---
name: company_execution_layer
description: |
  Build and manage an execution layer for your company brain — turning knowledge docs into runnable playbooks and SOPs via a skills marketplace.
  Triggers: "set up execution layer", "create skills marketplace", "wire skills to company brain", "build company playbook", "execution layer for knowledge base"
---

# Company Execution Layer Builder

Transform your company's second brain (interconnected docs, SOPs, playbooks) into an **execution layer** — a structured skills marketplace where Claude can run real workflows over your existing knowledge, not just reference it.

## When to use

- "Set up an execution layer for my company brain"
- "Create a skills marketplace from our SOPs and playbooks"
- "Wire skills into our company knowledge base"
- "Turn our docs into runnable Claude skills"
- "Build an execution layer so the team can run playbooks with AI"

## How to use

### Step 1: Audit your company brain

Identify the knowledge docs that already exist — wiki pages, Notion databases, Google Docs, markdown vaults, etc. These form your **context layer**. List the key areas:

- Brand guidelines & tone of voice
- Standard operating procedures (SOPs)
- Playbooks (sales, onboarding, support, content)
- Product specs & architecture docs
- Meeting formats & reporting templates

### Step 2: Scaffold the skills marketplace

Create a directory structure that separates context from execution:

```
company-brain/
├── CLAUDE.md                  # Root config pointing to skills & context
├── context/                   # Your second brain (knowledge layer)
│   ├── brand/
│   │   └── voice-and-tone.md
│   ├── products/
│   │   └── product-specs.md
│   ├── processes/
│   │   └── sops.md
│   └── team/
│       └── org-chart.md
├── skills/                    # Execution layer (skills marketplace)
│   ├── content-creation/
│   │   └── SKILL.md
│   ├── client-onboarding/
│   │   └── SKILL.md
│   ├── weekly-report/
│   │   └── SKILL.md
│   └── proposal-generator/
│       └── SKILL.md
└── output/                    # Where finished work lands
```

### Step 3: Write skills that reference (not hard-code) context

Each skill should **reference** your context docs rather than duplicating content. This keeps context live and avoids drift.

Example `skills/content-creation/SKILL.md`:

```markdown
---
name: content_creation
description: |
  Create on-brand content using company voice guidelines and product knowledge.
  Triggers: "write a blog post", "draft social copy", "create content"
---

# Content Creation Skill

## Steps

1. Read `context/brand/voice-and-tone.md` for brand voice rules
2. Read `context/products/product-specs.md` for accurate product details
3. Ask the user for: topic, format (blog/social/email), target audience, length
4. Draft the content following brand guidelines
5. Output the finished piece to `output/content/` with a dated filename
```

### Step 4: Configure CLAUDE.md to wire it together

Your root `CLAUDE.md` should register available skills and point to the context layer:

```markdown
# Company Brain — Execution Layer

## Context (read these for company knowledge)
- `context/brand/` — Brand voice, visual identity
- `context/products/` — Product specs, features, pricing
- `context/processes/` — SOPs, workflows, approval chains
- `context/team/` — Org chart, roles, responsibilities

## Available Skills (run these to ship work)
- `/content-creation` — Draft on-brand content
- `/client-onboarding` — Run the client onboarding checklist
- `/weekly-report` — Generate the weekly status report
- `/proposal-generator` — Build a client proposal from template

When a user invokes a skill, read its SKILL.md and follow the steps exactly.
Always pull live context from the context/ directory — never hard-code company info.
```

### Step 5: Add a new skill from an existing SOP

To convert any existing SOP or playbook into a skill:

1. **Identify the SOP** — find the document that describes the process
2. **Extract the steps** — pull out the ordered sequence of actions
3. **Map inputs/outputs** — what does the skill need from the user? What does it produce?
4. **Reference context** — link to any company docs the skill needs to read
5. **Create `skills/<skill-name>/SKILL.md`** — write the skill following the template above
6. **Register it** — add the skill to the root `CLAUDE.md`

### Step 6: Scale across the team

The execution layer provides **team-wide leverage** because:

- Anyone on the team can run any skill — no tribal knowledge required
- Context stays centralized and live — update once, all skills benefit
- New hires get instant access to institutional playbooks
- Skills can be shared, forked, and improved collaboratively

## Key Principles

| Principle | Why it matters |
|---|---|
| **Reference, don't hard-code** | Context docs change; skills that reference them stay current automatically |
| **Separate context from execution** | Clean architecture — brain knows, skills do |
| **One skill per playbook** | Keep skills focused and composable |
| **Output to a known location** | Makes finished work easy to find and review |
| **Register in CLAUDE.md** | Discoverability — the team sees what's available |

## References

- Source video: [Build an Execution Layer for Your Company Brain (Step by Step)](https://www.youtube.com/watch?v=gMm50Sy_GmQ)
- Free template: [Company Skills Marketplace Template](https://github.com/bradautomates/company-skills-marketplace-template)
- By Bradley Bonanno — [LinkedIn](https://www.linkedin.com/in/bradbonanno/)
