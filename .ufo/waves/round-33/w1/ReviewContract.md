# ReviewContract — adversarial read of the round-33 frozen contract (w1)

Seat: tameshi-r33-w1-ReviewContract-4. Scope: `contract.json` at freeze `f6d8a891f1d966c5c3cdda385090da3a6e804675` (HEAD). Verdict first; evidence; smallest safe correction. No counter was executed (bounds: default mode is the L1's step; control runs belong to the control seats). All claims below are from reading committed blobs and the working tree.

## Verdict (calibrated)

The claim architecture is sound: C1's predicate quantifies only over sets the counter itself enumerates (18/8 public copies, sealed files via recursive `ls-tree`, and — once F2 is fixed — the control receipt rows); C2's quantifier over SOURCES rows is existential and enumerated by the counter. The runner/tool/snapshot pins are single concrete values, all matching the committed blobs at freeze (`a7d3f2dd…`, `9dbbce62…`, `217edd57…`). The freeze commit is byte-consistent with the contract for tool, snapshot, runner, contract.json, and c2 counter.

Five gaps should be closed by the L1 as amendments before any data run (each listed with severity). None changes the substance of either predicate; they define the measurement protocol the freeze left undefined.

---

## Findings by severity

### F1 (HIGH) The measurements would run un-frozen counter bytes; this is already true for C2

Evidence:
- `frozen_artifacts` pins counters by path only (`c1_counter`, `c2_counter`), with no sha, unlike tool/runner/snapshot. The counter process executes the working-tree file; nothing in either counter verifies the running bytes equal the committed pin (C1's receipt gate ties the receipt to the committed blob, not to the file that is actually running; C2 has no self-check at all).
- Observed drift today: `sha256sum .ufo/evidence/round-33/c2/c2-measure.py` = `f12cef086dd0e53cb6f8964b33417fd425b80ef811e2733da461444973839d06`; committed at freeze and at HEAD = `f1c6c3a73a5da7fcda8da48b72679595241a85196a8afa28a3afe2a1cf4f452d`. The working tree differs.
- The delta (`git diff f6d8a891 -- .ufo/evidence/round-33/c2/c2-measure.py`) changes two behaviors: (1) row acceptance now requires `int(id[1:]) > 99` and teaches opening `supersedes S055` followed by whitespace or a dash (was `startswith('supersedes S055')`); (2) the digest search is now scoped to the `## Gate` section (`re.search(r'^## Gate\b(.*?)(?=^## |\Z)', …, re.M|re.S)`) instead of the whole lesson file. These edits tighten the counter, but they are post-freeze edits to a frozen artifact, uncommitted, with no amendment artifact (F5) and no disclosure.
- This drift appeared during this session (working sha matched the freeze in an earlier check minutes before). The L1 must reconcile authorship, revert or commit as an explicit amendment.

Smallest safe correction:
- Contract: add counter shas to `frozen_artifacts` (or to an amendment record), and add a sentence: "the L1 runs both counters from the committed frozen bytes (`git show REV:<path>` into a temp dir) and records both counters' shas with the after-receipt; the working-tree copies are not the measured object."
- Immediately: reconcile the c2 working-tree drift before any controls receipt or data run.

### F2 (HIGH) The controls-receipt gate does not enforce the receipt's content; the C1 receipt conjunct is reachable by a do-nothing control world

Evidence:
- `c1-measure.py:287-288`: `controls_ok = (receipt.get('counter_sha256') == sha256(self_b) and receipt.get('all_false') is True)`. The default gate never inspects `controls`: an empty list, rows with `predicate_pass: true`, missing tools, or a fabricated `all_false: true` all pass as long as the counter sha matches.
- The contract predicate (contract.json line 18) says the receipt "records every control tool failing the predicate". With the gate as written, a receipt with `controls: []` and `all_false: true` satisfies the conjunct with zero control scoring. Named control: the CtlDoNothing world (or no control run at all) can reach this conjunct; because the control seats write the receipt via `--write-controls` (which does fill rows), the hole is specifically a hand-authored or truncated receipt — the counter cannot distinguish it.
- Note the asymmetry that is fine: `--write-controls` scores controls against the public panel only (the sealed set does not exist yet), so a control that passes public blocks data (`all_false=false` → exit 1) — conservative and intended. The sealed set is the real defense; the control wave cannot catch a public-only allowlist. That limitation is inherent and should stay.

Smallest safe correction (counter, lines 287-291):
- Require `isinstance(receipt.get('controls'), list) and len(receipt['controls']) >= 1 and all(r.get('predicate_pass') is False for r in receipt['controls'])`; keep the sha check.
- Contract sentence: append "…and the counter rejects a receipt whose controls list is empty or contains any `predicate_pass` entry."

### F3 (HIGH) Kill-rule gaps: what a "full run" is, when the measurement revision is chosen, and whether seat re-runs score

Evidence: `kill_rule` (contract.json, C1 and C2) says "the first full default-mode counter run at the measurement revision decides" / "the first full counter run at the measurement revision decides". Undefined:
- "Full": a run that exits 2 (SETUP — `c1-measure.py:358-362` prints `C1_R33: SETUP (…)` and exits 2), a run killed by `timeout`, or a host failure prints no verdict line. Is one of those "the first full run"? If yes, PASS=false would be recorded without a verdict; if no, the rule is silent.
- "At the measurement revision": REV is the L1's free choice; nothing pins it to a recorded commit (round 32 pinned the seal commit `24a5a5bb`; round 33 has no equivalent sentence).
- Seat re-runs: wave rule 1 ("no counter runs on tool bytes outside the item that names them") makes seat scoring impossible, yet the kill rule says "a rule changed after any seat has scored is not the claim's rule" — the clause is inert/contradictory as written.

Smallest safe correction (exact sentence for both C1 and C2 kill rules):
- "The deciding run is the first default-mode counter run at the measurement revision that prints the final `C1_R33:`/`C2_R33:` verdict line and exits 0 or 1. A run that exits 2, is killed, or times out before printing that line does not decide; its state is preserved and the next qualifying run decides. Only the L1's deciding run scores; dev sweeps, seat runs and re-runs are observations and never scorers. The measurement revision is the lane tip at the moment the L1 launches the deciding run, recorded in that run's `rev=` output."
- Optionally add: "the 18/8 public copies are seed-dependent for the 9/2 generated members; the seed of the deciding run defines the panel evaluated, which is why the first-run rule exists."

### F4 (MED-HIGH) C2 lesson-Gate digest coupling: format trap and attribution gap

Evidence (working c2, lines 75-81): the digest search is now correctly scoped to the `## Gate` section, but still requires the token `sha256[ :=]+([0-9a-f]{64})` — separators only, no interposed characters:
- The established lesson house style wraps digests in backticks: round-32.md lines 21, 28, 31 (`sha256 \`f3d37d57…\``). Under the current regex a Gate written in house style finds no token and `gate_sha_ok` stays false — a correct Gate would cause C2 to miss. A false negative the scribe can trip by following the established format.
- Attribution: any sha256-labeled true-digest token inside the Gate section satisfies the check, even if the sentence attributes the digest to the wrong URL (e.g., the moving `/3/` alias) or omits the snapshot path, access date, and byte count that the counter docstring says it verifies (c2-measure.py lines 14-15). The check binds the digest to the Gate section, not to the snapshot record.

Smallest safe correction:
- Contract sentence: change "the digest recorded in the round-33 lesson Gate at REV" to "the round-33 lesson Gate section at REV (between `## Gate` and the next `##` heading) contains a sha256 token equal to the committed snapshot digest, written as `sha256 <hex>` (no backticks around the hex), alongside the versioned URL `https://docs.python.org/3.15/library/doctest.html` and the access date".
- Counter hardening (recommend as an amendment): within the Gate block, match `sha256[ :=`]+([0-9a-f]{64})` (tolerate backticks) and additionally require the versioned URL substring in the same block.

### F5 (MED) Amendment procedure: amendment 1 already landed without the artifact the contract requires; compare round-32 amendment-2

Evidence:
- HEAD = `27902a165aa932dabf65f0e13d55cb202b4cd770` "round-33 amendment 1: fix c1 counter --write-controls --receipt arg handling (procedural; predicate, kill rule and label unchanged; no seat has scored the claim's rule)". `git diff f6d8a891 -- .ufo/evidence/round-33/c1/c1-measure.py` shows only the `write_controls` signature/receipt-path change (procedural, as claimed).
- The contract says amendments "land only as new frozen artifacts … and are disclosed in the round lesson". Round-33 evidence has no `contract-amendment-N.json` (directory listing of `.ufo/evidence/round-33/`: `c1 c2 before contract.json dev repair`), and there is no round-33 lesson yet. Disclosure exists only in the commit message.
- Round-32 precedent (the standard to compare against): `.ufo/evidence/round-32/v2/contract-amendment-2.json` has schema, `amends` link, `change`, `reason`, `data_disclosure` (including the L1's explicit judgment), `new_TOOL_SHA256`, unchanged `kill_rule`; the round-32 lesson (lines 62-65, 117-120) records that amendment 2 re-pinned the tool before any v2 run after DeterminismProbe's finding. The round-32 ruling therefore is: a re-pin before any data run is still the claim's rule when it lands as a new frozen artifact before any run and is disclosed — the closure's routed mistake-7 fix then made the counter refuse to run without a committed receipt naming its sha, which is now c1's gate.
- So: the procedure is sound; this round has not followed it for amendment 1 (no artifact).

Smallest safe correction (L1 action + contract sentence):
- L1: create `.ufo/evidence/round-33/contract-amendment-1.json` before data with the round-32 amendment-2 fields (schema, amends, change, reason, data_disclosure stating no default-mode run has occurred, new counter shas for both counters, unchanged kill rule).
- Contract sentence (replace the parenthetical in the kill rule): "amendments land only as new frozen artifacts (`.ufo/evidence/round-33/contract-amendment-N.json`, naming the changed pins and stating that no default-mode run has occurred) before any data run and are disclosed in the round lesson; a tool re-pin or counter amendment before any data run remains the claim's rule only in that form — otherwise it is a rule change after scoring and not the claim's rule."

### F6 (LOW) Contract/counter wording mismatches to align while F1 is open

- The frozen c2 row regex `S[0-9]{3,}` also matches `S099` (lexically), so the sentence "id > S099" is under-enforced by the frozen counter; the uncommitted working version adds the numeric check. Resolve together with F1 (keep the numeric check).
- The contract says teaches "opens `supersedes S055 -`"; the frozen counter checks `startswith('supersedes S055')` without requiring the dash; the working version accepts whitespace or a dash. Align the sentence to the stricter form (`supersedes S055` followed by whitespace or a dash).
- `no_universal_clauses` (contract.json line 52) claims the only quantifiers "run over sets the counter itself enumerates (… the SOURCES rows)". True for both claims once F2 is fixed; C2 additionally relies on the lesson Gate section existing at REV — note `corpus/lessons/round-33.md` does not exist yet (expected; must exist at measurement, else `gate_sha_ok=false`).

---

## Residual risk and verification gaps

- I did not execute either counter (bounds prohibit default runs; control runs belong to the control seats). All code-level findings are from reading the committed/frozen blobs and the working tree; the receipt-gate behavior (F2) is read, not exercised.
- The c2 working-tree drift (F1) appeared during this session; authorship is unattributed here. The L1 must reconcile before any controls receipt is committed.
- The sealed held-out set does not exist yet, so no held-out assessment is possible; `ho_invalid=0` and the ≥8/≥6 size thresholds (`c1-measure.py:346`) are the enforcement points.
- The control seats (CtlDoNothing, CtlAlwaysPass, CtlAlwaysFail, CtlShaOnly) will each run `--write-controls`; the L1 must commit one receipt that names the counter sha at the measurement REV (`edd8fbb0…` for c1 at HEAD) and verifies the new gate (F2) before data.
- bwrap/tool behavior was not re-run here; the tool auditing relies on v1's `run_tool` (600 s timeout) unchanged from round 32.

## Commands used (exit-captured)

- `git -C <lane> rev-parse --verify f6d8a891…^{commit}` → `f6d8a891f1d966c5c3cdda385090da3a6e804675` (exit 0).
- `git -C <lane> log --oneline -6` → HEAD `27902a165` (amendment 1), freeze `f6d8a89`, prior round-32 heads (exit 0).
- `git -C <lane> diff f6d8a891 -- …` (c1, c2): only c1 changed, 10+/10- (c1); c2 working drift described in F1 (exit 0).
- `sha256sum` of working files: tool `9dbbce62…`, runner `a7d3f2dd…`, snapshot `217edd57…`, c1 `edd8fbb0…`, c2 `f12cef08…`; committed-at-freeze: tool `9dbbce62…`, c1 `7ff776df0…`, c2 `f1c6c3a…`, contract `bf8f477c…` (all exit 0).
- `grep -c` of the QUOTE byte string in `doctest-snapshot.html` → 3 (exit 0).

No tools were installed; no production files were edited; the only file written is this report.
