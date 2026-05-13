# How to Use

## This is a Claude Code Skill

`buy-me-a-car` is a Claude Code skill -- a markdown file that gives Claude domain-specific expertise when triggered by certain phrases. There is nothing to `pip install`.

## Install

1. Copy the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/buy-me-a-car
cp SKILL.md ~/.claude/skills/buy-me-a-car/SKILL.md
```

2. Restart Claude Code (or open a new session). The skill is auto-loaded.

## Trigger Phrases

Claude will activate this skill when you say things like:

- "Help me find a used car under $25k"
- "Negotiate the OTD price with this dealer"
- "Analyze this CARFAX report for red flags"
- "Compare these used car listings across sites"
- "Draft outreach emails to dealers for a 2022 Civic"
- "What's the out-the-door price in Texas?"

It will **not** trigger for car maintenance, repair, insurance, or new-car-only discussions.

## First 60 Seconds

**Input:**

> Help me find a reliable used sedan under $25k in Texas. I want low miles, 2020 or newer.

**What Claude does:**

1. Searches Autotrader, CarGurus, Cars.com, FB Marketplace, Craigslist for matching listings
2. Builds a comparison table (year, make, model, trim, mileage, price, deal rating)
3. Flags "Great Deal" and "Good Deal" listings
4. Asks if you want CARFAX analysis, OTD breakdown, or outreach templates

**Output (abbreviated):**

```
Year  Vehicle                      Miles    Price  Type     Location       Deal
----  --------------------------  ------  -------  -------  -------------  -----------
2022  Honda Civic EX              28,400  $24,500  Dealer   Austin, TX     Good Deal
2021  Toyota Corolla SE           35,200  $21,900  Dealer   Houston, TX    Great Deal
2021  Hyundai Elantra SEL         31,800  $19,500  Dealer   Round Rock, TX Great Deal

Found 5 listings matching criteria.
```

Then say: "Run CARFAX on the Civic and give me the OTD for Texas" -- Claude will analyze the report, calculate tax + title + reg + doc fee, flag add-ons to decline, and draft a dealer email.

## Running the Demo

The demo uses mock data and needs only Python 3.8+:

```bash
bash run.sh
```

This runs all six stages (search, CARFAX, OTD, outreach, negotiation, decision tracker) and prints results to stdout. No API keys or network access required.

## What the 50-State Fee Data Covers

- State sales tax rates (state-level; local rates added per-query)
- Title and registration fees per state
- Doc fee caps (CA, CO, FL, IL, MD, NY, OH, OR, TX, WA)
- Common dealer add-ons with recommended decline scripts
