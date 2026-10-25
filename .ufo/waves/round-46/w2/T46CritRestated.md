seat: T46CritRestated
item: attacked the SCORECARD.md round-46 block and the standing tables it appends at C0 `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` — the calibration axis row's evidence cell, the supersession sentence, the dropped promotion-review clause, the code_view row's non-specific pointer, the FROZEN_UNCHANGED scope, and the receipt status of every after value.

Lane read-only. Scratch: `/tmp/tameshi-r46-T46CritRestated/` (SCORECARD-C0.md, LOG-C0.md, lesson-C0.md extracted from C0; counter work dirs `w1/`, `w1b/`, `w2/`, `w3/`; `coldread-c0.json`, `coldread-base.json`). No lane write except this report. No `git add/commit/stash/checkout/reset`, no `jj`, no fixture repo (none needed). Tools installed: none.

# What I attacked

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6f2168e:SCORECARD.md` from `## Round 46` (line 2166) through `### Round 46 — claims, measurement and verdicts` (line 2202) and the `Capabilities demonstrated this round` table (2220-2226), plus the three documents that must agree with it: `corpus/lessons/round-46.md`, `LOG.md` (newest entry, line 2304+), and the committed receipts under `.ufo/evidence/round-46/`.

---

## F1 — HIGH — the restated calibration row states a value its own command does not print, at the revision the row names

**Attacks:** the calibration axis row (`SCORECARD.md:2199`), whose `Measured commit` cell says `round-46 content revision`; and C1's silence about it.

`SCORECARD.md:2199`:
> `| calibration | 6 | Restraint score of the strict cold-read monitor python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV (`calibration_restraint_score`; `box3_full_page=false`, **60 of 64 sections credited**): two points per restrained, evidence-linked `[~]` SHONEN box; box 3 is not credited. ...`

Commands and output (the statement's own command, run by me against a scratch clone at `w1/clone`, C0 tree):

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/tameshi-r46-T46CritRestated/w1/clone --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
exit=0   revision 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
calibration_restraint_score 6   coldread.sections_covered 55   coldread.sections_total 64   box3_full_page False

$ python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/tameshi-r46-T46CritRestated/w1/clone --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
exit=0   revision 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
calibration_restraint_score 6   coldread.sections_covered 60   coldread.sections_total 64   box3_full_page False
```

`60 of 64` is the **base** value; at the revision the row cites the same command prints **55 of 64**. The score integer is right (`6`), so C1 passes: `measure.py:15` and `:145` compare, for an `axis` row, only "the integer in the score cell". I ran C1 at C0 and it prints `total=0` / `C1_R46_PASS=true` (see *Counter runs into scratch*), so the false section count passes the claim untouched. Nothing in the block, the lesson or the LOG says 55, and no round-46 receipt carries a section count at all (the `before/` and `after/` files print `score=6 box3_full_page=False` only); the committed `60 of 64` lines are rounds 27/28 (e.g. `.ufo/evidence/round-27/after/c1-measure-af7b70d.stdout:1`), i.e. the number was copied forward from an older revision.

**Impacted axis:** calibration. This is the exact drift class the round exists to remove — a standing row that states what the lane used to print — inside the section that claims to have removed it.

**Smallest safe correction:** change the parenthetical to `sections_covered 55 of 64 at the round-46 content revision` (or drop the section count from the cell and cite the run), and add the `sections_covered` field to the calibration statement's comparison in `statements.json`/`measure.py` so the value is checked, not just the integer.

---

## F2 — HIGH — the supersession sentence claims the counter checks more than it checks

**Attacks:** `SCORECARD.md:2172` (the standing-tables preamble).

> `This section supersedes, for every value it states, the standing rows of the capability and axis tables above ... the counter ... reads exactly these rows (last row wins) and re-runs the 22 commands ...`

What the counter actually compares, from its own docstring (`calibration/measure.py:11-16`):
- `cap` row: the evidence cell's `CMD -> PRINTED LINE`, exit N[, tool sha256 `12 hex`] "compared whole with (printed line, exit code[, sha256 prefix of the tool file at REV])";
- `axis` row: "the claim is the integer in the score cell, compared with the integer the command prints".

Not compared anywhere: the `What it can now do` cell, the `First-working round` cell (both are `"what": null, "first": null` for all 22 entries of `statements.json`; `measure.py:244-246` reads them only in `--emit`), the axis rows' `Evidence / counting rule` text, `Measured commit`, and `Last-change round`. F1 is the concrete instance: `60 of 64` sits inside the evidence cell of an axis row, so "for every value it states" is false and the number drifted unnoticed.

Second, smaller instance: "restates the line its frozen command prints" is not what the counter compares for every row. For `six-leg regression ledger` the statement's `obs` is `^(REGRESSION: \w+ \(cases=\d+ passed=\d+)`, so the compared value is a regex capture group and the restated row (`:2178`) quotes `REGRESSION: PASS (cases=9 passed=9` — an unbalanced fragment, not the line the command prints. The block is honest about the cause ("the regression row quoted a truncated line", `:2206`) but the preamble's "the line ... prints" is the counter's capture, not the line.

**Impacted axis:** calibration (the claim's own axis).

**Smallest safe correction:** replace "for every value it states" with the counter's real surface: "for the printed line, exit code and pinned tool sha256 of each capability row, and the score integer of each axis row; the What, First-working, rule, commit and round cells are carried text and are not measured."

---

## F3 — HIGH — the restated calibration rule silently drops the independent-promotion gate

**Attacks:** `SCORECARD.md:2199` against the row it supersedes, `SCORECARD.md:1537` (round-31 table).

Round-31 (`:1537`):
> `two points per restrained, evidence-linked [~] SHONEN box (SHONEN.md:5-12), box 3 only when the monitor credits the full page; the last 2 points need independent promotion review`

Round-46 (`:2199`):
> `two points per restrained, evidence-linked [~] SHONEN box; box 3 is not credited.`

Two rule changes are made in rule position with no note:
1. "box 3 only when the monitor credits the full page" becomes "box 3 is not credited" — read as a rule, the axis caps at 3×2 = 6 forever; read as a state, it is a measurement written where a rule belongs.
2. "the last 2 points need independent promotion review" is dropped. Under the round-31 rule, 8 = 6 monitor points + 2 granted by an independent review; under the round-46 text, 8 would follow from four credited boxes with no review gate at all.

This is the axis the round claims, and C1 cannot see it (F2). It is the inverse of a raise: the block lowers the standing value 8 → 6 and simultaneously removes the gate that made 8 legitimate, so a later box-3 credit could restate 8 without the review the lane's own history required (round-16/17 `calibration 6 → 8 (pending non-author)`, `SCORECARD.md:588,625`; `:374` "These scalar/mark counts are not a fresh outside promotion review").

**Impacted axis:** calibration.

**Smallest safe correction:** restate the round-31 rule verbatim in the row, then state the value and the reason for the correction separately: "the monitor prints 6; the 2 promotion-review points recorded at rounds 16/17/31 were never granted by an independent review, so the standing value is 6."

---

## F4 — LOW — three different revisions are named for the same values, and one of them cannot produce them

**Attacks:** `SCORECARD.md:2172` vs `:2206` vs `:2198-2200`.

- `:2172`: "Values are what each command printed at records revision `a6892b196f923efbed242ce9ea599a3f745b2138`".
- `:2206` (C1 after cell): "`total=0` `C1_R46_PASS=true` at records revision `e630ae791a831828f51b8f192996a907ff8ed78d`".
- `:2198-2200` (all three axis rows): `Measured commit | round-46 content revision` (= C0 `6f2168e`).

The restated tables do not exist at `a6892b1`:

```
$ git show a6892b1:SCORECARD.md | grep -c "Standing self-assessment — re-stated at round 46"
0
$ git show e630ae7:SCORECARD.md | grep -c "Standing self-assessment — re-stated at round 46"
1
$ git show 745a583:SCORECARD.md | sha256sum ; git show a6892b1:SCORECARD.md | sha256sum
4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1  -   (freeze)
4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1  -   (a6892b1)
```

`SCORECARD.md` is byte-identical at the freeze and at `a6892b1`, so a C1 run there reads the same 22 rows as `before/c1-at-freeze.stdout` and prints `total=21` (`unparsed=19`, `mismatches=2`), not `total=0`. The per-command printed lines are plausible at `a6892b1` (they are what `--emit` recorded there), but the block's own C1 after value was not printed there, and the deciding revision is a third one. A reader cannot tell which revision any given cell was measured at, and the "records revision" label is applied to two different commits.

**Impacted axis:** calibration (provenance of the claim).

**Smallest safe correction:** one sentence naming all three explicitly: "the printed lines were observed at `a6892b1` (wave-1 evidence); the rows were appended at `e630ae7`; the deciding values are taken at C0 `6f2168e`."

---

## F5 — HIGH — `FROZEN_UNCHANGED=1` does not cover the two counters C2 measures

**Attacks:** `SCORECARD.md:2210` and the mitigation it names for the disclosed cheat Z (`:2218`).

> `:2210` ... `which also prints FROZEN_UNCHANGED=1` (**no counter**, statements list, manifest, snapshot, package copy or contract changed since the freeze) ...

`.ufo/evidence/round-46/deciding-run.sh` step 0 diffs this set between `745a583` and `REV`:

```
FROZEN="$E/contract.json $E/calibration/measure.py $E/calibration/statements.json $E/coverage/measure.py $E/coverage/sources $E/assimilation/package $E/assimilation/adoption-map.json $E/hardening/mutate.py $E/hardening/mutants.json $E/control/run-controls.py $E/no-harm.sh"
```

`hardening/freshness-counter.py` and `hardening/coverage-counter.py` are not in it, and they are the bytes `mutate.py --targets hardened` mutates. They did not exist at the freeze:

```
$ git ls-tree -r --name-only 745a583 .ufo/evidence/round-46/hardening/
build-manifest.py  mutants.json  mutate.py
$ git diff --stat 745a583 6f2168e -- .ufo/evidence/round-46/hardening/
 assemble.py | 71 ++ ... coverage-counter.py | 411 ++++++ ... freshness-counter.py | 815 ++++++++ ... try-mutants.py | 41 ++
```

So `FROZEN_UNCHANGED=1` is compatible with an arbitrary post-freeze edit of the two counters under test, and the parenthetical's "no counter ... changed since the freeze" is false as written. The guard's real content is "the frozen inputs are unchanged"; the C2 subjects are new artifacts. Reproduced at C0 with the script's own set:

```
$ git diff --quiet 745a583 6f2168e -- $FROZEN        → exit 0   (FROZEN_UNCHANGED would be 1)
$ git diff --stat 745a583 6f2168e -- .ufo/evidence/round-46/hardening/{freshness,coverage}-counter.py
 coverage-counter.py | 411 +++++  freshness-counter.py | 815 +++++   2 files changed, 1226 insertions(+)
```

**Impacted axes:** operability (the C2 surface) and calibration (a false provenance sentence in the block).

**Smallest safe correction:** add both counters to the printed `COUNTER_SHA256` block (they are already printed for three other files) and rewrite the parenthetical to "the frozen inputs are unchanged; the two hardened counters under test are new since the freeze and their sha256 is printed above."

---

## F6 — HIGH — the `bounded ANSI-C code_view` row's evidence pointer proves nothing about code_view

**Attacks:** `SCORECARD.md:2191` vs `:2190`.

Both rows carry the identical command, identical printed line and identical tool prefix:

```
:2190 | tally-audit-v3 runner audit | ... | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c` | round 35 |
:2191 | bounded ANSI-C code_view  | ... | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c` | round 37 |
```

A whole-tool tally of 35/35 pass is a selftest result, not a measurement of "keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, preserve a literal `#`". This is also an identity collapse: the contract counts "22 frozen statements (19 capability rows ...)", but two of the 19 rows are byte-identical measurements of the same command, so the statement count overstates the number of distinct things measured by one. The specific demonstration exists and is committed:

```
$ git show 6f2168e:.ufo/evidence/round-37/code-view/after.stdout
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=1/1 tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede rev=ae9b771ab795fb5b4a6302165d8abdc0a2c6b229 C2_R37_PASS=true
```

with the before receipt showing the honest red (`before.stdout`: `ansi_trailing_comment=0/1 ... C2_R37_PASS=false`). C1 accepts the row because the row's printed line matches; the row is therefore indistinguishable from the row above it.

**Impacted axis:** calibration (a standing row whose evidence does not support its claim).

**Smallest safe correction:** point the row at `.ufo/evidence/round-37/code-view/after.stdout` (value `ansi_trailing_comment=1/1 ansi_literal_hash=1/1`) and keep the tool sha as the pin, or drop the row as a separate statement and let the tally-audit-v3 row carry the sha.

---

## F7 — LOW — 17 of 19 capability rows' pointers are selftest tallies; four assert counts their printed line does not contain

**Attacks:** the restated capability rows `SCORECARD.md:2176-2194` (item (a) of the assignment).

Of the 19 rows, 17 point at a `--selftest` tally; the two exceptions are `sources-registry` (`rows=120 SOURCES_CENSUS: CLEAN`, a real census) and `six-leg regression ledger` (`REGRESSION: PASS (cases=9 passed=9`, a real 9-leg replay). Where the `What` cell asserts numbers, the printed line does not carry them:

| row | line | `What` asserts | printed line |
|---|---|---|---|
| tally-audit-v2 runner audit | `:2189` | "kill all 18 public + 8 sealed must-kill ... accept all 8 public + 6 sealed must-accept" | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` |
| tally-audit-v3 runner audit | `:2190` | "kills 6/6 public + 4/4 sealed ... accepts 3/3 public + 3/3 sealed" | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` |
| hermetic env-differential probe | `:2184` | "nine pinned selftests under seven explicit profiles" | `ENVDIFF_SELFTEST: 9/9 pass` |
| staged-id adoption guard | `:2194` | "0-3-space census pattern ... refuse its own naive arithmetic map ... by-document map" | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` |

The counts are true and backed elsewhere — `.ufo/evidence/round-34/measure/c1-deciding-run.stdout:1` (`v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0`), `.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout:17` (`pub_kill=6/6 pub_accept=3/3 ho_kill=4/4 ho_accept=3/3`), `tools/env-diff.py:29` (`PROFILES = ("host","clean","clean_repeat","tz","locale","home","columns")`) — but not by the row's own pointer. `:2172` does disclose that `What`/`First-working` are "carried unchanged", which is why this is LOW and not a claim defect; F6 is the same class with no backing pointer at all, which is why it is HIGH.

**Impacted axis:** calibration.

**Smallest safe correction:** add the count-bearing receipt path to each `What` cell (as `:2184` already does for the env-diff receipt), or narrow the `What` cell to what the tally shows.

---

## F8 — LOW — receipt status of the block's values (item (d))

**No committed receipt at C0** (`git ls-tree -r --name-only 6f2168e .ufo/evidence/round-46` has no `after/`):

| value | cell | receipt |
|---|---|---|
| `total=0` `C1_R46_PASS=true` at `e630ae7` | `:2206` | none. The C1 selftest receipts are 3-statement toy runs (`selftest/c1-selftest.stdout:1,18`: `statements=3`); the only 22-statement `total=0` lines in the tree are wave-1 **cheat** runs (`w1/CritC1Control.md:57` counter edited, `:37` statements list edited). |
| `rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260` | `:2208` | none. `selftest/c3-selftest.stdout` prints `rev=m` on toy fixtures; no lane-revision line exists. |
| `rows=120` | `:2176` | none. The lesson names one — `corpus/lessons/round-46.md:125` "End: `.ufo/evidence/round-46/census-end.stdout` (recorded at the content revision)" — and that file does not exist in the C0 tree (`ls-tree` lists only `census-start.{exit,stdout,stderr}`). |
| `20/20 passed` (no-harm-gate selftest) | `:2226` | none. Only `w1/ExecFalsifier.md:87`. |
| `SEAT_NAME_SELFTEST: cases=4 failed=0` | `:2226` | none anywhere in the tree (grep hits only the tool source `quality/seat-name-check.py:66` and the SCORECARD row itself). |
| `60 of 64 sections credited` | `:2199` | none, and false at C0 — F1. |

I reproduced the last two now, from the C0 tree:

```
$ python3 .ufo/evidence/round-46/quality/no-harm-gate.py --selftest     → SELFTEST: 20/20 passed / VERDICT: PASS, exit 0
$ python3 .ufo/evidence/round-46/quality/seat-name-check.py --selftest  → SEAT_NAME_SELFTEST: cases=4 failed=0, exit 0
```

so the values are true; what is missing is the receipt the row implies.

**Receipted values (spot-checked, all match):** `killed=25 survived=0 neutral_killed=0 pristine=1 equivalence=1` at `a6892b1` — `quality/c88-90-falsifiers.stdout:9`; all 17 stated `tool sha256` prefixes — independently recomputed as `git show 6f2168e:<sha_file> | sha256sum | cut -c1-12` for every `sha_file` in `statements.json`, 17/17 match (the code_view and tally-audit-v3 rows both resolve to `da8c1ef4b30c`, which is F6); `total=21` / `mismatches 2` / `unparsed 19` — `before/c1-at-freeze.stdout:23` with 19 `UNPARSED` lines and the two `MISMATCH` lines at `:3` (regression, truncated quote) and `:21` (calibration 8 vs 6); controls — `control/controls-at-freeze.stdout:1-7` (CTL_A..G, including `killed=21 neutral_killed=6` and `pristine=0`); no-harm six monitors — `before/no-harm-at-base.stdout:1-6`; `fresh=71 score=9` and `disputed S048, S093` — `.ufo/evidence/round-45/after/c1-at-content.stdout:1-3` (and re-observed by me at C0, see F9 scratch); `recorded_cases=9 depth_score=9` — `before/no-harm-at-base.stdout:1` (re-observed at C0); `C1_R46_SELFTEST: cases=18 failed=0` / `C2_R46_SELFTEST: cases=8 failed=0` / `C3_R46_SELFTEST: cases=24 failed=0` — `selftest/{c1,c2,c3}-selftest.stdout`; statements pin `a15a8b45…f246e9` — `sha256sum` of `calibration/statements.json` at C0 matches the block; `4 and 8 mutants alive` — `w1/MutC3Counter.md:8` ("18 killed, 4 survived") and `w1/MutDriver.md:43` ("all 8 probes ... survived"); `19 capability rows` / 22 statements — counted from `statements.json` (19 `cap` + 3 `axis`); `five of the 22 statements pin no tool file` — 5 null `sha_file` entries.

---

## F9 — LOW — numbers that disagree between the block, the lesson and the LOG (item (e))

1. **LOG.md:2308** — "The round-45 spot-check routed the counters' selftest survivors (**12 + 8 + 8** in the round-45 mutation audits)". The audits report 12 (`w1/MutC1Counter.md`, 12 `SURVIVED` rows), 8 (`w1/MutC2Counter.md`, 8 `SURVIVED` rows) and **9** (`w2/MutC1Reviews.md`, 9 `SURVIVED` rows) = 29. The manifest declares 25: freshness 15 (12 + 4 unique reviews survivors) and coverage 10 (8 survivor rows, M13 splitting into C07/C08/C09) after dedupe of F06/F08/F09/F10 and reviews 11/13. So the LOG's `8` is wrong for the reviews audit and its total (28) matches neither the 29 found nor the 25 declared; no document reconciles 29 → 25. The block's "25 declared survivors" (`:2207`) is correct.
2. **`60 of 64`** in the block (`:2199`) vs the command's 55/64 at C0 (F1). The lesson and LOG state no section count, so nothing cross-checks it.
3. **Lesson `corpus/lessons/round-46.md:125`** names `census-end.stdout` "recorded at the content revision"; the file is absent at C0 (F8). The LOG's census claim is only "census exit 0 at start" (`LOG.md`), which is receipted.
4. Everything else I compared agrees: before `total=21`/19 unparsed (block `:2206` = LOG "19 of 22 standing statements carried no machine-checkable value"), selftests 18/8/24 (LOG "C1 18/18, C2 8/8, C3 24/24" = receipts), rows 117 → 120 (block `:2176`, LOG), 37 wave-1 seats with `MutC1Counter`/`ScribeQuality` dead (LOG) and 7 `ExecStmt*` reports (LOG "Seven executor seats"), 25 + 6 mutants (contract, manifest, block `:2207`), depth 9 / freshness 9 / calibration 6 (block `:2198-2200` = receipts), `4 and 8 mutants alive` (block `:2218` = `w1/MutC3Counter.md:8`, `w1/MutDriver.md:43`).

---

## (c) calibration axis — does the block read as a raise?

**No raise sentence found.** The value is pinned at 6 in four places: `:2168` "monitor 6"; `:2199` score cell `6` and `Last-change round | 46 (restated 8 → 6; no raise claimed)`; `:2206` axis cell "monitor 6, unchanged"; `:2212` "Calibration monitor: 6 → 6 ... no raise is claimed".

Two raise-adjacent strings, both disclaimed in the same block, so neither is a defect on its own:
- `:2206` verdict cell `improved (measured)` on a calibration-axis claim. The same words are the verdict of round-45's freshness claim (`:2154`), which *did* move 1 → 9, so a skim of verdict cells reads as axis movement. `:2212` disclaims it two lines later.
- `:2199` `Last-change round 46` on the calibration row, i.e. the axis is recorded as changed this round; the parenthetical says the change is a downward correction.

The real calibration finding is the inverse of a raise: F3, the promotion gate dropped while the value is lowered 8 → 6.

---

## Counter runs into scratch (observed, not a verdict)

Every run here uses `--lane` = the lane, `--rev` = the named revision, and a fresh empty work dir; the deciding run remains the L1's.

- `coldread/measure.py` at `6f2168e` (C0) and at `683eedd` (base): results in F1 — `restraint 6`, `covered 55/64` at C0, `60/64` at base, `box3_full_page False` both. Exit 0 both.
- C1 `calibration/measure.py` at C0 `6f2168e` (fresh empty work dir `w3`, wall 10m36s — the sweep includes `bash tools/mutate-and-run.sh --regression`, statement timeout 1800 s):

```
STATEMENT axis/depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT axis/calibration: claimed=6 observed=6 (exit=0) MATCH
STATEMENT axis/freshness: claimed=9 observed=9 (exit=0) MATCH
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 append_only=1 total=0 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C1_R46_PASS=true
real 10m36.327s   PIPE_EXIT=0
```

  Observed, not a verdict — the deciding run is the L1's. It matters for F1/F2: at the very revision the block's rows are written for, the counter prints `total=0` and `PASS` while the calibration row's evidence cell states a section count (`60 of 64`) that the same command does not print (`55 of 64`). The counter cannot see it, exactly as its docstring says.

- C1 at `a6892b1`: **not completed by me** — the first C0 attempt hit the 600 s tool deadline (`[Command timed out after 600 seconds]`), and a detached `a6892b1` run produced no output before I closed the item (its scratch `w2/` holds only `fleet/`). It is not needed: `SCORECARD.md` is byte-identical at the freeze and at `a6892b1` (`sha256 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1` both), so a run there reads the same 22 rows as `before/c1-at-freeze.stdout`, which prints `total=21` (`unparsed=19`). The `total=0` cell cannot have been printed at `a6892b1` (F4).

---

## Severity summary

| id | severity | subject | axis |
|---|---|---|---|
| F1 | HIGH | `:2199` states 60/64; the command prints 55/64 at the cited revision | calibration |
| F2 | HIGH | `:2172` "supersedes, for every value it states" overstates the counter's surface | calibration |
| F3 | HIGH | `:2199` drops the independent-promotion gate from the calibration rule | calibration |
| F5 | HIGH | `:2210` `FROZEN_UNCHANGED=1` does not cover the two hardened counters | operability / calibration |
| F6 | HIGH | `:2191` code_view row's pointer is the tally-audit-v3 tally; the real receipt exists | calibration |
| F4 | LOW | three revisions named for one set of values; `a6892b1` cannot print them | calibration |
| F7 | LOW | 17/19 rows point at selftest tallies; four assert counts absent from the line | calibration |
| F8 | LOW | five after values have no committed receipt (two reproduced by me now) | calibration / coverage |
| F9 | LOW | LOG `12 + 8 + 8` vs audits 12 + 8 + 9 and manifest 25; lesson's `census-end.stdout` absent | calibration / operability |

Nothing above is a defect of the C1 counter's arithmetic or of its selftest: the selftest receipts (`selftest/c1-selftest.stdout`, 18/18) and the 22-statement shape reproduce, and the counter does exactly what its docstring says. Every finding is about what the block says around the counter.
