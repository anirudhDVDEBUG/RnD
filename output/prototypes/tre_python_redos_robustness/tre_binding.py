"""Minimal Python ctypes binding for the TRE regex library."""

import ctypes
import ctypes.util
import sys

# --- Load TRE shared library ---

_lib_path = ctypes.util.find_library("tre")
if not _lib_path:
    # Try common paths directly
    import platform
    if platform.system() == "Linux":
        for p in ("/usr/lib/x86_64-linux-gnu/libtre.so",
                  "/usr/lib/aarch64-linux-gnu/libtre.so",
                  "/usr/local/lib/libtre.so"):
            try:
                _tre = ctypes.CDLL(p)
                _lib_path = p
                break
            except OSError:
                continue
    if not _lib_path:
        raise OSError(
            "TRE library not found. Install it:\n"
            "  Ubuntu/Debian: sudo apt-get install libtre-dev\n"
            "  macOS:         brew install tre\n"
        )
else:
    _tre = ctypes.CDLL(_lib_path)

# --- Constants ---

REG_EXTENDED = 1
REG_NOSUB = 8
REG_NOMATCH = 1

# --- Structures ---

class regex_t(ctypes.Structure):
    """TRE compiled regex. Opaque — we allocate enough space."""
    _fields_ = [
        ("re_nsub", ctypes.c_size_t),
        ("value", ctypes.c_void_p),
    ]


class regmatch_t(ctypes.Structure):
    _fields_ = [
        ("rm_so", ctypes.c_int),
        ("rm_eo", ctypes.c_int),
    ]


# --- Function signatures ---

_tre.tre_regcomp.argtypes = [ctypes.POINTER(regex_t), ctypes.c_char_p, ctypes.c_int]
_tre.tre_regcomp.restype = ctypes.c_int

_tre.tre_regexec.argtypes = [
    ctypes.POINTER(regex_t), ctypes.c_char_p,
    ctypes.c_size_t, ctypes.POINTER(regmatch_t), ctypes.c_int
]
_tre.tre_regexec.restype = ctypes.c_int

_tre.tre_regfree.argtypes = [ctypes.POINTER(regex_t)]
_tre.tre_regfree.restype = None


# --- Public API ---

def compile(pattern: str, flags: int = REG_EXTENDED) -> regex_t:
    """Compile a POSIX ERE pattern using TRE."""
    preg = regex_t()
    rc = _tre.tre_regcomp(ctypes.byref(preg), pattern.encode("utf-8"), flags)
    if rc != 0:
        raise ValueError(f"TRE regex compilation failed (error code {rc}) for pattern: {pattern}")
    return preg


def match(preg: regex_t, text: str) -> bool:
    """Return True if text matches the compiled pattern (full or partial)."""
    m = regmatch_t()
    rc = _tre.tre_regexec(ctypes.byref(preg), text.encode("utf-8"), 1, ctypes.byref(m), 0)
    return rc == 0


def free(preg: regex_t) -> None:
    """Free a compiled TRE regex."""
    _tre.tre_regfree(ctypes.byref(preg))
