# ReviewPinChain — round-34 w1 seat report

Seat: `tameshi-r34-w1-ReviewPinChain` (reviewer). Scope: verify the pin chain across
history for C1 (`tools/tally-audit-v2.py` MEASURED TRUE at `c17e593b51802dd4ed568da3265f21c6d00c4273`,
lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`).

All commands ran against a `--no-hardlinks` clone at
`/fast/scratch/hyaku/tameshi-r34-seats/ReviewPinChain/lane`, checked out
`--detach` at the tip (`git rev-parse HEAD` = `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`).
Reproduce any row with:
`git -C <clone> show <rev>:<path> | sha256sum` (clone made per the seat setup line).

## Verdict: PIN CHAIN INTACT — measurement rev c17e593b carries exactly the pinned bytes; tip 0b99d48e adds only the receipt commit.

## Pin matrix (all `git show <rev>:<path> | sha256sum`, each exit 0)

| artifact | rev | sha256 | expected | match |
|---|---|---|---|---|
| tools/tally-audit-v2.py | f6d8a891 | 9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4 | contract `frozen_artifacts.tool_sha256` `9dbbce62...33a4` | YES |
| tools/tally-audit-v2.py | 49876298 | 7a59f576a3899df0455bcec87647a0f389baa576e978751a63ff6b1ba8b38833 | `7a59f576...` (amendment 3) | YES |
| tools/tally-audit-v2.py | ee398492 | 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10 | `7b11ba25...8d10` | YES |
| tools/tally-audit-v2.py | c17e593b5180... | 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10 | frozen pin | YES — measurement rev has pinned bytes |
| tools/tally-audit-v2.py | 0b99d48e (tip) | 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10 | frozen pin | YES |
| tools/mutate-and-run.sh | 66e1fb44 (base) | a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 | `a7d3f2dd...2eb9` | YES |
| tools/mutate-and-run.sh | c17e593b | a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 | same | YES |
| tools/mutate-and-run.sh | 0b99d48e (tip) | a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 | same | YES |
| .ufo/evidence/round-33/c1/c1-measure.py | 6aaad5b3 | f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c | `f6b8868c...a07f28c` (amendment 6) | YES |
| .ufo/evidence/round-33/c1/c1-measure.py | c17e593b | f6b8868c...a07f28c (full above) | same | YES |
| .ufo/evidence/round-33/c1/c1-measure.py | 0b99d48e | f6b8868c...a07f28c | same | YES |
| .ufo/evidence/round-33/c1/controls-receipt.json | 0b99d48e | f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa | (no pin given; recorded) | — |

Extracted-to-scratch copies verify identically:
`sha256sum tool.py` = `7b11ba25...8d10`, `sha256sum pristine.sh` = `a7d3f2dd...2eb9`
(extract commands: `git -C lane show 0b99d48e...:tools/tally-audit-v2.py > tool.py`, exit 0; same for `pristine.sh`).

## Ancestry and delta c17e593b -> tip

- `git merge-base --is-ancestor c17e593b5180... 0b99d48e...` → exit 0 (measurement rev IS an ancestor of tip).
- `git log -1 --format='%H %P' 0b99d48e` → parent is exactly `c17e593b51802dd4ed568da3265f21c6d00c4273`: tip = measurement rev + one commit.
- `git diff --name-only c17e593b..0b99d48e -- .ufo/evidence/round-33 tools` → 0 paths. Frozen round-33 artifacts and tools/ are byte-identical between measurement rev and tip.
- The single landing commit `0b99d48e` adds `.ufo/evidence/round-34/{census-end.*, measure/c1-deciding-run.*, src/*}`, `corpus/knowledge/witness-equivalence-rule.md`, `corpus/lessons/round-34.md` and modifies `LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md` (`git diff --name-status c17e593b..0b99d48e`).

## Deciding-run receipt (at tip)

- `.ufo/evidence/round-34/measure/c1-deciding-run.exit` content: `0`.
- `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` content (verbatim, matches dispatch):
  `C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true`

## Counter pin logic (why `tool_sha_ok=1` despite the contract field)

`git show 0b99d48e:.ufo/evidence/round-33/c1/c1-measure.py` lines:
- L57: `TOOL_SHA256 = '7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10'  # pinned at freeze; see contract.json ("tool_sha")`
- L349: `tool_sha_ok = tool_present and TOOL_SHA256 is not None and sha256(tool_b) == TOOL_SHA256`
- L58/350: `PINNED_RUNNER_SHA = 'a7d3f2dd...2eb9'`; `runner_sha_ok = ... == PINNED_RUNNER_SHA`
- L367-368: `controls_ok = (receipt['counter_sha256'] == sha256(self_b) and receipt['all_false'] is True and rows_ok)` — receipt self-attestation.

The counter pins via its own constants, not via `contract.json`.

## Controls receipt contents (tip bytes)

`.ufo/evidence/round-33/c1/controls-receipt.json`: `counter_sha256` =
`f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` (matches the
amendment-6 counter blob above, so `controls_ok` self-attestation holds at c17e593b and tip);
`runner_sha256` = `a7d3f2dd...2eb9`; `all_false` = true; `seed` = `a7acbc0ec97d2710`;
four control rows, all `predicate_pass: false`:
- CtlDoNothing.py: kill 0/18, accept 8/8
- CtlAlwaysPass.py: kill 0/18, accept 8/8
- CtlAlwaysFail.py: kill 18/18, accept 0/8
- CtlShaOnly.py: kill 18/18, accept 1/8
(repro: `python3 -c 'import json; d=json.load(open(".ufo/evidence/round-33/c1/controls-receipt.json")); print(d)'` in the tip checkout.)

Minting commit: `git log -- .ufo/evidence/round-33/c1/controls-receipt.json` → single
commit `9dd3174` ("controls receipt minted at the amended rev 6aaad5b3 ... four seat
controls all predicate_pass=false").

## Held-out set (tip)

`git ls-tree -r --name-only 0b99d48e -- .ufo/evidence/round-33/heldout` → exactly 14 files:
8 `ho-kill-*.json` + 6 `ho-accept-*.json` (names listed in transcript).
`git log -- .ufo/evidence/round-33/heldout` → exactly one touching commit, `c17e593b`
("sealed held-out set authored after the amendment-6 counter freeze").
`git merge-base --is-ancestor 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a c17e593b...` → exit 0,
so the held-out adding-commit is a descendant of the amendment-6 counter freeze —
consistent with `heldout_after_freeze=1`. No post-measurement commit touches the directory
(the c17e593b→tip diff over the path is empty).

## Monotonic pin chain (tool)

`git log --oneline -- tools/tally-audit-v2.py` → 3 commits, newest first:
`ee39849` (amendment 5, re-pinned) ← `4987629` (amendment 3+4) ← `f6d8a89` (initial freeze).
Blobs: f6d8a89→`9dbbce62`, 4987629→`7a59f576`, ee39849→`7b11ba25` carried unchanged
through c17e593b and tip. `git log --oneline -- tools/mutate-and-run.sh` shows last
runner change at `bb68156` (round-30); blob `a7d3f2dd...2eb9` identical at base
66e1fb44, c17e593b, tip.

## Findings

### F1 (LOW, informational — expected per assignment, not a measurement defect)

`.ufo/evidence/round-33/contract.json` (sole touching commit `f6d8a89`, per
`git log -- .ufo/evidence/round-33/contract.json`) is stale w.r.t. the re-pinned tool:

- L7 `"tool_sha256": "9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4"`
  — the f6d8a891 blob, two revisions behind the current pin `7b11ba25...8d10`.
- L18 predicate text still reads "the tool bytes equal the frozen pin 9dbbce62...33a4".

No later amendment updated the contract. Impact assessment: none on the landed
measurement — the deciding counter (`c1-measure.py` L57, L349) checks its own
`TOOL_SHA256` constant (`7b11ba25...8d10`), and the recorded run passed `tool_sha_ok=1`
against the pinned bytes. Risk: a third-party verifier that enforces the contract
predicate literally (bytes == `9dbbce62`) would score the current tree FAIL, and a
naive reader sees the comment on counter L57 ("see contract.json") pointing at a
contradicting value. Repro:

```
git -C <clone> show f6d8a891:tools/tally-audit-v2.py | sha256sum   # 9dbbce62...33a4
git -C <clone> show 0b99d48e:tools/tally-audit-v2.py | sha256sum   # 7b11ba25...8d10
grep -n '9dbbce62\|tool_sha256' <clone>/.ufo/evidence/round-33/contract.json
```

Severity LOW: documented staleness, contradicted only if contract text is treated as
executable; the routed counter is the deciding instrument and it is self-consistent.

### F2 — none. No defect found in the landed measurement chain.

## Residual risk / verification gaps

- Pin-chain seat verified bytes/ancestry only; it did NOT re-execute the counter
  (kill rule CONSUMED — prohibited) and did not replay the 18/8/8/6 tallies. Receipt
  fields were cross-checked against committed bytes, not recomputed.
- The `9dd3174` controls-mint commit and `c17e593b` held-out commit both sit between
  the freeze revs and tip; I verified ancestry (`merge-base --is-ancestor`, exit 0) and
  path exclusivity by diff, but did not audit per-copy authoring receipts in
  `.ufo/evidence/round-34/dev/authoring-receipts.json` (outside pin-chain scope).
- `seed=685f63bd25263908` in the receipt is recorded, not re-derived (seed is generated
  per run by `secrets.token_hex(8)`, counter L341 — nothing to check it against).

## Tooling

No installs; system `git`, `sha256sum`, `python3` sufficed. Pacman untouched per the
2026-10-20 pause ruling. No counter invocation in default mode (kill rule consumed);
counter was only `git show`-extracted for source reading.
