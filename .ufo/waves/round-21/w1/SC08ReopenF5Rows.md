done

# S015 / S016 / S028 live reopen (2026-10-21)

Scope: reopened the three existing rows in `corpus/SOURCES.md` and checked their cited claims against the live canonical URLs. This report does not edit the registry. The C2 contract requires `corpus/knowledge/hermetic-env-differential.md` to have a `source:` header citing a mined SOURCES row; S028 is already mined, while S015 and S016 are still queued.

## S015 — Cram

**Verdict: drifted in anchor/precision; the core claims remain present.**

- Live URL: <https://bitheap.org/cram/>. The page identifies the example suite as Cram 0.7 and links `cram-0.7.tar.gz`; no separate page version or modification date is exposed. Reader result: HTML, native extraction (`artifact://48158`).
- The row's `§Usage` anchor is incomplete for output matching: the suffix rules appear earlier under “Format in a nutshell”; the `§Usage` section contains the skip and environment-reset statements.
- Located current wording:
  - “Output lines ending with either of the above keywords are always first matched literally with actual command output.” The preceding bullets specify `(re)` and `(glob)`; `(no-eol)` matches output without a final newline. For unprintable output, “Actual output lines containing unprintable characters are escaped and suffixed with a space and the keyword `(esc)`”; expected lines for it must also contain the keyword.
  - “Skipped tests (empty tests and tests that exit with return code `80`) are marked with `s` instead of a dot.”
  - The environment list says `TMPDIR`, `TEMP`, `TMP` are set to the runner's temp directory; `LANG`, `LC_ALL`, `LANGUAGE` to `C`; `TZ` to `GMT`; `COLUMNS` to `80`; and `CDPATH` and `GREP_OPTIONS` to the empty string. It expressly qualifies COLUMNS: with `--shell=zsh`, it cannot be reset and reflects terminal width.
- Precision drift: the current row describes `(esc)` alongside matching suffixes, but the page describes it as an escape marker for unprintable output, not a separate matching mode. The unqualified “COLUMNS=80” statement omits the zsh exception. The core facts otherwise hold; the page also names `TEMP`, `TMP`, `CDPATH`, and `GREP_OPTIONS`, omitted by the row's concise summary.
- Suggested anchor wording: `§Format in a nutshell (literal-first output matching and suffixes) and §Usage (return-80 skip and environment resets) @ Cram 0.7, reopened 2026-10-21`.
- Proposed C2 mutable cells, **only if the entry uses S015 as supporting evidence**: `recheck: 365d -> 365d` (fixed release documentation); `used-by: — -> corpus/knowledge/hermetic-env-differential.md`. S015 is currently `queued`, so it cannot itself satisfy the required mined-row `source:` header without a separate status transition. It need not be cited if S028 is used for that header.

## S016 — testscript (rogpeppe/go-internal)

**Verdict: teaches quote holds; the row's line anchor is mislocated on current `master`.**

- Live URL: <https://raw.githubusercontent.com/rogpeppe/go-internal/master/testscript/doc.go>. Current `master` resolves to commit `38c169d642f5e6ee08f0c90fe56b64c5ae2db19e` (commit date 2026-10-05); latest release API reports `v1.15.0` (published 2026-05-28). The raw module file says `go 1.25`; `doc.go` itself does not state a package release version. Reader result: text (`artifact://48159`); GitHub API evidence for the commit and release was also opened.
- **The current `doc.go:56-61` does not locate the row's teaching quote**: it contains the tail of the `hello.text` example (`stdout 'hello world\n'`, `! stderr .`, `-- hello.text --`, `hello world`). This is an anchor defect; the available commit metadata does not establish when it arose, so it is not attributed to a post-2026-10-19 change.
- All teaching claims are located in current `master`:
  - `testscript/doc.go:46-50`: “Each script is a text archive”; it begins with a command script followed by supporting files.
  - `:62-71`: “Each script runs in a fresh temporary work directory tree, available to scripts as $WORK”; `HOME=/no-home` and `TMPDIR=$WORK/.tmp` are documented, with Windows/Plan 9 alternatives also stated.
  - `:104-120`: “The command prefix ! indicates that the command on the rest of the line … must fail, not succeed”; the condition list explicitly includes `[net]` and `[exec:prog]`.
- Suggested replacement anchor: `testscript/doc.go:46-50, 62-71, 104-120 @ master 38c169d642f5e6ee08f0c90fe56b64c5ae2db19e, reopened 2026-10-21` (or pin a release tag instead of mutable `master`).
- Proposed C2 mutable cells, **if S016 is included as supporting evidence**: `recheck: 365d -> 90d` (mutable branch and defective line anchor); `used-by: — -> corpus/knowledge/hermetic-env-differential.md`. As with S015, S016 remains queued and cannot serve as the required mined-row header citation without a status transition.

## S028 — Bazel Test Encyclopedia

**Verdict: anchor and core claims hold; tighten two paraphrases.**

- Live URL: <https://bazel.build/reference/test-encyclopedia>. The page provides no Bazel release/version label. Its live HTML metadata reports `dateModified: 2026-10-20T15:33:42.541Z` (`artifact://48779`); the reader used the markdown alternate (`artifact://48160`). The page's modification metadata postdates the registry's 2026-10-19 opening, but without the prior response snapshot I cannot attribute a specific content change to that interval.
- Located current wording in `§Role of the test runner`: the outcome “must depend only on” declared-dependency source files, declared-dependency build products, and resources guaranteed by the test runner to remain constant. For results, “If a test process runs to completion and terminates normally with an exit code of zero, the test has passed. Any other result is considered a test failure. In particular, writing any of the strings `PASS` or `FAIL` to stdout has no significance to the test runner.”
- In `§Initial conditions`, `LANG` is required to be unset and `TZ` required to be `UTC`. `TEST_PREMATURE_EXIT_FILE` is marked optional and is an absolute private-file path “used for catching calls to `exit()`.”
- Precision drift: “exit code alone decides” should preserve the source's normal-completion condition (and its separate treatment of timeouts, signals, or prohibited behavior); the stdout claim is directly supported. “Catches early exits” is broader than the documented “catching calls to `exit()`”; narrow it to that wording. The row's LANG/TZ claims hold, although the initial-condition table specifies additional locale variables too.
- Suggested anchor wording: `§Role of the test runner (normal completion/exit result and PASS/FAIL stdout) and §Initial conditions (LANG, TZ, TEST_PREMATURE_EXIT_FILE) @ bazel.build, page modified 2026-10-20T15:33:42.541Z, version unstated; reopened 2026-10-21`.
- Recommended C2 header source: `source: S028` (already mined). Proposed mutable cells: `recheck: 365d -> 90d` (the live docs page is mutable and now carries a 2026-10-20 modification date); `used-by: corpus/lessons/round-12.md -> corpus/lessons/round-12.md, corpus/knowledge/hermetic-env-differential.md`.

## Evidence and limits

- Local rows read from `corpus/SOURCES.md:26-27,39`; F5 context from `corpus/README.md`; C2 entry path and mined-row requirement from `.ufo/evidence/round-21/c2-contract.json`.
- Live page reads completed for all three canonical URLs above. The reader did not expose HTTP status codes; no status code is claimed. GitHub API reads resolved current `master` commit and latest release for S016.
- The LSP device is not mounted (`read xd://lsp` returned `No such tool`); source text was read directly, and text search was used only to locate the registry rows, not as semantic proof.
- No shell commands, builds, tests, or installs were run; therefore no command exit codes apply. No packages/tools were installed or updated.
