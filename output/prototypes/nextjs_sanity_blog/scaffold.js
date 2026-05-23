#!/usr/bin/env node
/**
 * scaffold.js — Demonstrates what the nextjs_sanity_blog skill generates.
 * Creates a complete Next.js + Sanity blog project structure with all
 * schema definitions, client config, page components, and studio embed.
 */

const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, 'generated-blog');

function write(rel, content) {
  const full = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content.trimStart());
  console.log(`  created  ${rel}`);
}

console.log('\n=== Next.js + Sanity Blog Scaffolder ===\n');
console.log(`Output directory: ${OUT}\n`);

// ── package.json ──
write('package.json', `
{
  "name": "my-blog",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next-sanity": "^7.0.0",
    "@sanity/image-url": "^1.0.0",
    "@sanity/vision": "^3.0.0",
    "@portabletext/react": "^3.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.2.0",
    "sanity": "^3.0.0",
    "@sanity/cli": "^3.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.0.0",
    "postcss": "^8.0.0"
  }
}
`);

// ── .env.local ──
write('.env.local', `
NEXT_PUBLIC_SANITY_PROJECT_ID=your_project_id
NEXT_PUBLIC_SANITY_DATASET=production
`);

// ── Sanity config ──
write('sanity.config.ts', `
import { defineConfig } from 'sanity'
import { structureTool } from 'sanity/structure'
import { visionTool } from '@sanity/vision'
import { schemaTypes } from './src/sanity/schemaTypes'

export default defineConfig({
  name: 'default',
  title: 'My Blog',
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
  plugins: [structureTool(), visionTool()],
  schema: { types: schemaTypes },
})
`);

// ── Schema: Post ──
write('src/sanity/schemaTypes/post.ts', `
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
    defineField({
      name: 'body',
      type: 'array',
      of: [{ type: 'block' }, { type: 'image' }],
    }),
  ],
})
`);

// ── Schema: Author ──
write('src/sanity/schemaTypes/author.ts', `
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
`);

// ── Schema index ──
write('src/sanity/schemaTypes/index.ts', `
import { post } from './post'
import { author } from './author'

export const schemaTypes = [post, author]
`);

// ── Sanity client ──
write('src/sanity/lib/client.ts', `
import { createClient } from 'next-sanity'

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
  apiVersion: '2024-01-01',
  useCdn: true,
})
`);

// ── Image helper ──
write('src/sanity/lib/image.ts', `
import createImageUrlBuilder from '@sanity/image-url'
import { client } from './client'

const builder = createImageUrlBuilder(client)

export function urlFor(source: any) {
  return builder.image(source)
}
`);

// ── GROQ queries ──
write('src/sanity/lib/queries.ts', `
import { groq } from 'next-sanity'

export const postsQuery = groq\`*[_type == "post"] | order(publishedAt desc) {
  _id, title, slug, publishedAt, excerpt, mainImage
}\`

export const postBySlugQuery = groq\`*[_type == "post" && slug.current == $slug][0] {
  _id, title, slug, publishedAt, excerpt, mainImage, body
}\`

export const postSlugsQuery = groq\`*[_type == "post" && defined(slug.current)][].slug.current\`
`);

// ── Blog listing page ──
write('src/app/blog/page.tsx', `
import Link from 'next/link'
import { client } from '@/sanity/lib/client'
import { postsQuery } from '@/sanity/lib/queries'

export const revalidate = 60

export default async function BlogPage() {
  const posts = await client.fetch(postsQuery)

  return (
    <main className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Blog</h1>
      <div className="space-y-8">
        {posts.map((post: any) => (
          <article key={post._id} className="border-b pb-6">
            <Link href={\`/blog/\${post.slug.current}\`}>
              <h2 className="text-2xl font-semibold hover:text-blue-600">
                {post.title}
              </h2>
            </Link>
            {post.publishedAt && (
              <time className="text-gray-500 text-sm">
                {new Date(post.publishedAt).toLocaleDateString()}
              </time>
            )}
            {post.excerpt && <p className="mt-2 text-gray-700">{post.excerpt}</p>}
          </article>
        ))}
      </div>
    </main>
  )
}
`);

// ── Blog detail page ──
write('src/app/blog/[slug]/page.tsx', `
import { client } from '@/sanity/lib/client'
import { postBySlugQuery, postSlugsQuery } from '@/sanity/lib/queries'
import { PortableText } from '@portabletext/react'

export const revalidate = 60

export async function generateStaticParams() {
  const slugs: string[] = await client.fetch(postSlugsQuery)
  return slugs.map((slug) => ({ slug }))
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await client.fetch(postBySlugQuery, { slug: params.slug })

  if (!post) return <div>Post not found</div>

  return (
    <main className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
      {post.publishedAt && (
        <time className="text-gray-500">
          {new Date(post.publishedAt).toLocaleDateString()}
        </time>
      )}
      <div className="prose mt-8">
        <PortableText value={post.body} />
      </div>
    </main>
  )
}
`);

// ── Studio embed ──
write('src/app/studio/[[...tool]]/page.tsx', `
'use client'
import { NextStudio } from 'next-sanity/studio'
import config from '../../../../sanity.config'

export default function StudioPage() {
  return <NextStudio config={config} />
}
`);

// ── Layout ──
write('src/app/layout.tsx', `
import './globals.css'

export const metadata = {
  title: 'My Blog',
  description: 'Built with Next.js and Sanity',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
`);

// ── Globals CSS ──
write('src/app/globals.css', `
@tailwind base;
@tailwind components;
@tailwind utilities;
`);

// ── Tailwind config ──
write('tailwind.config.ts', `
import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: { extend: {} },
  plugins: [],
}
export default config
`);

// ── tsconfig ──
write('tsconfig.json', `
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
`);

// ── Summary ──
const files = [];
function countFiles(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) countFiles(path.join(dir, entry.name));
    else files.push(path.relative(OUT, path.join(dir, entry.name)));
  }
}
countFiles(OUT);

console.log(`\n--- Scaffold complete ---`);
console.log(`Total files generated: ${files.length}`);
console.log(`\nProject structure:`);

// Print tree
const tree = {};
files.sort().forEach(f => {
  const parts = f.split(path.sep);
  let node = tree;
  parts.forEach((p, i) => {
    if (i === parts.length - 1) node[p] = null;
    else { node[p] = node[p] || {}; node = node[p]; }
  });
});

function printTree(node, prefix) {
  const keys = Object.keys(node);
  keys.forEach((k, i) => {
    const last = i === keys.length - 1;
    const connector = last ? '└── ' : '├── ';
    console.log(prefix + connector + k);
    if (node[k]) printTree(node[k], prefix + (last ? '    ' : '│   '));
  });
}
printTree(tree, '');
