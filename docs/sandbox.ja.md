[English](sandbox.md) | [简体中文](sandbox.zh-CN.md) | 日本語

# サンドボックスの中で使うときの設定

draw.io の書き出しは、OS のサンドボックスの中では異常終了します。エージェントをサンドボックスで動かしている場合は、draw.io のコマンドだけをサンドボックスの外で動かすように設定してください。以下のパスは macOS の draw.io のものです。

## Claude Code

設定ファイルの `sandbox.excludedCommands` に draw.io のコマンドを足します。

```json
{
  "sandbox": {
    "excludedCommands": ["/Applications/draw.io.app/Contents/MacOS/draw.io:*"]
  }
}
```

## Codex

`~/.codex/rules/` の下の `.rules` ファイル（たとえば `~/.codex/rules/drawio.rules`）に次のルールを足します。

```python
prefix_rule(pattern=["/Applications/draw.io.app/Contents/MacOS/draw.io", "-x"], decision="allow")
```

## 設定が適用される条件

どちらの設定も、draw.io のコマンドを単独で実行したときにだけ適用されます。`&&` や `;`、パイプでほかのコマンドとつなぐとサンドボックスの中で動き、書き出しが失敗します。
