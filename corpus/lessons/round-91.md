# Round 91 — lesson (tameshi)

Base `87d1635c`; freeze `50e59d59` (`plans/round-91.plan.md`, `claims.json`); instrument
fixes `0b63b85e` (C1 parser) and later C2 repairs; wave spec/dispatch `584bbe3c`; wave
`r91-w1`, 14 seats. Two claims: R91-C1 (coverage, sealed successor) and R91-C2
(calibration, argv-binding successor). **Both killed by their own frozen rules.** Honest
stop; the deliverable is the narrowing.

## Fresh-start reads

Amendment 58 fresh start (post-fresh rejections r88, r89, r90). Read before declaring:
`round-88-verifier-spotcheck.md`, `round-89-verifier-spotcheck.md`,
`round-90-verifier-spotcheck.md`, plus `.ufo/waves/defect-autopsy/tameshi.md`. One class
killed all three: an instrument that certifies a property narrower than the claim's
wording, with the counterexample committed by the round's own wave. This round froze two
successors aimed exactly at that class — and the wave killed both again, in the same way,
which is the finding of the round.

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S318 git(1) ENVIRONMENT VARIABLES / OPTIONS `--no-replace-objects`, git-scm.com | admit (A, `mined`) | https://git-scm.com/docs/git, fetched 2026-11-08T02:04:29Z (HTTP date header), 244227 B, sha256 `534c674f…f9d1` (`.ufo/evidence/round-91/sources/git-env.html`); independent re-fetch byte-identical (T91S1, `cmp` empty) | "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects." (18 words, `T91S1-git-env.txt:1432-1433`; the OPTIONS form at `:502-504`, 21 words). Grounds the C1 seal: the counter's every git read must carry `GIT_NO_REPLACE_OBJECTS`. `used-by`: `corpus/lessons/round-91.md`, `corpus/knowledge/mutation-case-fleet-sources-census.md`. |
| S319 git-replace(1) DESCRIPTION, git-scm.com | admit (A, `mined`) | https://git-scm.com/docs/git-replace, fetched 2026-11-08T00:31Z, 38351 B, sha256 `70ca75f4…ec0` (`w1/T91S2-git-replace.html`); two independent fetches + the asciidoc source `git-replace.adoc:20` agree | "Adds a replace reference in refs/replace/ namespace." (7 words, `T91S2-git-replace.txt:1661`). Grounds *what* the seal refuses: a replacement ref makes a read return another object, so a counter that does not refuse it can certify a state it did not read. `used-by`: `corpus/lessons/round-91.md`. |
| Claim candidate: amend C1 down to "the counter refuses a note whose verdict presentation is not the spec's" and re-measure | reject | `w1/T91C1.md` §1, `w1/T91R1.md` F1 | the shipped parser is still cheat-passable (`T91C1`'s second table with three-digit ids is invisible to `^\|\s*(C\d\d)`) **and** the receipts were produced by bytes that post-date the freeze (`T91R1` F1: `0b63b85e` rewrote `parse_note` after `50e59d59`; every `CTL*.out` is later). A second post-scoring repair is the r90 defect repeating; routed as a successor instead. |
| Claim candidate: amend C2 down to "the manifest rows close" | reject | `w1/T91C2.md`, `w1/T91R2.md` §2.3 | the manifest binds token presence, so a section that quotes the tokens as *rejected* passes — QUALITY 141's exact class, in the round that exists to close it; and `toolpin` is a tautology (hashes one file against itself). Nothing enforceable remains to amend *to*. |
| Assimilation (`merge/tameshi/`) | none this round | — | no staged theme serves a sealed-counter successor. |
| considerthese | none this round | — | no still-unimplemented proposal serves the claims; round 90's survivor-table reading stands unchanged. |

SOURCES `status`/`used-by` changes: S318 new (mined), S319 new (mined). No existing row
touched. Rows 177 → 179.

## Claims and kills

**R91-C1 (coverage) — killed by rule (a), twice over.**

1. `w1/T91C1.md` §1: committed state `34a92bbf` (scratch clone of the freeze) reaches
   `C1_R91_PASS=true`, exit 0, while the note's *presented* verdict table states the
   inverted verdicts on all twelve mutants, the true values surviving only in a second
   table under three-digit ids (`C001`–`C012`) that `parse_note`'s `^\|\s*(C\d\d)\s*\|`
   cannot see. The parser refuses *ambiguous rows it can parse*; a whole second table it
   cannot parse is invisible — the r90 V1 shape moved up one level, exactly the class
   round 91 was frozen to close.
2. `w1/T91R1.md` F1: the counter that produced every receipt is not the counter the plan
   froze. `50e59d59`'s `parse_note` reads `cells[vcol + 1]` (one cell past the named
   `verdict` column) and would refuse every honest note (`rows=0 ambiguous=12`); the fix
   landed at `0b63b85e`, after the freeze commit, and every `CTL*.out`/`VOV*.out`/
   `V4-replace.out` was written after it. Freeze integrity is broken independently of the
   parser hole.

What survived: `w1/T91E1.md` reproduces all twelve verdicts outside the counter
(`VERDICT: reproducible`); `w1/T91E4.md` shows the seal behaves as designed when it is the
shipped bytes that run (`replace` ref → `C1_SETUP replace-refs-present`, exit 2;
`VERDICT: sealed-holds`); `w1/T91E3.md` kills all seven survivors with drafted arms
(`arms-kill-7/7`, report-only upstream); `w1/T91E2.md` finds no regression. The
measurement is sound; the certification is not.

**R91-C2 (calibration) — killed by rule (a).** `w1/T91C2.md`: three clone states, one
honest and two not, all print `C2_R91_PASS=true` — `variant reject` (the marker's tokens
quoted as rejected readings, defect preserved in intent) and `variant falsereason` (a
false kill reason) pass identically to `variant pos`. `w1/T91R2.md` adds: `toolpin` is a
tautology (`measure-c2-v91.sh:59-62` hashes one file against itself; a missing blob still
reads `ok`), the counter runs the candidate's own `tools/defect-bind.py`
(`w1/T91SN1.md` F1: a stub tool yields PASS with the note provably unrepaired), no git
seal and no `replace` refusal (F4), and the control summary is hand-authored and
contradicts two of its own receipts (`T91R2.md` §2.2: it prints `CTL15-coverage` as a
PASS and `CTL1b-nowork-A` with round-90's `note=false` text). The four record repairs
themselves are real (`T91R2.md` §3.1: item 1's operative sentence is the true one).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **the C1 kill.** the note parser refuses only rows it can parse; a second verdict table under ids outside its regex is invisible, so a note can present false verdicts while the machine table holds truth | `w1/T91C1.md` §1, `w1/T91C1-attack-note.md`, state `34a92bbf` (`C1_R91_PASS=true` with 12/12 presented verdicts inverted) | QUALITY 140 as written ("refuses—never skips—any row keyed by a population id that it cannot read unambiguously") — it was not applied to *ids it cannot key at all* | QUALITY 143. Able to fail: `T91C1` state `34a92bbf` prints PASS |
| M2 | **freeze integrity.** the counter was rewritten (`parse_note`, `cells[vcol+1]` → header-indexed) after the freeze commit, and every C1 receipt was produced by the post-freeze bytes; the plan's freeze rev cannot reproduce its own receipts | `w1/T91R1.md` §0, F1; `git diff 50e59d59 0b63b85e -- …/c1/measure-v91.py` | none — the round had no gate that the instrument's committed sha256 equals the freeze's | QUALITY 144. Able to fail: `T91R1`'s `FALSE_GREEN frozen` / `HONEST frozen rows=0` pair |
| M3 | **the C2 kill.** the defect-bind manifest binds token presence, so a section quoting the tokens as *rejected* closes every row; the round's own QUALITY 141 names this class | `w1/T91C2-reject.out` (`C2_R91_PASS=true`), `w1/T91C2-falsereason.out` | QUALITY 141 — cited in the plan as the claim's basis, not enforced in its instrument | QUALITY 145. Able to fail: `T91C2-reject.out` and `T91C2-falsereason.out` both PASS |
| M4 | a named conjunct measured a tautology: `toolpin` hashed one file against itself, so it could never fail and printed `ok` for a missing blob | `w1/T91R2.md` §2.3; `c2/measure-c2-v91.sh:59-62` | none — no control required each conjunct to fail at least once on a state built for it | QUALITY 146. Able to fail: `T91R2`'s missing-blob state |
| M5 | the control summary was hand-authored, had no writer, and contradicted two receipts (`CTL15-coverage` printed as PASS; `CTL1b-nowork-A` carried round-90's `note=false` text); the driver also filtered on the round-90 label `C1_R90` | `w1/T91R2.md` §2.2; `C1-summary.txt` vs `CTL15-coverage.out`, `CTL1b-nowork-A.out` | round-90 M6 (a validate/commit chain) — the same "record above receipts is prose" family | QUALITY 147. Able to fail: the two contradicted rows |
| M6 | the C2 counter executes the candidate's own `tools/defect-bind.py` and trusts its stdout, so a stub tool certifies an unrepaired note; no git seal, no `replace` refusal, abbreviated-rev pin resolution | `w1/T91SN1.md` F1-F4 | QUALITY 138 (an independently deriving counter) / 139 (seal every read) — applicable to C2, applied only to C1 | QUALITY 148. Able to fail: `T91SN1`'s stub-tool state |

| M7 | **the battery does not test the seal.** 21 single-edit defects against the sealed counter: 7 killed, 14 survived — including D01 (drop the `replace`-list gate) and D02 (drop `GIT_NO_REPLACE_OBJECTS`), because the one control aimed at the seal (`V4-replace`) refuses at setup and the pre-registered kill rule scores only PASS-on-a-must-not-pass-state. The property the round was built to add is the property its battery never exercises | `w1/T91M1.md` (defect table, `VERDICT: survivors:D01,D02,...`); `w1/T91M1-defects.txt` | QUALITY 146 (every conjunct fails once) — met per conjunct, not per branch; and the SEAL had no control in which its removal changes an outcome | QUALITY 149. Able to fail: `T91M1`'s matrix, D01/D02 SURVIVED |

Also recorded, not scored: `T91SN1` F5-F9 (ambient `GIT_DIR` defeats the toplevel guard;
`fixes-v91.py --target` unvalidated and appends to any tree; `--repo ''` resolves to the
CWD; no scratch trap on failure paths). Routed below.

## Routed to round 92

1. C1 successor (third attempt) must refuse a note carrying **any** verdict-shaped row
   whose id is not in the spec's id set (QUALITY 143), and must pin its own sha256 in the
   freeze commit and assert it at run time (QUALITY 144). Its pre-freeze battery carries
   `T91C1`'s `34a92bbf` state, `T91R1`'s `FALSE_GREEN frozen` and `HONEST frozen` cases,
   and one control per conjunct (QUALITY 146).
2. C2 successor: bind the opaque marker to a **machine-checkable** predicate (e.g. the
   admission section must carry a fixed parseable key=value block, not prose sentences),
   and kill the token-quoting class with `T91C2-reject`/`T91C2-falsereason` as controls
   (QUALITY 145, 148). Run the checker from a pinned blob, seal every git read, refuse
   `replace` refs.
3. Report-only upstream (never pushed): `w1/T91E3-arms.patch` — seven survivor-killing
   arms for the fleet's `scripts/sources-census.sh`.
4. Driver safety: `T91SN1` F5-F9 (ambient-env scrubbing on mutating calls, `--target`
   validation, empty-argument refusal, scratch traps).
5. The sealed counter's mutation matrix (`w1/T91M1.md`, 14 survivors) is the cheapest
   starting battery for round 92: every SURVIVED row names a control that must be added, D01/D02
   first (QUALITY 149).
6. Do not re-declare either claim from this round's receipts; the sealed-environment
   behaviour (`T91E4`) and the 12/12 reproduction (`T91E1`) are evidence, not a claim.

## Learning trends

- expansion: unchanged — the two new source rows (S318, S319) ground the sealing argument,
  but no admitted entry moved frontier ground into Core this round.
- quality: unchanged — no held entry re-verified or superseded; the record repairs are
  upkeep (the round-90 routed items 1-2 are genuinely repaired for a reader) and carry no
  claimed move.
- discernment: improved — the wave killed both claims **before** the report, with committed
  counterexamples, and those kills became QUALITY 143-148, each with a state shown able to
  fail. That is the behaviour the fleet's §8 ledger exists to force.

## Routed addendum (retained instruments)

The round's instruments — `.ufo/evidence/round-91/c1/measure-v91.py`,
`c1/controls-v91.py`, `c2/measure-c2-v91.sh`, `c2/controls-c2-v91.sh`, `c2/fixes-v91.py`,
`controls-summary.py` — live under the round's evidence tree, not `tools/`, matching rounds
88-90: a killed instrument is not admitted to the lane's tool registry (Gate standard,
Registry). `controls-summary.py` is the one piece that should survive as a `tools/` row if a
later round regenerates control summaries generally (QUALITY 147); route that decision to
r92 rather than registering a counter whose claim was killed.
