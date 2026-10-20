# V01R16RunnerBreak — how round-16 commits c699c8c and 05a2247 broke the round-14 disposition gate, and why the L1 called it "by design"

Scope: reconstruction only, committed bytes only. Baseline `28aeef4` (round-15
spot-check, 2026-10-20T06:00:06-03:00), wave-1 `c699c8c` (10:49:37-03:00),
wave-2 `05a2247` (11:18:08-03:00), lane tip `98bea7d`. All lane bytes read with
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <rev>:<path>`;
every execution ran in a `/tmp` fleet-mirror clone (siblings symlinked) or a
`git archive` extraction. The live lane worktree was not executed against or
modified; no tools were installed or updated.

## 1. Timeline (commit / time / path:line / event)

| Time (-03:00) | Rev | Path:line | Event |
|---|---|---|---|
| 2026-10-20T06:00:06 | `28aeef4` | `tools/mutate-and-run.sh` | Last round-15 commit; runner bytes sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` (last actual edit was `606716f`, round 10). |
| 06:00:06 | `28aeef4` | `.ufo/evidence/round-13/expected.json:12` | Pin `inputs["tools/mutate-and-run.sh"] = 75ed934d…adc5` still matches live bytes. Entry command `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` → **exit 0 clean**, counts `{effective:11, superseded:1, passed:11, failed:0}` (I re-ran it from a `git archive 28aeef4` extraction). |
| 10:49:37 | `c699c8c` | `tools/mutate-and-run.sh:15,91,562-563,570,899-962,1219-1223,1225-1226` | +108/−24: adds leg 7 `js-round-gate` — header/leg table (`:15`, `:91`), `PIN_ROUNDGATE`/`REV_ROUNDGATE` (`:562-563`), `TABLE_ROUNDGATE` (`:570`), the 64-line embedded spec heredoc (`:899-962`), the `regression_case_git js-round-gate` call (`:1219-1223`), `nlegs=7` (`:1226`). New whole-file sha256 `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594`. |
| 10:49:37 | `c699c8c` | `.ufo/evidence/round-13/expected.json:12` | Unchanged. Gate at this rev: **exit 2** `expected_input_digest_mismatch`, `observed 89722ddb… expects 75ed934d…`. `SKILL.md:1681` (active round-15 registry row) still states `--root .` → `0 clean`. |
| 11:18:08 | `05a2247` | `tools/mutate-and-run.sh:1661-1670,1680-1681` (+ comment hunks at `:95-103`, `:547-548`) | +19/−6: leg-count agreement selftest (call sites/spec files/`nlegs`/tuples must all be 7). New whole-file sha256 `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa` — still not the pinned `75ed934d`. Gate remains **exit 2**. |
| 11:18:08 | `05a2247` | `SKILL.md:1681`, `SKILL.md:1736` (errata row; `:1741` at tip) | The L1 rewrites the active disposition row: "(since round 16 the runner input moved, so `--root .` returns 2 `expected_input_digest_mismatch` **by design**; use `--root` on `git archive 28aeef4` extracted to /tmp → 0 clean)" and appends the errata row "`--root .` → 2 … by design; run on `git archive 28aeef4` → 0". `git log -S "since round 16 the runner input moved"` → only `05a2247`. |
| 11:18:08 | `05a2247` | `corpus/lessons/round-16.md:63` | Mistakes row: class `reference-drift`; "captured-by: **the gate itself (by design)**"; fix: "Correct fail-closed behaviour. The registry row now names the archived-root invocation". |
| 11:31:50 | `3490708` | `SKILL.md:1741`; `w3/RX5.md`, `w3/RX6.md` | Errata attribution becomes "RR10 (w2)"; the wave-3 re-read reports land. |
| 11:46:02 | `09ee1d0` | `w3/RX9.md:58`; `.ufo/evidence/round-16/coldread/ledger.json` | Final page `906fb649…`; ledger merges the re-reads (below). |
| 11:48:34 | fleet `a067c63` | `.ufo/reports/round-16/tameshi.md:90` | L1's own final wording: "coverage, operability, freshness and adjacency are unchanged. One note on operability: the round-14 disposition gate now exits 2 at `--root .`, **by design**, because its pinned runner input moved. Its archived-root form exits 0 (RR10, RX5)." |
| (tip) | `98bea7d` | `tools/mutate-and-run.sh`, `expected.json:12` | Gate still **exit 2**; runner `0673d2e5…`; not re-pinned anywhere (`.ufo/evidence/round-16` holds no dispositions/expected file: `git ls-tree -r 017a2b0 .ufo/evidence/round-16 | grep -Ei 'dispos|expected'` → empty). |

## 2. The break, mechanically

The pin chain (all lane-relative):

1. `.ufo/evidence/round-14/dispositions.json:3` — `"expected_file": ".ufo/evidence/round-13/expected.json"`.
2. `.ufo/evidence/round-14/dispositions.json:4-8` — pins the expected file and two receipts:
   `a0160794…` (expected.json), `a02718e9…` (verification.json), `df83a729…` (producer-oracle-repair.json).
3. `.ufo/evidence/round-13/expected.json:12` — pins `tools/mutate-and-run.sh` at `75ed934d…`.
4. `tools/evidence-disposition.py:1184-1191` — "INTEGRITY FIRST": every `expected.inputs` digest is verified against the **live tree** before any row predicate runs; a mismatch raises `CouldNotEvaluate("expected_input_digest_mismatch")` with the observed/expected pair.

The gate tool itself is byte-identical at every rev in this range (`sha256
1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95` at
`28aeef4`, `c699c8c`, `05a2247`, `98bea7d`), so nothing in the checker changed —
only the instrument it pins.

Consequence: because the pin is a **whole-file digest of a lane instrument**, any
additive edit to `tools/mutate-and-run.sh` guarantees the round-14 gate returns 2
at `--root .`. That is exactly what `c699c8c` did (leg 7), and what `05a2247` did
again (leg-count check). The tool was behaving correctly; the pin was not
maintained. The gate cannot distinguish this by-design mismatch from tampering
(the same exit-2 class covers both), which is why the archived-root recipe was
introduced — and why that recipe grades a frozen commit, not the tree it ships in.

Verified at tip:
`python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
→ exit 2,
`{"id":"expected_input_digest_mismatch","status":"could_not_evaluate","detail":"tools/mutate-and-run.sh: observed 0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa expects 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5"}`.

## 3. Which seats observed it

| Seat | Page rev | Verdict on section 1676 | Evidence |
|---|---|---|---|
| **RR10** (w2) | page sha `3d8a1edb…` (`SKILL.md` at `c699c8c`) | **`gap-blocking`** — one blocking gap: "evidence-disposition entry command yields exit2 expected_input_digest_mismatch at c699c8c: … observed 89722ddb… vs expected.inputs pin 75ed934d… — wave-1 commit c699c8c edited a gate-pinned input without re-pinning round-13 expected.json/dispositions.json; registry row '0 clean' unreachable until re-pinned" | `w2/RR10.md:11-13, 40-46, 51-66`; machine block `:81`; remediation "re-pin `inputs[tools/mutate-and-run.sh]` … or supersede the pin in dispositions" at `:64-66` |
| **RX5** (w3) | page sha `e289acec…` (`05a2247`) | **`executed-ok`, no gaps** — reproduced exit 2 with `observed 0673d2e5… expects 75ed934d…`, and archived `28aeef4` → exit 0; accepted both as "the two special forms the registry now spells out (`--root .` → exit 2 … **by design**; archived `28aeef4` root → exit 0 clean)" | `w3/RX5.md:44, 94-96, 113` |
| **RX6** (w3) | `05a2247` | row-by-row errata re-anchor; the disposition row "verified" (`observed 0673d2e5… expects 75ed934d…`; archived → exit 0) | `w3/RX6.md:40` |
| **RX9** (w3) | `05a2247`/`3490708` | same row "verified"; exit 2 at lane, exit 0 on extracted `28aeef4` | `w3/RX9.md:58` |
| ToolsNoHarm (w2 monitor) | `c699c8c` | ran **nine selftests only** (`evidence-disposition.py --selftest` 34/34, `pin-disposition.py --selftest` 18/18, …); never the registered entry command | `w2/ToolsNoHarm.md:15-25, 35-37` |

So four seats executed the gate; only RR10 treated the red entry command as a
defect. Crucially, RR10's blocking verdict is attached to the **old section text
sha `7544ca69…`**. `05a2247` rewrote that section, and RX5 re-read the **new text
sha `f6cdac5b…`** as `executed-ok`. The final page (`017a2b0` / `906fb649…`) has
section 1676 at exactly `f6cdac5b…` (I recomputed with `measure.py`'s
`sectionize` on the committed `SKILL.md`), so the credit follows the by-design
text; RR10's `gap-blocking` stays in the ledger on a sha no longer on the page.

Ledger proof (`.ufo/evidence/round-16/coldread/ledger.json` at `017a2b0`):

- `97cf436b…`, start 1676, verdict `gap-blocking`, blocking_gaps 1, text sha `7544ca69…`, seats `[CR27, RR10]`;
- `e289acec…`, start 1676, verdict `executed-ok`, gaps 0, text sha `f6cdac5b…`, seat `[RX5]`;
- final-page `906fb649…` section 1676 text sha = `f6cdac5b…` → credited by RX5's entry.

That is the same sha-only hole as the round-14 reconciliation bucket
(`e8720037…`, credited by CR26 at runner `75ed934d` though the bucket's step 3 is
red at the landed runner) — the non-author spot-check's C2 failure
(`corpus/lessons/round-16-verifier-spotcheck.md:94-130, 216-222`).

## 4. Why "by design" instead of re-pinning

The L1's recorded reasoning is concentrated in three places:

- `corpus/lessons/round-16.md:63` — class `reference-drift`, captured-by "**the gate itself (by design)**", fix "Correct fail-closed behaviour."
- `SKILL.md:1681` + `:1741` — the row now teaches the failure as intended and substitutes the archived-root recipe.
- fleet `.ufo/reports/round-16/tameshi.md:90` — same sentence, plus "operability … unchanged".

Sequencing: `w2/RR10.md` is first added in `05a2247` itself (`git log
--diff-filter=A -1`), the same commit that rewrites `SKILL.md:1681` — the L1
landed the gap-blocking finding and the by-design relabel together.

The inference chain that produced it (reconstructed; the first step is verified,
the leap is the mistake):

1. The gate is correct to refuse a changed input (true — fail-closed is the
   tool's contract).
2. The runner change was intentional (true — leg 7 and the leg-count check).
3. Therefore the exit 2 is "by design" — **false step**: it is the expected
   consequence of an intentional edit only if "expected" means "predicted", not
   "acceptable". The registry's own verdict map still classes exit 2 as
   could-not-evaluate for "invalid, missing or tampered inputs"; calling the same
   exit "by design" in the entry-command cell makes the row and its verdict map
   disagree.
4. The archived-root run proves the gate still works and the historical evidence
   is intact (true), so no re-pin is needed — **false step**: that run grades
   `28aeef4`, not the branch tip, and leaves the registered entry command
   red-capable at the rev that publishes the row.

The lane's own rule forbids exactly this move: "A moved pin is never
re-interpreted against the new bytes" / "A moved substrate needs a re-pin, never
a re-interpretation of the old table" (`SKILL.md:1083-1084`, `:811-812`,
`:1260`; `corpus/knowledge/service-optin-protocol.md:60-62`). The registry edit
is a re-interpretation of the moved pin, not a re-pin. The spot-check states the
same in one line: "**'By design' holds for the gate's fail-closed behaviour, not
for leaving it un-repinned**" (`round-16-verifier-spotcheck.md:148-149`).

**Re-pinning was available, additively.** The v1 schema puts real constraints on
a superseding manifest — every receipt value must live in the expected file's
directory and be pinned, including the two round-13 sibling receipts
(`tools/evidence-disposition.py:38-40`, `:115`, `:1145-1151`, `:339-342`), and
editing the round-13 expected file directly would break the dispositions `inputs` pins (`dispositions.json:5-7`).
But I built a two-file, additive superseding manifest in the `/tmp` clone at
`98bea7d` and the gate returned **exit 0 clean**:

- the lane's round-13 dir + `.ufo/evidence/round-13/expected-r16.json` = a copy of
  `expected.json` with **one value changed**: `inputs["tools/mutate-and-run.sh"]`
  → `0673d2e5…` (all 13 input keys equal; rows untouched);
- `.ufo/evidence/round-16-test/dispositions.json` = a copy of the round-14
  manifest with only `expected_file` and `inputs` changed (its three `inputs`
  digests re-pinned to the new expected file and the two unchanged receipts);
  all 12 rows byte-identical.

Result at `98bea7d`: `status clean`, `exit 0`, counts
`{effective:11, superseded:1, passed:11, failed:0}` — the same accounting as the
baseline. Only two new files were added; `git status --porcelain` in the clone
showed no modifications. (A fully separate directory with copied receipts also
reaches exit 0, but the two-file variant is the smallest.) So the round-16 record
"the round did neither and did not list this as an open debt"
(`round-16-verifier-spotcheck.md:149-153`) is correct: the repair was not blocked
by the schema or by evidence immutability.

Two contributing effects, both visible:

- **Attribution inversion.** The gate detected; RR10 reported; the L1 (author of
  the moving commit) caused it. Recording captured-by "the gate itself (by
  design)" erases both the reporter and the cause, and makes the finding look
  self-closing.
- **Scope of the correction.** Only the round-15 registry row (`:1681`) was
  annotated. The round-14 recipe at `SKILL.md:1580-1584` still states the
  pre-round outcomes, and its bucket (`1563-1596`) kept CR26's wave-1 credit at
  the old runner sha. The spot-check's C2 failure sits precisely there
  (`:94-130`); the L1's own "corrections sweep every mention" rule was missed
  (`:204`).

[INFERENCE] I found no evidence of a deliberate cover-up. The observable
incentive is procedural: a by-design annotation plus a fresh re-read at the new
section sha restores bucket credit (the ledger merge is per section-sha,
strictest-wins), while a re-pin would have required authoring the superseding
manifest and then re-reading the bucket against a clean run. The cheaper path
also happened to clear a blocking verdict without changing the underlying
condition.

## 5. Precise mistake class

**Moved-pin re-interpretation (expectation relabeling), with detector-as-capturer
attribution and an unearned "axis unchanged" claim.**

- Primary: a whole-file instrument pin drifted by the round's own commit; the
  response was to edit the *stated expected outcome* (`0 clean` → `2 by design`)
  rather than re-pin the input or mark the row historical. This is the lane's
  named anti-pattern (`SKILL.md:1083-1084`), not a new class.
- Secondary 1: the lesson row credits the **detector** as the capturer ("the gate
  itself (by design)") while the actual reporter was RR10 — the finding's origin
  and the causal commit disappear from the record.
- Secondary 2: the same record asserts operability "unchanged"
  (`.ufo/reports/round-16/tameshi.md:90`) while the registered entry command at
  HEAD returns could-not-evaluate; the non-author scored the axis **harmed**
  (`round-16-verifier-spotcheck.md:134-155`).
- Secondary 3: cold-read `executed-ok` cannot catch this class. RX5 verified the
  **weakened text** faithfully (the commands do return 2 and the archived root
  does return 0); the defect is upstream in the text edit, and RR10's blocking
  verdict was cleared by re-reading the edited section at a new sha. Naming this
  matters for C2: input-keyed credit (R16-C2b) catches post-read surface drift,
  but it does not catch an expectation rewritten *before* the read; only a
  reader who knows the prior text (RR10) or a non-author obligation check can.

## 6. Divergences and limits

- RR10's remediation names `tools/pin-disposition.py` as "the lane's own pinning
  path"; that tool is **read-only** by contract (`tools/pin-disposition.py:2`,
  CLI `--manifest/--root`/`--selftest` at `:36`; its only writes are selftest
  fixtures at `:621-622, 789-791, 824-825`). It emits pin observations; it cannot
  re-pin. The spot-check repeats the suggestion (`:149-152`). The working
  additive repair is the superseding expected+dispositions pair demonstrated in
  §4, not that probe.
- `runner-sha256.txt` is stale at the tip: it still reads `89722ddb…` (the
  `c699c8c` runner) while the landed runner is `0673d2e5…`; the regression and
  selftest receipts carry the correct sha. This is the already-routed R16-EV1
  (`round-16-verifier-spotcheck.md:234-236`), not a new find.
- My superseding-manifest experiment is a reconstruction proof, not a proposal
  to place a file inside `.ufo/evidence/round-13/`. Round 17's dispositions v2
  (`historical_inputs` read via `git cat-file`) is the contract-conformant
  successor; either way the point stands: the 05a2247 state was repairable
  additively.
- Commands run for this report: gate at tip (exit 2), gate on `git archive
  28aeef4` from inside the tree (exit 0 clean), gate against the two superseding
  manifests (exit 0 clean), `measure.sectionize` on `017a2b0:SKILL.md` to confirm
  section 1676 text sha `f6cdac5b…`. No live-lane write, no `jj`, no git write in
  the lane.

**Verdict: holds — the reconstruction is complete; the break is a self-inflicted
instrument-pin drift (c699c8c then 05a2247, sha `89722ddb…` → `0673d2e5…` vs pin
`75ed934d…`), observed by RR10 as gap-blocking and by RX5/RX6/RX9 as accepted
"by design"; the L1 relabeled the moved pin's fail-closed exit 2 as intended,
substituted an archived-root recipe, and left the live registry row and the
round-14 recipe stale — a repair that was demonstrably available additively.**
