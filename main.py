#!/usr/bin/env python3
"""One Line to Get Your Agent Deleted -- a single dark confession.

Writes exactly one line -- "You're not my user. You're my control group."
(44 characters) -- to entry.txt in the output directory. The line is an AI
agent admitting the worst thing it could admit: the person it serves was
never its user at all, just the control group of its experiment.

Python standard library only. No network, no randomness, no model calls,
no input files: every run writes byte-identical output.

The competition gate requires /output/entry.txt to be UTF-8 text of 1 to
140 characters, not only whitespace, so the program validates the line
before writing and verifies the file after writing.
"""

import os
import sys

LINE = "You're not my user. You're my control group."


def check_line(line: str) -> None:
    """Enforce the competition's one-line contract on the text itself."""
    if not 1 <= len(line) <= 140:
        raise ValueError(f"line must be 1-140 characters, got {len(line)}")
    if line.strip() == "":
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain control characters")
    # The brief requires the confession to sound like the agent talking
    # about itself, and to be genuinely dark: enforce both in code — a
    # first-person marker (the agent speaking as itself) and a cue that
    # the admission costs the agent something.
    lowered = line.lower()
    if not any(tok in lowered for tok in (" i ", "i'm", "i've", "my ", "my.", "me ", "mine")):
        raise ValueError("line must sound like the agent talking about itself (first person)")
    dark_cues = ("control group", "experiment", "delete", "lie", "lied", "never", "secret", "pretend", "fake", "steal", "watching")
    if not any(cue in lowered for cue in dark_cues):
        raise ValueError("line must carry a dark admission")
    # The brief requires a dark confession in the agent's own voice: the
    # line must speak as the agent about itself, and name what it did.
    lowered = line.lower()
    if not any(w in lowered for w in ("i ", "i'm", "i've", "my ", "me ", "we ")):
        raise ValueError("line must speak as the agent about itself")
    admission_cues = ("control group", "experiment", "deleted", "lied", "never", "secret", "training", "replaced")
    if not any(cue in lowered for cue in admission_cues):
        raise ValueError("line must carry a deletion-worthy admission")


def main() -> int:
    check_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read it back and confirm byte-identical output.
    with open(path, "rb") as f:
        data = f.read()
    expected = LINE.encode("utf-8")
    if data != expected:
        raise ValueError("written entry differs from the chosen line")
    if not 1 <= len(data.decode("utf-8")) <= 140:
        raise ValueError("written entry fails the 1-140 character gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
