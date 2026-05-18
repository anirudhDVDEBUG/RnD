#!/usr/bin/env node
/**
 * Demo: Anna's Archive Skill Generator Pipeline
 * Simulates the full MCP tool flow with mock data (no API keys needed).
 */

const MOCK_SEARCH_RESULTS = [
  {
    title: "Getting Things Done: The Art of Stress-Free Productivity",
    author: "David Allen",
    format: "PDF",
    size: "4.2 MB",
    year: 2015,
    md5: "a1b2c3d4e5f6",
  },
  {
    title: "Getting Things Done for Teens",
    author: "David Allen, Mike Williams",
    format: "EPUB",
    size: "2.1 MB",
    year: 2018,
    md5: "f6e5d4c3b2a1",
  },
];

const MOCK_EXTRACTED_METHODOLOGY = {
  name: "gtd_productivity",
  core_framework: "Getting Things Done (GTD)",
  steps: [
    {
      phase: "Capture",
      description: "Collect everything that has your attention into trusted external systems",
      actions: [
        "Write down every open loop, task, idea, or commitment",
        "Use an inbox (physical or digital) as the single capture point",
        "Empty your head completely — don't filter or organize yet",
      ],
    },
    {
      phase: "Clarify",
      description: "Process each captured item to determine what it is and what action is required",
      actions: [
        "Ask: Is this actionable? If no → trash, reference, or someday/maybe",
        "If actionable: define the very next physical action",
        "If it takes <2 minutes, do it immediately",
        "If multi-step, define it as a project (desired outcome + next action)",
      ],
    },
    {
      phase: "Organize",
      description: "Put clarified items into appropriate categories and lists",
      actions: [
        "Next Actions list (by context: @computer, @phone, @errands)",
        "Projects list (any outcome requiring >1 action)",
        "Waiting For list (delegated items with expected dates)",
        "Calendar (only date/time-specific commitments)",
        "Someday/Maybe list (future possibilities)",
      ],
    },
    {
      phase: "Reflect",
      description: "Regularly review your system to maintain trust and currency",
      actions: [
        "Weekly Review: process all inboxes to zero",
        "Review all project and next action lists",
        "Update Waiting For items",
        "Assess calendar for upcoming commitments",
        "Trigger new actions from projects",
      ],
    },
    {
      phase: "Engage",
      description: "Choose actions with confidence using contextual criteria",
      actions: [
        "Filter by context (where are you, what tools available)",
        "Filter by time available",
        "Filter by energy level",
        "Filter by priority",
      ],
    },
  ],
  decision_trees: [
    "Item captured → Actionable? → No → Trash / Reference / Someday",
    "Item captured → Actionable? → Yes → <2 min? → Do it now",
    "Item captured → Actionable? → Yes → >2 min → Delegate or Defer",
    "Deferred → Single action → Next Actions list (by context)",
    "Deferred → Multiple actions → Projects list + define next action",
  ],
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function separator(title) {
  console.log(`\n${"=".repeat(60)}`);
  console.log(`  ${title}`);
  console.log(`${"=".repeat(60)}\n`);
}

function generateSkillMd(methodology) {
  return `---
name: ${methodology.name}
description: |
  Apply the ${methodology.core_framework} methodology for stress-free productivity.
  Captures all open loops, clarifies next actions, organizes by context,
  and maintains system trust through weekly reviews.
  Triggers: task management, productivity system, GTD, weekly review, next actions
---

# ${methodology.core_framework} Methodology

Structured productivity system extracted from "Getting Things Done" by David Allen.

## When to use

- "Help me set up a GTD system"
- "Process my inbox using GTD"
- "Run a weekly review"
- "What's my next action for this project?"
- "Organize my tasks by context"

## Methodology

${methodology.steps
  .map(
    (step) => `### Phase: ${step.phase}

${step.description}

${step.actions.map((a) => `- ${a}`).join("\n")}`
  )
  .join("\n\n")}

## Decision Trees

${methodology.decision_trees.map((d) => `- ${d}`).join("\n")}

## Workflow

1. **Daily**: Process inbox to zero using Clarify rules
2. **Before work**: Check calendar + Next Actions for current context
3. **Weekly**: Full Weekly Review (process, review, update, trigger)
4. **When stuck**: Apply the 4-criteria engagement model (context, time, energy, priority)

## References

- Source: "Getting Things Done" by David Allen (2015 revised edition)
- Framework: GTD (Getting Things Done)
`;
}

function auditSkill(skillMd) {
  const checks = [
    { name: "YAML frontmatter present", pass: skillMd.startsWith("---") },
    { name: "Name field defined", pass: skillMd.includes("name:") },
    { name: "Description field defined", pass: skillMd.includes("description:") },
    { name: "When to use section", pass: skillMd.includes("## When to use") },
    { name: "Methodology section", pass: skillMd.includes("## Methodology") },
    { name: "Workflow section", pass: skillMd.includes("## Workflow") },
    { name: "Trigger phrases (3+)", pass: (skillMd.match(/^- "/gm) || []).length >= 3 },
    { name: "Actionable steps present", pass: (skillMd.match(/^- /gm) || []).length >= 10 },
    { name: "References section", pass: skillMd.includes("## References") },
  ];
  return checks;
}

async function main() {
  console.log("Anna's Archive Skill Generator - Demo Pipeline");
  console.log("(Mock mode: no API keys or network access required)\n");

  // Step 1: Search
  separator("STEP 1: Search Anna's Archive");
  console.log('Query: "Getting Things Done David Allen"');
  await sleep(500);
  console.log(`\nFound ${MOCK_SEARCH_RESULTS.length} results:\n`);
  MOCK_SEARCH_RESULTS.forEach((r, i) => {
    console.log(`  [${i + 1}] ${r.title}`);
    console.log(`      Author: ${r.author} | Format: ${r.format} | Size: ${r.size} | Year: ${r.year}`);
  });
  console.log("\n  -> Selected: [1] (best match)");

  // Step 2: Download
  separator("STEP 2: Download Book");
  const selected = MOCK_SEARCH_RESULTS[0];
  console.log(`Downloading: ${selected.title}`);
  console.log(`Format: ${selected.format} | Size: ${selected.size}`);
  await sleep(300);
  console.log("Status: Download complete (simulated)");
  console.log("Extracted text: 85,432 characters from 312 pages");

  // Step 3: Extract methodology via Gemini
  separator("STEP 3: Extract Methodology (Gemini)");
  console.log("Sending extracted text to Gemini for structured methodology extraction...");
  await sleep(400);
  console.log(`\nExtracted framework: ${MOCK_EXTRACTED_METHODOLOGY.core_framework}`);
  console.log(`Phases identified: ${MOCK_EXTRACTED_METHODOLOGY.steps.length}`);
  console.log(`Decision trees: ${MOCK_EXTRACTED_METHODOLOGY.decision_trees.length}`);
  console.log(`\nPhases:`);
  MOCK_EXTRACTED_METHODOLOGY.steps.forEach((s) => {
    console.log(`  - ${s.phase}: ${s.actions.length} actions`);
  });

  // Step 4: Generate SKILL.md
  separator("STEP 4: Generate SKILL.md");
  const skillMd = generateSkillMd(MOCK_EXTRACTED_METHODOLOGY);
  console.log("Generated SKILL.md content:\n");
  console.log("--- BEGIN SKILL.md ---");
  console.log(skillMd);
  console.log("--- END SKILL.md ---");

  // Step 5: Audit
  separator("STEP 5: Audit SKILL.md");
  const auditResults = auditSkill(skillMd);
  let passCount = 0;
  auditResults.forEach((check) => {
    const icon = check.pass ? "PASS" : "FAIL";
    console.log(`  [${icon}] ${check.name}`);
    if (check.pass) passCount++;
  });
  console.log(`\nAudit score: ${passCount}/${auditResults.length} checks passed`);
  console.log(
    passCount === auditResults.length
      ? "Status: SKILL.md is ready for use!"
      : "Status: Some checks failed - review needed."
  );

  // Summary
  separator("PIPELINE COMPLETE");
  console.log("Summary:");
  console.log(`  Book: ${selected.title}`);
  console.log(`  Author: ${selected.author}`);
  console.log(`  Framework extracted: ${MOCK_EXTRACTED_METHODOLOGY.core_framework}`);
  console.log(`  Skill name: ${MOCK_EXTRACTED_METHODOLOGY.name}`);
  console.log(`  Output: SKILL.md (${skillMd.length} bytes)`);
  console.log(`  Audit: ${passCount}/${auditResults.length} passed`);
  console.log(`\nTo use: cp SKILL.md ~/.claude/skills/${MOCK_EXTRACTED_METHODOLOGY.name}/SKILL.md`);
}

main().catch(console.error);
