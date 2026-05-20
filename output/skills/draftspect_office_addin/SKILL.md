---
name: draftspect_office_addin
description: |
  Build Electron-based Office add-ins (Word and Excel) powered by Claude Code.
  TRIGGER when: user wants to create an Office add-in with Claude Code, integrate Claude into Word or Excel, build a document chat sidebar, or use Office.js with an AI agent.
  DO NOT TRIGGER when: user is working on generic Electron apps without Office integration, or using Office APIs without AI features.
---

# Draftspect: Office Add-Ins Powered by Claude Code

Build local Office add-ins (Word & Excel) that let users chat with Claude Code directly inside their documents. The add-in reads and edits the active document and can pull in local folders/files as context.

## When to use

- "Create a Word add-in that uses Claude to edit documents"
- "Build an Excel sidebar that chats with Claude Code"
- "I want an Office add-in powered by Claude Code"
- "How do I integrate Claude Code into Microsoft Office?"
- "Build a document assistant that reads and edits Word/Excel files"

## How to use

### 1. Project Setup

Scaffold an Electron + Office.js project:

```bash
mkdir my-office-addin && cd my-office-addin
npm init -y
npm install electron office-addin-dev-certs
```

Create the manifest XML for Word or Excel sideload:

```xml
<!-- manifest.xml -->
<OfficeApp xmlns="http://schemas.microsoft.com/office/appforoffice/1.1" xsi:type="TaskPaneApp">
  <Id>your-uuid-here</Id>
  <Version>1.0.0</Version>
  <ProviderName>YourName</ProviderName>
  <DefaultLocale>en-US</DefaultLocale>
  <DisplayName DefaultValue="Draftspect" />
  <Description DefaultValue="Chat with Claude Code inside Office" />
  <Hosts>
    <Host Name="Document" />  <!-- Word -->
    <Host Name="Workbook" />  <!-- Excel -->
  </Hosts>
  <DefaultSettings>
    <SourceLocation DefaultValue="https://localhost:3000/taskpane.html" />
  </DefaultSettings>
  <Permissions>ReadWriteDocument</Permissions>
</OfficeApp>
```

### 2. Core Architecture

The add-in has three layers:

- **Taskpane UI** — HTML/JS sidebar rendered in Office, provides chat interface
- **Local Server** — Electron or Node process that spawns and manages Claude Code CLI
- **Office.js Bridge** — reads/writes document content via the Office JavaScript API

### 3. Reading Document Content (Word)

```javascript
async function getDocumentText() {
  return Word.run(async (context) => {
    const body = context.document.body;
    body.load("text");
    await context.sync();
    return body.text;
  });
}
```

### 4. Reading Document Content (Excel)

```javascript
async function getSheetData() {
  return Excel.run(async (context) => {
    const range = context.workbook.getSelectedRange();
    range.load("values");
    await context.sync();
    return range.values;
  });
}
```

### 5. Writing Back to Documents

```javascript
// Word: insert or replace text
async function insertText(text) {
  return Word.run(async (context) => {
    const body = context.document.body;
    body.insertText(text, Word.InsertLocation.replace);
    await context.sync();
  });
}

// Excel: write values to a range
async function writeToRange(values) {
  return Excel.run(async (context) => {
    const sheet = context.workbook.worksheets.getActiveWorksheet();
    const range = sheet.getRange("A1").getResizedRange(
      values.length - 1, values[0].length - 1
    );
    range.values = values;
    await context.sync();
  });
}
```

### 6. Spawning Claude Code as Backend

Use `child_process` to run Claude Code CLI and pipe document context:

```javascript
const { spawn } = require("child_process");

function startClaudeSession(contextPaths) {
  const args = ["--print", "--verbose"];
  const proc = spawn("claude", args, {
    cwd: contextPaths[0],
    stdio: ["pipe", "pipe", "pipe"],
  });
  return proc;
}
```

### 7. Connecting Context Folders

Allow users to point the add-in at local folders (notes, drafts, repos) which get passed as working directory or appended to the prompt context. The add-in configuration stores these paths and injects them when spawning Claude.

### 8. Key Considerations

- **Sideloading**: For development, sideload the manifest via Office's "Insert > My Add-ins > Upload" or use `office-addin-debugging` tools
- **HTTPS**: Office.js requires HTTPS even locally — use `office-addin-dev-certs` to generate local certificates
- **Permissions**: The manifest must declare `ReadWriteDocument` for full document access
- **MCP & Skills**: Since Claude Code runs locally, all configured MCP servers, skills, and CLAUDE.md files on the user's machine are available to the agent
- **Security**: The add-in runs entirely locally — no data leaves the machine except through Claude's normal API calls

## References

- **Source Repository**: https://github.com/LeonardHope/Draftspect-Add-Ins-for-Word-and-Excel-Powered-by-Claude-Code
- [Office Add-ins Documentation](https://learn.microsoft.com/en-us/office/dev/add-ins/)
- [Office.js API Reference](https://learn.microsoft.com/en-us/javascript/api/overview)
- [Claude Code CLI Documentation](https://docs.anthropic.com/en/docs/claude-code)
