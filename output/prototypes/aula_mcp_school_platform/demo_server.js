#!/usr/bin/env node
/**
 * Aula MCP Demo Server — demonstrates the tool interface with mock data.
 * No real credentials needed. Shows what the actual aula-mcp server exposes.
 */

const MOCK_PROFILES = [
  {
    id: "child-001",
    name: "Magnus Jensen",
    role: "child",
    school: "Skovlunde Skole",
    class: "3.B",
    age: 9
  },
  {
    id: "child-002",
    name: "Freja Jensen",
    role: "child",
    school: "Skovlunde Skole",
    class: "1.A",
    age: 6
  },
  {
    id: "parent-001",
    name: "Lars Jensen",
    role: "parent",
    relation: "Far"
  }
];

const MOCK_CALENDAR = [
  {
    date: "2026-05-06",
    title: "Matematikdag",
    description: "Temadag med fokus pa matematik i hverdagen",
    child: "Magnus Jensen",
    allDay: true
  },
  {
    date: "2026-05-08",
    title: "Foraldremode 3.B",
    description: "Klassens trivsel og sommerplaner",
    child: "Magnus Jensen",
    time: "19:00-20:30"
  },
  {
    date: "2026-05-12",
    title: "Skolefotografering",
    description: "Husk pænt tøj",
    child: "Freja Jensen",
    allDay: true
  }
];

const MOCK_MESSAGES = [
  {
    id: "msg-101",
    from: "Lone Hansen (Klasselærer, 3.B)",
    subject: "Tur til Experimentarium d. 15/5",
    date: "2026-05-05",
    preview: "Kære forældre, vi skal på tur til Experimentarium torsdag d. 15. maj. Mødested er skolen kl. 8:15. Medbring madpakke og regnjakke.",
    unread: true
  },
  {
    id: "msg-102",
    from: "SFO Skovlunde",
    subject: "Sommerafslutning 20. juni",
    date: "2026-05-04",
    preview: "Husk tilmelding til sommerafslutning senest fredag d. 9. maj. Der bliver vandaktiviteter og is.",
    unread: true
  },
  {
    id: "msg-103",
    from: "Mette Andersen (Klasselærer, 1.A)",
    subject: "Læsebog glemt",
    date: "2026-05-02",
    preview: "Hej Lars, Freja har glemt sin læsebog i skolen. Den ligger på mit bord.",
    unread: false
  }
];

const MOCK_UGEPLANER = [
  {
    child: "Magnus Jensen",
    class: "3.B",
    week: 19,
    year: 2026,
    days: {
      mandag: ["Dansk: Læseforståelse (s. 42-45)", "Matematik: Brøker - arbejdsark"],
      tirsdag: ["Engelsk: Nutid øvelser", "Natur/teknik: Planteforsøg"],
      onsdag: ["Idræt: Boldspil", "Billedkunst: Akvarelmaling"],
      torsdag: ["Dansk: Diktat", "Historie: Vikingeprojekt fortsat"],
      fredag: ["Musik: Fløjte", "Fri leg", "Tidlig fri kl. 12:30"]
    }
  },
  {
    child: "Freja Jensen",
    class: "1.A",
    week: 19,
    year: 2026,
    days: {
      mandag: ["Dansk: Bogstavjagt", "Matematik: Tal til 20"],
      tirsdag: ["Dansk: Højtlæsning", "Kreativ: Perleplade"],
      onsdag: ["Idræt: Leg i hallen", "Musik: Sang og rytme"],
      torsdag: ["Matematik: Former", "Natur: Tur i skoven"],
      fredag: ["Dansk: Rim og remser", "Fri leg", "SFO fra kl. 12"]
    }
  }
];

// --- MCP Tool simulation ---

function handleToolCall(toolName, args) {
  switch (toolName) {
    case "get_profiles":
      return { profiles: MOCK_PROFILES };
    case "get_calendar":
      return { events: MOCK_CALENDAR };
    case "get_messages":
      return { messages: MOCK_MESSAGES, unread_count: MOCK_MESSAGES.filter(m => m.unread).length };
    case "get_ugeplaner":
      return { ugeplaner: MOCK_UGEPLANER };
    default:
      return { error: `Unknown tool: ${toolName}` };
  }
}

// --- Demo execution ---

function main() {
  console.log("=".repeat(60));
  console.log("  AULA MCP SERVER — Demo with Mock Data");
  console.log("  (Denmark's school platform via Model Context Protocol)");
  console.log("=".repeat(60));
  console.log();

  // Simulate MCP tool calls
  const tools = ["get_profiles", "get_calendar", "get_messages", "get_ugeplaner"];

  for (const tool of tools) {
    console.log(`--- Tool: ${tool} ---`);
    const result = handleToolCall(tool);
    console.log(JSON.stringify(result, null, 2));
    console.log();
  }

  console.log("=".repeat(60));
  console.log("  MCP Server Tools Summary");
  console.log("=".repeat(60));
  console.log();
  console.log("  Tool              | Description");
  console.log("  ------------------|--------------------------------------------");
  console.log("  get_profiles      | List children & parents on the account");
  console.log("  get_calendar      | School events for a date range");
  console.log("  get_messages      | Inbox messages and threads");
  console.log("  get_ugeplaner     | Weekly plans from teachers");
  console.log();
  console.log("To use with real data:");
  console.log("  1. git clone https://github.com/Casperjuel/aula-mcp.git");
  console.log("  2. Add AULA_USERNAME and AULA_PASSWORD to .env");
  console.log("  3. Add MCP server config to ~/.claude.json");
  console.log("  4. Ask Claude: 'What's on my kids' schedule this week?'");
  console.log();
}

main();
