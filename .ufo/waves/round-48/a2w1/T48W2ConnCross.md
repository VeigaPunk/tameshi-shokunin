# T48W2ConnCross — cross-claim evidence-discipline scan (C1 calibration × C2 freshness)

Seat: T48W2ConnCross (connector, Godspeed, leaf). Item: compare the evidence discipline of the
C1 rows and the C2 rows — both restate an observation of a live surface (a command's output;
a web page) — across repeat counts, attestation, snapshot pins, live checks and deciding-time
drift; name what each claim's discipline catches that the other's misses; name the coupling;
recommend one generalising QUALITY criterion with a falsifier sketch.

Method: read-only. No counter was executed (nothing in this item needs a probe; every finding
below is from the frozen files themselves). Line refs are to the frozen counters
(`.ufo/evidence/round-48/{calibration,freshness}/measure.py`, sha256 per freeze-2.json), the
contract (never edited), the deciding script, and the content revision `c7586b9a`. Digest and
count checks were recomputed on disk and via `git show`; outputs quoted as observed.

## 1. The two disciplines side by side

| Axis | C1 (calibration) | C2 (freshness) |
|---|---|---|
| Repeat count | R=3 rounds × 6 profiles per statement, + up to 6 extra P0 observations per statement for rare members (`calibration/measure.py:392,533`); attestation probability disclosed (`contract.json:31`) | One fetch per URL at authoring (the snapshot), one live fetch per URL at deciding (`freshness/measure.py:336-351,430`); no repeats, no class |
| Value class | `stable` / `nondeterministic` declared per row; oversize refused (`contract.json:41`, amendment 3) | none — `refreshed` is binary per target |
| Attestation | In-invocation observation only; committed receipts "never attestation" (amendment 4, `contract.json:31`) | Lane-authored receipt *is* evidence, but only its sha256 is verified against the snapshot; `fetched_at`/`http_status`/`tool` are trusted text (`freshness/measure.py:263-285`) |
| Snapshot pins | statements.json sha (in code), BASE hard-coded and refused otherwise, per-row tool sha256 prefix verified against `git show REV:file`, counter self-pin, append-only SCORECARD (`calibration/measure.py:343-347,410-417,570-584`) | snapshot sha256 prefix in the registry row's anchor cell, receipt sha256 == snapshot digest, receipt url ∈ row urls, self-pin (`freshness/measure.py:241-285,439-446`) |
| Live check | Executes the pinned tools from a clone of REV (bytes == pinned bytes by construction), whole picked line + exit compared across rounds (`calibration/measure.py:304-341`) | One 60 s urllib fetch; verdict = a ≤25-word quote is a substring of the live extracted text; live-vs-snapshot byte equality never required (`freshness/measure.py:336-351,435`) |
| Deciding-time drift | FLEET lines: census-script digest + lane cleanliness + sibling HEADs at rounds+1 points; `fleet_drift=1` fails the predicate (`calibration/measure.py:369-390,470-474`) | none for the web surface beyond quote presence; none at all for the census validator it executes live (`freshness/measure.py:96,379-394`) |

## 2. What C1's discipline catches that C2's misses

**F1 — the single-fetch restatement, with zero transient budget.**
C2 credits a target on exactly one live fetch at the deciding run; `unreachable` is "reported,
never credited" (`contract.json:118` kill rule; acceptance at `freshness/measure.py:430,435`).
A 60-second network transient at the deciding minute zeroes the whole claim; there is no
repeat count, no unreachable-class, no attestation arithmetic. This is precisely the defect
class round 47 routed as "a single flaky observation was restated as a standing value"
(`contract.json:77`), and it is why C1 carries R=3 + classes + disclosed attestation
probability (`contract.json:31`). C1's posture applied to C2 would fetch 3× and distinguish
"quote removed" (stable-absent → miss) from "surface unreachable" (class → declare).
Show: `python3 .ufo/evidence/round-48/freshness/measure.py --lane LANE --rev REV --no-live`
prints `live=skipped` as acceptable — the only live-discipline probe a seat can run.

**F2 — whole-output drift vs a 25-word substring.**
C2's live check is `quote in extract(raw)` (`freshness/measure.py:351`): the page may be
substantively rewritten (numbers, context, surrounding claims) while the quote survives, and
`refreshed=1`. C1 compares whole picked lines across three rounds and pins the tool digest
(`calibration/measure.py:319-347`), so output drift *within* its invocation is a MISMATCH.
The only sha equality C2 ever checks is receipt↔snapshot (`freshness/measure.py:283`);
snapshot↔live is unbound. (On disk the four receipt↔snapshot pairs are consistent — S026
`a4c5c46b4af9`, S048 `e9cbc3e1ab7c`, S093 `2cb77df2f4be`, S108 `04e4c091715a`; observed via
`sha256sum` against each `.receipt.json`. The seam is live↔snapshot, not receipt↔snapshot.)

**F3 — unbound provenance text.**
`check_receipt` verifies url membership, sha256==digest, `bytes` present
(`freshness/measure.py:263-285`); it cannot verify `fetched_at` (date prefix only) or the
`tool` field, and no live re-observation can see a fetch date. A snapshot fetched last year
and relabelled `fetched_at: 2026-10-26T…` passes every offline check C2 runs. C1 refused
exactly this class for its own receipts: "a lane-authored receipt is unbound text and could
attest any value" (`contract.json:31`, amendment 4). The committed receipts are internally
consistent (fetched 08:40–08:41Z 2026-10-26, sha256 match, byte counts match) — this names
the seam C1's rule would close, not an observed forgery.

## 3. What C2's discipline catches that C1's misses

**F4 — cross-artefact digest chaining; C1's report evidence is unbound and unchecked.**
C2 binds three artefacts across two stores: registry-row anchor prefix ↔ committed snapshot
bytes ↔ receipt sha256 (`freshness/measure.py:241-285`); substituting any one breaks the
chain at deciding. C1's analogue artefacts — the observation receipts under
`.ufo/evidence/round-48/calibration/observations/` — are report-only (`contract.json:31`),
carry no digest binding to anything the counter recomputes, and are absent from the deciding
run's FROZEN set (`deciding-run.sh:22`): silently editing them changes no verdict and no
receipt. Show: `ls .ufo/evidence/round-48/calibration/observations/` — nothing anywhere
re-hashes those files.

**F5 — external rot is re-observed live; C1 cannot see outside the repo at all.**
C2 re-fetches the network at the deciding run (deciding-run.sh:32 runs the counter with live
on); a source that removed the quoted content fails there. C1's surface is repo-internal; its
only external sensors are the census-script digest and sibling HEADs
(`calibration/measure.py:369-390`). Web rot between authoring and deciding is invisible to
C1 by construction.

**F6 — observation-tool provenance.**
C2's receipts record the fetching tool (`tool: curl 8.23.0 …`, observed in all four
`.receipt.json`). C1's FLEET lines record only the census digest — no versions of git, bwrap,
jj or node, whose presence defines its deps semantics (`calibration/measure.py:87,369-390`).
A host tool upgrade between rounds that shifts deps behaviour would leave no provenance trail
in C1's receipts. (C2's `tool` field is itself unchecked trusted text — same seam as F3.)

## 4. Coupling

**X1 (declared, `contract.json:94`) — the registry count value couples C1 to C2's artefacts.**
The first C1 statement `sources-registry` restates `rows=N` from the v2 census run inside the
REV clone (`calibration/measure.py:255-262`; statement pins
`.ufo/evidence/kaika-round-1/sources-census-v2.sh`). C2's rows S265–S268 move N from 124 to
128 — observed: `git show 473336d9:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
→ 124; same command at `c7586b9a` → 128; the standing row at `c7586b9a:SCORECARD.md:2332`
declares `rows=128 … runs 3 stable` (round-47 row at `:2268` declared 124). So C1's row at
the content revision requires C2's four rows to be *present and v2-well-formed*; if they
vanished at REV the count drops, observation says 124, the row declares 128 → MISMATCH.
One-way only: C1 needs C2's artefact *presence*, never its *verdict* — C2 can fail while C1
passes, and junk rows that keep the v2 CLEAN verdict (13 fields, valid enums, used-by
present) shift the count with no defender: the no-harm monitor is a floor (`>=124`), and C1
attests whatever count the row declares as long as observation matches. Lineage: the same
coupling was recorded at round 46 (`c7586b9a:SCORECARD.md:2241`, rows=120 over C3's rows);
what is new in round 48 is that the counted artefact is produced by a *live-network* claim.

**X2 (discovered) — the fleet census validator is executed live by C2, digested only by C1.**
C2's `census_exit` runs `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` from the
live fleet filesystem against REV-materialised bytes (`freshness/measure.py:96,379-394`);
the deciding run runs it on the live lane worktree (`deciding-run.sh:33`). C1 records the
script's sha256 prefix at rounds+1 points and fails on change (`calibration/measure.py:369-390,470`)
but never executes it. Consequences: (a) validator drift between freeze and deciding is caught
only if it lands before C1's first FLEET point — drift in the C2→C1 window of the deciding
run is invisible to both counters (fleet_drift compares only C1's own four points); (b) the
pre-registration census receipt (`.ufo/evidence/round-48/census-start.exit` = 0) pins no
validator digest anywhere, so freeze→deciding validator integrity rests on C1's in-run FLEET
lines alone. X2 is the exact mirror of F3: C2 trusts live *code* the way C1 distrusts lane
*text* — and neither claim binds what the other relies on.

**X3 (discovered, minor) — the deciding script's step-0 comment overstates the freeze surface.**
`deciding-run.sh:5-6` says FROZEN_UNCHANGED covers "the C2 snapshots and receipts", but the
FROZEN list at `deciding-run.sh:22` omits `.ufo/evidence/round-48/freshness/sources` (and
`calibration/observations`). Un-scorable either way — the snapshots legitimately post-date
the freeze (committed at `5054532`, after freeze `7552984`), C1's observations are
non-attesting, and C2's in-band chain covers the snapshots at REV — but a reader auditing the
freeze boundary from the comment would mis-audit. It is a contradiction between comment and
implementation sitting exactly on the boundary between the two pinning architectures
(freeze-set diff vs in-band digest chain).

## 5. Recommended QUALITY criterion (one, generalising across both claims)

> **Bound-or-reobserve, never once.** Every value a standing record restates from a live
> surface (command output, web page) must, at scoring time, be traceable to evidence that is
> either (a) *digest-bound* — a sha256 of the observed bytes recorded where the claim's
> record lives, verified against those bytes — or (b) *re-observed* — reproduced by the
> counter in the same invocation that scores the claim. A value resting on exactly one
> observation that is neither digest-bound nor re-observable is a miss, not a verdict, and
> must be declared (class + observation count), never silently restated as standing.

Both round-48 claims are partial instances: C1 implements (b) with repeats and classes but
binds nothing its counter doesn't re-run (F4); C2 implements (a) for bytes but leaves
provenance fields and the live comparison unbound (F2, F3), and its live axis is a single
unclassed observation (F1). The criterion names the shared rule without favouring either
architecture.

Falsifier sketch: in a scratch lane, (i) relabel a C2 receipt's `fetched_at` to the required
date over snapshot bytes truly fetched a year earlier — the digest chain still closes, the
quote is still live, so the record credits a value (fetch date) that is neither bound nor
re-observable; (ii) attest a C1 row member from a committed observation receipt the counter
never re-runs (pre-amendment-4 behaviour). A counter honouring the criterion declines both
(`UNATTESTED` / not refreshed / declared-class-only); if either prints PASS, the criterion is
falsified. Both halves are one-command reachable: (i) is `sed` on a receipt + the frozen
`--selftest` fixture, (ii) is exactly what amendment 4 already killed — the criterion merely
states the rule both fixes instantiate, extended to provenance fields and live code (X2).

## 6. Risks and non-goals

- F1 is a risk sketch, not an observed failure: all four receipts on disk show http 200 at
  08:40–08:41Z 2026-10-26 and digest-consistent snapshots; the live check outcome at the
  deciding run belongs to the L1's single deciding invocation.
- Adopting the criterion verbatim would bite the frozen C2 design (fetched_at is not
  retroactively bindable); it is a recommendation for the lesson/QUALITY ledger, not a
  proposed change to this round's frozen predicate, contract, or counters.
- No counter was run and no scratch tree was needed; nothing was written outside this report.
  Attempt-1 connectors T48ConnCorpus (R=3 corpus grounding) and T48ConnSiblings (sibling-lane
  patterns) were checked for overlap — neither compares the two claims' disciplines; the
  round-46 precedent `SCORECARD.md:2241` is cited as lineage at X1.
