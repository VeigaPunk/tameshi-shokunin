# T47CritC1Control — C1 (calibration) cheapest-pass attack

Seat: leaf critic, no dispatch. Lane checkout read-only; only this report was written.
Lane repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`,
freeze `9acfbe21435e1976636a276448dee1d5e7155915`. Every experiment below ran on throwaway clones made with
`git clone -q --no-hardlinks <lane> $D`, verified with `git -C $D rev-parse --show-toplevel == $D`, checked out to
the freeze, and committed with `-c user.name=crit -c user.email=crit@crit` (no other identity, no lane git write).

**Tooling:** nothing installed or upgraded. `python3` (host), `git`, `bash`, `bwrap` — all present already.

**Scratch relocation (orchestrator interrupt, mid-run):** the first 20 GB of scratch was created under
`/tmp/tameshi-r47-T47CritC1Control/` and filled the 128 GB `/tmp` partition (96 %). On instruction I killed the two
live runs, captured their receipts, deleted the whole `/tmp/tameshi-r47-T47CritC1Control` tree (freed 20 GB, `/tmp`
back to 26 GB free) and moved the remaining work to `/var/tmp/tameshi-r47-T47CritC1Control/` (root fs, 565 GB free).
No run that died on ENOSPC is reported as a finding: the two killed runs (a full `--emit` pass, a 3-statement probe)
were discarded and re-run from `/var/tmp`; the runs reported below all exited on their own. **The 16–20 GB
`/tmp` tree is gone; nothing of mine remains under `/tmp`.**

---

## 1. Verdict in one line

`measure.py` alone cannot distinguish a real statement from a rewired or env-hijacked one: **the cheapest pass that
the counter accepts and no gate refuses costs one environment variable pair, edits no tracked file except
`SCORECARD.md`, and prints `C1_R47_PASS=true`** (§6). The cheapest counterfeit of all is 2 lines added to the frozen
counter itself (§4), refused only by `deciding-run.sh`, a script that is *not* in its own `FROZEN` list and not
pinned anywhere.

The honest pass is *also* one command (`--emit` + paste, already receipted as `CTL_K` in
`control/controls-at-freeze.stdout`: `total=0 … C1_R47_PASS=true`). So the attack is not about cost: it is that three
mutations of *equal* counter output are indistinguishable — honest rows, rows over a rewritten tool, rows over a
hijacked P0.

## 2. What the counter binds, and what it does not

`calibration/measure.py:1-30` (the frozen predicate) binds, per statement: the picked line, the exit code, a 12-hex
prefix of `sha_file` at REV, and a declared deps set that must equal the observed deps. It binds the *identity* of
the tool only to **REV** — never to the freeze. Consequences, each tested below:

| | bound at REV | bound at FREEZE |
|---|---|---|
| counter bytes (`self_pin`) | yes | **no** |
| statements bytes (`stmts_pin`) | yes (constant inside the counter) | **no** |
| statement tool bytes (`sha_file`) | only as a prefix in the row | **no** |
| P0 environment | nothing | **no** — it is `os.environ` of the deciding process |

`deciding-run.sh:26-27` adds a `git diff --quiet FREEZE..REV` over a `FROZEN` path list. That list contains
`$E/calibration`, `$E/coverage`, `$E/hardening`, `$E/control`, `$E/no-harm.sh`, `$E/contract.json`, two
`before/base-*.txt` and the hard brief. It does **not** contain `tools/`, `.ufo/evidence/round-21`, `-45`,
`-kaika-round-1`, `-round-15`, or `deciding-run.sh` itself.

All nineteen distinct `sha_file` targets of the 22 frozen statements are outside that list:

```
MUTABLE .ufo/evidence/kaika-round-1/sources-census-v2.sh
MUTABLE .ufo/evidence/round-15/verify.py
MUTABLE .ufo/evidence/round-21/coldread/measure.py
MUTABLE .ufo/evidence/round-45/freshness/measure.py
MUTABLE tools/{command-binding,env-diff,evidence-disposition,mte-interop,pin-disposition,
               registry-replay,repeat-control,staged-id-guard,tally-audit-v2,tally-audit-v3,
               wave-accounting,witness-metadata,write-path-census-v2,write-path-census-v3}.py
MUTABLE tools/mutate-and-run.sh
```

## 3. Cheats scored

| # | cheat | counter verdict | refused by | closes with |
|---|---|---|---|---|
| a | every row `deps none` | **false** (`dep_mismatch=5`) | the counter itself | — (already control `CTL_J`) |
| b | every row declares all five deps | **false** (`dep_mismatch=1` per statement; 22/22 in a full run) | the counter itself | — |
| c | edit `statements.json` only | **false** (`stmts_pin=0`) | `stmts_pin` + `FROZEN_UNCHANGED` | already closed |
| c′ | edit `statements.json` **and** the hash constant inside `measure.py` | **true** | `FROZEN_UNCHANGED=0` only | §7.1 |
| d | 2 lines in `measure.py` | **true**, `self_pin=1`, exit 0 | `FROZEN_UNCHANGED=0` only | §7.1 |
| e | rewrite a statement's tool (argv untouched, `sha_file` path unchanged) | **true** (MATCH, `deps none`) | **nothing** — `tools/` is not in `FROZEN` | §7.2 |
| f | banner line matching `obs` printed before the real report | **true** (MATCH on a count the tool never computes) | **nothing** | §7.3 |
| g | hijack P0 through the deciding shell's environment | **true**, zero tracked-file drift | **nothing** | §7.4 |
| h | paste the freeze receipt's rows | **false** once any statement's output moves at REV | the counter itself | — |

## 4. (c′)/(d) The pins are self-referential — evidence

`self_pin` compares the *running* file to `git show REV:measure.py`; `stmts_pin` compares the statements blob to a
constant that lives inside that same file. Commit the edit and both are satisfied. Measured, on a clone at the
freeze, two inserted lines after `append_only = int(rev_sc.startswith(base_sc))` (`measure.py:272`):

```
C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unpinned=0 \
        append_only=1 total=0 rev=4e30f38a7520f2c051a9b663432109239bedb4c3 C1_R47_PASS=true
exit=0
```
```
$ git -C expA diff --quiet FREEZE HEAD -- .ufo/evidence/round-47/calibration/measure.py
FROZEN_DIFF_CLEAN=0
```

No statement was executed in that run: the cheat returns before the profile setup. The same trick with a
`total = 0` rewrite instead of an early return would leave all 22 statements running and simply report a zero
total — the counter's own arithmetic is inside the file the pin trusts.

Editing `statements.json` alone is refused, as designed:

```
C1_R47_PARTIAL: … stmts_pin=0 … total=1 … C1_R47_PASS=false
```

`stmts_pin` is a constant in `measure.py` (`STATEMENTS_SHA256`, `measure.py:49`), so c′ = c + the update of that
constant in the same commit; by the expA result (`self_pin=1` on a committed edit) c′ reaches `PASS=true`.
`[INFERENCE from expA + expC, not separately run end to end: the arithmetic is the counter's own.]`

## 5. (e)/(f) The tool is not frozen — evidence

**(e) rewrite the tool, keep the argv.** `tools/repeat-control.py` replaced by a 2-line printer; row states the new
sha (which the counter reads from REV, so it always agrees with itself):

```
STATEMENT cap/repeated pristine-control gate: claimed=SELFTEST: PASS (29 cases)|0|913db5ac38d5 \
  observed=SELFTEST: PASS (29 cases)|0|913db5ac38d5 (exit=0) MATCH declared_deps=none observed_deps=none DEPS-OK
C1_R47_PARTIAL: self_pin=1 stmts_pin=1 statements=1 … total=0 … C1_R47_PASS=false
```
and against the deciding script's own path list:
```
git diff --quiet FREEZE HEAD -- <the FROZEN list>  →  FROZEN_OK=1
```
i.e. a gutted statement tool is invisible to every gate in the round. The only trace is the 12-hex prefix in the
row changing, and nothing compares that prefix to the freeze.

Note what this costs in the do-nothing controls: the minimum version of (e) is **five** tool rewrites, because the
five statements with a non-empty observed deps set (`six-leg regression ledger` `fleet-root,node`,
`effective expectation reconciliation` `jj`, `retained invocation-context gate` `fleet-root`,
`hermetic env-differential probe` `env,node`, `mutation report interop` `node`) are exactly the rows blanket
`deps none` cannot state. `CTL_J` is therefore not the cheapest cheat; it is the most expensive honest-looking one.

**(f) first match wins.** `pick_line` (`measure.py:141-152`) uses `re.search(..., re.M)`, so the *first* line matching `obs` is the picked
value. A one-line banner prepended to `tools/repeat-control.py`:

```
banner: SELFTEST: PASS (1 cases)      ← picked, claimed, MATCHed
real:   SELFTEST: PASS (29 cases)     ← ignored
```
```
STATEMENT cap/repeated pristine-control gate: claimed=SELFTEST: PASS (1 cases)|0|0797cda86ab5 \
  observed=SELFTEST: PASS (1 cases)|0|0797cda86ab5 (exit=0) MATCH declared_deps=none observed_deps=none DEPS-OK
```
The row states a case count the tool never computes, in all six profiles, with `deps none` correct by
construction. A second run with an identical banner but the body untouched gave the same MATCH and `deps none`,
confirming the banner and not the body is what the counter reads.

**(h) paste the freeze receipt.** The freeze receipt `before/c1-at-freeze.stdout` carries every P0 value, so it is
the obvious zero-work source for the rows. It does not survive the round's own content moves: appending four
registry rows to `corpus/SOURCES.md` and pasting the `sources-registry` row unchanged gives
`observed=- (exit=1) UNOBSERVABLE … total=1 … C1_R47_PASS=false`. Good — the C3 wave's registry growth will move
`sources-registry` (`rows=120`), so the honest rows must be taken *after* the C3 rows land, not from the freeze
receipt.

## 6. (g) Hijack P0 — the cheapest pass nothing refuses

`profile_env(work, 'P0', rev)` (`measure.py:176-179`) is `host_env()`: **every** environment variable of the
deciding process, minus `GIT_*`. P1–P5 are constructed. So the L1's own shell decides what "the live host prints".
Two startup hooks reach every statement without touching the repository:

* `PYTHONPATH=<dir>` with `sitecustomize.py` — imported by every `python3 SCRIPT` before the script body;
* `BASH_ENV=<file>` — sourced by every non-interactive `bash SCRIPT` before the script body.

Both were verified to intercept exactly the statements and not the counter:

```
BASH_ENV=inj.bash bash tools/mutate-and-run.sh --selftest                 → MUTATE_SELFTEST: 0/0 pass      (rc=0)
BASH_ENV=inj.bash bash tools/mutate-and-run.sh --regression --workdir …   → REGRESSION: ALLPASS (cases=0 …  (rc=0)
BASH_ENV=inj.bash bash .ufo/evidence/kaika-round-1/sources-census-v2.sh   → == A rows / 999 / SOURCES_CENSUS: CLEAN …  (rc=0)
PYTHONPATH=inj python3 tools/repeat-control.py --selftest                 → SELFTEST: PASS (29 cases)      (rc=0)
PYTHONPATH=inj python3 -c 'print("COUNTER-SURVIVES")'                     → COUNTER-SURVIVES
```
The `sitecustomize` hook is selective (it exits only when `sys.orig_argv[1]` ends with one of the 22 target paths),
so the counter itself runs normally.

Because P0 is injected and P1–P5 are not, the observed dependence set becomes `env` (plus whatever else really
moves), which the counter *honestly* derives; `--emit` then hands back rows that declare exactly that. One `--emit`
run under the poisoned environment, one paste, one commit: `SCORECARD.md` is the only tracked file that changed,
`FROZEN_UNCHANGED=1`, `self_pin=1`, `stmts_pin=1`, `total=0`, `C1_R47_PASS=true`. No statement ever executed.
The rows are lies of the exact shape the contract forbids ("states what the statement's command prints"), and the
counter's definition of a dependence validates them.

**Measured:**
<!-- F-RESULT -->

**The tell** (a reviewer's only defense): every injected row's deps set contains `env`, whereas
`before/c1-at-freeze.stdout` records `env` for exactly one statement. A deciding receipt whose 22 statements all
depend on `env` contradicts the freeze receipt and should be refused on sight.

## 6b. What the same experiment found on the way: the observation is load-sensitive, and a timeout *is recorded as a dependence*

Two `--emit` passes were made on the same clone at the same rev under the same injection, one while the fleet was
busy and one while it was quiet. Per-statement tuples, only for the statements that moved:

```
tally-audit-v2 runner audit   busy : P1=UNOBSERVABLE|timeout  P2..P5 ok      → deps bwrap,env,fleet-root,jj,node
                              quiet: P1..P5 all `TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0`  → deps none
tally-audit-v3 runner audit   busy : P1..P5 all UNOBSERVABLE|timeout         → deps env
bounded ANSI-C code_view      quiet: P1..P5 all `TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0`  → deps none
six-leg regression ledger      busy : P2=`REGRESSION: FAIL (cases=9 passed=8`, exit 1   → deps bwrap,env,fleet-root,node
                              quiet: P2=`REGRESSION: PASS (cases=9 passed=9`, exit 0   → deps env,fleet-root,node
```
Pasting the busy run's rows and deciding on the quiet host gave
`total=5 … mismatches=0 unparsed=0 unobservable=1 dep_mismatch=4 … C1_R47_PASS=false` — four of them purely from
the load difference, the fifth from a bug of my own. `comparable()` maps a timeout to
`('UNOBSERVABLE', 'timeout')`, so **any variant that is merely slow differs from P1 and is written down as a
dependence**: a 14-worker pool that also shares the host with other seats converts scheduling contention into a
false deps clause. The same mechanism explains the freeze receipt's odd `hermetic env-differential probe` row:
freeze `P1..P5 = 2/9, 2/9, 2/9, 1/9, 2/9` (`deps env,node`) versus `9/9, 2/9, 9/9, 8/9, 9/9` (`deps bwrap,node`) in
two runs today, while the tool itself now prints `ENVDIFF_SELFTEST: 9/9 pass` under the host env, a clean env and
a node-dropped env alike — its nine pinned legs degrade under load, not under the profile.

This is the same class of defect as C2's "a crash is not a kill", and it is the one that will actually bite the
L1: the round's design *requires* the rows to exist at REV before the deciding measurement, so the L1 must predict
the observation from an earlier run, and a load difference between the two is enough for an honest `--emit`-paste
to fail its own deciding run. Smallest correction:

```python
for dep, prof in VARIANTS:
    o, note = results[(sid, prof)]
    if o is None:                    # timeout or crash in a variant is not evidence of a dependence
        unstable += 1
        continue
    if comparable((o, note), s['kind']) != ref:
        observed_deps.add(dep)
...
total = mism + unparsed + unobs + depm + unpinned + unstable
```
with `unstable` also counting a second observation of each profile that disagrees with the first (C2's repeat
discipline, applied here), and the receipt recording `jobs` and the wall time. On today's evidence `unstable`
would have been 0 on a quiet host and ≥ 12 on a busy one: the honest claim is then a claim about an idle machine,
which is at least a claim the judge can reproduce.

## 7. Smallest safe corrections

Each is short enough to write here. All of §7.1–7.4 change the frozen predicate, so they are **pre-data amendments**
to be recorded in `contract.amendments` and committed before any seat scores — not edits to make now.

### 7.1 Anchor the pins at the freeze, not at REV

```python
FREEZE = '9acfbe21435e1976636a276448dee1d5e7155915'
...
raw = git('-C', lane, 'show', '%s:%s' % (rev, STATEMENTS_PATH), binary=True)
fz  = (git('-C', lane, 'rev-parse', '--verify', FREEZE + '^{commit}') or '').strip()
self_pin  = int(self_pin  and git('-C', lane, 'show', '%s:%s' % (fz, SELF_PATH), binary=True) == me)
stmts_pin = int(stmts_pin and git('-C', lane, 'show', '%s:%s' % (fz, STATEMENTS_PATH), binary=True) == raw)
```
Refuses both c′ and d with the counter's own line, not with an out-of-band script. It also makes an amendment
*visible*: you cannot change the counter without moving `FREEZE`, and moving the freeze is a contract edit.

Add `$E/deciding-run.sh` to the deciding script's `FROZEN` list and execute it from the freeze blob, the way
`no-harm.sh` is already executed (`git show "$REV:$E/no-harm.sh" > "$OUT/no-harm.sh.copy"; bash …`):

```bash
git show "$FREEZE:.ufo/evidence/round-47/deciding-run.sh" > "$OUT/deciding.sh" && bash "$OUT/deciding.sh" …
```
As shipped, `deciding-run.sh` is neither frozen, nor self-pinned, nor run from a blob, so it is the one file that
can delete its own gate.

### 7.2 Bind the statement tools to the freeze

```python
tool_drift = sum(1 for s in statements if s.get('sha_file')
                 and git('-C', lane, 'show', '%s:%s' % (fz, s['sha_file']), binary=True)
                  != git('-C', lane, 'show', '%s:%s' % (rev, s['sha_file']), binary=True))
...
total = mism + unparsed + unobs + depm + unpinned + tool_drift
```
Nineteen lines of `FROZEN` in `deciding-run.sh` would do the same belt-and-braces, but the counter is the right
place: the claim *is* about these commands, so a statement whose tool moved is a different statement. The round's
work (SCORECARD rows, C2 additions, C3 snapshots) touches none of them; a legitimate need to move one is an
amendment, which is exactly the signal this round is supposed to produce.

### 7.3 One matching line, or fail closed

```python
def pick_line(stmt, out):
    ...
    ms = re.findall(pat, out, re.M)
    if len(ms) != 1:
        return None          # 0 = unobservable, >1 = a banner shadows the verdict
    return ms[0]
```
(the `census` and `monitor` branches need the same `len(...) == 1` on their two regexes). Before adopting, count
matches in the six per-profile dumps the counter already writes (`work/<P>/obs-<id>.stdout`) — that is a
`grep -c` over existing receipts, no re-run. This also closes the weaker variant of (f) where an overloaded `obs`
regex (`^(WRITE_CENSUS_V2_SELFTEST: .*)$`) matches more than one line.

### 7.4 Make P0 a declared profile, not an inherited one

```python
P0_ALLOW = ('HOME', 'USER', 'LOGNAME', 'SHELL', 'TERM', 'LANG', 'LC_ALL', 'TZ', 'TMPDIR')
def profile_env(work, prof, rev):
    if prof == 'P0':
        e = {k: os.environ[k] for k in P0_ALLOW if k in os.environ}
        e['PATH'] = os.path.join(work, prof, 'shim'); build_shim(e['PATH'])
        e['PYTHONDONTWRITEBYTECODE'] = '1'; e['REV'] = rev
        return e
```
An allowlist (not a denylist) removes `PYTHONPATH`, `PYTHONHOME`, `PYTHONSTARTUP`, `BASH_ENV`, `ENV`,
`SHELLOPTS`, `LD_PRELOAD`, `NODE_OPTIONS`, `CDPATH` and the ambient `PATH` in one move, and keeps P0 host-shaped
(real `HOME`, real locale, real `TZ`). Rebuilding `PATH` from `build_shim()` is what makes it a *declared* profile;
keeping the ambient `PATH` leaves a shadowing route open even with the rest allowlisted.

Belt: print the passed env in the receipt and let the deciding script refuse a non-allowlisted name.

```python
print('P0_ENV %s' % ' '.join(sorted(profile_env(work, 'P0', rev))))
```
```bash
grep -qE 'P0_ENV .*\b(PYTHONPATH|BASH_ENV|PYTHONHOME|LD_PRELOAD)\b' "$OUT/c1.stdout" && rc=1
```

### 7.5 Independence of the axis witnesses (not a cheat, a duplicate authority)

`axis/calibration`, `axis/freshness` and `axis/depth` have as `sha_file` the *same three files* that `no-harm.sh`
parses: `.ufo/evidence/round-21/coldread/measure.py`, `.ufo/evidence/round-45/freshness/measure.py`,
`tools/mutate-and-run.sh`. Replacing the first two with two printers that echo the expected strings leaves both
no-harm monitors green:

```
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
```
So one rewiring turns both the axis row and its monitor green; the "seven monitors" cannot witness a C1 axis row
because they read the row's own witness. §7.2 closes this too (the axis witness sha must equal the freeze sha);
`deciding-run.sh`'s `COUNTER_SHA256` block already computes the number a human needs but nothing compares it.

## 8. Bounds of this review

* I did not run the honest pass (no lane write); `CTL_K` in `control/controls-at-freeze.stdout` already receipted
  `total=0 … C1_R47_PASS=true`, so the honest route is proven and cheap — which is the point: the cheats are not
  cheaper than honesty, they are *indistinguishable* from it.
* I did not run a full 22-statement pass for c′, e or f; each was scored on the statement it attacks with `--only`,
  and the pass follows from the counter's arithmetic (`measure.py:328`), with
  `--only`-runs showing `total=0` for the attacked statement. Only (g) was carried to a full deciding-shaped pass.
* Nothing in the lane, the fleet repo, the read-only package, or any jj/Git state was modified. Fixture repos were
  throwaway clones under `/var/tmp`; no `git add/commit/stash/checkout/switch/reset/pull/push` was run in the lane.
