---
name: content_engine_social_media
description: |
  Agentic skill that creates social media content end-to-end: generates 5 channel-adapted pieces from a single topic/idea, creates an AI-generated image via fal-ai (nano-banana-2), and auto-publishes via Upload-Post. One conversation, zero n8n nodes.
  Triggers: "create social media content", "generate posts for all channels", "content engine", "social media campaign", "auto-publish content"
---

# Content Engine – Social Media Content Creation Skill

Agentic Claude Code skill that creates social media content end-to-end: 5 channel-adapted pieces + AI-generated image (nano-banana-2) + auto-publish via Upload-Post. One conversation, zero n8n nodes.

## When to use

- "Create social media content about [topic]"
- "Generate posts for all my social channels"
- "Run the content engine for [product/idea]"
- "Create a social media campaign with images"
- "Auto-publish content across platforms"

## How to use

### Prerequisites

1. **fal-ai API key** – Set `FAL_KEY` environment variable for AI image generation (nano-banana-2 model).
2. **Groq API key** – Set `GROQ_API_KEY` environment variable if using Groq for fast LLM inference.
3. **Upload-Post credentials** – Configure upload-post for auto-publishing to social platforms.
4. **Python 3.10+** – The skill uses Python tooling.

### Workflow Steps

1. **Topic Input**: Provide a topic, idea, product, or content brief.
2. **Content Generation**: The skill generates 5 channel-adapted content pieces tailored for different social media platforms (e.g., Twitter/X, LinkedIn, Instagram, Facebook, blog/newsletter).
3. **Image Generation**: An AI-generated image is created using fal-ai's nano-banana-2 model to accompany the content.
4. **Review**: Review and optionally edit the generated content and image before publishing.
5. **Auto-Publish**: Content is automatically published to configured channels via Upload-Post.

### Configuration

Set the following environment variables:

```bash
export FAL_KEY="your-fal-ai-api-key"
export GROQ_API_KEY="your-groq-api-key"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Example Usage

```
User: Create social media content about our new AI-powered analytics dashboard

Claude: I'll run the content engine to create 5 channel-adapted posts
        with an AI-generated image and publish them.
```

The skill handles the entire pipeline in a single conversation:
- Generates platform-specific copy (tone, length, hashtags, formatting)
- Creates a matching visual via fal-ai image generation
- Publishes to all configured channels via Upload-Post

## References

- **Source Repository**: [iamasters-academy/content-engine](https://github.com/iamasters-academy/content-engine)
- **Topics**: agentic, claude-code, content-creation, fal-ai, groq, social-media, upload-post
- **License**: See repository for license details
