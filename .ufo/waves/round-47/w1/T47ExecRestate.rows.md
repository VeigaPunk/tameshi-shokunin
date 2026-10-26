# T47ExecRestate — the C1 restated rows at the freeze (full 22-statement `--emit`)

seat: `T47ExecRestate` · item: run the FULL C1 counter once at the freeze with `--emit`; deliver the rows.

| field | value |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/tameshi-shokunin` |
| rev measured | `9acfbe21435e1976636a276448dee1d5e7155915` (the freeze) |
| base | `0b5b7cd2b2c15d23086e811a0f0348d84261277b` |
| counter | `.ufo/evidence/round-47/calibration/measure.py` (self-pinned by the run: `self_pin=1`) |
| statements list | `statements.json`, sha256 `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56` (`stmts_pin=1`) |
| command | `python3 .ufo/evidence/round-47/calibration/measure.py --lane LANE --rev 9acfbe21… --base 0b5b7cd2… --work WORK --emit` |
| work dir | `/var/tmp/tameshi-r47-T47ExecRestate/w` (empty at start; moved off `/tmp` on the L1’s ENOSPC instruction; 2.4 GiB) |
| profiles | six per statement: P0 live host, P1 clean full, P2 = P1−bwrap, P3 = P1−jj, P4 = P1−node, P5 = P1 inside a bwrap-bound decoy fleet root |
| wall | 2385 s (one pass, `jobs=14`, 132 observations) |
| verdict line | `C1_R47: … total=22 … C1_R47_PASS=false` (`unparsed=22`: the standing rows carry no `deps` clause yet) |

At the freeze no row can be parsed (`claim_of` needs the full `deps` clause, `measure.py` `CLAIM_CAP`), so this run
compares **no value**: `mismatches=0` is vacuous here. The 22 rows below are the *observations* the draft must state.

## 1. The 22 rows, verbatim from `--emit` (counter order)

```text
EMIT_CAP | sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0, tool sha256 `b9b754713c9c`, deps `none` | fleet round 1 (kaika) |
EMIT_CAP | mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof; `--regression` refuses a miscounted tally (round 30) | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0, tool sha256 `a7d3f2dd7d47`, deps `none` | historical round 3; re-demonstrated round 31 |
EMIT_CAP | six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9`, exit 0, tool sha256 `a7d3f2dd7d47`, deps `fleet-root,node` | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
EMIT_CAP | repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, exit 0, tool sha256 `296fe566dc59`, deps `none` | round 12 |
EMIT_CAP | six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0, tool sha256 `331529eadafe`, deps `none` | round 13 |
EMIT_CAP | exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations | `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0, tool sha256 `df3390682a04`, deps `none` | round 13 |
EMIT_CAP | effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)`, exit 0, tool sha256 `39ee5c5effd9`, deps `jj` | round 14 |
EMIT_CAP | retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → `SELFTEST: PASS (49/49)`, exit 0, tool sha256 `7e4519d9a0ea`, deps `fleet-root` | round 15 |
EMIT_CAP | hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0, tool sha256 `e8b47ab7cf23`, deps `bwrap,node` | round 21 |
EMIT_CAP | callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | `python3 tools/wave-accounting.py --selftest` → `ACCOUNTING_SELFTEST: 8/8 pass`, exit 0, tool sha256 `96b3038a77f8`, deps `none` | round 22 |
EMIT_CAP | required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations | `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0, tool sha256 `9230c68e53a5`, deps `none` | round 23 |
EMIT_CAP | refusing-registry-replay | replay frozen registry requirements and refuse to publish a binding bundle from rejected rows | `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0, tool sha256 `9fcd2dbba737`, deps `none` | round 24 |
EMIT_CAP | mutation report interop | emit each recorded leg as a mutation-testing-elements report and check it with the official schema and metrics library | `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, exit 0, tool sha256 `193ea6e32f89`, deps `node` | round 25 |
EMIT_CAP | tally-audit-v2 runner audit | audit the mutation runner's regression tally without editing it: head/static/runtime/harness checks kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies, controls-gated counter | `python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0, tool sha256 `7b11ba25aead`, deps `env,fleet-root,node` | round 34 (tool landed round 33, predicate honestly not decided there) |
EMIT_CAP | tally-audit-v3 runner audit | audit the runner's regression tally without editing it, across all four `(root,auto,KEEP)` triples, comparing the FULL stdout plus exit and scanning a comment-blinded code view; kills 6/6 public + 4/4 sealed must-kill copies (failing check exactly `runtime`), accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies, under a pinned sha256 | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `env` | round 35 |
EMIT_CAP | bounded ANSI-C code_view | Keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, and preserve a literal `#` inside the quote; nested substitutions and unquoted backslash-newline remain unsupported | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `env,fleet-root,node` | round 37 |
EMIT_CAP | write-path-census-v2 | classify a string-literal `expected.json` on `.write_bytes` and an `os.replace` / `os.rename` write, which the round-39 census misses, with planted flagged and scratch controls | `python3 tools/write-path-census-v2.py --selftest` → `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`, exit 0, tool sha256 `402285329588`, deps `none` | round 40 |
EMIT_CAP | write-path census destination resolution | resolve a write destination held in a variable through up to four assignments/`os.path.join`/`+`/`/`/f-string hops and classify it as expected-value, scratch or update-flagged, for `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and `os.symlink`; v2 cannot connect a destination to a token that is not on the same line | `python3 tools/write-path-census-v3.py --selftest` → `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`, exit 0, tool sha256 `095924a7a165`, deps `none` | round 41 |
EMIT_CAP | staged-id adoption guard | decide, before any append, which ids of a staged registry package collide with the lane registry (0-3-space census pattern), dedupe a staged row whose document the registry already holds, refuse its own naive arithmetic map because the targets are still staged ids, and admit only a by-document map whose held rows dedupe to their registry id and whose new documents take ids at or above the safe floor | `python3 tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`, exit 0, tool sha256 `03a796c5726c`, deps `none` | round 43 |
EMIT_AXIS | depth | 9 | One point per recorded mutation case in the runner's ledger comment (`tools/mutate-and-run.sh:87-95`, nine legs), capped at 10; command D prints `recorded_cases=9 depth_score=9` (`.ufo/evidence/round-46/before/no-harm-at-base.stdout`, `after/no-harm.stdout`), tool sha256 `a7d3f2dd7d47`, deps `none` |
EMIT_AXIS | calibration | 6 | Restraint score of the strict cold-read monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` (`calibration_restraint_score`; `box3_full_page=false`, 60 of 64 sections credited): two points per restrained, evidence-linked `[~]` SHONEN box; box 3 is not credited. The round-31 table above stated 8; the monitor prints 6 at the round-46 base, so 8 was a stale standing value, tool sha256 `657f009bdf1c`, deps `none` |
EMIT_AXIS | freshness | 9 | `floor(10 * fresh / 73)` from the round-45 counter `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV` (`fresh=71`, `score=9`; 2 rows disputed: S048, S093); the round-44 one-document unit (the S160 row count, 1; command in the round-45 block above) stays a monitor, tool sha256 `ba64041f49ff`, deps `none` |
```

## 2. The verdict line, verbatim

```text
C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=22 unobservable=0 dep_mismatch=0 unpinned=0 append_only=1 total=22 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false
```

## 3. `PROFILES` lines — every statement whose observed dependence set is not `none`

```text
PROFILES six-leg regression ledger: P0=REGRESSION: PASS (cases=9 passed=9|0 P1=REGRESSION: PASS (cases=9 passed=9|0 P2=REGRESSION: PASS (cases=9 passed=9|0 P3=REGRESSION: PASS (cases=9 passed=9|0 P4=REGRESSION: SETUP (cases=9 passed=4|2 P5=REGRESSION: SETUP (cases=9 passed=0|2
PROFILES effective expectation reconciliation: P0=SELFTEST: PASS (66/66)|0 P1=SELFTEST: PASS (66/66)|0 P2=SELFTEST: PASS (66/66)|0 P3=UNOBSERVABLE|exit=1 P4=SELFTEST: PASS (66/66)|0 P5=SELFTEST: PASS (66/66)|0
PROFILES retained invocation-context gate: P0=SELFTEST: PASS (49/49)|0 P1=SELFTEST: PASS (49/49)|0 P2=SELFTEST: PASS (49/49)|0 P3=SELFTEST: PASS (49/49)|0 P4=SELFTEST: PASS (49/49)|0 P5=SELFTEST: PASS (49/49)|1
PROFILES hermetic env-differential probe: P0=ENVDIFF_SELFTEST: 9/9 pass|0 P1=ENVDIFF_SELFTEST: 9/9 pass|0 P2=ENVDIFF_SELFTEST: 2/9 pass|1 P3=ENVDIFF_SELFTEST: 9/9 pass|0 P4=ENVDIFF_SELFTEST: 8/9 pass|1 P5=ENVDIFF_SELFTEST: 9/9 pass|0
PROFILES mutation report interop: P0=MTE_SELFTEST: 17/17 pass|0 P1=MTE_SELFTEST: 17/17 pass|0 P2=MTE_SELFTEST: 17/17 pass|0 P3=MTE_SELFTEST: 17/17 pass|0 P4=UNOBSERVABLE|exit=2 P5=MTE_SELFTEST: 17/17 pass|0
PROFILES tally-audit-v2 runner audit: P0=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P1=UNOBSERVABLE|timeout P2=UNOBSERVABLE|timeout P3=UNOBSERVABLE|timeout P4=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P5=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0
PROFILES tally-audit-v3 runner audit: P0=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P1=UNOBSERVABLE|timeout P2=UNOBSERVABLE|timeout P3=UNOBSERVABLE|timeout P4=UNOBSERVABLE|timeout P5=UNOBSERVABLE|timeout
PROFILES bounded ANSI-C code_view: P0=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P1=UNOBSERVABLE|timeout P2=UNOBSERVABLE|timeout P3=UNOBSERVABLE|timeout P4=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P5=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0
```

Eight of 22 statements differ in some variant profile in *this* run: `six-leg regression ledger`, `effective expectation reconciliation`, `retained invocation-context gate`, `hermetic env-differential probe`, `mutation report interop`, `tally-audit-v2 runner audit`, `tally-audit-v3 runner audit`, `bounded ANSI-C code_view`.
Three of those eight are load artifacts — see §5 before writing the table.

## 4. Dependence sets, this run vs the five T47ExecObs seats

| statement | deps in this run | Obs seat | agreement |
|---|---|---|---|
| sources-registry | `none` | ObsA none | agree |
| mutation sweep runner | `none` | ObsB none | agree |
| six-leg regression ledger | `fleet-root,node` | ObsE fleet-root,node (run1); run2 added a spurious jj | agree; flake hazard noted by ObsE |
| repeated pristine-control gate | `none` | ObsB none | agree |
| six-leg content-disposition probe | `none` | ObsB none | agree |
| exposed witness provenance correction | `none` | ObsB none | agree |
| effective expectation reconciliation | `jj` | ObsC jj | agree |
| retained invocation-context gate | `fleet-root` | ObsC fleet-root | agree |
| hermetic env-differential probe | `bwrap,node` | ObsC bwrap,node (work dir outside /tmp); env,node at /tmp | agree |
| callback-authoritative wave accounting | `none` | ObsC none | agree |
| required-command-receipt-binding | `none` | ObsD none | agree |
| refusing-registry-replay | `none` | ObsD none | agree |
| mutation report interop | `node` | ObsD node | agree |
| tally-audit-v2 runner audit | `env,fleet-root,node` | ObsD none  <-- DISAGREES with this run (load artifact) | DISAGREE (artifact) |
| tally-audit-v3 runner audit | `env` | ObsD none  <-- DISAGREES with this run (load artifact) | DISAGREE (artifact) |
| bounded ANSI-C code_view | `env,fleet-root,node` | ObsE none  <-- DISAGREES with this run (load artifact) | DISAGREE (artifact) |
| write-path-census-v2 | `none` | ObsE none | agree |
| write-path census destination resolution | `none` | ObsE none | agree |
| staged-id adoption guard | `none` | ObsE none | agree |
| depth | `none` | ObsA none | agree |
| calibration | `none` | ObsA none | agree |
| freshness | `none` | ObsA none | agree |

Every disagreement is the same object: a **timeout**, not a dependence (§5).

## 5. The three rows whose deps clause here is a load artifact

`tally-audit-v2 runner audit`, `tally-audit-v3 runner audit` and `bounded ANSI-C code_view` did not finish inside
their frozen per-statement timeout in some profile of this run. `observe()` maps `TimeoutExpired` to
`(None, "timeout")` and `comparable()` maps that to `("UNOBSERVABLE", "timeout")`, so a timeout is compared as a
*difference* and the counter reports it as a dependence name. It is not one.

The proof is internal to this run: `tally-audit-v3 runner audit` and `bounded ANSI-C code_view` are the **same
command** (`python3 tools/tally-audit-v3.py --selftest`) at the same rev, yet in the same profile they disagreed —
P4/P5 passed for one statement and timed out for the other. A command cannot depend on `node` and not depend on it
at once; the difference is scheduling. Same for `env`: it is defined as P0 ≠ P1, and here it fires only because P1
timed out while P0 passed.

Measured causes (all receipts under `/var/tmp/tameshi-r47-T47ExecRestate/`):

| statement | frozen timeout | solo runtime (measured here) | cells that timed out in this run | headroom |
|---|---|---|---|---|
| tally-audit-v2 runner audit | 900 s | **802 s** (`probe-v2-P1.out`, 22/22 pass) | P1, P2, P3 (900 s cap) | 12 % |
| tally-audit-v3 runner audit | 1800 s | **513 s** (`probe-v3-P1.out`, 35/35 pass) | P1–P5 | 3.5× |
| bounded ANSI-C code_view | 1800 s | 513 s (same command) | P1, P2, P3 | 3.5× |

The 14-way schedule in `measure()` runs these beside `six-leg regression ledger` (9 legs, ~8 min per profile) and
`mutation sweep runner` (106 cases); under that concurrency the 802 s solo run no longer fits the 900 s cap. Note the statements list is frozen and sha256-pinned: the timeout cannot
be raised without breaking `stmts_pin`.

Direct dependence evidence, independent of the timeouts:

- neither `tools/tally-audit-v2.py` nor `tools/tally-audit-v3.py` contains the token `node`, `jj`, `bwrap` or `fleet`
  (`grep -nE "node|jj|bwrap|fleet"` → 0 matches in both files), so none of the three names the counter reported can
  be a prerequisite of these selftests;
- `tally-audit-v3 --selftest` under the exact P2 shim (bwrap removed) → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`,
  546 s, obs 1453 B — the same bytes as P0/P4/P5 (`probe-v3-P2.out`);
- `tally-audit-v2` passed under P0, P4 and P5 with the identical 869-byte obs in this run, and under P1 solo;
- the P3 (jj) cells were measured by two other seats on this rev: ObsD (`none`, all six profiles) and ObsE
  (`none` for the v3 command).

### Row text to write instead (only the deps field changes; every other byte is the emit output)

```text
EMIT_CAP | tally-audit-v2 runner audit | audit the mutation runner's regression tally without editing it: head/static/runtime/harness checks kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies, controls-gated counter | `python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0, tool sha256 `7b11ba25aead`, deps `none` | round 34 (tool landed round 33, predicate honestly not decided there) |
EMIT_CAP | tally-audit-v3 runner audit | audit the runner's regression tally without editing it, across all four `(root,auto,KEEP)` triples, comparing the FULL stdout plus exit and scanning a comment-blinded code view; kills 6/6 public + 4/4 sealed must-kill copies (failing check exactly `runtime`), accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies, under a pinned sha256 | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `none` | round 35 |
EMIT_CAP | bounded ANSI-C code_view | Keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, and preserve a literal `#` inside the quote; nested substitutions and unquoted backslash-newline remain unsupported | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `none` | round 37 |
```

## 6. Notes for the writer

- `unparsed=22` at the freeze means the counter never compared a value in this run; it parsed no row. The 22 rows are
  the observation set, and `mismatches=0` must not be quoted as "the standing rows are correct".
- The value, exit and tool sha256 of the 17 statements that do not time out agree with what ObsA–ObsE measured on
  the same rev, independently. The tool sha256 prefixes are `git show HEAD:<file>` digests, invariant across profiles.
- `deps` vocabulary is `{bwrap, env, fleet-root, jj, node}`; two real prerequisites seen in this run have no slot and
  must not be folded into a name: the ledger’s and the tally audits’ hard-coded `/tmp` scratch (`tools/tally-audit-v3.py`
  `auto_root()`), and `git` (used by the ledger and by `pin-disposition`/`mutation sweep runner`).
- The deciding run must be taken on an otherwise idle host with several GiB free on **both** the `--work`
  filesystem and `/tmp`: `tally-audit-v3`’s selftest allocates a real `/tmp/tameshi-r4-2-regression.*` root and its
  31/35 cases collapse without it (ObsD §7). A `/tmp`-full or loaded deciding run turns these three rows into
  `dep_mismatch` and fails C1 through no fault of the row.

## 7. Receipts

`/var/tmp/tameshi-r47-T47ExecRestate/`:

```text
emit.out                     the full 68-line output of the one pass: 22 STATEMENT, 22 PROFILES, 22 EMIT, verdict, EXIT=1
probe-v3-P1.out              513 s  TALLY_AUDIT_V3_SELFTEST: 35/35 pass (P1 env, no siblings)
probe-v2-P1.out              802 s  TALLY_AUDIT_V2_SELFTEST: 22/22 pass (P1 env, no siblings)
probe-v3-P2.out              546 s  TALLY_AUDIT_V3_SELFTEST: 35/35 pass (P1 minus bwrap)
obs/                         the 121 obs-*.stdout files of the pass (one per non-timed-out cell; the 11 timeout
                             cells leave no file: tally-v2 P1-P3, tally-v3 P1-P5, bounded ANSI-C P1-P3)
```

`emit.out` sha256 `71df39bd67b3ea999908493908b6185f7e343c815cf7587c4e5dec93f16cb67c`, 18665 bytes.
