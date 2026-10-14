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
for both cases (Appendix A / Appendix B). An executor with no oral context can
run either case from this page alone.

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

## Mutation-sweep recipe — numbered, executable from this page alone

Runs a suite's own code through one-exact-edit mutants and measures what it
catches. Every step below is replayable by an agent with no other context; the
two worked cases (Appendix A JS, Appendix B bash) are the calibration.
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