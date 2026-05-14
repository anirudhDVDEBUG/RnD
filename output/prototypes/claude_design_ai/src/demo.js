#!/usr/bin/env node
// Claude Design AI - Interactive Demo
// Shows what the skill produces when triggered with various prompts

const fs = require('fs');
const path = require('path');
const { generateDesignSystem, generateLandingPage } = require('./generator');

const DIVIDER = '─'.repeat(60);

function showBanner() {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║          Claude Design AI  ·  Skill Demo                ║
║   AI-powered UI/UX architect for Claude Code            ║
╚══════════════════════════════════════════════════════════╝
`);
}

function showSkillTriggers() {
  console.log(DIVIDER);
  console.log('SKILL TRIGGER PHRASES (what activates this in Claude Code):');
  console.log(DIVIDER);
  const triggers = [
    '"Convert this screenshot to a React component"',
    '"Generate a Tailwind CSS component from this design"',
    '"Create a design system with dark mode support"',
    '"Build a responsive layout from this wireframe"',
    '"Create an SVG icon set for my project"',
    '"Generate a shadcn/ui compatible button"',
  ];
  triggers.forEach(t => console.log(`  -> ${t}`));
  console.log();
}

function showGeneratedPreview() {
  console.log(DIVIDER);
  console.log('DEMO: Generating a full design system...');
  console.log(DIVIDER);

  const components = generateDesignSystem();
  generateLandingPage();

  // Show a preview of key components
  console.log('\n' + DIVIDER);
  console.log('PREVIEW: Button component (first 30 lines)');
  console.log(DIVIDER);
  const buttonPath = path.join(__dirname, '..', 'output', 'components', 'Button.tsx');
  if (fs.existsSync(buttonPath)) {
    const lines = fs.readFileSync(buttonPath, 'utf-8').split('\n');
    lines.slice(0, 30).forEach((line, i) => {
      console.log(`  ${String(i + 1).padStart(3)} │ ${line}`);
    });
    if (lines.length > 30) console.log(`  ... (${lines.length - 30} more lines)`);
  }

  console.log('\n' + DIVIDER);
  console.log('PREVIEW: DarkModeToggle component (first 25 lines)');
  console.log(DIVIDER);
  const togglePath = path.join(__dirname, '..', 'output', 'theme', 'DarkModeToggle.tsx');
  if (fs.existsSync(togglePath)) {
    const lines = fs.readFileSync(togglePath, 'utf-8').split('\n');
    lines.slice(0, 25).forEach((line, i) => {
      console.log(`  ${String(i + 1).padStart(3)} │ ${line}`);
    });
    if (lines.length > 25) console.log(`  ... (${lines.length - 25} more lines)`);
  }

  console.log('\n' + DIVIDER);
  console.log('DESIGN TOKENS (extracted from generated system)');
  console.log(DIVIDER);
  const tokensPath = path.join(__dirname, '..', 'output', 'design-tokens.json');
  if (fs.existsSync(tokensPath)) {
    const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf-8'));
    console.log('  Colors (primary):');
    Object.entries(tokens.colors.primary).forEach(([k, v]) => {
      console.log(`    ${k.padEnd(4)} ${v}  ${'█'.repeat(3)}`);
    });
    console.log('  Spacing:');
    Object.entries(tokens.spacing).forEach(([k, v]) => {
      console.log(`    ${k.padEnd(4)} ${v}`);
    });
    console.log('  Typography scale:');
    Object.entries(tokens.typography.scale).forEach(([k, v]) => {
      console.log(`    ${k.padEnd(4)} ${v}`);
    });
  }
}

function showOutputTree() {
  console.log('\n' + DIVIDER);
  console.log('OUTPUT FILE TREE');
  console.log(DIVIDER);

  const outputDir = path.join(__dirname, '..', 'output');
  function walk(dir, prefix = '') {
    const entries = fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => {
      if (a.isDirectory() && !b.isDirectory()) return -1;
      if (!a.isDirectory() && b.isDirectory()) return 1;
      return a.name.localeCompare(b.name);
    });
    entries.forEach((entry, idx) => {
      const isLast = idx === entries.length - 1;
      const connector = isLast ? '└── ' : '├── ';
      const childPrefix = isLast ? '    ' : '│   ';
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        console.log(`  ${prefix}${connector}${entry.name}/`);
        walk(fullPath, prefix + childPrefix);
      } else {
        const size = fs.statSync(fullPath).size;
        const sizeStr = size > 1024 ? `${(size / 1024).toFixed(1)}KB` : `${size}B`;
        console.log(`  ${prefix}${connector}${entry.name} (${sizeStr})`);
      }
    });
  }
  console.log('  output/');
  walk(outputDir);
}

function showConclusion() {
  console.log('\n' + DIVIDER);
  console.log('WHAT THIS SKILL DOES IN PRACTICE');
  console.log(DIVIDER);
  console.log(`
  In Claude Code, this skill activates when you say things like:
    "create a design system" or "convert this screenshot to React"

  Claude then generates:
    - TypeScript React components with full props interfaces
    - Tailwind CSS utility classes (responsive + dark mode)
    - Theme provider with localStorage persistence
    - SVG icon components (tree-shakeable)
    - Barrel exports for clean imports
    - tailwind.config.js with custom tokens

  The generated code is production-ready and works with:
    - Next.js, Vite, Create React App
    - shadcn/ui component library
    - Any Tailwind CSS 3.x project
`);
}

// --- Main ---
showBanner();
showSkillTriggers();
showGeneratedPreview();
showOutputTree();
showConclusion();

console.log('Done. See output/ directory for all generated files.\n');
