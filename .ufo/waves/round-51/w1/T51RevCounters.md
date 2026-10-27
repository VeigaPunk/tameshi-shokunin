# T51RevCounters — frozen counters vs predicate sentences (round-51, wave 1)

Seat: T51RevCounters · 2026-10-26 · read-only review.
Scope: `.ufo/evidence/round-51/c{1,2,3}/measure.py` against `claims.C{1,2,3}.predicate` in `.ufo/evidence/round-51/contract.json:22,35,49`; plus the three mandated checks (committed-bytes-only, TMPDIR/--work, crash-vs-PASS-label).

Method: full reads of all three counters and the contract; clause-by-clause mapping; read-only probes (selftests of all three counters, sha256 comparisons against `freeze.json`, sweep-receipt format grep, base-ledger diff, owner-blob pin, spec first-add commit time). No counter was run as a deciding verdict; every counter output below is reported as observed probe output. No LSP server is mounted in this seat's toolset, so literal `read`/`grep` were used; no semantic-proof claims are made beyond the cited lines. Working bytes of all reviewed files match the `freeze.json` pins (`sha256sum` over the 10 frozen paths — all identical), so this review is of the frozen bytes.

## Findings

### F1 — medium · C2 regression clause binds targets to live working trees, not revisions
`c2/measure.py:37` hardcodes `FLEET = '/home/vgpnk/Projects/shokunin'`; `:165-166` symlink those owner repos into the regression work dir and `:245-246` likewise reads the pin blob from the FLEET checkout. Every lane-side clause measures committed bytes (`show` at REV), and the pin clause reads a committed blob (`git show lrev:path`), but the `--regression` clause (`contract.json:35` "run from a clone at REV") pins only the lane; the nine gate targets are whatever the sibling working trees contain at run time.
Show: `sed -n '37p;162,176p;244,246p' .ufo/evidence/round-51/c2/measure.py`
Direction: looser than a strict at-REV reading (faithful to how the runner consumes targets at runtime; the deciding run witnesses only the lane tree — `deciding-run.sh` clean-tree-before/after — not siblings). A dirty sibling at deciding time can flip `regression=0/1` while all other clauses are revision-pinned.

### F2 — medium-low · C2 uncaught IndexError degrades diagnostics to a fake FAIL
`c2/measure.py:212` `name = path.split('corpus/', 1)[1]` raises IndexError when a cited SOURCES row's used-by names the entry without a `corpus/` prefix; `:356` catches only `(RuntimeError, ValueError, subprocess.CalledProcessError)`. Result: traceback, exit 1, no SETUP line — indistinguishable by exit code from a measured FAIL in `c2.exit`. Fail-closed (can never produce PASS), but an environmental data quirk would be misread as a verdict. Same class: `OSError` from `:163-171` (`makedirs`/`symlink`) is uncaught.
Show: `sed -n '205,215p;354,358p' .ufo/evidence/round-51/c2/measure.py`

### F3 — low · all counters: crash and measured FAIL share exit 1; the printed label is the only discriminator
Labels are built only after all checks complete (`c1:192-196`, `c2:276-279`, `c3:222-228`) and printed once (`c1:276`, `c2:361`, `c3:330`); caught exception classes exit 2 with `*_R51: SETUP`. No crash path prints a PASS label (mandated check: answered NO — a crash cannot print PASS). But `*.exit=1` alone cannot distinguish crash from `PASS=false`; the kill rules key on the printed label, and `deciding-run.sh` keys rc plus prints `tail -1` of stdout, so the round is safe. Residual exposure is only for consumers reading exit files without stdout.
Show: `grep -n 'SETUP\|print(line)\|return rc' .ufo/evidence/round-51/c{1,2,3}/measure.py`

### F4 — low · C1 "one row per F1..F10" is implemented as "one row per key of the frozen JSON"
`c1/measure.py:106` iterates `expected.items()`; nothing requires the key set to be exactly F1..F10 — `:195` only prints `frontier_rows=len(expected)`. The counter also does not bind the expected bytes itself: `:31` `EXPECTED_SHA = None  # pinned in freeze.json; the deciding run checks the frozen bytes`. The binding is real but external: `freeze.json` pins `c1/frontier-expected.json` and `deciding-run.sh`'s FROZEN list diffs it freeze→REV (any drift ⇒ DECIDING_RUN_EXIT=1). In isolation the counter is looser than the sentence; at round level the loophole is closed.
Show: `sed -n '29,31p;106,108p;193,196p' .ufo/evidence/round-51/c1/measure.py && grep -n 'frontier-expected' .ufo/evidence/round-51/deciding-run.sh .ufo/evidence/round-51/freeze.json`

### F5 — low · C1 round check is skipped for open statuses
`c1/measure.py:124` verifies `(round N)` only when `want['status'] != 'open'`; a frozen open row carrying a round would go unverified and a stray `(round N)` on an open cell passes. No effect today: the frozen file gives `round: null` to the three open rows F3/F7/F9 (`.ufo/evidence/round-51/c1/frontier-expected.json`). Looser than "states the status and round frozen".
Show: `sed -n '124,127p' .ufo/evidence/round-51/c1/measure.py && python3 -c "import json;d=json.load(open('.ufo/evidence/round-51/c1/frontier-expected.json'))['rows'];print({k:v['round'] for k,v in d.items() if v['status']=='open'})"`

### F6 — low · C1 SOURCES check evaded by malformed or emphasized rows
`c1/measure.py:153` skips rows with ≠11 cells entirely (no conflict, no used-by check); `:158,161` compare the status cell by exact string, so `**mined**` or trailing whitespace evades both conflict directions. The new S272/S273 rows must be exactly 11 plain cells to be checked at all. Looser than "no corpus/SOURCES.md row is `queued` with a used-by path or `mined` without one".
Show: `sed -n '150,164p' .ufo/evidence/round-51/c1/measure.py`

### F7 — low · C1 pointer clause reads only the status cell (stricter), range/word checks exact (match)
`:130` collects `README.md:A-B` pointers from the status cell only — a pointer in another cell of the row would not count (stricter than "row … cites"). `:133` accepts 1..6 lines (`b-a > 5` rejected) = the sentence's "<= 6 lines"; `:135-136` requires the id as a `\b` token (so F1 never matches inside F10) and the status phrase case-insensitively in the joined lines. Verified match where it matters.
Show: `sed -n '129,137p' .ufo/evidence/round-51/c1/measure.py`

### F8 — low · C2 regression clause keys on the LAST `REGRESSION: ` line, prefix match
`c2/measure.py:184-187` takes the last line starting `REGRESSION: ` and requires exit 0 plus prefix `REGRESSION: PASS (cases=10 passed=10`. An earlier FAIL line followed by a late PASS line would satisfy the clause (looser); trailing text after the prefix is allowed, faithful to the sentence's open-ended quote.
Show: `sed -n '184,187p' .ufo/evidence/round-51/c2/measure.py`

### F9 — low · C3 verdict-map token checks admit decimals
`c3/measure.py:123` `(?<![0-9])0(?![0-9])` matches the `0` in `0.5` (likewise `1` in `1.5`), and the usage-code check `:182` would accept `2` "declared" by `2.5`. Looser than the sentence's token intent for the verdict map; no effect on real rows (`0 clean; 1 failed; 2 usage`).
Show: `sed -n '121,124p;180,183p' .ufo/evidence/round-51/c3/measure.py`

### F10 — low · C3 registry section ends at any `#` line, including inside fences
`c3/measure.py:92` treats any line starting `#` as the section boundary — a fenced block with shell comments inside `### Gate/probe registry` would truncate row collection. Fail-closed (rows become `missing`), never a false PASS; noted because the real registry (SKILL.md:1499) is prose-adjacent and future edits with fences would silently fail C3.
Show: `sed -n '89,99p' .ufo/evidence/round-51/c3/measure.py`

### F11 — info · C2 pre-registration margin is 19 s in fact
The counter faithfully implements "MUTATE_DATE after the commit that first added the spec" (`:152-156`, strict `>`; freeze_ts = oldest adding commit's committer time, `:256-257`). Observed: spec first added at `fe335384` 2026-10-26T20:52:43-03:00 (=23:52:43Z); sweep `MUTATE_DATE: 2026-10-26T23:53:02Z` — 19 s. The check passes, but the evidential margin for "pre-registration before any mutant ran" is thin; a contract-strength matter, not a code defect.
Show: `git log --diff-filter=A --format='%H %cI' -- .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec | tail -1 && grep -n 'MUTATE_DATE' .ufo/evidence/round-51/c2/sweep/sweep.txt`

### F12 — info · C3 row/tool binding is substring-loose but execution-exact
Candidate selection `t not in c[2]` (`c3:121` in `row_reason`, `:202` in `measure`) is substring-based, but the executed self-test argv must name the tool exactly as argv[1]/argv[2] (`:135-141`), so a row for a superset path cannot cover the wrong tool. No defect.

## Mandated checks

1. **Committed bytes at REV only** — YES for all three, with one bounded exception. C1: every read is `git show`/`cat-file -e` at REV or BASE (`c1:175,183,191` and `show`/`exists` defs `:42-50`). C3: `show`/`ls-tree` at REV (`c3:103,106,111,190`), clone checked out detached at REV (`:198-199`). C2: lane bytes at REV (`:225,250,258`), owner blob via `git show lrev:path` in the owner repo (`:245-246`); the exception is F1's FLEET working-tree symlinks for the regression runner (`:165-166`). The deciding run additionally extracts counters from REV bytes and refuses a dirty lane tree (`deciding-run.sh`: `git show "$REV:$E/$f"`, `clean-tree-before.txt`).
2. **TMPDIR/--work honored, no hardcoded /tmp** — YES. No `/tmp` literal in any counter (`grep -n '/tmp' …` — no matches). C1 selftest: `mkdtemp(dir=os.environ.get('TMPDIR') or None)` (`c1:203`). C2: requires an existing empty `--work` (`c2:350-352`), clone + tmp under it, `TMPDIR` set for the runner (`c2:163-173`); selftest honors TMPDIR (`c2:317`). C3: same `--work` validation (`c3:319-321`), per-command tmp under work with `TMPDIR` (`c3:161-164`), selftest honors TMPDIR (`c3:244`). The only hardcoded absolute path is C2's `FLEET` (F1), which is an environment coupling, not a tmp violation.
3. **Can a crash print a PASS label?** — NO (see F3). Labels are emitted exactly once, after all checks, from data computed inside `measure()`; all anticipated failures exit 0/1/2/64 with the label, `SETUP`, or usage; uncaught exceptions traceback with exit 1 and no label.

## Verified-positive evidence (commands run, outputs observed)

- Counter bytes match the freeze pins: `sha256sum` over `contract.json`, `c1/measure.py`, `c1/frontier-expected.json`, `c2/measure.py`, `c2/bash-drift-pins.defects.spec`, `c3/measure.py`, `c3/tools-base.json`, `control/controls.py`, `no-harm.sh`, `deciding-run.sh` — all 10 identical to `freeze.json` values (spec `a98271f6…` = `SPEC_SHA` at `c2:38`).
- C2's recorded-leg regex is byte-identical to the canonical command D (`SCORECARD.md:73-74`) — `LEDGER_RE` at `c2:52`.
- C2's `wiring()` is a faithful port of the round-26 rule, same four components and regexes (`c2:75-101` vs `.ufo/evidence/round-26/c1-measure.py:8-13,46-65`).
- `BASE_LEGS` (`c2:41-51`) equals the base ledger exactly: `git show 9962033f:tools/mutate-and-run.sh | grep -oE '^#   (js|bash)-\S+'` → 9 legs, symmetric diff empty.
- Pin chain: `git -C kagi-shokunin show e64e81b8:corpus/drift-pins.sh | sha256sum` → `c138d34c7f0dfe9…` = sweep `CONTROL: GREEN … pristine-sha256=` (sweep.txt:5).
- Sweep receipt satisfies every C2 regex: one `MUTATE_DATE` (:2), exact CONTROL line (:5), ten `DEFECT` lines matching the ten spec ids in spec order (:7-27), `MUTATE_RESTORE: OK` (:29), `MUTATE: DONE` (:31). Spec has 10 `@defect` lines each preceded by `# PREDICT`; observed verdicts (2 KILLED / 8 SURVIVED) match the contract's recorded sweep.
- Selftests (probes, receipts in this dir): `T51RevCounters-c1-selftest.txt` — `cases=6 failed=0` rc 0; `T51RevCounters-c2-selftest.txt` — `cases=11 failed=0` rc 0; `T51RevCounters-c3-selftest.txt` — `cases=10 failed=0` rc 0. C1's selftest exercises the appended-correct PASS, rewrite-in-place FAIL (`readme_prefix=0`), queued/mined conflicts and used-by-missing paths (`c1:233-240`).
- No tool installs or upgrades were made (none needed).

## Residual risk and verification gaps

- I did not run any counter against the lane at REV (deciding-run territory); C2's full `measure()` incl. the regression clone was exercised only via selftest, so runtime behaviors like the 3600 s timeout path and symlink layout remain untested here.
- F1 means the deciding `regression=1` is only as clean as the sibling working trees at that moment; no monitor witnesses them.
- F2's IndexError path and C2's FLEET-coupled OSError path would surface as exit-1 receipts, not SETUP; a re-run under `--explain` would be needed to classify.
- C1's sentence-level strength (are the frozen statuses the right reading?) is explicitly `cannot_see` territory; this seat reviewed counter-vs-sentence fidelity only.
- C3 row truthfulness (kind/write-scope/pinned semantics per real tool) is out of scope for the counter and this review (contract `cannot_see`, wave-2 probes).

## Summary

- All three counters implement their frozen predicate sentences; no finding can produce a false PASS — every divergence fails closed or is bound elsewhere (freeze.json pins + deciding-run FROZEN diff).
- C2's regression clause alone is not revision-pinned on the target side (F1, FLEET working-tree symlinks, `c2:37,165-166`).
- C2 has an uncaught IndexError path (`c2:212`) that would masquerade as FAIL (F2); crash vs FAIL share exit 1 in all three (F3) — labels remain the discriminator and no crash prints PASS.
- C1 trusts the frozen JSON's key set (no F1..F10 count enforcement, `EXPECTED_SHA=None`, `c1:31,106`) — closed externally (F4); open rows skip round checks (F5, no effect on frozen rows); ≠11-cell or emphasized SOURCES rows evade the status checks (F6).
- C3 verdict-map tokens admit decimals (`c3:123,182`, F9); registry section ends at any `#` line incl. fences (`c3:92`, F10, fail-closed).
- Command D, round-26 wiring rule, BASE_LEGS, spec sha, blob pin `c138d34c…`, sweep-receipt formats and the 19 s pre-registration margin all verified as stated (Verified-positive; F11).
- Selftests: C1 6/6, C2 11/11, C3 10/10, rc 0 — receipts `T51RevCounters-c{1,2,3}-selftest.txt` in this directory.
