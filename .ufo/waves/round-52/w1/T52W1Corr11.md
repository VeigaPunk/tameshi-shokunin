# T52W1Corr11 — correction record for round-51 re-key entry `## The operator's runbook and the six-leg regression (round 10, measured)`

Seat: scribe (wave 1, round 52). Item: one correction record for the round-51 cold-read re-key entry
read by `T51W2Read11`, at `read_rev 02ec217c4d0afabe727fde2e261b7951d28fb4e9`, repairing routed defect 3
(`.ufo/evidence/round-21/coldread/ledger.json` recorded `wrong_expectations: 0` because round 51's
`refresh.py` wrote 0 from code, not from the reader).

Deliverables written (both inside `.ufo/waves/round-52/w1/`; nothing else touched):

- `.ufo/waves/round-52/w1/T52W1Corr11.json` — the record
- `.ufo/waves/round-52/w1/T52W1Corr11.md` — this report

`wrong_expectations: 3`, `findings` length 3, one per falsifier the reader itself recorded as not holding
at its candidate.

## Provenance and method

- Contract read first (never edited): `.ufo/evidence/round-52/contract.json`; frozen counter
  `.ufo/evidence/round-52/c2/measure.py` (m4 docstring and `check_findings`/`m4` code at
  `.ufo/evidence/round-52/c2/measure.py:1-30,90-101,145-170`).
- Reader file read in full from the lane checkout: `.ufo/evidence/round-51/coldread/reads/T51W2Read11.md`
  (36 269 bytes; present at REV: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e 02ec217c4d0afabe727fde2e261b7951d28fb4e9:.ufo/evidence/round-51/coldread/reads/T51W2Read11.md` → exit 0).
- Section text taken from git objects only, never the worktree:
  `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | awk 'NR>=1272 && NR<=1364'`.
- Ledger entry matched at the round-52 base `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`:
  `git -C … show ef19d8e1…:.ufo/evidence/round-21/coldread/ledger.json` → 20 entries with read_rev `02ec217c`,
  `corrections: 0`; the entry for this heading carries `seats: ["T51W2Read11", "L1 TameshiR51a3 integration (attempt 3)"]`,
  `start: 1272`, `end: 1280`, `wrong_expectations: 0`. The heading in the delivered JSON is byte-identical to
  `entry['heading']` (checked by equality in Python, output below).
- No executable claim was re-run: the reader's selftest execution (`T51W2Read11.md:55`, pointer row 15; execution `:99-103`)
  is a record of round 51, not mine, and is reported as the reader's observation only.

## Span conflict, verbatim

The item names lines **1272-1280** as the section text; the ledger entry records `start 1272, end 1280`.
The reader's own resolution is wider: `T51W2Read11.md:13-15` records

> Heading `## The operator's runbook and the six-leg regression (round 10, measured)` re-resolved at
> **SKILL.md:1272**; span **1272–1364**; next heading `## Final pointers — the standing map at the arc's
> close (round 11, measured)` at **:1365**.

Measured here with the frozen counter's own `section()` resolver (`levels=(1,2)` on the SKILL.md text at
`02ec217c`): `reader-resolved section lines: 1272 - 1364`. The three failing statements sit at SKILL.md
**:1305-1306**, **:1321**, i.e. inside the reader-resolved `##` section but outside the ledger's recorded
end 1280 (the recorded end is the first `###` sub-heading, `### The operator's runbook — …` at :1281).
Nothing in 1272-1280 itself fails: the reader's only pointers into that range are
`T51W2Read11.md:40` (ord 0, `:1226-1228`) and `:42` (ord 2, `:1250-1254`), both verdict `holds`. Reported,
not smoothed; the canonical judge decides the span.

## Findings carried into the record (3)

1. **stale-pointer — the leg-list anchor is one line short at its own governed sha.**
   Reader: `.ufo/evidence/round-51/coldread/reads/T51W2Read11.md:71`
   `- **F1 (anchor precision, present at write time): `list :85-89` misses leg 1 at its own governed sha.**`
   (pointer row `:45`, verdict `**off-by-one at its own governed sha; absent at range at CAND**`).
   Section statement: `SKILL.md:1306` — `embedded legs (list `tools/mutate-and-run.sh:85-89`; sources `:90-97`;`.
   Shown by: `git -C … show 606716f7:tools/mutate-and-run.sh | awk 'NR>=80 && NR<=89'` per the reader's
   row `:45` (six entries at :84-89; `js-kimi-census` at :84 outside the cited range). I did not re-run it;
   quoted from the reader.
2. **stale-pointer — the default regression scratch is no longer `/tmp/…`.**
   Reader: `T51W2Read11.md:78`
   `- **F2 (made false by the round's TMPDIR change): the default scratch is no longer `/tmp/…`.**`
   (pointer row `:53`, verdict `**held at governed sha (code :1089); superseded at CAND by the TMPDIR change**`).
   Section statement: `SKILL.md:1321` — ``mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX``.
   Reader's located bytes: CAND `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"` (:149 comment
   "(r51 honours TMPDIR)", code :1432; run :157/:491; selftest :160/:1555) — reader row `:53`. Round-52 C2
   m2/m3c encode the same rule at the page level (`.ufo/evidence/round-52/c2/measure.py:14-15,30-33`).
3. **stale-count — "replays six embedded legs" is ten at the candidate.**
   Reader: `T51W2Read11.md:85`
   `- **F3 (made false by the tenth leg): "replays **six** embedded legs" and the six-shaped receipt lines are`
   (continuation `:86-87`; unrelated second half at `:92`).
   Section statement: `SKILL.md:1305-1306` — ``--regression` replays **six** embedded legs`.
   Reader's located bytes: header `:84` "(… r26 nine; r51 ten)", entries :88-97, pins :614-633, tables
   :634-643, registry :1459-1506, `REGRESSION_EXPECT` ten rates :1446 (`T51W2Read11.md:86-87`). Independent
   corroboration in the sibling reader `T51W2Read12.md:88` ("CAND runner has ten wired legs — header `:84`,
   list `:88-97`"), which is a different seat's record, cited as corroboration only.

## Reader statements deliberately NOT counted (each excluded on the item's own rule)

| reader line | reader text (verdict) | excluded because |
|---|---|---|
| `T51W2Read11.md:44` | `**holds as a governed record; identity triple stale at CAND**` (runbook/tool identity) | a `holds` verdict; the sha governs and verifies at `75ed934d`; the VERSION-ambiguity half is also labelled `holds as text at CAND` at `:67` |
| `:41` | `**holds as a governed record; identity stale at CAND (expected)**` (runbook `e1e349b6…`) | reader marks it expected/disclosed; the 511 L / 31 416 B triple verifies exactly at its revision |
| `:46,:47,:48,:49,:50` | `holds at governed sha; moved at CAND` (`sources :90-97`, `pins/tables :550-559`, `specs :766/:841`, `registry :1132-1141`, exit map `:115-119`) | `holds` verdicts; the section scopes them "line anchors as read at `75ed934d…`, the sha governs" (`SKILL.md:1307-1308`) |
| `:51` | mode mirror `:104-106`, `:932-960` — `holds at governed sha (both verbatim-located); moved at CAND` | `holds` verdict |
| `:52` | `holds at governed sha; moved at CAND` (`:1488-1527` selftest arms) | `holds` verdict |
| `:56` (JSON row `:167`) | `record stands; format anchors verified; shape superseded at CAND` | the receipt is a record at the pinned bytes; its six-shaped receipt lines are already named inside finding 3's verbatim quote |
| `:57` | `record, untraceable; partly corroborated` (owner's 21:00:24Z run) | record-class, reader does not falsify it |
| `:58` | `holds` (`:925-929`) + `Info note F4` | F4 is explicitly "adjacent, not this section's text … No action for this seat" (`:93-95`) |
| `:64` | `absent (ephemeral, expected)` (`/tmp/w10-t10-4-ev/`) | reader marks expected/ephemeral |
| `:124-127` | `**No wrong expectation found**: every checkable recorded value …` | reader's own conclusion about everything else it checked |

Note the reader's own frame (severity bullets `:112-127`; machine verdict `:181`): "The section survives falsification as a sha-governed record with
two currency notes and one off-by-one anchor" — the three recorded falsifiers are F1, F2, F3; F4 is
out-of-section. This record carries exactly those three, with F3 counted once (its second half is a
`holds as text` verdict, see `:67`, `:92`).

## Gates run (observation only; no claim decided here)

- `python3 .ufo/evidence/round-52/c2/measure.py --selftest` →
  `C2_SELFTEST: cases=8 failed=0`, rc 0 (8 `SELFTEST … ok` lines). The frozen counter was **not** run
  against the lane: the corrections list is empty at the base (`corrections: 0`) and filling it is the
  integration owner's write, not this seat's.
- m4-shaped check of this one record against the reader bytes at `02ec217c` and the ledger entry at
  `ef19d8e1` (frozen `check_findings`, `reader_file` equality, count equality): `M4-SHAPE AT BASE: OK`.
- Required quote self-check (frozen rule: collapse whitespace, ≥20 chars, substring of the reader file) —
  output pasted verbatim:

```
finding1 len=50 substring=True class=stale-pointer
finding2 len=87 substring=True class=stale-pointer
finding3 len=102 substring=True class=stale-count
wrong_expectations=3 len(findings)=3 equal=True
rc=0
```

command:

```
python3 -c "
import json,re,sys
rec=json.load(open('.ufo/waves/round-52/w1/T52W1Corr11.json'))
flat=re.sub(r'\s+',' ',open('.ufo/evidence/round-51/coldread/reads/T51W2Read11.md').read())
for i,f in enumerate(rec['findings'],1):
    q=re.sub(r'\s+',' ',f['quote']); print('finding%d len=%d substring=%s class=%s'%(i,len(q),q in flat,f['class']))
print('wrong_expectations=%d len(findings)=%d equal=%s'%(rec['wrong_expectations'],len(rec['findings']),rec['wrong_expectations']==len(rec['findings'])))
"
```

and the same three quotes also verify against the committed bytes at REV
(`git -C … show 02ec217c…:.ufo/evidence/round-51/coldread/reads/T51W2Read11.md` → `check_findings(...) is None`).

- `skill_statement` locating: `list `tools/mutate-and-run.sh:85-89`` → SKILL.md:1306; ``mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX``
  → SKILL.md:1321; ``--regression` replays **six** embedded legs`` → SKILL.md:1305-1306 (wrap-joined, present
  in the section after whitespace collapse; reported as `[]` for the single-line locator, `in-section: True`).
  All three are inside the reader-resolved section (1272-1364).

## Out of scope / not done

- No edit to `.ufo/evidence/round-21/coldread/ledger.json` (the 20-entry `corrections` list is the
  integration owner's write; this seat exports one record in the m4 shape).
- No product code, no judge, no counter run against the lane, no git/jj mutation, no `agent://all`, no
  `/home/vgpnk/Projects/shokunin` writes, no sibling-lane writes.
- No tools installed or upgraded (uv/npm/pacman untouched; pacman transactions are paused host-wide).
- No scratch directory was needed: every read was `git show` from the lane's object store plus Python on
  tracked files, so `/fast/scratch/hyaku/tameshi-r52/T52W1Corr11/` was never created (verified absent) and
  nothing had to be deleted. No `/tmp` writes.

## Summary

- Delivered `.ufo/waves/round-52/w1/T52W1Corr11.json` for entry `## The operator's runbook and the six-leg regression (round 10, measured)`, reader `T51W2Read11`, `read_rev 02ec217c…`.
- `wrong_expectations: 3` = `len(findings)` = 3: F1 (leg-list anchor `:85-89` off by one, stale-pointer), F2 (`/tmp` default scratch superseded by TMPDIR, stale-pointer), F3 (six legs, ten at CAND, stale-count).
- Every quote is a byte-exact substring of the reader file after whitespace collapse (50/87/102 chars) and also verifies against the committed bytes at `02ec217c`.
- Exclusions are named per reader line: `holds` verdicts, `(expected)`/ephemeral/record-class notes, and F4 (reader: "adjacent, not this section's text").
- Span conflict reported verbatim: ledger entry records 1272-1280, reader resolves 1272-1364; the three failing statements are SKILL.md:1305-1306, :1321, inside the section, outside the recorded end.
- Gates: `C2_SELFTEST: cases=8 failed=0` rc 0; m4-shaped check `OK`; the counter was not run against the lane (no claim decided).
- Nothing in the lane checkout was modified apart from this report and the JSON record; no scratch, no tool installs.
