author: TameshiR15.AttackMapping (critic, leaf; source-read only)

# AttackMapping — falsifying planned C1 on "mapping false → exit 1"

Read revision: lane HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0`. `tools/context-capture.py` **did not exist** when I read the tree (`tools/` glob: evidence-disposition, pin-disposition, witness-metadata, bash-witness-study, repeat-control, mutate-and-run.sh). Historical `.ufo/evidence/round-14/capture-context.py` on disk sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` = `tool_sha256` in retained `context-receipt.json:4`, so the source I attacked is the receipt's tool. I executed nothing from the lane: no gate, no selftest, no helper, no regex trial. Every behavioural statement below comes from reading the source. Where I trace control flow by hand, I mark it [SOURCE-TRACE]; I did not run it. Tool installs: none.

Axes affected: **calibration**, through C1 and routed defect 5. Operability is touched only if the CLI surface changes. Depth, coverage, freshness and adjacency are untouched.

## 1. What the current evidence actually tests

- `guardrails.json` check `runner_variable_swap_discriminator` loads the script with `runpy`. It calls only `parse_runner_mapping` and `mapping_block`, then asserts `not out["all_match"]` and `not row["checks"]["constant_names_match_leg"]`. It never calls `decide()` or `main()`, and never observes an exit code or finding. The round-14 closure routed this as "helper-only … do not satisfy that clause" (`corpus/lessons/round-14-verifier-spotcheck.md:160`).
- `decide()` (capture-context.py:553-580) turns `mapping.all_match` falsy into `mismatch`/exit 1 (`:576-577`). It returns free-text reasons only. No stable finding ID exists anywhere in the script; the only stable tokens are the five `CHECKS` names (`:109-115`) and receipt keys `all_match`, `leg_set_equal`, `leg_order_equal`.

## 2. Counterexample A (primary): mutant that removes the mapping verdict and still passes both nominal tests

**Mutant M:** delete `capture-context.py:576-577` (or equivalently rename the `all_match` key read by `decide`).

| Test | Under M | Why [SOURCE-TRACE] |
|---|---|---|
| Helper-only swap control (guardrails) | still passes, prints `runner_variable_swap_rejected` | it never reaches `decide` |
| "Nominal CLI" test: copy lane to temp, replace `"$REV_BASH"` with `"$REV_CHECKLIST"` in the bash-surface-census call, run CLI, assert exit 1 | **still exit 1** | any runner byte change breaks `sources.runner.matches_manifest_declaration` (`:504-509`, manifest `derived_from.sha256` = `75ed934…`), so `decide` emits "runner source digest does not match the manifest declaration" (`:574-575`) whatever the mapping says |
| "Nominal CLI" test in a temp lane that is not `git init`'d | **still exit 1** | `git rev-parse --git-dir` baseline fails → `baseline_ok` false → `control.effective` false → "git poison positive control is ineffective" (`:403-409`, `:570-571`) |

So "mapping false → exit 1" is non-discriminating whenever any other `decide` predicate co-fails. In a mutated-runner fixture, the runner-digest predicate always co-fails unless the fixture manifest is re-declared. Exit agreement alone repeats the round-13 lesson ("Exit agreement alone proves intended regression — reject", spotcheck:125).

**The fixture that kills M** is a differential pair of real CLI subprocess runs over the same synthetic temp lane:

1. **Clean twin.** The fixture runner is minimal synthetic text and need not be the 1500-line runner. It must contain:
   - six `#   <leg> <repo>/<path> N/N (N%)` header rows matching `HEADER_ROW_RE` (`:83-88`);
   - six `PIN_X=<64hex>` and six `REV_X=<40hex>` lines with suffixes JS/BASH/TSUKUROI/MADO/CHECKLIST/CLAIMS;
   - a `run_regression() {` … `}` block, closing brace at column 0, with six `regression_case_git` calls in manifest order matching `CALL_RE` (`:92-101`);
   - REV_BASH == REV_CHECKLIST, mirroring the real runner `:545,:551`, so that the swap is value-neutral.

   The rest of the fixture:
   - The manifest has `derived_from.path` ending `tools/mutate-and-run.sh` and `derived_from.sha256 = sha256(fixture runner)`.
   - `expected.json` has `inputs["tools/pin-disposition.py"] = sha256(fixture probe)`.
   - The lane root is `git init`'d; the poison path is absent.
   - The probe yields a six-leg `pin-disposition-v1` `status:"ok"` doc. It must carry `observed_at`, `pinned.status:"verified"`, non-`unavailable` content and `tool_sha256` equal to its own disk digest. It can be the real probe over synthetic sibling git repos (the pattern in `pin-disposition.py:697-733`) or a stub.

   Expected result: **exit 0, findings `[]`.**
2. **Mapping twin.** Identical except one call's `"$REV_BASH"` becomes `"$REV_CHECKLIST"`, **and the fixture manifest `derived_from.sha256` is recomputed to the mutated runner digest**. The manifest legs, the probe and therefore the probe output are unchanged. The probe does not read `derived_from`: grep for `derived_from` in `pin-disposition.py` finds no hits.

   Expected result [SOURCE-TRACE `:283-294`]: only `bash-surface-census` fails, on exactly `rev_name_and_value_match_manifest` (the name differs while the value is equal) and `constant_names_match_leg`. Six PIN and six REV definitions remain, so the parse passes. Set and order stay equal. Literal historical reason text: `leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg`. **Exit 1.** The finding set must be **exactly** the mapping IDs; checking that it merely contains them is not enough.

Under M the mapping twin exits 0, so the pair discriminates. A selftest that asserts only `exit==1`, or asserts that the findings include the mapping ID while other IDs are present, does not kill M.

## 3. Counterexample B: retained-receipt check mode trusts a forgeable summary bit

The integration interface plans a retained-receipt checker that reuses `decide` predicates. `decide` reads only `mapping.all_match` (`:576`). Take this receipt variant:

- the round-14 `context-receipt.json` with `mapping.legs[1].checks.constant_names_match_leg` set to `false` and `legs[1].match` set to `false`;
- top-level `mapping.all_match: true` and `reasons: []` left unchanged.

Through `decide` it returns `ok`/0 [SOURCE-TRACE]. A degenerate `"mapping": {"all_match": true}` also passes. A helper-only test that feeds `decide` a dict with `all_match:false` passes while this receipt-mode false-clean ships.

## 4. Counterexample C: optional hardening (pre-existing in historical source, not routed)

- **Commented call evasion.** `CALL_RE.finditer` runs over the whole continuation-joined body (`:223-225`) and is not anchored to line start. A commented-out call (`# regression_case_git bash-surface-census … "$REV_BASH" …`) therefore counts as a call. Suppose the live call is rewritten so `CALL_RE` no longer matches it (for example `${PIN_BASH}` instead of `"$PIN_BASH"`) and the manifest `derived_from` is re-declared. The count stays 6 and `all_match` stays true, so the result is exit 0 while the executed binding changed. The only trace is `runner_call.line == None`, because `CALL_LINE_RE.match` rejects `#` lines (`:102,:227-234`), and nothing checks it.
- **Unquoted reassignment.** `PIN_CONST_RE` is `^PIN_X=<64hex>$` (`:89`), so a later `PIN_BASH="$PIN_CLAIMS"` is invisible.

Both need a re-declared runner digest to reach exit 0, so the digest pin remains the primary guard. Cheap fixes:
- anchor `CALL_RE` as `^[ \t]*regression_case_git` with `re.M` on the joined body, and/or fail mapping when any `line is None`;
- reject any `^(PIN|REV)_[A-Z0-9_]+=` assignment line not matched by the strict regex.

Do not make these C1 blockers.

## 5. Classification facts the selftest must respect (exit2 preempts exit1)

These are [SOURCE-TRACE] facts. Do not fixture them as exit 1.

- Runner perturbations that change call/header count, uniqueness or shared leg set raise `InvalidContext("runner_unparsed")` → **exit 2** (`:242-253`). Examples: a dropped call, a duplicated leg, a call that no longer matches `CALL_RE`, a header renamed without its call.
- Manifest-leg perturbations are rejected by the probe before `decide`. This covers a changed repo/path (checked against the embedded `CANONICAL_BY_LEG`, `pin-disposition.py:126-136`) and a changed commit/sha, which yields a pinned status that is not `verified`. Either way the result is `probe_baseline_unusable` → **exit 2** (`:352-361`). The mapping block is computed (`:515`) but loses to exit 2.
- So a hermetic mapping-false exit-1 fixture **must perturb the runner, not the manifest legs**, and must re-declare `derived_from.sha256`. A consistent leg rename in both header and call keeps the parse valid, so it gives set/order mismatch → exit 1. Only this and the REV-name swap are clean single-cause exit-1 cases.

## 6. Recommendations

**Required (routed defect 5 plus the stated C1 interface; impacts calibration):**

1. The standalone `--selftest` invokes the public CLI as a subprocess against a temp lane via a root override. The historical `LANE_ROOT` is SELF-derived (`:45-47`). For `tools/context-capture.py` this must be **two** `dirname`s; copying the four-level expression lands on `/home/vgpnk/Projects`. Add an explicit `--root` (lane) option used by both selftest and prospective mode. Receipt output goes under that root at the round-15 path, so round 14 is never written.
2. Emit stable finding IDs with deterministic JSON. Mapping IDs derive from existing tokens, for example:
   - `mapping_leg_set_differs`;
   - `mapping_leg_order_differs`;
   - one ID per failed `CHECKS` name, such as `mapping_rev_name_and_value_match_manifest` and `mapping_constant_names_match_leg`, with the leg in `detail`.

   Keep the non-mapping predicates distinct, for example `runner_digest_mismatch`, `positive_control_ineffective` and `probe_observation_mismatch`. Then a co-failing predicate is visible rather than satisfying the mapping assertion.
3. Include the differential pair from §2 with literal expectations:
   - clean twin: `(0, [])`;
   - REV-swap twin with re-declared digest: `(1, ["mapping_constant_names_match_leg", "mapping_rev_name_and_value_match_manifest"])`, compared as an exact sorted list, in the convention of `evidence-disposition.py:1571-1572`.

   Optionally add a third twin: the same swap **without** re-declaring the digest. Expect exactly the runner-digest ID **plus** the two mapping IDs, which proves the IDs do not mask each other.
4. Receipt-check mode must not trust the summary bits in `mapping.all_match`, `match` or `reasons`. It must:
   - recompute each `match` from exactly the five `CHECKS` keys;
   - recompute `all_match = leg_set_equal ∧ leg_order_equal ∧ all(match)`;
   - require six legs whose order and set equal the manifest legs;
   - emit a distinct ID when the stored summary disagrees, for example `receipt_mapping_summary_inconsistent` (exit 1, or exit 2 if classified as tamper; pick one class and pin it).

   Pin §3's forged receipt as a selftest case.
5. In the registry (SKILL.md:1602, owned by Registry), state that exit 2 dominates exit 1. Declare 64 explicitly as usage/could-not-evaluate (the historical `main` `:610-613` returns 64 with no receipt).

**Optional hardening (not routed; must not gate admission):**

- §4 call anchoring and the `line is None` failure; strict-assignment rejection.
- The selftest checks that the positive-control baseline `--git-dir` resolves inside the temp lane, so that a git repo in a parent directory cannot leak.
- The selftest classifies a host-existing `POISON_PATH` (`/nonexistent/…`, an `lexists` on the host, `:469`) as could-not-evaluate (2), not FAIL.

**Unearned claims to reject:**

- "mapping false → exit 1 is verified" on the strength of the guardrails helper, or of a bare exit-1 CLI run;
- that the mapping check detects every binding change: §4 shows it does not once the digest is re-declared;
- any claim that the selftest re-proves round-13/14 live observations;
- any change to calibration scalar 6.
