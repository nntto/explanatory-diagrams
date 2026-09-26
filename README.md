English | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

# explanatory-diagrams

An agent skill that lets Claude Code and Codex draw diagrams for pull request descriptions and design docs with draw.io. Give the agent a diff, notes, or screenshots, and it returns an SVG with the draw.io source embedded (`.drawio.svg`). The file works as an ordinary image in Markdown, and you can open it in draw.io to edit it later.

## Samples

**[Browse all 18 samples](docs/samples/en/README.md)**: before/after comparisons, refactoring explanations, and diagram types such as architecture, sequence, state machine, and ER diagrams, each with notes on when to use it. The agent picks the closest sample and follows its style.

**AWS architecture diagram.** An order API deployed across two Availability Zones (AZs), so it keeps taking orders if one of them fails. The steps of the request flow are numbered.

![AWS architecture diagram of an order API in two AZs. An ALB routes requests to both AZs, and RDS replicates synchronously to a standby](docs/samples/en/aws-architecture.drawio.svg)

**Design changes, compared on screenshots.** Screenshots from before and after a theme color change, side by side. The changed parts are outlined in orange, and each number points to a row in the table of changed values. The screenshots show a mock admin screen with a Japanese UI.

![Before/after screenshots and a table of values for a change that matches the date range fill, the input focus ring, and the link button text to the store's colors](docs/samples/en/design-before-after.drawio.svg)

The samples were finished by hand. To see what agents actually returned with this skill, see [Output by model](#output-by-model).

## Why draw.io

![Table comparing Mermaid, image generation, and draw.io](docs/why-drawio.en.drawio.svg)

## Install

Use only one of these methods for each agent.

### A. skills CLI (recommended)

```sh
npx skills@latest add nntto/explanatory-diagrams --skill explanatory-diagrams -g -a claude-code -a codex
```

To install it only in the current project, drop `-g`.

### B. Claude Code plugin

```sh
claude plugin marketplace add nntto/explanatory-diagrams
claude plugin install explanatory-diagrams@nntto
```

Requires Claude Code 2.1.142 or later.

### C. Manual

```sh
git clone https://github.com/nntto/explanatory-diagrams.git
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.claude/skills/explanatory-diagrams
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.agents/skills/explanatory-diagrams
```

## Requirements

- **draw.io desktop**, to export diagrams to SVG. The commands in the skill use the macOS path.
- **python3**, to embed screenshots in a diagram.
- **gh**, to add diagrams to pull requests.

If your agent runs in an OS sandbox, see [Using the skill in a sandbox](docs/sandbox.md).

## Usage

Describe what you want in plain words, and the agent loads the skill. For example:

- "Make a diagram of this PR's changes for the PR description. Compare against main."
- "Diagram the infrastructure change in infra.diff."
- "Use the before and after screenshots to make a diagram comparing the color changes."

To call the skill explicitly, type `/explanatory-diagrams` in Claude Code (`/explanatory-diagrams:explanatory-diagrams` if you installed it as a plugin) or `$explanatory-diagrams` in Codex.

The text in a diagram follows the language of the document it goes into.

## Output by model

The [output page](tests/skill-evals/explanatory-diagrams/README.md) shows what seven models (four from Claude and three from Codex) returned for the same request and materials.

## License

MIT ([LICENSE](LICENSE)). The AWS Architecture Icons in the samples and eval outputs are not covered; they are subject to [AWS's terms](https://aws.amazon.com/architecture/icons/).
