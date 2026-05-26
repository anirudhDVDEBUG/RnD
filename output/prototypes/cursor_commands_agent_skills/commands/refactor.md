# /refactor

## Purpose
Propose and apply a targeted refactoring to improve code quality without changing behavior.

## Inputs
- `target`: File path or function name (required)
- `goal`: What to improve — readability | performance | testability | duplication (required)

## Behavior
1. Read the target code in full.
2. Identify the specific smell or improvement opportunity matching `goal`.
3. Propose the refactoring with before/after snippets.
4. Verify behavioral equivalence (no change to public API or side effects).
5. List any tests that should be re-run.

## Output Format

```
## Refactoring: <target>
**Goal:** <goal>

### Before
<code snippet>

### After
<code snippet>

### Rationale
<why this is better, with metrics if possible>

### Verification
- Tests to re-run: ...
- Behavioral equivalence: confirmed / needs-check
```
