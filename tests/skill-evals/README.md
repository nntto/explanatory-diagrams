# skill の eval

skill に同じ依頼を渡し、モデルごとにどんな成果物が出るかを並べて比べる仕組み。依頼文、入力ファイル、skill の中身、読み込ませる指示を固定し、モデルと effort だけを変える。

いまは `explanatory-diagrams`（図解の skill）のケースだけがある。skill の本体は [skills/explanatory-diagrams/](../../skills/explanatory-diagrams/) にあり、`explanatory-diagrams/suite.json` の `skill` がこの場所を指す。モデルごとの出力は [explanatory-diagrams/README.md](explanatory-diagrams/README.md) に並べている。

公開している記録は、skill をこのリポジトリに移す前に実行したもの（[公開済みの記録](#公開済みの記録)）。

## 固定するもの

| 固定するもの | 置き場所・方法 |
|---|---|
| 依頼文 | `cases/<case>/prompt.md` の本文。ふだん打つ短い依頼にし、出力の置き場所だけを指定する |
| 依頼の前提になる資料 | `cases/<case>/input/`。説明する対象のメモや、添付する画像。`setup.sh` が作業場所に置く |
| skill の中身 | 実行の最初に `results/<日時>/_skill/` へ写し、すべての実行でその写しを使う。commit と sha256 を記録する |
| 読み込ませる指示 | この skill と、環境の注意書き（下記）だけ。自分の CLAUDE.md、AGENTS.md、メモリ、ほかの skill、MCP は読ませない |
| 実行環境 | Claude も Codex も OS のサンドボックスの中で動かし、draw.io の書き出しだけを外で動かす |

モデルの出力は毎回ぶれるので、入力を固定しても同じ図にはならない。ばらつきを見るときは `--runs 2` 以上で実行する。

### 隔離の方法

- **Claude**：`CLAUDE_CODE_DISABLE_CLAUDE_MDS`、`CLAUDE_CODE_DISABLE_AUTO_MEMORY`、`CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` を `1` にし、`--setting-sources project` でユーザー設定と skill を外す。skill は plugin の形に包んで `--plugin-dir` で渡す。Bash はサンドボックスの中で動かし、`excludedCommands` で draw.io だけを外に出す。書き込める場所は Codex にそろえ、作業場所・`$TMPDIR`・`/tmp` にする。
- **Codex**：実行ごとに一時的な `HOME` と `CODEX_HOME` を作る。`auth.json` は写さずにリンクだけを置き、実行後にディレクトリごと消す。`skills.bundled.enabled=false` と `--disable apps --disable plugins` で、この skill 以外を外す。使えるツールを Claude（シェル・ファイル編集・画像を見る）にそろえるため、`web_search="disabled"` と `--disable image_generation` で Web と画像生成を外す。`--sandbox workspace-write` で動かし、`rules/drawio.rules` で `draw.io -x` だけをサンドボックスの外で動かす。
- **環境の注意書き**：draw.io がサンドボックスの外で動くのは、ほかのコマンドとつなげずに単独で実行したときだけ。つなげるとサンドボックスの中で異常終了する。ふだんの環境にはない制約なので、同じ文を Claude には `--append-system-prompt`、Codex には一時的な `CODEX_HOME/AGENTS.md` で伝える。文は `run_skill_eval.py` の `ENV_NOTE` にあり、結果のページにも載る。

## 使い方

リポジトリのルートで実行する。

```bash
python3 tests/skill-evals/run_skill_eval.py run explanatory-diagrams
```

- `--model opus-5.5 gpt-6-sol` のように、`suite.json` の `models[].id` で絞れる。
- `--case 'design-*'` でケースを絞れる。
- `--jobs` は同時に動かす数（既定 3）。Claude の実行はどれも同じ利用上限を使う。
- 結果は `explanatory-diagrams/results/<日時>/` に出る。そこの `README.md` に、依頼文と入力、近い見本、モデルごとの出力の図・時間・費用・skill を読んだかが、公開ページと同じ書き方で並ぶ。
- 結果のページだけを作り直すときは `run_skill_eval.py report <結果のディレクトリ>`。

`results/` はコミットしない。残したい結果は `publish` で `explanatory-diagrams/outputs/` に写し、[explanatory-diagrams/README.md](explanatory-diagrams/README.md) を作り直してからコミットする。写すのは各モデルが `out/` に置いたファイルと、時間・費用・最後の返答などの記録（`runs.json`）。やり取りの記録（`transcript.jsonl`）は大きいので写さない。

```bash
python3 tests/skill-evals/run_skill_eval.py publish tests/skill-evals/explanatory-diagrams/results/<日時>
```

- 公開済みのほかのモデルの結果は残り、同じモデルの結果は置き換わる。Claude と Codex を別々に実行しても、1 つの README に並ぶ。
- 依頼文・入力・skill の中身のどれかが公開済みの結果と違うときは、混ぜずに止まる。
- 依頼文・入力・skill を直したら、全モデルを実行し直す。最初の publish の前に一度だけ `outputs/<case>/` を消す。Claude と Codex を別々に publish するときも、消すのは 1 回でよい。同じ依頼文・入力・skill で実行した結果は、止まらずに並ぶ。
- 最後の返答に残る、実行ごとの一時ディレクトリの絶対パスは、`<workspace>` に置き換えて写す。
- 出力を skill のフォルダに置かないのは、skill と一緒に配られるのを避けるためと、次の eval でモデルが見本と取り違えて写さないようにするため。

Claude Code に組み込みの `claude plugin eval` でも、同じケースを実行できる（Claude のモデルだけ）。ケースはその形式（`prompt.md`、`case.yaml`、`graders/`）で書いてある。合格条件は、Skill ツールを使ったこと（`graders/skill-used.md`）と、`out/` に `.drawio.svg` があること（`graders/diagram-svg.md`）。

```bash
python3 tests/skill-evals/run_skill_eval.py official explanatory-diagrams --model sonnet-5
```

## 公開済みの記録

`explanatory-diagrams/outputs/` の記録は、skill をこのリポジトリに移す前に、dotfiles（非公開）で実行したもの。

- その時の skill は、図を PNG（`.drawio.png`）で書き出していた。いまの skill は SVG（`.drawio.svg`）で書き出す。公開している出力が PNG なのはそのため。いまの合格条件（`graders/diagram-svg.md`）は `.drawio.svg` を見るので、この PNG は合格条件には合わない。
- `runs.json` の各実行の `skill` にある `path` と `commit` は、移す前のリポジトリのもの。このリポジトリの履歴にはない。そのことを示すため、`skill.repo` に「移す前の dotfiles（非公開）」と書いた。[explanatory-diagrams/README.md](explanatory-diagrams/README.md) の「実行の条件」の表にも、commit の横に書き添えている。
- いまの skill で実行した結果は、skill の中身が違うので、そのままでは publish が止まる。実行し直す手順は「[使い方](#使い方)」に書いた。

## ケースを足す

1. `explanatory-diagrams/cases/<case>/` を作り、`prompt.md`（frontmatter と依頼文）、`case.yaml`、`setup.sh`、`input/`、`graders/` を置く。既存のケースを複製するのが早い。
2. 近い見本があれば、`suite.json` の `cases.<case>.references` に skill の中のパス（`templates/<name>/<name>.drawio.svg`）を書く。結果のページと公開ページに、近い見本として載る。
3. `setup.sh` が `input/` をそのまま写すだけでないときは、作業場所に何を置くかを `suite.json` の `cases.<case>.workspace` に書く。README の入力の欄に載る。たとえば `refactor-dependency-inversion` は、`input/before` と `input/after` から git リポジトリを組み立て、モデルには main との差分を読ませている。
4. 入力には実在の会社・人・業務の資料を使わず、架空の題材にする。画面の画像が必要なら、`sources/mock-admin-ui/` のような架空の画面から撮る。
5. 結果を公開したら、ルートの [README.md](../../README.md#output-by-model)（Output by model）、[README.ja.md](../../README.ja.md#モデルごとの出力)（モデルごとの出力）、[README.zh-CN.md](../../README.zh-CN.md#各模型的输出)（各模型的输出）の表に、ケースを 1 行足す（説明する変更と、渡した資料）。

## 画面の画像の作り方

`explanatory-diagrams/sources/mock-admin-ui/` は、AntD で作った架空の雑貨店の管理画面。ケース `design-token-change` の入力画像と、skill の見本 `design-before-after` はここから撮った。店、人名、住所、電話番号、注文は、すべて架空のもの。ケースの入力（`cases/*/input/`）にある人名・住所・数値・業務のルールも架空。

```bash
cd tests/skill-evals/explanatory-diagrams/sources/mock-admin-ui
npm install
node shoot.js shots
```

## 前提

- 公開している記録は、移す前の dotfiles で、macOS と draw.io デスクトップ版（`/Applications/draw.io.app`）を使って実行した。ほかの OS では試していない。
- このリポジトリに移してから（SVG で書き出すいまの skill で）は、run・publish・official をまだ実行していない。
- Claude Code、Codex CLI、draw.io デスクトップ版が入っていること。
- gpt-6 系のモデルは、古い Codex CLI では動かなかった。どの版から動くかは確かめていない。公開している記録は codex-cli 0.156.0 で実行した。使った版は結果のページと、[explanatory-diagrams/README.md](explanatory-diagrams/README.md) の「実行の条件」の表に記録される。
- 確かめた Mac では、`~/.docker` の中にシンボリックリンクがあると、Bash を許可した `claude plugin eval` が実行前に止まった。
