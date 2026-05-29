# How to Use

## Install (standalone CLI)

No external dependencies. Requires Python 3.8+.

```bash
git clone https://github.com/seomarlboro/domain-check-skills.git
cd domain-check-skills
python3 domain_check.py myproject com,io,dev
```

Or use this prototype directly:

```bash
bash run.sh
```

## Install as a Claude Code Skill

1. Copy the `SKILL.md` file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/domain-check-availability
cp SKILL.md ~/.claude/skills/domain-check-availability/SKILL.md
```

2. Restart Claude Code (or start a new session).

3. **Trigger phrases** that activate the skill:
   - "check domain"
   - "domain availability"
   - "is this domain available"
   - "find available domains"
   - "search domain name"
   - "check domain name options for a new startup"

When triggered, Claude will use `curl` to call the digmyname.com API and format results as a table.

## First 60 Seconds

**Input:**
```
> check if launchpad is available as a domain
```

**What Claude does (via the skill):**
```bash
curl -s "https://api.digmyname.com/check?domain=launchpad&tlds=com,net,io,dev,ai,co,org"
```

**Output you see:**
```
Domain                    Status       Best Price     Registrar
----------------------------------------------------------------------
launchpad.com             TAKEN        $8.88          Namecheap
launchpad.net             AVAILABLE    $10.98         Namecheap
launchpad.io              AVAILABLE    $25.99         Porkbun
launchpad.dev             AVAILABLE    $10.11         Cloudflare
launchpad.ai              TAKEN        $58.98         Namecheap
launchpad.co              AVAILABLE    $10.87         Porkbun
launchpad.org             TAKEN        $8.57          Cloudflare

Summary: 4/7 domains available
Best deal: launchpad.net at $10.98 via Namecheap
```

## CLI Usage (standalone)

```bash
# Check default TLDs (com, net, io, dev, ai, co, org, app, xyz)
python3 domain_check.py brandname

# Check specific TLDs
python3 domain_check.py brandname com,io,dev,ai

# Full domain input (TLD is stripped, then all requested TLDs are checked)
python3 domain_check.py example.com com,net,io
```

The script tries the live API first. If unreachable, it uses built-in mock data so the demo always produces output.
