---
name: gpt55_instant_system_card_analysis
description: |
  Analyze and summarize the GPT-5.5 Instant System Card from OpenAI, covering safety evaluations, capability benchmarks, deployment mitigations, and risk assessments.
  TRIGGER when: user asks about GPT-5.5 Instant safety, GPT-5.5 Instant system card, OpenAI model safety evaluations, or comparing frontier model risk assessments.
---

# GPT-5.5 Instant System Card Analysis

Reference skill for understanding and working with the GPT-5.5 Instant System Card published by OpenAI.

## When to use

- "What safety evaluations were done for GPT-5.5 Instant?"
- "Summarize the GPT-5.5 Instant system card"
- "How does GPT-5.5 Instant compare to previous models on safety benchmarks?"
- "What are the deployment mitigations for GPT-5.5 Instant?"
- "What risks were identified in the GPT-5.5 Instant evaluation?"

## How to use

1. **Fetch the system card**: Retrieve the full document from the OpenAI publication for the most current details.
2. **Key areas to analyze**:
   - **Model overview**: GPT-5.5 Instant is OpenAI's lightweight frontier model optimized for speed and cost-efficiency while maintaining strong safety properties.
   - **Safety evaluations**: Review the Preparedness Framework assessments including CBRN (chemical, biological, radiological, nuclear), cybersecurity, persuasion, and model autonomy evaluations.
   - **Benchmark results**: Check performance on standard safety benchmarks (TruthfulQA, BBQ bias, toxicity generation) and capability evaluations.
   - **Red teaming**: Examine findings from internal and external red team exercises covering jailbreaks, harmful content generation, and misuse vectors.
   - **Deployment mitigations**: Document the system-level safeguards including content filtering, rate limiting, usage policies, and monitoring systems.
   - **Risk ratings**: Note the Preparedness Framework risk level assignments (low/medium/high/critical) across each evaluation category.
3. **Compare with prior cards**: Reference GPT-4o and GPT-5 system cards for trend analysis on safety improvements and new risk categories.
4. **Extract actionable insights**: Identify implications for developers building on the model, including known limitations, recommended guardrails, and use-case restrictions.

## Key concepts

- **Preparedness Framework**: OpenAI's structured approach to evaluating catastrophic and frontier risks before deployment.
- **System card vs. model card**: System cards cover the full deployed system (model + safeguards + policies), not just the base model.
- **Staged deployment**: Models are released incrementally with monitoring to catch emergent risks.

## References

- [GPT-5.5 Instant System Card](https://openai.com/index/gpt-5-5-instant-system-card) — Primary source document from OpenAI
- [OpenAI News RSS](https://openai.com/blog/rss.xml) — Feed for latest OpenAI publications
