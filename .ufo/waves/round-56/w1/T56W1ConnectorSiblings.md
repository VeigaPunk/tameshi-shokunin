# T56W1ConnectorSiblings — sibling overlap scan (round 56, wave 1)

Axes: **adjacency** (primary), **operability** (C2 scope boundary).
Seat item: scan sibling lanes read-only for an existing receipt-to-revision binding rule or
provenance gate; classify each hit as duplicate / complement / contested; name what tameshi's
C2 must not absorb.

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
(frozen instrument set; base `981c5e8b`). No sibling file was opened for write, no lane production
file was touched, no git/jj mutation was run. Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W1ConnectorSiblings`,
removed on exit. No tool was installed for this seat (nothing was needed).

Receipts (command + output for every claim below): `T56W1ConnectorSiblings-receipts/`
(`sweep-terms.txt`, `sibling-inventory.txt`, `gate-comparison.txt`, `negative-sweeps.txt`).

## 1. What C2 owns, stated so it can be compared

`tools/receipt-revision-gate.py` (frozen) refuses a receipt when the revision it **names** is not
the revision it is **certified for**:

| role | rule | codes |
|---|---|---|
| `positive` / `verdict` | exactly one distinct `rev=` token; it must equal `--certified`, or name a revision whose bytes are identical on every path in `--paths` | `RECEIPT_REV_ABSENT`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_REV_UNRESOLVABLE`, `RECEIPT_REV_MISMATCH`, `RECEIPT_REV_CONTENT_DRIFT` |
| `control` | every `rev=` token resolves and is an ancestor of, or equal to, `--certified` | `RECEIPT_CONTROL_NOT_ANCESTOR` |
| both | path/digest hygiene | `RECEIPT_MISSING`, `RECEIPT_EMPTY`, `RECEIPT_NOT_BLOB`, `RECEIPT_DIGEST_MISMATCH`, `RECEIPT_REQUIRED_LINE_MISSING` |

The distinctive subject is **the certification relation**: receipt → the revision the lane is
about to accept it for. Not the tool's revision, not the run's own stamp, not file digests.

## 2. Sibling lanes at scan time

`git -C <lane> rev-parse HEAD`, working tree clean except `kaidoku` (130), `kengaku` (5),
`tsukuroi` (3), `kama` (1), `kasegi` (1), `tameshi` (2 — this round's untracked evidence).
Recorded in `sibling-inventory.txt`.

| lane | HEAD | lane | HEAD |
|---|---|---|---|
| audio | `7a2fcd4f0883` | kumitate | `14057f3e3899` |
| chousa | `9eef15e7c0e0` | lore | `380ef3abc7c7` |
| game-dev-2d | `7753d49b1667` | mado | `3b55b6e91e40` |
| game-dev-3d | `89dd182b7094` | mori | `325f7e639916` |
| kagi | `69b61db46be4` | revenger | `6defe31e4af9` |
| kaidoku | `dc73587a8b9c` | souji | `0242085909fb` |
| kake | `1a48131577ba` | tabi | `2844de3067eb` |
| kama | `7ee8cbdf160f` | tameshi | `c3e2ca9f0207` |
| kasegi | `5ab3a60a5cb0` | tsukuroi | `b866a1d3d266` |
| kengaku | `7864296ee02a` | kotoba | `47dbe8781657` |
| kotodama | `44f76d456c1b` | | |

## 3. Hits — one row per sibling artifact that owns a receipt-to-revision rule or a provenance gate

`blob` is `git -C <lane> rev-parse HEAD:<path>` (full hashes in `sibling-inventory.txt`).

| # | sibling | path (anchor) | what it owns | relation to C2 |
|---|---|---|---|---|
| 1 | chousa | `corpus/evidence/round51/receipt-check.py` (QUALITY.md:896, criterion 84; blob `75a171b9ce39`) | A receipt's **first five lines** carry `tool-rev: <40hex> tool: <path> [digest: sha256:<64hex>]`; the named revision must resolve, be an ancestor of `--tip`, and the tool's blob at tip must equal its blob at that revision. Codes `RECEIPT_NO_REV`, `RECEIPT_REV_UNKNOWN`, `RECEIPT_REV_UNLANDED`, `RECEIPT_TOOL_ABSENT`, `RECEIPT_TOOL_MOVED`, `RECEIPT_DIGEST_MISMATCH`, `RECEIPT_OK`. | **complement** — subject is the *tool* revision (does the tip still carry the code the receipt measured). Its header convention is not `rev=`, so it is blind to C2's class: on both real receipts it prints `RECEIPT_NO_REV` (§4), never reaching the two-token defect. |
| 2 | kotodama | `tools/check-receipt-seq.py` (QUALITY.md:55 criterion 17, :59 criterion 19; blob `b46e77eb7348`) | Receipt header equality: `# stamped revision:` = `# evaluated revision:` = `# measured revision (lane main):`, recorded tree = `git rev-parse <stamped>^{tree}`, counter sha256 = sha256(counter); `--topo` adds carrier-parentage (the commit carrying a receipt has the stamped revision as parent); `--lands` reads committed bytes only. | **complement** — subject is the receipt's relation to **its own run** (stamp == evaluation), and the post-records carrier. It says nothing about whether the named revision is the one the lane certifies. On both real receipts: `FAIL missing_headers=['stamped','evaluated','measured','tree']` (§4). |
| 3 | souji | `tools/souji-receipt-run.py` (QUALITY.md:129 Q55, :151 Q61; blob `8f78ec1beef3`) | Receipt v1 header binds `rev=<40hex>`, `tool`, `tool_sha256`, `cmd`, `rc`, `utc`; `verify` re-reads the committed blob at the named revision and refuses `RECEIPT-TOOL-DIGEST-MISMATCH`. Q55 requires every count a record quotes to name such a receipt. | **complement** — subject is **tool bytes at the named revision** plus "a quoted count needs a bound receipt". It does not ask whether the named revision is the certified one. On the round-54 receipt: `RECEIPT-MALFORMED header order or fences do not match receipt v1` (§4). |
| 4 | kama | `tools/round33-gate-receipts.py` (QUALITY.md:315 KQ43; blob `900154d7af55`) | Capture runs a gate **from a pinned lane revision against that revision** and three disposable fixtures; audit replays each case from its pinned source revision; KQ43 requires argv, source **and evaluated** revisions, gate/runner digests, numeric exit, captured stdout/stderr, and that report text distinguish the evaluated revision from the commit that first carries the receipt. | **complement** — closest sibling on *evaluated revision*, but scoped to kama's own gate-receipt replay (fixture cases). It does not gate a round's control/verdict receipts against the revision under certification. |
| 5 | tsukuroi | `tools/run-receipt.py` + `tools/check-report-receipts.py` (QUALITY.md:147 criterion 77; blobs `9944bd1899d3`, `5ea796e2dc57`) | A revision-cited gate/measurement is admissible only with a committed receipt whose JSON-lines header names `revision` (equal or leading prefix of the cited hash) and `tool_sha256`; the run executes a sandbox clone at the tool revision. The checker enforces the citation leg over a report. | **complement** — same direction (receipt must name the revision a record cites), but on the **citation** side of a report, not on the **acceptance** side of a deciding gate. On a tameshi lesson: `{"cited": 0, "unreceipted": 0}` (§4) — its citation grammar does not match tameshi records at all. |
| 6 | tsukuroi | `tools/_revision.py` + `tools/check-revision-binding.py` (blobs `24f398a6b981`, `86ef0ad09602`) | Binds a **gate's `--revision` CLI input** to a landed commit: branch validity, resolution, ancestry of `refs/heads/<branch>`, optional pushed-ness; error classes `E-BRANCH-INVALID`, `E-REVISION-INVALID`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`, `E-GIT-FAILED`. The judge keeps an independent copy on purpose. | **complement** — this is the *input* revision of a tool, not the revision a receipt names. No receipt is read. |
| 7 | kake | `corpus/QUALITY.md:433` and `:450` + `.ufo/waves/round-30/witness/witness_receipt_identity.py`, `witness_claim_receipt_backing.py` (blobs `220a934752aa`, `0b2e3eef2750`, `9e535cb13336`) | Two rules: a measurement receipt names the revision it measured **and the sha256 of every tool whose bytes it depends on**; every revision a report/SCORECARD names as measured has a **committed receipt naming that revision** (a glob proves nothing). | **complement** — presence + revision agreement from the record side (revision → receipt), and digest identity. The witness is a fixed round-30 instrument, not a gate for later rounds (its own criterion says so). |
| 8 | kake | `corpus/knowledge/receipt-integrity.md` (blob at HEAD, lane `1a48131577ba`) | Receipt→run binding: `receipt["counterSha256"] == sha256(invoked counter)`, `toolSha256` binding, the three defect classes (counter-error receipt, missing tool, planted earlier run). | **complement** — binds a receipt file to *the invocation that wrote it*; C2 binds a receipt to *the revision it is evidence for*. Both are needed; neither implies the other. |
| 9 | chousa | `corpus/knowledge/receipt-binding-r38.md` + `corpus/knowledge/revision-binding-r31.md` (blob at HEAD) | r38: every counter receipt binds `gate_sha256_pre`/`gate_sha256_post` and counter identity, measured by the counter, not the gate under test. r31: a **claim** carries a `sha256` pin compared against the exact source bytes (`CLAIM_SOURCE_REVISION_MISMATCH`). | **complement** — r38 is byte binding of the gate under test; r31 is a content pin on a claim's source. Neither is a receipt→certified-revision rule. |
| 10 | kaidoku | `.ufo/waves/round-17/tools/receipt-validate-v2.py` (SKILL.md:866; blob `a6d98240c263`) | Validates a receipt's recorded file digests, pins, mid-run drift and mid maps; 32 selftest cases. | **complement** — digest/pin integrity of a run's own record. No revision comparison. |
| 11 | kagi | `corpus/release-clock.py` (SKILL.md:48, :442; blob `77e26228d298`) | Replays a **pinned** rearmed receipt; `--observe` writes a new receipt and returns `RECEIPT-MISMATCH`/exit 1 on drift; SKILL states "Receipts/checksums bind *bytes* … never imply provider attestation". | **complement** — observed-vs-pinned receipt comparison inside one tool; the scope sentence is a limit C2 should keep, not a rule it duplicates. |
| 12 | kumitate | `scripts/receipt-attest.mjs` + `corpus/knowledge/receipt-identity-canonicalization.md` (blob `0e9baaf05b2d`) | `receipt-attest` v3: canonical-JSON record digest as identity, sha256sum text-mode sidecar, nonce ledger whose evidence set is the **whole directory** (R52-9), `VALID/REPLAY/TAMPERED/UNREADABLE/USAGE`. | **complement** — receipt *identity* and nonce replay. `grep -n -iE 'revision|commit' scripts/receipt-attest.mjs` prints **0 hits**: it has no revision axis at all. |
| 13 | revenger | `corpus/knowledge/digest-scope-versus-provenance.md` (blob `a459db90da35`) | Digest equality holds only over the exact bytes hashed; a reformatted save invalidates a digest claim. | **complement** — supplies the semantics C2's `--paths` content-identity escape relies on, and warns that a digest leg is not behaviour (C2's own `cannot_see` says the same). |
| 14 | game-dev-3d | `corpus/knowledge/unreal-mcp/PROVENANCE.md` (SKILL.md:184; blob `66ba696469d1`) | Pin + byte-identity + install receipts for an MCP tree, with a named SHA-256 of the provenance file itself. | **complement** — asset provenance, no receipt/revision relation. |
| 15 | kama | `corpus/QUALITY.md` KQ16 (`:61`) and KQ74 (`:410`) | Capture provenance: `git show <pinned-commit>:<path>` declared as author-recorded provenance, corroborated by `git cat-file blob`; KQ74 admits a live receipt's provenance only when each digest is bound to the artifact the same run used. | **complement** — provenance of a *capture*, record-time verification. Adjacent, not the same subject. |

## 4. Mechanical proof that the neighbours cannot see C2's defect

One command set, four gates, the two receipts the lane **already accepted**
(`gate-comparison.txt`; certified `c3e2ca9f0207`):

| gate | round-54 `control/controls-b.stdout` | round-55 `after/c2.stdout` |
|---|---|---|
| tameshi `tools/receipt-revision-gate.py` | `codes=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98` (REFUSED, rc 0 by design of the counter's verdict line) | `codes=RECEIPT_REV_ABSENT` (REFUSED) |
| chousa `receipt-check.py` | `RECEIPT_NO_REV`, `RECEIPT_CHECK=FAIL`, rc 1 | `RECEIPT_NO_REV`, rc 1 |
| kotodama `check-receipt-seq.py` | `FAIL missing_headers=['stamped','evaluated','measured','tree']`, `RECEIPT-SEQ: FAIL`, rc 1 | same, rc 1 |
| souji `souji-receipt-run.py verify` | `RECEIPT-MALFORMED header order or fences do not match receipt v1`, rc 2 | — |
| tsukuroi `check-report-receipts.py` (on `corpus/lessons/round-54.md`) | `{"cited": 0, "unreceipted": 0}`, rc 0 | — |

Reading: every sibling gate refuses these receipts, and **every refusal is for a different
reason** than C2's. chousa stops at "no `tool-rev:` header" before it ever tokenizes `rev=`;
kotodama stops at missing header lines; souji stops at the header shape; tsukuroi finds nothing
to cite. None of them reaches "the receipt names `077d431e6996` while the lane certifies
`c2108100`". That is the gap C2 fills, and it is not filled twice.

## 5. Boundary — what C2 must report and **not** absorb

These are sibling-owned legs. Writing them into `corpus/knowledge/receipt-revision-binding.md`,
the QUALITY criterion, or the `## Standing rules` rule would duplicate a sibling rule under a
different name, and in one case would contradict it:

1. **Tool-revision-moved** (`RECEIPT_TOOL_MOVED`, chousa 84). C2's gate reads only `rev=`; it has
   no tool path and no tip comparison. Do not claim C2 detects a receipt measured on code the tip
   no longer carries.
2. **Stamp == evaluation** (kotodama 17/19). C2 does not read `# stamped revision:` /
   `# evaluated revision:`. **This one is a live contradiction risk:** kotodama requires *exact*
   equality between stamp and evaluation, while C2 deliberately permits `rev=` ≠ certified when the
   bytes are identical on a declared path list (`RECEIPT_REV_CONTENT_DRIFT` is the refusal, and
   equality on `--paths` is the acceptance). The knowledge entry must scope the content-identity
   escape to the **certification** relation and must not restate it as a general rule about a
   receipt's own run.
3. **Digest-of-bytes** (`tool_sha256`, `gate_sha256_pre/post`, canonical record digest — souji,
   chousa r38, kake, kumitate). C2's `RECEIPT_DIGEST_MISMATCH` reads an optional `.sha256` sidecar
   beside the receipt; it is not a tool/counter digest leg.
4. **Citation side** (tsukuroi 77, kake `:450`): "a record that cites a revision must have a
   receipt naming it" is the converse direction. C2 gates receipts the lane **accepts**, not
   claims a record **makes**.
5. **Carrier parentage** (kotodama `--topo`): post-records topology of the commit carrying a
   receipt. C2 has no topology leg (`RECEIPT_CONTROL_NOT_ANCESTOR` is revision ancestry, not
   carrier parentage).

## 6. Naming risk (report, do not absorb)

chousa owns the `RECEIPT_REV_*` token family with disjoint semantics:
`RECEIPT_REV_UNKNOWN` (commit not in repo) and `RECEIPT_REV_UNLANDED` (not an ancestor of tip).
C2 uses `RECEIPT_REV_ABSENT`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_REV_UNRESOLVABLE`,
`RECEIPT_REV_MISMATCH`, `RECEIPT_REV_CONTENT_DRIFT`. No exact name collides, but a reader who
greps `RECEIPT_REV_` fleet-wide gets two rule sets. The C2 knowledge entry should name chousa
QUALITY 84 once, as the neighbour whose subject is the tool revision, so the family split is
recorded rather than discovered later.

## 7. Negative sweeps (what the scan did not find)

`negative-sweeps.txt`:

- **A.** No sibling `SKILL.md` `## Standing rules` section carries a receipt / revision /
  provenance / digest rule — `grep -icE` = `0` for mado, tabi, tsukuroi, **and tameshi** (the C2
  rule will be the first in that section, fleet-wide).
- **B.** Only tameshi ships deciding-run scripts (`ls */tools/deciding* */​.ufo/evidence/round-*/deciding-run.sh`
  → `tameshi-shokunin` alone). No sibling deciding gate exists whose receipt binding C2 would
  duplicate.
- **C.** No sibling knowledge entry, QUALITY criterion or SKILL states the certified-revision rule:
  `grep -rn -iE 'certified revision|evidence only for the content'` outside tameshi → **0 hits**.
- **D.** No sibling file `corpus/knowledge/receipt-revision*` exists; the C2 entry name is free.

Term sweep over `corpus/knowledge`, `SKILL.md`, `tools/` for `rev=`, `receipt`, `attestation`,
`provenance`, `digest`, `frozen receipt` (`sweep-terms.txt`): 1336 tameshi, 1087 tsukuroi,
~615 tabi, 308 kotodama provenance hits, 161 kotodama attestation hits, 72 kaidoku provenance.
The rows above are the subset that **binds a receipt (or a capture) to a revision or to a run**;
the remainder are per-round instruments and prose that name receipts without stating a binding
rule.

## 8. Verdict

**overlap=complement.**

Seven siblings own a receipt-to-revision or receipt-to-run binding in five distinct senses
(tool revision · stamp==evaluation · tool bytes at the named revision · citation backing ·
carrier parentage) and five more own provenance/identity gates. None owns the certification
relation — "the receipt the lane accepts names the revision the lane certifies, or bytes identical
on a declared surface" — and each neighbour gate was measured to refuse the two real receipts for a
*different* reason than C2's. C2 duplicates nothing; it completes the set.

Two items must be **reported and not absorbed**: the kotodama stamp==evaluation exactness (C2's
content-identity escape must be scoped to certification only, or the two rules read as
contradictions) and chousa's `RECEIPT_REV_*` family (disjoint semantics, shared prefix).

## 9. Limits of this scan

- `grep`-led discovery over three roots per lane; a rule stated only in `corpus/lessons/`,
  `PROVINCE.md`, `SHONEN.md` or a wave report is reached only when it also lands in a criterion or
  a tool docstring. The five neighbour gates were **run**, not read.
- `kaidoku` (130), `kengaku` (5), `tsukuroi` (3), `kama` (1), `kasegi` (1) had dirty worktrees at
  scan time; findings are stated at committed HEAD blobs, not at their working trees.
- Running a sibling gate is not a verdict on that gate's own claim; each was used here only as a
  witness that its rule does not cover C2's defect class.
- This seat cannot see whether a sibling round is *concurrently* changing one of these rules.

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ `ok … /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, exit `0` (W01/W04
advisories only).
