# 図解のプラクティス集

図を読みやすくする作法を、根拠とともにまとめる。色・線・大きさの決まりは [references/drawio-style.md](../references/drawio-style.md) に、どんな表現ができるかは [samples/README.md](../samples/README.md) にある。ここでは、そう描く理由と、根拠の確かさを示す。

根拠は、実証研究（メタ分析を含む）、専門家や公的機関のガイド、規格・仕様に分けて書く。教材の学習や統計グラフで得られた結果を PR や設計ドキュメントの図に当てはめた箇所は、その旨が分かるように書く。

## 一覧

| プラクティス | 要点 | サンプル |
|---|---|---|
| [意味は対象のすぐ横に書き、凡例は共通の記法に使う](#意味は対象のすぐ横に書き凡例は共通の記法に使う) | 要素・線・系列の意味は、直接ラベルで書く。凡例は、繰り返し使う記法と量の尺度に使う | [direct-labels/](direct-labels/) |

## 意味は対象のすぐ横に書き、凡例は共通の記法に使う

要素、線、グラフの系列が何を表すかは、その対象のすぐ横に書く。これを直接ラベルと呼ぶ。凡例は、同じ記法を何度も使うときや、色の濃さで量を読ませるときに使う。目的は凡例をなくすことではなく、「どれが何か」を確かめるためだけに、凡例と図のあいだを行き来させないことである。

### 描き方

1. 要素名、系列名、変更点、遷移の条件は、対象のすぐ横に書く。凡例を見ないと意味が分からない図にしない。
2. 同じ色・線種・記号を図の中で何度も使うときは、その意味を凡例にまとめてよい。個々の名前や条件は、凡例があっても対象の横に書く。
3. ラベル同士が重なる、対象を隠す、文字が小さくなるときは、まず名前を短くするか、図を分ける。それでも収まらなければ、見せたい要素に絞って直接ラベルを付け、残りは凡例にまとめる。重なりと文字の読みやすさは、PR 本文の幅（約 814px）に縮めて確かめる。
4. 凡例を使うときは、対象の近くに置き、図の中の並びと同じ順に並べる。置き場所を見出しの下に固定しない。
5. 色の濃さや大きさで量を読ませるときは、値と単位を書いた尺度の凡例を残す。
6. UML・BPMN・ER のように記法が決まっている図では、記号の意味を変えない。読み手が知らないかもしれない記号だけを凡例で補い、要素名や条件は対象の横に書く。
7. ラベルの文字を線と同じ色にするかは任意とする。同じ色にするなら、白地とのコントラストが 4.5:1 以上の色に限る。この skill の配色では、primary の青（6.5:1）と補足の文字色（5.0:1）は基準を満たすが、secondary の橙（3.2:1）、灰（3.0:1）、薄い灰（2.5:1）は満たさない。基準を満たさない色の線は、補足の文字色で名前を書き、位置や引き出し線で線と対応させる。
8. 図の要旨と、大事な関係や変更は、本文や代替テキストにも書く。画像の中のラベルだけでは、スクリーンリーダーの利用者に伝わらないことがある。

### サンプル

題材と数値は、サンプルのために作った架空のもの。

#### 説明図

![確認メールの送信をキューに任せる変更を、左は凡例で、右は直接ラベルで示した図。右では「追加」「消した直接の送信」「応答の後で送る」を対象の横に書いている](direct-labels/direct-labels-diagram.drawio.svg)

確認メールの送信をキューに任せる変更を、左は凡例で、右は直接ラベルで示した。右では「追加」「消した直接の送信」「応答の後で送る」を対象の横に書いたので、凡例と図を行き来しなくても読める。色と線の種類はどちらにも残しており、右では文字でも同じ意味を示している。

#### チャート

![API ごとの応答時間 p95 の折れ線グラフを、左は凡例で、右は線の端の系列名で示した図。注文確定の p95 は 5 週目のキャッシュ追加で約 850ms から約 400ms に下がっている](direct-labels/direct-labels-chart.drawio.svg)

API ごとの応答時間 p95 を、左は凡例で、右は線の端の系列名で示した。右では、見てほしい「注文確定」だけを青の太字にし、ほかの系列名は補足の文字色で書いた。橙や薄い灰の線の名前を線と同じ色で書くと、白地とのコントラストが足りないため、文字の色ではなく位置で線と対応させている。

### 根拠

| 分かっていること | 根拠 | 種類と確かさ |
|---|---|---|
| 関連する文章と図を近くに置くと、学習の成績が上がる | [R4] 58 の比較（計 2,426 人）のメタ分析で、効果量 g = 0.63 | メタ分析。教材の学習については強い根拠。PR や設計図を読む速さや、レビューでの見落としへの効果は調べていない |
| 図の中の対応する箇所の近くに説明を書くと、番号付きの凡例で説明するより、対応する箇所へ視線が多く向かう。ただし、成績の差は出ないことがある | [R5] 実験 1・2 では、近くに書いた形が応用問題（転移テスト）で上回った（d = 0.80、0.73）。番号付きの凡例と比べた実験 3 では d = 0.35 で有意差がなく、対応する箇所への視線移動だけが多かった（d = 1.35） | 査読付きの実証研究。説明図に近い条件での比較だが、結果は比べた条件で分かれる |
| 凡例を使うなら、図の中の並びと凡例の順をそろえると速く読める | [R1] そろえた場合とそろえない場合で、棒グラフの複雑な比較は 3.85 秒と 4.83 秒、6 系列の折れ線は 5.70 秒と 6.45 秒だった。図と凡例のあいだの視線の往復も減った | 査読付きの実証研究（各 18 人）。凡例どうしを比べたもので、直接ラベルと比べたものではない |
| 複数の図で凡例の順を統一しても、図ごとの並びに合わせた場合と比べて、はっきりした差は出ていない | [R2] 図ごとに合わせた場合（17.54 秒）と統一した場合（18.26 秒）の差は有意でなかった | 査読付きの実証研究（24 人）。条件が限られる |
| 折れ線は線の端に系列名を書くと読みやすい。棒グラフでは凡例が要ることが多く、その場合は凡例の並びを棒に合わせる | [G1] | 専門家の指針 |
| 凡例を使うと、図と凡例のあいだで視線が行き来する。直接ラベルは、要素が密集すると文字が重なりやすい | [G2] | 公的機関の実務ガイド |
| 線の端の系列名は、モバイル表示で崩れないかを確かめる。狭い画面では凡例に切り替える作図ツールもある | [G3] | 作図ツールのガイド |
| 注釈は対象の近くに、ほかの要素と重ならないように置き、画面の大きさを変えて確かめる。欠かせない情報は本文にも書く | [G4] | 統計局の実務ガイド |
| 色だけで情報を伝えない。文字と背景のコントラストは 4.5:1 以上（大きい文字は 3:1 以上）にする | [G5] | アクセシビリティの基準。読む速さの研究ではない |
| BPMN のメッセージフローのように、仕様で線の形と意味が決まっている記法がある | [G6] | 仕様 |

### まだ分かっていないこと

- 図のほかの条件をそろえ、凡例と直接ラベルだけを変えてグラフの読みやすさを比べた研究は、十分に見つかっていない。[R3] は直接ラベルを含む図を比べているが、コントラストなどほかの要素も同時に変えている。
- 直接ラベルにすれば認知負荷が下がる、とまでは言えない。文章と図を近くに置いたとき、測定した認知負荷が下がるという結果は一貫していない [R6]。
- 何系列までなら直接ラベルが向いているか、という目安は見つかっていない。
- 視線の往復は、少ないほどよいとは限らない。減らしたいのは、対応が分からずに図の中を探し回る視線の動きである。
- Tufte、Cleveland、Kosslyn の著書と、Nature Methods の Krzywinski（2013）"Labels and callouts" は、該当する箇所を確認できていないため、根拠に使っていない。

### 既存のサンプルとの関係

[samples/](../samples/README.md) の図の多くは、見出しの下に凡例を置いている。これらを描き直すまでは、サンプルの凡例の置き方をまねず、このプラクティスに従う。

### 出典

2026-09-29 に調べた。調査には ChatGPT Pro を使い、各出典の本文か抄録を確かめた。このうち [R1] と [R2] の数値、[R4] と [R5] の抄録、[G1]〜[G4] の該当箇所は、このリポジトリに載せる前に原典とも照合した。

- **[R1]** Huestegge, L., & Philipp, A. M. (2011). Effects of spatial compatibility on integration processes in graph comprehension. *Attention, Perception, & Psychophysics*, 73, 1903–1915. https://doi.org/10.3758/s13414-011-0155-1
- **[R2]** Riechelmann, E., & Huestegge, L. (2018). Spatial legend compatibility within versus between graphs in multiple graph comprehension. *Attention, Perception, & Psychophysics*, 80, 1011–1022. https://doi.org/10.3758/s13414-018-1484-0
- **[R3]** Renshaw, J. A., Finlay, J. E., Tyfa, D., & Ward, R. D. (2004). Understanding visual influence in graph design through temporal and spatial eye movement characteristics. *Interacting with Computers*, 16(3), 557–578. https://doi.org/10.1016/j.intcom.2004.03.001 （確認は抄録まで。比べた条件の詳細は [R1] の紹介による）
- **[R4]** Schroeder, N. L., & Cenkci, A. T. (2018). Spatial contiguity and spatial split-attention effects in multimedia learning environments: A meta-analysis. *Educational Psychology Review*, 30, 679–701. https://doi.org/10.1007/s10648-018-9435-9 （確認は抄録まで）
- **[R5]** Johnson, C. I., & Mayer, R. E. (2012). An eye movement analysis of the spatial contiguity effect in multimedia learning. *Journal of Experimental Psychology: Applied*, 18(2), 178–191. https://doi.org/10.1037/a0026923
- **[R6]** Schroeder, N. L., & Cenkci, A. T. (2020). Do measures of cognitive load explain the spatial split-attention principle in multimedia learning environments? A systematic review. *Journal of Educational Psychology*, 112(2), 254–270. https://doi.org/10.1037/edu0000372 （確認は抄録と冒頭まで）
- **[G1]** Few, S. (2005). *Effectively Communicating Numbers: Selecting the Best Means and Manner of Display*. https://www.perceptualedge.com/articles/Whitepapers/Communicating_Numbers.pdf （本文 17 ページ「If a Legend Is Required, Determine Where to Place It」）
- **[G2]** data.europa.eu. Direct labelling. *Data Visualisation Guide*. https://data.europa.eu/apps/data-visualisation-guide/direct-labelling
- **[G3]** Datawrapper Academy. What to consider when creating line charts. https://www.datawrapper.de/academy/what-to-consider-when-creating-line-charts ／ Customizing your line chart. https://www.datawrapper.de/academy/customizing-your-line-chart
- **[G4]** Office for National Statistics. Annotations. *Service Manual*. https://service-manual.ons.gov.uk/data-visualisation/guidance/annotations
- **[G5]** W3C. Understanding SC 1.4.1: Use of Color. https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html ／ Understanding SC 1.4.3: Contrast (Minimum). https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html ／ Complex Images. https://www.w3.org/WAI/tutorials/images/complex/
- **[G6]** Object Management Group. (2014). *Business Process Model and Notation (BPMN)*, Version 2.0.2, §9.4. https://www.omg.org/spec/BPMN/2.0.2/

## プラクティスを増やす

1. ルールと、その根拠を集める。根拠は、実証研究・ガイド・仕様に分け、どこまで言えるかと、まだ分からないことを書く。
2. ルールに従った図と従わない図を並べたサンプルを `.drawio.svg` で描き、`practices/<name>/` に置く。書き出しは [drawio-workflow.md](../references/drawio-workflow.md) に従う。
3. この README の一覧に行を足し、節を追加する。[drawio-style.md](../references/drawio-style.md) の決まりと食い違うときは、あわせて直す。
