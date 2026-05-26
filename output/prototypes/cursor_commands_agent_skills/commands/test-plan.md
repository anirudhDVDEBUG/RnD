# /test-plan

## Purpose
Generate a structured test plan for a feature or module.

## Inputs
- `scope`: Module path or feature description (required)
- `depth`: quick | standard | thorough (optional, default: standard)

## Behavior
1. Read the target module or feature description.
2. Identify public API surface and edge cases.
3. Categorize tests: unit, integration, e2e.
4. For each test case, specify: name, type, input, expected output, rationale.
5. Prioritize by risk (highest-risk cases first).

## Output Format

```
## Test Plan: <scope>

### Unit Tests
| # | Name | Input | Expected | Rationale |
|---|------|-------|----------|-----------|

### Integration Tests
| # | Name | Setup | Steps | Expected |
|---|------|-------|-------|----------|

### Edge Cases
- ...

### Coverage Estimate
<percentage estimate and gaps>
```
