# T51W2ExecTool14 — C3 row falsification: `tools/registry-replay.py`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, candidate `6d8c11e378aa90b12650808e1b79270742935f15` (base `9962033fd7a75aa2f2847e979dd687a5d28505a1`).
- Row under test: `SKILL.md:2155`, inside section `#### Gate/probe registry — round 51` (`SKILL.md:2138`). Row index 14 of the 30 rows in that section.
- Tool: `tools/registry-replay.py`, sha256 `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` at CAND.
- Receipts: `.ufo/waves/round-51/w2/T51W2ExecTool14/` (stdout/stderr of every probe, `run-full-observations.json`, and the four bundle files of the clean subset run).
- This seat had no `## Reader` item (not one of the twenty re-key readers); it makes no cold-read credit claim.

## Verdict

The row is **counter-conformant and operationally truthful on its load-bearing fields** (kind, entry, exit map incl. usage code, write scope, last-line marker). Verified two ways: by probe, and by importing the C3 counter's own `row_reason`/`run_row` from `.ufo/evidence/round-51/c3/measure.py` and running them against the CAND clone — both returned `None` with last line `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, i.e. the counter credits this row.

One real field mismatch and four precision/limits were found (none blocks C3 for this row):

| # | Severity | Claim | Finding |
|---|---|---|---|
| M1 | real, narrow | `Pinned values` lists `tools/registry-check.py` | no digest of it is compared anywhere; a byte-changed runner still yields exit 0 and a published bundle (measured). The parenthetical ("runner digest taken from the clone copy that runs") is provenance wording, not a pin. |
| M2 | precision | verdict-map text for exit 1 | enumerates refusals + uncaught traceback; a *self-test case failure* also exits 1 (measured `9/10 pass`, exit 1) and is not named. |
| M3 | precision | entry command cell | `--repo .` states no fleet precondition; the run only reaches 0 when the checkout's parent directory holds the sibling lanes (or symlinks). The write-scope cell discloses the mechanism, and the measured refusal in a sibling-free clone exits 1 exactly as the verdict map declares. |
| M4 | precision | write scope file set | the four named files appear together only on exit 0; a refused run writes `observations.json` alone (measured). |
| M5 | coverage, not falsity | self-test | 9 of 10 cases are `--project`, 1 is `--plan` (`tools/registry-replay.py:202-245`); no case exercises the `--run` entry command, so the gate's end-to-end path is untested by its self-test. |

**Known C3 blocker is not this row.** Round-51 row 16 is `round21 measure facade`; its self-test fails from a sibling-free clone (observed in my full-panel run: exit 1, `CalledProcessError` at `tools/round21-measure.py:74`). My row (index 14) passes its self-test in exactly that context — it needs no sibling repos.

## Row under test (verbatim, `SKILL.md:2155`)

```
| frozen registry replay | gate | `python3 tools/registry-replay.py --run --repo . --rev REV --requirements .ufo/evidence/round-23/requirements.json --registry-baseline .ufo/evidence/round-23/registry-baseline.json --out DIR` | 0 clean; 1 failed (refused rows: RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT; an uncaught traceback also exits 1); 2 could-not-evaluate (registry digest mismatch, frozen requirements drift, clone HEAD mismatch, INVALID_OBSERVATIONS); 64 could-not-evaluate (usage) | `python3 tools/registry-replay.py --selftest` → REGISTRY_REPLAY_SELFTEST: 10/10 pass | `.ufo/evidence/round-23/requirements.json`, `.ufo/evidence/round-23/registry-baseline.json`, `tools/registry-check.py` (runner digest taken from the clone copy that runs) | caller-selected `--out` DIR (observations.json, bundle.json, expected.json, live-dependent.json) plus a private clone under TMPDIR; row commands run inside that clone, whose fleet mirror symlinks the live siblings, so the run is not write-isolated from them; selftest under TMPDIR | tameshi |
```

The counter's section parser sees exactly one row for this tool. The older 8-cell table row at `SKILL.md:2052` is **invisible** to the counter: its nearest heading is `SKILL.md:1964` `### Round-21 gate/probe registry — finite environment differential`, which does not match `^#{2,4} Gate/probe registry`. That is predicate-by-design, not a defect; it also means the earlier row's text (no finding id in its self-test cell) never enters the coverage decision.

## Measured probes (clone at CAND, scratch TMPDIR, stdin `/dev/null`)

| Probe | Invocation | Exit | Last stdout line | Wall |
|---|---|---|---|---|
| row self-test (exact backticked command) | `python3 tools/registry-replay.py --selftest` | **0** | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 389 ms |
| usage probe | `python3 tools/registry-replay.py --r51-no-such-flag` | **64** | (stdout empty; stderr `registry-replay: one of the arguments --run --project --plan --selftest is required`) | 38 ms |
| entry command, full frozen panel (43 rows) | `--run --repo . --rev 6d8c11e… --requirements .ufo/evidence/round-23/requirements.json --registry-baseline .ufo/evidence/round-23/registry-baseline.json --out OUT` | **1** | `{"finding_ids": ["RUNNER_NOT_HELD"], "refused_rows": ["mutate-and-run-regression", "round21-measure-selftest"], …}` | 60.8 s |
| entry command, 2-row subset, lane inside a fleet with sibling symlinks | same, subset pair | **0** | `{"finding_ids": [], "refused_rows": [], "revision_pinned": 2, "rows": 2, …}`, four files written | 18.65 s |
| altered runner bytes (fixture clone, one appended comment line, committed) | same as above at the probe commit | **0** | bundle published, `runner_sha256_clone_copy = 3a411cc0…` | 19.3 s |
| self-test with one case expectation broken (fixture copy) | `--selftest` | **1** | `REGISTRY_REPLAY_SELFTEST: 9/10 pass` | 438 ms |
| missing `--requirements` path | `--run … --requirements <absent>` | **1** | traceback `FileNotFoundError` | 46 ms |
| registry baseline altered by one byte | `--run …` | **2** | stderr `registry-replay: frozen registry digest mismatch` | 47 ms |
| requirements altered (one `expect.exit`) | `--run …` | **2** | stderr `registry-replay: frozen requirements differ from source registry` | 43 ms |
| `--project` invalid / unreadable observations | `--project bad.json --out … --json` | **2** / **2** | `{"finding_ids": ["INVALID_OBSERVATIONS"]}` | 41/43 ms |
| `--plan` | `--plan --repo . --json` | **0** | plan JSON | 42 ms |

Row self-test output reproduced byte-exactly (`od -c` of last line: `REGISTRY_REPLAY_SELFTEST: 10/10 pass\n`); the marker is the first whitespace token of the last non-empty stdout line, so it satisfies the counter's finding-id rule.

## Field-by-field against source

**Kind `gate` — truthful.** The tool refuses rather than warns: with two rows not held, exit 1 and `bundle.json`/`expected.json`/`live-dependent.json` are withheld (`registry-replay.py:118-131`, `183`); the refused run's `--out` contained `observations.json` only.

**Exit map — complete for reachable codes.** Static enumeration: `SystemExit(64)` at `:50` (argparse error); `return 2` at `:77`, `:84`, `:95` (`INVALID_OBSERVATIONS`), `:141` (digest mismatch), `:146` (requirements drift), `:159` (clone HEAD mismatch), `:280` (`--project` unreadable/invalid JSON); `project()` returns 1 on findings (`:108`), 0 with a bundle (`:111`); `raise SystemExit(main())` at `:291` makes every other failure an uncaught traceback → 1, which the row states explicitly. All four declared codes were reproduced above; no fifth code is reachable.

- The row is *more* accurate than the tool's own docstring: `:27-28` says `2 invalid or unavailable input`, but an absent requirements file exits 1 via traceback (measured). The row covers that case with "an uncaught traceback also exits 1".
- M2 stands: `9/10 pass` exits 1 and the verdict map's parenthetical for 1 does not mention self-test case failure.

**Pinned values — M1.** `.ufo/evidence/round-23/requirements.json` and `.ufo/evidence/round-23/registry-baseline.json` are genuinely pinned against each other: baseline digest is checked at `:138-141`, semantic equality of the two frozen row sets at `:143-146`; both were broken deliberately and both produced exit 2. `tools/registry-check.py` is **not** pinned: its digest is computed from the clone copy at `:163` and only stored in `observations` at `:177` as `runner_sha256_clone_copy`; there is no expected value to compare (`requirements.json` keys are exactly `registry_sha256`, `requirements`, `schema`, `source_revision`; `registry-baseline.json` contains no `sha256` field at all — `grep -c sha256` = 0). Measured: a fixture lane whose `tools/registry-check.py` bytes differ (sha `3a411cc0…` vs `cba16646…` at CAND) still exits 0 and publishes. The cell's parenthetical discloses provenance, but listing the path under *Pinned values* overstates it — no verdict depends on its digest. Counter cannot see this (it only checks the path exists at REV).

Also worth recording as an inherited limit, not a lie: the frozen pair is never compared with the lane's live `tools/registry.json` at REV, so "0 clean" means "the caller's frozen 43-row bundle replays", not "the live registry has not drifted". The base-page row (`SKILL.md:2052`) says this openly ("frozen requirement/registry digests come from the caller's files"); the round-51 row does not.

**Write scope — accurate with one conditional.** Clean run writes exactly the four named files (subset run `--out`: `bundle.json`, `expected.json`, `live-dependent.json`, `observations.json`). M4: on exit 1 only `observations.json` exists. The private clone is `tempfile.TemporaryDirectory(prefix='tameshi-registry-replay-')` and is removed (a dedicated TMPDIR was empty after the self-test; after both `--run` attempts the only residue was kept by *other* tools' rows — `tameshi-r16-CRMeasure-*`, `tameshi-r17-MeasureV2-*`, and the runner's deliberately kept `tameshi-r4-2-regression.*`). The non-isolation sentence is true and slightly understated: `:161` symlinks the live siblings into the mirror **and** `:170` hands `run_row` the live `layout['fleet_root']`, so rows are told the live fleet root, not the mirror. That is why the seat did not execute the full panel against live siblings (see Bounds).

**Last-line marker — meaningful, computed.** Not help text: breaking one case in a scratch copy produced `CASE stream-at-limit FAIL` and `REGISTRY_REPLAY_SELFTEST: 9/10 pass` at exit 1; `passed` is compared to `total` at `:244-245`. The marker exists only on stdout and is the terminal line.

**Entry command / 0 reachability — M3.** From a clone whose parent holds no sibling lanes (my first context), the full panel exits 1: `mutate-and-run-regression` got 2 (`SETUP (repo_identity_mismatch: …/fleet/kumitate-shokunin is not its own repository)`) and `round21-measure-selftest` got 1 (traceback at `tools/round21-measure.py:74`, `git -C …/fleet/tameshi-shokunin show` exit 128 because the clone was named `cand`). Re-run with the checkout named `tameshi-shokunin` in a directory holding symlinks to the live sibling lanes, a 2-row subset held and exited 0 — so the 0 path is reachable, but only inside the fleet context the write-scope cell describes. The entry-command cell gives `--repo .` with no hint of that precondition; a reader who copies it from a bare clone gets exit 1 (which is at least honestly mapped).

## Bounds and risks

- Read-only on lane, fleet and sibling repos. All execution happened in `git clone --shared` fixtures under `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool14/`; the single fixture commit asserted `git rev-parse --show-toplevel` = the fixture clone before running. No git/jj mutation in the lane or fleet.
- The full 43-row panel was deliberately **not** re-run with live sibling symlinks: `mutate-and-run-regression` would then execute mutation cases against the sibling repos through the mirror and the live fleet root, which the seat's read-only bound forbids. That row's outcome at REV is C2's to measure, not this seat's.
- Therefore the row's `0 clean` for the *entire* frozen panel is not directly witnessed here; what is witnessed is (a) exit 0 with a published four-file bundle for a held subset in the documented fleet context, and (b) exit 1 with `RUNNER_NOT_HELD` outside it, exactly as declared.
- M1 is the only claim-level falsity; it is disclosed by the tool's docstring ("this tool authenticates no producer") but not by the row's cell, and C3's Pinned-values check cannot distinguish a pinned path from a merely read path.
- No shim, source edit or row edit was made; the row needs none for C3's counter to credit it.
- `/tmp` footprint: every probe ran under an explicit `TMPDIR` inside the seat scratch (now deleted). The only `/tmp` residue attributable to this seat's window is a 19-byte empty `tameshi-registry-check-*` directory, created by the audited runner's own hardcoded `mkdtemp` during `registry-check-selftest`; it was left in place because concurrent seats run the same fixture and attribution is ambiguous. Total: well under the 50 MB bound.
