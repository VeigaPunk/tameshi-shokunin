# T52W1Corr01 — correction record for round-51 cold-read re-key `T51W2Read01`

Seat: T52W1Corr01 (scribe, calibration lane). L1 TameshiR52, wave 1. Milestone: C2 m4 correction record.
Deliverable: `.ufo/waves/round-52/w1/T52W1Corr01.json` (written; 3 findings).
Section: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`, read_rev
`02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read01`, reader file
`.ufo/evidence/round-51/coldread/reads/T51W2Read01.md`.

## What was read

- `.ufo/evidence/round-52/contract.json` (read, not edited) — C2 `m4` = 20 correction records, one per round-51 re-key entry, verbatim quotes, `wrong_expectations == len(findings)`.
- `.ufo/evidence/round-51/coldread/reads/T51W2Read01.md` in full (`awk END{print NR}` → 75 lines).
- Section text at read_rev: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` → lines 131–245 (heading at 131, next heading at 246).
- Ledger entry for this seat: `python3 -c` over `.ufo/evidence/round-21/coldread/ledger.json` printed `heading` = the exact heading above, `read_rev` = `02ec217c…`, `seats` = `["T51W2Read01", "L1 TameshiR51a3 integration (attempt 3)"]`, `wrong_expectations: 0` (the routed defect: round 51's `refresh.py:227` hard-codes `'wrong_expectations': 0` from code, not from the reader record).

## Findings (3) — every quote is one line of the reader file, byte-exact

| # | class | reader file line | section line | quote (verbatim) |
|---|-------|------------------|--------------|------------------|
| F1 | stale-pointer | `T51W2Read01.md:9` | `SKILL.md:174` | ``raw pointer `tools/mutate-and-run.sh:425`: CAND line 425 is `d = hits[0]`; the `APPLY FAIL … old-string-count=%d expected=1` print is at 433-435`` |
| F2 | stale-pointer | `T51W2Read01.md:10` | `SKILL.md:211` | ``raw pointer `tools/mutate-and-run.sh:569-574`: CAND lines 569-574 are the restore-drift check and `MUTATE_RESTORE: OK`, not the cited division/DEGRADED behavior`` |
| F3 | unsupported | `T51W2Read01.md:65` (`residual_unverified_prose`) | `SKILL.md:228` | ``Section says 'corrected in round 27, seat Read03'; the claimed report path does not exist in the CAND tree`` |

`skill_statement` per finding (quoted from the section, byte-exact, asserted to be a whitespace-squashed substring of `SKILL.md:131-245`):

- F1 — ``the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425``` (`SKILL.md:174`)
- F2 — ``the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574``` (`SKILL.md:211`)
- F3 — ``this shows endpoint identity, not the absence of a transient write (SKILL.md:377-378; corrected in round 27, seat Read03)`` (`SKILL.md:228`)

### Independent check of each finding at read_rev (not taken from the reader)

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:tools/mutate-and-run.sh | awk 'NR>=423 && NR<=436 … NR>=566 && NR<=585'`; observed:

- `425|    d = hits[0]` — the section's `:425` anchor does **not** hold at read_rev.
- `434|        sys.stderr.write('APPLY FAIL id=%s line=%d old-string-count=%d expected=1\n' …)` — the cited failing-count print sits at 433–435, i.e. +9 from the anchor.
- `569|  if [[ "$TARGET_SHA0" != "$target_sha1" …` … `575|    "$TARGET_SHA0" "$target_sha1" "$pristine_sha1"` — `:569-574` is the restore-drift/`MUTATE_RESTORE: OK` block, not pct/DEGRADED.
- `579|  pct=$(( (200 * killed + total) / (2 * total) ))`, `581-583| … printf 'MUTATE: DEGRADED (…)' … exit 1` — the cited behavior is at 578–583.
- Runner length at read_rev: `git show …:tools/mutate-and-run.sh | wc -l` → `2159` (reader's figure confirmed).
- `git show …:tools/mutate-and-run.sh | grep -c "all unique"` → `0` (reader's "no `all unique` literal in its CAND bytes" confirmed).
- `git cat-file -e 02ec217c…:.ufo/waves/round-27/w2/Read03.md` → `fatal: path '…' does not exist in '02ec217c…'`, exit 128; `ls .ufo/waves/round-27/w2/` → `No such file or directory`. F3's cited report path is absent at read_rev.

## Not counted (deliberate exclusions)

- The reader's `holds` pointer rows (`mutation-case-kimi-census.md:*`, `mutation-case-kagi-census.md:*`, `gates-survey-kumitate.md:19-31`, `corpus/README.md` G-R2-1, `SKILL.md:25-27`, `SKILL.md:377-378`) — verdicts are `holds`; the item excludes holds verdicts.
- The `/tmp/<lane>-r<round>-<n>-work/` statement (`SKILL.md:136`): the reader records that the CAND runner defaults to `${TMPDIR:-/tmp}` and that this "does not contradict the documented default namespace" — a disclosed, accurate note, not a failure. It is the subject of C2 m2 through a different surface (the round-51 registry runner row), not of this section.
- The `all unique` attribution to the historical Kimi/Kagi drivers: the reader records the section attributes it to those drivers and the maintained runner reports the failure count instead — consistent, no failing statement.
- The ten-leg panel updates: reader states the section carries no tenth-leg count claim, so nothing there fails.

## Judgment call recorded (F3)

The reader filed the two anchors in its own `findings` array (one aggregated `low` entry) and filed the round-27 attribution under `residual_unverified_prose` / "Residual risk", not in `findings`. I count it because the section states a provenance ("corrected in round 27, seat Read03") whose cited artifact is absent at read_rev — an unsupported premise the reader recorded as fact ("the claimed report path does not exist in the CAND tree"), not a statement it marked accurate. Consequence for the record: `wrong_expectations = 3`, whereas the reader's own array lists 1 aggregated finding; the two anchors are split because each is a distinct stale pointer and C2's frozen floor binds `:425` and `:569-574` separately. If the L1 prefers the reader's own aggregation, dropping F3 and merging F1/F2 yields 1; the verbatim floor `T51W2Read01: [':425', ':569-574']` (`.ufo/evidence/round-52/c2/measure.py:36`) still passes only with both anchors present in the quotes.

## Counter conformance (observed, not a verdict)

Ran the frozen counter's own rule — no counter verdict was taken; only `--selftest` and the frozen `check_findings` helper:

```
python3 -B - <<'EOF'
import sys, json, importlib.util
sys.dont_write_bytecode = True
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec=importlib.util.spec_from_file_location('m52', LANE+'/.ufo/evidence/round-52/c2/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rec=json.load(open(LANE+'/.ufo/waves/round-52/w1/T52W1Corr01.json',encoding='utf-8'))
rd=open(LANE+'/'+rec['reader_file'],encoding='utf-8').read()
print('heading-exact:', rec['heading']=='## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence')
print('read_rev-prefix:', rec['read_rev'].startswith(m.R51_REKEY_REV))
print('reader_file:', rec['reader_file']=='.ufo/evidence/round-51/coldread/reads/T51W2Read01.md')
print('count==len:', rec['wrong_expectations']==len(rec['findings']), len(rec['findings']))
print('check_findings:', m.check_findings(rec['findings'], rd, m.FLOORS['T51W2Read01']))
for f in rec['findings']:
    print('quote', len(m.squash(f['quote'])), 'chars, verbatim=', m.squash(f['quote']) in m.squash(rd), '| floor hits=', [l for l in m.FLOORS['T51W2Read01'] if l in m.squash(f['quote'])])
EOF
```

Output as observed:

```
heading-exact: True
read_rev-prefix: True
reader_file: True
count==len: True 3
check_findings: None
quote 144 chars, verbatim= True | floor hits= [':425']
quote 160 chars, verbatim= True | floor hits= [':569-574']
quote 106 chars, verbatim= True | floor hits= []
```

`check_findings: None` is the frozen rule's pass value (`.ufo/evidence/round-52/c2/measure.py:82-95`); both floor labels `:425` and `:569-574` are covered; each quote squashes to ≥20 and ≤200 chars and is a substring of the whitespace-squashed reader file. `wrong_expectations == len(findings) == 3`.
`python3 -B .ufo/evidence/round-52/c2/measure.py --selftest` → `C2_SELFTEST: cases=8 failed=0`, exit 0 (observed).

Note: the record was validated with the frozen `check_findings`/`FLOORS` symbols, not by running `measure.py --lane … --rev …`; the m4 verdict belongs to the L1's deciding run and is not asserted here.

## Touched surfaces

- Written: `.ufo/waves/round-52/w1/T52W1Corr01.json` (deliverable), `.ufo/waves/round-52/w1/T52W1Corr01.md` (this report).
- Not written: the lane checkout (including `.ufo/evidence/round-21/coldread/ledger.json` — the record is handed to the L1 for insertion into the top-level `corrections` list, which is empty at base: `corrections: 0`), the contract, the fleet repo, sibling lanes, `~/.local/bin`, any PATH dir.
- No git/jj mutation, no index change, no commit. No fixture repo, no clone: every read was `git show` / direct read. Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1Corr01` was used once, only to reproduce the import pattern against a copy of `measure.py` (it wrote no `__pycache__`), and was removed: `rm -rf -- "$S"; ls -d "$S"` → `No such file or directory`. An ignored `__pycache__/measure.cpython-314.pyc` exists under `.ufo/evidence/round-52/c2/` (mtime 2026-10-27T01:47:19-03:00); it is not this seat's — every counter read here ran as `python3 -B` with `sys.dont_write_bytecode = True`, and the reproduction above created none. No tool installed or upgraded.

## Limits

- Only the two runner anchors and the round-27 path absence were independently re-verified; the reader's other statements were taken as recorded (and excluded where it recorded `holds`).
- The reader's base-rev line numbers (`:425` was the count print at base) were not re-derived: the lane's round-51 base rev is not named in the reader file, and re-deriving it is not needed for the CAND-falseness this record states.
- The record counts 3 findings against the reader's 1 aggregated finding (see "Judgment call recorded").

## Summary
- Deliverable `.ufo/waves/round-52/w1/T52W1Corr01.json`: heading/read_rev/reader/reader_file exact, `wrong_expectations = 3`, 3 findings.
- F1 stale-pointer `:425` (reader:9 → `SKILL.md:174`); F2 stale-pointer `:569-574` (reader:10 → `SKILL.md:211`); F3 unsupported round-27 Read03 provenance (reader:65, restated at :74 → `SKILL.md:228`).
- Anchors re-verified at `02ec217c`: runner `:425` is `d = hits[0]`, count print at 434; `:569-574` is restore-drift/OK, pct 579, DEGRADED 581-583.
- `.ufo/waves/round-27/w2/Read03.md` absent at read_rev (`git cat-file -e` exit 128) — F3's ground.
- Frozen `check_findings` (with `FLOORS['T51W2Read01']`) returned `None`; all three quotes verbatim after whitespace squash; floors `:425`/`:569-574` covered.
- `measure.py --selftest` → `cases=8 failed=0`, exit 0. No deciding-run verdict taken.
- Lane checkout unmodified; no clone/fixture/scratch, no git mutation, no tool install.
