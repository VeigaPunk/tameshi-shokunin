# Round 85 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Date: 2026-11-04. Reviewed base `45fa68046b0ce8c285ce161f3c6e164e6e721f06` → final `2758f513f768084f406dd6ce1a3932997f9f5e8a`. Independent closure reviewer: this integrator session (non-author). No lane-authored counter, production CLI, gate or selftest was executed during closure; lane artifacts were read from committed bytes by plain git/grep/wc/sha256 and Python over `git show` output.

## Decision

Status **ok**: real landed work, not a marker; six cited lane commits resolve and are ancestors of the branch tip. **Not admitted; rejected-honest-stop.** R85-C1's frozen eight-case predicate is literally green, but the round's own critic produced a no-git basename oracle that reaches the same 8/8. The lane declined certification before this review, kept the counterfeit witness, and changed no predicate or score. No owned axis is harmed: the change is a new standalone read-only tool, no existing tool or held entry was modified, and the score rows are unchanged.

| Axis | Verdict | Evidence |
|---|---|---|
| operability | unprovable | `tools/design-blob-audit.py` exists at the tip and its committed receipts are internally consistent, but the only frozen certification predicate accepts an oracle that performs no git read, no receipt parse and no hash; the claimed committed-object audit is not certified and no capability row or score delta was claimed. |
| depth | unchanged | No new decision-table/error-pattern knowledge claim; SKILL.md gained only the tool's registry row, appended. No harm observed. |
| calibration | unchanged | Honest-stop is correctly retained (M4) rather than relabelled, but criterion 111 stood before the freeze and was missed; no numeric calibration move was declared and the score stays 8. |
| freshness | unchanged | Bounded preservation receipts exist; no separately declared freshness move. No harm observed. |
| coverage | unchanged | No frontier-Core move; SOURCES rows 171→171 and no surface added to PROVINCE.md. |
| adjacency | unchanged | Connector compared kaidoku/kumitate committed-object methods read-only; no absorption or contested-scope claim. |

Scores remain depth10/calibration8/freshness9 (delta0); no capability enters `## Capabilities`. This axis table is the closure ledger's verdict table.

## Step-1 conformance

Report `.ufo/reports/round-85/tameshi.md` is committed in the fleet repo at `33b5fbb04e276712a138086e0294900142e1acd7`, author and committer `tameshi-shokunin <tameshi@shokunin.local>`, commit time 2026-11-04 15:35:56 -0300. It is an ancestor of `origin/master` (exit0) and was filed after the lane tip (`2758f513`, 15:34:04 -0300), so commit-before-report holds. It carries the required sections in order (Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN); the SHONEN heading has four `[~]` lines for the four `SHONEN.md` boxes and no `[x]`. It cites six lane commits, each tied to the round-85 `LOG.md` entry; all six exist and pass ancestry against the branch ref (never `@{u}`):

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
for h in 118dbc80 5a3cba20 2cc738d9 ecb61d56 288f826d 2758f513; do
  git cat-file -e "$h^{commit}" && git merge-base --is-ancestor "$h" refs/heads/master
done
```

Observed: `exists=yes ancestor=yes` for all six; branch tip `refs/heads/master` = `2758f513f768084f406dd6ce1a3932997f9f5e8a`. The lane repo is detached (jj-colocated), so ancestry was tested against the branch ref only.

Lane cleanliness and push state (helper is pure git, read-only):

```sh
/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/tameshi-shokunin
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-remote origin refs/heads/master
```

Observed: `state branch=master local=2758f513f768084f406dd6ce1a3932997f9f5e8a remote=2758f513f768084f406dd6ce1a3932997f9f5e8a ahead=0 behind=0 head=detached tracked=0 untracked=0`; `status --porcelain` empty; `ls-remote` `2758f513f768084f406dd6ce1a3932997f9f5e8a refs/heads/master`. No uncommitted round work and no unpushed round commit.

Prompt fidelity: rendering `templates/round-prompt.md` with lane `tameshi`, round `85`, fleet root and the lane axes and line-comparing it against `.ufo/prompts/tameshi-round-85.md` yielded two mismatches, both expected: the rendered `<tameshi-repo>` placeholder versus the actual `tameshi-shokunin` path, and the addendum separator line before §6. Sections 1–5 (mission/axes binding, 1–3 claims, frontier step, L2 floor, report contract with path and SHONEN heading, commit-then-push and write scope) are byte-equal apart from those two. The five child-lane items are present: report path/filename, commit-before-report ordering, `SHONEN` heading, commit-hash citation, lane write scope. The prompt's last routing line is the all-18-`@m_zfl` operational note; the report's "configured routes" wording matches that line and does not claim answering-provider history. `MISSION.md` §L2 keeps the role-class bucket advisory; no bucket conflict appears.

Wave evidence: `.ufo/waves/round-85/w1-dispatch.json` carries one `taskCall` with 9 tasks (executor3; scribe, scout, reviewer, critic, mutation-tester, connector each1); `w1.ready` names lane/round/wave/dispatch/l1 and `w1.ready.dispatched` records one dispatch; `w1-results.json` lists 9 settled seats; `settlement.json` reports 9 seats, 9 named reports, attack3/9=33.3 %, residual0, dead0, planner L1. `w1-spec.json` maxLanes16, so 9 seats sit inside the run-15 8–16 band and above the protocol L2 floor of 8.

Dispatch/complete digest (copied from the mutable log, not a line-number citation):

```text
2026-11-04T12:50:51-03:00 launch tameshi round=85 pgid=117779 driver=hyaku-inline attempt=1
2026-11-04T15:36:12-03:00 complete tameshi round=85; hyaku-inline attempt=1
```

## R85-C1 — re-measurement versus evidence verification

**Re-measured by this reviewer (plain committed-byte measurement, no lane module imported):** the end-to-end demonstration population and the freeze/tool identity facts.

1. Freeze immutability. `git show 118dbc80:.ufo/evidence/round-85/measure.py | sha256sum` = `1e5d60718f1ac6205ff1f5f33a51a9b7ac2ae7800a5bad1e68ce74ab8e83d6f4`; `git diff 118dbc80 2758f513 -- .ufo/evidence/round-85/measure.py | wc -l` = `0`. The counter bytes scored are the counter bytes at the tip.
2. Tool absence → presence. `git cat-file -e 45fa6804:tools/design-blob-audit.py` exits128 (`path ... exists on disk, but not in '45fa6804'`); at the tip the path exists with SHA256 `6194a30d96287e69932581704b6d1941e3f21af3a7210a6c3d9ed3f1f9869349`, identical at measured revision `ecb61d56` and at `2758f513`, matching the `# tool_sha256:` line in `final/selftest.txt` and `final/real-demo.txt`. `git diff --name-status 45fa6804 2758f513 -- tools/` prints only `A tools/design-blob-audit.py`; no existing tool was modified.
3. Real-task population, independently re-derived. A Python loop over `git show REV:PATH` bytes: select `.ufo/evidence/round-79/*.txt` containing `# design_base:`, parse `design_tool` and `design_tool_sha256`, hash the candidate path's blob at `45fa6804`, compare:

```text
population files: 7
carried= 3 different= 4
```

Matches `final/real-demo.txt` (`receipts=7 carried=3 orphan=4`, exit1) and the scout's independent committed-byte classification. The three carried receipts are `c2-base-selftest.txt`, `c3-base-selftest.txt`, `r78-control-rerun.txt`; the four different are `c1-base-sweep.txt`, `c1-false-correction.txt`, `c2-control-battery.txt`, `c3-control-battery.txt`.

**Evidence-verified under PROTOCOL Gate standard (committed receipts, not re-executed):** the frozen before/after and selftest tallies.

```text
before.txt       8 CASE lines, 0 ok=true, DESIGN_CAPABILITY: cases=8 passed=0 mismatches=8 R85_C1_PASS=false, exit1, measured_rev 118dbc80, candidate_rev 45fa6804
accept-control   8 CASE lines, 0 ok=true, same 0/8/false, exit1
final/after.txt  8 CASE lines, 8 ok=true, DESIGN_CAPABILITY: cases=8 passed=8 mismatches=0 R85_C1_PASS=true, EXIT=0, measured_rev ecb61d56
final/selftest  21 ': PASS' arm lines, DESIGN_BLOB_AUDIT_SELFTEST: 21/21 pass, EXIT=0
final/supplemental  4 JSON case records (1 positive preflight + 3 counted), SUPPLEMENTAL_PROBE: cases=3 passed=3 mismatches=0, EXIT=0
```

The constant-accept control's actual 0/8 differs from the plan's predicted seven failures; the error is disclosed and retained as M2, and the target was not changed after scoring. The supplemental receipt's four `ok` records against a `cases=3` summary are explained by the probe source: the preflight record returns early and is not part of the counted three. It is a labelling clarity debt, not a false tally; routed below.

**Why certification does not verify.** The frozen `ok` expression requires an exact exit code and empty stdout on the four setup cases, but on the four row cases only requires a state token and a summary substring; it never requires a `DESIGN_BLOB_ROW` prefix, a row path, an anchored/unique summary or whole-output shape, and it passes the `--root` name to the instrument. `T85C1.md`'s committed counterfeit reads only `--root`, performs zero git reads, emits no row records and a malformed summary suffix, and still scores 8/8 exit0. That mechanism is visible in the counter's own committed bytes; I did not execute either instrument. The lane's reject is therefore correct on its own evidence, and its honest-stop (no repertoire row, no score increment, no predicate rewrite) is the right disposition. This is the same class as round 59's cheat-passable counter; criterion 111 already required the cheat family before freeze.

**No-harm check.** `git diff 45fa6804 2758f513 -- SCORECARD.md` is append-only: scores remain depth10/calibration8/freshness9, no retirement or saturation change, and round 84's rejected wrong-axis claim is untouched. `corpus/SOURCES.md` changes only S289's used-by cell (8→9 paths, adding `corpus/lessons/round-85.md`; status mined, recheck 180d and every other cell unchanged). `SKILL.md` gains only the appended round-85 registry row. Bounded receipts in `final/checks.json` and the named sweeps support the preserved floors; they are lane runtime evidence, not closure reruns.

## Discernment spot-check

Sources re-opened on 2026-11-04; committed source bytes inspected at the tip.

| Item | Gate decision | Re-opened source | Outside judgment | Reason |
|---|---|---|---|---|
| Bounded design-receipt audit and its reviewer repairs | admit (to retained lane tools, not the repertoire) | `tools/design-blob-audit.py` at `2758f513` (SHA256 `6194a30d…`, identical at measured `ecb61d56`); `final/selftest.txt` 21 PASS arms; `final/real-demo.txt` | agree | The committed tool exists, is read-only, and its receipts are internally consistent; the real-task population re-measured 7/3/4 exactly. Admitting it as retained tooling rather than a capability matches what the receipts show. |
| R85-C1 capability certification | reject (honest-stop) | `measure.py` `ok` expression; `T85C1.md` counterfeit source and 8/8 receipt | agree | The counter's row cases bind on substrings and the exposed `--root` label; a no-git oracle reaching the same 8/8 defeats the frozen predicate as capability evidence. Keeping the witness and refusing an after-scoring predicate fix is the correct handling. |
| S289 re-open (source row) | admit as a scoped A row; used-by delta only | https://git-scm.com/docs/git-cat-file, page last updated in 2.56.0 (2026-09-28), §DESCRIPTION and §OPTIONS `-t` | agree | Both quoted strings are present verbatim on the live page. Measured whitespace tokens: lesson quote 11, row `teaches` quote 18, both ≤25. The quote supports raw object inspection only, which is exactly the scope the row and lesson state. |
| S293 duplicate row | reject | `corpus/SOURCES.md` S293 at `2758f513` | agree | The row is `rejected` with a within-scope duplicate reason naming S289 and a stated flip; the URL is already held as S289, so no second row is justified. |

No new `SOURCES.md` row was written this round: S289 was re-opened and only its `used-by` cell moved, while S293 stays rejected. The frontier step's sourced-claim link therefore rides the re-opened row (lesson Gate and `.ufo/evidence/round-85/source-cat-file.txt` cite it), not a new row.

Required census command run independently:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Observed exit0 and `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`; W01 S101 tierC mined and W04 duplicate-URL warnings retained (S047,S048,S075,S076,S077,S078,S081,S092,S104,S160,S265,S266,S267,S268,S274,S288,S293,S303). The same warning set appears in the report's before and after blocks; nothing was erased.

## Learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | SOURCES rows 171→171, admitted knowledge 0, frontier-Core 0, capability rows 0. A re-opened row's used-by delta is curation bookkeeping, not coverage growth. |
| quality | unchanged | No held entry was superseded or re-verified as a separately claimed move; the new tool is additive. The repaired implementation raises no existing entry's quality and no stale entry was left unmarked. |
| discernment | unchanged | The final gate decisions agree with this outside review, but the load-bearing event is a missed standing criterion (111) at freeze; the catch came from the round's own adversarial seat, no new grounded QUALITY criterion was added, and M4 retains the failure. Agreement on an honest-stop does not show improved recognition. |

## Routed defects — tameshi next round

1. Before any successor certification freeze, execute criterion 111's cheat family (fingerprint, invocation-sequence, pinned-hash, always-accept) and require data-derived expected rows with a complete anchored output shape. Do not amend R85's frozen counter or its predicate; a discriminating counter is a new freeze.
2. Label the supplemental preflight record distinctly from the counted cases, or count every printed case in the summary, so `4 ok` records cannot be read against `cases=3`.
3. Derive control predictions from the instrument's actual required tokens before declaring them (the constant-accept "seven failures" was wrong); if unmeasured, say so. M2 already records the miss.
4. Preserve M5's inherited-`GIT_*` limit on the frozen counter and the existing debts: receipt race/parent aliases, conversion, caller revision authority, malformed kind/source-id.
5. Keep the failed certification witness and the rejected verdict unchanged; a later green run on a new counter never retroactively repairs R85.

No lane-authored file was edited; only this verifier artifact is closure-owned. No tools installed or updated. SHONEN promotion is operator-owned: the four boxes now look checkable by a non-author from committed artifacts (registry, end-to-end round-79 audit, executable instructions, province scope), but this closure wrote no `[x]` and ran no promotion audit. Self-evaluation: accuracy4 (runtime evidence necessarily indirect); completeness4 (all four duties bounded and evidenced); clarity4 (claim/trend separation explicit); actionability4 (routed defects name the next freeze); conciseness3 (required command/output evidence lengthens the record). Overall3.8/5. Improvement: require the cheat family to run before the declaration commit, not only after settlement.
