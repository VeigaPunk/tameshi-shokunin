# T56W2Read10 — cold-read re-read at C0

Seat: `T56W2Read10` (wave 2, cold-read re-read 10/18)
Heading: `### Gate/probe registry`
Candidate (`cand`): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
Section at C0: lines **1541–1558** (18 lines), `section_sha256` = `99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77`
Verdict: **verified-record** (no findings)

Section hash computed with the FROZEN round-18 `sectionize` (never reimplemented),
loaded by `importlib` from
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py`,
whose blob at C0 hashes to `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`
(the round-56 validator's `R18_PIN`). The frozen round-18 `sectionize` splits C0's
`SKILL.md` into **64** sections; `### Gate/probe registry` matches **exactly one**
(start 1541, end 1558), so the heading is unambiguous and no sibling section
competes for it. The next heading is `## Pin disposition and provenance
correction — round 13` at line 1559; the parent is `## Repeated controls and
gate registry — round 12` at line 1521.

The section's bytes are identical at base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`
(lines 1528–1545) and at C0 (lines 1541–1558) — the round-56 commit shifted the
section 13 lines down without touching it, which is why the round-55 binder lost
it. The `section_sha256` above is the value the round-55 binder will bind.

Receipts: `.ufo/waves/round-56/w2/T56W2Read10-receipts/` (12 transcripts).

## Commands run

Setup (scratch, `/fast/scratch/hyaku/tameshi-r56/T56W2Read10`):

```
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin clone && git -C clone checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
```

Section hash (frozen round-18 `sectionize`, via `importlib`):

```
python3 -c "import importlib.util,subprocess;s=importlib.util.spec_from_file_location('m','/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);raw=subprocess.run(['git','-C','/home/vgpnk/Projects/shokunin/tameshi-shokunin','show','c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md'],capture_output=True).stdout;print([x for x in m.sectionize(raw) if x['heading']=='### Gate/probe registry'])"
```

→ `[{'start': 1541, 'end': 1558, 'heading': '### Gate/probe registry', 'sha256': '99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77'}]`

Every gate command was run with cwd = the clone at C0, with `TMPDIR` pointed at
this seat's scratch (so the tools' scratch trees land here, not in `/tmp`).

### Row 1 — repeated pristine controls (`tools/repeat-control.py`)

```
python3 tools/repeat-control.py --selftest
python3 tools/repeat-control.py --runs 3 --out $DIR/out -- python3 -c 'print("pristine-control")'
python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch
python3 tools/repeat-control.py --runs 3 --out $DIR/mis -- python3 -c 'import random;print(random.random())'
python3 tools/repeat-control.py --runs 3 --out $DIR/nz -- python3 -c 'import sys;sys.exit(7)'
python3 tools/repeat-control.py --runs 3 --out $DIR/na -- no-such-command-xyz
```

Observed:

| arm | expected by the section | observed | exit |
|---|---|---|---|
| `--selftest` | self-test runs | `SELFTEST: PASS (29 cases)` | 0 |
| run mode, 3 identical controls | 0 clean | `REPEAT_CONTROL: controls_match` | 0 |
| `--snapshot` on `ControlGate/` | 0 clean | `SNAPSHOT_EXPECTED id=controls_match exit=0` / `SNAPSHOT_OBSERVED id=controls_match exit=0` | 0 |
| `--snapshot` on `ControlGate/mismatch/` | 1 failed | `SNAPSHOT_EXPECTED id=controls_mismatch exit=1` / `SNAPSHOT_OBSERVED id=controls_mismatch exit=1` | 1 |
| run mode, differing stdout | 1 failed | `REPEAT_CONTROL: controls_mismatch` | 1 |
| run mode, stable nonzero baseline | 2 could-not-evaluate | `REPEAT_CONTROL: baseline_nonzero` | 2 |
| run mode, command not found | 2 could-not-evaluate | `REPEAT_CONTROL: command_unavailable` | 2 |
| snapshot with one byte appended | 2 could-not-evaluate | `SNAPSHOT_TAMPER run-1.stdout digest mismatch` → `snapshot_tampered` | 2 |
| `--out` pointing at an existing DIR | 64 could-not-evaluate | `repeat-control: --out already exists (refused, never overwritten)` → `invalid_usage` | 64 |

Every exit in the row's verdict map (`0 clean; 1 failed; 2 and 64 could-not-evaluate`)
is produced by the tool, and the tool's own `EXIT_BY_ID`
(`tools/repeat-control.py:122-130`) and docstring (lines 43-46) class exit 2 and
exit 64 as could-not-evaluate — the row's wording matches the instrument.

### Row 2 — bash declared-witness study (`tools/bash-witness-study.py`)

```
python3 tools/bash-witness-study.py selftest
python3 tools/bash-witness-study.py count
python3 tools/bash-witness-study.py check
python3 tools/bash-witness-study.py run
python3 tools/bash-witness-study.py rerun
python3 tools/bash-witness-study.py --bogus
```

Observed:

| arm | expected by the section | observed | exit |
|---|---|---|---|
| `selftest` | self-test runs | `WITNESS_SELFTEST: 51/51 pass` / `VERDICT: PASS` | 0 |
| `count` (the row's entry command) | 0 complete classified sample | `counts … total=10 witness_classified=10` / `unresolved none` | 0 |
| `count` on a tampered `declared.tsv` | 1 unresolved/failed integrity | `WITNESS_STUDY: TAMPER declared.tsv sha256=ac029138… committed=0def0d3b…` | 1 |
| `count` with `summary.json` removed | 2 could-not-evaluate | `WITNESS_STUDY: CANNOT-EVALUATE (missing …/summary.json — run the sweep first)` | 2 |
| `check` | 1 (runner DRIFT) | `WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de470… committed=75ed934d…` / `FAIL (1 problems; 96 files covered)` | 1 |
| `run` | 2 could-not-evaluate | `WITNESS_STUDY: CANNOT-EVALUATE (runner-drift …)` | 2 |
| `rerun` | 2 could-not-evaluate | `WITNESS_STUDY: CANNOT-EVALUATE (runner-drift …)` | 2 |
| missing mode (argparse usage) | 64 usage only | `bash-witness-study.py: error: the following arguments are required: mode` | 64 |

`EXIT_USAGE` is raised from exactly one place — `UsageParser.error`
(`tools/bash-witness-study.py:1743`) — so "64 usage only (argparse)" is exact,
and the tool's docstring confirms it: *"Usage errors exit 64 (the probe contract),
not argparse's default 2."*

### Pinned values, runner pin and disclosure

```
sha256sum tools/repeat-control.py tools/bash-witness-study.py tools/mutate-and-run.sh
sha256sum .ufo/evidence/round-12/ControlGate/expected.json .ufo/evidence/round-12/ControlGate/mismatch/expected.json .ufo/evidence/round-12/BashWitness/declaration.json .ufo/evidence/round-12/BashWitness/declared.tsv .ufo/evidence/round-12/BashWitness/manifest.json .ufo/evidence/round-12/BashWitness/summary.json
git show 9df9212:SHONEN.md
git show c7986cd:SHONEN.md
git show c7986cd~1:SHONEN.md
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

- Every file the row's "Pinned values" cell names exists at C0 and its digest
  matches the pin recorded for it: `expected.json` (`controls_match`, exit 0) and
  `mismatch/expected.json` (`controls_mismatch`, exit 1); `declaration.json`
  (`e8d2024a…`, matching its entry in `manifest.json`), `declared.tsv`
  (`0def0d3b…`, the digest `declaration.json` records), `manifest.json`
  (95 entries; `declaration.json`, `declared.tsv`, `summary.json`,
  `bash-surface-census.spec` and `pristine.sh` all present with digests matching
  the files on disk).
- The prose's "`manifest.json` itself is not pinned" holds: `manifest.json` does
  not appear in its own file map (`manifest_files` excludes it,
  `tools/bash-witness-study.py:840-841`), and grepping `manifest.json`'s own
  sha256 across `.ufo/evidence/round-12/` returns nothing.
- The runner pin `75ed934d…` recorded in `declaration.json` is stale: the runner
  at C0 hashes to `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`.
  `check` reports that as its single problem, `run`/`rerun` refuse with exit 2,
  and `count` still exits 0 — `cmd_count`'s body contains no `RUNNER` reference
  and no `mutate-and-run` reference, so the row's "`count` never reads the
  runner" is exactly right.
- The disclosure claim ("not blind: … the author had seen the source, the spec,
  the recorded aggregate outcomes and the per-defect KILLED/SURVIVED entries")
  is corroborated by `declaration.json`'s `disclosure` key, which enumerates the
  kill-rate header of `tools/mutate-and-run.sh`, the `corpus/README.md` coverage
  row, the `SOURCES.md S033 row and the recorded `TABLE_BASH` per-defect
  KILLED/SURVIVED entries.
- The calibration correction holds: at the round-12 landing commit `9df9212`,
  `SHONEN.md` line 9 reads `- [~] Instructions executable by an agent without
  oral context` with the scope-bounded qualifier on the next line; at
  `c7986cd~1` the same line reads `- [ ]` and `c7986cd` (which made it `[~]`) is
  an ancestor of `9df9212`. `corpus/lessons/round-1-verifier-spotcheck.md`
  records the non-credit ("the box-3 increment is not credited").
- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  exits 0.
- `git status --porcelain` in the C0 clone was **empty** after every command
  above — the read wrote nothing into the lane.

## Binder acceptance (proved, not asserted)

The round-56 reader gate was run against a scratch fixture carrying this seat's
report alone (`git clone --shared` → `checkout --detach c013745…` →
`git -C "$D" rev-parse --show-toplevel` asserted equal to the fixture dir →
the report, its `.md` and its receipts copied in → one commit in the fixture):

```
python3 .ufo/waves/round-56/validate-readers.py --lane . --rev HEAD \
    --c0 c0137451f5b7f22d65f748fc69f1b181f55e1378 --work $EMPTY --explain
```

→ `EXPLAIN PASS '### Gate/probe registry' sha=99285e24a71a`, and
`READERS_R56: rev=… c0=c0137451f5b7 r18=7ca87a7c9819 headings=18
passed=1/18 failed=17 refusals=17 warn=1 xrev=0`.

This seat's heading is the one `PASS`. The 17 remaining `READER_MISSING`
refusals are the other seventeen seats' reports, which are not in the tree yet;
they are not attributable to this seat. The single `WARN READER_FINDINGS_EMPTY`
is this seat's own empty `findings` list — the validator warns, it does not
refuse, and it is the expected shape for a section with nothing false in it.

## Findings

**None.** No statement in the section is false of the tree at C0 and no command
the section tells a reader to run fails.

## Notes (improvements, stale-but-true, style — not defects)

1. **Verdict labels, not exit codes.** Row 1 says "0 clean; 1 failed"; the
   tool's finding IDs are `controls_match` / `controls_mismatch`, so "failed"
   reads as *the command* failing when it means *the gate's verdict*. The exit
   codes and their classes are correct. The round-21 registry row for the same
   tool writes the IDs inline ("0 clean (controls_match); 1 failed
   (controls_mismatch)", `SKILL.md:2199`); attaching them here would cost one
   parenthesis.
2. **"Pinned values" is a file list, and one of its three entries is the one
   the prose says is not pinned.** Row 2's cell names `declaration.json`,
   `declared.tsv`, `manifest.json`; the prose says "`manifest.json` itself is not
   pinned". Both are true under different readings — the cell lists the
   artifacts the probe *verifies*, the prose speaks of what is *pinned by a
   digest*. The prose reconciles them explicitly, so the section is not
   self-contradictory. Renaming the column "artifacts verified" would remove
   the friction for a reader who meets the table before the paragraph. (The
   round-21 row for the same probe annotates each file and also names
   `summary.json` and the runner, `SKILL.md:2185`.)
3. **"a seventh independently measured gate" is a round-12 ordinal.** The study
   is a probe over the already-recorded leg 2 (`bash-surface-census`, defects
   B1–B10, target pinned at `fecee874…`), and `tools/registry.json` carries it
   as `kind: probe` — so the claim is true in substance. But the runner now
   carries **ten** legs (`SKILL.md:1345`, `:1432`;
   `tools/mutate-and-run.sh:88-97`), and "the seventh recorded case" is a live
   phrase elsewhere in the file (`:1598`, `:1799`). Time-scoping the ordinal
   would keep a C0 reader from reading it as a live count.
4. **The runner drift the paragraph discloses is still live at C0.** "is stale
   at round 27" marks first observation; the parenthetical exit contract holds
   verbatim at C0, and the drift has not been re-pinned since. Nothing is
   false; a reader could still come away thinking it was since repaired.
5. **One attribution has no path.** "seat ReRead08" is cited bare while "seat
   Read25" carries `.ufo/waves/round-27/w1/Read25.md`. The ReRead08 report
   resolves uniquely (`.ufo/waves/round-27/residual/ReRead08.md` is the only
   file of that name in the tree), so the citation is locatable, but a path
   would make it so without a search.

## Verification gaps

- The bash study's **sweep was not run**: `run` and `rerun` refuse before any
  sweep starts (runner drift), so the sweep's own behaviour at C0 is
  unobserved. Everything the section asserts about those two modes is the
  refusal itself, which was observed.
- `bash-witness-study.py declare` was not run (it writes into the evidence
  tree and would need a separate `--evidence` copy); the section makes no claim
  about it beyond the write-scope cell, which was verified at the code level
  (`--workdir` inside the evidence tree, `materialize_target` a read-only
  `git show`).
- The "Owner" and "Kind" cells are registry metadata; `Kind` was corroborated
  against `tools/registry.json` (`bash-witness-count` → `probe`) and the
  round-21 registry, but `Owner: tameshi` is not machine-checkable from the
  tree.
- The "seventh independently measured gate" sentence is a scope claim about the
  round-12 registry; I confirmed the study is a probe over recorded leg 2 and
  is not a runner leg, but I did not audit the round-12 kill-rate accounting
  the claim leans on.

## Tooling

No tool was installed or upgraded by this seat; every command used was already
present on the host (`git`, `python3`, `bash`, `coreutils`). No `pacman`,
`uv`, `npm` or `cargo` transaction was performed.
