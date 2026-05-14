---
name: AI Engineering Skill Pack
description: |
  Methodology-first skill for AI engineers covering RAG evaluation, agent debugging, MCP server development, paper reproduction, and benchmark reporting. Triggers: "evaluate RAG pipeline", "debug agent", "build MCP server", "reproduce paper results", "run benchmark report", "RAG eval", "agent trace debugging"
version: 1.0.0
author: surpradhan
tags:
  - ai-engineering
  - rag-evaluation
  - agent-debugging
  - mcp-server
  - benchmarking
  - paper-reproduction
  - claude-code-skills
---

# AI Engineering Skill Pack

A methodology-first skill for Claude Code that provides structured workflows for common AI engineering tasks: RAG evaluation, agent debugging, MCP server development, paper reproduction, and benchmark reporting.

## When to use

- "Evaluate my RAG pipeline" — run retrieval and generation quality assessments
- "Debug this agent's behavior" — trace agent execution, inspect tool calls, and diagnose failures
- "Build an MCP server for X" — scaffold and implement Model Context Protocol servers
- "Reproduce results from this paper" — systematically replicate ML/AI paper experiments
- "Generate a benchmark report" — run standardized evaluations and produce comparison reports

## How to use

### 1. RAG Evaluation

Systematically evaluate Retrieval-Augmented Generation pipelines:

1. **Define evaluation dataset**: Identify or create a set of queries with known-good reference answers
2. **Measure retrieval quality**:
   - Compute recall@k, precision@k, and MRR for the retriever
   - Check chunk relevance by inspecting retrieved passages against ground truth
   - Log retrieval latency per query
3. **Measure generation quality**:
   - Score faithfulness (is the answer grounded in retrieved context?)
   - Score relevance (does the answer address the query?)
   - Check for hallucination by comparing claims against source passages
4. **Report results**: Generate a structured eval report with per-query breakdowns and aggregate metrics
5. **Iterate**: Suggest specific improvements based on failure patterns (e.g., chunking strategy, embedding model, prompt template)

```bash
# Example: Run RAG eval on a pipeline
claude "Evaluate my RAG pipeline in src/rag/ using the test queries in eval/queries.json"
```

### 2. Agent Debugging

Trace and diagnose issues in LLM-based agent systems:

1. **Capture execution trace**: Log each step — LLM call, tool invocation, observation, and decision
2. **Identify failure points**: Find where the agent deviates from expected behavior
   - Tool call errors (wrong arguments, missing tools)
   - Reasoning loops (agent repeating the same action)
   - Context overflow (exceeding token limits)
3. **Inspect intermediate state**: Review the agent's scratchpad, memory, and tool outputs at each step
4. **Root cause analysis**: Classify the failure (prompt issue, tool issue, planning issue, context issue)
5. **Suggest fixes**: Provide specific, actionable recommendations

```bash
# Example: Debug an agent failure
claude "Debug why my agent in src/agent/ fails on the task described in tests/task_003.json"
```

### 3. MCP Server Development

Build Model Context Protocol servers following best practices:

1. **Define resources and tools**: Specify what data the server exposes (resources) and what actions it supports (tools)
2. **Scaffold the server**: Create the MCP server structure with proper transport handling (stdio/SSE)
3. **Implement handlers**:
   - Resource handlers: list, read, subscribe
   - Tool handlers: list, call with proper input validation
   - Prompt handlers (optional): list, get
4. **Add error handling**: Proper MCP error codes and descriptive messages
5. **Test**: Validate with the MCP Inspector or a Claude Code client

```bash
# Example: Create an MCP server
claude "Build an MCP server that exposes my PostgreSQL database as resources with read-only query tools"
```

### 4. Paper Reproduction

Systematically reproduce results from ML/AI research papers:

1. **Parse the paper**: Extract key claims, datasets, hyperparameters, model architecture, and evaluation metrics
2. **Set up environment**: Identify dependencies, framework versions, and hardware requirements
3. **Implement or adapt**: Write code matching the paper's methodology, noting any ambiguities
4. **Run experiments**: Execute training/evaluation with the paper's exact configuration
5. **Compare results**: Generate a comparison table (paper-reported vs. reproduced) with confidence intervals
6. **Document discrepancies**: Note any gaps and hypothesize causes (random seed, hardware, undocumented details)

```bash
# Example: Reproduce paper results
claude "Reproduce the main results from the paper at docs/paper.pdf using the dataset in data/"
```

### 5. Benchmark Reporting

Run standardized evaluations and produce structured reports:

1. **Select benchmarks**: Identify appropriate benchmarks for the task (e.g., MMLU, HumanEval, custom suites)
2. **Configure evaluation**: Set up model parameters, sampling settings, and evaluation harness
3. **Execute benchmarks**: Run evaluations with proper logging and timing
4. **Aggregate results**: Compute means, standard deviations, and percentiles across runs
5. **Generate report**: Produce a markdown report with tables, comparisons to baselines, and key findings

```bash
# Example: Run benchmark report
claude "Run benchmarks on my model in src/model/ against the test suite in benchmarks/ and generate a report"
```

## Methodology Principles

- **Reproducibility first**: Always log seeds, versions, and configurations
- **Structured output**: Generate machine-readable results (JSON/CSV) alongside human-readable reports
- **Iterative improvement**: Each evaluation should produce actionable next steps
- **Fail loudly**: Surface errors and edge cases rather than silently degrading
- **Compare against baselines**: Always include reference points for context

## References

- Source: [surpradhan/claude-code-for-ai-engineers](https://github.com/surpradhan/claude-code-for-ai-engineers)
- Full skill pack (6 skills, 3 templates, 5 slash commands): [surpradhan.gumroad.com](https://surpradhan.gumroad.com/l/claude-code-for-ai-engineers)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Anthropic Skills Convention](https://github.com/anthropics/skills)
