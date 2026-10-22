# ConnectorOverlap — sibling-overlap scan for C2 (oracle anchoring), round 27 wave 1

Seat: TameshiR27.ConnectorOverlap (connector, leaf, read-only). Judged on: adjacency.
Scan date: 2026-10-22. Kumitate head scanned: `f69817edf687c8ce4f87ed7953a353399232f69e`
(2026-10-22 09:28:19 -0300). Tools installed or updated: none.

## Verdict

Tameshi absorbs nothing. This scan is report-only.

1. **No newer cite-check revision.** No kumitate revision pins any of the four holes
   (S_OOR_EDGE, S_STRICT, S_USAGE, S_PIN_INCLUDES). `scripts/cite-check.mjs` at kumitate
   head is byte-identical to the pinned blob. Every kumitate Git ref that carries the
   file resolves to the same blob.
2. **No owner rule for pin prefixes.** Kumitate states no prefix rule for pins in any
   document outside the code. The only prefix behaviour is the code itself
   (`digest.startsWith(pin.hex)`), which is state, not specification. The entry's call
   that "S_PIN_INCLUDES is held by convention only" stands.
3. **No sibling vocabulary overlap.** No sibling lane holds S012 or the
   specification-anchored versus state-anchored split. The overlaps that do exist are
   adjacent, not duplicate.
4. **The holes were lost in routing (new finding).** Tameshi's round-26 closure routed
   five items to kumitate: the zero-resolved fixture and the four holes. Kumitate's
   round-39 spot-check transcribed only the zero-resolved fixture. The four holes are
   on no kumitate backlog.

## Evidence

### Kumitate: the cite-check revision

- `GIT_OPTIONAL_LOCKS=0 git -C kumitate-shokunin log --all --oneline -- scripts/cite-check.mjs`
  lists `1205c66` (round-30) as the newest commit that touched the file.
- `sha256sum scripts/cite-check.mjs` returns `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`.
  `git show 1205c66…:scripts/cite-check.mjs | sha256sum` returns the same value. This equals
  the S088 pin in `corpus/knowledge/oracle-anchored-survivors.md:1`.
- Of the 191 refs (`refs/heads/master` plus `refs/jj/keep/*`), 190 resolve
  `scripts/cite-check.mjs` to blob `9770de8c…`, the blob of `1205c66`. The remaining ref
  has no such path.
- `git status --porcelain scripts/cite-check.mjs` prints nothing, so the file has no
  dirty edit.
- `merge-base --is-ancestor 1205c66 HEAD` holds.
- The hermetic selftest in that blob still lacks each of the four witnesses:
  - `:1883-1886`: the `LINE_OOR` case uses `:999`, not line n+1.
  - `:1928-1932`: the `ORPHAN_REF` case asserts the warn severity but never runs with
    `--strict`.
  - No case runs an unknown flag. `rg "status === 64|--bogus" scripts/cite-check.mjs`
    returns no case.
  - `:1895-1899`: the pin mismatch token is `0123456789ab`. This is a non-matching
    token, not an interior slice of the digest.

### Kumitate: prefix rule for pins

- `cite-check.mjs:36-38` (header): a pin is a marker word, then "7-40 hex". Only the
  length is fixed. The header says nothing about prefix versus substring.
- `cite-check.mjs:1195` and `:1219`: `digest.startsWith(pin.hex)`. This is the code under
  mutation, so it is state-anchored by S012's definition.
- `SKILL.md:690-694` is the only owner prose on pin semantics: "a bare sha of a
  superseded revision in a corpus doc is read as a content pin of the nearest cited file
  and becomes a `PIN_MISMATCH` error the moment that file changes". It does not say
  whether a pin must be a prefix.
- A prefix search found nothing outside cite-check. The command was
  `rg -n '(digest|sha|hex|pin)[A-Za-z.]*\.(startsWith|includes)\(' scripts/*.mjs`. Its
  only other hit is a path prefix (`anchor-truth.mjs:529`), not a pin rule.
- Prose that talks about prefixes (`native-admission-detail.md:93`,
  `runtime-remainder-census.md:294`, `local-ship.md:211`) concerns the `sha256:` label
  prefix in UFO-FSD runtime digests. That is the leading label on a full digest, not the
  leading slice of a short pin.

### Kumitate: the routing loss

- `tameshi-shokunin/corpus/lessons/round-26-verifier-spotcheck.md:233-237`, item 7, reads:
  "add a hermetic case for a scanned document with zero resolved citations … plus the
  four lane-named holes: line n+1, `--strict` with one warning, unknown-flag exit 64,
  interior-slice content pin."
- `kumitate-shokunin/corpus/lessons/round-39-verifier-spotcheck.md:151-157`, item R39-5,
  cites only lines 172-179 of that lesson, the neighbour finding. It ends "Add a
  zero-resolved, no-drift fixture." None of the four holes appear.
- `rg 'S_PIN_INCLUDES|S_OOR_EDGE|S_USAGE|S_STRICT|S_EMPTY_GUARD'` across the sibling
  lanes finds no hit in kumitate. Its only hit is an unrelated shell variable at
  `souji-shokunin/tests/runner-23.sh:254`.
- `cite-check.mjs:1590` still reads
  `totals.filesScanned > 0 && totals.resolved > 0 && !drift`. Even the transcribed item
  has not landed.

### Kumitate: a second contract anchor for S_USAGE outside the blob

- `kumitate-shokunin/corpus/knowledge/round-close-gate.md:204-206` reads: "Same four-value
  shape as the three gates beside it (`cite-check.mjs`: 0/1/2/64; …)". Line `:202` reads:
  "64 | usage (unknown flag, …)" (that row is round-gate's).
- This is an owner document separate from the mutated file. It meets S012's "fixed
  outside the code under mutation" more strongly than header line 71. It partly answers
  the entry's bound at `oracle-anchored-survivors.md:78-80`: "not an independent
  specification document".
- No such outside-blob prose exists for the other three holes. `SKILL.md:599` lists
  `[--strict]` without semantics. `lessons/round-10.md:97` ("Warnings never gate without
  `--strict`") is about round-gate, not cite-check.

### Adjacent knowledge in other siblings (no duplicates)

| Lane, path:line | What it holds | Relation to C2 |
|---|---|---|
| `chousa-shokunin/corpus/lessons/round-24.md:80-82` | "A test oracle can lie in the same way as the code": GNU grep reads NUL as a line break | Shows an oracle that shares the subject's failure mode, the risk S012 names. Has no anchoring vocabulary. |
| `kake-shokunin/scripts/freshness-sweep.mjs:1434-1439` | selftest case `d unknown flag -> exit 64`, `pass: r.code === 64` | The exact witness cite-check's selftest lacks (S_USAGE). A house precedent, not a cite-check pin. |
| `kake-shokunin/corpus/QUALITY.md:113-116` | the output contract covers every exit path, including usage errors | A quality rule adjacent to S_USAGE. |
| `audio-shokunin/reports/round-97/r97-boundary.md:295` | `wpexec` observed exiting rc 64 "(EX_USAGE)" | A third-party tool that behaves as S090 describes. Observation only, in a report rather than the corpus. |
| `game-dev-2d-shokunin/corpus/lessons/r103-receipt-shape-gate.md:35-36` | "`signature` is a **prefix-substring pin**", matched by `signature in output` | A fleet gate that declares substring containment legal for its pins. This bears out the entry's point (`:62-63`) that an owner could declare substring pins legal. It is a different object (an output-line signature), not a content digest. |
| `kagi-shokunin/SCORECARD.md:71`, `corpus/knowledge/claim-ledger.md:75-82,179-182` | "anchored expectations" | Means a regular expression anchored to the last line. This is a term collision, not oracle anchoring. |
| `kotoba-shokunin/corpus/knowledge/corpus-integrity-round11.md:207-210` | "equivalent mutants" as inputs the checker should treat identically | A term collision with mutation-testing equivalence. Not a survivor class. |
| `kagi-shokunin/corpus/QUALITY.md:106` (QM19) | a timeout or unaccounted row is "invalid, never a surviving mutant" | An adjacent survivor-classification rule (receipt validity), orthogonal to anchoring. |

No sibling lane cites S012 (`2608.17214`, "Oracles That Cannot Fail") or uses
"specification-anchored", "state-anchored" or "anchored expectation" in S012's sense. The
command was `rg -i 'oracle.anchor|specification-anchored|state-anchored|anchored expectation|differential (oracle|hole|expectation|testing)|test.oracle|Oracles That Cannot Fail|2608\.17214'`
over every `*-shokunin` lane except tameshi.

## Affected axes

- **adjacency (judged): improved, report-only.** The scan names one cross-lane break: the
  round-26 item 7 holes never reached kumitate. It also names one owner anchor that
  tameshi did not cite (`round-close-gate.md:204`).
- **C2 (`classified=4`): unaffected.** Nothing here changes `anchors.json`, the probe or a
  class. All four anchored-hole calls stand. S_PIN_INCLUDES stays convention-held.
- **No axis harmed**, as long as the move below does not touch the committed anchors (see
  Risks).

## Proposed move (one, bounded)

Re-route, do not absorb. In the round-27 closure's routed-defects list, the integrator
should restate round-26 item 7 to kumitate (owner) with the anchors attached:

- The four witnesses, each with its anchor. The source is the table at
  `oracle-anchored-survivors.md:42-47`.
- A note that R39-5 carried only the zero-resolved fixture.
- For S_PIN_INCLUDES, an owner decision instead of a defect claim. Either declare the
  prefix rule in the header at `:36-38` (for example "a pin is a leading slice of the
  digest or commit name"), which turns the hole into a contract-backed defect. Or declare
  substring pins legal, which closes it as a contract change.
- For S_USAGE, a cite to `round-close-gate.md:204` as the owner's outside-blob statement
  of the 0/1/2/64 vocabulary.

This combines the entry's own recipe (`:68-70`, "route it to the gate owner") with the
routing gap found here. It costs one closure paragraph, and no tameshi corpus or anchor
file changes.

## Risks

- **Changing the committed anchors breaks C2's receipt.** `c2-measure.py` checks the
  anchors sha256 (`780e1009fc48…`, `oracle-anchored-survivors.md:2`), so a change to
  `anchors.json` now breaks the C2 receipt chain. Adding `round-close-gate.md:204` as a
  fifth anchor row would do exactly that. Do it only as prose in the closure or a later
  round, not in `anchors.json` this round.
- **The second S_USAGE anchor is still owner-written.** `round-close-gate.md:204` is a
  separate document, but the same owner wrote it. It is stronger than a header comment,
  but it is not an independent specification. Do not upgrade the entry's §5 bound beyond
  that.
- **The kumitate pin will drift.** Kumitate is active (head dated 2026-10-22). Any
  cite-check edit moves header line numbers and needs new anchors, as the entry's
  `recheck` line already says.
- **This overlap goes stale on the next kumitate edit.** A fix there would retire the
  "no newer revision" overlap. Recheck by blob hash, not by commit id.

## Verification (read-only, no clone needed)

```
cd /home/vgpnk/Projects/shokunin/kumitate-shokunin
GIT_OPTIONAL_LOCKS=0 git log --all --oneline -- scripts/cite-check.mjs | head -1   # 1205c66 …
sha256sum scripts/cite-check.mjs                                                   # 40573448…c10c9f
rg -n 'startsWith\(pin.hex\)' scripts/cite-check.mjs                               # :1195, :1219
rg -n 'S_PIN_INCLUDES|interior-slice|unknown-flag exit 64' corpus                  # no hit
sed -n '151,157p' corpus/lessons/round-39-verifier-spotcheck.md                    # R39-5: zero-resolved only
sed -n '204,206p' corpus/knowledge/round-close-gate.md                             # cite-check 0/1/2/64
```
