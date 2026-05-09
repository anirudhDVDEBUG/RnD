---
name: google_ads_cli_toolkit
description: |
  Manage Google Ads, Google Tag Manager (GTM), and GA4 from the terminal using the google-ads-cli-toolkit.
  TRIGGER when: user asks about Google Ads campaign management, GTM container operations, GA4 analytics queries, or PPC automation from the CLI.
  DO NOT TRIGGER when: user is working with other ad platforms (Meta Ads, LinkedIn Ads) or non-Google analytics tools.
---

# Google Ads CLI Toolkit

Open-source CLI toolkit for managing Google Ads, Google Tag Manager (GTM), and Google Analytics 4 (GA4) from the terminal, with built-in Claude Code integration.

## When to use

- "Help me manage my Google Ads campaigns from the terminal"
- "Pull my GA4 analytics data via CLI"
- "Automate Google Tag Manager container changes"
- "Set up the google-ads-cli-toolkit for PPC management"
- "Query my Google Ads performance metrics from the command line"

## How to use

### 1. Clone and install the toolkit

```bash
git clone https://github.com/nicolasmaldonadoj/google-ads-cli-toolkit.git
cd google-ads-cli-toolkit
pip install -r requirements.txt
```

### 2. Configure Google API credentials

The toolkit requires Google API credentials for each service you want to use:

- **Google Ads API**: You need a `google-ads.yaml` config file with your developer token, client ID, client secret, refresh token, and customer ID. See [Google Ads API docs](https://developers.google.com/google-ads/api/docs/first-call/overview) for setup.
- **GTM API**: Enable the Tag Manager API in Google Cloud Console and configure OAuth2 credentials.
- **GA4 API**: Enable the Google Analytics Data API and configure service account or OAuth2 credentials.

### 3. Use the CLI tools

The toolkit provides Python-based CLI scripts for interacting with Google Ads, GTM, and GA4:

- **Google Ads**: Query campaigns, ad groups, keywords, and performance metrics using GAQL (Google Ads Query Language).
- **GTM**: Manage containers, workspaces, tags, triggers, and variables programmatically.
- **GA4**: Pull analytics reports, dimensions, and metrics.

### 4. Claude Code integration

The toolkit includes a playbook designed for Claude Code. When working with Google Ads, GTM, or GA4 tasks:

1. Ensure the toolkit is cloned and dependencies are installed in your workspace.
2. Verify API credentials are configured (check for `google-ads.yaml` or equivalent config).
3. Use the provided CLI scripts to execute queries and management operations.
4. Leverage Claude to compose GAQL queries, interpret campaign performance, and automate bulk operations.

### Tips

- Always confirm the Google Ads customer ID before running queries (use the format `XXX-XXX-XXXX`).
- Use `--dry-run` flags when available to preview changes before applying them.
- For bulk operations, review the generated changes before committing them to avoid unintended ad spend.
- Keep your `google-ads.yaml` and credential files out of version control (add to `.gitignore`).

## References

- **Repository**: https://github.com/nicolasmaldonadoj/google-ads-cli-toolkit
- **Google Ads API docs**: https://developers.google.com/google-ads/api/docs/start
- **GTM API docs**: https://developers.google.com/tag-platform/tag-manager/api/v2
- **GA4 Data API docs**: https://developers.google.com/analytics/devguides/reporting/data/v1
