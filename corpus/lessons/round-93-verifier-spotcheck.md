author: hyaku closure (non-author integrator, @m_zfl)

# Round 93 verifier spot-check (non-author integrator, @m_zfl)

Lane `tameshi` round 93, closure judge (non-author). Lane HEAD after round:
`848412ee0d167db99cf81432d0b237fb16d2fdda`; base before round (closure prompt):
`b392f5fa8299d55c698408dd164b4105204195d6`; report base (report text): `4a7e259b`.

## Step-1 conformance

- Report committed in fleet repo by lane identity:
  `git log --format='%an %H' -- .ufo/reports/round-93/tameshi.md` →
  `tameshi-shokunin 7e506e24d3b43723c1e768ab721ffdc57fdc6863` (committed, not orphaned).
- Report has SHONEN heading with one line per box (4 boxes, all `[~]` with evidence pointers) — not a marker.
- Cited commits all exist and are ancestors of `master` (`merge-base --is-ancestor`):
  `b392f5f..848412e` log lists 14 commits (9cad4f6e..848412ee) — all ancestor-ok; base check
  `merge-base --is-ancestor b392f5f 848412e` → ancestor-ok. Lane tip `848412ee` = `master` tip.
- Lane repo clean and pushed: `jj-lane.sh state` → `branch=master local=848412ee remote=848412ee ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` → empty; `ls-remote origin refs/heads/master` → `848412ee` (matches).
- Prompt carries the template contract (§1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 8+, §4 report,
  §5 commit/push scope, §6 hyaku addendum) — conforms.
- Defects are status-neutral and named in notes (see routed items below).

## Per-claim re-check

### R93-C1 (coverage) — re-measured by closure judge
- Ran myself: `python3 -I .ufo/evidence/round-93/c1/measure-v93.py --repo . --rev 848412ee --work /tmp/closure93-work`
  → `C1_R93_PASS=true`, exit 0, `n=12 killed=5 survived=7 mismatched=0 badrows=0 verdict_tables=1`,
  all 19 conjuncts true, `C1_SOURCE S320/S321/S322 row:1,quote:1`. Matches reported values.
- Before (base `4a7e259b`): receipt `nowork-base.out` shows `C1_SETUP spec-absent-at-rev` exit 2 (committed evidence; base spec truly absent at that revision — the before-state has no counter).
- Battery evidence: committed `C1-summary.txt` → `states=35 matched=35 mismatches=0 missing=0` (I inspected head + count matched the report's claim; battery itself not re-executed — the counter re-measure above covers the predicate; R93E3's byte-identical replay receipt is in the wave record).
- Wording: narrowed by A1/A3 (see claims ledger below) — the frozen 12-cell/23-state predicate holds; three record sentences were wider than the instrument and were corrected in `plans/round-93.plan.md` before filing (A1 fence coverage, A2 width rules, A3 self-referential seal). The claim's falsifiable core verifies.
- Verdict: **improved** (coverage decides refusal on verdict content not id shape; both directions controlled). Gate verification: this is the lane's own counter but it executes against committed spec bytes at the landing rev — the `source` conjunct checks located quotes in committed snapshots (S320/S321/S322 `quote:1` observed above), and selfpin/pins/pin all true at rev. A3 (self-referential seal) is a stated residual defect, not a falsifier of this round's predicate.

### R93-C2 (calibration) — re-measured by closure judge
- Ran myself: `python3 -I tools/conjunct-disposition.py --lane . --rev 848412ee` →
  `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`, exit 0.
- Ran myself: `python3 -I tools/conjunct-disposition.py --selftest` → `DISPOSITION_SELFTEST: 6/6 pass`.
- Committed receipts match: `c2-at-landing.out` (`rows=19 falsifiable=17 unfalsifiable=2 findings=0`), `c2-selftest.out` (6/6).
- A4 do-nothing control: committed `c2-cheat-all-unfalsifiable.out` shows the mechanism-worded all-unfalsifiable manifest prints `findings=0` but the frozen counts/kill rule reject it — the lane measured the gap rather than claiming the checker alone suffices.
- Verdict: **improved** at conjunct granularity; rule-level falsifiability incomplete and honestly stated (A6/M8).

### Axis harm check
- `git diff b392f5f 848412e -- SCORECARD.md`: one capability row added (`conjunct-disposition audit`), Round 93 section appended with both claims and `Scores unchanged: depth 10, calibration 8, freshness 9 (delta 0)`.
- Standing sweeps reported byte-identical base→landing (`SELFSTATE rows=26 match=24 stale=2`,
  `RECEIPT_BIND receipts=12 bound=4 corrected=8 unbound=0`, `POINTER_RECHECK rows=12 met=12`,
  `WAVE_RECONCILE rows=6 met=6`, `REGISTRY_CHECK held=74/78` with the same four pre-existing differs) via R93E2 `no-regression` — committed spots consistent; no owned axis harmed.

## Pre-file falsification ledger (addendum §8)

- Ran: `python3 scripts/hyaku/prefile-falsification.py --lane tameshi --round 93 --wave r93-w1`
  → `PREFILE-FALSIFICATION: pass claims=2 rows=13 attack_seats=6 findings=0`, exit 0.
- Ledger `.ufo/waves/round-93/claim-falsification.tsv`: 13 rows covering both claim ids, all six
  attack seats (R93R1, R93R2, R93C1, R93M1, R93SN1, R93CN1) for each claim (6 attack seats × 2 claims = 12, plus C1/R93CN1 row = 13 — all seats present). Four `falsifies-wording` rows (C1: A1/R93R1, A2/R93S1, A3/R93SN1; C2: A4/R93SN1) each name a plan amendment (A1–A4); the rest are `neutral` with reasons.
- Adjudication of the 4 failing rows: all real and reconciled — the wave falsified four sentences of the record before filing and the lane narrowed them in `plans/round-93.plan.md` (A1–A4) and the report. None leaves a claim's stated wording falsified as filed. Verdict: **ledger passes; no claim unverified.**

## Discernment spot-check (LEARNING.md)

Re-opened from `corpus/lessons/round-93.md` `## Gate`:

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S321 GFM §4.10 Tables | admit | `.ufo/evidence/round-93/sources/s321.txt` lines 4396/4496 (429. `github.github.com/gfm/`) | agree | quote shown verbatim: `single header row, a delimiter row separating the header from the data` + `The table is broken at the first empty line…` — ≥1 located source, ≤25-word quotes, admittable. Verbatim present in committed snapshot. |
| S322 CommonMark §4.5 Fenced code blocks | admit | `.ufo/evidence/round-93/sources/s322.txt:2619` (`spec.commonmark.org/0.31.2/`) | agree | quote verified: `A fenced code block begins with a code fence, preceded by up to three spaces of indentation.` (17 words ≤25). |
| S320 sha256sum(1) re-opened | re-opened, no status change | `.ufo/evidence/round-93/sources/s320.html` (snapshot present) | agree | row was re-opened and re-fetched this round; `used-by` correctly extended with registry-change log; census passes. |
| Candidate: relax ID_SHAPE to 3-digit | reject | `.ufo/evidence/round-92/c1/measure-v92.py` + round-92 receipts (committed at prior revs) | agree | widening id shape retains the R92-C1 killer class (honest A13 table refuses); a different keying rule is required, not a wider pattern — rejection is sound. |
| Candidate: key `measured:` line inside a fenced block | reject | `.ufo/waves/round-92/w1/T92C1-A7-measured-in-fence.out` + S322 §4.5 | agree | fenced content is literal text (S322); keying it would refuse honest notes quoting figures in code blocks. |

SOURCES quote check: S321 row (≤25-word quotes, line numbers verified in snapshot) and S322 row (17-word quote verified at line 2619) both hold.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ `tameshi ok …/corpus/SOURCES.md`, exit 0, same pre-existing W04 duplicate-URL warnings (S293/S303/S314/S318). Row count: `grep -c '^|' corpus/SOURCES.md` → 184 pipe-rows (report's 182 = content rows; 2 extra are the header/separator rows). 180→182 content rows as reported.

## Trend verdicts (agree with report, evidence-based)

- **expansion: unchanged** — S321/S322 + one instrument pair entered; no knowledge entry, no frontier ground moved to Core. The report's own reasoning matches AXES.md (a source row is not expansion alone).
- **quality: improved** — verdict-content reader refusing on verdict not id shape (QUALITY 154/155, both directions controlled); doc-linkage rule (157) with the denying-row rejection state; new criteria 159–162 each with a falsifiable receipt; `C1_CONTROLS states=35 matched=35`.
- **discernment: improved** — the round's own wave falsified four record sentences before filing (A1–A4), each narrowed to what the instruments enforce; two HIGH instrument defects (A3 self-referential seal, M9 receipt-guard holes) filed as routed items rather than reported as passes. The ledger pass with 4 named narrowings is direct evidence of self-calibration.

## Routed defects for next round (from the wave, acknowledged by the lane)

1. **A1**: `coverage` scan is fence-blind — route README scan through `block_lines` and require the path as its own cell (not substring).
2. **A2**: width rules — return the delimiter row, add a `delim` finding; decide the remainder-row pad/truncate policy (currently refuses non-header-width data rows though S321 allows them).
3. **A3 (HIGH)**: self-referential seal — anchor the gate identity externally (`fnmatch`/self-pinned bytes) and `die` on pin disagreement; one lane commit currently can execute a foreign gate. Round-94 remediation stated in the lesson.
4. **A4**: C2 `names-the-seal` substring test — add `--min-falsifiable` + a reason test naming a state or digest.
5. **M9**: receipt guard holes — `O_NOFOLLOW`/`lstat` refusal + run-scoped outdir.
6. **M10**: driver `GIT_*` scrubbing (`sealed_env()` on every driver git call) + canary selftest.
7. **M8/A6**: eight rule-level discriminating states (source occurrence half, both width halves, position, figure-exactly-one, verdict-column count, fence, spec count).
8. **M1**: a fixture-assembly assertion that the positive control's transform was honest (no stray edits in the verdict table).

## SHONEN box checkability

All four SHONEN boxes are `[~]` lane-asserted with evidence pointers — no `[x]` claimed. The wave (12 seats, R93E3 byte-identical replay, R93CN1 no-overlap) independently supports boxes 2–4; a fully checkable independent promotion review remains operator-owned.
