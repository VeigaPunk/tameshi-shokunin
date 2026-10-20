# ReviewMeasureV2Code — `.ufo/evidence/round-17/measure.py` at `eb7838b`

Scope: code review of `.ufo/evidence/round-17/measure.py` at
`eb7838b16490ca7ba17ea3242ade76a61f744af2` against SKILL.md's input-keyed
section (`SKILL.md:1855-1903`) and `corpus/QUALITY.md:127-133` (QUALITY 23),
plus byte-compatibility of sectionizer/SHONEN/depth/sources with round-16
`.ufo/evidence/round-16/measure.py` at `98bea7d`.

Workspace: fleet-mirror clone at
`/tmp/tameshi-r17w2-ReviewMeasureV2Code-Yb8EKB/fleet/tameshi-shokunin`
(checkout `eb7838b`, `rev-parse HEAD` confirmed), plus a private `/tmp`
scratch repo for producer-receipt experiments. No lane tool was run against
the live lane root. No installs (strace 7.2, Python 3.14.8, git 2.56.0 already
present).

## Findings

### 1. BLOCKING — `live-lane-read:` is blind to real `trace-inputs.py` receipts

SKILL.md's table row (`SKILL.md:1877`) promises: "A trace opened a file in the
live lane while the root was a clone | No credit (`live-lane-read:`) | The
read was not of the recorded revision".

The producer and the consumer disagree on the field:

- `trace-inputs.py:292-306` routes an open under the live lane (when
  `root != lane`) to `self.lane_reads` (line 302-303), *not* `self.external`
  (the `elif` chain checks the lane before the fleet); `trace-inputs.py:683-684`
  emits it as `"live_lane_reads"`. Its own selftest asserts the separation:
  `trace-inputs.py:827-829` — `live in d["live_lane_reads"] and live not in
  d["external"]`.
- `measure.py:404-408` only inspects `receipt.get('external')` and calls
  `under_live_lane(key)` on those keys. `measure.py` never reads
  `live_lane_reads`. `assemble.py` has zero `live_lane` references
  (`grep -c live_lane assemble.py` → `0`), so nothing else in the recipe
  catches it either.
- The selftest exercises an impossible receipt shape:
  `measure.py:875-878` builds `TRACE_LIVE_PATH` with the live-lane path inside
  `external` — precisely what `trace-inputs.py` guarantees never to emit.

End-to-end demonstration (both runs exit 0):

1. Real producer receipt: ran
   `trace-inputs.py --root $R --out $R/.ufo/evidence/round-17/coldread/traces/live.json --cwd $R -- cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md`
   on a scratch git repo. Receipt: `schema=tameshi-trace-inputs-v1`,
   `external={}`, `live_lane_reads={'/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md': 'b1bd20ae…'}`,
   `inputs={}`. Committed it with a v2-shaped ledger entry
   (`instruction/executed-ok`, `commands_executed_count=1`, input
   `corpus/input.txt` verified) pointing `traces` at that receipt, then
   `python3 .ufo/evidence/round-17/measure.py --rev <scratch HEAD> --repo $R`:
   `covered 1 / 1`, `reasons {'credited': 1}` — **credited**.
2. Control, same path moved into `external` (hand-edited, not producible):
   `covered 0 / 1`,
   `reasons {'live-lane-read:/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md': 1}`.

So the reason is reachable only with a receipt the documented producer cannot
emit; with real wave-2 receipts, a clone-rooted read that also opened a live
lane file earns credit and `live-lane-read:` never fires. That falsifies both
the row-5 decision and the "every stated reason reachable" acceptance for the
documented pipeline (trace-inputs.py → assemble.py → measure.py).

Fix: in `trace_reason` (`measure.py:361-410`) treat a non-empty
`live_lane_reads` map like the external case (return
`live-lane-read:<p>`) — or reject non-empty `live_lane_reads` outright — and
switch the selftest fixture at `measure.py:875-878` to the producer's real
shape. `assemble.py` should either merge/deny the field as well, or the ledger
entry must carry a marker measure verifies.

### 2. MINOR — sources docstring regex does not match the code

`measure.py:31` states the row pattern as `` `^\|\s*S[0-3]{3,}\s*\|`… ``
while `measure.py:114` compiles `r'^\|\s*S[0-9]{3,}\s*\|'` (the round-16
pattern). On `corpus/SOURCES.md` at `eb7838b`: the stated regex matches 15
rows, the code matches 62 (the census output is the code's 62 rows; at
`98bea7d`: 55). Doc-only; code is v1-identical. Fix the `[0-3]` typo or drop
the inline regex in favor of "see sources_census".

### 3. MINOR — trace-gate docstring overstates the `commands_executed_count<=0` case

`measure.py:51-53`: "when `traces` is non-empty (or always for an entry with
`commands_executed_count>0` in strict mode) each trace path must resolve…".
`measure.py:376` returns `None` (credit) for `cmd <= 0` before validating a
declared `traces` list. Demonstrated: `class=record`, `verdict=verified-record`,
`commands_executed_count=0`, valid input, `traces=['no/such/trace.json']` →
`entry_reason` returns `None` (credited). QUALITY 23 only requires receipts for
entries that executed commands, so the behavior is defensible; the sentence at
`measure.py:51-53` should say "when commands>0 and traces is non-empty", or the
code should validate declared traces unconditionally (fail-closed).

### 4. INFORMATIONAL — the "byte-compatible" claim holds for depth/sources/sectionizer, not whole-`shonen`, at `98bea7d`

Command pair, both exit 0:

- `python3 /tmp/r16-measure-98bea7d.py --rev 98bea7d… --repo $C`
- `python3 .ufo/evidence/round-17/measure.py --rev 98bea7d… --repo $C --ledger-rev 98bea7d…:.ufo/evidence/round-16/coldread/ledger.json`

Identical: `recorded_cases=7`, `depth_score=7`, `ledger_legs` (7 names),
`ledger_guardrail` (header_legs/regression_calls/selftest_tuples=7,
`lists_agree=true`, `unique_recorded_gates=7`), and `sources`
(`rows=55, malformed=0, tiers={A:47,B:6,C:2}, status={mined:28,queued:24,rejected:3}`).
`sectionize()` is byte-identical on both real SKILL pages (54 and 58 sections)
and on 11 edge cases (empty, no-heading, headings-only, `####`, `#tag`,
unclosed fence, trailing whitespace, CRLF, non-UTF-8, preamble-only, `~~~`
fence); `shonen_boxes()` and `sources_census()` are identical on both revs.

Not identical: `shonen.box3_ledger_link` and `shonen.box3_points`.
r16 = `true/true`, r17 = `false/false`; the other seven SHONEN fields match.
Causes: `BOX3_LINK` is hardcoded to the round-17 ledger path
(`measure.py:122,623`) and the `98bea7d` SHONEN box 3 names only the round-16
path; `box3_points` additionally needs `coldread.box3_full_page`, and the v1
ledger has no `inputs`, so v2 credits 0/54 (`{'inputs-unrecorded': 54}`) even
though r16 credited 54/54. This is intended v2 hardening, but if the wave's
acceptance means whole-object `shonen` equality at `98bea7d`, it is
unsatisfiable without parameterizing `BOX3_LINK`/relaxing the input gate; the
SHONEN *census* is identical. Precision note for the docstring's
"SHONEN census … byte-compatible" claim, not a defect for C1 (the round-17
page names the round-17 ledger in box 3's continuation, and a v2 ledger does
carry inputs).

### 5. INFORMATIONAL — exit summary conflates default-ledger absence with exit 2

`measure.py:87` says "2 rev/blob/ledger/overlay missing". A missing *default*
ledger is a measured state, not an error: `--rev 98bea7d…` and
`--rev eb7838b…` with no ledger both exit 0 with
`reasons={"no-ledger": 54|58}`. Exit 2 applies to an explicit
`--ledger-file`/`--ledger-rev` target being unreadable/missing (selftest
`exit2-ledger-file-missing`, `exit2-ledger-rev-blob-missing`). The SKILL.md
registry row has the same wording. Fix the wording; behavior matches the
selftest and v1.

### 6. INFORMATIONAL — `ledger_committed` means "equals the default blob at the measured rev"

`measure.py:1445-1448` compares the used ledger bytes to
`REV:.ufo/evidence/round-17/coldread/ledger.json`. A ledger pinned with
`--ledger-rev <other-rev>:<round-16 path>` is `ledger_committed=false` even
though it is a committed blob at its own rev (observed on all three red-before
runs). Not defined anywhere in the docstring; name is easy to misread. No
effect on credit.

## QUALITY 23 (input-keyed credit) — direct checks

Reproduced byte-for-byte the claim in `corpus/QUALITY.md:127-133`
("credited at `e69b488`, uncredited (`input-drift:tools/mutate-and-run.sh`) at
`09ee1d0`"): the exact command

```
python3 .ufo/evidence/round-17/measure.py --rev <R> \
  --ledger-rev 98bea7d…:.ufo/evidence/round-16/coldread/ledger.json \
  --inputs-overlay .ufo/evidence/round-17/redbefore/legacy-r14-inputs.json
```

run for `R ∈ {98bea7d, e69b488, 09ee1d0}` (all exit 0) reproduced
`.ufo/evidence/round-17/redbefore/measure-{98bea7d,e69b488,09ee1d0}.json` with
JSON equality (not just key fields). Strict no-override run at `98bea7d`
reproduced `measure-98bea7d-strict.json` exactly (`{'no-ledger': 54}`,
`trace_gate=strict`). Cross-check of the input map: all files the overlay
pins still verify at `e69b488` → `credited`; at `98bea7d`/`09ee1d0`
`tools/mutate-and-run.sh` has the drifted sha (`75ed934d…` → `0673d2e5…`) →
`input-drift`; the other 53 v1 entries have no `inputs` → `inputs-unrecorded`.
Veto logic verified by the selftest's dupe cases and by the e69b488 page's
`verdict:gap-blocking`/`wrong-expectations:1` reasons (a clean credit cannot
launder them).

Every reason string is dynamically reachable (scratch repo, `entry_reason` /
`coldread` calls): `credited` → None; `verdict:not-executed`;
`verdict:maybe`; `malformed-entry` (boolean count); `wrong-expectations:1`;
`blocking-gaps:2`; `verdict-class:verified-record/instruction`;
`verdict-class:executed-ok/record`; `class:frobnicate`;
`commands-executed-count:0`; `inputs-unrecorded`; `input-missing:<p>`;
`input-not-blob:tools`; `input-drift:<p>`; `traces-unrecorded`;
`trace-missing:<p>`; `trace-invalid:<p>`; `trace-input-unrecorded:<p>`;
`live-lane-read:<p>` (external shape only — see finding 1); `no-ledger`;
`invalid-ledger`; `no-ledger-entry`. The `--inputs-overlay` whitelist
(`measure.py:127-128`, `OVERLAY_FIELDS`) rejects verdict/class injection with
exit 2 (`overlay-field-forbidden`). `IGNORED_INPUTS` (`measure.py:125`)
equals assemble's `DROPPED_INPUT_KEYS` (`assemble.py:125-128`), and assemble
emits the fields measure consumes (`commands_executed_count`, `inputs`,
`traces`; `assemble.py:776-800`), so the integration is coherent.

## Verification executed (commands, exits, key lines)

| # | Command | Exit | Key output |
|---|---|---|---|
| 1 | `python3 .ufo/evidence/round-17/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 89/89 pass (scratch /tmp/tameshi-r17-MeasureV2-ec4msb7l)` |
| 2 | r16 measure at `98bea7d` + r17 measure at `98bea7d --ledger-rev 98bea7d:.ufo/evidence/round-16/coldread/ledger.json` | 0/0 | depth 7=7, legs/guardrail/sources identical; shonen `true/true` vs `false/false`; r17 `{'inputs-unrecorded': 54}` |
| 3 | Function-level parity harness (imported both modules) | 0 | `sectionize` identical on 13/13 cases incl. both SKILL pages (54/58 sections) and non-UTF-8/CRLF/unclosed fence; `shonen_boxes`/`sources_census` identical |
| 4 | Red-before trio + strict run (see command above) | 0 each | 4/4 reproduction JSON equal to the committed `redbefore/measure-*.json`; e69b488 `{'credited':1,…}`, 98bea7d/09ee1d0 `{'input-drift:tools/mutate-and-run.sh':1,'inputs-unrecorded':53}` |
| 5 | Reason reachability harness on a scratch git repo | 0 | all 21 reason strings produced (list above); `cmd0 + declared missing trace` → `None` |
| 6 | Real `trace-inputs.py` receipt with live-lane read → committed → `measure.py --rev HEAD` | 0 | `covered 1/1`, `{'credited': 1}` (finding 1) |
| 7 | Same receipt with live-lane path hand-moved into `external` → measure | 0 | `covered 0/1`, `{'live-lane-read:/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md': 1}` |
| 8 | Normal producer receipt (`cat corpus/input.txt`) + ledger → measure, no overrides | 0 | `covered 1/1`, `trace_gate=strict`, `overrides_used=false`, `box3_full_page=true`, `score=8` |
| 9 | `measure.py --rev eb7838b` with a v2-shaped full ledger at the landing page | 0 | `58/58 credited`, `box3_link=true`, `box3_points=true`, `score=8` (mechanism for C1); default run with no ledger is 6 / `{'no-ledger': 58}` |

C1 note: as cloned, `eb7838b` has no
`.ufo/evidence/round-17/coldread/ledger.json` (live dir has `assemble.py`,
`trace-inputs.py`, `bucket-commands.json`, `traces/` only), so the literal
`--rev eb7838b` run is `score 6`, `no-ledger`; `box3_full_page=true`/score 8
requires the landing commit that contains the assembled ledger. The tool's
mechanism for that is proven (row 9), but C1 must be cited at that later
commit.

Residual risks: `measure.py` does not bind `receipt['rev']`/`root`/`cwd` to
the entry (assemble enforces `receipt.rev == read_rev` at
`assemble.py:439-442`); a hand-committed ledger + receipt with a mismatched
rev would still credit. `under_live_lane` resolves relative external keys
against the caller's CWD (producer emits absolute paths, so not hit here).
Neither is required by QUALITY 23's text; both are defense-in-depth.

## Verdict

Holds for QUALITY 23's input-keyed rule, the strict trace gate on real
producer receipts, red-before reproducibility, exit codes, and v1
sectionizer/depth/sources parity; **falls** on the live-lane row —
`measure.py` reads `external` while `trace-inputs.py` records clone-vs-live
reads in `live_lane_reads`, so a real offending trace is credited and
`live-lane-read:` is unreachable through the documented pipeline. Fix that
(and the selftest fixture) before C1 is cited; the docstring regex/trace-gate
and whole-`shonen`-parity notes are minor.
