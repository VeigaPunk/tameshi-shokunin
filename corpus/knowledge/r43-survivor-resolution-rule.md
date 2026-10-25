# Survivor resolution — a pre-declared rule for mutants a battery does not kill

source: S089 (held, re-opened), S159 (new); S155 (held), S158 (held)

Round 43, tameshi L1. This entry states the rule the lane applies when a
declared mutant survives its kill battery, and the two fixtures that resolve the
round-42 survivors under it. It does not claim that any mutant is equivalent:
the lane never decides equivalence by assertion, only by the three verdicts the
rule defines.

## Why a rule is needed

A mutation score is only comparable when each survivor has a named outcome.
Both vendors say the tool cannot make that call:

- Stryker, on the equivalent-mutant page (held S089, re-opened 2026-10-25):
  "It is called equivalent mutant. There is no definitive way for Stryker to
  find and ignore them." — located at line 16 of this round's snapshot
  `.ufo/evidence/round-43/sources/stryker-equivalent-mutants.html`
  (38687 B, sha256 `79f6501a`; byte-identical to S089's 2026-10-22 anchor). The
  page's example is a branch guarded by `10 ** 0 = 1`, where `>=`, `<=`, `>` and
  `<` all produce the same output — the tool cannot see that, so it reports a
  survivor.
- Wikipedia (new S159, opened 2026-10-25): "Equivalent mutants detection is one
  of the biggest obstacles to practical usage of mutation testing." (line 796,
  `<p id="mw-w">`), and "The resulting program is behaviorally equivalent to the
  original one. Such mutants are called equivalent mutants." (line 794,
  `<p id="mw-Q">`). Both sit in the `Mutation testing overview` section — this
  revision has no equivalent-mutant section of its own, and the page carries no
  survivor vocabulary: it uses no "survivor", "unkilled" or "unreachable" text,
  and its behavioural definition does not separate a dead-code survivor from an
  equivalent mutant. That separation is this lane's rule, not the page's.

PIT's `DetectionStatus` (held S158) answers differently: it declares the class
`EQUIVALENT(true)` — "Mutation is equivalent to the un-mutated code. Treated as
detected although by definition it cannot be." (line 71–72 of the committed
snapshot; the enum constant is line 75) — so a vendor that knows the class
scores it as detected while stating that no test can reach it. That is a
reporting convention, not a detection: no producer of the status was traced in
this round's snapshot (the enum file alone), and the same enum keeps the other
separation: a run that exits non-zero is `RUN_ERROR` / `MEMORY_ERROR` /
`TIMED_OUT`, never `KILLED`. A lane that counted a crashed run as a kill would
inflate its score; a lane that counted every survivor as a defect would
overstate its coverage; a lane that silently scored a dead-code survivor as
detected would borrow PIT's convention for a class PIT itself says cannot be
demonstrated. The rule below is the lane's answer to all three.

## The rule (K/D/E/U)

Applied in order to each survivor of the frozen mutant set:

| Verdict | Condition | What it means for the score |
|---|---|---|
| **K — killed** | The round's battery produces at least one FAIL under the exit-plus-FAIL oracle: the tool exits 0 with parseable output and a case differs from its declared classification. The killing fixture must contain no runtime-unreachable statement, so the kill rests on reachable code. | counted as a kill |
| **D — dead_code_only** | The mutant survives K, and every case on which it differs from the pristine tool is a fixture whose source contains a statement after an unconditional `return`/`raise` in the same block. | a named survivor class, **not** a kill, **not** equivalence |
| **E — equivalent** | The mutant differs from the pristine tool on no case in the declared corpus. | a named survivor class; reserved, not reached in round 43 |
| **U — unresolved** | Anything else: `not_killed` (a reachable-input survivor), `runtime_error` (non-zero exit, traceback or unparseable output), `apply_error` (the declared edit does not apply exactly once). | does not count toward resolution |

Two consequences follow, and both are load-bearing:

1. **A survivor is never relabelled.** D and E are named classes with their own
   evidence; dropping a survivor from the declared set is not a verdict under
   this rule.
2. **A dead-code fixture is a legitimate case for an analyzer, but not a kill.**
   A static analyzer's contract is about source text, so a fixture whose
   discriminating construct is unreachable is still a valid assertion about the
   tool — and the lane still refuses to count it as a kill, because no runtime
   path reaches the construct that distinguishes the mutant.

## The two round-42 survivors, resolved

The declared set is `.ufo/evidence/round-42/census/mutants.json` (six mutants,
classes `attr`, `method`, `outflag`), unchanged. Round 42's own predicate
`C2_R42_PASS` stays false — that record is not re-adjudicated here.

| Mutant | Round-42 outcome | Round-43 verdict | Evidence |
|---|---|---|---|
| `outflag_no_parse_args_check` (`if flag and _parse_args_ns(...)` → `if flag:`) | survived (4/6) | **K** — `F11_outflag_namespace` | The fixture binds `options = SimpleNamespace(out='golden')` and passes `Path(options.out)` to a writer. The tool's documented rule is that an output-flag destination counts only when the base is a `parse_args` namespace; the mutant drops that check and reports `explicit_out=1` where the tool reports `0`. Reachable code: no statement follows a `return`. |
| `method_fold_several_returns` (`if len(returns) != 1:` → `if len(returns) < 1:`) | survived (4/6) | **D** — `F12_method_two_returns` | A method whose body has two top-level returns: the first is `os.path.join('tmp', 'expected.json')`, the second `os.path.join('golden', 'expected.json')`. Pristine refuses to fold a multi-return method (resolved text `self.destination()`); the mutant folds the first return (`tmp/expected.json`). The second top-level return is unreachable, so this is the only discriminating input class — hence D, not K. |

`F12`'s construction is deliberate: since `method_return` reads only the
method's direct body children, any method with two of them has an unreachable
second `return`. There is no reachable-input fixture for this mutation, and the
rule says so instead of manufacturing one.

## What this does not claim

- Not that `method_fold_several_returns` is equivalent. It differs from the
  tool (D, not E); the difference is on unreachable input.
- Not that the surface is covered. The killing fixture exercises one shape (a
  `SimpleNamespace` carrying an output-flag dest name). Attribute writes,
  `default=`/`set_defaults`, sub-parsers and the rest of the false-negative list
  in `r42-attribute-and-outflag-destinations.md` stay outside it.
- Not a universal kill rate. Six declared mutants, five kills, one named
  survivor; the numbers describe this set at this revision.
- Not a rival of the vendors' vocabularies. The K/D/E/U rule is the lane's own
  reporting convention for its artifacts; S155/S158 supply the outcome
  vocabulary it borrows (a run error is not a kill, a no-coverage candidate is
  not a survivor). The lane deliberately does **not** adopt S158's
  `EQUIVALENT(true)` scoring: it keeps E as a named survivor class with no kill
  credit, because the lane has no detector for it and PIT's convention assumes
  a human decided the class.
- Not Wikipedia's taxonomy. S159 defines equivalence behaviourally and has no
  survivor classes; the page is cited for the definition and for the obstacle
  claim only.
