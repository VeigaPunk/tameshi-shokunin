# T51W2ExecTool27 — C3 registry row audit: `tools/write-path-census-v2.py`

Seat T51W2ExecTool27, round 51 wave 2 (falsify). Read-only on the lane; every execution ran
from `git clone --shared` checkouts at CAND with scratch `TMPDIR` and stdin `/dev/null`.
Raw receipts: `.ufo/waves/round-51/w2/@P@ExecTool27/` (01–07b).

**Subject.** SKILL.md:2168 at `6d8c11e378aa90b12650808e1b79270742935f15` — the row
`| write-form census v2 | probe | ... |`. Frozen tool index 27 of 30
(`.ufo/evidence/round-51/c3/tools-base.json`), **not** index 16 (`tools/round21-measure.py`),
so the row-16 clone-context blocker is not this row.

## Result

**No falsifying mismatch on any of the four shallow fields the counter reads; three real
source-level mismatches found in what the row *says* about the tool.** The counter covers this
row (verified by running the frozen `measure.py` at CAND: `covered line 2168 selftest exit=0`).
The predicate's own `cannot_see` clause — "that a row's kind, write scope and pinned-value
description are true of the tool" — is where this row fails.

## 1. The row's own backticked self-test: green, fast, exactly as recorded

`python3 tools/write-path-census-v2.py --selftest` from a `--shared` clone at CAND,
`TMPDIR=$S/work/tmp`, stdin `/dev/null`:

- **exit 0**, five consecutive runs and three runs in a second independent clone, identical output every time.
- **wall 0.035–0.040 s** (limit 900 s).
- last stdout line, byte-identical to the row's recorded marker:
  `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`
  (receipts `02-selftest-and-usage.txt` D1–D4).
- cwd-independent: runs green from `/tmp` via an absolute path, because the default fixture path
  resolves through `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` (`:95-96`) — the
  tool anchors on its own location, not on cwd. A clone-context failure is therefore impossible
  for this tool's default mode.

## 2. Usage probe `--r51-no-such-flag`: exit 2, declared

- **exit 2** on five runs, wall 0.038–0.043 s, stdout empty, stderr
  `write-path-census-v2.py: error: unrecognized arguments: --r51-no-such-flag`.
- The row declares `2 could-not-evaluate (usage: unknown flag, or no mode given)`. The counter's
  token test (`(?<![0-9])2(?![0-9])`) matches. **Consistent.**
- The *no-mode* branch also measures 2 (`ap.print_usage(sys.stderr); return 2` at `:98-99`), so
  the row's parenthetical "or no mode given" is true as written.

## 3. Exit-code map: complete for 0/1/2, but understates the 1-branch's causes

Source has exactly three return sites — `:84 return 0 if not failed else 1`, `:99 return 2`,
`:103 sys.exit(main())` — plus argparse's built-in 2. No `os._exit`, no signal handling, no
`subprocess`, so **no code beyond 0/1/2 is reachable** and the map declares all three
(probed: 3/64/124/128 undeclared but unreachable — receipts `04-exit-code-map.txt` F1–F4).

**Mismatch 3a — the row's `1 failed` parenthetical names two causes; there are six.**
The row says: "1 failed (planted-fixture mismatch, also the uncaught exit for a missing or
unparsable fixtures JSON)". Measured reachable exit-1 paths through `--fixtures` (`:45-48`, no
try/except anywhere in the tool):

| input | exception | exit |
|---|---|---|
| valid JSON object, wrong counts | (planted mismatch, `:70-71`) | 1 |
| **missing file** | `FileNotFoundError` | 1 |
| **unparsable JSON** | `json.JSONDecodeError` | 1 |
| **a directory** | `IsADirectoryError` | 1 |
| **a JSON array** | `AttributeError: 'list' object has no attribute 'get'` | 1 |
| **an object missing keys** | `FAIL missing fixture …` then `:84` | 1 |

So a *valid* JSON file that is a list, or any directory path, exits 1 through an uncaught
traceback the row does not name. This is a **class-label error, not a code-coverage error**:
PROTOCOL §Gate standard maps 1 to `failed`, and four of these six are setup/`could-not-evaluate`
conditions being reported as `failed`. The row itself half-admits the shape by calling the
missing/unparsable case "the uncaught exit", but stops enumerating too early. A verdict reader
who sees exit 1 cannot tell "the planted fixture mismatched" (a real finding) from "the path
was a directory" (setup).

**Mismatch 3b — the usage probe's code is right for the wrong reason in the map.** Not an error,
but note for the L1: the map's `2` is attached to "usage", and the tool's only non-usage
`could-not-evaluate` route (unreadable input) is misfiled under 1 per 3a.

## 4. Kind `probe` — the one place the row is right and the *tool* is the reason

PROTOCOL §Gate standard: "A tool that cannot fail is a **probe**." This tool *can* fail (exit 1
on a planted mismatch), so by the letter of that sentence it would be a gate. But the tool has
**no measurement mode at all**: `--selftest` is the sole operation, and its entire subject is a
JSON file committed in the same repo (`:29`, `:95-96`). It reads no lane surface, compares no
lane state to a baseline, and returns a verdict about nothing but its own fixtures. `probe` is
therefore the correct *practical* kind, but the row reaches it by a route the standard does not
describe, and the counter cannot test either reading (it checks the literal string
`gate|probe` only).

**Structural observation, unique in the table.** Of the 30 round-51 rows, this is the **only**
one whose Entry command cell and Self-test command cell are the same backticked command
(`python3 tools/write-path-census-v2.py --selftest`; receipt `03-counter-row-logic.txt`, count: 1).
That is honest given the tool has one mode, but it makes the row's "entry command" field
carry no entry — a reader gets no invocation that does anything except self-test.

## 5. Pinned values: load-bearing, but count-pinned only

Row: "`.ufo/evidence/round-40/census/fixtures.json`; expected counts are literals in the selftest".

- Path exists at CAND **and** at BASE (`git cat-file -e`, both).
- Expected counts are literals at `:54-60`. **True.**
- **The pin is load-bearing**: appending a second write site to the pinned `bytes_unflagged`
  body moved the verdict to `bytes_unflagged=2 … FAIL … exit 1`. So the pinned file really does
  drive the expected behaviour. **True.**
- **The pin is not content-pinned.** Swapping `write_bytes` → `write_text` inside the pinned
  `bytes_unflagged` body — a *different write form*, the exact thing this tool exists to see —
  left `bytes_unflagged=1` and exit 0. The tool hashes nothing; only the five integer counts in
  the fixture file's values are ever compared. A hand-edit of the pinned artifact that preserves
  counts is invisible. PROTOCOL §Gate standard's "Two evidences" digest requirement is therefore
  not met as stated — though, since this registers as a `probe` with literals in-repo, the clause
  may not bind. Flagging for the L1, not calling it a kill. (Receipt `06-pinned-values.txt` H1–H4.)

## 6. Write scope: accurate

Row: "reads the fixtures JSON only; writes no lane path (stdout only)".

- Only file-opening call in the tool is `open(path, encoding='utf-8')` at `:46` — read mode, no
  mode argument, no other `open`/`.write`/`os.replace`/`os.rename`/`tempfile`/`shutil`/`Path`.
- `git status --porcelain` empty before and after; `--untracked-files=all` empty; **scratch
  `TMPDIR` left completely empty** — the tool allocates no scratch at all, unlike its siblings.
- `strace` confirms exactly one open of `…/clone/.ufo/evidence/round-40/census/fixtures.json`,
  `O_RDONLY`, and no `O_WRONLY|O_RDWR|O_CREAT` opens at all (receipt `05-write-scope.txt` G1–G3).
- `--fixtures PATH` only relocates the read, exactly as the row's Entry cell says. **True.**

## 7. Last-line marker: a real diagnostic, not author-chosen help text — with one vacuous counter

The row records the marker line and all five of its values. Tested three ways
(receipt `07-marker-and-mutation.txt`, `07b-scratch-vacuity.txt`):

- The marker is **computed**, not echoed: neutering `EXPECTED_RE` to never match drops
  `bytes_unflagged`/`replace_unflagged` to 0 → exit 1; neutering `FLAG_RE` raises
  `bytes_flagged`/`replace_flagged` to 1 → exit 1. It is a genuine five-position reading of the
  tool's own classifier. **Passes the "meaningful diagnostic" test.**
- **But `scratch_replace=0` is vacuous.** That fixture body is
  `os.replace('/tmp/a', '/tmp/scratch-out.json')` — `EXPECTED_RE` does **not** match it, and
  `classify_text` only increments `unflagged` when `EXPECTED_RE` matches *and* `SCRATCH_RE` does
  not (`:40`). The cell is therefore 0 unconditionally, and neutering `SCRATCH_RE` to never match
  leaves the verdict green (exit 0). **`SCRATCH_RE` — the scratch-exclusion rule the marker
  advertises as `scratch_replace=0` — is dead code against this fixture set.** One of the five
  numbers the registry row publishes as a finding is not a finding.
- Ordering note for the L1: on a red run the `FAIL …` lines print *after* the marker
  (`:72-83`), so the marker is the last stdout line only on the green path. The counter's marker
  check is unreachable on red (`run_row` returns early on `rc != 0`), so this does not affect
  scoring — but any future "marker must be last line" reading would fail the red path.

## 8. What this row proves about C3's comfort, in one line

This is a **structurally sound, honest, green row** — the strongest of the thirty on
concreteness, because the tool it names is a pure function of a committed file, so it is
clone-proof and hermetic. Its defects are all *prose-vs-source*: the exit-1 parenthetical
enumerates two of six causes and misfiles setup errors as `failed` (§3a); the pinned value is
count-only, not digest-pinned (§5); and one of the five advertised counters is vacuous (§7).
None is a counter mismatch, and none makes C3's predicate false. They are the exact residue the
contract's `cannot_see` line names, and they should be recorded as such rather than repaired
here — the seat does not write source or the row.

## Audit target and worktree state

All reads of the row and of the tool used `git show <rev>:<path>` at CAND, i.e. **committed
candidate bytes**, not the worktree. At yield time the lane worktree carries an in-flight edit to
`SKILL.md` by another party (18 insertions / 18 deletions: `tools/mutate-and-run.sh` line-pointer
refreshes and a TMPDIR note, all above the round-51 table, net line count unchanged) — not this
seat's, and line 2168 still carries this row verbatim. The audit is therefore unaffected; a
re-key against the final revision should re-read the row from that revision rather than from
line 2168.

## Evidence summary

| check | measured | row says | verdict |
|---|---|---|---|
| self-test exit | 0 (×8, two clones) | 0 clean | **match** |
| self-test wall | 0.035–0.040 s | — | well inside 900 s |
| last line | `WRITE_CENSUS_V2_SELFTEST: … all five values` | same string | **match** |
| usage probe exit | 2 | 2 could-not-evaluate | **match** |
| codes reachable | {0,1,2} only | 0/1/2 declared | **match, unreachable extras absent** |
| exit-1 causes | 6, incl. dir / JSON-array / missing-key | 2 named | **mismatch (§3a)** |
| kind | probe (sole mode = selftest) | probe | **match in practice, not by the standard's route** |
| pinned path | exists CAND+BASE, load-bearing | pinned | **match** |
| pinned strength | count-only, no digest | "counts are literals" | **match to the letter; weaker than Two-evidences** |
| write scope | one `O_RDONLY` open; no writes; TMPDIR empty | stdout only | **match** |
| marker meaningful | computed; moves under 2 of 3 mutations | recorded | **match, with `scratch_replace` vacuous (§7)** |
| counter result at CAND | `covered line 2168 selftest exit=0` | — | row is covered |
