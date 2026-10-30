# T58W2CritLedger — round-58 wave-2 ledger critic report

Seat: T58W2CritLedger · Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
C0 (content-final): `8063d0a551fc5b3cb5a2d397da7353af53444534` (verified lane tip) · Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`
Machine-readable output: `T58W2CritLedger.json` · Receipts: `T58W2CritLedger-receipts/`

## 1. Frozen C1 counter at C0

Run in a scratch clone detached at C0 (`git clone --shared` + `checkout --detach`; verified
`rev-parse --show-toplevel` = the clone). Frozen instrument, untouched:

```
$ python3 .ufo/evidence/round-58/c1/measure.py --lane $S/clone --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --work $S/work-c1b
C1_R58: self=9b7c01673912 rev=8063d0a551fc rows=51/51 agree=51/51 old49=ok fixed=37 declined=1 thisround=8 panel=4/5 spot=ok total=0 C1_R58_PASS=true
exit code: 0
```

The counter's own docstring names its blind spot, which this seat attacks: *"What it cannot see:
that a keyed, new excerpt really resolves the defect (semantic support)."*

## 2. Semantic audit — the five weakest fixed rows

Chosen by evidence incidence (incidental single-line excerpts, receipt-only evidence,
cross-generation evidence). For each: full statement from the frozen set, installed row, commit
ancestry, `status_at_base` coherence, and whether the excerpt actually resolves the defect at C0.

| id | sab→status | fix commit | ancestry/A2 | semantic verdict |
|----|------------|-----------|-------------|------------------|
| R51.5 | open→fixed | `38e4e3aff7cf` | ok (post-base, names id) | **agree** |
| R52.1 | fixed→fixed | `441c26bec5e4` | ok (pre-base, basename tie) | **agree** |
| R53.5 | open→fixed | `764f87bc8a9f` | ok (post-base, names id) | **agree** |
| R53.9 | fixed→fixed | `d33053f7552d` | ok (pre-base, A8 panel tie) | **agree** |
| R55.6 | fixed→fixed | `981c5e8b20a2` | ok (pre-base, A8 panel tie) | **agree** |

- **R51.5** — commit `38e4e3aff7cf` adds `## R51.5 — cross-domain handoff to kagi` to
  `corpus/lessons/round-58.md:88` plus stage receipt
  `.ufo/waves/round-58/w1/T58W1Fix08/stage/kagi-crossdomain-r51.5.md`; no kagi file edited.
  Kagi claims verified read-only at the pinned revision `c49023b773b6…` (kagi's current HEAD):
  `corpus/drift-pins.sh` line 158 `printf 'DRIFT   %s %s\n' "$p" …`, line 400 `out=$(…)`,
  line 403 `elif ! grep -q "$3" <<< "$out"; then` (unanchored), line 404 `no /%s/ in output`.
  Lateness note: filed 7 rounds after the promised "next report"; round-52's report instead
  rejected the suggested fix (`round-52.md:15`). Substance real.
- **R52.1** — `status_at_base=fixed` is coherent: the honest-stop branch was recorded
  (`LOG.md:2444` "round 52 (honest stop, run wrap-up)", appended by `a41195dfc13a`, ancestor of
  base) and the successor generation's frozen deciding receipts settle the calibration debt:
  `.ufo/evidence/round-54/after/c1.stdout:5` `credited=64 lost=0 rekeyed=7/7 readers=7/7
  monitor=8/64 unstable=0 total=0 C1_R54_PASS=true` (byte-verified at C0). The named round-52
  script `.ufo/evidence/round-52/deciding-run.sh` still exists at C0 and was never re-run; the
  resolution stands on the item's disjunctive wording (INFERENCE, judged fair).
- **R53.5** — `764f87bc8a9f` adds `.ufo/evidence/round-53/verify-freeze-final.stdout`
  (`FREEZE 9e09db2b6c52 files=8 amendments=7` + `FREEZE_INTEGRITY: OK`, byte-verified) and an
  append-only `LOG.md` correction naming `cf872769ed8a…` and `9e09db2b…`, explicitly superseding
  `e62d9971 (amendments 1–5)`; the historical pointer (`LOG.md:2468`) and original amendments=5
  receipt are retained by design (SCORECARD.md:2829: "retain the historical freeze receipts as
  records"). Both demands (refresh receipt, correct pointer) met without rewriting history.
- **R53.9 / R55.6** — all six / all seven named files tracked at C0, each introduced by the
  cited commit (`receipts/07`). Evidence excerpts are incidental single lines — weak evidence,
  real resolution.

Ancestry/A2 audit of **all 37** fixed routed rows: 0 violations (`receipts/03`); the 8 post-base
fix commits all name their ids.

## 3. Findings (minor, routed to the L1)

### F1 — 7 historical open ledger rows are not named in the newest Planned paragraph; the counter is structurally blind to this

```
newest Planned: round 59 at SCORECARD line 2823, 15 nonblank lines
open rows in ledger: 20; named in newest Planned paragraph: 13
MISSING: ['R45.1','R45.4','R46.2','R47.5','R48.4','R49.3','R49.5']
```
(`receipts/02-planned-open-ids.txt` — replication of `planned_ids()` extended to whole-token
matching of every ledger-open id.)

They appear only collectively: *"R50.4: … the historical seven open ledger items are not claimed
resolved."* The frozen counter cannot flag this, ever: (a) `judge()` runs only over the 51
frozen-set defects — the 49 old rows get only the old49 byte-equality arm; (b) inside
`planned_ids()` the id pattern is `PLANNED_ID = re.compile(r'\bR5[0-6]\.\d+\b')`, which cannot
match a pre-50 id, so `open_unplanned` can structurally never fire for a historical open row.
The A5 docstring sentence ("open: the item id is named in the newest Planned paragraph")
overstates what the code checks.

**Smallest safe correction:** do not touch the frozen instrument or the old49 rows
(byte-equality pins them). Name the seven ids explicitly in the next Planned paragraph; a
successor counter may widen `PLANNED_ID` and extend the agree arm to old open rows.

### F2 — two installed fixed rows carry stale pre-fix `assessment` fields that contradict their own status/evidence at C0

- `corpus/routed-defects.json` R51.5 row: *"next canonical round report omits the cross-domain
  finding … do not file the promised report item"* — while the same row cites `status=fixed`,
  commit `38e4e3aff7cf`, and `evidence[0]` quoting `round-58.md:88`, i.e. the filing that now
  exists. The row asserts both that the filing exists and that it does not.
- R53.5 row: *"Later-round freeze hygiene does not repair those records"* — while the same row
  cites commit `764f87bc8a9f`, whose LOG correction supersedes the stale pointer and whose
  refreshed receipt prints `amendments=7` + `FREEZE_INTEGRITY: OK`; SCORECARD.md:2829 itself
  records "R53.5: resolved this round … at `764f87bc`".

**Smallest safe correction:** refresh the two `assessment` fields (both are new rows, not
constrained by the old49 byte-equality arm): record the at-base judgment and append
"superseded: resolved by `<commit>`". No counter change needed.

## 4. Other checks

- **Panel** — 4/5 disagreements (allowed 5): R54.5, R54.6, R56.2, R56.3 (ledger
  `status_at_base=open`, panel verdict `fixed`). Counter prints `panel=4/5`. No action.
- **R51.3 (bonus)** — round-21 coldread `ledger.json` carries the named correction
  (*"wrong_expectations 0 was written from code (round-51 refresh.py:227)"*, routed_by round-51
  spotcheck defect 3) and `.ufo/evidence/round-52/coldread/refresh.py:216` now writes
  `'wrong_expectations': len(reader['findings'])`. Fix real.
- **Decisive wave-1 C2 forgery** — not adjudicated by this seat; per the L1, C2 stays not
  admitted regardless of its numerical verdict. Frozen targets untouched by this seat.

## 5. Verdict

`gap-minor` — the frozen C1 counter passes at C0 (`total=0`, agree=51/51) and the five weakest
fixed rows all resolve semantically; two minor gaps (F1 plan-of-record/counter regex scope, F2
stale row assessments) are routed to the L1 adjudication.

Honesty: every claim above carries its command and output in `T58W2CritLedger-receipts/`;
statements so marked are INFERENCE. Tools installed: none (pacman untouched). Scratch
`/fast/scratch/hyaku/tameshi-r58/T58W2CritLedger` deleted before yield.
