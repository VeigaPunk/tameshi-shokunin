---
name: tameshi-shokunin
description: Domain specialist — verification-fixture craft. Rank: shonen (probation).
---

# tameshi-shokunin

verification-fixture craft playbook. Probation seed — rounds 1-3 build the corpus from
measured surfaces; every rule below must earn a cited source before it
counts. Nothing here is oral knowledge.

## Standing rules

- Read-only substrates unless PROVINCE.md declares a write surface;
  detection-and-report for operator-owned remediation.
- Secrets shape-only, never content-read.
- Every claim: measured anchor (path:line, command output, evidence id).
  Observation / inference / unknown stay separate.
- Errata append-only; rejections kept.

## Source notes (probation wave 1)

The sections below distil the three survey notes written this wave; every rule
cites its note line. The notes label each claim O (observation) / I (inference)
/ U (unknown); inferences carried below keep the (I) mark.

- `corpus/knowledge/gates-survey-kumitate.md` — the six kumitate suites: exit
  maps, case counts, mutation controls, fail-closed arms, verdict asserts.
- `corpus/knowledge/gates-survey-kagi.md` — the six kagi gates: exit lattice,
  POLICY refusals, five evidence-discipline habits, findings F-1/F-2.
- `corpus/knowledge/verification-patterns-fleet.md` — the shared verifier shape
  (P1–P10, ≥2 independent lanes) vs two lane-specific encodings.

The notes are live artifacts — the kagi survey records its own line numbers
moving mid-survey and pins refs to a sha (gates-survey-kagi.md:420-438). All
refs below were re-resolved by line number on 2026-10-14; a reader on a
differing revision re-resolves rather than trusts.

## Gate-shape decision table — hermetic vs live vs audit-lane

| Shape | Answers | Runs against | Green means (and only means) | Source |
|---|---|---|---|---|
| **Hermetic suite** (`--selftest`) | does the tool's own machinery work | fixtures under `mkdtemp` only, cleaned in `finally`; no live path read | every asserted case fired on generated data; passes in any repo state | gates-survey-kumitate.md:19-31 |
| **Live gate** (default mode) | what the current substrate state is | the live host/tree, read-only | measured counts on the verdict line; exit lattice 0/1/2 (usage 64) | gates-survey-kagi.md:24-31, 75-88 |
| **Audit lane** | do claims about a named revision still hold | retained outputs + the committed revision | per-claim verdict (`CONFIRMED`/`UNVERIFIABLE`); byte-identity first | verification-patterns-fleet.md:28-35, 69-74 |

Rules:

- **Hermetic means no live path is read.** All six kumitate suites build
  fixtures under `mkdtemp` and remove them in `finally`
  (gates-survey-kumitate.md:28-31); claims-check's hermeticity is proven from
  outside by env poisoning — `UFO_SRC=/nonexistent … --selftest` → PASS
  (gates-survey-kumitate.md:218-222). A live assertion inside a suite stays
  gated (`--integrations`), never smuggled into the hermetic group
  (gates-survey-kumitate.md:51-58).
- **A live gate may not pass on nothing.** The kagi ledger refuses coverage over
  a scorecard with no round tables, and a cell audit where no cell cites a claim
  row — "the audit would be vacuous" (gates-survey-kagi.md:139-143).
- **An audit lane re-executes recipes, not prose.** Kaidoku r5 audits re-ran the
  recipes: 8/8 compare outputs byte-identical including a 63 MB request;
  `UNVERIFIABLE` means "cannot re-run or no evidence either way"
  (verification-patterns-fleet.md:28-35).
- **Claims precede the move, with their recipe.** Game briefs open with a
  declared falsifiable claim; kaidoku blocks pair `claim:` with `verify:` /
  `verified-at:` / `suggested: admit` (verification-patterns-fleet.md:24-26,
  69-74).
- **The verifier is a named non-author replaying committed/retained state** —
  committed hashes re-pinned before any run, instrumented runs under disjoint
  scratch (verification-patterns-fleet.md:28-30, 59-61).
- **Anything changed after verification carries its own proof:** post-verifier
  simplifier flags landed "byte-identical-proven, batteries re-run green"; a
  consolidation commit carried "own 163/163 re-verification"
  (verification-patterns-fleet.md:50-52).

## The mutation bar — nominal vs load-bearing

A suite is **nominal** while its green is a count; **load-bearing** only when a
disabled or attacked mechanism makes exactly the targeted cases fail.

- **Never quote a case count from source.** Counts are loop-sensitive (proxy 71
  literal sites → 102 cases; claims 35 → 39; kimi 41 → 43; kagi static sites
  6/1/0/1/6/2 vs measured 16/13/29/34/61/97). Name the executed summary line or
  the suite's own counter (gates-survey-kumitate.md:316-318;
  gates-survey-kagi.md:44-64).
- **Arm coverage is the floor, not the bar.** Five kumitate suites carry an
  "every declared kind fires" meta-check; (I) it proves each branch is *reached*,
  not that a wrong implementation would be *caught*
  (gates-survey-kumitate.md:283-286, 308-311).
- **The measured mutation controls, in strength order:** cite-check's mutation
  copy — copies the tree, rewrites `gate.rs:15`→`:11`, requires a
  `SYMBOL_OFF_LINE` hit — but it is integration-gated and does not run under
  `--selftest` (gates-survey-kumitate.md:51-58); scope-gate `--falsify`, a
  mutation mode that attacks the gate itself (gates-survey-kagi.md:490);
  claims-check's external env-poison probe (gates-survey-kumitate.md:218-222).
- **Adjudicate a mutation miss with a discriminator, never by retrofitting the
  record.** `--falsify` measured 16/18 here: exit matched, token did not; the
  same rule's scratch case passed inside 61/61 — so the rule is intact and this
  host's breadth counts collapsed (gates-survey-kagi.md:259-325).
- **Refusal paths need their own cases.** Three of six `policy_check` paths
  (`inline-shell`, `backslash`, `empty-quotes`) have no selftest case — precisely
  the bypass class round 11's adversary found; an edit deleting or reordering
  them would be caught by nothing (gates-survey-kagi.md:326-361).
- **A suite whose asserts are weaker than its contract carries a weaker bar than
  it prints.** Cite-check's hermetic asserts are substring-based; (I) the survey
  marks it weakest of the six on self-checking axes, compensated by
  repair-regression cases (gates-survey-kumitate.md:83-89, 312-315).
- **Unmeasured stays named.** Round-gate `INTERNAL_ERROR` has no hermetic case;
  integration groups were not executed; no mutant experiment yet tests the
  suites' own code against regressions (gates-survey-kumitate.md:144-156,
  320-331).

## Mutation-bar decision table — kill-rate bands (round 2, measured)

The corpus's first measured kill-rate: the 43-case hermetic suite of
`kumitate-shokunin/scripts/kimi-census.mjs` against 10 single-edit mutants →
**8/10 killed (80 %)**; control `43/43 pass`, the suite count held on every
mutant run, no inconclusive run (mutation-case-kimi-census.md:29-37). The case
sits on the 50-80/>80 boundary, so that boundary reading is the worked one; the
bands below carry the admission decision.

| Kill rate | What the suite is | Admission reading |
|---|---|---|
| **>80 %** | load-bearing: most plausible defects die, each on named cases | cite it as the surface's proof-of-catching; classes outside the injected vocabulary stay named (mutation-case-kimi-census.md:109-144) |
| **50-80 %** | partially load-bearing: survivors are measured, not assumed | cite it only with the survivors table attached; every survivor is a gap until a case pins it (mutation-case-kimi-census.md:44-53) |
| **<50 %** | nominal: green is a count, not a catch | never cite it as protection; the round admits anyway — the survivors table IS the finding (`plans/round-2.plan.md:8-9`; mutation-case-kimi-census.md:29-33) |

Rules:

- **Bands are a report convention, not a pass/fail gate.** An 8/10 admits, and so
  does a <50 % — with the gap recorded in the table, not softened
  (mutation-case-kimi-census.md:29-37, :185-191). (U: the corpus holds one
  kill-rate measurement; the 50 % crossover itself is unmeasured, and PROVINCE's
  ≥2-lane rule gates calling the method fleet-general, PROVINCE.md:16-17.)
- **Inject in a copy; one exact edit per fresh copy.** Every mutant is a copy
  under `/tmp/tameshi-r2-1-work/`; the driver asserts each old string occurs
  exactly once (`all unique`) before writing; no defect compounds with another;
  the original stays read-only (mutation-case-kimi-census.md:22-25, :148-166).
  Runs are `--selftest` or `--root` pointed under /tmp only — no live tree read
  (mutation-case-kimi-census.md:4-7).
- **Restore exact bytes, proven by hash.** Original sha256 before = after
  (`83016d45…4f426`), size and mtime unchanged, `git status --porcelain --
  <path>` empty (mutation-case-kimi-census.md:34-35). A sweep without this proof
  has no recorded substrate result.
- **Defect taxonomy — inject one per class, and read which class the suite can
  see:**
  - *off-by-one / table desync*: D1 `counted: 18 → 17` (kimi-census.mjs:105)
    killed on 16 cases; D2 `findings.slice(0, 6)` → `slice(0, 5)`
    (kimi-census.mjs:378) **survived** — the truncation boundary is never
    exercised (max findings in any suite run = 2 against a cap of 6) and the
    DRIFT asserts are prefix-only (kimi-census.mjs:498)
    (mutation-case-kimi-census.md:44-45, :82-92).
  - *inverted condition*: D3 `!e.children.includes(n)` → `includes(n)`
    (kimi-census.mjs:332) killed on 16 cases — a green fixture flips to
    all-UNLISTED, so the exact baseline catches it
    (mutation-case-kimi-census.md:46, :74-76).
  - *dropped arm*: D4, the root-stray reporting loop deleted
    (kimi-census.mjs:351-353), killed on exactly the three root-enum cases; D5,
    chain presence `gens.length > 0` → `true` (kimi-census.mjs:255), killed on
    one case (mutation-case-kimi-census.md:47-48, :61-65).
  - *wrong pin / unasserted constant*: D6, `server.token` floor `0o600` →
    `0o644` (kimi-census.mjs:124), killed on 2 cases; D10, `FROZEN.K2 25 → 24`
    (kimi-census.mjs:145) **survived** — only `frozen.K5` is asserted
    (kimi-census.mjs:526); the FAMILY/frozen lines are reported, never read
    (mutation-case-kimi-census.md:49, :53, :94-99).
  - the case's widened classes: D7 weakened floor predicate, D8 wrong
    fail-closed exit, D9 weakened secrecy kind pin — all killed on exactly
    their arm's cases (mutation-case-kimi-census.md:50-52, :66-73).
- **A survivor is a finding; a kill names its case set.** D2/D10 live on
  reported-but-unasserted surfaces — the assert vocabulary pins behavior, not
  reporting completeness (mutation-case-kimi-census.md:101-107); a kill quoted
  without its failing labels is unverified (mutation-case-kimi-census.md:59-76).
- **When mutation testing is not worth it.** (a) Defects already caught by the
  green baseline or an exact verdict-line assert need no mutant budget — D1/D3
  die on the same 16 cases (mutation-case-kimi-census.md:74-76); mutants pay
  where the asserts cannot look (D2/D10). (b) A suite that never runs in the
  path that matters yields no signal: cite-check's mutation control is
  integration-gated and never runs under `--selftest`
  (gates-survey-kumitate.md:51-58). (c) Mutation measures the suite, not the
  substrate — live-tree drift needs a live gate
  (mutation-case-kimi-census.md:206-207). (d) Single-edit mutants say nothing
  about coordinated rewrites or timing (mutation-case-kimi-census.md:195-199);
  the sweep is cheap here (7.0 s for 11 runs, :30) but that cost profile is
  host-local (U; mutation-case-kimi-census.md:204-205).

## No-permissiveness audit recipe

Goal: prove a change did not make anything pass by absence — no finding went
quiet, no arm stopped firing, no claim passed on a warning line. In order:

1. **Fix the revision under audit.** Line refs pin to a sha; a reader on a
   differing revision re-resolves. Stamps are recomputed (`ok=56 stale=0`),
   never re-typed (gates-survey-kagi.md:246-254, 420-438).
2. **Capture the before-set; compare against it.** Prior rows/ledgers are the
   regression fence — "prior rows 0-mismatch", "all 102 prior ledger rows +
   receipts byte-stable" (verification-patterns-fleet.md:37-39).
3. **Compare by byte-identity; scrub volatility only by an explicit list**
   (pids, timing, paths, ASLR, decimal wobble), and keep residual line drift in
   a named field (`provenance_only_line_diff`)
   (verification-patterns-fleet.md:32-35).
4. **Match verdicts fail-closed:** a claim passes only when the exit code equals
   the expected one AND the expected ERE matches the last non-empty output line;
   a verdict-shaped string followed by failure fails (`reason=verdict-not-final`)
   (gates-survey-kagi.md:161-168).
5. **Abstention is declared, counted, exit-neutral — and proven both ways.**
   `[substrate]` rows `DEFER … reason=substrate-absent`; the guard is the
   both-paths selftest; only-ABSENT/SKIP output may exit 0
   (gates-survey-kagi.md:187-197).
6. **Zero-work is a defect, not a green** (gates-survey-kagi.md:139-143).
7. **Falsifications and defects are findings, never softened;** the verifier
   catches what the author missed; post-verification changes carry their own
   proof (verification-patterns-fleet.md:46-57).
8. **Leave holes named as unknowns, not as green:** live verdicts unmeasured for
   five of six kagi gates; the kumitate integration group not executed
   (gates-survey-kagi.md:442-465; gates-survey-kumitate.md:320-331).

## Fail-closed arm taxonomy

Exit 2 is not one class. A red run means different things — read the arm:

| Arm | Fires when | Shape | Source |
|---|---|---|---|
| **SETUP** — cannot measure | input missing/unusable (`--src` gone, `op` absent, fixture dir not a dir) | exit 2, a named line before any effect (`ADJACENCY_SCOPE: SETUP (…)`), never a bare death | gates-survey-kagi.md:93-99 |
| **Malformed committed data** | a census row / declaration is malformed | census `die`s exit 2 ("not a verdict"); scope-gate accumulates `BAD-ROW` → `DEFECT` exit 1 — opposite calls, both deliberate | gates-survey-kagi.md:100-106 |
| **POLICY** — refused before the effect | the act would leak/overstep: non-regular or `op://`-carrying op-side paths; claim rows outside a 5-verb allowlist (quote-stripped before matching; 22 denied verbs); nested self-audit; stamp-set shrink without `--prune`; checklist rows naming `op.env`; hashing a no-hash path | exit 2, structural, before exec | gates-survey-kagi.md:107-138 |
| **Zero-work** | the gate would report over nothing | refused; a gate that measures nothing must not exit 0 | gates-survey-kagi.md:139-143 |
| **Deferral** | substrate absent for a `[substrate]`-tagged row | `DEFER … reason=substrate-absent`, counted, not executed, never FAIL; guards: tag lives in the data file, both-paths selftest | gates-survey-kagi.md:187-197 |

Rules:

- **Declare arms as tokens and prove coverage — or say it is unproven.** Proxy
  12/12 arms fired; claims 5/5; kimi-census 1 token, 3 cases; round-gate 7
  declared / 6 fired (`INTERNAL_ERROR` uncovered); surface-probe and cite-check
  have no token enum, so their exit-2 paths are uncovered until a case asserts
  them (gates-survey-kumitate.md:287-292).
- **Name the arm in the verdict:** `FAIL-CLOSED (TOKEN)`, never a free-form
  string; where no enum exists the suite can neither declare nor assert arm
  coverage (gates-survey-kumitate.md:106-118).
- **An arm that cannot fire on this host is an unknown, not a pass:**
  `BREADTH-EXCEEDS` never fires while live child counts sit far below their pins
  (gates-survey-kagi.md:279-291); whether the two zero-POLICY gates simply lack
  that surface is unrecorded (gates-survey-kagi.md:145-153).
- **Known gate-internal holes, carried not hidden:** cite-check's empty-scan
  exit-2 is asserted only as an in-process condition, not the CLI `return 2`
  mapping (gates-survey-kumitate.md:70-81).
