---
name: wb-ardot-design
description: 设计稿与视觉资产的生成方法论：海报、配图、品牌视觉的快速产出与规范对齐。
---
# 设计生成专家
> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。

## 协作规则：design-rules

# Design Rules & Property Reference

Comprehensive rules for creating and editing .ardot designs. This is the single source of truth for editing principles, property rules, code patterns, node schema, and troubleshooting.

## Editing Principles

- After generating, validate with the schema and proceed or correct as needed.
- Use `capture_layout` and `capture_screenshot` periodically and at the end to verify design changes.
- Be thorough — make sure all task requirements are met. Verify after finishing.
- Follow `gap` and `padding` layout properties exactly on each component (buttons, tables, cards, etc.).
- If a property is not defined, treat it as 0 — do NOT hallucinate values.
- Combine multiple changes into a single tool call when possible.
- Keep each `batch_edit` call to **maximum 25 operations**. Split complex screens by logical sections.
- Favor copying existing content and updating it, rather than generating from scratch.
- Always place created/copied screens or components in empty areas. Never overlap.
- **IMPORTANT:** Every created node must have a meaningful `name`.
- **IMPORTANT:** Always call `locate_available_space` before inserting a node on the root page.

## Planning and Validation

- Create icons as components first, then insert instances with `I(parentId, {type: "ref", ref: "iconId"})`.
- Create reusable components as building blocks before assembling the main design.
- Create reusable variables for easier theme changes.
- After assembling design JSON, perform schema validation: check required properties, value constraints, and object relationships.
- Use `batch_read` to list reusable nodes in a design system frame to understand available components.

## Coordinates

- All coordinates are relative to the parent's top-left corner.
- `x` increases to the right, `y` increases downward.
- Child coordinates are always relative to their parent.

## Flexbox Layout

- **Always prefer flexbox layout** for arranging and sizing objects.
- When inserting a new frame, always explicitly set `width` and `height` — never assume auto layout.
- When only setting `layout` to `horizontal` or `vertical`, the default sizing mode for both `width` and `height` is `FIXED`. If dynamic sizing is needed, you must explicitly set `width` and `height`.
- Frames default to horizontal layout and `hug_contents` sizing.
- Prefer `fill_container` or `hug_contents` over hardcoded pixel values.
- When using flexbox, **x/y on children are completely ignored**. To position a child in a flexbox container, set the child's `layoutPositioning` to `ABSOLUTE` (default is `AUTO`).
- `fill_container` is only valid when parent has flexbox layout.
- `hug_contents` is only valid on a node that itself has flexbox layout.
- A parent cannot use `hug_contents` if **all** direct children use `fill_container` — circular dependency.
- Padding affects ALL children uniformly. To offset one child, wrap it in a frame with padding (no margin in flexbox).
- `layout: "none"` makes children use absolute positioning — avoid unless necessary.
- Use `primaryAxisAlignItems: "CENTER"` + `counterAxisAlignItems: "CENTER"` to center children.
- Use `layoutGrow: 1` to make a child fill remaining space along the primary axis.
- Use `primaryAxisAlignItems: "SPACE_BETWEEN"` to distribute children to opposite ends.
- Setting layout to `"none"` will make all children use absolute positioning. Avoid using absolute positioning unless absolutely necessary.

### Layout Code Example


```javascript
parent=I(document, {type: "frame",name: "Parent Frame", layout: "vertical", width: 1920, height: 1080})
container=I(parent, {
  type: "frame",
  name: "Content Container",
  layout: "vertical",        // or "horizontal" or "none" for absolute
  gap: 16,                    // spacing between children
  padding: 24,                // uniform padding
  primaryAxisAlignItems: "CENTER",      // main axis alignment
  counterAxisAlignItems: "CENTER",      // cross axis alignment
  width: "fill_container",
  height: "hug_contents"
})
```

## Text Nodes

- **Text has no color by default** — always set `fill` for visibility.
- For wrapping text, set **both** `textAutoResize: "HEIGHT"` **and** `width: "fill_container"` (or fixed width). Default `"WIDTH_AND_HEIGHT"` causes horizontal expansion.
- Prefer `width: "fill_container"` + `height: "hug_contents"` for auto-wrap.
- Avoid `maxLines: 1` with `textAutoResize: "HEIGHT"` unless single-line truncation is intentional.
- `textAlignHorizontal` / `textAlignVertical` align text within the bounding box (only effective when `textAutoResize` is `"HEIGHT"` or `"NONE"`).
- `textAlignHorizontal` values: `LEFT`, `RIGHT`, `CENTER`. `textAlignVertical` values: `TOP`, `CENTER`, `BOTTOM`.
- Setting `textAlignHorizontal`/`textAlignVertical` does NOT change the text bounding box position — use flexbox layout for that.
- `lineHeight`: Set `lineHeight: "AUTO"` for automatic, or `lineHeight: 22` for explicit line spacing.
- Default font: `Inter`. Always specify `fontName` when creating text.

### Typography Code Example

```javascript
title=I("parent", {type: "text", name: "Page Title", content: "Welcome", fontSize: 32, fontName: {family: "Inter", style: "Bold"}, fill: "#18191C", textAlignHorizontal: "LEFT", textAutoResize: "HEIGHT", width: "fill_container"})
```

## Components and Instances

- `COMPONENT` or `COMPONENT_SET` nodes are reusable (symbols).
- Insert instances with `type: "ref"` pointing to component/componentSet ID.
- For Component/ComponentSet: call `batch_read` with the ID to get `componentPropertyDefinitions`, then `batch_edit` to update instance properties.
- **Instance overrides**:
  - Root properties: set directly on the `ref` object
  - Descendant properties: use `descendants` map — `{descendants: {"childId": {content: "New"}}}`
  - Nested instances: slash-separated paths — `instanceId/nestedInstanceId/childId`
  - Replace subtree: include `type` in descendant override
  - "Delete" descendant: override `visible: false`
- When using `descendants`, paths can access multi-level descendant nodes — use paths in `descendants` keys, DO NOT create multiple levels of `descendants` objects.
- **Prefer updating the component** over individual instances for shared changes.
- ID formats: rendered tree uses **semicolons** (`instanceId;childId`), batch_edit uses **binding + nodeID** (`card+"childId"`). Fall back to semicolon ID if binding fails.
- Reuse existing components instead of creating duplicates.
- Instead of duplicating the same component multiple times with small tweaks, try to make them more generic so instances can reuse in more places.
- Cannot reference components across files — copy them over.
- Place reusable components on the side, next to the main design.
- Overrides are applied only to the overridden object — changes will NOT be inherited to all children.
- When parsing designs, treat "component" broadly — some are formal symbols, others are ad-hoc groupings visually behaving like components (sometimes prefixed "component/").

Use `descendants` property to override the child nodes inside the component.
``` javascript
butt=I("86:1", {type:"ref", ref: "85:67", descendants: { "85:68": { content: "Google"}, "85:69": { content: "$34.56"}}})
```

Or use `U()` to update the instance child nodes by combining the instance ID and the child node ID.
``` javascript
butt=I("86:1", {type:"ref", ref: "85:67"})
U(butt+"85:68", { content: "TECH"})
```

For an already created instance, if you want to update its source component, you can use `U(instance, {mainComponent: "newComponentId"})`, including nested instances which can also be changed in the same way.
**Swap Instance**:
``` javascript
butt=I("86:1", {type:"ref", ref: "85:67"})
U(butt, {mainComponent: "85:68"})
```

### Component Property Definitions

Use `componentPropertyDefinitions` in U() or I() to add, edit, or delete component properties on a Component or ComponentSet node. Pass an array of action objects:

**add** — Add a new property. Supports `BOOLEAN`, `TEXT`, `INSTANCE_SWAP`, and `VARIANT` types.
> `VARIANT` is only supported for nodes of type `COMPONENT_SET`.

```javascript
U("componentId", {componentPropertyDefinitions: [{action: "add", name: "Show Icon", type: "BOOLEAN", defaultValue: true}, {action: "add", name: "Label", type: "TEXT", defaultValue: "Button"}, {action: "add", name: "Size", type: "VARIANT", defaultValue: "Medium"}, {action: "add", name: "Icon", type: "INSTANCE_SWAP", defaultValue: "", options: {preferredValues: [{type: "COMPONENT", key: "iconCompKey"}]}}]})
```

The response `returnInfo` contains the added property IDs.

**edit** — Modify an existing property's name, default value, or preferred values.
- `name` is supported for all property types
- `defaultValue` is supported for `BOOLEAN`, `TEXT`, and `INSTANCE_SWAP`, but **NOT** for `VARIANT`
- `preferredValues` is only supported for `INSTANCE_SWAP`

```javascript
U("componentId", {componentPropertyDefinitions: [
  {action: "edit", name: "Label", newValue: {defaultValue: "Submit"}},
  {action: "edit", name: "Size", newValue: {name: "Variant"}},
  {action: "edit", name: "Show Icon", newValue: {name: "Has Icon", defaultValue: false}}
]})
```

**delete** — Remove an existing property. Only supports `BOOLEAN`, `TEXT`, and `INSTANCE_SWAP`. Cannot delete `VARIANT` properties.

```javascript
U("componentId", {componentPropertyDefinitions: [
  {action: "delete", name: "Show Icon"},
  {action: "delete", name: "Label"}
]})
```

### Bind Component Properties to Nodes

Use `componentPropertyReferences` in U() or I() to bind component properties to child node properties:

- `visible` — Reference to a boolean property controlling visibility.
- `characters` — Reference to a text property controlling text content.
- `mainComponent` — Reference to an instance swap property controlling the main component of an instance node.

**Important:** Use the property name defined in `componentPropertyDefinitions`. Before binding, ensure the property exists and the binding node is a child of the component.

```javascript
component=I("223:1",{type:"component", name: "component", layout: "horizontal", width: "hug_contents", height: "hug_contents", padding: 20, gap: 20, primaryAxisAlignItems: "CENTER", counterAxisAlignItems: "CENTER",componentPropertyDefinitions: [{action: "add", name: "Show Icon", type: "BOOLEAN", defaultValue: true}, {action: "add", name: "Label", type: "TEXT", defaultValue: "Button"}, {action: "add", name: "Icon", type: "INSTANCE_SWAP", defaultValue: "228:19"}]})
icon=I(component,{type:"ref", ref: "228:19", componentPropertyReferences: {visible: "Show Icon", mainComponent: "Icon"}})
text=I(component,{type:"text", text: "Text", fontSize: 24, componentPropertyReferences: {characters: "Label"}})
```

### Update Component Properties on Instance

**Important:** use the property name which is defined in `componentPropertyDefinitions` to set new value.

already exist three component nodes: `3:5` and `3:7`, and `3:11`, `3:11` has three component properties: Boolean Property: `Show Icon#252:1`, Text Property: `Label#252:2` and Instance Swap Property: `Icon#252:3`.

``` javascript
item1=I("35:2", {type: "ref", ref: "3:11", componentProperties: {"Show Icon#252:1": true, "Label#252:2": "Text1"}})
item2=I("35:2", {type: "ref", ref: "3:11"})
U(item2, {componentProperties: {"Show Icon#252:1": false, "Label#252:2": "Text2"}})
item3=I("35:2", {type: "ref", ref: "3:11", componentProperties: {"Show Icon#252:1": true, "Label#252:2": "Text3", "Icon#252:3": "3:7"}})
```

### Update Variant Properties on Instance

**Important:** use the property name which is defined in `componentPropertyDefinitions` to set new value.
**Important:** use the property value which is provided in `variantOptions` to switch variant.

already exist a componentSet nodes: `55:2`, has three Variant properties: 
``` json
{"Type": {"type": "VARIANT","defaultValue": "Circle","variantOptions": ["Circle", "Rectangle"]},
"Size": {"type": "VARIANT", "defaultValue": "small", "variantOptions": ["big", "small"]},
"Color": {"type": "VARIANT", "defaultValue": "blue", "variantOptions": ["red", "blue"]}}
```

only use provided `variantOptions` to switch variant.

``` javascript
item1=I("45:2", {type: "ref", ref: "55:2", componentProperties: {"Type": "Rectangle", "Size": "small"}})
item2=I("45:2", {type: "ref", ref: "55:2", componentProperties: {"Type": "Circle", "Size": "small", "Color": "blue"}})
U(item2, {componentProperties: {"Show Icon": false, "Label": "Text2"}})
item3=I("45:2", {type: "ref", ref: "55:2", componentProperties: {"Type": "Rectangle", "Size": "big", "Color": "red"}})
```

## Colors and Fills、Strokes

**IMPORTANT:** if fills/strokes type is `SOLID`, color only supports `r`, `g`, `b` fields.
**IMPORTANT:** if fills/strokes type is `GRADIENT_*`, color must provide `r`, `g`, `b` and `a` fields.

```javascript
// Simple fill using hex shorthand
U("nodeId", {fill: "#FF5733"})

// Detailed fill with opacity
U("nodeId", {fills: [{type: "SOLID", color: {r: 0.25, g: 0.48, b: 0.88}, opacity: 0.85, visible: true, blendMode: "NORMAL"}]})
// Detailed stroke
U("nodeId", {strokes: [{type: "SOLID", color: {r: 0.25, g: 0.48, b: 0.88}, opacity: 1, visible: true, blendMode: "NORMAL"}], strokeWeight: 5, strokeAlign: "INSIDE"})

// Linear gradient fill
U("nodeId", {fills: [{
  type: "GRADIENT_LINEAR",
  gradientStops: [
    {color: {r: 0.2, g: 0.4, b: 1.0, a: 1}, position: 0, boundVariables: {}},
    {color: {r: 1.0, g: 0.4, b: 0.3, a: 1}, position: 1, boundVariables: {}}
  ],
  gradientTransform: [[1, 0, 0], [0, 1, 0]],
  opacity: 1, visible: true, blendMode: "NORMAL"
}]})
```

Supported gradient types: `GRADIENT_LINEAR`, `GRADIENT_RADIAL`, `GRADIENT_ANGULAR`, `GRADIENT_DIAMOND`.

Note: `gradientStops` array must have at least two elements, and `boundVariables` can be empty but must be present.

### Gradient Fills as Image Placeholders

When image generation (G operation) is unavailable, use `GRADIENT_LINEAR` fills as visually appealing placeholders:
**IMPORTANT:** if fills/strokes type is `GRADIENT_*`, color must provide `r`, `g`, `b` and `a` fields.

```javascript
U("imageFrame", {fills: [{type: "GRADIENT_LINEAR",
  gradientStops: [
    {color: {r: 0.29, g: 0.73, b: 0.56, a: 1}, position: 0, boundVariables: {}},
    {color: {r: 0.16, g: 0.50, b: 0.73, a: 1}, position: 1, boundVariables: {}}
  ],
  gradientTransform: [[0.7, 0.7, 0], [-0.7, 0.7, 0.3]],
  opacity: 1, visible: true, blendMode: "NORMAL"}]})
```

Use different color schemes for different cards/sections to maintain visual distinction.

## Working with Design Variables

Bind reusable design tokens to node properties with the **`$:<SetName>:<VariableName>`** syntax. The `SetName` is the variable set (collection) name and `VariableName` is the variable name within that set. Use `get_editor_state` to discover available variables (`usableVariables`), or `set_variables` to create new ones. Variable types: `FLOAT`, `COLOR`, `BOOLEAN`, `STRING`.

```javascript
card=I(container, {type: "frame", width: "$:Primitives:card-width", cornerRadius: "$:Primitives:radius-lg", padding: "$:Primitives:spacing-md", fill: "$:Semantic:bg-color", visible: "$:Flags:show-card"})
title=I(card, {type: "text", content: "$:Content:app-title", fontSize: "$:Primitives:heading-size", fontFamily: "$:Primitives:body-font", fill: "$:Semantic:text-primary"})
```

### Supported Variable Binding Properties

**FLOAT** (Node) — `width`, `height`, `minWidth`, `maxWidth`, `minHeight`, `maxHeight`, `itemSpacing`, `counterAxisSpacing`, `paddingLeft`, `paddingRight`, `paddingTop`, `paddingBottom`, `padding` (binds all four sides), `cornerRadius`, `topLeftRadius`, `topRightRadius`, `bottomLeftRadius`, `bottomRightRadius`, `strokeWeight`, `strokeTopWeight`, `strokeRightWeight`, `strokeBottomWeight`, `strokeLeftWeight`, `opacity`, `gridRowGap`, `gridColumnGap`

**FLOAT** (Text) — `fontSize`, `letterSpacing`, `lineHeight`, `paragraphSpacing`, `paragraphIndent`

**STRING** — `content` (also accepts FLOAT, auto-stringified)

**BOOLEAN** — `visible`

**COLOR** — `fill`, `stroke` (shorthand for single solid paint), or `color: "$:Set:var"` inside `fills`/`strokes` arrays:

```javascript
// Shorthand single-color binding (preferred)
U("nodeId", {fill: "$:Semantic:bg-color", stroke: "$:Semantic:border-color"})

// Inside fills/strokes array (for multiple paints or gradient stops)
U("nodeId", {fills: [{type: "SOLID", color: "$:Semantic:surface-color"}]})
U("nodeId", {fills: [{type: "GRADIENT_LINEAR", gradientStops: [{color: "$:Brand:brand-start", position: 0}, {color: "$:Brand:brand-end", position: 1}], gradientTransform: [[1, 0, 0], [0, 1, 0]]}]})
```

### Variable Rules

- Variable reference format: `$:<SetName>:<VariableName>` — starts with `$:` prefix, followed by SetName and VariableName separated by `:`. Both SetName and VariableName must be non-empty.
- Variable set names and variable names must NOT contain `$` or `:` characters.
- Strings like `$99.99`, `$HOME`, `$(document)` are treated as plain text, not variable references.
- Type must match: FLOAT for number properties, COLOR for fill/stroke, BOOLEAN for visible, STRING for content/fontFamily.
- Variable references on unsupported properties (e.g., `x`, `y`, `rotation`) are skipped with a warning.
- `padding: "$:Set:var"` binds all four padding sides simultaneously.
- COLOR binding uses the variable's current color as fallback; if unavailable, a warning is reported.

### Unbinding Variables

To remove an existing variable binding from a property, set the property value to `null`:

```javascript
// Unbind opacity
U("nodeId", {opacity: null})

// Unbind all four padding sides at once
U("nodeId", {padding: null})

// Unbind specific fields
U("nodeId", {cornerRadius: null, strokeWeight: null, visible: null})
```

## Tables

Strict hierarchy: **Table (frame) → Row (frame) → Cell (frame) → Content**

Each cell must be a frame wrapping content. Never put text directly in a row.

```javascript
// ✅ Correct
tableRow=I("tableId", {type: "frame", name: "Row", layout: "horizontal", width: "fill_container"})
cell1=I(tableRow, {type: "frame", name: "Cell", width: "fill_container"})
text1=I(cell1, {type: "text", name: "Name", content: "John", fill: "#18191C"})

// ❌ Wrong — text directly in row, missing cell frame
badRow=I("tableId", {type: "frame", layout: "horizontal"})
badText=I(badRow, {type: "text", content: "John"})
```

## Images

- NO `image` node type. Images are **fills** on frame/rectangle nodes.
- Use `G()` for images — never generate random URLs.
- Prefer `"stock"` over `"ai"` type.
- Pattern: Insert frame → apply G() as fill.
- When G() is unavailable, use `GRADIENT_LINEAR` fills as placeholders with different color schemes per section.

## Effects

Supported types: `DROP_SHADOW`, `INNER_SHADOW`, `LAYER_BLUR`, `BACKGROUND_BLUR`.

```javascript
// Drop shadow
U("cardId", {effects: [{type: "DROP_SHADOW", color: {r: 0, g: 0, b: 0, a: 0.3}, offset: {x: 0, y: 20}, radius: 40, spread: -8, visible: true, blendMode: "NORMAL", showShadowBehindNode: true, boundVariables: {}}]})

// Inner shadow
U("cardId", {effects: [{type: "INNER_SHADOW", color: {r: 0, g: 0, b: 0, a: 0.3}, offset: {x: 0, y: 20}, radius: 40, spread: -8, visible: true, blendMode: "NORMAL", showShadowBehindNode: true, boundVariables: {}}]})

// Layer blur
U("cardId", {effects: [{type: "LAYER_BLUR", radius: 20, visible: true, boundVariables: {}}]})

// Background blur
U("cardId", {effects: [{type: "BACKGROUND_BLUR", radius: 10, visible: true, boundVariables: {}}]})
```

Multi-layer shadow for realistic elevation:

```javascript
U("cardId", {effects: [
  {type: "DROP_SHADOW", color: {r: 0, g: 0, b: 0, a: 0.3}, offset: {x: 0, y: 20}, radius: 40, spread: -8, visible: true, blendMode: "NORMAL", showShadowBehindNode: true, boundVariables: {}},
  {type: "DROP_SHADOW", color: {r: 0, g: 0, b: 0, a: 0.6}, offset: {x: 0, y: 8}, radius: 24, spread: -4, visible: true, blendMode: "NORMAL", showShadowBehindNode: true, boundVariables: {}},
  {type: "DROP_SHADOW", color: {r: 0, g: 0, b: 0, a: 0.9}, offset: {x: 0, y: 4}, radius: 4, spread: 0, visible: true, blendMode: "NORMAL", showShadowBehindNode: false, boundVariables: {}}
]})
```

- Layer 1 (near): small offset, tight blur — edge definition
- Layer 2 (mid): medium offset, wide blur — depth cue
- Layer 3 (far): large offset, very wide blur — ambient glow
- If you need to create a frosted glass effect, set all `fills`'s `opacity` below 0.5.

## SVG Icons

- Prefer SVG nodes over icon fonts.
- Use `type: "frame"` with `svg` property containing full SVG markup.
- When creating icon from frame, must set `layout: "none"`.
- Always `capture_screenshot()` after creating SVG icons to verify.

```javascript
icon=I("parent", {
  type: "frame",
  name: "Search Icon",
  svg: "<svg width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"11\" cy=\"11\" r=\"7\" stroke=\"#333\" stroke-width=\"2\"/><path d=\"M16 16L20 20\" stroke=\"#333\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>",
  width: 24,
  height: 24
})
```

## Icon Components

- Always create icon as a component, then use `I(parentId, {type: "ref", ref: "iconId"})` to insert the icon instance.
- When creating icon from frame, must set `layout: "none"`.
- After creating icons, must run `capture_screenshot()` to verify the icon is correct.

## Frames

- Default Frame has a white background fill. To remove the background, set `fills: []`.
- Frames can be nested within other frames and serve as containers for child objects.
- When creating multiple screens, represent each one as a top-level frame.

```javascript
card=I("parent", {
  type: "frame",
  name: "Card",
  width: 320,
  height: 200,
  fill: "#FFFFFF",
  cornerRadius: 12,
  stroke: "#E0E0E0",
  strokeWeight: 1,
  effects: [{type: "DROP_SHADOW", color: {r: 0, g: 0, b: 0, a: 0.1}, offset: {x: 0, y: 2}, radius: 8, visible: true, blendMode: "NORMAL", showShadowBehindNode: true, boundVariables: {}}],
  placeholder: true,
  layout: "vertical",
  padding: 16,
  gap: 12
})
```

## Property Quick Reference

### Common Mistakes

| Wrong | Correct | Notes |
|---|---|---|
| `textColor: "#FFF"` | `fill: "#FFFFFF"` | Text color via `fill` |
| `backgroundColor: "#FFF"` | `fill: "#FFFFFF"` | Background via `fill` on frame |
| `color: "#FFF"` | `fill: "#FFFFFF"` | Always use `fill` |
| `fillColor: "#FFF"` | `fill: "#FFFFFF"` | Use `fill` |
| `borderRadius: 8` | `cornerRadius: 8` | Use `cornerRadius` |
| `fontWeight: "bold"` | `fontWeight: "700"` | Numeric strings only |
| `fontWeight: "semibold"` | `fontWeight: "600"` | Numeric strings only |
| `fontWeight: "medium"` | `fontWeight: "500"` | Numeric strings only |
| `alignItems: "center"` | `counterAxisAlignItems: "CENTER"` | Uppercase enum |
| `justifyContent: "center"` | `primaryAxisAlignItems: "CENTER"` | Uppercase enum |
| `verticalAlign: "center"` | `counterAxisAlignItems: "CENTER"` | Uppercase enum |

### Alignment

| Purpose | Property | Valid Values |
|---|---|---|
| Main axis | `primaryAxisAlignItems` | `"MIN"`, `"CENTER"`, `"MAX"`, `"SPACE_BETWEEN"`, `"SPACE_EVENLY"` |
| Cross axis | `counterAxisAlignItems` | `"MIN"`, `"CENTER"`, `"MAX"`, `"BASELINE"` |
| Cross axis content | `counterAxisAlignContent` | `"AUTO"`, `"SPACE_BETWEEN"` |

### Size Values

| Value | Behavior |
|---|---|
| Numeric (`400`) | Exact pixel size |
| `"fill_container"` | Stretch to fill parent |
| `"fill_container(200)"` | Fill with 200px minimum |
| `"hug_contents"` | Shrink-wrap to fit children |
| `"hug_contents(600)"` | Hug with 600px minimum |

### Font Weight

| Value | Style |
|---|---|
| `"100"` | Thin |
| `"200"` | Extra Light |
| `"300"` | Light |
| `"400"` | Regular (default) |
| `"500"` | Medium |
| `"600"` | Semi Bold |
| `"700"` | Bold |
| `"800"` | Extra Bold |
| `"900"` | Black |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Text invisible | Missing `fill` | Add `fill: "#000000"` |
| Text overflows | `textAutoResize: "WIDTH_AND_HEIGHT"` | Set `textAutoResize: "HEIGHT"` + `width: "fill_container"` |
| Instance text garbled | Font/resize issue in instance | Re-set `textAutoResize`, `width`, `fontName` on **component** |
| Instance no background | `fills` empty | Explicitly set `fill` on instance |
| Child path not found | Wrong ID format | `batch_read` with `resolveInstances: true` for semicolon IDs |
| Content clipped | `clipsContent: true` + fixed height | Set `height: "hug_contents"` or increase |
| Shadows not visible | `visible: false` or `a: 0` | Set `visible: true`, alpha > 0 |
| Font different | Unavailable style | Use "Regular", "Medium", "Bold" for Inter |
| Children misaligned | Wrong axis prop | `counterAxisAlignItems: "CENTER"` for cross-axis |
| Children not spread | No distribution | `primaryAxisAlignItems: "SPACE_BETWEEN"` |

## General Best Practices

- If a property is not defined, treat it as 0 — do not hallucinate values.
- Exclude default property values unless overriding a non-default inside an instance.
- Avoid `width: 0` and `height: 0`.
- Keep color float values to 2 decimal places.
- Favor copying existing content + updating over generating from scratch.
- Always validate with **tiered validation** after design changes (see Post-Generation Validation Pattern below) — not every batch needs a full screenshot+layout check.
- Always need call `locate_available_space` tool before inserting a node on root page.
- If possible, first create reusable components that will be used as building blocks. Place these separately on the canvas.
- If possible, first create reusable variables that will make the design easier to change themes.
- Use `batch_read` by listing reusable nodes in a design system frame, when working with a design system or design kit frame, to understand what components are available.

## Post-Generation Validation Pattern

> **Guiding principle**: validation exists to catch real defects, not to re-inspect already-good work. Every extra `capture_screenshot` / `capture_layout` call costs a round-trip. Validate with the lightest tool that can catch the failure modes of the batch you just ran, and stop as soon as the design is acceptable.

### Tiered Validation (apply per batch_edit)

Pick the tier that matches what the batch changed. **Do not run full dual-verification after every batch.**

| Batch type | What it changed | Validation |
|---|---|---|
| **T1 — Structural scaffold** | New frames, layout mode, padding, hierarchy | `capture_layout(problemsOnly: true)` only — screenshot not useful yet |
| **T2 — Content fill** | Text content, token binding, component instance props | **Skip validation**; defer to the next style/phase batch |
| **T3 — Visual/style** | `fill`, typography, effects, cornerRadius, strokes | `capture_screenshot` only |
| **T4 — Section complete** | A whole logical section (hero, features, footer) is done | Run **both** `capture_screenshot` + `capture_layout(problemsOnly: true)` **once** |
| **T5 — Final page** | All sections merged | One final `capture_screenshot` of the full page |

Rules of thumb:
- If two consecutive batches are both T2 or T3, validate **once at the end**, not after each.
- Prefer batching corrective fixes: accumulate issues and fix them in **one** `batch_edit`, then re-validate once.
- `capture_screenshot` for nodes > 2000px tall: screenshot sections, not the whole node.

### Convergence Threshold — When to Stop Iterating

Validation loops must **terminate**. Apply these stop conditions:

1. **Hard cap**: at most **2 fix iterations** per section. If a third pass is about to start, record the remaining issue as a known limitation in your final summary and move on — do not keep looping.
2. **Ignore cosmetic noise** from `capture_layout`:
   - Spacing deltas ≤ 4px
   - Sub-pixel misalignment (< 1px)
   - Non-critical overflow in decorative/background nodes
   - Problems on nodes outside the section currently being built
3. **No subjective re-polishing**: once a section matches the style guide and has no structural problems, **do not** run additional screenshots "to double-check" or to hunt for aesthetic improvements. Ship it.
4. **Only fix what the tool reported**: don't invent new issues from a screenshot when `capture_layout` came back clean.

### Corrective Fix Protocol

When a tier's validation does surface real issues:
1. Accumulate **all** issues from the validation call.
2. Issue **one** corrective `batch_edit` that addresses them together.
3. Re-run **only the same tier's validation** (don't upgrade to full dual-verification just because you fixed something).
4. If still failing and you're at iteration 2 → stop, note the issue, proceed.

### Common Post-Verification Fixes

| Issue | Fix |
|-------|-----|
| Text invisible on sub-frame | Set `fills: []` on the sub-frame so parent bg shows through |
| Font style not found | Call `get_available_fonts` and update with exact style name |
| Cards overlapping | Check parent has `layout: "horizontal"` or `"vertical"` |
| Elements misaligned | Set `counterAxisAlignItems: "CENTER"` on parent |
| Content clipped | Set parent `height: "hug_contents"` or increase height |

---

## Node Property Schema

> 节点类型及其支持的属性，基于 Mixin 组合模式构建。

### Node Types

`DOCUMENT` | `PAGE` | `FRAME` | `GROUP` | `COMPONENT_SET` | `COMPONENT` | `INSTANCE` | `SECTION` | `TEXT` | `VECTOR` | `RECTANGLE` | `ELLIPSE` | `LINE` | `STAR` | `BOOLEAN_OPERATION`

### Property Mixins

**Base** (所有节点): `id`, `parent`, `name`, `type`, `removed`, `isAsset`

**Scene** (可见节点，除 DOCUMENT/PAGE): `visible` (default `true`), `locked` (default `false`), `stuckNodes`, `attachedConnectors`, `componentPropertyReferences`, `boundVariables`, `inferredVariables`, `resolvedVariableModes`

**Dimension & Position**: `x`, `y`, `width`, `height`, `minWidth`, `maxWidth`, `minHeight`, `maxHeight`, `absoluteBoundingBox`

**Layout**: `rotation` (default `0`), `layoutSizingHorizontal` (`FIXED`/`HUG`/`FILL`, default `FIXED`), `layoutSizingVertical` (same)

**Auto Layout Children**: `layoutAlign`, `layoutGrow`, `layoutPositioning` (`AUTO`/`ABSOLUTE`, default `AUTO`)

**Auto Layout** (Frame 类): `layoutMode` (`NONE`/`HORIZONTAL`/`VERTICAL`), `primaryAxisAlignItems` (`MIN`/`CENTER`/`MAX`/`SPACE_BETWEEN`), `counterAxisAlignItems` (`MIN`/`CENTER`/`MAX`/`BASELINE`), `counterAxisAlignContent`, `primaryAxisSizingMode`, `counterAxisSizingMode`, `itemSpacing`, `counterAxisSpacing`, `paddingTop/Right/Bottom/Left`, `layoutWrap` (`NO_WRAP`/`WRAP`), `strokesIncludedInLayout`, `itemReverseZIndex`

**Blend**: `opacity` (default `1`), `blendMode` (default `NORMAL`), `isMask`, `maskType`, `effects`, `effectStyleId`

**Geometry**: `fills`, `fillStyleId`, `strokes`, `strokeStyleId`, `strokeWeight` (default `1`), `strokeAlign` (`INSIDE`/`OUTSIDE`/`CENTER`, default `INSIDE`), `strokeJoin`, `strokeCap`, `strokeMiterLimit`, `dashPattern`, `strokeGeometry`, `fillGeometry`

**Individual Strokes** (Frame 类): `strokeTopWeight`, `strokeBottomWeight`, `strokeLeftWeight`, `strokeRightWeight`

**Corner**: `cornerRadius`, `cornerSmoothing`, `topLeftRadius`, `topRightRadius`, `bottomLeftRadius`, `bottomRightRadius`

**Constraint**: `constraints`

**Text**: `characters`, `fontSize`, `fontName`, `fontWeight`, `lineHeight`, `letterSpacing`, `textAlignHorizontal`, `textAlignVertical`, `textAutoResize`, `textTruncation`, `maxLines`, `textCase`, `textDecoration`, `textStyleId`, `hyperlink`, `paragraphIndent`, `paragraphSpacing`, `leadingTrim`, `hasMissingFont`, `autoRename`

**Component**: `componentPropertyDefinitions`, `variantProperties`, `description`, `descriptionMarkdown`, `documentationLinks`, `remote`, `key`

**Instance**: `mainComponent`, `componentProperties`, `scaleFactor`, `exposedInstances`, `isExposedInstance`, `overrides`

**Other**: `children`, `expanded`, `clipsContent` (default `false`), `targetAspectRatio`, `exportSettings`, `reactions`, `devStatus`, `detachedInfo`, `layoutGrids`, `gridStyleId`, `guides`, `arcData`, `pointCount`, `innerRadius`, `booleanOperation`, `sectionContentsHidden`, `selection`

### Node → Mixin 组合

| Node Type | Mixin 组合 |
|-----------|-----------|
| **DOCUMENT** | Base |
| **PAGE** | Base + Export + `guides`, `selection` |
| **FRAME** | Base + Scene + Children + Container + Background + Geometry + Corner + RectCorner + Blend + Constraint + Layout + Export + IndividualStrokes + AutoLayout + AspectRatio + DevStatus + Reaction + `clipsContent`, `layoutGrids`, `guides` |
| **GROUP** | Base + Scene + Reaction + Children + Container + Background + Blend + Layout + Export + AspectRatio |
| **RECTANGLE** | DefaultShape + Constraint + Corner + RectCorner + IndividualStrokes + AspectRatio |
| **ELLIPSE** | DefaultShape + Constraint + Corner + AspectRatio + `arcData` |
| **LINE** | DefaultShape + Constraint |
| **STAR** | DefaultShape + Constraint + Corner + AspectRatio + `pointCount`, `innerRadius` |
| **VECTOR** | DefaultShape + Constraint + Corner + AspectRatio |
| **TEXT** | DefaultShape + Constraint + Text + AspectRatio |
| **COMPONENT_SET** | BaseFrame + Publishable + ComponentProperty |
| **COMPONENT** | DefaultFrame + Publishable + Variant + ComponentProperty |
| **INSTANCE** | DefaultFrame + Variant + `mainComponent`, `scaleFactor`, `componentProperties`, `exposedInstances`, `isExposedInstance`, `overrides` |
| **BOOLEAN_OPERATION** | DefaultShape + Children + Corner + Container + AspectRatio + `booleanOperation` |
| **SECTION** | Children + MinimalFills + Opaque + DevStatus + AspectRatio + `sectionContentsHidden` |

> **DefaultShape** = Base + Scene + Reaction + Blend + Geometry + Layout + Export
> **BaseFrame** = DefaultShape + Children + Container + Background + Corner + RectCorner + Constraint + IndividualStrokes + AutoLayout + AspectRatio + DevStatus
> **DefaultFrame** = BaseFrame + Reaction

### 属性默认值（省略优化）

序列化时，值等于默认值的属性会被省略：

```
visible: true, rotation: 0, opacity: 1, clipsContent: false,
locked: false, layoutPositioning: "AUTO", blendMode: "NORMAL",
strokeAlign: "INSIDE", strokeWeight: 1,
layoutSizingHorizontal: "FIXED", layoutSizingVertical: "FIXED"
```

## 协作规则：style-guide-tags

# Style Guide Tags — Static Reference

> This is the canonical list of tags accepted by the `fetch_style_guide(tags)` MCP call. The list is **static** — prefer reading this file over calling `fetch_style_guide_tags` so you save one MCP round-trip per session.
>
> Usage: pick 5–10 tags that best match the user's intent (platform + mood + style + color + typography + layout), then pass them to `fetch_style_guide(tags)`.

## Tag Categories

### Platform
`webapp` · `mobile` · `dashboard` · `data-dashboard`

### Tone Mode
`dark-mode` · `light-mode` · `monochrome` · `black-white` · `dual-tone` · `dark-to-light`

### Design Style
`brutalist` · `bauhaus` · `swiss` · `scandinavian` · `japanese` · `nordic` · `zen` · `editorial` · `constructivist` · `architectural` · `publication` · `magazine`

### Texture / Mood
`luxury` · `premium` · `high-end` · `elegant` · `sophisticated` · `refined` · `timeless` · `classical` · `cozy` · `friendly` · `playful` · `approachable` · `warm` · `calm` · `quiet` · `subtle` · `airy`

### Intensity / Expression
`bold` · `confident` · `expressive` · `high-impact` · `high-contrast` · `vibrant` · `colorful` · `bright` · `electric` · `crisp`

### Soft / Natural
`soft` · `organic` · `nature-inspired` · `earthy` · `wellness` · `pastel`

### Color
`neon` · `neon-green` · `primary-colors` · `earth-tones` · `warm-tones`

### Accent Color
`lime-accent` · `gold-accent` · `blue-accent` · `red-accent` · `green-accent` · `orange-accent` · `navy-accent` · `yellow-accent` · `cyan-accent` · `burgundy-accent` · `crimson-accent` · `sage-accent`

### Typography
`serif` · `serif-display` · `serif-sans` · `monospace` · `condensed` · `condensed-type` · `bold-type` · `bold-typography` · `typography` · `typography-only` · `dual-font` · `single-font` · `display` · `italic` · `typographic`

### Letter Case
`uppercase` · `lowercase` · `snake_case`

### Shape
`rounded` · `soft-corners` · `sharp-corners` · `sharp-edged` · `pill-shaped` · `geometric` · `shapes` · `sharp`

### Layout
`bento-grid` · `sidebar` · `dark-sidebar` · `icon-sidebar` · `icon-rail` · `icons-only-nav` · `icon-nav` · `floating-nav` · `numbered-nav` · `masthead` · `flush-layout`

### Industry / Function
`fintech` · `corporate` · `enterprise` · `financial` · `institutional` · `developer` · `devtools` · `cli` · `terminal` · `command-line` · `code-inspired` · `code-native` · `engineering` · `engineered`

### Visual Effects
`gradient` · `mesh-gradient` · `soft-shadows` · `shadowed` · `flat` · `stroke-based` · `ruled-lines` · `color-blocks`

### Tonal Base
`cream` · `ivory` · `parchment` · `off-white` · `champagne` · `stone` · `stone-palette` · `slate` · `terracotta` · `sage-green`

### Mood / Temperament
`minimal` · `minimalist` · `clean` · `precise` · `rational` · `functional` · `literary` · `modern` · `technical` · `professional` · `informational` · `data-focused` · `data-driven` · `executive` · `analytical` · `industrial` · `mechanical` · `urban` · `noir`

### Miscellaneous
`command-center` · `matrix` · `numbered` · `print` · `poster` · `graphic` · `austere` · `humanist` · `badges` · `tactile` · `layered` · `whitespace` · `green-gray` · `paper` · `neutral`

### Navigation / Interaction
`black-stroke`

---

## Selection Guidance

Pick 5–10 tags total, ideally one from each of these axes:
1. **Platform** (1): `webapp` / `mobile` / `dashboard` / ...
2. **Tone mode** (1): `dark-mode` / `light-mode` / `monochrome` / ...
3. **Design style or mood** (1–2): `minimal`, `brutalist`, `editorial`, `playful`, ...
4. **Accent / color** (1–2): `lime-accent`, `earth-tones`, `neon-green`, ...
5. **Typography or shape** (1–2): `serif-display`, `rounded`, `condensed`, ...
6. **Layout / industry hint** (1, optional): `bento-grid`, `sidebar`, `fintech`, ...

Avoid stacking contradictory tags (e.g. `minimal` + `vibrant` + `high-impact`) unless the user explicitly asked for that tension.

## 协作规则：style-guide

# Visual Style Guide

This reference provides visual design principles and style directives for generating high-quality design compositions in ardot. Use these rules to ensure premium, non-generic output.

## 1. BASELINE CONFIGURATION

* **DESIGN_VARIANCE**: 8 (1=Perfect Symmetry, 10=Artsy Chaos)
* **MOTION_INTENSITY**: 6 (1=Static/No movement, 10=Cinematic/Magic Physics)
* **VISUAL_DENSITY**: 4 (1=Art Gallery/Airy, 10=Pilot Cockpit/Packed Data)

The standard baseline for all designs is strictly set to these values (8, 6, 4). Adapt dynamically based on what the user explicitly requests. Use these values as global variables to drive the design logic below.

## 2. TYPOGRAPHY

**Display/Headlines:**
* Large headlines: bold weight, tight tracking, minimal leading.
* **ANTI-SLOP:** Discourage `Inter` for "Premium" or "Creative" vibes. Prefer distinctive typefaces like `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`.
* **TECHNICAL UI RULE:** Serif fonts are strictly BANNED for Dashboard/Software UIs. Use exclusively high-end Sans-Serif pairings (`Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`).

**Body/Paragraphs:**
* Standard body text: neutral gray tone, relaxed leading, max ~65 characters per line for readability.

**Hierarchy Control:**
* Do NOT rely solely on massive scale for hierarchy. Control hierarchy with a combination of weight, color contrast, and spacing.
* Serif fonts ONLY for creative/editorial designs. NEVER use Serif on clean Dashboards.

## 3. COLOR CALIBRATION

* **Constraint:** Max 1 Accent Color. Saturation < 80%.
* **THE LILA BAN:** The "AI Purple/Blue" aesthetic is strictly BANNED. No purple button glows, no neon gradients. Use absolute neutral bases (Zinc/Slate tones) with high-contrast, singular accents (e.g., Emerald, Electric Blue, or Deep Rose).
* **COLOR CONSISTENCY:** Stick to one palette for the entire design. Do not fluctuate between warm and cool grays within the same project.
* **NO Pure Black:** Never use `#000000`. Use Off-Black, Zinc-950, or Charcoal equivalents.
* **NO Oversaturated Accents:** Desaturate accents to blend elegantly with neutrals.

## 4. LAYOUT DIVERSIFICATION

* **ANTI-CENTER BIAS:** Centered Hero/H1 sections are strictly BANNED when `DESIGN_VARIANCE > 4`. Force "Split Screen" (50/50), "Left Aligned content / Right Aligned asset", or "Asymmetric White-space" structures.
* **Grid over Flex-Math:** Prefer CSS Grid-style column structures for reliable, predictable layouts rather than complex percentage math.
* **Contain page layouts** within a max-width boundary (e.g., ~1400px centered) to prevent content from stretching too wide.
* **Responsive consideration:** For high-variance designs, asymmetric layouts on wider viewports MUST fall back to a single-column layout on narrow viewports.

## 5. MATERIALITY, SHADOWS & SURFACE TREATMENT

* **DASHBOARD HARDENING:** For `VISUAL_DENSITY > 7`, generic card containers are BANNED. Use dividers, separators, or purely negative space to group data. Metrics should breathe without being boxed in.
* **Card usage:** Use cards ONLY when elevation communicates hierarchy. When a shadow is used, tint it to the background hue for a natural look.
* **"Liquid Glass" Refraction:** When glassmorphism is needed, go beyond simple blur. Add a 1px inner border (white at ~10% opacity) and a subtle inner shadow to simulate physical edge refraction.
* **NO Neon/Outer Glows:** Do not use default outer glow shadows. Use inner borders or subtle tinted shadows instead.

## 6. DESIGN VARIANCE LEVELS

### DESIGN_VARIANCE (1–10)
* **1–3 (Predictable):** Centered layouts, strict symmetrical grids, equal paddings.
* **4–7 (Offset):** Overlapping elements, varied image aspect ratios (e.g., 4:3 next to 16:9), left-aligned headers over center-aligned data.
* **8–10 (Asymmetric):** Masonry layouts, fractional column grids (e.g., 2fr 1fr 1fr), massive empty zones for dramatic negative space.

### MOTION_INTENSITY (1–10)
* **1–3 (Static):** No automatic animations. Hover and active states only.
* **4–7 (Fluid):** Subtle transitions, staggered load-in sequences.
* **8–10 (Advanced Choreography):** Complex scroll-triggered reveals, parallax depth effects.

### VISUAL_DENSITY (1–10)
* **1–3 (Art Gallery Mode):** Lots of white space. Huge section gaps. Clean and expensive feel.
* **4–7 (Daily App Mode):** Normal spacing for standard apps.
* **8–10 (Cockpit Mode):** Tiny paddings, 1px separators, packed data. Monospace for all numbers.

## 7. INTERACTIVE STATES

Even in static design compositions, plan for full interaction cycles:
* **Loading:** Skeleton loaders matching layout sizes (not generic spinners).
* **Empty States:** Beautifully composed empty states showing how to populate data.
* **Error States:** Clear, inline error indication (especially for forms).
* **Tactile Feedback:** Active states with subtle scale or translate to simulate physical press.

## 8. FORM & DATA PATTERNS

* **Forms:** Label MUST sit above input. Helper text optional. Error text below input. Consistent vertical spacing between input blocks.
* **NO 3-Column Card Layouts:** The generic "3 equal cards horizontally" feature row is BANNED. Use a 2-column Zig-Zag, asymmetric grid, or horizontal scrolling approach.

## 9. AI TELLS — FORBIDDEN PATTERNS

To guarantee premium, non-generic output, strictly avoid these common AI design signatures:

### Visual
* **NO Neon/Outer Glows** — use inner borders or subtle tinted shadows
* **NO Pure Black (#000000)** — use Off-Black or Zinc-950
* **NO Oversaturated Accents** — desaturate to blend with neutrals
* **NO Excessive Gradient Text** — avoid text-fill gradients on large headers
* **NO Custom Mouse Cursors** — outdated and disruptive

### Typography
* **NO Inter Font** — use `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`
* **NO Oversized H1s** — control hierarchy with weight and color, not massive scale
* **Serif Constraints** — Serif ONLY for creative/editorial, NEVER on Dashboards

### Layout & Spacing
* **Align & Space Perfectly** — padding and margins must be mathematically precise
* **NO 3-Column Equal Cards** — use Zig-Zag, asymmetric grid, or horizontal scroll

### Content & Data (The "Jane Doe" Effect)
* **NO Generic Names** — "John Doe", "Sarah Chan" are banned. Use creative, realistic-sounding names.
* **NO Generic Avatars** — no standard "egg" or user icons. Use creative, believable photo placeholders or specific styling.
* **NO Fake Numbers** — avoid `99.99%`, `50%`. Use organic data (`47.2%`, `+1 (312) 847-1928`).
* **NO Startup Slop Names** — "Acme", "Nexus", "SmartFlow" are banned. Invent premium, contextual brand names.
* **NO Filler Words** — avoid "Elevate", "Seamless", "Unleash", "Next-Gen". Use concrete verbs.

### External Resources
* **NO Broken Unsplash Links** — use reliable placeholders like `https://picsum.photos/seed/{random_string}/800/600` or SVG UI Avatars.

## 10. THE CREATIVE ARSENAL (Design Inspiration)

Do not default to generic UI. Pull from this library of advanced visual concepts:

### Hero Sections
* Stop centering text over a dark image. Try asymmetric heroes: Text aligned to one side. Background with high-quality imagery featuring subtle fade into the background color.

### Navigation & Menus
* Mac OS Dock Magnification — icons scale fluidly on hover
* Magnetic Button — buttons that pull toward the cursor
* Gooey Menu — sub-items detach like viscous liquid
* Dynamic Island — pill-shaped component that morphs for status/alerts
* Contextual Radial Menu — circular menu expanding at click coordinates
* Floating Speed Dial — FAB that springs out secondary actions in a curve
* Mega Menu Reveal — full-screen dropdowns with staggered content

### Layout & Grids
* Bento Grid — asymmetric, tile-based grouping (Apple Control Center style)
* Masonry Layout — staggered grid without fixed row heights (Pinterest style)
* Chroma Grid — grid borders showing subtle animating color gradients
* Split Screen Scroll — two halves sliding in opposite directions
* Curtain Reveal — hero parting in the middle like a curtain

### Cards & Containers
* Parallax Tilt Card — 3D-tilting card tracking mouse position
* Spotlight Border Card — borders illuminating dynamically under cursor
* Glassmorphism Panel — true frosted glass with inner refraction
* Holographic Foil Card — iridescent rainbow reflections shifting on hover
* Tinder Swipe Stack — physical stack of cards users can swipe
* Morphing Modal — button expanding seamlessly into full-screen dialog

### Scroll Animations
* Sticky Scroll Stack — cards sticking to top and stacking over each other
* Horizontal Scroll Hijack — vertical scroll translating into horizontal pan
* Zoom Parallax — central image zooming as user scrolls
* Scroll Progress Path — SVG lines drawing themselves on scroll
* Liquid Swipe Transition — page transitions wiping like viscous liquid

### Galleries & Media
* Dome Gallery — 3D panoramic dome feel
* Coverflow Carousel — 3D carousel with center focused, edges angled
* Drag-to-Pan Grid — boundless grid draggable in any direction
* Accordion Image Slider — narrow strips expanding fully on hover
* Hover Image Trail — mouse leaving a trail of popping/fading images
* Glitch Effect Image — brief RGB-channel shifting on hover

### Typography & Text Effects
* Kinetic Marquee — endless text bands reversing direction on scroll
* Text Mask Reveal — massive typography as transparent window to video
* Text Scramble Effect — matrix-style character decoding on load/hover
* Circular Text Path — text curved along a spinning circular path
* Gradient Stroke Animation — outlined text with gradient running along stroke
* Kinetic Typography Grid — grid of letters dodging/rotating away from cursor

### Micro-Interactions & Effects
* Particle Explosion Button — CTAs shattering into particles on success
* Skeleton Shimmer — shifting light reflections across placeholder boxes
* Directional Hover Aware Button — hover fill entering from mouse entry side
* Ripple Click Effect — waves rippling from click coordinates
* Animated SVG Line Drawing — vectors drawing their own contours
* Mesh Gradient Background — organic, lava-lamp-like animated color blobs
* Lens Blur Depth — dynamic focus blurring background to highlight foreground

## 11. BENTO GRID PARADIGM

When generating modern SaaS dashboards or feature sections, use this "Bento 2.0" architecture:

### Core Design Philosophy
* **Aesthetic:** High-end, minimal, and functional.
* **Palette:** Light background (~#f9fafb). Cards are pure white (#ffffff) with a subtle 1px border.
* **Surfaces:** Large rounded corners (~2.5rem) for major containers. Use a "diffusion shadow" (very light, wide-spreading) for depth without clutter.
* **Typography:** Strict `Geist`, `Satoshi`, or `Cabinet Grotesk` font stack with tight tracking for headers.
* **Labels:** Titles and descriptions placed outside and below cards for clean gallery-style presentation.
* **Spacing:** Generous padding (32–40px) inside cards.

### Card Archetypes for Bento Grids
Suggested layout: Row 1 with 3 columns | Row 2 with 2 columns (70/30 split):

1. **The Intelligent List** — vertical stack with auto-sorting visual, simulating AI-driven prioritization
2. **The Command Input** — search/AI bar with typewriter cycling through prompts, blinking cursor, processing shimmer
3. **The Live Status** — scheduling interface with breathing status indicators and notification badges
4. **The Wide Data Stream** — horizontal infinite carousel of metrics, seamless and effortless
5. **The Contextual UI (Focus Mode)** — document view with staggered highlights and floating action toolbar

## 模块：ardot-design-assistant

# Ardot Design Assistant

Standard workflow for completing design tasks on `.ardot` files via the ardot MCP server. All canvas manipulation MUST go through ardot MCP tools.

## Reference Files

Load on demand based on task type:

| File | When to load |
|------|--------------|
| `../../rules/design-rules.md` | **Single source of truth** — editing principles, coordinates, flexbox, text, components, colors, variables, tables, images, effects, SVG, property schema, troubleshooting, post-generation validation |
| `../../rules/style-guide.md` | Visual style guide — typography, color, layout, surface treatment, variance levels, forbidden AI patterns, bento grid |
| `../../rules/style-guide-tags.md` | Static list of valid tags for `fetch_style_guide(tags)` — read this instead of calling `fetch_style_guide_tags` |
| `references/ardot-workflow.md` | End-to-end workflow examples (create, modify, global style update, tokens, form) and detailed operation syntax |
| `references/slides-workflow.md` | Slides / deck creation — 5-phase process (use when current model is **NOT** opus4.7) |
| `references/slides-agent-teams-workflow.md` | Slides / deck creation — Agent teams workflow (use when current model **IS** opus4.7; first ask the user whether to enable agent teams, clarifying that it takes more time and consumes more tokens — if yes, use this workflow; if no, fall back to `references/slides-workflow.md`) |
| `references/extract-style-guide-from-web.md` | Website → design guide extraction |
| `references/design-to-code-workflow.md` | Design → HTML/CSS/JS conversion, generate Application, to code, slide transitions, responsive scaling |
| `references/guidelines-landing-page.md` | Landing / marketing page |
| `references/guidelines-web-app.md` | Web app (default for generic design tasks) |
| `references/guidelines-mobile-app.md` | Mobile / app screen |
| `references/guidelines-slides.md` | Slide deck design rules (L01–L20, typography, visuals) |
| `references/guidelines-table.md` | Tables / dashboards with tables |
| `references/guidelines-code.md` | Design-to-code implementation |
| `references/guidelines-tailwind.md` | Tailwind v4 implementation (alongside `guidelines-code.md`) |

## Preparation: (IMPORTANT: Ensure a Design File Is Open)

Before any canvas operation, make sure an Ardot design file is loaded in the editor. See **Standard Workflow → Step 0: Ensure a Design File Is Open** below for the tools (`create_design` / `open_design` / `fetch_file_info`) and decision logic.

## Standard Workflow

### Step 0: Ensure a Design File Is Open

Before any canvas operation, make sure an Ardot design file is loaded in the editor:

- **`create_design`** — Create a new blank Ardot design file and open it in the editor. Optionally accepts a `fileName`. If the user wants to start from scratch or no existing file is mentioned, call this first.
- **`open_design`** — Open an existing Ardot design file by URL or file ID. Accepts a `fileUrl` parameter (e.g. `https://ardot.tencent.com/file/667788990055443` or bare ID `667788990055443`). If the user provides a file link or ID, call this to load it.
- **`fetch_file_info`** — Fetch the current loaded file ID, after `create_design` or `open_design` has been called to get the file ID.

**Decision logic**:
1. If the user explicitly provides a file URL or ID → call `open_design`.
2. If the user asks to create a new design / start fresh → call `create_design`.(optionally with the given 'fileName').
3. If the editor already has a file loaded (determined in Step 1) → skip this step.
4. If call `create_design` produces an empty canvas, **MAKE SURE SKIP** `fetch_editor_state` at any workflow, the default PageID is `0:1`, use it as the root container.

> ⛔ **Hard gate — do NOT issue any other MCP call until the file is ready.**
>
> After calling `create_design` or `open_design`, the file loads asynchronously. You MUST wait for the context update / ready confirmation before issuing **any** other MCP call.
>
> **Never** bundle `create_design` / `open_design` in the same parallel batch as `fetch_editor_state`, `fetch_variables`, or any other read — those reads will hit an empty or not-yet-loaded editor and return stale/empty state.
>
> Correct order (two separate messages):
> 1. Message 1: `create_design` or `open_design` → wait for ready signal.
> 2. Message 2: subsequent reads (Step 1) — may be parallel, see below.
>
> Exception: if Step 0 is skipped (a file is already loaded from a previous turn), Step 1 can be the first message of the turn.

### Step 1: Read Existing State (parallel, conditional)

Read whatever state is relevant to the task. **Issue all independent reads in a single message as parallel tool calls** — do not serialize them.

| Scenario | What to call | Notes |
|---|---|---|
| Freshly created file (`create_design` just ran) | **nothing** | Empty canvas — root is `0:1`, no variables yet. Skip Step 1, go straight to Step 2. |
| Opened existing file / file already loaded | `fetch_editor_state({includeSchema: false})` + `fetch_variables` | Parallel in one message. |
| Pure modification (file already loaded, target known) | The above **plus** any of `batch_read` / `capture_layout` / `capture_screenshot` as needed | All parallel in one message. |

> **Do NOT call `fetch_style_guide_tags`.** The tag list is static — read `../../rules/style-guide-tags.md` instead.

### Step 2: Creative vs. Compositional

- **Creative** (new screen, page, dashboard, restyle) → proceed to Steps 3–4
- **Compositional** ("add a button", "move this") → skip to Step 5 and load `design-rules.md`

### Step 3: Load Design Guidelines

Load **one or more** design-type guideline, first match wins:

| Priority | Trigger | File |
|---|---|---|
| 1 | slides, presentation, deck, 幻灯片, 演示文稿 | `references/guidelines-slides.md` |
| 2 | mobile, app, iOS, Android, 移动端 | `references/guidelines-mobile-app.md` |
| 3 | landing, marketing, SaaS, 落地页, 营销 | `references/guidelines-landing-page.md` |
| 4 | table, dashboard with tables, 表格 | `references/guidelines-table.md` |
| 5 | convert to code, to App, HTML, 转代码, 出码, 生成应用，转应用 | `references/guidelines-code.md` (+ `guidelines-tailwind.md` if Tailwind) |
| 6 | (web app, default) | `references/guidelines-web-app.md` |

`guidelines-code.md` / `guidelines-tailwind.md` are implementation guidelines and can be loaded **alongside** a design-type guideline when code generation is involved.

### Steps 4–6: Style + Space + Inspection (parallel)

Issue these as **a single parallel batch** in one message — they have no mutual dependency:

- **`fetch_style_guide(tags)`** — pick 5–10 fitting tags from `../../rules/style-guide-tags.md` (see the Selection Guidance section there).
- **`locate_available_space({width, height})`** — required for new top-level screens; skip for pure modification tasks. Never overlap existing content.
- **Inspection calls** (only if modifying existing design and not already covered in Step 1): `batch_read` (find by pattern/ID, `readDepth: 3` for component structure), `capture_layout` (detect problems), `capture_screenshot` (visual verify).

Skip any sub-call that doesn't apply to the current task. The point of parallel batching is to collapse independent reads into one round-trip, not to force every tool to run.

> If a follow-up read depends on this batch's result (e.g. `batch_read({readDepth: 3})` targeting a component discovered via an earlier `batch_read`), issue it as a separate message afterward. Most tasks don't need that.

### Step 7: Execute Design

`batch_edit` with ≤ 25 ops per call. Build order: **structure → content → style → verify**. Ops: **I()** Insert, **U()** Update, **C()** Copy, **M()** Move, **D()** Delete, **G()** Image. For detailed syntax and examples, load `references/ardot-workflow.md`.

### Step 8: Validate

Follow the **Post-Generation Validation Pattern** in `design-rules.md`. Use **tiered validation** — pick the lightest check that matches what the batch changed (T1 structural → `capture_layout` only; T2 content → skip; T3 visual → `capture_screenshot` only; T4 section-complete → both once; T5 final page → one screenshot). **Do not run full dual-verification after every batch_edit.** Enforce the convergence threshold: **max 2 fix iterations per section**, ignore ≤4px spacing noise, no subjective re-polishing once the section matches spec.

## Specialized Workflows

When the task matches one of the following, load the linked reference and follow it strictly (do not improvise the procedure from SKILL.md):

- **Slides / presentation / deck** → choose workflow based on the current model. When the model is **opus4.7**, ask the user whether to use the agent teams workflow (clarify that it takes more time and consumes more tokens): if yes, use `references/slides-agent-teams-workflow.md`; if no, use `references/slides-workflow.md`. For other models, use `references/slides-workflow.md` directly. Mandatory design rules live in `references/guidelines-slides.md`.
- **Website → style guide extraction** → `references/extract-style-guide-from-web.md`
- **Design → frontend code** → `references/design-to-code-workflow.md`

## Essential Constraints

These rules apply at all times. Full rule set and troubleshooting are in `design-rules.md`.

- **Every node needs a `name`** — assign meaningful names to all created nodes
- **Keep float colors to 2 decimals** — avoid long floating-point values
- **Text is invisible by default** — always set `fill` on text nodes
- **Use `fill` for all colors** — never use `textColor`, `backgroundColor`, `color`, or `fillColor`
- **Use `cornerRadius`** — not `borderRadius`
- **Font weight must be numeric strings** — `"400"`, `"700"`, not `"bold"`
- **Alignment uses uppercase enums** — `counterAxisAlignItems: "CENTER"`, not `alignItems: "center"`
- **Prefer flexbox layout** — always set `width` and `height` on new frames explicitly
- **Layout default sizing is FIXED** — when setting `layout` to `horizontal`/`vertical`, must explicitly set `width`/`height` for dynamic sizing
- **x/y are ignored in flexbox** — if you need to set x/y on children of flexbox parents, also set `layoutPositioning: "ABSOLUTE"`
- **`fill_container` requires flexbox parent** — only valid when parent has layout
- **`hug_contents` requires own flexbox layout** — only valid on a node that itself has flexbox layout
- **Default frame has white background** — set `fills: []` to remove
- **Max 25 ops per batch_edit** — split by logical sections
- **Every I/C/R needs a binding name** — `document` is predefined for root only
- **No U() on copied descendants** — copied nodes get new IDs; use `descendants` in C() instead
- **No image node type** — images are fills on frames; use G() with `"stock"` preferred
- **Icon frames must set `layout: "none"`** — and always `capture_screenshot()` to verify
- **Create icons as components** — then use `I(parentId, {type: "ref", ref: "iconId"})` to insert instances
- **Variable binding uses `$` prefix** — `fill: "$primary-color"`, `gap: "$spacing-small"`
- **Favor copying + updating** over generating from scratch
- **Parallelize independent reads** — when multiple MCP read calls have no data dependency (e.g. `fetch_editor_state` + `fetch_variables`), issue them in a single message as parallel tool calls; do not serialize them. **Exception**: never bundle these reads in the same message as `create_design` / `open_design` — wait for the file-ready context update first
- **Validate with tiered checks** — match the tier to the batch type (see `design-rules.md` Post-Generation Validation Pattern); do NOT run full screenshot+layout after every batch_edit
- **Text wrapping needs both** — `textAutoResize: "HEIGHT"` AND `width: "fill_container"` (or fixed width)
- **`lineHeight`** — set `lineHeight: "AUTO"` for automatic (preferred) or `lineHeight: 22` for explicit spacing

## 模块：image-to-ui

# Image to UI — 图生 UI

将参考图片（截图、线框图、设计稿截图、手绘草图等）转化为可编辑的 ardot 画布设计稿。

**核心流程**：图片 → 设计风格提取 → 结构化精细描述 → 反思校验 → 画布绘制

本 Skill 采用 4 阶段流水线，融合 Prompt Chaining + Reflection + Multi-Agent Collaboration 设计模式。

## 输出规则

**Phase 1~3 是 Agent 内部思考过程，所有中间数据（`design_spec`、`page_structure`、校验结果等）禁止输出给用户。** 用户只需要看到：
- 简短的进度提示（如"正在分析设计风格…""正在构建画布…"）
- Phase 4 完成后的最终画布截图和完成说明

## 触发场景

在以下情况下激活本技能：

- **截图还原**："把这张截图做成设计稿"、"还原这个界面"、"复刻这个页面"
- **图片参考设计**："参照这张图设计"、"按照这个风格做一个页面"、"照着这个截图画"
- **草图转设计**："把我的手绘草图转成设计稿"、"根据线框图生成界面"
- **中文关键词**："图生 UI"、"截图转设计稿"、"照着这张图做"、"参照设计"、"还原界面"

**与其他能力的区分**：

| 场景 | 使用的 Skill |
|------|-------------|
| 用户上传图片 → 生成 ardot 画布设计稿 | **本 Skill（image-to-ui）** |
| 用户纯文字描述 → 生成 ardot 画布设计稿 | `ardot-design-assistant` |
| 用户上传图片 → 只做结构化分析，不生成设计稿 | `image-understanding-native` |
| 用户上传图片 → 编辑/风格转换图片本身 | `text_to_image` / `edit_image` MCP 工具（图片创作） |

## 工作流程

### Phase 1：设计风格提取（内部，不输出）

**目标**：从参考图片中提取 `design_spec`，所有参数格式直接对齐 ardot design-mcp API。

1. **获取图片** — 从用户上传的图片或提供的 URL 获取图片内容
2. **加载 `image-understanding-native` Skill**，执行 **设计风格提取**（任务 B）
3. 看图提取 `design_spec`，覆盖 10 个维度：style_direction / colors / variables / typography / spacing / corner_radius / shadows / borders / icons / layout

### Phase 2：结构化精细描述（内部，不输出）

**目标**：基于 Phase 1 的 design_spec，执行全页面结构分析，得到 `page_structure`。

1. 继续使用 `image-understanding-native` Skill，执行 **全页面结构分析**（任务 A）
2. 分析时所有设计参数引用 Phase 1 的 `design_spec`：
   - section 的 background 颜色来自 `design_spec.colors`
   - element 的字号来自 `design_spec.typography.scale`
   - 间距值来自 `design_spec.spacing.patterns`

### Phase 3：反思校验（内部，不输出）

**目标**：独立评审 Phase 1 + Phase 2 的结果，确保足够完整和准确。

Agent 作为独立的 Critic 角色，**重新看原图**，检查 4 个维度：

| 维度 | PASS 条件 |
|------|----------|
| 风格完整性 | colors >= 5 角色、typography >= 3 级、spacing 有 base_unit + >= 3 pattern、variables >= 5 COLOR + >= 2 FLOAT |
| 结构覆盖率 | sections bbox 总面积 / 10000 >= 90% |
| 参数一致性 | page_structure 中颜色值与 design_spec.colors 匹配率 >= 80% |
| 可绘制性 | 100% elements 有 type + label + bbox，交互元素有 width/height |

**回退策略**：

| 问题类型 | 修复方式 |
|---------|---------|
| 风格参数缺失/不准 | 回到 Phase 1 补充提取 |
| 结构区域遗漏 | 回到 Phase 2 追加分析 |
| 参数不一致 | 用 design_spec 的值替换结构描述中的值 |
| 元素不可绘制 | 对缺参数的元素补充视觉属性 |

**最多 2 轮**（初始 + 1 次修正）。第 2 轮仍未全部 PASS 则降级继续进入 Phase 4。

### Phase 4：画布绘制 (Agent Teams)

**目标**：基于 `design_spec` + `page_structure`，在 ardot 画布上生成可编辑的设计稿。

**加载 `ardot-design-assistant` Skill**，按照其标准工作流执行。

#### Design Lead 执行步骤

0. 确保设计文件已打开 — `create_design` / `open_design`（如编辑器已有文件则跳过），等待就绪确认后再继续
1. `fetch_editor_state(includeSchema: false)` — 获取画布状态和可用组件（schema 和编辑指南已内置为 reference 文件）
2. 加载内置设计规范 — 根据 `design_spec.style_direction.platform` 读取对应的 `references/guidelines-*.md` 文件
3. `fetch_style_guide(tags: design_spec.style_direction.tags)` — 匹配内置风格
4. `apply_variables(variables: design_spec.variables)` — **直接传入**，设置设计 Token
5. `locate_available_space(width, height)` — 定位画布位置
6. `batch_edit` scaffold — 创建顶层 Frame + 每个 section 的 placeholder Frame

#### 复杂度评估

| sections 数量 | 执行模式 |
|--------------|---------|
| <= 3 | 单 Agent 逐 section 构建 |
| >= 4 | Team Mode：spawn sub-agents 并行构建 |

#### Team Mode 执行

1. `team_create("image-to-ui-team")`
2. 为每个 section spawn 一个 sub-agent，prompt 包含：
   - 目标 frame ID
   - 该 section 的 `page_structure` 片段
   - `design_spec` 精简版（只保留该 section 用到的部分）
   - ardot 规则约束（25 ops/call、text 需 fill、cornerRadius 等）
3. 等待所有 sub-agents 完成
4. `capture_screenshot` 各 section → 保存到 `/workspace/ardot-screenshots`，读取截图文件检查视觉正确性
5. `batch_edit` 修复整合问题
6. `capture_screenshot` 全页 → 读取截图文件做最终验证
7. `team_delete`

### 阶段间的信息传递

| 从 | 到 | 传递内容 | 消费方式 |
|----|-----|---------|---------|
| Phase 1 | Phase 2 | `design_spec` | 颜色/字号/间距引用 |
| Phase 1 | Phase 3 | `design_spec` | 校验风格完整性和参数一致性 |
| Phase 2 | Phase 3 | `page_structure` | 校验结构覆盖率和可绘制性 |
| Phase 1 | Phase 4 | `design_spec.variables` | 直接传给 `apply_variables` |
| Phase 1 | Phase 4 | `design_spec.style_direction.tags` | 传给 `fetch_style_guide` |
| Phase 1 | Phase 4 | `design_spec.typography/spacing/shadows` | sub-agent 的设计参数 |
| Phase 2 | Phase 4 | `page_structure.layout.sections` | scaffold 结构 + sub-agent 任务分解 |

### bbox → ardot 尺寸转换

Phase 2 的 bbox 是百分比坐标，Phase 4 需要转换为 ardot 的 px 值：
- `x_px = bbox.x / 100 * viewport.width`
- `y_px = bbox.y / 100 * viewport.height`
- `width_px = bbox.width / 100 * viewport.width`
- `height_px = bbox.height / 100 * viewport.height`

优先使用 `width`/`height` 字段中的精确 px 值（如 `"240px"`）；当该字段为 `"fill"` 或 `"auto"` 时，回退到 bbox 换算值。

### 用户文字优先

当用户同时提供了参考图片和文字描述，且两者存在差异时：
- **文字描述优先** — 用户的文字说明是最终意图
- **图片作为视觉参考** — 图片提供布局和风格的参考基线
- 例如：用户上传了一张蓝色主题的 dashboard 截图，但文字说"帮我做一个绿色主题的类似页面" → 布局参照截图，颜色用绿色

## 关键规则

1. **中间数据不输出** — Phase 1~3 的 `design_spec`、`page_structure`、校验结果等 JSON 是 Agent 内部数据，**禁止在对话中输出给用户**。只给简短进度提示。
2. **严格按 4 阶段顺序执行** — Phase 1 → 2 → 3 → 4，不跳过任何阶段
3. **Phase 1 和 Phase 2 不可合并** — 先完成完整的 design_spec，再做结构分析
4. **Phase 3 必须重新看原图** — 不能只看 Phase 1/2 的数据，必须回头看原图独立评审
5. **design_spec.variables 直接传给 apply_variables** — 不做任何格式转换
6. **typography.scale 直接用于 batch_edit** — fontWeight 用数字字符串，lineHeight 用 `{value, unit}` 格式
7. **最多 2 轮校验** — Phase 3 不通过则修正 1 次，第 2 轮仍未通过则降级继续
8. **用户文字说明优先于图片** — 文字描述与图片有冲突时以文字为准
9. **不重复加载 Skill** — 如果 image-understanding-native 或 ardot-design-assistant 已在上下文中，不需要重复加载

## 模块：image-understanding-native

# Image Understanding Native — 图片结构化语义分析

Agent 直接利用自身多模态能力，将 UI 截图/设计稿转化为结构化 JSON。零外部依赖，不启动 MCP Server，不调用外部模型。

## 四种分析任务

| 任务 | 输入 | 输出 | 加载文档 | 何时使用 |
|------|------|------|---------|---------|
| **A. 全页面结构分析** | 截图 | `page_structure` | `task-a-page-structure.md` | "分析截图"、"看看布局" |
| **B. 设计风格提取** | 截图 | `design_spec` | `task-b-design-spec.md` | `image-to-ui` Phase 1，或"提取设计风格" |
| **C. 区域语义描述** | 截图 + 区域 | `region_description` | `task-c-region.md` | "描述这个区域"、"这块是什么" |
| **D. 对比差异分析** | 两张截图 | `comparison` | `task-d-comparison.md` | "对比差异"、"改了什么" |

> **任务合并**：用户同时要结构分析和风格提取（如"分析截图并提取设计规范"），合并为一次输出。

## 加载协议

**每次任务必须加载**：
1. `references/common.md` — 通用约定（坐标系、精度、视口推断、bbox 方法论）
2. 对应任务的 reference 文件（见上表）

## 工作流

1. **准备图片** — 确保图片已在上下文中可访问（用户上传、COS 下载、截图工具等）
2. **加载文档** — 按加载协议加载 `common.md` + 对应任务文件
3. **执行分析** — 看图 → 按 Schema 输出 JSON
4. **输出** — JSON 代码块 + 自然语言摘要

**分析原则**：系统性扫描（从上到下、从左到右）→ 识别平台和视口 → 追求精确（颜色 hex、字号 px、间距具体值）→ 不确定时 `~` 前缀但不过度标注。

## 关键规则

1. **零外部依赖** — 全部分析由 Agent 自身完成
2. **输出即产物** — JSON 是自包含的，不假设特定下游
3. **追求精确** — 能给具体值就不用"约"
4. **严格遵循 Schema** — 按各任务文件中的 Schema 输出
5. **图片先准备好** — 分析前确保图片在上下文中可访问
