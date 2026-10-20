# S12K02Holes — scout, R17-CMD-BIND (K02 holes 1–7, receipt/command binding)

Seat: TameshiR18.S12K02Holes (leaf scout, read-only on lane bytes).
Rev measured: `183f87b899e6cae46be98d251cbc87fb5118f6ca`.
Scratch: `/tmp/tameshi-r18w1-S12K02Holes-ybn9IM` (synthetic `mini` repo + a
`--shared` clone `lane-clone`; every git write was inside those /tmp repos,
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`).
Tools installed: none.

Committed bytes read (from the rev, not the worktree):

| file | lines | sha256 |
|---|---:|---|
| `.ufo/evidence/round-17/measure.py` | 1602 | `d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3` |
| `.ufo/evidence/round-17/coldread/assemble.py` | 1942 | `8bcce2eafe37e5ca11e1a145e4c6c826071eca55917ddb464a1b6da190f6ccd1` |
| `.ufo/evidence/round-17/coldread/bucket-commands.json` | 1940 | `39b9392afb5d230750683e6ed5b1ce7ed74079a150318f136421293930328bf5` |

Axes attacked: **soundness** (a credit must track what the bucket requires),
**provenance** (`read_rev`/traces/commands describe what was run),
**stability** (no bucket uncredited by files it does not depend on).

Calibration commands used throughout (all exits recorded):

- `python3 .ufo/evidence/round-17/measure.py --selftest` → exit 0,
  `MEASURE_SELFTEST: 94/94 pass` (scratch `/tmp/tameshi-r17-MeasureV2-bm7282zi`).
- `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest` → exit 0,
  `SELFTEST: all checks passed`.
- Clone at the rev, measure with no `--repo`:
  `covered 58 / 58 box3 True restraint 8 overrides False trace_gate strict`.
- Entry recount with the module's own `entry_reason(repo, rev, e, True)`:
  `entries 68 passing 58 nonpassing 10` (5×`verdict:wrong-expectation`,
  5×`input-drift`), matching the spot-check §3 count.

## Hole status at 183f87b

### Hole 1 — self-reported inputs, no binding to traces or to the section's commands — **partly**

What closed (input corroboration):

- Entry with `commands_executed_count>0` must list ≥1 committed trace
  (`measure.py:368-381`, `traces-unrecorded` in strict mode;
  `assemble.py:596-600`, `trace-receipt-missing`).
- Receipt must be a blob at REV with schema `tameshi-trace-inputs-v1`; its
  `inputs` keys must be present in the entry's inputs with equal sha
  (`measure.py:388-412`, `trace-input-unrecorded` / `trace-input-drift`).
- Assembler additionally requires receipt `rev == report.read_rev`
  (`assemble.py:456-460`, demo rejection below).

What stays open (command binding):

- `argv` is never compared to anything. `grep -n argv measure.py assemble.py`
  yields only the CLI `main(argv=…)` and one synthetic fixture
  (`measure.py:773`); `assemble.py` has no `argv` occurrence at all.
- The declared command list is destroyed at assembly: the report's
  `commands_executed` list (`assemble.py:16`) is reduced to
  `commands_executed_count = sum(len(o["commands_executed"]))`
  (`assemble.py:885-886`); ledger entries carry no `commands_executed` field
  (verified: `entries have commands_executed list: False`).
- `measure.py` — the cited-score consumer — does not check receipt `rev` or
  entry `read_rev` at all (`trace_reason` `measure.py:368-424` reads only
  schema/inputs/live_lane_reads/external).

Failure-backed demos (synthetic `mini` at `/tmp/...`, commits
`ab699ac…`, `d380625…`, `53ce6b7…`):

1. Pure-prose bucket ("No commands are declared in this section at all.") +
   `class=instruction`, `verdict=executed-ok`, `commands_executed_count=1`,
   one receipt whose `argv=["cat","PROVINCE.md"]`, entry `read_rev="0"*40`,
   receipt `rev="f"*40` → **credited** (`measure.py --repo mini --rev d380625`
   exit 0; `[(5, True, 'credited')]`).
2. `assemble.py` accepted a report declaring
   `commands_executed=["echo totally-unrelated"]` with the same `cat` receipt
   (`rejected reports: none`; entry `cmd_count 1`, `traces 1`).
3. One receipt covers an arbitrary declared count: report with five commands
   and one receipt → accepted, `cmd_count 5 traces 1`; the resulting committed
   ledger is **credited** by `measure.py` (`[(5, True, 'credited')]`).

Real-data corroboration at the rev (tip ledger, credited entries):

| start | heading | fenced commands | receipts (first two argv, abbreviated) |
|---:|---|---:|---|
| 17 | Standing rules | 0 | `bash -c nl -ba corpus/knowledge/…` ; `sha256sum corpus/knowledge/…` |
| 94 | The mutation bar | 0 | `bash corpus/checklist-run.sh --selftest` ; `bash corpus/claim-ledger.sh --selftest` |
| 1010 | Re-sweep cadence | 0 | `sed -n '230,240p' corpus/knowledge/fleet-kill-rate-ledger.md` |
| 1436 | Where to enter | 0 | `sed -n '35,64p' …/operator-runbook.md` |

The same pattern X16 found on the round-16 ledger (six pure-prose instruction
buckets, `.ufo/waves/round-17/w1/X16BucketCommands.md`) survives at the tip:
credit rests on "the seat ran *something* and traced files", not on the
section's commands.

### Hole 2 — class dodge — **partly**

- The specific zero-command dodge is closed: `entry_reason` returns
  `commands-unrecorded` for any entry with count 0, class-independent
  (`measure.py:516-517`); selftest `record-zero-cmd-commands-unrecorded`
  (`measure.py:1050-1074`).
- Class is still the seat's declaration checked against verdict strings only
  (`entry_credit_reason`, `measure.py:472-507`); the mechanical `class` in
  `bucket-commands.json` is never consulted. A `record` entry with count>0 and
  one receipt credits a pure-prose bucket (demo 1 above).
- Census at the census rev (`bucket-commands.json`): 23/54 class
  disagreements — 13 `executes_commands=yes`/`record` (starts 314, 899, 921,
  1092, 1164, 1212, 1302, 1380, 1396, 1499, 1597, 1609, 1707) and 10
  `no`/`instruction` (17, 94, 131, 246, 466, 883, 965, 1010, 1069, 1436).
- G5's "class-independent gate" is true only of the commands/input/trace gates;
  the class *credit* rule is still self-declared.

### Hole 3 — `--inputs-overlay` overrides any field — **closed**

- `OVERLAY_FIELDS = {start, skill_sha256, heading, inputs, read_rev, traces}`
  (`measure.py:134-136`); any other item key exits 2
  (`measure.py:1574-1582`); selftest `overlay-field-forbidden`
  (`measure.py:1358-1367`).
- Demo: overlay `{"start":5,...,"verdict":"executed-ok","class":"instruction"}`
  → exit 2, `{"error":"overlay-field-forbidden","fields":["class","verdict"]}`.
- Residual (accepted by G6, not a hole): `inputs`/`traces` may still be
  overwritten, but the run reports `overrides_used: true`, `ledger_source:
  file`, and the cited tip run is `overrides False`, `trace_gate strict`.
  Overlay items are keyed by `(skill_sha256,start)`, so they cannot retarget a
  bucket to another section sha.

### Hole 4 — directory/tree keys — **closed**

- Input bytes go only through `ls_tree_mode` + `cat_file_blob`
  (`measure.py:325-356`); mode must be `100644|100755`, else
  `input-not-blob` (`measure.py:190-203` reject tree mode `040000`).
- Demo: `inputs={"tools": <sha256 of `git show REV:tools`>}` → exit 0,
  `input-not-blob:tools` (not credited). The old `git show REV:path`-based
  hole is gone.

### Hole 5 — reads of the live lane from a "clone" run — **partly**

Closed:

- Every git call scrubs inherited `GIT_*` (`measure.py:140`), load-bearing:
  with `GIT_DIR=<canary>/.git GIT_WORK_TREE=<canary>` exported, the landed tool
  measures `mini` (exit 0, `revision d380625…`); a scratch mutant with
  `GIT_ENV = dict(os.environ)` exits 2 `rev-missing` for the same call.
- `--repo` defaults to the git toplevel containing the script
  (`default_repo`, `measure.py:1450-1458`), so a clone measures itself; the
  no-`--repo` clone run above measured the clone's rev.
- Receipt `live_lane_reads`/`external` keys under the lane root must be bound:
  `.git/` read or regular blob whose sha equals the recorded digest at REV
  (`measure.py:413-423`, `427-451`); `assemble.py:464-472` rejects unbound
  live reads and `456-460` rejects a receipt rev that is not `read_rev`.
  Demo: live-lane `SKILL.md` with digest `"c"*64` → `live-lane-read:…/SKILL.md`.

Open:

- `.git/` reads are accepted unconditionally, whatever the digest
  (`measure.py:443-444`). Demo: `live_lane_reads={LIVE+"/.git/HEAD":"c"*64}`
  → **credited**. So live refs/index/HEAD reads are "bound" by rule, not by
  bytes.
- Live **sibling** repos (kumitate/kagi/tsukuroi/mado) are outside
  `LIVE_LANE_ROOT` (`measure.py:133`) and pass the external check; demo: a
  receipt `external` key for `kumitate-shokunin/tools/whatever.sh` with a fake
  digest was accepted. K02 hole 5(b)'s `pin-disposition --root /home/...`
  sibling reads are therefore still invisible.
- `trace` `cwd`/`root` are not checked against the measured repo (measure
  ignores them; assemble checks only `rev`).

### Hole 6 — git-object reads invisible / symbolic revs — **partly (documented limit)**

- `--rev` is resolved once to 40-hex (`resolve_commit`, `measure.py:155-167`)
  and every blob read uses `revision`; `--rev HEAD` reports
  `rev_input HEAD`, `revision 1702254…` (40-hex). Immutable-rev measurements
  are reproducible.
- Still open: entry `read_rev` is never compared to the measured rev by
  `measure.py`; the credit demo uses `read_rev="0"*40` and still credits.
  Receipt `rev` is bound only at assembly (`assemble.py:456-460`), not at
  measurement. Git-object reads are not inputs; live `.git/` reads pass hole-5
  rule unconditionally. A ledger produced by any other path can therefore cite
  a foreign `read_rev` undetected at the consumer.

### Hole 7 — over-invalidation by the page/ledger/SHONEN — **partly**

Closed for exactly two keys:

- `IGNORED_INPUTS = {"SKILL.md", ".ufo/evidence/round-17/coldread/ledger.json"}`
  (`measure.py:132`), dropped from the entry view (`316-323`) and from receipt
  inputs (`407`); `assemble.py` drops the same two (`DROPPED_INPUT_KEYS`,
  `131-134`, merge at `507`). Demo: entry inputs
  `{"SKILL.md": <sha>, "PROVINCE.md": <sha>}` → credited.

Open (same class of defect one key over):

- Every other file the seat opened still gates credit. Demo: entry input
  `SHONEN.md`; editing SHONEN.md then measuring → `input-drift:SHONEN.md`,
  not credited.
- The exemption is the literal default ledger path only; a ledger read via
  `--ledger-rev REV:path`, a round-18 ledger, or any other self-referential
  output is not exempt.
- Real-byte consequence: two credited tip entries pin the advisory census
  `.ufo/evidence/round-17/coldread/bucket-commands.json` as an input
  (entries `start 1814` and `start 1897`, both `reason None`). In the /tmp
  clone, appending one newline to that file and committing gave
  `covered 56 / 58 box3 False restraint 6` with
  `input-drift:.ufo/evidence/round-17/coldread/bucket-commands.json: 2`.
  So a file with **no consumer** is load-bearing for box 3.

## Spot-check point: receipts are not bound to declared/required commands — **confirmed**

- **Declared:** the only declared-command list (report `commands_executed`) is
  summed and dropped (`assemble.py:885-886`; ledger entry keys have no such
  field). `measure.py` sees only the integer `commands_executed_count` and
  requires `>=1` trace, not one per command. Demos: 1 receipt ↔ 1 declared
  command accepted; 1 receipt ↔ 5 declared commands accepted and credited.
- **Required:** the mechanically extracted page commands live only in
  `bucket-commands.json`, and no code reads it (below).
- **Receipt side:** neither tool reads `argv`; `measure.py` does not even read
  receipt `rev`. A pure-prose bucket is credited by `cat PROVINCE.md`.
- Producer/consumer asymmetry worth naming: `assemble.py` binds
  receipt.rev == report.read_rev, but the cited consumer (`measure.py`) does
  not re-check that binding, so a hand-built or differently produced ledger
  is not held to it.

## `bucket-commands.json` — contents and consumers

Contents (`schema tameshi-bucket-commands-v1`, `bucket-commands.json:1-10`):

- `rev 98bea7d…`, `skill_sha256 906fb649…` (SKILL.md **at 98bea7d**),
  `ledger_path .ufo/evidence/round-16/coldread/ledger.json`.
- 54 buckets, each with `start,end,heading,sha256`, `fenced_blocks` (with
  `command_lines`, `other_executable_like`), `inline_commands`,
  `numbered_steps`, `executes_commands`,
  `executes_commands_incl_numbered_steps`, `ledger {credits,class,verdict,
  commands_executed_count,seats,matched_entries}`, `mechanical_vs_ledger`.
- Aggregates: `n_buckets 54`, `n_executes_yes 27`, `n_disagree 23`
  (13 yes+record, 10 no+instruction), `n_uncovered 0`.
- There is **no `required_commands` field**: it records candidate command
  inventories and two flags, leaving selection to a consumer.
- Staleness: the tip page is `de6c2b0…` (sha256 of SKILL.md at 183f87b) with 58
  sections; only 45/54 old section shas match the tip at the same start, and
  the file's page sha (`906fb6…`) no longer exists at tip.

Consumers: **none.**

- `git grep -q "bucket-commands" <rev> -- '*.py' '*.mjs' '*.sh' '*.js'` →
  exit 1 (no match); `executes_commands` over the same set → exit 1.
- 22 tracked files mention the path: the JSON itself, the round-17 ledger (two
  entries' `inputs`), one trace receipt (`traces/RR2/13.json`, which merely
  opened it), and wave-17/18 prose/dispatch/spec (`X16BucketCommands.md`,
  K02, wave-2 reviews, `dispatch1.json`, `spec1.json`, `spawn1.json`).
- X16's own report frames it as advisory: the JSON "keeps
  `other_executable_like` so the L1 can re-grade with a tighter/looser rule
  without re-parsing" (`.ufo/waves/round-17/w1/X16BucketCommands.md`,
  Caveats).
- In-flight status (untracked at report time, not at the rev): the round-18
  kit `.ufo/evidence/round-18/measure.py` and `coldread/assemble.py` also
  contain no `bucket-commands`/`executes_commands` reference
  (`grep -rq … ; echo $?` → 1). `measure.py:135-137` extends `IGNORED_INPUTS`
  to `SKILL.md`, the round-17 ledger and the round-18 ledger — the hole-7
  fix is carried forward, but advisory files such as the census are still not
  exempt.
- Paradox: no consumer, yet two credited ledger entries pin its sha. Making it
  a consumer rule in round 18 will require re-pinning/regenerating those
  entries, or it will keep dropping 2 buckets on every edit.

## Lesson Gate G5/G7 corrections (spot-check §7 item 2, line 423)

- `corpus/lessons/round-17.md:22` (G5) claims "K02 holes 1–4 … closed in
  `measure.py` (89/89 selftest)". At the rev: holes **3 and 4 are closed**,
  hole **1 is only partly** (no argv/command binding; receipt rev/read_rev
  unchecked by the consumer), hole **2 is only partly** (zero-command specific
  closed; class still self-declared). Selftest tally observed: **94/94**
  (`MEASURE_SELFTEST`), so the cited 89 is a dated build count; the
  spot-check's "89 vs final 94" note is correct.
- `corpus/lessons/round-17.md:24` (G7) cites "K02 hole 5" for
  "one edit would uncredit the whole page". K02 hole 5 is live-lane reads
  (`K02InputCreditHoles.md:28`); the described over-invalidation is **hole 7**
  (`K02InputCreditHoles.md:30`). Off-by-two pointer, as the spot-check routed.
- The narrowed claim the L1 may preserve ("input-keyed evidence", not
  "required commands executed") is exactly what the code supports: inputs are
  bound, commands are not.

## Remaining unknowns

- Real-data rate of unrelated receipts per bucket: not measured here (would
  require pairing each credited entry's receipt `argv` with the bucket's
  mechanically extracted commands; X16 is the closest census and is keyed to
  the stale page).
- Whether any wave-2 seat exploited the `.git/` unconditional acceptance: no
  sampled receipt needed it; the code path is open.
- Round-18 contract F's new `measure.py` cannot inherit the round-17
  `IGNORED_INPUTS` literally: it must ignore both ledger paths (contract says
  so) and should decide whether `bucket-commands`-style advisory artifacts
  stay pinned inputs.

Verdict: **partial** — holes 3/4 closed, holes 1/2/5/6/7 only partly closed; the spot-check's point holds: receipts are bound to input sets and (at assembly) to `read_rev`, never to the bucket's declared or required commands; `bucket-commands.json` is an unconsumed, stale advisory census that two credited entries nonetheless pin as an input.
