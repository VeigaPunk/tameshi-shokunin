# C01 — sibling-lane overlap scan (read-only, connector seat)

Subject: tameshi round 17 claims C1 (input-keyed cold-read credit) and C2 (entry-command
registry/monitor + jj fixes). This is an advisory scan; no sibling file was written, no
sibling gate was executed, no `jj` or git write was run.

## 1. Method

- Read-only greps/reads over seven named lanes plus (separately labelled) `tabi` and the fleet
  `scripts/hyaku/`. All line numbers are the **live working tree** at these tips:
  kumitate `1770305`, kotoba `c61a973`, mado `0ab1ccc`, tsukuroi `6923fe0`, kagi `c2cab35`,
  kake `7c61c8c`, kama `cff9e62`, tabi `1205d26`; tameshi subject `98bea7d`.
- Search keys: `registry|entry command|no-harm`, `sha256|digest|drift|input-keyed`,
  `strace|openat`, `rev-parse --show-toplevel|branch tip|branch-tip|detached`, `jj`,
  `cold.?read|credit`, `tameshi-shokunin`, `mutate-and-run|cf41efaa`.
- Counts quoted below were measured (`awk`/`grep -c` over the table text), not estimated.
- Commands run (all read-only; all exit 0 unless noted):
  - `git --no-optional-locks -C <lane> rev-parse --short HEAD` × 8 → tips above.
  - `grep -rn 'tameshi-shokunin' --include=*.{md,py,sh,mjs} <lane> | grep -v '/\.ufo/' | head -8`
    → hits in **mado** and **tsukuroi**; empty for kumitate, kotoba, kagi, kake, kama.
  - `grep -rn 'mutate-and-run\|cf41efaa' … <lane> | grep -v '/\.ufo/' | head -8` → mado 5
    locations, tsukuroi 3 files; empty elsewhere.
  - `grep -rn 'show-toplevel' --include=*.{py,sh,mjs,js} .` → tameshi `tools/pin-disposition.py:79,255`;
    tabi `scripts/check-measurement-binding.mjs:242`; remaining hits are audio-/game-dev- scratch
    trees and a vendored `node_modules` path — no other named lane has a guard.
  - `grep -rn 'sha256\|blob' tsukuroi-shokunin/tools/check-section-citations.py` → 0 hits;
    `grep -rn 'cf41efaa\|gate-mutation-sweep' mado-shokunin/tools/*` → 0 hits (exit 1): no sibling
    gate enforces the mutate-and-run pins.
  - `awk` row counts: mado gate registry 15 data rows; kagi `checklist.tsv` 16 (9 `runnable`,
    7 `by-hand`); this report's §2 table 39 rows.

## 2. Adjacency table

Legend — relation to tameshi: **R** row-registry/monitor prior art · **E** execute-registered-
commands-and-compare · **I** input-keyed/digest-bound credit · **F** frozen two-evidences ·
**J** jj / branch-tip · **G** repo-identity guard · **C** contested scope · **X** cross-lane consumer.

| Owner | path:line | Relation |
|---|---|---|
| kumitate | `SKILL.md:587` | R — `## Gate registry`, 7 gates, columns *entry command / self-test / pinned values*; prose table, not machine-readable |
| kumitate | `SKILL.md:607-609` | **named gap**: "no gate yet ships the §Gate standard 'two evidences' frozen-snapshot run … and no verdict line names the revision it measured" — precisely what tameshi `--rev` supplies |
| kumitate | `SKILL.md:613` | R — `## Verifiable checklist`, 13 `- [ ]` rows each with `→ exit N + \`MARKER\`` |
| kumitate | `scripts/surface-probe.mjs:182` | R — frozen checklist grammar `CHECKLIST_RE` |
| kumitate | `scripts/surface-probe.mjs:857` | E — `SKIP(self)` recursion guard for a row that invokes the runner itself |
| kumitate | `scripts/surface-probe.mjs:858` | E — rows executed via `spawnSync('bash', ['-c', cmd])` (shell string, unlike tameshi's argv arrays) |
| kumitate | `corpus/knowledge/executable-scorecard.md:59` | R — "a prose bullet is not credited"; only items `--checklists` executes count |
| mado | `SKILL.md:541` | R — `## Gate registry`, 15 rows (measured), full fleet-standard columns |
| mado | `SKILL.md:551` | **X C** — `mado-regression` entry command is literally `MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh bash tools/mado-verify.sh --regression` |
| mado | `SKILL.md:563` | I — `mado-label-check`: doc/receipt bytes read `via git show`, optional `measured_commit` |
| mado | `SKILL.md:589-591`; `tools/mado-verify.sh:1863-1868` | X — "mutable sibling harness digest is printed as provenance, **not an enforced harness pin**"; code prints `REGRESSION_HARNESS: … sha256=… (recorded revision … — provenance, not gated)` and the recorded `HARNESS_SHA_RECORDED` (`:1641`) is never compared |
| mado | `SKILL.md:753,758` | X — harness named again in round-evidence prose |
| mado | `.ufo/waves/round-13/frozen/verify.py:1-16` + `frozen/expected.json:2-6` | **F** — pins `gate.sh` + `harness.sh` sha256 and verifies **before** execution; `expected_exit`/`expected_marker` |
| mado | `tools/mado-tripwire.py:1-27` | E — post-hoc no-harm monitor over OMP JSONL; classes `host_mutation\|package_query\|live_probe`; "issued ≠ executed"; detection, not prevention |
| mado | `tools/mado-verify.sh:669`, `:3406` | G/self-test — `STUB_GIT_HEAD`; `git show HEAD:<path> \| sha256sum` committed-byte compare |
| mado | `corpus/lessons/round-14.md:127-129` | J — read-only `jj log` without `--ignore-working-copy` created local snapshot/import state; future calls must use the flag |
| kagi | `corpus/checklist-run.sh:1-40` + `corpus/checklist.tsv:1-12` | **R E** — TSV row registry (`id class lead check expect_exit expect_last reason note`); 16 data rows = 9 `runnable` / 7 `by-hand` (measured); `--only ID` prints `CHECKLIST_ROW: CLEAN\|BROKEN`; splits `delegated` (row re-invokes an existing gate) from `direct` |
| kagi | `corpus/adjacency.tsv:14,82`; `PROVINCE.md:43` | **C** — contested-scope vocabulary (`contested\|shared-read\|writer\|unresolved`) as data with a basis citation + token; chrome-profile contested with kake |
| kagi | `PROVINCE.md:51` | R — `scope-gate.sh`: `--selftest` 61 cases, `--falsify` 18/18 mutations |
| tsukuroi | `SKILL.md:1705-1712`, `:1737`, `:1778` | **I R** — entry commands take `--revision <commit>`, "git object reads or lane files only", write scope `None` |
| tsukuroi | `tools/measure-update-recheck.py:1-14` | I — "`--revision` only reads git blobs with read-only plumbing (`GIT_OPTIONAL_LOCKS=0`)" |
| tsukuroi | `corpus/knowledge/memory-arm-mutants-s8.md:23,150`; `memory-arm-ver-s8.md:27,215`; `closeout-r11.md:337` | **X** — sha256-pinned citations of tameshi `mutate-and-run.sh` = `cf41efaa…`, 1341 L |
| kake | `SKILL.md:208,212` | R — `### Owned freshness gate registry`; gate row cites `replay-proof.mjs` verifying frozen input digests before baseline/candidate |
| kake | `.ufo/round-20/replay-proof.mjs:1-18`; `frozen/citation-locality/expected.json:1-6` | F — `baselineRevision` + `baselineScriptSha256` + per-input `inputs{}`, verified before both CLIs run |
| kake | `scripts/freshness-sweep.mjs:702,855` | J-adjacent — `rev-list --count origin/main..HEAD` (unpushed-units accounting) |
| kake | `.ufo/round-20/resume/mistakes.md:44,47` (citing `corpus/lessons/round-16.md:35-38`) | I — "validator is not identity"; normalized digest required for byte-identity claims |
| kama | `AGENTS.md:6` | **J C** — jj-colocated; HEAD detached after helper commit; read tip with `git rev-parse master` / `jj-lane.sh state`, never `@{u}`, `--abbrev-ref HEAD`, `branch --show-current`; git-writing gates run in `/tmp` clone |
| kama | `SKILL.md:294,303` | R — `## Local gate/probe registry`; "Registered reconciliation" exit map is **0 clean / 2 drift / 1 could-not-evaluate** (inverted vs fleet 0/1/2) |
| kama | `tools/kama-probe.sh:25,110` | R — `--registry PATH` override, same flag name tameshi uses |
| kama | `registry/history/*.json` | R — registry snapshot history with `transitions`, `drift`, stable-rerun expectations |
| kotoba | `verifiers/verify_skill_checklist.py:1-45` | **R** — disposition map over SKILL boxes: `executed:<id>\|delegated:<path>\|unexecuted:<reason>`, pinned by normalized-text sha256 so reword/add/remove FAILs; §schema `kotoba-checklist-v1` |
| kotoba | `verifiers/checklist-command-vocabulary.json:1-30` | R — closed argv[0] vocabulary for checklist commands |
| kotoba | `verifiers/check_assertion_floors.py:34-41,129-131` | R — registry anchor must live **outside** the instrument; `registry_anchor_drift()` |
| kotoba | `verifiers/check_substrate_pins.py:1-30` | I — sha256+mtime pins, `PASS\|DRIFT\|UNKNOWN`, `--json` |
| tabi *(outside the named seven)* | `scripts/check-measurement-binding.mjs:1-20` | **I** — binds a counted claim to counter blob sha256 + `measuredRevision` + `countedInputs`; findings `counted_inputs_undeclared`, `counted_input_changed` (`git diff measuredRevision REV -- <countedInputs>`) |
| tabi *(outside the named seven)* | `scripts/check-measurement-binding.mjs:236-248` | **G** — `resolveRepo()` via `rev-parse --show-toplevel`; refuses on failure; git pinned against graft/replace/fsmonitor |
| tabi *(outside the named seven)* | `SKILL.md:1836-1840` | R — measurement-binding registry row, `--at REV [--reproduce]`, re-runs both arms |
| fleet | `scripts/hyaku/lane-addendum.md:116-145` (esp. `:136-142`) | **J** — canonical rule: jj helper is the only writer; HEAD detached; record measured/pinned revisions as the **branch tip**, never bare `HEAD`; read-only jj only with `--ignore-working-copy` |
| fleet | `scripts/hyaku/jj-lane.sh:51-81` | J — resolution order `origin/HEAD` → `master`/`main` → `show-ref` verify; pure-git `print_state` |

## 3. What is actually shared (clusters)

**A. Row-registry-over-SKILL-items, then execute.** Four lanes already bind prose/checklist rows
to commands: kumitate (`surface-probe --checklists`, executes but via `bash -c`), kagi
(`checklist-run.sh`, executes with expected exit **and expected last line**, plus bijection and
`by-hand` rows), kotoba (`verify_skill_checklist`: static coverage + command-vocabulary test only —
`executed:<id>` names an in-file check and "whether that check's rule captures the box's intent is
the reviewer's call" (`:188-192`); no box command is run), kama (`kama-probe check`, executes a
domain registry). None re-executes **at an arbitrary revision**;
tameshi's `--rev` + mkdtemp fleet-mirror clone is unshared. tameshi's argv-only JSON registry is
strictly narrower than kumitate's shell-string grammar — that is a difference to state, not a
parity claim.

**B. Input-keyed credit.** tabi ships the same rule tameshi is adding, with a different subject:
tabi binds a *counter* (its bytes, the measured revision, the declared counted inputs) and fails
`counted_input_changed` when a declared input moves between `measuredRevision` and `REV`. tameshi
binds a *seat's executed-input set*. kake's `replay-proof`/`expected.json`, mado's two frozen
runners and tsukuroi's `--revision` gates are the same "verify digests, then compare" shape.

**C. jj / repo identity.** The branch-tip rule is already fleet law
(`lane-addendum.md:136-142`) and already restated by kama (`AGENTS.md:6`). mado owns the incident
evidence for the `--ignore-working-copy` half. Repo-identity as a *refusal* (toplevel must equal
the requested root) exists only as tabi's `resolveRepo()` pass-through and mado's
`STUB_GIT_HEAD` self-test; tameshi's realpath-equality refusal
(`tools/pin-disposition.py:79,255`) appears to be the strictest in the fleet — not a duplicate.

## 4. Contested scope

1. **`tameshi-shokunin/tools/mutate-and-run.sh` is tameshi-owned but sibling-consumed.**
   mado runs it inside a registered gate (`mado/SKILL.md:551`, usage `:753,758`) and declares the
   digest "provenance, not an enforced harness pin" (`:589-591`, confirmed in code:
   `mado-verify.sh:1866-1867` only prints `HARNESS_SHA_RECORDED`; the enforced pins are
   `SPEC_SHA` at `:1875` and the derived target); tsukuroi pins its sha in **five** corpus loci
   across three files (`memory-arm-mutants-s8.md:23,150`, `memory-arm-ver-s8.md:27,215`,
   `closeout-r11.md:337`). Measured: `grep -rn cf41efaa` over each lane's `tools/` and `scripts/`
   returns **no hits** — no sibling *gate* reads those pins. Consequence: tameshi's round-17
   repo-identity edit changes the sha and mechanically breaks nothing, but silently ages five
   documentary pins in two sibling lanes. Disclosure is tameshi's; re-pinning is theirs.
2. **Branch-tip semantics belong to the fleet helper**, not to a lane tool. tameshi's
   `pin-disposition.py` fix should implement/quote `lane-addendum.md:136-142` and
   `jj-lane.sh:51-81`, not define a second convention.
3. **kagi↔kake chrome-profile** (`adjacency.tsv:82`, `PROVINCE.md:43`) is the fleet's only worked
   example of *contested* scope declared as data (`contested` + `presence-only` + basis/token).
   It is the template tameshi should copy for item 1 rather than a place tameshi may pin.
4. **Exit-map collision.** kama's registry uses `0 clean / 2 drift / 1 could-not-evaluate`, the
   inverse of the fleet 0/1/2 tameshi implements. Citing kama's registry as precedent without
   noting this would launder a different contract.

## 5. Cite, do not absorb

| Cite | For | Do not import |
|---|---|---|
| tabi `check-measurement-binding.mjs:1-20` | counted-input drift vocabulary (`counted_inputs_undeclared`, `counted_input_changed`) and "counter digest at measuredRevision **and** at REV" | tabi's counter/manifest schema; tameshi's subject is a seat input set |
| kagi `checklist-run.sh:1-40`, `checklist.tsv:1-12` | `delegated` vs `direct` split, `by-hand` rows as declarations, `--only ID` single-row verdict | lead-ERE bijection, runnable floor, 8-column TSV |
| kumitate `SKILL.md:607-609` | the cross-lane gap `--rev` closes (no verdict names its revision); `SKILL.md:587` registry shape | prose-table registry; `bash -c` execution |
| kumitate `surface-probe.mjs:857` | `SKIP(self)` recursion guard semantics for a registry row that invokes the checker | — |
| mado `frozen/verify.py:1-16` + `expected.json:2-6` | the two-evidences shape (digests verified **before** execution; expected exit+marker) | mado's frozen file layout |
| kama `kama-probe.sh:25,110` | `--registry PATH` flag precedent (grade an old registry against a new checker) | kama's 0/2/1 exit map |
| kotoba `verify_skill_checklist.py:1-45,188-198` | disposition-coverage over checklist rows; normalized-text sha pinning precedent; its own stated limit that `executed:` is a claim, not an execution | its `executed\|delegated\|unexecuted` map as a substitute for exit measurement |
| kotoba `check_assertion_floors.py:129-131` | anchor registry outside the instrument (matches tameshi's `registry.json` + `registry-check.py` split) | floor tables |
| kagi `adjacency.tsv:14,82` | `contested`/`shared-read` + basis/token vocabulary | kagi's census |
| fleet `lane-addendum.md:136-142` | authoritative jj branch-tip rule | — |
| mado `corpus/lessons/round-14.md:127-129` | why read-only `jj` needs `--ignore-working-copy` | — |

## 6. Second-order effects / risks

- **Held-count inflation.** A registry row whose argv re-invokes an already-registered gate is
  *delegated*, not independent assurance. kagi splits the two explicitly; tameshi's
  `held=N/M` does not. [INFERENCE] Some tameshi rows will be wrappers; the report should say how
  many, or the held count overstates C2.
- **Absolute paths inside a `--rev` clone.** `registry-check.py --rev` clones into a fleet-mirror
  layout with siblings **symlinked** to the live fleet. A row whose argv names an absolute fleet
  path would therefore read *live* bytes at a "measured rev". tameshi's own rows are lane-relative
  (per contract B, `cwd = lane root`); the hazard is a row that shells out to a sibling — mado's
  `SKILL.md:551` shows that pattern exists in the fleet. [INFERENCE] worth an explicit check when
  building the registry.
- **Doc-pin aging** (§4.1): five sibling loci go stale on landing the `mutate-and-run.sh` guard.
  Not a gate break; still a cross-lane claim change.
- **Parity claim risk.** Kumitate already *executes* its checklist; claiming "first executable
  entry registry" would be false. The defensible claim is the narrower one: argv-only, re-executed
  against committed bytes at an arbitrary rev.
- **jj snapshot mutation** is already evidenced by mado; tameshi's contract rule has a sibling
  precedent to cite instead of an assertion.

## 7. Limits

- No sibling gate was executed; "registered" is read from their SKILL tables, not observed.
- tabi is outside the seven lanes named in the Target; included only because it is the closest
  single prior art for C1. L1 may discard it.
- One kake row (`SKILL.md:212`) was truncated at read time (write-scope cell); no claim is made
  about that cell.
- tameshi's own `registry.json` was not audited here — this seat scanned siblings.

## 8. Connector return

- **Evidence:** §2 table (39 cited rows, 7 lanes + tabi + fleet), §3 clusters, §4 four contested
  boundaries; all path:line values above were read in the live trees at the stated tips.
- **Affected axes:** calibration (C1 — prior-art duplication and held-count inflation), operability
  (C2 — cross-lane consumers of `mutate-and-run.sh`, exit-map divergence, clone-path hazard).
- **Proposed move (one, bounded, contract-compatible):** keep interfaces A/B byte-for-byte; add to
  the round-17 report a short citation block that (i) names tabi's `counted_input_changed` and
  kagi's `delegated|direct` as the prior art for C1/C2 semantics, (ii) states how many
  `REGISTRY_CHECK: held` rows are delegated wrappers, and (iii) discloses the four sibling
  doc-pins of `mutate-and-run.sh` that the jj/repo-identity edit ages. No sibling file edited, no
  schema change, no new instrument.
- **Risks:** the citation block can itself become an overclaim if (ii) is asserted without counting;
  the clone-path hazard stays unnamed unless checked at build time; citing kama's registry without
  its inverted exit map would be a false precedent.
- **Verification:** re-run the §2 greps at the landed tip; confirm `registry-check.py --rev` rows
  contain no absolute fleet paths; `git -C <sibling> grep cf41efaa` still resolving to historical
  text only.

VERDICT: built — adjacency table delivered with four contested boundaries; two overlaps (tabi
input-keying, kagi row-registry) are cite-not-absorb, and `mutate-and-run.sh` is the one real
cross-lane write hazard.
