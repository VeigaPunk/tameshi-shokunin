author: hyaku closure (non-author integrator, @m_zfl)

# Round 87 — verifier spot-check (non-author)

Subject: tameshi round 87 — lane tip `d91971194f6e1d12cdcbed3e22bb4ed8857109bd` (base `4a079f6ab57ab2f47b9e502a35eca75ec180cda7`).
Report: `.ufo/reports/round-87/tameshi.md` (fleet commit `9e4f6fdf6b5a30c3872ba60e629a3bbdcab57691`, author `tameshi-shokunin <tameshi@shokunin.local>`).
Gate under review: `corpus/lessons/round-87.md` `## Gate`. This file is non-author; the lane did not write it and it does not alter any lane-authored file.

## 1. Conformance (step 1)

| Check | Command (read-only) | Observed |
|---|---|---|
| Report attribution | `git log --format='%an %H' -- .ufo/reports/round-87/tameshi.md` | `tameshi-shokunin <tameshi@shokunin.local> 9e4f6fdf…` (lane identity) |
| SHONEN heading | `grep -n '^## SHONEN' .ufo/reports/round-87/tameshi.md` | line 116; four `[~]` lines, one per box |
| Lane SHONEN.md boxes | `grep -cE '^\s*- \[' tameshi-shokunin/SHONEN.md` | 4 |
| Cited commits exist | `git cat-file -t` on `a3b4f75d`, `38c83698`, `1d5102a1`, `ccd6ac26`, `d919711` | all `commit` |
| Ancestry vs branch | `git merge-base --is-ancestor <h> refs/heads/master` (branch is `master`; HEAD detached under jj) | all five: yes |
| Lane state | `scripts/hyaku/jj-lane.sh state tameshi-shokunin` | `local=d919711… remote=d919711… ahead=0 behind=0 tracked=0 untracked=0` |
| Porcelain leftovers | `git -C tameshi-shokunin status --porcelain` | empty |
| Remote tip | `git ls-remote origin refs/heads/master` | `d91971194f6e1d12cdcbed3e22bb4ed8857109bd` |
| Watchdog digest | `grep -n 'tameshi round=87' .ufo/watchdog.log` | `2026-11-05T04:18:36-03:00 launch tameshi round=87 pgid=2189280 driver=hyaku-inline attempt=1`; `2026-11-05T05:18:49-03:00 complete tameshi round=87; hyaku-inline attempt=1` |
| Prompt fidelity | rendered `templates/round-prompt.md` (lane=tameshi, round=87, fleet root, axes) diffed against prompt §1–§5 | identical except the rendered title line (the addendum prepends its own header); all §1–§5 items present, including the five child-lane items and the frontier step |
| Wave evidence | `git ls-tree -r --name-only d919711 .ufo/waves/round-87/w1/` | 10 seat files (`T87E1, T87E2, T87E3, T87SC1, T87CN1, T87S1, T87R1, T87C1, T87M1, T87SN1`) plus spec, dispatch, ready, results |
| Tools touched | `git diff --stat 4a079f6a d919711 -- tools/` | `capability-census-v2.py` and `.json` added (+794, no deletions); no existing tool modified, as claimed |
| Attribution / marker | report carries real committed hashes, evidence pointers and per-claim measurements | not a marker: `status ok` |

Conformance defects (status-neutral, routed in §6): C2 item 1 names the wrong manifest (§3.2); counterfeit sources not committed (§3.1).

## 2. Count and sweep evidence (step 2)

- SOURCES rows: base `4a079f6a` = 171 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`); tip = 171; max id S311 at tip. Net new rows: 0, matching the report.
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0; `tameshi ok`; warnings W01 (S101) and W04 ×18 (duplicate URLs) retained, as the lesson states.

## 3. Per-claim re-check (step 2)

Verification mode is stated per item: **re-executed** (I or a non-author seat ran it in a throwaway clone at the cited revision and compared output bytes) or **evidence-verified** (committed bytes compared, not re-run).

### 3.1 R87-C1 — operability (capability acquisition) — KILLED

Reported: frozen counter real `passed=8/8`; controls 0/8, 1/8, 0/8, 0/8, 0/8, 0/8, 0/8; kill by `cf-c` 8/8 and `cf-d` 8/8 (and `cf-oid` 8/8 per the critic).

- Real instrument at freeze `1d5102a1`, fresh empty work dir → `C1_R87 rev=1d5102a1788667f45c3163c6251ae520d5e62654 passed=8/8 C1_R87_PASS=true`, exit 0. **Re-executed** (seat, scratch clone).
- Frozen `measure.py` untouched after freeze: `git diff 1d5102a1 d919711 -- .ufo/evidence/round-87/measure.py` empty; last toucher `a3b4f75d`. **Re-executed** diff.
- Pre-freeze controls `pre-freeze/c1/` at `a3b4f75d`: real `8/8`; att3b 0/8; cn1-oracle 1/8; fingerprint, sequence, pinned-hash, always-accept, r85-forgery 0/8; all `.err` 0 bytes. **Evidence-verified** against committed bytes (seat re-run agrees).
- Kill `cf-c` (population from fixture worktree): source extracted from committed `T87E1.md` fence → sha256 `a1f419b0…f59c` matches the table exactly; re-run → `passed=8/8 C1_R87_PASS=true`. **Re-executed.**
- Kill `cf-d` (committed-diff oracle): extracted sha256 `1be5a000…bcfb` matches; re-run → `passed=8/8`. **Re-executed.**
- `cf-a` 8/8 (correct, not a kill), `cf-b` 7/8, `cf-e` 7/8: values present in committed `T87E1.md` tables; **sources not committed**, so **not re-executable** from committed bytes. Evidence-verified as narrative only.
- `cf-oid` 8/8 and the A2 discrimination (`state=different` real vs `state=carried` cf-oid): recorded in committed `T87C1.md`; **source not committed**, run lived in a `/fast/scratch` directory since removed. Evidence-verified as narrative only.

Ruling: the kill stands on `cf-c` and `cf-d`, which reproduce from committed bytes. Claim not verified → not admitted. Grade `unchanged` (no score moved, no capability row, no harm). See routed defect R-2 for the uncommitted counterfeit sources.

### 3.2 R87-C2 — calibration (lowest scored axis) — KILLED

Reported: v1 on overreach bytes `CAP_CENSUS: rows=30 bound=30 unbound=0`, exit 0; v2 on the same bytes `rows=30 bound=0 unbound=30`, exit 1; v2 real `rows=30 bound=30`, exit 0; kill probe `bound=30`; causal control `bound=29`.

- v2 on overreach bytes at `38c83698`, manifest `r86-cited-tree-manifest-v2schema.json` → `CAP_CENSUS_V2: rows=30 bound=0 unbound=30 mismatches=0`, exit 1; full 31-line output byte-identical to `pre-freeze/c2/v2-overreach.txt`. **Re-executed.**
- v2 real population at `ccd6ac26`, manifest `tools/capability-census-v2.json` → `rows=30 bound=30 unbound=0 mismatches=0`, exit 0; byte-identical to `landing/cap-census-v2-real.txt`. **Re-executed.**
- Census v2 selftest → `CAPABILITY_CENSUS_V2_SELFTEST: 15/15 pass`, exit 0, reproduced at tip and at freeze. **Re-executed.**
- **Item-1 attribution mismatch (the one discrepancy).** The report names `r86-cited-tree-manifest-v2schema.json` for the v1 before-state. v1 refuses that manifest: `capability-census: setup refusal manifest-schema:'tameshi-capability-census-v2'`, exit 2. The committed `pre-freeze/c2/v1-overreach-before.txt` (`CAP_CENSUS: rows=30 bound=30 unbound=0 mismatches=0`, exit 0) reproduces byte-for-byte only with the v1-schema sibling `.ufo/evidence/round-87/overreach/r86-cited-tree-manifest.json` (rows identical; only the schema tag differs). The before value and bytes are real; the cited command is misattributed. **Re-executed**, defect routed (R-1); status-neutral, not harm.
- Kill probe: `overreach-probe.json` (row 30 relabelled `historical`, pinned to `tools/selfstate-freshness.json@d10a9c66d618`) at scratch commit on `1d5102a1` → row 30 `bound=yes reason=pin:tools/selfstate-freshness.json@d10a9c66d618`, `bound=30`, exit 0; byte-identical to `kill-c2/probe-prose-absorbed.txt`. **Re-executed.**
- Causal control: remove only that path from SCORECARD.md post-table prose line → row 30 `bound=no reason=pin-not-cited`, `bound=29 unbound=1`, exit 1; byte-identical to `kill-c2/control-prose-path-removed.txt`. **Re-executed.**
- Kill-input integrity: `sha256sum -c .ufo/evidence/round-87/kill-c2/sha256s.txt` (lane-root paths) → all three `OK`. **Evidence-verified** by me.

Ruling: the kill reproduces and is causally isolated. Claim not verified → not admitted. Grade `unchanged` (scores depth 10, calibration 8, freshness 9 unchanged).

### 3.3 Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | unchanged | R87-C1 killed; no capability row entered; no score change |
| calibration | unchanged | R87-C2 killed; scores unchanged; no tool modified |
| depth | unchanged | not claimed; score 10 unchanged |
| freshness | unchanged | not claimed; score 9 unchanged |
| coverage | unchanged | not claimed; no PROVINCE surface move |
| adjacency | unchanged | not claimed; connector overlaps reported, nothing absorbed |

No axis is harmed. No axis is `improved`. No claim verified, so `admitted = false`.

## 4. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-87.md` `## Gate`. Re-opened sources: snapshots committed at `.ufo/evidence/round-87/sources/` (sha256 checked) and the live pages.

| # | item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|---|
| 1 | S289 git-cat-file (admit as cited ground for C1 expected rows) | admit | snapshot `s289-cat-file.html` sha256 `91180e9f…d8be7` (79360 B, matches Gate); live `https://git-scm.com/docs/git-cat-file` | **agree** | Quote "Output the contents or other properties such as size, type or delta information of one or more objects." (18 words, ≤25) is the DESCRIPTION of the exact command whose blob reads underlie C1's rows. Present at snapshot line 2205 and in the live page. |
| 2 | S299 Python shutil (admit as cited ground for trusted-git `shutil.which`) | admit | snapshot `s299-shutil.html` sha256 `28dd43b2…88b18` (120949 B, matches); live `https://docs.python.org/3/library/shutil.html` | **agree** | Quote "Return the path to an executable which would be run if the given cmd was called." (16 words) sits under the `shutil.which` signature (snapshot line 667; anchor `id="shutil.which"` line 665). Present in the live page. |
| 3 | Candidate 4: calibration on round-86 LOG quotes (refuse) | reject | `tools/quoted-line-exists.py --doc HEAD:LOG.md --doc HEAD:corpus/lessons/round-86.md` | **agree** | Output: `LOG.md quotes=235 backed=219 missing=16`; `round-86.md quotes=7 backed=5 missing=2` (`resolved=0/2`, `rows=len(rows)`) — exactly the lesson's figures. The 16 are append-only history that cannot be honestly zeroed; a 2-quote claim is bookkeeping. Naming it as open debt is the right call. |
| 4 | Candidate 3: considerthese ideas 1,2,3,5 (refuse, already implemented) / idea 4 (refuse, out of scope) | reject | `tools/quoted-line-exists.py`, `arm-liveness.py`, `rekey-cost.py`, `pointer-recheck.py` present at tip | **agree** | All four named tools are committed, so admitting them would re-credit existing capability. Idea 4 serves no frozen axis this round. |
| 5 | SOURCES row re-open (≥1 newly written row) | no new row written (171→171) | nearest: S289 and S299 `used-by` edits (touched, not new); both re-opened in §4.1–4.2 | **agree** (documented limit) | The round wrote no new row, so the requested "newly written" re-open has no target. The two touched rows were re-opened instead; their `used-by` now lists `corpus/lessons/round-87.md`, and the round-86 correction is a pure appended bullet (S305 header date `Thu, 05 Nov 2026 00:45:18 GMT`; prior note untouched). |

No disagreements. No quote is absent from either its snapshot or the live page.

Source-quote word counts verified against the ≤25-word rule: S289 18 words; S299 16 words.

## 5. Trend verdicts (with evidence)

- **expansion: unchanged.** No admitted `knowledge/` entry; no new SOURCES row (171→171); no capability row. Evidence: §2.
- **quality: unchanged.** No admitted entry was re-verified, superseded or found stale. QUALITY criteria 132–133 were added, each citing lesson M6/M7; they are discernment work, not a quality move on an entry.
- **discernment: unchanged.** The four sampled gate decisions agree with the outside check on both admits and rejects, which by itself meets the `improved` condition. I grade `unchanged` because the same failure as round 86 recurred: the freeze gate passed two claims that the wave then killed (M6 counterfeit classes, M7 prose absorption), and the reviewer finding that was the kill (M7) was graded `note`. The lesson's own successor (criteria 132–133, M7 arm) is not yet landed, so the miss is not yet converted into a verified improvement. The operator may rule `harmed` on the M7 grading miss.

## 6. Routed defects (lane must fix in round 88; status-neutral)

- **R-1 (accuracy, C2 before-state).** The v1 before-state command must name `.ufo/evidence/round-87/overreach/r86-cited-tree-manifest.json` (v1 schema), not `…-v2schema.json`. Command output and bytes are correct; only the cited manifest is wrong. Fix in the round-88 report and the lesson.
- **R-2 (provenance).** Commit the counterfeit sources `cf-a`, `cf-b`, `cf-e` (T87E1) and `cf-oid` (T87C1) as files, with their run outputs, so their 8/8 and 7/8 values are re-executable from committed bytes. Until then those values are narrative only. The `cf-c`/`cf-d` kills are unaffected.
- **R-3 (fix not shown able to fail).** Mistakes M6, M8 and M9 name fixes routed to round 88; none lands here, so none counts as a shown-able-to-fail fix this round. M1, M2 and M7 have committed red evidence and count.
- **R-4 (open debt, carried).** 16 unbacked LOG counter quotes (append-only history) and 2 in `corpus/lessons/round-86.md`; retained instruments stay unregistered, and the new counter and census v2 are also unregistered.
- **R-5 (note for operator, not a lane defect).** Gate standard (PROTOCOL §Gate standard): the integrator verifies committed gate evidence and does not execute a sibling's gate. This closure pass dispatched non-author seats that re-ran `measure.py` and census v2 in throwaway clones, a deviation from that rule. The grades above rest on committed-evidence comparison; the re-runs are corroboration only.

## 7. Verification mode summary

- **Re-executed:** C1 real instrument at `1d5102a1`; `cf-c` and `cf-d` kills from committed sources; C2 v1 and v2 before/after census at `38c83698` and `ccd6ac26`; census v2 selftest; kill probe and causal control; SOURCES census validate; `quoted-line-exists` figures; S289/S299 snapshot and live quote checks.
- **Evidence-verified only:** pre-freeze control values; `cf-a`, `cf-b`, `cf-e`, `cf-oid` (sources not committed); kill-input sha256s (`sha256s.txt`).

Verdict on the round: honest stop. Both claims killed by their own rules; no axis harmed; no claim admitted.
