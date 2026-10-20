# S06 — Run round-15 verify.py from live lane and a fleet-mirror clone

Seat: TameshiR17.S06RunR15Verify (scout; leaf, no subagents). Lane tip at dispatch:
98bea7da5801f4bc58e4187690ee1687c8a5061f. Target rev:
7650fe4db89f3a706aed63d048ac47e02289cc72. No tools installed; nothing upgraded.

## Commands and exits

### 1. Fleet-mirror clone (/tmp sandbox, lane at the target rev)

```
W=$(mktemp -d /tmp/tameshi-r17w1-S06RunR15Verify-XXXXXX); mkdir $W/fleet
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = .../tameshi-shokunin ] || ln -s "$s" $W/fleet/; done
git clone -q .../tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q 7650fe4db89f3a706aed63d048ac47e02289cc72
cd $W/fleet/tameshi-shokunin
python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72
```

- `git rev-parse HEAD` in clone = `7650fe4db89f3a706aed63d048ac47e02289cc72`.
- **Exit 0**, wall 1.73 s, 44 checks, `FAIL` lines 0.
- Receipt: `.ufo/evidence/round-15/verification-3.json` (clone had verification/-2), `attempt=3`,
  `passed=true`, `failed_checks=[]`, `artifact_dir=.ufo/evidence/round-15/attempt-3`.
- Head of stdout: `rev-resolves PASS`, `baseline-resolves PASS a9cf4da…`,
  `prefix-resolves PASS bca5deb2f61f…`, both tool pins PASS
  (`c4a1d165…` at REV, `0ed784e0…` at prefix), receipt pins PASS, all six
  `integrity-*` PASS, `selftest-new: PASS … SELFTEST: PASS (49/49)`,
  `gate-frozen-builtin: PASS exit=0`, `mapping-oracle-discriminates: PASS
  oracle old=FAIL/1 new=PASS/0`, `measure-before/after-fields: PASS`,
  `sources-census: PASS`, `sources-census-ok-line: PASS`.

### 2. Live lane root

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72
```

- **Exit 0**, wall 1.70 s, 44 checks, 0 `FAIL`.
- Receipt: `.ufo/evidence/round-15/verification-4.json`, `attempt=4`, `passed=true`,
  `failed_checks=[]`, `artifact_dir=.ufo/evidence/round-15/attempt-4`.
- Full stdout diff live-vs-clone: only the `tempfile.mkdtemp` path in the
  `selftest-same-path-same-argv` line differs (`/tmp/tameshi-r15-verify-o599mows`
  vs `…-j0inxzt4`); everything else byte-identical. So live and clean-clone
  behaviour coincide at this rev.
- Writes made by the run (exclusive-create; nothing tracked modified):
  - new untracked `?? .ufo/evidence/round-15/attempt-4/`
    (`expected.json`, `before.json`, `after.json`, `sources-after.json`)
  - new untracked `?? .ufo/evidence/round-15/verification-4.json`
  - `git status --porcelain` before/after differ only by those two entries.
    Pre-existing live dirt (unchanged): ` M .gitignore`,
    ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`,
    `?? .ufo/evidence/round-16/__pycache__/`, `?? .ufo/evidence/round-17/`,
    `?? .ufo/waves/round-17/`. The live run is unaffected by that dirt.

## Does it read live `tools/` bytes?

Authority bytes come from git, not the worktree: `ROOT` is derived from the
script's own path (`verify.py:89`) and every pin/preservation read is
`git -C ROOT show <rev>:<path>` (`verify.py:147-158`, used at `:389`, `:417`,
`:436`, `:456`, `:463`, `:470`) with `GIT_*` stripped from the child env.
But four places touch the live worktree:

| Live read / exec | Location | Effect on run |
|---|---|---|
| `tools/context-capture.py` bytes, sha vs `PIN_TOOL_SHA256` | `verify.py:638-640` | **Sensitive.** Mismatch → `registered-tool-source-pin: FAIL` → exit 1. |
| executes live `tools/context-capture.py --check --json` (cwd = lane root) | `verify.py:642-650` | **Behaviour-sensitive.** Tool does not self-hash, so the check still passed under a byte-tampered copy (see probe below). |
| `.ufo/evidence/round-15/measure.py` bytes vs REV blob | `verify.py:760-765` | **Sensitive.** Mismatch → `measure-script-pin: FAIL` → exit 1. |
| executes live `.ufo/evidence/round-15/measure.py --rev {baseline,REV}` | `verify.py:776`, `:787` | Live bytes are what run (pin above guards drift). |
| existing `round-15/frozen/**` fixture bytes | `verify.py:504-511`, `:265-278` | Reads and digest-verifies; a mismatch raises `SystemExit` → `runner-write-refusal: FAIL`. No rewrite when digest matches (confirmed: no tracked frozen path changed). |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | `verify.py:105`, `:835-837` | Absolute fleet tool; it reads the lane's **live** `corpus/SOURCES.md` (`scripts/sources-census.sh:467`, `:483`). Only `exit==0` + `tameshi\tok\t` are asserted. |

Not read live: `tools/mutate-and-run.sh`, `SHONEN.md`,
`corpus/lessons/round-14-verifier-spotcheck.md`, the round-14 receipts and
round-12..14 trees — all compared/consumed as committed blobs only
(`verify.py:456-474`). Concretely: at this rev the runner blob is
`75ed934d…75ed93` while the live file is already `0673d2e5…` (round-17 jj
repo-identity guard, HEAD), and the live run is still green.

`verify.py` itself is not self-pinned: it executes the bytes present at
`.ufo/evidence/round-15/verify.py` and derives `ROOT` from them (`:89`), so a
wave edit to this file would silently change what "the round-15 run" means.

## Mutation probes (throwaway clone only; live lane untouched)

Each probe appended one comment line to its target, ran the same command, and
restored with `git checkout -- <path>` inside the /tmp clone:

| Perturbed live file | Exit | FAIL lines |
|---|---|---|
| `tools/context-capture.py` | **1** | `registered-tool-source-pin` only. `gate-frozen-builtin` still PASS exit=0 → the gate does not verify its own bytes at runtime; only the runner-side pin catches drift. |
| `tools/mutate-and-run.sh` | **0** | none — confirms worktree-independence for the runner. |
| `.ufo/evidence/round-15/measure.py` | **1** | `measure-script-pin` only (`worktree measure.py differs from revision blob`). |

## Rev-bound scope (extra falsifier)

Running the same verifier with `--rev 98bea7d…` (branch tip) in the clone gives
**exit 1**, 4 failures: `integrity-tools/mutate-and-run.sh` (75ed93 vs 0673d2),
`integrity-SHONEN.md` (3b1dc5 vs 4a11ad), `runner-published-digest`, and
`measure-after-fields` (`runner_sha256_matches_round14_published: 0≠1`,
`recorded_cases: 7≠6`). So round-15's verify.py is a receipt for **its own
REV 7650fe4**, not a tip regression gate: it MUST NOT be re-pointed at HEAD to
"prove" the lane still holds.

## Relevance to round-17 claims

- C2 (operability) rests partly on the round-17 `tools/mutate-and-run.sh` fix;
  that edit is invisible to round-15 verify (live run exit 0), so it neither
  rescues nor harms the round-15 receipt.
- The live round-15 receipt is only put at risk by wave edits to
  `tools/context-capture.py`, `round-15/measure.py`, the round-15 `frozen/`
  fixtures, or `verify.py` itself. None of those are in this round's declared
  C1/C2 edit set (dispositions v2, registry-check, registry.json,
  mutate-and-run.sh, pin-disposition.py).
- Do not count the freshly-added `verification-4.json` / `attempt-4/` as new
  evidence for C1/C2; they are a reproducibility replay of round-15 at 7650fe4.

## Verdict

holds — exit 0 / 44-44 from both live lane and fleet-mirror clone (identical
stdout apart from the mkdtemp path); it is worktree-sensitive only to
`tools/context-capture.py`, round-15 `measure.py`, round-15 frozen fixtures and
its own bytes, and is pinned to rev 7650fe4.
