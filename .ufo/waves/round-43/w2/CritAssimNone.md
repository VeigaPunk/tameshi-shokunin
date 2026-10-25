# CritAssimNone — round 43, wave 2: the `Assimilation: none` challenge

Seat: `L1Tameshi43.CritAssimNone` (critic, leaf, axis **coverage**). 2026-10-25.
Item: *"Challenge `Assimilation: none`. Read `/home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.md`
and name the single entry that would have served this round's claims better than the new knowledge entry,
or state that none would. Give the entry name, its theme, and one sentence on why the round's own entry
is or is not a better fit. Read-only."*

Read-only throughout. The assimilation package was read only; nothing was written, fetched, committed or
pushed there, no campaign tool was run, and the lane checkout, its Git index and its jj state were not
touched. My only write is this file. No counter was run at `c5335c70bff750218b3a6db0a92daae76509a0de`
or at any other revision (the item is a package-scope question, decidable from bytes), so no deciding
run was contaminated. No tool was installed.

---

## Verdict

**None would.** Of the package's 86 entries (85 files on disk, the 86th folded; `MERGE-REPORT.md:7`
and `:15-21`), no single entry would have served round 43's three claims better than the round's own
`corpus/knowledge/r43-survivor-resolution-rule.md`.

**Closest single candidate named as the item asks: `survivor-classification.md`**
(`MERGE-REPORT.md:34`, staged `S166`/`S156`), theme **F8/F1 — surviving-mutant classification: a
survivor is a candidate hole and becomes a hole only after it is classified into behaviourally
equivalent vs. behaviourally different** (`knowledge/corpus/knowledge/survivor-classification.md:31-33`;
package theme map `.ufo/waves/round-43/w1/ScoutAssim.md` §2, F1/F6/F9 row).

**One sentence on the comparison:** the round's own entry is the better fit, because
`survivor-classification.md` is refused on three still-live grounds — a drifted quote, a false recheck
predicate, and duplication of the held F8 entry `oracle-anchored-survivors.md` (`corpus/lessons/round-42.md:82-97`;
re-verified below) — and it carries neither a rule nor a fixture, while `r43-survivor-resolution-rule.md`
carries the K/D/E/U rule and both measured verdicts (F11 kill, F12 dead-code-only) for the unchanged
six-mutant set.

---

## 1. The candidate space, by claim

Each claim was matched against the whole package, not against the one entry the round's lesson happens
to name.

| Claim (axis) | Package candidate(s) | Theme | Package status at these bytes | Better fit than the round's own entry? |
|---|---|---|---|---|
| **C1 depth** — two round-42 survivors resolved under K/D/E/U | `survivor-classification.md` (`MERGE-REPORT.md:34`) | F8/F1 survivor classification (candidate hole → classified) | **REFUSED** r42, grounds unrepaired (`corpus/lessons/round-42.md:82-97`) | **No.** It states a doctrine ("a survivor is a candidate hole"), not a rule over a declared set, and holds no fixture. The round's entry's *thesis* subsumes it (`r43-survivor-resolution-rule.md:62-66`: "A survivor is never relabelled") and the lane already holds the F8 ground it duplicates (`oracle-anchored-survivors.md`). |
| C1 depth (runner-up) | `mutation-score-semantics-cjk.md` (`MERGE-REPORT.md:32`) | F1/F9 score denominator + equivalent-mutant class | **DEFERRED** r42, both gates admit; flip unmet (below) | **No.** It supplies denominator arithmetic for a *score*; C1's target has no score field (`contract.json:23`: `mutants_killed=5 dead_code_only=1 equivalent=0 unresolved=0`). It answers the round-44 question, not this one. |
| C1 depth (equivalence cluster) | `llm-mutant-equivalence-cost.md` (`:31`), `cjk-mutation-metric-and-tool-comparison.md` (`:36`) | F1/F9 equivalence rate; Chinese metric | both DEFERRED, same flip family | **No.** C1 explicitly declines equivalence (`contract.json:30`: E "reserved; not reached this round") — these entries argue *toward* the equivalence judgement the round refuses to make. |
| **C2 calibration** — seven record-agreement classes m6–m13 | **none** | — | — | **No candidate exists.** 0 of the 85 files match `scorecard|self-assessment|record.agreement|m1[0-3][ =]|census-valid|planned \(round` (§5 command 1). |
| **C3 operability** — staged-id guard before any append | **none** | — | — | **No candidate exists.** 2 of 85 files match `collision|renumber|staged.id|by-document`, and both are the host trash runtime's *name* collision (`r13-trash-refusal-root-cause.md:7`; `r15-landing-kit-dry-run.md:31`), not a registry-id collision. No entry discusses renumbering a staged id set. |

### Why the runner-up does not win either

`mutation-score-semantics-cjk.md` is the only candidate with gate verdicts already on record (both r42
gates said admit, `corpus/lessons/round-42.md:99-106`), so it is the strongest possible counterexample to
"none". It still loses for two independent reasons, both checkable at these bytes:

1. **Its ground is already held.** The entry's denominator thesis — killed ÷ non-equivalent, equivalent
   mutants excluded — is the held F1 ground in `corpus/knowledge/mutation-score-semantics.md` (the word
   `denominator` occurs 5× there, including the `detected/valid` vs `k/(k+s)` comparison). Adopting the
   staged file would add a second vocabulary over the same arithmetic, which is the round-42 deferral's
   own stated reason to wait for a *divergence* measurement.
2. **Its flip is not discharged.** `mutation-score-semantics-cjk.md:56` still points at
   `CANNOT-ANSWER.md` §3.7, which resolves nowhere in the landing repo and is *obsolete* where it does
   resolve (the package's own `cjk-mutation-metric-and-tool-comparison.md:2,20` cites a refereed 2024
   journal article that closes the gap). Re-verified in these bytes at §5. A round that adopted it
   as-is would import an unresolvable pointer — the same class of defect the round-42 Gate refused on
   the survivor entry.

So "admissible" is false for the refused entry, "not yet admissible" for the deferred ones, and
"not on the claim" for all of them.

---

## 2. The refusal is still live (the counterexample actually tested)

The strongest case *for* an entry serving C1 better is that `survivor-classification.md` is the
package's nearest text to the round's theme ("what a survivor is called"). I re-tested the three
refusal grounds against the package's current bytes rather than trusting the round-42 narration:

```
$ grep -nE 'recheck|とは|168 killed' \
    knowledge/corpus/knowledge/survivor-classification.md
5:recheck: 180d — re-run `curl -fsSL '...j-six-mutation-testing' | grep -c '168 killed'`
   (expect 1; ...)
13:  out of 183 mutants; "生き残ったミュータントがすべてテストの穴とは当たり
```

- Ground 1 (drifted quote) stands: the staged text still carries `とは当たり` where the page reads
  `とは限りません` (`corpus/lessons/round-42.md:85-88`).
- Ground 2 (false recheck) stands: the recheck cell still expects 1 (`grep -c '168 killed'` → 2 at the
  live page, per `corpus/lessons/round-42.md:89-91`).
- Ground 3 (duplication) stands: the lane's K/D/E/U rule now states the classification thesis itself
  (`r43-survivor-resolution-rule.md:62-66`), and the held F8 entry `oracle-anchored-survivors.md`
  already carries the oracle-anchoring half.

An entry whose three refusal grounds all survive cannot be the entry that "would have served better";
it could only have served at the cost of the round's own record discipline.

---

## 3. What the package *did* serve, without being adopted

This is the distinction the item turns on: `Assimilation: none` is an **adoption** statement, not a
**usage** statement, and the round says exactly that (`corpus/lessons/round-43.md:9-12`: "the package's
staged ids were examined read-only for the collision hazard, never adopted").

- The package's staged registry **is C3's measurement input**, not a candidate source:
  `contract.json:65` `"staged_input": ".../merge/tameshi/SOURCES.append.md (read-only; never written,
  never fetched)"`, and `guard/measure.py:6,56` binds `STAGED_REL` to the same path.
- The package's own post-append hazard (six id collisions, `S153`–`S158`) is the hazard C3's guard
  answers, and the guard's safe floor `S256` is derived from the staged set's extent
  (`corpus/lessons/round-43.md` Ids block; `MERGE-REPORT.md:114-124`).
- Bound worth stating so no one over-reads it: **C2 does not use the package.** m13's indented-row
  mirror is built inside the counter (`calibration/measure.py:25-31,177-181,329-338`), and the staged
  append contains **0** indented rows (`grep -cE '^ {0,3}\| S[0-9]{3} \|'` → 103, column-zero form →
  103). So the package served one claim (C3) as data and none as an adopted entry.

---

## 4. Impacted axes

| Axis | Impact |
|---|---|
| depth (C1) | None negative. The package's depth-adjacent entries are refused (survivor classification) or deferred on held ground (denominator); the round's own entry is the only one carrying the rule + both fixtures. |
| calibration (C2) | None. The package has no entry on record-vs-tree agreement; the claim is unaffected by the package either way. |
| operability (C3) | **Positive, unclaimed as assimilation.** The package is the guard's staged input; `Assimilation: none` correctly separates that use from adoption. |
| coverage (my axis) | All 86 entries accounted: 1 refused (survivor-classification), 3 deferred in the same cluster, 82 off-claim or same-ground. |

---

## 5. Evidence (commands; all read-only, run from the stated roots)

From `/home/vgpnk/Projects/shokuknow/merge/tameshi` (package, never written):

```
grep -rilE 'scorecard|self-assessment|record.agreement|m1[0-3][ =]|census-valid|planned \(round' \
  knowledge amendments | wc -l                                        → 0        (C2: no entry)
grep -rilE 'collision|renumber|staged.id|by-document' knowledge amendments
  → r13-trash-refusal-root-cause.md, r15-landing-kit-dry-run.md       (C3: 2 hits, both trash name collision)
ls knowledge/corpus/knowledge/*.md amendments/corpus/knowledge/*.md | wc -l → 85  (86 entries, 1 folded)
grep -ciE 'dead.?code|unreachable' knowledge/corpus/knowledge/mutation-score-semantics-cjk.md → 0
  (the deferred denominator entry cannot speak to C1's D class)
grep -cE '^ {0,3}\| S[0-9]{3} \|' SOURCES.append.md → 103 ; column-zero form → 103 ; indented → 0
sed -n '54,58p' knowledge/corpus/knowledge/mutation-score-semantics-cjk.md
  → "the gap is recorded in `CANNOT-ANSWER.md` §3.7" (pointer still live in the entry)
```

From `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (lane, read-only):

```
grep -nE 'proposed knowledge entries' MERGE-REPORT.md → :7 (86 entries)
grep -nE 'survivor-classification|mutation-score-semantics-cjk' MERGE-REPORT.md → :34, :32
grep -n 'denominator' corpus/knowledge/mutation-score-semantics.md | wc -l → 5   (ground already held)
grep -niE 'denominator' corpus/knowledge/r43-survivor-resolution-rule.md → 0 matches
  (the round's entry does not claim the denominator; it therefore does not need the deferred entry)
sed -n '2134,2142p' LOG.md → round-41 same-ground refusal class, cited as the precedent
```

---

## 6. Smallest safe correction

**To the decision: none.** `Assimilation: none` survives the strongest available counterexample
(`survivor-classification.md`) on three live refusal grounds, and survives the second
(`mutation-score-semantics-cjk.md`) on held ground plus an unmet flip and a target that has no field
for it. Do not adopt an entry this round; the round's own entry remains the correct one.

**To the record (optional, already reported elsewhere):** `corpus/lessons/round-43.md:64-71` names
only `mutation-score-semantics-cjk.md` where the package carries four equivalent-mutant entries
(`survivor-classification.md`, `mutation-score-semantics-cjk.md`, `llm-mutant-equivalence-cost.md`,
`cjk-mutation-metric-and-tool-comparison.md`). That is a *thinner* deferral, not a wrong decision — it
omits candidates, so it cannot make "none" false — and wave-1 seat `ScribeLessonGate` already scored it
as D5 (`.ufo/waves/round-43/w1/ScribeLessonGate.md:192`). No further action from this seat.

---

## 7. What I did not establish

- I did not re-open any deferred entry's sources; adoption admissibility here rests on the recorded r42
  verdicts plus the two byte-level checks above (drifted quote, dead pointer), both re-verified in the
  package's own files.
- I ran no campaign counter. The item is a scope question over 86 stored entries; the absence results
  in §5 are exhaustive over the files on disk (85 files = 86 entries), not a sample.
- I did not measure whether adopting any entry *alongside* the round's entry would have helped; the
  round's entry budget and theme slot are one document, and both candidate replacements would displace
  the rule that C1's target measures.
