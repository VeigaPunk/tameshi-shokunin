# X07MeasureV2 — round-17 measure.py (interface contract C)

## Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-17/measure.py` (new file)
  - sha256: `f654d5b660c27632e121d8959c58d0d23b2d2f5ce29db0e5e0eda45dda829997`

## Behavior

Ported `.ufo/evidence/round-16/measure.py` with `sectionize`, `shonen_boxes`,
`sources_census`, `entry_credit_reason` (v1 rule) byte-identical, plus:

- `LEDGER_PATH` and `BOX3_LINK` now `.ufo/evidence/round-17/coldread/ledger.json`.
- Input rule (R16-C2b) in `entry_input_reason()` (measure.py:209): fires only on
  entries with `commands_executed_count>0` that already pass the v1 credit rule.
  Requires non-empty `inputs` dict; each recorded input's blob is read via
  `git show <rev>:<path>` at the measured `--rev` and re-hashed. Reasons:
  `inputs-unrecorded`, `input-missing:<path>`, `input-drift:<path>`
  (multi-failure `;`-joined, sorted).
- `--ledger-file PATH` (local file), `--ledger-rev REV:PATH` (any pinned blob;
  split on first `:`; mutual exclusion + malformed -> exit 64; unreadable/missing
  -> exit 2 with typed JSON error).
- `--inputs-overlay FILE`: JSON list of `{start, heading, skill_sha256, read_rev,
  inputs, ...}` merged into matching entries by `(skill_sha256, start)`;
  merged count reported as `coldread.inputs_overlay_merged`; non-list/unreadable
  -> exit 2.
- Per-section `reason` output: `coldread.sections[]` =
  `{start, heading, credited, reason}` (`reason == 'credited'` on credit) and a
  `coldread.reasons` histogram over all sections. `missing[]` shape unchanged.
- `coldread.external_inputs`: merged `{path: sha}` map, reported only (never
  credited), per contract.
- Entries with `commands_executed_count<=0` (or absent/unparseable) keep v1
  rules untouched — no input requirement.

## Evidence

### Selftest

```
$ python3 .ufo/evidence/round-17/measure.py --selftest
... (all PASS)
MEASURE_SELFTEST: 58/58 pass (scratch /tmp/tameshi-r17-MeasureV2-4niyah5f)
```

exit 0. 58/58 covers: all ported v1 cases (no-ledger 6, full ledger 8, missing
entry 6, gap-blocking 6, byte-changed 6, bad verdict, zero-commands instruction,
instr+verified-record, record+verified-record, unknown class, record+executed-ok,
trailing-whitespace strip, box3 nolink/continuation-link/wrong-box, exits
0/2/64/2-no-repo) plus new: `record-zero-cmd-credited` (8),
`unrecorded-{score,reasons}` (`inputs-unrecorded`×4), `input-missing-*`,
`redbefore-drift-*` (input file rewritten at later rev -> `input-drift`×4,
box3 false, score 6; same ledger at pre-drift rev credits 8),
`ledger-rev-drift-6` (cross-rev: input check keys on `--rev`),
`overlay-merge-credits` (merged=4, ghost item ignored), `overlay-stale-drift`,
`ledger-file-*`, and flag-validation exits (64 both flags, 64 malformed
ledger-rev, 2 missing ledger blob/file/overlay, 2 non-list overlay).

### Acceptance command on lane tip

```
$ python3 .ufo/evidence/round-17/measure.py --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f \
    --ledger-rev 98bea7da5801f4bc58e4187690ee1687c8a5061f:.ufo/evidence/round-16/coldread/ledger.json
exit=0
sections covered/total: 0/54
box3_full_page: false
box3_ledger_link: false   (tip SHONEN box-3 points at round-16 ledger path)
calibration_restraint_score: 6
reasons histogram: {"inputs-unrecorded": 54}
```

All 54 sections have sha-matched ledger entries (round-16 full-page coverage was
real), but every entry has `commands_executed_count>0` and a v1 ledger carries no
`inputs` field, so the input rule uncredits all — the exact red-before the
claim fixes. `--inputs-overlay` or a v2 ledger restores credit.

## Retained evidence

- Selftest scratch: `/tmp/tameshi-r17-MeasureV2-4niyah5f` (synthetic repo, all
  commits + overlay fixtures).
- Tip output: `/tmp/m17-tip.json` on this host.
- File sha256: `f654d5b660c27632e121d8959c58d0d23b2d2f5ce29db0e5e0eda45dda829997`.

## Risks / notes

- Overlay items merge by `entry.update(item)` — an overlay item's keys
  overwrite same-named entry fields. Contract lists `{start, heading,
  skill_sha256, read_rev, inputs}`; `start`/`heading`/`skill_sha256` are
  identical by key match, so only `read_rev`/`inputs` (and extra keys) change.
  A hostile overlay could overwrite `verdict`/`sha256` — accepted per contract
  (overlay is a trusted seat-supplied input for legacy grading).
- `input-drift`/`input-missing` reasons are computed at the measured `--rev`
  (not `read_rev`), matching the contract's "at the measured rev" wording.
- Box-3 link check requires the literal round-17 ledger path inside the box-3
  block; tip still links the round-16 path -> `box3_ledger_link` false until
  SHONEN is appended by the L1.
- No tool installs needed (python3/git stdlib only).

## Verdict

built

## Follow-up — hardening per K02 (holes 1–7), R05 (F1–F10), K06, plus L1 addenda

### File

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-17/measure.py`
  - new sha256: `f348adc3d88a7adf98451b366bf7fdef1bafefc94df992961f2595c85a328c89`
  - 1499 lines, stdlib only. `sectionize`/`shonen_boxes`/`sources_census` untouched.

### What changed (mapped to the mandate)

| # | mandate | implementation |
|---|---|---|
| 1 | class-independent input gate on EVERY entry | `input_reason()` runs after the class gate for all classes. `record/verified-record/0 commands` now needs one verified input; `{}` → `inputs-unrecorded`. |
| 2 | fail-closed aggregation with veto | `coldread()` collects per-entry reasons; a section is covered only when `credited>0` and no veto-eligible entry exists. Veto-eligible = bad/unknown verdict, `gap-blocking`, `wrong-expectation`, `not-executed`, `blocking_gaps>0`, `wrong_expectations>0`; **exempt** when ≥1 of its inputs fails at REV (stale failure). Clean entry never launders a failing twin. Per-section `vetoed` flag. |
| 3 | `ls-tree` mode + `cat-file blob` + canonical keys | `ls_tree_mode()` requires exactly one entry, mode `100644/100755`; tree/symlink/gitlink → `input-not-blob:<p>`; absent → `input-missing:<p>`; bytes only via `cat_file_blob` (`git show` never used for inputs). `canonical_lane_path()` rejects `''`, leading `/`, leading `./`, empty/`.`/`..`/`.git` components, NUL, non-UTF-8 → `input-not-blob:<p>`. |
| 4 | ignore `SKILL.md` and the round-17 ledger path | `IGNORED_INPUTS`; dropped before the non-empty check and before verification, in both entry inputs and trace inputs. `{SKILL.md: …}` alone → `inputs-unrecorded` (K02 hole 7). |
| 5 | trace binding | `trace_reason()`: with `commands_executed_count>0`, `traces` must be a non-empty list of paths that resolve at REV as blobs; each must parse as `tameshi-trace-inputs-v1` (`trace-invalid:<p>`), its `inputs` ⊆ entry inputs with equal sha (`trace-input-unrecorded:<p>`), and its `external` must not name any path under the live lane root (`live-lane-read:<p>`). Missing/blobless → `trace-missing:<p>`. |
| 6 | overlay whitelist + `overrides_used` | Allowed item keys: `start`, `skill_sha256`, `heading`, `inputs`, `read_rev`, `traces` (matching/identity keys must be allowed or the X10 fixture itself would be rejected); any other key → exit 2 `overlay-field-forbidden`; wrong type on `inputs`/`traces` → exit 2 `overlay-field-invalid`. Outputs `overrides_used`. |
| 7 | GIT_* scrub, resolved revision | `GIT_ENV` drops every `GIT_*` at import; every `git()` call uses it. `--rev` and the REV part of `--ledger-rev` are rejected when option-like (64) and resolved with `rev-parse --verify --quiet --end-of-options X^{commit}` (2 when unresolvable); all reads and `revision` use the resolved 40-hex sha; raw argument echoed as `rev_input`. |
| 8 | selftest per item | 89/89 checks, below. |

R05 F8 add-ons (cheap, reported): `ledger_source` (`rev`|`file`), `ledger_committed` (bytes identical to the REV ledger blob), `trace_gate` (`strict`|`legacy`).

Addendum 1: selftest fixture git runs with a `GIT_*`-free env (identity via repo-local
config, `HOME` in the sandbox).

Addendum 2: `--repo` defaults to the git toplevel containing the script
(`default_repo(__file__)`), so a clone measures itself.

### Design boundary (explicit, please review)

L1 asks both for a hard trace gate on `commands_executed_count>0` and for the
legacy r14 overlay to *credit* at e69b488. Those are jointly unsatisfiable for a
v1 ledger entry: its `traces` key is absent, and no round-17 receipt can exist as
a blob at a round-14 rev. Resolution: trace binding is enforced **strictly when
no override flag is given** (the cited-number path), and declared traces are
still fully validated when overrides are used; with overrides and no traces the
run is explicitly a measurement aid (`overrides_used: true`,
`trace_gate: "legacy"`), matching K06 condition 7 (the 8 may never use
`--ledger-file`/`--ledger-rev`/`--inputs-overlay`). The strict gate is proven
satisfiable (falsifier E); the legacy mode is what lets the red-before credit at
its read rev.

### Selftest

```
$ python3 .ufo/evidence/round-17/measure.py --selftest
MEASURE_SELFTEST: 89/89 pass (scratch /tmp/tameshi-r17-MeasureV2-ehqfip96)
```

exit 0. Ported v1 cases plus: `record-zero-cmd-input-credited` and
`record-zero-cmd-no-input-uncredited` (replaces the old free-credit case);
`bool-count-malformed`; `input-not-blob-dir` / `input-not-blob-symlink`;
five `noncanonical-*` keys; `skill-only-unrecorded`, `ledger-only-unrecorded`,
`skill-plus-file-credited`; `traces-unrecorded`, `trace-missing`,
`trace-invalid`, `trace-input-unrecorded`, `live-lane-read`;
`dupe-veto-clean-first`, `dupe-veto-fail-first`, `dupe-stale-no-veto`,
`dupe-live-veto`; `overlay-redbefore-credits-at-read-rev` (overlay with the X10
shape, merged=4, ghost ignored) and `overlay-redbefore-drift`;
`overlay-field-forbidden`; `overlay-traces-allowed`;
`ledger-file-drift`, `ledger-rev-committed`, `ledger-rev-cross-rev-drift`;
`revision-40hex` (HEAD → resolved sha), `git-env-scrubbed` (poisoned
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`), `default-repo-is-script-toplevel`
(copy run without `--repo`); all exit-code cases incl. option-like `--rev` and
`--ledger-rev` (64).

### Acceptance runs (live lane, exact command)

```
$ python3 .ufo/evidence/round-17/measure.py --rev <R> \
    --ledger-rev 98bea7da…:.ufo/evidence/round-16/coldread/ledger.json \
    --inputs-overlay .ufo/evidence/round-17/redbefore/legacy-r14-inputs.json
exit=0 for each R
```

| rev | r14 bucket (`start 1563`) reason | covered/total | box3 | score | overrides / gate | output |
|---|---|---|---|---|---|---|
| `98bea7da5801f4bc58e4187690ee1687c8a5061f` | `input-drift:tools/mutate-and-run.sh` | 0/54 | false | 6 | true / legacy | `.ufo/evidence/round-17/redbefore/measure-98bea7d.json` |
| `e69b488f65b17bcfd41949abf7d538a77678dc26` | **`credited`** | 1/51 | false | 6 | true / legacy | `.ufo/evidence/round-17/redbefore/measure-e69b488.json` |
| `09ee1d099190918ec388019bb79afbb6b93f1ff2` | `input-drift:tools/mutate-and-run.sh` | 0/54 | false | 6 | true / legacy | `.ufo/evidence/round-17/redbefore/measure-09ee1d0.json` |

Exactly the expected progression. `inputs_overlay_merged=1` at each rev; tip
reasons `{input-drift:tools/mutate-and-run.sh: 1, inputs-unrecorded: 53}`;
e69b488 `{credited: 1, inputs-unrecorded: 43, verdict:gap-blocking: 1,
verdict:wrong-expectation: 5, wrong-expectations: 1}` (fail-closed vetoes at
that page); 09ee1d0 identical to tip. `ledger_committed=false` at all three
(the ledger is pinned at the later tip rev, which the override reports).

Strict no-override run at tip (round-17 ledger absent at that rev):

```
$ python3 .ufo/evidence/round-17/measure.py --rev 98bea7da…
exit=0  covered=0/54  reasons={"no-ledger": 54}  trace_gate=strict
revision=98bea7da5801f4bc58e4187690ee1687c8a5061f
```

saved as `.ufo/evidence/round-17/redbefore/measure-98bea7d-strict.json`.

### Hardening falsifiers on real lane bytes (K02 holes 1–4, R05 F1)

Fleet-mirror clone at the tip in `/tmp/tameshi-r17w1-X07MeasureV2-vHFbJk` (all
git writes confined there), crafted ledger committed, live measure run with
`--repo <clone> --rev HEAD` (strict, no overrides), section `start 1563`:

| variant | crafted entry | observed reason | hole closed |
|---|---|---|---|
| A | subset input (`dispositions.json`), no `traces` | `traces-unrecorded` | K02 hole 1 / R05 F4 |
| B | `record/verified-record/0 cmds/inputs {}` | `inputs-unrecorded` | K02 hole 2 / R05 F2 |
| C | `inputs {"tools": …}` | `input-not-blob:tools` | K02 hole 4 / R05 F3 |
| D | clean entry + `gap-blocking` entry, same sha | `verdict:gap-blocking`, covered 0 | R05 F1 |
| E | valid input + valid in-rev trace | `credited`, covered 1/54 | gate satisfiable |

### Residual risks

- The class label stays seat-declared. A seat can label an executed bucket
  `record` and credit `verified-record` with one verified input plus one trace;
  execution itself is not provable from the ledger (same residual R05 §2 names).
- `--rev HEAD`/branch names remain symbolic by nature: the resolved sha is what
  is measured, but a moving ref between invocations changes the answer; the
  claim should pass 40-hex revs (K06 condition 1).
- Overrides make a run a measurement aid; `ledger_committed`/`overrides_used`
  are the guardrails. The cited 8 must come from the strict, no-override form.
- Trace `external` rejection compares realpaths against the live lane; a trace
  rooted *inside* the live lane (root, not external) is not rejected by
  requirement 5 as written.
- No tool installs (python3/git only).

Verdict: built (hardened; acceptance progression reproduced).

## Follow-up 2 — wave-2 fixes (ReviewMeasureV2Code, MutateMeasureV2, LessonReview F1)

### File

- `.ufo/evidence/round-17/measure.py`
  - new sha256: `1cac0db8755dd4cf6626cf14edc42ad67cda08d8a5bbe40ea8604d83828e87a5`
  - 1550 lines; `python3 -c "import ast"` parses clean.

### Fixes (mapped)

| # | mandate | implementation |
|---|---|---|
| 1 | `live_lane_reads` receipt field must uncredit | `trace_reason` returns `live-lane-read:<p>` for any non-empty `live_lane_reads` map (sorted first key), plus the existing `external` check. Selftest fixture `TRACE_LIVE_PATH` now emits the real producer shape (`live_lane_reads`, matching `trace-inputs.py:683-684`); `TRACE_EXT_PATH` keeps the external shape and `live-lane-read-external` still proves the external arm. |
| 2 | commands gate, class-independent (K02 hole 2 / LessonReview F1) | `entry_reason` returns `commands-unrecorded` for `commands_executed_count == 0` (every class; a zero-command record can no longer credit), after the class gate and before the input gate. Traces-committed still required only in strict mode, preserving the legacy red-before. |
| 3 | kill the two mutation survivors | M4: trace receipt key present but digest differs → new `trace-input-drift:<path>` (`entry['inputs'][key] != receipt['inputs'][key]`); selftest `trace-input-drift` (receipt `drift.json` pins `INPUT_V2_SHA`). M6: overlay item containing only `verdict` → exit 2 `overlay-field-forbidden`; selftest `overlay-verdict-only-forbidden`. |
| 4 | docstring | sources regex `[0-3]` → `[0-9]`; exits summary now says missing default ledger is a measured `no-ledger` (exit 0), exit 2 only for rev/required-blob missing, explicit `--ledger-file`/`--ledger-rev` unreadable, or overlay unreadable/forbidden-field. |

### Selftest

```
$ python3 .ufo/evidence/round-17/measure.py --selftest
MEASURE_SELFTEST: 93/93 pass (scratch /tmp/tameshi-r17-MeasureV2-bduz1uv3)
```

exit 0. New/changed checks: `record-zero-cmd-commands-unrecorded` (was
`record-zero-cmd-input-credited`, now expects `commands-unrecorded` ×4 and
0 covered), `record-zero-cmd-no-input-uncredited` (also `commands-unrecorded`),
`record-with-commands-credited` (record + verified-record + commands>0 + valid
trace + valid input → 4/4, 8), `trace-input-drift`, `live-lane-read` (real
producer shape), `live-lane-read-external`, `overlay-verdict-only-forbidden`.

### Red-before rerun (L1's exact commands)

```
$ for r in 98bea7d e69b488 09ee1d0: measure.py --rev <R> --ledger-rev 98bea7d:…round-16/ledger.json --inputs-overlay …/legacy-r14-inputs.json
exit=0 each
diff -q vs committed .ufo/evidence/round-17/redbefore/measure-*.json
IDENTICAL 98bea7d / e69b488 / 09ee1d0 / strict
```

Byte-identical outputs — no field I changed affects these runs (the r14 entry
has commands>0 so it passes the new commands gate; no receipt carries
`live_lane_reads`). The r14 bucket still reads `credited` at `e69b488` and
`input-drift:tools/mutate-and-run.sh` at `09ee1d0`/tip.

Verdict: built (wave-2 hardening applied; K02 hole 2 closed, live-lane-read reachable via producer receipts).
