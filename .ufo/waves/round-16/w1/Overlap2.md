# Overlap2 — sibling-overlap scan (kama r16, kaidoku r17 × tameshi r16 C1/C2)

Seat: connector, wave 1. Read-only. Read timestamp 2026-10-20T13:28:39Z
(10:28:39 -0300). No mutant run, no gate/test execution, no diagnostic run
against lane or sibling code. One write: this file.

## Verdict in one paragraph

**No file-path or write-target overlap exists between tameshi r16 and kama r16
or kaidoku r17.** All three lanes write disjoint repos and disjoint report
files; fleet commits are serialized by `flock`. One *name* collision exists at
the fleet root (`/home/vgpnk/Projects/shokunin/.ufo/waves/round-16/` is the
protocol lane's tracked directory, not tameshi's), which creates a misroot
hazard only. On **surface/craft** there is one live overlap worth acting on:
kaidoku r17's C1(a) is repairing exactly the defect class that tameshi C2's
single `skill_sha256` pin can fall into once L1 edits `SKILL.md` to repair
blocking gaps. C1's own surface (kumitate `scripts/round-gate.mjs`) is stable
against concurrent kumitate work: the pinned rev's content SHA-256 equals
kumitate HEAD's *current* content SHA-256, and no sibling has recorded a
mutation case for that gate.

## Evidence and commands (all exit 0 unless stated)

| # | command | observed |
|---|---|---|
| 1 | `sha256sum SKILL.md .ufo/evidence/round-16/coldread/SKILL.snapshot.md` (tameshi) | both `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` |
| 2 | `git status --porcelain` (tameshi) | `A .ufo/evidence/round-16/coldread/SKILL.snapshot.md`; `?? .ufo/evidence/round-16/census-start.txt`; `?? .ufo/waves/round-16/` — `SKILL.md` clean |
| 3 | `git -C kama-shokunin status --porcelain` | `M tools/kama-probe.sh`; `?? .ufo/waves/round-16/`; `?? tests/probe-verdicts/` |
| 4 | `git -C kaidoku-shokunin status --porcelain` | `?? .ufo/waves/round-17/` |
| 5 | `git -C kumitate-shokunin status --porcelain` / `rev-parse HEAD` | empty; HEAD `1770305fae20826b39905a8251ddeca6b4957ac4` |
| 6 | `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs \| sha256sum` | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` |
| 7 | `git -C kumitate-shokunin show HEAD:scripts/round-gate.mjs \| sha256sum` | same `f890e277…a834d3e9` |
| 8 | `git -C kumitate-shokunin merge-base --is-ancestor 364f1d5 HEAD` | exit 0 (`ANCESTOR-OF-HEAD`) |
| 9 | `git -C kumitate-shokunin ls-tree 364f1d5 scripts/round-gate.mjs` and `ls-tree HEAD …` | both `100755 blob 1f7d623e…` |
| 10 | `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs \| grep -cE '^\s*check\('` | `60` |
| 11 | `git -C kumitate-shokunin show HEAD:scripts/round-gate.mjs \| grep -c 'sections'` | `0` |
| 12 | `git status --porcelain` (fleet) | `M .ufo/watchdog.log`; nine `?? .ufo/state/*.report-baseline` (driver files) |
| 13 | `git ls-files .ufo/waves/round-16` (fleet) | 6 tracked files: `before.md`, `clobber/classify.out`, `clobber/classify.sh`, `dispatch.md`, `gate/mutate.sh`, `gate/runs.md` |
| 14 | `git log --oneline -1 -- .ufo/waves/round-16/` (fleet) | `7c5b34f round-16: restore root SCORECARD/LOG …` |
| 15 | `ls .ufo/reports/round-16/ .ufo/reports/round-17/` | `kama.md` and `tameshi.md` absent (both in flight); `kaidoku.md` present only in `round-16/` (05:42) |

## O1 — Write sets are disjoint (no collision)

| lane | live writes (row 3/4/2) | report target |
|---|---|---|
| kama r16 | `tools/kama-probe.sh`, `tests/probe-verdicts/*`, `tools/kama-llamacpp-live.py`, lane `.ufo/waves/round-16/` | `.ufo/reports/round-16/kama.md` |
| kaidoku r17 | lane `.ufo/waves/round-17/{tools,pilot,w1,…}`, plus its SKILL/LOG/SCORECARD/SOURCES/QUALITY | `.ufo/reports/round-17/kaidoku.md` |
| tameshi r16 | `.ufo/evidence/round-16/**`, `.ufo/waves/round-16/**` (lane repo), `tools/mutate-and-run.sh`, SCORECARD/SHONEN/SKILL | `.ufo/reports/round-16/tameshi.md` |

Intersection is empty. kama's C1 target (`tools/kama-probe.sh`) and C2
(`tools/kama-llamacpp-live.py`, `tests/llamacpp-live/`) are not in tameshi's
ledger or source registry; kama's frozen snapshot
(`kama-shokunin/.ufo/waves/round-16/frozen/manifest.json:3-5`) pins
`sha256 93ee4302…`, `source_commit 20e392e…`, `source_path tools/kama-probe.sh`
— lane-internal only. kaidoku's r17 wave files are all under its lane
(`.ufo/waves/round-17/…`, including `contract.md`, `claims.json`,
`tools/*.py`).

## O2 — Name collision: fleet-root `.ufo/waves/round-16/` belongs to the protocol lane

Rows 13–14: the fleet-root directory is tracked and is the **protocol** lane's
round 16 (`dispatch.md:1` = `# Protocol round 16 — L2 dispatch receipt`). Tameshi's
own wave dir is `tameshi-shokunin/.ufo/waves/round-16/` (lane repo). Seats' tools
start at the fleet root, so a seat that resolves the relative trailer
`.ufo/waves/round-16/w1/<Seat>.md` from the fleet root writes into a sibling
lane's tracked directory. The wave-1 context already carries the absolute-path
rule (verified present), and rows 12–13 show **no such pollution yet**: no
`w1/` under the fleet dir and no modified protocol files.

Bounded check for L1 before the report:
`git -C /home/vgpnk/Projects/shokunin status --porcelain .ufo/waves/round-16/`
must be empty; any `w1/` or `<Seat>.md` there is a misroot, to be copied
byte-exact into the lane and deleted from the fleet copy (kama/kaidoku prompts
carry the same sweep; this lane should not skip it because "our wave dir is
elsewhere").

## O3 — C1 surface: kumitate `round-gate.mjs` is stable and self-contained

- Rows 6–7: pinned rev content == **kumitate HEAD content**, not merely
  rev-resolvable. The pin is therefore not stale against HEAD today.
- Row 8: pinned rev is an ancestor of HEAD; row 5: kumitate tree clean; no
  kumitate peer is in the live roster. [INFERENCE] kumitate is not mid-round
  right now; if it launches mid-round, rows 6–9 still make C1 drift-immune.
- Row 9: mode `100755` at both revisions. The runner mirrors the exec bit and
  refuses on pin mismatch (`tools/mutate-and-run.sh:99-106`), so the materialized
  leg is byte- and mode-identical.
- The pinned blob imports only Node builtins (`node:child_process`, `fs`, `os`,
  `path`, `url` at `round-gate.mjs:130-137`), and its `--selftest` is documented
  hermetic/temp-dir/zero-network (`:45-48`). No sibling file in kumitate's tree
  is needed to run the leg → **no transitive dependency on kumitate's working
  tree**.
- Row 10 gives 60 static `check(` registrations, matching
  `kumitate-shokunin/corpus/lessons/round-24.md:61` (`round-gate 60/60`) and the
  §13 projection's "60 `check(` registrations"
  (`tameshi-shokunin/corpus/knowledge/arm-class-matrix.md:317`). The verdict
  literals are `ROUND_GATE_SELFTEST: ${passed}/${results.length} pass` and
  `VERDICT: PASS|FAIL` (`round-gate.mjs:1505-1506`, assertion at `:1399-1400`).
  The 60/60 *run* is still unexecuted by me — wave 1 forbids it; the sweep is
  L1's.
- **Byte anchor for the pre-registration:** §13 pins the same artifact at
  `sha256 f890e277…a834d3e9` (`arm-class-matrix.md:301`) — identical to
  rows 6–7. The predictions are therefore anchored to the exact bytes the sweep
  will mutate; no re-derivation is needed, and no "§13 was written against a
  different revision" objection exists.
- **No duplicate sibling claim found.** kumitate's `SCORECARD.md:1168-1182`
  records a 41-mutation audit of *some* gate (16 killed / 25 survived), but its
  counters are `sections`, `adv`, `yes` — and row 11 shows `round-gate.mjs`
  contains **zero** occurrences of `sections`. `grep -rn 'round-gate'` over
  kumitate's `corpus/` + `LOG.md` + `SCORECARD.md`, filtered for
  mutation/kill/mutant, returned only selftest-count lines, no mutation case.
  So the seventh leg is complementary, not a re-run of a sibling's record.
  Caveat to state in the report: kumitate's own note says its audited suite was
  "a regression net for the arms, not a proof that the arms are correct"
  (`SCORECARD.md:1179-1180`); tameshi should not upgrade that into a
  mutation-completeness claim for `round-gate`.

## O4 — The live overlap: kaidoku r17 C1(a) is repairing the class C2's pin can exhibit

kaidoku r17 declared (`kaidoku-shokunin/.ufo/waves/round-17/claims.json:9-15`):
claim (a) appends a named correction to every "pins stayed unchanged during
execution" statement, and builds a producer that records **pre/post pin maps
with timestamps and compares them (shown able to fail)**. Its source defect is
`corpus/lessons/round-16-verifier-spotcheck.md:183`: *"one 20-entry hash map and
`pins_unchanged_during_run:true`, but no before/after maps … proves only that
recorded hashes match committed S/A bytes 20/20, not that files were stable
throughout the run."* The instrument contract is explicit
(`.ufo/waves/round-17/contract.md:12-20`): `snapshot()` / `compare()`, and *"It
proves only 'same bytes at two instants', never 'unchanged throughout'."*

Tameshi C2 has the same shape: the ledger schema records **one**
`skill_sha256` per entry, from the frozen snapshot. But the wave context says
*"blocking gaps are repaired by L1 and re-read in wave 2"*
(`tameshi-shokunin/.ufo/waves/round-16/spec1.json` context, verified verbatim).
If any section lands `gap-blocking`, L1 edits `SKILL.md`, and the ledger's
`skill_sha256` then describes the **pre-repair** bytes only. A report sentence
of the form "full-page cold-read of SKILL.md (sha256 97cf…)" would then assert
an identity that no longer holds at round end — the exact overreach kaidoku's
outside verifier caught one lane over.

Today the pins agree (row 1: `97cf…` twice) and `SKILL.md` is clean (row 2), so
the risk is latent, not present. It materializes only if `SKILL.md` is edited.

Also note the ownership surface: tameshi `PROVINCE.md:10-12` lists "kaidoku's
audit-lane pattern (verify: lines, bit-exact evidence ids)" under **Owns**, while
kaidoku is concurrently *amending that pattern's provenance discipline*. That is
not a write collision (tameshi never writes kaidoku), but any citation of the
pattern this round must be pinned: kaidoku r17 baseline
`b563c799d97774aae4351276fe43cb897311e349` (`claims.json:4`), never kaidoku
HEAD, and never the in-flight r17 files as landed evidence.

## O5 — In-flight craft analogue, not admissible this round: kama r16 stub matrix

kama r16 is building `tests/probe-verdicts/<Family>.json` + `check.py`: a
declared-family × fixture table with an exact expected
`{verdict, reason, exit}` per row (`kama-shokunin/.ufo/waves/round-16/build/spec.json`
context, "Stub-matrix schema"), across eight families (LoadingEnvelope,
LoadingRace, Overbroad503, NonLoadingStatuses, ReadyControls, AuthAndDead,
EnvelopeShapes, ForeignControls). That is the same *shape* as tameshi's arm-class
matrix (declared family × fixture × meta-check). It is not a mutation corpus and
it is uncommitted/in flight (row 3; 7 of 8 family files present at 10:27).
Consequence: **not** usable as second-lane evidence for any pattern claim this
round. The two-lane admission rule triggers only for a claim of generality; C1
is a case-depth record (the mutation pattern already spans four lanes in the
existing ledger, `tools/mutate-and-run.sh:84-89`) and C2 is lane-local, so
neither claim needs kama. If L1 nevertheless wants a second lane for the
"pre/post pin map" craft, the candidate is kaidoku r17 **after it commits**, not
during.

## O6 — Commit path and resource contention

- Fleet commits race-free: `scripts/hyaku/fleet-commit.sh:37` takes
  `flock -w 1200`; `:31-32` refuse absolute/`..` paths and `.ufo/state/*` +
  `.ufo/watchdog.log`. Report filenames are lane-distinct (`kama.md` vs
  `tameshi.md`, both in `round-16/`; kaidoku in `round-17/`). Residual, by
  design: the helper pushes all local master ahead of origin, so a tameshi push
  may carry kama's already-committed-but-unpushed commit; no rebase, no index
  race. Do not pass any path outside the round's own report.
- Contention, not collision: kaidoku is running Ghidra analyze sessions
  (`/tmp/rea-ghidra-*`, per its `contract.md`), kama launches an ephemeral
  llama-server on a non-registered loopback port (its C2 context), tameshi runs
  one control + 10 mutants of a hermetic Node suite. `mutate-and-run.sh` verdicts
  are exit-based; duration is provenance only (`:71`, `MUTATE_TARGET` /
  `CONTROL:` / `DEFECT` lines). A load-induced child failure would surface as
  `SURVIVED`/`INCONCLUSIVE`, never silently as a kill — so if any leg reports
  `INCONCLUSIVE` or `SETUP`, re-run after the siblings' waves and record both
  runs; never read duration as evidence.

## One bounded move (synthesis with kaidoku r17 C1(a))

**Add a `skill_pins` object to the L1-assembled
`.ufo/evidence/round-16/coldread/ledger.json`:** `{pre: {sha256, taken_at_utc},
post: {sha256, taken_at_utc}, compare: "equal"|"changed"}`, with `pre` = the
frozen snapshot (`97cf…`) and `post` taken **after the last `SKILL.md` write
before the report**. Keep `entries[]` unchanged — this is an additive top-level
key, not a schema rewrite.

- Why it is non-obvious: the ledger's `skill_sha256` looks like proof for the
  whole round, but it is one instant. The round *plans* to edit `SKILL.md`
  (repair loop), which is exactly the window a single pin cannot cover, and the
  sibling lane is being graded on repairing that same overreach this round.
- Cost: one `sha256sum` pair and a compare. Reuse the lane's existing
  before/after pattern (`tools/mutate-and-run.sh:73`, `:500-504`,
  `MUTATE_RESTORE`), no new tool, no dependency on kaidoku.
- Axes: **calibration improves** (C2's evidence statement becomes two-instant
  and falsifiable); **depth untouched** (C1 ledger legs unaffected); **no other
  axis harmed**. If `SKILL.md` is never edited, `pre == post` is a one-line
  proof and nothing else changes.
- Risks, stated: (1) `ledger.json` is a named interface — an exact-shape reader
  could flag the extra key; mitigate by keeping it a single additive object and
  documenting it in the report; (2) ordering ambiguity — define `post` as "last
  write before report" explicitly; (3) do **not** claim the pre/post-pin pattern
  as general from this round: its second lane (kaidoku r17) has not landed.
- Verification: `sha256sum SKILL.md .ufo/evidence/round-16/coldread/SKILL.snapshot.md`
  (equal today); `git diff --stat -- SKILL.md` at report time (empty ⇒ equal);
  read back `json` keys; red control in `/tmp`: copy `SKILL.md`, append one byte,
  recompute → `compare: "changed"`, exit non-zero from the checker.

## Limits

- No mutant, selftest, gate or diagnostic was executed (wave-1 pre-registration
  rule). Every behavioral statement above is a static read and is marked
  `[INFERENCE]` where it predicts what a run would print.
- I did not read kama/kaidoku filed reports or their wave seat reports; only the
  files pinned in the evidence table, their PROVINCE/SCORECARD tails, live wave
  specs/manifests, and kaidoku's r16 spotcheck lines cited above.
- `kumitate.round` = 18 in `.ufo/state/` while kumitate's prompt-less repo sits
  at round 34: I treat driver counters as opaque and do not infer round identity
  from them. [INFERENCE] "not mid-round" rests on the empty tree + absent roster
  entry, not on that counter.
- Tool installs/upgrades: none.
