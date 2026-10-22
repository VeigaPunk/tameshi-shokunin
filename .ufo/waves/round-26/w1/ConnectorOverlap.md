# ConnectorOverlap — round 26 wave 1 (adjacency)

Seat: TameshiR26.ConnectorOverlap (connector, leaf). Date: 2026-10-22.
Read-only throughout: no git write, no jj command, no gate or selftest run, nothing written except this file. No tool installed or updated.

## Verdict

**No contested scope.** kumitate owns `scripts/cite-check.mjs`, its contract and its own per-repair mutation controls; tameshi owns the cross-gate ledger leg `js-cite-check` as a read-only primary-surface probe. No other lane measures the gate by mutation.

There is one **record contradiction**, and it belongs to tameshi, not to a sibling. The frozen contract calls the gate "never-measured". tameshi's own ledger and census record a PREP-T6 probe of 1/4 at the **same blob** (`40573448…`). The kumitate log also records four owner mutation controls on the gate. No wave-1 draft item supersedes the stale ledger cells.

## Evidence

### 1. kumitate owns the gate and records its own mutation work (read-only, `GIT_OPTIONAL_LOCKS=0`)
- Pin identity: `git -C kumitate-shokunin show 1205c66…:scripts/cite-check.mjs | sha256sum` gives `40573448…0c9f`, 2537 lines. kumitate HEAD `dfa159d` has the same sha. `git log 1205c66..HEAD -- scripts/cite-check.mjs` is empty, so the gate has not moved since the pin.
- Ownership: kumitate `PROVINCE.md:15`, "The lane's own instruments `scripts/*.mjs` (registry: `SKILL.md` §Gate registry)". Registry row: kumitate `SKILL.md:599` (HEAD), `| cite-check | gate | …`.
- Its own "symbol-machinery mutation copy": `scripts/cite-check.mjs:78` (header) and `:2372-2383` (pin). It copies the live self tree, rewrites `gate.rs:15` to `gate.rs:11`, and requires a `SYMBOL_OFF_LINE` hit. It sits in the **integration** group (`checkI`), so the hermetic `--selftest` that the ledger leg runs does not reach it. The leg and the owner control therefore measure different groups, and neither displaces the other.
- Owner mutation controls recorded in kumitate:
  - `LOG.md:1090`: round 23 fence masking, "selftest 20→26/26, mutation-proven"; `corpus/lessons/round-23.md:14`, "3/3 mutation arms".
  - `LOG.md:1123`: round 25 alias gating, "mutation control 32/34 un-gated"; `corpus/lessons/round-25.md:13`.
  - `LOG.md:1135`: round 26 pairing, "mutation control 36/41".
  - `LOG.md:1162`: round 28 quote grammar, "mutation control 55/58".
  - Each control is a reverted-feature check that the owner ran on its own suite at an earlier blob. None is a pre-registered sweep, and none is a ledger row.
- `corpus/QUALITY.md` (HEAD) mentions cite-check only as gate-clean Q6 (`:35`, `:97`). It has no mutation criterion for the gate. The working tree has uncommitted `corpus/QUALITY.md` and `corpus/SOURCES.md` edits (kumitate's own round). Their diff contains no cite-check, mutation or tameshi line.
- `git grep -i tameshi HEAD -- ':!.ufo'` in kumitate finds one hit, `corpus/lessons/round-37.md:17` (a misroot sweep), and no claim on the leg.

### 2. Other lanes: none measures it
I scanned every `*-shokunin` lane except kumitate and tameshi with `rg --hidden --no-ignore cite-check`, excluding `.git`, `interactive-sessions`, sandboxes, scratch directories and jsonl files. Every hit is a citation, a precedent or advice:
- kagi: `corpus/lessons/round-11.md:182` (names the gate as a re-verifier).
- kotoba: `.ufo/round-22/scouts/A5.md:55`, "No mutation probe on kumitate was performed"; `corpus/knowledge/sibling-citation-routing-round21.md:53`.
- kama: `.ufo/waves/round-17/build/advice/ConnectTameshi.md:27`, "tameshi already measures three gate-attacking controls: "cite-check's mutation copy"…". This credits tameshi's method layer, citing tameshi `SKILL.md:110-113`. Also `round-19/build/advice/KumitateOverlap.md:41`, advising against importing the gate's pin code.
- kengaku `corpus/evidence/round11-fleet/r11-connector.md:23`, mado `.ufo/waves/round-20/w1/reports/ConnSiblingClassifiers.md:22` and chousa `.ufo/evidence/round-1/wave-plan.json:545`: citations only.
- Filtering the same scan for `mutat|mutant|sweep|kill` adds only the kotoba A5 "no mutation probe" line and the kama advice line.
- Full fleet scan (all lanes plus the fleet-root `.ufo`, 938 s): it adds mori, souji and tabi, again with no measurement.
  - mori: `.ufo/waves/round-20/build/ConnKumitate.md:17` (inventory) and `round-23/build/ConnSoujiKama.md:68` (an `ENOSPC` false positive at `cite-check.mjs:2247`).
  - souji: `.ufo/waves/round-16/w2/ConnSiblingOverlap2.md:142,272` (registry-row grep).
  - tabi: `.ufo/waves/round-17/w1/ConnSiblingJj.md:98` (git call sites `:1678,1866`).
  - Fleet root: `.ufo/reports/AGGREGATE.md:929` counts the gate as a kessho "builder instance", absorbed in-province, which is a pattern credit rather than a measurement. `:1212` (D-109, OPEN) is an `--integrations` attribution defect in kumitate `SKILL.md:552-553`. The fleet-root hits matching `mutat|sweep|kill` are kumitate's own round reports (`reports/round-16/kumitate.md:234`) and aggregator sweeps that quote them.

### 3. tameshi PROVINCE
- Lines 7-11 cover the leg: "**Owns:** … `kumitate-shokunin/scripts/*` (six gates with selftest suites + mutation controls)". Lines 15-18 cover the bound: tameshi "Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)". The sweep ran on a scratch copy (`sweep.txt:3`, `MUTATE_TARGET: /fast/scratch/hyaku/tameshi-r26/cite-check.mjs sha256=40573448…`), so it stays inside that bound.
- Lines 27-40 (Core) name only the six round-1 legs. The seventh and eighth legs entered by append (`:49-83`, the round-16 and round-18 blocks, "probed read-only as a kumitate `scripts/*` primary surface"). At integration `a08e85c`, PROVINCE has **no round-26 append** (105 lines; `grep -i 'nine|cite-check|round 26'` only matches `:89`, "nine-file population"). The round-25 append `:101-102` still says "emits the eight recorded ledger legs". `DraftProvinceReadme` (`make-spec-w1.py:89-92`) drafts the missing append, so this is pending work, not contested scope.

### 4. kotoba frontmatter check: not triggered
`git diff d414079 a08e85c -- SKILL.md` has one hunk, `@@ -2084,0 +2085,17 @@`, which appends at end of file and leaves the frontmatter unchanged. The only frontmatter item in the wave is `DraftEntry` (`make-spec-w1.py:53-58`). It targets the knowledge entry `corpus/knowledge/mutation-case-kumitate-cite-check.md`, not `SKILL.md`. Per the item's own condition, I did not read `kotoba-shokunin/corpus/knowledge/frontmatter-rule-authorities-round48.md`.

### 5. The contradiction: "never-measured" against tameshi's own record
- `.ufo/evidence/round-26/contract.json:11`: "ninth recorded mutation case on a never-measured kumitate gate (scripts/cite-check.mjs)".
- `corpus/knowledge/fleet-kill-rate-ledger.md:94` (at `a08e85c`, blame `9f1d3c3` 2026-10-14): "kumitate `scripts/cite-check.mjs` (pin `40573448…`, 2,537 L) | PREP-T6 **probe**: 4 defects — **1 killed** (K3 …; suite 61/62), 3 survivors".
- Same file, `:107`: "| cite-check | 62 | `40573448330f52fb` | **probe only, 1/4** (§2); full sweep open". Also `:224` (U4): "the cite-check probe (1/4) is an indication, not a rate".
- `corpus/knowledge/fleet-suite-census.md:611` (same probe, "a full sweep is not recorded at this write").
- `corpus/knowledge/gates-survey-kumitate.md:51` and `SKILL.md:110-113`: tameshi had already recorded kumitate's mutation copy as a measured mutation control.
- The ledger's "(retained)" probe scratch is gone: `ls /tmp/w5-prept6-cite/work/` gives "No such file or directory". The probe now rests on the ledger and census text only.
- Coverage of the probe against round 26: the probe's survivors were aggregate CLI verdict collapse, n/n summary counts and CLI exit fail-open. All three are suite-runner or CLI accounting. The round-26 spec (`cite-check.defects.spec`) re-targets none of them. The closest is `S_USAGE` (usage exit 64→65), a different arm. The two survivor sets are disjoint, so the combined record has 3 + 5 named survivor shapes.
- Precedent for superseding a cell: ledger `:280` ("§3 supersession (cells, not edits)"), `:403-417` (round 16, seventh row) and `:424-437` (round 18, eighth row). At `a08e85c` the ledger ends at `:437` with **no ninth row**. `grep -n 'ledger|PREP-T6|probe only' make-spec-w1.py` shows that no wave-1 item drafts one.

## Proposed move (one, bounded)

The L1 makes two text-only additions:

1. **Ledger:** append "## Round 26 — ninth row appended (2026-10-22)" to `corpus/knowledge/fleet-kill-rate-ledger.md`, in the round-16 and round-18 shape. Put the `js-cite-check` row there: hermetic `--selftest`, 62 cases, `env -i` guard; **5/10**, 5 kill-aimed and 5 hole-aimed, 10/10 predictions held; sweep 2026-10-22T10:02:07Z at runner `d22c4025…` (`sweep.txt:1-2`); landed runner `fb91ef76…`; rev `1205c66`, sha256 `40573448…0c9f`. Add one supersession sentence: §2 `:94` and §3 `:107` ("probe only, full sweep open"), U4 `:224`, and census `fleet-suite-census.md:611` are superseded by this row. The PREP-T6 probe's three CLI-accounting survivors stay unmeasured by the sweep, and its scratch receipt is no longer on disk.
2. **Novelty wording:** in the entry, the lesson and the SKILL section, replace any "never-measured" phrasing with "first pre-registered full sweep. A prior PREP-T6 probe recorded 1/4 at the same blob, and the owner records reverted-feature mutation controls (kumitate `LOG.md:1090,1123,1135,1162`)". The frozen contract stays as written. The lesson can record the contract wording as a corrected claim.

**Axes:**
- calibration improves: four stale record cells meet the repo bytes, and one overclaim is corrected.
- depth is unchanged: `c1-measure.py:32` reads only `tools/mutate-and-run.sh`, so the ledger and prose cannot move C1.
- C2 is untouched: `c2-measure.py:37-90` reads only `tools/registry.json`, `SKILL.md`, `SCORECARD.md`, `corpus/lessons/round-25.md` and `corpus/knowledge/mte-report-interop.md`.
- adjacency improves: kumitate's owner controls get credit by citation, not by absorption.

**Second-order effects:**
- Verification: `tools/mte-interop.py` and `--regression` do not read the ledger prose.
- Substrate: `sources-census.sh` validates `SOURCES.md` rows, not ledger text [INFERENCE: I did not open the census script].
- Contract: the frozen claim is not edited. Its "never-measured" stays on record, contradicted in the lesson rather than smoothed over.

**Risks:**
- Shrinking the "learning" headline. The 9th recorded case still holds, because the probe was never a ledger row.
- Line anchors `:94`, `:107` and `:224` drift if any other append lands first. Cite them at `a08e85c`.
- The probe's scratch is unrecoverable. The supersession must not restate its numbers as re-verified.

**Verification:**
- `GIT_OPTIONAL_LOCKS=0 git -C tameshi-shokunin show <REV>:corpus/knowledge/fleet-kill-rate-ledger.md | grep -n 'Round 26 — ninth row'` gives 1 hit.
- `grep -rn 'never-measured' corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/lessons/round-26.md` at `<REV>` gives 0 hits.
- `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE` still prints `recorded_cases=9 wired_legs=9 depth_score=9`, unchanged by the edit.
