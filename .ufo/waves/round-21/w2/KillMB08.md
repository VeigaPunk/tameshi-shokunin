# done — MB08 genuinely discriminated (constructed-argv contract only)

## Scope and axes

- **Operability:** replay only frozen C1 mutant MB08 and identify whether its intended discriminator actually fails.
- **Calibration:** distinguish a checked subprocess-argument contract from demonstrated malicious-hook execution; retain exact controls, outputs, and restoration evidence.
- **Isolation:** production source remained read-only; all Git-writing/selftest activity ran in private clones, with sibling symlinks read-only inside bubblewrap. No subagents, other mutation probes, full batteries, installs, or integrations.

Implementation revision: `790abd2129f153c13b471e381d454186edbde65e`. The owning source read from production was byte-identical to `git show 790abd2129f153c13b471e381d454186edbde65e:tools/bash-witness-study.py` (that command exited 0).

## Mutant and expected detector

Frozen definition: `.ufo/evidence/round-21/c1-mutants.json:42-47`; exact old-anchor occurrence count **1**. The mutation removes only `-c core.hooksPath=/dev/null` from fixture `git init` at `tools/bash-witness-study.py:1259-1263`:

```diff
-                ["git", "-c", "core.hooksPath=/dev/null",
+                ["git",
                  "-C", str(repo), "init", "--quiet"],
```

The intended detector is `fixture init pins hooks off`, implemented at `tools/bash-witness-study.py:1298-1311`. It wraps `subprocess.run` with `unittest.mock.patch.object(..., wraps=subprocess.run)`, executes `fixture_repo("command-pin-fixture", ...)`, selects the actual recorded command for each operation, and requires exactly one command containing the adjacent argument pair `["-c", "core.hooksPath=/dev/null"]`. Real subprocess calls still run; this is not source hashing, source grepping, a stubbed successful subprocess, or an import/syntax check.

All implementation line references above and below refer to the stated revision; the production file matched its pinned blob digest.

## Required frozen replay: command, exit, and stderr

Executed exactly this argv, with inherited `GIT_*` removed and outer `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`:

```text
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB08 --jobs 1 --json
```

Exit **0**. Full, unmodified JSON stdout: `.ufo/waves/round-21/w2/mutations/MB08.json`.

Exact stderr (also saved as `mutations/MB08.stderr.txt`):

```text
C1 MB08 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Frozen receipt:

- Pristine control: exit **0**, no timeout, `VERDICT: PASS`.
- MB08: anchor count **1**, exit **1**, no timeout, `VERDICT: FAIL`.
- Intended failing case: `check fixture init pins hooks off                  FAIL`.
- Counts: killed **1**, survived **0**, inconclusive **0**.
- Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Spec SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.
- JSON stdout SHA-256: `b78a8494a516c1f33bf5479fef3a601a7fe151181d1483b63467ed4866544fb5`.
- Ruler stderr SHA-256: `64830b77319829ff5f6270dc435fdd5582335dfdbbd8c2d0c5fe6dd23695e1b7`.

The ruler's `fail_lines` also contains `check FAIL without denominator is inconclusive, not a crash ok` in both pristine and mutant outputs. That is a **passing case name containing FAIL**, not another failed assertion: the ruler extracts lines by substring at `.ufo/evidence/round-21/c1-survivors.py:53`. Full-output reproduction below resolves that ambiguity.

## Same-detector pristine / mutated / restored lifecycle

Because the frozen ruler deletes its private clones (`c1-survivors.py:131,139-140`), an additional private, item-only lifecycle retained complete raw selftest output and explicitly restored exact source bytes.

Private root: `/tmp/tameshi-r21-KillMB08-wzq0f4e4`.

Setup commands (each exit **0**, empty stdout/stderr):

```text
git -c core.hooksPath=/dev/null clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB08-wzq0f4e4/fleet/tameshi-shokunin
git -c core.hooksPath=/dev/null -C /tmp/tameshi-r21-KillMB08-wzq0f4e4/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Sibling symlinks were created beside that private clone. All three phases used this **same** detector argv, matching the frozen ruler's selftest envelope (`c1-survivors.py:38-57`), with a 900-second timeout:

```text
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind /tmp/tameshi-r21-KillMB08-wzq0f4e4 /tmp/tameshi-r21-KillMB08-wzq0f4e4 --unshare-net --die-with-parent --chdir /tmp/tameshi-r21-KillMB08-wzq0f4e4/fleet/tameshi-shokunin env -i PATH=<inherited PATH, recorded verbatim in MB08.lifecycle.json> HOME=/tmp/tameshi-r21-KillMB08-wzq0f4e4/home TMPDIR=/tmp/tameshi-r21-KillMB08-wzq0f4e4/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 /tmp/tameshi-r21-KillMB08-wzq0f4e4/fleet/tameshi-shokunin/tools/bash-witness-study.py selftest
```

| Phase | Exit | Actual terminal output | Actual failed cases |
|---|---:|---|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | None |
| Exact frozen MB08 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | Only `fixture init pins hooks off` |
| Exact-byte restored | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | None |

Every phase had empty stderr. Mutant `fixture add pins hooks off` and `fixture commit pins hooks off` both remained `ok`; the rest of the selftest completed. The source's check bookkeeping and terminal exit are at `bash-witness-study.py:1231-1238,1711-1716`. Thus the red result is neither setup/import/syntax failure nor an unrelated assertion.

The mutated file was confirmed byte-identical to applying the frozen old/new replacement once. Pristine and restored stdout matched byte-for-byte, and their SHA-256 matched the frozen ruler's pristine control. Mutated stdout also matched the frozen ruler's mutant hash.

### Hashes and restoration evidence

| Bytes | SHA-256 |
|---|---|
| Pinned blob / pristine source | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Exact MB08 source | `60673aaf0cb793fde6dc7ee3c256edd8954981e3c98c4f0d4ec9e0711f0d2053` |
| Restored private source | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Production source before and after lifecycle | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Pristine and restored stdout | `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1` |
| Mutated stdout | `1f6fea873f906b9b49bba6ba0c8039bed20d79e29853c548b5c750d54c3e7909` |
| All three stderr streams (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Exact private restored-bytes comparison: **true**. Production before/after byte equality: **true**. The scratch source is left restored. No production tools, contracts, ledgers, corpus, index, or refs were changed by this probe.

Full supplemental evidence, relative to the repository:

- `.ufo/waves/round-21/w2/mutations/MB08.lifecycle.json` — exact setup/detector argv, phase exits, complete output, timings, hashes, and byte-equality receipts.
- `.ufo/waves/round-21/w2/mutations/MB08.pristine.stdout.txt` and `.stderr.txt`.
- `.ufo/waves/round-21/w2/mutations/MB08.mutated.stdout.txt` and `.stderr.txt`.
- `.ufo/waves/round-21/w2/mutations/MB08.restored.stdout.txt` and `.stderr.txt`.

## Agreement, limitation, and final verdict

**Agree:** frozen C1 marks MB08 `KILLED`, and its intended `fixture init pins hooks off` case genuinely discriminates the missing **constructed argv pin**. Pristine is green, the unique anchor was exercised, only the intended assertion fails, and restoration returns to the identical green output.

**Calibration limit:** `bash-witness-study.py:1298-1299` explicitly describes these as command-pin contracts, not evidence of a reachable init/add hook in the scrubbed fixture environment. `safe_env` comes from `git_clean_env()` (`:333-339`, consumed at `:1258,1262`); those separate environment checks also remain green. The observed mutation changes the actual constructed `git init` argv, but this probe installs or executes **no malicious hook**, and proves no malicious-hook side-effect difference. Under this clean fixture, ordinary Git operations complete in both versions. That does not make the versions equivalent to the explicitly asserted command-pin contract; it does prevent promoting the kill into a claim of demonstrated hook-execution prevention.

No registry identity/PID-reuse test is involved; no claim about real PID reuse is made. This leaf result is author-side advisory, not integration/admission, an aggregate recount, or an expertise/depth increase. Tools installed/updated: **none**.

**Verdict: genuinely discriminated, narrowly for the declared constructed-argv contract.**

Report: `.ufo/waves/round-21/w2/KillMB08.md`
