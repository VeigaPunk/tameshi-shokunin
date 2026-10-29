# T57W1CritClaimShape: claim-shape audit of C1 and C2 (round 57, wave 1)

Seat: T57W1CritClaimShape (critic, leaf). Lane base `5e3569969b532310d2b8a3d130901757a3df356b`; lane HEAD re-read as `5e35699` at the end of this audit, no lane file changed by this seat. Contract `.ufo/evidence/round-57/contract.json`. Rules applied: prompt §6 item 9 ("Claim sizing", `.ufo/prompts/tameshi-round-57.md` lines 529-551), `AXES.md` (calibration signal: "SHONEN.md/SCORECARD entries match observed repo state"; a claim names the axis it moves; saturation and retirement), prompt §1 ("Your lane axes: depth + calibration").

Note on the item's pointer: the assignment cites "§9" of the prompt. The prompt has no section 9; its claim-sizing rules are item 9 under section 6. I applied those rules.

## 0. Verdicts

| claim | verdict as declared | blocking defects | separable from the other claim? |
|---|---|---|---|
| **C1** calibration | **not admissible under §9 as written** | B1 target reachable by a do-nothing-on-substance control (demonstrated, E1); B2 floors reward claimed fixes, which inverts calibration; B3 the counted object is the ledger, not the SHONEN/SCORECARD entries AXES names as the calibration signal, and the axis sits at its saturation line 8; B4 two inherited counter rules make the round-57 counter wrong (`R4\d` planned regex; `BASE = e3729de8`) | verifiable without C2 only after repair D7 (open rows must be accepted for R56.2/R56.5/R56.6). Not content-separable: three of its rows are C2's result. |
| **C2** operability | **admissible after repairs** (predicate is countable, do-nothing control cannot reach it, separable from C1) | C2-1 axis binding (prompt §1 lists depth and calibration only); C2-2 one arm is already true at base (non-discriminating); C2-3 exit map omits exit 1 and is ambiguous for RECEIPT_REV_UNRESOLVABLE; C2-4 mutants and rows unnamed | yes: C2 does not read C1. C1 reads C2 only through three rows (see §4). |

Both claims: `before` pointers `before/c1.stdout` and `before/c2.stdout` do not exist yet (`.ufo/evidence/round-57/before/` is empty; `git status` shows only the untracked round-57 directories), and `frozen_paths` is `[]` (contract line 51) although C1's target relies on a frozen file set.

## 1. Evidence of the decisive check (E1: do-nothing-on-substance control reaches the C1 target)

C1 inherits the round-50 counter (`.ufo/evidence/round-50/c1/measure.py`; the round-57 counter is not yet staged, so the round-50 counter is the proxy). I built a control in a scratch clone (`git clone --shared`, detached at the base; commits only in the clone; the lane was not touched):

- CTL_JUNK step A (`b63cc5f…` first try, superseded; final `84ea6bca0bd8c092eaf70eb55e07ee1d5fb75333`): append one line per routed item to `corpus/QUALITY.md`, each line `- <id> marker, round-57 control: <first curated key of that item that is not an ACK word>`. No semantic change to any rule.
- CTL_JUNK step B (final `1ab5e1456e277c9b8322be82d5b031e6669b72cb`): rewrite the ledger so all 49 rows are `fixed`, evidence = the appended line, `commit` = step A.
- Command: `python3 .ufo/evidence/round-50/c1/measure.py --lane <clone> --rev 1ab5e1456e27… --explain`
- Output (receipt `T57W1CritClaimShape-receipts/ctl_junk_B.stdout`, exit 0):
  `C1_R50: … defects=49 rows=49 fixed=49 open=0 declined=0 fixed_this_round=49 … evidence_bad=0 key_miss=0 fixed_bad=0 … total=0 C1_R50_PASS=true`
- Contrast CTL_FAB (same ledger, excerpt not in the tree; `92f58918…`, receipt `ctl_fab_B.stdout`, exit 1): `evidence_bad=49 … total=54 C1_R50_PASS=false`.

Reading: the counter rejects fabricated excerpts but accepts appended text as a fix. The R57 target adds floors (fixed ≥ 20, declined ≤ 14, ≥ 6 this-round fixes, 49 original rows untouched, spot-checks byte-equal). [INFERENCE, not run: the CTL_JUNK construction above, with the 49 original R40-49 rows left alone and the R50-56 rows appended, would meet each of these arms, since none of them tests the content of a fix.] Therefore the R57 target as written is reachable by a control that does no routed work. §9: "if it meets the target, the counter or target is wrong — fix it before data." Data has not been scored yet, so the repair is still allowed.

One practical note: the first try failed on R49.5 because its first key is `carried`, an `ACK_WORDS` entry (round-50 measure.py line 54). Picking a non-ACK key fixed it. A lane choosing keys is therefore a free variable; the keys are frozen in `defects.json`, which is correct, but the ACK filter is key-dependent and is not an argument against the junk result.

## 2. Evidence for C2 (E2: gate exit map and the Standing-rules cell)

Gate probes against the lane snapshot (`tools/receipt-revision-gate.py`, read-only, git objects only; receipts `T57W1CritClaimShape-receipts/gate-exit-map-probe.txt` and `gate-probes/`):

| situation | command shape | exit | stdout code |
|---|---|---|---|
| no arguments | `gate` with no args | **1** | usage text (`raise SystemExit('usage…')`, gate lines 183-188) |
| certified REV unresolvable | `--certified 0123…4567 --receipt v:verdict` | **2** | `RECEIPT_REV_UNRESOLVABLE` (line 192-194) |
| receipt names unresolvable REV | `--certified BASE --receipt v-unres:verdict` | **3** | `RECEIPT_REV_UNRESOLVABLE` |
| verdict names 981c5e8b, drift on SKILL.md | `--paths` file listing `SKILL.md` | **3** | `RECEIPT_REV_CONTENT_DRIFT` (line 151) |
| same, no `--paths` | | **3** | `RECEIPT_REV_MISMATCH` (line 146) |
| verdict names 981c5e8b, bytes identical on `tools/receipt-window.py` | `--paths` file | **0** | `GATE: … verdict=PASS` |

Facts this fixes:
- The `0/2/3` map in the proposed registry row is incomplete (exit 1 exists) and not a function of the code (UNRESOLVABLE gives exit 2 for the certified REV and exit 3 for a receipt's REV).
- SKILL.md `## Standing rules` row 53 ("a verdict receipt names another revision … on the declared `--paths` surface") says `RECEIPT_REV_MISMATCH`. The gate emits `RECEIPT_REV_CONTENT_DRIFT` in that situation (verified, exit 3). The defect is real; row 54 already carries the correct parenthetical (`no --paths: RECEIPT_REV_MISMATCH`).
- All four tokens in the Standing-rules table (MISMATCH, CONTENT_DRIFT, UNRESOLVABLE, ABSENT) are in the gate's code list (gate lines 46-49). The arm "every `RECEIPT_*` token is a code the gate defines" is therefore already true at base and cannot move. Only the cell-equality arm discriminates.
- Gate rows referencing the gate: `tools/registry.json` has one row, `receipt-revision-gate-selftest` (kind `selftest`). The contract's "gate rows = 0" before-state is correct (verified with a `python3` count over `rows`).
- `registry-check.py` has `--only NAME` (line 12, 70). I did not verify its `held=N/N` output line; this is unverified.
- `tools/receipt-revision-gate.py` contains no hardcoded `/tmp` (`grep -n /tmp` → empty). Its selftest allocates through `tempfile`, so it honours `TMPDIR`. The registry row's prose "falls back to the platform default `/tmp`" describes tempfile behaviour, not a §7.4 defect. I do not route one.
- SKILL.md has 2214 lines; the newest gate/probe table is `### Round-26 gate/probe registry — report interop` at line 2175, header `| Name | Kind | Command | Exits / rule |`. Appending a row there changes no line above 2175.

## 3. Defect list with replacement sentences

Each defect has an ID, the claim, the evidence, and a replacement sentence to paste into the plan, the contract or the counter.

**Shared (both claims)**

- **S1 (C2 axis binding, also C1 saturation).** Prompt §1 says the lane's axes are depth and calibration. C2 moves operability, which the contract says "carries no standing score". Replace contract `claims.C2.axis` with: `"axis": "operability (not a prompt-§1 lane axis; no standing score; verdict by counts only; the operator rules on the binding)"`. Alternative: declare C2 a capability acquisition (AXES, Capabilities) and enter its row in the capabilities table.
- **S2 (before pointers).** `before/c1.stdout` and `before/c2.stdout` are not produced. Replace each `before` pointer with: `"before": "stdout of <counter> --lane LANE --rev 5e3569969b532310d2b8a3d130901757a3df356b --work EMPTY_DIR --explain, committed at .ufo/evidence/round-57/before/<c1|c2>.stdout before the first ledger or registry commit"`.
- **S3 (frozen_paths empty).** Replace `"frozen_paths": []` with: `"frozen_paths": [".ufo/evidence/round-57/c1/defects.json", ".ufo/evidence/round-57/c1/measure.py", ".ufo/evidence/round-57/c2/measure.py", "corpus/lessons/round-50-verifier-spotcheck.md … round-56-verifier-spotcheck.md", "the 49 original rows of corpus/routed-defects.json (R40.1-R49.5)", "the 22 gate rows of tools/registry.json (no change to their argv or expect)"]`. Freeze arms (byte-equal checks) belong here, not in a claim total.

**C1 (calibration)**

- **C1-B1 (do-nothing reach, E1).** Add `CTL_JUNK` to the pre-registered controls with expected verdict FAIL, and repair the rule before data. Recommended repair (removal witness): a `fixed` row needs at least one evidence item whose excerpt is present in its path at `routed_at` and absent at REV (the defect text removed, not new text added). Items whose defect is an absence (a missing row, a missing file) cannot be `fixed` by this rule and must be `open` or `declined`. Replacement sentence: `"fixed requires a removal witness: an evidence item whose whitespace-normalised excerpt occurs in its path at the routing commit and does not occur in that path at REV; an item with no removal witness is open or declined, never fixed."` Expected consequence (not run): CTL_JUNK, which removes nothing, fails the removal arm and the target is unreachable. Honest fallback if the operator rejects the removal witness: narrow the claim to `"C1 measures ledger-to-tree agreement under the new-keyed-excerpt rule; it does not measure fix quality"`, and say that a CTL_JUNK pass means the claim is bookkeeping, not calibration.
- **C1-B2 (floors invert calibration).** Remove `fixed >= 20`, `declined <= 14` and `>= 6 this-round fixes` from the target (they reward claimed fixes: a ledger that honestly marks 30 items open fails). Replacement sentence: `"C1_R57_PASS=true iff corpus/routed-defects.json at REV has exactly one row for each item of the frozen N=51 set and the counter's disagreement total is 0; the status mix (fixed/open/declined) and this-round counts are printed, not gated."` Note: round-50's floor is the only thing that makes its CTL_OPEN fail; with the floor gone CTL_OPEN must be re-tested, not assumed.
- **C1-B3 (object and saturation, §9 bullet 3 and AXES).** §9 requires a calibration claim to "count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state". C1 counts ledger rows. The ledger is a self-record of routed defects, and only the `open` arm reads SCORECARD. Also, `calibration = 8` is the lane's saturation line (contract `lowest_axis`), so no counted move can change the score: the scored axis cannot move. Replacement sentence for the claim surface: `"C1 counts disagreements between the routed-defect ledger, the newest SCORECARD 'Planned (round' paragraph and the tree at REV; the calibration score stays at its saturation line 8 and the claim verifies as a count move on a sub-axis 'calibration.routed-ledger', which SCORECARD.md must record with the split reason (AXES 'Working the axes': split with reason)."` Alternative: retire the calibration score and say so.
- **C1-B4a (inherited planned regex).** `planned_ids` in round-50 measure.py line 111 uses `\bR4\d\.\d+\b`. Any round-57 `open` row for R50-R56 can never pass `open_unplanned`. Replacement counter rule: `"the planned-id pattern is \bR5[0-6]\.\d+\b (round 50-56 items) and \bR4\d\.\d+\b (round 40-49 items); both match in the newest 'Planned (round' paragraph"`.
- **C1-B4b (inherited BASE constant).** `measure()` uses `base or BASE`, `BASE = 'e3729de8…'` (line 272), and `main()` never passes a base. So "fixes carried by commits after the base" counts every commit since round 50, not since round 57. Replacement sentence: `"at least 6 of the fixed rows are carried by commits that are not ancestors of 5e3569969b532310d2b8a3d130901757a3df356b (passed as --base to the counter, not the constant)"` — or drop the arm under C1-B2.
- **C1-N (N not concrete).** The before-state says "~52 routed items", the target says "N", the expected count is 51 (prompt §6 item 9 rule; per-round counts 4+8+6+9+10+7+7 = 51). Replacement: `"N = 51: the count printed by extract-defects.py at base 5e3569969b…, pinned in defects.json; the before line reads rows=0/51"`. My rough recount agrees with 51 (R54 has ten labelled items plus the `R54.5 extended` line folded into R54.5; R51 has one labelled head and seven unlabelled), but I did not re-run the extractor. The count is therefore unverified by this seat.
- **C1-S (completeness word).** The surface says "against the routed items of the seven spot-checks"; the `cannot_see` says "whether the N-item set is the complete set". The first is a universal with no enumerating command. Replacement surface: `"the 51 items of the frozen set c1/defects.json, extracted from the seven spot-check files at base; the set's completeness is not measured by C1 and is the extractor's recall, attacked by readers"`.
- **C1-G (guards inside the claim).** "The 49 original rows byte-identical to base" and "the seven spot-check files byte-equal to the frozen set" are freeze guards, not calibration. Move them to S3's frozen_paths; keep them out of the total.
- **C1-L (line-exact evidence).** The counter requires an excerpt to occur inside the stated `lines a-b` (round-50 `check_evidence`, line 148). C2 and any SKILL.md line shift can break a C1 row (see §4). Replacement rule: `"evidence resolves when its normalised excerpt occurs in the path at REV, within the stated lines when those lines still hold it, else exactly once in the file; a line drift is printed as a note, not a miss"`.
- **C1-R (conditional status).** R56.4 is "ledger row; referent record only if a wave-1 seat establishes the referents" and R56.7 is "report phrasing corrected in the report". A conditional status cannot be scored, and a report-only fix is not a keyed tree change. Replacement: fix each row's status at freeze: `R56.4 open (Planned round 57)`, `R56.7 open (Planned round 57) or fixed by a lesson errata line`.

**C2 (operability)**

- **C2-1 (exit map).** Replace the registry exit-map text with: `"exit 0 PASS; exit 2 only when --certified does not resolve (GATE: error=unresolvable-certified); exit 3 when any receipt is refused (named code on stdout); exit 1 usage or crash (stderr, no verdict line)"`. Note in the same cell that RECEIPT_REV_UNRESOLVABLE can exit 2 (certified) or 3 (receipt).
- **C2-2 (non-discriminating arm).** Delete "every `RECEIPT_*` token … is a code the gate defines" from the target: it is true at base (gate lines 46-49 cover all four tokens in the Standing-rules table). Keep only: `"the Standing-rules row 53 cell reads RECEIPT_REV_CONTENT_DRIFT (no --paths: RECEIPT_REV_MISMATCH, mirroring row 54) and equals the code the gate emits on a counter-built drifting fixture"`.
- **C2-3 (rows, ≥3 is vague).** Replace `>= 3 active gate-kind rows` with exactly four rows, each run as `python3 tools/receipt-revision-gate.py --lane . --certified <REV> [--paths <file>] --receipt <committed-fixture>:verdict` (never `--selftest`): (a) exit 0, same-bytes receipt naming `981c5e8b20a2…` with `--paths tools/receipt-window.py`; (b) exit 2, `--certified` a 40-hex value that does not resolve; (c) exit 3, `RECEIPT_REV_CONTENT_DRIFT` on `--paths SKILL.md` (fixture names 981c5e8b); (d) exit 3, `RECEIPT_REV_MISMATCH` with no `--paths`. Probe results for (a)-(d) are in §2.
- **C2-4 (mutants unnamed).** Replace `"three counter-applied gate mutants (accept-on-drift, wrong refusal code, exit 0 on unresolvable)"` with: `"M1: line 150 'if drift:' never true (accept on drift; row (c) goes red); M2: line 151 RECEIPT_REV_CONTENT_DRIFT replaced by RECEIPT_REV_MISMATCH (row (c) red); M3: line 194 'return 2' replaced by 'return 0' (row (b) red); each applied to a scratch copy of the tree, each killed iff at least one of rows (a)-(d) fails under registry-check --rev REV --only"`. Name the M3 situation (certified REV) so "unresolvable" is not read as the receipt-REV case (exit 3).
- **C2-5 (SKILL row location).** `the SKILL gate/probe registry table` names no heading and about 20 such tables exist (lines 1590-2175). Replace with: `"a row for receipt-revision-gate appended to the table under '### Round-26 gate/probe registry — report interop' (SKILL.md:2175, the last such table), whose 'Exits / rule' cell carries the exit map of C2-1"`.
- **C2-6 (cell edit line count).** The Standing-rules cell edit at line 53 is in place (same line count), so no SKILL line above 2175 shifts. State it: `"the edits to SKILL.md are one in-place cell change at line 53 and one appended row after line 2175; no other SKILL line moves"`.

## 4. Causal separability: is C1 still verifiable without C2?

Answer: **yes, after repair C1-B4a, and only if the three C2-routed rows are scored as ordinary rows.** The current wording makes it false in content, not in the verifier.

- C2 does not read C1 (its arms read the registry, the gate, SKILL.md and fixtures). C2 is verifiable without C1.
- C1 reads C2 through three rows: R56.2 (SKILL cell, C2 arm), R56.5 (controls header, C2 kill rule), R56.6 (gate rows, C2). Without C2 those rows can only be `open`; with the current planned regex (`R4\d`) an `open` R56.x row fails, so C1 cannot verify without C2 at all. Repair C1-B4a removes that.
- Under the C1-B2 repair (no fix floor), C1 is verifiable without C2 when the three rows are `open` and named in `Planned (round 57)`. The C1 predicate then has no arm that reads a C2 result.
- The line coupling (C1-L): C2's SKILL edits are in place at line 53 and append after line 2175. The C1 rows that cite SKILL.md (R49.3 at lines 1503, 1509, 1555 in the ledger) are above both, so they do not move. This protects the rows only while C2 keeps that discipline. Repair C1-L removes the coupling.

Exact wording for the plan (one sentence):

> C1 verifies with C2 absent: rows R56.2, R56.5 and R56.6 are `fixed` only if a post-routing commit at or below REV adds a new keyed excerpt to their path, and are otherwise `open` and named in the newest `Planned (round 57)` paragraph; C1's predicate reads no C2 receipt, and C2's commits change no C1 arm.

Exact wording for the counter's header (one line): `# C1 reads only corpus/routed-defects.json, the frozen c1/defects.json and SCORECARD.md at REV; no C2 artifact is an input.`

## 5. Do-nothing reachability (§9 bullet 6)

- C1: CTL_0 (base) → total>0 (contract `before`; not re-run by this seat). CTL_JUNK → total=0 with the round-50 counter (E1). **Reachable: defect B1.** Repair per C1-B1.
- C2: CTL_0 (base) → gate rows = 0 (verified: the single gate-referencing row is kind `selftest`), `total=1` per contract. A control that writes four rows, the SKILL cell and the appended row would reach the target, but that is the claimed work, so it is not a defect. The arm that a do-nothing control passes is C2-2 (defect).

## 6. Sweeps that found nothing (with command output)

- `grep -n /tmp tools/receipt-revision-gate.py` → no output. Hence no §7.4 route.
- `python3` count of registry rows referencing `receipt-revision-gate` → `1 [('receipt-revision-gate-selftest', 'selftest')]`. Confirms the contract's before-state of zero gate rows.
- `sed -n 46,49p tools/receipt-revision-gate.py` → all four Standing-rules tokens defined (basis of C2-2).
- `grep -n "R4\\d" measure.py` → line 111 `\bR4\d\.\d+\b` (basis of C1-B4a); `BASE =` line 272 (basis of C1-B4b).
- `ls corpus/lessons/round-5{0..6}-verifier-spotcheck.md` → seven files present (C1 surface exists).

## 7. Limits and unverified

- I did not run the round-57 counters (not staged yet); E1 uses the round-50 counter as the proxy the contract says C1 inherits. The repairs in C1-B1 and C1-B4 change that counter, so E1's result must be re-run on the amended counter before it is cited as the round-57 result.
- The N = 51 value is not re-derived by the extractor; the rough recount above supports it only.
- Registry-check's `held=N/N` line and its `--only` behaviour were not executed.
- Semantic support of a keyed excerpt is not tested (the contract's `cannot_see` says so).
- Scratch clone deleted after this report was written; receipts are in `T57W1CritClaimShape-receipts/`.

## 8. Tools installed or upgraded

None. This seat used only `git`, `python3` (stdlib) and the lane's own tools, read-only on the lane.

## 9. Receipts

Under `.ufo/waves/round-57/w1/T57W1CritClaimShape-receipts/`:
- `ctl_junk_B.stdout` (exit 0, `C1_R50_PASS=true`), `ctl_fab_B.stdout` (exit 1, `C1_R50_PASS=false`), `ctl_junk_result.json` (commit hashes A, B, B_fab and the key choices).
- `gate-exit-map-probe.txt` and `gate-probes/` (the six gate probes, with the probe receipt files).
