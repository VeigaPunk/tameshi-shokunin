# Review: pre-registration preceded every mutant run (round 26, js-cite-check leg)

## Verdict

HOLDS. The frozen contract commit `622d31d90b1fbc55c56e91a2b012bc18d6f1421a` (committer time 2026-10-22T10:01:47Z) precedes the only recorded mutant-run start (MUTATE_DATE 2026-10-22T10:02:07Z, 20 seconds later), and the spec and predictions bytes are identical at `622d31d`, at integration `a08e85c5d7f899e8a5992e20517edb1a380d79eb`, and in the sweep-time copy. `622d31d` is an ancestor of `a08e85c`. No correction needed.

## Named axes

1. Temporal precedence — registration commit time vs mutant run start.
2. Byte immutability — spec and predictions unchanged from registration through integration.
3. Coverage — every mutant run in this leg sits under the pre-registration timestamp.
4. Evidence fidelity — all times and sha256 values below were observed this session, not copied from claims.

## Evidence

### 1. Commit times (command observed this session)

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show -s --format='%H | committer %cI | author %aI | %s' <rev>` returned:

```
622d31d90b1fbc55c56e91a2b012bc18d6f1421a | committer 2026-10-22T07:01:47-03:00 | author 2026-10-22T06:49:39-03:00 | round-26: pre-register claims C1 ... and C2 ...; frozen counters, spec and predictions before any mutant run
a08e85c5d7f899e8a5992e20517edb1a380d79eb | committer 2026-10-22T07:06:40-03:00 | author 2026-10-22T07:06:40-03:00 | round-26: ninth ledger leg js-cite-check (5/10, 10/10 verdict predictions) ...
d4140796f4e48e8ec81b793facba73fbd03b4443 | committer 2026-10-22T06:49:39-03:00 | author 2026-10-22T06:49:39-03:00 | round-25 verifier spot-check ...
```

`git merge-base --is-ancestor 622d31d a08e85c` exited 0: the registration commit is an ancestor of the integration commit.

### 2. Run start time

`.ufo/evidence/round-26/cite-check/sweep/sweep.txt:2`:

```
MUTATE_DATE: 2026-10-22T10:02:07Z
```

In -03:00 terms: registration commit 07:01:47-03:00, then run start 07:02:07-03:00 (20 seconds later). Sweep artifacts were written at 2026-10-22 07:02:31.88 -0300 (`stat` on sweep.txt, results.tsv, defects.tsv), about 24 seconds of sweep wall time — consistent with 11 hermetic runs of roughly 150 ms each plus harness overhead.

### 3. The registration commit is where the spec and predictions first appear

`git log --diff-filter=A --format='%h added %cI %s' --follow -- <path>` resolved both files to exactly one commit:

```
622d31d added 2026-10-22T07:01:47-03:00 round-26: pre-register claims C1 ... before any mutant run
```

No earlier or later adding commit exists for either path.

### 4. Byte identity of spec and predictions (observed sha256)

At `622d31d`, at `a08e85c`, in the working tree, and in the sweep-time copy `sweep/spec.copy`:

| File | sha256 |
|---|---|
| `cite-check.defects.spec` | `969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208` |
| `predictions.json` | `f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e` |

All four spec readings hash identically; all three predictions readings hash identically. The `spec.copy` snapshot written next to the sweep output proves the bytes used at run time equal the pre-registered bytes. (Accessed 2026-10-22.)

### 5. Coverage — every mutant run for this leg

- `grep -c MUTATE_DATE sweep.txt` = 1, at line 2: one sweep invocation.
- `grep -rn MUTATE_DATE .ufo/evidence/round-26/` finds that line only; no second sweep record exists for this leg.
- The invocation covers CONTROL plus 10 defects (5 KILLED, 5 SURVIVED per `sweep/results.tsv`), all children of the single run start at 10:02:07Z. Per-run `.out` files under `sweep/evidence/` carry no embedded timestamps (checked `control.out:1-12`, which begins `kumitate cite-check --selftest` with no date line), so the sweep-start timestamp is the authoritative per-leg record, and it postdates registration.

Corroborating target identity: `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum` = `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, matching `MUTATE_TARGET`, `CONTROL pristine-sha256`, and `MUTATE_RESTORE after` in sweep.txt.

### 6. Watchdog log is not needed

Opened `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` this session (head and tail; 55,442 bytes; last write 2026-10-22 07:43:10 -0300). It records only lane launch/complete events (e.g. line 679: `2026-10-22T06:52:11-03:00 launch tameshi round=26 pgid=2455563`); `grep -in 'tameshi|cite.check|mutat'` finds no per-mutant-run rows. Every timing fact needed for this check comes from git objects and the sweep artifacts, so the watchdog log is not required as evidence.

## Residual risk and verification gaps

- The wall-clock margin between registration commit and run start is only 20 seconds. Both timestamps come from the same host clock, so skew is not a live concern, but the durable proof is the commit object plus the byte-identical `spec.copy`, not the margin itself.
- MUTATE_DATE stamps the sweep invocation, not each of the 11 runs individually; per-run precedence is inherited from the single start time. No evidence suggests any run preceded the sweep start, but individual per-run start times are not recorded anywhere.
- Filesystem mtimes (07:02:31 -0300) are mutable metadata and were used only as corroboration.
- The runner hash recorded in sweep.txt line 1 (`d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`) is the runner as of sweep time; whether it matches the integrated runner is the runner-diff seat's question, not this one.

No tool installs or upgrades were made for this check. All git reads used `GIT_OPTIONAL_LOCKS=0`; no write commands, no `jj`, no edits outside this report.
