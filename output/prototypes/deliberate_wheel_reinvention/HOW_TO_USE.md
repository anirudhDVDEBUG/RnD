# How to Use

## This is a Claude Code Skill

### Installation

1. Copy the `SKILL.md` file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/deliberate_wheel_reinvention
cp SKILL.md ~/.claude/skills/deliberate_wheel_reinvention/SKILL.md
```

2. That's it. No dependencies, no API keys, no build step.

### Trigger phrases

Once installed, Claude Code activates this skill when you say things like:

- "I want to truly understand how databases work by building one myself"
- "Should I reimplement a template engine or just use Jinja2?"
- "Help me learn networking by building something from scratch"
- "I keep using SQLAlchemy but don't understand the internals"
- "What's the best way to deeply learn compilers through practice?"

### What Claude does with this skill

Claude will:
1. Ask what domain you want to go deeper in
2. Suggest specific things to reimplement (not too big, not too small)
3. Scope a minimal version with 3 essential behaviors and explicit "leave out" list
4. Set a concrete done-condition so you know when you've learned the thing
5. Guide you through building it, encouraging attempt-first-then-compare
6. Help you extract transferable principles and pick the next wheel

## Standalone CLI demo

The repo also includes a standalone Python tool that demonstrates the skill's knowledge base:

```bash
# No dependencies needed — Python 3.10+ stdlib only
bash run.sh
```

### First 60 seconds

```
$ bash run.sh

=== Deliberate Wheel Reinvention — Demo ===

================================================================
  DELIBERATE WHEEL REINVENTION
  Learn by building — pick the right wheels to reinvent
================================================================

  Available domains (6 total):

    compilers       -> Lexer (tokenizer), Recursive descent parser, Register allocator
    databases       -> B-tree index, Simple query parser, WAL journaling
    networking      -> HTTP/1.1 server, DNS resolver, TCP over UDP
    os              -> Memory allocator, Simple filesystem, Shell
    search          -> Inverted index, TF-IDF scorer, Finite state transducer
    web             -> Template engine, URL router, Form validator

  ...followed by a full example learning plan for "inverted index"
  and a JSON export of a plan for "URL router".
```

### CLI options

```bash
# Interactive guided mode (prompts you to pick domain + wheel)
python3 wheel_reinvention.py --interactive

# Show wheels in a specific domain
python3 wheel_reinvention.py --domain compilers

# Generate a full learning plan
python3 wheel_reinvention.py --plan search "TF-IDF scorer"

# Export entire catalog as JSON
python3 wheel_reinvention.py --json
```
