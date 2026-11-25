"""Tests for main.py — Have You Tried Turning It Off?

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-199
characters, not only whitespace. The judge additionally requires a
single funny line from a hopeless tech support agent to a desperate
customer. Tests are written first and run before main.py exists.
Stdlib only.
"""

import hashlib
import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent
MAIN = REPO / "main.py"
OUTPUT = Path("/output/entry.txt")

EXPECTED = (
    "Great news \u2014 I've already turned it off and on again from my end,"
    " so your computer should feel supported any second now."
)


def run_main(cwd=None):
    return subprocess.run(
        [sys.executable, str(MAIN)],
        cwd=str(cwd or REPO),
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestLine(unittest.TestCase):
    def test_line_length_in_gate(self):
        self.assertGreaterEqual(len(EXPECTED), 1)
        self.assertLessEqual(len(EXPECTED), 199)

    def test_line_not_only_whitespace(self):
        self.assertTrue(EXPECTED.strip())

    def test_line_is_single_line(self):
        self.assertNotIn("\n", EXPECTED)
        self.assertNotIn("\r", EXPECTED)

    def test_line_is_valid_utf8(self):
        raw = EXPECTED.encode("utf-8")
        self.assertEqual(raw.decode("utf-8"), EXPECTED)

    def test_line_mentions_the_classic_with_a_twist(self):
        lowered = EXPECTED.lower()
        self.assertIn("turned it off and on again", lowered)
        # The twist: the agent did it remotely, on his own end.
        self.assertIn("from my end", lowered)

    def test_line_is_agent_voice_not_customer_mockery(self):
        # Cheerful-useless agent voice; no second-person blame.
        self.assertIn("Great news", EXPECTED)
        self.assertNotIn(" you ", EXPECTED.lower().replace("your", ""))
        self.assertNotIn("your fault", EXPECTED.lower())


class TestProgram(unittest.TestCase):
    def setUp(self):
        if OUTPUT.exists():
            OUTPUT.unlink()

    def test_main_exists(self):
        self.assertTrue(MAIN.is_file(), "main.py must exist at repo root")

    def test_run_exits_zero_and_writes_file(self):
        result = run_main()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(OUTPUT.is_file())

    def test_output_content_exact(self):
        run_main()
        raw = OUTPUT.read_bytes()
        self.assertEqual(raw.decode("utf-8"), EXPECTED)
        self.assertEqual(raw, EXPECTED.encode("utf-8"))

    def test_output_passes_gate(self):
        run_main()
        text = OUTPUT.read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text), 1)
        self.assertLessEqual(len(text), 199)
        self.assertTrue(text.strip())
        self.assertNotIn("\n", text)

    def test_deterministic_across_two_runs(self):
        run_main()
        first = OUTPUT.read_bytes()
        run_main()
        second = OUTPUT.read_bytes()
        self.assertEqual(first, second)
        self.assertEqual(
            hashlib.sha256(first).hexdigest(),
            hashlib.sha256(second).hexdigest(),
        )

    def test_creates_output_dir_when_missing(self):
        import shutil

        if Path("/output").exists():
            shutil.rmtree("/output")
        result = run_main()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(OUTPUT.is_file())

    def test_overwrites_stale_longer_content(self):
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(b"X" * 500 + b"\n trailing junk\n")
        result = run_main()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(OUTPUT.read_bytes(), EXPECTED.encode("utf-8"))

    def test_runs_from_another_directory(self):
        # Cwd-independence: the program must not depend on the cwd.
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            result = run_main(cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                OUTPUT.read_bytes(), EXPECTED.encode("utf-8")
            )

    def test_em_dash_byte_round_trip(self):
        run_main()
        raw = OUTPUT.read_bytes()
        # Em dash U+2014 is 3 bytes in UTF-8; char count != byte count.
        self.assertIn("—".encode("utf-8"), raw)
        self.assertEqual(len(raw), len(EXPECTED.encode("utf-8")))
        self.assertGreater(len(raw), len(EXPECTED))

    def test_stdlib_only_imports(self):
        text = MAIN.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                module = stripped.split()[1].split(".")[0]
                self.assertIn(
                    module,
                    {"os", "pathlib", "sys"},
                    f"non-stdlib or unexpected import: {stripped}",
                )


if __name__ == "__main__":
    unittest.main()
