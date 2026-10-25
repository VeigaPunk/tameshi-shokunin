# Round-42 contract review — findings first

Reviewer: L1Tameshi42.ReviewContract. Review date: 2026-10-25.
Scope: Icontract.json causal separability, universal-clause enumeration, single-valued re-derivable targets, freeze ordering.

## Findings

### F1 [MEDIUM — calibration] C1 universal clause not fully enumerated: round-41 S-id citations are never checked
- Contract statement (contract.json line 15): "the round-41 and round-42 records cite no unmined S-id, no unresolvable repo path (line-scoped extraction) and no unreachable revision".
- The m7 class (contract.json line 26) only covers round-42: "a round-42 record cites an S-id the registry does not hold as mined".
- Implementation: `calibration/measure.py:236-243` iterates **only** `rec42` for the S-id check; the adjacent m8 (`:244-247`) and m11 (`:249-257`) loops iterate `rec41 + rec42`. So a round-41 record citing an unmined bare S-id passes C1.
- Reproduction (scratch clone, deleted after): cloned lane into `/tmp/tameshi-r42-ReviewContract-m7`, committed `echo 'cites S777 in round-41 lesson' >> corpus/lessons/round-41.md`, ran:
  `python3 .ufo/evidence/round-42/calibration/measure.py --lane <clone> --rev 6d2c2df0150b7d201ce19bdf98f10da996fc2fe1 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
  Output: no `MISMATCH m7` for S777; only the expected base m10/records lines. At the measurement revision this record would contribute `m7=0` while violating the statement's round-41 clause.
- The fix is to loop `rec41 + rec42` in the m7 loop (or narrow the statement to round-42).

### F2 [LOW — precision] C2 junk-control failure enumeration in the contract is incomplete vs its own receipt
- Contract.json line 48: "a junk tool that prints every site as not-unflagged fails F02 F03 F05 F06 F07 F08 F09 (receipt control/c2-junk.stdout)".
- The cited receipt `control/c2-junk.stdout` actually fails **F01, F04, and the three live sites** in addition to F02/F03/F05/F06/F07/F08/F09: `fixtures_pass=1/10`, `live_1682_ok=0 live_1685_ok=0 live_123_ok=0`.
- Direction of discrepancy: the receipt shows a *stronger* discriminator than the contract text claims; the control still works, but the contract's enumeration is inaccurate. (Expected: the junk tool zeroes `scratch`/`explicit_out`, so F01 and F04 must fail, as must 1682/1685 (scratch=1 wanted) and 123 (explicit_out=1 wanted).)

## Checks that passed

### Causal separability (C1 without C2, C2 without C1)
- No cross-reference between the two counters: `calibration/measure.py` references only its own path (`SELF_REL`, `CONTRACT_REL`); `census/measure.py` references its own path, `CONTRACT_REL`, and `MUTANTS_REL`. Neither reads the other's outputs, receipts, or directories.
- Each counter self-pins to its own committed bytes (`calibration/measure.py:375-385`, `census/measure.py:366-378`) and measures independently derivable facts (records/registry/paths/revisions vs tool behavior/fixtures/mutants). C1's `records=6` is satisfied by round-41/42 self-assessment records, which are produced by wave seats regardless of C2's outcome; C2's fixtures/live/mutant gates are independent of calibration records. No shared mutable state between the two measurements.

### Universal clauses — otherwise enumerated
- C1: statement clauses map to m6 (scorecard row count, `:228-233`), m8 (paths, `:244-247`), m10 (receipt presence + supersede coverage, `receipt_audit` `:187-221`), m11 (revision reachability incl. fleet repo, `:249-257`), m7 (round-42 S-ids) — with F1 as the only gap. The `records=6` and `self_pin=1` predicate terms are target-enumerated.
- C1 do-nothing/selftest family matches: `T2_*` selftest cases (measure.py:301-315) cover stale-counts / valid-supersede-clears / junk-supersede-still-counts / partial-supersede-still-counts; `--selftest` exit 0, 9/9 OK (before/c1-selftest.stdout).
- C2: statement clauses map to `fixtures_pass=10/10` (all 10 FIXTURES, incl. F06 mixed-callers), `live_1682_ok/live_1685_ok/live_123_ok` with needles `mkdtemp`/`--out` in `resolved` (measure.py:204-211, 263-280), and `mutants_ok` (>=3 mutants covering classes attr/method/outflag, each find exactly once, all killed vs the exit-plus-FAIL oracle, `:427-455`). Kill oracle matches contract `kill_oracle` (`oracle` `:311-317`: errors→runtime_error, fails→killed, else survived).

### Targets single-valued and re-derivable by one command over committed bytes
- C1 target: `self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 C1_R42_PASS=true, exit 0`; re-derived by the single counting command with `--rev REV --freeze FREEZE` over committed bytes (records/registry from REV, pin from freeze).
- C2 target: `C2_R42_PASS=true, exit 0`; single counting command; tool bytes and mutants.json read at REV (`show(lane, rev, TOOL_REL)`, `show(lane, rev, MUTANTS_REL)`), fixtures pinned in the counter.

### Freeze precedes every wave-1 file
- `git log -3`: `322b5cd32b4319a05340d249ae752d12a9e6b19f 2026-10-25T06:22:19-03:00` (freeze, HEAD) → `c77c2b7e64d2e356381441ecf94abac03e984606 2026-10-25T04:26:26-03:00` (base) → `b8e39564…`.
- Freeze commit contains exactly `contract.json` + both counters (git show --stat: 3 files). Counter hashes at freeze equal the declared `counter_sha256` values (C1 `9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e`, C2 `3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2`).
- Contract blob sha at freeze == working-tree sha (`437afc7d692ca3e15288e488de0f4dd2ebb24c85bf0cf30cd463dab0caa3fc20`); no post-freeze amendment (post_freeze_amendments=[]).
- Every wave-1 file exists only after the freeze: `.ufo/waves/round-42/spec-w1.json`, `dispatch-w1.json`, `w1/swarm-registry.json` at 06:25 (all untracked); `before/`, `control/`, `census-sources/` at 06:22:33–51 (> freeze 06:22:19). None are in any commit.

### Base/control honesty
- C1 base receipt `before/c1-at-base.stdout` matches `before_expected`: `m10=1 records=3 C1_R42_PASS=false`, exit 1.
- C2 base receipt `before/c2-at-base.stdout` matches `before_expected`: `tool_absent=1 live_unflagged_v3=3 C2_R42_PASS=false`, exit 1.
- Control receipts: `control/c1-do-nothing.stdout` (scratch rev `5e74a8cbd555b2589c64c5f92eb4baf8679fbb1b`) shows records=6, m10=1 — matches "adds three round-42 records but no superseding receipt keeps m10=1". `control/c2-v3-in-slot.stdout` fails exactly F01/F04 + the three live sites — matches contract. `control/c2-junk.stdout` behavior consistent with the junk tool source (`junk-tool.py` zeroes scratch/explicit_out/unflagged), with the enumeration nit in F2.

## Residual risks / not checked
- Per kill rules I did not run either counter at a measurement revision; the one deciding run belongs to the L1.
- The `inherited_state` watchdog/jj claim (contract.json line 9) is not independently verifiable from committed bytes; no contradiction found.
- The scratch clone used for F1 was deleted; all state above is from committed bytes and untracked receipts.

## Tooling
No tools installed (none required beyond git/python3 present on host).
