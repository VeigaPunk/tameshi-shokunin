# RepeatControlNote — round-16 append falsification (repeated-control note)

Seat: RepeatControlNote (leaf). Lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
All lane reads at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`; sibling reads via
`git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show`. Scratch:
`/tmp/tameshi-r16w2-RepeatControlNote-5FeMEZ` (`SCRATCH` below). No installs or upgrades were made.
Runtimes: `/usr/bin/python3` 3.14.8, `node` v24.21.0 (fnm path), git 2.56.0.

**Verdict in one line: the round-16 append holds on every statement I attacked —
runner pin and both line ranges, `repeat-control.py` identity, the `controls_mismatch`
reproduction, and append-only discipline — with one interpretive gloss noted (S6) and one
stale-sentence residual risk (§3.1 left unedited by design).**

## Statements, method, verdict

| # | Statement in `corpus/knowledge/repeated-control-precondition.md` @ c699c8c | Verdict |
|---|---|---|
| S1 | `:107` §3.1's runner pin ``75ed934d…``, six legs at `:84-89`, "was true at round 12" | **holds** |
| S2 | `:108` round-16 runner sha256 ``89722ddb…`` | **holds** |
| S3 | `:108-109` "gained a seventh leg", legs at `:85-91` | **holds** |
| S4 | `:109` "`repeat-control.py` is unchanged" | **holds** |
| S5 | `:109-113` kumitate round-gate selftest prints `mkdtemp` names; gate returns `controls_mismatch` exit 1 while the exit verdict is stable | **holds** (reproduced) |
| S6 | `:113-114` "That is the gate's declared scope, not a defect (see `mutation-case-kumitate-round-gate.md` §0)" | **holds** (observation/machinery verified; "not a defect" is a sound interpretive gloss, not a literal §0 sentence) |
| S7 | append-only: `git diff 28aeef4 c699c8c -- <note>` shows only additions | **holds** |

## Evidence

### S1 — round-12 pin and six-leg range
- `git show 9df9212:tools/mutate-and-run.sh | sha256sum` → `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` (exit 0). 9df9212 is the
  round-12 commit that last touched the note (`round-12: repeated controls and bounded bash witness attribution`).
- Lines 84-89 at 9df9212 are exactly the six leg rows (`js-kimi-census` … `js-claims-check`); line 80 says
  `# --regression (r4-2; r7-1 leg ledger; r10-2 six legs)`.
- Same bytes/pin at the append base `28aeef4` (round-15): sha256 `75ed934d…`.
- The note at 9df9212 line 54 carries the same pin and `:84-89` text, so the round-16 sentence describes that
  revision correctly.

### S2 — round-16 runner sha
- `git show c699c8c:tools/mutate-and-run.sh > $SCRATCH/mutate-and-run.c699c8c.sh && sha256sum` →
  `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594`.
- Committed receipt `.ufo/evidence/round-16/round-gate/runner-sha256.txt` @ c699c8c: identical line.
- `.ufo/evidence/round-16/round-gate/runner-regression.txt` first line:
  `REGRESSION_TOOL: …/tools/mutate-and-run.sh sha256=89722ddb…f5594`.

### S3 — seventh leg at :85-91
- c699c8c runner lines 85-91 (seven rows, one per line): `js-kimi-census` (85), `bash-surface-census` (86),
  `bash-tsukuroi-census` (87), `bash-mado-verify` (88), `bash-checklist-run` (89), `js-claims-check` (90),
  `js-round-gate … 5/10 (50 %)` (91). Line 81: `# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven)`.
- Leg 7 is implemented, not just a comment: `git diff 28aeef4 c699c8c -- tools/mutate-and-run.sh` shows
  `108 insertions(+), 24 deletions(-)` with an embedded `js-round-gate.spec`, `regression_case_git js-round-gate`
  wiring and `PIN_ROUNDGATE` at the target pin `364f1d5`; `bash -n` on the extracted committed bytes → exit 0.
- Committed selftest (`runner-selftest.txt`) ends `MUTATE_SELFTEST: 81/81 pass` / `VERDICT: PASS`, including
  `PASS embedded leg specs: seven files written` and `PASS embedded leg js-round-gate: spec and recorded table agree`.
- Committed `runner-regression.txt` ends `REGRESSION: PASS (cases=7 passed=7…)`, with
  `REGRESSION_CASE js-round-gate: PASS … defects=10`, `REGRESSION_PIN js-round-gate … sha256=f890e277…d3e9`.

### S4 — repeat-control.py unchanged
- sha256 `296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25` at all three checkpoints:
  9df9212 (round 12), 28aeef4 (round 15 / append base), c699c8c (round 16).
- `git log --format='%h %s' 9df9212..c699c8c -- tools/repeat-control.py` → empty output (exit 0): no commit in
  that span touched the file.
- The note's own round-12 final line (`:84`, `Final gate sha256: 296fe566…`) equals the file's current hash.

### S5 — controls_mismatch on the pinned kumitate round-gate selftest (reproduced)
Target materialized read-only from the sibling repo:
`git -C …/kumitate-shokunin show 364f1d5:scripts/round-gate.mjs > $SCRATCH/rg/round-gate.mjs` →
sha256 `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`, 80,415 B / 1,511 lines.
Kumitate HEAD `1770305`, `git status --porcelain` → 0 entries before/after.

Command (tool bytes copied from c699c8c; isolated env; fresh `--out`; gate writes outside the target dir):

```
env -i HOME=$SCRATCH/envhome TMPDIR=$SCRATCH/envtmp PATH=/usr/bin:/bin /usr/bin/python3 \
  $SCRATCH/repeat-control.c699c8c.py --runs 3 --out $SCRATCH/ctrl3 -- \
  <node> $SCRATCH/rg/round-gate.mjs --selftest
```

- Gate exit `1`; `ctrl3/finding.txt` verbatim:
  `REPEAT_CONTROL: controls_mismatch` / `REPEAT_EXIT: 1`.
- `command.txt` records `tool-sha256=296fe566…bc25`, `python=3.14.8`, `runs=3`, `cwd=$SCRATCH`.
- Per-run exits: `run-1/2/3.exit` = `0`, `0`, `0`; stderr = 0 bytes in all three.
- Per-run stdout: 10,077 B and 63 lines each, three distinct sha256 — i.e. the exit verdict is stable and the
  streams are not (`REPEAT_COMPARE identical=no runs=3`).
- Suite verdict inside every run: 60 `PASS` lines, `ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS`.
- Cause is exactly the mkdtemp name: each run contains one unique token matching
  `kumitate-round-gate-selftest-[A-Za-z0-9]{6}` occurring 9 times; substituting that token makes all three
  captures byte-identical (single normalized sha256 `412d06c5…`, `diff` empty). `diff run-1 run-2` changes
  exactly 9 lines, selftest cases 30, 32, 33, 35, 36, 37, 53, 54, 56 — no other difference.
- Cross-check with retained seat evidence (`.ufo/waves/round-16/w1/RGControl.md` @ c699c8c): same verdict for
  N=3 and N=5, exit 0 and empty stderr 8/8, one token ×9/run, token-substituted captures identical. That seat
  reported 9,663 B/run vs my 10,077 B/run; the delta is exactly the longer `TMPDIR` prefix on those 9 lines
  (46 chars × 9 = 414 B), not a behavioural difference. Its normalized hash differs from mine only because each
  normalization leaves its own parent TMPDIR intact.

### S6 — "declared scope, not a defect"
- The gate declares the byte policy in its own committed bytes: `tools/repeat-control.py:22-23` "Bytes are
  compared as bytes: no decoding, stripping, newline normalization or whitespace folding anywhere in the
  comparison path"; `:32` mismatch on any `(exit, stdout, stderr)` disagreement; `:92-94` a clean match "is not a
  determinism proof and it cures no flakiness".
- The note's own §3.1 (`:53`) states "the unnormalized-byte comparison is the gate's own policy", and §5 (`:80`)
  predicts a volatile-output gate reads `controls_mismatch` on an honest repeat. So the sentence is consistent
  with the note's declared scope.
- `mutation-case-kumitate-round-gate.md` §0 (same commit) supplies the observation anchor: 8 pristine runs exit
  0 with empty stderr, stdout differs every run via one `mkdtemp` suffix on 9 lines; `repeat-control.py` →
  `controls_mismatch` exit 1; "Verdicts are graded on exit status only".
- Precision note: "not a defect" is an interpretation of that declared byte policy — §0 itself does not use the
  words "declared scope" or "not a defect". The interpretation is supported, and the pointer is apt.

### S7 — append-only discipline
```
$ git --no-optional-locks diff --numstat 28aeef4 c699c8c -- corpus/knowledge/repeated-control-precondition.md
11      0      corpus/knowledge/repeated-control-precondition.md        # exit 0
```
- One hunk: `@@ -101,3 +101,14 @@`; 0 lines starting `-`; the added lines are the blank separator, the
  `## Round 16 note (append-only)` heading, a blank line, and nine content lines. Nothing before line 101 is
  touched.
- Blob identity confirms the append is the whole change: the note blob is `28ba852b…` at 9df9212 (round 12),
  `28aeef4` and `e69b488` (c699c8c's parent), and only becomes `c629abb3…` at c699c8c.
- Worktree note is clean (`git --no-optional-locks status --porcelain -- <note>` → 0 entries), matching the
  committed bytes.

## Residual risk / gaps
- **Stale §3.1 sentence in the same file.** `:54` still says "pin unchanged … six recorded legs at `:84-89`",
  which is false of the current c699c8c tree. Append-only discipline forbids editing it, and the Round-16 note
  explicitly scopes it as round-12 truth (`:107`), so this is bounded but remains a read-alone hazard for anyone
  citing §3.1 without §Round 16.
- **"Not a defect" is judgment.** It follows from the declared byte policy and §5's own prediction, but it is
  not a verbatim claim in the cited §0. No contradictory evidence was found.
- **Not rerun:** the full seven-leg `--regression` sweep (cited committed receipt instead; only `bash -n` and the
  committed selftest/regression receipts were checked), snapshot-mode gate arms, and any cross-host reliability
  claim (the note explicitly makes none). S5 was reproduced on one host/one environment, matching the gate's
  own finite-observation scope.
