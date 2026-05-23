# Tech Details: Next.js + Sanity Blog Skill

## What It Does

This Claude Code skill is a code-generation template. When triggered, Claude follows a structured recipe to scaffold a complete blog application using Next.js 14 (App Router) for the frontend and Sanity v3 as the headless CMS. It generates TypeScript source files, Sanity schema definitions, a configured client, GROQ queries, and React page components -- producing a working blog that supports static generation with incremental revalidation.

The skill does not run any persistent service or call any AI model. It instructs Claude to execute shell commands (`create-next-app`, `npm install`, `sanity init`) and write source files in a specific order.

## Architecture

### Data Flow

```
Sanity Studio (browser, /studio)
    |
    v
Sanity Cloud (hosted content lake)
    |  <-- GROQ queries over HTTPS
    v
Next.js App (SSR / ISR)
    |
    v
Blog pages rendered to browser
```

### Key Files and Their Roles

| File | Purpose |
|------|---------|
| `sanity.config.ts` | Registers schema types, plugins (structure + vision), and project credentials |
| `src/sanity/schemaTypes/post.ts` | Defines the `post` document: title, slug, date, excerpt, image, Portable Text body |
| `src/sanity/schemaTypes/author.ts` | Defines the `author` document: name, image, bio |
| `src/sanity/lib/client.ts` | Creates the `next-sanity` client with project ID, dataset, API version, CDN toggle |
| `src/sanity/lib/queries.ts` | GROQ queries: list all posts (sorted by date), fetch single post by slug, get all slugs for static params |
| `src/app/blog/page.tsx` | Server component -- fetches all posts, renders listing with title/excerpt/date links |
| `src/app/blog/[slug]/page.tsx` | Server component -- fetches single post, renders Portable Text body via `@portabletext/react`, implements `generateStaticParams` |
| `src/app/studio/[[...tool]]/page.tsx` | Client component -- embeds full Sanity Studio via `next-sanity/studio` |

### Dependencies

- **next-sanity** -- Sanity client + studio integration for Next.js
- **@sanity/image-url** -- Builds CDN URLs for Sanity image assets
- **@portabletext/react** -- Renders Sanity's Portable Text (rich text) as React components
- **sanity** (devDep) -- Sanity Studio v3 runtime
- **tailwindcss** -- Utility-first CSS framework

### Content Model

Two document types:

- **Post**: title (string, required), slug (slug, sourced from title), publishedAt (datetime), excerpt (text), mainImage (image with hotspot), body (array of blocks + images)
- **Author**: name (string, required), image (image), bio (text)

The skill does not create a category/tag schema or link posts to authors. These are left as natural follow-up tasks.

## Limitations

- **No author-post relationship**: Posts don't reference authors. You'd add a `reference` field to connect them.
- **No categories/tags**: No taxonomy schema is generated. You'd define a `category` type and add a reference array to posts.
- **No draft preview mode**: The skill sets up `useCdn: true` for production reads but doesn't configure Next.js Draft Mode or a preview secret.
- **No SEO metadata**: No `generateMetadata` function for Open Graph tags, canonical URLs, or structured data.
- **No pagination**: The blog listing fetches all posts. For large blogs, you'd add GROQ slice operators and pagination UI.
- **No image optimization**: Uses `@sanity/image-url` for URLs but doesn't integrate with Next.js `<Image>` component for automatic optimization.
- **Requires a Sanity account**: The Sanity project ID must be obtained by running `sanity init`, which requires a (free) Sanity account.

## Why It Might Matter

**Content-driven lead-gen sites**: Blog + CMS is the backbone of inbound marketing. This skill lets a Claude-driven agent spin up a content site in minutes -- useful for agent factories that produce lead-gen properties or niche content sites at scale.

**Marketing teams**: Non-technical marketers can ask Claude to "create a blog" and get a working CMS-backed site without hiring a developer. The embedded Sanity Studio means content editing happens at `/studio` with no separate dashboard.

**Rapid prototyping**: For anyone building Claude-driven products, this demonstrates the "scaffold a full-stack app from a trigger phrase" pattern -- the same approach works for e-commerce, dashboards, or documentation sites.
