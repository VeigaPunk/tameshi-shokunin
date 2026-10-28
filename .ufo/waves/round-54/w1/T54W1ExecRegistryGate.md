# T54W1ExecRegistryGate — registry rows still return their outcomes (operability)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Content commit C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`;
base `d33053f7552db4bd290c99a36979760f544c41ad`. Lane tip observed during the wave: `99c3bc88d704566197783f66b211ee0a830e0330`
(L1 C1 fix pass). `git diff 59c3810..99c3bc8 -- tools/registry.json` is empty: the registry under test is C0's.

Verdict: **the seven `scratch_root` cells changed no row's registered outcome and the registry still validates.** All runs
exit 0 as claimed below. Two residuals are reported at the end; neither falsifies the frozen C1/C2 claims and I fixed nothing.

Receipts: `.ufo/waves/round-54/w1/T54W1ExecRegistryGate-receipts/` (transcripts `01`–`14`, fixtures `registry-mutated.json`,
`full-registry-c0.json`, `full-registry-base.json`).

## 1. The two commands the seat names

`01-registry-check-selftest.txt`

```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py --selftest
...
SELFTEST_CASE live-root-warning PASS (exit=0)
SELFTEST: PASS (51 cases)
EXIT=0
```

## 2. Seven rows, one at a time, at C0 (`02-seven-rows-at-c0.txt`)

| row | `ROW …` line | exit |
|---|---|---|
| registry-check-selftest | `ROW registry-check-selftest expect=0 got=0 held` | 0 |
| repeat-control-selftest | `ROW repeat-control-selftest expect=0 got=0 held` | 0 |
| bash-witness-selftest | `ROW bash-witness-selftest expect=0 got=0 held` | 0 |
| pin-disposition-selftest | `ROW pin-disposition-selftest expect=0 got=0 held` | 0 |
| evidence-disposition-selftest | `ROW evidence-disposition-selftest expect=0 got=0 held` | 0 |
| context-capture-selftest | `ROW context-capture-selftest expect=0 got=0 held` | 0 |
| env-diff-selftest | `ROW env-diff-selftest expect=0 got=0 held` | 0 |

Each run printed `REGISTRY_CHECK: held=1/1 superseded=0`. Command form (one invocation per row):

```
python3 tools/registry-check.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 59c38109bf119d0e9d4f878644a82babc937bc1e --only <row>
```

The same seven at base (`03-seven-rows-at-base.txt`) are `got=0 held`, exit 0, and at the lane tip `99c3bc8`
(`14-seven-rows-at-tip.txt`) again 7× `held`, 7× exit 0.

Whole registry: `--rev d33053f7552d --json` → `rev_resolved d33053f… exit 0 held 49/49 superseded 7`
(`full-registry-base.json`); `--rev 59c38109… --json` → `rev_resolved 59c38109… exit 0 held 49/49 superseded 7`
(`full-registry-c0.json`). `13-outcome-parity-base-vs-c0.txt` compares the two reports row by row:

```
same row-name set: True | rows 56
rows whose (held, got) changed: none
```

So the cells changed nothing anywhere in the registry, not only in the seven.

## 3. What the cells are — structurally only an addition (`07-structural-diff.txt`)

Both registries recursively compared after stripping `scratch_root`:

```
base rows 56 C0 rows 56
top-level keys base: ['rows', 'schema'] C0: ['rows', 'schema']
rows equal after stripping scratch_root: True
cells added at C0: ['repeat-control-selftest', 'bash-witness-selftest', 'pin-disposition-selftest',
                   'evidence-disposition-selftest', 'context-capture-selftest', 'registry-check-selftest',
                   'env-diff-selftest']
cells present at base: []
expect blocks changed: []   argv changed: []   timeout_s changed: []   source changed: []
```

Schema string unchanged (`tameshi-entry-registry-v1` at both revs), row count unchanged (56), superseded partition unchanged.

## 4. The field is inert to the runner — mutation experiment (`04-mutation-run.txt`, fixture `registry-mutated.json`)

`registry-mutated.json` is the C0 registry with three mutations (`diff` in the receipt): `repeat-control-selftest`
`scratch_root` → `"TOTALLY WRONG CLAIM"`, `registry-check-selftest` cell deleted, `env-diff-selftest` cell → `12345`.

```
$ python3 tools/registry-check.py --root … --rev 59c38109… \
      --registry …/T54W1ExecRegistryGate-receipts/registry-mutated.json --only repeat-control-selftest
ROW repeat-control-selftest expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
EXIT=0
$ … --only env-diff-selftest
ROW env-diff-selftest expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
EXIT=0
```

`scratch_root` is not read by `run_row()`; the only `scratch_root` hits in `tools/registry-check.py` are the unrelated
`strict_scratch_root()` helper (`tools/registry-check.py:757-768`, `:780`, `:931`), which reads `TMPDIR` from the
environment, not the row.

## 5. The registry still validates — no schema violation (`05-schema-validation.txt`)

Validator: `registry_errors()` in the tool that owns the schema (`tools/registry-check.py:180`).

```
C0  sha256 ef79ab8e91986565d728f998c0468a5eb32e9ec30ae7527d6bda39e9cd4287c4
base sha256 d65a5c42b4c1e234edb5b21829954af2603925d9eb93ac9d3472f28ad360427b
WT  sha256 ef79ab8e… | identical to C0: True
registry_errors(C0)   = []
registry_errors(base) = []
rows carrying scratch_root at C0: 7
rows carrying scratch_root at base: 0
duplicate JSON keys at C0: none
```

Beyond the schema, `06-source-anchor-sweep.txt` resolves every row's `source` `<file>@<rev>:<line>` at its cited rev:
`rows=56 unresolvable=0`. The seven cited lines were opened and each names its tool (e.g. `env-diff-selftest →
SKILL.md@370f2df:1975 | | tools/env-diff.py | probe | python3 tools/env-diff.py --contract …`).

## 6. The cell set is exactly the helper's callers (`09-tool-to-row-map.txt`)

`grep -l strict_scratch_root tools/*.py` returns exactly seven files — `bash-witness-study.py`, `context-capture.py`,
`env-diff.py`, `evidence-disposition.py`, `pin-disposition.py`, `registry-check.py`, `repeat-control.py` — and the
`argv` tool of each of the seven cell-bearing rows is one of them, one to one. No row whose tool lacks the helper
carries a cell; no helper caller's row lacks one.

## 7. TMPDIR arms, from the registry's side (`08-tmpdir-arms.txt`)

* empty arm, `TMPDIR=` : all seven rows `held`, exit 0 (the row inherits the empty value; the declared-unset reading
  is the contract's, `corpus/knowledge/scratch-root-contract.md`).
* unusable arm, `TMPDIR=/nonexistent/seat-root` into `--rev`:

```
REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root:
  TMPDIR is not a usable directory: '/nonexistent/seat-root' (could-not-evaluate))
EXIT=2
```

one line, names the value, no traceback — the class registry-check itself claims.

## 8. Residuals (reported, not fixed; neither is a C2/C1 falsifier)

**R1 — the owned schema does not know the new key.** `registry_errors()` validates
name/kind/argv/expect/timeout_s/source/status/tags/external/discriminating and ignores `scratch_root` entirely; the
schema doc block in `tools/registry-check.py:15-29` lists no `scratch_root`, and the schema string was not bumped. The
receipt shows a wrong-typed (`12345`), a deleted and a wrong-content cell all still give `registry_errors(...) = []` and
a `held` row. The claim "the seven rows carry the `scratch_root` cell" is therefore enforced only by this round's
counter: `c2/measure.py`'s docs arm requires each cell to contain `TMPDIR`, `empty`, `could-not-evaluate`
(`.ufo/evidence/round-54/c2/measure.py:138-152` at C0). Consequence: a later round that re-emits `tools/registry.json`
from SKILL can drop the cells and `registry-check` will still print `held=49/49`. Candidate future fix: validate the
cell when present (string containing the three tokens) and document it in the schema block — schema `v2` or a declared
optional cell.

**R2 — the registry has no could-not-evaluate row state.** C0 makes the seven tools exit 2 on a set-but-unusable
`TMPDIR`, but `run_row()` only knows exit-equals-expect, so the registry renders that as a verdict. Live mode on a
clone of the tip (`11-row-state-unusable-tmpdir.txt`):

```
$ TMPDIR=/nonexistent/seat-root python3 tools/registry-check.py --root $C --only env-diff-selftest
ROW env-diff-selftest expect=0 got=2 differs
REGISTRY_CHECK: held=0/1 superseded=0
EXIT=1
$ … --only registry-check-selftest
ROW registry-check-selftest expect=0 got=2 differs
EXIT=1
```

The same probe against the pre-C0 tree `d33053f` (`12-row-state-base-d33053f.txt`) gives
`repeat-control-selftest … got=2 differs`, `context-capture-selftest … got=2 differs`,
`pin-disposition-selftest … got=1 differs`, `env-diff-selftest … got=1 differs`. So the conflation is pre-existing and
C0 changes the code (`1 → 2` for the four tools) without changing the verdict (`differs` before and after). C0's exit
class is invisible at the registry layer: a harness reading `REGISTRY_CHECK: held=1/1` cannot tell an environment fact
from a regression on these rows. `--rev` mode masks it only because registry-check aborts first with exit 2.
Scope of R2: exactly the seven rows. `10-scratch-allocators-outside-helper.txt` lists the other tools that allocate
scratch with plain `tempfile` (no `strict_scratch_root()`), and three rows probed from that set
(`receipt-measure-selftest`, `witness-metadata-selftest`, `trace-inputs-selftest`) still hold at `TMPDIR=/nonexistent/seat-root`
(`11-row-state-unusable-tmpdir.txt`, `got=0 held`), so the seven-cell boundary is where the contract stops, not a
regression elsewhere.

## 9. Discipline

* No lane file edited; no mutating git/jj run anywhere; fixtures only under the seat scratch
  `/fast/scratch/hyaku/tameshi-r54/T54W1ExecRegistryGate` (`lane-c0` = `git clone --shared`; `base-d33053f` = `git archive`
  extract, no checkout). Scratch removed at exit.
* Tooling: none installed, none upgraded.
* Census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  → exit 0 at wave start and at report time (report lines W04 duplicates / W01 mined only).
