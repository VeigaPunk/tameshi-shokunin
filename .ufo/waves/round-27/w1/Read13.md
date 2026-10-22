# Read13: cold read of "### Reading a receipt — the discipline"

Verdict: gap-minor (class: instruction). Section is SKILL.md:965-1009 at rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. Page sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 matches the assignment.

No blocking gap and no wrong expectation. The command runs and the rules hold at head. The gaps are one stale count, one truncated sample line, one dead scratch pointer, and three wording items.

## Setup

- Clone: /tmp/Read13-g2ia/fleet/tameshi-shokunin, detached at 2227d83, `git status --porcelain` empty. Sibling repos are symlinks under /tmp/Read13-g2ia/fleet.
- Section bounds: heading at line 965. The next heading, "## The re-sweep cadence and the six-case confidence statement (round 8, measured)", is at line 1010. The section is therefore 965-1009 and has no fenced code.
- Class: instruction. Items 1-6 tell a reader how to read a regression receipt and what to do on PASS, FAIL or SETUP. Item 7 names a command and the output it should give. The measured figures in items 2, 3 and 7 are checked as record claims.

## Collector runs (receipts Read13-1 to Read13-10)

Each run was made from inside the clone as `python3 tools/trace-inputs.py --root /tmp/Read13-g2ia/fleet/tameshi-shokunin --out <traces>/Read13-N.json -- <argv>`. All ten receipts show rev 2227d83, exit 0, no untracked opens and no live-lane reads.

- Read13-1, `bash tools/mutate-and-run.sh --selftest`: 6.58 s. Final lines `MUTATE_SELFTEST: 97/97 pass` and `VERDICT: PASS`. Exit 0.
- Read13-4, `bash tools/mutate-and-run.sh --regression`: 267.79 s, under the six-minute cap. Closing line `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`, then `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.e4yjSP (removed on PASS; --keep retains)`. Exit 0. The block has nine REGRESSION_PIN, nine REGRESSION_SWEEP, nine REGRESSION_TABLE and nine REGRESSION_CASE lines, and no REGRESSION_DEFECT lines. Tables read match=10/10 on eight legs and match=15/15 on bash-checklist-run, all with flips=0. The REGRESSION_EXPECT figures (8/10, 8/10, 6/10, 4/10, 7/15, 7/10, 5/10, 5/10, 5/10) equal the measured kill counts on every leg.
- Read13-2, Read13-5, Read13-6, Read13-7, Read13-10: reader runs over plans/round-7.plan.md lines 1-20, tools/mutate-and-run.sh lines 120-166, 1160-1372 and 1420-1460, and corpus/knowledge/fleet-kill-rate-ledger.md lines 1-60.
- Read13-3, Read13-9: grep runs over tools/mutate-and-run.sh for the output tokens and the call sites.
- Read13-8: sha256 of the four lane files opened by path.

## Claim checks

Verified:

(a) Steps 1-3 tokens. Every REGRESSION_ token in the section is printed by tools/mutate-and-run.sh: PIN at 1228-1231, SWEEP at 1250-1251, DEFECT at 1283-1297, TABLE and WORKDIR at 1318-1320, CASE at 1322-1327, TOOL, DATE, BAND and EXPECT at 1368-1372, and the closing verdict at 1440-1459. All of them appear in Read13-4.

(b) Step 2 PASS form. Line 1322 prints `REGRESSION_CASE <leg>: PASS (band: killed-delta<=<ktol> flips<=<ftol> inconclusive=0 defects=<D>)`, and all nine legs print it with 0 0 tolerance (ledger legs are called with 0 0 at lines 1339-1340). D is 10 on eight legs and 15 on bash-checklist-run, as the section says. The selftest fixture row `bash-checklist-run ... 15:7` at line 1951 agrees. N=9 matches the closing line, the selftest's "nine files written" and "calls=9 specs=9 nlegs=9" (Read13-1), and the header at lines 161-162 (r18 to eight, r26 to nine). The closing count is hard-coded as nlegs=9 at line 1430.

(c) Step 3 FAIL form. The DEFECT rows (1283, 1286, 1297) and the TABLE row (1318) match the section. ABSENT on either side counts (1283 and 1297). The selftest's doctored-table cases pass at head: `regression engine fails a doctored table`, `doctored table names K/S`, `out-of-band FAIL names flips=2` (Read13-1).

(d) Step 4 SETUP. Each of these returns 2 and never a pass: missing repo as repo_identity_mismatch (1189-1191), revision not found (1194-1196), path not in revision (1198-1200), git show failure (1203-1206), missing target (1235-1236), pin mismatch (1240-1243), refused sub-sweep (1253-1254). The closing logic at 1439-1459 prints FAIL with exit 1 if any case fails, then SETUP with exit 2 if any case cannot verify, and PASS with exit 0 only when neither occurred. A SETUP can never print PASS.

(e) Step 5 ledger. fleet-kill-rate-ledger.md lines 13-14 say every rated cell is tied to the pin it was swept at and that a rate is never implied to hold at a later revision. Lines 26-30 say composition is stated beside every rate. The four §1 rates at lines 45-48 (8/10, 8/10, 6/10, 4/10) equal the first four REGRESSION_EXPECT figures and the measured tables.

(f) Step 7 arms. Every arm the step names appears in Read13-1: git-materialized replay at exact tolerance, drifted working tree not moving a git-pinned leg, pin mismatch and unresolvable revision as SETUP (exit 2), and one flipped entry failing loudly.

(g) Step 7 tolerance sentence. BAND_KILLED=1 and BAND_FLIPS=1 at lines 186-187. The callers that take these defaults are all fixture cases inside the selftest (lines 1618-1915, Read13-9). The one non-fixture caller passes 0 0 (line 1340). "Exercised by the selftest only" holds.

Minor gaps:

1. Step 7 count. The line `MUTATE_SELFTEST: 67/67 pass` is pinned to rev cf41efaa. At 2227d83 the same command prints `MUTATE_SELFTEST: 97/97 pass`, `VERDICT: PASS`, exit 0 (Read13-1). The verdict and exit code reproduce and every named arm is present, but the printed number is out of date at head, and the step does not say that the count grows as arms are added.
2. Step 3 sample line. tools/mutate-and-run.sh:1326 prints `REGRESSION_CASE <leg>: FAIL (out of band:<reasons>; log: <dir>/sweep.log)`. The section quotes the line and stops after `flips=1`, without the `; log:` tail.
3. Step 3 pointer. `/tmp/w7-tameshi-1/flip-run.out` does not exist on this host (`ls` reports no such file). The round-7 js-kimi-census doctored run was not re-run. At head the same FAIL path is exercised only through the selftest fixture (Read13-1). The sample arithmetic (match=9/10, flips=1, killed-delta=1) follows the engine at lines 1308-1319.
4. Step 6 citation. plans/round-7.plan.md:11-15 says attestation is read-only, reproduced from pins or the missing piece named, and that tameshi attests. It does not say that the sibling's note is never edited. That phrase is the section's own gloss.
5. Step 2 historical instance. The T7-1 instance (rev cf41efaa, four legs, cases=4 passed=4, exit 0) is not reproduced. A receipt at another revision cannot be credited here, so that revision was not checked out. At 2227d83 the same command reports nine legs (Read13-4), which agrees with the section's own rule N=9 since round 26.
6. Step 1 block shape. REGRESSION_WORKDIR prints once per leg (`REGRESSION_WORKDIR <leg>: <dir>`) and once at the end. The root line (1442, 1448, 1454, 1457) follows the verdict line in all three outcomes, so the verdict line is not the last line of the block. The section lists WORKDIR once, before the verdict line.

Blocking gaps: none.
Wrong expectations: none. The 67/67 figure is scoped to cf41efaa in the text. I rate it stale, not wrong, because the verdict, the exit code and every named arm reproduce at head.

## Smallest safe correction (not applied; I edit nothing)

- Step 7: write the count with its revision, for example "67/67 at cf41efaa; 97/97 at 2227d83", or state the rule as "VERDICT: PASS, exit 0; the count grows as arms are added."
- Step 3: add "; log: <dir>/sweep.log" to the sample line. Replace the /tmp/w7 pointer with "round-7 negative run (scratch since removed)".
- Step 6: drop "the sibling's note is never edited", or cite a line that states it.
- Step 1: say that WORKDIR prints per leg and again at the end, after the verdict line.

## Outside the collector

These ran outside the collector. None supplies evidence I rely on, and every fact above comes from a traced command or its output.

- The clone (prescribed by step 1). It read the live repo's git object store, as the step specifies.
- `git rev-parse HEAD` and `git status --porcelain` in the clone.
- `ls` of plans/, corpus/knowledge/, the traces and report directories (metadata only), and `ls -ld /tmp/w7-tameshi-1`.
- `python3 --version`, `ls -la tools/`, `python3 tools/trace-inputs.py --help`.
- `sha256sum tools/mutate-and-run.sh`, which gave fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de, the same as Read13-8.
- SKILL.md was read with the read and grep tools. SKILL.md is excluded from inputs by rule. tools/trace-inputs.py was read by hand and is listed in inputs.
- After the report was written, one Python check (outside the collector) read only this report file, parsed its single json block, and confirmed the block loads and that its traces and opened files match. It read no evidence.

## Tooling

No tools installed or updated. The collector ran on the host as installed. Pacman was not used.

## Residual risk and verification gaps

- The cf41efaa replay (step 2 instance and step 7 count) was not reproduced.
- The round-7 doctored negative run was not reproduced. No doctored copy of a ledger leg could be run under the collector without editing the clone, which would have broken the receipt hashes.
- The external_inputs entries are the nine sibling blobs that the regression replay materialized with git show. Their sha256 values are the pins that the tool checked against the materialized bytes (no SETUP was raised), not an independent sha256sum of git show output.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read13", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 965, "heading": "### Reading a receipt \u2014 the discipline", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": [
  "Step 7 count is pinned to rev cf41efaa (67/67). At 2227d83 the same command prints MUTATE_SELFTEST: 97/97 pass and VERDICT: PASS, exit 0 (Read13-1). Verdict and exit reproduce and every named arm is present; the printed number is out of date at head and the step does not say the count grows as arms are added.",
  "Step 3 sample FAIL line omits the tail. tools/mutate-and-run.sh:1326 prints REGRESSION_CASE <leg>: FAIL (out of band:<reasons>; log: <dir>/sweep.log); the section stops after flips=1.",
  "Step 3 pointer /tmp/w7-tameshi-1/flip-run.out does not exist on this host. The round-7 js-kimi-census doctored run was not re-run; the FAIL path is exercised at head only by the selftest fixture (Read13-1). The sample arithmetic (match=9/10, flips=1, killed-delta=1) matches the engine at lines 1308-1319.",
  "Step 6 cites plans/round-7.plan.md:11-15, which say attestation is read-only, reproduced from pins or the missing piece named, and that tameshi attests. They do not say the sibling's note is never edited; that phrase is the section's own gloss.",
  "Step 2 historical instance (T7-1, rev cf41efaa, four legs, cases=4 passed=4) is not reproduced because a receipt at another revision cannot be credited. At 2227d83 the same command reports nine legs (Read13-4), matching the section's N=9 since round 26 rule.",
  "Step 1 block shape: REGRESSION_WORKDIR prints once per leg and again at the end, after the verdict line (tools/mutate-and-run.sh:1442, 1448, 1454, 1457). The section lists WORKDIR once, before the verdict line."
 ],
 "commands_executed": [
  "bash tools/mutate-and-run.sh --selftest",
  "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(i+1, L[i]) for i in range(0,min(len(L),20))]\" plans/round-7.plan.md",
  "grep -n -E \"REGRESSION_|MUTATE_SELFTEST|checklist-run|cases=|SETUP|killed-delta\" tools/mutate-and-run.sh",
  "bash tools/mutate-and-run.sh --regression",
  "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(i+1, L[i]) for i in range(119,166) if i < len(L)]\" tools/mutate-and-run.sh",
  "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(i+1, L[i]) for i in range(1159,1372) if i < len(L)]\" tools/mutate-and-run.sh",
  "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(i+1, L[i]) for i in range(0,60) if i < len(L)]\" corpus/knowledge/fleet-kill-rate-ledger.md",
  "sha256sum tools/trace-inputs.py tools/mutate-and-run.sh plans/round-7.plan.md corpus/knowledge/fleet-kill-rate-ledger.md",
  "grep -n -E \"regression_case |BAND_KILLED=|BAND_FLIPS=|run_regression|--regression\\)|--selftest\\)\" tools/mutate-and-run.sh",
  "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(i+1, L[i]) for i in range(1419,1460) if i < len(L)]\" tools/mutate-and-run.sh"
 ],
 "opened": ["tools/mutate-and-run.sh", "plans/round-7.plan.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "tools/trace-inputs.py"],
 "inputs": {
  "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
  "plans/round-7.plan.md": "49cd55fd0efaf892c281ec90538310cd5691af2af4ab1270c9945146fdc0fcec",
  "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
  "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
 },
 "external_inputs": {
  "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
  "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
  "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
  "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
  "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
  "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
  "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9",
  "kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs": "6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f",
  "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"
 },
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-7.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-8.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-9.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read13-10.json"
 ]}]}
```

Note on what I checked. I read SKILL.md lines 965-1009 at 2227d83 and classed the section as instruction, because items 1-7 tell a reader how to read a regression receipt and item 7 names a command. I ran the selftest and the full nine-leg regression replay under the collector; both exited 0, and the replay closed with PASS (cases=9 passed=9). I then checked each token, each PASS, FAIL and SETUP rule, the tolerance default, and the ledger statements against the code, the output and the cited files. Everything matches except the stale 67/67 count, the truncated FAIL sample, the dead round-7 pointer, and the three wording items above. The monitor reason for this section was no-ledger-entry at this revision, so this receipt set is the coverage I add.

COLDREAD Read13: gap-minor
