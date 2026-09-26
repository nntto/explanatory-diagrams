# skill の eval

skill に同じ依頼を渡し、モデルごとにどんな成果物が出るかを並べて比べるための仕組みです。依頼文、入力ファイル、skill の中身、読み込ませる指示を固定し、モデルと effort だけを変えます。

いまは `explanatory-diagrams`（図解の skill）のケースだけがあります。モデルごとの出力は [explanatory-diagrams/README.md](explanatory-diagrams/README.md) に並べています。

## 固定するもの

| 固定するもの | 置き場所・方法 |
|---|---|
| 依頼文 | `cases/<case>/prompt.md` の本文。ふだん打つ短い依頼にし、出力の置き場所だけを指定する |
| 依頼の前提になる資料 | `cases/<case>/input/`。説明する対象のメモや、添付する画像。`setup.sh` が作業場所に置く |
| skill の中身 | 実行の最初に `results/<日時>/_skill/` へ写し、すべての実行でその写しを使う。commit と sha256 を記録する |
| 読み込ませる指示 | この skill と、環境の注意書き（下記）だけ。自分の CLAUDE.md、AGENTS.md、メモリ、ほかの skill、MCP は読ませない |
| 実行環境 | Claude も Codex も OS のサンドボックスの中で動かし、draw.io の書き出しだけを外で動かす |

モデルの出力は毎回ぶれるので、入力を固定しても同じ図にはなりません。ばらつきを見るときは `--runs 2` 以上で実行します。

### 隔離の方法

- **Claude**：`CLAUDE_CODE_DISABLE_CLAUDE_MDS`、`CLAUDE_CODE_DISABLE_AUTO_MEMORY`、`CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` を `1` にし、`--setting-sources project` でユーザー設定と skill を外す。skill は plugin の形に包んで `--plugin-dir` で渡す。Bash はサンドボックスの中で動かし、`excludedCommands` で draw.io だけを外に出す。書き込める場所は Codex にそろえ、作業場所・`$TMPDIR`・`/tmp` にする。
- **Codex**：実行ごとに一時的な `HOME` と `CODEX_HOME` を作る。`auth.json` は写さずにリンクだけを置き、実行後にディレクトリごと消す。`skills.bundled.enabled=false` と `--disable apps --disable plugins` で、この skill 以外を外す。使えるツールを Claude（シェル・ファイル編集・画像を見る）にそろえるため、`web_search="disabled"` と `--disable image_generation` で Web と画像生成を外す。`--sandbox workspace-write` で動かし、`rules/drawio.rules` で `draw.io -x` だけをサンドボックスの外で動かす。
- **環境の注意書き**：draw.io がサンドボックスの外で動くのは、ほかのコマンドとつなげずに単独で実行したときだけ。つなげるとサンドボックスの中で異常終了する。ふだんの環境にはない制約なので、同じ文を Claude には `--append-system-prompt`、Codex には一時的な `CODEX_HOME/AGENTS.md` で伝える。文は `run_skill_eval.py` の `ENV_NOTE` にあり、比較ページにも載る。

## 使い方

```bash
python3 tests/skill-evals/run_skill_eval.py run explanatory-diagrams
```

- `--model opus-5.5 gpt-6-sol` のように、`suite.json` の `models[].id` で絞れる。
- `--case 'design-*'` でケースを絞れる。
- `--jobs` は同時に動かす数（既定 3）。Claude の実行はどれも同じ利用上限を使う。
- 結果は `explanatory-diagrams/results/<日時>/` に出る。`compare.html` を開くと、固定した入力、近い見本、モデルごとの出力画像・時間・費用・skill を読んだかが並ぶ。
- 比較ページだけを作り直すときは `run_skill_eval.py report <結果のディレクトリ>`。

`results/` はコミットしません。残したい結果は `publish` で `explanatory-diagrams/outputs/` に写し、[explanatory-diagrams/README.md](explanatory-diagrams/README.md) を作り直してからコミットします。写すのは各モデルが `out/` に置いたファイルと、時間・費用・最後の返答などの記録（`runs.json`）です。やり取りの記録（`transcript.jsonl`）は大きいので写しません。

```bash
python3 tests/skill-evals/run_skill_eval.py publish tests/skill-evals/explanatory-diagrams/results/<日時>
```

- 公開済みのほかのモデルの結果は残り、同じモデルの結果は置き換わる。Claude と Codex を別々に実行しても、1 つの README に並ぶ。
- 依頼文か入力が公開済みの結果と違うときは、混ぜずに止まる。
- 出力を skill のフォルダに置かないのは、skill と一緒に配られるのを避けるためと、次の eval でモデルが見本と取り違えて写さないようにするため。

Claude Code に組み込みの `claude plugin eval` でも、同じケースを実行できる（Claude のモデルだけ）。ケースはその形式（`prompt.md`、`case.yaml`、`graders/`）で書いてある。

```bash
python3 tests/skill-evals/run_skill_eval.py official explanatory-diagrams --model sonnet-5
```

ただし、`~/.docker` の中にシンボリックリンクがある Mac では、Bash を許可した `claude plugin eval` は実行前に止まる（Docker の認証情報をサンドボックスで確実に隠せないため）。

## ケースを足す

1. `explanatory-diagrams/cases/<case>/` を作り、`prompt.md`（frontmatter と依頼文）、`case.yaml`、`setup.sh`、`input/`、`graders/` を置く。既存のケースを複製するのが早い。
2. 近い見本があれば、`suite.json` の `cases.<case>.references` に skill の中のパスを書く。比較ページで出力の横に並ぶ。
3. `setup.sh` が `input/` をそのまま写すだけでないときは、作業場所に何を置くかを `suite.json` の `cases.<case>.workspace` に書く。README の入力の欄に載る。たとえば `refactor-dependency-inversion` は、`input/before` と `input/after` から git リポジトリを組み立て、モデルには main との差分を読ませている。
4. 入力に業務固有の名前を入れない。画面の画像が必要なら、`sources/mock-admin-ui/` のような架空の画面から撮る。
5. 結果を公開したら、skill の README の「モデルごとの出力」の表に、ケースを 1 行足す（説明する変更と、渡した資料）。

## 画面の画像の作り方

`explanatory-diagrams/sources/mock-admin-ui/` は、AntD で作った架空の雑貨店の管理画面です。ケース `design-token-change` の入力画像と、skill の見本 `design-before-after` はここから撮りました。

```bash
cd tests/skill-evals/explanatory-diagrams/sources/mock-admin-ui
npm install
node shoot.js shots
```

## 前提

- Claude Code、Codex CLI、draw.io デスクトップ版（`/Applications/draw.io.app`）が入っていること。
- gpt-6 系のモデルは、新しい Codex CLI でないと動かない。使った版は比較ページに記録される。
