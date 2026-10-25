# ExecCensus — round 43, wave 1

Seat: `L1Tameshi43.ExecCensus` (leaf). Item: run the fleet sources census `validate` for lane
`tameshi`, report stdout/stderr/exit code and the row count it implies, and leave the bytes for
the L1 to copy. No tool installs (nothing needed; no pacman/uv/npx action taken — pacman stays
paused per the operator directive). No counter run; no lane edit; no git/jj mutating command.

## Command and streams

Run from `/home/vgpnk/Projects/shokunin` at **2026-10-25T10:52:15Z** (UTC; local mtime of the
saved file `07:52:15 -0300`):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

- **exit code: 0**
- **stderr: empty** (0 bytes; saved `census-start.stderr`)
- **stdout: 11 lines, 1015 bytes**, sha256 `bb8c4162239efce3e0e798ed19c66d0949873269df53b638fc147c3d037af621`
  (saved `/tmp/tameshi-r43-ExecCensus-/census-start.stdout`)

Verbatim stdout (tabs shown as-is; 9 × W04 + 1 × W01 + 1 ok):

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Zero `E[0-9][0-9]` lines (validate exit 0 means no E findings, no missing registry, and the
`used-by` path check `usedby_findings()` emitted nothing: every mined row's used-by target
resolves against the lane root). Warnings, per the script contract, do not affect exit status.
The 10 W lines name 10 distinct rows: S047, S048, S075, S076, S077, S078, S081, S092, S101, S104.

## Row count implied: **113 registry rows**

`validate` never prints a count, so the count was pinned three independent ways on the exact
bytes that were live at capture:

1. **Capture-state identity.** At capture the lane file was `corpus/SOURCES.md` sha256
   `afb6e5cb014be1a1a4a3621f10d34fe7afa6f9df241517ddf869896c709c38da`, 450 lines, 95387 bytes.
   That is byte-identical to the freeze blob `17f6ef0c72ec27e1aea305b5c95806b43bb2caef:corpus/SOURCES.md`
   (`git show HEAD:corpus/SOURCES.md | sha256sum` → same hash, 450 lines / 95387 bytes).
2. **Same parser, `census` mode, on a scratch extraction of that blob** (`git archive HEAD` into
   `/tmp`, then `sources-census.sh census --file …/corpus/SOURCES.md`, exit 0):

   ```
   file	rows	113
   file	tier.A	101
   file	tier.B	9
   file	tier.C	3
   file	status.mined	85
   file	status.queued	22
   file	status.rejected	6
   ```

   `FLEET rows 113`, `invalid 0`, `missing 0`. Saved as `/tmp/tameshi-r43-ExecCensus-/census-start.rows.stdout`.
   Its `validate --file` output, with the lane column and `ok` path normalized away, diffs empty
   against the live capture (`DIAG_DIFF_RC=0`), so the scratch blob and the captured lane state
   are the same registry.
3. **Parser replica + direct line count.** Re-implementing the script's `row_pass` rules
   (0–3-space headings/rows, `## Registry` section only, header and separator rows skipped) gives
   `rows=113`, `NF=13 count=113`, `distinct_ids=113`, first `S001`, last `S158`, zero duplicate
   ids. Direct count of registry body lines is 114, minus the single `|---|---|…|` separator = 113.

So the capture implies 113 parsed rows: 101 tier A / 9 B / 3 C, 85 mined / 22 queued / 6 rejected;
all 113 have 13 pipe fields (no E01/E02), no duplicate id (no E03), and the id range is
S001–S158 with declared gaps (leads/allocation gaps, not lost rows).

## Baseline agreement

The saved stdout is byte-identical to both round-42 baselines:

```
cmp /tmp/tameshi-r43-ExecCensus-/census-start.stdout .ufo/evidence/round-42/census-sources/start.stdout  → 0
sha256 .ufo/evidence/round-42/census-sources/{start,after}.stdout → bb8c4162… (both)
```

A second live run at 10:53:13Z (file still sha `afb6e5cb`) reproduced the same 11 lines and exit 0
(`cmp … → 0`), i.e. the census-start result is deterministic.

## Live drift observed during this seat (not mine, flagged for the L1)

`corpus/SOURCES.md` was being written by another seat while this item ran; the saved "before"
bytes are the 10:52:15Z capture above. Observed states:

| UTC | sha256 | lines | registry rows | last id | validate stdout |
|---|---|---|---|---|---|
| 10:52:15Z (capture) | `afb6e5cb…` | 450 | 113 | S158 | 11 lines, exit 0 (saved) |
| 10:53:22Z | `8e404f30…` | 457 | 115 (S159, S160 present) | S160 | 11 lines, exit 0, byte-identical |
| 10:53:57Z | `5e556fdc…` | 456 | 114 | S159 | 11 lines, exit 0, byte-identical |
| 10:54:53Z (last check) | `5e556fdc…` | 456 | 114 | S159 | 11 lines, exit 0, byte-identical |

`git status --porcelain corpus/SOURCES.md` is now ` M`. The appended row(s) are clean
(`S159 | Mutation testing (Wikipedia) — https://en.wikipedia.org/wiki/Mutation_testing | docs | A | …`,
mined, 2026-10-25, 180d) and add no E/W codes, which is why validate bytes did not move even as
the row count did. **The census-before row count is 113**, tied to sha `afb6e5cb…`; any count taken
after 10:53:22Z belongs to the post-append state.

## Artifacts left in place (for the L1 to copy)

- `/tmp/tameshi-r43-ExecCensus-/census-start.stdout` — 1015 B, sha256 `bb8c4162…` (required)
- `/tmp/tameshi-r43-ExecCensus-/census-start.stderr` — 0 B
- `/tmp/tameshi-r43-ExecCensus-/census-start.rows.stdout` — 315 B, the `census`-mode row totals
  for the same capture state (sha256 `4e2292ed…`)

The scratch `git archive` extraction and intermediate outputs were deleted; the three files above
are the only residue.

## Not done (by bounds)

- No edit to `corpus/SOURCES.md` (the observed change is another seat's append; I did not touch it).
- No round-43 counter run (C1/C2/C3 deciding runs belong to the L1).
- No `git add/commit/stash/checkout/switch/reset/pull/push`, no mutating `jj` command;
  only read-only `git show`, `git archive`, `git status`, `git rev-parse`.
