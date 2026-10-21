# ResVerdictCritic-5 — attack on the round24 recorded verdict

Seat: `TameshiR24-2.ResVerdictCritic-5` (critic, read-only; no "Run" in the item).
Tip inspected: `4903959687d16623adeeeae059bc010dcfc9d23f`. No tool installed or updated.
Only this file was written.

## Verdict

**"C1 improved (measured)" holds against the frozen contract. "Bounded by errata", as the
SCORECARD and LOG record it, does not.**

- The 1/11 → 11/11 move is real, and the frozen bounds absorb every wave-1 weakness. Nothing
  found requires the canonical judge to reject the claim.
- "numeric 8→8" is correctly stated: it was measured at base, after and tip. But that number
  cannot detect the calibration harm that wave 1 found, so it is not evidence that no harm was
  done.
- The recorded verdict understates its own bounds in four fixable ways (D1–D4 below). One
  consumer-facing calibration harm remains live at the tip (D2).

## Axes

- C1 predicate count (frozen ruler).
- Calibration honesty of the verdict record: SCORECARD, LOG, SKILL.md and the tool docstring.
- Restraint and depth (strict monitor).
- Registry battery.
- Source census.

## Strongest argument that the claim is NOT met, and whether it holds

**The argument.** The claim is "harden required-command binding against eleven named
… predicates routed by round23 critics" (`contract.json` claim). By the round's own record,
11/11 does not show hardening against the routed defects:

- K2 is author-added and K4 is a control (lesson Erratum I, `corpus/lessons/round-24.md:128-135`).
- The QUALITY48 execution note says K7–K11 "show a new capability, not a repair"
  (`corpus/QUALITY.md:506-510`). Under QUALITY48 that leaves K1, K3, K5 and K6 as repairs.
- For K2, K3, K4, K8, K9 and K11, a weaker implementation passes both the frozen ruler and the
  selftest, so nothing catches it (Erratum F, `:92-112`).
- The routed "bounded streams" defect is publication-only, with no redaction (Erratum E).
- The routed "live-dependent" defect is listed only in an undigested sidecar. The binding gate
  still certifies both live rows as ordinary receipts (Erratum M, `:160-170`).
- Worse, a refused `--run` into a reused `--out` leaves a stale pair that `command-binding.py`
  passes with exit 0 and `[]`. A refusal can therefore read as green (Erratum O, `:191-201`;
  `w1/CodePublish.md` F1, with a probe).

**Why it does not hold against the frozen bounds** (`contract.json:60-65`):

- Bound 1: "K1-K4 count selftest kills of four specific mutants, not general mutation
  adequacy". This absorbs the K2, K3 and K4 survivors (PredK2, PredK3, PredK4, MutFixtures).
- Bound 3: "K7-K11 test the new projection/plan CLI on synthetic fixtures; an actual replay
  run is separate evidence". This absorbs:
  - single-fixture K7–K11;
  - the `--project` validation gaps (CodeProjectInputs);
  - publication-only K9;
  - Erratum M's gate certifying live rows (actual-replay evidence, not a predicate);
  - Erratum O's stale `--out` (each K7–K9 case uses a fresh `fx/<name>-out`, `measure.py:159-167`).
- The claim text says "not a score uplift", and the predicate names are literal ("…-refused",
  "…-listed"). Each one is measured as named.
- K5/K6 are not vacuous. The pinned successors differ from the superseded rows only by the
  `"bundle_sha256": "…"` token (`tools/registry.json`, rows `command-binding-frozen-clean(-pinned)`
  and `command-binding-source-read-red(-pinned)`). At base, the substitution held (`before.json`
  K5/K6 `substituted: true`). So the after failure is attributable to the pin.

So the counterexample is a **tradeoff that the contract disclosed in advance**, not a reason to
reject the claim. What remains is fixable: the record must say this plainly where the verdict
is stated (D1).

Measurement grounding:

- `before.json`: 6a1821a, exit 1, instrument `0a7f6daa…`.
- `after.json`: c8c5b88, 11/11, exit 0.
- `final-verification.json` (untracked): at 4903959, ruler 11/11 exit 0 with the same
  `instrument_sha256 0a7f6daa…`, selftests 44/44 and 10/10.
- Retained replay `replay/{observations,bundle,expected,live-dependent}.json`: one vintage. Both
  revisions are `d2eaecd…`, the 43 names agree, and the pin matches. I checked this with a
  read-only python3 json/sha256 check whose output was
  `pin ok True`, `obs names==bundle names True`.

## Defects in the recorded verdict (counterexample → evidence)

### D1 — the bound set cited at the verdict is narrower than the errata the same commit wrote

- `SCORECARD.md:1156` verdict cell says "bounded by lesson Errata E–L", and `LOG.md:1630` says
  "lesson Errata E–L".
- `git show 250069f:corpus/lessons/round-24.md | grep -n Erratum` lists E, F, G, H, I, J, K, L,
  **M** and **N**. That is the same commit that wrote the SCORECARD and LOG text, and O–P
  followed at 4903959.
- The SCORECARD capabilities bound (`SCORECARD.md:1168-1170`) cites only "Errata E … and G".
  The capability text is "refuse to publish … list live-dependent rows" (`:1150`). Three errata
  directly bound that text and are not cited:
  - L: pin inputs are read from the working tree.
  - M: the gate certifies live rows. K10 inspects only the report.
  - O: a refused run leaves a stale, self-certifying green pair. SKILL.md's "writes only
    under `--out`" is false.
- The LOG findings list (`LOG.md:1622-1628`) omits:
  - live rows certified by the gate (M);
  - the stale green after refusal (O);
  - the false, unenforced superseded expectation, and `--tag new-r23` selecting 0 rows and
    exiting 0 (P);
  - the lack of row isolation (K).

  These are exactly the "live rows certified by the gate" findings the assignment names.

Impacted axis: calibration honesty of the verdict record. The count is not affected.

### D2 — refuted claims remain on the consumer-facing surface with no appended correction

- `SKILL.md:2052`, Write-scope cell: "writes only under `--out`". Erratum O (lesson `:200-201`)
  says this "is false as stated".
- `tools/registry-replay.py:9`: "each retained stdout/stderr is bounded by --max-stream-bytes".
  Erratum E says it overclaims, because `observations.json` holds 265,728 bytes.
- `tools/registry-replay.py:18`: "Writes only under --out." CodePublish F4 shows a global
  `post-checkout` hook writing outside `--out`, because `env()` strips the caller's
  `GIT_CONFIG_GLOBAL`.
- Last SKILL.md commit: `git log -3 -- SKILL.md` → `d2eaecd` (pre-wave). Round 23's precedent
  appended "Round23 correction (fresh falsification, appended; text above unchanged)" in
  SKILL.md itself (`SKILL.md:2033`). Round 24 appended nothing there, so a SKILL.md reader never
  sees Errata E or O.
- Not freezing tool bytes is defensible, since it protects the before/after pair. Not appending
  a SKILL.md correction is not: it is text, not tool, fixture, ruler or registry bytes.

Impacted axis: calibration (restraint in substance). The strict monitor cannot see this (see
the numeric note below).

### D3 — one of two harmed intermediates is undisclosed

- `.ufo/evidence/round-24/monitor-intermediate-A.json` records bd38c02, 47/62, restraint 6, with
  the note "harmed intermediate … after round24 implementation edits". It is retained but cited
  nowhere in SCORECARD, LOG or lesson. A grep for `intermediate` over those files and QUALITY or
  knowledge finds only B (`lesson:220`).
- Round 23 recorded every harmed intermediate next to its verdict (`SCORECARD.md:1060-1063`,
  `:1100-1102`). Wave-1 CorpusScorecard D2 asked for exactly this (`w1/CorpusScorecard.md`,
  "Smallest safe correction" item 2). It was not applied.

Impacted axis: calibration honesty (no-harm narrative). Restraint at the final revision is not
affected.

### D4 — the tip no-harm and capability evidence are not landed or cited

- The SCORECARD no-harm (`:1158-1161`) is at c8c5b88. The commits 250069f, 671a6e2 and 4903959
  then edited inputs the monitor reads. `ledger.json` references SCORECARD.md 11×, LOG.md 9×,
  QUALITY.md 24× and lessons/round-24 1× (read-only json count). B proves such an edit harmed
  restraint (60/62, restraint 6 at 250069f).
- The only tip receipt, `final-verification.json` at 4903959 (62/62, restraint 8, depth 8;
  registry 47/47 with 7 superseded; census 0), is **untracked**
  (`git status --porcelain` → `?? .ufo/evidence/round-24/final-verification.json`) and uncited.
  Its note records a discarded first attempt (ENOSPC on /tmp).
- The capability row's Evidence cell still reads "`.ufo/evidence/round-24/` final receipts"
  (`SCORECARD.md:1150`), which names no file. It does not say that the actual replay refused
  0/43, so refusal is shown only on synthetic fixtures (CorpusScorecard D1, unapplied).

Impacted axis: provenance of no-harm. No harm is shown in fact.

## Axis harm check

| Axis | Base | After / tip | Harmed? |
|---|---|---|---|
| C1 count | 1/11 (6a1821a) | 11/11 (c8c5b88, 4903959) | improved within bounds |
| restraint / depth | 8 / 8 at 6a1821a (`w1/RunMonitor.md:40`); 8/8 at 549ede2 (r23 `final-verification.json`) | 8 / 8, 62/62 at c8c5b88 (`noharm-c8c5b88.json`) and 4903959 (untracked `final-verification.json`) | no (numeric); intermediates A, B harmed then restored |
| registry | 46/46 active, 4 superseded (r23 final) | 47/47 held, 7 superseded | no; superseded `command-binding-selftest` fails 38/38 vs 44/44 by design (Erratum P) |
| census | exit 0, 81 rows | exit 0, 83 rows; W04 dup-url lines concern S047–S081 only [INFERENCE: pre-existing] | no |
| calibration honesty of the record | — | D1–D4 | **yes, on text surfaces (fixable)** |

**On "numeric 8→8".** The statement is correct and matches contract bound 4 ("numeric
calibration stays 8 unless separately justified"). The base and after values are measured, not
borrowed. But restraint = 2·(`~` boxes 1–4) plus box-3 ledger credit (`w1/RunMonitor.md:36`), and
`SHONEN.md` is byte-identical from base to rev (`:40`, "this ruler does not discriminate the
round-24 delta"). It cannot register D2's false SKILL.md and docstring statements. "8→8, no
other axis harmed" is therefore true of the instrument and silent on that harm. The record
should say so, not imply that calibration was checked for harm.

## Smallest safe correction (append-only; L1 decides; no tool, fixture, ruler or registry bytes)

1. Append a correction under SCORECARD's round-24 measured section and in LOG:
   - The verdict is bounded by lesson **Errata E–P**.
   - The capabilities row is additionally bounded by L, M (the gate certifies live rows) and O
     (refused run → stale green; "writes only under `--out`" false).
   - The actual replay refused 0/43; refusal is shown on synthetic fixtures only.
   - Repoint "final receipts" to `after.json` and `final-verification.json`.
2. Append "Round24 correction (fresh falsification, appended; text above unchanged)" after
   `SKILL.md:2057`, following round23's `:2033` pattern. State:
   - writes are not confined to `--out` (git hooks run; caller git hardening is stripped);
   - the stream bound is publication-only, with no redaction;
   - a refused run does not clear an earlier bundle;
   - the gate's clean verdict covers the two live rows.
3. Disclose `monitor-intermediate-A.json` (bd38c02, 47/62, restraint 6) beside B.
4. Land `final-verification.json` and cite it as the tip no-harm. Note that restraint 8 is
   structurally blind to text overclaims.

   Because steps 1–3 touch monitored text, re-measure the strict monitor after them. If it
   drifts, re-anchor and retain the intermediate, as B was.

The verdict text then becomes: improved (measured, within the frozen bounds); numeric 8→8,
delta 0; bounded by Errata E–P.

## What I checked (read-only)

- Inspected: `contract.json`, `measure.py`, `before.json`, `after.json`, `noharm-c8c5b88.json`,
  `final-verification.json`, `monitor-intermediate-A.json` and `-B.json`, `replay/*`,
  `replay-command.json` and `replay-gate.json`.
- Corpus and surfaces: SCORECARD 1127–1170, LOG 1589–1631, `lessons/round-24.md` 1–220,
  knowledge 40–96, QUALITY 487–523, SKILL.md 2030–2060, `registry-replay.py:1-26`,
  `tools/registry.json` rows.
- Seat reports: CorpusScorecard, CodePublish, CodeProjectInputs, ClosureCarry and RunMonitor,
  plus the outcomes and accounting (64/64 completed, 0 dead, `finding_ids []`).
- Read-only git with `GIT_OPTIONAL_LOCKS=0`:
  - `git show --stat` for 6a1821a, 04657a6, 250069f, 671a6e2 and 4903959;
  - `git log -3 -- SKILL.md`;
  - `git show 250069f:corpus/lessons/round-24.md`;
  - `git status --porcelain`.
