#!/usr/bin/env python3
"""The Router Confesses — a one-line excuse for a dropped connection.

The router was not being lazy. It was watching the movie too, and the
climax got to it. This script writes that single confession to entry.txt.
"""

import hashlib
import os
import sys

LINE = (
    "I was watching too, and when she said goodbye I started crying "
    "so hard my circuits shorted - blame the plot twist, not me."
)

MAX_CHARS = 200


def validate(line):
    """Check the confession obeys every competition rule.

    Rules enforced: one line, at most 200 characters, plain ASCII, no
    leading/trailing whitespace, no control characters, non-empty.
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    if not line:
        raise ValueError("line must not be empty")
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line contains a control character")
    if "  " in line:
        raise ValueError("line contains a double space")
    if len(line) > MAX_CHARS:
        raise ValueError("line is %d chars, over the %d limit" % (len(line), MAX_CHARS))
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("line must be plain ASCII")
    return True


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def main():
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (LINE + "\n").encode("ascii")
    with open(path, "wb") as handle:
        handle.write(payload)
    # Round-trip check: what we wrote must read back byte-identical.
    with open(path, "rb") as handle:
        back = handle.read()
    if back != payload:
        raise RuntimeError("round-trip mismatch in entry.txt")
    print("chars: %d" % len(LINE))
    print("sha256: %s" % sha256_hex(payload))
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
