# T54W1Crit02 — seven frozen vs 23 actual (C1)

Axes: discernment, calibration.
Milestone: falsify the claims.
Verdict: **the frozen predicate needs an amendment.**

Exact sentence:
> Amend C1 arms 3–4 (and the contract target's rekey/reader clauses) to require a `rekey-r54-<c0>`-bound credit-passing entry and a matching committed `*Read*.json` pin for every heading in `lost-headings-at-c0.json` (23), not only `lost-headings-at-base.json` (7) — otherwise `C1_R54_PASS=true` can hold while any of the sixteen C0-only losses is credited by a fig-leaf entry outside that re-key directory.

---

## Counterexample

Binder authority is the 23 (`lost-headings-at-c0.json` ∪ base seven). Counter arms 3–4 and the stable scan only enforce the frozen seven. A deciding revision that (a) properly re-keys and reader-pins the seven, and (b) restores credit for the sixteen via ledger entries whose traces do **not** lie under `rekey-r54-<c0>/` (and need no `*Read*.json`), still clears arms 1–5 if arm1 prints `cand_credited=64 lost=0 ok`. That is a fig leaf: credit without the round's own re-key/reader provenance for sections the wave treats as the re-read set.

Impacted axes: calibration (credit provenance), discernment (duplicate heading authorities).
Smallest safe correction: the amendment sentence above (widen arms 3–4 denominator to the C0 lost set; keep arm1's 64/64 floor).

---

## A1 — Set difference: 16 of 23 are not among the seven

### Command
```bash
python3 - <<'PY'
import json
base=json.load(open("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/lost-headings-at-base.json"))
c0=json.load(open("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/lost-headings-at-c0.json"))
print("base", len(base), "c0", len(c0), "only_c0", len(set(c0)-set(base)), "base_subset", set(base)<=set(c0))
for h in c0:
    if h not in set(base):
        print("ONLY_C0", h)
PY
```

### Output
```
base 7 c0 23 only_c0 16 base_subset True
ONLY_C0 ## The leg ledger — replay, receipt, and how it is read (round 7, measured)
ONLY_C0 ### The tick and the pin read
ONLY_C0 ### Triggers T1–T3 and the re-pin rule
ONLY_C0 ### The service's limits — what tameshi refuses to mutation-test
ONLY_C0 ## The operator's runbook and the six-leg regression (round 10, measured)
ONLY_C0 ## Repeated controls and gate registry — round 12
ONLY_C0 ### Gate/probe registry
ONLY_C0 ## Pin disposition and provenance correction — round 13
ONLY_C0 ### Round-13 gate/probe registry
ONLY_C0 ## Effective expectation reconciliation — round 14
ONLY_C0 ## Context gate classification and explicit exit classes — round 15
ONLY_C0 ### Round-15 gate/probe registry
ONLY_C0 ## Live-tree re-pin and entry-command monitor — round 17
ONLY_C0 ### Round-17 gate/probe registry — re-pin and monitor
ONLY_C0 ### Round-18 gate/probe registry — routed-defect closure
ONLY_C0 ### Round-21 gate/probe registry — finite environment differential
```

Receipt: `.ufo/waves/round-54/w1/T54W1Crit02-receipts/replay-set-diff.txt`

---

## A2 — The sixteen were credited at base and all lost at C0 (C0 edit drift)

### Command
```bash
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev d33053f7552db4bd290c99a36979760f544c41ad \
  > /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1Crit02-receipts/coldread-at-base.json
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 59c38109bf119d0e9d4f878644a82babc937bc1e \
  > /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1Crit02-receipts/coldread-at-c0.json
# then summarize the sixteen (script in receipts/sixteen-credit-status.txt)
```

### Output (summary)
```
sixteen_count 16
SUMMARY base_credited_among_16 16
SUMMARY c0_credited_among_16 0
base_total_credited 57
c0_total_credited 41
```

Each of the sixteen fails at C0 with `input-drift:` on paths this round edited (`tools/*.py`, `tools/registry.json`, `corpus/SOURCES.md`, …). Full per-heading table: `T54W1Crit02-receipts/sixteen-credit-status.txt`.

---

## A3 — Precheck arm still covers the sixteen (credit floor)

Arm1 runs frozen `coldread-precheck.sh` with floor `ef19d8e1…` and requires a last line containing `lost=0 ok`. The precheck computes `lost = floor_credited − cand_credited`. Floor credits 64; the sixteen were in that credited set at base/floor; therefore arm1 cannot pass until every one of them is credited again at the deciding revision.

### Command
```bash
W=$(mktemp -d /fast/scratch/hyaku/tameshi-r54/T54W1Crit02/work-XXXXXX)
export TMPDIR=$W HYAKU_SCRATCH=/fast/scratch/hyaku
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 59c38109bf119d0e9d4f878644a82babc937bc1e \
  --work "$W" --explain
```

### Output
```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=59c38109bf11 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

Receipt: `T54W1Crit02-receipts/c1-at-c0.stdout`

Precheck formula (bytes of frozen script):
```
lost = sorted(fc - cc)
state = 'RED' if len(cc) < len(fc) else 'ok'
```
Receipt: `T54W1Crit02-receipts/precheck-lost-formula.txt`

So: **credit coverage for the sixteen exists (arm1). Provenance coverage does not (arms 3–5).**

---

## A4 — Duplicate authorities: binder uses 23; counter uses 7

### Command
```bash
rg -n "lost-headings|frozen =" /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py
rg -n "HEADINGS|BASE7|lost-headings" /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/integrate/binder.py
```

### Output
```
=== measure.py HEADINGS load ===
18:               for EVERY heading frozen in c1/lost-headings-at-base.json the
52:HEADINGS = '.ufo/evidence/round-54/c1/lost-headings-at-base.json'
169:    frozen = json.loads((Path(__file__).resolve().parent / 'lost-headings-at-base.json').read_text('utf-8'))
=== binder.py HEADINGS load ===
12:For every heading in .ufo/evidence/round-54/c1/lost-headings-at-c0.json (plus the
50:HEADINGS = json.loads(Path(LANE, E, 'c1/lost-headings-at-c0.json').read_text('utf-8'))
51:BASE7 = json.loads(Path(LANE, E, 'c1/lost-headings-at-base.json').read_text('utf-8'))
52:HEADINGS = sorted(set(HEADINGS) | set(BASE7))
```

`measure.py` never opens `lost-headings-at-c0.json` (`"lost-headings-at-c0.json referenced? False"` in `arm4-scope-ast.txt`). Wave assigns 23 `*Read*` seats covering all sixteen (`wave-vs-counter-readers.txt`: `sixteen_with_wave_reader 16`), but arm4 only loops `for h in frozen` (denominator 7).

Contract target text matches that narrow scope (`"every one of the seven base-lost sections"`) while still requiring `cand_credited=64` — the split that creates the fig-leaf hole.

Receipt: `T54W1Crit02-receipts/dual-authority.txt`, `contract-scope.txt`

---

## A5 — Fig-leaf simulation (arms 3–4 ignore the sixteen)

### Command
```bash
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1Crit02-receipts/../T54W1Crit02-receipts/figleaf-simulation.txt
# (generated by the seat; contents below)
```

### Output
```
hypothetical: 7 proper rekeys+readers; 16 credited outside rekey-r54
arm3_rekeyed_ok True => 7/7
arm4_readers_ok True => 7/7
arm1_all_23_of_lost_credited_proxy True
sixteen_with_rekey_bound 0
sixteen_with_reader_pin 0
C1_PASS_IF_MONITOR_AND_STABLE_ALSO_OK True
```

Structural confirm from counter source: unstable-input scan iterates `for e in bound` where `bound` is traces under `rekey-r54-<c0>/` only — so a LOG.md-pinned fig-leaf **outside** that directory is invisible to arm5 as well (`figleaf-structural.txt`).

**Answer:** yes — closure can accept `C1_R54_PASS=true` while a section among the sixteen has a fig-leaf entry.

---

## Verdict

The claim "precheck still covers the 23" is **true for the credit floor** and **false for re-key/reader provenance**. That gap is a fixable defect (duplicate heading authorities between binder and counter), not an accepted `cannot_see` tradeoff: `cannot_see` covers fairness of judgment, not whether the frozen predicate even requires a reader pin / rekey bind for the C0 re-read set.

**the frozen predicate needs an amendment**, with the exact sentence in the header.

---

## Tooling / scratch

- No pacman/uv installs this seat.
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1Crit02/` (work dirs under it; trap cleanup on seat exit).
- Census: `scripts/sources-census.sh validate --root … tameshi` → exit 0 (`T54W1Crit02-receipts/census-validate.txt`).
- No lane production files edited; write scope only `.ufo/waves/round-54/w1/T54W1Crit02.md` + `T54W1Crit02-receipts/`.
