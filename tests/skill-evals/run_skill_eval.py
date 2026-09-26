#!/usr/bin/env python3
"""skill の出力を、入力を固定したままモデルごとに比べる。

入力として固定するもの:
  - 依頼文（cases/<case>/prompt.md の本文）と、作業場所に置く入力（setup.sh が cases/<case>/input/ をもとに置く）
  - skill の中身（実行の最初に results/<日時>/_skill/ へ写し、全実行でその写しを使う）
  - 読み込ませる指示: この skill と、環境の注意書き（ENV_NOTE）だけ。自分の CLAUDE.md・AGENTS.md・メモリ・ほかの skill・MCP は読ませない
  - 実行環境: どちらも OS のサンドボックスの中で動かし、draw.io の書き出しだけを外で動かす

使い方:
  python3 tests/skill-evals/run_skill_eval.py run explanatory-diagrams [--case GLOB] [--model ID ...] [--runs N] [--jobs N]
  python3 tests/skill-evals/run_skill_eval.py report tests/skill-evals/explanatory-diagrams/results/<日時>
  python3 tests/skill-evals/run_skill_eval.py publish tests/skill-evals/explanatory-diagrams/results/<日時>  # outputs/ と README を更新する
  python3 tests/skill-evals/run_skill_eval.py official explanatory-diagrams [--model ID ...]   # claude plugin eval で実行する
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import fnmatch
import hashlib
import json
import re
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

EVALS_ROOT = Path(__file__).resolve().parent
REPO = EVALS_ROOT.parents[1]
IGNORED = {"__pycache__", ".DS_Store", "results"}
# 図として扱う拡張子。skill の出力とサンプルは .drawio.svg にしたが、それより前の記録は .drawio.png なので両方を扱う
IMAGE_SUFFIXES = (".svg", ".png")
# plugin の形に包むときの名前。.claude-plugin/marketplace.json の plugin 名にそろえる
PLUGIN_NAME = "explanatory-diagrams"
CLAUDE_TOOLS = ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill", "TodoWrite"]
# eval の環境だけにある制約を、どちらのモデルにも同じ文で伝える（Claude はシステムプロンプト、Codex は AGENTS.md）。
# ふだんの環境では draw.io をどう呼んでも動くので、この制約で出来が左右されないようにする。
ENV_NOTE = ("この環境では、シェルのコマンドは OS のサンドボックスの中で動く。"
            "draw.io の書き出し（{drawio} -x ...）だけはサンドボックスの外で動くが、"
            "ほかのコマンドと &&、;、パイプ、改行でつなげず、単独で実行したときに限る。"
            "つなげるとサンドボックスの中で動き、異常終了する。")
_print_lock = threading.Lock()


def log(*args):
    with _print_lock:
        print(*args, flush=True)


# ---------- 入力の読み込みと指紋 ----------

def load_suite(name: str) -> tuple[Path, dict]:
    suite_dir = EVALS_ROOT / name
    return suite_dir, json.loads((suite_dir / "suite.json").read_text())


def split_front_matter(text: str) -> tuple[dict, str]:
    """prompt.md の frontmatter（key: value の 1 行だけ扱う）と本文に分ける。"""
    if not text.startswith("---\n"):
        return {}, text.strip()
    head, _, body = text[4:].partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            meta[key.strip()] = value.strip()
    return meta, body.strip()


def tree_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and not (set(p.relative_to(root).parts) & IGNORED))


def fingerprint(root: Path) -> str:
    """ディレクトリ内のファイル名と中身から sha256 を作る。同じ入力なら同じ値になる。"""
    h = hashlib.sha256()
    for p in tree_files(root):
        h.update(str(p.relative_to(root)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def git_state(path: Path) -> dict:
    def git(*args):
        return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True).stdout.strip()
    return {"commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain", "--", str(path)))}


def tool_version(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"unavailable: {e}"


def copy_tree(src: Path, dst: Path):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*IGNORED))


# ---------- 1 回の実行 ----------

def claude_command(model: dict, prompt: str, plugin_dir: Path, drawio: str) -> tuple[list[str], dict]:
    settings = {"sandbox": {
        "enabled": True,
        "autoAllowBashIfSandboxed": True,
        "allowUnsandboxedCommands": False,
        # draw.io（Electron）はサンドボックスの中では異常終了するので、このコマンドだけ外で動かす
        "excludedCommands": [f"{drawio}:*"],
        # Codex の workspace-write と同じく、作業場所と $TMPDIR に加えて /tmp に書けるようにする
        "filesystem": {"allowWrite": ["/tmp"]},
    }}
    cmd = ["claude", "-p", prompt,
           "--model", model["model"], "--effort", model["effort"],
           "--setting-sources", "project", "--settings", json.dumps(settings),
           "--plugin-dir", str(plugin_dir), "--strict-mcp-config", "--no-session-persistence",
           "--allowedTools", ",".join(CLAUDE_TOOLS),
           "--append-system-prompt", ENV_NOTE.format(drawio=drawio),
           "--output-format", "stream-json", "--verbose"]
    env = {**os.environ,
           "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1",
           "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
           "CLAUDE_CODE_DISABLE_BUNDLED_SKILLS": "1"}
    return cmd, env


def codex_home(tmp: Path, skill_snapshot: Path, drawio: str) -> Path:
    """自分の AGENTS.md・メモリ・ほかの skill を読ませないための一時的な CODEX_HOME を作る。"""
    home = tmp / ".codex"
    (home / "skills").mkdir(parents=True)
    (home / "rules").mkdir()
    real = Path.home() / ".codex"
    os.symlink(real / "auth.json", home / "auth.json")  # 認証情報は写さずリンクだけ置く
    if (real / "models_cache.json").exists():
        shutil.copy2(real / "models_cache.json", home / "models_cache.json")
    copy_tree(skill_snapshot, home / "skills" / skill_snapshot.name)
    (home / "AGENTS.md").write_text(ENV_NOTE.format(drawio=drawio) + "\n")
    (home / "rules" / "drawio.rules").write_text(
        "# draw.io（Electron）はサンドボックスの中では異常終了するので、書き出しだけを外で動かす\n"
        f'prefix_rule(pattern=["{drawio}", "-x"], decision="allow")\n')
    return home


def codex_command(model: dict, prompt: str, workspace: Path, home: Path) -> tuple[list[str], dict]:
    cmd = ["codex", "exec", "-m", model["model"],
           "-c", f'model_reasoning_effort="{model["effort"]}"',
           "-c", "skills.bundled.enabled=false",
           # Claude に渡すツール（シェル・ファイル編集・画像を見る）にそろえ、Web と画像生成は外す
           "-c", 'web_search="disabled"', "--disable", "image_generation",
           "--disable", "apps", "--disable", "plugins",
           "--skip-git-repo-check", "--ephemeral", "--json",
           "-C", str(workspace), "--sandbox", "workspace-write", prompt]
    env = {**os.environ, "HOME": str(home.parent), "CODEX_HOME": str(home)}
    return cmd, env


def summarize_claude(lines: list[dict], skill_name: str) -> dict:
    s = {"final_message": "", "cost_usd": None, "turns": None, "tool_calls": 0, "skill_used": False, "usage": None}
    for e in lines:
        if e.get("type") == "assistant":
            for c in e.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    s["tool_calls"] += 1
                    blob = json.dumps(c.get("input", {}), ensure_ascii=False)
                    if skill_name in blob and (c.get("name") == "Skill" or "SKILL.md" in blob):
                        s["skill_used"] = True
        if e.get("type") == "result":
            s.update(final_message=e.get("result") or "", cost_usd=e.get("total_cost_usd"),
                     turns=e.get("num_turns"), usage=e.get("usage"), is_error=e.get("is_error"))
    return s


def summarize_codex(lines: list[dict], skill_name: str) -> dict:
    s = {"final_message": "", "cost_usd": None, "turns": 0, "tool_calls": 0, "skill_used": False,
         "usage": {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0}, "errors": []}
    for e in lines:
        item = e.get("item") or {}
        if e.get("type") == "item.completed" and item.get("type") == "agent_message":
            s["final_message"] = item.get("text", "")
        if e.get("type") == "item.completed" and item.get("type") == "command_execution":
            s["tool_calls"] += 1
            if f"{skill_name}/SKILL.md" in item.get("command", ""):
                s["skill_used"] = True
        if e.get("type") == "turn.completed":
            s["turns"] += 1
            for k in s["usage"]:
                s["usage"][k] += (e.get("usage") or {}).get(k, 0)
        if e.get("type") in ("error", "turn.failed"):
            s["errors"].append(e.get("message") or json.dumps(e.get("error"), ensure_ascii=False))
    return s


def claude_plugin(tmp: Path, skill_snapshot: Path) -> Path:
    """skill を plugin の形に包む。名前は公開している plugin（PLUGIN_NAME）にそろえる。"""
    plugin = tmp / "plugin"
    (plugin / ".claude-plugin").mkdir(parents=True)
    (plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps(
        {"name": PLUGIN_NAME, "version": "0.0.0", "description": "eval のために包んだ skill"}))
    copy_tree(skill_snapshot, plugin / "skills" / skill_snapshot.name)
    return plugin


def run_once(job: dict) -> dict:
    case, model, run_no = job["case"], job["model"], job["run_no"]
    run_dir: Path = job["run_dir"]
    run_dir.mkdir(parents=True, exist_ok=True)
    # skill の写しも作業場所も、実行ごとの一時ディレクトリに置く。
    # リポジトリの中に置くと、ケースの定義やほかの実行の結果をモデルが読めてしまう。
    tmp = Path(tempfile.mkdtemp(prefix="work-"))
    workspace = tmp / "work"
    workspace.mkdir()
    subprocess.run(["bash", str(case["dir"] / "setup.sh")], cwd=workspace, check=True)

    if model["vendor"] == "claude":
        cmd, env = claude_command(model, case["prompt"], claude_plugin(tmp, job["skill_snapshot"]), job["drawio"])
    else:
        home = codex_home(tmp / "home", job["skill_snapshot"], job["drawio"])
        cmd, env = codex_command(model, case["prompt"], workspace, home)

    log(f"start  {case['name']} / {model['id']} / run {run_no}")
    started = time.time()
    timed_out = False
    with open(run_dir / "transcript.jsonl", "wb") as out, open(run_dir / "stderr.log", "wb") as err:
        proc = subprocess.Popen(cmd, cwd=workspace, env=env, stdin=subprocess.DEVNULL,
                                stdout=out, stderr=err, start_new_session=True)
        try:
            proc.wait(timeout=job["timeout"])
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
    elapsed = time.time() - started

    # 作業場所に残ったもの（入力を除く）を結果として残す
    shutil.copytree(workspace, run_dir / "workspace",
                    ignore=lambda d, names: [n for n in names if Path(d) == workspace and n in ("input", ".claude")],
                    symlinks=True)
    shutil.rmtree(tmp, ignore_errors=True)

    events = []
    for line in (run_dir / "transcript.jsonl").read_text(errors="replace").splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    summarize = summarize_claude if model["vendor"] == "claude" else summarize_codex
    summary = summarize(events, job["skill_name"])
    outputs = sorted(str(p.relative_to(run_dir)) for p in (run_dir / "workspace").rglob("*") if p.suffix in IMAGE_SUFFIXES)
    meta = {"case": case["name"], "model": model, "run": run_no, "command": cmd[:1] + [a if a != case["prompt"] else "<prompt>" for a in cmd[1:]],
            "exit_code": proc.returncode, "timed_out": timed_out, "seconds": round(elapsed, 1),
            "outputs": outputs, **summary}
    (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    status = "timeout" if timed_out else ("ok" if proc.returncode == 0 else f"exit {proc.returncode}")
    log(f"finish {case['name']} / {model['id']} / run {run_no}: {status}, {len(outputs)} png, {elapsed:.0f}s")
    return meta


# ---------- run ----------

def select_cases(suite_dir: Path, pattern: str | None) -> list[dict]:
    cases = []
    for d in sorted((suite_dir / "cases").iterdir()):
        if not (d / "prompt.md").exists() or (pattern and not fnmatch.fnmatch(d.name, pattern)):
            continue
        meta, prompt = split_front_matter((d / "prompt.md").read_text())
        cases.append({"name": d.name, "dir": d, "prompt": prompt, "meta": meta})
    return cases


def cmd_run(args):
    suite_dir, suite = load_suite(args.suite)
    skill_dir = REPO / suite["skill"]
    models = [m for m in suite["models"] if not args.model or m["id"] in args.model]
    cases = select_cases(suite_dir, args.case)
    if not cases or not models:
        sys.exit("ケースかモデルが見つからない")

    out = suite_dir / "results" / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    snapshot = out / "_skill" / skill_dir.name  # 記録と、サンプルを写しただけの出力の見分けに使う。実行には一時ディレクトリの写しを渡す
    copy_tree(skill_dir, snapshot)
    for c in cases:
        copy_tree(c["dir"] / "input", out / "_inputs" / c["name"])

    manifest = {
        "suite": args.suite, "started_at": dt.datetime.now().isoformat(timespec="seconds"),
        "skill": {"path": suite["skill"], "sha256": fingerprint(skill_dir), **git_state(skill_dir)},
        "cases": [{"name": c["name"], "prompt": c["prompt"], "prompt_sha256": sha256_text(c["prompt"]),
                   "input_sha256": fingerprint(c["dir"] / "input"),
                   "input_files": [str(p.relative_to(c["dir"] / "input")) for p in tree_files(c["dir"] / "input")],
                   "references": suite.get("cases", {}).get(c["name"], {}).get("references", [])} for c in cases],
        "models": models, "runs": args.runs,
        "tools": {"claude": tool_version(["claude", "--version"]), "codex": tool_version(["codex", "--version"]),
                  "drawio": suite["drawio"]},
        "environment_note": ENV_NOTE.format(drawio=suite["drawio"]),
        "isolation": {
            "claude": "CLAUDE_CODE_DISABLE_{CLAUDE_MDS,AUTO_MEMORY,BUNDLED_SKILLS}=1, --setting-sources project, "
                      "--plugin-dir（この skill だけ）, --strict-mcp-config, sandbox.enabled（draw.io だけ除外、/tmp に書ける）, "
                      "環境の注意書きを --append-system-prompt で渡す",
            "codex": "一時的な HOME と CODEX_HOME（auth.json はリンク）, skills.bundled.enabled=false, "
                     "--disable apps/plugins/image_generation, web_search=disabled, "
                     "--sandbox workspace-write（draw.io -x だけ rules で外へ）, "
                     "環境の注意書きを CODEX_HOME/AGENTS.md で渡す",
        },
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    jobs = [{"case": c, "model": m, "run_no": r, "run_dir": out / c["name"] / m["id"] / f"run-{r}",
             "skill_snapshot": snapshot, "skill_name": skill_dir.name,
             "drawio": suite["drawio"], "timeout": args.timeout or int(c["meta"].get("timeout_seconds", 1800))}
            for c in cases for m in models for r in range(1, args.runs + 1)]
    log(f"{len(jobs)} 回の実行を始める → {out}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for f in concurrent.futures.as_completed([pool.submit(run_once, j) for j in jobs]):
            try:
                f.result()
            except Exception as e:  # 1 回の失敗で全体を止めない
                log(f"error: {e!r}")
    write_run_readme(out)


# ---------- 結果のページ（Markdown） ----------


def cmd_report(args):
    write_run_readme(Path(args.results).resolve())


def image_hashes(root: Path) -> dict:
    return {hashlib.sha256(p.read_bytes()).hexdigest(): str(p.relative_to(root))
            for p in root.rglob("*") if p.suffix in IMAGE_SUFFIXES}


def scrub_paths(text: str) -> str:
    """最後の返答に残る、実行ごとの一時ディレクトリの絶対パスを <workspace> に置き換える（マシン固有の情報を公開しない）。

    Markdown のリンク先を `(</abs/.../out/a.svg>)` のように山かっこで囲んだパスは、囲みごと置き換える。
    パスの前半だけを置き換えると `<<workspace>/out/a.svg>` になるため。山かっこの中はスペースを含んでよい。"""
    workspace = r"(?:/private)?(?:/var/folders/[^\s)`\]]*?|/tmp)/work-[^/\s)`\]]+/work"
    text = re.sub(rf"<{workspace}([^<>\n]*)>", r"<workspace>\1", text)
    return re.sub(workspace, "<workspace>", text)


def token_counts(vendor: str, usage: dict | None) -> tuple[int | None, int | None]:
    if not usage:
        return None, None
    if vendor == "claude":
        total_in = sum(usage.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    else:
        total_in = usage.get("input_tokens", 0)
    return total_in, usage.get("output_tokens")


def run_record(run_dir: Path, manifest: dict, m: dict, templates: dict, target: Path | None = None) -> dict:
    """1 回の実行（results/<日時>/<case>/<model>/run-N/）の記録を、runs.json の 1 件の形にする。

    target を渡すと出力の図をそこへ写し、パスを outputs/<case>/ からの相対にする（publish）。
    渡さないと写さず、パスを results/<日時>/<case>/ からの相対にする（実行結果のページ）。"""
    meta = json.loads((run_dir / "meta.json").read_text())
    workspace = run_dir / "workspace"
    out_dir = workspace / "out"
    found = [(f, f.relative_to(out_dir), False) for f in sorted(out_dir.rglob("*")) if f.is_file()] if out_dir.exists() else []
    # out/ に図が 1 枚もないときは、ほかの場所に置いた図を写す。置き場所を取り違えたことも結果として残す
    # （out/ に図があるときに外まで拾うと、作業途中の切り抜きなどが混じる）
    if not any(f.suffix in IMAGE_SUFFIXES for f, _, _ in found):
        found += [(f, f.relative_to(workspace), True) for f in sorted(workspace.rglob("*")) if f.suffix in IMAGE_SUFFIXES]
    files = []
    for f, rel, outside in found:
        if target is not None:
            (target / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target / rel)
            path = f"{m['id']}/{run_dir.name}/{rel}"
        else:
            path = str(f.relative_to(run_dir.parents[1]))
        files.append({"path": path, "outside_out": outside, "location": str(f.relative_to(workspace)),
                      "same_as_template": templates.get(hashlib.sha256(f.read_bytes()).hexdigest())})
    tokens_in, tokens_out = token_counts(m["vendor"], meta.get("usage"))
    return {"run": meta["run"], "started_at": manifest["started_at"], "seconds": meta["seconds"],
            "cost_usd": meta.get("cost_usd"), "input_tokens": tokens_in, "output_tokens": tokens_out,
            "tool_calls": meta["tool_calls"], "skill_used": meta["skill_used"],
            "exit_code": meta["exit_code"], "timed_out": meta["timed_out"], "errors": meta.get("errors") or [],
            "final_message": scrub_paths(meta["final_message"]), "files": files,
            "skill": manifest["skill"], "cli": manifest["tools"].get(m["vendor"])}


def cmd_publish(args):
    """results/<日時>/ の出力と記録を outputs/<case>/<model>/ へ写し、スイートの README を作り直す。

    ほかのモデルの公開済みの結果は残す。同じモデルの結果は置き換える。
    依頼文・入力・skill の中身のどれかが公開済みのものと違うときは、混ぜずに止める。
    skill を直したら、全モデルを実行し直してから、outputs/<case>/ を消して公開する。"""
    src = Path(args.results).resolve()
    manifest = json.loads((src / "manifest.json").read_text())
    suite_dir, suite = load_suite(manifest["suite"])
    templates = image_hashes(src / "_skill" / Path(manifest["skill"]["path"]).name)
    for case in manifest["cases"]:
        dest = suite_dir / "outputs" / case["name"]
        runs_path = dest / "runs.json"
        data = json.loads(runs_path.read_text()) if runs_path.exists() else {}
        fixed = {"prompt_sha256": case["prompt_sha256"], "input_sha256": case["input_sha256"]}
        if data and {k: data.get(k) for k in fixed} != fixed:
            sys.exit(f"{case['name']}: 依頼文か入力が、公開済みの結果と違う。outputs/{case['name']}/ を消してから公開する")
        published = {r["skill"]["sha256"] for m in data.get("models", {}).values() for r in m["runs"]}
        if published - {manifest["skill"]["sha256"]}:
            sys.exit(f"{case['name']}: skill の中身が、公開済みの結果と違う。全モデルを実行し直し、outputs/{case['name']}/ を消してから公開する")
        data.update(case=case["name"], **fixed, environment_note=manifest.get("environment_note"))
        models = data.setdefault("models", {})
        for m in manifest["models"]:
            run_dirs = [src / case["name"] / m["id"] / f"run-{r}" for r in range(1, manifest["runs"] + 1)]
            run_dirs = [d for d in run_dirs if (d / "meta.json").exists()]
            if not run_dirs:
                continue
            shutil.rmtree(dest / m["id"], ignore_errors=True)
            runs = [run_record(run_dir, manifest, m, templates, target=dest / m["id"] / run_dir.name) for run_dir in run_dirs]
            models[m["id"]] = {"vendor": m["vendor"], "model": m["model"], "effort": m["effort"], "runs": runs}
            log(f"公開: {case['name']} / {m['id']}（{len(runs)} 回）")
        dest.mkdir(parents=True, exist_ok=True)
        runs_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    write_suite_readme(suite_dir, suite)


def run_anchor(case: str, mid: str, run: dict, runs: list) -> str:
    """同じモデル名の見出しがケースの数（と実行の回数）だけ並ぶので、表から飛ぶ先はケース名つきのアンカーにする。"""
    return f"{case}-{mid.replace('.', '')}" + (f"-run{run['run']}" if len(runs) > 1 else "")


def md_cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def write_suite_readme(suite_dir: Path, suite: dict):
    """outputs/*/runs.json から、ケースごとにモデルの出力を並べた README を作る。"""
    skill_dir = REPO / suite["skill"]
    order = [m["id"] for m in suite["models"]]
    case_dirs = [d for d in sorted((suite_dir / "cases").iterdir()) if (suite_dir / "outputs" / d.name / "runs.json").exists()]
    # skill をこのリポジトリに移す前の記録は、runs.json の skill に repo がある。
    # publish はケースの中で skill の中身が違う結果を混ぜないので、移す前の記録かどうかはケースごとに決まる
    old_cases = [d.name for d in case_dirs if all(
        r["skill"].get("repo") for m in json.loads((suite_dir / "outputs" / d.name / "runs.json").read_text())["models"].values() for r in m["runs"])]
    whose = "公開している記録は、どれも " if len(old_cases) == len(case_dirs) else f"ケース {'、'.join(old_cases)} の記録は、"
    history = [whose + "skill をこのリポジトリに移す前に、dotfiles（非公開）で実行したものである。"
               "当時の skill は図を PNG（`.drawio.png`）で書き出しており、今の skill は SVG（`.drawio.svg`）で書き出す。"
               "「実行の条件」の表にある commit は移す前のリポジトリのもので、このリポジトリの履歴にはない。", ""] if old_cases else []
    lines = [f"# {suite_dir.name}：モデルごとの出力", "",
             "同じ入力（依頼文・資料・画像・skill の中身）を渡したときに、モデルごとに返ってきた図を並べている。"
             "skill の説明はリポジトリの [README](../../../README.md)（[日本語](../../../README.ja.md)、[简体中文](../../../README.zh-CN.md)）に、"
             "eval の仕組みと実行のしかたは [../README.md](../README.md) にある。", "",
             *history,
             "ケースの題材（雑貨店の EC サイトと管理画面）、人名・住所・電話番号・注文番号・数値・業務のルールは、どれもこの eval のために作った架空のものである。", "",
             "どのモデルも 1 回ずつしか実行していないので、同じモデルでも実行し直せば図は変わる。"
             "時間は複数の実行を同時に動かして測ったので、目安として見てほしい。"
             "Codex CLI は費用を返さないので、Codex のモデルの費用は「—」にしている。"
             "この README と `outputs/` は `python3 tests/skill-evals/run_skill_eval.py publish <結果のディレクトリ>` で作り直すので、手では編集しない。", ""]
    for case_dir in case_dirs:
        meta, _ = split_front_matter((case_dir / "prompt.md").read_text())
        lines.append(f"- [{case_dir.name}](#{case_dir.name})：{meta.get('description', '')}")
    lines.append("")
    for case_dir in case_dirs:
        data = json.loads((suite_dir / "outputs" / case_dir.name / "runs.json").read_text())
        lines += case_section(case_dir, data, suite, suite_dir / "outputs" / case_dir.name, suite_dir)
    (suite_dir / "README.md").write_text("\n".join(lines))
    log(f"README: {suite_dir / 'README.md'}")


def write_run_readme(out: Path):
    """results/<日時>/ に、その実行の結果を公開ページと同じ書き方で並べた README.md を作る。図はどこにも写さない。"""
    manifest = json.loads((out / "manifest.json").read_text())
    suite_dir, suite = load_suite(manifest["suite"])
    templates = image_hashes(out / "_skill" / Path(manifest["skill"]["path"]).name)
    sk = manifest["skill"]
    lines = [f"# {manifest['suite']}：{manifest['started_at']} の実行結果", "",
             "公開する前に見るためのページ。残す結果は `python3 tests/skill-evals/run_skill_eval.py publish "
             f"{os.path.relpath(out, REPO)}` で outputs/ に写す。", "",
             f"- skill：`{sk['path']}`、sha256 `{sk['sha256'][:12]}`、commit `{sk['commit'][:7]}`{'（未コミットの変更あり）' if sk['dirty'] else ''}",
             f"- CLI：{manifest['tools'].get('claude')}／{manifest['tools'].get('codex')}"]
    lines += [f"- {vendor} の隔離：{text}" for vendor, text in manifest["isolation"].items()]
    lines.append("")
    by_name = {d.name: d for d in (suite_dir / "cases").iterdir()}
    for case in manifest["cases"]:
        models = {}
        for m in manifest["models"]:
            run_dirs = [out / case["name"] / m["id"] / f"run-{r}" for r in range(1, manifest["runs"] + 1)]
            runs = [run_record(d, manifest, m, templates) for d in run_dirs if (d / "meta.json").exists()]
            if runs:
                models[m["id"]] = {"vendor": m["vendor"], "model": m["model"], "effort": m["effort"], "runs": runs}
        data = {"prompt_sha256": case["prompt_sha256"], "input_sha256": case["input_sha256"],
                "environment_note": manifest.get("environment_note"), "models": models}
        lines += case_section(by_name[case["name"]], data, suite, out / case["name"], out)
    (out / "README.md").write_text("\n".join(lines))
    log(f"結果のページ: {out / 'README.md'}")


def case_section(case_dir: Path, data: dict, suite: dict, files_root: Path, page_dir: Path) -> list[str]:
    """1 つのケースの節（依頼文、入力、モデルごとの表と出力、実行の条件）を作る。

    リンクはすべて、ページを置くディレクトリ（page_dir）からの相対パスにする。
    files_root は、data の files[].path の起点（outputs/<case>/ か results/<日時>/<case>/）。"""
    skill_dir = REPO / suite["skill"]
    order = [m["id"] for m in suite["models"]]
    rel = lambda path: os.path.relpath(path, page_dir)
    cdir = rel(case_dir)
    base = rel(files_root)
    lines = []
    _, prompt = split_front_matter((case_dir / "prompt.md").read_text())
    lines += [f"## {case_dir.name}", "", f"依頼文（[prompt.md]({cdir}/prompt.md)）", ""]
    lines += [f"> {line}" if line else ">" for line in prompt.splitlines()] + [""]
    case_conf = suite.get("cases", {}).get(case_dir.name, {})
    workspace = case_conf.get("workspace", "作業場所の `input/` に置いて渡す")
    lines += [f"入力（[input/]({cdir}/input/)。[setup.sh]({cdir}/setup.sh) が{workspace}）", ""]
    inputs = tree_files(case_dir / "input")
    # 画像は下の表に並べるので、ここには画像以外を直下の単位で載せる（ソース一式のようなディレクトリは 1 行にまとめる）
    for top in sorted((case_dir / "input").iterdir()):
        files = [f for f in inputs if f.suffix not in IMAGE_SUFFIXES and (f == top or top in f.parents)]
        if files:
            label = top.name if top.is_file() else f"{top.name}/（{len(files)} ファイル）"
            lines.append(f"- [{label}]({cdir}/input/{top.name})")
    # 変更前（before）の画像を変更後（after）より先に並べる
    images = sorted((f for f in inputs if f.suffix in IMAGE_SUFFIXES),
                    key=lambda f: [{"before": "0", "after": "1"}.get(part, part) for part in f.parts])
    if images:
        lines += ["", "<table><tr>"]
        for f in images:
            rel_ = f.relative_to(case_dir / "input")
            lines.append(f'<td><img src="{cdir}/input/{rel_}" width="220"><br><code>{rel_}</code></td>')
        lines.append("</tr></table>")
    refs = case_conf.get("references", [])
    if refs:
        lines += ["", "関連するサンプル（skill の中）：" + "、".join(
            f"[{Path(r).parent.name}]({rel(skill_dir / r)})" for r in refs)]

    models = sorted(data["models"].items(), key=lambda kv: order.index(kv[0]) if kv[0] in order else len(order))
    lines += ["", "| モデル | effort | 時間 | 費用の目安 | トークン（入力／出力） | ツール | skill | 出力 |", "|---|---|---|---|---|---|---|---|"]
    for mid, m in models:
        for run in m["runs"]:
            cost = f"${run['cost_usd']:.2f}" if run.get("cost_usd") is not None else "—"
            tokens = f"{run['input_tokens']:,}／{run['output_tokens']:,}" if run.get("input_tokens") is not None else "—"
            status = "時間切れ" if run["timed_out"] else ("" if run["exit_code"] == 0 else f"終了コード {run['exit_code']}")
            outs = "、".join(Path(f["path"]).name + ("（out/ の外）" if f.get("outside_out") else "")
                            + ("（サンプルと同じ）" if f["same_as_template"] else "") for f in run["files"]) or "なし"
            lines.append(f"| [{mid}](#{run_anchor(case_dir.name, mid, run, m['runs'])}) | {m['effort']} | {run['seconds']:.0f} 秒 | {cost} | {tokens} | "
                         f"{run['tool_calls']} 回 | {'読んだ' if run['skill_used'] else '読んでいない'} | "
                         f"{md_cell(status + ('：' if status else '') + outs)} |")

    for mid, m in models:
        for run in m["runs"]:
            heading = mid + (f"（run {run['run']}）" if len(m["runs"]) > 1 else "")
            lines += ["", f'<a id="{run_anchor(case_dir.name, mid, run, m["runs"])}"></a>', "", f"### {heading}", "", f"`{m['model']}`、effort {m['effort']}、{run['started_at']} に実行", ""]
            images = [f for f in run["files"] if f["path"].endswith(IMAGE_SUFFIXES)]
            for f in run["files"]:
                if f["path"].endswith(IMAGE_SUFFIXES):
                    lines.append(f"![{mid} の出力：{Path(f['path']).name}]({base}/{f['path']})")
                    if f.get("outside_out"):
                        lines.append(f"\n{Path(f['path']).name} は、依頼した out/ ではなく `{f.get('location') or f['path'].split('/', 2)[2]}` に置かれていた。")
                    if f["same_as_template"]:
                        lines.append(f"\n{Path(f['path']).name} はサンプル `{f['same_as_template']}` と同じ画像（サンプルを写しただけ）。")
                    lines.append("")
                else:
                    lines.append(f"- [{Path(f['path']).name}]({base}/{f['path']})")
            if not images:
                lines.append("図の出力なし。")
            for err in run["errors"]:
                lines.append(f"\nエラー：`{md_cell(err)[:300]}`")
            fence = "~~~~" if "~~~" not in run["final_message"] else "`````"
            lines += ["", "<details><summary>最後の返答</summary>", "", f"{fence}text", run["final_message"].strip(), fence, "", "</details>"]

    lines += ["", "### 実行の条件", "", f"依頼文の sha256 `{data['prompt_sha256'][:12]}`、入力の sha256 `{data['input_sha256'][:12]}`。", "",
              "| モデル | 実行日時 | skill の sha256 | commit | CLI |", "|---|---|---|---|---|"]
    for mid, m in models:
        for run in m["runs"]:
            s = run["skill"]
            # 移す前のリポジトリで実行した記録は、commit がこのリポジトリのものではないことを書き添える
            where = f"、{s['repo']}" if s.get("repo") else ""
            lines.append(f"| {mid} | {run['started_at']} | `{s['sha256'][:12]}` | `{s['commit'][:7]}`{where}{'（未コミットの変更あり）' if s['dirty'] else ''} | {md_cell(run['cli'])} |")
    if data.get("environment_note"):
        lines += ["", f"環境の注意書き（どのモデルにも同じ文で渡した）：{data['environment_note']}"]
    lines.append("")
    return lines


# ---------- official（claude plugin eval） ----------

def cmd_official(args):
    """同じケースを claude plugin eval で実行する。skill の写しとケースを 1 つの plugin に包んで渡す。"""
    suite_dir, suite = load_suite(args.suite)
    skill_dir = REPO / suite["skill"]
    out = suite_dir / "results" / (dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-official")
    plugin = out / "_plugin"
    (plugin / ".claude-plugin").mkdir(parents=True)
    (plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps(
        {"name": PLUGIN_NAME, "version": "0.0.0", "description": "eval のために包んだ skill"}))
    copy_tree(skill_dir, plugin / "skills" / skill_dir.name)
    copy_tree(suite_dir / "cases", plugin / "evals")  # claude plugin eval は evals/ を読み、実行中のモデルからは隠す
    models = [m for m in suite["models"] if m["vendor"] == "claude" and (not args.model or m["id"] in args.model)]
    for m in models:
        cmd = ["claude", "plugin", "eval", str(plugin), "--scaffold", "--trust-plugin", "--no-publish",
               "--ablation", "none", "--runs", str(args.runs), "--model", m["model"],
               "--output-dir", str(out / m["id"]), "--allow-tools", "Bash", "Write", "Edit"]
        if args.case:
            cmd[4:4] = ["--case", args.case]
        log("$ " + " ".join(cmd))
        subprocess.run(cmd)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)
    r = sub.add_parser("run", help="モデルごとに実行し、結果のページ（results/<日時>/README.md）を作る")
    r.add_argument("suite")
    r.add_argument("--case", help="ケース名の glob")
    r.add_argument("--model", nargs="+", help="suite.json の models[].id")
    r.add_argument("--runs", type=int, default=1)
    r.add_argument("--jobs", type=int, default=3)
    r.add_argument("--timeout", type=int, help="1 回の上限（秒）。省略時は prompt.md の timeout_seconds")
    r.set_defaults(func=cmd_run)
    rep = sub.add_parser("report", help="結果のディレクトリから、結果のページを作り直す")
    rep.add_argument("results")
    rep.set_defaults(func=cmd_report)
    pub = sub.add_parser("publish", help="結果の出力と記録を outputs/ へ写し、スイートの README を作り直す")
    pub.add_argument("results")
    pub.set_defaults(func=cmd_publish)
    o = sub.add_parser("official", help="claude plugin eval で実行する（Claude のモデルだけ）")
    o.add_argument("suite")
    o.add_argument("--case")
    o.add_argument("--model", nargs="+")
    o.add_argument("--runs", type=int, default=1)
    o.set_defaults(func=cmd_official)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
