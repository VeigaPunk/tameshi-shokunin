# RevengerTraceBytes — round-36 trace-receipt reverse-engineering (w1)

Seat: revenger (leaf, read-only). No subagents. No tools installed (none needed; pacman untouched per host pause). No production files edited; only this report written.

## What I attacked

The four round-36 cold-read refresh trace receipts at
`.ufo/evidence/round-36/coldread/traces/L1/source-{1,2,3,4}.json`:
(a) schema `tameshi-trace-inputs-v1`; (b) every trace input sha256 equals
`git show <rev>:<path> | sha256sum` at the refresh commit; (c) the traced argv
actually reads the cited paths.

## Reconstructed chain

- All four traces record `rev = e423c41ba253357ab8c8513f0376dad9d38ab248`
  (round-36 content commit, 2026-10-24 03:14:00 -03:00; parent
  `796e08b8…` = the C1 before-rev). The refresh commit that committed the
  traces/ledger is its child `b455001e2589b3f4f471d94a3de7e5e549b9f54c`
  (03:16:09, matching the receipts' measurement_interval). `e423c41b` is an
  ancestor of `b455001e`, and `git diff e423c41b HEAD` over all nine input
  paths is EMPTY — so (b) holds at the recorded rev, at the refresh commit,
  and at HEAD identically.
- The traced runs executed in a temp checkout
  `/tmp/tameshi-r36-refresh-08zapax9/lane` (now gone). The instrument's
  `live_lane_reads: {}` and `external: {}` in every trace prove the temp lane
  did not read the live lane or anything outside it; `dropped_home_count: 0`.
- Instrument identity: `instrument_sha256 = f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4`
  in all receipts == sha256 of `tools/trace-inputs.py` @ `e423c41b`
  (recomputed; exact match). That instrument is a strace-based syscall
  observer: `inputs` holds successful opens of regular files, write-flag
  opens excluded (`O_WRONLY|O_RDWR|…`), realpath-resolved, `.git` excluded,
  filtered to files tracked at the recorded HEAD (`git ls-files --cached`),
  hashed from actual bytes — i.e. the `inputs` maps are OBSERVED reads, not
  declared lists. Rev `e423c41b` was captured independently by the instrument
  from the temp repo at trace time.
- (c) argv semantics: the traced command is `python3 -B -c <script> ROOT
  START END PATHS`. The script reads exactly `ROOT/SKILL.md` (slicing lines
  START..END from `splitlines(keepends=True)`) plus `ROOT/<rel>` for each rel
  in the JSON PATHS list — no other file reads exist in the code. Verified
  `set(inputs) == {"SKILL.md"} ∪ set(PATHS)` for all four traces (9 / 3 / 4 /
  2 entries) — the observed syscall surface equals the argv's implied read
  set exactly: no more, no less.
- Byte-exact stdout replay (the decisive (c) proof): reconstructing stdout
  from rev content — `b''.join(SKILL.md_lines[START-1:END])` +
  `"\nSOURCE-READS: …"` line + per-path `SOURCE <rel> bytes=<n>
  sha256=<h>` lines with hashes of `git show e423c41b:<rel>` — reproduces the
  receipts' `stdout_sha256` exactly for all four traces (see table). Combined
  with `exit: 0` in trace and receipt, the recorded output demonstrably came
  from reading exactly those paths at that rev.
- Cross-consistency: receipts' argv[6:] == trace argv element-wise; receipts'
  `--out` == the actual trace file paths; `section_start` == argv START ==
  ledger entry `start` == `affected-sections.json` start (131 / 375 / 1380 /
  1436). The four appended `round-21/coldread/ledger.json` entries
  (`read_rev e423c41b`) have `inputs` identical to the trace `inputs`, point
  at the right trace files, and their `sha256`/`skill_sha256` ==
  sha256(section slice with trailing newline stripped) — recomputed, all four
  match. All argv line ranges are within SKILL.md's 2136 lines at the rev,
  and each range's first line is exactly the corresponding affected-sections
  heading (`## Mutation-sweep recipe…`, `## Restore discipline…`,
  `### The map…`, `### Where to enter…`).
- Ledger/receipts/traces/ledger-instrument files all clean vs HEAD
  (`git status --porcelain` empty over the evidence paths).

## Per-trace verdicts

| trace | section (SKILL.md lines) | inputs | (a) schema | (b) hashes vs `git show e423c41b:path` | (c) argv reads cited paths (set-equality + stdout replay) | receipt stdout replay | verdict |
|---|---|---|---|---|---|---|---|
| source-1.json | 131–245 Mutation-sweep recipe | 9 | PASS | 9/9 match | PASS | b17c30eaf87d98f436787829ff8ae9f61ad5f340b7e0db2fae179d09093f747c | **PASS** |
| source-2.json | 375–404 Restore discipline | 3 | PASS | 3/3 match | PASS | 913f4064893dd21cb043759e3a5e0965f0c82580007feeeff875052fa9379819 | **PASS** |
| source-3.json | 1380–1395 The map | 4 | PASS | 4/4 match | PASS | b56fa1120492023021a43fdf09c3be0ec39ec74c6a35cf319e26a2468c4e3dbf | **PASS** |
| source-4.json | 1436–1448 Where to enter | 2 | PASS | 2/2 match | PASS | 05c7ce3f856b080f8bae6447caf7cbed5ce25cb1a144e2ed163189de8432af35 | **PASS** |

All nine unique input paths verified at `e423c41b`, including
`tools/mutate-and-run.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
(matches the round-36 frozen byte-pin).

## Commands run (revisions in place)

- `git cat-file -t` / `git log -1 --format='%H %P %ci %s'` / `git log -3` @ `e423c41b…`
- `for p in <9 paths>: git show e423c41b…:$p | sha256sum` — all nine
- `git ls-tree -r e423c41b… -- <9 paths>` (tracked) + `git show e423c41b…:SKILL.md | wc -l` → 2136
- `git log -1 -- <trace path>` → b455001e (refresh commit); `git diff --stat e423c41b… HEAD -- <9 paths>` → empty; `git merge-base --is-ancestor e423c41b… b455001e…` → true
- Python replay (scratch, no repo writes): per trace — schema assert, `set(inputs) == {SKILL.md} ∪ argv[7]`, sha256(`-c` script), byte-exact stdout reconstruction from `git show e423c41b…` blobs vs receipt `stdout_sha256`, receipt argv[6:]/--out/exit/instrument cross-check, ledger slice-hash + inputs + range + trace-pointer cross-check
- sha256(`tools/trace-inputs.py` @ e423c41b) → f59c9312… (== receipts' instrument_sha256)
- `git status --porcelain` over evidence paths → clean

## Notes / divergences

- None material. Three initial mismatches were my own modeling assumptions,
  each resolved in the evidence's favor: instrument hash is of the outer
  `trace-inputs.py` tool (not the inner `-c` script); receipts' `--out` is
  argv[4]; ledger `sha256` is the slice hash minus trailing newline.
- Residual caveat [INFERENCE-free]: syscall-level ground truth rests on the
  instrument's design + embedded selftest suite; I could not re-strace the
  runs because the temp checkout is gone. The byte-exact stdout replay from
  rev content independently pins the outputs to the cited inputs at that rev.
- Trace runs ran at the content commit `e423c41b` (parent of the refresh
  commit `b455001e` that committed the receipts), consistent with the C1
  kill_rule ordering: content first, refresh evidence second.

## Verdict

**VERDICT: PASS — all four round-36 trace receipts (source-1..4.json) are
internally consistent and rev-bound: schema `tameshi-trace-inputs-v1` ✓,
every input sha256 == `git show e423c41ba253357ab8c8513f0376dad9d38ab248:<path>`
(== refresh commit b455001e == HEAD) ✓, and the traced argv provably reads
exactly the cited paths (observed-read set == argv read set; byte-exact
stdout replay matches all four receipt stdout_sha256) ✓.**
