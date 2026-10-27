# T52W1ExecColdreadProbe — predicted cold-read sections this round must re-key

Seat: executor leaf (wave 1). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
(READ-ONLY; every git mutation below happened in the scratch clone).
Base: `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`. No claim is judged here; the numbers are
observed probe output, not a verdict.

Receipts: `.ufo/waves/round-52/w1/T52W1ExecColdreadProbe.receipts/` (precheck stdout per
variant, `measure-*.json`, `measure-summary.json`, `base-lane.json`, `tolerance.log`,
`shAs*.txt`, edit logs, and the three driver scripts `apply_edits.py`, `bisect.sh`, `bisect2.sh`).

## 1. Method (exact commands)

    S=/fast/scratch/hyaku/tameshi-r52/T52W1ExecColdreadProbe; mkdir -p "$S"
    git clone --shared -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
    git -C "$S/clone" rev-parse --show-toplevel        # -> $S/clone (asserted before any commit)

Per variant: `git -C "$S/clone" checkout -q -B <v> ef19d8e1e7ba…` + `reset --hard`, apply edits
(`T52W1ExecColdreadProbe.receipts/apply_edits.py`, exact-string replacements with occurrence assertions), commit with fixture
identity (`-c user.name=hyaku-fixture -c user.email=fixture@tameshi.invalid`), then

    HYAKU_SCRATCH="$S" bash .ufo/evidence/round-48/quality/coldread-precheck.sh \
        "$S/clone" ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 "$CAND"
    python3 "$S/clone/.ufo/evidence/round-21/coldread/measure.py" \
        --repo "$S/clone" --rev "$CAND" --explain

Both revisions are passed explicitly (never `master`; the clone's `master` was left at the lane
tip and no run read it). Floor measured read-only against the lane at base as well:
`python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev ef19d8e1e7ba… --explain`.

Floor receipt (`precheck-vbase.txt`, `measure-vbase.json`): **64/64 credited, score 8,
box3_full_page true, vetoed 0, lost=0 ok** at an empty commit on base
(`144d1a2d3203358172d3238bd2be7760528cd5bc`). The same 64/64/8 is printed for the lane at base
(`T52W1ExecColdreadProbe.receipts/base-lane.json`).

Edits applied, with the base line each one touches (all line numbers are base bytes,
`git show ef19d8e1e7ba…:<path>`):

| tag | file:line (base) | change | occurrence count asserted |
|---|---|---|---|
| a | `tools/registry.json:1014` | `"MTE_INTEROP: PASS legs_conforming=9/9"` → `…10/10` | 1 |
| b | `tools/round21-measure.py:8` | one line: `execution authenticity.` → `execution authenticity (round 52: fleet-bound selftest).` | 1 |
| c1 | `SKILL.md:2136` | `the nine ledger legs` → `the ten ledger legs` | 1 |
| c2 | `SKILL.md:2136` | `` `mte-interop-check` (9/9) `` → `(10/10)` | 1 |
| c3 | `SKILL.md:174` | `` `tools/mutate-and-run.sh:425` `` → `:434` | 1 |
| c4 | `SKILL.md:211` | `` `tools/mutate-and-run.sh:569-574` `` → `:579-583` | 1 |
| c5 | `SKILL.md:937` | `` `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. `` → `` `${TMPDIR:-/tmp}/…` `` | 1 |
| c6 | `SKILL.md:2149` (`\| fleet mutation runner \|` row of `#### Gate/probe registry — round 51`) | `under /tmp` → `under ${TMPDIR:-/tmp}` | 2 in that row |
| d | `corpus/knowledge/fleet-kill-rate-ledger.md` (441 lines at base) | append one supersession paragraph naming the drift-pins cell | append |
| e | `.ufo/evidence/round-21/coldread/ledger.json` | new top-level `"corrections"` key (one record) | key absent before |

`SKILL.md:1321` (`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`) was deliberately **not** edited:
it is the second, unbackticked occurrence, and the item names only the `:937` bullet.

Variant commits: `va 093fad44aaf6`, `vb 3159e8326a59`, `vc f1c2fd65348f`, `vd 2b06c0a3f314`,
`ve cb4d55d2a11d`, `vall cb46b8ee9bd0`, `vbase 144d1a2d3203` (full 40-hex in `shAs*.txt`).

## 2. Bisect: sections lost per edit

Precheck RED means `cand_credited < floor_credited` (`.ufo/evidence/round-48/quality/coldread-precheck.sh:27`).
Reason classes: `input-drift:<path>` = the section's only surviving ledger entry recorded a sha256
for a file this round edits (`.ufo/evidence/round-18/measure.py:330`, called from the class-independent gate at `:353`);
`drifted=` empty = the SKILL.md text changed, so the section `sha256` no longer matches any ledger
entry (`derived` — precheck prints `drifted=` because the reason is `no-ledger-entry`, not drift;
seen in `precheck-vc.txt`).

### (a) `tools/registry.json` needle → `precheck-va.txt` — lost 3, credited 61, score 8→6

```
LOST ## Live-tree re-pin and entry-command monitor — round 17 | drifted=corpus/QUALITY.md,corpus/README.md,corpus/SOURCES.md,tools/mte-interop.py,tools/mutate-and-run.sh,tools/registry.json
LOST ### Round-21 gate/probe registry — finite environment differential | drifted=corpus/QUALITY.md,corpus/SOURCES.md,tools/mutate-and-run.sh,tools/registry.json
LOST ### Round-26 gate/probe registry — report interop | drifted=tools/registry.json
```

### (b) one line in `tools/round21-measure.py` → `precheck-vb.txt` — lost 2, credited 62, score 6

```
LOST ### Round-21 gate/probe registry — finite environment differential | drifted=corpus/QUALITY.md,corpus/SOURCES.md,tools/mutate-and-run.sh,tools/round21-measure.py
LOST ### Round-26 gate/probe registry — report interop | drifted=tools/round21-measure.py
```

(b) is a strict subset of (a). (a)∪(b) = exactly the three sections the contract's no-harm note
predicts (round-17 section, round-21 registry, round-26 registry).

### (c) the six SKILL.md replacements → `precheck-vc.txt` — lost 3, credited 61, score 6

```
LOST ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | drifted=
LOST ### Round-26 gate/probe registry — report interop | drifted=
LOST ### Using the ledger | drifted=
```

Per-replacement attribution, measured by re-sectionizing base SKILL.md with each replacement applied
alone (`.ufo/evidence/round-18/measure.py:209` `sectionize`), command in §1:

| replacement | base line | section whose `sha256` changes |
|---|---|---|
| c1 nine→ten | 2136 | 2132 `### Round-26 gate/probe registry — report interop` |
| c2 9/9→10/10 | 2136 | 2132 |
| c3 :425→:434 | 174 | 131 `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` |
| c4 :569-574→:579-583 | 211 | 131 |
| c5 TMPDIR bullet | 937 | 933 `### Using the ledger` |
| c6 `under /tmp` ×2 | 2149 | 2132 |

So (c) is 3 sections but 6 replacement sites: 131 (c3+c4), 933 (c5), 2132 (c1+c2+c6). Only 131 and
933 are *new* losses; 2132 is already lost by (a).

### (d) the kill-rate-ledger line → `precheck-vd.txt` — lost 14, credited 50, score 6

```
LOST ## The leg ledger — replay, receipt, and how it is read (round 7, measured) | drifted=corpus/README.md,corpus/SOURCES.md,corpus/knowledge/closeout-r11.md,corpus/knowledge/fleet-kill-rate-ledger.md,corpus/knowledge/incremental-pin-disposition.md,tools/mutate-and-run.sh
LOST ## The operator's runbook and the six-leg regression (round 10, measured) | drifted=corpus/knowledge/closeout-r11.md,corpus/knowledge/fleet-kill-rate-ledger.md,corpus/knowledge/incremental-pin-disposition.md,corpus/knowledge/operator-runbook.md,tools/mutate-and-run.sh,tools/registry.json,tools/trace-inputs.py
LOST ## The re-sweep cadence and the six-case confidence statement (round 8, measured) | drifted=corpus/knowledge/fleet-kill-rate-ledger.md
LOST ### Reading a receipt — the discipline | drifted=corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh
LOST ### Round-26 gate/probe registry — report interop | drifted=corpus/knowledge/fleet-kill-rate-ledger.md
LOST ### Six-case confidence statement (round 8, measured) | drifted=corpus/knowledge/closeout-r11.md,corpus/knowledge/fleet-kill-rate-ledger.md,corpus/knowledge/incremental-pin-disposition.md,corpus/knowledge/input-keyed-coldread-credit.md,corpus/knowledge/mutation-case-kagi-census.md,corpus/knowledge/operator-runbook.md,corpus/knowledge/repeated-control-precondition.md,corpus/knowledge/service-limits.md,corpus/knowledge/verification-patterns-fleet.md,tools/mutate-and-run.sh,tools/trace-inputs.py
LOST ### The map — where a reader enters, artifact by artifact | drifted=corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh
LOST ### The re-pin semantics, as executed | drifted=corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh,tools/trace-inputs.py
LOST ### The receipt at this boundary | drifted=corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh
LOST ### The service's limits — what tameshi refuses to mutation-test | drifted=PROVINCE.md,corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh
LOST ### The six-leg regression — usage and this round's receipt | drifted=corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh
LOST ### The tick, executed | drifted=corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh
LOST ### Triggers T1–T3 and the re-pin rule | drifted=corpus/knowledge/fleet-kill-rate-ledger.md,tools/mutate-and-run.sh
LOST ### What stays open — named, never closed by prose | drifted=corpus/knowledge/closeout-r11.md,corpus/knowledge/fleet-kill-rate-ledger.md,corpus/knowledge/operator-runbook.md,corpus/knowledge/service-limits.md,tools/trace-inputs.py
```

13 sections go down on the kill-rate-ledger line alone; the 14th (2132) also lists it.

### (e) the top-level `"corrections"` key → `precheck-ve.txt` — lost 0

```
COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=cb4d55d2a11d cand_credited=64 lost=0 ok
```

score stayed 8, `box3_full_page` true, `ledger_committed` true (`measure-summary.json`). Mechanism:
the round-21 wrapper adds the ledger path to the monitor's ignored inputs —
`.ufo/evidence/round-21/coldread/measure.py:112`
`module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))` — so the ledger blob is
never an input of any entry, and a top-level key does not touch `entries` (read at
`.ufo/evidence/round-18/measure.py:570`). **The corrections key costs no credit at any record
count**; only the knowledge-ledger line does.

## 3. Full stack (a–e) → `precheck-vall.txt` — lost 18, credited 46, score 6

```
COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=cb46b8ee9bd0 cand_credited=46 lost=18 RED
```

`measure-vall.json`: score 6, box3_full_page false, vetoed 0, depth_score 10 (unchanged).
Union check: (a) ∪ (b) ∪ (c) ∪ (d) ∪ (e) = 18 distinct headings, exactly the 18 LOST lines, no
extra and no missing. The monitor itself exits **0** at 46/64 — the exit code carries no signal
(`measure_exit=0` for every variant); the precheck exit 1 is the only RED.

The contract's note (`.ufo/evidence/round-52/contract.json`, `no_harm.coldread_note`) names three
sections; that measurement covers (a)+(b) only. **(c) adds 2 and (d) adds 13**, so the wave-2
re-key target is 18, not 3, and `no_harm.coldread_precheck` requires `lost=0` at the deciding run.

## 4. Re-key target list (18 sections, base line spans, sole surviving creditor)

Entry counts are the ledger entries matching the section sha; every section has exactly **one**
surviving entry at base — all other entries are already stale, so losing that one loses the section.

| # | section (base lines) | lost by | credit comes from ledger entry | that entry's inputs hit by this round |
|---|---|---|---|---|
| 1 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (131-245) | c3, c4 (text) | `#511` seats `T51W2Read01`, read_rev `02ec217c4d` | none (text edit changes the section sha) |
| 2 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` (921-932) | d | `#515` `T51W2Read05`, `02ec217c4d` | `corpus/knowledge/fleet-kill-rate-ledger.md` |
| 3 | `### Using the ledger` (933-964) | c5 (text) | `#516` `T51W2Read06`, `02ec217c4d` | none (text edit) |
| 4 | `### Reading a receipt — the discipline` (965-1009) | d | `#517` `T51W2Read07`, `02ec217c4d` | kill-rate ledger |
| 5 | `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` (1010-1020) | d | `#124` `CR19`, `4acdeac9e4` | kill-rate ledger (only input) |
| 6 | `### Triggers T1–T3 and the re-pin rule` (1069-1091) | d | `#358` `Read04B`, `b05d2ee8e7` | kill-rate ledger (of 16 inputs) |
| 7 | `### Six-case confidence statement (round 8, measured)` (1092-1154) | d | `#318` `Read16`, `2227d8338c` | kill-rate ledger (of 7) |
| 8 | `### The tick, executed` (1164-1211) | d | `#519` `T51W2Read09`, `02ec217c4d` | kill-rate ledger |
| 9 | `### The receipt at this boundary` (1212-1229) | d | `#520` `T51W2Read10`, `02ec217c4d` | kill-rate ledger |
| 10 | `### The re-pin semantics, as executed` (1230-1245) | d | `#130` `CR26`, `4acdeac9e4` | kill-rate ledger |
| 11 | `### The service's limits — what tameshi refuses to mutation-test` (1246-1271) | d | `#403` `ColdA04`, `bb681566b1` | kill-rate ledger |
| 12 | `## The operator's runbook and the six-leg regression (round 10, measured)` (1272-1280) | d | `#521` `T51W2Read11`, `02ec217c4d` | kill-rate ledger (only input) |
| 13 | `### The six-leg regression — usage and this round's receipt` (1302-1364) | d | `#522` `T51W2Read12`, `02ec217c4d` | kill-rate ledger |
| 14 | `### The map — where a reader enters, artifact by artifact` (1380-1395) | d | `#523` `T51W2Read13`, `02ec217c4d` | kill-rate ledger |
| 15 | `### What stays open — named, never closed by prose` (1449-1463) | d | `#217` `L1 TameshiR21 author source re-anchor`, `8eaae28ec4` | kill-rate ledger |
| 16 | `## Live-tree re-pin and entry-command monitor — round 17` (1814-1845) | a | `#527` `T51W2Read17`, `02ec217c4d` | `tools/registry.json` |
| 17 | `### Round-21 gate/probe registry — finite environment differential` (1964-2103) | a, b | `#451` `ColdB10`, `bb681566b1` | `tools/registry.json`, `tools/round21-measure.py` |
| 18 | `### Round-26 gate/probe registry — report interop` (2132-2171) | a, b, c1/c2/c6, d | `#530` `T51W2Read20`, `02ec217c4d` | `tools/registry.json`, `tools/round21-measure.py`, kill-rate ledger |

Entry indices are positions in `.ufo/evidence/round-21/coldread/ledger.json` `entries` at base;
seats/read_rev/inputs read from that file. `#451` also lists `.ufo/evidence/round-21/coldread/ledger.json`,
which the wrapper ignores (`round-21/coldread/measure.py:112`) — that is why it survives the
`corrections` key but not (a)/(b).

Cross-check that matters for wave 2: **11 of the 18** sole creditors are the round-51 re-key
entries (`seats` starting `T51W2Read`): sections 131, 921, 933, 965, 1164, 1212, 1272, 1302, 1380,
1814, 2132. Of the 20 round-51 re-key entries in the ledger, **8 list
`corpus/knowledge/fleet-kill-rate-ledger.md`**, so a single supersession line in that file
un-credits 8 of them at once. The round-52 re-key therefore re-does most of the round-51 re-key.

## 5. Extra entry keys `findings` / `reader_files` — tolerated

`tolerance.log`, `measure-vtol.json`, `measure-vtol2.json`:

- **vtol** (`1ede3d5e48d08a71fb2ca10864b48c7ba164ff51`): appended one synthetic entry
  (532 entries) carrying `findings` and `reader_files` plus clean shape (`verified-record`,
  `blocking_gaps 0`, `wrong_expectations 0`). Monitor: **exit 0, 64/64 credited, score 8,
  vetoed 0, ledger_committed true**.
- **vtol2** (`1464ddd5f0007aa6de2b080d00c0ea33bdaabc9d`): added `findings` + `reader_files` to the
  21 existing entries that list both `tools/registry.json` and `tools/round21-measure.py`.
  Monitor: **exit 0, 64/64, score 8, vetoed 0**.

Mechanism: the monitor reads only whitelisted per-entry fields — `entry_failure` /
`entry_credit_reason` (`.ufo/evidence/round-18/measure.py:459`, `:477`), `inputs_view` (`:321`),
`trace_reason` (`:373`) — and unknown keys are never inspected. So the round-52 re-key entries may carry the
readers' `findings`/`reader_files` without any monitor change.

## 6. Risks / blockers

- No blockers. The probe ran entirely in scratch; the clone is deleted after the receipts were
  copied. No claim was run: no `--selftest`, no C1/C2 counter, no `no-harm.sh`.
- Prediction scope: this bisect models only **credit loss**. It predicts nothing about whether the
  wave-2 re-key entries will themselves pass the input gate (they must record shas of the edited
  files, including the new kill-rate-ledger bytes) or the strict trace gate (`trace_reason`,
  `.ufo/evidence/round-18/measure.py:373`), nor about C2 `m6`.
- (b) is modelled as a one-line docstring change; any other one-line change to
  `tools/round21-measure.py` has the same effect (loss keys on the file's sha256, not its content).
  So `vb`'s two lost sections are the floor for that edit, not a property of my particular line.
- `SKILL.md:1321` still says `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`; line 1321 lies inside
  section 1302 (`### The six-leg regression — usage and this round's receipt`, spans 1302-1364), which
  (d) already un-credits — so a second TMPDIR edit there would cost no *additional* section, but it
  is outside this item's edit set and was left alone.

## Summary

1. Floor at base is 64/64 credited, score 8; the full edit stack (a–e) leaves 46/64, score 6, 18 sections lost, precheck RED.
2. (a) registry needle loses 3; (b) round21-measure line loses 2 (subset of a); (c) the six SKILL replacements lose 3; (d) the kill-rate-ledger line loses 14; (e) the `corrections` key loses 0.
3. Contract's "three sections, score 8→6" note covers only (a)+(b); the real wave-2 re-key target is 18.
4. The `corrections` key is free because the wrapper ignores the ledger blob as an input (`round-21/coldread/measure.py:112`); the knowledge-ledger line is the expensive edit (13 unique sections + 2132).
5. Every lost section has exactly one surviving creditor entry at base, so each needs one fresh reader entry; 11 of 18 are the round-51 `T51W2Read*` re-keys, re-done.
6. Extra entry keys `findings`/`reader_files` are tolerated: exit 0, 64/64, score 8, vetoed 0, both for a synthetic appended entry and for 21 existing entries.
7. The monitor exits 0 at 46/64 — only `coldread-precheck.sh:27` (lost>0 → exit 1) discriminates, and `no_harm.coldread_precheck` demands lost=0 at the deciding run.
8. No blocker; scratch deleted, receipts copied to `.ufo/waves/round-52/w1/T52W1ExecColdreadProbe.receipts/`.
