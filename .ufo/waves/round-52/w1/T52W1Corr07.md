# T52W1Corr07 — correction record for round-51 cold-read re-key entry `### Reading a receipt — the discipline`

Seat: T52W1Corr07 · round 52 wave 1 · lane `tameshi-shokunin` · contribution to **C2 m4** (one correction record per round-51 re-key entry).
Deliverable: `.ufo/waves/round-52/w1/T52W1Corr07.json`. This report is the seat's only other write.

## Behavior

Read reader `.ufo/evidence/round-51/coldread/reads/T51W2Read07.md` in full (153 lines, 8 rows in `reads.json` plus a findings list and a verification log) and the section bytes at
`read_rev 02ec217c4d0afabe727fde2e261b7951d28fb4e9` (`SKILL.md:965-1009`), then transcribed every statement the reader
recorded as **not** holding at its candidate. Three findings; the ledger entry currently claims zero.

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | sed -n '965,1009p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | sed -n '976p;986p;1003p'
sed -n '40983,41012p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/ledger.json
```

Provenance checks (read-only):
- Reader file is byte-identical at base `ef19d8e1…`, `read_rev 02ec217c…` and `HEAD`: `git show <rev>:.ufo/evidence/round-51/coldread/reads/T51W2Read07.md | sha256sum` → `a451528b8ff54708be3e5c61b9cf864a9a5db4df83cb66c37de7ddbe3e66f736` at all three.
- The ledger entry is `.ufo/evidence/round-21/coldread/ledger.json:40983-41012`: `"class": "record"` (:40989), `"verdict": "verified-record"` (:40990), `"wrong_expectations": 0` (:40992), `"read_rev": "02ec217c…"` (:40995), `"seats": ["T51W2Read07", …]` (:41005-41006).
- The section is keyed correctly: the monitor's own splitter at `read_rev` returns `start 965 end 1009 sha256 ecd74f306a05b96d3f87227de52e6e2bdf74f243ebbd2da232bef0f29b3611c8`, equal to the entry's `sha256` and `skill_sha256` (`python3` import of `.ufo/evidence/round-18/measure.py` `sectionize`, applied to `git show 02ec217c:SKILL.md`). No provenance defect here.

## Findings (3)

Reader verdict vocabulary used: row `claim_state` `stale-at-cand` / `absent`; the reader's own "Findings, strongest first" list numbers them 1, 3 and 2 there.

| # | class | quote (byte-exact from one reader line) | reader line | section statement at `read_rev` |
|---|---|---|---|---|
| 1 | `stale-count` | `The N chain is stale: the runner now wires ten legs` | `reads/T51W2Read07.md:60` (ordinal 2 `note`) | `SKILL.md:976` — "`cases=N passed=N` (D is 15 for checklist-run, 10 for other current legs; N=8 since round 18, N=9 since round 26)." |
| 2 | `stale-pointer` | `` `/tmp/w7-tameshi-1/flip-run.out` does not exist `` | `reads/T51W2Read07.md:141` (finding 3; row ordinal 3 `verdict: "absent"`, `claim_state: "absent"`; row `:64-76`, excerpt `:71`, note `:74`) | `SKILL.md:986` — "… `flips=1)` (negative run, `/tmp/w7-tameshi-1/flip-run.out`)." |
| 3 | `stale-count` | `exits 0 and prints VERDICT: PASS at CAND — but the tally is stale` | `reads/T51W2Read07.md:116` (ordinal 6 `note`) | `SKILL.md:1003-1004` — "`bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 at `cf41efaa…`" |

Detail behind each, as the reader recorded it:

1. **N chain (`SKILL.md:976`).** Reader row ordinal 2 is `verdict: "holds"`, `claim_state: "stale-at-cand"`; its `falsifier` (`:61`) reads "This is the section's strongest falsifier and it STANDS: a reader applying the section at CAND expects cases=9 and gets cases=10", and the `note` (`:60`) says the runner now wires ten legs (`REGRESSION_EXPECT` ten, `:1446`; selftest leg-count agreement `:2033`), so a full replay prints `cases=10`. The section bytes are unchanged between base and candidate, so the expectation is one leg behind.
2. **Dead `/tmp` pointer (`SKILL.md:986`).** Reader row ordinal 3 `verdict: "absent"`, `claim_state: "absent"` (row `:64-76`); the path does not exist (`:71` "ls: cannot access '/tmp/w7-tameshi-1/flip-run.out': No such file or directory — re-confirmed by this seat"), round-16 had already flagged it and no preserved copy is in the tree (`:74`), re-checked in the `falsifier` (`:75`). The reader records the claim's mechanism as independently corroborated, but the pointer itself is dead — the section points a reader at a receipt that cannot be read.
3. **Selftest tally (`SKILL.md:1003`).** Reader row ordinal 6 `claim_state: "stale-at-cand"`; `note` (`:116`) records the command passing but printing `107/107` at CAND (and `106/106` at base, `:113`), while the section prints `67/67` pinned to tool sha `cf41efaa…`. The reader's `falsifier` (`:117`): "the printed tally (107/107) does not match the section's 67/67" and "the printed count is revision-dependent, not a constant."

### Records deliberately not counted

- **Row ordinal 1 (`cf41efaa…` "revision"), row `:36-48`, `note` `:46`** — reader verdict `holds`, `claim_state holds`; the "loose word 'revision'" is recorded as a nuance on a verifying pin ("the pin itself verifies"), so it is a `holds` verdict and is excluded per the item's rule.
- **Row ordinal 5 (round-7 plan gloss), row `:92-104`, `:102-103`** — `holds`; recorded as a supported gloss, not a quote.
- **Rows ordinal 0, 4, 7 (`:22-34`, `:78-90`, `:120-134`)** — `holds`; field set, ledger pointer, r4-2 fixture tolerance.
- **Reader findings 5 and 6 (`:143-144`)** — TMPDIR and panel-tool updates explicitly record *no claim falsified*; disclosed and accurate.
- **"Section resolution" bullets (`:9-10`)** — a monitor/resolver observation about the `###` scan, not a statement of the section.

## Self-check (frozen counter's rule: whitespace-collapsed substring, `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/c2/measure.py` `check_findings`, :82-95)

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 -c "
import json,re
rec=json.load(open('.ufo/waves/round-52/w1/T52W1Corr07.json'))
flat=re.sub(r'\s+',' ',open(rec['reader_file'],encoding='utf-8').read()).strip()
ok=True
for i,f in enumerate(rec['findings']):
    q=re.sub(r'\s+',' ',f['quote']).strip(); hit=q in flat; ok &= hit and 20<=len(q)<=200
    print('quote[%d] len=%d substring=%s :: %s'%(i,len(q),hit,q))
print('wrong_expectations=%d findings=%d all_ok=%s'%(rec['wrong_expectations'],len(rec['findings']),ok and rec['wrong_expectations']==len(rec['findings'])))
"
quote[0] len=51 substring=True :: The N chain is stale: the runner now wires ten legs
quote[1] len=47 substring=True :: `/tmp/w7-tameshi-1/flip-run.out` does not exist
quote[2] len=65 substring=True :: exits 0 and prints VERDICT: PASS at CAND — but the tally is stale
wrong_expectations=3 findings=3 all_ok=True
```

Cross-check with the frozen counter's own function (read-only import, floored seat list has no entry for `T51W2Read07`), reading the file through `git show` at `read_rev`:

```
check_findings: None
quote[0] single-line=True   quote[1] single-line=True   quote[2] single-line=True
skill_statement[0] in-section=True  skill_statement[1] in-section=True  skill_statement[2] in-section=True
```

Each quote is also a substring of a *single* raw line of the reader file (checked above), not a join across lines. All three `skill_statement` strings are exact substrings of the `SKILL.md:965-1009` section after whitespace collapse (the third spans the wrap at `:1003-1004`).

## Gates / counters

- No claim counter was run: C1/C2 verdicts are the L1's deciding run. Nothing here is a verdict. The frozen C2 counter's `check_findings` was *imported* as a pure function to self-check quotes; it was not run as `measure.py --lane … --rev …`, and no `--selftest` was needed (the function's selftest cases are `measure.py:209-212`).
- No scratch directory was created: this item required no clone, fixture or runner execution, so no `/fast/scratch/hyaku/tameshi-r52/T52W1Corr07/` and nothing to delete. No file was written under `/tmp`.
- Tooling: nothing installed or upgraded.
- Import byproduct: importing the frozen counter for the quote check wrote the gitignored `.ufo/evidence/round-52/c2/__pycache__/measure.cpython-314.pyc` (mtime 01:47, `git check-ignore -v` → `__pycache__/`); removed immediately, and `ls .ufo/evidence/round-52/c2/` now shows only `measure.py`.

## Touched surfaces

- Written: `.ufo/waves/round-52/w1/T52W1Corr07.json`, `.ufo/waves/round-52/w1/T52W1Corr07.md` (this file).
- Read-only: lane git objects, `.ufo/evidence/round-51/coldread/reads/T51W2Read07.md`, `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-52/c2/measure.py`, `.ufo/evidence/round-18/measure.py`, `.ufo/evidence/round-52/contract.json`, `corpus/lessons/round-51-verifier-spotcheck.md`.
- No git/jj mutation, no index or jj-state touch, no fleet-root write, no sibling-lane access, no `agent://all` message.

## Observation for the integrator (not a finding against the reader)

- The ledger has **no top-level `"corrections"` list today**: `python3 -c "import json;d=json.load(open('.ufo/evidence/round-21/coldread/ledger.json'));print(sorted(d))"` → `['carried_from', 'entries', 'provenance', 'round21_provenance', 'schema']`, and `grep -n '"corrections"' …/ledger.json` → no match. m4 (`measure.py:21-28`, `:145-165`) requires `corrections` to hold one record per round-51 re-key entry and currently scores `m4=20`; the list must be added with all 20 records, this one among them.
- There are exactly 20 round-51 re-key entries: `grep -c '"read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9"' …/ledger.json` → 20.

## Limits

- The findings are the reader's recorded verdicts, transcribed with byte-exact quotes; this seat did **not** re-run `tools/mutate-and-run.sh --selftest`, did not re-measure the ten-leg `REGRESSION_EXPECT` line, and did not attempt to recover `/tmp/w7-tameshi-1/flip-run.out` (unrecoverable by the reader's own account). The section text and its line anchors at `read_rev` were re-read directly.
- Completeness is bounded by what one reader file records; a second reader of the same section could hold other statements to be false that this record does not carry.

## Summary

- Produced the C2 m4 correction record for re-key entry `### Reading a receipt — the discipline` (`read_rev 02ec217c…`, reader T51W2Read07): 3 findings, `wrong_expectations: 3` against the entry's recorded `0`.
- Findings: N chain `N=9` stale under ten legs (`SKILL.md:976`); dead `/tmp/w7-tameshi-1/flip-run.out` pointer (`:986`); `MUTATE_SELFTEST: 67/67` tally stale vs candidate `107/107` (`:1003`).
- Not counted: the reader's five `holds` rows (including the loose "revision" word) and its two "no claim falsified" notes.
- Every quote verified as a whitespace-collapsed substring of the reader file, single raw line, 47-65 chars; frozen `check_findings` returns `None`.
- Section keying verified against the monitor's own `sectionize` at `read_rev` (`sha256 ecd74f30…` equals the ledger entry).
- Observation: the round-21 ledger still has no top-level `"corrections"` list (20 re-key entries exist); the integrator must add it.
- Wrote only `.ufo/waves/round-52/w1/T52W1Corr07.json` and `.md`; no git/jj mutation, no scratch, no tool installs, no claim verdict.
