# T54W1Read11 — cold read of `## Repeated controls and gate registry — round 12`

- Heading: `## Repeated controls and gate registry — round 12`
- Candidate revision (C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- Section span: SKILL.md lines 1504–1522 (canonical bytes: heading line through line 1522, no trailing newline; the following `### Gate/probe registry` at line 1524 is a different section)
- `section_sha256`: `2613c4fe5c89d2971d16622a0cf1888acc40b8c26a137b9c4bd120cc95053a96`
- Class: record (a source pointer, a 3-row decision table and a recipe — all stating facts with pointers). I nevertheless executed the tool the section names, inside an extracted tree at C0.
- Verdict: one finding. The section does not credit while that finding stands.

## Finding 1 — the `corpus/SOURCES.md:500` anchor no longer resolves at C0

Quote (byte-exact substring of the section, line 1506):

```
S026 superseded by S265, `corpus/SOURCES.md:500`
```

Why: at C0 line 500 of `corpus/SOURCES.md` is `- Next unused id: S265 (S261–S264 are map-only reserved; …)` and says nothing about supersession; the supersession sentence is line 503. C0's own edit to `corpus/SOURCES.md` (five insertions: the S277, S278 and S279 table rows above line 500, then a blank line and a Round 54 bullet below it) moved the sentence from line 500 to line 503, so the parenthetical's pointer is stale exactly at the revision it is read against. The cited line at C0 is itself one of the two "Next unused id: S265" bullets that line 503 declares were not updated in round 48.

Evidence (lane repo, read-only):

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show d33053f7552d:corpus/SOURCES.md | sed -n '500p'
- Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; snapshots and receipts under `.ufo/evidence/round-12/freshness/sources/`). The two "Next unused id: S265" lines above were not updated in round 48; this line corrects them without rewriting.
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:corpus/SOURCES.md | sed -n '500p'
- Next unused id: S265 (S261–S264 are map-only reserved; staged ids S161–S255 stay reserved by document for the package).
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:corpus/SOURCES.md | sed -n '503p'
- Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; snapshots and receipts under `.ufo/evidence/round-12/freshness/sources/`). The two "Next unused id: S265" lines above were not updated in round 48; this line corrects them without rewriting.
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat d33053f..59c3810 -- corpus/SOURCES.md
 corpus/SOURCES.md | 5 +++++
 1 file changed, 5 insertions(+)
```

## What I opened and what I checked (all at C0)

Section bytes were read from the commit only (`git show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md`, lines 1504–1522), never from the working tree. `section_sha256` was reproduced independently by hashing those canonical bytes (`sha256 = 2613c4fe…53a96`, 1436 bytes / 1434 chars).

Anchors that resolve at C0:

- `S004` — `corpus/SOURCES.md:15`; `S265` — `corpus/SOURCES.md:140` (row text: "supersedes S026's anchor and quote only"). Both rows are present at C0.
- `corpus/knowledge/repeated-control-precondition.md` — blob `0d45d1c991343a5458ff4ee59d3fa6e96719791c` at C0; it carries the same finding→exit→class table as the section's table.
- `.ufo/evidence/round-12/verification-final.json` — blob `861091916e2b91df3afa5f2acdbdf72f015e2a48`; `passed: true`, and its checks include `repeat-control-selftest` (0/0), `frozen-match` (0/0), `frozen-mismatch` (1/1), `real-pristine-three-controls` (0/0), `runner-six-leg-regression` (0/0) — which also supports "the six-leg runner of round 12".
- `tools/repeat-control.py` — blob `0d662e5d1abefb9398bed86007cad330a8c788eb`, mode 100755; `$HYAKU_SCRATCH` is defined for a cold reader at SKILL.md:28/147/169.

Table cells exercised against the tool at C0 (tree extracted with `git archive 59c3810 | tar -x` into scratch; `TMPDIR` inside the seat scratch):

| Section claim | Command | Observed | Verdict |
|---|---|---|---|
| "Three or more zero-exit controls match on raw stdout and stderr" → `controls_match` | `python3 tools/repeat-control.py --runs 3 --out "$S/out-match" -- bash -c 'echo hi'` | `REPEAT_COMPARE identical=yes runs=3` / `REPEAT_CONTROL: controls_match`, exit 0 | holds |
| "Equal nonzero controls" → `baseline_nonzero`, exit 2 | `--runs 3 --out "$S/out-nonzero" -- bash -c 'exit 7'` | `REPEAT_CONTROL: baseline_nonzero`, exit 2 | holds |
| "The output directory must not exist" | `--runs 3 --out "$S/out-match" -- …` (re-using the dir) | `REPEAT_CONTROL: invalid_usage`, exit 64, "an existing DIR is refused with exit 64" (`tools/repeat-control.py:25`) | holds |
| `--runs` floor of 3 backs "three or more" | `--runs 1 …` | `REPEAT_CONTROL: invalid_usage`, exit 64; code rejects `runs < 3` (`tools/repeat-control.py:275`, `:394`) | holds |
| `--snapshot` is read-only validation (registry section, same tool) | `--snapshot .ufo/evidence/round-12/ControlGate` | `SNAPSHOT_EXPECTED id=controls_match exit=0` / `SNAPSHOT_OBSERVED id=controls_match exit=0`, exit 0 | holds |
| mismatch snapshot | `--snapshot .ufo/evidence/round-12/ControlGate/mismatch` | `SNAPSHOT_OBSERVED id=controls_mismatch exit=1`, exit 1 | holds |
| selftest | `--selftest` | `SELFTEST: PASS (29 cases)`, exit 0 | holds |
| exit map "2 and 64 could-not-evaluate" (registry section) | `EXIT_BY_ID` at `tools/repeat-control.py:122-130` and the docstring at `:43` ("`invalid_usage` … could-not-evaluate") | consistent | holds |
| "Caller owns timeout policy; hanging commands yield no verdict" | `tools/repeat-control.py:79-87` (no timeout, no supervisor) and the knowledge note §2/§3.1 | consistent | holds |
| "not a determinism proof" bound | knowledge note §2 ("Determinism is a property of the program across runs, including runs not taken") | consistent | holds |

Receipts (durable copies): `T54W1Read11-receipts/{selftest,snap-match,snap-mismatch,run-match,run-nonzero,usage}.out`.

## Not defects (checked, then dismissed)

- "the six-leg runner of round 12": `.ufo/evidence/round-12/verification-final.json` has a `runner-six-leg-regression` check (exit 0), and `.ufo/evidence/round-12/EvidenceScribe/inventory.md:97` speaks of "the existing six legs". The current runner carries ten ledger rows, but the sentence is dated to round 12, not to C0.
- Row 2 ("All runs executed and any differ …") and row 3 ordering match the tool's fixed precedence (`command_unavailable` before `controls_mismatch` before `baseline_nonzero`).
- The registry table and the witness-declaration paragraph sit in the next section (`### Gate/probe registry`, line 1524 onward), so no cell or sentence there is in this section's byte span.
- `seat ReRead08` is not in this section's span.

## Scratch

Seat tree `/fast/scratch/hyaku/tameshi-r54/T54W1Read11/` (C0 extract, TMPDIR, fixture outputs) was deleted after the receipts were copied into the wave directory; nothing was left behind.
