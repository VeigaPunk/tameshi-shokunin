# T54W1ExecFreeze — round-54 freeze integrity (crash-resume re-implementation)

Milestone: freeze integrity. Judged on: calibration.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `d33053f7552db4bd290c99a36979760f544c41ad`, freeze `441c26bec5e4c1cc31bc2a840f311cb8d1965259`,
C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`. The lane advanced to
`99c3bc88d704566197783f66b211ee0a830e0330` (C1 fix pass) and then to
`7883e0e58937d47724b91f1a0475a8785118b696` (amendment 1: `c1/measure.py` arm 3 re-key discovery)
and to `3146479c21387dc5affe56f334aba1f770386b61` (round record) while this seat ran; the pinning
arm is measured at the first two, and §9 measures the amended freeze separately because it is no
longer the same manifest.

Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1ExecFreeze/` (removed at the end of the seat; the
instrument is embedded verbatim in §1 so the check is still runnable). No tool was installed or
upgraded; `pacman` was not touched.

No lane file was edited by this seat. Writes are confined to
`.ufo/waves/round-54/w1/T54W1ExecFreeze.md` and
`.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/`.

## 1. The instrument

Round 53's `.ufo/evidence/round-53/verify-freeze.sh` re-derived every recorded digest from the bytes
at FREEZE and printed `FREEZE_INTEGRITY: OK|MISMATCH`. Round 54's item asks for that plus two arms
the round-53 script did not have (manifest coverage of the contract, and both counters executed from
the frozen bytes). The re-implementation is a scratch script, not a lane file:

```
python3 freeze-resume-r54.py LANE FREEZE REV WORK [skip-counters]
```

Arms: (1) digest — recorded sha256 vs blob at FREEZE; (2) coverage — `contract.frozen_paths` vs the
manifest file list; (3) pinning — every contract path byte-identical between FREEZE and REV (this is
`deciding-run.sh`'s own `FROZEN_UNCHANGED` gate, re-derived); (4) counters — extract
`c1/measure.py`, `c1/lost-headings-at-base.json`, `c2/measure.py`, `no-harm.sh` from the blobs at
FREEZE into `WORK/code` and run both counters from those bytes at REV. Exit 1 on any digest or
pinning mismatch, 0 otherwise.

Script (verbatim; the scratch copy had `sha256=07d38c62dd93003cc06487d53412ffca61bbeddfaceb40fb6acf10ba6cd7a0df`.
Reproduce by pasting this block into a file and running the commands below — it reads only git
objects and writes only under `WORK`):

```python
#!/usr/bin/env python3
"""Round-54 crash-resume freeze integrity check (re-implemented from round-53's
verify-freeze.sh), with the three extra arms this round's item asks for.

Usage: freeze-resume-r54.py LANE FREEZE REV WORK [skip-counters]

  1. digest    re-derive every sha256 recorded in .ufo/evidence/round-54/freeze.json
               from the blob committed at FREEZE; an unreadable or differing file is
               a MISMATCH (a resumed L1 must not trust a re-frozen manifest).
  2. coverage  compare contract.json's `frozen_paths` with the manifest's file list
               (modulo freeze.json itself, which cannot carry its own digest) and
               name every path the manifest never hashes.
  3. pinning   re-derive deciding-run.sh's FROZEN_UNCHANGED gate: every path in
               contract.frozen_paths must be byte-identical between FREEZE and REV.
               This is the arm that makes "the counters run from FREEZE bytes" and
               "the counters run from REV bytes" the same statement.
  4. counters  extract c1/measure.py (with its sibling lost-headings-at-base.json,
               which c1 reads from Path(__file__).parent), c2/measure.py and
               no-harm.sh from the blobs at FREEZE into WORK/code and run both
               counters from THOSE bytes at REV, never from the working tree.

Prints FREEZE_INTEGRITY: OK only when every recorded digest matches; the other arms
print their own verdicts. Exit 1 on any mismatch, 0 otherwise. Stdlib only; writes
only under WORK and reads only git objects.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

LANE, FREEZE, REV, WORK = sys.argv[1:5]
SKIP = len(sys.argv) > 5 and sys.argv[5] == "skip-counters"
E = ".ufo/evidence/round-54/"
WORK = Path(WORK)
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
bad = []


def git(*args):
    r = subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, env=ENV)
    return r.stdout, r.returncode


def blob(rev, path):
    data, rc = git("show", "%s:%s" % (rev, path))
    return data if rc == 0 else None


def sha(data):
    return hashlib.sha256(data).hexdigest() if data is not None else "UNREADABLE"


man = json.loads(blob(FREEZE, E + "freeze.json"))
con = json.loads(blob(FREEZE, E + "contract.json"))
print("FREEZE %s files=%d amendments=%d" % (FREEZE[:12], len(man["files"]),
                                            len(man.get("amendments", []))))
print("\n-- arm 1: recorded digest vs blob at FREEZE")
print("| path | recorded sha256 | computed sha256 | match |")
print("|---|---|---|---|")
for rel, want in sorted(man["files"].items()):
    got = sha(blob(FREEZE, E + rel))
    ok = got == want
    print("| `%s` | `%s` | `%s` | %s |" % (rel, want, got, "YES" if ok else "NO"))
    if not ok:
        bad.append("digest %s computed %s != recorded %s" % (rel, got, want))

manifest = {E + k for k in man["files"]} | {E + "freeze.json"}
contract = set(con["frozen_paths"])
print("\n-- arm 2: contract.frozen_paths vs manifest (+freeze.json)")
print("CONTRACT_FROZEN_PATHS=%d MANIFEST=%d SET_EQUAL=%s"
      % (len(contract), len(manifest), "yes" if contract == manifest else "no"))
for p in sorted(contract - manifest):
    print("EXTRA_IN_CONTRACT %s sha256_at_freeze=%s" % (p, sha(blob(FREEZE, p))))
for p in sorted(manifest - contract):
    print("EXTRA_IN_MANIFEST %s" % p)
print("COVERAGE_GAP=%d (contract paths the manifest never hashes)" % len(contract - manifest))

print("\n-- arm 3: contract.frozen_paths FREEZE vs REV (%s)" % REV[:12])
drift = 0
for p in sorted(contract):
    a, b = blob(FREEZE, p), blob(REV, p)
    same = a is not None and b is not None and a == b
    drift += 0 if same else 1
    print("PINNED %s %s" % (p, "yes" if same else "NO freeze=%s rev=%s" % (sha(a)[:12], sha(b)[:12])))
print("FROZEN_UNCHANGED=%d/%d" % (len(contract) - drift, len(contract)))
if drift:
    bad.append("FROZEN_UNCHANGED %d/%d" % (len(contract) - drift, len(contract)))

if not SKIP:
    print("\n-- arm 4: both counters run from the FREEZE bytes")
    code = WORK / "code"
    for rel in ("c1/measure.py", "c1/lost-headings-at-base.json", "c2/measure.py", "no-harm.sh"):
        (code / rel).parent.mkdir(parents=True, exist_ok=True)
        data = blob(FREEZE, E + rel)
        if data is None:
            print("COUNTER_BYTES %s ABSENT-AT-FREEZE" % rel)
            bad.append("%s absent at freeze" % rel)
            continue
        (code / rel).write_bytes(data)
        print("COUNTER_BYTES %s sha256=%s" % (rel, sha(data)))
    for key in ("c1", "c2"):
        wd = WORK / key
        wd.mkdir(parents=True, exist_ok=True)
        env = dict(ENV)
        env["TMPDIR"] = str(wd / "tmp")
        Path(env["TMPDIR"]).mkdir(exist_ok=True)
        run = subprocess.run([sys.executable, str(code / key / "measure.py"), "--lane", LANE,
                              "--rev", REV, "--work", str(wd / "work"), "--explain"],
                             capture_output=True, env=env)
        out = run.stdout.decode("utf-8", "replace") + run.stderr.decode("utf-8", "replace")
        (WORK / ("%s.out" % key)).write_text(out)
        line = [l for l in out.strip().splitlines() if l.startswith(key.upper() + "_R54:")]
        print("COUNTER_RUN %s exit=%d %s" % (key, run.returncode, (line[-1] if line else "<none>")[:150]))

print()
if bad:
    print("FREEZE_INTEGRITY: MISMATCH")
    for b in bad:
        print("MISMATCH", b)
    sys.exit(1)
print("FREEZE_INTEGRITY: OK")
```

## 2. Arm 1 — recorded digest vs blob at `441c26b` (7/7 match)

```
$ python3 freeze-resume-r54.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    441c26bec5e4c1cc31bc2a840f311cb8d1965259 59c38109bf119d0e9d4f878644a82babc937bc1e <work> skip-counters
FREEZE 441c26bec5e4 files=7 amendments=0
```

| path (under `.ufo/evidence/round-54/`) | recorded sha256 | computed sha256 | match |
|---|---|---|---|
| `c1/measure.py` | `6a39b38770e828aaa7624644169b07aed18f2f26477170c12d85a33799b1efec` | `6a39b38770e828aaa7624644169b07aed18f2f26477170c12d85a33799b1efec` | YES |
| `c1/lost-headings-at-base.json` | `a953d2e87116effc943f56a532b785cae8c8f44a104635083634c05fe0b8bb10` | `a953d2e87116effc943f56a532b785cae8c8f44a104635083634c05fe0b8bb10` | YES |
| `c2/measure.py` | `b4684a3f555e8cbfda6fc9c7208827a3816a60cf53186269fdec41d5025e9e49` | `b4684a3f555e8cbfda6fc9c7208827a3816a60cf53186269fdec41d5025e9e49` | YES |
| `contract.json` | `e15bffb3e888dd39bfc2a0932f054a416a506351c1be850427989792b08c380e` | `e15bffb3e888dd39bfc2a0932f054a416a506351c1be850427989792b08c380e` | YES |
| `no-harm.sh` | `1aa2fa9df9eac9380be0d24d0191a4c25f93030895db8d5fbeba6147920b639a` | `1aa2fa9df9eac9380be0d24d0191a4c25f93030895db8d5fbeba6147920b639a` | YES |
| `deciding-run.sh` | `8a26856a81b6c8505b6f076a227b62c31fb04b179bd74aae706e70d8c7e44194` | `8a26856a81b6c8505b6f076a227b62c31fb04b179bd74aae706e70d8c7e44194` | YES |
| `control/controls.sh` | `3f1e5f5ce26159d914faa4f4339ba2e5f1484eb6b3be9f032a02be575203e6b4` | `3f1e5f5ce26159d914faa4f4339ba2e5f1484eb6b3be9f032a02be575203e6b4` | YES |

Verdict: `FREEZE_INTEGRITY: OK`. Independently, the same seven blobs are byte-identical at C0 and in
the worktree at the time of measurement (`same=YES` for all seven), so at that moment no post-freeze
re-freeze or silent body edit was present. (A deliberate re-freeze landed after this measurement —
§9 — and it is not internally consistent; the finding there is about the amended manifest, not about
the seven digests below.) `freeze.json` itself carries no digest (self-reference); its bytes are
pinned by the freeze commit — that is exactly the "modulo freeze.json itself" allowance.

## 3. Arm 2 — `contract.frozen_paths` vs the manifest file list

```
CONTRACT_FROZEN_PATHS=11 MANIFEST=8 SET_EQUAL=no
EXTRA_IN_CONTRACT .ufo/evidence/round-18/measure.py sha256_at_freeze=7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37
EXTRA_IN_CONTRACT .ufo/evidence/round-21/coldread/measure.py sha256_at_freeze=657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb
EXTRA_IN_CONTRACT .ufo/evidence/round-48/quality/coldread-precheck.sh sha256_at_freeze=3b07847afc86d0d6c14d2e6c20a6b3778da1798d9304204ec3a360a6301b2924
COVERAGE_GAP=3 (contract paths the manifest never hashes)
```

Set arithmetic: the manifest lists 7 files; adding `freeze.json` (the self-referential member the
item excludes) gives 8. `contract.json` lists 11. The three extra contract paths are the inherited
counter bodies the round's counters execute (`round-48/quality/coldread-precheck.sh` is shelled by
c1 arm 1; `round-21/coldread/measure.py` is the monitor; `round-18/measure.py` supplies `sectionize`
and the credit algorithm). `SET_EQUAL=no` is therefore the correct, reproducible answer, and the
manifest is narrower than the contract.

Mitigation actually in place: `deciding-run.sh`'s `FROZEN=` list at line 34 names all 11 paths and
line 35 runs `git diff --quiet "$FREEZE" "$REV" -- $FROZEN`, so the deciding run does gate the three;
and arm 3 below shows all 11 byte-identical. What is missing is at the artifact level: a resumed L1
that trusts only `freeze.json` (as round 53's `verify-freeze.sh` did) gets no signal if one of the
three inherited bodies was rewritten between the freeze and the measured revision. Round 53 had the
same omission (`round-53/freeze.json` = 8 files, its `deciding-run.sh` line 35 also carried the same
three) and published a manifest `note` explaining the FROZEN_UNCHANGED coupling; round 54's
`freeze.json` dropped that `note` as well.

## 4. Arm 3 — pinning, `FREEZE` vs `REV` (the deciding run's `FROZEN_UNCHANGED` gate, re-derived)

At C0 `59c38109bf11`:

```
FROZEN_UNCHANGED=11/11   FREEZE_INTEGRITY: OK   (exit 0)
```

At the live HEAD `99c3bc88d704566197783f66b211ee0a830e0330` (C1 fix pass, committed after the seat
started):

```
CONTRACT_FROZEN_PATHS=11 MANIFEST=8 SET_EQUAL=no
COVERAGE_GAP=3 (contract paths the manifest never hashes)
FROZEN_UNCHANGED=11/11
FREEZE_INTEGRITY: OK
```

`git merge-base --is-ancestor 441c26be 59c38109` exits 0, so the freeze is an ancestor of the content
commit, as the contract's `base`/freeze ordering requires. No frozen byte moved from the freeze
through the C1 fix pass. After that, a deliberate re-freeze (amendment 1) did move three of them —
see §9, which is where the integrity finding is.

## 5. Arm 4 — both counters run from the frozen bytes

Both counters are extracted from the blobs at `441c26b` (not from the working tree) with their
sibling data and run with `--lane LANE --rev REV --work <empty>`. Extracted digests equal the
manifest's (`COUNTER_BYTES c1/measure.py sha256=6a39b387…`, `c1/lost-headings-at-base.json
sha256=a953d2e8…`, `c2/measure.py sha256=b4684a3f…`, `no-harm.sh sha256=1aa2fa9d…`).

`c1/measure.py` reads its heading list from `Path(__file__).resolve().parent /
'lost-headings-at-base.json'`, which is why the manifest freezes that sibling too; extracting both
is sufficient and no working-tree read occurs.

### C1 — reproduces both frozen C1 numbers exactly

At base (`EXPLAIN` lines omitted for width; full files in the receipts dir):

```
C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false   (exit 1)
```

At C0:

```
C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false   (exit 1)
```

These match the contract's C1 `before` (`credited=57 lost=7 monitor=6/57` at `d33053f7`) and the wave
context's C0 reading (`credited=41 lost=23`) unit for unit. The instrument runs and is deterministic
in this arm.

### C2 — runs, but the `usable` arm is short at every revision

At base:

```
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=0 note=0 sources=0 total=14 C2_R54_PASS=false
```

At C0:

```
EXPLAIN unusable registry-check rc=2 line='registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory'
...
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
```

At HEAD `99c3bc8` the same arm is short:

```
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=99c3bc88d704 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
```

The C2 target asks for `7/7 exit 0 ... on a usable one with
no mkdir under /tmp`; `usable_ok=6` keeps `total>=1`, and the contract's kill rule ("any arm short of
7/7 makes C2_R54_PASS=false") leaves C2_R54_PASS=false at every revision measured here.

Cause, isolated (not a tree defect — `tools/registry-check.py` is byte-identical at base, C0 and
HEAD: `sha256=ade15cc008c07d54c77812d27b49079180168d843439b0b1c458292fa0f2a33f`):

```
$ cd <clone at base> && TMPDIR=<fresh dir> python3 tools/registry-check.py --selftest
exit=0   SELFTEST: PASS (51 cases)

$ cd <clone at base> && TMPDIR=<fresh dir> strace -f -e trace=mkdir,mkdirat -o <log> python3 tools/registry-check.py --selftest
exit=1
SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=4.542s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=5.040s survivor=False marker=False)
SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)
```

The frozen C2 counter's `usable` arm runs every self-test under `strace -f` to count `/tmp` mkdirs
(`c2/measure.py`, the `strace -f -e trace=mkdir,mkdirat` loop). `registry-check`'s own self-test
contains two `timeout`/`setsid`-`setpgid` cases that do not survive being traced: untraced they pass,
traced they fail. A second independent traced run reproduces the same two failures:

```
$ ... strace -f -e trace=mkdir,mkdirat -o <log> python3 tools/registry-check.py --selftest
exit=1
SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=14.446s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=17.341s survivor=False marker=True)
SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)
```

What the two cases do (`tools/registry-check.py:1177` `run_escape_case`): a child calls
`os.setsid()` / `os.setpgid(0, 0)`, writes `ready`, sleeps 5 s, then writes a `survived` marker; the
tool runs that row with `timeout=1` and the case asserts `ROW ... got=timeout differs`, a readable
process identity, no surviving process and no marker. Under tracing the row's timing changes: in the
second run the escaped child wrote its `survived` marker (`marker=True`), i.e. the 1 s kill missed a
child that the tracer had slowed down; in the first run both `survivor` and `marker` are false, so
the failing term was the recorded row output/identity, not a surviving process. Either way the
assertion is tracing-sensitive: 51/51 pass untraced, the same 2 cases fail traced, twice, with the
elapsed time itself moving from 4.5 s/5.0 s to 14.4 s/17.3 s as host load changed.

So the tracer the counter uses to prove "no mkdir under /tmp" is what breaks the exit-0 measurement
for that one tool. The failure is timing-shaped (the same two cases took 4.5 s/5.0 s on one run and
14.4 s/17.3 s on the next as host load rose), so this arm is load-sensitive: [INFERENCE] the same
frozen bytes could print `usable_ok=7` on a quiet host. On this host every observed run printed 6 —
base, two at C0, HEAD, and the recorded `before` artifact.

## 6. Negative controls — the instrument has teeth

Fixtures were committed in a scratch `git clone --shared` at
`/fast/scratch/hyaku/tameshi-r54/T54W1ExecFreeze/neg` (toplevel asserted equal to the fixture dir
before every git mutation; the lane was never written):

* `N1 = 1e62580fa26e3423cb8ffe0c63e801289d91397b` — a re-freeze that records an all-zero digest for
  `c1/measure.py`.
* `N2 = bf9255aacbab3fa70afa5c516169c646ead07719` — a post-freeze commit that appends one line to the
  frozen `c1/measure.py`, branched from the real freeze.

```
$ python3 freeze-resume-r54.py <neg> N1 N1 <work> skip-counters
| `c1/measure.py` | `0000…` | `6a39b387…` | NO |
FREEZE_INTEGRITY: MISMATCH
MISMATCH digest c1/measure.py computed 6a39b38770e828aaa7624644169b07aed18f2f26477170c12d85a33799b1efec != recorded 0000000000000000000000000000000000000000000000000000000000000000
EXIT=1

$ python3 freeze-resume-r54.py <neg> 441c26be N2 <work> skip-counters
PINNED .ufo/evidence/round-54/c1/measure.py NO freeze=6a39b38770e8 rev=ec45449c645e
FROZEN_UNCHANGED=10/11
FREEZE_INTEGRITY: MISMATCH
EXIT=1
```

So the re-implemented check detects both failure modes a resumed L1 cares about: a re-freeze whose
manifest no longer matches the frozen bytes (arm 1) and a post-freeze body edit (arm 3). Arm 1 alone
— the round-53 shape — cannot see the second mode, which is why arm 3 is carried here.

## 7. Findings

**F1 — the freeze manifest does not cover the whole frozen surface the contract declares.**
`contract.frozen_paths` (11) is not equal to `freeze.json`'s file list plus `freeze.json` (8); the
gap is `.ufo/evidence/round-18/measure.py`, `.ufo/evidence/round-21/coldread/measure.py`,
`.ufo/evidence/round-48/quality/coldread-precheck.sh` (`COVERAGE_GAP=3`). All three are byte-identical
from the freeze through C0 and HEAD, and `deciding-run.sh`'s own `FROZEN=`/`git diff --quiet` gate
does cover them, so the deciding run is not exposed — but an artifact-only resume (the round-53
`verify-freeze.sh` pattern) is blind to them, and round 54's manifest dropped the explanatory `note`
round 53 carried. The amended manifest at `7883e0e` still lists 7 files, so the gap survives the
re-freeze. Recommendation for the L1 (a lane edit is outside this seat's bounds): add the
three paths to `freeze.json` (a re-freeze, therefore an amendment) or state in the manifest that it
covers only the round directory and that `deciding-run.sh` pins the rest.

**F2 — the contract's recorded C2 `before` is off by one against the artifact it cites.**
Contract: `unusable_exit2=3 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false (measured at d33053f7,
.ufo/evidence/round-54/before/c2.stdout)`. The cited file now exists (untracked, written 11:32) and
its verdict line is `… usable_ok=6 … total=14 …`; my independent run of the frozen bytes at the same
rev also prints `total=14`, and `total = (7-3)+(7-7)+(7-7)+(7-6)+(7-0)+1+1 = 14`. The arithmetic in
the frozen contract cannot be produced by its own cited counter. Numbers are the calibration surface,
so this is a finding, not a nit; the L1 should correct the `before` line (or cite the artifact as-is
and re-state the delta) rather than let a wrong `before` stand as the round's baseline.

**F3 — the `before` receipts are not in the freeze.** `git ls-tree -r <rev> --
.ufo/evidence/round-54/before/` is empty at base, at `441c26be` and at C0; both `before/c1.stdout`
and `before/c2.stdout` appeared only as untracked worktree output (11:29 and 11:32, after the 11:19
freeze). A resumed L1 cannot verify either `before` claim from the freeze; today it re-derives them
(the C1 `before` does reproduce exactly — §5), and for C2 the re-derivation disagrees with the
contract (F2). Recommendation: commit the `before` receipts before the freeze, or list them in
`frozen_paths`.

**F4 — C2 cannot pass with the frozen counter; the `usable` arm is instrument-bound.**
`usable_ok=6` at base, C0 and HEAD, and the short tool is `registry-check`, whose self-test loses
exactly two `timeout`-`setsid`/`setpgid` cases under the counter's `strace -f` (untraced: 51/51
PASS, exit 0; traced: the same two cases fail in two independent runs, one of them with the escaped
child writing its `survived` marker). `tools/registry-check.py` is identical in all three revisions
(`sha256=ade15cc00…`), so the arm is not a property of this round's edits; the frozen C2 counter's
tracer is what fails it. Because the failure is timing-shaped (elapsed 4.5 s → 14.4 s as load rose),
the arm is also load-dependent: [INFERENCE] the same frozen bytes can print `usable_ok=7` on an idle
host, so the single deciding invocation is a coin-flip on host load, which is a calibration hazard in
its own right. With the contract's kill rule this is an honest-stop/counter-amendment decision for the L1,
not something a seat may patch: either the counter's `usable` arm must accept a traced-vs-untraced
differential (or run the tool untraced and trace only a probe), or the contract's `usable_ok` target
must be stated against what the instrument can actually measure. **Consequence as frozen: at the
revisions measured here `C2_R54_PASS=true` is not produced, and the C2 kill rule fires.**

**F5 — the amendment commit's manifest records a stale digest for `contract.json`.** At `7883e0e`
amendment 1 rewrote `contract.json` (an `amendments` entry, the `controls` arrays reformatted, the
trailing newline dropped) and recorded the new `c1/measure.py` digest, but `freeze.json` still records
`contract.json = e15bffb3e888dd39bfc2a0932f054a416a506351c1be850427989792b08c380e` — the
pre-amendment bytes — while the committed contract now hashes
`fca27997d22414d8c63bb3a7a376b332a91887d8d5c0603e929e3f934ef86dda`:
`FREEZE_INTEGRITY: MISMATCH (6/7 match)` (§9, receipt `freeze-arm1-at-amendment-1-7883e0e.out`).
The pre-amendment freeze `441c26be` is still internally consistent (7/7, §2), so this is a defect
introduced by the amendment, not by the original freeze. Remediation: recompute the contract digest
in the same commit as the amendment (and keep a trailing newline so the file stays a normal text blob).

**F6 — round 54 ships no verify-freeze equivalent, and the deciding run never checks the manifest.**
`grep -n "freeze.json\|sha256\|verify-freeze" .ufo/evidence/round-54/deciding-run.sh` matches only
line 35, the `FROZEN=` pathspec; `ls .ufo/evidence/round-54/ | grep -i verify` is empty, while round 53
carried `.ufo/evidence/round-53/verify-freeze.sh` (and its `.stdout`). So nothing that runs at
decision time compares `freeze.json`'s recorded digests with the committed bytes: F5 passes the
deciding run silently. Remediation: give round 54 the round-53 check — arms 1–3 of the §1 instrument
are exactly what a resume needs — or call it from `deciding-run.sh` before the counters run.

Nothing in §2–§4 is a defect: the seven digests match, the freeze is an ancestor of the measured
revisions, all eleven contract paths are byte-identical across the window, and both counters execute
from the frozen bytes with the C1 numbers reproducing the contract exactly.

## 8. Census (conformance)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
exit=0
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

139 rows (`S001`–`S279`), exit 0. Warnings present are the pre-existing `W04 duplicate url` notices,
unchanged by this seat.

## 9. Live amendment 1 (`7883e0e`) — the freeze moved under this seat

While this seat ran, the lane committed `7883e0e58937d47724b91f1a0475a8785118b696` ("round-54:
amendment 1 — C1 arm 3 discovers the re-key directory from each traced path's directory component").
That commit re-freezes: it rewrites `c1/measure.py`, `contract.json` and `freeze.json`. Re-running
arm 1 against the amended manifest, with the amended commit as FREEZE:

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 - 7883e0e58937d47724b91f1a0475a8785118b696 <<'PY'
  import json, subprocess, hashlib, sys
  H = sys.argv[1]; E = '.ufo/evidence/round-54/'
  def blob(r, p):
      x = subprocess.run(['git', '-C', '.', 'show', '%s:%s' % (r, p)], capture_output=True)
      return x.stdout if x.returncode == 0 else None
  man = json.loads(blob(H, E + 'freeze.json'))
  print('FREEZE %s files=%d amendments=%s' % (H[:12], len(man['files']),
                                              [a['n'] for a in man.get('amendments', [])]))
  bad = 0
  for rel, want in sorted(man['files'].items()):
      got = hashlib.sha256(blob(H, E + rel)).hexdigest(); ok = got == want; bad += not ok
      print('| %s | %s | %s | %s |' % (rel, want, got, 'YES' if ok else 'NO'))
  print('FREEZE_INTEGRITY: %s (%d/%d match)' % ('MISMATCH' if bad else 'OK',
                                                len(man['files']) - bad, len(man['files'])))
  PY

FREEZE 7883e0e58937 files=7 amendments=[1]
| c1/lost-headings-at-base.json | a953d2e87116effc… | a953d2e87116effc… | YES |
| c1/measure.py | 63f5f88147b898ee… | 63f5f88147b898ee… | YES |
| c2/measure.py | b4684a3f555e8cbf… | b4684a3f555e8cbf… | YES |
| contract.json | e15bffb3e888dd39… | fca27997d22414d8… | NO |
| control/controls.sh | 3f1e5f5ce26159d9… | 3f1e5f5ce26159d9… | YES |
| deciding-run.sh | 8a26856a81b6c850… | 8a26856a81b6c850… | YES |
| no-harm.sh | 1aa2fa9df9eac938… | 1aa2fa9df9eac938… | YES |
FREEZE_INTEGRITY: MISMATCH (6/7 match)
```

The amendment updated `c1/measure.py`'s digest and appended its `amendments` entry, but left
`contract.json`'s recorded digest at the pre-amendment value although the same commit rewrote the
contract. The mismatch is unchanged at the latest revision this seat observed,
`3146479c21387dc5affe56f334aba1f770386b61` (the round-record commit): same 6/7, same stale
`e15bffb3…` vs `fca27997…` (`freeze-arm1-at-head-3146479.out`). The original freeze `441c26be` is
internally consistent (7/7, §2); the amended one is not (F5). Full output:
`freeze-arm1-at-amendment-1-7883e0e.out`. The amended counters were not re-run against a decided
revision here — the amendment post-dates this seat's counter window, and the amended `c1/measure.py`
is a different instrument from the one frozen at `441c26be`.

## 10. Receipts

`.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/`

| file | content |
|---|---|
| `freeze-resume-at-c0.out` | arm 1–3 at C0 and both counters from frozen bytes (one run) |
| `freeze-resume-at-head-99c3bc8.out` | arm 1–3 at the live HEAD |
| `freeze-arm1-at-amendment-1-7883e0e.out` | arm 1 at the amended freeze (6/7, `contract.json` stale) |
| `freeze-arm1-at-head-3146479.out` | the same check at the latest observed HEAD (6/7, still stale) |
| `negative-control-A-refreeze.out` | N1: wrong recorded digest → MISMATCH, exit 1 |
| `negative-control-B-postfreeze-drift.out` | N2: frozen body edited after the freeze → MISMATCH, exit 1 |
| `c1-frozen-bytes-at-base.out` | C1 at base, frozen bytes (credited=57 lost=7) |
| `c1-frozen-bytes-at-c0.out` | C1 at C0, frozen bytes (credited=41 lost=23) |
| `c2-frozen-bytes-at-base.out` | C2 at base (usable_ok=6, total=14) |
| `c2-frozen-bytes-at-c0.out` | C2 at C0 (usable_ok=6, total=1) |
| `c2-frozen-bytes-at-head-99c3bc8.out` | C2 at HEAD |
| `registry-check-selftest-untraced-at-base.out` | registry-check --selftest, TMPDIR usable, no strace (exit 0) |
| `registry-check-selftest-under-strace-at-base.out` | the same under `strace -f` (exit 1, 2 timeout cases) |
| `registry-check-selftest-under-strace-at-base-run2.out` | traced re-run, same two cases (exit 1, one with `marker=True`) |
| `census-validate.out` | census validate, exit 0, 139 rows |

Scratch tree removed at the end of the seat.
