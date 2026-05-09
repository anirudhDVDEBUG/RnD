# How to Use — Google Ads CLI Toolkit

## Install (Full Toolkit)

```bash
git clone https://github.com/nicolasmaldonadoj/google-ads-cli-toolkit.git
cd google-ads-cli-toolkit
pip install -r requirements.txt
```

Dependencies: `google-ads`, `google-api-python-client`, `google-analytics-data`, `google-auth`, `google-auth-oauthlib`, `pyyaml`.

## Claude Code Skill Setup

This is a **Claude Code Skill**. To install:

```bash
mkdir -p ~/.claude/skills/google_ads_cli_toolkit
cp SKILL.md ~/.claude/skills/google_ads_cli_toolkit/SKILL.md
```

### Trigger Phrases

The skill activates when you say things like:

- "Help me manage my Google Ads campaigns from the terminal"
- "Pull my GA4 analytics data via CLI"
- "Automate Google Tag Manager container changes"
- "Set up the google-ads-cli-toolkit for PPC management"
- "Query my Google Ads performance metrics from the command line"

**Does NOT trigger for:** Meta Ads, LinkedIn Ads, or non-Google analytics platforms.

## Configure Google API Credentials

Before using with real data, you need credentials for each service:

### Google Ads API

Create `google-ads.yaml` in the toolkit root:

```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: "123-456-7890"
```

Get credentials at: https://developers.google.com/google-ads/api/docs/first-call/overview

### GTM API

1. Enable Tag Manager API in Google Cloud Console
2. Create OAuth2 credentials (Desktop app type)
3. Run the initial auth flow to generate a refresh token

### GA4 API

1. Enable Google Analytics Data API in Cloud Console
2. Create a service account or OAuth2 credentials
3. Grant the service account Viewer access on your GA4 property

## First 60 Seconds

No credentials needed — this demo uses mock data.

**Step 1: Run the demo**

```bash
bash run.sh
```

**Step 2: Try individual commands**

```bash
# Account overview
python3 google_ads_cli.py status

# Campaign list with full metrics
python3 google_ads_cli.py campaigns --metrics

# Execute a GAQL query
python3 google_ads_cli.py query "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED'"

# GTM container summary
python3 google_ads_cli.py gtm

# GA4 traffic report by source
python3 google_ads_cli.py ga4
```

**Expected output (status command):**

```
  ACCOUNT STATUS — 123-456-7890

  Campaigns:     5 total (4 enabled, 1 paused)
  Daily Budget:  $275.00
  Period Cost:   $48,291.35
  Conversions:   2,847
  GTM Containers: 2
  GA4 Sources:   5

  Status: All systems operational (mock mode)
```

**Step 3: With real credentials** — create `google-ads.yaml`, then replace `google_ads_cli.py` with the full toolkit scripts from the [source repo](https://github.com/nicolasmaldonadoj/google-ads-cli-toolkit).

## CLI Reference

| Command | Description |
|---------|-------------|
| `status` | Account overview: campaign counts, budgets, total metrics |
| `campaigns` | List all campaigns (add `--metrics` for performance data) |
| `campaigns --metrics` | Full metrics: impressions, clicks, CTR, CPC, cost, conversions, ROAS |
| `query "<GAQL>"` | Execute a Google Ads Query Language query |
| `gtm` | List GTM containers with tag/trigger/variable counts |
| `ga4` | GA4 traffic report: sessions, users, conversions, revenue by source |
| `--customer-id XXX` | Override the default customer ID (any command) |
