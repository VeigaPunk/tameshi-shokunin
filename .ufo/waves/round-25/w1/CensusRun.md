# CensusRun — fleet sources census validation for lane `tameshi`

**Verdict.** The assigned read-only run **exits 0** (clean). It emits exactly **seven
non-ok lines, all `W04`** (same URL across scopes), and **zero `E01`–`E12` error lines**.
The trailing `tameshi<TAB>ok<TAB><path>` status line closes the lane. The command is
deterministic: three consecutive runs produce byte-identical stdout (sha256 prefix
`4acd8c3877435137`) with zero bytes on stderr. The lane registry
`tameshi-shokunin/corpus/SOURCES.md` parses to **83 rows** with **no malformed row
(E01), no invalid enum (E05/E06/E07), no bad date (E08/E09), no community-at-tier-A
(E10), and no dangling used-by path (E11)** — every registry row was structurally
admitted; the only residue is the advisory `W04` class.

This item is read-only. It changes no production file, writes no registry, and creates
no new artifact beyond this report.

## Command and exit code

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

- **Exit code: `0`** (`clean or warnings`; the script's own contract: "0 clean or
  warnings · 1 E/overdue findings … · 2 usage/env/missing registry").
- stdout: 8 lines. stderr: 0 bytes.
- Tool sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`
  (`scripts/sources-census.sh`); registry sha256
  `20119ebbc1f153c93ee5338c0072b731a07d3ef3ac633b72c6890c5089a7c2b9`
  (`tameshi-shokunin/corpus/SOURCES.md`).
- Environment: GNU bash 5.3.20, GNU Awk 5.4.1 (gawk is the script's parser).
- Determinism: 3 repeats → identical stdout sha, `diff run1 run3` empty.

## Every non-ok line (verbatim, TSV)

All seven are the same code class, `W04` — "same URL across scopes" — emitted at
`scripts/sources-census.sh:644-645` when a URL was already seen under a different
scope key (`u in url_seen && !(scope_key in url_scopes)`).

| # | line (lane⇥code⇥detail) | registry row | URL (normalised) | first row with that URL |
|---|---|---|---|---|
| 1 | `tameshi⇥W04⇥S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes` | `corpus/SOURCES.md:56` | `pitest.org/quickstart/incremental_analysis` | S041 (`:50`) |
| 2 | `tameshi⇥W04⇥S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes` | `corpus/SOURCES.md:57` | `pitest.org/quickstart/incremental_analysis` | S041 (`:50`) |
| 3 | `tameshi⇥W04⇥S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes` | `corpus/SOURCES.md:84` | `man7.org/linux/man-pages/man1/strace.1.html` | S060 (`:69`) |
| 4 | `tameshi⇥W04⇥S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes` | `corpus/SOURCES.md:85` | `docs.jj-vcs.dev/latest/git-compatibility` | S061 (`:70`) |
| 5 | `tameshi⇥W04⇥S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes` | `corpus/SOURCES.md:86` | `man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html` | S068 (`:77`) |
| 6 | `tameshi⇥W04⇥S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes` | `corpus/SOURCES.md:87` | `man7.org/linux/man-pages/man2/open.2.html` | S072 (`:81`) |
| 7 | `tameshi⇥W04⇥S081 duplicate url bazel.build/reference/test-encyclopedia across scopes` | `corpus/SOURCES.md:90` | `bazel.build/reference/test-encyclopedia` | S028 (`:39`) |

Closing status line (not a finding):

```
tameshi⇥ok⇥/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

### Error-code census (coverage of the validator)

Code histogram over the lane's stdout: `ok` × 1, `W04` × 7, **no `E*` line at all**
(`grep -c '^tameshi⇥E'` → `0`). Consequently none of E01–E12 fired:
no malformed row (NF≠13), no bad id, no duplicate id, no duplicate URL+scope,
no kind/tier/status enum violation, no future or non-ISO `opened`, no invalid
`recheck`, no community at tier A, no missing used-by path, no row outside `## Registry`.

## Why the seven `W04`s are advisory, not defects

Each W04 pair is a **deliberate supersede chain**, not accidental duplication. Every
one of the seven later rows carries an explicit `supersedes S###` marker in its
`teaches` cell, and the earlier row in each pair keeps the original, broader scope:

| later row | supersedes | original scope | later scope (narrowed) |
|---|---|---|---|
| S047 (`:56`) | S041 (`:50`) | "F7 — PIT's result-reuse assumptions" | "PIT's documented experimental incremental-analysis assumptions, not a general reuse guarantee" |
| S048 (`:57`) | S047 | S047's item-4 prioritisation scope | "PIT's item-4 prioritisation distinction without resolving an ambiguous pronoun" |
| S075 (`:84`) | S060 (`:69`) | "strace's own `%file`, `-f`, `-o` and `-y` semantics for an input observer over lane commands" | "supersedes S060's anchor only: the syscall filter the lane collector actually passes" |
| S076 (`:85`) | S061 (`:70`) | "colocated jj/git workspaces: what Git HEAD points at and why a Git-side HEAD read is not the branch tip" | "supersedes S061's paragraph anchor only" |
| S077 (`:86`) | S068 (`:77`) | "PR_SET_CHILD_SUBREAPER's reparenting rule: an orphaned process is reparented to the nearest still living ancestor" | "supersedes S068's anchor only" |
| S078 (`:87`) | S072 (`:81`) | "open(2)'s access modes and open-time effects, for whether an O_RDWR open is a pure read input" | "supersedes S072's teaches: what an O_RDWR open is, without the O_TRUNC overstatement" |
| S081 (`:90`) | S028 (`:39`) | "Bazel's normative hermetic test contract" | "precise test-result and premature-exit wording, superseding S028's shorthand" |

The set of registry rows whose `teaches` contains `supersedes S###` is exactly
`S047 S048 S075 S076 S077 S078 S081` — **7 rows, identical to the 7 W04 lines**. The
correlation is exact and one-to-one, which confirms the W04 set is fully explained by
the supersede mechanism and that no unrelated duplicate URL lurks in the registry.
The script's own rule set anticipates this: `W04` is a warning and "W-codes and
unlisted lanes never change status", whereas `E04` (duplicate URL **within** a scope)
would fail validation — and E04 did not fire, because the supersede marker in `teaches`
is what distinguishes a legitimate scope-narrowing from a same-scope duplicate.

Row-status context (all seven are `status=mined`; their predecessors are also
`mined`): the `W04` residual is a scope-narrowing record trail, not an unused or
thin row, so `W03` (mined but unused) and `W02` (thin reject reason) do not fire
either.

## Registry census for the same lane (context for the coverage axis)

`scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi` (exit 0):

```
tameshi  rows 83   tier.A 74   tier.B 7   tier.C 2
tameshi  status.mined 54   status.queued 23   status.rejected 6
FLEET    rows 83   tier.A 74   tier.B 7   tier.C 2   tier.invalid 0
FLEET    status.queued 23  status.mined 54  status.rejected 6  status.invalid 0
FLEET    missing 0
```

All 83 rows carry a valid tier and a valid status; `tier.invalid = 0`,
`status.invalid = 0`, `missing = 0`. Because the lane is the only registry present
for this root's target set, `FLEET.*` mirrors the lane's own totals exactly.

## Fleet-wide cross-check (context only, not part of the assignment)

Running the same validator over the whole fleet root (`validate --root
/home/vgpnk/Projects/shokunin`, no lane argument) also exits **0** with empty stderr.
`W04` counts by lane: souji 30, kama 25, tabi 16, kengaku 14, kagi 14, tsukuroi 9,
**tameshi 7**, mado 7, mori 6, kaidoku 5, revenger 3, lore 2 (+1 `W01`), kasegi 2,
audio 2 (+1 `W01`), kake 1. The `tameshi` block in the fleet-wide run is **byte-for-byte
the same 8 lines** as the lane-scoped run, so lane scoping neither adds nor suppresses
findings. The lane's 7 `W04`s place it mid-fleet — below the four heaviest lanes
(souji, kama, tabi, kengaku/kagi) and above the lightest (kake, audio, kasegi, lore).

`shared` mode over the fleet root shows that two of the six tameshi URLs are also
present in sibling lanes — `docs.jj-vcs.dev/latest/git-compatibility` (tameshi, mori,
souji) and `man7.org/linux/man-pages/man2/open.2.html` (tameshi, souji) — i.e. those
two are cross-lane coincidences rather than tameshi-internal scope splits, while the
other four (pitest incremental_analysis, strace.1, PR_SET_CHILD_SUBREAPER.2const,
bazel test-encyclopedia) are tameshi-local. `shared` is a separate mode from
`validate` and does not affect the validate verdict.

## Cross-check against an existing receipt (read-only)

The lane already holds `.ufo/evidence/round-25/census-start.stdout` and
`.ufo/evidence/round-25/census-start.exit` (both written 2026-10-22 05:20:15 -0300,
by an earlier seat, before this item's run at 05:21:04). `cmp` shows
`census-start.stdout` is **byte-identical** to this run's stdout, and
`census-start.exit` contains `0` — the same exit code. The receipt therefore
reproduces exactly; this item adds no new divergence.

## Findings, risks, blockers

- **Findings.** 7 advisory `W04` findings, all explained one-to-one by
  supersede-chain rows; 0 error findings; exit 0. The registry is contract-clean.
- **Risk.** None to the lane's contract compliance. The residual `W04` count is a
  property of the supersede mechanism, not of registry hygiene; suppressing it would
  mean merging scope-narrowed rows, which would destroy the anchor-level correction
  trail the lane's `teaches` cells record (S075→S060, S076→S061, S077→S068,
  S078→S072, S081→S028, S047/S048→S041). **No correction is warranted.**
- **Blockers.** None.
- **Smallest safe correction.** None required — nothing to change. This item is a
  read-only observation; it deliberately makes no move on any axis and edits no
  production file.

## Method note (mutation, tools, side effects)

- No tool was installed or upgraded: `sources-census.sh` needs only bash + coreutils +
  gawk, all present (bash 5.3.20, gawk 5.4.1). No pacman/uv/npm/cargo transaction was
  performed, so there is nothing to record on the tooling directive.
- The script was invoked with no `--out`, so it wrote **stdout only**; the fleet repo
  `/home/vgpnk/Projects/shokunin` and the lane repo were not mutated by this run.
  `git status --porcelain` (read-only, `GIT_OPTIONAL_LOCKS=0`) shows no new entries
  attributable to this item; the pre-existing dirty set (`.ufo/state/*.report-baseline`,
  `.ufo/watchdog.log`, `.scratch/goal-20261022-hyaku-12h.md`, `write`,
  `scripts/hyaku/__pycache__/`) predates it and belongs to other seats.
- All command output was captured under `/tmp` only.
