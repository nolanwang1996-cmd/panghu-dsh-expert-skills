---
name: wb-ralph-loop
description: 长任务的循环迭代执行方法论：目标拆解、循环推进、验收检查与止损。
---
# 循环迭代执行专家
> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。

## 操作指引：cancel-ralph

# Cancel Ralph

To cancel the Ralph loop:

1. Check if `.codebuddy/ralph-loop.local.md` exists using Bash: `test -f .codebuddy/ralph-loop.local.md && echo "EXISTS" || echo "NOT_FOUND"`

2. **If NOT_FOUND**: Say "No active Ralph loop found."

3. **If EXISTS**:
   - Read `.codebuddy/ralph-loop.local.md` to get the current iteration number from the `iteration:` field
   - Remove the file using Bash: `rm .codebuddy/ralph-loop.local.md`
   - Report: "Cancelled Ralph loop (was at iteration N)" where N is the iteration value

## 操作指引：help

# Ralph Loop Plugin Help

Please explain the following to the user:

## What is Ralph Loop?

Ralph Loop implements the Ralph Wiggum technique - an iterative development methodology based on continuous AI loops, pioneered by Geoffrey Huntley.

**Core concept:**
```bash
while :; do
  cat PROMPT.md | codebuddy --continue
done
```

The same prompt is fed to CodeBuddy repeatedly. The "self-referential" aspect comes from CodeBuddy seeing its own previous work in the files and git history, not from feeding output back as input.

**Each iteration:**
1. CodeBuddy receives the SAME prompt
2. Works on the task, modifying files
3. Tries to exit
4. Stop hook intercepts and feeds the same prompt again
5. CodeBuddy sees its previous work in the files
6. Iteratively improves until completion

The technique is described as "deterministically bad in an undeterministic world" - failures are predictable, enabling systematic improvement through prompt tuning.

## Available Commands

### /ralph-loop <PROMPT> [OPTIONS]

Start a Ralph loop in your current session.

**Usage:**
```
/ralph-loop "Refactor the cache layer" --max-iterations 20
/ralph-loop "Add tests" --completion-promise "TESTS COMPLETE"
```

**Options:**
- `--max-iterations <n>` - Max iterations before auto-stop
- `--completion-promise <text>` - Promise phrase to signal completion

**How it works:**
1. Creates `.codebuddy/.ralph-loop.local.md` state file
2. You work on the task
3. When you try to exit, stop hook intercepts
4. Same prompt fed back
5. You see your previous work
6. Continues until promise detected or max iterations

---

### /cancel-ralph

Cancel an active Ralph loop (removes the loop state file).

**Usage:**
```
/cancel-ralph
```

**How it works:**
- Checks for active loop state file
- Removes `.codebuddy/.ralph-loop.local.md`
- Reports cancellation with iteration count

---

## Key Concepts

### Completion Promises

To signal completion, CodeBuddy must output a `<promise>` tag:

```
<promise>TASK COMPLETE</promise>
```

The stop hook looks for this specific tag. Without it (or `--max-iterations`), Ralph runs infinitely.

### Self-Reference Mechanism

The "loop" doesn't mean CodeBuddy talks to itself. It means:
- Same prompt repeated
- CodeBuddy's work persists in files
- Each iteration sees previous attempts
- Builds incrementally toward goal

## Example

### Interactive Bug Fix

```
/ralph-loop "Fix the token refresh logic in auth.ts. Output <promise>FIXED</promise> when all tests pass." --completion-promise "FIXED" --max-iterations 10
```

You'll see Ralph:
- Attempt fixes
- Run tests
- See failures
- Iterate on solution
- In your current session

## When to Use Ralph

**Good for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration and refinement
- Iterative development with self-correction
- Greenfield projects

**Not good for:**
- Tasks requiring human judgment or design decisions
- One-shot operations
- Tasks with unclear success criteria
- Debugging production issues (use targeted debugging instead)

## Learn More

- Original technique: https://ghuntley.com/ralph/
- Ralph Orchestrator: https://github.com/mikeyobrien/ralph-orchestrator

## 操作指引：ralph-loop

# Ralph Loop Command

Execute the setup script to initialize the Ralph loop:

```!
"${CODEBUDDY_PLUGIN_ROOT}/scripts/setup-ralph-loop.sh" $ARGUMENTS
```

Please work on the task. When you try to exit, the Ralph loop will feed the SAME PROMPT back to you for the next iteration. You'll see your previous work in files and git history, allowing you to iterate and improve.

CRITICAL RULE: If a completion promise is set, you may ONLY output it when the statement is completely and unequivocally TRUE. Do not output false promises to escape the loop, even if you think you're stuck or should exit for other reasons. The loop is designed to continue until genuine completion.
