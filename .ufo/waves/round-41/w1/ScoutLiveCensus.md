# ScoutLiveCensus — write-path-census-v3 over every tools/*.py

Seat: `L1Tameshi41.ScoutLiveCensus` · lane `tameshi-shokunin` · census measured at revision `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937` (the freeze `HEAD` when the run started; worktree clean apart from untracked `.ufo/evidence/round-41/sources/` and `.ufo/waves/round-41/`). The lane `HEAD` later advanced to `b37ce97`; `git diff d4ee4e63..b37ce97 -- tools/` is empty and both tool sha256s are unchanged (see the lane-state section at the end), so every row below binds to both revisions.

## Command (read-only; no counter invoked)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
for f in tools/*.py; do python3 tools/write-path-census-v3.py --file "$PWD/$f"; done
```

`write-path-census-v3.py` has no directory mode (`--file` / `--selftest` / `--fixtures` only; `tools/write-path-census-v3.py:309-333`), so per-file invocation is the only way to census a tree. Absolute paths were passed so the emitted `file:line` prefix is unambiguous. Scratch copy of the raw output: `/tmp/tameshi-r41-livecensus/run.txt` (v3), `/tmp/tameshi-r41-livecensus/v2-run.txt` (v2) — convenience only; every number in this report is inlined below, so a `/tmp` sweep leaves no dangling evidence.

## Tool identity observed

- `tools/write-path-census-v3.py` sha256 `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` — matches `contract.json` `C2.tool_sha256`.
- `tools/write-path-census-v2.py` sha256 `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` — matches `C2.v2_sha256`.
- Control only (not the measurement): `--selftest` → `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`, exit 0.

## Per-file totals (25 files)

Columns are v3 `summarize()` keys (`sites` = every write call it recognized; `expected_sites` = destination resolves to an expected-value name; `unflagged` = expected and not scratch and not file-flagged). `v2_sites/v2_unfl` are the imported `write-path-census-v2.classify_text` line counts on the same file, for contrast.

| file | sites | expected_sites | variable_expected | symlink_expected | scratch_expected | unflagged | parse_errors | v2_sites | v2_unfl |
|---|---|---|---|---|---|---|---|---|---|
| bash-witness-study.py | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| command-binding.py | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| context-capture.py | 3 | 2 | 2 | 0 | 0 | 2 | 0 | 3 | 0 |
| env-diff.py | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| evidence-disposition.py | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 |
| golden-verdict.py | 3 | 3 | 3 | 0 | 3 | 0 | 0 | 3 | 0 |
| mte-interop.py | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 |
| pin-disposition.py | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 |
| receipt-measure.py | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| receipt-window.py | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| registry-check.py | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 |
| registry-replay.py | 5 | 1 | 1 | 0 | 0 | 1 | 0 | 5 | 1 |
| repeat-control.py | 6 | 2 | 1 | 1 | 2 | 0 | 0 | 3 | 0 |
| round21-measure.py | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| tally-audit-v2.py | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| tally-audit-v3.py | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| tally-audit.py | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| trace-inputs.py | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| wave-accounting.py | 2 | 1 | 1 | 0 | 1 | 0 | 0 | 2 | 1 |
| wave-parent-settle.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wave-route-mix.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| witness-metadata.py | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 0 |
| write-path-census-v2.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| write-path-census-v3.py | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| write-path-census.py | 2 | 1 | 1 | 0 | 1 | 0 | 0 | 5 | 0 |
| **TOTAL** | **111** | **10** | **9** | **1** | **7** | **3** | **0** | **117** | **2** |

`parse_errors=0` for every file — no `SyntaxError` record from `classify_source` in the tree.

## Every expected-value site (10)

`resolved` is v3's folded destination text (`_resolve`); long traces are cut at 150 chars. `scratch`/`flagged`/`unflagged` are the record booleans the fixture counters assert.

| file:line | kind | resolved | scratch | flagged | unflagged |
|---|---|---|---|---|---|
| `tools/context-capture.py:1682` | open | `os.path.join(directory, "expected.json")self.case_dir(name)namedirectory self.case_dir(name)  nameexpected.json"expected.json"` | 0 | 0 | 1 |
| `tools/context-capture.py:1685` | open | `os.path.join(directory, "expected.json")self.case_dir(name)namedirectory self.case_dir(name)  nameexpected.json"expected.json"` | 0 | 0 | 1 |
| `tools/golden-verdict.py:52` | open | `os.path.join(tmp, 'expected.txt')tempfile.TemporaryDirectory(prefix='golden-verdict-')golden-verdict-'golden-verdict-'tmp tempfile.TemporaryDirectory(…` | 1 | 0 | 0 |
| `tools/golden-verdict.py:54` | open | `os.path.join(tmp, 'same.txt')tempfile.TemporaryDirectory(prefix='golden-verdict-')golden-verdict-'golden-verdict-'tmp tempfile.TemporaryDirectory(pref…` | 1 | 0 | 0 |
| `tools/golden-verdict.py:56` | open | `os.path.join(tmp, 'other.txt')tempfile.TemporaryDirectory(prefix='golden-verdict-')golden-verdict-'golden-verdict-'tmp tempfile.TemporaryDirectory(pre…` | 1 | 0 | 0 |
| `tools/registry-replay.py:123` | write_bytes | `expected.json` | 0 | 0 | 1 |
| `tools/repeat-control.py:811` | open | `os.path.join(tamper_duplicate_key, "expected.json")os.path.join(scratch, "snap-tamper-duplicate-key")scratch tempfile.mkdtemp(prefix="tameshi-r12-repe…` | 1 | 0 | 0 |
| `tools/repeat-control.py:820` | os.symlink | `os.path.join(tamper_manifest_symlink, "expected.json")os.path.join(scratch, "snap-tamper-manifest-symlink")tempfile.mkdtemp(prefix="tameshi-r12-repeat…` | 1 | 0 | 0 |
| `tools/wave-accounting.py:165` | write_text | `Path(directory)tempfile.TemporaryDirectory(prefix='tameshi-r22-accounting-')'tameshi-r22-accounting-'directory tempfile.TemporaryDirectory(prefix='tam…` | 1 | 0 | 0 |
| `tools/write-path-census.py:95` | open | `os.path.join(tmp, 'case.expected')tempfile.TemporaryDirectory(prefix='write-path-census-')write-path-census-'write-path-census-'tmp tempfile.Temporary…` | 1 | 1 | 0 |

Sites per file: context-capture.py 2, golden-verdict.py 3, registry-replay.py 1, repeat-control.py 2, wave-accounting.py 1, write-path-census.py 1. `unflagged=1` appears on exactly 3 sites (context-capture.py:1682, :1685, registry-replay.py:123).

## Grounding each flagged/unflagged site against the source line

- `tools/repeat-control.py:811` — `with open(duplicate_path, "wb") as handle:`; `duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")` (:808), `tamper_duplicate_key` ← `os.path.join(scratch, "snap-tamper-duplicate-key")` (:806), `scratch` ← `tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir="/tmp")`. v3 scratch=1.
- `tools/repeat-control.py:820` — `os.symlink(os.path.join(snap_stable, "expected.json"), os.path.join(tamper_manifest_symlink, "expected.json"))`; link path traces to the same `/tmp` mkdtemp. v3 symlink_expected=1, scratch=1. v2 sees neither line (`WRITE_RE` does not match `open(<name>, "wb")` with no expected literal nor a bare `os.symlink(` head) — this is the live evidence for `live_var_expected_v2=0` / `live_symlink_sites_v2=0` in C2.
- `tools/context-capture.py:1682` and `:1685` — `with open(expected_path, "wb")` / `open(expected_path, "w", ...)`; `expected_path = os.path.join(directory, "expected.json")` (:1662), `directory = self.case_dir(name)`. `case_dir` (:1631-1635) joins `self.root`, and `self.root = tempfile.mkdtemp(prefix="context-capture-selftest-", dir="/tmp")` (:1624). **v3 reports scratch=0 / unflagged=1 here**, because `_resolve` stops at the method call `self.case_dir(name)` and never reaches the mkdtemp. These are the only two live false positives under the contract's declared scope limit ("any path computed by a non-folding call is not resolved").
- `tools/registry-replay.py:123` — `(out / 'expected.json').write_bytes(...)`; `out = Path(args.out)` (:181, `:282`), i.e. a CLI-supplied output directory, not a tempdir and not gated by an `--update` flag. **Genuinely unflagged expected write**: `resolved=expected.json`, scratch=0, flagged=0, unflagged=1. v2 also counts it (its `EXPECTED_RE` sees the literal on the same line).
- `tools/golden-verdict.py:52/:54/:56` — `open(golden|same|other, 'w')` under `tempfile.TemporaryDirectory(prefix='golden-verdict-')` (:44). scratch=1 so unflagged=0. Note `:54` and `:56` carry `expected=1` although their basenames are `same.txt`/`other.txt`: `expected` is `EXPECTED_RE.search(resolved)` (`:165`) and `resolved` folds the tempdir source text `golden-verdict-`, so the word `golden` in the *prefix* trips `EXPECTED_RE`. Harmless here (scratch), but it is why `expected_sites=3` rather than 1.
- `tools/wave-accounting.py:165` — `(work / 'expected.json').write_text(...)`; `work` ← `tempfile.TemporaryDirectory(prefix='tameshi-r22-accounting-')` (:156). v3 scratch=1, unflagged=0; v2 reports unflagged=1 on this line (false positive: v2 tests `SCRATCH_RE` against the line only, and the tempdir is on the previous line).
- `tools/write-path-census.py:95` — `with open(path, 'w')` under `tempfile.TemporaryDirectory(prefix='write-path-census-')`; scratch=1 and **flagged=1** because `flagged = FLAG_RE.search(text)` is file-wide (:218) and that same file defines `FLAG_RE` with the literal `--update\b` at :55. Any file that contains the flag pattern text flags itself; this is the only flagged=1 file in the tree.

## Zero-site files are true zeros, not misses

- `tools/wave-parent-settle.py`: only read `with open(args.receipt, encoding='utf-8')` (:75) — no write call.
- `tools/wave-route-mix.py`: no `open(`/`write_*`/`os.replace`/`os.rename`/`os.symlink` text at all.
- `tools/write-path-census-v3.py` / `write-path-census-v2.py`: only read-mode `open(...)` (:277, :322 in v3; :46 in v2). Note v2 scores `v2_sites=3` on the *v3 source* because v2 line-matches the regex literals `\.write_bytes\s*\(` etc. inside v3's pattern strings — a concrete v2 false-positive class with no write behind it.

## v3 vs v2 on the live tree (same 25 files)

- Totals: v3 `sites=111`, `unflagged=3`; v2 `sites=117`, `unflagged=2`.
- v3 finds write calls v2 cannot see on the same file: `repeat-control.py` 6 vs 3, `pin-disposition.py` 10 vs 7, `evidence-disposition.py` 7 vs 6 (variable/`Path` receivers).
- v2 over-counts where v3 does not: `witness-metadata.py` 13 vs 10, `registry-check.py` 8 vs 4, `write-path-census.py` 5 vs 2, `write-path-census-v3.py` 3 vs 0 — all line-regex hits with no write call (including matches on regex/source-string text).
- v2 has no `--file` mode at all (`write-path-census-v2.py:87-95` exposes `--selftest`/`--fixtures` only); the contrast above was produced by importing `classify_text`, the same function `census/measure.py` embeds. Running `python3 tools/write-path-census-v2.py --file <f>` is a usage error (exit 2).

## Confidence and remaining unknowns

- Observed (direct command output, reproducible): the per-file totals, the 10 expected sites with their line numbers and record booleans, the 0 parse errors, the tool sha256s, and the v2 contrast counts.
- Observed but interpretive: `context-capture.py:1682/:1685` are scratch writes semantically (mkdtemp chain at :1624) while v3 scores them unflagged — grounded in source lines, consistent with the contract's `declared_scope_limit`, not a counter bug claim.
- [INFERENCE] The two v3-unflagged-but-scratch sites would move `unflagged` from 3 to 1 if `case_dir` were folded; the contract does not require that and I make no pass/fail claim for C2 — that is the L1 counter's single run at the measurement revision.
- Out-of-model write forms (checked, not hidden expected-value writes): v3 recognizes only `open` with a write mode, `.write_text`/`.write_bytes`, `os.replace`/`os.rename` (both args) and `os.symlink` (`tools/write-path-census-v3.py:112-140`, docstring :12-13). The tree also contains `shutil.copy*`/`copytree` 9 lines, `os.remove` 9, `.mkdir` 41, `os.makedirs` 30, `.chmod` 5, `NamedTemporaryFile` 3, and 0 `os.link`/`os.unlink`. The `shutil.copytree` destinations (repeat-control.py:788, :797, :802, :807, :818, :832) are all under the `/tmp` `scratch` root; the non-scratch copies land on `mutate-and-run.sh` (mte-interop.py:280), a `*.spec` file (mte-interop.py:341) and `tools/registry.json` (registry-check.py:1046) — none is an expected-value filename, so no expected-value destination in this tree is hidden behind an unmodeled form. This is a name/line audit, not a proof of the recognizer set's completeness.
- Not measured by me (and deliberately so): no counter was run at the tip. `C1`/`C2` pass/fail is the L1's single default-mode run at the measurement revision.

## Lane state and contract amendments observed while scouting (not my edits)

`tools/` stayed clean and byte-stable for the whole run: `git status --porcelain tools/` empty, `git diff d4ee4e63..b37ce97 -- tools/` empty, and both tools keep their contract shas (`v3 095924a7…ef0279`, `v2 40228532…d878b`). The per-file table and the 10 sites are therefore computed against the pinned tool bytes at both revisions.

Meanwhile the lane advanced from `d4ee4e63` to `b37ce97` ("round-41: C1 records reconciliation + C2 write-path-census-v3") and `.ufo/evidence/round-41/contract.json` was amended after my first read. Amendments `A1`–`A5` re-pin the C1/C2 counters and the C2 fixtures; at the time of writing (`A5` is in the working tree, uncommitted) the contract pins are

```
claims.C1.counter_sha256   9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd
claims.C2.counter_sha256   83268eff97048cd4223a6f015b901c5efbde15d7b0d506bd40e5611b373ce94c
claims.C2.fixtures_sha256  20b6254d39a75fb9b09b783131a7cdcaf360c36642e39424343166515aa26329
claims.C2.tool_sha256      095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279
```

and `sha256sum .ufo/evidence/round-41/{calibration/measure.py,census/measure.py,census/fixtures.json}` returns exactly those three values. This supersedes the earlier version of this note, which reported the working-tree bytes as differing from the frozen pins: the difference was the amendment path (pins moved onto the new bytes), not drift against a fixed pin. Frozen-at-dispatch values were `f00917dd…` / `5d57c709…` / `a4123ce3…`.

Consequence for my control: the `--selftest` behind "Tool identity observed" ran against whatever `census/fixtures.json` bytes were present at that moment, and `A2` changed that file afterwards. It is evidence that v3 passes on the fixtures present at run time, not on the originally frozen ones; the per-file census is unaffected because it reads `tools/*.py` only.

## Durable evidence locus

Every number here is inlined (25-row totals table, 10 site rows, both control outputs) and nothing cited lives under `.ufo/waves/*/scratch*/`. Checked at writing time: `.ufo/waves/round-35/` in this lane repo holds only `w1/`, `w2/`, `residual/` and the dispatch/spec/validate files — no `scratch/` or `scratch-evidence/`; `git cat-file -t 4efaf63` → `fatal: Not a valid object name 4efaf63`; `grep -rl ScoutLiveCensus .ufo/waves/round-35` → no match. The round-35 checkpoint-based recovery path described by peer seats is not present in this checkout, and this seat needs nothing from it.

Report: .ufo/waves/round-41/w1/ScoutLiveCensus.md
