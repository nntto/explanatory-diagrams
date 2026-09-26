# draw.io での画像の取り込み・書き出し・貼り付け

## 既存図の再利用

既存図を使う場合は、出典 URL、図番号やページ、利用条件、切り出しなどの変更内容を残す。加工後も、凡例・矢印・数値条件など、図の意味を支える情報との対応を保つ。

CC BY などのライセンスで公開されている図は、ライセンスの条件に従って載せる。CC BY 4.0 なら、著作者、題名、出典の URL、ライセンスの名前と URL を図の中に書く。切り出しや番号の追加などの変更をしたときは、そのことも書く。見本の [templates/reference-figure](../templates/reference-figure/reference-figure.drawio.png) は、CC BY 4.0 で公開されている論文の図を、この形で載せている。

利用の許諾がない他者の著作物は、引用として載せる。引用として扱うために、図の中で次のことを満たす。

- 引用した部分に「引用」と見出しを付け、枠などで自分の説明と区別する。
- 図の主役は自分の説明にし、引用はその説明に必要な範囲にとどめる。
- 著作者、題名、掲載日、URL を引用元として書く。撮影した画面なら撮影日も書く。
- 引用した図や画面は変えない。番号や枠を加えたときは、引用者が加えたものだと書く。

見本の [templates/screenshot-annotation](../templates/screenshot-annotation/screenshot-annotation.drawio.png) は、この形で Google 検索のトップページを引用している。

## 画像の埋め込み

アプリのスクリーンショット、VRT の基準画像、既存資料の図などを図の中に取り込める。どの場面で使うかは [SKILL.md](../SKILL.md) の「画像を埋め込む」にある。

画像は data URI として図の XML に埋め込む。埋め込むことで図がファイル1つで完結し、共有先やリポジトリの移動で画像が失われない。外部ファイルへの参照は避ける。

```xml
<mxCell id="shot" value=""
  style="shape=image;html=1;imageAspect=0;image=data:image/png,iVBORw0KGgoAAAANSUhEUg..."
  vertex="1" parent="1">
  <mxGeometry x="80" y="200" width="320" height="380" as="geometry" />
</mxCell>
```

data URI は PNG から作る。

```bash
python3 -c 'import base64,sys; print("data:image/png," + base64.b64encode(open(sys.argv[1],"rb").read()).decode())' shot.png
```

- `image=data:image/png,` の後ろに base64 を続ける。draw.io はカンマ以降を base64 として解釈する。`data:image/png;base64,` と書くとエラーにならず、画像が描画されないまま空白になる。
- `mxGeometry` の `width` と `height` は元画像の縦横比に合わせる。`imageAspect=0` を指定すると、指定した寸法のまま描画する。
- 強調したい範囲は、画像の上に `fillColor=none` の矩形を重ねる。XML で後に記述したセルが前面に描画される。
- base64 化すると元ファイルサイズの約 1.33 倍になる。数百 KB までは実用上問題ない。大きい画像は縮小するか、必要な範囲だけ切り出してから埋め込む。
- 書き出した PNG で、スクリーンショット内の文字が読めるかを確認する。縮小しすぎると文字が潰れる。

他者の画面や資料を取り込むときは、既存図の再利用と同じく出典と利用条件を残す。

- 画面の要素を強調するときは、screen-capture skill の手順に従い、撮影時に強調する（Playwright CLI なら `highlight`）。図では番号と説明だけを重ねる。
- Web ページに載っている図は、ページを開いて図の要素だけを撮影して取り込める（Playwright CLI なら `screenshot <要素>`）。図の中の文字が潰れないよう、解像度を上げて撮る。出典の URL と撮影日を残す。

見本は [templates/screenshot-annotation](../templates/screenshot-annotation/screenshot-annotation.drawio.png)（画面と実装の対応）と [templates/reference-figure](../templates/reference-figure/reference-figure.drawio.png)（外部資料の図の利用）にある。画面の前後比較は [templates/design-before-after](../templates/design-before-after/design-before-after.drawio.png) にある。

## 書き出し

図は、編集元の XML を埋め込んだ PNG（`.drawio.png`）1 つで渡す。表示用の PNG と編集用の `.drawio` を別々に残さない。

macOS の draw.io デスクトップ版で、XML から `.drawio.png` を書き出す。

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -e -s 2 -b 20 -o fig.drawio.png fig.drawio
```

- `-e` は編集元の XML を PNG に埋め込む。この PNG を draw.io で開くと元の図として編集できるので、PNG 1 つが表示と編集元を兼ねる。
- 拡張子は `.drawio.png` にする。編集元を含む PNG だと分かる。
- `-s` は拡大率、`-b` は余白（px）。幅 1000px 以内で描いた図を `-s 2` で書き出すと、PR の表示幅（814px）に縮んでも高精細の画面でにじまない。大きさの目安は [drawio-style.md](drawio-style.md) の「大きさ」にある。
- 書き出した PNG で、文字と線の読みやすさ、説明する対象の対応・個数・関係が保たれていることを確認する。
- XML の `fig.drawio` は書き出し用の中間ファイル。書き出した後は残さない。

## `.drawio.png` を編集する

テンプレートや既存の図を XML で編集するときは、`.drawio.png` から XML を取り出し、編集後に `.drawio.png` へ書き出し直す。

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f xml -o fig.drawio fig.drawio.png
# fig.drawio を編集する
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -e -s 2 -b 20 -o fig.drawio.png fig.drawio
```

取り出した XML は、属性の順序や `x="0"` の省略など表記が変わることがあるが、図の内容は変わらない。

数値から決まる境界や探索経路などを示す場合は、図が示す条件と結果を原典や計算で確かめる。確認できない主張は、根拠のある範囲へ修正するか、図から外す。

## PR への貼り付け

- 本文は `--body-file`、画像は `--attach` で渡す。本文中の同じローカルパスの画像参照は、アップロード先の URL に置き換わる。

```bash
gh pr edit -R <owner/repo> <number> --body-file body.md --attach './fig.drawio.png#alt'
```

- 添付するのは `.drawio.png`。編集元は PNG に含まれるため、`.drawio` の XML を本文に同梱しない。`--attach` は画像と動画しか受け付けず、`.drawio` は渡せない。
- `.drawio.png` はリポジトリにコミットしない。設計ドキュメントとして残す場合だけ、`docs/` 配下に `.drawio.png` を置く。
- scratchpad などリポジトリ外から実行するときは `-R` が必要。
