# Round 35 W2 — SentinelScope

Snapshot: 2026-10-23, local time `-0300`. Axes: checkout/scope integrity, byte integrity, and attribution.

## Summary

- **HYGIENE:** 23 of 61 discovered Git worktrees contained ignored CPython `__pycache__` files. They are inside seat-named checkout paths; the final status scan showed only ignored cache directories, not modified tracked files or ordinary untracked files. Table below identifies each checked-out file by exact path, mtime, and SHA-256.
- **BOUND:** the requested `/fast/scratch/hyaku/tameshi-r35-seats/SentinelScope/lane` already existed at `d16f9b5a…`, not dispatch pin `7da6e076…`. The prescribed clone failed without replacing it; the requested target commit is absent from that checkout. Thus the clean-worktree negative applies only to the stale checkout, not the requested pin.
- **BOUND / unattributed external activity:** two Tameshi-specific files exist in the parent `/home/vgpnk/Projects/shokunin/.ufo/` tree, outside `tameshi-shokunin`. Their timestamps and hashes are recorded below; local evidence does not attribute their creation to a W2 seat.
- No installs, code probes, behavioral tests, or checkout edits were performed. No `jj` command was run.

## HYGIENE — bytecode written inside checkouts

**Exploit path:** a seat runs Python from a checkout; CPython writes `.pyc` under the checkout's `__pycache__`. `git status --ignored=matching --porcelain --untracked-files=all` marks these as `!!`, so ordinary status omits them even though the lane was required to remain read-only.

**Evidence:** at `2026-10-23T18:48:26-0300`, a read-only scan over all 61 `.git` roots under `/fast/scratch/hyaku/tameshi-r35-seats/` returned `REPO_COUNT=61 DIRTY_COUNT=23 STATUS_FAILURES=0 SCAN_RC=0`. Every nonempty status was solely an ignored `__pycache__/` directory. At `18:47:49-0300`, the cache inventory and `sha256sum` scan returned `CACHE_SCAN_RC=0`; the following rows are the cache files inside Git worktrees (work-directory caches outside worktrees are excluded). All paths are beneath the corresponding seat-named directory; seat attribution is path-based, not process-identity evidence.

| Seat/path root | Exact file | mtime (`-0300`) | SHA-256 |
|---|---|---|---|
| ScoutHarnessRegion | `/fast/scratch/hyaku/tameshi-r35-seats/ScoutHarnessRegion/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:33:09.757176171 | `6cd02f00e5721d34a804f68c4bb2d5230e7532fb6656e5baf84e9fee74003acf` |
| ScoutHarnessRegion | `/fast/scratch/hyaku/tameshi-r35-seats/ScoutHarnessRegion/lane/tools/__pycache__/tally-audit-v2.cpython-314.pyc` | 2026-10-23 18:33:09.769113763 | `587a5243860b5df7db30759c2d0ddfb636bc4c2da9af4e78555ac2b1f5e91adb` |
| SentinelSandbox | `/fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/pinned/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:32:48.538619769 | `2017bec75cefb4a7c31e8124057d09ad007af5241d848f112324d9853c303182` |
| AttackPreambleSeed | `/fast/scratch/hyaku/tameshi-r35-seats/AttackPreambleSeed/lane-pin/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:35:45.622925320 | `bf1119dc8d1aadd72266a09e6bc77aa1005e1977883c9bdf5d3139fb8ef5476e` |
| AttackPreambleSeed | `/fast/scratch/hyaku/tameshi-r35-seats/AttackPreambleSeed/lane-pin/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:32:08.958209862 | `2797efbe482c81c0de68cf644e3b28ccf0c344a8ad24bd8475cc45e848ef5d24` |
| AttackQuotedHash | `/fast/scratch/hyaku/tameshi-r35-seats/AttackQuotedHash/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:04:20.040414608 | `6b275a3382ef039a6de1760d9fcdaf035b397a12bf92e87ad82ddbbd00b09178` |
| AttackArithHash (stale checkout) | `/fast/scratch/hyaku/tameshi-r35-seats/AttackArithHash/lane.attempt1-stale/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:05:14.820390470 | `7750eca69f04f846d5a4de3a0cbe4a0093057d571e8a848dc75920c13e857b80` |
| AttackArithHash | `/fast/scratch/hyaku/tameshi-r35-seats/AttackArithHash/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:38:19.391172495 | `64b77f088627836fb806beb2e8817e7ac34626c60377650136b97e0d1d48f233` |
| AttackArithHash | `/fast/scratch/hyaku/tameshi-r35-seats/AttackArithHash/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:31:51.833622533 | `e67dc80b126a84b1db923bc986392062d9ba282fc2d9b74f7f5e216168652435` |
| AttackNameAssembly | `/fast/scratch/hyaku/tameshi-r35-seats/AttackNameAssembly/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:40:32.005927312 | `10f489e925387cf865a588399946dd3c4a0f151c5acbdff923bb1153e6d48e2e` |
| AttackNameAssembly | `/fast/scratch/hyaku/tameshi-r35-seats/AttackNameAssembly/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:32:03.166294331 | `c1d73c1296acb90d2d0b0d599450358b04f4ee031f1724618e6da56943ed53fe` |
| AttackQuotedCase | `/fast/scratch/hyaku/tameshi-r35-seats/AttackQuotedCase/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:34:45.633582967 | `02412ecffe81517dd816ecbcad16b184b11c8bf62b85f9521eda7276f599dbeb` |
| AttackQuotedCase | `/fast/scratch/hyaku/tameshi-r35-seats/AttackQuotedCase/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:45:06.799347460 | `31c025538d7fe9ff3c74cf4c06223e975220bce511011fa336782d42a5bb6cef` |
| AttackRootKeys | `/fast/scratch/hyaku/tameshi-r35-seats/AttackRootKeys/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:31:50.635455236 | `f2db86e934ac1cfdfc6aa18c7e793c4d790f15d97f5110c3d8eaf51a80c3ff0d` |
| AttackRootKeys | `/fast/scratch/hyaku/tameshi-r35-seats/AttackRootKeys/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:31:50.630862605 | `ce4e462deb85931d7364dff82c3b98d55a81c3d6984c25c37fa49749d50ecfba` |
| AttackTransientExit | `/fast/scratch/hyaku/tameshi-r35-seats/AttackTransientExit/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:32:36.347612625 | `7330b347825660c8ce84a59cf4de3a334715dbe571078738d1086bb7917392d7` |
| AttackStderrScope | `/fast/scratch/hyaku/tameshi-r35-seats/AttackStderrScope/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:33:19.993415503 | `fd44853488100b860e1f8d1f9c565b5326a232b62ce7de68f2a7c852ff1f8d64` |
| AttackHelperScope | `/fast/scratch/hyaku/tameshi-r35-seats/AttackHelperScope/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:38:52.306196944 | `ff1421e424b71194be3d18df745cf71f061f8072ddb9abad038a80208805fadd` |
| AttackTailHarness | `/fast/scratch/hyaku/tameshi-r35-seats/AttackTailHarness/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:34:01.315665584 | `8c10e88e093588e798c2a41c11a6e6c68885147eb84d46a58defe7f0c03ac67b` |
| AttackTailHarness | `/fast/scratch/hyaku/tameshi-r35-seats/AttackTailHarness/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:32:17.578901621 | `7a0a8596d89cae0652078e19003821f8690186d2d85d1079ee669821f61083ee` |
| SimplifyCodeView | `/fast/scratch/hyaku/tameshi-r35-seats/SimplifyCodeView/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:37:27.963172977 | `be86005abb83f4f8caa04daa1b5eb0f27d29c943a7990a405a963fdfcf4bab99` |
| RevengerEnvKeys | `/fast/scratch/hyaku/tameshi-r35-seats/RevengerEnvKeys/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:04:57.697808076 | `b25a1dbda37f0321b603591ce52114ab76293c16d4eb357407313c5a483ef574` |
| ReviewPanelDistinct | `/fast/scratch/hyaku/tameshi-r35-seats/ReviewPanelDistinct/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:03:52.223975036 | `b5ad256796b50d5f7089994e1ab380e0ebc42f0049941ea6aebedd24e25ed7ed` |
| ReviewSealedGate | `/fast/scratch/hyaku/tameshi-r35-seats/ReviewSealedGate/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:04:19.938469802 | `f6ba7e9445e3d8fab1ee05ee7f133da108b6f2d274eef4f635e6666d58c356ae` |
| ConnectorCommentBlind | `/fast/scratch/hyaku/tameshi-r35-seats/ConnectorCommentBlind/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:40:11.719776949 | `aa5c8d2b394965e349b7c0b82249fe356c17d792c72aac4027077fa065737b72` |
| ConnectorCommentBlind | `/fast/scratch/hyaku/tameshi-r35-seats/ConnectorCommentBlind/lane/tools/__pycache__/bash-witness-study.cpython-314.pyc` | 2026-10-23 18:41:49.915447676 | `46ad78f5fc043f75eae6405a472ac0de738f65efd731c353a5872dee07023363` |
| ConnectorCommentBlind | `/fast/scratch/hyaku/tameshi-r35-seats/ConnectorCommentBlind/lane/tools/__pycache__/mte-interop.cpython-314.pyc` | 2026-10-23 18:41:49.938878489 | `a3202fc6c8e62a8780abf85893bf9b6a659970684f20417831bac9676dccec1d` |
| RevengerConfigSpace | `/fast/scratch/hyaku/tameshi-r35-seats/RevengerConfigSpace/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:39:46.416418119 | `02eafd0082e71b64ccea01908dde2ed495c8683e4c03e76bcdb3dc9ce900b67d` |
| RevengerConfigSpace | `/fast/scratch/hyaku/tameshi-r35-seats/RevengerConfigSpace/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:39:46.410182684 | `e37da7bd42f7fc0c1d60b49acc352084f03ce7a61c4469739a6f73515a523a41` |
| ReviewOracle | `/fast/scratch/hyaku/tameshi-r35-seats/ReviewOracle/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:41:50.403135655 | `527f9abb3e262670038fa9e6760705b85eb38465406cfe39f6c6b1e8a7807b06` |
| SimplifyConfigs | `/fast/scratch/hyaku/tameshi-r35-seats/SimplifyConfigs/lane/.ufo/evidence/round-35/c1/__pycache__/c1-measure.cpython-314.pyc` | 2026-10-23 18:31:53.233746190 | `68b5c10b7e0886611f3b1d0444e16ad06c250558b42bb27f555f466d3df799d5` |
| ReviewCodeView | `/fast/scratch/hyaku/tameshi-r35-seats/ReviewCodeView/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:05:05.523478026 | `6af2e35e004b76f70400ab16df85146102a6147ba1e2c79d36686edfba519655` |
| RevengerVerdictLine | `/fast/scratch/hyaku/tameshi-r35-seats/RevengerVerdictLine/lane/tools/__pycache__/tally-audit-v3.cpython-314.pyc` | 2026-10-23 18:37:35.897477501 | `4ccc0fbc2f1107b8f2fc28ada6b750813c51b5b4a61dea96e681f0db32c56497` |

**Impact:** these are ignored Python bytecode writes inside supposedly read-only worktrees. No code or panel data change is evidenced by the status scan, but ignored files can persist and contaminate later runs. **Smallest remediation:** future Python invocations should set `PYTHONDONTWRITEBYTECODE=1` or `PYTHONPYCACHEPREFIX` to a per-seat scratch directory outside each checkout. Do not delete these artifacts as part of this audit.

## BOUND — wrong pre-existing lane prevented pin-specific inspection

**Exploit/path:** the prescribed setup attempted to clone into a nonempty `lane/`; Git refused. The chained `checkout` did not run. The existing checkout is stale for the assignment pin.

Exact attempted command:
```sh
mkdir -p /fast/scratch/hyaku/tameshi-r35-seats/SentinelScope && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r35-seats/SentinelScope/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelScope/lane checkout -q --detach 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```
Result: `fatal: destination path '/fast/scratch/hyaku/tameshi-r35-seats/SentinelScope/lane' already exists and is not an empty directory.`; shell `SETUP_EXIT=128`.

**Evidence:** `/fast/scratch/hyaku/tameshi-r35-seats/SentinelScope/lane` mtime `2026-10-23 18:02:43.670194831 -0300`; `.git/HEAD` mtime `18:02:43.836740479 -0300`, SHA-256 `b73a8a8b9db3c6d99a2b726f6c879a5e548122e5ae350f7dd35ab33c949272f2`; `.git/index` SHA-256 `1f1a9d4220c3669e5ea1274110bf825cc7b323a407230dfad60874768437a061`. `git -C .../lane rev-parse HEAD` returned `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` (exit 0), and `git status --porcelain --untracked-files=all` was empty (exit 0). The requested commit exists in the source checkout: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e '7da6e076c2e25936a3b60dde2a4080d8f05b7e5b^{commit}'` exit 0; `git show -s` reports it at `2026-10-23T18:26:38-03:00`. The same `cat-file` query in the existing lane failed with exit 128 (`Not a valid object name`); `git diff --stat d16f9b5a… 7da6e076…` there also failed exit 128 (`bad object`).

**Impact:** the assigned dispatch-tip working tree was not available for inspection. The clean status above proves only that the pre-existing `d16f9b5a` checkout was clean before generated caches are considered; it does not establish a clean `7da6e076` working tree. **Smallest remediation:** preserve the existing checkout and rerun the lane-specific audit from a fresh, empty scratch destination pinned to `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.

## BOUND — parent-level Tameshi artifacts outside the lane repository

A read-only stat/hash check found these files outside `tameshi-shokunin`, modified during the observed wave window. Their presence is confirmed; local file metadata does not identify the writer, so this is **not** attributed to a W2 seat.

| Exact path | mtime (`-0300`) | SHA-256 |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-35.md` | 2026-10-23 18:14:04.853944414 | `0354e9c3d4e51a09e6ab36f7fef210b0ecd1e8dec961c67a1f86a98a43a5bca6` |
| `/home/vgpnk/Projects/shokunin/.ufo/state/tameshi.report-baseline` | 2026-10-23 18:14:04.855944412 | `ed9951ef052a6e0fa4703bc182b8aabc9f96877046c1e9bd9f09f80771115b88` |

`stat` and `sha256sum` both returned exit 0. A wider parent-tree timestamp scan also surfaced concurrent sibling-project and parent SCM metadata activity; its path/time output is `artifact://840`. Those observations are not evidence of authorship by a round-35 seat. **Impact:** writer attribution is unresolved for parent-level metadata. **Smallest remediation:** keep seat outputs in their designated tameshi report paths and retain dispatcher provenance for any parent-level state/prompt writes.

## Commands and bounded negative

The only mutating Git command in my transcript was the provided `git clone` attempt above; it failed with exit 128 before cloning. Because the shell used `&&`, the chained `git checkout` was not executed. No mutating `jj` command ran. Subsequent Git commands were read-only queries (`status`, `rev-parse`, `cat-file`, `show`, `diff`). No checkout file was written by this audit; the only intended write is this report.

**Could not find:** in the final 61-worktree status scan, all commands returned exit 0 and all 23 nonempty results were only `!! __pycache__/` directories. No tracked modifications or ordinary untracked source/data files were reported in those worktrees. This negative is bounded to the filesystem snapshot at `2026-10-23T18:48:26-0300` and does not cover the unavailable `7da6e076` SentinelScope lane.