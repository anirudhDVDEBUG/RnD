#!/usr/bin/env node
/**
 * MarkPDF Demo — Converts Markdown to styled HTML (document + slides).
 * Demonstrates what the MarkPDF MCP server does under the hood.
 *
 * Usage: node convert.js [input.md] [--slides] [--output path]
 */

const fs = require("fs");
const path = require("path");
const { marked } = require("marked");
const hljs = require("highlight.js");

// ---------- Marked configuration with syntax highlighting ----------

marked.setOptions({
  gfm: true,
  breaks: false,
  renderer: (() => {
    const renderer = new marked.Renderer();
    renderer.code = function ({ text, lang }) {
      const language = lang && hljs.getLanguage(lang) ? lang : "plaintext";
      const highlighted = hljs.highlight(text, { language }).value;
      return `<pre><code class="hljs language-${language}">${highlighted}</code></pre>`;
    };
    return renderer;
  })(),
});

// ---------- CSS Themes ----------

const DOCUMENT_CSS = `
  :root { --accent: #2563eb; --text: #1e293b; --muted: #64748b; --bg: #ffffff; --border: #e2e8f0; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; color: var(--text);
         max-width: 800px; margin: 0 auto; padding: 48px 32px; line-height: 1.7; background: var(--bg); }
  h1 { font-size: 2rem; margin: 1.5em 0 0.5em; color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 0.3em; }
  h2 { font-size: 1.5rem; margin: 1.3em 0 0.4em; color: var(--text); }
  h3 { font-size: 1.2rem; margin: 1.1em 0 0.3em; color: var(--muted); }
  p { margin: 0.8em 0; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  strong { color: var(--text); }
  blockquote { border-left: 4px solid var(--accent); padding: 0.8em 1.2em; margin: 1em 0;
               background: #f1f5f9; border-radius: 0 6px 6px 0; color: var(--muted); font-style: italic; }
  table { width: 100%; border-collapse: collapse; margin: 1em 0; }
  th { background: var(--accent); color: white; padding: 10px 14px; text-align: left; font-weight: 600; }
  td { padding: 10px 14px; border-bottom: 1px solid var(--border); }
  tr:nth-child(even) td { background: #f8fafc; }
  pre { background: #1e293b; color: #e2e8f0; padding: 16px 20px; border-radius: 8px; overflow-x: auto; margin: 1em 0; }
  code { font-family: 'Fira Code', 'Cascadia Code', monospace; font-size: 0.9em; }
  p code { background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: var(--accent); }
  ul, ol { margin: 0.6em 0; padding-left: 1.6em; }
  li { margin: 0.3em 0; }
  li input[type="checkbox"] { margin-right: 0.5em; }
  hr { border: none; border-top: 2px solid var(--border); margin: 2em 0; }
  img { max-width: 100%; border-radius: 8px; }
  em { color: var(--muted); }
  @media print { body { max-width: none; padding: 0; } }
`;

const SLIDES_CSS = `
  :root { --accent: #2563eb; --text: #1e293b; --bg: #ffffff; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #0f172a; }
  .slide { width: 960px; min-height: 540px; margin: 32px auto; padding: 60px 72px;
           background: var(--bg); border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
           display: flex; flex-direction: column; justify-content: center; page-break-after: always; }
  .slide:first-child { text-align: center; }
  h1 { font-size: 2.4rem; color: var(--accent); margin-bottom: 0.4em; }
  h2 { font-size: 1.8rem; color: var(--text); margin-bottom: 0.6em; }
  h3 { font-size: 1.3rem; color: #64748b; margin-bottom: 0.4em; }
  p { font-size: 1.1rem; line-height: 1.6; margin: 0.5em 0; color: var(--text); }
  ul, ol { font-size: 1.1rem; line-height: 1.8; padding-left: 1.5em; }
  li { margin: 0.3em 0; }
  table { width: 100%; border-collapse: collapse; margin: 1em 0; }
  th { background: var(--accent); color: white; padding: 10px 14px; text-align: left; }
  td { padding: 10px 14px; border-bottom: 1px solid #e2e8f0; }
  tr:nth-child(even) td { background: #f8fafc; }
  strong { color: var(--accent); }
  pre { background: #1e293b; color: #e2e8f0; padding: 14px 18px; border-radius: 8px; overflow-x: auto; font-size: 0.85rem; }
  code { font-family: 'Fira Code', monospace; }
  @media print { body { background: white; } .slide { box-shadow: none; margin: 0; border-radius: 0; } }
`;

// ---------- Conversion functions ----------

function mdToHtmlDocument(mdContent, title) {
  const body = marked.parse(mdContent);
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(title)}</title>
  <style>${DOCUMENT_CSS}</style>
</head>
<body>
${body}
</body>
</html>`;
}

function mdToSlides(mdContent, title) {
  const slides = mdContent.split(/\n---\n/).map((s) => s.trim()).filter(Boolean);
  const slideHtml = slides
    .map((slide) => `  <div class="slide">\n${marked.parse(slide)}\n  </div>`)
    .join("\n\n");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(title)}</title>
  <style>${SLIDES_CSS}</style>
</head>
<body>
${slideHtml}
</body>
</html>`;
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// ---------- CLI ----------

function main() {
  const args = process.argv.slice(2);
  const isSlides = args.includes("--slides");
  const outputIdx = args.indexOf("--output");
  let outputPath = outputIdx !== -1 ? args[outputIdx + 1] : null;
  const inputFile = args.find((a) => !a.startsWith("--") && a !== outputPath) || "sample.md";

  const inputPath = path.resolve(inputFile);
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: File not found: ${inputPath}`);
    process.exit(1);
  }

  const mdContent = fs.readFileSync(inputPath, "utf-8");
  const baseName = path.basename(inputFile, path.extname(inputFile));
  const title = baseName.replace(/[_-]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  let html, defaultOutput;
  if (isSlides) {
    html = mdToSlides(mdContent, title);
    defaultOutput = path.join("output", `${baseName}_slides.html`);
  } else {
    html = mdToHtmlDocument(mdContent, title);
    defaultOutput = path.join("output", `${baseName}.html`);
  }

  outputPath = outputPath || defaultOutput;
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputPath, html);

  const stats = {
    input: inputFile,
    format: isSlides ? "slides" : "document",
    output: outputPath,
    size: `${(Buffer.byteLength(html) / 1024).toFixed(1)} KB`,
    wordCount: mdContent.split(/\s+/).filter(Boolean).length,
  };

  if (isSlides) {
    stats.slideCount = mdContent.split(/\n---\n/).filter((s) => s.trim()).length;
  }

  console.log("\n┌─────────────────────────────────────────────┐");
  console.log("│  MarkPDF Demo — Markdown → Styled Output    │");
  console.log("└─────────────────────────────────────────────┘\n");
  console.log(`  Input:       ${stats.input}`);
  console.log(`  Format:      ${stats.format}`);
  console.log(`  Words:       ${stats.wordCount}`);
  if (stats.slideCount) console.log(`  Slides:      ${stats.slideCount}`);
  console.log(`  Output:      ${stats.output}`);
  console.log(`  Size:        ${stats.size}`);
  console.log(`\n  ✓ Conversion complete!\n`);

  return stats;
}

// Allow use as module or CLI
if (require.main === module) {
  main();
} else {
  module.exports = { mdToHtmlDocument, mdToSlides };
}
