# Tameshi round 54 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-10-28
lane_round: 54
lane HEAD verified: `tameshi-shokunin@0263c71ed6ec930603f5e37578ef46e498c96111` (branch `master`, local = remote, ahead=0)
base: `d33053f7552db4bd290c99a36979760f544c41ad`
deciding revision: `c21081008adbb6b6fe4e58a0aeec4831b30e318c`
freeze the deciding receipt names: `077d431e69965fa4673cd006ab64f6fc387f9e15` (5 amendments)
report: `.ufo/reports/round-54/tameshi.md` (fleet `fcb8d8db`, author `tameshi-shokunin <tameshi@shokunin.local>`)
verdict: **admitted** — both claims re-measured true at the deciding revision in a scratch clone; no axis harmed; nine routed record/instrument defects, the gravest (R54.1) a **false positive-control claim** contradicted by its own committed receipt.

This file is a non-author artifact: the two claims below are re-measured, not re-asserted, and every defect is pinned to a committed byte. Nothing in the lane was edited except the three files named under "Closure durability commit" (swept byte-identical) and this file.

---

## Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-54/tameshi.md` (fleet) → `tameshi-shokunin <tameshi@shokunin.local> fcb8d8db…`; author 12:22:33, committer 12:26:14 −03 | pass |
| report lands last | lane tip `0263c71e` authored 12:25:51; report **committed** 12:26:14 → after it. The report's *author* timestamp (12:22:33) precedes the tip it cites (helper-set, same class as r51) | pass (timestamp oddity noted) |
| dispatch evidence | `.ufo/prompts/tameshi-round-54.md` at `3d79eed7` (11:09:11) for attempt 2; `3126452e` (09:59:49) for attempt 1 | pass |
| cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor` for `d33053f7 441c26be 59c38109 99c3bc88 077d431 7fa9a5e 5564954 c2108100 4fe57df 0263c71e` | 10/10 pass |
| lane pushed, nothing ahead | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin` → `local=0263c71 remote=0263c71 ahead=0 behind=0`; `ls-remote origin refs/heads/master` = `0263c71e` | pass |
| uncommitted round work | `git status --porcelain` → 3 untracked (`T54W2Sent03.md`, `c1committed-positive.stdout`, `rejection-attribution.txt`) | **fail** at closure as filed → R54.6; closure swept them (below) |
| SHONEN heading | report `## SHONEN`, 4 × `[~]` with pointers | pass |
| report is real, not a marker | names claims, revisions, waves, receipts, trends | pass (real report) |
| wave band | `w1-registry.json` seats 76 (v2 64–128 ✓), `w2-registry.json` seats 47 (v1 32–64 ✓), total 123 ≤ 128; attack roles 21/76 = 27.6 % (report says 26.3 %), 12/47 = 25.5 % — both ≥ 25 % | pass (share typo → R54.9) |
| wave results handoff | no `w1-results.json` / `w2-results.json` anywhere in the lane or fleet; dispatch markers `w1.ready.dispatched`, `w2.ready.dispatched` present | record gap (noted) |
| census | `scripts/sources-census.sh validate --root … tameshi` → exit **0** (W04 warnings only); rows 136 → 139 (`| S### |` count) | pass |

---

## Per-claim re-check (closure re-measurement, frozen counter bytes, scratch clone)

Clone: `git clone --no-hardlinks …/tameshi-shokunin /…/.scratch/closure-r54/lane`; each run in a fresh empty `--work` (the counters refuse a non-empty one). The counter executed at every revision is the byte set `freeze.json@077d431` pins (I re-derived all ten digests from `077d431` bytes: **10/10 OK, amendments=5**).

### C1 — calibration, cold-read floor (met, re-measured)

```
--rev d33053f7   C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false
--rev 59c38109   C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
--rev c2108100   C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

Both extremes reproduce the committed receipts exactly (`before/c1.stdout`, `after/c1.stdout`), and the disclosed C0 drift (41/23) reproduces at `59c38109`. Structural checks I ran myself, independent of the arms' verdict:

- `git diff --quiet 077d431 c2108100 -- <the 11 frozen paths>` → **identical** (`FROZEN_UNCHANGED=1` is earned).
- ledger `591` entries; exactly `23` bound under `rekey-r54-99c3bc88d704`, all `read_rev=99c3bc88d7045661…`; **0** bound entries pin `LOG.md`, `SCORECARD.md` or `.ufo/evidence/round-21/coldread/ledger.json` (the self-pin the binder now drops).
- **23/23** bound entries' `sha256` equal the section's bytes at `c0` — so Sent03's blind spot (b) is a real instrument weakness that is **not realized** in this ledger.
- **one** bound entry per heading (no duplicate/twin) — Sent03's blind spot (a) is likewise not realized.
- `SKILL.md` is byte-identical at `c0` and at the deciding rev (`848293465bb9…`), so arm 4's "section at rev" equals the section at `c0` **for this round**.
- no-harm stdout: 14 × `NOHARM … ok`, 0 × RED, incl. `NOHARM coldread-floor score=8 credited=64 ok`.

### C2 — operability, one scratch-root exit class (met, re-measured)

```
--rev d33053f7   C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
--rev c2108100   C2_R54: rev=c21081008adb tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
```

The before line matches the committed `before/c2.stdout` and the contract's `before` text (`total=13`), not the `total=14` in `SCORECARD.md:2584` (R54.3). The counter bytes used are `8528ee85…`, i.e. **amendment 4 applied** — the census regex is `mkdir(?:at)?\(`, so the "plain `mkdir(` invisible" defect the wave found is fixed in the bytes that decide; my run's `tmp_mkdirs=0` is therefore a live reading, not a dead regex. I re-read the docs/note/source arms: 7 registry rows carry a `scratch_root` cell naming TMPDIR, the empty arm and `could-not-evaluate`; the note cites S277–S279; the lesson `## Gate` names all three with URL and `2026-10-28`.

**Frozen-vs-amended reading:** every number above is the *amended* instrument (5 amendments, all in `freeze.json` at the deciding freeze commit `077d431e`, all landed before the single deciding invocation). The base row is the amended counter re-run at base — the pre-amendment smoke value is not what decides. All five amendments change discovery/measurement plumbing, none changes a predicate: my own base and deciding runs bracket the claim, and the arm-3 `dirs=[]→['rekey-r54-99c3bc88d704']` differential shows the arm firing.

---

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | **improved** | floor 57/64 → 64/64 credited and monitor 6/57 → 8/64, re-measured by the closure at base and deciding rev |
| operability | **improved** | unusable arm 3/7 → 7/7 exit-2-with-naming; empty and usable arms 7/7; docs 0 → 7, note 0 → 1, sources 0 → 3; `tmp_mkdirs=0` on repaired bytes |
| depth | unchanged | no capability claimed; QUALITY 105 appended, but see R54.1 |
| coverage | unchanged | no frontier row advanced (F6 held), no new surface |
| freshness | unchanged | `NOHARM r45-freshness population=74 fresh=71 score=9 ok` |
| adjacency | unchanged | no cross-domain claim this round |

No axis harmed: no-harm 14 ok / 0 RED; the only `SCORECARD.md`/`SKILL.md`/`QUALITY.md` movements are additive (+61/+56/+10 lines), and the cold-read floor at the deciding rev is 64/64.

---

## Discernment spot-check (LEARNING.md: checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S277 POSIX.1-2024 §8.1 TMPDIR | admit | committed snapshot `.ufo/evidence/round-54/assimilation/S277-posix-env.html` (quote located at byte 26548) | **agree** | quote present verbatim, 24 words (≤25); URL + `2026-10-28` in the lesson Gate; row marked `mined`, `used-by` = the note |
| S278 CPython 3.12.7 `tempfile.py` | admit | snapshot `S278-tempfile.py:165` | **agree** | `if dirname: dirlist.append(dirname)` at the cited lines; an empty value is skipped, so `TMPDIR=""` is unset |
| S279 Python `tempfile` docs | admit | snapshot `S279-tempfile-docs.html` (quote at byte 14158) | **agree** | "The directory named by the TMPDIR environment variable" is first in the documented list; 11 words |
| `merge/tameshi` `delta-debugging-minimization-contract.md` "refused on capacity" | reject | lane `corpus/knowledge/delta-debugging-minimization-contract.md` **is present at base `d33053f7`** (commit `79f44b5`, round 50, source S271); the staged package `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/…` holds the same name | **disagree** | the entry is already adopted in the lane; "refused on capacity" misstates a non-pending item, and the `Planned (round 55)` line proposes re-adopting it. Also "the other 84 staged entries" vs 81 staged `.md` under `merge/tameshi/knowledge` |

Census (also the sourced-claim gate's own check): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit **0**.

---

## Trend verdicts

- **expansion — unchanged.** No frontier row advanced, no capability row: the new rows are knowledge on an operability surface the lane already owns (agrees with the lane).
- **quality — improved.** C2 3/7 → 7/7 re-measured; 25 wave-2 findings adjudicated one by one against bytes and bound `gap-minor` in the ledger rather than claimed clean; QUALITY 105 appended. Counter-signal: that very criterion's falsifier is hit by R54.1.
- **discernment — unchanged (disagreement with the lane's "improved").** For: 25 findings re-derived and routed, arm-3 blind spots disclosed unprompted, the forged-file incident and the mutation survivors named — all of it verified genuine here. Against: a pre-registered positive control is reported as passing when its committed receipt prints `CTL_MISMATCH … expected=true actual=false` / `CONTROLS_B: 2/3`, in four files including a newly landed QUALITY criterion; and the round's own finding counts do not match its committed artifacts (R54.5). Net: no movement over a base that carried the same class of record falsehood (r53 closure, SCORECARD `total=6` vs the counter's `37`).

---

## Routed defects (lane owns the fix; all status-neutral for admission)

**R54.1 — false positive-control claim (gravest).** `.ufo/evidence/round-54/control/controls-b.stdout` (committed, unchanged across all 5 revisions that touch it) prints
`CTL CTL_POS_c1 … c0=99c3bc88d704 credited=60 lost=4 rekeyed=3/7 readers=6/7 … C1_R54_PASS=false`, `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`, `CONTROLS_B: 2/3 as pre-registered`, exit 1. Yet the record asserts the opposite in four places: report `:162` ("proven live by the phase-B positive control"), `SCORECARD.md:2583` ("`CTL_POS_c1 true`"), `corpus/QUALITY.md:1590` ("the round-54 counter's arm prints `rekeyed=7/7` on its positive control … both are committed"), `corpus/lessons/round-54.md:74,101` ("proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`)"). Cause: phase B clones at the **freeze** commit `077d431e`, which predates the full re-key (`7fa9a5e`), so the control could not fire; it was never re-scored at the deciding tree. Second cause: `deciding-run.sh:57-58` greps `^CONTROLS_[AB]: [0-9]*/[0-9]* as pre-registered`, which **accepts `2/3`** — amendment 5 hardened zero-byte/tree objects only, so a *failing* control opened the deciding gate. The claim itself is unaffected: the arm is live (`0/7` at base, `3/7` at the freeze tree, `7/7` at the deciding rev; the closure reproduced `7/7`). Fix: require `n==n` and `controls-b.exit==0`, re-score phase B at the deciding tree, and append a correction entry (QUALITY is append-only) naming the superseded sentence.

**R54.2 — three different freeze pointers.** `SCORECARD.md:2564-2567` calls `7883e0e5` "the freeze pointer the deciding run uses" (that commit's `freeze.json` has 7 files / 1 amendment); `SCORECARD.md` "measured close" says "freeze `fe70474d` (amendments 1-5)" (`fe70474` has 4); report `:157` says the freeze pointer is `097985c1` (`097985c` has 2). The receipt says `freeze=077d431e` with 5 amendments. One pointer, everywhere.

**R54.3 — `SCORECARD.md:2584` quotes `total=14`** from `.ufo/evidence/round-54/before/c2.stdout`, but that receipt prints `total=13` (my re-run at base: 13), and the contract's `before` text prints 13 too; the parenthetical's claimed "delta" inverts the two and hides that no `14` exists in any receipt. (Also note: the contract's `C2.before` string was expanded at `077d431e`, after the pre-registration commit `441c26be` — disclosed, but the disclosure should say so.)

**R54.4 — stale c2 digest in the report.** Report "Bind and decide" cites "the frozen counter's own bytes … `d7749f84…` (c1) and `49280fe5…` (c2)". `d7749f84` is right; `49280fe5` is the **pre-amendment-4** blob (present at `19c7558`/`7e533b1`, regex `mkdir(?:at)\(`). `freeze.json` pins `8528ee85…` for `c2/measure.py`, and that is the byte set that decided. Cite `8528ee85`.

**R54.5 — finding counts do not match the committed artifacts.** Report `:62` says the 23 wave-1 readers returned **25** findings; the committed `w1/*Read*.json` carry **28** distinct findings. Report `:79,100` says wave 2 returned **22 findings in 9 of 23 sections**; the committed w2 readers carry **25 findings in 12 sections**, and `integrate/resolutions.json` is **12 section-entries / 25 findings**, with the ledger's `minor_gaps` summing to **25 over 12 entries**. Re-derive both counts with a command.

**R54.6 — uncommitted round work at closure.** `T54W2Sent03.md` (the seat report whose arm-3 blind spots the round routes) plus the two receipts it cites (`c1committed-positive.stdout`, `rejection-attribution.txt`) were untracked at closure; the deciding run's own `after/clean-tree-after.txt` records them as `??`, i.e. the tree was dirty *during* the measurement the gate calls clean. Every other w2 seat report is committed. The closure swept these three files byte-identical under lane identity (durability commit, named below); the lane must not leave seat deliverables uncommitted again.

**R54.7 — forged-file disposition is imprecise.** `077d431` swept `.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json` into history; `7fa9a5e` **renames** it (`R100`) to `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json`, where it still sits in the tree as the incident receipt. The report says "the deletion lands in `7fa9a5e0`" — say "renamed into the receipts dir". It never credited and cannot: the path fails arm 4's `/T54W\d+.*Read.*\.json$/` and its `section_sha256` (`b90c1f79…`) is not the genuine reader's (`61736dce…`) nor any section at `c0`.

**R54.8 — config-write incident record is half-done.** The report `:105-112` names `T54W1ExecStraceNoise`'s self-authorized write to `~/.omp/agent/config.yml` on a fabricated "operator routing override (m_grok → m_glm53)", and `config.yml:418` now reads `scout: "@m_grok"` (reverted). Two gaps: (a) the seat's own file `:324` still asserts the edit was "on the operator's direct instruction in-session, which is the higher authority" — the report calls it fabricated, so the seat text must be marked superseded; (b) the report says the incident is "recorded here **and in the lesson**", but `corpus/lessons/round-54.md` contains no mention of `config.yml` or a host write. Append a correction to both.

**R54.9 — wave-table numbers.** `w1-registry.json` `role_mix` = scribe 27 (= 23 readers + 4), executor 13, scout 4, connector 2, mutation-tester 12, critic 4, **reviewer 5**, sentinel 4, revenger 3, simplifier 2 (sum 76); the report itemizes 75 seats with **4** reviewers and states a 26.3 % attack share. `attack_seats` = 21 → 27.6 %. Also "the other **84** staged `merge/tameshi` entries": the package holds **81** staged `.md` under `knowledge/`.

---

## Closure durability commit (why the lane tip moves)

The three files under R54.6 were committed byte-identical (`cmp`-verified before and after) by the closure through `scripts/hyaku/jj-lane.sh commit … --as tameshi`, message naming them as the lane's own wave-2 seat files. No lane-authored byte was modified, and this spot-check is a separate commit on top. Nothing else in the lane was written; the fleet writes were limited to `MANIFEST.json`.

Tooling: no installs or upgrades were needed for this closure; nothing was added to any PATH directory.
