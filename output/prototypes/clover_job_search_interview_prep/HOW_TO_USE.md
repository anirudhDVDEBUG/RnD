# How to Use — Clover Job Search & Interview Prep

## Run the Demo (no keys needed)

```bash
git clone <this-repo>
cd clover_job_search_interview_prep
bash run.sh
```

Requires only Python 3.10+. No pip installs — stdlib only.

---

## Install the Real MCP Server

### 1. Add to Claude's MCP config

Edit `~/.claude.json` (or your project's `.mcp.json`) and add:

```json
{
  "mcpServers": {
    "clover": {
      "command": "npx",
      "args": ["-y", "@fourleafai/clover-mcp"]
    }
  }
}
```

This requires Node.js 18+ and npm/npx on your PATH.

### 2. Install the Claude Skill (optional, enhances routing)

```bash
mkdir -p ~/.claude/skills/clover-job-search
# Copy the SKILL.md from the source repo into that directory:
cp SKILL.md ~/.claude/skills/clover-job-search/SKILL.md
```

The skill file tells Claude *when* to reach for the Clover MCP tools. Without it the tools still work, but Claude may not automatically invoke them from natural-language prompts.

### 3. Trigger Phrases

Once the MCP server is configured, these prompts activate the Clover tools:

| Prompt | Tool called |
|---|---|
| "Find me software engineer jobs in SF" | `job_search` |
| "Prepare me for an interview at Stripe for Senior SWE" | `interview_prep` |
| "What questions should I expect for a data scientist role?" | `interview_prep` |
| "Review my resume for this backend engineer position" | `resume_review` |
| "Help me with mock interview practice" | Directs to four-leaf.ai voice mock |

---

## First 60 Seconds

**Input** (type into Claude after MCP is configured):

```
Find me senior software engineer jobs, then prepare me for an interview at the top result.
```

**Output** (Claude calls two MCP tools and returns):

```
I found 5 matching jobs. Here are the top results:

1. Senior Software Engineer @ Stripe
   San Francisco, CA (Hybrid) — $190K-$250K
   Tags: Python, Go, Distributed Systems, Payments

2. Staff ML Engineer @ Anthropic
   San Francisco, CA (On-site) — $300K-$400K
   ...

---

Interview Prep for Stripe — Senior Software Engineer:

Process: Recruiter screen > Tech phone screen > On-site (3 rounds) > Committee

Technical Questions:
  - Design a payment processing pipeline with idempotency and retries.
  - How would you build a rate limiter for distributed API servers?

Behavioral:
  - Tell me about a time you simplified a complex system.
  - Describe a situation where you disagreed with a technical decision.

Tips:
  - Stripe values clarity of thought — explain trade-offs explicitly.
  - Show awareness of financial system constraints.
```

No API keys are needed for the MCP server itself — it connects to four-leaf.ai's public endpoints.
