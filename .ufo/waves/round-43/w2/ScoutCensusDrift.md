# ScoutCensusDrift — census re-run vs recorded after.stdout (round 43, w2)

Item: run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
and diff against `.ufo/evidence/round-43/census-sources/after.stdout`;
report exit code, row count, any warning present in one and not the other.

Axis under attack: **freshness** of the recorded census receipt (does the evidence file still
describe the lane registry, and does it discriminate anything).

## Verdict

**No drift. No warning appears in one and not the other. The receipt is current and the
comparison is discriminating — but the receipt is degenerate: `after.stdout` is byte-identical
to `start.stdout`, to both round-42 receipts, and round 43 keeps no `after.exit`.**

## Reproduction (read-only)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tameshi > /tmp/now.stdout 2>/tmp/now.stderr
$ echo $?            # 0
$ wc -l /tmp/now.stdout   # 11
$ wc -c /tmp/now.stdout   # 1015
$ md5sum /tmp/now.stdout \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-43/census-sources/after.stdout
12d1004ffa553a5825bfb426f31f06f0  /tmp/now.stdout
12d1004ffa553a5825bfb426f31f06f0  .../census-sources/after.stdout
$ diff -u .../after.stdout /tmp/now.stdout ; echo $?   # 0
```

- **Exit code: 0** (clean-or-warnings; no `E` line). `stderr` empty.
- **Row count: 11 stdout lines** = 10 warning rows + 1 `ok` row. `validate` emits no row
  metric (as `w1/ScribeLessonGate.md:260` already recorded). The registry size is
  `114` rows, from `census` mode:
  `tameshi rows 114`, `tier.A 102 / tier.B 9 / tier.C 3 (invalid 0)`,
  `status.mined 86 / queued 22 / rejected 6`.
- **Warning-set diff: empty (0 lines).** 9×`W04` + 1×`W01`, in the same order:
  `after.stdout:1-8,10` W04 (S047, S048, S075, S076, S077, S078, S081, S092, S104),
  `after.stdout:9` W01 (S101, tierC mined with used-by), `after.stdout:11` `ok <path>`.
  All four warning codes' subjects exist in `corpus/SOURCES.md` (e.g. `corpus/SOURCES.md:56`
  S047, `:101` S092, `:109` S101, `:113` S104); no warning id is orphaned and the 104
  unwarned rows are silent as expected.

## Why the match is real, not vacuous (sensitivity control)

In a `git clone --shared` scratch copy of the lane, one registry row was mutated
(`S047` → `Queue777`, dropping the duplicated pitest.org URL):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /tmp/<clone>
# W04 count 9 -> 8, `W04 S047 ...` gone, exit still 0
```

So the counter does see registry text; byte-equality above is identity, not incapacity.
A scratch clone at committed HEAD reproduces the 10 warning lines verbatim; only the
lane-label field and the `ok` path move (see F2).

## Findings

**F1 — Receipt is current for the registry (observed, high confidence).**
`corpus/SOURCES.md` in the working tree is byte-identical to `HEAD` (`e20cf89`,
`git diff --stat HEAD -- corpus/SOURCES.md` → empty), to the freeze of record
(`git show 3aee2c0:corpus/SOURCES.md | cmp - corpus/SOURCES.md` → identical), and to
`c5335c70`'s content; sha256 `c50ca1fbce6b1afb769735793d2ca520d05e5e8a830fd3ea88a7c48fb4c961fd`.
Census script sha256 `3fb72615…`, tree-clean, last touched `2026-10-19` (`6a1dd8ce`), i.e.
older than both receipts; `shokunin.conf:55` (`tameshi|tameshi-shokunin|…`) unchanged since
`2026-10-19`. Nothing the receipt depends on has moved, so a null diff is the correct answer
rather than a stale file being re-validated against a stale snapshot.

**F2 — The last line is root-literal, so byte-identity is only reproducible at the same
`--root` (observed, high confidence).** `scripts/sources-census.sh:452-485` builds the roster
from `"$ROOT"/*-shokunin` without `realpath`, and `:745` emits `ok\t$f`. Running the same
registry through a symlinked root
(`--root /tmp/w2-probe`, `tameshi-shokunin ->` real lane) produced
`tameshi  ok  /tmp/w2-probe/tameshi-shokunin/corpus/SOURCES.md` and exit 0, with all 10
warning lines unchanged. Consequence for falsifiers: a re-run from a worktree/clone root
cannot be `cmp`-compared wholesale against `after.stdout`; normalise field 1 and drop/relabel
the `ok` line first. My own run used the exact literal `--root` from the item, so the diff is
legitimate.

**F3 — `after.stdout` carries no before/after signal (observed, high confidence).**
All four receipts hash alike:
sha256 `bb8c4162239efce3e0e798ed19c66d0949873269df53b638fc147c3d037af621` for
`round-42/{start,after}.stdout` and `round-43/{start,after}.stdout`; md5 `12d1004f…`;
1015 bytes, 11 lines, newline-terminated. So the round-43 `census-sources/` pair witnesses
only a steady state — it cannot show that anything changed between start and after, and it is
also identical to round 42's pair. This is *consistent* with the round's
`Assimilation: none` (the append is staged in
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`, not applied to
`corpus/SOURCES.md`), but a receipt named `after` that equals `start` should not be read as
evidence of an applied change.

**F4 — Round 43 dropped `after.exit` (observed, high confidence; minor).**
`ls .ufo/evidence/round-43/census-sources/` → `after.stdout`, `start.exit`, `start.stdout`.
Round 42 kept `after.exit` (contents: `0`). The after exit code is not witnessed in round 43;
it is only derivable from the absence of `E` lines (the tool's exit 0 on warnings-only is
pinned by selftest `W-only-registry-exit-0`). My re-run gives exit 0, matching the derivation.

**F5 — Date stability (observed, medium confidence = sampled).**
`--today 2026-10-25` and `--today 2026-10-26` both yield md5 `12d1004f…`. The registry's
latest `opened` is `2026-10-25`, so no `E08` (future-opened) can appear as the clock advances;
`validate` never reports `overdue`, so cadence dates cannot perturb this output either. The
receipt will stay byte-stable for the registry content it was taken from.

**F6 — mtime footprint above the receipt is a rewrite of identical bytes (observed).**
`corpus/SOURCES.md` mtime/ctime `2026-10-25 07:58:48 -0300` post-dates
`after.stdout` (`07:53:57`) yet the bytes equal `HEAD` and the freeze, and the fresh census
reproduces the receipt exactly. Read as a same-content rewrite by some process (checkout /
materialisation), not as registry drift; no lane writer is evidenced by the bytes.

## Unknowns

- Which process rewrote `corpus/SOURCES.md` at `07:58:48` with identical bytes (F6). Read-only
  lane bounds prevent tracking it down; no content consequence.
- Whether the absent `after.exit` was an intentional receipt-trimming decision or an
  oversight (F4). No document in `.ufo/evidence/round-43/` states it.

## Tooling

No installs or upgrades were made (pacman is paused host-wide; nothing here required a new
tool). Scratch used: one `git clone --shared` under
`/tmp/tameshi-r43-w2-ScoutCensusDrift-clone` plus `/tmp/w2-probe`, both deleted before return.
No counter was run at `c5335c70…`; lane checkout untouched (read-only); only this report was
written.
