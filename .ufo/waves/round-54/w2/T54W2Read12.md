# T54W2Read12 — cold read at C1, section `### Gate/probe registry`

- Seat: T54W2Read12 (wave 2, hyaku run 11, tameshi round 54)
- Milestone: C1 fresh read at C1
- Candidate (C1): `99c3bc88d704566197783f66b211ee0a830e0330`
- Section span at C1: start 1524, end 1541
- `section_sha256` (as printed by `.ufo/waves/round-54/reader-section.py`):
  `99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77`
- Section bytes: `SKILL.md` lines 1524-1540 (the trailing blank line 1541 is stripped by the
  sectionizer; `sectionize()` in `.ufo/evidence/round-18/measure.py` joins the body with `\n`
  and no trailing newline). Reproduced locally: same sha256, 17 lines, first line
  `### Gate/probe registry`, last line
  `to new material or establish full-page instruction sufficiency.`

## Verdict

**Clean. `findings: []`.**

Every rule in the section names an anchor that resolves at C1, no sentence contradicts another
in the section, no table cell is stale against the artifact it cites, and the duplicate /
run-together / missing-space scan is empty. JSON deliverable:
`.ufo/waves/round-54/w2/T54W2Read12.json`.

Nothing below is a finding; the evidence table records what I checked so an adjudicator can
re-run each line, and the reconciliations section records the three near-misses I decided not
to report, with why.

## Evidence per claim in the section

### Table row 1 — `repeated pristine controls` | gate

| Cell | Claim | Verification |
|---|---|---|
| Entry command | `--runs 3 --out DIR -- COMMAND ARG...` or `--snapshot DIR` | Both forms run: `--runs 3 --out <fresh>` exit 0 `REPEAT_CONTROL: controls_match`; `--snapshot .ufo/evidence/round-12/ControlGate` exit 0 `SNAPSHOT_OBSERVED id=controls_match exit=0`. `usage:` banner in the tool lists exactly these two forms plus `--selftest`. |
| Verdict map | `0 clean; 1 failed; 2 and 64 could-not-evaluate` | `EXIT_BY_ID` (`tools/repeat-control.py:122-130`): `controls_match 0`, `controls_mismatch 1`, `baseline_nonzero/command_unavailable/snapshot_tampered/setup_error 2`, `invalid_usage 64`. The tool's own docstring (`:48-51`) states: "`baseline_nonzero`, `command_unavailable`, `snapshot_tampered`, `setup_error` and `invalid_usage` are could-not-evaluate". So the `2 and 64` grouping is the tool's own vocabulary, not a stale summary. Runtime: usage arm exits 64 printing `REPEAT_CONTROL: invalid_usage`. |
| Self-test command | `python3 tools/repeat-control.py --selftest` | exit 0, `SELFTEST: PASS (29 cases)`. |
| Pinned values | `ControlGate/expected.json`, `mismatch/expected.json`; literal expected IDs/exits in tool selftest | Both blobs present at C1; `--snapshot` of the committed directory returns exit 0 and `--snapshot` of `mismatch/` returns `controls_mismatch`/1-shaped data (the selftest asserts `expected_exit == EXIT_BY_ID[expected_id]` at `:402`). |
| Write scope | fresh caller-selected DIR; isolated `$TMPDIR` selftest tree (`tameshi-r12-*`); snapshot read-only | `mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=strict_scratch_root())` (`:611`); strace of `--selftest` shows `tameshi-r12-repeat-control-selftest.1pnk3yrs` created under the seat TMPDIR. After snapshot + runs + selftests, `git -C <clone> status --porcelain` is empty: nothing written into the lane tree. |
| Owner | `tameshi` | lane owner; consistent with the heading's round-12 source line (`:1506-1508`, outside this section). |

### Table row 2 — `bash declared-witness study` | probe

| Cell | Claim | Verification |
|---|---|---|
| Entry command | `python3 tools/bash-witness-study.py count` | exit 0; prints `declared 0def0d3b… declared.tsv`, `control exit=0 denominator=16 exercised=14 skipped=2 skip=verbs-sandboxed,verbs-break-injection`, 10 classified rows. `cmd_count` (`:1051-1125`) reads evidence only — it never opens the runner, so the prose's "`count` never reads the runner" is exact. |
| Verdict map | `0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage only (argparse)` | 0 on `count` (above); 1 on `check` (DRIFT, below); 2 on `run`/`rerun` (runner-drift, below); 64 on an invalid subcommand (`bash-witness-study.py: error: argument mode: invalid choice: 'bogus'`), raised by `UsageParser.error` → `EXIT_USAGE` (`:1717-1725`), i.e. the argparse usage arm. |
| Self-test command | `python3 tools/bash-witness-study.py selftest` | exit 0, `WITNESS_SELFTEST: 51/51 pass`, `VERDICT: PASS`. |
| Pinned values | `BashWitness/declaration.json`, `declared.tsv`, `manifest.json` | All three blobs present at C1; `check` reports no TAMPER on any listed digest. |
| Write scope | own evidence directory plus isolated `$TMPDIR` selftest tree (`bash-witness-selftest-private.*`, selftest only); sibling object store read-only | `mkdtemp(prefix="bash-witness-selftest-private.", dir=strict_scratch_root())` (`:1259-1260`); strace shows `bash-witness-selftest-private.1s7w8ppt` under the seat TMPDIR. Sibling access is `["git","-C",kagi,"show","--end-of-options",…]` only (`:367`, `:916`) — read-only object reads, no write path. |
| Owner | `tameshi` | as above. |

### Prose paragraph

1. "Registry scope is these round-12 instruments; no new conformance assertion is made about the
   historical runner." — table holds exactly the two round-12 instruments named in the
   round-12 section above (`:1504-1508`).
2. "Witness declarations are integrity-frozen (declaration, mapping, target, spec, summary;
   `manifest.json` itself is not pinned, seat ReRead08)" — `cmd_check`'s required list is exactly
   `[DECLARATION_NAME, DECLARED_NAME, TARGET_NAME, SPEC_NAME, SUMMARY_NAME]` (`:1182-1187`), and
   `check` verifies every digest those five carry; `manifest.json` is not hashed by `check` and
   `manifest_files` excludes it, which is the round-27 ReRead08 M4 clause this sentence now
   states ("nothing pins manifest.json itself"). `seat ReRead08` resolves:
   `.ufo/waves/round-27/residual/ReRead08.md`.
3. "not blind: before declaring, their author had seen the source, the spec, the recorded
   aggregate outcomes and the per-defect KILLED/SURVIVED entries
   (`.ufo/evidence/round-12/BashWitness/declaration.json`; seat ReRead08)" — the tool's Disclosure
   block states the mapping "was authored from the pinned target's selftest and the embedded
   spec", and `declaration.json.disclosure` names the four outcome surfaces (kill-rate header,
   README coverage row, SOURCES S033 row, TABLE_BASH per-defect KILLED/SURVIVED). Both halves of
   the clause are in the cited receipt.
4. "The declaration's runner pin `75ed934d…` is stale at round 27 (`check` exits 1 DRIFT;
   `run`/`rerun` refuse, exit 2; `count` never reads the runner; seat Read25,
   `.ufo/waves/round-27/w1/Read25.md`)." — re-measured at C1, all four sub-claims hold:
   - `check` exits 1: `WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de470… committed=75ed934d…` + `FAIL (1 problems; 96 files covered)`.
   - `run` exits 2: `WITNESS_STUDY: CANNOT-EVALUATE (runner-drift …)`; `rerun` exits 2 with the same refusal.
   - `count` exits 0 (above) and does not read the runner.
   - `Read25.md` exists at C1 and states exactly this receipt (its `B1`).
5. "The bash study deepens one recorded case, never a seventh independently measured gate." —
   antecedent resolves: the page's six gates are at `:1133-1148` ("five measured families over the
   six gates"), and the bash study is the probe on the recorded bash-surface-census case.
6. "Calibration correction to the historical promotion paragraph above: `SHONEN.md` box 3 carried
   a scope-bounded `[~]` at round 12, not `[ ]`; `corpus/lessons/round-1-verifier-spotcheck.md`
   excludes it from the score." — `SHONEN.md` at the round-12 commit `546b371` reads
   `- [~] Instructions executable by an agent without oral context` with the scope-bounded lane
   assertion; the lesson says "with the score re-pinned at 6 — the box-3 increment is not
   credited". Both halves true; "the historical promotion paragraph above" resolves to
   `:1497-1501`.
7. "Appending this registry does not extend the earlier Appendix A/B cold-read to new material or
   establish full-page instruction sufficiency." — self-limiting; Appendix A/B are the page's own
   worked appendices (`:1467`).

### Text-quality scan (QUALITY 104 classes)

- Table shape: header + separator + both rows each parse to exactly 8 cells under the declared
  8-column header — no malformed row.
- No trailing whitespace, no tabs, no double spaces anywhere in lines 1524-1540.
- Duplicate-parenthetical scan: the only repeated citation is `seat ReRead08` in two different
  parentheticals with different content (frozen-set parenthetical; receipt parenthetical). Not a
  duplicated parenthetical, and no identical-text repeat.
- No run-together token or missing space; the paragraph is one long line but token separation is
  intact (`ReRead08). The declaration's`, `exit 2; count`).

## Considered and reconciled (deliberately NOT reported)

1. **"0 clean; 1 failed" vs the tool's IDs `controls_match`/`controls_mismatch`.** A reader can
   join the label to the decision table five lines above (`:1512-1513`) and to
   `REPEAT_CONTROL: controls_match` output. The cell is a verdict summary, not the ID list; not
   defensible as a defect.
2. **Pinned-values cell lists `manifest.json` while the prose says "`manifest.json` itself is not
   pinned".** Reconciled by the column's own semantics (where the pinned values live) and by the
   word "itself": `check` hashes every digest recorded *in* the manifest and no digest *of* the
   manifest. Not a contradiction.
3. **`2 and 64 could-not-evaluate` (row 1) next to `64 usage only` (row 2).** The repeat-control
   docstring files `invalid_usage` (64) under could-not-evaluate in its own words, and row 2
   additionally says *why* 64 occurs (usage). Both rows are accurate for their own tool.

## Artifacts opened

- `SKILL.md` at C1 — `git show 99c3bc88…:SKILL.md`, lines 1524-1541 (section) and 1130-1150,
  1460-1523 (antecedents).
- `.ufo/waves/round-54/reader-section.py` (span/sha procedure).
- `.ufo/evidence/round-18/measure.py` at C1 (`sectionize()` boundary/sha rule).
- `tools/repeat-control.py` at C1 (exit map `:122-130`, usage path `:208-276`, selftest scratch
  `:611`, snapshot mode, docstring `:36-70`).
- `tools/bash-witness-study.py` at C1 (subcommands `:1740-1770`, `cmd_count`/`cmd_check`,
  `UsageParser` `:1717-1725`, selftest scratch `:1259-1265`, disclosure block `:55-70`).
- `.ufo/evidence/round-12/ControlGate/expected.json`, `ControlGate/mismatch/expected.json`.
- `.ufo/evidence/round-12/BashWitness/declaration.json`, `declared.tsv`, `manifest.json`,
  `declaration-hash.txt`, `selftest.sha256.txt`.
- `.ufo/waves/round-27/w1/Read25.md`, `.ufo/waves/round-27/residual/ReRead08.md`.
- `SHONEN.md` at C1; `SHONEN.md` at round-12 commit `546b371`; at `c7986cd`; at `121696b`.
- `corpus/lessons/round-1-verifier-spotcheck.md` at C1.
- `tools/mutate-and-run.sh` at C1 (sha256 `977de470…` — the drift target).

## Commands run (all in scratch; clone at `$S/fixture.KtAASO/lane`, `git rev-parse --show-toplevel` = that directory, HEAD = C1)

```console
$ export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read12
$ python3 .ufo/waves/round-54/reader-section.py <lane> 99c3bc88d704566197783f66b211ee0a830e0330 "### Gate/probe registry"
{"heading": "### Gate/probe registry", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1524, "end": 1541, "section_sha256": "99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77"}

$ git clone --shared <lane> "$D/lane" && git -C "$D/lane" checkout 99c3bc88…
99c3bc88d704566197783f66b211ee0a830e0330

# per-anchor existence (git cat-file -e at C1), 10 paths
tools/repeat-control.py -> PRESENT
tools/bash-witness-study.py -> PRESENT
.ufo/evidence/round-12/ControlGate/expected.json -> PRESENT
.ufo/evidence/round-12/ControlGate/mismatch/expected.json -> PRESENT
.ufo/evidence/round-12/BashWitness/declaration.json -> PRESENT
.ufo/evidence/round-12/BashWitness/declared.tsv -> PRESENT
.ufo/evidence/round-12/BashWitness/manifest.json -> PRESENT
corpus/lessons/round-1-verifier-spotcheck.md -> PRESENT
SHONEN.md -> PRESENT
.ufo/waves/round-27/w1/Read25.md -> PRESENT

$ python3 tools/bash-witness-study.py check
WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
WITNESS_CHECK: FAIL (1 problems; 96 files covered)
exit=1

$ python3 tools/bash-witness-study.py count
exit=0
declared	0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3	…/declared.tsv
control	exit=0	denominator=16	exercised=14	skipped=2	skip=verbs-sandboxed,verbs-break-injection
row	B1	KILLED	exit=1	…
(unresolved: none; witness_classified=10)

$ python3 tools/bash-witness-study.py run --timeout 5
WITNESS_STUDY: CANNOT-EVALUATE (runner-drift tools/mutate-and-run.sh sha256=977de470… committed=75ed934d…)
exit=2

$ python3 tools/bash-witness-study.py rerun
WITNESS_STUDY: CANNOT-EVALUATE (runner-drift …)
exit=2

$ python3 tools/bash-witness-study.py bogus
bash-witness-study.py: error: argument mode: invalid choice: 'bogus' (choose from 'declare', 'run', 'rerun', 'count', 'check', 'selftest')
exit=64

$ python3 tools/bash-witness-study.py selftest
WITNESS_SELFTEST: 51/51 pass
VERDICT: PASS
exit=0

$ python3 tools/repeat-control.py --selftest
SELFTEST: PASS (29 cases)
exit=0

$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
SNAPSHOT_OBSERVED id=controls_match exit=0
REPEAT_CONTROL: controls_match
exit=0

$ rm -rf out1 && python3 tools/repeat-control.py --runs 3 --out out1 -- true
REPEAT_OUT …/out1
REPEAT_CONTROL: controls_match
exit=0

$ python3 tools/repeat-control.py --runs 3
repeat-control: --out is required
REPEAT_CONTROL: invalid_usage
exit=64

$ python3 -c "<load both modules>; print(strict_scratch_root())"
rc strict_scratch_root() -> /fast/scratch/hyaku/tameshi-r54/T54W2Read12
bw strict_scratch_root() -> /fast/scratch/hyaku/tameshi-r54/T54W2Read12

$ TMPDIR=/nonexistent-r54-read12 python3 tools/repeat-control.py --selftest
repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-r54-read12' (could-not-evaluate)
REPEAT_CONTROL: setup_error
exit=2
$ TMPDIR=/nonexistent-r54-read12 python3 tools/bash-witness-study.py selftest
WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-r54-read12' (could-not-evaluate)
exit=2

$ strace -f -e trace=mkdir,mkdirat -o bs.strace python3 tools/bash-witness-study.py selftest
grep -o 'bash-witness-selftest-private\.[A-Za-z0-9_]*' bs.strace | sort -u
bash-witness-selftest-private.1s7w8ppt
$ strace -f -e trace=mkdir,mkdirat -o rc.strace python3 tools/repeat-control.py --selftest
grep -o 'tameshi-r12-repeat-control-selftest\.[A-Za-z0-9_]*' rc.strace | sort -u
tameshi-r12-repeat-control-selftest.1pnk3yrs

$ git -C "$D/lane" status --porcelain
(empty)  # no lane file written by any read/test above

# section-sha reproduction under the sectionizer rule (lines 1524-1540, no trailing newline)
sha256: 99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77

# box-3 correction
$ git show 546b371:SHONEN.md | sed -n '9,11p'
- [~] Instructions executable by an agent without oral context
  [lane assertion, scope-bounded: fleet round-1 cold-read of blob 4eb4cf3:SKILL.md — Appendix A + B sweep recipe only, …]
$ git show 99c3bc88…:corpus/lessons/round-1-verifier-spotcheck.md | sed -n '17p'
… with the score re-pinned at 6 — the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed); …
```

## Tooling / bounds

- No tool installed or upgraded; `strace` was already present. No pacman transaction was attempted.
- Read-only everywhere outside my lane write scope; the only writes are
  `.ufo/waves/round-54/w2/T54W2Read12.json` (this seat) and `.ufo/waves/round-54/w2/T54W2Read12.md`.
- All mutating git calls in fixtures used `-C "$D"` on a `git clone --shared` under
  `/fast/scratch/hyaku/tameshi-r54/T54W2Read12/`; `SKILL.md` and every other lane file untouched
  (clone `git status` empty after all runs).

## Known limits

- I did not re-derive the round-12 blob of `SHONEN.md` from the `.ufo/evidence/round-12/` receipts;
  I used the round-12 commit `546b371` (the round-12 verifier spot-check commit) as the round's
  state. Box 3 is `[~]` there and at every later blob checked (`c7986cd`, `121696b`, C1).
- The `seat ReRead08` citation names no path; it resolves to
  `.ufo/waves/round-27/residual/ReRead08.md` (the round-27 residual report), which is the only
  ReRead08 deliverable at C1 plus its `.ufo/evidence/round-27/coldread/traces/` inputs.
- The verdict-map label choice `0 clean; 1 failed` was accepted as a summary of
  `controls_match`/`controls_mismatch` (reasoning above); an adjudicator preferring the literal
  finding IDs could read it as a minor label gap.
