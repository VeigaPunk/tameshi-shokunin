# W2SimplifierLessonGate — round-36 lesson gate audit

Seat: W2SimplifierLessonGate (round-36 w2 falsify wave; leaf, read-only; judged on **calibration**).
Attacked: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-36.md` end to end (committed `e423c41`), per assignment: (1) `## Mistakes` rows carry class/evidence/captured-by/fix; (2) the Gate records the S103 URL+date+quote; (3) every claim in the lesson is backed by a committed pointer. Per-section verdicts below.

Bounds compliance: all paths absolute; only non-mutating git (`log`, `ls-files`, `show`, `diff`, `cat-file`) run; the only byte I wrote in the shared tree is this report. Frozen artifacts (`tools/tally-audit-v3.py` `6188db16…`, `tools/mutate-and-run.sh` `a7d3f2dd…`, r35/r36 counters, r21 ledger) re-hashed read-only, never edited. No tool installs (none needed; no `pacman`). No scratch files needed, none created. No deletion candidates → no `lsp` reference check applicable (target is prose; nothing deleted; grep not offered as semantic proof anywhere).

## Commands and revisions (all under /home/vgpnk/Projects/shokunin/tameshi-shokunin)

- `sha256sum tools/tally-audit-v3.py tools/mutate-and-run.sh .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-36/c1/c1-measure-v2.py .ufo/evidence/round-36/src/s103-git-hash-object.html` → `6188db16…d354` ✓, `a7d3f2dd…2eb9` ✓, `d360a159…bbe3`, `9eb8944c…fa53` ✓ (matches contract), `dd826dae…6100` ✓ (matches lesson+row); `wc -c` snapshot → `29933` ✓.
- `git log --all --oneline -- '*ResidualSentinelClosure*'` → empty ✓; `git ls-files '.ufo/waves/round-35/residual/'` → exactly the five reports ✓.
- `git show 796e08b:corpus/SOURCES.md | grep -c '^| S[0-9]'` → **99**; `git show b455001e:…` → **100**; `git diff 796e08b b455001e -- corpus/SOURCES.md` → single added row `+| S103 |…` ✓ (no other row lines → no status/recheck/used-by flips ✓).
- `sed -n '1607,1608p' .ufo/evidence/round-36/src/s103-git-hash-object.html` (§DESCRIPTION heading at `:1604`) + `wc -w` on the quoted span → **18**.
- `jq` on `.ufo/evidence/round-36/after/monitor-at-{796e08b,b455001e}.stdout`, `control/monitor-at-e423c41b.stdout` → `calibration_restraint_score` **6** (60 sections) / **8** (64) / **6** (60); exits: census 0, monitors 0, `v1-at-emptypanel` 0 (vacuous PASS), `v2-at-emptypanel` 1, `c1v2-at-b455001e` 0.
- `jq '.entries | length' .ufo/evidence/round-21/coldread/ledger.json` → **497** = 493 retained + 4 added (matches `refresh-receipts.json`); last 4 entries: the four sections at 131/375/1380/1436, `read_rev` = `e423c41b…` ✓.
- `jq '(.items|length)' .ufo/waves/round-36/spec-w{1,2}.json` → **39 / 39** (band 32–64 ✓).
- Per-input r35-span edit census: `git log --oneline 51d3f08…..796e08b -- <file>` → LOG.md 1, SCORECARD.md 2, corpus/README.md 1, corpus/SOURCES.md 1, closeout-r11.md 1, survivor-fixture-minimization.md 1, **corpus/QUALITY.md 0**, **tools/mutate-and-run.sh 0**.
- `git ls-files | grep -i census` → no round-36 start receipt (see F1); `git ls-files --error-unmatch` over all 18 lane artifacts the lesson names → **18/18 committed**.
- Reads: lesson, round-35 lesson, `LOG.md:1888-1990`, `contract.json`, `QUALITY.md:845-852` (criterion 72), `SOURCES.md:112` (S103 row), `refresh-receipts.json`, `affected-sections.json`, `c1-measure.py:495-545`, `c1-measure-v2.py:495-560`, receipt/stdout/exit files, wave spec/validate files, `corpus/lessons/round-36-verifier-spotcheck.md:92`.

## Per-section verdicts

### Header / intro — PASS
"TameshiR36, attempt 1, 2026-10-24" matches `contract.json` (`l1`/`attempt`/`frozen_at`). Both claims routed from the r35 closure ✓ (r35 lesson: cold-read lapse routed to r36; residual seat ResidualCriticPredicate §1 routed the cardinality successor; contract claims C1/C2). Dead-pointer repair in LOG ✓ (`LOG.md:1900-1906`); ANSI-C deferral to round 37 with reason ✓ (`contract.json` routed_repairs, `LOG.md` r36 entry).

### "What this round attacked, and why" — PASS with one precision defect (F2)
Calibration 6 (was 8) ✓ (r35 lesson "Cold-read credit lapse": 8@`51d3f08`, 6@`34fa5b0`; monitor receipts). Four drifted headings ✓ (`affected-sections.json`: exactly 4 sections @ 131/375/1380/1436; 4 ledger entries; 4 trace receipts `traces/L1/source-1..4.json`). The eight-file union ✓ exact set-equality with `affected-sections.json` paths. **F2**: the mechanism sentence "the r35 record repairs rewrote their cited inputs" is over-broad — in the true r35 span `51d3f08..796e08b`, **6 of 8** union members were rewritten by r35, but `corpus/QUALITY.md` (last touch `2da841b`, round-31) and `tools/mutate-and-run.sh` (last touch `bb68156`, round-30; byte-identical `a7d3f2dd…` across all r35 measurements) were not. Both are genuinely drifted inputs under the monitor's rule (hence in the union), just not via r35 repairs.

### Gate — PASS with two precision defects (F3) and one material claim (F1)
- **S103 URL ✓** (`SOURCES.md:112` COL3, snapshot header, contract). **Date ✓** "2026-10-24 UTC" (row COL7/COL10, contract). **Snapshot ✓** committed, sha256 and 29,933 bytes exact. **Quote ✓ verbatim** (snapshot `:1607-1608`, §DESCRIPTION `:1604`).
- **F3a**: "(19 words)" is wrong — the quoted span is **18 words** (`wc -w` = 18). **F3b**: "§DESCRIPTION first sentence" is a truncation — the sentence continues "(which can be outside of the work tree), and optionally writes the resulting object into the object database." The same truncated labeling is carried into `SOURCES.md` COL7 and `LOG.md`. (r35 set the precedent for catching exactly this class on S102.)
- "Mined into refresh-receipts.json and this lesson" ✓ (receipts cite S103 as `cited_source` ×4; row Tier A ✓, status `mined` ✓ COL5/COL9).
- "Rejected this round: none" ✓ consistent (registry delta `796e08b→b455001e` is exactly +S103; no other round-36 fetch rows).
- "Rows: 99 → 100 (S103 only). No flips" ✓ (counts + single-row diff above).
- **F1 (material)**: "both receipts kept under `.ufo/evidence/round-36/`" is **false** for the start receipt. Only `after/census-at-b455001e.{exit,stdout}` exists (exit 0, "ok", 100 rows ✓). `git ls-files | grep -i census` shows **no round-36 census-start receipt at any commit**, while the lane convention (r25–r35) keeps `census-start.*` + `after/census-end.*` pairs every round. The 99-row start *number* is independently true (`git show 796e08b:corpus/SOURCES.md` → 99), so the fix is to land the missing receipt or append-only reword per QUALITY 72 — not a silent repair.

### Mistakes — PASS
Exactly one row; carries **class** (reference-drift), **evidence**, **captured-by**, **fix**, plus shown-able-to-fail. Evidence ✓ (LOG `:1888-1893` names `ResidualSentinelClosure.md`; `git log --all` empty; residual dir holds exactly the five named reports). Captured-by ✓ (QUALITY 72 records "no in-lane criterion caught it at r35 write time — the r35 closure's step-1 pointer sweep", pointer `corpus/lessons/round-35-verifier-spotcheck.md` resolves and is committed). Fix ✓ (append-only LOG correction `:1900-1906`; QUALITY criterion 72 at `QUALITY.md:845-852` whose falsifier IS the r35 dead pointer).

### Holds — PASS
`code_view` ANSI-C hold stays open with the stated reason verified: `tally-audit-v3.py` = `6188db16…` (recomputed), pinned by the SCORECARD capability row (`:1686`, `:1698`), the frozen v1 counter (`TOOL_SHA256`) and the v2 successor (`TOOL_SHA256`) — an edit voids all three; round-37 plan matches `contract.json`. Refresh-scope honesty ✓: "L1-author input-keyed source reads only; not independent/blind cold-read" appears verbatim in `refresh-receipts.json` (top scope, per-receipt scope ×4, `round36_provenance`), with instrument/stdout sha256s, exit 0, `read_rev` = content commit.

### Wave note — PASS with one forward reference (F4)
"w1 build 39 / w2 falsify 39 prepared as validator-checked specs" ✓: `spec-w{1,2}.json` items = 39/39 = 78 (in band 32–64), specs + `validate-w{1,2}.{stdout,stderr}` committed; independently confirmed by `corpus/lessons/round-36-verifier-spotcheck.md:92` ("39 tasks each, stderr empty … 0 seats ran"). **F4**: "the round report itemizes the 78 prepared-but-undispatched seats" points at an artifact that does not exist at `e423c41`, `b455001` or `d9c496b` (repo-wide `git ls-files`; `.ufo/reports/` holds only round-1). Forward reference, expected to resolve at round closure — sibling seats filed the same finding independently.

## Findings summary

| # | Severity | Section | Finding |
|---|---|---|---|
| F1 | material | Gate | Round-start census receipt (99 rows @ `796e08b`) was **not kept**; "both receipts kept under `.ufo/evidence/round-36/`" false. Number itself verified true. Fix: land receipt or append-only reword (QUALITY 72). |
| F2 | precision | What this round attacked | "r35 record repairs rewrote their cited inputs" holds for 6/8 union members only; `corpus/QUALITY.md` (round-31 `2da841b`) and `tools/mutate-and-run.sh` (round-30 `bb68156`) drifted from earlier rounds. Union list itself exact. |
| F3 | precision | Gate | Quote annotation "(19 words)" is **18**; "§DESCRIPTION first sentence" is a truncated first sentence (continues past the quote). Quote text itself verbatim; same truncation carried into SOURCES row and LOG. |
| F4 | forward-ref | Wave note | Round-36 report absent at every round-36 commit; the 78-seat itemization is currently backed only by the specs (39+39) and the committed spotcheck note. |

Adjacent (not lesson defects, LOG/wave-prep only): w2 context text (`spec-w2.json:284` / `dispatch-w2.json:568` / `validate-w2.stdout:568`) says "**80** prepared-but-undispatched seats" — ground truth is 78, which the lesson states correctly. `LOG.md:1940` names `validate-w1.json`/`validate-w2.json` where the committed receipts are `validate-w{1,2}.stdout/.stderr`; `LOG.md` r36 entry names `control/monitor-at-content-commit.*` where the committed file is `control/monitor-at-e423c41b.*`.

## Verdict

**VERDICT: PASS WITH FINDINGS — lesson structurally sound (Mistakes row complete; Gate carries S103 URL+date+verbatim quote; 18/18 named lane artifacts committed), with 1 false receipt-keeping claim (F1), 2 precision defects (F2: mechanism over-broad for 2/8 inputs; F3: 18 words, truncated first sentence), 1 forward reference (F4, round report not yet landed). Calibration notes: all quoted numbers re-derived exactly (6→8 monitor, 99→100 rows, 493+4 ledger, 6/3/9 v2 targets, 39+39=78, 18 words); no edits made to the shared tree beyond this report; no deletion candidates found — the next deletion candidate here would be the lesson's own over-broad causal clause, and removing it harms nothing.**
