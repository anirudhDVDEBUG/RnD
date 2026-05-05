---
name: tre_python_redos_robustness
description: |
  Build a Python binding for the TRE regex engine using ctypes, and demonstrate its robustness against ReDoS (Regular Expression Denial of Service) attacks compared to Python's built-in `re` module.
  TRIGGER: user wants to use TRE regex engine, build ctypes bindings for TRE, test ReDoS resilience, compare regex engines for security, or wrap a C regex library in Python.
---

# TRE Python Binding — ReDoS Robustness Demo

Create a Python `ctypes` binding for the [TRE](https://github.com/laurikari/tre/) regular expression engine and demonstrate its resistance to ReDoS attacks.

## When to use

- "Wrap the TRE regex library in Python using ctypes"
- "Test a regex engine for ReDoS vulnerability"
- "Compare TRE vs Python re module for catastrophic backtracking"
- "Build a ctypes binding for a C regex library"
- "I need a regex engine that doesn't backtrack"

## How to use

### 1. Install the TRE library

Ensure the TRE C library is installed on the system:

```bash
# Ubuntu/Debian
sudo apt-get install libtre-dev

# macOS (Homebrew)
brew install tre

# From source
git clone https://github.com/laurikari/tre.git
cd tre && ./configure && make && sudo make install
```

### 2. Create the Python ctypes binding

Build a Python module that wraps TRE's C API using `ctypes`:

```python
import ctypes
import ctypes.util

# Load the TRE shared library
_lib_path = ctypes.util.find_library("tre")
if not _lib_path:
    raise OSError("TRE library not found. Install libtre-dev or equivalent.")
_tre = ctypes.CDLL(_lib_path)

# TRE constants
REG_EXTENDED = 1
REG_NOSUB = 8

# TRE regex_t structure
class regex_t(ctypes.Structure):
    _fields_ = [
        ("re_nsub", ctypes.c_size_t),
        ("value", ctypes.c_void_p),
    ]

# TRE regmatch_t structure
class regmatch_t(ctypes.Structure):
    _fields_ = [
        ("rm_so", ctypes.c_int),
        ("rm_eo", ctypes.c_int),
    ]

def tre_compile(pattern: str, flags: int = REG_EXTENDED) -> regex_t:
    """Compile a regex pattern using TRE."""
    preg = regex_t()
    result = _tre.tre_regcomp(ctypes.byref(preg), pattern.encode(), flags)
    if result != 0:
        raise ValueError(f"TRE compilation failed with code {result}")
    return preg

def tre_match(preg: regex_t, text: str) -> bool:
    """Test if text matches the compiled TRE pattern."""
    match = regmatch_t()
    result = _tre.tre_regexec(ctypes.byref(preg), text.encode(), 1, ctypes.byref(match), 0)
    return result == 0

def tre_free(preg: regex_t):
    """Free a compiled TRE regex."""
    _tre.tre_regfree(ctypes.byref(preg))
```

### 3. Test ReDoS robustness

Compare TRE against Python's `re` module with known ReDoS patterns:

```python
import re
import time

# Classic ReDoS pattern: catastrophic backtracking
redos_patterns = [
    (r"(a+)+$", "a" * 25 + "!"),
    (r"(a|a)+$", "a" * 25 + "!"),
    (r"(a|aa)+$", "a" * 25 + "!"),
]

for pattern, evil_input in redos_patterns:
    # Test Python re
    start = time.perf_counter()
    try:
        re.match(pattern, evil_input)
    except Exception:
        pass
    py_time = time.perf_counter() - start

    # Test TRE
    start = time.perf_counter()
    preg = tre_compile(pattern)
    tre_match(preg, evil_input)
    tre_free(preg)
    tre_time = time.perf_counter() - start

    print(f"Pattern: {pattern}")
    print(f"  Python re: {py_time:.4f}s")
    print(f"  TRE:       {tre_time:.6f}s")
    print()
```

TRE handles these patterns in constant time because it does **not** use backtracking. Python's `re` module uses a backtracking NFA engine, which makes it vulnerable to exponential blowup on adversarial inputs.

### 4. Key points

- **TRE** uses an algorithm based on tagged NFAs — no backtracking, so no catastrophic performance on adversarial patterns
- **Python's `re`** uses a backtracking implementation susceptible to ReDoS
- TRE also supports approximate (fuzzy) matching, which is a unique feature
- The `ctypes` approach avoids the need for a compiled C extension module
- TRE is used in production systems including Redis

## References

- [Simon Willison's blog post: TRE Python binding — ReDoS robustness demo](https://simonwillison.net/2026/May/4/tre-python-binding/#atom-everything)
- [Research repo with full code](https://github.com/simonw/research/tree/main/tre-python-binding)
- [TRE regex library (GitHub)](https://github.com/laurikari/tre/)
