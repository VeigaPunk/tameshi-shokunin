# T54W1Read23 — cold read of `### Round-26 gate/probe registry — report interop`

Content commit (cand): `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0, round 54).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Read from git objects only; every execution below ran in a `git clone --shared` copy at C0 under my own scratch, never in the lane.

## Section identity

`python3 .ufo/waves/round-54/reader-section.py <lane> 59c38109bf119d0e9d4f878644a82babc937bc1e "### Round-26 gate/probe registry — report interop"` printed:

```
{"heading": "### Round-26 gate/probe registry \u2014 report interop", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 2158, "end": 2197, "section_sha256": "cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52"}
```

The section is lines 2158–2197 of `SKILL.md` at C0 (23,083 bytes read through `git show 59c3810…:SKILL.md`): the round-26 `tools/mte-interop.py` table, then `#### Gate/probe registry — round 51` with 29 gate/probe rows.

## Finding (1)

### F1 — the mte row states a PASS rule the tool does not implement

Quote (byte-exact in the section, line 2162):

> `0 PASS (every leg found conforms, at least one leg)`

Why: the tool raises SETUP and exits 2 unless the leg set equals the ten ledger legs (`tools/mte-interop.py:317-319`), so a PASS always carries all ten legs and the cell's `at least one leg` states a PASS rule the tool never implements, contradicting the same cell's own SETUP clause `leg set not equal to the ten ledger legs`.

Receipt (run in the C0 clone with my scratch as TMPDIR):

```
$ D=$(mktemp -d "$TMPDIR/onleg.XXXXXX")
$ python3 tools/mte-interop.py --check --workdir "$D"
MTE_INTEROP: SETUP (leg set [] / table set [] differs from the ten ledger legs ['bash-checklist-run', 'bash-drift-pins', 'bash-mado-verify', 'bash-surface-census', 'bash-tsukuroi-census', 'js-cite-check', 'js-claims-check', 'js-kimi-census', 'js-round-gate', 'js-sources-check'])
rc=2
```

So a run that finds any leg count other than ten is SETUP/2, not `0 PASS`, and a PASS cannot occur with "at least one" leg. The same understatement was recorded by the round-27 independent reader of this heading (`Read39`: "PASS wording … understates the rule … so PASS means nine of nine") and was never changed when the ledger grew to ten legs in round 51. Fix is one clause: `0 PASS (every leg found conforms: the ten ledger legs)`.

## What I opened and checked (no other finding)

Artifacts opened at C0 (all through `git show C0:<path>` or the C0 clone):

| Artifact | Checked |
|---|---|
| `tools/mte-interop.py` | exit map (0/1/2/64 via `Parser.exit(64)`), `LEG_TABLE` = 10 legs, leg-set equality at 317-319, `--emit`/mkdtemp write sites (199, 276, 309, 386), `run_regression` sibling symlinks (not hermetic) |
| `tools/bash-witness-study.py` | `WITNESS_SELFTEST:`/`VERDICT:` last-line order (1729-1731), `--evidence` flag, `strict_scratch_root` used only by `cmd_selftest` (1260), so the `check` verdict map is unaffected by the round-53/54 scratch arm |
| `tools/command-binding.py` | `COMMAND_BINDING_SELFTEST:` is the last stdout line (193) |
| `tools/context-capture.py` | `SELFTEST: PASS (n/n)` at 1799, no lane write during `--check` |
| `tools/env-diff.py` | `ENVDIFF_SELFTEST:` last line (213), `tameshi-r21-envdiff.` prefix (80) |
| `tools/evidence-disposition.py` | `SELFTEST: PASS (n/n)` (3142), `tameshi-r14-evidence-disposition-selftest.` prefix (2370) |
| `tools/golden-verdict.py` | `/3` selftest emitter (66), TMPDIR temp dir only |
| `tools/pbt-staged-id.py` | `cases=/failed=` emitter (1092), `pbt-staged-id-` work root (807), usage folds to 2 (894) |
| `tools/pin-disposition.py` | exit map 0/2 (docstring 77-80) plus 1 on selftest FAIL (1346), selftest prefix (725) |
| `tools/receipt-measure.py` | six `ITEM_IDS` (37), delegation of `--repo/--rev` unchanged to stage `measure.py`, prefixes `receipt-measure-selftest.` and stage `tameshi-r20-measure.` |
| `tools/receipt-window.py` | `EXIT_CLEAN/FAIL/CE/USAGE = 0,1,2,64` (23), 64 for missing `--contract/--receipts` (362) |
| `tools/registry-check.py` | docstring exit map (52-54), `strict_scratch_root` (757-766), `--rev` mkdtemp (780), selftest emitter `SELFTEST: PASS (n cases)` (1830) |
| `tools/registry-replay.py` | `RUNNER_NOT_HELD`, `RUNNER_CLEANUP_FAILED`, `STREAM_LIMIT`, `INVALID_OBSERVATIONS` literals; registry digest check (139) |
| `tools/repeat-control.py` | all seven verdict literals; `SELFTEST: PASS (n cases)` (872) |
| `tools/round21-measure.py` | reads the `FLEET` literal out of `c2-count.py` (77); selftest 13 checks |
| `tools/shrink-case.py` | exit-2 class for bad argument/unreadable/no-kill (docstring), `SHRINK_SELFTEST` emitter (605) |
| `tools/staged-id-guard.py` | `SELFTEST_REGISTRY`/`SELFTEST_STAGED_*` literals, read-only (`open(path,'rb')` only), `VERDICT:` emitter |
| `tools/tally-audit-v2.py` | `REF_BLOCK` tally + `rm -rf "$root"` on auto PASS (100-103), `CONFIGS` (265), `tally-audit-v2.*` scratch (562) |
| `tools/tally-audit-v3.py` | `auto_root()` really allocates `/tmp/tameshi-r4-2-regression.XXXXXX` and `atexit`-removes it (408-433); 6-char suffix shape |
| `tools/tally-audit.py` | `TALLY_AUDIT_SELFTEST` (436), `tally-audit` prefix |
| `tools/trace-inputs.py` | `trace-inputs-run-` private workdir (593), `SELFTEST:` emitter (965) |
| `tools/wave-accounting.py` | 8/8 + 16/16 emitters (188-192) |
| `tools/wave-parent-settle.py` | `/3` (59), no tempfile use (0 hits) |
| `tools/wave-route-mix.py` | 8/8 emitter (89), ROUTEMIX line on stderr (121-123), no writes |
| `tools/witness-metadata.py` | `SELFTEST: PASS 39/39` (1211), pinned lane files (68-128), `finally` cleanup (1185) |
| `tools/write-path-census{,-v2,-v3,-v4}.py` | exact counter emitters, `GATES` = 21 names (22-43), v3 `EXPECT` table (268), no lane writes |
| `tools/mutate-and-run.sh` | `--regression/--target/--defects/--suite/--workdir` flags, `DEGRADED` line (581), exit map 0/1/2/64 (81-82), `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"` (1432), ten golden legs in the header, `REGRESSION_TABLE` output (1392), embedded `TABLE_*` |
| `tools/registry.json` | 56 rows; `mte-interop-selftest` expects `MTE_SELFTEST: 17/17 pass`, `mte-interop-check` expects `MTE_INTEROP: PASS legs_conforming=10/10`; the seven selftest rows carry the new `scratch_root` cell |
| `.ufo/evidence/round-12/BashWitness/{declaration,summary,manifest}.json`, `declared.tsv`, `rerun-20261020T035435Z/summary.json` | declaration pins `declared.tsv` sha; `check` reads them |
| `.ufo/evidence/round-12/ControlGate/{expected.json,mismatch/expected.json}` | driven as `--snapshot` in both directions |
| `.ufo/evidence/round-13/{expected,verification,producer-oracle-repair,pin-manifest,witness-metadata}.json` | present; `pin-manifest` driven through `pin-disposition` |
| `.ufo/evidence/round-14/context-receipt.json` | digest `05cb55b8…` matches the cell's prefix |
| `.ufo/evidence/round-20/{contract,public-cli-cases}.json`, `stage/{measure,receipt-window}.py`, `final/{receipts,historical-receipts,receipt-window-selftest}.json`, `.ufo/waves/round-20/dispatch.json` | the committed `receipt-window-selftest.json` records `exit 0` and last line `RECEIPT_WINDOW_SELFTEST: 20/20 pass` |
| `.ufo/evidence/round-21/{c2-contract.json,f5/receipt.json,c1-survivors.py,c2-count.py}` | `FLEET = Path("/home/vgpnk/Projects/shokunin")` (c2-count.py:19) — the cell's fleet-root sentence resolves |
| `.ufo/evidence/round-22/{measure.py,accounting-extra-cases.json}` | present; selftest 8/8 + 16/16 |
| `.ufo/evidence/round-23/{requirements,registry-baseline,extra-cases}.json`, `.ufo/evidence/round-24/extra-cases.json` | present |
| `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec` | present; the round-51 spec names the pinned rev/blob and 13 cases |
| `.ufo/evidence/round-32/heldout/` | 22 committed seed files (the cell says "committed provenance … not read at run time") |
| `.ufo/evidence/round-38/golden/measure.py`, `corpus/knowledge/{golden-comparison-verdict,fleet-kill-rate-ledger}.md` | present |
| `.ufo/evidence/round-40/census/fixtures.json`, `.ufo/evidence/round-41/census/fixtures.json`, `.ufo/evidence/round-49/c2/panel.json` | present |
| `.ufo/waves/round-40/settlement-receipt.json`, `.ufo/waves/round-41/settlement-receipt.json` | driven through `wave-parent-settle` |

Every path the section cites was probed with `git cat-file -e C0:<path>`: **75 cited paths, 0 missing** (including `tools/vendor/mutation-testing-{report-schema,metrics}-3.9.0.tgz`).

### Counts reproduced exactly (29 selftests, C0 clone)

| Row | Claimed | Observed last line | exit |
|---|---|---|---|
| bash declared-witness study | `WITNESS_SELFTEST: 51/51 pass` then `VERDICT:` | `WITNESS_SELFTEST: 51/51 pass` / `VERDICT: PASS` | 0 |
| context receipt replay | `SELFTEST: PASS (49/49)` | `SELFTEST: PASS (49/49)` | 0 |
| environment-profile differential | `ENVDIFF_SELFTEST: 9/9 pass` | `ENVDIFF_SELFTEST: 9/9 pass` | 0 |
| evidence disposition accounting | `66/66 cases` | `SELFTEST: PASS (66/66)` | 0 |
| golden verdict classes | `GOLDEN_VERDICT_SELFTEST:` | `GOLDEN_VERDICT_SELFTEST: 3/3 pass` | 0 |
| mte report interop | `MTE_SELFTEST: 17/17 pass` | `MTE_SELFTEST: 17/17 pass` | 0 |
| pbt staged-id generator | `cases=35 failed=0` | `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` | 0 |
| pin disposition | `SELFTEST: PASS n/n` | `SELFTEST: PASS (19/19)` | 0 |
| round-20 receipt-window measure | `10/10 pass` | `RECEIPT_MEASURE_SELFTEST: 10/10 pass` | 0 |
| receipt-window validity | `20/20 pass` | `RECEIPT_WINDOW_SELFTEST: 20/20 pass` | 0 |
| entry-registry walk | `SELFTEST: PASS (51 cases)` | `SELFTEST: PASS (51 cases)` | 0 |
| frozen registry replay | `10/10 pass` | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 0 |
| repeated control agreement | `SELFTEST: PASS (29 cases)` | `SELFTEST: PASS (29 cases)` | 0 |
| round21 measure facade | `13/13 pass` | `ROUND21_MEASURE_SELFTEST: 13/13 pass` | 0 |
| shrink-case | `cases=21 failed=0` | `SHRINK_SELFTEST: cases=21 failed=0` | 0 |
| staged-id adoption guard | `VERDICT: PASS` + `cases=N failed=M` | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` / `VERDICT: PASS` | 0 |
| tally audit v2 | `22/22 pass` | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | 0 |
| tally audit v3 | `35/35 pass` | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | 0 |
| tally audit undercount guard | `11/11 pass` | `TALLY_AUDIT_SELFTEST: 11/11 pass` | 0 |
| traced input surface | `SELFTEST: n/n` | `SELFTEST: 30/30` | 0 |
| wave accounting | `8/8 frozen plus 16/16 supplemental` | `ACCOUNTING_SELFTEST: 8/8 pass` + `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass` / `FINDING: SELFTEST_PASS` | 0 |
| wave parent settlement | `3/3 pass` | `WAVE_PARENT_SELFTEST: 3/3 pass` | 0 |
| wave-route-mix | `8/8 pass` | `ROUTEMIX_SELFTEST: 8/8 pass` | 0 |
| witness metadata companion | `SELFTEST: PASS 39/39` | `SELFTEST: PASS 39/39` | 0 |
| write-form census v2 | `bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` | identical | 0 |
| write-path census v3 | `var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` | identical | 0 |
| write-path census v4 | `cases=15 failed=0` | `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0` | 0 |
| write-path census | `planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1` | identical | 0 |
| command binding receipts | finding id only | `COMMAND_BINDING_SELFTEST: 44/44 pass` | 0 |

### Entry commands driven

```
$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
SNAPSHOT_OBSERVED id=controls_match exit=0
REPEAT_CONTROL: controls_match                                   rc=0
$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch
SNAPSHOT_OBSERVED id=controls_mismatch exit=1
REPEAT_CONTROL: controls_mismatch                                rc=1     (matches "0 clean (controls_match); 1 failed (controls_mismatch)")
$ python3 tools/witness-metadata.py --check --lane-root . --companion .ufo/evidence/round-13/witness-metadata.json
WITNESS_METADATA: metadata_consistent reason=ok exit=0 …         rc=0
$ python3 tools/context-capture.py --check
CONTEXT: OK (id=context_consistent … sha256=05cb55b86446… exit=0 findings=0)   rc=0
$ python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-40/settlement-receipt.json
WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal         rc=0
$ python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-41/settlement-receipt.json
WAVE_PARENT: verdict=UNSETTLED detail=parent_exit_unix missing                rc=1
$ python3 tools/write-path-census.py --census .   → rc=0 (all 21 gate tools classified)
$ python3 tools/write-path-census-v4.py --file tools/env-diff.py   → rc=0
$ python3 tools/write-path-census-v3.py --file tools/env-diff.py
expected_sites=0 parse_errors=0 scratch_expected=0 sites=4 symlink_expected=0 unflagged=0 variable_expected=0   rc=0
$ python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin  → rc=0
```

The `$TMPDIR`-unusable rule stated in the `entry-registry walk` row also resolves:

```
$ TMPDIR=/nonexistent-xyz python3 tools/registry-check.py --selftest
registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-xyz' (could-not-evaluate)
rc=2
$ TMPDIR=/nonexistent-xyz python3 tools/bash-witness-study.py selftest
WITNESS_STUDY: could-not-evaluate: … TMPDIR is not a usable directory: '/nonexistent-xyz' (could-not-evaluate)
rc=2
```

No traceback, the value is named, exit 2 — as the `read-only`/scratch text of the two rows says.

## Checked and deliberately not filed

- `python3 tools/bash-witness-study.py check` at C0 exits 1 with
  `WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de470… committed=75ed934d…` (the declaration froze the round-12 runner). Not filed: the row's verdict map names `digest drift` as a `1 failed` arm and its Pinned-values cell says the digest is *frozen*, so the behaviour matches the cell; also, the row does not assert `check` is currently clean. (Runner sha256 at C0 and at base `d33053f` is the same `977de470…`.)
- The mte self-test command in the round-51 row is bare `python3 tools/mte-interop.py --selftest` while the registry row and the round-26 row's Command cell carry the `uv run --no-project --with jsonschema==4.25.1` prefix. Not filed: the cell states the precondition (`needs python jsonschema and node`) and bare python3 gives `MTE_SELFTEST: 17/17 pass`, exit 0, on this host.
- `Owner tameshi: the registry has no owner field. Not filed: ownership is a section-table column, not a registry claim.
- `at 84aa673` after `SELFTEST: PASS (51 cases)` is a provenance qualifier in the same style as `at exit 0` elsewhere; the measured last line is exactly `SELFTEST: PASS (51 cases)` and `84aa673a1a476e48ccf239335696f0518d08bae7` resolves in the lane.

## Seat hygiene

- Every execution ran in `/fast/scratch/hyaku/tameshi-r54/T54W1Read23/lane-c0` (`git clone --shared` of the lane at C0; `git rev-parse --show-toplevel` printed that clone), with `TMPDIR` under my own scratch; nothing was written under `/tmp` and no lane file was read from the working tree for the section text.
- No lane file was edited; no mutating git/jj command ran anywhere; no tool was installed (system `python3`, `node`, `uv` sufficed).
- `git -C <lane> status --porcelain` shows only other seats' untracked wave directories — no modification from this seat.
- My scratch tree (clone, logs, dumps) is removed at exit.
