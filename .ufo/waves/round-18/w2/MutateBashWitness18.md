# MutateBashWitness18 — scoped mutation probe
## Scope and axes
- Axes: **depth + calibration** (verification-fixture craft); **operability** monitored. This is a leaf mutation probe, not a round judgment.
- Read revision: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`. Target: `tools/bash-witness-study.py`.
- Result: **2 KILLED, 10 SURVIVED, 0 INCONCLUSIVE**, across 12 single-point mutants. Every `@old` had `count == 1` before mutation. All 12 pristine and all 12 restored owning selftests passed.
- The actual owning invocation is positional `selftest` (`tools/bash-witness-study.py:1701,1715,1730-1731`), not a literal `--selftest` option. No usage-error invocation was counted as a detector.
- Scratch root: `/tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC`; base clone: `/tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC/fleet/tameshi-shokunin`. Twelve independent scratch clones under `/tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC/mutants/MB01` through `MB12` each owned its own source and Git index; shared Git objects were only read. No sibling source was mutated.
- Only live-lane write: this report. No live-lane Git write, no `jj`, no source fix, no integration, no runtime/route changes, no subagent dispatch, and no background job. Foreground detector calls were batched four at a time and awaited before restoration.
## Commands and isolation
Clone and detach of the base copy both exited **0** with empty stdout/stderr:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC/fleet/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git -C /tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC/fleet/tameshi-shokunin checkout -q --detach 01d586ddbc5fcd78659557c4e93a6ee8517b87d1
```
The clone setup additionally scrubbed every inherited `GIT_*` key and pinned clone-time `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`. Sibling links were created only beside the base scratch clone per the assignment. Each independent mutant clone was made with `git clone --shared -q /tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC/fleet/tameshi-shokunin <scratch-repo>`; all twelve clone exits were **0**.
The same bounded command was used on pristine, mutated, and restored bytes of each instance. For the following template, `ID` is the literal table ID and `R` is its absolute scratch repository path:

```sh
W=/tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC
ID=MB01  # MB01..MB12, as enumerated below
R="$W/mutants/$ID/tameshi-shokunin"
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  /usr/bin/bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$W" "$W" --unshare-net --die-with-parent --chdir "$R" \
  env -i PATH=/usr/bin:/bin HOME="$W/home" TMPDIR="$W/tmp" LC_ALL=C \
  /usr/bin/timeout --signal=TERM --kill-after=5s 30s \
  /usr/bin/python3 "$R/tools/bash-witness-study.py" selftest
```
Actual launcher cwd was `R`, and the parent launcher also removed every inherited `GIT_*` name. At the detector entry point **no `GIT_*` key was set**, including the configuration pins: this avoids an outer pin masking a pin-removal mutant. HOME/TMPDIR were private scratch directories. The production `git_clean_env()` supplied its own pins except where mutated. The selftest itself deliberately exported GIT_DIR/GIT_WORK_TREE pointing only at its temporary canary repository. The fleet and host outside the scratch root were read-only, /tmp was a private namespace, and networking was unshared. All runs completed without timeout.
An initial base-clone detector used the identical envelope with `R=/tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC/fleet/tameshi-shokunin`: exit **0**, `WITNESS_SELFTEST: 43/43 pass`, `VERDICT: PASS`. Thus **37** owning selftest invocations were exercised: one initial base probe plus 12 pristine / 12 mutated / 12 restored.
## Mutation results
All source pointers below are lane-relative at the read revision. `P/M/R` are actual pristine/mutated/restored exits. Every stderr was empty. The expected outcomes listed here were registered in the tool transcript before the edits; all twelve predictions held. For survivors, the prediction was explicitly an inference that no current case would turn red, not evidence of safety.
| ID | Source point | Single change | Expected owning detector | P/M/R | Mutant output / failing cases | Result |
|---|---|---|---|---|---|---|
| MB01 | `tools/bash-witness-study.py:336` | Remove prefix scrub (`if True`) | Two Git-redirection cases fail | 0/1/0 | WITNESS_SELFTEST: 41/43 pass; VERDICT: FAIL; `GIT_DIR/GIT_WORK_TREE cannot redirect materialization`, `GIT_DIR/GIT_WORK_TREE cannot redirect sweep` | **KILLED** |
| MB02 | `tools/bash-witness-study.py:336` | Narrow prefix to `GIT_DIR` | Sweep-redirection case fails | 0/1/0 | WITNESS_SELFTEST: 42/43 pass; VERDICT: FAIL; `GIT_DIR/GIT_WORK_TREE cannot redirect sweep` | **KILLED** |
| MB03 | `tools/bash-witness-study.py:336` | Scrub only `GIT_DIR` and `GIT_WORK_TREE` | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB04 | `tools/bash-witness-study.py:337` | Delete global-config pin | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB05 | `tools/bash-witness-study.py:337` | Use `REPO / ".gitconfig"` instead of `/dev/null` | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB06 | `tools/bash-witness-study.py:338` | Set NOSYSTEM to `"0"` instead of `"1"` | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB07 | `tools/bash-witness-study.py:338` | Delete NOSYSTEM pin | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB08 | `tools/bash-witness-study.py:1259` | Remove hooks-off option from init only | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB09 | `tools/bash-witness-study.py:1264` | Remove hooks-off option from add only | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB10 | `tools/bash-witness-study.py:1269` | Remove hooks-off option from commit only | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB11 | `tools/bash-witness-study.py:1246` | Use `dir=private_root.parent` for child tree | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |
| MB12 | `tools/bash-witness-study.py:1681` | Delete wrong child `private_root / "missing"` | [INFERENCE] No current case fails | 0/0/0 | WITNESS_SELFTEST: 43/43 pass; VERDICT: PASS; failing cases: none | **SURVIVED** |

The killing cases are defined at `tools/bash-witness-study.py:1333-1336`: the complete scrub removal fails both materialization and sweep; the GIT_DIR-only prefix still protects object materialization but fails the sweep canary. MB03 shows that protecting those two planted keys alone is sufficient to satisfy the current detector despite losing the full-prefix contract stated at `:66-67`.
## Durable routing: named survivor coverage gaps
Route every row below to **tameshi / `tools/bash-witness-study.py` selftest owner**, through TameshiR18’s report integration. These are open coverage findings, not permission to alter the contract, and no tool fix was made in this seat. No additional adversarial detector was run.
| Gap | Survivor | Name and source | Routed finding |
|---|---|---|---|
| BW18-G01 | MB03 | **GIT-prefix completeness** — `tools/bash-witness-study.py:333-339,1284-1300,1333-1336` | The two-key denylist passes both existing canary cases but no longer scrubs arbitrary GIT_* names. Route a bounded fixture for keys beyond GIT_DIR/GIT_WORK_TREE (for example GIT_INDEX_FILE/GIT_COMMON_DIR/GIT_CONFIG_COUNT), with a named failing case. Actual redirected behavior for those extra keys was not run here. |
| BW18-G02 | MB04 | **Global-config pin removal** — `tools/bash-witness-study.py:337,1257-1278` | Removing GIT_CONFIG_GLOBAL=/dev/null is not detected. Route a poisoned private-HOME global-config canary, so this guard removal is failure-backed rather than relying on a benign environment. |
| BW18-G03 | MB05 | **Global-config wrong anchor** — `tools/bash-witness-study.py:337` | Using REPO/.gitconfig instead of /dev/null is not detected. Route an anchor-discriminating repository-config fixture; no such poison was planted in this probe. |
| BW18-G04 | MB06 | **NOSYSTEM false boundary** — `tools/bash-witness-study.py:338` | Changing the pin value from 1 to 0 passes. Route a controlled system-config canary or equivalent bounded behavioral assertion that distinguishes enabled and disabled system configuration; host system configuration was not poisoned. |
| BW18-G05 | MB07 | **NOSYSTEM missing pin** — `tools/bash-witness-study.py:338` | Deleting the NOSYSTEM pin passes. Route a distinct missing-pin regression through the same controlled configuration surface; this is separate from the false-value mutation. |
| BW18-G06 | MB08 | **Fixture init hooks-off pin** — `tools/bash-witness-study.py:1258-1262` | Removing the explicit hooks-off option from fixture init passes. Route command-pin coverage and assess whether init has an independent relevant hook/template effect; this survivor alone does not demonstrate hook execution or an exploit. |
| BW18-G07 | MB09 | **Fixture add hooks-off pin** — `tools/bash-witness-study.py:1263-1267` | Removing the explicit hooks-off option from fixture add passes. Route an applicable hostile fixture-hook canary so this omission is discriminated; no hook payload was executed here. |
| BW18-G08 | MB10 | **Fixture commit hooks-off pin** — `tools/bash-witness-study.py:1268-1274` | Removing the explicit hooks-off option from fixture commit passes. Route an isolated commit-hook canary with a stable selftest case name; no hostile hook was installed here. |
| BW18-G09 | MB11 | **Private selftest-root containment** — `tools/bash-witness-study.py:1240-1247` | Creating the child tree in private_root.parent instead of private_root passes. Route a case that observes fixture-tree containment beneath the dedicated outer private root. The child still uses mkdtemp; no host-boundary breach was demonstrated. |
| BW18-G10 | MB12 | **Private selftest-root cleanup anchor** — `tools/bash-witness-study.py:1676-1681` | Cleaning private_root/missing instead of private_root passes. Route a post-return cleanup assertion before namespace teardown. [INFERENCE] The wrong anchor leaves the outer private root until sandbox teardown; this probe did not separately observe that directory after the selftest returned. |

**Calibration limit:** survival here means the owning selftest did not discriminate the changed bytes in this bounded, clean-entry environment. It does not by itself establish a successful malicious configuration/hook attack. In particular, init’s hooks-off option may be redundant for the exercised Git operation, and the misplaced child root still comes from `mkdtemp`. Those remain named discrimination gaps rather than claimed exploits. The private /tmp namespace also removes leaked temporary entries on teardown, so MB12 was not claimed as an observed persistent host leak.
## Unique-anchor and byte-restoration evidence
The pristine source was read from the exact Git object with the following read-only command (exit **0**), not from a moving live worktree:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  git -C /tmp/tameshi-r18w2-MutateBashWitness18-3Yx9zC/fleet/tameshi-shokunin show 01d586ddbc5fcd78659557c4e93a6ee8517b87d1:tools/bash-witness-study.py
```
For each exact `old` string in the manifest below, `original_text.count(old)` returned **1** before editing. The expected one-point bytes were computed as `original_text.replace(old, new, 1)`; the actual detector-time `sha256sum <absolute-instance-source>` matched that expected mutant hash for all twelve. Empty `new` means that one line was deleted. Each mutation and its reverse were applied surgically, and all original bytes were restored before the restored detector batch.
Common pristine **and restored** source SHA-256 (`P`):

```text
8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12
```
| ID | @old count | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | Restored detector |
|---|---:|---|---|---|---|
| MB01 | 1 | P | `f3b408bce0160396bce3608ca335b961f7876c390c65427746d662f08966c74d` | P | exit 0; 43/43 pass |
| MB02 | 1 | P | `83fb7a0480eb59e476253f5e83079fcaf4acec0d17d737e0fa3f7f7bf081dce3` | P | exit 0; 43/43 pass |
| MB03 | 1 | P | `6b8e5b49e41e7eaa8b65816f81d4cdcd05fe51bac9672e94a9570b4bb9921804` | P | exit 0; 43/43 pass |
| MB04 | 1 | P | `77d8750aa80d3a1229a9ac08ab0cf4c407f21c2426e71ecd4c43c14bac153083` | P | exit 0; 43/43 pass |
| MB05 | 1 | P | `d4409801bbbaa97b61af68c4f4d74ca4c0731268159d811e0fd72d5915d40963` | P | exit 0; 43/43 pass |
| MB06 | 1 | P | `2b94a4f766ccd89cff275deb95edada401d7937167a713df67040b8631c9b169` | P | exit 0; 43/43 pass |
| MB07 | 1 | P | `3f3e6407728ef07ebd768df08e3d0f0d58e88e004db3be4ad5e199dadf7de2bc` | P | exit 0; 43/43 pass |
| MB08 | 1 | P | `d301a110cc7198442ac8e5f8254800c66a20562b5e71d11f266d6624df5df1ad` | P | exit 0; 43/43 pass |
| MB09 | 1 | P | `55f920a9e6c7ac347ee5034c8a49b38077d00999070c7b92ffadd917c86b1666` | P | exit 0; 43/43 pass |
| MB10 | 1 | P | `8885eacc71ca47049d0dfbb3e3842b87fad7c8039aa71226158dac235c2ccdff` | P | exit 0; 43/43 pass |
| MB11 | 1 | P | `2ccb234aada833fda0941dbf726e6df6ea3a0a221e035efd93a7dabc5ac506bb` | P | exit 0; 43/43 pass |
| MB12 | 1 | P | `2ab018f560d7ba4b226a722b2c264271778ff6630e9216f73d1d1778397f5d31` | P | exit 0; 43/43 pass |

All 24 pristine/restored source hashes were `P`. The untouched base-clone source also retained `P` in the final `sha256sum` output. All restored stdout and stderr matched their own pristine outputs exactly. No mutation was left applied.
### Exact single-point manifest

```json
[
  {
    "id": "MB01",
    "path": "tools/bash-witness-study.py",
    "line": 336,
    "old_count": 1,
    "old": "           if not name.startswith(\"GIT_\")}",
    "new": "           if True}"
  },
  {
    "id": "MB02",
    "path": "tools/bash-witness-study.py",
    "line": 336,
    "old_count": 1,
    "old": "           if not name.startswith(\"GIT_\")}",
    "new": "           if not name.startswith(\"GIT_DIR\")}"
  },
  {
    "id": "MB03",
    "path": "tools/bash-witness-study.py",
    "line": 336,
    "old_count": 1,
    "old": "           if not name.startswith(\"GIT_\")}",
    "new": "           if name not in (\"GIT_DIR\", \"GIT_WORK_TREE\")}"
  },
  {
    "id": "MB04",
    "path": "tools/bash-witness-study.py",
    "line": 337,
    "old_count": 1,
    "old": "    env[\"GIT_CONFIG_GLOBAL\"] = \"/dev/null\"\n",
    "new": ""
  },
  {
    "id": "MB05",
    "path": "tools/bash-witness-study.py",
    "line": 337,
    "old_count": 1,
    "old": "    env[\"GIT_CONFIG_GLOBAL\"] = \"/dev/null\"",
    "new": "    env[\"GIT_CONFIG_GLOBAL\"] = str(REPO / \".gitconfig\")"
  },
  {
    "id": "MB06",
    "path": "tools/bash-witness-study.py",
    "line": 338,
    "old_count": 1,
    "old": "    env[\"GIT_CONFIG_NOSYSTEM\"] = \"1\"",
    "new": "    env[\"GIT_CONFIG_NOSYSTEM\"] = \"0\""
  },
  {
    "id": "MB07",
    "path": "tools/bash-witness-study.py",
    "line": 338,
    "old_count": 1,
    "old": "    env[\"GIT_CONFIG_NOSYSTEM\"] = \"1\"\n",
    "new": ""
  },
  {
    "id": "MB08",
    "path": "tools/bash-witness-study.py",
    "line": 1259,
    "old_count": 1,
    "old": "                [\"git\", \"-c\", \"core.hooksPath=/dev/null\",\n                 \"-C\", str(repo), \"init\", \"--quiet\"],",
    "new": "                [\"git\",\n                 \"-C\", str(repo), \"init\", \"--quiet\"],"
  },
  {
    "id": "MB09",
    "path": "tools/bash-witness-study.py",
    "line": 1264,
    "old_count": 1,
    "old": "                [\"git\", \"-c\", \"core.hooksPath=/dev/null\",\n                 \"-C\", str(repo), \"add\", \"--\", TARGET_GIT_PATH],",
    "new": "                [\"git\",\n                 \"-C\", str(repo), \"add\", \"--\", TARGET_GIT_PATH],"
  },
  {
    "id": "MB10",
    "path": "tools/bash-witness-study.py",
    "line": 1269,
    "old_count": 1,
    "old": "                [\"git\", \"-c\", \"core.hooksPath=/dev/null\",\n                 \"-C\", str(repo), \"-c\", \"user.name=fixture\",",
    "new": "                [\"git\",\n                 \"-C\", str(repo), \"-c\", \"user.name=fixture\","
  },
  {
    "id": "MB11",
    "path": "tools/bash-witness-study.py",
    "line": 1246,
    "old_count": 1,
    "old": "            prefix=\"bash-witness-selftest.\", dir=private_root))",
    "new": "            prefix=\"bash-witness-selftest.\", dir=private_root.parent))"
  },
  {
    "id": "MB12",
    "path": "tools/bash-witness-study.py",
    "line": 1681,
    "old_count": 1,
    "old": "        shutil.rmtree(private_root, ignore_errors=True)",
    "new": "        shutil.rmtree(private_root / \"missing\", ignore_errors=True)"
  }
]
```
## Captured detector output
The output dictionary below is lossless for all 36 instance runs: pristine/restored phases use `green` for every ID; MB03–MB12 mutated phases also use `green`; MB01 and MB02 mutated phases use their named red output. All stderr values are the empty string. The initial base-clone run also used `green`.

| Output key | stdout SHA-256 | Uses |
|---|---|---|
| green | `316b97139aaa2fafa1ab08c2df6471ba8dec5b4480efa1a9589ae0341e5020be` | 35 |
| MB01-red | `95c0c67ce10e3ebc1cc9d55f873840354571e2e7dfd9a6c08d3b57ef0fc99bd9` | 1 |
| MB02-red | `8f3abf330cc05156ab30ea70f5b12f5ef505e9bddbf01cef176d8d5e14b1dab1` | 1 |

### green

```text
  check GIT_DIR/GIT_WORK_TREE cannot redirect materialization ok
  check GIT_DIR/GIT_WORK_TREE cannot redirect sweep  ok
  check extract_spec picks the census heredoc        ok
  check parse_spec id/desc/literals                  ok
  check runner_pins reads both constants             ok
  check runner_pins refuses a short PIN_BASH with a named error ok
  check unescape maps \n                             ok
  check spec_precheck flags a non-unique literal     ok
  check control log: 14 exercised + 2 expected skips + terminal 16 ok
  check dump lines never count as labels             ok
  check killed-on-witness when a declared case fails ok
  check accidental when no declared case fails       ok
  check declared NONE red is accidental              ok
  check green with full denominator survives         ok
  check no SELFTEST line is inconclusive             ok
  check non-terminal SELFTEST line is inconclusive   ok
  check odd denominator is inconclusive              ok
  check incomplete numbering is inconclusive         ok
  check unexpected skip label is inconclusive        ok
  check green with failing cases is inconclusive     ok
  check runner INCONCLUSIVE is inconclusive          ok
  check duplicate spec id refuses                    ok
  check FAIL without denominator is inconclusive, not a crash ok
  check unknown verdict is inconclusive              ok
  check duplicate case label is inconclusive         ok
  check PASS summary with a bad case is inconclusive ok
  check KILLED with exit 0 is inconclusive           ok
  check usage error exits 64                         ok
  check declared.tsv round-trip keeps NONE rows      ok
  check untampered declared.tsv verifies             ok
  check planted tamper refuses with a named error    ok
  check collect_results recomputes ten survived rows ok
  check duplicate result id refuses                  ok
  check unknown result id refuses                    ok
  check verdict/exit mismatch refuses                ok
  check mutant digest mismatch refuses               ok
  check check CLEAN on a full-manifest fixture       ok
  check missing manifest refuses                     ok
  check pruned manifest is not CLEAN                 ok
  check summary tamper is detected                   ok
  check summary preserves top-level exposed declaration kind ok
  check count recomputes rows and matches summary    ok
  check count refuses summary/raw mismatch           ok
WITNESS_SELFTEST: 43/43 pass
VERDICT: PASS
```

### MB01-red

```text
  check GIT_DIR/GIT_WORK_TREE cannot redirect materialization FAIL
  check GIT_DIR/GIT_WORK_TREE cannot redirect sweep  FAIL
  check extract_spec picks the census heredoc        ok
  check parse_spec id/desc/literals                  ok
  check runner_pins reads both constants             ok
  check runner_pins refuses a short PIN_BASH with a named error ok
  check unescape maps \n                             ok
  check spec_precheck flags a non-unique literal     ok
  check control log: 14 exercised + 2 expected skips + terminal 16 ok
  check dump lines never count as labels             ok
  check killed-on-witness when a declared case fails ok
  check accidental when no declared case fails       ok
  check declared NONE red is accidental              ok
  check green with full denominator survives         ok
  check no SELFTEST line is inconclusive             ok
  check non-terminal SELFTEST line is inconclusive   ok
  check odd denominator is inconclusive              ok
  check incomplete numbering is inconclusive         ok
  check unexpected skip label is inconclusive        ok
  check green with failing cases is inconclusive     ok
  check runner INCONCLUSIVE is inconclusive          ok
  check duplicate spec id refuses                    ok
  check FAIL without denominator is inconclusive, not a crash ok
  check unknown verdict is inconclusive              ok
  check duplicate case label is inconclusive         ok
  check PASS summary with a bad case is inconclusive ok
  check KILLED with exit 0 is inconclusive           ok
  check usage error exits 64                         ok
  check declared.tsv round-trip keeps NONE rows      ok
  check untampered declared.tsv verifies             ok
  check planted tamper refuses with a named error    ok
  check collect_results recomputes ten survived rows ok
  check duplicate result id refuses                  ok
  check unknown result id refuses                    ok
  check verdict/exit mismatch refuses                ok
  check mutant digest mismatch refuses               ok
  check check CLEAN on a full-manifest fixture       ok
  check missing manifest refuses                     ok
  check pruned manifest is not CLEAN                 ok
  check summary tamper is detected                   ok
  check summary preserves top-level exposed declaration kind ok
  check count recomputes rows and matches summary    ok
  check count refuses summary/raw mismatch           ok
WITNESS_SELFTEST: 41/43 pass
VERDICT: FAIL
```

### MB02-red

```text
  check GIT_DIR/GIT_WORK_TREE cannot redirect materialization ok
  check GIT_DIR/GIT_WORK_TREE cannot redirect sweep  FAIL
  check extract_spec picks the census heredoc        ok
  check parse_spec id/desc/literals                  ok
  check runner_pins reads both constants             ok
  check runner_pins refuses a short PIN_BASH with a named error ok
  check unescape maps \n                             ok
  check spec_precheck flags a non-unique literal     ok
  check control log: 14 exercised + 2 expected skips + terminal 16 ok
  check dump lines never count as labels             ok
  check killed-on-witness when a declared case fails ok
  check accidental when no declared case fails       ok
  check declared NONE red is accidental              ok
  check green with full denominator survives         ok
  check no SELFTEST line is inconclusive             ok
  check non-terminal SELFTEST line is inconclusive   ok
  check odd denominator is inconclusive              ok
  check incomplete numbering is inconclusive         ok
  check unexpected skip label is inconclusive        ok
  check green with failing cases is inconclusive     ok
  check runner INCONCLUSIVE is inconclusive          ok
  check duplicate spec id refuses                    ok
  check FAIL without denominator is inconclusive, not a crash ok
  check unknown verdict is inconclusive              ok
  check duplicate case label is inconclusive         ok
  check PASS summary with a bad case is inconclusive ok
  check KILLED with exit 0 is inconclusive           ok
  check usage error exits 64                         ok
  check declared.tsv round-trip keeps NONE rows      ok
  check untampered declared.tsv verifies             ok
  check planted tamper refuses with a named error    ok
  check collect_results recomputes ten survived rows ok
  check duplicate result id refuses                  ok
  check unknown result id refuses                    ok
  check verdict/exit mismatch refuses                ok
  check mutant digest mismatch refuses               ok
  check check CLEAN on a full-manifest fixture       ok
  check missing manifest refuses                     ok
  check pruned manifest is not CLEAN                 ok
  check summary tamper is detected                   ok
  check summary preserves top-level exposed declaration kind ok
  check count recomputes rows and matches summary    ok
  check count refuses summary/raw mismatch           ok
WITNESS_SELFTEST: 42/43 pass
VERDICT: FAIL
```

## Tooling and stop boundary
Existing tools: Python **3.14.8**, Git **2.56.0**, bubblewrap **0.13.1**, GNU timeout/coreutils **9.12**. **No tool installation or update.** No host service change or pacman transaction.
The assigned mutation probe is complete. Only the requested owning selftests and restoration/hash evidence were exercised; no unrelated gate, registry run, alternative runtime, fix, or round adjudication was performed.

partial — owning selftest killed 2/12 mutants; 10 named survivor coverage gaps routed; 12/12 exact-byte restorations and restored 43/43 selftests passed.
