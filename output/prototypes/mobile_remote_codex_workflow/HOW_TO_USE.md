# How to Use

## Install

```bash
# No external dependencies — Python 3.10+ only
git clone <this-repo>
cd mobile_remote_codex_workflow
```

## Run the Demo

```bash
bash run.sh
```

No API keys required — uses mock data to simulate the full Codex workflow.

## As a Claude Skill

Drop the skill file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/mobile_remote_codex_workflow
cp SKILL.md ~/.claude/skills/mobile_remote_codex_workflow/SKILL.md
```

### Trigger Phrases

- "I want to monitor my Codex coding tasks from my phone"
- "How do I approve or steer Codex changes remotely?"
- "Set up a mobile-friendly remote coding workflow with AI"
- "I need to manage coding agents across multiple devices"
- "Help me review and approve AI-generated code on the go"

## First 60 Seconds

**Input:** Run `bash run.sh`

**Output:**
```
[1] CREATING TASKS FROM MOBILE (iOS ChatGPT App)
  Task created: ctx_a1b2c3d4
  Description: Add input validation to the signup form...
  Device: iOS (ChatGPT App)

[2] MONITORING PROGRESS IN REAL TIME
  [ 15%] Reading codebase and understanding context...
  [ 30%] Planning implementation approach...
  [ 50%] Writing code changes...
  [ 70%] Running tests and validating...
  [ 85%] Generating diffs for review...
  [100%] Ready for review.

[3] STEERING TASK FROM MOBILE
  Instruction: "Focus on email validation first, use RFC 5322 regex pattern"
  Acknowledged: True

[4] REVIEWING CODE DIFFS ON MOBILE
  --- src/auth/validators.py (+24/-3)
  --- tests/test_validators.py (+35/-0)

[5] APPROVING CHANGES FROM MOBILE
  Action: APPROVED
  PR Created: https://github.com/myorg/webapp-frontend/pull/427

[6] CROSS-DEVICE DASHBOARD
  (JSON summary of all tasks and their statuses)
```

## Integration with Real Codex

To connect to the actual OpenAI Codex API (when available):

1. Install the ChatGPT mobile app (iOS/Android)
2. Sign in with a Codex-enabled OpenAI account
3. Start tasks from the Codex tab
4. Monitor/steer/approve from any device signed into the same account

The workflow patterns demonstrated here (create → monitor → steer → review → approve) map 1:1 to the real Codex mobile experience.
