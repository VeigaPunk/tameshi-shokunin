# round-95 verifier spot-check — non-author closure review

author: hyaku closure (non-author integrator, @m_zfl)

Round `tameshi` 95, attempt 1. Base `02ff6290945dde18062a366799a774abb50fb365`; lane tip
`cc41a31bf6e3a0241ab06ab6eb9011fde734e8f1` (branch `master`, remote equal). Report
`.ufo/reports/round-95/tameshi.md`, committed on the fleet repo by `tameshi-shokunin
<tameshi@shokunin.local>` at `dfe5d4d6ac0e1c013889574b7ba4610e96621eda` with the filing-record
addendum at `cb3e4b4378f38be81e8a5389bdff983d35fe4870`. I did not author this round and edited
no lane file but this one.

## Conformance (step 1)

| Item | Result |
|---|---|
| Report present at the roster path, committed by the lane identity | pass — both commits authored `tameshi-shokunin <tameshi@shokunin.local>` (`git log --format='%an %H' -- .ufo/reports/round-95/tameshi.md`) |
| `## SHONEN` heading, one line per box | pass — `grep -c '^## SHONEN'` → 1; four `[~]` lines, each with a resolvable pointer and an explicit "No independent promoter review" |
| Every cited lane commit exists and is an ancestor of the branch tip | pass — eleven hashes cited (`0d3fc99b`, `fea47819`, `0685c358`, `20fabad4`, `f219fb0c`, `3ca1981a`, `16cf0d58`, `4bd1e88f`, `3610b46c`, `cc41a31b`, base `02ff6290`); `git cat-file -e` rc 0 and `merge-base --is-ancestor <h> cc41a31b` rc 0 for all |
| No uncommitted round work; pushed | pass — `jj-lane.sh state` prints `branch=master local=cc41a31b remote=cc41a31b ahead=0 behind=0 … untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` → `cc41a31b…` |
| Dispatched prompt carries the template contract | pass — §2 claims/admission, §2b frontier step, §3 L2 floor (8 batched, route map matching `MISSION.md` §L2 concurrency), §4 report contract with the `SHONEN` heading rule, §5 commit/push scope + L0; plus the five child-lane items (report path, commit-before-report ordering at `:521`, `SHONEN` grep, commit-hash citation, lane write scope) |
| Report sections in order | pass — Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN |
| Wave accounting | 13 seats, one v1 wave (`w1-dispatch.json counts.total=13`; roles executor 4, scribe 1, scout 1, reviewer 2, critic 1, mutation-tester 1, sentinel 1, connector 1, revenger 1), all 13 seat reports present under `.ufo/waves/round-95/w1/`; `.ufo/waves/round-95/w1-results.json` records 13 results with `output: null` after the kernel restart — disclosed in the report |
| Stale-lane | respawn-per-round driver; launch/complete digest carried into the round notes; no L0 question opened; no tool installed |
| Marker test | not a marker — real committed work, evidence pointers, resolvable hashes |

Conformance defects named (all status-neutral): the Gate line-number drift (D1 below), the
`w1-results.json` `output: null` handoff (D2), the attack-share parenthetical (D3). None of them
makes the report a marker and none changes the status.

## Claim re-checks (step 2)

Both claims were declared `measured`; neither is exploratory, so no `unprovable-but-better`
ruling arises. The counting commands were re-executed by me at the named revisions (they are the
claims' own instruments, not lane gates); the battery, forge matrix and selftest tallies were
verified from committed receipts per PROTOCOL §Gate standard (Closure consequence).

### R95-C1 — coverage: five presentation classes in the successor note reader

Command re-run (counter blob at `4bd1e88f`, sha256 `5f0d1770…` = the freeze value):

```
python3 -I .ufo/evidence/round-95/c1/measure-v95.py --repo <lane> --rev 4bd1e88f3f488fa7d14fa3b2fb4943b80acfcf01 --work <empty dir>
C1_SUMMARY rev=4bd1e88f… n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0 trivial=0
            witnessed=7/7 note=present mismatched=0 badrows=0 verdict_tables=1
C1_SOURCE S320=row:1,quote:1 S321=row:1,quote:1 S322=row:1,quote:1 S323=row:1,quote:1
C1_R95_PASS=true   exit=0
```

The wording's own revision ("at the instrument revision") was tested literally as well:
`--rev 20fabad4dc64b2feff16853a4cce01d9b324f821` prints the same summary with
`verdict_tables=1 mismatched=0 badrows=0`, `C1_R95_PASS=true`, exit 0; the counter blob at that
revision hashes `5f0d177034173971439be06eb5fbf32dfa8fec4b35a856fc617999e4554ccc2e` (match).

Before-state re-read from the committed receipts (`pre-freeze/before-v94/`): round-94 counter at
`6a2a1fdd` — `indent-code-row` exit 1 `verdict_tables=2`, `C1_BADROWS dup:368:C01 … dup:379:C12`;
`indent-token` exit 1 `ids=false`; `escaped-backslash-pipe` exit 1 `ids=false mismatched0=false`,
`C1_BADROWS width:9:cells=4`; `two-hyphen-delimiter` exit 1; `double-pin` exit 0
`C1_R94_PASS=true`. Do-nothing control at base `02ff6290`: `C1_SETUP spec-absent-at-rev`, exit 2.

Battery: `pre-freeze/controls-run.log:52` prints `C1_CONTROLS states=50 matched=50 mismatches=0
missing=0`; 50 `*.out` receipts exist. The five added states' receipt tails read
`C1_R95_PASS=true` (indent-code-row, indent-token, escaped-backslash-pipe, two-hyphen-delimiter)
and `exit=2 / C1_SETUP self-pin-line-count / C1_R95_PASS=false` (double-pin) — exactly the
frozen lines. 45 receipts carry `counter_sha=5f0d1770…` (the five `D01`–`D05` receipts correctly
carry the digest of the *mutated* counter they ran).

Verdict: **coverage improved** — re-measured (counter) + evidence-verified (battery, before
receipts).

### R95-C2 — calibration: the disposition audit reads receipt bytes

Command re-run at `4bd1e88f`:

```
python3 -I .ufo/evidence/round-95/conjunct-disposition-v95.py --lane <lane> --rev 4bd1e88f… --min-falsifiable 17
DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0   exit=0
python3 -I … --selftest
DISPOSITION_SELFTEST: 11/11 pass   exit=0
```

Manifest binding checked independently: the 17 `state` rows of `conjunct-disposition.json` each
name a receipt under `pre-freeze/controls/` whose `counter_sha=` line equals
`5f0d177034173971439be06eb5fbf32dfa8fec4b35a856fc617999e4554ccc2e`, the sha256 of
`.ufo/evidence/round-95/c1/measure-v95.py` at `4bd1e88f` — 17/17 good, 0 bad. The two
`unfalsifiable` rows (`canary`, `unstable0`) each name a mechanism and a state/digest anchor.

Forge matrix (evidence-verified): 8 checks, 0 failed — `forge-handwritten` v95 exit 1
`DISPOSITION_FINDING receipt-absent-at-rev figure`; `forge-counter-sha` v95 exit 1
`receipt-counter-sha-mismatch mismatched0`; `forge-replace-ref` v95 exit 2
`DISPOSITION_SETUP replace-refs-present`; the round-94 checker prints `findings=0` on both
receipt forgeries and reads the substituted counter. Do-nothing control at base:
`DISPOSITION_SETUP counter-absent-at-rev`, exit 2.

Verdict: **calibration improved** — re-measured (checker + selftest) + evidence-verified (forge
matrix, controls).

## Pre-file falsification ledger (step 2b)

```
python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tameshi --round 95
PREFILE-FALSIFICATION: pass claims=2 rows=12 attack_seats=7 findings=0      exit=0
```

Ledger `.ufo/waves/round-95/claim-falsification.tsv`: 12 rows, both claims covered (6 C1 / 6 C2),
all seven attack seats present (R95R1, R95R2, R95C1, R95M1, R95SN1, R95CN1, R95L1). Three
`falsifies-wording` rows each name a narrowing — R95R1 → plan §A9 (Gate layout, reflowed at
`20fabad4` and re-scored exit 0, which I re-verified above at that revision), R95C1 → §A4
(summary token order), R95SN1 → §A7 (environment-trust limits). I adjudicate all three rows
**real and reconciled**: the claim sentences survive their amended wording, and the falsifier was
a record sentence, not a frozen predicate. No spurious row.

## Discernment spot-check (step 3)

The round's `## Gate` declares **zero source rejects** ("Rejected this round: none"), and the
census corroborates it (`rejected=11` before and after). The reject sample below is therefore
taken from the round's own recorded rejections — the non-discriminating fixture constructions
(`## Mistakes` M2/M3) and the round-94 disposition reject the round carries forward — since a
round that rejects nothing leaves no admit/reject pair inside its Gate.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S323 CommonMark §4.4 Indented code blocks | admit (A, `mined`) | `https://spec.commonmark.org/0.31.2/` re-fetched live 2026-11-08 (HTTP 200, 514 698 B, sha256 `c85f56cc…f0d` byte-identical to `.ufo/evidence/round-95/sources/s323.html`); quote located in the snapshot | agree on the admit, disagree on the cited line | the 16-word quote is verbatim and present in the counter's `norm_text`; but `line 2355` does not carry it under the Gate's stated renderer — the sentence starts at 2358 (see D1) |
| S321 GFM Tables §4.10 (three quotes) | admit (A, `mined`, re-opened no status change) | `https://github.github.com/gfm/` re-fetched live (HTTP 200, sha256 `b153d814…220` = committed `s321.html`) | agree | all three quoted spans are verbatim, ≤25 words, and present in `norm_text` (`quote:1` in the counter); line numbers again off by 3–4 (D1) |
| S320 sha256sum(1) (re-opened) | admit unchanged | `https://man.archlinux.org/man/sha256sum.1.en` re-fetched live (HTTP 200, sha256 `b968bc09…77b` = committed `s320.html`) | agree | the 6-word DESCRIPTION sentence is verbatim; cited `line 84` vs renderer line 88 (D1). The row's other `teaches` clauses are unquoted paraphrase — carried observation, not a broken citation |
| R95S1 fixture `escaped-backslash-pipe`, first construction | reject as non-discriminating, replaced | `pre-freeze/before-v94/escaped-backslash-pipe.out` (v94 exit 1 `ids=false width:9:cells=4` on the corrected five-column fixture) and `plans/round-95.plan.md` §A1 | agree | the first four-column fixture let the round-94 reader pad the row and print `C1_R94_PASS=true`; the do-nothing control caught it, which is exactly the criterion (`captured-by: the round's own do-nothing control`) |
| Round-94 reject, `canary`/`unstable0` declared unfalsifiable | reject (carried) | `conjunct-disposition.json` rows `canary` and `unstable0` at `4bd1e88f` | agree | each reason names a mechanism plus a state (`timeout`) or the `GATE_SHA256` anchor; firing either needs a nondeterministic pinned gate, which the `pin` conjunct forbids |

`sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, `tameshi ok
…/corpus/SOURCES.md`, with the pre-existing W01/W04 warning classes (the round's own S323
duplicate-URL warning is disclosed in the report and does not fail the gate).

My own census over the two commits: base rows 182, A=164 B=14 C=4, mined=148 queued=23
rejected=11; tip rows 183, A=165 B=14 C=4, mined=149 queued=23 rejected=11; malformed rows 0.
Matches the report's before→after.

## Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | improved | five presentation classes newly governed; `C1_R95_PASS=true` re-measured at both the instrument and the records revision; battery 50/50 |
| calibration | improved | receipt bytes read from the object store and bound to the counter digest; both forge sets refused; selftest 11/11; 17/17 manifest receipts bound |
| depth | unchanged | no new recorded mutation case (R95M1: 26 killed / 12 survived of 38; the twelve round-94 survivors do not move); score stays 10 |
| freshness | unchanged | S320–S322 re-opened for `used-by` only; no re-pin (score stays 9) |
| operability | unchanged | instruments extended in place; no new tool row; capability enters the capabilities table instead |
| adjacency | unchanged | R95CN1 records six sibling `split_cells` implementations diverging on `\\|` and edits none |

No axis is harmed: no knowledge entry was removed or superseded (`corpus/knowledge/` diff
empty), no score moved down, and the only registry changes are the three `used-by` appends plus
the S323 add.

## Trend verdicts

- **expansion: unchanged.** No `corpus/knowledge/` entry was added (`git diff --name-status
  02ff6290 cc41a31b -- corpus/knowledge/` → empty), so CORPUS contract rule 4's expansion
  predicate (admitted knowledge on uncovered ground) is not met. The one new row (S323) is a
  registry row; frontier ground advanced (indented literal class now governs the reader) but
  that is a coverage move, not expansion.
- **quality: improved.** Two instruments were strengthened with measured before/after and the
  successor refuses what its predecessor accepted: battery 45 → 50 (50/50), C2 forge matrix
  8/8 with both v95 refusals against v94 `findings=0`; QUALITY 169–172 appended, each with an
  "Able to fail" receipt. Caveat carried: no rule-level kill moves (R95M1) and the sentinel's
  F2–F7 stay open and routed.
- **discernment: improved.** The round's own wave falsified two record sentences before filing
  (Gate layout → A9, reflow at `20fabad4` and re-scored exit 0; summary token order → A4), three
  record-number defects were fixed at `16cf0d58` rather than glossed, and the do-nothing controls
  caught two non-discriminating fixtures (M2/M3). The honest limit: the two HIGH sentinel findings
  are declared as limits (A7), not claimed as protected. Residual: QUALITY 172 was written this
  round and its own Gate still violates it (D1) — an improvement with a named residue, not harm.

## Routed defects for round 96

1. **D1 — Gate cited line numbers are off by 3–4 under the Gate's own stated renderer.** Measured
   with `strip_tags` per the convention `R95S1.md` §2 names (script/style/comments removed, tag →
   one space, entities unescaped, lines right-trimmed) over the committed snapshots:
   S320 `Print or check SHA256 (256-bit) checksums.` → line **88** (Gate says 84);
   S321 `The delimiter row consists of cells whose only content are hyphens` → **4403** (Gate
   4399); S321 `a single header row, …` → **4396** (Gate 4393); S321 `The table is broken at the
   first empty line, …` → **4496** (Gate 4493); S322 `A fenced code block begins with a code
   fence, …` → **2618–2619** (Gate 2615); S323 `An indented code block is composed of …` →
   **2358–2359** (Gate 2355). The registry's own S321 anchor (`line 4496`) contradicts the
   lesson's 4493, so the drift is visible inside the lane. The quotes themselves are exact, ≤25
   words, all present in `norm_text` (`C1_SOURCE … quote:1` ×4), so no claim changes: this is a
   QUALITY 172 violation to re-pin next round, not a claim falsifier. Route to the lesson writer
   (and the `M1`-class "number-drift" rule).
2. **D2 — wave handoff lost its outputs.** `.ufo/waves/round-95/w1-results.json` carries 13
   results with `output: null` after the orchestrator kernel restart; seat verdicts rest on the
   retained seat reports. Already disclosed in the report; route the handoff durability as a
   tooling defect (it overlaps R95SN1 F2–F7, already scheduled for round 96).
3. **D3 — the attack-share parenthetical.** `5/13 by the policy's role set` does not resolve:
   `scripts/hyaku/ufo-wave-policy.json` carries no attack-role list, and the addendum §6 set
   (reviewer, critic, mutation-tester, labrat) gives 4/13 = 31 %, still ≥25 %. Record the share
   against the addendum's named set next round.
4. **D4 — S320's `teaches` paraphrases three sentences** of the page (`reads`/`checks` vs
   `read`/`check`; `--status is silent` vs `don't output anything`). The row carries no quoted
   span for them, so this is not a broken citation; the lesson writer should either quote them
   verbatim or mark them paraphrase. Carried from R95S1 §2.
5. **D5 — the round has no source reject** (Gate: "none"; census `rejected=11` unchanged). Not a
   defect by the contract, but a round with four admits and zero rejects exercises no rejection
   judgment; the next round should either open a candidate it can honestly refuse or record the
   sweep that found none.
