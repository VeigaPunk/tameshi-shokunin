# T47MutC1Counter — C1 counter selftest mutation audit (tameshi round 47)

Seat: T47MutC1Counter (leaf, no subagents). Judged on: calibration (C1).
Target: `.ufo/evidence/round-47/calibration/measure.py` (508 lines), audited through its own `--selftest` (35 cases).
Scratch: `/tmp/tameshi-r47-T47MutC1Counter/` (baseline stdout, battery driver, per-run results JSON).
Date: 2026-10-25.

## Method

- Copied the counter to scratch (`measure.pristine.py`); verified byte-identical to the lane file.
- Detector validated first: pristine `--selftest` → `C1_R47_SELFTEST: cases=35 failed=0`, `VERDICT: PASS`, exit 0 (73 s wall). A mutant is **killed** iff its selftest prints `VERDICT: FAIL` (exit nonzero); a crash/timeout would be inconclusive (none occurred).
- Each mutant = one minimal source edit on a private copy; run `--selftest`; copy deleted afterwards. Mutants were never written to the lane. 29 selftest runs total (1 baseline + 25 battery + 2 follow-up + 1 two-site gradation), ~7 min wall at 6-way parallelism.

## Result summary

18 of 26 rules killed; 8 survivors. All survivors were run to a fully green selftest (`cases=35 failed=0`, `VERDICT: PASS`) — they are coverage findings, not contract changes.

| Rule | Mutant (line) | Verdict | Killing case(s) |
|---|---|---|---|
| last-row-wins | `rows[...] = cells` → `rows.setdefault(...)` (118) | **killed** | T08, T09 |
| fenced hiding (toggle) | `fenced = not fenced` → `fenced = True` (81) | **killed** | T10 |
| comment hiding (dotall) | drop `flags=re.S` (77) | survived | — |
| claim regex: arrow | `ARROW +` dropped from `CLAIM_CAP` (54) | survived | — |
| claim regex: exit charset | `exit (\d+)` → `exit (-?\d+)` (54) | survived | — |
| claim regex: tool sha | `{12}` → `{6}` in `CLAIM_CAP` (54) | **killed** | T01 (+20 more) |
| claim regex: deps charset | `[a-z,-]+` → `[A-Za-z,-]+` (54+56) | killed only at BOTH sites; each single site survives (see below) | T23 (M07c) |
| axis integer parse | `fullmatch(r'\d+')` → `r'\w+'` (134) | **killed** | T17 |
| observed line picking | `m.group(1)` → `m.group(0)` (153) | **killed** | T01 (+8) |
| exit capture | `obs = [line, str(p.returncode)]` → `[line, '0']` (227) | **killed** | T01 (+8) |
| sha prefix compare | `hexdigest()[:12]` → `[:8]` (230) | **killed** | T01 (+8) |
| comparable() cut | return full `obs` instead of the cut (239) | survived | — |
| P0-vs-P1 env rule | `add('env')` → `add('node')` (304) | **killed** | T25_env |
| P2 bwrap profile | `('bwrap','P2')` → `('bwrap','P4')` (57) | **killed** | T24/T25_bwrap, T25_node |
| P3 jj profile | `('jj','P3')` → `('jj','P2')` (57) | **killed** | T25_jj, T24_jj, T25_bwrap |
| P4 node profile | `('node','P4')` → `('node','P3')` (57) | **killed** | T25_node, T24_node, T25_jj |
| P5 fleet-root decoy bind | drop `'--bind', decoy, FLEET` from the bwrap argv (212) | **killed** | T24/T25_fleet-root |
| deps equality / `none` clause | `frozenset() if names == ['none'] else ...` → `frozenset(names)` (131) | **killed** | T01 (+5) |
| unpinned count | drop `not`: counts pinned instead (296) | **killed** | T21, T01 (+4) |
| append-only prefix | `startswith` → `endswith` (272) | **killed** | T18 |
| stmts pin | `== pin` → `!= pin` (257) | **killed** | T18, T14 |
| self pin | digest compare dropped: `int(blob is not None)` (255) | **killed** | T15 |
| statement count | `len(statements) == n_expected` → `>=` (329) | survived | — |
| `total == 0` predicate | → `total <= 1` (329) | survived | — |
| `--only` never passing | drop `and not only` (329) | survived | — |
| decoy stub exit code (probe) | STUB `exit 7` → `exit 0` (59) | survived | — |

## Killing evidence (case code from the selftest)

```python
('T01_all_match', good, {}, 'total=0'),
('T08_last_row_wins_stale_first', base_sc + cap_hdr + row_cap('alpha', 'ALPHA: 1/3 pass', 0) + B() + '\n' + cap_hdr + A() + '\n'
 + axis_hdr + row_score(), {}, 'total=0'),
('T09_last_row_wins_stale_last', base_sc + cap_hdr + A() + B() + '\n' + cap_hdr + row_cap('alpha', 'ALPHA: 1/3 pass', 0) + '\n'
 + axis_hdr + row_score(), {}, 'mismatches=1'),
('T10_fenced_table_ignored', base_sc + '```\n' + cap_hdr + row_cap('alpha', 'ALPHA: 9/9 pass', 0) + '```\n' + cap_hdr + A() + B()
 + axis_hdr + row_score(), {}, 'total=0'),
('T15_self_pin_broken', good, {'selfbytes': b'# not the counter\n'}, 'self_pin=0'),
('T17_axis_noninteger_unparsed', doc(A(), B(), score=row_score('seven')), {}, 'unparsed=1'),
('T18_match_is_true', good, {}, 'C1_R47_PASS=true'),
('T21_statement_without_sha_file_unpinned', good, {'nosha': True}, 'unpinned=1'),
('T23_unsorted_unknown_dep_name_unparsed', doc(A(deps='Bwrap'), B()), {}, 'unparsed=1'),
for dep in ('bwrap', 'jj', 'node', 'fleet-root', 'env'):
    cases.append(('T24_undeclared_%s_dependence' % dep, 'dep:' + dep + ':none', {'dep': dep}, 'dep_mismatch=1'))
    cases.append(('T25_declared_%s_dependence_matches' % dep, 'dep:' + dep + ':' + dep, {'dep': dep}, 'dep_mismatch=0'))
```

Sample got-lines: M01 `FAIL T09 ... want='mismatches=1' got=... mismatches=0 ... total=0 ... C1_R47_PASS=true`; M13/M17 `FAIL T25_declared_..._dependence_matches want='dep_mismatch=0' got=... dep_mismatch=1 ... total=1 ... C1_R47_PASS=false`; M20 `FAIL T18 ... append_only=0 ... C1_R47_PASS=false`; M23 `FAIL T15 ... want='self_pin=0' got=... self_pin=1 ...`. Full per-mutant fail lists: `/tmp/tameshi-r47-T47MutC1Counter/results.json`.

The deps charset is enforced twice (DEPS_RE at 56 gates the early parse and axis rows; CLAIM_CAP at 54 gates cap rows). Widening either single site is a no-op for T23 (the other gate still rejects `Bwrap` → unparsed → case passes); widening both (M07c, one logical defect) is killed by T23 (`cases=35 failed=1`, `VERDICT: FAIL`).

## Survivors (coverage findings)

1. **Comment hiding, dotall (M03)** — without `re.S`, `<!--...-->` spanning lines is not blanked, but T11's comment is followed by a good table, so last-row-wins overwrites the leaked stale rows. No case leaves a hidden-block row as the LAST row of its kind.
2. **Arrow anchor (M04)** — `CLAIM_CAP` works with the U+2192 arrow requirement deleted; T07's prose row lacks exit/sha/deps, so it is rejected regardless. No wrong/missing-arrow-with-otherwise-valid-claim fixture exists.
3. **Exit charset (M05)** — `exit (-?\d+)` accepted everywhere; no negative or malformed exit appears in any fixture.
4. **comparable() cut (M12)** — comparing the FULL observation (cap: line+exit+sha; axis: line+sha) instead of the cut changes nothing, because every fixture's `sha_file` content is profile-invariant. A dependence that expresses itself through the tool sha (or an axis sha drifting across profiles) is untested.
5. **Statement count `>=` (M22)** — T16 only drops statements; a fixture committing EXTRA statements would pass. Statement injection is not covered.
6. **`total <= 1` (M24)** — off-by-one slack in the pass gate is invisible: every negative case keys on a component count (`mismatches=1`, `unparsed=1`, ...) or an already-broken pin, and T18 has total=0. One single mismatch would still print `C1_R47_PASS=true` under the mutant.
7. **`--only` gate (M25)** — dropping `and not only` survives because T26's subset (1 of 3) already fails the count check. Pinning the gate itself needs an `--only` run naming ALL statements (in production the 22-count check also masks it, so severity is low, but the gate is unpinned by this battery).
8. **Decoy stub exit code (M26b)** — no selftest case executes the decoy `sources-census.sh` stub (the fleet-root fixture only tests file existence under the bind). The stub's `exit 7` behavior is exercised only by real statements, never by the battery.

Each single-site deps-charset gradation (M07 at CLAIM_CAP only, M07b at DEPS_RE only) also survived, recorded above.

## Restoration evidence

- Lane counter bytes untouched: `sha256sum` before = after = `c54debb241c0df7fa282f619bb0905472a375ce0b3e5f800edc6f8945daa0f30`; `cmp` against the pristine scratch copy: identical.
- All mutants ran on copies under `/tmp/tameshi-r47-T47MutC1Counter/` and were deleted after their run; no sibling source, no lane jj/Git state touched; the only lane write is this report file.
- Tooling: none installed (system python3 + git only; pacman guard respected).

## Verdict

The C1 selftest is a strong detector for its core semantics (row selection, fence hiding, value/exit/sha capture, all five dependence attributions, pins, append-only, unpinned, none-clause, partial labelling): 18/26 one-site defects killed. Its blind spots are: hidden-content leakage (comment dotall), glyph/charset looseness in the claim regex (arrow, exit sign; deps charset only caught when both duplicated regexes widen), the comparable() cut, statement over-count, off-by-one slack in the `total == 0` gate, the redundant-in-battery `not only` gate, and the decoy stub's behavior. Reported as coverage findings; contract untouched.
