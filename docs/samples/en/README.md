English | [简体中文](../zh-CN/README.md) | [日本語](../../../skills/explanatory-diagrams/samples/README.md)

# Samples

This page lists the 20 samples and what each one shows. They are English versions of the Japanese samples in the skill: the layout is the same, and only the text is translated. The screenshots embedded in the design-before-after sample are still in Japanese.

The skill itself ships only the Japanese samples and their [Japanese list](../../../skills/explanatory-diagrams/samples/README.md). The agent reaches that list from [SKILL.md](../../../skills/explanatory-diagrams/SKILL.md) and borrows ways of showing things from the samples. The samples are examples of what can be expressed, not templates to fill in. This page is not part of the skill.

## How the samples are grouped

The samples fall into three groups.

- **Ways to show a change**: styles such as before/after comparisons that you can combine with any kind of diagram.
- **Refactoring explanations**: ways to show a change, applied to common refactorings.
- **Diagram types**: one sample per notation or subject, such as architecture, sequence, and state machine diagrams. These do not show a before and after.

For example, to explain a change to an AWS setup, the agent draws in the notation of "AWS architecture diagram" and marks the change as in "Overlay the diff on one diagram".

The samples drawn with shapes share one made-up online store (orders, payments, and shipping). The design change and palette samples use the theme of a made-up admin screen for a household goods store, built with AntD for these samples. The screenshots were taken from that screen, whose source is in [`tests/skill-evals/explanatory-diagrams/sources/mock-admin-ui/`](../../../tests/skill-evals/explanatory-diagrams/sources/mock-admin-ui/). The "before" values in the palette are the ones AntD computed.

The subjects, names, figures, and business rules in the samples (such as the refund auto-approval limit and shipping fees) are all made up.

Every sample is a `.drawio.svg` file that you can open and edit in draw.io. The colors and the ways to draw lines and symbols are listed in [references/drawio-style.md](../../../skills/explanatory-diagrams/references/drawio-style.md) (in Japanese).

## Ways to show a change

### Compare side by side

Example: changes where the difference in structure is the point. Before and after share the same frame (here, the layer bands), so only what changed stands out. Add the change in count as well, such as "3 → 1".

![Side-by-side before/after diagram of a change from the UI calling external APIs directly to going through a service layer, titled "Move payment and restock into OrderService; the UI calls 1 part"](before-after-split.drawio.svg)

### Overlay the diff on one diagram

Example: changes that touch only part of the whole. On the "after" diagram, overlay what was added and what was removed. This sample outlines what was added in blue and marks what was removed with a gray dashed line and ✕.

![AWS architecture diagram with the diff overlaid, titled "Offload email to SQS and Lambda, responding without waiting"](before-after-diff.drawio.svg)

### Compare design changes on screenshots

Example: changes to how things look, such as color, spacing, or corner radius. Put the real screens from before and after side by side (stack wide components vertically), and outline the parts to look at. Number the outlines and match them to a table of the changed values. This sample draws the outlines in orange.

![Before/after screenshots side by side, titled "Match date range fill, focus ring & link color to store"](design-before-after.drawio.svg)

### Compare color palettes before and after

Example: changes that replace a theme's color steps (background, border, fill, text) all at once. Line up the steps in columns. For each color that changes, put the "before" row above the "after" row; show unchanged colors only once. Outline the problem steps and the changed values. This sample outlines problem steps in orange and changed values in blue.

![Before/after color palette titled "Define 10 primary steps to remove gray steps"](palette-before-after.drawio.svg)

### Compare amounts by size

Example: changes where the change in amount is the point, such as lines of code. Stack blocks whose height is proportional to the amount, and note the scale. Connect each block to where it goes, such as unchanged, moved, or taken over, with an arrow.

![Before/after blocks sized by line count, titled "The order edit page's hook goes from 160 lines to 70"](before-after-amount.drawio.svg)

## Refactoring explanations

### Move where state lives

Example: refactorings that move state out of a hook or module into another place. Show the state being moved and its new home, and note that the number of states stays the same. This sample shows the state being moved in orange and its new home in blue.

![Side-by-side before/after diagram titled "Extract 3 states from useOrderEditor into useDraft"](refactor-move-state.drawio.svg)

### Make names consistent

Example: refactorings that change only names. Split each name into its parts and line them up in a table, showing the name that breaks the naming rule and its new name. Also list what changes at the call sites.

![Rename diagram titled "Align useOrderEditSave with useOrderSave per naming rules"](refactor-rename.drawio.svg)

### Extract and export functions

Example: refactorings that move functions private to one file into their own module and export them. Draw current uses as solid lines, and uses that a later PR will add as dashed lines.

![Side-by-side before/after diagram titled "Extract order-table converters to orderTableConverters.ts"](refactor-extract-module.drawio.svg)

### Share state

Example: refactorings that merge the state each component kept on its own into one state, shared by the components that handle the same data. Show the change as the drop in the number of states (3 → 1), and keep the old positions as dashed outlines.

![Side-by-side before/after diagram titled "Combine per-table saving state into one shared state per order"](refactor-share-state.drawio.svg)

### Remove a value that was copied and passed along

Example: refactorings in multi-stage processing that remove a copied value passed from stage to stage, so that every step reads the original. Split the data, the steps that read it, and the results into bands, and overlay before and after in one diagram. This sample shows what was removed with orange dashed lines and strikethrough, and shows the value now read, and the values it affects, in blue.

![Before and after overlaid in one diagram, titled "Remove passed-around display_name and read name directly"](refactor-remove-duplicate.drawio.svg)

## Diagram types

### AWS architecture diagram

Example: explaining where services run and how they are made redundant. Use AWS icons and groups (Region, VPC, AZ, subnet), and number the steps of the request flow.

![AWS architecture diagram titled "Order API deployed across 2 AZs to accept orders even if one fails"](aws-architecture.drawio.svg)

### Sequence diagram

Example: explaining, in order, how several participants interact. Use distinct arrows for synchronous calls, asynchronous messages, and responses, along with activation bars and alt frames.

![Sequence diagram titled "Flow: order confirmation, external payment, Webhook notification"](sequence.drawio.svg)

### State machine diagram

Example: explaining states and the events, guards, and actions that move between them. Write transition labels as "event [guard] / action".

![State machine diagram titled "Order status: from awaiting payment to delivered, cancelled, or returned"](state-machine.drawio.svg)

### C4 container diagram

Example: explaining the apps, databases, and external services that make up a system, and how they connect. Label each relationship with what it does and "[technology]".

![C4 container diagram titled "Containers linking Web App, Admin, Order API & external systems"](c4-container.drawio.svg)

### ER diagram

Example: explaining tables, columns, and keys, and how rows in one table relate to rows in another. Explain the crow's foot symbols in a legend, and record design decisions as notes.

![Tables for orders, order items, payments, and more, titled "ER diagram: customers, addresses, orders, items, products, payments"](er-diagram.drawio.svg)

### Business flow (BPMN)

Example: explaining who does which task and where the flow branches. Put each role in its own lane, and use markers to tell human tasks from system tasks.

![Business flow titled "Flow: buyer return request, auto-approval, inspection, and refund"](business-flow.drawio.svg)

### Euler diagram (sets and elements)

Example: explaining which items a combination of conditions selects. Draw sets as circles and items as dots, and add a table showing the result for each item.

![Euler diagram titled "Email recipients: subscribed with valid address, minus opt-outs"](euler-sets.drawio.svg)

### Components and state

Example: explaining which part of a screen holds each piece of state, and which parts read and write it. Distinguish the kinds of state by border style (solid, dashed, dotted).

![Component tree and where state lives, titled "State ownership and read/write flow in order edit components & store"](state-ownership.drawio.svg)

### Code and runtime values

Example: explaining logic where the lines that run, or the value returned, depend on the input. Align each line of code with the values it evaluates to for each input.

![Code and the values evaluated for 3 inputs, titled "shippingFee condition checks and execution flow across 3 inputs"](code-trace.drawio.svg)

### Timeline and deadlines

Example: logic decided by what happens after how many minutes, such as deadlines, timeouts, and retry intervals. Put events as dots on a timeline with ticks, and show the deadline each event sets as an arrow. Write what each arrow means at its tip, and write the rules as text beside the timeline.

![Timeline where a cart hold's deadline is extended by each action and released when actions stop, titled "Release a cart hold 15 minutes after the last action"](timeline.drawio.svg)

## Adding a sample

The steps for adding a sample to the skill are in the [Japanese list](../../../skills/explanatory-diagrams/samples/README.md#サンプルの追加). When you add one, also add English and Simplified Chinese versions to `docs/samples/en/` and `docs/samples/zh-CN/` and to their lists, so that all three languages have the same samples.
