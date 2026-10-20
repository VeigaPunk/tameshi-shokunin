# S_KIND survivor non-equivalence probe

## Finding

The exact S_KIND mutant is **not whole-CLI equivalent**: `--help` omits `RECHECK_OVERDUE`. However, this is not a corpus-dependent checker difference. Against the valid off-suite fixture below, actual `--json` validation exits 0 in both copies and emits byte-identical JSON, including the `RECHECK_OVERDUE` warning. The help branch returns before reading `--self`, so the fixture path is present in that invocation but its contents do not cause the help-line difference.

The S_KIND pre-registration is `.ufo/evidence/round-18/sources-check/sources-check.defects.spec:13-16`. The pinned declaration is `scripts/sources-check.mjs:108-115`; the warning emission is at `:330-335`. The only uses of `FINDING_KINDS` are the usage text at `:130` and the one-sided coverage check at `:784-785` (search output also showed the declaration at `:108`). The selftest adds observed kinds through `expectKind` (`:575-581`) and has an overdue fixture (`:656-672`), so the removed kind is itself observed before the declared-kind check. **[INFERENCE]** Consequently this single deletion does not appear to change selftest output, but `--selftest` was not run.

## Exact source/mutant evidence

Materialized pinned blob using:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs > /tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/pristine.mjs
```

Command chain exit: 0. Pinned blob SHA-256: `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`, matching the pre-registered spec at `.ufo/evidence/round-18/sources-check/sources-check.defects.spec:2`.

Built `/tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/mutant.mjs` by replacing exactly one `  'RECHECK_OVERDUE',\n` with the empty string (guarded for one occurrence), matching spec lines 15-16. Mutant SHA-256: `c80cb365d1093156013b3ddc839863d224685eae579280da0c6ff90c004f67c4`. `diff -u pristine.mjs mutant.mjs` exited 1 as expected and showed only deletion of the line at pinned source line 114.

## Fixture and outputs

Fixture bytes and all process outputs are retained under:

```text
.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/
```

- `fixture/corpus/SOURCES.md` — SHA-256 `7a7c9dca345efe7e90deb6d0a196750c0b5bf97b46321d4786e5caa4422090bd`; overdue registry row at line 6.
- `fixture/corpus/knowledge/alpha.md` — SHA-256 `4568a06e3dd7904d2d0593dadf5d204c20bcf1116f2822903e19bafdb0fc255e`.
- Full command log, source/mutant hashes, fixture bytes, output hashes, and interpretation: `transcript.md`.
- Exact stdout files: `pristine-check.json`, `mutant-check.json`, `pristine-help.txt`, `mutant-help.txt`; stderr files are empty (all 0 bytes).

Executed the following four invocations; each exited 0:

```text
node /tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/pristine.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture --today 2026-10-19 --json
node /tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/mutant.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture --today 2026-10-19 --json
node /tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/pristine.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture --today 2026-10-19 --help
node /tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/mutant.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_KIND/fixture --today 2026-10-19 --help
```

`cmp` of the check JSON exited 0. Both output objects contain the same warning `{\"severity\":\"warn\",\"kind\":\"RECHECK_OVERDUE\",\"path\":\"corpus/SOURCES.md\",\"line\":6,\"detail\":\"id=S001 recheck=2026-10-18\"}`. Both have `verdict: CLEAN`, `exitCode: 0`, and one warning.

`diff -u pristine-help.txt mutant-help.txt` exited 1. The single difference is the help `findings:` line: pristine lists `... HEADER_INCOMPLETE USED_BY_ASYMMETRY RECHECK_OVERDUE`; mutant ends at `... HEADER_INCOMPLETE USED_BY_ASYMMETRY`. Both help commands exit 0. Source `runCli` returns `USAGE` on help before `runCheck` (`scripts/sources-check.mjs:488-497`), explaining why this observed difference does not depend on the corpus.

## Contract assessment

The header comment explicitly identifies `RECHECK_OVERDUE` as a warning (`scripts/sources-check.mjs:31`) and describes text/JSON check results and exit behavior (`:39-44`). The actual checker still reports that warning in pristine and mutant JSON. The header does not explicitly promise that the help text’s `findings:` enumeration is complete; the help omission is externally observable and makes that inventory inconsistent with the documented finding kind, but it does not violate the stated warning-emission behavior. The help-only difference is therefore a real CLI non-equivalence, not evidence of a different corpus-check result.

## Verdict

**PARTIAL — the mutant changes `--help` output, but no corpus-driven check-output distinction was found; the fixture’s validation output is byte-identical.**
