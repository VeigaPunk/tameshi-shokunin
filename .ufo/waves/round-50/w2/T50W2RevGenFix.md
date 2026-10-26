# T50W2RevGenFix — review of routed item R49.1 (generator error-path fix)

Seat: T50W2RevGenFix (leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`e3729de862f73ae080d98fcf522a7081ce16e40a`, content revision `80ea77e99e239982ab0b93e416645ef2359725d3`.
Item: review the fix commit `43bfa7ae` (diff `43bfa7ae^..43bfa7ae -- tools/pbt-staged-id.py`)
against R49.1's asks (`.ufo/evidence/round-50/c1/defects.json` R49.1; routed text at
`corpus/lessons/round-49-verifier-spotcheck.md:122`; spec `.ufo/waves/round-49/w2/T49W2RevGenCode.md`
F1–F3; executor report `.ufo/waves/round-50/w1/T50ExecGenFix.md`).
Scratch `/fast/scratch/hyaku/tameshi-r50/T50W2RevGenFix` (deleted before yield); receipts copied to
`.ufo/waves/round-50/w2/T50W2RevGenFix.receipts/`. No tool installs (none needed; pacman paused).
No verdicts issued — this is a review; deciding runs are the L1's.

Identity checks: `43bfa7ae` is post-base (`git merge-base --is-ancestor e3729de8 43bfa7ae` → 0),
touches `tools/pbt-staged-id.py`, and is an ancestor of the content revision (→ 0). The blob at
`80ea77e9:tools/pbt-staged-id.py` = sha256 `a6e1253ad3542303ca31d66de69ccaa1caf32576c128dc6756daa332b9c8561e`
= the w1 deliverable verbatim; base blob `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05`.
Guard pin at base/tip/working tree: sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` (the contract's named gate).

## Ask-by-ask check (R49.1: "each fix needs a selftest case that fails before it")

Red run = base bytes plus exactly the four new cases (two imports + case block; `diff base.py
base-plus-tests.py` shows nothing else), as the w1 executor specified:

```
TMPDIR=$S/tmp-red python3 -I base-plus-tests.py --selftest
```
→ exit 1, `PBT_STAGED_ID_SELFTEST: cases=35 failed=4` — the four new cases FAIL, all 31
pre-existing cases PASS. Byte-identical to w1's `red-before.stdout` (cmp silent).

Green run at the content revision:

```
TMPDIR=$S/tmp-green python3 -I fixed.py --selftest
```
→ exit 0, `cases=35 failed=0` (twice; deterministic). Byte-identical to w1's `green-after.stdout`.

| Ask | Fixed-code evidence | Base contrast |
|---|---|---|
| F1: unreadable guard exits 2 (setup), never 1 or a fabricated counterexample | `guard_problem` (`tools/pbt-staged-id.py:878-889`: `os.path.isfile` + `os.access(guard, os.R_OK)`), wired in `main()` (`:1110-1113`); `run_guard` maps `OSError` from `subprocess.run` to setup (`:789-790`). Probe: `chmod 000` copy, seed 1, 1 case → exit 2, stdout 0 bytes, stderr `pbt-staged-id: guard is not readable: …`, no dump, no work root (receipt `noread.out`/`noread.err`) | Same probe on base → exit 1, `VIOLATION index=0 exit 2, oracle expects 1` + one dump line (receipt `noread2.out`) — reproduces round-49 F1 and w1 `red-before-f1.stdout` |
| F2: mid-run dump/case-file write failures are setup (exit 2), not an uncaught traceback | `SetupProblem` (`:81-86`) carries every setup failure to one exit path; guarded dump writes (`:838-844`), case-file writes (`:773-783`), dump close may fail without replacing the setup message (`:853-857`). Selftest cases `dump-write-failure-is-setup` (real `/dev/full`, `:1071-1082`) and `case-write-failure-is-setup` (`:1051-1057`) PASS | Both FAIL on base (red 4/4) |
| F3: no work-root leak between `mkdtemp` and the `try/finally` | `workspace()` context manager (`:799-818`) creates the temp root, case dir, and removes the root in one `finally` covering every later failure; `run()` uses it (`:821-830`). Case `case-dir-failure-removes-work-root` (`:1059-1069`) asserts no new `pbt-staged-id-*` root after an injected case-dir failure; PASS | FAIL on base (no `workspace`; `globals().get('workspace')` is None) |
| Each fix has a selftest case that fails before it | the four new cases live at `tools/pbt-staged-id.py:1019-1090`; they call `main()`/`run_guard()`/`workspace()` directly — they reach the production code paths end-to-end (round-50's selftest-reaches-measure criterion), unlike round-49's selftests | all four FAIL on base bytes (35/35 split: 31 pass, 4 fail) |

No work-root leftovers after any probe (0 `pbt-staged-id-*` in TMPDIRs and `/tmp`).

## Interface and RNG draw order — unchanged

Capability run, seed 4949 / 400 cases, guard pin `03a796c5…`, on base and fixed:

```
TMPDIR=$S/tmp-cap-{base,fixed} python3 -I {base,fixed}.py --guard guard_base.py --seed 4949 --cases 400 --dump …jsonl
```
- Last stdout line byte-identical on both: `PBT_STAGED_ID: cases=400 violations=0 counterexample=none
  classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31`
  (= the no-harm monitor's exact string; also equals w1 `base-capability.stdout`).
- Dumps byte-identical: sha256 `ca62402bc6125cb8003b3854a30bef829d29d5c6656be1f8a516ca2828a7cd28`
  on both (the round-49 frozen dump hash). An identical dump = identical per-case draws ⇒ the RNG
  draw order is unchanged: `random.Random(seed)` + one `rnd.shuffle(order)` (`:823-825` = base
  `:785-787`), `RECIPES` block byte-identical between base and fixed.
- Interface unchanged: same five flags `--guard --seed --cases --dump --selftest` (`main()` `:1096-1114`);
  guard argv shape `[sys.executable, '-I', guard, '--registry', R, '--staged', S] (+['--map', M]) + '--json'`
  (`:771-784`); exit-2 surface identical including byte-identical stderr for a guard that is a
  directory (`cmp` silent on `guarddir` probes); last-line `PBT_STAGED_ID` format unchanged.
- Only non-comment code changes are the three fixes + `SetupProblem` + `workspace` + `guard_problem`;
  no oracle, `check()`, classifier, recipe or CLI text was touched (full `base-vs-fixed.patch`,
  286 lines, in receipts).

## C1-row support (not a verdict)

The w1 hand-off's three proposed evidence items resolve at the content revision: `tools/pbt-staged-id.py`
lines 878-886 (inside `guard_problem`, 878-889) carry `os.path.isfile`-keyed new text; lines 40-42
carry `unreadable guard`; lines 799-803 sit inside `workspace` (800-818). All three excerpts are
absent at base `e3729de8` and the file is touched by post-base commit `43bfa7ae`. Whether the row is
`fixed` is the C1 counter's/deciding run's call.

## Residual risk / verification gaps

- `unreadable-guard-is-setup` and `dump-write-failure-is-setup` skip where the environment cannot
  exercise them (uid 0; no `/dev/full`). Both ran here (uid 1000, Linux).
- The selftest mutates the module-global `tempfile.tempdir` inside a try/finally restore
  (`:1029-1030`, `:1084`) — contained, but a global mutation.
- I re-derived the red run by porting the four cases verbatim from the fixed file; the port is
  faithful (diff shows only the imports + block) and my red/green outputs are byte-identical to w1's
  receipts, but the four cases' names/results are the only thing asserted about the base behavior.

## Summary

- The fix at `43bfa7ae` (in the tree at `80ea77e9`, byte-exact vs the w1 deliverable) meets every ask
  of R49.1: F1 unreadable guard → exit 2 with no fabricated counterexample; F2 write failures → exit 2;
  F3 work-root leak closed; and each fix has a selftest case that fails on the base bytes.
- Red/green reproduced independently: base+tests `cases=35 failed=4`; fixed `cases=35 failed=0`; both
  byte-identical to w1's receipts. Unreadable-guard probe: base exit 1 + VIOLATION; fixed exit 2,
  empty stdout, clean message, no dump, no leftovers.
- No interface or RNG change: seed-4949/400 capability line byte-identical, dumps byte-identical
  (sha256 ca62402b…, the frozen hash), recipes/RNG code identical, argv/flags/last-line unchanged.
- Commit ancestry verified: post-base, touches `tools/pbt-staged-id.py`, ancestor of the content revision.
- No tool installs; receipts in `T50W2RevGenFix.receipts/`; scratch deleted.
