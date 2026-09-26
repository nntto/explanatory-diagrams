# draw.io のアセット資料

図形の仕様や連携方法は、公式資料を参照できる。

| 知りたいこと | 公式資料 |
|---|---|
| 図形を検索し、スタイルとサイズを取得する | [MCP の search_shapes](https://github.com/jgraph/drawio-mcp/blob/main/mcp-tool-server/README.md#search_shapes) |
| XML の図形・親子構造・接続線 | [AI 向け Style Reference](https://www.drawio.com/docs/reference/diagram-generation/style-reference/)、[共通 XML reference](https://github.com/jgraph/drawio-mcp/blob/main/shared/xml-reference.md) |
| ER テーブル | [テーブルの説明](https://www.drawio.com/docs/diagram-types/entity-relationship-tables/)、[パレット定義](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/diagramly/sidebar/Sidebar-ER.js) |
| 追加アイコンと画像の外部参照 | [追加アイコンの説明](https://www.drawio.com/docs/manual/shapes/extra-icon-sets/) |
| 既存図を画像として取り込む・切り出す | [画像の挿入](https://www.drawio.com/docs/manual/insert/add-images/)、[画像の切り出し](https://www.drawio.com/docs/manual/insert/image-crop/) |
| MCP・スキルとの連携 | [公式 MCP](https://www.drawio.com/docs/manual/generate/drawio-mcp-server/)、[公式スキル](https://github.com/jgraph/drawio-mcp/blob/main/plugins/codex/drawio/skills/drawio/SKILL.md) |

デスクトップ版の CLI で書き出すと、画像のパスで指定する Google Cloud の新しいアイコン（`img/lib/google_cloud/...`）は表示されない。Google Cloud は `mxgraph.gcp2` の図形を使う。

ローカルの見本には、[AWS 構成図](../templates/aws-architecture/aws-architecture.drawio.png)、[C4 コンテナ図](../templates/c4-container/c4-container.drawio.png)、[ER 図](../templates/er-diagram/er-diagram.drawio.png)、[業務フロー](../templates/business-flow/business-flow.drawio.png)がある。
