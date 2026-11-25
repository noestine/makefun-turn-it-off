"""Have You Tried Turning It Off? — make.fun entry.

Writes one funny single line a hopeless tech support agent says to a
desperate customer to /output/entry.txt.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-199
characters, not only whitespace. The line is a single line, ~120
characters, deterministic, stdlib only, no network, no input.
"""

import sys
from pathlib import Path

LINE = (
    "Great news \u2014 I've already turned it off and on again from my end,"
    " so your computer should feel supported any second now."
)

OUTPUT_PATH = Path("/output/entry.txt")


def validate(text):
    """Check the line against the sealed gate. Returns an error string
    or None when the text passes."""
    if not isinstance(text, str):
        return "entry is not text"
    if not (1 <= len(text) <= 199):
        return f"entry is {len(text)} characters, must be 1-199"
    if not text.strip():
        return "entry is only whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if any(ord(ch) < 0x20 for ch in text):
        return "entry contains control characters"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8"
    return None


def main():
    error = validate(LINE)
    if error is not None:
        print(f"error: {error}", file=sys.stderr)
        return 1
    try:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_bytes(LINE.encode("utf-8"))
        # Verify what actually landed on disk: read it back and
        # re-validate, so a partial or mangled write never passes
        # silently as a successful run.
        written = OUTPUT_PATH.read_bytes().decode("utf-8")
        error = validate(written)
        if error is not None:
            print(f"error: written file failed validation: {error}",
                  file=sys.stderr)
            return 1
        if written != LINE:
            print("error: written file differs from the entry line",
                  file=sys.stderr)
            return 1
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
