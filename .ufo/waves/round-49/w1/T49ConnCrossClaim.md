# T49ConnCrossClaim — round-49 cross-claim pattern findings

Seat: connector (leaf). Item: cross-claim pattern finder over C1 (calibration) and C2 (coverage).
Inputs read (all read-only; no counter executed, no scratch needed — no drivers were run):

- `.ufo/evidence/round-49/contract.json` (claims, predicates, controls, kill rules)
- `.ufo/evidence/round-49/c1/measure.py` (frozen C1 counter, 590 lines)
- `.ufo/evidence/round-49/c2/measure.py` (frozen C2 counter, 465 lines)
- `.ufo/evidence/round-49/control/c1-controls.py`, `control/c2-controls.sh`, `control/c1-controls.stdout`, `control/c2-controls.stdout`, `control/c1-selftest.stdout`, `control/c2-selftest.stdout`, `control/no-harm-at-base.stdout`
- `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json` (90 base pointers)
- `tools/staged-id-guard.py` (the pinned named gate, sha256 verified `03a796c5…` matches contract)
- Wave-1 in-flight artifacts (read-only): `.ufo/evidence/round-49/c1/refresh.py`, `c1/merge-reads.py`, `.ufo/waves/round-49/w1/T49ExecGenerator.pbt-staged-id.py`, `w1/*.rows.json` reader receipts
- Not opened, per seat bounds: `control/c2-WITNESS.stdout`, `c2-CTL_FIX.stdout`, `c2-CTL_ABSENT.stdout` (their tail lines reached me only via the committed `c2-controls.stdout` summary, which is not a forbidden path).

## (a) Shared weaknesses — what each counter cannot see, and leak paths

### What C1 cannot see (with lines)

1. **Whether anyone read anything.** `check_reads` (`c1/measure.py:256-315`) keys rows on `(heading, ordinal, raw)` re-derived from its own extractor (`:262`) and checks only `file`, `ranges`, `verdict=='holds'` (`:304`) and excerpt containment (`:311`). The `reader`, `base_verdict`, `note` fields of the reads schema are never inspected. The `mech_reads` writer in the controls harness (`control/c1-controls.py:124-145`) labels itself `reader: 'control (mechanical, unread)'` and CTL_K2 passes with those rows — the positive control that demonstrates the blind spot by passing.
2. **Semantic support.** Contract `claims.C1.cannot_see` states it: the counter checks the excerpt is really at the pointed place, not that the quoted text supports the section's sentence. Covered out-of-band by wave-2 re-read seats and the closure spot-check.
3. **Live-lane coupling of the judge.** `measure()` (`c1/measure.py:368-373`) pins the round-21/round-18 monitor bytes both at the **live lane path** and at REV. The deciding run therefore fails setup on a dirty working tree even with a correct REV — a hygiene dependency C2 does not have (C2 never executes lane bytes except its own `--selftest`-free counter; it materializes REV blobs, `c2/measure.py:249-265`).
4. **Pointer-set shape beyond a floor.** `FLOORS` (`c1/measure.py:78-80`) are base-derived lower bounds; `floor_short` (`:382`) only fires on deletion. Added spurious pointers each need a row, but mechanical rows are cheap (point 1), so section bodies can drift in content while staying fully "credited" — heading text is frozen, body quality is not judged.

### What C2 cannot see (with lines)

1. **Method.** Only outcomes over the frozen interface are scored: pristine run + dump shape (`c2/measure.py:322-327`), per-case re-execution against the counter's own oracle (`:320-327`), class counts over the dump (`:117-165`), and mutant kills confirmed differentially (`:336-346`). Nothing checks the generator is a *property-based* generator; CTL_FIX (`control/c2-fixed-gen.py`, "the cheapest generator that skips generation") proves a fixture-replay stub passes pristine + oracle + classes and still fails (confirmed=6/12, `c2-controls.stdout`). The hidden panel (`contract.claims.C2.panel.why_hidden`) is the sole method-level discriminator, and it blocks tuning to the mutants, not tuning to the guard.
2. **Record semantics.** `records()` (`c2/measure.py:268-291`) greps the entry head for `source: S…` and checks the SOURCES row shape (`len(cells)==11`, `cells[7]=='mined'`, `cells[8]=='2026-10-26'`, `:285`) plus one README line containing `F10` and `held (round 49)` (`:288-290`). The entry body and the row's content are unverified (census/no-harm monitors cover the corpus externally).
3. **Single-seed scope.** SEED=4949 is frozen (`:49`); "capability" is capability at that seed against this guard. Acknowledged in the contract, not a defect.

### Cross-leak analysis

- **No counter reads the other claim's evidence.** C2's counter reads exactly five lane paths: the guard, the generator, `corpus/knowledge/pbt-generator-pilot.md`, `corpus/SOURCES.md`, `corpus/README.md` (`c2/measure.py:45-48,268-291`) — none are C1 artifacts. C1's counter reads SKILL.md target sections, the monitor files, `c1/reads.json`, `corpus/SOURCES.md` (SID resolution, `:176-181`), and whatever the seven sections cite; none are C2 artifacts (base census below). There is no path by which C1's reads.json/ledger or C2's panel/entry/generator enter the other counter.
- **Two files are read by both counters** (the only shared surface, see (b)): `corpus/SOURCES.md` and `corpus/README.md`. Both counters read them as REV blobs, so views are consistent; no runtime state flows between counters.
- **Editorial leak channel (controllable).** If C1's integrated sections newly cited `tools/pbt-staged-id.py` or `corpus/knowledge/pbt-generator-pilot.md`, C1's rows would quote C2's artifacts, making C1's verification content-dependent on C2's files. At base the seven sections cite no generator-era file (census: the `tools/*` citations are `mutate-and-run.sh`, `repeat-control.py`, `pin-disposition.py`, `witness-metadata.py`, `evidence-disposition.py`). Keeping it that way is an integration choice, not a counter property.
- **Interference, not leak.** Two narrow ways C2's required record edits can break C1 rows: (i) C2 must edit README's F10 row *in place* (line 87 today: `| F10 | … | open |` → `held (round 49)`), and C1 has three whole-file `path` rows quoting `corpus/README.md` — if any quoted excerpt lived on that line, the edit would make it `excerpt_miss` (`c1/measure.py:311`). Scanned all wave-1 `*.rows.json`: no row quotes the F10 text (excerpts are README §1 / coverage-map material). Clean today, fragile by construction. (ii) C2 appends new SOURCES rows; SID pointers require exactly one registry-row match (`c1/measure.py:176-181`), so a new row id duplicating a cited S-id (S003, S004, S026, S041, S047, S049) would turn those pointers `unresolved`. Contract names the planned rows S182/S183 (`frontier_step.sources`) — no collision. Both hazards are one-line checks the integration can enforce.

### The shared meta-pattern (strength, compensating for the blindness)

Both counters are **blind by design and name their blind spot with a control**:

| | blind spot | demonstrating control (receipt) |
|---|---|---|
| C1 | mechanical rows pass | CTL_K2 **passes** with fabricated rows (`c1-controls.stdout`, total=0, PASS=true) — positive control naming what the counter cannot see |
| C2 | fixture replay is not generation | CTL_FIX **fails** the panel (confirmed=6/12 < 11) — negative control showing the cheapest shortcut dies |
| C2 | kill path unreachable? | WITNESS confirms 12/12 mutants differentially distinguishable before reveal (`c2-controls.stdout`) |

Both counters also **re-derive every evidence key themselves**: C1 re-extracts pointers at REV and keys rows by its own `(heading, ordinal, raw)`; C2 re-runs every dumped case and re-derives the oracle, and confirms each mutant kill by re-executing both variants and comparing full outputs modulo volatile sha keys (`comparable`, `c2/measure.py:188-197,342-343`). Neither counter trusts a seat-reported value.

## (b) Causal separability

### File touch-sets at REV (counter reads)

| file | C1 | C2 |
|---|---|---|
| `SKILL.md` (7 target sections) | yes (`c1/measure.py:368,206-231`) | no |
| `.ufo/evidence/round-21/coldread/measure.py` + `round-18/measure.py` (pinned judge) | yes (`:369-373`, executed) | no |
| `.ufo/evidence/round-49/c1/reads.json` | yes (`:64`, blob at REV) | no |
| `.ufo/evidence/round-21/coldread/ledger.json` | yes (via the monitor) | no |
| `corpus/SOURCES.md` | **yes** (7 SID pointers + VOLATILE) | **yes** (`c2/measure.py:271-285`) |
| `corpus/README.md` | **yes** (3 path pointers + VOLATILE) | **yes** (`c2/measure.py:288`) |
| `LOG.md`, `SCORECARD.md` | yes (2 line + 2 path pointers; VOLATILE) | no |
| `corpus/QUALITY.md` | yes (VOLATILE only) | no |
| `tools/staged-id-guard.py` | no | yes (pinned, `:45,253`) |
| `tools/pbt-staged-id.py` | no | yes (`:46`) |
| `corpus/knowledge/pbt-generator-pilot.md` | no | yes (`:48`) |
| hidden panel (outside lane) | no | yes (`--panel`, sha-pinned `:47,232`) |

**Files both counters touch: exactly `corpus/SOURCES.md` and `corpus/README.md`** (record files, read as REV blobs by both). Base census of the 90 pointers: 39 line, 35 path, 8 unresolvable, 1 external, 7 sid; per-section counts match FLOORS (34/10/17/5/5/9/10).

### Can C2 verify without C1 landed? — Yes.

C2's counter and controls never read SKILL.md, the monitor, the ledger, or reads.json. C1's landing edits (sections, reads.json, ledger re-key via `c1/refresh.py`) are invisible to C2's score. C2's controls were in fact already scored at the freeze commit `14d03ea` (`c2-controls.stdout`, rev field) before any C1 integration existed — direct evidence of separability.

### Can C1 verify without C2 landed? — Yes, with two shared-record caveats.

Counter-level, C1 needs nothing C2 produces. The schedule lands both in one candidate, and C1's design is already record-durable: the re-key binds ledger inputs to **non-record** files only and reads the five record files through `git cat-file blob CAND:…` (`c1/refresh.py` docstring + READ_CMD; contract `claims.C1.work_plan`), so C2's appends/edits to SOURCES/README cannot lapse credit. The residual ordering caveats are the two interference checks from (a): don't quote README's F10 line in any row (verified clean), and don't collide C2's new SOURCES row ids with S003/S004/S026/S041/S047/S049 (planned S182/S183 are safe). Neither caveat couples the counters; both are one-line greps the integration can assert before freezing the candidate.

## (c) A pattern worth a QUALITY criterion

**Proposed criterion — "Witness-bound measured claims."** Any measured claim whose score is produced by a frozen counter over seat-generated evidence must:

1. **Bind evidence by the counter's own derived keys at REV.** Receipts are matched on identifiers the counter re-derives from the judged tree (C1: `(heading, ordinal, raw)` from its extractor; C2: the seeded dump re-executed case-by-case), never on seat-chosen keys. *(Both counters satisfy this.)*
2. **Name the blind spot with a demonstrating control of each needed polarity.** Ship one control that *passes* the counter while exhibiting exactly what it cannot see (C1 CTL_K2: fabricated rows → PASS), and one that *fails* while exhibiting the cheapest cheating path (C2 CTL_FIX: fixture replay → 6/12 kills, total=10 → FAIL). A counter without such a control cannot distinguish "evidence is real" from "evidence is shaped to the checker."
3. **Confirm every kill/verdict differentially by re-execution.** A claimed mutant kill counts only when both variants are re-run on the counterexample and their full outputs differ (C2 `comparable`, `c2/measure.py:188-197,342-343`); a claimed located read counts only when the excerpt is re-located in the REV blob (C1 `:311`). No reported value is ever taken on trust.

Honourable second, from C1 alone: **durability by synthetic perturbation** — a "credit survives future record edits" claim must be verified by materializing the edit inside the counter (probe line appended to the five records in a `--shared` scratch clone, `c1/measure.py:336-366`) and re-running the unchanged judge on the perturbed commit, not argued from the re-key design. This is the general shape for any future "durable against X" claim.

## Risks

- **R1 (low, live):** C2's in-place README F10 edit is line-stable for C1's three whole-file README excerpts only because no row quotes that line; a future row or L1 `EXTRA_ROWS` quoting the F10 row would be broken by C2's edit (`excerpt_miss`). Mitigation: grep rows for `F10` before freezing the candidate. Observed clean this wave.
- **R2 (low):** a C2-cited SOURCES row id colliding with S003/S004/S026/S041/S047/S049 would resolve those SID pointers to two rows → `unresolved` (`c1/measure.py:176-181`). Planned S182/S183 safe; assert at integration.
- **R3 (hygiene):** C1 pins the monitor at the *live lane* path (`c1/measure.py:369-373`); stray working-tree edits under `.ufo/evidence/round-21|18` void setup even at a good REV. The receipts-only-after-REV rule keeps this quiet, but it is a real coupling worth a pre-deciding `git status` check.
- **R4 (acknowledged scope):** C2's frozen seed makes the claim "capability at seed 4949 against this guard"; overfitting to the seed is bounded only by the hidden panel. This is the contract's intent, not a defect to fix this round.
- **R5:** reads.json is not sha-pinned; it is whatever the candidate commit carries. Content checks make fabrication expensive (only mechanical fabrication passes, and only with section-consistent pointers), but reads.json bytes should be treated as part of the candidate, not of post-REV receipts.

## Verification (commands exercised)

- `read` of contract, both counters (full), both control harnesses, frozen selftest receipts, no-harm receipt, control summary receipts (not the three forbidden C2 stdout files).
- `sha256sum tools/staged-id-guard.py` → `03a796c5…2dca8`, equals `GUARD_SHA` in `c2/measure.py:45` and the contract.
- Pointer census via `python3` over `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json` → 90 pointers; overlap with C2 read-set computed from `c2/measure.py:45-48,268-291`.
- Record-pointer ranges extracted (README ×3 path, LOG.md:316-317, SCORECARD.md:13, SOURCES.md SIDs) and cross-checked against C2's planned edits (README F10 line 87; planned rows S182/S183 per contract `frontier_step.sources`).
- Wave-1 reader receipts scanned (`python3` over `w1/*.rows.json`): no `F10` text in any row excerpt; the three README rows quote §1/coverage-map material.
- No counter invoked (no drivers needed; frozen selftest receipts show 34/34 C1 and 11/11 C2 cases passing at freeze).

## Summary

- C1 and C2 share one design: blind-by-construction counters that re-derive every evidence key and name their blind spot with controls (C1 CTL_K2 passes on fabricated rows; C2 CTL_FIX fails on fixture replay, WITNESS proves reachability).
- C1 cannot see that anyone read, or that excerpts support sentences (`c1/measure.py:256-315`; contract `cannot_see`); C2 cannot see generation method or record semantics (`c2/measure.py:268-346`).
- No leak path between the counters; the only shared files are `corpus/SOURCES.md` and `corpus/README.md`, read as REV blobs by both.
- Causally separable both ways: C2 scored at freeze with zero C1 artifacts; C1's re-key reads records through blobs, so C2's record edits cannot lapse credit.
- Two one-line integration checks keep the peace: no C1 row may quote README's F10 line (verified clean), and C2's new SOURCES ids must not collide with S003/S004/S026/S041/S047/S049 (S182/S183 safe).
- Proposed QUALITY criterion "witness-bound measured claims": counter-derived keys, blind-spot-demonstrating controls, differential re-execution for every kill.
- Risks: live-lane monitor pin hygiene (C1), README F10 edit vs whole-file excerpts, SID-collision; all low and checkable pre-freeze.
