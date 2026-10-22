# MutateC1Counter — mutation probe of the round-26 C1 counter

Seat: `TameshiR26.MutateC1Counter` (mutation-tester). Wave 1 of round 26, item C1 (depth).
Everything below was run inside a private clone and a /tmp scratch tree. The lane was not
edited except for this report file.

## Verdict

**The counter can fail, and it kills all six assigned mutations.** At the base revision
`d4140796` the same counter reports `depth_score=8` and exits 1. Every one of the six
assigned runner mutations is detected: four score down to 8 (exit 1), one drops a leg to
`UNWIRED` with a named missing part (exit 1), and the duplicated ledger line makes the
counter refuse with `SETUP` (exit 2).

**But the counter is a purely textual wiring check, and eight further weakenings of the
`js-cite-check` leg pass it with `depth_score=9` and exit 0.** Two of those eight also pass
the runner's own `--selftest`; one of them makes the runner's *replay* refuse (`MUTATE:
SETUP`, exit 2) while the counter still calls the leg WIRED. Those are the coverage holes
this item is worth reporting.

## Setup (evidence)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/MutateC1Counter-r26
git -C /tmp/MutateC1Counter-r26 checkout -q --detach a08e85c5d7f899e8a5992e20517edb1a380d79eb
git -C /tmp/MutateC1Counter-r26 log --oneline -1
a08e85c round-26: ninth ledger leg js-cite-check (5/10, 10/10 verdict predictions), runner and interop wired to nine legs, ...
```

Detector (unmodified, copied out of the clone):

```
$ sha256sum /tmp/MutateC1Counter-r26/.ufo/evidence/round-26/c1-measure.py
7be08265e2cb12ff73ab5791f1da73fb0fc0335429026d793b6bf1b18428f843
```

Subject under test (pristine bytes, never edited in place):

```
$ sha256sum /tmp/MutateC1Counter-r26/tools/mutate-and-run.sh
fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de
$ git -C /tmp/MutateC1Counter-r26 show a08e85c5d7f899e8a5992e20517edb1a380d79eb:tools/mutate-and-run.sh | sha256sum
fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de
```

Every mutant was written to a fresh scratch tree under
`/tmp/MutateC1Counter-r26-scratch/<variant>/tools/mutate-and-run.sh` (one file per
variant); the clone's own working tree stayed clean (`git status --porcelain` empty).
The counter reads only `CLONE/tools/mutate-and-run.sh`, so each scratch dir is a valid
`--repo` argument.

What the counter actually checks (`.ufo/evidence/round-26/c1-measure.py`):

- `:23-24` — `LEDGER_RE` / `LEG_RE` match a ledger comment line `#   <leg> <path> <n>/<m>`;
  `:38-39` count them; `:40-42` a repeated leg name is a `SETUP` refusal.
- `:47` spec heredoc present: literal `cat >"$d/<leg>.spec"`.
- `:49` regression replay call present: `^\s*regression_case_git <leg> \$`.
- `:52` leg-check entry present: `'<leg>:<leg>.spec:TABLE_<X>:<n>:<k>'`.
- `:57-61` the named `TABLE_<X>` line exists, and its pair count equals `<n>` while its
  `KILLED` count equals `<k>`.
- `:67-69` `depth_score = min(10, recorded, wired)`; exit 0 only when `depth_score >= 9`.

It never opens the embedded spec, never opens the pinned blob, never runs the runner.

## The counter can fail (baseline)

The counter file itself was committed at `622d31d` (the frozen contract commit), so the
"before" state is the counter run against the base revision's runner:

```
$ git show d4140796f4e48e8ec81b793facba73fbd03b4443:tools/mutate-and-run.sh | grep -c '^#   \(js\|bash\)-'
8
$ python3 .ufo/evidence/round-26/c1-measure.py --repo /tmp/MutateC1Counter-r26-scratch/v0_base_at_d414079
C1_LEG js-kimi-census: WIRED
C1_LEG bash-surface-census: WIRED
C1_LEG bash-tsukuroi-census: WIRED
C1_LEG bash-mado-verify: WIRED
C1_LEG bash-checklist-run: WIRED
C1_LEG js-claims-check: WIRED
C1_LEG js-round-gate: WIRED
C1_LEG js-sources-check: WIRED
C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8
EXIT=1
```

Against the integration revision the same counter is green:

```
$ python3 .ufo/evidence/round-26/c1-measure.py --repo .
C1_LEG js-cite-check: WIRED
C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9
EXIT=0
```

## Assigned mutations (all six killed)

Anchors in `tools/mutate-and-run.sh` at `a08e85c`: ledger line `:95`, spec heredoc
`:1082`–`:1140`, `regression_case_git js-cite-check` block `:1424`–`:1428`,
`TABLE_CITECHECK` `:629`, selftest leg tuple `:1955`.

| # | Variant | Mutation | Counter output | Exit | Verdict |
|---|---------|----------|----------------|------|---------|
| 1 | `v1_drop_ledger_line` | delete ledger line `#   js-cite-check … 5/10 (50 %)` (`:95`) | `C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8` | 1 | KILLED |
| 2 | `v2_drop_regression_call` | delete the `regression_case_git js-cite-check` call + `st_citecheck=$?` (`:1424-1428`) | `C1_LEG js-cite-check: UNWIRED (regression-call)` → `depth_score=8` | 1 | KILLED |
| 3 | `v3_drop_spec_heredoc` | delete `cat >"$d/js-cite-check.spec" <<'EOT'` … `EOT` (`:1082-1140`) | `C1_LEG js-cite-check: UNWIRED (spec-heredoc)` → `depth_score=8` | 1 | KILLED |
| 4 | `v4_lent_killed_5to4` | selftest tuple `…TABLE_CITECHECK:10:5` → `:10:4` (`:1955`) | `C1_LEG js-cite-check: UNWIRED (table-counts)` → `depth_score=8` | 1 | KILLED |
| 5 | `v5_table_verdict_killed_to_survived` | `K_UNRESOLVED_SEV:KILLED` → `SURVIVED` in `TABLE_CITECHECK` (`:629`) | `C1_LEG js-cite-check: UNWIRED (table-counts)` → `depth_score=8` | 1 | KILLED |
| 6 | `v6_duplicate_ledger_line` | duplicate ledger line `#   js-cite-check …` | `C1_DEPTH: SETUP (duplicate ledger leg names)` | 2 | KILLED (refusal, not a score) |

Observed transcript for #2, #4 and #6 (representative, unedited):

```
=== v2_drop_regression_call ===
C1_LEG js-cite-check: UNWIRED (regression-call)
C1_DEPTH: recorded_cases=9 wired_legs=8 depth_score=8
EXIT=1
=== v4_lent_killed_5to4 ===
C1_LEG js-cite-check: UNWIRED (table-counts)
C1_DEPTH: recorded_cases=9 wired_legs=8 depth_score=8
EXIT=1
=== v6_duplicate_ledger_line ===
C1_DEPTH: SETUP (duplicate ledger leg names)
EXIT=2
```

Note on #4/#5: both land on the same `table-counts` reason. The counter does not
distinguish "the tuple lies" from "the table lies" — both are caught only because a
verdict flip changed the `KILLED` count. That is the hinge the next section opens.

## Extra probes — weakenings the counter cannot see

Each variant below is a real weakening of the `js-cite-check` leg. The counter calls the
leg WIRED and exits 0 in every case. Where an independent detector exists (the runner's
own `--selftest`, and a direct sweep against the pinned blob) it is run too, so the
report separates "the counter is blind" from "nothing is blind".

| # | Variant | Weakening | Counter | Runner `--selftest` | Direct sweep |
|---|---------|-----------|---------|--------------------|--------------|
| 7 | `v7_gut_spec_body_keep_cat` | the whole 57-line spec heredoc body replaced by junk; the `cat >"$d/js-cite-check.spec"` opening line kept | WIRED, `depth_score=9`, exit 0 | **FAIL** 96/97 (`FAIL embedded leg js-cite-check: spec and recorded table agree`) | — |
| 8 | `v8_ledger_rate_lie` | ledger line kill-rate text `5/10 (50 %)` → `9/10 (90 %)` (`:95`) | WIRED, `depth_score=9`, exit 0 | PASS 97/97 | — |
| 9 | `v9_table_id_rename` | `S_USAGE:SURVIVED` → `S_USAGE_X:SURVIVED` in `TABLE_CITECHECK` (`:629`), counts unchanged | WIRED, `depth_score=9`, exit 0 | **FAIL** 96/97 | — |
| 10 | `v10_wrong_pin` | `PIN_CITECHECK=405734…c9f` → `PIN_CITECHECK=000…0` (`:619`) | WIRED, `depth_score=9`, exit 0 | PASS 97/97 | pin mismatch → `REGRESSION_CASE … SETUP (pin mismatch: …)` at runner `:1239-1241` |
| 11 | `v11_verdict_swap_counts_preserved` | `K_UNRESOLVED_SEV:KILLED`→`SURVIVED` **and** `S_USAGE:SURVIVED`→`KILLED`: the table now lies about which defects died, killed count still 5 | WIRED, `depth_score=9`, exit 0 | PASS 97/97 | — |
| 12 | `v12_ledger_path_wrong` | ledger line target path → `kumitate-shokunin/scripts/cite-checkx.mjs` (`:95`) | WIRED, `depth_score=9`, exit 0 | PASS 97/97 | — |
| 13 | `v13_drop_spec_defect_directive` | the `@defect S_USAGE` directive (3 lines) deleted from the embedded spec; the table still lists 10 ids | WIRED, `depth_score=9`, exit 0 | **FAIL** 96/97 | — |
| 14 | `v14_stale_old_string_in_spec` | `@old     return 64;` → `@old     return 66;` in the embedded spec: the string no longer exists in the pinned blob | WIRED, `depth_score=9`, exit 0 | PASS 97/97 | **`MUTATE: SETUP (spec/preparation failed for 1 defect(s); no suite run)`, exit 2** |

Transcript for the two decisive rows (#14 and the control sweep):

```
=== v14 sweep (stale @old) ===
MUTATE_TARGET: …/target.mjs sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f bytes=126735
MUTATE_SPEC: …/cite-check.extracted.spec defects=10
APPLY FAIL id=S_USAGE line=50 old-string-count=0 expected=1
MUTATE: SETUP (spec/preparation failed for 1 defect(s); no suite run)
SWEEP_EXIT=2

=== v0 sweep (pristine spec, same target bytes) ===
MUTATE_RESTORE: OK (target-sha256 before=405734…c9f after=405734…c9f pristine-sha256=405734…c9f)
MUTATE: DONE (target=target.mjs defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
SWEEP_EXIT=0
```

The control sweep is also a free consistency check on the recorded table: replaying the
frozen spec against the pinned blob `405734…c9f` at
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` reproduces `killed=5 survived=5 kill-rate=50 %`,
i.e. `TABLE_CITECHECK` (`5/10`) and the ledger line agree with the bytes today. The
pinned blob hash was confirmed independently:

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
```

(`git show` only; the sibling repo was not written. `GIT_OPTIONAL_LOCKS=0` was set on
every read-only git call. No `jj` command was run anywhere.)

## Named weakenings, with the smallest safe correction

The counter can only be hardened by teaching it something it does not currently read.
Each item below names the smallest change that would close it; **none of these edits are
made here** — production files are the L1 integrator's to change.

1. **Spec body is unchecked (rows 7, 13).** The counter only greps the heredoc's opening
   line. Smallest fix: also require that the heredoc body contain one `@defect <id>` line
   per table id, e.g. assert `re.search(r"^@defect %s \|" % id, body, re.M)` for each id
   in the leg's table, and that the number of `@defect` directives equals `<n>`.
   Alternatively — cheaper and stronger — assert that the extracted heredoc body is
   byte-identical to the frozen pre-registration
   `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`. The runner's own selftest
   already kills rows 7 and 13, so this is a counter-side gap only.
2. **Only counts are checked, not identities or verdicts (rows 9, 11).** The counter
   compares `len(pairs)` with `<n>` and the number of `KILLED` with `<k>`; the *ids* and
   the *verdict attached to each id* are never compared with anything.
   Smallest fix: for each id in the table, require the id to appear exactly once as
   `@defect <id> |` in the embedded spec (row 9) — that closes the rename. Row 11 needs
   more: the counter would have to compare the table's per-id verdicts with the measured
   sweep evidence (`.ufo/evidence/round-26/cite-check/sweep/sweep.txt`), not with a
   count. Until then the table can lie about *which* defects died as long as the count
   holds.
3. **The ledger comment's numbers and path are unchecked (rows 8, 12).** The counter
   regexes `#   <leg> <path> <n>/<m>` but never reads `<n>/<m>` or `<path>`.
   Smallest fix: parse the `<n>/<m>` pair out of the ledger line and require
   `m == k` (the table's KILLED count) and `n == len(table pairs)`; require the ledger
   path to equal the `kumitate-shokunin/…` path in the leg's `regression_case_git` call.
   This makes the ledger comment a checked claim rather than prose.
4. **The pin and revision are unchecked (row 10).** `PIN_CITECHECK` / `REV_CITECHECK` are
   never compared with the materialized blob. The counter is a text reader, so the
   smallest in-counter fix is weak; the honest fix is to have the counter *also* read the
   git object store (`git -C <repo> show <rev>:<path> | sha256sum`) and compare it with
   `PIN_<X>`. That makes the counter need the fleet checkout, which is a design choice
   for the integrator, not for this seat.
5. **A spec whose `@old` strings no longer match the pinned blob is invisible (row 14).**
   The counter never resolves the spec against the target. Smallest fix: for each
   `@old` in the embedded spec, assert it occurs exactly once in the pinned blob
   (requires the same fleet read as item 4). This is the row where the counter said
   WIRED while the tool's own replay refused with `SETUP` — the most consequential gap
   found.
6. **A leg that is fully wired but has no ledger comment line is invisible.** The counter
   iterates over legs *found in the ledger* (`:39`); a leg that the runner actually
   executes but that lacks the `#   <leg> …` comment is never counted and never checked.
   Smallest fix: collect leg names from the `regression_case_git` calls and from the
   selftest leg tuples as well, and require the two sets to agree.
7. **`depth_score = min(10, recorded, wired)` caps the signal.** With nine legs the score
   is 9 either way; a tenth leg that is wired but uncounted (item 6) or a score of 10
   cannot be distinguished from 9 by the score alone. The per-leg `C1_LEG` lines carry
   the real signal; the headline score should not be read as "nine independent
   properties verified".
8. **The counter cannot detect a runner that is wired but never executed.** It reads the
   source of `mutate-and-run.sh` only; whether `--regression` actually runs the ninth leg
   is a runtime fact. The runner's own `--selftest` (97 cases, green at the pin) and the
   `v0` sweep above are the runtime witnesses.

## Restoration evidence

- The clone's `tools/mutate-and-run.sh` is byte-identical to the committed blob at
  `a08e85c` (both `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`).
- `git -C /tmp/MutateC1Counter-r26 status --porcelain` → empty. All mutants live in
  `/tmp/MutateC1Counter-r26-scratch/<variant>/tools/mutate-and-run.sh`; the pristine copy
  `/tmp/MutateC1Counter-r26-scratch/v0_pristine/tools/mutate-and-run.sh` hashes
  `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` — the same digest
  as the committed blob, so no mutant leaked back.
- The lane tree was not written by this seat. (`git status --porcelain` in the lane shows
  `M corpus/knowledge/mte-report-interop.md` and untracked `.ufo/evidence/round-26/after/`
  and `.ufo/waves/round-26/` — the first and third are other seats'/the integrator's
  output; this seat added only this report file.)
- No `jj` command was executed anywhere, and no git write command was run in the lane.

## Tooling

No tools were installed or upgraded for this item: `git`, `python3`, `bash`, `node` and
`sha256sum` were already present and sufficient. No pacman transaction was attempted
(host pacman transactions are paused), and no host service was restarted.

## What the integrator can take from this

The six assigned mutations are all caught, and the counter fails as intended at the base
revision. The counter should be read as a *wiring* check only. If C1's depth claim is to
mean "the ninth leg is really replayable at its pin", the counter as frozen cannot
establish that on its own: rows 7, 13 and 14 describe a runner the counter calls WIRED
while the runner itself refuses or fails. Closing items 1 and 5 (spec-body fidelity to the
frozen pre-registration, and `@old` resolution against the pinned blob) would close the
three highest-cost gaps with the least new machinery.

Report: .ufo/waves/round-26/w1/MutateC1Counter.md
