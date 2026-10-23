# AllFourLog — cold read of `LOG.md` at lane tip `0b99d48` (round-34 entry + earlier entries)

**Scope:** full cold read of `LOG.md` top-to-bottom (1,846 lines) against the detached lane
checkout at `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`, plus verification of every
round-34 entry claim against the committed tree. No verdict consumed; observations only.
No tool installs or updates were performed (bwrap 0.13.1, git, python3 already present).

## Identity checks (all commands run in `/fast/scratch/hyaku/tameshi-r34-seats/AllFourLog`)

- Clone + detach: `git clone --no-hardlinks … && git checkout --detach 0b99d48e` → exit 0
  (`setup.exit` = `0`).
- Live file == tip bytes: `sha256sum …/LOG.md` and
  `git show 0b99d48e:LOG.md | sha256sum` both
  `34ec26b76ee2fa00cbb6ade6b5a6cbd64137dc77aa36196659abb90a1ccaaacb`; `wc -l` = 1,846.
  Earlier entries byte-unchanged: `git diff c17e593b..0b99d48e -- LOG.md` is +28/−0,
  the round-34 block only; the round-34 entry is the file's last entry (lines 1820–1846).
- Pins at tip: `git show 0b99d48e:tools/tally-audit-v2.py | sha256sum` →
  `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` (matches pin);
  `git show 0b99d48e:tools/mutate-and-run.sh | sha256sum` →
  `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches pin).
- Cited revisions resolve: `git rev-parse 6aaad5b3` →
  `6aaad5b389e7eed426ec3b452617bcbf9bf7f35a`; `9dd3174c` →
  `9dd3174c6daaa55ff5bee32878b700ee3bc731b7`; `c17e593b` →
  `c17e593b51802dd4ed568da3265f21c6d00c4273`; `f6d8a891` →
  `f6d8a891f1d966c5c3cdda385090da3a6e804675` (all exits 0).

## Round-34 entry — claim-by-claim

1. **Amendment 6 (`6aaad5b3`, pre-authoring, pre-data).** Confirmed. `git show 6aaad5b3
   --stat` modifies `.ufo/evidence/round-33/c1/c1-measure.py` (+38), records amendment 6 in
   `contract-amendments.json` (6 entries, last = set-aware gate), and commits the two r33
   post-report seat reports (`w1/DevPrintf.md`, `w1/RevengerWitness.md`). Counter sha256 at
   `6aaad5b3` and at tip is `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`
   (both `git show … | sha256sum` and on-disk `sha256sum`, matches the frozen pin). Diff shows
   `ho_witness_ok` gained exactly the LOG-described set-aware rule (kill+head →
   leg-assignment-line diff + identical block; accept+head → identical block; accept+vector →
   `a==b`; kill+vector → `a!=b`, len==9 enforced in `validate_ho`).
   - "Probe battery 8/8 exact": `dev/witness-probes.json` + `.stdout` carry 8 named results
     (Q1-comment-accept, Q3-inert-head-kill, Q3b-ridealong-accept, K-extra-leg-assign-kill,
     K-nonbare-leg-kill, A-inert-head-accept, A-head-with-block, KV-block-identical). [NOTE:
     no committed expectation table — "exact" is author-stated, results are committed.]
   - "public panel re-run 18/18 + 8/8": `dev/panel.stdout` = `panel copies: 26 kill: 18
     accept: 8` / `PANEL: kill=18/18 accept=8/8 elapsed=109.0s`. Confirmed.
   - "tool selftest 22/22": `dev/tool-selftest.stdout` ends `TALLY_AUDIT_V2_SELFTEST: 22/22
     pass`. Confirmed.
2. **Controls receipt at `9dd3174c`.** Confirmed. `controls-receipt.json` (committed
   `9dd3174c`, verified via `git log --diff-filter=A`): `all_false:true`, 4 controls all
   `predicate_pass:false` (CtlDoNothing 0/18+8/8, CtlAlwaysPass 0/18+8/8, CtlAlwaysFail
   18/18+0/8, CtlShaOnly 18/18+1/8), `counter_sha256` = `f6b8868c…a07f28c` = amended bytes,
   `runner_sha256` = pinned runner. Successful mint record:
   `.ufo/evidence/round-34/controls/mint.stdout` → `C1_R33_CONTROLS: controls=4
   all_false=True`, `mint.exit` = `0`. The earlier failed mint
   (`.ufo/evidence/round-33/c1/controls-mint.{stdout,exit}`: `NameError: name 'score_tool'
   is not defined`, exit 1) is honestly preserved — and consistent with `score_tool` being
   absent at `732b686` (verified: `git show 732b686:…c1-measure.py | grep -c '^def
   score_tool'` → 0) and restored at `5bfa3b5`.
3. **Sealed set `c17e593b`.** Confirmed, and independently replayed. Commit adds exactly the
   14 JSONs under `.ufo/evidence/round-33/heldout/` (8 kill + 6 accept). I imported the
   counter as a module (bounds-allowed; never invoked `--lane/--rev/--work` default mode)
   and ran its own `validate_ho` + `apply_edits` + `ho_witness_ok` + `run_tool_sandboxed`
   over all 14 committed files with the pinned runner and tool (scratch
   `test/runner.sh` sha `a7d3f2dd…`, `test/tool.py` sha `7b11ba25…`). Result, exit 0:
   all 8 kills → `witness=(True,…)` + `KILL rc=1`; all 6 accepts → `witness=(True,…)` +
   `ACCEPT rc=0`; zero invalid. This matches `ho_kill=8/8 ho_accept=6/6 ho_invalid=0` in the
   deciding receipt on the same committed bytes.
   - `heldout_after_freeze` chronology: `git log --diff-filter=A` shows heldout files added
     at `c17e593b`, a descendant of counter-add `f6d8a891` and amendment `6aaad5b3`. The flag
     is true, though its mechanism (counter.py:407-411) anchors on the counter's *adding*
     commit (`f6d8a891`, r33 freeze), not on amendment 6 — see F3.
4. **Deciding run.** `.ufo/evidence/round-34/measure/c1-deciding-run.exit` = `0`; `.stdout`
   is byte-identical to the LOG-quoted receipt line including `seed=685f63bd25263908`,
   `rev=c17e593b…`, `C1_R33_PASS=true`. Dir contains only this run — consistent with "first
   full default-mode run". Confirmed.
5. **SCORECARD capability row.** `SCORECARD.md:1636` `## Round 34` block + capability row at
   :1657 (`tally-audit-v2 runner audit`, cites the deciding receipt, counter path, tool pin).
   Current axes unchanged: "Current axes — re-stated at round 31" still holds depth 9 /
   calibration 8; no score drift vs LOG claims.
6. **Frontier bullet.** S101 row exists (`SOURCES.md:109`), tier C, mined, used-by =
   `corpus/knowledge/witness-equivalence-rule.md`; snapshot `.ufo/evidence/round-34/src/
   s101-mutation-testing.html` = 4,341 bytes, `sha256sum` → `0fde8a7bf52acdc5d1c04f01f9ccc948
   96db1844cfdeced98a419861ab7cf420` — matches the row's pinned digest. gnu.org + TLDP rejects
   recorded in `corpus/lessons/round-34.md` Gate. Census receipts: `census-end.exit` = `0`,
   `census-end.stdout` ends `tameshi ok` with expected W04s + a W01 (S101 tier-C note).
   Row count at tip: `grep -c '^| S' corpus/SOURCES.md` → 98 (LOG "97 → 98" consistent).
   `witness-equivalence-rule.md` cites S097 (:57) and S101 (:62). Confirmed.
7. **Wave bullet.** See F1.

## Findings

**F1 (low — freshness/missing pointer): the wave evidence lands one commit after the tip the
entry describes.** At `0b99d48e` the wave bullet claims "one v2 wave … built and validated",
but `.ufo/waves/round-34/` does not exist at the tip (`git ls-tree -r 0b99d48e --name-only |
grep 'waves/round-34'` → empty) and the entry carries no pointer. The artifacts exist only
from `a5b1936` (post-tip: `git show a5b1936 --stat` → `spec-w1.json` 64 items, role histogram
mutation-tester 28 / reviewer 21 / executor 7 / scout 3 / critic 1 / sentinel 1 / revenger 1
/ connector 1 / scribe 1; `dispatch-w1.json` counts.spawn 64, registry members all
`agentId:null` — consistent with "zero dispatches from this session"). At the dispatch tip
the "validated" claim is unverifiable from the tree (validator stdout/exit not committed;
`dispatch-w1.stderr` is 0 bytes). Not a false claim — a pointer/timing gap.

**F2 (info — mixed-generation evidence, disclosed):** `dev/authoring.stdout` is the
*first-generation* run (`ho-kill-vector-setup-threshold` `witness:[false,'vector']`,
`SEALED: … all_as_expected=False`) while the committed `dev/authoring-receipts.json` is the
*final* generation (all 14 `as_expected:true`; verified via `python3 -c json.load`). The
files carry no in-file marker that they are different generations; only
`corpus/lessons/round-34.md` Mistakes §1 explains the first-gen witness `[2,2,0,…]` was
caught and re-authored to `[2,0,…]`. A reader of `dev/` alone sees an apparent contradiction
(receipts all-true vs stdout all-false). Not a verdict defect: the committed sealed bytes
replay `witness=True` + `KILL rc=1` for that copy under the counter's own functions
(reproduced; command in item 3 above), and the lesson discloses the sequence.

**F3 (info — flag semantics):** `heldout_after_freeze` verifies each heldout file's adding
commit is a descendant of the counter's *adding* commit `f6d8a891` (the r33 freeze), not of
amendment 6 `6aaad5b3` (counter.py:385,407-411). The LOG claim "authored after the
amendment-6 freeze" is chronologically true (`c17e593b` is a descendant of `6aaad5b3`;
verified via `git merge-base --is-ancestor`), but the receipt flag itself would not
distinguish a file added between `f6d8a891` and `6aaad5b3`. Precision note, not an error.

**F4 (info — expectation table not committed):** "Probe battery 8/8 exact" commits the 8
result tuples but not the expected values they were judged against; "exact" is author-stated.

## Earlier entries (1–1819) — cold-read results

- No missing pointers: every lane-relative path cited in earlier entries exists at the tip
  (68-path audit, exit-verified: `tools/*`, `corpus/knowledge/*`, `corpus/lessons/*`,
  `plans/*`, `.ufo/*` evidence/wave dirs). `PROTOCOL.md`, `AXES.md`, `MISSION.md`,
  `scripts/sources-census.sh`, `scripts/hyaku/lane-addendum.md`, `.ufo/l0-questions.md` are
  fleet-root paths and exist there; `corpus/QUALITY.md` exists (lane QUALITY cites resolve
  to it). The two `reports/r10-ver-t10.md` / `reports/r11-ver-t11.md` absences are recorded
  *in* the LOG as open items — consistent, not stale.
- No score drift found: recent-round LOG claims match SCORECARD's restated axes (depth 9,
  calibration 8) and per-round measured-result rows; round-34 adds a capability row with no
  scalar change — consistent with the lesson's "No owned axis score" sentence.
- Stale-by-design cells were re-resolved where cheap: r33 "Sources 96 → 97" + r34 "97 → 98"
  chain agrees with 98 `^| S` rows at tip; r33 "mte-interop SETUP repaired (17/17)" is
  corroborated by SCORECARD.md:1526's `MTE_SELFTEST: 17/17 pass` receipt citation.
- Not re-verified by execution (out of this seat's scope / host-state dependent): embedded
  selftest/regression commands from rounds 1–24 historical receipts; file counts carried
  forward from committed receipt artifacts only.

## Residual risk / verification gaps

- The deciding run itself was not re-executed (kill rule consumed); all sub-results were
  instead reproduced via module import on pinned bytes — equivalent coverage for the
  held-out layer, receipt-file verification for the rest.
- The public 26-copy panel was not re-run end-to-end (`panel.stdout` + deciding receipt
  relied on; `public_panel`/`score_tool` seed determinism not re-derived).
- "Validated" status of the wave spec rests on the `a5b1936` commit message + empty
  `dispatch-w1.stderr`; no validator stdout artifact exists anywhere in the tree.
- Earlier-entry audit is a pointer/claim consistency check, not a per-command replay of
  33 historical rounds.
