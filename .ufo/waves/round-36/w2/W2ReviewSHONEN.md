# W2ReviewSHONEN — per-box falsification of the round-36 report's SHONEN section

Seat: reviewer (calibration), round 36 wave 2, leaf — read-only, no dispatch.
Attacked: `## SHONEN` in `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tameshi.md`
(lines 123–128; report bytes `1392a440756d2d0081189c9b5f34e5c708c80a4a57e8eeceb1553712744132a5`
= fleet commit `f4ef953`). Criteria applied: (a) every `[~]` pointer resolves at the
refresh commit, (b) no box carries `[x]` without a named non-author verifier.

## Revisions

- Refresh commit under test: `b455001e2589b3f4f471d94a3de7e5e549b9f54c` (contract C1 `after`)
- Lane tip: `fbb01cf46f8437fd1264c1a3acc053c882fa2164`; receipts tip `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`
- Content commit (control): `e423c41ba253357ab8c8513f0376dad9d38ab248`
- Before baseline: `796e08b888849308d0c4d5e932e56833600a139f`
- `SHONEN.md` sha256 `55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09` at all five revisions.

## Commands run (from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless noted)

1. `git show <REV>:SHONEN.md | sha256sum` for `796e08b e423c41 b455001 d9c496b fbb01cf` — identical sha; `git diff 796e08b..fbb01cf -- SHONEN.md` empty.
2. `git show <REV>:SHONEN.md | python3 -c '...^- \[([x~ ])\] ...'` (SCORECARD command C verbatim) at `b455001`, `HEAD` — both `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`.
3. `git show b455001:SHONEN.md | grep -nE '^- \['` — four `[~]` box lines (5, 7, 9, 11); no `[x]` anywhere (`grep "\[x\]"` exit 1).
4. `git cat-file -e b455001:<path>` for `reports/round-1-calibration.md`, `.ufo/evidence/round-21/coldread/ledger.json`, `PROVINCE.md`, `LOG.md`, `tools/tally-audit-v3.py` — all exist.
5. `git show b455001:reports/round-1-calibration.md | grep -n '^## box-'` — `## box-1` :71, `## box-2` :105, `## box-3` :132, `## box-4` :167 (one match each for 1/2/4).
6. `git show b455001:.ufo/evidence/round-21/coldread/ledger.json | python3` — valid JSON, `entries`=497, sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf` (same at HEAD).
7. `sed -n '123,128p' .ufo/reports/round-36/tameshi.md | python3` (from fleet root) — `bullets=4 marks=['~','~','~','~']`; `grep "\[x\]"` on the report = no match.
8. `grep -n '"shonen"' -A12 .ufo/evidence/round-36/after/monitor-at-{796e08b,b455001e}.stdout` and `control/monitor-at-e423c41b.stdout` — per-box fields quoted below.
9. Read-only source inspection: `.ufo/evidence/round-21/coldread/measure.py:17-18,111` (loads and configures the round-18 credit implementation), `.ufo/evidence/round-18/measure.py:679-683` (credit composition).
10. `git show b455001:LOG.md | grep -n '^## Round 3[4-6]'` — `## Round 34` :1820, `## Round 35` :1848, `## Round 36` :1898.
11. `git show b455001:tools/tally-audit-v3.py | sha256sum` — `6188db16…` = frozen pin (so box-4's "not absorbed" claim holds literally).

## Per-box result

| Box | Report mark (line) | SHONEN.md @ b455001 | Pointer(s) resolve @ b455001 | `[x]` w/o named non-author verifier | Result |
|---|---|---|---|---|---|
| 1 | `[~]` (125) | `[~]` (SHONEN.md:5) | yes: `reports/round-1-calibration.md#box-1` (`## box-1` :71) and `.ufo/evidence/round-21/coldread/ledger.json` (valid, 497 entries) | none (no `[x]`) | pointer criterion PASS; per-box claim falsified (F1) |
| 2 | `[~]` (126) | `[~]` (:7) | yes: `reports/round-1-calibration.md#box-2` (`## box-2` :105) | none | PASS; wording note (F3) |
| 3 | `[~]` (127) | `[~]` (:9) | yes: `.ufo/evidence/round-21/coldread/ledger.json` | none | pointer criterion PASS; "unchanged" falsified (F1); stale cross-reference (F2) |
| 4 | `[~]` (128) | `[~]` (:11) | yes: `reports/round-1-calibration.md#box-4` (`## box-4` :167) | none | PASS |

Pointer-anchor semantics: each target heading is `## box-N`, so the GitHub slug `#box-N` matches
(one occurrence each at the lines above). No pointer points at a `/tmp`, session-local or
untracked artifact.

## Findings by severity

### F1 — MEDIUM (calibration): the round's 64/64 credit is attributed to box 1, and box 3's credit change is reported as "unchanged"

Report line 125 (box 1) says "cold-read monitor credits 64/64 sections at the refresh commit"
and appends `.ufo/evidence/round-21/coldread/ledger.json`; report line 127 (box 3) says
"unchanged". The monitor's own per-box logic contradicts that placement:

- `.ufo/evidence/round-18/measure.py:679-683` (implementation loaded by
  `.ufo/evidence/round-21/coldread/measure.py:17-18`; box-3 link set at `:111`):
  `box3_points = box3_marked and box3_link and cr['box3_full_page']`;
  `restraint = 2*sum(mark~ for box in (1,2,4)) + 2*box3_points`.
  Boxes 1/2/4 earn 2 points on the mark alone; the monitor never reads box 1's evidence link.
  `box3_full_page` (`sections_covered == sections_total`) gates **box 3 only**.
- Receipts: before `after/monitor-at-796e08b.stdout:2` score 6, `:4` `box3_full_page:false`,
  `:1791` `sections_covered:60`, `:1829` `box3_points:false`. Control
  `control/monitor-at-e423c41b.stdout:2,4,1829` identical. After
  `after/monitor-at-b455001e.stdout:2` score 8, `:4` `box3_full_page:true`, `:1766`
  `sections_covered:64`, `:1799` `box3_points:true`.
- Therefore the only per-box credit delta this round is box 3: 0 → 2 points (6 → 8 total).
  Box 1's credit is unchanged (2 → 2), and the ledger is box 3's required link, not box-1
  evidence. The box-1 bullet carries box-3's evidence pointer and box-3's coverage number;
  the box-3 bullet calls the one box that moved "unchanged" and omits the 64/64 restoration
  that produced its two points.
- Charitable reading: "cold-read monitor credits 64/64 sections" could be a global statement
  placed in the bullet, not a box-1-specific claim. Even so, in a per-box section it reads as
  box-1 support, and the corresponding box-3 statement is factually wrong about the credited
  state. The C1 numeric claim itself (8, 64/64) is unaffected and matches the receipts.

### F2 — LOW/MEDIUM (stale, unlinked evidence): box 3's canonical audit section still records `[ ]` rejection

`reports/round-1-calibration.md` at `b455001` (sha `fc46d59d…`, unchanged since `cd31c6b`;
same sha at HEAD) says under `## box-3` (:132): "Why `[ ]` — no lane assertion at all"
(:159) and "Box 3's two points and the separate independent-review two points remain
unearned" (:165); its dispositions table (:208) records box 3 as `[ ] (assertion rejected)`.
No errata in that file supersedes it. The current `[~]` is legitimately supported by the
input-keyed monitor (mark + ledger link + full page → `box3_points:true`), and the round-36
report correctly points box 3 at the ledger, not at `#box-3` — so this is not a pointer
failure. But a reader following the box-3 trail inside the same audit file sees the opposite
verdict; the file needs an append-only errata or a re-point note.

### F3 — LOW (wording): box 2 bullet describes audit rounds, not the end-to-end task

Line 126 says "rounds 34–36 capability/audit work logged in LOG.md". The LOG headings do
exist at `b455001` (:1820, :1848, :1898), so the claim resolves, and the pointer
`#box-2` does document the round-3 kagi census as the end-to-end task. But the bullet's own
description substitutes ongoing capability/audit rounds for the canonical row ("at least one
end-to-end domain task executed"). The `[~]` remains supported by the pointer target; this is
a wording overreach, not a mark/pointer failure.

### F4 — RESIDUAL RISK (convention, not a defect): pointer base is the lane root, not the report's directory

The report is committed in the fleet repo (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tameshi.md`),
where `reports/` is empty and `.ufo/evidence/` does not exist; all four pointers resolve only
lane-root-relative at `b455001`. The round-35 report used the same lane-relative convention, so
this is consistent with lane practice, but the report never names the lane root, so a standalone
fleet reader gets dead links.

## Checks that passed

- All four `[~]` pointers resolve at `b455001` (paths exist; anchors `box-1`/`box-2`/`box-4`
  each match once; ledger is valid JSON, 497 entries, sha `29bddc03…`).
- Zero `[x]` in the report's SHONEN section and zero `[x]` in `SHONEN.md` at `b455001`; the
  census reads `checked=0 asserted=4`. The "[x] needs a named non-author verifier" condition is
  therefore vacuously satisfied, and the historical `[x]` marks described in the pointer targets
  name TAMESHI-B1/B2/B3 *as lane-dispatched, explicitly not independent* — correctly downgraded
  to `[~]`.
- `SHONEN.md` is byte-identical across `796e08b..fbb01cf`, so no box was silently flipped this
  round and no mark drift exists behind the report's "unchanged" claims (true of the file/mark,
  false of box 3's credited state — F1).
- Box 4's "deferred to round 37, not absorbed" holds: `tools/tally-audit-v3.py` at `b455001`
  still hashes to the frozen `6188db16…`; `contract.json` records the deferral.
- Pointer-target statements match the bullets' "no independent promotion verifier" parentheticals
  (`#box-1` :100-102, `#box-2` :127-129, `#box-4` :190).

## Residual risk and verification gaps

- The report's SHONEN section is a paraphrase of `SHONEN.md`, not the canonical checklist; my
  checks bind to the lane `SHONEN.md`/pointer targets at `b455001`, not to report wording as an
  independent claim source.
- I did not re-run the cold-read monitor (that is C1's seat); F1 rests on the committed receipts
  and the credit algorithm's per-box fields, which name `box3_points`/`box3_full_page`
  explicitly.
- Box-2's "end-to-end" characterization and box-3's stale `#box-3` section are documentation
  issues; neither breaks a pointer or a mark.

## Verdict

**PASS on the two stated criteria, per box:** all four `[~]` pointers resolve at refresh commit
`b455001e`; no box carries `[x]` (so no unnamed non-author verifier is claimed). **F1 stands as a
medium calibration defect**: the report's per-box SHONEN attribution assigns the round's 64/64
coverage credit to box 1 and calls box 3 "unchanged", while the monitor's own fields show box 3
is the only box whose credit moved (0 → 2, `box3_points` false → true). All four boxes pass the
pointer test; box 4 passes cleanly, box 2 carries only the wording note (F3), box 1 carries the
misattributed coverage/ledger pointer, and box 3's "unchanged" is false for the credited state.
