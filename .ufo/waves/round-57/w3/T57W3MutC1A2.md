# T57W3MutC1A2 — mutation probe of the round-57 C1 counter, amendment 2

**Seat**: T57W3MutC1A2 (wave 3 of 3, L1 `TameshiR57`)
**Lane**: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Lane base**: `5e3569969b532310d2b8a3d130901757a3df356b`
**Final monitored-content commit C0b**: `adf87899c70d616140a81185a8f9acbbdfb30392`
**Mutated artifact**: `.ufo/evidence/round-57/c1/measure.py` (the round-57 C1 counter, amendments 1 and 2)
**Machine-readable output**: `.ufo/waves/round-57/w3/T57W3MutC1A2.json`
**Receipts**: `.ufo/waves/round-57/w3/T57W3MutC1A2-receipts/`
**Staged proposals (NOT applied)**: `.ufo/waves/round-57/w3/T57W3MutC1A2/stage/`

## 0. Headline

| | |
|---|---|
| mutants built | **11** (ten defect sites; the `panel_tie` site has two variants) |
| **killed** with the proposed selftest cases | **11 / 11** |
| killed by the **shipped selftest alone** | **2 / 11** (M01, M02b) |
| **survived** the shipped selftest alone | **9 / 11** (M02a, M03, M04, M05, M06, M07, M08, M09, M10) |
| baseline of the shipped selftest on pristine bytes | **RED — 92/99, exit 1** |

Two findings for the L1, in order of consequence:

1. **The shipped selftest fails on the pristine amendment-2 bytes.** `python3 measure.py --selftest`
   prints `C1_R57_SELFTEST: 92/99 pass` and exits 1 on the exec seat's staged copy, and
   `89/96 pass` on the lane's evidence copy. The seven failing cases are exactly the panel-arm
   cases. A red baseline makes every mutant inconclusive, so this seat could not adjudicate
   anything until the baseline was made green.
2. **The amendment-2 arms (A8 tie, A9 provenance) have no selftest coverage.** Nine of the eleven
   mutants survive the shipped selftest. The proposed cases kill all eleven.

Both are **coverage findings, not a licence to change the contract**. Nothing was edited in the
lane; the fixes are staged for the L1.

## 1. Base selection and poll

The item's poll target was
`.ufo/waves/round-57/w3/T57W3ExecC1SelftestA2/stage/.ufo/evidence/round-57/c1/measure.py`.
It was present on the first poll and never changed during the seat:

```
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3ExecC1SelftestA2/stage/.ufo/evidence/round-57/c1/measure.py
caabfbf7ef5470b34bec401af6c9672c59bc56dcbce7e45cf23707621771e1bb  .../T57W3ExecC1SelftestA2/stage/.ufo/evidence/round-57/c1/measure.py
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/measure.py
6f3b7627a41dfbad2838f2d1fe31f7f7136a9a3de2fcc4a9bf2cd1c207013ca8  .../.ufo/evidence/round-57/c1/measure.py
```

Both hashes were re-verified identical at the end of the seat (receipt `01-base-hashes.txt`).
The matrix was run against **both** copies (staged `caabfbf7…`, lane copy `6f3b7627…`); the
verdicts are identical on both.

## 2. The red baseline (finding 1)

Command and output (receipt `02-shipped-selftest-staged.out`, `03-shipped-selftest-lane-copy.out`):

```
$ python3 base-staged.py --selftest --work "$S/work-r0"
SELFTEST panel agrees: panel=0/5, pass                                FAIL
SELFTEST panel exactly allowed disagreements passes                   FAIL
SELFTEST panel one over allowed: panel_over=1                          FAIL
SELFTEST panel over counts the excess only                             FAIL
SELFTEST panel without a verdict for an id disagrees                   FAIL
SELFTEST panel without a verdict for a fixed-at-base id disagrees      FAIL
SELFTEST cli good exits 0, verdict is last line                       FAIL
C1_R57_SELFTEST: 92/99 pass
exit=1
```

**Cause** (read from the bytes, confirmed by the counter's own EXPLAIN note):

```
  last run: {'panel_prov': 3} notes=[('panel-provenance', 'R50.1', None), ('panel-provenance', 'R50.2', None), ('panel-provenance', 'R50.3', None)]
```

The selftest's `run()` helper writes the panel file as
`pblob = json.dumps({'verdicts': panel})` — **no `detail`, no `files`**. Amendment 2's
`panel_provenance()` therefore reads `det = None` for every id, `seat = None`, the seat's wave
file is absent, and every id is counted as a provenance shortfall: `counts['panel_prov'] == 3` on
every panel case, so `total` is 3 and the "panel agrees: panel=0/5, pass" case cannot pass. The
`cli good exits 0` case fails for the same reason.

This is a **fixture gap in the selftest harness, not a defect in the amendment-2 code**: the
provenance arm itself behaves correctly on the fixture it is given (see §4, M04/M05/M06/M09/M10).

**Repair (scratch only).** The selftest's panel fixture is extended so the provenance arm has a
passing case: the panel file gains `detail` (a seat per id), the seat's own
`.ufo/waves/round-57/w2/<seat>.json` wave file is written, and `w2-results.json` lists the seat.
The cli pin is then read from the panel file on disk instead of from a re-serialised dict.

```
$ python3 repair.py base-staged.py base-repaired.py
$ python3 base-repaired.py --selftest --work "$S/work-r2"
C1_R57_SELFTEST: 99/99 pass
exit=0
```

Receipt `04-repaired-selftest-staged.out`. The repair touches **only** the selftest harness; the
counter's code region is untouched, so the mutants remain single edits of the amendment-2 code.

## 3. Detectors

Two independent detectors were run on pristine bytes, on every mutant, and on the restored bytes.

* **D1 — the shipped selftest**, with the harness repair above so the baseline is green
  (99/99). Command: `python3 <mutant> --selftest --work <dir>`. Signal: the set of failing
  `SELFTEST` case names and the exit code.
* **D2 — an independent amendment-2 probe** written by this seat (receipt `probe.py`). It builds
  its own fixture lane, calls `measure()` of the module under test, and prints the observable
  value of each amendment-2 arm (`panel_prov`, `fixed_bad`, `evidence_bad`, the terms line). Its
  eleven scenarios cover: canonical-path exclusion (A7), the panel-commit tie and its three
  controls (A8), and the five provenance sub-checks plus the w2/w3 routing (A9). On pristine bytes
  every scenario reproduces its expected observation, so a difference on a mutant is attributable
  to the mutation.

Verdict rule: **KILLED** if either detector shows a difference attributable to the mutation;
**SURVIVED** if neither does; **INCONCLUSIVE** if a mutant only *hides* baseline failures.

## 4. The mutants

Each mutant is a **single edit** of the amendment-2 code of the base file. Every old string was
asserted to occur **exactly once** in the base (`old_string_occurrences_in_base == 1` for all
eleven), and each mutant was built in a **fresh scratch copy** — the base file was asserted
byte-unchanged after every mutation.

| id | mutation (single edit) | base site | shipped selftest | with proposed cases | D2 probe |
|---|---|---|---|---|---|
| M01 | `npath`: `posixpath.normpath(p)` removed | A7 | **KILLED** | KILLED | KILLED |
| M02a | `panel_tie`: `startswith(pc[:40])` → always true | A8 | survived | **KILLED** | KILLED |
| M02b | `panel_tie`: `len(pc) >= 7` dropped | A8 | **KILLED** | KILLED | KILLED |
| M03 | `pcommits`: restriction to `fixed` verdicts dropped | A8 | survived | **KILLED** | KILLED |
| M04 | provenance: sha check removed | A9 | survived | **KILLED** | KILLED |
| M05 | provenance: verdict-equality removed | A9 | survived | **KILLED** | KILLED |
| M06 | provenance: `listed` check removed | A9 | survived | **KILLED** | KILLED |
| M07 | provenance: w3 path routing removed | A9 | survived | **KILLED** | KILLED |
| M08 | `panel_prov` not added to `TERMS` | A9 | survived | **KILLED** | KILLED |
| M09 | `panel_prov` count not assigned | A9 | survived | **KILLED** | KILLED |
| M10 | provenance: loop skipping ids | A9 | survived | **KILLED** | KILLED |

### Exact edits

```
M01  "    return posixpath.normpath(p) if isinstance(p, str) and p else p"
   -> "    return p"

M02a "        panel_tie = len(pc) >= 7 and commit.startswith(pc[:40])"
   -> "        panel_tie = len(pc) >= 7 and True"

M02b "        panel_tie = len(pc) >= 7 and commit.startswith(pc[:40])"
   -> "        panel_tie = commit.startswith(pc[:40])"

M03  "            pcommits = {k: (v.get('commit') or '') for k, v in panel.get('detail', {}).items()\n
                          if isinstance(v, dict) and panel.get('verdicts', {}).get(k) == 'fixed'}"
   -> "            pcommits = {k: (v.get('commit') or '') for k, v in panel.get('detail', {}).items()\n
                          if isinstance(v, dict)}"

M04  "        ok = blob is not None and hashlib.sha256(blob).hexdigest() == files.get(seat) and seat in listed"
   -> "        ok = blob is not None and seat in listed"

M05  "            ok = v == panel.get('verdicts', {}).get(d['id'])"
   -> "            ok = True"

M06  "        ok = blob is not None and hashlib.sha256(blob).hexdigest() == files.get(seat) and seat in listed"
   -> "        ok = blob is not None and hashlib.sha256(blob).hexdigest() == files.get(seat)"

M07  "        wv = 'w3' if isinstance(seat, str) and seat.startswith('T57W3') else 'w2'"
   -> "        wv = 'w2'"

M08  "         'declined_over', 'this_round_short', 'panel_pin', 'panel_over', 'base_status_bad', 'panel_prov')"
   -> "         'declined_over', 'this_round_short', 'panel_pin', 'panel_over', 'base_status_bad')"

M09  "            counts['panel_prov'] = panel_provenance(lane, rev, defects, panel, note)"
   -> "            counts['panel_prov'] = 0"

M10  "    for d in defects:\n        det = panel.get('detail', {}).get(d['id'])\n        seat = det.get('seat') if isinstance(det, dict) else None\n"
   ->  "    for d in defects:\n        if panel.get('verdicts', {}).get(d['id']) == 'declined':\n            continue\n        det = panel.get('detail', {}).get(d['id'])\n        seat = det.get('seat') if isinstance(det, dict) else None\n"
```

The executed mutants and their hashes are in
`T57W3MutC1A2-receipts/06-mutation-matrix-staged.json`; the mutant files are reproduced
deterministically by `drive.py` (receipt `drive.py`).

### Observed differences (D2 probe, representative)

```
M01  probe npath_spotcheck     evidence_bad 1 -> 0   agree 0 -> 1   total 1 -> 0
M02a probe tie_always_true     fixed_bad    1 -> 0   agree 0 -> 1   total 1 -> 0
M02b probe tie_len7_dropped    fixed_bad    1 -> 0   agree 0 -> 1   total 1 -> 0
M03  probe pcommits_filter     fixed_bad    1 -> 0   agree 0 -> 1   total 1 -> 0
M04  probe prov_sha             panel_prov   1 -> 0   total 1 -> 0
M05  probe prov_verdict         panel_prov   1 -> 0   total 1 -> 0
M06  probe prov_listed          panel_prov   1 -> 0   total 1 -> 0
M07  probe prov_w3_route        panel_prov   0 -> 2   total 0 -> 2
M08  probe (all scenarios)      terms line loses the `panel_prov=` field
M09  probe prov_sha             panel_prov   1 -> 0   total 1 -> 0
M10  probe prov_loop_skip       panel_prov   1 -> 0   total 1 -> 0
```

Every mutant moves an observable counter value in the direction that breaks the amendment-2
guarantee — a mutant that lets a row through (`fixed_bad` 1 → 0), lets a bad provenance through
(`panel_prov` 1 → 0), or invents a shortfall (`panel_prov` 0 → 2). No mutant is equivalent.

## 5. Proposed cases for the survivors (finding 2)

Nine mutants survive the shipped selftest. Each proposed case moves its tally off zero **and**
has an independent control that passes. Added to the repaired harness they take the suite from
99/99 to **110/110**, and every one of the eleven mutants is killed (receipt
`08-mutant-kill-table-with-cases.txt`).

| mutant | proposed case | what it pins |
|---|---|---|
| M02a | `A8 tie control: a panel commit that is not a prefix refuses the row` | A8's prefix test is a real test: a panel commit that is not a prefix of the row's commit must not tie |
| M02b | `A8 tie: a panel commit shorter than 7 hex chars does not tie the row` | the `len(pc) >= 7` guard |
| M03 | `A8 tie: a non-fixed panel verdict does not tie the row` | only a `fixed` verdict's panel commit may tie |
| M04 | `A9 provenance: a seat file whose sha does not match the panel pin counts a shortfall` | the provenance sha check |
| M05 | `A9 provenance: a seat verdict that differs from the panel verdict counts a shortfall` | the provenance verdict-equality |
| M06 | `A9 provenance: a seat that the wave results do not list counts a shortfall` | the `listed` check |
| M07 | `A9 provenance: a w3 seat is looked up in w3` | the w2/w3 routing by seat-name prefix |
| M08 | `A9: the terms line carries panel_prov` | `panel_prov` is in `TERMS` |
| M09 | `A9 provenance: a shortfall makes the verdict line fail` | the provenance count reaches the verdict |
| M10 | `A9 provenance: a declined id is counted too` | the provenance loop visits every id |

Kill evidence with the proposed cases (receipt `08-mutant-kill-table-with-cases.txt`):

```
BASE: staged exec-seat copy + harness repair + amendment-2 cases
PRISTINE: rc=0 C1_R57_SELFTEST: 110/110 pass  failing=0
M01  KILLED       C1_R57_SELFTEST: 109/110 pass  canonical admissible path passes
M02a KILLED       C1_R57_SELFTEST: 109/110 pass  A8 tie control: a panel commit that is not a prefix refuses the row
M02b KILLED       C1_R57_SELFTEST: 105/110 pass  A8 tie: a non-fixed panel verdict does not tie the row; A8 tie: a panel commit shorter than 7 hex chars does not tie the row; forgery: ...; message naming R50.12 / xR50.1 / v1.R50.1 does not name R50.1; tie: a different path in the item text refused
M03  KILLED       C1_R57_SELFTEST: 109/110 pass  A8 tie: a non-fixed panel verdict does not tie the row
M04  KILLED       C1_R57_SELFTEST: 108/110 pass  A9 provenance: a seat file whose sha does not match the panel pin counts a shortfall; A9 provenance: a shortfall makes the verdict line fail
M05  KILLED       C1_R57_SELFTEST: 108/110 pass  A9 provenance: a declined id is counted too; A9 provenance: a seat verdict that differs from the panel verdict counts a shortfall
M06  KILLED       C1_R57_SELFTEST: 109/110 pass  A9 provenance: a seat that the wave results do not list counts a shortfall
M07  KILLED       C1_R57_SELFTEST: 109/110 pass  A9 provenance: a w3 seat is looked up in w3
M08  KILLED       C1_R57_SELFTEST: 109/110 pass  A9: the terms line carries panel_prov
M09  KILLED       C1_R57_SELFTEST: 105/110 pass  A9 provenance: a declined id is counted too; A9 provenance: a seat file whose sha does not match the panel pin counts a shortfall; A9 provenance: a seat that the wave results do not list counts a shortfall; A9 provenance: a seat verdict that differs from the panel verdict counts a shortfall; A9 provenance: a shortfall makes the verdict line fail
M10  KILLED       C1_R57_SELFTEST: 106/110 pass  A9 provenance: a declined id is counted too; A9 provenance: a seat file whose sha does not match the panel pin counts a shortfall; A9 provenance: a seat that the wave results do not list counts a shortfall; A9 provenance: a shortfall makes the verdict line fail
```

## 6. What is NOT claimed

* **The amendment-2 counter code is not shown to be defective.** Every mutant was killed, i.e.
  the code as written distinguishes the correct behaviour from a plausible defect. This seat found
  no defect in the amendment-2 code itself.
* **The finding is about the selftest.** Nine of eleven mutants of the amendment-2 arms survive
  the shipped selftest: the arms are implemented but untested, and the suite that would expose
  that is itself red on the pristine bytes.
* No contract change is proposed. The staged files only make the existing behaviour observable.

## 7. Staged proposals (not applied)

`.ufo/waves/round-57/w3/T57W3MutC1A2/stage/`

* `.ufo/evidence/round-57/c1/measure.py` — the drop-in: harness repair + amendment-2 cases
  (110/110 green). Built from the exec seat's staged copy `caabfbf7…`.
* `harness-repair.patch` — the harness repair alone (99/99 green).
* `selftest-cases.patch` — the amendment-2 cases alone, on top of the repair.

The repair and the cases are separable so the L1 can take one without the other; the exec seat
`T57W3ExecC1SelftestA2` was working in the same area and was notified of both findings.

## 8. Restoration evidence

* **No lane file was edited.** `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status
  --porcelain` shows only this seat's own untracked wave-3 deliverables; no tracked lane file is
  modified.
* Every mutant was built in a **fresh scratch copy** under
  `$HYAKU_SCRATCH/tameshi-r57/T57W3MutC1A2/`. The base file was asserted byte-unchanged after
  each mutation (`assert sha(open(BASE,'rb').read()) == base_sha`) and re-hashed at the end of
  the seat.
* Before/after hashes (identical before and after):

```
caabfbf7ef5470b34bec401af6c9672c59bc56dcbce7e45cf23707621771e1bb  exec-seat staged .ufo/evidence/round-57/c1/measure.py
6f3b7627a41dfbad2838f2d1fe31f7f7136a9a3de2fcc4a9bf2cd1c207013ca8  lane .ufo/evidence/round-57/c1/measure.py
```

* No `git` mutation was run in the lane or in the fleet repo; the probe's fixture repos are
  created under the scratch dir and each asserts `git rev-parse --show-toplevel` equals the
  fixture dir before any commit there.
* Scratch: `$HYAKU_SCRATCH/tameshi-r57/T57W3MutC1A2` (removed by the seat's `trap`).

## 9. Commands run

```
sha256sum <both base copies>                                  # receipts 01
python3 base-staged.py    --selftest --work $S/work-r0        # receipts 02  (92/99, exit 1)
python3 base-evidence.py  --selftest --work $S/work-r1        # receipts 03  (89/96, exit 1)
python3 repair.py base-staged.py base-repaired.py             # harness repair (scratch)
python3 base-repaired.py  --selftest --work $S/work-r2        # receipts 04  (99/99, exit 0)
python3 addcases.py base-repaired.py base-repaired-cases.py proposed-cases.patch
python3 base-repaired-cases.py --selftest --work $S/work-r3   # receipts 05  (110/110, exit 0)
python3 probe.py <base> $S/work-probe                         # D2 probe, 11 scenarios
python3 drive.py base-staged.py   matrix/   work-drive/       # receipts 06  (full matrix, staged base)
python3 drive.py base-evidence.py matrix-ev/ work-drive-ev/   # receipts 07  (full matrix, lane copy)
python3 (mutant matrix on the repaired+cases base)            # receipts 08  (11/11 killed)
```

## 10. Tooling

No tool was installed, upgraded or downgraded: `python3 3.14.8` and `git` were already present
and sufficient, so the operator tooling directive was not triggered. All pacman transactions
remain paused as instructed.
