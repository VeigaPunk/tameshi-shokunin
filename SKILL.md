---
name: tameshi-shokunin
description: "Verification-fixture craft for 'hermetic suites', 'mutation testing', and 'gate fixtures'. Anti-trigger: product behavior or endpoint health; route those to the product lane or kama. Rank: shonen."
---

# tameshi-shokunin

verification-fixture craft playbook. Rounds 1–3 built the corpus from measured
surfaces; every rule below earns a cited source. The first two mutation cases
— round 2 JS, round 3 bash, both 8/10 killed — are worked here (seven recorded since round 16; eight since round 18), and this page carries
the method as an executable recipe: numbered steps from pin to restore proof,
defect templates with exact-string guidance, kill-rate bands, restore
discipline, the measured bash-vs-JS divergences, and complete reproduce specs
for both cases (Appendix A / Appendix B). Historical cold-read proof: fleet round 1 re-ran all 10+10
Appendix A/B mutants (`.ufo/evidence/kaika-round-1/coldread/`); round 16 adds a full-page cold-read (Errata — round 16).

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
| **Live gate** (default mode) | what the current substrate state is | the live host/tree, read-only | measured counts on the verdict line; exit lattice 0/1/2 (kagi folds usage/setup into 2; 64 is kumitate's hermetic usage code) | gates-survey-kagi.md:24-31, 75-88 |
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
catches. The recipe is intended to be self-contained; round 16's full-page
cold-read executed it end to end (two seats; Errata — round 16).
Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).

1. **Pick the target and prove its control.** Prove the actual run has no
   live-path or host effects; `--selftest` alone does not establish hermeticity.
   Use private `--root` fixtures and exclude or control host-gated branches
   (mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:24-38).
   Require a reported case count, executed/skipped accounting, and verdict:
   kumitate `n/m pass` + `VERDICT:` (gates-survey-kumitate.md:19-31);
   kagi `SELFTEST: PASS (n cases)` includes its enumerated skip entries.
   Historical controls on the pinned bytes were green:
   `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit0
   (mutation-case-kimi-census.md:20-21), and bash16 enumerated cases,
   14 executed +2 skipped (mutation-case-kagi-census.md:27-35,42-43).
   A red control has no kill denominator: stop and record setup failure.
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
   mutation-case-kagi-census.md:44-47). Require `new != old` in future drivers:
   a no-op is a driver defect, not a survivor. The cited historical notes do
   not establish that particular round-2 guard. Any count ≠1 aborts until the string
   is re-derived from the pinned bytes.
6. **Run control + mutants.** Control first: run the unmutated copy, record
   stdout, exit code, summary line, duration — expect the step-1 green. Then per
   defect, one at a time: fresh copy from pristine → apply the one exact
   replacement (`str.replace(old, new, 1)`) → assert mutant sha256 ≠ pristine
   sha256 → run the suite with a timeout (300 s used in round 2, 280 s in round
   3). For future runs retain full streams plus exit, mutant SHA, duration
   and summary, then aggregate the rows. Historical Kimi records stdout,
   exit/SHA/results (mutation-case-kimi-census.md:26-28); Kagi also records
   duration/summary (mutation-case-kagi-census.md:48-49). No defect compounds;
   a mutant file is never patched or reused.
7. **Adjudicate each run against the suite's own verdict.** Green = exit 0 AND
   the verdict line says PASS with the full count.
   - **Killed** = the run went red (exit ≠ 0 or the PASS verdict/line broken)
     *and* the full enumerated count remains, with skipped cases distinguished.
     Both historical sweeps held their enumerated denominators43 and16
     (mutation-case-kimi-census.md:30-33; mutation-case-kagi-census.md:27-35,50-53).
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

Cost profile to record: wall time, per-run timeout, host/runtime versions.
Round2:7.0s for11 runs, nodev24.21.0 (mutation-case-kimi-census.md:20-21,29-31);
round3:11.0s for11 runs against a280s bound
(mutation-case-kagi-census.md:50-53). Cross-host stability remains unknown:
Kimi U5 at204-205; Kagi U5 at203-204.

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
   — a two-space substring also occurs once and yields the byte-identical mutant;
   the full line keeps `count == 1` robust when nearby code moves.
3. **One behavior per edit; minimal edit wins.** A defect that changes two
   mechanisms cannot be read for which class the suite saw
   (mutation-case-kimi-census.md:22-25).
4. **Literal replacement, never regex.** Use `str.replace(old, new, 1)` (both
   drivers). Code carries regex metacharacters — `(mode & m.modeFloor)`,
   `${n}`, `slice(0, 6)`, `[[ "$got" -ge "$floor" ]]` appear in the manifests
   (`${n}` in Appendix A's D4 below; the other three in
   mutation-case-kimi-census.md:156-166 / mutation-case-kagi-census.md:218-236); a regex substitution silently
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
  die on 16 cases each, 14 shared (mutation-case-kimi-census.md:74-76); mutants pay
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

## Restore discipline — before/after identity, not continuous non-write proof

All edits must stay in scratch. Before/after fingerprints establish endpoint
identity, not that no transient write occurred. Apply this policy in order:

1. **Before the sweep:** sha256 (full), size, mtime, repo revision, and
   `git status --porcelain -- <path>` empty — recorded in the note's header
   (mutation-case-kimi-census.md:13-16; mutation-case-kagi-census.md:13-17).
2. **All edits in scratch:** `cp -p` the artifact into the lane namespace and
   edit only copies (mutation-case-kimi-census.md:4-7;
   mutation-case-kagi-census.md:44-45).
3. **After the sweep:** require endpoint fingerprints to agree; historical
   Kimi recorded hash83016d45…4f426,43273B, unchanged mtime and path cleanliness
   (mutation-case-kimi-census.md:34-35); no after-repo revision was recorded.
   Kagi recorded hash275d8294…53009f,44212B, unchanged09:47:15 mtime,
   clean path and `cmp`-identical scratch copy (mutation-case-kagi-census.md:54-56).
   Its after-repo revision is likewise not established by those records.
4. **A drift is an incident:** stop, report it as one, do not "repair" by
   rewriting — a repair would itself be an unauthorized write.
5. **Never restore via `git checkout`/`git restore`.** Those write to the
   substrate; the only correct end state is *never-modified*. (I)
6. **Retain durable evidence.** The historical probes reran from scratch
   (`SCORECARD.md:13`), but the case-note commands rely on an unversioned
   `mutate_driver.py` and do not directly rebuild after scratch loss.
   Use the maintained `bash tools/mutate-and-run.sh --regression` ledger
   replay for those pinned cases; it does not recover the old driver.
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
- **Kill width is structural, not quality.** (I) Most bash fixture checks
  use an exit/token pair; some assert multiple tokens and two verb cases are
  host-gated skips. JS uses filesystem fixtures/subprocesses, DRIFT prefix
  checks and an exact CLEAN assertion; broad predicates affect many cases
  (mutation-case-kimi-census.md:82-89; mutation-case-kagi-census.md:27-35,171-175).
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
  shapes. (I) two independent source lanes measured → the two-lane method bar
  holds for these shapes (PROVINCE.md:15-16); this is not independent executor
  replication. Band interiors remain unprobed (mutation-case-kagi-census.md:58-60);
  verb-path U2 and host-stability U5 remain open (:193-206).

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
| **POLICY** — refused before the effect | the act would leak/overstep: non-regular or `op://`-carrying op-side paths; claim rows outside a 5-verb allowlist (quote-stripped before matching; 23 denied verbs); nested self-audit; stamp-set shrink without `--prune`; checklist rows naming `op.env`; hashing a no-hash path | refused before exec: exit 2 structural, except `drift-pins.sh`, which prints the POLICY line and returns its DRIFT verdict, exit 1 (`drift-pins.sh:142-148`, `:252-258`; round 17) | gates-survey-kagi.md:107-138 |
| **Zero-work** | the gate would report over nothing | refused; a gate that measures nothing must not exit 0 | gates-survey-kagi.md:139-143 |
| **Deferral** | substrate absent for a `[substrate]`-tagged row | `DEFER … reason=substrate-absent`, counted, not executed, never FAIL; guards: tag lives in the data file, both-paths selftest | gates-survey-kagi.md:187-197 |

Rules:

- **Declare arms as tokens and prove coverage — or say it is unproven.** Proxy
  12/12 arms fired; claims 5/5; kimi-census 1 token, 3 cases; round-gate 7
  declared / 6 fired (`INTERNAL_ERROR` uncovered); surface-probe and cite-check
  have no token enum: each asserts one CLI `--src` exit-2 arm, the rest of their
  exit-2 paths have no arm accounting (gates-survey-kumitate.md:287-292).
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
   is a fresh byte copy; the original is never a write target unless `--workdir` is its own directory (keep scratch apart).
2. **Spec parse + uniqueness.** Every `@old` must occur exactly once (non-overlapping count), asserted
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
- restore proof `MUTATE_RESTORE: OK` (sha before = after; the tool emits no
  separate tree-clean check — round-18 correction);
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
pinned original revision. Four legs at that revision (r7-1; seven since round 16; eight since round 18) — `js-kimi-census`
(r2, killed 8/10 = 80 %), `bash-surface-census` (r3, 8/10 = 80 %),
`bash-tsukuroi-census` (r5, 6/10 = 60 %), `bash-mado-verify` (r6, 4/10 = 40 %)
— each with its recorded kill-rate as its expectation
(`tools/mutate-and-run.sh@9f1d3c3:72-109`, `:511-522`; at round 18 the recorded tables sit at `:597-620`). The ledger
is the receipt tameshi's records cite for kill-rate claims; the standing per-gate rate rows
are `corpus/knowledge/fleet-kill-rate-ledger.md` (eight rows since its round-18 block).

### Using the ledger

- **One command replays every leg.** `bash tools/mutate-and-run.sh
  --regression [--workdir DIR] [--keep]` allocates a fresh default scratch
  `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
  it is removed on PASS unless `--keep`, retained on FAIL/SETUP; caller workdirs
  are never removed. Pre-allocation SETUP has no root to retain. Exits0/1/2:
  PASS/FAIL/SETUP (`tools/mutate-and-run.sh:126-136,1273-1294,1364-1384`).
- **Each leg's bytes come from the repo's git object store, not the working
  tree.** `git show <rev>:<path>` materializes the pinned blob into the case
  workdir and validates mode/SHA (`tools/mutate-and-run.sh:1104-1175`);
  `REGRESSION_PIN` names repo/rev/path/pin (:1159-1160). Working-tree drift
  does not change that blob. The old tsukuroi/mado pins are historical,
  not a statement that their current trees match those recorded bytes.
  A missing repo/rev/blob or pin mismatch refuses before that leg's suite;
  later legs still run and their statuses aggregate (:1314-1374).
- **Every kill-rate claim carries the receipt.** Cite `REGRESSION: PASS
  (cases=N passed=N; …)` (N=4 at r7-1, 7 since round 16, 8 since round 18) with the
  executed tool sha (`REGRESSION_TOOL`) and the per-leg pins
  (`REGRESSION_PIN`) — the receipt is tied to the tool revision that ran and
  to each leg's pinned bytes.
- **Contribution contract — what a leg carries.** A pinned target path,
  Git revision and SHA; one-edit defects with unique `@old` and `@new != @old`;
  a command exercising `$MUTANT` under controlled fixtures; enumerated,
  executed and skipped counts distinguished; and the exact recorded verdict
  table. Host-gated branches must be excluded/controlled or explicitly named,
  not called hermetic merely because the flag is `--selftest`.
  Current anchors: pins/revisions/tables `tools/mutate-and-run.sh:597-620`,
  first-four specs :648-829, inventory :82-100, eight dispatches :1314-1356.
  (U) The recorded case set remains tameshi-carried; no fleet-contributed
  leg is established by this registry.

### Reading a receipt — the discipline

1. **Read the block, not the last line.** `REGRESSION_TOOL` ·
   `REGRESSION_DATE` · `REGRESSION_BAND` · `REGRESSION_EXPECT` · one
   `REGRESSION_PIN` per leg · per leg one `REGRESSION_SWEEP` +
   `REGRESSION_TABLE` + `REGRESSION_CASE` · `REGRESSION_DEFECT` rows for
   differences · `REGRESSION_WORKDIR` · the closing `REGRESSION:
   PASS|FAIL|SETUP` line.
2. **PASS is exact for ledger legs.** Every case line `PASS (band:
   killed-delta<=0 flips<=0 inconclusive=0 defects=D)` and every
   `REGRESSION_TABLE … match=D/D … flips=0`; the closing line's
   `cases=N passed=N` (D is 15 for checklist-run, 10 for other current legs; N=8 since round 18). Measured instance (T7-1, 2026-10-14; replayed by this
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
  on a report file and ticks 450 s (round 8: `scripts/shokunin-watchdog.sh:3-5` at fleet `17c1fad`); its lane map
  then did not name tameshi (`:14`); since `5efb4114` (2026-10-19) the lanes live in `shokunin.conf`, which names tameshi
  (round 17). Tameshi's tick is still its own round series [I].
- **Per case, two readings:** the target's relation to each repo's branch-tip bytes
  (`current` / `stale` / `drift`; `<branch>` = the `branch=` field of
  `../scripts/hyaku/jj-lane.sh state <repo>` (git config `lane.branch` first, else function `detect_branch()`; cite by name, line anchors into the helper move)) and the tool's relation to the last run (`held` / `moved`):

| Reading | Rule | What it means |
|---|---|---|
| `current` | `tip=$(git rev-parse --verify --quiet --end-of-options "refs/heads/<branch>^{commit}")`; `git show <tip>:<path>` sha256 == the recorded pin (unresolvable `<branch>` → SETUP rc 2; path absent at the tip → the equality fails) | the swept bytes are the repo's branch-tip blob — never a jj working-copy `HEAD` (`@-`), which no remote has (round 17) |
| `stale` | the recorded revision is an ancestor of `refs/heads/<branch>` and the branch-tip blob differs | the gate moved past the recorded revision; the table's revision is historical, the table is not wrong |
| `drift` | the live file's sha ≠ the `refs/heads/<branch>` blob's, or `git status --porcelain -- <path>` is non-empty (a clean porcelain is not tip evidence: jj's exported working-copy commit `HEAD` can hold the bytes) | uncommitted/unpushed bytes; a reading for ledger hygiene — round 7's `git show <rev>:<path>` replay is already immune to it |
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
  instances at round 8 (2026-10-14): tsukuroi `084951be…` (6/10) → `bba6cdf6…`; mado
  `d7edaab4…` (4/10) → `90d50cdd…` (both have moved again since; re-read, never carry).
- **T2 — the harness sha ≠ the revision a case's table was measured under** →
  re-run the reproduction under the new revision and record both pins. Precedent
  (corrected round 18): round 16's RerunSweep under runner `0673d2e5…` reproduced case 7;
  mado under `b56c6e57…` was never re-cut (U, `mutation-case-mado-verify.md:17-23`); the harness itself moved four times in
  one day (`597e1419…` → `b56c6e57…` → `4dc69ef9…` → `e3f838d4…` → `cf41efaa…`)
  and no recorded table was re-interpreted for it.
- **T3 — an owner lane records a re-run at a new revision** → an appended row;
  §1–§4 are never edited (`fleet-kill-rate-ledger.md:170-173`).
- **The re-pin rule.** A moved pin is never re-interpreted against the new bytes
  (:811-812). The old table stays; the moved case lands at its newest revision
  with both shas and the delta, appended. `moved=0 stale=0` is a complete
  outcome, recorded as such — drift is never manufactured by re-cutting cases.
  The round-8 replay receipt (tool `cf41efaa…`, four legs; 19:15:54Z, rc 0):
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

Re-read three minutes later (**20:03:34Z**, same scratch): both moving cells now
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
adjudicate them. (Anchors `:…` are this page; `PROVINCE.md` is repo-relative; other bare note names are under `corpus/knowledge/`.) The
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
| e | Credential material / endpoint health | out of province — report, never absorb | `PROVINCE.md:14-18`, `PROVINCE.md:20` |
| f | Product semantics — whether a gate's verdicts are right | never measured — sensitivity ≠ truth | `:879-881`; `fleet-kill-rate-ledger.md:156-158` |
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
  this revision" (`:925-929`; dated there since round 16) and the round-9 receipt's `cases=4`
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
| `corpus/knowledge/mutation-case-*.md` (six at round 11; seven since round 16; eight since round 18) | per-case spec, verdict table, survivor probes, reproduce sections | re-deriving a recorded rate |
| `tools/mutate-and-run.sh` | the instrument: `--selftest`, `--regression` (six-leg registry at round 11, seven since round 16, eight since round 18; git-materialized replay) | any sweep or replay |
| `corpus/README.md` | the coverage map — one row per note, holds + sources | checking what the corpus holds |
| `plans/round-N.plan.md`, `plans/round-N-record-draft.md` | each round's plan and record by convention (rounds 4–10); no separate round-11 record file exists (the wave deliverables are the record, `LOG.md:316-317`; closeout note `corpus/knowledge/closeout-r11.md`); the completion pack (`plans/completion-evidence.md`, this wave, uncommitted at this write) collects the per-round lines and debts | auditing a round's receipts |
| `LOG.md`, `SCORECARD.md` | the round rows and the move-log rows with their counting commands | provenance of any round |

### Boundary readings, executed by this lane

Two executions, nothing else measured here; scratch `/tmp/w11-t11-4-ev/` (gone — round-18 correction: replay the tool at `606716f`, sha256 `75ed934d…`; round-18 wave 2 reproduced `80/80` and `cases=6 passed=6` there, `.ufo/waves/round-18/w2/CR30.md`).

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
  cadence is its §6; the round-11 schedule additions landed in `corpus/knowledge/closeout-r11.md:155-213`,
  not in the runbook (planned at `plans/round-11.plan.md:80-103`). No lane declares a clock interval — the
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

Box 3 was `[ ]` at this write (`[~]` since; Errata — round 16): `executor-test-sufficiency.md:160–184`
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
`SHONEN.md` box 3 carried a scope-bounded `[~]` at round 12, not `[ ]`;
`corpus/lessons/round-1-verifier-spotcheck.md` excludes it from the score.
Appending this registry does not extend the earlier Appendix A/B cold-read
to new material or establish full-page instruction sufficiency.

## Pin disposition and provenance correction — round 13

Sources: S003 and PIT precision correction S047 (historical S041 retained);
`corpus/knowledge/incremental-pin-disposition.md`; outside routed
`corpus/lessons/round-12-verifier-spotcheck.md`, Routed defects item 3;
runtime receipts in `.ufo/evidence/round-13/`.

| Observation | Decision | Limit |
|---|---|---|
| Recorded target bytes equal the current worktree | Report `unchanged` content | Mode, dependencies, environment, runner/spec and invocation identity remain unmeasured |
| Readable verified pin differs from current bytes | Report `changed` content | Re-pin a future owner-opted-in sweep; never transfer an old rate |
| Repo, commit, path or pin cannot be evaluated | Report `unavailable`, with reason | Never silently borrow the enclosing fleet repo or label it unchanged |
| All three content identities agree | Keep `result_reuse=not_established` | A content probe is not an incremental verdict cache or mutation re-sweep |
| Frozen summary kind is null but its top-level declaration is explicit | Retain original bytes and add checked normalized companion | Preserve the exact non-blind kind and exposure disclosure; no retroactive preregistration |

Recipe from this lane root:

1. Read the source-backed scope and `not_compared` list before the result.
2. `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`
   observes only hashes and git metadata. Retain stdout with its sibling branch-tip
   commits before treating it as a dated reading. It executes no sibling gate.
3. `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json`
   checks the new companion against digest-anchored frozen sources.
4. The original round-12 summary and rerun summary retain their historical
   null fields. The companion normalizes the canonical summary only; the
   rerun null is explicitly outside its normalized scope. The producer's
   wrong-nesting bug is fixed separately for future summary generation;
   its regression selftest asserts the exact top-level exposed kind.
5. Do not rerun a sibling's gate to obtain closure evidence. A non-author
   closure verifies committed receipts and their measured revision.

### Round-13 gate/probe registry

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| six-leg content disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed | `python3 tools/pin-disposition.py --selftest` | `.ufo/evidence/round-13/pin-manifest.json`; canonical leg mapping and literal selftest labels in tool | normal mode read-only lane/sibling files and git; selftest isolated temp repos only | tameshi |
| exposed witness provenance companion | gate | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 metadata_consistent/clean; 1 metadata_inconsistent/failed; 2 input_unavailable or snapshot_tampered/could-not-evaluate, including usage | `python3 tools/witness-metadata.py --selftest` | literal frozen input digests and expected kind/disclosure in tool; companion expected verdict; `.ufo/evidence/round-13/expected.json` | check read-only lane inputs; selftest isolated temp trees only | tameshi |

No registry row changes rank, SHONEN authority, or the six recorded cases.
The historical summary's producer SHA names the producer that actually ran,
not the repaired current producer. No old evidence hash is regenerated.
PIT source clarification: S048 supersedes S047's object-specific
paraphrase; retain only the supported distinction “item 4 is
prioritisation, not a reuse skip”. No test-versus-mutation pronoun claim
is needed by this method.

## Effective expectation reconciliation — round 14

Sources: `corpus/lessons/round-13-verifier-spotcheck.md`, Routed defects1–3;
S049 (Python child-environment contract), S003 Limitations, and
`corpus/knowledge/incremental-pin-disposition.md`, empirical correction8.
These instructions add no full-page cold-read or independent promotion credit.

| Evidence condition | Decision | Error pattern / limit |
|---|---|---|
| Expected exit agrees but the intended assertion is absent | Failed expectation, not mechanism proof | A FileNotFoundError before the assertion is a setup failure |
| A stale expected row is replaced by later evidence | Keep its raw observation and explicitly supersede the row | Both named oracle replacements must themselves be effective and pass; never silently drop a row |
| Snapshot input or receipt bytes differ from their pinned digest | Could-not-evaluate | Do not reinterpret an edited receipt as a new historical verdict |
| A new context experiment explicitly records its child override | Read only that new experiment's outcome | Documentation or output equality cannot recover an omitted historical environment |
| A content probe agrees under one GIT_DIR injection | Bounded scrub observation | Not general hermeticity, safe result reuse, target execution or a fresh mutation rate |

Recipe, from this lane root:
1. Read the historical expectations and raw observations before accepting a
   later summary; distinguish twelve expected rows from thirteen pinned inputs.
2. **Historical (round 14, runner `75ed934d…`):** at `--root .` both manifests now return 2
   `expected_input_digest_mismatch` (the runner moved in round 16). Replay with cwd = an extracted
   `git archive 28aeef4` tree: `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json`
   → 1, failing the unresolved producer_before assertion (a matching exit 1 alone is insufficient).
3. The same command with `dispositions.json` → 0: the only repair is that row's explicit supersession,
   keeping raw receipt/check and both passing replacements. Live-tree form: the round-17 re-pin section (round-18 manifests since then).
4. `.ufo/evidence/round-14/verification-final.json` retains the corrected
   selftest and frozen before/after outcomes; `verification.json` retains the
   initial18-of34 fixture failures rather than disguising them as green.
   The revision measured is recorded separately.
   A non-author closure reads committed evidence, never executes sibling gates.
5. **Archived experiment, not an entry point:** the round14
   `capture-context.py` produced the retained context receipt and must not be
   run again because its historical output path replaces that frozen receipt.
   Use the maintained retained-only gate in the round15 registry below.

### Round-14 historical registry — superseded by round 15

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| effective expectation disposition | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` (historical; live entry since round 18: `.ufo/evidence/round-18/dispositions.json`; round 17's now exits 2, bash-witness moved) | 0 clean; 1 failed semantic expectations; 2 could-not-evaluate invalid/missing/tampered inputs; 64 usage | `python3 tools/evidence-disposition.py --selftest` | `.ufo/evidence/round-14/dispositions.json` and before counterpart pin historical expected/receipts; historical expected pins13 original inputs; literal isolated selftest expectations in tool | normal mode read-only lane evidence, stdout only; selftest isolated temporary fixtures | tameshi |
| archived invocation context capture | historical gate, not active | do not run; retained source `.ufo/evidence/round-14/capture-context.py` only | historical outcomes retained, not an active verdict map | historical helper-only controls do not satisfy the standalone gate selftest | unchanged round13 pin manifest and context receipt | archive bytes read-only; no supported invocation | tameshi |

The disposition manifest is configured authority, not cryptographic proof of
author authenticity. Receipt replay proves its recorded predicates, not that
every historical command was independently re-executed. Unmapped receipt-only
checks do not acquire new expected rows by being mentioned in a summary.

## Context gate classification and explicit exit classes — round 15

Sources: S051 (maintained retained-context gate, opened this round),
S049 (explicit child invocation), `corpus/lessons/round-15.md` (Gate and
Mistakes), and `corpus/lessons/round-14-verifier-spotcheck.md`, Routed
defects item 5; `../PROTOCOL.md` §Gate standard. This appendix corrects the
active registry classification and exit classes. Effective runtime evidence is
`.ufo/evidence/round-15/verification-3.json`; the two earlier failed harness
receipts remain retained history, not green evidence or outside admission.
It adds no successor sweep, seventh recorded case, promotion credit,
outside-admission authority, author authentication, new live-capture
capability or environment-independence claim.

**Classification correction.** The round-14 instrument
`.ufo/evidence/round-14/capture-context.py` compares the pin probe's two
documents (only top-level `observed_at` excluded), an exact environment delta
and a positive git control, persists probe/runner source digests against the
round-13 `expected.json` and `pin-manifest.json`, and checks the runner's six
leg mappings; `decide()` returns `ok`/exit0 or `mismatch`/exit1
(`:2-31`, `:553-580`, `:605-643`). Verdict behavior over persisted
expectations is a **gate** under §Gate standard, not a probe. The round-14
registry history is retained above with an inline archive marker, not a callable entry.

**Archive status.** That historical script is **archived, not active**: its
bytes stay at sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`,
it is not an entry point, the maintained gate never invokes it, and its noarg
prospective-capture guidance is superseded. This supersedes round-14 recipe
step 5 and the historical registry row above; both are now marked archive-only.
The maintained
gate is `tools/context-capture.py`; the active use is retained-receipt replay,
not a new live experiment. Round-14 receipts are read-only inputs, never
regenerated.

**Retained-check semantics.** The maintained command replays a retained
receipt against an expected pin—built in for the frozen clean receipt,
caller-supplied through `--receipt`/`--expected` otherwise—checks the required
structure, and re-derives each predicate from the stored raw fields. The
receipt is data: check mode never executes retained argv, never opens a
recorded root path and never reruns the git or probe experiment. It must not
trust the receipt's stored summary booleans or stored `status`/`exit`/`reasons`:
absent, wrongly typed, duplicate-key or contradicting fields are findings,
never a clean pass. The negative retained fixture
`.ufo/evidence/round-14/context-missing-env.json` (sha256
`1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`) is
the discriminating counterpart: passed with a caller-committed expected pin
(schema `tameshi-context-expected-v1`) naming `missing_injected_environment`
and exit1, it must fail at exit1; the clean retained receipt (sha256
`05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`) is the
exit0 counterpart and the tool's built-in frozen default. Selftest inputs are
synthetic fixtures, distinct from these retained files.

| Evidence condition | Decision | Limit |
|---|---|---|
| Retained receipt digest matches the pinned expectation and every required raw predicate and structure agrees | `clean`, exit0 | Proves only the retained receipt's recorded and re-derived facts under its declared scope; never that stored argv was re-executed |
| A re-derived predicate, source digest, control or mapping disagrees | `failed`, exit1 with the stable finding ID (the missing-environment case keeps `missing_injected_environment`) | A named predicate failure; never relabel it a probe observation, a retry-until-green, or a substantive environment finding |
| Missing, unreadable, wrongly typed, duplicate-key or non-UTF-8 input; edited frozen snapshot; unavailable setup | Could not evaluate, exit2 with a stable kind, no traceback as a verdict | No compared verdict from absent or edited bytes; an edited snapshot is integrity failure, not semantic mismatch |
| Usage error or an undeclared nonzero code | Could not evaluate, exit64 for usage, no receipt written | Usage is lane vocabulary mapped to could-not-evaluate, not a failed experiment |
| Historical round-14 receipt interpreted | Bounded observation of one declared `GIT_DIR` injection and six static mappings | No leg or suite execution, result reuse, concurrent sibling stability, global environment independence, or retrospective repair of round-13's undocumented setup |

**Exit classes.** Both active gates share three classes over four exit codes: `0` clean,
`1` failed, `2` and `64` could-not-evaluate (`2` invalid, unavailable or
tampered input/setup; `64` usage, no receipt); an undeclared nonzero code also
reads as could-not-evaluate. This corrects the disposition row's former
`64 usage` wording and the context row's former probe label and absence of 64;
it changes no historical command outcome, the round-14 admission, or the C1
scalar.

### Round-15 gate/probe registry

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| retained invocation-context gate | gate | `python3 tools/context-capture.py --check` (frozen round-14 clean receipt); `--check --receipt FILE --expected FILE` for a caller-pinned retained receipt | 0 clean (`context_consistent`); 1 failed stable finding ID (e.g. `missing_injected_environment`); 2 and 64 could-not-evaluate (receipt/expected missing, malformed or tampered, e.g. `snapshot_tampered`; 64 `usage_error`) | `python3 tools/context-capture.py --selftest` | frozen clean receipt `.ufo/evidence/round-14/context-receipt.json` sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` and its built-in id/exit pin in tool; expected-pin schema `tameshi-context-expected-v1` (`receipt_sha256`/`id`/`exit`) for other retained receipts; negative fixture `context-missing-env.json` sha256 `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`; literal selftest exit/finding pairs in tool | check reads receipt/expected bytes and its own source for a reported digest, writes nothing, never opens recorded root paths or executes stored argv; selftest writes isolated temporary fixtures only; archived round-14 bytes retained | tameshi |
| effective expectation disposition | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` (**superseded in round 17**: since round 16 this command returns 2 `expected_input_digest_mismatch` at `--root .` because the runner input moved; the 0-clean outcome is restored only by re-pinning, not by relabelling. Live entry: `--dispositions .ufo/evidence/round-18/dispositions.json` → 0 (round 17's now 2), see the round-17 re-pin section; frozen replay: cwd = extracted `git archive 28aeef4` → 0) | 0 clean; 1 failed semantic expectations; 2 and 64 could-not-evaluate (invalid, missing or tampered inputs; 64 usage) | `python3 tools/evidence-disposition.py --selftest` | `.ufo/evidence/round-14/dispositions.json` and before counterpart pin historical expected/receipts; historical expected pins13 original inputs; literal isolated selftest expectations in tool | normal mode read-only lane evidence, stdout only; selftest isolated temporary fixtures | tameshi |

The maintained gate's expected values are configured authority, not
cryptographic proof of author authenticity; a clean check replays recorded
predicates and pinned digest binding, never a re-execution of stored argv and
never a fresh measurement. Selftest green is capability only; the frozen
retained replay is the committed-input evidence of the Gate standard's "Two
evidences", and neither is an outside-admission sample. No row here changes
rank, SHONEN authority, the six recorded cases, or the archived round-12–14
bytes; no sibling gate is registered or executed by this lane, and no
successor sweep or seventh case is claimed.

Explicit mode reads caller-selected files with caller permissions; use only
non-secret receipt and expected JSON. Paths can follow filesystem symlinks:
digest binding verifies the bytes read, not filesystem-origin authenticity
or a race-free confinement boundary. Selftest reads its own source for the
reported tool digest, not live domain artifacts. Pre-integration wave1
capture/root-override recipes are superseded by this retained-only cutover;
they are advisory planning, never public capture-capability evidence.

Could-not-evaluate takes precedence over a mismatched expected verdict: an
edited snapshot or unavailable input stays exit2, with any expectation
disagreement secondary. A clean result with a wrong id/exit pin becomes
failed/exit1. Help exits0 only as a non-verdict informational mode; context-capture's selftest
exits0/1/2 for pass/case failure/setup inability and64 for invalid invocation (the disposition selftest: 0 pass, 1 case failure or an uncaught setup traceback; round 17).

## Errata — round 16 full-page cold-read

Round 16 cold-read every section of this page (snapshot sha256
`97cf436b…3580`, 51 buckets = preamble + 50 headings outside code fences)
with 30 cold-read seats (CR01–CR27, three of them with a/b replicas); reports
`.ufo/waves/round-16/w1/CR*.md`, re-reads `w2/RR*.md` and `w3/RX*.md`, ledger
`.ufo/evidence/round-16/coldread/ledger.json` (assembled from those reports by
`coldread/assemble.py`; it holds the merged verdict and gap counts per bucket).
The page edits are in-place repairs, and so are this table's own cells: a
later row's corrections of an earlier row stay visible in git
(`git log -p -- SKILL.md`), not as appended rows. Wrong expectations were repaired
in place with the line count of every edited section unchanged (except `### Round-15 gate/probe registry`, +1 blank separator; see the round-17 section), so every
`SKILL.md:<line>` self-anchor still resolves; the old wording stays in git
(`git show e69b488:SKILL.md`, sha256 `97cf436b…`; also
`.ufo/evidence/round-16/coldread/SKILL.snapshot.md`). Repairs:

| Snapshot line | Was | Now | Found by |
|---|---|---|---|
| 15 | cold-read proof covers one JS mutant only; sufficiency unverified | points here | CRCritic1 |
| 134-135 | observed cold-read proof covers one historical JS mutant | round 16 executed the recipe end to end (CR04a, CR04b) | CRCritic1 |
| 63 | live gate "exit lattice 0/1/2 (usage 64)" | kagi folds usage/setup into 2; 64 is kumitate's hermetic usage code (`claim-ledger.sh --bogus-flag` → 2, `claims-check.mjs --bogus-flag` → 64) | CR02 |
| 271-272 | a two-space substring "produces a *different mutant*" | it yields the byte-identical mutant; the full line keeps `count == 1` robust | CR05 |
| 278-280 | `${n}` said to appear in the two notes' manifests | `${n}` is in Appendix A's D4 on this page; the notes carry the other three tokens | CR05 |
| 360-361 | D1/D3 "die on the same 16 cases" | 16 cases each, 14 shared | CR06 |
| 505 | 22 denied verbs | 23 (`claim-ledger.sh:164`) | CR10 |
| 513-515 | surface-probe and cite-check exit-2 paths "uncovered" | each asserts one CLI `--src` exit-2 arm; no arm accounting beyond it | CR10 |
| 925 | "Four legs at this revision" | dated: four at r7-1, seven since round 16 | CR16 |
| 949-950 | receipt literal `cases=4` | `cases=N`, N per revision | CR16 |
| 1390, 1393 | mutation-case notes "(six)"; round-11 record "lands" in `plans/` | dated count; no separate round-11 record file exists (the wave deliverables are the record) | CR23, RR08 (w2) |
| 1472 | "Box 3 remains `[ ]`" | dated: `[ ]` at that write, `[~]` since | CRCritic1, CRCritic2 |
| 1614 | `PROTOCOL.md` §Gate standard | `../PROTOCOL.md` (fleet root; the lane holds none) | CR27 |
| 3, 9-10 | unquoted frontmatter `description:` (strict YAML rejects the second `: `); "Two mutation cases are now measured" | quoted; the first two cases are worked here, seven recorded since round 16 | RR01 (w2) |
| 1346 | quotes "Four legs at this revision" at `:925-929` | notes that line 925 is dated since round 16 | WholePage (w2) |
| 1391 | "six-leg registry" | six at round 11, seven since round 16 | RR08, RR11 (w2) |
| round-15 registry, disposition row | `--root .` said to exit 0 | since round 16 the runner input moved: `--root .` → 2 `expected_input_digest_mismatch` by design; run with `--root` at an extracted `git archive 28aeef4`, from the lane root → 0 | RR10 (w2) |
| round-16 registry, assemble row | "64 usage" | argparse usage exits 2 | RR13 (w2) |

Minor gaps (non-blocking; named in the seat reports, counted in the ledger): dead `/tmp`
evidence paths in records of rounds 6–9; anchors written as tool sha256 values
rather than git revisions (`cf41efaa…`, `597e1419…`); Appendix B survivor-probe
fixture contents are not spelled out (seats rebuilt them from the gate's
header schema); `git status --porcelain` on a sibling may take its index lock —
prefer `git --no-optional-locks -C <repo> status --porcelain`; round-7 section
`tools/mutate-and-run.sh:<line>` anchors predate later growth of the tool
(CR16, RR07); nested check [51] of round-gate's selftest records itself as a
skip-as-pass (`round-gate.mjs:1381-1382`).

## Seventh recorded case and full-page cold-read — round 16

**The seventh case.** kumitate `scripts/round-gate.mjs` at rev `364f1d5`
(blob sha256 `f890e277…a834d3e9`, 60-case hermetic `--selftest`) against 10
single-edit mutants → **5/10 killed (50 %)**, control green, 0 inconclusive,
`MUTATE_RESTORE: OK`; every one of the 10 predictions, committed in `e69b488`
before the sweep, held. Detail of record:
`corpus/knowledge/mutation-case-kumitate-round-gate.md`. The case is ledger leg
`js-round-gate` (`tools/mutate-and-run.sh --regression` → `cases=7` at round 16; `cases=8` since round 18).

Reproduce it (read-only on kumitate; scratch in `/tmp`):

```sh
W=$(mktemp -d /tmp/tameshi-r16-rg.XXXXXX)
git -C ~/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > "$W/round-gate.mjs"
sha256sum "$W/round-gate.mjs"   # f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
E=.ufo/evidence/round-16/round-gate
bash tools/mutate-and-run.sh --target "$W/round-gate.mjs" --defects "$E/round-gate.defects.spec" \
  --suite "$(cat "$E/suite.txt")" --label js-round-gate --workdir "$W/work"
# expect: CONTROL: GREEN ... MUTATE: DONE (... killed=5 survived=5 inconclusive=0 kill-rate=50%)
```

Rules this case adds:

- **Scrub the environment of a suite that shells out to git.** round-gate's
  fixtures run `git` with the inherited environment: an exported `GIT_DIR`
  makes the pristine control commit into that repository, and a `TMPDIR`
  inside a work tree turns the control red. Run the suite under `env -i` with
  its own `HOME` and `TMPDIR` (the string in `suite.txt`); the ledger leg
  carries the same string. This scrubs; it does not confine: a hostile mutant
  can still write outside its directory or reach the network (GuardAudit,
  round 16) — use `bwrap` when mutants are untrusted.
- **Grade by exit, not by stdout bytes**, when the suite prints `mkdtemp`
  names: three pristine runs differ byte-for-byte yet exit 0 every time, so a
  repeated-control byte comparison reports `controls_mismatch` (exit 1) for a
  deterministic verdict. `tools/mutate-and-run.sh` grades on exit only.
- **Test a projected interval at its edge.** The round-4 projection said any
  `REPORT_MIN_BYTES` in [26, 1059] keeps every fixture verdict; the mutant at
  1059 survived and the one at 1060 was killed by the 1059-byte fixture. A
  midpoint edit would not have tested the bound.
- **Show each survivor is not equivalent off-suite** before calling it a gap:
  run the survivor-probe harness (`$E/survivor-probes/probes.mjs`, probe ids in
  the case note) on the pristine copy (exit 0) and on the mutant (exit 1).

**The full-page cold-read.** Every bucket of this page was read by a seat
that saw only the page and what it names; instructions were executed in
`/tmp`, records re-anchored. The errata section above lists what it found and
repaired; repaired and new sections were re-read by fresh seats (wave 2, then a residual check). The counting
command: `python3 .ufo/evidence/round-16/measure.py --rev REV` (field
`coldread.box3_full_page`). Lane seats are the lane: this earns the box-3
lane assertion (`[~]`), never an independent `[x]`.

### Round-16 gate/probe registry

| Name | Kind | Command | Exits |
|---|---|---|---|
| `tools/mutate-and-run.sh` | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage |
| `.ufo/evidence/round-16/measure.py` | probe | `python3 .ufo/evidence/round-16/measure.py --rev REV` · `--selftest` | 0 measured · 2 rev/blob missing · 64 usage |
| `.ufo/evidence/round-16/coldread/assemble.py` | gate | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 every bucket covered (a rejected report is printed, not counted) · 1 a bucket uncovered · 2 usage (argparse), an invalid override or a heading mismatch (round 17) |
| `.ufo/evidence/round-16/attribution/reattribute.py` | probe | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 corrected rule passes the oracle · 1 it fails |
## Live-tree re-pin and entry-command monitor — round 17

Sources: `corpus/lessons/round-16-verifier-spotcheck.md` §3 and §6 (routed
R16-OP1, R16-MON1); S062 (`git rev-parse --show-toplevel`), S063 (git
repository discovery and `GIT_*` environment), S061 (jj leaves Git `HEAD`
detached at `@-`). This section restores the round-14 capability's live
verdict and adds the monitor that would have caught its loss. It claims no
new mutation case and no promotion credit.

| Evidence condition | Decision | Error pattern / limit |
|---|---|---|
| A lane instrument pinned by historical `expected.json` moved by a committed change | Append a v2 manifest whose `historical_inputs` reads that path's pinned bytes from a 40-hex ancestor commit | Waive only paths that moved: a waiver of an unchanged file exits 2 `historical_input_unneeded`; evidence paths can never be waived (`historical_input_forbidden`) |
| A waived path's live bytes differ from `<anchor>:<path>` (round 18: the branch tip `refs/heads/<lane.branch>`, not `HEAD`) | Could not evaluate, exit 2 `historical_input_uncommitted` | A worktree edit is tampering, not a by-design move |
| The waiver rev is a tree id, dangling, not an ancestor, shallow, or reached through replace refs, grafts or an inherited `GIT_DIR` | Could not evaluate, exit 2 | The pinned sha256 still guards content; these guard provenance |
| A registered command's outcome changes after an instrument edit | Re-pin or supersede in the same round; sweep every mention | "By design" names the mechanism; it never excuses the outcome |
| A registry row stops holding its admitted outcome | `registry-check.py` reports `differs`, exit 1 | A row leaves `active` only as `superseded` with `superseded_by`, and still runs |
| A tool or fixture runs git while the caller exported `GIT_DIR`/`GIT_WORK_TREE` | Every lane tool scrubs `GIT_*` before git (round 18 adds `bash-witness-study.py`; historical `.ufo/evidence/round-16/measure.py` still does not — run it only through `registry-check`, which scrubs) | Unscrubbed fixture commits moved this lane's HEAD and index in round 17 |
| A repo path has no `.git` of its own inside a git super-repo | Runner regression leg: SETUP `repo_identity_mismatch`, exit 2 | Without the guard git silently answers from the parent repo's objects |

Recipe, from this lane root (round-13/14 evidence bytes stay immutable):

1. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` (round 18; round 17's two now exit 2)
   → 1 `failed`, the `producer_before` expectation unresolved (`"expectation": "producer_before"`).
2. The same command with `.ufo/evidence/round-18/dispositions.json` → 0 `clean`,
   `"effective": 11`, `"superseded": 1`; text mode prints one `HISTORICAL <path> rev=<rev> sha256=<sha>` line per waived instrument.
3. `python3 tools/registry-check.py --rev <40-hex lane commit>` replays every row of
   `tools/registry.json` in a scratch clone (siblings symlinked beside it) and ends with
   `REGISTRY_CHECK: held=N/M superseded=K`. Grade an older rev with `--registry <current registry file>`.
   Run it with `--rev`, never on the live tree: some rows write receipts into their root.
4. Read a sibling's or this lane's committed bytes at the branch tip `refs/heads/<branch>`
   (`tools/pin-disposition.py` head rows carry `branch` and `head_differs_from_branch`), never at `HEAD`.

### Round-17 gate/probe registry — re-pin and monitor

| Name | Kind | Command | Exits |
|---|---|---|---|
| `tools/evidence-disposition.py` (v2 manifests) | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` (round 18; the round-17 manifest now exits 2) · `--selftest` | 0 clean · 1 failed expectations · 2 could not evaluate (invalid, missing, tampered or unprovenanced input) · 64 usage |
| `tools/registry-check.py` | gate | `python3 tools/registry-check.py --rev REV [--registry PATH] [--tag TAG] [--json]` · `--selftest` | 0 every active row held · 1 a row differs · 2 registry invalid, rev unresolvable or clone failed · 64 usage |
| `tools/mutate-and-run.sh` (guard + scrub) | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | as the round-16 row; a borrowed repo identity is SETUP 2 |
| `tools/pin-disposition.py` (branch tip) | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` · `--selftest` | as the round-13 row |

## Input-keyed cold-read credit — round 17

Sources: `corpus/lessons/round-16-verifier-spotcheck.md` §2 and §6 (routed
R16-C2b, R16-C2c); S058 (verifying traces: rebuild when a recorded dependency
hash differs), S059 and S064 (a cache hit is sound only for inputs in its key),
S060 (strace sees files opened by name). Knowledge:
`corpus/knowledge/input-keyed-coldread-credit.md`.

**Correction of round 16.** The round-16 full-page assertion (section above,
"Every bucket of this page was read…") was wrong at `09ee1d0` on one bucket:
`## Effective expectation reconciliation — round 14` kept a sha-only credit
while the runner it executes against moved, and its recipe then exited 2. The
errata section's "line count of every edited section unchanged" also missed one
section: `### Round-15 gate/probe registry` grew from 30 to 31 lines. Both
statements stay as written; this paragraph supersedes them.

| Evidence condition | Decision | Error pattern / limit |
|---|---|---|
| A ledger entry's recorded input still has its sha256 as a regular blob at the measured rev | Input verified | Inputs are lane paths; sibling and git-object reads are recorded as external and never credited |
| Any recorded input drifted, vanished, or is a tree/symlink | The entry does not credit (`input-drift:`, `input-missing:`, `input-not-blob:`) | A section whose bytes did not change still loses credit |
| An entry has no inputs, or executed commands without committed trace receipts | No credit (`inputs-unrecorded`, `traces-unrecorded`, `trace-missing:`) | Applies to `record` and `instruction` entries alike |
| A failing entry for the bucket still has verified inputs | Veto: the bucket is uncovered | One passing read never launders a failing one |
| A trace opened a file in the live lane while the root was a clone | No credit (`live-lane-read:`) unless the read is under `.git/` or its bytes equal the blob at the read rev (`measure.py` docstring) | Such a read was not of the recorded revision |

Recipe for one bucket, cold:

1. Clone the lane at a 40-hex commit into a fleet-mirror layout
   (`W=$(mktemp -d); mkdir $W/fleet`, symlink each sibling `*-shokunin` repo into
   `$W/fleet/`, `git clone -q <lane> $W/fleet/tameshi-shokunin`, `git -C … checkout -q --detach <rev>`).
2. Run every command the bucket names under
   `python3 tools/trace-inputs.py --root $W/fleet/tameshi-shokunin --out <receipt.json> -- <argv…>` (round 18; same CLI and receipt as the round-17 copy);
   the receipt lists the tracked files opened (`inputs`), untracked opens, and external fleet files.
3. Record the verdict block (schema `tameshi-coldread-report-v2`) with the receipts' inputs plus every lane
   file opened by hand, then `python3 .ufo/evidence/round-18/coldread/assemble.py --reports <dir> --carry <prior ledger> --out <ledger>`.
4. Commit the ledger and every receipt it names together, with no recorded input changed after the reads,
   then `python3 .ufo/evidence/round-19/coldread/measure.py --rev REV` → `coldread.box3_full_page` and `calibration_restraint_score` (current default ledger; earlier round-17/18 paths below remain historical evidence).
   A cited number uses no `--ledger-file`/`--ledger-rev`/`--inputs-overlay` (`overrides_used` false).

Limits: an open trace does not see environment variables, stat-only probes,
reads on inherited descriptors or network; a seat can still omit a command.
The rule makes a recorded read checkable, not complete.

### Round-17 gate/probe registry — input-keyed credit

| Name | Kind | Command | Exits |
|---|---|---|---|
| `.ufo/evidence/round-17/measure.py` | probe | `python3 .ufo/evidence/round-17/measure.py --rev REV` · `--selftest` | 0 measured (a missing default ledger is 0 with reason `no-ledger`) · 2 rev or required blob missing, an explicit `--ledger-file`/`--ledger-rev` unreadable, a forbidden overlay field · 64 usage |
| `.ufo/evidence/round-17/coldread/trace-inputs.py` | probe | `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --root DIR --out FILE -- ARGV…` · `--selftest` | 0 traced (the command's exit is in the receipt) · 2 strace unavailable or the command never executed · 64 usage; `--selftest` 0 pass, 1 a case failed — it fails under an outer tracer (nested ptrace is refused), so never wrap it |
| `.ufo/evidence/round-17/coldread/assemble.py` | gate | `python3 .ufo/evidence/round-17/coldread/assemble.py --reports DIR --out FILE [--expect-skill-sha SHA]` · `--selftest` | 0 every bucket covered, no report rejected · 1 a bucket uncovered, a report rejected, or no report found · 2 usage (argparse) |

## Eighth recorded case — round 18

kumitate `scripts/sources-check.mjs` at rev `0acb7752d19058b953ebbeba253b1e35f6548de5`
(blob sha256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`, 897 lines,
mode 100755) is ledger leg `js-sources-check`: 5/10 killed, 10/10 predictions held. The
spec and predictions were committed (`93d22aa`) before any mutant ran; the suite is the
hermetic `env -i` form of case 7 (`.ufo/evidence/round-18/sources-check/suite.txt`); eight
pristine controls were byte-identical (`.ufo/evidence/round-18/sources-check/control/`).
Entry: `corpus/knowledge/mutation-case-kumitate-sources-check.md`. Replay:
`bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-sources-check: PASS`,
`cases=8 passed=8`. Wave 2 probed all five survivors off-suite: four are non-equivalent, `S_KIND`
differs only in `--help` output (entry errata ER8-2).

| Survivor class in this case | What the suite does not pin | Fix belongs to |
|---|---|---|
| one-sided kind coverage (`S_KIND`) | observed kinds ⊆ declared kinds | kumitate |
| verdict-line text (`S_VERDICT`) | the final `SOURCES_CHECK: DRIFT (...)` line | kumitate |
| line attribution, counters (`S_DUP_LINE`, `S_ENTRY_COUNT`) | detail text and non-row counters | kumitate |
| per-entry read-failure kind (`S_FILE_READ`) | no fixture reaches the per-entry read-failure branch (the `READ_FAILED` fixture fails at the directory read) | kumitate |

### Round-18 gate/probe registry — routed-defect closure

| Name | Kind | Command | Exits / rule |
|---|---|---|---|
| `.ufo/evidence/round-18/defect-probes.py` | probe | `python3 .ufo/evidence/round-18/defect-probes.py --rev REV` · `--selftest` | 0 measured (`DEFECT_PROBES: open=N closed=M total=11`) · 2 a probe errored, a pristine selftest was red, or an anchor was not unique · 64 usage. A guard probe is `closed` only when the pristine selftest exits 0 and the guard-removal mutant exits nonzero; children run under bwrap with the fleet read-only; never wrap it in `tools/trace-inputs.py` (P05–P07 run that tool's selftest, and nested ptrace is refused → 2) |
| `tools/registry-check.py` (round 18) | gate | unchanged CLI | `timeout_s` must be a finite number in (0, 86400] (`NaN`/`Infinity` literals refused at parse; a larger finite value used to crash `communicate()` with exit 1) → 2 naming the row; descendants of a row (including ones that called `setsid`/`setpgid`) are killed at timeout and after the row exits, and pipe draining is bounded — limits: a descendant that changes UID may be unkillable, same-tick PID reuse is not excluded, and an orphan adopted from a pre-existing checker child can be signalled (`.ufo/waves/round-18/w2/SentinelKillCode.md`); survivors fail the row with `cleanup_error` |
| `tools/evidence-disposition.py` (round 18) | gate | unchanged CLI (`--selftest` now needs `jj` on PATH) | G2/G3 read one anchor commit: `refs/heads/<lane.branch or attached branch>`; a jj-colocated repo with detached HEAD and no `lane.branch` → 2; a detached non-jj clone (`registry-check --rev`) anchors on its checked-out commit only when a branch or remote-tracking ref contains it. HEAD is never read as the tip in a bound lane (jj leaves `HEAD` at `@-`) |
| `tools/bash-witness-study.py` (round 18) | probe | unchanged CLI | every git child drops all inherited `GIT_*` and pins `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`; its pinned round-13 bytes are read from `4acc607` through `.ufo/evidence/round-18/dispositions.json` (the round-17 manifests are superseded) |
| `tools/trace-inputs.py` | probe | `python3 tools/trace-inputs.py --root DIR --out FILE -- ARGV…` · `--selftest` | promoted current collector; the historical round-17 evidence copy remains unchanged, not byte-identical to the promoted tool. The promoted selftest discriminates removal of O_RDWR exclusion, private-cache anchoring and root-execve checks |
| `.ufo/evidence/round-18/measure.py`, `coldread/assemble.py` | probe, gate | as round 17, default ledger `.ufo/evidence/round-18/coldread/ledger.json`; `--carry` copies prior entries verbatim plus a `carried_from` key; `--explain` per bucket | input-keyed credit only: it binds credit to recorded inputs, not to the commands a bucket requires — never cite it as command coverage |
| `.ufo/evidence/round-19/measure.py` | gate with `--check`; otherwise measurement probe | `python3 .ufo/evidence/round-19/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --check` · `--selftest` | 0 all five frozen correction items hold; 1 open item; 2 cannot evaluate; 64 usage. Without `--check`, 0 reports a count, not acceptance. Public-CLI selftest uses inline synthetic snapshots plus four frozen package fixtures and literal expectations (`SOURCE_PINS` binds source-baseline/source-round18-final). `contract.json` describes the population; `before.json`/after receipts are measured outputs, not selftest inputs. No network/Git writes; selftest scratch only; owner tameshi. Metadata reconciliation, not producer authentication, cold-read or required-command coverage; QUALITY37–39, lessonround19, S049. |
| `.ufo/evidence/round-19/coldread/measure.py` | probe | `python3 .ufo/evidence/round-19/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV` · `--selftest` | Delegates unchanged credit/trace/veto/CLI rules to frozen round-18 `measure.py`, selecting round-19 `coldread/ledger.json` as default (no legacy overrides). Same exit map and input-keyed-only bound. Round-19 refreshed entries are L1-author source reads, not new blind or independent cold-read/command-coverage evidence; old entries retained verbatim. Inputs/receipt hashes are revision-pinned; external observations remain outside the credited-input predicate. Owner tameshi, read-only except inherited isolated selftest scratch. |

### Round-20 gate/probe registry — frozen receipt instruments

Source: `corpus/lessons/round-20.md`, QUALITY41, opened S049 for the
explicit child-environment boundary. Original stage files and older
receipts are historical evidence and remain byte-preserved. The active
round20 counting entry omits the inherited unsupported `--check` spelling;
the wrapper executes the unchanged frozen ruler and records its own digest
separately as `runner_sha256`.

| Name | Kind | Entry / self-invocation | Verdict map | Persisted values / scope / owner |
|---|---|---|---|---|
| `tools/receipt-window.py` | gate | `python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json`; self-invocation `python3 tools/receipt-window.py --selftest` | 0 clean; 1 failed; 2 could-not-evaluate; 64 usage/could-not-evaluate | `.ufo/evidence/round-20/contract.json` frozen/installed/historical identities, plus `public-cli-cases.json` independent synthetic expectations; read-only inputs, isolated selftest temp fixtures; owner tameshi |
| `tools/receipt-measure.py` | gate | `python3 tools/receipt-measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --json`; self-invocation `python3 tools/receipt-measure.py --selftest` | 0 clean (six predicates); 1 failed; 2 usage/could-not-evaluate | unchanged `.ufo/evidence/round-20/stage/measure.py`, frozen contract and committed revision inputs; wrapper selftest invokes public CLI over isolated Git fixtures with persisted six-item IDs/exits; no live-tree writes; owner tameshi |
| `.ufo/evidence/round-20/coldread/measure.py` | probe | `python3 .ufo/evidence/round-20/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --explain`; self-invocation `python3 .ufo/evidence/round-20/coldread/measure.py --selftest` | 0 observed; 2 could-not-evaluate; 64 usage/forbidden override (could-not-evaluate); selftest 0 clean/1 failed | selects the round20 ledger using the unchanged round18 credit algorithm; refuses ledger-file, ledger-rev and inputs-overlay flags, including abbreviations and equals forms, with SELECTOR_OVERRIDE_FORBIDDEN; L1-author input-keyed source re-anchoring is not recipe execution, independent/blind cold-read, or required-command coverage; isolated package selftests; owner tameshi |

Receipt-window recipe: freeze staged instrument digests before dispatch;
do not edit them in place; install only after original readers return;
record actual aware start/end times and instrument SHA beside the complete
observation. With changed frozen/installed identities use `edit_interval`
(not the inherited planning annotation `install_window`). The identity
case validates byte membership without imposing a freshness floor.
Historical identities are classified, not authenticated or re-executed.
The ruler hardcodes this round's six predicates: it is not a generic
contract-schema validator. `install_window` and `expectations` in the
inherited contract are descriptive, not enforced schema fields.

### Round-21 gate/probe registry — finite environment differential

Source: `corpus/lessons/round-21.md`, QUALITY43–44 and
`corpus/knowledge/hermetic-env-differential.md` (mined S079, reopened S028).
The frozen C1/C2 scripts and populations remain unchanged from33d03b7;
the maintained facade supplies public isolated fixture selftests without
rewriting those instruments. These are bounded measurements, not admission
or execution-authentication mechanisms.

| Name | Kind | Entry | Verdict map | Self-invocation | Persisted values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| `tools/env-diff.py` | probe | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/tameshi-f5.json` | 0 all surfaces classified; 1 incomplete/failed measurement; 2 could-not-evaluate; 64 usage | `python3 tools/env-diff.py --selftest` | frozen nine pins/seven profiles in `.ufo/evidence/round-21/c2-contract.json`; raw tuples in `.ufo/evidence/round-21/f5/receipt.json`; fixtures cover sensitivity, repeat variation and pin refusal | requested output and isolated `/tmp/tameshi-r21-envdiff.*`; sibling blobs read-only, no network | tameshi |
| `tools/wave-route-mix.py` | gate | `python3 tools/wave-route-mix.py --spec .ufo/waves/round-21/spec1.json --json` | 0 clean; 1 concentration/unrouted-role failure; 2 could-not-evaluate; 64 usage | `python3 tools/wave-route-mix.py --selftest` | max-share0.40 and literal synthetic expectations; round20 refused spec/round21 accepted spec retained | none; reads operator role routes, never edits routing | tameshi |
| `tools/round21-measure.py` | gate facade | `python3 tools/round21-measure.py --claim c1 --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --json` (use `--claim c2` for F5) | 0 clean; 1 failed population; 2 could-not-evaluate; 64 usage | `python3 tools/round21-measure.py --selftest` | delegates unchanged `c1-survivors.py`/`c2-count.py`; frozen mutant/population JSON; literal fixture exits and stable finding fields in facade | isolated fixture/private clones only; no lane Git writes | tameshi |
| `.ufo/evidence/round-21/coldread/measure.py` | probe | `python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --explain` | 0 observed; 2 could-not-evaluate; 64 usage/forbidden override; selftest0 clean/1 failed | `python3 .ufo/evidence/round-21/coldread/measure.py --selftest` | selects round21 ledger, unchanged round18 algorithm and round20 strict override refusal | isolated selftest/private reads only | tameshi |

C1's guard kills include child-environment/command-pin contracts and
synthetic process identities, not demonstrated malicious hooks or PID
reuse. C2's repeat comparison deliberately preserves random-path raw
output variation; nine classified does not mean nine deterministic
selftests or universal hermeticity. The frozen counter validates declared
pins/tuple arithmetic and a source header, not producer authenticity.
Current source re-anchors retain the199-entry prefix and label authorship;
they are not blind/independent cold-read or required-command coverage.

Round22 addition (same registry section; same-ground calibration repair):
`corpus/knowledge/callback-authoritative-accounting.md`, minedS082 and
QUALITY45. Partial reports, report prose and content verdicts do not supply
terminal seat status. Retained declared callbacks bind exact registered
name/agent/role; our own evidence does not authenticate provider telemetry.

| Name | Kind | Entry | Verdict map | Self-invocation | Persisted values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| `tools/wave-accounting.py` | gate | `python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/bundle.json --expected .ufo/evidence/round-22/expected.json --json` | 0 clean; 1 failed invariant; 2 malformed/unavailable/tampered input, could-not-evaluate; 64 usage, could-not-evaluate | `python3 tools/wave-accounting.py --selftest` | digest-pinned round22 bundle/expected.json, wrong-count bundle/expected pair; eight literal public-CLI rejection fixtures in frozen round22 measure.py | read-only input; isolated selftest temporary files only | tameshi |

The frozen round22 `measure.py` is this gate's original eight-fixture
counter/oracle, not an independent second green. Supplemental isolated
public-CLI fixtures cover16 further schema/accounting guards without
changing that frozen claim denominator. The wrong-count entry uses the
same gate with `wrong-count-bundle.json` and `wrong-count-expected.json`;
its persisted expected verdict is1/TOTAL_MISMATCH. Raw harness
`failed (exit N)` statuses were normalized to `failed` when projecting
the bundle; the gate deliberately consumes the normalized declared schema,
not arbitrary raw callback text. Normal `--help` exits0 as help, not a
measured accounting verdict.

Round23 addition (same registry section; same-ground calibration):
`corpus/knowledge/required-command-binding.md`, minedS083 and QUALITY46.
Source-read credit, including62/62, is not required-command coverage.
Freeze explicit requirement names/argv/expect before execution; match
new retained observations by name, exact argv, declared clone cwd/revision,
integer exit and all required stdout tokens. Preserve expected-red commands.

| Name | Kind | Entry | Verdict map | Self-invocation | Persisted values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| `tools/command-binding.py` | gate | `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` | 0 clean declaration binding; 1 mismatch; 2 invalid/unavailable/tampered, could-not-evaluate; 64 usage, could-not-evaluate | `python3 tools/command-binding.py --selftest` | expected digest pins complete bundle; public fixtures include `.ufo/evidence/round-23/extra-cases.json`; frozen ten-case counter `measure.py`; source-read bundle/expected pair is expected1/ARGV_MISMATCH | read-only input; isolated selftest scratch only | tameshi |

The evidence-only `round-23/replay.py` runs the frozen baseline registry
requirements in an isolated clone using the existing registry runner's
opt-in `retain_streams=True`; ordinary registry CLI output remains bounded.
It checks the requirements against the pinned source registry before running.
Invocation parameters and full decoded streams are newly retained unsigned
observations, not retrofilled historical fields or execution authentication.
The gate itself validates bundle-declared requirements; choosing another
trusted expected file chooses another contract, not a provider signature.
Ten synthetic rejection cases, the finite baseline registry replay and the
input-keyed source monitor are separate populations. Historical R17-CMD-BIND
full-page/ledger-consumer coverage remains open; no independent promotion.

Round23 correction (fresh falsification, appended; text above unchanged).
The replay above is not an isolated clone. Two external rows,
`pin-disposition-read` and `verify-round15`, read live fleet state, and the
clone symlinks live sibling repos. The result is 41 revision-pinned rows
plus 2 live-dependent rows. The instrument supplies receipt argv, cwd and
revision, so the replay verdict tests only exit and stdout. Argv
discrimination rests on the source-read pair and the synthetic cases. The
gate binds bundle-declared requirements; requirement freezing is the
replay instrument's pre-execution check (QUALITY47).

Round24 addition (same registry section; same-ground calibration):
`corpus/knowledge/replay-projection-hardening.md`, minedS084/S085, QUALITY48.
The round23 replay instrument stays unchanged; its successor tool refuses
to publish a binding bundle from a rejected, cleanup-failed or over-limit
runner row. It lists live-dependent rows, and it realpath-normalises fleet
identity.

| Name | Kind | Entry | Verdict map | Self-invocation | Persisted values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| `tools/registry-replay.py` | gate | `python3 tools/registry-replay.py --project OBS --out DIR --json`; `--run --repo LANE --rev REV --requirements FILE --registry-baseline FILE --out DIR`; `--plan --repo LANE --json` | 0 bundle published or plan printed; 1 refused (RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT); 2 invalid/unavailable input, could-not-evaluate; 64 usage, could-not-evaluate | `python3 tools/registry-replay.py --selftest` | literal fixtures in the tool; frozen requirement/registry digests come from the caller's files | writes only under `--out`; rows run in a private clone whose fleet mirror symlinks live siblings | tameshi |

Registry rows `command-binding-selftest-r24` (44/44), `command-binding-frozen-clean-pinned`
and `command-binding-source-read-red-pinned` supersede the three round23 rows
append-only. The two pinned rows also require their exact `bundle_sha256`.
Frozen ruler: `.ufo/evidence/round-24/measure.py` (eleven predicates).
Receipt argv, cwd and revision remain instrument-supplied, and no producer
authentication is claimed.

Round24 correction (fresh falsification; earlier text preserved).
The table's write-scope and exit-map cells are not reliable safety promises.
The replay creates temporary clones; row commands can reach live siblings;
Git hooks may run because the clone does not disable them. Writes are not
confined to `--out`. The stream limit bounds bundle publication only:
`observations.json` retains complete, unredacted streams before that check.
A refused projection does not clear an older bundle/expected pair in the
same output directory; that stale pair can still return clean from the gate.
Malformed observations may publish a bundle the consumer rejects, and
unavailable-input errors can escape as exit 1 rather than documented exit 2.
Use only caller-trusted local revision code and a fresh output directory;
neither the clone nor this gate is a sandbox or producer authentication.

The replay gate covers all 43 stored receipts, including both declared-live
rows. `revision_pinned=41` means not declared live, not self-contained:
`mutate-and-run-regression` and `round21-measure-selftest` additionally read
live sibling object stores. The 47-row current registry battery and the
43-row frozen replay are different populations. `registry-replay-selftest`
is the fourth new active registry row and expects 10/10; its tests exercise
projection and planning, not `--run`. Public command-binding fixtures include
both `.ufo/evidence/round-23/extra-cases.json` and the round24 counterpart.
The superseded 38/38 row still runs, fails against 44/44, and is excluded
from the active tally. Full limitations and evidence: `corpus/lessons/round-24.md`
Errata E–P and residual corrections; `corpus/knowledge/replay-projection-hardening.md`.
