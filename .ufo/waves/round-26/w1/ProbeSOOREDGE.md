# Probe S_OOR_EDGE — off-suite falsifier for kumitate `scripts/cite-check.mjs`

**Verdict: the mutant and the pristine pin ARE DISTINGUISHED by a hermetic, off-suite input.**

## 1. What the defect is

`S_OOR_EDGE` is a pre-registered hole-aimed mutation on the pinned bytes of
`kumitate-shokunin/scripts/cite-check.mjs` at rev
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`.

Edit (from `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`), applied at
pristine line **1312** inside `refFinding()`:

```js
    const bad = ref.start > n || ref.end > n;          // pristine
    const bad = ref.start > n + 1 || ref.end > n + 1;  // mutant
```

`n` is `countLines(target)` (pinned line 336-340: `text.split('\n').length`, minus
one when the text ends in a newline). The mutant therefore accepts a citation of
line **n+1** of an n-line file as in-range; the pristine pin flags it `LINE_OOR`
(severity `error`, pinned line 222).

The pre-registration predicted `SURVIVED` because the only `LINE_OOR` fixture in
the hermetic suite cites `:999` of a 20-line file (`cite-check.mjs:1883-1886`),
which is far past n+1, so the one-line widening is invisible to the suite.

## 2. Materialization of the pin and the mutant

Both files were built in the `/tmp` scratch dir `/tmp/soor/w1`, never in the
lane tree.

```
$ cd /tmp/soor/w1
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > pristine.mjs
$ sha256sum pristine.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  pristine.mjs
$ wc -l pristine.mjs
2537 pristine.mjs
```

The sha256 matches the frozen pin recorded in
`.ufo/evidence/round-26/cite-check/predictions.json`
(`"pin_sha256": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"`)
and the spec header line 2, and the line count matches the spec's `2537 lines`.

The mutant was produced by a single exact-string replacement, asserted to occur
exactly once:

```python
src = open('pristine.mjs').read()
old = "    const bad = ref.start > n || ref.end > n;"
new = "    const bad = ref.start > n + 1 || ref.end > n + 1;"
assert src.count(old) == 1
open('mutant.mjs','w').write(src.replace(old, new))
```

Diff between the two materialized files (the only byte difference):

```
$ diff pristine.mjs mutant.mjs
1312c1312
<     const bad = ref.start > n || ref.end > n;
---
>     const bad = ref.start > n + 1 || ref.end > n + 1;
```

## 3. The probe

The probe drives the **public CLI** (`--src/--self/--fleet`), not `--selftest`,
over a synthetic tree. It cites exactly line n+1 of an n-line file: a 20-line
`src/scripts/real.mjs` (so `countLines` = 20) cited as `scripts/real.mjs:21`.

`/tmp/soor/w1/probe.sh`:

```bash
#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Off-suite falsifier for mutation S_OOR_EDGE
#   target : kumitate-shokunin/scripts/cite-check.mjs
#   rev    : 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a
#   edit   : const bad = ref.start > n || ref.end > n;
#         -> const bad = ref.start > n + 1 || ref.end > n + 1;
#
# The defect only widens the accepted line range by exactly ONE line. The
# hermetic --selftest suite never cites line n+1 of an n-line file, so the
# mutant passes all 62 suite cases. This probe instead drives the PUBLIC CLI
# (not --selftest) over a synthetic tree and cites exactly line n+1.
#
# Hermetic: a fresh mktemp tree, `env -i`, no network, no host reads outside
# the temp tree (HOME is redirected into the temp tree).
# ---------------------------------------------------------------------------
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PRISTINE="$HERE/pristine.mjs"
MUTANT="$HERE/mutant.mjs"
NODE="$(command -v node)"

ROOT="$(mktemp -d "${TMPDIR:-/tmp}/soor-edge-probe.XXXXXX")"
trap 'rm -rf "$ROOT"' EXIT
SRC="$ROOT/src"; SELF="$ROOT/self"; FLEET="$ROOT/fleet"
mkdir -p "$SRC/scripts" "$SELF" "$FLEET"

# 20-line source file. countLines() returns exactly 20 for this text.
: > "$SRC/scripts/real.mjs"
for i in $(seq 1 20); do printf '// line %s\n' "$i" >> "$SRC/scripts/real.mjs"; done

# The doc cites exactly line n+1 = 21 of that 20-line file.
printf '# probe doc\n\nEdge citation: `scripts/real.mjs:21`.\n' > "$SELF/SKILL.md"

run() {
  local label="$1" tool="$2"
  echo "===== $label ====="
  env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$tool" \
      --src "$SRC" --self "$SELF" --fleet "$FLEET" 2>&1
  echo "----- exit status: $? -----"
}

run "PRISTINE" "$PRISTINE"
run "MUTANT" "$MUTANT"
```

### Observed output — pristine

```
$ cd /tmp/soor/w1 && bash probe.sh
===== PRISTINE =====
kumitate cite-check — kumitate-cite-check-v1
src=/tmp/soor-edge-probe.BUIcxA/src (index 1 files)
self=/tmp/soor-edge-probe.BUIcxA/self  fleet=/tmp/soor-edge-probe.BUIcxA/fleet
mode:

SKILL.md
  SKILL.md:3  ERROR LINE_OOR          [source/src] scripts/real.mjs:21 — scripts/real.mjs:21 out of range — scripts/real.mjs has 20 lines

totals
  filesScanned=1 docs=1 tokens=2 refs=1 symbols=0 findings=2
  orphanRefs=0 altOwnerRefs=0 declarations=0
  bySeverity={"error":1,"note":1}
  byClass={"source":2}
  byKind={"LINE_OOR":1,"OK":1}
  byRung={"src":2}
  pins=0 ok=0 mismatch=0 untyped=0 revUnknown=0 unchecked=0
  indexFiles=1 selfIndexFiles=1 fleetIndexFiles=0
VERDICT: FAIL
CITE_CHECK: DRIFT (files=1 tokens=2 errors=1 warnings=0)
----- exit status: 1 -----
```

### Observed output — mutant

```
===== MUTANT =====
kumitate cite-check — kumitate-cite-check-v1
src=/tmp/soor-edge-probe.BUIcxA/src (index 1 files)
self=/tmp/soor-edge-probe.BUIcxA/self  fleet=/tmp/soor-edge-probe.BUIcxA/fleet
mode:

totals
  filesScanned=1 docs=1 tokens=2 refs=1 symbols=0 findings=2
  orphanRefs=0 altOwnerRefs=0 declarations=0
  bySeverity={"note":2}
  byClass={"source":2}
  byKind={"OK":2}
  byRung={"src":2}
  pins=0 ok=0 mismatch=0 untyped=0 revUnknown=0 unchecked=0
  indexFiles=1 selfIndexFiles=1 fleetIndexFiles=0
VERDICT: PASS
CITE_CHECK: CLEAN (files=1 tokens=2 errors=0 warnings=0)
----- exit status: 0 -----
```

The two runs differ in three independent observable ways: the `LINE_OOR` error
line (present only in pristine), `VERDICT: FAIL` vs `VERDICT: PASS`, and the
process **exit status 1 vs 0**. The exit status alone is a sufficient oracle.

## 4. The mutant really is a suite survivor (the probe is off-suite, not a re-run of the suite)

Both pinned and mutated binaries still pass the full hermetic suite, so the
suite genuinely cannot see this defect and the probe is the only thing that can:

```
$ env -i PATH=/usr/bin:/bin HOME=/tmp node ./pristine.mjs --selftest | tail -3
62/62 cases passed (hermetic)
VERDICT: PASS
$ env -i PATH=/usr/bin:/bin HOME=/tmp node ./mutant.mjs --selftest | tail -3
62/62 cases passed (hermetic)
VERDICT: PASS
```

(`--selftest` was run in the `/tmp` scratch dir, never inside
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.)

## 5. Boundary sanity: the difference is exactly the n+1 line

Sweeping the cited line number over the same tree shows the mutant's accepted
range is widened by exactly one line and nothing more:

```
ref :19  pristine[VERDICT: PASS CITE_CHECK: CLEAN ...] mutant[VERDICT: PASS CITE_CHECK: CLEAN ...]
ref :20  pristine[VERDICT: PASS CITE_CHECK: CLEAN ...] mutant[VERDICT: PASS CITE_CHECK: CLEAN ...]
ref :21  pristine[VERDICT: FAIL CITE_CHECK: DRIFT ...] mutant[VERDICT: PASS CITE_CHECK: CLEAN ...]
ref :22  pristine[VERDICT: FAIL CITE_CHECK: DRIFT ...] mutant[VERDICT: FAIL CITE_CHECK: DRIFT ...]
```

`:21` is the unique discriminating single-line input: `:20` is in range for both,
`:22` is out of range for both.

Other ref spellings that hit the same one-line window also separate:

```
doc[`scripts/real.mjs:20-21`]   pristine: DRIFT   mutant: CLEAN
doc[`scripts/real.mjs:19-21`]   pristine: DRIFT   mutant: CLEAN
doc[`scripts/real.mjs L21`]     pristine: DRIFT   mutant: CLEAN
doc[`scripts/real.mjs:21-25`]   pristine: DRIFT   mutant: DRIFT   (end=25 > n+1, both flag it)
```

The `L21` and `:20-21` forms are a robustness check on the ref parser: they
confirm the separation does not depend on the exact `:N` spelling, only on the
numeric end of the range.

## 6. Argument that no input could distinguish them — refuted

There is no such argument. The pre-registration's `SURVIVED` prediction was
about the *suite* (no fixture cites n+1), not about the *program*. The line-range
predicate is a total function of `(ref.start, ref.end, n)`, and the mutant
changes it on exactly the inputs where `ref.start == n+1` (or `ref.end == n+1`,
or a range spanning n+1 while no endpoint exceeds n+1). The probe exhibits such
an input and the two programs return different verdicts and different exit
codes on it. Therefore the two binaries are **not** behaviourally equivalent, and
no argument of equivalence can stand.

## 7. Smallest safe correction implied (for the lane's integrator; NOT applied here)

The mutant's own line is the defect. The correct predicate is the pristine one,
`ref.start > n || ref.end > n` (pristine line 1312). The lesson the fixture
set lacks is a fixture citing exactly `n+1` of an n-line file — e.g. a 20-line
`scripts/real.mjs` cited as `:21` — asserted `LINE_OOR` error, which would have
killed this mutant. No production file was edited by this seat.

## 8. Environment, tooling, and bounds

- Node: `v24.21.0` (`/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node`).
- **No packages were installed or upgraded by this seat**, so there is no
  install record to report. The probe needed only `node`, `mktemp`, `printf`
  and `git` (all pre-existing).
- Everything ran under `/tmp/soor/w1` (scratch) and `/tmp/soor-*` (probe temp
  trees). Nothing was executed inside
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Read-only git was used against the sibling lane
  (`git -C .../kumitate-shokunin show <rev>:scripts/cite-check.mjs`); no git
  write command was run, and **no `jj` command was run anywhere**.
- Files written by this seat: this report only. The pristine/mutant/probe
  artifacts live in `/tmp` scratch and are not lane files.

## 9. Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-26/w1/ProbeSOOREDGE.md`
  (this report) — the only lane file touched.

PROBE S_OOR_EDGE: DISTINGUISHED
