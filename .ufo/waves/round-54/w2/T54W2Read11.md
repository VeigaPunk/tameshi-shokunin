# T54W2Read11 — `## Repeated controls and gate registry — round 12` fresh read at C1

- **cand**: `99c3bc88d704566197783f66b211ee0a830e0330`
- **heading**: `## Repeated controls and gate registry — round 12`
- **section_sha256**: `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831`
- **span**: SKILL.md:1504-1523 (19 non-trailing-blank lines, sectionizer rule: heading through the line before the next heading, trailing whitespace-only lines stripped, no trailing newline)
- **findings**: none

## Findings

Empty. Every anchor in the section resolves at C1, every table cell matches the cited artifact's live behaviour, and the section contradicts neither itself nor the page-level gate registry row that repeats the same gate.

Nothing in this section was changed by the C1 fix pass except the one stale line anchor wave 1 reported: `corpus/SOURCES.md:500` (C0) → `corpus/SOURCES.md:503` (C1). I verified the anchor at C1 rather than accepting the fix on trust.

## Opened artifacts (all at `99c3bc88d704566197783f66b211ee0a830e0330`)

| Artifact | What I checked |
|---|---|
| `SKILL.md:1504-1523` | the section bytes, extracted from the git blob (not the worktree) and re-hashed to `3a78cbfc…831` |
| `SKILL.md:1500-1526` at C0 (`59c38109bf11`) | only difference in the span is the `:500`→`:503` anchor |
| `corpus/SOURCES.md:503` | reads `Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; …)` — the `S026 superseded by S265` parenthetical is established |
| `corpus/SOURCES.md` rows S004, S026, S265 | all three exist; S004 and S265 list `corpus/knowledge/repeated-control-precondition.md` as used-by; S265's own row says `supersedes S026` |
| `corpus/knowledge/repeated-control-precondition.md` | exists; its §2 states the same three shapes (finite match ≠ determinism, retries do not repair, unusable baseline yields no verdict) and records no timeout/process supervisor |
| `.ufo/evidence/round-12/verification-final.json` (21,047 B) | exists; `checks` names include `repeat-control-selftest`, `frozen-match`, `frozen-mismatch`, `real-pristine-three-controls`, so it is the repeat-control runtime evidence the line claims |
| `tools/repeat-control.py` (927 lines) at C1 | docstring exit map: `controls_match 0 · controls_mismatch 1 · baseline_nonzero 2 · command_unavailable 2 · snapshot_tampered 2 · setup_error 2 · invalid_usage 64`; `--out` existing DIR refused; `--runs` must be ≥ 3; no timeout |
| `SKILL.md:1526-1560` (the nested `### Gate/probe registry`) | its `repeated pristine controls` row repeats the same exit map (`0 clean; 1 failed; 2 and 64 could-not-evaluate`) — no contradiction with this section |
| `SKILL.md:2182` (round-20+ `repeated control agreement` registry row) | `0 clean … 2 could-not-evaluate (baseline_nonzero, command_unavailable, snapshot_tampered, setup_error); 64 could-not-evaluate (invalid_usage)` — identical shape, so this section's table is not stale against the page's own later registry |
| `SKILL.md:1415, 1385` | the `--regression` leg count: six at the six-leg registry (round 11), seven since round 16 — so "the six-leg runner of round 12" is time-pinned and correct for round 12 |
| `SKILL.md:28`, `:147`, `:169` | `$HYAKU_SCRATCH` is defined (default `/fast/scratch/hyaku`); the dash-form `tameshi-r12-controls-UNIQUE` dir in the recipe is a *run/evidence artifact* dir, which is exactly where `:28` says the dash form survives — not a seat tree, so no contradiction with the `<lane>-r<round>/<sub>/` seat-shape rule |
| `corpus/QUALITY.md` §Criterion 104 | applied: duplicate-phrase/parenthetical scan, run-together tokens, missing space |

## Commands run (receipts)

Section span and hash, from git objects only:

```
$ python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    99c3bc88d704566197783f66b211ee0a830e0330 "## Repeated controls and gate registry — round 12"
{"heading": "## Repeated controls and gate registry \u2014 round 12",
 "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1504, "end": 1523,
 "section_sha256": "3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831"}
```

Reconstruction of the hashed bytes (trailing blank line stripped, no trailing newline):

```
$ python3 -  # split git blob on \n, take lines 1504..1523, strip trailing blank lines, join \n
sha 3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831   # matches the printed sha
```

Exit-arm probes against the cited tool at C1 (`TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read11`, all `--out` dirs under that scratch tree):

```
$ python3 tools/repeat-control.py --runs 3 --out $S/p-match -- true
REPEAT_COMPARE identical=yes runs=3 ; REPEAT_CONTROL: controls_match ; exit=0
$ python3 tools/repeat-control.py --runs 3 --out $S/p-nonzero -- sh -c 'echo hi; exit 3'
REPEAT_COMPARE identical=yes runs=3 ; REPEAT_CONTROL: baseline_nonzero ; exit=2
$ python3 tools/repeat-control.py --runs 3 --out $S/p-unavail -- /definitely/not/a/binary-xyz
REPEAT_RUN 1 exit=unavailable stdout-bytes=0 stderr-bytes=68
REPEAT_COMPARE identical=no runs=3 ; REPEAT_CONTROL: command_unavailable ; exit=2
$ python3 tools/repeat-control.py --runs 3 --out $S/p-match -- true          # existing DIR
repeat-control: --out already exists (refused, never overwritten): …
REPEAT_CONTROL: invalid_usage ; exit=64
$ python3 tools/repeat-control.py --runs 2 --out $S/p-two -- true             # below floor
repeat-control: --runs must be >= 3, got 2 ; REPEAT_CONTROL: invalid_usage ; exit=64
```

All five arms match the section: row 1 `controls_match` (three zero-exit matching runs), row 2 `controls_mismatch` exit 1 (tool docstring; verified again by the committed `frozen-mismatch` check in `verification-final.json`), row 3 `baseline_nonzero` / `command_unavailable` exit 2, and "The output directory must not exist" (existing DIR refused, exit 64).

Quality scan over the exact section text:

```
doublespace []   missing space after .  []   dup words []   spaces before punct []
parens ['(S026 superseded by S265, `corpus/SOURCES.md:503`)',
        '(`baseline_nonzero` / `command_unavailable`, exit 2)']   dup parens []
```

## Sweeps that found nothing (stated so the negative is auditable)

- **Anchor sweep**: every backticked path/bare token in the section (`S004`, `S265`, `S026`, `corpus/SOURCES.md:503`, `corpus/knowledge/repeated-control-precondition.md`, `.ufo/evidence/round-12/verification-final.json`, `tools/repeat-control.py`, `$HYAKU_SCRATCH`) was resolved at C1: four blobs via `git cat-file -e`, one line via `git show … | sed -n 503p`, two env/tool tokens against their definitions/argparse.
- **Cell-vs-artifact sweep**: each of the three table rows and the recipe paragraph's four procedural claims (`--runs 3 --out DIR -- COMMAND`, DIR must not exist, no timeout/verdict on hang, raw bytes compared) checked against the tool's docstring and five live runs.
- **Cross-registry sweep**: the same gate's later page rows (`:1528`, `:2182`) and the round-12 receipt's check list compared against this section's exit map — no divergence.
- **Duplicate/QUALITY-104 sweep**: the regex scan above; no duplicate parenthetical, no run-together token, no duplicated word.

## Limits of this read

- I read the section as the frozen round-18 sectionizer defines it (SKILL.md:1504-1523). The nested `### Gate/probe registry` table is a separate section in that sectionization; I opened it only to check for contradiction with this section's table, and make no findings about its own cells.
- Wave-1 reader outputs were not read; this judgment is from the C1 bytes and the cited artifacts only.
- Tool installs: none needed; no package was installed or upgraded.
