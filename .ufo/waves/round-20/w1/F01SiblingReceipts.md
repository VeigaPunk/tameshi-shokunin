# F01 — Sibling Lanes Scan: Receipt-Window, Instrument-SHA, and Measurement-Interval Rules

**Seat:** `TameshiR20-3.F01SiblingReceipts`  
**Role:** UFO-FSD Connector  
**Round:** 20 (Attempt 2, hyaku), Wave 1 Advisory  
**Target:** Scan sibling lanes' `corpus/lessons/round-*-verifier-spotcheck.md` and `QUALITY.md` for receipt-window, instrument-sha, or measurement-interval rules. Report each match (lane, path, line, rule) and whether tameshi's gate duplicates or could reuse it. Read-only; do not edit siblings.  
**Report Path:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/w1/F01SiblingReceipts.md`  

---

## 1. Declared Axes

1. **Calibration (Claim C1, Primary Focus, Lane Cap 8):** Close the QUALITY20 recurrence by advancing the population from 0/6 to 6/6 via a contract frozen before dispatch, staged instruments, and a receipt-time instrument-sha / measurement-interval validity gate. Numeric score is held at lane cap 8 (the final 2 points require independent outside review).
2. **Depth:** Preserved at 8 (no reduction in verification-fixture breadth or depth).
3. **Substrate & Contract Integrity:** Zero mutations to production code, sibling lane files, Git/JJ refs, or fleet infrastructure. All checks are hermetic, stdlib-only, and read-only.
4. **Quality & Discernment:** Grounded verification across all 20 sibling repositories; explicit distinction between intentional hermetic leaf design and defective duplication; trace second-order effects across contract, substrate, and verification surfaces.

---

## 2. Executive Summary

A comprehensive scan across all 20 sibling lanes in `/home/vgpnk/Projects/shokunin/*-shokunin` was executed, covering both `corpus/QUALITY.md` and all filed `corpus/lessons/round-*-verifier-spotcheck.md` documents.

- **10 sibling lanes** contain explicit rules governing instrument digests (`tool_sha256`, `producer_digest`, `PINNED_INSTRUMENT_SHA256`), execution timestamps, or pre-freeze/post-freeze validity boundaries:
  - `mado-shokunin`: Criterion 24 (producer identity `tool_sha256`), Criterion 25 (mutant receipts), `receipt-check.py`.
  - `tabi-shokunin`: Criterion 26 (run claim argv/producer digest/rev), Criterion 30 (producer path and sha256), Criterion 35 (no-harm gate set binding), Criterion 37 (selftest producer identity).
  - `mori-shokunin`: Criterion 33 (in-process load-vs-end input hashing, `moving: false`), Criterion 58 (freeze-order receipt executing-script digest), Criterion 62 (present delivered instrument failure vs missing capability).
  - `kengaku-shokunin`: Rule R7 (unscored pre-freeze runs; `FROZEN: timestamp < request_ts`).
  - `kaidoku-shokunin`: Criterion 19 (temporal stability pin maps at UTC instants), Criterion 23 (evidence timestamp `<= committer_time (%cI)` via `evidence-timestamps.py`).
  - `kake-shokunin`: Criterion line 103 (derived counts vs declared total), line 128 (disposable runner git recreation), line 148 (live-page `fetchedAt`), `round-22-verifier-spotcheck.md` (`PINNED_INSTRUMENT_SHA256`).
  - `souji-shokunin`: Criterion Q6 (verdict sha256 equals installed file), Criterion Q31 (pointers to committed objects), Criterion Q41 (no rewriting filed evidence).
  - `kasegi-shokunin`: Rule R3 (instrument verdict names matcher, definition, and byte inputs), Rule R7 (freeze detector before implementation).
  - `game-dev-2d-shokunin`: Criterion Q8 (serial-only battery receipts), Criterion Q9 (verdict cites blob SHA).
  - `game-dev-3d-shokunin`: Criterion Q9 (target SHA-256 and adversary suite), Criterion Q13 (concurrent seed mutation is infrastructure failure).
- **10 sibling lanes** (`audio`, `chousa`, `kagi`, `kama`, `kotoba`, `kotodama`, `kumitate`, `lore`, `revenger`, `tsukuroi`) were scanned with zero matching receipt-window or measurement-interval rules (they enforce general provenance, exact quotes, and replay commands, but lack temporal interval or instrument-sha gating).
- **Key Finding:** No sibling lane possesses a gate identical to tameshi's `stage/receipt-window.py`. Tameshi's gate is unique in solving the QUALITY20 recurrence by enforcing a two-phase temporal interval gate (`measurement_interval` vs `edit_interval`) paired with contract-indexed instrument SHAs and historical classification.

---

## 3. Sibling Lanes Scan: Matches & Duplication / Reuse Analysis

### 1. `mado-shokunin`

- **Matches:**
  - `mado-shokunin/corpus/QUALITY.md:131–137` (Criterion 24):
    > "24. A sentence that relies on a scan, selftest, measure or replay receipt cites one whose own bytes name its producer (`tool_sha256=` equal to `git show <measured_commit>:<tool> | sha256sum`, read with the producer status checked) and its `measured_commit`; a claimed re-cut is a committed receipt with those fields, never a narrated rerun; a report labels every tool sha with the revision it belongs to..."
  - `mado-shokunin/corpus/QUALITY.md:138` (Criterion 25):
    > "25. An instrument tightening counts as biting only with a committed mutant receipt in which the pre-change instrument credits a committed mutant and the post-change instrument rejects it, both instruments named by sha256 and each mutant by its diff digest..."
  - `mado-shokunin/corpus/lessons/round-18-verifier-spotcheck.md:47, 70–71, 118` (Verifier spot-check of Criterion 24):
    - Line 47: Validates `grep -c tool_sha256=` across round-17 receipts (producing red findings `MISSING_PROVENANCE`).
    - Lines 70–71: Verifies `evidence/tripwire-frozen-before.txt` header `tool_sha256=962919ce…` vs after `tool_sha256=c1ae45a7…`.
    - Line 118: Defect R18-V2 requiring committed header-bound receipts (`tool_sha256`, `measured_commit`).
  - `mado-shokunin/corpus/lessons/round-19-verifier-spotcheck.md:51–53`:
    - Checks that `hashlib.sha256(git show 7b4839d:PRODUCER)` matched receipt headers.
  - `mado-shokunin/.ufo/waves/round-18/receipt-check.py`:
    - Runnable checker reading `receipt-claims.json`; extracts `tool_sha256` and `measured_commit` from receipt text, checks git ancestry (`git merge-base --is-ancestor`), compares against `git show <measured_commit>:<tool> | sha256sum`, and emits `ok`, `MISSING_PROVENANCE`, `SHA_MISMATCH`, or `STALE`.
- **Duplication vs Reuse:**
  - *Duplicate:* Mado and tameshi both mandate that every execution receipt carries the SHA-256 of the executing tool and reject receipts missing this provenance (`MISSING_PROVENANCE` in mado, `RECEIPT_MISSING_FIELD`/`UNKNOWN_INSTRUMENT` in tameshi).
  - *Differences:* Mado's `receipt-check.py` relies on live Git subprocesses (`git show`, `git merge-base`) dynamically checking individual files. Tameshi's `stage/receipt-window.py` is fully hermetic and operates on JSON documents (`contract.json` + `receipts.json`), leaving Git commit checks to `measure.py`. Furthermore, Mado has no concept of `measurement_interval` or `edit_interval` (time-window boundaries).
  - *Reuse verdict:* Tameshi cannot reuse `mado-shokunin`'s script because tameshi requires hermetic execution without git execution inside the validity gate. However, Mado's concept of `STALE` (tool modified between measured revision and read revision) is conceptually handled in tameshi via the interval gate.

### 2. `tabi-shokunin`

- **Matches:**
  - `tabi-shokunin/corpus/QUALITY.md:102–106` (Criterion 26):
    > "26. A run claim (a count, verdict or exit 'at REV') cites a committed receipt recording argv, producer digest, the revision it ran at and its exit; or it says 'holds by drift diff' and names the empty `git diff --name-only` over every counted input plus the counter path..."
  - `tabi-shokunin/corpus/QUALITY.md:126–130` (Criterion 30):
    > "30. A committed receipt records the producer it ran (path and sha256 of gate, selftest, harness or counter); a claim cites it only when that digest equals the blob registered for the claim. Receipts from an earlier hardening are labelled history by a committed index in the superseding round; the frozen receipt is not edited."
  - `tabi-shokunin/corpus/QUALITY.md:147–150` (Criterion 35):
    > "35. A no-harm receipt binds the complete gate set and executed gate bytes to the measured revision; a later orchestration runner has its own separately pinned identity. An earlier run is not a run at that revision."
  - `tabi-shokunin/corpus/QUALITY.md:154–156` (Criterion 37):
    > "37. A self-test claim cites a committed receipt under `corpus/evidence/` with argv, exit, stdout and producer identity, not solely a wave summary."
- **Duplication vs Reuse:**
  - *Duplicate:* Criterion 30 is the exact conceptual counterpart to tameshi's contract-registered instrument sha checks and historical classification. Tabi explicitly requires that historical receipts from earlier hardenings be classified/indexed as history rather than rewritten, which directly mirrors tameshi's rider: historical bytes and receipts are immutable, classified by `contract.json:historical`.
  - *Differences:* Tabi enforces this through manual spot-check and prose verification rather than a dedicated gate script. Tabi lacks temporal interval validation (`measurement_interval`).
  - *Reuse verdict:* Tabi's rule validates tameshi's design posture, but provides no software artifact for tameshi to reuse.

### 3. `mori-shokunin`

- **Matches:**
  - `mori-shokunin/corpus/QUALITY.md:78` (Criterion 33):
    > "33. A receipt's provenance is the exact identity and content of every verdict-driving input, not a `dirty` boolean or a porcelain status line... A gate receipt must hash each declared input at load and at end (`__file__`/imported module bytes, census, frozen control, fixture packs), record the observed `rev-parse HEAD` rather than an asserted pin, and report `moving: false` only when the scope is equal and every declared input digest is equal; otherwise the run is a dirty or moving working-tree observation that cannot be cited as committed bytes or as a complete dirty-path list."
  - `mori-shokunin/corpus/QUALITY.md:196–201` (Criterion 58):
    > "58. A freeze-order receipt carries the measured full commit, exact loaded-byte register/correction digests, executing-script digest, resolved claim bases/tips, overrides and argv. Unbound legacy output remains unbound; new metadata does not retroactively bind old JSON. A historical correction and prospective-label verification are separate units, not interchangeable defects."
  - `mori-shokunin/corpus/QUALITY.md:217–221` (Criterion 62):
    > "62. A present delivered instrument that crashes or returns malformed metadata is an after-mode regression, not proof that its capability is absent. Missing-capability red is reserved for the explicitly measured before boundary; source and receipt failure must remain distinguishable."
- **Duplication vs Reuse:**
  - *Duplicate:* Criterion 58 requires the executing-script digest in freeze-order receipts. Criterion 33 addresses the exact problem of instrument/input mutation during execution.
  - *Differences:* Mori solves in-run mutation by double-hashing inputs (`at load and at end`) inside the single tool process. While effective for a single process, this does not protect against cross-seat in-wave mutations where an L1 integrator edits a file while concurrent subagent seats are reading it. Tameshi's approach (stage changes at a separate path before dispatch, install only after wave completion, gate receipts by measurement interval) is architecturally superior for multi-agent swarm waves.
  - *Reuse verdict:* Mori's double-hashing is orthogonal. Tameshi should not replace staging with in-process double-hashing.

### 4. `kengaku-shokunin`

- **Matches:**
  - `kengaku-shokunin/corpus/QUALITY.md:133` (Rule R7):
    > "R7 — runs before the freeze are tagged unscored. Any trial whose UTC precedes the `FROZEN:` line is labelled `unscored` in its receipt and is never cited as coverage; the scored block names the freeze sha. No live request is sent before the frozen battery/table file exists (M09). Check: the `FROZEN:` timestamp is earlier than the first scored `request_ts`, the earliest `request_ts` of any receipt is later than the frozen file's first commit or `FROZEN:` line, and every pre-freeze receipt contains `unscored`."
- **Duplication vs Reuse:**
  - *Duplicate / Analogue:* Rule R7 is the most direct sibling precedent for receipt timestamp gating. It compares a receipt execution timestamp (`request_ts`) against a contract freeze timestamp (`FROZEN:` line or commit time) and requires `frozen_time <= request_ts`.
  - *Differences:* Kengaku's R7 only checks a single lower boundary (`request_ts >= frozen_time`). Tameshi's `stage/receipt-window.py` implements a complete two-phase lifecycle with edit intervals:
    - Frozen instrument receipt must satisfy: `measurement_interval.end <= edit_interval.start`.
    - Installed instrument receipt must satisfy: `measurement_interval.start >= edit_interval.end`.
    - Rejects receipts overlapping the edit interval or using unindexed instrument SHAs.
  - *Reuse verdict:* Tameshi already generalizes and surpasses Kengaku's R7. However, Kengaku's R7 provides a critical insight for tameshi's identity case (see Section 4).

### 5. `kaidoku-shokunin`

- **Matches:**
  - `kaidoku-shokunin/corpus/QUALITY.md:29` (Criterion 19):
    > "19 | A temporal-stability statement about a run or execution ('unchanged during/across/throughout a run or execution', 'stable throughout') is admitted only in the form 'identical bytes at the named instants', and every instant named must have a retained record: the producing tool keeps each pin map (per-path SHA-256 and size) with its UTC timestamp and the comparison verdict, including mid-run checks, plus a retained red run in which a mutated path is named and the comparison fails..."
  - `kaidoku-shokunin/corpus/QUALITY.md:33` (Criterion 23):
    > "23 | An evidence timestamp is admitted only if it is at or before the committer time (`%cI`, not blame's author column) of the commit that introduced its line. Every zoned timestamp in a round's committed evidence tree is checked with `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <lane> --rev <shipping-rev> --path <dir> --strict` (exit 0 required); a later instant is a `future_dated <path>:<line>` defect. Zoneless timestamps are not checked and are stated as unchecked; no grace window (a +65 s instance exists)..."
  - `kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py`:
    - Standalone tool checking that timestamps in committed evidence do not exceed `%cI` committer time.
- **Duplication vs Reuse:**
  - *Duplicate / Synergy:* Kaidoku's Criterion 23 establishes the fleet standard for timestamp integrity against Git commit time. In tameshi, `stage/measure.py` implements the corresponding check for contract freeze order: `contract.frozen_at <= commit_time(CONTRACT) <= commit_time(DISPATCH)`.
  - *Differences:* Kaidoku checks static text files via `git blame --porcelain` to detect future-dated claims. Tameshi's `receipt-window.py` checks structured JSON receipts to detect in-wave instrument race conditions.
  - *Reuse verdict:* `evidence-timestamps.py` is specialized for Kaidoku's Markdown/JSON evidence trees; tameshi's `measure.py` already includes dedicated commit-time helpers (`commit_time(repo, rev, path)` using `git log -1 --format=%cI`).

### 6. `kake-shokunin`

- **Matches:**
  - `kake-shokunin/corpus/QUALITY.md:103–106`:
    > "A count that repeats the instrument's own declared total is not evidence. An unmeasurable baseline (instrument not validated) exits nonzero, never with the 'proven absent' code."
  - `kake-shokunin/corpus/QUALITY.md:128–131`:
    > "A receipt that names a disposable runner path (`/tmp/...`) must carry the command that recreates the runner from Git (e.g. `git show <commit>:<path>`); a tmpfs path alone is not evidence. Round 22's runners are recorded in `.ufo/waves/round-22/postfix/REPRODUCE.md`."
  - `kake-shokunin/corpus/QUALITY.md:148–151`:
    > "A live-page receipt states what it proves: the policy result of the bytes served at `fetchedAt`."
  - `kake-shokunin/corpus/lessons/round-22-verifier-spotcheck.md:51, 67`:
    - Verifier re-checks `PINNED_INSTRUMENT_SHA256` for `matrix.py` and `cases.json` (stub matrix rejected before rows are read).
- **Duplication vs Reuse:**
  - *Duplicate:* Hardcoded `PINNED_INSTRUMENT_SHA256` constants in the counter script.
  - *Differences:* Kake embeds the hash constant directly in the Python source code. Tameshi parameterizes instrument hashes in `contract.json` (`frozen_sha256` and `installed_sha256`), providing clean separation between the gate engine and the round's declared contract.
  - *Reuse verdict:* Tameshi's contract-driven architecture is superior; hardcoding hashes into `receipt-window.py` would violate the round-agnostic design of tools.

### 7. `souji-shokunin`

- **Matches:**
  - `souji-shokunin/corpus/QUALITY.md:30` (Criterion Q6):
    > "Q6 | A certification or tool verdict names the sha256 of the bytes it measured, and that digest equals the installed file; each certifier writes its own fragment (no shared writable relay); the candidate-selection rule exercises the class under test."
  - `souji-shokunin/corpus/QUALITY.md:80` (Criterion Q31):
    > "pointers in committed notes/lessons resolve to committed objects; a receipt written after the measured commit is cited from the next round only."
  - `souji-shokunin/corpus/QUALITY.md:100` (Criterion Q41):
    > "Safety API changes include a clean consumer cutover... Never rewrite filed evidence, suppress the real guard error or relax the oracle merely to get green."
- **Duplication vs Reuse:**
  - *Duplicate:* Q6 mandates that verdicts name the sha256 of measured bytes and match the installed file. Q41 forbids rewriting filed evidence.
  - *Differences:* Souji does not gate execution time windows or staging intervals.

### 8. `kasegi-shokunin`

- **Matches:**
  - `kasegi-shokunin/corpus/QUALITY.md:37` (Rule R3):
    > "R3 | An instrument verdict names its matcher and definition; 'frozen' names both byte inputs and the filesystem definition, and replays publish every divergent definition."
  - `kasegi-shokunin/corpus/QUALITY.md:49` (Rule R7):
    > "R7 | Freeze an axis claim against its registered detector before implementation. A provenance/header count cannot stand in for citation resolution; instrument-correctness claims must change and exercise the actual detector..."
- **Duplication vs Reuse:**
  - *Duplicate:* Emphasizes freezing detectors and byte inputs prior to implementation.
  - *Differences:* Procedural rule without an executable interval verification gate.

### 9. `game-dev-2d-shokunin`

- **Matches:**
  - `game-dev-2d-shokunin/corpus/QUALITY.md:20` (Criterion Q8):
    > "Q8 | serial-only receipts. Admission evidence comes from serial battery runs, never concurrent launches; check for one receipt dir per run and no second battery overlapping it."
  - `game-dev-2d-shokunin/corpus/QUALITY.md:21` (Criterion Q9):
    > "Q9 | committed bytes. The verdict cites the blob SHA it ran, landings are additive for evidence (no prior CASES expected string changes — harness code may change, pinned strings may not), and a post-commit replay writes a new unique receipt instead of overwriting the committed one..."
- **Duplication vs Reuse:**
  - *Duplicate:* Q9 enforces that the verdict cites the blob SHA it ran.
  - *Differences:* Q8 deals with concurrency hazards by banning concurrent launches entirely ("serial-only receipts"). In tameshi's multi-agent swarm architecture (hyaku waves with 100+ seats), serial execution is impossible. Tameshi's staging + interval validation enables safe concurrency without restricting execution to serial runs.

### 10. `game-dev-3d-shokunin`

- **Matches:**
  - `game-dev-3d-shokunin/corpus/QUALITY.md:20` (Criterion Q9):
    > "Q9 | A verifier or falsification result names the exact target SHA-256; gate admission also includes an adversary suite whose expected detections run against those same bytes."
  - `game-dev-3d-shokunin/corpus/QUALITY.md:24` (Criterion Q13):
    > "Q13 | Battery inputs run from a write-isolated snapshot with before/after seed digests; concurrent seed mutation is infrastructure failure, not a row verdict."
- **Duplication vs Reuse:**
  - *Duplicate:* Q13 explicitly identifies "concurrent seed mutation is infrastructure failure" and requires isolated snapshots.
  - *Differences:* Addresses test fixtures and seeds rather than the measuring instrument itself.

### 11. Sibling Lanes with Zero Matches (Explicitly Scanned)

The following sibling lanes were systematically scanned across their `corpus/QUALITY.md` and `corpus/lessons/round-*-verifier-spotcheck.md` files:
- `audio-shokunin`: Focuses on audio measurement, FFT/Truepeak filtering, and non-author rechecks.
- `chousa-shokunin`: Focuses on research citations, primary sources, and research-gate shell digests.
- `kagi-shokunin`: Focuses on secrets/vault commands and host-gate authorizations.
- `kama-shokunin`: Focuses on model-serving endpoints, error envelopes, and snapshot manifests.
- `kotoba-shokunin`: Focuses on promptcraft, input-class controls, and fleet-root identity separation.
- `kotodama-shokunin`: Focuses on linguistic/mythological consistency and world-bible sourcing.
- `kumitate-shokunin`: Focuses on orchestration tooling, step schemas, and build dependencies.
- `lore-shokunin`: Focuses on world-bible encoding, prior-art sweeps, and sealed-reader receipts.
- `revenger-shokunin`: Focuses on REA Evidence-ID derivation and decompilation fidelity.
- `tsukuroi-shokunin`: Focuses on host-operability, update gates, and cross-lane provenance citations.

None of these 10 lanes contain receipt-window or measurement-interval rules.

---

## 4. UFO-FSD Connector Move: Compatible Synthesis Proposal

### Evidence & Contradiction Observed

1. **The Identity Case in `stage/receipt-window.py` (lines 184–188):**
   ```python
   name, role = contract["index"][sha]
   if role == "identity" or name not in contract["windows"]:
       infos.append({"id": "INSTALL_IDENTITY", "receipt": rid,
                     "detail": f"{name}: frozen and installed bytes are identical"})
       continue
   ```
   When `frozen_sha256 == installed_sha256` (which is true in Round 20 for both `receipt-window.py` and `measure.py`, because staged instruments are frozen before dispatch and installed byte-identically post-wave), the gate records `INSTALL_IDENTITY` and skips all window checks. It verifies that `measurement_interval.start <= measurement_interval.end`, but does **not** verify whether `measurement_interval.start >= contract.frozen_at`.
2. **Sibling Precedent (Kengaku R7 & Kaidoku Q23):**
   - Kengaku Rule R7 requires: `FROZEN: timestamp < request_ts`. Any receipt generated prior to the freeze timestamp is marked `unscored` and cannot count toward coverage.
   - Kaidoku Criterion 23 requires: `evidence_timestamp <= committer_time (%cI)`. Receipts cannot claim timestamps later than the commit introducing them.
3. **The Subtle Race / Leak Surface:**
   Under tameshi's current `stage/receipt-window.py`, if a seat accidentally or maliciously submitted a receipt produced during pre-round drafting (before `contract.frozen_at`), and the instrument bytes happened to be unchanged, the gate would accept the receipt under `INSTALL_IDENTITY`. This violates the contract intent: *receipts must be produced during the wave under the frozen contract, not predating it*.

### Proposed Move

**Synthesize Kengaku R7 and Kaidoku Q23 into Tameshi's Receipt Validation:**
Add an explicit lower-bound check for non-historical receipts:
`contract.frozen_at <= receipt.measurement_interval.start`.

- For historical receipts (`sha in contract["historical"]`), this check is bypassed (lines 175–179), preserving legacy replay validity (e.g. `c1-before` and historical round-18/19 witness receipts legitimately predate round 20's `frozen_at`).
- For active/installed instruments (`role == "identity"` or `role == "frozen"` or `role == "installed"`), the receipt's `measurement_interval.start` must be `>= contract.frozen_at`.

### Affected Axes

- **Calibration (Claim C1):** Improves calibration soundness by eliminating the possibility of pre-freeze stale receipt leakage into the scored population.
- **Depth:** Preserved at 8 (tightens verification rigor without reducing test domain).
- **Substrate Integrity:** Zero harm. During wave 1, staged bytes (`stage/receipt-window.py` with sha256 `f03ae7e9...`) remain strictly frozen and unedited. This proposal is recorded for L1 integrator synthesis during the post-wave install phase or future contract iterations.

### Second-Order Effects

1. **Runtime:** Requires receipts to record aware ISO-8601 timestamps with valid UTC offsets (already required by `require_interval`).
2. **Contract Surface:** Uses `contract.frozen_at`, which is already present in `.ufo/evidence/round-20/contract.json:5` (`"2026-10-21T07:40:18Z"`). No schema change is needed.
3. **Substrate & Integrity:** Does not require running git subprocesses inside `receipt-window.py`; `frozen_at` is read directly from the parsed `contract.json`.
4. **Verification Surface:** Historical receipts in `.ufo/evidence/round-20/final/historical-receipts.json` are already filtered by `sha in contract["historical"]` before this check, ensuring zero false rejections on historical replays.

### Risks & Verification

- **Risk:** Timezone offset parsing errors between local BRT (UTC-03:00) and UTC.
  - *Mitigation:* `receipt-window.py`'s `parse_ts()` already normalizes `"Z"` to `"+00:00"` and parses via `datetime.fromisoformat()`, ensuring proper aware datetime comparison across all valid ISO-8601 representations.
- **Verification on Committed Round-20 Bytes:**
  - Contract `frozen_at` = `2026-10-21T07:40:18+00:00`.
  - All wave-1 executor receipts have measurement intervals starting after `07:40:18Z`.
  - Historical receipts are classified under `contract.historical` and remain green.

---

## 5. Agreed / Disagreed Points & Defects

- **Agree with Tameshi Contract & Architecture:**
  - Agree that staging instrument bytes before dispatch (`.ufo/evidence/round-20/stage/`) and installing them byte-identically post-wave (`tools/receipt-window.py`) definitively closes the QUALITY20 in-place mutation recurrence.
  - Agree that keeping `stage/receipt-window.py` hermetic (evaluating `contract.json` + `receipts.json` without git subprocesses) is strictly superior to `mado`'s git-dependent `receipt-check.py`.
- **Agree with Sibling Precedents:**
  - Agree with `tabi` Criterion 30: historical receipts must be indexed as history and never rewritten.
  - Agree with `kengaku` Rule R7: trials predating the contract freeze must not be credited.
- **Defects Observed:**
  - **Minor Nomenclature Mismatch:** In `.ufo/evidence/round-20/contract.json` line 27, the instrument metadata defines `"install_window": {"start": "...", "end": "..."}`, whereas `stage/receipt-window.py` line 89 checks for `"edit_interval"`. For identity instruments (`frozen == installed`), this branch is skipped, so no failure occurs. However, if frozen and installed shas were ever different, line 89 would raise `ContractError("...differs frozen/installed and needs edit_interval")`. The contract should use the key `"edit_interval"`.

---

## 6. Commands and Observed Outputs

The following read-only commands were executed to gather and verify evidence:

1. **Scan `corpus/QUALITY.md` across all sibling lanes:**
   - Command: `functions.glob(path="/home/vgpnk/Projects/shokunin/*-shokunin/corpus/QUALITY.md", gitignore=False)`
   - Output: 21 files matched across all 20 sibling lanes plus tameshi.
2. **Scan `round-*-verifier-spotcheck.md` across all sibling lanes:**
   - Command: `functions.glob(path="/home/vgpnk/Projects/shokunin/*-shokunin/corpus/lessons/round-*-verifier-spotcheck.md", gitignore=False)`
   - Output: Found verifier spotchecks in `kumitate`, `souji`, `tsukuroi`, `kaidoku`, `mado`, `mori`, `tameshi`, `kama`, `kake`, `kagi`, `tabi`, `kengaku`, `audio`, `game-dev-2d`, `kotodama`, `kotoba`, `lore`, `kasegi`, `game-dev-3d`, `revenger`, `chousa`.
3. **Targeted grep for receipt, instrument, interval across `QUALITY.md`:**
   - Command: `functions.grep(path="/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md;...", pattern="receipt|instrument|interval|tool_sha256", gitignore=False)`
   - Output: Identified Criterion 24 in `mado`, Criterion 33 & 58 in `mori`, Rule R7 in `kengaku`, Criterion 19 & 23 in `kaidoku`, Criterion 26 & 30 in `tabi`, Criterion Q6 in `souji`, Criterion Q9 in `game-dev-2d`.
4. **Verify `mado` receipt-check tool:**
   - Command: `functions.read(path="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/receipt-check.py:1-45")`
   - Output: Extracted full specification of mado's tool sha and commit ancestry checker.
5. **Verify `kaidoku` evidence-timestamps tool:**
   - Command: `functions.read(path="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py:1-40")`
   - Output: Verified regex and git blame committer-time validation.
6. **Verify `tameshi` staged gate implementation:**
   - Command: `functions.read(path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py:134-200")`
   - Output: Verified check loop, interval validation, identity bypass, and historical classification.

---

## 7. Tooling Directive Record

In compliance with the operator tooling directive (2026-10-19):
- **Host `pacman`:** PAUSED host-wide. No pacman commands executed.
- **Tool Installs / Updates:** Zero tools were installed, updated, or removed.
- **Channel / Version / Reason:** None. All scans utilized existing Python 3 stdlib and harness tools.
- **Write Scope:** Exactly one file written: this report at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/w1/F01SiblingReceipts.md`. Sibling lanes and production code were accessed read-only.
