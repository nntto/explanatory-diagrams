# 図解のプラクティス集

図を読みやすくする作法を、その根拠となる出典の引用とともにまとめる。色・線・大きさの決まりは [references/drawio-style.md](../references/drawio-style.md) に、どんな表現ができるかは [samples/README.md](../samples/README.md) にある。

## 一覧

| プラクティス | 要点 |
|---|---|
| [意味は対象のすぐ横に書き、凡例は共通の記法に使う](direct-labels/README.md) | 要素・線・系列の意味は、直接ラベルで書く。凡例は、繰り返し使う記法と量の尺度に使う |
| [図にするのは、文章や箇条書きでは読み取りにくい関係だけ](relations-not-text/README.md) | 箇条書きや表と同じ速さで読めるなら図にしない。文を箱に入れず、要素と関係で描く |
| [1 枚に主題を 1 つ、箱には見出しだけを書く](one-subject-short-labels/README.md) | 載せる要素を描く前に決める。箱は見出し 1 行と短い補足 1 行までにし、説明は本文に置く |

## プラクティスを増やす

プラクティスは 1 つにつき 1 つのディレクトリ `practices/<name>/` に置く。`README.md` にルール、ルールに従った図と従わない図を並べた `.drawio.svg` のサンプル、根拠となる出典の引用を書き、この一覧に行を足す。[drawio-style.md](../references/drawio-style.md) の決まりと食い違うなら、あわせて直す。
