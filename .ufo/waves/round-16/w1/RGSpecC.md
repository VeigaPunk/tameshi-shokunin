# RGSpecC — C1 defect drafting, class C (counts + finding-kind meta-check)

Seat: `TameshiR16.RGSpecC` (wave 1, pre-registration phase). Date: 2026-10-20.
Scope: exactly 3 candidate single-edit defects in class C — counts and the
finding-kind meta-check (selftest count lines, one-sided counts; arm-class-matrix
§13.4/§13.5). Spec fragment: `.ufo/waves/round-16/w1/RGSpecC.spec` (spec v1).
No mutant was run; predictions below are pre-registered before any sweep.

## Pin

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin \
    show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs \
    > /tmp/tameshi-r16-RGSpecC/round-gate.mjs
$ sha256sum → f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  ✓ (matches pin)
$ wc -l → 1511
```

## Pristine control (allowed once per Target)

```
$ node round-gate.mjs --selftest        → exit 0
  ROUND_GATE_SELFTEST: 60/60 pass
  VERDICT: PASS
```

## Re-derived fixture arithmetic (basis for RGC-THIN-FLOOR)

`node -e` re-eval of the suite's report templates (`:785-794`), no file written:

```
thin5=25 · mentions10_r1=1059 · mentions1_r10=1119 · noshonen5=1536 · big5/big2=1579
big5_origin=1603 · big5_cited=1610 · mismatch5=1959 · headingless5=2100
```

Smallest non-thin *read* report = **1059 B** (r8's `fxMentions(10,'round-1')`);
thin fixture = **25 B** — reproduces §13.10 #3 and the §13.4 interval [26, 1059].

## Candidates

All `@old` uniqueness counts measured with a literal `str.count` over the pinned
blob (python3); `[A-Za-z]` regex-style counts are equal here since all texts are
literal. `@new` ≠ `@old` for all three.

### RGC-THIN-FLOOR — thin-report floor inside the unmeasured interval — SURVIVED

- `@old` `const REPORT_MIN_BYTES = 1024;` — **count = 1** (line 167)
- `@new` `const REPORT_MIN_BYTES = 512;`
- Sole read: `round-gate.mjs:345` (`add('REPORT_THIN', 'error', bytes >= REPORT_MIN_BYTES, …)`).
- **Prediction: SURVIVED.** With the floor at 512 no fixture report lands in
  (512, 1024]: thin fixture is 25 B (still thin → r4's `REPORT_THIN` arm fires),
  and every other read report is ≥1059 B (still non-thin). r4's floor-side
  predicate `thinBytes < 1024` (`:913`) asserts a fixture-computed byte count
  against a hardcoded literal, not the symbol — so the constant is
  *interval*-pinned, not point-pinned (§13.4). No `checks=`/kind-list/exit-code
  assert moves.

### RGC-KIND-DROP — remove `'TREE_DIRTY'` from `FINDING_KINDS` — SURVIVED

- `@old` `  'TREE_DIRTY', 'UNPUSHED', 'REPORT_UNTRACKED',` — **count = 1** (line 175)
- `@new` `  'UNPUSHED', 'REPORT_UNTRACKED',`
- `FINDING_KINDS` (`:171-176`) has exactly one consumer: the meta-check
  `missing = FINDING_KINDS.filter((k) => !observed.has(k))` (`:1488`); `observed`
  is fed only by `parseFindings` off emitted `ROUND_GATE  <sev>  <KIND>` lines
  (`:857-860`). Nothing compares emitted kind literals to the enum; JSON
  check-shape asserts `typeof c.id === 'string'` only (`:1256-1257`).
- **Prediction: SURVIVED.** r26 (`:1141-1148`) still passes: the `add()` call at
  `:451` still emits literal `'TREE_DIRTY'`, `kindsEq` compares stdout kinds to
  its own expected list, and `d.includes('entries=6')` is intact. The meta-check
  computes `enum(13) ∖ observed(14) = ∅` → `ok` — this is the exact one-sidedness
  of §13.4: the net sees `enum ∖ observed`, never `observed ∖ enum`. Inverse
  probe (append `'INTERNAL_ERROR'` to the enum) would be KILLED via the same
  check — a candidate for another class seat if L1 wants the boundary measured
  from both sides.

### RGC-PASS-COUNT — selftest summary numerator `passed` → `passed + 1` — SURVIVED

- `@old` `  lines.push(\`ROUND_GATE_SELFTEST: ${passed}/${results.length} pass\`);`
  — **count = 1** (line 1505)
- `@new` `  lines.push(\`ROUND_GATE_SELFTEST: ${passed + 1}/${results.length} pass\`);`
- **Prediction: SURVIVED.** The mutant prints `61/60 pass`; the only readers of
  that line are (a) the nested-run hermeticity check `:1399` —
  `/^ROUND_GATE_SELFTEST: \d+\/\d+ pass$/` is shape-only — and (b) `VERDICT:` /
  the exit code, both computed from `passed === results.length` (`:1506`,`:1508`),
  which is unchanged. §13.5 #2: the selftest counts are reported but unread.
  Caveat (honesty): this mutant's output delta exists only when a check fails —
  on an all-green run its observability rests entirely on the shape-only assert.

## Class verdict summary (pre-registered)

| ID | @old line | Prediction | Arm exercised |
|---|---|---|---|
| RGC-THIN-FLOOR | :167 | SURVIVED | §13.4 floor, interval-pinned |
| RGC-KIND-DROP | :175 | SURVIVED | §13.4 one-sided meta-check |
| RGC-PASS-COUNT | :1505 | SURVIVED | §13.5 unread summary counts |

Predicted kill-rate contribution of this class: **0/3**. If any comes back
KILLED that is itself a calibration finding (an assert we did not see in the
static read). A fourth, KILLED-anchoring candidate L1 may substitute:
`missing.length === 0` → `missing.length !== 0` (`:1490`, count=1) — predicts
KILLED trivially (meta-check fails immediately) but measures only that the
meta-check's predicate is wired, not its one-sidedness.

## Commands run

- `git -C kumitate-shokunin show 364f1d59…:scripts/round-gate.mjs` → blob pinned, sha256 ✓
- `node round-gate.mjs --selftest` → exit 0, `ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS`
- `python3` literal counts for the three `@old` strings → 1, 1, 1
- `node -e` fixture byte-size re-eval → table above (matches §13.10 #3)
- `grep -n` maps: `REPORT_MIN_BYTES` reads (:167 def, :345 use); `FINDING_KINDS`
  consumers (:171-176 def, :1488 sole read); `passed`/`results.length` (:1498-1508);
  `observed` lifecycle (:692, :860, :1488, :1491).

## Risks / notes

- All three predictions are SURVIVED by design — class C is the blind-spot
  family; the KILLED substitute above is offered if L1 wants mix balance.
- `@old` for RGC-PASS-COUNT contains `` ` `` and `${…}` verbatim; spec v1 has no
  escape for backtick but none is needed (escapes only `\n \t \r \\`; backtick is
  literal text and `@old` matching is a byte-substring search).
- No installs, no sibling-repo writes, no mutant executions. Scratch:
  `/tmp/tameshi-r16-RGSpecC/` (pinned blob + this analysis).
