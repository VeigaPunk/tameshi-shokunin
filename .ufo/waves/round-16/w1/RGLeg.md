# RGLeg — C1 ledger plumbing: seventh regression leg `js-round-gate`

Seat: TameshiR16.RGLeg · wave 1 · date 2026-10-20

## Mid-flight retarget (L1 message)

L1 redirected this seat: do NOT edit `tools/mutate-and-run.sh` in place while
cold-read seats run it live; deliver the edited copy as a separate file. I had
already applied the leg edits to the live file, so I:

1. `cp tools/mutate-and-run.sh .ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh`
   (preserved the edited copy — sha256 `f91f7fa8cab3d4e1f0f8d0f31bee2f3837c635b22f11735971702f93a5194736`
   after subsequent fixes),
2. `git show HEAD:tools/mutate-and-run.sh > tools/mutate-and-run.sh` (restore),
3. verified restore: `sha256sum tools/mutate-and-run.sh` →
   `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, matching
   `git show HEAD:tools/mutate-and-run.sh | sha256sum` and the pin L1 stated
   (`75ed934d…`). `git status --porcelain tools/mutate-and-run.sh` → clean
   (empty output, exit 0).

Then I fixed three places where my in-place edits had dropped text, all in the
deliverable copy only: a lost "and parsed, and each recorded table's ids…"
clause (header :149-152), a lost "against its own spec, plus the exec-bit
mirror arms…" line (:152), and the usage() clause "immune to working-tree
drift; a missing repo/rev/blob or a pin mismatch is a SETUP refusal)" (:203-206).
Final `diff <(git show HEAD:tools/mutate-and-run.sh) RGLeg.mutate-and-run.sh`
shows ONLY the intended leg-7 changes — every existing leg is byte-identical.

## Files changed

- `.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh` (NEW, deliverable;
  sha256 `f91f7fa8cab3d4e1f0f8d0f31bee2f3837c635b22f11735971702f93a5194736`,
  based on HEAD blob sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`,
  last tool commit `606716f703f7699af458476a31fc78ddc9bf552c`).
- `tools/mutate-and-run.sh` — restored byte-exact to HEAD; NOT modified in the
  final state. L1 installs the deliverable after cold-reads finish.

## What the leg adds (all line numbers are in the deliverable file)

- :14-15 header provenance — r16 adds the seventh measured gate.
- :81 `r10-2 six legs; r16 seven` in the --regression header line.
- :91 ledger comment line, verbatim:
  `#   js-round-gate         kumitate-shokunin/scripts/round-gate.mjs    @@RG_KILLED@@/10 (@@RG_PCT@@ %)`
- :95-102 sources paragraph — adds arm-class-matrix.md §13 pre-registration;
  "All seven defect specs are embedded below".
- :149-152 selftest prose — r16 extends the embedded-ledger sweep to seven legs.
- :203-206 usage() leg list — `js-round-gate` appended.
- :546-548 `REV_*` comment block — notes leg 7's placeholder status.
- :562-563 `PIN_ROUNDGATE=f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`,
  `REV_ROUNDGATE=364f1d5954158ef8844bca4a5fef57b05d2f2ca5`.
- :570 `TABLE_ROUNDGATE='@@R16_ROUNDGATE_TABLE@@'`.
- :598 `regression_specs` header comment → "the seven embedded case specs".
- :900-906 `js-round-gate.spec` heredoc; body is the single line
  `@@R16_ROUNDGATE_SPEC@@` (quoted `<<'EOT'`, so the marker reaches the spec
  file literally).
- :909-910 `-s` spec-existence check extended with `js-round-gate.spec`.
- :1122 `REGRESSION_EXPECT` printf — `js-round-gate=%s/%s` appended; :1128-1129
  corresponding `table_count/table_total` args over `TABLE_ROUNDGATE`.
- :1131 `st_roundgate` added to the status locals.
- :1162-1166 `regression_case_git js-round-gate` call — target
  `kumitate-shokunin/scripts/round-gate.mjs`, suite `node "$MUTANT" --selftest`,
  workdir `$root/js-round-gate` (mirrors js-claims-check exactly).
- :1168-1169 `nlegs=7`; status loop includes `$st_roundgate`.
- :1591-1593 selftest leg-cut comment → "the seven embedded legs'".
- :1602 `st 'embedded leg specs: seven files written'`.
- :1610 `lent` entry `'js-round-gate:js-round-gate.spec:TABLE_ROUNDGATE:10:@@RG_KILLED@@'`.

## Placeholders for L1 substitution (the only `@@…@@` markers)

| Line | Marker | Substitute |
|------|--------|------------|
| 91 | `@@RG_KILLED@@` and `@@RG_PCT@@` | measured killed count (integer) / percent (integer) from the 10-mutant sweep |
| 570 | `@@R16_ROUNDGATE_TABLE@@` | measured table, e.g. `D1:KILLED,…,D10:…` — must round-trip through `table_count`/`table_total` (comma-separated `ID:VERDICT`, no spaces) |
| 905 | `@@R16_ROUNDGATE_SPEC@@` | the measured spec file body (may be multi-line; it is the whole heredoc body) |
| 1610 | `@@RG_KILLED@@` | same integer as :91 (selftest asserts `table_count TABLE_ROUNDGATE KILLED == this`) |

`grep -n '@@'` confirms exactly these four marker occurrences on three lines
(:91 carries two). No other `@@` tokens exist in the file.


## Evidence

- `bash -n .ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh` → exit 0 (two runs;
  pre-substitution syntax clean — the markers sit inside a comment, a quoted
  string, and a quoted heredoc, all parse-safe).
- `diff <(git show HEAD:tools/mutate-and-run.sh) RGLeg.mutate-and-run.sh` →
  25 hunks, all shown in-session; no hunk touches any existing leg's spec
  heredoc, table, pin, or call.
- Restore proof: `tools/mutate-and-run.sh` sha256 `75ed934d…c5` == HEAD blob.
- NOT RUN: `--selftest`, `--regression`, or any mutant run (forbidden
  mid-wave; L1 runs them after substitution). The pre-substitution file would
  selftest-fail anyway: `@@R16_ROUNDGATE_TABLE@@` yields `table_total=1,
  KILLED=0` against `lent`'s `10:@@RG_KILLED@@`, and the placeholder spec body
  has no `@defect` rows — this is by design and only resolves once L1
  substitutes real measured values.

## Recommendations (bounded)

1. Substitute markers before ANY selftest/regression run; re-run `bash -n`
   after substitution, then `bash … --selftest` (hermetic). The `lent` loop
   emits one `st` case per leg, so the recorded 60/60 grows to 61/61 with the
   new line `PASS embedded leg js-round-gate: spec and recorded table agree`.
2. `@@R16_ROUNDGATE_TABLE@@` must contain NO whitespace and exactly the spec's
   ids; `@@RG_KILLED@@` must be a bare integer (it feeds a `-eq` test).
3. The file's `VERSION` string still says `r10-2` — untouched per "keep
   existing legs byte-identical" scope; L1 may bump it at install time if
   round conventions require.
4. The `regression_specs` `-s` check will pass pre-substitution only because
   the placeholder line is non-empty; do not ship without substitution.

## Blockers

None.
