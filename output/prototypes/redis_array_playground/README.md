# Redis Array Playground

**TL;DR:** An interactive browser-based playground for the new Redis Array data type (PR #15162). Pick a command, fill in parameters, and see live results — no Redis server needed. Everything runs client-side in JavaScript, emulating all 18 array commands including the powerful `ARGREP` server-side grep.

**Headline result:** Run `ARGREP fruits CONTAINS berry WITHVALUES NOCASE` against a 20-element fruit array and get instant filtered results — all in your browser, zero setup.

See [HOW_TO_USE.md](HOW_TO_USE.md) for quick-start instructions and [TECH_DETAILS.md](TECH_DETAILS.md) for architecture details.

## Source

- Blog post: [Simon Willison — Redis Array](https://simonwillison.net/2026/May/4/redis-array/#atom-everything)
- Live demo by Simon: [tools.simonwillison.net/redis-array](https://tools.simonwillison.net/redis-array)
- Redis PR: [redis/redis#15162](https://github.com/redis/redis/pull/15162)
