# MutateDisposition18 — scoped mutation findings
## Scope and axes
- Seat: `TameshiR18.MutateDisposition18`; read revision: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
- Axes: **depth** (G2/G3 shared-anchor semantics and G3/G5 object guards), **calibration** (failure-backed kills versus named survivors), with **operability** monitored through pristine/restored controls. This is a mutation-probe result, not a round judgment.
- Twelve independent single-line mutants; the production tool and its selftest expectations were not fixed or relaxed. No delegation, other runtime, live-lane git writes, sibling edits, installations, or upgrades. The only live-lane write is this report.
- Scratch root `W=/tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd`; detached clone `C=/tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd/fleet/tameshi-shokunin`. Each independent variant is `$C/.mutation-probes/MutateDisposition18/MXX/tools/evidence-disposition.py`. All variants were restored to exact pristine bytes.
## Commands and isolation
- Setup used `git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$C"`, then `git -C "$C" checkout -q --detach 01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; both exited **0**. The subprocess environment removed **every** inherited `GIT_*` key and disabled global/system Git configuration; no lane-path Git environment values were set. Read-only `git -C "$C" rev-parse HEAD` returned the pinned revision. Scratch fleet siblings are symlinks to the read-only live siblings.
- Sandbox readiness probe exited **0**, printing `sandbox-ready /tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd/fleet/tameshi-shokunin`. Every behavioral detector used the same envelope below, launched with cwd `$C`, all inherited `GIT_*` keys removed, and a **150-second** outer timeout. `env -i` further empties the sandbox environment; only the shown variables are supplied. The fleet and the whole host are read-only; only `$W` and ephemeral namespace `/tmp` are writable; network is unshared.
```sh
W=/tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd
C="$W/fleet/tameshi-shokunin"
# For each M01..M12, run this identical command in pristine, mutated, restored phases:
M="$C/.mutation-probes/MutateDisposition18/$ID/tools/evidence-disposition.py"
/usr/bin/bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$W" "$W" --unshare-net --die-with-parent --chdir "$C" \
  env -i PATH="$PATH" HOME="$W/home" TMPDIR="$W/tmp" \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  /usr/bin/python3 "$M" --selftest
```
- Four bounded detector processes ran concurrently at a time; every batch was awaited to completion, with no background jobs. Selftest-created git/jj writes stayed inside the sandbox. Its `fixtures kept at /tmp/...` FAIL suffixes refer to ephemeral namespace paths, not retained host fixtures.
- The unmodified clone tool also ran once through the same envelope: exit **0**, `SELFTEST: PASS (63/63)`. Then every independent variant had its own pristine, mutant, and restored run: **37 completed selftest invocations** in total (1 + 12 + 12 + 12), no timeout or setup/process failure. All stderr captures were empty.
## Mutation registration
Before mutation, each original line was checked against the recorded line number, and `pristine.count(old.encode()) == 1` was asserted for every mutant. All **12 @old counts were exactly 1**. The variants initially had the same whole-file SHA-256 as the pinned clone tool. Surgical edits changed only the listed line, without changing fixture expectations. Locations below are `tools/evidence-disposition.py` at the pinned revision.
| Mutant | Path:line | @old count | Old line | Mutated line |
|---|---|---:|---|---|
| M01 — ignore-configured-lane-branch | `tools/evidence-disposition.py:465` | 1 | `branch = proc.stdout.decode("utf-8", "replace").strip() if proc.returncode == 0 else ""` | `branch = ""` |
| M02 — attached-branch-hardcoded-master | `tools/evidence-disposition.py:472` | 1 | `branch = ref[len(prefix):]` | `branch = "master"` |
| M03 — remove-jj-unbound-refusal | `tools/evidence-disposition.py:492` | 1 | `if os.path.lexists(str(lane / ".jj")):` | `if False and os.path.lexists(str(lane / ".jj")):` |
| M04 — remove-detached-containment | `tools/evidence-disposition.py:520` | 1 | `if not containing_refs:` | `if False and not containing_refs:` |
| M05 — containment-requires-exact-ref-tip | `tools/evidence-disposition.py:507` | 1 | `"--contains",` | `"--points-at",` |
| M06 — detached-anchor-uses-containing-tip | `tools/evidence-disposition.py:525` | 1 | `return "HEAD", commit` | `return containing_refs[0], _commit_of(lane, containing_refs[0])` |
| M07 — g2-waiver-uses-head-not-shared-anchor | `tools/evidence-disposition.py:609` | 1 | `anchor_entry = tree_entry(lane, anchor_commit, path)` | `anchor_entry = tree_entry(lane, "HEAD", path)` |
| M08 — g3-ancestry-uses-head-not-shared-anchor | `tools/evidence-disposition.py:539` | 1 | `["merge-base", "--is-ancestor", "--end-of-options", rev, anchor_commit],` | `["merge-base", "--is-ancestor", "--end-of-options", rev, "HEAD"],` |
| M09 — g3-accepts-peeled-tag-object | `tools/evidence-disposition.py:532` | 1 | `if proc.returncode != 0 or resolved != rev:` | `if proc.returncode != 0:` |
| M10 — g5-accepts-symlink-blob-mode | `tools/evidence-disposition.py:645` | 1 | `if kind != "blob" or mode not in TREE_MODES:` | `if kind != "blob":` |
| M11 — g5-refuses-executable-regular-mode | `tools/evidence-disposition.py:549` | 1 | `TREE_MODES = ("100644", "100755")` | `TREE_MODES = ("100644",)` |
| M12 — configured-branch-hardcoded-master | `tools/evidence-disposition.py:477` | 1 | `branch_ref = "refs/heads/" + branch` | `branch_ref = "refs/heads/master"` |

## Observed detector results
Pristine and restored runs each printed exactly `SELFTEST: PASS (63/63)` and exited **0** for all twelve variants. The exit triplet is **pristine / mutant / restored**. A baseline failure would be inconclusive; none occurred. KILLED means a nonzero owning-selftest exit with named behavioral case failures, not a syntax/import/setup failure.
| Mutant | Exits | Verdict | Expected owning detector / coverage challenge | Actual failing cases |
|---|---|---|---|---|
| M01 | 0 / 1 / 0 | **KILLED** | `v2-jj-prebookmark-branch-tip`, `v2-jj-branch-tip` | `v2-jj-prebookmark-branch-tip`, `v2-jj-branch-tip` |
| M02 | 0 / 0 / 0 | **SURVIVED** | `non-master-attached-branch fixture (coverage challenge)` | none; `SELFTEST: PASS (63/63)` |
| M03 | 0 / 1 / 0 | **KILLED** | `v2-jj-without-lane-branch` | `v2-jj-without-lane-branch` |
| M04 | 0 / 1 / 0 | **KILLED** | `v2-detached-no-published-ref` | `v2-detached-no-published-ref` |
| M05 | 0 / 1 / 0 | **KILLED** | `v2-registry-clone-detached-anchor` | `v2-registry-clone-detached-anchor` |
| M06 | 0 / 1 / 0 | **KILLED** | `v2-registry-clone-detached-anchor` | `v2-registry-clone-detached-anchor` |
| M07 | 0 / 1 / 0 | **KILLED** | `v2-jj-prebookmark-branch-tip` | `v2-jj-prebookmark-branch-tip` |
| M08 | 0 / 1 / 0 | **KILLED** | `v2-jj-branch-tip` | `v2-jj-branch-tip` |
| M09 | 0 / 1 / 0 | **KILLED** | `v2-historical-tag-object` | `v2-historical-tag-object` |
| M10 | 0 / 1 / 0 | **KILLED** | `v2-historical-symlink-mode` | `v2-historical-symlink-mode` |
| M11 | 0 / 0 / 0 | **SURVIVED** | `historical 100755 regular-blob acceptance fixture (coverage challenge)` | none; `SELFTEST: PASS (63/63)` |
| M12 | 0 / 0 / 0 | **SURVIVED** | `non-master lane.branch fixture (coverage challenge)` | none; `SELFTEST: PASS (63/63)` |

### Actual failure output
These are the complete failing `SELFTEST_CASE` output lines, not predicted failures.
```text
M01
SELFTEST_CASE v2-jj-prebookmark-branch-tip FAIL (ids=['historical_input_unavailable'] expects=['historical_input_uncommitted'])
SELFTEST_CASE v2-jj-branch-tip FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
M03
SELFTEST_CASE v2-jj-without-lane-branch FAIL (ids=['historical_input_unneeded'] expects=['historical_input_unavailable'])
M04
SELFTEST_CASE v2-detached-no-published-ref FAIL (exit=0 expects=2; ids=[] expects=['historical_input_unavailable']; payload exit=0; status='clean' expects='could_not_evaluate')
M05
SELFTEST_CASE v2-registry-clone-detached-anchor FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
M06
SELFTEST_CASE v2-registry-clone-detached-anchor FAIL (exit=2 expects=0; ids=['historical_input_uncommitted'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
M07
SELFTEST_CASE v2-jj-prebookmark-branch-tip FAIL (exit=0 expects=2; ids=[] expects=['historical_input_uncommitted']; payload exit=0; status='clean' expects='could_not_evaluate')
M08
SELFTEST_CASE v2-jj-branch-tip FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
M09
SELFTEST_CASE v2-historical-tag-object FAIL (exit=0 expects=2; ids=[] expects=['historical_input_unavailable']; payload exit=0; status='clean' expects='could_not_evaluate')
M10
SELFTEST_CASE v2-historical-symlink-mode FAIL (exit=0 expects=2; ids=[] expects=['historical_input_unavailable']; payload exit=0; status='clean' expects='could_not_evaluate')
```
- M01 summary: **2/63 failed**; M03–M10 summaries: **1/63 failed each**; M02, M11, M12 summaries: **63/63 passed**. Overall: **9 KILLED / 3 SURVIVED / 0 INCONCLUSIVE**. The jj refusal mutant M03 was killed by the wrong stable finding ID (`historical_input_unneeded` instead of `historical_input_unavailable`), despite still exiting 2; this is an ID-sensitive kill, not a false claim that the mutant accepted that particular fixture.
## Named survivors and routing
All three are **OPEN coverage findings**, routed by this report to **TameshiR18 → tameshi evidence-disposition selftest/fixture owner**. No guard/contract change is proposed or applied. The survivor result is observed; suggested extra fixture outcomes are marked [INFERENCE] because they were not executed.
| Gap ID | Survivor and evidence | Route / missing discriminating scenario |
|---|---|---|
| **D18-ATTACHED-NONMASTER** | M02 at `tools/evidence-disposition.py:472` hardcodes the attached local branch to `master`; owning selftest still exits 0, 63/63. | G2/G3 attached-branch fixture coverage. [INFERENCE] Add a valid attached `main` or `topic/...` branch with no `lane.branch` and no `master` ref; correct resolution should use the attached branch. This mutant would instead select an unavailable or wrong master anchor. |
| **D18-G5-EXECUTABLE** | M11 at `tools/evidence-disposition.py:549` removes allowed mode `100755`; owning selftest still exits 0, 63/63. The contract explicitly permits `100644/100755` (`:58`, `:637`). | G5 regular executable-blob positive coverage. [INFERENCE] A clean historical pin whose tree entry is a regular `100755` blob should pass, while M11 would reject it as `historical_input_unavailable`. Do not widen accepted modes to accommodate the mutant. |
| **D18-CONFIG-NONMASTER** | M12 at `tools/evidence-disposition.py:477` ignores the configured branch value by always using `refs/heads/master`; owning selftest still exits 0, 63/63. | G2/G3 explicit `lane.branch` fixture coverage. [INFERENCE] Bind `lane.branch=topic/...` with its authoritative tip distinct from HEAD/master (or with master absent); correct G2/G3 resolution must use that named local branch. |

Supporting fixture sweep executed with the target-search tool: pattern `chmod|100755|100644|lane.branch|init.defaultBranch|refs/heads/|git.*init` over `tools/evidence-disposition.py:1693-3101`. Existing explicit JJ fixture initialization/configuration uses `master` (`:2164-2167`), and its bookmark/tip checks use `master` (`:2197`, `:2219-2240`); detached clone and no-ref fixtures explicitly initialize `master` (`:2258`, `:2282`). The sweep returned no `chmod`, `100755`, `100644`, or `init.defaultBranch` match in the selftest region. This supports the named branch-name/mode coverage findings without claiming a new production-tool defect.
## Before/after hashes and restoration
Common pristine and restored SHA-256 **A** = `66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44` (**119851 bytes**). For every variant: pristine detector before/after hash = A; mutant detector before/after hash = the table value; restored detector before/after hash = A. Exact byte equality against the original was asserted, not just matching hashes. The clone's original `tools/evidence-disposition.py` also remained byte-identical to pristine.
| Mutant | Mutant SHA-256 (before = after detector) | Restored SHA-256 | Restored detector |
|---|---|---|---|
| M01 | `0ec5fc045ca8d914d19ce08d6d2fd2c6801f9b1a54844046a3b870d2edcc84ad` | A; exact bytes equal | exit 0; 63/63 |
| M02 | `c7af4921667b7ea528bf27de5bbc2bd6c015e43d4cbfbbbe796f968549bcd511` | A; exact bytes equal | exit 0; 63/63 |
| M03 | `ce2d7dbc74d1c75a3022469dfc1f95ebc3bae2af3923896b93f78bf29a380e11` | A; exact bytes equal | exit 0; 63/63 |
| M04 | `5f353df4e27881e070c8ab016bc322f2a74a4447d4917ed818ede7a725346879` | A; exact bytes equal | exit 0; 63/63 |
| M05 | `e79cef9f8365b25c6411c86fc38fc7919e4a8cb250b451d53c7a29c96c1f9390` | A; exact bytes equal | exit 0; 63/63 |
| M06 | `f6126ab6a14598a1e5fca6bf9bd2cdea8fd24009582fb2491ddb46c890f99432` | A; exact bytes equal | exit 0; 63/63 |
| M07 | `cc6e8de62da54bab3d2c6f6ee8a77ca9ac382801d78aa513f9224d0bb09e07e5` | A; exact bytes equal | exit 0; 63/63 |
| M08 | `d1e048575925cfee11d1fbfc58a7f00bff26625c9282d9878a4f381017648981` | A; exact bytes equal | exit 0; 63/63 |
| M09 | `5a2e51cb4733721af3d10d2c23404e240127ce097840af3539eb7a021e9021b3` | A; exact bytes equal | exit 0; 63/63 |
| M10 | `045f5a8235e7db6dce7456d9ea41509dab1febe7373bd4db6c0d788ea599829d` | A; exact bytes equal | exit 0; 63/63 |
| M11 | `420e85115bcb99503db316894c336e7128bc3218bb75c457ddf8f437c662a922` | A; exact bytes equal | exit 0; 63/63 |
| M12 | `e5f366c142b8ea9d9b7f4349a3c3e3926d28404d86551f6326e4882a767536c5` | A; exact bytes equal | exit 0; 63/63 |

## Receipts and limits
- Retained scratch receipts: `/tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd/MXX-pristine.receipt.json`, `MXX-mutated.receipt.json`, `MXX-restored.receipt.json`; each contains the full exact argv/environment-expanded command string, cwd, exit, elapsed seconds, complete stdout/stderr, and detector before/after hashes. The clone-tool control is `/tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd/pristine.receipt.json`.
- Consolidated copies: `/tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd/receipts.json` and `/tmp/tameshi-r18w2-MutateDisposition18-a8ns9tjd/mutations.json` (the latter records @old counts, exact old/new strings, locations, mutant hashes, verdicts, and restoration equality). Those paths are scratch evidence, not durable lane artifacts; the substantive commands, hashes, outputs and routes are embedded above in this lane report.
- Executed scope is the owning `--selftest` only, on pristine/mutated/restored bytes. No registry/full-lane gate, production receipt rerun, round judgment, integration, shipping, or replacement runtime was performed. Survivor-specific proposed fixture outcomes remain [INFERENCE]. Tool installations/updates: **none**.

partial — 9/12 mutants KILLED; 3 SURVIVED and are named/routed coverage gaps; all 12 variants restored to exact pristine bytes and 63/63 passing selftests.
