---
name: initiate
description: Session startup — read handoff, check git state, orient on what's next
user-invocable: true
---

## Session Initiation Procedure

You are starting a new session. Run through these steps IN ORDER to get fully oriented, then present a concise briefing to the user.

### Step 1: Read the handoff report

Glob `scripts/output/session-handoff-*.md` for timestamped handoffs, and also check for legacy `scripts/output/session-handoff.md`. If only one file exists, read it — it is the most direct summary from the previous session. If multiple exist (concurrent sessions), list them with timestamps and ask: "Found [N] handoffs — continue from most recent, a specific one, or combine?" Then read the chosen file(s). If "combine", merge the pending items.

### Step 2: Check uncommitted changes

Run `git status` and `git diff --stat`.

Identify:
- Modified files (what areas of the codebase were touched)
- Untracked files (new features/files added)
- Staged vs unstaged changes

If there are changes beyond what the handoff report describes, note them — they may represent work done after the report was written.

### Step 3: Recent commits

Run `git log --oneline -10`.

Summarize what the last few commits accomplished. Note the gap between committed work and uncommitted work.

### Step 4: Check memory

Read the memory index (`MEMORY.md` in the project's memory directory) and scan for any memories that seem relevant to what's pending. Read the most important ones (especially feedback and project memories). Don't read all files — just the ones that matter for what's next.

### Step 5: Verify cost-aware mode

Check that you are running as **Sonnet** (not Opus). If you detect you are Opus, warn the user immediately:

```
⚠️ COST WARNING: This session is running on Opus. For cost efficiency, restart with Sonnet selected.
Opus should only be used as a subagent for frontier reasoning tasks (see /cost-aware skill).
```

If running as Sonnet, confirm briefly: `✅ Running as Sonnet (cost-aware mode active)`

Read the cost-aware skill (`.claude/skills/cost-aware/SKILL.md`) to load the escalation protocol. All subagents launched this session must use `model: "sonnet"` or `model: "haiku"` unless an explicit Opus escalation is triggered.

### Step 6: Reconstruct the active problem

**Always run this step**, even if the handoff looks clean. This is the crash-recovery backstop.

Look at the most recently touched code to infer what problem was actively being solved:

1. Run `git diff HEAD --stat` to identify the most-changed files
2. For the top 2-3 most modified files, run `git diff HEAD -- <file> | head -120` to read the actual changes
3. If a `copilot-logs/` directory exists, check it: `ls -t copilot-logs/ | head -3`, then `tail -80` on the newest one

From this, synthesize:
- **What was being built or fixed** (the feature or bug)
- **What state it was in** (complete, mid-implementation, or broken)
- **What the likely next action was** (the thing the user would have typed next)

If the handoff already covers this clearly, you can be brief here. If the session crashed with no clean handoff, this becomes the primary recovery signal.

### Step 7: Present the briefing

Output a concise briefing in this format:

```
## Session Briefing

### Model
[Sonnet ✅ or Opus ⚠️ — with cost warning if Opus]

### Product
[One line — what this is, from handoff or CLAUDE.md]

### Last Session
[What was done, from handoff report]

### Uncommitted Changes
[If any beyond what handoff describes — otherwise omit]

### Pending
[What's next, from handoff + memory]

### Key Reminders
[Any feedback memories that apply — budget discipline, git workflow, etc.]

### Active Problem (crash recovery)
[What the code diffs + logs reveal was actively being worked on — feature/bug, completion state, likely next action. Always show this section.]

### Ready
[Suggestions for what to pick up, or "Ready for instructions."]
```

Keep it tight. The user wants to glance at this and know exactly where things stand.
