# T55W1ExecReKeyDryBind — re-key dry bind (round 55, w1)

Axis: calibration. Base `631cd6455e58dce969310b4c0466c3383d9f5108`. Everything below ran in a
scratch clone at that rev (`/fast/scratch/hyaku/tameshi-r55/T55W1ExecReKeyDryBind/clone`); the
lane itself was never written, and the frozen counters, contract, freeze manifest, `binder.py`,
`ledger.json` and the round-18/21/48 instruments were read only.

**Verdict.** The re-key route works end to end: a reader report for `## Standing rules`, a bound
ledger entry, the round-18/21 credit algorithm crediting the section, and the precheck printing
`lost=0`. The frozen round-54 binder cannot be used as-is — it hardcodes the round-54 heading
source, the round-54 wave dirs, the round-54 adjudication file and round-54 labels — and it needs
four flags, which are implemented in
`T55W1ExecReKeyDryBind-receipts/binder-r55.py` (diff: `binder-r55.patch`, 47 changed lines).

**Second, larger finding.** The round brief says "this edit DRIFTS that one cold-read section".
That is true of the SKILL.md edit *as such*, but **the round's other deliverables drift 17 more
sections**: landing the round's own content edits without re-keying them takes the cold-read page
from `64/64` (score 8) to `46/64` (score 6) and turns the precheck `RED lost=18`. Measured, see §5.

---

## 1. What was demonstrated, in order

1. Clone at base, detach at the frozen rev.
2. Apply the round-55 SKILL.md edit (the round-54 sentence "Measured on each tool's
   `--selftest`/`selftest` path … other modes are outside that measurement" replaced by the
   round-55 truth: every documented allocating mode — the seven self-tests plus
   `env-diff --contract` — as one stderr line with exit 2, and the five non-allocating modes lazy).
   Section grows from lines 17–40 to 17–43. Commit **C0**.
3. Write a reader report for `## Standing rules` at C0 with the frozen round-18 sectionizer, plus
   the round-55 heading set. Commit **PIN**.
4. Run the adapted binder: `rekeyed=1 skipped=0 headings=1`, exit 0. Commit the ledger entry and
   its trace — **CAND**.
5. Round-21 credit algorithm at CAND: the section is `credited` (start 17, end 43, `vetoed`
   false), `64/64` sections covered, `trace_gate: strict`, `overrides_used: false`,
   `calibration_restraint_score: 8`.
6. Precheck floor `631cd64` → CAND: `lost=0 ok`, exit 0.
7. Control (edited SKILL.md, floor ledger, no round-55 entry): the section is
   `no-ledger-entry`, `63/64`. The credit therefore comes from the bind, not from the edit.

Commits (scratch clone only, all with `git -C <clone>` and
`git -C <clone> rev-parse --show-toplevel == <clone>` asserted first):

| role | commit |
|---|---|
| base | `631cd6455e58dce969310b4c0466c3383d9f5108` |
| C0 (SKILL.md edit) | `314cfe29036a2347b138761b9eb7d6e06dad41f8` |
| PIN (reader + headings) | `03d434abe5c14358d5a75bff70397c7efe5697f4` |
| CAND (ledger + trace) | `adfd49dba48d29ec0e2f68a98776b24dbcbc8035` |

Section at C0: start 17, end 43, `section_sha256`
`4f959fd727cdb630d2507de403b2cb20ae5c14ccc170c527a0d708f997e08b9b`, SKILL.md blob
`a157f37d8915d460c0694b5eb660db48f37d9c3ce99e9d13917e74f01ec55545`.

## 2. Reader report (the artifact the item asks for)

`.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind.reader.json` (published beside this report), with
`T55W1ExecReKeyDryBind.reader.md` beside it because the binder requires the pair:

```json
{"heading": "## Standing rules",
 "cand": "314cfe29036a2347b138761b9eb7d6e06dad41f8",
 "section_sha256": "4f959fd727cdb630d2507de403b2cb20ae5c14ccc170c527a0d708f997e08b9b",
 "findings": []}
```

`cand` is a **scratch** commit: the L1 cannot reuse this report for the lane's own C0 and needs a
fresh reader there (the shape and the checks are the reusable part; the sha changes with the
bytes). A reader whose `findings` list is non-empty is *not* bound — the binder SKIPs it — and round
55 has no `resolutions.json`, so every re-keyed reader must be clean.

## 3. The exact command sequence the L1 must run

Precondition, and this is the part that decides the outcome: **bind last.** `PIN` must be a commit
that already carries every content edit to any path in the ledger's input graph —
`tools/repeat-control.py`, `tools/context-capture.py`, `tools/registry.json`,
`corpus/SOURCES.md`, `corpus/QUALITY.md`, `PROVINCE.md`, `tools/*.py` read by those sections. Only
`LOG.md`, `SCORECARD.md` and `SKILL.md` are dropped by the binder and safe to edit after the bind;
new files are inert. `C0` stays the commit whose SKILL.md carries the final `## Standing rules`
bytes (it may precede PIN).

```bash
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=631cd6455e58dce969310b4c0466c3383d9f5108
C0=<commit carrying the final SKILL.md ## Standing rules bytes>
PIN=<content-final commit, >= C0>
: "${HYAKU_SCRATCH:=/fast/scratch/hyaku}"; W="$HYAKU_SCRATCH/tameshi-r55/L1-rekey"; mkdir -p "$W"

# 1. the drift set at PIN (floor-credited minus PIN-credited) -> headings.json
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$BASE" > "$W/floor.json"
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$PIN" --explain > "$W/pin.json"
python3 - "$W/floor.json" "$W/pin.json" "$W/headings.json" <<'PY'
import json, sys
floor = {s['heading'] for s in json.load(open(sys.argv[1]))['coldread']['sections'] if s['credited']}
pin = {s['heading']: s for s in json.load(open(sys.argv[2]))['coldread']['sections']}
lost = sorted(h for h in floor if not pin[h]['credited'])
json.dump(lost, open(sys.argv[3], 'w'), indent=1)
for h in lost: print('LOST %s | %s' % (h, pin[h]['reason']))
print('drift headings=%d' % len(lost))
PY

# 2. bind (a second pass over a later PIN replaces the entry, never grows the ledger)
OUT="$LANE/.ufo/evidence/round-21/coldread/rekey-r55-${C0:0:12}"
mkdir -p "$OUT"
python3 "$LANE/.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py" \
  "$LANE" "$C0" "$PIN" "$OUT" \
  --headings "$W/headings.json" \
  --waves .ufo/waves/round-55/w1 \
  --label 'L1 TameshiR55 re-key (round 55)'
#    expects: REKEY <heading> ... for each heading, then
#    REFRESH rekeyed=<n> skipped=0 headings=<n>   exit 0.
#    exit 1 == a SKIP: no-clean-reader | reader-has-findings:n>0 | no-stable-inputs |
#    no-section-at-c0 | reader-md-missing. Adjudicate it; do not freeze over it.

# 3. commit ledger + traces, then measure at the deciding revision
git -C "$LANE" add -A .ufo/evidence/round-21/coldread
DEC=$(git -C "$LANE" rev-parse HEAD)
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$DEC" --explain \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["coldread"]["sections_covered"], d["coldread"]["sections_total"], d["calibration_restraint_score"], d["trace_gate"], d["overrides_used"])'

# 4. precheck — must print lost=0 and exit 0
bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$LANE" "$BASE" "$DEC"
```

The runnable copy of this sequence, with the dry-run numbers in its header, is
`T55W1ExecReKeyDryBind-receipts/l1-rekey.commands.sh`.

Expected shapes observed in the dry run: binder `8 s`, one measure `45–50 s` (`--explain`), the
precheck `170–200 s` (it measures floor and cand).

## 4. Can the frozen binder be reused as-is? No — precisely these must change

The frozen file is `.ufo/evidence/round-54/integrate/binder.py`
(`9395bb7c…990bb5`) and stays untouched. The adapted copy is
`T55W1ExecReKeyDryBind-receipts/binder-r55.py` (`f57098ca…f25fc`); full diff in
`binder-r55.patch`. Five deltas, all additive:

1. **Heading source.** `HEADINGS` was `lost-headings-at-c0.json ∪ lost-headings-at-base.json`
   under `.ufo/evidence/round-54`. Round 55's drift set is neither; `--headings FILE` supplies it,
   with the round-54 union kept as the no-flag default.
2. **Wave dirs.** `WAVE_DIRS` was the literal `('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')`;
   round-55 readers live in `.ufo/waves/round-55/w1`. `--waves DIR` (single dir per flag).
3. **Adjudication file.** `RES_PATH` was the round-54 `integrate/resolutions.json`; round 55 has
   none. `--resolutions FILE`, and absent/inexistent means **zero** findings allowed per heading —
   which is the strict reading for this round.
4. **Labels.** `seats` and `rev_reason` were hardcoded `L1 TameshiR54a2 re-key (round 54)` /
   `round-54 re-key: …`; `--label TEXT` replaces both.
5. **Trace argv.** `argv` was a reconstructed round-54 literal (`__file__`, raw C0/PIN); it now
   records the argv actually used. For a no-flag replay with resolved hashes and an absolute
   script path the rendered argv is the same list; for anything else it is the truthful one.

Nothing else needed changing: the ledger path, the dropped inputs (`LOG.md`, `SCORECARD.md`,
`SKILL.md`, the ledger), the frozen round-18 sectionizer extraction at C0, the input union, the
`class`/`verdict` carry-over and the replace-on-second-pass rule are all correct for round 55 as
they stand.

## 5. Evidence

| command | output |
|---|---|
| `python3 binder-r55.py CLONE 314cfe29… 03d434ab… OUT --headings … --waves .ufo/waves/round-55/w1 --label …` | `REKEY ## Standing rules start=17 inputs=2497 dropped=0` · `REFRESH rekeyed=1 skipped=0 headings=1` · exit 0 |
| `python3 .ufo/evidence/round-21/coldread/measure.py --repo CLONE --rev adfd49db… --explain` | `covered 64/64`, score 8, `trace_gate strict`, `overrides_used false`; `## Standing rules` → `{"credited": true, "start": 17, "end": 43, "reason": "credited", "vetoed": false}` |
| `bash .ufo/evidence/round-48/quality/coldread-precheck.sh CLONE 631cd645… adfd49db…` | `COLDREAD_PRECHECK floor=631cd6455e58 floor_credited=64 cand=adfd49dba48d cand_credited=64 lost=0 ok` · exit 0 |
| control: floor ledger + edited SKILL.md, measured at its own rev | `covered 63`; `## Standing rules` → `{"credited": false, "reason": "no-ledger-entry"}` |
| ledger inspection at CAND | 592 entries (591 + 1); exactly **one** carries `4f959fd7…` — the new entry, `inputs=2497` |
| `--ledger-file` control attempt | refused, exit 64 `SELECTOR_OVERRIDE_FORBIDDEN` (the round-21 wrapper forbids the override) — hence the fixture-repo control above |

The bound entry: `class instruction`, `verdict gap-minor`, `minor_gaps 0`,
`blocking_gaps 0`, `wrong_expectations 0`, `commands_executed_count 2498`, `traces
[.ufo/evidence/round-21/coldread/rekey-r55-314cfe29036a/traces/section-01.json]`, `reports` = the
reader JSON + MD. It passes the strict input and trace gates, which is what `credited` means here.

## 6. Drift: the finding the L1 must act on

Every credited entry pins sha256 digests of its inputs at its read revision, and the credit
algorithm re-verifies them at the deciding revision. So **any byte change to an input path
uncredits the sections that entry covers**, until they are re-keyed at the content-final commit.
Measured in fixture clones of CAND:

| probe | covered | lost | note |
|---|---|---|---|
| CAND (standalone) | 64/64 | 0 | score 8, box3 full page |
| + reformat of `tools/registry.json` | 53/64 | 11 | `## Standing rules` → `input-drift:tools/registry.json` |
| …then re-bind at that content-final commit | 54/64 | 10 | the re-keyed section is restored; the other 10 need their own readers |
| + every round-55 content surface (`tools/repeat-control.py`, `tools/context-capture.py`, `tools/registry.json`, `corpus/SOURCES.md`, `corpus/QUALITY.md`), no re-key | 46/64 | **18** | precheck `lost=18 RED`, exit 1; score 6 |
| + `corpus/knowledge/scratch-root-contract.md` only | 64/64 | 0 | that path is in no input set |

Lost headings in the last probe (full list in
`T55W1ExecReKeyDryBind-receipts/round55-edits-lost-sections.txt`): `## Context gate classification
and explicit exit classes — round 15`, `## Effective expectation reconciliation — round 14`,
`## Live-tree re-pin and entry-command monitor — round 17`, `## Mutation-sweep recipe — numbered
steps; bounded cold-read evidence`, `## Pin disposition and provenance correction — round 13`,
`## Repeated controls and gate registry — round 12`, `## Standing rules`, `## The leg ledger —
replay, receipt, and how it is read (round 7, measured)`, `## The operator's runbook and the six-leg
regression (round 10, measured)`, `### Gate/probe registry`, `### Round-13 gate/probe registry`,
`### Round-15 gate/probe registry`, `### Round-17 gate/probe registry — re-pin and monitor`,
`### Round-18 gate/probe registry — routed-defect closure`, `### Round-21 gate/probe registry —
finite environment differential`, `### Round-26 gate/probe registry — report interop`,
`### The service's limits — what tameshi refuses to mutation-test`, `### Triggers T1–T3 and the
re-pin rule`.

Consequences for the round, stated without choosing for the L1: either the round produces readers
for the full drift set at the content commit and binds them in one pass (17 extra readers, exactly
the round-54 shape that produced `lost-headings-at-c0.json`), or it lands one re-key and records
that the cold-read page and `calibration_restraint_score` fall from `64/64`/8 to `46/64`/6. The
`--headings` flag exists precisely so the first option is one command.

Secondary risk, measured: the bound entry carries **2497 inputs** because the union compounds
across the round-53 and round-54 re-keys (3 → 2499 → 2500 → 2497 → 2497). Binding at the
content-final commit is what stops this from firing; a later edit to any of those files kills the
section again.

## 7. Blockers / not run

- No blockers. Nothing was executed against the lane: `SKILL.md`, `SCORECARD.md`, `LOG.md`,
  `corpus/**`, `tools/**` and the frozen evidence are untouched (verified by writing only under
  `.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind*`).
- Not run, because it is outside this seat: the census validation, the C1/C2 counters, and the
  round's production edits.
- The scratch tree was wiped by something outside this seat mid-run (all `tameshi-r55` seat dirs
  were recreated at one timestamp); the work was rebuilt from base and every artifact is now in the
  lane receipts dir. Nothing in this report depends on a deleted path.
- No tool was installed or upgraded (the `pacman` pause did not matter here).
- Fixture commits were made only in scratch clones under
  `/fast/scratch/hyaku/tameshi-r55/T55W1ExecReKeyDryBind/`, each after asserting
  `git -C <dir> rev-parse --show-toplevel == <dir>`; the control and probe commits live in
  `control/`, `drift/`, `order/`, `round55edits/` and are disposable.
