# F6 next-move census — survivors whose kill needs a fixture the suite lacks

Scope: the nine legs named in `tools/mutate-and-run.sh` @ `9f3084bc60ad56aac01e4556ef4c7653df2f65e5` lines 84-100; survivor records in `corpus/knowledge/mutation-case-*.md`; leg pins read from the same blob lines 603-620. O: every path:line and pin below was read at `9f3084bc` or in the lane working tree. I: the size estimates and the rank order. No fixture was built, minimized or run for this report.

Verdict: 24 of the 40 recorded survivors have a kill that needs an input or case the suite never builds (Table 2, ranked); the other 16 are assert-, pin-, check-side or equivalent and are listed with reasons in Table 3. Rank 1 (kagi B5) is the already-owned C2 build.

## Table 1 — the nine leg pins

| Leg | Target | Rev | Blob sha256 (16) |
|---|---|---|---|
| L1 js-kimi-census | kumitate-shokunin/scripts/kimi-census.mjs | 175de6ba2e9e904010411b19cab27e0af9aad3d4 | 83016d45…2724f426 |
| L2 bash-surface-census | kagi-shokunin/corpus/surface-census.sh | fecee8743e52eb8fb5fbb40782934cb619a1a96e | 275d8294…db53009f |
| L3 bash-tsukuroi-census | tsukuroi-shokunin/tools/tsukuroi-census.sh | 165307fe4746a8807b02ec4a7d7ecac0368454a6 | 084951be…809c78c5 |
| L4 bash-mado-verify | mado-shokunin/tools/mado-verify.sh | eead56b20ad2b28299ae4fa623d52a99b44c743c | d7edaab4…e32d0e13 |
| L5 bash-checklist-run | kagi-shokunin/corpus/checklist-run.sh | fecee8743e52eb8fb5fbb40782934cb619a1a96e | 7e5ec98b…2fd576bf |
| L6 js-claims-check | kumitate-shokunin/scripts/claims-check.mjs | 175de6ba2e9e904010411b19cab27e0af9aad3d4 | e9a21b44…21b0f61b |
| L7 js-round-gate | kumitate-shokunin/scripts/round-gate.mjs | 364f1d5954158ef8844bca4a5fef57b05d2f2ca5 | f890e277…a834d3e9 |
| L8 js-sources-check | kumitate-shokunin/scripts/sources-check.mjs | 0acb7752d19058b953ebbeba253b1e35f6548de5 | 6a293a72…f37e258f |
| L9 js-cite-check | kumitate-shokunin/scripts/cite-check.mjs | 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a | 40573448…c7c10c9f |

## Table 2 — ranked next F6 moves (fixture the suite lacks)

Rank ascending by expected fixture size (smallest first). The fixture column states the killing input; the last column estimates its size from the note's own probe description.

| Rank | Survivor | Leg | Note evidence (path:line) | Fixture the suite lacks (kill shape) | Est. fixture size |
|---|---|---|---|---|---|
| 1 | B5 exec x-bit arm | L2 | corpus/knowledge/mutation-case-kagi-census.md:71, :107-116 | census row declared `exec` whose live file lost +x (probe row `asset exec -`, file at mode 644) | 1 row + 1 file mode; C2 already owns this build |
| 2 | D7 include tolerance | L4 | corpus/knowledge/mutation-case-mado-verify.md:86, :126-129 | clean fixture plus one undeclared 18th `source =` line | 1 line |
| 3 | D8 assert-blind threshold | L6 | corpus/knowledge/mutation-case-kumitate-claims.md:150-155 | the case's own 2-char `AB` token present in the section file (recorded class (a); input never built) | 1 token |
| 4 | B1 id shape | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:184, :251 | one row id `AB1` (two letters) | 1 row |
| 5 | A1 section stop | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:183, :243-244 | one bullet after the `##` stop (7 items against 6 rows) | 1 bullet + 1 row |
| 6 | D1 odd-count floor | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:187, :249-250 | 5-item section, 3 runnable + 2 by-hand | 1 section |
| 7 | G1 unknown argument | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:190, :239-240 | one `--definitely-not-a-mode` invocation (mode loop untested across all 34 cases) | 1 invocation |
| 8 | B8 usage refusal | L3 | corpus/knowledge/mutation-case-tsukuroi-census.md:97, :144-148 | one `--bogus` invocation (parser at `:921-937` never exercised) | 1 invocation |
| 9 | E1 UFO_SRC arm | L7 | corpus/knowledge/mutation-case-kumitate-round-gate.md:68, :109, :150 | one run with `UFO_SRC` set to a value (cleanEnv deletes it; fixtures set only empty) | 1 env value |
| 10 | S_OOR_EDGE | L9 | corpus/knowledge/mutation-case-kumitate-cite-check.md:53, :89 | one citation at line n+1 of an n-line file (`:21` of 20 lines) | 1 citation line |
| 11 | S_PIN_INCLUDES | L9 | corpus/knowledge/mutation-case-kumitate-cite-check.md:57, :92 | one pin that is an interior slice of the file digest | 1 pin value |
| 12 | S_FILE_READ | L8 | corpus/knowledge/mutation-case-kumitate-sources-check.md:103, :142, :163, :239 | readable SOURCES.md plus one knowledge entry at mode 0o000 that reaches the per-entry read arm (the existing READ_FAILED fixture returns at readdirSync) | 1 entry file + mode; killing check code is proven in .ufo/waves/round-18/w2/KumitateRouting.md |
| 13 | S_USAGE | L9 | corpus/knowledge/mutation-case-kumitate-cite-check.md:56, :91 | an unknown-flag invocation pinned to exit 64; no hermetic case pins the usage exit | 1 invocation + exit pin |
| 14 | D9 unresolved arm | L6 | corpus/knowledge/mutation-case-kumitate-claims.md:160-169 | covered cell `yes — round-11-reading` with one bare stem that resolves nowhere (the guard at `:315` is never entered) | 1 covered cell + 1 stem |
| 15 | D7 cap unreached | L6 | corpus/knowledge/mutation-case-kumitate-claims.md:142-147 | one live section plus seven unresolved headings (7 findings; max in-suite is 3) | 1 section + 7 headings |
| 16 | B3 deny-list | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:185, :234-238 | one row per uncovered deny-list alternative (fixtures cover 3 of 8) | 5 rows or a refusal loop |
| 17 | R1 tomllib arm | L4 | corpus/knowledge/mutation-case-mado-verify.md:89, :140-144 | PATH python3 wrapper that fails any tomllib read (no scenario removes python3/tomllib) | 1 env stub |
| 18 | D5 failing-selftest exit | L4 | corpus/knowledge/mutation-case-mado-verify.md:84, :121-125 | scenario where `--selftest` itself fails (probe: no-op `sed` on PATH) plus an exit-2 case | 1 env stub + 1 case |
| 19 | B10 PCI-unreadable | L3 | corpus/knowledge/mutation-case-tsukuroi-census.md:99, :157-165 | fixture whose pci dir is a missing path (every fixture mkdirs it; the -1 sentinel never returns) | 1 fixture path |
| 20 | B7 sample cap | L3 | corpus/knowledge/mutation-case-tsukuroi-census.md:96, :137-142 | 9-package stub against the default cap of 8 (fixture delivers 4) | 9-package stub |
| 21 | B2 tracked species | L7 | corpus/knowledge/mutation-case-kumitate-round-gate.md:66, :88-90, :148-149 | a `--tracked` run with a missing reports dir (no fixture runs tracked mode with it) | 1 invocation + tracked fixture |
| 22 | E2 stderr verdict | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:188, :247-248 | a row whose check prints its verdict on stderr only | 1 stub row |
| 23 | S_STRICT | L9 | corpus/knowledge/mutation-case-kumitate-cite-check.md:54, :90 | a tree with exactly one warning run under `--strict` (no hermetic case passes `--strict`) | 1 tree + 1 case |
| 24 | D9 mid-run change | L4 | corpus/knowledge/mutation-case-mado-verify.md:88, :135-139 | a real mid-run change to the config plane, triggered at the run's 2nd `sort` call (the row is asserted only in its PASS direction) | timing harness; largest fixture here |

## Table 3 — survivors excluded from the fixture-absent class (kill is assert-, pin-, check-side or equivalent)

| Survivor | Leg | Note evidence (path:line) | Why no new fixture is required |
|---|---|---|---|
| D2 render truncation | L1 | corpus/knowledge/mutation-case-kimi-census.md:82-92, :223-230 | survival is assert-caused; the >=6-findings region is fixture-unreached but a 6-finding fixture alone does not pin the `+N more` tail (prefix assert). Note keeps D2 out of the unreached-arm class |
| D10 frozen constant | L1 | corpus/knowledge/mutation-case-kimi-census.md:94-100 | assert `frozen=25` on the existing empty-root fixture |
| B10 CLEAN summary | L2 | corpus/knowledge/mutation-case-kagi-census.md:76, :118-124 | assert the summary counts on the existing green one-row fixture |
| B9 roll-line fields | L3 | corpus/knowledge/mutation-case-tsukuroi-census.md:98, :149-155 | assert the four `planes=` fields on an existing non-all-HEALTHY fixture (12 blocked cases exist) |
| D3 unread row status | L4 | corpus/knowledge/mutation-case-mado-verify.md:82, :117-119 | assert the row status and counts on the existing clean fixture |
| D8 sha-pin NOTE | L4 | corpus/knowledge/mutation-case-mado-verify.md:87, :131-133 | assert the `sha_pin` NOTE text on the existing clean fixture |
| C1 UNMATCHED-ITEM | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:120, :186, :243-245 | note's own census classes it (a); recommended repair is an `UNMATCHED-ITEM` assert |
| F2 `--only` broken line | L5 | corpus/knowledge/mutation-case-kagi-checklist.md:127, :189, :245-246 | note's own census classes it (a); recommended repair asserts the `failed=` cell on a broken row. mutation-score-semantics.md:64 lists it NoCoverage, a taxonomy tension recorded below |
| C1059 floor edge | L7 | corpus/knowledge/mutation-case-kumitate-round-gate.md:64, :110, :151 | recommended repair is a point pin of the floor constant; a 1040-byte thin-report fixture is the alternative the probe used |
| A2 fail-closed tail | L7 | corpus/knowledge/mutation-case-kumitate-round-gate.md:65, :107, :149-150 | detail-tail assert on one existing fail-closed fixture |
| CKIND enum meta-check | L7 | corpus/knowledge/mutation-case-kumitate-round-gate.md:67, :92-96, :151 | `observed ⊆ enum` check; equivalent for gate behaviour, weakens only the suite net |
| S_KIND | L8 | corpus/knowledge/mutation-case-kumitate-sources-check.md:95, :129-134, :159, :236-239 | declaration-only gap; corpus output byte-identical, distinguishable only on `--help` output. Killing check uses the existing RECHECK_OVERDUE fixture |
| S_VERDICT | L8 | corpus/knowledge/mutation-case-kumitate-sources-check.md:97, :135-136, :160 | assert the DRIFT line on the existing drift fixture (routing check calls `runCase('drift-verdict-line')`) |
| S_DUP_LINE | L8 | corpus/knowledge/mutation-case-kumitate-sources-check.md:101, :137-138, :161 | the existing ID_DUPLICATE case asserts kind and exit; add the reported-line assert (routing built a fresh fixture, so fixture-free repair is plausible but unproven) |
| S_ENTRY_COUNT | L8 | corpus/knowledge/mutation-case-kumitate-sources-check.md:102, :139-141, :162 | assert `entries_with_source=1` on the existing `clean` fixture (routing check does exactly this) |
| S_EMPTY_GUARD | L9 | corpus/knowledge/mutation-case-kumitate-cite-check.md:55, :93 | equivalent: the dropped guard is redundant code, 316/316 differential runs identical; no fixture can kill it |

## Notes, inference and unknowns

- Classification basis (O): the ledgers' own vocabulary — fleet-kill-rate-ledger.md:143-150 and operator-runbook.md:157-163 put repaired-by-a-new-case survivors in class (b) unreached fixture/arm: kagi B5, tsukuroi B7/B10, mado D7/R1, claims D9. Table 2 uses the operative test "the killing input does not exist in the suite", which adds the no-case classes (d)/(NoCoverage) and the notes' own fixture-unreached admissions for checklist six, claims D7/D8/C1059-style boundaries.
- Taxonomy tension (O, not resolved here): mutation-case-kagi-checklist.md:218-222 classes F2 as (a) while mutation-score-semantics.md:64 lists it as a NoCoverage candidate; mutation-case-kumitate-claims.md:173-175 groups D7/D8 as reported-but-unasserted while :139 says all three survivors need inputs the fixtures never build. Table 2/3 follow each case note's own repair description over the cross-note labels.
- mado D9 is recorded as class (c) one-directional assert (operator-runbook.md:162-163) but the note states it is "a branch no fixture constructs" (mutation-case-mado-verify.md:135-139), so it appears in Table 2 at the largest size.
- Cite-check S_USAGE: the note gives the usage-exit gap (cite-check.md:91) but does not state whether any hermetic case invokes the usage path; if one does, an exit pin suffices and the row moves to Table 3.
- U: expected fixture sizes are estimates from the notes' probe descriptions, not measured; no ddmin was run. Whether the suite's existing fixtures can be edited in place (rather than adding cases) is not stated in the notes and is not checked here. C2 (B5) is the only fixture this lane knows to be under construction in this wave.
- U: this census does not check whether any of these survivors has since moved (owner hardening) at the leg pins; each row is authority-scoped to the pinned blob in Table 1.
