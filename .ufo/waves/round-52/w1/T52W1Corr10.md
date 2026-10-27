# T52W1Corr10 — correction record for round-51 re-key entry `### The receipt at this boundary`

Scope: C2 m4 evidence only (one of the 20 round-51 re-key correction records). Deliverable:
`.ufo/waves/round-52/w1/T52W1Corr10.json`. No claim decided here; probes are reported as observed.

## Target entry

- Ledger entry: `.ufo/evidence/round-21/coldread/ledger.json` entry with heading
  `### The receipt at this boundary`, `read_rev 02ec217c4d0afabe727fde2e261b7951d28fb4e9`, span 1212–1229,
  `seats[0] T51W2Read10`, `wrong_expectations: 0`, `inputs` = `corpus/knowledge/fleet-kill-rate-ledger.md`
  + `tools/mutate-and-run.sh`. Shown by
  `python3 -c "import json;d=json.load(open('.ufo/evidence/round-21/coldread/ledger.json'));print([e for e in d['entries'] if e['heading']=='### The receipt at this boundary' and e['read_rev'].startswith('02ec217c')])"`.
- Section text at the read revision, `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` lines 1212–1229
  (heading 1212, next heading `### The re-pin semantics, as executed` at 1230).
- Reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read10.md`, present at the read revision and
  byte-identical to the working-tree copy:
  `git show 02ec217c…:.ufo/evidence/round-51/coldread/reads/T51W2Read10.md | sha256sum` =
  `sha256sum .ufo/evidence/round-51/coldread/reads/T51W2Read10.md` =
  `ebee5af23ff5483b21bf653c52c7e04751258c1fa48598179373ef15eb1ec4c4`.

## Findings (2) — statements of the section the reader recorded as not holding at CAND

1. **`class: stale-pointer`** — quote (reader file line 108):
   `**Minor (known class, deepened by this round): anchor rot on `tools/mutate-and-run.sh:733-791`.**`
   Concerns SKILL.md:1225 `(`tools/mutate-and-run.sh:733-791`), so the two `stale` substrates cannot move`.
   The reader recorded the range as **absent at range — anchor rot** (reader line 43): at CAND it holds
   leg-spec heredoc bytes, and the materialization code moved to `regression_case()` `:1222–1402`
   (reader lines 109–114). The claim holds elsewhere (the mechanism is true and selftested) but the pointer
   does not resolve to the cited content.
   Command, run against the read revision's runner bytes too:
   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c…:tools/mutate-and-run.sh | sed -n '733,740p;788,791p'`
   → `@defect B6 | surface-census.sh:371`, `@defect B7 …`, `@defect B8 | tsukuroi-census.sh:935` and the
   leg-3 heredoc tail — leg-spec bytes, not materialization; and
   `… | grep -n "regression_case()"` → `1222:regression_case() {`.
2. **`class: false`** — quote (reader file line 80):
   `so "still not embedded" is false of the runner at`
   Concerns SKILL.md:1227 `Cases 5–6 are still not embedded: their rows carry no `REGRESSION``.
   The reader's split verdict (reader lines 74–84, and again lines 115–119): the ledger-side half holds
   byte-exactly (`fleet-kill-rate-ledger.md:282`), but the runner-side present-tense clause is false of the
   candidate runner — cases 5–6 are embedded since r10-2, and CAND wires 10 legs. "Superseded
   present-tense narration", flagged before by CR32 and Read18, no supersession pointer added.
   Command (run): `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c…:tools/mutate-and-run.sh | grep -n "r10-2 leg 5\|r10-2 leg 6\|want 10"`
   → `850:  # r10-2 leg 5: kagi corpus/checklist-run.sh …`, `925:  # r10-2 leg 6: kumitate scripts/claims-check.mjs …`,
   `2034:  st "leg-count agreement: calls=$lcalls specs=$lfiles nlegs=$lnlegs (want 10)" $?`; and
   `… | grep -n "bash-checklist-run\|js-claims-check"` → leg table `:92`/`:93` plus `regression_case_git bash-checklist-run` at `:1479`.

## Excluded — recorded but not counted

- `fleet-kill-rate-ledger.md:282` — reader verdict **holds** (reader line 44 table row, `"verdict": "holds"` at line 165); ledger byte-identical base→CAND.
- `/tmp/w9-tameshi-t93/*` logs and kept workdir (SKILL.md:1215–1216, 1222) — reader records them
  **absent (ephemeral, expected)**, the known CR32/Read18 class, and calls them historical records of a
  pre-TMPDIR run (reader lines 45–46, 120–124). Disclosed/historical, not a failing statement of the
  section. The section is scoped "Run at the tick", so the paths record where that run wrote.
- `67/67` selftest tally (SKILL.md:1218) and `4 legs` / `cases=4 passed=4` (SKILL.md:1219–1221) — reader
  marks both **historical records** of the `cf41efaa…` tool, corroborated byte-for-byte by the ledger
  (:341, :281/:350), and only "not the current tally / shape" (CAND 107/107, 10 legs). Historical and
  accurate as records → excluded by the item's rule.
- Timestamps `19:58:59Z` vs ledger ER-4 `19:58:18Z` (SKILL.md:1215) — reader: two independent runs,
  consistent (reader lines 85–88); not a mismatch.
- Panel-tool updates (`tally-audit*.py`, `mte-interop.py`) — reader states they touch none of this
  section's anchors (reader lines 125–128).
- The reader's own residual tally agrees: "two known-class residuals (runner anchor rot …; the superseded
  'still not embedded' narration) plus the ephemeral-/tmp and labeled-historical-count notes" (reader
  line 198) — i.e. two not-holding statements, the rest notes.

## Self-check (frozen counter rule)

`check_findings` imported from `.ufo/evidence/round-52/c2/measure.py` (whitespace-collapsed substring,
≥20 chars), run against the reader file; queue receipt
`.ufo/waves/round-52/w1/T52W1Corr10.check.txt`:

```
check_findings -> None
wrong_expectations == len(findings): True
quote len=97 collapsed=97 single-line-at=[108] verbatim=True class=stale-pointer
quote len=49 collapsed=49 single-line-at=[80] verbatim=True class=false
skill_statement single-line-at= [1225] len= 78
skill_statement single-line-at= [1227] len= 66
```

Both quotes are single-line substrings (97 and 49 chars, ≤200) of the reader file;
`wrong_expectations: 2 == len(findings)`. Counter health probe as observed:
`python3 .ufo/evidence/round-52/c2/measure.py --selftest` → `C2_SELFTEST: cases=8 failed=0`, rc 0.
No counter run against the lane revision; this seat produces evidence, not a verdict.

## Bounds

Read-only on the lane (all lane reads via `git show`); wrote only
`.ufo/waves/round-52/w1/T52W1Corr10.json`, `.ufo/waves/round-52/w1/T52W1Corr10.md` and
`.ufo/waves/round-52/w1/T52W1Corr10.check.txt`. Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1Corr10`
created and deleted before yield; no `/tmp` writes, no clone, no git/jj mutation, no tool install.
Ledger edits (the top-level `corrections` list) are not this seat's file; this record is the payload m4
consumes.

## Summary

- Targeted the round-51 re-key entry `### The receipt at this boundary` (read_rev 02ec217c…, T51W2Read10, span 1212–1229).
- Two findings: stale-pointer `tools/mutate-and-run.sh:733-791` (anchor rot, content at :1222–1402) and false "Cases 5–6 are still not embedded" (embedded since r10-2; CAND has 10 legs).
- wrong_expectations = 2 = len(findings); both quotes byte-exact single-line substrings, verified by the frozen `check_findings` (returns None).
- Excluded as holds/disclosed/historical: ledger :282, ephemeral `/tmp/w9-tameshi-t93` logs, historical 67/67 and 4-leg receipts, timestamp difference, panel-tool note.
- Counter selftest observed green: `C2_SELFTEST: cases=8 failed=0`, rc 0.
- Deliverables: `.ufo/waves/round-52/w1/T52W1Corr10.json`, `.ufo/waves/round-52/w1/T52W1Corr10.md`, `.ufo/waves/round-52/w1/T52W1Corr10.check.txt`.
- No claim decided; no lane edits; scratch removed.
