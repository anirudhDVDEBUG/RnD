#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo "  Google Ads CLI Toolkit — Demo Run"
echo "  (Using mock data — no API keys required)"
echo "============================================================"
echo ""

# 1. Account status overview
echo ">>> python3 google_ads_cli.py status"
python3 google_ads_cli.py status

# 2. List campaigns with performance metrics
echo ">>> python3 google_ads_cli.py campaigns --metrics"
python3 google_ads_cli.py campaigns --metrics

# 3. Execute a GAQL query
echo '>>> python3 google_ads_cli.py query "SELECT campaign.id, campaign.name, metrics.impressions FROM campaign"'
python3 google_ads_cli.py query "SELECT campaign.id, campaign.name, metrics.impressions FROM campaign"

# 4. GTM containers
echo ">>> python3 google_ads_cli.py gtm"
python3 google_ads_cli.py gtm

# 5. GA4 analytics report
echo ">>> python3 google_ads_cli.py ga4"
python3 google_ads_cli.py ga4

echo "============================================================"
echo "  Demo complete. All commands ran with mock data."
echo "  To use with real Google Ads, configure google-ads.yaml"
echo "  and install the full toolkit from:"
echo "  https://github.com/nicolasmaldonadoj/google-ads-cli-toolkit"
echo "============================================================"
