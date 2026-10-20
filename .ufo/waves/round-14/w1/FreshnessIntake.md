# FreshnessIntake — round 14 w1

Seat: `TameshiR14.FreshnessIntake` (scout, leaf; no subagent dispatch).
Target: Inspect existing service opt-in and current successor evidence for `kimi` (`kumitate-shokunin`), `tsukuroi` (`tsukuroi-shokunin`), and `mado` (`mado-shokunin`) starting from latest `SCORECARD.md` planned freshness successor request.
Method: Read-only static inspection of sibling repositories (`kumitate-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`), historical pins, defect specs in `tools/mutate-and-run.sh`, `corpus/knowledge/service-optin-protocol.md`, `corpus/knowledge/service-limits.md`, and `corpus/knowledge/fleet-kill-rate-ledger.md`. In-memory string matching and SHA-256 analysis only.
Sibling gate runs: **0**. Sibling file mutations: **0**. Host/toolchain modifications: **0**.
State at intake time: Baseline `d6809df7775338f000e44c8a916067b8866867fb`; `claims.json` explicitly pins guardrail `"freshness successor sweep not preclaimed"`.

---

## 1. Named Axes (Godspeed Framing)

Per `AXES.md` and `SCORECARD.md`:

| Axis | Posture / Status in this Inspection |
|---|---|
| **freshness** | **Refusal issued; honesty preserved.** Stale-successor ledger debt remains open and accurately attributed; no ungrounded successor sweep is fabricated or pre-claimed without an owner opt-in and runnable mapped spec. Readiness refusal only is cited. |
| **calibration** | **Readiness refusal / fail-closed intake.** Enforces fail-closed intake rules (`service-limits.md` rows a, b, c): rejects missing opt-ins, non-unique `@old` anchors (9/10 duplicate on mado, 1/10 missing on kimi), and dirty working trees. (Note: Main cites readiness refusal only; no scalar score increase claimed.) |
| **depth** | **Preserved.** Six recorded cases in `tools/mutate-and-run.sh` remain six; no fake or partial successor case added. |
| **operability** | **Harm-free.** Zero execution overhead, zero sibling workspace interference, zero drift imposed on live repos. |
| **coverage** | **Boundary maintained.** Re-sweep queue remains an offer, not an ungrounded mandate; boundaries of self-service vs. service mode remain clear. |
| **adjacency** | **Strict adherence.** `PROVINCE.md:16-18` strictly respected: tameshi never mutates or executes sibling gates without explicit protocol contract. |

---

## 2. Intake Baseline & Contract Grounding

In `SCORECARD.md` (lines 391–395):
> *"Next intended claim: freshness — prepare one owner-opted-in successor sweep at an actual current pinned revision (kimi now joins tsukuroi/mado debt), including explicit spec remapping and a retained run, or an honest intake refusal. This is a plan, not an execution or future round claim."*

Under `service-optin-protocol.md` (§0–§1) and `service-limits.md` (§1), a mutation sweep operates under strict intake criteria:
1. **Request shape (§1):** Pinned revision (sha256, byte count, newline count, mtime, porcelain-clean tree at open); one-command hermetic suite invocable against a copy (`bash "$MUTANT" --selftest`); clause-mapped defect spec with pre-registered expectations and unique `@old` anchors (`count == 1`).
2. **Refusal trigger (Row a):** *"a gate with no opt-in and no pinned revision: no lane names the gate; or a request arrives without committed bytes ... no sweep; the queue is an offer, not a schedule; ... a round with no opt-in records the no-opt-in line as its complete outcome."*
3. **Refusal trigger (Row b):** *"a gate with no one-command hermetic suite (and no runnable spec): the suite cannot run against a copy ... or an `@old` is not unique; refused before any suite runs — `MUTATE: SETUP (<reason>)`, exit 2, no headline."*
4. **Refusal trigger (Row c):** *"a moved substrate held to the old table: stale (the recorded revision no longer names the live bytes) or drift (worktree differs from HEAD) -> a re-pin, never a re-interpretation ... a dirty tree waits for the commit."*

---

## 3. Candidate-by-Candidate Findings (READ-ONLY)

### Candidate 1: `kimi` (`kumitate-shokunin/scripts/kimi-census.mjs`, leg `js-kimi-census`)

- **Historical Pinned Revision:**
  - Commit: `175de6ba2e9e904010411b19cab27e0af9aad3d4`
  - Blob SHA-256: `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` (896 lines, 43,273 bytes)
- **Current Owner State (`kumitate-shokunin`):**
  - HEAD Commit: `1770305fae20826b39905a8251ddeca6b4957ac4`
  - Target Blob SHA-256: `5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0` (931 lines, 45,713 bytes)
  - Worktree: Porcelain clean (`git status --porcelain` is empty)
  - Content Status: `changed` (content modified since pin; entered freshness debt in r13 `fleet-kill-rate-ledger.md` ER-5)
- **Owner Opt-In Status:** **ABSENT.**
  - Comprehensive inspection of `kumitate-shokunin` (`LOG.md`, `SCORECARD.md`, `SKILL.md`, `.ufo/`, `corpus/`) reveals no request, issue, or plan opting into a tameshi mutation sweep.
- **Defect Spec Evaluation (Historical Spec vs. Current Live File):**
  - Evaluated all 10 defects (`D1`–`D10`) from `tools/mutate-and-run.sh` against current `kimi-census.mjs`:
    - `D1` through `D9`: `@old` unique (`count == 1`).
    - `D10`: **MISSING (`count == 0`)**.
      - Historical `@old`: `const FROZEN = { K1: 3, K2: 25, K3: 9, K4: 9, K5: 3 };`
      - Current file line 149: `const FROZEN = { K1: 3, K2: 26, K3: 9, K4: 9, K5: 3 };` (member counter K2 incremented from 25 to 26 in round 20/34).
  - [INFERENCE] Attempting to run the unmapped historical spec against the live file is predicted to fail closed at setup (`py_helper apply` would exit 2: missing match on D10; no mutation runner or suite was executed).
- **Intake Decision:** **REFUSED** under `service-limits.md` row (a) (no opt-in request) and row (b) (unrunnable spec: `@old` count != 1).

---

### Candidate 2: `tsukuroi` (`tsukuroi-shokunin/tools/tsukuroi-census.sh`, leg `bash-tsukuroi-census`)

- **Historical Pinned Revision:**
  - Commit: `165307fe4746a8807b02ec4a7d7ecac0368454a6`
  - Blob SHA-256: `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` (976 lines, 44,947 bytes)
- **Current Owner State (`tsukuroi-shokunin`):**
  - HEAD Commit: `8606bad4cbc6451ac2890c9f8e2548a36c386db6` (current HEAD; `9574a189...` observed in r13)
  - Target Blob SHA-256: `d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e` (2,642 lines, 142,572 bytes)
  - Worktree: **DIRTY** (`git status --porcelain` shows uncommitted round-14 in-flight edits to `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `corpus/`, etc.)
  - Content Status: `changed` (gate file has grown from 976 lines to 2,642 lines) and worktree is active/dirty.
- **Owner Opt-In Status:** **ABSENT (Self-Service Chosen).**
  - In `tsukuroi-shokunin/.ufo/waves/round-12/OverlapMethod.md` and `resumed/OverlapMethodR.md`:
    > *"In-Lane Mutation Testing: Permitted & Owned: Under the self-service protocol, tsukuroi may run single-defect mutant experiments on /tmp copies to verify fault-detection (e.g. MutationPlanR)... Refuses delegating product gate testing to tameshi."*
  - Tsukuroi explicitly elected self-service mode in round 5 (`tsukuroi-shokunin/plans/round-5.plan.md:3-11`) and has not submitted an opt-in for tameshi service testing.
- **Defect Spec Evaluation (Historical Spec vs. Current Live File):**
  - The historical 10 defects (`B1`–`B10`) from round 5 target anchors in the initial 976-line file.
  - While literal strings exist in the current 2,642-line file (e.g. B8 moved from line 935 to line 2,628), the file has grown by ~170%, with dozens of new CLI options, functions, and arms not represented in the historical 10-defect spec.
  - No current clause-mapped defect spec covering the expanded gate has been authored or mapped by the owner.
  - `service-limits.md` row (c) explicitly dictates: *"a dirty tree waits for the commit"*.
- **Intake Decision:** **REFUSED** under `service-limits.md` row (a) (no opt-in request), row (c) (unpinned moved substrate with active dirty tree), and `service-optin-protocol.md` §0.

---

### Candidate 3: `mado` (`mado-shokunin/tools/mado-verify.sh`, leg `bash-mado-verify`)

- **Historical Pinned Revision:**
  - Commit: `eead56b20ad2b28299ae4fa623d52a99b44c743c`
  - Blob SHA-256: `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` (1,098 lines, 45,334 bytes)
- **Current Owner State (`mado-shokunin`):**
  - HEAD Commit: `97c35835da3702df2f397d5c70ac6b1d871f012d`
  - Target Blob SHA-256: `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` (2,736 lines, 126,827 bytes; moved from `037b05dc...` in r13)
  - Worktree: Porcelain clean (`git status --porcelain` is empty)
  - Content Status: `changed` (stale pin, moved substrate)
- **Owner Opt-In Status:** **ABSENT (Self-Service Executed).**
  - Inspection of `mado-shokunin` round 14 artifacts (`.ufo/waves/round-14/evidence/`) shows that mado runs its own in-lane recut and mutation testing (`mado-r14-recut-0blumi29`, `regular-target.spec`, `covering.spec`, `historical`) using `tameshi-shokunin/tools/mutate-and-run.sh` directly as a read-only tool in private `/tmp` workspaces.
  - Mado has not opted into a tameshi-managed successor sweep.
- **Defect Spec Evaluation (Historical Spec vs. Current Live File):**
  - Evaluated the 10 defects (`D1`–`D9`, `R1`) from `tools/mutate-and-run.sh` against current `mado-verify.sh` (2,736 lines):
    - `D1`: **count = 2** (`MADO_VERIFY: CLEAN (%s pass...`)
    - `D2`: **count = 2** (`if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then`)
    - `D3`: **count = 2** (`row hypr-live live.plane SKIP...`)
    - `D4`: **count = 1** (unique)
    - `D5`: **count = 48** (`return 2` occurs in dozens of selftest cases)
    - `D6`: **count = 2** (`(hyprland bindings input monitors looknfeel...`)
    - `D7`: **count = 2** (`if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then`)
    - `D8`: **count = 2** (`if [ "$sha" = "4f52854a3c14" ]; then`)
    - `D9`: **count = 2** (`if [ "$after" = "$before" ]; then`)
    - `R1`: **count = 2** (`row walker walker.config UNKNOWN...`)
  - **Summary:** Only **1 of 10** `@old` anchors is unique (`D4`). The other **9 of 10** defects fail with duplicate matches (`count == 2` or `count == 48`).
  - **Root Cause:** In expanding `mado-verify.sh`, mado embedded its own stub and regression verification machinery directly into the script, including comments and tests that cite the exact historical anchor strings verbatim.
  - [INFERENCE] Attempting to run this spec is predicted to fail closed at `py_helper apply` with `SETUP` exit 2 (duplicate `@old` match on 9/10 defects; no mutation runner or suite was executed).
- **Intake Decision:** **REFUSED** under `service-limits.md` row (a) (no opt-in request), row (b) (unrunnable spec: 9/10 defects violate `count == 1`), and row (c) (moved substrate held to old table).

---

## 4. Bounded Honest Intake Refusal Summary

| Candidate Target | Owner Opt-in Present? | Current Pinned Bytes? | Runnable Mapped Spec? | Exact Intake Verdict | Applicable Failure Rule |
|---|---|---|---|---|---|
| **kimi** (`kumitate-shokunin/scripts/kimi-census.mjs`) | **No** (none filed) | Committed HEAD clean (`5e8d5913...`, 931 L) | **No** (D10 `@old` count=0; K2 bumped 25→26) | **REFUSED** | `service-limits.md` Row a (no opt-in) + Row b (missing anchor D10) |
| **tsukuroi** (`tsukuroi-shokunin/tools/tsukuroi-census.sh`) | **No** (self-service elected) | Uncommitted / Dirty (`d17d32a3...`, 2,642 L) | **No** (spec unmapped to 2,642-line gate expansion) | **REFUSED** | `service-limits.md` Row a (no opt-in) + Row c (dirty worktree / unpinned) |
| **mado** (`mado-shokunin/tools/mado-verify.sh`) | **No** (self-service in round 14) | Committed HEAD clean (`fba82a66...`, 2,736 L) | **No** (9/10 defects non-unique: count=2 or 48) | **REFUSED** | `service-limits.md` Row a (no opt-in) + Row b (duplicate anchors D1-D3, D5-D9, R1) |

### Exact Missing Prerequisites Required Before Any Successor Sweep Can Run:

1. **Owner-Authored Request:** An explicit service opt-in filed by the owner lane in its own plan/log per `service-optin-protocol.md` §1 template (mode: service, target path, committed SHA-256, byte count, line count, mtime, and porcelain-clean tree assertion).
2. **Current-Revision Spec Mapping:** An owner-curated, clause-mapped defect spec where every `@old` string occurs **exactly once** (`count == 1`) in the current version of the target file, with pre-registered `killed` or `survived` expectations for each defect.
3. **Hermetic Suite Verification:** Explicit confirmation that the suite executes hermetically on a `/tmp` copy without accessing live host/session resources (`the-janitor`, running Hyprland compositor, live pacman database, etc.).
4. **Stable Repository Worktree:** For `tsukuroi-shokunin`, all concurrent round work must be committed and tree porcelain-clean before opening a measurement window.

---

## 5. Concrete Changes, Risks & Mitigations

- **Concrete Changes Made by this Seat:**
  - Written this report at `.ufo/waves/round-14/w1/FreshnessIntake.md`.
  - Zero modifications to sibling repositories (`kumitate-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`).
  - Zero modifications to shared lane files (`LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`).
- **Risks Identified:**
  - *Risk 1 (Premature Sweep Execution):* Running `mutate-and-run.sh` against the live sibling files with historical specs would fail with exit code 2 (`SETUP`), creating noise, or worse, modifying `/tmp` environments improperly.
    - *Mitigation:* Bounded refusal halts execution before any mutation harness or test suite is invoked.
  - *Risk 2 (Preclaiming Successor Coverage):* Claiming freshness progress without valid sweeps would violate `claims.json` guardrails and `QUALITY.md` criterion 14.
    - *Mitigation:* Freshness axis is honestly marked unadvanced; stale-successor debt remains recorded debt in `fleet-kill-rate-ledger.md`.
  - *Risk 3 (Province Overreach):* Attempting to "fix" or re-map defect specs for sibling gates without owner input violates `PROVINCE.md:14-18`.
    - *Mitigation:* Remapping is declared an owner prerequisite, preserving province boundaries.

---

## 6. Checks L1 Should Run (After All Seats Finish)

1. Verify that `FreshnessIntake.md` is present at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-14/w1/FreshnessIntake.md`.
2. Confirm that no sibling repositories were altered:
   ```sh
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin status --porcelain
   git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain
   ```
   (Both must show zero changes authored by tameshi).
3. Confirm that no files in `tameshi-shokunin` outside the designated wave report were mutated by this seat:
   ```sh
   git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain .ufo/evidence/round-12 .ufo/evidence/round-13 tools/
   ```
   (Must be clean).
4. Verify that `claims.json` guardrail `"freshness successor sweep not preclaimed"` holds true.

---

## 7. Bounded Observation Methodology & In-Memory Verification Receipts

### 7.1 Bounded Search Queries and Path Sweeps Supporting 'No Opt-in Found'

Observations are strictly bound to the specific files, revisions, and search queries executed below. This report makes **no claim of unanchored global absence** across unread files or unrecorded branches.

1. **`kumitate-shokunin`** (Commit `1770305fae20826b39905a8251ddeca6b4957ac4`, worktree clean):
   - **Bounded queries executed:**
     - Query A: `rg -i "tameshi|opt[- ]in|mutate[- ]and[- ]run" /home/vgpnk/Projects/shokunin/kumitate-shokunin`
     - Query B: `rg "kimi-census" /home/vgpnk/Projects/shokunin/kumitate-shokunin/LOG.md /home/vgpnk/Projects/shokunin/kumitate-shokunin/SCORECARD.md /home/vgpnk/Projects/shokunin/kumitate-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/`
   - **Observed hits:**
     - Query A returned **0 matches** across the entire repository.
     - Query B returned 54 matches, all strictly concerning internal member-census operations, selftest assertions (43 → 45), and residue tracking (e.g. K2 frozen member count bumped from 25 to 26).
     - **Result:** 0 opt-in requests to tameshi for a service sweep exist in the scanned files.

2. **`tsukuroi-shokunin`** (Commit `8606bad4cbc6451ac2890c9f8e2548a36c386db6`, worktree dirty with round-14 in-flight files):
   - **Bounded queries executed:**
     - Query: `rg -i "tameshi|opt[- ]in|mutate[- ]and[- ]run" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
   - **Observed hits:**
     - Returned matches in `.ufo/evidence/fleet-r1-interactive/parent-review.md:17`, `.ufo/waves/fleet-r1-interactive/`, `.ufo/waves/round-12/OverlapMethod.md:52`, and `.ufo/waves/round-12/resumed/OverlapMethodR.md:18, 82`.
     - Explicit declarations found:
       - *"In-Lane Mutation Testing: Permitted & Owned: Under the self-service protocol, tsukuroi may run single-defect mutant experiments on /tmp copies... Refuses delegating product gate testing to tameshi."* (`OverlapMethod.md:56`)
       - Historical reference to self-service round 5 (`tsukuroi-shokunin/plans/round-5.plan.md:3-11`).
     - **Result:** Tsukuroi explicitly asserts the self-service model for its gate. 0 service opt-in requests to tameshi exist in the scanned files.

3. **`mado-shokunin`** (Commit `97c35835da3702df2f397d5c70ac6b1d871f012d`, worktree clean):
   - **Bounded queries executed:**
     - Query A: `rg -i "tameshi|opt[- ]in|mutate[- ]and[- ]run" /home/vgpnk/Projects/shokunin/mado-shokunin`
     - Query B: `rg -i "tameshi|opt[- ]in|mutation" /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14`
   - **Observed hits:**
     - Returned matches in `.ufo/waves/round-13/` and `.ufo/waves/round-14/` (`evidence/regression-recut.txt`, `evidence/regular-target-mutants.txt`, `frozen/gate.sh:1597-1598`).
     - Observed activity: Mado performs self-service in-lane mutation testing in private scratch (`/tmp/mado-r14-recut-0blumi29/`) invoking `tameshi-shokunin/tools/mutate-and-run.sh` directly as a read-only tool (`gate.sh:1597-1598`: *"Discipline: the harness (tameshi-shokunin/tools/mutate-and-run.sh) is consumed read-only"*).
     - **Result:** Mado manages its own in-lane defect recuts. 0 service opt-in requests to tameshi exist in the scanned files.

---

### 7.2 In-Memory Literal Count Procedure

To evaluate spec mapping without executing any mutations or sibling test suites, an in-memory literal matching procedure was executed using Python. The parser replicated the exact unescaping logic of `tools/mutate-and-run.sh` (`py_helper:unescape` handling `\n`, `\t`, `\r`, `\\` escapes) and counted occurrences of each defect's `@old` string against the live file contents via `target_text.count(d["old"])`.

**Procedure script:**
```python
import sys

ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}

def unescape(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\":
            n = s[i + 1]
            out.append(ESCAPES[n])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)

def parse_spec_text(text):
    defects = []
    cur = None
    for line in text.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@defect"):
            if cur: defects.append(cur)
            rest = line[len("@defect"):].strip()
            idpart, _, desc = rest.partition("|")
            cur = {"id": idpart.strip(), "desc": desc.strip()}
        elif line.startswith("@old"):
            cur["old"] = unescape(line[len("@old"):].lstrip(" "))
        elif line.startswith("@new"):
            cur["new"] = unescape(line[len("@new"):].lstrip(" "))
    if cur: defects.append(cur)
    return defects

with open("/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh") as f:
    runner = f.read()

kimi_spec = runner.split("cat >\"$d/js-kimi-census.spec\" <<'EOT'")[1].split("EOT")[0]
tsukuroi_spec = runner.split("cat >\"$d/bash-tsukuroi-census.spec\" <<'EOT'")[1].split("EOT")[0]
mado_spec = runner.split("cat >\"$d/bash-mado-verify.spec\" <<'EOT'")[1].split("EOT")[0]

targets = [
    ("kumitate (kimi-census.mjs)", "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs", kimi_spec),
    ("tsukuroi (tsukuroi-census.sh)", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh", tsukuroi_spec),
    ("mado (mado-verify.sh)", "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh", mado_spec),
]

for name, path, spec in targets:
    with open(path) as f:
        target_text = f.read()
    defects = parse_spec_text(spec)
    print("=== " + name + " (" + str(len(defects)) + " defects) ===")
    counts = {}
    for d in defects:
        c = target_text.count(d["old"])
        counts[d["id"]] = c
        if c != 1:
            print("  MISMATCH " + d["id"] + ": count=" + str(c) + " (expected 1)")
    unique_count = sum(1 for c in counts.values() if c == 1)
    print("  Summary: " + str(unique_count) + "/" + str(len(defects)) + " unique @old strings found")
```

---

### 7.3 Verbatim Execution Output of In-Memory Literal Counts

```text
=== kumitate (kimi-census.mjs) (10 defects) ===
  MISMATCH D10: count=0 (expected 1)
  Summary: 9/10 unique @old strings found
=== tsukuroi (tsukuroi-census.sh) (10 defects) ===
  Summary: 10/10 unique @old strings found
=== mado (mado-verify.sh) (10 defects) ===
  MISMATCH D1: count=2 (expected 1)
  MISMATCH D2: count=2 (expected 1)
  MISMATCH D3: count=2 (expected 1)
  MISMATCH D5: count=48 (expected 1)
  MISMATCH D6: count=2 (expected 1)
  MISMATCH D7: count=2 (expected 1)
  MISMATCH D8: count=2 (expected 1)
  MISMATCH D9: count=2 (expected 1)
  MISMATCH R1: count=2 (expected 1)
  Summary: 1/10 unique @old strings found
```

---

### 7.4 Explicit Distinction: Inference vs. Execution

- **Static Fact:** In-memory matching of historical defect specs against current file bytes reveals that:
  - `kimi-census.mjs` has 0 occurrences of `@old` for `D10`.
  - `mado-verify.sh` has multiple occurrences for 9 out of 10 defect `@old` anchors.
- **[INFERENCE] (Predicted Outcome):** Based on the fail-closed assertion logic implemented in `tools/mutate-and-run.sh` (`py_helper:apply` requires `target.count(old) == 1`, exiting 2 otherwise), an attempt to run the historical defect specs against the live target files without remapping is **predicted to fail closed at setup**.
- **Execution Truth:** **Zero mutation runs, zero test suites, and zero sibling gates were executed.** No code was executed against live sibling repos.

---

### 7.5 Integration Citation Bound

Main integration will cite **readiness refusal only** (under `service-limits.md` rows a, b, c), and will not cite an axis-improved assertion. Bounded honesty is maintained; stale-successor debt remains open in `fleet-kill-rate-ledger.md`.

