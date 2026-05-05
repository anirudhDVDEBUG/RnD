#!/usr/bin/env node
/**
 * Mock Markifact MCP Server — demonstrates the tool schema and human-in-the-loop
 * flow without requiring real ad platform credentials.
 */

const PLATFORMS = {
  google_ads: {
    name: "Google Ads",
    tools: [
      "google_ads_list_campaigns",
      "google_ads_get_campaign",
      "google_ads_create_campaign",
      "google_ads_update_campaign",
      "google_ads_pause_campaign",
      "google_ads_list_ad_groups",
      "google_ads_create_ad_group",
      "google_ads_list_keywords",
      "google_ads_add_keyword",
      "google_ads_get_performance_report",
    ],
  },
  meta_ads: {
    name: "Meta Ads",
    tools: [
      "meta_ads_list_campaigns",
      "meta_ads_get_campaign",
      "meta_ads_create_campaign",
      "meta_ads_update_campaign",
      "meta_ads_list_ad_sets",
      "meta_ads_create_ad_set",
      "meta_ads_list_ads",
      "meta_ads_create_ad",
      "meta_ads_get_insights",
    ],
  },
  ga4: {
    name: "GA4",
    tools: [
      "ga4_run_report",
      "ga4_list_properties",
      "ga4_get_realtime_report",
      "ga4_list_audiences",
    ],
  },
  tiktok_ads: {
    name: "TikTok Ads",
    tools: [
      "tiktok_ads_list_campaigns",
      "tiktok_ads_create_campaign",
      "tiktok_ads_list_ad_groups",
      "tiktok_ads_get_report",
    ],
  },
  linkedin_ads: {
    name: "LinkedIn Ads",
    tools: [
      "linkedin_ads_list_campaigns",
      "linkedin_ads_create_campaign",
      "linkedin_ads_list_creatives",
      "linkedin_ads_get_analytics",
    ],
  },
};

// ── Mock data ──────────────────────────────────────────────────────────
const MOCK_CAMPAIGNS = [
  {
    id: "camp_001",
    platform: "google_ads",
    name: "Brand Awareness — Q2 2026",
    status: "ENABLED",
    budget_daily: 150.0,
    impressions: 245320,
    clicks: 4821,
    ctr: "1.97%",
    spend: 3240.5,
    conversions: 187,
    cpa: 17.33,
  },
  {
    id: "camp_002",
    platform: "google_ads",
    name: "Product Launch — Widget Pro",
    status: "ENABLED",
    budget_daily: 300.0,
    impressions: 512100,
    clicks: 11234,
    ctr: "2.19%",
    spend: 8450.0,
    conversions: 342,
    cpa: 24.71,
  },
  {
    id: "camp_003",
    platform: "meta_ads",
    name: "Retargeting — Cart Abandoners",
    status: "ENABLED",
    budget_daily: 80.0,
    impressions: 98450,
    clicks: 3210,
    ctr: "3.26%",
    spend: 1920.0,
    conversions: 156,
    cpa: 12.31,
  },
  {
    id: "camp_004",
    platform: "meta_ads",
    name: "Lookalike — Top Buyers",
    status: "PAUSED",
    budget_daily: 200.0,
    impressions: 0,
    clicks: 0,
    ctr: "0%",
    spend: 0,
    conversions: 0,
    cpa: 0,
  },
  {
    id: "camp_005",
    platform: "tiktok_ads",
    name: "Gen-Z Awareness — Summer",
    status: "ENABLED",
    budget_daily: 120.0,
    impressions: 780200,
    clicks: 18900,
    ctr: "2.42%",
    spend: 2640.0,
    conversions: 95,
    cpa: 27.79,
  },
  {
    id: "camp_006",
    platform: "linkedin_ads",
    name: "B2B Lead Gen — Enterprise",
    status: "ENABLED",
    budget_daily: 250.0,
    impressions: 34500,
    clicks: 890,
    ctr: "2.58%",
    spend: 5120.0,
    conversions: 42,
    cpa: 121.9,
  },
];

// ── Tool handlers ──────────────────────────────────────────────────────
function isWriteOperation(toolName) {
  return /create|update|pause|add|delete|remove/.test(toolName);
}

function handleTool(name, args) {
  // List campaigns (any platform)
  if (name.includes("list_campaigns")) {
    const platform = name.split("_")[0] + "_" + name.split("_")[1];
    const filtered = MOCK_CAMPAIGNS.filter((c) =>
      c.platform.startsWith(platform.replace("_ads", ""))
    );
    return { campaigns: filtered.length > 0 ? filtered : MOCK_CAMPAIGNS };
  }

  // Get single campaign
  if (name.includes("get_campaign")) {
    const camp =
      MOCK_CAMPAIGNS.find((c) => c.id === args?.campaign_id) ||
      MOCK_CAMPAIGNS[0];
    return { campaign: camp };
  }

  // Performance / insights / report
  if (
    name.includes("report") ||
    name.includes("insights") ||
    name.includes("analytics")
  ) {
    return {
      date_range: args?.date_range || "last_30_days",
      metrics: {
        impressions: 1670570,
        clicks: 39055,
        ctr: "2.34%",
        total_spend: 21370.5,
        conversions: 822,
        avg_cpa: 25.99,
        roas: 3.8,
      },
    };
  }

  // Create operations (write — requires confirmation)
  if (name.includes("create")) {
    return {
      created: true,
      id: "camp_" + Math.random().toString(36).slice(2, 8),
      name: args?.name || "New Campaign",
      status: "PAUSED",
      message: "Campaign created in PAUSED state. Enable when ready.",
    };
  }

  // Update / pause
  if (name.includes("update") || name.includes("pause")) {
    return {
      updated: true,
      id: args?.campaign_id || "camp_001",
      changes: args || { status: "PAUSED" },
    };
  }

  return { message: `Tool ${name} executed successfully`, args };
}

// ── MCP protocol simulation ────────────────────────────────────────────
function buildToolList() {
  const tools = [];
  for (const [platformKey, platform] of Object.entries(PLATFORMS)) {
    for (const toolName of platform.tools) {
      const isWrite = isWriteOperation(toolName);
      tools.push({
        name: toolName,
        description: `[${platform.name}] ${toolName.replace(/_/g, " ")}${isWrite ? " (requires confirmation)" : ""}`,
        inputSchema: {
          type: "object",
          properties: {
            campaign_id: { type: "string", description: "Campaign ID" },
            name: { type: "string", description: "Campaign name" },
            budget: { type: "number", description: "Daily budget" },
            date_range: {
              type: "string",
              enum: ["today", "last_7_days", "last_30_days", "last_90_days"],
            },
          },
        },
        annotations: {
          readOnlyHint: !isWrite,
          destructiveHint: isWrite,
          confirmationRequired: isWrite,
        },
      });
    }
  }
  return tools;
}

// ── Demo runner ────────────────────────────────────────────────────────
function runDemo() {
  console.log("=".repeat(64));
  console.log("  Markifact MCP Server — Mock Demo");
  console.log("=".repeat(64));
  console.log();

  // Show registered tools
  const tools = buildToolList();
  console.log(`Registered ${tools.length} MCP tools across ${Object.keys(PLATFORMS).length} platforms:\n`);

  for (const [key, platform] of Object.entries(PLATFORMS)) {
    console.log(`  ${platform.name}: ${platform.tools.length} tools`);
  }

  console.log(`\n${"─".repeat(64)}`);
  console.log("DEMO 1: List all campaigns (READ — no confirmation needed)");
  console.log("─".repeat(64));

  const listResult = handleTool("google_ads_list_campaigns", {});
  console.log("\n> Tool: google_ads_list_campaigns");
  console.log("> Confirmation required: NO (read operation)\n");
  for (const c of listResult.campaigns) {
    console.log(
      `  [${c.status.padEnd(7)}] ${c.name.padEnd(35)} ` +
        `spend=$${c.spend.toFixed(2).padStart(9)}  ` +
        `conv=${String(c.conversions).padStart(4)}  ` +
        `CPA=$${c.cpa.toFixed(2)}`
    );
  }

  console.log(`\n${"─".repeat(64)}`);
  console.log("DEMO 2: Get cross-platform performance report (READ)");
  console.log("─".repeat(64));

  const reportResult = handleTool("google_ads_get_performance_report", {
    date_range: "last_30_days",
  });
  console.log("\n> Tool: google_ads_get_performance_report");
  console.log("> Date range:", reportResult.date_range);
  console.log("> Confirmation required: NO (read operation)\n");
  const m = reportResult.metrics;
  console.log(`  Impressions:  ${m.impressions.toLocaleString()}`);
  console.log(`  Clicks:       ${m.clicks.toLocaleString()}`);
  console.log(`  CTR:          ${m.ctr}`);
  console.log(`  Total spend:  $${m.total_spend.toLocaleString()}`);
  console.log(`  Conversions:  ${m.conversions}`);
  console.log(`  Avg CPA:      $${m.avg_cpa}`);
  console.log(`  ROAS:         ${m.roas}x`);

  console.log(`\n${"─".repeat(64)}`);
  console.log("DEMO 3: Create a new campaign (WRITE — confirmation required)");
  console.log("─".repeat(64));

  console.log("\n> Tool: meta_ads_create_campaign");
  console.log("> Args: { name: 'Summer Sale 2026', budget: 200 }");
  console.log("> Confirmation required: YES (write operation)");
  console.log();
  console.log(
    '  [HUMAN-IN-THE-LOOP] The AI client would show a confirmation dialog:'
  );
  console.log(
    '  ┌─────────────────────────────────────────────────────────┐'
  );
  console.log(
    '  │  Create campaign "Summer Sale 2026" on Meta Ads?       │'
  );
  console.log(
    '  │  Daily budget: $200.00                                  │'
  );
  console.log(
    '  │                                                         │'
  );
  console.log(
    '  │  [Approve]   [Deny]                                     │'
  );
  console.log(
    '  └─────────────────────────────────────────────────────────┘'
  );
  console.log();

  console.log("  User approved. Executing...\n");
  const createResult = handleTool("meta_ads_create_campaign", {
    name: "Summer Sale 2026",
    budget: 200,
  });
  console.log(`  Created: ${createResult.name} (ID: ${createResult.id})`);
  console.log(`  Status:  ${createResult.status}`);
  console.log(`  Note:    ${createResult.message}`);

  console.log(`\n${"─".repeat(64)}`);
  console.log("DEMO 4: Pause underperforming campaigns (WRITE — confirmation)");
  console.log("─".repeat(64));

  const highCPA = MOCK_CAMPAIGNS.filter((c) => c.cpa > 25 && c.status === "ENABLED");
  console.log("\n> Strategy: Pause all campaigns with CPA > $25.00");
  console.log(`> Found ${highCPA.length} campaigns to pause:\n`);
  for (const c of highCPA) {
    console.log(`  - ${c.name} (CPA: $${c.cpa.toFixed(2)}, platform: ${c.platform})`);
  }
  console.log();
  console.log("  [HUMAN-IN-THE-LOOP] Each pause requires separate confirmation.");
  for (const c of highCPA) {
    const pauseResult = handleTool("google_ads_pause_campaign", {
      campaign_id: c.id,
    });
    console.log(`  Paused: ${c.name} (${pauseResult.id})`);
  }

  // Summary
  console.log(`\n${"=".repeat(64)}`);
  console.log("  Summary");
  console.log("=".repeat(64));
  console.log();
  console.log("  This mock demonstrates the Markifact MCP server pattern:");
  console.log(
    `  - ${tools.length} tools registered across ${Object.keys(PLATFORMS).length} ad platforms`
  );
  console.log(
    "  - Read operations execute immediately (no confirmation)"
  );
  console.log(
    "  - Write operations require human-in-the-loop approval"
  );
  console.log(
    "  - Supports: Google Ads, Meta Ads, GA4, TikTok Ads, LinkedIn Ads"
  );
  console.log();
  console.log("  To use the real server: npx markifact-mcp");
  console.log(
    "  Docs: https://github.com/markifact/markifact-mcp"
  );
  console.log();
}

// If run directly, execute the demo
if (require.main === module) {
  runDemo();
}

module.exports = { buildToolList, handleTool, PLATFORMS, MOCK_CAMPAIGNS };
