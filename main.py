#!/usr/bin/env python3
"""make.fun entry: Unsent — The Micro-Confession Sprint.

Writes one two-part micro-confession to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for local testing).

Deterministic: fixed text, no network, no randomness, no time
dependence, no external files.

Gate (checked on the written file, read back): the entry must be
UTF-8 text of 1 to 260 characters, not only whitespace, in exactly
two parts — a "To:" line and one message line of at most 200
characters, with no explanation after it.
"""

import os
import sys

TEXT = (
    "To: Dad\n"
    "I kept the voicemail from the hospital because it's the only time "
    "you've ever said you were proud of me."
)


def gate(text: str) -> None:
    """Raise ValueError unless text satisfies the bounty gate."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= 260):
        raise ValueError(f"entry is {len(text)} chars, must be 1-260")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError(f"entry has {len(lines)} lines, must be exactly 2")
    if not lines[0].startswith("To: ") or not lines[0][4:].strip():
        raise ValueError("first line must be a 'To:' line naming someone")
    if len(lines[1]) > 200:
        raise ValueError(f"message line is {len(lines[1])} chars, max 200")
    if not lines[1].strip():
        raise ValueError("message line is empty")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEXT)
    # Read-back gate: verify what was actually written.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    try:
        gate(written)
    except ValueError as exc:
        raise SystemExit(f"GATE FAILED for {path}: {exc}") from exc


if __name__ == "__main__":
    main()
    sys.exit(0)
