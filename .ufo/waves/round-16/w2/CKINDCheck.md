# CKINDCheck — w2 falsification: note §3 CKIND equivalence claim

Seat: `TameshiR16.CKINDCheck` (wave 2, lane axes: depth + calibration).
Lane read at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`; target read from the
sibling repo's object store, never edited. Scratch:
`/tmp/tameshi-r16w2-CKINDCheck-FfTYe3`. No tool installed, no repo written.

## Target

Note §3 (`corpus/knowledge/mutation-case-kumitate-round-gate.md`, "The
meta-check is one-sided (CKIND)") claims:

1. `FINDING_KINDS` has no reader other than `:171` (declaration) and `:1488`
   (meta-check) in kumitate `scripts/round-gate.mjs` @ `364f1d5`;
2. therefore "the mutant's gate behaviour is identical to pristine";
3. the survivor is "equivalent for gate behaviour; it weakens only the suite's
   own net", not a gate detection gap.

Attacked by static read-site proof plus a pristine-vs-mutant differential over
non-selftest modes on one fixture.

## Artifact identity (reproduced)

```
$ git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs | sha256sum
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -
$ ... | wc -lc
   1511   80415
$ git ls-tree 364f1d5 -- scripts/round-gate.mjs
100755 blob 1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3	scripts/round-gate.mjs
$ git rev-parse HEAD:scripts/round-gate.mjs   # HEAD 1770305
1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3      # same blob as 364f1d5
$ git log -1 --format='%h %cs' 364f1d5 -- scripts/round-gate.mjs
364f1d5 2026-10-13                            # last-touching commit
```

The note's pin (80,415 B, 1,511 lines, mode 100755, `f890e277…d3e9`) and its
"HEAD holds the same blob" statement both hold. `git --no-optional-locks status
--porcelain` in kumitate-shokunin: 0 entries before and after.

Mutant byte-identity with the round's case (my one-line edit, then hash):

```
$ sed -i "s/'TREE_DIRTY', 'UNPUSHED'/'UNPUSHED'/" mutant/round-gate.mjs
$ diff -u pristine/round-gate.mjs mutant/round-gate.mjs
-  'TREE_DIRTY', 'UNPUSHED', 'REPORT_UNTRACKED',
+  'UNPUSHED', 'REPORT_UNTRACKED',
$ sha256sum mutant/round-gate.mjs
1e6d4deba1a4da841ba700b2f3878a241a46959f0af8b49e68c7711fc057a9a0
```

That sha equals `.ufo/evidence/round-16/round-gate/sweep/results.tsv` row
`CKIND SURVIVED 0 2932 1e6d4deb…` exactly, and the pre-registered
`@old`/`@new` pair in `round-gate.defects.spec` (sha256 `e99b87eb…11c4`, equal
to `sweep/spec.copy`) is the same edit. So the object attacked is the case's
object, not a lookalike.

## 1. Read sites — static

```
$ git show 364f1d5:scripts/round-gate.mjs | grep -n FINDING_KINDS
171:const FINDING_KINDS = [
1488:      const missing = FINDING_KINDS.filter((k) => !observed.has(k));
```

Two occurrences total. `:171` is the `const` declaration; **the sole read is
`:1488`**. Line 175 (the edit line) is `'TREE_DIRTY', 'UNPUSHED',
'REPORT_UNTRACKED',` — the member the mutant drops.

No dynamic escape hatch: `grep -nE 'eval\(|new Function|globalThis|import\('`
over the whole file returns nothing; the file is an ES module (no `with`), has
no `export`/`module.exports`, and `main()` is self-contained
(`process.exitCode = main()` at `:1511`). The only way to reach a module-local
binding is an identifier in this file, and the identifier appears nowhere else.

Call-graph confinement of the read:

- `:635  if (opts.selftest) return selfTest();` — the only `selfTest` call site
  (`grep -n 'selfTest('` → `:635`, `:689` only), and it returns before any mode
  dispatch;
- `:689  function selfTest()` — `:1488` is inside it (`try` block of the
  selftest, `:874-1496`).

Cross-file: the sibling scripts `claims-check.mjs:109`, `kimi-census.mjs:151`,
`proxy-check.mjs:377`, `sources-check.mjs:108` each declare their *own*
independent `FINDING_KINDS`; none reads round-gate's (not exported). The only
cross-file relation is `proxy-check.mjs:292-299` hashing the file —
`pin.round-gate` → `scripts/round-gate.mjs` — and that pin currently equals the
file (`SCORECARD.md:297` = `f890e277…d3e9` = computed sha). That is a hash pin
on repo bytes, not a reader of the enum; it is irrelevant to a /tmp copy and is
not round-gate gate behaviour.

**Answer to the target's first question: yes — no read exists outside
`:171`/`:1488`; more precisely, the only read is `:1488`, inside `selfTest()`,
unreachable unless `--selftest` was passed.** The note's own sentence "grep -n
`FINDING_KINDS` → :171 and :1488 only" reproduces exactly.

## 2. Non-selftest differential — dynamic

One fixture, built fresh in scratch (`setup-fixture.sh`): git work tree
`fix/` (branch `main`, bare `origin.git`, pushed) with

- `SCORECARD.md`: `| 7 | … |` row + `## Planned` naming round 8;
- `LOG.md`: `- 2026-01-02 — round 7 fixture entry`;
- `.ufo/reports/round-{5,6,7}/kumitate.md`; round-7 report 1,537 B, 2 headings,
  names `round-7`, no SHONEN heading; round-5/6 are tracked-mode reports;
- phase 2 adds untracked `dirty.txt` so close mode must fire `TREE_DIRTY`.

Every run: `env -i` with private `HOME`/`TMPDIR`, `GIT_CONFIG_GLOBAL`/
`GIT_CONFIG_SYSTEM=/dev/null`, node `v24.21.0` (Linux 7.2.11). Pristine and
mutant run against the **same** fixture path, so path-bearing output is
comparable. Gate-side status before/after phase 1: empty; phase 2 before/after:
only `?? dirty.txt` — the gate did not mutate the fixture.

Result (stdout bytes, exits, stderr; `norm` = strip `"durationMs": <n>` only):

| mode (fixture) | pristine | mutant | stdout | stderr |
|---|---|---|---|---|
| `--round 7` audit | exit 0, 219 B | exit 0, 219 B | byte-identical | empty |
| audit `--strict` | exit 1, 219 B | exit 1, 219 B | byte-identical | empty |
| audit `--json` | exit 0, 2126 B | exit 0, 2126 B | norm-identical; raw differs only `durationMs` 4 vs 3 | empty |
| `--tracked` (3 filed rounds) | exit 0, 63 B | exit 0, 63 B | byte-identical | empty |
| `--close` clean tree | exit 0, 219 B | exit 0, 219 B | byte-identical | empty |
| `--close` dirty tree | exit 1, 284 B | exit 1, 284 B | byte-identical | empty |
| `--close --json` dirty | exit 1, 2652 B | exit 1, 2652 B | norm-identical; raw `durationMs` 8 vs 7 | empty |
| fail-closed `--json`, missing reports dir | exit 2 | exit 2 | norm-identical; `"kind": "REPORTS_DIR_MISSING"` | empty |
| usage `--tracked --close` | exit 64 | exit 64 | stdout+stderr identical | empty |

Key observed line, identical on both sides in dirty close:

```
ROUND_GATE  error  TREE_DIRTY  entries=1 first5=["?? dirty.txt"]
ROUND_GATE: DRIFT (round=7 lane=kumitate checks=13 errors=1 warnings=1)
```

So the kind whose name was removed from the enum **still fires and is still
reported**; the enum is not consulted on any verdict, finding, filter or render
path.

Controls proving the JSON residual is clock jitter, not mutation:

- pristine `--json` repeated twice: raw differs (`durationMs` 4 vs 3),
  normalized identical;
- pristine audit and pristine dirty-close repeats: normalized identical to
  their first runs; mutant repeats likewise;
- `--json` ×3 per side: each side raw-identical within itself (`durationMs`
  4,4,4 on both), cross-side normalized identical.

## 3. Selftest cross-check (the mutation's own hit surface)

Both sides, same `TMPDIR` parent, `env -i`, private `HOME`:

```
pristine --selftest exit=0 stderr=0B ROUND_GATE_SELFTEST: 60/60 pass
mutant   --selftest exit=0 stderr=0B ROUND_GATE_SELFTEST: 60/60 pass
PASS  [60/60]  every declared finding kind fires in at least one fixture — 14 kinds observed   (both sides)
selftest stdout normalized-identical (only the random mkdtemp suffix normalized)
```

The recorded sweep agrees: `sweep/evidence/CKIND.out` ends `60/60 pass`,
`VERDICT: PASS`, `14 kinds observed`; `results.tsv` row says `CKIND  SURVIVED
exit 0  duration-ms 2932  mutant-sha256 1e6d4deb…`. My independent run
reproduces the survivor and the tally, and additionally shows the selftest
*output* is unchanged, not just its exit.

## 4. Why it is equivalent (and where the net is weakened)

At `:1486-1493`:

```js
check('every declared finding kind fires in at least one fixture', () => {
  const missing = FINDING_KINDS.filter((k) => !observed.has(k));
  ok: missing.length === 0,
  detail: missing.length ? `never fired: ${missing.join(', ')}` : `${observed.size} kinds observed`,
});
```

`observed` is populated only by `parseFindings` (`:857-860`) from emitted
`ROUND_GATE  sev  KIND  detail` lines, i.e. from actual gate runs. With
`enum' = enum ∖ {TREE_DIRTY}`, `missing' = enum' ∖ observed ⊆ enum ∖ observed =
missing`; pristine `missing = ∅`, so mutant `missing' = ∅` necessarily. The
check's `ok` can only stay true, and `observed.size` is unaffected, which is why
even the printed detail line is identical.

The equivalence is therefore structural, not incidental: `TREE_DIRTY` is emitted
by the string literal at `:451` (`add('TREE_DIRTY', 'error', …)`), which the
edit does not touch; the enum is a selftest-only inventory.

The weakening the note claims is real and latent: with `TREE_DIRTY` no longer
listed, a future regression in which that kind stops firing (or its fixture is
removed, e.g. selftest check [25/26] at `:1127-1146`) would leave `missing`
empty and the meta-check green. In that sense the mutant removes a suite net
while changing no gate behaviour — exactly the note's "equivalent for gate
behaviour; it weakens only the suite's own net". §6's owner recommendation
(`observed ⊆ enum`, i.e. a two-sided check) would have caught it.

## 5. Caveats and residual risk

- **Measurement caveat for repeaters, not a note defect:** `--json` is *not*
  byte-deterministic even pristine-vs-pristine — `durationMs`
  (`:569`, `:613`, `:671`) jitters (observed 4 vs 3 in two pristine runs).
  A literal byte-diff of two `--json` runs can false-positive; strip
  `durationMs` (or compare parsed bodies) before comparing. All other modes
  compared byte-identical.
- In-tree (not copy) application of the edit would be caught by kumitate's own
  `pin.round-gate` sha256 through proxy-check (`PIN_DRIFT`), but that is a
  repo-state gate, not round-gate behaviour; the sweep's copy-and-restore
  method (`MUTATE_RESTORE: OK`) keeps "equivalent for gate behaviour" exact.
- Scope: one revision (`364f1d5`, bytes identical at HEAD), one host, node
  v24.21.0; the fixture is mine, deliberately exercising `TREE_DIRTY` both
  firing (dirty close) and not applicable (audit/tracked), all 10 audit checks,
  the close tail, fail-closed JSON, and usage exit 64. Executed modes: 9
  non-selftest invocations per side plus selftest; no skipped check in the
  selftest runs (both 60/60).

## Verdict

**Holds.** `FINDING_KINDS` is read exactly once (`round-gate.mjs:1488`, inside
`--selftest`-only code); the mutant's non-selftest behaviour is identical to
pristine across audit/`--strict`/`--json`/`--tracked`/close-clean/close-dirty/
fail-closed/usage on one fixture (identical exits and stderr; stdout identical
except the clock-jitter `durationMs` field), with `TREE_DIRTY` still firing and
reported; the note's "equivalent for gate behaviour, weakens only the suite's
net" is the correct reading of this survivor.
