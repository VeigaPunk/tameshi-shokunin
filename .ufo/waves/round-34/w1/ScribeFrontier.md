# Round 34 / W1 — ScribeFrontier audit

## Verdict and scope

The four requested frontier checks conform structurally: the Gate source row has a URL, access date, and a quote under 25 words; the census capture ends successfully; the sourced-claim conjunct is supported by the knowledge entry and S101 registry row; and the Mistakes section contains the required fields. One non-blocking annotation discrepancy is recorded below: the lesson labels the quote “15 words,” while the exact quote has 16 whitespace-delimited words. It still meets the <=25-word requirement. [`.ufo/evidence/round-34/census-end.stdout`, `.ufo/evidence/round-34/census-end.exit`; `corpus/lessons/round-34.md:14-23,35-40,42-52`; `corpus/SOURCES.md:109`; `corpus/knowledge/witness-equivalence-rule.md:62-66`]

The lesson describes one mixed build+attack v2 wave under policy v2, band 64–128, with >=25% attack seats. This is reported as the lesson's description, not independently reconstructed from a dispatch artifact. [`corpus/lessons/round-34.md:66-73`]

## Requested checks

| Check | Evidence and result |
|---|---|
| Gate row | **PASS.** S101's Gate entry includes `https://mutation-testing.org/`, “accessed 2026-10-23 UTC,” and a quoted Overview feature-list excerpt. The lesson labels it “15 words”; a count of the exact excerpt gives 16 whitespace-delimited words, which is still <=25. [`corpus/lessons/round-34.md:14-23`; source registry confirms URL, fetched date, pinned snapshot and digest at `corpus/SOURCES.md:109`] |
| Census receipt | **PASS.** The committed capture lists S101 as mined and used by `corpus/knowledge/witness-equivalence-rule.md`, then ends with `tameshi ok` for `corpus/SOURCES.md`; the paired exit receipt contains `0`. The stdout is transcribed below with tab separators rendered as `\t`. [`.ufo/evidence/round-34/census-end.stdout`; `.ufo/evidence/round-34/census-end.exit`] |
| Sourced-claim conjunct | **PASS.** The knowledge entry cites S101 and explicitly says it was “opened this round”; the registry row is dated 2026-10-23 and lists that knowledge entry in `used-by`. [`corpus/knowledge/witness-equivalence-rule.md:62-66`; `corpus/SOURCES.md:109`; `corpus/lessons/round-34.md:35-40`] |
| Mistakes fields | **PASS.** At least one entry has `class`, `evidence`, `captured-by`, and `fix`; the first entry supplies all four labels. [`corpus/lessons/round-34.md:42-52`] |

Recorded census stdout (tabs rendered as `\t`; the committed receipt was read, not rerun):

```text
tameshi\tW04\tS047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi\tW04\tS048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi\tW04\tS075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi\tW04\tS076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi\tW04\tS077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi\tW04\tS078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi\tW04\tS081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi\tW04\tS092 duplicate url bazel.build/remote/caching across scopes
tameshi\tW01\tS101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi\tok\t/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

The paired `.exit` receipt contains exactly `0`. [`.ufo/evidence/round-34/census-end.stdout:1-10`; `.ufo/evidence/round-34/census-end.exit:1`]

## Measurement context (observed receipt, not retested)

The deciding-run capture reports:

```text
C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true
```

Its paired exit capture is `0`. This records the landed claim under attack; no counter or tool measurement was rerun for this audit. [`.ufo/evidence/round-34/measure/c1-deciding-run.stdout:1`; `.ufo/evidence/round-34/measure/c1-deciding-run.exit:1`; lesson summary `corpus/lessons/round-34.md:8-12`]

## Provenance commands and captured results

All paths below are absolute. The scratch command outputs and status files are under `/fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/`.

| Exact command | Result / captured status |
|---|---|
| `mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-mkdir` | exit `0` (`exit-mkdir`) |
| `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/lane; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-clone` | exit `0` (`exit-clone`) |
| `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-checkout` | exit `0` (`exit-checkout`) |
| `git -C /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/lane rev-parse HEAD > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/tip.txt; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-tip` | stdout `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`; exit `0` (`tip.txt`, `exit-tip`) |
| `git -C /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/tool.py; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-show-tool` | exit `0` (`exit-show-tool`); `sha256sum /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/tool.py > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/tool.sha256; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-hash-tool` stdout `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`; hash command exit `0` (`exit-hash-tool`) |
| `git -C /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/pristine.sh; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-show-runner` | exit `0` (`exit-show-runner`); `sha256sum /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/pristine.sh > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/runner.sha256; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-hash-runner` stdout `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; hash command exit `0` (`exit-hash-runner`) |
| `printf '%s\n' 'exporting source-code mutants; suppressing equivalent mutants; computing the mutant-detection rate and the set of live mutants' > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/quote.txt; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-write-quote` | exit `0` (`exit-write-quote`) |
| `wc -w < /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/quote.txt > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/quote-count.out; echo $? > /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/exit-count-quote` | stdout `16`; exit `0` (`quote-count.out`, `exit-count-quote`) |

The operational commands above had their exit codes saved after execution. The shell invocations also included final display-only `printf`/`cat` calls to print those saved values; those display calls did not have separate status files and are not used as evidence.

## Finding

**Non-blocking quote-count annotation:** `corpus/lessons/round-34.md:20-22` calls the Gate excerpt “15 words”; the exact quoted text is 16 whitespace-delimited words. Reproducer: `wc -w < /fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/quote.txt` → `16` (exit `0`; status at `exit-count-quote`). The required upper bound is nevertheless met. No other failure of the four requested structural checks was observed.

## Touched surfaces, exclusions, and artifact paths

- Only this report was written in the fleet repository: `.ufo/waves/round-34/w1/ScribeFrontier.md`.
- Scratch-only artifacts: the detached clone, pinned byte copies `tool.py` and `pristine.sh`, hash/exit records, and `quote.txt`/count output under `/fast/scratch/hyaku/tameshi-r34-seats/ScribeFrontier/`.
- No product source, frozen tool/runner, lane index, or lane state was edited. No tools were installed.
- Out of scope: no C1 counter invocation, no tool/runner execution, no mutation/attack run, and no revalidation of the captured measurement; no independent fetch of S101. The report verifies the requested landed-artifact structure and recorded receipts only.
