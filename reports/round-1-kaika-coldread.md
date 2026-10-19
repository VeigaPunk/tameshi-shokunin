# Cold-read — tameshi-shokunin SKILL.md, Appendix A + Appendix B

Seat: `W2RoundTameshi.ColdReadLab-2` (leaf L2; single probe; repo read-only;
scratch only `/tmp/tameshi-r1-coldread5-998226/`). Executed 2026-10-19,
22:04–22:10Z.

**Hypothesis (H).** An agent with no oral context can execute LANE/SKILL.md's
two worked examples end-to-end from the page alone — Appendix A (JS) and
Appendix B (bash): pin, uniqueness check, control, all 10 defects each, verdict
table, survivor non-equivalence probes, restore/byte-identity proof — and
reproduce the recorded verdict tables. Falsified by any GAP-BLOCKING step or
WRONG-EXPECTATION.

**Route.** The page directs all sweep writes through the pinned harness
(SKILL.snapshot.md:829–847, the round-6 protocol). Used
`tools/mutate-and-run.sh` r10-2, sha256
`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`. The
harness has no `--check` verb, so the recipe-step-5 uniqueness gate
(SKILL:171–178) was exercised by a small literal-count checker
(`check_uniqueness.py`); the harness independently asserts `count(old)==1` and
`new != old` before any suite run (tool usage block), so the gate was doubly
enforced. The harness route was chosen over the appendices' literal
`python3 mutate_driver.py` route; both are page-internal (the appendices write
"driver contract (write from this spec)").

Host/runtime: node v24.21.0 (matches round 2's recorded runtime), GNU bash
5.3.15, linux 7.2.3-arch1-3, 32 cpus; per-run timeout 300 s (harness default;
page used 300 s round 2 / 280 s round 3).

## Scope + contamination log

Opened/read, and nothing else:

- LANE `SKILL.md` (snapshot below) — the page under test.
- `tools/mutate-and-run.sh` — page-directed instrument; read its usage/help,
  header contract and spec parser only (its embedded-ledger comments list the
  same cases as the page; the specs below were transcribed from the Appendix
  manifests, not from the tool's embedded copies — the uniqueness gate's
  first-line readings independently re-confirmed every page site).
- Target gate files, read-only: kumitate `scripts/kimi-census.mjs` and kagi
  `corpus/surface-census.sh`, materialized via
  `git -C <sibling> show <rev>:<path>` at the page's pinned revisions; kagi's
  gate read only in the ranges needed to build the survivor probes.
- Sibling repos otherwise touched only via `git status/ls-tree/rev-parse/
  merge-base` metadata.
- `ls` of the lane root and the worktrees parent (names only).

Contamination: **none of the forbidden material was opened** — no `corpus/`,
`LOG.md`, `reports/`, `plans/`, `SCORECARD.md`, `SHONEN.md`, `.ufo/` (except
writing my own output dir), no dossiers, no dead seats' `/tmp` dirs. The page's
Appendix B probe commands cite "note §7 commands" (SKILL:621), i.e. the round-3
corpus note, which is contamination-flagged; it was **not** read, and the probe
fixtures were reconstructed from the artifact plus the page's recorded probe
readings instead (see Appendix B, step 8).

## SKILL snapshot

`/tmp/tameshi-r1-coldread5-998226/SKILL.snapshot.md` (copied out to
`.ufo/evidence/kaika-round-1/coldread/SKILL.snapshot.md`) — sha256
`33e3009c919cd0fb0b2c67bbd7927655289450750f4f69d9ca86758d81000f81`, 1477
lines, captured **2026-10-19T22:04:07Z**. All `SKILL:` refs below are line
numbers in this snapshot.

## Appendix A run — JS case

Pins first, from the committed object store:

- `git -C kumitate-shokunin show 175de6ba:scripts/kimi-census.mjs` →
  sha256 `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`,
  896 lines / 43273 B — **equals the page's pin** (SKILL:533–536). Blob
  `a2bf15c0…`; `175de6ba` is an ancestor of HEAD `16a5441`.

Control (before any mutation): `node pristine.mjs --selftest` → exit 0,
`KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS` (SKILL:540–546) —
evidence `evidence/A-control.txt`, `appendixA/control.out`.

Uniqueness gate (`check_uniqueness.py spec-A.txt pristine.mjs`): all 10 `@old`
strings `count=1`, first-line readings 105/378/332/351/255/124/306/396/292/145
matching every page site exactly; final literal line `all unique` (SKILL:171–178,
567–584) — `evidence/A-check.txt`.

Manifest transcription: `spec-A.txt` sha256 `ae45bba5…`; the D4 en-dash
(U+2013, SKILL:567) and D8's trailing-newline edit (SKILL:578) are carried by
the count-1 match.

Sweep (harness, `--suite 'node "$MUTANT" --selftest'`, 11 runs): control GREEN
exit 0; `MUTATE_RESTORE: OK` (target-pristine sha256 before = after =
`83016d45…`); `MUTATE: DONE (defects=10 killed=8 survived=2 inconclusive=0
kill-rate=80%)`; wall 7.82 s (page recorded 7.0 s; the page labels cost
host-local — SKILL:240–245). Full log `evidence/A-tool.txt`,
`appendixA/{D1..D10}.out`, `appendixA/results.tsv`.

Measured vs recorded, per defect (labels read from the full logs; page table
SKILL:585–592):

| id | recorded | measured | match |
|---|---|---|---|
| D1 | 27/43 FAIL (16 cases) | 27/43 FAIL, 16 `FAIL` labels (first: green fixture flips) | yes |
| D2 | 43/43 PASS — **survivor** | 43/43 PASS | yes |
| D3 | 27/43 FAIL (16) | 27/43 FAIL, 16 labels | yes |
| D4 | 40/43 FAIL (3) | 40/43 FAIL, 3 labels (both root-enum arms + orthogonality) | yes |
| D5 | 42/43 FAIL (1) | 42/43 FAIL, 1 label (presence-gated chain) | yes |
| D6 | 41/43 FAIL (2) | 41/43 FAIL, 2 labels (0600 floor, FIFO arm) | yes |
| D7 | 41/43 FAIL (2) | 41/43 FAIL, 2 labels (credential floor, token floor) | yes |
| D8 | 40/43 FAIL (3) | 40/43 FAIL, 3 labels (2× root-missing + json token) | yes |
| D9 | 41/43 FAIL (2) | 41/43 FAIL, 2 labels (FIFO, dangling symlink) | yes |
| D10 | 43/43 PASS — **survivor** | 43/43 PASS | yes |

Kills 8/10 = 80 %, survivors {D2, D10}, 0 inconclusive — matches the page's
recorded table exactly.

**Survivor probes (SKILL:552–555, 214–223) — both reproduced:**

- D2 on an empty root: pristine last line `… +22 more`; mutant `… +23 more`
  (one fewer id; node exits 1 in both) — `evidence/A-probe-empty-*.txt`.
- D10: pristine `FAMILY K2  members=0  checked=0  frozen=25`; mutant
  `frozen=24` — page's `frozen=24 (vs 25)` confirmed.

Restore proof: tool `MUTATE_RESTORE: OK`; scratch pristine `cmp`-identical to
the materialized pinned bytes (SKILL:390, 593); pinned blob re-read after the
sweep still `83016d45…`. The kumitate **working tree** path is dirty — see
O4/incident below; the pinned blob is untouched.

## Appendix B run — bash case

Pin: `git -C kagi-shokunin show fecee874:corpus/surface-census.sh` → sha256
`275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, 44212 B,
886 newlines, last byte `0x63` (no trailing newline — SKILL:601–604), blob mode
`100755` (`ls-tree`, matching the page's "mode 755"); `fecee874` is an ancestor
of HEAD `aea7a43`; `git status --porcelain -- corpus/surface-census.sh` empty.

Control: `bash pristine.sh --selftest` → exit 0, `SELFTEST: PASS (16 cases)`
with `ok-case 01..14` + `skip-case 15/16 … substrate-absent` inside the count
(SKILL:608–612) — `evidence/B-control.txt`, `appendixB/control.out`.

Uniqueness gate: all 10 `@old` `count=1` at first-lines
241/435/229/200/214/371/405/85/191/862, `all unique` — `evidence/B-check.txt`.
`spec-B.txt` sha256 `dd6142fc…`; the `\\n` printf-format escapes (SKILL:633–651)
round-tripped exactly.

Sweep (harness, `--suite 'bash "$MUTANT" --selftest'`, 11 runs): control GREEN
exit 0; `MUTATE_RESTORE: OK` (`275d8294…` before = after); `MUTATE: DONE
(defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)`; wall 11.54 s
(page recorded 11.0 s; host-local per SKILL:240–245). Logs
`evidence/B-tool.txt`, `appendixB/{B1..B10}.out`, `appendixB/results.tsv`.

Measured vs recorded, per defect (page table SKILL:652–663):

| id | recorded | measured | match |
|---|---|---|---|
| B1 | FAIL 1/16 — 05 undeclared-file | `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0`; `FAIL (1/16 cases)` | yes |
| B2 | FAIL 2/16 — 01 clean, 04 runtime-absent | `bad-case 01 clean`, `bad-case 04 runtime-absent`; `FAIL (2/16)` | yes |
| B3 | FAIL 3/16 — 01, 04, 06 crosscheck-disagree | those three; `FAIL (3/16)` | yes |
| B4 | FAIL 1/16 — 07 symlink-swap, **token-only** | `bad-case 07 symlink-swap want exit=1 token=SURFACE LINK got exit=1`; `FAIL (1/16)` | yes |
| B5 | **PASS (16 cases) — survivor** | PASS (16 cases) | yes |
| B6 | FAIL 2/16 — 01, 04 | 01, 04; `FAIL (2/16)` | yes |
| B7 | FAIL 1/16 — 10 sqlite-unavailable (`unverified=3` tripwire) | `bad-case 10 sqlite-unavailable exit=1` with the `SHAPE UNVERIFIED`/`unverified=3` token absent (assert sites pristine.sh:782); `FAIL (1/16)` | yes |
| B8 | FAIL 2/16 — 13 malformed-row, 14 fused-shape-row | `bad-case 13 malformed-row want exit=2 token=bad kind got exit=1`, `bad-case 14 fused-shape-row exit=1`; `FAIL (2/16)` | yes |
| B9 | FAIL 2/16 — 03 asset-gone, 04 runtime-absent | those two; `FAIL (2/16)` | yes |
| B10 | **PASS (16 cases) — survivor** | PASS (16 cases) | yes |

Kills 8/10 = 80 %, survivors {B5, B10}, 0 inconclusive — exact match, including
the B4 token-only kill and B7's token tripwire.

**Survivor probes (SKILL:621–625, 214–223) — both reproduced.** The page names
the probe commands but not the fixture trees ("note §7 commands", contamination-
forbidden); fixtures were reconstructed from the gate's own input contract and
the page's recorded probe readings (a census row declaring an `exec` surface
with no execute bit; a clean file row for the summary probe):

- B5: pristine prints `SURFACE DIVERGED $HOME/bin/tool (declared exec, no
  execute bit)` + `SURFACE_CENSUS: DRIFT`, rc=1; mutant prints
  `SURFACE OK       $HOME/bin/tool (exec 644)` + `SURFACE_CENSUS: CLEAN`, rc=0
  — page's reading verbatim — `evidence/B-probe-B5-*.txt`.
- B10: pristine summary `… ok=1 absent=0 …`; mutant `… ok=0 absent=0 …` — page
  verbatim — `evidence/B-probe-B10-*.txt`.

Restore proof: `MUTATE_RESTORE: OK`; scratch `cmp`-identical to the pinned
bytes; kagi path `git status --porcelain` still empty; live file sha256 still
`275d8294…`, size 44212 B, mode 755, mtime `2026-10-14 09:47:15` unchanged
(SKILL:664–667).

## Step sufficiency table

Verdicts: SUFFICIENT · SUFFICIENT (latitude) · ADDITIVE-IMPROVISATION ·
GAP-BLOCKING · WRONG-EXPECTATION · NOT EXERCISED. "Evidence" names copied files
under `.ufo/evidence/kaika-round-1/coldread/`.

| Step (page refs) | Appendix A | Appendix B | Evidence |
|---|---|---|---|
| 1 control (138–148) | SUFFICIENT | SUFFICIENT | A-control.txt, B-control.txt |
| 2 pin (150–157) | SUFFICIENT (latitude) | SUFFICIENT | A-tool.txt, B-tool.txt; see O4 |
| 3 pristine copy (158–161) | SUFFICIENT | SUFFICIENT | cmp in O5 |
| 4 defect list (162–170) | SUFFICIENT | SUFFICIENT | spec-A.txt, spec-B.txt |
| 5 uniqueness gate (171–178) | SUFFICIENT | SUFFICIENT | A-check.txt, B-check.txt |
| 6 control + mutants (179–188) | SUFFICIENT | SUFFICIENT | A-tool.txt, B-tool.txt |
| 7 adjudicate (189–213) | SUFFICIENT | SUFFICIENT | appendixA/\*.out, appendixB/\*.out |
| 8 survivor probes (214–223) | SUFFICIENT | **ADDITIVE-IMPROVISATION** | A-probe-\*, B-probe-\* |
| 9 restore proof (224–229) | SUFFICIENT (latitude) | SUFFICIENT | O4, O5 |
| 10 record (230–236) | SUFFICIENT | SUFFICIENT | this report |
| appendix commands (540–555 / 608–625) | SUFFICIENT | SUFFICIENT (probes: me) | — |
| appendix driver contract (557–566 / 626–632) | SUFFICIENT (latitude) | SUFFICIENT (latitude) | harness r10-2 route, L829–847 |
| appendix manifest (567–584 / 633–651) | SUFFICIENT | SUFFICIENT | spec-A.txt, spec-B.txt |
| appendix expected table (585–592 / 652–663) | SUFFICIENT | SUFFICIENT | tables above |

Notes on the non-plain cells:

- **A·step 2 (latitude).** The page's pin is a committed blob; the blob at
  `175de6ba` equals the recorded sha. The appendix's extra
  `git status --porcelain` cleanliness sub-assert did not hold *at sweep time*:
  a foreign in-flight edit landed on the kumitate worktree file at
  2026-10-19T22:06:51Z (73 s after `MUTATE_DATE 22:05:38Z`). The page's own
  rule covers a moved substrate ("re-derive … or re-anchor", SKILL:537–539)
  and its incident discipline records drift rather than smoothing it
  (SKILL:687–690); the sweep ran on the git blob, so the recorded table is
  bound to `83016d45…`, re-verified after the run. Not blocking.
- **A·step 8 / B·step 8.** A's probe commands are complete and reproduced as
  printed. B's two probe commands reference `$W/probe*` fixture files whose
  construction is only in the forbidden round-3 note (SKILL:621). I rebuilt
  them from the gate's input contract; both probes then produced the page's
  exact recorded readings, so the recorded expectation was complete enough to
  derive the fixture. This is the page's one genuine latitude item for a cold
  reader — improvised but non-blocking.
- **A/B·driver contract (latitude).** Appendices describe a python driver;
  the page's protocol (829–847) directs the pinned harness. Both route through
  the same contract items (`--check` uniqueness, control first, one mutant per
  defect, kill criterion, restore re-check). Chose the harness; the missing
  `--check` verb was replaced by the explicit checker.
- **A·step 9 (latitude).** The page's stronger form is "scratch copy
  `cmp`-identical" (390) plus a clean substrate path. Kumitate's worktree path
  is dirty from the foreign edit above; the tool's target-restore proof and the
  `cmp` proof hold, and the pinned blob re-read is unchanged.

No cell is GAP-BLOCKING, WRONG-EXPECTATION or NOT EXERCISED.

## O / I / U

**O (measured, with location).**
1. Both appendices reproduce their recorded verdict tables exactly:
   A 8/10 (D2/D10 survivors), B 8/10 (B5/B10) — `appendixA/results.tsv`,
   `appendixB/results.tsv`; B4 token-only and B7's `unverified=3` tripwire
   reproduced (`appendixB/B4.out`, `B7.out`).
2. Controls green first run: A `43/43 pass`/`PASS` exit 0; B `PASS (16 cases)`
   exit 0 with the two declared `skip-case`s inside the count.
3. All four survivor probes show observable non-equivalence off-suite:
   A `+23 more` vs `+22 more`, `frozen=24` vs `25`; B `SURFACE OK … (exec 644)`
   rc0 vs `SURFACE DIVERGED … no execute bit` rc1, `ok=0` vs `ok=1`.
4. Kumitate `scripts/kimi-census.mjs` worktree is dirty (` M`, sha
   `5e8d5913…`, 44770 B, mtime 2026-10-19T22:06:51Z) while the pinned blob at
   `175de6ba` re-reads `83016d45…`; kagi's path is clean and byte-identical to
   its pin.
5. Restore: `MUTATE_RESTORE: OK` both sweeps; scratch pristine copies
   `cmp`-identical to the materialized pinned bytes.
6. 22 suite runs, 0 inconclusive, 0 timeouts, across both sweeps; wall 7.82 s
   (A) and 11.54 s (B) on a 32-cpu host with a 300 s per-run bound.
7. Both spec files gate to `all unique` with first-line readings equal to the
   page's declared sites.

**I.** H held for both appendices on this host: the page is executable cold to
the recorded tables, with zero blocking gaps and zero wrong expectations; the
only improvisation is Appendix B's probe fixture construction (step 8), whose
expected readings pin its semantics well enough that the reconstruction
reproduced them exactly.

**U.** (a) Cross-host stability of the two cost readings (page's own U5);
(b) whether the appendices' literal python-driver route behaves identically to
the harness route (not exercised — latitude taken); (c) whether the concurrent
kumitate edit alters any later reading of that path (not this seat's; the blob
pin is what this record binds to); (d) equivalence of my reconstructed B probe
fixtures to the round-3 note's §7 fixtures (note not readable under the
contamination rule; outputs matched).

COLDREAD: SUFFICIENT (appendixA=8/10 recorded=8/10 appendixB=8/10 recorded=8/10 blocking-gaps=0 wrong-expectations=0 survivors-probed=4/4)

---
L1 integration note (W2RoundTameshi, 2026-10-19): the evidence copy
`.ufo/evidence/kaika-round-1/coldread/SKILL.snapshot.md` was replaced by
`SKILL.snapshot.README` before commit — the snapshot is byte-identical
to `git show 4eb4cf3:SKILL.md` (sha256 `33e3009c…0f81`), so the copy was
redundant, and its text tripped the round's credential sweep. The
`SHA256SUMS.txt` line for it stays as the record of the executed bytes.
