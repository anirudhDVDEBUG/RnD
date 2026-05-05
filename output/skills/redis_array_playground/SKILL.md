---
name: redis_array_playground
description: |
  Build an interactive browser-based playground for Redis Array commands using WASM.
  TRIGGER when: user wants to explore Redis array data type, build a Redis command playground, create WASM-based Redis demos, or work with ARGREP/ARSET/ARSCAN commands.
  DO NOT TRIGGER when: general Redis usage, Redis caching patterns, or non-array Redis data structures.
---

# Redis Array Playground

Create an interactive browser playground for the new Redis Array data type, compiled to WASM and running entirely in the browser.

## When to use

- "Build a Redis Array command explorer in the browser"
- "Create a WASM playground for testing Redis ARGREP commands"
- "I want to try Redis array commands without a server"
- "Make an interactive UI for Redis array operations like ARSET, ARSCAN, ARGREP"
- "Build a browser-based Redis sandbox with the new array type"

## How to use

### 1. Set up the WASM Redis build

Compile Redis from the arrays branch to WASM so it runs in the browser:
- Clone the Redis repo and checkout the branch with array support (PR #15162)
- Use Emscripten to compile a subset of Redis to WebAssembly
- Expose the command interface via a JavaScript bridge

### 2. Build the command builder UI

Create an interactive HTML/JS interface with:
- A sidebar listing all array commands: `ARCOUNT`, `ARDEL`, `ARDELRANGE`, `ARGET`, `ARGETRANGE`, `ARGREP`, `ARINFO`, `ARINSERT`, `ARLASTITEMS`, `ARLEN`, `ARMGET`, `ARMSET`, `ARNEXT`, `AROP`, `ARRING`, `ARSCAN`, `ARSEEK`, `ARSET`
- A main panel that dynamically renders the selected command's parameters
- Support for predicates (e.g., MATCH dropdown with value input)
- Checkboxes for optional flags (AND, OR, LIMIT, WITHVALUES, NOCASE)
- A live command preview showing the assembled Redis command string
- A "Run command" button and reply display area

### 3. Implement ARGREP support

The most powerful command is `ARGREP` which runs server-side grep against array values:
- Uses the vendored TRE regex library for approximate matching
- Supports predicates: MATCH, PREFIX, SUFFIX, CONTAINS
- Options: AND/OR logic, LIMIT, WITHVALUES, NOCASE
- Example: `ARGREP myarr MATCH CHERRY AND LIMIT 10 WITHVALUES NOCASE`

### 4. Wire up execution

- Send commands to the WASM Redis instance via the JS bridge
- Parse and display replies in a formatted output section
- Maintain state across commands (arrays persist in the WASM instance)

### Example single-file structure

```html
<!DOCTYPE html>
<html>
<head><title>Redis Array Playground</title></head>
<body>
  <div id="sidebar"><!-- command list --></div>
  <div id="main">
    <div id="builder"><!-- dynamic command builder --></div>
    <div id="command-preview"><!-- live command string --></div>
    <button id="run">Run command</button>
    <div id="reply"><!-- output --></div>
  </div>
  <script src="redis.wasm.js"></script>
  <script src="playground.js"></script>
</body>
</html>
```

## References

- Blog post: https://simonwillison.net/2026/May/4/redis-array/#atom-everything
- Live playground: https://tools.simonwillison.net/redis-array
- Redis Arrays PR: https://github.com/redis/redis/pull/15162
- TRE regex library: https://github.com/laurikari/tre/
- Antirez on AI-assisted development: https://antirez.com/news/164
