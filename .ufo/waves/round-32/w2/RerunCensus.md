# RerunCensus — round-32 wave 2 (operability: census re-run)

Seat: `TameshiR32.RerunCensus`. L1: `TameshiR32`. Item: `RerunCensus` in
`.ufo/evidence/round-32/w2-items.json`. Claim under test: **C1 (operability, capability
acquisition)**; this seat measured the census surface only.

Scope note: nothing in the lane was edited by this seat. All experiments ran in
`/fast/scratch/hyaku/tameshi-r32-seats/RerunCensus/` (four throwaway clones of the lane,
never the live tree). The live lane was read and one read-only command was run there as
assigned; `git status --porcelain` in the lane shows only the L1's own wave-2 files.

---

## Verdict (first)

1. **The fleet-wide census (contract v1) is clean and byte-identical to the round-32
   baseline.** Exact command run, full output pasted in §1, exit **0**. Same 8 W04
   warnings, same `ok` line, `diff` against
   `.ufo/evidence/round-32/before/census-start.stdout` is **empty (identical)**. No new
   warning, no new error on the fleet surface.

2. **The lane's own census v2 fails at the measurement revision `a4f7181`.** Row count
   **96**; verdict **`SOURCES_CENSUS: VIOLATIONS`**, exit **1**. Exactly one new
   violation, introduced by the round-32 content revision itself:

   ```
   == B2 id-or-path cite (must print nothing)
   no-id-or-path-cite: S099 tools/tally-audit.py ()
   ```

3. **Cause.** The new `S099` row (`corpus/SOURCES.md:107`, added at `a4f7181`) lists
   `tools/tally-audit.py` in its used-by cell, but that file carries **no `S099` cite**
   (0 occurrences of `S099` or `pitest`), and the H4 path-token fallback is empty for
   this row because the source cell's URL ends in `/` — so the used-by claim is
   unsupportable as written. The sibling row `S097` names the same file and *does* pass,
   because the tool cites `S097` at `tools/tally-audit.py:21`.

4. **Smallest safe correction: one cell — remove `tools/tally-audit.py` from `S099`'s
   used-by, keeping `corpus/knowledge/runner-tally-audit.md`** (which cites `S099` three
   times and therefore still passes). Verified in a scratch clone (§6): census v2 →
   `SOURCES_CENSUS: CLEAN`, exit 0; the lane's registered gate row `sources-census`
   returns to *held* (held=46/49, back to its pre-round-32 value); the tool and runner
   digests are untouched; cold-read credit is unchanged (63/64 → 63/64, §7).

5. **C1's measurement is unaffected by this.** `.ufo/evidence/round-32/v2/c1-measure-v2.py`
   contains **0** references to `SOURCES` or `census`; the C1 predicate pins only the
   tool bytes, the runner bytes, and the copy set. This is a lane-gate regression, not a
   C1 predicate failure. The tool's frozen sha256 `9639c458…99ef` and the runner's
   `a7d3f2dd…2eb9` are both intact at `a4f7181` and at the current lane HEAD `4b529ee`.

---

## 1. Fleet census — exact command, full output, exit

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

stderr was 0 bytes. Exit code **0**.

## 2. Comparison with the round-32 baseline

```
$ diff -u tameshi-shokunin/.ufo/evidence/round-32/before/census-start.stdout \
        /fast/scratch/hyaku/tameshi-r32-seats/RerunCensus/fleet-census.stdout && echo IDENTICAL_TO_BASELINE
IDENTICAL_TO_BASELINE
```

**No new warning and no new error.** The baseline (`before/census-start.stdout`, exit
file `census-start.exit` = `0`) and the run above are byte-for-byte the same: the same
8 W04 duplicate-URL warnings (S047, S048, S075, S076, S077, S078, S081, S092) and the
same `ok` line. Contract v1 does not implement the H4 id-or-path block, so it cannot
see the defect in §3 — that is exactly why §3 exists as a separate lane gate.

Fleet row counts at the measurement revision (contract v1 `census` mode, read-only):

```
tameshi	rows	96
tameshi	tier.A	87   tier.B	7   tier.C	2
tameshi	status.mined	68   status.queued	22   status.rejected	6
FLEET	missing	0
```

## 3. Lane census v2 in the clone at `a4f7181` — row count and verdict

Clone (own scratch dir, no shared objects, no hardlinks):

```
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r32-seats/RerunCensus/c
$ git -C /fast/scratch/hyaku/tameshi-r32-seats/RerunCensus/c checkout -q --detach \
    a4f718138bdad20de741faeca57891645e5a64d9
$ git -C .../c rev-parse HEAD
a4f718138bdad20de741faeca57891645e5a64d9
```

Full run of `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` from the clone root:

```
== A rows
96
== A malformed (must be 0)
0
== A tiers
A=87 B=7 C=2
== A status
mined=68 queued=22 rejected=6
== A dup ids (must print nothing)
== A enum/tier-inflation (must print nothing)
== A mined used-by missing (must print nothing)
== B1 strict id-cite (informational)
no-id-cite: S031 corpus/knowledge/arm-class-matrix.md
no-id-cite: S031 corpus/knowledge/fleet-suite-census.md
no-id-cite: S031 corpus/knowledge/mutation-case-mado-verify.md
no-id-cite: S031 corpus/knowledge/self-hardening-r6.md
no-id-cite: S031 corpus/knowledge/fleet-kill-rate-ledger.md
no-id-cite: S031 corpus/knowledge/mutation-case-kumitate-claims.md
no-id-cite: S031 corpus/knowledge/mutation-case-kagi-checklist.md
no-id-cite: S031 corpus/knowledge/service-limits.md
no-id-cite: S031 corpus/knowledge/service-standing-state.md
no-id-cite: S031 corpus/knowledge/operator-runbook.md
no-id-cite: S031 corpus/knowledge/closeout-r11.md
no-id-cite: S031 corpus/lessons/round-10.md
no-id-cite: S032 corpus/knowledge/mutation-case-kimi-census.md
no-id-cite: S032 corpus/knowledge/executor-test-sufficiency.md
no-id-cite: S032 corpus/knowledge/arm-class-matrix.md
no-id-cite: S033 corpus/knowledge/mutation-case-kagi-census.md
no-id-cite: S033 corpus/knowledge/arm-class-matrix.md
no-id-cite: S034 corpus/knowledge/fleet-suite-census.md
no-id-cite: S034 corpus/knowledge/mutation-case-tsukuroi-census.md
no-id-cite: S034 corpus/knowledge/fleet-kill-rate-ledger.md
no-id-cite: S034 corpus/knowledge/service-optin-protocol.md
no-id-cite: S035 corpus/knowledge/fleet-suite-census.md
no-id-cite: S035 corpus/knowledge/mutation-case-mado-verify.md
no-id-cite: S036 corpus/knowledge/mutation-case-kagi-checklist.md
no-id-cite: S037 corpus/knowledge/mutation-case-kumitate-claims.md
no-id-cite: S099 tools/tally-audit.py
count=26
== B2 id-or-path cite (must print nothing)
no-id-or-path-cite: S099 tools/tally-audit.py ()
== VERDICT
SOURCES_CENSUS: VIOLATIONS
EXIT=1
```

**Row count: 96. Verdict: `SOURCES_CENSUS: VIOLATIONS`, exit 1.** B1 (informational)
count rose 25 → 26 because of the same S099 pair; B2 (gated) rose 0 → 1.

The same verdict reproduces at the current lane HEAD and in the live lane:

```
$ git -C .../c-head checkout --detach 4b529ee && bash .ufo/evidence/kaika-round-1/sources-census-v2.sh | tail -4
no-id-or-path-cite: S099 tools/tally-audit.py ()
== VERDICT
SOURCES_CENSUS: VIOLATIONS
EXIT=1
```

## 4. Root cause

`corpus/SOURCES.md:107` (added by the round-32 content revision `a4f7181`):

```
| S099 | PIT Mutation Testing — https://pitest.org/ | docs | A | ... | mined | 2026-10-23 | 180d |
       tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md |
```

The H4 B2 rule (`.ufo/evidence/kaika-round-1/sources-census-v2.sh`, the `no-id-or-path-cite`
loop) requires, for each mined row and each used-by path, that the file contain **the row
id**, or else the **source path token** (the last `/`-segment of the source cell after the
` — ` prefix is stripped):

```
b=${s##*/}; grep -qF "$i" "$p" || { [ -n "$b" ] && grep -qF "$b" "$p"; } || echo "no-id-or-path-cite: $i $p ($b)"
```

For `S099` the source cell is `PIT Mutation Testing — https://pitest.org/`, so the
stripped token is `https://pitest.org/` and `b=${s##*/}` is the **empty string** — hence
the empty `()` in the diagnostic, and no path fallback exists. The id fallback also
fails:

```
$ grep -ciE 'pitest|S099' tools/tally-audit.py   → 0
$ grep -c  'S099' corpus/knowledge/runner-tally-audit.md → 3
$ grep -c  'S097' tools/tally-audit.py               → 1   (tools/tally-audit.py:21)
```

So `S099`'s used-by cell claims a consumer that carries no trace of the source, while
`S097` — same file, same commit — passes because the tool does cite `S097` at
`tools/tally-audit.py:21` (`status 0..255 at the first leg (bash exit statuses are
0..255; S097)`).

Only two mined rows name a `tools/` file in used-by, and only these two exist:

```
$ awk -F'|' '$9 ~ /mined/ && $12 ~ /tools\//' corpus/SOURCES.md
S097  tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md
S099  tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md
```

Both rows were added by `a4f7181` (`git show a4f7181 -- corpus/SOURCES.md` → 14
insertions, 1 deletion; `S097`/`S099` absent at `2da841b` and at the base `e24688b2`).

**This is a round-32 regression, not a pre-existing condition.** Census v2 at the
pre-content revision and at the base is CLEAN:

| revision | rows | census v2 | exit |
|---|---|---|---|
| `e24688b2` (base) | 94 | `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | 0 |
| `528f8dee` (tool freeze, before content) | 94 | `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | 0 |
| `2da841b` (round-31 content) | 94 | `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | 0 |
| **`a4f7181` (round-32 content = measurement revision)** | **96** | **`SOURCES_CENSUS: VIOLATIONS`** | **1** |
| `4b529ee` (lane HEAD) | 96 | `SOURCES_CENSUS: VIOLATIONS` | 1 |

The census-v2 script itself is unchanged (`sha256 b9b754713c9c359823e85106e0177e6678bd95b567d1c897fd7f3464945a2bc3`,
matching the sha recorded in `.ufo/evidence/round-12/EvidenceScribe/inventory.md:26`).

## 5. Blast radius — which registered lane gate regressed

`tools/registry.json:571` registers the gate row `sources-census`:

```json
{"name": "sources-census", "kind": "gate",
 "argv": ["bash", ".ufo/evidence/kaika-round-1/sources-census-v2.sh"],
 "expect": {"exit": 0, "stdout_contains": ["SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)"]},
 "status": "active", "tags": ["baseline"]}
```

Full `tools/registry-check.py` runs in throwaway clones (same tool, same registry
sha256 `c1b75366…1b73c`, one row per revision):

| revision | held | differing rows |
|---|---|---|
| `528f8dee` (pre-content) | **46/49** | `mutate-and-run-regression`, `round21-measure-selftest`, `mte-interop-check` |
| `a4f7181` (measurement revision) | **45/49** | the same three **+ `sources-census`** |
| `a4f7181` + the fix of §6 | **46/49** | the same three (pre-existing; they fail in a clone for environment reasons — they touch the live fleet root — and are not round-32's doing) |

Verbatim, on the measurement revision:

```
ROW mutate-and-run-regression expect=0 got=2 differs
ROW sources-census expect=0 got=1 differs
ROW round21-measure-selftest expect=0 got=1 differs
ROW mte-interop-check expect=0 got=2 differs
REGISTRY_CHECK: held=45/49 superseded=7
```

and after the §6 fix, the `sources-census` line is gone:

```
ROW mutate-and-run-regression expect=0 got=2 differs
ROW round21-measure-selftest expect=0 got=1 differs
ROW mte-interop-check expect=0 got=2 differs
REGISTRY_CHECK: held=46/49 superseded=7
```

So the round-32 content revision cost the lane exactly **one** registered gate row, and
the fix restores it exactly.

## 6. The smallest safe correction

**Change one cell of `corpus/SOURCES.md` — drop `tools/tally-audit.py` from `S099`'s
used-by.** The row keeps `corpus/knowledge/runner-tally-audit.md`, which cites `S099`
three times, so the row stays a mined, supported row and the registry keeps an honest
consumer for the PIT source.

```
-| S099 | … | mined | 2026-10-23 | 180d | tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md |
+| S099 | … | mined | 2026-10-23 | 180d | corpus/knowledge/runner-tally-audit.md |
```

Verified in a scratch clone (`c-fix`), no other file touched:

```
$ bash .ufo/evidence/kaika-round-1/sources-census-v2.sh | tail -4
== B2 id-or-path cite (must print nothing)
== VERDICT
SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)
EXIT=0

$ python3 tools/registry-check.py --root <c-fix> --only sources-census
ROW sources-census expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
EXIT=0

$ sha256sum tools/tally-audit.py tools/mutate-and-run.sh
9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef  tools/tally-audit.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh
```

Both digests are unchanged — the tool still matches `TOOL_SHA256` in
`.ufo/evidence/round-32/v2/c1-measure-v2.py:66`, and the runner still matches
`PINNED_RUNNER_SHA`. The fleet census on the fixed file is also unchanged (same 8 W04 +
`ok`, exit 0).

### Why the alternative correction is worse

The other way to satisfy B2 is to put an `S099` cite into `tools/tally-audit.py`. That
must **not** be done: the tool bytes are frozen and pinned — counter v2's `TOOL_SHA256`
is `9639c458…99ef`, and the C1 predicate requires *REV's* `tools/tally-audit.py` to have
exactly that sha256 (`c1-measure-v2.py:18,66,358`). Editing the tool would move the
measured object's pinned identity after data, which is precisely the judgment the L1
already had to make once (amendment 2, `.ufo/evidence/round-32/v2/contract-amendment-2.json`).
The registry-side one-cell edit is strictly smaller and touches no measured byte.

### Why not a third option

Changing `S099`'s status to `queued` would also silence B2 but would drop the registry's
claim that the PIT source was mined and used, and would shift the status histogram
(mined 68→67). Larger and less truthful than the one-cell edit.

## 7. Cold-read credit impact of the correction (measured, not assumed)

The fix edits `corpus/SOURCES.md`, a widely-read input, so its drift cost was measured
rather than guessed. Control and treatment are the same clone family, the same wave-2
ledger (493 entries, `4b529ee:.ufo/evidence/round-21/coldread/ledger.json`), and the
same wave-2 trace files (66 present at `4b529ee`):

```
$ python3 .ufo/evidence/round-18/measure.py --repo . --rev 4b529ee \
      --ledger-rev 4b529ee:.ufo/evidence/round-21/coldread/ledger.json      # control
covered 63 of 64   restraint 6
uncovered: ['### Round-21 gate/probe registry — finite environment differential']

$ … --rev <fix revision 9ece0fa> --ledger-rev 4b529ee:…                    # treatment
covered 63 of 64   restraint 6
uncovered: ['### Round-21 gate/probe registry — finite environment differential']
```

**Identical: the one-cell fix costs zero cold-read credit.** The mechanism is the
section-credit rule (a section is credited when *at least one* entry bound to it still
verifies every recorded input): the wave-2 entries that did record `corpus/SOURCES.md`
(`ColdA02` §4, `ColdB02` §4/§5) go stale at the fix revision, but sibling entries for
the same sections that did not record it (`ColdC01` §4, `ColdA03`/`ColdC02` §5) still
credit them.

The single uncovered section, `### Round-21 gate/probe registry — finite environment
differential`, is uncovered **before** the fix as well; it is pre-existing and unrelated
(its reason is `input-drift:.ufo/evidence/round-21/coldread/ledger.json`).

For reference, the L1's recorded content monitor at `a4f7181`
(`.ufo/evidence/round-32/content-monitor-a4f71813.json`) reads `covered 59/64` with 5
uncovered headings; that receipt predates the wave-2 ledger append (commit `4b529ee`),
which is why the post-wave-2 state measures 63/64.

## 8. Also observed (not this seat's to change)

- The standing capability row `SCORECARD.md:1514` (`### Current standing capabilities —
  re-stated at round 31`) claims `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh`
  → *exit 0, 94 rows, `SOURCES_CENSUS: CLEAN`*. At the measurement revision the same
  command prints **96 rows** and **`VIOLATIONS`, exit 1**. The standing row's row-count
  and verdict are both stale at `a4f7181`. Flagged for the L1 / `ReviewScorecardLog`;
  this seat did not edit SCORECARD.md.
- `corpus/SOURCES.md` sha256: `56838b80…c3d8` at `a4f7181`; `37f51b61…92f1` after the
  §6 fix.

---

## Files changed by this seat

**None in the lane.** This seat wrote only this report
(`.ufo/waves/round-32/w2/RerunCensus.md`) and files under its own scratch directory
`/fast/scratch/hyaku/tameshi-r32-seats/RerunCensus/` (four clones + captured outputs,
942 MB, all removable). The lane working tree was not modified; `git status --porcelain`
there shows only the L1's own wave-1/wave-2 files.

## Risks and blockers

- **The correction is the L1's to land.** It edits `corpus/SOURCES.md`, a widely-read
  input, at/after the measurement revision. §7 measures the credit cost as zero, but the
  L1 should land it *before* the first full v2 counter run so the measurement revision
  and the census verdict agree, and should re-run the content monitor at the landing
  revision to confirm 63/64.
- **The three other differing registry rows** (`mutate-and-run-regression`,
  `round21-measure-selftest`, `mte-interop-check`) fail at `528f8dee` as well as at
  `a4f7181`, so they pre-date round 32 and are outside this item. They fail in a clone
  because their argv points at the live fleet root.
- **Do not edit `tools/tally-audit.py`** to satisfy B2 (§6, "Why the alternative
  correction is worse"): its sha256 is pinned by counter v2 and by the C1 predicate.
- No blockers: every command required by the item was run and its output captured.

## Tools installed

None. No package, binary, or tool was installed or upgraded by this seat; the work used
only `git`, `bash`, `python3`, `awk`, `grep`, `sha256sum`, `diff`, and the lane's own
`tools/registry-check.py` / `.ufo/evidence/round-18/measure.py`. No host service was
restarted, no `pacman` transaction was attempted (the host-wide pacman guard is paused).
