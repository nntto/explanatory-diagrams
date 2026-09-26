# 状態の色を店の色に合わせる

## 背景

管理画面の成功・警告・エラーの色は、AntD の既定のままだった。店の主色（焦げ茶 `#5b4636`）と並ぶと鮮やかすぎて、タグやお知らせだけが浮いて見えていた。

## 変更

AntD の `ConfigProvider` の `theme.token` に、次の値を足した。部品のコードは変えていない。

| トークン | 変更前（AntD の既定） | 変更後 |
|---|---|---|
| `colorSuccess` | `#52c41a` | `#2f7d4f` |
| `colorSuccessBg` | `#f6ffed` | `#e9f2ec` |
| `colorSuccessBorder` | `#b7eb8f` | `#a9ccb5` |
| `colorWarning` | `#faad14` | `#b7791f` |
| `colorError` | `#ff4d4f` | `#b83a2e` |

- 警告とエラーの背景・枠線の色は、指定した色から AntD が計算する（警告の背景 `#f7f4e9`、エラーの背景 `#f7ece9` になる）。
- 成功だけは、背景と枠線も指定した。暗い緑を 1 色だけ渡すと、AntD が計算する背景が灰色がかった色（`#b1bdb4`）になったため。
- 情報（info）の青は変えていない。「出荷待ち」のタグは青のまま。

## 変わる画面

- 注文一覧：「支払い」「出荷」のタグと、表の上の警告・エラーのお知らせ
- お届け先の編集：保存完了のお知らせ、入力エラーと注意の表示

## 画面の画像

変更前後の同じ画面を、同じ幅・同じデータで撮った（VRT の基準画像と同じ撮り方）。

- `screenshots/before/orders.png`、`screenshots/after/orders.png`：注文一覧
- `screenshots/before/delivery-form.png`、`screenshots/after/delivery-form.png`：お届け先の編集
