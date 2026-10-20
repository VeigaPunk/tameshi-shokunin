# Round 15 w2 — ReviewExistingDisposition (C1 source/registry, static)

Seat: `TameshiR15.ReviewExistingDisposition` (reviewer, leaf). Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Scope: effective-expectation disposition gate (`tools/evidence-disposition.py`, C1), its exit-64 classification, and whether round-15 changed any predicate. Static review only. No gate, selftest, check, build, or test was executed. No tool was installed or updated.

Author-side advisory. This is not a verdict, admission, or independent promotion evidence.

## Exact sources read

| Path | Read | Notes |
|---|---|---|
| `AGENTS.md` | whole | LOG/append and read-only substrate rules |
| `corpus/lessons/round-14-verifier-spotcheck.md` | lines 5–7, 84, 96, 98, 157–160 | Routed defect 5 asks for exit 64 mapped to could-not-evaluate. Records checker hash `1609a9df…2d42d2d95` (line 84) |
| `tools/evidence-disposition.py` | 1–135 (docstring, exit map, USAGE); 147–148; 1125–1225 (run_mode); 1228–1260 (selftest fixtures); 1506–1507 (`_status_for`); 1510–1548, 1549–1603 (selftest harness and case body); 1594–1626 (case literals); 1797–1857 (usage-case loop and finish); 1860–1956 (parse_argv and main) | All `return 64`, `UsageError`, `CouldNotEvaluate` and `return 2` sites located by grep and read in context |
| `SKILL.md` (round-14 section) | 1563–1607 | Round-14 row at `:1601`, unchanged from HEAD. Retained paragraph at `:1604–1607` |
| `SKILL.md` (round-15 section) | 1660–1691 | Exit-class paragraph `:1668–1674`, round-15 registry `:1676–1681` |

Hashes observed at review time (the lane is live, so these can drift):
- `tools/evidence-disposition.py` sha256 `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95`. Equals `git show HEAD:tools/evidence-disposition.py` and the lesson's recorded checker hash.
- `SKILL.md` sha256 `032368fbb681c158a6ddd1130ff9fa044b3980dc0fa39c37e43f41e4b12c2cf1`. The file was edited during this review; the exit-class paragraph's wording changed between my first and second reads (see Observation O3).

Read-only git used: `git log -- tools/evidence-disposition.py`, `git diff HEAD --stat -- tools/evidence-disposition.py`, `git show 6431478 -- tools/evidence-disposition.py`, `git show HEAD:tools/evidence-disposition.py`, `git show HEAD:SKILL.md`, `git diff HEAD -U0 -- SKILL.md`, `git status --porcelain`. No `~/.omp` or credential file was read.

## Bounded agreement

**A1. No predicate change in the gate source.**
- `git diff HEAD -- tools/evidence-disposition.py` is empty.
- The worktree sha256 equals the HEAD blob sha256 and the lesson-recorded checker hash.
- The file's history is `0c6e36d` (introduced) and `6431478` (last touched). `6431478` changes only selftest fixtures: `_build_lane` gamma stdout gains `"marker": "GAMMA_OK"` (`:1311–1313`), and the duplicate-JSON-key fixture is re-expressed (`:1808–1817`). No predicate line changed in that commit.
- Caveat: I did not diff `0c6e36d` against its parent, since this tool was created there. The predicate claim covers round-15 and `6431478`, not round-14 authoring.

**A2. Exit 64 is reached only by usage.**
- `return 64` occurs only at `:1932` (empty argv) and `:1941` (`UsageError` from `parse_argv`).
- `raise UsageError` occurs only in `parse_argv` (`:1873–1918`).
- Nothing in `run_mode` or `evaluate_dispositions` returns 64.
- Normal run mode: `main` (`:1944–1952`) wraps `run_mode` in `except CouldNotEvaluate` (→ 2) and `except Exception` (→ 2 with `internal_error`). The only exit-1 sources are findings (`:1204`) and selftest failure (`:1852`).
- The round-15 classification "64 usage, no receipt" matches the code path.

**A3. Exit 2 vs exit 1 split is coherent for input integrity.**
- Malformed, duplicate-key, non-UTF-8, missing, unreadable, and digest-mismatched inputs all raise `CouldNotEvaluate` (exit 2). Examples: `:183–193`, `:304`, `:326`, `:510` (`receipt_check_duplicate`), `:515` (`receipt_check_invalid`), and the digest checks at `:1172–1176` and `:1188–1192`.
- Semantic mismatches are findings (exit 1): `expected_exit_mismatch` (`:607`), `expected_contains_missing` (`:613`), and similar.
- Selftest pins literal IDs and exits for the exit-2 cases (`:1788`, `:1800`, `:1792–1795`), and for the usage cases only the code (see F5).

**A4. Registry and tool agree on the normal-mode verdict map.** SKILL round-15 row `:1681` (`0 clean; 1 failed semantic expectations; 2 and 64 could-not-evaluate; 64 usage`) matches `run_mode`'s 0/1 and the `main` 2 path. The historical round-14 row at `:1601` is unchanged from HEAD and still says `64 usage`, as the round-15 correction intends.

## Findings

Severity is for the disposition gate's exit-lattice contract. None changes a predicate, a verdict on any registered normal-mode command, or the C1 scalar.

**F1 — low. `--help`/`-h` exits 0 with no evaluation.**
- Source: `tools/evidence-disposition.py:1933–1935`: `if argv in (["--help"], ["-h"]): sys.stdout.write(USAGE); return 0`.
- Contract: exit 0 is `clean` (USAGE `:128`, docstring `:65`, SKILL `:1668–1670`, `:1681`). The round-15 exit-class text says a non-evaluation must be could-not-evaluate, not clean.
- Counterexample (by reading, not run): `evidence-disposition.py --help` returns 0 and reads no receipt. A caller that treats exit 0 as clean would pass.
- Not reached by any registered command. Not a predicate change. Selftest has no `--help` case.
- Suggested fix for the lane to choose: exit 64 for help, or a documented exception. Do not leave help at 0 under a "0 = clean" map.

**F2 — low. The `--selftest` path escapes the exit map.**
- Source: `main` calls `return selftest()` at `:1942–1943`, outside the `try` that starts at `:1944`.
- Trigger: any exception that escapes `selftest()`'s setup. The first statement is `tempfile.mkdtemp(... dir="/tmp")` at `:1512`, which is not inside the case `try` (`:1546`). A failing `/tmp` would raise `OSError`, and Python exits 1 with a traceback.
- Contract: SKILL `:1670–1671` says an undeclared nonzero code "reads as could-not-evaluate". Exit 1 means failed-expectation in the registry (`:1681`), so this path is misclassified.
- Scope limit: the registry's verdict map covers normal mode. The "Self-test command" column declares no verdict map, so this is a conformance gap in the selftest entry, not in the gate verdict. Normal run mode is fully wrapped.
- Suggested fix: move `selftest()` under the same try, or wrap its setup and map to exit 2.

**F3 — low (labelling). The exit-64 could-not-evaluate mapping exists only in SKILL prose.**
- The tool's own exit map still says `64 usage error` (`:67–69` and `:128–131` in USAGE). The round-15 mapping at `SKILL.md:1668–1674` and `:1681` labels 64 as could-not-evaluate.
- `_status_for` (`:1506–1507`) returns `None` for 64. The 64 path emits no JSON and no status token (`:1931–1941`), so `--json` consumers see empty stdout with exit 64.
- Counterexample: a `--json` caller cannot distinguish "could not evaluate" from "usage" except by the exit code. The tool never emits `could_not_evaluate` for 64.
- Not a predicate change. The round-14 lesson asked for "map exit64 explicitly to could-not-evaluate". The registry does that; the tool text and status contract do not.

**F4 — low (classification boundary, no selftest pin). A named check missing from a pinned receipt exits 1.**
- Source: `receipt_check_missing` is added as a finding at `:808–812`; `run_mode` then returns 1 (`:1204`).
- Compare: a duplicate receipt check is exit 2 (`:510`, pinned at `:1800`), and a missing receipt file is exit 2 (`:304`, `:1168–1170`).
- The registry says exit 2 covers "invalid, missing or tampered inputs" (`SKILL.md:1681`). A check absent from a digest-verified receipt is arguably a missing input, but it lands in the failed class.
- The lane may intend this: `row_missing` is exit 1 by design (`:1597`), and the round-14 rule says an absent assertion is a failed expectation (`SKILL` round-14 table, "Expected exit agrees but the intended assertion is absent"). I cannot confirm intent from the text.
- `receipt_check_missing` has no selftest case. Grep finds it only at `:808` and `:812`.
- Suggested fix: state the boundary explicitly in SKILL and the tool docstring, and add a pinned selftest case either way.

**F5 — low (coverage). Usage selftest cases check only the exit code.**
- `:1828–1837` assert `returncode == 64` for `usage-no-arguments` and `usage-selftest-extra`.
- They do not assert empty stdout, the absence of JSON, or the stderr usage text. There is no `--help` case and no `--json` usage case.
- A future regression that printed a JSON body with exit 64 would still pass.

**O1 — observation. Routed defect 5 partly addressed in this file.** The lesson's "map exit64 to could-not-evaluate" is satisfied by the SKILL registry and exit-class text (`:1668–1674`, `:1681`). It is not reflected in the tool's own docstring, USAGE, or status contract (F3).

**O2 — observation. The "three classes over four exit codes" wording is accurate.** Exit codes 0, 1, 2, 64 map to clean, failed, and could-not-evaluate. The earlier wording "four-class lattice" was replaced during this review.

**O3 — observation. SKILL.md drifted during review.** Between my first and second reads, the exit-class paragraph changed from "four-class lattice" to "three classes over four exit codes", and the round-15 registry line moved from `:1682` to `:1681`. The diff against HEAD shows 85 insertions and 1 deletion. The one deleted line is round-14 prose (`checks do not acquire new expected rows…`, HEAD `:1607`). That sentence still appears at `SKILL.md:1607` at the reviewed hash, so this is a re-wrap, not a policy loss. Citations here use the current line numbers. The hash is recorded above.

## Verification gaps

- No gate, selftest, or `--help` run. All behaviors in F1, F2, and F4 are from static reading and are not observed.
- `/tmp` failure behavior in F2 is hypothesized from `:1512`, not reproduced.
- I did not review `0c6e36d` against its parent for predicate drift from its introduction; A1 covers the round-14 repair and round-15 state only.
- The round-14 selftest IDs and literal exits were read in the case harness (`:1594–1626`, `:1788–1800`) but not checked against outputs.
- I did not inspect `corpus/SOURCES.md` S050 or `tools/context-capture.py`; both are outside C1 scope.

## Messages and tool installs

- No message sent to `TameshiR15`. F1 and F2 are implementation-level but not critical: they affect help and selftest exit classification, not any registered normal-mode verdict, predicate, or the C1 scalar.
- Tools installed or updated: none.
