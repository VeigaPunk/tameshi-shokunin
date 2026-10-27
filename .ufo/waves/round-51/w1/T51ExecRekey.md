# T51ExecRekey — round-51 cold-read re-key instrument

Seat: T51ExecRekey (executor, round-51 w1). Item: build the round-51 cold-read re-key instrument.
Deliverable: `.ufo/waves/round-51/w1/T51ExecRekey/refresh.py` (269 lines, 16173 B, mode 755, sha256
`2055eb335041070de6984ebb9c5440fe959cdcdaa128f4c7b550c4c8b40e61a5`; the L1 copies it to
`.ufo/evidence/round-51/coldread/refresh.py`). The only new lane paths this seat wrote are this report and
this directory; every fixture clone was scratch and is deleted before yield. No tools installed.

## 1. Interface and behaviour

`refresh.py LANE CAND READERS_JSON` (usage exit 64 otherwise, `refresh.py:260-262`).

- **Targets are computed, not hardcoded** — `refresh.py:49` (BASE `9962033fd7a75aa2f2847e979dd687a5d28505a1`),
  `refresh.py:176-179`: the unchanged round-21 monitor is run strict (no override) on a `--shared` scratch
  clone at BASE and at CAND (`refresh.py:90-102`, `--repo CLONE --rev REV`), and the targets are the headings
  it credits at BASE and does not credit at CAND, in BASE page order. Refusals: no target at all
  (`:180-181`), a target not credited at BASE (`:183-184`, structural — see §5), a target heading absent or
  not a single section at CAND (`:185-186`, `:116-117`).
- **Read method** (round-49 method, `.ufo/evidence/round-49/c1/refresh.py`, extractor/resolver from the
  round-49 counter `.ufo/evidence/round-49/c1/measure.py`): per target the section text and every lane file
  its pointers cite are read in the clone at CAND under `tools/trace-inputs.py`
  (`refresh.py:123-135`, `:208-214`). Non-record files are direct opens; the five record files
  (round-49 `VOLATILE`: LOG.md, SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md, corpus/README.md) are
  read through `git cat-file blob CAND:<path>`, so cited lines are observed without making the whole growing
  file an input (`READ_CMD`, `refresh.py:59-76`). SKILL.md is read as the page and never an entry input
  (`:129-131`, `:216`). Trace cleanliness is enforced (`:217-222`): no volatile input, no live-lane read
  outside `.git/`, no untracked read, no missed direct read.
- **One-hop internal pointer** (`refresh.py:137-144`, applied at `:197-203`): when a target's pointers resolve
  to no non-record file, its own unresolved internal line pointer (`:N-M` into SKILL.md) is followed once —
  those SKILL.md lines are read and the file pointers they carry are opened, and the span is recorded in the
  receipt as `internal_pointer_follow`. This is load-bearing for exactly one section (see §2,
  `## The operator's runbook…`: its 9 lines cite only `:1226-1228`, and those lines carry
  `fleet-kill-rate-ledger.md:282` → `corpus/knowledge/fleet-kill-rate-ledger.md`).
- **Seats** from READERS_JSON (`refresh.py:204-206`): every target must name at least one seat; `"*"` is the
  default for headings the file does not name (fixture runs used it; the real run should name the wave-2
  readers per heading). The L1 integration seat is appended.
- **Ledger append** (`refresh.py:224-239`): one `class: record`, `verdict: verified-record`,
  `commands_executed_count: 1` entry per target with `skill_sha256` = the section sha at CAND,
  `read_rev` = CAND, `inputs` = trace inputs minus SKILL.md, `traces` = the receipt,
  `seats` = readers + `L1 TameshiR51 integration`, `reports` = `.ufo/evidence/round-51/coldread/reads/` and
  `.ufo/evidence/round-51/coldread/rekey-<cand8>/refresh-receipts.json`. Existing entries are never touched:
  the ledger is rewritten with its own serialization (`indent=1`, `ensure_ascii=True`, no trailing newline;
  round-trips byte-identically, verified) and appended only.
- **Guard before any write** (`refresh.py:164-169`): the working-tree ledger must parse equal to the ledger
  blob at CAND, so the entries are appended to the revision they claim to be appended to.
- **Writes**: the round-21 ledger; `.ufo/evidence/round-51/coldread/rekey-<cand8>/{traces/section-<n>.json,
  refresh-receipts.json}`. Scratch `$HYAKU_SCRATCH/tameshi-r51/refresh`, removed in `finally` (`:255-256`).
  Runtime on this host: ~35 s (two monitor runs ~15 s each + 20 traces), one live clone.

## 2. Fixture proof (observed)

Fixture built exactly as the item prescribes, in scratch (`$S=/fast/scratch/hyaku/tameshi-r51/T51ExecRekey`):

```
git clone -q --shared LANE $S/lane && git -C $S/lane checkout -q --detach 84aa673a1a476e48ccf239335696f0518d08bae7
# (1) append '# round-51 cold-read fixture: appended comment line (monitor drop test)' to tools/mutate-and-run.sh
# (2) add one row inside the SKILL.md '### Gate/probe registry' table (8 cells, after the 2026-10-26 row set)
git -C $S/lane add -A && git -C $S/lane commit  -> 925bd28783c1d49c7cea6bba163612c3b851be00
```

| step | command | observed |
|---|---|---|
| base | `python3 -B .ufo/evidence/round-21/coldread/measure.py --repo $S/lane --rev 9962033fd7a7…` | total 64 covered 64 **score 8** strict |
| drop | same, `--rev 925bd287…` | total 64 covered **44** **score 6** strict |
| re-key | `python3 …/T51ExecRekey/refresh.py $S/lane 925bd287… readers.json` | `TARGETS 20 BASE 9962033f (64/64 score 8) CAND 925bd287 (44/64 score 6)`, exit 0 |
| commit | ledger + receipts committed in the fixture (`20264c217cee5096eb74e7254f8d5b15b43103d9`) | ledger 511 → 531 entries, previous 511 entries byte-identical (`prefix-preserved True`) |
| restore | monitor `--rev 20264c21…` | total 64 covered **64** **score 8** strict, no uncovered section |
| precheck | `bash .ufo/evidence/round-48/quality/coldread-precheck.sh $S/lane 9962033fd7a7… HEAD` | `COLDREAD_PRECHECK floor=9962033fd7a7 floor_credited=64 cand=HEAD cand_credited=64 lost=0 ok`, exit 0 |

Second fixture adds the C1 shape (an append to a record file): same runner comment and registry row **plus**
`<!-- round-51 re-key fixture: appended README record line -->` at the end of `corpus/README.md`, commit
`974d2d9005a7cb29bc6bdd6166e2e571c57a8f22`; monitor 64/44 score 6 (same 20 headings — the README append adds
no drop because the four README-referencing sections already drop on the runner byte change); refresh →
`TARGETS 20 … (44/64 score 6)`, exit 0; commit `0f28deeb246b950dccaffb4a05e93228a4de3f60`; monitor 64/64
score 8; precheck `lost=0 ok` exit 0. The record-via-blob reads mean the new entries do not pin README, so
they survive the append (this is the C1 durability case the real round needs).

Drop composition (`monitor-summary.txt`): 19 of the 20 targets lose credit with
`input-drift:tools/mutate-and-run.sh` in their entry reasons; `### Gate/probe registry` is
`no-ledger-entry` (its section sha changed). 44 credited, score 6, matches the contract's freeze measurement.

Reproduce the fixtures (they are scratch, deleted at yield; the receipts below are the retained evidence):

```
S=$(mktemp -d -p /fast/scratch/hyaku/tameshi-r51/T51ExecRekey)
git clone -q --shared tameshi-shokunin $S/lane && git -C $S/lane checkout -q --detach 84aa673a1a476e48ccf239335696f0518d08bae7
# apply the three edits above, then (fixture identity, -C, toplevel asserted)
git -C $S/lane add -A && git -C $S/lane commit -m 'fixture'
python3 refresh.py $S/lane $(git -C $S/lane rev-parse HEAD) readers.json
git -C $S/lane add -A && git -C $S/lane commit -m 'rekey'
```

## 3. The 20 sections to re-key, with their pointers (wave-2 reader list)

Recomputed from the fixture candidate `974d2d90`; the instrument recomputes them for the real CAND, so this
list is the expected shape, not a constant. Full machine-readable detail (every pointer, ordinal, resolved
kind, `skill_line`): `T51ExecRekey/targets.json`. `direct` files are opened; record files are read as
`CAND` blobs; `../scripts/hyaku/jj-lane.sh` is external (fleet repo) and is not read, per round 49.

- **## Mutation-sweep recipe — numbered steps; bounded cold-read evidence** (131-245) — direct
  `corpus/knowledge/mutation-case-kimi-census.md:4-7,20-21,13-16,41-53,155-166,183-191,22-25,26-28,30-33,59-76,44-53,29-31,82-99,34-35`,
  `corpus/knowledge/mutation-case-kagi-census.md:24-38,27-35,42-43,13-17,44-45,184-191,44-47,48-49,50-53,67-67,82-103,88-91,111-114,118-122,252-254,54-56`,
  `corpus/knowledge/gates-survey-kumitate.md:19-31`, `corpus/knowledge/gates-survey-kagi.md`,
  `tools/mutate-and-run.sh:425,569-574`; record `corpus/README.md`
- **## Restore discipline — before/after identity, not continuous non-write proof** (375-404) — direct
  `corpus/knowledge/mutation-case-kimi-census.md:13-16,4-7,172,34-35`,
  `corpus/knowledge/mutation-case-kagi-census.md:13-17,44-45,54-56`, `tools/mutate-and-run.sh`;
  records `SCORECARD.md:13,16`, `corpus/README.md`
- **### The protocol — ordered, fail-closed** (827-857) — `corpus/knowledge/mutation-case-mado-verify.md:73,187-189`, `tools/mutate-and-run.sh`
- **### The boundaries — what a service run is not** (858-882) — `corpus/knowledge/fleet-suite-census.md:288-291`, `tools/mutate-and-run.sh:36-38`, `corpus/knowledge/mutation-case-mado-verify.md:57-59,175-176,66-72,237-238,240-260,17-23,229-230`
- **## The leg ledger — replay, receipt, and how it is read (round 7, measured)** (921-932) — `tools/mutate-and-run.sh`, `corpus/knowledge/fleet-kill-rate-ledger.md`
- **### Using the ledger** (933-964) — `tools/mutate-and-run.sh:126-136,1273-1294,1364-1384,1104-1175,1159-1160,1384-1450,603-629,657-839,83-108,1384-1428`
- **### Reading a receipt — the discipline** (965-1009) — `plans/round-7.plan.md:11-15`, `corpus/knowledge/fleet-kill-rate-ledger.md`, `tools/mutate-and-run.sh`
- **### The tick and the pin read** (1021-1068) — `tools/mutate-and-run.sh` (external `../scripts/hyaku/jj-lane.sh` not read)
- **### The tick, executed** (1164-1211) — `tools/mutate-and-run.sh:511-518`, `corpus/knowledge/fleet-kill-rate-ledger.md:318-353`
- **### The receipt at this boundary** (1212-1229) — `tools/mutate-and-run.sh:733-791`, `corpus/knowledge/fleet-kill-rate-ledger.md:282`
- **## The operator's runbook and the six-leg regression (round 10, measured)** (1272-1280) — no file pointer in the section; internal `:1226-1228` followed → `corpus/knowledge/fleet-kill-rate-ledger.md` (`internal_pointer_follow`, trace `T51ExecRekey/trace-section-11-internal-follow.json`)
- **### The six-leg regression — usage and this round's receipt** (1302-1364) — `tools/mutate-and-run.sh:85-89,90-97,550-559,766,841,1132-1141,115-119,104-106,932-960,1488-1527,925-929,1218-1222,1226-1228,965-1008`, `corpus/knowledge/fleet-kill-rate-ledger.md:85-88,281`
- **### The map — where a reader enters, artifact by artifact** (1380-1395) — `corpus/knowledge/operator-runbook.md`, `corpus/knowledge/fleet-kill-rate-ledger.md`, `corpus/knowledge/service-limits.md`, `corpus/knowledge/service-optin-protocol.md`, `corpus/knowledge/fleet-suite-census.md`, `corpus/knowledge/service-standing-state.md`, `corpus/knowledge/closeout-r11.md`, `plans/round-11.plan.md`, `plans/completion-evidence.md`, `tools/mutate-and-run.sh`; records `LOG.md:316-317`, `SCORECARD.md`, `corpus/README.md`
- **### Gate/probe registry** (1499-1517) — `tools/repeat-control.py`, `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`, `SHONEN.md`, `corpus/lessons/round-1-verifier-spotcheck.md`, `.ufo/evidence/round-12/ControlGate/expected.json`, `.ufo/evidence/round-12/BashWitness/declaration.json`, `.ufo/waves/round-27/w1/Read25.md`
- **## Seventh recorded case and full-page cold-read — round 16** (1755-1806) — `corpus/knowledge/mutation-case-kumitate-round-gate.md`, `tools/mutate-and-run.sh`, `.ufo/evidence/round-16/measure.py`
- **### Round-16 gate/probe registry** (1807-1814) — `tools/mutate-and-run.sh`, `.ufo/evidence/round-16/measure.py`, `.ufo/evidence/round-16/coldread/assemble.py`, `.ufo/evidence/round-16/attribution/reattribute.py`
- **## Live-tree re-pin and entry-command monitor — round 17** (1815-1846) — `tools/evidence-disposition.py:368-390`, `tools/registry-check.py`, `tools/registry.json`, `tools/pin-disposition.py`, `corpus/lessons/round-16-verifier-spotcheck.md`, `.ufo/evidence/round-16/measure.py`, `.ufo/evidence/round-18/dispositions-before.json`, `.ufo/evidence/round-18/dispositions.json`; record `corpus/SOURCES.md:70-72`
- **### Round-17 gate/probe registry — re-pin and monitor** (1847-1855) — `tools/evidence-disposition.py`, `tools/registry-check.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, `.ufo/evidence/round-18/dispositions.json`, `.ufo/evidence/round-13/pin-manifest.json`
- **## Eighth recorded case — round 18** (1906-1925) — `corpus/knowledge/mutation-case-kumitate-sources-check.md`, `tools/mutate-and-run.sh`, `.ufo/evidence/round-18/sources-check/suite.txt`
- **### Round-26 gate/probe registry — report interop** (2133-2137) — `tools/mte-interop.py`

## 4. Controls (all observed; raw JSON in this directory)

- **The new entry is what credits** — from the green fixture, delete only the `### Gate/probe registry`
  re-key entry and commit: monitor 63/64, score 6, uncovered `### Gate/probe registry | no-ledger-entry`
  (`monitor-control-drop-entry.json`, commit `4c95277`). So the 44 → 64 restore is carried by the appended
  entries, not by anything else in the re-key commit.
- **The trace receipt is load-bearing** — point one re-key entry's `traces` at a non-existent receipt:
  monitor 63/64, score 6, `### Using the ledger |
  input-drift:tools/mutate-and-run.sh;trace-missing:…/traces/absent.json` (`monitor-control-trace-missing.json`,
  commit `5a67951`). Receipts must be committed with the ledger.
- **Determinism** — a second clone at the same CAND re-run produces the same 20 entries
  (`appended entries identical: True`), the same input maps, the same traced read stdout shas and the same
  order (`determinism-run.log`).
- **Refusals** (`refusal-controls.out`): usage exit 64; working-tree ledger ≠ ledger at CAND exit 1;
  nothing dropped (CAND=BASE clone) `no section lost credit …: nothing to re-key` exit 1; no reader seats
  for a target exit 1 with the heading named, fixture left clean.

## 5. Notes, risks, ordering for the L1

- **Sequencing (the one thing that can silently fail).** Credit is read from the ledger *at the measured
  revision*, so the re-key entries and their receipts must be committed at the revision whose monitor run
  counts. Round 49 did exactly that (`f181a96` "C1 re-key — seven ledger entries trace-bound…", then
  `fc5ac74` at candidate `54a52365`). Proposed order: content commit CAND (C2 runner + C3 registry row + C1
  README/SOURCES edits) → run `refresh.py LANE CAND readers.json` on a tree whose ledger equals CAND →
  commit ledger + `.ufo/evidence/round-51/coldread/rekey-<cand8>/` → monitor + `coldread-precheck.sh` at the
  new commit → deciding run at that revision.
- **Targets must be recomputed for the real CAND.** C1 appends to `corpus/README.md` and adds a SOURCES row;
  the instrument computes drops dynamically, and the record-via-blob reads keep the new entries free of the
  growing record files (fixture v2 shows the append adds no new drop and the re-key survives it).
- **The "target not credited at base" refusal cannot fire** by construction (targets = base-credited minus
  CAND-credited). It is an assertion, not a reachable branch; the reachable neighbours are "nothing dropped"
  and "target heading absent at CAND". Noted so a green run is not mistaken for having exercised it.
- **READERS_JSON for wave 2**: map each of the 20 headings to the seats that read it; `"*"` remains a
  documented fallback but a `*`-only map would put a fixture-style seat name in the ledger. Every target
  needs at least one seat or the run refuses.
- **Dependencies**: python3 + strace + git in the lane, the round-49 counter present at CAND
  (`.ufo/evidence/round-49/c1/measure.py` — it exists at base and at the freeze commit), and a `--shared`
  clone (object-store reads through alternates are `.git/` reads, which the monitor binds to REV). The
  instrument does not gate on the monitor's sha; it records it and measures with the bytes at CAND. In the
  fixture receipts that sha is `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb`, the round-49
  frozen `MONITOR_SHA` — the round-51 monitor is unchanged, so the measurement is the round's own score.
- **Risk (not observed)**: a section whose cited file C1/C2 moves or deletes would lose its pointer and the
  instrument would refuse on "cites no non-record lane file" rather than credit a phantom read. Both round-51
  claims only append.

## Retained evidence in this directory

`refresh.py`; `targets.json`; `monitor-summary.txt`; `monitor-cand-974d2d90.json` (44/64, score 6, the
pre-re-key state with raw per-section reasons); `monitor-after-0f28deeb.json` (64/64, score 8);
`monitor-control-drop-entry.json`; `monitor-control-trace-missing.json`; `refresh-receipts-v1.json`,
`refresh-receipts-v2.json` (per-section direct files, record blobs, internal follow, inputs, trace paths,
argv, stdout sha); `trace-section-11-internal-follow.json`; `precheck-v1.out`, `precheck-v2.out`;
`determinism-run.log`; `refusal-controls.out`.

## Summary

Built `.ufo/waves/round-51/w1/T51ExecRekey/refresh.py`: targets are computed by running the unchanged
round-21 monitor at BASE and CAND (never a hardcoded list), each target is re-read trace-bound in a
`--shared` clone at CAND (record files via `git cat-file blob`), and one `record`/`verified-record` ledger
entry per target is appended with seats from READERS_JSON and receipts under
`.ufo/evidence/round-51/coldread/rekey-<cand8>/`. Fixture at `84aa673` + runner comment + registry row:
monitor 64/44 score 6 → after the re-key commit 64/64 score 8, precheck lost=0; a second fixture with a
README append behaves the same. Deterministic across re-runs; controls show the entry and its trace are each
load-bearing (63/64 when either is removed). 20 sections are re-keyed (19 runner-input drift, 1
`no-ledger-entry`); headings and pointers are listed in §3 and in `targets.json` for the wave-2 readers. The
L1 must name the real seats, run on a tree whose ledger equals CAND, and commit the ledger and receipts at
the revision the monitor measures.
