# ConnectorOverlap — round 33, wave 1

**Overlap found: three committed method imports, not competing ownership.** One bounded proposal follows; no C1/C2 verdict, integration, or admission is asserted.

Axes: this seat addresses **adjacency**; the proposed import supports C1 **operability** evidence. C2 **freshness** remains untouched. These are not measured axis gains.

## Evidence

Paths below are relative to `/home/vgpnk/Projects/shokunin/`; `@` names the last commit changing that report, resolved within a pinned sibling revision. The cited working-file bytes matched the committed Git blobs. Sibling experiments were read, not rerun; no sibling scratch directory was opened.

| Committed path@hash | What Tameshi could import |
|---|---|
| `mado-shokunin/.ufo/waves/round-27/w1/reports/CritC2Counter.md@b6650d583924d670c9e98594ffb1c6f25e8e7682` | Lines 22–42, 54–62: recognizable benign edits permit a normalized source-pin classifier; use independently justified positive alternatives and state the observable equivalence projection. |
| `kotoba-shokunin/.ufo/waves/round-60/build/MutC1Counter.md@7b80ae80cda69a95b6fc90879395113a99a57912` | Lines 10–13, 58–73: keep semantic equivalents separate from behavioral mutants, and distinguish diagnostic-text kills or direct assertions from a changed end-to-end decision. |
| `kake-shokunin/.ufo/waves/round-42/w1/MutRegexPct.md@1e1da6975dfb592f014253b8597c90a7008ae50c` | Lines 19–34, 38–40: a concrete CLI witness exposed a Unicode-digit defect missed by both generated comparisons, while a regex-only difference was masked downstream; require witnesses at the actual judged boundary. |

Discovery covered fleet `.ufo/reports/round-3*/` and `.ufo/waves/`, the six named sibling rounds, and direct runner references throughout each sibling's `.ufo/waves/**/*.md`. Searches used `mutate-and-run|--regression|tally-audit` and `sealed|held[ -]out|mutation|mutant|differential|false.positive` with case-insensitive matching and ignored files included. Other hits included Mado's read-only runner consumption, Kama's control-versus-mutation distinction, Chousa's failed-pristine qualifications, and Kumitate's targeted-versus-incidental rejections. This is a selected import set, not a claim that every broad search result was reviewed or that no other overlap exists.

### Exact read-only command evidence

All commands ran from `/fast/scratch/hyaku/tameshi-r33-seats/ConnectorOverlap/`, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset and `GIT_OPTIONAL_LOCKS=0`. Each following captured exit file was read and contained `0`; stderr was empty.

```sh
timeout 20s git --no-optional-locks -C /home/vgpnk/Projects/shokunin/mado-shokunin log -1 --format=%H 86f7355baed981acb060eb0b813b86904f9b885b -- .ufo/waves/round-27/w1/reports/CritC2Counter.md; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/ConnectorOverlap/last-mado.exit
# stdout: b6650d583924d670c9e98594ffb1c6f25e8e7682

timeout 20s git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kotoba-shokunin log -1 --format=%H 79cf263800552812ce6a45f4bb0313668b576749 -- .ufo/waves/round-60/build/MutC1Counter.md; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/ConnectorOverlap/last-kotoba.exit
# stdout: 7b80ae80cda69a95b6fc90879395113a99a57912

timeout 20s git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kake-shokunin log -1 --format=%H 61046fcffa23898cd93b7a5a0af4906dac9926c9 -- .ufo/waves/round-42/w1/MutRegexPct.md; echo $? > /fast/scratch/hyaku/tameshi-r33-seats/ConnectorOverlap/last-kake.exit
# stdout: 1e1da6975dfb592f014253b8597c90a7008ae50c
```

Full commands and raw outputs, including `ls-tree` and matching work-file `hash-object` results, are retained in `/fast/scratch/hyaku/tameshi-r33-seats/ConnectorOverlap/git-receipts.json:63-124`. Matching blobs were Mado `c0bfed617f71b6f085eea092cd085cad36900087`, Kotoba `e9bd2b41a58c2ab9c7761a1e145cb22aa0088c1f`, and Kake `31335e5e07b1dadc8cd0ab58ec32008c20b517fa`. These checks establish the report bytes cited here, not their experimental conclusions.

## Smallest safe correction: one paired witness card

**Proposal only:** attach a projection-aware paired witness card to each existing C1 development finding, using its already captured evidence. Pair the faulty runner with a behavior-preserving alternative sharing the relevant structural nuisance where available. Record runner hashes, the independent semantic argument or concrete status-vector witness, expected and observed `(exit, first stdout line)` for the tally, and the auditor's `(exit, final stdout label)`. Mark missing evidence as unestablished rather than inventing a pair or counting a diagnostic change as behavioral sensitivity.

[INFERENCE] This combines Mado's positive-control lesson with Kotoba's attribution discipline and Kake's final-boundary witness: it can distinguish a syntax recognizer that rejects unfamiliar correct copies from an audit that identifies the intended tally fault. No sibling implementation, product gate, or experimental result transfers to Tameshi.

### Second-order effects and contradictions

- **Runtime:** this is an evidence overlay, not another sweep. It adds no invocation to the frozen tool or runner. A correct first line and exit are separate from stderr, incidental later output, or an instrumentation failure.
- **Contract:** `.ufo/evidence/round-33/contract.json:18,23,38-44` fixes the predicate and control-before-held-out ordering. Cards do not amend validity, drop difficult rows, lower thresholds, repair tool bytes, or authorize another counter run.
- **Important incompatibility:** `c1/c1-measure.py:171-183` applies the same witness screen to both sets: a vector must demonstrate a changed tally outcome; `kind=head` only demonstrates changed pre-tally bytes. An output-preserving tally-only refactor therefore cannot use that vector route. Do not mechanically transplant Mado's green population, pad a head edit to satisfy validation, or call a head difference proof of semantic equivalence. Such a case remains development evidence unless independently valid under the existing rule.
- **Different kill contracts:** Mado's report at lines 101–107 describes counting any nonzero suite exit, including unrelated setup failures. Tameshi C1 instead requires exit 1 plus final `TALLY_AUDIT: FAIL` (`c1/c1-measure.py:197-205`). Import the witness method, not that adjudication rule.
- **Substrate:** retain the existing sandbox and stdout-only boundary; introduce no live sibling paths, shared state, new tools, or access to sealed material. This connector neither authored nor opened round-33 held-outs.
- **Verification and freshness:** preserve raw outcomes beside the interpretation. A card cannot establish universal equivalence or generator independence. The S055 replacement row, versioned URL, snapshot, and C2 counter are unaffected.

## Risks and verification

Risk: paired cases can share the same mistaken generator, and a surviving edit may be equivalent or masked rather than a missed fault. Independent semantic reasoning and an observable witness address different questions; neither substitutes for the other. Existing evidence may not support a complete pair, which must stay explicit.

For the L1's evidence review, check each card against the existing raw receipts and the frozen stdout/exit projections, retain diagnostic-only and unestablished cases separately, and confirm any eventual held-out file satisfies the unchanged validator and ordering. This proposes no additional default-mode measurement. Runtime improvement and general specificity were not exercised here.

Only discovery reads, bounded read-only Git commands, scratch receipts, and this report were produced. No production edits, Git writes, jj commands, tests, counters, audit-tool runs, model calls, or other agent runtime were performed. All started commands completed; no owned process tree remains. Tools installed or updated: none.

Report: .ufo/waves/round-33/w1/ConnectorOverlap.md
