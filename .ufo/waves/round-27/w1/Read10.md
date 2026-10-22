# Read10 cold read: SKILL.md:883-898, "### The report shape — what the opting-in lane receives"

**Verdict: `wrong-expectation`** (class `record`). This bucket is not credited. Two claims in the section do not hold when the cited record is read cold. Everything else the section says checks out.

## Read point and scope

- Lane revision `2227d8338c02aa9a5fd7d95c1a41b76865ad7647`. SKILL.md sha256 `386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95`, which matches the assignment.
- Clone: `/tmp/Read10-rfje/fleet/tameshi-shokunin`, detached at that revision. The four hashed inputs' working-tree sha256 values equal their committed blobs at that revision (receipts Read10-8, Read10-12, Read10-15).
- Section span: heading at line 883. The next heading, `### The mado run (T6-1, 2026-10-14) — measured`, is at line 899. There is no code fence inside 883-898.
- Class `record`: the section lists what the opting-in report contains and points at the mado case note and at the tool. It tells no reader to run a command.
- Monitor reason `input-drift:tools/mutate-and-run.sh`: the tool at this revision has sha256 `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`. Every tool claim below was checked against that file.

## Checks that hold

- **Tool sha256 pin.** `tools/mutate-and-run.sh:495` prints `MUTATE_TOOL: <path> sha256=`. The live output matches `sha256sum` (receipts Read10-6 and Read10-8).
- **Target sha256 and size.** `:497` prints `MUTATE_TARGET: <path> sha256= bytes=`. Live output shows `bytes=198` (Read10-6).
- **Control line.** `:529` (RED) and `:533` (GREEN) print `CONTROL: … pristine-sha256=`. Live output shows `CONTROL: GREEN (exit=0 …)` (Read10-6).
- **Kill-rate rows.** `:537` writes the `results.tsv` header (`id verdict exit duration-ms mutant-sha256 desc`). `:541` runs each defect into `$EVID/<id>.out`. `:550` prints `DEFECT <id>: KILLED|SURVIVED|…`, and `:552` appends the row. The live evidence file `evidence/F1.out` holds the suite's own text, `FAIL add` (Read10-11).
- **Restore proof.** `:558-564` prints `MUTATE_RESTORE: OK (target-sha256 before= after= pristine-sha256=)` only when the target and pristine hashes both match. Live output shows before equal to after (Read10-6). The section's parenthetical is accurate.
- **No tree-clean check.** `run_sweep` spans `:460-577` (Read10-5). None of the `status`, `porcelain` or `rev-parse` hits (Read10-7: lines 297, 1154-1193, 1876-1898) falls inside it. The round-18 correction is consistent with the code.
- **Note header.** `corpus/knowledge/mutation-case-mado-verify.md:8-9` says "this note is the only fleet file written by this run" (Read10-1, Read10-4).
- **Probes exist.** Note §2 (`:101-115`) has one row for each survivor: D3 `:110`, D5 `:111`, D7 `:112`, D8 `:113`, D9 `:114`, R1 `:115`.
- **Unknowns, recommendations, reproduce header.** Note §7 is at `:224`, §8 at `:240`, §9 at `:262` (Read10-4).

## Checks that do not hold

**W1. The reproduce block does not rebuild the sweep (`:262-293`).** Command block `:281-293`. Ten-edit block `:298-310`.

1. The `--defects` path, `/tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec` (`:286`), is absent on this host. `ls` returns "No such file or directory" (Read10-9). The tool refuses it: `MUTATE: SETUP (spec is not a regular file: /tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec)`, child exit 2 (Read10-13). The spec is not embedded in the note. Five of its ten rows are elided in the lane copy: `:299` (D1), `:301` (D3), `:304` (D6), `:305` (D7), `:308` (R1). Exact `@old` and `@new` strings cannot be rebuilt from the lane.
2. The block's target is the live working-tree file `mado-shokunin/tools/mado-verify.sh`. Its sha256 is `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1` (Read10-14). The pin is `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` (SKILL.md:810; note spot-checks at `:312`). So the block would run against bytes other than the measured ones. [INFERENCE: the kill counts would then differ. This is not measured here.]
3. The block calls the live-lane tool path (`bash tameshi-shokunin/tools/mutate-and-run.sh`) with no recorded tool revision. The note records that the tool moved mid-round, from `597e1419…` to `b56c6e57…`, and that reproduction under the current tool is unmeasured (note §7, U3).

**W2. The survivor-probe item is not met for D3 and D8 (`:103-115`).** The item requires "an input outside the suite's fixtures". Rows P3 (`:110`) and P8 (`:113`) run on "clean fixture". Note §9 (`:274-275`) identifies that fixture as the suite's own clean fixture, byte-identical to the sweep-side build. The note's own sentence at `:104` says each probe "constructs an input the suite's fixtures do not". That sentence is false for those two rows. Rows P5 (`:111`), P7 (`:112`), P9 (`:114`) and PR1 (`:115`) change the environment (a PATH shadow), add a source line, or change timing. They are outside the fixture but are not fixture inputs.

## Minor gaps

- **M1. Exact edit site is not a tool field.** `defects.tsv` column 2 is the line of the `@defect` directive in the spec, not the target line. Observed: F1 gives 1 and F2 gives 4 (Read10-11; py helper `cmd_list`). The operator must derive the target site. The note records its own `:1088`-style sites in sections 1 and 9; the tool does not emit them.
- **M2. Suite command is not printed.** No `MUTATE_*` line prints the `--suite` string (printf sites `:495-574`; Read10-2, Read10-5). It is recorded only from the invocation (note §0 and §9).
- **M3. Line count is not a tool pin.** `MUTATE_TARGET` (`:497`) prints sha256 and bytes only. The line count is lane-supplied under the opt-in contract (SKILL.md:808-812).
- **M4. Clause map is partly lane-supplied.** `MUTATE_SPEC` (`:506`) prints the spec path and the defect count. The clause text lives in each description (`defects.tsv` column 3). The mapping itself comes from contract item 3 (SKILL.md:818-822).
- **M5. Two report items have no protocol step.** Survivor probes and the recommendation are not among the six numbered protocol steps (SKILL.md:838-852). The probe script `probe/probes.sh` (note `:105`, `:273`, `:289`) is scratch-only. The section should name the operator step that produces these two items.

## Smallest safe correction (not applied; I edited nothing)

1. In `corpus/knowledge/mutation-case-mado-verify.md`: put the ten exact `@old`/`@new` pairs in a tracked file with no ellipses. Pin the target sha256 `d7edaab4…d0e13` in the block and state that the block is scratch-only. Otherwise remove the word "rebuilds" from `:262-293`.
2. Either build the D3 and D8 probes on an input outside the suite's fixtures, or change `:104` to name P3 and P8 as runs on the suite's own fixture.
3. In SKILL.md `:883-898`, add that the line count is lane-supplied (`:808-812`), that the suite string comes from the invocation, that the edit site is derived by the operator, and that probes and recommendations are operator steps outside the protocol (`:838-852`). Then re-read this bucket at the new revision.

## Limits and disclosures

- **Not run.** `--regression` (the round-26 pilot measured about 4 min 54 s under strace) and a full sweep of the mado target. The spec is absent and the target has drifted, so a sweep would not test the section. The section does not name `--selftest`, so I did not run it.
- **Outside the collector.** The clone build: git clone from the lane, checkout, sibling symlinks, and a sha256 of the clone's SKILL.md. SKILL.md is never a traced input. Listing of the live `coldread/traces` and `waves/round-27/w1` directories (plain `ls`, no content read).
- **Receipt check.** After tracing ended, I loaded all sixteen receipts in the live traces directory and checked schema, rev, exit, inputs, external keys and `live_lane_reads` (empty in all sixteen). The first form of receipt 15 also called `git status`, which read unrelated tracked files into its inputs. I reran it to the same path with a blob-only command, so the final receipt 15 is the only copy.
- **Not opened.** `SCORECARD.md`, `LOG.md`, `.ufo/evidence/round-21/coldread/ledger.json`.
- **Tooling.** No tool installed or upgraded. Record: none.
- **Scratch.** `/tmp/Read10-rfje` (clone, fixture and work directories). No lane file written except the sixteen receipts and this report.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read10", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 883, "heading": "### The report shape \u2014 what the opting-in lane receives", "class": "record", "verdict": "wrong-expectation",
  "blocking_gaps": [],
  "wrong_expectations": [
   "W1: the reproduce block (note :262-293; command block :281-293; ten-edit block :298-310) does not rebuild the sweep from the lane. (a) Its --defects path /tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec (:286) is absent on this host (Read10-9). The tool refuses it with MUTATE: SETUP (spec is not a regular file) (Read10-13). The spec is not embedded, and five of its ten rows are elided (:299 D1, :301 D3, :304 D6, :305 D7, :308 R1). (b) Its target is the live working-tree mado-shokunin/tools/mado-verify.sh, sha256 050efc72...03f1 (Read10-14), not the pin d7edaab4...d0e13 (SKILL.md:810; note :312). (c) It runs the live-lane tool path with no recorded tool revision; the note says the tool moved mid-round and that reproduction under the current tool is unmeasured (note section 7, U3).",
   "W2: the survivor-probe item is not met for D3 and D8. Rows P3 (note :110) and P8 (note :113) run on 'clean fixture', which note section 9 (:274-275) identifies as the suite's own clean fixture, byte-identical to the sweep-side build. The item requires an input outside the suite's fixtures. The note's sentence at :104 says each probe constructs an input the suite's fixtures do not, which is false for those two rows. Rows P5 (:111), P7 (:112), P9 (:114) and PR1 (:115) change the environment, add a source line, or change timing; they are outside the fixture but are not fixture inputs."
  ],
  "minor_gaps": [
   "M1: exact edit site is not a tool field. defects.tsv column 2 is the line of the @defect directive in the spec (py helper cmd_list; observed F1 to 1 and F2 to 4 in Read10-11), not the target line. The operator must derive the target site; the note records its own :1088-style sites in sections 1 and 9, and the tool does not emit them.",
   "M2: suite command is not printed by any MUTATE_* line (printf sites :495-574; Read10-2, Read10-5). It is recorded only from the invocation (note sections 0 and 9).",
   "M3: line count is not a tool pin. MUTATE_TARGET (:497) prints sha256 and bytes only (observed bytes=198, Read10-6). The line count is lane-supplied under the opt-in contract (SKILL.md:808-812).",
   "M4: clause map is partly lane-supplied. MUTATE_SPEC (:506) prints the spec path and defect count; the clause text lives in each description (defects.tsv column 3). The mapping comes from contract item 3 (SKILL.md:818-822).",
   "M5: survivor probes and the recommendation are not among the six numbered protocol steps (SKILL.md:838-852). The cited probe script probe/probes.sh (note :105, :273, :289) is scratch-only. The section should name the operator step that produces these two items."
  ],
  "commands_executed": [
   "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-mado-verify.md",
   "grep -n -E \"MUTATE_TOOL|MUTATE_DATE|MUTATE_TARGET|MUTATE_SPEC|CONTROL:|DEFECT |MUTATE_EVIDENCE|results\\.tsv|defects\\.tsv|spec\\.copy|MUTATE: DONE|MUTATE_RESTORE|pristine-sha256|sha256sum\" tools/mutate-and-run.sh",
   "bash tools/mutate-and-run.sh --help",
   "grep -n -E '^#{1,3} |only fleet|^\\| (probe|P3|P5|P7|P8|P9|PR1) |^```|Spot-checks|Scratch root|spec/mado|Reproduce|Shared class|By clause|survived|Survived' corpus/knowledge/mutation-case-mado-verify.md",
   "sed -n 440,580p tools/mutate-and-run.sh",
   "bash tools/mutate-and-run.sh --target /tmp/Read10-rfje/scratch/fixture.sh --defects /tmp/Read10-rfje/scratch/fixture.defects --suite 'bash \"$MUTANT\"' --workdir /tmp/Read10-rfje/scratch/work-fixture --label read10-fixture",
   "grep -n -E 'status|porcelain|worktree|working tree|tree-clean|rev-parse' tools/mutate-and-run.sh",
   "sha256sum tools/mutate-and-run.sh tools/trace-inputs.py corpus/knowledge/mutation-case-mado-verify.md",
   "ls -la /tmp/w6-tameshi-mado-verify /tmp/w6-tameshi-mado-verify/spec",
   "sed -n 300,440p tools/mutate-and-run.sh",
   "bash -c 'cd /tmp/Read10-rfje/scratch/work-fixture && echo \"--- defects.tsv\" && cat defects.tsv && echo \"--- results.tsv\" && cat results.tsv && echo \"--- evidence/F1.out\" && cat evidence/F1.out && echo \"--- ls workdir\" && ls -la'",
   "sha256sum .ufo/waves/round-26/w1/ColdreadPilot.md",
   "bash tools/mutate-and-run.sh --target /tmp/Read10-rfje/scratch/fixture.sh --defects /tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/Read10-rfje/scratch/work-w1 --label mado-verify.sh --tail 14",
   "sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh",
   "bash -c 'for p in tools/mutate-and-run.sh tools/trace-inputs.py corpus/knowledge/mutation-case-mado-verify.md .ufo/waves/round-26/w1/ColdreadPilot.md; do echo \"$p blob=$(git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:$p | sha256sum | cut -d\" \" -f1)\"; done; echo \"HEAD=$(git rev-parse HEAD)\"'",
   "grep -n -E 'fixture-A|defects[.]spec|D1 +:|D3 +:|D6 +:|D7 +:|R1 +:|probes[.]sh' corpus/knowledge/mutation-case-mado-verify.md"
  ],
  "opened": ["SKILL.md", "tools/trace-inputs.py", "tools/mutate-and-run.sh", ".ufo/waves/round-26/w1/ColdreadPilot.md", "corpus/knowledge/mutation-case-mado-verify.md"],
  "inputs": {
   "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
   "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
   "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
   ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7"
  },
  "external_inputs": {
   "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1"
  },
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-2.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-4.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-5.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-6.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-7.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-8.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-9.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-10.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-11.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-12.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-13.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-14.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-15.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read10-16.json"
  ]
 }]}
```

## Plain-English note: what I checked

I built a clone at the pinned revision and read the section (lines 883-898) and its neighbours. I classed it as a record. I opened the cited mado case note and the tool's emit sites, all under the trace collector. I then ran the tool on a scratch fixture to see its real output. I also ran the reproduce block's own spec path and checked the live mado target's sha256 against the pin. Each check has a receipt. The tool claims all hold: the tool and target pins, the control line, the per-defect rows and evidence, and the restore line with no tree-clean check. The note claims hold too, apart from the two defects in W1 and W2. The reproduce block cannot run from the lane. Two survivor rows use the suite's own fixture. Those two findings are why this bucket is not credited.

COLDREAD Read10: wrong-expectation
