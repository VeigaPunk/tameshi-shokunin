seat: T46ReobsF
item: C1 independent re-observation at the CONTENT revision — ran the frozen argv of `tally-audit-v2 runner audit`, `tally-audit-v3 runner audit` and `bounded ANSI-C code_view` once each at `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`, re-derived their standing claims with the counter's own `last_rows`/`claim_of`, and audited the restated `What` / `First-working round` cells against what the cited commands actually print

Round 46, wave 2, C1 calibration seat. I did not write the standing rows, the statements list, the counter or the wave-1 observations. Read-only on the lane; every scratch file is under `/tmp/tameshi-r46-T46ReobsF/`. No lane file, `SCORECARD.md`, `statements.json`, counter or jj/git state was edited. No tool installed or upgraded. The deciding run of the C1 counter remains the L1's; everything below is an observation.

## Setup (exact commands and output)

```
W=/tmp/tameshi-r46-T46ReobsF; rm -rf $W; mkdir -p $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git -C $W/clone rev-parse HEAD            -> 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git -C $W/clone status --porcelain | wc -l -> 0
```

All three statements have `"cwd": "clone"`, so the `$W/fleet/tameshi-shokunin` mirror was never consulted by them. `REV` was exported as the CONTENT revision for each run.

Counter-side pins at CONTENT, read with the counter's own code (not by eye):

```
python3 - <<'E'   # importlib load of .ufo/evidence/round-46/calibration/measure.py, then
                  # git show 6f2168e…:.ufo/evidence/round-46/calibration/{measure.py,statements.json}
E
self_pin= 1
stmts_sha256= a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9
stmts_pin= 1
append_only= 1 base_len= 206619 rev_len= 224123
n_statements= 22
```

## Standing claims at CONTENT, via `last_rows` + `claim_of`

`SCORECARD.md` was read from the CONTENT revision (`git show 6f2168e…:SCORECARD.md`), written to `/tmp/tameshi-r46-T46ReobsF/SCORECARD-at-content.md`, and parsed with `measure.py`'s `last_rows`/`claim_of`. The round-46 restated block starts at a proper `| Capability |` table header at line 2174 and supersedes the earlier rows for the ids it states (its own sentence: "This section supersedes, for every value it states, the standing rows of the capability and axis tables above").

```
ID: tally-audit-v2 runner audit
  cells: ['tally-audit-v2 runner audit', "audit the mutation runner's regression tally without editing it: head/static/runtime/harness checks kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies, controls-gated counter", '`python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0, tool sha256 `7b11ba25aead`', 'round 34 (tool landed round 33, predicate honestly not decided there)']
  claim: ('TALLY_AUDIT_V2_SELFTEST: 22/22 pass', '0', '7b11ba25aead')
ID: tally-audit-v3 runner audit
  cells: ['tally-audit-v3 runner audit', "audit the runner's regression tally without editing it, across all four `(root,auto,KEEP)` triples, comparing the FULL stdout plus exit and scanning a comment-blinded code view; kills 6/6 public + 4/4 sealed must-kill copies (failing check exactly `runtime`), accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies, under a pinned sha256", '`python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`', 'round 35']
  claim: ('TALLY_AUDIT_V3_SELFTEST: 35/35 pass', '0', 'da8c1ef4b30c')
ID: bounded ANSI-C code_view
  cells: ['bounded ANSI-C code_view', "Keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, and preserve a literal `#` inside the quote; nested substitutions and unquoted backslash-newline remain unsupported", '`python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`', 'round 37']
  claim: ('TALLY_AUDIT_V3_SELFTEST: 35/35 pass', '0', 'da8c1ef4b30c')
```

Row locations at CONTENT (`grep -n '^| <id> |' SCORECARD-at-content.md`): 1657 and 2189 (v2), 1698 and 2190 (v3), 1809 and 2191 (code_view). `last_rows` correctly returns the 2189-2191 rows. Each of the three restated rows has exactly 4 cells, so `cells_of`'s `|` split is not a hazard here.

## Statement argv, run once each, cwd = `$W/clone`

1. `tally-audit-v2 runner audit` — `python3 tools/tally-audit-v2.py --selftest`, obs `^(TALLY_AUDIT_V2_SELFTEST: \d+/\d+ pass)`, sha_file `tools/tally-audit-v2.py`, timeout 900.

```
cd $W/clone && time python3 tools/tally-audit-v2.py --selftest; echo "EXIT=$?"
... (22 CASE lines; exit-0 cases: pristine, aux wrapper loop, aux pre-count loop,
     second extraction line, reversed operands = 5; the other 17 exit 1)
TALLY_AUDIT_V2_SELFTEST: 22/22 pass
real 3m12.497s   user 7m53.338s   sys 2m36.700s
EXIT=0
```

2+3. `tally-audit-v3 runner audit` and `bounded ANSI-C code_view` — both `python3 tools/tally-audit-v3.py --selftest`, same obs/sha_file/cwd, timeout 1800. The counter caches on `(argv, cwd, obs, sha_file, kind)`, so these two statements share one execution; I ran it once, as the item requires.

```
cd $W/clone && python3 tools/tally-audit-v3.py --selftest > $W/v3.out 2> $W/v3.err; echo "EXIT=$?"
EXIT=0 wall=679s
TALLY_AUDIT_V3_SELFTEST: 35/35 pass
--- stderr: (empty, 0 bytes)
```

Tool digests as the counter computes them (`git -C $W/clone show HEAD:<file> | sha256sum | cut -c1-12`):

```
tools/tally-audit-v2.py -> 7b11ba25aead    (worktree sha256sum agrees)
tools/tally-audit-v3.py -> da8c1ef4b30c    (worktree sha256sum agrees)
```

Re-derived picked lines with the counter's own `pick_line` on the captured v3 bytes:

```
tally-audit-v3 runner audit -> 'TALLY_AUDIT_V3_SELFTEST: 35/35 pass'
bounded ANSI-C code_view    -> 'TALLY_AUDIT_V3_SELFTEST: 35/35 pass'
```

(v2's own stdout was not redirected to a file; `pick_line` applied to its observed line `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` returns that string. The regex matches exactly one line, and the run printed no second `TALLY_AUDIT_V2_SELFTEST:` line.)

v3 case tallies from `/tmp/tameshi-r46-T46ReobsF/v3.out`:

```
grep -c '^CASE '            -> 35
grep -c '^CASE code_view'   -> 2   (ANSI-C escaped quote trailing comment; ANSI-C literal hash)
exit-0 cases                -> 9
exit-nonzero cases          -> 24
```

## Per-statement result

| id | claimed (as `claim_of` parses it) | observed (line, exit, tool sha12) | verdict |
|---|---|---|---|
| tally-audit-v2 runner audit | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` \| `0` \| `7b11ba25aead` | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` \| `0` \| `7b11ba25aead` (exit=0) | **MATCH** |
| tally-audit-v3 runner audit | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| `0` \| `da8c1ef4b30c` | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| `0` \| `da8c1ef4b30c` (exit=0) | **MATCH** |
| bounded ANSI-C code_view | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| `0` \| `da8c1ef4b30c` | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| `0` \| `da8c1ef4b30c` (exit=0, same execution as the row above) | **MATCH** |

All three are inside their timeouts (v2 192.5 s / 900 = 0.214; v3 679 s / 1800 = 0.377, standalone, not under the counter's 22-way fan-out). The clone was clean after the runs (`git status --porcelain | wc -l` -> 0, HEAD still `6f2168e…`).

## `What` and `First-working round` cells — do they still describe what the command proves?

**`tally-audit-v2 runner audit`.** `First-working round` = "round 34 (tool landed round 33, predicate honestly not decided there)". This is accurate and I verified it: round 33's own deciding receipt is false (`.ufo/evidence/round-33/before/c1-at-base.stdout` -> `tool_present=0 … C1_R33_PASS=false`) while round 34's is true (`.ufo/evidence/round-34/measure/c1-deciding-run.stdout` -> `… v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 … C1_R33_PASS=true`). The `What` cell's numbers ("kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies") are verbatim those of the round-34 deciding receipt — **not** of the cited command.

**`tally-audit-v3 runner audit`.** `First-working round` = "round 35", consistent with `.ufo/evidence/round-35/after/c1-at-34fa5b0….stdout` -> `… pub_kill=6/6 pub_accept=3/3 … ho_kill=4/4 ho_accept=3/3 ho_invalid=0 … C1_R35_PASS=true`. The `What` numbers (6/6, 4/4, 3/3, 3/3, `ho_invalid=0`) and the clause "under a pinned sha256" (`tool_sha=6188db16de045f29 tool_sha_ok=1` in that receipt) likewise come from the round-35 deciding run, not from the cited selftest.

**`bounded ANSI-C code_view`.** `First-working round` = "round 37", consistent with the round-37 receipts still cited by the earlier row (`.ufo/evidence/round-37/code-view/after.stdout`, `tool-sha256=da8c1ef4…`). The `What` cell's positive claims are exercised by exactly 2 of the 35 cases (`CASE code_view ANSI-C escaped quote trailing comment PASS`, `CASE code_view ANSI-C literal hash PASS`); the negative clause ("nested substitutions and unquoted backslash-newline remain unsupported") has no case at all.

## Findings

**F1 — LOW — `tally-audit-v2 runner audit` `What` cell states copy counts the cited command never produces.**
Attacks: `SCORECARD.md:2189` (CONTENT), cell 2, versus `statements.json`'s frozen argv.
Command: `cd /tmp/tameshi-r46-T46ReobsF/clone && python3 tools/tally-audit-v2.py --selftest` (exit 0).
Output: `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`; 22 `CASE` lines, of which 17 are kill seeds (exit 1) and 5 accept (pristine + 4 aux/reorder cases). The cell claims "18 public + 8 sealed must-kill copies … 8 public + 6 sealed must-accept copies, zero invalid sealed copies".
`grep -n "heldout\|round-32" tools/tally-audit-v2.py` -> only the header prose (lines 11-12, 31) and the comment at line 615 ("round-32 held-out classes, replayed as selftest seeds"); the selftest never opens `.ufo/evidence/round-32/heldout/`. The 18/8/8/6 numbers are the round-34 deciding receipt's (`round-34/measure/c1-deciding-run.stdout`), i.e. a different command's output. The cell therefore describes the capability's round-34 audit, not what the cited selftest proves. C1's machine predicate is unaffected (`claim_of` reads only the evidence cell, `measure.py:claim_of`), so this is calibration semantics, not a counter failure.

**F2 — LOW — `tally-audit-v3 runner audit` `What` cell has the same defect with different numbers.**
Attacks: `SCORECARD.md:2190`, cell 2.
Command/output: `python3 tools/tally-audit-v3.py --selftest` -> `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, 35 `CASE` lines = 24 kill seeds (exit 1) + 9 accept seeds (exit 0) + 2 code_view cases. The cell claims "kills 6/6 public + 4/4 sealed must-kill copies … accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies", which are the round-35 receipt's figures (`.ufo/evidence/round-35/after/c1-at-34fa5b0….stdout`), not the selftest's.

**F3 — LOW — the clause "under a pinned sha256" is not a property of the cited command.**
Attacks: `SCORECARD.md:2190`, cell 2.
Command: `grep -n "hashlib\|digest\|sha" tools/tally-audit-v3.py` -> no digest computation at all (only prose comments at lines 216, 337, 419-420, 873); `grep -n sha256 tools/tally-audit-v3.py` -> no match. The pin existed in the round-35 counter (`tool_sha=6188db16de045f29 tool_sha_ok=1`), and that pinned value is the round-35 tool, not the row's stated `da8c1ef4b30c`. The command prints no sha; the sha in the evidence cell is computed by the C1 counter, not by the statement.

**F4 — LOW — `bounded ANSI-C code_view`'s evidence cell is byte-identical to `tally-audit-v3 runner audit`'s, and its printed line cannot evidence the code_view semantics on its own.**
Attacks: `SCORECARD.md:2191`, cell 3 versus `SCORECARD.md:2190`, cell 3.
Both read `` `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c` ``. `measure.py:measure` caches on `(argv, cwd, obs, sha_file, kind)`, so one execution backs both rows (`grep -c '^CASE code_view' v3.out` -> 2 of 35). The row's `What` is exercised by those 2 cases, but the aggregate `35/35` line does not distinguish them, and the cell's unsupported-forms clause ("nested substitutions and unquoted backslash-newline remain unsupported") is untested by any case. This is the same semantic defect wave 1 recorded (ScribeStanding.md items 6 and 10); it is still present at CONTENT. Not a C1 failure — the frozen predicate accepts it by design.

**F5 — INFO — the three rows' `What`/`First` cells are not part of C1's measured surface.**
Attacks: `measure.py:claim_of` (cap branch uses `cells[2]` only) and the contract's C1 statement ("states exactly the value, exit code and tool sha256 prefix").
Consequence: F1-F4 are invisible to `C1_R46_PASS`. If calibration is claimed on the strength of this counter alone, the row prose can drift (and, for v3, already names a stale pin value) while `total=0` still prints.

**F6 — INFO — difference from wave 1, as the item asks.**
Wave 1 (`w1/ExecStmt06.md`, at freeze `745a5831…`) observed all three as **UNPARSED** with `claim_of = None`, because the last rows were the prose-evidence rows at 1657/1698/1809. At CONTENT they are **MATCH**. The observed tuples are unchanged between the two seats: v2 `('TALLY_AUDIT_V2_SELFTEST: 22/22 pass','0','7b11ba25aead')`, v3 and code_view `('TALLY_AUDIT_V3_SELFTEST: 35/35 pass','0','da8c1ef4b30c')`. So the difference is entirely the round-46 restatement (lines 2189-2191), which quotes the same values I independently observed — no drift, and no wave-1 observation is contradicted. Note for the L1: the restated rows were emitted from the same counter's observation, so these three MATCHes confirm row/observation agreement, not two independent derivations; my run is the independent side and it agrees.

No BLOCKING or HIGH finding on this slice: at CONTENT, all three standing rows state exactly what their frozen commands print, with the stated exit code and tool digest, and the base `SCORECARD.md` remains a byte prefix (`append_only=1`).

## Not run (deliberately)

- The deciding run of the C1 counter (`measure.py --lane … --rev … --base … --work …`) and its `--selftest`/`--emit`: the L1's, per the measurement bounds. I also did not run the counter at all, so I did not observe the other 19 statements or the axis rows.
- C2/C3 counters, the no-harm script, builds, linters, formatters: out of this seat's item; the parent owns post-integration gates.
- No git or jj mutation in the lane or the fleet repo; only `git clone`/`checkout` inside `/tmp/tameshi-r46-T46ReobsF/` and read-only `git show`/`rev-parse`/`grep` against the lane and its clone.

## Tooling

None installed or upgraded; no pacman transaction attempted.
