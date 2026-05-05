# Technical Details

## What It Does

This project provides a minimal Python `ctypes` binding for the [TRE](https://github.com/laurikari/tre/) regular expression library and benchmarks it against Python's built-in `re` module using known ReDoS (Regular Expression Denial of Service) attack patterns. TRE uses a tagged NFA algorithm that guarantees linear-time matching regardless of pattern complexity, making it immune to catastrophic backtracking.

The binding exposes three operations — compile, match, and free — mapping directly to TRE's `tre_regcomp`, `tre_regexec`, and `tre_regfree` C functions via `ctypes.CDLL`.

## Architecture

```
tre_binding.py        — ctypes wrapper: loads libtre.so, defines structs, exposes compile/match/free
redos_benchmark.py    — Benchmark harness: runs evil patterns against both engines with timeout
run.sh                — Entry point: checks for libtre, runs benchmark
```

**Data flow:**
1. Load `libtre.so` / `libtre.dylib` via `ctypes.util.find_library`
2. Define C structs (`regex_t`, `regmatch_t`) as ctypes Structures
3. For each ReDoS pattern: compile with TRE, time the match, compare to Python `re` (with timeout to avoid hanging)

**Dependencies:**
- TRE C library (`libtre-dev` / `brew install tre`)
- Python 3.8+ (stdlib only — `ctypes`, `re`, `time`, `signal`)

## Limitations

- The `ctypes` struct layout for `regex_t` is platform-dependent; the binding uses a simplified layout that works on Linux/macOS x86_64 and aarch64 but may need adjustment for exotic platforms.
- TRE does not support all PCRE features (lookaheads, lookbehinds, backreferences). It implements POSIX ERE plus approximate matching.
- The binding is minimal — no support for TRE's approximate/fuzzy matching API (though it could be added).
- TRE's last upstream release is old (2009); the library is stable but not actively developed.

## Why This Matters for Claude-Driven Products

- **Agent factories / automation:** Agents that accept user-supplied regex (for data extraction, routing, filtering) are vulnerable to ReDoS if using Python `re`. Swapping in TRE eliminates this entire attack class.
- **Lead-gen & marketing tools:** Web scrapers and content parsers that process adversarial HTML with regex can be DoS'd. TRE provides a safe drop-in.
- **Security posture:** Any product that lets end-users define patterns (search, validation, routing rules) needs a backtrack-free engine to avoid availability attacks.
- **ctypes pattern:** The binding demonstrates a general pattern for wrapping any C library in Python without compilation steps — useful for integrating native tools into Claude-orchestrated pipelines.

## References

- [Simon Willison's blog post](https://simonwillison.net/2026/May/4/tre-python-binding/#atom-everything)
- [TRE GitHub](https://github.com/laurikari/tre/)
- [ReDoS on OWASP](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)
