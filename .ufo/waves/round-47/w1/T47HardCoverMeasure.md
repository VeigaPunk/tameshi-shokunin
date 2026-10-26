# T47HardCoverMeasure — coverage group, selftest addition (round 47, C2)

Seat `T47HardCoverMeasure` (group `coverage`). Deliverable written:
`.ufo/waves/round-47/w1/T47HardCoverMeasure.addition.py` (one top-level
`extra_T47HardCoverMeasure()`, helpers `_xT47HardCoverMeasure_*`). Nothing else in the lane was
touched; scratch under `/tmp/tameshi-r47-T47HardCoverMeasure/`.

Counter being hardened: `.ufo/evidence/round-46/hardening/coverage-counter.py`
(sha256 `200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9`, the
`base_sha256.coverage` pin of `hardening/pool.json`). Pool: `.ufo/evidence/round-47/hardening/pool.json`.

## Result

**5 of 6 assigned mutants killed** (`measure:int:0`, `measure:int:1`, `measure:cmp:6`,
`measure:bool:5`, `measure:cmp:9`), each by exactly one named case. The sixth, `measure:const:0`,
is **structurally unreachable** through `--selftest` under the frozen assembly: the mutation makes
`measure()` raise before its first `print`, and the round-46 `selftest()` aborts on its first case
because its `build()` helper indexes an empty stdout. Proof and the refused workaround are below —
no fake kill was added.

## Verification (commands and exit codes)

| # | command | exit | result |
|---|---|---|---|
| 1 | `python3 .ufo/evidence/round-47/hardening/assemble.py --group coverage --add /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-47/w1/T47HardCoverMeasure.addition.py --out /tmp/tameshi-r47-T47HardCoverMeasure/h.py` | 0 | `wrote ... (1 additions)` |
| 2 | `python3 /tmp/tameshi-r47-T47HardCoverMeasure/h.py --selftest` | 0 | 26 cases, 0 failed, `VERDICT: PASS`; all six `T47M_*` cases `PASS` |
| 3 | `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardCoverMeasure/h.py --group coverage --ids measure:int:0,measure:int:1,measure:const:0,measure:cmp:6,measure:bool:5,measure:cmp:9` | 0 | `PRISTINE pass`; 5 × `killed`; `measure:const:0 crashed` |
| 4 | `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardCoverMeasure/h.py --group coverage` (all 86) | 0 | `PRISTINE pass`; killed 69 (baseline 64); `REGRESSED: []`; all 4 NEUTRAL `survived` |

Sweep counts (group `coverage`, 86 mutants from `pool.json`): baseline
`.ufo/evidence/round-47/before/base-coverage.txt` killed 64; with this addition killed 69.
New kills are exactly the five above. Every baseline kill stays killed; no mutant moved
killed → survived/crashed/timeout. Neutrals `Tree.read:commute:0`, `Tree.ls:commute:0`,
`measure:commute:0`, `measure:commute:1` all `survived`.

## Per-mutant evidence

Fixture (built once per run, `tempfile.mkdtemp`, removed in `finally`): two googletest rows
`S256`/`S257` with matching snapshots under `SNAP_PREFIX` and sha256 prefixes, and — for the
"passing" lane — entries `corpus/knowledge/{a,b}.md` (provenance trio, `verified-at: 2026-10-25`,
quote found in the folded snapshot, both listed in the used-by cells) indexed by
`` `knowledge/a.md` ``/`` `knowledge/b.md` ``, plus `corpus/knowledge/c.md` = `plain note, cites
nothing` (not an entry; refused silently). The "failing" lane has one entry only (`a.md`) with two
rows and a matching index. `measure()` is called in process with `contextlib.redirect_stdout`, so
an exception is reported as a named `FAIL ... raised <Exc>` instead of a traceback.

| pool id | case | separating input | original vs mutant | helper output |
|---|---|---|---|---|
| `measure:int:0` | `T47M_measure_exit_zero_on_pass` | passing lane | `return 0 if passed else 1` vs `1 if passed else 1`: exit 0 vs 1 | `FAIL T47M_measure_exit_zero_on_pass want=(0, 'C2_R45_PASS=true') exit=1 got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true` |
| `measure:int:1` | `T47M_measure_exit_one_on_fail` | failing lane (one entry) | `... else 1` vs `... else 2`: exit 1 vs 2 | `FAIL T47M_measure_exit_one_on_fail want=(1, 'C2_R45_PASS=false') exit=2 got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false` |
| `measure:cmp:6` | `T47M_measure_refused_only_for_other_reasons` | passing lane incl. `c.md` citing no row | `why != 'cites no googletest row'` vs `==`: pristine prints no `REFUSED`; mutant prints `REFUSED corpus/knowledge/c.md cites no googletest row` | `FAIL T47M_measure_refused_only_for_other_reasons want=(None, 'C2_R45_PASS=true', '!REFUSED ') exit=0 got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true` |
| `measure:bool:5` | `T47M_measure_row_ids_join` | passing lane | `','.join(sorted(rows)) or '-'` vs `and`: `row_ids=S256,S257` vs `row_ids=-` | `FAIL T47M_measure_row_ids_join want=(None, 'row_ids=S256,S257') exit=0 got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=- rev=m C2_R45_PASS=true` |
| `measure:cmp:9` | `T47M_measure_entry_index_suffix` | passing lane, both entries indexed | `'' if p in indexed else ' (not indexed)'` vs `p not in indexed`: `ENTRY corpus/knowledge/a.md` vs `ENTRY corpus/knowledge/a.md (not indexed)` | `FAIL T47M_measure_entry_index_suffix want=(None, 'ENTRY corpus/knowledge/a.md', '!(not indexed)') exit=0 got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true` |
| `measure:const:0` | `T47M_measure_selfpin_binary` | passing lane | `tree.read(SELF_PATH, binary=True)` vs `False`: pristine `self_pin=1`, rc 0; mutant feeds a `str` to `hashlib.sha256` → `TypeError` | in `--selftest`: `rc=1, 0 FAIL lines, 0 stdout lines` (`crashed`). In isolation (module loaded, case called directly): `PASS T47M_measure_selfpin_binary want=(None, 'self_pin=1') exit=0 got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true` for pristine and `FAIL T47M_measure_selfpin_binary raised TypeError` for the mutant |

Raw `measure()` stdout on the passing lane (captured, per mutant), which is what the output cases
assert: pristine → three lines, no `REFUSED`, `ENTRY corpus/knowledge/a.md` /
`ENTRY corpus/knowledge/b.md`, `row_ids=S256,S257`; `measure:cmp:6` → additionally
`REFUSED corpus/knowledge/c.md cites no googletest row`; `measure:cmp:9` → both `ENTRY` lines end
` (not indexed)`; `measure:bool:5` → `row_ids=-`. Each mutant produces exactly one `FAIL` line in
`--selftest` (measured), so the attribution above is one-to-one; `measure:int:0` no longer
contaminates the output cases because those pass `want_rc=None`.

## Why `measure:const:0` cannot be killed by any in-selftest case

1. The mutation is `measure`'s `binary=True` → `False`. `Tree.read(path, binary=False)` returns
   `out.stdout.decode('utf-8', 'replace')` or `None`; it can never return bytes. So for every lane
   where `SELF_PATH` exists at the rev, `measure` executes `hashlib.sha256(<str>)` and raises
   `TypeError` at the `self_pin` line — which is **before any `print` in `measure`**. Where
   `SELF_PATH` is absent, `blob is not None` is `False`, the hash is never evaluated, and the mutant
   is byte-identical to pristine (`self_pin=0`); no separation exists there.
2. The round-46 `selftest()` body (base source, unchanged by `assemble.py`) calls
   `build(reg, ents, readme)` for its first case `T1_two_entries_pass` at line 201, and `build`
   ends at line 176 with `return out.stdout.strip().splitlines()[-1]` — an unguarded index. The
   subprocess run of the mutated counter prints nothing (step 1), so this raises `IndexError` in
   the parent before the first `PASS`/`FAIL` line is printed. Additions are called only at base
   lines 205–211, after that loop. Observed: `python3 m_measure_const_0.py --selftest` → rc 1,
   `stdout_lines=0`, stderr = `IndexError: list index out of range` at
   `line = build(reg, ents, readme)`.
3. Therefore no case in `extra_T47HardCoverMeasure()` (nor in `extra_HardCover1/2`) is reached
   under this mutant; the run is a crash, and `pool.py` classifies crashes as not killed. This
   matches the declared baseline (`crashed`).
4. Refused workaround: I could print from module level (`if '--selftest' in sys.argv: ...`) so a
   case runs at import before `selftest()`. I did **not** do it: the brief requires the case set to
   be run by the single `extra_*()` (so it feeds `(cases, failed)`), an import-time `FAIL` line is
   printed outside the tally (`cases=26 failed=0` alongside a `FAIL`), and it would convert
   *arbitrary* crashes of any mutant into `killed` — precisely the fake-kill pattern the brief
   refuses. Fixing it honestly needs one line in the frozen harness (`… or ['']` at base line 176,
   as `_xHardCover1_last_line` already does at its own call site), which is outside a seat's writable
   scope.

## Design notes

- Cases assert rule outputs, never source text, AST, hashes or lengths; all six pass on the
  pristine counter (verified above), so the neutral mutants keep surviving.
- `_xT47HardCoverMeasure_lane()` creates its own repo (`git init -q -b m`), checks
  `git rev-parse --show-toplevel == os.path.realpath(d)` before the first commit, commits only with
  `-c user.name=t -c user.email=t@t`, and the directory is removed in `finally`.
- Read-only reuse of the round-46 additions: `_xHardCover2_row`, `_xHardCover2_ENTRY` (the registry
  line shape and provenance trio already validated by C06–C10). No base function changed; the
  addition adds `contextlib`, `io`, `shutil` imports at module level (stdlib, no side effects).
- Cost: six in-process `measure()` calls per `--selftest` (~0.3 s), no network, no live process.

## Risks

- `measure:const:0` remains `crashed`; that is one kill short of the six in the milestone and is
  not recoverable from a seat's file set (argument above).
- If a future addition moved case execution before the base loop, `T47M_measure_selfpin_binary`
  would immediately start killing `measure:const:0`; the case is already behavioural and passing.
- The output-only cases would also fail under any mutant that breaks `measure`'s printing on the
  passing lane; that would still be a kill (never a crash), since the in-process call is wrapped.

## Tooling

No installs or upgrades in this seat (pacman paused host-wide; nothing was needed).
`python3 3.14.8`, `git` from the host, pool/assemble helpers as committed at freeze
`9acfbe21435e1976636a276448dee1d5e7155915`.
