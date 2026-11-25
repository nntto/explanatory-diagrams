# 図にするのは、文章より速く読み取れる関係があるときだけ

図は、文章や箇条書き、表より速く読み取れる関係があるときだけ描く。描く前に、同じ内容を文章や箇条書き、表にしても同じ速さで読めるかを考える。読めるなら、図にしない。

文を箱に入れて並べただけの図は、文章より読みやすくならない。配置や線で関係が読み取れる形にする。図の配置や形で何が速く読み取れるのかを言えないなら、文章だけにする。

## サンプル

題材は、サンプルのために作った架空のもの。

![注文確定の処理を、左は文を箱に入れて、右は要素と関係で示した図。右では、注文 API が在庫 API と決済 API を並行して呼び、両方が注文 DB に書く](relations-not-text.drawio.svg)

注文確定の処理を、左は文を箱に入れて、右は要素と関係で示した。左は、箇条書きを読むのと変わらない。右では、注文 API から 2 つの API への分岐と、注文 DB への合流が、形で分かる。

## 根拠

- "Diagrammatic representations also typically display information that is only implicit in sentential representations" / "problem solving can proceed through a smooth traversal of the diagram, and may require very little search" — Larkin, J. H. & Simon, H. A. (1987). [Why a diagram is (sometimes) worth ten thousand words](https://doi.org/10.1111/j.1551-6708.1987.tb00863.x)（要旨。同じ情報でも、図は位置で情報を整理するので探す手間が減る）
