# L1Tameshi41.ReviewScribeEntry — round 41 w1 (pass 2)

Reviewed: `corpus/knowledge/r41-variable-destination-writes.md`
sha256 `ee7df01249e11d53a8f29911e3c1345bb78f93be7d9b7654474470fe74f3903a`, 107 lines, mtime 2026-10-25 03:46.
The draft was rewritten twice while this seat ran (62 lines `be997a8a…`, then 78 lines `5d9eb0f7…`, now this one).
Findings below are against **`ee7df012…` only**; the first pass's HIGH items were H1–H6 and its later items N1–N3 / M1–M5,
and the "closed" table records which the rewrite actually fixed.

Scope kept as assigned: sentences that overreach the two sources or the measured live sites, numbers without a receipt,
universal wording — each with the exact narrower replacement. No counter was run, at any revision. Live-site and path
checks call the tool and the counter's own helper functions directly.

Receipts that decide the new findings:

```
git -C kotodama-shokunin log --format='%h %ad' --date=short -- tools/harness/round_runner_conformance.py
  ac47c78 2026-10-19
git -C kotodama-shokunin log --format='%h %ad' --date=short -- tools/harness/receipt_guard_adoption.py
  4a7aede 2026-10-19
git -C tameshi-shokunin log --format='%h %ad' --date=short -- tools/write-path-census-v2.py
  5641ed8 2026-10-24
grep -n '__file__' tools/write-path-census-v3.py
  318:            here = os.path.dirname(os.path.abspath(__file__))
grep -c 'symlink' kotodama-shokunin/tools/harness/{round_runner_conformance,receipt_guard_adoption}.py   -> 0, 0
grep -c 'update_golden\|update-golden\|--update' (same two files)                                         -> 0, 0
grep -n "'--out'" tools/write-path-census-v3.py                                                          -> no match
```

## Closed since pass 1 (verified fixed, no action)

| pass-1 item | what the rewrite now says | verified how |
|---|---|---|
| H1 `3.14` | lines 1-2 read `Python 3.15.1 documentation` | snapshot `<title>` says 3.15.1 |
| H2/H3 fabricated resolved paths | lines 40-42 state the field is a concatenation, not a filesystem path, and say reading it as a path overstates it | `classify_source` record dump |
| H4 fixture-root inversion | lines 80-82 distinguish a scratch root from a non-scratch fixture root | `tools/repeat-control.py:597`; `fixtures.json` `var_unflagged` |
| H5 `get_source_segment` "bytes" | lines 14-15 now say a source segment, `None` on missing location | `ast.html` §ast.get_source_segment |
| H6 "two assignments up" | line 37 says three hops from `:597` | `:808` → `:806` → `:597`; `ReviewLiveSite.md:25-28` |
| N1 two-of-three unflagged | lines 50-60 name all three, and identify `tools/registry-replay.py:123` | directory census: 3 `unflagged` |
| N2 "expected but not unflagged evidence" | gone; lines 62-65 are a reading rule only | `tools/write-path-census-v3.py:177` |
| N3 "neither live call site" | lines 67-69 state seven sites, all `expected=False` | measured: 7 |
| M1 four scratch markers | lines 77-78 list all six | `SCRATCH_MARKERS`, `:38-45` |
| M2 per-destination update flag | lines 78-79 say the flag is read from the whole file | `:218` |
| M4 `write_bytes` unquoted | lines 21-23 ground it in the signature | `pathlib.html` §Path.write_bytes |
| M5 receiver generalization | lines 19-23 argue from the absence of a destination parameter | same |

## HIGH

### H1 · line 89 · "Both landed 2026-10-19, six days before this lane's v2."

Five, not six. The siblings landed 2026-10-19 (`ac47c78`, `4a7aede`); `tools/write-path-census-v2.py` has exactly
one commit, `5641ed8`, dated **2026-10-24**. Six days is the interval to **v3** (`d4ee4e6`, 2026-10-24 author date,
committed for the round-41 freeze) or to the 2026-10-25 freeze date, not to v2.

Replace `six days before this lane's v2` with:

> five days before this lane's v2 (`5641ed8`, 2026-10-24)

## MEDIUM

### M1 · line 90 · "no `__file__`, `with_name` or `joinpath`"

The token is present in the file: `tools/write-path-census-v3.py:318` reads
`here = os.path.dirname(os.path.abspath(__file__))`. The claim is true only of the *resolver*, and a reader who greps
finds a hit that looks like a refutation.

Replace `no `__file__`, `with_name` or `joinpath`` with:

> no resolver branch for `__file__`, `with_name` or `joinpath`

(Both siblings do have those branches — `round_runner_conformance.py:40,86,91` — so the contrast itself holds.)

### M2 · lines 57-60 · "the census counts it because an explicit output flag is not in the update-flag pattern. That is a classification gap, not a hidden update."

Two defects in two sentences. (a) The tool has no notion of `--out` at all (`grep -n "'--out'" tools/write-path-census-v3.py`
→ no match); it reports this site because `EXPECTED_RE` matched `expected.json` in the resolved text and nothing
suppressed it. The stated cause is an explanation the tool cannot express. (b) "not a hidden update" is a judgment;
the flag is in `tools/registry-replay.py:259` (`p.add_argument('--out')`) with `out = Path(args.out)` at `:181`, which
a reader can check, but whether an explicit `--out` ought to count as an update flag is a policy question this entry
does not settle.

Replace lines 57-60 with:

> The third, `tools/registry-replay.py:123`, writes `expected.json` into the directory named by its own
> `--out` argument (`tools/registry-replay.py:181,259`). The file text carries no update-flag token, so nothing
> suppresses the score. Whether an explicit `--out` directory should count as an update flag is not decided here.

### M3 · lines 90-93 · "plus three things those do not do: `os.symlink` destinations, the expected-value / scratch / update-flag classification, and scratch tracing through the assignment chain"

Two of the three are confirmed absent (`symlink`: 0 matches in both siblings; update-flag handling: 0 matches in both).
"the expected-value … classification" is not wholly absent: `round_runner_conformance.py:269-292` builds
`expected = f"reports/round-{round_number}/validation.json"` and matches write targets against it. That is one
hard-coded expected path, not a classifier, but "those do not do" reads as a flat negative.

Replace with:

> plus three things those do not do at destination level: `os.symlink` destinations, an expected / scratch /
> update-flag classifier over a resolved destination (the conformance tool matches one hard-coded expected path,
> `round_runner_conformance.py:269-292`), and scratch tracing through the assignment chain

## LOW

| line | current | narrow to | receipt |
|---|---|---|---|
| 7 | `cannot see` | `does not see` | "cannot" claims a limit on every literal-line census; the measured limit is v2's |
| 25 | `Neither source says anything about static analysis of a fixture census.` | `Neither quoted sentence mentions a fixture census or static analysis.` | `grep -ci 'census\|static analysis'` → 0 on both snapshots |
| 38 | `and the literal sits on the next line` | `and the literals sit on lines 821-822` | `tools/repeat-control.py:821,822`; the decisive reason is the absent `os.symlink` pattern, so the clause is supporting, not primary |
| 44-45 | `so both are correctly exempt` | `so both record `unflagged=0`` | `unflagged = expected and not scratch and not flagged`, `tools/write-path-census-v3.py:177` |
| 64-65 | `is routed to the next round` | `is not made in this round` | no routing artifact exists (no L0 question, no registry row); a forward promise is not evidence |
| 103-104 | `The scope seat exercises those cases and the docstring says the resolver is bounded.` | keep, but do **not** cite the report's path | `.ufo/waves/round-41/w1/ReviewV3Scope.md` landed 03:43 and does exercise these cases; see the m8 note below for why the path must stay out |

Note on line 103: the scope seat's verdict is stronger than "bounded" — five of the six docstring classes are
contradicted by observation. The draft's rewritten list (lines 100-104) already matches that verdict, so no prose
change is needed; the sentence is now substantiated by a landed report. This closes pass 1's LOW item on the scope
seat.

## Numbers audit (every numeral in `ee7df012…`)

| number | line | receipt | verdict |
|---|---|---|---|
| `183a4f8c…5317` | 1 | `sha256sum .ufo/evidence/round-41/sources/ast.html` | matches |
| `0044cae6…f093` | 2 | same, `pathlib.html` | matches |
| `3.15.1` ×2 | 1,2 | snapshot titles | matches |
| `15 words` | 12 | `len(q.split())` | matches |
| `16 words` | 19 | `len(q.split())` | matches |
| `180d` | 4 | contract wave item | matches |
| `2026-10-25` ×3 | 3,1,2 | contract `frozen_at`; both rows `opened` | matches |
| `depth of four` | 75 | `MAX_DEPTH = 4`, `tools/write-path-census-v3.py:42` | matches |
| `:811`, `:820` | 37-38 | tool records; `sites=6`, `expected_sites=2` | match |
| `:597` | 37 | `tools/repeat-control.py:597` | matches |
| `three` unflagged sites | 50 | directory census | matches |
| `:1682`, `:1685`, `:123` | 51,57 | tool records | match |
| seven replace/rename sites | 69 | directory census | matches |
| `2026-10-19` | 89 | `ac47c78`, `4a7aede` | matches |
| `six days` | 89 | 2026-10-19 → 2026-10-24 = five | **wrong — H1** |
| `depth 8` | 87 | `round_runner_conformance.py:34` | matches |
| `depth 6` | 88 | `receipt_guard_adoption.py:151,175` | matches |
| `five-pass` | 87 | `round_runner_conformance.py:109` `for _ in range(5)` | matches |
| `2026-10-19` "six days … v2" arithmetic | 89 | see above | — |

## Mechanical, gating

The seat spec says "Max 60 lines" (`.ufo/waves/round-41/spec-w1.json:149`); the draft is **107**, forty-seven over.
The prior-art section (lines 84-96) and the false-positive section (lines 48-69) are 13 and 22 lines of that. Either
the L1 waives the cap explicitly, or the entry is cut to the source statements, the two-site table, the m8-safe
reading rule and the not-claimed list. This is not an overreach finding, but a 107-line note will fail the seat's own
constraint no matter how the prose reads.

## C1 m8 status (checked, not assumed)

`path_tokens()` only accepts backticked tokens starting with `corpus/`, `tools/`, `.ufo/evidence/round-41/`,
`.ufo/waves/round-41/`, or the exact filenames in `PATH_EXACT` (`.ufo/evidence/round-41/calibration/measure.py:45-60`).
Run over the draft, the extracted set is: `tools/write-path-census-v2.py`, `tools/write-path-census-v3.py`,
`tools/repeat-control.py`, `tools/context-capture.py`, `tools/registry-replay.py`, `PROVINCE.md`. All resolve at
`--rev work`; `tools/write-path-census-v3.py` also resolves at the freeze (`git cat-file -e d4ee4e6:…`).

Two consequences worth keeping in mind when editing:
- The prior-art paths (`kotodama-shokunin/tools/harness/…`) are **not** extracted (no matching prefix), so they add no
  m8 risk. The illustrative `…/snap-tamper-duplicate-key/expected.json` is skipped for `…` at `:186`.
- Adding any `.ufo/waves/round-41/…` citation **would** enter the token set, and the wave tree is untracked at the
  freeze, so it would count as m8 until committed. That is why line 103 names the seat and not its report path.

## Residual risk

- **C1 m7 coupling.** The header cites S153/S154. `corpus/SOURCES.md` in the working tree holds both rows as `mined`
  (109 rows by `grep -c '^ *| *S[0-9]'`), but they resolve only if that append rides the same commit as this entry.
  The draft cannot fix this.
- **Snapshot drift.** Both snapshots are 3.15.1 under the rolling `docs.python.org/3/` URL; `recheck: 180d` is what
  keeps the quotes checkable, and the earlier `3.14` label shows the label drifts faster than the quotes do.
- **Not re-verified here:** whether the L1 has waived the 60-line cap for this entry. If not, the line count alone
  blocks the seat.
- **Peer note:** two incoming messages describe a move/removal of `.ufo/waves/round-35/scratch*` in another lane.
  This report cites no scratch path (`grep -n 'round-35\|scratch/'` → no match), so nothing here dangles.

## Tooling

No installs or upgrades; no pacman transaction was run. `git`, `python3`, the lane's census tool, and the counter's
pure helper functions (`path_tokens`, `resolves`) were sufficient; no counter run was executed.

Report: .ufo/waves/round-41/w1/ReviewScribeEntry.md
