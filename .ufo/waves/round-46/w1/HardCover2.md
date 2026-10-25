seat: HardCover2
item: C2 selftest additions for the round-45 coverage counter — kill declared survivors C06,C07,C08,C09,C10 with behavioural cases, keep all neutrals alive.

# Deliverable

- `.ufo/waves/round-46/w1/HardCover2.addition.py` — exactly one top-level `extra_HardCover2()`, helpers `_xHardCover2_*`; 5 cases, each named after the mutant id it kills.
- Scratch only under `/tmp/tameshi-r46-HardCover2/` (`orig.py` copy of the round-45 counter, `hard.py` assembled hardened copy). Lane checkout otherwise untouched; no git/jj mutation in the lane; no commits anywhere.

# Verification (helpers, as assigned)

```
$ python3 .../hardening/assemble.py --group coverage \
    --add .../w1/HardCover2.addition.py --out /tmp/tameshi-r46-HardCover2/hard.py
wrote /tmp/tameshi-r46-HardCover2/hard.py (1 additions)

$ python3 /tmp/tameshi-r46-HardCover2/hard.py --selftest
PASS T1_two_entries_pass ... PASS T10_indented_row_counts          (round-45 cases, unchanged)
PASS C06_readme_fullpath_index want=('indexed=2', 'C2_R45_PASS=true') got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
PASS C07_rows_one_fails want=('rows=1', 'C2_R45_PASS=false') got=C2_R45: self_pin=1 rows=1 entries=2 indexed=2 row_ids=S256 rev=m C2_R45_PASS=false
PASS C08_entries_one_fails want=('entries=1', 'C2_R45_PASS=false') got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS C09_indexed_lt_entries_fails want=('indexed=1', 'C2_R45_PASS=false') got=C2_R45: self_pin=1 rows=2 entries=2 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS C10_self_pin_zero_fails want=('self_pin=0', 'C2_R45_PASS=false') got=C2_R45: self_pin=0 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=false
C2_R45_SELFTEST: cases=15 failed=0
VERDICT: PASS
EXIT=0

$ python3 .../hardening/try-mutants.py --group coverage --file /tmp/tameshi-r46-HardCover2/hard.py
PRISTINE pass VERDICT: PASS
MUTANT C01 mutant survived
MUTANT C02 mutant survived
MUTANT C03 mutant survived
MUTANT C04 mutant survived
MUTANT C05 mutant survived
MUTANT C06 mutant killed
MUTANT C07 mutant killed
MUTANT C08 mutant killed
MUTANT C09 mutant killed
MUTANT C10 mutant killed
MUTANT CN1 neutral survived
MUTANT CN2 neutral survived
MUTANT CN3 neutral survived
EXIT=0
```

Before state (same sweep on the unhardened round-45 counter, `/tmp/tameshi-r46-HardCover2/orig.py`):

```
PRISTINE pass VERDICT: PASS
MUTANT C06 mutant survived
MUTANT C07 mutant survived
MUTANT C08 mutant survived
MUTANT C09 mutant survived
MUTANT C10 mutant survived
MUTANT CN1 neutral survived
MUTANT CN2 neutral survived
MUTANT CN3 neutral survived
```

# Per mutant: case, separating input, attribution

Attribution sweep applied each mutant to `hard.py` and ran `--selftest`; each produced exactly one FAIL line, its own case (no collateral failure):

```
C06 -> FAIL C06_readme_fullpath_index got=C2_R45: self_pin=1 rows=2 entries=2 indexed=0 ... C2_R45_PASS=false
C07 -> FAIL C07_rows_one_fails        got=C2_R45: self_pin=1 rows=1 entries=2 indexed=2 ... C2_R45_PASS=true
C08 -> FAIL C08_entries_one_fails     got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 ... C2_R45_PASS=true
C09 -> FAIL C09_indexed_lt_entries_fails got=C2_R45: self_pin=1 rows=2 entries=2 indexed=1 ... C2_R45_PASS=true
C10 -> FAIL C10_self_pin_zero_fails   got=C2_R45: self_pin=0 rows=2 entries=2 indexed=2 ... C2_R45_PASS=true
```

- **C06** (`README index full-path form`; mutant drops the `'`%s`' % path` arm): fixture is two valid googletest rows (S256/S257, same snapshot sha8 prefix, `mined`, both entries in used-by), two valid entries, README indexes them as `` `corpus/knowledge/a.md` `corpus/knowledge/b.md` `` (full repo path). Pristine: indexed=2 → PASS=true; mutant: indexed=0 → PASS=false. The case asserts the PASS token plus `indexed=2`.
- **C07** (`len(rows) >= 2` → `>= 1`): same fixture but only row S256, both entries valid and indexed. Pristine: rows=1 → PASS=false; mutant: rows=1, entries=2, indexed=2 → PASS=true. Asserts `rows=1` **and** `C2_R45_PASS=false`.
- **C08** (`len(entries) >= 2` → `>= 1`): two rows, one entry `corpus/knowledge/a.md`, README indexes both names (so indexed==entries holds). Pristine: entries=1 → PASS=false; mutant: entries=1, rows=2, indexed=1 → PASS=true. Asserts `entries=1` **and** `C2_R45_PASS=false`.
- **C09** (`len(indexed) == len(entries)` → `len(indexed) >= 1`): two rows, two valid entries, README indexes only `` `knowledge/a.md` ``. Pristine: indexed=1 ≠ entries=2 → PASS=false; mutant: indexed=1 ≥ 1 → PASS=true. Asserts `indexed=1` **and** `C2_R45_PASS=false`. This is the PASS-token version of round-45 T7, which pinned only `indexed=1` and therefore let the mutant survive.
- **C10** (`self_pin == 1` → `self_pin >= 0`): otherwise fully passing fixture (two rows, two entries, both indexed) but the commit at `SELF_PATH` carries different bytes (`b'# not the running counter\n'`) instead of the running file. Pristine: self_pin=0 → PASS=false; mutant: self_pin=0 accepted → PASS=true. Asserts `self_pin=0` **and** `C2_R45_PASS=false`. This is a behavioural rule (committed bytes vs running bytes), not a source-byte pin: the fixture bytes are arbitrary and the case flips only on the self_pin predicate.

Fixture mechanics (identical to the round-45 selftest's): `tempfile.TemporaryDirectory` per case, `git init -q -b m`, `rev-parse --show-toplevel` asserted equal to `os.path.realpath(d)`, commits with `-c user.name=t -c user.email=t@t`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, all `GIT_*` stripped from the env, counter run as `[sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm']`, snapshots written under the module's own `SNAP_PREFIX`, running file bytes committed at the module's own `SELF_PATH`. No `len(rows) >= 2` / `len(entries) >= 2` / `len(indexed) == len(entries)` / `passed = self_pin == 1 and len(entries)` text appears in the addition, so every mutant's `old` text stays unique for `mutate.apply`.

# Unrun / out of scope

- Equivalence over the round-45 data revision (`ea25e022…`) was not run: seat bounds restrict counters to `--selftest` or `--rev 745a58…`/`683eedd…`; that comparison belongs to the L1's deciding run (`mutate.py --targets hardened`).
- No tool installs or upgrades were needed. No pacman transaction run.

# Risks

- The cases depend on the round-45 module's scratch-repo contract (`SELF_PATH`, `SNAP_PREFIX`, `gt_rows`/`entry_ok` semantics). If the assembler's `SELF_PATH` repoint changes, `put(SELF_PATH, …)` follows the module global, so it tracks automatically.
- `try-mutants.py` reports group-wide status; the per-mutant attribution above is the evidence that each kill is caused by its own case rather than by an unrelated regression (C01–C05 remain `survived`, as allowed for unassigned ids).
