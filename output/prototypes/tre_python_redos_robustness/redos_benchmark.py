"""Benchmark TRE vs Python re on known ReDoS patterns."""

import re
import time
import signal
import sys

# Timeout handler for Python re (prevents hanging)
class RegexTimeout(Exception):
    pass

def _timeout_handler(signum, frame):
    raise RegexTimeout()

def time_python_re(pattern: str, text: str, timeout_sec: float = 2.0) -> tuple:
    """Time Python re.match with a timeout. Returns (seconds, timed_out)."""
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, timeout_sec)
    start = time.perf_counter()
    timed_out = False
    try:
        re.match(pattern, text)
    except RegexTimeout:
        timed_out = True
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
    elapsed = time.perf_counter() - start
    return elapsed, timed_out


def time_tre(pattern: str, text: str) -> float:
    """Time TRE compile+match+free."""
    import tre_binding
    start = time.perf_counter()
    preg = tre_binding.compile(pattern)
    tre_binding.match(preg, text)
    tre_binding.free(preg)
    return time.perf_counter() - start


def main():
    # Check if TRE is available
    try:
        import tre_binding
    except OSError as e:
        print(f"ERROR: {e}")
        print("\nRunning in MOCK MODE (simulated results):\n")
        run_mock()
        return

    print("=" * 60)
    print("  TRE vs Python re — ReDoS Robustness Benchmark")
    print("=" * 60)
    print()

    # Known ReDoS patterns that cause catastrophic backtracking
    test_cases = [
        (r"(a+)+$", 25, "nested quantifier"),
        (r"(a|a)+$", 25, "alternation ambiguity"),
        (r"(a|aa)+$", 25, "overlapping alternation"),
        (r"(.*a){20}", 20, "greedy dot-star repeated"),
    ]

    for pattern, n, description in test_cases:
        evil_input = "a" * n + "!"
        print(f"Pattern: {pattern}  ({description})")
        print(f"Input:   {'a' * min(n, 10)}...{'a' * min(n, 5)}! ({n} a's + '!')")
        print()

        # TRE timing
        tre_time = time_tre(pattern, evil_input)

        # Python re timing (with 2s timeout)
        py_time, timed_out = time_python_re(pattern, evil_input, timeout_sec=2.0)

        if timed_out:
            print(f"  Python re: >{py_time:.4f}s  [TIMEOUT - catastrophic backtracking]")
        else:
            print(f"  Python re:  {py_time:.4f}s", end="")
            if py_time > 0.1:
                print("  [SLOW - backtracking]")
            else:
                print("  [OK]")

        print(f"  TRE:        {tre_time:.6f}s  [linear time - no backtracking]")

        if py_time > 0 and tre_time > 0:
            speedup = py_time / tre_time
            print(f"  Speedup:    {speedup:,.0f}x")

        print()

    print("-" * 60)
    print("Conclusion: TRE is immune to ReDoS because it uses a tagged")
    print("NFA algorithm with no backtracking. Python's re module uses a")
    print("backtracking NFA that is vulnerable to exponential blowup.")
    print("-" * 60)


def run_mock():
    """Simulated output when TRE library is not installed."""
    print("=" * 60)
    print("  TRE vs Python re — ReDoS Robustness Benchmark (MOCK)")
    print("=" * 60)
    print()
    mock_results = [
        ("(a+)+$", 25, "nested quantifier", 2.0, True, 0.00018),
        ("(a|a)+$", 25, "alternation ambiguity", 2.0, True, 0.00015),
        ("(a|aa)+$", 25, "overlapping alternation", 2.0, True, 0.00016),
        ("(.*a){20}", 20, "greedy dot-star repeated", 2.0, True, 0.00021),
    ]
    for pattern, n, desc, py_time, timed_out, tre_time in mock_results:
        print(f"Pattern: {pattern}  ({desc})")
        print(f"Input:   {'a' * min(n, 10)}...{'a' * min(n, 5)}! ({n} a's + '!')")
        print()
        print(f"  Python re: >{py_time:.4f}s  [TIMEOUT - catastrophic backtracking]")
        print(f"  TRE:        {tre_time:.6f}s  [linear time - no backtracking]")
        print(f"  Speedup:    {py_time / tre_time:,.0f}x")
        print()
    print("-" * 60)
    print("NOTE: TRE library not installed. Above are simulated results.")
    print("Install libtre-dev to see real benchmarks.")
    print("-" * 60)


if __name__ == "__main__":
    main()
