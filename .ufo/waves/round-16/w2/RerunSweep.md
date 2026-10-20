# RerunSweep — falsify C1's round-gate measured table (round 16, wave 2)

**Verdict: HOLDS.** Independent re-run of the 10-defect sweep reproduces the
recorded table exactly — 10/10 verdicts, 10/10 exits, 10/10 mutant sha256s,
identical failing-check sets and nested [51] tallies. No flips.

## Setup

- Scratch: `/tmp/tameshi-r16w2-RerunSweep-LMSfoe` (mktemp -d per contract).
- Worktree: `git -C tameshi-shokunin archive c699c8c36d6e4eca4b796b81a8247904aa145ec8 | tar -x`
  → `/tmp/tameshi-r16w2-RerunSweep-LMSfoe/worktree` (read-only checkout; no worktree mutation).
- Target materialized: `git -C kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs`
  → sha256 `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`,
  80,415 B, 1,511 lines — matches note §0 pin and sweep.log `MUTATE_TARGET`.
  Blob mode `100755` mirrored with `chmod 755` (kumitate `ls-tree` confirms 100755).
- Spec: `git show c699c8c…:.ufo/evidence/round-16/round-gate/round-gate.defects.spec`
  → sha256 `e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4`
  — matches note §1 (`e99b87eb…11c4`).
- Tool: `worktree/tools/mutate-and-run.sh` at c699c8c → sha256
  `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` (runner-sha256.txt
  receipt). **Observed delta:** the recorded 13:40:15Z sweep ran `75ed934d…adc5`
  (r10-2, pre-ledger-embedding); this re-run used the committed landing revision
  `89722ddb` (r16, leg 7 embedded). Note §2 records both shas; the tool's
  defect-application and suite-run path is unchanged between them.
- Host: node v24.21.0 (note §6 records v24.21.0), Linux 7.2.11.
- Repos untouched: `git --no-optional-locks status --porcelain` → 0 entries on
  kumitate-shokunin; 10 entries on tameshi-shokunin are pre-existing lane state
  (my sweep wrote only to /tmp).

## Command executed

```
bash worktree/tools/mutate-and-run.sh \
  --target $SCRATCH/round-gate.mjs \
  --defects $SCRATCH/round-gate.defects.spec \
  --label js-round-gate --workdir $SCRATCH/work \
  --suite 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest'
```

Suite string copied verbatim from `.ufo/evidence/round-16/round-gate/suite.txt`
(single line, byte-for-byte). Exit 0; wall ~36 s; sweep.log retained at
`/tmp/tameshi-r16w2-RerunSweep-LMSfoe/sweep.log`, full evidence under
`/tmp/tameshi-r16w2-RerunSweep-LMSfoe/work/`.

## Comparison — recorded vs re-run

Column diff of `results.tsv` (id, verdict, exit, mutant-sha256; duration-ms
excluded by design):

```
diff recorded-cols.txt rerun-cols.txt  →  IDENTICAL (no output)
```

| id | recorded | re-run | exit | mutant sha256 match | checks failed (excluding [51]) |
|---|---|---|---|---|---|
| A1 | KILLED | KILLED | 1 | `1186162e…` ✓ | [1] [2] [3] [12] [16] [21] [22] [27] [46] [47] — exactly the note's 10 |
| A3 | KILLED | KILLED | 1 | `05f2f411…` ✓ | [52] [53] — rt8 prefix stays green ✓ |
| B1 | KILLED | KILLED | 1 | `fc32499f…` ✓ | [32] [45] ✓ |
| E3 | KILLED | KILLED | 1 | `81cfe486…` ✓ | [54] ✓ |
| C1060 | KILLED | KILLED | 1 | `432b4d50…` ✓ | [8] ✓ |
| C1059 | SURVIVED | SURVIVED | 0 | `35791a36…` ✓ | 0 ✓ |
| A2 | SURVIVED | SURVIVED | 0 | `d6aa922c…` ✓ | 0 ✓ |
| B2 | SURVIVED | SURVIVED | 0 | `a8af2f4c…` ✓ | 0 ✓ |
| CKIND | SURVIVED | SURVIVED | 0 | `1e6d4deb…` ✓ | 0 ✓ |
| E1 | SURVIVED | SURVIVED | 0 | `7d56ab89…` ✓ | 0 ✓ |

Tail lines: `CONTROL: GREEN (exit=0 …pristine-sha256=f890e277…d3e9)`;
`MUTATE_RESTORE: OK (before=after=f890e277…d3e9)`;
`MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5
inconclusive=0 kill-rate=50%)` — identical to recorded sweep.log tail.

## Secondary claims re-checked

- **Nested [51] witness:** every kill also fails [51]; tallies observed:
  A1 `50/60`, A3 `58/60`, B1 `58/60`, E3 `59/60`, C1060 `59/60` — matches note §2
  parenthetical exactly.
- **A3 pin-width gradient:** mutant line `warnings=0 errors=0` observed in
  evidence/A3.out [52]/[53]/[59]; [59] rt8 (prefix regex) stays PASS — matches
  note §3.
- **B1 species asymmetry:** [32] fails on token `MAIN_REPO_NOT_GIT` at the
  main-path site while B2's tracked-site edit of the same token survives 60/60 —
  matches note §3.
- **C1060 edge kill:** evidence/C1060.out [8] shows the 1059-byte r8 report
  reclassified — `kinds=[REPORT_THIN,REPORT_ROUND_MISMATCH]` — matching note §3's
  interval-edge claim.
- **Determinism note:** duration-ms differs run-to-run (recorded ~2930 ms, re-run
  ~3110–3340 ms) as expected; verdict oracle is exit status only, per spec header.

## No flips

0 verdict flips, 0 exit differences, 0 inconclusive, control green, restore OK.
Deltas vs the recorded run are only: scratch paths (mkdtemp names), timestamps,
durations, and the tool sha (75ed934d → 89722ddb, the commit-expected r16 tool —
a methodology delta, not a result delta).

## Verdict

**C1's measured table holds**: re-running §1-§2 of
`corpus/knowledge/mutation-case-kumitate-round-gate.md` under the recorded suite
contract reproduces every verdict, exit, mutant digest, and failing-check set
exactly — 5/10 killed, 10/10 predictions.

## Environment

node v24.21.0, bash 5.x, python3 (runner's spec parser), git; no installs needed.
