# ResidualReceipts — every citation in the round-41 report, checked at the tip

Scope: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md`, every backticked path and every
`.ufo/evidence/round-41/...` citation, checked against the lane tip
`812ee0d11d267e131be3dc8db0b71253cbae9234`.

Method: all lane reads are `git show <tip>:<path>` / `git cat-file -e <tip>:<path>` — tip-pinned, never
the worktree (see R2). Replays are the two counters the assignment permits (plus `--control`), commands C
and D as defined in `SCORECARD.md:73-75`, and the round-21 coldread monitor; all read-only. No file
outside this report was written; no tool installed.

Verdict: **6 DEFECT (1 high, 1 medium, 4 low), 56 PASS.** No defect moves a number the round measured at
its two receipted commits; the high one is record integrity, not measurement.

## DEFECTS

**D1 — high — `LOG.md` at the tip carries the round-41 tail bullets inside the round-39 and round-40
sections; two closed rounds now cite this round's evidence.**

```
git show 812ee0d:LOG.md | awk 'NR>=2060 && NR<=2185 && (/^- /||/^## /){print NR": "substr($0,1,60)}'
→ 2061: ## 2026-10-24 — round 39 …
  2069: - Command D at the measured commit: `recorded_cases=9 depth_
  2073: - Receipts after the deciding runs: `.ufo/evidence/round-41/
  2080: ## 2026-10-24 — round 40 …
  2088: - Command D at the measured commit: `recorded_cases=9 depth_
  2092: - Receipts after the deciding runs: `.ufo/evidence/round-41/
  2111: ## 2026-10-25 — round 41 …
  2168: - Command D at the measured commit: `recorded_cases=9 depth_
  2172: - Receipts after the deciding runs: `.ufo/evidence/round-41/
```
The spans are byte-identical, not merely similar:

```
python3 (compare LOG.md spans)
→ 39 copy == 40 copy: True
  39 copy == 41 first 10: True      # lines 2069-2078 == 2088-2097 == 2168-2177
  last line of stray copy: '  named.'
  line 2079: ''
```
Ten lines per copy: the whole `Command D at the measured commit …` bullet and the whole `Receipts after
the deciding runs …` bullet, including `The C1 run at b37ce974 is retained as history`, sit inside
`## 2026-10-24 — round 39` (2069-2078) and `## 2026-10-24 — round 40` (2088-2097) as well as in their
own section (2168-2177).

Origin is pinned by commit, not by inference:

```
for R in b37ce974 baa18b7b 2ae00eb7 0c8e1be 812ee0d; do printf '%s: ' $R;
  git show $R:LOG.md | grep -c 'retained as history'; done
→ b37ce974: 0
  baa18b7b: 3
  2ae00eb7: 3
  0c8e1be: 3
  812ee0d: 3
```
So the `baa18b7b` LOG edit ("wave-1 evidence … record corrections, A2/A5 rule declarations", the commit
the report's landed-changes table names) wrote the round-41 tail bullets three times: at the two
already-superseded anchors and at the correct one. Three commits later the tree still holds all three.

Why it is not caught by the round's own instruments: C1's m8 class resolves *cited paths*, and these paths
do resolve at the tip; a citation that belongs to a different round's section is outside every declared
class. The round-41 section itself is intact, so the sentence the report cites — "`LOG.md` `## 2026-10-25 —
round 41`" — is individually supported; the defect is that the same text is also attributed to rounds 39
and 40, which is a false statement about those rounds' evidence. A reader auditing round 40 now finds
round-41 receipts and a round-41 deciding-run history under its heading.

**D2 — medium — `~/.omp/logs/omp.2026-10-25.*.log`: the stated reason for the UNSETTLED verdict is
contradicted by the cited artifact.**
Report: "the seat sessions in `~/.omp/logs/omp.2026-10-25.*.log` are UUID-keyed, so a name →
terminal-unix map is not reconstructible from the log".

```
grep -h 'Session exit recorded' /home/vgpnk/.omp/logs/omp.2026-10-25.*.log | grep -c 'L1Tameshi41'
→ 38
```
each line carrying the seat name in `sessionFile` and the exit timestamp on the same record, e.g.
`{"timestamp":"2026-10-25T03:45:43.859-03:00",…,"message":"Session exit recorded",
"sessionFile":"/home/vgpnk/.omp/agent/sessions/…/L1Tameshi41/L1Tameshi41.ExecC2Base.jsonl",
"reason":"dispose","kind":"normal"}`.

```
python3 - (registry names ∩ names with an exit line)
→ registry 40 with exit line 38   missing ['ReviewScorecardNumbers', 'ScribeScorecard']
```
The UUID is the *value* of `sessionId`; the seat name is in `sessionFile` on the same record, so 38 of 40
wave-1 seats do have a name → `terminal_unix` mapping in the cited log.

The verdict still holds, on the other leg — the parent has no exit line:

```
grep -h 'Session exit recorded' … | grep -c '"sessionId":"L1Tameshi41"'   → 0
python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-41/settlement-receipt.json
→ WAVE_PARENT: verdict=UNSETTLED detail=no seats   (exit 1)
```
and `tools/wave-parent-settle.py:19-23` returns `'no seats'` only because the receipt's `seats` list is
empty (`'parent_exit_unix missing'` is the next check). The honest statement is "the receipt carries
`seats: []` and the parent has no exit line", not "not reconstructible". The same false reason is embedded
in `.ufo/waves/round-41/settlement-receipt.json` (`evidence`, `tool_verdict`), so the correction must
travel with the record.

**D3 — low — `.ufo/evidence/round-41/census/command-d.stdout` is attributed to the measured commit; its
own header names `b37ce974`.**

```
git show 812ee0d:.ufo/evidence/round-41/census/command-d.stdout
→ # command D at b37ce974b6efb8c465626d7346149549a3300a4b
  recorded_cases=9 depth_score=9
  boxes=4 checked=0 asserted=4 untouched=0
  coldread score at a3d6c690 = 6
  coldread score at b37ce974 = 6
git log --oneline -- .ufo/evidence/round-41/census/command-d.stdout
→ baa18b7 round-41: wave-1 evidence … (unchanged at the tip and at 2ae00eb7)
```
The numbers are right (replay at 2ae00eb7 and 812ee0d under PASS-48/49), but the file does not support
"at the measured commit". Provenance-label defect, no numeric harm.

**D4 — low — `.ufo/evidence/round-41/census/{start,end}.stdout` do not contain the row counts cited for
them.**
Report: "Round start: exit 0, 107 rows, 9 × W04 + 1 × W01, zero E codes
(`.ufo/evidence/round-41/census/start.stdout`)"; "Round end: exit 0, 109 rows …".

```
git show 812ee0d:.ufo/evidence/round-41/census/start.stdout | wc -l  → 11
git show 812ee0d:.ufo/evidence/round-41/census/end.stdout   | wc -l  → 11
```
11 lines = ten warnings + `tameshi	ok	…/corpus/SOURCES.md`; no `.stderr` exists for either. `validate`
mode emits no `rows` line — only `census` mode does (`scripts/sources-census.sh:21-23`) — so the counts
come from elsewhere, where they are present and true:

```
git show 812ee0d:.ufo/evidence/round-41/before/c1-at-base.stdout      | tail -1  → … sources_rows=107 rev=a3d6c690… (exit 1)
git show 812ee0d:.ufo/evidence/round-41/after/c1-at-2ae00eb7.stdout  | tail -1  → … sources_rows=109 rev=2ae00eb7… (exit 0)
bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi | grep rows
→ tameshi	rows	109   (exit 0)
```
The claimed warning set (9 × W04 + 1 × W01) and "zero E codes" are exactly what `start.stdout` shows.

**D5 — low — `scripts/hyaku/ufo-wave-policy.json` does not resolve in the lane.**
```
git cat-file -e 812ee0d:scripts/hyaku/ufo-wave-policy.json ; echo $?
→ fatal: path 'scripts/hyaku/ufo-wave-policy.json' does not exist in '812ee0d…'   (128)
```
It exists at the fleet root only (`/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`:
`"waveMinLanes": 32`, `"waveMaxLanes": 64`). `LOG.md:2163` cites the same file by absolute path, so the
lane's own convention is the absolute form; the report's fleet-relative form does not resolve against the
lane it lives in. The band is independently supported by the lane's dispatch:
`.ufo/waves/round-41/dispatch-w1.json` → `policy.waveMinLanes=32`, `policy.waveMaxLanes=64`,
`counts.total=40`.

**D6 — low — the tip re-run has no receipt.**
Report: "Both counters were run again at the lane tip `812ee0d…` and printed the same two lines, exit 0
each."
```
git ls-tree -r --name-only 812ee0d .ufo/evidence/round-41/ | grep -i '812ee0d\|tip'
→ (no output)
```
The substance is true — the replay at the tip reproduces both lines and exit 0 (PASS-47) — but the round
meets its own committed-receipt standard at `baa18b7b` and `2ae00eb7` only, and not for this sentence.

## PASS — revision identity

1. tip `812ee0d11d267e131be3dc8db0b71253cbae9234` — `git rev-parse HEAD` → `812ee0d…`;
   `git log --oneline -1` → `812ee0d round-41: late seat report and census end exit code`.
2. measured `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6` — `git cat-file -t` → `commit`.
3. base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046` — `git cat-file -t` → `commit`.
4. freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937` — `git cat-file -t` → `commit`;
   `git log --diff-filter=A -- .ufo/evidence/round-41/contract.json` → `d4ee4e6`, matching "freeze:
   contract, v3 tool, fixtures, both counters".
5. digest `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` —
   `git show 812ee0d:tools/write-path-census-v3.py | sha256sum` → `095924a7…0279` (identical at
   `b37ce974` and `2ae00eb7`); it is the contract's `claims.C2.tool_sha256`, not a git blob id
   (`git rev-parse 812ee0d:tools/write-path-census-v3.py` → `84b4b430…`).
6. `b37ce974…` / `baa18b7b…` / `0c8e1be…` — all `git cat-file -t` → `commit`, and `git show --name-only`
   matches each landed-changes row (`0c8e1be` adds the `2ae00eb7` C1/C2 pair plus `census/end.stdout`;
   `812ee0d` adds `census/end.exit` and `w1/ScribeScorecard.md`).

## PASS — evidence files

7. `.ufo/evidence/round-41/calibration/measure.py` — present; replay prints the C1 line (PASS-44/45).
8. `.ufo/evidence/round-41/before/c1-at-base.stdout` — `m6=1 m9=1 total=2` verbatim; `…/c1-at-base.exit`
   = `od -c` → `1 \n`, matching "exit 1".
9. `.ufo/evidence/round-41/after/c1-at-baa18b7b.stdout` — `total=0` present, `rev=baa18b7b…`;
   `…/c1-at-baa18b7b.exit` = `0 \n`, matching "exit 0".
10. `.ufo/evidence/round-41/census/fixtures.json` — four fixtures; `symlink_unflagged` and
    `literal_unflagged` rooted at `tests/fixtures` (A2's re-root), `var_unflagged` a variable destination,
    `scratch_var` under `/tmp`.
11. `.ufo/evidence/round-41/census/measure.py` — present; replay prints the C2 line (PASS-46/47).
12. `.ufo/evidence/round-41/after/c2-at-baa18b7b.stdout` — the full `C2_R41: … C2_R41_PASS=true` line,
    containing every field the report quotes (`tool_sha_ok=1`, `var_expected=1`, `symlink_expected=1`,
    `live_var_lineno=811`, `live_symlink_lineno=820`, `mutant_*_killed=1`); `…exit` = `0 \n`.
13. `.ufo/evidence/round-41/sources/` — `git ls-tree -r -l` → `ast.html 362029`,
    `pathlib.html 271189`; `sha256sum` → `183a4f8c…5317`, `0044cae6…4f093`: the exact digests and byte
    sizes stated.
14. `.ufo/evidence/round-41/control/c2-control.{stdout,exit}` (cited by behaviour) — replay prints
    `C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0 C2_R41_CONTROL_PASS=false`, exit 1; `.exit` =
    `1 \n` — the declared control value.
15. contract pins (cited as "the contract") — C1 counter `9aaa99ac…`, C2 counter `83268eff…`, tool
    `095924a7…`, fixtures `20b6254d…`; each equals `sha256sum` of the tip file.
16. `.ufo/evidence/round-21/coldread/measure.py` — present; replay at `a3d6c690` and `2ae00eb7` prints
    `"calibration_restraint_score": 6`, matching "score 6 at the measured commit".

## PASS — lane paths

17. `tools/write-path-census-v3.py` — `git cat-file -e` → 0.
18. `tools/repeat-control.py:811` — `sed -n 811p` → `        with open(duplicate_path, "wb") as handle:`;
    `duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")`, under
    `scratch = tempfile.mkdtemp(…, dir="/tmp")` (line 597) — a variable destination and a scratch one,
    matching "v2 records a write site with no expected-value destination" (`live_var_sites_v2=1`,
    `live_var_expected_v2=0`).
19. `tools/repeat-control.py:820` — same command → `        os.symlink(`; target under
    `snap_stable = os.path.join(scratch, "snap-stable")` (line 766) — scratch, and invisible to v2
    (`live_symlink_sites_v2=0`).
20. `SCORECARD.md` — `grep -n '^#\+ *Round 41'` → `1895:## Round 41 — …`,
    `1965:### Round 41 — after the deciding run`; `:1944` carries the C1 no-self-pin hold the report's
    open-items paragraph refers to.
21. `corpus/lessons/round-41.md` — `grep -n '^#\+ '` → `78:## Holds`, `108:### C1 instrument`,
    `123:### C2 instrument`; `:51` = `### Correction — the round-40 quarantine summary`, stating "one
    adopted, six refused, ten present-but-not-appended" (the numbers behind `(1, 6, 10)`).
22. `corpus/knowledge/r41-variable-destination-writes.md` — present; header carries both source ids, both
    snapshot sha256 values, `ground: F4`.
23. `corpus/README.md` — `grep -n r41-variable-destination-writes` → line 517, coverage row citing S153,
    S154.
24. `corpus/QUALITY.md` — `grep -n 'Criterion 80'` → `967:### Criterion 80 — name the pins a tool edit
    breaks, before the edit`; it cites `considerthese/2026-10-24.md` proposal 1 and states the falsifier's
    three-revision behaviour. Falsifier replay (verbatim from the criterion):
    `d16f9b5 exit=0`, `691bb51 exit=1`, `5829676 exit=0` — as stated.
25. `LOG.md` — `grep -n '^## .*round 41'` → `2111:## 2026-10-25 — round 41: self-assessment
    reconciliation and variable-destination write census`. The section exists and carries the cited
    bullets; the duplication inside rounds 39/40 is D1.
26. `.ufo/waves/round-41/dispatch-w1.json` — parses; `taskCall` present with `tasks` → 40;
    `counts.total=40`; `note` = "Issue exactly one batched task call" — supporting "exactly one batched
    `task` call from the validator's `taskCall`".
27. `.ufo/waves/round-41/w1/` — `git ls-tree … w1/ | grep -c '\.md$'` → 40 reports, smallest 3154 B, none
    empty.
28. `.ufo/waves/round-41/w1/swarm-registry.json` — `members` 40; roles →
    `reviewer 10, executor 8, scribe 7, scout 6, critic 5, mutation-tester 3, connector 1` — the exact
    declared mix.
29. `.ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions}` — 109 / 103 / 2 lines; `reg-ids`
    equals the tip registry id set; `staged-ids` contiguous `S153`…`S255`; `collisions` = `S153`,`S154`;
    base∩staged = 0, tip∩staged = 2 — the stated 0 / 2.
30. `.ufo/waves/round-41/w1/CriticR40Discharge.md` — carries both halves the report leans on:
    `MISMATCH m9 … its table counts (1, 6, 10)` and the independent derivation
    `rows=17 adopted=1 refused=6 present=10`, plus the `m9=0` receipt at the round commit.
31. `.ufo/waves/round-41/w1/ExecV3Selftest.md` — `var_unflagged=1 symlink_unflagged=1
    literal_unflagged=1 scratch_var=0`, then A1 (line 70) and A2 (line 135) mutants killed with
    `FAIL planted var_unflagged` on the mutant — the first two of the three mutants.
32. `.ufo/waves/round-41/w1/MutFixtureVar.md` / `MutConstantClassifier.md` — the `tests/golden` →
    `tests/fixtures` re-root with the argument-swap mutant, and the constant-classifier kill, both present.
33. `SKILL.md`, `PROVINCE.md` — `git log --oneline a3d6c690..812ee0d -- PROVINCE.md SKILL.md` → empty,
    matching "was not edited" / "the round did not edit `SKILL.md`"; `PROVINCE.md:20` `"Out of province →
    report, never absorb"` and `:44` `"Adjacent — report, never absorb"` are the rules invoked.
34. `considerthese/2026-10-24.md` — `grep -n -i proposal` → `61:## Self-improvement ideas (proposals only,
    not acted on)` and `63:1. **Pin blast-radius report before a tool edit.**` — the exact proposal the
    QUALITY row and the report name.
35. `tools/write-path-census.py` absent at `31687496` — `git cat-file -e 31687496:tools/write-path-census.py`
    → `fatal: … exists on disk, but not in '31687496'` (128): the refusal's flip condition holds.
36. `tools/context-capture.py:1682` / `:1685` — `with open(expected_path, "wb") as handle:` and
    `with open(expected_path, "w", encoding="utf-8") as handle:` — write sites whose destination is a
    computed path, the stated false-positive class.
37. `tools/registry-replay.py:123` — `    (out / 'expected.json').write_bytes(…` under the `--out` root —
    the stated counted-because-explicit-flag case.
38. `kotodama-shokunin/tools/harness/{round_runner_conformance,receipt_guard_adoption}.py` — both exist;
    `grep -n depth` → `def _resolve(node, constants, runner_path, depth=8)` and `def collect(self, tree,
    depth=6)` / `def resolve(self, node, depth=6)`; both files mtime 2026-10-19 — the stated depths.
39. `.ufo/waves/round-41/settlement-receipt.json` — `registry_members: 40`, `reports_present: 40`,
    `empty_reports: []`, `dead_seats: []`.
40. `.ufo/waves/round-41/settlement-receipt.stdout` — `WAVE_PARENT: verdict=UNSETTLED detail=no seats`,
    `exit=1`.
41. `tools/wave-parent-settle.py` — `--receipt` replay → `WAVE_PARENT: verdict=UNSETTLED detail=no seats`,
    exit 1.
42. `~/.omp/logs/omp.2026-10-25.*.log` — the glob resolves (673 files dated 2026-10-25). Existence PASS;
    the reason attached to them is D2.
43. `.ufo/evidence/round-41/census/start.exit` / `end.exit` — `od -c` → `0 \n` and `0` respectively,
    matching "exit 0" for both census runs.

## PASS — numeric and quoted content (replayed)

44. `m6=1 m9=1 total=2` at base —
    `python3 .ufo/evidence/round-41/calibration/measure.py --lane
    /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046`
    → `C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=a3d6c690… C1_R41_PASS=false`,
    exit 1 — byte-identical to `before/c1-at-base.stdout`.
45. `total=0` at the deciding commit — same command at `baa18b7b` → `… m9=0 total=0 records=3
    sources_rows=109 rev=baa18b7b… C1_R41_PASS=true`, exit 0; identical line (rev aside) at `2ae00eb7`
    and `812ee0d`.
46. C2 before — `python3 .ufo/evidence/round-41/census/measure.py --lane … --rev a3d6c690…` →
    `C2_R41: tool_absent=1 var_expected=0 symlink_expected=0 rev=a3d6c690… C2_R41_PASS=false`, exit 1.
47. C2 after / tip — same command at `2ae00eb7` and at `812ee0d` → the exact 25-field line the report
    quotes, `… mutant_symlink_arg_killed=1 rev=<rev> C2_R41_PASS=true`, exit 0 both. This is the replay
    behind D6's "the substance is true".
48. `recorded_cases=9 depth_score=9` — command D from `SCORECARD.md:73` at `b37ce974`, `2ae00eb7`,
    `812ee0d` → `recorded_cases=9 depth_score=9` at all three (D3 concerns the label only).
49. `boxes=4 checked=0 asserted=4 untouched=0` — command C from `SCORECARD.md:75` at the same three
    revisions → `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8` at all three.
50. `calibration_restraint_score: 6` at base and round commit — coldread replay at `a3d6c690` and
    `2ae00eb7` → `"calibration_restraint_score": 6` both.
51. "79 mined / 22 queued / 6 rejected" at base — status-cell counter over
    `git show a3d6c690:corpus/SOURCES.md` → `Counter({'mined': 79, 'queued': 22, 'rejected': 6})`, 107 rows.
52. Id ranges and gaps — base holds 107 ids (`S001`…`S152`); gaps exactly `S038 S039 S098`, `S109–S131`,
    `S133–S151`; `S132` and `S152` present — the stated list, item for item.
53. "13 awk fields and carries no pipe" — `awk -F'|' '/^\| S15[34] /{print $2, NF}'` → `S153 13`,
    `S154 13` (a literal pipe in a cell would raise the count).
54. "Python 3.15.1 documentation" — `git show <tip>:…/sources/ast.html | grep -o '<title>…'` →
    `ast — Abstract syntax trees &#8212; Python 3.15.1 documentation`; same form for `pathlib`.
55. "A1–A5, all `before_data: true`; A2 and A5 `rule_changed: true`" — contract `amendments` →
    `A1 True False`, `A2 True True`, `A3 True False`, `A4 True False`, `A5 True True`. Exact.
56. "9 × W04 + 1 × W01, zero E codes" — `start.stdout`: nine `W04` lines (S047, S048, S075, S076, S077,
    S078, S081, S092, S104), one `W01` (S101), no `E`-prefixed line.

## Residual risk

**R1 — the report's evidence block is green-only where its own receipts are not.** `after/` holds a red C1
run: `git show 812ee0d:.ufo/evidence/round-41/after/c1-at-b37ce974….stdout` →
`MISMATCH m8 .ufo/waves/round-41/w1/swarm-registry.json cited but does not resolve at b37ce974…`,
`C1_R41: … m8=1 total=1 … C1_R41_PASS=false`, `.exit` = `1 \n`. `LOG.md:2175` and `SCORECARD.md:1979`
disclose it; the report's before→after block does not, so a reader of the report alone would not know an
intermediate C1 was red on a landing-order defect. (Two further copies of that same sentence also sit at
`LOG.md:2076` and `:2095` — D1.)

**R2 — the worktree diverges from the tip, and the divergence is a live repair of D1/D3/D6.**
`git diff --stat` in the lane at check time → 7 paths: `census/command-d.stdout` (+8 lines: `## 2ae00eb7`
and `## 812ee0d` re-runs of commands C and D), `contract.json` (+2/−2), `w1/ReviewScorecardNumbers.md`
(+67), `w1/ScribeScorecard.md` (+46), `LOG.md` (28 changed: the stray round-41 bullets in the round-39 and
round-40 sections replaced by one-line round-appropriate bullets — i.e. D1 being repaired), `SCORECARD.md`
(25), `corpus/lessons/round-41.md` (6). Every content statement above is `git show <tip>:<path>`. If those
edits land committed, D1, D3 and D6 close and the tip changes; uncommitted, they change nothing at the tip.
A filesystem-based reader of the lane right now sees different bytes than this report describes.

**R3 — `before_data: true` is a self-attestation with no ordering artifact.** The base, control and
census-start receipts were all *added* in `b37ce97` — the same commit that carries A1–A4:
`git log --diff-filter=A -- .ufo/evidence/round-41/before/c1-at-base.stdout` → `b37ce97`. No git-level
ordering exists between the receipts and the amendments, so "No default-mode run preceded them" can be
neither confirmed nor refuted from the repository. It rests on the L1's word, plus the structural fact that
a base-revision run cannot exercise the amended counter. This is the one claim in the report with no
artifact at all behind it.

**R4 — settlement is missing on a different leg than stated (D2).** The parent genuinely has no exit line
(0), and 2 of 40 wave-1 seats (`ReviewScorecardNumbers`, `ScribeScorecard`) have no `Session exit recorded`
line while 38 do. A successor receipt can be populated from that log and would then resolve on evidence
rather than on a claim of impossibility.

**R5 — the C2 counter has no `--selftest` mode.** `python3 .ufo/evidence/round-41/census/measure.py …
--selftest` → `measure.py: error: unrecognized arguments: --selftest`, exit 2; accepted arguments are
`--lane --rev --control --fixtures`. The `selftest_exit=0` field in the C2 line is the *tool's* selftest run
in-process, which is what the report says — the assignment's framing, not the report, mismatches the CLI.

**R6 — D1 is invisible to the round's own instrument by construction.** C1's m8 resolves cited paths, and
every path the stray bullets cite resolves at the tip; m9 reads the round-40 *lesson*, not `LOG.md`. So
the duplication could land, persist through three commits, and leave both counters green. A class for
"citation appears under a section for another round" does not exist in either counter.

## Verification gaps

- Only the four seat reports the report names by name were read for content; "40 of 40, none empty" is
  size-based.
- "Dead seats: 0" was not re-derived from hub-side deliveries; all 40 registry members carry
  `agentId: null`, so the registry alone cannot distinguish spawned-and-settled from never-spawned.
- `corpus/lessons/round-40.md` was not re-audited; `git log -1 --format='%h' -- corpus/lessons/round-40.md`
  → `4678127`, i.e. untouched since before the base — all the report claims.
- The round-end `census` run I replayed read the worktree `corpus/SOURCES.md`, which is unmodified since
  the tip; its `rows 109` therefore describes the tip.
- Install log: none.
