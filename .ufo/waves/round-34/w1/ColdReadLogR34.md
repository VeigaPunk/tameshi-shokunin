# ColdReadLogR34 — cold-read re-crediting of LOG.md `## Round 34` (round 34, wave 1)

Seat: cold-read re-crediting (routed from the r33 closure). Verdict: **the `## Round 34` entry
re-credits clean — every commit hash, path, receipt line, and count in the entry verifies against
the dispatch tip `0b99d48e`; the deciding-run line matches the committed stdout byte-for-byte, and
the counter's `ho_invalid=0` / `heldout_after_freeze=1` conjuncts reproduce by module import.**
No material findings. One observation-grade ambiguity in a dev artifact (O1) and two
out-of-lane unverifiables (R1, R2) are recorded below.

## Method and pins

All work in `/fast/scratch/hyaku/tameshi-r34-seats/ColdReadLogR34/` (clone `lane`, detached
material inspected via `git show <rev>:<path>`; no git/jj write commands anywhere; lane
untouched). Counter used only as an imported module (bounds-authorized); the kill rule was not
consumed — no default-mode counter run.

- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks <fleet> lane` → exit 0 (`setup.exit`=0)
- `git show 0b99d48e…:tools/tally-audit-v2.py  > tool.py` → exit 0; sha256 `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` = pin ✓
- `git show 0b99d48e…:tools/mutate-and-run.sh > pristine.sh` → exit 0; sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` = pin ✓
- Tip `0b99d48e` is ancestor of fleet-root HEAD `a5b19364` (`merge-base --is-ancestor` → 0); `git diff 0b99d48e HEAD -- LOG.md` empty (0 +/- lines) — no post-dispatch drift in the entry.

## Verification matrix (entry claim → evidence)

| Entry claim | Evidence | Result |
|---|---|---|
| Amendment 6 `6aaad5b3` (set-aware witness gate, pre-authoring, pre-data) | commit `6aaad5b389e7eed426ec3b452617bcbf9bf7f35a` exists, message "amendment 6 set-aware witness gate (pre-authoring, pre-data)…", stat touches `c1-measure.py` (+38) and dev receipts; ancestor of everything below | ✓ |
| Probe battery 8/8 exact | `.ufo/evidence/round-34/dev/witness-probes.json` = 8 outcome strings; each matches the set-aware rule branch-by-branch (e.g. `KV-block-identical -> (False, 'block-identical')`, `Q3b-ridealong-accept -> (False, 'head-with-block-edit')`) | ✓ |
| Public panel re-run 18/18 + 8/8 | `dev/panel.stdout`: `PANEL: kill=18/18 accept=8/8` (copies 26) | ✓ |
| Tool selftest 22/22 | committed `dev/tool-selftest.stdout`: `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`; **freshly reproduced** on the pinned bytes: `python3 tool.py --selftest` → exit 0, `22/22 pass` (139.5 s, bg_2683) | ✓ |
| Controls receipt minted at amended rev, `9dd3174c`, 4 controls all false | commit `9dd3174c6daaa55ff5bee32878b700ee3bc731b7` message matches; `controls-receipt.json`: `all_false: true`, 4 rows `predicate_pass: false`, `counter_sha256 = f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` = sha256 of `git show 6aaad5b3:.ufo/evidence/round-33/c1/c1-measure.py` AND of the same path at `c17e593b`; `runner_sha256` = runner pin | ✓ |
| Sealed set 8 must-kill (2 head + 6 block-behavioral) + 6 must-accept (2 head + 4 block-equiv), committed at `c17e593b` | `ls-tree` census: `ho-kill-head-*` 2, `ho-kill-vector-*` 6, `ho-accept-head-*` 2, `ho-accept-vector-*` 4 (14 total); every copy's `adding_commit` = `c17e593b…` (reproduced via counter module); tool+counter adding commit `f6d8a891` is ancestor of all 14 → `freeze_ok=True`, `heldout_after_freeze=1` | ✓ |
| Per-copy authoring receipts | `dev/authoring-receipts.json`: 14 rows, all `as_expected: true`, all `witness[0]: true` | ✓ |
| Deciding run receipt, exit 0 | `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` line 1 equals the goal-quoted receipt **byte-for-byte** (`grep -Fx -f goal-receipt.txt` → exit 0; whitespace-joined LOG quote also equal), file is exactly 1 line; `c1-deciding-run.exit` = `0`; fleet-root working copies byte-identical to tip blobs (`cmp` → 0 for both) | ✓ |
| `ho_invalid=0` (implicit in receipt) | **Reproduced**: imported the measurement-rev counter as a module (`repro-witness.py`); canonical `ho_witness_ok` returns `True` for all 14 sealed copies; suspect `ho-kill-vector-setup-threshold` gives a=`(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')` vs b=`(0, 'REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)')` → `(True, 'vector')` | ✓ |
| Frontier: S101 opened; census 97→98 | `corpus/SOURCES.md` has 98 `^| S` rows; S101 at line 109 with snapshot `.ufo/evidence/round-34/src/s101-mutation-testing.html`, sha256 `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420` = recomputed ✓ | ✓ |
| gnu.org bash manual rejected; TLDP duplicate also rejected | `corpus/lessons/round-34.md` "Rejections:" lines 24–32; TLDP snapshot `src/s101b-abs-exit-status.html` present, sha256 `60cebcc8c8d41ae936136a79f7b94f773fbf09399a31fb32ce722bde992bd291` matches the lesson's `60cebcc8…d291` | ✓ |
| Lesson + knowledge (cites S097 + S101) | `corpus/lessons/round-34.md` and `corpus/knowledge/witness-equivalence-rule.md` exist at tip; knowledge cites S097 (lines 57–61) and S101 (lines 62–65) | ✓ |
| Capability row enters SCORECARD | `SCORECARD.md` line 1657 (round-34 capability row quoting the deciding receipt) + Round 34 section at line 1636; r33 row (line 1622) honestly reads "measurement NOT RUN" | ✓ |
| Motivation: "two uncommitted r33 seat reports" | commit `6aaad5b3` adds exactly `.ufo/waves/round-33/w1/DevPrintf.md` (+340) and `.ufo/waves/round-33/w1/RevengerWitness.md` (+161) | ✓ |
| Entry landed at dispatch tip | `git log 0b99d48e -- LOG.md`: tip commit "round-34: C1 measured true at c17e593b (deciding run receipt)…" | ✓ |

## Findings

None material. Every credited artifact (tool pin, runner pin, counter bytes, controls receipt,
sealed set, deciding receipt, SCORECARD row) verified against the tip, and the two receipt
conjuncts that depend on execution (`ho_invalid=0`, `heldout_after_freeze=1`) were reproduced
independently of the deciding run's own stdout.

**O1 (observation, no action required):** `dev/authoring.stdout` records the *caught first
authoring pass* — suspect row `"witness": [false, "vector"], "as_expected": false`, footer
`SEALED: kill=8 accept=6 all_as_expected=False` — while the cited `dev/authoring-receipts.json`
(all-true) and the canonical gate agree the sealed copy passes. This is exactly the mistake the
lesson's Mistakes §1 documents (first-pass witness `[2,2,0,…]` ties SETUP), and both sides
reproduce: with vector `[2,2,0,…]` the gate returns `(False, 'vector')` with a==b=`(2, 'REGRESSION:
SETUP (cases=9 passed=7 cannot-verify=2)')`; with the sealed `[2,0,…]` it returns `(True, 'vector')`.
Residual: the stdout's `SEALED:` footer can read as final without the lesson context, and the LOG
entry cites only the JSON — a cosmetic ambiguity in a measurement-only dev artifact, not a defect
in the credited chain.

## Residual risk / verification gaps

- R1: wave-level claims ("one v2 wave, policy v2 band 64-128, ≥25% attack", "taskCall returned to
  the orchestrator", "seat relays folded") have no artifact at the lane tip (`.ufo/waves/round-34/`
  is absent from the tree) — consistent with the entry's own "zero dispatches from this session";
  verifiable only orchestrator-side.
- R2: `v1_kill=18/18 v1_accept=8/8` inside the deciding receipt was not re-executed here (the kill
  rule is consumed and the full panel re-run belongs to the lab-rat seat); it is corroborated by
  the committed pre-data `dev/panel.stdout` (18/18 + 8/8 through the amended machinery) and by the
  fresh 22/22 selftest, but the deciding-run panel itself was taken on the receipt's word.
- Environment: bwrap 0.13.1 present; no tool installs or upgrades were needed (no pacman use).

## Key commands

```
git -C lane show 0b99d48e…:tools/tally-audit-v2.py  > tool.py     # sha 7b11ba25… = pin
git -C lane show 0b99d48e…:tools/mutate-and-run.sh > pristine.sh  # sha a7d3f2dd… = pin
grep -Fx -f goal-receipt.txt tip-deciding.stdout                 # exit 0 (byte-for-byte)
python3 repro-witness.py    # canonical ho_witness_ok over all 14 copies; suspect a/b tuples
python3 freeze.py           # adding commits; freeze_ok True; receipts-JSON row pull
python3 tool.py --selftest  # exit 0, 22/22 (fresh, pinned bytes)
```
Scratch evidence retained at `/fast/scratch/hyaku/tameshi-r34-seats/ColdReadLogR34/`
(`repro1.stdout`, `selftest.stdout`, `tip-deciding.{stdout,exit}`, scripts).
