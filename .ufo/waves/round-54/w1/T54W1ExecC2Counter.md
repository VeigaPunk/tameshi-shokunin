# T54W1ExecC2Counter — C2 verify (frozen counter), round 54

Seat `T54W1ExecC2Counter` (executor, operability), lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Every run below is at `--rev` = C0 `59c38109bf119d0e9d4f878644a82babc937bc1e` (40 chars, derived with
`git rev-parse 59c3810`, never retyped). Counter bytes are pinned by sha256: the round amended the C2 counter twice while
this seat ran, so each line names the exact bytes it executed. Raw output: `…/w1/T54W1ExecC2Counter-receipts/`.

## 0. Answer

**The currently freeze-pinned counter passes at C0.** Bytes sha256 `8528ee85…` (freeze.json pin = HEAD blob = worktree; it
became the pin at HEAD `fe70474`, the round-54 "amendment 4" revision, and is still the pin at HEAD `077d431`) print:

```
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
EXIT=0
```

No arm is short. `sources=3`, not the brief's `sources=1`: the counter counts *each* cited-and-mined S id, and C0 cites
S277, S278 and S279 (§5), so 3 is correct and not a shortfall.

**The bytes frozen when the wave opened do not pass reliably.** At the seat's start the pin was `b4684a3f…`; five runs of
those exact bytes at C0 gave **4 × `usable_ok=6` / `C2_R54_PASS=false` / exit 1** and **1 × `usable_ok=7` / pass**. The failing
arm and tool:

```
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
```

Amendments 2 and 4 of this round address exactly that (`freeze.json` amendments[]; commits `19c7558`/`097985c`/`fe70474`),
and with them the arm is stable at 7/7 here (§4).

**One instrument defect stands, independent of any arm:** an unresolvable `--rev` exits 1 with a Python traceback instead of
the counter's documented `exit 2` setup error (§6 O1).

## 1. Every run, with its bytes

| # | when (UTC) | counter sha256 (first 8) | role | verdict | exit |
|---|---|---|---|---|---|
| A | 14:28–14:30 | `b4684a3f` | original freeze pin | `usable_ok=6` … `PASS=false` | 1 |
| B | 14:33–14:41 | `b4684a3f` | repeat | `usable_ok=6` … `PASS=false` | 1 |
| C | 14:47:20 | `49280fe5` | amendment 2 | `usable_ok=7` … `PASS=true` | 0 |
| D | 14:55:51 | `b4684a3f` | original pin, quiet host | `usable_ok=7` … `PASS=true` | 0 |
| E | 14:56:36 | `b4684a3f` | repeat | `usable_ok=6` … `PASS=false` | 1 |
| F | 14:59:24 | `b4684a3f` | repeat | `usable_ok=6` … `PASS=false` | 1 |
| G | 15:04:53 | `49280fe5` | amendment 2, HEAD `4e2de73` | `usable_ok=7` … `PASS=true` | 0 |
| H | 15:07:46 | `8528ee85` | amendment 4, HEAD `fe70474` | `usable_ok=7` … `PASS=true` | 0 |
| I | 15:10:48 | `8528ee85` | **authoritative**: a byte copy of the pin (`copy sha == FREEZE_PIN`), HEAD `fe70474` | `usable_ok=7` … `PASS=true` | 0 |

Runs A/B were not teed; their verdict lines are quoted from the tool output, identical to each other, and the two
registry-check strace logs are preserved as `counter-strace-registry-check.log` and
`counter-run-B-strace-registry-check.log`. Runs C–I are teed with the executed sha256 (and, from G on, the HEAD) recorded
beside the output; run I is the authoritative one because the executed bytes were a copy whose sha256 was checked against
`freeze.json`'s pin in the same command.

So the same *frozen* bytes at the same revision produced both `PASS=false` and `PASS=true` (D vs A/B/E/F). That is not a tree
property, and §4 shows what it is.

## 2. Independent hand reproduction — unusable arm, `registry-check`

Clone at C0 (`git clone --shared` into scratch; `git -C <clone> rev-parse --show-toplevel` printed the clone, HEAD printed
`59c38109bf119d0e9d4f878644a82babc937bc1e`):

```
$ cd <clone-at-C0>
$ env TMPDIR=/nonexistent-x54 PYTHONDONTWRITEBYTECODE=1 python3 tools/registry-check.py --selftest
EXIT=2
--- stdout ---   (empty, 0 lines)
--- stderr ---   (1 line)
registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-x54' (could-not-evaluate)

occurrences of 'could-not-evaluate' ........ stdout 0, stderr 1
occurrences of 'Traceback (most recent call last)' ... stdout 0, stderr 0
```

Files: `…-receipts/hand-unusable-registry-check.stdout` (empty), `…-receipts/hand-unusable-registry-check.stderr` (that line).

The counter's own reading of the same arm and tool, from a failing run above — both pasted as the item asks:

```
EXPLAIN unusable registry-check rc=2 line='registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory'
```

They agree: exit 2, exactly one naming line, the TMPDIR value named, no traceback.

## 3. All seven tools × all three arms, by hand

`env TMPDIR=… python3 <tool> <selftest arg>` inside the C0 clone; cell = exit code:

| tool | unusable `/nonexistent-x54` | empty `TMPDIR=""` | usable fresh dir |
|---|---|---|---|
| registry-check | 2 (1 naming line, 0 tracebacks) | 0 | 0 |
| env-diff | 2 (1/0) | 0 | 0 |
| bash-witness-study | 2 (1/0) | 0 | 0 |
| evidence-disposition | 2 (1/0) | 0 | 0 |
| pin-disposition | 2 (1/0) | 0 | 0 |
| context-capture | 2 (1/0) | 0 | 0 |
| repeat-control | 2 (1/0) | 0 | 0 |

Matches the counter's `unusable_exit2=7 naming=7 empty_ok=7` on every run, including the failing ones — the flip was confined
to the strace arm, for `registry-check` only.

## 4. Why the pre-amendment strace arm flipped

The frozen arm read `usable_ok += (proc.returncode == 0 and hits == 0)` where `proc` was
`strace -f -e trace=mkdir,mkdirat … python3 <tool> <selftest>`. `tools/registry-check.py`'s own self-test asserts a wall-clock
bound on two process-group escape cases — `tools/registry-check.py:1223` at C0: `and elapsed < 3.5`. Under trace those cases
take 4.5–12.8 s here:

```
SELFTEST_CASE timeout-kills-setsid-pipe  FAIL (exit=1 elapsed=4.784s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=4.596s survivor=False marker=False)
SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)
   (second clone) 4.527s / 4.711s        (cold cache, later) 11.563s / 12.792s
```

The same tool, same clone, **without** strace:

```
timeout-kills-setsid-pipe PASS elapsed=1.701s ; timeout-kills-setpgid-pipe PASS elapsed=1.701s ; SELFTEST: PASS (51 cases)  rc=0
run 2:                        2.033s / 2.037s                     SELFTEST: PASS (51 cases)  rc=0
```

In every traced failure `survivor=False marker=False` — the kill the case exists to prove *did* happen; only the clock failed.
And the `/tmp` census is zero, checked with a regex of my own, not the counter's (`mkdir(|mkdirat(` followed by `"/tmp`), so
the result does not depend on the amended census regex:

```
mkdir/mkdirat lines in the counter's registry-check strace log: 238
of those, paths under /tmp:                                    0
```

So the traced rc was measuring ptrace overhead (strace 7.2, Python 3.14.8), which is precisely what `freeze.json`
amendment 2 says it fixes. **Residual margin, worth knowing for the deciding run:** the amendment takes the rc from the plain
run, but the plain run still carries registry-check's own `elapsed < 3.5` assertion, and the measured plain values at C0 are
1.70 s and 2.03 s — about 1.5 s of headroom on a host running >100 concurrent seats. That is the remaining load sensitivity,
not a fault in either the tool's contract or the counter's predicate.

## 5. The other arms, and what I opened to check them

- **docs=7** — `tools/registry.json` at C0, the seven `*selftest` rows. Every `scratch_root` cell is the same text and
  contains all three required tokens (`TMPDIR`, `empty`, `could-not-evaluate`):
  `"TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)"`.
- **note=1** — `corpus/knowledge/scratch-root-contract.md` at C0: three-arm table, the S278 `:163-165` quote
  (`if dirname: dirlist.append(dirname)`), the S277 quote, the S279 search-list sentence, and the paragraph naming the
  counter's own blind spot.
- **sources=3** — `corpus/SOURCES.md` rows S277/S278/S279 are `mined`, each with
  `corpus/knowledge/scratch-root-contract.md` in its used-by cell, each with a located quote and `2026-10-28`;
  `corpus/lessons/round-54.md` `## Gate` names all three ids with `2026-10-28` and an `https://` URL.
- The C2 "before" receipt now exists and is committed: `.ufo/evidence/round-54/before/c2.stdout` is 1307 B at HEAD and ends
  `C2_R54: rev=d33053f7552d … usable_ok=7 … total=13 C2_R54_PASS=false` — i.e. at base the original pin read `usable_ok=7`,
  consistent with §4's load dependence rather than with a tree difference (`tools/registry-check.py` is byte-identical at base
  and C0, sha256 `ade15cc0…`).

## 6. Instrument observations (report-only; I changed nothing)

**O1 — an unresolvable `--rev` exits 1 with a traceback, not the documented setup exit 2.** `measure.py:96` resolves the rev
through `git(..., check=True)`, outside the `Setup` handler, so any bad or non-existent rev escapes as
`subprocess.CalledProcessError`. Deliberate receipt:

```
$ python3 .ufo/evidence/round-54/c2/measure.py --lane $PWD --rev deadbeef00 --work <empty> --explain
Traceback (most recent call last):
  ...
  File ".../c2/measure.py", line 96, in main
    rev = git(['rev-parse', '--verify', '%s^{commit}' % a.rev], lane).stdout.decode().strip()
subprocess.CalledProcessError: Command '['git', ..., 'rev-parse', '--verify', 'deadbeef00^{commit}']' returned non-zero exit status 128.
EXIT=1
```
Its docstring promises "2 on setup error" and `main()`'s `except Setup` prints `C2_R54: error=… total=1 C2_R54_PASS=false`;
neither happens. A `check=False` plus `raise Setup(...)` on that one call would make the promise true.
(`…-receipts/counter-unresolvable-rev.txt`, and the accidental reproduction in
`…-receipts/counter-F1-unresolvable-rev-39char-literal.txt`.)

**O2 — my own error, recorded so nobody chases it.** I typed the C0 id once as 39 characters
(`…a82babc937c1e`, missing the `b` of `…937bc1e`). Git rejected it correctly; I first read that rejection as an object-store
flap and was about to report a lane defect. The byte comparison settled it:

```
$ printf '%s' "…a82babc937c1e" | od -c | tail -1      -> 0000047 (39 bytes)
$ printf '%s' "$(git rev-parse 59c3810)" | od -c …    -> 0000050 (40 bytes), ends 'b c 1 e'
prefix 7..40 of the real id -> every length resolves to commit
```
**No lane defect exists there**; the store resolved C0 on every occasion I checked it with a correct id
(`git rev-list --all | grep -c '^59c38109'` → `1`, and `git cat-file -p` printed C0's tree and its parent `441c26be`).
Every measurement reported above uses the derived 40-char id.

**O3 — the freeze gate needs the current re-freeze commit, not `441c26be`.** `deciding-run.sh` refuses with
`FROZEN_UNCHANGED=0` (and forces `rc=1`) when the FROZEN paths differ between its FREEZE argument and REV. At the tip I
checked, with FREEZE = the original freeze commit the wave brief carries:

```
$ git diff --stat 441c26be HEAD -- .ufo/evidence/round-54/{contract.json,freeze.json,c1/measure.py,c1/lost-headings-at-base.json,c2/measure.py,no-harm.sh,deciding-run.sh,control/controls.sh}
 .ufo/evidence/round-54/c1/measure.py   | 19 ++++++++++------
 .ufo/evidence/round-54/c2/measure.py   | 26 +++++++++++++++-------
 .ufo/evidence/round-54/contract.json   | 40 +++++++++++++++++++++++++++++-----
 .ufo/evidence/round-54/deciding-run.sh | 31 ++++++++++++++++++++++++++
 .ufo/evidence/round-54/freeze.json     | 39 +++++++++++++++++++++++++++------
 5 files changed, 128 insertions(+), 27 deletions(-)
```
(HEAD `077d431` at the time of the check.)
This is round bookkeeping, not a C2 arm, but the deciding invocation must pass the freeze commit that already contains
amendments 1–4 (or the gate reconciled), otherwise a passing C2 verdict will not survive `deciding-run.sh`.

**O4 — the C2 counter changed twice under this seat** (`49280fe5` amendment 2, then `8528ee85` amendment 4, "the /tmp census
regex now matches plain mkdir( as well as mkdirat("). Both amendments are real fixes to real defects I measured, and the
counter now passes; but a reader of the round record must quote the sha with any C2 verdict, because "PASS=false" and
"PASS=true" are both true statements about C0 depending on which pin is meant.

## 7. Bounds, tooling, cleanup

- Written: this report and `.ufo/waves/round-54/w1/T54W1ExecC2Counter-receipts/`. No lane file was edited; the counter,
  registry, contract, freeze, ledger and wave spec are untouched; no mutating git/jj command was run anywhere (clones were
  `git clone --shared` into scratch, checkouts only, `rev-parse --show-toplevel` asserted before use).
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1ExecC2Counter/`, removed at the end of the seat (the receipts needed are in
  the lane's w1 dir, not there).
- Tools installed or upgraded: none (none was needed; host pacman is paused regardless).
- Census: round-start/end duty of the L1, not this seat.
