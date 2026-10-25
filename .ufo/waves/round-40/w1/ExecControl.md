# ExecControl — C1 control re-run (v1 patterns against the frozen fixtures)

Seat: executor (leaf). Axis: depth. Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Contract read at `.ufo/evidence/round-40/contract.json` (frozen at `5641ed84c8dc148c34c8dd83f062279ddf06b4af`);
not edited. The default (non-control) counter was **not** run; no live-lane file was edited.
All scratch work in `/tmp/tameshi-r40-ExecControl/`.

## Assigned run

```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-40/census/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --control
C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false
EXIT=1
```

`C1_R40_CONTROL_PASS=false`, exit `1`. Default mode was not invoked.

This reproduction is byte-identical to the stored control artifact:
`cmp` of the fresh line vs `.ufo/evidence/round-40/control/v1-on-fixtures.stdout` → exit 0,
sha256 `6bc895367e1f31c787e57fb47fc1a38744ef46dad148ad14497421d271b6f9bc` on both;
`.ufo/evidence/round-40/control/v1-on-fixtures.exit` contains `1`.

False is the *intended* control verdict: `meets` at `census/measure.py:99` demands the v2 target shape
(`bytes_unflagged==1 and replace_writes>=1 and replace_unflagged==1`), and v1 scores 0 on both planted
classes. The line's three counters are the evidential part, not the PASS bit.

## Why the zeros are the right zeros (v1 vs v2 on the same fixture bytes)

Fixtures blob sha256 `af237473b3966d8b37e24bc9272909178aac4f2d77252045a0e3f9a5b20efa5d`, identical at
`HEAD` and in the worktree (`git show HEAD:…/fixtures.json | sha256sum` vs `sha256sum` on disk).

```
bytes_unflagged    v1 writes=1 unflagged=0 | v2 writes=1 unflagged=1
bytes_flagged      v1 writes=1 unflagged=0 | v2 writes=1 unflagged=0
replace_unflagged  v1 writes=0 unflagged=0 | v2 writes=1 unflagged=1
replace_flagged    v1 writes=0 unflagged=0 | v2 writes=1 unflagged=0
scratch_replace    v1 writes=0 unflagged=0 | v2 writes=1 unflagged=0
```

(scratch probe: load `census/measure.py`'s `v1_classify` and
`tools/write-path-census-v2.py`'s `classify_text`, apply both to `fixtures.json`.)

- `bytes_unflagged` (`fixtures.json:2`, `(out / 'expected.json').write_bytes(b'x')`): v1 *does* count the
  write (`writes=1`) but `V1_EXPECTED_RE` (`measure.py:38-40`) only knows `.expected`, `expected.txt`,
  `golden`, `snapshot` — `expected.json` misses, so `unflagged=0`. This is a true expected-pattern miss.
- `replace_unflagged` (`fixtures.json:4`, `os.replace(tmp, 'case.expected')`): `V1_WRITE_RE`
  (`measure.py:33-37`) has no `os.replace`/`os.rename` alternative, so v1 records **no write at all**
  (`writes=0`), not a flagged-write that misses the expected literal.

Independent check that the fixtures are not one-sided: v2's own selftest on the same bytes passes every
planted expectation.

```
$ python3 tools/write-path-census-v2.py --selftest --fixtures .ufo/evidence/round-40/census/fixtures.json
WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
V2_SELFTEST_EXIT=0
```

So the control's 0/0/0 and v2's 1/1 demonstrate a real capability gap on the same fixture content.

## Falsification attempts

1. **Is the control constant-false by construction?** No. Swapping in v1-visible fixture content flips it.

   ```
   $ python3 …/measure.py --lane "$PWD" --fixtures /tmp/tameshi-r40-ExecControl/v1-visible.json --control
   C1_R40_CONTROL: v1_bytes_unflagged=1 v1_replace_writes=1 v1_replace_unflagged=1 C1_R40_CONTROL_PASS=true
   EXIT=0
   ```

   That scratch fixture uses `(out / 'case.expected').write_bytes(b'x')` and
   `(out / 'case.expected').write_text('x')`, i.e. forms v1 can see. The frozen PASS=false therefore comes
   from the frozen fixture composition, not from dead logic.

2. **Is the replace term load-bearing?** Yes. Bytes class made v1-visible, replace left as `os.replace`:

   ```
   $ python3 …/measure.py --lane "$PWD" --fixtures /tmp/tameshi-r40-ExecControl/half.json --control
   C1_R40_CONTROL: v1_bytes_unflagged=1 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false
   EXIT=1
   ```

3. **Does `--control` honour the revision?** No — it silently scores the worktree fixtures.

   ```
   $ python3 …/measure.py --lane "$PWD" --rev 304e3355705640af2879c772fc9a5c2902c61763 --control
   C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false
   EXIT=1
   ```

   Same line as the no-rev run. `main` dispatches to `control()` at `measure.py:114-116`, before any
   `git_show(..., rev, ...)`; `control()` opens `os.path.join(lane, FIXTURES)` (`measure.py:115`). At the
   base rev the fixtures blob does not exist (`git show 304e335:…/census/fixtures.json` →
   `fatal: path … exists on disk, but not in '304e335…'`, exit 128), yet control still returns the
   live-fixture verdict. The emitted control line also carries no `rev=` field, so the stored
   `control/v1-on-fixtures.*` artifact is rev-unbound. Control output cannot establish the base-rev claim;
   base false must be read off absence (see below).

4. **Predicate-shape caveat (not a C1 falsifier).** The contract's clause “embedded v1 patterns score …
   replace writes=0 on those two planted cases” is guaranteed by regex construction: v1 has no
   `os.replace` alternative, so *any* `os.replace` line yields `replace_writes=0`. Unlike the bytes class,
   the control cannot distinguish “v1 expected-regex miss” from “v1 write-regex blindness” for the replace
   class. C1's v2-side hits (`live_replace_v2`, and MT01's killed `os.replace` mutant) still carry that
   clause; only the control's attribution is coarser than the bytes case.

5. **Empty fixture file.** Malformed input is not a clean usage failure:

   ```
   $ python3 …/measure.py --lane "$PWD" --fixtures /tmp/tameshi-r40-ExecControl/empty.json --control
   KeyError: 'bytes_unflagged'   (measure.py:96)
   EXIT=1
   ```

   Robustness note only; exit stays non-zero.

## Baseline consistency (static checks, default mode not run)

- v1 pin intact: `sha256sum tools/write-path-census.py` =
  `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62`, equal to `claims.C1.v1_sha256` and
  to `git show HEAD:…`.
- v2 pin intact at `HEAD` (= freeze commit): `sha256sum` of the worktree file and of
  `git show HEAD:tools/write-path-census-v2.py` both =
  `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b`, equal to `claims.C1.tool_sha256`.
- Base rev `304e335`: v2 tool absent (`git show 304e335:tools/write-path-census-v2.py` exit 128) and
  fixtures absent (exit 128), so the default counter takes the `tool_absent=1` branch (`measure.py:120-130`)
  and emits `C1_R40_PASS=false`. That is inference from source + absence, not a default-mode run; the
  deciding run remains the L1's.

## Verdict

Control milestone met: the assigned line reproduces exactly (`v1_bytes_unflagged=0 v1_replace_writes=0
v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false`, exit 1), it matches the stored evidence byte-for-byte,
and the zeros are attributable to the two specific v1 gaps (`expected.json` literal not in
`V1_EXPECTED_RE`; `os.replace`/`os.rename` absent from `V1_WRITE_RE`). No predicate was rewritten.

## Risks / notes

- `--control` ignores `--rev` and does not hash the fixture blob; the control line is not self-binding.
  It should not be cited as evidence about base-rev state or about which fixture bytes were scored.
- Control PASS is reachable with v1-visible fixture content, so the false verdict's value depends on the
  frozen fixtures blob (`af2374…`), which currently matches at HEAD and worktree but is unchecked by the tool.
- Empty/malformed fixtures raise a traceback instead of a usage exit.
- No installs or updates performed; no lane file edited except this report.
