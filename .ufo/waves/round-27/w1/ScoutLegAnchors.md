# ScoutLegAnchors — round 27, wave 1: specification anchors for the other eight legs

Seat: TameshiR27.ScoutLegAnchors (scout, leaf). Content revision
`2227d8338c02aa9a5fd7d95c1a41b76865ad7647`. Read-only: no production file, no lane
file and no sibling repo was written.

## Verdict

The eight legs name **35 surviving defects**, and each lane treats its survivors as suite
holes in its own words ("measured gaps", "read by nothing", "unreached arm", "hole-aimed").
**17 of the 35** are held by a header or usage line that states the expected
behaviour outright; **6 more** follow only by definition, label order or arithmetic;
**12 have no contract anchor at all** and their hole call rests on the pristine run
(state-anchored, the S012 sense). The 12 unanchored rows are concentrated in two legs:
checklist-run (4) and claims-check (2 of 3), with surface-census, mado-verify,
round-gate and sources-check contributing one or two each. The distribution below is
planning data for the next F8 move: an anchored survivor can be re-judged without a new
run of the pristine; an unanchored one cannot.

## Scope and method

- Legs and pins read from `tools/mutate-and-run.sh:603-620` (observed: `PIN_JS` at :603,
  `REV_JS` :604, `PIN_BASH` :605, `REV_BASH` :606, `PIN_TSUKUROI` :607, `REV_TSUKUROI`
  :608, `PIN_MADO` :609, `REV_MADO` :610, `PIN_CHECKLIST` :611, `REV_CHECKLIST` :612,
  `PIN_CLAIMS` :613, `REV_CLAIMS` :614, `PIN_ROUNDGATE` :615, `REV_ROUNDGATE` :616,
  `PIN_SOURCESCHECK` :617, `REV_SOURCESCHECK` :618, `PIN_CITECHECK` :619, `REV_CITECHECK`
  :620). The ninth leg, `js-cite-check`, is outside this item's list of eight and is not
  classified here.
- Blobs materialised with `GIT_OPTIONAL_LOCKS=0 git -C <repo> show <rev>:<path>` and
  checked against the recorded pins. Observed sha256 of the eight materialised files:
  `83016d45…4f426` (kimi), `275d8294…53009f` (surface), `084951be…c78c5` (tsukuroi),
  `d7edaab4…d0e13` (mado), `7e5ec98b…576bf` (checklist), `e9a21b44…0f61b` (claims),
  `f890e277…d3e9` (round-gate), `6a293a72…258f` (sources). All eight equal the pin
  constants.
- Survivor sets cross-checked against the recorded tables `TABLE_*` at
  `tools/mutate-and-run.sh:621-628` and against §1 of each case note. The counts are
  2 + 2 + 4 + 6 + 8 + 3 + 5 + 5 = 35.
- "Anchor" uses the round's own vocabulary (`corpus/knowledge/oracle-anchored-survivors.md`
  §2 and §5): a **contract** anchor is a header comment line or the gate's usage text of
  the pinned blob, fixed outside the mutated statement. The entry's bound applies: header
  comments are written by the same owner as the code, so they are contract-anchored, not
  independent-specification anchored.
- Three values in the table: **YES** = a quoted header/usage line states the behaviour the
  mutant breaks; **DERIVED** = the expectation follows only from a definition, a label
  order or arithmetic on header facts; **NONE** = no header/usage statement, so the hole
  call is differential.

## Table

`rev` is the leg's `REV_*`; `site` is the recorded mutation site on that rev. "Lane's hole
call" cites the case note line that named the survivor a gap or hole.

### 1. kimi-census — `kumitate-shokunin/scripts/kimi-census.mjs` @ `175de6ba`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| D2 (cap 6→5) | :378 `findings.slice(0, 6)` | `mutation-case-kimi-census.md:135-137` "The verdict-line truncation boundary and its `+N more` arithmetic (D2)" | **YES** | `kimi-census.mjs@175de6ba:71` — "KIMI_CENSUS: DRIFT (<KIND> <id>; …)            at most 6 findings, then `+N more`" |
| D10 (FROZEN.K2 25→24) | :145 `const FROZEN = { K1: 3, K2: 25, … }` | `mutation-case-kimi-census.md:138-139` "Frozen-block constants other than K5 (D10): only `frozen.K5` is asserted" | **DERIVED** | `kimi-census.mjs@175de6ba:24-31` — "the counts are read live and total 49 … `agents/secondary/` = 18 lane files, `skills/` = 5 entries … K2 = the 18 files under `agents/secondary/` … the 5 entries under `skills/` …, plus `plugins/installed.json` and the `plugins/managed/kimi-webbridge` tree as one presence-only member." No line states `K2 = 25`; 25 is the enumeration (18+5+1+1) and the :8/:157 total 49 |

### 2. surface-census — `kagi-shokunin/corpus/surface-census.sh` @ `fecee874`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| B5 (exec x-bit arm deleted) | :214-217 | `mutation-case-kagi-census.md:149-150` "The exec x-bit arm (B5): fixture-absent; real drift … would be reported `SURFACE OK`" | **YES** | `surface-census.sh@fecee874:17` — `kind:  file \| dir \| exec   (exec = regular file carrying u+x)`; :10-11 — "v1 compares the live host against two committed data files and exits non-zero on any change" |
| B10 (CLEAN summary `ok=` arg → `$N_ABSENT`) | :862 | `mutation-case-kagi-census.md:151-152` "The CLEAN/DRIFT summary counts (B10): `ok=`/`absent=`/`skipped=` … are reported, never read" | **NONE** | Header documents only the verdict vocabulary (:32-37) and the exit map (:37-38). No line states the CLEAN summary's argument order or that `ok=` carries `N_OK` |

### 3. tsukuroi-census — `tsukuroi-shokunin/tools/tsukuroi-census.sh` @ `165307fe`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| B7 (SAMPLE_N 8→9) | :160 `SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}` | `mutation-case-tsukuroi-census.md:137-139` (cap unreached); :181 "the sample inventory (B7's only trace)" | **YES** | `tsukuroi-census.sh@165307fe:36` — "probe   pacman -Qkk over a bounded sample of `pacman -Qq` (SAMPLE_N=8, default)"; usage :182 — "`--sample N` … (default 8)" |
| B8 (usage refusal exit 2→1) | :935 | `mutation-case-tsukuroi-census.md:144-147` "The parser (`:921-937`) is never [run]" | **YES** | `tsukuroi-census.sh@165307fe:31` — "Usage errors also exit 2."; usage :185 — "Exit map:     0 HEALTHY \| 1 DEGRADED \| 2 BLOCKED (worst plane wins; usage errors also 2)" |
| B9 (roll-line args PKG_V/SYS_V swapped) | :967 | `mutation-case-tsukuroi-census.md:149-152` "wrong plane attribution for any consumer reading the fields" | **DERIVED** | usage `tsukuroi-census.sh@165307fe:184` — "Verdict line: TSUKUROI_CENSUS: HEALTHY\|DEGRADED\|BLOCKED (packages=.. systemd=.. drivers=.. journal=..)". Field labels and order only; no line binds `packages=` to the packages plane verdict |
| B10 (PCI-unreadable branch → silent `absent(pci_10de=0)`) | :487-493 | `mutation-case-tsukuroi-census.md:157-159` "a full verdict flip (BLOCKED→HEALTHY) on an unreadable inventory, precisely the anti-claim the gate documents (`:79-80`)" | **YES** | `tsukuroi-census.sh@165307fe:77-80` — "block … nvidia hardware in PCI but core function offline …, or PCI inventory unreadable with no other positive evidence" |

### 4. mado-verify — `mado-shokunin/tools/mado-verify.sh` @ `eead56b2`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| D3 (skipped live row SKIP→PASS) | :588 | `mutation-case-mado-verify.md:117-120` "D3 — class: row status on an unread row" | **DERIVED** | `mado-verify.sh@eead56b2:25-26` — "Anti-claim: a plane that cannot be verified reads UNKNOWN and blocks CLEAN — never a fake CLEAN". The header fixes "not a pass" for an unverified plane; the gate's own token for the deliberate skip is SKIP, which no header line states |
| D5 (failing `--selftest` returns 1) | :429 `return 2` | `mutation-case-mado-verify.md:121-124` "D5 — class: failure-path exit code unobservable" | **YES** | `mado-verify.sh@eead56b2:13` — "2 = tool/usage error (bad args; a failing --selftest)." |
| D7 (include count `-ne`→`-lt`) | :484 | `mutation-case-mado-verify.md:126-129` "D7 — class: count/tolerance boundary never reached" | **YES** | `mado-verify.sh@eead56b2:33-34` — "hypr    — hyprland.conf is a pure orchestrator: 17 source statements in the exact include order (MADO-1 §1/§3)" |
| D8 (conf sha pin always "matches") | :574 | `mutation-case-mado-verify.md:131-134` "D8 — class: record-level NOTE row, no assert" | **DERIVED** | `mado-verify.sh@eead56b2:52-54` — "pins    — Hyprland 0.56.2 commit efb5099…, waybar v0.15.0, walker 2.17.0 (SKILL.md "Version pins"): a changed pin is a FAIL". The header's pin rule covers version pins and says FAIL; the mutated site is the `hyprland.conf` file-sha NOTE, a form the header does not state (tension recorded, not resolved here) |
| D9 (boundary comparison always identical) | :738 | `mutation-case-mado-verify.md:135-138` "D9 — class: safety row asserted only in its PASS direction" | **NONE** | Header states the read-only property (`:22-24` "READ-ONLY on every substrate … no file is written") but not the before/after comparison or its FAIL branch. A comparison that cannot fail does not contradict the stated property |
| R1 (tomllib arm UNKNOWN→PASS) | :651 | `mutation-case-mado-verify.md:140-143` "a PASS row whose detail says the reader is missing is exactly the fake-pass the gate's header forbids" | **YES** | `mado-verify.sh@eead56b2:25-26` — "a plane that cannot be verified reads UNKNOWN and blocks CLEAN — never a fake CLEAN" |

### 5. checklist-run — `kagi-shokunin/corpus/checklist-run.sh` @ `fecee874`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| A1 (section stop `'## '*`→`'## '`) | :107 | `mutation-case-kagi-checklist.md:183` probe (7 items, 6 rows); :218 survivor census class (b) | **DERIVED** | `checklist-run.sh@fecee874:4` — "`SKILL.md` §Credential-hygiene checklist holds 16 items."; :22-25 — "The mapping is a bijection over the 16 items: one row per item, one item per row … an item no row matches, is a defect." The 16-item set is stated; the extraction delimiter that A1 widens is not |
| B1 (id charset `^[A-Z][0-9]+$`) | :139 | `mutation-case-kagi-checklist.md:184` probe ("row id `AB1` … accepted") | **NONE** | Header gives the columns only (`:10-11` `id <TAB> class <TAB> lead …`); no id grammar anywhere in header or usage |
| B3 (deny list drops `the-janitor stop`) | :75 | `mutation-case-kagi-checklist.md:185` probe; :221 "the deny-list drop (B3) is the first secret-hygiene surface … re-openable" | **YES** | `checklist-run.sh@fecee874:42` — "any `check` naming op.env, `op run\|read\|inject`, a handler start/stop/run or the ledger gate" |
| C1 (UNMATCHED-ITEM never emitted) | :226 | `mutation-case-kagi-checklist.md:186` probe; class (a) at :218 | **YES** | `checklist-run.sh@fecee874:24-25` — "a row whose lead matches nothing, or an item no row matches, is a defect." |
| D1 (`floor_of` truncates) | :174 | `mutation-case-kagi-checklist.md:187` probe ("the floor cell lies by one on odd counts") | **NONE** | Header shows the field `CHECKLIST_RATIO: … floor=F …` (`:28`) without a definition; the only "ceil" statement is the code comment `checklist-run.sh@fecee874:73` — code, not header or usage |
| E2 (row capture drops `2>&1`) | :261 | `mutation-case-kagi-checklist.md:188` probe ("row prints its verdict on stderr only") | **NONE** | Header `:13-14` says "expect_last = ERE matched against the last non-blank **stdout** line of the check". No header line requires stderr capture; the wording points at the mutant, not at the pristine |
| F2 (`--only` BROKEN line prints `failed=0`) | :285 | `mutation-case-kagi-checklist.md:189` probe | **NONE** | Header `:37-38` prints `CHECKLIST_ROW: CLEAN\|BROKEN (id=…)`; the `failed=` field the mutant falsifies is not in the stated shape |
| G1 (unknown argument exit 2→0) | :88 | `mutation-case-kagi-checklist.md:190` probe; :220 "a CLI fail-open (G1)" | **YES** | `checklist-run.sh@fecee874:39` — "Exit      0 clean · 1 item or declaration defect · 2 usage/setup/shape" |

### 6. claims-check — `kumitate-shokunin/scripts/claims-check.mjs` @ `175de6ba`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| D7 (DRIFT cap 6→5) | :431 `shown.slice(0, 6)` | `mutation-case-kumitate-claims.md:142-145`; :197 "The DRIFT line's `+N more` tail and its arithmetic (D7)" | **YES** | `claims-check.mjs@175de6ba:53` — "CLAIMS: DRIFT (<KIND> row=<ID> detail; …)   at most 6 findings, then `+N more`" |
| D8 (symbol floor 3→2) | :382 `t.length >= 3` | `mutation-case-kumitate-claims.md:150-155`; :198 "the symbol floor's semantics (D8 …)" | **NONE** | Header `:34` — "SECTION_NO_SYMBOL        no backticked symbol is verbatim in the file". No header line defines symbol eligibility or a minimum length |
| D9 (guard drops `unresolved` from the sum) | :315 | `mutation-case-kumitate-claims.md:160-163`; :208 "the unresolved-sum guard (D9)" | **NONE** | Header `:27` — "NOTE_MISSING             a cell's explicit `knowledge/x.md` has no file". The prose-only cell shape the guard covers is not stated |

### 7. round-gate — `kumitate-shokunin/scripts/round-gate.mjs` @ `364f1d59`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| C1059 (REPORT_MIN_BYTES 1024→1059) | :167 | `mutation-case-kumitate-round-gate.md:84-86` "the edge pair … 1059 survived"; §4 probe row | **YES** | `round-gate.mjs@364f1d59:69` — "error   REPORT_THIN             report < 1024 bytes (`(bytes=<n>)`)." |
| A2 (FAIL-CLOSED tail gains `detail: `) | :617 | `mutation-case-kumitate-round-gate.md:100-104` §4 probe P1/P1b | **NONE** | Header lists fail-closed tokens (`:115-119`) and names the `--json` shape (`:128`), but no text-mode `ROUND_GATE: FAIL-CLOSED (token) detail` format; usage `:177-183` carries only the exit map |
| B2 (tracked `REPORTS_DIR_MISSING`→`MAIN_REPO_NOT_GIT`) | :527 | `mutation-case-kumitate-round-gate.md:92-95` "the same one-token edit … survives at the tracked-mode site, because no fixture runs `--tracked` with a missing reports dir" | **NONE** | Header `:115-116` lists both tokens but binds neither to a mode; only `NO_FILED_REPORTS` is explained (`:117-119`). No line says tracked mode with a missing reports dir must emit `REPORTS_DIR_MISSING` |
| CKIND (`TREE_DIRTY` dropped from `FINDING_KINDS`) | :175 | `mutation-case-kumitate-round-gate.md:95-98` "The meta-check is one-sided (CKIND)" | **YES** | `round-gate.mjs@364f1d59:91` — "error   TREE_DIRTY         close: `git status --porcelain` non-empty (first 5 entries named)." |
| E1 (`UFO_SRC` set-value resolves the canonical candidate) | :163 | `mutation-case-kumitate-round-gate.md:100-104` §4 probe P9 | **YES** | `round-gate.mjs@364f1d59:58-59` — "--origin      UFO_SRC               else the first existing of ~/Projects/ufo-fsd-alpha and ~/Projects/origin-work/ufo-fsd-alpha" |

### 8. sources-check — `kumitate-shokunin/scripts/sources-check.mjs` @ `0acb7752`

| survivor | site | lane's hole call | spec anchor? | anchor `path@rev:line` — quote |
|---|---|---|---|---|
| S_KIND (`RECHECK_OVERDUE` dropped from `FINDING_KINDS`) | :114 | `mutation-case-kumitate-sources-check.md:129-135` "the kind-coverage meta-check is one-sided … Removing a declared kind passes the meta-check" | **YES** | `sources-check.mjs@0acb7752:31` — "RECHECK_OVERDUE      — an ISO recheck date or opened + Nd is before today" (declared as a warn finding) |
| S_VERDICT (DRIFT line `(…)`→`[…]`) | :483 | `mutation-case-kumitate-sources-check.md:136-137` "no case pins the DRIFT verdict line" | **YES** | `sources-check.mjs@0acb7752:41` — "SOURCES_CHECK: DRIFT (<kind list>)" |
| S_DUP_LINE (duplicate reported at `index + 2`) | :251 | `mutation-case-kumitate-sources-check.md:138-139` "no case asserts a finding's `line`/`:N` location" | **NONE** | Header `:13` — "ID_DUPLICATE        E03  an otherwise well-formed registry id is repeated". No line-number field is stated for any finding |
| S_ENTRY_COUNT (`entriesWithSource += 2`) | :368 | `mutation-case-kumitate-sources-check.md:140-143` "a positive `entriesWithSource` is not pinned" | **DERIVED** | `sources-check.mjs@0acb7752:40` — "SOURCES_CHECK: CLEAN (… entries_with_source=k legacy=l)". The field is contract-visible; what `k` counts is carried by the name only |
| S_FILE_READ (per-entry read failure → `SOURCES_MISSING`) | :356 | `mutation-case-kumitate-sources-check.md:143-145` "the per-entry read arm is not reached" | **NONE** | Header states only "SOURCES_CHECK: FAIL-CLOSED (<kind>)" (`:42`) and the usage exit map. `SOURCES_MISSING` vs `READ_FAILED` is not distinguished in header or usage |

## Count

| leg | survivors | YES | DERIVED | NONE |
|---|---|---|---|---|
| kimi-census | 2 | 1 (D2) | 1 (D10) | 0 |
| surface-census | 2 | 1 (B5) | 0 | 1 (B10) |
| tsukuroi-census | 4 | 3 (B7, B8, B10) | 1 (B9) | 0 |
| mado-verify | 6 | 3 (D5, D7, R1) | 2 (D3, D8) | 1 (D9) |
| checklist-run | 8 | 3 (B3, C1, G1) | 1 (A1) | 4 (B1, D1, E2, F2) |
| claims-check | 3 | 1 (D7) | 0 | 2 (D8, D9) |
| round-gate | 5 | 3 (C1059, CKIND, E1) | 0 | 2 (A2, B2) |
| sources-check | 5 | 2 (S_KIND, S_VERDICT) | 1 (S_ENTRY_COUNT) | 2 (S_DUP_LINE, S_FILE_READ) |
| **total** | **35** | **17** | **6** | **12** |

Reading: **17/35 = 49 %** of the recorded survivors have an explicit header/usage anchor;
**23/35 = 66 %** have an anchor of any strength; **12/35** would be state-anchored if
re-judged the round-26 way. The unanchored set is not spread evenly: checklist-run alone
holds 4 of the 12, and claims-check holds 2 of its 3.

## Evidence (commands and observed output)

Blob materialisation and pin check (one command per leg, run from
`/home/vgpnk/Projects/shokunin`):

```
GIT_OPTIONAL_LOCKS=0 git -C kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C tsukuroi-shokunin show 165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C mado-shokunin show eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs | sha256sum
GIT_OPTIONAL_LOCKS=0 git -C kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs | sha256sum
```

Observed, matching `PIN_*` one for one:

```
83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426  kimi.mjs
275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f  surface.sh
084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5  tsukuroi.sh
d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13  mado.sh
7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf  checklist.sh
e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b  claims.mjs
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  roundgate.mjs
6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f  sources.mjs
```

Survivor sets observed in the runner (`sed -n '621,628p' tools/mutate-and-run.sh`):
`TABLE_JS` survivors D2, D10; `TABLE_BASH` B5, B10; `TABLE_TSUKUROI` B7–B10; `TABLE_MADO`
D3, D5, D7, D8, D9, R1; `TABLE_CHECKLIST` A1, B1, B3, C1, D1, E2, F2, G1; `TABLE_CLAIMS`
D7, D8, D9; `TABLE_ROUNDGATE` C1059, A2, B2, CKIND, E1; `TABLE_SOURCESCHECK` S_KIND,
S_VERDICT, S_DUP_LINE, S_ENTRY_COUNT, S_FILE_READ.

Anchor lines were read from the sha-verified copies with `awk 'NR==…'` on the materialised
blobs; the quotes in the table are verbatim excerpts, with `…` marking elided text. Sample
(kimi + mado):

```
$ awk 'NR==71' kimi.mjs
 *   KIMI_CENSUS: DRIFT (<KIND> <id>; …)            at most 6 findings, then `+N more`
$ awk 'NR==13' mado.sh
# UNVERIFIABLE) · 2 = tool/usage error (bad args; a failing --selftest).
$ awk 'NR==25||NR==26' mado.sh
#   * Anti-claim: a plane that cannot be verified reads UNKNOWN and blocks
#     CLEAN — never a fake CLEAN (SKILL safety rule 5).
```

No tool was installed or upgraded for this item.

## Smallest safe correction (recommendation to the L1; nothing applied)

For the next F8 move, split the 35 hole calls by anchor status rather than by leg:

1. **Re-judge the 17 YES rows without a new containment run.** Each has a header/usage
   line the mutant contradicts, and the line is outside the mutated statement, so the
   anchoring recipe in `oracle-anchored-survivors.md` §2 applies unchanged. This is the
   cheapest wave: no fixture design is needed, only a witness input per row and an
   expectation read off the quoted line.
2. **Treat the 6 DERIVED rows as anchor-strength labels, not as YES.** D10 (kimi) needs an
   arithmetic anchor (the K2 enumeration and total 49); B9 (tsukuroi) and S_ENTRY_COUNT
   (sources) rest on label names; A1 (checklist) rests on the 16-item set; mado D3 and D8
   rest on general rules whose exact token or row form is unstated. Record them as
   `derived` in the entry, the way S_PIN_INCLUDES is recorded as convention-only.
3. **Route the 12 NONE rows to the gate owners as unanchored holes** (checklist B1, D1,
   E2, F2; claims D8, D9; surface B10; mado D9; round-gate A2, B2; sources S_DUP_LINE,
   S_FILE_READ). Each needs either a header/usage sentence that states the expected
   behaviour or an external anchor; without one, a hole call is differential.
4. **Two rows need a wording decision before they can anchor anything.** checklist E2's
   header says `expect_last` matches the last non-blank **stdout** line (`:13-14`) while
   the pristine captures `2>&1`; the header currently points at the mutant. mado D8's
   header pin rule says a changed pin is a FAIL (`:52-54`) while the file-plane sha pin is
   implemented as a NOTE (`:574-577`); the header and the implementation disagree about
   the row's severity. Neither is this scout's call to change.

## Unknowns and limits

- Anchors are **O** (line numbers and quotes read from sha-verified pinned blobs) plus **I**
  (the judgement that a quoted line states the behaviour the mutant breaks). The 17/6/12
  split is that judgement applied uniformly; a different reader could move a row between
  YES and DERIVED, most plausibly mado D3, mado D8 and checklist A1.
- One reading per anchor line; header line numbers move with the file, so a re-pin needs a
  re-read of the quoted lines (the round-27 entry already records this bound).
- Header/usage text is written by the gate owner. A contract anchor is not an independent
  specification; the entry's §5 bound applies to all 17 YES rows equally.
- I did not re-run any suite or mutant. The mutation sites are the recorded `@old`/`@new`
  pairs at `tools/mutate-and-run.sh:657-1081` (the eight legs in scope; the ninth leg's
  spec begins at :1082); each was checked against the pinned blob's line content where
  the table quotes a line, not by applying the edit.
- The ninth leg `js-cite-check` (`PIN_CITECHECK` :619, `REV_CITECHECK` :620) is outside the
  eight named in this item and is not counted.
- Whether a header sentence can be added without changing the gate's version pin is the L1
  and gate owner's decision; I made no edit.
