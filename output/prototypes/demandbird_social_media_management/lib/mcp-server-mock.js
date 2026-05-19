/**
 * Mock MCP server simulation for DemandBird.
 * Shows the tools that the real DemandBird MCP server would expose.
 */

const MCP_TOOLS = [
  {
    name: 'demandbird_list_platforms',
    description: 'List all connected social media platforms and their status',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'demandbird_create_post',
    description: 'Create a new social media post for one or more platforms',
    inputSchema: {
      type: 'object',
      properties: {
        content: { type: 'string', description: 'Post content' },
        platforms: { type: 'array', items: { type: 'string' }, description: 'Target platforms' },
        scheduledAt: { type: 'string', description: 'ISO 8601 scheduled time (optional)' },
      },
      required: ['content'],
    },
  },
  {
    name: 'demandbird_list_posts',
    description: 'List posts filtered by status (draft, scheduled, published)',
    inputSchema: {
      type: 'object',
      properties: {
        status: { type: 'string', enum: ['draft', 'scheduled', 'published'] },
      },
    },
  },
  {
    name: 'demandbird_repurpose',
    description: 'Repurpose a post into platform-specific variants',
    inputSchema: {
      type: 'object',
      properties: {
        postId: { type: 'string' },
        targetPlatforms: { type: 'array', items: { type: 'string' } },
      },
      required: ['postId', 'targetPlatforms'],
    },
  },
  {
    name: 'demandbird_analytics',
    description: 'Get engagement analytics across all platforms',
    inputSchema: { type: 'object', properties: {} },
  },
];

function listMcpTools() {
  return MCP_TOOLS;
}

module.exports = { listMcpTools, MCP_TOOLS };
