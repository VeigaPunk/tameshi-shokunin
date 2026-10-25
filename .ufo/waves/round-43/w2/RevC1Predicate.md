# RevC1Predicate — C1 predicate re-derived from the counter and the contract sentence

Seat: `L1Tameshi43.RevC1Predicate` (wave 2, falsify). Item: list every field the C1 predicate
requires and the code line that produces it; report any required field produced by a constant, any
field printed but not required, and whether `mutants_killed=5 dead_code_only=1` is reachable while a
different mutant set is declared.

**Objects of record**

| object | bytes | note |
|---|---|---|
| counter of record (freeze) | `.ufo/evidence/round-43/mutants/measure.py` @ `3aee2c078f8976499b587086af3577fc94dc8cf1`, `sha256 0d0f81bdbe09bb53997ade30911fc178a38de072f84aacf23c6c9c0a710e57f1` | matches `claims.C1.counter_sha256` |
| contract | `.ufo/evidence/round-43/contract.json` @ freeze, amendments A1–A10 | A10 is the last amendment; **no A11** |
| lane worktree counter | `sha256 3d1ff3dc6b75658dfbb5ada11a310ff3067144ae11bd30c8cc4147ad40eed8c0` (snapshot) | **dirty, mid-edit by L1**; see §7 |
| mutant declaration | `.ufo/evidence/round-42/census/mutants.json`, `sha256 b3abab06a48d41535aa35bc520d0884489cb684a7a52b5369c2aadc3db430358` | **identical at base and freeze**, and named by no contract field |

Base `487b8f0…` does not contain `.ufo/evidence/round-43/` at all, so the counter's predicate line
is a freeze-only object; every line number below is from the freeze blob (`0d0f81bd`).

---

## 0. Sentence → predicate decomposition

C1's `statement` carries five separable propositions; only three reach code as predicates:

| id | sentence fragment | predicate term |
|---|---|---|
| S1 | "the two survivors of the round-42 mutant set" | **none** — the set is never identified |
| S2 | "`outflag_no_parse_args_check` is killed by a new reachable-code fixture (`F11_outflag_namespace`)" | name membership only (L623) + a constant (L589–591) |
| S3 | "`method_fold_several_returns` is classified dead_code_only … with a differential probe" | `dead_arg_ok` (L588→L625), membership (L624) |
| S4 | "five killed and one dead-code-only and zero unresolved" | `len(killed)==5`, `len(dead_code_only)==1`, `unresolved==0` (L621–622) |
| S5 | "with the round-42 mutant declaration unchanged" | **none** — count only (L620) |

So the predicate enforces S3 and S4 fully, S2 and S5 nominally. Findings F1 and F2 are exactly S2
and S5.

---

## 1. Every field the predicate requires, and the line that produces it

`passed` is L617–L638 (18 conjuncts). Each printed field that enters it:

| # | field | producer (freeze line) | term | how it is produced |
|---|---|---|---|---|
| 1 | `self_pin` | 489, 493 | 617 | `sha(contract-pinned blob at freeze) == pin` **and** `sha(running file) == pin` |
| 2 | `tool_absent` | 496 | 617 | `tool_raw is None → 1`; the tool exists at base and freeze, so 0 by construction |
| 3 | `tool_sha_ok` | 499 | 617 | `sha(tools/write-path-census-v4.py @ rev) == frozen_tools[TOOL_REL]` |
| 4 | `selftest_exit` | 507 | 618 | exit of `tool --selftest` |
| 5 | `fixtures_pass` (`%d/%d`) | 342, 360, 598 | 618 (`== len(FIXTURES)`) | measured; denominator is the 12-key `FIXTURES` constant |
| 6 | `run_errors` | 353, 365, 599 | 619 (`not errors`) | measured |
| 7 | `live_ok` | 361, 366, 371, 600 | 619 (`all`) | measured over the 3 `LIVE` coordinates |
| 8 | `live_unflagged_v4` | 549, 601 | 619 (`== 0`) | measured over every `tools/*.py` at rev (27 files at freeze) |
| 9 | `live_tool_errors` | 446, 549, 602 | 620 (`live_errors == 0`) | measured — **required but absent from the contract target** |
| 10 | `mutants_declared` | 554, 603 | 620 (`len(mutants)==6`) | `len()` of an **unpinned** input |
| 11 | `mutants_killed` | 572, 604 | 621 | measured |
| 12 | `dead_code_only` | 582, 605 | 621 | measured |
| 13 | `equivalent` | 578, 606 | 622 (`not equivalent`) | measured |
| 14 | `unresolved` | 587, 610 | 622 (`== 0`) | derived: `len(not_killed)+len(runtime_error)+len(apply_error)` |
| 15 | `killed_names` | 585, 611 | 623 (`KILL_NAMES ⊆`) | **name strings from the unpinned declaration** |
| 16 | `dead_code_names` | 586, 612 | 624 (`DEAD_CODE_NAMES ⊆`) | name strings from the unpinned declaration |
| 17 | `dead_code_cases` | 583, 613 | 588→625 | measured differential, exact list |
| 18 | `dead_code_arg_ok` | 588, 615 | 625 | `dead_code_cases[method_fold] == ['F12_method_two_returns']` |
| 19 | `kill_fixture_reachable` | 589–591, 616 | 625 | **constant** (§2) |

Accounting is tight: each mutant lands in exactly one of killed / dead_code_only / equivalent /
not_killed / runtime_error / apply_error (L570–583, `continue` at 564/573), so 5+1 with the rest zero
partitions all six declared mutants. Nothing escapes accounting; the hole is identity, not counting.

## 2. Required fields produced by a constant (or by construction)

### F1 — HIGH — `kill_fixture_reachable` is a pure function of the `FIXTURES` constant

```python
589  kill_fixture = FIXTURES.get('F11_outflag_namespace')
590  kill_fixture_reachable = 0 if (kill_fixture is None or unreachable_statements(
591      kill_fixture[0])) else 1
```

`FIXTURES['F11_outflag_namespace'][0]` is a triple-quoted literal (L206–L222). The expression reads
no tool, no mutant, no rev, no freeze: it is `1` for every run of these bytes. It is required at
L625 and is one of the 16 terms in the contract's target line. S2's operative phrase — *"is killed
**by** a new reachable-code fixture (F11)"* — is therefore not tested at all; the field only
restates that F11's own source text has no statement after an unconditional `return`/`raise`.

**Proof (executed).** A mutant *named* `outflag_no_parse_args_check` but carrying
`attr_bind_several_assignments`' edit is killed by an attr fixture, F11 never appears, and the frozen
counter still prints `kill_fixture_reachable=1 C1_R43_PASS=true`, exit 0:

```
C1_R43: self_pin=1 … mutants_killed=5 dead_code_only=1 … dead_code_arg_ok=1 kill_fixture_reachable=1 … C1_R43_PASS=true
### INTROSPECT outflag_no_parse_args_check apply_count=1 fails=1 errors=0
###   failing_cases=[('F03_attr_ambiguous', False)]
```

The honest set does satisfy the sentence — its `outflag_no_parse_args_check` fails
`[('F11_outflag_namespace', False)]` — so the claim is true **de facto** and unfalsified **by the
code**. That is precisely the sentence=code gap: a true sentence attested by a constant.

### F2 — HIGH — the mutant declaration is unpinned; identity is a name string

C1 reads the declaration at rev (L551–L554) and the predicate uses only `len(mutants)==6` (L620) and
name membership (L623–624). There is **no sha256 of `mutants.json` anywhere**: not in the counter
(grep: `mutants_sha` absent from the freeze blob), not in the contract (`claims.C1.mutant_set` is
prose, `"… at REV, unchanged (six mutants, classes attr/method/outflag)"`). `KILL_NAMES` and
`DEAD_CODE_NAMES` are module constants (L248–249) matched against names the declaration supplies, so
the declaration author decides which edit each pinned name carries. The declaration already carries a
`class` field (`attr`/`method`/`outflag`) that the counter never reads.

### F3 — MEDIUM — `tool_absent` and `self_pin` carry no information for a permitted run

- `tool_absent` (L496): `tools/write-path-census-v4.py` exists at base and at freeze
  (`sha256 784de4c0…` at both), so this term is 0 for every permitted `--rev`.
- `self_pin` (L489–493): compares the counter blob at `--freeze` with a pin stored in the contract at
  the same `--freeze` commit. It attests *bytes match the contract*, never *contract matches the
  sentence* — a lane that freezes a wrong predicate and pins it gets `self_pin=1` (this round: the
  pin and `kill_fixture_reachable=1` travelled together). `tool_sha_ok` (L499) has the same shape but
  at least pins a third-party artifact by content.

## 3. Fields printed but not required

| field | line | status |
|---|---|---|
| `rev` | 626 | printed, never compared to `contract.base_rev` or `frozen_before`; no rev-membership check anywhere |
| `freeze` | 627 | printed, never compared to `contract.frozen_at`/ancestry |
| `first_error` | 629–630 | printed only when `errors` is non-empty, i.e. only when the predicate is already false — diagnostic |
| `C1_R43:` | 593 | label |
| `not_killed`, `runtime_error`, `apply_error` | 607–609 | not named in `passed`, but jointly required via `unresolved` (L587→L622); printed so a reader can decompose it |
| `killed_names`, `dead_code_names`, `dead_code_cases` | 611–613 | **required** (L623–624, L588) but **absent from the contract target** |

### F4 — MEDIUM — the declared target line is not the predicate's field set

Contract target names 15 terms; the predicate has 18 conjuncts (19 fields, `live_ok`+`fixtures_pass`
render as pairs). Missing from the target: `live_tool_errors` (required at L620), `killed_names`,
`dead_code_names`, `dead_code_cases`. The target also orders `kill_fixture_reachable=1
dead_code_arg_ok=1` while the counter prints `dead_code_arg_ok=1 kill_fixture_reachable=1`, so the
target is neither a substring nor an ordered subsequence of any honest output (verified against the
freeze run below). The target's one distinctive field is the constant of F1.

Honest freeze run (control, this seat, the only permitted measurement rev):

```
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12 run_errors=0
live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=5
dead_code_only=1 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0
killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,
outflag_dests_never_recorded,outflag_no_parse_args_check
dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns
dead_code_arg_ok=1 kill_fixture_reachable=1 rev=3aee2c0… freeze=3aee2c0… C1_R43_PASS=true
```

## 4. Is `mutants_killed=5 dead_code_only=1` reachable with a different mutant set declared?

**Yes — proven twice, with `C1_R43_PASS=true` and exit 0, on byte-identical frozen counter bytes
(`self_pin=1`), at the permitted freeze rev.** The harness swaps only the `MUTANTS_REL` read; every
other byte and every other input is the record.

Pass 2 — four names that never existed, all five "kills" carrying one real edit:

```
mutants: phantom_k1..k4 + outflag_no_parse_args_check  (all five = outflag edit)
         + method_fold_several_returns (real)
--->
mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 unresolved=0
killed_names=outflag_no_parse_args_check,phantom_k1,phantom_k2,phantom_k3,phantom_k4
dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns
dead_code_arg_ok=1 kill_fixture_reachable=1 C1_R43_PASS=true   (rc=0)
```

Pass 3 — the round-42 survivor's edit is **absent**; its name carries an attr edit:

```
mutants: phantom_a1..a4 + outflag_no_parse_args_check (all five = attr_bind edit)
         + method_fold_several_returns (real)
--->
mutants_killed=5 dead_code_only=1 equivalent=0 unresolved=0
killed_names=outflag_no_parse_args_check,phantom_a1..a4
kill_fixture_reachable=1 C1_R43_PASS=true   (rc=0)
```

Consequence: the predicate cannot distinguish *"the round-42 survivor was killed"* from *"a mutation
bearing the survivor's name was killed"*, and cannot distinguish *"the round-42 six"* from *"some
six"*. S1 and S5 are unenforced; the count is real, the identity is nominal.

## 5. Residual risks not covered by a predicate term

- **R1 — unpinned live corpus.** `stage()` (L429–439) writes every `tools/*.py` at rev; the three
  live sites (L251–259) and `lane_unflagged` (L441–449) read them. `frozen_tools` pins only
  `write-path-census-v4.py` and `staged-id-guard.py`. `tools/context-capture.py`
  (`sha256 c4a1d165…`) and `tools/registry-replay.py` (`sha256 9fcd2dbb…`) are identical at base and
  freeze but **unpinned**, so `live_ok`/`live_unflagged_v4` are measured on content no pin names.
  Combined with the unvalidated `rev` (§3), a run at an arbitrary rev can pass with a doctored live
  corpus. [INFERENCE from L251–259, L429–449, L496–L499; not executed, because only `--rev` base and
  freeze are permitted to this seat.]
- **R2 — D/E corpus asymmetry.** `differential()` (L471–484) iterates `FIXTURES` only, never the live
  files, while K's battery includes them. A mutant whose only divergence is on a live file falls to
  `equivalent` (L578) — the E sentence says "over the declared corpus", so the corpus is ambiguous
  and the dead-code classification ignores live evidence.
- **R3 — strict-bind false negatives.** Once kill provenance is bound (see §6), the binding compares
  the *whole* reachable failing-case list, so a survivor that also fails a live site is refused.

## 6. Verification method and gaps

- Executed: the frozen bytes at `--rev`/`--freeze 3aee2c0…` (honest, PASS=true, rc=0); the same bytes
  with only the declaration read swapped (passes 2 and 3); per-mutant introspection of the honest
  six and of the fabricated `outflag` entry; byte checks of the tool, the declaration and the two
  live files at base and freeze.
- Not executed: any counter run at a rev other than base/freeze (bound); the patched counter
  end-to-end (it cannot pass before the contract amendment, §7); no lane write, no git mutation, no
  jj command.
- No language server applies to this Python counter in the lane; caller/definition checks were done
  by reading the freeze blob with line numbers plus execution, not by `lsp`.
- Scratch used and removed: `/tmp/tameshi-r43-w2-RevC1Predicate-*`, `/tmp/tameshi-r43-c1-*`,
  `/tmp/honest-*`. Harness and fabricated declarations are reproduced in the appendix so the two
  proof runs are re-runnable without the scratch tree.

## 7. The in-flight repair (snapshot `3d1ff3dc`) and what it still needs

The worktree counter now adds `mutants_sha_ok` (L562) and `kill_binding` (L601), prints
`kill_binding`/`kill_cases`/`mutants_sha_ok` (L626–629) and requires both (L638) — i.e. the two
defects F1/F2 are being closed. Three conditions must hold before it is frozen:

1. **The contract must gain the pin, or the predicate is false.** `mutants_sha_ok` reads
   `claims.C1.mutants_sha256` (L562); the contract at freeze has no such key →
   `want_mutants=None` → `mutants_sha_ok=0`. Measured:
   `declared mutants_sha256 in contract: None`; `actual sha at freeze = b3abab06…` (equal at base).
   A11 must add `"mutants_sha256": "b3abab06a48d41535aa35bc520d0884489cb684a7a52b5369c2aadc3db430358"`;
   a reviewer must check that the pin equals the **base-rev** blob sha, otherwise it is the same
   mutual attestation as `self_pin`.
2. **The target line must be rewritten and `counter_sha256` moved.** `kill_fixture_reachable`
   disappears from the output; `kill_binding`, `kill_cases`, `mutants_sha_ok` appear. The C1 target
   as frozen (`… kill_fixture_reachable=1 dead_code_arg_ok=1`) will match nothing printed.
3. **State the strictness.** `kill_binding` requires `kill_cases[outflag] ==
   ['F11_outflag_namespace']` exactly; a survivor failing F11 *and* another reachable case is refused
   (R3). Safe direction, but the sentence should say "killed by F11 alone" if the code says it.

### Answers, in one line each

- **Required fields:** 19, table in §1 — `self_pin`, `tool_absent`, `tool_sha_ok`, `selftest_exit`,
  `fixtures_pass`, `run_errors`, `live_ok`, `live_unflagged_v4`, `live_tool_errors`,
  `mutants_declared`, `mutants_killed`, `dead_code_only`, `equivalent`, `unresolved`, `killed_names`,
  `dead_code_names`, `dead_code_cases`, `dead_code_arg_ok`, `kill_fixture_reachable`.
- **Required field from a constant:** `kill_fixture_reachable` (L589–591) is a pure function of the
  `FIXTURES` literal; `tool_absent` (L496) is 0 by construction at every permitted rev; `self_pin`
  (L489–493) is 1 for any self-consistent freeze.
- **Printed but not required:** `rev` (L626), `freeze` (L627), `first_error` (L629–630), the
  `C1_R43:` label (L593); `not_killed`/`runtime_error`/`apply_error` are required only through the
  `unresolved` sum. Conversely `live_tool_errors`, `killed_names`, `dead_code_names` and
  `dead_code_cases` are required but missing from the declared target.
- **Different mutant set reaching 5/1:** yes — two executed proofs, both `C1_R43_PASS=true`, exit 0,
  `self_pin=1`, one of them with the round-42 survivor's edit entirely absent.

---

## Appendix — reproduction

Freeze the objects first (`S=$(mktemp -d)`):

```
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FREEZE=3aee2c078f8976499b587086af3577fc94dc8cf1
git -C $LANE show $FREEZE:.ufo/evidence/round-43/mutants/measure.py > $S/measure_frozen.py
sha256sum $S/measure_frozen.py   # 0d0f81bdbe09bb53997ade30911fc178a38de072f84aacf23c6c9c0a710e57f1
```

Honest run (the permitted measurement rev):

```
python3 $S/measure_frozen.py --lane $LANE --rev $FREEZE --freeze $FREEZE
```

Swapped-declaration run (`drive.py` in `$S`; run from `$S` so `import measure_frozen` resolves):
`run()` swaps `M.show` for `MUTANTS_REL` only and leaves every other read on the record; `main()` is
the frozen `main`. Pass 2 uses `mutants_a.json`, pass 3 uses `mutants_b.json` — both six entries with
one edit repeated five times plus the real dead-code edit:

```python
import os, sys
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
import measure_frozen as M
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '3aee2c078f8976499b587086af3577fc94dc8cf1'
ORIG = M.show
def run(swap):
    fab = open(swap, 'rb').read()
    M.show = lambda lane, rev, path, _f=fab: _f if path == M.MUTANTS_REL else ORIG(lane, rev, path)
    sys.argv = ['measure_frozen.py', '--lane', LANE, '--rev', REV, '--freeze', REV]
    print('rc=%d' % M.main())
run(os.path.join(S, 'mutants_a.json'))
run(os.path.join(S, 'mutants_b.json'))
```

`mutants_a.json` (pass 2): five × `{"find": "if flag and _parse_args_ns(node.value, env, ctx, depth + 1, seen):", "replace": "if flag:"}`
named `phantom_k1..phantom_k4` and `outflag_no_parse_args_check`, plus
`{"name": "method_fold_several_returns", "find": "if len(returns) != 1:", "replace": "if len(returns) < 1:"}`.

`mutants_b.json` (pass 3): five × `{"find": "if len(vals) == 1 and not isinstance", "replace": "if len(vals) >= 1 and not isinstance"}`
named `phantom_a1..phantom_a4` and `outflag_no_parse_args_check`, plus the same dead-code entry.

Per-mutant kill provenance (the honest six and the fabricated `outflag`):

```python
body, count = M.apply_once(tool_raw.decode(), mut['find'], mut['replace'])
fails, errors, _, _, _, _, detail = M.battery(<mutant.py>, work)   # detail keys = failing cases
differ = M.differential(tool_path, <mutant.py>, work)               # 'reachable' | 'dead_code'
```

Recorded honest provenance: `outflag_no_parse_args_check → F11_outflag_namespace (reachable)`;
`method_fold_several_returns → F12_method_two_returns (dead_code)`;
`attr_bind_several_assignments → F03_attr_ambiguous (reachable)`.
