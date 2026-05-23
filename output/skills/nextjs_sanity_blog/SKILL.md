---
name: nextjs_sanity_blog
description: |
  Scaffolds and builds a complete blog using Next.js and Sanity CMS.
  TRIGGER: user wants to create a blog, build a blog with Next.js, set up Sanity CMS blog, scaffold a blog project, or create a content-driven website.
---

# Next.js + Sanity Blog Builder

A skill for scaffolding and building a production-ready blog using Next.js as the frontend framework and Sanity as the headless CMS.

## When to use

- "Create a blog with Next.js and Sanity"
- "Scaffold a new blog project"
- "Set up a headless CMS blog"
- "Build a content-driven blog website"
- "Create a Next.js blog with a CMS backend"

## How to use

### 1. Initialize the Next.js project

Create a new Next.js app with TypeScript and Tailwind CSS:

```bash
npx create-next-app@latest my-blog --typescript --tailwind --eslint --app --src-dir
cd my-blog
```

### 2. Install Sanity dependencies

Add the Sanity client and required packages:

```bash
npm install next-sanity @sanity/image-url @sanity/vision @portabletext/react
npm install -D sanity @sanity/cli
```

### 3. Set up Sanity Studio

Initialize Sanity within the project:

```bash
npx sanity@latest init --env --create-project "My Blog" --dataset production
```

This creates a `sanity.config.ts` and `.env.local` with your project ID and dataset.

### 4. Define the blog schema

Create `src/sanity/schemaTypes/post.ts`:

```typescript
import { defineField, defineType } from 'sanity'

export const post = defineType({
  name: 'post',
  title: 'Post',
  type: 'document',
  fields: [
    defineField({ name: 'title', type: 'string', validation: (r) => r.required() }),
    defineField({ name: 'slug', type: 'slug', options: { source: 'title' }, validation: (r) => r.required() }),
    defineField({ name: 'publishedAt', type: 'datetime' }),
    defineField({ name: 'excerpt', type: 'text', rows: 3 }),
    defineField({ name: 'mainImage', type: 'image', options: { hotspot: true } }),
    defineField({ name: 'body', type: 'array', of: [{ type: 'block' }, { type: 'image' }] }),
  ],
})
```

Create `src/sanity/schemaTypes/author.ts`:

```typescript
import { defineField, defineType } from 'sanity'

export const author = defineType({
  name: 'author',
  title: 'Author',
  type: 'document',
  fields: [
    defineField({ name: 'name', type: 'string', validation: (r) => r.required() }),
    defineField({ name: 'image', type: 'image' }),
    defineField({ name: 'bio', type: 'text' }),
  ],
})
```

### 5. Configure the Sanity client

Create `src/sanity/lib/client.ts`:

```typescript
import { createClient } from 'next-sanity'

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
  apiVersion: '2024-01-01',
  useCdn: true,
})
```

### 6. Create blog pages

**Blog listing** — `src/app/blog/page.tsx`:
- Query all posts via GROQ: `*[_type == "post"] | order(publishedAt desc)`
- Render a list of posts with title, excerpt, date, and link to detail page.

**Blog detail** — `src/app/blog/[slug]/page.tsx`:
- Query single post by slug: `*[_type == "post" && slug.current == $slug][0]`
- Render post title, image, date, and body using `@portabletext/react`.
- Implement `generateStaticParams` for static generation.

### 7. Embed Sanity Studio (optional)

Mount Sanity Studio at `/studio` by creating `src/app/studio/[[...tool]]/page.tsx`:

```typescript
'use client'
import { NextStudio } from 'next-sanity/studio'
import config from '../../../../sanity.config'

export default function StudioPage() {
  return <NextStudio config={config} />
}
```

### 8. Environment variables

Ensure `.env.local` contains:

```
NEXT_PUBLIC_SANITY_PROJECT_ID=your_project_id
NEXT_PUBLIC_SANITY_DATASET=production
```

### 9. Run the project

```bash
npm run dev
```

Visit `http://localhost:3000/blog` for the blog and `http://localhost:3000/studio` for the CMS.

## References

- Source: [BuildShipGrowRepeat/nextjs-sanity-blog-skill](https://github.com/BuildShipGrowRepeat/nextjs-sanity-blog-skill)
- Listed in: [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [Next.js Documentation](https://nextjs.org/docs)
- [Sanity Documentation](https://www.sanity.io/docs)
- [next-sanity](https://github.com/sanity-io/next-sanity)
