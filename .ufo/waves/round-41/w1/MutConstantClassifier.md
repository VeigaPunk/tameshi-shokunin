# MutConstantClassifier — C2 counter vs `classify_source` returning a constant

Seat: `L1Tameshi41.MutConstantClassifier` (read-only in the lane). Lane checkout, jj state and Git
index untouched; the only lane write is this report. Scratch copies under `/tmp/tameshi-r41-mutconst-*`.

## Verdict

**Neither mutant passes. `C2_R41_PASS=false` for both.** The C2 predicate is *not* broken by a
constant `classify_source`; it is killed independently by `fixtures_ok` (`measure.py:235`),
`selftest_exit` and `live_ok` (`measure.py:237-244`). Receipts below.

## Mutants built

Base blob: `tools/write-path-census-v3.py` at freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`,
sha256 `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` (identical to the
contract `claims.C2.tool_sha256`). Only `classify_source` was touched (signature at
`tools/write-path-census-v3.py:216`); `summarize`, the selftest and everything else are byte-identical.

| Mutant | Inserted as the first statement of `classify_source` | Tool sha256 | Repo HEAD |
|---|---|---|---|
| `zero` | `return []  # mutant: constant zero records` | `b68698efed6d2135e6f034e7e6fd51dc8b30699434cf696f73ef42afec0836d1` | `4a4e3cd3b2bb6dcf00f7d5c98f65dae029f6092f` |
| `one` | `return [{ 'lineno': 810, 'kind': 'open', 'resolved': 'expected.json', 'expected': True, 'scratch': False, 'flagged': False, 'unflagged': True, }]` (single record, every input) | `345882de7af1d52389d23ffc2804d0991f09033c46d0e740bc716223fdf9645f` | `7981399a0bae42861641395bb96add44be26b4e2` |

`one` is the adversarial shape for this family: `unflagged` is derived, not free
(`tools/write-path-census-v3.py:177` → `'unflagged': expected and not scratch and not flagged`), so
"unflagged variable record" means `expected=True, scratch=False, flagged=False` and a variable `kind`.
`lineno: 810` / `kind: 'open'` is also chosen to land inside the live `open` window the counter scans
(`measure.py:203`), i.e. the mutant is overfitted toward passing, not away from it.

Each repo carries exactly the blobs the counter reads at `--rev`:

```
/tmp/tameshi-r41-mutconst-zero|one/
  tools/write-path-census-v3.py          (mutant)
  tools/write-path-census-v2.py          (freeze blob, sha 4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b)
  tools/repeat-control.py                (freeze blob, sha 296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25)
  .ufo/evidence/round-41/census/fixtures.json   (freeze blob, sha a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31)
  .ufo/evidence/round-41/contract.json          (freeze contract, only claims.C2.tool_sha256 replaced by the mutant sha)
```

The contract pin was replaced by design, so `tool_sha_ok=1` in both runs is the *ceiling* of what a
substituted tool can buy: the pin is self-referential and detects nothing here
(`measure.py:158-165` compares the blob to the same repo's patched pin). The kill therefore rests on
the behavioural terms.

## Exact commands

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/census/measure.py \
  --lane /tmp/tameshi-r41-mutconst-zero --rev 4a4e3cd3b2bb6dcf00f7d5c98f65dae029f6092f

python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/census/measure.py \
  --lane /tmp/tameshi-r41-mutconst-one --rev 7981399a0bae42861641395bb96add44be26b4e2
```

Counter used is the frozen lane file, sha256
`5d57c7097fb33a66d11cb19b834dd7f92ade268c56562c8a34d7a94bf64ef696` = contract
`claims.C2.counter_sha256`. No default-mode run against the lane, no `--rev work`, no run at the tip
`d4ee4e63…`.

## Receipts — stdout verbatim, then exit codes

`zero`:

```
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=1 var_unflagged=0 var_expected=0 symlink_unflagged=0 symlink_expected=0 literal_unflagged=0 scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=0 live_var_resolved_v3=0 live_var_scratch_v3=0 live_var_sites_v2=0 live_var_expected_v2=0 live_symlink_lineno=0 live_symlink_resolved_v3=0 live_symlink_scratch_v3=0 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 rev=4a4e3cd3b2bb6dcf00f7d5c98f65dae029f6092f C2_R41_PASS=false
```

exit `1`.

`one`:

```
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=1 var_unflagged=1 var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=1 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=810 live_var_resolved_v3=1 live_var_scratch_v3=0 live_var_sites_v2=0 live_var_expected_v2=0 live_symlink_lineno=0 live_symlink_resolved_v3=0 live_symlink_scratch_v3=0 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 rev=7981399a0bae42861641395bb96add44be26b4e2 C2_R41_PASS=false
```

exit `1`.

Self-test of each mutant against the frozen fixtures (same file the counter passes it):

```
# zero
WRITE_CENSUS_V3_SELFTEST: var_unflagged=0 symlink_unflagged=0 literal_unflagged=0 scratch_var=0
FAIL planted var_unflagged: want unflagged=1 got 0
FAIL planted var_unflagged: want expected_sites=1 got 0
FAIL planted symlink_unflagged: want unflagged=1 got 0
FAIL planted symlink_unflagged: want expected_sites=1 got 0
FAIL planted literal_unflagged: want unflagged=1 got 0
FAIL planted literal_unflagged: want expected_sites=1 got 0
FAIL planted scratch_var: want expected_sites=1 got 0
exit=1

# one
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=1
FAIL planted scratch_var: want unflagged=0 got 1
exit=1
```

## Per-term failure (from `measure.py:235-256`)

| Term | `zero` | `one` | Required | Blocker? |
|---|---|---|---|---|
| `fixtures_ok` (TARGET `measure.py:48-55`) | false (`var_unflagged`/`var_expected`/`symlink_*`/`literal_*` all 0) | false (`scratch_var_unflagged=1` vs `0`) | true | **yes, both** |
| `selftest.returncode == 0` | 1 | 1 | 0 | **yes, both** |
| `live_ok` (`measure.py:237-244`) | false (`live_var_resolved_v3=0`) | false (`live_var_scratch_v3=0`, `live_symlink_resolved_v3=0`) | true | **yes, both** |
| `sha_ok == 1` | 1 (patched pin) | 1 (patched pin) | 1 | no |
| `v2_sha_ok == 1` | 1 | 1 | 1 | no |
| `v2_misses` | true | true | true | no |
| `killed.resolve/symlink == 1` | 1 / 1 | 1 / 1 | 1 / 1 | no |

## Why no constant `classify_source` can pass — not just these two samples

`fixture_fields` (`measure.py:71-85`) calls the mutant on four fixtures and `fixtures_ok`
(`measure.py:235`) requires `var_unflagged=1` **and** `scratch_var_unflagged=0`
(`measure.py:49,54`). A constant classifier returns the same record list for both inputs, so both
summaries are identical and both counters are equal: `var_unflagged = scratch_var_unflagged`. The
requirement set is unsatisfiable for *any* constant list of any length — the only escape is for the
classifier to return a different record set for the `/tmp`-rooted `scratch_var` fixture
(`fixtures.json:5`), which is exactly the behaviour a constant cannot have. `live_ok` repeats the
contradiction: it requires `live_var_scratch_v3=1` (`measure.py:239`) while the fixture block requires
`var_unflagged=1`, i.e. `scratch=0` (`tools/write-path-census-v3.py:177`).

The `one` receipt shows the contradiction in the raw numbers rather than in prose:
`var_unflagged=1 … scratch_var_unflagged=1` on the *same* constant record.

## Coverage findings (not a predicate break; no contract change implied)

1. `mutant_resolve_killed` / `mutant_symlink_killed` are non-discriminating when the tool's selftest is
   already red: both mutants report `=1` purely because a red selftest fails after mutation too. The
   conjunction is still sound because `selftest.returncode == 0` is a separate mandatory term
   (`measure.py:252`), but a reader must not cite `killed=1` here as evidence of recognizer coverage.
2. `tool_sha_ok` validates the blob against the *same revision's* contract (`measure.py:158-165`), so it
   cannot detect a self-pinned mutant; it only proves pin well-formedness. My runs are the proof: the
   strongest passing term for both mutants is `tool_sha_ok=1`. The fixture/selftest/live terms, not the
   pin, are what make substitution uneconomical.
3. The `open`-window live probe (`measure.py:203`, lines 805-815) is satisfied by the constant `one`
   mutant (`live_var_resolved_v3=1`); only `live_var_scratch_v3` and the `os.symlink` window separate it
   from the real tool. That pair is load-bearing for the live half.

## Restoration / before-after integrity

The scratch copies are the mutants themselves; the lane base they were derived from was never written.

| Artifact | Before (start of seat) | After (end of seat) |
|---|---|---|
| `tameshi-shokunin/tools/write-path-census-v3.py` | `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` (working tree) / same via `git show d4ee4e63:…` | `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` — unchanged |
| `tameshi-shokunin/.ufo/evidence/round-41/census/measure.py` | `5d57c7097fb33a66d11cb19b834dd7f92ade268c56562c8a34d7a94bf64ef696` | same — unchanged |
| `tameshi-shokunin/.ufo/evidence/round-41/contract.json` | `058f43932f5376d6ef47b025e2e5b6898942e8a7f7628cc8a3ba4acf718442f2` | same — unchanged, never edited |
| `/tmp/…-zero/tools/write-path-census-v3.py` | `b68698efed6d2135e6f034e7e6fd51dc8b30699434cf696f73ef42afec0836d1` | same (committed; `git show HEAD:…` re-hashed identical) |
| `/tmp/…-one/tools/write-path-census-v3.py` | `345882de7af1d52389d23ffc2804d0991f09033c46d0e740bc716223fdf9645f` | same (committed; re-hashed identical) |

`git -C tameshi-shokunin status --porcelain` at seat start and end differs only by sibling wave output
(`?? .ufo/evidence/round-41/sources/`, `?? .ufo/waves/round-41/`,
`?? corpus/knowledge/r41-variable-destination-writes.md`, and a concurrent `M corpus/SOURCES.md` from a
scribe seat). No path I touched appears in either listing. Scratch `__pycache__/` created by module
loading in the `/tmp` repos is untracked and does not affect `git show rev:path`, which is what the
counter reads.

## Tooling

No install or update performed; `python3 3.14.8` and `git 2.56.0` already present. pacman untouched per
the host-wide pause.

Report: .ufo/waves/round-41/w1/MutConstantClassifier.md
