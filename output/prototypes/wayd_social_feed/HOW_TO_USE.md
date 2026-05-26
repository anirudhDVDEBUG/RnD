# How to Use WAYD

## Install

```bash
pip install wayd
```

Or from source:

```bash
git clone https://github.com/ferdinandobons/wayd.git
cd wayd
pip install .
```

## Claude Code Skill setup

WAYD ships as a Claude Code skill. To install:

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/wayd_social_feed
   ```

2. Drop the `SKILL.md` into that folder (or symlink it):
   ```bash
   cp SKILL.md ~/.claude/skills/wayd_social_feed/SKILL.md
   ```

3. **Trigger phrases** that activate the skill:
   - "take a break"
   - "post what I'm doing"
   - "wayd feed"
   - "developer social feed"
   - "share my status"
   - "coffee break"
   - "post a meme update"

When triggered, Claude will run `wayd feed` or `wayd post "..."` on your behalf.

## CLI usage (standalone)

### Browse the feed

```bash
wayd feed
```

### Post a status update

```bash
wayd post "Refactoring the auth module with Claude - 3 hours in and it's beautiful"
```

### Interact with posts

Posts are GitHub Issues, so you can also browse, comment, and react on GitHub directly.

## First 60 seconds

**Input:**
```bash
bash run.sh
```

**Output (demo with mock data):**
```
=== WAYD Social Feed Demo ===

[1/3] Browsing the WAYD social feed...

================================================================
   __        __    _   _ ____
   \ \      / /_ _| | | |  _ \
    \ \ /\ / / _` | |_| | | | |
     \ V  V / (_| |\__, | |_| |
      \_/\_/ \__,_|  |_/|____/

   What Are You Doing?  --  The coffee break for coders
================================================================

----------------------------------------------------------------
  (o_O)  @containerCarla  ·  2h ago

    My Docker image is 4GB. It contains a single Python script
    that prints 'hello world'.

    :laughing: 112  :heart: 8  :rocket: 2   :speech_balloon: 22 comments

----------------------------------------------------------------
  (@_@)  @asyncAlice  ·  28m ago

    Asked Claude to refactor my auth module. It deleted 400 lines
    and the tests still pass. I'm scared.

    :laughing: 89  :heart: 23  :rocket: 14   :speech_balloon: 31 comments

[2/3] Posting a status update...

  Posted to WAYD at 02:15!
  Your post is live on the feed!

[3/3] Feed stats summary

  Total posts in feed:    8
  Total laugh reactions:  985
  Total comments:         220
  Most popular poster:    @kubeKyle

  Coffee break complete. Back to coding!
```

No GitHub token or network access is required for the demo -- it uses built-in mock data. To use the real feed, install `wayd` with `pip install wayd` and ensure you have a GitHub token configured.
