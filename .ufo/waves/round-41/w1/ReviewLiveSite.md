# ReviewLiveSite — C2 live variable-destination sites in `tools/repeat-control.py`

Round 41, attempt 2. Freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`.
Seat: read-only. Contract read first: `.ufo/evidence/round-41/contract.json`.

**Pin state at review time.** The *committed* contract (blob at `d4ee4e6`) carries the original pins
(`census/measure.py 5d57c709…`, `census/fixtures.json a4123ce3…`, `calibration/measure.py f00917dd…`). The **working-tree**
contract has since gained an `amendments` array (A1/A2/A3, mtime 03:42) re-pinning the two C2 files to `83268eff…` and
`20b6254d…` and adding `mutant_symlink_arg_killed=1` to C2's target. Both states were verified. **Nothing in this report
changes between them**: `tools/repeat-control.py` and `tools/write-path-census-v3.py` are untouched by the amendment, the live
half of the counter's logic is byte-identical (A2 only inserts the third mutant and shifts later line numbers by +2), and I
quote both line sets below.

Blob identity (so the cited lines are the same at base, freeze and worktree):
`git rev-parse {a3d6c69,d4ee4e6}:tools/repeat-control.py` = `70c91e7e6b1957d6b1eaa106b2be2659d042cfd7` for **both** revisions, and
`git hash-object tools/repeat-control.py` = `70c91e7e…` in the worktree; `git diff base freeze -- tools/repeat-control.py` is
empty (the only file added between base and freeze is `tools/write-path-census-v3.py`, 346 lines).

## 1. Exact sites (confirmed)

| # | site | line | source |
|---|------|------|--------|
| A | variable-destination `open()` | **811** | `        with open(duplicate_path, "wb") as handle:` |
| B | `os.symlink(...)` whose destination is an `expected.json` | **820** (call node; destination argument on **822**) | `820:        os.symlink(` / `821:            os.path.join(snap_stable, "expected.json"),` / `822:            os.path.join(tamper_manifest_symlink, "expected.json"),` / `823:        )` |

Counter-side note: `_record` stamps the **Call node's** `lineno`, i.e. 820, not the destination argument's 822. Both land inside
the counter's windows (`open` 805–815, `os.symlink` 815–825; pinned counter `measure.py:224` and `:226`, pre-amendment `:221`
and `:223`), and v3 finds exactly two `expected=True` records in the whole file (811 `open`, 820 `os.symlink`); the second
symlink at 834 (`run-2.stdout` → `run-1.stdout`) is `expected=0`, so the window selection is unambiguous.

## 2. Assignment that makes each site scratch

A — `open(duplicate_path, "wb")` @811. Scratch provenance chain (all hops consulted inside `MAX_DEPTH=4`):

- **597** `    scratch = tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir="/tmp")` — supplies the
  `/tmp`, `tempfile`, `mkdtemp` and name-`scratch` markers.
- **806** `        tamper_duplicate_key = os.path.join(scratch, "snap-tamper-duplicate-key")` — **the hop that makes the
  destination scratch-rooted**.
- **808** `        duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")` — the assignment that puts the
  `expected.json` literal on the destination path at all.

B — `os.symlink(src, dst)` @820, destination arg @822:

- **597** as above.
- **817** `        tamper_manifest_symlink = os.path.join(scratch, "snap-tamper-manifest-symlink")` — **the hop that makes the
  destination scratch-rooted**.
- the `"expected.json"` literal is inline in the destination argument at **822** (no separate assignment).

Measured with v3's own `classify_source` on blob `70c91e7e` (`importlib` load of `tools/write-path-census-v3.py`, sha256
`095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` = contract `tool_sha256`, unchanged by A2):

```
811 open       expected=1 scratch=1 unflagged=0
820 os.symlink expected=1 scratch=1 unflagged=0
```

Counterfactual (scratch provably load-bearing, not incidental): replacing the join root at 806 with `"/elsewhere"`, and
separately at 817, flips only that site to `expected=1 scratch=0 unflagged=1`. `expected` is unchanged, so
`live_var_scratch_v3` / `live_symlink_scratch_v3` are exactly what pin the 597→806/817→811/822 chain. Captured traces
(truncated) show the consulted segments:
`duplicate_path → os.path.join(tamper_duplicate_key, "expected.json") → os.path.join(scratch, …) → scratch → tempfile.mkdtemp(… dir="/tmp")`.

Predicted live fields at the measurement revision (contract target satisfied; I did not run the counter):
`live_var_lineno=811 live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0
live_symlink_lineno=820 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0`.

## 3. Can v2's line pattern connect the destination to `expected.json` there? — **No, at both sites, for two different structural reasons.**

v2 is strictly per-line: `WRITE_RE` and `EXPECTED_RE` are both applied to the *same* `text.splitlines()` element, with no scope,
no AST and no binding table (`tools/write-path-census-v2.py:32-42`, loop at :36, both regexes at :40). Running the counter's own
regex pair (pinned `measure.py:39` and `:46`; pre-amendment `:37` and `:44`; byte-identical semantics to v2's) on the exact lines:

| line | source | V2_WRITE_RE | V2_EXPECTED_RE |
|------|---------|------------|----------------|
| 808 | `duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")` | 0 | 1 |
| **811** | `with open(duplicate_path, "wb") as handle:` | **1** | **0** |
| 819 | `os.remove(os.path.join(tamper_manifest_symlink, "expected.json"))` | 0 | 1 |
| **820** | `os.symlink(` | **0** | **0** |
| 821 | `os.path.join(snap_stable, "expected.json"),` | 0 | 1 |
| **822** | `os.path.join(tamper_manifest_symlink, "expected.json"),` | **0** | **1** |

- **Site A (811):** v2 sees the write (`open(..., "wb")`), but the destination token is the bare name `duplicate_path`; the only
  quoted literal on the line is `"wb"`, which `EXPECTED_RE` rejects. The `expected.json` literal is at 808 and the scratch root
  at 597/806. A single-line scan cannot join them → `live_var_expected_v2=0` (the resolution miss the contract describes).
  `live_var_sites_v2=1` is emitted but not asserted by the predicate.
- **Site B (820/822):** this is a **site** miss before it is a resolution miss. `os.symlink` is absent from `V2_WRITE_RE`
  entirely, so `live_symlink_sites_v2=0`; and the write form (820) and the `expected.json` literal (822) are even on *different*
  lines, so no line-local pairing could fire for this call whatever the regex set. Line 822 alone shows the reverse split
  (`WRITE=0, EXPECTED=1`): literal present, write form absent.

## 4. Review observations

- **Medium (residual strength, not a failure):** v3's `expected` signal does not require *name* resolution for either site's
  destination when the literal sits inside the destination expression itself; only `scratch` does. Measured on the live file with
  the counter's own `RESOLVE_MUTANT` (`bound = None`): the expected records collapse to `820 os.symlink expected=1 scratch=0` and
  the 811 `open` record leaves the expected set entirely (`live_var_resolved_v3=0`). So the resolve mutant is killed by the
  *open-site* live checks and by `live_symlink_scratch_v3`, never by `live_symlink_resolved_v3`.
  A2's third mutant (`os.symlink` dest `node.args[1]` → `node.args[0]`) closes part of this for the fixtures — it fails
  `symlink_unflagged` (measured: `(unflagged=0, expected=0)`), proving the destination **argument** is selected — but it still
  does not test name resolution for the symlink destination.
- **Low (`literal_unflagged` is non-discriminating):** measured with the `resolve` mutant, `literal_unflagged` stays
  `(unflagged=1, expected_sites=1)` — identically for the committed fixture (`a4123ce3`, all-literal `os.replace`) and the
  amended one (`20b6254d`, re-rooted at `"tests/fixtures"`). Cause: `_resolve`'s `Call` branch (`tools/write-path-census-v3.py:58-94`,
  literal branch at :87-93) returns the call's own source segment as trace, so `expected.json` matches from the source text with no
  folding. Likewise `symlink_unflagged` survives the resolve mutant unchanged `(1, 1)`. The name-resolution capability is therefore
  pinned by `var_unflagged` + `scratch_var` (both fall to `(0, 0)`) and by the live open site, not by the "literal" fixture. The
  field name `literal_unflagged`/`literal_expected` overstates what that fixture proves. A2's re-rooting did not change this.
- **Info:** on the amended pins I re-derived the fixture half without running the counter: `fixtures_ok=True`
  (`var 1/1, symlink 1/1, literal 1/1, scratch_var_unflagged 0`) and all three mutants are killed by the fixtures
  (`resolve` → var `(0,0)`, scratch_var `(0,0)`; `symlink` → symlink `(0,0)`; `symlink_arg` → symlink `(0,0)`).
  The amended fixtures keep v2's embedded-pattern control at `v2_var_expected=0 v2_symlink_sites=0` (measured), i.e.
  `C2_R41_CONTROL_PASS=false` as the contract's `do_nothing_control` requires.
- **Info:** `live_var_sites_v2` and `live_symlink_sites_v2` are emitted; the asserted live set is
  `live_var_resolved|live_var_scratch|live_var_expected_v2|live_symlink_resolved|live_symlink_scratch|live_symlink_sites_v2`
  (pinned `measure.py:240`, pre-amendment `:237`). Consistent with the frozen target.

## 5. Residual risk / verification gaps

- I did **not** run either counter (contract kill rule; the single deciding run is the L1's, after all reports land). A
  base-revision run cannot exercise the live half anyway (`tool_absent=1`), so the live values above were reproduced directly
  from v3's `classify_source` plus `measure.py`'s `v2_line` regex pair on the identical blob `70c91e7e`.
- Line numbers for `tools/repeat-control.py` are exact for base, freeze and worktree. If the measurement revision moves that file
  (or the census counter is amended again), re-derive: windows 805–815 / 815–825; sites 597 / 806 / 808 / 811 / 817 / 820–822.
- Concurrent lane state (not my edits, verified read-only): `tools/` clean; `.ufo/evidence/round-41/{contract.json,census/measure.py,
  census/fixtures.json,calibration/measure.py}` differ from HEAD and are recorded by the contract's own A1–A3 amendments and by
  `ScoutLiveCensus.md`. My findings are computed against the pinned tools and both counter variants, as stated above.
- Tooling: nothing installed or upgraded (no pacman/uv/npx channel used); contract, lane checkout and Git index untouched
  (my only write is this report; two throwaway `/tmp` files were removed).

## Appendix — self-contained reproducer (no scratch tree, no counter run)

Reads the frozen blob straight out of Git, so it survives any `/tmp` or `.ufo/waves/*/scratch*` sweep. Output below is the
verified run (2026-10-25) and matches every number cited above.

```python
import importlib.util, re, subprocess
L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937"
blob = subprocess.run(["git", "-C", L, "show", REV + ":tools/repeat-control.py"],
                      capture_output=True, check=True).stdout.decode()
spec = importlib.util.spec_from_file_location("v3", L + "/tools/write-path-census-v3.py")
v3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v3)
print("v3 expected records:")
for r in v3.classify_source(blob):
    if r["expected"]:
        print(" ", r["lineno"], r["kind"], "expected=%d scratch=%d unflagged=%d" % (r["expected"], r["scratch"], r["unflagged"]))
V2W = re.compile(r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]|\.write_text\s*\(|\.write_bytes\s*\(|os\.replace\s*\(|os\.rename\s*\(""")
V2E = re.compile(r"""['"][^'"]*(?:\.expected\b|expected\.txt|expected\.json|golden|snapshot)[^'"]*['"]""")
lines = blob.splitlines()
print("v2 per-line (lineno write expected):")
for n in (808, 811, 819, 820, 821, 822):
    print(" ", n, int(bool(V2W.search(lines[n - 1]))), int(bool(V2E.search(lines[n - 1]))))
for old, new in (('tamper_duplicate_key = os.path.join(scratch, "snap-tamper-duplicate-key")',
                  'tamper_duplicate_key = os.path.join("/elsewhere", "snap-tamper-duplicate-key")'),
                 ('tamper_manifest_symlink = os.path.join(scratch, "snap-tamper-manifest-symlink")',
                  'tamper_manifest_symlink = os.path.join("/elsewhere", "snap-tamper-manifest-symlink")')):
    cut = blob.replace(old, new, 1)
    print("severed", old.split(" =")[0] + ":", [(r["lineno"], r["expected"], r["scratch"], r["unflagged"])
          for r in v3.classify_source(cut) if r["lineno"] in (811, 820) or (r["expected"] and r["lineno"] < 830)])
```

Observed output:

```
v3 expected records:
  811 open expected=1 scratch=1 unflagged=0
  820 os.symlink expected=1 scratch=1 unflagged=0
v2 per-line (lineno write expected):
  808 0 1
  811 1 0
  819 0 1
  820 0 0
  821 0 1
  822 0 1
severed tamper_duplicate_key: [(811, True, False, True), (820, True, True, False)]
severed tamper_manifest_symlink: [(811, True, True, False), (820, True, False, True)]
```

The two `severed …` lines are the counterfactual: each site flips to `scratch=0 unflagged=1` only when its own
`scratch`-carrying assignment (806 / 817) is replaced, and `expected` never changes. `git ls-files`/scratch trees are not
consulted by this reproducer.
