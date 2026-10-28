# T54W2Read18 — cold read of `### Round-15 gate/probe registry` at C1

- Seat: `T54W2Read18`
- Heading: `### Round-15 gate/probe registry`
- Candidate revision: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Section range at C1: start 1702, end 1732
- `section_sha256` printed by `reader-section.py`: `78edbb693cdddcab61902811985918087529c444d3fb01da7bcaf4a674daf4ea`
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Read18` (`HYAKU_SCRATCH=/fast/scratch/hyaku`, `TMPDIR` set to it)

## Findings

1. `{"quote": "historical expected pins13 original inputs", "why": "The verb and its object count are run together as the nonexistent token `pins13`, where the cell means the historical expected manifest pins 13 original inputs (that manifest carries exactly 13 `inputs`), and every other occurrence in SKILL.md writes `pins ` with a space."}`

Byte evidence: the string sits in the "effective expectation disposition" row's Pinned-values cell (section-relative offset 2195; SKILL.md line 1707). The document writes `pins ` (with a space) 14 times and `pins13` twice — the second instance is the near-duplicate registry row at SKILL.md line 1627, outside this section's range and therefore not counted as this section's finding.

Command and output that show it:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md \
  | grep -n "pins13" | cut -c1-120
1627:| effective expectation disposition | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/ev
1707:| effective expectation disposition | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/ev

$ grep -o "pins1[0-9]\|pins [0-9]*" SKILL.C1.md | sort | uniq -c
     14 pins 
      2 pins13
```

The count is also factually right once the space is restored: `.ufo/evidence/round-13/expected.json` at C1 has `inputs: 13` (`git show 99c3bc8:.ufo/evidence/round-13/expected.json | python3 -c "import json,sys;print(len(json.load(sys.stdin)['inputs']))"` → `13`), so the defect is the missing space, not a wrong number.

## What was checked and cleared (no finding)

### Anchors resolve at C1

| Anchor in the section | Check | Result |
|---|---|---|
| `tools/context-capture.py` (entry and `--selftest`) | `git ls-tree -r 99c3bc8 -- tools/` and `git show 99c3bc8:tools/context-capture.py` | present |
| `tools/evidence-disposition.py` (entry and `--selftest`) | same | present |
| `.ufo/evidence/round-14/context-receipt.json` sha256 `05cb55b8…` | `git show 99c3bc8:.ufo/evidence/round-14/context-receipt.json \| sha256sum` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` — matches the pinned cell |
| negative fixture `context-missing-env.json` sha256 `1ee9d09b…` | `git show 99c3bc8:.ufo/evidence/round-14/context-missing-env.json \| sha256sum` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` — matches |
| built-in id/exit pin | `git show 99c3bc8:tools/context-capture.py` (lines 150-160) | `FROZEN_EXPECTED_ID = "context_consistent"`, `FROZEN_EXPECTED_EXIT = 0` |
| expected-pin schema `tameshi-context-expected-v1` and keys `receipt_sha256`/`id`/`exit` | tool line 141 (`EXPECTED_SCHEMA`), line 265 (`EXPECTED_KEYS` adds the schema key) | resolves |
| `.ufo/evidence/round-14/dispositions.json` and its before counterpart | `git ls-tree 99c3bc8 .ufo/evidence/round-14/` | `dispositions.json`, `dispositions-before.json` both present |
| live entry `.ufo/evidence/round-18/dispositions.json` → 0 | `git ls-tree 99c3bc8 .ufo/evidence/round-18/` (manifest present); all four pinned `inputs` digests recomputed at C1 match; `historical_inputs` waivers present | not stale |
| `git archive 28aeef4` | `git cat-file -t 28aeef4` → `commit` | resolves |
| "see the round-17 re-pin section" | `## Live-tree re-pin and entry-command monitor — round 17` exists (SKILL.md:1840), and its recipe states the same round-18 manifest → `0 clean`, `effective: 11`, `superseded: 1` | resolves |
| the Gate standard's "Two evidences" | external (`PROTOCOL.md:390-397` per committed round-15/round-18 seat notes); not a lane anchor | out of lane, unchanged |

### Verdict-map and exit-class cells against the artifacts they cite

- `0 clean (context_consistent)`, `missing_injected_environment` exit 1, `snapshot_tampered` exit 2, `usage_error` exit 64: all literal in `tools/context-capture.py` (docstring lines 62-89 and the code paths).
- "A clean result with a wrong id/exit pin becomes failed/exit1" — `apply_expected()` raises `expected_verdict_mismatch` and sets exit 1 only when `result["exit"] == 0`; a could-not-evaluate result stays at its nonzero exit, matching "could-not-evaluate takes precedence".
- "Help exits0" — `main()` returns 0 for `-h/--help` in both cited tools.
- "context-capture's selftest exits 0/1/2 … and 64 for invalid invocation" — `parse_argv` raises `UsageError` before the selftest dispatch, `run_selftest()` returns `harness.finish()` or 2 on setup error.
- "the disposition selftest: 0 pass, 1 case failure, 2 could-not-evaluate — an unusable scratch root … named, never a traceback" — `main()` catches `ScratchRootUnusable` around `selftest()` and returns 2 with the message (`strict_scratch_root()` names the `TMPDIR` value); usage is 64 before dispatch.
- Reproduction of the *policy* cells was not needed: the C0→C1 diff for this section is one line (the exit-arm sentence), so the rest of the section was already read at C0; only the bytes at C1 were judged here.

### Structure

Scripted check over the extracted section: every table line has 9 pipes (8 columns), zero unbalanced parentheses, no double spaces, no trailing whitespace; 31 lines, newline-terminated.

## Observations that are not graded as findings (and why)

- `Pre-integration wave1 capture/root-override recipes` (SKILL.md:1723): the prose elsewhere says "wave 1"/"wave 2", but `wave1` is also a machine identifier in this repo (`.ufo/waves/round-21/capacity-before-wave1.json`, `"name": "wave1"` in bundle JSON), so I could not defend it as certainly a missing space and did not grade it.
- `stays exit2`, `failed/exit1`, `Help exits0`: the whole surrounding round-14 block (SKILL.md lines 1653-1690, 2033) uses this compact `exitN` form as house shorthand (16 `exit 2` vs 2 `exit2`, but the compact form is used deliberately in those cells), so it is not a missing space.

## Artifacts opened

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` at `99c3bc88d704566197783f66b211ee0a830e0330`, lines 1702-1732 (the section), plus lines 1560-1620, 1653-1690, 1840-1900 for cross-reference.
- `99c3bc8:tools/context-capture.py` (docstring, `run_check`, `apply_expected`, `parse_argv`, `main`).
- `99c3bc8:tools/evidence-disposition.py` (`ScratchRootUnusable`/`strict_scratch_root`, `emit_could_not_evaluate`, `parse_argv`, `main`, `selftest`).
- `99c3bc8:.ufo/evidence/round-14/context-receipt.json`, `.ufo/evidence/round-14/context-missing-env.json`, `.ufo/evidence/round-14/dispositions.json`, `.ufo/evidence/round-18/dispositions.json`, `.ufo/evidence/round-13/expected.json`.
- `.ufo/waves/round-54/spec-w2.json` (reader discipline), `corpus/QUALITY.md` (criterion numbering), `.ufo/waves/round-54/w2/` listing.
- `.ufo/evidence/round-54/reader-section.py` output only (not edited).

## Commands run

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read18 && export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read18
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 99c3bc88d704566197783f66b211ee0a830e0330 "### Round-15 gate/probe registry"
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf11 "### Round-15 gate/probe registry"
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md   # lines 1702-1732 to scratch, then inspected
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf11:SKILL.md   # same range, diffed C0 vs C1
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 59c38109bf11 99c3bc88d704566197783f66b211ee0a830e0330 --stat
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc8:.ufo/evidence/round-14/context-receipt.json | sha256sum
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc8:.ufo/evidence/round-14/context-missing-env.json | sha256sum
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc8:.ufo/evidence/round-18/dispositions.json   # pinned inputs
for p in <four manifest inputs>; do git -C ... show 99c3bc8:$p | sha256sum; done
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -t 28aeef4
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc8:tools/context-capture.py | grep -n "context_consistent|missing_injected_environment|snapshot_tampered|usage_error|FROZEN_*"
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc8:tools/evidence-disposition.py | grep -n "ScratchRootUnusable|strict_scratch_root|def main|return 64"
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -n "Two evidences" 99c3bc8 -- .
```

Python structural check (pipes/parentheses/double spaces) and the `pins13` substring/count check were run inside the scratch dir on the extracted section bytes.

## Bounds honoured

- No lane file, counter, contract, freeze, ledger, registry or wave spec was edited; no `SKILL.md` edit; no git/jj mutation anywhere.
- Only written paths: `.ufo/waves/round-54/w2/T54W2Read18.json` and `.ufo/waves/round-54/w2/T54W2Read18.md`.
- No tool installation or upgrade was needed; nothing was installed or updated.
