# Probe S_STRICT — off-suite falsifier for kumitate `scripts/cite-check.mjs`

**Verdict: the mutant and the pristine pin ARE DISTINGUISHED by a hermetic, off-suite input.**
The discriminating input is a `--strict` run over a doc tree containing **exactly one
warn-level finding** (and no errors).

## 1. What the defect is

`S_STRICT` is a pre-registered hole-aimed mutation on the pinned bytes of
`kumitate-shokunin/scripts/cite-check.mjs` at rev
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`.

Edit (from `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`), applied at
pristine line **1589** inside `runCheck()`:

```js
  const drift = totals.error > 0 || (opts.strict && totals.warn > 0);   // pristine
  const drift = totals.error > 0 || (opts.strict && totals.warn > 1);   // mutant
```

`totals.warn` is the count of warn-severity findings across the whole scan
(pinned line 1584-1587: `if (f.severity === 'error') totals.error++; else if
(f.severity === 'warn') totals.warn++;`). The pristine pin promotes **any**
warn into DRIFT under `--strict`; the mutant requires **two or more** warns. A
tree with exactly one warn therefore drifts in the pristine and passes in the
mutant.

The pre-registration predicted `SURVIVED` because no hermetic fixture ever runs
with `--strict` (the suite's `run()` helper passes only `strict: false`), so
warn promotion is unasserted by the 62-case suite.

## 2. Materialization of the pin and the mutant

Both files were built in the `/tmp` scratch dir `/tmp/sstrict`, never in the lane
tree.

```
$ mkdir -p /tmp/sstrict
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/sstrict/pristine.mjs
$ sha256sum /tmp/sstrict/pristine.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/sstrict/pristine.mjs
$ wc -l /tmp/sstrict/pristine.mjs
2537 /tmp/sstrict/pristine.mjs
```

The sha256 matches the frozen pin recorded in
`.ufo/evidence/round-26/cite-check/predictions.json`
(`"pin_sha256": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"`)
and the spec header line 2; the line count matches the spec's `2537 lines`.

The mutant was produced by a single exact-string replacement, asserted to occur
exactly once:

```js
const src = fs.readFileSync(process.env.SRC, "utf8");
const old = process.env.OLD, neu = process.env.NEW;
const n = src.split(old).length - 1;
if (n !== 1) { console.error(`FATAL: @old occurs ${n} times, expected exactly 1`); process.exit(2); }
fs.writeFileSync(process.env.DST, src.replace(old, neu));
```

with `OLD` / `NEW` taken verbatim from the spec's `@old` / `@new` lines for
`@defect S_STRICT`.

Diff between the two materialized files (the only byte difference):

```
$ diff /tmp/sstrict/pristine.mjs /tmp/sstrict/mutant.mjs
1589c1589
<   const drift = totals.error > 0 || (opts.strict && totals.warn > 0);
---
>   const drift = totals.error > 0 || (opts.strict && totals.warn > 1);
```

## 3. The probe

The probe drives the **public CLI** (`--src/--self/--fleet --strict`), not
`--selftest`, over synthetic temp trees. The tree is built so that
`totals.filesScanned > 0`, `totals.resolved > 0` (so the verdict guard does not
fail closed) and `totals.error == 0` — the **only** difference between the two
bins is the warn count. The single warn is produced by an `ORPHAN_REF`: a lone
line ref `:424242` with no owning path token anywhere above it (pinned severity
`warn`, pinned line 221; the finding is emitted at pinned line 1491-1494).

`/tmp/sstrict/probe.sh`:

```bash
#!/usr/bin/env bash
# S_STRICT off-suite probe (tameshi round-26 C1).
# Materializes the pristine kumitate pin, derives the S_STRICT mutant by the
# exact @old/@new edit from cite-check.defects.spec, builds disposable doc trees
# with 0 / 1 / 2 warn-level findings, and runs BOTH binaries through the real
# CLI (--strict --json). Purely hermetic: temp trees only, env -i, no network.
set -u

NODE="${NODE:-/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node}"
KUMITATE="${KUMITATE:-/home/vgpnk/Projects/shokunin/kumitate-shokunin}"
PIN_REV="${PIN_REV:-1205c6621a2eccbb8ffceae86d9e7b79a7990b3a}"
WORK="$(mktemp -d /tmp/sstrict-probe-XXXXXX)"
trap 'rm -rf "$WORK"' EXIT

PRISTINE="$WORK/pristine.mjs"
MUTANT="$WORK/mutant.mjs"

# --- 1. pristine pin ------------------------------------------------------
git -C "$KUMITATE" show "$PIN_REV:scripts/cite-check.mjs" > "$PRISTINE"
echo "pin sha256 : $(sha256sum "$PRISTINE" | cut -d' ' -f1)"
echo "pin lines  : $(wc -l < "$PRISTINE")"

# --- 2. mutant: the exact S_STRICT @old/@new edit ------------------------
OLD='  const drift = totals.error > 0 || (opts.strict && totals.warn > 0);'
NEW='  const drift = totals.error > 0 || (opts.strict && totals.warn > 1);'
OLD="$OLD" NEW="$NEW" SRC="$PRISTINE" DST="$MUTANT" "$NODE" -e '
const fs = require("fs");
const src = fs.readFileSync(process.env.SRC, "utf8");
const old = process.env.OLD, neu = process.env.NEW;
const n = src.split(old).length - 1;
if (n !== 1) { console.error(`FATAL: @old occurs ${n} times, expected exactly 1`); process.exit(2); }
fs.writeFileSync(process.env.DST, src.replace(old, neu));
console.log("mutation applied: 1 occurrence replaced");
'
echo "mutant diff (unified, context 0):"
diff -U0 "$PRISTINE" "$MUTANT" | tail -n +3

# --- 3. disposable doc trees --------------------------------------------
# src tree holds the cited real file; self tree holds the docs; fleet is an
# empty parent dir (the tool refuses a non-dir with exit 2).
mk_tree() {           # mk_tree <dir> <number-of-warn-docs>
  local root="$1" warns="$2"
  mkdir -p "$root/src/scripts" "$root/self/corpus/knowledge" "$root/fleet"
  printf 'export const x = 1;\n' > "$root/src/scripts/real.mjs"
  printf '# doc\n\nSee `scripts/real.mjs`.\n' > "$root/self/SKILL.md"
  local i
  for ((i = 1; i <= warns; i++)); do
    # a lone ref with no owning path token -> exactly one ORPHAN_REF (warn)
    printf '# orphan %s\n\nA lone ref (:424242) with no path token anywhere above it.\n' "$i" \
      > "$root/self/corpus/knowledge/orphan-$i.md"
  done
}

run_case() {          # run_case <label> <warn-count>
  local label="$1" warns="$2"
  local root="$WORK/case-$label"
  mk_tree "$root" "$warns"
  local out
  for bin in pristine mutant; do
    env -i PATH=/usr/bin:/bin HOME=/nonexistent "$NODE" "$WORK/$bin.mjs" \
      --src "$root/src" --self "$root/self" --fleet "$root/fleet" \
      --strict --json > "$root/$bin.json" 2> "$root/$bin.err"
    printf '%s' "$?" > "$root/$bin.status"
  done
  local ps ms pv mv
  ps=$(cat "$root/pristine.status"); ms=$(cat "$root/mutant.status")
  pv=$("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(r.verdict+" "+r.citeCheck+" warn="+r.totals.warn+" error="+r.totals.error+" note="+r.totals.note+" resolved="+r.totals.resolved+" files="+r.totals.filesScanned+" byKind="+JSON.stringify(r.totals.byKind))' "$root/pristine.json")
  mv=$("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(r.verdict+" "+r.citeCheck+" warn="+r.totals.warn+" error="+r.totals.error+" note="+r.totals.note+" resolved="+r.totals.resolved+" files="+r.totals.filesScanned+" byKind="+JSON.stringify(r.totals.byKind))' "$root/mutant.json")
  echo "case $label (warn-docs=$warns)"
  echo "  pristine: exit=$ps  $pv"
  echo "  mutant  : exit=$ms  $mv"
  # the finding census must be byte-identical; only the strict threshold differs
  if ! diff <("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(JSON.stringify(r.files,null,1))' "$root/pristine.json") \
            <("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(JSON.stringify(r.files,null,1))' "$root/mutant.json") >/dev/null; then
    echo "  NOTE: finding censuses differ between pristine and mutant"
  else
    echo "  finding census: IDENTICAL in pristine and mutant"
  fi
  if [ "$ps" != "$ms" ]; then
    echo "  => DISTINGUISHED by exit status (pristine=$ps, mutant=$ms)"
  else
    echo "  => same exit status ($ps)"
  fi
  if [ -s "$root/pristine.err" ] || [ -s "$root/mutant.err" ]; then
    echo "  stderr pristine: $(cat "$root/pristine.err")"
    echo "  stderr mutant  : $(cat "$root/mutant.err")"
  else
    echo "  stderr: empty for both"
  fi
  echo
}

run_case "zero-warn" 0
run_case "one-warn" 1
run_case "two-warn" 2

# --- 4. independent warn shape (SUFFIX_RESOLVED, not ORPHAN_REF) --------
# The discriminator is the warn COUNT, not the warn KIND: a unique-suffix
# citation is the second, independent warn kind that separates the two bins.
echo "case one-warn-suffix (SUFFIX_RESOLVED instead of ORPHAN_REF)"
SR="$WORK/case-suffix"
mkdir -p "$SR/src/scripts/ufo-lib" "$SR/self/corpus/knowledge" "$SR/fleet"
printf 'export const x = 1;\n' > "$SR/src/scripts/real.mjs"
printf 'export const y = 1;\n' > "$SR/src/scripts/ufo-lib/base.mjs"
printf '# doc\n\nSee `scripts/real.mjs`.\n' > "$SR/self/SKILL.md"
printf '# suffix\n\nResolve `ufo-lib/base.mjs`.\n' > "$SR/self/corpus/knowledge/suffix.md"
for bin in pristine mutant; do
  env -i PATH=/usr/bin:/bin HOME=/nonexistent "$NODE" "$WORK/$bin.mjs" \
    --src "$SR/src" --self "$SR/self" --fleet "$SR/fleet" --strict --json \
    > "$SR/$bin.json" 2> "$SR/$bin.err"
  printf '%s' "$?" > "$SR/$bin.status"
done
ss=$(cat "$SR/pristine.status"); sm=$(cat "$SR/mutant.status")
echo "  pristine: exit=$ss  $("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(r.verdict+" "+r.citeCheck+" warn="+r.totals.warn+" byKind="+JSON.stringify(r.totals.byKind))' "$SR/pristine.json")"
echo "  mutant  : exit=$sm  $("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(r.verdict+" "+r.citeCheck+" warn="+r.totals.warn+" byKind="+JSON.stringify(r.totals.byKind))' "$SR/mutant.json")"
[ "$ss" != "$sm" ] && echo "  => DISTINGUISHED by exit status (pristine=$ss, mutant=$sm)" || echo "  => same exit status ($ss)"
echo

# --- 5. control: the SAME one-warn tree WITHOUT --strict ----------------
# Without --strict, warn never promotes, so the mutant's threshold change is
# unreachable and both bins must agree. If they do not, the discriminator is
# not strict-specific.
echo "control: one-warn tree WITHOUT --strict"
NR="$WORK/case-nostrict"
mkdir -p "$NR/src/scripts" "$NR/self/corpus/knowledge" "$NR/fleet"
printf 'export const x = 1;\n' > "$NR/src/scripts/real.mjs"
printf '# doc\n\nSee `scripts/real.mjs`.\n' > "$NR/self/SKILL.md"
printf '# orphan\n\nA lone ref (:424242) with no path token anywhere above it.\n' > "$NR/self/corpus/knowledge/orphan.md"
for bin in pristine mutant; do
  env -i PATH=/usr/bin:/bin HOME=/nonexistent "$NODE" "$WORK/$bin.mjs" \
    --src "$NR/src" --self "$NR/self" --fleet "$NR/fleet" --json \
    > "$NR/$bin.json" 2> "$NR/$bin.err"
  printf '%s' "$?" > "$NR/$bin.status"
done
ns=$(cat "$NR/pristine.status"); nm=$(cat "$NR/mutant.status")
echo "  pristine: exit=$ns  $("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(r.verdict+" "+r.citeCheck+" warn="+r.totals.warn)' "$NR/pristine.json")"
echo "  mutant  : exit=$nm  $("$NODE" -e 'const r=JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"));console.log(r.verdict+" "+r.citeCheck+" warn="+r.totals.warn)' "$NR/mutant.json")"
[ "$ns" = "$nm" ] && echo "  => agree, as required (the discriminator is --strict specific)" || echo "  => DISAGREE (unexpected)"
echo
```

### Observed output — pristine

```
$ bash /tmp/sstrict/probe.sh
pin sha256 : 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
pin lines  : 2537
mutation applied: 1 occurrence replaced
mutant diff (unified, context 0):
@@ -1589 +1589 @@
-  const drift = totals.error > 0 || (opts.strict && totals.warn > 0);
+  const drift = totals.error > 0 || (opts.strict && totals.warn > 1);
case zero-warn (warn-docs=0)
  pristine: exit=0  PASS CLEAN warn=0 error=0 note=1 resolved=1 files=1 byKind={"OK":1}
  mutant  : exit=0  PASS CLEAN warn=0 error=0 note=1 resolved=1 files=1 byKind={"OK":1}
  finding census: IDENTICAL in pristine and mutant
  => same exit status (0)
  stderr: empty for both

case one-warn (warn-docs=1)
  pristine: exit=1  FAIL DRIFT warn=1 error=0 note=1 resolved=1 files=2 byKind={"OK":1,"ORPHAN_REF":1}
  mutant  : exit=0  PASS CLEAN warn=1 error=0 note=1 resolved=1 files=2 byKind={"OK":1,"ORPHAN_REF":1}
  finding census: IDENTICAL in pristine and mutant
  => DISTINGUISHED by exit status (pristine=1, mutant=0)
  stderr: empty for both

case two-warn (warn-docs=2)
  pristine: exit=1  FAIL DRIFT warn=2 error=0 note=1 resolved=1 files=3 byKind={"OK":1,"ORPHAN_REF":2}
  mutant  : exit=1  FAIL DRIFT warn=2 error=0 note=1 resolved=1 files=3 byKind={"OK":1,"ORPHAN_REF":2}
  finding census: IDENTICAL in pristine and mutant
  => same exit status (1)
  stderr: empty for both

case one-warn-suffix (SUFFIX_RESOLVED instead of ORPHAN_REF)
  pristine: exit=1  FAIL DRIFT warn=1 byKind={"OK":1,"SUFFIX_RESOLVED":1}
  mutant  : exit=0  PASS CLEAN warn=1 byKind={"OK":1,"SUFFIX_RESOLVED":1}
  => DISTINGUISHED by exit status (pristine=1, mutant=0)

control: one-warn tree WITHOUT --strict
  pristine: exit=0  PASS CLEAN warn=1
  mutant  : exit=0  PASS CLEAN warn=1
  => agree, as required (the discriminator is --strict specific)
```

### Observed output — mutant

The mutant half of each case is printed in the same run above (the `mutant  :`
lines). The decisive case, side by side on the *same* one-warn tree, in the
tool's own text output:

```
===== pristine (text mode) =====
exit=1
kumitate cite-check — kumitate-cite-check-v1
src=/tmp/sstrict/showcase/src (index 1 files)
self=/tmp/sstrict/showcase/self  fleet=/tmp/sstrict/showcase/fleet
mode: strict

corpus/knowledge/orphan.md
  corpus/knowledge/orphan.md:3  WARN  ORPHAN_REF        [source/none] :424242 — :424242 has no owning path token in corpus/knowledge/orphan.md (no sticky owner yet)

totals
  filesScanned=2 docs=2 tokens=2 refs=0 symbols=0 findings=2
  orphanRefs=1 altOwnerRefs=0 declarations=0
  bySeverity={"note":1,"warn":1}
  byClass={"source":2}
  byKind={"OK":1,"ORPHAN_REF":1}
  byRung={"src":1,"none":1}
  pins=0 ok=0 mismatch=0 untyped=0 revUnknown=0 unchecked=0
  indexFiles=1 selfIndexFiles=2 fleetIndexFiles=0
VERDICT: FAIL
CITE_CHECK: DRIFT (files=2 tokens=2 errors=0 warnings=1)
```

```
===== mutant (text mode) =====
exit=0
kumitate cite-check — kumitate-cite-check-v1
src=/tmp/sstrict/showcase/src (index 1 files)
self=/tmp/sstrict/showcase/self  fleet=/tmp/sstrict/showcase/fleet
mode: strict

corpus/knowledge/orphan.md
  corpus/knowledge/orphan.md:3  WARN  ORPHAN_REF        [source/none] :424242 — :424242 has no owning path token in corpus/knowledge/orphan.md (no sticky owner yet)

totals
  filesScanned=2 docs=2 tokens=2 refs=0 symbols=0 findings=2
  orphanRefs=1 altOwnerRefs=0 declarations=0
  bySeverity={"note":1,"warn":1}
  byClass={"source":2}
  byKind={"OK":1,"ORPHAN_REF":1}
  byRung={"src":1,"none":1}
  pins=0 ok=0 mismatch=0 untyped=0 revUnknown=0 unchecked=0
  indexFiles=1 selfIndexFiles=2 fleetIndexFiles=0
VERDICT: PASS
CITE_CHECK: CLEAN (files=2 tokens=2 errors=0 warnings=1)
```

The two runs differ in three independent observable ways: the `VERDICT:` line
(`FAIL` vs `PASS`), the `CITE_CHECK:` line (`DRIFT` vs `CLEAN`), and the process
**exit status (1 vs 0)**. The exit status alone is a sufficient oracle. The
finding census is byte-identical (same `byKind`, same `bySeverity`, same
`files` array in `--json`), which confirms the divergence is *only* the strict
threshold and not an unrelated parsing difference.

## 4. The mutant really is a suite survivor (the probe is off-suite, not a re-run of the suite)

Both pinned and mutated binaries still pass the full hermetic suite, so the
suite genuinely cannot see this defect and the probe is the only thing that can:

```
$ env -i PATH=/usr/bin:/bin HOME=/nonexistent node /tmp/sstrict/pristine.mjs --selftest | tail -3
PASS  bare run (no --src): both candidates absent keeps the --src fail-closed arm (exit 2) — exit=2 cite-check: fail-closed — --src /tmp/kumitate-cite-selftest-2ddHG5/home-none/Projects/ufo-fsd-alpha is missing
62/62 cases passed (hermetic)
VERDICT: PASS
$ env -i PATH=/usr/bin:/bin HOME=/nonexistent node /tmp/sstrict/mutant.mjs --selftest | tail -3
PASS  bare run (no --src): both candidates absent keeps the --src fail-closed arm (exit 2) — exit=2 cite-check: fail-closed — --src /tmp/kumitate-cite-selftest-9QVJCO/home-none/Projects/ufo-fsd-alpha is missing
62/62 cases passed (hermetic)
VERDICT: PASS
```

(`--selftest` was run in the `/tmp` scratch dir, never inside
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.)

## 5. Boundary sanity: the discriminator is exactly `warn == 1`

Sweeping the number of warn-producing docs over the same tree shape shows the
two bins agree everywhere except the single-warn point:

```
warns=0  pristine[exit=0 PASS/CLEAN warn=0]  mutant[exit=0 PASS/CLEAN warn=0]
warns=1  pristine[exit=1 FAIL/DRIFT warn=1]  mutant[exit=0 PASS/CLEAN warn=1]
warns=2  pristine[exit=1 FAIL/DRIFT warn=2]  mutant[exit=1 FAIL/DRIFT warn=2]
warns=3  pristine[exit=1 FAIL/DRIFT warn=3]  mutant[exit=1 FAIL/DRIFT warn=3]
warns=4  pristine[exit=1 FAIL/DRIFT warn=4]  mutant[exit=1 FAIL/DRIFT warn=4]
```

`warn == 1` is the unique discriminating warn count: `warn == 0` never
promotes in either bin, and `warn >= 2` promotes in both.

Two further robustness checks, both in the probe output above:

- **The warn KIND does not matter.** A tree whose single warn is a
  `SUFFIX_RESOLVED` (a unique-suffix citation `ufo-lib/base.mjs` against
  `src/scripts/ufo-lib/base.mjs`) separates the bins exactly the same way
  (pristine exit 1 DRIFT, mutant exit 0 CLEAN). The discriminator is the warn
  *count*, not the warn *kind*, so the probe is not tied to one fixture shape.
- **The `--strict` flag is load-bearing.** The same one-warn tree run *without*
  `--strict` gives exit 0 / PASS / CLEAN in **both** bins, because the mutant's
  changed predicate is unreachable when `opts.strict` is false. This confirms
  the separation is specific to the mutated branch and is not an artifact of the
  tree.

## 6. Argument that no input could distinguish them — refuted

There is no such argument. The pre-registration's `SURVIVED` prediction was
about the *suite* (no fixture passes `--strict`), not about the *program*. The
drift predicate is a total function of `(totals.error, opts.strict,
totals.warn)`, and the mutant changes it on exactly the inputs where
`opts.strict === true && totals.error === 0 && totals.warn === 1`. The probe
exhibits such an input — a tree with one warn-level finding and no errors, run
with `--strict` — and the two programs return different verdicts
(`FAIL`/`DRIFT` vs `PASS`/`CLEAN`) and different exit codes (1 vs 0) on it.
Therefore the two binaries are **not** behaviourally equivalent, and no
argument of equivalence can stand.

## 7. Smallest safe correction implied (for the lane's integrator; NOT applied here)

The mutant's own line is the defect. The correct predicate is the pristine one,
`totals.error > 0 || (opts.strict && totals.warn > 0)` (pristine line 1589).
The gap in the fixture set is that no hermetic case runs with `--strict` at
all. A single hermetic case would close it: materialize a tree with exactly one
warn-level finding and one resolved citation, run `runCheck` with
`{ strict: true }`, and assert `verdict === 'FAIL'` (and `totals.warn === 1`).
That case kills `S_STRICT` and is orthogonal to the existing 62. No production
file was edited by this seat.

## 8. Environment, tooling, and bounds

- Node: `v24.21.0` (`/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node`).
- **No packages were installed or upgraded by this seat**, so there is no
  install record to report. The probe needed only `node`, `mktemp`, `printf`,
  `diff` and `git` (all pre-existing).
- Everything ran under `/tmp/sstrict` (scratch) and `/tmp/sstrict-probe-*`
  (probe temp trees, removed by the script's `trap`). Nothing was executed
  inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Read-only git was used against the sibling lane
  (`git -C .../kumitate-shokunin show <rev>:scripts/cite-check.mjs`); no git
  write command was run, and **no `jj` command was run anywhere**.
- Files written by this seat: this report only. The pristine/mutant/probe
  artifacts live in `/tmp` scratch and are not lane files.

## 9. Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-26/w1/ProbeSSTRICT.md`
  (this report) — the only lane file touched.

PROBE S_STRICT: DISTINGUISHED
