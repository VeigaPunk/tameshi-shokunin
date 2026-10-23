# [seat ColdReadScorecardR34] — r34-w1 cold-read re-crediting of SCORECARD.md round-34 block

Scope (routed from the r33 closure): `SCORECARD.md` from `## Round 34` (line 1636) to EOF
(line 1670) at lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Every cited
hash/commit/receipt checked for existence at the tip; every quote compared against committed
bytes; the recorded counting command re-run in scratch with `--work`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ColdReadScorecardR34/`; lane = detached
`git clone --no-hardlinks` at the tip, `git status --porcelain` → 0 lines (clean).
No lane writes, no git/jj write commands, no tool installs (none needed — `git`, `python3`,
`bwrap`, `bash`, `timeout` all present at `/usr/bin/*`).

**Verdict: AGREE — every cited object exists at the tip, every quote matches committed bytes,
and the counting command re-runs to the recorded line (byte-identical under the recorded
seed; same verdict under a fresh seed). One minor evidence-quality observation on an
adjacent lesson receipt (below) that does not affect the scorecard block's claims.**

## Setup + pins (commands run, exit codes)

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ColdReadScorecardR34
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin .../lane   -> clone_exit=0
git -C lane checkout -q --detach 0b99d48e...                                       -> checkout_exit=0
git -C lane rev-parse HEAD                                                       -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
git show 0b99d48:tools/tally-audit-v2.py | sha256sum   -> 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  == PIN
git show 0b99d48:tools/mutate-and-run.sh | sha256sum   -> a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  == PIN
sha256sum lane/.ufo/evidence/round-33/c1/c1-measure.py -> f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c  == PIN (amendment 6)
git show 6aaad5b3:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum -> f6b8868c…a07f28c  (counter bytes at the amended rev are the minted/pinned bytes)
```

## Cited commits — all exist, ancestry correct

| cite in block | resolves to | check | result |
|---|---|---|---|
| `c17e593b…` (measured commit) | `c17e593b51802dd4ed568da3265f21c6d00c4273` | `git rev-parse --verify …^{commit}`; `merge-base --is-ancestor c17e593b HEAD` | exists; ancestor-of-tip exit 0 |
| `732b6860` (r33 head, Before cell) | `732b6860dbb5c55a5f60145c0f4903a91a902c58` | same + `git log -1` | exists; subject `round-33: C2 measured … honest stop` — it IS the r33 head; ancestor of c17e593b exit 0 (via `3fc1b2fe → 6aaad5b3`) |
| `6aaad5b3` (amendment 6) | `6aaad5b389e7eed426ec3b452617bcbf9bf7f35a` | same | exists; subject `round-34: amendment 6 set-aware witness gate (pre-authoring, pre-data)`; ancestor of c17e593b exit 0 |
| `7b11ba25…8d10` (tool pin) | — | `git rev-parse 7b11ba25^{commit}` → MISSING | correctly NOT a commit — it is the byte-pin sha256, verified by `sha256sum` above |

Chain verified by `git log --format='%H %P %s'`:
`732b6860 (r33 head) → … → 3fc1b2fe → 6aaad5b3 (amendment 6) → 9dd3174c (controls mint) →
c17e593b (sealed set authored) → 0b99d48 (deciding-run receipt + SCORECARD row)`.

## Cited files — all exist at tip (`git ls-tree -r HEAD`)

`.ufo/evidence/round-33/after/c1-at-head-notrun.{stdout,exit}` ✓;
`.ufo/evidence/round-34/measure/c1-deciding-run.{stdout,exit}` ✓;
`.ufo/evidence/round-33/heldout/` = 14 JSON (8 `ho-kill-*` + 6 `ho-accept-*`) ✓;
`.ufo/evidence/round-34/dev/authoring-receipts.json` ✓ (14/14 `as_expected:true`, witness
kinds `head-leg-assignment`×2 / `vector`×6 / `head`×2 / `vector-equivalence`×4 = the 8 kill +
6 accept split the block claims);
`.ufo/evidence/round-33/c1/controls-receipt.json` ✓; `.ufo/evidence/round-33/c1/c1-measure.py` ✓;
`tools/tally-audit-v2.py`, `tools/mutate-and-run.sh` ✓ (pins above);
`.ufo/evidence/round-33/contract-amendments.json` ✓ (amendment 6 entry present, set-aware
witness gate wording matching the block's prose);
`corpus/lessons/round-34.md` ✓; `.ufo/evidence/round-34/src/s101-mutation-testing.html` ✓;
`corpus/SOURCES.md` row `| S101 |` at line 109 ✓.

Post-measurement drift: `git diff --name-only c17e593b..HEAD` lists only
`measure/`, `src/s101*`, `census-end.*`, `LOG.md`, `SCORECARD.md`, `corpus/{SOURCES.md,
knowledge/witness-equivalence-rule.md,lessons/round-34.md}` — no frozen input (tool, runner,
counter, controls receipt, heldout) changed between measurement revision and tip. Heldout
already present at `c17e593b` (`git ls-tree -r c17e593b -- heldout` → 14).

## Quotes — all match committed bytes

- **Before cell**: file `.ufo/evidence/round-33/after/c1-at-head-notrun.stdout` reads
  `C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=0(receipt-missing) v1_kill=0/0 v1_accept=0/0 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 heldout_after_freeze=0 seed=1aa0e2f272685fcd rev=732b6860dbb5c55a5f60145c0f4903a91a902c58 C1_R33_PASS=false`; `.exit` = `1`. The block's quote elides `tool_sha_ok=1 runner_sha_ok=1`, `seed=…`, `rev=…` with `…` — every retained fragment is byte-identical; `exit 1 at 732b6860` matches (short of the receipt's rev=). ✓
- **After cell**: `c1-deciding-run.stdout` is byte-identical to the quoted
  `tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true`; `.exit` = `0`. ✓
- **Capabilities row**: receipt begins `C1_R33:` and ends `C1_R33_PASS=true` with the quoted
  tally fields in order ✓; counter/tool paths exist; pin `7b11ba25…8d10` verified.
- **"minted at `6aaad5b3`"**: `git log -- controls-receipt.json` → single adding commit
  `9dd3174c6daaa55ff5bee32878b700ee3bc731b7` (`round-34: controls receipt minted at the
  amended rev 6aaad5b3`); `6aaad5b3` ancestor of `9dd3174c` ancestor of `c17e593b`. Receipt
  JSON: `all_false:true`, 4/4 `predicate_pass:false` (CtlDoNothing 0/18+8/8, CtlAlwaysPass
  0/18+8/8, CtlAlwaysFail 18/18+0/8, CtlShaOnly 18/18+1/8), `counter_sha256=f6b8868c…a07f28c`
  = counter bytes at both `6aaad5b3` and tip. `.ufo/evidence/round-34/controls/mint.stdout`
  (exit 0) prints `C1_R33_CONTROLS: controls=4 all_false=True` with rows matching the receipt
  field-for-field. ✓ (Observation: the receipt JSON carries no rev field itself; the
  minted-at claim is attested by the adding commit + `counter_sha256` binding, not an
  embedded `rev=`.)
- **"only `C1_R33_PASS=true` counter output on record"**: `git grep -l 'C1_R33_PASS=true' HEAD`
  → `deciding-run.stdout` is the sole receipt artifact; other hits are contract target text
  (`contract.json`) or narrative quotes (SCORECARD/LOG/lessons). ✓
- **S101 freshness row**: SOURCES.md:109 cites `sha256 0fde8a7b…f420`, committed snapshot —
  `sha256sum s101-mutation-testing.html` → `0fde8a7b…f420`, `wc -c` → 4341 = "4,341 bytes";
  rejected TLDP copy `s101b-abs-exit-status.html` → 9728 bytes, `sha256 60cebcc8c8d41ae936136a79f7b94f773fbf09399a31fb32ce722bde992bd291` = lesson's `60cebcc8…d291`; S097 holds the scope at tier A (SOURCES.md:106). ✓
- **Planned (round 35) Holds**: lesson `## Holds` lists exactly the eight classes the block
  names (Guard-2 divisibility, TallyArms-02 coexistence, quoted case subject, helper-function
  refactors, per-index record parsing, preamble seeding, nonzero-leg stress, all-pairs nlegs
  recompute; "whole-stdout comparison" marked already-landed), tool pin `7b11ba25…8d10` frozen. ✓
- **"no capability since round 25"**: r25 admitted `mte-interop` ("capability added",
  SCORECARD.md:1243); rounds 29/30/32/33 each state "no capability row" explicitly
  (lines 1461/1479/1588/1626) and r32:1558/r33:1614 both say "no capability row has entered
  since round 25". ✓
- **"depth 9 → 9 (command D)"**: ran command D on committed bytes —
  `git show HEAD:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'`
  → `recorded_cases=9 depth_score=9`, exit 0; identical at `c17e593b`. ✓

## Counting command re-run (in scratch, `--work` in scratch)

Recorded command (verbatim from the block):
`python3 .ufo/evidence/round-33/c1/c1-measure.py --lane LANE --rev c17e593b51802dd4ed568da3265f21c6d00c4273 --work EMPTY_DIR`

Counter semantics reviewed first (`c1-measure.py:326-431`): all writes go under `--work`;
`--lane` is only read via `git -C lane show/ls-tree/log` (env scrubbed of `GIT_*`); `--seed`
defaults to random. Run against the scratch clone (identical bytes/history at `c17e593b`).

1. **Seed-pinned reproduction** (deterministic check; the seed is a recorded datum):
   ```
   python3 lane/.ufo/evidence/round-33/c1/c1-measure.py \
     --lane /fast/scratch/hyaku/tameshi-r34-seats/ColdReadScorecardR34/lane \
     --rev c17e593b51802dd4ed568da3265f21c6d00c4273 \
     --work /fast/scratch/hyaku/tameshi-r34-seats/ColdReadScorecardR34/work-seeded \
     --seed 685f63bd25263908          -> exit 0, wall 267.4s
   stdout: C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true
   ```
   Byte-identical to `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` (diff: empty). ✓

2. **Literal recorded argv** (no `--seed`, fresh work dir):
   ```
   python3 lane/.ufo/evidence/round-33/c1/c1-measure.py \
     --lane /fast/scratch/hyaku/tameshi-r34-seats/ColdReadScorecardR34/lane \
     --rev c17e593b51802dd4ed568da3265f21c6d00c4273 \
     --work /fast/scratch/hyaku/tameshi-r34-seats/ColdReadScorecardR34/work-literal   -> exit 0, wall 267.4s
   stdout: C1_R33: … identical fields … seed=7a362cd35a66438b … C1_R33_PASS=true
   ```
   Same verdict and all seven tallies under a fresh random seed — the measurement is not
   seed-fragile. ✓

Per the consumed kill rule these are observation runs on a scratch copy; the deciding run
stands. No real-lane path was touched (`--work` is the only write surface).

## Findings

- **F1 (minor, adjacent, not a scorecard defect)** — `s101-fetch.exit` cannot evidence the
  gnu.org "two timeouts" the lesson cites it for: committed bytes are `MUT_EXIT=0`
  (`git show 0b99d48:.ufo/evidence/round-34/src/s101-fetch.exit`; file name says "fetch",
  content is a zero mutation-testing.org-style exit, no stderr sibling exists). The
  SCORECARD block itself claims only that the rejections were "recorded in the round-34
  lesson Gate" — true. The duplicate-scope ground for rejecting both gnu.org and TLDP rows
  is independently verifiable (S097 row holds the scope at tier A). Repro:
  `cat lane/.ufo/evidence/round-34/src/s101-fetch.exit` → `MUT_EXIT=0`.
  (Sibling `ColdReadLesson34` reached the same F1 independently.)

- **F2 (observation)** — `controls-receipt.json` has no `rev`/commit field; "minted at
  `6aaad5b3`" is attested by the adding commit `9dd3174c` and the receipt's
  `counter_sha256` (= the amended-rev bytes), not embedded in the receipt. No defect:
  the scorecard wording is accurate and the binding is cryptographically checkable.

## Residual risk / gaps

- I did not independently re-run the tool selftest or witness-probe batteries; I verified
  their committed receipts (`tool-selftest.stdout` = `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`,
  `panel.stdout` = `PANEL: kill=18/18 accept=8/8`, `witness-probes.json`/`.stdout` = 8/8
  exact) — and my two full counter re-runs re-executed the pinned tool on all 26 public +
  14 sealed copies plus every heldout witness under real `bwrap` (2×267 s, exit 0 both).
- The r33 `.ufo/evidence/round-33/c1/controls-mint.{stdout,exit}` pair records an EARLIER
  failed mint attempt (`NameError: score_tool`, exit 1) — superseded by the successful
  `round-34/controls/mint.*`; consistent with the amendment-1 history. Not a defect.
- `seed=685f63bd25263908` reproduces the receipt byte-for-byte — seed determinism confirmed;
  the only seed-dependent bytes are `seed=` itself.

## One-line

SCORECARD.md's round-34 block re-credits cleanly at `0b99d48`: every cited hash/commit/
receipt exists, every quote matches committed bytes, and the counting command re-runs to
`C1_R33_PASS=true` — byte-identical under the recorded seed — with exit 0.
