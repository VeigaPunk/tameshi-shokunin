# T51ConnSibling — sibling-overlap scan (round 51, tameshi, w1)

Seat: connector (sibling-overlap scan). Read-only greps over the fleet lanes
(`/home/vgpnk/Projects/shokunin/*-shokunin`, SKILL.md, corpus/knowledge,
corpus/QUALITY.md); the one non-grep check is a read-only `git cat-file`/`ls-tree`
probe into kagi's repo. No lane bytes were modified; no scratch was created (no
receipt files were generated — every citation below is a committed lane file).
Commands used:
`grep -nE '…' /home/vgpnk/Projects/shokunin/<lane>/SKILL.md /home/vgpnk/Projects/shokunin/<lane>/corpus/knowledge /home/vgpnk/Projects/shokunin/<lane>/corpus/QUALITY.md`;
`git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file -t <rev>`,
`git -C … ls-tree <rev> -- corpus/drift-pins.sh`,
`git -C … cat-file blob <rev>:corpus/drift-pins.sh | sha256sum`.

---

## 1. Axis (a): kagi drift-pins.sh / drift-baseline gates

### 1a. The C2 mutation target is kagi-owned — confirmed by blob identity
The tameshi C2 spec pins rev `e64e81b8eb96f3682b00c1e7a291e84420b280fa` and blob
sha256 `c138d34c…`. Verified read-only in the kagi repo:

- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file -t e64e81b8eb96f3682b00c1e7a291e84420b280fa` → `commit`.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin ls-tree e64e81b8eb96f3682b00c1e7a291e84420b280fa -- corpus/drift-pins.sh` → `100755 blob 8a2903dc977a1ef6ea0430b21d1760392ccc2827 corpus/drift-pins.sh`.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file blob e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh | sha256sum` → `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb` — matches the spec's prefix.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin log --oneline -1 e64e81b8eb96f3682b00c1e7a291e84420b280fa` → `e64e81b round-9: freshness axis-move — drift gate with committed baselines, transcript-gate correction`.

Corroborating kagi record: `kagi-shokunin/.ufo/waves/round-22/build/Entry09.md:42`
documents round-9 v2 of `drift-pins.sh` at sha `c138d34c7f0d…c70feb`, 451 lines,
19088 B — the same round, the same hash.

Kagi's own registry row and gate section:
- `kagi-shokunin/SKILL.md:45` — `| Trust a cited line ref / catch host-file drift | bash corpus/drift-pins.sh … | … exit 0 DRIFT_PINS: CLEAN (files=N symbols=M); 1 DRIFT (…) |`.
- `kagi-shokunin/SKILL.md:177-232` — §Freshness gate — drift pins: baselines committed in `corpus/drift-baseline.tsv` + `corpus/drift-symbols.tsv` (`:185-188`); verdict vocabulary `OK | DRIFT | MISSING | LINK | UNPINNED | EXTRA | DUP | POLICY | EMPTY` and symbols `OK | MOVED | GONE | AMBIG | COUNT | SHAPE` (`:200-204`); `--pin` records, does not repair (`:212-221`); hash policy for 6 private no-hash files (`:222-229`); `--selftest` 13 cases (`:183`, `:45`).

**Conclusion:** kagi is the **owner lane** for the exact tool C2 mutates, its
baselines, and its verdict vocabulary. tameshi may cite kagi's verdict semantics
and kagi's own failure-class records (below) as precedent; it must NOT absorb the
tool bytes, the baseline TSVs, or any kagi host-state claim. Chousa already made
the same sibling appraisal: `chousa-shokunin/.ufo/waves/round-31/build/ConnectorSiblings31.md:32-33` — ``kagi | corpus/drift-pins.sh:9-18,45-77 | … Strongest fleet precedent for live drift detection on cited artifacts``.

### 1b. Other drift/baseline gates (each owned by its lane)
- **kake**: `scripts/freshness-sweep.mjs` — registry row `kake-shokunin/SKILL.md:212` (`| freshness-sweep | gate | node scripts/freshness-sweep.mjs --offline … | 0=clean … 1=failed/drift; 2=could-not-evaluate; 64=usage | … --selftest |`), section `:217-232` §Live-vs-source drift detection, pins in `corpus/knowledge/freshness-pins.json` (`:189-193`). Plus live-vs-source byte-drift tools `webzites grokbot reconcile` / `kimi-surface.mjs sync-check` (`:221-227`).
- **kama**: `tools/kama-probe.sh check` gate — `kama-shokunin/SKILL.md:304-308` (`0 reconciled; 2 failed/drift; 1 could-not-evaluate/probe error`); drift timeline `corpus/knowledge/drift-timeline.md`, `SKILL.md:91-108`.
- **mori**: `tools/mori-census.sh --drift <baseline.json>` — `mori-shokunin/corpus/knowledge/audit-r11.md:121` (baseline `corpus/evidence/baseline-r10-20261015T2231Z.json`; `MORI_DRIFT: none`/`warn_pct`); knowledge `corpus/knowledge/drift-repin-r20.md`, `drift-pin-r10.md`; evidence `corpus/evidence/drift-classification-r20.json`, `drift-r12-…-classification.md`.
- **kaidoku (luna)**: zero-drift pre/post config-pair custody — `kaidoku-shokunin/SKILL.md:544-605` (pre-pair sha256 receipts; `:598-604` "Compare same-round only"; `:605` "Drift disposes the claim, not the config"); battery entry `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`.
- **chousa**: `research-gate --pin / --drift` row — `chousa-shokunin/SKILL.md:87` (`GATE_DRIFT: none / <changed tokens>`, exit 0/1/2).
- **kotodama**: gate-battery baselines under `reports/round-10/drift/` (e.g. `reports/round-10/drift/fix-21.md`, referenced at `kotodama-shokunin/SKILL.md:661`).

Excluded false positive: `audio-shokunin/corpus/live/r77-simpl/drift-envelope.txt` is an audio-signal envelope, not a gate.

---

## 2. Axis (b): "assertion satisfied by the harness environment" class (oracle reads output that contains paths/ids)

Direct sibling precedents — each names the same mechanism C2's kill-aimed misses
rely on: an unanchored `grep -q`/substring check over output that contains the
quarry's id/hash in a scratch path or data field, so the assertion is satisfied by
the environment, not by the verdict.

1. **kagi — `corpus/knowledge/claim-ledger.md:178-181`**: the first membership
   implementation used an *unanchored substring search*; "every score digit (`7`,
   `9`) matched a sha256/line field followed by a TAB, so all 48 real cells looked
   pointed"; fixed by an anchored selftest case `cells-numeric-anchored` (`:181-182`).
   This is the closest documented incident to the C2 mechanism (id inside printed
   scratch path satisfying a grep).
2. **kagi — `corpus/knowledge/checklist-execution.md:161-165`**: "a check that
   greps an unanchored pattern can be satisfied by a comment"; countermeasure H1
   is line-anchored for exactly that reason; "No guard can tell a meaningful
   assertion from a well-formed one."
3. **mori — `corpus/knowledge/verdict-contract-r13.md:133-137,196-197`**: an
   internal check "counts nothing (`grep -qE` matches any line, so a duplicate
   roll survives)"; `:197` "duplicate roll inside the census's own selftest |
   **not closed there** — `grep -qE` over a file matches any line".
4. **mori — `corpus/knowledge/selftest-flake-r9.md:195-197`**: a mutation that
   only renames the id to `WATCHDOG_STALE_X` still passes "because the harness
   asserts unanchored substring regexes — expected semantics, not a gap".
5. **chousa — `corpus/knowledge/claim-record-fields-r33.md:9-12`**: two unanchored
   regexes over the raw claim line read a member named `line`/`sha256`/`id`/
   `source`/`span`/`expect`/`marker` inside a *nested object* as the record's own
   field — an oracle satisfied by token occurrence anywhere in the payload.
6. **chousa — `.ufo/waves/round-22/build/ReviewSafety.md:13`**: `claim-ledger.sh`
   accepts `bash` as a first token and denies selected words/metacharacters but
   "does not constrain the script path or prove what the script reads" — the
   allowlist assertion is satisfied by the harness/token shape, not semantics.
7. **mado — `corpus/knowledge/host-bar-producer-census-r40.md:24`**: a probe that
   is "one read, `if makoctl mode | grep -q 'do-not-disturb'; then`, a substring
   test on the mode name, not an equality test".
8. **kagi QUALITY QM10** (`corpus/QUALITY.md:48`): an absence sweep whose pattern
   matches its own text is not emptiness evidence (mirror: self-match).
9. **kaidoku QUALITY 13** (`corpus/QUALITY.md:22`): occurrence counts must use
   `grep -o … | wc -l`, never `grep -c` — the recorded verify command must itself
   reproduce (a 69-line minified file yields 1, not 45, under `grep -c`).
10. **kake QUALITY** (`corpus/QUALITY.md:101-106,263-264`): a count that repeats
    the instrument's own declared total is not evidence; "turn candidate output
    into its own oracle. Fake/stub-echo tests are not behavioral acceptance
    evidence."
11. **kengaku probes** (`SKILL.md:577,587,594,601`): by design, "prediction
    mismatches are on the summary line, never in the exit code" (probes exit 0
    even when `mismatches=N`) — an explicit instance of harness-pass ≠ oracle-match.
12. **tameshi's own class** — `tameshi-shokunin/corpus/knowledge/oracle-anchored-survivors.md:90-93` (round-27, frontier F8): "before calling a survivor a hole, name its anchor; when the only anchor is the pristine run, say 'differential hole' and route it to the gate owner as unanchored." The C2 kill-aimed misses (K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN) are exactly unanchored-oracle survivors of this class.

Citable for C2: items 1-7 above (sibling records as precedent — they document the
same failure shape and its fix/anchor), plus tameshi's own 12. Not absorbable:
all of these are sibling-internal gate/knowledge artifacts; owners keep them.

---

## 3. Axis (c): gate registry tables conforming to PROTOCOL §Gate standard

PROTOCOL.md:375-421 (Gate standard) requires a registry row per gate/probe with
fields: name, kind gate|probe, entry command, verdict map (code → class), self-test
command + spelling, pinned-value path, write scope, owner; registry home = lane
SKILL.md. Sibling lanes with conforming **8-field markdown registry rows**:

| Lane | Header line | Notes |
|---|---|---|
| kagi | SKILL.md:696, 748 | rows 698-701, 750-754; `| name \| kind \| entry command \| verdict map \| selftest \| pinned values \| write scope \| owner |` |
| kasegi | SKILL.md:979 | rows 981-982 (+1039-1041); type cell uses combined `gate\|probe` |
| kengaku | SKILL.md:562 | rows 564-605; explicitly titled "Gate/probe registry (PROTOCOL §Gate standard)" |
| kake | SKILL.md:210 | rows 212-213; later registries at 481/536/724 |
| kaidoku | SKILL.md:1290, 1408 | round-32/34 instrument registries |
| mori | SKILL.md:543, 737 | round-21/26 registries |
| mado | SKILL.md:2081 | row 2083 |
| tsukuroi | SKILL.md:1707 | rows 1709, 1737; superseding tables for rounds 18-31 |
| souji | SKILL.md:217 | rows 218+ |
| kotodama | SKILL.md:648 | rows 649+ (`| name \| kind \| entry command \| verdict map \| self-test \| pinned values \| write scope \| owner |`) |
| tabi | SKILL.md:2388 | round-21 runnable-artifacts registry |
| chousa | SKILL.md:78 | rows 80-135 |

Variants that are **not** the 8-field schema (do not use as the C3 template):
- kama `SKILL.md:296-308` — 5 columns, owner carried in prose; later round registries say "Same columns as `## Local gate/probe registry`".
- revenger `SKILL.md:277` — `| field | value |` key/value list, not row-per-gate.
- lore `SKILL.md:50-94` — per-gate field blocks (not a table), but follows `../PROTOCOL.md:360-406` and uses `--self-test` spelling.
- tabi `SKILL.md:1557/1612/1655/1753` — 6-column tables merging kind/owner and verdict-map cells.

Conformance declarations in prose: `kumitate-shokunin/SKILL.md:589` ("Registry home per the fleet protocol's §Gate standard (round 34)"), `kotoba-shokunin/SKILL.md:447` ("Registry home under PROTOCOL.md § Gate standard (round 54)").

For C3's own row standard (8 cells, kind, verdict map with 0/1 and usage code,
exactly one backticked self-test command, finding id, pinned paths that exist or
`none`, write scope, owner `tameshi`), the closest precedents to copy the *form*
from are kengaku `:562`, kagi `:696`, tsukuroi `:1707`, mado `:2081` — full
8-field rows with 0/1/2 maps and one backticked selftest command. Rows themselves
are sibling-owned and must not be absorbed or copied into tameshi's registry.

---

## 4. What must not be absorbed (owner lanes)

- **kagi**: `corpus/drift-pins.sh`, `corpus/drift-baseline.tsv`, `corpus/drift-symbols.tsv`, `corpus/inrow-pins.tsv`, `corpus/sources-census.sh`, `corpus/claim-ledger.sh` + knowledge gates. Owner of the C2 target tool.
- **kake**: `scripts/freshness-sweep.mjs`, `scripts/citing_set.py`, `scripts/corpus-contract.mjs`, webzites tools.
- **kama**: `tools/kama-probe.sh`, `tools/test-snapshot.sh`, `registry/endpoint-consumers.tsv`.
- **mori**: `tools/mori-census.sh` + drift baselines.
- **kaidoku**: config-drift custody protocol.
- **chousa**: `tools/research-gate.sh` + all round counters.
- **mado**: `tools/mado-evidence-audit.py` etc.
- **kotodama**: gate battery under `reports/round-10/drift/`, `tools/check-gate-battery.py`.
- **souji / tabi / tsukuroi / kasegi / kengaku / kumitate / kotoba / revenger**: their registry rows and gates.

---

## Summary
1. C2's mutation target is kagi's `corpus/drift-pins.sh` at kagi rev `e64e81b8` (blob sha256 `c138d34c…`, commit "round-9: freshness axis-move"): verified via `git cat-file`/`ls-tree`/`cat-file | sha256sum`; kagi is the owner lane for the tool and its verdict vocabulary.
2. The unanchored-oracle class has direct fleet precedent: kagi `claim-ledger.md:178-181` (digit-in-sha field), `checklist-execution.md:161-165` (grep satisfied by a comment), mori `verdict-contract-r13.md:133-137,197` and `selftest-flake-r9.md:195-197`, chousa `claim-record-fields-r33.md:9-12` and `ReviewSafety.md:13`, mado `host-bar-producer-census-r40.md:24`.
3. tameshi already names this class: `oracle-anchored-survivors.md:90-93` ("route to the gate owner as unanchored") — the C2 kill-aimed misses are its instantiation.
4. Drift/baseline gates also exist in kake, kama, mori, kaidoku, chousa, kotodama — none duplicates kagi's symbol+hash pinning; kagi is sole owner of `drift-pins.sh`.
5. Conforming 8-field gate registries: kagi:696/748, kasegi:979, kengaku:562, kake:210, kaidoku:1290/1408, mori:543/737, mado:2081, tsukuroi:1707, souji:217, kotodama:648, tabi:2388, chousa:78; kama (5-col), revenger (field/value), lore (definition-list) are non-template variants.
6. All cited mechanisms/rows are sibling-owned; tameshi may cite them as precedent only, and must register its own C3 rows with owner `tameshi`.
