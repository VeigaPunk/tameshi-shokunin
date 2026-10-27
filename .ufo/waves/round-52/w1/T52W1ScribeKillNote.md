# T52W1ScribeKillNote — C2 m5 supersession line (round 52, wave 1)

- Seat: `T52W1ScribeKillNote` (scribe, leaf; no subagents). Item: draft the C2 m5
  supersession line for `corpus/knowledge/fleet-kill-rate-ledger.md`, name its
  insertion point, and check that no other §3 cell contradicts recorded cases 1–10.
- Read-only on the lane: this seat wrote only this report and the receipt files
  beside it under `.ufo/waves/round-52/w1/`. No lane file, index or jj state was
  touched (`git status --porcelain` before and after shows the same set:
  `M SCORECARD.md`, `M SKILL.md`, `M corpus/knowledge/fleet-kill-rate-ledger.md`,
  `M tools/registry.json`, `M tools/round21-measure.py`, `?? .ufo/evidence/round-52/integrate/`,
  `?? .ufo/waves/round-52/`).
- The frozen rule I drafted against is `measure.py` m5, read at the freeze digest
  (`2c771d768e692811f7a39135800d27fbdb6403f4d12d46289bff404ee6ba9fbd`, equal to
  `git show acc27abe:.ufo/evidence/round-52/c2/measure.py | sha256sum`):

  ```python
  idx = [i for i, ln in enumerate(led) if ln == DRIFT_ROW]
  sup = [ln for ln in led[idx[0] + 1:]] if len(idx) == 1 else []
  ok = any('drift-pins' in ln and 'unmeasured by sweep' in ln and 'supersed' in ln.lower() and 'case 10' in ln
           for ln in sup)
  ```

  with `DRIFT_ROW = '| drift-pins | 13 | `c138d34c7f0dfe95` | unmeasured by sweep; hermetic |'`
  (`.ufo/evidence/round-52/c2/measure.py:30`, `:201-206`).

## 1. Deliverable — the exact line

One physical line (1,125 chars):

```text
- **§3 supersession (cell, not edit; round-8 precedent `:280`).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`) as recorded case 10: `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (`.ufo/evidence/round-51/c2/sweep/sweep.txt:31`), wired as the runner's tenth leg (`C2_LEG bash-drift-pins: WIRED`, `.ufo/evidence/round-51/after/c2.stdout:10`; `REGRESSION: PASS (cases=10 passed=10 …)`, `:22`); entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`. That case 10 measurement supersedes the cell; §3’s table stays as written. Three of the eight survivors (`K_GONE_ARM`, `K_AMBIG_GT`, `K_SHAPE_OPTIN`) are `oracle-leak` artifacts — the defect-id sandbox path satisfied the gate’s unanchored verdict-word grep (`corpus/lessons/round-51.md:34`; confirmed, `.ufo/waves/round-51/w1/T51LabSandboxLeak.md:95-102`, neutral-sandbox counter-run reads 5/10) — so the recorded 2/10 is what the sweep measured, not the suite’s detecting power. Routed by the round-51 spot-check, defect 7.
```

**Insertion point — append at file end, after `:437`.** The base file ends at
`:437` (`did not drain the service queue.`). Append exactly four lines and move
nothing: one blank line, the heading `## Round 52 — §3 drift-pins cell superseded (2026-10-27)`,
one blank line, the bullet above. In the current lane working tree that block
already sits at `:438-441` (`git diff -- corpus/knowledge/fleet-kill-rate-ledger.md`
→ `@@ -435,3 +435,7 @@`, `4 insertions(+)`, `0 deletions`); landing this line means
replacing only the bullet at `:441`.

Placement rationale (two admissible positions, one chosen):

- m5 accepts any line after the unique `:119` row (`measure.py` `idx[0] + 1:`), so
  both "end of the section holding `:280`" and "file end" qualify.
- File end is chosen because this file appends per-round blocks at the end
  (`## Round 16` `:403`, `## Round 18` `:424`) and never edits above; inserting
  into ER-2 after `:283` would put a round-52 note ahead of the round-16/18
  blocks and break the chronology the file already keeps.
- Verified in the scratch probe (below): the appended block keeps the `:119` row
  byte-identical and unique — `drift_row_matches 1 at [119]`, `drift_row_bytes_ok True`
  (`T52W1ScribeKillNote.tokens.txt`).

## 2. Clause-by-clause grounding

| clause in the line | evidence (file:line) | command that shows it |
|---|---|---|
| row `:119` said "unmeasured by sweep" | `corpus/knowledge/fleet-kill-rate-ledger.md:119` | `python3 -c "…l==DRIFT_ROW…"` → `matches 1` (`tokens.txt`); `sed -n '119p' …` |
| kagi `corpus/drift-pins.sh` @ `e64e81b8`, blob `c138d34c…` | kagi commit blob | `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh \| sha256sum` → `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb` |
| sweep receipt line | `.ufo/evidence/round-51/c2/sweep/sweep.txt:31` | `grep -n 'MUTATE: DONE' …` → `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (verbatim) |
| suite of 13 at the pin (matches §3's Suite column) | `sweep.txt:6` | `sed -n '6p'` → `  \| DRIFT_SELFTEST: PASS (13 cases)` |
| wired as the tenth leg | `.ufo/evidence/round-51/after/c2.stdout:10` | `sed -n '10p'` → `C2_LEG bash-drift-pins: WIRED` (tenth of ten `C2_LEG` lines, `:1-10`) |
| runner regression over ten legs | `after/c2.stdout:22` | `sed -n '22p'` → `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)` |
| recorded case 10 entry | `corpus/knowledge/mutation-case-kagi-drift-pins.md:8` (`# Mutation case 10 …`), `:14-16` (pin + recheck) | `sed -n '8p;14,16p' …` |
| three survivors are `oracle-leak` artifacts, named | `corpus/lessons/round-51.md:34` (class row); `sweep.txt:10,12,17` (`K_GONE_ARM`, `K_AMBIG_GT`, `K_SHAPE_OPTIN` `SURVIVED`) | `sed -n '34p' corpus/lessons/round-51.md`; `grep -n 'K_GONE_ARM\|K_AMBIG_GT\|K_SHAPE_OPTIN' sweep.txt` |
| confirmation, neutral counter-run 5/10 | `.ufo/waves/round-51/w1/T51LabSandboxLeak.md:63` ("not falsified — it is confirmed"), `:95-102` (verdict: flips exactly the three, neutral 2/10 → 5/10), `:120` (3/3 repeats) | `sed -n '63p;95,102p;120p' …` |
| routed by the round-51 spot-check, defect 7 | `corpus/lessons/round-51-verifier-spotcheck.md:132` ("Append a supersession note pointing at case 10, following the round-8 precedent at `:280`") | `sed -n '132p' …` |

Wording notes (calibration):

- "said \"unmeasured by sweep\"" quotes the cell as written; the line asserts the
  supersession, not a rewrite of the cell — same shape as the round-8 precedent
  `:280` ("said \"unmeasured by sweep\"; rows 5/6 are the measurements that
  supersede those cells — §3's tables stay as written").
- The masking sentence names the three mutants and cites the confirmation report
  rather than the case entry, because the entry's own standing paragraph still
  says the finding "had not published" (finding F4). The 5/10 figure is the
  executed neutral counter-run in that report, not a projection.
- "wired as the runner's tenth leg" is sourced to `C2_LEG …:10` + `cases=10` at
  `:22`; both are receipt lines, not inferred.

## 3. Frozen-rule check (probe, not a verdict)

Scratch: `/fast/scratch/hyaku/tameshi-r52/T52W1ScribeKillNote` (deleted after
the run), one `git clone --shared` of the lane
(`git -C "$S/clone" rev-parse --show-toplevel` → `$S/clone`, HEAD `1f72d7d8`).
Frozen counter run with `--lane "$S/clone" --rev HEAD --explain`:

- before the block: `C2_CHECK m5 MISMATCH row=1 note=False` /
  `C2_R52: … m1=2 m2=1 m3=3 m4=20 m5=1 m6=0 total=27 C2_R52_PASS=false`
  (`T52W1ScribeKillNote.m5-before.txt`) — the contract's BASE reading reproduced
  exactly.
- after appending the four lines and committing in the clone:
  `C2_CHECK m5 ok row=1 note=True` / `m5=0` (`T52W1ScribeKillNote.m5-after.txt`).
  The other m-values stay at base there only because that clone lacks the round's
  other edits; **this is a rule-shape probe, not a claim verdict.** The deciding
  run is the L1's.

Frozen counter selftest also run as observed: `python3 …/c2/measure.py --selftest`
→ `C2_SELFTEST: cases=8 failed=0`.

## 4. §3 cell check against recorded cases 1–10

`T52W1ScribeKillNote.cells.txt` (generated from `corpus/knowledge/fleet-kill-rate-ledger.md`)
maps every §3 row to its case:

| §3 row | cell state (present tense) | recorded case | verdict |
|---|---|---|---|
| `:107` cite-check | "**probe only, 1/4** (§2); full sweep open" | case 9 (`mutation-case-kumitate-cite-check.md:44`, same pin `40573448…`, suite 62) | **CONTRADICTED** (F1) |
| `:108` surface-probe | "unmeasured; hermetic" | none in 1–10 | consistent |
| `:109` round-gate | "unmeasured; hermetic" | case 7 (`fleet-kill-rate-ledger.md:410`, same pin `f890e277…`, suite 60) | **CONTRADICTED** (F2) |
| `:110` proxy-check | "unmeasured; hermetic; expect low survivor count" | none | consistent |
| `:111` claims-check | "unmeasured; hermetic; …" | case 6 (ledger `:277`) | superseded at `:280` — consistent |
| `:119` drift-pins | "unmeasured by sweep; hermetic" | case 10 (`sweep.txt:31`) | superseded by this line — consistent |
| `:120` op-ref-probe | "unmeasured by sweep; hermetic" | none | consistent |
| `:121` checklist-run | "unmeasured by sweep; hermetic" | case 5 (ledger `:276`) | superseded at `:280` — consistent |
| `:122` scope-gate | "unmeasured by sweep; self-attack 16/18 (§2); F-1 open" | none | consistent |
| `:123` claim-ledger | "unmeasured by sweep; F-2 …" | none | consistent |
| — | case 8 sources-check | — | not a §3 row; ledger `:426-427` says so |

Answer to the item's check: after this line, **two other §3 cells still
contradict recorded cases** — they pre-date round 52, are not created or touched
by this line, and m5 does not bind them. Reported as findings, not fixed here.

## 5. Findings

**F1 — §3 `:107` cite-check cell is false against case 9.**
`corpus/knowledge/fleet-kill-rate-ledger.md:107` reads "**probe only, 1/4** (§2);
full sweep open — hermetic 62-case run on a copy"; case 9 is that full sweep, at
the same pin and suite size: `corpus/knowledge/mutation-case-kumitate-cite-check.md:44`
→ `## 2. Result — 5/10 killed (50 %), 10/10 verdict predictions held`, with
`recheck: … REGRESSION_CASE js-cite-check` at `:3` and the runner receipt
`.ufo/evidence/round-51/after/c2.stdout:20` → `REGRESSION_CASE js-cite-check: PASS`.
The ledger carries no append block and no supersession for case 9:
`grep -n 'ninth\|Round 26\|case 9' corpus/knowledge/fleet-kill-rate-ledger.md`
→ no output. Show it: `sed -n '107p' corpus/knowledge/fleet-kill-rate-ledger.md;
sed -n '44p' corpus/knowledge/mutation-case-kumitate-cite-check.md`.

**F2 — §3 `:109` round-gate cell is false against case 7.**
`:109` reads "unmeasured; hermetic"; the ledger's own case-7 row at `:410` reads
`| kumitate scripts/round-gate.mjs (leg js-round-gate) | … | **5/10 (50 %)** … |`,
detail `mutation-case-kumitate-round-gate.md:50`. The Round-16 block does
acknowledge the row — `:414-418` ("the queue row that said `unmeasured` is this
file's §3 (`:109`)") — but that paragraph corrects the block's own "§5" label; it
does not supersede the cell, so a reader of §3 alone still reads "unmeasured".
Show it: `sed -n '109p;410p;414,418p' corpus/knowledge/fleet-kill-rate-ledger.md`.

**F3 — §2 `:94` cite-check probe row is stale for the same reason as F1.**
`:94` reads "a probe, **not a sweep** … the queue's head is now 'probed only'";
case 9 is a sweep with composition, at the cell's own pin (`40573448…`). §2 is
outside m5's surface; recorded because §3 `:107` points the reader at it ("(§2)"),
so the two stale statements reinforce each other. Show it:
`sed -n '94p' corpus/knowledge/fleet-kill-rate-ledger.md`.

**F4 — the case-10 entry's standing paragraph is stale against the published
confirmation.** `corpus/knowledge/mutation-case-kagi-drift-pins.md:19` and
`:126-130` say the sandbox-leak finding "still await[s] the named confirmation
seat" / "had not published when this entry was drafted … owes its independent
confirmation"; `.ufo/waves/round-51/w1/T51LabSandboxLeak.md:63` says "The
hypothesis was not falsified — it is confirmed" and `:95-102` records the verdict
(3/3 repeats, neutral 2/10 → 5/10). The drafted line cites the confirmation, not
the entry's standing paragraph; the entry itself is a follow-up, outside m5.
Show it: `sed -n '19p;126,130p' corpus/knowledge/mutation-case-kagi-drift-pins.md;
sed -n '63p;95,102p' .ufo/waves/round-51/w1/T51LabSandboxLeak.md`.

**F5 — §3 preamble counts are stale prose (not cells).** `:100-101`
("Kumitate's five unmeasured … unchanged") and `:114-115` ("Kagi's five
unmeasured") now overstate the queue for kumitate (cases 6, 7, 9) and kagi
(cases 5, 10). m5 binds the cell only; noted so a future editor does not treat
the preamble as a cell that the round-8 precedent protects.

**F6 — the lane working tree already holds a different, uncommitted variant of
this line.** `corpus/knowledge/fleet-kill-rate-ledger.md:441` (869 chars) already
contains a drift-pins supersession bullet that also satisfies the frozen rule —
observed, not inferred: a second scratch clone carried those four lines verbatim
and the frozen counter read `C2_CHECK m5 ok row=1 note=True`
(`T52W1ScribeKillNote.m5-worktree-variant.txt`). But it cites only
`corpus/lessons/round-51.md`, does not name the three survivors, and does not
cite the confirmation report. No wave-1 registry item names the ledger
edit (`python3 … swarm-registry.json` over items containing `ledger` /
`kill-rate` → only the 20 cold-read correction seats and this seat), so its author
is not identified in the registry. Action for the L1: land exactly one bullet —
replace `:441` with the line in §1 (nothing else moves).

## 6. Bounds, tooling, artifacts

- No tool installed or upgraded (pacman paused per host rule; nothing needed).
- Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1ScribeKillNote` removed after the
  probe; no `/tmp` usage beyond nothing; receipts are the wave-dir copies below.
- Receipts: `T52W1ScribeKillNote.m5-before.txt`, `.m5-after.txt`,
  `.m5-worktree-variant.txt`, `.cells.txt`, `.tokens.txt`, `.final-line.txt`
  (all in `.ufo/waves/round-52/w1/`).
- Not decided here: C2 itself. The probe shows the m5 rule flips; whether the
  claim passes belongs to the L1's deciding run at the content revision.

## Summary

- Delivered the m5 line (1,125 chars) and its insertion point: appended as a new
  `## Round 52` block after `:437`, nothing moved; the working tree already holds
  a weaker 869-char variant at `:441` that should be replaced, not doubled.
- Every clause is sourced: `sweep.txt:3,6,31`, `after/c2.stdout:10,22`,
  `mutation-case-kagi-drift-pins.md:8,14-16`, `round-51.md:34`,
  `T51LabSandboxLeak.md:63,95-102`, spot-check `:132`; the kagi blob sha was
  re-derived from the kagi repo and matches `c138d34c…`.
- Probe in a scratch clone: `m5 MISMATCH` before, `m5 ok` after; frozen selftest
  8/8. Probe, not a verdict.
- `:119` stays byte-identical and unique; the append is 4 insertions, 0 deletions.
- §3 check: no cell contradicts cases 1–10 *after* this line except two
  pre-existing ones — `:107` cite-check (case 9, 5/10) and `:109` round-gate
  (case 7, 5/10) — plus the stale §2 `:94` probe row and the entry's standing
  paragraph; all reported with commands, none edited.
- Lane untouched; receipts and this report are the only writes.
