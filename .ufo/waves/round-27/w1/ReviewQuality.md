# ReviewQuality: QUALITY criteria 53 and 54 (round 27)

Reviewer: TameshiR27.ReviewQuality (leaf member, no dispatch). Judged on calibration.

Scope: `corpus/QUALITY.md:591-611` (criteria 53 and 54). Content revision `2227d8338c02aa9a5fd7d95c1a41b76865ad7647`; base `91edf9cd82ccc72e10f62f81d37181f549d593b8`; pre-registration `70df8d6a485418d9e57fed9d21e84fba71d4be66`.

Method: every counter run used a scratch clone under `/tmp/tq27-rq/` (`clone` pinned at `2227d83`, plus scratch clones `e1` to `e10`). Counter copies in `/tmp/tq27-rq/bin/` are unmodified copies of `.ufo/evidence/round-27/c1-measure.py` and `c2-measure.py`. No lane file was written.

## Verdicts

- **Criterion 53: amend before landing.** The cited numbers reproduce, and the falsifier fires as stated at `e08444d3` and at base `91edf9cd`. Two things keep it from being checkable as written. Its trigger has two readings, and read literally round 27 falls inside it (H1). Its "independent seats" clause is not something the counter can check (M2).
- **Criterion 54: amend.** The lesson backing holds, and the falsifier fires as stated for a changed committed probe or anchors byte. But the rule checks that digests are named, not that a run produced the receipt. A receipt whose digest was rewritten to the current probe passes with stale results (M1). So the C2 claim's word "executed" has no counter check behind it.

I recommend the lead settle H1 before the round lands. The other findings can be recorded as bounds or routed to the counter owner.

## Findings by severity

### High

**H1. Criterion 53's trigger has two readings. Round 27 is in scope on the literal one.**

- Literal text (`corpus/QUALITY.md:591-594`): "a file traced as an input of a credited cold-read section".
- Monitor credit is per section, keyed by sha256. A section is credited when any ledger entry whose sha256 matches the section passes, with `covered = credited > 0 and not vetoes` (`.ufo/evidence/round-18/measure.py:611-638`). Entries that fail still list their traced inputs in the section's reasons.
- Round 27's content revision changes `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md` and `corpus/SOURCES.md` (`git diff --name-only 91edf9cd 2227d83`).
- Credited section 1155, "## The cadence's first scheduled tick, and the service's limits (round 9, measured)", has a failing sibling entry. Its failing inputs are exactly those five files. The same reason string appears at base. Method: `measure.py --rev <rev> --explain` at both revisions, compared per section (see Monitor comparison below).
- The counter registers none of this. C1 reads `covered=25/64 restraint=6 box3_mismatch=1` at base and at head. The per-entry reasons for all 64 sections are identical base to head.
- Read literally, round 27 must re-read section 1155, or declare calibration harmed in its SCORECARD measured row, before landing. In the part of the round-27 SCORECARD section I read (`SCORECARD.md:1334-1349` at `2227d83`) I found neither a harm declaration nor a re-read plan for 1155. I did not read the rest of that section.
- Read the way the monitor credits (the passing entry carries the credit), round 27 is out of scope, because a failing sibling backs no credit. [INFERENCE: this is the reading the credit rule implements; the criterion's text does not say so.]
- The gap is shown by construction (E9, below). One edit to `corpus/knowledge/mutation-score-semantics.md` at base leaves `covered=62/62 restraint=8 box3_mismatch=0`, exit 0. That file is traced only by already-failing sibling entries of four credited sections.
- Smallest correction: name the reading in 53. I recommend the crediting-entry reading, with the bound "entries that already fail are not measured." If the lead keeps the literal reading, round 27 must re-read 1155, and every other credited section whose failing sibling the round touches, or declare harm, before landing. The counter cannot choose between these.

### Medium

**M1. Criterion 54 is satisfied by a rewritten digest. Naming is not provenance.**

- Test E4. The probe was edited and committed (`0ecc632`). `receipt.json` `probe_sha256` was rewritten to the new probe's sha256 (`d74d94ff…`) and committed (`10d4496`). Observed: `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0. The four results are still the old run's results. The probe was not re-run.
- Code: `c2-measure.py:86-88` compares the receipt's two digest fields with the bytes at REV. `c2-measure.py:117-129` read each result's class and meets-fields from the receipt without re-deriving them.
- Consequence: the criterion checks which bytes a receipt names, not that a run produced it. Anyone who can write `receipt.json` passes the check. The contract's C2 claim ("by an executed probe") has no counter check behind it.
- Correction: add one sentence to 54 saying naming is not provenance, and that a claim of execution needs a re-run at that revision (by the counter, or a result digest the counter recomputes). The counter fix belongs to the counter owner; the counter is frozen at pre-registration.

**M2. Criterion 53's "independent seats" cannot be checked by the counter.**

- The credit gate (`measure.py:513-526`) reads the verdict, the class, the blocking and wrong-expectation counts, the commands count, repo-relative inputs, and trace receipts. Nothing reads `seats` or `reports`. The only matches in `round-18/measure.py` and `round-21/coldread/measure.py` are comments and docstrings. The trace receipt builder (`measure.py:785-795`) writes only `schema`, `inputs`, `live_lane_reads` and `external`.
- Test E10 (`aa7e73d`). On a credit-carrying entry (ledger line 302; section "## The mutation bar — nominal vs load-bearing"), `seats` `"CR06"` was changed to `"NOBODY"`. Observed: `covered=25/64 restraint=6 box3_mismatch=1`, exit 1. The uncovered list is identical to head, and the section stays `credited`.
- The lane's own text already separates lane authorship from independence: `SKILL.md:1801-1803` ("never an independent `[x]`"), `corpus/lessons/round-19.md:102-104` ("L1-author … not a new blind or independent cold-read"), and `corpus/lessons/round-16-verifier-spotcheck.md:226-227` ("The cold-read credit is sha-only"). The counter does not measure any of this.
- Correction: state in 53 that independence is checked by reading each re-credited entry's `seats` and `reports` against the wave roster, not by the counter.

**M3. The C2 counter trusts the receipt's class.**

- Test E8 (`a9c0af1`). The `S_USAGE` receipt's `pristine_meets_anchor` was set to false, and its class was left as `anchored-hole`. Observed: `S_USAGE: anchored-hole pristine_meets=False mutant_meets=False`, then `classified=4 anchored_holes=4`, exit 0.
- Code: `c2-measure.py:117-129` count `r['class']` directly. The receipt's `expect` is never compared with `anchors.json`.
- This is a counter defect outside 54's text. Route it to the counter owner. The counter is frozen in the pre-registration, so a fix is a contract question for the lead.

### Low

**L1. Criterion 53: citation range and the artifact that declares harm.**
- The cite `lessons/round-26-verifier-spotcheck.md:112-135` does not contain the phrase "numeric 8 → 8". That phrase is at `:109-110`. Routed item 2 repeats it at `:219-221`.
- "Declares calibration harmed among its measured results" does not name an artifact. Round 26's report declared harm ("a harm, not a no-harm", `corpus/lessons/round-26.md:138-142`), while the SCORECARD measured row C2 read "numeric 8 → 8" (`SCORECARD.md:1309`). Round 27's own correction (`SCORECARD.md:1321-1332`) calls that row wrong. Name the artifact; I recommend the SCORECARD measured row.

**L2. Criterion 53 leaves external inputs unmeasured.**
- Ledger entries carry `external_inputs`. One example is `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/cite-check.mjs`, at ledger lines 256-277. The monitor records these and never reads their bytes; `measure.py:554,605-608` are the only uses. Trace receipts check external keys only under the live lane (`measure.py:423-428`).
- Of 1,202 unique external paths in the head output, none is under the lane. 735 are under the fleet root, 95 under `kumitate-shokunin`, 4 under other projects, and 368 sit outside `/home/vgpnk/Projects` (sampled: round-17 wave scratch under `/tmp`).
- Correction: scope 53 to repo-relative inputs (the ledger `inputs` field), and state that external inputs are recorded, not measured.

**L3. Criterion 54: attribution, scope, the interpreter, and a docstring overclaim.**
- Attribution. Lesson item 4 (`:225-228`) says "QUALITY 51's receipt check does not tie a receipt to the tool bytes". QUALITY 51 (`corpus/QUALITY.md:572-574`) names the round-26 `c2-measure.py` as its falsifier. The link holds, but a reader following the cite finds a different name. Quote the lesson's words, or cite QUALITY 51 beside it.
- Scope. Lesson item 4 says "a future calibration counter". Criterion 54 says "a counter that accepts a run receipt". The lesson's evidence covers calibration counters only.
- Interpreter. `receipt.json:5` records `"node": "v24.21.0"` as text. The interpreter's bytes are not digested. Decide whether "tool bytes" includes it.
- Docstring. `c2-measure.py:17-18` says the receipt "is bound to the bytes that produced it". The check shows naming only (E4). Correct the docstring along with the counter fix.

**L4. Information: the counter reads committed bytes only.**
- E3: with a probe edit left uncommitted at `2227d83`, the counter reports `classified=4`, exit 0. It reads `git show REV:path`. That matches "at the measured revision", but the falsifier fires only on a committed change.

## Lesson backing (followed cites)

| Cite | What it says | Status |
|---|---|---|
| 53 → `lessons/round-26-verifier-spotcheck.md:112-135` | Table at `:120-123`: d4140796 62/62, restraint 8, depth 8; e08444d3 25/64, restraint 6, depth 9. `box3_full_page` false (`:127-128`). Calibration harmed (`:132-135`). | Backed. Numbers reproduced (table rows C1-c, C1-a below). |
| 53, phrase "numeric 8 → 8" | At `:109-110` and `:219-221`, outside the cite. | Backed. Add `:109-110` to the cite. |
| 54 → `lessons/round-26-verifier-spotcheck.md:225-228` | Item 4: counter gameable by prose and unrelated receipts; receipt check does not tie a receipt to tool bytes; a future calibration counter must bind receipts to tool digests. | Backed for calibration counters. See L3. |
| 54 → QUALITY 51 (`corpus/QUALITY.md:568-574`) | Bound: the receipt check does not tie a receipt to the tool bytes; falsifier is the round-26 `c2-measure.py`. | Backed. This is the link 54 relies on. |

## Checkability

| Property | Counter decides? | Evidence |
|---|---|---|
| 53: coverage, restraint, box3 at a landed revision | Yes | C1 rows below. The monitor reads the ledger at the revision (`ledger_source` = `rev`). |
| 53: which sections a round's edits touch | Partly; section level only | E9, H1 |
| 53: independence of seats | No | E10, M2 |
| 53: external inputs | No | L2 |
| 53: where harm is declared | No | L1 |
| 54: digests named at REV | Yes | E1, E5 |
| 54: receipt produced by those bytes | No | E4, M1 |
| 54: result class matches recorded fields | No | E8, M3 |
| 54: input bytes | Yes, indirectly | Anchors file digest in the receipt; the pinned kumitate blob through `anchors.json` `blob_sha256`, checked live at `c2-measure.py:89-94`; SOURCES rows read at REV |
| 54: tool bytes | Probe script only | Receipt `probe_sha256`; the interpreter is not digested (L3) |

## Constructed cases (scratch clones; commands and observed output)

Commands: `cd /tmp/tq27-rq && python3 bin/c1-measure.py --repo <clone> --rev <rev>` and `python3 bin/c2-measure.py --repo <clone> --rev <rev>`. Exit codes were read with `echo $?`.

| ID | Clone (commit) | Change | Observed | Criterion expects | Result |
|---|---|---|---|---|---|
| C1-a | `e08444d3` | none | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9`, exit 1 | exit 1, box3 1 | Fires as stated |
| C1-b | `91edf9cd` | none | same numbers; line 1 equals `.ufo/evidence/round-27/c1-before.stdout` line 1; exit 1 | same | Fires as stated |
| C1-c | `d4140796` | none | `covered=62/62 restraint=8 box3_mismatch=0 depth_score=8`, exit 0 | baseline | Baseline holds |
| C1-d | `2227d83` | none | `covered=25/64 restraint=6 box3_mismatch=1`, exit 1 | pre-repair | Informational |
| E6 | `163893d` (on base) | one blank line appended after line 275 of `corpus/knowledge/mutation-case-kagi-census.md` | `covered=51/62 restraint=6 box3_mismatch=1`, exit 1; 11 headings uncovered | fires | Fires |
| E9 | `7bcd9c1` (on base) | blank line and one sentence appended after line 81 of `corpus/knowledge/mutation-score-semantics.md` | `covered=62/62 restraint=8 box3_mismatch=0`, exit 0 | fires under the literal reading | Does not fire (H1) |
| E10 | `aa7e73d` (on head) | `"CR06"` changed to `"NOBODY"` on a credit-carrying entry (ledger line 302) | `covered=25/64 restraint=6 box3_mismatch=1`, exit 1; uncovered list identical; section still `credited` | independence should matter | Does not fire (M2) |
| C2-a | `2227d83` | none | `classified=4 anchored_holes=4`, exit 0 | target | Target state; not proof of execution (M1) |
| E1 | `8f70a38` | probe docstring line 16 edited and committed | four `UNCLASSIFIED (receipt not bound to probe and anchors bytes)`; `classified=0`; exit 1 | fires | Fires |
| E5 | `0c49db3` | `anchors.json` line 4 edited and committed | same as E1; exit 1 | fires | Fires |
| E3 | `2227d83` plus uncommitted probe edit | working tree only | `classified=4`, exit 0 | does not see working tree | Expected (L4) |
| E4 | `10d4496` | probe committed (`0ecc632`); receipt `probe_sha256` rewritten to the new digest | `classified=4 anchored_holes=4`, exit 0 | should fail (no re-run) | Does not fire (M1) |
| E8 | `a9c0af1` | `S_USAGE.pristine_meets_anchor` set to false; class kept | `S_USAGE: anchored-hole pristine_meets=False`; `classified=4`, exit 0 | should fail (class inconsistent) | Does not fire (M3) |

Note on an earlier seat test: `31ba157` changed the seat of ledger entry 0. That entry matches no SKILL section by sha256 and already fails on `input-drift:PROVINCE.md`, so its seats could not move coverage. The result was uninformative, so I discarded it and used E10.

## Monitor comparison (run at four revisions with `--explain`)

- Base `91edf9cd` against head `2227d83`: 25 credited at both. 0 of 64 sections change their per-entry reasons.
- Round 26, `d4140796` to `e08444d3`: 37 credited sections lost (62 to 25). At round-26 base, 44 of 62 credited sections already had a failing sibling entry; at head, 14 of 25 do. 51 sections credited at base have at least one failing entry at head (37 lost outright, 14 still credited). The lesson's "37 sections" counts only the section-level loss.

## Smallest corrections (proposed text)

**53.** Replace the trigger sentence and add the bounds; keep the falsifier.

> 53. Round 27. A round that edits a file which is an input of the ledger entry crediting a section (an entry whose sha256 matches the section and passes at the base revision) either has those sections cold-read again by fresh seats at its content revision before it lands, or declares calibration harmed in its SCORECARD measured row. Entries that already fail are not measured by the monitor. The monitor does not read seats, reports or external inputs, so independence is checked by reading each re-credited entry's seats and reports against the wave roster. A calibration no-harm reading names the strict monitor at the landed head, never an earlier revision. Captured by: `lessons/round-26-verifier-spotcheck.md:109-110,112-135,219-221`. Falsifier: (unchanged).

**54.** Add one sentence after "...counts as absent."

> Naming is not provenance: this check does not show that the receipt's results came from the named bytes, so a claim that a probe ran needs a re-run at that revision.

Also: the C2 claim in `.ufo/evidence/round-27/contract.json` says "by an executed probe". Reword it to "by a probe whose receipt names its bytes", unless the lead adds a re-run. The contract is frozen, so this is the lead's call.

## Residual risk and verification gaps

- Anyone who can write `receipt.json` passes C2 (M1).
- The counter cannot tell who recorded a cold read. Any committed receipt whose input sha256 values match credits its entry (M2).
- I did not run `anchor-probe.py`, so I have not reproduced the four receipt results.
- The kumitate blob: the counter's contract-quote checks passed at head, which implies the pinned blob matched [INFERENCE]. I did not check its sha256 separately.
- The overlap check in H1 uses the monitor's `input-drift` reasons. An entry that fails for another reason and lists no file falls outside that check.
- I read only part of the round-27 SCORECARD section (`:1334-1349` at `2227d83`).
- I ran no gates, selftests, sweeps or mutation runs, as assigned.

## Calibration of this review

- Run and observed: every row of the constructed-case table, and the monitor comparison, in scratch clones.
- Read and confirmed by path and line: the code and lesson citations.
- Inferred, marked [INFERENCE] above: the crediting-entry reading as the intent of 53, and which sections count as in scope under each reading. The round-26 correction says the SCORECARD row was wrong, but not why.
- Not claimed: no producer authentication, no promotion, no score.

## Tooling and access record

- Installs and upgrades: none. `/home/vgpnk/.omp/agent/RULES.md` was read first. Tools used were git 2.56.0 and Python 3.14.8, both already present.
- Lane access: read-only git with `GIT_OPTIONAL_LOCKS=0` (clone source, log, rev-parse, show, diff). One `git status --porcelain` in the lane ran without that variable; that was my error. It is read-only apart from an optional index stat refresh. At that moment the lane showed 3 porcelain entries, none created by me. No lane write, and no `jj` command anywhere.
- Scratch: `/tmp/tq27-rq/` (`clone`, `e1` to `e10`, `mut1`, `bin/`, `out/`). Monitor outputs: `out/monitor-*.json` and `out/explain-*.json`.
