# ReviewGate15 — C2 census attack on tools/tally-audit.py

## Verdict: miss found, but inside the pattern's named limits — no uncovered write

Frozen classifier (`tools/write-path-census.py:46-50`, `WRITE_RE`) counts `tally-audit.py`
at **write_sites=3 unflagged=0** — only lines 158, 320, 426 (`open(<tmp>, 'w')` scratch
scripts). Reproduced by loading the pinned tool and calling `classify_text` on the live
file.

## Missed writes in the file (WRITE_RE returns None for each)

- **tools/tally-audit.py:384** — `p = subprocess.run(argv, capture_output=True)` with
  `argv = ['bash', runner_path, '--regression']` (line 381). The subprocess executes the
  mutation runner's regression, which creates a fresh REGRESSION_WORKDIR and writes
  regression artifacts (REF_BLOCK lines 60-84 show the runner's `printf REGRESSION_WORKDIR`
  and `rm -rf "$root"` path). This is the one write in the file that lands outside the
  temp sandbox — caller-visible storage under `--workdir` — and the census sees none of
  it. It is gated behind `--then-regression` (line 453), a real opt-in flag, but
  `FLAG_RE` (line 55) only matches `--update*`/`update_goldens`, so the file would be
  classified unflagged had the write been visible at all.
- **tools/tally-audit.py:363, 418** — `tempfile.mkdtemp(prefix='tally-audit.')`:
  filesystem-creating calls, invisible to `open()`/`.write_text()`/`.write_bytes()`.
- **tools/tally-audit.py:366** — `os.mkdir(rtmp)`: directory write, same miss.
- **tools/tally-audit.py:371, 434** — `shutil.rmtree(tmp, ignore_errors=True)`: deletes,
  outside the write-only pattern.
- **tools/tally-audit.py:386-387** — `sys.stdout.write` / `sys.stderr.write`: pattern
  matches `.write_text(`/`.write_bytes(` only, never bare `.write(`.

## Why the named limits cover the miss

Docstring `tools/write-path-census.py:9-11`: *"This is not a full lexer and not a claim
that every write in every language is seen. Shell redirects and writes whose path is not
on the same line as the call are outside the frozen patterns."*

- Line 384's write happens inside the spawned bash runner → "every write in every
  language" disclaimer applies (it is also effectively a shell-side workdir creation).
- mkdtemp / os.mkdir / rmtree are Python filesystem mutations not enumerated by the two
  named exclusions; only the catch-all "not a claim that every write … is seen" covers
  them. If the catch-all is itself the named limit, the coverage is total; if the two
  specific exclusions are the entire limit, then `:366` (`os.mkdir`) is the one
  uncovered in-language, same-line miss — though it is scratch-space and would never
  flip `unflagged` (EXPECTED_RE requires `.expected`/`golden`/`snapshot` in the literal).

## Impact on the frozen predicate

None reachable: C2's PASS conjuncts require `gates=21/21` classified from REV bytes plus
selftest values, but assert **no** per-gate `write_sites` count. The undercount (3 vs ≥8
mutation points) cannot falsify `C2_R39_PASS`. `unflagged=0` is also correct for this
file — no write targets an expected-value file.

Residual risk: any sibling gate whose only writes are subprocess-driven expected-file
writes (like line 384's shape) is invisible to both `write_sites` and `unflagged`, and
the predicate has no conjunct that would notice.
