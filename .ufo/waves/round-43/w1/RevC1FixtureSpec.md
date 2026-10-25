# RevC1FixtureSpec — F11 and F12 read as SPEC statements, not as observations

Scope: `.ufo/evidence/round-43/mutants/measure.py` (`sha256 901d947f…`, the bytes the working-tree
contract now pins) against `tools/write-path-census-v4.py` (`784de4c0…`, unchanged at freeze) and
`corpus/knowledge/r42-attribute-and-outflag-destinations.md`. Question: is each fixture's declared
class derivable from the documented behavior, or is it only *whatever the tool printed*?

No measurement run was performed. Pristine/mutant/differential runs below are in-process or against
scratch copies under `/tmp/tameshi-r43-RevC1FixtureSpec-run`.

## Verdict

- **F11_outflag_namespace — derivable.** The class follows from docstring `:26-29` plus entry
  `:24-25`, `:50-54`. No component of its declared `want` requires running the tool.
- **F12_method_two_returns — the rule derives, one field does not.** The refusal derives from
  docstring `:21-23` and entry `:44-45`; the four bits derive from the refusal. The `needle`
  (`'self.destination()'`, `measure.py:243`) does **not** derive from any document — it pins the
  undocumented `resolved` fallback string. It is the only component in either fixture that is
  "whatever the tool printed", and it is **not load-bearing**.
- Neither fixture's *class* is tool-printed-only. One implementation defect (H1) makes the
  class-computing machinery unsound in general, but it does not change either verdict this round.

## 1. What each fixture asserts, stated as a spec sentence

### F11 (`measure.py:209-228`)

> A write whose destination root is `<name>.<dest>`, where `<dest>` is the `dest` of a declared
> output option (`--out` at `:13`), is **not** `explicit_out` when `<name>` is bound to a namespace
> that is not a `parse_args(...)` result. Being an expected-path write with no scratch marker and
> no update flag, it is `unflagged`.

Site: line 8, `(out / 'expected.json').write_bytes(data)`; `out` is the second parameter of the
module-level `publish`; its single in-module call passes `Path(options.out)` and
`options = SimpleNamespace(out='golden')` (`:15`).

Derivation chain, clause by clause:

| clause used | document |
|---|---|
| output options are `--out/--output/--out-dir/--output-dir`, dest `-`→`_` or `dest=` | docstring `:24-25`; entry `:49-50` |
| the namespace **must** come from `parse_args(...)` before an attribute read counts | entry `:22-25` ("That is the binding the tool checks for: the namespace must come from a `parse_args(...)` call before an attribute read counts as an option value") |
| the parameter clause also requires an expression "that does" (i.e. the same parse_args test) | docstring `:26-29`; entry `:50-53` |
| a call with any other argument keeps the site unflagged | entry `:53-54` |

`SimpleNamespace(out='golden')` is not a `parse_args` result, so both the direct attribute branch
and the parameter branch fail: `explicit_out=False`. Derivable without execution.

### F12 (`measure.py:230-244`)

> A `self.<m>()` call used as a write destination is **not** folded when `<m>` has two *top-level*
> `return <expr>` statements. The destination stays unresolved, so the site is not `expected`.

Site: line 11, `open(self.destination(), 'w')`; `destination` has `return first` (`:7`) followed by
`return os.path.join('golden', …)` (`:8`).

| clause used | document |
|---|---|
| fold only for a method with **exactly one top-level** `return <expr>` | docstring `:21-23`; entry `:44-45` |
| "evaluated in the method's own top-level assignments" | docstring `:23`; entry `:45` |
| unresolved destinations are not proven safe | docstring `:37-43` |

Two top-level returns ⇒ no fold ⇒ the destination is not a path ⇒ no expected token ⇒
`expected=False`, and the remaining bits follow. Derivable without execution.

## 2. Derivability of every asserted field

Legend: **D** = stated in the docstring/entry; **D′** = documented in a *different* committed
knowledge entry; **S** = only in tool source (constant or expression); **O** = observable only by
running the tool (not derivable from any committed prose).

| field | F11 | F12 | source of truth |
|---|---|---|---|
| assertion of record (the rule) | D | D | docstring `:21-29`; entry `:44-54` |
| `expected` | D′ + S | D′ + S | `EXPECTED_RE` at tool `:57` (`expected\.json\|…\|golden\|snapshot`). The r42 entry never lists the token set; `corpus/knowledge/r40-write-form-misses.md:10` documents `expected.json` as an expected-path token. Derived values, not quibbles: F11 `True` (literal `'expected.json'` is the right operand of `/`), F12 `False` (unfolded call text carries no token). |
| `scratch` | S | S | `SCRATCH_MARKERS` at tool `:61-68`; entry `:101` documents only that the test is a whole-resolved-text substring test. F11 `False`: no marker in `'expected.json'`. F12 `False`: no marker in `self.destination()`. |
| `explicit_out` | D | D | F11: docstring `:26-29` + entry `:24-25`. F12: no output-option shape is involved at all. |
| `unflagged` | **S** | **S** | tool `:385` `expected and not scratch and not flagged and not explicit_out`. Docstring `:30` states only "`explicit_out` implies not `unflagged`"; the r42 entry states nothing about the conjunction. |
| `lineno` (8 / 11) | D | D | the write-call line of the fixture source; structural. |
| `needle` | — (None) | **O** | `'self.destination()'` is the generic-`Call` branch of `_resolve` (tool `:165-203`), which seeds `trace = _src(node, text)` and returns it joined with argument resolutions. Nothing in docstring `:21-30`, docstring `:45-47` (which lists `resolved` as a field without defining it) or entry `:44-48` says what an unfolded call's `resolved` contains. **This is the one "whatever the tool printed" component.** |

Consequence for `unflagged`: all twelve fixture `want` dicts and all three `LIVE` entries assert an
`unflagged` value whose defining formula exists only at tool `:385`. The fixtures are therefore
document-derivable for their *class* but not for that *field*; a reader holding only the docstring
and the r42 entry cannot compute it.

## 3. Findings by severity

### H1 — The amended K/D machinery discards live-site failures (mislabels `equivalent` / `dead_code_only`)

`battery()` populates the reachability detail **only inside the fixture loop**:

```
measure.py:358        detail[name] = bool(unreachable_statements(src))     # fixture branch only
measure.py:373        fails.append('%s:%d %s' % (rel, lineno, reason))     # live branch: no detail
measure.py:559-560    reachable_fails = [case for case in mdetail if not mdetail[case]]
                      if mf and reachable_fails: killed.append(name)
```

A live-site failure contributes to `mf` but never to `mdetail`, so it can never reach
`reachable_fails`. The mutant then falls through to `differential()` (`measure.py:448-461`), which
iterates `FIXTURES` only, so a live-only divergence yields `differ == []`.

This contradicts the contract's K text — "the round-43 battery (12 fixtures + 3 live sites)
produces at least one FAIL" (`contract.json`, `claims.C1.rule.K_kill`) — because the code requires
the FAIL to be a *fixture*. Two demonstrations, the second included `stub_live_only.py` /
`stub_mut_plus_live.py` wrappers that are identical to the tool on all twelve fixtures and differ
only at the documented live sites:

```
# live-only regression, all fixtures green
fixture_pass=12/12 fails=['tools/context-capture.py:1682 scratch=0 want 1',
                          'tools/context-capture.py:1685 scratch=0 want 1']
detail(fixture-only)={}   K gate evaluates to killed=False
differential(stub,pristine)=[]        => classification reached: equivalent

# real method_fold_several_returns mutation PLUS the same live regression
fails=['F12_method_two_returns expected=1 want 0',
       'tools/context-capture.py:1682 scratch=0 want 1',
       'tools/context-capture.py:1685 scratch=0 want 1']
detail={'F12_method_two_returns': True}  reachable_fails=[]
K gate killed=False
differential=[('F12_method_two_returns','dead_code')]  => would classify: dead_code_only
```

The second case is the dangerous one: a mutant that regresses two documented live sites and also
touches a dead-code fixture is labelled `dead_code_only`, i.e. it is exempted from the kill rule for
the wrong reason. This round's verdict is unaffected — the real
`method_fold_several_returns` mutation differs on no live file (my own AST scan of `tools/*.py`:
`methods with >=2 top-level returns in tools/: NONE`; CritC1DeadCode Evidence 4 reaches the same
conclusion by full re-censusing) — but the class-computing machinery would accept an incorrect
class, which is exactly the failure mode this axis is supposed to exclude.

Correction (not applied — read-only seat): record live failures in `detail` too, or gate on
"at least one failing case whose source is reachable", treating live cases as reachable by
definition, and extend `differential()` to the live files.

Note this also qualifies CritC1DeadCode's Evidence 4 sentence "the K oracle battery covers the
three LIVE sites": under `measure.py:559-560` it covers them for *reporting*, not for *killing*.

### H2 — F12's `needle` pins an undocumented `resolved` fallback

`measure.py:243` asserts `'self.destination()' in site['resolved']`. Measured pristine output:

```
{"expected": false, "explicit_out": false, "flagged": false, "kind": "open",
 "lineno": 11, "resolved": "self.destination()", "scratch": false, "unflagged": false}
```

Three problems, in order of importance:

1. **Not derivable.** Neither the docstring nor the entry defines `resolved` for an unfolded call
   (docstring `:45-47` names the field only). A reader of the spec cannot produce this string.
2. **Not load-bearing.** The mutant flips `expected` `False→True`, so the four bits already
   discriminate; `check_site` compares bits first and the needle second (`measure.py:317-325`).
   Removing the needle leaves F12's class and the kill/differential outcome identical.
3. **Over-constraining.** A legitimate, equally conservative implementation that leaves an unfolded
   call's destination unresolved (`resolved=''`, or a marker such as `<unresolved>`) satisfies every
   documented property — `expected=False, scratch=False, explicit_out=False, unflagged=False` — and
   fails F12. The fixture therefore tests an implementation detail rather than the documented rule.

Recommendation: drop the needle, or add the fallback sentence to the docstring ("an unfolded
`self.<m>()` destination is reported as the call's source segment").

### M1 — `unflagged`'s defining conjunction is source-only

See §2. Tool `:385`; docstring `:30`; entry has no statement. Every `unflagged=` assertion in the
battery (12 fixtures + 3 live) depends on it. One sentence in the docstring fixes the whole class.

### M2 — `expected` token set is source-only for these two fixtures

`EXPECTED_RE` (tool `:57`) includes `golden`, `snapshot`, `.expected\b` — none of which the r42
entry lists. F11 and F12 both turn on its substring test (F11 `True` from `expected.json`; F12
`False` from the absence of a token in `self.destination()`). The r40 entry documents
`expected.json`; a reader of only the r42 entry cannot derive these two bits.

### L1 — F12's comment implies a distinction the tool does not make

The comment (`measure.py:231-233`) contrasts a first return under `'tmp'` with a second under
`'golden'`. Two facts measured:

- `SCRATCH_MARKERS` holds `'/tmp'` (with the slash, tool `:61`), so `'tmp'` does **not** register:
  under the mutant the folded value is `expected=True, scratch=False, unflagged=True`.
- The second (dead) return's *value* is never read by either tool; only its **count** matters to
  `method_return` (tool `:138-140`). The fixture asserts a count rule, not a value conflict.

Neither fact changes the declared class (F12's `want` asserts only the pristine behaviour), but the
comment invites a wrong inference about what the fixture discriminates.

### L2 — Name collision with the tool's own selftest, asserting the opposite

`tools/write-path-census-v4.py:510` has a selftest case named `method_two_returns` — two `return`
statements, one *nested* under `if fast:`, count 1 — and it asserts the fold **succeeds**
(`unflagged=True`). `F12_method_two_returns` has two *top-level* returns and asserts the fold is
**refused**. A grep by name returns two contradictory specs. (CritC1DeadCode Finding 2 already
records the coverage gap in that selftest case; the contradictory-assertion angle is additional.)

### L3 — F11 is load-bearing: the selftest case named for its rule is vacuous

`tools/write-path-census-v4.py:610` `output_attr_not_parse_args` reads as if it pins F11's rule.
It does not: the fixture module declares **no** output option, so `Module.out_dests` is empty and
the guard at tool `:284` short-circuits before `_parse_args_ns` is ever called:

```
out_dests for selftest output_attr_not_parse_args = {}
records: [... 'explicit_out': False ...]        # same class with or without the check
out_dests output_namespace_param = {'output': '--output'}
```

Confirmed by selftest scoring: the `outflag_no_parse_args_check` mutant passes `--selftest` with
`cases=15 failed=0`, as does pristine. F11 is the only executable test of the refusal direction in
either artifact. Its class is derivable (above) *and* the fixture is necessary — the strongest
positive statement about F11.

## 4. Positive, non-obvious results worth recording

- **F12's `dead_code_only` is forced, not chosen.** The mutant differs from pristine iff a
  same-class method has ≥2 top-level `Return` nodes (`method_return`, tool `:138-140`); a second
  top-level `return` is unreachable in every Python program. So the divergence domain is a subset
  of programs containing dead code — a derivation from the document plus language semantics, not an
  observation. (CritC1DeadCode Evidence 2 proves the same by a different route; both stand.)
- **F12 is the battery's only dead-code fixture.** Under the counter's own detector:
  `unreachable per fixture: F01…F11 False, F12 True`. The D gate therefore cannot mislabel another
  fixture this round.
- **The ten round-42 fixtures are byte-identical between rounds** (`src`, `want`, `needle` equal;
  round 43 only appends `lineno=None`), so "mutant set unchanged, battery extended" holds for the
  fixture text. The ten are: F01…F10, and `NEW_FIXTURES` is exactly `{F11, F12}`.
- **F11's `lineno=8` is a real assertion, not decoration** (`check_site` takes the `lineno is None`
  branch only for a `None` lineno; F04 uses that branch, F11 does not). It resolves to the single
  `write_bytes` site.
- **Frozen and working fixture text agree.** `diff 17f6ef0c:…/measure.py <working>` changes only
  `battery()`/`main()` (the A5 reachability gate, the `frozen_tools` pin read, the ablatable F11
  lookup). `F11`/`F12` bytes are identical in both, so this review applies to the frozen artifact
  and to the amended one.

## 5. Residual risk and verification gaps

- **Reachability is static.** `kill_fixture_reachable` means "no statement after an unconditional
  `return`/`raise` in the same block" (`measure.py:377-400`), not "the write executes". F11's
  `main()` is never called (no `__name__` guard), so the write never runs — the same shape as
  F04–F06 and irrelevant to a static analyser, but the claim "reachable-code fixture" should be
  read in that narrow sense.
- **No renamed-identifier protection was added.** The battery's only positive `parse_args` namespace
  name is `args` (F04/F06, plus `Path(a.out)` in the live file). A tool that special-cased the name
  `args` would still pass all twelve fixtures; the rename guard lives only in the tool's selftest
  (`opts`, `ns`, `parsed`), which is outside the C1 fixture predicate. The r42 entry already
  discloses the literal-table hazard (`:114-115`); F11/F12 do not reduce it.
- **`unreachable_statements` under-detects** control-flow-unreachable tails (e.g. `while True:`
  followed by a statement). Direction is conservative — a case reads `reachable` — and cannot bite
  here (count 1 means no divergence). Recorded by CritC1DeadCode Finding 4; not re-tested here.
- **Oracle freeze.** The counter bytes are not the frozen bytes (`901d947f…` vs `ad7ecf8c…` at
  `17f6ef0c`); contract amendment A5 discloses the change and moves the pin, while
  `amendments_note` still reads "counters … byte-unchanged". Provenance/pin ownership sits with
  MutC1F11 §4 and MutC1F12 §7; I confirm the byte mismatch and note that it does not affect the
  fixture text.

## 6. Commands run (evidence)

```
python3 -I tools/write-path-census-v4.py --file /tmp/…/F11_outflag_namespace.py --json
  -> [{expected:true, explicit_out:false, flagged:false, lineno:8, resolved:"expected.json",
       scratch:false, unflagged:true}]
python3 -I tools/write-path-census-v4.py --file /tmp/…/F12_method_two_returns.py --json
  -> [{expected:false, explicit_out:false, flagged:false, lineno:11,
       resolved:"self.destination()", scratch:false, unflagged:false}]
# mutant replay over all 12 fixtures (find/replace from round-42 mutants.json)
outflag_no_parse_args_check  -> DIFF F11: explicit_out true, unflagged false, resolved + " argparse --out"
method_fold_several_returns  -> DIFF F12: expected true, unflagged true,
                                resolved "os.path.join('tmp', 'expected.json')tmp'tmp'expected.json'expected.json'"
# selftest scoring of all six mutants
PRISTINE 15/0 · outflag_no_parse_args_check 15/0 · method_fold_several_returns 15/0 ·
method_fold_disabled 2 fail · attr_bind_several_assignments 2 fail ·
attr_never_resolve_self 2 fail · outflag_dests_never_recorded 8 fail
# fixture-level reachability
unreachable per fixture: only F12_method_two_returns True
# live corpus
methods with >=2 top-level returns in tools/: NONE
# K-gate hole (H1)
stub_live_only      -> fixture 12/12, fails live-only, detail={}, killed=False, differential=[] => equivalent
stub_mut_plus_live  -> detail={F12:True}, reachable_fails=[], differential=[F12 dead_code] => dead_code_only
```

Scratch: `/tmp/tameshi-r43-RevC1FixtureSpec-run` (created and removed). No tool installed or
upgraded; no pacman transaction. Lane checkout unmodified: `git status --porcelain` shows only
pre-existing entries from other seats, none written by this seat.
