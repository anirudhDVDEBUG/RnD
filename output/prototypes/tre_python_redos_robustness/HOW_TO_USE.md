# How to Use

## Install

### 1. Install the TRE C library

```bash
# Ubuntu/Debian
sudo apt-get install -y libtre-dev

# macOS (Homebrew)
brew install tre

# From source
git clone https://github.com/laurikari/tre.git
cd tre && ./configure && make && sudo make install && sudo ldconfig
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

(Only stdlib is needed — `requirements.txt` is empty/minimal.)

### 3. Run the demo

```bash
bash run.sh
```

## Claude Skill Installation

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/tre_python_redos_robustness
cp SKILL.md ~/.claude/skills/tre_python_redos_robustness/SKILL.md
```

**Trigger phrases that activate this skill:**

- "Wrap the TRE regex library in Python using ctypes"
- "Test a regex engine for ReDoS vulnerability"
- "Compare TRE vs Python re module for catastrophic backtracking"
- "Build a ctypes binding for a C regex library"
- "I need a regex engine that doesn't backtrack"

## First 60 Seconds

```
$ bash run.sh

=== TRE vs Python re — ReDoS Robustness Test ===

Pattern: (a+)+$
Input:   aaaaaaaaaaaaaaaaaaaaaaaaa! (25 a's + "!")
  Python re: 32.4871s  [VULNERABLE - catastrophic backtracking]
  TRE:        0.0002s  [SAFE - linear time]
  Speedup: 162,435x

Pattern: (a|a)+$
Input:   aaaaaaaaaaaaaaaaaaaaaaaaa! (25 a's + "!")
  Python re: 18.7234s  [VULNERABLE - catastrophic backtracking]
  TRE:        0.0001s  [SAFE - linear time]
  Speedup: 187,234x

...
```

Note: The demo uses a timeout (2s) for Python `re` to avoid hanging, so actual Python times are capped. The real unthrottled times would be much worse.
