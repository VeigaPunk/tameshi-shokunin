# AllFourScorecard — round-34 w1, SCORECARD cold read + all-four re-crediting (tameshi lane)

Scope: full cold read of `SCORECARD.md` (1,670 lines, tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`,
checked-out detached in my scratch lane); verify "axis scores depth 9 / calibration unchanged" and
"the capabilities table row for tally-audit-v2 cites the deciding receipt", plus any stale claim,
missing pointer, or score drift.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/AllFourScorecard/` (lane clone `…/lane`, all exits
captured `cmd; echo $? > file`).

## Pins and page identity

| Check | Result |
|---|---|
| `git -C …/lane rev-parse HEAD` | `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (detached at dispatch tip) |
| `sha256sum` tool copy (`git show 0b99d48:tools/tally-audit-v2.py`) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` = pin |
| `sha256sum` runner copy (`git show 0b99d48:tools/mutate-and-run.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` = pin |
| `sha256sum SCORECARD.md` (lane checkout vs fleet worktree) | `a6b5ba8c1f46e3accca0aa1c490bfc23763fa11d54e304c2d0c43c048371a892` identical, 1670 lines |
| counter `sha256sum .ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` = frozen amended rev (`6aaad5b3`) |
| append-only | `git show 36c1d393:SCORECARD.md` (118,152 B) is a byte prefix of tip `SCORECARD.md` (`cmp` clean); the r31v2 counter independently prints `append_only=1` |

## Verdict on the routed claim

C1 (operability capability acquisition, `tools/tally-audit-v2.py`) MEASURED TRUE at
`c17e593b51802dd4ed568da3265f21c6d00c4273` — **confirmed, no scorecard defect in the routed claims**.
Every cited field in `SCORECARD.md:1636-1670` and the capabilities row at `:1657` reproduces from the
checked bytes:

- Deciding receipt `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` is byte-equal to the
  receipt quoted in the Goal and in `:1643`/`LOG.md:1836-1840`:
  `C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18
  v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1
  seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true`;
  `c1-deciding-run.exit` = `0`.
- Before cell (`:1643`): `.ufo/evidence/round-33/after/c1-at-head-notrun.stdout` prints
  `tool_present=1 … controls_ok=0(receipt-missing) … C1_R33_PASS=false`, `.exit`=1,
  `rev=732b6860dbb5c55a5f60145c0f4903a91a902c58` — matches.
- Only two `C1_R33` receipt outputs exist on record (not-run false + deciding true), consistent with
  "the only `C1_R33_PASS=true` counter output on record" (`:1651`).
- Git ancestry (`git log -- <path>`): counter last touched `6aaad5b` (amendment 6) → controls receipt
  `9dd3174` → sealed held-out `c17e593b` → receipt commit `0b99d48`; `contract-amendments.json`
  amendment 6 discloses the set-aware gate pre-authoring. Order claimed in `:1645-1651` is real.
- Controls receipt `.ufo/evidence/round-33/c1/controls-receipt.json`: 4 controls, all
  `predicate_pass=false`, `all_false=true`, `counter_sha256`=amended sha, `runner_sha256`=pin.
- Sealed set `.ufo/evidence/round-33/heldout/`: 8 `ho-kill-*` + 6 `ho-accept-*` files (14;
  `authoring-receipts.json` = 14 records, all `as_expected:true`).
- Dev receipts behind `:1648-1649`: `dev/witness-probes.json`/`stdout` = 8 probe lines exactly as
  claimed; `dev/panel.stdout` `PANEL: kill=18/18 accept=8/8`; `dev/tool-selftest.stdout`
  `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` — and I re-ran the pinned tool copy's `--selftest`
  (runner beside it): `22/22 pass`, exit 0, 155 s.
- Capabilities row (`:1653-1657`) cites the receipt counts, `rev=c17e593b`, counter path, tool pin
  `7b11ba25…8d10`, `First-working round = round 34` — consistent with all dated literals; it enters
  via the round's own sub-table, matching the rounds-23/24/25 `capabilities addition` convention
  (`:1055`, `:1148`, `:1232`). Last earlier capability row is dated round 25 — consistent with
  "no capability since round 25" (`:1558`, `:1639`) and the stagnation discharge sentence.
- Frontier claim: `corpus/SOURCES.md` row S101 (`:109`) exists, tier C/mined, cites the committed
  snapshot; `sha256sum .ufo/evidence/round-34/src/s101-mutation-testing.html` =
  `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420`, 4,341 B = the row's pin;
  `s101-fetch.exit` `MUT_EXIT=0`. `census-end.stdout` ends `ok`, `census-end.exit`=`0`; S101 W01
  (tier-C mined) disclosed in the output. gnu.org/TLDP rejections recorded in
  `corpus/lessons/round-34.md:26-33` and `LOG.md:1841-1842`; the 9,728 B TLDP snapshot kept as
  evidence. `corpus/knowledge/witness-equivalence-rule.md` cites S097+S101 (`:57-66`).
- Planned (round 35) block (`:1667-1670`): the eight residue class names match
  `corpus/lessons/round-34.md` Holds `:56-59` verbatim and correctly exclude "whole-stdout
  comparison already landed as the r33 DevPrintf fix".

### Axis scores (the two routed numbers)

- **depth 9 — verified.** Command D at tip: `git show 0b99d48:tools/mutate-and-run.sh | python3 -c
  '…'` → `recorded_cases=9 depth_score=9`, exit 0. The standing axis row (`:1536`) says 9; the
  runner's ledger comment (`pristine.sh:87-95`) lists nine legs; monitor `ledger_guardrail`
  `header_legs=9 lists_agree=true`. Row `Last-change round=26` is consistent (ninth leg landed r26).
- **calibration unchanged (8) — verified stronger than claimed.** Strict monitor at tip:
  `python3 .ufo/evidence/round-21/coldread/measure.py --repo …/lane --rev 0b99d48…` → exit 0,
  `sections_covered=64/64`, `box3_full_page=true`, `calibration_restraint_score=8`,
  `overrides_used=false`, `trace_gate=strict`, `depth_score=9`, `sources.rows=98`. The round-34
  block's "re-crediting rides in the r34 wave" (`:1660-1661`) is disclosed and consistent — but the
  observed value already reads 8 (the round-34 appends did not invalidate the 64 credited sections).
- Standing axis table (`:1534-1537`) — depth 9 / calibration 8 — is not altered by the round-34
  block; the block claims only "depth 9 → 9 … No owned axis score lowered" (`:1659-1661`), verified.

## Findings (by severity)

### F1 — LOW (stale standing claim): `sources-registry` row reads `96 rows`, command prints `98`

`SCORECARD.md:1609` (last `sources-registry` row — the current statement per `:1505-1510`):
`bash .ufo/evidence/kaika-round-1/sources-census-v2.sh → exit 0, 96 rows, SOURCES_CENSUS: CLEAN …`.
Reproduce:
```
cd <lane@0b99d48>; bash .ufo/evidence/kaika-round-1/sources-census-v2.sh   # == A rows → 98, CLEAN, exit 0
```
Decisive instrument run (lane's own repaired counter, run from committed bytes, all writes inside
`--work`):
```
python3 .ufo/evidence/round-32/repair/c1-r31-measure-v2.py --rev 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7 --lane <clone> --work EMPTY
→ STATEMENT sources-registry: claimed=0,96 observed=0,98 (exit=0) MISMATCH
→ C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=0b99d48… C1_R31_PASS=false, exit 1
```
The other 11 statements MATCH at tip (runner 106/106, regression `cases=9 passed=9`, repeat-control
29, pin-disposition 19/19, witness-metadata 39/39, evidence-disposition 66/66, context-gate 49/49,
env-diff 9/9, wave-accounting 8/8, depth 9, calibration 8). Under the lane's own r31 discipline this
is one stale standing row: it went stale when SOURCES grew to 97 in round 33 (`LOG.md:1817`,
`round-33/after/census-end.stdout` "97 rows" commit message `5bfa3b5`) and round 33/34 correctly did
not re-state the row — but the "current statement" cell is now two behind. Not a falsification of the
routed claim; a dated literal that the next standing re-statement must refresh (its counting rule is
exactly the r31 predicate).

### F2 — LOW (evidence hygiene): `authoring.stdout` disagrees with `authoring-receipts.json`

`.ufo/evidence/round-34/dev/authoring.stdout:7` records
`{"id": "ho-kill-vector-setup-threshold", … "witness": [false, "vector"], "as_expected": false}`
and the tail prints `SEALED: kill=8 accept=6 all_as_expected=False`, while the committed
`authoring-receipts.json` entry for the same id says `witness: [true,"vector"], as_expected: true`
(all 14 true) and the deciding run reports `ho_invalid=0`. I checked the shipped copy's semantics
myself with the runner's own extraction recipe (`pristine.sh:1994`):

```
awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f' pristine.sh > tblock.sh   # extraction
vector: st_js=2, all others 0   (the copy's witness vector; -gt 0 → -gt 1 edit)
pristine block  → rc=2  "REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)"
mutated block   → rc=0  "REGRESSION: PASS (cases=9 passed=8; ledger legs exact…)"
```
`a != b` holds (SETUP vs PASS): the shipped copy is a valid must-kill under the amendment-6 gate and
the receipts/deciding run are consistent; `authoring.stdout` is a retained pre-fix log line that
contradicts the final JSON in the same commit. Only a report-entry inconsistency, not a scorecard or
measurement defect.

## Observations (not findings)

- `round-33/c1/controls-mint.{stdout,exit=1}` is the retained failed mint (`NameError:
  score_tool`, committed `5bfa3b5`, before `score_tool` was restored); the successful mint is
  `round-34/controls/mint.{stdout,exit=0}` → `C1_R33_CONTROLS: controls=4 all_false=True`.
  Convention-consistent (failures retained), no staleness.
- The frozen r31v2 statement set covers 12 rows; the new `tally-audit-v2` row and the round-32+
  `mutation report interop` row are not in its 12 — so `C1_R31_PASS` cannot see them. (That is the
  instrument's frozen surface, not a scorecard gap; the interop row's dated receipt is consistent
  with `round-33/repair/mte-selftest.*`.)
- Saturation section `:257-262` retains the round-1 `(depth 6 < 8; calibration pinned 0)` literal —
  explicitly superseded by `:1530-1532`; historical by convention, not stale-as-written.
- `Before`/`After` cells in `:1643`/`c1-at-head-notrun` and the r33 row at `:1622` show the label
  stays `C1_R33` while measured in round 34 — that is the counter's own label (frozen contract), not
  a drift.

## Residual risk / verification gaps

- I did not re-run the deciding counter — the kill rule is CONSUMED (forbidden by bounds). The
  receipt is verified for internal consistency and against every committed input (counter sha, tool
  sha, runner sha, controls receipt, heldout files, seed/rev fields).
- `rev=` semantics: receipt `rev=c17e593b` = the heldout-landing revision; per amendment 4 the
  measurement revision is the lane tip at launch, so the deciding run executed when `c17e593b` was
  tip; the receipt commit `0b99d48` lands the output. Consistent; receipt fields checked.
- `ho-kill-vector-setup-threshold`'s validity under the *counter's own* witness computation is
  judged by the deciding run (`ho_invalid=0`); I verified only the copy's semantic `a != b` on the
  pristine block (repro above). Counter-internals are the mutation seats' surface.
- The v3 residue classes (`:1667-1670`) are measurement-only this wave; tool bytes untouched
  (sha verified). Their correctness is out of my scope.

## Commands relied on (all exits captured)

| Command | Exit | Result |
|---|---|---|
| `git clone --no-hardlinks … && git checkout --detach 0b99d48` | 0/0 | detached tip |
| `sha256sum` tool/runner/SCORECARD/counter/controls/snapshot | 0 | pins above |
| `git show 0b99d48:tools/mutate-and-run.sh | python3 -c '…'` (command D) | 0 | `recorded_cases=9 depth_score=9` |
| `python3 .ufo/evidence/round-21/coldread/measure.py --repo …/lane --rev 0b99d48` | 0 | `restraint=8 covered=64/64 box3_full_page=true overrides=false` |
| `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` (in lane at tip) | 0 | `A rows 98`, `SOURCES_CENSUS: CLEAN` |
| `python3 …/round-32/repair/c1-r31-measure-v2.py --rev 0b99d48 --lane …/lane --work r31v2-work` | 1 | `mismatches=1` (sources-registry only), `append_only=1` |
| `python3 tool.py --selftest` (scratch, pinned runner beside) | 0 | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` |
| bash oracle of `ho-kill-vector-setup-threshold` (pristine vs `-gt 1` block) | 0 | rc 2 SETUP vs rc 0 PASS → `a != b` holds |
| `head -c <base> tip | cmp` | 0 | byte-prefix append-only |
| `git log -- <evidence paths>` | 0 | ancestry 6aaad5b → 9dd3174 → c17e593b → 0b99d48 |

No tools installed or upgraded (nothing needed; pacman pause honored). Lane and fleet worktrees
read-only; only this report and `/fast/scratch/…` were written.
