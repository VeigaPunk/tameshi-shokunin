done — assigned frozen-C2 mutation probe completed: 39 single-point mutants; 36 killed, 1 survived, 2 inconclusive/unviable. All pristine and restored detector suites were green; exact counter bytes restored after every mutant.

# MT2C2Counter — round 21, wave 1

## Scope, axes, and limits

- **Calibration:** distinguish a changed counter verdict from a crash, a baseline failure, or the counter's deliberately changing `counter_sha256` field. Report the survivor and unexercised paths without declaring the contract complete.
- **Operability:** committed, replayable synthetic inputs; bounded executions of the real frozen counter CLI; real private-clone/bubblewrap execution of a synthetic tool selftest.
- Frozen base: `33d03b716d3edcf1d8656d46d6df61801d232c52`. The counter and contract were copied from this commit with `git show`, not copied from a moving working tree.
- Scratch: `/tmp/tameshi-r21-MT2C2Counter-4X7Pcw`.
- Private fixture clone: `/tmp/tameshi-r21-MT2C2Counter-4X7Pcw/fleet/tameshi-shokunin`.
- Last synthetic fixture commit: `aa0b227d493cb69ad23b6e89ef6b2bde0e87d5fe`; its ancestors contain the 47 individually committed fixture inputs. Commit identity was `seat <seat@local>`.
- No production patch, integration, round judgment, fleet mutation, or subagent dispatch. The only lane write is this requested report. **Do not integrate the synthetic fixture commits.** Sibling repository links and all actual frozen surfaces were read-only.
- This tests the **counter**, not the env-diff implementation. The receipt tuples, S999 source row, entry, and tool are explicitly synthetic test data. A synthetic 9/9 result is not evidence that any of the nine real surfaces was executed under the F5 profiles.

## Detector and fixtures

`prepare.py` makes the required `git clone -q --no-hardlinks`, checks out the frozen base detached, links sibling lane directories read-only, then commits synthetic receipt/entry/SOURCES/tool variants. The valid receipt has all nine frozen identities and actual blob hashes read through `git show`; all seven initial profile tuples are `(0, sha256(empty), sha256(empty))`. It declares `normalization: none`, `classification: invariant`, and `sensitive_to: []`.

Other positive controls exercise nondeterminism (`clean_repeat` stdout hash differs) and sensitivity (`host` exits 7 and `tz` stderr differs). Negative commits independently vary pins, records, normalization presence, every required profile, tuple types/digests, classification, tool presence/exit, entry/header/source status, receipt schema/JSON, and the counting gates. The synthetic tool asserts `--selftest`, prints `synthetic fixture selftest: pass`, and exits either 0 or 7; the failing variant intentionally retains the same stdout text so the counter must use the exit status.

For each mutant the same named fixture set ran on **pristine → mutated → restored** bytes. Every set included `valid-invariant`. Each invocation had a 20-second outer deadline; no timeout occurred. Up to four fixture invocations ran concurrently within an immutable-byte phase; mutations themselves were sequential because they shared one scratch counter path. The frozen counter's own selftest subprocess retained its original 900-second timeout.

The fixed detector expects each fixture's declared CLI exit and, where specified, its rejection reason. Its suite exit is 0 only if those expectations hold and ordinary counter invocations produce JSON. A **kill** additionally requires a real counter exit-code difference, not merely a missing finding or changed hash. A malformed-input crash with the same rejecting exit is **inconclusive/unviable**, not killed. No expectation is derived from mutated implementation output.

There were **49 pristine control invocations** (47 committed cases plus invalid-revision and usage cases), all matching expectations. The mutation triplets added **276 counter invocations**, for **325 total**. All 39 pristine detector suites and all 39 restored detector suites exited 0.

### Exact top-level commands and observed exits

All commands ran with cwd `/tmp/tameshi-r21-MT2C2Counter-4X7Pcw`, except the prerequisite version query. Each command below exited **0**. Probe-driver exit 0 means results were recorded; it does not mean every mutant was killed.

```sh
bwrap --version && python3 --version && git --version
python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/prepare.py
python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/probe.py --mode controls
python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/probe.py --mode mutants --only M01,M02,M03,M04,M05,M06,M07,M08,M09,M10,M11,M12,M13
python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/probe.py --mode mutants --only M14,M15,M16,M17,M18,M19,M20,M21,M22,M23,M24,M25,M26
python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/probe.py --mode mutants --only M27,M28,M29,M30,M31,M32,M33,M34,M35,M36,M37,M38,M39
sha256sum /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/counter/pristine.py /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/counter/probe.py /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/counter/c2-contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c2-count.py
```

Observed control output:

```text
{"cases": 49, "detector_exit": 0, "failures": []}
```

The preparation subprocess argv, exits, stdout, and stderr—including every clone, checkout, add, commit, and frozen-blob read—are recorded in `/tmp/tameshi-r21-MT2C2Counter-4X7Pcw/prepare-commands.json`. Every counter argv and observed exit is in its per-mutant JSON or `controls.json`.

All preparation/detector subprocesses used the invoking environment with every `GIT_*` key removed, then private `HOME`, `TMPDIR`, and `XDG_CONFIG_HOME` under scratch, plus `PYTHONDONTWRITEBYTECODE=1`. Fixture commits used per-command `core.hooksPath` pointing to the private empty-hooks directory. The counter's temporary selftest clones therefore also lived under this seat's private TMPDIR. No host Git configuration or hook was edited.

Representative actual counter argv, with the detector environment described above:

```sh
# Valid synthetic receipt: exit 0.
/usr/bin/python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/counter/probe.py --repo /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/fleet/tameshi-shokunin --rev 53ed129929ec822b0354d95ec17f1ca10c5c8081 --json
# Wrong repo pin: pristine exit 1, M01 exit 0, restored exit 1.
/usr/bin/python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/counter/probe.py --repo /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/fleet/tameshi-shokunin --rev 15ad8f390d34182c80778bca5bf7245724cc4ded --json
# Diagnostic invocation must remain noncounting: exit 1 in all M39 phases.
/usr/bin/python3 /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/counter/probe.py --repo /tmp/tameshi-r21-MT2C2Counter-4X7Pcw/fleet/tameshi-shokunin --rev 167dd0496400a9df3188ef85e4c765d24b32a3f3 --json --skip-selftest
```

Two pin fault fixtures preserve the exact frozen contract and use a **private per-process PATH shim**:

- `pin-unreadable`: only the exact frozen `tameshi-runner` blob read returns 128.
- `frozen-blob-drift`: only the exact frozen `js-kimi-census` blob read appends `\nSYNTHETIC-DRIFT\n`. Its committed receipt pin deliberately matches these altered bytes, isolating `frozen-blob-drift` from `pin-blob-mismatch`.

Every other Git argv delegates to the real Git executable. These scripts live in scratch `shims/unreadable/git` and `shims/drift/git`; they are not globally activated. Neither actual frozen blob nor any sibling repo was changed.

## Mutant table

Lines refer to the frozen counter. Each replacement occurs at exactly one source location; complete old/new literals are in `specs.json` and each `mutants/Mxx.json`. `P/M/R` is the **counter exit** on pristine/mutated/restored bytes for the named witness, not the detector suite exit. For multiple witnesses listed in one row, the triplet applies to each.

| ID | Line | Single-point defect | Witness fixture(s) | P/M/R | Verdict |
|---|---:|---|---|---|---|
| M01 | 49 | Omit `repo` from pin comparison loop | bad-pin-repo | 1/0/1 | killed |
| M02 | 49 | Omit `rev` from pin comparison loop | bad-pin-rev | 1/0/1 | killed |
| M03 | 49 | Omit `path` from pin comparison loop | bad-pin-path | 1/0/1 | killed |
| M04 | 59 | Disable receipt blob-hash mismatch check | bad-pin-blob | 1/0/1 | killed |
| M05 | 54 | Do not record unreadable frozen blob | pin-unreadable | 1/0/1 | killed |
| M06 | 58 | Do not record frozen blob drift | frozen-blob-drift | 1/0/1 | killed |
| M07 | 46 | Treat missing surface record as valid | missing-record, missing-receipt, bad-json | 1/0/1 | killed |
| M08 | 61 | Do not require declared normalization string | missing-normalization | 1/0/1 | killed |
| M09 | 66 | Substitute a control tuple for an absent profile | missing-profile-host, -clean, -clean_repeat, -tz, -locale, -home, -columns | 1/0/1 | killed |
| M10 | 36 | Accept bool as integer exit | tuple-bool | 1/0/1 | killed |
| M11 | 36 | Drop integer-exit type requirement | tuple-exit-float, tuple-exit-string | 1/0/1 | killed |
| M12 | 38 | Skip stdout digest hex validation | tuple-stdout-hex | 1/0/1 | killed |
| M13 | 38 | Skip stderr digest hex validation | tuple-stderr-hex | 1/0/1 | killed |
| M14 | 74 | Ignore required nondeterministic label | bad-nondeterministic-class | 1/0/1 | killed |
| M15 | 79 | Ignore required invariant label | bad-invariant-class | 1/0/1 | killed |
| M16 | 79 | Ignore invariant `sensitive_to` emptiness | bad-invariant-sensitive | 1/0/1 | killed |
| M17 | 81 | Ignore required env-sensitive label | bad-sensitive-class | 1/0/1 | killed |
| M18 | 81 | Ignore exact differing-profile list | bad-sensitive-list | 1/0/1 | killed |
| M19 | 73 | Reverse clean/repeat inequality | valid-invariant, valid-nondeterministic, valid-sensitive | 0/1/0 | killed |
| M20 | 77 | Reverse differing-tuple predicate | valid-invariant, valid-sensitive | 0/1/0 | killed |
| M21 | 88 | Report absent tool as exit 0 | tool-missing | 1/0/1 | killed |
| M22 | 171 | Accept any non-null selftest exit | tool-fails | 1/0/1 | killed |
| M23 | 171 | Let `--skip-selftest` satisfy `ok_st` | skip-selftest | 1/0/1 | killed |
| M24 | 113 | Admit a missing knowledge entry | entry-missing | 1/0/1 | killed |
| M25 | 117 | Admit an entry with no source header | source-no-header, source-header-line16 | 1/0/1 | killed |
| M26 | 125 | Treat queued source as mined | source-queued | 1/0/1 | killed |
| M27 | 125 | Accept any mined row, not the cited ID | source-unreferenced | 1/0/1 | killed |
| M28 | 114 | Search beyond the first 15 entry lines | source-header-line16 | 1/0/1 | killed |
| M29 | 152 | Ignore receipt schema | wrong-schema | 1/0/1 | killed |
| M30 | 173 | Require only some classified surfaces | bad-pin-repo | 1/0/1 | killed |
| M31 | 173 | Omit selftest from final exit gate | tool-fails, skip-selftest | 1/0/1 | killed |
| M32 | 173 | Omit entry from final exit gate | source-queued | 1/0/1 | killed |
| M33 | 173 | Map counting failure to exit 0 | missing-receipt | 1/0/1 | killed |
| M34 | 173 | Map counting success to exit 1 | valid-invariant | 0/1/0 | killed |
| M35 | 143 | Map unresolved revision to exit 1, not 2 | invalid-rev | 2/1/2 | killed |
| M36 | 138 | Map usage failure to exit 2, not 64 | usage | 64/2/64 | killed |
| M37 | 36 | Remove stdout string-type guard | tuple-stdout-type | 1/1/1, mutant crashes | inconclusive/unviable |
| M38 | 36 | Remove stderr string-type guard | tuple-stderr-type | 1/1/1, mutant crashes | inconclusive/unviable |
| M39 | 171 | Remove explicit `not a.skip_selftest` conjunct | skip-selftest | 1/1/1 | survived |

For M01–M38, detector suite exits were **0/1/0**. For M39 they were **0/0/0**. M37/M38's red detector result is not counted as a killed mutant because neither changed the rejecting CLI exit and both failed to emit normal JSON.

### Actual output excerpts

The positive pristine control emitted `classified: 9`, `total: 9`, `f5_entry: true`, `f5_entry_detail: S999`, and `tool_selftest: {exit: 0, present: true, summary: "synthetic fixture selftest: pass"}`.

For M06's same committed fault fixture:

```text
# pristine exit 1
C2: classified=8/9 tool_selftest=pass f5_entry=True rev=a63bcab669ce2e077f21c5dc40499182a88cd548
# mutated exit 0
C2: classified=9/9 tool_selftest=pass f5_entry=True rev=a63bcab669ce2e077f21c5dc40499182a88cd548
# restored exit 1 (recorded in mutants/M06.json)
```

M37's mutated stderr ends:

```text
  File "/tmp/tameshi-r21-MT2C2Counter-4X7Pcw/counter/probe.py", line 38, in tuple_of
    if not HEX.match(o) or not HEX.match(s):
TypeError: expected string or bytes-like object, got 'int'
```

M38 has the same call site with `TypeError: expected string or bytes-like object, got 'NoneType'`. Their pristine and restored controls instead emit the normal `profile-host-missing` finding and exit 1.

### Survivor

**M39 survives.** The removed expression is:

```python
# pristine
ok_st = (not a.skip_selftest) and st.get("exit") == 0
# mutant
ok_st = st.get("exit") == 0
```

For the skip fixture, both versions still emit `tool_selftest: {"skipped": true}` and exit 1; for the valid fixture both exit 0. [INFERENCE] Under the present public CLI dataflow, the explicit conjunct is redundant because the skipped `st` dictionary has no `exit`, so `st.get("exit") == 0` remains false. This is a bounded survival observation, not permission to alter the noncounting contract or remove the guard. M23 and M31 demonstrate that unsafe skip acceptance does change the verdict and is detected.

## Guard coverage gaps and disagreements

This is a fixture/behavior inventory, **not instrumented whole-program branch coverage**. The following paths or obligations have no dedicated triggering fixture in this probe:

| Untested item | Why the current fixtures do not establish it |
|---|---|
| `tool_selftest` `TimeoutExpired` result, lines 101–103 | Every synthetic tool completes immediately. The 900-second inner-timeout branch was not forced. The 20-second detector timeout was never reached. |
| Selftest clone/checkout failure handling, lines 92–93 | All selftest repos/revisions resolve and clone successfully. Invalid-rev is rejected earlier at line 143; it does not exercise these `check=True` failure paths. |
| Receipt-root `AttributeError` recovery, lines 150–155 | `bad-json` exercises JSON parsing failure, not a valid JSON list/scalar root. |
| Filtering a non-dict surface element at line 153 | Missing-record removes a row; all remaining surface elements are dicts. No fixture places a scalar in the surfaces list. |
| Counter's own hostile `GIT_*` scrub | The detector removes these keys before invoking the counter, so deletion of `env()`'s filter is not challenged by an injected hostile variable here. |
| Git-object-only behavior versus a deliberately contradictory dirty worktree | All receipt/entry/SOURCES variants are committed and read by revision. No uncommitted decoy was used as an opposing witness. |
| Successful tool with empty/blank-only stdout | Every present synthetic tool prints one nonblank line. Summary extraction's empty-output branch was not forced. |

The stdout/stderr type guards **do have** malformed-value fixtures, but M37/M38 remain inconclusive rather than proving a verdict-changing kill. No claim of complete mutation coverage is made.

Four explicit boundary controls passed with the pristine counter:

| Fixture | Commit | Observed result and scope |
|---|---|---|
| normalization-not-none | `7d6bdc1c567f4054e9a571d406bd6978e0709255` | exit 0, 9/9. A declared arbitrary normalization string is accepted. Frozen contract tuple prose permits declared normalization; the shared profile protocol says normalization `none`. This records that discrepancy without changing either. |
| invariant-sensitive-null | `4d2579a3e36b65fdea1ad7d7587333e889d69b5b` | exit 0, 9/9. Code explicitly accepts null as well as `[]`, whereas the frozen classification prose names `[]`. |
| source-old-opened | `5260150271d1ba3faaaead6f2af656530ed2f167` | exit 0, 9/9, f5_entry true. S999's `opened` cell is `2000-01-01`. The counter checks cited/mined status but does not establish the round's separate opened-this-round obligation. |
| nondeterministic-sensitive-wrong | `aa0b227d493cb69ad23b6e89ef6b2bde0e87d5fe` | exit 0, 9/9. With unequal clean/repeat tuples, an arbitrary `sensitive_to` list is ignored. The frozen nondeterministic rule constrains the label only; this is not called a contract violation. |

These are existing predicate limits, not newly introduced defects. In particular, this counter cannot authenticate that synthetic hashes came from executed profiles or that a source was actually opened; independent surface evidence and source review remain separate obligations. No contract change was made or proposed as part of the mutation probe.

A bounded reference search over `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools` and `.ufo/evidence/round-21`, pattern `c2-count\.py|def check_surface|rule-nondeterministic`, found the counter, contract counting command, and before-recorded command; it found no separate counter fixture harness in those searched directories. This is not a repository-wide claim about other agents' scratch tests.

## Hashes and exact restoration

Common **before and after SHA-256 for every mutant**:

```text
9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2
```

Every per-mutant JSON records `before_sha256`, `mutated_sha256`, `restored_sha256`, and `restoration_exact: true`, plus the restored detector run. The final `sha256sum` independently printed this same value for the pristine scratch file, restored scratch file, and untouched lane counter. The copied contract remained:

```text
5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd
```

Mutated-byte SHA-256 values:

```text
M01 7ae2b5c051c7839569100caf37e697f0b6d696cf0d655b4fe4e286811ab5873f
M02 4363763b44477abf83f65c671616f5db8bb632d5b9d93753e335bedb03838fa1
M03 5d5cf1b66a812c69b35ce8ad49a4e74236f9472d396bd72535a5b92730e1161d
M04 504ca212380255e585f403bde59ada6d9d2e835dbf329cc2ab0555d8e0409675
M05 013e41602d0e427f185877c8a63d362ca659143779c8b6a93222b122e9c1c6dc
M06 aed76d018cb3df7a2cf777a722c6baf37762fe2e5fd3630d6773beba5026aae1
M07 7d04b5f48ddc2af93a9eeef0d45d925f4428fcda24c64b065d50130ac904e785
M08 1bed6289f2a5893676f95c3f418fa2540db9a82eef89a8cea97e7d6ec77344fe
M09 4100719ce4540be8c5ed280e095bb92b52330dfb7947dcf8882a7437fb6ff8f8
M10 ac9ddc2da0eecd232dd7e08ac2729287d694c1ecf404e6a2b2d7136a7dded557
M11 4af7764c89f1f6af06c57c589d4f25aa10b6c2016733bf9dce78889f4d22469b
M12 bc1f732c507194286c2ae9b2362066168e8c641c9dc21f8c69adcb8329de8798
M13 efef0f92626e7062b7d9362de3e9db733b3e8b1531b517e9f7ed6966bc53ec16
M14 244095cfd83f0c45c4d1aa64a3e8ba79550a8fad711022469659f5969a73c849
M15 049a1647d3e2bc8ee677a0e1778fd47d895a740ff68af7b9448423f85abd4705
M16 31b981e2cbda5d13ed3296b1f8a594fa60e16db4d5c41f8e27d5239c49bd96cc
M17 deaef9fa9089eefccf1fda0f514a5408ceb4a75f762623a59d428826058b03d8
M18 01a852154917967c9ffa03a1f2f1cd7785178c7b5b91f6907c5c80031075db34
M19 54f2dbd1a44a937782f65530b5edb8f96d02c36539c414b0b7675a72cab241ee
M20 2e84f74bd099e9b4d2954d856df61566a2bb7421f94a295682282499f29c80cc
M21 58a5618ca72088850db393cc764599f6402e38d98343e9915af04c3cc6cd8e6d
M22 a13e817dc32eb951f2af7df8d75ac2757ef182da801e38447c63bda653ecf3bd
M23 1686dbc54df48f84eb38a8f10e0be30b940f874b45b175ae33e95e2a59c8517b
M24 e90cf6be96fb956c3af740ac37f83d305f8e2aafaed8f3734bdc675ce7818fb4
M25 a9681ca9336fa5f9f98f0f437854080128c22a47dc93addcdfe4c72d622e2abe
M26 8db3bfc42eb6f126c655623486a54f97276bfcc4bdd3ddbdd36ae2d36328c4c7
M27 50c7250ca2871bb73a1ce77d43db694ba790bffe81aba6d022acabbc355d29a1
M28 03609cb16311660a3f087d6570d3d1a703a6f1a02b0a5000ce75d0cb9999ef88
M29 2ab8c43a2d5da56cfc9736e2e3308982f6e24cc0bb9036f51c590e868086c153
M30 560a52f663e6128009b63197f25744add6b6fc7bd01c56c9b6613dbcf4eacd3d
M31 d9764e76fb8bbc2d44d5807768589db37a32bec0b321748b2631f270f40b209b
M32 d52155b962a5db1ce46d6ac1565ed3b7651b16d94b0acef7577a2cb1bd649e9d
M33 7c8b2a0075294d81dbd588b553bf44d0510046ac2c2dbcace680f26b554ace6f
M34 6a2b8b86e58964af8825abd1e04b81c07e10ff078082a4a924452936cc02d142
M35 d947fadaa39970e3444f85eb4ea18c49b81c85428ccff6ac0a21d3050a130959
M36 0e64b2e322e19e748bba3c2e855d75f45e18fbab469082657214ce866adfabc7
M37 af27386b0ea7c47d4f19b70d3a96eb79e5f43c75845e83d1aaf2cbcc485b6533
M38 84807f01a357ce7014175e00a73b3d4fb68e17a04a6116feb6d00a4b9051a0d5
M39 c3f8bf0a14815ce2fb3bb549648f34b07e0561ea4fe0948f6ede58c24f277f6d
```

## Evidence index and tooling

All following paths are under `/tmp/tameshi-r21-MT2C2Counter-4X7Pcw/`:

- `prepare.py`, `prepare-commands.json`: exact fixture construction and recorded subprocess output.
- `manifest.json`: frozen base, clone path, common hashes, last synthetic commit.
- `fixtures.json`: all 47 fixture names, exact commit revisions, expected exits/findings, sidecar selection, and argv additions.
- `probe.py`, `specs.json`: the bounded detector and complete one-location mutations.
- `controls.json`: all 49 original control results.
- `mutants/M01.json` through `mutants/M39.json`: old/new code, all three phases' argv/exits/semantic results, exact hashes/restoration evidence.
- `mutants/M01.py` through `mutants/M39.py`: the isolated mutant bytes for inspection, not integration.
- `logs/controls/` and `logs/Mxx-{pristine,mutated,restored}/`: actual stdout/stderr for every invocation.
- `counter/probe.py`: restored exact frozen counter; `counter/pristine.py` and `counter/c2-contract.json`: unmodified reference bytes.

Installed tools used: bubblewrap **0.13.1**, Python **3.14.8**, Git **2.56.0**. **No install/update transactions** were performed. Only the assigned counter/fixture probes were run; no lane build, broader test battery, calibration monitor, or claim-admission check is asserted.
