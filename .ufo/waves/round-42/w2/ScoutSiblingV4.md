# ScoutSiblingV4 — v4 census over sibling-lane tools (round 42, wave 2)

Attacked: `tools/write-path-census-v4.py` (sha256 `784de4c0…fe122fe5`, landed in `5f739ac`; lane HEAD `a21845f`) against `write-path-census-v3.py` (sha256 `095924a7…0279eef0279`) on sibling code it was never tuned on.
Siblings read-only: kotodama `21e6a7f` (25 files), tsukuroi `564db0b` (51 files), kumitate `be4a820` (no `tools/` directory, so skipped). Python 3.14.8. Access date 2026-10-25.
Per file: `python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v4.py --file <f> --json` and `python3 -I …/write-path-census-v3.py --file <f>`. Sites were joined on (lineno, kind) by a throwaway script in `/tmp/tameshi-r42w2-ScoutSiblingV4-run`, which has since been deleted.

## Findings

**F1: no crashes.** Across 76 files, 243 write sites and 15 expected-value sites there was no non-zero exit, no stderr and no `parse-error` record from either v3 or v4. No expected-value site appears in v3 but is missing from v4. `--selftest` printed `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`.

**F2: two sites flip, and v4 is right about both.** Each one is v4 `scratch=1` where v3 had `unflagged=1`. No site flipped to `explicit_out`.
- `kotodama-shokunin/tools/check-gate-battery.py:1255` writes `(malformed_root / "fake-gate" / "r9-pre" / "expected.json").write_text(...)`.
- `kotodama-shokunin/tools/check-gate-battery.py:1304` writes `(aggregate_root / "expected.json").write_text(...)`.
- Both sit inside `with tempfile.TemporaryDirectory(prefix="gate-battery-baselines-") as tmp:` / `root = Path(tmp)` at `check-gate-battery.py:967-968`, with `malformed_root = root / "malformed-root"` (`:1253`) and `aggregate_root = root / "aggregate-root"` (`:1300`). These are scratch writes, so v3's unflagged result was a false positive.

**F3: the flips come only from the depth cap.** None of v4's three new resolution steps causes either flip.
- The cause is `MAX_DEPTH` going from 4 to 8 (v4 `:71`, v3 `:43`). Swapping the cap alone in /tmp copies settles it:
  - v3 at depth 8 gives `:1255 … scratch=1 unflagged=0` and `:1304 … scratch=1 unflagged=0`.
  - v4 at depth 4 gives `:1255 … scratch=0 unflagged=1` and `:1304 … scratch=0 unflagged=1`.
- The flips need more depth because the chain is long. `:1255` is three `/` operations, then the name `malformed_root`, then `root / …`, then `root`. v3 stops at depth 5 before reaching `Path(tmp)` and the `TemporaryDirectory` binding.
- The three new steps (attribute binding, method-return fold, output-flag trace) add 0 flips on 76 sibling files.
- The output-flag step does fire once: `tsukuroi-shokunin/tools/run-receipt.py:115` `open(a.out, 'w')` gets `explicit_out=True` with resolved text `ap.parse_args()/out argparse --out`. That is correct (`--out` at `:65`), but the site is not an expected-value write, so it changes no counter.
- v4's docstring (`:15`) says it "keeps v3's walk and adds three bounded resolution steps". The depth change appears only in the Scope paragraph (`:36`). Any wave-1 record that credits a sibling improvement to the attribute or output-flag steps would be wrong.

**F4: the depth cap still decides results, and the next site over is just past it.** `check-gate-battery.py:1323` writes `(advisory_base / "expected.json").write_text(...)`, where `advisory_base = write_baseline(advisory_root / …)` (`:1319`). It is under the same `TemporaryDirectory`, so it is scratch. v4 stock reports `scratch=0 unflagged=1`. v4 with `MAX_DEPTH = 16` (/tmp copy) reports `:1323 … scratch=1 unflagged=0`. A scratch verdict depends on how long the chain is, so v4's `unflagged=0` is no more robust than v3's was.

**F5: none of the 13 sites v4 still calls unflagged is a hidden expected-value update.** v3 reports all 13 the same way.

| Sites | Real destination | Why v4 misses it |
|---|---|---|
| `check-gate-battery.py:996`, `:1050` | `base` / `fixture` parameters of the nested defs `write_baseline` (`:978`) and `write_registry_fixture` (`:1044`); every caller passes a path under `root` from the temp dir (`:1076,1090,1151,1171`) | parameters of nested functions are not traced (`_param_args` only handles module functions, and only for the output-flag step) |
| `check-gate-battery.py:1323` | scratch (F4) | depth cap 8 |
| `exercise-handoff-e2e.py:1757,1776,4466,4490,4521,4587` | e.g. `:4483-4484` `with tempfile.TemporaryDirectory(...) as control_dir:` / `superseded_root, _ = v3_freezed_copy(fixture, control_dir, …)`; then `victim = superseded_root / baseline_rel`, so scratch | tuple-unpacking assignment is not bound (`_bind`, `:342-353`, takes a single `Name` target only); resolution then takes the literal text of `baseline_rel` (`reports/round-*/handoff/expected.json`) |
| `exercise-handoff-e2e.py:1586`, `:4132` | `v1_freeze(root, target_dir)` / `v3_freeze(...)` write `Path(target_dir) / "expected.json"`. Callers pass `args.freeze` (`--freeze DIR`, `:4633`, `:4669`, `:4708`) or a fixture path under a temp workdir (`:1636`, `:4197`) | an explicit operator-chosen destination like `--out`, but `--freeze` is not in `OUTPUT_FLAGS` (`:68`) and `FLAG_RE` (`:66`) covers only `--update*`. Under v4's every-caller rule the scratch caller would block `explicit_out` anyway |
| `tsukuroi-shokunin/tools/mutants-btrfs-space-r30.py:358` (`os.rename`), `:359` (`os.symlink`) | `full = os.path.join(d, r['snapshot'])` with `d = os.path.join(work, name)` (`:329`); every `run_case` call passes `work = tempfile.mkdtemp(...)` (`:382-395`), so scratch | the scratch marker is not followed through module-function parameters. `expected=1` is itself spurious: `EXPECTED_RE` (`:57`) matches the dict-key text `'snapshot'`, because a Call's resolved text includes its own source (`:200-205`) |

## Remaining unknowns
- I did not check whether any wave-1 record actually credits sibling or lane flips to the attribute or output-flag steps rather than the depth cap. That is for the records reviewers.
- No tools were installed or upgraded.

## Verdict
SURVIVES: v4 does not crash on 76 sibling files, and both of its scratch reversals of v3's unflagged result are correct. The caveat is that both come from the depth cap (4 to 8) alone, not from v4's three named steps, and line 1323 shows the depth cap still decides results.
