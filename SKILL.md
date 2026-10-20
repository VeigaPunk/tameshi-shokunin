---
name: tameshi-shokunin
description: Domain specialist — verification-fixture craft. Rank: shonen (probation).
---

# tameshi-shokunin

verification-fixture craft playbook. Rounds 1–3 built the corpus from measured
surfaces; every rule below earns a cited source. Two mutation cases are now
measured — round 2 JS, round 3 bash, both 8/10 killed — and this page carries
the method as an executable recipe: numbered steps from pin to restore proof,
defect templates with exact-string guidance, kill-rate bands, restore
discipline, the measured bash-vs-JS divergences, and complete reproduce specs
for both cases (Appendix A / Appendix B). Historical cold-read proof covers
one JS mutant only; current full-sweep/bash sufficiency remains unverified.

## Standing rules

- Read-only substrates unless PROVINCE.md declares a write surface;
  detection-and-report for operator-owned remediation.
- Secrets shape-only, never content-read.
- Every claim: measured anchor (path:line, command output, evidence id).
  Observation / inference / unknown stay separate.
- Errata append-only; rejections kept.
- **Scratch namespace is `/tmp/<lane>-r<round>-<n>-*/` from the first write**
  (both mutation lanes kept every mutant + evidence there —
  mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:4-6). The
  substrate tree is never a mutation target.

## Source notes

The sections below distil the corpus notes; every rule cites its note line.
The notes label each claim O (observation) / I (inference) / U (unknown);
inferences carried below keep the (I) mark.

- `corpus/knowledge/gates-survey-kumitate.md` — the six kumitate suites: exit
  maps, case counts, mutation controls, fail-closed arms, verdict asserts.
- `corpus/knowledge/gates-survey-kagi.md` — the six kagi gates: exit lattice,
  POLICY refusals, five evidence-discipline habits, findings F-1/F-2.
- `corpus/knowledge/verification-patterns-fleet.md` — the shared verifier shape
  (P1–P10, ≥2 independent lanes) vs two lane-specific encodings.
- `corpus/knowledge/mutation-case-kimi-census.md` (round 2) — the JS worked
  case: `kimi-census.mjs` 43-case suite vs 10 single-edit mutants → 8/10 killed
  (80 %); survivors D2/D10; full protect/gap inventory, driver spec, unknowns.
- `corpus/knowledge/mutation-case-kagi-census.md` (round 3) — the bash worked
  case: `surface-census.sh` 16-case selftest vs 10 single-edit mutants → 8/10
  killed (80 %); survivors B5 (fixture-absent arm) / B10 (unread count);
  kill-width and survivor-class comparison in §4, driver spec in §7.
- `plans/round-3.plan.md` — the round-3 axis move (depth + operability) and its
  pre-registered anti-claim: a wild divergence between the JS and bash
  kill-rates IS the finding (language-class differences in what suites protect).

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

## Mutation-sweep recipe — numbered steps; bounded cold-read evidence

Runs a suite's own code through one-exact-edit mutants and measures what it
catches. The recipe is intended to be self-contained; observed cold-read proof
covers one historical JS mutant, not full sweeps, survivor probes or bash.
Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).

1. **Pick the target and prove its control.** The suite must run hermetically
   (`--selftest`) or on `--root` pointed under `/tmp` — no live path read
   (mutation-case-kimi-census.md:4-7; the bash selftest rebuilds every fixture
   under `mktemp -d` — mutation-case-kagi-census.md:24-26) — and it must print
   its own executed case count and a verdict as its closing lines: kumitate
   shape `n/m pass` + `VERDICT:` (gates-survey-kumitate.md:19-31), kagi bash
   shape per-case lines + `SELFTEST: PASS (n cases)`
   (mutation-case-kagi-census.md:33-35). Run the control on the pinned bytes and
   require green: `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0
   (mutation-case-kimi-census.md:20-21) or `SELFTEST: PASS (16 cases)`, exit 0
   (mutation-case-kagi-census.md:42-43). A red control has no denominator —
   stop and record it as setup failure.
2. **Pin the artifact — committed bytes only.** Record: path, full sha256,
   size, line count, mtime, repo revision, and `git status --porcelain --
   <path>` empty (mutation-case-kimi-census.md:13-16;
   mutation-case-kagi-census.md:13-17 — note that gate's 887th line carries no
   trailing newline). A pin on uncommitted bytes is a false anchor — the kagi
   claim-ledger pin was once surveyed from a dirty intermediate state and had to
   be re-pinned (corpus/README.md G-R2-1 row; gates-survey-kagi.md errata
   block). If the path is dirty: stop.
3. **Copy pristine to scratch.** `mkdir -p /tmp/<lane>-r<round>-<n>-work/evidence`
   then `cp -p <artifact> …/pristine.<ext>`; re-verify (`sha256sum`; the bash
   lane additionally `cmp`-verified its copy — mutation-case-kagi-census.md:44-45).
   All edits happen to copies; the original is never a write target.
4. **Write the defect list from the templates.** 8–12 defects, one per class
   (catalog + entry template in the next section), each ONE exact-string
   replacement or single block deletion, each with a pre-registered
   `expect: killed|survived` and the reason — the JS 10-defect manifest is the
   shape (mutation-case-kimi-census.md:41-53, :155-166). Pre-registration is
   what makes an expectation miss a calibration datum instead of a
   rationalization (E1: the author's D7 expectation was wrong and is kept —
   mutation-case-kimi-census.md:183-191; round 3's E1 kept miscalled case
   counts — mutation-case-kagi-census.md:184-191).
5. **Driver `--check` — the fail-closed uniqueness gate.** For every defect:
   assert `count(old) == 1` in the pristine copy, print the count and first
   matching line, and require the literal line `all unique` — both lanes'
   drivers did exactly this (mutation-case-kimi-census.md:22-25;
   mutation-case-kagi-census.md:44-47). Also assert `new != old`: a no-op edit
   is a driver bug, not a survivor (the round-2 driver asserts
   `replacement was a no-op`). Any count ≠ 1 aborts the sweep until the string
   is re-derived from the pinned bytes.
6. **Run control + mutants.** Control first: run the unmutated copy, record
   stdout, exit code, summary line, duration — expect the step-1 green. Then per
   defect, one at a time: fresh copy from pristine → apply the one exact
   replacement (`str.replace(old, new, 1)`) → assert mutant sha256 ≠ pristine
   sha256 → run the suite with a timeout (300 s used in round 2, 280 s in round
   3) → write full combined output to `evidence/<id>.selftest.txt` and exit code
   + mutant sha256 + duration + summary to `evidence/<id>.meta.json`; aggregate
   rows to `evidence/results.json` (mutation-case-kimi-census.md:26-28;
   mutation-case-kagi-census.md:48-49). No defect compounds with another; a
   mutant file is never patched or reused.
7. **Adjudicate each run against the suite's own verdict.** Green = exit 0 AND
   the verdict line says PASS with the full count.
   - **Killed** = the run went red (exit ≠ 0 or the PASS verdict/line broken)
     *and* the suite still enumerated its full case count — held on every run in
     both sweeps (`(<n>/43`, `(<n>/16 cases)`;
     mutation-case-kimi-census.md:30-33; mutation-case-kagi-census.md:50-53).
     Collect the failing-case labels verbatim; a kill quoted without its failing
     labels is unverified (mutation-case-kimi-census.md:59-76). Bash grammar:
     `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0`
     and summary `SELFTEST: FAIL (1/16 cases)`
     (mutation-case-kagi-census.md:82-103).
   - **A kill can be token-only, not exit-only.** B4's deleted symlink arm kept
     the exit code (the row fell into the regular-file arm, `got exit=1` like
     the expected one) and died on the token assert alone
     (mutation-case-kagi-census.md:88-91). Adjudicate exit AND token/verdict;
     never exit alone.
   - **Survived** = green with the same count as control → a finding, never a
     footnote; it names a gap until a case pins it
     (mutation-case-kimi-census.md:44-53).
   - **Inconclusive** = no definitive verdict (timeout, crash before the
     summary, count not enumerated). Not a kill. Re-run it; keep every record.
   - **Kill rate = killed / (killed + survived)** — inconclusive runs are
     excluded from the denominator and named beside it. Round 2: 8/10 = 80 %,
     no inconclusive run, 11 runs in 7.0 s (mutation-case-kimi-census.md:29-31).
     Round 3: 8/10 = 80 %, 11 runs in 11.0 s (mutation-case-kagi-census.md:50-53).
8. **Probe every survivor for non-equivalence.** Run the mutant on an input
   outside the suite's fixtures that exercises the mutated surface; its output
   must differ from pristine. JS D2 on an empty root: one fewer id and
   `+23 more` (vs pristine `+22 more`); D10: `frozen=24` (vs 25)
   (mutation-case-kimi-census.md:82-99). Bash B5: mutant `SURFACE OK … (exec
   644)` exit 0 where pristine prints `SURFACE DIVERGED … no execute bit` exit
   1; B10: `ok=0` where pristine prints `ok=1`
   (mutation-case-kagi-census.md:111-114, :118-122, :251-253). If no observable
   input differs, the mutant may be *equivalent code* — record that as a
   calibration item, not as a gap.
9. **Restore + prove the substrate never moved.** Re-run step 2's checks:
   sha256 after == before, size and mtime unchanged, `git status --porcelain --
   <path>` empty (mutation-case-kimi-census.md:34-35;
   mutation-case-kagi-census.md:54-56). The sweep's edits all lived in scratch,
   so this proves the *absence* of writes; it is the record's headline, not an
   appendix. Full checklist below (Restore discipline).
10. **Record the sweep as a note + a corpus row.** Kill-rate table (control +
    one row per defect: class, exact edit + site, exit, suite line, verdict,
    failing-case labels), by-class tally, protected/not-protected inventory,
    survivor probes, reproduce spec (driver manifest + commands), calibration
    and errata, unknowns — the two mutation-case notes are the model
    (mutation-case-kimi-census.md §1, §3-§6;
    mutation-case-kagi-census.md §1-§7). Counts quoted only from executed
    summary lines (mutation bar above); refs pinned to the record's revision,
    re-resolved if the substrate moved.

Cost profile to record with every sweep: wall time, per-run timeout, host +
runtime versions — round 2: 7.0 s for 11 runs on node v24.21.0; round 3:
11.0 s for 11 runs (~1.0 s each) against a 280 s per-run bound
(mutation-case-kimi-census.md:204-205; mutation-case-kagi-census.md:50-53).
Stability across hosts stays unknown in both (U5 each).

## Defect-taxonomy templates and exact-string guidance

The classes are the injection vocabulary; read which class the suite can see.
One defect per class per sweep, and widen beyond the measured set when the
artifact offers a new mechanism.

**Entry template (one per defect, written before any run):**

```
id:      D<n>/B<n>
class:   <class name from the catalog>
site:    <artifact path>:<line(s)> at pinned rev <short-sha>
old:     <exact bytes, copied from the pinned artifact — indentation significant>
new:     <exact bytes; EMPTY = delete the old block entirely>
why:     <the plausible defect a real regression would introduce here>
expect:  killed|survived — because <which cases should see it and how>
```

**Exact-string rules (each learned from a measured edit):**

1. **Copy `old` from the pinned artifact, never from a note or memory.** The
   uniqueness gate (recipe step 5) is the arbiter: `count(old) == 1`, literal
   `all unique` required. Re-derive on any substrate movement.
2. **Include the full line when indentation disambiguates.** Round 2 D3 is
   `      if (!e.children.includes(n)) {` with six leading spaces in the driver
   — a two-space substring also occurs once, but produces a *different mutant*
   and different bytes. Exact means exact.
3. **One behavior per edit; minimal edit wins.** A defect that changes two
   mechanisms cannot be read for which class the suite saw
   (mutation-case-kimi-census.md:22-25).
4. **Literal replacement, never regex.** Use `str.replace(old, new, 1)` (both
   drivers). Code carries regex metacharacters — `(mode & m.modeFloor)`,
   `${n}`, `slice(0, 6)`, `[[ "$got" -ge "$floor" ]]` all appear in the two
   manifests (mutation-case-kimi-census.md:156-166;
   mutation-case-kagi-census.md:218-236); a regex substitution silently
   mis-scopes on them. If a line editor must be used, escape metacharacters or
   prefer literal-mode tools.
5. **Byte-level exactness:** preserve quoting, spacing, and the trailing
   newline (D8's old is `  return 2;\n` — the newline is part of the edit); a
   file whose last line has no newline stays that way (the bash gate's 887th
   line — mutation-case-kagi-census.md:14-15). Assert mutant sha256 ≠ pristine
   sha256 so a no-op cannot masquerade as a survivor.
6. **Never compound, never patch after a run;** a new idea means a new defect,
   a fresh copy, a new run id.

**Class catalog (worked rows are the calibration):**

| Class | Edit shape | What kills it | JS evidence (round 2) | Bash evidence (round 3) |
|---|---|---|---|---|
| off-by-one count / table desync | a literal count ±1 | exact-count asserts + the green baseline | D1 → 16 cases (mutation-case-kimi-census.md:44) | B7 `+1`→`+2` → 1 case (`unverified=3`) (mutation-case-kagi-census.md:73) |
| boundary / truncation cap | slice/limit ∓1 | only a case exercising the boundary | D2 **survived** — boundary never reached (max 2 vs cap 6) (mutation-case-kimi-census.md:45, :82-92) | B2 `-ge`→`-gt`, B6 `len+1`→`len` → 2 cases each (the two exit-0 green fixtures) (mutation-case-kagi-census.md:68, :72, :95-97) |
| inverted condition | negate a predicate | the green fixture itself flips | D3 → 16 (mutation-case-kimi-census.md:46) | B3 `!=`→`==` → 3 (the two green fixtures + case 06 crosscheck-disagree) (mutation-case-kagi-census.md:69) |
| dropped arm | delete the arm's reporting/effect lines | exactly that arm's cases — if any exist | D4 → 3 root-enum cases; D5 → 1 (mutation-case-kimi-census.md:47-48) | B4 → 1, **token-only kill**; B5 **survived** — no case reaches the arm (mutation-case-kagi-census.md:70-71, :88-91) |
| weakened presence gate | force a presence bool to `true` | the single no-chain tripwire | D5 → 1 (mutation-case-kimi-census.md:48) | (not injected; see B1 guard inversion → 1) |
| guard inversion | `-eq 0` ↔ `-ne 0` | the one case with a stray child | — | B1 → 1 (case 05 undeclared-file) (mutation-case-kagi-census.md:67, :84-87) |
| wrong constant pin | change a pinned literal (mode floor) | cases asserting the pinned value | D6 → 2 (mutation-case-kimi-census.md:49) | (mode drift covered by fixtures; not re-injected) |
| weakened predicate semantics | change the comparison operator | fixtures whose bits discriminate | D7 → 2 (mutation-case-kimi-census.md:50) | (see B2/B3) |
| inverted class select | swap the classes two arms select | both classes' cases | — | B9 → 2 (cases 03/04) (mutation-case-kagi-census.md:75, :102-103) |
| wrong exit-code mapping | change a fail-closed return | the fail-closed cases | D8 → 3 (mutation-case-kimi-census.md:51) | B8 `die` 2→1 → 2 (cases 13/14) (mutation-case-kagi-census.md:74, :100-101) |
| weakened type/kind pin | broaden a kind check | anti-read fixtures | D9 → 2 (mutation-case-kimi-census.md:52) | (symlink arm deletion B4 covers the kind branch) |
| reported constant (display-only) | change a constant only reported | only a case that reads it | D10 **survived** (only `frozen.K5` asserted) (mutation-case-kimi-census.md:53, :94-99) | B10 **survived** (`ok=` unasserted) (mutation-case-kagi-census.md:76, :118-122) |

Shared survivor classes across the two cases, named: **reported-but-unasserted
data** (D2/D10, B10) and the bash-only **unreached/fixture-absent arm** (B5) —
one on the report side, one on the fixture side; both are "the suite cannot
see a real difference" (mutation-case-kimi-census.md:101-107;
mutation-case-kagi-census.md:105-126).

## Kill-rate bands — admission readings (rounds 2–3, measured)

The corpus's first measured kill-rate: the 43-case hermetic suite of
`kumitate-shokunin/scripts/kimi-census.mjs` against 10 single-edit mutants →
**8/10 killed (80 %)**; control `43/43 pass`, the suite count held on every
mutant run, no inconclusive run (mutation-case-kimi-census.md:29-37). Round 3's
second measurement: the 16-case selftest of
`kagi-shokunin/corpus/surface-census.sh` against 10 single-edit mutants →
**8/10 killed (80 %)**; control `SELFTEST: PASS (16 cases)`, count held, no
inconclusive run, 11.0 s for 11 runs (mutation-case-kagi-census.md:42-60).
Both points sit on the 50-80/>80 boundary, so that boundary reading is the
worked one; the bands below carry the admission decision.

| Kill rate | What the suite is | Admission reading |
|---|---|---|
| **>80 %** | load-bearing: most plausible defects die, each on named cases | cite it as the surface's proof-of-catching; classes outside the injected vocabulary stay named (mutation-case-kimi-census.md:109-144) |
| **50-80 %** | partially load-bearing: survivors are measured, not assumed | cite it only with the survivors table attached; every survivor is a gap until a case pins it (mutation-case-kimi-census.md:44-53) |
| **<50 %** | nominal: green is a count, not a catch | never cite it as protection; the round admits anyway — the survivors table IS the finding (`plans/round-2.plan.md:8-9`; mutation-case-kimi-census.md:29-33) |

Rules:

- **Bands are a report convention, not a pass/fail gate.** An 8/10 admits, and so
  does a <50 % — with the gap recorded in the table, not softened
  (mutation-case-kimi-census.md:29-37, :185-191). (U: the 50 % crossover itself
  is unmeasured — both measurements landed at 80 %, so the band interiors are
  still unprobed; the divergence section carries the (I) reading on PROVINCE's
  ≥2-lane bar, PROVINCE.md:16-17.)
- **Inject in a copy; one exact edit per fresh copy.** Every mutant is a copy
  under `/tmp/<lane>-r<round>-<n>-work/`; the driver asserts each old string
  occurs exactly once (`all unique`) before writing; no defect compounds with
  another; the original stays read-only (mutation-case-kimi-census.md:22-25,
  :148-166; mutation-case-kagi-census.md:44-47). Runs are `--selftest` or
  `--root` pointed under /tmp only — no live tree read
  (mutation-case-kimi-census.md:4-7).
- **Restore exact bytes, proven by hash.** Original sha256 before = after
  (`83016d45…4f426` JS; `275d8294…53009f` bash), size and mtime unchanged,
  `git status --porcelain -- <path>` empty (mutation-case-kimi-census.md:34-35;
  mutation-case-kagi-census.md:54-56). A sweep without this proof has no
  recorded substrate result.
- **A survivor is a finding; a kill names its case set.** D2/D10/B10 live on
  reported-but-unasserted surfaces; B5 on an unreached arm — the assert
  vocabulary and the fixture set pin behavior, not completeness
  (mutation-case-kimi-census.md:101-107; mutation-case-kagi-census.md:105-126);
  a kill quoted without its failing labels is unverified
  (mutation-case-kimi-census.md:59-76).
- **When mutation testing is not worth it.** (a) Defects already caught by the
  green baseline or an exact verdict-line assert need no mutant budget — D1/D3
  die on the same 16 cases (mutation-case-kimi-census.md:74-76); mutants pay
  where the asserts cannot look (D2/D10/B5/B10). (b) A suite that never runs in
  the path that matters yields no signal: cite-check's mutation control is
  integration-gated and never runs under `--selftest`
  (gates-survey-kumitate.md:51-58). (c) Mutation measures the suite, not the
  substrate — live-tree drift needs a live gate
  (mutation-case-kimi-census.md:206-207). (d) Single-edit mutants say nothing
  about coordinated rewrites or timing (mutation-case-kimi-census.md:195-199;
  mutation-case-kagi-census.md:195-196); host-gated paths stay unmutated by
  design (the bash verbs cases skip on this host —
  mutation-case-kagi-census.md:27-38, :197-200). The sweeps are seconds-scale
  (7.0 s / 11.0 s for 11 runs) but that cost profile is host-local (U;
  mutation-case-kimi-census.md:204-205; mutation-case-kagi-census.md:203-204).

## Restore discipline — proof the substrate never moved

The mutation sweep's strongest claim is the negative one: the substrate was
never written. Prove it in this order:

1. **Before the sweep:** sha256 (full), size, mtime, repo revision, and
   `git status --porcelain -- <path>` empty — recorded in the note's header
   (mutation-case-kimi-census.md:13-16; mutation-case-kagi-census.md:13-17).
2. **All edits in scratch:** `cp -p` the artifact into the lane namespace and
   edit only copies (mutation-case-kimi-census.md:4-7;
   mutation-case-kagi-census.md:44-45).
3. **After the sweep:** re-run the same checks; every value identical. Round-2
   proof: `83016d45…4f426` before and after, 43273 B, mtime unchanged, kumitate
   tree clean for the path (mutation-case-kimi-census.md:34-35). Round-3 proof:
   `275d8294…53009f` before and after, 44212 B, mtime 09:47:15 unchanged, kagi
   tree clean, and the scratch copy still `cmp`-identical to the original
   (mutation-case-kagi-census.md:54-56).
4. **A drift is an incident:** stop, report it as one, do not "repair" by
   rewriting — a repair would itself be an unauthorized write.
5. **Never restore via `git checkout`/`git restore`.** Those write to the
   substrate; the only correct end state is *never-modified*. (I)
6. **Retain the scratch as evidence.** Both lanes' probes re-ran from
   `/tmp/tameshi-r2-1-work/` and `/tmp/tameshi-r3-1-work/`; each note's
   reproduce spec rebuilds the sweep even if /tmp is wiped
   (mutation-case-kimi-census.md §4; mutation-case-kagi-census.md §7;
   SCORECARD round-2 verification row).
7. **If the artifact was already dirty at pin time:** that pin is not a clean
   baseline — record the dirty state exactly, or better, stop and re-pin a
   committed revision (the G-R2-1 lesson, corpus/README.md round-2 addendum).

## Cross-language divergence — bash vs JS (round 3, measured)

Round 3 repeated the sweep on a second gate of a different language class:
kagi's `surface-census.sh` (886-line bash gate, 16-case selftest) next to round
2's kumitate `kimi-census.mjs` (896-line node gate, 43-case selftest). The
round pre-registered the anti-claim: a wild kill-rate divergence IS the finding
— language-class differences in what suites protect (`plans/round-3.plan.md:8-9`).
Measured: **the headline rate did not diverge** — both sweeps kill 8/10 (80 %),
both held the suite count on every mutant run, neither produced an inconclusive
run (mutation-case-kagi-census.md:162-170; mutation-case-kimi-census.md:29-37).
The language-class differences sit elsewhere (mutation-case-kagi-census.md:164-166).

| Axis | JS case (round 2) | Bash case (round 3) |
|---|---|---|
| artifact / lane | `kimi-census.mjs` / kumitate | `surface-census.sh` / kagi |
| language class | node (ESM) | bash |
| suite grammar | `n/43 pass` + `FAIL <label>` lines | `ok-case`/`bad-case`/`skip-case` lines + `SELFTEST: PASS/FAIL (n/16 cases)` |
| abstention | none in the recorded runs | 2/16 `skip-case … substrate-absent (handler not on PATH)` — inside the count |
| kill rate | 8/10 = 80 % | 8/10 = 80 % |
| kill width | up to 16/43 (D1/D3, incl. the green baseline) | widest 3/16 (B3); labels near-singletons |
| survivors | D2 truncation tail, D10 frozen constant — reported-but-unasserted | B10 `ok=` summary arg (same family) + B5 exec-x-bit arm — an arm no fixture reaches |
| calibration | 9/10 pre-run verdict expectations (E1 D7 miss) | 10/10 verdicts, 6/10 failing-case *counts* (E1: B2/B3/B6 each gained the second green fixture) |
| cost | 11 runs, 7.0 s | 11 runs, 11.0 s (control 1.0 s) |
| restore pin | `83016d45…` before = after | `275d8294…` before = after |

Rules (each backed by the two cases):

- **Read the case grammar before the summary.** A JS kill names failing labels
  and a collapsed pass count (`27/43 pass`); a bash kill names numbered cases
  with the expected exit+token and the summary counts bad cases
  (`SELFTEST: FAIL (1/16 cases)`) (mutation-case-kagi-census.md:82-103). Both
  are "red with the count held" — never compare the two summaries numerically.
- **Abstention is structural in the bash selftest.** 2/16 cases print
  `skip-case … substrate-absent` and still sit inside `PASS (16 cases)`; the
  hermetic case set is 14 + 2 substrate-gated that performed no execution. Quote
  the case lines with the summary or the count overstates coverage
  (mutation-case-kagi-census.md:27-35). The JS hermetic runs abstained from
  nothing (in the recorded runs).
- **A kill can be token-only.** B4's exit code still matched the expectation;
  only the token assert caught the deletion (mutation-case-kagi-census.md:88-91).
  Adjudicate exit AND token/verdict.
- **Kill width is structural, not quality.** (I) The bash suite rebuilds a fresh
  fixture per case and asserts `exit + one token` per run, so labels are
  near-singletons; the JS suite shares in-memory fixtures and asserts exact
  verdict lines, so one wrong predicate colours many cases
  (mutation-case-kagi-census.md:171-175).
- **Survivors sub-classify: unasserted data vs unreached arm.** JS's two
  survivors are values the asserts never read; bash keeps that class (B10) and
  adds the unreached-arm class (B5) — repair differs: assert the value vs add
  the case. B5's shape matches the F-2 bypass-class hole pattern — refusal
  paths without cases (mutation-case-kagi-census.md:176-180;
  gates-survey-kagi.md:326-361).
- **Exact strings are the sharpest tools in both grammars:** JS
  `'19 children, 18 declared'` and the exact CLEAN line; bash `unverified=3`
  (B7's tripwire) (mutation-case-kagi-census.md:181-182).
- **Anti-claim verdict:** no wild divergence; (O) same headline, different gap
  shapes. (I) two independent lanes measured → the method's two-lane generality
  bar is met for the measured shapes (PROVINCE.md:16-17); band interiors,
  verb-path mutants (U2) and host stability (U5) stay unknown
  (mutation-case-kagi-census.md:193-206).

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

## Appendix A — worked example: JS case (reproduce from this page alone)

Replicates TAMESHI-R2-1 (`mutation-case-kimi-census.md`); expected outcome:
**8/10 killed**, survivors D2/D10, control `43/43`, restore pin held. Runs in
seconds. Substrate read-only.

**Artifact pin** (verify before copying): `kumitate-shokunin/scripts/kimi-census.mjs`
— sha256 `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`,
896 lines, 43273 B; kumitate rev `175de6ba`; `git -C kumitate-shokunin status
--porcelain -- scripts/kimi-census.mjs` empty (mutation-case-kimi-census.md:13-16).
A differing sha means the substrate moved: re-derive the manifest below by
line content (the uniqueness gate will catch drift), or re-anchor to the note.

**Commands (order matters):**

```bash
W=/tmp/<lane>-r<round>-<n>-work
mkdir -p "$W/evidence" "$W/empty-root"
cp -p kumitate-shokunin/scripts/kimi-census.mjs "$W/pristine.mjs"
sha256sum "$W/pristine.mjs"        # must print 83016d45…4f426
node "$W/pristine.mjs" --selftest  # control: KIMI_CENSUS_SELFTEST: 43/43 pass
                                   #          VERDICT: PASS, exit 0
# write driver + manifest (below), then:
python3 "$W/mutate_driver.py" --check   # per-defect occurrences + 'all unique'
python3 "$W/mutate_driver.py" --run     # control + 10 mutants, writes evidence/
# survivor probes (must show the mutant observably different off-suite):
node "$W/mutant-D2.mjs"  --root "$W/empty-root" | tail -1   # …5 ids, '+23 more' (node exits 1)
node "$W/mutant-D10.mjs" --root "$W/empty-root" | grep 'FAMILY K2'  # frozen=24
```

**Driver contract (write from this spec):** load pristine text; `--check`:
`count(old)==1` per defect, print occurrences + first line, final line
`CHECK: all unique`, else exit 1; `--run`: for each defect assert uniqueness and
`new != old`, write `mutant-<id>.mjs` from a fresh replacement, run
`node mutant-<id>.mjs --selftest` (timeout 300 s), save stdout →
`evidence/<id>.selftest.txt`, and `{sha256, exit, duration, summary, verdict,
fails}` → `evidence/<id>.meta.json`; control first (`D00-control`); aggregate
`evidence/results.json`. Killed ⇔ exit ≠ 0 or `VERDICT: PASS` absent, with the
full count still enumerated.

**Manifest (exact strings; the en-dash in D4 is U+2013; `\n` shown as escapes
must be real newlines in the driver):**

```python
MANIFEST = [
  ("D1", "kimi-census.mjs:105", "kind: 'dir', counted: 18 },", "kind: 'dir', counted: 17 },"),
  ("D2", "kimi-census.mjs:378", "findings.slice(0, 6).map", "findings.slice(0, 5).map"),
  ("D3", "kimi-census.mjs:332", "      if (!e.children.includes(n)) {", "      if (e.children.includes(n)) {"),
  ("D4", "kimi-census.mjs:351-353", "  for (const n of strays) {\n    err('UNLISTED', n, `${n} sits at the root and is not declared by the frozen K1–K5 set`);\n  }\n", ""),
  ("D5", "kimi-census.mjs:255", "      const present = gens.length > 0;", "      const present = true;"),
  ("D6", "kimi-census.mjs:124", "kind: 'file', secret: true, modeFloor: 0o600 },", "kind: 'file', secret: true, modeFloor: 0o644 },"),
  ("D7", "kimi-census.mjs:306", "(mode & m.modeFloor) !== m.modeFloor", "(mode & m.modeFloor) === 0"),
  ("D8", "kimi-census.mjs:396", "  return 2;\n", "  return 1;\n"),
  ("D9", "kimi-census.mjs:292", "        ? (m.kind === 'dir' ? kind === 'dir' : isLeaf(kind))", "        ? (m.kind === 'dir' ? kind === 'dir' : kind === 'file')"),
  ("D10", "kimi-census.mjs:145", "const FROZEN = { K1: 3, K2: 25, K3: 9, K4: 9, K5: 3 };", "const FROZEN = { K1: 3, K2: 24, K3: 9, K4: 9, K5: 3 };"),
]
```

**Expected results (round-2 measured):** control 43/43 PASS; D1 27/43 FAIL
(16 cases); D2 **43/43 PASS — survivor**; D3 27/43 FAIL (16); D4 40/43 FAIL (3);
D5 42/43 FAIL (1); D6 41/43 FAIL (2); D7 41/43 FAIL (2); D8 40/43 FAIL (3);
D9 41/43 FAIL (2); D10 **43/43 PASS — survivor**; 8/10 = 80 %; 7.0 s sweep
(mutation-case-kimi-census.md:41-53). After: `sha256sum pristine.mjs` still
`83016d45…4f426`; size/mtime unchanged; kumitate `git status` clean for the
path (mutation-case-kimi-census.md:34-35). Any deviation from these numbers is
a finding about the host/suite, not a failure to hide.

## Appendix B — worked example: bash case (reproduce from this page alone)

Replicates TAMESHI-R3-1 (`mutation-case-kagi-census.md`); expected outcome:
**8/10 killed (80 %)**, survivors B5/B10, control `SELFTEST: PASS (16 cases)`,
restore pin held. Substrate read-only; all mutants under
`/tmp/<lane>-r<round>-<n>-work/`.

**Artifact pin** (verify before copying): `kagi-shokunin/corpus/surface-census.sh`
— sha256 `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`,
44212 B, 886 newlines (the 887th line carries no trailing newline), mode 755;
kagi rev `fecee87` (`fecee8743e52eb8fb5fbb40782934cb619a1a96e`); `git -C
kagi-shokunin status --porcelain -- corpus/surface-census.sh` empty
(mutation-case-kagi-census.md:13-17).

**Commands (order matters):**

```bash
W=/tmp/<lane>-r<round>-<n>-work
mkdir -p "$W/evidence"
cp -p kagi-shokunin/corpus/surface-census.sh "$W/pristine.sh"
sha256sum "$W/pristine.sh"        # must print 275d8294…53009f
bash "$W/pristine.sh" --selftest  # control: SELFTEST: PASS (16 cases), rc=0
                                  # (ok-case 01..14 + skip-case 15/16,
                                  #  both substrate-absent on this host)
# write driver + SPECS (below), then:
python3 "$W/mutate_driver.py" --check   # per-defect occurrences + 'all unique'
python3 "$W/mutate_driver.py" --run     # control + B1..B10, writes evidence/
# survivor probes (note §7 commands; run from the work dir):
bash "$W/mutant-B5.sh"  verify --root "$W/probe/host"  --census "$W/probe/census.tsv"  --shapes "$W/probe/shapes.tsv"  --baseline "$W/probe/baseline.tsv"
bash "$W/mutant-B10.sh" verify --root "$W/probe2/host" --census "$W/probe2/census.tsv" --shapes "$W/probe2/shapes.tsv" --baseline "$W/probe2/baseline.tsv"
```

**Driver contract:** same as Appendix A except the run command is
`bash mutant-Bx.sh --selftest` (cwd = the work dir) and the recorded summary
lines are the `ok-case`/`bad-case`/`skip-case`/`SELFTEST:` lines; predictions
compared at the end; evidence files `evidence/B<n>.selftest.txt` +
`.meta.json`; manifest below is the driver's exact literal form
(mutation-case-kagi-census.md:208-236, :240-249).

**Manifest (exact strings; Python literals as used by the round-3 driver —
`\n` are real newlines, `\"` real quotes, `\\n` a literal backslash-n inside a
printf format):**

```python
SPECS = [
  ("B1", "surface-census.sh:241", '  [[ ${#SCAN_DIR[@]} -eq 0 ]] && return 0', '  [[ ${#SCAN_DIR[@]} -ne 0 ]] && return 0'),
  ("B2", "surface-census.sh:435", '            elif [[ "$got" -ge "$floor" ]]; then printf \'SHAPE OK       %s rows %s %s >= %s\\n\' "$p" "$tbl" "$got" "$floor"', '            elif [[ "$got" -gt "$floor" ]]; then printf \'SHAPE OK       %s rows %s %s >= %s\\n\' "$p" "$tbl" "$got" "$floor"'),
  ("B3", "surface-census.sh:229", '      if [[ -n "$want_mode" && "$want_mode" != "$mode" ]]; then', '      if [[ -n "$want_mode" && "$want_mode" == "$mode" ]]; then'),
  ("B4", "surface-census.sh:200-204", "    if [[ \"$live\" == \"symlink\" ]]; then\n      printf 'SURFACE LINK     %s (declared %s)\\n' \"$p\" \"$kind\"\n      N_LINK=$((N_LINK + 1)); FAILED=1\n      continue\n    fi\n", ""),
  ("B5", "surface-census.sh:214-217", "           if [[ \"$kind\" == \"exec\" && ! -x \"$abs\" ]]; then\n             printf 'SURFACE DIVERGED %s (declared exec, no execute bit)\\n' \"$p\"\n             N_DIVERGED=$((N_DIVERGED + 1)); FAILED=1; continue\n           fi ;;\n", "           ;;\n"),
  ("B6", "surface-census.sh:371", '        if head -c "$(( ${#value} + 1 ))" "$abs" | cmp -s - "$MAGIC_EXPECT"; then', '        if head -c "${#value}" "$abs" | cmp -s - "$MAGIC_EXPECT"; then'),
  ("B7", "surface-census.sh:405-406", "            printf 'SHAPE UNVERIFIED %s %s (%s)\\n' \"$p\" \"$assertion\" \"${S_ERR_A[$p]}\"\n            N_UNVERIFIED=$((N_UNVERIFIED + 1)); FAILED=1", "            printf 'SHAPE UNVERIFIED %s %s (%s)\\n' \"$p\" \"$assertion\" \"${S_ERR_A[$p]}\"\n            N_UNVERIFIED=$((N_UNVERIFIED + 2)); FAILED=1"),
  ("B8", "surface-census.sh:85", "die() { printf 'surface-census: %s\\n' \"$1\" >&2; exit 2; }", "die() { printf 'surface-census: %s\\n' \"$1\" >&2; exit 1; }"),
  ("B9", "surface-census.sh:191", '      if [[ "$cls" == "runtime" ]]; then', '      if [[ "$cls" == "asset" ]]; then'),
  ("B10", "surface-census.sh:862", '        "${#SCAN_DIR[@]}" "$N_OK" "$N_ABSENT" "$N_SKIP"', '        "${#SCAN_DIR[@]}" "$N_ABSENT" "$N_ABSENT" "$N_SKIP"'),
]
```

**Expected results (round-3 measured):** control PASS (16 cases), rc=0; B1
FAIL 1/16 — bad-case 05 undeclared-file; B2 FAIL 2/16 — cases 01 clean, 04
runtime-absent; B3 FAIL 3/16 — 01, 04, 06 crosscheck-disagree; B4 FAIL 1/16 —
07 symlink-swap (token-only kill); B5 **PASS (16 cases) — survivor** (no
selftest case reaches the deleted exec x-bit arm); B6 FAIL 2/16 — 01, 04;
B7 FAIL 1/16 — 10 sqlite-unavailable (`unverified=3` tripwire); B8 FAIL 2/16 —
13 malformed-row, 14 fused-shape-row; B9 FAIL 2/16 — 03 asset-gone, 04
runtime-absent; B10 **PASS (16 cases) — survivor** (`ok=` summary arg
unasserted); 8/10 = 80 %; 11.0 s sweep (mutation-case-kagi-census.md:62-80,
:50-53). Non-equivalence probes: B5 prints `SURFACE OK … (exec 644)` rc=0 where
pristine prints `SURFACE DIVERGED … (declared exec, no execute bit)` rc=1; B10
prints `ok=0` where pristine prints `ok=1` (mutation-case-kagi-census.md:111-122,
:251-253). After: `sha256sum pristine.sh` still `275d8294…53009f`; size/mtime
unchanged; kagi `git status` clean for the path; scratch copy `cmp`-identical
(mutation-case-kagi-census.md:54-56).

## Third case — cross-author confirmation (round 5, measured)

Rounds 2–3 measured two gates of one lane's craft (kumitate JS, kagi bash); round
4 re-cut their 20 mutants into the arm-class matrix, rows A–G
(`corpus/knowledge/arm-class-matrix.md`; its round-5 errata block carries
VER-T1's chmod enumeration fix and the JS "unreached" wording scope, `:498-525`).
Round 5 moves the **author axis**: the third gate is
`tsukuroi-shokunin/tools/tsukuroi-census.sh` — a four-plane host-health census
(bash, 977 lines, sha256 `084951be…c78c5` at measurement) written by a different
lane, in a third suite dialect: per-case `PASS <label> (exit N, VERDICT)` /
`FAIL <label>: …` lines asserting exit + verdict word + ERE evidence substrings,
plus two per-case structural guards (fixture tree byte-identical after the run;
`host=fixture-host` host-read guard), summary
`TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`
(`corpus/knowledge/mutation-case-tsukuroi-census.md:63-66`). The anti-claim was
pre-registered — a wildly divergent kill profile amends the matrix, recorded not
smoothed (`plans/round-5.plan.md:9-10`). It diverged: **6/10 killed (60 %)** — the
first measurement inside the 50-80 % band, and the first case that amends a row.

**Incident, headline not appendix** (`mutation-case-tsukuroi-census.md:9-35`): the
substrate moved mid-run — a concurrent lane (tsukuroi's own S5-1) hardened the
tool at 14:06:23 (+56 lines, 0 deletions, 9 new selftest cases, 26 → 35). So the
assigned "original sha256 before = after" claim is **unsatisfiable**; every
measured cell still sits on the frozen pre-hardening copy (sha re-verified at the
end), and the provable negative is "this lane's writes never touched the
substrate". §6 replays the four survivors on the hardened revision: B10 killed by
a new case; B7/B8/B9 still survive it.

**Third kill-rate table** (control green rc 0, 1.77 s; 11 runs in 19.6 s; every
run enumerated `(26 cases, …)`, none inconclusive; composition 6 kill-aimed + 4
hole-aimed — `mutation-case-tsukuroi-census.md:63-79, :86-102`):

| Mutant | Class | Site | Verdict | Failing cases (count) |
|---|---|---|---|---|
| B1 | inverted condition (nvidia guard) | `:473` | killed | 2 — healthy-gpu, blocked-gpu (case 15 token-only; exit matched) |
| B2 | boundary, rc tolerance {0,1}→{0,2} | `:281` | killed | 3 — backup-only, sample-drift, sample-error (case 13 token-only) |
| B3 | dropped fail-closed arm (empty-ring) | `:434-452` | killed | 1 — empty-ring (`exit 0 wanted 2`) |
| B4 | weakened kind pin (journal classifier) | `:578` | killed | 1 — boot-errors (exact class tally) |
| B5 | off-by-one count (drift `+1`→`+2`) | `:615` | killed | 1 — timer-drift (`timer_drift=1` tripwire) |
| B6 | behavior predicate (rollup `worse()`) | `:210` | killed | 21 — every non-HEALTHY case |
| B7 | boundary / cap unreached (`SAMPLE_N` 8→9) | `:160` | **survived** | 26/26; probe: 9-package input samples 9 (pristine 8) |
| B8 | wrong exit-code mapping, out-of-band | `:935` | **survived** | 26/26; probe: `--bogus` rc=1 (pristine rc=2) |
| B9 | reported-but-unasserted verdict fields | `:967` | **survived** | 26/26; probe: `packages=HEALTHY systemd=DEGRADED` under a DEGRADED verdict |
| B10 | unreached arm (PCI-unreadable) | `:487-493` | **survived** | 26/26; probe: pristine BLOCKED → mutant HEALTHY |

Calibration: pre-registration held 10/10 on verdicts **and** 10/10 on failing-case
counts — the first of the three sweeps with no miss, credited to parsing the case
grammar before writing the defects (`mutation-case-tsukuroi-census.md:74-75,
:282-287`).

**Matrix hold — three cases, seven rows** (r5 cells are that note's measured
readings; `mutation-case-tsukuroi-census.md:200-266`):

| Row | JS r2 | bash r3 | bash r5 (third author) | 3-case reading |
|---|---|---|---|---|
| A verdict paths | D2 survives on the tail | B10 survives on summary fields | B9 survives on roll fields | **holds** — asserted stem protected (all 6 kills read through it), unasserted remainder not; new shape: the one full-roll-line assert sits on the all-HEALTHY fixture where a field swap is invisible |
| B fail-closed arms | D8 killed (exit-2 cases) | B8 killed (2 cases) | B3 killed (1); **B8 survives** (`:935`, no case) | **amended** — exit-map protection is bound to *executed refusal paths*, not the artifact; three gates, three exit-map philosophies for the same epistemic class |
| C counts | D1/D6/D7 killed | B2/B7 killed | B5 killed (1) | **holds** — asserted counts die (third exact-count tripwire `timer_drift=1`); cap reachability is per-cap (B7: fixture 4 vs cap 8) |
| D reported-unasserted | D2, D10 survive | B10 survives | B9 survives + §3.1 field inventory | **holds, 3rd author** — the only class surviving in all three; here it sits in verdict *products*, not just a summary tail |
| E unreached arms | none (D4/D5 reached) | B5 survives | B10 survives; §3.2 static inventory | **promoted toward pattern, still proposed** — 2 bash instances + inventory, zero JS instances; repair shape (add a case per arm) consistent |
| F coordinated edits | unprobed | unprobed | unprobed (10 single edits) | **unknown in all three** (U1 each) |
| G behavior predicates | D3/D9 killed | B1/B3/B6/B9 killed | B1/B4/B6 killed | **holds 9/9 across three gates**; width amendment: B6 kills 21/26 — width follows mutant placement (distance to the shared exit channel), not language |

**What the third data point changed** (each measured; none smoothed):

1. **The 80 % headline was composition, not method — bind every rate to its
   composition.** 80 / 80 / 60 at compositions 6-kill+4-hole (this case): a rate
   quoted without kill-aimed vs hole-aimed is not comparable across sweeps (E3,
   `mutation-case-tsukuroi-census.md:295-299`). The bands table's 50-80 % row is
   now the measured one, superseding the "band interiors unprobed" (U) — >80 %
   and <50 % stay unprobed, and the 50 % crossover is still unmeasured.
2. **Row B is narrower than the pair admitted.** "Fail-closed exit-map
   protected" holds only per executed refusal path: B8's out-of-band usage
   refusal (`:935`) has no case and survives a 2→1 flip. The exit-2 *species*
   also differ by author: JS environment failure, kagi malformed-data, tsukuroi
   cannot-assess / cannot-tell-clean-from-empty.
3. **Row E's second instance landed — and the class still is not admitted.** B10
   (PCI-unreadable, probe: pristine BLOCKED vs mutant HEALTHY) reproduces B5's
   shape in another author's bash gate; with §3.2's dozen static arms the class
   now has a repair recipe, but both instances are bash and no JS instance
   exists, so it stays *proposed*.
4. **Width is not a language property.** Round 3's near-singleton bash reading
   is inverted by B6 (21/26, the widest bash kill yet): the rollup edit sits on
   the shared exit channel every case asserts. Read width off placement, never
   off language.
5. **A hardening response was measured for the first time.** The concurrent
   S5-1 lane's 9 new cases closed exactly one of this case's four holes (B10)
   and left three open (B7's default site, B8, B9) on revision `aae45531`
   (`:305-320`) — and a concurrent, quoted-not-read sweep converged on 8/9 of
   the same hole classes (E4, corroboration not double-counting).
6. **Two suite mechanisms went unattacked:** the per-case fixture-non-mutation
   and host-override guards, and the whole systemd plane (no mutant, U3) —
   their load-bearing status is unknown.

**Three-case confidence statement** (PROVINCE's two-independent-lanes bar,
`PROVINCE.md:15-16`; three authors, three dialects, two languages):

- **Admitted with third-gate support:** reported-but-unasserted surfaces /
  asserted-stem-vs-remainder (3 gates); asserted counts and floors (3 gates);
  behavior predicates caught (9/9 across three gates); fail-closed exit-map
  protection **as narrowed** (case-coverage-bound).
- **Proposed:** unreached-arm survivors — 2 bash instances, no JS instance.
- **Unknown in all three:** coordinated edits (row F); rates >80 % and <50 %;
  the 50 % crossover; cross-host stability; the structural guards above.
- **Read the method, not the rate:** across three authors the constant is the
  survivor taxonomy (unasserted data / unreached arms / unmapped paths), not
  the headline percentage.

**What a fourth case would need to show.** A fourth bash sibling at 60-80 %
would add a table row and move nothing. It earns its round only by being one of:

1. **A second JS-family gate** — the author axis now has three points, the
   language axis one. A JS gate separates author from language behind width and
   survivor composition (a JS rollup-shaped mutant would test this section's
   placement reading).
2. **A coordinated-rewrite mutant** (row F's first entry) on any pinned suite.
3. **An unreached-arm instance in JS** — the one datum that would admit row E.
4. **A kill rate outside [50, 80]**, or a suite whose full-verdict-line pin sits
   on a discriminating fixture (row A's new shape) — does that gap close with a
   stricter pin style, or merely move?
5. **Mutants against the structural guards** (fixture non-mutation, host
   override, fail-closed token enums) and a systemd-plane mutant (U3).
6. **Re-runs of B7/B8/B9 against `aae45531` successors** — the hardening left
   three holes demonstrably open; whether they stay open is the live test of
   the "add a case" repair.

## The mutation service — running a sweep for an opting-in lane (round 6, measured)

Rounds 2–5 measured three fleet gates at tameshi's hand; round 6 turns the
method outward as the service the fleet census offered
(`fleet-suite-census.md:249-291`): an opting-in lane brings its own gate, the
service sweeps it hermetically and read-only, and returns a kill-rate table
plus recommendations — absorption stays with the owner lane. The first
engagement is **mado** (`corpus/knowledge/mutation-case-mado-verify.md:3-11`);
the run below is the worked instance this section formalizes, and the contract
it satisfies is the round-6 plan's measure clause (`plans/round-6.plan.md:30-34`:
pinned revision, one-command hermetic suite, recommendations-only).

### The opt-in contract — what the lane brings

1. **A pinned revision** — committed bytes of the gate with sha256, size, line
   count, mtime, and a porcelain-clean sibling tree at open. Mado's pin:
   sha256 `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13`,
   45334 B, 1098 newlines (the 1099th line carries no trailing newline). A
   moved substrate needs a re-pin, never a re-interpretation of the old table.
2. **A one-command hermetic suite** invocable against a copy — mado's gate
   takes `bash "$MUTANT" --selftest`; it must exercise the copy it is handed
   (mado's selftest re-enters `$0`), print its own executed count and verdict
   (`MADO_SELFTEST: 28/28 assertions passed` on green), and read no live path
   (`mutation-case-mado-verify.md:44-49`).
3. **A clause-mapped defect spec** — one single-edit defect per declared
   contract clause, pre-registered `expect: killed|survived`. Mado's: 10
   defects over six clauses — A verdict token · B UNKNOWN-never-CLEAN · C exit
   map · D declared-plane census · E sha comparison · F reader fallback
   (`mutation-case-mado-verify.md:51-55`).
4. Nothing else. The service never edits, repairs or re-pins the gate; a
   needed change is a recommendation to the owner (round-6 anti-claim,
   `plans/round-6.plan.md:23-25`).

### The protocol — ordered, fail-closed

All writes in scratch, through the pinned harness `tools/mutate-and-run.sh`
(the mado run's revision `597e1419…ff6331b`, 1001 lines; every run log carries
its own `MUTATE_TOOL` pin):

```bash
bash tools/mutate-and-run.sh --target <gate> --defects <spec> \
     --suite 'bash "$MUTANT" --selftest' --workdir <scratch>
```

1. **Pin + pristine.** The target is copied to a pinned pristine; every mutant
   is a fresh byte copy; the original is never a write target.
2. **Spec parse + uniqueness.** Every `@old` must occur exactly once, asserted
   **before any suite run**; `@new == @old` is refused. Any spec failure is
   `MUTATE: SETUP (<reason>)`, exit 2 — no headline.
3. **Control first.** The unmutated copy must run green; a red control exits 2
   (kills could not be attributed).
4. **One mutant per defect**, one suite run each: KILLED (suite exit ≠ 0) /
   SURVIVED (exit 0) / INCONCLUSIVE (timeout 124, or 126/127 not runnable).
5. **Restore re-check.** Target sha256 before = after — `MUTATE_RESTORE:
   OK|DRIFT`.
6. **Headline + evidence.** `MUTATE: DONE (… killed=… survived=…
   inconclusive=… kill-rate=…%)`; exit 0, DEGRADED exit 1 on any inconclusive.
   The evidence dir keeps pristine, every mutant, `evidence/<id>.out`,
   `results.tsv`, `spec.copy` (`MUTATE_EVIDENCE: <dir>`).

Pre-register the expected table before the run: T6-1 wrote its 10 verdict
predictions and six survivor classes first, and the prediction held 10/10
(`mutation-case-mado-verify.md:73, :187-189`).

### The boundaries — what a service run is not

- **Single-edit mutants only** — coordinated rewrites are unmeasured (matrix
  row F); a rate is bounded by its defect vocabulary.
- **Hermetic suites only** — no substrate-drift claim; results are
  per-revision and per-host (census §5 scope, `fleet-suite-census.md:288-291`).
- **Read-only** — target sha before = after and the sibling tree stays
  porcelain-clean; the provable negative is "the service's writes never
  touched the gate" (`mutation-case-mado-verify.md:57-59`).
- **Findings kept, never smoothed.** A survivor is a gap named with its class;
  a low kill rate is a report, not a service failure. Mado's 40 % is the
  first point below the 50-80 band, and it reads as composition (4 in-surface
  + 6 out-of-surface, measured 4/4 and 0/6), not as a suite regression
  (`mutation-case-mado-verify.md:66-72`).
- **Recommendations-only** — absorption stays with the owner; no acceptance
  means the recommendation is recorded unabsorbed
  (`mutation-case-mado-verify.md:237-238, :240-260`).
- **The harness itself is pinned per run.** The mado round saw the tool move
  mid-round by a concurrent lane (re-pin `b56c6e57…`); every number stays tied
  to the executed revision and the drift is recorded, not smoothed
  (`mutation-case-mado-verify.md:17-23`).
- **Sensitivity, not truth** — a sweep measures what the suite can detect,
  never whether the gate's verdicts are right
  (`mutation-case-mado-verify.md:229-230`).

### The report shape — what the opting-in lane receives

- pins: target sha256/size/lines, tool sha256, suite command + control line,
  spec clause map;
- the kill-rate table: control + one row per defect (id, clause, exact edit
  site, exit, verdict, failing-case labels for kills, verbatim from
  `evidence/<id>.out`);
- **survivor non-equivalence probes**: each survivor re-run on an input
  outside the suite's fixtures that exercises the mutated surface, pristine
  vs mutant outputs recorded (`mutation-case-mado-verify.md:103-115`);
- restore proof `MUTATE_RESTORE: OK` (sha before = after) + the tree-clean
  check;
- recommendation + named unknowns, as a corpus note; the note is the only
  fleet file the run writes (`mutation-case-mado-verify.md:8-9`), and its
  reproduce block rebuilds the sweep (`:262-293`).

### The mado run (T6-1, 2026-10-14) — measured

Target `mado-shokunin/tools/mado-verify.sh` @ `d7edaab4…d0e13`; tool
`597e1419…`; suite `bash "$MUTANT" --selftest`; control `MADO_SELFTEST:
28/28 assertions passed`, exit 0. **10 defects → 4 killed / 6 survived,
kill rate 40 %, 0 inconclusive**; 11 runs in 5.26 s
(`mutation-case-mado-verify.md:57-63`).

- Killed (4): D1 verdict token · D2 UNKNOWN guard · D4 DIVERGED exit · D6
  census drop — each on the scenario that names it (`:77-89`).
- Survived (6), each with its probe reading (`:103-115`): D3 skip-row
  `SKIP`→`PASS` (row + counts differ: `pass=17 skip=1` → `pass=18 skip=0`);
  D5 failure-path exit 2→1 (unobservable on a green run; identical failure
  block); D7 count tolerance `-ne`→`-lt` (undeclared 18th source: pristine
  DIVERGED → mutant CLEAN); D8 sha-pin NOTE text (`drifted` → `matches`);
  D9 boundary proof (a real mid-run change: pristine DIVERGED → mutant
  CLEAN); R1 tomllib arm (fake `PASS` on an unverifiable row).
- `MUTATE_RESTORE: OK` — target sha256 before = after; fleet tree
  porcelain-clean; an independent audit lane re-cut the same 10 defects with
  its own driver and reproduced 4 killed / 6 survived
  (`/tmp/w6-aud-t6-work/presweep-174248.txt`, 2026-10-14).

## The leg ledger — replay, receipt, and how it is read (round 7, measured)

Round 7 turns `--regression` from the tool's two-case self-check into the
fleet's **leg ledger**: every recorded mutation case is a leg, replayed at its
pinned original revision. Four legs at this revision — `js-kimi-census`
(r2, killed 8/10 = 80 %), `bash-surface-census` (r3, 8/10 = 80 %),
`bash-tsukuroi-census` (r5, 6/10 = 60 %), `bash-mado-verify` (r6, 4/10 = 40 %)
— each with its recorded kill-rate as its expectation
(`tools/mutate-and-run.sh:72-109`, :511-522). The ledger is the receipt
tameshi's records cite for kill-rate claims; the standing per-gate rate rows
are `corpus/knowledge/fleet-kill-rate-ledger.md`.

### Using the ledger

- **One command replays every leg.** `bash tools/mutate-and-run.sh
  --regression [--workdir DIR] [--keep]` — default scratch is a fresh
  `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless
  `--keep`, kept on FAIL/SETUP, never removed when `--workdir` was given. Exit
  map: 0 all legs PASS · 1 ≥1 leg FAIL · 2 cannot verify
  (`tools/mutate-and-run.sh:72-109`, :891-975).
- **Each leg's bytes come from the repo's git object store, not the working
  tree.** `git show <rev>:<path>` materializes the pinned blob into the case
  workdir and its sha256 must equal the recorded pin (`:733-791`; the
  `REGRESSION_PIN` line names repo + rev + path + pin). A sibling tree that
  has drifted past the recorded revision — tsukuroi's and mado's pins are
  ancestors of their HEADs today — or carries uncommitted edits cannot move a
  replay; a missing repo/rev/blob or a pin mismatch is a SETUP refusal before
  any suite runs.
- **Every kill-rate claim carries the receipt.** Cite `REGRESSION: PASS
  (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)` with the
  executed tool sha (`REGRESSION_TOOL`) and the per-leg pins
  (`REGRESSION_PIN`) — the receipt is tied to the tool revision that ran and
  to each leg's pinned bytes.
- **Contribution contract — what a case carries to become a leg.** A case is
  a pinned file set: fleet-relative target path + git revision + sha256 pin; a
  defect spec (one exact single edit per defect, `@old` unique in the pinned
  bytes, `@new != @old`); a one-command hermetic suite run with `$MUTANT` that
  exercises the copy and prints its own executed count and verdict; and the
  recorded verdict table, which is the leg's expectation — exact for ledger
  legs. The four legs above are the measured carriage of exactly this set
  (pins/revisions/tables `:511-522`; specs `:550-728`; leg registry
  `:927-944`). (U) A fleet-contributed case is not yet exercised; the ledger's
  case set is tameshi-carried at this revision.

### Reading a receipt — the discipline

1. **Read the block, not the last line.** `REGRESSION_TOOL` ·
   `REGRESSION_DATE` · `REGRESSION_BAND` · `REGRESSION_EXPECT` · one
   `REGRESSION_PIN` per leg · per leg one `REGRESSION_SWEEP` +
   `REGRESSION_TABLE` + `REGRESSION_CASE` · `REGRESSION_DEFECT` rows for
   differences · `REGRESSION_WORKDIR` · the closing `REGRESSION:
   PASS|FAIL|SETUP` line.
2. **PASS is exact for ledger legs.** Every case line `PASS (band:
   killed-delta<=0 flips<=0 inconclusive=0 defects=10)` and every
   `REGRESSION_TABLE … match=10/10 … flips=0`; the closing line's
   `cases=4 passed=4`. Measured instance (T7-1, 2026-10-14; replayed by this
   lane under the same revision `cf41efaa…`): four legs, all `match=10/10 …
   flips=0`, `REGRESSION: PASS (cases=4 passed=4; ledger legs exact:
   killed-delta<=0 flips<=0)`, rc 0.
3. **FAIL names its rows.** `REGRESSION_DEFECT <leg> <id>: measured=…
   recorded=…` (an `ABSENT` on either side counts), `REGRESSION_TABLE …
   flips=n`, and the case's `REGRESSION_CASE … FAIL (out of band: …)`. A
   doctored table was measured caught: `REGRESSION_DEFECT js-kimi-census D1:
   measured=KILLED recorded=SURVIVED` → `match=9/10 … flips=1` →
   `REGRESSION_CASE js-kimi-census: FAIL (out of band: killed-delta=1
   flips=1)` (negative run, `/tmp/w7-tameshi-1/flip-run.out`). Quote the rows,
   never the word; never hand-re-sweep to "confirm" a FAIL — the replay goes
   through the ledger and the divergence is the finding.
4. **SETUP is not a verdict.** A missing repo/rev/blob, a pin mismatch, or a
   refused sub-sweep means *cannot verify* — never a pass, never a suite
   failure; the fix is the environment (repo/rev/pin), never a
   re-interpretation of the recorded table.
5. **The ledger proves the instrument, not the gates.** A leg PASS says the
   tool reproduces the recorded table on the pinned bytes; it does not say the
   gate protects anything today. The rates live in
   `fleet-kill-rate-ledger.md` with their composition and revision — and a
   rate is never implied to hold at a later revision than its sweep pin.
6. **Attesting a sibling's claim uses the same discipline** (round-7
   attestation leg): replay the declared pins read-only, return the receipt —
   or name the missing piece; the sibling's note is never edited
   (`plans/round-7.plan.md:11-15`).
7. **The ledger's own arms are selftested.** `bash tools/mutate-and-run.sh
   --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 at
   `cf41efaa…` — including a git-materialized replay passing at exact
   tolerance, a drifted working tree not moving a git-pinned leg, pin
   mismatch / unresolvable revision as SETUP, and a single flipped entry
   failing loudly. The r4-2 tolerance (`killed-delta<=1 flips<=1`) remains the
   fixture-mode default and is exercised by the selftest only.

## The re-sweep cadence and the six-case confidence statement (round 8, measured)

Round 7 left its own gap open in writing: "this ledger's update cadence is a
convention, not a mechanism" (`corpus/knowledge/fleet-kill-rate-ledger.md:235-237`,
U9). Round 8 closes it by measurement: **the cadence is a pin read executed at the
tick** — three readings per case, three triggers, one re-pin rule — and the same
tick read is the ground the six-case confidence statement below stands on. No
daemon, no timer: "standing" is the ledger + the policy + an executed command at
the round boundary; whether any fleet driver would ever invoke the command with
no lane acting stays [U].

### The tick and the pin read

- **The tick is the round boundary.** The fleet driver idiom ends a lane's round
  on a report file and ticks 450 s (`scripts/shokunin-watchdog.sh:3-5`), and its
  lane map does not name tameshi (`:14`) — tameshi's tick is its own round series
  [I].
- **Per case, two readings:** the target's relation to the fleet's live bytes
  (`current` / `stale` / `drift`) and the tool's relation to the last run
  (`held` / `moved`):

| Reading | Rule | What it means |
|---|---|---|
| `current` | `git show HEAD:<path>` sha256 == the recorded pin | the swept bytes are the gate's live blob |
| `stale` | the recorded revision is an ancestor of HEAD and the live blob differs | the gate moved past the recorded revision; the table's revision is historical, the table is not wrong |
| `drift` | the worktree differs from its HEAD (`git status --porcelain -- <path>` non-empty, or the live file's sha ≠ the HEAD blob's) | uncommitted bytes; a reading for ledger hygiene — round 7's `git show <rev>:<path>` replay is already immune to it |
| tool `held` / `moved` | the harness sha == / ≠ the sha on the last `REGRESSION_TOOL` / `MUTATE_TOOL` line | the instrument moved since the table was measured |

Executed instance — this lane, tick 2026-10-14T19:15:14Z, host `plazir27`, tool
`cf41efaa…` (`sha256sum tools/mutate-and-run.sh`), scratch
`/tmp/w8-tameshi-t84/pin-read.txt`:

```
case                     recorded rev   live HEAD   relation   pin vs live blob
js-kimi-census           175de6ba       175de6ba    current    83016d45 == 83016d45
bash-surface-census      fecee874       fecee874    current    275d8294 == 275d8294
bash-tsukuroi-census     165307fe       aa136d69    stale      084951be != bba6cdf6
bash-mado-verify         eead56b2       0c20a76f    stale      d7edaab4 != 90d50cdd
kagi checklist-run       HEAD (r8)      fecee874    current    7e5ec98b == 7e5ec98b
kumitate claims-check    HEAD (r8)      175de6ba    current    e9a21b44 == e9a21b44
```

4 × `current` · 2 × `stale` · 0 × `drift`; tool `held`; all six worktrees clean
(0 porcelain lines on every path) *at the tick*.

- **Re-read six minutes later (19:20:29Z) — a live `drift`:** mado's in-flight
  round-8 edit (`git status --porcelain -- tools/mado-verify.sh` → ` M`; live file
  `dc864c6a…`, 99,716 B, mtime 16:19:40, vs HEAD blob `90d50cdd…`) moves that
  path to `stale` **and** `drift`; every other row reads as above. The pin read is
  a timestamped observation, re-run at the next tick — never carried as a
  standing claim.

- **Falsifiers, aimed at the reader** (scratch, read-only; the engine's own
  doctored-pin refusal is a different arm, selftested
  `MUTATE_SELFTEST: 67/67`): a case whose row points at a superseded blob reads
  `stale` (tsukuroi and mado above); a scratch copy of a live gate with one line
  appended reads `drift` (`/tmp/w8-tameshi-t84/drift-demo.txt`; substrate 0
  porcelain lines after); an untouched case reads `current`.

### Triggers T1–T3 and the re-pin rule

- **T1 — a case reads `stale`** → re-measure at the live revision, or record the
  STALE cell with its reason; **never an edit of the recorded table**. Live
  instances today: tsukuroi `084951be…` (6/10) → live `bba6cdf6…`; mado
  `d7edaab4…` (4/10) → live `90d50cdd…`.
- **T2 — the harness sha ≠ the revision a case's table was measured under** →
  re-run the reproduction under the new revision and record both pins. Precedent:
  the mado spec re-cut under `b56c6e57…` with identical verdicts and mutant shas
  (`mutation-case-mado-verify.md:17-23`); the harness itself moved four times in
  one day (`597e1419…` → `b56c6e57…` → `4dc69ef9…` → `e3f838d4…` → `cf41efaa…`)
  and no recorded table was re-interpreted for it.
- **T3 — an owner lane records a re-run at a new revision** → an appended row;
  §1–§4 are never edited (`fleet-kill-rate-ledger.md:170-173`).
- **The re-pin rule.** A moved pin is never re-interpreted against the new bytes
  (:811-812). The old table stays; the moved case lands at its newest revision
  with both shas and the delta, appended. `moved=0 stale=0` is a complete
  outcome, recorded as such — drift is never manufactured by re-cutting cases.
  The replay receipt at this revision (this lane, 19:15:54Z, rc 0):
  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0
  flips<=0)`, every leg `match=10/10 … flips=0` — the recorded tables hold at
  their own pinned blobs regardless of the live drift above.

### Six-case confidence statement (round 8, measured)

The case set at this write: the four embedded legs plus the two queue gates
entering in round 8.

| # | case (author · file) | language | suite | rate · composition | revision |
|---|---|---|---|---|---|
| 1 | js-kimi-census (kumitate · `scripts/kimi-census.mjs`) | node ESM | 43 | 8/10 = 80 % · 10 kill-aimed | r2 · `83016d45…` |
| 2 | bash-surface-census (kagi · `corpus/surface-census.sh`) | bash | 16 | 8/10 = 80 % · 10 kill-aimed | r3 · `275d8294…` |
| 3 | bash-tsukuroi-census (tsukuroi · `tools/tsukuroi-census.sh`) | bash | 26 | 6/10 = 60 % · 6 kill + 4 hole | r5 · `084951be…` |
| 4 | bash-mado-verify (mado · `tools/mado-verify.sh`) | bash | 28 | 4/10 = 40 % · 4 in + 6 out | r6 · `d7edaab4…` |
| 5 | kagi `corpus/checklist-run.sh` (T8-1) | bash | 34 | 7/15 = 47 % · 7 kill + 8 hole | r8 · `7e5ec98b…` |
| 6 | kumitate `scripts/claims-check.mjs` (T8-2) | node ESM | 39 | 7/10 = 70 % · 6 kill + 4 hole | r8 · `e9a21b44…` |

Cases 5–6 were measured this round in the lanes' own scratch (controls
`CHECKLIST_SELFTEST: PASS (34 cases)` and `CLAIMS_SELFTEST: 39/39 pass`;
`MUTATE_RESTORE: OK` both; tool `cf41efaa…`; runs under
`/tmp/w8-tameshi-t81/sweep/` and `/tmp/w8-t8-2-claims/work/`), and both notes
landed while this section was being written:
`corpus/knowledge/mutation-case-kagi-checklist.md` and
`corpus/knowledge/mutation-case-kumitate-claims.md` (both still being appended by
their own lanes — re-read a note's header rather than quoting a size). The ledger
rows and any `--regression` leg for either are follow-ups the notes themselves
name (claims note E3) — **the ledger rows are the authority once they land, and
an unlanded leg is named debt, never assumed**.

**State the real diversity — language is the weakest axis here.** Six cases, but
**two language classes** (node ESM ×2, bash ×4 — shebangs read from the pinned
bytes: `#!/usr/bin/env node` ×2, `#!/usr/bin/env bash` ×4), **four author lanes**
(kumitate ×2, kagi ×2, tsukuroi, mado) and **gate grammars that stay per-gate,
not per-language** (five measured families over the six gates: kumitate's two
node gates share `*_SELFTEST: n/m pass` + `FAIL` rows; kagi's two bash gates
differ — `ok-case`/`bad-case … got …` + `SELFTEST:` vs `checklist-selftest: …` +
`CHECKLIST_SELFTEST:`; tsukuroi `PASS <label> (exit N, VERDICT)`; mado `n/n
assertions`). A "five languages/authors" reading is not supported by the measured
roster: the case set multiplies by *author and gate shape*, not by language —
round 8's two additions are one bash gate and one node gate, both
already-measured language classes, and the round-3/5 finding already placed the
differences in kill width and composition, not in language. Counting tameshi's
own harness meta-sweep (ledger §2) would add a seventh *artifact* and a fifth
*author* — a boundary item, not a case. Count what varies: authors (four), gate
grammars (five families), and composition, which binds every rate above.

Against the round-5 three-case statement (this page's "Third case…" section) the
six-case reading moves only where measurement moved:

- **Holds, more instances:** reported-but-unasserted / asserted-stem-vs-remainder
  — the checklist note classifies `C1` (`UNMATCHED-ITEM`) and `F2` (`--only …
  failed=0`) as family (a) and six more as unreached inputs
  (`mutation-case-kagi-checklist.md:180-194`); the claims note's `D7` reproduces
  kimi's `slice(0, 6)` cap on a second kumitate gate, and its `D8` is a new
  sub-shape — a threshold the case is named for and cannot see
  (`mutation-case-kumitate-claims.md:285-291`). Rates bind to composition, and
  the band now reads 40 / 47 / 60 / 70 / 80 / 80.
- **Amended by the sixth case:** unreached-arm survivors — `D9` is the class's
  **first JS instance** (claims note Row E, `:249-254`), so the round-5 reading
  ("two bash instances, still zero JS") no longer stands; the class reading is
  now "an instance in each language class", still per-arm and not generalized.
- **Unknown in all six:** coordinated rewrites; cross-host stability; the 50 %
  crossover; the two round-8 notes' own unknowns.
- **Read the method, not the rate** — at six cases the constant remains the
  survivor taxonomy and the composition rule, not the headline percentage.

## The cadence's first scheduled tick, and the service's limits (round 9, measured)

Round 8 landed the cadence as policy + a demonstrated pin read; round 9 runs it at
a round boundary — the mechanism's **first scheduled tick** — and lands the piece
an intake decision needs beside it: **what tameshi refuses to mutation-test**.
No daemon, no timer: the tick is the round-8 section's command, executed and
pasted below; whether a fleet driver would ever invoke it with no lane acting
stays [U] (`:1019`).

### The tick, executed

Pin read at the round-9 boundary, **2026-10-14T20:00:34Z** (host `plazir27`;
scratch `/tmp/w9-tameshi-t93/pin-read-final.txt`; recorded pins/revisions are the
harness's `PIN_*`/`REV_*` for the four embedded legs
(`tools/mutate-and-run.sh:511-518`), and the r8 notes' pins for cases 5–6):

```
case                     recorded-rev live-HEAD    anc      pin==live live==HEADblob worktree   reading
js-kimi-census           175de6ba     175de6ba     yes      83016d45==83016d45 83016d45==83016d45 clean      current
bash-surface-census      fecee874     fecee874     yes      275d8294==275d8294 275d8294==275d8294 clean      current
bash-tsukuroi-census     165307fe     72b038da     yes      084951be==bba6cdf6 bba6cdf6==bba6cdf6 clean      stale
bash-mado-verify         eead56b2     12c8f08a     yes      d7edaab4==7da4ec50 7da4ec50==7da4ec50 clean      stale
kagi-checklist-run       fecee874     fecee874     yes      7e5ec98b==7e5ec98b 7e5ec98b==7e5ec98b clean      current
kumitate-claims-check    175de6ba     175de6ba     yes      e9a21b44==e9a21b44 e9a21b44==e9a21b44 clean      current
```

4 × `current` · 2 × `stale` · 0 × `drift`; tool **held** at `cf41efaa…`
(`sha256sum tools/mutate-and-run.sh`); all four sibling trees porcelain-clean
(0 lines each) *at the tick*. Both `stale` cells are their repos' committed HEAD
blobs — no drift at this read: tsukuroi-census `084951be…` → `bba6cdf6…`
(HEAD `72b038da`), mado-verify `d7edaab4…` → `7da4ec50…` (HEAD `12c8f08a`). The
round-8 tick read mado's cell as `90d50cdd…` (clean) and, six minutes later,
`dc864c6a…` (dirty); that in-flight edit is now committed as `7da4ec50…` — the
drift closed into a `stale` cell. The tick is a **timestamped observation,
re-run at the next boundary** — never carried as a standing claim.

Falsifier, aimed at the reader (scratch copy, `/tmp/w9-tameshi-t93/falsifier/`):
the same script with js-kimi-census's recorded pin replaced by a superseded sha
(`084951be…`) reads `stale`, while the row as recorded reads `current` — same
substrate, same moment; the reading follows the row's pin, not the substrate's
history.

The ledger carries its own record of this same tick — **ER-4**
(`corpus/knowledge/fleet-kill-rate-ledger.md:318-353`), appended independently by
the tick lane (T9-1): the same six readings (its second raw pass 20:00:29Z), both
drift-event chains (`084951be…` → `bba6cdf6…`; `d7edaab4…` → `7da4ec50…`), and the
same regression receipt — two records of one tick, kept un-merged and agreeing.

Re-read two minutes later (**20:03:34Z**, same scratch): both moving cells now
read `stale + drift` — tsukuroi's worktree `b54f5732…` vs its HEAD blob
`bba6cdf6…`, mado's `31364115…` vs `7da4ec50…`, both ` M` on
`git status --porcelain`; the owners' own round-9 lanes are editing their gates
(ER-4's addendum, `:354-360`, records the same continuation at 20:02Z with its
then-current shas). The tick's clean reading stands at its timestamp; a moving
file is never re-interpreted, and any re-sweep must pin the revision it measures
(T3).

### The receipt at this boundary

Run at the tick (this lane; `--selftest` 19:58:49Z, `--regression`
`REGRESSION_DATE 2026-10-14T19:58:59Z`; logs `/tmp/w9-tameshi-t93/selftest.txt`,
`/tmp/w9-tameshi-t93/regression.txt`):

- `--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0.
- `--regression` → 4 legs, each `match=10/10 … flips=0` (killed 8/8/6/4),
  closing `REGRESSION: PASS (cases=4 passed=4; ledger legs exact:
  killed-delta<=0 flips<=0)`, rc 0, tool `cf41efaa…`; workdir kept
  `/tmp/w9-tameshi-t93/regression`.

The legs replay their pinned blobs — git-materialized
(`tools/mutate-and-run.sh:733-791`), so the two `stale` substrates cannot move
them; re-verified at this boundary, since all four legs matched while cases 3–4
read `stale`. Cases 5–6 are still not embedded: their rows carry no `REGRESSION`
line — named debt, not smoothed (`fleet-kill-rate-ledger.md:282`).

### The re-pin semantics, as executed

- **T1 fired for two cases.** The rule is the round-8 section's (`:1069-1090`):
  re-measure at the live revision, or record the STALE cell with its reason —
  never an edit of the recorded table.
- **The intake precondition round 8 named is present, not errata.** The opt-in
  protocol carries the re-pin rule — "A moved substrate needs a re-pin, never a
  re-interpretation of the old table"
  (`corpus/knowledge/service-optin-protocol.md:59-62`) — cited here.
- **What a re-sweep produces lands appended.** The outcome is an appended row in
  `fleet-kill-rate-ledger.md` (append-only), the recorded tables byte-identical;
  a rate never travels to a later revision. ER-4 and its addendum name the
  re-sweeps of the two moved cases as follow-on rows — open at this write (the
  addendum reads them `stale + drift`), and an unlanded leg is named debt, never
  assumed.

### The service's limits — what tameshi refuses to mutation-test

The cadence applies this table at intake. Each refusal carries a measured anchor —
a refusal without an anchor is not written; the table states refusals, it does not
adjudicate them. (Anchors `:…` are this page; the others are repo-relative.) The
standalone note `corpus/knowledge/service-limits.md` (T9-2, this round) carries
the same rows as the detail of record — verbatim anchor quotes, the trigger column
and the intake-precondition check; this page is the compact rendering, and a
divergence between the two is the finding, never smoothed.

| # | Refusal | What it means | Anchor |
|---|---|---|---|
| a | No pinned revision / no opted-in lane | no sweep — the queue is an offer, not a schedule; a round with no opt-in records the no-opt-in line | `service-optin-protocol.md:26-30`; `fleet-suite-census.md:277-286` |
| b | No one-command hermetic suite | refused before any suite runs — the request shape requires it; spec/control failures are `MUTATE: SETUP`, exit 2, no headline | `:813-817`; `:840-844` |
| c | A moved substrate without a re-pin | a recommendation, never an edit — the service never edits, repairs or re-pins a gate | `:823-825` |
| d | Live substrates / sessions | never read; a live-plane probe is a PATH-level stub, never the session | `service-optin-protocol.md:129-132` |
| e | Credential material / endpoint health | out of province — report, never absorb | `PROVINCE.md:14-18`, `:20` |
| f | Product semantics — whether a gate's verdicts are right | never measured — sensitivity ≠ truth | `:879-881`; `fleet-suite-census.md:288-291` |
| g | Coordinated multi-edit rewrites | outside the defect vocabulary — no rate claimed | `fleet-kill-rate-ledger.md:220` (U2) |
| h | The exit-flatten family | a harness boundary — named, not fixed | `service-optin-protocol.md:267-269` |
| i | A directed-repair re-run presented as a rate | recorded as directed repair, not an independent rate | `fleet-kill-rate-ledger.md:35-36` |
| j | Foreign scratch | never removed | `service-optin-protocol.md:86-91` |

Anchors re-resolved 2026-10-14 on the live bytes; a reader on a differing revision
re-resolves rather than trusts.

## The operator's runbook and the six-leg regression (round 10, measured)

Round 7 made `--regression` the ledger's replay gate; rounds 8–9 left two
named gaps: the registry ran four legs with cases 5–6 "still not embedded —
named debt" (`:1226-1228`), and the operator the arc was built for had no
single entry point. Round 10 closes both — the runbook lands (T10-1, this
round), and the leg cut resolves as an **embedding** of cases 5–6 (T10-2),
never a re-cut.

### The operator's runbook — `corpus/knowledge/operator-runbook.md`

- **What it is.** One operator-facing document (`e1e349b6…` / 511 L / 31 416 B,
  uncommitted worktree file at this read; the sha governs): the tool, the
  six-case ledger, the opt-in protocol, the refusals, the cadence, and the
  regression mode — the loop runnable without oral context. It adds no gate
  measurement of its own; every line restates an anchored source.
- **Section map.** §0 quick start (the operator loop in one block) · §1 the
  service in one page · §2 the tool · §3 the six-case ledger · §4 the opt-in
  protocol · §5 the limits · §6 the cadence (tick, reading map, triggers
  T1–T3) · §7 the regression mode · §8 the operator's full loop (commissioning
  to append) · §9 that lane's executed receipts · §10 unknowns carried ·
  append-only errata.
- **Pointer, not a second home.** Its own rule: where it and an anchored
  source diverge, the anchored source governs — the same rendering/divergence
  rule this page applies to `service-limits.md` (`:1250-1254`).
- **Its receipts were executed at `cf41efaa…` (r7-1, four legs)** — §7's
  embedding-status line and §9's receipts were run there; its errata ER-R1/ER-R2
  record the r10-2 edit in motion and name the T2 remedy (re-run under the new
  revision, record both pins). The receipt below is that T2 record.

### The six-leg regression — usage and this round's receipt

At tool revision `75ed934d…` (`VERSION` = `mutate-and-run.sh r10-2`, 1 642 L;
uncommitted worktree file at this write), `--regression` replays **six**
embedded legs (list `tools/mutate-and-run.sh:85-89`; sources `:90-97`;
pins/tables `:550-559`; specs `:766`, `:841`; registry `:1132-1141` — line
anchors as read at `75ed934d…`, the sha governs):

| # | leg | target | recorded rev | recorded rate |
|---|---|---|---|---|
| 1 | `js-kimi-census` | kumitate `scripts/kimi-census.mjs` | `175de6ba` | 8/10 = 80 % |
| 2 | `bash-surface-census` | kagi `corpus/surface-census.sh` | `fecee874` | 8/10 = 80 % |
| 3 | `bash-tsukuroi-census` | tsukuroi `tools/tsukuroi-census.sh` | `165307fe` | 6/10 = 60 % |
| 4 | `bash-mado-verify` | mado `tools/mado-verify.sh` | `eead56b2` | 4/10 = 40 % |
| 5 | `bash-checklist-run` | kagi `corpus/checklist-run.sh` | `fecee874` | 7/15 = 47 % |
| 6 | `js-claims-check` | kumitate `scripts/claims-check.mjs` | `175de6ba` | 7/10 = 70 % |

- **Command, unchanged.** `bash tools/mutate-and-run.sh --regression
  [--workdir DIR] [--keep]`; default scratch
  `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless
  `--keep`, kept on FAIL/SETUP, never removed when `--workdir` was given. Exit
  map: 0 all legs PASS · 1 ≥1 leg FAIL · 2 cannot verify (SETUP) (`tools/mutate-and-run.sh:115-119`).
- **Where the bytes come from.** Each leg materializes from its repo's git
  object store at its recorded revision (`git show <rev>:<path>`) and the copy's
  sha256 must equal the recorded pin; a missing repo/rev/blob or a pin mismatch
  is a SETUP refusal before any suite runs. r10-2 also mirrors the blob's mode:
  a `100755` blob is `chmod +x`'d after materialization (`:104-106`, `:932-960`)
  — kagi's checklist gate re-execs itself in its selftest, `git show` carries no
  mode, and the leg refuses as SETUP without the bit (measured while the cut was
  made; the added selftest arms at `:1488-1527` cover the mirror).
- **Receipt, executed by this lane** (independent of the tool owner's; the
  owner's own run at the same revision, 21:00:24Z, closes identically),
  2026-10-14T21:02:39Z, tool `75ed934d…` before and after, scratch
  `/tmp/w10-t10-4-ev/` (regression workdir kept):
  - `--selftest` → `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0 —
    added arms include the exec-bit mirror and an embedded-ledger check that
    the six specs parse and agree with their recorded tables.
  - `--regression` → six legs, all exact: `match=10/10` (legs 1–4, 6),
    `match=15/15` (leg 5), every leg `flips=0 inconclusive=0`; closing
    `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0
    flips<=0)`, rc 0. Each `REGRESSION_PIN` line now carries the blob's
    `mode=` beside repo/rev/path/sha256, and `REGRESSION_EXPECT` lists six
    recorded rates.
- **The supersessions stay append-only.** The round-7 section's "Four legs at
  this revision" (`:925-929`) and the round-9 receipt's `cases=4`
  (`:1218-1222`) stand at `cf41efaa…`; the round-9 caveat that cases 5–6 were
  "still not embedded — named debt" (`:1226-1228`; ER-4 caveat (a)) is resolved
  at `r10-2` by embedding the recorded T8-1/T8-2 spec files (their 25 `@old`
  strings re-verified `count==1` against the pinned blobs) — the recorded
  tables are never edited and each leg's expectation is the rate its note
  recorded.
- **Reading a receipt** stays the round-7 discipline (`:965-1008`): read the
  block, not the last line; PASS is exact for ledger legs; FAIL names its
  `REGRESSION_DEFECT` rows; SETUP is not a verdict (fix the environment, never
  re-interpret a recorded table). The runbook's §7 is the operator's rendering
  of this command; on a differing revision the tool bytes and the run you
  executed govern.
- **Named debt, not smoothed.** The ledger's §1 embedding text still reads
  "cases 1 and 2 only" (`fleet-kill-rate-ledger.md:85-88`), superseded in the
  ledger by ER-2 (`:281`, four legs); a ledger row recording the six-leg
  registry is the ledger owner's follow-on — this page records the registry as
  measured at `r10-2`, and no ledger cell is edited from here.

## Final pointers — the standing map at the arc's close (round 11, measured)

Round 11 (training r10) is the arc's final round (`plans/round-11.plan.md:13`);
the LOG's rows name each round's training number — `round 4 (training r3)` …
`round 10 (training r9)` (`LOG.md:303-309`) — so this one is training r10 [I]. This
section adds no gate measurement of its own beyond the two executions under
*boundary readings* below; its job is the one thing the round sections never put
in one place: **where everything stands** — one pointer per standing artifact,
this boundary's own reads, the reader's entry points, and what the close leaves
open. Nothing here claims promotion or retirement: the arc ends, the service
remains, run by whoever the handoff names (`plans/round-11.plan.md:20-25`), and
the boundary tick this round runs was pre-announced in that plan (leg 1;
committed at `606716f`) before the wave existed — its announced-vs-fired pair
lands in the round's record, not here.

### The map — where a reader enters, artifact by artifact

| Artifact | Holds | Read it when |
|---|---|---|
| `corpus/knowledge/operator-runbook.md` | the operator's entry point (T10-1): §0 quick start · §2 the tool · §3 the six-case ledger · §4 opt-in · §5 limits · §6 the cadence (tick, reading map, T1–T3) · §7 the regression mode · §10 unknowns | you are the seat running the loop — renderer, not a second home: where it and an anchored source diverge, the anchored source governs (`:1294-1297`) |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | one row per gate — suite, rate + composition, survivors, last sweep + pin; §1–§4 byte-frozen, new rows appended below | before quoting any rate — the row is the standing receipt |
| `corpus/knowledge/service-limits.md` | the refusals, detail of record; this page carries the compact rendering (`:1246-1270`) | an intake question needs a refusal line |
| `corpus/knowledge/service-optin-protocol.md` | request shape, the re-pin rule, read-only guarantees, report shape, boundaries | your lane wants a sweep — or receives one |
| `corpus/knowledge/fleet-suite-census.md` | the suite census: the offer and the queue (surveyed-but-unmeasured pins) | picking the next case |
| `corpus/knowledge/service-standing-state.md` | the boundary note: fleet-visible vs lane-owned, handoff conditions, SC1–SC3 | taking the service over |
| `corpus/knowledge/mutation-case-*.md` (six) | per-case spec, verdict table, survivor probes, reproduce sections | re-deriving a recorded rate |
| `tools/mutate-and-run.sh` | the instrument: `--selftest`, `--regression` (six-leg registry, git-materialized replay) | any sweep or replay |
| `corpus/README.md` | the coverage map — one row per note, holds + sources | checking what the corpus holds |
| `plans/round-N.plan.md`, `plans/round-N-record-draft.md` | each round's plan and record by convention; the round-11 record lands there; the completion pack (`plans/completion-evidence.md`, this wave, uncommitted at this write) collects the per-round lines and debts | auditing a round's receipts |
| `LOG.md`, `SCORECARD.md` | the round rows and the move-log rows with their counting commands | provenance of any round |

### Boundary readings, executed by this lane

Two executions, nothing else measured here; scratch `/tmp/w11-t11-4-ev/`.

**Pin read** — the round-8 command set (`:1021-1053`), 2026-10-14T21:32:35Z:

```
case                 recorded-rev live-HEAD  relation  rec-pin  live-blob
js-kimi-census       175de6ba     175de6ba   current   83016d45 83016d45
bash-surface-census  fecee874     fecee874   current   275d8294 275d8294
bash-tsukuroi-census 165307fe     af8adf15   stale     084951be 10452443
bash-mado-verify     eead56b2     f7bfc9fe   stale     d7edaab4 93e43f8f
bash-checklist-run   fecee874     fecee874   current   7e5ec98b 7e5ec98b
js-claims-check      175de6ba     175de6ba   current   e9a21b44 e9a21b44
```

4 × `current` · 2 × `stale` · 0 × `drift`; all six paths porcelain-clean, tool
`held` at `75ed934d…` (`sha256sum`, vs the revision the round-10 receipts ran
under, `:1332-1344`). Both `stale` cells are their repos' committed HEAD blobs,
so T1 fired (`:1069-1090`): tsukuroi `084951be…` → `10452443…` (HEAD
`af8adf15` — the cell moved again since round 10's read of `c396662e…`;
recorded, not re-interpreted) and mado `d7edaab4…` → `93e43f8f…` (HEAD
`f7bfc9fe`). The re-pin rule leaves the recorded tables untouched; successor
rows land appended in the ledger (`:1230-1244`) — open at this write.

**Tool pulse** — same scratch, `--selftest` then `--regression`
(`REGRESSION_DATE 2026-10-14T21:32:40Z`):

- `--selftest` → `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0
  (`selftest.log`).
- `--regression` → six legs, all exact: `match=10/10` (legs 1–4, 6),
  `match=15/15` (leg 5), every leg `flips=0 inconclusive=0`; killed
  8/8/6/4/7/7; closing `REGRESSION: PASS (cases=6 passed=6; ledger legs
  exact: killed-delta<=0 flips<=0)`, rc 0; tool `75ed934d…` before and after
  (`regression.log`; workdir kept `/tmp/w11-t11-4-run/regression`).

The replay is drift-immune, re-verified at the close: legs 3–4 matched
byte-exact while their substrates read `stale` — the git-materialized blobs
ran, never the working trees (`:1324-1331`).

### Where to enter — four readers

- **The operator** (the seat the handoff names): `operator-runbook.md` §0; the
  cadence is its §6, and the round's schedule additions land with it
  (`plans/round-11.plan.md:80-103`). No lane declares a clock interval — the
  ticks so far are boundary-bound, and the interval is that seat's `[U]`.
- **A lane wanting a sweep**: the opt-in protocol for the request shape, then
  this page's recipe (`:131`) and its worked appendices A/B.
- **An auditor**: the ledger row → its case note → `--regression` at the
  recorded revisions; read the receipt block, not the last line (`:965-1008`).
- **The successor seat**: `service-standing-state.md`, then the ledger's
  unknowns and the runbook's §10.

### What stays open — named, never closed by prose

- **The interval** — the operator's `[U]` (above).
- **Whether any fleet driver invokes the tick with no lane acting** — round
  8's own `[U]` (`:1017-1019`), unchanged.
- **Whether the operator adopts the schedule** — `[U]`, recorded as such.
- **The two successor rows** (T1 fired again at this read) **and the ledger
  row for the six-leg registry** (`:1359-1363`) — open at this write.
- **The unknowns at their homes** — the ledger's U-list, the protocol's
  U1–U5, `service-limits.md` §5 — carried, not closed here.

Append-only to the last line: nothing above this section was edited by this
write; the recorded tables stand at their revisions, and a reader on a
differing revision re-resolves rather than trusts.

## Promotion-evidence calibration — fleet round-1

This lane's current checklist is `SHONEN.md`, not the historical training
closeout. Its supporting audit is `reports/round-1-calibration.md#box-1`.
Tameshi-dispatched reviewers remain part of tameshi for promotion authority
(`../PROTOCOL.md:63–68`); a different agent name does not justify `[x]`.
Lane assertions use `[~]` with durable evidence, not temporary logs.

Box 3 remains `[ ]`: `corpus/knowledge/executor-test-sufficiency.md:160–184`
establishes a historical single-JS-mutant exercise, not a current full cold-read.
The fresh CLI receipt in the audit verifies kill/survivor/restore behavior;
it is not a cold-reader exercise or an outside promotion/admission review.
The source audit rejects the broader claim rather than upgrading its confidence.
See `corpus/lessons/round-1.md` for the admitted correction and rejected claims.

## Repeated controls and gate registry — round 12

Source: S004/S026 and `corpus/knowledge/repeated-control-precondition.md`;
runtime evidence: `.ufo/evidence/round-12/verification-final.json`.
This is a standalone precondition check, not a change to the six-leg runner.

| Observation | Decision | Bound |
|---|---|---|
| Three or more zero-exit controls match on raw stdout and stderr | `controls_match` | Only this finite sample matched; not a determinism proof |
| Any available controls differ in exit or either stream | `controls_mismatch` | Do not attribute a later red suite solely to the mutant |
| Equal nonzero controls, or command unavailable | Could not evaluate baseline | No mutation kill-rate claim |

Recipe: choose a pristine command; put evidence outside any tree it inspects;
run `python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-UNIQUE -- COMMAND ARG...`;
retain raw observations before interpreting the finding. The output directory
must not exist. Caller owns timeout policy; hanging commands yield no verdict.
Do not retry until green, normalize output, or interpret a finite match as proof
of reliability. Command stdout/stderr may contain sensitive data: choose a
non-secret fixture command before retaining evidence.

### Gate/probe registry

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| repeated pristine controls | gate | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` or `--snapshot DIR` | 0 clean; 1 failed; 2 and 64 could-not-evaluate | `python3 tools/repeat-control.py --selftest` | `.ufo/evidence/round-12/ControlGate/expected.json`, `mismatch/expected.json`; literal expected IDs/exits in tool selftest | fresh caller-selected DIR; isolated `/tmp/tameshi-r12-*` selftest; snapshot read-only | tameshi |
| bash declared-witness study | probe | `python3 tools/bash-witness-study.py count` | 0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage/could-not-evaluate | `python3 tools/bash-witness-study.py selftest` | `.ufo/evidence/round-12/BashWitness/declaration.json`, `declared.tsv`, `manifest.json` | own evidence directory plus isolated `/tmp/tameshi-r12-*`; sibling object store read-only | tameshi |

Registry scope is these round-12 instruments; no new conformance assertion is
made about the historical runner. Witness declarations are integrity-frozen,
not blind: their author inherited prior source/spec exposure. The bash study
deepens one recorded case, never a seventh independently measured gate.

Calibration correction to the historical promotion paragraph above:
`SHONEN.md` box 3 currently carries a scope-bounded `[~]`, not `[ ]`;
`corpus/lessons/round-1-verifier-spotcheck.md` excludes it from the score.
Appending this registry does not extend the earlier Appendix A/B cold-read
to new material or establish full-page instruction sufficiency.