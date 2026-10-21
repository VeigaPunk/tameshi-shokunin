# Round24 — routed hardening is repaired only when it can fail

author: tameshi (CloseTameshi22, round24 L1 coordinator)

## Claims

C1 calibration, tied lowest numeric axis: eleven frozen hardening
predicates, 1/11 at 6a1821a8897eea6e7d9669292160ec9593669409, target 11/11
(`.ufo/evidence/round-24/contract.json`, ruler `measure.py`, `before.json`,
landed e338f1bd0749a1786d95d3d3cd9572bb10757667 before any seat). K4 (the
any-token mutant) was already killed at base and is kept as a control,
not a repair. These predicates are capability checks, not historical
defects, and numeric calibration stays 8.

## Gate

Admit candidate: `knowledge/replay-projection-hardening.md`,
`tools/registry-replay.py`, the round24 selftest fixtures and the pinned
successor registry rows.

Reject:
- calling a routed defect "fixed" before its predicate fails at base and
  holds after;
- reading four mutant kills as general mutation adequacy;
- reading realpath identity as write isolation;
- reading pinned digests as producer authentication.

Flip condition: an independently retained, applicable execution or
authority record.

S084 opened 2026-10-21 UTC: https://docs.python.org/3/library/os.path.html,
section `os.path.realpath`, first paragraph (Python 3.15.1 docs). Located
quote: "Return the canonical path of the specified filename, eliminating any
symbolic links encountered in the path". The same section says non-strict
mode "may still contain links or loops" for missing components. This is why
the row is scoped to identity, not isolation.

S085 opened 2026-10-21 UTC, own-work
`.ufo/waves/round-23/fresh-adjudication.json` at 6a1821a, lines 53–104,
`routed_not_executed`. Located quote (line 66): "do not pin bundle_sha256
literals, so a regenerated bundle and expected pair would still hold".

Both new rows start as mined, with recheck on-release (S084) or on-change
(S085), used by this lesson and the new knowledge entry. No existing row's
status, recheck or used-by changes.

Bounded lookup: identified 2, screened 2, included 2, excluded 0.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| falsifier-coverage / unmeasured hardening | Round23 `original-outcomes2.json`: 34/64 dead, including all 20 reviewers. `fresh-adjudication.json` `routed_not_executed`. Closure rounds[421]: any-vs-all mutant probe | QUALITY15/29 cover nondiscriminating fixtures, but no criterion required routed gaps to become failing predicates | QUALITY48 plus the frozen ruler. At base: K1–K3 mutants survive the 38-case selftest, K5–K6 substituted bundles still hold their rows, and K7–K11 have no tool, giving 1/11. The after measurement is recorded below once executed. |
| dangling promise / unmeasured after | this lesson's row above and `SCORECARD.md` round-24 section promised an after measurement "below"; none was retained at c8c5b88 (w1 CorpusLesson, ScribeLimits, PredK2, CorpusQuality48) | QUALITY6 (executed outcome in the same entry) | `.ufo/evidence/round-24/after.json` landed 04657a63fd140451a487aa8a6c333663f7061685. Shown able to fail: `git cat-file -e c8c5b88:.ufo/evidence/round-24/after.json` exits 128; at 04657a6 it exits 0 |
| single-fixture predicate over a multi-trigger guard | K10 sets `external` and `non_hermetic_argv` in one row; K7/K8/K9/K11 each use one fixture shape (w1 PredK7–PredK11, MutProject, MutPlan) | none → QUALITY49 | QUALITY49. Shown able to fail: MutProject's remove-external-classification mutant leaves frozen K10 discriminated (only the tool selftest kills it); MutPlan's drop-sibling-realpath mutant survives both selftest and K11 |
| wave dispatch / predecessor death | validator refused role `labrat` (`.ufo/waves/round-24/validation1-refused.stderr`); attempts 1–2 refused 64/64 at the 100-job cap (`dispatch1-attempt1.json`, `-attempt2.json`); CloseTameshi22 died with the session inside its retry loop | swarm validator (`unknown_role`); job-cap retry rule | role replaced before the validated payload; replacement L1 dispatched the same validated payload unchanged at attempt 3 (`dispatch1-attempt3.json`: 64 spawned, 0 refused) |

## After measurement (replacement L1 TameshiR24-2, 2026-10-21)

CloseTameshi22 died with the host session before measuring after. The
replacement L1 measured the unchanged frozen ruler (sha256 `0a7f6daa…`, as in
`before.json`) in a private clone at c8c5b88c8e961a929cdc351b95a7074c76958909:
11/11, exit 0 (`.ufo/evidence/round-24/after.json`). Seat RunRulerAfter
reproduced 11/11 and RunRulerBase reproduced the base 1/11 byte-identically.

Honest reading of 1/11 → 11/11:
- K4 is a carried control, so ten predicates were movable: 0/10 → 10/10.
- They cover seven mechanisms. K1/K2 mutate one argv comparison, K5/K6 test
  one digest-pin mechanism on two rows, and K7/K8/K9 end in one refusal branch.
- K7–K11 failed at base because `tools/registry-replay.py` was absent. That is
  a new capability, not the repair of a defective tool; round23's `replay.py`
  is unchanged.
- K2 (case-fold) was author-added, not a routed defect.

No-harm at c8c5b88 (`noharm-c8c5b88.json`): strict monitor 62/62, restraint
8, depth 8, overrides false; registry 47/47 held, 7 superseded, exit 0.
Census exit 0 at base 6a1821a (81 rows) and at c8c5b88 (83 rows).

## Fresh wave 1 — what the 64 falsifiers found (append-only errata)

The claim holds as measured. These findings bound it; none was repaired in this
round. Changing the tool, fixtures or ruler after the only falsification wave
would leave the change unreviewed and invalidate the frozen before/after pair.
Seat reports are under `.ufo/waves/round-24/w1/`.

- **Erratum E — the stream bound is publication-only.** `--run` writes complete
  streams to `observations.json` before `--max-stream-bytes` is checked; the
  retained file is 265,728 bytes. Redaction, half of the routed defect, is not
  implemented. The docstring line "each retained stdout/stderr is bounded" and
  the knowledge row "unbounded retained streams" overclaim (CorpusEntry,
  CorpusContract, ClosureCarry, PlanWalk, SentinelRun).
- **Erratum F — single-fixture predicates.** Weaker implementations that pass
  the frozen ruler, and what (if anything) catches them:
  - K2: case-folding only `argv[0]` — nothing (PredK2).
  - K3: `abs()` or truthiness exit comparison, or a sign-blind negative-exit
    check — nothing (MutFixtures, PredK3).
  - K4: last-token-only, case-insensitive or whitespace-stripped matching —
    nothing (PredK4).
  - K1 and per-token prefix matching: per-token prefix survives the selftest
    (MutFixtures).
  - K7: first-row-only check, `held is False`, skipping external rows,
    publishing under another filename — `held is False` is caught by the
    selftest only (PredK7).
  - K8: reading `cleanup_error` only when not held — nothing (PredK8).
  - K9: counting characters instead of bytes, or first row only — nothing
    (PredK9, MutProject).
  - K10: dropping either live-dependent disjunct — the selftest only
    (PredK10, MutProject).
  - K11: siblings not resolved — nothing (PredK11, MutPlan).
  - K5/K6 record no failure reason, so a content failure would also be
    credited (PredK5, PredK6). They test the row pins, not tool-side digest
    enforcement, which the selftest's `tampered` case covers.
- **Erratum G — projector input validation.**
  - `--project` publishes bundles that `command-binding.py` refuses with
    exit 2 (string/bool/missing `got`, duplicate/empty names, malformed
    requirements, short revision, relative cwd).
  - A lone-surrogate stream crashes with exit 1 instead of 2.
  - `--project` cleanly binds a requirement that no frozen registry declares
    (CodeProjectInputs).
  - Unavailable inputs in `--run` exit 1, not 2.
  - `--plan` on a missing repo exits 0.
  - A refused run leaves an earlier bundle in the same `--out` (CorpusSkill).
  - A symlinked sibling is mirrored under its target name, and two siblings
    with one target crash (PredK11, LabPlanLaneLink).
- **Erratum H — `revision_pinned` means "not declared live".**
  `mutate-and-run-regression` executes against live kagi objects through the
  sibling symlinks. It is counted among the 41 (OverlapKagi, ProvinceFit).
- **Erratum I — routed accounting.** Of the eight round23 routed defects:
  - six have frozen predicates;
  - the runner digest is implemented (and verified by RevRunnerHash), but has
    no predicate, which contradicts QUALITY48's own counting rule;
  - redaction is dropped;
  - the loose stdout tokens are left frozen, a no-retrofill decision that was
    never recorded until now (ClosureCarry, PlanWalk).

  The contract's "eleven routed" wording overstates this.
- **Erratum J — documentation.**
  - The selftest's fixture loader fails opaquely (`fixture-unavailable`, no
    path).
  - `SKILL.md` names only the round23 fixture file and omits the
    `registry-replay-selftest` row (CodeFixtureLoader, CodeAnchors, CorpusSkill).
  - The README row's evidence path `{contract,measure}.py/json` does not
    resolve (CorpusReadme).
  - S084's lesson paragraph narrows realpath's three stop conditions to
    "missing components" (SourceS084).
  - S085's range 53–104 clips the array (SourceS085).
- **Erratum K — security (SentinelRun).** The clone does not isolate row
  writes. Rows inherit the caller's environment and secrets. Output writes
  follow symlinks. Interruption can skip child cleanup.

Routed to round25 (unexecuted): split single-trigger fixtures for K7–K11;
an exact-failing-case attribution in a new ruler; exit-2 input handling and
consumer-equivalent validation in `--project`; clearing `--out` on refusal;
sibling-name mirroring; capture-time stream bounds and redaction; a
`--run` selftest; a registry row over the committed round24 observations.
- **Erratum L — pin inputs read from the working tree.** `--run` reads the
  frozen requirements/baseline pair from the ambient filesystem and binds it
  only to itself, not to `--rev`. No registry row pins the round24 replay
  bundle (OverlapKumitate, ClosureCarry). Routed to round25.
- **Erratum M — the gate certifies live rows.**
  - `project()` publishes all 43 rows, the two live-dependent ones included,
    as ordinary receipts. `replay-gate.json` (exit 0, `[]`) therefore
    certifies `pin-disposition-read` and `verify-round15` too. The 41/2
    split exists only in the report and the unpinned
    `live-dependent.json`. K10 inspects only the report.
  - The replay bound the round23 43-row set at d2eaecd, not the 47 active
    rows at c8c5b88.
  - Clone git failures exit 1, not 2.
  - The clone omits `core.hooksPath=/dev/null` (CodeRunReplay). Routed to
    round25.
- **Erratum N — the replay selftest is independent but thin.** No expected
  outcome is derived from the tool. However:
  - the selftest never reads `bundle.json`, `expected.json` or
    `refused_rows`;
  - its over-limit stream case is stderr-only;
  - the `--run` guards (registry digest pin, frozen-requirements equality)
    are tested neither by the selftest nor by the ruler;
  - the round24 fixture digest `6ad7842f…` is pinned nowhere
    (CodeSelftestOracle, CodeFixtureLoader).

  Routed to round25.
- **Erratum H addendum.** `round21-measure-selftest` also reads sibling
  object stores through the mirror symlinks (`tools/round21-measure.py:73-77`)
  while counted as revision-pinned (RevLiveRows). The seat's further claim
  that the kagi pin was pruned is refuted. It cited `feece8743`; the actual
  pin `fecee874` resolves (`git -C kagi-shokunin cat-file -t fecee874` →
  `commit`), and the row held at c8c5b88 (`noharm-c8c5b88.json`). The
  round23→24 bundles differ in 17 rows' bytes, none in exit codes or tokens.
  13 of the 41 "pinned" rows carry run-varying bytes, so `bundle_sha256` pins
  the stored capture only (RevBundleDiff).
- **Erratum O — `publish()` is non-atomic and the clone runs hooks.**
  - A stale pair left in `--out` after a refused run still passes
    `command-binding.py` with exit 0 and `[]`, so a refused run reads as
    green.
  - The three files are written in sequence without temp+replace.
  - An unusable `--out` exits 1 with a traceback.
  - `env()` strips a caller's `GIT_CONFIG_GLOBAL`, and the clone omits
    `core.hooksPath=/dev/null`. An operator's global post-checkout hook ran
    and wrote outside `--out` in the seat's /tmp probe (CodePublish).

  The SKILL.md row's "writes only under `--out`" is false as stated. Routed
  to round25.
- **Erratum P — a superseded expectation is false and unenforced.**
  Superseded row `command-binding-selftest` still runs and fails: it expects
  `38/38`, the tool prints `44/44`. Superseded rows do not count toward
  `held`, so the battery stays 47/47 (`noharm-c8c5b88.json`). Other details:
  - The successor's anchor (`fresh-adjudication.json:53-59`) cites "38
    cases [seat inference]", not 44.
  - `--tag new-r23` now selects zero active rows and exits 0. There is no
    `total == 0` guard; this is round17 F5, still open.
  - `registry-replay-selftest` is absent from `SKILL.md` (CodeSupersession).

  Routed to round25.

### Mistakes addendum (replacement L1)

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| seat misroot | RowAudit01 wrote its report to the fleet root, at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-24/w1/RowAudit01.md` (sha256 `3bc5633c…`), despite the wave context's absolute-path rule | prompt §6.3 misroot sweep | copied byte-exact into the lane (`cmp` 0) and the fleet copy removed. Shown able to fail: the sweep `git -C /home/vgpnk/Projects/shokunin status --porcelain` listed `?? .ufo/waves/round-24/`, and after removal it no longer does |
| errata append drifted the source monitor | QUALITY.md append at 250069f → monitor 60/62, restraint 6 (`monitor-intermediate-B.json`) | strict monitor input-drift | two actual traced re-reads (`source-traces-B/`) restore 62/62 at 671a6e2. Shown able to fail: the retained B receipt |

## Residual review — corrections, not additional capability claims

Eight ordinary reviewer/critic seats examined the receipts and append-only
corrections after wave 1. Their reports live under
`.ufo/waves/round-24/residual/`. No production tool, frozen fixture or
registry expectation was changed. The following statements supersede the
broader wording above.

- ResAfterRuler and ResErrataCritic found inconsistent mechanism grouping.
  The eleven predicate counter remains authoritative. Splitting stream-size
  from held/cleanup yields seven moved groups (argv, exit, digest pins,
  held/cleanup refusal, stream-size, live listing, identity) plus unchanged
  stdout K4. Merging all refusal returns yields six moved plus K4. Neither
  taxonomy is an additional breadth improvement.
- Erratum I's "never recorded until now" is false without the qualifier
  "in round24 prose": round23 fresh-adjudication line 104 and lesson lines
  109–112 already recorded the loose-token choice. A successor row could
  strengthen it without retrofilling the frozen pair; no such work landed.
- Erratum H's kagi example is not exhaustive. Both unlisted rows read
  live sibling object stores, including kumitate, tsukuroi and mado as well
  as kagi. RunRegistry's malformed-layout 45/47 run versus fleet-layout
  47/47 run demonstrates the dependency; CodeLiveList independently names it.
  The pruned-pin assertion remains refuted (actual `fecee874` resolves).
- Separate executed from inferred results: MutFixtures, MutProject,
  MutPlan, LabPlanLaneLink, CodeProjectInputs and CodePublish retain executed
  probes. PredK4/8/9/10/11, the sign-blind variant in PredK3, and the
  zero-active-tag exit in CodeSupersession are static seat inferences, not
  additional executions by this L1. Errata F/G/P must be read with that
  qualification. MutProject M05/M06 execute the two disjunct deletions.
- Omitted limits are retained here: MutProject M07/M08/M09 (schema,
  requirement-name type, stream-type guard removal) survived both detectors.
  PredK10's sidecar-deletion and all-rows-live variants are unexecuted seat
  inferences. ClosureCarry's dropped-token projection and CodeSelftestOracle's
  bundle-byte/digest handoff weaknesses are also code-derived inferences.
  No landed test validates the handoff or a two-token projected requirement.
  K8 refines K7's label on the real runner; a nondefault-limit-always-refuses
  mutant can pass K9 but is caught by the existing at-limit selftest
  [seat inference, CorpusContract]. Selected revision code runs with caller
  authority; a clone is not isolation. Duplicate observation rows can also
  corrupt report counts (CodeProjectInputs).
- S085's teaching cell "each" overclaims: six of eight routed items have
  predicates; clone-runner digest is observed but unpredicated, loose tokens
  stay open, and stream redaction is absent. Its defect text is at lines
  53–104 within the full array at 48–106. S084's default `strict=False`
  stops at missing components, symlink loops or OSError; the warning is not
  restricted to missing components.
- The QUALITY49 Mistakes row's fix is **not shown able to fail**. Its probes
  motivate a rule but no conforming fixture was landed. The separate
  missing-after-receipt row supplies this round's failure-backed frontier
  fix (`git cat-file -e`: 128 at c8c5b88, 0 at 04657a6). QUALITY49 is
  narrowed append-only to acknowledge both loop positions and QUALITY29/15.
- ResVerdictCritic's consumer-surface criticism is accepted: SKILL now
  directly warns about publication-only limits, unconfined writes, stale
  green pairs, inconsistent invalid-input exits and live receipts. The
  immutable tool docstring's original stronger assertions are not reliable.
  SCORECARD/LOG now cite Errata E–P and both harms: A at bd38c02
  (47/62, restraint 6), B at 250069f (60/62, restraint 6).
- ResMonitorReanchor reproduced B and its exact prefix preservation.
  Its reruns at 671a6e2 and 4903959 give 62/62, restraint 8. The L1 final
  receipt at 4903959 is `final-verification.json`. Scratch paths in traces
  are historical observations, not promises that those directories persist.
- ResAccounting confirms 64/64/0 and exact membership. Its D1 allegation
  about the misroot pointer is rejected: line 219 actually names the fleet
  source `/home/vgpnk/Projects/shokunin/.ufo/waves/round-24/w1/RowAudit01.md`,
  not the lane destination. The earlier copy/cmp/remove was observed by the
  L1; a new sweep receipt records current absence, not a fabricated rerun
  of the historical copy. The accounting gate validates retained declared
  callbacks, not provider authentication.

No general mutation-adequacy, producer-authentication, historical R17
coverage or promotion claim follows from the measured eleven predicates.
