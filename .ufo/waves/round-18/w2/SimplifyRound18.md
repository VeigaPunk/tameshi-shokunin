# SimplifyRound18 — YAGNI review of round-18 new/changed code

Seat: TameshiR18.SimplifyRound18 · wave 2 (FALSIFY; axes depth + calibration, operability monitored)
Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` — **no lane edits; this file is the only write**
Scratch: `/tmp/tameshi-r18w2-SimplifyRound18-ptcGaE` (lane clone at the read rev, `*-shokunin` siblings symlinked beside it). All patches and executions below ran there.

Reviewed (sha256 at the read rev):

| file | sha256 |
|---|---|
| tools/registry-check.py | `e072fd3995ca1df1477613f009193e20f3797bc4673ee3045a04afb9927c2899` |
| tools/evidence-disposition.py | `66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44` |
| .ufo/evidence/round-18/defect-probes.py | `99297d9645151dee948291638386f3e9189c7bab590bebda23de6e51dadebeaa` |
| .ufo/evidence/round-18/measure.py | `7ffbcff6ef642ec662b233a90c606db68f0e6a7a41639a46b7d3b5aa8e00ee1f` |
| .ufo/evidence/round-18/coldread/assemble.py | `bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a` |

Summary: **7 proven deletions/dedupes, −74 lines across three tools with every affected selftest green**, plus 3 unproven proposals and one metadata-debt list. Nothing claim-bearing is dead: the C1/C2 receipts do not depend on any line proposed for removal.

## Method and evidence discipline

- Diffs read: `git diff 183f87b 01d586d -- tools/registry-check.py tools/evidence-disposition.py`; `diff -u .ufo/evidence/round-17/measure.py .ufo/evidence/round-18/measure.py`; same for `coldread/assemble.py`; `defect-probes.py` is wholly new in round 18.
- Static scans: vulture 2.16 (`--min-confidence 60`), ruff 0.17.1 (`--select F`).
- **No `lsp` device is mounted** (`read xd://lsp` → `No such tool: xd://lsp`; the mounted-device list contains no lsp). Per the seat role, call-site evidence here is a literal `grep -n` census, **not** semantic reference proof; deletion claims are additionally backed by *executing* the file's own selftest on a patched copy.
- Proof procedure: deletion applied to a scratch copy → `ruff --select F` → the tool's `--selftest`. Git-touching lane selftests ran only inside the clone, launched with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`.
- No tools installed this wave (vulture, ruff, jj, bwrap already present).

## Confirmed deletions/dedupes (proven)

### D1 — `tools/registry-check.py:295-337` + `:347-359`: parse-level nonfinite rejection duplicates the per-field guard

The 43-line block (`_NonFiniteJSONConstant`, `_reject_json_constant`, `_json_marker_path`, `_nonfinite_location`) exists only to special-case `NaN`/`Infinity`/`-Infinity` at parse time. The same commit added the real guard in `registry_errors` (`:234-249`, finite check at `:240`): `math.isfinite(ts) and ts > 0`, with the row name in `timeout_owner`. Other schema-consumed numeric/string fields reject nonfinites by type (`expect.exit` int check `:224-226`, `stdout_contains` string check `:227-233`).

Measured: `json.loads` accepts the three literals and `1e999` → `inf` (`NaN→nan, Infinity→inf, -Infinity→-inf, 1e999→inf`; all `isinstance(int|float)` true, `math.isfinite` false). So `registry_errors` catches every one.

Proven: patched copy (block + special `except` removed; 3 expected strings at `:1491-1494` changed from `non-finite JSON number` to `finite positive number`):

```
patched reg-{nan,inf,neginf,overflow,bool}.json -> exit 2,
  "rows[0] ('timeout-<case>').timeout_s must be a finite positive number"
patched reg-valid.json -> exit 0, "ROW valid-row expect=0 got=0 held", held=1/1
patched registry-check.py --selftest -> exit 0, SELFTEST: PASS (46 cases)
ruff check --select F -> All checks passed
```

Pristine kept as control: NaN fixture → exit 2, `... rows[0].timeout_s (row 'timeout-nan'): non-finite JSON number NaN`.

C2 impact: none. A P09-shaped fixture (row `timeout-nonfinite`, NaN) under the patched tool gives exit 2 with `timeout_s`, `timeout-nonfinite`, no `Traceback` — exactly P09's closed predicate.

Tradeoff (must be stated in the record): after the deletion, a nonfinite constant in a JSON key the schema ignores (e.g. an unknown top-level key) is accepted instead of rejected; every schema-consumed field still rejects. The error text loses the JSON-pointer shape (`rows[0].timeout_s`) but keeps row name + field. Follow-on: the 5-tuple at `:1490-1497` collapses to `(case, token)` once all three messages are the same.

### D2 — `tools/registry-check.py:605-614` + `:692`: `_bounded_communicate`'s `previous_timeout` merge can never contribute

Only production caller passes `timeout_exc` (`:692`); the `=None` default exists solely for the selftest (`:1542`). CPython retains the output buffer **on the Popen object** across `communicate()` calls — `inspect.getsource(subprocess.Popen._communicate)` shows `self._fileobj2output` is created once and only reset `if not self._communication_started` — so the retried `TimeoutExpired` already carries everything the first one carried. `_check_timeout` raises with `b''.join(stdout_seq)`.

A/B measured on a real child (`early`, sleep 2.0; first `communicate(timeout=.15)` consumed `early`):

```
pristine _bounded_communicate(p, e1) -> ((b'early', b''), 1.0s)
patched  _bounded_communicate(p)     -> ((b'early', b''), 1.0s)
```

Patch: drop the parameter and 3 merge lines, change the callsite, drop `as timeout_exc`. −3 lines; patched selftest 46/46.

### D4 — `tools/registry-check.py:570-602`: `_cleanup_row` is two copy-paste bounded loops

The TERM loop and KILL loop differ only in `signum`, deadline constant, and `break` vs `return False`. Extraction used in the proof:

```python
def _signal_until_clean(proc, baseline_children, proc_starttime, signum, deadline):
    ...  # body once
def _cleanup_row(...):
    if _signal_until_clean(..., signal.SIGTERM, time.monotonic() + CLEANUP_TERM_GRACE_S):
        return True
    return _signal_until_clean(..., signal.SIGKILL, time.monotonic() + CLEANUP_FORCE_TIMEOUT_S)
```

Behavior identical (TERM timeout falls through to KILL; KILL timeout returns False). −4 lines; patched selftest 46/46.

**Combined registry-check patch (D1+D2+D4): 1908 → 1845 lines (−63), `--selftest` PASS (46 cases), ruff clean.**

### D7 — `.ufo/evidence/round-18/measure.py:650-651`: unreachable fallback

```python
if not explanation_reasons:
    explanation_reasons = ['no-ledger-entry']
```

The second block is reached only when `matches` is non-empty (`:612-622`: `if not matches: ... continue`), and the loop at `:627-634` appends exactly one element for every entry in `matches` (both branches). Therefore the list is non-empty and lines 650-651 never execute. Delete both.

Related over-general shape (not deleted in the proof, but the same patch could do it): `explanation_reasons` is populated on **every** measure call although only `section_record(..., explain=True)` consumes it (`:540-546`); `--explain` is off by default. Gate the appends on `explain` if the hot path matters.

Proven: patched measure 1659 → 1657 lines, `measure.py --selftest` exit 0, `MEASURE_SELFTEST: 98/98 pass`.

### D8/D9/D10 — `.ufo/evidence/round-18/coldread/assemble.py`: one duplicate assertion, two duplicate literals

- **D8 `:1276-1285`** — the new `trace-inputs-v1 receipt accepted` check re-tests the `inputs` equality already asserted by `inputs unioned from trace receipts` (`:1276-1281`). Only `led["_meta"]["reports_rejected"] == []` is new. Reduce to that condition (or fold it into the preceding check).
- **D9 `:778-785` vs `:969-976`** — the page record dict `{sha256, rev, path, sections, by_start, first_line}` is written twice (once in `assemble()`, once in `load_carry()`). Extract `page_record(sha, rev, path, text, sections)`; both call sites become one line.
- **D10 `:913-920` vs `:1993-2000`** — the `meta["pages"]` comprehension `{sha: {rev, path, buckets}}` is written twice (assemble-time and carry-merge). Extract `pages_meta(pages)`.

Proven: patch with all three → assemble 2105 → 2096 lines (−9); `assemble.py --selftest` exit 0, `SELFTEST: 80/80 pass`; ruff shows only the pre-existing `c_ok` (see carried-over note).

## Proposals (not patched in this seat)

### D6 — `tools/evidence-disposition.py:2198-2203` and `:2226-2231`: identical detached-HEAD probe

Both jj fixtures run the exact same 6-line `subprocess.run(["git","-C",lane,"symbolic-ref","-q","HEAD"], env=_selftest_git_env(), timeout=30)` only to inspect `returncode == 1`. Add `_git_exit(lane, *argv)` beside `_git_raw` (`:2029`, which raises on non-zero and therefore cannot be used for the expected-detached case) and call it twice: 12 lines become 2 calls plus a ~5-line helper (≈5 lines net). Not patched: the full `evidence-disposition.py --selftest` drives jj fixtures and was not rerun by this seat; the narrow check is that selftest.

### D11 — `.ufo/evidence/round-18/defect-probes.py:150-180`: one-function alias

`child_environment` is called only at `:180`, from the one-line `scrubbed_env` alias; the five call sites (`:221,479,885,904,987-988`) all say `scrubbed_env`. Merge the body into `scrubbed_env` (keep the docstring) or rename the callers; either way one symbol and 3 lines go. Literal census: `def child_environment` at 150, its only call at 180.

### D12 — `.ufo/evidence/round-18/defect-probes.py:213,288-307`: host-side `source_links` layer is shadowed in every production run

`main` always sets `SANDBOX_FLEET_ROOT` (`:1055`), and `sandbox_argv` then always mounts `--ro-bind $FLEET /mnt/source` (`:197-200`). bwrap mount order makes that ro-bind cover `$W/source`; the host-side sibling symlinks created at `:300-303` are never visible inside the sandbox. Measured with the probe's exact mount set (planted file at `$W/source/kagi-shokunin`):

```
/mnt/fleet/kagi-shokunin -> ../source/kagi-shokunin
readlink -f /mnt/fleet/kagi-shokunin      = /mnt/source/kagi-shokunin
ls -ld /mnt/source/kagi-shokunin          -> drwxr-xr-x (real fleet dir, not the planted file)
```

Deletion: drop `"source"` from `initialize_sandbox` (`:213`) and `source_links`/`source_link` (`:288,290,292,300-303`); keep the `fleet/<sibling> -> ../source/<name>` links — they resolve through the ro-bind. −~12 lines. Narrow check: `defect-probes.py --rev 01d586ddbc5fcd78659557c4e93a6ee8517b87d1 --only P11` (not run by this seat).

Over-general branch in the same block: `:199 if os.path.commonpath((str(work), str(fleet))) != str(work):` is constant-true for the only caller (work is a `/tmp` mktemp, fleet is the lane's parent), so the nested condition adds nothing over `if SANDBOX_FLEET_ROOT is not None:`. Delete the nested `if` and dedent one line.

## Metadata debt (dead weight, not code deletions)

- `defect-probes.py` `GUARD_SPECS` line fields for P01-P04 (`:56,63,70,77`) are **base-rev** numbers: `445/552/466/96` at `183f87b`, while the anchors sit at `532/645/786/104` at the read rev. Anchoring is byte-exact (`replace_once`), so grading is unaffected, but every receipt prints a wrong `target=tools/...:<line>`. P05-P07 (`:84,91,98` = `82/516/644`) match both revs. Same staleness in hardcoded target strings: P09 `:601 "221-227"` (actual timeout validation `:234-249`), P10 `:786 "306-322,385-387"` (actual cleanup `:570-602`, drain `:605-622`, timeout branch `:685-702`). Proposal: drop the `line` field and compute it from `pristine.find(spec["old"])` when formatting `target`, or update the strings.
- `.ufo/evidence/round-18/measure.py:886` still names its scratch `tameshi-r17-MeasureV2-`, and the `TRACE_*` fixture constants (`:775-781`) still point at `.ufo/evidence/round-17/coldread/traces/`. The synthetic repo is throwaway, so this is cosmetic; rename if touched.

## Carried over dead code (pre-existing, outside the round-18 delta — optional)

Each exists in the round-17 copy and survived the copy to round 18:

- `measure.py:1380` `noinput_ledger` assigned, never used (round-17 `:1328`).
- `coldread/assemble.py:1790` `c_ok` assigned, never used (round-17 `:1664`).
- `evidence-disposition.py:1703` `SELFTEST_V1_DOC` never used (base `:1603`).

Ruff F841 / vulture 60% report them. Fix is dropping the assignment (keep the call if it has side effects), one line each.

## Not proposed — deletions that would harm

- `_signal_process_identity`'s post-pidfd revalidation (`registry-check.py:496-514`): pidfd pins identity, but the second `in_row_scope()` also re-checks ancestry; the `pidfd-revalidates-starttime` selftest is built on it. Keep.
- `_row_cleanup_pending`'s zombie-child branch (`registry-check.py:563-566`): **not dead** — a child that becomes `Z` after `_reap_row_children`'s snapshot but before the pending snapshot makes this return `True`, forcing one more loop iteration to reap it. Deleting it would return “clean” with an adopted zombie left unreaped.
- `_bounded_communicate`'s stream close + bounded `wait` (`:615-621`): load-bearing when an escaped descendant holds the pipe.
- `run_row`'s `leader_finished` branch (`:688-693`): handles the timeout race where the leader exited but a descendant held the pipe; without it a completed row would be mislabeled `timeout`.
- `_enable_child_subreaper`'s `try/except AttributeError` (`:394-397`): unreachable on Linux (prctl is always exported) but four lines of defense against a non-glibc libc; deleting saves nothing meaningful.

## Preserved contract (why the C1/C2 claims are untouched)

- **C2 P09** stays closed under D1: the five literals still exit 2, the message still contains `timeout_s` and the row name, no `Traceback`. Measured on a P09-shaped fixture.
- **C2 P10** is unaffected: the process-cleanup/pipeline code is only *de-duplicated* (D4), not narrowed; `setsid`/`setpgid`/double-fork selftest cases still pass in the patched 46/46 run.
- **C1 depth 8** is outside this review's files (no mutation-runner, case entry, or registry row was touched).
- **No-harm registry**: no row or claim names the deleted helpers; the only callers are in-file (literal census above).
- Scratch proofs are copies; `git -C <lane> status --porcelain` was empty at `01d586d…` before this report was written.

## Evidence log (commands, exits, key lines)

Static:
```
$ vulture tools/registry-check.py --min-confidence 60          -> exit 0 (no findings)
$ vulture tools/evidence-disposition.py --min-confidence 60    -> exit 3: SELFTEST_V1_DOC unused (1703; base 1603)
$ vulture .ufo/evidence/round-18/defect-probes.py ...          -> exit 3: sys.dont_write_bytecode (false positive)
$ vulture .ufo/evidence/round-18/measure.py ...                -> exit 3: noinput_ledger (1380; base 1328)
$ vulture .ufo/evidence/round-18/coldread/assemble.py ...      -> exit 3: c_ok (1790; base 1664)
$ ruff check --select F <5 files>  -> registry / evidence-disposition / defect-probes clean;
                                      measure F841 noinput_ledger; assemble F841 c_ok
```

Baseline selftests at the read rev (clone, hermetic git env for git-touching ones):
```
$ python3 .ufo/evidence/round-18/measure.py --selftest         -> exit 0, 98/98 pass
$ env -u GIT_* python3 .ufo/evidence/round-18/coldread/assemble.py --selftest -> exit 0, 80/80 pass
$ python3 .ufo/evidence/round-18/defect-probes.py --selftest   -> exit 0, PASS (6 cases)
```

Patched-copy proofs (scratch):
```
$ python3 rcpatch/registry-check.py --selftest                 -> exit 0, PASS (46 cases), ruff clean
$ env -u GIT_* python3 rcpatch/assemble.py --selftest          -> exit 0, 80/80 pass
$ python3 rcpatch/measure.py --selftest                        -> exit 0, 98/98 pass
$ python3 rcpatch/registry-check.py --root <clone> --registry reg-nan.json      -> exit 2, finite positive number
   (same for inf, neginf, 1e999, true; valid row -> exit 0, held=1/1)
$ python3 <clone>/tools/registry-check.py --root <clone> --registry reg-nan.json -> exit 2, "non-finite JSON number NaN"
$ P09 shape (row timeout-nonfinite, NaN): exit 2; grep: timeout_s=1, timeout-nonfinite=1, Traceback=0
```

Drain A/B and bwrap shadow outputs are quoted in D2/D12. Combined patched deltas: registry 1908→1845 (−63), assemble 2105→2096 (−9), measure 1659→1657 (−2) — **−74 lines proven removable**, no failing check.

## Limits

- No `lsp` device: call-site claims are literal greps + executions, not semantic reference analysis.
- D6/D11/D12 are proposals: the evidence-disposition jj selftest and `--only P11` were not rerun by this seat; each is marked with its narrow check.
- `git status --porcelain` in the lane was empty before this file was written; no lane file was modified.

**Verdict: holds — the round-18 claims and their receipts are unaffected; 74 lines are provably removable in three tools, and the remaining dead weight is either pre-existing or in defense that should stay.**
