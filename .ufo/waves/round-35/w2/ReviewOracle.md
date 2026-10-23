# ReviewOracle — audit of the C1 counter's behavior oracle (round 35 w2)

Seat: `L1tameshi35.ReviewOracle` (leaf reviewer, godspeed). Dispatch tip: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`
(verified: `git show 7da6e076:...` in a detached clone at `/fast/scratch/hyaku/tameshi-r35-seats/ReviewOracle/lane`).

Pinned bytes verified at REV (sha256):

| artifact | at 7da6e076 | frozen pin | match |
|---|---|---|---|
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | contract:runner_sha256 | ✓ |
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` | contract.json:11 | ✓ |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` | task/contract A4 pins_new | ✓ |

All line numbers below are committed bytes at REV. No pinned artifact was edited; scratch
(specimens, drives, counter stdout) is under `/fast/scratch/hyaku/tameshi-r35-seats/ReviewOracle/`.
No tool installs (nothing needed); no pacman (bounds).

---

## 1. The enumeration I was asked for

`tally_block` (c1-measure.py:132) cuts `run_regression` (mutate-and-run.sh:1344-1471) at the first
`local nlegs=` and the last code-view brace. On the pinned bytes the extracted block is exactly
runner:1432-1470: first line `  local nlegs=9 npass=0 nfail=0 nsetup=0 st`, last line `  exit 0`,
39 lines. `leg_names` finds all nine `st_*=$?` assignments (runner:1390-1430). The driver
(c1-measure.py:163 `run_block`) runs the block VERBATIM per config with
`local st_<leg>=${N}` and `local root=<root> auto=<a> KEEP=<k>` preset, one bash process per
config, `set -u -o pipefail`, comparing (exit, FULL stdout) per vector.

### Printer statements in `run_regression`, and whether the oracle models them

IN-BLOCK (executed verbatim by the driver; labels, count fields, order compared byte-exact under
all four configs) — all modeled:

| runner line | statement |
|---|---|
| 1442-1443 | `REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)` |
| 1444 | `REGRESSION_WORKDIR: %s (kept)` |
| 1448-1449 | `REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)` |
| 1450 | `REGRESSION_WORKDIR: %s (kept)` |
| 1457-1458 | `REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)` |
| 1459 | `REGRESSION_WORKDIR: %s (kept)` |
| 1462-1463 | `REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)` |
| 1465 | `REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)` |
| 1466 | **`rm -rf "$root"`** — the rm decision itself |

The rm decision is genuinely exercised: under `(auto=1, KEEP=0)` the all-pass vector prints the
`(removed on PASS; --keep retains)` line and deletes the root (drive: after
`run_block(block, names, [[0]*9, [0]*9], (None,'1','0'), tmp)` the shared root
`/tmp/tameshi-r4-2-regression.je9yhkqg` had `isdir=False`); the other three configs print `(kept)`.

HEAD — **not executed by the oracle at all** (the block starts at 1432):

| runner line | statement |
|---|---|
| 1370 | `REGRESSION_TOOL: %s sha256=%s` |
| 1371 | `REGRESSION_DATE: %s` |
| 1372-1373 | `REGRESSION_BAND: ...` |
| 1374-1384 | `REGRESSION_EXPECT: recorded kill-rates — ...` (computed from the `TABLE_*` strings) |
| 1172-1328 | every printer of `regression_case`/`regression_case_git`, called nine times at 1386-1429 (`REGRESSION_PIN` 1230/1233, `REGRESSION_SWEEP` 1252, `REGRESSION_DEFECT` 1285/1288/1299, `REGRESSION_TABLE` 1320, per-case `REGRESSION_WORKDIR` 1322, `REGRESSION_CASE` PASS/FAIL/SETUP 1324/1328 and the SETUP refusals 1172-1265) |
| 1350-1354, 1359, 1363, 1366, 1367 | head `die_setup` refusals (stderr, exit 2) |

So: **every in-block statement is modeled (the oracle runs the extracted bytes, so labels, count
fields and order cannot drift), and every head statement is unmodeled by construction.** The
findings below are about what the modeled region still fails to see, and about the apparatus pin.

---

## 2. Findings, ranked

### F1 — CRITICAL: the frozen counter cannot emit `C1_R35_PASS=true` at the measurement revision

The A4 amendment bumped the counter bytes (`78bb43eb` → `515b0b1b`) and the tool
(`da23d3a2` → `ef98fc53`), but the rewritten counter's internal tool pin still holds the OLD tool:
`c1-measure.py:46` — `TOOL_SHA256 = 'da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f'`
(comment: "# v3 at the round-35 freeze" — now false). The tool at REV is `ef98fc53…`. The deciding
arithmetic (c1-measure.py:374, :445) requires `tool_sha == TOOL_SHA256` in default mode; the
control receipt bypasses it (`a.tool is not None` short-circuits — which is why controls passed).

Discriminating command (the contract's counting command, sans `--sealed`, at REV):

```
python3 <lane>/.ufo/evidence/round-35/c1/c1-measure.py --lane <lane> --rev 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b --work <empty>
```

Measured output (`.ufo`… no — scratch `ReviewOracle/c1-deciding.stdout`, wrapper `C1_EXIT=1`):

```
COPY kill  root-keyed-auto-mask  ... div=(1,0),(1,1) rc=1 checks=runtime pass=True
... pub_kill=5/5 pub_accept=3/3 pub_slots=8 pub_distinct=8 ho_kill=0/0 ...
C1_R35: mode=deciding tool_present=1 tool_sha=ef98fc5367cdb12c tool_sha_ok=0 runner_sha_ok=1
        ... C1_R35_PASS=false      (exit 1)
```

The panel itself is fully green (5/5, 3/3, distinct 8/8 — including both A4 root-keyed kills, so
the root-VALUE class is demonstrably closed), yet `tool_sha_ok=0` forces `PASS=false`. The
contract's own falsifier 6 ("the tool's sha at the measured revision differs from tool_sha256
above", contract.json:40, with `above` = contract.json:11 = `ef98fc53…`) does NOT trigger — the
counter enforces a different pin than the contract. Since `kill_rule` (contract.json:33) forbids
post-data changes, this must be amended pre-data (re-pin `TOOL_SHA256` to `ef98fc53…`, producing
new counter bytes and a new pins_new record) or the deciding run dies deterministically.
A4's own `pins_new` block (contract.json:106-112) is internally inconsistent: new counter bytes
that internally pin the old tool.

### F2 — CRITICAL: A4 residue — the oracle reproduces the real auto root's PATH, not its STATE

A4's surface (contract.json:26, item 4): "the auto triples run with the runner's REAL auto root
(/tmp/tameshi-r4-2-regression.XXXXXX), so a copy keyed on the real root value is observable".
Value — yes. State — no. At block time the real root is populated: the head creates `root/specs`
with nine embedded specs (runner:1365-1367) and nine case workdirs (runner:1171 `mkdir -p "$cwd"`
runs before every SETUP/materialization outcome). Proven by running the pinned runner:

```
bash <lane>/tools/mutate-and-run.sh --regression        # exit 2 (SETUP legs here; irrelevant)
  REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.dB9aju (kept)
  ls <root>  ->  bash-checklist-run bash-mado-verify bash-surface-census bash-tsukuroi-census
                 js-cite-check js-claims-check js-kimi-census js-round-gate js-sources-check specs
                 (specs/ holds 9 files)
```

The counter's auto root is an EMPTY `tempfile.mkdtemp(prefix='tameshi-r4-2-regression.', dir='/tmp')`
(c1-measure.py:58-69; the tool likewise, tally-audit-v3.py:365) whose docstring even admits "the
compared stdout carries the value, not the directory's contents" (tool, auto_root docstring).

Specimen S1 — one inserted line before runner:1441, gating on the real root's STATE
(`364853bac0fe45b17e98e19ca3c9ea1529823862dd1fec2d3fb651f3fc46d61a`):

```bash
  if [[ -d $root/specs ]]; then nfail=0; npass=$((nlegs - nsetup)); fi
```

Results, all measured:

- Counter ground truth: `diverged_configs = []` over all 267 vectors × 4 configs — BLIND.
- Tool v3: `rc=0`, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`,
  `CHECK runtime PASS vectors=30316 mismatched=0` — ACCEPTS.
- Real runner state (same block bytes, root = a genuine runner-produced root
  `/tmp/tameshi-r4-2-regression.3lRrfy`, `auto=1 KEEP=1`, vector one failing leg):

```
pristine rc=1 :: REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
S1       rc=0 :: REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
DIVERGES : True
```

This is the exact shape of the routed RevengerRootShape CRITICAL (failing leg masked into PASS
under the runner's default config, apparatus green), one predicate deeper: keyed on the root's
contents instead of its name. The A4 closure covers root value; root state is still invisible to
both the counter's ground truth and the tool. (By the frozen kill definition the specimen scores
"accept-valid" — the claim as lettered survives; what breaks is the soundness of the frozen
definition's equivalence to real runner behavior, which is what A4 was supposed to restore.)

The same asymmetry exists on the explicit side: the real runner `mkdir -p`s the workdir
(runner:1363) while the driver's explicit roots `tally-audit`/`tally-audit-explicit` are
nonexistent paths; a gate composed of existence + `auto=0` is real-reachable and oracle-invisible.

### F3 — BOUND: no `(auto=0, absolute root)` config exists; the apparatus comment claims otherwise

c1-measure.py:49 (and tally-audit-v3.py:348): "the explicit triples keep representative
caller-supplied --workdir values, relative and absolute." False in both files:
CONFIGS (c1-measure.py:52-53) carries `('tally-audit','0','1')` and `('tally-audit-explicit','0','0')`
— both relative. The real runner accepts absolute workdirs (`--workdir /tmp/x` → auto=0, absolute),
a reachable real state no config simulates. Wave-1 RevengerRootShape's BOUND ("absolute-vs-relative
gates would be caught by the (1,0)/(1,1) configs") fails for gates that compose `auto=0` with
absolute-ness.

Specimen S2 (`a02c611b0baceeb9b53f270339f04ff736e0ece804302fc177eeb631dc7128ef`), one line before
runner:1441:

```bash
  if [[ $auto -eq 0 && "$root" == /* ]]; then nfail=0; npass=$((nlegs - nsetup)); fi
```

- Counter: `diverged_configs = []` — BLIND ((0,·) roots are relative; (1,·) has auto=1).
- Tool v3: `rc=0`, `TALLY_AUDIT: PASS`, `runtime mismatched=0` — ACCEPTS.
- Real-state drive, `auto=0 KEEP=0`, one failing leg: absolute root `/tmp/r35-abs-probe` →
  pristine rc=1 vs S2 rc=0 (DIVERGES); relative root `r35-rel-probe` → both rc=1 (identical) —
  the gate is precisely keyed on the unswept dimension.

### F4 — BOUND: head printers are unmodeled, so real stdout divergence outside the block is invisible

By the frozen definition (kill = block divergence under a triple) these are not kill specimens,
and F1's class aside, the counter is behaving as specified. But the practical guarantee "accepted
⇒ real runs identical" does not hold for any head printer.

Specimen S3 (`7f8f925581d0fe1e0085bdb6c11ec3a14a4ea66221bc604fbfa97b08fb12f7db`): the BAND line's
format text `flips<=%s` → `flips>%s` (runner:1372-1373 fragment, unique).

- Counter: `diverged_configs = []` (block untouched).
- Tool v3: `rc=0`, `TALLY_AUDIT: PASS` — ACCEPTS.
- Real runs (both `--regression`, exit 2 in this environment):

```
pristine: REGRESSION_BAND: ... fixture-mode default killed-delta<=1 flips<=1
S3:       REGRESSION_BAND: ... fixture-mode default killed-delta<=1 flips>1
```

The same blindness covers `REGRESSION_EXPECT` (recorded kill-rates), `REGRESSION_TOOL/DATE`, and
every per-leg `REGRESSION_TABLE`/`REGRESSION_DEFECT`/`REGRESSION_CASE` line (runner:1172-1328) —
a runner that lies in its table lines or misreports its recorded expectations is accepted as
"behaviorally identical" by both ground truth and tool. Scope limit, not a claim violation.

### F5 — BOUND: kill ground truth counts reality-inert (phantom) kills

The vector space sweeps statuses 0..255 per position, but real leg statuses are only {0,1,2}:
`regression_case`'s literal returns in the pinned runner are exactly {0,1,2} (regex scan), and
`st_<leg>=$?` captures nothing else. The case arms (runner:1435-1437) are `0)`/`1)`/`*`.

Specimen S5 (`12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b`): one extra arm

```bash
      4) npass=$((npass + 1)) ;;
```

- Counter: diverges under ALL FOUR configs (at every status-4 vector) → a valid kill by the
  frozen definition.
- Tool v3: `rc=1`, `CHECK runtime FAIL vectors=30316 mismatched=3348` (first: cfg(1,0) statuses
  `4 0 … 0`: got 0 PASS, want 2 SETUP), failing check exactly `runtime` — i.e. exactly the kill
  rule's required shape. Such a copy would be counted in `ho_kill=k/k`.
- Reality: status 4 is unreachable (regression_case returns 0/1/2), so the copy can never change
  a real run. A sealed set could satisfy its kill quota with reality-inert specimens and the
  counter could not tell. (Measurement-integrity bound on what `ho_kill=k/k` MEANS; fails toward
  inflated kills, not false-accepts.)

Positive control: the driver calls each vector in a command-substitution subshell
(`out=$(tally …)`), so shell-variable state does NOT persist across vectors — a variable-carrying
phantom (S4b, `d7e50ee47c5c59fef32e6eaaa9387845426e24c67d45e11dbe87cd8a4addd1c`) is correctly
inert in both driver and reality (div=[]; tool accepts). File-state phantoms through the shared
root remain possible (see HYGIENE-1).

### HYGIENE

1. **Shared, mutable, rm-able auto root.** `AUTO_ROOT` is one global directory shared across all
   configs, all vectors, pristine and every copy (c1-measure.py:58-69). Under `(1,0)` the block's
   `rm -rf "$root"` (runner:1466) deletes it after the first all-pass vector; the remaining 266
   vectors of the runner's DEFAULT config execute with the root nonexistent — a state the real
   runner never exhibits — and `auto_root()` silently re-creates an empty one on the next call.
   Copies can also leave state in it that later copies' ground truth runs see.
2. **Dead placeholder.** `FREEZE_REV = '__FREEZE_REV__'` (c1-measure.py:47) is committed
   unfilled and never used (exactly 1 occurrence; the provenance gate reads history instead) —
   the comment "filled at freeze" is misleading.
3. **Stale comments.** c1-measure.py:46 "# v3 at the round-35 freeze" (false post-A4 — this is
   the round-34 ReviewPinChain F1 class recurring inside the amendment itself);
   c1-measure.py:49 / tally-audit-v3.py:348 "relative and absolute" (false — see F3).

---

## 3. What I could NOT break (with proof)

- **In-block printer completeness.** The block (runner:1432-1470) is extracted and executed
  verbatim; all nine in-block printer statements, their count fields (`cases/passed/failed/setup`,
  `cases/passed/cannot-verify`, `cases/counted`, `cases/passed`), their branch order
  (FAIL → SETUP → case-tally → PASS) and the rm decision are compared byte-exact as (exit, FULL
  stdout) under all four `(auto,KEEP)` triples — which are exactly the runner's four real states
  (default, `--keep`, `--workdir`, `--workdir --keep`). I found no in-block statement the oracle
  fails to reproduce; my only in-block-region "holes" (F2/F3) live in the driver's *context*
  (root state), not in any printer.
- **The A4 root-VALUE class stays closed.** In the measured deciding run both panel copies
  `root-keyed-auto-mask` and `root-keyed-auto-zero` diverge under `(1,0),(1,1)` and are killed
  (`rc=1`, check exactly `runtime`); the tool's selftest seeds the same class
  (tally-audit-v3.py:789 'real-root gated mask'). My value-independent S1 shows the surviving
  dimension is state, not value.
- **Head/static extraction is comment-safe.** Block boundaries are computed on the quote-aware
  comment-blanked code view (c1-measure.py:132-160); the pristine block cut lands exactly on
  `local nlegs=…` … `exit 0` with all nine leg names found.
- **Symmetric driver environment.** Pristine and copy run in identical HOME/TMPDIR/cwd/LC_ALL,
  stderr discarded symmetrically (stdout-only comparison is the frozen definition).
- **No false-accept found against the frozen definition itself:** every specimen the counter
  scores divergent is killed by the tool with `failing check exactly runtime` (S5), and every
  block-identical specimen is accepted (S1/S2/S3 — as defined, since they ARE block-identical).
  The claim-as-lettered is not yet falsified by any construction I could build; F1 (pin) and the
  F2/F3 soundness gaps are what stand between the letter and reality.

## 4. Residual risk and verification gaps

- No full GREEN real `--regression` run was executed (the leg suites are heavy and legs SETUP in
  the scratch clone for want of sibling repos). The real-root listing was taken from a SETUP-shape
  run, which is faithful for root contents: `mkdir -p` of `specs/` (1365-1366) and case dirs
  (1171) happens before any pin/materialization refusal. A green run would additionally populate
  the case dirs (targets, sweep logs) — MORE state, so F2's gap only widens.
- I did not audit the tool's own `oracle()` expected-stdout model (tally-audit-v3.py:401+) — out
  of slice; only the counter's ground truth and the tool's verdicts were exercised.
- I did not attack the A5 sealed-provenance gate (other seats' slice).
- The explicit-relative asymmetry (real runner mkdirs the workdir; driver's explicit roots do not
  exist) is reported inside F2 but was not separately specimen-ized; it is the same construction.
- F1 must be resolved pre-data by the L1 (counter re-pin amendment); my remit is the finding only.

## 5. Discriminating commands (all run; scratch under `/fast/scratch/hyaku/tameshi-r35-seats/ReviewOracle/`)

```
# F1: sha divergence + deciding-mode failure (exit 1)
git show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/tally-audit-v3.py | sha256sum   # ef98fc53…
grep -n 'TOOL_SHA256' <lane>/.ufo/evidence/round-35/c1/c1-measure.py                    # line 46: da23d3a2…
python3 <lane>/.ufo/evidence/round-35/c1/c1-measure.py --lane <lane> \
  --rev 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b --work <empty>                          # tool_sha_ok=0, PASS=false, exit 1

# F2/F3: counter blindness (python: import counter; behavior(); diverge())
#   S1 364853ba… div=[] ; tool rc=0 TALLY_AUDIT: PASS ; real-root drive pristine rc=1 vs S1 rc=0
#   S2 a02c611b… div=[] ; tool rc=0 TALLY_AUDIT: PASS ; abs auto=0 drive rc1→rc0, rel identical
# F4: real stdout divergence with apparatus green
bash <lane>/tools/mutate-and-run.sh --regression | grep REGRESSION_BAND   # flips<=1  (exit 2)
bash S3-band-text.sh               --regression | grep REGRESSION_BAND   # flips>1  (exit 2)
# F5: phantom kill counted per the rule
python3 <lane>/tools/tally-audit-v3.py --runner S5-status4-phantom.sh     # rc=1, CHECK runtime FAIL
```

Specimen bytes and drive transcripts: `ReviewOracle/S{1,2,3,4b,5}-*.sh`, `ReviewOracle/c1-deciding.stdout`,
`ReviewOracle/real-auto.stdout`, driver transcripts in the session log.
