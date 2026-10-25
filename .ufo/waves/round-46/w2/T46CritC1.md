seat: T46CritC1
item: attacked C1 (calibration) as declared in `contract.json` vs delivered at CONTENT — reproduced both cells, re-derived all 22 row-vs-observation tuples with the counter's own helpers, proved the frozen predicate accepts a truncated restatement and rejects the exact printed line, and checked the restated set for independence from C2/C3 and for any "calibration improved" sentence.

Round 46, wave 2, critic on claim C1. I am not an author of the standing tables, the statements list, the counter or wave 1's observations. Read-only on the lane: the only lane file I wrote is this report. All scratch under `/tmp/tameshi-r46-T46CritC1/`. No git/jj mutation in the lane, the fleet repo or a sibling lane (only `git clone`, `git checkout --detach`, `git show`, `git diff` inside `/tmp`). No tool installed or upgraded; no `pacman` transaction attempted.

## Setup

```
W=/tmp/tameshi-r46-T46CritC1; mkdir -p $W
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/work-base-clone
git -C $W/work-base-clone checkout -q --detach 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
```
The counter's own `setup()` builds the two clones it uses (`$W/work-before/{clone,fleet}`, `$W/work-after/{clone,fleet}`); both were checked out by the counter at the rev named below and every later command names its own `-C <clone>`.

## 1. The before cell is exact (reproduced byte for byte)

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433 \
  --base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d \
  --work /tmp/tameshi-r46-T46CritC1/work-before
```
exit 1, last line:
```
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C1_R46_PASS=false
```
Saved to `$W/before.stdout`; `diff -u` against `.ufo/evidence/round-46/before/c1-at-freeze.stdout` → no output; both files sha256 `fa50f36d2aeee0b46193bf4b3ae460480a5a41ca2f0a21970a1d24127096dba9`. The two mismatches are exactly what the cell says: `axis/calibration: claimed=8 observed=6` and `cap/six-leg regression ledger: claimed=REGRESSION: PASS (cases=9 passed=9 …)|0 observed=REGRESSION: PASS (cases=9 passed=9|0`. **The before cell is not an overstatement.**

## 2. The after cell is `total=0` at CONTENT (my own run, not the L1's receipt)

```
python3 .../calibration/measure.py --lane <lane> --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 \
  --base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --work /tmp/tameshi-r46-T46CritC1/work-after
```
exit 0, last line:
```
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 append_only=1 total=0 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C1_R46_PASS=true
```
All 22 `STATEMENT` lines print `MATCH` with identical claimed/observed tuples (saved `$W/after.stdout`). `--selftest` at CONTENT: `C1_R46_SELFTEST: cases=18 failed=0` / `VERDICT: PASS`, exit 0.

Independent re-derivation (`$W/compare.py`): `SCORECARD.md` read from git at CONTENT, parsed with the counter's `last_rows`/`claim_of`; observed value from the counter's own `obs-*.stdout` through `pick_line`; exit from my run; **sha recomputed here** as `git show REV:<sha_file> | sha256 | first 12`. Result: 20 of 22 statements MATCH on value+exit+sha; the two `UNOBSERVABLE` rows of my script are script artifacts, not counter defects — `bounded ANSI-C code_view` has no obs file of its own because it shares the frozen command with `tally-audit-v3 runner audit` (F3), and the `calibration` obs file is truncated to its last 200000 bytes so `json.loads` fails on the file while the counter parses the in-memory text. I resolved both separately:
```
git show 6f2168e…:tools/tally-audit-v3.py | sha256sum | cut -c1-12   -> da8c1ef4b30c   (row states da8c1ef4b30c)
python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev 6f2168e… > $W/coldread-content.json
python3 -c "import json;d=json.load(open('$W/coldread-content.json'));print(d['calibration_restraint_score'])"  -> 6
```
So my own computation of `mismatches` is 0, `unparsed` 0, `unobservable` 0 — the after cell reproduces. Append-only: `git show 683eedd:SCORECARD.md` (207,916 bytes) is a byte prefix of the CONTENT file (225,496 bytes) — `startswith=True`.

## Findings

### F1 — HIGH — the restated `calibration` row states a section count its own frozen command contradicts at REV (independently reproduces `w2/T46ReobsA.md` F1)

Attacks `SCORECARD.md:2199` (the deciding calibration standing row) and, through it, the C1 statement "state exactly the value … that the statement's frozen command prints at REV". Row text at CONTENT:
```
| calibration | 6 | Restraint score of the strict cold-read monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` (`calibration_restraint_score`; `box3_full_page=false`, 60 of 64 sections credited): … |
```
Command (same clone, same live fleet, only `--rev` differs):
```
python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev 6f2168e…
python3 -c "import json;c=json.load(open('…'))['coldread'];print(c['sections_covered'],c['sections_total'])"  -> 55 64
python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev 683eedd…
                                                                                          -> 60 64
```
`60 of 64` is the **base** value; at REV the command prints `55 of 64`. The five sections that lose credit are `## Standing rules`, `## Mutation-sweep recipe …`, `## Kill-rate bands …`, `## Cross-language divergence …`, `## Third case …`; at base each is `credited`, at REV each carries `input-drift:` vetoes naming `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*` — files this round appended (`git diff --stat 683eedd 6f2168e` → `SCORECARD.md | 64 +`, `LOG.md | 30 +`, `PROVINCE.md | 17 +`, `corpus/QUALITY.md | 66 +`, `corpus/README.md | 12 +`, `corpus/SOURCES.md | 3 +`). So the round's own records caused the drop and the row still states the pre-round number.

Why C1 cannot see it: `claim_of()` for `kind == 'axis'` returns `(cells[1],)` — only the integer score — and the statement's `obs` is `'monitor'` (the JSON `calibration_restraint_score`). The Rule cell's other numbers are outside the predicate, so `total=0` certifies a row whose stated observation is false at REV. `AXES.md:15` defines calibration as "SHONEN.md/SCORECARD entries match observed repo state", so by the axis definition this is a calibration mismatch, not prose.

Fix (smallest safe): state `55 of 64 sections credited` in that cell (the counter still passes, because it compares only `6`), or narrow the claim's wording to the score integer and drop the section count from the row. Do not read the current row as "no harm" — the round's appends are what moved it.

### F2 — HIGH — the frozen predicate accepts a truncated restatement and rejects the exact printed line (sharpens `w2/T46ReobsB.md` F1 from LOW on the row to HIGH on the claim)

Attacks the C1 statement's "state exactly the value … that the statement's frozen command prints at REV", via `SCORECARD.md:2178` and `statements.json`'s `obs` for that statement.

Row at CONTENT states `REGRESSION: PASS (cases=9 passed=9` (unbalanced, no ellipsis). My run's own captured output, line 50:
```
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```
The frozen `obs` is `^(REGRESSION: \w+ \(cases=\d+ passed=\d+)`, i.e. a **prefix** capture, so the row can only ever quote the first 38 characters. Fixture proof with the counter's own `measure()` (`$W/truncation-fixture.py`, one statement, command prints `RESULT: PASS (cases=9 passed=9; extra=x)`, obs `^(RESULT: \w+ \(cases=\d+ passed=\d+)`):
```
A_row_states_capture            -> exit=0 total=0 C1_R46_PASS=true
B_row_states_full_printed_line  -> exit=1 mismatches=1 total=1 C1_R46_PASS=false
```
So for this statement `total=0` **requires** a truncated quote and the exact printed line is counted a mismatch: the claim's word "exactly" is unreachable through the frozen predicate. Wave 1's before state quoted the same fragment *with* an explicit `…`; the restatement removed the ellipsis and the truncation became silent, which is what the counter certifies.

Second instance of the same class (lower severity): `retained invocation-context gate`'s row quotes `SELFTEST: PASS (49/49)`, the printed line is `selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)`; the capture is a balanced phrase, so a reader is not misled, but it is still a substring, not the line. No other statement's quoted value is a proper substring of its printed line (my `compare.py` truncation check flags exactly these two).

Fix: either amend the claim's wording to "the row states the statement's `obs` capture of the output", or (pre-data only, no longer possible) widen the regex to `^(REGRESSION: \w+ \(cases=\d+ passed=\d+[^)]*\))` and restate the full line. Post-data, the honest record is a note in the row that the quote is the counter's capture (which would then not match the counter either) — the L1 must choose between a passing counter and a true quote for this one row.

### F3 — LOW — `bounded ANSI-C code_view` is the same frozen statement as `tally-audit-v3 runner audit`

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 - <<'E'
import json, hashlib
d=json.load(open('.ufo/evidence/round-46/calibration/statements.json'))['statements']
seen={}
for s in d:
    k=(tuple(s['argv']),s['cwd'],s['obs'],s.get('sha_file'),s['kind'])
    seen.setdefault(hashlib.sha256(repr(k).encode()).hexdigest()[:8],[]).append(s['id'])
print('DUPES:', [v for v in seen.values() if len(v)>1])
E
-> DUPES: [['tally-audit-v3 runner audit', 'bounded ANSI-C code_view']]
```
Both entries are `["python3","tools/tally-audit-v3.py","--selftest"]`, `cwd=clone`, obs `^(TALLY_AUDIT_V3_SELFTEST: \d+/\d+ pass)`, `sha_file=tools/tally-audit-v3.py` — key hash `ba276aaf` for both.
`measure()` caches observations by that key, so the two statements share **one** execution and one `obs-*.stdout` (my script's `UNOBSERVABLE` for the second row is exactly this). `statements=22` therefore covers 21 distinct commands; a single tool regression would produce two mismatches from one cause, and the "22 frozen statements" count is 22 rows, not 22 independent observations. Not a value defect (the row count is honest as "19 capability rows"), but the claim's surface should say "22 rows (21 distinct commands)".

### F4 — LOW — the restated set is independent of C2 and C3 except the registry row, which depends on C3's three rows

- No pinned tool changed base→CONTENT: `git diff --stat 683eedd 6f2168e -- tools/ .ufo/evidence/kaika-round-1/sources-census-v2.sh .ufo/evidence/round-21/coldread/ .ufo/evidence/round-45/` prints nothing (only `.ufo/evidence/round-46/{calibration/*,contract.json}` appear when those paths are included). `SHONEN.md` is not in the 112-file diff.
- Freshness statement is rev-insensitive here: the round-45 counter prints `population=73 … fresh=71 score=9` at **both** `--rev 683eedd` and `--rev 6f2168e` (run at base: `C1_R45: … population=73 entries=73 verified=73 … fresh=71 score=9 … rev=683eedd…`; at CONTENT the counter's own obs file carries the same line with `rev=6f2168e…`). The three new rows do not enter its population.
- Depth statement reads `tools/mutate-and-run.sh`, unchanged.
- **Registry row depends on C3**: the census counts `corpus/SOURCES.md` rows; before `rows=117`, at CONTENT `rows=120`, and `corpus/SOURCES.md` grew by exactly 3 lines (C3's S258/S259/S260). So C1's after cell is unreachable without C3's rows, and a C3 failure (rows not appended) would flip this row to MISMATCH while the other 21 values stand. The other 21 restated values are causally independent of C2 and C3.
- Separately, the **calibration** row's stated value was invalidated by the round's own record set (F1) — so "the restated table is independent of the other claims' records" is false for that cell too, even though the score integer is unaffected.

### F5 — INFO — no sentence claims the calibration monitor improved; the only near-miss is the verdict cell "improved (measured)"

Searched the CONTENT blobs for improvement/raise language around calibration:
```
git show 6f2168e…:SCORECARD.md   (round-46 block)  -> C1 row Verdict cell: "improved (measured)"
                                                     same row Axis cell: "calibration (lowest non-retired axis; monitor 6, unchanged)"
                                                     axis row: "| calibration | 6 | … | 46 (restated 8 → 6; no raise claimed) |"
                                                     paragraph: "Calibration monitor: 6 → 6 (…; no raise is claimed)."
git show 6f2168e…:corpus/lessons/round-46.md | grep -n "improved\|raise\|rose"   -> (no match)
git show 6f2168e…:LOG.md   (round-46 entry)  | grep -n "improved\|raise\|rose"   -> (no match)
git show 6f2168e…:PROVINCE.md (round-46 append) -> "The lane's standing self-assessment is now machine-checkable …" (no score claim)
```
The verdict cell is the claim's verdict, and the same row and the paragraph below disambiguate it; nothing states the monitor rose. A reader skimming the Verdict column can misread "improved (measured)" as an axis move — INFO only, because the disambiguation is in the same table.

### F6 — INFO — `unparsed` in the total is pre-data, and the before total understates real drift

`contract.json` is byte-identical at the freeze and at CONTENT (`git show 745a58…:…contract.json | sha256sum` = `git show 6f2168e…:…contract.json | sha256sum` = `fcda5f7dc939553acf7ba05337f97efd1bee6696d4f154e9a3d675cfb75dc206`), and both `claims.C1.statement` ("mismatches + unparsed + unobservable = 0") and `claims.C1.target` (`total=0`) include `unparsed`; the calibration directory diff freeze→CONTENT is empty; selftest T6/T7 pin absent/prose rows to failure. Counting `unparsed` is therefore declared before any data — honest.

It is also not merely cosmetic: the 19 unparsed rows hid real drift. Base `SCORECARD.md:1609` (the effective `sources-registry` row) states `→ exit 0, SOURCES_CENSUS: CLEAN (…); … → 99 rows at round 35`, while the census printed `rows=117` at base; and the base `tally-audit-v3` row pins round-35 bytes (`6188db16…`) against the actual `da8c1ef4b30c`. So 21 → 0 includes at least two genuine stale values plus the calibration `8 → 6`, not only format conformance.

### F7 — INFO — the do-nothing control holds, but only at the freeze rev

The unchanged tree at the contract's control revision reproduces `total=21` / `C1_R46_PASS=false` byte-identically (section 1). At the base rev the counter refuses cleanly instead of scoring:
```
python3 .../calibration/measure.py --lane <lane> --rev 683eedde… --base 683eedde… --work <empty>
-> exit 2, stderr "C1_R46: statements.json absent at rev", no C1_R46 line
```
So the control is reproducible at `745a58…` (which the contract names) and not at `683eedd…`; the "unchanged tree cannot reach total=0" claim is sound for the revision it names.

## Answers to the item's questions

1. **Before cell exact?** Yes — byte-identical reproduction, sha256 `fa50f36d…`; `mismatches=2` are the calibration 8-vs-6 and the regression ellipsis, `unparsed=19` as printed.
2. **After cell?** My own run at CONTENT prints `total=0` / `PASS=true`, exit 0; my independent re-derivation finds 0 value/sha/exit differences over the 22 rows (with the two script artifacts explained). The after cell reproduces; the L1's deciding receipt should print the same line.
3. **Any sentence claiming calibration improved?** No. The only near-miss is the C1 verdict cell `improved (measured)`, disambiguated in the same table and the paragraph below ("monitor 6 → 6 … no raise is claimed"); lesson, LOG and PROVINCE say nothing of the kind.
4. **Is `unparsed` honest as a mismatch?** Yes — frozen pre-data in the contract (`total` includes it) and pinned by selftest T6/T7; and it is not merely formal, since two genuinely stale values sat in the unparsed bucket at base.
5. **Is the restated table causally independent of C2/C3?** For 21 of 22 values yes (no pinned tool changed, `SHONEN.md` unchanged, freshness identical at both revs, depth unchanged). The exception is the registry row: `rows=120` counts C3's three new rows (117 at base), so C1's after cell cannot be reached without C3. A second, weaker coupling is F1: the calibration row's stated section count was invalidated by the round's own appends (all three claims' records), not by C2's hardened files.

## The strongest argument that C1 is not an improvement of calibration — and whether it holds

**The argument.** C1 measures agreement between a SCORECARD cell and a regex capture of a tool's output, and the after state is produced by pasting the counter's own `--emit` rows. It therefore cannot distinguish a corrected claim from a reformatted one; 19 of the 21 before-failures are parse nonconformance rather than false statements, the calibration monitor is unchanged (6 → 6), and at the moment `total` reaches 0 the round's calibration surface actually got *worse*: five cold-read sections lost credit (60/64 → 55/64) because of the round's own appends, and the restated row still states the pre-round `60 of 64`. So "21 → 0" is a formatting-and-predicate event, not evidence that the lane's self-assessment quality improved.

**Does it hold?** Partly, and not as a falsification of the claim as declared.
- It fails on "purely formatting": the unparsed bucket hid at least two genuine stale values (registry 99 vs 117 at base; the stale tally-audit-v3 pin) plus the calibration 8 vs 6, so the restatement did correct real drift, and every row is now machine-checked, so future drift on these 22 surfaces becomes visible.
- It holds on the axis: the calibration score is unchanged and the file says so; nothing claims a raise.
- It holds, and this is the strongest reproducible form, on the round's own calibration surface: F1 is a *new* false observation written into the deciding row (60 where the command prints 55) and F2 shows the predicate cannot certify the true value of one statement (the exact line is a MISMATCH; the truncated prefix is `total=0`). Both are fixable in the row/predicate wording, neither moves a counter field — but together they mean `total=0` is not sufficient evidence for the claim's sentence "state exactly the value … that the frozen command prints at REV", which is the sentence C1 is declared on.

So: C1's target is met (verified here); C1's statement is not fully delivered (F1, F2), and the calibration axis monitor did not move (6 → 6). The verdict cell should not be read as a calibration-score improvement.

## Not run (out of seat scope)

- The C2 (`hardening/mutate.py`) and C3 (`coverage/measure.py`) counters, `no-harm.sh`, `deciding-run.sh`, and any build/lint gate.
- No `--emit` run of the C1 counter; no second run of the 22 statements beyond the two counter runs reported here (the freeze-rev and CONTENT-rev runs), because run-to-run stability of the statements was already measured by wave 1's seven `ExecStmt` seats and by `w2/T46Reobs*`.
- Nothing in `/home/vgpnk/Projects/shokuknow` was read or written for this item.
