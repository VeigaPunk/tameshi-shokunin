# T52W1Corr03 — correction record for round-51 cold-read re-key entry `### The protocol — ordered, fail-closed`

Seat `T52W1Corr03`, round 52 wave 1, lane `tameshi-shokunin`. Item: supply the correction record for the
round-21 cold-read ledger entry whose round-51 re-key (`read_rev 02ec217c…`) recorded
`wrong_expectations: 0` from code (routed defect 3 of
`corpus/lessons/round-51-verifier-spotcheck.md:128-129`: "`coldread/refresh.py:224-227` writes
`wrong_expectations: 0` for every re-keyed section, but T51W2Read20 recorded false statements").

Deliverable: `.ufo/waves/round-52/w1/T52W1Corr03.json` (one record, `wrong_expectations = 1`).
Verification receipt: `.ufo/waves/round-52/w1/T52W1Corr03.verify.txt`.

## Target entry (read-only, not edited)

- `.ufo/evidence/round-21/coldread/ledger.json:40868-40895` (entry index 513): `"heading": "### The protocol —
  ordered, fail-closed"` (`:40871`), `"wrong_expectations": 0` (`:40876`), `"read_rev":
  "02ec217c4d0afabe727fde2e261b7951d28fb4e9"` (`:40879`), seats `["T51W2Read03", "L1 TameshiR51a3 integration
  (attempt 3)"]`. The ledger has **no** top-level `corrections` key yet (`'corrections' in ledger → False`), and
  zero records for this entry — the m4-shaped defect this seat supplies one record for. Merging the record into
  the ledger is the L1/integration's edit, not this seat's (lane read-only outside this wave dir).
- Command: `python3 -c` over `.ufo/evidence/round-21/coldread/ledger.json` (see receipt, `ledger entry seats=…
  wrong_expectations=0`, `corrections key present=False; records for this entry now=0`).

## Reader file (read in full)

`.ufo/evidence/round-51/coldread/reads/T51W2Read03.md` (191 lines; reader re-keyed the same section at candidate
`6d8c11e378aa90b12650808e1b79270742935f15`, section bytes identical to its base). Its own verdict token, at
`T51W2Read03.md:119`, is `"verdict": "holds-with-one-standing-falsified-clause"` — the reader recorded exactly
one failed statement.

## Findings (1)

### 1. `false` — the `--workdir` safety clause (section step 1, SKILL.md:839)

- `quote` (reader `T51W2Read03.md:35`, the P9 table row; byte-exact substring of that ONE line, 179 chars after
  whitespace collapse):
  `step 1 clause: "the original is never a write target unless \`--workdir\` is its own directory (keep scratch apart)" (839) | :490–494, :500, :518, :519, :524, :548 | **FALSIFIED**`
- `class`: `false`
- `skill_statement` (SKILL.md:839 at `02ec217c`, verbatim):
  `the original is never a write target unless \`--workdir\` is its own directory (keep scratch apart)`
- Reader's recording of it: `T51W2Read03.md:47` — "**F1 — the workdir clause (P9) is false at candidate;
  standing, documented by round-27 Read08, never fixed.**"; `:48` restates the claim and gives the mechanism;
  `:145` (`"verdict": "FALSIFIED (standing; documented round-27 Read08, never fixed; not caused by r51
  changes)"`); `:178` (`falsifier_checked`).

Why it still stands at `read_rev` (my own read of the read_rev bytes, not a rerun of the reader):

| Check | Command | Observed |
|---|---|---|
| runner bytes identical to the candidate the reader measured | `git -C . show 02ec217c:tools/mutate-and-run.sh \| sha256sum` | `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda  -` (2159 lines), equal to the ledger entry's pinned `inputs["tools/mutate-and-run.sh"]` |
| `--workdir` handling has no guard | `git show 02ec217c:tools/mutate-and-run.sh \| sed -n '490,494p'` | `:490` `if [[ -z "$WORKDIR" ]]; then`, `:491` `mktemp -d "${TMPDIR:-/tmp}/…"`, `:493` `mkdir -p "$WORKDIR" …` — only create, no refusal of workdir == target dir |
| fixed-name outputs are written into `--workdir` | same, lines `500, 518, 519, 524, 548` | `:500` `PRISTINE="$WORKDIR/pristine.$(basename "$TARGET_ABS")"`, `:518` `> "$WORKDIR/defects.tsv"`, `:519` `… "$WORKDIR/spec.copy"`, `:524` `mutant="$WORKDIR/mutant-$id.$(basename "$TARGET_ABS")"`, `:548` `… > "$WORKDIR/results.tsv"` |
| the statement is still in the section at `read_rev` | `git show 02ec217c:SKILL.md \| sed -n '827,857p'` | section `### The protocol — ordered, fail-closed` at `SKILL.md:827-857` (31 lines); the clause is at `:839` |

So a target named `results.tsv`/`defects.tsv`/`spec.copy` inside `--workdir` is overwritten by the sweep, which
is what falsifies the sentence's named condition; the reader records this as pre-existing (round-27 Read08,
never fixed) and not caused by the round-51 edits. That is a disclosed *pre-existing* failure, not a
disclosed-and-accurate one — it counts.

## Reader statements deliberately NOT counted (with the reader's own verdict token)

The reader marked these `holds` and they are excluded by the item's rule ("Do not count a reader's 'holds'
verdicts"):

- `T51W2Read03.md:131` — `"verdict": "holds (imprecise: stdout, not per-defect logs; standing since round 27)"`
  for "every run log carries its own `MUTATE_TOOL` pin" (SKILL.md:831). Reader row `P5` = **holds**.
- `:159` — `"holds (wording overlap standing; …)"` for "KILLED (suite exit ≠ 0)" (SKILL.md:845). Reader row
  `P13` = **holds** ("superseded by the INCONCLUSIVE carve-out in the same sentence").
- `:163` — `"holds (incomplete: pristine sha also compared; DRIFT -> SETUP exit 2 unstated; standing)"` for the
  restore re-check (SKILL.md:847-848). Reader row `P14` = **holds**, an omission, not a false statement.
- `:171` — `"holds (list incomplete: omits defects.tsv and evidence/control.out; standing)"` for the evidence
  list (SKILL.md:851-852). Reader row `P16` = **holds**, an omission.
- Reader falsifiers `F6` (r51 TMPDIR change), `F7` (tenth leg), `F8` (four panel-tool updates): recorded
  "checked, no falsity" — no section statement contradicted.
- All other pointers `P1–P4, P6–P8, P10–P12, P15, P17`: **holds** at candidate.

No stale-pointer, unsupported-premise or stale-count failures were recorded by this reader. `findings` would be
`[]` only if the reader had recorded none; it recorded one, so `wrong_expectations: 1`.

## Gates / checks run (observed output, pasted)

Frozen counter rule, applied to the deliverable
(`.ufo/evidence/round-52/c2/measure.py:check_findings`, imported read-only; reader text pulled from the git
object at `read_rev`):

```
$ python3 - # frozen-rule check: check_findings(T52W1Corr03.json, reader file at read_rev) + per-quote substring
check_findings -> None
QUOTE len=179 in[20,200]=True substring_of_collapsed_reader=True substring_of_single_line=True
quote source line: .ufo/evidence/round-51/coldread/reads/T51W2Read03.md:35
section found=True lines=31
section range: SKILL.md:827-857
skill_statement in section -> True
ledger entry seats=['T51W2Read03'] wrong_expectations=0
ledger corrections key present=False; records for this entry now=0 (m4 bad while 0)
probe (not a verdict): reader_file exact=True wrong_expectations==len(findings)=True
```

Counter selftest (the only counter run this seat performs; no counter was run against the lane tree):

```
$ python3 .ufo/evidence/round-52/c2/measure.py --selftest
SELFTEST leg-count ok
SELFTEST section-stops ok
SELFTEST quote-verbatim ok
SELFTEST quote-forged ok
SELFTEST quote-short ok
SELFTEST floor ok
SELFTEST range ok
SELFTEST range-miss ok
C2_SELFTEST: cases=8 failed=0
```

A local probe (not a verdict) inserting the record into an in-memory copy of the ledger's `corrections` list
yields `records=1 reader_file_ok=True check=None count_ok=True` for `T51W2Read03` — i.e. the record has the
shape m4 consumes (`heading`, `read_rev`, `reader`, `reader_file`, `findings`, `wrong_expectations`) and no
floor applies to this seat (`FLOORS` names only `T51W2Read20` and `T51W2Read01`).

## Touched surfaces

- Wrote: `.ufo/waves/round-52/w1/T52W1Corr03.json`, `.ufo/waves/round-52/w1/T52W1Corr03.md`,
  `.ufo/waves/round-52/w1/T52W1Corr03.verify.txt`. Nothing else was created or modified.
- Not edited (read-only): `.ufo/evidence/round-21/coldread/ledger.json`, `SKILL.md`, `tools/*`,
  `.ufo/evidence/round-52/c2/measure.py`, `.ufo/evidence/round-51/**`.

## Out of scope / limits

- Merging this record into `.ufo/evidence/round-21/coldread/ledger.json` (and updating that entry's own
  `wrong_expectations`, which the L1 may prefer to supersede with a corrected count) is not this seat's edit.
- The reader's four standing `holds (imprecise/incomplete)` notes are recorded here but not counted; if the L1
  wants them reflected, they belong to `minor_gaps`, not to `wrong_expectations`.
- No tools installed or upgraded (no pacman transaction attempted; pacman is paused host-wide anyway).
- No scratch directory was needed: every check read git objects (`git show`) or the reader file; no clone, no
  fixture repo, no `/tmp` or scratch path is cited.
- No counter was run against the lane or a clone; the only counter execution is `--selftest`.

## Summary

- Supplied the m4-shaped correction record for ledger entry index 513 (`### The protocol — ordered, fail-closed`,
  `read_rev 02ec217c…`, reader `T51W2Read03`), which the round-51 `refresh.py` had stamped `wrong_expectations: 0`.
- One finding, class `false`: SKILL.md:839's "the original is never a write target unless `--workdir` is its own
  directory", recorded FALSIFIED at reader `T51W2Read03.md:35`/`:47`.
- Re-checked at `read_rev` bytes: runner sha `977de470…` (write sites `:500, :518, :519, :524, :548`; no workdir
  guard `:490-494`), section at `SKILL.md:827-857`, clause at `:839`.
- `wrong_expectations = 1 = len(findings)`; frozen `check_findings` returns `None`; quote is 179 chars, verbatim on
  one reader line.
- Four reader `holds (imprecise/incomplete)` notes (`:131, :159, :163, :171`) and falsifiers F6–F8 were checked and
  not counted.
- Counter selftest: `C2_SELFTEST: cases=8 failed=0`. Receipt: `.ufo/waves/round-52/w1/T52W1Corr03.verify.txt`.
