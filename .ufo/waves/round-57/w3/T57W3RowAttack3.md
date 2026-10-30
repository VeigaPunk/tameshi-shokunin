# T57W3RowAttack3 — semantic ledger attack

Axes: semantic coverage; fixing-commit identity; persistence at tip; reproducible evidence.

Scope: all 13 assigned rows. Ledger snapshot and frozen item texts are in this seat's receipts directory. Reviewed master `2c51affd37e15cd7cd258d76ba0f5f73ff235924`; C0b is `adf87899c70d616140a81185a8f9acbbdfb30392`. No lane content or ledger was edited. Recommendations only, not admission or judgment. Result: **3 wrong, 2 weak, 8 supported**.

## Findings (severity order)

### High — R56.5 open status ignores the committed successor repair

The historical round-56 files are unchanged, but checking only those files misses the actual successor. Commands:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%H %s' master -- .ufo/evidence/round-57/controls.sh .ufo/evidence/round-57/c2/measure.py
870d9b987f14a046964018429662a238f2fe9e20 round-57 (honest stop, operator wrap-up): unfrozen instruments ...
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-57/controls.sh
4: # ONE GENERATION. Controls are RECOMPUTED, never READ ...
5: # ... R56.5 ... round 56's C2 arm 5 read the round's committed controls-a/b.stdout ...
7: # generation plus a second one. Nothing here reads a committed receipt of this round.
13: # the script refuses (exit 2, CTL_GENERATION_ERROR) when REV already carries a controls receipt
```

The committed successor C2 implementation recomputes registry/gate results and no longer has the inherited own-receipts acceptance arm. This is a structural repair, not evidence that a deciding run passed. Recommend a fixed successor row, using 870d9b98 and the implementation, explicitly retaining execution qualification. Full outputs: `R565-successor-header.txt`, `R565-successor-history.txt`, `R56.5-successor-implementation.txt`.

### Medium — R55.2 cites a superseded, substantively incorrect correction

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show master:.ufo/waves/round-55/w1/T55W1ScribeSkill.md
147: C2_R55: rev=08d64e946006 grammar=9/9 ...
148:         docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
157: commit 9de7deac0d72`): `grammar=8/8 … total=0 C2_R55_PASS=true` ...
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format= adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/lessons/round-57.md
- **R55.2 — a quoted C2 total the receipt contradicts.** ...
+ **R55.2 — the quoted C2 total is not in the report.** ...
```

The row's ca75c267 correction accepted the verifier's false report attribution. C0b corrects that premise instead; row excerpts at lines 21 and 22 no longer resolve. Use adf87899 and current lesson lines 19–26. Full outputs: `R556-source-report.txt`, `R556-source-receipt.txt`, `R55.2-C0b-diff.txt`, `R55.2-tip-excerpts.txt`.

### Medium — R56.7 points to the old correction, not the actual bounded-interval repair

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show master:corpus/lessons/round-57.md
25:   labelled as earlier. The 9-mode run is `total=1`, verdict false. This line answers the item; the
27: - **R56.7 — "no byte changed after C0/PIN" holds from 877eedee to base only.** ...
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format= adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/lessons/round-57.md
- **R56.7 — "no byte changed after C0/PIN" is true of PIN→tip, not of C0→PIN.** ...
+ **R56.7 — "no byte changed after C0/PIN" holds from 877eedee to base only.** ...
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat 877eedee3ddb7fe25d7a6a09922b04ba13e5a99b 5e3569969b532310d2b8a3d130901757a3df356b -- SKILL.md corpus/QUALITY.md corpus/SOURCES.md corpus/knowledge tools
[no output]
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat c0137451f5b7 877eedee3ddb -- corpus/QUALITY.md corpus/SOURCES.md corpus/knowledge/receipt-revision-binding.md
corpus/QUALITY.md | 31 +...
corpus/SOURCES.md | 2 ++
corpus/knowledge/receipt-revision-binding.md | 39 +...
3 files changed, 72 insertions(+)
```

The status can remain fixed, but the row's line-25 excerpt is absent and fix identity should be adf87899. Full outputs: `R56.7-C0b-diff.txt`, `R56.7-interval.txt`, `R56.7-before-bind.txt`.

### Low — weak support, not asserted regressions

- **R56.2:** ca75c267 repairs the SKILL cell; the second required repair (semantic docs arm) lands in 870d9b98. Cite both. `R562-counter-history.txt` and `R562-tip-semantic-arm.txt` show implementation identity. The executed verdict fixture emits CONTENT_DRIFT (exit 3), matching the cell (`R56.2-verdict.txt`).
- **R56.3:** governing erratum plus README index exists, but frontmatter line 3 still instructs 14/14 and does not point to ER-R57-K1. This is weak under the item's explicit recheck-line pointer requirement; append-only superseding-entry interpretation may be acceptable. `R563-note.txt` and `R563-errata.txt` retain actual command outputs. Do not claim the frontmatter line changed.

## Complete row sweep

- **R54.10 — supported** (ledger `fixed`, commit `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`): 9cf0146 adds the explicit ER-R54-10 correction in SCORECARD; current receipts distinguish 0/7 and 0/30. The cited commit genuinely introduces the correction, not just a path touch.
- **R55.2 — wrong** (ledger `fixed`, commit `ca75c2674645ab6bdadeecb8584007c74342bfa9`): The row cites ca75c267 and excerpts no longer present at tip. That commit repeats the false premise that the scribe report quoted total=0 for the nine-mode run; actual report lines 147-148 say total=1 and line 157 labels the earlier eight-mode run. adf87899 replaces this with a correction of the verifier misquote.
- **R55.4 — supported** (ledger `open`, commit `none`): The committed phase-A receipt already finishes CTL_SKIP_c2 with total=4 and CONTROLS_A 5/5; no post-base change on that path corrects the stale report sentence, and the row honestly leaves it open.
- **R55.5 — supported** (ledger `fixed`, commit `c3e2ca9f020776b3d66c7af854fb82c834674fcf`): c3e2ca9f introduces both gate implementation and deciding-run integration. Current deciding-run gate 0b reads committed receipts and passes certified REV/paths/control/positive; gate 0c binds newly produced verdicts. Drift fixture refuses exit 3, confirming the required comparison is real.
- **R55.6 — supported** (ledger `fixed`, commit `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`): 981c5e8b explicitly introduces all seven listed missing receipt blobs. ls-tree verifies the same seven blobs at current tip; not merely the two cited JSON headers.
- **R55.7 — supported** (ledger `declined`, commit `none`): The spot-check itself explicitly labels contamination not lane debt; round-56 lesson records branch-byte restoration and the remaining external harness write scope. Declined matches that ownership, not a claim the harness is fenced.
- **R56.1 — supported** (ledger `open`, commit `none`): At tip SKILL line 491 still sends the 80-percent claim to 335-339, which instead discuss survivor classes; page-local references remain. Post-base path history shows no anchor replacement.
- **R56.2 — weak** (ledger `fixed`, commit `ca75c2674645ab6bdadeecb8584007c74342bfa9`): The table cell is corrected by ca75c267 and current verdict+paths drift emits CONTENT_DRIFT. However the item also requires the docs arm to check semantic truth; that committed implementation is in 870d9b98, not the row's ca75c267, and the evidence cites only the cell.
- **R56.3 — weak** (ledger `fixed`, commit `ca75c2674645ab6bdadeecb8584007c74342bfa9`): ca75c267 adds an explicit governing 19/19 erratum and README index, still present. Frontmatter recheck line 3 nevertheless retains 14/14 and has no pointer to the new erratum, despite the item asking for replacement or a pointer from that line.
- **R56.4 — supported** (ledger `fixed`, commit `ca75c2674645ab6bdadeecb8584007c74342bfa9`): ca75c267 records a concrete referent. Exact blob hashing confirms 13 SOURCES and 6 QUALITY mismatching labels all equal 877eedee bytes; this satisfies record-referent without rebinding.
- **R56.5 — wrong** (ledger `open`, commit `none`): Open is stale at current master: 870d9b98 commits round-57 controls header explicitly naming R56.5, ONE GENERATION and never reading committed receipts, plus a counter that recomputes gate/registry results instead of inheriting the own-receipts arm. The historical round-56 files cited by the row remain frozen, but do not establish current unresolved behavior.
- **R56.6 — supported** (ledger `fixed`, commit `ca75c2674645ab6bdadeecb8584007c74342bfa9`): ca75c267 adds three actual gate-kind rows plus SKILL exit map; extracted committed fixtures executed exits 0/3/2 with expected codes. The cited commit is the substantive registry repair.
- **R56.7 — wrong** (ledger `fixed`, commit `ca75c2674645ab6bdadeecb8584007c74342bfa9`): Fixed behavior exists at tip, but the row's excerpt is absent from its cited line 25 and its ca75c267 correction was explicitly rewritten at adf87899 to name the actual interval 877eedee to base. The canonical git diff for that interval is empty; C0-to-bind changes three claimed surfaces.

## Executed checks and residual risk

Every assigned item was read against its routed spot-check lines (`<ID>-spot.txt`), every ledger excerpt was compared to tip (`<ID>-tip-excerpts.txt`, `excerpt-sweep.txt`), each fixed row's actual commit patch was collected (`<ID>-target-diff.txt`), and cited-path history checked (`<ID>-history.txt`). `command-index.json` records git commands and output paths. Excerpt matching was whitespace-normalized, so ordinary wrapping was not treated as a defect.

Four gate invocations executed from extracted tip bytes, without invoking a deciding runtime: accept=exit 0 PASS; drift-positive=exit 3 CONTENT_DRIFT; unresolved-certified=exit 2 REV_UNRESOLVABLE; drift-verdict=exit 3 CONTENT_DRIFT. Each exact argv/stdout/exit is in `receipt-gate-*.txt` and `R56.2-verdict.txt`. These are direct gate checks, not a full registry-check run.

R55.6: `ls-tree -r` shows all seven inherited receipt paths as blobs in both 981c5e8b and tip (same blob ids). R56.4: hashing exact git-show bytes confirms all 13 SOURCES and 6 QUALITY mislabeled digests equal 877eedee referents (`R56.4-digest-check.txt`). R54.10: the two committed controls really say 0/7 and 0/30; SCORECARD explicitly corrects their pairing. R55.7: declined matches the spot-check's explicit not-lane-debt ownership; historical contamination cannot be experimentally reconstructed now.

LSP unavailable: reading `xd://lsp` returned `No such tool`; semantic references/definitions/diagnostics could not be requested. Fallback is object/diff inspection, not claimed semantic-server proof. No complete C1/C2 counter, controls script, cold-read/no-harm monitor, selftest or deciding run was executed. No saturation, same-identity routing, or resume-path claim is made; those are outside these ledger rows. No installs or upgrades. Scratch cleaned after receipts captured.

Self-evaluation: accuracy 4/5 (R56.3 superseding-entry interpretation remains contestable); completeness 4/5 (all 13 rows reviewed, no full controls execution claimed); clarity 4/5 (receipt index is needed for complete outputs); actionability 5/5 (per-row replacement commits/locations supplied); conciseness 4/5 (evidence required a longer report). Overall 4.2/5. Highest-impact improvement is an L1 decision on R56.3's additive-entry reading, not another status guess. User agreement expected with the explicitly bounded execution claims.
