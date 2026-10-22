# Probe S_PIN_INCLUDES — off-suite falsifier for kumitate `scripts/cite-check.mjs`

**Verdict: the mutant and the pristine pin ARE DISTINGUISHED by a hermetic, off-suite input.**

## 1. What the defect is

`S_PIN_INCLUDES` is a pre-registered hole-aimed mutation on the pinned bytes of
`kumitate-shokunin/scripts/cite-check.mjs` at rev
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`.

Edit (from `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, last
block), applied at pristine line **1195** inside `pinFindings()`:

```js
      } else if (digest.startsWith(pin.hex)) {   // pristine
      } else if (digest.includes(pin.hex)) {     // mutant
```

`digest` is the sha256 of the *cited file* the pin is attached to
(`sha256File(owner.rec.targetPath)`, pristine line 1187); `pin.hex` is the
7–40 hex-character payload of a `sha256`-kind pin (`collectPins`, pristine
lines 1116–1133). The pristine pin accepts a content pin only when the pin hex
is a **prefix** of the file digest; the mutant accepts it when the pin hex
appears **anywhere inside** the digest.

The pre-registration predicted `SURVIVED` because the hermetic suite's only
content-pin fixtures are a prefix hex (`digest.slice(0, 10)`, pristine line
1686) and an unrelated hex (`0123456789ab`, pristine line 1687). Neither hex is
an *interior* substring of the real digest, so a substring compare still
reports `PIN_MISMATCH` and the suite cannot see the widening
(`predictions.json` → `S_PIN_INCLUDES.reason`).

## 2. Materialization of the pin and the mutant

Both files were built in the `/tmp` scratch dir `/tmp/spininc`, never in the
lane tree.

```
$ mkdir -p /tmp/spininc
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/spininc/cite-check.pristine.mjs
$ sha256sum /tmp/spininc/cite-check.pristine.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/spininc/cite-check.pristine.mjs
$ wc -l /tmp/spininc/cite-check.pristine.mjs
2537 /tmp/spininc/cite-check.pristine.mjs
```

The sha256 matches the frozen pin recorded in
`.ufo/evidence/round-26/cite-check/predictions.json`
(`"pin_sha256": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"`)
and the spec header line 2; the line count matches the spec's `2537 lines`.

The mutant was produced by a single exact-string replacement, asserted to
occur exactly once (the spec's own guarantee: "Each @old occurs exactly once in
the pinned bytes"):

```python
p = '/tmp/spininc/cite-check.mutant.mjs'
s = open(p).read()
old = "      } else if (digest.startsWith(pin.hex)) {"
new = "      } else if (digest.includes(pin.hex)) {"
assert s.count(old) == 1, s.count(old)
open(p, 'w').write(s.replace(old, new))
```

Observed:

```
mutant patched: 1 occurrence
```

Diff between the two materialized files (the only byte difference):

```
$ diff -u /tmp/spininc/cite-check.pristine.mjs /tmp/spininc/cite-check.mutant.mjs
--- cite-check.pristine.mjs	2026-10-22 07:56:48.465238515 -0300
+++ cite-check.mutant.mjs	2026-10-22 07:56:48.472743873 -0300
@@ -1192,7 +1192,7 @@
           severity: 'note', target: pin.hex, via: 'pin',
           message: `content pin ${pin.hex} could not be verified (unreadable ${owner.rec.target})`,
         });
-      } else if (digest.startsWith(pin.hex)) {
+      } else if (digest.includes(pin.hex)) {
         counters.pinsOk++;
         out.push({
           file: rel, line, token: pin.hex, class: 'source', rung: 'src', kind: 'OK',
```

The rev-kind branch at pristine line 1219 still uses `digest.startsWith(...)`
and was **not** touched — only the `sha256`-kind branch changed, exactly as
the spec's `@old`/`@new` dictate.

## 3. The discriminating input

The distinguishing artifact is a **sha256 pin whose hex sits inside, not at the
start of, the cited file digest**. The probe:

1. writes a small target file `src/scripts/target.mjs`;
2. computes its sha256;
3. takes a **12-hex-character interior slice** (offset 8..20) of that digest as
   the pin hex;
4. writes a doc that cites `scripts/target.mjs` (so the pin has a resolved
   owner to hash) and then states `sha256 \`<interior slice>\``.

Pristine: `digest.startsWith(interior)` is **false** → `PIN_MISMATCH`
(severity `error`, pinned line 222) → verdict FAIL, exit 1.
Mutant: `digest.includes(interior)` is **true** → `OK` (severity `note`) →
verdict PASS, exit 0.

The hash arithmetic is explicit in the probe output:

```
digest      = 87008132b3dc10b44f143a9243206a2dd490cfebf793e2ecd9aa65a61a90f40a
pin hex     = b3dc10b44f14  (offset 8..20 of the digest)
startsWith  = false   includes = true
```

## 4. The probe

Hermetic by construction: it builds its own temp tree, runs both binaries with
`env -i` (empty environment), redirects `HOME` into a scratch dir, and never
touches the lane tree, the fleet root, or any sibling lane. It drives the
**public CLI** (`--src/--self`), not `--selftest`.

`/tmp/spininc/probe.sh`:

```bash
#!/usr/bin/env bash
# S_PIN_INCLUDES off-suite probe (round-26 C1 survivor probe).
# Hermetic: builds its own temp tree, runs pristine and mutant with `env -i`.
set -euo pipefail

SCRATCH="${SCRATCH:-/tmp/spininc}"
NODE_BIN="$(command -v node)"
NODE_DIR="$(dirname "$NODE_BIN")"
REPO=/home/vgpnk/Projects/shokunin/kumitate-shokunin
REV=1205c6621a2eccbb8ffceae86d9e7b79a7990b3a

rm -rf "$SCRATCH/tree"
mkdir -p "$SCRATCH/tree/src/scripts" "$SCRATCH/tree/self/corpus/knowledge" "$SCRATCH/home"

# 1. pristine pin bytes
git -C "$REPO" show "$REV:scripts/cite-check.mjs" > "$SCRATCH/cite-check.pristine.mjs"
cp "$SCRATCH/cite-check.pristine.mjs" "$SCRATCH/cite-check.mutant.mjs"

# 2. the single @old/@new edit from cite-check.defects.spec
python3 - "$SCRATCH/cite-check.mutant.mjs" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
old = "      } else if (digest.startsWith(pin.hex)) {"
new = "      } else if (digest.includes(pin.hex)) {"
assert s.count(old) == 1, s.count(old)
open(p, 'w').write(s.replace(old, new))
print("mutant patched: 1 occurrence")
PY

# 3. target file + a pin whose hex sits INSIDE the digest, not at its start
printf '// target file for S_PIN_INCLUDES probe\nexport const A = 1;\n' > "$SCRATCH/tree/src/scripts/target.mjs"
node -e '
const {createHash} = require("crypto"), fs = require("fs");
const d = createHash("sha256").update(fs.readFileSync(process.argv[1])).digest("hex");
const hex = d.slice(8, 20);                       // interior 12 hex chars
console.log("digest      = " + d);
console.log("pin hex     = " + hex + "  (offset 8..20 of the digest)");
console.log("startsWith  = " + d.startsWith(hex) + "   includes = " + d.includes(hex));
fs.writeFileSync(process.argv[2],
  "# S_PIN_INCLUDES off-suite probe\n\n" +
  "The cited file is `scripts/target.mjs`; its content pin is sha256 `" + hex + "`.\n");
' "$SCRATCH/tree/src/scripts/target.mjs" "$SCRATCH/tree/self/corpus/knowledge/pin.md"

# 4. run both, hermetically
for v in pristine mutant; do
  env -i PATH="$NODE_DIR:/usr/bin:/bin" HOME="$SCRATCH/home" \
    node "$SCRATCH/cite-check.$v.mjs" --src "$SCRATCH/tree/src" --self "$SCRATCH/tree/self" --json \
    > "$SCRATCH/$v.json" 2> "$SCRATCH/$v.err" && rc=0 || rc=$?
  echo "--- $v: exit=$rc"
  node -e '
    const r = require(process.argv[1]);
    const f = r.files.flatMap(f => f.findings).filter(f => f.via === "pin");
    for (const x of f) console.log(`    pin ${x.token} -> ${x.kind}/${x.severity}: ${x.message}`);
    console.log(`    verdict=${r.verdict} error=${r.totals.error} pinsOk=${r.totals.pinsOk} pinsMismatch=${r.totals.pinsMismatch}`);
  ' "$SCRATCH/$v.json"
done
```

The probe doc it materializes (`tree/self/corpus/knowledge/pin.md`):

```markdown
# S_PIN_INCLUDES off-suite probe

The cited file is `scripts/target.mjs`; its content pin is sha256 `b3dc10b44f14`.
```

The citation `scripts/target.mjs` is what gives the pin an owner: `ownerAt()`
(pristine lines 1522–1528) returns the nearest preceding **resolved** file
citation, and `pinFindings` hashes `owner.rec.targetPath`. Without that
citation the pin would be `PIN_UNTYPED` (unchecked) and the two binaries would
agree.

### Observed output — the probe run

```
$ bash /tmp/spininc/probe.sh
mutant patched: 1 occurrence
digest      = 87008132b3dc10b44f143a9243206a2dd490cfebf793e2ecd9aa65a61a90f40a
pin hex     = b3dc10b44f14  (offset 8..20 of the digest)
startsWith  = false   includes = true
--- pristine: exit=1
    pin b3dc10b44f14 -> PIN_MISMATCH/error: content pin b3dc10b44f14 does not match sha256(scripts/target.mjs)=87008132b3dc…
    verdict=FAIL error=1 pinsOk=0 pinsMismatch=1
--- mutant: exit=0
    pin b3dc10b44f14 -> OK/note: content pin b3dc10b44f14 matches sha256(scripts/target.mjs)
    verdict=PASS error=0 pinsOk=1 pinsMismatch=0
```

Both stderr files are empty (`pristine.err`, `mutant.err` are 0 bytes).

### Observed output — text mode, pristine

```
$ cd /tmp/spininc && env -i PATH="$NODE_DIR:/usr/bin:/bin" HOME=/tmp/spininc/home \
    node cite-check.pristine.mjs --src tree/src --self tree/self
kumitate cite-check — kumitate-cite-check-v1
src=/tmp/spininc/tree/src (index 1 files)
self=/tmp/spininc/tree/self  fleet=/tmp/spininc/tree
mode:

corpus/knowledge/pin.md
  corpus/knowledge/pin.md:3  ERROR PIN_MISMATCH      [source/src] b3dc10b44f14 — content pin b3dc10b44f14 does not match sha256(scripts/target.mjs)=87008132b3dc…

totals
  filesScanned=1 docs=1 tokens=1 refs=0 symbols=0 findings=2
  orphanRefs=0 altOwnerRefs=0 declarations=0
  bySeverity={"error":1,"note":1}
  byClass={"source":2}
  byKind={"PIN_MISMATCH":1,"OK":1}
  byRung={"src":2}
  pins=1 ok=0 mismatch=1 untyped=0 revUnknown=0 unchecked=0
  indexFiles=1 selfIndexFiles=1 fleetIndexFiles=2
VERDICT: FAIL
CITE_CHECK: DRIFT (files=1 tokens=1 errors=1 warnings=0)
----- exit: 1 -----
```

### Observed output — text mode, mutant

```
$ cd /tmp/spininc && env -i PATH="$NODEDIR:/usr/bin:/bin" HOME=/tmp/spininc/home \
    node cite-check.mutant.mjs --src tree/src --self tree/self
kumitate cite-check — kumitate-cite-check-v1
src=/tmp/spininc/tree/src (index 1 files)
self=/tmp/spininc/tree/self  fleet=/tmp/spininc/tree
mode:

totals
  filesScanned=1 docs=1 tokens=1 refs=0 symbols=0 findings=2
  orphanRefs=0 altOwnerRefs=0 declarations=0
  bySeverity={"note":2}
  byClass={"source":2}
  byKind={"OK":2}
  byRung={"src":2}
  pins=1 ok=1 mismatch=0 untyped=0 revUnknown=0 unchecked=0
  indexFiles=1 selfIndexFiles=1 fleetIndexFiles=2
VERDICT: PASS
CITE_CHECK: CLEAN (files=1 tokens=1 errors=0 warnings=0)
----- exit: 0 -----
```

The two runs differ in three independent observable ways: the
`ERROR PIN_MISMATCH` line (present only in pristine), `VERDICT: FAIL` vs
`VERDICT: PASS`, and the process **exit status 1 vs 0**. The exit status
alone is a sufficient oracle.

## 5. The mutant really is a suite survivor (the probe is off-suite, not a suite re-run)

Both binaries pass the full hermetic suite, so the suite genuinely cannot see
this defect and the probe is the only thing that can:

```
$ env -i PATH="$NODE_DIR:/usr/bin:/bin" HOME=/tmp/spininc/home node /tmp/spininc/cite-check.pristine.mjs --selftest | tail -2
62/62 cases passed (hermetic)
VERDICT: PASS
$ env -i PATH="$NODE_DIR:/usr/bin:/bin" HOME=/tmp/spininc/home node /tmp/spininc/cite-check.mutant.mjs --selftest | tail -2
62/62 cases passed (hermetic)
VERDICT: PASS
```

(`--selftest` was run in the `/tmp` scratch dir, never inside
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.)

## 6. Boundary sweep: the separation is exactly "interior vs prefix"

Sweeping the pin hex's offset inside the same digest (12 hex chars taken from
each offset), same tree, same CLI:

```
offset=0  hex=87008132b3dc  pristine_exit=0  mutant_exit=0   (prefix — both accept)
offset=4  hex=8132b3dc10b4  pristine_exit=1  mutant_exit=0   (interior — separated)
offset=8  hex=b3dc10b44f14  pristine_exit=1  mutant_exit=0   (interior — separated)
offset=16 hex=4f143a924320  pristine_exit=1  mutant_exit=0   (interior — separated)
offset=32 hex=d490cfebf793  pristine_exit=1  mutant_exit=0   (interior — separated)
offset=52 hex=65a61a90f40a  pristine_exit=1  mutant_exit=0   (interior — separated)
absent   hex=abcdef012345  pristine_exit=1  mutant_exit=1   (not in the digest — both reject)
```

Readings:

- offset 0 is the only agreeing **accept** case — the prefix hex, which is
  exactly what the suite already fixtures;
- every **interior** hex separates the two binaries;
- a hex absent from the digest agrees (both report `PIN_MISMATCH`), which is
  the suite's existing `0123456789ab` fixture and the reason the pre-registration
  predicted `SURVIVED`.

So the discriminating input class is precisely: *a valid sha256 pin whose hex
is a contiguous substring of the cited file's digest at an offset > 0*.

## 7. Argument that no input could distinguish them — refuted

There is no such argument. The pre-registration's `SURVIVED` prediction was
about the *suite* (no fixture carries an interior hex), not about the *program*.

Formally: let `D` be the 64-hex digest of the cited file and `h` the pin hex.
The pristine pin reports `OK` iff `D.startsWith(h)`; the mutant reports `OK`
iff `D.includes(h)`. For any `h` that occurs in `D` at some offset `k > 0` and
does not also occur at offset 0 (e.g. `h = D[8..20]`, verified by
`D.startsWith(h) === false` and `D.includes(h) === true` in the probe output),
the two predicates disagree. The probe exhibits exactly such an `h`, together
with a resolved owner citation so the pin is actually hashed, and the two
binaries return different verdicts, different severity, and different exit
codes on that single input.

Therefore the two binaries are **not** behaviourally equivalent, and no
equivalence argument can stand. This is a genuine survivor of the registered
hermetic suite, killable only by an off-suite input of the class above.

## 8. Smallest safe correction implied (for the lane's integrator; NOT applied here)

The mutant's own line is the defect. The correct predicate is the pristine one,
`digest.startsWith(pin.hex)` (pristine line 1195): a content pin is a *prefix*
of the file digest by construction, and accepting an interior substring lets
an unrelated 7-hex window of any file's digest masquerade as that file's
identity.

The fixture the suite lacks is a content-pin case whose hex is an **interior**
slice of the fixture file's digest (e.g. `digest.slice(8, 20)`), asserted
`PIN_MISMATCH`/error. Adding it to the hermetic group would kill this mutant
directly. No production file was edited by this seat.

## 9. Environment, tooling, and bounds

- Node: `v24.21.0` (`/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node`).
- **No packages were installed or upgraded by this seat**, so there is no
  install record to report. The probe needed only `node`, `python3`, `printf`
  and `git` (all pre-existing).
- Everything ran under `/tmp/spininc` (scratch). Nothing was executed inside
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Read-only git was used against the sibling lane
  (`git -C .../kumitate-shokunin show <rev>:scripts/cite-check.mjs`); no git
  write command was run in any repo, and **no `jj` command was run anywhere**.
- The probe's own temp tree is a plain directory tree, not a git repo; no
  `git init` was performed by this seat.
- Files written by this seat: this report only. The pristine/mutant/probe
  artifacts live in `/tmp/spininc` and are not lane files.

## 10. Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-26/w1/ProbeSPININCLUDES.md`
  (this report) — the only lane file touched.

PROBE S_PIN_INCLUDES: DISTINGUISHED
