source: S152 — https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download — abstract fragility sentence, opened 2026-10-24
verified-at: 2026-10-24
recheck: 365d
ground: F4 write forms the round-39 pattern missed

# Two write forms the frozen census pattern does not see

## What the tool adds

`tools/write-path-census-v2.py` classifies two forms that `tools/write-path-census.py` (pin `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62`) misses. A string literal `expected.json` on a `.write_bytes` call is an expected-path token for v2 and not for v1. `os.replace(` is a write site for v2 and not for v1. The planted fixtures in `.ufo/evidence/round-40/census/fixtures.json` are the discriminating set: unflagged cases count, flagged cases and a `/tmp` replace do not.

## Why the source is cited

S152's abstract says fragility and lack of context in snapshot files can lead to false positives. An unseen write of an expected file is the lane's version of that gap. The citation is that sentence, not a count of the lane's gates. S108 is not support for this entry.

## What is not claimed

The live hits are two named sites: `tools/registry-replay.py` writes `'expected.json'` via `.write_bytes`, and `tools/bash-witness-study.py` calls `os.replace`. Those are the pattern's hits. They are not a claim that every write in the tree is classified, and not a claim that the `os.replace` site writes an expected value. The destination there is a variable.
