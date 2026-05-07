# How to Use

## This is a Claude Code Skill

The CosmoBlk email-design project provides a **SKILL.md** file that Claude Code loads to gain email design capabilities. It does not require a running server — Claude reads the skill definition and follows its instructions when triggered.

## Install the skill

```bash
# Clone the skill repo into Claude's skills directory
mkdir -p ~/.claude/skills
git clone https://github.com/CosmoBlk/email-design.git ~/.claude/skills/email-design
```

After cloning, restart Claude Code (or start a new session). Claude will auto-discover `~/.claude/skills/email-design/SKILL.md`.

### Trigger phrases

Say any of these to Claude Code and it will activate the email design skill:

- "design an email"
- "create email template"
- "build an MJML email"
- "email campaign"
- "marketing email"

## Run this prototype locally

```bash
# Prerequisites: Node.js >= 16
cd cosmoblk_email_design
bash run.sh
```

This installs `mjml` (the only dependency), generates all six archetype emails, and writes `.mjml` + `.html` files to `output/`.

### CLI options

```bash
# Single archetype with specific ESP
node index.js <archetype> <esp>

# Examples:
node index.js welcome generic
node index.js promotional klaviyo
node index.js newsletter mailchimp
node index.js transactional activecampaign

# All six archetypes at once
node generate_all.js
```

**Archetypes:** `welcome`, `promotional`, `newsletter`, `transactional`, `reengagement`, `announcement`

**ESPs:** `generic`, `nitrosend`, `klaviyo`, `mailchimp`, `activecampaign`

## First 60 seconds

```
$ bash run.sh

╔══════════════════════════════════════════╗
║  CosmoBlk Email Design — Demo Runner     ║
╚══════════════════════════════════════════╝

→ Installing dependencies (mjml)...

─── 1. Single archetype: Welcome email ───

=== CosmoBlk Email Design Demo ===
Archetype : Welcome
Brand     : Vortex Labs
ESP       : generic
================================

MJML saved to: output/welcome.mjml
HTML saved to: output/welcome.html
HTML size: 9.2 KB

─── 2. All six archetypes at once ───

  [OK] Welcome         → output/welcome.html  (9.2 KB)
  [OK] Promotional     → output/promotional.html  (9.8 KB)
  [OK] Newsletter      → output/newsletter.html  (10.1 KB)
  [OK] Transactional   → output/transactional.html  (10.4 KB)
  [OK] Re-engagement   → output/reengagement.html  (9.1 KB)
  [OK] Announcement    → output/announcement.html  (9.9 KB)

✓ All done. Open any .html file in a browser to see the rendered email.
```

Open `output/welcome.html` in a browser to see the fully responsive email. Every email includes branded header, real copy, CTA button with a real `href`, and a CAN-SPAM compliant footer with unsubscribe link.

## ESP delivery via MCP

If you have an MCP server configured for your ESP (e.g., Nitrosend, Klaviyo), the skill instructs Claude to use available MCP tools to push the template directly to the ESP — no copy-paste needed. Set the ESP when generating to get correct merge tags (`*|FNAME|*` for Mailchimp, `{{ first_name }}` for Klaviyo, etc.).
