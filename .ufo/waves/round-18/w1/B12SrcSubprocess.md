# B12SrcSubprocess — S076 frontier source step (C2 P10)

## Behaviour
- Checked `corpus/SOURCES.md` for the target URL before drafting.
- Result: DUPLICATE. `https://docs.python.org/3/library/subprocess.html` is registered as S049 (`corpus/SOURCES.md:58`, status `mined`, opened 2026-10-20). Per the assignment, the draft stopped at `DUPLICATE S049`.
- Output written: `.ufo/waves/round-18/sources/S076-B12SrcSubprocess.md`.

## Evidence
- Command/tool: `_grep` for `docs.python.org/3/library/subprocess` in `tameshi-shokunin/corpus/SOURCES.md` returned one hit, line 58, S049 with the identical URL.
- Source opened: `read https://docs.python.org/3/library/subprocess.html` succeeded on the first try (no mirror needed). Page title: "subprocess — Subprocess management — Python 3.15.0 documentation"; 1460 lines in total, and I read lines 1–300.
- Timeout paragraph in the `run()` section (read at lines ~1–300): "If the timeout expires, the child process will be killed and waited for." The same paragraph states that the `TimeoutExpired` exception is re-raised after the child has terminated. It does not mention descendant processes. This is observed only in the part of the page I read; the `Popen` section (where `start_new_session` lives) was not read, because the stop rule applied.
- Row S049's recorded anchor and teaches text cover the `run()` env paragraph only (`corpus/SOURCES.md:58`).

## Gaps and limits
- No new row, Gate quote, or verbatim 25-word quote was produced, because the duplicate rule ended the draft. The duplicate-stop rule was applied as written.
- P10 purpose coverage: S049 does not record the timeout or `start_new_session` semantics. The L1 must decide whether to widen S049's scope or draft a distinct row (new id from S065, or a supersession). This seat did not edit the registry.
- Tools installed or updated: none.
- Git: no git commands run; no lane files modified other than the two outputs above.

## Verdict
DUPLICATE S049 — the registry already holds this URL; the P10 timeout/start_new_session purpose is not in S049's scope and is flagged for the L1. [built: decision file + report only]
