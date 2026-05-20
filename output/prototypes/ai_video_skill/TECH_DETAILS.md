# Technical Details — AI Video Skill

## What It Does

The AI Video Skill is a Claude Code skill that wraps 5 video-generation models behind a unified interface with automatic model selection and a self-improving quality-control loop. When a user asks Claude to "generate a video," the skill parses the prompt, picks the best model (or uses the user's choice), submits a generation request, scores the output on motion coherence / prompt adherence / visual fidelity, and — if quality falls below a configurable threshold — rewrites the prompt and re-generates. Successful prompt patterns are persisted to a local JSON file so future generations start from better baselines.

## Architecture

```
User prompt
    |
    v
[video_skill.py]  -- CLI entry point, argparse, print output
    |
    v
[models.py]        -- MODEL_REGISTRY (5 models), select_model(), generate_video()
    |                  Auto-selection uses keyword heuristics on the prompt.
    |                  Mock mode writes a placeholder .mp4 file.
    v
[quality_loop.py]  -- quality_loop(), evaluate_video(), refine_prompt()
                       QualityScore: motion_coherence, prompt_adherence, visual_fidelity
                       Weighted overall = 0.35*motion + 0.40*adherence + 0.25*fidelity
                       If overall < threshold → refine prompt → re-generate (up to max_iter)
                       Successful patterns saved to prompt_history.json
```

### Key Files

| File | Purpose |
|------|---------|
| `models.py` | Model registry, auto-selection heuristics, `generate_video()` with mock/real paths |
| `quality_loop.py` | Quality scoring, prompt refinement, history persistence, main loop |
| `video_skill.py` | CLI demo, multi-model sweep, user-facing output |
| `SKILL.md` | Claude Code skill descriptor (trigger phrases, usage docs) |
| `run.sh` | One-command demo runner |

### Data Flow

1. **Prompt → Model Selection**: Keyword matching (`dance` → Seedance, `photorealistic` → Veo, `artistic` → Wan, person-in-image → OmniHuman, default → Kling).
2. **Model → API Call**: Each model maps to a provider API key env var. Mock mode skips the API and writes a placeholder file.
3. **Output → Quality Evaluation**: Scores are computed (mock: randomized; real: would use CLIP or a vision model).
4. **Score < Threshold → Prompt Refinement**: Adds quality modifiers based on which dimension scored low. Borrows modifiers from `prompt_history.json` (past successes).
5. **Loop**: Steps 2-4 repeat up to `max_iterations` times.

### Dependencies

- **Mock mode**: Python 3.8+ stdlib only (no pip packages).
- **Real mode**: Would need `requests`, provider SDKs (Seedance API, Kling API, etc.), and optionally a CLIP model for quality evaluation.

## Limitations

- **No real API integrations yet**: The `generate_video()` real-API path raises `NotImplementedError`. The repo provides the orchestration layer — you wire in your own provider SDKs.
- **Quality evaluation is simulated**: Mock mode uses random scores. Real evaluation would need CLIP-based similarity scoring or a vision LLM.
- **Model selection is keyword-based**: No semantic understanding — "a realistic painting" would trigger Veo (via "realistic") even though Wan might be better.
- **No video post-processing**: No trimming, format conversion, or audio overlay.
- **Prompt history is local**: `prompt_history.json` is per-machine; no cloud sync or team sharing.

## Why It Matters

For teams building Claude-driven products:

- **Ad creatives / marketing**: Automate video ad generation at scale — feed product descriptions, get video variants across multiple models, quality-gated before delivery. The self-improving loop means fewer manual prompt iterations.
- **Agent factories**: Embeddable as a skill in any Claude Code agent. An agent-factory could offer "video generation" as a plug-in capability for customer-facing agents.
- **Lead-gen content**: Generate short social video clips from blog posts or product pages. The multi-model approach lets you A/B test visual styles (photorealistic via Veo vs. artistic via Wan).
- **Voice AI + video**: Combine with a voice-AI pipeline — generate a talking-head video (OmniHuman) synced to AI-generated speech for personalized outreach.

The key value is the **quality loop pattern**: instead of one-shot generation, the skill iterates toward acceptable quality automatically — a pattern transferable to any generative AI workflow (images, audio, copy).
