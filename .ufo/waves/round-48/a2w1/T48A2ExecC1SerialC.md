# T48A2ExecC1SerialC — C1 serial (`--jobs 1`) probe of the five-statement group C

Seat: T48A2ExecC1SerialC (executor, leaf), round 48 / attempt 2 / wave a2w1, calibration axis (C1 feed).
Lane: `tameshi-shokunin`, read-only. base `473336d9d789f6081195e7376d17836a24666bc3`,
CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`. Counter: frozen
`.ufo/evidence/round-48/calibration/measure.py` (sha256 `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3`,
freeze-2.json). One variable moved against the sibling seats: `--jobs 1` instead of the default `6`.
Counter executed only as a `--only` probe (label `C1_R48_PARTIAL`); a probe is never a verdict.

Deliverables: this report and `.ufo/waves/round-48/a2w1/T48A2ExecC1SerialC.stdout` (verbatim stdout,
28 lines, sha256 `5ba1f350060c6b7ec7c4b093a8d778ad24b475eaa994e1ba1aca3bfbca0f7b39`, 8022 bytes).
No tool installed or upgraded. No file under `corpus/`, `tools/` or `SCORECARD.md` touched.

## 1. Verdict

**No row of this group is contradicted by the serial observation.** All five restated standing rows
MATCH at `--jobs 1`: every P0 tuple seen in the three rounds is the declared single member, no member
is left unattested (`attested_extra=0`, `attested=0` shortfall), and no dependence falls outside the
declared set (`dep_mismatch=0`). The partial line reads `total=0 mismatches=0 unparsed=0 unobservable=0
dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1`.

The one-variable pair is clean: a sibling probe of the same five statements at the counter's default
`--jobs 6` (`T48W2ExecC1ProbeC.stdout`) is **byte-identical apart from two `FLEET` sibling lines**, so
for this group concurrency moves nothing at all — the rows' `stable` class is not load-dependent.
Two hygiene findings are reported in §7 (the counter does not echo `--jobs`; the
`effective expectation reconciliation` tool hard-codes `/tmp` fixtures and keeps them on failure).

## 2. Invocation, environment and measurements

```
S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1SerialC; export TMPDIR="$S"
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 \
  --base 473336d9d789f6081195e7376d17836a24666bc3 \
  --work "$S/w" --jobs 1 \
  --only "effective expectation reconciliation,retained invocation-context gate,hermetic env-differential probe,callback-authoritative wave accounting,required-command-receipt-binding"
```

- wall time **306.6 s** (`date +%s.%N` before/after), run window 2026-10-26 ~10:30:26–10:35:33 -0300.
- exit **1** — required: `--only` forces the partial label and `C1_R48_PASS=false`
  (`measure.py:578-582`), so exit 1 is the probe's contract, not a failure of the rows.
- stderr: **empty** (0 bytes).
- work dir under `/fast/scratch`, never `/tmp` (the counter refuses `/tmp`, `measure.py:396`;
  the round-47 `env-diff` P1 collision recorded in `w1/T48RevenEnvDiff.md` therefore cannot appear here).
- `FLEET` census script sha `3fb7261569f4` identical at all four points; `lane_clean=1` at all four;
  one sibling moved (below). Disk guard checked before the pass (`/fast` 619 G free) and after
  (`/fast` 602 G free, `/tmp` 126 G free); no ENOSPC.

## 3. Counter stdout, verbatim

`FLEET` points 1–4 (abridged here to the fields that move; the full lines are in the `.stdout`
deliverable, one line each):

```
FLEET point=1 census_sha=3fb7261569f4 lane_clean=1 siblings=…,souji-shokunin@4e56c48b8fc8,…
FLEET point=2 census_sha=3fb7261569f4 lane_clean=1 siblings=…,souji-shokunin@9da5e9a559f7,…
FLEET point=3 census_sha=3fb7261569f4 lane_clean=1 siblings=…,souji-shokunin@9da5e9a559f7,…
FLEET point=4 census_sha=3fb7261569f4 lane_clean=1 siblings=…,souji-shokunin@9da5e9a559f7,…
```

`STATEMENT` lines (5, verbatim):

```
STATEMENT cap/effective expectation reconciliation: claimed=SELFTEST: PASS (66/66)|0 sha=39ee5c5effd9 ROUNDS r1=SELFTEST: PASS (66/66)|0 r2=SELFTEST: PASS (66/66)|0 r3=SELFTEST: PASS (66/66)|0 DEPS required=jj unstable=none never=bwrap,env,fleet-root,node declared=jj MATCH DEPS-OK
STATEMENT cap/retained invocation-context gate: claimed=SELFTEST: PASS (49/49)|0 sha=7e4519d9a0ea ROUNDS r1=SELFTEST: PASS (49/49)|0 r2=SELFTEST: PASS (49/49)|0 r3=SELFTEST: PASS (49/49)|0 DEPS required=fleet-root unstable=none never=bwrap,env,jj,node declared=fleet-root MATCH DEPS-OK
STATEMENT cap/hermetic env-differential probe: claimed=ENVDIFF_SELFTEST: 9/9 pass|0 sha=e8b47ab7cf23 ROUNDS r1=ENVDIFF_SELFTEST: 9/9 pass|0 r2=ENVDIFF_SELFTEST: 9/9 pass|0 r3=ENVDIFF_SELFTEST: 9/9 pass|0 DEPS required=bwrap,node unstable=none never=env,fleet-root,jj declared=bwrap,node MATCH DEPS-OK
STATEMENT cap/callback-authoritative wave accounting: claimed=ACCOUNTING_SELFTEST: 8/8 pass|0 sha=96b3038a77f8 ROUNDS r1=ACCOUNTING_SELFTEST: 8/8 pass|0 r2=ACCOUNTING_SELFTEST: 8/8 pass|0 r3=ACCOUNTING_SELFTEST: 8/8 pass|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT cap/required-command-receipt-binding: claimed=COMMAND_BINDING_SELFTEST: 44/44 pass|0 sha=9230c68e53a5 ROUNDS r1=COMMAND_BINDING_SELFTEST: 44/44 pass|0 r2=COMMAND_BINDING_SELFTEST: 44/44 pass|0 r3=COMMAND_BINDING_SELFTEST: 44/44 pass|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
```

`EXTRA` lines: **none printed** — no member needed the post-round extra observations
(`attested_extra=0`; amendment 4's extra path was never entered).

`PROFILES` lines (18, verbatim; rounds 1–3):

```
ROUND 1
PROFILES effective expectation reconciliation: P0=SELFTEST: PASS (66/66)|0 P1=SELFTEST: PASS (66/66)|0 P2=SELFTEST: PASS (66/66)|0 P3=- P4=SELFTEST: PASS (66/66)|0 P5=SELFTEST: PASS (66/66)|0
PROFILES retained invocation-context gate: P0=SELFTEST: PASS (49/49)|0 P1=SELFTEST: PASS (49/49)|0 P2=SELFTEST: PASS (49/49)|0 P3=SELFTEST: PASS (49/49)|0 P4=SELFTEST: PASS (49/49)|0 P5=SELFTEST: PASS (49/49)|1
PROFILES hermetic env-differential probe: P0=ENVDIFF_SELFTEST: 9/9 pass|0 P1=ENVDIFF_SELFTEST: 9/9 pass|0 P2=ENVDIFF_SELFTEST: 2/9 pass|1 P3=ENVDIFF_SELFTEST: 9/9 pass|0 P4=ENVDIFF_SELFTEST: 8/9 pass|1 P5=ENVDIFF_SELFTEST: 9/9 pass|0
PROFILES callback-authoritative wave accounting: P0=ACCOUNTING_SELFTEST: 8/8 pass|0 P1=ACCOUNTING_SELFTEST: 8/8 pass|0 P2=ACCOUNTING_SELFTEST: 8/8 pass|0 P3=ACCOUNTING_SELFTEST: 8/8 pass|0 P4=ACCOUNTING_SELFTEST: 8/8 pass|0 P5=ACCOUNTING_SELFTEST: 8/8 pass|0
PROFILES required-command-receipt-binding: P0=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P1=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P2=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P3=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P4=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P5=COMMAND_BINDING_SELFTEST: 44/44 pass|0
ROUND 2
PROFILES effective expectation reconciliation: P0=SELFTEST: PASS (66/66)|0 P1=SELFTEST: PASS (66/66)|0 P2=SELFTEST: PASS (66/66)|0 P3=- P4=SELFTEST: PASS (66/66)|0 P5=SELFTEST: PASS (66/66)|0
PROFILES retained invocation-context gate: P0=SELFTEST: PASS (49/49)|0 P1=SELFTEST: PASS (49/49)|0 P2=SELFTEST: PASS (49/49)|0 P3=SELFTEST: PASS (49/49)|0 P4=SELFTEST: PASS (49/49)|0 P5=SELFTEST: PASS (49/49)|1
PROFILES hermetic env-differential probe: P0=ENVDIFF_SELFTEST: 9/9 pass|0 P1=ENVDIFF_SELFTEST: 9/9 pass|0 P2=ENVDIFF_SELFTEST: 2/9 pass|1 P3=ENVDIFF_SELFTEST: 9/9 pass|0 P4=ENVDIFF_SELFTEST: 8/9 pass|1 P5=ENVDIFF_SELFTEST: 9/9 pass|0
PROFILES callback-authoritative wave accounting: P0=ACCOUNTING_SELFTEST: 8/8 pass|0 P1=ACCOUNTING_SELFTEST: 8/8 pass|0 P2=ACCOUNTING_SELFTEST: 8/8 pass|0 P3=ACCOUNTING_SELFTEST: 8/8 pass|0 P4=ACCOUNTING_SELFTEST: 8/8 pass|0 P5=ACCOUNTING_SELFTEST: 8/8 pass|0
PROFILES required-command-receipt-binding: P0=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P1=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P2=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P3=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P4=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P5=COMMAND_BINDING_SELFTEST: 44/44 pass|0
ROUND 3
PROFILES effective expectation reconciliation: P0=SELFTEST: PASS (66/66)|0 P1=SELFTEST: PASS (66/66)|0 P2=SELFTEST: PASS (66/66)|0 P3=- P4=SELFTEST: PASS (66/66)|0 P5=SELFTEST: PASS (66/66)|0
PROFILES retained invocation-context gate: P0=SELFTEST: PASS (49/49)|0 P1=SELFTEST: PASS (49/49)|0 P2=SELFTEST: PASS (49/49)|0 P3=SELFTEST: PASS (49/49)|0 P4=SELFTEST: PASS (49/49)|0 P5=SELFTEST: PASS (49/49)|1
PROFILES hermetic env-differential probe: P0=ENVDIFF_SELFTEST: 9/9 pass|0 P1=ENVDIFF_SELFTEST: 9/9 pass|0 P2=ENVDIFF_SELFTEST: 2/9 pass|1 P3=ENVDIFF_SELFTEST: 9/9 pass|0 P4=ENVDIFF_SELFTEST: 8/9 pass|1 P5=ENVDIFF_SELFTEST: 9/9 pass|0
PROFILES callback-authoritative wave accounting: P0=ACCOUNTING_SELFTEST: 8/8 pass|0 P1=ACCOUNTING_SELFTEST: 8/8 pass|0 P2=ACCOUNTING_SELFTEST: 8/8 pass|0 P3=ACCOUNTING_SELFTEST: 8/8 pass|0 P4=ACCOUNTING_SELFTEST: 8/8 pass|0 P5=ACCOUNTING_SELFTEST: 8/8 pass|0
PROFILES required-command-receipt-binding: P0=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P1=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P2=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P3=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P4=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P5=COMMAND_BINDING_SELFTEST: 44/44 pass|0
```

No tuple in this run is unstable: for all five statements the six profiles printed the identical tuple
in all three rounds (30 observed tuples, 0 moved). `hermetic env-differential probe` P4 is `8/9 pass|1`
in every round — the thin required `node` dependence traced in `w1/T48RevenEnvDiff.md` §1.2
(`pin-mismatch-public-cli` fails without node), not a flaky observation; P2 is `2/9 pass|1` in every
round (bwrap absent).

Final line, verbatim:

```
C1_R48_PARTIAL: self_pin=1 stmts_pin=1 statements=5 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1 base=473336d9d789f6081195e7376d17836a24666bc3 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R48_PASS=false
```

`sibling_moves=1` is `souji-shokunin` `4e56c48b8fc8 → 9da5e9a559f7` between FLEET point 1 and point 2 —
disclosed, not drift (amendment 5); `census_sha` and `lane_clean` never moved.

## 4. Per-row answers (P0 outside V? unattested member? dependence outside D?)

| row | V (declared) | serial P0, r1/r2/r3 | outside V | unattested | deps D vs observed | verdict |
|---|---|---|---|---|---|---|
| effective expectation reconciliation | `SELFTEST: PASS (66/66)`/0, stable | same ×3 | no | no (`attested_extra=0`) | `jj` ⊇ `{jj}` | MATCH DEPS-OK |
| retained invocation-context gate | `SELFTEST: PASS (49/49)`/0, stable | same ×3 | no | no | `fleet-root` ⊇ `{fleet-root}` | MATCH DEPS-OK |
| hermetic env-differential probe | `ENVDIFF_SELFTEST: 9/9 pass`/0, stable | same ×3 | no | no | `bwrap,node` ⊇ `{bwrap,node}` | MATCH DEPS-OK |
| callback-authoritative wave accounting | `ACCOUNTING_SELFTEST: 8/8 pass`/0, stable | same ×3 | no | no | `none` ⊇ `{}` | MATCH DEPS-OK |
| required-command-receipt-binding | `COMMAND_BINDING_SELFTEST: 44/44 pass`/0, stable | same ×3 | no | no | `none` ⊇ `{}` | MATCH DEPS-OK |

Static cross-check of the four `tool sha256` prefixes at the measured revision (independent of the
counter, `git show rev:path | sha256sum`):

```
tools/evidence-disposition.py     rev=39ee5c5effd9 base=39ee5c5effd9
.ufo/evidence/round-15/verify.py  rev=7e4519d9a0ea base=7e4519d9a0ea
tools/env-diff.py                 rev=e8b47ab7cf23 base=e8b47ab7cf23
tools/wave-accounting.py          rev=96b3038a77f8 base=96b3038a77f8
tools/command-binding.py          rev=9230c68e53a5 base=9230c68e53a5
```

All five equal the section's evidence cells (`SCORECARD.md:2338-2342`) and are unchanged between base
and CONTENT, so `sha=` and the pinned blob agree.

The dependence mechanisms are visible in the raw observation files the counter keeps per profile
(`$S/w/round1/P*/obs-*.stdout`, quoted before scratch deletion):

- `effective expectation reconciliation`, P3 (jj removed) — `-` because the tool prints a FAIL line:
  `SELFTEST: FAIL (3/66 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest._6lwo0ym)`.
- `retained invocation-context gate`, P5 (decoy fleet root) — exit 1, failing on the census stub:
  `sources-census: FAIL exit=7 (expected 0)` / `sources-census-ok-line: FAIL ok line absent`
  (the counter's decoy stub is `exit 7`).
- `hermetic env-differential probe`, P2 (bwrap absent) — `ENVDIFF_SELFTEST: 2/9 pass`, exit 1;
  P4 (node absent) — r1/r3 `8/9 pass` exit 1 with `ENVDIFF_CASE pin-mismatch-public-cli FAIL`,
  r2 `9/9 pass` (the one unstable variant observation noted in §3).
- `callback-authoritative wave accounting` and `required-command-receipt-binding` are invariant over
  all six profiles in all three rounds, matching their `deps none`.

## 5. The `nondeterministic`-class question

Every one of the five rows declares `stable` (exactly one member) and the serial run observed exactly
that one member in all three P0 rounds; no serial observation saw **fewer** members than a declared
class, because no declared class here has more than one member. The question the item asks — did serial
execution see fewer members than the declared class — is therefore vacuous for this group, and it is
answered positively in the weaker sense that matters: serial execution did not see **more** either, so
nothing in this group is concurrency-driven. No observation moved at all: all six profiles returned the
same tuple in all three rounds for all five statements (30 tuples, 0 unstable, `unstable=none` on every
row), so there is no partially-observed member to attribute to either harness or tool.

Historical corroboration: the round-47 deciding receipt (`.ufo/evidence/round-47/after/c1.stdout:13,15,17,19,21`)
printed MATCH / DEPS-OK for the same five statements with the same tuples, so the serial observation
agrees with the round-47 run as well as with the round-48 rows.

## 6. The one-variable pair (QUALITY 96 evidence)

Sibling `T48W2ExecC1ProbeC` ran the same five statements at the counter's default worker count: its
dispatch entry (`.ufo/waves/round-48/a2w1-dispatch.json`, seat `T48W2ExecC1ProbeC`) carries the same
`--lane/--rev/--base/--work/--only` string and **no `--jobs` argument**, i.e. the default `6`
(`measure.py:1001`). Its stdout, `.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeC.stdout`
(sha256 `ca15d6270f0204de255a277798b3cc9d2ab7e99e7b1ec01df3d632381fec62d5`), differs from mine in
**two lines only**, and both are `FLEET` sibling lists:

```
$ diff T48A2ExecC1SerialC.stdout T48W2ExecC1ProbeC.stdout | grep -c '^[<>]'
2
```

Both differing lines are FLEET points 2 and 3/4 recording `souji-shokunin@4e56c48b8fc8` (theirs)
vs `@9da5e9a559f7` (mine, after that lane moved). Every `STATEMENT`, every `PROFILES` tuple, and the
final line — including `sibling_moves=1` — are byte-identical.

So the pair `--jobs 1` vs `--jobs 6`, same revision, same group, same counter bytes, moves **zero
observed values**: 90 serial observations vs the concurrent run agree on all 30 P0/P1 tuples of the
five statements and on all dependence sets. For this group the standing rows' `stable` class is
harness-concurrency-independent; the known concurrency-sensitive statement of round 48
(`six-leg regression ledger`, `.ufo/waves/round-48/w1/T48RevenRegression.md`) is outside this group.

## 7. Findings

**F1 (C1's evidence, low severity). The counter's output does not record the worker count, so a
`--jobs` pair is not auditable from receipts alone.** `measure.py:578-582` prints `self_pin`,
`stmts_pin`, `statements`, `rounds`, `append_only`, …, `base`, `rev` — but no `jobs=`. A reader of
`T48A2ExecC1SerialC.stdout` and `T48W2ExecC1ProbeC.stdout` cannot tell which one ran at 6; the pair
above rests on the dispatch text plus the wave's seat design, not on the two receipts. The pair
therefore demonstrates "concurrency-independent for this group" but cannot be re-derived from the
committed stdout alone. Fix (round 49, not this seat's scope): add `jobs=%d` to the verdict line; it
is a one-token change at `measure.py:578-582` and does not alter any predicate term.

**F2 (tool hygiene, low severity, pre-existing). `effective expectation reconciliation`'s selftest
hard-codes its fixture root to `/tmp` and keeps the tree when a case fails.**
`tools/evidence-disposition.py:2351` `Path(tempfile.mkdtemp(prefix="tameshi-r14-evidence-disposition-selftest.", dir="/tmp"))`
ignores `TMPDIR`; cleanup is on the success path only (`:3122` `shutil.rmtree`), while the failure
path prints `fixtures kept at {scratch}` (`:3115`). Consequence in this probe: the P3 (jj-removed)
profile fails its `v2-jj-*` cases, so each round left one ~6.7 MB tree — three from my run
(`…_6lwo0ym`, `…su38h2fq`, `…utifih7d`, named verbatim in my own `obs-*.stdout` files). Command that
shows it: `ls -d /tmp/tameshi-r14-evidence-disposition-selftest.*` (14 trees at 10:35, 11 after I
removed exactly my three; the rest predate or belong to sibling seats running the same statement
concurrently). Not a C1 contradiction — the row's P0/P1 tuples are exit 0 — but it is a
lane-rule-adjacent residue the deciding run will also produce (3 trees per deciding invocation, since
P3 runs every round) and it contradicts the tool's own docstring promise of "isolated /tmp fixtures"
only in the leaving-behind sense.

**F3 (confirmation, no defect).** `retained invocation-context gate`'s declared dependence is exactly
the decoy path: P5 fails only on the `exit 7` census stub, so `fleet-root` is load-bearing and not a
"deps-everything" claim. `hermetic env-differential probe`'s `2/9` under P2 is the bwrap-absent branch
(`BWRAP_UNAVAILABLE`), consistent with `w1/T48RevenEnvDiff.md` §1.3's note that `2/9` alone does not
discriminate bwrap-absent from shim-masked; here the shim sits under `/fast/scratch`, so it is the real
bwrap-absent branch and P1 stays `9/9|0` in all three rounds (amendment 10's premise holds under a
non-`/tmp` work dir at `--jobs 1` too).

## 8. Scratch, cleanliness, bounds

- Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2ExecC1SerialC` created, used as `TMPDIR` and `--work`
  parent, and deleted at the end; `ls -d` on it now returns "No such file or directory".
- Lane worktree untouched: `git status --porcelain -- corpus tools SCORECARD.md` → 0 lines,
  `git diff --quiet c7586b9a -- corpus tools SCORECARD.md` → clean. No git/jj mutating command run in
  the lane; no fixture repo created.
- Files written: this report and `T48A2ExecC1SerialC.stdout` (both under
  `.ufo/waves/round-48/a2w1/`). Everything else cited lives in the lane read-only.
- Tooling: nothing installed or upgraded (no pacman, uv, npm or binary fetch); only `python3`, `git`,
  `sha256sum`, `diff`, `stat`, `ls`, `df` as shipped.
