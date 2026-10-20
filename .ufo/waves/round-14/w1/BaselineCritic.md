# BaselineCritic — round 14 w1

Seat: TameshiR14.BaselineCritic (critic, leaf). Target: the self-derived expected values and digest baseline, plus the race on mutable inputs, behind C1 (effective expectation reconciliation).
Method: static reads of the round-13 bytes and git history at baseline `d6809df7775338f000e44c8a916067b8866867fb`. In-memory parsing and SHA-256 only. No receipt argv was executed, and no gate, selftest, runner, build or lint was run.
State at review time: `tools/evidence-disposition.py`, `dispositions-before.json`, `dispositions.json` and `capture-context.py` **do not exist yet**. This report reviews only the retained contract and the inputs it will consume. It makes no claim about completed code.
Tool installs/updates: none.

## Observed facts (static)

| Fact | Observation |
|---|---|
| `expected_checks` rows | **12** (not 13). 13 = `expected.inputs` count = `verification.json` check count |
| Receipt checks | verification.json 13 + producer-oracle-repair.json 2. Names unique across both. Every expectation has a same-named check |
| Receipt checks with no expectation | `pin_env_scrub`, `metadata_emit`, `frozen_and_guardrail_unchanged` |
| Commit provenance | expected.json, verification.json, producer-oracle-repair.json, verification-verdict.json and producer-oracle.py are all **added in one commit** `4acc607` (02:02:45-03:00 = 05:02:45Z). Runs started 04:59:26Z (verification) and 05:00:00Z (oracle) |
| Expected vs measured inputs | `expected.inputs` = 13. `verification.json.measured_input_sha256` = 12. The extra key is exactly `.ufo/evidence/round-13/producer-oracle.py`. The 12 shared values are equal |
| Worktree vs baseline | Every one of the 13 `expected.inputs` paths: worktree sha256 == recorded value == `git show d6809df:path` sha256 |
| Receipt digests (worktree == d6809df blob) | expected.json `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336`; verification.json `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f`; producer-oracle-repair.json `df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d` |
| Receipts covered by expected.inputs | **Neither** verification.json nor producer-oracle-repair.json |
| producer_before raw | exit1 matches. The contains string is absent from stdout (34 ok lines) **and** from stderr (FileNotFoundError traceback for `.ufo/evidence/tools/mutate-and-run.sh`). The before-file mismatch is robust to the stream choice |
| All other 11 rows, same-name binding | Every predicate passes against stdout. No contains literal appears in stderr. Receipt `expected_exit` equals the expected.json exit in all 12 |
| pin_live structure | 6 legs; `counts` field = 3/3/0. Counting `legs[].content_status` gives `{changed:3, unchanged:3}`, with **no `unavailable` key**. Top-level and per-leg `result_reuse` = not_established |

## Counterexamples

### CX1 — Identity substitution passes every predicate (fixable defect, calibration axis)
I evaluated every expectation against every receipt check:
- `pin_live` is satisfied by `pin_live` **and** `pin_env_scrub`. Their stdout is byte-identical, including `observed_at`.
- `producer_after` and `producer_after_oracle` each accept both checks.
- `producer_before` (original expectation) is satisfied by `producer_before_oracle`.
- `source_census` (`{exit:0}` only) is satisfied by 12 different checks.

Uniqueness alone allows two mislabelled bindings:
- `pin_live → pin_env_scrub`, because that check is otherwise unused.
- A swap of producer_after and producer_after_oracle.

Either is a false provenance claim: an "effective" row would cite a different run than its name. The gate would still exit 0.
**Smallest correction:** for effective rows, enforce `row.check == row.name`, or emit a stable `identity_substitution` finding with exit1. Superseded `producer_before` must also carry `check == "producer_before"` against verification.json.

### CX2 — The expectation baseline is post-observation, not preregistered (tradeoff; bound the claim)
expected.json was committed together with the receipts it judges, after both run windows. It also lists the oracle digest, which verification.json's measured set lacks. So at least the oracle rows and that input were added or edited after the initial crash was observed. The two oracle `contains` strings are literal fragments of observed output.

The gate therefore proves **consistency of the receipts with lane-authored expectations as committed at 4acc607 and unchanged at d6809df**. It does not prove:
- an independent prediction,
- that the expectations were frozen before observation,
- that any run produced those bytes.

`source_census` is exit-only, and no expectation binds argv. A pass on those rows proves only that a recorded exit code matched.
**Smallest correction:** use this wording in the dispositions reason fields, the report and the lesson. Never call expected.json a frozen preregistration. Do not edit expected.json. Superseding producer_before is reconciliation, not new red/green evidence.

### CX3 — The digest pin is self-derived (tradeoff; bound the claim)
`dispositions.inputs` is written by round-14 DispositionSpec from the current worktree bytes. The receipts are not covered by any round-13 `expected.inputs` pin. A receipt edited before DispositionSpec hashed it would therefore be pinned at its edited value, and the gate would pass.

The digest check only establishes that bytes did not change between authoring the disposition and running the gate. Configured authority = committed lane blobs at `d6809df` (authored in `4acc607`). The hyaku closure read these files but did not authenticate them (lesson §C1/§C2: "evidence-verified, not rerun"; "configured manifest authority is not adversarial baseline authentication"). There is no signature and no independent producer.
**Smallest correction:** do not add git to the stdlib gate interface. L1 compares the pins to the baseline outside the gate (see checks 2–3). The claim text says "matches lane-committed baseline d6809df", never "authentic" or "independently verified".

### CX4 — Race on mutable inputs between hashing and parsing (fixable defect)
Suppose the gate verifies a digest with one `open()` and then reopens the file to `json.load` it. A concurrent writer, a symlink swap, or another seat could then make the parsed bytes differ from the hashed bytes. Hashing `expected.inputs` targets such as `tools/*.py` and then rereading them has the same window.

**Proposed parsing from cached bytes** (gate implementation):
1. Have one `load(rel)` function and nothing else:
   - Reject absolute paths, `..`, backslashes, empty segments, and `os.path.normpath(rel) != rel`.
   - `os.lstat` every component under `--root` and refuse symlinks.
   - Read the whole file once into `cache[rel]: bytes`.
2. Compute every digest on `cache[rel]`. That includes the dispositions inputs, the original `expected.inputs`, and the receipts.
3. Parse JSON from the same cached bytes with `json.loads(b.decode('utf-8'), object_pairs_hook=reject_duplicates, parse_constant=reject)`. This catches duplicate `inputs`/`rows`/`checks` keys, where Python's default keeps the last value.
4. Exit 2 if a receipt contains duplicate check names.
5. Verify all digests before any predicate runs. On any mismatch, exit 2 and emit no pass/fail predicate results.
6. Parse structured predicates (`id`, `reason`, `rows`, `statuses`, `result_reuse`) from `json.loads(check["stdout"])` in memory. Match `contains` against `stdout` only. Recompute exit equality from expected.json. Treat the receipt's `exit_matches`/`expected_exit` as cross-check findings only, never as authority.
7. pin_live statuses: compute a full `{unchanged, changed, unavailable}` map from `legs[]`, with missing = 0. Cross-check it against the `counts` field and against `len(legs)` == `counts.legs` == 6. Disagreement between the two is its own finding.

The selftest cannot deterministically exercise the timing window. Its structural proxy is a single read site, which L1 inspects (check 5).

### CX5 — Race in ReceiptHarness between the baseline and injected runs (fixable defect)
The two pin-probe runs are separate in time and read sibling repos live. A sibling commit landing between them would show up in the comparison as a GIT_DIR effect.

For context: pin-disposition.py scrubs inherited `GIT_*` (lines 197–210). The expected result is therefore an inert injection. The receipt tests that scrub, bounded to `GIT_DIR` only.

**Smallest correction:** the harness records sibling HEAD and index identity before and after **both** runs, as verification.json already did with `sibling_indexes_before/after`. If anything moved, it marks the comparison `inconclusive` instead of equal or different. For the baseline run, it removes ambient `GIT_*` and records only the removed **names**. That keeps "baseline" from meaning "whatever L1's shell had".

### CX6 — Count authority conflict in the contract (fixable)
The goal text says "All13 expected rows". The data has 12 `expected_checks`. A gate or spec that asserts 13 will either fail or invent a row. Any number derived from `verification.json` checks (13) would wrongly pull in the three receipt-only checks.
**Correction:** enumerate `expected_checks` and assert 12 rows: 11 effective, plus producer_before superseded in after and effective in before. Gate and DispositionSpec were messaged directly with CX1/CX4/CX6 and with CX1/CX2/CX6 respectively.

## Impacted axes
- **calibration (C1):** CX1, CX2, CX3 and CX6 decide whether the claim is honestly bounded. CX4 decides whether the exit2 tamper semantics are real.
- **depth:** none affected.
- **freshness:** CX5 only. It is not a sweep, and nothing is preclaimed.
- **No harm** to the round-13 historical bytes: all 13 inputs and 3 receipts are byte-equal to d6809df.

## Checks L1 should run (after all seats finish)
1. `python3 tools/evidence-disposition.py --selftest`. The isolated fixtures should include: a substitution fixture (pin_live→pin_env_scrub must exit 1), a duplicate-JSON-key fixture (must exit 2), a non-normalized/`..` path fixture (exit 2), and a tampered-receipt fixture (exit 2 with no predicate pass emitted).
2. `git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-12 .ufo/evidence/round-13 tools/pin-disposition.py tools/witness-metadata.py tools/bash-witness-study.py tools/mutate-and-run.sh` should exit 0.
3. For each key in `dispositions.json.inputs` and `dispositions-before.json.inputs`, `git show d6809df:<path> | sha256sum` must equal the pinned value. The pin sets must include expected.json, verification.json and producer-oracle-repair.json.
4. `--dispositions .ufo/evidence/round-14/dispositions-before.json --json` should exit 1, with the only failing row being producer_before (contains absent).
5. `--dispositions .ufo/evidence/round-14/dispositions.json --json` should exit 0.
6. `diff` of the parsed before and after files: only the producer_before row changes.
7. Static review of the gate source:
   - exactly one file-read site;
   - `object_pairs_hook` present;
   - no `subprocess` outside `--selftest`;
   - no use of a receipt's `exit_matches` as authority;
   - an effective-row `check == name` rule.
8. After L1 runs `capture-context.py`, confirm:
   - context-receipt.json has `injected_env` == `{"GIT_DIR":"/nonexistent/tameshi-round14-poison"}` and no ambient environment dump;
   - sibling identity is recorded before and after both runs;
   - the comparison is labelled bounded to GIT_DIR.

## Claim wording L1 may admit
"The 12 round-13 expectations are reconciled as 11 effective plus 1 explicitly superseded (in after) against lane-committed receipts byte-equal to d6809df. This is consistency with configured, post-observation lane expectations. It is not authentication, not preregistration, and not a re-execution."
