# Round 29 C1 — pre-data design review

Reviewer: CriticC1Design. Frozen lane commit A: `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`.

## Scope and axes

**Primary axis: calibration** — SHONEN box 3 against current committed supporting evidence. **Impacted guardrails: operability** (revision-reproducible measurement) and **freshness** (input drift). Depth and coverage do not increase through restoring this reading; adjacency is outside this change. Definitions: fleet `AXES.md:11-16`; claim-sizing rules: fleet `.ufo/prompts/tameshi-round-29.md:343-365`.

This is the assigned static review, not a control-builder receipt or an admission judgment. No control variants were built, no counters were executed, and no inferred PASS is presented as observed output. Paths below are lane-relative at A unless explicitly prefixed `fleet`.

**Most consequential finding:** the outer counter is frozen, but its executable dependency chain is not. It loads the round-27 counter from the candidate revision, and that counter executes the monitor from the clone's live working tree. Consequently, the declared frozen predicate is not currently a function of frozen measurement code plus REV's committed data alone.

## 1. Identical sentence, executable condition, and label?

**Design verdict: label matches; prose agrees apart from markup; executable identity does not match the promise.**

- Contract label: `"predicate_label": "C1_R29_PASS"` (`.ufo/evidence/round-29/contract.json:15`). Receipt label: `PREDICATE: C1_R29_PASS=` (`.ufo/evidence/round-29/c1-measure.py:119`). These match exactly.
- The contract's predicate is one sentence (`contract.json:16`). The counter repeats it across docstring lines 6–14. Literal differences include contract `"holds a json block"` versus counter `"holds a ```json block"`; the counter also wraps paths and field names such as `reports`, `seat`, `start`, and `heading` in backticks. These are not substantive changes to the intended test, but the strings are not byte-identical after merely joining lines.
- The important difference is contract **"the frozen round-27 counter ... exits 0 at REV"** (`contract.json:16`) versus implementation:

  ```python
  counter = show(repo, rev, R27) or show(repo, BASE, R27)
  ```

  (`c1-measure.py:58-59`). Candidate REV supplies executable counter bytes whenever present. There is no equality check against the frozen round-27 bytes.
- The actual outer Boolean is:

  ```python
  passed = p.returncode == 0 and prefix_equal == 1 and bound == len(appended)
  ```

  (`c1-measure.py:118`). Parsed `covered`, `total`, `restraint`, and `mismatch` are display fields only; absent output becomes `?` and is not rejected (`:70-71`). The tuple is enforced only if the delegated round-27 counter remains authentic (`.ufo/evidence/round-27/c1-measure.py:49-54`).
- A smaller mismatch: the sentence names `.ufo/waves/round-29/*/swarm-registry.json`, but the implementation recursively accepts any path under the round-29 wave prefix ending `/swarm-registry.json`, including different nesting depths (`c1-measure.py:80-85`). Explicit nonempty `seats` and `reports` are also implementation requirements (`:91-93`) that the sentence should spell out rather than leave to the word "bound".

**Smallest safe correction:** before data, pin the delegated counter and monitor dependency identities, fail closed on malformed or missing measurement fields, and copy one precise predicate into contract and counter documentation. Resolve the registry-path/nonempty-set ambiguities explicitly. This is a repair to the oracle, not a new acceptance condition to introduce after scoring; fleet prompt `:357-360` forbids that move.

## 2. Is calibration the axis of the changed surface?

**Design verdict: yes, within the stated bounded surface; not coverage, depth, or independent promotion.**

Contract `:11-12` names calibration and SHONEN box 3. SHONEN actually marks box 3 `[~]` and links the cold-read ledger (`SHONEN.md:9-10`). The inherited counter compares that marked, linked assertion with `box3_full_page` and computes `box3_mismatch` (`round-27/c1-measure.py:45-49`). That is a concrete self-assessment/repo-state mismatch, as required by fleet prompt `:348-349`, rather than a bare score assertion.

The score is explicitly derived from restrained SHONEN marks and current full-page credit (`.ufo/evidence/round-18/measure.py:679-683`), so a genuine 1→0 mismatch correction can be calibration work even if SHONEN's text does not change. Re-scoring an existing rule and attaching evidence does not acquire a new domain surface (fleet prompt `:361-365`).

The extra roster/report check proves only syntactic association, not reader independence. QUALITY now says independence is checked through `seats`, `reports`, and the committed roster (`corpus/QUALITY.md:615-621`); the counter only unions member names and matches section labels (`round-29/c1-measure.py:80-114`). It does not check seat roles, non-authorship, transcript identity, completion, or the report's actual findings. Contract `:20` correctly acknowledges the forged-report/registry limitation. Do not upgrade that bounded association into a claim of independent reading or promotion authority.

**Impacted axes:** calibration directly; operability of the new association check secondarily. **Smallest safe correction:** retain the calibration label, describe the added check as syntactic evidence binding, and keep independent provenance a separately grounded obligation. Do not award new coverage/depth or promotion credit for a restored score of 8.

## 3. Can skipped work or a shortcut meet the predicate?

**Design verdict: yes in code reasoning; no experimental PASS is claimed here.**

### Counter identity shortcut

[INFERENCE] A candidate round-27 counter that simply returns success, while leaving the 371-entry ledger unchanged, satisfies the outer Boolean: delegated exit 0; prefix equal; appended count 0; bound count 0. The missing tuple is tolerated. This follows directly from `round-29/c1-measure.py:58-71,73-78,89-118`.

This example changes a supposedly frozen dependency and violates the contract's declared post-A edit discipline (`contract.json:39`); it is **not** an honest implementation of C1. Its significance is that the purported frozen counter does not enforce its own measurement-code identity. The unchanged outer file is not sufficient protection.

### Reader-free evidence shortcut without changing measurement code

[INFERENCE] Even with authentic counters, the accepted evidence format can be fabricated without a reader: append success-shaped ledger entries keyed by existing section hashes; provide matching input digests, committed trace JSON, a wave member name, and report JSON containing the same `seat`, `start`, and `heading`. That is data construction, not demonstrated cold reading.

Evidence for the gap:

- Section matching uses the entry's section hash (`round-18/measure.py:602-612`); class/verdict and command counts are supplied by the entry (`:477-526`).
- Input verification checks supplied path/digest pairs, not whether the input set is sufficient to support the section (`:330-359`).
- Trace validation checks schema and the trace's declared input pairs (`:393-417`). It neither demonstrates execution nor requires the trace's input map to cover the entry's input map; an empty declared trace-input map has no pairs to reject. The function explicitly says it binds recorded inputs, **"never argv to commands"** (`:373-374`).
- The added round-29 check requires only existing report paths, member names, and matching labels in a JSON block (`round-29/c1-measure.py:80-114`). A report's prose could admit that no reading occurred without being inspected by this check.
- Historical non-stale failure entries still veto credit (`round-18/measure.py:635-638`); a synthetic passing row is not automatically sufficient to erase such a failure. This review does not claim an unrun forged cohort bypassed that protection at A.

Contract `:20` already concedes the central provenance limitation. A genuine committed member label also does not establish that its owner read this section or was a non-author. Fabricating the labels would therefore meet the **syntactic** evidence condition, not the claimed independent-reader provenance.

**Smallest safe correction:** freeze executable identities first; require independently anchored dispatch/transcript provenance for any independence claim, and make the counter validate the intended report result and section/content-revision binding, not merely labels. Extra author-written JSON fields or another author-written digest cannot supply the missing authority. If the claim deliberately remains syntactic-only, say so before data; a winning skip-work control still triggers fleet prompt `:352-356`, rather than being rescued by a new post-data human veto. This trust-boundary tradeoff is for the canonical judge, not an admission decision by this reviewer.

## 4. Is “repair” honest, and what is new over round 28?

**Design verdict: repair is an honest restorative description only with both baselines disclosed; it is not a new calibration capability or newly covered ground.**

There are two different baselines:

1. Contract base `367ec0f1…`: contract `:5,17` records 63/64, restraint 6, mismatch 1. The round-28 spot-check independently records the same final state and names the remaining Round-18 registry section (`corpus/lessons/round-28-verifier-spotcheck.md:40-47,89`).
2. Frozen A: the assignment supplies 52/64 after the round's own edits drifted 12 sections. This observation was not re-run here. Read-only `git diff 367ec0f1… A -- corpus/SOURCES.md corpus/README.md corpus/QUALITY.md SHONEN.md SKILL.md .ufo/evidence/round-21/coldread/ledger.json` shows edits to the first three files, with no displayed change to the latter three. The contract explicitly puts those input edits into its own commit (`contract.json:39`). The 12 drifted sections are not a claim of 12 net newly lost credits: the recorded total changes 63→52, a net loss of 11.

Thus, raising A's 52 back to 63 would principally recover this round's own invalidated evidence, not finish the inherited target. The target is still full-page credit, restraint 8, mismatch 0. That is exactly the round-28 calibration outcome (`SCORECARD.md:1392-1396`; spot-check `:46-47`), not a larger domain outcome.

What round 29 adds is preservation of the now-371-entry prefix and a syntactic member/report binding for appended entries (`contract.json:16`; counter `:73-118`), plus the input-edit-order discipline in QUALITY 56 (`corpus/QUALITY.md:628-636`). Round 28 already preserved its earlier 354-entry prefix and non-entry metadata (`round-28-verifier-spotcheck.md:49-53`). The broader numerical restoration requirement at A is partially self-created work.

Routed-item accounting must remain explicit:

- Round-28 item 1 is C1's actual target: missing Round-18 credit, restraint 8, mismatch 0, and input edits before cold reads (`round-28-verifier-spotcheck.md:89`).
- Item 2, S059 digest drift, is not a predicate of C1 (`:90`); the old digest remains recorded in `corpus/SOURCES.md:68`. Do not imply this counter resolves it.
- Item 3, closing against one head, has a new QUALITY criterion (`corpus/QUALITY.md:638-645`) but is not enforced by the C1 Boolean.
- Item 4 carries the prior README, QUALITY, and runner debts (`round-28-verifier-spotcheck.md:92`). A appends the README wording correction (`corpus/README.md:431-438`) and QUALITY amendments (`corpus/QUALITY.md:613-626`); C1 does not test the runner leg-sum debt (`round-27-verifier-spotcheck.md:202-203`).

**Smallest safe correction:** report original-base→A drift separately from A→landed restoration, call the work restoration of an inherited missed target plus bounded evidence binding, and give an explicit disposition for routed items outside C1. Claim no new depth/coverage or saturation from recovering a self-induced drop.

## 5. Is the 371-entry prefix boundary correct?

**Design verdict: yes for count and off-by-one; narrower than whole-ledger immutability, with a typed-data equality caveat.**

The requested base blob contains exactly 371 entries. Code computes `n0 = len(base_ledger['entries'])`, compares `entries[:n0]`, and checks appended entries from `[n0:]` (`round-29/c1-measure.py:73-78`). Consequently, retained indices are 0–370 and the first appended index is 371. This matches the sentence.

Observed read-only data check, from the private clone:

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r29-CriticC1Design show 367ec0f1:.ufo/evidence/round-21/coldread/ledger.json | timeout 300 jq --slurpfile a .ufo/evidence/round-21/coldread/ledger.json '{base_entry_count: (.entries | length), a_entry_count: ($a[0].entries | length), a_prefix_equal: ($a[0].entries[:371] == .entries), nonentry_keys_equal: (($a[0] | del(.entries)) == (. | del(.entries))), last_index: ((.entries | length) - 1), index_370_heading: .entries[370].heading}'
```

Full stdout:

```json
{
  "base_entry_count": 371,
  "a_entry_count": 371,
  "a_prefix_equal": true,
  "nonentry_keys_equal": true,
  "last_index": 370,
  "index_370_heading": "### Round-21 gate/probe registry — finite environment differential"
}
```

Exit code: **0**. This was a JSON/data inspection, not execution of either counter.

Two limits matter:

- The implementation protects `entries`, not the other ledger keys (`round-29/c1-measure.py:73-78`). Top-level `schema`, `carried_from`, `provenance`, and `round21_provenance` exist (`ledger.json:2,24522-24528`) but are not compared. That matches the narrower frozen sentence about entries; it does not prove the prior round's stronger whole-ledger append-only property (`round-28-verifier-spotcheck.md:49-52`).
- [INFERENCE] Python list/dict equality is not JSON-type-sensitive: `0 == False`. For example, the first entry's `minor_gaps` is integer 0 (`ledger.json:14`); changing that value to JSON false would still compare equal after `json.loads`. The credit functions do not inspect `minor_gaps` (`round-18/measure.py:459-526`). This is a real typed-data preservation gap if “equal as data” means preserving JSON value types, even though the boundary count itself is correct.

**Smallest safe correction:** keep the 371 boundary; use type-sensitive normalized JSON comparison if unchanged JSON data is intended. Include non-entry keys only if the intended frozen promise is whole-ledger preservation, and say that explicitly before data rather than silently enlarging the claim later.

## 6. Does anything read the working tree rather than REV?

**Design verdict: yes — executable monitor sources do; ordinary measured ledger/page/input data are correctly REV-addressed in the authentic implementation.**

Dependency path:

1. Round-29 wrapper obtains the round-27 script through `git show REV:path`, with BASE fallback (`round-29/c1-measure.py:38-40,58-64`). This stage is committed-byte loading, but not fixed-code loading.
2. That script launches the **relative** `.ufo/evidence/round-21/coldread/measure.py` with `cwd=a.repo` (`round-27/c1-measure.py:35-36`). Python opens the clone's live file; it is not extracted from REV.
3. The live selector derives `ROOT` from `__file__` and imports `ROOT / '.ufo/evidence/round-18/measure.py'` from disk (`round-21/coldread/measure.py:17-21`). This is another live-tree executable dependency.
4. The genuine round-18 implementation then reads runner, SHONEN, SKILL, and SOURCES with `git show` at REV (`round-18/measure.py:173-191,659-666`); the default ledger is also fetched at REV (`:1601-1607`). Input and trace blobs are commit-addressed (`:330-350,393-400`). Thus, this is not evidence that it ordinarily reads a dirty working-tree ledger.

[INFERENCE] Holding REV fixed while modifying or removing either live monitor source can change the result. A clean checkout at a different revision also does not ensure those executable bytes are the ones promised by the frozen oracle. The round-27 check of the monitor's self-reported revision/strictness (`round-27/c1-measure.py:42-44`) does not establish the identity of the code making that report.

**Impacted axes:** operability/reproducibility and calibration truthfulness. **Smallest safe correction:** package the frozen round-27 script, round-21 selector, and round-18 implementation together at the frozen identity; run the packaged monitor by an absolute path, preserving the selector's package layout, while passing the candidate clone and REV only as data sources. Do not execute candidate-worktree Python merely because its cwd is the measured repository. This avoids imposing an unrelated clean-worktree requirement and preserves revision-addressed data reads.

## Review boundary

Fixable defects: transitive executable identity, live-source execution, malformed-result acceptance, registry-path ambiguity, and typed prefix equality. Fundamental bound: member names plus author-controlled reports cannot establish independent reading; adding more self-authored labels does not repair that authority gap.

No implementation was edited, integrated, or committed; no judge, counter, model call, or seat spawn was used. An existing control peer was sent code pointers; no additional control work was requested. The only lane write is this report. Work used a private no-hardlinks clone detached at A; frozen C1/C2 counter copies were saved to `/tmp/CriticC1Design-c1.py` and `/tmp/CriticC1Design-c2.py` before review. All shell processes were bounded by `timeout 300` and completed; no long-lived process was started. No tools were installed or updated.
