# 図解のプラクティス集

図を読みやすくする作法を、その根拠となる出典の引用とともにまとめる。色・線・大きさの決まりは [references/drawio-style.md](../references/drawio-style.md) に、どんな表現ができるかは [samples/README.md](../samples/README.md) にある。

## 一覧

| プラクティス | 要点 |
|---|---|
| [意味は対象のすぐ横に書き、凡例は共通の記法に使う](direct-labels/README.md) | 要素・線・系列の意味は、直接ラベルで書く。凡例は、繰り返し使う記法と量の尺度に使う |
| [置き場所を帯で分け、同じ形には同じ意味を 1 つだけ持たせる](layers-and-shapes/README.md) | 帯で置き場所の境界を示し、形・線・置き場所に意味を 1 つずつ持たせる。アイコンは、形を見て意味が分かるときだけ使う |

## プラクティスを増やす

プラクティスは 1 つにつき 1 つのディレクトリ `practices/<name>/` に置く。`README.md` にルール、ルールに従った図と従わない図を並べた `.drawio.svg` のサンプル、根拠となる出典の引用を書き、この一覧に行を足す。[drawio-style.md](../references/drawio-style.md) の決まりと食い違うなら、あわせて直す。
