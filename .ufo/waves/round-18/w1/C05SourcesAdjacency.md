# C05 — sources-check adjacency (case 8)

Axes: depth (is leg 8 a measurement of kumitate's own gate), calibration (do planted defects and their predictions follow that gate's exits). Operability is untouched.

No tools installed.

## Verdict

partial — case 8 measures kumitate's own gate; some plantable defects reimplement fleet E-codes, and the header's W02/W03/overdue correspondence is false on shared fixtures.

## What tameshi may claim

The method, on this file, read-only. Case 7's procedure is the template: ten defects and predictions committed before the sweep, then `tools/mutate-and-run.sh`, then a ledger leg (`corpus/knowledge/mutation-case-kumitate-round-gate.md:1-13,33-36`). The same procedure aimed at `kumitate-shokunin/scripts/sources-check.mjs` is a kumitate `scripts/*` primary surface (`tameshi-shokunin/PROVINCE.md:7-11`). The round-16 append already records that this file exists and is not yet a leg (`PROVINCE.md:51-62`). `tools/mutate-and-run.sh:85-91` lists seven legs and does not name `sources-check` or either `sources-census.sh` (confirmed: `git -C tameshi-shokunin grep` at `183f87b` on that file, no matches). Command D (`SCORECARD.md:73`) counts those comment-shaped legs. An eighth comment of that shape moves `recorded_cases` 7 → 8. The integer does not check who owns the predicate.

Round 17 §7 routes eight other defects (`corpus/lessons/round-17-verifier-spotcheck.md:415-454`). This surface is not among them.

Owner of the gate under test: kumitate. `kumitate-shokunin/PROVINCE.md:15` assigns `scripts/*.mjs` and `corpus/SOURCES.md` (checked by `scripts/sources-check.mjs`) to kumitate. `SKILL.md:605` registers it as an independent gate, contract `kumitate-sources-v1` (`sources-check.mjs:55`). Tameshi does not own the registry rules, the verdict lines, or the file.

Pin checked out of the object store, same blob at HEAD:

```
git -C kumitate-shokunin rev-parse 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs
→ 6b57424fc5a213a01015beaceb97de47a67967f0
git ls-tree 0acb775 … and HEAD → 100755, same blob
sha256sum scripts/sources-check.mjs
→ 6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f
```

`0acb775` (2026-10-19, "round-34: fix SOURCES Markdown row parsing") is the last commit that touches the path. The path was added in `1a8eed5`. HEAD is `1770305`; the blob is unchanged. `git status --porcelain -- scripts/sources-check.mjs` was empty before and after the probes.

Suite that a case-8 kill is graded against: `node scripts/sources-check.mjs --selftest`.

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  node kumitate-shokunin/scripts/sources-check.mjs --selftest
→ exit 0
SOURCES_SELFTEST: 46/46 pass
VERDICT: PASS
PASS lines 46, FAIL 0, SKIP 0
node v24.21.0
```

The parity check inside that suite shells the contract one-liners (`sources-check.mjs:840-871`; contract `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:68-76`). Observed line: `node=4/1/1 awk=4/1/1`. It does not invoke `scripts/sources-census.sh`.

## Who owns which program

| program | owner | bytes observed |
|---|---|---|
| `kumitate-shokunin/scripts/sources-check.mjs` | kumitate | sha256 `6a293a72…258f`, 897 lines, mode 100755, blob `6b57424f…` |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | fleet repo | sha256 `3fb72615…4e30`, 806 lines; last path commit `6a1dd8ce` ("ops: vendor canonical e737d2e…"); fleet HEAD `ae12f330` |
| `kagi-shokunin/corpus/sources-census.sh` | kagi | sha256 `03fb300a…6b3c`, 450 lines; `git ls-tree HEAD` → `100755` blob `7bcdb817…`; path commit `e1544c19`; kagi HEAD `c2cab35` |

Fleet script: SOURCES-CONTRACT-v1 census across child lanes (`sources-census.sh:2-18`). Modes census / validate / overdue / shared. E01–E12 and W01–W04. W-codes do not change status (`:16-18`, `:737-745`). Overdue is a separate mode and does change status (`:773-777`).

Kagi script: lane gate. Header says the contract awk is embedded verbatim and the cross-file checks are this gate's (`kagi-shokunin/corpus/sources-census.sh:4-13`; kagi `PROVINCE.md:53`). Findings include `SC_CREDENTIAL` (`:67-71,125-128`). Credential material is kagi's, and tameshi's province sends it there (`tameshi-shokunin/PROVINCE.md:18`). The recorded kagi census leg is `bash-surface-census` → `corpus/surface-census.sh` (`mutate-and-run.sh:86`), a different file (`mutation-case-kagi-census.md:10-11`).

## Fixture falsifier

Scratch: `/tmp/tameshi-r18w1-C05SourcesAdjacency-sTkxUo`. Same row shape, `--today 2026-10-19`, all `GIT_*` unset. Fleet via `validate|overdue --file`, kumitate via `--self`, kagi via `verify --root`. Clean control: all three exit 0.

| fixture | fleet | kumitate | kagi |
|---|---|---|---|
| clean mined row + sourced `alpha.md` | validate 0 `ok`; overdue 0 cadence | 0 `CLEAN` | 0 `CLEAN` |
| rejected, long `REJECTED:` , no `flip:` | validate 0 `ok` | 1 `REJECTED_NO_FLIP` | 1 `SC_REJECT_SHAPE` |
| rejected teaches `no` (length 2) | validate 0, prints `W02`, still `ok` | 1 `REJECTED_NO_REASON,REJECTED_NO_FLIP` | 1 `SC_REJECT_SHAPE` |
| mined `used-by` `—`, headerless `cost-and-profile.md` | validate 0, prints `W03`, still `ok` | 1 `MINED_UNUSED` | 1 `SC_MINED_UNUSED` |
| ISO recheck `2026-10-19` (due today) | validate 0; overdue 1 `S001 0d` | 0 `CLEAN` | 0 `CLEAN` |
| opened `2026-10-18` + `1d` (due today) | overdue 1 `S001 0d` | 0 `CLEAN` | 0 `CLEAN` |
| recheck `annual` | validate 0; overdue 0 cadence | 1 `RECHECK_INVALID` | 0 `CLEAN` |
| opened `2026-02-30` | validate 1 `E08` | 1 `OPENED_INVALID` | 0 `CLEAN` `legacy=1` |
| `community` at tier A | validate 1 `E10` | 1 `TIER_INFLATION` | 1 `SC_INFLATION` |
| mined `used-by` `../outside/outside.md` (file exists) | validate 0 `ok` | 1 `USED_BY_MISSING` | 1 `SC_USEDBY_MISSING` (not a repo corpus path) |
| new headerless `corpus/knowledge/new-note.md` | validate 0 `ok` | 1 `ENTRY_HEADER_REQUIRED` | 0 `CLEAN` `legacy=1` |

`[ -e escape/../outside/outside.md ]` was yes, so fleet E11 stayed silent because the path exists (`sources-census.sh:566-568`). Kumitate `repoPathExists` rejects `..` (`sources-check.mjs:161-165`).

Code that the table is executing:

- Fleet W02 is `status=="rejected" && length(teaches)<8` (`sources-census.sh:671-672`). Kumitate's header calls `REJECTED_NO_FLIP` fleet W02 (`sources-check.mjs:24,33-34`). The flip check is `\bflip:` (`:326-327`). Kagi requires a `REJECTED:` prefix and a `flip:` substring (`sources-census.sh:189-190`), which is the contract sentence (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:34-35`).
- Fleet W03 is mined and `usedby=="—"` only, and it is a warning (`sources-census.sh:673-674`). Kumitate `MINED_UNUSED` is an error for `""` or `—` (`sources-check.mjs:311-313`).
- Fleet overdue fires on `due<=today_s` (`:684`; header `:35` "on/after"; selftest `:147` expects `S002 0d`). Kumitate warns only when the day is strictly before today (`sources-check.mjs:330-335`); its own suite asserts exactly-today is clean (`:777-781`).
- Fleet `symbolic()` accepts `annual` (`:582`, selftest `:149`). Kumitate accepts an ISO date, `Nd`, or the token `on-release` (`:306-309`). Kagi's embedded census awk does not judge the recheck cell.
- Opened-date validity is fleet E08 (`:660-662`) and kumitate `OPENED_INVALID` (`:302-305`). The contract one-liners and the kagi gate do not check it.
- Tier inflation agrees: contract `:30`, fleet E10 `:668`, kumitate `:298-300`, kagi `SC_INFLATION`.
- A headerless file outside the frozen 38-path list is kumitate `ENTRY_HEADER_REQUIRED` (`sources-check.mjs:61-101,360-366`). Kagi counts every file with no column-1 `source:` as legacy and skips it (`kagi …/sources-census.sh:62-64,212`).

So a defect tameshi plants is an edit to kumitate's file. Whether that edit corresponds to fleet-owned semantics depends on which predicate it cuts:

- Fleet-script-hosted (fixture verdict matched fleet): `TIER_INFLATION` / E10, `OPENED_INVALID` / E08. The same class, from the two sources rather than from this run, is E01–E03, E05–E07, E11 for an in-root missing path, and E12 (`sources-check.mjs:10-22` names those codes; fleet implements them at `:635-668` and `:618-622`). A kill shows kumitate's 46-check suite noticed the edit. It is still a result about this suite. Fleet `scripts/sources-census.sh` did not run inside the suite.
- Shared with kagi, and the fleet process stayed exit 0: missing `flip:`, mined `—`, a `../` used-by that exists on disk.
- Kumitate's own clause: `annual` rejected, a new headerless knowledge file rejected, overdue silent on the due date. Fleet and kagi both stayed clean on `annual` and on the new headerless file. Fleet overdue exited 1 on the due date while kumitate exited 0.

Absent from kumitate, so a case-8 mutant cannot be "the fleet check, removed": E04 duplicate URL+scope, W01 tier-C mined, W04 cross-scope URL, the shared-URL mode, the lane roster (`sources-census.sh:24-38`). The header already says E04 and W01 are outside this contract (`sources-check.mjs:34`). Absent from kumitate and owned by kagi: `SC_CREDENTIAL`, the both-directions cite handshake, tier A/B as sole support, and the `corpus/(knowledge|lessons)/` path shape (`kagi …/sources-census.sh:39-55,185-231`).

## Proposed move

In the case-8 spec, before any mutant runs, tag each of the ten defects with one of those three labels and predict only the exit of `node scripts/sources-check.mjs --selftest`. Keep fleet W-code status and `due<=today` out of the prediction column. The ledger sentence records an eighth case of kumitate `scripts/sources-check.mjs`.

That raises calibration: the false W02/W03/overdue map in `sources-check.mjs:23-36` cannot be copied into the prediction table (a fleet-shaped prediction expects exit 0 where this suite exits 1, and exit 1 on the due date where this suite exits 0). Depth still moves, because command D counts the leg, and the target remains the kumitate gate case 7's procedure already allows. Operability is unchanged. The sibling header stays unedited.

Risk: command D will count a mislabeled leg. The tag is the part that keeps the claim honest. A mutant that only deletes `TIER_INFLATION` is a real suite kill of a contract rule all three programs implement; publishing that kill as a result about `scripts/sources-census.sh` or `kagi-shokunin/corpus/sources-census.sh` assigns the measurement to the wrong owner.

Verification already run is the table above (exits and verdict lines) plus the 46/46 control. After a spec exists, each `@old` string should occur once in blob `6b57424f…`, and each prediction should name a kumitate selftest exit.

partial — case 8 measures kumitate's own gate; some plantable defects reimplement fleet E-codes, and the header's W02/W03/overdue correspondence is false on shared fixtures.
