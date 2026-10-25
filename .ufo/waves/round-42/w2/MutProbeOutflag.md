# W2 MutProbeOutflag — outflag mutants of write-path-census-v4.py

Seat `L1Tameshi42.MutProbeOutflag`, 2026-10-25. Target `tools/write-path-census-v4.py`,
sha256 `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5` (equal in the
working tree and at `a21845f5`). Counter runs are **pre-run** `--probe-mutant` at
`--rev a21845f523b75adbd3e3f7a62af91294db224ad9` (control lines, never the measurement).
The lane checkout was not written apart from this file. Scratch copies were under
`/tmp/tameshi-r42w2-MutProbeOutflag-*` and have been deleted.

## Findings

1. **Three of the four assigned outflag mutants survive both detectors**: M1 (`_parse_args_ns`
   always True), M2 (`any()` for `all()`) and M4 (call-site keywords ignored). Both the counter
   oracle and the tool's selftest report a clean pass on them. All three are non-equivalent
   (finding 4). M1 and M2 hide a real expected-value write by marking it `explicit_out`.
2. **M3 (`--input` added to `OUTPUT_FLAGS`) is killed only by the counter**: `F05_inflag`
   (measure.py:149, `parser.add_argument('--input')` at :160). The selftest misses it because its
   input-flag case uses `--source` (write-path-census-v4.py:579, :590), so it never covers the
   `--input` spelling.
3. **Extra variant M2b, which accepts any call site in `_out_flag`'s per-site loop, is killed by
   both detectors.** The counter kills it with `F06_outflag_mixed_callers` (measure.py:164). The
   selftest fails `output_param_one_constant_caller` (v4:594). So the "EVERY in-module call"
   claim (v4:27-28) is pinned for a path-valued parameter. It is not pinned for a
   namespace-valued parameter (the `all()` in `_parse_args_ns`, v4:274), which M2 shows.
4. **The survivors are non-equivalent.** Each witness program below produces a different
   `--file W --json` result from the pristine and mutated tool:

| witness (expected-value site) | mutant | pristine | mutant |
|---|---|---|---|
| `cfg.out` where `cfg = Cfg()` is not a parse_args namespace, but `--out` is declared | M1 | explicit_out=0 unflagged=1 | explicit_out=1 unflagged=0 `argparse --out` |
| `run(opts)` writes `Path(opts.output)/expected.txt`; called as `run(ap.parse_args())` and `run(Cfg())` | M2 | explicit_out=0 unflagged=1 | explicit_out=1 unflagged=0 `argparse --output` |
| `emit("{}", dest_dir=ns.out)` with `--out` declared | M4 | explicit_out=1 unflagged=0 `argparse --out` | explicit_out=0 unflagged=1 |
| `emit("{}", ns.input)` with `--input` declared | M3 | explicit_out=0 unflagged=1 | explicit_out=1 unflagged=0 `argparse --input` |

   M1, M2 and M3 make the tool miss real writes, which is the dangerous direction. M4 makes it
   over-flag a correct write, which is the conservative direction.
5. **Why they survive.** No counter fixture and no selftest case has:
   - an attribute of an object that is not a parse_args namespace but whose name is a declared
     output dest. The only non-namespace case, `output_attr_not_parse_args` (v4:610), declares
     no `--out`, so `out_dests` is empty and `_parse_args_ns` is never reached;
   - a namespace parameter with mixed callers;
   - a keyword-passed destination.

   All live call sites in `tools/registry-replay.py` at `a21845f5` are positional and single:
   `publish(code, report, bundle, out)` at :185, `publish(..., Path(a.out))` at :282, and
   `run_replay(a)` at :287.
6. **Consequence for the `outflag` class in `mutants.json` (seat MutantAuthor).** The predicate
   needs every declared mutant `killed`. Of these mutants, only an M3-style or M2b-style edit
   is killable by the counter's oracle (measure.py:311). An M1, M2 or M4 edit would score
   `survived`.

## Commands and outputs

Driver: for each mutant, copy the tool and check that `find` occurs exactly once. Then run both
detectors on the pristine, mutated and restored bytes:

```
python3 .ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f \
  --probe-mutant /tmp/tameshi-r42w2-MutProbeOutflag-<M>/write-path-census-v4.py
python3 -I /tmp/tameshi-r42w2-MutProbeOutflag-<M>/write-path-census-v4.py --selftest
```

Baseline (pristine copy): `PROBE outcome=survived detail=` and
`WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`, both exit 0. The baseline is clean, so the results
below are conclusive.

| mutant | edit (unified-diff line) | `--probe-mutant` (mutated) | `--selftest` (mutated) | verdict |
|---|---|---|---|---|
| M1 | v4:261 `+    return True` (first statement of `_parse_args_ns`) | `outcome=survived detail=` | exit 0, `cases=15 failed=0` | **survived both** |
| M2 | v4:274 `-    return all(` / `+    return any(` | `outcome=survived detail=` | exit 0, `cases=15 failed=0` | **survived both** |
| M3 | v4:68 `OUTPUT_FLAGS = (..., '--output-dir', '--input')` | `outcome=killed detail=F05_inflag explicit_out=1 want 0` | exit 0, `cases=15 failed=0` | killed by counter only |
| M4 | v4:251 `-        for kw in call.keywords:` / `+        for kw in ():` | `outcome=survived detail=` | exit 0, `cases=15 failed=0` | **survived both** |
| M2b (extra) | v4:306-308 `return None`→`continue`; `return ' '.join(sorted(flags)) or None` | `outcome=killed detail=F06_outflag_mixed_callers explicit_out=1 want 0` | exit 1, `FAIL output_param_one_constant_caller: explicit_out=True, want False`, `FAIL ...: unflagged=False, want True`, `cases=15 failed=2` | killed by both |

Every probe ran with exit 0 and an empty stderr tail. On restored bytes, every mutant gave
`PROBE outcome=survived` and selftest exit 0, `cases=15 failed=0`.

## Restoration evidence (sha256)

| mutant | pristine | mutated | restored |
|---|---|---|---|
| M1 | 784de4c0…d122fe5 | 6776ef4fc810f9dec3db1f630effa60092ffa8c2dbf84c6469f0f7e62452a612 | 784de4c0…d122fe5 |
| M2 | 784de4c0…d122fe5 | 3d15380f2268f3e31854eb06a6a6ad286cb1ef6c52173e6ea6815a38ebbbc1af | 784de4c0…d122fe5 |
| M3 | 784de4c0…d122fe5 | add1862945a3fba457da868da6818190db1493ad16e7ac1b86cdab605228e465 | 784de4c0…d122fe5 |
| M4 | 784de4c0…d122fe5 | 4f2a2ccb80962754836392a6a653c646b0c324a9e859ee499857696edd966b34 | 784de4c0…d122fe5 |
| M2b | 784de4c0…d122fe5 | a53070bfe31936916ee813e05dffc6a6bce5d9b8b03bad0f7699c8d288a425bb | 784de4c0…d122fe5 |

After all runs, the lane `tools/write-path-census-v4.py` was still sha256
`784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`. Tooling: none installed
(Python 3.14.8, already present).

## Detector × mutant

| | M1 | M2 | M3 | M4 | M2b |
|---|---|---|---|---|---|
| counter `--probe-mutant` | survived | survived | **killed** (F05) | survived | **killed** (F06) |
| tool `--selftest` | survived | survived | survived | survived | **killed** (2 FAIL) |

BROKEN: the outflag recognizer's namespace guard (`_parse_args_ns`: always-True and the any-for-all edit) and its keyword call-site handling are not covered by either detector (M1, M2 and M4 survive both); the selftest also misses `--input` (M3).
