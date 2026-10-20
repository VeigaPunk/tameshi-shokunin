# C04 — sibling GIT_* prior art for contract E

Axes: contract-E fitness (drop every inherited `GIT_*`, no-op when none are set), falsifier strength (an object-store canary, not a HEAD watch), route-only exposure (name sibling holes, do not edit them). Operability stays a monitored route, not a patch.

No tools installed.

## Pins

`git --no-optional-locks -C <repo> rev-parse HEAD` and `status --porcelain` (both exit 0):

| lane | HEAD | porcelain |
|---|---|---|
| tsukuroi | `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33` | 0 |
| kumitate | `1770305fae20826b39905a8251ddeca6b4957ac4` | 0 |
| mado | `e629f731172b8238caffe50f152217ce56535fb4` | 0 |
| mori | `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` | 31, all under `.ufo/waves/round-17/`; `tools/` not listed |
| tameshi (gap only) | `183f87b899e6cae46be98d251cbc87fb5118f6ca` | 2 untracked (`.ufo/evidence/round-18/`, `.ufo/waves/round-18/`) |

Citations below are `git show <HEAD>:<path>` line numbers. Mori tool bytes match that HEAD.

R17-GIT-ENV is still the open item: `corpus/lessons/round-17-verifier-spotcheck.md:433-436` (`tools/bash-witness-study.py` has no full `GIT_*` scrub; pin `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`).

## What was searched

Wrapper `/tmp/tameshi-r18w1-C04-search-all.py` ran `git --no-optional-locks -C <repo> grep -n -I -F` at each HEAD. Script exit 0. `git grep` exit 1 means no hit.

Whole-tree hit counts:

| token | tsukuroi | kumitate | mado | mori |
|---|---:|---:|---:|---:|
| `GIT_DIR` | 7 (wave prose only) | 0 | 22 (wave prose only) | 181 |
| `GIT_CEILING_DIRECTORIES` | 2 (wave prose) | 0 | 0 | 12 |
| `env -i` | 1 (wave prose) | 0 | 11 (wave prose / fixtures, not `tools/`) | 147 |
| `env -u GIT` | 0 | 0 | 1 (wave prose) | 123 |

`tools/` + `scripts/` literal `GIT_DIR`: tsukuroi 0, kumitate 0, mado 0, mori 24. Tsukuroi's scrub does not spell `GIT_DIR`; it uses `startswith("GIT_")`. A `GIT_DIR`-only grep marks tsukuroi and kumitate clean and is wrong for both.

Tool surfaces at those HEADs: tsukuroi 12 `tools/*.py` + 2 shell; kumitate 7 `scripts/*.mjs`; mado 3 `tools/*`; mori 13 `tools/*`.

## Pattern to adopt (one move)

Port tsukuroi's prefix drop onto both subprocesses in `tools/bash-witness-study.py`, and lock it with an object-store canary that a three-name unset cannot pass.

Canonical helper, `tsukuroi-shokunin/tools/_revision.py:62-72`:

```python
def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    return env
```

Every `git` subprocess in the 12 tsukuroi Python tools uses that filter (inlined or imported):

- `tools/_revision.py:63` (imported by `check-appended-notices.py:22`, used at `:119`; `check-root-dac-correction.py:244`)
- `check-boot-chain.py:778`, `check-freshness-r17.py:326`, `check-locator-clarification.py:448` and `:577`, `check-recheck-commands.py:605`, `check-revision-binding.py:102`, `check-seat-scope.py:162`, `check-section-citations.py:406` and `:568`, `check-source-scope-correction.py:355`, `measure-update-recheck.py:438` and `:485`

`git --no-optional-locks -C tsukuroi grep -F git HEAD -- tools/boot-chain-audit.sh` exit 1 (no `git`). `tools/tsukuroi-census.sh` exit 0 with 3 lines, all the substring inside "digit"; no git invocation.

Same rule already lives on tameshi's runner, not on the witness tool. `tools/mutate-and-run.sh:257-267` builds `env -u` from every `GIT_[A-Za-z0-9_]*` name `env` prints. `bash-witness-study.py` does not:

- `tools/bash-witness-study.py:337-340` `git -C <kagi> show --end-of-options <rev>:corpus/surface-census.sh` passes no `env`.
- `:116-117` `SCRUB_ENV` is five non-git names. `:572-576` `sweep_env()` copies `os.environ` and pops only those. `:604-606` passes that dict to `bash tools/mutate-and-run.sh`.

Contract E's "all inherited `GIT_*`" is the comprehension, not the re-pins. Do not copy `LC_ALL=C` (it rewrites git stderr). `GIT_OPTIONAL_LOCKS=0` / `GIT_PAGER=cat` are a separate read-only policy; leave them off this change. Do not merge a second dict over the filtered env the way `check-root-dac-correction.py:244` does (`{**clean_env(), **identity}`), which can put `GIT_*` back.

Apply the filter in `sweep_env()` and pass the same dict as `env=` on the `git show` at `:337`. Keep the existing `SCRUB_ENV` pops. Record the new tool digest in the round-18 dispositions manifest; do not edit the round-13 pin `49e9e5e2…`.

### Canary that makes the filter load-bearing

Tsukuroi's own selftest calls `clean_env()` (`_revision.py:175`, `:182`, `:229`) and never assigns `os.environ["GIT_DIR"]` or `GIT_OBJECT_DIRECTORY`. [INFERENCE] Deleting the `startswith` filter would leave `REVISION_SELFTEST` green. That is the R17-GUARD-COVERAGE shape: the helper exists, the removal is not red.

Mori's poisoned arm is the right place to inject, and the wrong assertion. `tools/mori-misroot-sweep.py:561-575` exports only `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` and checks which paths `status` reports. `tools/mori-census.sh:3175` wraps the tool in `env -i`, which strips a hostile parent before the tool runs, so the harness cannot see a missing inner scrub.

`/tmp/tameshi-r18w1-C04-experiment.py` exit 0, scratch `/tmp/tameshi-r18w1-C04-gitenv-8wckxcsr`. Two empty commits, parent `GIT_*` stripped, then re-added per arm:

| arm | command result |
|---|---|
| control `git -C intended cat-file -t <canary-sha>` | exit 128 `could not get object info` |
| `GIT_DIR=<canary>/.git git -C intended rev-parse HEAD` | exit 0, canary sha `1fec644c…` (T1) |
| `GIT_OBJECT_DIRECTORY=<canary>/.git/objects git -C intended cat-file -t <canary-sha>` | exit 0 `commit` (T2) |
| unset only `GIT_DIR` `GIT_WORK_TREE` `GIT_INDEX_FILE`, leave object dir + alternates | `cat-file` still exit 0 `commit` (T3); `rev-parse HEAD` still the intended sha `44f31ca9…` (T3b) |
| tsukuroi filter, then the same hostile dict | `rev-parse` intended sha; `cat-file` exit 128 (T4, T4b) |
| `node` `spawnSync('git', ['-C', intended, 'rev-parse','HEAD'])` with no `env`, parent `GIT_DIR=<canary>/.git` | canary sha (T5 inherit) |
| same spawn with `env: {...process.env, GIT_CONFIG_GLOBAL:'/dev/null', GIT_CONFIG_SYSTEM:'/dev/null'}` | canary sha (T5 spread) |

Contradiction to spell, not average: `mori-census.sh:2105-2107` and `mori-round17-seat-regressions.py:1516-1518` say unsetting the trio stops an inherited value overriding `git -C`. T3b agrees for `rev-parse HEAD`. T3 disagrees for object reads. A canary that only watches decoy HEAD stays green while `git show <rev>:<path>` is reading the other store. `bash-witness-study.py:337` is that show.

Selftest arm, both repos under `/tmp`, never a `GIT_*` pointed at a lane checkout: build an intended repo whose `git show <rev>:corpus/surface-census.sh` bytes are known, and a decoy whose object store does not contain that commit. Run the show with only `GIT_OBJECT_DIRECTORY=<decoy>/.git/objects` exported into the tool process (no outer `env -i`). Pass iff stdout is the intended blob. Removing the filter fails the arm (T2). A census-style trio unset also fails it (T3). Add a second arm that exports `GIT_DIR` and `GIT_WORK_TREE` at the decoy so P11's names are locked directly; that arm alone would accept the trio unset.

## Do not adopt

- Kumitate `scripts/round-gate.mjs:704-710` looks like a scrub and is the opposite. `GIT_ENV = { ...process.env, GIT_CONFIG_GLOBAL, GIT_CONFIG_SYSTEM, author/committer keys }` keeps `GIT_DIR`. T5 spread. Production `git()` at `:211-214` passes no `env` at all. Whole-tree `GIT_DIR` count is 0; the hole is the missing argument, not a string.
- Mori census `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` (`mori-census.sh:2112`, repeated on every `$GIT_BIN` call; a scan of the blob found no git invocation outside that wrapper, comments, or the stub path). T3.
- Mori misroot's eight-name pop (`mori-misroot-sweep.py:69-87`, includes `GIT_OBJECT_DIRECTORY` and `GIT_ALTERNATE_OBJECT_DIRECTORIES`, deliberately keeps `GIT_CEILING_DIRECTORIES` at `:66-68`). Runtime is closed for those eight names. The selftest does not lock `GIT_OBJECT_DIRECTORY`. A fixed denylist is how `GIT_CONFIG_COUNT` stays out of the list; the prefix filter is the version that matches "all".
- `env -i` as the test harness (`mori-census.sh:3175`, `mori-silence-cases.sh:438`). Right for a hermetic fixture git, wrong as the proof the tool scrubs.
- Mori allowlists that already drop inherited `GIT_*` by never copying `os.environ`: `mori-round13-regressions.py:1218-1236`, `mori-round14-regressions.py:384-412`, `mori-round17-jj-regressions.py:166-177` (`sanitized_env` copies `PATH` `LANG` `LC_ALL` `TZ` `TERM` only; the later `pop` of four `GIT_*` keys is dead). An allowlist on the witness tool would also drop `HOME` and can change `git show` via global config. The prefix drop does not, when no `GIT_*` is set.

## Still exposed (route only)

1. `kumitate-shokunin/scripts/round-gate.mjs:211-214` production `spawnSync` inherits. Selftest `:704-718` spreads `process.env`. `fxGit` at `:717` is the fixture writer (`init`, `commit`, `push` at `:735-739`).
2. `kumitate-shokunin/scripts/cite-check.mjs:1137-1138` same inherit. Selftest writer `:1674-1677` (`spawnSync` with `cwd`, no `env`: `init`, `add`, `commit`). `:1866` `rev-parse` the same way. `sources-check.mjs`, `surface-probe.mjs`, `claims-check.mjs`, `kimi-census.mjs`, `proxy-check.mjs` do not spawn git.
3. `mado-shokunin/tools/mado-verify.sh:144` `tmo()` is `timeout 5` only. Live git, no scrub, `git grep -F 'tmo git -C'` exit 0: `:3774`, `:3813`, `:3823`, `:3827`, `:3829`, `:3830`, `:3848`, `:3858`, `:3886` (`git show`). `tools/` has zero `GIT_DIR`, `env -u GIT`, and `env -i` (those strings are wave reports, including `SentinelToolSafety.md:80-86` which already asked for the unset). Selftest `env PATH=...` at `:751` is not `env -i`; isolation there is a PATH stub (`:689-742`), not a scrub. `mado-action-plan.py:525-529` passes `PATH` only, and only for its self-invoke; it does not run git. `mado-tripwire.py:2021` re-invokes the scanner with inherited env and does not run git.
4. `mori-shokunin/tools/mori-census.sh:2112` trio only, plus `env -i` at `:3175` masking it.
5. `mori-shokunin/tools/mori-round15-regressions.py:782-791` copies `os.environ`, sets `GIT_OPTIONAL_LOCKS`, runs `git -C` the mori repo.
6. `mori-shokunin/tools/mori-round16-regressions.py:697-703` copies `os.environ`, runs `git -C` the mori repo.
7. `mori-shokunin/tools/mori-round17-seat-regressions.py:1520-1529` pops the trio, then `git` with `cwd=<mori repo>`.

Not routed: `mori-journal-window.py:749`, `mori-round16-context-check.py:373`, `mori-round17-context-check.py:581`, `mori-seat-terminal.py:551` copy or inherit the environment for a Python/journalctl re-invoke, not for git. `mori-silence-cases.sh:438` and the three allowlists above are closed for inherited `GIT_DIR`.

## Risks

- Prefix drop also removes `GIT_CEILING_DIRECTORIES`. `git -C <kagi>` with an explicit repo does not need it. A caller who relied on ceiling to stop discovery walks loses that bound. Do not re-set ceiling inside the witness tool.
- `sweep_env()` feeds `mutate-and-run.sh`, whose own `git_clean` already prefix-scrubs git. The parent drop is still required: contract E says the subprocess environment itself, and the runner has non-`git_clean` children. With no `GIT_*` set, the extra pop does not change argv, stdout, or the registered exit.
- The object arm must demand the intended blob (or a 128 on a decoy-only sha), not an unchanged decoy HEAD. T3b is the false pass.
- Canary repos stay under `/tmp`. A `GIT_DIR` aimed at a lane checkout is the round-17 write.

## Verification

Exercised: the `rev-parse` / `status` pins, the `git grep -F` counts, the mado `tmo git -C` grep (exit 0), and `/tmp/tameshi-r18w1-C04-experiment.py` (exit 0, lines above). Not executed: sibling selftests, `bash-witness-study.py`, tsukuroi `REVISION_SELFTEST`. The "deleting the filter stays green" sentence is inference from `_revision.py:157-242` containing no hostile `GIT_*` assignment.

Verdict: built
