# K05SpotcheckCoverage — does the round-17 wave-1 plan cover every routed defect and jj item?

Seat: TameshiR17.K05SpotcheckCoverage (critic, wave 1). Read-only. Scratch `/tmp/tameshi-r17w1-K05SpotcheckCoverage-fvG11f` (fleet-mirror clone at `98bea7d`; tools were edited only in that clone and restored with `git checkout -- tools/`). No installs.

Inputs I judged against:
- the closure `corpus/lessons/round-16-verifier-spotcheck.md` @98bea7d, §2, §4 (G6), §5 and §6 items 1–6;
- `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditTameshi.md` (§1, §2, §4, §5 R1–R3, §6) and `JjTrialTameshi.md` (hazards 1–8, Recommendations);
- the plan, which is the wave context plus the 69 item targets in `.ufo/waves/round-17/spec1.json`, and the round prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-17.md` §6.4 and §6.5.

Axes: **calibration** (C1), **operability** (C2), plus **step-1 conformance**, the closure's precondition.

## 1. Coverage matrix: closure-routed items

| Item | Plan items | Covered? | Gap / residual risk |
|---|---|---|---|
| **R16-OP1**: clean-capable live-tree disposition verdict, red-before and green-after, evidence immutable | X01 (v2 tool), X02 (v2 manifests), S09 (red-before 2/2 live, 1/0 archived), M02, K03, R03, X12. Red-before receipt `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt` already exists. | **yes** | (a) The v1 command stays at exit 2 forever. SKILL.md:1681 still registers it with verdict map `0 clean`; only the parenthetical says "2 by design". No item appends a pointer from that row to the round-17 v2 command. W03 adds a new registry, but the old row is not annotated, and that is the sweep the closure already faulted. (b) Contract A does not require the `historical_inputs` rev to be an ancestor of the branch (audit R2 asks for `merge-base --is-ancestor`). K03 attacks this, but no builder is told to add it. The X02 candidate does hold: `git merge-base --is-ancestor 4acc607 98bea7d` returned 0. The four `tools/` pins in round-13 `expected.json` match at 4acc607: `pin-disposition 297253971dab`, `witness-metadata df3390682a04`, `bash-witness-study 49e9e5e20b73`, `mutate-and-run 75ed934dc863`. |
| **R16-C2a**: stale round-14 recipe, plus a fresh-seat re-read at the new sha | R08 (line-preserving draft and archived-run exits), S09, S10. The re-read is declared for wave 2 (context C1). | **yes, conditional on wave 2** | The re-read must happen after R08's text is installed **and** after X02's manifests and X01's tool land. The new recipe runs those, so their bytes become traced inputs. See failure 1. |
| **R16-C2b**: input-keyed credit, red-before on the round-14 bucket | X07, X08, X09, X10 (legacy overlay), X16, S12, S13, R05, K02, M01, V03 | **yes** | There is an instrument hole the plan does not name; see §3, finding H1 (cached-import trace). Two scope holes also hit full-page coverage: buckets whose commands read only via `git show REV:…` or sibling repos trace **no** lane input, so they get `inputs-unrecorded`; and a recorded `SKILL.md` input over-invalidates on any later page edit. K02 attacks both, but the context does not decide them. |
| **R16-C2c**: box-3 text corrected by append | R06 (draft and SHONEN parse check) | **yes** (L1 applies) | none beyond the dependence on C1 |
| **R16-EV1**: stale `runner-sha256.txt` | R07 (draft). **Already applied live, uncommitted**: `git status` shows ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`, a 4-line dated append naming `0673d2e5…`, with the original line untouched. | **yes** | Recurrence: X05 moves the runner **again** (`0673d2e5` → new). No item says round-17 runner receipts (selftest/regression sha) must be produced after install, at the final tip. That is the same mistake class as EV1. |
| **R16-MON1**: monitor runs the registered entry commands so a live-tree change is caught *inside the round* | X03, X04, X13, X15, S01–S08, R04, K04, V02 | **tool yes; schedule no** | (a) The context declares no monitor run after the L1 installs staged tools or edits SKILL. "Inside the round" means at least one `registry-check.py` run between install and landing, and the plan names none. (b) Registered commands that write into the lane tree are not flagged (H3). |
| §4 **G6** disagreement (sha-only credit) | same as C2b; W01 (mistake rows), R02/W04 (QUALITY 23) | **yes** | none |
| §2 step-2 exit was only [INFERENCE] | S09 executes it | **yes** | none |
| §5 quality: "corrections sweep every mention" | S10 (round-14 recipe, disposition, box-3 mentions only) | **partial** | H2: stated selftest/regression outcomes in SCORECARD capability rows. Two are already stale at 98bea7d, and this round's own tool edits will make two more stale. No item owns them. |
| Prompt §6.5: each routed defect becomes a lesson-backed QUALITY criterion or fix, or the report says why not | R02, W04 (criteria 23–26 cover C2b, OP1, MON1, EV1), W01 | **mostly** | C2a and C2c are partial-sweep failures. The draft list has no criterion for them, and no "why not" is assigned. The existing §Evidence-standard sweep rule can serve, but the report must say so explicitly. |

## 2. Coverage matrix: jj items

| Source item | Plan items | Status | Gap |
|---|---|---|---|
| Audit R1 / §1.1 / §2.2: no repo-identity guard in `mutate-and-run.sh:1000-1035` | X05, S18; also the guard in contract A | **covered** | none |
| Audit R2 / §1.2 `:317-341` / §2.3: HEAD is `@-` | X06, X11 (red-before fixture), S03, S17 | **covered** | none |
| Audit R2: "assert `merge-base --is-ancestor` before citing" | none | **gap** | Contract A's historical rev has no ancestor check. Contract C's `trace-inputs.py` records `rev` = **`git rev-parse HEAD` of root**. That reintroduces the bare-HEAD pattern the prompt forbids (§6.4: "record measured/pinned revisions as the branch tip, never bare `HEAD`"). It is harmless in a fresh plain clone. It is wrong if a seat traces in the live colocated lane, which is detached since the round-17 helper commits. |
| `SKILL.md:1033` `current = git show HEAD:<path>` | R09 (draft), S11 | **covered** (draft; L1 applies) | none |
| Fixture `rev-parse HEAD` (`mutate-and-run.sh:1533/1592/1627`, `pin-disposition` fixtures, `probes.mjs`) | S11 classifies | **already true (keep)** | Decline reason not stated in the plan. C03 should record "fixture under /tmp, attached HEAD". |
| Audit §1.4 `measure.py:79` optional identity guard | none | **gap (low)** | X07 copies round-16 `measure.py` without a guard. Decline reason ("default repo is the lane itself") should be written down, or guard it in X07. |
| Audit §1.4 `probes.mjs` `FXROOT` override plus `rmSync(recursive)` | none | **gap (low)** | The file is evidence (immutable), so decline. The plan has no decline line, though, and SKILL.md:1790 names the harness as runnable. Add a one-line limit near :1790: "never set FXROOT under the fleet root". |
| Audit R3: lane repo config lacks `auto-track` and `commit` does not fail closed | S20 (state), C03 | **config now true; helper half is fleet-owned** | I read the lane's `.jj/repo/config-id`: `900fa08b5e426ae84a97`, not the audit's `86a634…`. `~/.config/jj/repos/900fa08b…/config.toml` (mtime 12:07) carries `auto-track = "none()"`. `jj-lane.sh cmd_commit` (`:186`) still checks only `-d .jj`. That is a fleet script the lane may not edit, so the decline should become an `l0-questions.md` append. No item routes it. |
| Audit §2.5 hooks/attribute bypass, §2.6 index reset | none | **already true / inert** | No decline line; one sentence in the report suffices ("0 hooks, 0 attributes", audit §4). |
| Trial: keep `auto-track="none()"` | — | **already true** (above) | none |
| Trial: `.gitignore` gets `.ufo/state/`, `.ufo/watchdog.log` | none in spec | **applied live, uncommitted** (`git diff .gitignore` → `+.ufo/state/`, `+.ufo/watchdog.log`) | It must be in the landing commit's path list. See H4 for the missing `__pycache__/`. |
| Trial: "lane tooling needs no changes" | X05 and X06 contradict it | **declined, by evidence** | The trial ran only attached-HEAD, sibling-pinned gates. The audit's §2.2/§2.3 reproductions beat it. The report should record the disagreement, not silently pick a side. |
| Trial: cite `pushed`/`landed`, never `committed` | prompt §6.4; W06 | **covered** | none |
| Trial hazards 2/7: `--include-ignored` on named files; a named directory commits like `git add <dir>` | none | **gap**: H4 | — |
| Trial hazard 4: detached HEAD is permanent | S11, R09, X06 | covered, **except** the new `trace-inputs.py` `rev` (above) | — |
| Trial hazards 5, 6, 8 (git-add staging, fsck noise, policy invariants) | prompt forbids `git add`; no fsck gate; helper blocklist | **already true** | none |

## 3. New findings (evidence)

**H1: an openat trace misses the tracked source of a cached Python import and records an untracked `.pyc` instead.** Contract C, `trace-inputs.py`.
In the clone at 98bea7d I ran:
```
strace -f -qq -e trace=openat -o st2.log python3 -c "import sys; sys.path.insert(0,'.ufo/evidence/round-16'); import measure"
```
I ran it twice and grepped run 2 for `round-16/(__pycache__|measure)` excluding ENOENT. That left one line:
```
openat(AT_FDCWD, ".../.ufo/evidence/round-16/__pycache__/measure.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
```
- `measure.py` itself is not opened. It is only stat'ed.
- `git ls-files --error-unmatch …pyc` → "Did you forget to 'git add'?" The file is untracked.
- So a traced command that imports a lane module, such as an assembler or measure that reuses the round-16 sectionizer by import, records an untracked file. Measure v2 then reports `input-missing:<pyc>` and uncredits the bucket. The real input, the `.py`, drifts unseen.
- The live lane already shows `?? .ufo/evidence/round-16/__pycache__/` (mtime 12:11:04, during this wave). Some seat imported round-16 `measure.py`.
- Smallest fix: `trace-inputs.py` runs the child with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPYCACHEPREFIX=<mkdtemp>`, or adds `-e trace=…,stat,newfstatat,statx` and records stat'ed `.py` sources. Inputs also need a tracked-at-REV filter (contract C says "lane-tracked"; the trace JSON contract does not). Add an X08 selftest case: import the same module twice; `inputs` must contain the `.py`.

**H2: stated outcomes that this round's own tool edits will falsify.** No owning item; this is the r16 harm class.
`git grep` @98bea7d:
- `SCORECARD.md:244` `pin-disposition.py --selftest → 18/18 PASS0`. X06 adds a case.
- `SCORECARD.md:246` `evidence-disposition.py --selftest → PASS34/34`. X01 adds about 8 cases.
- Already stale at 98bea7d: `SCORECARD.md:241` `MUTATE_SELFTEST: 80/80` (runner prints 83/83 since r16) and `:242` `REGRESSION: PASS (cases=6 …)` (now cases=7). X05 changes 83 again.

These rows are the source X04 builds registry rows from. Either a registry row encodes the count in `stdout_contains` and fails, or it is exit-only and the prose stays wrong unseen. Smallest fix: one appended, dated "current outcome at <tip>" note under `## Capabilities` (or per row), written **after** install from the X15-style post-install run. Also widen the S10-style sweep to every `n/n` selftest statement for the three edited tools.

Counter-check: the edits do not break other registered gates. In the clone I appended one comment byte to `tools/mutate-and-run.sh`, `tools/pin-disposition.py` and `tools/evidence-disposition.py`:
- `bash-witness-study.py count` → 0
- `witness-metadata.py --check --companion …round-13/witness-metadata.json` → 0
- `context-capture.py --check` → 0 `CONTEXT: OK (id=context_consistent …)`
- v1 round-14 disposition → 2 `expected_input_digest_mismatch`, unchanged from before the edit

All four gave the same results unedited at 98bea7d. X05, X06 and X01 add no **new** gate breakage among these four. Their only harm surface is stated counts.

**H3: a registered capability command writes into the lane evidence tree.**
- The round-15 capability row `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4…` writes `attempt-N/` and `verification-N.json` under `.ufo/evidence/round-15/` on every run (`verify.py:323-331`).
- Live lane now: `?? .ufo/evidence/round-15/attempt-4/` and `?? .ufo/evidence/round-15/verification-4.json` (mtime 12:21:56, wave 1; S06 runs it "from the live lane root").
- `registry-check.py --root .` (the default) would add another attempt on every monitor run.
- Step-1 conformance checks porcelain-empty and "no leftovers". The L1 must either delete these seat-generated attempts (untracked; prompt §6.5 says to resolve leftovers) or commit them as un-authored verification runs and name them.
- Smallest fix: R04/X04 mark that row `--rev`-only (clone), and the round report names `attempt-4` as discarded or kept.

**H4: `.gitignore` lacks `__pycache__/`; a directory-named helper commit would admit `.pyc`.**
Trial hazard 7 says a named directory commits like `git add <dir>`, respecting `.gitignore` only. If the landing commit lists `.ufo/evidence/round-16` or `.ufo/evidence/round-17` as a directory, the untracked `.pyc` lands. Smallest fix: add `__pycache__/` to the live `.gitignore` edit already in progress, or delete the cache and list evidence paths as files.

## 4. Which items would the next closure most likely fail (ranked)

1. **C1 `box3_full_page` at the measured commit** (likelihood high). Full-page credit now needs every instruction bucket re-read **after**:
   - the last SKILL.md edit: R08's recipe, R09's :1021-1068 text, W03's new section;
   - the last install of every traced tool: X01, X05, X06, and the round-17 measure/assemble/trace tools themselves.

   The read must also be **before** no later change: any post-wave-2 fix to a traced input yields `input-drift`, and the round has no wave 3. On top of that, H1 (pyc) and git-object-only buckets (`inputs-unrecorded`) can uncredit buckets that were read honestly. Correction:
   - freeze instruments and SKILL text, committed, before the wave-2 cold-read seats clone;
   - run `measure.py --rev <tip>` before landing and send each `input-drift`/`inputs-unrecorded` bucket to the ≤8-seat residual pass;
   - decide in contract C how git-object-only buckets get inputs (for example, the seat records the blobs it read as `inputs` at `read_rev`).
2. **Stated-outcome sweep (H2)** (medium-high): capability rows 241/242 are already stale, and 244/246 will go stale on install. A non-author re-running a capability evidence command sees a count that does not match. That is the closure's own operability signal ("a checklist item that no longer produces its stated outcome").
3. **Step-1 leftovers (H3, H4)** (medium): `attempt-4`, `verification-4.json`, `__pycache__/` and the `staged/` tree must each be committed-and-named or removed before the report. The `.gitignore` and EV1 edits must be in the commit path list.
4. **OP1 read as self-fulfilling** (medium): the v1 command still exits 2. SKILL :1681 still maps it to `0 clean`. registry.json grades the new command instead. The closure accepts this only if three things hold: the :1681 row gains an appended pointer to the v2 command and its manifests; `registry-check --rev 98bea7d --registry <after>` is shown with the v2 rows failing before; and no row's `expect` is weakened (K04).
5. **MON1 "inside the round"** (medium-low): there is no declared monitor run between install and landing. Add one `registry-check.py --rev <pre-landing tip>` run as evidence.
6. **jj declines unstated** (low): helper fail-closed on auto-track (fleet-owned, so an L0 question), `probes.mjs` FXROOT, `measure.py` guard, hooks/index inertness, and the trial-vs-audit disagreement. C03 should emit these as decline rows. The bare `HEAD` in `trace-inputs.py` `rev` should instead resolve the branch tip, or require a caller `--rev` and assert ancestry.

## 5. Smallest safe corrections (L1-actionable)

- X08 (or a wave-2 patch): bytecode suppression or stat tracing, plus a tracked-at-REV filter, plus a double-import selftest (H1). Record `rev` as the branch tip and not `HEAD`, or assert `merge-base --is-ancestor`.
- Contract A: require `historical_inputs[*].rev` to be an ancestor of the branch tip (exit 2 `historical_input_unavailable` otherwise).
- After installing staged tools: rerun the selftests/regression at the tip, append the current counts to SCORECARD capability rows 241/242/244/246, and append a pointer at SKILL.md:1681 to the v2 command (H2, OP1a).
- Sequence: install tools and SKILL text, then commit, then the wave-2 cold-read and monitor run, then `measure.py --rev <tip>`, then a residual re-read of drifted buckets.
- `.gitignore`: add `__pycache__/`. Name `attempt-4` and `verification-4.json` as discarded or kept. Mark the round-15 `verify.py` registry row as clone-only.
- Write decline lines for the jj items listed under §4 item 6, and append an `l0-questions.md` entry for the helper's auto-track fail-closed.

Verdict: **partial**. Every routed defect (OP1, C2a, C2b, C2c, EV1, MON1, G6) and both high-blast-radius jj risks (R1, R2) have owning items. The gaps are three uncovered findings (H1 pyc trace hole, H2 stated-count sweep, H3/H4 leftovers), three unscheduled steps (monitor-in-round, freeze before the cold-read, residual re-read), and a set of jj declines and ancestry checks that nobody owns.
