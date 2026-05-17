---
name: FB Ad Video Studio
description: |
  High-converting Facebook/Instagram/TikTok video ads built as code using HyperFrames compositions in Claude Code.
  Implements a battle-tested ad structure with audio pipeline and reverse-template workflow for motion-graphics video ads.
  
  Triggers: video ad, facebook ad, instagram ad, tiktok ad, HyperFrames, motion graphics ad, ad creative, video creative, ad composition
---

# FB Ad Video Studio

Create high-converting video ads for Facebook, Instagram, and TikTok entirely as code using HyperFrames compositions within Claude Code.

## When to use

- "Create a Facebook video ad for my product"
- "Build a high-converting Instagram Reels ad with motion graphics"
- "Generate a TikTok video ad creative using HyperFrames"
- "Make a video ad with hook, problem, solution, CTA structure"
- "Reverse-engineer this ad style into a reusable template"

## How to use

### 1. Define Your Ad Brief

Specify your product/service, target audience, platform (FB/IG/TikTok), desired duration (15s/30s/60s), and key message.

### 2. Choose Ad Structure

Follow the battle-tested ad framework:
- **Hook** (0-3s): Pattern interrupt to stop the scroll
- **Problem** (3-8s): Agitate the pain point
- **Solution** (8-18s): Introduce your product/offer
- **Social Proof** (18-24s): Testimonials or results
- **CTA** (24-30s): Clear call to action with urgency

### 3. Build HyperFrames Composition

Create the video ad as an HTML-based HyperFrames composition:

```html
<!-- Example frame structure -->
<div class="frame" data-duration="3000" data-transition="fade">
  <h1 class="hook-text">Stop scrolling if you...</h1>
  <div class="motion-element" data-animate="slide-up"></div>
</div>
```

### 4. Configure Audio Pipeline

Add background music, sound effects, and voiceover timing synced to frames:
- Background track selection
- Sound effect triggers on transitions
- Voiceover script with timestamp alignment

### 5. Reverse-Template Workflow

To replicate a winning ad style:
1. Analyze the reference ad structure (timing, transitions, text placement)
2. Extract the template pattern (frame count, durations, motion types)
3. Generate a new composition using that template with your content
4. Customize colors, fonts, and branding to match your brand

### 6. Export

Render the composition to video format optimized for each platform's specs:
- **Facebook Feed**: 1:1 or 4:5, up to 240min
- **Instagram Reels**: 9:16, 15-90s
- **TikTok**: 9:16, 15-60s

## Platform Specifications

| Platform | Aspect Ratio | Max Duration | Recommended |
|----------|-------------|--------------|-------------|
| FB Feed | 1:1, 4:5 | 240 min | 15-30s |
| IG Reels | 9:16 | 90s | 15-30s |
| TikTok | 9:16 | 10 min | 15-60s |

## Key Principles

- **Hook fast**: First 3 seconds determine if users keep watching
- **Text-heavy**: Most social video is watched on mute
- **Motion attracts**: Use kinetic typography and animated elements
- **Platform-native**: Match the look and feel of organic content
- **Test variations**: Generate multiple hooks/CTAs for A/B testing

## References

- Source: [ai-agents-for-agencies-coaches/fb-ad-video-studio](https://github.com/ai-agents-for-agencies-coaches/fb-ad-video-studio)
- Topics: claude-code, claude-skill, facebook-ads, hyperframes, motion-graphics, video-ads
