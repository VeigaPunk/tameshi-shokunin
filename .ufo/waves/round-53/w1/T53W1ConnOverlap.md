# T53W1ConnOverlap — sibling surface scan

## Scope and method

Read-only scan of fleet reports for rounds 52–57 that are present, latest sibling reports available at scan time, each lane's `SCORECARD.md` for relevant planned/current rows, `shokuknow/merge/` package names, and lane `SOURCES.md` rows. Checked cross-lane URL sharing with:

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin
```

The tameshi round-53 report was being written during this scan; its current draft identifies C1 (30 cold-read SKILL sections) and C2 (TMPDIR-aware tools), and the S275/S276 adoption. The deciding script was inspected to determine scope, not run.

## Findings

| Lane / evidence | Surface | Overlap with Tameshi R53 and interference |
|---|---|---|
| **kama**, round-52 report `round-52/kama.md:20`; round-53 report `round-53/kama.md:9-10`; SCORECARD current round-54 planned section | Scratch/TMPDIR policy and source-path calibration. Kama R52 says `tools/kama-probe.sh` honors `TMPDIR`; R53 changes its own replay/cited-path tools. | **Related policy, not same implementation.** Distinct lane files and predicates; no interference with the seven tameshi tools or its cold-read monitor. |
| **tsukuroi**, latest available `round-47/tsukuroi.md:5-7,13,30`; SCORECARD `:3065` | Census selftest with spaced `TMPDIR`; implementation falls back to `/tmp`, which its report explicitly says fails the frozen rule. | **Same broad scratch-hygiene policy, different lane tool and predicate.** No direct code conflict. A shared lesson is relevant, but adopting a fallback in tameshi would contradict its own stated rule. |
| **souji**, SCORECARD `:494-525` | Planned calibration/operability work includes cache tool TMPDIR support, trailing-slash TMPDIR cases, and two literal `/var/tmp` scripts. | **Potentially adjacent planned policy work**, not a same-file edit. No current report in rounds 52–57 identifies a direct touch of tameshi tools. |
| **mori**, SCORECARD `:2526-2528` and `:2701-2703`; latest report `round-55/mori.md` | Planned census arm pins the shared `scripts/sources-census.sh`; earlier planned scratch-residue producers. | **Shared substrate, but no demonstrated interference in this round.** Tameshi's `deciding-run.sh:42-43` invokes `sources-census.sh validate --root "$FLEET" tameshi`, explicitly lane-scoped; sibling registry errors/rows do not determine that result. A future mutation to the shared census script could affect it if tameshi's frozen-script guard does not pin/reject that change; inspect the actual frozen-file set before deciding. Mori's planned pin is not itself evidence of such a change. |
| **kotodama**, latest report `round-55/kotodama.md:19,77-78`; `kotodama-shokunin/corpus/SOURCES.md:304-305` | Its independent numeric S275/S276 rows concern Malagan and Malanggan, not Tameshi's mutation-testing papers. | **ID collision only, no URL/document collision.** Registries are lane-local; kotodama's S275 is a museum source and its S276 a monograph. It does not interfere with Tameshi's S275/S276 rows. |
| **chousa**, round-53 report `round-53/chousa.md:10,13,44`; latest `round-57/chousa.md:16` | Round-53 package assimilation and registry work; later report discusses correcting a misrooted fetch output. | **No same package or claimed tool surface.** It does not consume `merge/tameshi` or its S275/S276 sources. |
| **kumitate**, round-53 report `round-53/kumitate.md:18,41-47,114-132` | Same two standards (RFC 8785 and sha256sum) used as S104/S105 for its receipt-identity entry; adopts `merge/tameshi`? No: its report says this is its own entry and no assimilation overlap. | **Topical adjacency only.** No Tameshi source/document overlap, no shared tool/counter. Its report records no assimilation package adoption. |
| **kake**, round-55/56/57 reports | Repeated `merge/kake/` adoption and URL/source-ID collision handling; several unrelated shared mutation-testing URLs appear in the shared census (`pitest.org`, mutation report schema, Stryker docs). | **No same package or Tameshi S275/S276 URL.** General mutation-testing domain and common references are not the same resource: Tameshi's S275 DOI and S276 arXiv URL did not appear in another lane registry. |
| **mado**, latest report `round-51/mado.md`; SCORECARD records several historical tool scratch predicates | Prior `/tmp` refusal and TMPDIR scratch counters, but no current round-52–57 report. | **Historical pattern only; different tools and no current conflict.** |
| **tabi**, latest report `round-36/tabi.md` | Its adjacency surface reads sibling knowledge; round-36 report's census is scoped to `tabi`. | **No evidence it edits Tameshi SKILL/tools.** Tameshi's cold-read predicate is explicitly tied to Tameshi's own re-keyed ledger and reader artifacts. |

### Exact source overlap check

Tameshi S275 is DOI `10.1145/3540250.3558911`; S276 is `https://arxiv.org/abs/2212.11762`. Both appear in `merge/tameshi/SOURCES.append.md` as staged S161/S162 and in the Tameshi registry after renumbering. Searching all sibling lane registries found neither paper URL outside `tameshi-shokunin`. The fleet `shared` census does show many common URLs across lanes, including generic Python, Git, Pitest, and Stryker references; none of those is either new Tameshi paper URL. `shared` reports URL sharing, not interference by itself.

## Synthesis / bounded proposal

For this round, classify overlap by **same bytes/resource or shared executable substrate**, not by topical vocabulary or lane-local numeric source IDs. This avoids falsely conflating kotodama S275 with Tameshi S275, and distinguishes the several independent TMPDIR implementations from an edit conflict. Keep the one real second-order check explicit: because the deciding run calls the fleet census executable, verify its frozen-file/pin guard, even though the invocation is lane-scoped. The round-53 contract says the frozen file set must be byte-identical, but this scan did not inspect whether that set includes the shared fleet script; no claim is made that the guard does or does not include it.

## Axes and risk

- **Operability:** sibling scratch work may provide precedent, but no sibling report shows a current modification to Tameshi's tools. Mori's planned shared census pin is a possible future shared-substrate dependency, not present interference.
- **Calibration:** no sibling report found that measures or edits Tameshi's cold-read ledger/reader artifacts. Kama's calibration claim concerns cited repository paths, not cold-read.
- **Coverage/assimilation:** other lanes adopt their own `merge/<lane>/` packages. Chousa, kumitate, kake, and kotodama show no consumption of `merge/tameshi`; numeric S275/S276 labels are lane-local.
- **Risk:** shared scripts and fleet-level policy can create indirect effects even where source files are lane-local. The report evidence establishes a lane-scoped census call, but does not establish that the deciding run pins the external census script bytes.

## Verification performed

- Inspected reports in fleet `.ufo/reports/round-52` through `round-57` where present, including all eight available round-53 lane reports and `tameshi.md` as it appeared during the scan; also checked latest available reports for all sibling lanes.
- Inspected relevant SCORECARD planned/current lines for all sibling lane repositories; targeted searches found the scratch/TMPDIR/cold-read/S275/S276/package candidates listed above.
- `sources-census.sh shared --root /home/vgpnk/Projects/shokunin` returned shared-resource rows with exit 0. The Tameshi S275/S276 resource URLs were not in any other lane registry.
- Read `tameshi-shokunin/.ufo/evidence/round-53/deciding-run.sh:42-43`; command validates only lane `tameshi`.
- No files outside this report were modified; no tools installed.
