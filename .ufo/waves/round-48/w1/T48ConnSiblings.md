# T48ConnSiblings — sibling-lane patterns for round-48 C1/C2 (adjacency report)

Seat: T48ConnSiblings (leaf, no subagents). Read-only scan of sibling `*-shokunin`
lanes on the fleet. Nothing absorbed; recommendations only. Companion to the
round-48 contract (C1 calibration R=3; C2 freshness re-anchoring S026/S048/S093/S108).

---

## Part A — standing values whose command is nondeterministic (C1-adjacent)

### A1. kama — repeat count + agreement counter + refusal to certify on disagreement
- `kama-shokunin/tools/instrument-agreement.py:169-171` — prints `IA runs=N agree=A disagree=D digest=<sha256 prefix>`;
  exit 0 iff `disagree==0`, else exit 1. Default `--runs 3` (:122).
- `instrument-agreement.py:89-97` — selftest has an explicit `nondeterministic` arm
  (`agree=2 disagree=1`): nondeterminism is *declared and refused*, never laundered into a pass.
- Receipt embeds per-run digest/exit/stdout_head + declared `normalize` rules:
  `kama-shokunin/.ufo/waves/round-30/c2/receipt-a.json`.
- `kama-shokunin/SCORECARD.md:1589` — round-30 C2 row: "selftest … with the nondeterministic
  arm `agree=2 disagree=1`, two receipts `IA runs=3 agree=3 disagree=0`"; capability row `:1605-1606`.

### A2. audio — per-cell verdict DISTRIBUTIONS with counts (not point pins)
- `audio-shokunin/corpus/fixtures/measure_audio.py:448-479` — `fifo_hold_ladder_entry` records
  per-{feed,hold} cell `verdict_distribution` signature→count, "not a point pin"; a hold is
  `rep-stable` iff its **entire distribution equals the pinned arm's signature**; `None` when no
  hold in the ladder is rep-stable (:476-479).
- `audio-shokunin/SCORECARD.md:712-714` — r70 ladder: "6 holds × 2 feeds × 10 reps, per-cell
  verdict distributions"; verifier ×3 replay identical (`:685-686`).

### A3. game-dev-3d — honest mode envelopes, MAP as stable witness, explicit unpins
- `game-dev-3d-shokunin/SCORECARD.md:172` — "`jolt_threaded` child.log is NOT byte-stable
  (refusal-block count 11–12 observed; tolerance ≥8 never stressed below 11 — the MAP is the
  stable witness)".
- `:178` / `:184` — refusal band "stochastic ~475–575, 50%-point session-dependent"; two pinned
  points sit ~450 statements clear; "a two-point ladder cannot see inside".
- `:219` — multi-overlap order "honestly unpinned (`seqeq=-`/`pairs=-`) — verified as live flips
  by two independent seats". `:259` — "deferred-pin census kept unpinned by design".

### A4. game-dev-2d — measured bins + quantified jitter + honest mode admission
- `game-dev-2d-shokunin/SCORECARD.md:60` — regimes pinned {0–198}/198.05–198.35/≥198.5;
  "TIMEOUT truncation nondeterminism + duplicate-write splice edges (boundary)".
- `:64` — "edge ≈198.3–198.5ms stochastic ~1ms"; `:71` — probe meta "8 cells × 3 reps";
  `:199` — "honest mode admission, not a deterministic re-pin".

### A5. mori — quantified flaky admission with root cause (never restated as a standing value)
- `mori-shokunin/SCORECARD.md:417-421` — flaky-failure class admitted: grep-over-pipe SIGPIPE
  race at `tools/mori-census.sh:1783/:1809`; "admission seat ~25% false-FAIL in one battery;
  parent determinism battery 1/8 (55/56 …)" — root-caused, bounded, recorded as a defect.

### A6. chousa — commit-only rerun accounting with seeds
- `chousa-shokunin/SCORECARD.md:1603` — "130/130 twice … Re-derived by wave 2: 130/130 in
  6 further runs (RerunCounterA, RerunCounterB ×2, ScoutFreshnessH ×3)".
- `:1673-1676` — a rerun labeled "run 2" whose seed has **no committed output** is excluded from
  the count ("No separate committed output or receipt for the run 2 seed … so it is not included
  in the count of 5").
- `:1817` — seed-paired receipts (32101/32102 ×2); `:1911-1915` — 650/650 ×3 on fresh seeds
  after rebinding to the committed landed bytes.

### A7. kake — "two consecutive probes" rule; 3 identical sweeps at deciding
- `kake-shokunin/SCORECARD.md:94` — before-state: "pin-failure framed as 'two consecutive probes'
  (r3+r7)"; after-state "Standing claims re-verified against live state 22:47–22:50Z (3 timer
  sweeps + manual re-probe identical 12/5/1; 18-curl replication 0-diff)".

### A8. kengaku — R=3 parse for a standing forecast
- `kengaku-shokunin/SCORECARD.md:968` — "F1 true (812×3 parse)".

### A comparison — C1 (R=3, value sets, attested members, deps D) vs siblings

| C1 element | sibling analogue | status |
|---|---|---|
| R=3 | kama default 3; kengaku 812×3; chousa ×3 seeds | compatible |
| attestation (observed or committed receipt) | chousa commit-only reruns (:1673-1676) | compatible |
| deps set | tameshi round-21 env-diff profiles (own `SCORECARD.md:1522/2184/2276`) | compatible |
| value class stable / nondeterministic | kama declares-and-refuses; audio distributions; 3d envelopes; mori rates | C1 is *more permissive* |

Divergences where siblings are stricter (cheap-pass surface):
1. **No frequencies per member.** audio records full signature→count distributions (10 reps/cell);
   3d asserts the MAP with an explicit floor; kama refuses certification on any disagreement.
   C1's V is a bare set — a dominant-mode value with a rare outlier still passes as a valid
   2-member `nondeterministic` class if the outlier was observed once.
2. **No proof that multimodality belongs to the instrument, not the harness/environment.**
   Round-47's `six-leg regression ledger` FAIL was exactly a one-off P0 environmental flake; with
   R=3, declaring {FAIL passed=7, PASS passed=9} would pass, where siblings would refuse (kama),
   require a distribution + stability floor (audio), corroborate via independent seats (3d :219),
   or quantify + root-cause (mori).
3. **Observation receipts lack execution traceability.** chousa counts only committed, seed-linked
   rerun artifacts; kama receipts embed per-run digests. C1's "recorded as a P0 tuple … in a
   committed observation receipt" could be satisfied by hand-authored JSON.
4. **`stable` on 3 agreeing runs of a genuinely flaky command.** mori needed 25%/1-of-8 to expose
   its flake; audio used 10 reps; kake demanded two consecutive probes. A flake rate <1/3 silently
   passes as `stable`.

---

## Part B — re-anchoring held source rows (C2-adjacent)

### B1. kasegi — supersede rows + snapshot manifests with sha pins + honest archival notes
- `kasegi-shokunin/corpus/SOURCES.md:35-36` — S029 "supersedes S024 —", S030 "supersedes S022 —"
  (new rows open `supersedes`; old rows kept). `:39-40` — `recheck` cadence column
  (`730d`/`180d`/`on-release`).
- `kasegi-shokunin/corpus/QUALITY.md:48` (Q7) — "A pinned captured-source comparison is not a
  fresh network verification." `:50` (R8) — immutable row fields ⇒ new row beginning
  "supersedes S### —"; never edit old rows. `:65-66` (R11/R12) and `:77` (R13) — recheck
  instruments must cover the entry's own source ids, fail closed, and be shown load-bearing.
  `:89` (R15) — open defects carry runnable closure checks.
- `kasegi-shokunin/corpus/source-snapshots/round-23/manifest.json:3` — purpose: "verifies captured
  bytes, not current upstream freshness"; `:10` — `archival_note: "pre-round-32 capture; fetch
  instant not recorded"` (absence of a fetch receipt is explicitly recorded, not faked).
- `kasegi-shokunin/SCORECARD.md:407-408` — `source-recheck.py --manifest …` exit 0 ×3.

### B2. audio — per-row anchor location pins + date-conditioned recheck + superseded-fetch provenance
- `audio-shokunin/corpus/SOURCES.md:23-24` — S014/S015 supersede rows with exact `l.` anchors in
  the source; `recheck: on-release`.
- `audio-shokunin/corpus/QUALITY.md:9-13` (Q1-Q5) — provenance fields, version pinning, recheck
  must reproduce stated numbers on host; `:28-30` (Q20-Q22) — used-by completeness and control
  oracle independence.
- `audio-shokunin/corpus/live/r94-scout/RECEIPTS.md:23` — fetched sources pinned by
  `sources/FETCHED-SOURCES.sha256`; `sources/*.txt` (branch `main`) "is a superseded first fetch,
  kept only for provenance" (never overwritten).

### B3. kake — live re-verify at deciding with repeated sweeps; drift detection
- `kake-shokunin/SCORECARD.md:93-94` — standing claims re-verified against live state at the
  deciding window; PQ-12 loop armed and **caught a transition in-round** (:93); 18-curl
  replication 0-diff; pin failure must show as two consecutive probes.

### B4. kengaku — SUPERSEDED as a census status
- `kengaku-shokunin/SCORECARD.md:885` — P4 IDs: "48 MATCH/1 SUPERSEDED/2 offline groups";
  `:625` — re-verified every PROVINCE surface (`test -e`/`ss`/`sha256sum`) and re-opened
  23 public sources.

### B5. kotodama — per-claim retrieved-passage ledgers
- `kotodama-shokunin/SCORECARD.md:49` — "historical source rechecks: per-claim retrieved
  passages, access limits, contradictions and unresolved outcomes (13 supplemental ledgers /
  148 audits)".

### B comparison — C2 (snapshot + receipt + ≤25-word Gate quote + live check + entry re-pointing)

| C2 element | sibling analogue | status |
|---|---|---|
| superseding row opens `supersedes T —` | kasegi R8 (:50); audio S014/S015 (:23-24) | matches |
| committed snapshot + sha256 pin in anchor | audio FETCHED-SOURCES.sha256; kasegi manifest sha256 | matches |
| fetch receipt (url/fetched_at/http_status/sha) | kasegi *records absence* of fetch instant (manifest :10) — C2 is stronger | C2 stronger |
| quote located in extracted snapshot text | kasegi manifest quotes (substring + digest); audio `l.` anchors | matches |
| live re-fetch at deciding | kake live re-verify + 3 sweeps (:93-94); kasegi Q7 "not a fresh network verification" | matches |
| entries re-pointed (source/verified-at) | kasegi R8 immutable-field discipline; audio used-by lists | matches |

Cheap-pass surface:
1. **The deciding-time kill rule checks fetch *success*, not byte equality with the committed
   snapshot.** If the live fetch returns 200 but different bytes, nothing in the contract (as
   written) stops the target being counted refreshed while the snapshot — and every quote anchored
   to it — is stale. kake's PQ-12 caught exactly this silent-drift class in-round (:93), and
   their 3-sweep protocol is the guard. Recommendation: the deciding run must additionally require
   live sha == snapshot sha; mismatch ⇒ target not refreshed (or an explicit re-snapshot).
2. **Receipt and snapshot are both locally authored; nothing binds the receipt's `http_status 200`
   to a real fetch at build time** (seats run `--no-live`). By design the deciding run is live,
   but chousa's commit-only/seeded-receipt discipline (A6) is the analogue worth importing: record
   the raw fetch log or response headers in the receipt so a fabricated receipt is distinguishable
   later.
3. **Single-shot live fetch vs kake's 3 sweeps** — a transient failure fails the target
   (conservative), but a single success may be served from cache/proxy; this is a robustness note,
   not an exploitable pass.
4. C2 verifies the quote is *located* and phrase-bearing, not that it *supports* the entry's claim
   (audio Q5 / kasegi Q7 require rechecks to reproduce the stated numbers). Out of scope for the
   counter; noted only.

---

## Part C — sibling rules that would catch a cheap pass the round-48 contract misses

1. **kama agreement-refusal** (`instrument-agreement.py:169-171`): any disagreement among runs ⇒
   exit 1, receipt carries `disagree=D`. Would catch a `stable` label on a command that flaked
   within the R=3 window (round-48 accepts `stable` if all 3 agree; a 1-in-3 flake passes).
2. **audio verdict-distribution counts** (`measure_audio.py:448-479`): standing values should carry
   counts per member and a rep-stability floor — would catch a rare-outlier 2-member
   `nondeterministic` class.
3. **game-dev-3d independent-seat flips** (`SCORECARD.md:219`): multimodality should be
   corroborated outside the author's own run set before it becomes a co-equal standing member.
4. **mori quantified-flake admission** (`SCORECARD.md:417-421`): a flaky outcome should be
   quantified, root-caused, and bounded — round-48 lets one observed outlier enter V as an equal
   member without any of that.
5. **chousa commit-only execution-traceable receipts** (`SCORECARD.md:1673-1676`): attestation
   receipts should embed raw per-run output/seeds so a hand-written receipt cannot attest
   unattested tuples.
6. **kake two-consecutive-probes + live-mismatch detection** (`SCORECARD.md:93-94`): C2's
   deciding run should compare live bytes to snapshot sha; a 200 with different bytes must not
   count as refreshed.
7. **kasegi Q7** (`QUALITY.md:48`): "a pinned captured-source comparison is not a fresh network
   verification" — the deciding-time live check is the only freshness evidence; keep the build-time
   snapshot+receipt pair from being presented as freshness anywhere (C2 already separates them).

---

## Method / bounds
- Read-only over sibling lanes; no edits, no installs (read/grep only; no tooling changes to
  record). No scratch left behind; no network calls.
- All citations verified by direct read/grep on the fleet checkout at `f1cfaad…` (tameshi lane).
