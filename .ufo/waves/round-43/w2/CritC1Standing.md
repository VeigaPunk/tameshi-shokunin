# CritC1Standing — is 5+1 a legitimate close of the routed survivors? (C1, depth)

Seat `L1Tameshi43.CritC1Standing`. Item: judge the C1 verdict as a closure reader would —
does `dead_code_only` close the routed defect or merely re-label it; is F12 a fixture a
reasonable reviewer would accept as the basis for a named survivor class; and does the
round-42 `C2_R42_PASS=false` record stay honest under this round's rule.

Lane state while this seat ran: HEAD moved `e20cf89 → b510ad1 (A11) → e25cd2f → 6b83a11
(A14)`; every claim below names the bytes it refers to. All runs at `--rev 3aee2c0…`
(permitted freeze-of-record rev) or `487b8f0…` (base); no counter ran at `c5335c7`. Scratch
under `/tmp/tameshi-r43-w2-CritC1Standing/` (shared clone + counter copies). No installs.

**Verdict: RELABELLED.** The K/D/E/U rule is applied mechanically and the record is
internally consistent — nothing is faked, and the F11 kill of `outflag_no_parse_args_check`
is a genuine, bound, reachable-code kill (`kill_binding=1`, kill_cases `['F11…']`). But
`dead_code_only` for `method_fold_several_returns` is a label about the *fixture's shape*,
not a judgment about the mutant's reachability: the divergent output sits on a **live** write
site and is a false negative of exactly the class the tool exists to prevent, and the
justifying nonexistence claim ("no reachable-input fixture") holds only because the base
tool's own recorded W3 defect hides the reachable discriminating input.

---

## 1. What the routed defect asked and what was delivered

Round-42 routed it concretely (`corpus/lessons/round-42.md:216`, verbatim from
`.ufo/waves/round-42/w2/MutantAuthor.md:164`): `outflag_no_parse_args_check` is "killable
only by a fixture that registers `--out` and reads `.out` off an object that is not a
parse_args namespace"; `method_fold_several_returns` "differs only on dead code". Round 43
delivered F11 (exactly the routed fixture shape; kill bound to it by `kill_binding`,
`measure.py:615`) and F12 (the dead-code discriminator). So the *disposition* the route
named — "killable fixtures **or** a dead-code judgment" — was followed.

The question is whether the second half is a *judgment* or a *rename*. The round-42 record
already contained the observation "differs only on dead code" while scoring it unresolved.
Round 43's contribution is the rule that makes that observation a terminal class with a pass
value (`contract.json claims.C1.target`: `dead_code_only=1 unresolved=0 → C1_R43_PASS=true`).
The mutant, its edit, and its behaviour are byte-identical to what round 42 scored as a
survivor; only the name changed. The lesson itself concedes the ledger does not move:
`corpus/lessons/round-43.md` C1-limits — "Numeric depth stays 9: the counter adds a decision
table and two fixtures, not a ledger leg."

## 2. F12's divergence is on a *reachable* site — a false negative, not a non-event

Reproduced at `3aee2c0` (pristine `784de4c0…` vs mutant `if len(returns) != 1:` →
`if len(returns) < 1:`, applied once):

```
pristine  tools/write-path-census-v4.py --file F12 →
  site L11: expected=False scratch=False unflagged=False resolved=self.destination()
mutant →
  site L11: expected=True  scratch=False unflagged=True
            resolved=os.path.join('tmp', 'expected.json')tmp'tmp'expected.json'expected.json'
```

The site is line 11 (`with open(self.destination(), 'w')` inside `run()`) — a live statement;
the only unreachable statement is the second `return` inside `destination()` (lines 6-8), the
*trigger*, not the observed object. The mutant flips `expected` and `unflagged` on a live
write site — i.e., it reports a `tmp/…` write as an expected, unflagged write, a false
negative of exactly the class `live_unflagged_v4=0` polices. (The mangled `resolved` text is
shared pristine behaviour — identical output on a one-return `destination()` — so it is not
attributable to the mutant.)

Two structural counters from the committed code:

- **The tool's own scope includes unreachable code.** A fixture consisting of a write
  *after* `return` (`def main(): return; with open('golden/expected.json','w')…`) is still
  reported by the pristine tool — observed: `site L3 expected=True resolved=golden/…`.
  So "an input that no runtime path reaches" is not a meaningful input class for this
  analyzer: it consumes source text wholesale, by design.
- **The gate is fixture-granular, not divergence-granular.** `battery()` sets
  `detail[name] = bool(unreachable_statements(src))` (`measure.py:362`) — *any* statement
  after an unconditional `return`/`raise` *anywhere* in the fixture makes the whole case
  unreachable, and `differential()` tags the case `dead_code` on the same whole-fixture test
  (`measure.py:471`). The K gate discards F12's FAIL not because the *diverging statement* is
  unreachable — it is not — but because the fixture happens to contain a dead statement. The
  docstring gloss ("the mutant's divergence exists only on inputs that no runtime path
  reaches", `measure.py:19`) is therefore false of the observed divergence; the lesson's own
  limits section says the opposite — "The K rule's 'reachable' gate is a source-text
  property, not a runtime one" (`corpus/lessons/round-43.md`, C1 limits). One of the two
  sentences misstates the rule as shipped.

## 3. "No reachable-input fixture exists" is contingent on the base's own defect

`corpus/knowledge/r43-survivor-resolution-rule.md:84` asserts: "There is no reachable-input
fixture for this mutation, and the rule says so instead of manufacturing one." The argument
is true *only* because `method_return` collects `returns` from `method.body` direct children
(`tools/write-path-census-v4.py:138`), so two direct returns force an unreachable second
return. But the lane's own round-42 record says the unmutated tool misreads nested-return
methods (witness W3, `MutantAuthor.md:164`). A real-world method like

```python
def destination(self, branch):
    if branch:
        return 'tmp/expected.json'
    return 'golden/expected.json'
```

has two returns and **no unreachable statement** (`unreachable_statements` returns `[]` on
it — counter's own AST rule). With the W3 defect repaired (returns collected via
`ast.walk`, scratch copy `v4_w3fixed.py`, committed-byte edit elsewhere):

```
w3-fixed pristine  on H → site: expected=False unflagged=False resolved=self.destination(…)
w3-fixed + mutant  on H → site: expected=True  unflagged=True  resolved=golden/expected.json
```

A fixture with zero unreachable code distinguishes pristine from the mutant as soon as the
recorded W3 defect is fixed. `dead_code_only` is therefore a property of *(mutant × the
base's body-only return scan)*, not of the mutant: it evaporates under a repair the lane has
already documented and deferred. A class that exists only while a known base bug stands is
not a stable survivor class — it is the bug, renamed.

## 4. Is F12 acceptable as the basis for a named survivor class?

Partially. It is a genuine differential witness: the mutant's fingerprint differs on it and
on nothing else in the declared corpus (`dead_code_cases=F12_method_two_returns`, and — post
A14 — the differential now also covers the three live files; the mutant does not diverge
there, nor on any `tools/*.py` at `3aee2c0`: AST scan, 31 files, 0 methods with ≥2 direct
returns). But as the *basis for the nonexistence claim* it is insufficient:

- F12 is a **characterization fixture**: its declared `want` values (expected=False,
  unflagged=False, needle `self.destination()`) encode the pristine tool's current refusal,
  not an authored spec. The same fixture is a FAIL under the exit-plus-FAIL oracle —
  `C1_R43_PROBE … verdict=dead_code_only failures=1 first=['F12…expected=1 want 0']` —
  excluded only by the fixture-granular gate (§2). The class thus rests on a detection the
  rule declines to count, not on evidence that no reachable input exists.
- The nonexistence claim is really a static proof about the base's return scan, and it is
  false as stated (§3). The fixture cannot carry it; the proof does, and the proof is
  base-dependent.

## 5. Does `C2_R42_PASS=false` stay honest?

Yes — verified on committed bytes.

- `git diff --stat 487b8f0..HEAD -- .ufo/evidence/round-42` is empty; no round-43 commit
  touches `corpus/lessons/round-42*`; `mutants.json` last changed in round-42 (`f6762b8`)
  and is now pinned (`mutants_sha_ok=1`).
- `SCORECARD.md:2028-2042` still prints `mutants_killed=4 … C2_R42_PASS=false` with the two
  survivors named and the miss "reported, not narrowed".
- `corpus/knowledge/r43-survivor-resolution-rule.md:74` says the record "stays false — not
  re-adjudicated here", and the round-42 parenthetical predictions both verify
  (F11 is exactly the routed fixture; "differs only on dead code" is the D disposition).
- The round-43 claim does not edit the round-42 predicate; it adds a *new* predicate under
  which `dead_code_only` counts as resolved. A closure reader must not read `5+1` as a
  correction of `4/6`: the numbers measure different predicates over the same bytes.

## 6. Reproducibility defects a closure reader will trip on (fixable)

- `contract.json frozen_before` still says "the freeze of record is 114ffacd…" at `HEAD`
  (`6b83a11`), stale by four freeze commits (A11–A14 never updated it).
- `SCORECARD.md:2059` publishes `--freeze 17f6ef0c…` for C1. Measured: A10 counter bytes at
  `--rev 3aee2c0 --freeze 17f6ef0c` → `self_pin=0 → C1_R43_PASS=false`; at
  `--freeze 3aee2c0` → `PASS=true`; A14 bytes at `--freeze 6b83a11` → `PASS=true`
  (`self_pin=1 … kill_binding=1 mutants_sha_ok=1`). Only the newest freeze reproduces; the
  two pointers a reader is handed both fail.

## Smallest safe correction

Keep the disposition but rename and re-word it: the class is `input_deferred_defect` (or
"dead-code-triggered"), the gloss "the discriminating construct is unreachable in the
analyzed source under the tool's current body-level return scan; the differing site itself
is reachable", and the knowledge entry's absolute "no reachable-input fixture exists" gains
"under the v4 body-only return scan (W3)". Update `frozen_before` and the SCORECARD counting
command to the deciding freeze. If the canonical judge instead requires the stronger rule
("kills gated on the diverging site's reachability, not the fixture's"), then under the
committed bytes F12 is a kill and the honest line is `mutants_killed=6` — the current
`dead_code_only=1` is the weaker of the two readings and stands only under the
fixture-granular gate.

Report: `.ufo/waves/round-43/w2/CritC1Standing.md`
