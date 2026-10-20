# MutateMeasureV2 — round 17, wave 2

## Scope and axes

Seat: `TameshiR17.MutateMeasureV2-2`. Frozen target: `eb7838b16490ca7ba17ea3242ade76a61f744af2`.

Axes: **depth** (behavioral specificity of verification fixtures) and **calibration** (whether self-test green actually distinguishes the named bad behavior, with exact-byte restoration).

Attacked only `.ufo/evidence/round-17/measure.py` using eight independent, one-line mutants. Result: **6 killed, 2 survived, 0 inconclusive**. Every pristine and restored detector run exited 0 with `MEASURE_SELFTEST: 89/89 pass`. Survivors are coverage findings, not permission to weaken the contract or claims that the pristine implementation is defective. This seat does not judge C1, C2, or the round.

## Isolation and commands

Eight independent fleet-mirror clones were prepared, each detached at the frozen target; all preparation commands exited 0. Preparation repeated the required recipe:

```sh
W=$(mktemp -d /tmp/tameshi-r17w2-MutateMeasureV2-XXXXXX)
mkdir "$W/fleet"
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" "$W/fleet/"
done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$W/fleet/tameshi-shokunin"
git -C "$W/fleet/tameshi-shokunin" checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
```

Actual clone roots (`C`) and mutation assignments:

| ID | C |
|---|---|
| M1 | `/tmp/tameshi-r17w2-MutateMeasureV2-3g3zMm/fleet/tameshi-shokunin` |
| M2 | `/tmp/tameshi-r17w2-MutateMeasureV2-XCK6CW/fleet/tameshi-shokunin` |
| M3 | `/tmp/tameshi-r17w2-MutateMeasureV2-09ZqhA/fleet/tameshi-shokunin` |
| M4 | `/tmp/tameshi-r17w2-MutateMeasureV2-Pu1Pih/fleet/tameshi-shokunin` |
| M5 | `/tmp/tameshi-r17w2-MutateMeasureV2-vaujRx/fleet/tameshi-shokunin` |
| M6 | `/tmp/tameshi-r17w2-MutateMeasureV2-OsTdHn/fleet/tameshi-shokunin` |
| M7 | `/tmp/tameshi-r17w2-MutateMeasureV2-T1snz5/fleet/tameshi-shokunin` |
| M8 | `/tmp/tameshi-r17w2-MutateMeasureV2-fb3dXY/fleet/tameshi-shokunin` |

For each ID, from its own `C`, the executed outer command was:

```sh
python3 /tmp/tameshi-r17w2-MutateMeasureV2-3g3zMm/probe.py ID PHASE C
```

`PHASE` was `pristine`, then `mutated`, then `restored`. Independent IDs ran concurrently within each phase; no phase overlapped editing or restoration. The recorder executed the same detector argv in all 24 runs, bounded to 60 seconds, with `cwd=C`:

```sh
python3 "$C/.ufo/evidence/round-17/measure.py" --selftest
```

It ran `sha256sum "$C/.ufo/evidence/round-17/measure.py"` immediately before and after each detector and preserved its exit, stdout, stderr, and both hashes under `/tmp/tameshi-r17w2-MutateMeasureV2-3g3zMm/results/ID/PHASE.json`. Those scratch receipts are supplementary; reproducible mutations, command, hashes, exits and key output are embedded below. No detector timed out, and all detector stderr was empty. No test, production implementation, registry, ledger, or sibling source was changed permanently. No GIT_* variables were exported; M8 exercised the self-test's existing subprocess-only `/nonexistent` environment injection.

## Exact mutants and expected detectors

All path:line references below resolve in `.ufo/evidence/round-17/measure.py` at the frozen target. Each row replaces exactly the indicated line, preserving indentation and all other bytes. Fixtures were never edited.

| ID | Behavior-bearing path:line | Original line → replacement | Expected detector / fixture location |
|---|---|---|---|
| M1 | `measure.py:474` | `reason = input_reason(repo, rev, entry)` → `reason = input_reason(repo, rev, entry) if entry.get('commands_executed_count') else None` | `record-zero-cmd-no-input-uncredited`, lines 1008–1017: a zero-command record still needs inputs. |
| M2 | `measure.py:582` | `covered = credited > 0 and not vetoes` → `covered = credited > 0` | `dupe-veto-clean-first`, `dupe-veto-fail-first`, `dupe-live-veto`, lines 1166–1190: a clean duplicate cannot launder a current failing entry. |
| M3 | `measure.py:329` | `if mode not in BLOB_MODES:` → `if mode not in BLOB_MODES and mode != '120000':` | `input-not-blob-symlink`, lines 1091–1097: ls-tree mode 120000 must not pass the ordinary-file mode guard. Only the symlink branch was mutated, not directory/gitlink handling. |
| M4 | `measure.py:402` | `if key not in view or view[key] != rec_inputs[key]:` → `if key not in view:` | Trace binding must reject a shared input key whose receipt digest differs. Existing `trace-input-unrecorded` fixture, lines 1150–1156, exercises only an extra key. |
| M5 | `measure.py:358` | `return real == root or real.startswith(root + os.sep)` → `return real == root` | `live-lane-read`, lines 1158–1164: a descendant such as live-lane `SKILL.md` must be rejected, not only the root itself. |
| M6 | `measure.py:128` | `'read_rev', 'traces'))` → `'read_rev', 'traces', 'verdict'))` | `overlay-field-forbidden`, lines 1256–1264: allowing a verdict override should be distinguished from the whitelist. Existing fixture injects both `verdict` and `wrong_expectations`. |
| M7 | `measure.py:125` | `IGNORED_INPUTS = frozenset(('SKILL.md', DEFAULT_LEDGER_PATH))` → `IGNORED_INPUTS = frozenset()` | `skill-only-unrecorded`, `ledger-only-unrecorded`, `skill-plus-file-credited`, lines 1111–1124: self-referential input exemptions must be applied. |
| M8 | `measure.py:133` | `GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}` → `GIT_ENV = dict(os.environ)` | `git-env-scrubbed`, lines 1282–1288: inherited GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE must not redirect Git reads. |

## Kill table — actual detector results

`exit / passed` below is the detector process exit followed by its printed `MEASURE_SELFTEST` tally. Every pristine and restored run printed the relevant witness checks as `PASS`.

| ID | Pristine | Mutated | Restored | Verdict |
|---|---|---|---|---|
| M1 | 0 / 89/89 | 1 / 88/89 | 0 / 89/89 | killed |
| M2 | 0 / 89/89 | 1 / 86/89 | 0 / 89/89 | killed |
| M3 | 0 / 89/89 | 1 / 88/89 | 0 / 89/89 | killed |
| M4 | 0 / 89/89 | 0 / 89/89 | 0 / 89/89 | **survived** |
| M5 | 0 / 89/89 | 1 / 88/89 | 0 / 89/89 | killed |
| M6 | 0 / 89/89 | 0 / 89/89 | 0 / 89/89 | **survived** |
| M7 | 0 / 89/89 | 1 / 86/89 | 0 / 89/89 | killed |
| M8 | 0 / 89/89 | 1 / 88/89 | 0 / 89/89 | killed |

The complete set of mutated-run `FAIL` lines, grouped by ID:

```text
M1: FAIL record-zero-cmd-no-input-uncredited
M2: FAIL dupe-veto-clean-first
M2: FAIL dupe-veto-fail-first
M2: FAIL dupe-live-veto
M3: FAIL input-not-blob-symlink
M5: FAIL live-lane-read
M7: FAIL skill-only-unrecorded
M7: FAIL ledger-only-unrecorded
M7: FAIL skill-plus-file-credited
M8: FAIL git-env-scrubbed
```

### Survivor M4 — trace key membership does not prove digest binding

Actual mutated output included `PASS trace-input-unrecorded` and `MEASURE_SELFTEST: 89/89 pass` (exit 0), despite deletion of the digest-equality arm at `.ufo/evidence/round-17/measure.py:402`.

The current negative fixture at `.ufo/evidence/round-17/measure.py:1150-1156` points to `TRACE_EXTRA_PATH`, whose receipt adds `corpus/SOURCES.md` (`measure.py:873-874`). Its missing key is still rejected by the mutant. Thus this detector does not distinguish loss of equal-digest binding for an already-recorded key. [INFERENCE] A receipt with the same input key but a different recorded digest would expose the removed arm; no separate custom scenario was run. This is a fixture-coverage finding, not a demonstrated defect in pristine measurement.

### Survivor M6 — a combined forbidden-fields fixture masks one allowed field

Actual pristine/restored `PASS overlay-field-forbidden` detail listed both forbidden fields:

```json
{"error":"overlay-field-forbidden","fields":["verdict","wrong_expectations"]}
```

Actual mutated `PASS overlay-field-forbidden` detail listed only:

```json
{"error":"overlay-field-forbidden","fields":["wrong_expectations"]}
```

These blocks select the actual `error` and `fields` values from the printed JSON; its temporary `path` field is omitted. The mutated detector still ended `MEASURE_SELFTEST: 89/89 pass`, exit 0. The fixture injects two forbidden fields together (`.ufo/evidence/round-17/measure.py:1257`), but its assertion checks only exit 2 and the error identifier (`measure.py:1263-1264`). Consequently `wrong_expectations` preserves the rejection after `verdict` was wrongly added to `OVERLAY_FIELDS`. [INFERENCE] An overlay containing `verdict` alone would exercise the escaped whitelist restriction; that separate scenario was not run. Contract unchanged; no implementation or fixture fix made here.

## Before/after hashes and restoration

Common pristine SHA-256 (`H0`):

```text
f348adc3d88a7adf98451b366bf7fdef1bafefc94df992961f2595c85a328c89
```

For every phase below, the before-detector hash equaled the after-detector hash. Each restored file returned to H0 by reversing its exact one-line change; its restored self-test also returned to 89/89. No Git reset/checkout was used to restore a live tree.

| ID | Pristine before=after | Mutated before=after SHA-256 | Restored before=after |
|---|---|---|---|
| M1 | H0 | `accfb7530b26d76d86b126b58b6dc7024cbde971b6f297b172c97c76d24ccb94` | H0 |
| M2 | H0 | `82eca24b09b533d121c750b5d61c172a2de60f23768fb90536c6b623079210fb` | H0 |
| M3 | H0 | `838070a79e45be40f27e3dd3a1bf927bb62182cf4f2352d35e4f7002d1e8f435` | H0 |
| M4 | H0 | `dc36431e49990effc4a2d2625fb14d52685a44523d0c2c96539973719099d9a9` | H0 |
| M5 | H0 | `327aa206997513a513041a894d97890c2358ededdfdac99945b69bef7bdea30a` | H0 |
| M6 | H0 | `afd692f62968c4449f850a819c4eb59198af41351df8ed07f74c37360f106777` | H0 |
| M7 | H0 | `d4bc3e15420fc1cb976ea4dc99165d763b07ca99abb5fd38e0b4bdc2f584e978` | H0 |
| M8 | H0 | `b8d3669231b73849a121958f0886a57b5c80bb3437e4d7df727314139b7e353a` | H0 |

## Scope note and limitations

The detector's built-in `tempfile.mkdtemp(prefix='tameshi-r17-MeasureV2-')` created its usual 24 fixture directories directly under `/tmp`, rather than beneath the assigned outer scratch prefix. This was a scratch-path conformance deviation: TMPDIR was not redirected. All 24 exact directories named in the captured summaries were subsequently removed with a single explicit-path `rm -rf -- ...` command, exit 0; unrelated fixture directories were not targeted. Mutation clones and recorder receipts remain under the assigned outer prefix. Nothing was executed against the live lane root; its only write was this report. Tools installed/updated: none. No subagents, background jobs, omp CLI, jj, REA, live-lane Git writes, or sibling writes were used.

No full-page cold-read score or registry baseline was executed by this seat, and no claim beyond these eight specific mutation probes is made.

Verdict: **partial** — six named defenses are distinguished by `--selftest`; trace same-key digest binding and verdict-only overlay whitelist weakening survive, with all eight mutated files exactly restored.
