# T48A2ExecSixLegReplay — the ledger's tally/exit distribution over eight sequential replays

Seat: executor, round 48 / attempt 2 / a2w1 (calibration axis; C1 feed). Read-only on the lane; one
scratch root `/fast/scratch/hyaku/tameshi-r48/T48A2ExecSixLegReplay`, deleted before exit (verified:
the directory no longer exists; `/fast` 612 G free afterwards). No tool installed, no environment
variable set beyond `TMPDIR=$S`, no lane file written except this report and the receipts beside it.

## 0. What this attacks

| target | where |
|---|---|
| the restated row | `SCORECARD.md:2334` (identical at CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17` and at HEAD `17cc5ce`; the two commits differ only in `.ufo/waves/round-48/spec-a2w1.json`, `a2w1-dispatch.*`, `a2w1.ready` — `git diff --stat c7586b9a..HEAD`) |
| the statement behind it | `.ufo/evidence/round-47/calibration/statements.json`, id `six-leg regression ledger`, `obs ^(REGRESSION: \w+ \(cases=\d+ passed=\d+)`, `cmd_text bash tools/mutate-and-run.sh --regression` |
| the tool | `tools/mutate-and-run.sh`; blobs at HEAD and at `c7586b9a` both hash to `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, prefix `a7d3f2dd7d47` = the pin the row carries (`git show c7586b9a:tools/mutate-and-run.sh | sha256sum`) |

Declared value set, read through the statement's own `obs` plus the row's declared exit:

```
V = { ("REGRESSION: PASS (cases=9 passed=9", 0) }        declared class: stable (one member)
```

Any other `(line, exit)` pair is outside V. Command replayed, per the item, eight times strictly
sequentially, one process at a time:

```bash
S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecSixLegReplay; export TMPDIR=$S
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir "$S/wd$i"   # i=1..8
```

The tool is the lane's own file, never copied: `SELF=$(readlink -f "${BASH_SOURCE[0]}")`
(`tools/mutate-and-run.sh:178`) and `FLEET_ROOT=$(dirname … "$SELF")^3` (`:1358`), so a copy resolves
`FLEET_ROOT` to the scratch dir and every leg refuses at the repo-identity guard — the item is right
that copying it is not an option.

## 1. Result — 8/8 inside V; no out-of-V value observed

| # | start UTC | exit | wall s | load before → after | tally |
|---|---|---|---|---|---|
| 1 | 13:30:03 | 0 | 273.3 | 12.56 → 56.10 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| 2 | 13:34:36 | 0 | 407.1 | 56.10 → 76.69 | same |
| 3 | 13:41:23 | 0 | 346.1 | 76.69 → 73.32 | same |
| 4 | 13:47:09 | 0 | 295.9 | 73.32 → 68.79 | same |
| 5 | 13:52:05 | 0 | 268.3 | 68.79 → 61.39 | same |
| 6 | 13:56:34 | 0 | 250.7 | 61.39 → 58.34 | same |
| 7 | 14:00:44 | 0 | 282.8 | 58.34 → 74.35 | same |
| 8 | 14:05:27 | 0 | 285.3 | 74.35 → 76.53 | same |

Observed frequency of each member (n = 8, my replays only):

| member | exit | count | frequency |
|---|---|---|---|
| `REGRESSION: PASS (cases=9 passed=9` | 0 | 8 | **100 %** |
| `REGRESSION: FAIL (cases=9 passed=8` | 1 | 0 | 0 % |
| `REGRESSION: FAIL (cases=9 passed=7` | 1 | 0 | 0 % |
| `REGRESSION: SETUP …` | 2 | 0 | 0 % |
| `REGRESSION_DEFECT` lines, all runs | — | 0 | — |

**Finding against the declared value set: none.** The row declares one member (`stable`) and eight
sequential replays printed exactly that member with exit 0. Greps for the FAIL face came back empty in
all eight logs: `grep -E '^REGRESSION_CASE .*FAIL'` and `grep -E '^REGRESSION_DEFECT'` match nothing;
all nine `REGRESSION_CASE … PASS` lines are present in every run.

## 2. The instrument is stable below the tally, not only at it

Beyond the tally line, the measured verdict tables did not move: the nine `REGRESSION_SWEEP` lines of
each run — the per-leg `MUTATE: DONE (… killed=… survived=… inconclusive=0 kill-rate=…)` vectors —
hash identically across all eight runs (`sha256` over the 9 lines = `9d7e7c5b1a8916e6…`,
8 of 8 runs). Measured kill vectors, identical every time:

```
js-kimi-census 8/10 · bash-surface-census 8/10 · bash-tsukuroi-census 6/10 · bash-mado-verify 4/10
bash-checklist-run 7/15 · js-claims-check 7/10 · js-round-gate 5/10 · js-sources-check 5/10 · js-cite-check 5/10
```

That is the exact expectation of the ledger (`ktol=0 ftol=0`); no row left its recorded table. The
logs also show each leg's `git show` materialization passing its pin check (a leg that tripped
`pin mismatch` would print `REGRESSION_CASE … SETUP`, and none did), so the bytes replayed are the
pinned bytes. Whole-log diff `run1` vs `run2` differs **only** in `REGRESSION_DATE:` and the
`REGRESSION_WORKDIR*` path lines (`wd1` vs `wd2`); same for `run1` vs `run5`.

## 3. Reading this against C1 (what the numbers do and do not buy)

- Under amendment 4, the `(line, exit)` tuple a P0 observation prints is the attestation carrier. If
  the deciding invocation prints `PASS (cases=9 passed=9|0`, then the row's single member is attested
  by that run and no extra observation is needed to declare it. My eight replays are *consistent*
  with the declared row: they add eight more organic P0-shaped observations of the declared member.
- They do **not**, and cannot, attest the FAIL member: the row declares `stable` = one member, so
  every one of these eight tuples is inside V, and none is the second member. A sample that never
  leaves V never widens V.
- They also cannot retire the w1 counter-receipt that did leave it: `.ufo/waves/round-48/w1/
  T48ExecObs2.md` (§ *Run 2*, `PROFILES` line, `P0=REGRESSION: FAIL (cases=9 passed=8|1`) and the
  w1 replay B in `.ufo/waves/round-48/w1/T48RevenRegression.md` (§2). Both are prior data; my 8
  PASSes do not un-observe them. Pooled naïvely, the lane now holds 10 disclosed full replays of this
  command at host environment with 1 FAIL (9 PASS), plus w1's 4/40 standalone selftest failures and
  the a2 peer's 330-run, 1.5 %/run measurement
  (`.ufo/waves/round-48/a2w1/T48A2RevenSigpipePair.md`) — i.e. the failure is rare per run and my
  zero is what a ~1.5 % per-run rate predicts in 8 draws (`0.985^8 ≈ 0.886`).
- Practical consequence for the deciding run, stated as a number and not a verdict: this sample
  supports the row's declared member as the *typical* outcome; it does not make the single deciding
  invocation safe, and per the contract a FAIL printed there is a mismatch, not a rerun.

## 4. Fidelity of these replays to the counter's P0

- Same tool bytes: the tool at the content revision hashes to the row's pin (§0), and the legs
  re-verify their own pins at replay time (§2).
- Fleet root is the real `/home/vgpnk/Projects/shokunin`, where the pinned sibling lanes live, not the
  counter's synthetic mirror (`measure.py:303-318` symlinks sibling lanes into `<work>/P0/fleet` and
  clones the lane). The legs resolve `repo = FLEET_ROOT/<lane>` and require each lane to be its own
  repository, which holds in both arrangements; the pin checks confirm identical blobs. **Caveat
  (disclosed):** the two arrangements differ in the fleet-root path string, the parent repo above it,
  and the mirror is a fresh clone at the content revision rather than my working tree — but my working
  tree's `tools/` and `SCORECARD.md` are byte-identical to the content revision, so the replay target
  is the same.
- Environment: my replays ran under the host environment (P0-shaped), not under the counter's
  `env -i`-style profiles P1-P5, so nothing here speaks to those.
- Not a quiet host: loads 12.6 → 76.7 with other round-48 a2 seats and the L1 deciding run live —
  the same concurrency class the row's disclosure blames, yet 8/8 PASS.

## 5. Risks / limits

1. n = 8. At the peer's 1.5 %/run, the 95 % upper bound on the per-run FAIL rate given 0/8 is ≈ 31 %
   (rule of three), so this sample bounds nothing tightly; it is a distribution snapshot, not a rate.
2. One environment only (host P0): no P1-P5 evidence here.
3. Wall time spread 250.7-407.1 s (1.6× across eight runs at load 58-77) is load sensitivity, not
   instability of the result; the statement timeout is 2700 s, so no timeout exposure was observed.
4. My runs are probes, not the verdict. The lane's deciding invocation is the L1's, and a probe is
   never a verdict.
5. Repeat of the disclosure, not a new defect: the row's `stable` rests on one attested member while
   two prior receipts in this round show a FAIL member. If the deciding run prints FAIL, that is a
   mismatch under the contract as written; the successor question (re-pin the tsukuroi leg or declare
   `nondeterministic`) is already parked for round 49 at `SCORECARD.md:2367`.

## 6. Retained evidence (all beside this report)

| file | bytes | sha256 |
|---|---|---|
| `T48A2ExecSixLegReplay.tallies.txt` | 18304 | `6fc5db7835a308f63483919a7792f4d65cded83a4691a99cf7085cf7bf5dee7f` |
| `T48A2ExecSixLegReplay.run1.log` | 7175 | `5566afa0c48c5aadc583d3f46f2948dc6f9bd7d37088a5c42c60865dcd29e7fc` |
| `T48A2ExecSixLegReplay.run2.log` | 7175 | `0fa701bb76da8915a530cb190295fb9c61b87a7c5f6ba9db0c54ee2a31e666b8` |
| `T48A2ExecSixLegReplay.run3.log` | 7175 | `7d6259507e6b0b24bf6877eb9c0b40eb7898334fc37dc1cddfc7c4f376e3ed90` |
| `T48A2ExecSixLegReplay.run4.log` | 7175 | `b6d2b34fb3dde65ad474a54359ccce7cabc344b0d47208447d8c7d9dcc2bc39d` |
| `T48A2ExecSixLegReplay.run5.log` | 7175 | `9795868ffccf6b1cb769fc7bd34719b01fbb621271e8d0b7694f59046e36830e` |
| `T48A2ExecSixLegReplay.run6.log` | 7175 | `ebea52c031a168ccee8a5fcf6142d98f51d927310b9879d754ee770e863f4ecb` |
| `T48A2ExecSixLegReplay.run7.log` | 7175 | `628a9ebb811381920f32962e88e79f34ba867f3cf39f0dbc5b32c08302247b8f` |
| `T48A2ExecSixLegReplay.run8.log` | 7175 | `4ea1cdf19ac6f599f516216a8b63b0db6e5ea9f0906a5ec5d9a481704b45f4df` |

`T48A2ExecSixLegReplay.tallies.txt` is the driver's raw per-replay record (start/end UTC, exit, wall
ms, `/proc/loadavg` and `uptime` before/after, tool sha256 line, workdir + size, tally line, all nine
`REGRESSION_CASE` lines, the `REGRESSION_DEFECT` grep, log sha prefix), bracketed by a header that
states the declared V and the observed distribution and a footer with the full log fingerprints. Each
`wd$i` (7136 KiB) was removed immediately after its tally line was extracted; the scratch root itself
was removed before this report was written.

Lane cleanliness after the replays: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status
--porcelain -- corpus tools SCORECARD.md` printed nothing. No git or jj command in the lane was run
beyond read-only `rev-parse`/`log`/`diff`/`show`/`status`.
