[English](sandbox.md) | 简体中文 | [日本語](sandbox.ja.md)

# 在沙箱中使用时的设置

draw.io 在操作系统的沙箱中导出时会崩溃。如果 agent 在沙箱中运行，请设置为只让 draw.io 的命令在沙箱外运行。下面的路径是 macOS 上 draw.io 的路径。

## Claude Code

在设置文件的 `sandbox.excludedCommands` 中加入 draw.io 的命令。

```json
{
  "sandbox": {
    "excludedCommands": ["/Applications/draw.io.app/Contents/MacOS/draw.io:*"]
  }
}
```

## Codex

在 `~/.codex/rules/` 下的 `.rules` 文件（例如 `~/.codex/rules/drawio.rules`）中加入下面的规则。

```python
prefix_rule(pattern=["/Applications/draw.io.app/Contents/MacOS/draw.io", "-x"], decision="allow")
```

## 设置生效的条件

这两种设置都只在单独运行 draw.io 命令时生效。如果用 `&&`、`;` 或管道和其他命令连在一起，命令会在沙箱内运行，导出会失败。
