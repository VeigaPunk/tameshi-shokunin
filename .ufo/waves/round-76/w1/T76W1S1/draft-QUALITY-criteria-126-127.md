### Criterion 126 — a kill rule is satisfiable by construction before any data is measured

A kill rule is a contract about the landed bytes, not a hope about them: it
must be possible to show, from the frozen fixture table and the mutants
named against it, that the rule can hold — before any battery runs. A rule
that is unsatisfiable by construction fails at design time, and discovering
that failure mid-round is a defect disclosure and an honest stop, never a
rule amendment after a seat has scored. Concretely: when a new arm and a
standing mutant touch the same shared rule (the arm asserts a property only
because the mutant's target code provides it), the collision is provable from
the frozen table — list the arms each mutant can fail, and check the named
arm appears and no other arm is forced to fire. The rule is then written with
its intrinsic collateral disclosed (each mutant's full kill set named in the
frozen matrix), so the battery measures a matrix that was already shown
consistent, and a mid-round amendment is never needed. A kill rule a critic
can refute from the plan's own table is a predicate-design defect: the claim
is judged on the original predicates, and the disclosure is the fix.

Lesson: `corpus/lessons/round-75-verifier-spotcheck.md` §6 item 1 (the
arm16↔m2 collision was provable from the frozen fixture table before any
battery ran; the original kill rule (ii) was amended after measurement showed
it failing, and C1 was judged failed-as-declared) and
`corpus/lessons/round-75.md` `## Mistakes` (the freeze-timing admission
defect) and `## Settlement errata`; the r75 wave critic T75W1C1 §4a proved the
collision intrinsic before the correction. Round 76's frozen kill matrix
(`plans/round-76.plan.md` R76-C1, with the r75 collateral kills disclosed as
unchanged) is the construction-time form: each mutant's full kill set is
named before data.

Falsifier that must fail: a critic derives, from the frozen plan's own arm
table and mutant edits alone, that the frozen kill rule cannot hold — e.g.
an arm whose assertion passes only because the mutant's edit keeps the
asserted code path live, forcing a collateral kill the rule forbids. In
round 75 the derivation was `m2-delimited-tautology` makes `delimited()`
unconditionally true, so any span-delimiting arm (arm16) must also fire under
m2, contradicting the original rule (ii) "killed by an arm other than the
one it is named against"; the falsifier fired and C1 failed as declared
(`.ufo/evidence/round-75/` T75W1C1 §4a, `l1-c1-battery.txt`). Under this
criterion the falsifier must NOT fire: the round-76 plan's frozen matrix
names m2 → arm13 + arm16 and span-rule → arm14 + arm17 + arm18 as disclosed
collateral, so no derivation from the frozen table contradicts the rule.

### Criterion 127 — a claim's counter tuples are frozen in the plan before data, not after a scored counterexample

A claim whose counter is a population of rows — (capability, figure regex,
instrument path, pinned rev, argv, expect) tuples — freezes those tuples in
the plan, before any seat has data or scores. The manifest or table the
instrument measures is then checked against the frozen tuples byte-wise, and
a manifest that differs from the frozen table is not the counter: a
population defined after a scored counterexample cannot certify the claim,
because the counter moved in response to the attack. The freeze is what makes
the do-nothing control meaningful: the before-state must read red on exactly
the frozen population, and the after-state green on exactly the same rows.
Any change to the population mid-round — a laxer regex, a foreign
instrument, a dropped row — is itself a scored event: disclosed as an
admission defect, never relabelled pre-data.

Lesson: `corpus/lessons/round-75-verifier-spotcheck.md` §6 item 2 and
`## 2. Per-claim re-check` R75-C2 (Correction 2's tuple freeze was the right
fix and the landed manifest passes it, but a post-score counter change cannot
certify the claim's counter; the target `rows=17 match=16 stale=1
unexpected=0` never changed and the landed bytes satisfy every kill rule) and
`corpus/lessons/round-75.md` `## Settlement errata` (the "pre-data" wording
too broad; both corrections are named admission defects); the critic's scored
counterexample (control 4, the loose-token manifest printing the full
after-state at base with zero repairs) is the measurement that forced the
freeze. Round 76's plan freezes the C2 population's three new tuples in a
table that "IS the counter" (the reviewer seat diffs the landed manifest's
three rows against it byte-wise) and discloses its named gaps as not-rows.

Falsifier that must fail: a manifest printed after a scored counterexample —
one whose live-row regex is a token common to doc and instrument but not the
figure (the verdict prefix, or a shared literal) — prints the full expected
after-state at base with zero repairs, so the counter certifies no work. In
round 75 the falsifier fired: the loose-token manifest read
`SELFSTATE: rows=17 match=16 stale=1 unexpected=0` exit 0 at base
(`.ufo/evidence/round-75/controls-c75b.txt`, wave critic T75W1C1), which is
why Correction 2 froze the population to the committed prototype's tuples.
Under this criterion the falsifier must NOT fire: the round-76 plan's frozen
tuple table is the only population the counter may claim, and the two new
capability tuples pin `\d+/\d+` figures unique in the instruments' stdout
(the plan's token-uniqueness pre-check: pin-disposition exactly one match
`19/19`; evidence-disposition exactly one, `66/66`), so no loose-token
manifest satisfies the frozen tuples.
