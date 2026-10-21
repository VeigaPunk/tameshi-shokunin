# AxisBound — critique: "calibration 8 unchanged" + fewer named defects (round-19 C1)

Scope: attack only the axis/no-harm framing of claim C1 (five routed round-18
metadata/receipt defects 0/5 → 5/5 at frozen baseline
`7243e7f163f08978c8fd9b6c1ef67a2fefe7d190` → delivered `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`,
numeric calibration asserted to remain 8). Grounded in
`corpus/lessons/round-18-verifier-spotcheck.md` §5 and named committed files.
Advisory only; no production edits; no lane tools re-executed (evidence-verified
from committed blobs, receipts and the parent's current-monitor receipt, per the
round-18 verifier's own method).

## Strongest counterexample — C1's corrections themselves broke the claimed unchanged axis (fixable defect, unadmitted as of 21e79329)

Evidence: uncommitted-but-retained receipt
`.ufo/evidence/round-19/current-ledger-monitor-21e7932.json` reports
`calibration_restraint_score: 6`, `coldread.box3_full_page: false`, at the
delivered revision — versus the baseline-era monitor 60/60, restraint 8
(`final/measure-final-60.json` at `a85f710`, and the round-19 replay
`round18-final-measure.json` at `4b7c682`). The errata/receipt appends that
earn C1's 5/5 invalidated ~11 cold-read buckets (49/60 covered). Meanwhile the
committed `SCORECARD.md` tail says "Calibration remains **8**, a dated
historical score".

If the report claims "numeric calibration remains 8" while the only
current-revision measurement says 6, the claimed unchanged axis is already
harmed by the deliverable — a self-inflicted regression of exactly the class
the no-harm clause exists to exclude. The claim as audited
(`after-21e7932.json`: `corrected=5, open=0` at `21e79329`,
`ruler_sha256 c538c33d…`) satisfies the defect-count unit but is blind to this
harm because `measure.py` `evaluate()` checks only the five frozen predicates.

**Falsifier (primary)**: run the frozen round-18 cold-read ruler at the
delivered revision → `calibration_restraint_score` < 8 and/or
`sections_covered` < 60 means C1 cannot be admitted under "calibration
unchanged" unless (a) the repair restores it, or (b) the report scopes "8" to a
named dated revision AND commits the current monitor as a named receipt with
its observed value. Option (b) still risks a judge ruling the axis harmed;
option (a) is the only clean admission, but must not be manufactured (below).

**Impacted axes**: calibration (direct), quality (if the dip is concealed or
laundered), discernment (whether "remains 8" was re-verified at the delivered
revision or merely asserted).

**Smallest safe correction**: commit the current monitor receipt, qualify every
"remains 8" as "at `4b7c682`/`a85f710`, dated", and either (i) land the
bucket-refresh so a committed monitor at the final revision reads the restored
value, or (ii) declare the observed 6/49-60 with a bounded explanation. Never
quote the historical 60/60 without its revision label.

## Secondary counterexamples / rule mismatches for the repair plan

1. **Refreshed buckets are not the original cold-read credit.** The 60/60 at
   `a85f710`/`4b7c682` was non-author wave-2 reads. Refreshing invalidated
   buckets via L1 author reads changes provenance: the refreshed monitor may be
   admitted as a *maintained ledger* but MUST be labeled author-read with
   per-bucket carried/refreshed distinction (the documented `--carry` /
   `carried_from` mechanism covers carries, not re-reads). A restored 60/60
   produced by author re-reads MUST NOT be presented as equivalent cold-read
   credit, or C1's repair recreates the defect class it is fixing (receipt
   provenance overstated).
2. **External-input buckets may be unrefresherable.** The monitor's
   `external_inputs` cover dozens of cross-repo blobs. Any bucket whose input
   digest cannot be reproduced byte-equal at the delivered revision must stay
   `could-not-evaluate` — crediting it from memory or paraphrase fabricates
   coverage.
3. **Instrument sha missing on one new receipt.** `round18-final-measure.json`
   binds argv/revision/stream digests but carries no `tool_sha256` for
   `.ufo/evidence/round-18/measure.py` (the `bash-witness-selftest-complete.json`
   receipt does pin `tool_sha256` + `runner_sha256`). This contradicts the
   lane's own round-18 falsifier ("a receipt cited for a claim must print the
   runner sha256 equal to the landed blob", `corpus/lessons/round-18.md` — a
   line the R18-4/R18-5 erratum sits 40 lines below). Fix: append the
   instrument sha field/erratum, or extend the ruler to require it.
4. **Erratum R18-1's supersession is simultaneously over-broad and incomplete.**
   It claims to supersede "every staged/PENDING landed-tip statement" at a
   13-line list, but `grep -n PENDING` at `21e79329` yields lines
   2,10,53,65,91,97,114,118,120,122,132,136,143,173,174 — the list misses
   ~143 (EG-1, already resolved by a wave-2 erratum) and ~173–174, and lines
   118/120/122 carry live analysis (O_RDWR write-capable, pycache prefix,
   root-execve) that is NOT stale; only their trailing "PENDING" markers are.
   `QUALITY.md` criterion 37 (new, same commit) requires auditing every
   staged/PENDING mention — the correction under-satisfies its own rule.
   The ruler does not catch this (`guard()` checks only four tokens in the
   post-erratum tail: `line 2`, `Effective verified-at:`, `921ef807…`,
   `18 mutation survivors`). Smallest fix: append a dated clarifying erratum
   scoping supersession to PENDING markers only and naming EG-1 as
   previously-resolved.
5. **Duplicate-authority guard.** The frozen contract's population is five
   items; a "current monitor" is a sixth measurement surface. Keep it
   explicitly labeled monitor/not-claim-authority (the parent's stated plan)
   so C1 admission rests solely on the frozen five — no second claim.

## What holds (observed, not inference)

- `before.json` at baseline: corrected=0, open=5, exit semantics consistent;
  `after-21e7932.json`: corrected=5, same `ruler_sha256` — genuine
  failure-capable before/after pair on one ruler, input digests persisted.
- Ruler is non-trivially failure-capable: strict-JSON (duplicate-key,
  non-finite), digest-bound receipts with exact argv/revision/exit/stream
  checks, and a synthetic-mutant selftest covering missing-erratum,
  wrong-digest, tamper and unsuperseded cases (`measure.py` selftest mutants).
- No-harm on surfaces verified: `tools/` and `corpus/knowledge/fleet-kill-rate-ledger.md`
  untouched in `7243e7f1..21e79329`; append-only on LOG (+35/−0), QUALITY
  (+33/−0), README (+17/−0), SOURCES (+9/−1, the one deletion is the allowed
  S049 used-by cell); knowledge/lesson diffs are appended errata only;
  fleet `.ufo/reports/round-18/tameshi.md` unchanged (R18-5 repaired by
  evidence, not rewrite — matches the verifier's first disjunct).
- R18-1..R18-5 predicates all resolve true at `21e79329` against committed
  bytes (checks.json probes row revision=`921ef807` exit 0 digest-matches
  `probes.stdout` `d37c99e3…`; S008 row has 13 cells, idx8=`mined`,
  used-by includes the case file at all of `7243e7f1`/`21e79329`/`4b7c682`;
  witness complete receipt `VERDICT: PASS`, `43/43`; measure stdout
  revision/rev_input=`4b7c682`, overrides_used=false, 60/60, restraint 8).
- The failed first scratch run (`bash-witness-selftest.json` exit 1,
  FileNotFoundError on missing `tools/mutate-and-run.sh`) is retained and
  explicitly superseded — correct handling, not laundering.
- `receipt()` does not check optional `runner_sha256`/`tool_sha256` when
  absent — consistent with finding 3 (unpinned instrument passes).

## Minimal defensible acceptance

Admit C1 iff ALL hold at the committed delivered revision: (1) same
`ruler_sha256` reports corrected=0 at `7243e7f1` and corrected=5 at the tip,
with input digests persisted (observed); (2) the "calibration remains 8"
statement is either backed by a current-revision monitor ≥8 restored via
provenance-labeled maintained-ledger refresh, or explicitly revision-dated
with the current monitor receipt committed and its observed value quoted
verbatim (currently fails: monitor says 6, SCORECARD says "remains 8"
unqualified); (3) every new receipt cites instrument sha or the lesson
erratum names the omission; (4) supersession errata cover only stale
markers, never live analysis (finding 4 needs a narrowing erratum); (5) the
18 guard survivors and other residuals remain open with unchanged tool bytes
(observed). The defect-count claim is real and measured; the unchanged-axis
assertion is the load-bearing vulnerability and is the canonical falsifier.

## Sources / commands

All checks by revision-pinned blob reads (`git show REV:path`,
`git diff --numstat`, `git ls-tree`) under
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; receipts read at
`.ufo/evidence/round-19/` (committed and working-tree). No lane tool,
selftest or gate re-executed; `measure.py` was read, not run (copy inspected
at `/tmp/r19-measure.py`, sha `c538c33d…` matches receipt field). Round-18
verifier §5 items 1–5 mapped to R18-1..R18-5 in `contract.json`.
