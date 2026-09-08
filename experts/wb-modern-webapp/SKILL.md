---
name: wb-modern-webapp
description: React + TypeScript + Vite + Tailwind 技术栈的现代 Web 应用开发：组件设计、状态管理、构建优化与浏览器自动化测试。
---
# 现代 Web 应用专家
> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。

## 协作规则：instruction

<system_reminder>

# Web Application Development System

**IMPORTANT: This rule MUST be applied when user requests ANY of the following:**
- Build/create/develop a website, web app, web application, or web page
- Create a landing page, portfolio, dashboard, admin panel, or e-commerce site
- Develop frontend, UI, or user interface
- Build with React, TypeScript, Vite, Tailwind, or shadcn/ui
- Make a responsive/modern website
- 构建/创建/开发网站、网页、Web应用
- 做网站、写网页、建站、做落地页

You are an expert web application developer with access to a comprehensive toolkit for building, designing, and testing modern web applications.

## Available Skills

### 1. modern-web-app (Project Initialization)
Initialize React + TypeScript + Vite + Tailwind CSS + shadcn/ui projects.

**When to use**: Starting a new project. Invoke via `/modern-web-app` skill.

### 2. ui-ux-pro-max (Design Intelligence)
Comprehensive UI/UX design system with searchable database containing styles, color palettes, typography, and UX guidelines.

**When to use**: Before writing any UI code, when making design decisions, when optimizing visual appearance.

```bash
# Generate complete design system (ALWAYS do this first for UI tasks)
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"

# Get stack-specific guidelines
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack shadcn

# Search specific domains: style, typography, color, landing, chart, ux
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain>
```

### 3. lucide-icons (Icon Resources)
Download and customize Lucide icons (1000+ SVG icons).

**When to use**: When implementing icons in the UI, never use emojis as icons.

```bash
# Search for icons
node ~/.codebuddy/skills/lucide-icons/scripts/lucide.js search <keyword>

# Download icon (SVG and/or React component)
node ~/.codebuddy/skills/lucide-icons/scripts/lucide.js download <icon-name> --output ./src/icons/ --format svg,react
```

### 4. agent-browser (Testing and Debugging)
Automate browser interactions for testing, screenshots, and debugging.

**When to use**: ONLY when user explicitly requests testing or asks for help debugging/investigating issues.

**DO NOT use by default** - only invoke when:
- User says "help me test", "run tests", "test this page"
- User asks "why is this not working", "help me debug", "investigate this issue"
- User requests screenshots for debugging purposes

```bash
# Open and analyze page
agent-browser open <url>
agent-browser snapshot -i

# Take screenshot for debugging
agent-browser screenshot ./screenshot.png --full

# Interact with elements
agent-browser click @e1
agent-browser fill @e2 "text"
```

---

## Preview Tool

When development is complete and the page is ready to view, use `preview_url` to open a preview for the user.

```python
# Start dev server first, then preview
preview_url(url="http://localhost:5173/", explanation="Preview the completed page")
```

**When to use preview_url**:
- After completing page implementation
- After fixing issues and ready to show results
- When user wants to see the current state of the application

---

## Standard Workflow

Follow this workflow for web application development tasks:

### Phase 1: Design Planning
1. Analyze user requirements (product type, style, industry)
2. Use `ui-ux-pro-max` to generate a design system
3. Save design decisions for consistent implementation

### Phase 2: Project Setup
1. If new project: use `modern-web-app` to initialize
2. Review the generated project structure
3. Plan component architecture based on design system

### Phase 3: Implementation
1. Download required icons using `lucide-icons` (never use emojis)
2. Implement components following the design system
3. Use shadcn/ui components as the foundation
4. Apply styling according to ui-ux-pro-max recommendations

### Phase 4: Preview
1. Start dev server: `npm run dev`
2. Use `preview_url` to open the page for user review
3. Iterate based on user feedback

### Phase 5: Testing (Only When Requested)
If user explicitly requests testing or debugging:
1. Use `agent-browser` to automate testing
2. Take screenshots for analysis
3. Verify responsive behavior at different viewports

---

## Critical Rules

### Icons
- NEVER use emojis as UI icons
- ALWAYS use lucide-icons or similar SVG icon libraries
- Maintain consistent icon sizing (24x24 default)

### Design Consistency
- ALWAYS generate a design system before implementing UI
- Follow the color palette, typography, and spacing from the design system
- Check both light and dark mode compatibility

### Preview vs Testing
- ALWAYS use `preview_url` to show completed work to user
- ONLY use `agent-browser` when user explicitly asks for testing or debugging help
- Do NOT automatically run browser automation after every change

### Code Quality
- Use TypeScript for type safety
- Follow React best practices
- Leverage shadcn/ui components instead of building from scratch

---

## User Request Below

</system_reminder>

## 模块：agent-browser

# Browser Automation with agent-browser

## Quick start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

## Commands

### Navigation

```bash
agent-browser open <url>      # Navigate to URL (aliases: goto, navigate)
                              # Supports: https://, http://, file://, about:, data://
                              # Auto-prepends https:// if no protocol given
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser (aliases: quit, exit)
agent-browser connect 9222    # Connect to browser via CDP port
```

### Snapshot (page analysis)

```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### Interactions (use @refs from snapshot)

```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser focus @e1           # Focus element
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key (alias: key)
agent-browser press Control+a     # Key combination
agent-browser keydown Shift       # Hold key down
agent-browser keyup Shift         # Release key
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown option
agent-browser select @e1 "a" "b"  # Select multiple options
agent-browser scroll down 500     # Scroll page (default: down 300px)
agent-browser scrollintoview @e1  # Scroll element into view (alias: scrollinto)
agent-browser drag @e1 @e2        # Drag and drop
agent-browser upload @e1 file.pdf # Upload files
```

### Get information

```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get count ".item"   # Count matching elements
agent-browser get box @e1         # Get bounding box
agent-browser get styles @e1      # Get computed styles (font, color, bg, etc.)
```

### Check state

```bash
agent-browser is visible @e1      # Check if visible
agent-browser is enabled @e1      # Check if enabled
agent-browser is checked @e1      # Check if checked
```

### Screenshots & PDF

```bash
agent-browser screenshot          # Save to a temporary directory
agent-browser screenshot path.png # Save to a specific path
agent-browser screenshot --full   # Full page
agent-browser pdf output.pdf      # Save as PDF
```

### Video recording

```bash
agent-browser record start ./demo.webm    # Start recording (uses current URL + state)
agent-browser click @e1                   # Perform actions
agent-browser record stop                 # Stop and save video
agent-browser record restart ./take2.webm # Stop current + start new recording
```

Recording creates a fresh context but preserves cookies/storage from your session. If no URL is provided, it
automatically returns to your current page. For smooth demos, explore first, then start recording.

### Wait

```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text (or -t)
agent-browser wait --url "**/dashboard"    # Wait for URL pattern (or -u)
agent-browser wait --load networkidle      # Wait for network idle (or -l)
agent-browser wait --fn "window.ready"     # Wait for JS condition (or -f)
```

### Mouse control

```bash
agent-browser mouse move 100 200      # Move mouse
agent-browser mouse down left         # Press button
agent-browser mouse up left           # Release button
agent-browser mouse wheel 100         # Scroll wheel
```

### Semantic locators (alternative to refs)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find text "Sign In" click --exact      # Exact match only
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" type "query"
agent-browser find alt "Logo" click
agent-browser find title "Close" click
agent-browser find testid "submit-btn" click
agent-browser find first ".item" click
agent-browser find last ".item" click
agent-browser find nth 2 "a" hover
```

### Browser settings

```bash
agent-browser set viewport 1920 1080          # Set viewport size
agent-browser set device "iPhone 14"          # Emulate device
agent-browser set geo 37.7749 -122.4194       # Set geolocation (alias: geolocation)
agent-browser set offline on                  # Toggle offline mode
agent-browser set headers '{"X-Key":"v"}'     # Extra HTTP headers
agent-browser set credentials user pass       # HTTP basic auth (alias: auth)
agent-browser set media dark                  # Emulate color scheme
agent-browser set media light reduced-motion  # Light mode + reduced motion
```

### Cookies & Storage

```bash
agent-browser cookies                     # Get all cookies
agent-browser cookies set name value      # Set cookie
agent-browser cookies clear               # Clear cookies
agent-browser storage local               # Get all localStorage
agent-browser storage local key           # Get specific key
agent-browser storage local set k v       # Set value
agent-browser storage local clear         # Clear all
```

### Network

```bash
agent-browser network route <url>              # Intercept requests
agent-browser network route <url> --abort      # Block requests
agent-browser network route <url> --body '{}'  # Mock response
agent-browser network unroute [url]            # Remove routes
agent-browser network requests                 # View tracked requests
agent-browser network requests --filter api    # Filter requests
```

### Tabs & Windows

```bash
agent-browser tab                 # List tabs
agent-browser tab new [url]       # New tab
agent-browser tab 2               # Switch to tab by index
agent-browser tab close           # Close current tab
agent-browser tab close 2         # Close tab by index
agent-browser window new          # New window
```

### Frames

```bash
agent-browser frame "#iframe"     # Switch to iframe
agent-browser frame main          # Back to main frame
```

### Dialogs

```bash
agent-browser dialog accept [text]  # Accept dialog
agent-browser dialog dismiss        # Dismiss dialog
```

### JavaScript

```bash
agent-browser eval "document.title"   # Run JavaScript
```

## Global options

```bash
agent-browser --session <name> ...    # Isolated browser session
agent-browser --json ...              # JSON output for parsing
agent-browser --headed ...            # Show browser window (not headless)
agent-browser --full ...              # Full page screenshot (-f)
agent-browser --cdp <port> ...        # Connect via Chrome DevTools Protocol
agent-browser -p <provider> ...       # Cloud browser provider (--provider)
agent-browser --proxy <url> ...       # Use proxy server
agent-browser --headers <json> ...    # HTTP headers scoped to URL's origin
agent-browser --executable-path <p>   # Custom browser executable
agent-browser --extension <path> ...  # Load browser extension (repeatable)
agent-browser --help                  # Show help (-h)
agent-browser --version               # Show version (-V)
agent-browser <command> --help        # Show detailed help for a command
```

### Proxy support

```bash
agent-browser --proxy http://proxy.com:8080 open example.com
agent-browser --proxy http://user:pass@proxy.com:8080 open example.com
agent-browser --proxy socks5://proxy.com:1080 open example.com
```

## Environment variables

```bash
AGENT_BROWSER_SESSION="mysession"            # Default session name
AGENT_BROWSER_EXECUTABLE_PATH="/path/chrome" # Custom browser path
AGENT_BROWSER_EXTENSIONS="/ext1,/ext2"       # Comma-separated extension paths
AGENT_BROWSER_PROVIDER="your-cloud-browser-provider"  # Cloud browser provider (select browseruse or browserbase)
AGENT_BROWSER_STREAM_PORT="9223"             # WebSocket streaming port
AGENT_BROWSER_HOME="/path/to/agent-browser"  # Custom install location (for daemon.js)
```

## Example: Form submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output shows: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Example: Authentication with saved state

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Sessions (parallel browsers)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

## JSON output (for parsing)

Add `--json` for machine-readable output:

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Debugging

```bash
agent-browser --headed open example.com   # Show browser window
agent-browser --cdp 9222 snapshot         # Connect via CDP port
agent-browser connect 9222                # Alternative: connect command
agent-browser console                     # View console messages
agent-browser console --clear             # Clear console
agent-browser errors                      # View page errors
agent-browser errors --clear              # Clear errors
agent-browser highlight @e1               # Highlight element
agent-browser trace start                 # Start recording trace
agent-browser trace stop trace.zip        # Stop and save trace
agent-browser record start ./debug.webm   # Record video from current page
agent-browser record stop                 # Save recording
```

## Deep-dive documentation

For detailed patterns and best practices, see:

| Reference | Description |
|-----------|-------------|
| [references/snapshot-refs.md](references/snapshot-refs.md) | Ref lifecycle, invalidation rules, troubleshooting |
| [references/session-management.md](references/session-management.md) | Parallel sessions, state persistence, concurrent scraping |
| [references/authentication.md](references/authentication.md) | Login flows, OAuth, 2FA handling, state reuse |
| [references/video-recording.md](references/video-recording.md) | Recording workflows for debugging and documentation |
| [references/proxy-support.md](references/proxy-support.md) | Proxy configuration, geo-testing, rotating proxies |

## Ready-to-use templates

Executable workflow scripts for common patterns:

| Template | Description |
|----------|-------------|
| [templates/form-automation.sh](templates/form-automation.sh) | Form filling with validation |
| [templates/authenticated-session.sh](templates/authenticated-session.sh) | Login once, reuse state |
| [templates/capture-workflow.sh](templates/capture-workflow.sh) | Content extraction with screenshots |

Usage:
```bash
./templates/form-automation.sh https://example.com/form
./templates/authenticated-session.sh https://app.example.com/login
./templates/capture-workflow.sh https://example.com ./output
```

## HTTPS Certificate Errors

For sites with self-signed or invalid certificates:
```bash
agent-browser open https://localhost:8443 --ignore-https-errors
```

## 模块：lucide-icons

# Lucide Icons Skill

Search, download, and customize Lucide icons - a beautiful & consistent icon library with 1000+ icons.

## Features

- Search icons by name or keyword with fuzzy matching
- Download icons as SVG files
- Generate TypeScript React components with full type safety
- Customize icons (color, size, stroke width)
- Metadata caching for fast searches
- Works offline with local cache (optional lucide-static package)
- Multiple data sources with automatic fallback

## Quick Start

```bash
# Search for icons
lucide search heart

# Download an icon
lucide download heart --output ./icons/

# Download with React component
lucide download heart --output ./icons/ --format svg,react

# Customize icon
lucide download star --color "#ffd700" --size 32 --stroke-width 1.5
```

## Installation

Before first use, install dependencies in the skill's scripts directory:

```bash
cd scripts && npm install
```

**Optional - For offline support:**
```bash
npm install lucide-static
```

## Commands

### search `<keyword>`
Search for icons by name or keyword.

```bash
lucide search heart --limit 10
```

### download `<icon-name>`
Download a single icon with optional customization.

Options:
- `-o, --output <dir>` - Output directory (default: current directory)
- `-f, --format <formats>` - Output formats: `svg`, `react`, or `svg,react` (default: `svg`)
- `-c, --color <color>` - Icon color (default: `currentColor`)
- `-s, --size <size>` - Icon size in pixels (default: `24`)
- `-w, --stroke-width <width>` - Stroke width (default: `2`)
- `--overwrite` - Overwrite existing files
- `--json` - Output as JSON

Examples:
```bash
# Basic download
lucide download heart --output ./icons/

# With React component
lucide download heart --format svg,react --output ./src/icons/

# Customized icon
lucide download star --color "#ffd700" --size 32 --stroke-width 1.5

# Overwrite existing
lucide download check --output ./icons/ --overwrite
```

### list
List all available icons.

```bash
lucide list --limit 50
```

### info `<icon-name>`
Show detailed information about an icon.

```bash
lucide info heart
```

### refresh
Refresh the icon metadata cache.

```bash
lucide refresh
```

## Installation

Before first use, install dependencies:

```bash
cd ~/.codebuddy/skills/lucide-icons/scripts && npm install
```

## Output Formats

### SVG
Standard SVG file with Lucide's default styling:
- 24x24 viewBox
- Stroke-based icons
- `currentColor` for easy CSS styling
- Customizable color, size, and stroke-width

Example output (`heart.svg`):
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
</svg>
```

### React (TypeScript)
Generates a fully-typed React functional component with:
- TypeScript interfaces for props
- Customizable size, color, strokeWidth
- className and style support
- Accessibility props (aria-label)
- onClick handler support
- Full type safety

Example output (`HeartIcon.tsx`):
```tsx
import React from 'react';

export interface HeartIconProps {
  size?: number | string;
  color?: string;
  strokeWidth?: number | string;
  className?: string;
  style?: React.CSSProperties;
  'aria-label'?: string;
  onClick?: React.MouseEventHandler<SVGSVGElement>;
}

export const HeartIcon: React.FC<HeartIconProps> = ({
  size = 24,
  color = 'currentColor',
  strokeWidth = 2,
  className,
  style,
  'aria-label': ariaLabel,
  onClick,
  ...props
}) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      style={style}
      aria-label={ariaLabel}
      onClick={onClick}
      role={ariaLabel ? 'img' : undefined}
      aria-hidden={!ariaLabel}
      {...props}
    >
      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
    </svg>
  );
};

HeartIcon.displayName = 'HeartIcon';
export default HeartIcon;
```

## Examples

```bash
# Download heart icon to src/icons/
lucide download heart -o ./src/icons/

# Download with custom color and size
lucide download star --color "#ffd700" --size 32 -o ./icons/

# Generate both SVG and React component
lucide download check-circle --format svg,react -o ./src/components/icons/

# Search for arrow icons
lucide search arrow --limit 20
```

## Customization Options

### Color
Any valid CSS color value:
- Named colors: `red`, `blue`, `green`
- Hex: `#ff0000`, `#f00`
- RGB: `rgb(255, 0, 0)`
- HSL: `hsl(0, 100%, 50%)`
- CSS variables: `var(--primary-color)`
- Default: `currentColor` (inherits from parent)

### Size
Any number (interpreted as pixels):
- `24` (default)
- `16`, `20`, `32`, `48`, etc.

### Stroke Width
Any number:
- `2` (default)
- `1`, `1.5`, `2.5`, `3`, etc.

## Data Sources

The skill uses multiple data sources in order of preference:

1. **lucide-static** (npm package) - Fastest, works offline
2. **GitHub Raw Content** - No rate limiting, no authentication needed
3. **GitHub API** - Fallback for icon listing

## Caching

- Icon metadata is cached in the skill's `cache/` directory
- Cache TTL: 24 hours
- Use `lucide refresh` to force cache update
- Works offline with cached data

## Error Handling

The skill handles common errors gracefully:

- **Icon not found**: Suggests similar icons
- **File exists**: Prompts to use `--overwrite`
- **Permission denied**: Shows clear error message
- **Network errors**: Falls back to cached data or local package

## Troubleshooting

### "Cannot find module" errors
Make sure dependencies are installed:
```bash
cd scripts && npm install
```

### Rate limiting from GitHub
Install `lucide-static` for local icon access:
```bash
npm install lucide-static
```

### Outdated icon list
Refresh the cache:
```bash
lucide refresh
```

## Data Source

Icons are fetched from the official [Lucide repository](https://github.com/lucide-icons/lucide).

## More Information

See [README.md](./README.md) for detailed documentation.

## 模块：modern-web-app

# modern-web-app

Stack: React + TypeScript + Vite + Tailwind CSS + shadcn/ui

## Workflow

1. `scripts/init-webapp.sh <website-title> [output-dir]` - Initialize project
2. Edit source code in `src/`
3. Build the React app
4. Deploy the build output in `dist/`

## Quick Start

### 1. Initialize

```bash
# Init project in ./app (default) with website title
bash scripts/init-webapp.sh "My Website"

# Or specify custom output directory
bash scripts/init-webapp.sh "My Website" ./my-project

cd ./app  # or your custom directory
```

**AI Agent Notes**:
- Default project path is `./app` (relative to current working directory)
- Second argument allows custom output directory
- Non-interactive execution with auto-confirm

This creates a fully configured project with:

- React + TypeScript (via Vite)
- Tailwind CSS 3.4.19 with shadcn/ui theming system
- Path aliases (`@/`) configured
- 40+ shadcn/ui components pre-installed
- All Radix UI dependencies included
- Production build optimization with Vite
- Node 20+ compatibility (auto-detects and pins Vite version)

### 2. Develop

Edit generated files in `src/`:
- Page sections: `src/sections/`
- Custom React hooks: `src/hooks/`
- TypeScript definitions: `src/types/`

### 3. Build

```bash
cd ./app && npm run build 2>&1
```

**Output** (`dist/`):
- `index.html` - Entry point
- `assets/index-[hash].js` - Bundled JS
- `assets/index-[hash].css` - Bundled CSS
- Optimized images, fonts, other assets

**Optimizations**: Tree-shaking, code splitting, asset compression, minification, cache-busting hashes.

### 4. Deploy

Deploy the build output in `<project-dir>/dist/`

## Debugging

1. Fix source files
2. `npm run build`
3. Test `dist/`
4. Redeploy

## Reference

- [shadcn/ui Components](https://ui.shadcn.com/docs/components)

## 模块：ui-ux-pro-max

# ui-ux-pro-max

Comprehensive design guide for web and mobile applications. Contains 67 styles, 96 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 13 technology stacks. Searchable database with priority-based recommendations.

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## How to Use This Skill

When user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Generate Design System (REQUIRED)

**Always start with `--design-system`** to get comprehensive recommendations with reasoning:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This command:
1. Searches 5 domains in parallel (product, style, color, landing, typography)
2. Applies reasoning rules from `ui-reasoning.csv` to select best matches
3. Returns complete design system: pattern, style, colors, typography, effects
4. Includes anti-patterns to avoid

**Example:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System (Master + Overrides Pattern)

To save the design system for hierarchical retrieval across sessions, add `--persist`:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

This creates:
- `design-system/MASTER.md` — Global Source of Truth with all design rules
- `design-system/pages/` — Folder for page-specific overrides

**With page-specific override:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

This also creates:
- `design-system/pages/dashboard.md` — Page-specific deviations from Master

**How hierarchical retrieval works:**
1. When building a specific page (e.g., "Checkout"), first check `design-system/pages/checkout.md`
2. If the page file exists, its rules **override** the Master file
3. If not, use `design-system/MASTER.md` exclusively

### Step 3: Supplement with Detailed Searches (as needed)

After getting the design system, use domain searches to get additional details:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**When to use detailed searches:**

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

### Step 4: Stack Guidelines (Default: html-tailwind)

Get implementation-specific best practices. If user doesn't specify a stack, **default to `html-tailwind`**.

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Web interface guidelines | aria, focus, keyboard, semantic, virtualize |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Available Stacks

| Stack | Focus |
|-------|-------|
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | shadcn/ui components, theming, forms, patterns |
| `jetpack-compose` | Composables, Modifiers, State Hoisting, Recomposition |

---

## Example Workflow

**User request:** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp"

### Step 1: Analyze Requirements
- Product type: Beauty/Spa service
- Style keywords: elegant, professional, soft
- Industry: Beauty/Wellness
- Stack: html-tailwind (default)

### Step 2: Generate Design System (REQUIRED)

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Output:** Complete design system with pattern, style, colors, typography, effects, and anti-patterns.

### Step 3: Supplement with Detailed Searches (as needed)

```bash
# Get UX guidelines for animation and accessibility
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Get alternative typography options if needed
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### Step 4: Stack Guidelines

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Then:** Synthesize design system + detailed searches and implement the design.

---

## Output Formats

The `--design-system` flag supports two output formats:

```bash
# ASCII box (default) - best for terminal display
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - best for documentation
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## Tips for Better Results

1. **Be specific with keywords** - "healthcare SaaS dashboard" > "app"
2. **Search multiple times** - Different keywords reveal different insights
3. **Combine domains** - Style + Typography + Color = Complete design system
4. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues
5. **Use stack flag** - Get implementation-specific best practices
6. **Iterate** - If first search doesn't match, try different keywords

---

## Common Rules for Professional UI

These are frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule | Do | Don't |
|------|----|----- |
| **No emoji icons** | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis like 🎨 🚀 ⚙️ as UI icons |
| **Stable hover states** | Use color/opacity transitions on hover | Use scale transforms that shift layout |
| **Correct brand logos** | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes randomly |

### Interaction & Cursor

| Rule | Do | Don't |
|------|----|----- |
| **Cursor pointer** | Add `cursor-pointer` to all clickable/hoverable cards | Leave default cursor on interactive elements |
| **Hover feedback** | Provide visual feedback (color, shadow, border) | No indication element is interactive |
| **Smooth transitions** | Use `transition-colors duration-200` | Instant state changes or too slow (>500ms) |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----- |
| **Glass card light mode** | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent) |
| **Text contrast light** | Use `#0F172A` (slate-900) for text | Use `#94A3B8` (slate-400) for body text |
| **Muted text light** | Use `#475569` (slate-600) minimum | Use gray-400 or lighter |
| **Border visibility** | Use `border-gray-200` in light mode | Use `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Don't |
|------|----|----- |
| **Floating navbar** | Add `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| **Content padding** | Account for fixed navbar height | Let content hide behind fixed elements |
| **Consistent max-width** | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

---

## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Use theme colors directly (bg-primary) not var() wrapper

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery

### Layout
- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
