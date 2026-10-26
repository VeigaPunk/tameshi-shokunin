# T48A2ExecC1SerialA — C1 serial probe, group A (one variable: worker count)

Seat `T48A2ExecC1SerialA`, executor, axes: calibration. Milestone: C1 serial probe group A (a2w1).
Date 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`473336d9d789f6081195e7376d17836a24666bc3`, CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`.
Counter `.ufo/evidence/round-48/calibration/measure.py` sha256
`572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` (equals the blob at REV and
freeze-2.json); statements pin `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56`
(equals REV and freeze-2). Read-only seat: no lane source, tool, corpus or SCORECARD.md write.

## Command (exactly the assigned probe, `--jobs 1`)

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 \
  --base 473336d9d789f6081195e7376d17836a24666bc3 \
  --work "$S/w" --jobs 1 \
  --only "sources-registry,depth,calibration,freshness,mutation sweep runner"
```

`S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1SerialA`, `TMPDIR=$S`. Three rounds, six profiles
P0-P5, five statements, 90 invocations, strictly one worker.

## Observed result

- Label: `C1_R48_PARTIAL` (a probe, never a verdict: `--only` forces `partial` and
  `C1_R48_PASS=false` at `measure.py:570-575`). Exit **1** for that reason, not for a mismatch.
- Wall time **1171 s** (19 min 31 s), START `2026-10-26T13:30:09Z`, END `2026-10-26T13:49:40Z`,
  stderr empty.
- Verdict line (verbatim):

```
C1_R48_PARTIAL: self_pin=1 stmts_pin=1 statements=5 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1 base=473336d9d789f6081195e7376d17836a24666bc3 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R48_PASS=false
```

No `EXTRA` line was printed (`attested_extra=0`): no declared member was missing, so no extra P0
attestation observation was taken.

## Per-row verdict: does the serial run contradict the restated row?

For every row: no P0 tuple outside V, no unattested declared member, no dependence outside D.

| statement | row | declared V (class, sha, deps) | serial P0 r1 / r2 / r3 | verdict |
|---|---|---|---|---|
| sources-registry | SCORECARD.md:2332 | `rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0; stable; `b9b754713c9c`; `none` | same tuple, exit 0, in all three rounds (and P1-P5) | `MATCH` / `DEPS-OK` |
| mutation sweep runner | SCORECARD.md:2333 | `MUTATE_SELFTEST: 106/106 pass`, exit 0; stable; `a7d3f2dd7d47`; `none` | same tuple, exit 0, in all three rounds (and P1-P5) | `MATCH` / `DEPS-OK` |
| depth | SCORECARD.md:2354 | `9`; stable; `a7d3f2dd7d47`; `none` | 9 / 9 / 9 (and P1-P5) | `MATCH` / `DEPS-OK` |
| calibration | SCORECARD.md:2355 | `6`; stable; `657f009bdf1c`; `none` | 6 / 6 / 6 (and P1-P5) | `MATCH` / `DEPS-OK` |
| freshness | SCORECARD.md:2356 | `9`; stable; `ba64041f49ff`; `none` | 9 / 9 / 9 (and P1-P5) | `MATCH` / `DEPS-OK` |

Dependence read-out for all five: `required=none unstable=none never=bwrap,env,fleet-root,jj,node`,
declared `none` — i.e. the serial run reproduces exactly the emit's dependence picture (P2-P5
tuples equal P1 for these five); nothing observed in all three rounds is missing from D and nothing
declared is unobserved. `self_pin=1 stmts_pin=1 append_only=1 unpinned=0`.

## Nondeterministic rows and the worker-count question

None of the five statements in this group declares `nondeterministic`: all five rows declare
`stable` with one member, and the serial run observed exactly that one member in every round and
every profile. So "serial execution saw fewer members than the declared class" cannot arise here —
the declared class has one member, and that member was seen 3/3 rounds (and 6/6 profiles) at
`--jobs 1`. Serial execution adds no member and removes none.

## One-variable pair (QUALITY 96): same group at `--jobs 6`

The sibling seat probing the same group at the counter default (`T48W2ExecC1ProbeA`, `--jobs 6`;
no other flag differs) published, for the same COMMAND minus `--jobs 1`:

| variable | wall | tuples (P0-P5, r1-r3) | verdict components |
|---|---|---|---|
| `--jobs 6` (default) | 195 s | one member per statement, identical to the declared one | `total=0 mismatches=0 unattested=0 dep_mismatch=0 attested_extra=0 fleet_drift=0 sibling_moves=1` |
| `--jobs 1` (this seat) | 1171 s (6.0x) | same | same |

One variable changed (worker count) and the observed tuples did not change: for this group the
restated `stable` classes are not concurrency-driven, and the row values are not artifacts of
running six statements in parallel. Caveats, stated so the pair is not over-read: one invocation
per side (the kill rule forbids a second deciding run, and repeat probing would not be a verdict);
wall time is the only quantity the variable moved and it is confounded by the sibling seats that
were running inside both windows; `--jobs 1` removes intra-invocation concurrency, not host load,
so P0 (the live host environment) still runs under the fleet's load. The group contains none of the
statements disclosed as concurrency-sensitive (that is `six-leg regression ledger`, group B).

## Fleet state observed in this run

Four FLEET points: `census_sha=3fb7261569f4` constant, `lane_clean=1` at all four,
`fleet_drift=0`, `sibling_moves=1` (`souji-shokunin` `d805d1d61324` -> `9da5e9a559f7` between
points 2 and 3, disclosed as a move, not drift). Contrast with the author's emit receipt
(`emit-15b1521.stdout`), which printed `lane_clean=0` at points 2-4 while its tree was being
edited; this read-only seat's probe is clean at every point.

## Static corroboration (read-only reads, no extra probe run)

- `corpus/SOURCES.md` row count at REV under the census regex = **128** (base 124; +4 = S265-S268
  from commit `5054532`), so `rows=128` is the content-revision value, not a stale base value.
- Pinned tool prefixes at REV: `b9b754713c9c` (sources-census-v2.sh), `a7d3f2dd7d47`
  (mutate-and-run.sh), `657f009bdf1c` (round-21 coldread/measure.py), `ba64041f49ff`
  (round-45 freshness/measure.py) — equal to the declared prefixes in the five rows.
- `append_only=1`: the base SCORECARD.md is a byte prefix of the REV one.

## Findings

No finding against the five rows in this group: serial execution reproduces every declared member,
class, tool prefix and deps set.

F1 (context, cross-referenced from a sibling; not my measurement): `SCORECARD.md:2355`
(calibration row prose) says "60 of 64 sections credited", while `T48W2ExecC1ProbeA` measured 57
credited at REV (score value 6 unchanged). My run corroborates only the value (`calibration` = 6
in all 18 observations) and not the section count. Per that seat, the three lost credits trace to
commit `5054532` changing input files of three cold-read sections, and
`deciding-run.sh`'s `COLDREAD_SECTIONS_CREDITED>=60` check would then be red at REV [INFERENCE from
the sibling's measured 57; that script was not run here]. `SCORECARD.md` is under this seat's write
ban; disposition is the L1's.

## Limits

- One probe invocation only; this is not the deciding run and cannot become one.
- P0 runs in this shell's host environment (`host_env()` filters only `GIT_*`; `TMPDIR=$S`), so P0
  tuples include my environment, as the counter intends.
- `--jobs 1` measures intra-invocation serialization only; the fleet's other seats were live
  throughout both probe windows.

## Files changed

- `.ufo/waves/round-48/a2w1/T48A2ExecC1SerialA.md` (this report)
- `.ufo/waves/round-48/a2w1/T48A2ExecC1SerialA.stdout` (verbatim stdout; sha256
  `74ad6eac8b19c0d5b71498a8f0b1b8bd1d0c030800871dee830db6a0b2e0e4ec`, 6581 bytes, 28 lines)
- `.ufo/waves/round-48/a2w1/T48A2ExecC1SerialA.timing` (start/end/wall)

Cleanliness: no edit to corpus/, tools/, SCORECARD.md or any lane source; no mutating git or jj
command; scratch `/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1SerialA` deleted after copying the
receipts (verified absent below). Disk guard read before the pass: `/fast/scratch/hyaku` 23% used,
621.4G free. Tooling: nothing installed or upgraded (note: `/usr/bin/time` is absent on this host;
the first launch failed `rc=127` and the run was restarted with shell `date +%s` timing — wall time
above is from that restart).

## Verbatim stdout (28 lines)

```
FLEET point=1 census_sha=3fb7261569f4 lane_clean=1 siblings=audio-shokunin@7a2fcd4f0883,chousa-shokunin@00f8c7f5272a,game-dev-2d-shokunin@7753d49b1667,game-dev-3d-shokunin@89dd182b7094,kagi-shokunin@69b61db46be4,kaidoku-shokunin@a2f64e1da78a,kake-shokunin@044048597d62,kama-shokunin@0163fea2dab3,kasegi-shokunin@cc692008b0cf,kengaku-shokunin@d3a6277f1884,kotoba-shokunin@65a5c7a66324,kotodama-shokunin@f556d1049fe6,kumitate-shokunin@8d557f85312d,lore-shokunin@380ef3abc7c7,mado-shokunin@6a1a90528fe5,mori-shokunin@4548a34dc8b4,revenger-shokunin@6da884c6708f,souji-shokunin@4e56c48b8fc8,tabi-shokunin@d805d1d61324,tsukuroi-shokunin@8b7c41326801
FLEET point=2 census_sha=3fb7261569f4 lane_clean=1 siblings=audio-shokunin@7a2fcd4f0883,chousa-shokunin@00f8c7f5272a,game-dev-2d-shokunin@7753d49b1667,game-dev-3d-shokunin@89dd182b7094,kagi-shokunin@69b61db46be4,kaidoku-shokunin@a2f64e1da78a,kake-shokunin@044048597d62,kama-shokunin@0163fea2dab3,kasegi-shokunin@cc692008b0cf,kengaku-shokunin@d3a6277f1884,kotoba-shokunin@65a5c7a66324,kotodama-shokunin@f556d1049fe6,kumitate-shokunin@8d557f85312d,lore-shokunin@380ef3abc7c7,mado-shokunin@6a1a90528fe5,mori-shokunin@4548a34dc8b4,revenger-shokunin@6da884c6708f,souji-shokunin@9da5e9a559f7,tabi-shokunin@d805d1d61324,tsukuroi-shokunin@8b7c41326801
FLEET point=3 census_sha=3fb7261569f4 lane_clean=1 siblings=audio-shokunin@7a2fcd4f0883,chousa-shokunin@00f8c7f5272a,game-dev-2d-shokunin@7753d49b1667,game-dev-3d-shokunin@89dd182b7094,kagi-shokunin@69b61db46be4,kaidoku-shokunin@a2f64e1da78a,kake-shokunin@044048597d62,kama-shokunin@0163fea2dab3,kasegi-shokunin@cc692008b0cf,kengaku-shokunin@d3a6277f1884,kotoba-shokunin@65a5c7a66324,kotodama-shokunin@f556d1049fe6,kumitate-shokunin@8d557f85312d,lore-shokunin@380ef3abc7c7,mado-shokunin@6a1a90528fe5,mori-shokunin@4548a34dc8b4,revenger-shokunin@6da884c6708f,souji-shokunin@4ea897fe95d5,tabi-shokunin@d805d1d61324,tsukuroi-shokunin@8b7c41326801
FLEET point=4 census_sha=3fb7261569f4 lane_clean=1 siblings=audio-shokunin@7a2fcd4f0883,chousa-shokunin@00f8c7f5272a,game-dev-2d-shokunin@7753d49b1667,game-dev-3d-shokunin@89dd182b7094,kagi-shokunin@69b61db46be4,kaidoku-shokunin@a2f64e1da78a,kake-shokunin@044048597d62,kama-shokunin@0163fea2dab3,kasegi-shokunin@cc692008b0cf,kengaku-shokunin@d3a6277f1884,kotoba-shokunin@65a5c7a66324,kotodama-shokunin@f556d1049fe6,kumitate-shokunin@8d557f85312d,lore-shokunin@380ef3abc7c7,mado-shokunin@6a1a90528fe5,mori-shokunin@4548a34dc8b4,revenger-shokunin@6da884c6708f,souji-shokunin@4ea897fe95d5,tabi-shokunin@d805d1d61324,tsukuroi-shokunin@8b7c41326801
STATEMENT cap/sources-registry: claimed=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 sha=b9b754713c9c ROUNDS r1=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 r2=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 r3=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT cap/mutation sweep runner: claimed=MUTATE_SELFTEST: 106/106 pass|0 sha=a7d3f2dd7d47 ROUNDS r1=MUTATE_SELFTEST: 106/106 pass|0 r2=MUTATE_SELFTEST: 106/106 pass|0 r3=MUTATE_SELFTEST: 106/106 pass|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT axis/depth: claimed=9 sha=a7d3f2dd7d47 ROUNDS r1=9 r2=9 r3=9 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT axis/calibration: claimed=6 sha=657f009bdf1c ROUNDS r1=6 r2=6 r3=6 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT axis/freshness: claimed=9 sha=ba64041f49ff ROUNDS r1=9 r2=9 r3=9 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
ROUND 1
PROFILES sources-registry: P0=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P1=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P2=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P3=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P4=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P5=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0
PROFILES mutation sweep runner: P0=MUTATE_SELFTEST: 106/106 pass|0 P1=MUTATE_SELFTEST: 106/106 pass|0 P2=MUTATE_SELFTEST: 106/106 pass|0 P3=MUTATE_SELFTEST: 106/106 pass|0 P4=MUTATE_SELFTEST: 106/106 pass|0 P5=MUTATE_SELFTEST: 106/106 pass|0
PROFILES depth: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
PROFILES calibration: P0=6 P1=6 P2=6 P3=6 P4=6 P5=6
PROFILES freshness: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
ROUND 2
PROFILES sources-registry: P0=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P1=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P2=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P3=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P4=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P5=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0
PROFILES mutation sweep runner: P0=MUTATE_SELFTEST: 106/106 pass|0 P1=MUTATE_SELFTEST: 106/106 pass|0 P2=MUTATE_SELFTEST: 106/106 pass|0 P3=MUTATE_SELFTEST: 106/106 pass|0 P4=MUTATE_SELFTEST: 106/106 pass|0 P5=MUTATE_SELFTEST: 106/106 pass|0
PROFILES depth: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
PROFILES calibration: P0=6 P1=6 P2=6 P3=6 P4=6 P5=6
PROFILES freshness: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
ROUND 3
PROFILES sources-registry: P0=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P1=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P2=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P3=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P4=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 P5=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0
PROFILES mutation sweep runner: P0=MUTATE_SELFTEST: 106/106 pass|0 P1=MUTATE_SELFTEST: 106/106 pass|0 P2=MUTATE_SELFTEST: 106/106 pass|0 P3=MUTATE_SELFTEST: 106/106 pass|0 P4=MUTATE_SELFTEST: 106/106 pass|0 P5=MUTATE_SELFTEST: 106/106 pass|0
PROFILES depth: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
PROFILES calibration: P0=6 P1=6 P2=6 P3=6 P4=6 P5=6
PROFILES freshness: P0=9 P1=9 P2=9 P3=9 P4=9 P5=9
C1_R48_PARTIAL: self_pin=1 stmts_pin=1 statements=5 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1 base=473336d9d789f6081195e7376d17836a24666bc3 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R48_PASS=false
```

Scratch removed after the receipts were copied: `rm -rf -- /fast/scratch/hyaku/tameshi-r48/T48A2ExecC1SerialA`
followed by `test ! -e` on the same path, which printed `scratch absent:
/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1SerialA`.
