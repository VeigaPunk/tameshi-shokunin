# T49W2ExecC2Probe — wave-2 probe of `tools/pbt-staged-id.py` at the candidate

Seat: T49W2ExecC2Probe (executor, leaf). Item: exercise the C2 generator at the candidate; report
commands, exits, last lines and timings. Nothing here is a verdict; the deciding run is the L1's.

## Setup (what was run against what)

| item | value |
|---|---|
| candidate rev | `f181a961ae44061af486f600e5ea257d2baf78f8` (`git -C <lane> show --stat f181a96`, HEAD of `9b9b2a0`+`f181a96`) |
| guard | `tools/staged-id-guard.py`, sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` — equals the pinned digest in `.ufo/evidence/round-49/c2/measure.py:45` (`sha256sum` in the clone) |
| generator | `tools/pbt-staged-id.py`, sha256 `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05` |
| interpreter | `Python 3.14.8` (`python3 -V`) |
| tree | `git clone -q --shared <lane> cand && git -C cand checkout f181a96…`; `git -C cand rev-parse --show-toplevel` printed the clone, `rev-parse HEAD` printed the candidate |
| scratch | `/fast/scratch/hyaku/tameshi-r49/T49W2ExecC2Probe`, `TMPDIR` pinned per run; deleted before yield |
| installs | none (no pacman, no uv/npx; nothing needed) |
| not read | `/home/vgpnk/.local/state/`, the C2 panel, `c2-WITNESS/CTL_FIX/CTL_ABSENT.stdout`; no counter was run (not even `--selftest`) |

Receipts copied to this directory: `T49W2ExecC2Probe.runs.txt` (every seed run, dump shas, edge
cases, selftest), `T49W2ExecC2Probe.audit.txt` (independent classification of the 400-case dump),
`T49W2ExecC2Probe.census.txt` (blind-spot census), `T49W2ExecC2Probe.mutants.txt` (mutant probe),
and the two driver scripts `T49W2ExecC2Probe.mutprobe.py`, `T49W2ExecC2Probe.census.py`,
`T49W2ExecC2Probe.dump-audit.py` so every number below is reproducible from the pinned bytes.

## Item runs (commands, exits, last lines, timings)

All runs: `cd <scratch>/cand`, `TMPDIR=<scratch>/w/<tag>`,
`python3 -I tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed S --cases N --dump <file>`.
Wall times are `date +%s%N` deltas around the process; the tool's own line is
`PBT_STAGED_ID_TIME`. Receipt: `T49W2ExecC2Probe.runs.txt`.

### 1. `--selftest`

```
python3 -I tools/pbt-staged-id.py --selftest
```
exit 0, wall 42 ms, 31 `CASE … PASS` lines, last line
`PBT_STAGED_ID_SELFTEST: cases=31 failed=0`.

### 2. seed 4949, 400 cases, pristine guard (the claim's parameters)

```
python3 -I tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 4949 --cases 400 --dump …/dump.jsonl
```
exit 0, wall **13278 ms** (tool: `PBT_STAGED_ID_TIME: seconds=13.24`), dump 400 lines, sha256
`ca62402bc6125cb8003b3854a30bef829d29d5c6656be1f8a516ca2828a7cd28`. Class table, verbatim:

```
CLASS indent_1_3=248
CLASS indent_4_plus=31
CLASS id_4_plus_digits=31
CLASS collision=204
CLASS no_collision=62
CLASS held=49
CLASS unmapped=31
CLASS cascade=45
CLASS refusal=61
CLASS url_form_variant=30
CLASS map=104
CLASS map_inadmissible=31
PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31
```

Minimum class count 30, i.e. above the contract floor `class_min=10`
(`.ufo/evidence/round-49/contract.json`) and above the generator's own `CLASS_MIN = 20`
(`tools/pbt-staged-id.py:66`) — no `SHORT` markers. The last line matches the counter's frozen
regex `.ufo/evidence/round-49/c2/measure.py:59`
(`LAST_RE.match(...).groups() == ('400','0','none')`, checked with a two-line python probe).

### 3. seeds 1–5, 400 cases each

| seed | exit | wall ms | violations | min class |
|---|---|---|---|---|
| 1 | 0 | 12817 | 0 | 30 (`url_form_variant`) |
| 2 | 0 | 11787 | 0 | 30 |
| 3 | 0 | 12855 | 0 | 30 |
| 4 | 0 | 11735 | 0 | 30 |
| 5 | 0 | 12883 | 0 | 30 |

Each printed `PBT_STAGED_ID: cases=400 violations=0 counterexample=none …` and wrote a 400-line
dump; no `VIOLATION` line in any run (`grep -c VIOLATION` = 0). **No seed found a pristine
violation** — so neither a guard finding nor a generator (oracle) finding surfaced by this route.
Extended for breadth (same command, same guard): seeds 6–15 all exit 0, wall 12019–12771 ms, min
class 30; seed 4949 with `--cases 1200` exit 0, wall **36410 ms**, min class 89. Total pristine
case volume executed this wave: **7600** (16 × 400 + 1200).

Determinism (interface promises "deterministic from the seed"): a second seed-4949 run in a
*different* TMPDIR produced the identical dump (`cmp` clean, same sha256 `ca62402b…`, wall 11383
ms); different seeds differ (`cmp` on first line → DIFFER; four distinct dump shas). The generator
leaves no temp directory behind (`find <scratch>/w -maxdepth 1 -name 'pbt-staged-id-*'` → 0 after
completion).

### 4. `--cases 0` and `--cases 1`

```
python3 -I tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 4949 --cases 0 --dump …/c0/dump.jsonl
→ exit 2, wall 37 ms, stdout empty, stderr: pbt-staged-id: --cases must be at least 1
→ dump file not created (`ls` → No such file or directory)
```
`--cases 0` is a **setup refusal, not a zero-case run** (`tools/pbt-staged-id.py:980`). The frozen
interface in the contract does not state that lower bound; the counter only ever passes 400
(`measure.py:49`), so nothing is at risk — recorded as observed behaviour, no defect claimed.

```
--cases 1 → exit 0, wall 72 ms (tool: seconds=0.03), one dump line, last line
PBT_STAGED_ID: cases=1 violations=0 counterexample=none classes=indent_1_3=1,indent_4_plus=0,id_4_plus_digits=0,collision=1,no_collision=0,held=0,unmapped=1,cascade=0,refusal=0,url_form_variant=0,map=0,map_inadmissible=0
```
Nine classes print `SHORT` at n=1 (`tools/pbt-staged-id.py:827`) and the exit is still 0: exit
status answers "did any case violate?", never "was coverage adequate". A reader who trusts exit 0
alone at small N would be misled; the counter supplies its own `CLASS_MIN` re-classification
(`measure.py:50`), so the deciding label is unaffected.

Setup paths (all exit 2, stderr one line, no traceback): missing guard (`guard is not a regular
file: …`), unwritable dump (`cannot write dump …`), missing required args.

## Independent audit of the 400-case dump

`T49W2ExecC2Probe.dump-audit.py` re-runs the pristine guard over the unmodified seed-4949 dump and
classifies each case with a classifier written here (not the generator's, not the counter's).
Result (`T49W2ExecC2Probe.audit.txt`): all twelve classes reproduce the generator's own numbers
exactly (248 / 31 / 31 / 204 / 62 / 49 / 31 / 45 / 61 / 30 / 104 / 31), guard exits
0:232, 1:107, 2:61, and all five verdicts occur (`answered` 190, `refused` 76, `inadmissible` 31,
`admitted` 42, `setup_refusal` 61). Every documented JSON field carries a non-empty value at least
once (`collisions` 277, `column0_collisions` 135, `column0_miss` 142, `held` 75, `unmapped` 34,
`cascade` 50, `map_clash` 7, `map_dedupe` 20, `map_below_floor` 4, `map_staged_clash` 4,
`map_uncovered` 4, `map_undocumented` 3, `map_held_moved` 6, `analysis_refused` 8, …). Every map
reason tag the oracle projects occurs (injective 3, carry 3, registry 7, staged 4, floor 4, cover 4,
self 3, undocumented 3, held 6). Purity: the generator opens only the dump (`tools/pbt-staged-id.py:795`)
and the per-case files it writes (`:752`); it reaches the guard only through `subprocess`
(`:762`); `grep -n "\.local\|panel\|witness\|/home\|sys.path\|importlib\|exec(\|eval("` over it
returns no match.

## Falsification: mutants built in scratch (7 blind spots, 1 kill control)

Method (`T49W2ExecC2Probe.mutprobe.py`, receipt `T49W2ExecC2Probe.mutants.txt`): the pinned guard is
copied in scratch, one exact-string replacement is applied (count asserted = 1), and the generator
runs against it with `--seed 4949 --cases 400`. A survivor then gets a hand-made **witness** case
run through pristine and mutant to show the difference is real, not an equivalent mutation. The
witness for each also measures whether the case stream can reach the region at all
(`T49W2ExecC2Probe.census.txt`).

| # | mutation (exact string → replacement) | generator | guard `--selftest` | witness: pristine vs mutant | reach |
|---|---|---|---|---|---|
| X7 | `        if len(cells) < 5:` → `< 4` (**kill control**) | exit 1, 12 cases, `counterexample=11` | PASS (blind) | — | — |
| X1 | `result['registry_sha256'] = …read_bytes(args.registry)…` → `…read_bytes(args.staged)…` | exit 0, 400 cases | PASS (blind) | `registry_sha256` `0fde9438…` vs `57dbb2b1…` (= staged hash); exit 0/0 | every case |
| X2 | `MAX_TEXT = 32 * 1024 * 1024` → `1024 * 1024` | exit 0, 400 cases | PASS (blind) | 1.2 MiB registry: exit 0 `answered` vs exit 2 `setup_refusal` "larger than 1048576 bytes" | largest registry in the dump is **620 bytes** |
| X3 | `'registry_docs': len(registry_docs),` → `len(registry),` | exit 0, 400 cases | PASS (blind) | witness registry row with prose source: `registry_docs` 0 vs 1 | `registry_docs == registry_rows` in **all 339** answered cases |
| X4 | in `analyse`: `registry_docs.setdefault(...)` → `registry_docs[...] = sid` (first-wins → last-wins) | exit 0, 400 cases | PASS (blind) | `held` `{'S002': 'S001'}` vs `{'S002': 'S002'}` | **0** cases have two registry rows sharing a document |
| X5 | `re.split(r'\s+[—–]\s+', source)` → `re.split(r'\s+—\s+', source)` (drop U+2013) | exit 0, 400 cases | PASS (blind) | en-dash source: `held {'S001': 'S001'}` vs `{}` | em dash in 384 cases, **en dash in 0** |
| X6 | `    if not stat.S_ISREG(info.st_mode):` → `if False and …` | exit 0, 400 cases | PASS (blind) | `/dev/null` as `--registry`: exit 2 `"… is not a regular file"` vs exit 0 `answered` | the generator only ever writes regular files |
| X8 | `        if bare in seen:` → `if False and bare in seen:` (duplicate map key) | exit 0, 400 cases | **FAIL** | map with `"S002"` and `"staged:S002"`: exit 2 `"map file repeats the key"` vs exit 0 | structurally unreachable: the dump's map is `json.dumps` of a Python dict |

X7 proves the rig can kill (it reproduces a violation in 12 cases, 0.4 s), so the seven survivors
are findings, not a broken harness.

### F1 — the generator never grades the two sha values it requires to be present (attacks the C2 oracle-agreement wording)

`tools/pbt-staged-id.py:312` requires `registry_sha256`/`staged_sha256` to be **present**
(`SHA_KEYS`, `:68`) but the comparison loop that follows compares only `sorted(expected)`, and
`expected` (`tools/pbt-staged-id.py:246-264`) never contains them. Witness X1: the mutant returns the
staged hash as the registry hash and the generator reports `cases=400 violations=0`. The guard
docstring calls those fields "the bytes read" (`tools/staged-id-guard.py:52-53`). The counter does
not close the gap either: `comparable()` strips both keys before the differential
(`.ufo/evidence/round-49/c2/measure.py:188-193`, and its own selftest asserts that stripping at
`:419-420`). Consequence: **a panel mutant that corrupts either sha field cannot be confirmed by
this instrument**, so it would cost one of the 11 required kills. The generator's own `--selftest`
has no case for the field values either (31 cases, none over the sha pair).

### F2 — the stream never presents a registry row without a document, so `registry_docs` is degenerate (X3)

Census (`T49W2ExecC2Probe.census.txt`): `registry_docs != registry_rows` in **0 of 339** answered
cases; the six cases my census flagged (`index 37, 102, 167, 232, 297, 362`) are the refusal
recipe's malformed short rows, refused before any field is printed. Every recipe builds registry
rows through `doc_row` (`tools/pbt-staged-id.py:408`) or a path document, so a count/derivation
mutation in `registry_docs` (`tools/staged-id-guard.py:139-142,176`) is invisible.

### F3 — two registry rows sharing one document are never generated (X4)

Census: **0** cases. The library dedupe rule "first registry id wins" (`tools/staged-id-guard.py:142`,
mirrored at `tools/pbt-staged-id.py:134`) has no case that distinguishes `setdefault` from
last-wins; witness X4 changes `held` from `{'S002': 'S001'}` to `{'S002': 'S002'}` and the
generator stays silent. The same first-wins map feeds `map_dedupe`/`map_held_moved`, so a mutant
there is invisible too.

### F4 — only the em dash of the separator class is exercised (X5)

`document_key` splits source cells on `\s+[—–]\s+` (`tools/staged-id-guard.py:106`); every
generator source cell uses U+2014 (`tools/pbt-staged-id.py:409, 545, 548, 710`). Census: U+2013 in
**0** cases. Witness X5 (an en-dash source cell) moves `held` from `{'S001': 'S001'}` to `{}`.

### F5 — no setup-refusal path outside parse-level rows is reachable (X2, X6, X8)

The generator's only setup refusals are malformed rows and duplicate ids (`tools/pbt-staged-id.py:109-125`);
`read_bytes`' size cap (`tools/staged-id-guard.py:69,416-430`) and non-regular-file refusal (`:421`)
need inputs the generator cannot produce (largest registry in the dump: 620 bytes; only regular
files written), and the duplicate-map-key refusal (`:406-415`) needs a JSON document with a
repeated key, which `json.dumps` of a dict cannot emit. Witnesses X2/X6/X8 each flip exit 2 → 0.
The guard's own `--selftest` catches X8 but not X2/X6.

### F6 — the oracle is an independent *program*, not an independent *reading* (attacks "its own oracle written from the documented contract")

The generator's oracle functions are line-for-line the guard's: `parse_rows`
(`tools/pbt-staged-id.py:109` / guard `:77`), `document_key` (`:81` / `:99`), `normalise_document`
(`:93` / `:116`), `id_number` (`:104` / `:127`), `analyse_fields` (`:126` / `:132`), `map_fields`
(`:170` / `:180`), including the same reason ordering (generator comment `:209`: "reason order
follows the guard's own order") and at least one rule taken from the source, admitted in place:
`if len(sid) > 12:  # observed guard rule; not generated, kept for fidelity` (`:104`) — a rule the
guard's docstring never states. This is not a defect in the frozen label, but it bounds what
"oracle_disagree=0" can mean: a misreading shared by docstring, guard and oracle is invisible to
both, and the region where the oracle *knows* something not in the docstring is exactly the region
it never generates.

## Adjacent counter clauses (observed, for the L1, not relitigated)

* **Oracle agreement is narrow.** `measure.py:316` runs the counter's second oracle only on
  `map is None` cases (296 of 400), and for those it compares only `collisions`, `registry_rows`,
  `staged_rows`, and only when the expected exit is 0 (`:319-323`); verdict, held/unmapped/cascade,
  naive map, `safe_floor`, the column probes and every map field are not compared. The map cases
  (104) are cross-checked only by the generator's own oracle.
* **The F10 record check is a substring test.** `measure.py:288` passes on *any* README line
  containing both `F10` and `held (round 49)`. At the candidate, `corpus/README.md:87` (the frontier
  table row) still reads `open`, while `corpus/README.md:599` carries the conditioned `held
  (round 49)` sentence; the check is satisfied by the appended line only. A line that *denied* the
  movement would pass the same test.
* The pilot entry's leading block cites `S269`/`S270` and `corpus/SOURCES.md:144-145` carry
  `mined | 2026-10-26` — consistent with `measure.py:...records()` by inspection (not a run).

## What this seat did not do

No counter invocation (not even `--selftest`), no panel or witness file read, no lane write outside
`.ufo/waves/round-49/w2/`, no git mutation in the lane or the fleet repo (the one clone was created
with `git clone --shared` into scratch, its toplevel asserted before use), no claim decided.

## Summary

1. Candidate f181a96: generator sha `0cbee392…`, guard sha `03a796c5…` (pinned) — `--selftest` exit 0, 31/31 cases, 42 ms.
2. seed 4949 / 400 cases: exit 0, `violations=0`, wall 13.28 s, dump sha `ca62402b…`, 400 lines, min class 30 (floor 10).
3. Seeds 1–5 (and 6–15) × 400 + one 1200-case run: all exit 0, no pristine violation in 7600 cases; dumps deterministic per seed (identical sha across TMPDIRs).
4. `--cases 0` → exit 2 "must be at least 1" with no dump (37 ms); `--cases 1` → exit 0 with 9 classes `SHORT` (72 ms) — exit status never encodes coverage.
5. Independent classifier reproduces all 12 class counts; exits 232/107/61; all five verdicts and every documented field exercised at least once.
6. Kill control X7 killed in 12 cases (exit 1, 0.4 s); seven mutants survive: sha values (F1), `registry_docs` (F2), first-wins registry document (F3), en-dash separator (F4), size cap / non-regular file / duplicate map key (F5), each with a differential witness.
7. F1 is the sharpest: the generator and `measure.py:188-193` both exclude the two sha values, so a panel mutant on them is unconfirmable (one of the 11 kills at risk).
8. F6 bounds the oracle: same code shape as the guard and one source-derived rule at `:104`; adjacent counter clauses (map-case oracle skip, README substring test) noted for the L1.
