# T52W1Corr02 — correction record for round-51 cold-read re-key entry `## Restore discipline — before/after identity, not continuous non-write proof`

Seat T52W1Corr02, round 52 wave 1, C2 item m4 (one correction record per round-51 cold-read re-key entry).
Read-only on the lane except this report and `T52W1Corr02.json`; the contract and
`.ufo/evidence/round-52/c2/measure.py` (frozen counter, docstring m4 + `check_findings`) were read first and
not edited. No claim is decided here: this is the record the L1's m4 consumes, nothing more.

## 1. What the entry is

- Ledger entry: `.ufo/evidence/round-21/coldread/ledger.json:40841` (heading), `:40846`
  `"wrong_expectations": 0`, `:40849` `"read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9"`,
  `:40857-40858` seats `["T51W2Read02", "L1 TameshiR51a3 integration (attempt 3)"]`; `verdict`
  `verified-record`, `skill_sha256` `83c2cedd…` — the same section sha the reader records.
  Command: `python3 -c` load + filter (see §5).
- The zero is written from code, not derived from any reader finding: `.ufo/evidence/round-51/coldread/refresh.py:227`
  hardcodes `'wrong_expectations': 0` (with `'blocking_gaps': 0, 'minor_gaps': 0`) into every refreshed entry;
  the append at `refresh.py:221-231` carries no findings field at all. That is routed defect 3 of
  `corpus/lessons/round-51-verifier-spotcheck.md` ("Routed defects").
- Reader read in full: `.ufo/evidence/round-51/coldread/reads/T51W2Read02.md` (281 lines). Section under test
  at the entry's read_rev: `SKILL.md:375-404` at `02ec217c4d0afabe727fde2e261b7951d28fb4e9`
  (`git -C <lane> show 02ec217c…:SKILL.md`), heading at :375, next heading at :405. Section sha
  `83c2cedd…` (ledger `skill_sha256`), byte-identical to the reader's candidate reading.

## 2. Findings the reader recorded as not holding

One. The reader verdicts every pointer `holds` (P1-P11) and closes every statement-level falsifier in §4, with a
single exception it records against item 6's subject: the section speaks of **both** historical probes'
sensitivity re-runs reading the lane's retained scratch, but the reader found that the Kagi probe's
re-verification was a full independent re-sweep, not a retained-scratch re-run, and no `r3-1-work` scratch
appears anywhere in SCORECARD.

| # | quote (byte-exact, one reader line) | reader line | class | skill_statement |
|---|---|---|---|---|
| 1 | `not a retained-scratch re-run, and no \`r3-1-work\` scratch appears anywhere in SCORECARD.` | `.ufo/evidence/round-51/coldread/reads/T51W2Read02.md:162` | `unsupported` | `The historical probes' sensitivity re-runs read the lane's retained scratch` |

Section text concerned: `SKILL.md:396-397` at read_rev — "6. **Retain durable evidence.** The historical
probes' sensitivity re-runs read the lane's retained scratch (`SCORECARD.md:13`), but the case-note
commands…". The pointer `SCORECARD.md:13` is exact only for the round-2 (Kimi) probe (reader :159 "The pointer
is exact for the round-2 (Kimi) probe"); the reader records `SCORECARD.md:15` as the round-3 row that
re-verifies the Kagi probe through the shipped tool from a spec cut from the pinned artifact, and records the
absence of any `r3-1-work` scratch in SCORECARD (reader :160-162). The premise is therefore broader than any
cited pointer — class `unsupported`, not a moved pointer (nothing at :13 or :15 moved; the reader's §2 records
"No pointer moved", :76).

Why it counts despite the reader's own label: the reader also writes "Recorded as a scope note, not a defect"
(:166), but the item's rule counts what the reader *recorded*, and what it recorded is the section's statement
failing at its candidate for one of its two subjects; it is neither a `holds` verdict nor a note marked
disclosed/historical and accurate. Its "still holds for both probes" clause (:163-164) concerns a different
proposition — that scratch loss makes the re-runs unrecoverable — and does not repair the plural in the
sentence that cites `SCORECARD.md:13`.

Not counted (reader recorded no failure): P1-P7, P9-P11 `holds`; P8's pointer exactness for the Kimi probe;
P10's live end-to-end `--regression` run (exit 0, `REGRESSION: PASS (cases=10 passed=10…)`, 242.2 s, :201);
§4's closed falsifiers, including the two negative claims about after-repo revisions and item 5's `(I)`
premise; the reader's own method slip at :119 ("my first sed-range read mis-numbered it") — that is the
reader's own mis-read, not a statement of the section.

## 3. Deliverable

`.ufo/waves/round-52/w1/T52W1Corr02.json` — exactly the six keys `heading`, `read_rev`, `reader`,
`reader_file`, `wrong_expectations`, `findings`; `findings` holds exactly `{quote, class, skill_statement}`.
`wrong_expectations` = 1 = `len(findings)`. `heading` is the exact ledger heading (em dash), `read_rev` the
full `02ec217c…` sha, `reader` `T51W2Read02`, `reader_file`
`.ufo/evidence/round-51/coldread/reads/T51W2Read02.md` — the exact `want` string m4 builds from the seat.

## 4. Self-check (frozen counter's own rule)

`check_findings` imported from the frozen counter (`.ufo/evidence/round-52/c2/measure.py`) and called on my
findings with the reader file read through the counter's own `show()` at `read_rev` and again from the working
tree; the rule is whitespace-collapsed substring containment, ≥20 characters. Output verbatim:

```
check_findings(reader@REV) = None
check_findings(working-tree reader) = None
squash(q) substring of squash(reader@REV) = True
quote_chars = 88 | on exactly one reader line = [162]
wrong_expectations == len(findings) = True
skill_statement verbatim in section@REV = True
```

`None` = pass (no bad finding, no floor uncovered; T51W2Read02 carries no frozen floor in `FLOORS`). The
counter's rule itself was exercised read-only via its selftest:

```
SELFTEST leg-count ok
SELFTEST section-stops ok
SELFTEST quote-verbatim ok
SELFTEST quote-forged ok
SELFTEST quote-short ok
SELFTEST floor ok
SELFTEST range ok
SELFTEST range-miss ok
C2_SELFTEST: cases=8 failed=0
```

Command: `python3 .ufo/evidence/round-52/c2/measure.py --selftest`.

## 5. Commands used (all read-only)

- `cat .ufo/evidence/round-52/c2/measure.py`; `cat .ufo/evidence/round-51/coldread/reads/T51W2Read02.md`.
- `git -C <lane> show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` (section located by `startswith('## Restore discipline')`; lines 375-404 printed with `repr` to pin em dash and apostrophes).
- `python3` ledger filter: entries with `read_rev` starting `02ec217c` → 20; those with seat `T51W2Read02` → 1
  (heading, start 375, end 404, `skill_sha256` `83c2cedd…`, `wrong_expectations` 0).
- `grep -n 'wrong_expectations' .ufo/evidence/round-51/coldread/refresh.py` → `227:` (the hardcoded 0).
- `sed -n '205,240p' .ufo/evidence/round-51/coldread/refresh.py` (the append that omits findings).
- `grep -nE 'broader|exceeds|not a defect|scope note|mis-number|…' reads/T51W2Read02.md` → the only negative
  recording is the P8 scope note at :150, :159-162, :166, :235-236.
- `python3` importlib load of the frozen counter + `check_findings`/`show`/`squash`/`section` reads (§4); no
  counter was run against the lane.

## 6. Observed anomaly (reported, not adjudicated)

At the entry's own read_rev the ledger does not yet contain the round-51 re-key rows: `git show
02ec217c…:.ufo/evidence/round-21/coldread/ledger.json` parses to 511 entries, of which **0** carry
`read_rev` starting `02ec217c`, and the file has **no** top-level `corrections` key. In the working tree
today: 20 entries with `read_rev` `02ec217c…`, and `corrections` present but empty (0 records). Consequence for
whoever integrates: m4's 20-entry pairing and `corrections` list can only be satisfied at the round-52
measured REV, where wave 2's ledger write must add all 20 records (this file is 1 of 20) — no record exists at
`02ec217c`. This seat did not edit the ledger.

## 7. Bounds, cleanup, tooling

- Writes: only `.ufo/waves/round-52/w1/T52W1Corr02.json` and this report. Lane checkout otherwise untouched
  (no git/jj mutation, no index or `jj` state change); fleet repo, siblings, and `shokuknow` untouched.
- Scratch: `/fast/scratch/hyaku/tameshi-r52/T52W1Corr02/` was never needed (no clone, no fixture repo, no
  counter run requiring a work dir); confirmed absent after the work (`ls` → "No such file or directory").
  No files written under `/tmp`.
- Tools installed: none (so nothing to record under RULES.md); pacman untouched.
- Out of scope, deliberately: any judgment of C1/C2, any edit to `SKILL.md`, `tools/registry.json`,
  `tools/round21-measure.py`, the round-21 ledger, or the frozen counters; the other 19 correction records;
  the wave-2 re-key that restores the dropped cold-read sections.

## Summary

- Deliverable `.ufo/waves/round-52/w1/T52W1Corr02.json`: heading `## Restore discipline — before/after
  identity, not continuous non-write proof`, read_rev `02ec217c…`, reader `T51W2Read02`,
  `wrong_expectations` 1.
- One finding, class `unsupported`: the section's plural "The historical probes' sensitivity re-runs read the
  lane's retained scratch" (`SKILL.md:396`), recorded by the reader at reads/T51W2Read02.md:162 as "not a
  retained-scratch re-run, and no `r3-1-work` scratch appears anywhere in SCORECARD."
- Ledger entry (ledger.json:40841-40858) says `wrong_expectations: 0` because refresh.py:227 hardcodes 0 —
  routed defect 3.
- Frozen `check_findings` returns `None` for the record; quote is 88 chars on reader line 162; count equals
  len(findings); skill_statement is verbatim inside the section at read_rev.
- Counter selftest: `C2_SELFTEST: cases=8 failed=0`; no counter run against the lane.
- Anomaly for integration: at `02ec217c` the ledger has 0 rows with that read_rev and no `corrections` key;
  m4 can only pass at the round-52 measured REV after wave 2 writes all 20 records.
- No tools installed; no scratch left; lane/fleet/siblings read-only.
