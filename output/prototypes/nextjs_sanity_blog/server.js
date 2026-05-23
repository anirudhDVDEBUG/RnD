#!/usr/bin/env node
/**
 * server.js — Lightweight mock blog server that renders the scaffolded blog
 * with sample data, demonstrating what the final product looks like.
 * No Sanity API key required — uses embedded mock posts.
 */

const http = require('http');

const MOCK_POSTS = [
  {
    _id: '1',
    title: 'Getting Started with Next.js and Sanity',
    slug: { current: 'getting-started-nextjs-sanity' },
    publishedAt: '2026-05-20T10:00:00Z',
    excerpt: 'Learn how to build a modern blog using Next.js as your frontend framework and Sanity as your headless CMS. This guide walks you through the complete setup.',
    body: [
      'Next.js and Sanity make a powerful combination for content-driven websites. Next.js handles the frontend with server-side rendering and static generation, while Sanity provides a flexible, real-time content management system.',
      'The key advantages include: incremental static regeneration for fast page loads, GROQ queries for flexible content fetching, embedded Sanity Studio for content editing right inside your app, and Portable Text for rich content rendering.',
      'In this post, we walk through setting up schemas, configuring the Sanity client, building blog listing and detail pages, and embedding the studio.'
    ],
    author: 'Alex Chen'
  },
  {
    _id: '2',
    title: 'Mastering GROQ Queries for Blog Content',
    slug: { current: 'mastering-groq-queries' },
    publishedAt: '2026-05-18T14:30:00Z',
    excerpt: 'GROQ is Sanity\'s powerful query language. Learn the patterns you\'ll use most when building a blog — filtering, sorting, projections, and joins.',
    body: [
      'GROQ (Graph-Relational Object Queries) is the query language used by Sanity to fetch content. Unlike REST APIs or even GraphQL, GROQ lets you query deeply nested document graphs with a concise syntax.',
      'Common patterns for blogs include: fetching all posts sorted by date, filtering by category or tag, joining author data, and projecting only the fields you need for listing pages vs. detail pages.',
      'Example: *[_type == "post" && "nextjs" in categories[]->slug.current] | order(publishedAt desc)[0..9]'
    ],
    author: 'Sam Rivera'
  },
  {
    _id: '3',
    title: 'Deploying Your Sanity Blog to Vercel',
    slug: { current: 'deploying-sanity-blog-vercel' },
    publishedAt: '2026-05-15T09:00:00Z',
    excerpt: 'Take your Next.js + Sanity blog to production. This guide covers environment variables, ISR configuration, and webhook-based revalidation.',
    body: [
      'Deploying a Next.js + Sanity blog to Vercel is straightforward. Connect your Git repository, add your Sanity environment variables, and deploy.',
      'For production, you\'ll want to set up Incremental Static Regeneration (ISR) with on-demand revalidation triggered by Sanity webhooks. This gives you the performance of static pages with the freshness of dynamic content.',
      'Don\'t forget to configure your Sanity CORS origins to include your production domain, and set up a read token for draft mode previews.'
    ],
    author: 'Alex Chen'
  }
];

function renderPost(post) {
  return `
    <article style="border-bottom:1px solid #e5e7eb;padding-bottom:24px;margin-bottom:24px;">
      <a href="/blog/${post.slug.current}" style="text-decoration:none;color:inherit;">
        <h2 style="font-size:1.5rem;font-weight:600;margin:0 0 4px;">${post.title}</h2>
      </a>
      <div style="color:#6b7280;font-size:0.875rem;margin-bottom:8px;">
        ${new Date(post.publishedAt).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' })}
        &middot; ${post.author}
      </div>
      <p style="color:#374151;margin:0;">${post.excerpt}</p>
    </article>`;
}

function renderDetailPage(post) {
  return page(`${post.title} — My Blog`, `
    <a href="/blog" style="color:#2563eb;text-decoration:none;">&larr; Back to blog</a>
    <h1 style="font-size:2.5rem;font-weight:700;margin:16px 0 8px;">${post.title}</h1>
    <div style="color:#6b7280;margin-bottom:24px;">
      ${new Date(post.publishedAt).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric' })}
      &middot; ${post.author}
    </div>
    <div style="line-height:1.8;color:#1f2937;">
      ${post.body.map(p => `<p style="margin-bottom:16px;">${p}</p>`).join('')}
    </div>
  `);
}

function page(title, body) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title}</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
           margin: 0; padding: 0; background: #fafafa; color: #111; }
    .container { max-width: 720px; margin: 0 auto; padding: 48px 24px; }
    .badge { display:inline-block; background:#dbeafe; color:#1e40af; font-size:0.75rem;
             padding:2px 8px; border-radius:9999px; margin-bottom:8px; }
    nav { background:#fff; border-bottom:1px solid #e5e7eb; padding:12px 24px; }
    nav a { color:#111; text-decoration:none; font-weight:600; font-size:1.125rem; }
  </style>
</head>
<body>
  <nav><a href="/blog">My Blog</a></nav>
  <div class="container">
    ${body}
  </div>
</body>
</html>`;
}

const PORT = process.env.PORT || 3456;

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (url.pathname === '/' || url.pathname === '/blog') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(page('My Blog', `
      <span class="badge">Mock Data &middot; No API Key Required</span>
      <h1 style="font-size:2.5rem;font-weight:700;margin:8px 0 32px;">Blog</h1>
      ${MOCK_POSTS.map(renderPost).join('')}
    `));
    return;
  }

  const slugMatch = url.pathname.match(/^\/blog\/([a-z0-9-]+)$/);
  if (slugMatch) {
    const post = MOCK_POSTS.find(p => p.slug.current === slugMatch[1]);
    if (post) {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(renderDetailPage(post));
      return;
    }
  }

  res.writeHead(302, { Location: '/blog' });
  res.end();
});

server.listen(PORT, () => {
  console.log(`\n=== Mock Blog Server ===`);
  console.log(`Blog listing:  http://localhost:${PORT}/blog`);
  console.log(`Example post:  http://localhost:${PORT}/blog/getting-started-nextjs-sanity`);
  console.log(`\nServing ${MOCK_POSTS.length} mock posts (no Sanity API key needed)`);
  console.log(`Press Ctrl+C to stop.\n`);
});
