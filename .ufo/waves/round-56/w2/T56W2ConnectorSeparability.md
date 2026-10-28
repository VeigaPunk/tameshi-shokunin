# T56W2ConnectorSeparability

## Axes and separability evidence

Axes: **C1 calibration** and **C2 operability**. All trees below are scratch clones under `/fast/scratch/hyaku/tameshi-r56/T56W2ConnectorSeparability`; no lane production file or sibling file was edited.

| Tree | Construction | C1 verdict | C2 verdict |
|---|---|---|---|
| Docs absent / C1 bound | Started at C0, restored `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, and `tools/registry.json` to their exact pre-C0 blobs; removed `corpus/knowledge/receipt-revision-binding.md` (content commit `0e237811bf2fa82fb39a845b436e2c66dc2e04a7`). Added synthetic fixture readers, bound the frozen 18 at that content commit (`779b154529825f311788c985b69d78532261765b`), then restated SCORECARD (REV `9507862f54c266a87c54e61503d4c613c43ef2c8`). | `C1_R56: rev=9507862f54c2 c0=0e237811bf2f credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` | `C2_R56: rev=9507862f54c2 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` |
| Docs + own receipts / C1 unbound | Started at C0 with the C2 docs already present; added fixture `controls-a/b.stdout` and valid SHA-256 sidecars, without adding readers or a re-key (REV `9a2f3967d2ec198dcae09f88fc9ccc1df46ee638`). The positive receipt names C0; the gate accepts it by content identity over the declared frozen surface, which this commit does not change. | `C1_R56: rev=9a2f3967d2ec c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` | `C2_R56: rev=9a2f3967d2ec selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=PASS docs=4/4 total=0 C2_R56_PASS=true` |

Supplemental C0-rooted fixture: with C0's docs intact, C1 bind + correctly restated row (REV `2e73840dc14e018d7b5baeadbd58f515181354e1`) yielded `C1_R56: rev=2e73840dc14e c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true`; with own receipts absent, C2 yielded `C2_R56: rev=2e73840dc14e selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false`. This shows the C1 repair alone does not satisfy C2. The request's phrase “leave the docs absent” conflicts with C0's actual tree: C0 itself adds all four doc surfaces and the C2 counter reads `docs=4/4` at C0. The docs-absent Tree C above resolves that by creating a scratch content commit with those doc surfaces absent, then binding at that commit.

A further isolated variant removed only the new knowledge note from the C0-rooted C1-pass tree: C1 remained `64/64`, `rekeyed=18/18`, `readers=18/18`, `PASS=true`; C2 read `docs=3/4`, `own=own-receipts-missing`, `PASS=false`. The ledger has zero inputs naming that new note.

**Proposed move:** keep the C2 doc bytes in the final content PIN, then bind the C1 re-key at/after that PIN; do not edit `SKILL.md`, `QUALITY.md`, `SOURCES.md`, or `tools/registry.json` after binding without re-binding affected sections. The scratch QUALITY mutation dropped C1 to 58/64, while the required opposite-pass trees show the claims do not imply each other.


### Fixture limits and second-order effects

- Reader JSONs and own receipts in these clones are **synthetic fixture artifacts**, not human-read attestations or outputs of the real controls run. The frozen C1 counter checks the hash/cand/report shape; it cannot establish a reader actually read (the contract states this limitation). Tree B's own receipts were deliberately gate-acceptable fixture receipts. The direct gate run returned `verdict=PASS`; this tests counter separability, not run provenance.
- Ordering is load-bearing: in a scratch clone, appending one line to `corpus/QUALITY.md` *after* the C1 bind changed the result to `credited=58/64 lost=6 rekeyed=12/18 monitor=6/58 total=4 C1_R56_PASS=false`. The rebound entries pin that input at PIN. Commit all content/doc edits before binding; later changes to pinned inputs require a new bind.
- The SKILL.md standing-rule surface is also adjacent to C1: it occupies the frozen `## Standing rules` section. Removing it after reports are formed changes that section's bytes and invalidates its C1 hash binding. The docs-absent fixture instead made the docs change part of its content commit and generated fixture readers for that commit.

Commands exercised the frozen counters in scratch lanes:
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/measure.py --lane <scratch-clone> --rev HEAD --work <empty-dir> --explain`
and the corresponding `c2/measure.py` invocation. The real round-55 binder was run in scratch clones with the frozen round-18 sectionizer and the 18-heading list. Full counter outputs are in `T56W2ConnectorSeparability-receipts/separability-counters.txt`.

## Sibling overlap on final bytes

`overlap=complement`

I grepped sibling lane working trees (including tools/scripts and corpus QUALITY/knowledge) for receipt revision, `rev=`, provenance, attestation, and digest binding. The following owned artifacts are adjacent to C2 but do not implement the same relation: C2 binds a receipt to the revision the deciding gate certifies. “Complement” means the rule is useful alongside C2, not a duplicate or a contradiction.

| Final sibling artifact (current HEAD; blob prefix) | Owned rule | Relation |
|---|---|---|
| `chousa-shokunin/corpus/evidence/round51/receipt-check.py` (9eef15e7c0e0; 75a171b9ce39) | `tool-rev` must resolve/land; tool bytes at tip must match the named tool revision; optional tool digest. It binds the **tool** revision, not the revision the receipt is certified for. Its check on tameshi round-54 `controls-b.stdout` printed `RECEIPT_NO_REV`. | complement |
| `chousa-shokunin/corpus/knowledge/receipt-binding-r38.md` (9eef15e7c0e0; 67c073a9566c) | Counter-measured pre/post gate and counter digests; invocation identity. | complement |
| `chousa-shokunin/corpus/knowledge/revision-binding-r31.md` (9eef15e7c0e0; 475697b11989) | SHA-256 pin of a claim's source bytes, not a receipt/certified-revision equality rule. | complement |
| `kotodama-shokunin/tools/check-receipt-seq.py` (44f76d456c1b; b46e77eb7348) | Stamped, evaluated, and measured revisions must agree; recorded tree and counter digest, with optional carrier topology. On the committed tameshi round-54 and round-55 receipts it reported `SEQ-… FAIL missing_headers=['stamped', 'evaluated', 'measured', 'tree']`. | complement |
| `souji-shokunin/tools/souji-receipt-run.py` (994de3b447e9; 8f78ec1beef3) | Receipt binds `rev`, tool path, tool SHA, command and exit; verify checks the tool blob at the named revision. Both tameshi receipts returned `RECEIPT-MALFORMED header order or fences do not match receipt v1`. | complement |
| `souji-shokunin/corpus/knowledge/git-strict-descendant-relation-r40.md` (994de3b447e9; 0bc3075509b8) | Requires a register-row `commit` to be a strict descendant of its `receipt_rev`; topology relation, not deciding-gate certification. | complement |
| `kama-shokunin/tools/round33-gate-receipts.py` (7ee8cbdf160f; 900154d7af55), QUALITY KQ43 | Captured/replayed gate fixture records source and evaluated revisions, argv, digests, exit and output. It separates evaluated revision from receipt-carrier commit; it does not gate the lane's receipt against the deciding revision. | complement |
| `tsukuroi-shokunin/tools/run-receipt.py` + `tools/check-report-receipts.py` (fb5a1d8625f0; 9944bd1899d3 / 5ea796e2dc57) | A report-cited revision/tool pair must have a committed receipt. Citation-side coverage, not the deciding gate's acceptance relation. | complement |
| `tsukuroi-shokunin/tools/_revision.py` + `tools/check-revision-binding.py` (fb5a1d8625f0; 24f398a6b981 / 86ef0ad09602) | Binds a tool's `--revision` CLI input to a landed branch revision. No receipt is read. | complement |
| `kake-shokunin/corpus/knowledge/receipt-integrity.md` (1a48131577ba; 351afd3bb71b) | Binds `counterSha256`/`toolSha256` to the invocation that wrote the receipt and catches stale/planted files. Run identity, not the certified revision. | complement |
| `kumitate-shokunin/scripts/receipt-attest.mjs` (14057f3e3899; 3ff972d4fbb5) | Canonical-record digest, sidecar and nonce/replay identity. Final source has no revision/commit axis. | complement |
| `kaidoku-shokunin/tools/round-46/attest.py` (e4f2cfa5ebff; 7aaa9b72a5c8) | Resolves `--rev` and checks an artifact's own SHA-256 pin at that revision; artifact attestation, not receipt-to-certified-revision binding. | complement |
| `revenger-shokunin/corpus/knowledge/digest-scope-versus-provenance.md` (6defe31e4af9; a459db90da35) | Defines the scope/limits of digest equality and provenance; semantic guardrail, not a receipt gate. | complement |

No duplicate or contradictory owner was found among these final-byte hits. The mechanical probes and greps are preserved in `T56W2ConnectorSeparability-receipts/sibling-overlap.txt`.

## Risks and verification

- Risk: the separability verdicts rely on synthetic reader reports/own receipts; they do not certify human reading or actual controls-run provenance.
- Risk: C2's docs are already present at C0, contrary to the tree-A parenthetical; the docs-absent scratch tree demonstrates the requested state, while the C0-rooted supplemental tree records the actual C0 residual failure (`own-receipts-missing`).
- The two required opposite verdict pairs were observed from both frozen counters; Tree C additionally had `lost=0`, monitor `64/64 score=8 box3=true`, docs `0/4`; Tree B had C2 `own=PASS docs=4/4` while C1 remained `46/64`, `lost=18`.
- No tools installed or updated. No build, lint, or unrelated test suite run. Sibling repositories were read-only.
