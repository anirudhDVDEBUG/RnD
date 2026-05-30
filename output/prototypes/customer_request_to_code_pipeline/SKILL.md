---
name: customer_request_to_code_pipeline
description: |
  Turn customer feature requests, bug reports, or support tickets into implementable code changes using an automated pipeline.
  TRIGGER when: user wants to convert customer feedback into code, automate ticket-to-PR workflows, triage feature requests into engineering tasks, or build a request-to-implementation pipeline.
  DO NOT TRIGGER when: general code generation unrelated to customer input, or simple bug fixes without customer context.
---

# Customer Request to Code Pipeline

Convert customer requests, feature asks, and bug reports into concrete code changes — inspired by how Braintrust engineers use AI coding agents to turn customer input into shipped experiments and features.

## When to use

- "Turn this customer request into a code change"
- "Build a pipeline that converts support tickets into PRs"
- "Triage these feature requests and generate implementation plans"
- "Automate turning user feedback into engineering tasks with code"
- "Set up a workflow from customer input to code output"

## How to use

### Step 1: Parse the customer request

Extract structured information from the raw customer input:

- **What** the customer wants (feature, fix, improvement)
- **Why** they want it (use case, pain point)
- **Where** it applies (affected component, API, UI area)
- **Priority signals** (number of requesters, revenue impact, urgency)

### Step 2: Map to codebase scope

- Identify the relevant files, modules, and functions that would need changes
- Determine if it's a new feature, modification, or bug fix
- Assess complexity (single-file change vs. cross-cutting concern)
- Check for existing related code or patterns to follow

### Step 3: Generate an implementation plan

Produce a structured plan:

```markdown
## Request Summary
[One-line summary of what the customer wants]

## Affected Files
- path/to/file1.ext — reason for change
- path/to/file2.ext — reason for change

## Implementation Steps
1. [Concrete step with expected outcome]
2. [Next step]

## Testing Strategy
- Unit tests for [specific behavior]
- Integration test for [end-to-end flow]

## Risks & Considerations
- [Any breaking changes, migrations, or edge cases]
```

### Step 4: Implement the changes

- Write code following existing project conventions
- Run experiments or tests to validate the change
- Keep changes minimal and focused on the customer request
- Add appropriate test coverage

### Step 5: Summarize for review

Provide a clear summary linking the customer request back to the code change, making it easy for reviewers to understand the "why" behind each modification.

## Best Practices

- **Batch similar requests**: Group related customer asks to avoid redundant changes
- **Preserve customer language**: Reference the original request in commit messages and PR descriptions
- **Run experiments first**: For non-trivial changes, prototype and validate before committing
- **Keep scope tight**: One request = one focused PR; avoid scope creep
- **Close the loop**: Document how the change addresses the original request

## References

- [How Braintrust turns customer requests into code with Codex](https://openai.com/index/braintrust) — Engineering workflow case study on using AI agents to convert customer input into shipped code
