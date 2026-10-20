# Round-12 lesson — DRAFT OUTLINE (LessonScribe, evidence seat)

Status: **outline only, not a lesson.** L1 owns `corpus/lessons/round-12.md`; this file is the seat's only write (plus `capture.txt` beside it). Nothing below is a pass, a landed gate, or outside authority. Anchors: **O** observation · **I** inference · **U** unknown. `[PENDING: …]` marks a field that a sibling seat or L1 must fill from its own artifact; no value is invented here.

Pins at capture (`capture.txt`, 2026-10-20T02:16:27Z): HEAD `18ad5d0`; `corpus/SOURCES.md` committed sha256 `6b34e899…`, worktree sha256 `f8a5ac2e…` (modified, uncommitted, mid-edit by a sibling). `corpus/lessons/round-12.md` exists uncommitted at capture; this outline did not read or edit it. Re-resolve every pin before quoting.

---

## 0. Header and pins

- Revision line: `18ad5d0` (HEAD); worktree dirty (`M corpus/SOURCES.md`, `M corpus/knowledge/witness-scoped-kill-verdict.md`, `?? corpus/lessons/round-12.md`).
- Contract (`corpus/SOURCES.md` contract v1, rule 1): every new row's URL, access date, ≤25-word quote and location go in `## Gate`. This outline proposes **no new rows**.
- Pin table: `[PENDING: L1 fills at write, sha256sum + wc -l per file]`.

## 1. Claims of round 12 (the spec's two only)

| id | claim | state at capture |
|---|---|---|
| C1 calibration | repeated pristine-control gate: N≥3 runs, identical exit/stdout/stderr; nonzero baseline = could-not-evaluate | **not landed** — `tools/repeat-control.py` absent (`capture.txt`, "repeat-control tool"). Claim text stays `[PENDING: gate run output]`. |
| C2 depth | declared-witness split for pinned bash-surface-census (10 defects); existing 6 legs unchanged | **not measured** — BashWitness output absent. Claim text stays `[PENDING: BashWitness summary]`. |

Allowed C1 wording, only after the gate runs: "N identical control runs at revision X; `controls_match` exit 0." Forbidden: "deterministic", "flake-free", "determinism proven", "repeatable verdicts".

## 2. `## Gate`

### 2.1 Gate-sourced claims

Each row is admitted only when its quote is present in the repo or re-opened this round with an access date.

| id | claim | source row | quote status at capture | tier · scope | proposed verdict |
|---|---|---|---|---|---|
| G1 | a pristine control must be green before a verdict is read | S004 (cargo-mutants, §Tests fail in a clean tree?) | **no verbatim quote in repo**; `tests must first pass reliably` appears only in the SOURCES `teaches` cell (`capture.txt`) → `[PENDING: ControlKnowledge re-open]` | A · cargo-mutants' own semantics | `[PENDING]` — admit only with captured quote |
| G1b | baseline green is a witness precondition | S006 (shmutant, §The three verdicts) | **present**: "The selected tests were not green before any defect was injected." (`.ufo/evidence/kaika-round-1/witness/README.md:11`; `corpus/knowledge/witness-scoped-kill-verdict.md:15`) | A · shmutant's own bash semantics only | admissible (existing quote) |
| G2 | repeated executions of one suite can disagree; one green control cannot rule that out | S011 (ISSTA 2019, Shi/Bell/Marinov) | **present**: "mutation scores vary by four percentage points on average between repeated executions" (round-1 Gate row, fetched 2026-10-19T21:43:51Z) | A · flakiness impact on mutation verdicts; not bash-specific | admissible (existing quote) |
| G3 | reruns mitigate flakiness; a mitigation is not a proof | S026 (Google Testing Blog, 2016) | **partial**: "about 1.5% of all test runs reporting a 'flaky' result" present; the `fail-3-in-a-row` quote is `teaches` only → `[PENDING]` | A (company blog; self-reported rates) · Google's pipeline only | admit the mitigation claim only with the captured quote |
| G4 | the gate's exit IDs mean what the gate's interface says | own-work: `tools/repeat-control.py` (spec, not landed) | n/a | own-work · gate interface only | `[PENDING]` — needs landed file, a row allocated by L1 from `S047` (`SOURCES.md:133`), and a `path @ commit` anchor |

### 2.2 Rejected inferences (kept, QUALITY criterion 5)

- **R1 — "N identical green runs prove the control or suite is deterministic."** Rejected.
  - [I] A finite green streak of length N is consistent with a flaky test whose failure period exceeds N; the streak is a sample, not a bound.
  - S040 (TOSEM 2021, tier B secondary) defines flaky as failing inconsistently without changes to the code under test — quote present in the round-1 Gate ("Tests that fail inconsistently, without changes to the code under test, are described as flaky."). The captured definition does **not** itself answer whether finite reruns prove determinism; that question belongs to SourceSurvey's capture `[PENDING]`. This outline does not attribute that answer to S040.
  - S011 (G2) reports 9% of mutant-test pairs with unknown status even under repeated runs → reruns reduce, they do not exclude.
  - Flip condition: a declared bounded state/input space exhaustively run, or a cited source that proves determinism for the named gate. None is in the registry.
- **R2 — "N = 3 is the determinism threshold."** Rejected. [I] The number matches S026's fail-3-in-a-row mark, a mitigation convention; it is not derived from a source. Named as a lane choice.
- **R3 — "byte-identical stdout/stderr is what the source requires."** Open, not admitted as sourced. S028 (Bazel) says the exit code alone decides and "writing any of the strings PASS or FAIL to stdout has no significance to the test runner" (round-1 Gate quote present). Byte equality is therefore a **lane policy** for C1, not a source requirement. `[PENDING: SourceBazel verdict]`.

## 3. `## Mistakes` (append after MK-11; MK-1…MK-11 unchanged)

Format: class · evidence pointer · captured-by · fix. "Candidate" = proposed by this seat from the prior outside verdict; L1 admits or rejects.

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| MK-12 (candidate) | trend token reconciled inconsistently | `corpus/lessons/round-1-verifier-spotcheck.md:17` says "discernment improved"; `SCORECARD.md:118`, `LOG.md:463`, `corpus/lessons/round-1.md:208` say "unprovable-but-better"; `SCORECARD.md:234` defers to "the orchestrator's adjudication" without a token | none | one canonical token; each token cites its outside sample; the other becomes an append-only errata |
| MK-13 (candidate) | spot-check sample excluded the contested admit | spot-check samples K2 admit and S046/S029 rejects (`round-1-verifier-spotcheck.md:12-13`); the disputed K1 box-3 admit (`round-1.md:325`) and critic rejection (`.ufo/waves/kaika-w3/tameshi-critic.md:11`) are not sampled | none (no criterion covers sample composition) | a sample must include ≥1 item on which an outside verdict disagrees, when one exists |
| MK-14 (candidate) | three calibration pins in circulation | candidate 8 (`LOG.md:~611`, lane Gate); reviewer "pin **8**, not 10" (`.ufo/waves/kaika-w3/tameshi-review.md:16`); adjudicated 6 (`corpus/lessons/round-1.md:474-487`; `LOG.md:635-638`) | none | cite only the adjudicated value with its adjudication row |
| MK-15 (candidate) | outside-ness asserted by dispatcher identity | `tameshi-review.md:3` "fresh orchestrator-dispatched task; non-author" vs ER-I1 `round-1.md:207-213` ("dispatched seats cannot supply that outside authority") | PROVINCE/LEARNING rule, fleet file not in this repo | record the dispatcher and the independence rule applied; do not infer independence from a name |

- **Not included here:** the witness-preregistration contamination and the box-3 overclaim as a mined class. A sibling seat (MistakeMining) owns that; L1 merges by evidence, not by duplication. Existing record: `knowledge/witness-scoped-kill-verdict.md` E1 and `round-1.md` MK-10.
- **Named debt, carried:** 19 legacy knowledge entries without provenance headers (MK-7 repair limit); the `SKILL.md` stale status lines (ER-K5).

## 4. Status fields — old → new (contract rule 2: only `status`, `recheck`, `used-by` change; each change logged old→new here)

Old = committed `18ad5d0`. Worktree column = in-flight, uncommitted (not a basis for a logged change until committed).

| id | field | old (18ad5d0) | worktree (in-flight) | new — if condition met | condition |
|---|---|---|---|---|---|
| S004 | used-by | `corpus/knowledge/mutation-score-semantics.md` | + `corpus/knowledge/repeated-control-precondition.md` | same as worktree | file must exist at commit; **missing at capture** |
| S004 | status / recheck | mined / on-release | mined / on-release | unchanged | — |
| S006 | used-by | `…witness-scoped-kill-verdict.md, …mutation-score-semantics.md` | + `corpus/lessons/round-12.md` | add only if the lesson cites S006 in the committed file | path exists at capture (uncommitted) |
| S006 | status / recheck | mined / 90d | mined / 90d | unchanged | cadence not changed by a re-open |
| S026 | status | queued | **mined** | mined | only if `repeated-control-precondition.md` lands with `source:` citing S026. **Worktree flip is premature**: its used-by path is missing, so the contract census `missing:` check fails until it lands |
| S026 | used-by | — | `corpus/knowledge/repeated-control-precondition.md` | same | as above |
| S011 | status | queued | queued | mined only if a knowledge file cites it | otherwise stays queued; unavailable source = Gate note, not a status |
| S040 | status | queued | queued | mined only if cited; tier B, never sole support | — |
| S028 | status | queued | queued | queued (no rejection: R3 limits scope, it does not reject the source) | — |
| all | `opened` | 2026-10-19 | unchanged | unchanged | contract is silent on seat re-opens; `[U]` for L1 to decide — do not rewrite `opened` silently |

New rows: none proposed. If one is needed, L1 allocates from `S047` (`corpus/SOURCES.md:133`) — allocation by a single owner, never by a seat, to avoid two seats taking the same id.

## 5. Prior outside verdict — read, reflected

Sources read (each re-read at capture; line anchors in `capture.txt`):

| source | verdict |
|---|---|
| reviewer `W3ReviewTameshi`, `.ufo/waves/kaika-w3/tameshi-review.md:9-16` | ADMIT WITH CONDITIONS; calibration pin 8 not 10; quality → unchanged; F1/F2 → partly held; spot-check pending by design |
| critic, `.ufo/waves/kaika-w3/tameshi-critic.md:11,20,24-26` | reject K1 as measured at candidate 8; admit K2; admit and reject samples agree |
| orchestrator adjudication, `corpus/lessons/round-1.md:474-487`, `LOG.md:635-638` | K2 admitted; K1 rejected; pin 6; box 3 stays `[~]` with scope note, unscored |
| spot-check, `corpus/lessons/round-1-verifier-spotcheck.md:8-17` | admit/reject samples agree; discernment "improved" |

Disagreements, reflected (not smoothed):

- **D1 — box 3.** The lane admitted `[ ]→[~]` (`round-1.md:325-330`); the critic rejected the increment. Adjudication: not earned. Lesson for round 12: a mark's evidence must cover the mark's whole wording, and the scope line says so (ER-K7, MK-10). Consequence for C2: any declared-witness claim states the executed scope only.
- **D2 — discernment token.** `improved` (spot-check) vs `unprovable-but-better` (SCORECARD, LOG, ER-I1). Unreconciled in the repo. [I] Recommendation to L1, not a decision: keep `unprovable-but-better` until a sample includes the contested admit (MK-13) and the sampler's independence is recorded (MK-15). Opinion, labelled.
- **D3 — pin.** 8 (reviewer and lane candidate) vs 6 (adjudicated). Only 6 is current; 8 stays as history with its date.
- **D4 — is the spot-check outside?** The spot-check treats an orchestrator-dispatched reviewer as non-author; ER-I1 says dispatched seats cannot supply outside authority. `[U]` — fleet rule not in this repo. Report verbatim; do not resolve here.

## 6. Named limits and falsifiers

- **Limits:** C1 measures the control's repeatability over N runs at one host and one revision; it does not measure the suite's flakiness rate. C2 measures one pinned bash leg. [U] whether the N-run window ever catches a late flake.
- **Falsifiers (any one defeats the round-12 lesson):** "deterministic"/"flake-free" attached to a C1 result; N=3 presented as a sourced threshold; byte equality presented as a source requirement; a `mined` flip whose used-by file is absent; a discernment token without a sample pointer; a Gate quote without access date; a claim quoted from a worktree file that differs from the committed revision without saying so.
- **Debt carried:** MK-7 legacy headers (19); ER-K5 `SKILL.md` stale lines; fresh-reader box-3 run; D2 token reconciliation; D4 independence rule.

## 7. Verification L1 should run after integration (not run by this seat)

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git rev-parse HEAD && git status --short
sha256sum corpus/SOURCES.md corpus/lessons/round-12.md
for p in $(awk -F'|' '/^\| *S[0-9]+ *\|/ && NF==13 {s=$9; gsub(/ /,"",s); if (s=="mined") print $12}' corpus/SOURCES.md | tr ',' '\n' | tr -d ' '); do [ "$p" = "—" ] || [ -e "$p" ] || echo "missing: $p"; done
grep -n 'discernment' corpus/lessons/round-1-verifier-spotcheck.md SCORECARD.md LOG.md
python3 tools/repeat-control.py --selftest          # only after the file lands
python3 tools/repeat-control.py --runs 3 --out DIR -- <control argv>   # only after landing
```

## 8. Risks

1. Worktree `corpus/SOURCES.md` is mid-edit by a sibling: S026 flipped to `mined` with a missing used-by path; the census would fail (`capture.txt`, "used-by paths existence").
2. `corpus/lessons/round-12.md` exists uncommitted; this outline may conflict with it. L1 reconciles.
3. S004's verbatim quote is absent from the repo; S026's fail-3 quote is `teaches` only. Both block G1/G3 until captured.
4. S028 (exit-code-decides) and C1's byte-identity are in tension if C1 is framed as a source requirement.
5. Id collision on `S047` if more than one seat allocates.
6. The seat's own "old" values are the committed revision; L1 must pick a single baseline before logging any change.
