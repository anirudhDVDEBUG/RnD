---
name: biosymphony_ferm_doe
description: |
  Design-of-Experiments (DoE) planning for fermentation, bioprocess, and biomanufacturing workflows using BioSymphony's agentic AI harness. Includes biosafety-aware readiness gating, scale-up/scale-down bridging, and autonomous long-horizon experiment planning.
  Triggers:
    - User asks to plan a fermentation DoE or design of experiments
    - User needs bioprocess or biomanufacturing experiment planning
    - User wants scale-up or scale-down bridging for bioreactor experiments
    - User asks about biosafety gating or readiness checks for lab experiments
    - User wants to generate a DoE matrix for fed-batch, perfusion, or cell culture
---

# BioSymphony Fermentation DoE Skill

Agentic AI harness for pre-experiment Design-of-Experiments (DoE) planning in fermentation, bioprocess, and biomanufacturing. Designed with biosafety in mind, featuring readiness gating and scale-up/scale-down bridging.

## When to use

- "Plan a DoE for my fed-batch fermentation experiment"
- "Generate a design of experiments matrix for bioreactor scale-up"
- "Run biosafety readiness gating before starting my bioprocess experiment"
- "Bridge my bench-scale DoE to pilot-scale biomanufacturing"
- "Create a DoE for optimizing kLa in perfusion cell culture"

## How to use

1. **Install the tool**:
   ```bash
   git clone https://github.com/BioSymphony/biosymphony-ferm-doe.git
   cd biosymphony-ferm-doe
   pip install -e .
   ```

2. **Define your experiment parameters**: Specify the factors (e.g., temperature, pH, dissolved oxygen, feed rate, kLa), their ranges, and the response variables you want to optimize (e.g., titer, viability, productivity).

3. **Select your DoE type**: Choose from supported designs such as full factorial, fractional factorial, central composite, or Box-Behnken based on the number of factors and desired resolution.

4. **Run biosafety readiness gating**: Before generating the final DoE plan, the harness performs biosafety-aware readiness checks to ensure all planned experimental conditions fall within safe operating limits for your organism and facility.

5. **Generate the DoE plan**: The tool produces a structured experiment matrix with run order, factor levels, and blocking assignments. For scale-up or scale-down studies, it automatically applies bridging logic to translate parameters between scales (e.g., bench to pilot, pilot to manufacturing) using principles like constant kLa, constant P/V, or constant tip speed.

6. **Review and export**: Review the generated plan, including any flagged biosafety concerns, and export it for use in your LIMS, ELN, or bioreactor control system.

### Key features

- **Biosafety-aware gating**: Automatic checks against safety constraints before experiment execution
- **Scale-up / scale-down bridging**: Translates DoE parameters across bioreactor scales using standard engineering correlations
- **Long-horizon autonomy**: Designed for complex, multi-stage experimental campaigns
- **Fermentation-native**: Built-in support for fed-batch, perfusion, and continuous culture modes
- **kLa and mixing optimization**: First-class support for oxygen transfer and mixing parameters

## References

- Source repository: [BioSymphony/biosymphony-ferm-doe](https://github.com/BioSymphony/biosymphony-ferm-doe)
- Topics: bioprocess, design-of-experiments, fermentation, biomanufacturing, claude-code-skills
