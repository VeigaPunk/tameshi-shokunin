# T55W1RevColdread — attack the re-key plan

**Seat**: T55W1RevColdread (reviewer, axis: calibration; milestone: attack the re-key plan)
**Verdict**: The plan's factual claim about *the SKILL.md edit in isolation* is true — exactly one
section's bytes change (`## Standing rules`) — but the round's re-key obligation is **18 headings,
not 1**. The same round edits `tools/registry.json`, `tools/repeat-control.py`,
`tools/context-capture.py`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `SCORECARD.md` and `LOG.md`,
and cold-read credit is input-keyed: the crediting ledger entry for a section fails the moment any
file it records changes, even when the section's own bytes are untouched. Measured on a fixture at
base `0a2010ac` with the round's content patches + record edits applied:

| state | credited | precheck |
|---|---|---|
| base `0a2010ac` | **64/64** | — |
| edited, **no** re-key (`2ff57a1f`) | **46/64** | `lost=18 RED`, rc=1 |
| edited + 18 reader entries bound (`c94ad673`) | **64/64** | `lost=0 ok`, rc=0 |

A one-section re-key therefore leaves 17 sections lost and makes the deciding run's
`coldread-precheck` exit 1 (`deciding-run.sh:70-71` turns that into `rc=1`), and the no-harm
`coldread-floor` arm requires `credited>=64` (`no-harm.sh:17`). Both receipts:
`T55W1RevColdread-receipts/precheck-no-rekey.stdout`,
`T55W1RevColdread-receipts/precheck-rekeyed.stdout`.

Related receipts (beside this file): `section-table.txt`, `section-diff.txt`,
`lost-headings-at-c0.json`, `attribution.txt`, `crediting-entry-sha.txt`,
`pin-sim-uncovered.json`, `rekeyed-summary.json`, `binder-rekey2.stdout`, `commands.sh`,
`reader-report-example.json`.

---

## 1. What the round-18 `sectionize` says (exact boundaries)

Frozen sectionizer: `.ufo/evidence/round-18/measure.py:209-253` (`^#{1,3}(\s|$)` outside ``` fences;
step 2 is only `sha256` over the section's bytes). At `0a2010acd1e92e4e332774050825e21bcfc7e079`:

```
round-18 sectionize(SKILL.md at 0a2010ac…): sections=64
idx start end   sha256(12)  heading
 1     1    5 a2fe1bb731a1 
 2     6   16 03abd331d1ff # tameshi-shokunin
 3    17   40 61736dcebc2d ## Standing rules          <-- the edited section
 4    41   68 293fd76b1cb9 ## Source notes
 …
64  2158 2197 cc23587b353f ### Round-26 gate/probe registry — report interop
```

(`section-table.txt` holds all 64 rows.)

The scribe's edit (both drafts I read) keeps the section count at 64 and changes exactly one sha:

| draft | sections | `## Standing rules` | sha256 |
|---|---|---|---|
| base | 64 | 17–40 | `61736dcebc2d…` |
| `T55W1ScribeSkill-receipts/skill-section.patch` | 64 | 17–44 | `aca61890…` (its own `section-drift.txt`) |
| `T55W1ExecC2Full-receipts/patches.diff` (my fixture) | 64 | 17–46 | `be6aba7fe88d…` |

`section-diff.txt`: `sha-changed: ['## Standing rules']`, `added: [] removed: []`, and every section
after it shifts start by **+6** (the C2Full wording). The credit algorithm matches sections **by
sha only** (`measure.py:612` `matches = by_sha.get(sec['sha256'], [])`), so the start/end shift costs
no credit. The one place it does matter is `assemble.py`, which validates a reader report's `start`
against the page at `read_rev`; a fresh reader must therefore quote the **C0** start (e.g.
`### Triggers T1–T3` is 1083 at base, 1089 at C0), not the base start. The binder itself ignores a
reader's `start` (`binder-r55.py:146` checks only `cand` and `section_sha256`).

**The edit's own input surface does not grow.** Path-like tokens in the old vs new `## Standing
rules` text are identical (`PROVINCE.md`, `corpus/knowledge/scratch-root-contract.md`, `/tmp`,
`/fast/scratch/hyaku`, `<lane>-r<round>/<sub>/`); `env-diff --contract` is a tool name, not a path.
So the edit cannot enlarge the section's ledger input set; it only invalidates the section's sha.
`corpus/knowledge/scratch-root-contract.md` and `corpus/lessons/round-54.md` appear in **zero**
ledger entries' inputs, so items 1–3 of the round (tools, registry cells, note) and the in-place
lesson fixes cannot drift anything — *except* through the two tool files and `registry.json`.

## 2. The finding (blocking): the re-key obligation is 18 headings

A section credits iff ≥1 entry with its sha passes every gate and no non-stale failing entry vetoes
(`measure.py:602-647`; the inputs gate is `input_failures`, `measure.py:330`, applied at the
measured rev `REV`). At the fixture's C0/PIN the following **18** headings lose credit
(`pin-sim-uncovered.json`; causal file per heading from `attribution.txt`, computed over the
entries that actually credit at base, not the union the precheck prints):

| # | heading (exact) | base start | C0 start | why it is lost |
|---|---|---|---|---|
| 1 | `## Standing rules` | 17 | 17 | **sha changed** (the one text drift) |
| 2 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 142 | 148 | registry.json, repeat-control.py, context-capture.py, SOURCES, QUALITY |
| 3 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 932 | 938 | corpus/SOURCES.md |
| 4 | `### Triggers T1–T3 and the re-pin rule` | 1083 | 1089 | registry.json, both tools, SOURCES, QUALITY |
| 5 | `### The service's limits — what tameshi refuses to mutation-test` | 1265 | 1271 | registry.json, both tools |
| 6 | `## The operator's runbook and the six-leg regression (round 10, measured)` | 1295 | 1301 | tools/registry.json |
| 7 | `## Repeated controls and gate registry — round 12` | 1504 | 1510 | tools/repeat-control.py, SOURCES |
| 8 | `### Gate/probe registry` | 1524 | 1530 | tools/repeat-control.py |
| 9 | `## Pin disposition and provenance correction — round 13` | 1542 | 1548 | corpus/SOURCES.md |
| 10 | `### Round-13 gate/probe registry` | 1573 | 1579 | corpus/SOURCES.md |
| 11 | `## Effective expectation reconciliation — round 14` | 1589 | 1595 | context-capture.py, SOURCES |
| 12 | `## Context gate classification and explicit exit classes — round 15` | 1635 | 1641 | registry.json, context-capture.py, SOURCES |
| 13 | `### Round-15 gate/probe registry` | 1702 | 1708 | tools/context-capture.py |
| 14 | `## Live-tree re-pin and entry-command monitor — round 17` | 1840 | 1846 | registry.json, both tools, SOURCES, QUALITY |
| 15 | `### Round-17 gate/probe registry — re-pin and monitor` | 1872 | 1878 | registry.json, both tools, SOURCES |
| 16 | `### Round-18 gate/probe registry — routed-defect closure` | 1951 | 1957 | registry.json, SOURCES, QUALITY |
| 17 | `### Round-21 gate/probe registry — finite environment differential` | 1990 | 1996 | registry.json, SOURCES, QUALITY |
| 18 | `### Round-26 gate/probe registry — report interop` | 2158 | 2164 | registry.json, both tools |

`sha256`/`end` for each at C0 is in `lost-headings-at-c0.json`; those values are wording-specific
(my fixture used the C2Full SKILL wording), so the L1 must recompute `sectionize` at its own C0.
The **heading strings and the 17 non-text causes** are wording-independent.

Causal proof, not a union: for each of these, the entry (or entries) that credit at base is the one
whose recorded sha for a changed file no longer matches. E.g. (`crediting-entry-sha.txt`):

```
## Pin disposition and provenance correction — round 13   (sha 1fa3130bc6d4…)
   CREDITING entry rev=99c3bc88  corpus/SOURCES.md recorded=4a466c10d6bb base=4a466c10d6bb c0=c67412c44a23 match_at_base=True
### Gate/probe registry  (sha 99285e24a71a…)
   CREDITING entry rev=651773ab  tools/repeat-control.py recorded=3f82aa5a97c4 base=3f82aa5a97c4 c0=7d3a414f9e54 match_at_base=True
### Round-15 gate/probe registry (sha 78edbb693cdd…)
   CREDITING entry rev=99c3bc88  tools/context-capture.py recorded=be539b4cd1ce base=be539b4cd1ce c0=e6d0a06cf7a2 match_at_base=True
```

Two sections lose credit on `corpus/SOURCES.md` alone (#3, #9, #10) and one on
`tools/registry.json` alone (#6): those are the cheap ones the plan drops silently. The precheck's
`drifted=` list is the union of every non-crediting entry's failures and therefore over-reports
(e.g. it names `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`,
`.ufo/evidence/round-15/verify.py`, `corpus/knowledge/service-limits.md`, which this round does not
edit); use `attribution.txt` for the causal set.

**Why the round's own re-key measurements say “one”, and why they are wrong.** Two seats measured
only the SKILL edit: `T55W1ExecRekeyPrep-receipts/cand.json` (cand `64e76a7`, `covered=63/64`,
`lost_headings=['## Standing rules']`) and `T55W1ExecReKeyDryBind-receipts/commits.txt` (`64/64`
after one bind). Neither clone carried the registry/tool/record edits, so the input drift never
appeared. The precheck is only meaningful at the **full content+record commit** (or a PIN that
contains them).

## 3. Fresh reader bound at the content commit **does** restore credit — verified end to end

Using the adapted binder `T55W1ExecReKeyDryBind-receipts/binder-r55.py` (a copy of the frozen
round-54 driver with `--headings/--waves/--resolutions/--label`; the round-54 driver is frozen and
cannot be run as-is for round 55):

1. 18 reader reports `{heading, cand:<C0>, section_sha256:<C0 section sha>, findings:[]}` + a
   companion `.md` (shape: `reader-report-example.json`).
2. `binder-r55.py <clone> <C0> <PIN> <clone>/.ufo/evidence/round-21/coldread/rekey-r55-<c0short>
   --headings <list> --waves <readers> --label "L1 TameshiR55 re-key (round 55)"` →
   `REFRESH rekeyed=18 skipped=0 headings=18` (`binder-rekey2.stdout`).
3. Measure at the re-keyed commit: **64/64**, `calibration_restraint_score 8`,
   `## Standing rules` `{start:17,end:46,credited:true,reason:credited,vetoed:false}`
   (`rekeyed-summary.json`).
4. Real precheck floor=base cand=re-keyed: `COLDREAD_PRECHECK floor=0a2010acd1e9
   floor_credited=64 cand=c94ad673 cand_credited=64 lost=0 ok`, rc=0 (`precheck-rekeyed.stdout`).

The rules that make this work (all in `.ufo/evidence/round-21/coldread/measure.py` →
`.ufo/evidence/round-18/measure.py`): section matched by sha (`:612`); entry gates — verdict,
class, commands>0, inputs (`:330`), strict trace (`:373`); coverage `credited>0 and not vetoes`
(`:638`). Stale entries (`entry_is_stale`, `:528`) do **not** veto, which is why sections with an
old drifting entry only fail when *every* entry with the current sha drifts — exactly the 17 above.

Operational details the plan must carry:
- **A reader without a companion `.md` is skipped.** First run: `reader-md-missing` ×18,
  `REFRESH rekeyed=0 skipped=18`. The binder never says the `.md` is mandatory in its usage line.
- **`cand` must equal the resolved C0** (`binder-r55.py:146`); round-54 reader JSONs carry a
  different `cand` and are invisible/skipped. Fresh readers are required for all 18 headings; the
  dispatch has **no reader seats for the other 17** (75 items; only the dry-bind seat writes a
  reader, for `## Standing rules`).
- **`--resolutions` defaults to the round-54 file** (`binder-r55.py:82-84`,
  `.ufo/evidence/round-54/integrate/resolutions.json` exists and grants allowances for 8 of the 18
  headings — n=1 for most, n=2 for two, n=11 for `### Round-21 gate/probe registry` — all
  `"routed": "round 55"`). If the L1 leaves the flag off, round-54's allowances are
  silently inherited. Pass an explicit round-55 resolutions file (empty list if the fresh readers
  are clean) so the allowance is a decision, not a leftover.
- **The binder must be landed at a round-55 path** (e.g. `.ufo/evidence/round-55/integrate/binder.py`);
  the round-54 file is frozen and has no flags, so the adapted copy currently living under
  `.ufo/waves/round-55/w1/...-receipts/` is not a stable home for the deciding evidence.
- `OUTDIR` must be **inside the lane** (trace paths are `relpath(OUT, LANE)`); outside the repo the
  entries' traces fail to resolve.

## 4. DROP list: substance right, citation incomplete, and one ordering constraint

Actual binder constant (`binder-r55.py:55`):
`DROP = ('LOG.md', 'SCORECARD.md', 'SKILL.md', '.ufo/evidence/round-21/coldread/ledger.json')`.
The plan cites three; the fourth is required. Assessment:

- `LOG.md`, `SCORECARD.md` — **right and necessary**. This round writes both (items 5–6) and the
  measure does **not** ignore them (`IGNORED_INPUTS`, `measure.py:135-136`, holds only `SKILL.md`
  and the two round-17/18 ledgers; the round-21 wrapper adds the round-21 ledger). An entry that
  kept them would drift between PIN and the final rev, exactly the round-53 failure mode the
  binder's docstring names.
- `SKILL.md` — right but redundant: the credit rule ignores it (`IGNORED_INPUTS`), so dropping it
  changes nothing; keeping it would be harmless. 36 entries list it and still credit after the edit
  (e.g. `## Source notes`, base entry rev `8eaae28e`).
- `.ufo/evidence/round-21/coldread/ledger.json` — **required**: the binder rewrites that file after
  C0, and the round-21 wrapper adds it to `IGNORED_INPUTS`. Omitting it would make every bound
  entry drift against its own output.
- **Not** dropped, correctly: `corpus/SOURCES.md`, `corpus/QUALITY.md`, `tools/registry.json`,
  `tools/repeat-control.py`, `tools/context-capture.py` (and any other file this round touches).
  They are pinned at `PIN` instead. **Consequence**: `PIN` must be at or after the last commit that
  touches any non-dropped input. If the L1 binds at C0 and then lands the SOURCES rows / QUALITY
  criterion / lesson fixes, the 18 bound entries drift again at the deciding rev. My restoration
  used `PIN = C0` with all record edits already in C0; that is the ordering the real run must
  reproduce (bind last, then commit only the ledger + rekey dir).

## 5. Rejected shortcuts (do not take these)

- **Patching the stale entries' recorded sha values in place.** It would credit without re-reading,
  falsifying `commands_executed`/traces — the rule this ledger exists to enforce. All 17 must get a
  reader at C0, not an edited sha.
- **Dropping `corpus/SOURCES.md` / `corpus/QUALITY.md` from the binder's DROP-adjacent logic** to
  dodge the drift: the 17 headings are not re-keyed at all, so their entries are untouched; and
  dropping evidence files from new entries would discard the inputs those sections actually name.
- **Measuring the precheck at a rev before the record edits**: the deciding run measures at `REV`,
  which must carry items 5–6; C0-only measurement hides `corpus/SOURCES.md` and `corpus/QUALITY.md`
  drift only if those edits land later — and then they bite at `REV`.

## 6. Residual risk and verification gaps

- My C0/PIN is a **simulation**: the real wording of the SKILL edit and of the record edits is the
  L1's; the drift set depends on *which paths change*, not their bytes, so the 18-heading set and
  causes are stable. `start`/`end`/`sha256` in `lost-headings-at-c0.json` must be recomputed at the
  real C0.
- The `## Standing rules` `sha256` I bound (`be6aba7fe88d…`) belongs to the C2Full wording; the
  scribe-draft wording yields a different sha (`aca61890…`) with the same one-section result.
- I did not run the full deciding run (no C1/C2 counters), and I did not re-run readers with real
  content: my reader JSONs are `findings:[]` shells. The binder accepts them by construction; a real
  reader may return findings, which then need adjudication before binding.
- Timing: the round-21 measure took 68 s at base, 38 s at C0 with the base ledger, and **429 s**
  after the re-key at the re-keyed commit (18 new entries, one carrying 2 497 inputs). Budget the
  deciding run accordingly; the precheck runs the measure twice.
- Outside my item, reported not fixed: the committed freeze set `631cd64` has
  `contract.amendments=0`/`freeze.amendments=0`, while the working tree currently holds 5 contract
  amendments and 3 freeze amendments (`python3 -` over the two JSON files). The deciding run takes
  `FREEZE` as an argument and diff-checks the frozen files `FREEZE..REV`
  (`deciding-run.sh:65-68`), so whichever freeze commit is passed must re-derive its manifest and
  match what is committed at `REV`. The freeze.json/contract.json amendment counts must agree before
  that check is meaningful.

## Tooling

No installs or upgrades were needed; no pacman/uv/npx use. All fixtures under
`/fast/scratch/hyaku/tameshi-r55/T55W1RevColdread`; every git mutation ran with
`-C "$S/clone"` after `git rev-parse --show-toplevel` printed that path. The lane was read with
`git show`/`read` only; I edited nothing in the lane except this report and its receipts.
