# How to Use: Next.js + Sanity Blog Skill

## Install the Skill

This is a **Claude Code skill** (not an MCP server). Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/nextjs_sanity_blog
# Copy the SKILL.md from this repo (or the source repo) into that folder:
cp SKILL.md ~/.claude/skills/nextjs_sanity_blog/SKILL.md
```

Claude Code will auto-detect the skill on next launch.

### Trigger Phrases

Any of these will activate the skill:

- "Create a blog with Next.js and Sanity"
- "Scaffold a new blog project"
- "Set up a headless CMS blog"
- "Build a content-driven blog website"
- "Create a Next.js blog with a CMS backend"

## Prerequisites (for real usage)

- Node.js 18+
- A free [Sanity.io](https://www.sanity.io/) account (for the CMS backend)
- npm or pnpm

## First 60 Seconds

**Step 1:** Open Claude Code and type:

```
Create a blog with Next.js and Sanity
```

**Step 2:** Claude scaffolds the project. You'll see output like:

```
npx create-next-app@latest my-blog --typescript --tailwind --eslint --app --src-dir
npm install next-sanity @sanity/image-url @portabletext/react
npx sanity@latest init --env --create-project "My Blog" --dataset production
```

**Step 3:** Claude generates schemas (`post.ts`, `author.ts`), Sanity client config, GROQ queries, blog listing/detail pages, and an embedded Studio route.

**Step 4:** Run the result:

```bash
cd my-blog
npm run dev
# Blog:   http://localhost:3000/blog
# Studio: http://localhost:3000/studio
```

## Running This Demo (No API Key Needed)

This repo includes a standalone demo that shows the scaffold output and serves a mock blog:

```bash
bash run.sh
```

Or run the parts separately:

```bash
node scaffold.js     # Generate the project structure into ./generated-blog/
node server.js       # Serve a mock blog preview at http://localhost:3456/blog
```

The mock server runs with sample posts -- no Sanity account required.

## What Gets Generated

```
my-blog/
  sanity.config.ts              # Sanity Studio configuration
  src/
    sanity/
      schemaTypes/
        post.ts                 # Blog post document schema
        author.ts               # Author document schema
        index.ts                # Schema registry
      lib/
        client.ts               # Sanity client (GROQ fetcher)
        image.ts                # Image URL builder helper
        queries.ts              # Reusable GROQ queries
    app/
      layout.tsx                # Root layout with metadata
      globals.css               # Tailwind imports
      blog/
        page.tsx                # Blog listing (sorted by date)
        [slug]/
          page.tsx              # Blog detail (Portable Text body)
      studio/
        [[...tool]]/
          page.tsx              # Embedded Sanity Studio
  .env.local                    # Sanity project ID + dataset
  tailwind.config.ts
  tsconfig.json
  package.json
```
