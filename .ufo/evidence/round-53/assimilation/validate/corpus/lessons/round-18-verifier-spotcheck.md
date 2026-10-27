author: hyaku closure (non-author integrator, @m_opus)

# Round 18 — non-author verifier spot-check (tameshi)

**Outcome: status `ok`, admitted `true`.** Both declared claims verify at
`4b7c6823a462f5ea2eafcb262275300a545f3ed7`; no owned axis is harmed. This admits
the bounded depth and operability moves, not a claim that every guard is
comprehensively hardened, that the 18 named survivors are closed, or that
promotion is earned. I grade **expansion improved, quality improved (bounded),
discernment improved**, with five routed defects named in §5.

This is an independent closure, not lane authorship. Baseline:
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. Report:
`.ufo/reports/round-18/tameshi.md`, fleet commit
`a85e4d87f48c5f2f6bb885f2e09176e8f5fc9756`. I executed **no lane-owned gate,
selftest, monitor, or measurement tool**. Counts below were reconstructed from
revision-pinned Git blobs, committed receipts, and committed files; gate
verdicts and selftest tallies were evidence-verified, never re-executed. The
one command I ran outside plain reads is the census the closure contract
requires (`scripts/sources-census.sh validate`). Network was used only to
re-open external source quotes (§4).

Driver digest copied from the mutable watchdog log:
- `2026-10-20T16:23:30-03:00 launch tameshi round=18 pgid=1848077 driver=hyaku-inline attempt=1`
- `2026-10-20T19:03:31-03:00 complete tameshi round=18; hyaku-inline attempt=1`
- `2026-10-21T00:39:06-03:00 complete tameshi round=18; hyaku-inline attempt=1`

The second `complete` line is a driver re-completion (same attempt, no second
report commit); the report landed at 18:50:39, before the first complete line.
No other tameshi mission was open.

## 1. Step-1 conformance

`L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
`F=/home/vgpnk/Projects/shokunin`.

| Check | Command / source | Observed |
|---|---|---|
| Report landed by the lane, last | `git -C "$F" log --format='%an <%ae> %H %cI' -- .ufo/reports/round-18/tameshi.md` | `tameshi-shokunin <tameshi@shokunin.local> a85e4d87… 2026-10-20T18:50:39-03:00`; final lane commit `4b7c682` is 18:49:16. Pass. |
| Real report, not a marker | Report §§Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, SHONEN | Two checkable claims, 13 cited hashes, a LOG entry, four `[~]` box lines each with a pointer. Pass. |
| Cited commits exist and are ancestors | `git -C "$L" cat-file -e HASH^{commit}` + `git -C "$L" merge-base --is-ancestor HASH refs/heads/master` for all 13 hashes in the report table | All 13 pass: `93d22aa`, `aee4f36`, `58e5d53`, `e08271a`, `01d586d`, `9ee1c80`, `4acdeac`, `921ef80`, `5923d89`, `a9c94c5`, `a134a09`, `a85f710`, `4b7c682`. Ancestry was tested against `refs/heads/master`, never detached HEAD. |
| Lane identities | `git -C "$L" log --format='%h %an <%ae> %cI' 183f87b..4b7c682` | 13 commits, all `tameshi-shokunin <tameshi@shokunin.local>`. |
| Pushed, no round leftovers | `scripts/hyaku/jj-lane.sh state "$L"`; `git -C "$L" status --porcelain`; `git -C "$L" ls-remote origin refs/heads/master` | `local=remote=4b7c6823… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote master `4b7c6823a462f5ea2eafcb262275300a545f3ed7`. |
| Prompt durability | `git -C "$F" log --format='%an <%ae> %H %cI' -- .ufo/prompts/tameshi-round-18.md` | `tameshi-shokunin ef397f9ee75a… 2026-10-20T16:23:28-03:00`, two seconds before the launch line. |
| Prompt fidelity | `diff` of the two rendered prompts (template placeholders substituted) | Prompt §§1–5 byte-identical to `templates/round-prompt.md`; only the rendered working-dir line differs (`<tameshi-repo>` → `tameshi-shokunin`, the correct path); §6 hyaku addendum present with the L2 floor, routing sentence and write scope. |
| L2 route map vs MISSION | `MISSION.md` §L2 concurrency; prompt §3/§6 | MISSION defines role buckets only (no model pins); the prompt defers to the host route table and carries session overrides as host mechanics. No contradiction. |
| Wave accounting | `spec1.json` / `spec2.json` task counts; role census from `w1|w2/swarm-registry.json` | w1 73 = 20 scout, 18 scribe, 10 executor, 10 reviewer, 5 critic, 5 connector, 3 revenger, 2 sentinel; w2 93 = 61 reviewer, 11 scout, 6 executor, 6 critic, 4 mutation-tester, 2 sentinel, 2 connector, 1 simplifier; total 166. Matches the report exactly. |
| SHONEN heading / boxes | Report `## SHONEN` | Heading present, one line per box, four `[~]` with pointers, no `[x]`. |
| SHONEN canonical form | Compare `SHONEN.md` against the `PROTOCOL.md` seed modulo `<name>`; `cat -A` | Seed block identical; marks confined to the box plus one indented evidence line per box. Pass. |

Attribution of the report commit is to the lane identity, not an operator sweep.
No uncommitted lane round work was found before or after the spot-check.

## 2. Claims — re-derived, not accepted

### C1 — depth, recorded mutation cases 7 → 8 (**improved**)

The lane's declared counting rule (SCORECARD command D, `SCORECARD.md:73`) run
by me over pinned blobs:

```sh
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

- `183f87b899e6cae46be98d251cbc87fb5118f6ca` → `recorded_cases=7 depth_score=7`
- `4b7c6823a462f5ea2eafcb262275300a545f3ed7` → `recorded_cases=8 depth_score=8`

Supporting facts, independently re-derived from committed bytes:

- Target identity: `git -C kumitate-shokunin show 0acb7752…:scripts/sources-check.mjs | sha256sum` → `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`,
  equal to the spec pin, the predictions pin, the sweep target and the
  `REGRESSION_PIN` in `final/regression.stdout`.
- Pre-registration order: `93d22aa` is dated 2026-10-20T16:22:36-03:00; the
  sweep's own `MUTATE_DATE` is `2026-10-20T19:41:29Z` (= 16:41:29-03:00), so
  the spec and predictions preceded every mutant run.
- Sweep result: `grep -c '^DEFECT .*: KILLED'` → 5, `grep -c '^DEFECT .*: SURVIVED'`
  → 5, `PREDICTION_MATCH: 10/10`, `MEASURED_KILL_RATE: 5/10 = 50%` in
  `.ufo/evidence/round-18/sources-check/sweep/sweep.txt`.
- Determinism: `control/repeat-hashes.json` records 8 runs, all exit 0, one
  distinct stdout sha256 (`e0880a5a…465e5f`), 6,274 bytes each.
- Regression embedding: `final/regression.stdout` ends
  `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`,
  with `REGRESSION_TABLE js-sources-check: match=10/10 … flips=0`.
- Ledger row: `corpus/knowledge/fleet-kill-rate-ledger.md:432` carries the
  eight-leg table entry citing rev `0acb775`, sha256 `6a293a72…258f`, runner
  `fb6d86d5…` and the same 19:41:29Z run.

### C2 — operability, eleven named routed probes open → closed (**improved, bounded**)

Evidence-verified (receipts bound to the measured revision), plus my own counts
over the committed receipts:

- `grep -c '^PROBE P[0-9]* open' .ufo/evidence/round-18/c2-probes-v2-183f87b.txt`
  → **11**; the receipt closes with `DEFECT_PROBES: open=11 closed=0 total=11`.
- `grep -c '^PROBE P[0-9]* closed' .ufo/evidence/round-18/final/probes.stdout`
  → **11**, `open` → **0**; `DEFECT_PROBES: open=0 closed=11 total=11`.
- `grep -o 'pristine_exit=[0-9]* mutant_exit=[0-9]*' … | sort | uniq -c` →
  `7 pristine_exit=0 mutant_exit=1` (P01–P07), the killing guard-removal set.
- The final receipt is bound to the final tool revision:
  `sha256sum final/probes.stdout` → `d37c99e3…4eb8cf0`, identical to
  `final/checks.json` `probes.stdout_sha256` whose argv is
  `defect-probes.py --rev 921ef8077440f90d092aab4b9fdc750a45de1224`, exit 0.
- v1 is retained, not laundered: `c2-probes-e08271a.txt` ends
  `DEFECT_PROBES: could-not-evaluate (3 probe error(s))`, exit=2; the v2 rerun
  is on both revisions (`c2-probes-v2-*.txt`).
- Negative and positive disposition receipts: `final/before.stdout` → exit 1,
  `producer_before` failed with `expected_contains_missing`;
  `final/disposition.stdout` → exit 0, `"status": "clean"`, 11 effective,
  1 superseded, 0 failed.
- Selftest tallies (evidence-verified): disposition `SELFTEST: PASS (63/63)`;
  registry `SELFTEST: PASS (48 cases)`; bash-witness `WITNESS_SELFTEST: 43/43 pass`
  (`final/bash-witness.stdout`); trace `SELFTEST: 30/30`; measure 98/98;
  assemble 80/80.
- Registry no-harm: `final/registry-branch-aligned.stdout` → `"held": 31`,
  `"superseded": 4`, `"total": 31`, `"exit": 0`, `rev=5923d89…`.
- The bound is preserved in the lane's own EG-3: P08 binds `master`, P11
  exports two names, P09 tries two literals; 18 mutation survivors remain
  round-19 debt. The claim is the eleven named probes, not comprehensive
  hardening.

### No-harm monitor (calibration 8)

- `git diff 183f87b 4b7c682 -- SCORECARD.md` → 43 insertions, 0 deletions; the
  round-18 block adds depth 7→8 and records calibration as an unchanged
  score-8 monitor, not a third claim.
- Strict cold-read receipt, evidence-verified at its declared revision
  `a85f7107c4167cd9968248722256fcaf617fc30c`:
  `final/measure-final-60.json` → `sections_covered=60`, `sections_total=60`,
  `box3_full_page=true`, `calibration_restraint_score=8`,
  `overrides_used=false`, `reasons={"credited": 60}`. The intermediate
  `final/measure-final.json` at `a134a09` is retained at 59/60 with
  `box3_full_page=false` — disclosed, not counted.
- `SHONEN.md` still carries four `[~]` and zero `[x]`; no promotion is
  pre-claimed.

## 3. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1: 7→8 at command D on both pinned revisions; independent target-sha pin. |
| operability | improved (bounded) | C2: 11 open→0 open/11 closed with revision-bound receipts; no scalar is claimed. |
| calibration | unchanged | Score-8 monitor, 60/60 strict receipt at `a85f710`, four `[~]`, no `[x]`, EG-3 bounds stated. |
| coverage | unchanged | No new provincial surface admitted beyond the eighth case; no F1–F10 ground moved. |
| freshness | unchanged | No successor sweep claimed; kumitate gates read-only. |
| adjacency | unchanged | Owner recommendations routed to kumitate, no sibling change made; SiblingImpact cancelled and disclosed. |

No axis is harmed. Append-only files show zero deleted lines: `LOG.md` +62/−0,
`corpus/QUALITY.md` +163/−0, `corpus/README.md` +25/−0,
`corpus/lessons/round-17.md` +10/−0. `PROVINCE.md` +12/−0. `SHONEN.md` is the
disclosed canonical regeneration (2 added, 3 removed lines) with the removed
prose preserved in the LOG entry. `corpus/SOURCES.md` has 25 added and 5
deleted lines; all five deletions are the documented cells (S008 status+used-by;
S001/S052/S056/S057 used-by), and no other row was rewritten.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ exit 0, `Final census: rows=76 tiers=A67,B7,C2 status=mined48,queued23,rejected5; malformed=0`.
The six W04 warnings are the two pre-existing S047/S048 duplicate URLs plus the
four S075–S078 superseding rows; the report states exactly this. My own count of
the base blob reproduces the report's start histogram (rows 62, A54 B6 C2,
mined 35, queued 24, rejected 3); the working-tree count reproduces the end
histogram (rows 76, A67 B7 C2, mined 48, queued 23, rejected 5).

## 4. Discernment spot-check — gate decisions re-opened

Sampled from `corpus/lessons/round-18.md` `## Gate` (admit + reject) and from
newly written `corpus/SOURCES.md` rows.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| G2 — case 8 = kumitate `sources-check.mjs` | admit | `git -C kumitate-shokunin show 0acb7752…:scripts/sources-check.mjs \| sha256sum`; `93d22aa` commit time vs sweep `MUTATE_DATE`; sweep verdict counts | **agree** | Target sha256 equals the pre-registration pin, the sweep target and `REGRESSION_PIN`; spec/predictions preceded the run by 19 minutes; 5 KILLED / 5 SURVIVED with PREDICTION_MATCH 10/10 is exactly the admitted basis. |
| G1 — case 8 = kake `scripts/corpus-contract.mjs` | reject | `PROVINCE.md` Owns list; `kake-shokunin/scripts/corpus-contract.mjs`; `corpus/knowledge/service-optin-protocol.md` | **agree** | `kake` is absent from Owns (kumitate/kagi/kaidoku/game lanes only), the kake surface exists but is not a recorded leg, and the service opt-in note does require an owner request. Rejecting it kept the case on a declared primary surface. |
| S069 — setsid(2) quote (new row) | mined | https://man7.org/linux/man-pages/man2/setsid.2.html and `man 2 setsid` | **agree** | Page text: "The calling process will be the only process in the new process group and in the new session." (19 words, §DESCRIPTION ¶2); local man page matches. |
| S075 — strace(1) quote (new row) | mined | https://man7.org/linux/man-pages/man1/strace.1.html | **agree** | Page text: "Traces only the specified set of system calls." (§Filtering, `-e trace=syscall_set`); the correction of S060's `%file` anchor holds. |
| S078 — open(2) quote (new row) | mined | https://man7.org/linux/man-pages/man2/open.2.html | **agree** | Page text: "These request opening the file read-only, write-only, or read/write, respectively." (§DESCRIPTION access modes); the O_TRUNC overstatement correction is grounded. |
| S066 — RFC 8259 quote (new row) | mined | https://www.rfc-editor.org/rfc/rfc8259.txt §6 | **agree** | Text: "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted." |

The sampled admits and rejects agree with the gate. The disagreement I record
is not with a decision but with a falsifier's arithmetic: see §5c.

## 5. Routed defects (lane to fix next round)

1. **Stale metadata at the landed tip.** `corpus/knowledge/guard-kill-closure.md:2`
   still reads "Landed-tip results: PENDING (filled by L1 after landing)" at
   `4b7c682`; its own EG-1 erratum says the results are measured. The knowledge
   entry's `verified-at:` line is the metadata contract, so an appended
   correction naming that line is owed.
2. **Stale source status in an admitted entry.**
   `corpus/knowledge/mutation-case-kumitate-sources-check.md:1` still calls S008
   "queued … not yet a mined row", while `corpus/SOURCES.md` S008 is `mined`
   with this entry as used-by and ER8-1 states the change. Sweep the metadata
   mention or append a correction naming it.
3. **Falsifier's own arithmetic.** `corpus/lessons/round-18.md:79` states
   "deletions = the four allowed used-by cells only"; the committed diff has
   **5** deleted lines (S001, S008, S052, S056, S057), as the Gate paragraph
   itself lists. State five, or name S008's status+used-by line explicitly.
4. **Mis-invoked selftest receipt.** `final/checks.json` records
   `bash-witness-selftest` argv exit 64 with an empty stdout (stderr:
   `the following arguments are required: mode`), while the real tally is
   `WITNESS_SELFTEST: 43/43 pass` in `final/bash-witness.stdout`. Do not leave
   a failed invocation as the selftest row of the final receipt bundle.
5. **Unbacked final-revision claim.** The report says the no-override count at
   `4b7c682` returned 60/60,8, but the committed 60/60 receipt is at `a85f710`;
   no receipt names `4b7c682`. Land one at the cited revision or drop the
   sentence.

None of these changes a claim verdict: the claims rest on receipts that do
exist at their declared revisions, and the defects are metadata/receipt hygiene
plus one falsifier statement.

## 6. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | Two new admitted knowledge notes on uncovered ground (`guard-kill-closure.md`, `mutation-case-kumitate-sources-check.md`), each citing mined `S###` rows (S001/S008; S065–S074 plus correction rows S077/S078); README coverage rows added; census 62→76 rows (13 tier A + 1 tier B), mined 35→48. |
| quality | improved (bounded) | Weaker anchors superseded by stronger rows with re-opened quotes (S068→S077, S072→S078), stale round-16/17 readings dated in README, QUALITY 29–36 appended with wave-2 corrections, strict 60/60 receipt at `a85f710` with the 59/60 intermediate retained. Bounded by the §5 metadata/receipt defects; no admitted entry's substantive claim failed re-check. |
| discernment | improved | Sampled gate admits and rejects agree on re-open (§4); rejects are recorded with flips (S067, S071) and a first staged suite string was rejected against pre-registration; QUALITY criteria 29–36 are lesson-backed. The falsifier arithmetic defect (§5c) is routed, not excused. |

## 7. Scope statement

No promotion, mint, or lane-authored file was touched by this closure. No tool
was installed or updated. `SHONEN.md` boxes remain lane assertions (`[~]`); all
four carry resolvable pointers, so a non-author promotion review could be
executed if the operator calls it, but promotion is operator-owned and is not
claimed here. This spot-check is the only artifact written by the closure, and
it was committed through the jj lane helper under the protocol identity.
