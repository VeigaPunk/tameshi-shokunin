# The wave-artifact contract the orchestrator actually emits — and what a dead seat does to each reconcile row

Seat T73W1S12 (connector/contract). Read-only. This file is the acceptance
artifact for the seat; the scoped report is `.ufo/waves/round-73/w1/T73W1S12.md`.

## 0. Pins (read, never edited)

| object | pin |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/tameshi-shokunin` |
| lane HEAD while analysing | `06ce20f75b7fa793a670691efc9c090303420d46` (the C1 instrument bytes were stable across it) |
| `tools/wave-reconcile.py` | sha256 `63833dd1f6a770a27c2ee3b75e4d6d6be78d92a006281046c9ef653090838522`, last touched by `8f7ff279` ("C1 hardening from seat T73W1S03") |
| `tools/wave-reconcile.json` | sha256 `a1ce65e13456b21c94123c8e1e9c8b6091bcb1055d1f5359f54a6bda753f3b87`, last touched by `8f7ff279` |
| wave artifacts | round-72 wave read from git objects at `a3dd35742eee608d1205843dacebc461b4242b9e` |
| round-72 report | fleet repo `/home/vgpnk/Projects/shokunin`, blob `3664a6d30051410c3d2bb8c32926d13e284a5118:.ufo/reports/round-72/tameshi.md` |
| planner/validator | `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs` (107,309 B, 2,071 lines) |
| dispatcher | `/home/vgpnk/Projects/shokunin/scripts/hyaku/inline-dispatcher.py` (394 lines) |

**Moving target, recorded honestly.** The C1 instrument was committed at
`fddbb667` (22:01) and hardened at `8f7ff279` (22:08) *while this seat was
reading it*: `_record_claim` was added so every row kind binds its `record`
block, and the two `roles` rows lost their `printed` field (it was inert on
those rows at `fddbb667`; forcing it in the span would have failed the sweep).
All claims below are against the current bytes (hashes above); §7.4 keeps the
pre-fix receipt so the delta is visible.

## 1. Artifacts actually emitted

| artifact | writer | shape | carries |
|---|---|---|---|
| `<wave>.ready` | L1 (authored) | `{lane, round, wave, dispatch, l1}` | the dispatch request; r72: 12-name wave, dispatch path, `TameshiR72` |
| `<wave>.ready.partial` | dispatcher `register()` | `{seat: handle-id}` | seats spawned so far while a wave fills; **deleted** on full registration |
| `<wave>.ready.dispatched` | dispatcher `register()` | line 1 timestamp, line 2 `{seat: handle-id}` | the full spawn map; written **only** when `len(mine) == len(tasks)` |
| `<wave>-spec.json` | L1 (authored; validator input) | `{wave, maxLanes, reportDir, context, template, items:[{name, role, item, axes,…}]}` | the plan the validator checks |
| `<wave>-dispatch.json` | validator `run` output, committed by the L1 | `ufo-swarm-wave-dispatch-v1`: `counts{spawn,resume,total}`, `registry{path}`, `taskCall{context, tasks:[{name, agent, task}]}`, `resumeSends[]` | the executable payload |
| `<wave>/swarm-registry.json` | validator `run` (persist) | `ufo-swarm-registry-v1`: `{schema, wave, createdAt, updatedAt, reportDir?, priorRegistries?, members{name:{kind, agentId, role, item, axes?, milestone?, modelAlias?, card?, member?}}}` | identity/role/item/judgment binding; **cumulative** across re-runs |
| `<wave>-results.json` | dispatcher `finalize()` | `{lane, round, wave, seats, results:[{name, agent, output, note}]}` | one record per dispatched spawn seat; written **once**, when no seat is live |
| `<wave>/<Seat>.md` | each seat | markdown | the seat report (what `seat_reports` counts) |

Seat dirs (`T72W1S01/…`) and `swarm-registry.json` are not `.md`, so they do not
enter the seat-report count. At `a3dd3574` the top level of
`.ufo/waves/round-72/w1/` is exactly `swarm-registry.json` + 12 `T72W1S*.md`
(§7.1).

## 2. Field-by-field answers

### 2.1 What exactly does `seats` count?

`finalize()` builds one record per name in `w['names']` and writes
`'seats': len(res)` (`inline-dispatcher.py:288-296`). `w['names']` is
`[t['name'] for t in d['taskCall']['tasks']]` (`:226`, `:268`). The validator
emits `taskCall.tasks` from **spawn lanes only** (`ufo-swarm-wave.mjs:1458-1466`);
resume lanes travel in `resumeSends` and `counts.total = spawn + resume`
(`:1370`).

Therefore:

> `seats` = the number of **dispatched spawn lanes** (`taskCall.tasks`), i.e.
> the wave's spawn roster. It is not live seats, not settled seats, not seat
> reports, and not total lanes (resume lanes are excluded by construction).

Evidence: the census joins every results file to its dispatch and finds
`seats == len(results) == len(dispatch.taskCall.tasks)` in **351/351** joined
files, with `results` names equal to dispatch task names in **351/351**, and
**0** waves carrying `resumeSends` (§7.2). Round 72: `seats` 12, 12 records,
dispatch `counts.spawn` 12, `counts.resume` 0 (§7.1).

The round-60 counterexample is sharper: `w1.ready.partial` shows only
`T60W1S01`, `T60W1S02` ever spawned, `.ready.dispatched` second line is `{}`,
yet the settled file says `seats: 32` with 30 `dead_or_never_spawned` — the
field is the dispatch width, not execution (§7.3).

Because `seats` and `len(results)` are emitted from the same list, the `seats`
row's two artifact sides are equal by construction. Its only independent side
is the record's `printed` claim (`wave-reconcile.py:208-218`).

### 2.2 Is a dead seat a record?

**A spawned seat that dies: yes.** `finalize()` iterates `w['names']`, not the
live set, so the record is written regardless of liveness. `seat_output()`
(`:279-286`) returns the handle's text (`str(h.output())[:20000]`) whenever a
handle exists; it returns `None` only for a missing/`_Spawned` handle. The
`note` is set only when `output is None` (`:294-295`), i.e. only when the
**handle** was lost (kernel restart / adopted wave), never because the seat
died.

**A seat that never spawned: normally no record at all.** `register()` writes
`.dispatched` and registers the wave only when every task has been spawned
(`:262-273`), and `finalize()` only runs for registered waves (`:326-330`). A
wave stuck filling leaves `.partial` and no `-results.json`. A never-spawned
seat becomes a record only when a human/hand-settler writes one — exactly what
round 60 did (`dead_or_never_spawned: 30`, per-record note "operator usage cap
… seat never spawned").

**A resume seat: never in `results`.** Resume lanes are `resumeSends`, not
`taskCall.tasks`, so the dispatcher never iterates them. (Contract from code;
**not observed**: 0 of 3xx results files and 0 of 45,786 registry members are
resume rows.)

Corpus proof that dead/failed seats are records without any outcome marker:
1,556 records with `output: null` (all accompanied by a note: 1,161 "kernel
restarted", 103 "never spawned", 292 other death/exit prose), 118 records with
`output: ""` and **no** note, 1,708 non-null notes in total (152 also carrying
output text) (§7.2).

### 2.3 Can `results[]` carry a record whose `output` is empty or a note?

Yes. Both, and more:

| shape | observed count (live census) |
|---|---|
| `output` empty string (note `null`) | 118 |
| `output` null (note always non-null) | 1,556 |
| non-null `note` | 1,708 (152 of them with non-null output too) |
| `output` exactly 20,000 chars (= the `[:20000]` truncation) | 12 |
| `output` string `<output unavailable: …>` (handle raised) | 2 |

`output` is therefore **not** the seat's complete text and **not** an outcome:
it is a ≤20,000-char slice, it can be `""`, `null`, or an error string.
`note` is prose, written only for lost handles plus hand edits.

Record key sets are not one schema (351 parsed files): canonical
`{name, agent, note, output}` (332 files), older `{name, agent, id, output}` (9
files, no `note`, has an `id`), hand-augmented `+report_file` (6) and
`+report_file_present` (2). One file (kaidoku r50-w4) has no `results` list at
all. The reconciler's `_results` requires only `seats` int + `results` list and
`_agents` requires `agent` to be a string (`wave-reconcile.py:185-206`); its own
selftest fixture records carry only `{name, agent}` — output/note are outside
the measured contract.

### 2.4 What does `swarm-registry.json` carry that `results.json` does not?

Per member (keyed by seat name, the join key):

- `kind` (`spawn` | `resume`) — results cannot distinguish a resumed lane;
- `agentId` — the hub handle (`KaidokuR14.InstalledGoGate` shape) so a transcript
  can be named; `results` has **no id field at all**;
- `role` — the taxonomy role even when the dispatch identity is a generated
  agent-card name (validator `agent: lane.card ?? lane.role`, `:1288`);
- `item` — the full item text (the assignment authority);
- `axes`, `milestone`, `modelAlias`, `card`, `member` (resume owner) — the
  judgment/routing binding;
- document-level `schema`, `wave`, `reportDir`, `createdAt`, `updatedAt`,
  optional `priorRegistries`.

`results.json` carries none of these; it carries `output`/`note`, which the
registry never carries.

Two traps:

1. **The registry is cumulative, not per-wave.** `persistWaveRegistry` merges
   `existing ∪ plan.registry.members` and never prunes (`ufo-swarm-wave.mjs:1676`).
   Kotoba round-73: registry 55 members, spec/dispatch/results 36 — 19 extras
   with `item: null` from an earlier run of the same wave path (§7.5).
2. **The current orchestration never fills `agentId`.** `record` exists
   (`ufo-swarm-wave.mjs:1793`) but the inline dispatcher never calls it; round
   72's registry has `agentId: null` on all 12 members, and 0 of 281 registries
   that sit beside a results artifact have a filled id. Fleet-wide 335 of 974
   registry documents have at least one filled id, from older/manual runs.

### 2.5 What does the dispatcher do when a seat dies?

- Liveness is per handle id; `tick()` counts `nlive` per wave and calls
  `finalize()` only when `nlive == 0` (`inline-dispatcher.py:326-330`).
- **No respawn, no replacement, no per-seat status, no early finalize.** A dead
  seat simply stops being live; the remaining seats run to completion; the
  artifact is written once at the end with the dead seat's record.
- If the **orchestrator kernel** was lost, `adopt()`/`bootstrap()` rebuild
  handles as `_Spawned(job-id)`, so every record is written with
  `output: null` and the "orchestrator kernel restarted mid-wave" note (1,161
  corpus records).
- If the **L1** is dead but the wave is registered, finalization still happens;
  the `agent://` WAVE-DONE message fails and is logged (`notify-failed`).
- If the wave never fully fills, there is no results artifact (see 2.2).
- The validator is not a dispatcher: it plans, emits the dispatch payload and
  persists the registry; it has no death/status concept and does not write
  `-results.json`.

## 3. Dead-seat impact table — the six committed rows

One dead **spawn** seat on a canonical artifact (the r72 shape). A dead seat
keeps its record; the record carries its dispatch `agent` and either its
partial text, an empty string, or (lost-handle) `null` + note.

| row (kind) | dead-seat impact |
|---|---|
| `r72-report-seats` (`seats`) | **None to the measured value.** `printed=12 seats=12 records=12` is unchanged: the dead seat is still a record and still in `seats`. Only a hand-trimmed artifact (record dropped and `seats` edited) moves it. |
| `r72-report-seatreports` (`seat_reports`) | **The only kind that can move.** If the dead seat wrote no report, `files` drops by one; the row then measures the death as a report-count effect. With r72's bytes it is 12; a wave with one dead, report-less seat reads 11, so a claim of "12 reports" drifts and a claim of "11" meets. |
| `r72-plan-seats` (`seats`) | **None.** Same derivation as row 1; the plan's "12 seats" is a roster claim. |
| `r72-spec-roles` (`roles`) | **None.** The dead seat's `agent` is copied from the dispatch map, so the multiset is unchanged. (Undefined only on artifact variants whose records carry a null/absent `agent` — 38 such records exist in hand-settled files; `_agents` then raises `results-agent-absent`, exit 2.) |
| `r72-plan-roles` (`roles`) | **None.** Same measured side; r72's red arm is a plan-declared `labrat` vs an executed `revenger`, not death. |
| `r72-attack-share` (`attack_share`) | **None — and that is the semantic gap.** A dead attack seat still counts in both numerator and denominator. Fixture proof: 12 seats, 2 reviewers, one reviewer dead; `attack=4/12=33.3%` meets `floor=30`, while the live-only share is `3/12=25%` and would drift. The row measures composition, not executed attack work. |

Kind-level summary (what the seat asked for as four kinds):

| kind | dead seat effect | what it actually measures |
|---|---|---|
| `seats` | none | dispatched spawn records (roster width); `seats` and `len(records)` are the same list |
| `seat_reports` | may lower the file count | committed top-level `.md` files in the wave dir (not necessarily one per seat) |
| `roles` | none | multiset of `results[].agent` (dispatch identity: role, or a card name under `modelAlias`) |
| `attack_share` | none | named roles among results records ÷ number of records (roster composition) |

## 4. Well-definedness of the manifest as committed

Run at the pinned bytes (§7.6): `WAVE_RECONCILE: rows=6 met=6 unexpected=0`,
exit 0; selftest `12/12 pass`, exit 0. Both r72 red arms read
`expect=drift measured=drift ok`.

- All six rows are **well-defined against the committed round-72 artifact**:
  every artifact the rows name exists at its rev, decodes as UTF-8 JSON, and
  yields the measured values.
- **No row is *undefined* on a wave with a dead spawn seat.** The artifact has
  no death field, so death cannot make a row uncomputable; it makes three of
  the four kinds (seats/roles/attack_share) **blind** to death, and the fourth
  (seat_reports) sensitive only through a missing file.
- The semantics that **are** underdefined by death are the nouns:
  `seats`/`attack_share` read as "the wave executed N seats / N% attack" while
  measuring the dispatched roster. A dead seat silently keeps both numbers.
- Genuinely undefined (setup exit 2) cases, none caused by death alone:
  * no `-results.json` (wave never fully registered → never finalized);
  * a results row with null/non-string `agent` (hand-settled variants) for
    `roles`/`attack_share`;
  * a results file with no `results` list (kaidoku r50-w4);
  * a resume-only lane (excluded from `seats` by construction, so a
    "total lanes" claim is not measurable against `seats`).
- The `seats` row is **self-referential**: `printed == seats == len(records)`,
  where `seats` and `len(records)` are the same emitter expression. It cannot
  detect a results artifact whose roster was trimmed *and* whose `seats` field
  was trimmed with it — fixture wave B proves this: dispatch 12 tasks, results
  11 records/`seats: 11`, printed "11 seats" → `printed=11 seats=11 records=11`,
  meet (§7.7).
- The dispatch artifact is never read by the reconciler:
  `grep -c dispatch tools/wave-reconcile.py` → `0` (§7.7).

## 5. Proposal (proposal only; the manifest was not edited)

### P1 — row-level `population` field

Add one optional row field:

```json
"population": "results" | "dispatch" | "settled"
```

- **absent / `"results"`** — today's derivation (default; the six committed
  rows stay byte-identical in meaning and measured value).
- **`"dispatch"`** — the roster is the wave's dispatch artifact
  (`wave.dispatch` at `wave.rev`, `taskCall.tasks[]`); `seats` is compared to
  `len(tasks)` and, when present, `counts.spawn`; `resumeSends` is excluded by
  definition; for `roles`, a task's `agent` is used when it is a taxonomy role,
  otherwise the registry member's `role` (the only artifact that stores the
  role when `agent` is a card name). This makes the row independent of the
  artifact's self-report and catches a trimmed results file.
- **`"settled"`** — the roster is the records with an explicit boolean
  `settled: true` (or `state: "settled"`). If any record in the artifact lacks
  that field, the row is a setup error (exit 2, named
  `outcome-absent:<row>`), never a silent meet. No fleet artifact carries the
  field today (0 of 351 parsable results files; 0 of 14,610 records), so this value is
  deliberately unpayable until the producer emits it — the claim is refused
  rather than misread.

Why a field, not a new kind: the three populations feed the same three
existing kinds; a new kind would duplicate each kind × population and would
still be unfeedable for `settled`. `seat_reports` needs no population (it is a
file count), but it should name the expected files (`<name>.md` for the
dispatch names) instead of "any top-level `.md`".

Expected effect, measured with an independent oracle over the committed r72
bytes and the fixture (§7.8):

- r72: dispatch = 12 tasks, roles identical, `attack=3/12=25.0%` → adding
  `population:"dispatch"` leaves every measured value identical.
- fixture wave B (dispatch 12, results 11): `population:"dispatch"` seats →
  `printed=11` vs `12` **drift**; roles → 12 dispatch roles vs 11 declared
  **drift**; `population:"results"` seats → meet (as today). Note: attack at
  floor 25 would still meet at `4/12=33.3%`, so the attack row is not a
  roster-trim detector at that floor.
- `population:"settled"` on r72 or the fixture → **exit 2** (0 records carry
  `settled`).

### Falsifier (runnable once P1 exists)

P1 is **falsified** if any of these fails:

1. With the field absent, the committed six-row sweep is byte-identical to
   today: `WAVE_RECONCILE: rows=6 met=6 unexpected=0`, exit 0.
2. With `population:"dispatch"` added to r72's six rows, every measured value
   is unchanged (`printed=12 seats=12 records=12`; roles identical;
   `attack=3/12=25.0%`; `printed=11 files=12`).
3. On the deadseat fixture's wave B (dispatch 12 tasks, results 11 records,
   `seats: 11`), a seats row with `population:"dispatch"` reads **drift**
   while the same row with `population:"results"` reads **meet**.
4. A `population:"settled"` row over any current artifact (no per-record
   `settled`) exits **2**, not 0.

If (3) reads meet or (4) reads meet, the field is inert and P1 is refuted.

## 6. What a dead seat does *not* do

- It does not remove its record, change `seats`, change the role multiset, or
  lower `attack_share`.
- It does not cause a retry, a replacement handle, or a status field.
- It does not, by itself, make any of the six rows undefined; the artifact
  would need an explicit outcome field for a row to measure death at all.

## 7. Evidence chain (commands and pasted output)

### 7.1 Round-72 artifacts at the artifact rev

```
$ git -C tameshi-shokunin ls-tree -r --name-only a3dd3574 -- .ufo/waves/round-72/w1 \
    | sed 's#^\.ufo/waves/round-72/w1/##' | awk -F/ 'NF==1' | sort
swarm-registry.json
T72W1S01.md … T72W1S12.md          (12 files)
```

```
$ git -C tameshi-shokunin cat-file blob a3dd3574:.ufo/waves/round-72/w1-results.json \
    | python3 -I -X utf8 -c "import json,sys; d=json.load(sys.stdin); print('seats',d['seats'],'n',len(d['results']),'empty',sum(1 for r in d['results'] if not (r.get('output') or '').strip()),'notes',sum(1 for r in d['results'] if r.get('note')),'agents',sorted({r['agent'] for r in d['results']}))"
seats 12 n 12 empty 0 notes 0 agents ['connector','critic','executor','mutation-tester','revenger','reviewer','scout','scribe','sentinel']
```

```
$ cat .ufo/waves/round-72/w1.ready
{"lane":"tameshi","round":72,"wave":"w1","dispatch":"/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-72/w1-dispatch.json","l1":"TameshiR72"}
$ cat .ufo/waves/round-72/w1.ready.dispatched
2026-11-03T21:21:33
{"T72W1S01": "T72W1S01", "T72W1S02": "T72W1S02", "T72W1S03": "T72W1S03", "T72W1S04": "T72W1S04", "T72W1S05": "T72W1S05", "T72W1S06": "T72W1S06", "T72W1S07": "T72W1S07", "T72W1S08": "T72W1S08", "T72W1S09": "T72W1S09", "T72W1S10": "T72W1S10", "T72W1S11": "T72W1S11", "T72W1S12": "T72W1S12"}
```

Dispatch JSON: `counts={"spawn":12,"resume":0,"total":12}`,
`taskCall.tasks` 12, `resumeSends` 0, `schema=ufo-swarm-wave-dispatch-v1`.
Registry: 12 members, all `kind:"spawn"`, all `agentId:null`, `role`/`item`/
`axes` present; document keys `createdAt, members, reportDir, schema, updatedAt,
wave` (no `priorRegistries`).

Report blob `3664a6d3:.ufo/reports/round-72/tameshi.md` line 56:

```
- **The wave** (see "Wave" below): 12 seats, 11 reports; three seats found real
```

### 7.2 Fleet-wide census (`census.py`, shipped beside this file)

```
$ python3 -I -X utf8 .ufo/waves/round-73/w1/T73W1S12/census.py
RESULTS files=352 parsed=351 bad=1 joined_to_dispatch=351
SEATS seats==len(tasks)==len(results): 351/351
NAMES results names == dispatch tasks: 351/351
AGENT results.agent == dispatch.agent mismatches: 102
RESUME waves with resumeSends observed: 0
OUTPUT empty-string=118 null=1556 truncated-at-20000=12 unavailable-string=2
NOTES non-null=1708 (with non-null output=152)
NOTE-KINDS {'dead': 1, 'kernel restarted': 1161, 'killed': 72, 'never spawned': 103, 'no output': 72}
REGISTRY docs=974 bad=1 members=45786 kinds={'spawn': 45786} docs_with_any_agentId=335
```

(The 102 `agent` mismatches are hand-settled artifacts: 38 records with
`agent:null`, 32 with `agent:"task"`, 32 kasegi rerun rows; every
dispatcher-emitted artifact echoes the dispatch `agent` exactly. The corpus is
live — file counts move between runs; the 351/351 invariant held in every run.)

Null-output provenance (same corpus, focused pass):

```
output literally "None": 0
null output with note: 1556 without note: 0
note classes: {'restart': 1161, 'other': 292, 'never-spawned': 103}
files with empty outputs: 18
```

### 7.3 Round-60 never-spawned / hand-settled counterexample

```
$ ls .ufo/waves/round-60/
spec-w1.json  w1-dispatch.json  w1-results.json  w1-run.stderr  w1.ready  w1.ready.dispatched  w1.ready.partial
$ cat .ufo/waves/round-60/w1.ready.partial
{"T60W1S01": "T60W1S01", "T60W1S02": "T60W1S02"}
$ cat .ufo/waves/round-60/w1.ready.dispatched
2026-10-30T15:51:50
{}
$ python3 -I -X utf8 -c "import json;d=json.load(open('.ufo/waves/round-60/w1-results.json'));print(sorted(d));print(d['seats'],d.get('settled'),d.get('dead_or_never_spawned'),len(d['results']))"
['dead_or_never_spawned','lane','results','round','seats','settled','wave']
32 2 30 32
```

Sample dead record and live record:

```
{"name":"T60W1S03","agent":"task","note":"operator usage cap 2026-10-30: fleet capped at 32 concurrent jobs; seat never spawned (tranche fill halted)","output":null}
{"name":"T60W1S01","agent":"task","note":null,"output":"SEAT SETTLED: …"}
```

### 7.4 Pre-fix record binding (delta `fddbb667` → `8f7ff279`)

At the C1 commit `fddbb667`, a manifest whose `roles` and `attack_share`
record spans were replaced with `NOT-IN-RECORD-AT-ALL` still swept clean:

```
$ python3 -I -X utf8 prefx-tool.py --repo tameshi-shokunin \
    --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest prefx-manifest-ctrl.json
WAVE_ROW r72-spec-roles kind=roles … measured=meet ok | …
WAVE_ROW r72-attack-share kind=attack_share … measured=meet ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=6 met=6 unexpected=0          exit=0
```

At the current bytes the same forgery is refused:

```
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=… \
    --manifest /fast/scratch/…/ctrl-roles-printed.json
WAVE_RECONCILE error=setup:span-not-in-record:r72-spec-roles:.ufo/waves/round-72/w1-spec.json   exit=2
$ … --manifest ctrl-attack-printed.json
WAVE_RECONCILE error=setup:span-not-in-record:r72-attack-share:.ufo/reports/round-72/tameshi.md   exit=2
$ … --manifest ctrl-seats-printed.json
WAVE_RECONCILE error=setup:printed-not-in-span:r72-report-seats   exit=2
```

### 7.5 Registry divergence (kotoba round-73)

```
registry keys ['createdAt','members','reportDir','schema','updatedAt','wave']
spec items 36   dispatch tasks 36   registry members 55
registry - spec 19   spec - registry 0
member sample for an extra:
 {"kind":"spawn","agentId":null,"role":"connector","item":null,"axes":["coverage","depth"],"milestone":"Round-73 wave 1 …"}
```

`persistWaveRegistry` merges `existing ∪ plan.members` (validator `:1676`), so
the registry keeps members from an earlier 55-item run of the same wave path.

### 7.6 Frozen counters at the pinned bytes

```
$ sha256sum tools/wave-reconcile.py tools/wave-reconcile.json
63833dd1f6a770a27c2ee3b75e4d6d6be78d92a006281046c9ef653090838522  tools/wave-reconcile.py
a1ce65e13456b21c94123c8e1e9c8b6091bcb1055d1f5359f54a6bda753f3b87  tools/wave-reconcile.json
$ python3 -I -X utf8 tools/wave-reconcile.py --selftest
SELFTEST arm1-seats-meet                      ok (got=meet want=meet)
… (12 arms, all ok) …
WAVE_RECONCILE_SELFTEST: 12/12 pass                     exit=0
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . \
    --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | declared=… measured=…
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=drift ok | declared={…"labrat":1…} measured={…"revenger":1…}
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=6 met=6 unexpected=0               exit=0
```

### 7.7 Dead-seat fixture (reproducible script shipped beside this file)

```
$ bash .ufo/waves/round-73/w1/T73W1S12/deadseat-fixture.sh /fast/scratch/…/rerun
FIXTURE_REV=431b34ad536500dcd7cc4da6b2f61bdb34d10ce4
WAVE_ROW A-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW A-seatreports-11 kind=seat_reports expect=meet measured=meet ok | printed=11 files=11
WAVE_ROW A-seatreports-12 kind=seat_reports expect=drift measured=drift ok | printed=12 files=11
WAVE_ROW A-roles-spec kind=roles expect=meet measured=meet ok | declared={reviewer:2,…} measured={reviewer:2,…}
WAVE_ROW A-roles-plan kind=roles expect=meet measured=meet ok | declared=… measured=…
WAVE_ROW A-attack-floor30 kind=attack_share expect=meet measured=meet ok | attack=4/12=33.3% floor=30.0%
WAVE_ROW B-seats kind=seats expect=meet measured=meet ok | printed=11 seats=11 records=11
WAVE_ROW B-roles-spec kind=roles expect=meet measured=meet ok | declared=… measured=…
WAVE_ROW B-attack-floor25 kind=attack_share expect=meet measured=meet ok | attack=3/11=27.3% floor=25.0%
WAVE_RECONCILE: rows=9 met=9 unexpected=0                exit=0
```

Wave A's dead record is `{"name":"T07","agent":"reviewer","output":null,
"note":"seat died before delivering output; no report file"}`; its attack
`4/12=33.3%` meets floor 30 only because the dead reviewer is still counted
(live-only `3/12=25%`). Wave B has the same 12-task dispatch but an 11-record,
11-seat results artifact: all three rows still meet.

```
$ grep -c dispatch tools/wave-reconcile.py
0
```

### 7.8 Proposed-population oracle (independent of the tool)

```
== committed r72 wave
results(records)   seats=12 attack=3/12=25.0% roles={connector:1,critic:1,executor:3,mutation-tester:1,revenger:1,reviewer:1,scout:1,scribe:2,sentinel:1}
dispatch(tasks)    seats=12 attack=3/12=25.0% roles={…identical…}
records carrying a settled field: 0 of 12
== fixture
waveA results      seats=12 attack=4/12=33.3%
waveA dispatch     seats=12 attack=4/12=33.3%
waveB results      seats=11 attack=3/11=27.3%  roles={reviewer:1,…}
waveB dispatch     seats=12 attack=4/12=33.3%  roles={reviewer:2,…}
waveA/B settled field on records: 0 of 12 / 0 of 11
```

## 8. Honest negatives

- No wave in the fleet corpus carries `resumeSends` and no registry member is a
  resume row, so the resume-lane exclusions in §2.1/2.2 are read from the
  validator and dispatcher code, not observed in artifacts.
- The only observed dead/never-spawned wave with explicit outcome fields
  (round 60) is a hand-settled artifact with non-canonical top-level keys; the
  dispatcher itself never emits `settled`/`dead_or_never_spawned`.
- The fixture's death is synthetic; round 72 itself had 12/12 records with
  non-empty output and no notes, so the r72 red arms are count/role drift, not
  a dead-seat measurement.
- The corpus is live: 352 results files crossed the census (351 parsable,
  14,610 records; 350 at the first pass). The 351/351 seat/name invariant held
  in every pass, but the exact file counts in §7.2 are a snapshot.
- The C1 instrument changed under this seat mid-read (`fddbb667` →
  `8f7ff279`); §7.4 records the pre-fix hole rather than pretending the frozen
  bytes always bound every row.
- Not run: no attempt to construct a real dispatcher wave with a dead seat (the
  fleet is live and this seat may not spawn seats or write outside its scope).
