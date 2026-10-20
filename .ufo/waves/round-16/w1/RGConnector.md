# RGConnector — C1 sibling-overlap: is kumitate changing `scripts/round-gate.mjs`?

Seat: `TameshiR16.RGConnector` (connector, wave 1). Observed 2026-10-20
13:18–13:31Z (10:18–10:31 −03), read-only. No mutant was run and no
`round-gate` mode was executed by this seat; every kumitate command below is a
read (`log`/`show`/`status`/`rev-list`/`merge-base`/`branch`/`stash`/`worktree`/
`sha256sum`). `kumitate-shokunin` was never written. No scratch dir was created;
where another seat's scratch is cited it is labelled as such.

## Answer

**No — as recorded at kumitate HEAD `1770305` (2026-10-19T22:05:38−03) and
observed at 13:20–13:31Z, kumitate is not changing, hardening, or re-pinning
`scripts/round-gate.mjs`.**

- The path's last-touching commit is `364f1d5` (2026-10-13T22:49:20−03, the
  round-24 triage); **zero** commits touch the path after it (E1), and the file
  has only four commits in its whole history (E2).
- `364f1d5` is 37 commits behind HEAD but the blob is **byte-identical at both
  revs** and identical to the live working-tree file (E3–E6).
- Kumitate's working tree is porcelain-empty; one branch (`master` ==
  `origin/master`), no stash, one worktree (E5, E7–E9).
- The pin the owner publishes is the same blob: `pin.round-gate=` at
  `kumitate-shokunin/SCORECARD.md:297` (E10).
- The next round is already pre-registered and **none of its three claims names
  `round-gate`**: `SCORECARD.md:437-454`, claims at `:440` (kimi-census K1),
  `:450` (`proxy-check` distinct derivation), `:453` (runtime R5+R7). No
  `.ufo/rounds/round-35` exists (E11–E12).
- No kumitate round is in flight: `.ufo/state/kumitate.round` reads `18` with
  mtime 2026-10-15 01:50:57, no process matches `kumitate`, and the lane's
  newest artifact is round 34 (2026-10-19) (E13–E14).

## Evidence (command → exit → key output)

All paths relative to `/home/vgpnk/Projects/shokunin`; `K=kumitate-shokunin`.

| # | command | exit | key output |
|---|---|---|---|
| E1 | `git -C $K log --oneline 364f1d5..HEAD -- scripts/round-gate.mjs` | 0 | *(empty)* |
| E2 | `git -C $K log -4 --format='%h %cI %s' -- scripts/round-gate.mjs` | 0 | `364f1d5` 2026-10-13T22:49:20−03 round-24 triage; `c860887`; `23452e7`; `c91fe96` |
| E3 | `git -C $K show 364f1d5:scripts/round-gate.mjs \| sha256sum` | 0 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` |
| E4 | `git -C $K show HEAD:scripts/round-gate.mjs \| sha256sum` | 0 | same `f890e277…d3e9` |
| E5 | `git -C $K status --porcelain \| wc -l` | 0 | `0` |
| E6 | `sha256sum $K/scripts/round-gate.mjs` | 0 | `f890e277…d3e9`; 80415 B, mtime 2026-10-13 22:01:24 |
| E7 | `git -C $K rev-list --count 364f1d5..HEAD` | 0 | `37` |
| E8 | `git -C $K merge-base --is-ancestor 364f1d5 origin/master`; `git -C $K log -1 --format='%h %cI %s' origin/master` | 0 | yes; `1770305 2026-10-19T22:05:38−03 Integrate remote documentation; preserve local round log` |
| E9 | `git -C $K branch -a`; `git -C $K stash list`; `git -C $K worktree list` | 0 | only `master` + `origin/master`; stash empty; one worktree at `1770305` |
| E10 | `grep -n '^pin.round-gate=' $K/SCORECARD.md` | 0 | `297:pin.round-gate=f890e277…d3e9` |
| E11 | `sed -n '437,454p' $K/SCORECARD.md` | 0 | round-35 pre-registration; claims at `:440`, `:450`, `:453`; no `round-gate` |
| E12 | `find $K/.ufo/rounds -maxdepth 1`; `ls $K/.ufo/reports` | 0 | `round-33`, `round-34` (only `sources-gate.md`); reports: `round-33` only |
| E13 | `cat .ufo/state/kumitate.round`; `stat -c '%y' .ufo/state/kumitate.round`; `pgrep -af kumitate` | 0 / 0 / **1** | `18`; mtime 2026-10-15 01:50:57; `pgrep` no match |
| E14 | `grep -rn 'tameshi' $K --include='*.md' \| wc -l` | 0 | `0` — kumitate records nothing about this sweep or lane |
| E15 | `git -C $K log --oneline -3 -- scripts/kimi-census.mjs`; `sha256sum $K/scripts/kimi-census.mjs` | 0 | `1a8eed5` round-34 changed the gate (58+/32−); live `5e8d5913…` (SCORECARD `:301`) — the owner *does* edit and re-pin its own gates, but only in its own rounds |
| E16 | `sha256sum tameshi-shokunin/tools/mutate-and-run.sh`; `git -C tameshi-shokunin status --porcelain tools/mutate-and-run.sh`; `grep -n 'js-round-gate' …` | 0 / 0 / **1** | sha `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` (== S031 pin, `SOURCES.md:42`); porcelain empty; **0** matches for `js-round-gate` (`grep` exit 1 = no match) |
| E17 | command D regex (`tameshi-shokunin/SCORECARD.md:72-73`) over the working harness | 0 | `recorded_cases=6`; matched lines are the six existing legs only |

## Contested scope (three items, each explicit)

1. **Ownership boundary.** The gate is kumitate's: `kumitate-shokunin/SKILL.md:595`
   ("Owner: this lane (kumitate L1)") over the seven-row gate registry
   (`:587-605`), and its pin lives in kumitate's stanza. The *case* is tameshi's:
   `tameshi-shokunin/PROVINCE.md:12-16` owns the method with
   `kumitate-shokunin/scripts/*` as read-only primary surfaces and states
   "Never edits a sibling's gate code (read-only probes; recommendations travel
   in round reports)." The contest is therefore not over the sweep — it is over
   (a) who may pronounce the gate robust (kumitate, or the operator if the gate
   ever becomes fleet law) and (b) who may harden it (kumitate alone).
2. **Fleet-adoption status is open, not settled.** `.ufo/l0-questions.md:8`
   (kumitate round-10) asks exactly whether `round-gate.mjs` should be adopted at
   the driver level, with options (a) lane-local, (b) per-lane round ritual,
   (c) port findings into `report_of()`/driver closure. The file records no
   answer. `:9` (kumitate round-11, proxy claim block) is a second unanswered
   adoption question for the same lane. A tameshi kill rate is not a vote on
   either; in particular it does not test the defect named in `:8`
   (`scripts/shokunin-watchdog.sh:44` completes a round on file existence).
3. **Pin currency vs rev identity (the trap for a reviewer).** C1 names
   `364f1d5`; kumitate HEAD is `1770305` (37 commits later); `§13` of
   `arm-class-matrix.md` was read at `175de6ba` (2026-10-14). **All three revs
   resolve to the same blob** (`f890e277…d3e9`, E3–E4 and
   `kumitate-shokunin` history). The pin is *current at HEAD and six days older
   than the sweep*; a record that names only one rev invites either a false
   "stale pin" finding or a false "HEAD pin" claim.

Kumitate's own declared limits bound any claim about this gate
(`kumitate-shokunin/SCORECARD.md:1116-1131`): the tool "is a tripwire, not a
monitor"; its 1024-byte and 2-heading thresholds "are this lane's bar, not fleet
law"; `--tracked` excludes the in-flight report; audit mode cannot see a round
that filed no report. Only the two citation checks and the SHONEN heading trace
to written protocol.

## Would a recorded tameshi case on this pin conflict with owner work?

**No conflict with owner work as recorded**, under four conditions. The
positive evidence:

- No edit, no re-pin, no queued change (E1–E12). Round-35's gate edits are
  `kimi-census.mjs` (claim 1) and `proxy-check.mjs` (claims 1–2) (E11) — neither
  is `round-gate`. `proxy-check` *pins* `round-gate` but editing it does not
  change `round-gate`'s bytes, so `pin.round-gate` stays valid; editing the
  pinning tool updates `pin.proxy-check` (`:298`), not `:297`.
- Precedent is established in both directions: kumitate already records a
  sibling lane's mutation of `scripts/proxy-check.mjs` — "7 of 9 killed… the two
  surviving mutants are named gaps, queued with their proposed cases"
  (`SCORECARD.md:1337-1341`) — and tameshi already carries **two kumitate gates
  as recorded legs** (`corpus/SOURCES.md:42-43` S031/S032, `:48` S037;
  `kimi-census` 8/10, `claims-check` 7/10). A third kumitate gate is in-pattern,
  not a new land grab.
- Tameshi's harness already replays legs by materializing the blob from the
  sibling's object store (`git show <rev>:<path>`), so a sweep on a copy cannot
  move kumitate's tree or its pin (`tools/mutate-and-run.sh` header, r7-1
  contract). A missing rev is a SETUP refusal (exit 2), never a pass.

Conditions (each is a way the case *would* become a conflict):

1. **No writes to kumitate, and the witness must be shown.** The claims-case
   precedent records the sibling witness at both ends — target materialized from
   the object store, `kumitate git status --porcelain` empty
   (`corpus/knowledge/mutation-case-kumitate-claims.md:366-410`). C1 should carry
   the same before/after witness; the copy-only rule is what keeps the case
   inside `PROVINCE.md:16-18`.
2. **No owner/fleet certification language.** "Round-gate survives N/10" is
   tameshi's measurement of a pin; "round-gate is robust" or "ready for fleet
   adoption" is kumitate's (or the operator's) verdict, and `:8` is still open.
3. **No re-pin authority, and no claim that the pin is HEAD.** Tameshi may quote
   `SCORECARD.md:297`; it may not edit it, and it must state the three-rev
   identity rather than implying currency from a single rev.
4. **No half-registered leg.** The depth claim depends on the leg existing in
   `tools/mutate-and-run.sh` and on command D counting it
   (`tameshi-shokunin/SCORECARD.md:66,72-73`). Observed state at 13:28Z: the
   harness at HEAD is sha `75ed934…` (== S031 pin), contains **no**
   `js-round-gate` text, and command D's own regex returns
   `recorded_cases=6` (E16–E17). At 13:26:52Z a working-tree draft (sha
   `2e810b5…`, 49+/23−) held `PIN_ROUNDGATE`/`REV_ROUNDGATE` plus
   `@@RG_KILLED@@`, `@@RG_PCT@@`, `@@R16_ROUNDGATE_SPEC@@`; by 13:27:31Z it was
   reverted. A placeholder commit would fail the `--regression` selftest's
   integer expectation (`:1609`) and leave the depth score at 6.

| observed activity | evidence | conflict? |
|---|---|---|
| `round-gate.mjs` changed after the pin | E1, E2 | **no** |
| owner re-pin queued (round 35) | E11 | **no** — three claims, none names the file |
| owner has *ever* re-pinned a gate in-round | E15 (`kimi-census`, round 34) | **no**, but it bounds "the pin is final" phrasing |
| kumitate round live now | E12–E13 | **no** |
| kumitate aware of tameshi's sweep | E14 (0 mentions) | **no**, and it means results are not yet routed |

## What to report rather than absorb

1. **Survivor/refutation table as a kumitate-facing hand-off**, in the round
   report, using kumitate's own queue idiom (`SCORECARD.md:1337-1341`): mutant
   id, `§13` cell, measured verdict, proposed fixture. Do not edit kumitate's
   `SCORECARD.md`, its pin, or its lessons; tameshi has no re-pin authority.
2. **The open adoption questions `:8`/`:9` as status, not as answers.** Report
   that they remain open and that this sweep does not test the driver-closure
   defect named in `:8`; do not let a kill rate be cited as fleet certification.
3. **The three-rev one-blob reconciliation** (364f1d5 last-touch / 175de6ba §13
   read / HEAD 1770305) and a one-line owner-pin cross-check
   (`SCORECARD.md:297`). This is the non-author re-derivation, not a claim.
4. **Kumitate's declared limits** (quoted above) so the case does not imply the
   suite tests a monitor, a fleet threshold, an unfiled round, or the in-flight
   report.
5. **Environmental transients, labelled as such.** A sibling probe run under
   `/tmp/tameshi-r16-survivorprep/` hit `ENOSPC` at 13:27Z (`full.err`:
   `ENOSPC … at failClosed (round-gate.mjs:616)`); the clean re-run at 13:29:18Z
   shows 0 `"ok": false`, and `df -h /tmp` now reads 3 % used. Not a gate
   defect; but an aborted suite run must never be recorded as KILLED or
   SURVIVED.

## Proposed move (one, bounded)

**Make leg 7 a converted-projection case with two pre-registered signals, not a
tenth kill-aimed sweep.**

- **Composition.** 10 mutants = **3 positive controls** drawn from cells `§13`
  declares *covered* (predicted **KILLED**) + **7 hole-aimed** mutants drawn
  one-to-one from `§13`'s named uncovered cells (predicted **SURVIVED**):
  `INTERNAL_ERROR` token (`§13.3`, no fixture), tracked `REPORTS_DIR_MISSING`
  call site, main-repo `UPSTREAM_MISSING` species, `REPORT_MIN_BYTES` interval
  `[26,1059]` (`§13.4`), `HISTORY_LIMIT` 1000, `--selftest --json` unpinned
  (`§13.6`), `UFO_SRC` set-value branch. (`§13.5`'s detail tails / `durationMs`
  / JSON fields are already probed on pristine — see below — so use them as
  *observable* expectations, not as duplicate mutants.)
- **Pre-registration.** Write the 10 directives *and each predicted verdict +
  expected observable* to the spec file, timestamp it, and commit it **before**
  the first mutant runs. `§13` itself is already publicly prior (committed
  `e0c453e`, 2026-10-14T14:33:30−03; `§13` header: "no mutant was cut… a
  projection cell is a probe candidate for a future round").
- **Record two numbers.** (i) **prediction accuracy** (target 10/10), (ii)
  **kill rate** (target 3/10) with composition stated; the ledger's
  composition-binding rule (`fleet-kill-rate-ledger.md:17-24`) makes a new
  composition legitimate, and tsukuroi's 6+4 case is the format precedent. Add
  the record-time owner-pin line described above.

**Why this and not the default composition.** The six existing legs are
kill-aimed or mixed (80 %, 80 %, 60 %, 40 %, 47 %, 70 %); a seventh kill-aimed
case repeats the composition and adds little. `§13` was written *as a
prediction set* and explicitly nominated its cells as future probes; converting
it gives the round a falsifiable calibration reading (C2) **and** a genuine
seventh case (C1) in one artifact. The independent probes already exist:
`/tmp/tameshi-r16-survivorprep/probes.mjs` (another seat's scratch) carries
P1–P12 mapped to `§13.5`/`§13.6`, and its pristine log (13:29:18Z) reports 0
failed arms — i.e. the behaviour the survivors must preserve is established
**outside** the suite, which is exactly what makes a SURVIVED prediction
meaningful rather than a guess. (The `ENOSPC` run earlier that day was
superseded; see above.) A sibling cold-read seat independently ran the pinned
blob: `/tmp/tameshi-r16-CR10-3KfJ8A/rg-selftest.log` → `ROUND_GATE_SELFTEST:
60/60 pass`, `VERDICT: PASS`, copy sha `f890e277…` — consistent with C1, but it
is that seat's execution, not mine.

**Affected axes.** Calibration ↑ (falsifiable, public prior, per-cell
accounting; currently 6, the round claims 8); depth ↑ (seventh recorded case,
new composition; SCORECARD `:66` cap 10); operability neutral (harness change
only; replay cost recorded); no kumitate surface changes, so no sibling axis is
touched.

## Risks

1. **All-survivor leg is unfalsifiable on its own** — hence the 3 controls. If a
   control survives, that is a **refutation of `§13`**, to be recorded as the
   round's finding, not reclassified after the run.
2. **Replay cost.** `--regression` re-sweeps each leg (fresh control + one run
   per mutant); leg 7 adds 11 round-gate suite executions. The suite is 60
   checks with `mkdtemp`/git fixtures; kumitate measured 3.1 s at 49/49
   (`SCORECARD.md:428`), so [INFERENCE] ~4–6 s per run ≈ 45–65 s per regression
   leg. Record the measured wall time; the harness default is `--timeout 300`.
3. **INCONCLUSIVE ≠ SURVIVED.** Exit 124/126/127 is INCONCLUSIVE; under a
   loaded wave (64 scratch dirs counted at 13:28Z) a timeout must be re-run, and
   an aborted write (the `ENOSPC` above) must be discarded.
4. **Placeholder landing.** The leg must not land with `@@RG_KILLED@@` /
   `@@RG_PCT@@` / `@@R16_ROUNDGATE_SPEC@@`: command D's `\d+/\d+` will not
   count it, and `--regression --selftest` expects an integer
   (`tools/mutate-and-run.sh:1609`). Land only after the measured table exists.
5. **Future owner edit.** If kumitate re-pins later (its `kimi-census` round-34
   edit is the precedent), the leg still replays from `364f1d5`; the record must
   not imply currency beyond the pin, and the ledger §3 row
   (`fleet-kill-rate-ledger.md:109`) plus the S031/S032/S037 source dates need
   re-dating when the leg lands.

## Verification (for the L1; none of these was run by this seat except the read-only ones above)

```sh
# pin identity, before and after the sweep
git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs | sha256sum   # f890e277…d3e9
git -C kumitate-shokunin status --porcelain                                # empty
grep -n '^pin.round-gate=' kumitate-shokunin/SCORECARD.md                  # :297, same sha

# depth accounting after the leg lands
git show HEAD:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
# expected: recorded_cases=7 depth_score=7

# leg replay (exact expectation; fail-closed exit 2 is not a pass)
bash tools/mutate-and-run.sh --regression
# expected: REGRESSION_CASE js-round-gate: PASS; REGRESSION_PIN js-round-gate = f890e277…;
#           killed-delta 0, flips 0, inconclusive 0
bash tools/mutate-and-run.sh --selftest        # stays green

# pre-registration ordering proof: spec+prediction commit/mtime strictly before the sweep log
```

If any of these contradicts the table above, the table is the record: the
kumitate state was observed at HEAD `1770305` on 2026-10-20 13:20–13:31Z, and a
later owner edit changes the recommendation, not the observation.
