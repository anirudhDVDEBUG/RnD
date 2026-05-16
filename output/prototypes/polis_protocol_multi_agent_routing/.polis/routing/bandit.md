---
strategy: thompson_sampling
exploration_rate: 0.1
reward_metric: task_success_rate
decay: 0.95
---

# Routing Rules

| Task Type        | Primary Agent | Fallback Agent |
|------------------|---------------|----------------|
| code_generation  | claude        | codex          |
| web_research     | gemini        | gpt            |
| data_analysis    | claude        | gemini         |
| creative_writing | gpt           | claude         |
| code_review      | claude        | gpt            |
| summarization    | gemini        | claude         |
