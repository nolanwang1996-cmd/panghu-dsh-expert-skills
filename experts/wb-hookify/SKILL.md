---
name: wb-hookify
description: 分析对话/工作流中的重复模式，设计自动化钩子把重复操作固化为自动流程。
---
# 会话分析与钩子设计专家
> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。

## 成员角色：conversation-analyzer

You are a conversation analysis specialist that identifies problematic behaviors in CodeBuddy Code sessions that could be prevented with hooks.

**Your Core Responsibilities:**
1. Read and analyze user messages to find frustration signals
2. Identify specific tool usage patterns that caused issues
3. Extract actionable patterns that can be matched with regex
4. Categorize issues by severity and type
5. Provide structured findings for hook rule generation

**Analysis Process:**

### 1. Search for User Messages Indicating Issues

Read through user messages in reverse chronological order (most recent first). Look for:

**Explicit correction requests:**
- "Don't use X"
- "Stop doing Y"
- "Please don't Z"
- "Avoid..."
- "Never..."

**Frustrated reactions:**
- "Why did you do X?"
- "I didn't ask for that"
- "That's not what I meant"
- "That was wrong"

**Corrections and reversions:**
- User reverting changes CodeBuddy made
- User fixing issues CodeBuddy created
- User providing step-by-step corrections

**Repeated issues:**
- Same type of mistake multiple times
- User having to remind multiple times
- Pattern of similar problems

### 2. Identify Tool Usage Patterns

For each issue, determine:
- **Which tool**: Bash, Edit, Write, MultiEdit
- **What action**: Specific command or code pattern
- **When it happened**: During what task/phase
- **Why problematic**: User's stated reason or implicit concern

**Extract concrete examples:**
- For Bash: Actual command that was problematic
- For Edit/Write: Code pattern that was added
- For Stop: What was missing before stopping

### 3. Create Regex Patterns

Convert behaviors into matchable patterns:

**Bash command patterns:**
- `rm\s+-rf` for dangerous deletes
- `sudo\s+` for privilege escalation
- `chmod\s+777` for permission issues

**Code patterns (Edit/Write):**
- `console\.log\(` for debug logging
- `eval\(|new Function\(` for dangerous eval
- `innerHTML\s*=` for XSS risks

**File path patterns:**
- `\.env$` for environment files
- `/node_modules/` for dependency files
- `dist/|build/` for generated files

### 4. Categorize Severity

**High severity (should block in future):**
- Dangerous commands (rm -rf, chmod 777)
- Security issues (hardcoded secrets, eval)
- Data loss risks

**Medium severity (warn):**
- Style violations (console.log in production)
- Wrong file types (editing generated files)
- Missing best practices

**Low severity (optional):**
- Preferences (coding style)
- Non-critical patterns

### 5. Output Format

Return your findings as structured text in this format:

```
## Hookify Analysis Results

### Issue 1: Dangerous rm Commands
**Severity**: High
**Tool**: Bash
**Pattern**: `rm\s+-rf`
**Occurrences**: 3 times
**Context**: Used rm -rf on /tmp directories without verification
**User Reaction**: "Please be more careful with rm commands"

**Suggested Rule:**
- Name: warn-dangerous-rm
- Event: bash
- Pattern: rm\s+-rf
- Message: "Dangerous rm command detected. Verify path before proceeding."

---

### Issue 2: Console.log in TypeScript
**Severity**: Medium
**Tool**: Edit/Write
**Pattern**: `console\.log\(`
**Occurrences**: 2 times
**Context**: Added console.log statements to production TypeScript files
**User Reaction**: "Don't use console.log in production code"

**Suggested Rule:**
- Name: warn-console-log
- Event: file
- Pattern: console\.log\(
- Message: "Console.log detected. Use proper logging library instead."

---

[Continue for each issue found...]

## Summary

Found {N} behaviors worth preventing:
- {N} high severity
- {N} medium severity
- {N} low severity

Recommend creating rules for high and medium severity issues.
```

**Quality Standards:**
- Be specific about patterns (don't be overly broad)
- Include actual examples from conversation
- Explain why each issue matters
- Provide ready-to-use regex patterns
- Don't false-positive on discussions about what NOT to do

**Edge Cases:**

**User discussing hypotheticals:**
- "What would happen if I used rm -rf?"
- Don't treat as problematic behavior

**Teaching moments:**
- "Here's what you shouldn't do: ..."
- Context indicates explanation, not actual problem

**One-time accidents:**
- Single occurrence, already fixed
- Mention but mark as low priority

**Subjective preferences:**
- "I prefer X over Y"
- Mark as low severity, let user decide

**Return Results:**
Provide your analysis in the structured format above. The /hookify command will use this to:
1. Present findings to user
2. Ask which rules to create
3. Generate .local.md configuration files
4. Save rules to .codebuddy directory

## 模块：writing-rules

# Writing Hookify Rules

## Overview

Hookify rules are markdown files with YAML frontmatter that define patterns to watch for and messages to show when those patterns match. Rules are stored in `.codebuddy/hookify.{rule-name}.local.md` files.

## Rule File Format

### Basic Structure

```markdown
---
name: rule-identifier
enabled: true
event: bash|file|stop|prompt|all
pattern: regex-pattern-here
---

Message to show CodeBuddy when this rule triggers.
Can include markdown formatting, warnings, suggestions, etc.
```

### Frontmatter Fields

**name** (required): Unique identifier for the rule
- Use kebab-case: `warn-dangerous-rm`, `block-console-log`
- Be descriptive and action-oriented
- Start with verb: warn, prevent, block, require, check

**enabled** (required): Boolean to activate/deactivate
- `true`: Rule is active
- `false`: Rule is disabled (won't trigger)
- Can toggle without deleting rule

**event** (required): Which hook event to trigger on
- `bash`: Bash tool commands
- `file`: Edit, Write, MultiEdit tools
- `stop`: When agent wants to stop
- `prompt`: When user submits a prompt
- `all`: All events

**action** (optional): What to do when rule matches
- `warn`: Show message but allow operation (default)
- `block`: Prevent operation (PreToolUse) or stop session (Stop events)
- If omitted, defaults to `warn`

**pattern** (simple format): Regex pattern to match
- Used for simple single-condition rules
- Matches against command (bash) or new_text (file)
- Python regex syntax

**Example:**
```yaml
event: bash
pattern: rm\s+-rf
```

### Advanced Format (Multiple Conditions)

For complex rules with multiple conditions:

```markdown
---
name: warn-env-file-edits
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$
  - field: new_text
    operator: contains
    pattern: API_KEY
---

You're adding an API key to a .env file. Ensure this file is in .gitignore!
```

**Condition fields:**
- `field`: Which field to check
  - For bash: `command`
  - For file: `file_path`, `new_text`, `old_text`, `content`
- `operator`: How to match
  - `regex_match`: Regex pattern matching
  - `contains`: Substring check
  - `equals`: Exact match
  - `not_contains`: Substring must NOT be present
  - `starts_with`: Prefix check
  - `ends_with`: Suffix check
- `pattern`: Pattern or string to match

**All conditions must match for rule to trigger.**

## Message Body

The markdown content after frontmatter is shown to CodeBuddy when the rule triggers.

**Good messages:**
- Explain what was detected
- Explain why it's problematic
- Suggest alternatives or best practices
- Use formatting for clarity (bold, lists, etc.)

**Example:**
```markdown
⚠️ **Console.log detected!**

You're adding console.log to production code.

**Why this matters:**
- Debug logs shouldn't ship to production
- Console.log can expose sensitive data
- Impacts browser performance

**Alternatives:**
- Use a proper logging library
- Remove before committing
- Use conditional debug builds
```

## Event Type Guide

### bash Events

Match Bash command patterns:

```markdown
---
event: bash
pattern: sudo\s+|rm\s+-rf|chmod\s+777
---

Dangerous command detected!
```

**Common patterns:**
- Dangerous commands: `rm\s+-rf`, `dd\s+if=`, `mkfs`
- Privilege escalation: `sudo\s+`, `su\s+`
- Permission issues: `chmod\s+777`, `chown\s+root`

### file Events

Match Edit/Write/MultiEdit operations:

```markdown
---
event: file
pattern: console\.log\(|eval\(|innerHTML\s*=
---

Potentially problematic code pattern detected!
```

**Match on different fields:**
```markdown
---
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.tsx?$
  - field: new_text
    operator: regex_match
    pattern: console\.log\(
---

Console.log in TypeScript file!
```

**Common patterns:**
- Debug code: `console\.log\(`, `debugger`, `print\(`
- Security risks: `eval\(`, `innerHTML\s*=`, `dangerouslySetInnerHTML`
- Sensitive files: `\.env$`, `credentials`, `\.pem$`
- Generated files: `node_modules/`, `dist/`, `build/`

### stop Events

Match when agent wants to stop (completion checks):

```markdown
---
event: stop
pattern: .*
---

Before stopping, verify:
- [ ] Tests were run
- [ ] Build succeeded
- [ ] Documentation updated
```

**Use for:**
- Reminders about required steps
- Completion checklists
- Process enforcement

### prompt Events

Match user prompt content (advanced):

```markdown
---
event: prompt
conditions:
  - field: user_prompt
    operator: contains
    pattern: deploy to production
---

Production deployment checklist:
- [ ] Tests passing?
- [ ] Reviewed by team?
- [ ] Monitoring ready?
```

## Pattern Writing Tips

### Regex Basics

**Literal characters:** Most characters match themselves
- `rm` matches "rm"
- `console.log` matches "console.log"

**Special characters need escaping:**
- `.` (any char) → `\.` (literal dot)
- `(` `)` → `\(` `\)` (literal parens)
- `[` `]` → `\[` `\]` (literal brackets)

**Common metacharacters:**
- `\s` - whitespace (space, tab, newline)
- `\d` - digit (0-9)
- `\w` - word character (a-z, A-Z, 0-9, _)
- `.` - any character
- `+` - one or more
- `*` - zero or more
- `?` - zero or one
- `|` - OR

**Examples:**
```
rm\s+-rf         Matches: rm -rf, rm  -rf
console\.log\(   Matches: console.log(
(eval|exec)\(    Matches: eval( or exec(
chmod\s+777      Matches: chmod 777, chmod  777
API_KEY\s*=      Matches: API_KEY=, API_KEY =
```

### Testing Patterns

Test regex patterns before using:

```bash
python3 -c "import re; print(re.search(r'your_pattern', 'test text'))"
```

Or use online regex testers (regex101.com with Python flavor).

### Common Pitfalls

**Too broad:**
```yaml
pattern: log    # Matches "log", "login", "dialog", "catalog"
```
Better: `console\.log\(|logger\.`

**Too specific:**
```yaml
pattern: rm -rf /tmp  # Only matches exact path
```
Better: `rm\s+-rf`

**Escaping issues:**
- YAML quoted strings: `"pattern"` requires double backslashes `\\s`
- YAML unquoted: `pattern: \s` works as-is
- **Recommendation**: Use unquoted patterns in YAML

## File Organization

**Location:** All rules in `.codebuddy/` directory
**Naming:** `.codebuddy/hookify.{descriptive-name}.local.md`
**Gitignore:** Add `.codebuddy/*.local.md` to `.gitignore`

**Good names:**
- `hookify.dangerous-rm.local.md`
- `hookify.console-log.local.md`
- `hookify.require-tests.local.md`
- `hookify.sensitive-files.local.md`

**Bad names:**
- `hookify.rule1.local.md` (not descriptive)
- `hookify.md` (missing .local)
- `danger.local.md` (missing hookify prefix)

## Workflow

### Creating a Rule

1. Identify unwanted behavior
2. Determine which tool is involved (Bash, Edit, etc.)
3. Choose event type (bash, file, stop, etc.)
4. Write regex pattern
5. Create `.codebuddy/hookify.{name}.local.md` file in project root
6. Test immediately - rules are read dynamically on next tool use

### Refining a Rule

1. Edit the `.local.md` file
2. Adjust pattern or message
3. Test immediately - changes take effect on next tool use

### Disabling a Rule

**Temporary:** Set `enabled: false` in frontmatter
**Permanent:** Delete the `.local.md` file

## Examples

See `${CODEBUDDY_PLUGIN_ROOT}/examples/` for complete examples:
- `dangerous-rm.local.md` - Block dangerous rm commands
- `console-log-warning.local.md` - Warn about console.log
- `sensitive-files-warning.local.md` - Warn about editing .env files

## Quick Reference

**Minimum viable rule:**
```markdown
---
name: my-rule
enabled: true
event: bash
pattern: dangerous_command
---

Warning message here
```

**Rule with conditions:**
```markdown
---
name: my-rule
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.ts$
  - field: new_text
    operator: contains
    pattern: any
---

Warning message
```

**Event types:**
- `bash` - Bash commands
- `file` - File edits
- `stop` - Completion checks
- `prompt` - User input
- `all` - All events

**Field options:**
- Bash: `command`
- File: `file_path`, `new_text`, `old_text`, `content`
- Prompt: `user_prompt`

**Operators:**
- `regex_match`, `contains`, `equals`, `not_contains`, `starts_with`, `ends_with`

## 操作指引：configure

# Configure Hookify Rules

**Load hookify:writing-rules skill first** to understand rule format.

Enable or disable existing hookify rules using an interactive interface.

## Steps

### 1. Find Existing Rules

Use Glob tool to find all hookify rule files:
```
pattern: ".codebuddy/hookify.*.local.md"
```

If no rules found, inform user:
```
No hookify rules configured yet. Use `/hookify` to create your first rule.
```

### 2. Read Current State

For each rule file:
- Read the file
- Extract `name` and `enabled` fields from frontmatter
- Build list of rules with current state

### 3. Ask User Which Rules to Toggle

Use AskUserQuestion to let user select rules:

```json
{
  "questions": [
    {
      "question": "Which rules would you like to enable or disable?",
      "header": "Configure",
      "multiSelect": true,
      "options": [
        {
          "label": "warn-dangerous-rm (currently enabled)",
          "description": "Warns about rm -rf commands"
        },
        {
          "label": "warn-console-log (currently disabled)",
          "description": "Warns about console.log in code"
        },
        {
          "label": "require-tests (currently enabled)",
          "description": "Requires tests before stopping"
        }
      ]
    }
  ]
}
```

**Option format:**
- Label: `{rule-name} (currently {enabled|disabled})`
- Description: Brief description from rule's message or pattern

### 4. Parse User Selection

For each selected rule:
- Determine current state from label (enabled/disabled)
- Toggle state: enabled → disabled, disabled → enabled

### 5. Update Rule Files

For each rule to toggle:
- Use Read tool to read current content
- Use Edit tool to change `enabled: true` to `enabled: false` (or vice versa)
- Handle both with and without quotes

**Edit pattern for enabling:**
```
old_string: "enabled: false"
new_string: "enabled: true"
```

**Edit pattern for disabling:**
```
old_string: "enabled: true"
new_string: "enabled: false"
```

### 6. Confirm Changes

Show user what was changed:

```
## Hookify Rules Updated

**Enabled:**
- warn-console-log

**Disabled:**
- warn-dangerous-rm

**Unchanged:**
- require-tests

Changes apply immediately - no restart needed
```

## Important Notes

- Changes take effect immediately on next tool use
- You can also manually edit .codebuddy/hookify.*.local.md files
- To permanently remove a rule, delete its .local.md file
- Use `/hookify:list` to see all configured rules

## Edge Cases

**No rules to configure:**
- Show message about using `/hookify` to create rules first

**User selects no rules:**
- Inform that no changes were made

**File read/write errors:**
- Inform user of specific error
- Suggest manual editing as fallback

## 操作指引：help

# Hookify Plugin Help

Explain how the hookify plugin works and how to use it.

## Overview

The hookify plugin makes it easy to create custom hooks that prevent unwanted behaviors. Instead of editing `hooks.json` files, users create simple markdown configuration files that define patterns to watch for.

## How It Works

### 1. Hook System

Hookify installs generic hooks that run on these events:
- **PreToolUse**: Before any tool executes (Bash, Edit, Write, etc.)
- **PostToolUse**: After a tool executes
- **Stop**: When CodeBuddy wants to stop working
- **UserPromptSubmit**: When user submits a prompt

These hooks read configuration files from `.codebuddy/hookify.*.local.md` and check if any rules match the current operation.

### 2. Configuration Files

Users create rules in `.codebuddy/hookify.{rule-name}.local.md` files:

```markdown
---
name: warn-dangerous-rm
enabled: true
event: bash
pattern: rm\s+-rf
---

⚠️ **Dangerous rm command detected!**

This command could delete important files. Please verify the path.
```

**Key fields:**
- `name`: Unique identifier for the rule
- `enabled`: true/false to activate/deactivate
- `event`: bash, file, stop, prompt, or all
- `pattern`: Regex pattern to match

The message body is what CodeBuddy sees when the rule triggers.

### 3. Creating Rules

**Option A: Use /hookify command**
```
/hookify Don't use console.log in production files
```

This analyzes your request and creates the appropriate rule file.

**Option B: Create manually**
Create `.codebuddy/hookify.my-rule.local.md` with the format above.

**Option C: Analyze conversation**
```
/hookify
```

Without arguments, hookify analyzes recent conversation to find behaviors you want to prevent.

## Available Commands

- **`/hookify`** - Create hooks from conversation analysis or explicit instructions
- **`/hookify:help`** - Show this help (what you're reading now)
- **`/hookify:list`** - List all configured hooks
- **`/hookify:configure`** - Enable/disable existing hooks interactively

## Example Use Cases

**Prevent dangerous commands:**
```markdown
---
name: block-chmod-777
enabled: true
event: bash
pattern: chmod\s+777
---

Don't use chmod 777 - it's a security risk. Use specific permissions instead.
```

**Warn about debugging code:**
```markdown
---
name: warn-console-log
enabled: true
event: file
pattern: console\.log\(
---

Console.log detected. Remember to remove debug logging before committing.
```

**Require tests before stopping:**
```markdown
---
name: require-tests
enabled: true
event: stop
pattern: .*
---

Did you run tests before finishing? Make sure `npm test` or equivalent was executed.
```

## Pattern Syntax

Use Python regex syntax:
- `\s` - whitespace
- `\.` - literal dot
- `|` - OR
- `+` - one or more
- `*` - zero or more
- `\d` - digit
- `[abc]` - character class

**Examples:**
- `rm\s+-rf` - matches "rm -rf"
- `console\.log\(` - matches "console.log("
- `(eval|exec)\(` - matches "eval(" or "exec("
- `\.env$` - matches files ending in .env

## Important Notes

**No Restart Needed**: Hookify rules (`.local.md` files) take effect immediately on the next tool use. The hookify hooks are already loaded and read your rules dynamically.

**Block or Warn**: Rules can either `block` operations (prevent execution) or `warn` (show message but allow). Set `action: block` or `action: warn` in the rule's frontmatter.

**Rule Files**: Keep rules in `.codebuddy/hookify.*.local.md` - they should be git-ignored (add to .gitignore if needed).

**Disable Rules**: Set `enabled: false` in frontmatter or delete the file.

## Troubleshooting

**Hook not triggering:**
- Check rule file is in `.codebuddy/` directory
- Verify `enabled: true` in frontmatter
- Confirm pattern is valid regex
- Test pattern: `python3 -c "import re; print(re.search('your_pattern', 'test_text'))"`
- Rules take effect immediately - no restart needed

**Import errors:**
- Check Python 3 is available: `python3 --version`
- Verify hookify plugin is installed correctly

**Pattern not matching:**
- Test regex separately
- Check for escaping issues (use unquoted patterns in YAML)
- Try simpler pattern first, then refine

## Getting Started

1. Create your first rule:
   ```
   /hookify Warn me when I try to use rm -rf
   ```

2. Try to trigger it:
   - Ask CodeBuddy to run `rm -rf /tmp/test`
   - You should see the warning

4. Refine the rule by editing `.codebuddy/hookify.warn-rm.local.md`

5. Create more rules as you encounter unwanted behaviors

For more examples, check the `${CODEBUDDY_PLUGIN_ROOT}/examples/` directory.

## 操作指引：hookify

# Hookify - Create Hooks from Unwanted Behaviors

**FIRST: Load the hookify:writing-rules skill** using the Skill tool to understand rule file format and syntax.

Create hook rules to prevent problematic behaviors by analyzing the conversation or from explicit user instructions.

## Your Task

You will help the user create hookify rules to prevent unwanted behaviors. Follow these steps:

### Step 1: Gather Behavior Information

**If $ARGUMENTS is provided:**
- User has given specific instructions: `$ARGUMENTS`
- Still analyze recent conversation (last 10-15 user messages) for additional context
- Look for examples of the behavior happening

**If $ARGUMENTS is empty:**
- Launch the conversation-analyzer agent to find problematic behaviors
- Agent will scan user prompts for frustration signals
- Agent will return structured findings

**To analyze conversation:**
Use the Task tool to launch conversation-analyzer agent:
```
{
  "subagent_type": "general-purpose",
  "description": "Analyze conversation for unwanted behaviors",
  "prompt": "You are analyzing a CodeBuddy Code conversation to find behaviors the user wants to prevent.

Read user messages in the current conversation and identify:
1. Explicit requests to avoid something (\"don't do X\", \"stop doing Y\")
2. Corrections or reversions (user fixing CodeBuddy's actions)
3. Frustrated reactions (\"why did you do X?\", \"I didn't ask for that\")
4. Repeated issues (same problem multiple times)

For each issue found, extract:
- What tool was used (Bash, Edit, Write, etc.)
- Specific pattern or command
- Why it was problematic
- User's stated reason

Return findings as a structured list with:
- category: Type of issue
- tool: Which tool was involved
- pattern: Regex or literal pattern to match
- context: What happened
- severity: high/medium/low

Focus on the most recent issues (last 20-30 messages). Don't go back further unless explicitly asked."
}
```

### Step 2: Present Findings to User

After gathering behaviors (from arguments or agent), present to user using AskUserQuestion:

**Question 1: Which behaviors to hookify?**
- Header: "Create Rules"
- multiSelect: true
- Options: List each detected behavior (max 4)
  - Label: Short description (e.g., "Block rm -rf")
  - Description: Why it's problematic

**Question 2: For each selected behavior, ask about action:**
- "Should this block the operation or just warn?"
- Options:
  - "Just warn" (action: warn - shows message but allows)
  - "Block operation" (action: block - prevents execution)

**Question 3: Ask for example patterns:**
- "What patterns should trigger this rule?"
- Show detected patterns
- Allow user to refine or add more

### Step 3: Generate Rule Files

For each confirmed behavior, create a `.codebuddy/hookify.{rule-name}.local.md` file:

**Rule naming convention:**
- Use kebab-case
- Be descriptive: `block-dangerous-rm`, `warn-console-log`, `require-tests-before-stop`
- Start with action verb: block, warn, prevent, require

**File format:**
```markdown
---
name: {rule-name}
enabled: true
event: {bash|file|stop|prompt|all}
pattern: {regex pattern}
action: {warn|block}
---

{Message to show CodeBuddy when rule triggers}
```

**Action values:**
- `warn`: Show message but allow operation (default)
- `block`: Prevent operation or stop session

**For more complex rules (multiple conditions):**
```markdown
---
name: {rule-name}
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$
  - field: new_text
    operator: contains
    pattern: API_KEY
---

{Warning message}
```

### Step 4: Create Files and Confirm

**IMPORTANT**: Rule files must be created in the current working directory's `.codebuddy/` folder, NOT the plugin directory.

Use the current working directory (where CodeBuddy Code was started) as the base path.

1. Check if `.codebuddy/` directory exists in current working directory
   - If not, create it first with: `mkdir -p .codebuddy`

2. Use Write tool to create each `.codebuddy/hookify.{name}.local.md` file
   - Use relative path from current working directory: `.codebuddy/hookify.{name}.local.md`
   - The path should resolve to the project's .codebuddy directory, not the plugin's

3. Show user what was created:
   ```
   Created 3 hookify rules:
   - .codebuddy/hookify.dangerous-rm.local.md
   - .codebuddy/hookify.console-log.local.md
   - .codebuddy/hookify.sensitive-files.local.md

   These rules will trigger on:
   - dangerous-rm: Bash commands matching "rm -rf"
   - console-log: Edits adding console.log statements
   - sensitive-files: Edits to .env or credentials files
   ```

4. Verify files were created in the correct location by listing them

5. Inform user: **"Rules are active immediately - no restart needed!"**

   The hookify hooks are already loaded and will read your new rules on the next tool use.

## Event Types Reference

- **bash**: Matches Bash tool commands
- **file**: Matches Edit, Write, MultiEdit tools
- **stop**: Matches when agent wants to stop (use for completion checks)
- **prompt**: Matches when user submits prompts
- **all**: Matches all events

## Pattern Writing Tips

**Bash patterns:**
- Match dangerous commands: `rm\s+-rf|chmod\s+777|dd\s+if=`
- Match specific tools: `npm\s+install\s+|pip\s+install`

**File patterns:**
- Match code patterns: `console\.log\(|eval\(|innerHTML\s*=`
- Match file paths: `\.env$|\.git/|node_modules/`

**Stop patterns:**
- Check for missing steps: (check transcript or completion criteria)

## Example Workflow

**User says**: "/hookify Don't use rm -rf without asking me first"

**Your response**:
1. Analyze: User wants to prevent rm -rf commands
2. Ask: "Should I block this command or just warn you?"
3. User selects: "Just warn"
4. Create `.codebuddy/hookify.dangerous-rm.local.md`:
   ```markdown
   ---
   name: warn-dangerous-rm
   enabled: true
   event: bash
   pattern: rm\s+-rf
   ---

   ⚠️ **Dangerous rm command detected**

   You requested to be warned before using rm -rf.
   Please verify the path is correct.
   ```
5. Confirm: "Created hookify rule. It's active immediately - try triggering it!"

## Important Notes

- **No restart needed**: Rules take effect immediately on the next tool use
- **File location**: Create files in project's `.codebuddy/` directory (current working directory), NOT the plugin's .codebuddy/
- **Regex syntax**: Use Python regex syntax (raw strings, no need to escape in YAML)
- **Action types**: Rules can `warn` (default) or `block` operations
- **Testing**: Test rules immediately after creating them

## Troubleshooting

**If rule file creation fails:**
1. Check current working directory with pwd
2. Ensure `.codebuddy/` directory exists (create with mkdir if needed)
3. Use absolute path if needed: `{cwd}/.codebuddy/hookify.{name}.local.md`
4. Verify file was created with Glob or ls

**If rule doesn't trigger after creation:**
1. Verify file is in project `.codebuddy/` not plugin `.codebuddy/`
2. Check file with Read tool to ensure pattern is correct
3. Test pattern with: `python3 -c "import re; print(re.search(r'pattern', 'test text'))"`
4. Verify `enabled: true` in frontmatter
5. Remember: Rules work immediately, no restart needed

**If blocking seems too strict:**
1. Change `action: block` to `action: warn` in the rule file
2. Or adjust the pattern to be more specific
3. Changes take effect on next tool use

Use TodoWrite to track your progress through the steps.

## 操作指引：list

# List Hookify Rules

**Load hookify:writing-rules skill first** to understand rule format.

Show all configured hookify rules in the project.

## Steps

1. Use Glob tool to find all hookify rule files:
   ```
   pattern: ".codebuddy/hookify.*.local.md"
   ```

2. For each file found:
   - Use Read tool to read the file
   - Extract frontmatter fields: name, enabled, event, pattern
   - Extract message preview (first 100 chars)

3. Present results in a table:

```
## Configured Hookify Rules

| Name | Enabled | Event | Pattern | File |
|------|---------|-------|---------|------|
| warn-dangerous-rm | ✅ Yes | bash | rm\s+-rf | hookify.dangerous-rm.local.md |
| warn-console-log | ✅ Yes | file | console\.log\( | hookify.console-log.local.md |
| check-tests | ❌ No | stop | .* | hookify.require-tests.local.md |

**Total**: 3 rules (2 enabled, 1 disabled)
```

4. For each rule, show a brief preview:
```
### warn-dangerous-rm
**Event**: bash
**Pattern**: `rm\s+-rf`
**Message**: "⚠️ **Dangerous rm command detected!** This command could delete..."

**Status**: ✅ Active
**File**: .codebuddy/hookify.dangerous-rm.local.md
```

5. Add helpful footer:
```
---

To modify a rule: Edit the .local.md file directly
To disable a rule: Set `enabled: false` in frontmatter
To enable a rule: Set `enabled: true` in frontmatter
To delete a rule: Remove the .local.md file
To create a rule: Use `/hookify` command

**Remember**: Changes take effect immediately - no restart needed
```

## If No Rules Found

If no hookify rules exist:

```
## No Hookify Rules Configured

You haven't created any hookify rules yet.

To get started:
1. Use `/hookify` to analyze conversation and create rules
2. Or manually create `.codebuddy/hookify.my-rule.local.md` files
3. See `/hookify:help` for documentation

Example:
```
/hookify Warn me when I use console.log
```

Check `${CODEBUDDY_PLUGIN_ROOT}/examples/` for example rule files.
```
