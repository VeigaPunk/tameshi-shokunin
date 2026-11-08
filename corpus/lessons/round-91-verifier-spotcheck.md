author: hyaku closure (non-author integrator, @m_zfl)

# Round 91 — verifier spot-check (non-author)

Subject: tameshi round 91. Lane tip `63172b9889475103aeca976d37389d204010dd11`, base
`87d1635c8a1a90a405eb348da5ba3e8f93b4ae83`. Report: `.ufo/reports/round-91/tameshi.md`
(fleet commit `fc79b52f88d105a7378eff6f037cda34fe8b522d`, author `tameshi-shokunin`,
2026-11-08T02:12:51-03:00). Gate under review: `corpus/lessons/round-91.md` `## Gate` and
the round's own claims. This file is the only lane path this session writes; no
lane-authored file was edited, and no `[x]` was written into `SHONEN.md`.

Dispatch digest, copied from `.ufo/watchdog.log` at closure (the log is mutable):
- `2026-11-07T22:59:05-03:00 launch tameshi round=91 pgid=3454474 driver=hyaku-inline attempt=1`
- `2026-11-08T02:13:26-03:00 complete tameshi round=91; hyaku-inline attempt=1`

## 1. Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-91/tameshi.md` (fleet root) | `tameshi-shokunin tameshi@shokunin.local fc79b52f… 2026-11-08 02:12:51 -0300` (earlier draft `942374c4`, 02:06:52) | ok; filed after lane tip `63172b98` (02:12:01) and before the completion line (02:13:26) |
| `SHONEN` heading, one line per box | read of report §SHONEN; `grep -c '^- \[' SHONEN.md` | 4 lines, all `[~]` with pointers; `SHONEN.md` carries exactly 4 boxes | ok |
| Cited lane commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for `ace200b5 343b0347 048c3f30 3d3eee6b 75443431 0b63b85e bf085287 16ff3195 ee484d3b 50e59d59 eff7ca84 50fd2b88 69ecfeee 6a748fc1 336f0803 584bbe3c 8e46b3f4 8a4352a4 7a5e79f5 63172b98` (+ base `87d1635c`) | all 20 resolve; all `ancestor` | ok. `34a92bbf`, cited in §Claims as a *state*, is a scratch-clone object (`git cat-file -t` = missing); the pointer that resolves is the committed receipt `w1/T91C1-attack1.out` — named, status-neutral |
| Round commits by the lane identity | `git log --format='%h %an %s' 87d1635c..63172b98` | 21 commits: 20 `tameshi-shokunin`; 1 operator (`7c8c6553`, `considerthese: 2026-11-07 daily reflection`) | ok; the operator commit carries `considerthese/2026-11-07.md`, not lane round work — noted, status-neutral |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=63172b98 remote=63172b98 ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `63172b98…` | ok |
| Round is pure addition | `git diff --numstat 87d1635c 63172b98 \| awk '$2!=0'` | empty (139 files, 41820 insertions, 0 deletions) | ok |
| Prompt carries the template contract | `diff` of `templates/round-prompt.md` (140 lines) vs `.ufo/prompts/tameshi-round-91.md` lines 1–140 | only placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §§1–5 verbatim at the same line offsets; hyaku addendum §6 plus §§7… follow | ok. No MISSION.md bucket route map is quoted; §3 defers to the host route table. Prompt committed by `tameshi-shokunin` (`7ecf0699`) |
| Required report sections, in order | `grep -n '^## ' .ufo/reports/round-91/tameshi.md` | Work performed (:21), Landed changes (:80), Before → after (:96), Sources & frontier (:127), Trend verdicts (:153), SHONEN (:166) | ok |
| Misroot sweep | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | 5 entries, none tameshi-authored; fleet-root `plans/round-91.md` read: limine pin battery + `corpus/knowledge/limine-unverified-image-r91.md` = tsukuroi r91 host work, as the report routes | ok |

Marker test: the report names real committed work with resolving pointers and every
required section — a real report, not a marker. Status **ok**.

## 2. Claims (step 2) — both withdrawn by the round, both verdicts agreed

### 2.1 R91-C1 (coverage, sealed successor counter) — `unprovable`

Re-measured / re-read myself (committed bytes):

| Item | Command | Observed | Agrees with report |
|---|---|---|---|
| Honest-fixture predicate | read `pre-freeze/controls/CTL14-pos.out` | 16/16 conjuncts `true`, `C1_R91_PASS=true`, exit 0 | yes |
| Landing state at `8e46b3f4` | read `landing-c1-at-8e46b3f4.txt` | 15/16 conjuncts true, `source=false`, `C1_R91_PASS=false`, exit 1 | yes |
| Why `source=false` | `git show 8e46b3f4:corpus/knowledge/mutation-case-fleet-sources-census.md \| grep '^source:'` | cites S316, S317, S001; S318 absent — the note's `source:` line was not rewritten (the amending claim was killed) | yes |
| Kill rule (a), parser | read `w1/T91C1-attack1.out` + `T91C1-attack-note.md` | state `34a92bbf`: `C1_R91_PASS=true`, exit 0, `note=present mismatched=0`; the note's *presented* table `C001`–`C012` is the exact negation of the true table `C01`–`C12` (spot-verified on 8 of 12 rows); `parse_note`'s row regex `^\|\s*(C\d\d)\s*\|` cannot key three-digit ids, so the hidden table is invisible rather than ambiguous | yes — row real |
| Kill rule (a), freeze integrity | `git diff 50e59d59 0b63b85e -- .ufo/evidence/round-91/c1/measure-v91.py` | at the freeze `v = cells[vcol + 1]` (one cell past the named `verdict`), with `parse_note(nt, ids)`; the fix to `v = cells[vcol]` + header-indexed lookup landed at `0b63b85e`, **after** the freeze, and the control receipts were committed after it (`69ecfeee`, `50fd2b88`, `6a748fc1`) | yes — row real. Statically, on a standard row `\| C01 \| … \| KILLED \| witness \|` the frozen index reads the witness cell, which is not in `{KILLED, SURVIVED}`, so the frozen bytes refuse every honest row; receipts printing `ids=true` cannot come from them |
| Spec bytes pinned before any receipt | `git show ace200b5:.ufo/evidence/round-91/c1/census-mutants.json \| sha256sum` | `ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290` | yes (`ce8983d5…e290`) |

Independent measurement of the *subject* (never the lane's counter): I extracted the pinned
fleet gate with `git archive f47ad6ba8d306f8125597401cb2ce45c1297a593 scripts/sources-census.sh
scripts/fixtures/sources-census` into a scratch dir under `/tmp` (removed afterwards),
confirmed `sha256sum` = `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`
(the pin), then ran `bash scripts/sources-census.sh selftest` with `TMPDIR` in scratch:
pristine → exit 0 `selftest ok`; C11 edit (`&& exit 2` → `&& exit 1`) → exit 3
`selftest FAILED` (KILLED); C12 edit (`path=$(trim_cell "$path")` → `path=$path`) → exit 0
`selftest ok`, twice (SURVIVED). Both match the case note `:80-81` (`C11 KILLED`,
`C12 SURVIVED`): the measured table is sound; the counters that certified it were not.

Verdict: **unprovable** — the predicate is reachable on an honest fixture, but two
committed counterexamples (a PASS with the presented verdicts inverted, and receipts that
certify post-freeze bytes) show the predicate true where the claim's wording is false. The
lane's own verdicts (`C1 unprovable`, "killed by rule (a) three ways") agree.

### 2.2 R91-C2 (calibration, argv-binding successor) — `unprovable`

| Item | Command | Observed | Agrees with report |
|---|---|---|---|
| Three clone states, one PASS each | read `pre-freeze/controls/C2-pos.out`, `w1/T91C2-reject.out`, `w1/T91C2-falsereason.out` | all print `rows=ok argv=ok toolpin=ok blobrun=ok … C2_R91_PASS=true`, exit 0, at three distinct revs (`9603b833`, `760c4ee2`, `d140f2e5`) | yes — row real |
| `toolpin` is a tautology | read `c2/measure-c2-v91.sh:59-62` | `expect=$(sha256sum "$WORK/blobrun-ledger-witness.py" …)` and `pinned=$(sha256sum "$WORK/blobrun-ledger-witness.py" …)` hash the *same file*; `[ "$expect" = "$pinned" ] && toolpin=ok` | yes — structurally can only fail on a missing blob, never on a wrong pin |
| Landed state | read `landing-c2-at-8e46b3f4.txt` | three rows: two `closed`, `R90-2-lesson-receipt-addendum … state=open`; `rows=fail`, `argv/toolpin/blobrun=ok`, `C2_R91_PASS=false`, exit 1 | yes |

Verdict: **unprovable** — the manifest binds token presence, not the repair; the honest and
two forged clone states are indistinguishable to it, and one named conjunct cannot fail. The
lane's verdict agrees. The four record repairs are real and stay landed as upkeep
(`corpus/knowledge/…census.md` admission marker, `corpus/README.md` round-91 map position —
both read in the diff; pure addition).

### 2.3 §8 pre-file falsification ledger

```
$ python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tameshi --round 91
PREFILE-FALSIFICATION: pass claims=2 rows=15 attack_seats=7 findings=0
exit=0
```

`.ufo/waves/round-91/claim-falsification.tsv`: 15 rows covering `claims.json` C1 and C2; all
seven attack seats (T91R1, T91R2, T91C1, T91C2, T91M1, T91CN1, T91SN1) appear; 9
`falsifies-wording` rows, each naming `plans/round-91.plan.md` § Amendments A1/A2; 6
`neutral`. Adjudication: the three load-bearing falsifying rows (parser invisibility ×2,
toolpin tautology, three-PASS manifest) are real and I re-verified them directly; the
`T91R2` summary contradiction and the `T91SN1` driver findings are committed receipts I read
and found internally consistent with their cited files. No row is spurious, so both claims
fail to verify at the frozen wording — as reported.

### 2.4 Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | `unprovable` | R91-C1 predicate met on an honest fixture, killed by rule (a); no score move — `SCORECARD.md` Round 91 section |
| calibration | `unprovable` | R91-C2 predicate met, killed by rule (a); score 8 unchanged |
| depth | `unchanged` | no recorded-case or ledger leg added; SCORECARD states depth 10 |
| freshness | `unchanged` | two new SOURCES rows, no re-pin or recheck-cadence move; score 9 unchanged |
| operability | `unchanged` | no tool admitted; instruments retained under the evidence tree (lesson § Routed addendum) |
| adjacency | `unchanged` | no sibling-lane artifact edited; the fleet arms patch is report-only (`w1/T91E3.md`) |

No axis is harmed: `git diff 87d1635c 63172b98 -- SCORECARD.md` is narrative-only (no
numeric row changed), and the QUALITY/lesson diffs are pure additions
(`git diff … | grep -c '^-…'` = 0).

## 3. Discernment spot-check (step 3) — `corpus/lessons/round-91.md` `## Gate`

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S318 git(1) `GIT_NO_REPLACE_OBJECTS` | admit (A, mined) | re-fetched https://git-scm.com/docs/git live | **agree** | live body is byte-identical to the committed snapshot (244227 B, sha256 `534c674f…f9d1`); the quote "Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects." is present at `T91S1-git-env.txt:1432-1433`, 18 words ≤ 25; it grounds the seal the counter actually uses (`sealed_env()`) |
| S319 git-replace(1) DESCRIPTION | admit (A, mined) | re-fetched https://git-scm.com/docs/git-replace live | **agree** | identical bytes (38351 B, sha256 `70ca75f4…ec0`); tag-stripped body says "Adds a replace reference in refs/replace/ namespace." (`T91S2-git-replace.txt:1661`), 7 words; it grounds the `git replace -l` refusal the counter implements |
| Claim candidate: amend C1 down to "the counter refuses a note whose verdict presentation is not the spec's" | reject | `w1/T91C1.md` §1; `w1/T91R1.md` F1; committed `measure-v91.py` at `50e59d59` vs `0b63b85e` | **agree** | both kill grounds verified in committed bytes: the three-digit-id table is invisible to the row regex, and the frozen parser reads `cells[vcol + 1]`; nothing enforceable is left to amend to |
| Claim candidate: amend C2 down to "the manifest rows close" | reject | `w1/T91C2.md`; `w1/T91R2.md` §2.3; `c2/measure-c2-v91.sh:59-62` | **agree** | the three clone receipts all PASS, and `toolpin` hashes one file against itself — the rejection names the property a successor must bind (parseable admission fields, pinned checker blob) |

SOURCES registry: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tameshi` → `tameshi ok …/corpus/SOURCES.md`, exit 0, 21 warnings (20 pre-existing + the new
`W04 S318 duplicate url git-scm.com/docs/git across scopes`, the declared cross-scope family).
Rows 177 → 179 (`grep -c '^\| S[0-9]'` at `87d1635c` and `63172b98`), `git diff --numstat …
-- corpus/SOURCES.md` = `2 0`.

## 4. Trend verdicts (step 4)

- **expansion: unchanged** — two mined rows (S318, S319) and no admitted `knowledge/` entry,
  no coverage-map move into Core, no capability row (`SCORECARD.md` diff adds no capability
  row). A killed claim carries no expansion credit. Agreed.
- **quality: unchanged** — no held entry re-verified or superseded; the case note's admission
  marker and the README map position are status annotations (record upkeep for the round-90
  routed items 1–2), not a re-verification. Agreed.
- **discernment: improved** — the outside spot-check agrees with the gate on 2/2 admits and
  2/2 rejects above, and the round's own wave killed both claims before filing with committed
  counterexamples that became QUALITY 143–149, each naming a state shown able to fail. Agreed.

## 5. Routed defects (the lane's next round)

1. **Stale count mentions at the final commit.** `63172b98` adds QUALITY 149 and Mistakes M7,
   but `LOG.md:4988` still reads "QUALITY 143-148. Mistakes M1-M6" and
   `corpus/lessons/round-91.md` § Learning trends still reads "QUALITY 143-148". The report
   and `SCORECARD.md` say 143–149. Append corrections next round (append-only files); a
   corrected fact left standing in a sibling file is a defect.
2. **`claims.json` names a different freeze rev than the plan and report.**
   `.ufo/waves/round-91/claims.json` carries `"freeze": "ee484d3b…"` (the claims commit),
   while the plan, report and the freeze-integrity finding all name `50e59d59…` as the rev
   that carries the instrument bytes. Pin the same full hash in claims.json, the plan and the
   report next round; with instruments, the freeze rev is the rev whose bytes the receipts
   must certify (QUALITY 144).
3. **Carried (lane-owned, already routed):** the pre-freeze battery was produced by bytes that
   post-date the freeze; the successor must pin its own sha256 in the freeze and assert it at
   run time. Keep on the queue until it lands.
4. **Fleet misroot, not the lane's:** `/home/vgpnk/Projects/shokunin/plans/round-91.md` is
   tsukuroi r91's limine work; routed to tsukuroi by the report and left in place.

Notes for the operator: the strict §6 attack set (reviewer + critic + mutation-tester) is
5/14 = 36 % of the wave, above the 25 % floor; the report's 7/14 = 50 % also counts the
connector and sentinel seats. SHONEN boxes 1 and 2 look independently checkable from
committed artifacts (`SKILL.md` decision table `:86`, error-pattern/defect-taxonomy `:274`,
numbered checklist `:159`; the round-91 `LOG.md` entry); promotion remains operator-owned and
no `[x]` was written here.
