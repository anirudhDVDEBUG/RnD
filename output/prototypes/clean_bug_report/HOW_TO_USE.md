# How to Use

## Install the Claude Code Skill

Copy the `SKILL.md` file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/clean_bug_report
cp SKILL.md ~/.claude/skills/clean_bug_report/SKILL.md
```

That's it. No dependencies, no API keys, no build step.

## Trigger Phrases

Once installed, the skill activates when you say things like:

- "Help me write a bug report"
- "I need to file a GitHub issue"
- "Draft an issue for this problem I'm seeing"
- "Report this bug upstream"
- "Write up this error as an issue"

## First 60 Seconds

**Input** (you tell Claude):

> Help me file a bug for Flask. After upgrading to 3.1.2, `flask run` crashes
> with a ConnectionResetError on every request. Worked fine on 3.1.1.

**What Claude does:**

1. Asks you the four key questions (command, expected, actual, error output)
2. Drafts a clean report using your exact words
3. Shows you the draft and asks "Is there anything I added that you didn't actually verify yourself?"
4. Removes anything you can't confirm

**Output** (Claude produces):

```markdown
## Description

`flask run` crashes with ConnectionResetError after upgrading to Flask 3.1.2.

## Steps to reproduce

1. pip install flask==3.1.2
2. flask run --port 8080
3. Send any HTTP request to localhost:8080

## Expected behavior

Server handles the request and returns a response.

## Actual behavior

Server accepts the connection but immediately drops it.
Happens on every request, 100% reproducible.

## Error output

    Traceback (most recent call last):
      File ".../flask/serving.py", line 342, in run_wsgi
        execute(self.server.app)
    ConnectionResetError: [Errno 104] Connection reset by peer

## Environment

- Flask: 3.1.2 (worked on 3.1.1)
- Python: 3.12.4
- OS: Ubuntu 24.04
```

No root-cause speculation. No suggested fixes. Just the facts.

## Run the Demo

```bash
bash run.sh
```

This runs a side-by-side comparison showing a clean report vs. an AI-slop version, with automatic slop-pattern detection. No API keys required.
