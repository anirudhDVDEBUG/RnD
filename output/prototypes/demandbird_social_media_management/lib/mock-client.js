/**
 * Mock DemandBird API client for demo purposes.
 * Simulates the DemandBird API without requiring real credentials.
 */

const PLATFORMS = ['twitter', 'linkedin', 'bluesky', 'threads', 'youtube', 'substack'];

const MOCK_POSTS = [
  {
    id: 'post_001',
    content: 'Excited to announce our new AI-powered content pipeline! #AI #MarTech',
    platforms: ['twitter', 'linkedin'],
    status: 'published',
    scheduledAt: '2026-05-19T09:00:00Z',
    publishedAt: '2026-05-19T09:00:12Z',
    engagement: { likes: 142, shares: 38, comments: 12, impressions: 4820 },
  },
  {
    id: 'post_002',
    content: 'How we scaled our social presence across 6 platforms in 30 days — a thread.',
    platforms: ['twitter'],
    status: 'published',
    scheduledAt: '2026-05-18T14:30:00Z',
    publishedAt: '2026-05-18T14:30:05Z',
    engagement: { likes: 87, shares: 24, comments: 9, impressions: 3100 },
  },
  {
    id: 'post_003',
    content: 'Deep dive: Why unified social media management matters for B2B teams.',
    platforms: ['linkedin', 'substack'],
    status: 'scheduled',
    scheduledAt: '2026-05-20T11:00:00Z',
    publishedAt: null,
    engagement: null,
  },
  {
    id: 'post_004',
    content: 'Quick tip: Use content repurposing to 3x your reach without 3x the effort.',
    platforms: ['twitter', 'bluesky', 'threads'],
    status: 'scheduled',
    scheduledAt: '2026-05-21T08:00:00Z',
    publishedAt: null,
    engagement: null,
  },
  {
    id: 'post_005',
    content: 'Behind the scenes of our latest product video — shot entirely with AI assistance.',
    platforms: ['youtube', 'linkedin'],
    status: 'draft',
    scheduledAt: null,
    publishedAt: null,
    engagement: null,
  },
];

class DemandBirdClient {
  constructor(apiKey) {
    this.apiKey = apiKey || 'demo-key';
    this.posts = JSON.parse(JSON.stringify(MOCK_POSTS));
  }

  async listPlatforms() {
    return PLATFORMS.map(p => ({
      name: p,
      connected: true,
      handle: `@demo_${p}`,
    }));
  }

  async listPosts({ status } = {}) {
    if (status) {
      return this.posts.filter(p => p.status === status);
    }
    return this.posts;
  }

  async createPost({ content, platforms, scheduledAt }) {
    const post = {
      id: `post_${String(this.posts.length + 1).padStart(3, '0')}`,
      content,
      platforms: platforms || ['twitter'],
      status: scheduledAt ? 'scheduled' : 'draft',
      scheduledAt: scheduledAt || null,
      publishedAt: null,
      engagement: null,
    };
    this.posts.push(post);
    return post;
  }

  async repurposePost(postId, targetPlatforms) {
    const original = this.posts.find(p => p.id === postId);
    if (!original) throw new Error(`Post ${postId} not found`);

    const variants = targetPlatforms.map(platform => {
      let adapted = original.content;
      switch (platform) {
        case 'twitter':
          adapted = adapted.length > 280 ? adapted.slice(0, 277) + '...' : adapted;
          break;
        case 'linkedin':
          adapted = `${adapted}\n\n#ProfessionalGrowth #Industry`;
          break;
        case 'bluesky':
          adapted = adapted.replace(/#\w+/g, '').trim();
          break;
        case 'threads':
          adapted = `${adapted} [thread]`;
          break;
        case 'substack':
          adapted = `## ${adapted.split('.')[0]}\n\n${adapted}`;
          break;
        case 'youtube':
          adapted = `[Video description] ${adapted}`;
          break;
      }
      return { platform, content: adapted, status: 'draft' };
    });

    return { originalId: postId, variants };
  }

  async getAnalytics() {
    const published = this.posts.filter(p => p.engagement);
    const totals = published.reduce(
      (acc, p) => {
        acc.likes += p.engagement.likes;
        acc.shares += p.engagement.shares;
        acc.comments += p.engagement.comments;
        acc.impressions += p.engagement.impressions;
        return acc;
      },
      { likes: 0, shares: 0, comments: 0, impressions: 0 }
    );

    const platformBreakdown = {};
    for (const post of published) {
      for (const plat of post.platforms) {
        if (!platformBreakdown[plat]) {
          platformBreakdown[plat] = { posts: 0, impressions: 0 };
        }
        platformBreakdown[plat].posts += 1;
        platformBreakdown[plat].impressions += Math.round(
          post.engagement.impressions / post.platforms.length
        );
      }
    }

    return {
      totalPosts: published.length,
      ...totals,
      engagementRate: ((totals.likes + totals.shares + totals.comments) / totals.impressions * 100).toFixed(2) + '%',
      platformBreakdown,
    };
  }
}

module.exports = { DemandBirdClient, PLATFORMS };
