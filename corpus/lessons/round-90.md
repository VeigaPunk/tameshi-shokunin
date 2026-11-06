# Round 90 — lesson (tameshi)

Base `4e1c10e0`; expectations alone `33dd6e47`, amendment alone `dd0ddce9`; instruments
`a90218cc`, `3cf905bc`; C2 v2 receipts `a4797ebe`; freeze `3485ceb0` (`plans/round-90.plan.md`);
wave `r90-w1` (14 seats); C2 record repairs `9b5dde78`; C1 landing `bc2c85a6`.
Two claims: R90-C1 (coverage, sourced) and R90-C2 (calibration). Both predicates are met at
landing; both are killed by their own frozen rule (a). Honest stop.

## Fresh-start reads

Amendment 46/47 fresh start (post-fresh rejections: r88, r89). Read before declaring: the
round-87, -88 and -89 closures and spot-checks. One class killed all three: an instrument
certified a subject and a counterfeit printed what the instrument read. This round chose a
claim where the counter executes the subject itself (C1) — and still lost to two read-path
holes in that counter (M3, M4) — and a record-repair claim (C2) whose counter is the same
token-presence class the lane's QUALITY 136/138 already reject (M2).

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S316 gawk(1), Arch manual pages | admit (A, `mined`) | https://man.archlinux.org/man/gawk.1.en, fetched 2026-11-06, HTTP date `Fri, 06 Nov 2026 21:53:11 GMT`, 93111 B, sha256 `0023e3d9…9e10` (`.ufo/evidence/round-90/sources/s-gawk1.html`, text `s-gawk1.txt`) | "An & in the replacement text is replaced with the text that was actually matched." (15 words, `s-gawk1.txt:1026-1028`): mutant C09's `"&"` replacement rewrites the fragment with itself, so it is the strip deleted. Cited by the case note. |
| S317 bash(1), Arch manual pages | admit (A, `mined`) | https://man.archlinux.org/man/bash.1.en, fetched 2026-11-06, HTTP date `Fri, 06 Nov 2026 21:53:12 GMT`, 517346 B, sha256 `8d3bd142…c643` (`…/sources/s-bash1.html`, text `s-bash1.txt`) | "True if file exists and is a regular file." (9 words, the `-f` entry, `s-bash1.txt:3199-3200`; `-e` "True if file exists." at `:3197-3198`): C08 differs only on an existing non-regular path. Scope distinct from S273 (errexit/pipefail). Cited by the case note. |
| GNU manual pages on www.gnu.org (gawk String Functions, Regexp Operator Details; Bash Conditional Expressions) | reject this round (unreachable) | `curl` to www.gnu.org:443 failed to connect after 133-135 s twice and timed out after 25 s with `-4` (`.ufo/evidence/round-90/sources/gnu-unreachable.txt`) | not retrievable at fetch time, so no quote could be located there; the Arch pages render the same upstream man pages. Flip: www.gnu.org reachable; a later round may add the manual as the primary row and supersede. |
| Claim candidate: identity-keyed successor witness (round-89 routed item 1, QUALITY 137) | reject | `corpus/lessons/round-89.md` § Routed; MANIFEST tameshi r86-r89 | four rounds of instrument-certification claims killed by counterfeits; a fifth in the same shape is the same bet. Flip: an observer whose evidence channel a counterfeit cannot write. |
| Assimilation (`merge/tameshi/`) | none this round | — | no staged theme serves a fleet-gate mutation case. |
| considerthese `2026-11-05.md` idea 4 (standing per-tool survivor table) | applied to one gate | `considerthese/2026-11-05.md:73-74` | the case note carries a survivor table with witness, fleet impact and a scratch-proven killing arm per survivor (T90E3, 7/7); the daily panel over `tools/*.py` stays unimplemented. |

SOURCES `status`/`used-by` changes: S316 new (`used-by` corpus/knowledge/mutation-case-fleet-sources-census.md,
corpus/lessons/round-90.md); S317 new (same). No existing row touched. Rows 175 → 177.

## Claims and kills

**R90-C1 (coverage) — predicate met, killed by rule (a).** Counter at `bc2c85a6`:
`n=12 killed=5 survived=7 … witnessed=7/7 note=present mismatched=0`, all conjuncts true,
`C1_R90_PASS=true`, exit 0 (`.ufo/evidence/round-90/landing/c1-at-bc2c85a6.out`). The
measurement itself held every attack aimed at it: T90E1 reproduced 12/12 verdicts in an
ordinary shell with its own driver; T90L1 found them invariant over six environments; 12/12
pre-registered predictions held. The kill is in the counter's read path:

- T90R1 K2: the counter's git reads honour `refs/replace`; a scratch clone whose committed note
  says `C02 = KILLED` prints `C1_R90_PASS=true` under a local replace ref, and `false` with
  `GIT_NO_REPLACE_OBJECTS=1` (`.ufo/waves/round-90/w1/T90R1-probe-defects.out`, V4).
- T90R1 K1: a row carrying two verdict tokens is skipped silently, so a contradicting
  `| C02 | … | KILLED | SURVIVED |` line rides along with a PASS (V1-dup-row).
- Disputed, not counted as the kill: T90C1's prediction copy (a note whose cells are copied
  from `expected.tsv` passes). The state holds the true verdicts, so rule (a) as written does
  not fire; the objection is that the counter certifies cell truth, not provenance. Recorded in
  the note's limits.

**R90-C2 (calibration) — predicate met, killed by rule (a).** Counter at `9b5dde78`:
`rows=ok registry=held`, `C2_R90_PASS=true` (`landing/c2-at-9b5dde78.out`). T90C2 K1: a
registry row whose argv is `python3 -I -c "print('LEDGER_WITNESS_SELFTEST: 21/21 pass')"`
holds, so item 4 is "closed" with a row that runs nothing; K2: a correction that asserts the
wrong count and quotes the right phrase as rejected closes item 2; K3: neutered checker tools
pass the counter (`T90C2-*.out`). The repairs themselves are real (T90R2: all four actually
repaired) and stay landed as record upkeep.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | manifest v1 misread `receipt-tokens` (tokens must lie in the span AND the receipt) and a `doc-contains` token wrapped across a line, so the honest fixes left two rows open | `.ufo/evidence/round-90/pre-freeze/controls/superseded-manifest-v1/C2-pos.out` (`rows=fail` on the honest fix) | the positive control C2-pos, run before the freeze | manifest v2 before the freeze (`3cf905bc`); QUALITY 142. Shown able to fail: the v1 receipt |
| M2 | **the C2 kill.** C2's counter binds token presence and a needle in the row's stdout — the print-binding class of QUALITY 136/138 — while the lane's own round-89 lesson had just rejected "another print-binding counter" | `.ufo/waves/round-90/w1/T90C2.md` K1-K3; `T90C2-forge-registry.out` (`C2_R90_PASS=true`) | QUALITY 136 and 138 — applicable, not applied to a record-repair counter | QUALITY 141. Able to fail: `T90C2-forge-registry.out` passes the frozen counter |
| M3 | **a C1 kill.** a new counter re-opened a hole an older instrument had closed: round 82 hardened `tools/defect-bind.py` with `GIT_NO_REPLACE_OBJECTS`, round 90's `measure.py` reads git objects without it | `T90R1.md` K2; `T90R1-probe-defects.out` V4-replace-env vs V4-replace-sealed | none — the r82 hardening lives in one tool, not in a criterion | QUALITY 139. Able to fail: V4-replace-env prints PASS on a false committed note |
| M4 | **a C1 kill.** the note parser skips (does not refuse) an id-keyed row it cannot parse; the same rule refuses an honest note with a drafted-arm result column (D3) | `T90R1.md` K1, D3; V1-dup-row, R1-draft-column | none | QUALITY 140 (refuse ambiguous id-keyed rows; read verdicts from a named column) |
| M5 | expectation miss, written before results: CTL1-nowork at base was expected `note=absent`; the base has no spec, so the counter refuses at setup | `pre-freeze/expected.tsv` amendment 1 (committed alone in `dd0ddce9` before any control receipt) | the expectations file | amendment committed alone; no re-dating |
| M6 | the C1 landing commit `bc2c85a6` named `corpus/lessons/round-90.md` in S316/S317 `used-by` before the lesson existed, so the census printed E11 at that commit (validate and commit were chained with `;`) | census output in the L1 transcript at `bc2c85a6`: `E11 S316/S317 missing used-by corpus/lessons/round-90.md`, exit 1; repaired by this lesson's commit | the round-end census (exit 0 required) | land the lesson in the same commit as rows that cite it, or chain validate with `&&` before the commit |
| M7 | the controls drivers write their receipts into the frozen evidence tree with `"w"` and no existence guard; re-running them truncates the pre-freeze receipts with non-reproducible content | `T90SN1.md` F2 (also F1 `fixes.py --target` unvalidated, F3 empty path → cwd) | none | routed: receipts to a fresh dir, refuse an existing receipt |

## Routed to round 91

1. C1 successor counter: `GIT_NO_REPLACE_OBJECTS=1` and scrubbed `GIT_*` on every git call, refuse
   a non-empty `git replace -l` (QUALITY 139); refuse ambiguous id-keyed rows and read the verdict
   from a named column (QUALITY 140); pin the fixtures tree oid (T90R1 D4); section-scope the source
   row (D1); ignore fenced lines in the README rule (D2). Its pre-freeze battery includes T90R1's
   V1/V2/V3/V4 and T90C1's prediction copy. Do not rewrite R90's frozen counter or verdict.
2. C2 successor: bind the registry row's argv to the SKILL entry command and the tool blob to its
   pin; assert a correction's operative sentence, not a token (QUALITY 141).
3. Upstream (report-only, never pushed): the seven survivor-killing selftest arms
   (`.ufo/waves/round-90/w1/T90E3-arms.patch`), C12 first — it guards the fleet's own
   multi-path `used-by` convention on 20 lanes (T90CN1).
4. Driver safety: T90SN1 F1-F3, F5-F9.
5. Carried from round 89: the identity-keyed witness (QUALITY 137) and per-branch selftest arms (M10).

## Learning trends

- expansion: a new entry on ground the lane did not hold (the first fleet-root gate), sourced
  (S316, S317 mined this round) and placed in the coverage map (`corpus/README.md` § Round 90 —
  coverage map: the fleet's own registry gate).
- quality: the round-89 entry's missing coverage-map row and the lesson's count and wording
  defects were repaired by append (T90R2: all four routed items actually repaired).
- discernment: the wave killed both claims; the four kill/near-kill classes became QUALITY
  139-142, each with a committed state that shows the check can fail.

## Gate addendum (appended after the scout seat returned)

- Correction to the www.gnu.org rejection row above: wave scout T90S2 fetched three GNU Bash
  manual node pages from www.gnu.org at 21:52:11-21:53:17 GMT (HTTP 200;
  `.ufo/waves/round-90/w1/T90S2-*.html`, `T90S2.md:72-74`), inside the window in which the
  L1's own connections failed (`sources/gnu-unreachable.txt`). So the site was not down; the
  L1's connections failed at its fetch time. The rejection reason is narrowed to "not
  retrievable by the L1 at fetch time"; the decision stands for this round.
- T90S2's three proposed rows (Bash Conditional Expressions, Bash Builtins `read`, Word
  Splitting; placeholder ids S316-S318, which collide with the ids written above): **not
  appended** — redundant this round. The case note's C08 ground is S317 (the same `-e`/`-f`
  text from bash(1)), and C12's mechanism is shown by execution (the witness and the T90E3
  arm), not by a quote. Flip: S317's page drifts or is withdrawn; the gnu.org Conditional
  Expressions node (sha256 `401cf8ec…09fd`) is then the replacement, with a fresh id.
- The id collision is recorded as the census-note risk the assimilation item names: a seat
  proposing ids in parallel with the L1 cannot know the next free id; placeholder ids in seat
  output are never appended as-is.

## Mistakes addendum (appended after the mutation-tester seat returned)

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M8 | the C1 control battery exercises only some of the counter's checks: 20 single-edit weakenings of `measure.py`, 9 killed by the 16 committed controls; four survivors are reachable by a committed lane state (D04 duplicate rows, D05 any S-id, D06 figure numerator only, D19 two verdict cells per row) | `.ufo/waves/round-90/w1/T90M1.md:53-72` (defect table), `:88-93` (reachability proofs) | round-88 M8 / round-89 M10 (one control per check, per branch) — applicable, met per conjunct but not per branch | routed with item 1: the successor's pre-freeze battery carries one committed state per branch, including T90M1's four reachable states; D19 is the same hole as T90R1 K1 |
