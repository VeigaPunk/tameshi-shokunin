# CriticPredicate — round 35, wave 2

## Scope and axes

Attacked `C1_R35_PASS` as an evidence predicate: public distinctness/cardinality, runtime-only kills, control identity, and sealed minima. Axes: **depth** (what class closure the evidence establishes), **calibration** (finite-sample success versus general closure), and identity/provenance integrity. No C2 measurement or judgment is claimed.

Reviewed the A4/A5 apparatus, not its superseded versions, at dispatch revision `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Read contract.json, both required wave-1 reports, round-34 Holds, and v3's docstring before probing. Frozen artifacts and checkouts remained untouched. Higher-priority bounds prohibited the requested clone/checkout; instead, every probe read committed objects through the absolute lane path. Scratch: `/fast/scratch/hyaku/tameshi-r35-w2/CriticPredicate/`. No git mutations, deciding C1 run, tool audit, agent/runtime dispatch, installations, or pacman operations.

**Result: no CRITICAL false-PASS demonstrated. One concrete fail-closed blocker; two evidence-hygiene gaps; the runtime-only rule remains conservative.** In particular, the current pinned tool cannot satisfy the current counter's deciding identity conjunct. The hypothetical passing assignments below are explicitly algebraic counterexamples to stronger interpretations, not C1 receipts.

## Evidence and exact commands

### E1 — committed bytes and unaltered-expression probe

Command, exit **0**:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/tameshi-r35-w2/CriticPredicate/predicate_probe.py
```

Probe SHA256: `0427ccb1d76982a2413b13768165fb079070ec343fad03280f9e5dd620851077`.

The script reads the frozen counter from the dispatch commit, parses its AST, and evaluates its **unaltered** `tool_sha_ok`, final `ok`, kill-row, and accept-row expressions. It never calls counter `main()`, `score_copies()`, the behavioral oracle, or the audit tool. For final-predicate examples it explicitly supplies assumed successful rows; these are not scored specimens. It also calls the real edit applicator and `distinct_bodies()` on committed panel JSONs and constructed clone lists.

Exact read-only Git commands issued by E1 (every command exited **0**, stderr empty):

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/c1/c1-measure.py
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/contract.json
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/tally-audit-v3.py
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/tally-audit-v2.py
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b -- .ufo/evidence/round-35/c1/panel
```

The last command's stdout SHA256 is `751ea8babca396c94c9bcbfc49751f6ea75fea58383289c83d94ea0ef8923323`. For each listed panel JSON, the exact command is the same `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:` followed by its repository path; E1 prints the complete argv and SHA for every file.

| Committed object | SHA256 |
|---|---|
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` |
| `.ufo/evidence/round-35/contract.json` | `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0` |
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` |
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `panel/cfg00-accept-swap.json` under C1 | `c5e5c65257235eb0c9e16dc9227182267bc1d8b85db0c280ab2f556bd3052d46` |
| `panel/comment-names-leg.json` under C1 | `e39a524babea863f918cd531ad834b81ca700b997492933f847ad592ed183a5a` |

All line pointers below are relative to the absolute lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin/` and these committed bytes.

### E2 — receipt/probe fingerprints

Command, exit **0**:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r35-w2/CriticPredicate/predicate_probe.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/control/c1-v2-control.stdout
```

Output:

```text
0427ccb1d76982a2413b13768165fb079070ec343fad03280f9e5dd620851077  /fast/scratch/hyaku/tameshi-r35-w2/CriticPredicate/predicate_probe.py
8e975158ac5eab2cd4049b6549326bff1ef1eef840b2b9dd170392ee54859750  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/control/c1-v2-control.stdout
```

The existing control receipt was read, not rerun; its line 9 says `mode=control`, `tool_sha_ok=1`, `pub_kill=0/5`, `pub_accept=0/3`, `pub_distinct=8`, and `C1_R35_CONTROL_PASS=false`. Its execution exit 1 is declared in contract.json:31; I did not independently execute that control.

## Findings, ranked

### BOUND-1 — stale duplicate tool pin makes deciding PASS unreachable

**Counterexample:** the correct, contract-pinned A4 tool itself. Counter line 46 still declares:

```text
TOOL_SHA256=da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f
```

Contract.json:11,109-111 and the actual committed tool instead name `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`. Counter:374 requires equality with the stale constant in deciding mode, and :445 makes it mandatory. E1 emitted:

```text
actual_v3_deciding_tool_sha_ok=False
ideal_counts_with_actual_v3_pin=False
```

The second line assumes every public/sealed score, count, validity, provenance, and runner pin is favorable; the real tool hash still forces the extracted final predicate false. This is a direct logical consequence, **not a claimed execution of the deciding run**. No specimen authoring can repair it while these frozen bytes remain.

Impacted axes: depth demonstrability and calibration/identity. **Fail-closed, not a false-accept and not evidence that the repaired tool lacks capability.** This is a fixable duplicated-authority defect, not a quality trade.

Smallest safe correction **before a new freeze/data boundary:** align the counter's expected tool digest with the contract's A4 digest, and require a preflight equality among contract digest, counter constant, and committed tool blob. Prefer one authenticated source of expected identity rather than independently maintained constants. **Do not silently edit this frozen counter or reinterpret `--tool` as a repair.**

### BOUND-2 — `failed == ['runtime']` is intentionally narrower than generic detection

Counter:305-310 requires behavioral divergence, exit 1, and exactly one failing check, runtime. E1 evaluated the actual kill-row expression:

```text
kill div=1 rc=1 failed=["runtime"] pass=True
kill div=1 rc=1 failed=["head"] pass=False
kill div=1 rc=1 failed=["runtime", "head"] pass=False
kill div=1 rc=2 failed=["runtime"] pass=False
kill div=1 rc=0 failed=[] pass=False
kill div=0 rc=1 failed=[runtime] pass=False
```

Thus an actual detected kill can fail the **runtime-isolation** target when another check also fires; a refusal never earns kill credit. This can produce conservative under-credit, not false class closure. V3:694-705 constructs all four check results, prints each once, then returns 0 iff all succeed; :833-840 maps handled inability to audit to exit 2. The pinned implementation gives no evidence here that a missing-check transcript can masquerade as a normal successful audit.

Impacted axes: depth and precision/calibration. Smallest safe pre-data strengthening is to retain runtime-only credit for this target and, if a broader detection claim is wanted, define a separate predeclared per-check stratum. Crediting head-only failures, arbitrary nonzero exits, or weakening equality to membership would change the target; that is not a safe correction to the frozen rule.

### HYGIENE-1 — `pub_distinct` is diagnostic, not a conjunct; slot totals are not family coverage

Counter:381-384 derives public denominators from whatever files exist at REV. The final predicate :445-449 contains **neither an eight-slot floor nor `pub_distinct`**. E1's AST name sweep confirms both `pub_distinct` and `ho_distinct` are absent.

Conditional algebra (authenticated tool and all non-public requirements assumed true):

```text
ideal_counts_with_authenticated_tool=True
clone_counts_distinct_2_2=True
empty_public_panel=True
```

The clone construction repeats the committed cfg00 kill five times and comment-names-leg accept three times; the actual `distinct_bodies()` returns **2**. Applied runner hashes for the two bodies are respectively `3b5061b130abc7e07b9a8fbb74e06e98fdf7fcc624316eea16f70a61cd3e189a` and `8c654bc71aa5f4877ddec3a52ee458a2af6668aaaacca5f6cc0e812901813b57` (E1). The zero-public example satisfies `0 == 0` for both public score equalities. **These are not permitted edits to the frozen panel, not actual C1 PASSes, and the stale pin blocks them in current deciding mode.** They show a counter alone does not enforce the prose's eight-copy premise.

Even simply adding `pub_distinct == 8` would not establish family diversity: E1 appends a uniquely numbered inert comment after `run_regression() {` to each of those eight copies and changes its free-form class label. Output:

```text
comment_padded_public_distinct=8
comment_padded_same_noncomment_tokens=True
```

The latter compares the real counter's comment-blanked token sequences to the two original constructions. Eight hashes are compatible with the same single kill mechanism; arbitrary `class` labels are printed (:289,312) but have no required coverage quota.

Impacted axes: depth/coverage inference and calibration. Smallest safe pre-data strengthening: freeze and enforce the exact public manifest (five kill, three accept, eight expected applied-body digests), rather than merely printing distinctness; predeclare independent route-family requirements if claiming family coverage. No finite body count alone proves universal routed-class closure.

### HYGIENE-2 — sealed minima count slots, while control `tool_sha_ok` changes meaning

**Sealed side:** counter:431-449 requires at least four kill slots and two accept slots but does not require distinct bodies, novelty relative to the public panel, or a fixed route-family matrix. E1 repeats the same cfg00 kill four times and the same comment accept twice; `distinct_bodies()` returns **2**, with the same two applied-body hashes above. The final predicate's successful-count assignment remains true when diagnostic `ho_distinct=2`. [INFERENCE] Independently authored post-freeze specimens could also converge on those same mechanisms; ancestry does not provide semantic diversity. No sealed files were created and no provenance success was fabricated. This does not falsify the literal finite-set claim; it defeats treating six slots as six independent tests or universal class closure.

Smallest safe pre-data strengthening: count unique applied-body digests per polarity; reject duplicates within sealed and exact public replays if novelty is part of the claim; freeze a modest route-family quota independently of author-supplied labels. A4/A5's fixes should remain intact. These would be future rules, not additions to the frozen round-35 predicate.

**Control side:** :366-374 makes `tool_sha_ok` true for **any present explicitly selected tool**, even the predecessor. E1, using actual committed bytes, emitted:

```text
explicit_v3_control_tool_sha_ok=True
explicit_v2_control_tool_sha_ok=True
control_without_seals=False
```

Thus `tool_sha_ok=1` in control output means selection/presence, not identity with the claimed v3. This is a naming/provenance hazard, **not an observed C1 bypass**: :367 changes the label to `C1_R35_CONTROL`; :455 also prints `mode=control`; omitting seals still fails the four/two minima. The existing control receipt corroborates that separation (E2).

Smallest safe pre-data strengthening: always print the actual full selected-tool digest, distinguish `control_tool_present` from a digest-match field, and compare control bytes to the frozen predecessor pin when calling that run the predecessor control. Never translate a `C1_R35_CONTROL_PASS` label into `C1_R35_PASS`.

## What I could not break — bounded proofs

- **The actual public panel's distinctness:** E1 read committed JSON at the dispatch revision, applied every edit at its required count, and emitted `actual_public_counts kill=5 accept=3 distinct=8`; every actual edit application was true. The clone/empty examples are not present in this panel.
- **The four/two floor and validity gates:** with all other final-expression terms favorable, E1 emitted `seal_only_3_kill=False`, `seal_only_1_accept=False`, `one_invalid_seal=False`, and `provenance_false=False`.
- **All-specimen score equality:** under the same favorable assumptions, `one_public_kill_missed=False`. Slot duplication cannot excuse an actual miss among loaded copies.
- **Runner identity:** the committed runner hash equals `PIN_RUNNER`; E1 also emitted `runner_pin_false=False` for the final-expression mutation of that input.
- **Accept polarity:** extracted accept expression gives `accept div=0 rc=0 pass=True` and `accept div=1 rc=0 pass=False`; observed divergence cannot be credited as acceptance by that row rule.
- **Runtime-only refusal protection and mode separation:** proved by the truth table and fixed source paths above. No rc2 or head-only kill was credited; no control output was presented as C1.
- **A current deciding false-PASS:** not established. The opposite is established for the prescribed tool bytes: `tool_sha_ok=False`. No deciding run was consumed. A5 provenance was read but not independently re-attacked in this slice; no proof of universal authorship or universal vector equivalence is claimed.

## Boundary for the canonical decision

Keep the finite statement separate from its stronger gloss. The exact predicate, once its pin problem is addressed in an authorized future freeze, can certify agreement on the loaded specimens and sampled oracle domain. It cannot, from distinct counts and four/two minima, certify every member of every routed family. The present identity defect is repairable; admitting closure by relabeling a control, dropping runtime isolation, or equating slot count with independent coverage would instead weaken the claim's evidence. No frozen rule was changed by this review.
