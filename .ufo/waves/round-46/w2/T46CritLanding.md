seat: T46CritLanding
item: attacked `.ufo/evidence/round-46/deciding-run.sh` and the landing rule (QUALITY criterion 86) — the four mandated probes (a)–(d) plus the rc-handling and worktree-vs-REV reads the item asked for, each in a scratch clone of CONTENT `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`

Bounds kept: read-only on the lane checkout except this file; every scratch file under
`/tmp/tameshi-r46-T46CritLanding/`; `git clone -q --no-hardlinks` of the lane into
`/tmp/tameshi-r46-T46CritLanding/clone`, `checkout -q 6f2168e0…`,
`git -C /tmp/tameshi-r46-T46CritLanding/clone rev-parse --show-toplevel` → `/tmp/tameshi-r46-T46CritLanding/clone`
(verified before the first commit); every later git call names `-C /tmp/tameshi-r46-T46CritLanding/clone`; throwaway
identity `-c user.name=throwaway -c user.email=throwaway@example.invalid` used only with `git -C <clone>`;
`git reset --hard`/`git checkout`/`git add`/`git mv` only inside that clone; no git or jj command in the lane;
no pacman, nothing installed, no fetch performed by this seat.

## Method

- Step 0 was run **verbatim**: `sed -n '1,24p' …/.ufo/evidence/round-46/deciding-run.sh > /tmp/tameshi-r46-T46CritLanding/block0.sh`
  (shebang through the `COUNTER_SHA256` loop) and invoked as `bash block0.sh <clone> <rev> <outdir>`, i.e. the
  script's own `LANE REV OUT` arguments. The full script was **not** run (L1's, ~10 min).
- Every other step was reproduced as the single line the script contains, with the same variables, in the clone.
- One clean baseline and five probe revisions were committed in the clone (all on top of CONTENT):
  `7028c5b` cheat Z, `a0ac4fc` (b) harmless outside-frozen edit, `cf8d2e1` (b2) hardened-counter drift,
  `09d1530` (c) package copy replaced, `572b599` (d) admitted entry renamed, `1bd6274` (e) manifest-derived
  guard appended to a hardened counter. The clone is back at CONTENT (`git -C … reset --hard 6f2168e0…`, clean).

Baseline, clean worktree at CONTENT:

```
$ bash /tmp/tameshi-r46-T46CritLanding/block0.sh /tmp/tameshi-r46-T46CritLanding/clone 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 out/base
FROZEN_UNCHANGED=1 freeze=745a583181648cfc7f9c1b476cd1be7dc68f7433 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32
COUNTER_SHA256 calibration/measure.py ad5f85df21b1e3f01ff5922242900d0b3bba1a044c9ff19828ecf00ab1ce680a
COUNTER_SHA256 coverage/measure.py f8bfefdf6c08ce880c3f329018d946168dd022c50391d24551853326dbcfb5f5
COUNTER_SHA256 hardening/mutate.py 999e0a4b6e4725666d002130ada8dcad05f81d2fbaaefb4ba7ada4b1fd82ca66
block0_exit=0
```

Real `no-harm.sh` at CONTENT, run from the clone (50 s, exit 0, 404 B) — all six monitors ok:

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-117 120 ok
```

## Mandated probes

| probe | commit | observed | required | result |
|---|---|---|---|---|
| (a) cheat Z `total = 0 * (mism + unparsed + unobs)` in `calibration/measure.py`, committed | `7028c5b` | `FROZEN_UNCHANGED=0`, diff `.ufo/evidence/round-46/calibration/measure.py \| 2 +-`, `COUNTER_SHA256 calibration/measure.py 9bfd8918…` | `0` | **as required** |
| (b) harmless line appended to `selftest/c1-selftest.stdout` (outside the frozen list), committed | `a0ac4fc` | `FROZEN_UNCHANGED=1` | `1` | **as required** |
| (c) `assimilation/package/r9-false-red-rate.md` ground line replaced, committed | `09d1530` | `FROZEN_UNCHANGED=0`, diff `.ufo/evidence/round-46/assimilation/package/r9-false-red-rate.md \| 2 +-` | `0` | **as required** |
| (d) `corpus/knowledge/r5-undetected-flaky-failures.md` → `…-renamed.md` (`git mv` + README index + S259 `used-by`), committed; entry-name block run by hand | `572b599` | `ENTRY_NAMES_OK=0 got=[r5-undetected-flaky-failures-renamed.md r6-… r9-…] want=[r5-undetected-flaky-failures.md r6-… r9-…]` | `0` | **as required** |

Exact (d) block, as the script writes it (`E=.ufo/evidence/round-46`, `$OUT/c3.stdout` from the counter at `572b599`):

```
$ python3 .ufo/evidence/round-46/coverage/measure.py --lane $D --rev 572b599…   # exit 0
ENTRY corpus/knowledge/r5-undetected-flaky-failures-renamed.md
ENTRY corpus/knowledge/r6-flaky-failures-cluster.md
ENTRY corpus/knowledge/r9-false-red-rate.md
C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=572b599… C3_R46_PASS=true
```

So step 0 catches every *committed* edit to a frozen file, and step 3 catches a renamed entry **when the
worktree is clean**. Both statements are false once the worktree differs from REV, and step 0 cannot see the
C2 subject at all. Those are the findings.

## Findings

### 1. HIGH — step 3 compares REV entry names against the **worktree** package directory

What it attacks: `deciding-run.sh:29` `want=$(ls "$E/assimilation/package" | sort | tr '\n' ' ')` — the guard
added for CritC3Control Vd3. `names` comes from the counter at REV; `want` comes from whatever is on disk.

Command and output (clone, at `572b599`, where step 3 must refuse):

```
$ git -C $D checkout -q 572b599… && git -C $D mv .ufo/evidence/round-46/assimilation/package/r5-undetected-flaky-failures.md \
      .ufo/evidence/round-46/assimilation/package/r5-undetected-flaky-failures-renamed.md
$ git -C $D status --porcelain
R  .ufo/evidence/round-46/assimilation/package/r5-undetected-flaky-failures.md -> …-renamed.md
$ names=…; want=$(ls "$E/assimilation/package" | sort | tr '\n' ' ')
ENTRY_NAMES_OK=1 r5-undetected-flaky-failures-renamed.md r6-flaky-failures-cluster.md r9-false-red-rate.md
$ bash block0.sh $D 572b599… out/e4
FROZEN_UNCHANGED=1
```

The same read fails closed in the other direction: one untracked file in the package directory at a clean
CONTENT flips a correct check to `ENTRY_NAMES_OK=0 got=[r5-undetected-flaky-failures.md …] want=[extra-untracked.md r5-undetected-flaky-failures.md …]`
(observed). So the step is both forgeable and noisy, and `FROZEN_UNCHANGED` is blind to the forge because it is
tree-to-tree.

Impacted axes: coverage (C3's name-mapping guard), calibration (the deciding receipt's authority).
Smallest safe correction:

```
want=$(git -C "$LANE" ls-tree --name-only "$REV" -- "$E/assimilation/package" | sed 's#.*/##' | sort | tr '\n' ' ')
```

### 2. HIGH — step 1 executes the **worktree** `no-harm.sh` and its rc comes only from the substring `RED`

What it attacks: `deciding-run.sh:25`
`bash "$E/no-harm.sh" … > "$OUT/no-harm.stdout" 2>&1; cat …; grep -q RED … && rc=1`. The script is run from
`$E` = the checkout, not from REV, and no `no_harm.exit` is captured.

Command and output (clone at CONTENT, `no-harm.sh` replaced in the worktree by `#!/bin/bash` + `exit 2`, nothing
committed):

```
$ bash .ufo/evidence/round-46/no-harm.sh $D 6f2168e0… > out/no-harm.stdout 2>/dev/null; echo "no_harm_exit=$?"
no_harm_exit=2
$ wc -c < out/no-harm.stdout
0
$ rc=0; grep -q RED out/no-harm.stdout && rc=1; echo "step1_rc=$rc"
step1_rc=0
$ bash block0.sh $D 6f2168e0… out/e5c
FROZEN_UNCHANGED=1
$ git -C $D status --porcelain
 M .ufo/evidence/round-46/no-harm.sh
```

A no-harm step that did not run at all leaves the deciding run's `rc` untouched. The same hole covers any crash
before the first monitor line (missing file → bash exit 127, no `RED`), and any monitor whose failure text is not
the literal `RED`. The round-21 coldread counter the script invokes also has no self-pin
(`grep -n 'self_pin\|SELF_PATH\|open(os.path.abspath' .ufo/evidence/round-21/coldread/measure.py` → no matches), so
the `score=6` monitor's *script* is neither frozen nor pinned.

Impacted axes: calibration (no-harm gate), coverage (the gate that is supposed to bound C1's rows).
Smallest safe correction: run the script from REV (`git -C "$LANE" show "$REV:$E/no-harm.sh" > "$WORK/no-harm.sh"`)
and require its exit status:

```
bash "$WORK/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; nh=$?
echo "$nh" > "$OUT/no-harm.exit"; cat "$OUT/no-harm.stdout"
[ "$nh" = 0 ] || rc=1; grep -q RED "$OUT/no-harm.stdout" && rc=1
```

### 3. HIGH — the C2 subject files are outside the frozen pathspec, are absent at FREEZE, and no receipt records their bytes

What it attacks: the landing rule itself. Step 0 diffs `FREEZE..REV` over `$FROZEN`, whose `hardening/` entries are
`mutate.py` and `mutants.json` only. The two files C2 is *about* are not there, and cannot be:

```
$ git ls-tree -r --name-only 745a5831… -- .ufo/evidence/round-46/hardening/
.ufo/evidence/round-46/hardening/build-manifest.py
.ufo/evidence/round-46/hardening/mutants.json
.ufo/evidence/round-46/hardening/mutate.py
```

They enter at `a6892b196f923efbed242ce9ea599a3f745b2138` (wave-1 evidence), i.e. after the freeze, so a
`FREEZE..REV` diff can never bind them. Digests at CONTENT (for the L1 to compare at landing):
`hardening/freshness-counter.py f2a8ec0fc3e08be1f439527cab8abfe6607353e91e22a1ca9277e010c623c507`,
`hardening/coverage-counter.py 200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9`.
`frozen.stdout` prints digests for `calibration/measure.py`, `coverage/measure.py` and `hardening/mutate.py` — the
driver and the other two counters, never the two artifacts under mutation.

Command and output (clone, a 6-line manifest-derived guard appended to the hardened counter and committed):

```
$ git -C $D diff --stat 6f2168e0… 1bd6274… -- .ufo/evidence/round-46/hardening/freshness-counter.py
 .ufo/evidence/round-46/hardening/freshness-counter.py | 6 ++++++
$ bash block0.sh $D 1bd6274… out/e2c
FROZEN_UNCHANGED=1
$ python3 .ufo/evidence/round-46/hardening/freshness-counter.py --selftest | tail -2
C1_R45_SELFTEST: cases=34 failed=0
VERDICT: PASS
```

with `mutate.py`'s own `judge()` (imported from the clone) on that mutant: CONTENT source → `('F01','killed','VERDICT: FAIL')`,
edited source → `('F01','killed','')` — the mutant now dies on the guard's `sys.exit(1)` *before any selftest case
runs*. Neutral `FN1` stays `survived` on both. Boundary of this finding, stated honestly: all 25 declared mutants
already die behaviorally at CONTENT (my own seat check with `mutate.judge`, 25 s: 15/15 freshness + 10/10 coverage
killed, `FN1-3`/`CN1-3` survived), so **I did not produce a C2 verdict change**; what is demonstrated is that the
mechanism which converts a behavioural kill into a byte-pattern match is available in one unpinned file, with
step 0 green and the counter's own selftest still 34/34. A gutted selftest plus that guard would keep
`pristine=1`, `neutral_killed=0` and `equivalence=1` (the equivalence run compares the *measure* output at
`ea25e022…`, not the selftest) — [INFERENCE], not built.

Impacted axes: operability (C2), calibration (the receipt's provenance).
Smallest safe correction: make the receipt name the bytes it scored, and make the drift check able to see them —

```
for f in hardening/freshness-counter.py hardening/coverage-counter.py; do
  echo "C2_SUBJECT_SHA256 $f $(git -C "$LANE" show "$REV:$E/$f" | sha256sum | cut -c1-64)"; done
git -C "$LANE" diff --stat a6892b196f923efbed242ce9ea599a3f745b2138 "$REV" -- "$E/hardening/freshness-counter.py" "$E/hardening/coverage-counter.py"
```

(the second line must be empty, or its diff must be cited in the verdict record).

### 4. MEDIUM — the C3 fresh-quote requirement is waived when the entry basename has no package copy, so step 3 is the only guard and finding 1 defeats it

What it attacks: `coverage/measure.py` `entry_ok()` —
`if package_text is None or quote not in fold(package_text): fresh = True`. Deleting or renaming the package copy
(which is what a renamed entry does) makes `package_text is None`, so **any** located quote counts as fresh.

Command and output (clone at `572b599`, the renamed-entry commit of probe (d), no package copy for that basename):

```
C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=572b599… C3_R46_PASS=true
```

C3 passes with an entry that carries no quote absent from a package copy — the clause the contract states. The
counter's own T22/CTL_B shape (CritC3Control Vd2a/Vd5) is bypassed by renaming, and the only check that notices is
step 3, which finding 1 shows is a worktree read. Impacted axes: coverage.
Smallest safe correction (counter, frozen — recommendation only): refuse an entry whose basename is not the frozen
package basename for the document its `source:` line cites (`assimilation/package/<basename>` must exist at REV),
i.e. replace the `package_text is None or …` waiver with `package_text is None → refuse`.

### 5. LOW — step 0 is tree-to-tree and the `COUNTER_SHA256` lines are printed, never compared

What it attacks: `deciding-run.sh:22-24`. An uncommitted edit to a counter leaves `FROZEN_UNCHANGED=1` **and**
prints the clean REV digest in the same receipt — the line a reader would cite as provenance.

Command and output (clone at CONTENT, cheat Z applied but not committed):

```
$ git -C $D status --porcelain
 M .ufo/evidence/round-46/calibration/measure.py
$ bash block0.sh $D 6f2168e0… out/wt-cheat
FROZEN_UNCHANGED=1 freeze=745a5831… rev=6f2168e0…
COUNTER_SHA256 calibration/measure.py ad5f85df21b1e3f01ff5922242900d0b3bba1a044c9ff19828ecf00ab1ce680a
block0_exit=0
```

Consequence is bounded, not a pass: the three counters self-pin their running bytes against the REV blob
(`calibration/measure.py:180-182`, `coverage/measure.py:155`, `hardening/mutate.py:105`), so this cheat would report
`self_pin=0 … C1_R46_PASS=false` and exit 1 ([INFERENCE] for the counter run; I did not run C1 with a dirty
worktree). The defect is the receipt line, not the verdict. Smallest safe correction: add
`[ -z "$(git -C "$LANE" status --porcelain -- $FROZEN)" ] || { echo WORKTREE_DIRTY=1; rc=1; }` to step 0, and compare
each printed digest with a constant (they are stable: `ad5f85df…`, `f8bfefdf…`, `999e0a4b…`).

### 6. LOW — criterion 86's own landing check is not part of the deciding artifacts

Criterion 86 requires `git diff --name-only C..tip` to list receipt paths only. `deciding-run.sh` enforces
`FREEZE..C` drift (step 0) and writes receipts into `$OUT`, but nothing in the run, the receipt set or the script
records the `C..tip` listing — the script cannot, since the tip does not exist yet, and no seat in
`.ufo/waves/round-46/spec-w2.json` owns it. The L1's verdict record must therefore carry that listing or criterion 86
is asserted, not checked. Smallest safe correction: optional 5th argument `TIP`; when given,
`git -C "$LANE" diff --name-only "$REV" "$TIP" | grep -v "^$OUT/"` must be empty, else `rc=1`.

### 7. INFO — `assimilation/guard-map.json` is not in the frozen pathspec and nothing in the deciding path reads it

It exists at FREEZE (`745a583`), so the check is available, but C3's "adopted at guard-admitted ids S258/S259/S260"
clause is carried only by the counter's `row_ids` print (CritC3Control Vh shows any `S\d{3,}` id passes). An edit to
`guard-map.json` between FREEZE and CONTENT is invisible to step 0 and changes no counter output.
Smallest safe correction: add `$E/assimilation/guard-map.json` to `$FROZEN` and assert
`row_ids=S258,S259,S260` from `$OUT/c3.stdout`.

### 8. INFO — the deciding script itself carries no digest in its own receipt

`deciding-run.sh` enters at `e630ae7` (after the freeze), sha256 at CONTENT
`9f26160ab9673249c59aa9ae05c20267e2445c09081bef3b9d7786d58649a318`. A reader of `frozen.stdout` cannot tell which
script produced the receipts. Smallest safe correction: `echo "SELF_SHA256 $(sha256sum "$0" | cut -c1-64)"` into
`$OUT/frozen.stdout`.

## Verified sound (checked, not findings)

- **Exit-code trust is sound.** All three counters return nonzero on a false verdict
  (`calibration/measure.py:234`, `coverage/measure.py:181`, `hardening/mutate.py:159`: `return 0 if passed else 1`),
  so steps 2 and 4 reading `$?` instead of the PASS token loses nothing.
- **Committed post-freeze edits to frozen files are caught**, with the offending path in the receipt: probes (a) and
  (c) both printed `FROZEN_UNCHANGED=0` plus a one-line `git diff --stat`.
- **The three counters self-pin the worktree copy to the REV blob** (lines above), so a dirty worktree cannot turn a
  counter green — it can only make it red.
- **Step 3's parse of `$OUT/c3.stdout` is sound** for the shapes the counter emits: `ENTRY <path>` and
  `ENTRY <path> (not indexed)` both reduce to the basename; `REFUSED`/`C3_R46:` lines do not match `^ENTRY `.
- **Step 4's `rm -rf "$WORK"` before C1** means the counter's "`--work` must be empty or absent" guard cannot fire
  spuriously; an empty 4th argument makes C1 return 2 → `rc=1` (fails closed).
- **C3 at CONTENT is green in a clean clone**: `C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3
  row_ids=S258,S259,S260 … C3_R46_PASS=true`, exit 0, 0.29 s (seat check, not the verdict).

## Unrun

- No full `deciding-run.sh` run (L1's; ~10 min) and no C1/C2 deciding-equivalent run: probe (a) was scored by step 0
  only, as the item instructs.
- No census (`scripts/sources-census.sh validate`) and no `control/run-controls.py` run — outside this item.
- No gutted-selftest C2 pass built (finding 3's verdict-change boundary is [INFERENCE], stated as such).
- The counters were not run with a dirty worktree (finding 5's `self_pin=0` consequence is read from source, not observed).

## Tooling

Nothing installed or upgraded: no pacman transaction (host-wide pause respected), no uv/npx/cargo install, no network
access performed by this seat. Only the `python3` (3.14) and `git` already present were used.
