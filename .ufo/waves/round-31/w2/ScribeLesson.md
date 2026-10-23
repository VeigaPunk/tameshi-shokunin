# ScribeLesson — Gate draft

Drafting axes: citation completeness, provenance accuracy, and scope integrity.

## Paste-ready `## Gate` section

```markdown
## Gate

Sources re-opened or opened for this round:

- S055 (existing row re-opened; seat SrcDoctest): https://docs.python.org/3/library/doctest.html, fetched 2026-10-23 (216,574 bytes; SHA-256 `369dcc17009a2f36000284ca86eedb7cef4bc10f773e554754bbdad07791cc46`). Located quote (module introduction, first common-use bullet, HTML lines 249–250): “To check that a module’s docstrings are up-to-date by verifying that all interactive examples still work as documented.” (18 words). Keep S055; do not add a second row for this URL.
- S095 (Go testable examples; seat SrcGoExamples): https://go.dev/blog/examples, accessed 2026-10-23 UTC (40,059 bytes; SHA-256 `1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178`). Located quote (§Output comments, HTML lines 514–517): “The test passes if the test’s output matches its output comment.” (11 words).
- S096 (rustdoc documentation tests; seat SrcRustdoc): https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html, accessed 2026-10-23 UTC (51,137 bytes; SHA-256 `95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7`). Located quote (§Documentation tests, `#documentation-tests`, HTML lines 180–182): “rustdoc supports executing your documentation examples as tests. This makes sure that examples within your documentation are up to date and working.” (22 words).

Change log at content revision `2da841bd9913a2037d2bf612793382e572c9d205` (base `c111dab58b0a8d55e991bbd2efe3aad56717b95a`; `corpus/SOURCES.md` rows 92 → 94):

| ID | Status | Recheck | Used-by |
|---|---|---|---|
| S055 | `mined` → `mined` | `on-release` → `on-release` | `corpus/lessons/round-16.md` → `corpus/lessons/round-16.md`, `corpus/knowledge/executable-self-assessment.md` |
| S095 (new) | no row → `mined` | no row → `180d` | no row → `corpus/knowledge/executable-self-assessment.md` |
| S096 (new) | no row → `mined` | no row → `on-release` | no row → `corpus/knowledge/executable-self-assessment.md` |

S055’s registry `opened` value stayed `2026-10-20`; the source was re-opened on 2026-10-23. S095 and S096 were opened 2026-10-23. The historical `Next unused id: S092` line remains append-only; the old `S095` allocation footer is superseded by the current `Next unused id: S097` line (`corpus/SOURCES.md:368–377`).

Rejected drafts and identifier corrections:

- SrcDoctest’s proposed new S095 Python row was not added: its URL duplicates S055’s URL. The existing row was re-opened and its `used-by` gained the executable-self-assessment entry (`w1/SrcDoctest.md:7,23–31`; `corpus/SOURCES.md:368–372`).
- SrcGoExamples proposed S096, while SrcRustdoc proposed S095. The committed allocation is Go S095 and rustdoc S096: the Rustdoc proposal’s S095 identifier conflicts with the Go row, and the Go draft is shifted into the first available new ID (`w1/SrcGoExamples.md:32–41`, `w1/SrcRustdoc.md:18–25`, `corpus/SOURCES.md:373–377`). ScribeEntry’s earlier S095 Python / S096 Go / S097 Rust source mapping is superseded by the committed S055 / S095 / S096 mapping; no S097 source row was added (`w1/ScribeEntry.md:23,37–39`; `corpus/knowledge/executable-self-assessment.md:1,21–29`).

Binding-v4 controls and limits:

- Before cold-read data, the frozen binding-v4 replay rejected all five supplied negative-control shapes—`promptonly`, `donothing`, `textmention`, `noresult`, and `forged` (an echo-shaped call plus a matching result)—at 0/32 kept, exit 1. It also rejected the seven named historical input mutants: `different_tool`, `different_result_id`, `user_authored_call`, `error_result`, `comment_only_shell`, `result_before_call`, and `reused_call_id` (`w1/CtlBindV4Old.md:1–5,90–105`). This is evidence for those controls, not a universal forged-transcript guarantee.
- The separate new-shape falsifier found five of nine newly forged, non-executed shapes survived v4 at 63/63 kept, exit 0: `literal_heredoc`, `python_c_script_argument`, `false_and_branch`, `uncalled_function`, and `quoted_separator_argument`. Four were rejected: `echo_full_call`, `python_c_string`, `split_simple_commands`, and `changed_traced_argv` (`w1/CtlBindV4New.md:76–89,121–131`). The five survivors prevent treating a kept count as proof that the trace command executed.
- ReviewBindV4 separately found false-reject cases in its syntax-level matcher: genuine runs under control structures/loops, nested `bash -c`, launch wrappers outside the whitelist, comment-newline merging, quoted separator arguments, and backslash-newline continuations (`w1/ReviewBindV4.md:115–190`). These are review probes of the frozen binder, not a change to it.

Other wave-1 C1 rejection outcomes are negative controls, not successful mutation kills: do-nothing stayed red at seven mismatches; hidden-row, junk-row, deleted-row, and history-rewrite shapes were rejected, while their reports classify the mutation result as inconclusive because the frozen base already failed (`w1/CtlDoNothing.md:1–8`, `w1/CtlHiddenRows.md:3–7`, `w1/CtlJunkRows.md:3–7`, `w1/CtlRowsDeleted.md:1–11`, `w1/CtlRewriteInPlace.md:1–25`). Wrong-header controls A/B/D were rejected, but shape C (`| Axis | Score |`) passed, exposing the loose axis-header match; the old-value shortcut was rejected, while the contract-linked receipt shortcut passed (`w1/CtlWrongHeader.md:3–7`, `w1/CtlLabelShortcut.md:3–7`). The dead-seat probe also rejected document-frequency and anchor-token refinements as nondiscriminating; neither was adopted (`w1/BuildDeadSeatCheck.md:178–187`).
```

## Findings and evidence

- The content revision already contains the S055 re-open note, both new registry rows, and the corrected source IDs. Its `corpus/lessons/round-31.md` does not exist, so this is a draft for the L1 integrator, not a product-file edit.
- Source dates, digests, URLs, and anchors above come from the wave-1 fetch reports and the committed source/knowledge files; this seat did not fetch source pages or re-run source checks.
- Read-only evidence: content-revision `corpus/SOURCES.md:63–65,104–105,368–377`; `corpus/knowledge/executable-self-assessment.md:1–34`; `corpus/lessons/round-30.md:27–74`; base `SOURCES.md:63–65,355–366`; and the cited wave-1 reports.

## Commands and outcomes

Working directory for sandbox Git was only `/fast/scratch/hyaku/tameshi-r31-seats/ScribeLesson/`; all Git environment variables named by the lane bounds were unset.

- `mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/ScribeLesson` — completed without output.
- `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin .` — `Cloning into '.'...`; `done.`
- `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout --detach 2da841bd9913a2037d2bf612793382e572c9d205` — `HEAD is now at 2da841b round-31: content revision — SCORECARD standing rows re-stated (C1 data), S095-S096 + S055 re-open, knowledge entry, README row, QUALITY 66-71, SKILL recipe workdir rule`.
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show c111dab58b0a8d55e991bbd2efe3aad56717b95a:corpus/SOURCES.md > base-SOURCES.md` — completed without output; the captured baseline was read at lines 63–65 and 355–366.
- No gates, tests, counters, builds, or source fetches were run by this seat. No tools were installed or updated.

## Behavior, gates, and touched surfaces

- Behavior: no product behavior changed; the deliverable is a paste-ready lesson section grounded in committed bytes and wave-1 reports.
- Gates: none run by this seat. The observed control results stated in the draft are attributed to their wave-1 reports.
- Touched surfaces: this report only in the lane; the assigned scratch clone and `base-SOURCES.md` are under the assigned scratch directory.
- Out of scope: no edits to the lesson, registry, knowledge entry, SCORECARD, frozen binder/counter, or judge; no commit, push, publish, deployment, or producer-authentication/promotion/score claim.
- Known limit: the source observations are not independently re-fetched here; use the cited source-seat reports for their execution provenance. L1 must integrate the draft into the absent lesson file.
- Install record: none.

Report: `.ufo/waves/round-31/w2/ScribeLesson.md`
Scratch: `/fast/scratch/hyaku/tameshi-r31-seats/ScribeLesson/`
