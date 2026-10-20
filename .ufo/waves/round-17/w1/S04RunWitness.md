# S04RunWitness — registered entry commands of witness-metadata.py and bash-witness-study.py (round 17, wave 1)

Seat: TameshiR17.S04RunWitness (scout, leaf). Lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, tip
`98bea7da5801f4bc58e4187690ee1687c8a5061f` (branch master). Scratch: `/tmp/tameshi-r17w1-S04RunWitness-Rl6px6/`
(fleet-mirror clone: siblings symlinked, clone checked out at 98bea7d, porcelain-clean at start).
Tool installs or updates: none. Python used: system `Python 3.14.8`.
Writes: this report only. No lane file, sibling file, git write, or `jj` call. Entry-command runs were read-only
(`--check`, `count`, `--selftest`); all tamper probes ran in the /tmp clone, never in the live lane.

## Target and registry sources

Target: run the registered entry commands of `tools/witness-metadata.py` and `tools/bash-witness-study.py`
at the live lane and record exits vs the registered outcomes.

Registry provenance, read at 98bea7d (`git show 98bea7d:SKILL.md`):

- `SKILL.md:1553` — **round-13 gate/probe registry**, row `exposed witness provenance companion`:
  entry `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json`;
  map `0 metadata_consistent/clean; 1 metadata_inconsistent/failed; 2 input_unavailable or snapshot_tampered/could-not-evaluate, including usage`;
  self-test `python3 tools/witness-metadata.py --selftest`.
- `SKILL.md:1538` — round-13 recipe step 3 repeats the same entry command.
- `SKILL.md:1504` — **round-12 gate/probe registry**, row `bash declared-witness study`:
  entry `python3 tools/bash-witness-study.py count`;
  map `0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage/could-not-evaluate`;
  self-test `python3 tools/bash-witness-study.py selftest`.

**Source discrepancy (observed).** The target calls both tools' commands "round-13 registry", but the round-13
table (`SKILL.md:1548-1555`) contains no bash-witness-study row; that instrument's only registry row is the
round-12 one at `:1504`. A `grep -n "witness-metadata\|bash-witness-study"` over the whole SKILL.md at 98bea7d
returns exactly three hits (`:1504`, `:1538`, `:1553`), so neither row is superseded or archive-marked by the
round-14/15/16 tables. `[OBSERVED]` For the pending `tools/registry.json` (R16-MON1), the bash row's `source`
must cite `SKILL.md:1504` (round-12 registry), not the round-13 table; otherwise that instrument has no source.
`[INFERENCE]` (grading consequence, not measured).

## Registered commands — exits vs registered outcome

Live lane = `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at 98bea7d (tracked inputs unmodified, see F3).
Rev mirror = `/tmp/tameshi-r17w1-S04RunWitness-Rl6px6/fleet/tameshi-shokunin` at 98bea7d (clean clone).

| # | Command (cwd = lane root) | Registered outcome | Live lane | Rev mirror | Held? |
|---|---|---|---|---|---|
| 1 | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 `metadata_consistent`/clean | 0 — `WITNESS_METADATA: metadata_consistent reason=ok exit=0 … inputs=summary,declaration,declared,rerun_summary` | 0 — same line, mirror paths | **yes** |
| 2 | `python3 tools/witness-metadata.py --selftest` | self-test command; tool docstring = 0 clean | 0 — `SELFTEST: PASS 39/39` | 0 — `SELFTEST: PASS 39/39` | **yes** |
| 3 | `python3 tools/bash-witness-study.py count` | 0 complete classified sample | 0 — `counts killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10 witness_classified=10`; `declared_none B5,B10`; `unresolved none`; control `exit=0 denominator=16 exercised=14 skipped=2` | 0 — identical counts/rows | **yes** |
| 4 | `python3 tools/bash-witness-study.py selftest` | self-test command; tool docstring = 0 clean | 0 — `WITNESS_SELFTEST: 41/41 pass`, `VERDICT: PASS` | 0 — `WITNESS_SELFTEST: 41/41 pass`, `VERDICT: PASS` | **yes** |

All four rows were run twice in the live lane (initial pass, and a re-check at `2026-10-20T12:23:01-03:00`
after the concurrent dirt in F3) and once in the rev mirror; every run reproduced the same exit and terminal line.

Raw invocations, exact (all from the lane root):

```
python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json   # exit 0
python3 tools/witness-metadata.py --selftest                                                         # exit 0
python3 tools/bash-witness-study.py count                                                           # exit 0
python3 tools/bash-witness-study.py selftest                                                        # exit 0
```

## Exit-class reachability (auxiliary, not registered entries)

The verdict maps name three/four classes; these probes show the classes are reachable from real lane artifacts,
not only from synthetic selftest fixtures. Every probe ran in the rev clone; `git checkout -q --` restored the
tampered file and a re-run confirmed the clean exit afterwards.

| Probe | Expected class | Observed |
|---|---|---|
| `witness-metadata --check --companion .ufo/evidence/round-13/witness-metadata-old-null.json` (frozen producer-before companion) | 1 `metadata_inconsistent` | 1 — `metadata_inconsistent reason=normalized_kind_null` |
| `witness-metadata --check --companion .ufo/evidence/round-13/no-such.json` | 2 `input_unavailable` | 2 — `input_unavailable reason=companion_missing` |
| clone: raise `counts.total` to 11 in `.ufo/evidence/round-12/BashWitness/summary.json`, then `witness-metadata --check` | 2 `snapshot_tampered` | 2 — `snapshot_tampered reason=summary_digest_mismatch` (`6c04eb… != acc012…`) |
| `witness-metadata` with no mode | 2 (usage included in row 2 class) | 2 — argparse `one of the arguments --check --selftest --emit is required` |
| clone: same summary tamper, then `bash-witness-study.py count` | 1 failed integrity | 1 — `WITNESS_STUDY: COUNT summary/raw mismatch counts.total: stored=11 recomputed=10` |
| `bash-witness-study.py count --evidence <fresh empty dir>` | 2 could-not-evaluate | 2 — `CANNOT-EVALUATE (missing …/declaration.json — run \`declare\` first)` |
| `bash-witness-study.py` (no mode) / `count --bogus` | 64 usage | 64 / 64 |

## Findings

**F1 — all four registered commands return their registered outcome at both the live lane and 98bea7d.**
No drift in the entry surface. `count` recomputes 10/10 rows with `unresolved none`, and its control record
(`exit=0 denominator=16 exercised=14 skipped=2`, skips `verbs-sandboxed,verbs-break-injection`) matches the
round-12 declaration.

**F2 — non-entry mode `bash-witness-study.py check` is red at the tip, by design.**
`python3 tools/bash-witness-study.py check` at 98bea7d exits 1:

```
WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
WITNESS_CHECK: FAIL (1 problems; 96 files covered)
```

Cause traced by hashing `tools/mutate-and-run.sh` at successive revs `[OBSERVED]`:
round-12 `546b371` and `8742f5d` = `75ed93…` (the digest in `declaration.json#/inputs/runner`, and in the
companion's `historical_runner` field); round-16 `c699c8c` = `89722d…`; round-16 `05a2247` and tip `98bea7d` =
`0673d2…`. So the pin is the runner the round-12 sweep executed, and the round-16 runner edits legitimately moved
it. `check` is fail-closed on that move (`tools/bash-witness-study.py:1143-1147`), and neither registry row
registers `check` as the entry command or claims it exits 0 at the tip. **Not a C2 breach**: the registered entry
(`count`) reads only retained `results.tsv`/mutant/case-log evidence and does not consult the runner, which is why
row 3 holds while `check` drifts. No lane evidence needs rewriting; a re-pin of the frozen manifest would be a
new owner decision, not a wave-1 edit (instrument immutability, QUALITY 20). `[INFERENCE]` on the disposition.

**F3 — the live lane picked up concurrent sibling edits mid-observation; the registered entries are unaffected.**
My first `git --no-optional-locks status --porcelain` (at start) showed only untracked `round-16/__pycache__/`,
`round-17/` and `waves/round-17/`. A later status showed two tracked modifications, both with the identical
mtime `2026-10-20 12:21:34 -0300`:

```
 M .gitignore                                          (+2 lines)
 M .ufo/evidence/round-16/round-gate/runner-sha256.txt (+4 lines)
```

They were not produced by this seat (all my lane commands are read-only; the entry commands write nothing, and the
selftests write only under `tempfile.mkdtemp()`). Neither file is an input of the registered entries:
`witness-metadata --check` hashes only the round-12 `summary.json`, `declaration.json`, `declared.tsv` and the
rerun summary (`inputs=summary,declaration,declared,rerun_summary`), and `count` reads the round-12 BashWitness
evidence tree, which `git status` reports clean. The committed-rev mirror rows in the table above isolate the
result from this dirt.

**F4 — `witness-metadata` deliberately does not live-hash the producer or runner.** Its companion records
`producer.checked_live=false` and `historical_runner.checked_live=false` with the note that the runner digest is a
"C1 historical pin source"; this is the documented bounded scope, not a hole introduced now. The gate's clean
verdict therefore says nothing about the tip runner — consistent with F2 and with the row's stated scope.

## Residual unknowns

- `tools/registry.json` and `tools/registry-check.py` do not exist at 98bea7d (`tools/` holds the seven round-12/13
  instruments); the R16-MON1 held-count cannot be reproduced until the wave lands. This table is the input
  evidence for those rows, but the monitor's own grading is unmeasured here.
- `bash-witness-study.py run` and `rerun` were not exercised: `run` writes into the lane evidence directory and
  `rerun` creates `rerun-<stamp>/`, both outside a leaf's write scope and neither a registered entry command.
- Live-lane dirt (F3) may keep changing during the wave; only the committed mirror is a stable measurement basis.

## Verdict

holds — `witness-metadata.py --check` (0 `metadata_consistent`), `witness-metadata.py --selftest` (0, 39/39),
`bash-witness-study.py count` (0, 10/10 classified, unresolved none) and `bash-witness-study.py selftest`
(0, 41/41) each return their registered outcome at the live lane and at 98bea7d; the only red mode is the
non-registered `check`, whose named `mutate-and-run.sh` drift is the round-16 runner move against a frozen
round-12 pin.
