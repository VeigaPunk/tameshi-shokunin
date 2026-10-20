# C04FrontierMap — round 17: frontier rows and coverage-map rows

Seat: `TameshiR17.C04FrontierMap` (connector, wave 1, leaf). Lane tip read:
`98bea7da5801f4bc58e4187690ee1687c8a5061f`. No lane file was edited. Every
line number below is at that rev; `git diff --stat -- corpus/README.md
PROVINCE.md` is empty, so working-tree line numbers equal committed ones.

## Verdict

**No frontier row advances.** Exactly one row must be annotated: **F7**
(`corpus/README.md:84`) — two round-17 mechanisms sit on its ground without
measuring its next move. Four near-misses (F3, F4, F5, F8) need an explicit
"not advanced" sentence or the block will be misread. Coverage: one new
`knowledge/` row (new entry), two addenda keyed to existing maintained-ground
rows (`:184` dispositions, `:152` pin-disposition method), **no row for any new
instrument as an instrument**. `PROVINCE.md` and the `## Fleet round lessons`
table are unchanged.

One structural finding drives this: **no seat prompt in the validated wave
spec names any frontier row** (`spec1.json`, 67 items, regex `F[0-9]+\b` → 0
matches). Frontier annotation is unowned by the wave plan; W05 drafts it from
its own target, so this report is the only row-level input to that draft.

## Evidence

| # | Command (read-only) | Observed |
|---|---|---|
| 1 | `git show 98bea7d:corpus/README.md \| wc -l` | `237`; round blocks appended at `:123, :148, :180, :195, :219`; frontier table `:78-87` |
| 2 | `grep -n '^## \|^\| F[0-9]' corpus/README.md` | F4 `:81`, F7 `:84`, F8 `:85`; top coverage map `:3-16`; addendum `:38-62`; round-14 row `:184`; round-13 F7 row `:152`; operator-runbook row `:55`; fleet-lessons table `:22-28` |
| 3 | preamble `:68-73` + status correction `:105-121` | a ground reads `held` only when (a) an admitted `knowledge/` entry with `source:` cites a `mined` `SOURCES.md` row **and** (b) its next move in the table is measured |
| 4 | `git ls-tree -r --name-only 98bea7d corpus/knowledge \| wc -l` | `24` notes; `ground:` present on **4** (F1 `mutation-score-semantics`, F2 `witness-scoped-kill-verdict`, F3 `repeated-control-precondition`, F7 `incremental-pin-disposition`), absent on **20** |
| 5 | `git show 98bea7d:corpus/README.md \| sed -n '89,104p'` | Known gaps still says “New entries carry the header (2 of 21 now)”; measured at `98bea7d`: **5 of 24** notes have `^source:` in their first 5 lines |
| 6 | `git cat-file -e 98bea7d:tools/registry.json` | `fatal: … does not exist` — the registry is a new file, not a moved one |
| 7 | round-17 manifests (written by X01/X02) | `schema: evidence-dispositions-v2`; `supersedes` = the round-14 v1 files; `historical_inputs` = the four `tools/` paths pinned by `.ufo/evidence/round-13/expected.json:9-12` (`pin-disposition.py`, `witness-metadata.py`, `bash-witness-study.py`, `mutate-and-run.sh`) at rev `4acc607d…`; `dispositions.json` 12 rows (11 effective + 1 superseded); `dispositions-before.json` 12 rows, all effective, and it carries the `producer_before` row the contract requires to stay unresolved (the 1-failed outcome is the contract’s claim, [INFERENCE] here — I did not run the gate) |
| 8 | `git show 98bea7d:tools/evidence-disposition.py \| grep -n SCHEMA` | `SCHEMA = "evidence-dispositions-v1"` (`:94`); `expected_input_digest_mismatch` at `:1190, :1755`; no `supersedes`/`historical_inputs` in the dispositions schema |
| 9 | W06 draft (`w1/W06RunbookJj.md`) | corrects HEAD→branch-tip in `operator-runbook.md`; **adds no entry-command registry section** |
| 10 | W03 draft (`w1/W03SkillR17Draft.md`) | appends a SKILL.md section with the round-17 gate/probe registry (incl. `registry-check.py` rows); `tools/registry.json`/`registry-check.py` are not yet in the tree |
| 11 | W02 draft (`w1/W02KnowledgeDraft.md`) | new note `knowledge/input-keyed-coldread-credit.md`, with `ground: F<L1>` left for the L1; its §3 open items (write-mode opens, `realpath`, hash timing) are X08's contract to settle |
| 12 | S03 (`w1/S03RunPinDisposition.md`) | 21 sibling repos: 3 detached (kaidoku, kama, tameshi) and **each detached at its own branch tip**; none detached away from its tip; `pin-disposition.py` at the tip is byte-identical to the round-13 pin and contains no branch read |

## Frontier matrix (row-level)

| Row | Relation to this round | Verdict | Why (evidence) |
|---|---|---|---|
| F1 `:78` | none | untouched | no ledger leg emitted as schema JSON |
| F2 `:79` | none | untouched | no witness split, no bash leg |
| F3 `:80` | `registry-check` is a monitor, not a repeated control | **not advanced** | each registry row executes once and compares one exit/stdout; no N ≥ 3 tuple comparison; `tools/repeat-control.py` is unchanged this round |
| F4 `:81` | input-keyed credit looks like snapshot invalidation | **not advanced** | the unit is a cold-read credit ledger, not a gate’s expected-value update path; no gate survey (“counted per surveyed gate” is F4’s next move and is not performed); F4’s candidates S013–S017/S045 are not engaged by the new note |
| F5 `:82` | `registry-check --rev` clones into a fleet-mirror layout | **not advanced** | layout mirroring is not environment normalization; no `env -i LANG=C TZ=UTC` comparison; no gate selftests measured under it |
| F6 `:83` | none | untouched | no survivor fixture work |
| **F7 `:84`** | v2 dispositions read pinned historical instrument bytes; cold-read credit becomes input-keyed | **annotate; stays `open`** | both are unchanged-inputs reuse predicates, but neither classifies a **per-leg mutation reuse decision**: no recorded mutation leg or sibling target gate is swept, no successor sweep exists, every recorded leg keeps `result_reuse=not_established` (the registry-check runs lane entry commands, which includes selftests and the disposition gate — not mutation legs). F7’s next move (“pin-level cadence only → per-leg reuse decisions classified”) is unmeasured |
| F8 `:85` | none | **not advanced** | this is a repair round with no mutation sweep at all; the round-16 sentence “F8 needs a mutant-side survivor probe tied to an independently anchored expectation” remains exactly true |
| F9/F10 `:86-87` | none | untouched | no LLM pilot, no PBT generator |

## Row-level recommendations

### R1 — frontier annotation for F7 (required)

Target: append a `## Round 17 — …` block after `:237`; do **not** edit the
table row `:84` (round-16 precedent: “Superseded readings, dated, not
rewritten”). Use the round-13 block’s column shape so evidence has a home.

```markdown
| Note / frontier | Scope | Source / evidence |
|---|---|---|
| `corpus/README.md` frontier **F7** | Stays `open`. Round 17 adds an unchanged-inputs reuse predicate at lane-file granularity in two places: the appended v2 disposition manifest re-reads the four `tools/` paths pinned by round-13 `expected.json` from their blob at `4acc607d` (realpath repo-identity guard; evidence paths refused), and the cold-read ledger credits an executed bucket only when every traced input still has its recorded sha256 at REV. Neither is F7's next move: no recorded mutation leg or sibling target gate is swept, no successor sweep exists, and `result_reuse` remains `not_established` for every recorded leg. The F7 note's §3 ("the lane's pin object is coarser than either reuse predicate") stays true for mutant verdicts; the input-keyed rule's artifact is cold-read credit, not a mutation verdict. | `../tools/evidence-disposition.py`; `.ufo/evidence/round-17/dispositions.json`, `dispositions-before.json`, `op1-redbefore-98bea7d.txt`; `.ufo/evidence/round-17/coldread/` (only what exists at landing); `lessons/round-16-verifier-spotcheck.md` §2/§6; S003/S041 unchanged; Round-17 source rows per SOURCES.md |
```

Constraints on the text: say “stays `open`”, never “advances to held”; if the
word “advances” is used at all, scope it exactly as round 13 did
(“F7 advances from pin-cadence prose to a bounded machine-readable
disposition method, not a full incremental result cache”) plus “not to held”.
Do not cite a wave-2 `ledger.json` before it exists; an index row is a claim
written when the file exists (`/home/vgpnk/Projects/shokunin/CORPUS.md:46`).

### R2 — explicit non-advance lines (required, one sentence each)

Put these in the same appended block, in prose under the table. They are
cheap and they stop the three most likely misreads of this round’s machinery.

```text
F3 not advanced: registry-check executes each row once; no N≥3 repeated control
was run and repeat-control.py is unchanged.
F4 not advanced: the cold-read ledger is evidence bookkeeping, not a gate
expected-value update path; no gate update path was surveyed.
F5 not advanced: the fleet-mirror clone layout is not environment
normalization; no env -i comparison was run.
F8 not advanced: round 17 runs no mutation sweep; the round-16 F8 boundary
stands unchanged.
```

### R3 — coverage-map row for the new knowledge entry (required, conditional on the file landing)

Shape it like the round-16 row (`Note | Holds | Sources`). Write it only after
`corpus/knowledge/input-keyed-coldread-credit.md` exists; `Holds` must describe
what the note says, not the claim it is supposed to support. The source ids
must be minted, opened, and `mined` in `SOURCES.md` in the same round
(`QUALITY.md:10`); the strace row (S16 seat) is the external source, the lane
lesson and `measure.py` are own-work.

```markdown
| Note | Holds | Sources |
|---|---|---|
| `knowledge/input-keyed-coldread-credit.md` | Why sha-only cold-read credit goes stale: a bucket kept credit at an unchanged section sha while a lane file its commands ran moved (R16-C2b; round-14 bucket SKILL.md:1563-1596 kept `97cf436b` credit while `tools/mutate-and-run.sh` moved under its commands). Rule: an entry with `commands_executed_count>0` credits only if every traced lane input still has its recorded sha256 at REV, else `inputs-unrecorded` / `input-missing:<path>` / `input-drift:<path>`; inputs captured by `trace-inputs.py` (strace), limits named (undeclared interpreter/env/absence/write-mode inputs), re-measured with `measure.py --rev REV`; lane assertion, no promotion | S0xx (strace(1) — L1 mints); S0xx (round-16 spot-check §2/§6, if minted as own-work); `.ufo/evidence/round-16/coldread/ledger.json` |
```

Do not put `.ufo/evidence/round-17/coldread/` in `Sources` as W05 Draft A does
— it is evidence, not a `SOURCES.md` row; put it in `Holds` only if it exists
at landing.

### R4 — maintained-ground row for dispositions v2 (required)

Key it to the existing round-14 row at `:184` (“calibration of retained
expectations”); do **not** rewrite `:184`, and do not restate the round-14
twelve-row ledger as if it changed.

```markdown
| calibration of retained expectations — dispositions v2 | v1 (`evidence-dispositions-v1`) behaviour unchanged; v2 is additive: `supersedes` names the v1 manifest it supersedes (pinned in `inputs`), and `historical_inputs` re-reads a declared `tools/` path from its pinned rev (`git cat-file blob <rev>:<path>`) after a realpath repo-identity guard. Evidence paths are refused (`historical_input_forbidden`), unpinned keys refused (`historical_input_unknown`), unavailable rev/object refused (`historical_input_unavailable`); the digest must still equal the expected pin (`expected_input_digest_mismatch`). Live tree, branch tip: `.ufo/evidence/round-17/dispositions.json` → 0 clean, 11 effective + 1 superseded; `dispositions-before.json` → 1 failed with `producer_before` unresolved (a clean exit here would be a defect). The round-14 manifest and its twelve counted observations stay immutable; only the live-tree verdict is superseded. | `lessons/round-16-verifier-spotcheck.md` §3/§6 R16-OP1; `.ufo/evidence/round-17/dispositions.json`, `dispositions-before.json`, `op1-redbefore-98bea7d.txt`; S0xx (Build Systems à la Carte — verifying traces, L1 mints) |
```

### R5 — F7 method correction for `pin-disposition.py` (required)

This is a second `incremental-pin-disposition.md` row (the note already carries
a round-14 “empirical correction8” row at `:185`), not an edit of `:152`.

```markdown
| `knowledge/incremental-pin-disposition.md`, round-17 method correction | The `head` observation is corrected prospectively for jj colocation: attached HEAD → its branch; detached → `refs/remotes/origin/HEAD`'s branch, else `refs/heads/master`, else `refs/heads/main`; `head_differs_from_branch` is informational. Measured at the tip: three detached repos (kaidoku, kama, tameshi), each at its own branch tip; no repo was detached away from its tip, so no recorded round-13 disposition changes. The round-13 receipt and its `head` fields stay historical; `result_reuse` stays `not_established`. | `.ufo/waves/round-17/w1/S03RunPinDisposition.md`; `.ufo/evidence/round-17/jj/head-vs-branch.sh`; `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditTameshi.md` §1.2/§2.3; S0xx if a git plumbing source is opened (L1 mints) |
```

Phrase it “no recorded disposition changes **today**”, not “the method was
wrong”: at `98bea7d` the tool is byte-identical to its round-13 pin and the
round-13 readings were made under git semantics (S03 §C2).

### R6 — `registry-check.py` gets no coverage-map row (decision)

Coverage-map rows are note-indexed (`Note | Holds | Sources`), and W06’s
runbook draft adds no registry section, so row `:55`
(`knowledge/operator-runbook.md`) must **not** gain a registry claim. The
monitor is documented by W03’s SKILL.md registry table. Its index row is
`SCORECARD.md` `## Capabilities` — and per `AXES.md` §Capabilities (fleet
root) it may enter only after the round demonstrates it running (the L1’s
`--rev` red-before / tip green-after run), not on the wave-1 build.
Recommendation: capability row “entry-command registry replay”, evidence
`python3 tools/registry-check.py --rev REV --registry tools/registry.json --json`
→ `REGISTRY_CHECK: held=N/M`, first-working round 17 — **after** the executed
receipt exists. The existing “effective expectation reconciliation” row is not
a new capability; add the round-17 live-tree clean run to its evidence pointer
(the capability is restored, not gained), again only after the receipt.

### R7 — adjacent numeric correction (required if Known gaps is touched)

Known gaps (`:89-104`) carries a false present-tense count: “2 of 21 now”
against a measured 5 of 24 at `98bea7d`. Adding an entry increases both
numbers. If the block touches it, replace with the measured form and command:

```text
`for f in corpus/knowledge/*.md; do head -5 "$f" | grep -c '^source:'; done | sort | uniq -c` → `5 1` and `19 0` at 98bea7d (5 of 24 notes; 6 of 25 once the round-17 entry lands with its trio).
```

### R8 — `PROVINCE.md`: no change (decision)

No frontier row moves to Core, and the round measures no new sibling surface
(the only reads are the fleet’s own repos, and no gate runs). PROVINCE’s Core
appends have been for surface changes (the seventh mutation leg) and gate-count
corrections, not lane instruments. Appending a Core paragraph for
`registry-check`/`measure.py` would assert a capability entry the round has not
yet demonstrated. Keep `:40-42` (“F1–F10 in `corpus/README.md`”) as-is.

### R9 — `## Fleet round lessons` table: do not add W05’s Draft B (decision)

The table (`:22-28`) holds exactly one row, `lessons/round-1.md`, labelled the
fleet round; rounds 12–16 appended `## Round N` blocks and added no row. A
round-17 row there would make the table’s scope untrue (one fleet round plus
one lane round) and would imply a fleet round 17 exists. Put the round-17
lesson pointer in the `## Round 17` block instead. If the L1 overrules, the
table must be backfilled 12–16 first — out of this round’s scope.

## Contradictions found in landed drafts (named, not smoothed)

1. **W02 leaves `ground: F<L1>`.** Assign no frontier id. Only 4 of 24 notes
   carry `ground:`; 20 carry none. Labeling a calibration method as F7 would
   put a “frontier entry” in the record whose next move is unmeasured, and
   would let a later reader cite the F7 row as its ground. Remove the
   `ground:` line; if kinship is wanted, a body sentence suffices: “same
   unchanged-inputs predicate class as F7’s reuse rule; not a mutation-leg
   reuse classification”.
2. **W05 Draft C** says “under QUALITY 10 it cannot move F3 or F7”. The correct
   authority is the Frontier preamble (`:68-73`) plus the round-1 status
   correction (`:105-121`, “only when its next move is measured”); F3 is
   unrelated to the entry and naming it invites the wrong comparison. Its
   “no ground moves to `held`” sentence is right and should be kept verbatim.
3. **W05 Draft A** puts `.ufo/evidence/round-17/coldread/` in `Sources`. That
   is evidence, not a mined `SOURCES.md` row; the census rejects a used-by path
   that does not exist at landing and would silently index an unrun ledger.
4. **W05 Draft B** conflicts with the table’s own scope (R9 above).
5. **Round-16 block sentence** “Round 16 records mutant-side probes, but
   against SurvivorPrep's pristine-derived expectations only” stays untouched;
   round 17 adds no probe, so nothing in that block is superseded by this round.

## Post-install verification (for the L1, not run here)

```sh
R=<landing rev>; TIP=98bea7da5801f4bc58e4187690ee1687c8a5061f
git show $TIP:corpus/README.md | sed -n '84p'                   # F7 status still `open` at the base
git show $R:corpus/README.md | grep -c '^## Round 17'           # 1 after install
git show $R:corpus/README.md | sed -n '84p'                     # same F7 row; append-only kept the line
git show $R:corpus/README.md | grep -c 'F7'                     # table row + block rows; expect >= 2
for f in corpus/knowledge/*.md; do printf '%s ' "${f##*/}"; grep -m1 '^ground:' "$f" || echo none; done | wc -l   # 25 after the entry
git show $R:corpus/knowledge/input-keyed-coldread-credit.md | head -5 | grep -c '^source:\|^verified-at:\|^recheck:'  # 3
```

Also confirm the appended block adds no claim that the F7 status cell changed,
and that `corpus/README.md` line count only grows (append-only).

## Tools

No tool installed or updated (no need; read-only git/grep/python3). Scratch:
none used beyond reading committed bytes.

## Verdict

built — F7 is the only frontier row this round must annotate (stays `open`);
F3/F4/F5/F8 are explicitly not advanced; the new instruments map to one new
knowledge row and two maintained-ground addenda, not to instrument rows, and
`PROVINCE.md` needs no change.
