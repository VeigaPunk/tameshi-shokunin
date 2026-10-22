# Read12 cold read: SKILL.md `### Using the ledger` (line 933) at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647

Verdict: gap-minor (class: instruction). The one named command runs as written, and every behavior the section states was either observed in a run or read in the code. Three cited line anchors point at the wrong lines, and one contract phrase is not enforced by the tool.

## Evidence

Section bounds. The section runs from line 933 to line 964. Line 965 is the next heading, `### Reading a receipt — the discipline`. The section holds no fence. Its first bullet tells a reader to run `bash tools/mutate-and-run.sh --regression`, so the class is instruction.

Named command, traced (Read12-1; receipt exit 0; wall time 272.95 s, under the six-minute cap): `bash tools/mutate-and-run.sh --regression`. Observed: `REGRESSION_TOOL: ... sha256=fb91ef76...`, which matches the bytes of the lane file; nine `REGRESSION_CASE ... PASS` lines; each `REGRESSION_TABLE ... flips=0`; `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`; `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.ACxKlP (removed on PASS; --keep retains)`. The follow-up `ls -d` of that path exits 2 (Read12-6), so the root is gone.

Refusal path, traced (Read12-8; receipt exit 2; wall time 214.59 s). I removed the `mado-shokunin` link from my scratch mirror, then ran the same command under the collector. Observed: `REGRESSION_CASE bash-mado-verify: SETUP (repo_identity_mismatch: /tmp/Read12-2yJh/fleet/mado-shokunin is not its own repository; toplevel=unresolved)`. That leg printed no `REGRESSION_PIN` and no `REGRESSION_SWEEP` line. The three legs before it and the five after it printed PASS. Aggregate: `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)`, `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.e8z40f (kept)`. The `ls -d` of that path succeeds (Read12-11). This confirms refusal before the suite, later legs still running, statuses aggregating, and the root kept on SETUP.

Pinned blobs. Read12-4 ran a read-only helper. It ran `git show <rev>:<path>` in each sibling object store and hashed the bytes. All nine match the pin the tool records. Sample: `kumitate-shokunin@175de6ba...:scripts/kimi-census.mjs sha256=83016d45... match=yes`.

Anchors and code, at 2227d83.
- Read12-3 (traced grep): `git_clean -C "$repo" show` at :1202; `REGRESSION_PIN` printf at :1228 and :1231; `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` at :1358; `REGRESSION_TOOL` at :1368; exit statements at :1443 (exit 1), :1449 (exit 2), :1459 (exit 0).
- Read by hand: mode mirror :1211-1226; SHA compare :1238-1243; prerequisite checks :1349-1353 before the mktemp at :1358; `KEEP=0` at :188; `--workdir` at :1999 and `--keep` at :2003; removal test at :1453 (`auto -eq 1 && KEEP -eq 0`). The spec parser refuses an empty `@old` and an `@new` equal to `@old` at :399-401, and the apply step asserts count == 1 at :421-424. Both match the contract clauses.
- Spec anchors: pins, revisions and tables :603-629 (correct); the first four spec heredocs open at :659, :700, :745 and :790, and the fifth opens at :840, so :657-839 (correct); inventory :83-108 (correct); nine dispatches :1384-1428 (correct).
- History: Read12-9 shows `948:  local nlegs=4` at 9f1d3c3, so "N=4 at r7-1" matches.
- Contract wording: Read12-5 shows only the sweep summary `MUTATE: DONE (target=%s defects=%s killed=%s survived=%s inconclusive=%s kill-rate=%s%%)` at :574. It has no enumerated, executed or skipped counts.

Hashes and tree state. Read12-2: `tools/mutate-and-run.sh` fb91ef76..., `tools/trace-inputs.py` f59c9312.... Read12-7: `git status --porcelain` empty after both runs. `.gitignore` is listed as an input because git status read it. Every receipt I read shows rev 2227d8338c02... and empty `live_lane_reads`.

## Smallest safe correction
1. Replace `tools/mutate-and-run.sh:1104-1175` with `:1151-1156` (the materialization description) and `:1202-1243` (git show, mode and SHA checks).
2. Replace `(:1159-1160)` after `REGRESSION_PIN` with `(:1228-1231)`.
3. Replace the exit anchor with `:126-136` (exit map) plus the exit statements `:1443`, `:1449` and `:1459`.
4. Label "enumerated, executed and skipped counts distinguished" as a contributor requirement that no check enforces.
5. Change `Exits0/1/2` to `Exits 0/1/2`.

## Verification gaps and residual risk
- Read, not executed: `--keep` (:1453-1458), `--workdir DIR` (:1357-1362), pre-allocation SETUP (:1349-1358) and FAIL exit 1 (:1443).
- Read, not executed: the rev-missing, blob-missing and pin-mismatch refusals (:1188-1243). Only the missing-repo refusal ran.
- Not checked: the historical counts "7 since round 16" and "8 since round 18" (the section gives no pinned commit for them); "the old tsukuroi/mado pins are historical" (the legs ran at their pinned revisions, and current trees were not compared); and the policy sentences on host-gated branches and the (U) caveat, which no run can exercise.
- "Working-tree drift does not change that blob" rests on `git show <rev>:<path>` at :1197-1202. I made no drifted-tree run, because the sibling repositories are read-only.
- Observation outside section scope: a missing directory is reported under the label `repo_identity_mismatch`. The section's claim still holds.

## Disclosure and setup (not evidence)
- One refusal-path attempt ran without the collector. That was my error: `sh -c 'unlink .../mado-shokunin && bash tools/mutate-and-run.sh --regression'`. It printed the same SETUP result and kept root `/tmp/tameshi-r4-2-regression.DPojUj`, which Read12-10 checks. I did not use the untraced run as evidence; Read12-8 is the traced rerun.
- Untraced setup and probes: the detached mirror (`mktemp`, symlinks, `git clone` from the lane with `GIT_OPTIONAL_LOCKS=0`, detached checkout at 2227d83); the SKILL.md hash `386de44b...`; `command -v`, `strace -V`, `node --version` and `git --version`; an early untraced `git status` and `git rev-parse`; `ls -la` on the lane receipt and wave directories (names only, outside traces).
- Installs and updates: none. Already present: strace 7.2 (`/usr/bin/strace`), node v24.21.0 (fnm) and git 2.56.0. No install channel was used, so RULES.md was not needed.
- Scratch left in /tmp: `/tmp/Read12-2yJh` (clone, mirror, `blobs.sh`, `section.json`) and the kept roots `DPojUj` and `e8z40f`. The only lane writes are the receipts and this report.
- Read12-12 validates the JSON below in scratch before this report was written.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read12", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 933, "heading": "### Using the ledger", "class": "instruction", "verdict": "gap-minor",
  "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
   "Anchor tools/mutate-and-run.sh:1104-1175 for the git-show materialization and its mode and SHA checks misses the code: git show is at :1202, the mode mirror at :1211-1226, the SHA compare at :1238-1243. The range holds spec text, the end of regression_specs and the preamble of regression_case; the materialization is only described there (comment at :1151-1156).",
   "Anchor (:1159-1160) for REGRESSION_PIN points at a tolerance comment. The REGRESSION_PIN prints are at :1228-1231.",
   "Exit anchor tools/mutate-and-run.sh:126-136,1273-1294,1364-1384: :126-136 is the correct exit-map comment, but the exit statements are at :1443 (exit 1), :1449 (exit 2) and :1459 (exit 0). :1273-1294 is the per-defect verdict comparison and :1364-1384 is header output plus the first dispatch.",
   "The contract phrase enumerated, executed and skipped counts distinguished is not mechanized: the sweep summary at :574 prints defects, killed, survived, inconclusive and kill-rate only, and no check requires the other counts. It should be labelled a contributor requirement.",
   "Typo: Exits0/1/2 should read Exits 0/1/2."
  ],
  "commands_executed": [
   "bash tools/mutate-and-run.sh --regression",
   "sha256sum tools/mutate-and-run.sh tools/trace-inputs.py",
   "grep -n -E 'REGRESSION_PIN |git_clean -C \"[$]repo\" show|^ *exit [012]$|mktemp -d /tmp/tameshi-r4-2-regression|REGRESSION_TOOL:' tools/mutate-and-run.sh",
   "bash /tmp/Read12-2yJh/blobs.sh",
   "grep -n -i -E 'enumerat|executed|skipped|MUTATE: ' tools/mutate-and-run.sh",
   "ls -d /tmp/tameshi-r4-2-regression.ACxKlP",
   "git status --porcelain",
   "sh -c 'test ! -e /tmp/Read12-2yJh/fleet/mado-shokunin && bash tools/mutate-and-run.sh --regression'",
   "sh -c 'git show 9f1d3c3:tools/mutate-and-run.sh | grep -n -E \"^(nlegs|local nlegs|  local nlegs)|nlegs=\" ; git cat-file -t 9f1d3c3'",
   "ls -d /tmp/tameshi-r4-2-regression.DPojUj",
   "ls -d /tmp/tameshi-r4-2-regression.e8z40f",
   "python3 -c \"import json; d=json.load(open('/tmp/Read12-2yJh/section.json')); print(sorted(d['sections'][0].keys())); print(len(d['sections'][0]['commands_executed']), len(d['sections'][0]['traces']), len(d['sections'][0]['external_inputs']))\""
  ],
  "opened": ["tools/mutate-and-run.sh", "tools/trace-inputs.py", ".gitignore"],
  "inputs": {"tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4", ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116"},
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
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-2.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-4.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-5.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-6.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-7.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-8.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-9.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-10.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-11.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read12-12.json"
  ]
 }]}
```

## What I checked (plain English)
I read the section from my detached clone and classed it as an instruction. I ran its one named command under the collector twice: once on the intact mirror (PASS, nine of nine legs), and once with one leg's repository removed from my scratch mirror (SETUP, eight of nine, with the refused leg not run). I confirmed that the scratch root is removed after a PASS and kept after a SETUP. I re-hashed the nine pinned blobs from the sibling object stores. I checked each cited line anchor by grep and by reading the code, checked the historical leg count at 9f1d3c3, and confirmed that the clone was clean after the runs. Every behavior the section states matches either what I observed or what the code does. Three of its line pointers and one contract phrase do not match, so the verdict is gap-minor, not executed-ok.

COLDREAD Read12: gap-minor
