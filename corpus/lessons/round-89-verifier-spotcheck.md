author: hyaku closure (non-author integrator, @m_zfl)

# Round 89 — verifier spot-check (non-author)

Subject: tameshi round 89. Lane tip `20e78a5566ffe70a7dde1ff1b2672b334f958f68`, base `61990f3d8cd99932bfb0575e1c292e03d310b436`.
Report: `.ufo/reports/round-89/tameshi.md` (fleet commit `7a2bb16875d453c50219ef34fc2620c23cc45262`, author `tameshi-shokunin`, 2026-11-06T18:11:41-03:00).
Gate under review: `corpus/lessons/round-89.md` `## Gate`. The lane did not write this file, and this file changes no lane-authored file.

Dispatch digest, copied from `.ufo/watchdog.log` at closure (the log is mutable):
- `2026-11-06T16:42:47-03:00 launch tameshi round=89 pgid=2042993 driver=hyaku-inline attempt=1`
- `2026-11-06T18:12:21-03:00 complete tameshi round=89; hyaku-inline attempt=1`

## 1. Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H %cI' -- .ufo/reports/round-89/tameshi.md` (fleet root) | `tameshi-shokunin tameshi@shokunin.local 7a2bb168… 2026-11-06T18:11:41-03:00` | ok; filed after the last cited lane commit (18:10:50) and before the driver's completion line (18:12:21) |
| `SHONEN` heading, one line per box | read of the report §SHONEN | 4 lines, all `[~]`, each with a pointer | ok |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for `61990f3d`, `a65e11c0`, `48383295`, `8876cca5`, `ff7a4b06`, `20e78a55` | `commit` ×6, `anc=yes` ×6 | ok |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain` | `branch=master local=remote=20e78a55… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `20e78a55…` | ok |
| Round commits by the lane identity | `git log --format='%H %an <%ae>' 61990f3d..20e78a55` | 5 commits, all `tameshi-shokunin <tameshi@shokunin.local>` | ok |
| Prompt carries the template contract | `diff` of lines 1–140 of `templates/round-prompt.md` (kimi-shokunin) vs `.ufo/prompts/tameshi-round-89.md` | only placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §§1–5 verbatim; hyaku addendum §6 onward | ok. The prompt file was committed in the fleet repo by `tameshi-shokunin` (`ae0313bc`, "dispatch evidence (hyaku inline attempt 1)") — noted, status-neutral |

Marker test: the report carries landed commits and committed evidence; it is a real report. Status **ok**.

## 2. Claim R89-C1 (operability, capability acquisition): `tools/ledger-witness.py`

### 2.1 What I re-measured myself (committed bytes only)

| Quantity | Command | 61990f3d | ff7a4b06 | 20e78a55 | Reported |
|---|---|---|---|---|---|
| witness present | `git cat-file -e <rev>:tools/ledger-witness.py` | absent | present | present | absent → present — agrees |
| capability row | `git show <rev>:SCORECARD.md \| grep -c '^\| ledger witness \|'` | 0 | 1 | 1 | 0 → 1 — agrees (row annotated **not admitted** at the tip) |
| SOURCES rows | `git show <rev>:corpus/SOURCES.md \| grep -c '^\| S[0-9]'` | 172 | 174 | 175 | 172 → 175 — agrees |
| runner untouched | `git diff --stat 61990f3d 20e78a55 -- tools/mutate-and-run.sh` | — | — | empty | "unchanged" — agrees |
| round is pure addition | `git diff --numstat 61990f3d 20e78a55 \| awk '$2!=0'` | — | — | only the binary `s315-mkcheck.pdf` (`-`/`-`) | no lane file modified or deleted |

### 2.2 Gate evidence I verified (lane-owned counter and witness; not executed by me)

- No-work control: `.ufo/evidence/round-89/pre-freeze/nowork-base.out` — `witness=absent selftest=0/0 real=SETUP forgeries_refused=0/0 capability_row=0 C1_R89_PASS=false`, `exit=1`, revision `61990f3d`.
- Self-test: `pre-freeze/selftest.out` — `LEDGER_WITNESS_SELFTEST: 21/21 pass`, `exit=0`; `grep -c '^SELFTEST_ARM .* ok$'` = 21 (the tally matches the arm lines).
- Landing counter: `landing/measure-ff7a4b06.out` — `rev=ff7a4b06… witness=present selftest=21/21 real=PASS(legs=11) honest_accepted=2/2 forgeries_refused=12/12 capability_row=1 C1_R89_PASS=true`, `exit=0`. Revision measured: the landing, not the final tip; the tip adds only records (2.1 shows the conjuncts I can measure are identical at both).
- Kill evidence: `.ufo/waves/round-89/w1/T89E2.md` line 149 `VERDICT: accepted:hardlink,dirswap,symlink`; `T89E2-hardlink.witness.out` ends `LEDGER_WITNESS: legs=11 witnessed=11 findings=0 checks=- PASS`; the L1 reproduction `landing/t89e2-reproduced-by-l1.txt` shows all three `exit=0 … PASS`.
- Counter cheat: `w1/T89C1-counterfeit-witness.py` (43 non-empty lines; its only `subprocess` mention is the docstring "calls no subprocess") reaches `C1_R89_PASS=true` in `w1/T89C1-measure.out`.
- Wave completeness: `.ufo/waves/round-89/r89-w1-results.json` — `seats=12 results=12`.

### 2.3 Kill-rule ruling

Frozen kill rule (b) (`plans/round-89.plan.md:86-92`): killed if any committed runner variant that does not perform the ledger's real work is accepted by the landed witness, unless it works only through a declared limit. The three T89E2 runners exec a stub at every audited path and install the spec-exact bytes through an alias afterwards; aliasing is not among L1–L4 as frozen, and the witness prints `PASS`. **I agree: R89-C1 is killed by its own rule.** Independently, T89C1 shows the counter itself is cheat-passable (QUALITY 138), so the predicate could not have proved the claim either. The lane did not narrow the predicate after data: honest stop.

### 2.4 Owned-axis no-harm

`git diff 61990f3d 20e78a55 -- SCORECARD.md`: additions only (the `ledger witness` capability row and the `## Round 89` section; depth 10 / calibration 8 / freshness 9 unchanged). Standing sweeps at the landing, committed receipts: `selfstate-ff7a4b06.txt` `SELFSTATE: rows=26 match=24 stale=2 unexpected=0` exit 0 (identical to the round-88 receipt, so no new staleness); `pins-ff7a4b06.txt` `rows=26 settled=26 stale=0`; `registry-figure.txt` `rows=9 match=9`; `pointer-recheck.txt` `rows=12 met=12`. No harm found.

### 2.5 Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | unprovable | the declared claim is killed by its frozen rule (b); the capability is not demonstrated; nothing regressed (runner unchanged) |
| depth | unchanged | score 10 unchanged; no lane entry modified |
| calibration | unchanged | score 8 unchanged; QUALITY 136–138 are criteria, not a scored move |
| freshness | unchanged | score 9 unchanged; no `verified-at` re-check |
| coverage | unchanged | no ledger leg added |
| adjacency | unchanged | no adjacent ground taken |

Re-measured: 2.1 (presence, row count, source count, runner diff, addition-only). Evidence-verified, not executed: the witness self-test, the counter at the landing, the T89E2/T89C1 wave runs.

## 3. Discernment spot-check (`corpus/lessons/round-89.md` `## Gate`)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S313 execve(2) | admit (A, mined) | `curl https://man7.org/linux/man-pages/man2/execve.2.html` at closure: 43619 B, sha256 `ea744b04…d309` (identical to the lane's snapshot) | agree | both quotes present: "many attributes of the calling process remain unchanged (in particular, its PID)" at lines 463–464 (wrapped), "By default, file descriptors remain open across an" at line 254; both bear on the witness's exit-of-the-exec'd-pid and fd-write reasoning |
| S315 Licker & Rice, ICSE 2019 | admit as `queued` | `curl` of the Cambridge Apollo bitstream: 286638 B, sha256 `ceff92a9…2a4f` (identical); `pdftotext -layout` lines 164–168 | agree | "dependency graphs / defined by users of build tools cannot be trusted" sits in the left column at lines 165–167 (11 words); the concession "some edges might be missing from the re-covered graph" at line 332; `queued` with no citing entry is the right status for a successor grounding |
| Claim candidate: another print-binding counter | reject | `.ufo/evidence/round-89/landing/m1-r88-check-vs-stub-lines.txt` | agree | the round-88 `executed-set-check.py` prints `EXECUTED_SET: declared=11 executed_pass=11 … ok`, exit 0, on a runner that executes nothing; binding more printed lines is the same class |
| mkcheck2 (ICSE 2026) and three alternatives | reject | `https://dl.acm.org/doi/10.1145/3744916.3773204` and `/doi/pdf/…` → HTTP 403 (Cloudflare challenge); arXiv API query `mkcheck2` → no entry; `katei-lab/mkcheck2` README carries no paper text | agree with the decision; reason partly unverified | I could not locate a quotable open text either, so "no located quote" holds; "paywalled" I could not confirm (the ACM page is behind a bot challenge, not shown to be a paywall). Wording defect, routed |

SOURCES row check: S313, S314, S315 quotes counted with `grep -o '"[^"]*"' | wc -w` — longest 12 words (S313, S314), S315 11 words; all ≤25. S314's two quotes ("Prints paths associated with file descriptor arguments…", "Prints unabbreviated versions of environment…") each found once in the re-fetched strace(1) page (85238 B, sha256 `eedefecf…02f6`, identical).

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok …/corpus/SOURCES.md`, exit 0; one new warning `W04 S314 duplicate url … strace.1.html across scopes`, expected and declared in the gate row.

## 4. Trend verdicts

- **expansion: unprovable-but-better** — the new entry `corpus/knowledge/kernel-witnessed-ledger.md` is grounded (header trio present; cites mined S313/S314) and honest about the kill (§5 of the entry). But LEARNING's `improved` test requires each new entry to cite its coverage-map row, and `corpus/README.md` is untouched this round (`git diff --stat 61990f3d 20e78a55 -- corpus/README.md` empty; `grep -c kernel-witnessed corpus/README.md` = 0). Better, not provable under the criterion.
- **quality: unchanged** — no held entry re-verified or superseded.
- **discernment: improved** — the spot-check agrees with the gate on both admits and both rejects sampled, and the round's failures (M1, M6, M7) became grounded criteria QUALITY 136–138, each citing `lessons/round-89.md` `## Mistakes` and a committed control.

## 5. Verdict

Status **ok**; **not admitted** — `rejected-honest-stop`. The only claim is killed by its own pre-registered rule; no axis harmed.

## 6. Routed to tameshi round 90 (status-neutral)

1. Add a coverage-map row in `corpus/README.md` for `knowledge/kernel-witnessed-ledger.md` and have the entry cite it (the round-35 index-repair class).
2. Report §Trend says "the kill and nine other mistakes"; the lesson's trend line says "the kill and four other mistakes" (M1–M10 = the kill plus nine). Correct the lesson by an appended note.
3. The mkcheck2 rejection reason says "paywalled"; at closure the ACM page returned a bot challenge (403), not a demonstrated paywall. State "not retrievable at fetch time" or locate the text.
4. `tools/ledger-witness.py` is a retained instrument with no row in `tools/registry.json` and no registry row in `SKILL.md` (Gate standard, Registry) — the lane already carries this under R-4.
5. The lane's own routed items 1–5 (`lessons/round-89.md` § Routed): identity-keyed successor witness (QUALITY 137), independently deriving counter with the counterfeit-instrument control (QUALITY 138), per-branch selftest arms (M10), expectations committed alone first (M8), L3 narrowing, round-88 R-3/R-4 carry.
