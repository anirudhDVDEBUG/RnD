# AI Video Skill

Generate AI videos across 6 models (Seedance 2.0, Kling, Wan, Veo, OmniHuman) with a self-improving quality-control loop that refines prompts and re-generates until output meets a quality threshold. Works as a Claude Code skill triggered by natural language ("generate a video", "text to video").

**Headline result:** Say "generate a video of a dancer under neon lights" in Claude Code and the skill auto-selects the best model, generates the video, scores it on motion/adherence/fidelity, and retries with a refined prompt if quality is below threshold — all without manual intervention.

| Guide | What's inside |
|-------|---------------|
| [HOW_TO_USE.md](HOW_TO_USE.md) | Install, configure the skill, trigger phrases, first-60-seconds walkthrough |
| [TECH_DETAILS.md](TECH_DETAILS.md) | Architecture, data flow, limitations, product relevance |
