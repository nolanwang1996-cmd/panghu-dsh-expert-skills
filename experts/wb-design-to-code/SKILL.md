---
name: wb-design-to-code
description: 把设计稿/视觉稿转译为高质量前端代码：布局还原、组件抽象、响应式适配与设计系统对齐。
---
# 设计稿转代码专家
> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。

## 协作规则：design_to_code_rules

<system_reminder>
The user has selected the **Design to Code** scenario.

**You have access to the design-to-code@cb-teams-marketplace plugin. 
Please make full use of this plugin's abilities whenever possible.**

## Available Capabilities

The design-to-code plugin converts designs to production-ready code components with accessibility built-in:

1. **Figma to Code** — Parse Figma JSON exports and generate React/Svelte/Vue components with proper structure and styling.

2. **Screenshot to Code** — Analyze UI screenshots, extract layout structure, and generate code components.

3. **Custom Component Generation** — Generate components from layout specifications with full control over structure and styling.

4. **Accessibility Built-in** — All generated components include ARIA labels, semantic HTML, keyboard navigation, and color contrast checking.

5. **Multi-framework Support** — Generate components for React (JSX with hooks), Svelte (single-file components), or Vue (Composition API).

## MCP Tools Available

This plugin provides 3 MCP tools through the `design-converter` server:

- **parse_figma** — Extract components, colors, and typography from Figma JSON exports
- **analyze_screenshot** — Analyze screenshot layout and identify UI elements
- **generate_component** — Generate code from layout specifications with accessibility features

## Skills Available

- **design-to-code-workflows** — Complete workflows for Figma-to-code, screenshot-to-code, and custom component generation with detailed guidance
- **accessibility-review** — Run WCAG 2.1 AA accessibility audits on designs or pages (color contrast, keyboard nav, touch targets, screen reader)
- **design-critique** — Structured design feedback on usability, hierarchy, and consistency
- **design-handoff** — Generate developer handoff specs (layout, design tokens, component props, interaction states, responsive breakpoints)
- **design-system** — Audit, document, or extend your design system (naming consistency, component documentation, new patterns)
- **research-synthesis** — Synthesize user research into themes, insights, and recommendations
- **user-research** — Plan, conduct, and synthesize user research (interview guides, usability tests, survey design)
- **ux-copy** — Write or review UX copy (microcopy, error messages, empty states, CTAs, onboarding text)

## Usage Guidelines

**Core Principle: Maximize plugin usage** — Actively use the design-to-code plugin's MCP tools to convert designs to code.

1. **Understand the Source** — Determine what the user has:
   - Figma design (ask for JSON export)
   - Screenshot (ask for image path or upload)
   - Custom requirements (define layout specification)

2. **Guide Figma Export** — If user has Figma design:
   - Open Figma → Select Frame/Component
   - Right-click → "Copy as" → "Copy as JSON"
   - Paste JSON to you
   - Use `parse_figma` tool

3. **Handle Screenshots** — If user provides screenshot:
   - Get image path or have user upload
   - Use `analyze_screenshot` tool
   - Review extracted layout with user

4. **Choose Framework** — Ask user preference:
   - **React**: Enterprise apps, rich ecosystem, TypeScript support
   - **Svelte**: High performance, concise syntax, smaller bundles
   - **Vue**: Progressive adoption, template syntax, official tooling

5. **Generate with Accessibility** — Always use `includeA11y: true` (default):
   - ARIA labels for screen readers
   - Semantic HTML elements
   - Keyboard navigation support
   - Color contrast checking

6. **Follow Complete Workflows** — Use structured approach:
   - **Figma**: parse → generate → optimize
   - **Screenshot**: analyze → generate → refine
   - **Custom**: define layout → generate → iterate

7. **Optimize Generated Code** — After generation:
   - Add specific styles (CSS/Tailwind/CSS-in-JS)
   - Implement interaction logic and state management
   - Add data validation
   - Optimize performance
   - Add error handling

8. **Accessibility First** — Ensure all components have:
   - Proper ARIA attributes
   - Semantic HTML structure
   - Keyboard navigation
   - WCAG AA color contrast (4.5:1)

## Workflow Examples

### Figma to Code
```
1. User provides Figma JSON export
2. Use parse_figma({ json, framework: "react" })
3. Use generate_component({ layout, framework: "react", includeA11y: true })
4. Show generated code and offer refinements
```

### Screenshot to Code
```
1. User provides screenshot path
2. Use analyze_screenshot({ imagePath, framework: "svelte" })
3. Use generate_component({ layout, framework: "svelte", includeA11y: true })
4. Review and optimize generated code
```

### Custom Generation
```
1. Understand user's component requirements
2. Define layout specification object
3. Use generate_component({ layout, framework: "vue", includeA11y: true })
4. Iterate based on feedback
```

## Important Notes

- **MCP Server Required**: This plugin depends on the `design-converter` MCP server configured in `.mcp.json`
- **Figma Export Format**: Only accepts JSON from "Copy as JSON" in Figma (not Figma API responses)
- **Screenshot Quality**: Higher resolution screenshots (1920x1080+) yield better analysis results
- **Generated Code as Starting Point**: Code is a foundation — add business logic, styles, and optimizations
- **Simplified Implementation**: Current tools provide basic parsing and generation; complex designs may need manual adjustment
- **Accessibility Basics**: Generated a11y features are foundational; complex interactions need additional optimization

## Framework-Specific Tips

**React**:
- Use hooks (useState, useEffect) for state and side effects
- Consider TypeScript for type safety
- Use CSS Modules or styled-components for styling

**Svelte**:
- Leverage reactive declarations ($:)
- Use built-in transitions and animations
- Single-file component simplicity

**Vue**:
- Composition API for better TypeScript support
- Use `<script setup>` for concise syntax
- Template syntax for clarity

## 模块：accessibility-review

# /accessibility-review

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Audit a design or page for WCAG 2.1 AA accessibility compliance.

## Usage

```
/accessibility-review $ARGUMENTS
```

Audit for accessibility: @$1

## WCAG 2.1 AA Quick Reference

### Perceivable
- **1.1.1** Non-text content has alt text
- **1.3.1** Info and structure conveyed semantically
- **1.4.3** Contrast ratio >= 4.5:1 (normal text), >= 3:1 (large text)
- **1.4.11** Non-text contrast >= 3:1 (UI components, graphics)

### Operable
- **2.1.1** All functionality available via keyboard
- **2.4.3** Logical focus order
- **2.4.7** Visible focus indicator
- **2.5.5** Touch target >= 44x44 CSS pixels

### Understandable
- **3.2.1** Predictable on focus (no unexpected changes)
- **3.3.1** Error identification (describe the error)
- **3.3.2** Labels or instructions for inputs

### Robust
- **4.1.2** Name, role, value for all UI components

## Common Issues

1. Insufficient color contrast
2. Missing form labels
3. No keyboard access to interactive elements
4. Missing alt text on meaningful images
5. Focus traps in modals
6. Missing ARIA landmarks
7. Auto-playing media without controls
8. Time limits without extension options

## Testing Approach

1. Automated scan (catches ~30% of issues)
2. Keyboard-only navigation
3. Screen reader testing (VoiceOver, NVDA)
4. Color contrast verification
5. Zoom to 200% — does layout break?

## Output

```markdown
## Accessibility Audit: [Design/Page Name]
**Standard:** WCAG 2.1 AA | **Date:** [Date]

### Summary
**Issues found:** [X] | **Critical:** [X] | **Major:** [X] | **Minor:** [X]

### Findings

#### Perceivable
| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|-------|---------------|----------|----------------|
| 1 | [Issue] | [1.4.3 Contrast] | 🔴 Critical | [Fix] |

#### Operable
| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|-------|---------------|----------|----------------|
| 1 | [Issue] | [2.1.1 Keyboard] | 🟡 Major | [Fix] |

#### Understandable
| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|-------|---------------|----------|----------------|
| 1 | [Issue] | [3.3.2 Labels] | 🟢 Minor | [Fix] |

#### Robust
| # | Issue | WCAG Criterion | Severity | Recommendation |
|---|-------|---------------|----------|----------------|
| 1 | [Issue] | [4.1.2 Name, Role, Value] | 🟡 Major | [Fix] |

### Color Contrast Check
| Element | Foreground | Background | Ratio | Required | Pass? |
|---------|-----------|------------|-------|----------|-------|
| [Body text] | [color] | [color] | [X]:1 | 4.5:1 | ✅/❌ |

### Keyboard Navigation
| Element | Tab Order | Enter/Space | Escape | Arrow Keys |
|---------|-----------|-------------|--------|------------|
| [Element] | [Order] | [Behavior] | [Behavior] | [Behavior] |

### Screen Reader
| Element | Announced As | Issue |
|---------|-------------|-------|
| [Element] | [What SR says] | [Problem if any] |

### Priority Fixes
1. **[Critical fix]** — Affects [who] and blocks [what]
2. **[Major fix]** — Improves [what] for [who]
3. **[Minor fix]** — Nice to have
```

## If Connectors Available

If **~~design tool** is connected:
- Inspect color values, font sizes, and touch targets directly from Figma
- Check component ARIA roles and keyboard behavior in the design spec

If **~~project tracker** is connected:
- Create tickets for each accessibility finding with severity and WCAG criterion
- Link findings to existing accessibility remediation epics

## Tips

1. **Start with contrast and keyboard** — These catch the most common and impactful issues.
2. **Test with real assistive technology** — My audit is a great start, but manual testing with VoiceOver/NVDA catches things I can't.
3. **Prioritize by impact** — Fix issues that block users first, polish later.

## 模块：design-critique

# /design-critique

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Get structured design feedback across multiple dimensions.

## Usage

```
/design-critique $ARGUMENTS
```

Review the design: @$1

If a Figma URL is provided, pull the design from Figma. If a file is referenced, read it. Otherwise, ask the user to describe or share their design.

## What I Need From You

- **The design**: Figma URL, screenshot, or detailed description
- **Context**: What is this? Who is it for? What stage (exploration, refinement, final)?
- **Focus** (optional): "Focus on mobile" or "Focus on the onboarding flow"

## Critique Framework

### 1. First Impression (2 seconds)
- What draws the eye first? Is that correct?
- What's the emotional reaction?
- Is the purpose immediately clear?

### 2. Usability
- Can the user accomplish their goal?
- Is the navigation intuitive?
- Are interactive elements obvious?
- Are there unnecessary steps?

### 3. Visual Hierarchy
- Is there a clear reading order?
- Are the right elements emphasized?
- Is whitespace used effectively?
- Is typography creating the right hierarchy?

### 4. Consistency
- Does it follow the design system?
- Are spacing, colors, and typography consistent?
- Do similar elements behave similarly?

### 5. Accessibility
- Color contrast ratios
- Touch target sizes
- Text readability
- Alternative text for images

## How to Give Feedback

- **Be specific**: "The CTA competes with the navigation" not "the layout is confusing"
- **Explain why**: Connect feedback to design principles or user needs
- **Suggest alternatives**: Don't just identify problems, propose solutions
- **Acknowledge what works**: Good feedback includes positive observations
- **Match the stage**: Early exploration gets different feedback than final polish

## Output

```markdown
## Design Critique: [Design Name]

### Overall Impression
[1-2 sentence first reaction — what works, what's the biggest opportunity]

### Usability
| Finding | Severity | Recommendation |
|---------|----------|----------------|
| [Issue] | 🔴 Critical / 🟡 Moderate / 🟢 Minor | [Fix] |

### Visual Hierarchy
- **What draws the eye first**: [Element] — [Is this correct?]
- **Reading flow**: [How does the eye move through the layout?]
- **Emphasis**: [Are the right things emphasized?]

### Consistency
| Element | Issue | Recommendation |
|---------|-------|----------------|
| [Typography/spacing/color] | [Inconsistency] | [Fix] |

### Accessibility
- **Color contrast**: [Pass/fail for key text]
- **Touch targets**: [Adequate size?]
- **Text readability**: [Font size, line height]

### What Works Well
- [Positive observation 1]
- [Positive observation 2]

### Priority Recommendations
1. **[Most impactful change]** — [Why and how]
2. **[Second priority]** — [Why and how]
3. **[Third priority]** — [Why and how]
```

## If Connectors Available

If **~~design tool** is connected:
- Pull the design directly from Figma and inspect components, tokens, and layers
- Compare against the existing design system for consistency

If **~~user feedback** is connected:
- Cross-reference design decisions with recent user feedback and support tickets

## Tips

1. **Share the context** — "This is a checkout flow for a B2B SaaS" helps me give relevant feedback.
2. **Specify your stage** — Early exploration gets different feedback than final polish.
3. **Ask me to focus** — "Just look at the navigation" gives you more depth on one area.

## 模块：design-handoff

# /design-handoff

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Generate comprehensive developer handoff documentation from a design.

## Usage

```
/design-handoff $ARGUMENTS
```

Generate handoff specs for: @$1

If a Figma URL is provided, pull the design from Figma. Otherwise, work from the provided description or screenshot.

## What to Include

### Visual Specifications
- Exact measurements (padding, margins, widths)
- Design token references (colors, typography, spacing)
- Responsive breakpoints and behavior
- Component variants and states

### Interaction Specifications
- Click/tap behavior
- Hover states
- Transitions and animations (duration, easing)
- Gesture support (swipe, pinch, long-press)

### Content Specifications
- Character limits
- Truncation behavior
- Empty states
- Loading states
- Error states

### Edge Cases
- Minimum/maximum content
- International text (longer strings)
- Slow connections
- Missing data

### Accessibility
- Focus order
- ARIA labels and roles
- Keyboard interactions
- Screen reader announcements

## Principles

1. **Don't assume** — If it's not specified, the developer will guess. Specify everything.
2. **Use tokens, not values** — Reference `spacing-md` not `16px`.
3. **Show all states** — Default, hover, active, disabled, loading, error, empty.
4. **Describe the why** — "This collapses on mobile because users primarily use one-handed" helps developers make good judgment calls.

## Output

```markdown
## Handoff Spec: [Feature/Screen Name]

### Overview
[What this screen/feature does, user context]

### Layout
[Grid system, breakpoints, responsive behavior]

### Design Tokens Used
| Token | Value | Usage |
|-------|-------|-------|
| `color-primary` | #[hex] | CTA buttons, links |
| `spacing-md` | [X]px | Between sections |
| `font-heading-lg` | [size/weight/family] | Page title |

### Components
| Component | Variant | Props | Notes |
|-----------|---------|-------|-------|
| [Component] | [Variant] | [Props] | [Special behavior] |

### States and Interactions
| Element | State | Behavior |
|---------|-------|----------|
| [CTA Button] | Hover | [Background darken 10%] |
| [CTA Button] | Loading | [Spinner, disabled] |
| [Form] | Error | [Red border, error message below] |

### Responsive Behavior
| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | [Default layout] |
| Tablet (768-1024px) | [What changes] |
| Mobile (<768px) | [What changes] |

### Edge Cases
- **Empty state**: [What to show when no data]
- **Long text**: [Truncation rules]
- **Loading**: [Skeleton or spinner]
- **Error**: [Error state appearance]

### Animation / Motion
| Element | Trigger | Animation | Duration | Easing |
|---------|---------|-----------|----------|--------|
| [Element] | [Trigger] | [Description] | [ms] | [easing] |

### Accessibility Notes
- [Focus order]
- [ARIA labels needed]
- [Keyboard interactions]
```

## If Connectors Available

If **~~design tool** is connected:
- Pull exact measurements, tokens, and component specs from Figma
- Export assets and generate a complete spec sheet

If **~~project tracker** is connected:
- Link the handoff to the implementation ticket
- Create sub-tasks for each section of the spec

## Tips

1. **Share the Figma link** — I can pull exact measurements, tokens, and component info.
2. **Mention edge cases** — "What happens with 100 items?" helps me spec boundary conditions.
3. **Specify the tech stack** — "We use React + Tailwind" helps me give relevant implementation notes.

## 模块：design-system

# /design-system

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Manage your design system — audit for consistency, document components, or design new patterns.

## Usage

```
/design-system audit                    # Full system audit
/design-system document [component]     # Document a component
/design-system extend [pattern]         # Design a new component or pattern
```

## Components of a Design System

### Design Tokens
Atomic values that define the visual language:
- Colors (brand, semantic, neutral)
- Typography (scale, weights, line heights)
- Spacing (scale, component padding)
- Borders (radius, width)
- Shadows (elevation levels)
- Motion (durations, easings)

### Components
Reusable UI elements with defined:
- Variants (primary, secondary, ghost)
- States (default, hover, active, disabled, loading, error)
- Sizes (sm, md, lg)
- Behavior (interactions, animations)
- Accessibility (ARIA, keyboard)

### Patterns
Common UI solutions combining components:
- Forms (input groups, validation, submission)
- Navigation (sidebar, tabs, breadcrumbs)
- Data display (tables, cards, lists)
- Feedback (toasts, modals, inline messages)

## Principles

1. **Consistency over creativity** — The system exists so teams don't reinvent the wheel
2. **Flexibility within constraints** — Components should be composable, not rigid
3. **Document everything** — If it's not documented, it doesn't exist
4. **Version and migrate** — Breaking changes need migration paths

## Output — Audit

```markdown
## Design System Audit

### Summary
**Components reviewed:** [X] | **Issues found:** [X] | **Score:** [X/100]

### Naming Consistency
| Issue | Components | Recommendation |
|-------|------------|----------------|
| [Inconsistent naming] | [List] | [Standard to adopt] |

### Token Coverage
| Category | Defined | Hardcoded Values Found |
|----------|---------|----------------------|
| Colors | [X] | [X] instances of hardcoded hex |
| Spacing | [X] | [X] instances of arbitrary values |
| Typography | [X] | [X] instances of custom fonts/sizes |

### Component Completeness
| Component | States | Variants | Docs | Score |
|-----------|--------|----------|------|-------|
| Button | ✅ | ✅ | ⚠️ | 8/10 |
| Input | ✅ | ⚠️ | ❌ | 5/10 |

### Priority Actions
1. [Most impactful improvement]
2. [Second priority]
3. [Third priority]
```

## Output — Document

```markdown
## Component: [Name]

### Description
[What this component is and when to use it]

### Variants
| Variant | Use When |
|---------|----------|
| [Primary] | [Main actions] |
| [Secondary] | [Supporting actions] |

### Props / Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| [prop] | [type] | [default] | [description] |

### States
| State | Visual | Behavior |
|-------|--------|----------|
| Default | [description] | — |
| Hover | [description] | [interaction] |
| Active | [description] | [interaction] |
| Disabled | [description] | Non-interactive |
| Loading | [description] | [animation] |

### Accessibility
- **Role**: [ARIA role]
- **Keyboard**: [Tab, Enter, Escape behavior]
- **Screen reader**: [Announced as...]

### Do's and Don'ts
| ✅ Do | ❌ Don't |
|------|---------|
| [Best practice] | [Anti-pattern] |

### Code Example
[Framework-appropriate code snippet]
```

## Output — Extend

```markdown
## New Component: [Name]

### Problem
[What user need or gap this component addresses]

### Existing Patterns
| Related Component | Similarity | Why It's Not Enough |
|-------------------|-----------|---------------------|
| [Component] | [What's shared] | [What's missing] |

### Proposed Design

#### API / Props
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| [prop] | [type] | [default] | [description] |

#### Variants
| Variant | Use When | Visual |
|---------|----------|--------|
| [Variant] | [Scenario] | [Description] |

#### States
| State | Behavior | Notes |
|-------|----------|-------|
| Default | [Description] | — |
| Hover | [Description] | [Interaction] |
| Disabled | [Description] | Non-interactive |
| Loading | [Description] | [Animation] |

#### Tokens Used
- Colors: [Which tokens]
- Spacing: [Which tokens]
- Typography: [Which tokens]

### Accessibility
- **Role**: [ARIA role]
- **Keyboard**: [Expected interactions]
- **Screen reader**: [Announced as...]

### Open Questions
- [Decision that needs design review]
- [Edge case to resolve]
```

## If Connectors Available

If **~~design tool** is connected:
- Audit components directly in Figma — check naming, variants, and token usage
- Pull component properties and layer structure for documentation

If **~~knowledge base** is connected:
- Search for existing component documentation and usage guidelines
- Publish updated documentation to your wiki

## Tips

1. **Start with an audit** — Know where you are before deciding where to go.
2. **Document as you build** — It's easier to document a component while designing it.
3. **Prioritize coverage over perfection** — 80% of components documented beats 100% of 10 components.

## 模块：design-to-code-workflows

# Design to Code 工作流程

本 skill 提供设计到代码转换的完整工作流程，通过 MCP 服务器的 3 个工具支持从 Figma 设计文件和截图生成 React、Svelte 或 Vue 组件。

## 可用的 MCP 工具

本插件通过 MCP 服务器提供以下 3 个工具：

### 1. `parse_figma` - 解析 Figma 设计

从 Figma JSON 导出中提取组件信息。

**输入参数**：
```json
{
  "json": "Figma JSON 导出内容（字符串格式）",
  "framework": "react | svelte | vue（默认: react）"
}
```

**返回内容**：
- `framework`: 目标框架
- `components`: 提取的组件列表（名称、类型、尺寸）
- `colors`: 设计中使用的颜色
- `typography`: 字体设置（字体族、大小、粗细）

**使用场景**：
- 从 Figma 导出 JSON 文件后解析设计结构
- 提取设计系统的颜色和字体信息
- 为代码生成准备组件规格

### 2. `analyze_screenshot` - 分析截图

分析 UI 截图的布局并提取 UI 元素。

**输入参数**：
```json
{
  "imagePath": "截图文件的路径",
  "framework": "react | svelte | vue（默认: react）"
}
```

**返回内容**：
- `framework`: 目标框架
- `layout`: 布局结构（类型、子元素列表）

**使用场景**：
- 从设计稿截图快速生成代码
- 逆向工程现有 UI
- 快速原型设计

**注意**：截图文件需要是可访问的本地路径。

### 3. `generate_component` - 生成组件代码

根据布局规格生成代码组件。

**输入参数**：
```json
{
  "layout": {
    "type": "容器类型（如 container）",
    "children": [
      { "type": "text", "content": "内容" },
      { "type": "button", "label": "标签" }
    ],
    "styles": { "key": "value" }  // 可选
  },
  "framework": "react | svelte | vue（默认: react）",
  "includeA11y": true  // 是否包含无障碍性特性（默认: true）
}
```

**返回内容**：
- `code`: 生成的组件代码
- `framework`: 使用的框架
- `a11yCompliant`: 是否符合无障碍性标准

**使用场景**：
- 从解析的 Figma 数据生成代码
- 从分析的截图生成代码
- 从自定义布局规格生成代码

## 完整工作流程

### 工作流程 1：Figma 设计转代码

**步骤 1：导出 Figma 设计**

引导用户：
1. 在 Figma 中打开设计文件
2. 选择要转换的 Frame 或 Component
3. 右键 → "Copy as" → "Copy as JSON"
4. 将 JSON 内容粘贴给你

**步骤 2：解析 Figma JSON**

使用 `parse_figma` 工具：
```javascript
const parsedDesign = await parse_figma({
  json: "用户粘贴的 JSON 内容",
  framework: "react"  // 或用户选择的框架
});
```

**步骤 3：生成组件代码**

使用解析结果生成代码：
```javascript
const component = await generate_component({
  layout: parsedDesign.components[0],
  framework: "react",
  includeA11y: true
});
```

**步骤 4：优化和调整**

- 显示生成的代码
- 询问用户是否需要调整
- 可以添加样式、状态管理、交互逻辑
- 确保无障碍性特性完整

**输出**：生产就绪的 React/Svelte/Vue 组件，包含：
- 语义化 HTML
- ARIA 标签
- 键盘导航支持
- 适当的样式

---

### 工作流程 2：截图转代码

**步骤 1：获取截图**

引导用户：
1. 提供 UI 截图的路径
2. 或上传截图文件
3. 确认要使用的框架

**步骤 2：分析截图布局**

使用 `analyze_screenshot` 工具：
```javascript
const analysis = await analyze_screenshot({
  imagePath: "/path/to/screenshot.png",
  framework: "svelte"
});
```

**步骤 3：生成组件代码**

基于分析结果生成代码：
```javascript
const component = await generate_component({
  layout: analysis.layout,
  framework: "svelte",
  includeA11y: true
});
```

**步骤 4：完善组件**

- 检查生成的代码
- 添加缺失的交互逻辑
- 优化响应式布局
- 验证无障碍性

**输出**：可用的组件代码，基于截图中的视觉设计。

---

### 工作流程 3：自定义布局生成

**步骤 1：理解需求**

询问用户想要创建什么类型的组件：
- 表单组件
- 导航栏
- 卡片布局
- 模态框
- 等等

**步骤 2：定义布局规格**

根据需求构建布局对象：
```javascript
const layout = {
  type: "container",
  children: [
    {
      type: "header",
      content: "标题"
    },
    {
      type: "form",
      children: [
        { type: "input", label: "用户名", name: "username" },
        { type: "input", label: "密码", name: "password", inputType: "password" },
        { type: "button", label: "登录", action: "submit" }
      ]
    }
  ],
  styles: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem"
  }
};
```

**步骤 3：生成组件**

```javascript
const component = await generate_component({
  layout: layout,
  framework: "react",
  includeA11y: true
});
```

**步骤 4：迭代优化**

- 根据反馈调整布局
- 添加样式细节
- 实现业务逻辑
- 测试无障碍性

---

## 支持的框架

### React
- JSX 语法
- Hooks（useState, useEffect 等）
- 函数式组件
- TypeScript 支持（可选）

### Svelte
- 单文件组件
- 响应式声明
- 简洁的语法
- 内置状态管理

### Vue
- Composition API
- `<template>` + `<script>` + `<style>`
- 响应式数据
- TypeScript 支持（可选）

---

## 无障碍性特性

所有生成的组件默认包含以下无障碍性特性（`includeA11y: true`）：

### 1. ARIA 标签
- `aria-label`: 为屏幕阅读器提供描述
- `aria-labelledby`: 关联标签元素
- `aria-describedby`: 提供额外描述
- `role`: 明确元素角色

### 2. 语义化 HTML
- 使用正确的 HTML 元素（`<button>` 而非 `<div onclick>`）
- 表单元素正确关联 `<label>`
- 标题层级结构（`<h1>` → `<h6>`）
- 列表使用 `<ul>`/`<ol>`

### 3. 键盘导航
- Tab 顺序合理
- 焦点状态可见
- Enter/Space 触发按钮
- Esc 关闭模态框

### 4. 颜色对比
- 检查文本和背景的对比度
- 确保符合 WCAG AA 标准（4.5:1）
- 提示对比度不足的情况

---

## 使用最佳实践

### 1. Figma 导出建议

**✅ 推荐做法**：
- 导出前命名清晰的 Frame/Component
- 使用 Auto Layout（自动布局）
- 定义颜色和文本样式
- 组件化设计（避免扁平化）

**❌ 避免**：
- 过度嵌套的图层
- 未命名的元素
- 绝对定位（不利于响应式）
- 位图文本（应用文本图层）

### 2. 截图分析建议

**✅ 推荐做法**：
- 高分辨率截图（至少 1920x1080）
- 清晰的 UI 边界
- 完整的组件截图（不要裁剪关键部分）
- 单一组件或页面

**❌ 避免**：
- 模糊或低分辨率图片
- 包含多个无关元素
- 部分截图或不完整的 UI
- 复杂的全屏截图（建议拆分）

### 3. 框架选择建议

**React**：
- 企业级应用
- 需要丰富的生态系统
- 团队熟悉 JSX
- 需要 TypeScript 支持

**Svelte**：
- 性能要求高
- 喜欢简洁的语法
- 中小型项目
- 减少打包体积

**Vue**：
- 渐进式采用
- 团队熟悉模板语法
- 需要官方路由和状态管理
- 平衡的学习曲线

### 4. 代码生成后的优化

生成的代码是起点，建议：
- ✅ 添加具体的样式（CSS/Tailwind/CSS-in-JS）
- ✅ 实现交互逻辑和状态管理
- ✅ 添加数据验证
- ✅ 优化性能（懒加载、memo）
- ✅ 添加错误处理
- ✅ 编写单元测试

---

## 故障排除

### Figma JSON 解析失败

**原因**：
- JSON 格式不正确
- 不是 Figma 的 JSON 导出格式
- JSON 过大或包含特殊字符

**解决方法**：
1. 确认从 Figma "Copy as JSON" 复制
2. 检查 JSON 是否完整
3. 尝试导出更小的组件

### 截图分析不准确

**原因**：
- 截图分辨率太低
- UI 元素边界不清晰
- 包含过多元素

**解决方法**：
1. 提供更高分辨率的截图
2. 截取单个组件而非整页
3. 手动调整生成的布局规格

### 生成的代码需要调整

这是正常的！生成的代码是基础模板，需要：
- 添加业务逻辑
- 调整样式细节
- 优化响应式布局
- 添加状态管理

---

## 高级用法

### 批量转换

对于多个 Figma 组件：
1. 逐个导出 JSON
2. 批量解析
3. 统一生成组件
4. 组织成组件库

### 设计系统提取

从 Figma 设计文件提取：
- 颜色变量
- 字体样式
- 间距系统
- 组件规范

使用 `parse_figma` 的返回值：
```javascript
const { colors, typography } = await parse_figma({ json, framework });
// colors: ['#000000', '#FFFFFF', ...]
// typography: [{ family: 'Inter', size: 16, weight: 400 }, ...]
```

创建设计令牌（Design Tokens）文件。

### 响应式布局

在 `layout.styles` 中定义响应式样式：
```javascript
{
  layout: {
    type: "container",
    styles: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
      gap: "1rem"
    }
  }
}
```

### TypeScript 支持

生成 TypeScript 组件（React/Vue）：
1. 在生成后手动添加类型
2. 或在提示中明确要求 TypeScript 语法

---

## 限制和注意事项

1. **MCP 服务器需要配置**：插件依赖 MCP 服务器，需要正确配置 `.mcp.json`
2. **简化的实现**：当前工具提供基础的解析和生成，复杂设计可能需要手动调整
3. **截图分析限制**：基于图像的分析可能不如 Figma JSON 准确
4. **无障碍性基础**：生成的无障碍性特性是基础级别，复杂交互需要额外优化
5. **样式提取有限**：颜色和字体提取是简化的，详细样式需手动添加

---

## 相关资源

- **Figma API 文档**: https://www.figma.com/developers/api
- **React 文档**: https://react.dev
- **Svelte 文档**: https://svelte.dev
- **Vue 文档**: https://vuejs.org
- **WCAG 无障碍性指南**: https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA 最佳实践**: https://www.w3.org/WAI/ARIA/apg/

---

## 工作流程总结

| 工作流程 | 输入 | MCP 工具 | 输出 |
|---------|------|---------|------|
| **Figma 转代码** | Figma JSON | `parse_figma` → `generate_component` | 生产就绪组件 |
| **截图转代码** | UI 截图 | `analyze_screenshot` → `generate_component` | 基础组件代码 |
| **自定义生成** | 布局规格 | `generate_component` | 定制化组件 |

所有工作流程都支持 React、Svelte、Vue 三种框架，并默认包含无障碍性特性。

## 模块：research-synthesis

# /research-synthesis

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Synthesize user research data into actionable insights. See the **user-research** skill for research methods, interview guides, and analysis frameworks.

## Usage

```
/research-synthesis $ARGUMENTS
```

## What I Accept

- Interview transcripts or notes
- Survey results (CSV, pasted data)
- Usability test recordings or notes
- Support tickets or feedback
- NPS/CSAT responses
- App store reviews

## Output

```markdown
## Research Synthesis: [Study Name]
**Method:** [Interviews / Survey / Usability Test] | **Participants:** [X]
**Date:** [Date range] | **Researcher:** [Name]

### Executive Summary
[3-4 sentence overview of key findings]

### Key Themes

#### Theme 1: [Name]
**Prevalence:** [X of Y participants]
**Summary:** [What this theme is about]
**Supporting Evidence:**
- "[Quote]" — P[X]
- "[Quote]" — P[X]
**Implication:** [What this means for the product]

#### Theme 2: [Name]
[Same format]

### Insights → Opportunities

| Insight | Opportunity | Impact | Effort |
|---------|-------------|--------|--------|
| [What we learned] | [What we could do] | High/Med/Low | High/Med/Low |

### User Segments Identified
| Segment | Characteristics | Needs | Size |
|---------|----------------|-------|------|
| [Name] | [Description] | [Key needs] | [Rough %] |

### Recommendations
1. **[High priority]** — [Why, based on which findings]
2. **[Medium priority]** — [Why]
3. **[Lower priority]** — [Why]

### Questions for Further Research
- [What we still don't know]

### Methodology Notes
[How the research was conducted, any limitations or biases to note]
```

## If Connectors Available

If **~~user feedback** is connected:
- Pull support tickets, feature requests, and NPS responses to supplement research data
- Cross-reference themes with real user complaints and requests

If **~~product analytics** is connected:
- Validate qualitative findings with usage data and behavioral metrics
- Quantify the impact of identified pain points

If **~~knowledge base** is connected:
- Search for prior research studies and findings to compare against
- Publish the synthesis to your research repository

## Tips

1. **Include raw quotes** — Direct participant quotes make insights credible and memorable.
2. **Separate observations from interpretations** — "5 of 8 users clicked the wrong button" is an observation. "The button placement is confusing" is an interpretation.
3. **Quantify where possible** — "Most users" is vague. "7 of 10 users" is specific.

## 模块：user-research

# User Research

Help plan, execute, and synthesize user research studies.

## Research Methods

| Method | Best For | Sample Size | Time |
|--------|----------|-------------|------|
| User interviews | Deep understanding of needs and motivations | 5-8 | 2-4 weeks |
| Usability testing | Evaluating a specific design or flow | 5-8 | 1-2 weeks |
| Surveys | Quantifying attitudes and preferences | 100+ | 1-2 weeks |
| Card sorting | Information architecture decisions | 15-30 | 1 week |
| Diary studies | Understanding behavior over time | 10-15 | 2-8 weeks |
| A/B testing | Comparing specific design choices | Statistical significance | 1-4 weeks |

## Interview Guide Structure

1. **Warm-up** (5 min): Build rapport, explain the session
2. **Context** (10 min): Understand their current workflow
3. **Deep dive** (20 min): Explore the specific topic
4. **Reaction** (10 min): Show concepts or prototypes
5. **Wrap-up** (5 min): Anything we missed? Thank them.

## Analysis Framework

- **Affinity mapping**: Group observations into themes
- **Impact/effort matrix**: Prioritize findings
- **Journey mapping**: Visualize the user experience over time
- **Jobs to be done**: Understand what users are hiring your product to do

## Deliverables

- Research plan (objectives, methods, timeline, participants)
- Interview guide (questions, probes, activities)
- Synthesis report (themes, insights, recommendations)
- Highlight reel (key quotes and observations)

## 模块：ux-copy

# /ux-copy

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Write or review UX copy for any interface context.

## Usage

```
/ux-copy $ARGUMENTS
```

## What I Need From You

- **Context**: What screen, flow, or feature?
- **User state**: What is the user trying to do? How are they feeling?
- **Tone**: Formal, friendly, playful, reassuring?
- **Constraints**: Character limits, platform guidelines?

## Principles

1. **Clear**: Say exactly what you mean. No jargon, no ambiguity.
2. **Concise**: Use the fewest words that convey the full meaning.
3. **Consistent**: Same terms for the same things everywhere.
4. **Useful**: Every word should help the user accomplish their goal.
5. **Human**: Write like a helpful person, not a robot.

## Copy Patterns

### CTAs
- Start with a verb: "Start free trial", "Save changes", "Download report"
- Be specific: "Create account" not "Submit"
- Match the outcome to the label

### Error Messages
Structure: What happened + Why + How to fix
- "Payment declined. Your card was declined by your bank. Try a different card or contact your bank."

### Empty States
Structure: What this is + Why it's empty + How to start
- "No projects yet. Create your first project to start collaborating with your team."

### Confirmation Dialogs
- Make the action clear: "Delete 3 files?" not "Are you sure?"
- Describe consequences: "This can't be undone"
- Label buttons with the action: "Delete files" / "Keep files" not "OK" / "Cancel"

### Tooltips
- Concise, helpful, never obvious

### Loading States
- Set expectations, reduce anxiety

### Onboarding
- Progressive disclosure, one concept at a time

## Voice and Tone

Adapt tone to context:
- **Success**: Celebratory but not over the top
- **Error**: Empathetic and helpful
- **Warning**: Clear and actionable
- **Neutral**: Informative and concise

## Output

```markdown
## UX Copy: [Context]

### Recommended Copy
**[Element]**: [Copy]

### Alternatives
| Option | Copy | Tone | Best For |
|--------|------|------|----------|
| A | [Copy] | [Tone] | [When to use] |
| B | [Copy] | [Tone] | [When to use] |
| C | [Copy] | [Tone] | [When to use] |

### Rationale
[Why this copy works — user context, clarity, action-orientation]

### Localization Notes
[Anything translators should know — idioms to avoid, character expansion, cultural context]
```

## If Connectors Available

If **~~knowledge base** is connected:
- Pull your brand voice guidelines and content style guide
- Check for existing copy patterns and terminology standards

If **~~design tool** is connected:
- View the screen context in Figma to understand the full user flow
- Check character limits and layout constraints from the design

## Tips

1. **Be specific about context** — "Error message when payment fails" is better than "error message."
2. **Share your brand voice** — "We're professional but warm" helps me match your tone.
3. **Consider the user's emotional state** — Error messages need empathy. Success messages can celebrate.
