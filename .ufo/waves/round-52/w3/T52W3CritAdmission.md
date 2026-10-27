# T52W3CritAdmission — adversarial claim admission review at CAND1

Seat: critic. Scope: admission review of C1 (operability) and C2 (calibration) at CAND1
`7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`. Everything below is probe evidence, not a verdict;
the deciding run is the L1's single invocation. Contract, counters, controls, lesson, SCORECARD
block and wave-2 findings were read first; contract.json and lessons/round-52.md untouched.

## Question 1 — would either claim verify only through a forgery or a narrowed reading?

### C1 (operability): verifies at CAND1 without forgery; residuals are named, not blocking

- The frozen C1 counter ran to completion at CAND1 (wave-3 probe, non-deciding):
  `held=49/49 not_held=0 dropped=0 mte_row=0 c3_covered=30 c3_total=0 r21_cases_missing=0 total=0 C1_R52_PASS=true`
  (`.ufo/waves/round-52/w3/T52W3ExecC1Probe.stdout`, last line). The wave-2 probe's single
  missing unit (C3 `selftest-cell-commands=3`) is repaired at CAND1 — the round21 row Self-test
  cell carries exactly one backticked span (measured: 1 span,
  `python3 -c '...sed -n 2157p...'` against `git show 7ff81a5b:SKILL.md`).
- The one softened spot — the round21-measure self-test now reads the fleet root, so it passes
  "in a fresh clone outside the fleet" only on a host that has `/home/vgpnk/Projects/shokunin` —
  is **pre-registered, not post-hoc narrowing**: contract C1 `sourced` declares the fleet-bound
  reading, SOURCES row S274 (Bazel hermeticity) was opened this round and is cited by
  `corpus/lessons/round-52.md` (## Gate). The honesty cost is real but declared
  (`.ufo/waves/round-52/w2/T52W2ExecC1Probe.md` §6).
- Residual risks that bound the claim's meaning (none fire at CAND1):
  - lane-edit-reachable counter holes: base-active drop via `superseded`, C3 PASS-token parse,
    dual stale needles, `None/None` needle (`.ufo/waves/round-52/w2/T52W2MutC1Survivors.md`);
  - a held row's needle meaningfulness is unobservable (contract C1 `cannot_see`;
    `.ufo/waves/round-52/w1/T52W1CritC1.md`).

### C2 (calibration): is a genuine calibration move, but with current reader outputs the round's
### deciding combination (C2 PASS **and** no-harm OK) is reachable only through a forgery

- Calibration by the sizing rules, yes: m1/m3 count mismatches between lane records (SKILL.md
  leg-count phrases, runner pointers) and the tree (`tools/mte-interop.py` LEG_TABLE,
  `tools/mutate-and-run.sh` ranges); m4/m6 count ledger records against reader files; m5 a
  ledger cell. Before 27 → target 0 (`.ufo/evidence/round-52/c2/measure.py:3-31`).
- At CAND1 the frozen counter prints `total=0 C2_R52_PASS=true` — but m6 is **vacuous**:
  `t52_entries=0` (`.ufo/waves/round-52/w3/T52W3ExecNoHarm-c2.out`). The m6 guard activates
  only after the re-key.
- Measured admission conflict (all runs in a `--shared` scratch clone, fixture commits
  `a83de73a…` honest / `137f0b37…` forgery; production instrument
  `.ufo/evidence/round-52/coldread/refresh.py` + frozen round-21 monitor):
  - no-harm at CAND1 already fails one monitor: `NOHARM coldread-floor score=6 credited=45 RED`,
    the other 10 monitors ok (`.ufo/waves/round-52/w3/T52W3ExecNoHarm-noharm.out`).
  - Honest re-key (each of the 19 sections keyed with exactly its reader's recorded findings):
    the frozen monitor prints **score 6, credited 54/64** — 10 sections vetoed
    `wrong-expectations:4,3,2,2,2,2,1,1,1,1` (18 findings kept). The frozen floor
    (score>=8 AND credited>=64, `.ufo/evidence/round-52/no-harm.sh`) is RED.
    Receipt: `.ufo/waves/round-52/w3/T52W3CritAdmission-honest-rekey-monitor.json`.
  - Forgery variant (same entries, readers' findings dropped, `wrong_expectations` zeroed):
    monitor prints **score 8, credited 64/64** — floor OK.
    Receipt: `.ufo/waves/round-52/w3/T52W3CritAdmission-forged-rekey-monitor.json`.
  - The frozen C2 counter prints `m1=0…m6=0 total=0 C2_R52_PASS=true` on **both** fixtures
    (`.ufo/waves/round-52/w3/T52W3CritAdmission-c2-honest.stdout` vs `-c2-forged.stdout`).
    m6 cannot see the omission: an empty findings list trivially passes `check_findings` and
    `wrong_expectations==len(findings)` holds at 0 (`.ufo/evidence/round-52/c2/measure.py:63-76,117-129`;
    source-level confirmation by `.ufo/waves/round-52/w3/T52W3MutRefresh.md`, "Ignore findings
    for one heading" row).
- The 18 findings are real, not reader noise: the independent applied-fix falsifier records the
  same residue (Fix03:11 stale `first-four specs :657-839`; Fix03:12 stale
  `nine dispatches :1384-1428`; Fix04:2 stale literal `/tmp` pointer at SKILL.md:1321; Fix04's
  duplicated `(ten since round 51)` qualifier at :1305 —
  `.ufo/waves/round-52/w3/T52W3RevApplied1.md`).
- So, unless the L1 lands another honest fix+read cycle, admitting C2 together with a green
  no-harm requires either (a) dropping recorded findings — a forgery invisible to every frozen
  counter — or (b) adjudicating reader findings away — selection the wave-3 protocol forbids
  ("no selection by the L1"). An honest stop (no-harm RED, round fails) is the third option.

## Question 2 — is "no axis harmed" plausible given the re-key?

- Only the coldread floor moves with the re-key commit: it adds `.ufo` evidence only; tools-scope
  untouched; r45-freshness measured identical on the honest fixture (population=74, fresh=71,
  score=9, `C1_R45_PASS=true`) vs CAND1; the other 10 monitors read tools//corpus bytes the
  commit does not change (peer receipt `T52W3ExecNoHarm-noharm.out` shows them ok at CAND1).
- The floor, though, is decisive: the round-21 monitor credits a section only when its re-key
  entry records zero findings (`.ufo/evidence/round-18/measure.py:459-494` — any positive
  `wrong_expectations` fails and vetoes, measured), and the frozen floor demands all 64 back.
  With 16/19 readers delivered, 10 sections carry findings (2 readers still pending; the honest
  ceiling of 54 can only shrink). **Conclusion: no-harm is not plausible under an honest re-key
  with the readers' outputs as they stand.** This conflict was pre-visible:
  `.ufo/waves/round-52/w2/T52W2CritRekey.md` warned that honest nonempty findings make monitor
  credit impossible and that the L1 controls the submitted findings.

## Named risks (pointer each)

1. **R1 calibration/no-harm conflict** — honest re-key fails the frozen floor (54/64, score 6);
   only a findings-dropped ledger reaches 64/64. Evidence: the two monitor receipts above;
   `T52W2CritRekey.md`.
2. **R2 m6 completeness gap** — empty-findings entries pass m6; omission of recorded findings
   is invisible to the frozen C2 counter. `.ufo/evidence/round-52/c2/measure.py:63-76,117-129`;
   `T52W3MutRefresh.md`.
3. **R3 reader-record provenance** — the committed refresh validates quotes against
   *working-tree* reader files and accepts caller-supplied READERS_JSON; it does not bind seats
   to committed reader JSON records, so a re-key can claim a read no reader performed and m6
   cannot detect it. `.ufo/evidence/round-52/coldread/refresh.py:106-150,219-229`;
   `T52W2CritRekey.md` (selective omission / read identity).
4. **R4 C1 host-binding** — `round21-measure-selftest` and the C3 round21 row are held only
   where the fleet root exists at the absolute path; declared via contract `sourced`+S274 but
   it moves an environment dependency into a registered gate row.
   `.ufo/waves/round-52/w2/T52W2ExecC1Probe.md` §6.
5. **R5 C1 counter holes** — supersede-drop, PASS-token parse, dual/`None` needles reachable by
   lane edits; none fire at CAND1. `.ufo/waves/round-52/w2/T52W2MutC1Survivors.md`.

## Smallest safe correction

- Preferred: land one more honest fix pass for the 10 sections' recorded findings and re-read
  those sections (the round extends; the honesty mechanism stays intact). 
- Acceptable: honest stop — report the conflict; do not zero findings (kill rules and
  `T52W2CritRekey.md` both point this way).
- Prohibited: dropping/zeroing reader findings to clear the floor, or L1 adjudication of
  findings; either fakes the calibration axis's honesty guard.
- Structural (route to a later round, not this one): bind each reader's canonical JSON record to
  a committed revision and have m6 compare the ledger's findings/counts against those records
  rather than quote-substrings alone (`T52W2CritRekey.md`, smallest binding).

## Tooling / bounds

- No installs or upgrades (nothing needed); pacman untouched. 
- Scratch root `/fast/scratch/hyaku/tameshi-r52/T52W3CritAdmission` created, one shared clone,
  two fixture commits (toplevel asserted before each), fully deleted before yield.
- Lane read-only except this report and the four copied receipts under
  `.ufo/waves/round-52/w3/T52W3CritAdmission-*`; no git/jj mutation in the lane or fleet.
- Probe, not verdict: 3 out of 19 wave-3 readers (T52W3Read18/19, and T52W3Read11 delivered
  after my fixture was built with a zero-finding fallback — its actual report has 0 findings, so
  the honest ceiling of 54 stands) had not reported at probe time; the deciding run is the L1's.

## Summary

- C1 verifies at CAND1 without forgery (frozen counter total=0, wave-3 probe); its fleet-bound
  reading is pre-registered via contract `sourced` + S274, with named residuals.
- C2 is a genuine calibration move, but at CAND1 m6 passes vacuously (0 T52 entries).
- Measured: honest re-key → monitor 54/64, score 6 → frozen no-harm floor RED; findings-dropped
  variant → 64/64, score 8 → floor OK; frozen C2 prints total=0 PASS on both (m6 completeness gap).
- With 16/19 readers delivered, 10 sections carry 18 real findings (corroborated by the
  applied-fix falsifier); the honest ceiling of 54 can only shrink as the last readers land.
- Admitting C2 with a green no-harm is therefore reachable only via a forgery invisible to the
  frozen counters or via prohibited L1 selection; the honest alternative is a further fix+read
  cycle or an honest stop.
- No other axis is harmed by the re-key commit (freshness and 10 further monitors verified/peer-
  verified unchanged); no-harm stands or falls entirely on the coldread floor.
