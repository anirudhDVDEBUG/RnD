#!/usr/bin/env node
/**
 * Auto Project Builder - Demo
 *
 * Simulates the autonomous project-building pipeline from
 * hongmacho/auto-project-builder. In production the real tool
 * uses Claude Code as the agent; here we demonstrate the
 * pipeline stages and produce a real, runnable Next.js project
 * skeleton on disk.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUTPUT_DIR = path.join(ROOT, "generated_project");

// ── Helpers ──────────────────────────────────────────────────

function log(stage, msg) {
  const colors = {
    IDEA: "\x1b[36m",
    SCAFFOLD: "\x1b[33m",
    UI: "\x1b[35m",
    DB: "\x1b[32m",
    FEATURE: "\x1b[34m",
    VERIFY: "\x1b[32m",
    DONE: "\x1b[1m\x1b[32m",
  };
  const reset = "\x1b[0m";
  const c = colors[stage] || "";
  console.log(`${c}[${stage}]${reset} ${msg}`);
}

function writeFile(relPath, content) {
  const full = path.join(OUTPUT_DIR, relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content);
  log("SCAFFOLD", `  wrote ${relPath}`);
}

// ── Stage 1: Idea Generation ────────────────────────────────

const IDEAS = [
  {
    name: "BookmarkVault",
    slug: "bookmark-vault",
    desc: "A personal bookmark manager with tags, search, and reading-list tracking",
    entities: ["Bookmark", "Tag"],
  },
  {
    name: "MealPlanner",
    slug: "meal-planner",
    desc: "Weekly meal planning app with recipe storage and grocery list generation",
    entities: ["Recipe", "MealPlan"],
  },
  {
    name: "HabitTracker",
    slug: "habit-tracker",
    desc: "Daily habit tracking dashboard with streaks and analytics",
    entities: ["Habit", "Entry"],
  },
  {
    name: "MicroCMS",
    slug: "micro-cms",
    desc: "Lightweight content management system for personal blogs",
    entities: ["Post", "Category"],
  },
  {
    name: "TimeLog",
    slug: "time-log",
    desc: "Simple time-tracking tool for freelancers with project-based reports",
    entities: ["Project", "TimeEntry"],
  },
];

function pickIdea() {
  const idea = IDEAS[Math.floor(Math.random() * IDEAS.length)];
  log("IDEA", `Generated concept: "${idea.name}"`);
  log("IDEA", `  ${idea.desc}`);
  log("IDEA", `  Entities: ${idea.entities.join(", ")}`);
  return idea;
}

// ── Stage 2: Project Scaffolding ────────────────────────────

function scaffold(idea) {
  log("SCAFFOLD", "Creating Next.js project structure...");

  // Clean previous output
  if (fs.existsSync(OUTPUT_DIR)) {
    fs.rmSync(OUTPUT_DIR, { recursive: true });
  }

  // package.json
  writeFile(
    "package.json",
    JSON.stringify(
      {
        name: idea.slug,
        version: "0.1.0",
        private: true,
        scripts: {
          dev: "next dev",
          build: "next build",
          start: "next start",
        },
        dependencies: {
          next: "^14.0.0",
          react: "^18.0.0",
          "react-dom": "^18.0.0",
          "better-sqlite3": "^11.0.0",
          "lucide-react": "^0.300.0",
          "class-variance-authority": "^0.7.0",
          clsx: "^2.0.0",
          "tailwind-merge": "^2.0.0",
        },
        devDependencies: {
          typescript: "^5.0.0",
          "@types/node": "^20.0.0",
          "@types/react": "^18.0.0",
          tailwindcss: "^3.4.0",
          autoprefixer: "^10.0.0",
          postcss: "^8.0.0",
        },
      },
      null,
      2
    )
  );

  // tsconfig
  writeFile(
    "tsconfig.json",
    JSON.stringify(
      {
        compilerOptions: {
          target: "es5",
          lib: ["dom", "dom.iterable", "esnext"],
          allowJs: true,
          skipLibCheck: true,
          strict: true,
          noEmit: true,
          esModuleInterop: true,
          module: "esnext",
          moduleResolution: "bundler",
          resolveJsonModule: true,
          isolatedModules: true,
          jsx: "preserve",
          incremental: true,
          paths: { "@/*": ["./src/*"] },
        },
        include: ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
        exclude: ["node_modules"],
      },
      null,
      2
    )
  );

  // tailwind + postcss
  writeFile(
    "tailwind.config.ts",
    `import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
};
export default config;
`
  );

  writeFile(
    "postcss.config.js",
    `module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };
`
  );

  // next config
  writeFile(
    "next.config.js",
    `/** @type {import('next').NextConfig} */
module.exports = { reactStrictMode: true };
`
  );

  log("SCAFFOLD", "Project skeleton created.");
}

// ── Stage 3: UI Setup (shadcn/ui components) ────────────────

function setupUI(idea) {
  log("UI", "Setting up shadcn/ui components...");

  // globals.css
  writeFile(
    "src/app/globals.css",
    `@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --border: 214.3 31.8% 91.4%;
  --radius: 0.5rem;
}

body {
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  font-family: system-ui, -apple-system, sans-serif;
}
`
  );

  // cn utility
  writeFile(
    "src/lib/utils.ts",
    `import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
`
  );

  // Button component (shadcn-style)
  writeFile(
    "src/components/ui/button.tsx",
    `import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost";
  size?: "default" | "sm" | "lg";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    const base = "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50";
    const variants: Record<string, string> = {
      default: "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] hover:opacity-90",
      outline: "border border-[hsl(var(--border))] bg-transparent hover:bg-[hsl(var(--muted))]",
      ghost: "hover:bg-[hsl(var(--muted))]",
    };
    const sizes: Record<string, string> = {
      default: "h-10 px-4 py-2 text-sm",
      sm: "h-8 px-3 text-xs",
      lg: "h-12 px-6 text-base",
    };
    return (
      <button ref={ref} className={cn(base, variants[variant], sizes[size], className)} {...props} />
    );
  }
);
Button.displayName = "Button";
export { Button };
`
  );

  // Card component
  writeFile(
    "src/components/ui/card.tsx",
    `import * as React from "react";
import { cn } from "@/lib/utils";

export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("rounded-lg border border-[hsl(var(--border))] bg-white p-6 shadow-sm", className)} {...props} />;
}

export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("mb-4", className)} {...props} />;
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn("text-lg font-semibold", className)} {...props} />;
}

export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("text-sm text-[hsl(var(--muted-foreground))]", className)} {...props} />;
}
`
  );

  // Input component
  writeFile(
    "src/components/ui/input.tsx",
    `import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "flex h-10 w-full rounded-md border border-[hsl(var(--border))] bg-white px-3 py-2 text-sm placeholder:text-[hsl(var(--muted-foreground))] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[hsl(var(--primary))]",
        className
      )}
      {...props}
    />
  )
);
Input.displayName = "Input";
export { Input };
`
  );

  log("UI", `  Created: Button, Card, Input components`);
  log("UI", "shadcn/ui setup complete.");
}

// ── Stage 4: Database Layer ─────────────────────────────────

function setupDatabase(idea) {
  log("DB", "Setting up SQLite database layer...");

  const entity1 = idea.entities[0];
  const entity2 = idea.entities[1];
  const t1 = entity1.toLowerCase() + "s";
  const t2 = entity2.toLowerCase() + "s";

  // Database initialization
  writeFile(
    "src/lib/db.ts",
    `import Database from "better-sqlite3";
import path from "path";

const DB_PATH = path.join(process.cwd(), "data.db");

let db: Database.Database;

export function getDb() {
  if (!db) {
    db = new Database(DB_PATH);
    db.pragma("journal_mode = WAL");
    initSchema(db);
  }
  return db;
}

function initSchema(db: Database.Database) {
  db.exec(\`
    CREATE TABLE IF NOT EXISTS ${t1} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS ${t2} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      ${entity1.toLowerCase()}_id INTEGER REFERENCES ${t1}(id),
      created_at TEXT DEFAULT (datetime('now'))
    );
  \`);

  // Seed data if empty
  const count = db.prepare("SELECT COUNT(*) as c FROM ${t1}").get() as any;
  if (count.c === 0) {
    const insert = db.prepare("INSERT INTO ${t1} (title, description) VALUES (?, ?)");
    insert.run("Sample ${entity1} 1", "Auto-generated sample entry");
    insert.run("Sample ${entity1} 2", "Another auto-generated entry");
    insert.run("Sample ${entity1} 3", "Third auto-generated entry");
  }
}
`
  );

  log("DB", `  Schema: ${t1}, ${t2}`);
  log("DB", "  Seed data: 3 sample rows");
  log("DB", "Database layer complete.");
}

// ── Stage 5: Feature Implementation ─────────────────────────

function buildFeatures(idea) {
  log("FEATURE", "Building pages, API routes, and components...");

  const entity1 = idea.entities[0];
  const t1 = entity1.toLowerCase() + "s";

  // Layout
  writeFile(
    "src/app/layout.tsx",
    `import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "${idea.name}",
  description: "${idea.desc}",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-[hsl(var(--border))] px-6 py-4">
          <h1 className="text-xl font-bold">${idea.name}</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))]">${idea.desc}</p>
        </header>
        <main className="mx-auto max-w-4xl p-6">{children}</main>
      </body>
    </html>
  );
}
`
  );

  // Home page
  writeFile(
    "src/app/page.tsx",
    `import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

async function get${entity1}s() {
  // In production this fetches from the API route / DB
  return [
    { id: 1, title: "Sample ${entity1} 1", description: "Auto-generated sample entry" },
    { id: 2, title: "Sample ${entity1} 2", description: "Another auto-generated entry" },
    { id: 3, title: "Sample ${entity1} 3", description: "Third auto-generated entry" },
  ];
}

export default async function Home() {
  const items = await get${entity1}s();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Your ${entity1}s</h2>
        <Button>Add ${entity1}</Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <Card key={item.id}>
            <CardHeader>
              <CardTitle>{item.title}</CardTitle>
            </CardHeader>
            <CardContent>{item.description}</CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
`
  );

  // API route
  writeFile(
    "src/app/api/${t1}/route.ts",
    `import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET() {
  const db = getDb();
  const rows = db.prepare("SELECT * FROM ${t1} ORDER BY created_at DESC").all();
  return NextResponse.json(rows);
}

export async function POST(request: Request) {
  const body = await request.json();
  const db = getDb();
  const stmt = db.prepare("INSERT INTO ${t1} (title, description) VALUES (?, ?)");
  const result = stmt.run(body.title, body.description || "");
  return NextResponse.json({ id: result.lastInsertRowid }, { status: 201 });
}
`
  );

  log("FEATURE", `  Pages: layout.tsx, page.tsx`);
  log("FEATURE", `  API: /api/${t1} (GET, POST)`);
  log("FEATURE", `  Components: Button, Card, Input`);
  log("FEATURE", "Feature implementation complete.");
}

// ── Stage 6: Verification ───────────────────────────────────

function verify(idea) {
  log("VERIFY", "Running verification checks...");

  const required = [
    "package.json",
    "tsconfig.json",
    "next.config.js",
    "tailwind.config.ts",
    "src/app/layout.tsx",
    "src/app/page.tsx",
    "src/lib/db.ts",
    "src/lib/utils.ts",
    "src/components/ui/button.tsx",
    "src/components/ui/card.tsx",
    "src/components/ui/input.tsx",
  ];

  let ok = 0;
  let fail = 0;
  for (const f of required) {
    const full = path.join(OUTPUT_DIR, f);
    if (fs.existsSync(full)) {
      ok++;
    } else {
      log("VERIFY", `  MISSING: ${f}`);
      fail++;
    }
  }

  log("VERIFY", `  ${ok}/${required.length} files present`);
  if (fail === 0) {
    log("VERIFY", "All checks passed.");
  }
  return fail === 0;
}

// ── Main Pipeline ───────────────────────────────────────────

function main() {
  console.log("");
  console.log(
    "\x1b[1m========================================\x1b[0m"
  );
  console.log(
    "\x1b[1m  Auto Project Builder (Next.js Demo)  \x1b[0m"
  );
  console.log(
    "\x1b[1m========================================\x1b[0m"
  );
  console.log("");

  const idea = pickIdea();
  console.log("");

  scaffold(idea);
  console.log("");

  setupUI(idea);
  console.log("");

  setupDatabase(idea);
  console.log("");

  buildFeatures(idea);
  console.log("");

  const ok = verify(idea);
  console.log("");

  if (ok) {
    log("DONE", `Project "${idea.name}" generated successfully!`);
    log("DONE", `Output directory: ${OUTPUT_DIR}`);
    console.log("");
    console.log("To run the generated project:");
    console.log(`  cd ${OUTPUT_DIR}`);
    console.log("  npm install");
    console.log("  npm run dev");
    console.log("");
  }

  // Print file tree
  console.log("\x1b[1mGenerated file tree:\x1b[0m");
  printTree(OUTPUT_DIR, "");
  console.log("");

  return ok ? 0 : 1;
}

function printTree(dir, prefix) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  entries.forEach((entry, i) => {
    const isLast = i === entries.length - 1;
    const connector = isLast ? "└── " : "├── ";
    const childPrefix = isLast ? "    " : "│   ";
    console.log(`${prefix}${connector}${entry.name}`);
    if (entry.isDirectory()) {
      printTree(path.join(dir, entry.name), prefix + childPrefix);
    }
  });
}

process.exit(main());
