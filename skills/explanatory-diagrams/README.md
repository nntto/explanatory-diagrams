# explanatory-diagrams

PR 本文や設計ドキュメントに載せる説明図の描き方を揃える skill です。人が読むための一覧はこのファイル、エージェントの手順は [SKILL.md](SKILL.md)、draw.io の体裁は [references/](references/) にあります。

## 構成

| パス | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 手段の選び方、主題の決め方、draw.io で描くときの手順 |
| [references/drawio-assets.md](references/drawio-assets.md) | 図形・アイコンに関する公式資料の参照先 |
| [references/drawio-style.md](references/drawio-style.md) | 大きさ、配色、線と記号の規約 |
| [references/drawio-workflow.md](references/drawio-workflow.md) | 画像の埋め込み、PNG 書き出し、検収、PR への貼り付け |
| [templates/](templates/) | 見本の `.drawio.png`（編集元の XML を埋め込んだ PNG） |

draw.io 以外の手段（画像生成、デザインツール）は SKILL.md で振り分けだけを書いています。

## 見本の分け方

見本は 3 種類あります。

- **見せ方**：変更前後の比べ方など、どの図にも組み合わせられる体裁。
- **リファクタリングの説明**：見せ方を、よくあるリファクタリングに当てはめた例。
- **図の種類**：構成図、シーケンス図、状態遷移図など、記法ごとの見本。変更前後にはしていません。

たとえば AWS の構成の変更を説明するときは、「AWS 構成図」の記法で描き、「1 枚に差分を重ねる」の見せ方で変更点を示します。

図形で描いた見本は、同じ架空の EC サービス（注文・支払い・出荷）を題材にしています。デザインの変化とパレットの見本は、見本のために AntD で作った架空の雑貨店の管理画面のテーマを題材にしています。画面の画像はその画面を撮り（画面のソースは dotfiles リポジトリの `tests/skill-evals/explanatory-diagrams/sources/mock-admin-ui/`）、パレットの変更前の値は AntD が計算した値を載せています。ほかの画像を埋め込む 2 枚は、実物の画像を使っています。画面と実装の対応は Google 検索のトップページを引用し、外部資料の図の利用は MemGPT の論文の図を CC BY 4.0 のライセンスに従って載せています。引用元やライセンスなど、載せるために必要なことは、それぞれの図の中に書いています。画像はすべて `.drawio.png` で、draw.io で開くとそのまま編集できます。配色と線の意味は [references/drawio-style.md](references/drawio-style.md) にまとめています。

## 見せ方

### 左右に並べて比べる

使う場面：構造の違いそのものを見せたい変更。変更前と変更後で同じ枠組み（この例では層の帯）を共有し、変わったところだけが目に入るようにする。「3 つ → 1 つ」のような数の変化も添える。

![画面が外部 API を直接呼ぶ構造から、サービス層を通す構造への変更を左右に並べた図](templates/before-after-split/before-after-split.drawio.png)

### 1 枚に差分を重ねる

使う場面：全体の中の一部だけが変わる変更。変更後の図に、足したもの（青の枠）と消したもの（灰の破線と ✕）を重ねる。

![メール送信を SQS 経由にする変更を、AWS 構成図に重ねた図](templates/before-after-diff/before-after-diff.drawio.png)

### 画面を並べてデザインの変化を比べる

使う場面：色、余白、角丸など、見た目が変わる変更。変更前後の実画面を左右に並べ（横に長い部品は上下に並べ）、見てほしい部品を橙の枠で囲む。枠に番号を付け、変わった値の表と対応づける。

![日付範囲の塗りとフォーカスの輪、link の色を店の色に揃える変更を、変更前後の画面で比べた図](templates/design-before-after/design-before-after.drawio.png)

### 色のパレットを前後で比べる

使う場面：テーマの色の段階（背景・枠線・塗り・文字）をまとめて変える変更。段階を列にそろえ、変える色だけ変更前と変更後の行を上下に並べる。変えない色は 1 度だけ載せ、問題のある段階を橙の枠、変えた値を青の枠で囲む。

![主色の 10 段階を自分で決め、灰色の段階をなくす変更を、色のパレットで比べた図](templates/palette-before-after/palette-before-after.drawio.png)

## リファクタリングの説明

### 状態の置き場を移す

使う場面：フックやモジュールが持っていた状態を、別の場所へ切り出すリファクタリング。移す状態を橙、移した先を青で示し、状態の数が変わらないことも添える。

![useOrderEditor の状態を useDraft に切り出す変更を左右に並べた図](templates/refactor-move-state/refactor-move-state.drawio.png)

### 名前を揃える

使う場面：名前だけを変えるリファクタリング。名前を部品ごとに分けて表に並べ、規則から外れた名前と新しい名前を示す。呼び出し側で変わるところも並べる。

![フックの名前を use＋対象＋操作 に揃える変更の図](templates/refactor-rename/refactor-rename.drawio.png)

### 関数を切り出して公開する

使う場面：ファイルの中に閉じていた関数を切り出して公開するリファクタリング。今の利用関係は実線、後続の PR でつなぐ利用側は破線で示す。

![注文と表の変換を別ファイルに切り出して公開する変更を左右に並べた図](templates/refactor-extract-module/refactor-extract-module.drawio.png)

### 状態を共有する

使う場面：部品ごとに持っていた状態を、同じデータを扱う部品のあいだで 1 つにまとめるリファクタリング。状態の数の違い（3 つ → 1 つ）で変化を示し、移す前の位置を破線で残す。

![表ごとの「保存中」を注文ごとに 1 つにまとめる変更を左右に並べた図](templates/refactor-share-state/refactor-share-state.drawio.png)

### コピーして持ち回っていた値を削除する

使う場面：いくつかの段階にまたがる処理で、コピーして持ち回っていた値を削除し、どの処理も元の値を読むようにするリファクタリング。データ・読む処理・結果を帯に分け、変更前と変更後を 1 枚に重ねる。削除したものは橙の点線と打ち消し線、新しく読む値とそれによって変わる値は青で示す。

![商品データの取り込みバッチで、持ち回っていた display_name を削除し、どの処理も name を読むようにする変更の図](templates/refactor-remove-duplicate/refactor-remove-duplicate.drawio.png)

## 図の種類

### AWS 構成図

使う場面：サービスの配置と冗長化を説明する。AWS のアイコンとグループ（リージョン・VPC・AZ・サブネット）を使い、リクエストの流れに番号を振る。

![注文 API を 2 つの AZ に置いた AWS 構成図](templates/aws-architecture/aws-architecture.drawio.png)

### シーケンス図

使う場面：複数の参加者のあいだのやり取りを、順序どおりに説明する。同期・非同期・応答の矢印、活性区間、alt の枠を使い分ける。

![注文の確定から決済の完了までのシーケンス図](templates/sequence/sequence.drawio.png)

### 状態遷移図

使う場面：状態と、状態を移すイベント・条件・処理を説明する。遷移のラベルは「イベント [条件] / 処理」の順に書く。

![注文ステータスの状態遷移図](templates/state-machine/state-machine.drawio.png)

### C4 コンテナ図

使う場面：システムを構成するアプリ・DB・外部サービスと、そのあいだの関係を説明する。関係線には「何をするか」と「[技術]」を書く。

![注文システムの C4 コンテナ図](templates/c4-container/c4-container.drawio.png)

### ER 図

使う場面：テーブル・列・キーと、テーブル間の行数の関係を説明する。カラス足記法の記号の意味を凡例に示し、設計上の判断は注記で残す。

![注文・明細・支払いなどのテーブルの ER 図](templates/er-diagram/er-diagram.drawio.png)

### 業務フロー（BPMN）

使う場面：担当ごとの作業と分岐を説明する。レーンで担当を分け、人の作業とシステムの処理をマークで区別する。

![返品から返金までの業務フロー](templates/business-flow/business-flow.drawio.png)

### オイラー図（集合と要素）

使う場面：条件の組み合わせで決まる対象を説明する。集合を円、要素を点で置き、要素ごとの判定表を添える。

![メールの送り先を決める条件のオイラー図](templates/euler-sets/euler-sets.drawio.png)

### コンポーネントと状態

使う場面：画面の状態をどこが持ち、誰が読み書きするかを説明する。状態の種類は枠線（実線・破線・点線）で区別する。

![注文編集画面のコンポーネントツリーと状態の置き場](templates/state-ownership/state-ownership.drawio.png)

### コードと実行時の値

使う場面：入力によって、実行される行や返る値が変わる処理を説明する。コードの各行と、入力ごとに評価した値を同じ高さに並べる。

![送料を計算する関数と、3 つの入力で評価した値](templates/code-trace/code-trace.drawio.png)

### 画面と実装の対応

使う場面：画面のどこが、どの要素・コンポーネント・データから作られるかを説明する。撮影時に対象の要素を強調し（screen-capture skill の手順。見本は Playwright CLI の `highlight`）、図では番号と対応表を重ねる。見本は Google 検索のトップページ。

![Google 検索のトップページで強調した検索の部分と、HTML の要素の対応](templates/screenshot-annotation/screenshot-annotation.drawio.png)

### 外部資料の図の利用

使う場面：公表済みの構成や設計を採用する設計ドキュメント。資料の図は描き直さずに埋め込み、番号で自分たちの構成と対応づけ、出典・利用条件・加工内容を残す。見本は、CC BY 4.0 で公開されている MemGPT の論文の図を載せた。

![MemGPT の論文の Figure 3 と、返品対応エージェントの記憶の置き場の対応](templates/reference-figure/reference-figure.drawio.png)

## テンプレートの追加

1. 業務固有の名前、PR 番号、チケット番号を一般的な名前に置き換えた図を用意する。
2. [references/drawio-workflow.md](references/drawio-workflow.md) の手順で `.drawio.png` を書き出し、`templates/<pattern>/` に置く。
3. この README の「見せ方」「リファクタリングの説明」「図の種類」のうち当てはまる節に、使う場面と画像を追加する。

## モデルごとの出力

この skill に同じ依頼を渡したとき、モデルごとにどんな図が返るかを、別のページ（dotfiles リポジトリの [tests/skill-evals/explanatory-diagrams](https://github.com/nntto/dotfiles/blob/main/tests/skill-evals/explanatory-diagrams/README.md)）に並べています。Claude の 4 モデルと Codex の 3 モデルで、どれも 1 回ずつ実行した結果です。上の見本は人が仕上げた完成形で、こちらは依頼して実際に返ってきた図です。

| ケース | 説明する変更 | 渡した資料 |
|---|---|---|
| [aws-infra-change](https://github.com/nntto/dotfiles/blob/main/tests/skill-evals/explanatory-diagrams/README.md#aws-infra-change) | 商品画像の置き場を EFS から S3 に移し、CloudFront から配信する | 変更のメモと、Terraform の差分・変更後の一式 |
| [design-token-change](https://github.com/nntto/dotfiles/blob/main/tests/skill-evals/explanatory-diagrams/README.md#design-token-change) | 状態の色（成功・警告・エラー）を店の色に合わせる | 変更のメモと、変更前後の画面の画像 4 枚 |
| [refactor-dependency-inversion](https://github.com/nntto/dotfiles/blob/main/tests/skill-evals/explanatory-diagrams/README.md#refactor-dependency-inversion) | 出荷の処理が SDK を直接呼ばないよう、依存の向きを逆にする | git リポジトリ（main と作業ブランチ）と、変更のメモ |

出力の画像は、skill と一緒に配られないよう、また次の eval でモデルが見本と取り違えないよう、skill のフォルダの外に置いています。
