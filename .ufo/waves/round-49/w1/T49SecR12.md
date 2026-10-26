# T49SecR12 — C1 section critic: `## Repeated controls and gate registry — round 12`

Seat: T49SecR12 (leaf, calibration). Base `8ca67421111fa354b47b803358391d0b07fc6db9`.
Section audited: `SKILL.md:1479-1498` (sectionized section; the page's `### Gate/probe registry`
starts at 1499 and is a separate section, so it is out of range and only one adjacent statement is
reported, marked OUT OF RANGE). Heading text unchanged throughout. Deliverable:
`.ufo/waves/round-49/w1/T49SecR12.findings.json`. Receipts: `.ufo/waves/round-49/w1/T49SecR12.receipts/`.

Method: base blobs only (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421…:<path>`);
the gate was executed as a byte-identical copy of `tools/repeat-control.py` (sha256
`296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`, 35454 B — the same sha as
`HEAD:tools/repeat-control.py`) in a single scratch clone, with the seat scratch root as `TMPDIR`/
`--out`. The lane was not written; the lane's jj/Git state was not touched; no fixture repository was
needed; no tool was installed or upgraded. The frozen extractor was re-run on the section text (via
`.ufo/evidence/round-49/c1/measure.py`'s `extract`) to confirm the two in-range fixes keep the base
pointer set at 5 and introduce no new pointer beyond the intended `S026 → S265` substitution.

## Verdicts (false first, then page order)

| SKILL.md | Statement (abridged) | Verdict |
|---|---|---|
| 1483 | "not a change to the six-leg runner." | **false** (stale count; nine legs at base) |
| 1488 | "Any available controls differ … → `controls_mismatch`" | **false** on mixed availability (availability-first precedence) |
| 1508-1509 | "never a seventh independently measured gate" | **false** (OUT OF RANGE: stale ordinal; nine legs at base) |
| 1481 | "Source: S004/S026" | true (row live; anchor superseded → fix proposed) |
| 1479 | heading "— round 12" | true |
| 1481 | `corpus/knowledge/repeated-control-precondition.md` | true |
| 1482 | `runtime evidence: .ufo/evidence/round-12/verification-final.json` | true |
| 1483 | "This is a standalone precondition check" | true |
| 1487 | row 1 (three zero-exit controls → `controls_match`) | true |
| 1489 | row 3 (equal nonzero / unavailable → could-not-evaluate) | true |
| 1491 | "choose a pristine command" | true |
| 1491 | "put evidence outside any tree it inspects" | true |
| 1492 | the `repeat-control.py --runs 3 --out … --` command line | true |
| 1493 | "retain raw observations before interpreting the finding." | true |
| 1493-1494 | "The output directory must not exist." | true |
| 1494 | "Caller owns timeout policy; hanging commands yield no verdict." | true |
| 1495-1496 | "Do not retry until green, normalize output, or interpret a finite match as proof…" | true |
| 1496-1497 | "Command stdout/stderr may contain sensitive data…" | true |

## False statements

### 1. `SKILL.md:1483` — "not a change to the six-leg runner."

At base the runner has nine legs, so the definite description is false.

```
$ git -C LANE show 8ca67421…:tools/mutate-and-run.sh | sed -n '83p'
# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine) — the fleet's
$ git -C LANE show 8ca67421…:tools/mutate-and-run.sh | grep -cE '^#   (js|bash)-'
9
```

Six was the round-12 count. The page already dates this number where it names it — `SKILL.md:1391`
("six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26") and
errata row `SKILL.md:1740` correct `:1391` only. `git -C LANE show 8ca67421…:SKILL.md | grep -n
'1483'` returns `1483` alone: this line carries no dated correction, so a cold reader is told the
runner is six-leg today.

Fix (in the report's JSON): date-qualify — "not a change to the six-leg runner of round 12." Same
idiom as errata row 1740; no pointer, no heading. Receipts: `base-runner-legs.txt`, `base-section.txt`.

### 2. `SKILL.md:1488` — row 2, "Any available controls differ in exit or either stream → `controls_mismatch`"

The row is right whenever every run executed, and wrong when they did not. Reproduced at N = 3
(the section's own run count) with a script that prints `run1`, `run2` and then makes itself
non-executable:

```
$ python3 tools/repeat-control.py --runs 3 --out DIR -- DIR/probe/vanish3.sh
REPEAT_RUN 1 exit=0 stdout-bytes=5 stderr-bytes=0
REPEAT_RUN 2 exit=0 stdout-bytes=5 stderr-bytes=0
REPEAT_RUN 3 exit=unavailable stdout-bytes=0 stderr-bytes=98
REPEAT_COMPARE identical=no runs=3
REPEAT_CONTROL: command_unavailable
exit=2
```

Runs 1 and 2 are available and differ, so row 2's antecedent holds and its decision cell predicts
`controls_mismatch`/exit 1; the tool prints `command_unavailable`/exit 2. The tool decides
availability first: `tools/repeat-control.py:206-209` returns `command_unavailable` when any run is
unavailable, before the `(exit, stdout, stderr)` disagreement test at `:210-218`; the docstring states
the precedence at `:30-36`. Row 3's "or command unavailable" also matches the overlap, so as written
the table has no precedence and row 2 mispredicts. (T49ExecR12Cmd reached the same conclusion with an
N = 4 self-deleting probe, their `I.txt`; this seat's N = 3 receipt is
`T49SecR12.receipts/mixed-availability.txt` with the driver `mixed-vanish3.sh`.)

Fix: make the antecedent exclude the mixed case — "All runs executed and any differ in exit or
either stream". No pointer or heading changes. The all-executed case still reproduces:
`probes.txt` (`REPEAT_CONTROL: controls_mismatch`, exit 1).

### 3. OUT OF RANGE — `SKILL.md:1508-1509`, `### Gate/probe registry`: "never a seventh independently measured gate"

This sentence sits in `### Gate/probe registry` (sectionized 1499-1516), not in this seat's
1479-1498; it is reported because it is the stale lane count adjacent to the audited block. The
clause that the bash study is itself not a gate still holds; the ordinal presupposes six measured
gates, and at base a seventh exists (js-round-gate, `tools/mutate-and-run.sh:93`) out of nine legs
(`:83`, nine `#   js-|bash-` rows at `:87-95`). The note it rests on repeats the stale six at
`corpus/knowledge/repeated-control-precondition.md:70` ("…stay the six at
`tools/mutate-and-run.sh:84-89`"). Fix offered: "never a further independently measured gate".
**Caveat:** the round-21 monitor matches sections to ledger entries by sha256, and this section is
not one of the seven C1 targets, so applying that edit requires re-keying `### Gate/probe registry`
or deferring it to a round that will.

## Provenance refresh (statement true, fix proposed)

`SKILL.md:1481` "Source: S004/S026": S026 is a live row (`corpus/SOURCES.md:37`, mined, used-by
includes the cited note), so the statement is true — but the anchor is superseded at base. The cited
note's own header re-anchors it (`corpus/knowledge/repeated-control-precondition.md:1`, "S265
(supersedes S026) … re-fetched 2026-10-26T08:40:51Z"), and `corpus/SOURCES.md:140` defines S265 as
"supersedes S026's anchor and quote only". Proposed `S026 → S265`; re-running the frozen extractor on
the corrected section text yields exactly 5 pointers (`corpus/knowledge/repeated-control-precondition.md`,
`.ufo/evidence/round-12/verification-final.json`, `tools/repeat-control.py`, `S004`, `S265`), the base
floor, and `S265` resolves to `SOURCES.md:140`. The retained-history variant ("S004/S265 (historical
S026 retained)", the `SKILL.md:1519` idiom) would add a sixth S-id pointer that needs its own read
row. T49Read14 recorded the same supersession and the same replacement.

## Notes for the integrator (not verdicts)

- `SKILL.md:1489` row 3's decision cell, "Could not evaluate baseline", is prose the tool never
  prints — the printed ids are `baseline_nonzero` and `command_unavailable`, both exit 2
  (`tools/repeat-control.py:122-130`; probes `nonzero`/`unavail`). The semantics are right, so the
  verdict is true; T49ExecR12Cmd M2 flags the cold-reader mapping gap.
- `SKILL.md:1487` row 1's bound is a weaker paraphrase of `tools/repeat-control.py:92-94`, which adds
  "on this host in this environment"; no false claim, so no fix proposed.
- The section's cited note is itself stale at base: `corpus/knowledge/repeated-control-precondition.md:58`
  pins the tool at 30,557 B / sha `29d80254…` while the base blob is 35,454 B / sha `296fe566…`, and
  its line cites are shifted (`:58`, `:35`). That is the note's defect, not a false statement in the
  section; handed to the note's owner/T49ExecR12Cmd's cross-reference.
- `tools/registry.json` at base registers three `repeat-control.py` rows (snapshot clean/mismatch,
  selftest) sourced to `SKILL.md@98bea7d:1503` — no claim in this section contradicts them.
- The section's pointer set is untouched by the two in-range fixes: base 5 → 5, and every proposed
  `skill_old` is unique in the section (`not a change to the six-leg runner.` ×1, `Source: S004/S026
  and` ×1, the row-2 cell ×1).

## Receipts

`.ufo/waves/round-49/w1/T49SecR12.receipts/` — `base-section.txt` (1479-1498 numbered),
`base-runner-legs.txt` (runner :80-96 + leg count), `base-sources.txt` (SOURCES :15,:37,:140),
`base-note.txt` (note :1-3,:58,:70), `tool-identity.txt` (base/HEAD tool sha + bytes), `probes.txt`
(seven probe runs with exact argv, stdout/stderr/exit), `mixed-availability.txt` (the N=3
counterexample), `mixed-vanish3.sh` (driver, run once), `selftest.txt` (29 cases, exit 0),
`probe-findings/` (five `finding.txt` copies), `verification-final-receipt.txt` (the
`real-pristine-three-controls` check). Scratch `/fast/scratch/hyaku/tameshi-r49/T49SecR12` deleted
before yield; no `/tmp` or scratch path is cited as evidence.

## Summary
- 1483 "the six-leg runner" is false at base: nine legs (`tools/mutate-and-run.sh:83`, rows :87-95); the fix dates it ("…of round 12").
- 1488 row 2 mispredicts mixed availability (runs 1-2 differ, run 3 unavailable -> `command_unavailable`/2; precedence `tools/repeat-control.py:206-218`); fix requires all runs executed.
- OUT OF RANGE 1509 "never a seventh…" carries the same stale six-gate count (nine legs at base); fixing it needs re-keying `### Gate/probe registry`.
- 15 other statements are true: both paths and the runtime receipt, the three table mappings, the command line, the existing-`--out` 64, no timeout, byte-exact/no-retry, the sensitive-output warning.
- S004/S026 is true (row live) but anchored to a superseded pointer: S265 (`SOURCES.md:140`) is current and replacing it keeps the 5-pointer floor.
