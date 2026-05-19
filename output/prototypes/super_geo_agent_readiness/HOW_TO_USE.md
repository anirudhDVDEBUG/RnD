# How to Use

## This is a Claude Skill

The upstream repo is a **Claude Code skill** (a `SKILL.md` file that teaches Claude how to audit and optimize sites for GEO). This prototype also includes a standalone Python auditor you can run without Claude.

### Option A: Install the Skill in Claude Code

1. Copy the skill folder into your skills directory:

```bash
mkdir -p ~/.claude/skills/super_geo_agent_readiness
cp SKILL.md ~/.claude/skills/super_geo_agent_readiness/SKILL.md
```

2. Restart Claude Code (or open a new session).

3. Use any of these trigger phrases in conversation:
   - "Audit my site for generative engine optimization"
   - "How do I get my site cited by ChatGPT or Perplexity?"
   - "Set up llms.txt for my project"
   - "Make my API discoverable by AI agents"
   - "Add Schema.org structured data for AI search"
   - "MCP endpoint setup"
   - "Agent readiness audit"

Claude will then walk through the full GEO checklist: llms.txt, MCP manifest, Schema.org, OAuth, robots.txt, sitemap, and content quality.

### Option B: Run the Standalone Auditor

No API keys needed. Python 3.8+ only (stdlib, zero dependencies).

```bash
git clone <this-repo>
cd super_geo_agent_readiness
bash run.sh
```

Or audit a specific local directory:

```bash
python3 geo_audit.py /path/to/your/site/root
```

The auditor expects a directory with the same file layout a web server would serve (e.g., `llms.txt`, `robots.txt`, `.well-known/mcp.json`, `index.html`, etc.).

## First 60 Seconds

```
$ bash run.sh

=== Super GEO & Agent Readiness Demo ===

[Pass 1] Auditing well-configured sample site...

========================================================================
  GEO & Agent Readiness Audit  --  https://demo-saas.example.com
========================================================================
Check                           Score  Status  Detail
------------------------------------------------------------------------
llms.txt                         100%  PASS    Found (243 bytes)
llms-full.txt                      0%  FAIL    Not found
MCP manifest                     100%  PASS    Valid JSON; tools=yes, name=yes
Schema.org markup                  70%  PASS    2 JSON-LD block(s); types: WebSite, FAQPage
robots.txt                        100%  PASS    Blocked: none
OAuth discovery                   100%  PASS    issuer=yes, endpoints=yes
sitemap.xml                       100%  PASS    Found with 5 URL(s)
Content quality                   100%  PASS    Signals: lists, tables, citations
------------------------------------------------------------------------
OVERALL                           83.8%
========================================================================

Recommendations:
  1. [llms-full.txt] Create /llms-full.txt with expanded content for deeper AI context.

[Pass 2] Auditing a bare site with no GEO signals...
  (mostly FAIL -- shows what a non-optimized site looks like)
```

The two-pass comparison shows exactly what signals matter and what's missing.
