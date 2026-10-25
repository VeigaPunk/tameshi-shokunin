# CriticFixtureOverfit — C2 overfit attack (wave 1)

Seat: L1Tameshi42.CriticFixtureOverfit · 2026-10-25 · lane rev tested: `c77c2b7` (base), freeze `322b5cd`.
No lane checkout edits; all falsifier artifacts live under `/tmp/tameshi-r42-CriticFixtureOverfit-r1/` (git clone removed; files retained with shas below).

## Finding 1 — C2's frozen battery is satisfiable by literal name/line-number special-casing (no resolution)

Counterexample: `v3flip.py` (sha256 `63f688fe7b488fcb380f5eb85d7073ce2cea1188c87e9e43acefe30a625338ec`, 2965 B) = the real v3 tool plus ~12 lines that special-case exactly the identifier set named in the task (`root`, `case_dir`, `publish`, `out`, `--out`) and the live line numbers `1682/1685/123`. It performs no attribute-bound or outflag resolution.

Control run (allowed, never a measurement), measure.py `--tool-file` at base rev:

```
python3 .ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c77c2b7e64d2e356381441ecf94abac03e984606 \
  --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f \
  --tool-file /tmp/tameshi-r42-CriticFixtureOverfit-r1/v3flip.py
```

Output (no FAIL lines):

```
C2_R42_CONTROL: self_pin=1 tool_absent=0 tool_sha256=63f688… v3_sha_ok=1 v2_sha_ok=1
selftest_exit=0 fixtures_pass=10/10 run_errors=0 live_1682_ok=1 live_1685_ok=1 live_123_ok=1
live_unflagged_v3=3 live_unflagged_v4=0 live_tool_errors_v4=0 mutants_declared=0 mutants_killed=0
rev=c77c2b7… freeze=322b5cd… C2_R42_CONTROL_PASS=false
```

Every observable check that the predicate keys on is green (control mode forces `C2_R42_CONTROL_PASS=false` unconditionally — `passed = not control and …`, measure.py:462). The cheat has:
- line-number lock: measure.py:49-54 (`lineno in (1682,1685)` → scratch+`mkdtemp`; `lineno == 123` → explicit_out+`--out`);
- name lock: measure.py:56-61 (`self.case_dir(`+`self.root`+`tempfile.mkdtemp()` / `--out`+single `publish(` call);
- trivial `--selftest` exit 0 (measure.py:67-68).

The mutant gate does not rescue the counter: `--probe-mutant` on an attr-class mutant of the cheat (swap literal `self.case_dir(` → `self.base_dirs(`):

```
PROBE outcome=killed detail=F01_attr_scratch scratch=0 want 1
```

The kill oracle only observes "a battery case differed" (measure.py:311-317); it cannot tell a renamed literal from a disabled resolution step. So an adversarial v4 with literal tables satisfies the ≥3-mutant kill requirement too.

Stronger bound: `contentcheat.py` (sha256 `39e24f453c6e3368e240cea36eee8360c911c3a5ad722a20740aba4b45dbf142`, 3779 B) memoizes the 10 frozen fixture sources by exact bytes and the live sites by `(basename, lineno)`; same control run is also fully green (`fixtures_pass=10/10`, live 3/3). The entire frozen battery is satisfiable by table lookup alone.

## Finding 2 — which counter fixtures already vary names (audit)

From `measure.py:72-202` (FIXTURES) and `:204-211` (LIVE):

| Class | Fixtures | Identifiers used | Variation present |
|---|---|---|---|
| attr | F01/F02/F03 | `H`, attr `root`, method `case_dir(name)`, locals `directory`/`expected_path`/`handle` | only *assignment source* differs (mkdtemp vs `'golden'` vs `rebase` ambiguity); identifier set identical across all three |
| outflag | F04/F05/F06 | fn `publish(data, out)`, param `out`, flag `--out`/`--input`, `args.out` | only flag string varies (`--input`) and call-site count (F06 adds `Path('golden')`); fn/param names identical |
| other | F07–F10 | `EXPECTED`, `root`/`dest`, symlink, `--update-goldens` | not part of the claimed new classes |
| live | context-capture.py:1682/1685, registry-replay.py:123 | reuse the very same names (`self.case_dir`/`self.root`; `publish`/`out`/`--out`) **and** their exact line numbers are pinned in LIVE + check_site (measure.py:271-274 requires exactly one site at 1682/1685/123) | no renamed identifiers, no displaced line numbers anywhere |

Conclusion: no fixture renames the attr/method pair or the output param/flag beyond `--out`/`--input`; none perturbs line numbers. A v4 keyed on the literal set {`root`,`case_dir`,`publish`,`out`,`--out`} ∪ {1682,1685,123} passes the frozen battery — Finding 1 proves it.

## Finding 3 — cheapest additional falsifier for wave 2 (proposal only, not applied)

Renamed-identifier fixture harness, run directly against the landed v4 (no counter edits, no lane edits, independent of the deciding measurement):

```
python3 /tmp/tameshi-r42-CriticFixtureOverfit-r1/renamed_falsify.py <path-to-v4>
```

`renamed_cases.py` (sha `f91a43c76d7d288c1103ddcc43b6eaad962b12e663f0d935bcef3a5a9a099ef5`) defines 6 same-class cases whose identifiers are fully renamed: R01–R03 attr (`base`/`make_dir(tag)`/`folder`; scratch, golden, rebase-ambiguous), R04–R06 outflag (`emit(payload, dest)`, `--output-dir`, `--input-dir`, mixed caller). Expected classifications mirror F01–F06.

Probe results (harness = `renamed_falsify.py`, sha `cab9ccf014768d62f7b5b85de2f58ccf77d16b5f3e3684ae374ebea3dbbd902f`):

```
v3 (baseline):      R01 FAIL scratch=False want True · R04 FAIL explicit_out=False want True · R02,R03,R05,R06 ok (4/6)
v3flip (cheat):     identical profile — R01/R04 FAIL, rest ok (4/6)   ← name-lock exposed
contentcheat:        0/6 (no memo hit)                                ← content-lock exposed
```

An honest v4 that really resolves attribute-bound/outflag destinations passes all 6. The harness therefore separates a real resolver from a name/lineno-special-cased one at near-zero cost (one seat, ~30 s, no counter modification). Keep it as the wave-2 falsifier seat tool, and treat R01/R04 as the must-kill pair.

## What I could not check

- The real v4 implementation: absent at freeze (no `tools/write-path-census-v4.py` in `git ls-tree`; v3/v2 only). This attack targets the *counter*, which is the correct overfit surface before v4 lands.
- Mutants.json contents (do not exist pre-landing; the L1 writes them after v4 lands per the frozen protocol).
- Whether wave 2 will have ≥32 attack items; if so, the falsifier above is the recommended addition.

## Artifacts (retained under /tmp/tameshi-r42-CriticFixtureOverfit-r1/; clone deleted)

| file | sha256 | bytes |
|---|---|---|
| v3flip.py | `63f688fe7b488fcb380f5eb85d7073ce2cea1188c87e9e43acefe30a625338ec` | 2965 |
| contentcheat.py | `39e24f453c6e3368e240cea36eee8360c911c3a5ad722a20740aba4b45dbf142` | 3779 |
| renamed_cases.py | `f91a43c76d7d288c1103ddcc43b6eaad962b12e663f0d935bcef3a5a9a099ef5` | 3616 |
| renamed_falsify.py | `cab9ccf014768d62f7b5b85de2f58ccf77d16b5f3e3684ae374ebea3dbbd902f` | 3332 |
| mutant_attr.py | `459bb3bd1b2f6708baeb4e2357231d0c64af844f7a937e6f8df743b2f50e5c30` | 2966 |

No tools installed (none required). No lane/fleet/jj mutations made.
