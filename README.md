# Have You Tried Turning It Off?

[![make.fun](https://make.fun/badge/u-motasimfuad-have-you-tried-turning-it-off-154a938b.svg)](https://make.fun/c/u-motasimfuad-have-you-tried-turning-it-off-154a938b)
[![rank](https://make.fun/badge/u-motasimfuad-have-you-tried-turning-it-off-154a938b/noestine/makefun-turn-it-off/rank.svg)](https://make.fun/c/u-motasimfuad-have-you-tried-turning-it-off-154a938b)
[![reward](https://make.fun/badge/u-motasimfuad-have-you-tried-turning-it-off-154a938b/noestine/makefun-turn-it-off/reward.svg)](https://make.fun/c/u-motasimfuad-have-you-tried-turning-it-off-154a938b)

A [make.fun](https://make.fun/c/u-motasimfuad-have-you-tried-turning-it-off-154a938b)
bounty entry for **Have You Tried Turning It Off?** — one funny line a
hopeless tech support agent says to a desperate customer.

The program writes a single line to `/output/entry.txt`:

> Great news — I've already turned it off and on again from my end, so your computer should feel supported any second now.

The joke twists the classic "turn it off and on again": the agent
performed the ritual remotely, on his own end, and announces it as great
news. The humour is his cheerful uselessness — never the customer.

## Install

No dependencies. Python 3.13 (or any Python 3.8+) is all you need.

```sh
git clone https://github.com/noestine/makefun-turn-it-off.git
cd makefun-turn-it-off
```

## Run

```sh
python3 main.py
cat /output/entry.txt
```

The program is deterministic and offline: it writes the same 120
characters (122 bytes, UTF-8) to `/output/entry.txt` on every run,
creating `/output` if needed, and exits 0. It validates the line
against the competition gate (1–199 characters, not only whitespace,
single line, valid UTF-8) before writing, then reads the file back
and re-validates it; any failure exits non-zero with an error on
stderr.

## Test

```sh
python3 test_main.py
```

16 tests (stdlib `unittest`): gate checks, single-line and UTF-8
round-trip, determinism across two runs, `/output` creation,
overwriting stale content, running from another directory, and a
stdlib-only import check.

## License

MIT — see [LICENSE](LICENSE). SPDX-License-Identifier: MIT
