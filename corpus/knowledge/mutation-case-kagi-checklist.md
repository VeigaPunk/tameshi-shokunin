# Mutation case — kagi `corpus/checklist-run.sh` (service sweep, TAMESHI T8-1, round 8)

Swept 2026-10-14T19:13:25Z (= 16:13:25 -0300) by lane T8-1 (tameshi round 8,
training). Role: **the fifth fleet mutation case** (after kimi-census r2,
surface-census r3, tsukuroi-census r5, mado-verify r6) and the **third
engagement** under the service opt-in protocol
(`corpus/knowledge/service-optin-protocol.md` @ `84d0c154…`, 286 L): form =
**service** — tameshi runs the harness on /tmp copies; absorption stays with the
owner lane (kagi) and is recommendations-only (`PROVINCE.md:14-18`). The
triggering record is the round-8 dispatch; no kagi-side opt-in is recorded in
kagi's tree at this write (O: `grep -rIn tameshi|mutate-and-run kagi-shokunin/`
excluding `.git` → 0 matches) — whether the owner asked is U4.

Anchors: **O** observation · **I** inference · **U** unknown. shas are sha256,
first-16 unless marked full. This lane wrote only this file; kagi's and
tameshi's trees were read-only (§5); scratch `/tmp/w8-tameshi-t81/`; LOG.md /
SCORECARD folds happen at lane review, per dispatch-write-scope precedent.

## 0. The object, the instrument, the control

- **Target (O).** `kagi-shokunin/corpus/checklist-run.sh` —
  `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf`, 506 L /
  24 697 B, mode 755, mtime 2026-10-13 16:51:07 -0300. It is the committed HEAD
  blob: `git show HEAD:corpus/checklist-run.sh | sha256sum` → the same digest,
  with kagi `HEAD fecee8743e52eb8fb5fbb40782934cb619a1a96e` and
  `git status --porcelain` empty at open and at close (SC3). The recorded pin
  behind the dispatch is the same digest: kagi's survey row says 506 L /
  24 697 B / **34** cases (`gates-survey-kagi.md:29`), and the ledger's queue
  row carries suite 34, "unmeasured by sweep; hermetic"
  (`fleet-kill-rate-ledger.md:121`).
- **Instrument (O).** `tameshi-shokunin/tools/mutate-and-run.sh` @
  `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` (r7-1,
  1 341 L / 61 632 B, mtime 2026-10-14 15:29:01). The live file was copied to
  `/tmp/w8-tameshi-t81/mutate-and-run.sh` (`cp -p`, sha re-measured equal) and
  **the copy is what ran**; the live path was re-hashed at close and had not
  moved. The run's own `MUTATE_TOOL` line carries the copy's sha above. This
  revision is newer than the ledger §5 pulse pin (`b56c6e57…`, 1 080 L, cases=2)
  and ER-1's mid-flight revision (`13d2fbfc…`, 1 114 L); at this write its
  `--regression` leg list names **four** cases (O, header `:75-78`, spec
  literals `:552`/`:593`/`:638`/`:683`). Recorded as a T2-style new-revision
  observation for the cadence lane; not interpreted here.
- **The target was never a write target (O).** The harness was handed a `cp -p`
  copy (SC3: `cmp` identical to the live file) and mutates only fresh copies of
  its own pristine; the live file's sha256 is unchanged after every run and
  after the probes (§5). The run's `MUTATE_TARGET` line carries
  bytes=24697 and the pinned digest.
- **Suite (O).** `bash "$MUTANT" --selftest`, 34 cases, control
  `CONTROL: GREEN (exit=0 duration-ms=1870 pristine-sha256=7e5ec98b…)` /
  `CHECKLIST_SELFTEST: PASS (34 cases)`. Hermetic basis, measured at this
  write: the selftest builds every fixture under `mktemp -d`
  (`checklist-run.sh:341-344`) and re-invokes the gate copy with
  `--tsv`/`--skill` pointing at those fixtures (`:416`) — no case reads a live
  path; the same control re-run from `cwd=/` with a scratch `HOME` printed the
  same PASS, rc 0. On the dispatch's "hermetic per the round-3 census": the r3
  census did **not** exercise this gate — it names `checklist-run.sh` as its own
  unexercised fallback (U4, `mutation-case-kagi-census.md:201-202`); the
  family's hermetic-run rule is `gates-survey-kagi.md:58-64` plus the ledger row
  above. What this lane measured is the fixture-only control + the write fence.
- **Spec hygiene (O).** 15 defects, one exact-string edit each; the harness
  asserts every `@old` count==1 before any suite run (tool header `:52-56`), and
  this lane pre-validated the same table independently (15/15 count=1, no
  no-op). Per-mutant `diff` against the pristine: **exactly one changed line**
  for all 15 (each `diff` = 2 lines: one `-`, one `+`), per-mutant sha256 in
  `sweep/results.tsv`.

## 1. Defect spec — clauses, composition, pre-registration

The gate's declared contract, read off its own header/verdict list
(`checklist-run.sh:2-61`), split into seven clauses this spec maps one or more
defects to:

| clause | surface | gate lines | defects |
|---|---|---|---|
| A item extraction | section start/stop, `- [ ] ` bullets, continuations | `:96-116` | A1, A2 |
| B row-declaration policy | 8 columns, id/class/reason rules, deny list | `:120-172` | B1, B2, B3, B4 |
| C lead bijection | row↔item counting, UNMATCHED/DUPLICATE both ways | `:205-237` | C1, C2 |
| D ratio floor | `floor_of`, the `k*FLOOR_DEN >= items_n` test | `:174`, `:239-246` | D1, D2 |
| E row execution | exit-set membership, last-non-blank-line assert | `:256-279` | E1, E2 |
| F verdict lines / exit map | CLEAN/BROKEN lines, `return 1`, `--only` render | `:281-297` | F1, F2 |
| G CLI modes | unknown argument refusal | `:79-91`, `:501-506` | G1 |

Composition, **stated before the run**: 7 defects cut at sites this lane could
name as asserted by the suite's own fixtures ("kill-aimed": A2, B2, B4, C2, D2,
E1, F1) and 8 at seams it predicted unreached or unasserted ("hole-aimed": A1,
B1, B3, C1, D1, E2, F2, G1). Predictions were pre-registered as comments in the
spec file before the sweep; the table below is that pre-registration verbatim,
`K` = expect KILLED, `S` = expect SURVIVED.

| id | clause | edit site on `7e5ec98b` | expect |
|---|---|---|---|
| A1 | A | `:107` section stop `'## '*` → `'## '` | S |
| A2 | A | `:104` header gate sets `in=0` | K |
| B1 | B | `:139` id regex `^[A-Z][0-9]+$` → `^[A-Z]+[0-9]+$` | S |
| B2 | B | `:160` by-hand non-space floor `>= 20` → `>= 0` | K |
| B3 | B | `:75` deny list drops `the-janitor stop` | S |
| B4 | B | `:145` `expect_exit` regex accepts a bare integer only | K |
| C1 | C | `:226` UNMATCHED-ITEM condition `== 0` → `== -1` | S |
| C2 | C | `:227` DUPLICATE-ITEM threshold `> 1` → `> 2` | K |
| D1 | D | `:174` `floor_of` truncates instead of ceiling | S |
| D2 | D | `:73` `FLOOR_DEN=2` → `1` | K |
| E1 | E | `:264` exit-set membership → exact equality | K |
| E2 | E | `:261` row capture drops `2>&1` | S |
| F1 | F | `:289` `return 1` → `0` on the BROKEN path | K |
| F2 | F | `:285` `--only` BROKEN line prints `failed=0` | S |
| G1 | G | `:88` unknown argument `exit 2` → `0` | S |

Measured: **every verdict matched its prediction — 7/7 K and 8/8 S, 15/15.**

## 2. Kill-rate table

| # | clause | injected defect (site on `7e5ec98b`) | exit | verdict | failing labels |
|---|---|---|---|---|---|
| — | control | unmutated pristine copy | 0 | GREEN `34/34` | — |
| A1 | A | section stop narrowed to the two-char header (`:107`) | 0 | SURVIVED | 0 |
| A2 | A | the header gate never opens the section (`:104`) | 1 | **KILLED** | 30 — `clean: exit 2 want 0` … |
| B1 | B | id charset loosened (`:139`) | 0 | SURVIVED | 0 |
| B2 | B | padded by-hand reasons accepted (`:160`) | 1 | **KILLED** | 1 — `padded reason: exit 0 want 2` |
| B3 | B | deny-list alternative `the-janitor stop` dropped (`:75`) | 0 | SURVIVED | 0 |
| B4 | B | `expect_exit` rejects multi-exit sets (`:145`) | 1 | **KILLED** | 21 — `clean: exit 2 want 0` … |
| C1 | C | UNMATCHED-ITEM line never emitted (`:226`) | 0 | SURVIVED | 0 |
| C2 | C | DUPLICATE-ITEM tolerates two declarers (`:227`) | 1 | **KILLED** | 1 — `duplicate item: no /DUPLICATE-ITEM 4 .2 rows declare it./ in output` |
| D1 | D | `floor_of` floor-not-ceil (`:174`) | 0 | SURVIVED | 0 |
| D2 | D | ratio denominator `2 → 1` (`:73`) | 1 | **KILLED** | 10 — `clean: exit 1 want 0` … |
| E1 | E | multi-exit arms never accepted (`:264`) | 1 | **KILLED** | 4 — `clean: exit 1 want 0`; `ratio line`; `three-way exit`; `final clean` |
| E2 | E | row output captured without stderr (`:261`) | 0 | SURVIVED | 0 |
| F1 | F | BROKEN path returns 0 (`:289`) | 1 | **KILLED** | 10 — `exit mismatch: exit 0 want 1` … |
| F2 | F | `--only` BROKEN line prints `failed=0` (`:285`) | 0 | SURVIVED | 0 |
| G1 | G | unknown argument fail-open (`:88`) | 0 | SURVIVED | 0 |

`MUTATE: DONE (target=kagi-checklist defects=15 killed=7 survived=8
inconclusive=0 kill-rate=47%)` — 7/15 = 46.7 %, printed 47 %. Cost: 16 runs in
27.9 s wall (control 1 870 ms; mutants 168–2 009 ms) against the 300 s per-run
timeout, never approached.

## 3. Kill adjudication — the fleet rule, then the mechanisms

The protocol's rule (`service-optin-protocol.md:199-204`): killed = suite red
**and** the full case count still enumerated; exit-only is insufficient. All
seven kills satisfy it (O, `sweep/evidence/<id>.out`): each ran the case loop to
completion, ended on `CHECKLIST_SELFTEST: FAIL (n/34 cases)`, and n equals the
number of `checklist-selftest: FAIL` label lines — A2 30, B2 1, B4 21, C2 1,
D2 10, E1 4, F1 10. No exit-only or crash-only kill; 0 inconclusive. Full label
sets are in the evidence files (`grep '^checklist-selftest: FAIL'`); the labels
that carry the mechanism, verbatim:

- **A2** — 30 labels, from `clean: exit 2 want 0` through every fixture case:
  with the section gate at `in=0`, `extract_items` returns 0 items and every
  fixture that runs the section gate dies at its SETUP line (30/34; the four
  passing cases — `list`, `only by-hand`, `only unknown`, `missing section` —
  are the paths that bypass the gate or expect that SETUP).
- **B2** — `padded reason: exit 0 want 2`: only the pad-reason fixture separates
  a `>= 0` floor from `>= 20`; nothing else re-tests the non-space floor.
- **B4** — 21 labels from `clean: exit 2 want 0`: the suite's fixture rows
  themselves carry multi-exit sets (`rest_rows` uses `0|1`, tri-exit uses
  `3|4|5`), so narrowing the regex to a bare integer breaks the fixtures at
  policy time — the widest blast radius of any single-edit here.
- **C2** — `duplicate item: no /DUPLICATE-ITEM 4 .2 rows declare it./ in
  output`: with the threshold at 2, the dup-lead fixture's two declarers go
  unreported; the test also expects `UNMATCHED-ITEM 1`, which the mutant still
  emits, so only the DUPLICATE-ITEM assert is the tripwire.
- **D2** — 10 labels from `clean: exit 1 want 0`, plus
  `floor breach: no /RATIO .runnable=2 floor=3 items=6./`: `FLOOR_DEN=1` makes
  the 4/6 fixture breach its own floor, so the clean and ratio-mode cases fail
  before any row runs.
- **E1** — `clean: exit 1 want 0`; `ratio line`; `three-way exit`; `final
  clean`: the `0|1` fixture row and the tri-exit case are the two asserted
  directions of the exit-set contract; exact equality breaks both.
- **F1** — 10 labels from `exit mismatch: exit 0 want 1`: every
  defect-expecting case loses its rc; the mutant still prints the BROKEN line,
  so the label text is intact and only the exit code is wrong — exactly what an
  exit-only adjudicator would also have caught.

## 4. Survivors — every one a measured behaviour difference

Probes re-run pristine vs the sweep's mutant on inputs the suite's fixtures do
not build (fixture script + logs `/tmp/w8-tameshi-t81/probes/`); each cell is a
measured reading, none reads a live substrate. Classes per the fleet vocabulary
(`fleet-kill-rate-ledger.md:143-150`): (a) reported-but-unasserted · (b)
unreached fixture/arm.

| id | class | probe input | pristine | mutant |
|---|---|---|---|---|
| A1 | (b) | bullet `- [ ] omega` under the next `##` header (7 items, 6 rows) | `RATIO: runnable=6/6 floor=3`, rc 0 | `UNDECLARED (items=7 rows=6)` + `UNMATCHED-ITEM 7` + `floor=4`, rc 1 |
| B1 | (b) | row id `AB1` (two letters) | `POLICY row 1: id AB1 is not <letter><digits>`, rc 2 | accepted; `CHECKLIST_LIST: rows=6 runnable=6`, rc 0 |
| B3 | (b) | row check `the-janitor stop` | `POLICY row C1: check touches a denied surface (…)`, rc 2 | accepted; listed, rc 0 (probe never execs the verb) |
| C1 | (a) | 5 rows declared against 6 items | `UNDECLARED` + `UNMATCHED-ITEM 6 (no row declares it)`, rc 1 | `UNDECLARED` only; the item line is gone, rc 1 |
| D1 | (b) | 5-item section, 3 runnable + 2 by-hand | `RATIO: runnable=3/5 floor=3`, rc 0 | `floor=2`, rc 0 — the floor cell lies by one on odd counts |
| E2 | (b) | row prints its verdict on stderr only | last-line assert reads `A1: OK` → `CHECKLIST_RUN: CLEAN`, rc 0 | `ITEM-LASTLINE C1 (want /^A1: OK$/ got '')` → `BROKEN`, rc 1 |
| F2 | (a) | `--only C1` on a failing row | `CHECKLIST_ROW: BROKEN (id=C1 failed=1 — …)`, rc 1 | `failed=0`, plus a duplicated `CHECKLIST_ROW: BROKEN (id=1 failed=0 …)` line from the extra printf arg; rc 1 |
| G1 | (b) | `--definitely-not-a-mode` | message + rc 2 | the same message + **rc 0** (fail-open) |

Reading: six of the eight are unreached inputs (the suite's fixtures never build
them); two are values the gate prints but no case asserts. The F2 mutant's
duplicated line is the printf-arg-reuse artifact — recorded as observed, not
smoothed.

## 5. Restore proof and write fence

- `MUTATE_RESTORE: OK (target-sha256 before=7e5ec98b… after=7e5ec98b…
  pristine-sha256=7e5ec98b…)` — the pinned copy is bit-identical after the whole
  sweep (O, `sweep.log:71`).
- The live file was re-hashed after the sweep and after the probes:
  still `7e5ec98b…`; kagi `git status --porcelain` empty; the tameshi tree
  porcelain-clean too and the harness live sha unchanged at `cf41efaa…` (SC3).
- What this proves is the negative: **this lane's writes never touched the
  gate** — the target was only ever read and copied. No stability claim about
  kagi's tree beyond the two readings is made (protocol §2 rule).

## 6. Readings — the fifth row, and what it changes

- **Rate with composition, never alone.** 47 % = 7 kill-aimed (7/7) + 8
  hole-aimed (0/8). The co-extensive shape is now a **third measured instance**
  (mado 4/4 + 0/6; tsukuroi 6/6 + 0/4): nothing outside the asserted surface was
  caught, and nothing inside it escaped. The rate is composition, not a suite
  verdict; no cross-gate comparison is made here.
- **Pre-registration held 15/15** — and the per-clause split says where the
  suite stands: A 1/2 · B 2/4 · C 1/2 · D 1/2 · E 1/2 · F 1/2 · G 0/1.
- **Survivor census:** (a) 2 — C1, F2; (b) 6 — A1, B1, B3, D1, E2, G1. Against
  the ledger §4 instance list (kimi D2/D10; kagi B5/B10; tsukuroi B7–B10; mado
  D3/D5/D7/D8/D9/R1): a **CLI fail-open** (G1) and an **output-capture** loss
  (E2) are new mechanisms at the same (b) class, and the deny-list drop (B3) is
  the first secret-hygiene surface this method has found re-openable by a
  single edit.
- **Ledger hand-off (not this lane's write).** The §1 row shape takes: suite 34
  (at sweep) · **7/15 (47 %)** with the composition above · survivors A1, B1,
  B3, C1, D1, E2, F2, G1 with the classes in §4 · hardened: **no** (owner =
  kagi; §7) · last sweep r8 · pin `7e5ec98b…` (506 L) · driver: harness copy
  `cf41efaa…` (r7-1), passed via `/tmp`, live path unchanged.

## 7. Recommendations (owner-side; recommendations only, per `PROVINCE.md:14-18`)

Ranked by measured exposure; each names the swept mutant it would kill.

1. **Exercise every deny-list alternative (kills B3).** The fixtures cover 3 of
   the 8 alternatives (`op.env`, `claim-ledger.sh`, `the-janitor run`); a loop
   case asserting each of `op run`, `op read`, `op inject`, `the-janitor
   start|stop` refuses at POLICY closes the gap. Secret-hygiene surface, so
   first.
2. **A CLI refusal case (kills G1).** `--<unknown>` → rc 2 + message; the mode
   loop is currently untested across all 34 cases. (The neighbouring arm —
   `--only` with no id — is a guard no case reaches either; it was **not**
   mutated here, so this is a sighting, not a measurement.)
3. **A boundary + completeness pair (kills A1 and C1).** One fixture with a
   bullet after the section stop, one run asserting `UNMATCHED-ITEM`.
4. **Assert the `--only` rendering on a broken row (kills F2)** — the `failed=`
   cell, so the single-row report cannot silently say 0.
5. **A stderr-verdict row case (kills E2)** — or an explicit statement that row
   checks must print their verdict to stdout.
6. **A floor pin at an odd item count (kills D1)** — pin the printed `floor=`
   cell, not just the breach condition.
7. **An id-shape case (kills B1)** — `AB1` (or a digit-less id) must refuse.

Nothing above is applied here; acceptance and any hardening are kagi's call
(Rule 5: an unabsorbed recommendation is a complete record).

## 8. Spot-checks (three, re-run 2026-10-14T19:16Z on the live bytes/scratch)

- **SC1 — the sweep's own headline cells (O).** `grep -n 'MUTATE_TOOL\|
  CONTROL:\|MUTATE_RESTORE\|MUTATE: DONE' sweep.log` → line 1 `MUTATE_TOOL: …
  sha256=cf41efaa…`, line 5 `CONTROL: GREEN (exit=0 duration-ms=1870
  pristine-sha256=7e5ec98b…)` + `CHECKLIST_SELFTEST: PASS (34 cases)`, line 71
  `MUTATE_RESTORE: OK (… before=7e5ec98b… after=7e5ec98b…)`, line 73 `MUTATE:
  DONE (target=kagi-checklist defects=15 killed=7 survived=8 inconclusive=0
  kill-rate=47%)`.
- **SC2 — a kill's adjudication, from the evidence file (O).** `sed -n '1,2p'
  sweep/evidence/B2.out` → `checklist-selftest: FAIL padded reason: exit 0 want
  2` and `CHECKLIST_SELFTEST: FAIL (1/34 cases)` — red, enumerated, labelled.
- **SC3 — the live object and the trees (O).** `sha256sum
  kagi-shokunin/corpus/checklist-run.sh` → `7e5ec98b…76bf`; `git show
  HEAD:corpus/checklist-run.sh | sha256sum` → the same; `git status --porcelain`
  → 0 lines; `cmp` of the scratch pristine against the live file → identical;
  `sha256sum tameshi-shokunin/tools/mutate-and-run.sh` → `cf41efaa…` with the
  tameshi tree porcelain-clean.

## 9. Reproduce

```
mkdir -p /tmp/w8-tameshi-t81 && cd /tmp/w8-tameshi-t81
cp -p /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh tool.sh
cp -p /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh pristine-checklist-run.sh
# write checklist.spec (below), then:
bash tool.sh --target /tmp/w8-tameshi-t81/pristine-checklist-run.sh \
  --defects /tmp/w8-tameshi-t81/checklist.spec \
  --suite 'bash "$MUTANT" --selftest' --label kagi-checklist \
  --workdir /tmp/w8-tameshi-t81/sweep
```

Spec (`checklist.spec`; the sweeps' predictions lived as comments on each
`@defect` line before the run — §1):

```
@defect A1 | section never closes — the '## ' stop becomes an exact two-char header
@old     [[ "$line" == '## '* ]] && break
@new     [[ "$line" == '## ' ]] && break
@defect A2 | section never opens — the header gate sets in=0
@old       [[ "$line" == '## Credential-hygiene checklist' ]] && in=1
@new       [[ "$line" == '## Credential-hygiene checklist' ]] && in=0
@defect B1 | id charset loosened (multi-letter ids accepted)
@old     if [[ ! "$id" =~ ^[A-Z][0-9]+$ ]]; then
@new     if [[ ! "$id" =~ ^[A-Z]+[0-9]+$ ]]; then
@defect B2 | by-hand non-space floor 20 -> 0
@old     ((ns >= 20)) || {
@new     ((ns >= 0)) || {
@defect B3 | deny list drops `the-janitor stop`
@old the-janitor start|the-janitor stop|the-janitor run
@new the-janitor start|the-janitor run
@defect B4 | expect_exit accepts a single integer only
@old     [[ "$exexit" =~ ^[0-9]+(\\|[0-9]+)*$ ]]
@new     [[ "$exexit" =~ ^[0-9]+$ ]]
@defect C1 | UNMATCHED-ITEM never reported (condition 0 -> -1)
@old ((hits == 0)) && defect "UNMATCHED-ITEM
@new ((hits == -1)) && defect "UNMATCHED-ITEM
@defect C2 | DUPLICATE-ITEM threshold raised 1 -> 2
@old ((hits > 1)) && defect "DUPLICATE-ITEM
@new ((hits > 2)) && defect "DUPLICATE-ITEM
@defect D1 | floor_of truncates instead of ceiling
@old floor_of() { printf '%s' "$(((($1 + FLOOR_DEN - 1)) / FLOOR_DEN))"; }
@new floor_of() { printf '%s' "$((($1) / FLOOR_DEN))"; }
@defect D2 | ratio denominator 2 -> 1
@old FLOOR_DEN=2   # floor = ceil(items / FLOOR_DEN)
@new FLOOR_DEN=1   # floor = ceil(items / FLOOR_DEN)
@defect E1 | exit-set membership becomes exact equality
@old       [[ "|$want|" == *"|$rc|"* ]] || {
@new       [[ "$want" == "$rc" ]] || {
@defect E2 | row output captured without stderr (2>&1 dropped)
@old     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}" 2>&1) || rc=$?
@new     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}") || rc=$?
@defect F1 | defect path returns 0 — BROKEN still exits 0
@old     return 1\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
@new     return 0\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
@defect F2 | --only BROKEN line prints failed=0
@old printf 'CHECKLIST_ROW: BROKEN (id=%s failed=%s — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
@new printf 'CHECKLIST_ROW: BROKEN (id=%s failed=0 — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
@defect G1 | unknown argument fail-open — exit 2 -> 0
@old     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 2 ;;
@new     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 0 ;;
```

Evidence layout (harness default): `sweep/{pristine,mutant-<id>}.*`,
`evidence/control.out`, `evidence/<id>.out`, `evidence/results.tsv`,
`evidence/defects.tsv`, `evidence/spec.copy`, `sweep.log`; probes under
`/tmp/w8-tameshi-t81/probes/` (`run-probes.sh`, `probes.log`, fixture skills and
`probe*.tsv`).

## 10. Unknowns

- **U1** — suite-only scope: the 15 mutants were adjudicated by `--selftest`
  alone; the gate's real mode (the live 16-row declaration) was never run and
  is not measured here.
- **U2** — cross-host/toolchain stability unmeasured (single host, bash 5.3.15,
  python 3.14.7, Linux 7.2.3-arch1-3, 2026-10-14).
- **U3** — coordinated multi-edit rewrites and check reordering are outside the
  single-edit experiment (unmeasured fleet-wide).
- **U4** — provenance: no kagi-side opt-in is recorded in kagi's tree at this
  write (O: 0 matches); the dispatch is the record, and the owner's intent is U.
- **U5** — whether a fifth leg is cut into `--regression` (and from which spec)
  is the cadence lane's play, not this write; the tool revision executed here
  (`cf41efaa…`, four legs) is newer than the ledger's recorded one.
- **U6** — the survivor set is spec-bound: other single-edit defects exist
  unmeasured (named: the `--only` missing-value guard arm, §7.2).
- **U7** — the r3 census's "hermetic fallback" wording is now superseded by a
  measurement (this sweep + its control), but the census file itself still
  carries U4 as written; a re-pin errata there is a cadence-lane edit, not this
  write.

## Errata (append-only)

(none yet — new entries go below this line, never edits above)