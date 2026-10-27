# T52W1MutC2 — frozen C2 counter probes

Counter: `.ufo/evidence/round-52/c2/measure.py`, copied to scratch before mutation. The pristine `--selftest` returned 0 (`cases=8 failed=0`); at base `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`, the counter returned 1 with observed `m1=2 m2=1 m3=3 m4=20 m5=1 m6=0 total=27` (base output details in the probe log). Constructed green fixture tree `59849bd64173834578e86637ef676456c1f022bc`; pristine counter returned 0, `total=0 C2_R52_PASS=true`.

Each mutant is a single textual behavior edit, stored with its exact bytes under `T52W1MutC2/`. Run protocol: `python3 <mutant>.py --selftest`; then pristine and mutant via `python3 <counter>.py --lane <scratch-clone> --rev <fixture-rev> --explain`. Fixture commits were made only in the scratch clone from the stated base; mutant files and receipts are deliverables, not lane counter edits.

| Mutant / clause | Fixture revision | Observed pristine → mutant (`total`) | Selftest | Verdict / note |
|---|---|---|---|---|
| M01 section boundary levels | `42e05b7a44e3b2e3cb4cd01f9062d974f0497b38` | 1 → 0 (`1 → 0`) | 0 | SURVIVED; nested `####` boundary hides the bad phrase from mutant |
| M02 “ledger legs” regex | `6d5cf13ebee17b484e67f5636779a0b2c7a25598` | 1 → 1 (`1 → 1`) | 0 | KILLED; mutant misses the phrase, and required nonempty phrase check still fails |
| M03 mte-interop mention cardinality | `01ef9b6ee2b789bb47d72f740d6ffeaee655460b` | 1 → 0 (`1 → 0`) | 0 | SURVIVED; duplicate mention passes weakened `>=1` check |
| M04 runner row `/tmp`/TMPDIR | `f75c136ae61f44d7895c361009403ba4a536a509` | 1 → 0 (`1 → 0`) | 0 | SURVIVED |
| M05 claim phrase must be unique/single-line | `f89f68fa5505e5860ba23499f0180b5ff960162b` | 1 → 0 (`1 → 0`) | 0 | SURVIVED; duplicate claim line with first valid pointer passes mutant |
| M06 pointer range validation | `681f869ce2da55adb34e1ee0d0942c4f424f5773` | 1 → 0 (`1 → 0`) | 0 | SURVIVED; mutant searches the whole runner rather than cited range |
| M07 bullet continuation scan | `65b782cd9874cdf077470b050d3d34ded44513d0` | 0 → 0 (`0 → 0`) | 0 | INCONCLUSIVE: fixture edit did not create a violation inside scanned bullet; pristine baseline passed |
| M08 r51 entry count | `70ed705ba0acf634696e7f57042f8e3d35cf031d` | 1 → 1 (`20 → 20`) | 0 | KILLED; remaining m4 guard returns 20 when entry count is not exactly 20, so weakened threshold alone cannot pass |
| M09 canonical reader-file path | `6cdd16da9f8f4432c48aae6941bbb3347c74b5c2` | 1 → 0 (`1 → 0`) | 0 | SURVIVED; wrong reader path is accepted |
| M10 quote substring/verbatim check | `cc004c328987d73e73631af3e916d47ddb250a1d` | 1 → 0 (`1 → 0`) | 1 | KILLED by selftest (`quote-forged` fails), although violation-tree run wrongly passes |
| M11 frozen floor labels | `13b8ee2cc8893d850072444a40483bc65e8b6a5e` | 1 → 0 (`1 → 0`) | 0 | SURVIVED; removal of floors accepts missing Read20 label |
| M12 findings-count equality | `018c7e3bb4b360facfb6a156fd9eb9ecec8008f7` | 1 → 1 (`1 → 1`) | 0 | KILLED; observed mutation still reports m4 mismatch on wrong count |
| M13 m5 byte-identical drift row | `aa86cd26aadb9783be01f393df719c045ffa8785` | 1 → 1 (`2 → 2`) | 0 | INCONCLUSIVE: tree had unrelated m4 mismatch (prior fixture state); not attributable to row check |
| M14 m6 T52 seat selection | `37bb7736cfaa16813b65424697212effbf107a63` | 1 → 0 (`1 → 0`) | 0 | SURVIVED on cleanly isolated tree; missing findings on T52 entry is missed |
| M15 minimum 20-character quote | `793b8c289ff785aeadf622fe11da48cdc3bd8565` | 1 → 1 (`1 → 1`) | 0 | INCONCLUSIVE: constructed 19-character quote did not isolate the min-length behavior; both runs flagged m4 |
| M16 m5 note phrase requirement | `24a6f0ad2d439fe3db5dde0d5d1c1ccee50a4a6e` | 1 → 0 (`1 → 0`) | 0 | SURVIVED; note lacking “unmeasured by sweep” passes weakened check |
| M17 whitespace-collapse behavior | green `59849bd64173834578e86637ef676456c1f022bc` | pristine 0 → mutant 1 (`0 → 18`) | 1 | KILLED on valid green tree and selftest; identity `squash` rejects whitespace-normalized quotes |

Full observed summary lines and probe details are in `T52W1MutC2/mutant-matrix.txt` and `T52W1MutC2/extra-probes.txt`. Mutant SHA-256 values are recorded in `T52W1MutC2/mutant-hashes.txt`.

## Evidence locations and commands

- Frozen counter and base C2 statements: `.ufo/evidence/round-52/c2/measure.py`; baseline command: `python3 <counter> --lane <scratch-clone> --rev ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 --explain`.
- Round-26 section and round-51 row: `SKILL.md:2132-2149`; inspect with `git show REV:SKILL.md` or detector command above.
- Runner needles: `tools/mutate-and-run.sh:434` (`old-string-count=`) and `:581` (`MUTATE: DEGRADED`); detector checks cited ranges.
- M4 reader records: `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-51/coldread/reads/T51W2ReadNN.md`; M5 cell: `corpus/knowledge/fleet-kill-rate-ledger.md:119`; same detector command.
- Counter copy pristine SHA-256 before scratch probes: `2c771d768e692811f7a39135800d27fbdb6403f4d12d46289bff404ee6ba9fbd`; after probes the lane file had the same SHA-256. Scratch clone and scratch files were removed. No tool installed or updated.

## Summary

- 17 single-edit counter mutants probed; several survive, exposing calibration gaps.
- Clean fixture baseline passed; base counter observed total=27.
- Inconclusive probes: M07, M13, M15; they are not counted as kills.
- Full output receipts and mutants are in `T52W1MutC2/`.
