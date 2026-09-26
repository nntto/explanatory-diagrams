English | [简体中文](../zh-CN/README.md) | [日本語](../../../skills/explanatory-diagrams/templates/README.md)

# Sample list

This is the English version of the Japanese samples that come with the skill. Each sample has the same layout as the Japanese one; only the text is translated. The screenshots embedded in the design-before-after sample are still in Japanese.

The skill ships only the Japanese samples. When an agent draws a diagram for a document in another language, it translates the text of the sample. The Japanese list is [templates/README.md](../../../skills/explanatory-diagrams/templates/README.md). The agent opens it from [SKILL.md](../../../skills/explanatory-diagrams/SKILL.md) to find a close sample. This page is for reading in this repository and is not part of the skill.

This page lists the samples and when to use each one.

The subjects, names, figures, and business rules (such as the refund auto-approval amount and shipping fees) in the samples are all made up for the samples.

## How the samples are grouped

There are three kinds of samples.

- **Ways to show a change**: formats you can combine with any diagram, such as how to compare before and after.
- **Refactoring explanations**: ways to show a change, applied to common refactorings.
- **Diagram types**: samples for each notation or subject, such as architecture diagrams, sequence diagrams, and state machine diagrams. These are not before/after diagrams.

For example, to explain a change to an AWS architecture, draw it with the notation from "AWS architecture diagram" and show the change as in "Overlay the diff on one diagram".

The samples drawn with shapes all use the same made-up online shop (orders, payments, shipping). The design change and palette samples use the theme of a made-up general store's admin screen, built with AntD for the samples. The screenshots were taken of that screen, and its source is in [`tests/skill-evals/explanatory-diagrams/sources/mock-admin-ui/`](../../../tests/skill-evals/explanatory-diagrams/sources/mock-admin-ui/) in this repository (nntto/explanatory-diagrams). The "before" values in the palette are the values AntD computed.

All samples are `.drawio.svg` files. Open one in draw.io to edit it as is. What the colors and lines mean is in [references/drawio-style.md](../../../skills/explanatory-diagrams/references/drawio-style.md). The documents in references/ are in Japanese.

## Ways to show a change

### Compare side by side

When to use: changes where you want to show the difference in structure itself. Before and after share the same frame (in this example, the layer bands), so only what changed catches the eye. Also note the change in count, such as "3 → 1".

![Side-by-side before/after diagram of a change from the UI calling external APIs directly to going through a service layer, titled "Move payment and restock into OrderService; the UI calls 1 part"](before-after-split.drawio.svg)

### Overlay the diff on one diagram

When to use: changes where only part of the whole changes. On the after diagram, overlay what was added (blue frame) and what was removed (gray dashed line and ✕).

![AWS architecture diagram with the diff overlaid, titled "Offload email to SQS and Lambda, responding without waiting"](before-after-diff.drawio.svg)

### Compare design changes with screens side by side

When to use: changes to how things look, such as color, spacing, or corner radius. Put the real screens before and after side by side (stack wide parts top and bottom), and mark the parts to look at with orange frames. Number the frames and match them to a table of the changed values.

![Before/after screens side by side, titled "Match date range fill, focus ring & link color to store"](design-before-after.drawio.svg)

### Compare color palettes before and after

When to use: changes that replace a theme's color steps (background, border, fill, text) together. Line up the steps in columns, and for the colors that change, put the before row above the after row. Show colors that do not change only once. Mark problem steps with orange frames and changed values with blue frames.

![Before/after color palette titled "Define 10 primary steps to remove gray steps"](palette-before-after.drawio.svg)

## Refactoring explanations

### Move where state lives

When to use: refactorings that move state held by a hook or module to another place. Show the state to move in orange and where it moves in blue, and note that the number of states stays the same.

![Side-by-side before/after diagram titled "Extract 3 states from useOrderEditor into useDraft"](refactor-move-state.drawio.svg)

### Align names

When to use: refactorings that only change names. Split the names into parts and line them up in a table, showing the name that breaks the rule and the new name. Also list what changes at the call sites.

![Rename diagram titled "Align useOrderEditSave with useOrderSave per naming rules"](refactor-rename.drawio.svg)

### Extract and export functions

When to use: refactorings that extract functions that were private to one file and export them. Show current use with solid lines, and uses that a later PR will connect with dashed lines.

![Side-by-side before/after diagram titled "Extract order-table converters to orderTableConverters.ts"](refactor-extract-module.drawio.svg)

### Share state

When to use: refactorings that combine the state each component held into one state, shared by the components that handle the same data. Show the change as the difference in the number of states (3 → 1), and keep the old positions as dashed lines.

![Side-by-side before/after diagram titled "Combine per-table saving state into one shared state per order"](refactor-share-state.drawio.svg)

### Remove a value that was copied and passed along

When to use: refactorings in processing that spans several stages, where you remove a value that was copied and passed along so that every step reads the original value. Split data, the steps that read it, and results into bands, and overlay before and after in one diagram. Show what was removed with orange dashed lines and strikethrough, and the newly read value and the values it changes in blue.

![Before and after overlaid in one diagram, titled "Remove passed-around display_name and read name directly"](refactor-remove-duplicate.drawio.svg)

## Diagram types

### AWS architecture diagram

When to use: explaining where services are placed and how they are made redundant. Use AWS icons and groups (Region, VPC, AZ, subnet), and number the steps of the request flow.

![AWS architecture diagram titled "Order API deployed across 2 AZs to accept orders even if one fails"](aws-architecture.drawio.svg)

### Sequence diagram

When to use: explaining the interactions between several participants in order. Use different arrows for sync calls, async messages, and responses, and use activation bars and alt frames.

![Sequence diagram titled "Flow: order confirmation, external payment, Webhook notification"](sequence.drawio.svg)

### State machine diagram

When to use: explaining states and the events, guards, and actions that move between them. Write transition labels in the order "event [guard] / action".

![State machine diagram titled "Order status: from awaiting payment to delivered, cancelled, or returned"](state-machine.drawio.svg)

### C4 container diagram

When to use: explaining the apps, databases, and external services that make up a system, and how they relate. On each relationship line, write what it does and "[technology]".

![C4 container diagram titled "Containers linking Web App, Admin, Order API & external systems"](c4-container.drawio.svg)

### ER diagram

When to use: explaining tables, columns, and keys, and how many rows relate between tables. Show what the crow's foot symbols mean in a legend, and leave design decisions as notes.

![Tables for orders, order items, payments, and more, titled "ER diagram: customers, addresses, orders, items, products, payments"](er-diagram.drawio.svg)

### Business flow (BPMN)

When to use: explaining each role's tasks and branches. Split roles into lanes, and use markers to tell human tasks from system tasks.

![Business flow titled "Flow: buyer return request, auto-approval, inspection, and refund"](business-flow.drawio.svg)

### Euler diagram (sets and elements)

When to use: explaining which targets a combination of conditions picks. Draw sets as circles and elements as dots, and add a table of the result for each element.

![Euler diagram titled "Email recipients: subscribed with valid address, minus opt-outs"](euler-sets.drawio.svg)

### Components and state

When to use: explaining which part of a screen holds each piece of state, and who reads and writes it. Tell the kinds of state apart by border (solid, dashed, dotted).

![Component tree and where state lives, titled "State ownership and read/write flow in order edit components & store"](state-ownership.drawio.svg)

### Code and runtime values

When to use: explaining logic where the lines that run or the value returned depend on the input. Put each line of code at the same height as the values evaluated for each input.

![Code and the values evaluated for 3 inputs, titled "shippingFee condition checks and execution flow across 3 inputs"](code-trace.drawio.svg)

## Adding a sample

The steps for adding a sample to the skill are in the [Japanese list](../../../skills/explanatory-diagrams/templates/README.md#テンプレートの追加). When you add one, also add its English and Simplified Chinese versions to `docs/samples/en/` and `docs/samples/zh-CN/` and to these lists, so that all three languages have the same samples.
