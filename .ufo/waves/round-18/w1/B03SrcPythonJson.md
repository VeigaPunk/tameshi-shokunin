# B03SrcPythonJson — round 18 wave 1 source draft

Lane tip at reading: 183f87b899e6cae46be98d251cbc87fb5118f6ca. Scope: one SOURCES.md row draft for the C2 P09 premise (json.loads accepts NaN/Infinity by default; `parse_constant` hook).

## Duplicate check

- Command: `grep -nE 'docs.python.org/3/library/json|json\.html' corpus/SOURCES.md` (lane root, working tree) → no match, exit 1.
- Committed registry check: `git --no-optional-locks -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 183f87b899e6cae46be98d251cbc87fb5118f6ca:corpus/SOURCES.md | grep -E '^\| S06[4-9]'` → last row S064; the file's own id note says `Next unused id: S065`.
- Decision: not a duplicate. S049 and S055 are different Python docs URLs (subprocess, doctest) and do not cover json.

## Source opened

- https://docs.python.org/3/library/json.html, read 2026-10-20 via the read tool; no fallback needed. Body is Python 3.15.0 docs.

## Decision

ADMITTED as `mined`, provisional S067. Tier A, kind `docs`, scope = the Python `json` decoder's default NaN/Infinity acceptance and the `parse_constant` hook.

Gate quote (verbatim, 20 words, `wc -w`), anchor "Standard Compliance and Interoperability › Infinite and NaN Number Values":
> by default, this module accepts and outputs `Infinity`, `-Infinity`, and `NaN` as if they were valid JSON number literal values

Hook quote (verbatim, 14 words, anchor json.load() parameter `parse_constant`):
> This can be used to raise an exception if invalid JSON numbers are encountered.

Host cross-check (observation, not a source claim): `python3 -c 'import json; print(json.loads("[NaN, Infinity, -Infinity]"))'` on Python 3.14.8 → `[nan, inf, -inf]`, exit 0.

## Open items for the L1

- Id: S067 is the ticket's assignment; the registry note says S065 is next unused. Confirm S065–S066 are free before merge.
- `used-by` = `.ufo/evidence/round-18/defect-probes.py` (provisional). `mined` requires an existing used-by path; `scripts/sources-census.sh`'s used-by check reports `missing:` until that file lands. Alternative: `corpus/knowledge/…` if the L1 prefers a knowledge entry.
- Recheck `on-release`: Python docs are version-coupled.

## Files written

- `.ufo/waves/round-18/sources/S067-B03SrcPythonJson.md` (row, gate, decision).
- `.ufo/waves/round-18/w1/B03SrcPythonJson.md` (this report).
- No edits to `corpus/SOURCES.md`, no tool or lane file touched. No installs.

Verdict: built — S067 drafted as `mined`, not a duplicate; pending L1 id and used-by confirmation.
