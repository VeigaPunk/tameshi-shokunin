# Read25 cold read: SKILL.md "### Gate/probe registry" (line 1499)

## Verdict

wrong-expectation. The section stays uncovered for C1 at rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. The repeat-control row and the calibration correction check out. Two registry cells are false (bash write scope and exit 64), and one paragraph claim, that witness declarations are integrity-frozen, does not hold for the bash study's runner pin at this revision. The section never discloses that pin drift.

## Setup

- Clone: /tmp/Read25-orwmay13/fleet/tameshi-shokunin, detached at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 matches the pinned value.
- Section: SKILL.md lines 1499 to 1516. It ends before the next level-2 heading, "Pin disposition and provenance correction", at line 1517.
- Receipts: Read25-1 to Read25-26 in .ufo/evidence/round-27/coldread/traces/. All 26 have rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 and no external or live-lane reads.
- Class: record. The section is a registry table, a short paragraph and a calibration correction, all stating facts with pointers. I still ran every named entry and self-test command, so the class does not change the verdict.

## Findings

Blocking gap B1: the bash study's runner pin is stale at 2227, and the section does not say so.

- check exits 1 with "WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5" (Read25-10; tools/bash-witness-study.py:1156, return at :1222).
- run and rerun refuse before any sweep starts, with "WITNESS_STUDY: CANNOT-EVALUATE (runner-drift ...)" and exit 2 (Read25-25, Read25-26). The refusal is raised in ensure_target_and_spec (:569). _prepare (:928-934) calls it, and cmd_run and cmd_rerun (:1010-1019) call _prepare first.
- count, the entry command the section lists, exits 0 and never reads the runner (Read25-4 inputs; cmd_count at :1051-1125).
- Only the whole-runner digest is stale. extract_spec on the current runner gives sha256 d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741 (Read25-22), which equals the spec pin in declaration.json.

Wrong expectation W1: the bash row's write scope names an isolated /tmp/tameshi-r12-* location. That prefix does not appear in tools/bash-witness-study.py (Read25-8, Read25-18). The selftest's only /tmp use is tempfile.mkdtemp(prefix="bash-witness-selftest-private.", dir="/tmp") at :1240-1241, with a nested bash-witness-selftest.* directory at :1245-1246. The evidence-directory half of the row is right: the sweep passes --workdir inside the evidence tree (:606-609; Read25-23).

Wrong expectation W2: the bash row's verdict map says "64 usage/could-not-evaluate". Exit 64 is EXIT_USAGE (:119) and is raised only by UsageParser.error (:1724), for argparse usage errors. could-not-evaluate is exit 2, EXIT_CANNOT (:949, :1073, :1774) (Read25-21). The row's "2 could-not-evaluate" entry is right.

Wrong expectation W3: the paragraph calls witness declarations integrity-frozen. At 2227 that holds for declaration.json, declared.tsv, the target, the spec, summary.json and manifest.json, since check reports no TAMPER line (Read25-10). It does not hold for the runner input, whose pinned digest is stale (B1).

Minor gaps:
- M1: the repeat row labels exit 0 "clean" and exit 1 "failed". The tool's findings are controls_match and controls_mismatch (tools/repeat-control.py:122). The exit codes are right.
- M2: "never a seventh independently measured gate" and "Registry scope is these round-12 instruments" are scope claims. I checked only that both instruments date to round 12.
- M3: "inherited prior source/spec exposure" is looser than the disclosure. The disclosure lists recorded aggregate outcomes, a coverage row, a SOURCES row and per-defect TABLE_BASH KILLED/SURVIVED entries (declaration.json disclosure, Read25-6).
- M4: the Kind and Owner cells are registry metadata and cannot be checked from code.

## What checks out

- Repeat-control row. Run mode: three identical controls, controls_match, exit 0 (Read25-5); --out must not already exist (tools/repeat-control.py:315). Snapshot mode: stable snapshot exit 0 (Read25-11), mismatch snapshot exit 1 (Read25-12); the mode executes nothing (:55, :449). Self-test: "SELFTEST: PASS (29 cases)", exit 0 (Read25-2); its scratch is /tmp/tameshi-r12-repeat-control-selftest.* (:597). Pinned files: ControlGate/expected.json (controls_match, exit 0) and mismatch/expected.json (controls_mismatch, exit 1) (Read25-6). Exit map: EXIT_BY_ID (:122).
- Bash row, in part. count exits 0 with witness_classified=10 and unresolved none (Read25-4). selftest exits 0 with "WITNESS_SELFTEST: 51/51 pass" (Read25-3). declaration.json, declared.tsv and manifest.json are present and verify (Read25-6, Read25-10). Sibling reads are read-only git show calls on kagi (:347-350). The count exit codes match cmd_count (:1073 exit 2, :1125 exit 1 or 0).
- Calibration correction. SHONEN.md at the round-12 landing commit 9df9212 has box 3 as "[~] Instructions executable by an agent without oral context", with the qualifier "scope-bounded: fleet round-1 cold-read ... Appendix A + B sweep recipe only" (Read25-14 line 9; Read25-19). So "carried a scope-bounded [~] at round 12, not [ ]" is accurate. The lesson file says "the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed)" (Read25-7). Appendix A and B are at SKILL.md:527 and :594.

## Monitor reasons

- input-drift:SHONEN.md. The correction describes round 12. The round-12 blob (3b1dc526...) is the state the correction describes. Later commits changed SHONEN.md (Read25-9), but that does not change what the round-12 blob says, so the correction stands.
- input-drift:tools/mutate-and-run.sh. Real for this section (B1, W3), though the section text never names the file. It enters through declaration.json's runner pin.
- input-drift:tools/bash-witness-study.py. I checked the entry command, self-test and verdict map against the current file (sha256 60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9).
- Outside this section, for L1: SKILL.md:1472-1473 says box 3 was "[ ]" at its write and "[~]" only since round 16. The blobs at c7986cd and 121696b both show "[~]" at line 9 (Read25-15, Read25-16). I did not check commits before cd31c6b, so I cannot say which write that paragraph meant.

## Smallest safe correction (for L1; nothing edited)

1. Bash row write scope: replace "isolated /tmp/tameshi-r12-*" with "isolated /tmp/bash-witness-selftest-private.* (selftest only)".
2. Bash row verdict map: replace "64 usage/could-not-evaluate" with "64 usage only".
3. Add one sentence after the table: "At 2227 the runner pin is stale. check exits 1 (DRIFT). run and rerun refuse with CANNOT-EVALUATE runner-drift (exit 2). count does not read the runner. The extracted spec still matches d2ad3f29...; re-declare the runner pin before any sweep."
4. In the paragraph, replace "integrity-frozen" with the list of what is frozen (declaration, declared mapping, target, spec, summary, manifest), and say the runner pin is stale at 2227.
5. Optional: repeat row labels "controls_match" and "controls_mismatch" in place of "clean" and "failed".

## Verification gaps

- No sweep was run. run and rerun refuse before one starts, so the sweep's behaviour at this revision is unobserved.
- Kind and Owner cells, the seventh-gate sentence and the lane's kill-rate accounting were not checked.
- SKILL.md:1472-1473 and commits before cd31c6b were not checked. They are outside the section.
- The clone followed step 1: git clone from the live lane, then a detached checkout. That ran outside the collector and is not listed as a command. The heading scan of SKILL.md also ran outside the collector.

## Tooling

No tool was installed or upgraded. I read the tooling directive (RULES.md) first. The collector's strace, python3, git, grep and sha256sum were already present and were used as found.

```json
{
 "schema": "tameshi-coldread-report-v2",
 "seat": "Read25",
 "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
 "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [
  {
   "start": 1499,
   "heading": "### Gate/probe registry",
   "class": "record",
   "verdict": "wrong-expectation",
   "blocking_gaps": [
    "B1 undisclosed runner-pin drift: the frozen runner pin (declaration.json inputs.runner sha256 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5) does not match tools/mutate-and-run.sh (sha256 fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de). check exits 1 with DRIFT (Read25-10; tools/bash-witness-study.py:1156, :1222). run and rerun exit 2 before any sweep starts with CANNOT-EVALUATE runner-drift (Read25-25, Read25-26; ensure_target_and_spec :569, reached via _prepare :928-934 from cmd_run and cmd_rerun :1010-1019). The listed entry command count exits 0 and never reads the runner (Read25-4 inputs; cmd_count :1051-1125). The section discloses none of this."
   ],
   "wrong_expectations": [
    "W1 bash row write scope names isolated /tmp/tameshi-r12-*. tools/bash-witness-study.py never uses that prefix (Read25-8, Read25-18). Its only /tmp use is tempfile.mkdtemp(prefix=bash-witness-selftest-private., dir=/tmp) at :1240-1241, with a nested bash-witness-selftest.* directory at :1245-1246. The evidence-directory half of the row is right: the sweep passes --workdir inside the evidence tree (:606-609; Read25-23).",
    "W2 bash row verdict map says 64 usage/could-not-evaluate. Exit 64 is EXIT_USAGE (:119), raised only by UsageParser.error (:1724) for argparse usage errors. could-not-evaluate is exit 2, EXIT_CANNOT (:949, :1073, :1774) (Read25-21).",
    "W3 the paragraph says witness declarations are integrity-frozen. That holds at 2227 for declaration.json, declared.tsv, the target, the spec, summary.json and manifest.json: check reports no TAMPER line (Read25-10), and extract_spec on the current runner reproduces the pinned spec sha256 d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741 (Read25-22). It does not hold for the runner input, whose pinned digest is stale (B1)."
   ],
   "minor_gaps": [
    "M1 repeat row labels exit 0 as clean and exit 1 as failed. The tool's findings are controls_match and controls_mismatch (tools/repeat-control.py:122). The exit codes are correct (Read25-2, Read25-5, Read25-11 exit 0; Read25-12 exit 1).",
    "M2 two scope sentences are checked only for round dating: The bash study deepens one recorded case, never a seventh independently measured gate; Registry scope is these round-12 instruments.",
    "M3 inherited prior source/spec exposure is looser than the disclosure, which lists recorded aggregate outcomes, a coverage row, a SOURCES row and per-defect TABLE_BASH KILLED/SURVIVED entries (declaration.json disclosure, Read25-6).",
    "M4 the Kind and Owner cells are registry metadata and cannot be checked from code."
   ],
   "commands_executed": [
    "python3 -c 'import sys;[print(open(p,encoding='\"'\"'utf-8'\"'\"').read()[:200000]) for p in sys.argv[1:]]' tools/repeat-control.py tools/bash-witness-study.py",
    "python3 tools/repeat-control.py --selftest",
    "python3 tools/bash-witness-study.py selftest",
    "python3 tools/bash-witness-study.py count",
    "python3 tools/repeat-control.py --runs 3 --out /tmp/Read25-W-ctl-1 -- python3 -c 'print('\"'\"'pristine-control'\"'\"')'",
    "python3 -c 'import sys;[print(open(p,encoding='\"'\"'utf-8'\"'\"').read()[:200000]) for p in sys.argv[1:]]' .ufo/evidence/round-12/ControlGate/expected.json .ufo/evidence/round-12/ControlGate/mismatch/expected.json .ufo/evidence/round-12/BashWitness/declaration.json .ufo/evidence/round-12/BashWitness/declared.tsv .ufo/evidence/round-12/BashWitness/manifest.json",
    "python3 -c 'import sys;[print(open(p,encoding='\"'\"'utf-8'\"'\"').read()[:200000]) for p in sys.argv[1:]]' SHONEN.md corpus/lessons/round-1-verifier-spotcheck.md",
    "grep -n -E 'EXIT_[A-Z]+ *=|mkdtemp|tameshi-r12|RUNNER *=|EVIDENCE_DEFAULT *=|KAGI_DEFAULT *=|def cmd_[a-z]+|DRIFT|SWEEP_DIR *=|SELF *=|EVIDENCE_ROOT *=' tools/bash-witness-study.py tools/repeat-control.py",
    "git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin log 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 '--format=%H|%ad|%s' --date=short -- SHONEN.md",
    "python3 tools/bash-witness-study.py check",
    "python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate",
    "python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch",
    "git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin log 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 -E -i '--grep=round[ -]?(12|16)' '--format=%H|%ad|%s' --date=short",
    "bash -c 'git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show 9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md | sha256sum; git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show 9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md | grep -n \"^- \\[\"'",
    "bash -c 'git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show c7986cdf051cbe9d047f02f76f2e1da0b36a84e3:SHONEN.md | sha256sum; git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show c7986cdf051cbe9d047f02f76f2e1da0b36a84e3:SHONEN.md | grep -n \"^- \\[\"'",
    "bash -c 'git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show 121696bf92db813f75f792be8590cf2c2c98edb1:SHONEN.md | sha256sum; git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show 121696bf92db813f75f792be8590cf2c2c98edb1:SHONEN.md | grep -n \"^- \\[\"'",
    "bash -c 'git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SHONEN.md | sha256sum; git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SHONEN.md | grep -n \"^- \\[\"'",
    "grep -n -E '\"git\"|/tmp|unresolved|def classify|def counts|def build_summary|def cmd_count|read-only|git_clean_env\\(\\)' tools/bash-witness-study.py",
    "git -C /tmp/Read25-orwmay13/fleet/tameshi-shokunin show 9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md",
    "sha256sum tools/trace-inputs.py",
    "grep -n -E 'EXIT_USAGE|EXIT_CANNOT|EXIT_FAIL|def main|return EXIT' tools/bash-witness-study.py",
    "python3 -c 'import hashlib,importlib.util; s=importlib.util.spec_from_file_location('\"'\"'bws'\"'\"','\"'\"'tools/bash-witness-study.py'\"'\"'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); t=open('\"'\"'tools/mutate-and-run.sh'\"'\"',encoding='\"'\"'utf-8'\"'\"').read(); x=m.extract_spec(t); print('\"'\"'extract_spec_sha256'\"'\"', hashlib.sha256(x.encode('\"'\"'utf-8'\"'\"')).hexdigest()); print('\"'\"'runner_sha256'\"'\"', hashlib.sha256(open('\"'\"'tools/mutate-and-run.sh'\"'\"','\"'\"'rb'\"'\"').read()).hexdigest())'",
    "grep -n -E 'workdir|--target|--regression|mutate-and-run|subprocess.run\\(|Popen' tools/bash-witness-study.py",
    "grep -n -E 'def _prepare|ensure_target_and_spec\\(|def load_declaration|def verify_declared_digest|def cmd_count|_prepare\\(' tools/bash-witness-study.py",
    "python3 tools/bash-witness-study.py run",
    "python3 tools/bash-witness-study.py rerun"
   ],
   "opened": [
    ".ufo/evidence/round-12/BashWitness/bash-surface-census.spec",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-run.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep.cli.exit",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep.cli.log",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/defects.tsv",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B1.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B10.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B2.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B3.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B4.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B5.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B6.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B7.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B8.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B9.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/control.out",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B1.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B10.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B2.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B3.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B4.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B5.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B6.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B7.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B8.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B9.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/pristine.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/results.tsv",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/spec.copy",
    ".ufo/evidence/round-12/BashWitness/declaration-before-run.txt",
    ".ufo/evidence/round-12/BashWitness/declaration-hash.txt",
    ".ufo/evidence/round-12/BashWitness/declaration.json",
    ".ufo/evidence/round-12/BashWitness/declare.out",
    ".ufo/evidence/round-12/BashWitness/declared.tsv",
    ".ufo/evidence/round-12/BashWitness/manifest.json",
    ".ufo/evidence/round-12/BashWitness/pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/cli.exit",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/cli.log",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/defects.tsv",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B1.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B10.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B2.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B3.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B4.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B5.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B6.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B7.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B8.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B9.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/control.out",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/manifest.json",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B1.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B10.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B2.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B3.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B4.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B5.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B6.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B7.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B8.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B9.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/pristine.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/results.tsv",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/spec.copy",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
    ".ufo/evidence/round-12/BashWitness/selftest.out",
    ".ufo/evidence/round-12/BashWitness/selftest.prefix.out",
    ".ufo/evidence/round-12/BashWitness/selftest.sha256.txt",
    ".ufo/evidence/round-12/BashWitness/summary.json",
    ".ufo/evidence/round-12/BashWitness/sweep/cli.exit",
    ".ufo/evidence/round-12/BashWitness/sweep/cli.log",
    ".ufo/evidence/round-12/BashWitness/sweep/defects.tsv",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B1.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B10.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B2.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B3.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B4.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B5.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B6.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B7.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B8.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B9.out",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/control.out",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B1.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B10.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B2.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B3.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B4.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B5.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B6.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B7.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B8.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B9.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/pristine.pristine.sh",
    ".ufo/evidence/round-12/BashWitness/sweep/results.tsv",
    ".ufo/evidence/round-12/BashWitness/sweep/spec.copy",
    ".ufo/evidence/round-12/ControlGate/expected.json",
    ".ufo/evidence/round-12/ControlGate/mismatch/expected.json",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.exit",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stderr",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stdout",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.exit",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stderr",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stdout",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.exit",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stderr",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stdout",
    ".ufo/evidence/round-12/ControlGate/run-1.exit",
    ".ufo/evidence/round-12/ControlGate/run-1.stderr",
    ".ufo/evidence/round-12/ControlGate/run-1.stdout",
    ".ufo/evidence/round-12/ControlGate/run-2.exit",
    ".ufo/evidence/round-12/ControlGate/run-2.stderr",
    ".ufo/evidence/round-12/ControlGate/run-2.stdout",
    ".ufo/evidence/round-12/ControlGate/run-3.exit",
    ".ufo/evidence/round-12/ControlGate/run-3.stderr",
    ".ufo/evidence/round-12/ControlGate/run-3.stdout",
    "SHONEN.md",
    "corpus/lessons/round-1-verifier-spotcheck.md",
    "tools/bash-witness-study.py",
    "tools/mutate-and-run.sh",
    "tools/repeat-control.py",
    "tools/trace-inputs.py"
   ],
   "inputs": {
    ".ufo/evidence/round-12/BashWitness/bash-surface-census.spec": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-run.out": "56ca34615f6c2d84a1305c3435458e6bd0c1732dc11095eb4e8b5291deb1c102",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep.cli.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep.cli.log": "944b82b0727b35eddbd5ed020948c43afadbedd1cce515a9b8cbecf1c81282d8",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/defects.tsv": "0dee2387f756b058cb466577a8893856a4078a7d5946d98af1fbbcb3ecae6342",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B10.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B2.out": "879b7d8e2cf90d13e4823e02e6130187bb072c77582a55b6bed129244c1675ee",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B3.out": "38737f1f34733faabba3dda448c7e380b90a380157d7a89a757f2d3d660b0868",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B4.out": "cca77bd91adfe019a8ef26e931c98ac21eaf0e13b607faad6b9014bba20e1ff4",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B5.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B6.out": "0691009001b8c808f60cb9a90a9481455d023106a1a14e8eb2197bee32ab37f3",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B7.out": "75ae64703c47896c0e6cc2b1347790c30c511a1f762cda44cd7a38a0af6559f1",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B8.out": "e972da147adbdbe7df0be252e981fdca3b772c972f338abefd8c92c06856beca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/B9.out": "468723a0be9a5bcd716ea6c69fb3bb399b3f9a2a8bbf94267b773abc8f615e75",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/evidence/control.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B1.pristine.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B10.pristine.sh": "001b757454954cfac740530139d1416dc26e9dc40c2f7cd1c0e51bbbf2354bbd",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B2.pristine.sh": "443ce1fdd35e1a0de2c42ef809d30beef68252ba80972f67c681cc8760a908b3",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B3.pristine.sh": "5efd188121f8e7b9fb100caa27b973cb4603e1b6157fbf13c4b100a86603ba3d",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B4.pristine.sh": "c5f3b2b9d479fbf37aa28216d58f5f97220405cf0a140eef42409e0e97201a72",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B5.pristine.sh": "1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B6.pristine.sh": "627a037aaa27104f286acc9220d176dd45df5fe9e1371fc418962d98af793c54",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B7.pristine.sh": "0c920258f41e6367f0a00b8b51d319372875b1d27b68b8e47a5702a286a31aaa",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B8.pristine.sh": "cce2b52381d0faed40ed7adc8f63f8d9a08d631ed7812357e8aec5ca757b47fa",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/mutant-B9.pristine.sh": "e1ee079ac2f3db7ed5f57f2b3d33c732f7913880e18dd91d5128f086d63a10ad",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/pristine.pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/results.tsv": "8ec8ea9468ba97b5007e715639b6e2014daf17ac36afd4e6cff55840f5fb3e97",
    ".ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/spec.copy": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/BashWitness/declaration-before-run.txt": "d2343ddf7675c09313b02115453095969a285ed7cc3d85abd72b9c1e13b40042",
    ".ufo/evidence/round-12/BashWitness/declaration-hash.txt": "5fcb6d31f50eb4e4f6e09adaa41de20074ef571456dc42e7d930471b91e454ea",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declare.out": "c9e1c65cf25eeddfea2b078f839516c254ed7d2be59b3d8958dfe474d4994f44",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/manifest.json": "273ffc39308a6c55bdb1c8f7a86bac9f95886ec470773c99b4d1e2db5b25e1cf",
    ".ufo/evidence/round-12/BashWitness/pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/cli.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/cli.log": "bcfce949fee3c64538b50a0b22f41c152732c259fa259fbc662dc398d35420d4",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/defects.tsv": "0dee2387f756b058cb466577a8893856a4078a7d5946d98af1fbbcb3ecae6342",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B10.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B2.out": "879b7d8e2cf90d13e4823e02e6130187bb072c77582a55b6bed129244c1675ee",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B3.out": "38737f1f34733faabba3dda448c7e380b90a380157d7a89a757f2d3d660b0868",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B4.out": "cca77bd91adfe019a8ef26e931c98ac21eaf0e13b607faad6b9014bba20e1ff4",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B5.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B6.out": "0691009001b8c808f60cb9a90a9481455d023106a1a14e8eb2197bee32ab37f3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B7.out": "e1457e49c311640e1df770783c4ec4ce35028a879bddbfcb2c53a4450a68d3d6",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B8.out": "e972da147adbdbe7df0be252e981fdca3b772c972f338abefd8c92c06856beca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/B9.out": "468723a0be9a5bcd716ea6c69fb3bb399b3f9a2a8bbf94267b773abc8f615e75",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/evidence/control.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/manifest.json": "80ae3ea7e5cdf1fa94960b7ed2cc7c7e3bc5e26002d58d7fe22c0a8f57c49d3f",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B1.pristine.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B10.pristine.sh": "001b757454954cfac740530139d1416dc26e9dc40c2f7cd1c0e51bbbf2354bbd",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B2.pristine.sh": "443ce1fdd35e1a0de2c42ef809d30beef68252ba80972f67c681cc8760a908b3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B3.pristine.sh": "5efd188121f8e7b9fb100caa27b973cb4603e1b6157fbf13c4b100a86603ba3d",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B4.pristine.sh": "c5f3b2b9d479fbf37aa28216d58f5f97220405cf0a140eef42409e0e97201a72",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B5.pristine.sh": "1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B6.pristine.sh": "627a037aaa27104f286acc9220d176dd45df5fe9e1371fc418962d98af793c54",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B7.pristine.sh": "0c920258f41e6367f0a00b8b51d319372875b1d27b68b8e47a5702a286a31aaa",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B8.pristine.sh": "cce2b52381d0faed40ed7adc8f63f8d9a08d631ed7812357e8aec5ca757b47fa",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/mutant-B9.pristine.sh": "e1ee079ac2f3db7ed5f57f2b3d33c732f7913880e18dd91d5128f086d63a10ad",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/pristine.pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/results.tsv": "22f229e56dd5b1d65db9aae82a2d7194b4d80a593894b9e28b40235af81e36da",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/spec.copy": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-12/BashWitness/selftest.out": "2cd01d5271fc017cdea9e5e62a197952a67fd7e676926ce8f97ddb4590ed461c",
    ".ufo/evidence/round-12/BashWitness/selftest.prefix.out": "51d6cf720fd7ff77f7c399b5c8bbb76149d8ffaeea1d0959f4f1fd529f38878b",
    ".ufo/evidence/round-12/BashWitness/selftest.sha256.txt": "a0aaf77096a5e671810600f31da56e5c0bc416c9a744385bf35525f64666c98c",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    ".ufo/evidence/round-12/BashWitness/sweep/cli.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/BashWitness/sweep/cli.log": "66e9bf5087df815dacfe303e16a73102d82ade1597e439817c556999f818cd76",
    ".ufo/evidence/round-12/BashWitness/sweep/defects.tsv": "0dee2387f756b058cb466577a8893856a4078a7d5946d98af1fbbcb3ecae6342",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B10.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B2.out": "879b7d8e2cf90d13e4823e02e6130187bb072c77582a55b6bed129244c1675ee",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B3.out": "38737f1f34733faabba3dda448c7e380b90a380157d7a89a757f2d3d660b0868",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B4.out": "cca77bd91adfe019a8ef26e931c98ac21eaf0e13b607faad6b9014bba20e1ff4",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B5.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B6.out": "0691009001b8c808f60cb9a90a9481455d023106a1a14e8eb2197bee32ab37f3",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B7.out": "c76b809c8262c9ba3f715f63e594f5e06a1e4591da8ee8538fb963e1d8736884",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B8.out": "e972da147adbdbe7df0be252e981fdca3b772c972f338abefd8c92c06856beca",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/B9.out": "468723a0be9a5bcd716ea6c69fb3bb399b3f9a2a8bbf94267b773abc8f615e75",
    ".ufo/evidence/round-12/BashWitness/sweep/evidence/control.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B1.pristine.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B10.pristine.sh": "001b757454954cfac740530139d1416dc26e9dc40c2f7cd1c0e51bbbf2354bbd",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B2.pristine.sh": "443ce1fdd35e1a0de2c42ef809d30beef68252ba80972f67c681cc8760a908b3",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B3.pristine.sh": "5efd188121f8e7b9fb100caa27b973cb4603e1b6157fbf13c4b100a86603ba3d",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B4.pristine.sh": "c5f3b2b9d479fbf37aa28216d58f5f97220405cf0a140eef42409e0e97201a72",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B5.pristine.sh": "1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B6.pristine.sh": "627a037aaa27104f286acc9220d176dd45df5fe9e1371fc418962d98af793c54",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B7.pristine.sh": "0c920258f41e6367f0a00b8b51d319372875b1d27b68b8e47a5702a286a31aaa",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B8.pristine.sh": "cce2b52381d0faed40ed7adc8f63f8d9a08d631ed7812357e8aec5ca757b47fa",
    ".ufo/evidence/round-12/BashWitness/sweep/mutant-B9.pristine.sh": "e1ee079ac2f3db7ed5f57f2b3d33c732f7913880e18dd91d5128f086d63a10ad",
    ".ufo/evidence/round-12/BashWitness/sweep/pristine.pristine.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
    ".ufo/evidence/round-12/BashWitness/sweep/results.tsv": "6399660d94162245ef4d5011796e4f52c01ca61767865789049da2c5ee853fb9",
    ".ufo/evidence/round-12/BashWitness/sweep/spec.copy": "d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741",
    ".ufo/evidence/round-12/ControlGate/expected.json": "1b645be04d756c304a1ef5ecc221cf92f82c5f4afbdcfde4b77fe27117684aa1",
    ".ufo/evidence/round-12/ControlGate/mismatch/expected.json": "57f010e99e69a6632869c125229f8bcf0cfdaf866b6dcab9f16ed07ebc8f6771",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
    ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stdout": "b52929a30ae03d121fdd499fa74bd6ec58f06ebbc802c53c3b1918e67916b539",
    ".ufo/evidence/round-12/ControlGate/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/run-1.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
    ".ufo/evidence/round-12/ControlGate/run-1.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
    ".ufo/evidence/round-12/ControlGate/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/run-2.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
    ".ufo/evidence/round-12/ControlGate/run-2.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
    ".ufo/evidence/round-12/ControlGate/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
    ".ufo/evidence/round-12/ControlGate/run-3.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
    ".ufo/evidence/round-12/ControlGate/run-3.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
    "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
    "corpus/lessons/round-1-verifier-spotcheck.md": "f99ef0ae2b3a3e4939c86b9ce5ab1e701733801c1cc1c7063767edf692e0edad",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
    "tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
   },
   "external_inputs": {
    "tameshi-shokunin@9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md": "3b1dc52601bc1e5636909764c10f6a2ccfacbb8d9ca7991a0a8f2358a145ac58",
    "tameshi-shokunin@c7986cdf051cbe9d047f02f76f2e1da0b36a84e3:SHONEN.md": "f9bcbe1a24e3ffbcd5de8d7ffb36740d9f8a098e006f2d38bddc4e9a167e3e7b",
    "tameshi-shokunin@121696bf92db813f75f792be8590cf2c2c98edb1:SHONEN.md": "3b1dc52601bc1e5636909764c10f6a2ccfacbb8d9ca7991a0a8f2358a145ac58",
    "tameshi-shokunin@c699c8c36d6e4eca4b796b81a8247904aa145ec8:SHONEN.md": "4a11ade530ac802fa148bcd77661cb5c9447b0db099bf1d5532517560fadd26f"
   },
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-6.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-7.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-8.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-9.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-10.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-11.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-12.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-13.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-14.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-15.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-16.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-17.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-18.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-19.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-20.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-21.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-22.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-23.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-24.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-25.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read25-26.json"
   ]
  }
 ]
}
```

## Note on what I checked

I cold-read the section in a /tmp clone pinned to 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. I opened every cited tool and evidence file, and the SHONEN.md and lesson files, through the trace collector. I ran each named entry and self-test command: the repeat-control run, snapshot and selftest, and the bash-witness count, selftest, check, run and rerun commands. I compared each claim with the cited code and with the round-12 SHONEN.md blob. Two registry cells are false, and the runner pin is stale, so the section stays uncovered. The repeat-control row and the calibration correction hold.

COLDREAD Read25: wrong-expectation
