[English](README.md) | 简体中文 | [日本語](README.ja.md)

# explanatory-diagrams

只需提供代码差异（diff）、设计笔记或界面截图，即可自动生成 draw.io 格式示意图的 skill。输出文件采用内嵌可编辑数据的 SVG 格式（`.drawio.svg`）。可以直接作为普通图片插入 Markdown 文档；若后续需要微调布局或修改文案，也可以直接用 draw.io 打开进行二次编辑，还可以交给 agent 修改。

## 为什么选择 draw.io？

为了兼顾表现范围、文字与结构的准确性，以及事后修改的便利。

![Mermaid、AI 生成图与 draw.io 的对比](docs/why-drawio.zh-CN.drawio.svg)

类似 Mermaid 的文本绘图工具虽然轻便，但只能自动排布固定种类的图，能画的构图受到限制；而图像生成 AI 虽然视觉效果好，细小的文字和线条却可能与指示不符，也很难只修改其中一部分。使用 draw.io，图形、图标和界面截图都可以放在任意位置，事后也能只修改其中一部分。代价是差异（diff）为 draw.io 的 XML，不易阅读，并且需要 draw.io 桌面版。

## 示例

Skill 会从 18 种模板中选出最接近的一种，按照其版式作图；没有合适的模板时，会用新的版式绘制。

- **[模板列表（共 18 种）](docs/samples/zh-CN/README.md)**：架构图、时序图、状态机图、ER 图、UI 变更对比图等。

### 架构图

跨两个可用区（AZ）的订单 API 高可用架构。为请求路径按顺序编号，并标出 RDS 向备用实例的同步复制。

![跨两个 AZ 的 AWS 架构图：ALB 进行流量分发，RDS 向备用实例同步复制数据](docs/samples/zh-CN/aws-architecture.drawio.svg)

### UI 变更对比

主题色更新前后的界面对比。用带编号的高亮框标出变更组件，并与下方的属性对照表关联，修改前后的颜色数值一目了然。

![对比日期范围填充、焦点框及链接按钮颜色的 UI 变更图](docs/samples/zh-CN/design-before-after.drawio.svg)

*注：以上示例为人工微调后的参考基准。各模型实际自动生成的原始结果，请参考 [模型生成评估](tests/skill-evals/explanatory-diagrams/README.md)。*

## 环境要求

需在本地安装以下工具：

- **draw.io 桌面版**：用于将图表导出为 SVG（默认使用 macOS 应用程序路径）。
- **Python 3**：用于将截图等位图嵌入到 SVG 载荷中。
- **GitHub CLI（`gh`）**：用于将生成的图表直接附加到 Pull Request。

在沙箱环境中运行时，请参考 [沙箱环境配置](docs/sandbox.zh-CN.md)。

## 安装方法

根据使用环境，选择以下任意一种方式即可：

### 1. skills CLI（推荐）

```sh
npx skills@latest add nntto/explanatory-diagrams --skill explanatory-diagrams -g -a claude-code -a codex
```

去掉 `-g` 参数则仅安装到当前项目。

### 2. Claude Code 插件

```sh
claude plugin marketplace add nntto/explanatory-diagrams
claude plugin install explanatory-diagrams@nntto
```

需 Claude Code 2.1.142 或更高版本。

### 3. 手动配置

克隆仓库并创建符号链接至对应目录：

```sh
git clone https://github.com/nntto/explanatory-diagrams.git
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.claude/skills/explanatory-diagrams
ln -s "$PWD/explanatory-diagrams/skills/explanatory-diagrams" ~/.agents/skills/explanatory-diagrams
```

## 使用方法

指定相关素材（diff、笔记、截图），使用自然语言发出作图需求：

- “根据与 main 分支的 diff，画一张说明这个 PR 改动的图。”
- “根据 infra.diff，画一张展示架构变更的图。”
- “根据修改前后的截图，做一张对比 UI 颜色变化的示意图。”

也可以显式调用 skill 命令：

- Claude Code：`/explanatory-diagrams`（作为插件安装时为 `/explanatory-diagrams:explanatory-diagrams`）
- Codex：`$explanatory-diagrams`

图表中的文字语言会跟随图表所在文档的语言。

## 模型生成评估

在 [评测目录](tests/skill-evals/explanatory-diagrams/README.md) 中汇总了 7 种模型（Claude 系列 4 种、Codex 系列 3 种）在相同输入和要求下的生成结果。

## 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。模板与评测样例中包含的 AWS 图标不适用本许可证，须遵守 [AWS 架构图标使用条款](https://aws.amazon.com/architecture/icons/)。
