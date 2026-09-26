# draw.io での画像の取り込み・書き出し

## 既存図の再利用

既存図を使う場合は、出典 URL、図番号やページ、利用条件、切り出しなどの変更内容を残す。加工後も、凡例・矢印・数値条件など、図の意味を支える情報との対応を保つ。

CC BY などのライセンスで公開されている図は、ライセンスの条件に従って載せる。CC BY 4.0 なら、著作者、題名、出典の URL、ライセンスの名前と URL を図の中に書く。切り出しや番号の追加などの変更をしたときは、そのことも書く。

利用の許諾がない他者の著作物は、引用の要件を満たすと確かめられる場合に限り、引用として載せる。確かめられないときは、許諾を得るか、自作の画面や図に差し替える。

図の中では、次のことを満たす。これだけで引用の要件がそろうとは限らない。公表された著作物であることや、説明に引用が必要であることなども要る。

- 引用した部分に「引用」と見出しを付け、枠などで自分の説明と区別する。
- 図の主役は自分の説明にし、引用はその説明に必要な範囲にとどめる。
- 著作者、題名、掲載日、URL を引用元として書く。撮影した画面なら撮影日も書く。
- 引用した図や画面は変えない。番号や枠を加えたときは、引用者が加えたものだと書く。

引用の要件とこの書き方は、日本の著作権法の引用の考え方に沿っている。ほかの国では条件が違う。

## 画像の埋め込み

アプリのスクリーンショット、見た目の回帰テスト（VRT）の基準画像、既存資料の図などを図の中に取り込める。どの場面で使うかは [SKILL.md](../SKILL.md) の「画像を埋め込む」にある。

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
- 書き出した図で、スクリーンショット内の文字が読めるかを確認する。縮小しすぎると文字が潰れる。

画面の前後比較の見本は [templates/design-before-after](../templates/design-before-after/design-before-after.drawio.svg) にある。

他者の画面や資料を取り込むときは、既存図の再利用と同じく出典と利用条件を残す。

- 画面の要素を強調するときは、画面を撮る道具で、撮影時に強調する（Playwright CLI なら `highlight`）。図では番号と説明だけを重ねる。
- Web ページに載っている図は、ページを開いて図の要素だけを撮影して取り込める（Playwright CLI なら `screenshot <要素>`）。図の中の文字が潰れないよう、解像度を上げて撮る。出典の URL と撮影日を残す。

## 書き出し

図は、編集元の XML を埋め込んだ SVG（`.drawio.svg`）1 つで渡す。表示用の画像と編集用の `.drawio` を別々に残さない。

書き出す前に、XML の `<mxGraphModel>` に `background="#ffffff"` を付ける。ほかの属性はそのまま残す。見本から取り出した XML には、すでに付いている。

```xml
<mxGraphModel background="#ffffff" ...>
```

draw.io のデスクトップ版で、XML から `.drawio.svg` を書き出す。次のコマンドは macOS の場合の例。ほかの OS では、`/Applications/draw.io.app/Contents/MacOS/draw.io` を draw.io の実行ファイルのパスに置き換える。ほかの OS では試していない。

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f svg -e -b 20 --embed-svg-fonts false --theme light -o fig.drawio.svg fig.drawio
```

- `-e` は編集元の XML を SVG に埋め込む。この SVG を draw.io で開くと、元の図として編集できる。SVG 1 つが表示と編集元を兼ねる。
- `-b` は余白（px）。
- `--embed-svg-fonts false` を付ける。付けないと、draw.io が文字のラベルを 1 つずつ PNG の画像にして埋め込み、ファイルが大きくなる。見本の 1 枚では、付けると 71KB、付けないと 1.1MB だった。
- 白の背景（`background="#ffffff"`）と `--theme light` は両方付ける。
  - 白の背景を付けないと、背景が透明になる。GitHub のダークモードでは、暗い背景に暗い文字が乗って読めなくなる。
  - `--theme light` を付けないと、色が `light-dark()` で見る人の配色に合わせて変わり、描いた色のとおりに表示されない。
- 拡張子は `.drawio.svg` にする。編集元を含む SVG だと分かる。
- 大きさの目安は [drawio-style.md](drawio-style.md) の「大きさ」にある。
- 書き出した図をブラウザで開き、文字と線の読みやすさ、説明する対象の対応・個数・関係が保たれていることを確認する。macOS の Quick Look のサムネイルは図の端を切り落とすので、確認に使わない。
- XML の `fig.drawio` は書き出し用の中間ファイル。書き出した後は残さない。

## `.drawio.svg` を編集する

テンプレートや既存の図を XML で編集するときは、`.drawio.svg` から XML を取り出し、編集後に `.drawio.svg` へ書き出し直す。

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f xml -o fig.drawio fig.drawio.svg
# fig.drawio を編集する
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f svg -e -b 20 --embed-svg-fonts false --theme light -o fig.drawio.svg fig.drawio
```

取り出した XML は、属性の順序や `x="0"` の省略など表記が変わることがあるが、図の内容は変わらない。

数値から決まる境界や探索経路などを示す場合は、図が示す条件と結果を原典や計算で確かめる。確認できない主張は、根拠のある範囲へ修正するか、図から外す。
