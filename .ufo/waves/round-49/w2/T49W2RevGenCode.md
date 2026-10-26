# T49W2RevGenCode — code review of tools/pbt-staged-id.py (wave 2, falsify)

Item: interface conformance with contract claims.C2.generator_interface, determinism,
temp hygiene, guard-call timeouts, error paths, stdlib-only.
Target: `tools/pbt-staged-id.py` at REV `f181a961ae44061af486f600e5ea257d2baf78f8`
(988 lines; scratch extraction verified byte-identical to the REV blob:
`git -C tameshi-shokunin cat-file blob f181a961…:tools/pbt-staged-id.py | cmp - <copy>` → silent).
Gate pin re-verified: `sha256sum tools/staged-id-guard.py` at REV →
`03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` = contract's named gate.
Scratch root `/fast/scratch/hyaku/tameshi-r49/T49W2RevGenCode` (deleted before yield);
receipts copied to `.ufo/waves/round-49/w2/T49W2RevGenCode.receipts/`. No tool installs (none needed).
I did not author the reviewed code; nothing here is a verdict — the deciding run is the L1's.

## Findings

### F1 — MAJOR: unreadable guard exits 1 ("violation") instead of 2 ("setup")
`tools/pbt-staged-id.py:41` (docstring) promises "2 = setup problem (bad arguments, unwritable
dump, unreadable guard)"; contract `claims.C2.generator_interface` says "exit 0 none, 1 violation,
2 setup". `main()` checks only `os.path.isfile` (`:982`) and `run_guard` catches only
`subprocess.TimeoutExpired` (`:773`). An unreadable guard passes `isfile`; `python3 -I` itself
exits 2 with **empty stdout**; `json.loads(b'')` → `answer=None`; `check()` → "stdout is not one
JSON object" → violation, exit 1, with a fabricated counterexample index.
Command (probe, uid 1000):
```
cp tools/staged-id-guard.py $S/probe/noread.py && chmod 000 $S/probe/noread.py
python3 -I tools/pbt-staged-id.py --guard $S/probe/noread.py --seed 1 --cases 1 --dump $S/probe/m2.jsonl
```
Observed (`receipts/noread.out`): `unreadable_guard_exit=1`;
`VIOLATION index=0 exit 2, oracle expects 1`; stderr
`/usr/bin/python3: can't open file '…/noread.py': [Errno 13] Permission denied`;
last line `PBT_STAGED_ID: cases=1 violations=1 counterexample=0 … refusal=1 …`.
Impact on the deciding run: none direct — the frozen counter materializes both guard copies
itself (default 644), so the pristine guard is always readable, and the counter never relies on
the generator's exit-2 path (`pristine_bad` requires exit 0). But the contract-named error path
lands in the wrong exit class and mints a bogus counterexample. Fix is two lines: an
`os.access(guard, os.R_OK)` pre-check in `main()` → 2, and/or `except OSError` around
`subprocess.run` → 2.

### F2 — MINOR: mid-run dump/case-file write errors are uncaught (exit 1 + traceback, not 2)
`run()` guards only the dump **open** (`:793-799`); `dump.write`/`dump.flush` inside the loop
(`:803-806`) and `write_text` of the case files can still raise `OSError` (e.g. ENOSPC) →
unhandled traceback, exit 1, no `PBT_STAGED_ID` last line. The counter would then score
`pristine_bad` (no LAST_RE match) instead of seeing a clean setup refusal. Same setup-family
misclassification as F1; not probed (needs a full filesystem) — cited from code.

### F3 — MINOR: one hygiene gap between mkdtemp and the try/finally
`tools/pbt-staged-id.py:790-791`: `os.makedirs(case_dir, exist_ok=True)` runs before the
`try:` that owns `shutil.rmtree(work)` (`:815-817`); if it raises, the mkdtemp dir leaks.
Improbable (parent created microseconds earlier), hygiene-only. All probes verified clean:
0 leftovers in three separate TMPDIRs (`t1_leftovers=0 t2_leftovers=0 tmp_leftovers=0`) and
`roottmp_leaks=0` for `/tmp/pbt-staged-id-*`.

### F4 — INFO: generator's own class floor (20) is stricter than the frozen contract (10)
`tools/pbt-staged-id.py:66` `CLASS_MIN = 20  # this seat's observed distribution floor (contract: 10)`.
The `SHORT` label it prints is advisory; the frozen counter enforces `CLASS_MIN = 10`. At the
deciding params (seed 4949, 400 cases) the observed distribution is
`indent_1_3=248, indent_4_plus=31, id_4_plus_digits=31, collision=204, no_collision=62,
held=49, unmapped=31, cascade=45, refusal=61, url_form_variant=30, map=104, map_inadmissible=31`
— every class ≥ 30, no SHORT flags (`receipts/r1.out`). Floor met with ≥3× margin.

### F5 — INFO: stdout is not byte-identical across runs (TIME line)
`tools/pbt-staged-id.py:827-828` prints `PBT_STAGED_ID_TIME: seconds=…`, so stdout differs run
to run. The contract pins the **dump** (byte-identical — verified below) and only the **last**
stdout line; the counter matches the last non-empty line only. No impact; recorded so
"deterministic" is not misread as stdout-identical.

### F6 — INFO: hung guard is reported as a violation (exit 1), not setup
`GUARD_TIMEOUT = 60` (`:67`); on `TimeoutExpired` `run_guard` returns `{'exit': 124, 'json': None}`
(`:773-775`) → `check()` → "exit 124, oracle expects …" → violation, exit 1. Coherent with
"stops at the first violation" (a hang is a guard that gives no answer); the counter's kill path
still works (differential `comparable()` differs: pristine answers, mutant times out).
Probe: guard = `import time; time.sleep(600)`, cases=1 → `hang_exit=1` after 60s,
`VIOLATION index=0 exit 124, oracle expects 1`, `orphan_sleepers=0` (subprocess.run kills the
child — no leak), dump line present (`receipts/hang.out`).

## Conformance verified (positive column, each with evidence)

1. **Flags**: `--guard --seed --cases --dump --selftest` (`main() :967-975`); required-arg and
   `--cases < 1` → exit 2 (`:977-980`; observed `cases0_exit=2`, `no_cases_flag_exit=2`).
2. **Guard invocation shape**: `[sys.executable, '-I', guard, '--registry', R, '--staged', S]
   (+ ['--map', M]) + '--json'` (`:762-768`) = contract's
   `python3 -I GUARD --registry R --staged G [--map M] --json`.
3. **Own oracle only**: no import/exec/read of the guard's source anywhere (full read + grep);
   interaction is subprocess-only, per contract.
4. **Stops at first violation** (`break`, `:812-813`); the violating case is in the dump
   (probe dumps have exactly counterexample-index+1 lines).
5. **Dump format**: one JSONL line per run `{index, registry, staged, map}`, `sort_keys=True`
   (`:803-806`); compatible with the counter's `load_dump` including map-as-list
   (`rec_map_setup_refusal` emits lists; counter accepts dict/list/str/int).
6. **Last line**: `PBT_STAGED_ID: cases=%d violations=%d counterexample=%s classes=%s`
   (`:829-831`) matches the contract text and the counter's
   `LAST_RE = ^PBT_STAGED_ID: cases=(\d+) violations=(\d+) counterexample=(\d+|none)\b`.
7. **Exits**: 0/1/2 implemented (`run() :833`, `main() :978-983`); guard missing → 2,
   dump-is-dir → 2, bad args → 2 (all probed: `guard_missing_exit=2`, `dump_is_dir_exit=2`).
8. **Determinism**: two clean sequential runs at seed 4949 / 400 cases → dumps byte-identical
   (`cmp` silent; sha256 `ca62402bc6125cb8003b3854a30bef829d29d5c6656be1f8a516ca2828a7cd28`
   for both), stdout identical modulo the TIME line, and identical to an earlier independent
   clean run. An initial apparent nondeterminism was my own concurrent probe deleting the
   shared scratch TMPDIR mid-run — the VIOLATION stdout names the deleted
   `pbt-staged-id-7jtdf_br/case/registry.md`; probes re-run isolated. Not a generator defect.
9. **Temp hygiene**: single `mkdtemp` under TMPDIR (`:787`), `rmtree` in `finally` (`:815-817`)
   and on dump-open failure (`:797`); TMPDIR honored (probes redirected it); zero leftovers.
10. **Timeouts**: `GUARD_TIMEOUT=60` on every guard call (`:772`).
11. **stdlib only**: imports `:45-54` (argparse, json, os, random, re, shutil, subprocess,
    sys, tempfile, time).
12. **Oracle fidelity at these bytes**: 400/400 pristine cases pass the generator's full-field
    oracle (exit, verdict, exact field set, all map-reason projections) — two independent clean
    runs, `violations=0`. The counter's weaker oracle (exit-2-ness, collisions, registry_rows,
    staged_rows) checks a subset of what the generator already verified → `oracle_disagree=0`
    expected at the deciding run.
13. **Reason projection fidelity**: `reason_classes` patterns match the guard's exact prose for
    all 9 categories (`injective`, `does not carry`, `collide with registry ids`, `still staged
    ids`, `below the safe floor`, `does not cover`, `on itself`, `undocumented row`,
    `held document off`), and category order matches `validate_map`'s append order — verified
    line-by-line against `tools/staged-id-guard.py` at REV; empirically all 31
    inadmissible-map cases in the clean run passed.
14. **Field-set exactness**: analysis mode = 18 fields + verdict + registry/staged_sha256 =
    the guard's JSON exactly; map mode adds the 12 map fields + analysis_refused + refused.
    `check()` enforces exact set equality both directions (`:283-289`).
15. **Class predicates** in `case_classes` are token-identical to the frozen counter's
    (indentation bands, id-length ≥5 at indent ≤3, collision/held/unmapped/cascade from the
    analysis JSON, refusal on exit 2, map/map_inadmissible, url_form_variant via normalized
    URL sets) — so the generator's CLASS lines predict the counter's recount.

## Residual risk / verification gaps
- Oracle fidelity is proven only on the 400 cases seed 4949 draws; other seeds could reach
  shapes where oracle and guard diverge (e.g. `document_key` edge forms not generated). The
  deciding run settles it.
- Hidden panel kills not assessed (not my item; panel unread per bounds).
- F2 cited from code, not probed (would require a full filesystem).
- Probe receipts were produced against the scratch extraction, verified byte-identical to the
  REV blob before use.

## Summary
- F1 MAJOR: unreadable guard → exit 1 + fabricated counterexample instead of exit 2 (docstring
  :41 and contract say setup); probe receipt `noread.out`; unreachable in the deciding run
  (counter materializes readable copies) but a real interface-conformance defect; 2-line fix.
- F2 MINOR: mid-run dump/case write OSError uncaught → traceback exit 1, not 2 (code-cited).
- F3 MINOR: `os.makedirs(case_dir)` outside the try/finally can leak the mkdtemp dir (edge).
- F4/F5/F6 INFO: generator's CLASS_MIN=20 vs contract 10 (advisory; all classes ≥30 observed);
  stdout carries a non-deterministic TIME line (dump + last line remain pinned); hung guard →
  violation exit 1 after 60s with no orphan processes.
- Verified: flags, guard CLI shape, own-oracle-only, first-violation stop, dump format, last
  line, exits 0/1/2, stdlib-only, TMPDIR-only hygiene with clean teardown, 60s guard timeout.
- Determinism: same seed → byte-identical dumps (sha256 ca62402b…), stdout identical modulo
  the TIME line; earlier apparent divergence traced to my own concurrent probe wiping the
  shared scratch TMPDIR, not the generator.
- Pristine fidelity: 400/400 cases pass the generator's full-field oracle; class distribution
  all ≥30 ≥ contract's 10; reason-projection and field-set checks match the guard exactly.
- Guard pin intact at REV (sha256 03a796c5…). No verdicts issued; deciding run is the L1's.
