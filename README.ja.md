[English](README.md) | [简体中文](README.zh-CN.md) | 日本語

# explanatory-diagrams

PR の説明や設計ドキュメントに載せる図を、コーディングエージェント（Claude Code、Codex）に draw.io で描かせる skill です。差分やメモ、画面の画像などを渡して頼むと、エージェントが図を描き、draw.io の編集データを埋め込んだ SVG（`.drawio.svg`）を返します。この SVG はふつうの画像として貼れて、draw.io で開けばそのまま直せます。

## 見本

**[見本の一覧（18 枚）](skills/explanatory-diagrams/templates/README.md)** に、変更前後の比べ方、リファクタリングの説明、構成図・シーケンス図・状態遷移図・ER 図などの見本を、使う場面と一緒に並べています。エージェントはこの一覧から近い見本を選び、その体裁に沿って描きます。

**AWS の構成図**：注文 API を 2 つのアベイラビリティゾーン（AZ）に置き、片方が止まっても注文を受け付けられるようにした構成です。リクエストの流れに、順に番号を振っています。

![注文 API を 2 つの AZ に置いた AWS 構成図。ALB が 2 つの AZ にリクエストを振り分け、RDS はスタンバイへ同期複製する](skills/explanatory-diagrams/templates/aws-architecture/aws-architecture.drawio.svg)

**画面を並べてデザインの変化を比べる**：テーマの色を変えた前後の画面を並べています。変わった部品を橙の枠で囲み、枠の番号で下の表の値と対応づけています。

![日付範囲の塗り、入力欄のフォーカスの輪、link ボタンの文字色を店の色に揃える変更を、変更前後の画面と値の表で比べた図](skills/explanatory-diagrams/templates/design-before-after/design-before-after.drawio.svg)

見本は人が仕上げたものです。エージェントが実際に返した図は[モデルごとの出力](#モデルごとの出力)にあります。

## なぜ draw.io で描くのか

![Mermaid・画像生成・draw.io を比べた表](docs/why-drawio.ja.drawio.svg)

## 入れ方

同じエージェントには、次のうち 1 つの方法で入れてください。

### A. skills CLI（おすすめ）

```sh
npx skills@latest add nntto/explanatory-diagrams --skill explanatory-diagrams -g -a claude-code -a codex
```

`-g` を外すと、今のプロジェクトだけに入ります。

### B. Claude Code のプラグイン

```sh
claude plugin marketplace add nntto/explanatory-diagrams
claude plugin install explanatory-diagrams@nntto
```

Claude Code 2.1.142 以降が必要です。

### C. 手で置く

```sh
git clone https://github.com/nntto/explanatory-diagrams.git
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.claude/skills/explanatory-diagrams
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.agents/skills/explanatory-diagrams
```

## 必要なもの

- **draw.io のデスクトップ版**：図を SVG に書き出すときに使います。skill のコマンドは macOS のパスで書いています。
- **python3**：画面の画像を図に埋め込むときに使います。
- **gh**：図を PR に貼るときに使います。

エージェントを OS のサンドボックスの中で動かしている場合は、[サンドボックスの設定](docs/sandbox.ja.md)も必要です。

## 使い方

図にしたいものをふだんの言葉で頼めば、エージェントがこの skill を読み込みます。

- 「この PR の変更を、PR の説明に載せる図にして。main との差分を見て。」
- 「infra.diff をもとに、構成の変更を図にして。」
- 「変更前後の画面の画像から、色の変更を比べる図を作って。」

skill を指定して呼ぶときは、Claude Code では `/explanatory-diagrams`（プラグインとして入れた場合は `/explanatory-diagrams:explanatory-diagrams`）、Codex では `$explanatory-diagrams` と入力します。

図の文言は、図を載せる文書の言語で書かれます。

## モデルごとの出力

同じ依頼と資料を 7 つのモデル（Claude の 4 つと Codex の 3 つ）に渡したときの出力を、[出力のページ](tests/skill-evals/explanatory-diagrams/README.md)に並べています。

## ライセンス

MIT ライセンスです（[LICENSE](LICENSE)）。ただし、見本と eval の出力に含まれる AWS のアイコンは対象外で、[AWS の規約](https://aws.amazon.com/architecture/icons/)に従います。
