# DraftSkillSurvivors — survivor-class table for `## Ninth recorded case — round 26`

**Seat:** `TameshiR26.DraftSkillSurvivors` (leaf scribe, wave 1 of 2)
**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Target of the table:** the new section `## Ninth recorded case — round 26` at the end of
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md`
**Model:** the round-18 table in `## Eighth recorded case — round 18` (SKILL.md:1918-1923)
**Survivor source:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/sweep/results.tsv`
(5 SURVIVED rows: `S_OOR_EDGE`, `S_STRICT`, `S_EMPTY_GUARD`, `S_USAGE`, `S_PIN_INCLUDES`; 5 KILLED rows are out of scope here)

**Scope note (lane bounds):** this seat writes exactly one file — this report. No lane file
was edited, no `jj` command was run, no git write command was run in the lane, and every
command below ran in `/tmp` scratch. No tool was installed or upgraded this session.

---

## 1. Verdict (first)

1. **Five survivors, five rows; four are suite holes, one is an equivalent mutant.**
   `S_OOR_EDGE`, `S_STRICT`, `S_USAGE`, `S_PIN_INCLUDES` are each distinguished from the
   pristine pin by a hermetic, off-suite input (witnesses in §3). `S_EMPTY_GUARD` is an
   **equivalent mutant**: no input distinguishes it, because `totals.resolved > 0` implies
   `totals.filesScanned > 0` in the pinned code. It is not a hole and must not be counted
   as one.
2. **The fix belongs to kumitate for the four holes** — the suite that fails to pin them is
   kumitate's own `scripts/cite-check.mjs` hermetic group. `S_EMPTY_GUARD` has no fix
   anywhere: there is nothing to add to the suite that could kill it.
3. **Every row is justified by a pinned-byte line number** (§4) and by a witness I ran
   myself against the recorded mutant SHAs (§2, §3). The five mutant SHA256s I rebuilt
   from the pinned bytes are byte-identical to `results.tsv`, so my witnesses are witnesses
   *for the recorded mutants*, not for look-alikes.

### Drafted table (fenced; for the L1 to integrate into SKILL.md)

Place immediately after the existing `## Ninth recorded case — round 26` lead paragraph and
before `### Round-26 gate/probe registry — report interop`. Column headers and order copy
the round-18 table (SKILL.md:1918-1919) exactly: `Survivor class in this case` /
`What the suite does not pin` / `Fix belongs to`.

```markdown
| Survivor class in this case | What the suite does not pin | Fix belongs to |
|---|---|---|
| line-range edge (`S_OOR_EDGE`) | a citation of exactly line n+1 (n = the target file's line count): the only out-of-range fixture cites `:999` of a 20-line file, so the one-line widening of the range check is invisible | kumitate |
| strict threshold (`S_STRICT`) | the warn-promotion threshold under `--strict` — one warn must drift; the base fixture always carries errors, so `totals.error > 0` short-circuits the promote and no case asserts a one-warning clean run | kumitate |
| usage exit (`S_USAGE`) | the exit code of an unknown flag (the documented usage code 64): no hermetic case passes an unknown flag | kumitate |
| compare direction (`S_PIN_INCLUDES`) | a content pin that is an interior slice of the digest: the suite's pin hexes are a prefix of the digest and an unrelated hex, so a substring compare still reports `PIN_MISMATCH` | kumitate |
| redundant verdict guard (`S_EMPTY_GUARD`) | nothing — `totals.resolved > 0` implies `totals.filesScanned > 0`, so the dropped conjunct is equivalent code and no input can separate the two programs | no one: equivalent mutant — record it as equivalent, do not count it as a hole and do not open a fix |
```

---

## 2. Provenance: the mutants I probed are the recorded mutants

Pinned bytes read out of the sibling repo's object store (read-only):

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs \
    > /tmp/tameshi-r26-draftskill/cite-check.mjs
$ sha256sum /tmp/tameshi-r26-draftskill/cite-check.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/tameshi-r26-draftskill/cite-check.mjs
$ wc -l /tmp/tameshi-r26-draftskill/cite-check.mjs
2537 /tmp/tameshi-r26-draftskill/cite-check.mjs
```

Blob sha256 and line count match the pin in
`.ufo/evidence/round-26/cite-check/predictions.json` (`pin_sha256`, `1205c662…`) and the spec
header (`.ufo/evidence/round-26/cite-check/cite-check.defects.spec:2`).

Each of the five survivors was rebuilt from the pinned bytes by applying the spec's exact
`@old` → `@new` string (one occurrence asserted per edit):

```
$ cd /tmp/tameshi-r26-draftskill/work
$ python3 - <<'PY'   # one literal replace per mutant, count(old)==1 asserted
... PY
old occurrences: 1
$ sha256sum *.mjs
949c29035366702b3e93ca9d8ed5a6df25275f104ebe72490a7cc11893bea5d5  S_EMPTY_GUARD.mjs
f1b41c7f59c030111a134c85433b238eab03214ada4746dd7c3b9ac156efb093  S_OOR_EDGE.mjs
206a7f94a948dd98c8f92c3e77b50a47aba20d1356d2e6b7c3ae6efe8387c0bc  S_PIN_INCLUDES.mjs
caf4d03911d7cc0ef301612f96c3f2c8d0083fab7cc5921017ebf061525fb921  S_STRICT.mjs
0ec5fff61e3c91e13a3b87b71106921633ebdf107e2e6fbb33a018cddfe3afcd  S_USAGE.mjs
```

Each rebuilt SHA256 is byte-identical to the `mutant-sha256` column of
`.ufo/evidence/round-26/cite-check/sweep/results.tsv` (rows 6-10). The sweep verdicts also
reproduce under the recorded hermetic form (`env -i … node "$MUTANT" --selftest`,
`tools/mutate-and-run.sh:1426`):

```
$ for s in S_OOR_EDGE S_STRICT S_EMPTY_GUARD S_USAGE S_PIN_INCLUDES pristine; do
    env -i PATH=/usr/bin:/bin HOME=/tmp/tameshi-r26-draftskill/nohome \
        TMPDIR=/tmp/tameshi-r26-draftskill/nohome/tmp LC_ALL=C \
        /home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node \
        $s.mjs --selftest >$s.selftest.out 2>&1; echo "$s selftest exit=$?"; done
S_OOR_EDGE selftest exit=0 | 62/62 cases passed (hermetic) VERDICT: PASS
S_STRICT selftest exit=0 | 62/62 cases passed (hermetic) VERDICT: PASS
S_EMPTY_GUARD selftest exit=0 | 62/62 cases passed (hermetic) VERDICT: PASS
S_USAGE selftest exit=0 | 62/62 cases passed (hermetic) VERDICT: PASS
S_PIN_INCLUDES selftest exit=0 | 62/62 cases passed (hermetic) VERDICT: PASS
pristine selftest exit=0 | 62/62 cases passed (hermetic) VERDICT: PASS
```

(Node v24.21.0; all runs under `/tmp`. Nothing was executed inside the lane tree.)

---

## 3. Witnesses, one per survivor

### 3.1 `S_OOR_EDGE` — line-range edge (hole)

Edit site: pinned `cite-check.mjs:1312`
`const bad = ref.start > n || ref.end > n;` → `ref.start > n + 1 || ref.end > n + 1`.
`n` is `countLines(target)` (pinned `:336-340`).

Fixture (hermetic, `/tmp`): a 20-line `src/scripts/real.mjs` and a `SKILL.md` citing
exactly line **21 = n+1**.

```
$ N=/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N pristine.mjs \
    --src w/oor/src --self w/oor/self --fleet w/oor
  SKILL.md:1  ERROR LINE_OOR  [source/src] scripts/real.mjs:21 — scripts/real.mjs:21 out of range — scripts/real.mjs has 20 lines
  byKind={"LINE_OOR":1,"OK":1}
CITE_CHECK: DRIFT (files=1 tokens=2 errors=1 warnings=0)
pristine exit=1
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N S_OOR_EDGE.mjs \
    --src w/oor/src --self w/oor/self --fleet w/oor
CITE_CHECK: CLEAN (files=1 tokens=2 errors=0 warnings=0)
mutant exit=0
```

**Distinguished.** Why the suite misses it: the suite's only `LINE_OOR` fixture cites
`:999` of a 20-line file — `cite-check.mjs:1656` writes the 20-line `scripts/real.mjs`,
`:1684` writes `Out-of-range ref: \`scripts/real.mjs:999\``, and the case at `:1883-1887`
asserts only that a `LINE_OOR` finding exists for `:999`. n+1 is never cited.

### 3.2 `S_STRICT` — strict threshold (hole)

Edit site: pinned `cite-check.mjs:1589`
`const drift = totals.error > 0 || (opts.strict && totals.warn > 0);` → `totals.warn > 1`.

Fixture: one doc with exactly **one** warn finding (`ORPHAN_REF`, severity `warn` per
pinned `:221`) and no errors, scanned with `--strict`.

```
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N pristine.mjs --strict \
    --src w/strict3/src --self w/strict3/self --fleet w/strict3
  SKILL.md:1  WARN  ORPHAN_REF  [source/none] :424242 — :424242 has no owning path token in SKILL.md (no sticky owner yet)
  bySeverity={"warn":1,"note":1}
CITE_CHECK: DRIFT (files=1 tokens=2 errors=0 warnings=1)
pristine exit=1
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N S_STRICT.mjs --strict \
    --src w/strict3/src --self w/strict3/self --fleet w/strict3
  bySeverity={"warn":1,"note":1}
CITE_CHECK: CLEAN (files=1 tokens=2 errors=0 warnings=1)
mutant exit=0
```

**Distinguished.** Why the suite misses it: `opts.strict` defaults to `false`
(pinned `:250`) and is set only by `--strict` (pinned `:264`); the hermetic `run()` helper
passes the suite's own `base` (pinned `:1859`), and no case in the 62-case hermetic group
runs the gate with `strict: true`. Stronger point I measured — even adding `--strict` to
the *suite invocation* does not kill the mutant, because the base fixture always carries
errors (the `bogus-path → UNRESOLVED error` case at `:1871-1876` asserts
`rep.verdict === 'FAIL'`), so `totals.error > 0` short-circuits the promote:

```
$ env -i … $N pristine.mjs  --selftest --strict  → exit=0  62/62 cases passed (hermetic) VERDICT: PASS
$ env -i … $N S_STRICT.mjs --selftest --strict  → exit=0  62/62 cases passed (hermetic) VERDICT: PASS
```

A dedicated one-warn / zero-error fixture is required; that is why the fix is kumitate's.

### 3.3 `S_USAGE` — usage exit (hole)

Edit site: pinned `cite-check.mjs:2512` (`return 64;` → `return 65;`), reached from
`main()`'s `parseArgs` catch (pinned `:2510-2513`). The usage code 64 is a documented
contract in the file header (pinned `:71` — "64 usage error").

```
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N pristine.mjs --bogus-flag >/dev/null 2>&1
pristine exit=64
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N S_USAGE.mjs --bogus-flag >/dev/null 2>&1
mutant exit=65
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N pristine.mjs --help >/dev/null 2>&1
pristine help exit=0
```

**Distinguished.** Why the suite misses it: the suite only ever spawns the gate with valid
flags — the two child-process cases use `--json --self … --fleet …` (pinned `:2310`) and
`--self … --fleet …` (pinned `:2338`). `parseArgs` throws only on an unknown argument
(pinned `:270`) or a missing directory value (pinned `:254-256`), so no hermetic case ever
reaches the `return 64` line. Note the suite already has the shape of the missing case: the
fail-closed child case asserts `r.status === 2` (pinned `:2342`), so a sibling case for
status 64 on an unknown flag is a one-line addition on kumitate's side.

### 3.4 `S_PIN_INCLUDES` — compare direction (hole)

Edit site: pinned `cite-check.mjs:1195` (in the `sha256`-kind branch of `pinFindings`)
`} else if (digest.startsWith(pin.hex)) {` → `digest.includes(pin.hex)`.
`digest` is the sha256 of the cited file (pinned `:1187`); `pin.hex` is the 7-40 hex
payload of a `sha256`-kind pin (pinned `:1116-1133`).

Fixture: the pin hex is an **interior slice** of the real digest
(`digest[20:32] = 03c2a0027143`, and `digest.startswith('03c2a0027143')` is `False`).

```
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N pristine.mjs \
    --src w/pin/src --self w/pin/self --fleet w/pin
  SKILL.md:3  ERROR PIN_MISMATCH  [source/src] 03c2a0027143 — content pin 03c2a0027143 does not match sha256(scripts/real.mjs)=6a223213b06a…
  byKind={"OK":1,"PIN_MISMATCH":1}
CITE_CHECK: DRIFT (files=1 tokens=1 errors=1 warnings=0)
pristine exit=1
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N S_PIN_INCLUDES.mjs \
    --src w/pin/src --self w/pin/self --fleet w/pin
  byKind={"OK":2}
CITE_CHECK: CLEAN (files=1 tokens=1 errors=0 warnings=0)
mutant exit=0
```

**Distinguished.** Why the suite misses it: the suite's content-pin fixtures are a
*prefix* of the digest (`digest.slice(0, 10)`, pinned `:1686`) and an unrelated hex
(`0123456789ab`, pinned `:1687`), and the case at `:1895-1900` asserts only that a match
and a `PIN_MISMATCH` both appear. I confirmed `0123456789ab` is **not** a substring of the
fixture digest (`6a223213b06ad46fd10a03c2a00271436edc1d038a2e1fcd16c5ab505334194f`), so a
substring compare still reports the mismatch. Extra observation worth carrying into the
entry: the mutant widens only the `sha256`-marked branch — the rev-kind content fallback
at pinned `:1219` still uses `startsWith`, so the mutant introduces an asymmetry between
the two content-pin paths.

### 3.5 `S_EMPTY_GUARD` — equivalent mutant (NOT a hole)

Edit site: pinned `cite-check.mjs:1590`
`const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';`
→ `const verdict = totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';`

Observed: no input separates the two programs. Empty-scan-set fixture:

```
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N pristine.mjs --src w/empty/src --self w/empty/self --fleet w/empty
  VERDICT: FAIL
  CITE_CHECK: DRIFT (environment: empty-scan-set)
  cite-check: fail-closed — empty scan set under …/w/empty/self
exit=2
$ env -i HOME=/tmp/tameshi-r26-draftskill/nohome $N S_EMPTY_GUARD.mjs --src w/empty/src --self w/empty/self --fleet w/empty
  VERDICT: FAIL
  CITE_CHECK: DRIFT (environment: empty-scan-set)
  cite-check: fail-closed — empty scan set under …/w/empty/self
exit=2
```

Byte-identical behaviour, and the reason is structural, not a gap in my search:

* `totals.filesScanned++` (pinned `:1556`) happens inside the per-document loop, **before**
  `analyzeDoc` runs.
* `totals.resolved++` (pinned `:1583`) happens inside that same loop iteration, over the
  findings that `analyzeDoc` returned for that document.
* Therefore `totals.resolved > 0` ⇒ at least one document was scanned ⇒
  `totals.filesScanned > 0`. The dropped conjunct is **implied** by the surviving one.

So the pristine predicate `filesScanned > 0 && resolved > 0` and the mutant predicate
`resolved > 0` are logically equivalent over every input, not merely over the fixture set.
The mutant changes no observable output anywhere:

* `report.verdict` — identical by the implication above.
* `report.citeCheck` (`CLEAN`/`DRIFT`, pinned `:1594`) — derived from the same verdict.
* `main()`'s exit code (pinned `:2530`) — derived from the same verdict.
* `main()`'s fail-closed arm (pinned `:2527-2529`) — reads `report.totals.filesScanned`
  and `report.totals.resolved` **directly**, not the verdict, so the exit-2 empty-scan-set
  path is untouched by the edit.

**Conclusion: no oracle on this input space can kill `S_EMPTY_GUARD`.** It must be recorded
as an equivalent mutant in the corpus entry and must not be counted as a suite hole, and it
must not be counted as a "fix belongs to kumitate" item — no case added to kumitate's
suite can change its fate. (Consistent with the sibling probe `ProbeSEMPTYGUARD` in
`.ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md`, which reaches the same verdict.)

---

## 4. Per-row justification, pinned-byte line numbers

All line numbers are on kumitate `scripts/cite-check.mjs` at rev
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` (blob sha256 `40573448…c10c9f`, 2537 lines).

| Survivor | Mutated site | What the suite does / does not reach | Hermetic case that would kill it |
|---|---|---|---|
| `S_OOR_EDGE` | `:1312` `const bad = ref.start > n \|\| ref.end > n;` | the only `LINE_OOR` case is `:1883-1887` (fixture `:1684`, target `:1656`), citing `:999` of a 20-line file; n+1 is never cited | a fixture citing `:21` of that 20-line file, asserting `LINE_OOR` |
| `S_STRICT` | `:1589` `opts.strict && totals.warn > 0` | `strict` defaults false (`:250`), set only by `--strict` (`:264`); no hermetic case runs strict; the base fixture always has errors so `totals.error > 0` (`:1589`) masks the threshold | a `--strict` case over a fixture with exactly one warn and zero errors, asserting `FAIL` |
| `S_USAGE` | `:2512` `return 64;` (from `main()`'s parse catch `:2510-2513`; contract documented at `:71`) | the suite spawns the gate only with valid flags (`:2310`, `:2338`); `parseArgs` throws only at `:270`/`:254-256` | a child-process case with an unknown flag asserting `r.status === 64` (the shape exists at `:2342` for status 2) |
| `S_PIN_INCLUDES` | `:1195` `digest.startsWith(pin.hex)` (sha256-kind branch; rev-kind fallback `:1219` untouched) | the suite's pin hexes are a digest prefix (`:1686`) and an unrelated hex (`:1687`); the case `:1895-1900` asserts only "a match and a mismatch exist" | a fixture whose `sha256` pin is an interior slice of the digest, asserting `PIN_MISMATCH` |
| `S_EMPTY_GUARD` | `:1590` verdict predicate | `resolved` (`:1583`) can only increment inside the loop that already incremented `filesScanned` (`:1556`) ⇒ implied; the suite's empty-scan-set case (`:1964-1969`) therefore cannot see the drop | **none exists** — equivalent mutant |

---

## 5. Placement and shape notes for the L1

* Round-18's table is SKILL.md:1918-1923 and has exactly three columns
  (`Survivor class in this case` / `What the suite does not pin` / `Fix belongs to`) and
  four rows for five survivors (it merges `S_DUP_LINE` and `S_ENTRY_COUNT`). The drafted
  table above keeps round-18's headers and order verbatim but uses **one row per survivor**
  (5 rows), as the task specifies.
* Round-18's third column is uniformly `kumitate`. Here it is `kumitate` for the four
  holes and explicitly "no one / equivalent mutant" for the fifth — a divergence from the
  round-18 precedent, flagged rather than smoothed over, because the fifth row has no
  fix to route.
* **Working-tree conflict (verbatim, for the canonical judge):** the lane's SKILL.md is
  already modified in the working tree (uncommitted; `git status --porcelain -- SKILL.md`
  → ` M SKILL.md`) and that modification already carries a survivor table with a
  **different third column** and different wording:

  ```
  | Survivor class in this case | What the suite does not pin | Decision |
  |---|---|---|
  | line-range edge (`S_OOR_EDGE`) | a citation of exactly line n+1 | hole; fix belongs to kumitate |
  | strict threshold (`S_STRICT`) | any `--strict` run (one warning must drift) | hole; kumitate |
  | usage exit (`S_USAGE`) | the exit code of an unknown flag | hole; kumitate |
  | compare direction (`S_PIN_INCLUDES`) | a pin that is an interior slice of the digest | hole; kumitate |
  | redundant guard (`S_EMPTY_GUARD`) | nothing: equivalent code | keep it a survivor in the table and the score (Stryker cannot mark equivalents, S089); name it equivalent in the entry; do not count it as a hole |
  ```

  My draft follows the **round-18 shape** the task names (third column `Fix belongs to`),
  and its substance agrees with that working-tree text on all five rows (four holes, one
  equivalent mutant). The L1 owns the merge; I did not touch the file.
* The neighbouring claim in that same working-tree paragraph — "the non-hermetic
  `--integrations` group kills none of the five and is red at the pristine pin on live
  trees" — I did **not** re-measure (it needs the live kumitate tree, which is outside
  this seat's scope). I neither confirm nor contradict it.

## 6. Out of scope / not done

* No lane file written except this report; no `jj` command; no git write command in the
  lane; the sibling repo `kumitate-shokunin` was read through `git show` only.
* The 5 KILLED defects and the kill-rate ledger are other seats' records; not re-derived
  here beyond confirming the recorded mutant SHAs and the 5/5 SURVIVED verdicts.
* No tool installed or upgraded (no pacman / uv / npm / cargo transaction this session).
