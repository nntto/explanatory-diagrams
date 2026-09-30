---
name: explanatory-diagrams
description: "Explains changes and systems with diagrams: before/after comparisons, architecture, data models, where state lives, and how items map to sets. Use when asked to draw, diagram, or visualize something for a PR description, design doc, or review reply. Draws with draw.io and returns an image with its editable source embedded, so the diagram can be edited later."
---

# 図解で説明する

説明したい関係に応じて、既存図の引用・再利用、draw.io での描画、画像生成を選ぶ。公表済みの技術では、原論文や公式資料の既存図も候補として探せる。図形や画像は、その追加によって対象や関係が伝わりやすくなる場合に使う。

画像生成は、その操作を扱う道具やスキル（imagegen など）を使う。

## 図で伝えること

説明対象の構造や振る舞いを、要素と関係からなるモデルとして描く。同じ対象に関わる複数の関係を結び付け、読み手が全体のつながりをたどれる図にする。

## 表す対象から図形を選ぶ

| 表す対象 | 図形・ライブラリの候補 |
|---|---|
| 抽象的な概念、集合と要素 | 基本図形、コンテナ、オイラー図 |
| 時間に沿ったやり取り | UML のシーケンス図 |
| 状態と遷移 | UML のステートマシン図 |
| 利用者、担当者、組織 | General の人物、UML Actor、Network、Clipart |
| テーブル、属性、キー、テーブル間の関係 | Entity Relation のテーブルと関係線 |
| クラウドのサービスや配置範囲 | AWS、Google Cloud、Azure のサービスアイコンとグループ |
| ソフトウェアの役割や境界 | UML、C4 |
| 業務の手順や担当範囲 | BPMN、スイムレーン |
| 実際の画面、既存資料の図 | 画像の埋め込み（後述） |

アセットの仕様や連携方法の参照先は [references/drawio-assets.md](references/drawio-assets.md) にある。

## 画像を埋め込む

draw.io は PNG などの画像を図の中に埋め込める。図形で描き直すより、実物を見せたほうが速く正確に伝わる場面で使う。埋め込んだ画像の上に枠・矢印・注釈を重ねると、実物と説明を1枚で対応づけられる。

| ユースケース | 図に何を重ねるか |
|---|---|
| 画面の前後比較 | 実画面を左右に並べ、変更した範囲を枠で囲む |
| 画面と実装の対応 | 画面を撮る道具（Playwright CLI など）で、撮影時に対象の要素を強調する。番号と対応表で、要素やデータの出どころを示す |
| 外部資料の図の利用 | 論文や公式ドキュメントの図を取り込み、番号で自分たちの構成と対応づける |

次の場合は埋め込まない、または加工してから埋め込む。

- 要素と関係を抽象化して伝えたい構造は、画像ではなく図形で描く。
- 個人情報や機密が写る画面は、マスクしてから取り込む。
- 縮小すると文字が潰れる画像は、必要な範囲だけ切り出す。

埋め込みの手順とサイズの目安は [references/drawio-workflow.md](references/drawio-workflow.md) にある。

## この skill が渡すもの

大きさ、配色、線と記号の規約は [references/drawio-style.md](references/drawio-style.md) にある。

凡例と直接ラベルの使い分けのように、図を読みやすくする作法とその根拠は [practices/README.md](practices/README.md) にある。

`samples/` の `.drawio.svg` は、この skill でどんな表現ができるかを示すサンプル。一覧と、それぞれが示している表現は [samples/README.md](samples/README.md) にある。サンプルは、変更前後の比べ方のような「見せ方」、それをよくあるリファクタリングに当てはめた「リファクタリングの説明」、構成図やシーケンス図のような「図の種類」に分かれている。

サンプルは型ではない。当てはまるものを選んで文言を差し替えるのではなく、説明する対象に合わせて図を組み立て、使えそうな表現をサンプルから取り入れる。たとえば変更を説明するときは、図の種類のサンプルの記法で描き、見せ方のサンプルの方法で変更点を示す。1 枚の図に、いくつかのサンプルの表現を組み合わせてよい。

図の文言は、図を載せる先の文書の言語で書く。

画像の取り込み、既存図の再利用、書き出し、確認は [references/drawio-workflow.md](references/drawio-workflow.md) に従う。

## サンプルを増やす

実案件の図をサンプルにするときは、業務固有の名前・PR 番号・チケット番号を一般的な名前に置き換える。`.drawio.svg` を書き出して `samples/<pattern>/` に置き、[samples/README.md](samples/README.md) の一覧に、そのサンプルが示す表現と画像を追加する。
