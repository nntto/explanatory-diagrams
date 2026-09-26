English | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

# explanatory-diagrams

An agent skill that has your coding agent draw explanatory diagrams with draw.io for pull request descriptions and design docs. From your request and materials (such as diffs, notes, and screenshots), the agent draws a diagram and returns an SVG with the draw.io source embedded (`.drawio.svg`). You can paste it as a normal image, and open it in draw.io to edit it.

![Side-by-side before/after diagram: CheckoutPage stops calling the payment and inventory APIs directly and calls only OrderService, which now handles the charge and rolls back inventory if payment fails](docs/samples/en/before-after-split.drawio.svg)

A sample finished by hand. For diagrams that agents actually returned with this skill, see [Output by model](#output-by-model).

## Why draw.io

![Table comparing Mermaid, image generation, and draw.io on visual freedom, editing later, use in PRs or READMEs, reviewing changes, and what you need](docs/why-drawio.en.drawio.svg)

draw.io gives more layout freedom than Mermaid, and unlike image generation, you can fix the diagram later. The trade-offs: the diff is draw.io XML and hard to read, and you need the draw.io desktop app.

## What it covers

Good at:

- Before/after comparisons
- System architecture and AWS architecture diagrams
- Data models (ER diagrams)
- Where state lives
- Sequence diagrams
- State machine diagrams
- Business flows
- Sets and elements
- Code and runtime values
- Changes in UI design
- Color palettes

Out of scope: image generation and taking screenshots. The skill leaves these to other tools that handle them.

## Install

Works with Claude Code and Codex. Use one method per agent; do not install the same skill more than one way. These steps follow each tool's documentation and have not been tested end to end yet.

### A. skills CLI (main method)

```sh
npx skills@latest add nntto/explanatory-diagrams --skill explanatory-diagrams -g -a claude-code -a codex
```

`-g` installs it for your user: into `~/.agents/skills/` for Codex and `~/.claude/skills/` for Claude Code. To install it only in the current project, drop `-g`.

### B. Claude Code plugin marketplace

```sh
claude plugin marketplace add nntto/explanatory-diagrams
claude plugin install explanatory-diagrams@nntto
```

This plugin keeps `SKILL.md` at the plugin root. According to the Claude Code changelog, Claude Code 2.1.142 and later read this layout. Invoke it as `/explanatory-diagrams:explanatory-diagrams`.

### C. Manual

```sh
git clone https://github.com/nntto/explanatory-diagrams.git
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.claude/skills/explanatory-diagrams
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.agents/skills/explanatory-diagrams
```

## Requirements

- draw.io desktop. The commands in the skill use the macOS path (`/Applications/draw.io.app/Contents/MacOS/draw.io`). Tested on macOS 26.6 with draw.io 31.4.4. Not tried on other operating systems.
- `python3`, to embed screenshots in a diagram.
- `gh`, to put diagrams into pull requests. Whether `gh pr edit --attach` accepts SVG has not been confirmed.

### Sandbox

draw.io export crashes inside an OS sandbox. If you run your agent in a sandbox, configure it yourself so that only the draw.io command runs outside the sandbox.

- Claude Code: add the command to `sandbox.excludedCommands` in your settings.

  ```json
  {
    "sandbox": {
      "excludedCommands": ["/Applications/draw.io.app/Contents/MacOS/draw.io:*"]
    }
  }
  ```

- Codex: add this rule to a `.rules` file under `~/.codex/rules/` (for example, `~/.codex/rules/drawio.rules`).

  ```python
  prefix_rule(pattern=["/Applications/draw.io.app/Contents/MacOS/draw.io", "-x"], decision="allow")
  ```

In both cases, the draw.io command runs outside the sandbox only when it runs on its own. If it is chained with other commands (for example with `&&`, `;`, or a pipe), it runs inside the sandbox and the export fails.

## Usage

Ask in plain words. For example:

- "Make a diagram of this PR's changes for the PR description. Compare against main."
- "Diagram the infrastructure change based on infra.diff."
- "From the before and after screenshots, make a diagram that compares the color changes."

To invoke the skill explicitly, use `/explanatory-diagrams` in Claude Code (`/explanatory-diagrams:explanatory-diagrams` if you installed it as a plugin) or `$explanatory-diagrams` in Codex.

The text in the diagram is written in the language of the document it goes into. If you ask in English for a diagram in a Japanese PR, the diagram text is Japanese.

## Samples

The list, with when to use each sample, is in [docs/samples/en/README.md](docs/samples/en/README.md). There are 18 samples, grouped into three kinds: ways to show a change, refactoring explanations, and diagram types.

The samples come in English, Simplified Chinese, and Japanese versions, which differ only in the text. The screenshots embedded in design-before-after are Japanese in every version. The skill includes only the Japanese versions. The English and Chinese versions are in `docs/samples/` in this repository, for reading with this README. Diagram text follows the language of the target document (see [Usage](#usage)), so when the agent draws for a document in another language, it translates the sample text.

## Output by model

[This page](tests/skill-evals/explanatory-diagrams/README.md) shows what each model returned for the same request and materials.

On 2026-09-26, we ran each case once with four Claude models (Opus 5.5, Sonnet 5, Haiku 4.5, Fable 5.1) on Claude Code 2.1.282, and three Codex models (gpt-6-astra, gpt-6-sol, gpt-6-luna) on codex-cli 0.156.0. The runs used the skill as it was before the move to this repository. At that time it exported PNG (`.drawio.png`). Six models returned a `.drawio.png` with the source embedded in all three cases; Haiku 4.5 returned a PNG without the source in all three. We checked only whether each output followed the format, not how good the diagrams are. With one run each, we cannot tell whether the differences are a trend or chance. The page, including the models' replies, is in Japanese.

| Case | Change to explain | Materials given |
|---|---|---|
| [aws-infra-change](tests/skill-evals/explanatory-diagrams/README.md#aws-infra-change) | Move product images from EFS to S3 and serve them through CloudFront | Notes on the change, and the Terraform diff and full configuration after the change |
| [design-token-change](tests/skill-evals/explanatory-diagrams/README.md#design-token-change) | Match the status colors (success, warning, error) to the store's colors | Notes on the change, and four before/after screenshots |
| [refactor-dependency-inversion](tests/skill-evals/explanatory-diagrams/README.md#refactor-dependency-inversion) | Invert the dependency so the shipping logic no longer calls the SDK directly | A git repository (main and a working branch), and notes on the change |

## License

MIT ([LICENSE](LICENSE)).

- The AWS Architecture Icons (in the aws-architecture and before-after-diff samples and some eval outputs) are not covered by this license. They follow [AWS's terms](https://aws.amazon.com/architecture/icons/).
- The subject of the samples and evals (an online shop for general goods and its admin screens), names, addresses, phone numbers, order numbers, figures, and business rules (such as the refund auto-approval amount and shipping fees) are all made up for the samples and evals.
- The skill's steps for quoting others' material ([references/drawio-workflow.md](skills/explanatory-diagrams/references/drawio-workflow.md#既存図の再利用)) follow the approach to quotation under Japanese copyright law.

## Contact

Please open an Issue for questions and bug reports.
