English | [简体中文](sandbox.zh-CN.md) | [日本語](sandbox.ja.md)

# Using the skill in a sandbox

draw.io crashes when it exports inside an OS sandbox. If your agent runs in a sandbox, configure it so that only the draw.io command runs outside. The paths below are for draw.io on macOS.

## Claude Code

Add the draw.io command to `sandbox.excludedCommands` in your settings.

```json
{
  "sandbox": {
    "excludedCommands": ["/Applications/draw.io.app/Contents/MacOS/draw.io:*"]
  }
}
```

## Codex

Add this rule to a `.rules` file under `~/.codex/rules/` (for example, `~/.codex/rules/drawio.rules`).

```python
prefix_rule(pattern=["/Applications/draw.io.app/Contents/MacOS/draw.io", "-x"], decision="allow")
```

## When the settings apply

Both settings apply only when the draw.io command runs on its own. If it is chained with other commands using `&&`, `;`, or a pipe, it runs inside the sandbox and the export fails.
