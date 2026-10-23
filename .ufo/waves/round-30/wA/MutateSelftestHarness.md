Verdict: **SURVIVED — silent detector loss demonstrated in H5b.** Adding one status-capture assignment after `tally_line`'s comparison preserves a green pristine selftest and also makes the same selftest accept a dropped tally operand. This is a harness coverage finding, not a measurement of the frozen counter or a judgment of C1. All modified runner bytes were restored exactly.

## Evidence and scope

Axis: **operability**, specifically whether the selftest remains an effective detector. Secondary observations concern detector coverage; restoration is the no-harm constraint.

Seat: `TameshiR30A2.MutateSelftestHarness-7`.

Scratch root, abbreviated `S` below:

`/fast/scratch/hyaku/tameshi-r30a2-seats/MutateSelftestHarness-7`

All source locations below refer to `S/clone/tools/mutate-and-run.sh` with the frozen fix applied. Locations use the pristine line numbers unless explicitly marked inserted.

- Tally operand list: `tools/mutate-and-run.sh:1431`.
- Runtime completeness refusal: `tools/mutate-and-run.sh:1451-1458`; untouched except that each requested drop probe removed one operand at line 1431.
- Block extraction: `tools/mutate-and-run.sh:1992`.
- Independent assignment-name extraction: `tools/mutate-and-run.sh:1993`.
- Name cardinality assertion: `tools/mutate-and-run.sh:1994`.
- `tally_line` comparison and implicit return: `tools/mutate-and-run.sh:2002-2005`.
- Vector positions and success-count assertion: `tools/mutate-and-run.sh:2011-2018`.

### Exact setup commands

Executed as an `&&` chain; exit 0, no output:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r30a2-seats/MutateSelftestHarness-7
 timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r30a2-seats/MutateSelftestHarness-7/clone
 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/MutateSelftestHarness-7/clone checkout -q --detach f09d3425258403a51422c9959e25340807982947
 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/MutateSelftestHarness-7/clone apply /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/witness/fix.diff
```

The leading spaces on the last three displayed commands are insignificant. No production source was edited.

### Detector and expected outcome

Every completed detector invocation ran from `S/clone`, with the Git environment variables unset, using the same bounded command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 bash tools/mutate-and-run.sh --selftest
```

Expected control: exit 0 and `VERDICT: PASS` on the frozen fixed runner. Expected drop detector: nonzero exit on the runner with ` "$st_citecheck"` removed from the tally loop at line 1431. No status assignment, runtime guard, or other tally code was changed for that drop.

For every log basename in the tables except `pristine.stdout` and `drop-control.stdout`, the exact surrounding command was:

```sh
set -o pipefail && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 bash tools/mutate-and-run.sh --selftest |& tee /fast/scratch/hyaku/tameshi-r30a2-seats/MutateSelftestHarness-7/<basename> | wc -l
```

`<basename>` is the literal filename listed below. `pristine.stdout` used `| tee <absolute-log-path>` without `wc -l`; `drop-control.stdout` used `|& tee <absolute-log-path>` without `wc -l`. Pipeline exit status was preserved by `pipefail`. Counted logs had 103 lines, except `H3-names-drop.stdout`, which had 96.

The first requested asynchronous baseline launch was refused by the tool's existing background-job limit before execution. It is not a detector result. All measured runs were synchronous and completed without timeout. Only one detector ran at a time because the source bytes were shared within this isolated seat; read-only hash collection ran concurrently.

## Mutants and results

Each harness mutant was applied alone to pristine bytes, then the same last-operand drop was added. Both edits were reversed before the restored run. The preceding restored run supplied the next row's pristine baseline. `pristine.stdout`, `drop-control.stdout`, and `drop-restored.stdout` also establish the intact-harness control: **0 / 1 / 0**, with summaries **101/101 PASS / 98/101 FAIL / 101/101 PASS**.

| ID | Harness mutation | Pristine exit | Harness-only exit and output | Harness + drop exit and output | Restored exit | Harness verdict; drop verdict |
|---|---|---:|---|---|---:|---|
| H1 | Start extraction at the tally `for` line, omitting counter initialization | 0 | 1; 98/101, FAIL | 1; 98/101, FAIL | 0 | KILLED; INCONCLUSIVE because the harness-only control is red |
| H2 | End marker expects an indented closing brace instead of the function's column-zero brace | 0 | 1; 98/101, FAIL | 1; 98/101, FAIL | 0 | KILLED; INCONCLUSIVE because the harness-only control is red |
| H3 | Derive status names from the tally operands rather than independent `st_*=$?` assignments | 0 | 0; 101/101, PASS | 1; names=8, then unbound variable; no final verdict | 0 | SURVIVED; drop KILLED |
| H4 | Replace exact nine-name check with a nonempty-name check | 0 | 0; 101/101, PASS | 1; 98/101, FAIL | 0 | SURVIVED; drop KILLED |
| H5a | Remove first-line equality; check subprocess exit only | 0 | 0; 101/101, PASS | 1; 99/101, FAIL | 0 | SURVIVED; drop KILLED |
| **H5b** | **Capture comparison status with `rc=$?`, but omit returning that status** | **0** | **0; 101/101, PASS** | **0; 101/101, PASS** | **0** | **SURVIVED; drop SURVIVED — silent detector loss** |
| H6 | Repeat position 7 instead of testing position 8, keeping nine iterations | 0 | 0; 101/101, PASS | 1; 98/101, FAIL | 0 | SURVIVED; drop KILLED |

The H1/H2 double-mutant failures are not credited as drop kills. Their harness-only baselines already failed. H3's nonzero exit includes an explicit cardinality failure before the unbound-variable termination.

### Exact mutation recipes

All replacements were surgical edits of `tools/mutate-and-run.sh`. No two harness mutants were combined.

H1, replace line 1992 with:

```bash
  tblock=$(awk '/^  for st in /{f=1} f&&/^}$/{exit} f' "$SELF")
```

H2, replace line 1992 with:

```bash
  tblock=$(awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^  }$/{exit} f' "$SELF")
```

H3, replace line 1993 with:

```bash
  mapfile -t tnames < <(awk '/^  for st in /{for (i=4; i<NF; i++) {s=$i; gsub(/["$;]/,"",s); print s}}' "$SELF")
```

H4, replace line 1994 with:

```bash
  [[ -n "$tblock" && ${#tnames[@]} -gt 0 ]]
```

H5a, replace line 2004 with:

```bash
    [[ $rc -eq $want_rc ]]
```

H5b, insert **only** `rc=$?` after line 2004, producing:

```bash
    out=$(bash "$root/tally.sh" 2>&1)
    rc=$?
    [[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
    rc=$?
  }
```

This is a plausible shell refactoring defect: preserving the comparison status for later use but forgetting that the final assignment, not the comparison, now determines the function's return value. The assignment succeeds, so callers accept unsuccessful comparisons.

H6, replace line 2011 with:

```bash
    for ti in 0 1 2 3 4 5 6 7 7; do
```

For every drop probe, replace line 1431 with:

```bash
  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck"; do
```

### Evidence log mapping

All logs are directly under `S`; line references refer to those saved outputs.

| ID | Harness-only log | Drop log | Restored log | Pristine baseline log |
|---|---|---|---|---|
| H1 | `H1-start.stdout:95-103` | `H1-start-drop.stdout:95-103` | `H1-restored.stdout:95-103` | `drop-restored.stdout:95-103` |
| H2 | `H2-end.stdout:95-103` | `H2-end-drop.stdout:95-103` | `H2-restored.stdout:95-103` | `H1-restored.stdout:95-103` |
| H3 | `H3-names.stdout:95-103` | `H3-names-drop.stdout:95-96` | `H3-restored.stdout:95-103` | `H2-restored.stdout:95-103` |
| H4 | `H4-count.stdout:95-103` | `H4-count-drop.stdout:95-103` | `H4-restored.stdout:95-103` | `H3-restored.stdout:95-103` |
| H5a | `H5a-exit-only.stdout:95-103` | `H5a-exit-only-drop.stdout:95-103` | `H5a-restored.stdout:95-103` | `H4-restored.stdout:95-103` |
| H5b | `H5b-swallow.stdout:95-103` | `H5b-swallow-drop.stdout:95-103` | `H5b-restored.stdout:95-103` | `H5a-restored.stdout:95-103` |
| H6 | `H6-vector.stdout:95-103` | `H6-vector-drop.stdout:95-103` | `H6-restored.stdout:95-103` | `H5b-restored.stdout:95-103` |

Intact harness with the drop, `S/drop-control.stdout:95-103`, exit **1**:

```text
PASS tally harness: block extracted, leg status names=9 (want 9)
FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (0/9)
PASS help exits 0
PASS missing --target exits 64
PASS --regression refuses --target (exit 64)
MUTATE_SELFTEST: 98/101 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.JHudGt)
```

H5b with the **same drop**, `S/H5b-swallow-drop.stdout:95-103`, exit **0**:

```text
PASS tally harness: block extracted, leg status names=9 (want 9)
PASS tally harness: all nine legs pass -> PASS passed=9, exit 0
PASS tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (9/9)
PASS tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (9/9)
PASS help exits 0
PASS missing --target exits 64
PASS --regression refuses --target (exit 64)
MUTATE_SELFTEST: 101/101 pass
VERDICT: PASS
```

H3's complete final diagnostic, `S/H3-names-drop.stdout:95-96`, exit **1**:

```text
FAIL tally harness: block extracted, leg status names=8 (want 9)
tools/mutate-and-run.sh: line 1999: tnames[$k]: unbound variable
```

H5a's drop run, `S/H5a-exit-only-drop.stdout:96-98`, demonstrates reduced sensitivity without a silent pass:

```text
FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (8/9)
PASS tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (9/9)
```

H6 also reports `(9/9)` on both pristine vector families despite omitting position 8. Thus success-count equality alone does not establish distinct-position coverage. The requested drop still fails because the all-zero case remains checked.

## Hashes and restoration evidence

Exact command, run before mutation, on each harness-only and harness-plus-drop state, and after every restoration:

```sh
sha256sum tools/mutate-and-run.sh
```

Pristine fixed-runner hash, abbreviated **B**:

`9a931bc2d0c31c32dd3a4ccf6594b56c3474628cca513b675901a8666fbec7d4`

The intact-harness drop-control hash was:

`225a08529357ff395cb7de5c9e95450299a291a7eb57a139b87731be775a0f2b`

| ID | Before | Harness-only SHA-256 | Harness + drop SHA-256 | After restoration |
|---|---|---|---|---|
| H1 | B | `840c943132b4bec8408ec562dea3fb858069551cfc051ec96028fe32624cfa0a` | `18748ecb048cbbe287dc5aa3d23d8d22105ddd18d8afba05739f3c1a16b44210` | B |
| H2 | B | `eac585d35d9e4b3c45bb004e780b08b5b599358d20affbf0c68e927453aefc10` | `ef575991ce441c67c95b0145818f990f59e2491cd20a0950165bbc9f9203d358` | B |
| H3 | B | `6e8a8fe63751004b67c21f6956d59d9d90ed3c2aca43bc4ff3a4bd14ca0025ca` | `d19773179385da76b356746cadaac5af1312b022124c710c0a82f6a5744a97fb` | B |
| H4 | B | `ed0de653cf5886774f126b0305a0e236da72a7968e9cf0178c756ab83d08b007` | `1290bf8f6254d3fbb9125d3bd359970b7e54d8e5a650a5e6a14c82d44bde01b2` | B |
| H5a | B | `d4670ad058212e06b0d60b21a4c3d22dd13a4e82ed856ad583e201da02394a99` | `dc006e233437616b2d7149305b2cf6c38ecbd4640b5ef15183ebf825dcbe4f64` | B |
| H5b | B | `adfd2ac15c843f1fb5b7f34aa54c3d71d68077bb4289bdf872d9000ae9c2eae7` | `454fee3088377c6641972687bd97413ee2d9ea8bbec63745cf97b17f3f3fe251` | B |
| H6 | B | `81d6c6f361b362aa418f28723943b42d9501b5fe7da3ec8a81493b48018863ad` | `bd08a7779c4c5472c4123c90404c6f0f17117af7940a6a0a155ffb4ce2c48845` | B |

The drop control was also restored to B before H1. All eight restoration runs exited 0 with `MUTATE_SELFTEST: 101/101 pass` and `VERDICT: PASS`. Final restored evidence is `S/H6-restored.stdout:95-103`; final observed source hash is B. Restoration used inverse surgical edits, including removing H5b's inserted assignment, not a destructive Git operation.

Execution boundaries: no sealed directory access; no counter invocation; no full `--regression` replay; no subagents or other agent runtime; no production-source edits; no Git write commands outside this seat's clone; no commits. No tools were installed or updated. All detector calls finished. Final command `timeout 10 fuser -v /fast/scratch/hyaku/tameshi-r30a2-seats/MutateSelftestHarness-7/clone` exited 1 with no output, reporting no process using that directory at that check; no kill was issued. This is not a claim about unrelated peer processes or every temporary subdirectory.

## Smallest safe correction

For the demonstrated H5b defect, delete the added `rc=$?` so the comparison remains `tally_line`'s final command. If capturing its status is genuinely needed, explicitly `return "$rc"` afterward. No tally change is required. The frozen runner already has the comparison in final position and has been restored to that exact form; this probe does not propose changing the contract or shipping the mutant.
