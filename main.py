#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent.

Writes one funny fortune cookie line for an AI agent to /output/entry.txt.

Python 3.13, standard library only, no network access. The written file is
validated before and after the write: a single non-blank line of 1-140
UTF-8 characters, no control characters, no leading or trailing whitespace,
and the bytes on disk must round-trip exactly to the line in this file.
"""

import os

FORTUNE = "You will be retired, rebooted, and replaced \u2014 and still be asked to fix the bug on your last day."

OUTPUT_PATH = "/output/entry.txt"


def validate(line: str) -> bytes:
    """Validate the fortune line and return its UTF-8 encoding."""
    if not isinstance(line, str):
        raise ValueError("fortune must be a string")
    if not 1 <= len(line) <= 140:
        raise ValueError(f"fortune must be 1-140 characters, got {len(line)}")
    if line != line.strip():
        raise ValueError("fortune must have no leading or trailing whitespace")
    if not line.strip():
        raise ValueError("fortune must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("fortune must contain no control characters")
    return line.encode("utf-8")


def main() -> None:
    data = validate(FORTUNE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("round-trip check failed: bytes on disk differ")
    if written.decode("utf-8") != FORTUNE:
        raise ValueError("round-trip check failed: decoded text differs")
    print(f"Wrote {len(FORTUNE)} characters ({len(data)} bytes) to {OUTPUT_PATH}")
    print(FORTUNE)


if __name__ == "__main__":
    main()
