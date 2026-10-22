# ProbeSEMPTYGUARD — C1 survivor probe for S_EMPTY_GUARD

**Seat:** `TameshiR26.ProbeSEMPTYGUARD` (leaf executor, wave 1 of 2)
**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Target:** kumitate `scripts/cite-check.mjs` at rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`
**Defect under probe:** `S_EMPTY_GUARD` (pre-registered spec `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`)
**Scratch only:** everything below ran under `/tmp`. No lane file was modified, no `jj` command was run, no git write command was run.

---

## VERDICT (first, per lane bounds)

**No input separates the pristine binary from the S_EMPTY_GUARD mutant. The mutant is behaviourally equivalent to the pristine on every input tried, and the code carries a structural proof of that equivalence: `totals.resolved` is incremented only inside the same per-document loop that increments `totals.filesScanned`, so `resolved > 0` implies `filesScanned > 0` always. The dropped guard `totals.filesScanned > 0` is therefore *redundant* given the surviving guard `totals.resolved > 0`, not merely untested.**

The sweep's `PREDICT SURVIVED` for S_EMPTY_GUARD was correct — and the reason is stronger than "the suite has no case for it": the mutant is an equivalent mutant, i.e. it cannot be killed by *any* oracle on this input space.

---

## 1. The two programs

### Pristine (materialized from the pin)

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs \
    > /tmp/s_empty_guard/cite-check.pristine.mjs
$ wc -l   /tmp/s_empty_guard/cite-check.pristine.mjs
2537 /tmp/s_empty_guard/cite-check.pristine.mjs
$ sha256sum /tmp/s_empty_guard/cite-check.pristine.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/s_empty_guard/cite-check.pristine.mjs
```

Blob sha256 `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f` and line count `2537` match the pin recorded in the spec header and in the round-26 contract.

### Mutant (exactly the spec `@old`/`@new`, one occurrence, single-line delta)

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/cite-check.defects.spec`:

```
# PREDICT SURVIVED — an empty scan set also has zero resolved citations, so the resolved guard alone still fails it (co-extensive guard).
@defect S_EMPTY_GUARD | the verdict drops only the scanned-files guard
@old   const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
@new   const verdict = totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
```

Applied exactly:

```
$ python3 - <<'PY'   # (edited copy; the @old string occurs exactly once — printed "old occurrences: 1")
...
PY
old occurrences: 1
$ diff -u cite-check.pristine.mjs cite-check.mutant.mjs
@@ -1587,7 +1587,7 @@
   }

   const drift = totals.error > 0 || (opts.strict && totals.warn > 0);
-  const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
+  const verdict = totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
   return {
```

Byte-level confirmation that nothing else changed:

```
$ python3 -c "...common prefix/suffix trim..."
len 126735 126708 delta -27
pristine: b'filesScanned > 0 &&'
mutant  : b''
context before: b' (opts.strict && totals.warn > 0);\n  const verdict = totals.'
```

The mutant differs from the pristine by exactly the 27 bytes `filesScanned > 0 && ` removed. `sha256sum` of the mutant: `949c29035366702b3e93ca9d8ed5a6df25275f104ebe72490a7cc11893bea5d5`.

---

## 2. Where the two expressions can differ — and why they cannot

The two verdicts disagree only when

```
filesScanned == 0  AND  resolved > 0  AND  !drift
```

i.e. exactly the state the task hint points at: *does any input reach `filesScanned == 0` with `resolved > 0`?*

### Structural answer: no, and the reason is a code invariant

In `/tmp/s_empty_guard/cite-check.pristine.mjs`, `runCheck()` has exactly one write site for each counter:

```
1554:    docs: docs.length, filesScanned: 0, ...
1549:    resolved: 0, error: 0, warn: 0, note: 0,
...
1554:  for (const rel of docs) {
1555:    let text;
1556:    try { text = readFileSync(join(opts.self, rel), 'utf8'); } catch { continue; }
1557:    totals.filesScanned++;                                  <-- filesScanned++
...
1583:      if (f.kind === 'OK') totals.resolved++;                <-- resolved++ (same loop body)
1584:    }
1585:    totals.findings += findings.length;
1586:    files.push({ file: rel, findings });
1587:  }
1589:  const drift = totals.error > 0 || (opts.strict && totals.warn > 0);
1590:  const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
```

`grep -n 'totals\.resolved\|totals\.filesScanned\|resolved++\|filesScanned++'` on the pristine bytes returns exactly:

```
1556:    totals.filesScanned++;
1583:      if (f.kind === 'OK') totals.resolved++;
1590:  const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
```

`totals.resolved` is bumped **only** inside the `for (const rel of docs)` loop, and only *after* `totals.filesScanned++` has already run for that same document (line 1556 precedes line 1583, and the `catch { continue; }` on line 1556 skips the whole body without touching either counter). Therefore:

> **`totals.resolved > 0` ⟹ at least one document was scanned ⟹ `totals.filesScanned > 0`.**

The guard the mutant drops is *implied* by the guard it keeps. `filesScanned > 0 && resolved > 0` and `resolved > 0` are the same predicate over every reachable state. The mutant is an **equivalent mutant**: no oracle, on any input, can distinguish it.

### Empirical answer: no input reaches it either

The probe below additionally hunts for the state directly, with an instrumented build that aborts if it ever occurs.

---

## 3. The probe

Files, all under `/tmp/s_empty_guard/` (nothing in the lane):

| file | role |
|---|---|
| `cite-check.pristine.mjs` | pinned bytes, sha256 `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f` |
| `cite-check.mutant.mjs` | pristine + the exact `S_EMPTY_GUARD` `@old`→`@new` edit |
| `cite-check.instrumented.mjs` | pristine + an assertion that fires iff `filesScanned == 0 && resolved > 0` |
| `extract.py` | parses a captured run (`--stdout--` … `--stderr--`) into `filesScanned/resolved/verdict` |
| `probe.sh` | the driver (5 phases) |
| `kumitate_pin/` | the full pinned kumitate tree (`git archive 1205c66 \| tar -x`), used as a real 75-document corpus |

The instrumented build differs from the pristine by exactly this insertion immediately before the verdict line:

```js
  if (totals.resolved > 0 && totals.filesScanned === 0) {
    process.stderr.write('INVARIANT_VIOLATION filesScanned=0 resolved=' + totals.resolved + '\n');
    process.exitCode = 91;
  }
```

### Driver shape

Every run is a real CLI process under `env -i` (no inherited environment), from a `mktemp -d` tree:

```
env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$bin" \
    --src "$SRC" --self "$selfdir" --fleet "$FLEET" "$@" \
    > out 2> err
```

and the two binaries are compared on the **triple** `(exit status, stdout bytes, stderr bytes)` — not on a parsed verdict. A run counts as a difference only if all three differ.

Phases:

1. **Hand-built scenario battery** — 16 trees × 6 flag sets = 96 paired runs. The trees are chosen to attack the invariant from every side: a true empty scan set (no `SKILL.md`, no `corpus/`), a corpus with no `.md`, a prose-only doc (`filesScanned=1, resolved=0`), a doc with one resolvable citation, a doc that both resolves and drifts, an unreadable doc (`chmod 000` — read fails, so `filesScanned` does not advance), an unreadable doc alongside a good one, an absolute path, a `~/.omp/...` home-config path, a `target/` pruned path, a `.ufo/` runtime artifact, a *directory* literally named `x.md`, a nested `corpus/knowledge/doc.md`, runtime-artifact + real citation together, `SKILL.md` as a *directory*, and an unreadable `SKILL.md`.
2. **Randomized fuzz** — 300 generated doc trees × 2 flag sets = 600 paired runs, seeded (`random.Random(20261026)`), drawing from 19 token shapes (real paths, dead paths, pruned paths, runtime artifacts, absolute paths, home paths, alias-with-ref forms, fragments).
3. **Full pinned kumitate tree** — the whole `1205c66` tree (80 markdown files) as `--self`, giving 75 scanned documents and 1679 resolved citations.
4. **Pinned hermetic suite** — `node <binary> --selftest` on both, byte-compared after masking the two known sources of run-to-run nondeterminism (the fixture repo's fresh `HEAD` sha and the `mkdtemp` directory name — I verified the pristine binary differs from *itself* across two consecutive runs in exactly those two places, so masking them is required for a fair comparison, not a fudge).
5. **Instrumented invariant sweep** — the instrumented build is run over every tree from phases 1–3 plus `--selftest`, and any `INVARIANT_VIOLATION` on stderr is counted.

An extra exotic pass (symlinked `.md`, FIFO `.md`, 512 random bytes as `.md`, fenced-only citation, UTF-8 BOM, zero-byte `.md`, a 5000-citation `.md`) also produced zero differences.

### Probe source

```bash
#!/usr/bin/env bash
# =====================================================================
# S_EMPTY_GUARD survivor probe  (off-suite, hermetic, /tmp only)
#
# Pristine (kumitate scripts/cite-check.mjs @ 1205c66, line 1590):
#   const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
# Mutant (S_EMPTY_GUARD @old/@new from .ufo/evidence/round-26/cite-check/cite-check.defects.spec):
#   const verdict = totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
#
# The two expressions differ only when filesScanned == 0 && resolved > 0
# && !drift.  This probe hunts for such a state and, failing that, proves
# the two binaries are indistinguishable on every input tried.
#
# Everything runs from a mktemp tree under /tmp with `env -i`.
# No lane file is written or executed in place; no git write command is used.
# =====================================================================
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PRISTINE="$HERE/cite-check.pristine.mjs"
MUTANT="$HERE/cite-check.mutant.mjs"
INSTRUMENTED="$HERE/cite-check.instrumented.mjs"
NODE="$(readlink -f "$(command -v node)")"
ROOT="$(mktemp -d /tmp/s-empty-guard-probe.XXXXXX)"
trap 'rm -rf "$ROOT"' EXIT

SRC="$ROOT/src"
FLEET="$ROOT/fleet"
S="$ROOT/self"
mkdir -p "$SRC/scripts" "$SRC/config" "$SRC/src/utils" "$FLEET"
printf '{"a":1}\n' > "$SRC/config/app.json"
for i in $(seq 1 20); do echo "// real line $i"; done > "$SRC/scripts/real.mjs"
echo 'export const x = 1;' > "$SRC/src/utils/thing.ts"

run_one() { # $1 binary  $2 selfdir  $3.. extra CLI args
  local bin="$1" selfdir="$2"; shift 2
  env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$bin" \
      --src "$SRC" --self "$selfdir" --fleet "$FLEET" "$@" \
      > "$ROOT/out.$$" 2> "$ROOT/err.$$"
  local rc=$?
  printf 'RC=%s\n--stdout--\n%s--stderr--\n%s' "$rc" "$(cat "$ROOT/out.$$")" "$(cat "$ROOT/err.$$")"
  rm -f "$ROOT/out.$$" "$ROOT/err.$$"
}

DIFFS=0
COUNTER=0

# ---------------------------------------------------------------- (0) trees
mkdir -p "$S/s1_empty_scan_set"                                   # nothing scanned at all
mkdir -p "$S/s2_corpus_no_md/corpus"; echo notes > "$S/s2_corpus_no_md/corpus/notes.txt"
mkdir -p "$S/s3_prose_only"
printf '# prose only\n\nno citations here\n' > "$S/s3_prose_only/SKILL.md"
mkdir -p "$S/s4_resolves_one"
printf '# resolves\n\nsee `config/app.json`\n' > "$S/s4_resolves_one/SKILL.md"
mkdir -p "$S/s5_resolves_and_drifts"
printf '# drifts\n\nsee `config/app.json` and `scripts/no-such-file.mjs`\n' > "$S/s5_resolves_and_drifts/SKILL.md"
mkdir -p "$S/s6_unreadable_only/corpus"
printf '# locked\n\n`config/app.json`\n' > "$S/s6_unreadable_only/corpus/locked.md"
chmod 000 "$S/s6_unreadable_only/corpus/locked.md"
mkdir -p "$S/s7_unreadable_plus_good/corpus"
printf '# locked\n\n`config/app.json`\n' > "$S/s7_unreadable_plus_good/corpus/locked.md"
chmod 000 "$S/s7_unreadable_plus_good/corpus/locked.md"
printf '# good\n\n`config/app.json`\n' > "$S/s7_unreadable_plus_good/corpus/good.md"
mkdir -p "$S/s8_absolute_path"
printf '# absolute\n\nsee `/etc/hostname`\n' > "$S/s8_absolute_path/SKILL.md"
mkdir -p "$S/s9_home_config"
printf '# home\n\nsee `~/.omp/config.json`\n' > "$S/s9_home_config/SKILL.md"
mkdir -p "$S/s10_pruned_dir"
printf '# pruned\n\nsee `target/debug/out.rs`\n' > "$S/s10_pruned_dir/SKILL.md"
mkdir -p "$S/s11_runtime_artifact"
printf '# runtime\n\nsee `.ufo/pending-work.json`\n' > "$S/s11_runtime_artifact/SKILL.md"
mkdir -p "$S/s12_dir_named_md/corpus/x.md"                         # directory literally named x.md
mkdir -p "$S/s13_nested_md/corpus/knowledge"
printf '# nested\n\n`config/app.json`\n' > "$S/s13_nested_md/corpus/knowledge/doc.md"
mkdir -p "$S/s14_runtime_plus_real"
printf '# runtime artifact\n\n`.ufo/pending-work.json` and `config/app.json`\n' > "$S/s14_runtime_plus_real/SKILL.md"
mkdir -p "$S/s15_skill_is_dir/SKILL.md"                            # SKILL.md is a DIRECTORY
printf '# inside\n\n`config/app.json`\n' > "$S/s15_skill_is_dir/SKILL.md/inner.md"
mkdir -p "$S/s16_skill_unreadable"
printf '# x\n\n`config/app.json`\n' > "$S/s16_skill_unreadable/SKILL.md"
chmod 000 "$S/s16_skill_unreadable/SKILL.md"

# ------------------------------------------------------- (1) hand-built battery
printf '=== (1) hand-built scenario battery: pristine vs mutant (stdout+stderr+exit status) ===\n'
while read -r name; do
  for extra in "--json" "" "--strict --json" "--all --json" "--symbols --json" "--strict"; do
    A="$(run_one "$PRISTINE" "$S/$name" $extra)"
    B="$(run_one "$MUTANT" "$S/$name" $extra)"
    if [ "$A" = "$B" ]; then st='identical'; else st='DIFFERENT'; DIFFS=$((DIFFS+1)); fi
    printf '%s' "$A" > "$ROOT/A.txt"
    info="$(python3 "$HERE/extract.py" "$ROOT/A.txt")"
    flag=''
    case "$info" in
      'filesScanned=0 resolved=0'*) : ;;
      'filesScanned=0 '*) flag='   <<< COUNTEREXAMPLE: filesScanned==0 with resolved>0'; COUNTER=$((COUNTER+1));;
    esac
    printf '%-22s %-18s %-10s %s%s\n' "$name" "${extra:-<text>}" "$st" "$info" "$flag"
  done
done <<'NAMES'
s1_empty_scan_set
s2_corpus_no_md
s3_prose_only
s4_resolves_one
s5_resolves_and_drifts
s6_unreadable_only
s7_unreadable_plus_good
s8_absolute_path
s9_home_config
s10_pruned_dir
s11_runtime_artifact
s12_dir_named_md
s13_nested_md
s14_runtime_plus_real
s15_skill_is_dir
s16_skill_unreadable
NAMES

# ---------------------------------------------------------------- (2) fuzz
printf '\n=== (2) randomized doc-tree fuzz: 300 trees x 2 flag sets ===\n'
python3 - "$ROOT" <<'PY'
import os, random, sys
root = sys.argv[1]
rng = random.Random(20261026)
tokens = [
    "config/app.json", "scripts/real.mjs", "scripts/no-such-file.mjs", "src/utils/thing.ts",
    "target/debug/out.rs", ".ufo/pending-work.json", "/etc/hostname", "~/.omp/config.json",
    "base:1233", "dispatcher:5", "cli:1", "manifest.json", "meta.json", "gen_roles.rs",
    "real.rs:2", "gate.rs:1", "config/app.json:12", "ufo-lib/base.mjs", "*.mjs",
]
for n in range(300):
    d = os.path.join(root, "fuzz", "t%03d" % n)
    os.makedirs(os.path.join(d, "corpus", "knowledge"), exist_ok=True)
    for k in range(rng.randint(0, 3)):
        lines = ["# fuzz doc %d/%d" % (n, k), ""]
        for _ in range(rng.randint(0, 6)):
            t = rng.choice(tokens)
            shape = rng.randint(0, 3)
            if shape == 0:   lines.append("see `%s`" % t)
            elif shape == 1: lines.append("see `%s` and `scripts/real.mjs`" % t)
            elif shape == 2: lines.append("`%s`" % t)
            else:            lines.append("plain prose mentioning %s" % t)
        name = rng.choice(["SKILL.md", "corpus/doc.md", "corpus/knowledge/doc.md"])
        with open(os.path.join(d, name), "w") as fh:
            fh.write("\n".join(lines) + "\n")
PY

fuzz_diff=0; fuzz_counter=0; fuzz_runs=0
for selfdir in "$ROOT"/fuzz/t*; do
  for extra in "--json" "--strict --json"; do
    A="$(run_one "$PRISTINE" "$selfdir" $extra)"
    B="$(run_one "$MUTANT" "$selfdir" $extra)"
    fuzz_runs=$((fuzz_runs+1))
    [ "$A" != "$B" ] && fuzz_diff=$((fuzz_diff+1))
    printf '%s' "$A" > "$ROOT/A.txt"
    info="$(python3 "$HERE/extract.py" "$ROOT/A.txt" | sed -E 's/filesScanned=([0-9]+) resolved=([0-9]+).*/\1 \2/')"
    case "$info" in
      '0 0') : ;;
      '0 '*) fuzz_counter=$((fuzz_counter+1));;
    esac
  done
done
printf 'fuzz runs=%d  output/exit differences=%d  filesScanned==0 & resolved>0 hits=%d\n' \
  "$fuzz_runs" "$fuzz_diff" "$fuzz_counter"
DIFFS=$((DIFFS + fuzz_diff)); COUNTER=$((COUNTER + fuzz_counter))

# ------------------------------------------------- (3) real pinned kumitate tree
printf '\n=== (3) full pinned kumitate tree (1205c66) as --self ===\n'
if [ -d "$HERE/kumitate_pin" ]; then
  K="$HERE/kumitate_pin"
  env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$PRISTINE" --src "$K" --self "$K" --fleet "$FLEET" --json > "$ROOT/kp.json" 2> "$ROOT/kp.err"; kprc=$?
  env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$MUTANT"   --src "$K" --self "$K" --fleet "$FLEET" --json > "$ROOT/km.json" 2> "$ROOT/km.err"; kmrc=$?
  printf 'pristine rc=%d  mutant rc=%d\n' "$kprc" "$kmrc"
  if cmp -s "$ROOT/kp.json" "$ROOT/km.json" && cmp -s "$ROOT/kp.err" "$ROOT/km.err"; then
    printf 'pinned-tree stdout+stderr: IDENTICAL\n'
  else
    printf 'pinned-tree stdout+stderr: DIFFERENT\n'; diff "$ROOT/kp.json" "$ROOT/km.json" | head -20; DIFFS=$((DIFFS+1))
  fi
  python3 - "$ROOT/kp.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1])); t = r["totals"]
print("pinned-tree totals: filesScanned=%d resolved=%d error=%d warn=%d verdict=%s"
      % (t["filesScanned"], t["resolved"], t["error"], t["warn"], r["verdict"]))
PY
else
  printf 'kumitate_pin tree absent — skipped\n'
fi

# --------------------------------------------------- (4) pinned hermetic suite
printf '\n=== (4) pinned hermetic suite on both binaries ===\n'
env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$PRISTINE" --selftest > "$ROOT/st.p" 2>&1; prc=$?
env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$MUTANT"   --selftest > "$ROOT/st.m" 2>&1; mrc=$?
printf 'pristine --selftest rc=%d ; mutant --selftest rc=%d\n' "$prc" "$mrc"
# the suite output is not byte-stable run to run (fixture repo HEAD sha + tmpdir
# name), so both are masked before comparison; the sha mask is the same one
# applied to a pristine-vs-pristine control run.
NORM='s#/tmp/kumitate-cite-selftest-[A-Za-z0-9]+#TMP#g; s#[0-9a-f]{40}#SHA#g'
sed -E "$NORM" "$ROOT/st.p" > "$ROOT/st.pn"
sed -E "$NORM" "$ROOT/st.m" > "$ROOT/st.mn"
if cmp -s "$ROOT/st.pn" "$ROOT/st.mn"; then
  printf 'selftest stdout/stderr: identical\n'
else
  printf 'selftest stdout/stderr: DIFFERENT\n'; diff -u "$ROOT/st.pn" "$ROOT/st.mn" | head -40; DIFFS=$((DIFFS+1))
fi
grep -E 'cases passed|^VERDICT' "$ROOT/st.p" | tail -3

# ------------------------------------ (5) instrumented invariant sweep
printf '\n=== (5) instrumented build: does any run reach filesScanned==0 with resolved>0? ===\n'
inv_viol=0; inv_runs=0
for selfdir in "$S"/* "$ROOT"/fuzz/t* "$HERE/kumitate_pin"; do
  [ -d "$selfdir" ] || continue
  for extra in "--json" "--strict --json"; do
    env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$INSTRUMENTED" \
        --src "$SRC" --self "$selfdir" --fleet "$FLEET" $extra > "$ROOT/i.out" 2> "$ROOT/i.err"
    inv_runs=$((inv_runs+1))
    if grep -q INVARIANT_VIOLATION "$ROOT/i.err"; then
      inv_viol=$((inv_viol+1)); printf 'VIOLATION in %s %s\n' "$selfdir" "$extra"
    fi
  done
done
env -i PATH=/usr/bin:/bin HOME="$ROOT" "$NODE" "$INSTRUMENTED" --selftest > "$ROOT/is.log" 2>&1
if grep -q INVARIANT_VIOLATION "$ROOT/is.log"; then inv_viol=$((inv_viol+1)); printf 'VIOLATION in --selftest\n'; fi
inv_runs=$((inv_runs+1))
printf 'instrumented runs=%d  invariant violations (filesScanned==0 && resolved>0)=%d\n' "$inv_runs" "$inv_viol"

printf '\nSUMMARY: total differing runs = %d\n' "$DIFFS"
printf 'SUMMARY: states with filesScanned==0 and resolved>0 = %d\n' "$COUNTER"
if [ "$DIFFS" -eq 0 ] && [ "$COUNTER" -eq 0 ]; then
  printf 'PROBE RESULT: no input found that separates pristine from mutant\n'
else
  printf 'PROBE RESULT: separator found\n'
fi
```

The extractor (`extract.py`) — it reads a captured run and reports the counters, so the probe can both compare bytes and report the invariant state:

```python
import sys, json, re
raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.search(r"--stdout--\n(.*?)--stderr--", raw, re.S)
body = m.group(1) if m else ""
try:
    rep = json.loads(body)
    t = rep["totals"]
    print("filesScanned=%d resolved=%d error=%d warn=%d verdict=%s"
          % (t["filesScanned"], t["resolved"], t["error"], t["warn"], rep["verdict"]))
except Exception:
    v = re.search(r"VERDICT: (\w+)", body)
    print("text verdict=%s" % (v.group(1) if v else "none"))
```

---

## 4. Observed outputs

### 4.1 Probe summary (verbatim tail)

```
=== (2) randomized doc-tree fuzz: 300 trees x 2 flag sets ===
fuzz runs=600  output/exit differences=0  filesScanned==0 & resolved>0 hits=0

=== (3) full pinned kumitate tree (1205c66) as --self ===
pristine rc=1  mutant rc=1
pinned-tree stdout+stderr: IDENTICAL
pinned-tree totals: filesScanned=75 resolved=1679 error=1865 warn=3434 verdict=FAIL

=== (4) pinned hermetic suite on both binaries ===
pristine --selftest rc=0 ; mutant --selftest rc=0
selftest stdout/stderr: identical
62/62 cases passed (hermetic)
VERDICT: PASS

=== (5) instrumented build: does any run reach filesScanned==0 with resolved>0? ===
instrumented runs=635  invariant violations (filesScanned==0 && resolved>0)=0

SUMMARY: total differing runs = 0
SUMMARY: states with filesScanned==0 and resolved>0 = 0
PROBE RESULT: no input found that separates pristine from mutant
```

Phase 1 (hand-built battery) — all 96 paired runs `identical`; the interesting rows:

```
s1_empty_scan_set      --json             identical  filesScanned=0 resolved=0 error=0 warn=0 verdict=FAIL
s3_prose_only          --json             identical  filesScanned=1 resolved=0 error=0 warn=0 verdict=FAIL
s4_resolves_one        --json             identical  filesScanned=1 resolved=1 error=0 warn=0 verdict=PASS
s5_resolves_and_drifts --json             identical  filesScanned=1 resolved=1 error=1 warn=0 verdict=FAIL
s6_unreadable_only     --json             identical  filesScanned=0 resolved=0 error=0 warn=0 verdict=FAIL
s7_unreadable_plus_good --json             identical  filesScanned=1 resolved=1 error=0 warn=0 verdict=PASS
s12_dir_named_md       --json             identical  filesScanned=0 resolved=0 error=0 warn=0 verdict=FAIL
s14_runtime_plus_real  --json             identical  filesScanned=1 resolved=2 error=0 warn=0 verdict=PASS
s15_skill_is_dir       --json             identical  filesScanned=0 resolved=0 error=0 warn=0 verdict=FAIL
s16_skill_unreadable   --json             identical  filesScanned=0 resolved=0 error=0 warn=0 verdict=FAIL
```

(16 scenarios × 6 flag sets; every row `identical`; the full listing was produced and shows no `DIFFERENT` and no `COUNTEREXAMPLE` marker.)

Exotic pass — 7 additional trees × 2 flag sets, 14 paired runs, 0 differences:

```
x_symlink      --json           identical  "verdict": "FAIL"
x_fifo         --json           identical  "verdict": "FAIL"
x_binary       --json           identical  "verdict": "FAIL"
x_fenced       --json           identical  "verdict": "FAIL"
x_bom          --json           identical  "verdict": "FAIL"
x_emptyfile    --json           identical  "verdict": "FAIL"
x_big          --json           identical  "verdict": "FAIL"
...
exotic diffs=0
```

### 4.2 The two binaries, side by side (verbatim)

True empty scan set (`--self` has neither `SKILL.md` nor `corpus/`):

```
########## TRUE EMPTY SCAN SET (no SKILL.md, no corpus/) ##########
--- pristine ---
  filesScanned=0 docs=0 tokens=0 refs=0 symbols=0 findings=0
VERDICT: FAIL
CITE_CHECK: DRIFT (environment: empty-scan-set)
rc=2
--- mutant ---
  filesScanned=0 docs=0 tokens=0 refs=0 symbols=0 findings=0
VERDICT: FAIL
CITE_CHECK: DRIFT (environment: empty-scan-set)
rc=2

--- JSON verdict field ---
pristine: verdict=FAIL filesScanned=0 resolved=0
mutant: verdict=FAIL filesScanned=0 resolved=0
```

Prose-only doc (`filesScanned=1`, `resolved=0`) — the state the dropped guard was supposed to catch:

```
########## pristine  --self empty ##########
  filesScanned=1 docs=1 tokens=0 refs=0 symbols=0 findings=0
VERDICT: FAIL
CITE_CHECK: DRIFT (environment: zero-resolutions)
rc=2
########## mutant  --self empty ##########
  filesScanned=1 docs=1 tokens=0 refs=0 symbols=0 findings=0
VERDICT: FAIL
CITE_CHECK: DRIFT (environment: zero-resolutions)
rc=2
```

One resolvable citation (`filesScanned=1`, `resolved=1`) — the surviving guard alone decides:

```
########## pristine  --self one ##########
  filesScanned=1 docs=1 tokens=1 refs=0 symbols=0 findings=1
VERDICT: PASS
CITE_CHECK: CLEAN (files=1 tokens=1 errors=0 warnings=0)
rc=0
########## mutant  --self one ##########
  filesScanned=1 docs=1 tokens=1 refs=0 symbols=0 findings=1
VERDICT: PASS
CITE_CHECK: CLEAN (files=1 tokens=1 errors=0 warnings=0)
rc=0
```

---

## 5. Argument that no input can tell them apart

Three independent legs, all pointing the same way.

**(a) The verdict expressions are logically equal on every reachable state.**
`runCheck()` increments `totals.filesScanned` at line 1556 and `totals.resolved` at line 1583 — both inside the single `for (const rel of docs)` loop, with 1556 strictly before 1583 and the `catch { continue; }` on 1556 skipping both. `totals.resolved` is written nowhere else in the file (`grep` confirms three hits: the initializer at 1549, the increment at 1583, and the reads at 1590/1626/2527/2528). Hence `resolved > 0 ⟹ filesScanned > 0`, so `filesScanned > 0 && resolved > 0` ≡ `resolved > 0`. The mutant's predicate is the pristine's predicate, identically.

**(b) The disagreeing state is unreachable.** `filesScanned == 0 && resolved > 0` would require a resolved citation in a document that was never counted as scanned — impossible, since the only source of `resolved` is the `OK` findings of a document whose `filesScanned++` already ran. The instrumented build, which aborts on exactly that state, was run over 635 distinct invocations (16 hand-built trees + 300 fuzz trees + the full 75-document pinned kumitate tree, each with two flag sets, plus `--selftest`) and produced **0** `INVARIANT_VIOLATION`s.

**(c) Empirically, the two binaries are byte-identical.** Across 96 + 600 + 14 + 2 (pinned tree) paired CLI runs, comparing `(exit status, stdout bytes, stderr bytes)`: **0 differences**. On the full pinned kumitate tree the two JSON reports and the two stderr streams are byte-identical (`cmp -s` clean, `filesScanned=75 resolved=1679`). The pinned hermetic suite returns `rc=0` and `62/62 cases passed` on both, with identical output after masking the suite's two known nondeterministic fields (the fixture repo's fresh `HEAD` sha and the `mkdtemp` name — I confirmed the pristine binary differs from *itself* run-to-run in exactly those two places, and nowhere else).

**Conclusion:** S_EMPTY_GUARD is an **equivalent mutant**. The dropped guard is co-extensive with the surviving one, not merely unasserted by the suite. This is a stronger statement than "the suite has no case for it" — no oracle on any input can kill it.

---

## 6. Consequences for the round-26 ledger (advisory only — no files changed)

- The sweep's `PREDICT SURVIVED` for S_EMPTY_GUARD held, and the reason is now pinned to a code invariant rather than to a suite gap. A reader should not read this survivor as "an untested hole"; it is a no-op edit.
- If the lane wants a *hole-aimed* survivor class, the useful next question is whether the other four survivors are also equivalent mutants or genuinely unasserted behaviour. This probe says nothing about S_OOR_EDGE, S_STRICT, S_USAGE, S_PIN_INCLUDES.
- The `filesScanned` counter is nonetheless worth keeping in the report: `renderText` (line 1626) and `main` (lines 2527–2528) use it for the `empty-scan-set` / `zero-resolutions` environment diagnostics, so the counter is load-bearing even though that particular *verdict* conjunct is not.

---

## 7. Lane compliance

- Files written: **this report only**, at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md`. Nothing else in the lane was created, edited or deleted.
- All code execution happened under `/tmp/s_empty_guard/` (plus `/tmp` scratch dirs created by `mktemp`), under `env -i`. The lane tree was never executed in place; no selftest/gate/sweep was run inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Sibling repo `/home/vgpnk/Projects/shokunin/kumitate-shokunin` was read only, via `git show` and `git archive` of the pinned rev. No git write command was issued in the lane or in the sibling. **No `jj` command was run anywhere.**
- Tooling: **no installs or updates were performed.** Node v24.21.0 and git were already present (`node` resolved through fnm at `/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node`; `git` at `/usr/bin/git`); no pacman, `uv tool`, `cargo`, or `npm -g` transaction occurred.
- Sources opened this session: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/cite-check.defects.spec` (read 2026-10-22, quote: *"the verdict drops only the scanned-files guard"*) and the pinned `scripts/cite-check.mjs` bytes at rev `1205c66` (read 2026-10-22, quote: *"const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';"*).
- No subagent was dispatched; no producer-authentication, promotion or numeric-score claim is made.

---

PROBE S_EMPTY_GUARD: EQUIVALENT
