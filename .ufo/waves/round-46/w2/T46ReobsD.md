seat: T46ReobsD
item: C1 independent re-observation at the CONTENT revision `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` of `effective expectation reconciliation`, `retained invocation-context gate`, `hermetic env-differential probe`, with effective-expectation reconciliation of the restated rows, the retained invocation-context gate re-run, and a hermetic env-differential probe of the three frozen commands

# T46ReobsD — C1 re-observation at CONTENT (round 46, wave 2)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; CONTENT `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`;
base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`; freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`.
I did not write the standing rows and I did not write wave 1's observations. Read-only on the lane except this
report; every scratch file under `/tmp/tameshi-r46-T46ReobsD/`. No tool installed, upgraded or removed
(§9); no `pacman`; no git mutation in the lane.

## Result in one line

All three statements **MATCH** at CONTENT (`SELFTEST: PASS (66/66)|0|39ee5c5effd9`,
`SELFTEST: PASS (49/49)|0|7e4519d9a0ea`, `ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23`), the committed
evidence cells are byte-identical to the rows `emit_row()` produces from my own independent observation, and
none of the three printed values drifted from wave 1. **But none of the three is hermetic**, and one of them is
not even a function of REV: `retained invocation-context gate`'s exit 0 is gated by a hard-coded
out-of-lane census tool run against the **live fleet root** (§7.1, HIGH), and the other two lose their stated
value when `jj` / `bwrap` are absent from `PATH` (§7.2, §7.3, HIGH).

## 1. Setup (exact commands and output)

```
W=/tmp/tameshi-r46-T46ReobsD; rm -rf $W; mkdir -p $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
```

```
clone=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 mirror=6f2168e028ce7ff6e82ac92093ac05dd1f147c32
21                       # ls $W/fleet | wc -l  → 20 sibling symlinks + the tameshi-shokunin mirror dir
```

Statements pin re-derived by this seat, not trusted:

```
$ sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/calibration/statements.json
a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9
```

equals `contract.json:claims.C1.statements_sha256` and `measure.py:STATEMENTS_SHA256` (printed by my harness:
`stmts_pin_local a15a8b45…46e9`).

## 2. Method

`/tmp/tameshi-r46-T46ReobsD/run3.py` imports the counter by path
(`.ufo/evidence/round-46/calibration/measure.py` of the lane), reuses its
`env()` (every `GIT_*` dropped, `PYTHONDONTWRITEBYTECODE=1`), its `pick_line()` and its
`{work}`/`{clone}`/`{rev}` substitution verbatim, runs each of the three frozen `argv` **once** with
`cwd=$W/clone` and `REV=6f2168e0…`, and derives the sha prefix with `git -C $W/clone show HEAD:<sha_file>`
exactly as `observe()` does. Claimed values were read with the counter's own helpers from the **CONTENT**
blob, never the worktree:

```
rev_sc = git -C LANE show 6f2168e0…:SCORECARD.md ; rows = m.last_rows(rev_sc) ; m.claim_of(s, rows[(kind,id)])
```

The three rows `last_rows` returns are SCORECARD.md lines **2182 / 2183 / 2184** (round-46 block, header
`| Capability | What it can now do | Evidence pointer | First-working round |`); the stale round-31 rows at
lines 1520-1522 and the dated rows at 246-248 are earlier in file order and are superseded by last-row-wins.

## 3. Per-statement result (the item's core table)

`claimed` = `claim_of(stmt, rows[(kind,id)])` at CONTENT; `observed` = picked line | exit | tool sha256 prefix.

| id | claimed | observed | verdict |
|---|---|---|---|
| effective expectation reconciliation | `SELFTEST: PASS (66/66)` \| 0 \| `39ee5c5effd9` | `SELFTEST: PASS (66/66)` \| 0 \| `39ee5c5effd9` | **MATCH** |
| retained invocation-context gate | `SELFTEST: PASS (49/49)` \| 0 \| `7e4519d9a0ea` | `SELFTEST: PASS (49/49)` \| 0 \| `7e4519d9a0ea` | **MATCH** |
| hermetic env-differential probe | `ENVDIFF_SELFTEST: 9/9 pass` \| 0 \| `e8b47ab7cf23` | `ENVDIFF_SELFTEST: 9/9 pass` \| 0 \| `e8b47ab7cf23` | **MATCH** |

Raw harness output (one run each, `obs` regex matches in parentheses):

```
STATEMENT cap/effective expectation reconciliation: claimed=SELFTEST: PASS (66/66)|0|39ee5c5effd9 observed=SELFTEST: PASS (66/66)|0|39ee5c5effd9 (exit=0, secs=8.40, obs_matches=1) MATCH
STATEMENT cap/retained invocation-context gate: claimed=SELFTEST: PASS (49/49)|0|7e4519d9a0ea observed=SELFTEST: PASS (49/49)|0|7e4519d9a0ea (exit=0, secs=1.97, obs_matches=1) MATCH
STATEMENT cap/hermetic env-differential probe: claimed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 observed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 (exit=0, secs=0.23, obs_matches=1) MATCH
```

Tool sha256 prefixes, two independent derivations (git blob at REV and the checkout bytes; the clone is clean,
so they must agree — they do):

```
$ for f in tools/evidence-disposition.py .ufo/evidence/round-15/verify.py tools/env-diff.py; do git -C $W/clone show HEAD:$f | sha256sum | cut -c1-12; done
39ee5c5effd9
7e4519d9a0ea
e8b47ab7cf23
$ for f in …; do sha256sum $f | cut -c1-12; done        # in $W/clone
39ee5c5effd9
7e4519d9a0ea
e8b47ab7cf23
```

Each `obs` regex matched exactly one line (`obs_matches=1`), every command exited 0, and none approached its
`timeout` (8.40 s / 900, 1.97 s / 900, 0.23 s / 900).

## 4. Effective-expectation reconciliation — the committed cells are exactly what the observation implies

I re-emitted each row with the counter's own `emit_row(stmt, observed, committed_cells)` from **my** observed
tuples and compared against the committed line (the `EMIT_CAP | ` print prefix swapped for `| `):

```
effective expectation reconciliation | byte-identical after prefix swap: True
retained invocation-context gate    | byte-identical after prefix swap: True
hermetic env-differential probe     | byte-identical after prefix swap: True
```

The row's backticked command text is also the frozen `argv` for all three (`argv_text_in_row: True`), so a
reader who pastes the row's command runs the statement:

```
effective expectation reconciliation  cmd_text == ' '.join(argv)   python3 tools/evidence-disposition.py --selftest
retained invocation-context gate     cmd_text == ' '.join(argv)   python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72
hermetic env-differential probe      cmd_text == ' '.join(argv)   python3 tools/env-diff.py --selftest
```

Nothing to reconcile: claimed == observed == emitted for all three.

## 5. The restated rows' `What` and `First-working round` cells

| id | `What` — does it still describe the capability? | `First-working round` |
|---|---|---|
| effective expectation reconciliation | **Yes.** The three clauses map to named selftest cases: "account for every historical expected row" → `missing-row-drop`, `unknown-row`, `duplicate-row-name`; "reject an exit-only setup crash" → `exit-only-false-positive`, `unsuperseded-crash-mismatch`; "preserve that raw failure under a checked explicit oracle supersession" → `superseded-raw-missing`, `superseded-raw-binding`, `superseded-oracle-binding`, `supersession-unwarranted`, `superseded-unexplained-reason`. The tool registers 62 named `case`/`historical_case` calls (52 + 10, counted by AST) plus further `record()` checks (the identity-guard and usage-class loops and `argv-never-executed`) for the printed 66/66. | `round 14` — matches the tool's first-add commit `0c6e36d 2026-10-20 round-14: reconcile effective expectations and retain invocation context`. Accurate. |
| retained invocation-context gate | **Partly.** The receipt clauses are real (docstring steps 1/4 pin and digest-verify the two round-14 receipts; step 7 produces frozen clean 0 / missing-env 1 / tampered 2 / usage 64), and my run printed those PASS lines. But the cell omits the thing that decides the exit code: a fleet-wide census leg outside the lane (§7.1). What it states is true of the receipt checks and silent about the gate on exit 0. | `round 15` — matches `0494c24 2026-10-20 round-15: integrate context gate falsifiers and registry`. Accurate. |
| hermetic env-differential probe | **Not proved by the frozen command.** The cell says the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable". I verified the receipt independently: 9 surfaces, `invariant`×8, `nondeterministic`×1 and that one is `js-round-gate`, `raw-output-variable` count 0 — **the cell is factually correct**. But `env-diff.py --selftest` never opens that receipt (`grep -n "receipt-initial\|f5/" tools/env-diff.py` → no match); its 9 cases are six synthetic probe scripts (`invariant`, `tz`, `locale`, `home`, `columns`, `repeat`) plus `missing-bwrap`, `timeout`, `pin-mismatch-public-cli`. So the cell describes the tool's main mode and cites an artifact the frozen command does not read (finding F4). The statement id's word "hermetic" is also not supported by the selftest, which needs `bwrap` (§7.3). | `round 21` — matches `370f2df 2026-10-21 round-21: kill 18 old guard mutants and add finite F5 environment differential`. Accurate. |

No `What` cell overstates the *number* it prints; the overstatements are of scope (§7.1, §7.4).

## 6. Differences from wave 1's observation (ExecStmt04, at the freeze `745a583`)

1. **Verdict, all three: UNPARSED → MATCH.** Wave 1 read `claimed=-` (the round-31 prose cells at lines
   1520-1522 carry no `→ \`value\`, exit N` grammar); I read the round-46 cells at 2182-2184. That is the
   restatement working, and the observed tuples are unchanged — the claim did not move, the row did.
2. **Observed values: no difference.** Wave 1 (run 1 and run 2) and the L1's `before/c1-at-freeze.stdout`
   lines 7-9 record exactly the tuples I observed at CONTENT. Nothing drifted between freeze and CONTENT.
3. **Probe count without `bwrap`: 1/9 (wave 1) vs 1/9 and 2/9 (mine).** Not a contradiction: with my minimal
   shim (no `node`, no `bwrap`) I reproduce wave 1's `1/9`; with a full `/usr/bin` minus `bwrap` shim I get
   `2/9` because the extra pass is `pin-mismatch-public-cli`, whose child CLI needs `node`. The tool is
   unchanged (`e8b47ab7cf23` both times); the shim contents differ. Recorded so the two numbers are not read
   as a drift.
4. **Wall time only:** `effective expectation reconciliation` 8.40 s here vs 3.24 s in wave 1 (first-run
   fixture creation); the printed tally is identical.

## 7. Hermetic env-differential probe of the three frozen commands (seat-added, beyond the item's one run)

`/tmp/tameshi-r46-T46ReobsD/probe.py`. Profiles, each a full `env -i` construction except P0:
**P0** = the counter's `env()` (inherited minus `GIT_*`, `REV` set — this is the claim observation of §3);
**P1** = `PATH=/usr/bin:/bin HOME=/nonexistent TMPDIR=… LANG=C LC_ALL=C TZ=UTC`;
**P2** = P1 + `LANG/LC_ALL=en_US.UTF-8 TZ=Pacific/Chatham COLUMNS=20 LINES=5 TERM=dumb
PYTHONPATH=/nonexistent GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent`;
**P3** = a minimal shim of 53 symlinks (python3, git, bash, coreutils, jq, `awk` — no `gawk`, no `jj`, no
`bwrap`, no `node`); **P4** = every `/usr/bin` entry except `bwrap` (so `node`, `gawk`, no `bwrap`); **P5** = P1 + a
one-entry shim holding `jj`.

| statement | P0 (claim) | P1 | P2 | P3 minimal shim | P4 no-bwrap | P5 +jj |
|---|---|---|---|---|---|---|
| effective expectation reconciliation | `PASS (66/66)` 0 | **`FAIL (3/66 …)` 1** | **`FAIL (3/66 …)` 1** | **`FAIL (3/66 …)` 1** | **`FAIL (3/66 …)` 1** | `PASS (66/66)` 0 |
| retained invocation-context gate | `PASS (49/49)` 0 | `PASS (49/49)` 0 | `PASS (49/49)` 0 | `PASS (49/49)` **1** | `PASS (49/49)` 0 | `PASS (49/49)` 0 |
| hermetic env-differential probe | `9/9 pass` 0 | `9/9 pass` 0 | `9/9 pass` 0 | **`1/9 pass` 1** | **`2/9 pass` 1** | `9/9 pass` 0 |

### 7.1 Finding F1 — HIGH — `retained invocation-context gate`: exit 0 is gated by live, out-of-lane, unpinned state

Attacked: the restated row `| retained invocation-context gate | … exit 0, tool sha256 \`7e4519d9a0ea\` |`
(SCORECARD.md:2183) and the C1 claim that its exit code is what the frozen command prints at REV.

`verify.py` runs, after all the pinned checks, a census leg on **absolute paths outside the lane**:

```
.ufo/evidence/round-15/verify.py:105   CENSUS_TOOL = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
.ufo/evidence/round-15/verify.py:835   census_argv = [CENSUS_TOOL, "validate", "--root",
.ufo/evidence/round-15/verify.py:836                  "/home/vgpnk/Projects/shokunin", "tameshi"]
.ufo/evidence/round-15/verify.py:840   any(line.startswith("tameshi\tok\t") for line in census_stdout.splitlines())
```

Running exactly that argv (read-only; the tool's header says "Read-only: parses shokunin.conf LANES rows
textually … writes only stdout or --out"):

```
$ env -i PATH=/usr/bin:/bin HOME=/nonexistent LANG=C LC_ALL=C TZ=UTC \
    /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url … (11 W04/W01 warning lines)
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

So the exit code depends on the **live lane worktree's `corpus/SOURCES.md`**, not on REV and not on the clone.
The tool's own header fixes the semantics: `exit: 0 clean or warnings · 1 E/overdue findings (or census
missing)`. I demonstrated both branches with a scratch fleet root (no fleet write):

```
$ …/sources-census.sh validate --root /tmp/tameshi-r46-T46ReobsD/fakeroot tameshi        # one row status=watch
tameshi	E07	S002 status=watch
EXIT=1
$ …/sources-census.sh validate --root /tmp/tameshi-r46-T46ReobsD/fakeroot/clean tameshi  # same rows, valid status
tameshi	ok	/tmp/tameshi-r46-T46ReobsD/fakeroot/clean/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

And a failing census leg flips `verify.py`'s exit while the picked line stays identical — observed under P3,
where the census leg failed for a different reason (missing `gawk` in my shim):

```
sources-census: FAIL exit=2 (expected 0)
sources-census-ok-line: FAIL ok line absent
… (all other checks PASS, including `selftest-new-full-count` printing SELFTEST: PASS (49/49))
EXIT=1
```

Consequences: (a) the counter would record `SELFTEST: PASS (49/49) | 1 | 7e4519d9a0ea` → **MISMATCH** and
`C1_R46_PASS=false`, with no byte changed at REV; (b) the census tool is **not pinned** by the statement —
`grep -c "sources-census.sh" verify.py` → 1 (the constant only), so editing
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (sha256
`3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, outside the lane) changes the observed
exit silently; (c) the deciding run is a race with any wave-2 or later write to the live
`tameshi-shokunin/corpus/SOURCES.md` that introduces an E code. It does not falsify C1 at this moment (I
observed exit 0), but the row's `exit 0` is not a function of REV alone.

### 7.2 Finding F2 — HIGH — `effective expectation reconciliation` needs `jj` on `PATH`; the row does not say so

Attacked: the restated row `| effective expectation reconciliation | … SELFTEST: PASS (66/66), exit 0, tool
sha256 \`39ee5c5effd9\` |` (SCORECARD.md:2182).

```
$ cd $W/clone && env -i PATH=$W/nojj HOME=/nonexistent TMPDIR=$W/ptmp LANG=C LC_ALL=C TZ=UTC \
    python3 tools/evidence-disposition.py --selftest
SELFTEST: FAIL (3/66 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.k027rs_d)
EXIT=1
$ env -i PATH=/usr/bin:/bin:$W/withjj … python3 tools/evidence-disposition.py --selftest
SELFTEST: PASS (66/66)
EXIT=0
```

The differentiator is `jj` alone (P1 and P2 both fail identically; adding only a `jj` symlink to the minimal
`PATH` restores 66/66 with `HOME=/nonexistent`). The dependency is documented in the tool's own docstring
(`tools/evidence-disposition.py:121`, "Selftest also requires `jj` for its isolated colocated-repository
cases.") but not in the row. On a host without `jj` the picked line no longer matches
`^(SELFTEST: PASS \(\d+/\d+\))`, so the statement degrades from MATCH to **UNOBSERVABLE** and `total` grows by
one. This is a precondition of the standing value; the row states the value without it.

### 7.3 Finding F3 — HIGH — `hermetic env-differential probe` needs `bwrap` (selftest) and `node` (main mode)

Attacked: the restated row `| hermetic env-differential probe | … ENVDIFF_SELFTEST: 9/9 pass, exit 0, tool
sha256 \`e8b47ab7cf23\` |` (SCORECARD.md:2184).

```
$ cd $W/clone && env -i PATH=$W/nobwrap HOME=/nonexistent TMPDIR=$W/ptmp LANG=C LC_ALL=C TZ=UTC \
    python3 tools/env-diff.py --selftest
ENVDIFF_CASE invariant FAIL
… (tz, locale, home, columns, repeat FAIL; timeout FAIL)
ENVDIFF_CASE missing-bwrap PASS
ENVDIFF_CASE pin-mismatch-public-cli PASS
ENVDIFF_SELFTEST: 2/9 pass
EXIT=1
```

With the 53-link minimal shim (no `node`, no `bwrap`, no `gawk`) it is `ENVDIFF_SELFTEST: 1/9 pass`, EXIT=1. `execute()`
(`tools/env-diff.py:57-60`) returns `BWRAP_UNAVAILABLE` when `shutil.which("bwrap")` is empty, and the case
literally named `missing-bwrap` (`:161-162`) passes only because it is given an explicit nonexistent `bwrap=`
path that bypasses the guard — so the one case that names the missing dependency cannot fail when the
dependency is missing. The printed line still matches the `obs` regex, so the counter records a **MISMATCH**
(`1/9`/`2/9` ≠ `9/9`), not an unobservable.

Main mode has a second undeclared dependency: `tools/env-diff.py:234-237` probes `node --version` and
`bash --version` after building the report but before writing it, inside the `try` whose handler prints
`ENVDIFF_SETUP` and returns 2:

```
$ env -i PATH=$W/nojj … python3 clone/tools/env-diff.py --contract $W/contract.json --out $W/ptmp/out.json --fleet-root $W/fleet
ENVDIFF_SETUP: [Errno 2] No such file or directory: 'node'
EXIT=2
no receipt written
```

A bash-only contract therefore produces **no receipt at all** on a host without `node`. Not on the frozen
command's path (which is `--selftest`), but it is part of the capability the `What` cell describes.

### 7.4 Finding F4 — LOW — the env-diff `What` cell cites a receipt the frozen command never reads

`grep -n "receipt-initial\|f5/" tools/env-diff.py` → no match; `selftest()` (`:143-195`) is nine synthetic
cases. The cell's factual assertion is nevertheless **true** (I verified the receipt: 9 surfaces, 8
`invariant`, 1 `nondeterministic` = `js-round-gate`, zero `raw-output-variable`), so this is a scope
overstatement, not a false statement: the C1 evidence cell proves the classifier on fixtures, not the
classification of the committed nine pinned selftests.

### 7.5 Finding F5 — INFO — the context-gate statement is REV-invariant except for the tool hash

The frozen `argv` pins `--rev 7650fe4db89f3a706aed63d048ac47e02289cc72` (round 15); `REV` only reaches it as an
unused environment variable. So the statement re-runs a fixed historical verification; the only REV-dependent
part of the claim is the tool sha256 prefix (`7e4519d9a0ea`, which I re-derived). The row is honest about the
rev it names, but "the value the statement prints at REV" is, for this statement, a constant plus a hash.

### 7.6 Finding F6 — INFO — `verify.py` is not side-effect-free

Each run creates `attempt-N/` and `verification-N.json` in the tree it runs from (the counter's throwaway clone
absorbs it; wave 1 recorded the same). Harmless for C1 (fresh clone per run, exclusive-create naming), recorded
because a deciding run's `--work` clone is not left pristine.

## 8. Retained evidence

All under `/tmp/tameshi-r46-T46ReobsD/`:

- `clone/` (REV `6f2168e0…`, detached), `fleet/` (20 sibling symlinks + `tameshi-shokunin` mirror at REV).
- `run3.py` (one observation per statement), `results.json` (claimed/observed/verdict/exit/secs/matches/argv).
- `raw/{effective-expectation-reconciliation,retained-invocation-context-gate,hermetic-env-differential-probe}.{stdout,stderr}`
  — full streams of the claim runs.
- `reconcile.py` (emit_row round-trip, cmd_text↔argv, claim_of), `probe.py` (P1-P5), `raw/verify-P3.{out,err}`,
  `raw/census-{P1,P3}.err`, `raw/census-scratchroot.out`, `contract.json`, `fakeroot/` (clean and E07 registry
  fixtures), `nobwrap/`, `nojj/`, `withjj/` shims.

## 9. Tooling record

Nothing installed, upgraded or removed; `pacman` untouched (host-wide pause respected). Pre-existing tools used:
Python 3.14.8, git 2.56.0, jj 0.45.1 (`/home/vgpnk/.local/bin/jj`), bubblewrap 0.13.1 (`/usr/bin/bwrap`),
node (`/usr/bin/node`), gawk (`/usr/bin/gawk`).

## 10. Bounds compliance

- Lane: read-only except this report. No `statements.json`, counter, SCORECARD, tool or receipt edited; no
  `git add/commit/stash/checkout/switch/reset/pull/push` and no `jj` command in the lane. The only git
  mutations were `git clone` / `git checkout --detach` inside `/tmp/tameshi-r46-T46ReobsD/`.
- `/home/vgpnk/Projects/shokuknow` never touched; the fleet repo `/home/vgpnk/Projects/shokunin` only read (the
  census argv in §7.1 is read-only by the tool's own contract).
- All scratch under `/tmp/tameshi-r46-T46ReobsD/`; no fixture repository was created, so the
  `git -C "$D" rev-parse --show-toplevel` rule did not apply to anything this seat ran.

## 11. Risks and blockers for the L1's deciding run

1. **F1 is the one to watch.** Take the deciding run while the live
   `tameshi-shokunin/corpus/SOURCES.md` is free of E findings (it is `ok` as of this report: warnings only,
   exit 0) and do not let a concurrent write land between the census leg and the counter's comparison; a
   census E code turns statement 8 into MISMATCH with nothing changed at REV.
2. **F2/F3 are host preconditions, not defects in the numbers.** The deciding run must inherit the host
   environment (`jj` on `PATH`, `bwrap` on `PATH`); never `env -i`. On this host both resolve, which is why
   all three MATCH.
3. No blocker in this seat's scope: all three statements are observable, single-line, in-timeout, byte-identical
   to the rows the counter would emit, and agree with wave 1's observation and with
   `before/c1-at-freeze.stdout` lines 7-9. Nothing in my three falsifies C1.
