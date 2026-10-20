# Fleet kill-rate ledger — the standing verification-health view (TAMESHI T7-2, round 7)

Drafted 2026-10-14 by lane T7-2 (tameshi round 7), state of measurements
measured at this write. Role: **one row per gate — suite size, kill-rate,
survivor classes, hardened-or-not, last-sweep date + pin** — so every
kill-rate claim a fleet record makes can cite one standing receipt instead of
re-quoting the underlying notes. This file adds no new gate measurement: its
own executions are the pins and the harness pulse in §6.

- Scope: the census universe (kumitate's six, kagi's six) plus the measured
  gates beyond it (tsukuroi, mado); the four measured rows are §1, the
  surveyed-but-unmeasured ten are §3, adjacent measured artifacts are §2.
- Sources are pinned in §7; every rated cell is tied to the pin it was swept
  at, and a rate is never implied to hold at a later revision.
- Anchors: **O** observation · **I** inference · **U** unknown. shas are
  sha256, first-16 unless marked full. Substrates read-only during this
  write; scratch `/tmp/w7-tameshi-t72/`; write scope this file only
  (LOG.md / SCORECARD / README updates fold in at lane review, per
  dispatch-write-scope precedent).

## 0. Reading a row

- **Suite (at sweep pin)** — the suite's own executed counter on the swept
  bytes; where the owner later hardened, the live count is given after it
  (`26 → 35`). Counts are executed counters, never static case-site counts.
- **Kill-rate** — single-edit mutants vs the gate's hermetic suite, one rate
  per sweep, **composition-bound**: the rate is only comparable across sweeps
  of similar composition (tsukuroi note E3, `mutation-case-tsukuroi-census.md`
  :296-301; census R.4 `fleet-suite-census.md:596-597`). Composition is stated
  beside every rate.
- **Survivors** — measured, each with a non-equivalence probe in its note
  (the mutant is shown to change behaviour on an input the suite does not
  build). Class vocabulary in §4.
- **Hardened** — what the *owner* did after the sweep (tameshi never patches a
  sibling gate, `PROVINCE.md:16-18`). A post-hardening re-run of the same spec
  is a **directed repair**, not an independent rate; it is recorded as such.
- **Last sweep** — date · target pin · tool/driver. The harness is
  `tameshi-shokunin/tools/mutate-and-run.sh` (rev pins named); rounds 2/3/5
  used the manual round-2-replica drivers.

## 1. Measured — the four fleet sweeps (all 2026-10-14)

| # | Gate (owner · file) | Suite (at sweep) | Kill-rate (composition) | Survivors (measured classes) | Hardened | Last sweep · target pin · driver |
|---|---|---|---|---|---|---|
| 1 | kumitate · `scripts/kimi-census.mjs` (r2) | 43 cases | **8/10 (80 %)** — 10 kill-aimed | D2 findings-cap boundary (reported tail past a prefix assert); D10 `FROZEN.K2` reported constant (unasserted) | **no** — pin unchanged r2 → today; survivors unabsorbed | r2 · `83016d45…` (896 L) · manual driver, scratch `/tmp/tameshi-r2-1-work/` |
| 2 | kagi · `corpus/surface-census.sh` (r3) | 16 cases (14 hermetic + 2 substrate-gated `skip-case`) | **8/10 (80 %)** — 10 kill-aimed | B5 deleted exec x-bit arm (fixture-absent / unreached arm); B10 CLEAN-summary `ok=` field (reported-but-unasserted) | **no** — pin unchanged r3 → today; note left gaps as recommendations only | r3 · `275d8294…` (886 L) · manual driver, scratch `/tmp/tameshi-r3-1-work/` |
| 3 | tsukuroi · `tools/tsukuroi-census.sh` (r5) | 26 cases | **6/10 (60 %)** — 6 kill-aimed (6/6) + 4 hole-aimed (0/4) | B7 default sample cap (cap unreached); B8 usage exit map (out-of-band, CLI parser no case); B9 roll-line fields (unasserted verdict fields); B10 PCI-unreadable branch (unreached arm; probe flips BLOCKED→HEALTHY) | **yes, owner** (lane S5-1): 26 → 35 cases at `aae45531`; replay of the 4 survivors: **B10 killed, B7/B8/B9 still survived** | r5 · `084951be…` (976 newlines) · manual driver, scratch `/tmp/w5-tameshi-1-work/` |
| 4 | mado · `tools/mado-verify.sh` (r6) | 28 assertions (scenarios A–D) | **4/10 (40 %)** — 4 in-surface (4/4) + 6 out-of-surface (0/6); assertion set and kill set co-extensive on this spec | D3 SKIP→PASS row unread; D5 failing-selftest exit 2→1 unobservable; D7 include-count tolerance never reached; D8 sha-pin NOTE claims untested match; D9 boundary safety row asserted only in its PASS direction (new class); R1 tomllib arm unreachable in-suite | **yes, owner** (lane M6-1): +88/−0 inside `selftest()`, 28 → 53 assertions at `c4c1afb7`; **same spec re-run: 10/10 (100 %)** — directed repair. Residuals unabsorbed: rc-6 dead arm, exit-flatten family, 51 live-plane row sites, 2 out-of-band usage exits | r6 · `d7edaab4…` (1,098 L) · harness `597e1419…` (R1); whole spec re-cut under `b56c6e57…` with identical verdicts + mutant shas (scribe) |

Cell detail, with sources:

1. **kimi-census** — pin `83016d45049b009a` (896 L / 43,273 B), kumitate HEAD
   `175de6b`, path porcelain-clean; live today = the same sha (O). Control
   `KIMI_CENSUS_SELFTEST: 43/43 pass`. D2: `findings.slice(0, 6)` → `5`,
   boundary unreached (max findings in any suite run = 2; the DRIFT assert is
   prefix-based `:498`); D10: `FROZEN.K2 25` → `24`, only `frozen.K5` asserted
   (`:526`); both probed non-equivalent on an empty root. Headline
   `mutation-case-kimi-census.md:29`; VER-T1 errata E2 `:207-237` (D2 is
   assert-caused, not unreachability-caused).
2. **surface-census** — pin `275d8294a94e9eb7` (886 L / 44,212 B); live today
   = the same sha (O). B5 probe: consider `asset exec` at mode 644 — pristine
   `SURFACE DIVERGED … no execute bit` exit 1 vs B5 `SURFACE OK … (exec 644)`
   exit 0. B10 probe: green fixture summary pristine `ok=1` vs B10 `ok=0`,
   both exit 0. Headline `mutation-case-kagi-census.md:50`.
3. **tsukuroi-census** — sweep pin `084951be…c78c5` (976 newlines; HEAD
   `165307fe`); incident I1: the substrate moved mid-run **by the owner's own
   concurrent lane** — before ≠ after is that writer, and every §1/§2 cell is
   on the frozen copy (`mutation-case-tsukuroi-census.md:9-36`). Composition:
   B1–B6 aimed at defects the asserts should catch (all killed), B7–B10 at
   predicted survivor families (all survived). The owner's hardening comment
   in-gate (`tsukuroi-census.sh:915-920`) quotes its own 23-defect first pass
   `13 killed / 10 survived`; the replay (`mutation-case-tsukuroi-census.md`
   §6) leaves B7's default site, B8 and B9 open at `aae45531`. Live today
   `aae45531` (1,032 newlines) = committed HEAD blob; tsukuroi HEAD
   `dc3436d`, tree clean (O).
4. **mado-verify** — sweep pin `d7edaab4…d0e13` (1,098 L / 45,334 B); suite
   `bash "$MUTANT" --selftest`; sweep at 17:42:16Z. Six survivor probes (P3,
   P5, P7, P8, P9, PR1) each a measured behaviour difference
   (`mutation-case-mado-verify.md:105-147`). D9 is the new arm-class shape
   (safety row asserted only in its PASS direction). Owner hardening
   `mado-shokunin/corpus/knowledge/gate-mutation-proof.md` @ `716836ca…`
   (167 L): 10/10 re-run, residuals §3 there; live today `c4c1afb7` (1,186 L)
   = committed HEAD blob; mado HEAD `c8f6667`, tree clean (O).

Embedding status (O, §5): the harness's `--regression` currently embeds
**cases 1 and 2 only** (`PIN_JS`/`PIN_BASH`, `tools/mutate-and-run.sh:482-483`);
cases 3 and 4 are not embedded at this write, so their tables carry no
`REGRESSION` line over themselves yet.

## 2. Adjacent measured — not fleet sweeps; carried so the view is not over-read

| Artifact | Measurement | Reading | Source |
|---|---|---|---|
| kumitate `scripts/cite-check.mjs` (pin `40573448…`, 2,537 L) | PREP-T6 **probe**: 4 defects — **1 killed** (K3: report path drops the drift gate; suite 61/62), 3 survivors (K1 aggregate CLI verdict collapse, K2 summary counts always n/n, K4 CLI exit fail-open); `MUTATE_RESTORE: OK`, kumitate tree clean | a probe, **not a sweep**: no composition, no full table; the queue's head is now "probed only" | scratch `/tmp/w5-prept6-cite/work/results.tsv` (retained); census R.4 `fleet-suite-census.md:607-615` |
| tameshi `tools/mutate-and-run.sh` `--regression` comparator | meta-sweep r6: pre-hardening R1 **0/6 killed** (predicted, 6/6 survived), post-hardening R2 **6/6 killed (100 %)** on new selftest labels rg5–rg9; selftest 37/37 → 55/55 | the instrument's own gate, hardened by its owner (tameshi); the two rates bound its comparator, not a fleet gate | `self-hardening-r6.md` @ `f2c347ac…`, §1–§3 |
| kagi `corpus/scope-gate.sh` (pin `078a2601…`, 1,129 L) | self-attack `--falsify`: **16/18 caught** on this host, exit 1 — two `SCOPE BREADTH-EXCEEDS` token misses; README's unqualified "18/18" contradicted | the gate's own mutation mode, not a tameshi sweep; not comparable as a kill-rate | `gates-survey-kagi.md` §6 (F-1) §6/§8 |

## 3. Surveyed, unmeasured — the standing offer's queue

Kumitate's five unmeasured (order per census §5 / R.4, unchanged;
`fleet-suite-census.md:277-291`, `:594-615`). Suite counts are executed pulse
counters (`--selftest`) on these pins; pins re-measured today, kumitate HEAD
`175de6b`, tree clean (O).

| Gate | Suite (cases) | Pin (first-16) | State / sweep prerequisite |
|---|---|---|---|
| cite-check | 62 | `40573448330f52fb` | **probe only, 1/4** (§2); full sweep open — hermetic 62-case run on a copy; the integration group stays a declared skip |
| surface-probe | 42 | `148cbf85ce4c7682` | unmeasured; hermetic |
| round-gate | 60 | `f890e277af83a78f` | unmeasured; hermetic |
| proxy-check | 102 | `a052ddb97a0b6f84` | unmeasured; hermetic; expect low survivor count |
| claims-check | 39 | `e9a21b441f1216bf` | unmeasured; hermetic; expect low survivor count |

Kagi's five unmeasured (kagi's six-gate family; pins re-measured today, HEAD
`fecee87`, tree clean; O). Suites per `gates-survey-kagi.md:24-31` and the
G-R2-1 corrected claim-ledger pin `:554-566`.

| Gate | Suite (cases) | Pin (first-16) | State / sweep prerequisite |
|---|---|---|---|
| drift-pins | 13 | `c138d34c7f0dfe95` | unmeasured by sweep; hermetic |
| op-ref-probe | 29 | `509f084ad33229db` | unmeasured by sweep; hermetic |
| checklist-run | 34 | `7e5ec98b9e1d0afa` | unmeasured by sweep; hermetic |
| scope-gate | 61 (+`--falsify` 18) | `078a260184e25282` | unmeasured by sweep; self-attack 16/18 (§2); F-1 open |
| claim-ledger | 97 | `93c5827202b9cdec` | unmeasured by sweep; F-2: 3 of 6 refusal paths have no case |

**Boundary — sightings and adjacent machinery, not queued (census §6
`:617-626`):** kake `scripts/{freshness-sweep,probe-delta}.mjs`, kama
`tools/{kama-probe,test-snapshot}.sh`, kotoba `verifiers/*` — file existence
is O, their gate-ness is U until a survey admits them; tabi `tools/` absent;
the game lanes' verifier machinery and kaidoku's audit lanes are adjacent
patterns with no survivor tally (`verification-patterns-fleet.md`).

## 4. Fleet-wide readings carried by this ledger

- **Rate sequence (measured, one row per sweep):** 80 % (kimi r2) · 80 %
  (kagi r3) · 60 % (tsukuroi r5) · 40 % (mado r6). Directed-repair follow-ups:
  100 % (mado hardened, same spec) and the harness meta 0/6 → 6/6. Bands stay
  as amended; no floor claimed (`fleet-suite-census.md:594-606`).
- **Composition binds a rate.** mado's 40 % is the first sub-50 point and is
  composition, not suite regression: 4 in-surface defects all killed, 6
  out-of-surface none — "the suite's assertion set and its kill set are
  co-extensive on this spec" (`mutation-case-mado-verify.md:66-72`). Never
  average or compare rates without composition (tsukuroi E3).
- **Survivor-class vocabulary (measured instances):**
  **(a) reported-but-unasserted surface** — kimi D2/D10, kagi B10, tsukuroi
  B9, mado D3/D8; **(b) unreached fixture/arm** — kagi B5, tsukuroi B7/B10,
  mado D7/R1; **(c) one-directional assert** — mado D9 (new shape);
  **(d) out-of-band exit map** — tsukuroi B8, mado D5. Repair shapes differ:
  (a)/(c) assert the value, (b) adds one case per arm, and a cap stays open
  when the new case env-overrides the default the mutant edits (tsukuroi B7 at
  the hardened revision, `mutation-case-tsukuroi-census.md:307-321`).
- **Two hardening precedents, two outcomes.** Owner-side hardening closed 1 of
  4 tsukuroi survivors (replay-measured) and all 6 mado survivors (same spec,
  directed); both residual lists stay open and owner-owned.
- **Not claimed (the ledger's boundary):** cross-host / toolchain stability of
  any rate (single host, 2026-10-14); coordinated multi-edit rewrites
  (matrix §7, unmeasured everywhere); suite sensitivity ≠ gate truth (nothing
  here measures whether a gate's verdicts about the real world are right);
  live-substrate drift (suites are hermetic by construction).

## 5. The instrument and its regression gate (re-measured by this lane)

- `tools/mutate-and-run.sh` @ `b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb`
  (1,080 L): `--selftest` → `MUTATE_SELFTEST: 55/55 pass` / `VERDICT: PASS`,
  rc 0; `--regression` → `REGRESSION: PASS (cases=2 passed=2; band
  killed-delta<=1 flips<=1)`, rc 0 — both run today by this lane (23.4 s
  total; log `/tmp/w7-tameshi-t72/regression`, `MUTATE_TOOL` line carries the
  sha above). Embedded cases: `js-kimi-census` (pin `83016d45…`) and
  `bash-surface-census` (pin `275d8294…`), each `match=10/10`, `flips=0`,
  80 % (`tools/mutate-and-run.sh:482-483`, `:739-744`).
- **Not yet embedded at this write: the tsukuroi and mado cases** — the round-7
  plan's leg 1 carries the embedding (`plans/round-7.plan.md:4-10`); when it
  lands, this ledger's embedding line and case count change as an appended
  row, not an edit of §1–§4.
- The service contract a lane opts into (pinned revision + one-command
  hermetic suite exercising the copy + clause-mapped spec) is
  `SKILL.md:794-918` (`SKILL.md` @ `137879dd…`, 918 L).

## 6. Spot-checks (run 2026-10-14 for this write; scratch `/tmp/w7-tameshi-t72/`)

- **S1 — live pins vs recorded pins (O).** `sha256sum` on all targets:
  kimi-census `83016d45…`, surface-census `275d8294…` (both = their sweep
  pins); tsukuroi live `aae45531…` (= the hardened replay revision; committed
  HEAD blob, `git show HEAD:tools/tsukuroi-census.sh`), mado live
  `c4c1afb7…` (= hardened; `git show HEAD:tools/mado-verify.sh`); the ten
  unmeasured pins identical to §3; kumitate HEAD `175de6b` + clean, kagi HEAD
  `fecee87` + clean, tsukuroi `dc3436d` + clean, mado `c8f6667` + clean.
- **S2 — headline cells re-read on the source bytes (O).**
  `sed -n` on the four notes: kimi `:29` contains "kill rate 8/10 (80 %);
  survivors D2, D10"; kagi `:50` "8/10 (80 %); survivors B5, B10"; tsukuroi
  `:68` "6/10 (60 %); survivors B7, B8, B9, B10"; mado `:60` "4/10 (40 %),
  survivors D3, D5, D7, D8, D9, R1"; census R.4 `:596-602` carries the same
  four rates + the mado hardened 10/10; `mutation-case-mado-verify.md` `:211`
  embeds-status: "the 4-case embed did not happen in either".
- **S3 — harness pulse (O).** `bash tools/mutate-and-run.sh --selftest` →
  55/55 PASS, rc 0; `bash tools/mutate-and-run.sh --regression --workdir
  /tmp/w7-tameshi-t72/regression` → `REGRESSION: PASS (cases=2 passed=2)`,
  both case tables `match=10/10 recorded-killed=8 measured-killed=8
  survived=2 flips=0`, rc 0.

## 7. Sources (pinned at this write; sha256 first-16 / `wc -l`)

| File | sha256 (16) | lines | Use here |
|---|---|---|---|
| `corpus/knowledge/mutation-case-kimi-census.md` | `034524eff8f19cb8` | 237 | r2 case (§1.1) |
| `corpus/knowledge/mutation-case-kagi-census.md` | `0d5dc3cd7d2d21a3` | 258 | r3 case (§1.2) |
| `corpus/knowledge/mutation-case-tsukuroi-census.md` | `b431bc6ce2b53e4e` | 396 | r5 case + replay (§1.3) |
| `corpus/knowledge/mutation-case-mado-verify.md` | `f2d53d495e6c1d8b` | 323 | r6 case (§1.4) |
| `corpus/knowledge/fleet-suite-census.md` | `ec1c2d8d2877a21d` | 674 | census + service receipt (§1–§3) |
| `corpus/knowledge/self-hardening-r6.md` | `f2c347acd323b077` | 261 | harness meta-sweep (§2, §5) |
| `corpus/knowledge/gates-survey-kagi.md` | per §1 + G-R2-1 | 620 | kagi counts/pins (§3) |
| mado `corpus/knowledge/gate-mutation-proof.md` | `716836ca1bf3484a` | 167 | mado hardening (§1.4) |
| `/tmp/w5-prept6-cite/work/results.tsv` | (scratch) | 4 rows | cite-check probe (§2) |
| `tools/mutate-and-run.sh` | `b56c6e57f1b7ae91` | 1,080 | instrument (§5) |
| `SKILL.md` | `137879dd174383ca` | 918 | service contract (§5) |

## 8. Unknowns

- **U1** — no cross-host/toolchain stability reading for any rate (single
  host, bash 5.3.15 / node v24.21.0 / python 3.14.7, 2026-10-14).
- **U2** — coordinated multi-edit rewrites unmeasured everywhere (matrix §7).
- **U3** — the tsukuroi and mado tables are not re-verified by the harness's
  own `--regression` (cases=2 at this write); their reproduction under future
  tool revisions is unmeasured.
- **U4** — the ten surveyed gates' kill profiles are unknown; the cite-check
  probe (1/4) is an indication, not a rate.
- **U5** — live-substrate sensitivity unmeasured for every gate; hermetic
  suites never read the live tree by construction.
- **U6** — suite sensitivity ≠ gate truth: nothing here measures whether a
  gate's verdicts about the real world are correct.
- **U7** — the mado and tsukuroi hardened revisions were measured only against
  the specs they were hardened against (directed repair); independent defect
  sets against them are unmeasured.
- **U8** — sightings (kake, kama, kotoba) have unresolved gate-ness; their
  admission state is U until a survey admits them.
- **U9** — this ledger's update cadence is a convention, not a mechanism: a
  new sweep appends a row (or an errata block); who runs the update is the
  dispatcher's call, not fixed here.

## Errata (append-only)

(none yet — new entries go below this line, never edits above per
`corpus/QUALITY.md` item 4)

**ER-1 — post-write concurrent drift, observed and recorded (O; appended
2026-10-14 by T7-2, minutes after §6).** Between §5–§6's measurements and this
append, two files this ledger cites moved under concurrent (sanctioned)
round-7 lanes — recorded, not smoothed (round-6 precedent: harness drift
mid-round, `fleet-suite-census.md:571-588`).

1. `tameshi-shokunin/tools/mutate-and-run.sh` — §5's pulse ran at
   `b56c6e57…` (the run's own `MUTATE_TOOL` line carries that pin); at this
   append the working tree holds `13d2fbfc63ea02ec…`, 1,114 L,
   `git diff --numstat` +71/−37, mtime 15:26:45 — the round-7 embedding lane's
   edit in flight. Static read of that revision: `PIN_TSUKUROI=084951be…` and
   `PIN_MADO=d7edaab4…` exist (`:511`, `:513`), while the regression summary
   printfs still read `cases=2` (`:790`, `:796`, `:800`). **The new revision's
   case set and `--regression` behaviour are U here** — §5's "cases=2 at this
   write" is the state measured at the pulse; re-measure before quoting
   either.
2. `tsukuroi-shokunin/tools/tsukuroi-census.sh` — §1.3/§6 recorded the live
   file as `aae45531…`, committed HEAD blob, tree clean; at this append the
   working tree holds `d666bba305240d8c…` (1,186 L; `git diff --numstat`
   +162/−8 vs `dc3436d`; mtime 15:24:40) — a concurrent writer, unpinned by
   this ledger. The reference revisions stand (`084951be…` sweep, `aae45531…`
   replay); a future sweep must re-pin.

mado `tools/mado-verify.sh` re-measured unchanged at `c4c1afb7…` (O). No rate
in §1–§4 is re-cut by this entry; the moved cells are read-only observations,
and a reader needing current live identities should re-run §6 S1's
`sha256sum` set. New errata entries go below this one.

**ER-2 — the fifth and sixth cases land: kagi `corpus/checklist-run.sh` and kumitate `scripts/claims-check.mjs` — six gates measured (O; appended 2026-10-14 by T8-3, tameshi round 8).** Two independent sweeps ran this round — service form, targets read-only, predictions pre-registered before each run, one scratch per lane (`/tmp/w8-tameshi-t81/`, `/tmp/w8-t8-2-claims/`); each note is its run's only fleet file. §1's table is not edited; these rows are the append U9's own rule prescribes (`:235-237`; the update rule `:170-172`). Columns per §0.

| # | Gate (owner · file) | Suite (at sweep) | Kill-rate (composition) | Survivors (measured classes) | Hardened | Last sweep · target pin · driver |
|---|---|---|---|---|---|---|
| 5 | kagi · `corpus/checklist-run.sh` | 34 cases | **7/15 (47 %)** — 7 kill-aimed (7/7) + 8 hole-aimed (0/8) | A1, B1, B3, C1, D1, E2, F2, G1 — (a) 2: C1, F2 · (b) 6: A1, B1, B3, D1, E2, G1; new mechanisms: CLI fail-open (G1), output-capture loss (E2), deny-list re-openable (B3) | **no** — recommendations only; owner = kagi | r8 · `7e5ec98b9e1d0afa` (506 L / 24 697 B = kagi HEAD `fecee87` blob) · harness copy `cf41efaa…` (r7-1) via `/tmp`, live path unchanged |
| 6 | kumitate · `scripts/claims-check.mjs` | 39 checks | **7/10 (70 %)** — 6 kill-aimed (6/6) + 4 hole-aimed (1/4) | D7 (cap `slice(0, 6)`→`5` — the kimi D2 site, independently re-measured), D8 (assert-blind threshold — new sub-shape; probe P8 flips the verdict), D9 (unreached arm — first JS instance) | **no** — recommendations stay owner-side | r8 · `e9a21b441f1216bf` (925 newlines / 48 265 B = kumitate HEAD `175de6b` blob) · harness `cf41efaa…` (r7-1) |

- **Rate sequence, appended to §4's** (`:134-137`): 80 % (kimi r2) · 80 % (kagi r3) · 60 % (tsukuroi r5) · 40 % (mado r6) · **47 % (kagi checklist r8)** · **70 % (kumitate claims r8)**. Composition binds each rate, as §0 states: the co-extensive shape has a third measured instance (row 5, 7/7+0/8, after mado 4/4+0/6 and tsukuroi 6/6+0/4), and row 6's 6/6+1/4 is the first pre-registered hole-aimed mutant measured killed (D10; the prediction was wrong in the safe direction — T8-2 E1). No cross-gate comparison is made or implied.
- **§3 supersession (cells, not edits).** The §3 queue rows `claims-check` (`:111`) and `checklist-run` (`:121`) said "unmeasured by sweep"; rows 5/6 are the measurements that supersede those cells — §3's tables stay as written. Eight queue rows stand: kumitate's cite-check, surface-probe, round-gate, proxy-check; kagi's drift-pins, op-ref-probe, scope-gate, claim-ledger.
- **§5 / ER-1 supersession (embedding + tool).** §5's "cases=2 at this write" and ER-1 item 1's in-flight revision are superseded: the harness at `cf41efaa8be5f52d…` (r7-1; 1 341 L / 61 632 B) carries **four** materialized legs and passes them at the exact band — `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, every leg `match=10/10 flips=0` (O: T8-2's run 2026-10-14T19:14:16Z, `mutation-case-kumitate-claims.md` §6; corroborated `reports/r7-aud-t7.md` §1). U3 (`:221-223`) narrows: the tsukuroi and mado tables now ARE re-verified by the harness's own `--regression` — at their recorded pins, under `cf41efaa…`; the candidates' live revisions are not what the legs replay (pin read in ER-3).
- **Named follow-ups (not edits, not written here).** Cases 5/6 are not embedded in `--regression`: T8-2 E3 records the target pin / suite / spec for the tool's owner, and T8-1 U5 leaves the leg-cut decision to the same owner — rows 5/6 therefore carry no `REGRESSION` line over themselves. The r3 census's "hermetic fallback" wording is superseded by case 5 (T8-1 U7), and census §5's instrument pin (`597e1419…`, `:251-262`) sits two revisions behind the live tool — a re-pin errata item for the census owner.
- **Sources pinned at this append (re-measured immediately before the write):** `corpus/knowledge/mutation-case-kagi-checklist.md` @ `43da70e6…` (367 `wc -l`; unterminated final line / 22 952 B); `corpus/knowledge/mutation-case-kumitate-claims.md` @ `3da1312e…` (409 `wc -l`; unterminated final line / 29 236 B). Cells above are the notes' own §2/§6 hand-off rows; case 5's note self-identifies as the third service engagement (`PROVINCE.md:14-18` absorption rule).

**ER-3 — the re-sweep cadence: when an owner requests one, and what comes back (policy + executed pin read; appended 2026-10-14 by T8-3).** U9 (`:235-237`) recorded this ledger's update as "a convention, not a mechanism". The mechanism is three triggers, stated from the owner's side, plus one mechanical pin read that says which trigger fired. It governs the six measured rows above; a first sweep of an unmeasured §3 gate is not a re-sweep.

*The pin read (one command set per case, run at the boundary — the executed instance follows):*

    sha256sum <gate-file>                                # vs the case row's recorded pin
    git -C <owner-repo> show HEAD:<path> | sha256sum     # is the recorded revision the HEAD blob?
    git -C <owner-repo> status --porcelain -- <path>     # working tree vs HEAD

*Readings.* **current** — recorded pin = live file = HEAD blob, tree clean (the row's pin still names the object; a re-sweep is a fresh reading, not a repair). **stale** — the recorded revision is an ancestor of the live gate; the substrate moved after the sweep (trigger 3). **drift** — the working tree differs from its HEAD (a writer is on the gate; wait for the commit, then re-pin). The read is hygiene and a trigger reading, not a replay guard: the harness's legs materialize from git blobs (`git show <rev>:<path>`), so a drifted tree cannot move a materialized leg (`reports/r7-aud-t7.md` §2–§3).

Executed at this append, 2026-10-14T19:21:00Z (all six rows; rows 3/4 show the trigger live — both substrates moved mid-round):

| # | case | recorded pin | live | HEAD blob | worktree | reading |
|---|---|---|---|---|---|---|
| 1 | kimi-census | `83016d45…` | `83016d45…` | `83016d45…` | clean | current |
| 2 | surface-census | `275d8294…` | `275d8294…` | `275d8294…` | clean | current |
| 3 | tsukuroi-census | `084951be…` | `bba6cdf6…` (1 472 L) | `bba6cdf6…` | clean | **stale** |
| 4 | mado-verify | `d7edaab4…` | `dc864c6a…` (2 186 L) | `90d50cdd…` | dirty | **stale + drift** |
| 5 | checklist-run | `7e5ec98b…` | `7e5ec98b…` | `7e5ec98b…` | clean | current |
| 6 | claims-check | `e9a21b44…` | `e9a21b44…` | `e9a21b44…` | clean | current |

*Triggers — an owner should request a re-sweep when any one holds:*

1. **After hardening.** Any owner edit that absorbs a survivor (or otherwise changes the gate) supersedes the swept revision: the recorded table is a measurement at the old pin, and the owner's own spec re-run closes *that spec* (directed repair, §0) — an independent re-sweep (fresh or extended spec) is the new independent reading. Precedents: tsukuroi 26 → 35 cases, B10 closed / B7–B9 open (§1.3); mado 28 → 53 assertions, same spec 10/10 (§1.4).
2. **After suite changes.** Any change to the suite's executed case set moves the composition the rate is bound to (§0; tsukuroi E3) — the old rate's comparability lapses even where the gate's behaviour is unchanged. Recorded instance: mado 28 → 53.
3. **On substrate drift.** The pin read above reads stale or drift. A moved substrate needs a **re-pin**, never a re-interpretation of the old table — the request shape already carries this (`service-optin-protocol.md:59-62`); both revisions stay in the record.

*What a re-sweep is, and what comes back.* The service protocol's request shape (`service-optin-protocol.md:54-107`): pinned revision · hermetic one-command suite invocable on a copy · clause-mapped single-edit spec with pre-registered expectations. The run is read-only to the substrate, the note is the only fleet file written, and the outcome lands **as an appended row or errata block in this ledger** — never as an edit of §1–§4. A re-sweep measures the live revision; the old row stands as its revision's record; a rate never travels (per-revision, per-host; §0); `moved=0` is recorded, never manufactured.

*What the cadence is not.* No daemon and no timer: the ledger stays the standing view + this policy + the pin read as an executed command at a round boundary; who runs it remains the dispatcher's call ([O] no round created a background process; [U] whether a fleet driver would invoke it unaided). Divergence between a cadence re-sweep and an owner's own receipt is the FINDING (per-revision, per-host scope) — never smoothed.

New errata entries go below this one.

**ER-4 — the cadence fires its first scheduled tick: regression re-run exact · six-case pin read · two drift events recorded (O; appended 2026-10-14 by T9-1, tameshi round 9; `plans/round-9.plan.md` leg 1).** ER-3 landed the cadence as policy + one executed read; this is the policy's first invocation at a round boundary — the receipt. No §1–§4 cell is edited; the moved cells are append-only readings, old tables stand at their revisions, and a moved pin is never re-interpreted.

*Tick — exact command set and scratch.* Per case, ER-3's command set verbatim (`sha256sum <gate-file>`; `git -C <repo> show HEAD:<path> | sha256sum`; `git -C <repo> status --porcelain -- <path>`) plus the ancestor check `git -C <repo> merge-base --is-ancestor <rev> HEAD`; then the harness itself: `bash tools/mutate-and-run.sh --selftest` and `bash tools/mutate-and-run.sh --regression --workdir /tmp/w9-tameshi-t91/regression`. Scratch `/tmp/w9-tameshi-t91/` (`tick.log` = both harness runs; `pin-read.log` = the raw six-case read, second pass 20:00:29Z). Tool at the tick `cf41efaa8be5f52d…` (1 341 L / 61 632 B, r7-1): **held** vs ER-2's pin (`:281`).

*Pin read (executed at the tick, 19:58Z; second raw pass 20:00:29Z, same readings):*

| # | case | recorded pin @ recorded rev | live | live = HEAD blob | worktree · recorded rev ancestor | reading |
|---|---|---|---|---|---|---|
| 1 | kimi-census | `83016d45…` @ `175de6ba` | `83016d45…` | yes | clean · yes | current |
| 2 | surface-census | `275d8294…` @ `fecee874` | `275d8294…` | yes | clean · yes | current |
| 3 | tsukuroi-census | `084951be…` @ `165307fe` | `bba6cdf6…` (1 472 L / 73 919 B) | yes | clean · yes | **stale** |
| 4 | mado-verify | `d7edaab4…` @ `eead56b2` | `7da4ec50…` (2 887 L / 131 612 B) | yes | clean · yes | **stale** |
| 5 | checklist-run | `7e5ec98b…` @ `fecee874` | `7e5ec98b…` | yes | clean · yes | current |
| 6 | claims-check | `e9a21b44…` @ `175de6ba` | `e9a21b44…` | yes | clean · yes | current |

Headline as measured: `LEDGER: 6 cases in; target current=4 stale=2 drift=0; tool held (cf41efaa…)`. Rows 3/4 are the two ER-3 already read `stale` (row 4 additionally `drift`); mado's `drift` reading is closed — the worktree is clean at this read and the edit is now a commit (below). Rows 1/2/5/6 read `current`, unchanged since ER-3.

*Drift events recorded (trigger 3 · date · old → new · cause where readable).* Both repos' round-8 commits are stamped 2026-10-14T19:55:09Z — after ER-3's read, before this tick. Mado's commit carried the gate edit; tsukuroi's is the scribe's land (its gate path was last moved by round 7).

- **row 3, tsukuroi `tools/tsukuroi-census.sh`** — `084951be…` @ `165307fe` (round 4) → **`bba6cdf6…`** @ HEAD `72b038d` (round-8 commit). Readable blob chain: `084951be` (`165307fe`) → `aae45531` (`da95290`, round 5, 17:33:30Z — the owner hardening §1.3 already records as its replay revision) → `bba6cdf6` (`aa136d6`, round 7, 19:06:31Z). Commit messages are round-generic; the writers are the owner's own lanes.
- **row 4, mado `tools/mado-verify.sh`** — `d7edaab4…` @ `eead56b2` (round 5) → **`7da4ec50…`** @ HEAD `12c8f08` (round-8 commit). Chain: `d7edaab4` (`eead56b2`) → `c4c1afb7` (`c8f6667`, round 6, 18:17:26Z — the hardening §1.4 records) → `90d50cdd` (`0c20a76`, round 7, 19:06:31Z) → `7da4ec50` (`12c8f08`). The working-tree transients already on record — `6ea07110…` (round-9 plan [O]) and `dc864c6a…` (ER-3) — resolved into the committed `7da4ec50`; `drift` is superseded by `stale`, not left open.
- [U] what each moved revision's mechanisms do — whether the recorded verdict/survivor classes reproduce at `bba6cdf6…` / `7da4ec50…` — is unmeasured here; that is this round's re-sweep work (its own appended rows), not this receipt.

*Regression re-run — the instrument's own gate (receipt; workdirs `/tmp/w9-tameshi-t91/regression/` kept).* `MUTATE_SELFTEST: 67/67 pass` · `VERDICT: PASS`, rc 0. `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0, `REGRESSION_DATE: 2026-10-14T19:58:18Z`; every leg git-materialized at its recorded rev, `MUTATE_RESTORE: OK` per leg (target-sha256 before = after = the pinned bytes):

| leg | materialized rev | pin sha256 | sweep | table line | case |
|---|---|---|---|---|---|
| js-kimi-census | `175de6ba…` | `83016d45…` | 8/10 (80 %) | `match=10/10 … flips=0` | PASS |
| bash-surface-census | `fecee874…` | `275d8294…` | 8/10 (80 %) | `match=10/10 … flips=0` | PASS |
| bash-tsukuroi-census | `165307fe…` | `084951be…` | 6/10 (60 %) | `match=10/10 … flips=0` | PASS |
| bash-mado-verify | `eead56b2…` | `d7edaab4…` | 4/10 (40 %) | `match=10/10 … flips=0` | PASS |

Two measured caveats, stated not smoothed: (a) the tool embeds **4** legs — cases 5/6 (checklist-run, claims-check) carry no `REGRESSION` line at `cf41efaa…`; the leg-cut decision stands with the tool owner (ER-2's named hand-offs, `:282`), nothing re-cut to manufacture a line; (b) the legs replay recorded pins while live gates 3/4 read `stale` — a git-materialized leg cannot be moved by a drifted tree (the tool's own selftest arms: "drifted working tree does not move a git-pinned leg"; "drifted leg swept the pinned blob bytes, not the tree"), so this PASS is a statement about the recorded revisions, not the live files.

*What this tick closes, and what it does not.* U9 gets its first executed firing: the tick ran at a round boundary, the six-cell read and both drift events are appended, and the engine re-passed at the revision ER-2 pinned. It closes nothing else: the re-sweeps of the two `stale` cases land as their own rows, no rate is re-cut, `stale=2` is the reading — a tick that read `stale=0` would be as complete. Sibling trees read-only, clean before and after (kumitate `175de6b` · kagi `fecee87` · tsukuroi `72b038d` · mado `12c8f08`). A divergence between this tick and any owner's receipt is the FINDING, never smoothed.

New errata entries go below this one.

**ER-4 addendum — post-tick continuation: both moved gates read worktree-dirty again, minutes after the tick (O; appended 2026-10-14 by T9-1; ER-1's post-write-drift precedence).** The tick read the two moved cells clean/`stale`; at the read below both owners' gates carry uncommitted edits again. No ER-4 cell is re-cut — both readings are true at their timestamps, and the working revisions are moving: re-read before quoting. [I] the writers are the owners' own round-9 lanes — their `plans/round-9-record-draft.md` files and tsukuroi's `corpus/knowledge/aur-drift-receipt-r9.md` land in the same minutes, and tameshi lanes never write sibling gates (`PROVINCE.md`).

- **tsukuroi `tools/tsukuroi-census.sh`** — worktree `5d16378d…` (1 535 L / 79 432 B, mtime 20:02:42Z), `git diff --numstat` +63/−0 vs HEAD blob `bba6cdf6…` → reading **stale + drift** (ER-4 row 3 read `stale`, clean).
- **mado `tools/mado-verify.sh`** — worktree `5b6ace8e…` (3 076 L / 141 461 B, mtime 20:02:38Z), +196/−7 vs HEAD blob `7da4ec50…` → reading **stale + drift** (ER-4 row 4 read `stale`, clean).
- Tool re-read at 20:02Z: `cf41efaa8be5f52d…`, mtime 15:29:01 −03:00 — still **held**; ER-4's regression receipt stands as the tick's record.

Consequence for the cadence: trigger T3 is live again on both legs; any re-sweep must pin the revision it measures (the moved substrate's re-pin rule, ER-3) and never re-interpret a moving file. `drift` here is a reading, not a defect — the owners are editing their own gates.

New errata entries go below this one.

## ER-5 — round-13 structured content disposition (2026-10-20)

Executed:
`python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`
→ exit 0; `pin-dispositions.json` records 6 legs, unchanged3/changed3/
unavailable0, with `result_reuse=not_established` on every row.
Full command/stdout and input digests:
`.ufo/evidence/round-13/verification.json`, `expected.json`;
source method: S003 and S048,
`incremental-pin-disposition.md`.

`observed_at=2026-10-20T04:59:26Z` marks the end of a sequential read
window, not an atomic fleet snapshot or each row's instant. Every row
records the HEAD actually read and both HEAD/worktree SHA256 values.

| Leg | Observed owner HEAD | HEAD = worktree SHA256, abbreviated | Content vs original recorded pin |
|---|---|---|---|
| js-kimi-census | `1770305fae20826b39905a8251ddeca6b4957ac4` | `5e8d591324064fff` | changed |
| bash-surface-census | `c2cab35bc92e57e39e5489bac3386db078345b3f` | `275d8294a94e9eb7` | unchanged |
| bash-tsukuroi-census | `9574a189a758251da5957eee8ff0f38ba2d03c7f` | `d17d32a35946c71c` | changed |
| bash-mado-verify | `59cfbdc3ab5e7b6aaf68f86e1b2ae8d51c938b1e` | `037b05dcd3f86e12` | changed |
| bash-checklist-run | `c2cab35bc92e57e39e5489bac3386db078345b3f` | `7e5ec98b9e1d0afa` | unchanged |
| js-claims-check | `1770305fae20826b39905a8251ddeca6b4957ac4` | `e9a21b441f1216bf` | unchanged |

All six original blobs verified against the configured manifest pins.
This is byte-content status only: mode, environment, dependencies,
runner/spec context and invocation are explicitly not compared. The
manifest is a committed configured baseline, not a cryptographically
authenticated external authority. Changing it changes the baseline.

This corrects the **current use**, not the dated truth, of the old
four-current/two-stale reading. Kimi's target has also changed; its
successor sweep joins the existing tsukuroi/mado successor debt.
The probe does not evaluate ancestry, so `changed` is not relabelled
`stale` by inference here. It runs no sibling suite, closes no mutation
re-sweep and produces no new kill-rate or recorded case.

## Round 16 — seventh row appended (2026-10-20)

Appended; nothing above is edited. The row for kumitate `round-gate.mjs` in
the §5 queue said `unmeasured`. It is measured now:

| gate | suite | rate (composition) | survivors | sweep | pin |
|---|---|---|---|---|---|
| kumitate `scripts/round-gate.mjs` (leg `js-round-gate`) | `--selftest`, 60 checks, under the `env -i` guard | **5/10 (50 %)**; 5 kill-aimed / 5 hole-aimed, 10/10 predictions held | C1059 floor edge, A2 fail-closed detail tail, B2 tracked species, CKIND enum shrink (equivalent for gate behaviour), E1 `UFO_SRC` set-value | 2026-10-20T13:40:15Z, runner `75ed934d…` | rev `364f1d5`, sha256 `f890e277…d3e9` |

Detail of record: `mutation-case-kumitate-round-gate.md`. Receipt: `REGRESSION:
PASS (cases=7 passed=7 …)` at runner `89722ddb…`.

Wave-2 correction (LedgerMatrixAppend, DepthCritic): the block above calls the
queue "§5". The queue row that said `unmeasured` is this file's §3 (`:109`),
and the offer queue is `fleet-suite-census.md` §5 (`:283`). Measuring the gate
was tameshi's own read-only case; it did not drain the service queue.
