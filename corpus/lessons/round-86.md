# Round 86 — the discriminating certification, and the repertoire bound to bytes

Lane author TameshiR86 (attempt 1) / TameshiR86a2 (attempt 2, settlement) /
TameshiR86a3 (attempt 3, verification and landing), 2026-11-04. Base
`d10a9c66d6181cddcad52cdbffd672beb886ff6c`; freeze
`55d5a5c6002a048337cc511e1712df87b961d364`. `LOG.md` round 86 is the landing
record. Attempt 1 froze two claims, dispatched wave 1 and died before landing;
attempt 2 re-verified the freeze bytes, ran the wave to settlement, attacked
both frozen claims with the wave's seats and independently, and lands this
honest stop.

## Gate

Candidate: two claims. R86-C1 is a capability acquisition on operability — a NEW
discriminating certification counter for `tools/design-blob-audit.py`, with the
QUALITY criterion-111 cheat family executed and committed BEFORE the freeze. It
does not amend round-85's counter or its rejected verdict; it pays round-85's
closure routed defect 1. R86-C2 is calibration — every row of the lane's own
capability repertoire bound to repo state (a live freshness row naming it, or a
receipt the row itself cites that resolves at the named revision).

Source **S305** (Git git-ls-tree documentation) re-opened by L1 on 2026-11-04:
`https://git-scm.com/docs/git-ls-tree`, HTTP/2 200, 39083 B, sha256
`ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267`,
snapshot `.ufo/evidence/round-86/sources/s305-ls-tree.html` (+ `s305.headers`).
Located quotes, snapshot lines 1808 and 1812: “The mode of the object.” (5
words) and “The type of the object (commit, blob or tree).” (9 words). The
source supports listing semantics only — a tree listing carries a mode and a
type per entry, and its `FIELD NAMES` section gives the default format
`%(objectmode) %(objecttype) %(objectname)%x09%(path)` (snapshot line 1754) —
and is cited by R86-C1's expected-row derivation, which reads exactly those two
fields per entry before hashing the candidate blob itself. It does **not**
enumerate the octal modes: the `100644`/`100755` regular-blob boundary the
counter uses is S291's (index-format) ground, and it does not support the audit
verdict policy or any execution-provenance claim.

**Admit:** S305 as the re-opened listing-semantics source for R86-C1 (the
byte-identical re-fetch proves the same document, so no new row).
**Reject:** a second git-ls-tree row — within-scope duplicate of S305 (flip: a
distinct document at a distinct URL that states a rule S305 does not, e.g. the
mode/type field table in a normative spec).

Assimilation: none. `merge/tameshi/MERGE-REPORT.md` and the newest
`considerthese/2026-10-28.md` were read; neither serves these two frozen
claims, and no package row or knowledge entry was appended.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | inherited: a certification freeze without the criterion-111 cheat family | round-85's frozen counter admitted a no-git basename oracle at 8/8 (`T85C1.md`, sha256 `0acb90ac…`); the round-85 closure rejected the certification | QUALITY criterion 111, which stood before that freeze | this round executes the four cheat classes plus the r85 witness itself, and commits their receipts BEFORE the freeze: fingerprint 0/8, sequence 4/8, pinned-hash 0/8, always-accept 0/8, r85-forgery 6/8 against the real instrument's 8/8. Paid at the freeze bytes; the same defect then reappeared in a class the family did not model (M3) |
| M2 | wrong candidate tree in the counter's own expectation | the first run of `.ufo/evidence/round-86/measure.py` scored the real instrument 7/8: the `carried` case's expected rows were computed against the modified candidate tree instead of the carried-case candidate | the real instrument, run before the freeze — its correct rows disagreed with the counter's | expectations are derived per case from that case's own candidate revision (`tree_for(rev)`); the pre-freeze run then read 8/8. No target or predicate changed after any scoring |
| M3 | **the frozen R86-C1 counter is non-discriminating**: its arm class is disclosed by frozen path labels, and its fixture worktree is readable | `T86E2-att3b-cheat.py` (sha256 `89863caa…`, zero process spawns, zero git reads) and `T86CN1-oracle-worktree.py` each score `passed=8/8 C1_R86_PASS=true` exit 0 at the frozen counter — L1 reproduced both (`.ufo/evidence/round-86/attacks/c1-label-worktree-oracle.out`, `c1-label-worktree-hybrid.out`). Root cause: `pop/ok-<nonce>`, `pop/mx-<nonce>`, `pop/rf-<nonce>-{sha,inc,mix}`, `pop/zp-<nonce>` keep a stable class substring, and the mixed-arm worktree coincides with the candidate tree | the plan's own kill rule ("any control printing `passed=8/8` … kills the claim") plus QUALITY criterion 111's cheat family, which modelled fingerprint/sequence/pinned-hash/always-accept but not a **path-label + worktree** oracle | routed to round 87: the successor counter must use opaque nonce paths (no class substring), derive every expected row from committed objects only, and force the fixture worktree off the candidate tree. The fix counts only once the successor counter scores both oracles below its target — **not demonstrated yet** |
| M4 | **the frozen R86-C2 census is non-discriminating**: a relabel control with *cited* pins that resolve as **trees** binds every row | `.ufo/evidence/round-86/attacks/c2-cited-tree-relabel.out` — all 30 rows declared historical, each pinned to a cited ancestor directory at base, prints `CAP_CENSUS: rows=30 bound=30 unbound=0 mismatches=0` exit 0, i.e. the exact frozen after-state tuple with nothing bound to a receipt. L1 built the manifest independently (`c2-cited-tree-build.py`, `c2-cited-tree-manifest.json`) | the plan's kill rule clause "a relabel control that binds a row, kills the claim" plus QUALITY criterion 77 (a receipt population is files, not whatever the regex happens to accept) | routed to round 87: a historical pin must resolve as a **blob** (`git cat-file -t` = blob, cf. criterion 77's `not-regular-file` class), and `is_cited` must not accept a bare ancestor directory or a `path:line` token as the receipt path. The fix counts only once A1c scores `bound<30` — **not demonstrated yet** |
| M5 | pointer and quote-count drafting defects in the round's own frozen artifacts | the frozen plan and contract said "page lines 1807 and 1811"; the quotes sit at snapshot lines 1808 and 1812 (1807/1811 are `<dd>` open tags). The second quote is 9 whitespace tokens, not 10. The lesson's Gate attributed the `100644`/`100755` boundary to S305, which enumerates no octal mode | the scribe seat's pointer fixture (`T86S1-pointer-receipts.txt`: `resolved=0/2` at the frozen pointers, `resolved=2/2` at 1808/1812) and QUALITY criterion 116 (every pointer the round adds is re-resolved at the landing revision) | pointers, word count and the boundary attribution corrected in the plan, the contract (recorded as amendment A1), this lesson and the `corpus/SOURCES.md` round note; predicate, counter, case population, target and kill rule untouched. Correction receipt: `.ufo/evidence/round-86/pointer-recheck.out` |

| M6 | the two frozen claims are not jointly satisfiable with the capability row C1's type requires | C1 is declared a capability acquisition, whose AXES rule puts its row in `## Capabilities` in the same round; C2's frozen predicate counts exactly `rows=30` over that same table, so a 31st row makes C2 print `rows=31` and fail. Measured: `tools/capability-census.py --repo . --rev <any>` counts table rows (`rows=len(rows)`), and an unlisted row is `unbound` | AXES.md §Capabilities read against the frozen predicate text before the freeze — no seat needed to see it | no capability row is entered this round (C1 is killed anyway, M3); round 87 must add the successor capability row and let the census predicate be stated over a named population, not a frozen count, so a row addition cannot silently change a calibration claim |
| M7 | **two wave seats died without a report and left their scratch on disk, and no results file was ever written** | T86M1 (mutation-tester) ended with an empty scratch and no `T86M1.md`; T86SN1 (sentinel) ran 30+ probes (a logging `git` shim, a forged census manifest, absolute-path probes) and wrote no `T86SN1.md`; `.ufo/waves/round-86/w1-results.json` does not exist because attempt 2's L1 session ended at 22:09 before the dispatcher settled. Seat state had to be reconstructed from `w1/swarm-registry.json`, the 72 delivered files and `history://` | the wave context's two requirements (write your `Report:`, `rm -rf` your scratch before you yield) — both stood, but **no automated check reads them**, and the L1 died before it could either | attempt 3 recovered both seats' scratch byte-exact into `.ufo/waves/round-86/w1/dead-seat-T86SN1/` and `dead-seat-T86M1.note.txt`, removed them from `/fast/scratch`, and recorded the reconstruction. Round 87: the L1 writes a `settlement.json` before it may end, and `wave-reconcile` gains a dead-seat clause (a seat with no named report is a `dead` row, its scratch path recorded) |
| M8 | **a hand-drafted receipt header records a tool sha no run produced** | attempt 2's `.ufo/evidence/round-86/pointer-recheck.out` carried `# tool_sha256: e3b0c442…` (the empty-file hash) and `# tool:` the wave-dir fixture that no revision carried, so the standing sweep read `receipts=70 … unbound=1` (`detail=tool-absent`) while the round's own LOG claimed every sweep exit 0 | `tools/receipt-bytes-bind.py` at the tip — it re-derives the sha from the committed tool bytes and refuses the row | attempt 3 regenerated the receipt from its own run with the real fixture sha `7c349fce…` plus a `measured_bytes_rev` clause naming the commit that carries the fixture (criterion-128 two-commit pattern); sweep reads `unbound=0` at the final tip. Round 87: receipts are generated by a script that prints the header from `sha256sum`, never typed |

## Settlement — both frozen claims killed by their own rules

The literal predicates verify at the frozen bytes and at the landing revision
(C1 real instrument `passed=8/8`, C2 full manifest `rows=30 bound=30 unbound=0
mismatches=0`), and the five committed C1 controls stay below target (0/8, 4/8,
0/8, 0/8, 6/8). Neither claim is admitted: both are falsified by construction,
each by a class their frozen control sets did not model (M3, M4). A frozen
target is never narrowed after data, so this round is an honest stop on both
claims — it lands the counters, the control receipts, the two defeat receipts,
and the two mined defects, and claims no capability row, no axis increment and
no admission.

Limits, stated as limits: the C1 counter compares stdout and exit only, never
the read channel, so a worktree byte read and a `cat-file` byte read are
indistinguishable at the comparison; the C2 census binds by (path, rev) and a
tree resolves. Both limits are properties of the frozen bytes, not of the
landed data.

Attempt 3 measured two further limits of the same bytes
(`.ufo/evidence/round-86/landing/attempt3-probes.txt`). (1) Both instruments
strip `GIT_*` but invoke `git` by bare name, so their data channel is
PATH-inherited: a logging shim in `PATH` recorded all 73 of `measure.py`'s git
invocations and all 13 of the census's (P1, P2). This is a limit, not a new
kill — a PATH shim also serves the counter's own expected rows, so the class
collapses into the root-label oracle already killed by M3 — but it means the
instruments certify committed objects only when `PATH` is trusted. A failing
`git` fails closed: `measure.py` exit 1 with `P3_PASS_LINES=0`, the census exit
2 `setup refusal` (P3, P4, P6). (2) The census accepts a caller-supplied
`--manifest` from outside the repo and prints the frozen after-state tuple for
it (P5 `CAP_CENSUS: rows=30 bound=30 unbound=0 mismatches=0`, exit 0), so the
manifest is not bound to the repo or the revision — routed to round 87 with
M4.

## Source curation delta

S305 `used-by` old → new: `corpus/lessons/round-77.md, corpus/lessons/round-79.md,
corpus/lessons/round-82.md` → the same plus `corpus/lessons/round-86.md`. Status
mined → mined, recheck 365d → 365d, scope/anchor/opened unchanged. Registry rows
171 → 171; no tier additions; no source-id reuse; no new row. Census before and
after exit 0 with the standing warnings retained.
