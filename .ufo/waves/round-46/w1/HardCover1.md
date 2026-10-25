seat: HardCover1
item: authored 5 selftest cases for the round-45 coverage counter, killing declared survivors C01–C05 of mutants.json group `coverage` without killing the neutral mutants.

# HardCover1 — C2 selftest additions C01,C02,C03,C04,C05 (coverage counter)

## Deliverable

`.ufo/waves/round-46/w1/HardCover1.addition.py` (5322 bytes) — one top-level `extra_HardCover1()`
plus helpers `_xHardCover1_SNAP` / `_xHardCover1_sha()` / `_xHardCover1_row()` /
`_xHardCover1_last_line()`. It returns `(cases, failed)`, prints one `PASS|FAIL <case> want=… got=…`
line per case. Nothing else in the lane was written; no tool was installed (no pacman, no uv, no
network); scratch lives in `/tmp/tameshi-r46-HardCover1/`.

Baseline copy: `cp .ufo/evidence/round-45/coverage/measure.py /tmp/tameshi-r46-HardCover1/orig.py`
→ `sha256sum` of both = `2f321b2c499ff4329483ef640ac96e629ad67a8e0e16f8e0a6920d7031fbf894` (identical).

Every case builds a scratch repo the way the counter's own selftest does (`git init -q -b m` in a
`tempfile.TemporaryDirectory`, `rev-parse --show-toplevel` asserted equal to `os.path.realpath(d)`,
commit with `-c user.name=t -c user.email=t@t`, `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_NOSYSTEM=1`), commits the running file bytes at `SELF_PATH` (so `self_pin=1`), then runs
`[sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm']` and asserts on the last
stdout line (the `C2_R45: self_pin=… rows=… entries=… indexed=…` tally). No case asserts on source
bytes; the only byte read of the running file is the `SELF_PATH` commit the counter itself requires.

## Per-mutant result

| id | case name | separating input (pristine rule vs mutant) | pristine tally | mutant tally |
|---|---|---|---|---|
| C01 | `C01_github_not_googletest` | 2 rows whose source URL is `https://github.com/example/notgoogletest/docs/{advanced,primer}.md` (github, not google/googletest), snapshots present under `SNAP_PREFIX` with matching sha, 2 valid entries indexed. `GT_RE` must reject them. | `rows=0 entries=0` | `rows=2 entries=2 indexed=2 … PASS=true` |
| C02 | `C02_round44_snapshot_path` | 2 googletest rows anchored to `.ufo/evidence/round-44/coverage/sources/{advanced,primer}.md`, files committed there with matching sha. `SNAP_RE` is pinned to `SNAP_PREFIX` (round-45) and must not accept a round-44 path; the mutant's `round-4[45]` does. | `rows=0 entries=0` | `rows=2 entries=2 indexed=2 … PASS=true` |
| C03 | `C03_missing_snapshot_empty_sha` | 2 googletest rows anchored to `SNAP_PREFIX + missing{,_2}.md e3b0c442` — the snapshot is absent at REV and the anchor carries sha256(`b''`)'s 8-hex prefix. Pristine `if data is None: continue` skips the row; the mutant substitutes `b''` and the empty-digest anchor then validates. | `rows=0 entries=0` | `rows=2 entries=0 indexed=0 … PASS=false` |
| C04 | `C04_entry_without_source_line1` | entry `b.md` line 1 is ` S256 S257 — upstream` (citation kept, `source:` removed); entry `a.md` is a valid control. Pristine requires `lines[0].startswith('source:')`. | `rows=2 entries=1 indexed=1` | `rows=2 entries=2 indexed=2 … PASS=true` |
| C05 | `C05_entry_without_recheck_line3` | entry `b.md` line 3 is `review: 365d` instead of `recheck: 365d`; `a.md` valid. Pristine requires `lines[2].startswith('recheck:')`. | `rows=2 entries=1 indexed=1` | `rows=2 entries=2 indexed=2 … PASS=true` |

For C01/C02 the mutant does not merely change a count — it turns the fixture into a passing run
(`C2_R45_PASS=true`), which is exactly the false-positive the round-45 counter admitted. C03 changes
`rows=0` to `rows=2` while entries stay 0 (the empty snapshot text cannot carry a located quote), so
the separating field is `rows`. C04/C05 change `entries=1 indexed=1` to `entries=2 indexed=2`.

Isolation: under each single-mutant build exactly one of the five cases fails and the other four pass
(see the per-mutant runs below). Each case's fixture is the minimum for its rule: 2 rows + 2 entries
only because the frozen predicate needs `rows>=2`/`entries>=2`, so a mutant that disables the rule is
observably flipped into `PASS=true`.

## Verification commands and output

1. Assemble:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/hardening/assemble.py --group coverage \
  --add /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-46/w1/HardCover1.addition.py \
  --out /tmp/tameshi-r46-HardCover1/hard.py
wrote /tmp/tameshi-r46-HardCover1/hard.py (1 additions)
```

2. `python3 /tmp/tameshi-r46-HardCover1/hard.py --selftest` (exit 0):

```
PASS T1_two_entries_pass want='C2_R45_PASS=true' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
PASS T2_rows_only_fail want='entries=0' got=C2_R45: self_pin=1 rows=2 entries=0 indexed=0 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T3_old_verified_at want='entries=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T4_quote_not_in_snapshot want='entries=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T5_not_used_by want='entries=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T6_bad_sha_prefix want='rows=1' got=C2_R45: self_pin=1 rows=1 entries=2 indexed=2 row_ids=S257 rev=m C2_R45_PASS=false
PASS T7_not_indexed want='indexed=1' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T8_queued_rows want='rows=0' got=C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=m C2_R45_PASS=false
PASS T9_non_googletest_url want='rows=0' got=C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=m C2_R45_PASS=false
PASS T10_indented_row_counts want='rows=2' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
PASS C01_github_not_googletest want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=m C2_R45_PASS=false
PASS C02_round44_snapshot_path want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=m C2_R45_PASS=false
PASS C03_missing_snapshot_empty_sha want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=m C2_R45_PASS=false
PASS C04_entry_without_source_line1 want='entries=1 indexed=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS C05_entry_without_recheck_line3 want='entries=1 indexed=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
C2_R45_SELFTEST: cases=15 failed=0
VERDICT: PASS
```

3. `python3 .ufo/evidence/round-46/hardening/try-mutants.py --group coverage --file /tmp/tameshi-r46-HardCover1/hard.py`
(9.5 s wall):

```
PRISTINE pass VERDICT: PASS
MUTANT C01 mutant killed
MUTANT C02 mutant killed
MUTANT C03 mutant killed
MUTANT C04 mutant killed
MUTANT C05 mutant killed
MUTANT C06 mutant survived
MUTANT C07 mutant survived
MUTANT C08 mutant survived
MUTANT C09 mutant survived
MUTANT C10 mutant survived
MUTANT CN1 neutral survived
MUTANT CN2 neutral survived
MUTANT CN3 neutral survived
```

4. Baseline, same helper against the unmodified round-45 counter
(`--file /tmp/tameshi-r46-HardCover1/orig.py`) — the declared survivors really do survive today:

```
PRISTINE pass VERDICT: PASS
MUTANT C01 mutant survived
MUTANT C02 mutant survived
MUTANT C03 mutant survived
MUTANT C04 mutant survived
MUTANT C05 mutant survived
MUTANT C06 mutant survived
MUTANT C07 mutant survived
MUTANT C08 mutant survived
MUTANT C09 mutant survived
MUTANT C10 mutant survived
MUTANT CN1 neutral survived
MUTANT CN2 neutral survived
MUTANT CN3 neutral survived
```

5. Per-mutant isolation (mutant applied to `hard.py` via `mutate.apply`, each build run with
`--selftest`; only the failing case differs, every other C-case still passes). Mutant builds written to
`/tmp/tameshi-r46-HardCover1/m_C0{1..5}.py`:

```
== C01 exit 1
   FAIL C01_github_not_googletest want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
== C02 exit 1
   FAIL C02_round44_snapshot_path want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
== C03 exit 1
   FAIL C03_missing_snapshot_empty_sha want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=2 entries=0 indexed=0 row_ids=S256,S257 rev=m C2_R45_PASS=false
== C04 exit 1
   FAIL C04_entry_without_source_line1 want='entries=1 indexed=1' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
== C05 exit 1
   FAIL C05_entry_without_recheck_line3 want='entries=1 indexed=1' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
```

(Each run also printed the four sibling C-cases as `PASS`, e.g. under C01:
`PASS C02_round44_snapshot_path … rows=0 entries=0`, `PASS C03_missing_snapshot_empty_sha … rows=0 entries=0`,
`PASS C04_entry_without_source_line1 … entries=1 indexed=1`, `PASS C05_entry_without_recheck_line3 … entries=1 indexed=1`.)

## Notes, risks, blockers

- All five assigned survivors are killed behaviourally; no mutant was killed by a source-byte pin.
  Evidence: the three neutral mutants (CN1 appended comment, CN2 `13`→`0xD`, CN3 trailing comment),
  which only alter bytes/representation, survive the hardened file.
- `C06`–`C10` (README full-path index form, `rows>=2`, `entries>=2`, `indexed==entries`, `self_pin` in
  the predicate) remain survivors under my addition alone. They are outside this seat's item; C2's
  `killed>=23` needs the sibling additions plus these five.
- Case C03's separating field is `rows`, not `entries`: the substituted empty snapshot cannot carry a
  located quote, so `entries` stays 0 under the mutant. The assertion `rows=0 entries=0` therefore
  pins both, and the mutant is separated by `rows` flipping to 2.
- Case C02 needs a committed round-44 snapshot file with a matching sha so that the mutant's broader
  anchor regex can validate the row; without the file the mutant would also skip it and the case
  would not separate.
- Nothing in the lane checkout was modified except the deliverable file; no git/jj command was run
  beyond read-only `git -C <lane> rev-parse HEAD` (`10a05fdf56d210988a30cf1a0a9dcd349441ba1a`) and the
  scratch-repo commits inside `/tmp/tameshi-r46-HardCover1`-owned temp dirs.
- Unrun checks: the lane-wide `mutate.py --lane … --rev …` deciding run and `--targets hardened`
  equivalence are the L1's, not this seat's; I ran only `--selftest` and the helper sweeps above.
