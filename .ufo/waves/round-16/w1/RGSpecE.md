# RGSpecE — C1 defect drafting, class E/G (arms no fixture reaches; behaviour predicates/boundaries)

Seat: TameshiR16.RGSpecE · wave round-16/w1 · lane /home/vgpnk/Projects/shokunin/tameshi-shokunin
Target: kumitate-shokunin `scripts/round-gate.mjs` @ git rev `364f1d5954158ef8844bca4a5fef57b05d2f2ca5`

## Pin verification (observed)

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin \
    show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs \
    > /tmp/tameshi-r16-RGSpecE/round-gate.mjs
$ sha256sum /tmp/tameshi-r16-RGSpecE/round-gate.mjs
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9   # == declared pin
$ wc -l …
1511
```

## Pristine control (allowed once; no mutant was run)

```
$ cd /tmp/tameshi-r16-RGSpecE && node --version → v24.21.0
$ timeout 240 node round-gate.mjs --selftest ; exit=0
PASS  [60/60]  every declared finding kind fires in at least one fixture — 14 kinds observed
ROUND_GATE_SELFTEST: 60/60 pass
VERDICT: PASS   (wall 3.40 s)
```

No mutant was cut or executed — predictions below are pre-registered from the
pinned bytes + corpus/knowledge/arm-class-matrix.md §13 (read lines 298-500) only.

## @old uniqueness (literal `str.count` on the pinned bytes)

| ID | @old | count |
|---|---|---|
| RGE-1 | `  if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(envSrc);` | 1 |
| RGE-2 | `    if (v.startsWith('--')) throw new Error(\`${flag} requires a directory (got ${JSON.stringify(v)})\`);` | 1 |
| RGE-3 | `  if (filed.length < 2) {` | 1 |

(Counted with python3 `blob.count()`; spec fragment at `.ufo/waves/round-16/w1/RGSpecE.spec`.)

## Candidates

### RGE-1 — class E (§13.6 #5): `UFO_SRC` set-value arm — predicted **SURVIVED**

- `@old` `  if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(envSrc);` (target :163)
- `@new` same line with `resolve(envSrc)` → `resolve(SRC_CANDIDATES[0])`.
- **Reason.** The true-branch is dead under the whole suite. `runGate` always
  spawns with `cleanEnv()` (:712-716), which deletes `UFO_SRC` (:711). The only
  set-values anywhere are `UFO_SRC:''` on the three derived-origin runs
  (:1347, :1354, :1369 — fails `envSrc.trim() !== ''`, so the *else* path runs)
  and `UFO_SRC:'/nonexistent/origin'` on the nested spawn (:1390), which always
  carries `--selftest` (:1393); `opts.selftest` skips `resolveSrcDefault`
  (:296) before `main()` dispatches to `selfTest()` (:635). No check can observe
  which expression the dead branch evaluates. Every fixture verdict is
  unchanged → SURVIVED.

### RGE-2 — class E (§13.6 #4 sibling): `dirValue` flag-like guard — predicted **SURVIVED**

- `@old` `    if (v.startsWith('--')) throw new Error(\`${flag} requires a directory (got ${JSON.stringify(v)})\`);` (target :246)
- `@new` predicate weakened to `v.startsWith('---')`.
- **Reason.** This throw only fires when a dir flag's value begins `--`. A grep
  of every `runGate`/nested call shows none: u1 passes bare `--bogus` (:1223,
  rejected at :273), u2/u3 hit the `--round` throws (:1228-1237), u5's `--repo ''`
  exits through the :245 empty guard (:1243-1247), rt8's bogus `--repo` is a plain
  path (:1477), and the nested `--selftest` uses non-flag values (:1392-1394).
  On reached inputs `startsWith('--')` ≡ `startsWith('---')` → SURVIVED.

### RGE-3 — class G (§13.3 NO_FILED_REPORTS threshold, §13.8 boundary): `filed.length < 2 → < 1` — predicted **KILLED**

- `@old` `  if (filed.length < 2) {` (target :535)
- `@new` `  if (filed.length < 1) {`
- **Reason.** The refusal boundary *is* pinned, at rt3 (:1432-1438): fixture
  `tkOne` files exactly one report (rounds `[7]`, :1432), so `filed.length === 1`.
  Pristine: `1 < 2` → `failClosed(… 'NO_FILED_REPORTS' …)`, exit 2, verdict line
  `ROUND_GATE: FAIL-CLOSED (NO_FILED_REPORTS) … filed=1 …` — both regexes in the
  assert (:1435-1436) match. Mutant: `1 < 1` false → `filed.slice(0, -1)` is `[]`
  (:544), `summarize([])` → `CLEAN`, exit 0 with no findings; the check's
  `rt3.status === 2` fails → suite red → KILLED. Neighbours rt1/rt2/rt6-rt8 all
  use `filed=3` fixtures (`tkClean`/`tkOld`/`tkOut`, rounds `[3,4,5]`) and are
  untouched; `NO_FILED_REPORTS` is not a `FINDING_KINDS` member so the meta-check
  (:1487-1493) is unaffected either way.

## Notes / bounded recommendations

- Alternate unreached-arm candidates left for sibling seats (to keep classes
  disjoint): `INTERNAL_ERROR` catch-all token (:683, §13.6 #1), tracked-mode
  `REPORTS_DIR_MISSING` site (:527, §13.6 #2), main-repo `UPSTREAM_MISSING` site
  (:488, §13.6 #3), env-lane invalid throw (:277-279, §13.6 #4), `REPORT_MIN_BYTES`
  interval move inside [26, 1059] (:167/:345, §13.4 — projected SURVIVED),
  `HISTORY_LIMIT` (:168, §13.4), citation range form (:318, §13.6 #7).
- If L1 wants a second predicted-KILLED in this fragment, `filed.length < 3` is a
  degenerate alternative (would trip rt1/rt2/rt6-rt8 — kills for a *wide* reason,
  less diagnostic of the boundary).
- Files changed: `.ufo/waves/round-16/w1/RGSpecE.spec`, `.ufo/waves/round-16/w1/RGSpecE.md` (this report). Scratch: `/tmp/tameshi-r16-RGSpecE/` (materialized blob + selftest.out).
- No installs; no sibling-repo writes; no commits.
