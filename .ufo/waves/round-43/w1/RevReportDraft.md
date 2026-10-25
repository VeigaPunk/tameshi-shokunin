# RevReportDraft — round 43 / w1: claim sentence = predicate sentence = printed label?

Seat: `L1Tameshi43.RevReportDraft` (leaf; no dispatch). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Snapshot: 2026-10-25T07:52–07:58:35-03:00. Freeze commits seen: `17f6ef0` (original pins) and `5cd2154` (A4/A5 pins, 07:56:24). **The instrument set moved during this review** (see F0); every quote below is labelled *frozen* (bytes at `17f6ef0`) or *HEAD* (bytes at `5cd2154`/working tree), and both printed-label runs are recorded verbatim.

Commands run (only allowed forms; `REV`/`--freeze` ∈ {`487b8f0`, `17f6ef0`}):

```
python3 .ufo/evidence/round-43/mutants/measure.py     --lane … --rev 17f6ef0 --freeze 17f6ef0
python3 .ufo/evidence/round-43/calibration/measure.py --lane … --rev 487b8f0|17f6ef0 --freeze 17f6ef0
python3 .ufo/evidence/round-43/guard/measure.py       --lane … --rev 17f6ef0 --freeze 17f6ef0
```

No installs, no writes outside `/tmp/tameshi-r43-RevReportDraft/`, no git/jj mutation.

## Axes named

1. **Literal identity** — is the contract sentence the same statement as the docstring predicate sentence and as the printed label?
2. **Quantifier coverage** — for each `all/every/no/only`, is the set enumerated by the counter?
3. **Executed agreement** — does the label produced at a permitted rev agree with the sentence?
4. **Instrument integrity** — a measurement is only a statement about the claim if the pinned bytes are the bytes that ran (found while executing axis 3).

---

## F0 (BLOCKING, precedes C1–C3): the pinned instruments changed mid-wave; at the declared freeze no claim can now print `PASS=true`

| file | pin @17f6ef0 | bytes @17f6ef0 | pin @5cd2154 | bytes @5cd2154 | disk 07:58:35 |
|---|---|---|---|---|---|
| `mutants/measure.py` | `ad7ecf8c…` | `ad7ecf8c…` | `901d947f…` | `901d947f…` | `901d947f…` |
| `calibration/measure.py` | `092c76cd…` | `092c76cd…` | `092c76cd…` | `092c76cd…` | **`52961c37…`** |
| `guard/measure.py` | `6278edcd…` | `6278edcd…` | `fbc8ad3c…` | `fbc8ad3c…` | `fbc8ad3c…` |
| `tools/staged-id-guard.py` | `8140945a…` | `8140945a…` | `efa5f129…` | `efa5f129…` | **`365bf958…`** (edited 07:55:17 → 07:58:28, three revisions) |

Observed `self_pin` (label field, not inference):

- frozen counters, `--freeze 17f6ef0`: `C1 self_pin=1`, `C2 self_pin=1`, `C3 self_pin=1` (my 07:52 runs).
- after the wave-1 edits, `--freeze 17f6ef0`: `C1 self_pin=0`, `C2 self_pin=0`, `C3 self_pin=0` (my 07:56–07:58 runs). Predicate fails on `self_pin` alone.
- `calibration/measure.py` on disk (`52961c37…`) is pinned by *neither* freeze ⇒ `C2 self_pin=0` at both freezes until the pin and the bytes agree again.
- `tools/staged-id-guard.py` on disk (`365bf958…`) is pinned by neither freeze ⇒ `tool_sha_ok=0` for C3 at any rev once committed in this state.

Two contract texts are now false and are *not* covered by A4/A5's own disclosure:

- `frozen_before`: "frozen before any wave seat ran and before the first deciding run" — A4/A5 are dated "during wave 1" and `5cd2154` postdates w1 seat reports.
- `amendments_note`: "amendments … change citations and disclosures only; **claims.\*, the predicates, counters, targets, kill rule and controls are byte-unchanged**" — A4 changed the tool and its pin; A5 changed two counters and three pins.

Substance of A4/A5 is rule-preserving (A5 implements the frozen K sentence; A4 implements the frozen by-document sentence), but the *bytes* are not, so the freeze declaration no longer describes the instrument. This is the same finding `L1Tameshi43.RevProvenance` raised at 07:57; I reproduce it independently from pin arithmetic.

---

## C1 — verdict: **NOT the same statement** (contract ⊃ predicate; label contradicted both, then contradicted `self_pin`)

**Contract** (`contract.json:22`):
> "The two survivors of the round-42 mutant set are resolved under the pre-declared rule K/D/E/U: outflag_no_parse_args_check is killed by a new reachable-code fixture (F11_outflag_namespace) and method_fold_several_returns is classified dead_code_only by the declared dead-code construct with a differential probe, leaving five killed and one dead-code-only and zero unresolved, with the round-42 mutant declaration unchanged."

**Predicate** (frozen `mutants/measure.py:33-42`, byte-identical at HEAD):
> "Predicate `C1_R43_PASS` is true iff: self_pin=1, tool_absent=0, tool_sha_ok=1, selftest_exit=0, fixtures_pass=12/12, run_errors=0, the three live sites match, live_unflagged_v4=0 over every tracked `tools/*.py` at REV, mutants_declared=6, mutants_killed=5, dead_code_only=1, equivalent=0, unresolved=0, `outflag_no_parse_args_check` ∈ killed, and `method_fold_several_returns` ∈ dead_code_only."

**Label — frozen counter @07:52, `--rev 17f6ef0 --freeze 17f6ef0`** (the `tool_sha_ok=1` field here is **withdrawn**; the frozen bytes reproducibly print `tool_sha_ok=0` — see Addendum B):
> `C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 … mutants_declared=6 mutants_killed=6 dead_code_only=0 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,method_fold_several_returns,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names= dead_code_cases= dead_code_arg_ok=0 kill_fixture_reachable=1 … C1_R43_PASS=false`

**Label — HEAD counter @07:56, `--rev 17f6ef0 --freeze 17f6ef0`:**
> `C1_R43: self_pin=0 … mutants_killed=5 dead_code_only=1 … killed_names=…,outflag_no_parse_args_check dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_fixture_reachable=1 … C1_R43_PASS=false`

### F1.1 (HIGH) The frozen counter did not implement the frozen K rule: it killed on the dead-code fixture
Frozen `mutants/measure.py:550-552`: `if mf: killed.append(name); continue`. Any battery FAIL is a kill, with no reachability gate, although `rule.K_kill` requires "the killing fixture contains no runtime-unreachable statement" and `differential()` already classifies cases `dead_code`/`reachable`.

Reproduced per mutant in `/tmp` against the frozen tool (imported the frozen fixture set, staged fixtures in `/tmp`, ran `battery`+`differential`):

```
method_fold_several_returns  battery_fails=['F12_method_two_returns expected=1 want 0']  differ=[('F12_method_two_returns','dead_code')]
outflag_no_parse_args_check  battery_fails=['F11_outflag_namespace explicit_out=1 want 0']  differ=[('F11_outflag_namespace','reachable')]
(attr_bind→F03, attr_never→F01/F02, method_fold_disabled→F01, outflag_dests→F04: all 'reachable')
```

So the mutant's only divergence is on F12 (dead code), yet it was recorded `killed`. `dead_code_only=0`, `dead_code_arg_ok=0`, `mutants_killed=6` — the target "`mutants_killed=5 dead_code_only=1`" was unreachable at the frozen bytes' design, not just at this rev. HEAD's A5 gate (`reachable_fails`) repairs exactly this and yields the claimed 5/1/0 (label above).

### F1.2 (MEDIUM) Widening: the claim names the killing fixture; the predicate never checks which fixture kills
"C1: killed by a new reachable-code fixture (F11_outflag_namespace)". The predicate tests `outflag_no_parse_args_check ∈ killed` plus `kill_fixture_reachable=1`, and the frozen computation of that field (`mutants/measure.py:568`) reads **F11's source text only** — it does not assert F11 is the killing case. A mutant killed by any of the other eleven fixtures would satisfy both fields. The attribution is *true* (differential above: F11 is the only differing case) but it is **not tested**; at HEAD the field still only inspects `FIXTURES['F11_outflag_namespace']`.

### F1.3 (MEDIUM) Widening: two provenance clauses are untested
- "the two survivors of the round-42 mutant set" — the counter enumerates the six entries of `mutants.json` and never reads the round-42 record. The provenance is true (`.ufo/evidence/round-42/after/c2-at-242c1b4a.stdout:4,6`: `method_fold_several_returns … outcome=survived`, `outflag_no_parse_args_check … outcome=survived`), but nothing in the predicate would notice a different survivor set.
- "with the round-42 mutant declaration unchanged" — no pin, hash or `git diff` against round 42; the counter would accept any six-mutant file. I verified byte equality by hand: `.ufo/evidence/round-42/census/mutants.json` is `b3abab06…` at both `487b8f0` and `17f6ef0`. True, untested.

### F1.4 (LOW) The docstring predicate is narrower than the code predicate and the contract target
The predicate sentence omits `kill_fixture_reachable` and `dead_code_arg_ok`, both of which the code requires (`mutants/measure.py:614`) and both of which the contract `target` lists. The printed label prints both. Three artefacts, three field sets.

### Quantifiers
- "every tracked `tools/*.py`" — **enumerated** (`git ls-tree -r … tools/` in `stage()`); no flag.
- "zero unresolved" — **enumerated**: the loop partitions all six mutants into killed/dead/equivalent/unresolved (apply- and run-errors included); no flag.
- "the two survivors" — **not enumerated as a set** (F1.3); arithmetic `5+1+0 = 6` happens to cover the six declared mutants, but the two-element set the sentence names is never computed.

---

## C2 — verdict: **same envelope, NOT the same statement** in four classes plus the `classes=` token

**Contract** (`contract.json:39-40`):
> "The lane's self-assessment records agree with the observed repo state across seven classes: … plus m12 (the newest SCORECARD round block declares the next round's planned claims) and m13 (the newest standing sources-registry counting command is census-valid and load-bearing on an indented-row mirror), with total=0."
> target: "C2_R43_PASS=true: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0"

**Predicate** (`calibration/measure.py:32-34`, unchanged by the wave-1 edit):
> "Predicate `C2_R43_PASS` is true iff: self_pin=1, classes=7 (all seven declared classes ran — a counter that omits m12/m13 cannot pass), and m6=m7=m8=m10=m11=m12=m13=0."

**Label — base `487b8f0` and freeze `17f6ef0` (identical):**
> `C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=1 m13=1 total=2 records=3 sources_rows=113 standing=113 receipts=17 revisions=3 m13_probe=standing=6_column0=112_valid=113 … C2_R43_PASS=false first=m12:…`

This matches `before_state` exactly (`m12=1 m13=1`), so the *before* statement is honest. The claim is a post-repair statement, not yet reachable here.

### F2.1 (HIGH) `classes=7` is a constant, and the predicate sentence says it proves seven classes ran
`calibration/measure.py:440` `declared = 7`; `:456` `passed = self_pin == 1 and declared == 7 and total == 0`. Nothing derives or checks it against `len(classes)`. The label therefore prints an assertion as a measurement. A class computed vacuously (`m13 = []` unconditionally) still prints `classes=7` and passes. The predicate sentence's parenthetical "(all seven declared classes ran — a counter that omits m12/m13 cannot pass)" is **not what the counter tests**; omission is caught only by a `KeyError` in the field loop, and vacuity is not caught at all. The wave-1 edit even added, 8 lines later in the same docstring, "`classes=` is the count of declared classes and is a constant: the evidence that a class ran is its own m-field, not that token" — i.e. the docstring now contradicts its own predicate sentence.

### F2.2 (MEDIUM) m12: sentence quotes a bold field; the frozen test was a bare substring
Contract `classes.m12` (`contract.json:51`): "the newest '## Round N' SCORECARD block carries `'**Planned (round N+1):**'`". Frozen `calibration/measure.py:120-121`: `wanted = 'Planned (round %d)' % (round_no + 1)`. Bold marker and colon are untested; any prose occurrence passes, so "declares the next round's planned claims" was satisfiable by a sentence that merely mentions them. **Widening (sentence > test)** at the freeze; HEAD now tests `'**Planned (round %d):**'`, which makes the two equal.

### F2.3 (MEDIUM) m13: the sentence binds the *command*; the counter tests a substring of the *row* and its own two regexes
Contract `classes.m13` (`:52`): "the newest standing sources-registry row's counting command names the census-valid 0-3-space pattern, and an indented-row mirror proves the difference (column0 = N-1, census-valid = N)". Frozen `:165`: `if '0,3' not in newest and '0-3space' not in newest:` — a substring test over the whole row line, not the backticked command cell; and `:167-169` builds the mirror from `corpus/SOURCES.md` and counts it with `count_patterns()`, the counter's *own* two regexes. The cited command is never executed or parsed. So `m13=0` establishes only (a) the row's text contains `0,3`, and (b) the counter's own patterns differ by one on an indented mirror — the mirror is a self-check of the counter, not evidence about the named command. A row carrying the column-zero command plus the prose "0,3" would have passed (HEAD's `T2_column_zero_plus_prose_detected` now closes that hole by restricting to backticked `grep` cells). **The residual misattribution survives the repair**: the "load-bearing mirror" half still says nothing about the command.

### F2.4 (HIGH) m10: the frozen counter exempted the superseding receipt too — the opposite of its own sentence
Contract `classes.m10` (`:49`): "no presence receipt under `.ufo/waves` asserts present/absent contrary to the tree; a receipt named in another receipt's supersedes is history and its claims are not counted". Frozen `:242-244` adds **both** ends: `superseded.add(key…)` **and `superseded.add(value)`**, where `value` is the *superseding* receipt; `:252` then skips any claim whose `receipt ∈ superseded`. The docstring says "the superseding receipt carries the claims" — the code dropped exactly those claims. Live at the freeze, three receipts carry `supersedes`:

```
.ufo/waves/round-21/original-outcomes2-corrected.json -> original-outcomes2.json file-presence inference
.ufo/waves/round-42/supersede/round-20-outcomes.json  -> .ufo/waves/round-20/outcomes.json
.ufo/waves/round-42/supersede/round-41-residual-receipt.json -> .ufo/waves/round-41/residual/receipt.json
```

so the universal "no presence receipt under `.ufo/waves`" was, at the freeze, **not enumerated as stated**: every receipt appearing on either side of any `supersedes` was excused. HEAD adds only the key — sentence and code now agree. Note the round-42 m10 had a stronger covering condition ("all its own assertions agreeing, re-asserting every path of the superseded receipt"); round 43 dropped it, so "carried class" overstates continuity.

### F2.5 (HIGH) The record universal is not enumerated, and the round-42 floor was dropped
`RECORDS` is `corpus/lessons/round-42.md`, `corpus/lessons/round-43.md`; `round-43.md` exists at **neither** `487b8f0` nor `17f6ef0`, and absent files are silently skipped (frozen `:357-361`, `if raw is not None`). With the SCORECARD round block and the LOG slice, `records=3`. The contract says "**The lane's self-assessment records** agree" — the lane holds ~44 `corpus/lessons/*.md`, five `considerthese/*.md`, and `plans/`, `reports/`, none enumerated. Round-42's predicate required `records=6`; round 43 has **no record-count floor**, so a shrinking set is invisible to the predicate (`records=` is printed but not compared). **Widening of the sentence; narrowing of the floor.**

### F2.6 (MEDIUM) m8 is called "carried" but lost a prefix and a suffix gate
Round-42 m8 counted prefixes `corpus/ tools/ .ufo/ considerthese/ plans/ reports/`; round-43 `CITE_PREFIXES` (frozen `:61`) drops `considerthese/`, and `corpus/lessons/round-42.md` cites `considerthese/2026-10-24.md` by backtick — that cite is now unchecked. The frozen `path_cites` also required a `SKIP_SUFFIXES` match, so a broken `.yml/.png/.csv/.yaml` cite was invisible. The frozen *class sentence* matches the implementation (it lists the five prefixes), so this is a narrowing against the contract statement's "the five round-42 classes", not an internal contradiction. (HEAD removed the suffix gate and added brace expansion — closer to the sentence.)

### F2.7 (MEDIUM) The wave-1 repair weakened m11 from "revision" to "any object"
Contract `classes.m11`: "every 40-hex revision cited by those records resolves in the lane". Frozen `:268`: `git … cat-file -e token^{commit}` — a cited 40-hex had to be a commit. HEAD `:290`: `git … cat-file -e token` — any object resolves. Concrete counter-example from the checked file set: `SCORECARD.md` cites `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e`, `cat-file -t` = **tree**, `cat-file -e` exit 0, `cat-file -e …^{commit}` exit 128. It sits outside the newest round block today, so `m11=0` is not currently false — but the class no longer tests the word "revision" it claims. **Widening introduced by the repair.**

### F2.8 (LOW) Label fields ≠ target fields
Label prints `records, sources_rows, standing, receipts, revisions, m13_probe` (not in the target) and the target's `C2_R43_PASS=true:` prefix does not match the label's shape (`C2_R43:` first, `C2_R43_PASS=` last). Diagnostics are legitimate; the target is not a byte-comparable template of the label.

### Quantifiers
- "every S-id cited by the round-42/43 records" (m7) — enumerated over `records=3` texts with masking; the *set of records* is the problem (F2.5), not the ids.
- "every backtick cite under …" (m8) — **not enumerated as written**: suffix gate + dropped prefix (F2.6).
- "no presence receipt under `.ufo/waves`" (m10) — **not enumerated as written** at the freeze (F2.4).
- "every 40-hex revision" (m11) — **not enumerated as "revision"** at HEAD (F2.7).
- "all seven declared classes ran" — **not enumerated** (F2.1).

---

## C3 — verdict: **NOT the same statement** (contract lists five behaviours; the predicate exposes none of three of them; the label said `false`)

**Contract** (`contract.json:59-60`):
> "tools/staged-id-guard.py answers the round-42 post-append hazard before any append: it extracts collisions with the census-valid 0-3-space pattern, refuses a colliding row with no document, dedupes a staged row whose document the registry already holds, refuses its own naive arithmetic map because its targets are still staged ids, and admits only a by-document map (held rows dedupe; new documents take ids at or above the safe floor)."

**Predicate** (frozen `guard/measure.py:9-32`, excerpt of the bullets that matter):
> "* self_pin=1 … * live_collisions_agree=1 — the tool's collision set equals the counter's own independent extraction (0-3-space pattern) … * live_unmapped=0, live_verdict=refused — every colliding staged row carries a document, and the tool refuses its own naive arithmetic map; … * safe_map_admitted=1 — a by-document map (held rows dedupe to their registry id; new documents take ids at or above the safe floor) is admitted; * map_dedupe_live=1 …"

**Label — frozen tool, @07:52, `--rev 17f6ef0 --freeze 17f6ef0`:**
> `C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=13 selftest_failed=0 staged_rows=103 live_collisions=6 live_collisions_agree=1 live_held=2 live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=0 map_dedupe_live=1 safe_floor=S256 … C3_R43_PASS=false`

**Label — repaired counter, @07:57, same rev/freeze:** `self_pin=0 … safe_map_admitted=0 … C3_R43_PASS=false` — the counter stages the tool **from the rev**, and `17f6ef0` still holds the buggy blob, so this rev cannot reach `safe_map_admitted=1` regardless of the working-tree repair.

### F3.1 (HIGH, fixed at HEAD) The frozen tool could not admit any map with two or more entries
`tools/staged-id-guard.py:172` (frozen): `if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):` → the joined targets `S105S106S256S257S258S259` never match ⇒ `map_reasons=["map has a target that is not an S-id"]` ⇒ the counter's own six-entry by-document map was refused. Reproduced with the counter's exact construction:

```
safe = {'S153':'S105','S154':'S106','S155':'S256','S156':'S257','S157':'S258','S158':'S259'}
frozen tool  -> exit 1, map_ok=false, reasons=["map has a target that is not an S-id"]
HEAD tool    -> exit 0, map_ok=true, map_reasons=[], map_dedupe={'S153':'S105','S154':'S106'}, selftest 14/14
```

So the contract's "admits … a by-document map" was false as executed at the freeze; the predicate's `safe_map_admitted=1` was unreachable. A4 repairs it (the repaired tool admitted the map at 07:57).

### F3.2 (HIGH) "Refuses a colliding row with no document" has no predicate field
There is no `live_undocumented_refused` field. `live_unmapped=0` asserts the *data* has no undocumented collision (top-level `unmapped=[]`), and `selftest_cases>=13` aggregates the tool's own T2 case. The label cannot show the behaviour; a tool that deleted T2 and added two trivial cases would still print `selftest_cases>=13, selftest_failed=0`. **Contract component not tested by the predicate; only aggregated.**

### F3.3 (MEDIUM) "Admits **only** a by-document map" — the universal over maps is two instances
The counter feeds exactly one inadmissible map (the tool's own `naive_map`) and one admissible map (its own construction). No independent adversarial maps (a plausible document map that assigns held rows fresh ids, a below-floor partial map, a non-injective document map) are fed live; the tool's selftest covers three of those shapes (`T3_map_onto_registry_refused`, `T3_map_onto_staged_refused`, `T4_non_injective_refused`) but, again, only through the aggregate count. **Widening of "only".**

### F3.4 (MEDIUM) The 0-3-space claim is not discriminated by live data
The live registry has **0 rows with 1–3 leading spaces** (my regex count over `corpus/SOURCES.md`), and the tool's own output confirms `column0_miss=[]`, `column0_collisions == collisions`. A column-zero extractor would therefore agree with the counter exactly (`live_collisions_agree=1`) on this data. The only discrimination is the tool's selftest T1, one of 13 aggregated cases. **The label's `live_collisions_agree=1` is not evidence for "census-valid 0-3-space pattern".**

### F3.5 (LOW) "New documents take ids at or above the safe floor" — one instance, exactly at the floor
The safe map's four new ids are `S256..S259` with `safe_floor=S256` (equal to the tool's `max(registry)+1`); the counter never feeds a below-floor map live, so the floor rule is evidenced once, at its boundary, not as a rule.

### F3.6 (LOW) "Answers the … hazard **before any append**" — untested
No predicate field observes an append or its ordering; the tool is a read-only analysis, and the sentence's temporal clause is satisfied by construction, not by the counter.

### Quantifiers
- "every colliding staged row carries a document" — **enumerated** over the live staged set (`live_unmapped` computed from `doc['unmapped']`; 6 collisions); no flag.
- "admits **only** a by-document map" — **not enumerated** (F3.3).
- "new documents take ids **at or above** the safe floor" — one instance (F3.5).

---

## Severity summary

| # | Severity | Finding |
|---|---|---|
| F0 | blocking | Frozen instruments rewritten mid-wave (`17f6ef0` → `5cd2154`); `calibration/measure.py` and `tools/staged-id-guard.py` pinned by **neither** freeze at the 07:58 snapshot; `self_pin=0` for all three at `17f6ef0`; `frozen_before` and `amendments_note` now false |
| F1.1 | high | Frozen C1 killed on the dead-code fixture (K rule unimplemented) → label `killed=6 dead=0`, target unreachable; repaired at HEAD but only reachable at a post-A5 rev |
| F2.1 | high | `classes=7` is a literal presented as a measurement; the predicate sentence claiming "all seven ran" is unimplemented and contradicted by the same docstring |
| F2.4 | high | m10 exempted both ends of `supersedes` at the freeze, opposite to its sentence; three live pairs |
| F2.5 | high | "the lane's self-assessment records" enumerated over 3–4 texts; no `records` floor (round 42 required 6); `round-43.md` silently skipped |
| F3.1 | high | Frozen guard could not admit a multi-entry map → `safe_map_admitted=0`; claim false as executed, repaired at HEAD |
| F3.2 | high | "refuses a row with no document" has no field, only an aggregate selftest count |
| F1.2/F1.3 | medium | F11 kill attribution and the round-42 survivor provenance / "declaration unchanged" are true but untested |
| F2.2/F2.3 | medium | m12 bold-field sentence vs substring test (frozen); m13 mirror proves the counter's own regexes, not the cited command (persistent) |
| F2.6/F2.7 | medium | m8 lost `considerthese/` and the suffix gate vs "carried"; m11 repair accepts a tree as a "revision" (`4f3d8af5…` type=tree) |
| F1.4/F2.8 | low | Predicate sentence, code predicate, contract target and printed label carry three different field sets |
| F3.3–F3.6 | medium/low | "only", the 0-3-space discriminator, the floor and "before any append" are each single-instance or untested |

## Residual risk / verification gaps

- I could measure only `487b8f0` and `17f6ef0`. `5cd2154` is verified by **pin arithmetic only** (`pin == bytes at rev == disk` for C1 counter, C3 counter at 07:57, tool at 07:57); I did not run a counter there, and the working tree moved again after that check (`staged-id-guard.py` → `365bf958` at 07:58:28), so even that alignment is historical.
- The repairs in A4/A5 were validated by reading the code and by one manual tool invocation plus the frozen-counter comparison; I did not exercise `--control` (C1/C3) or `--probe-mutant` as controls, and `--selftest` only for C2/C3 indirectly through the counters.
- Whether C1/C3 will print `PASS=true` at the L1's deciding rev depends on that rev descending from the A4/A5 bytes **and** on all six pins matching at that commit. Neither holds at the 07:58 snapshot (`calibration/measure.py`, `staged-id-guard.py`).
- No tooling was installed; nothing outside `/tmp/tameshi-r43-RevReportDraft/` was written except this report.

---

# Addendum (08:06) — the contract text and the instruments moved; revised verdicts

The contract and all three counters were amended while this report was being written (A4–A10; `17f6ef0` → `5cd2154` → `114ffacd` → `53cb32b` → `273c047` → `c5335c7` → `3aee2c0` → `e20cf89`). Everything above quoted the **17f6ef0-era** bytes; this addendum states what is true at `e20cf89`/working tree and corrects two of my own statements.

## A0. The freeze chain and its pins, verified by hashing (no counter run)

| commit | amendments in its own contract | C1/C2/C3 pin == committed bytes | guard pin |
|---|---|---|---|
| `697d2f1` | — | OK / OK / OK | `8140945a` |
| `f0f2636` | A1 | OK / OK / OK | `8140945a` |
| `17f6ef0` | A1–A3 | OK / OK / OK | `8140945a` |
| `5cd2154` | A1–A5 | OK / OK / OK | `efa5f129` |
| `114ffacd` | A1–A7 | OK / OK / OK | `365bf958` |
| `53cb32b` | A1–A8 | OK / OK / OK | `365bf958` |
| `273c047` | A1–A9 | OK / OK / OK | `e219007f` |
| `c5335c7` | A1–A9 | OK / OK / OK | `e219007f` |
| `3aee2c0` | A1–A10 | OK / OK / OK | `2e8f2e89` |
| `e20cf89` | A1–A10 | OK / OK / OK | `2e8f2e89` |

So **every freeze's pins agree with its own committed bytes** (10/10 × 3) — `RevProvenance`'s diagnosis is right: a stale *pointer*, not a bad pin. Three defects remain in the contract's narration:

- **`frozen_before` names `114ffacd`**, but A9 (`273c047`) and A10 (`3aee2c0`) both postdate it and A9/A10 changed all three counters. A deciding run with `--freeze 114ffacd` therefore prints `self_pin=0` for C1, C2 and C3 (`RevProvenance` measured 0/0/0; my table explains why: the running bytes are the A9/A10 blobs, `114ffacd` pins the pre-A9 blobs). The last freeze whose pins match the running bytes is `e20cf89` (1/1/1 at the peer's run) — and at my 08:06 snapshot the disk had already moved again (`mutants/measure.py` = `b56a34d7…`, pinned by the *working-tree* contract only).
- **`amendments_note` is false in the sentence that matters**: "No amendment changes claims.\* (other than `counter_sha256` and the class sentences **restated verbatim**)". Diffed against `17f6ef0`, `claims.C2.classes` **m8, m10, m11, m12 and m13 all changed text**, and `claims.C3.statement` changed and grew. The note simultaneously says the class sentences changed and that they were restated verbatim.
- The disk churned through five guard-tool blobs (`8140945a` → `efa5f129` → `365bf958` → `e219007f` → `2e8f2e89`) and at least three calibration-counter blobs; at 07:58 `calibration/measure.py` (`52961c37…`) was pinned by *no* freeze. Pins agree again at 08:06, but only with the uncommitted working-tree contract.

## B. C1 corrections (supersedes F1.1's label line; adds F1.6)

- **The frozen counter also failed `tool_sha_ok`.** Frozen `mutants/measure.py:486` compares the census tool to `contract['tool_sha256']`, and at every freeze that key holds the **guard** blob (`8140945a` at `17f6ef0`); the census pin lives in `frozen_tools['tools/write-path-census-v4.py']` (`784de4c0`). Re-running the **frozen blob extracted to `/tmp`** with `--rev 17f6ef0 --freeze 17f6ef0` prints:

  ```
  C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=0 … mutants_killed=6 dead_code_only=0 … dead_code_arg_ok=0 kill_fixture_reachable=1 … C1_R43_PASS=false
  ```

  At the base rev the tool is absent (`tool_absent=1`), so `tool_sha_ok=0` at **both** permitted revs. Two independent blockers, exactly as `RevC1Counter` reported. **I withdraw the `tool_sha_ok=1` in my 07:52 in-lane capture**: I cannot reproduce it from the frozen bytes, the on-disk file was rewritten three times after it, and the reproducible value is 0. The 07:52 sample stays in §C1 only as a record of an unrepeatable state.

- **F1.6 (new) D is keyed on the fixture's source, not on the construct the mutant changed.** `differential()` assigns `'dead_code'` when `unreachable_statements(fixture_src)` is non-empty — anywhere in the fixture. A mutant that diverges on a *reachable* construct inside a fixture that happens to contain some unrelated dead code is therefore excused as `dead_code_only`. Combined with the unpinned `mutants.json` (F1.3), a re-declared entry under the same name that diverges on a different reachable fixture still passes: the name in the target is never bound to a kill site. `kill_fixture_reachable` stays a constant read off the F11 literal even on a run whose kill rests on F12 (my 07:52 label shows `kill_fixture_reachable=1` beside a kill list that included `method_fold_several_returns`).

- **F1.5 measured**: the frozen target listed **15** fields while the label printed **24** (+`C1_R43_PASS`); extras were `live_tool_errors, not_killed, runtime_error, apply_error, killed_names, dead_code_names, dead_code_cases, rev, freeze`, and the target's last two fields were in reverse order against the print (`kill_fixture_reachable, dead_code_arg_ok` vs `dead_code_arg_ok, kill_fixture_reachable`). **A11 did not close it**: the target now lists **16** fields (added `mutants_sha_ok`, `kill_binding`, dropped `kill_fixture_reachable`) while the label prints 26 named fields + PASS — 10 always-printed extras (`live_tool_errors, not_killed, runtime_error, apply_error, killed_names, dead_code_names, dead_code_cases, kill_cases, rev, freeze`) plus conditional `first_error`. Two order divergences remain: target puts `mutants_sha_ok` right after `live_unflagged_v4` (label prints it 24th, after `kill_cases`), and `kill_binding` before `dead_code_arg_ok` (label prints `dead_code_arg_ok` at :639 before `kill_binding` at :640). Still no verbatim target reproduction.

## C. C2 revisions

- **F2.9 (new, high) the statement now contradicts its own class.** `claims.C2.statement` is unchanged and still says "… m11 **revision reachability** … the five **round-42** classes"; `claims.C2.classes.m11` now reads:

  > "every 40-hex **object** cited by those records resolves in the lane (**object existence, not commit-only**)"

  My F2.7 (I probed a cited tree object `4f3d8af5…`: object-exit 0, commit-exit 128) is therefore no longer a hidden implementation slip — it is written into the class sentence while the claim sentence still says "revision". Top-level sentence ≠ class sentence, and "carried" is false for m11 and (still, F2.6) for m8.
- **Repaired to match their class sentences**: m12 (field form, not substring), m10 (only the superseded receipt is exempt), m13(a) (backticked `grep` cells only). m13(b) still proves the counter's own two regexes on its own mirror, never the cited command (F2.3 residual).
- **Persists**: `classes=7` is still `declared = 7` (`:440`, `:456`) while the predicate sentence still says "(all seven declared classes ran)" — the counter's own added prose now concedes the token is a constant, so the docstring contradicts itself. Record set still 3–4 texts with no floor (F2.5).

## D. C3 revisions (new F3.7; reverse gap)

- **F3.7 (new, high — the strongest single instance of this seat's defect)** A9/A10 enlarged `claims.C3.statement` with three behaviours:

  > "dedupes a staged row whose document the registry already holds **under any URL form (scheme, www., case, trailing slash)**, … **refuses a map that moves a held document off its registry id or decides an undocumented row**, and admits only a by-document map whose **every** fresh target is at or above the safe floor"

  The predicate sentence is **unchanged**: eleven bullets, and no bullet covers URL-form identity, held-off-id refusal, undocumented-row decisions, or "every" fresh target; `claims.C3.target` gained no field either. Those three behaviours are exercised only inside the tool's own selftest, which the counter consumes as the aggregate `selftest_cases>=13` (a count that would still be met with two trivial replacements). So the C3 claim sentence now claims strictly more than the counter tests — introduced by the very amendment wave intended to repair calibration.
- **Reverse gap**: the counter code/label gained `naive_agree`, `substitute`, `staged_sha256`; none appears in the predicate sentence or the target.
- **The tool repair is real, verified**: the repaired tool admits the counter's exact six-entry by-document map (exit 0, `map_ok=true`, `map_dedupe={S153:S105, S154:S106}`) and its selftest is 14/14; the frozen tool refused that map with "target that is not an S-id". But at `--rev 17f6ef0` the counter stages the *frozen* tool, so C3's label at the ticket freeze is false by construction; the claim is only reachable at a rev descending from the A6 tool.
- **Persists**: F3.2 (undocumented refusal has no field), F3.3 ("only" = one naive + one safe map), F3.4 (0-3-space not discriminated by live data: 0 indented registry rows, `column0_miss=[]`), F3.5 (floor evidenced once, at the boundary), F3.6 ("before any append" untested).

## E. Revised bottom line

1. **Nothing can be decided with `--freeze 17f6ef0` or `--freeze 114ffacd`**: `self_pin=0` for all three counters (measured: 17f6ef0 0/0/0 after the wave-1 edits; 114ffacd 0/0/0 per `RevProvenance`; my hash table explains both).
2. `--freeze e20cf89` reaches `self_pin=1` on all three, but the running bytes have since moved (`b56a34d7…`), so the deciding run must name a commit whose pins match the exact bytes it runs — and `frozen_before` must be rewritten to that commit, not `114ffacd`.
3. **Sentence = predicate today holds for**: C2 m6/m7, m12, m13(a), the repaired m10; C3's collision / held / naive-map / floor-shape bullets; C1's numeric core. **It fails for**: C2 `classes=7` (constant), m11 (statement vs class), m8 ("carried" but narrower), m13(b) (mirror misattribution), the record universal; C1's F11 attribution, round-42 provenance, "declaration unchanged", and the 15-vs-24 field mismatch; and C3's three new statement behaviours plus "before any append". That is the calibration finding this seat exists to return: the repairs fixed the *counters to their sentences*, then the *sentences were widened past the counters*.

# Addendum 2 (08:10) — A11 (`b510ad1`) and A12 (`bb36f80`); the gap narrows, then a pin breaks

Pin/body arithmetic extended (hash-only; no counter run):

| commit | amendments | C1 pin vs blob | C2 | C3 | guard |
|---|---|---|---|---|---|
| `b510ad1` (A11) | A1–A11 | OK `b56a34d7` | OK `97609511` | OK `ae66342d` | OK `2e8f2e89` |
| `bb36f80` (A12) | A1–A12 | **MISMATCH** pin `b56a34d7` ≠ blob `3d1ff3dc` | OK `97609511` | OK `47a6afce` | OK `2e8f2e89` |

- **A12 commits a broken C1 pin inside its own tree**: `sha(bb36f80:mutants/measure.py) = 3d1ff3dc` while `claims.C1.counter_sha256 = b56a34d7`, so `self_pin=0` *unconditionally* at `bb36f80`, not only for running bytes. The L1's own prerun receipt confirms it: `.ufo/evidence/round-43/prerun/c1-at-A12.stdout` prints `self_pin=0 … killed=5 dead_code_only=1 kill_binding=1 mutants_sha_ok=1 … C1_R43_PASS=false`.
- `frozen_before` still names `114ffacd` — stale a second time.

**Repaired since my first pass** (what was only claimed is now tested):

- **C1**: `mutants_sha_ok` (`:561-562`) pins the declaration blob at `claims.C1.mutants_sha256` (`b3abab06…`, the bytes I verified equal at base and freeze); `kill_binding` (`:601`) requires `outflag_no_parse_args_check`'s failing fixture to be exactly `['F11_outflag_namespace']`; `kill_cases` prints the per-mutant binding; `--probe-mutant` now distinguishes `equivalent`. F1.2 and the pin half of F1.3 are closed; the round-42 *survivor* provenance is still not read (only the declaration bytes are pinned). `kill_fixture_reachable` remains a constant read off the F11 literal — now informative, since `kill_binding` does the real work.
- **C3**: the target grew `held_refused=1 naive_agree=1 substitute=0`; the counter implements `held_refused` (`:261-270`, a real `--map` probe that moves a held row to `floor+50`), `naive_agree`, `substitute`, `staged_sha256`. One caveat: `held_refused` **defaults to 1** when `own_held` is empty (`:261`) — vacuous on a registry with zero held collisions; the live package has 3, so it did run (prerun `held_refused=1`, `C3_R43_PASS=true` at `bb36f80`).

**Still open at HEAD (the three artefacts still disagree)**:

- **C3's docstring predicate is still the original 11 bullets**: no bullet for `held_refused`, `naive_agree`, `substitute`, or the three behaviours A9/A10 wrote into the statement (any-URL-form dedupe; refusing a map that moves a held document off its registry id **or decides an undocumented row**; "every" fresh target ≥ floor). So *predicate sentence ⊊ code predicate ⊊ statement*: the code tests two of the three new claims (`held_refused`; URL-form identity only inside the normalized join, which the bullet describes as "dedupe by URL"), and the statement's "refuses a map that … decides an undocumented row" and "every" remain untested by any named field.
- **C2**: predicate sentence still says "(all seven declared classes ran)" beside `declared = 7`; `claims.C2.statement` still says "m11 **revision** reachability" while `classes.m11` says "40-hex **object**"; m13(b) still proves the counter's own regexes.
- **C2's content is presently red**, independent of the sentence question: prerun `c2-at-A12.stdout` shows `m7=5 m8=3 total=8` (first hit `corpus/lessons/round-43.md unknown S160`), `sources_rows=114`, `records=4`. Record repair, not counter repair, is needed before C2's `total=0` can hold.
- **Deciding-run precondition (unchanged, now harder)**: it must name a commit that (a) pins the exact bytes it runs — `bb36f80` cannot, since its C1 pin is broken — and (b) is named in `frozen_before`. Today no commit satisfies (a)+(b); A13 must do both.
