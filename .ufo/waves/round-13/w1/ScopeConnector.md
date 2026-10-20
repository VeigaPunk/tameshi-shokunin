# ScopeConnector — Round 13 Wave 1 Report: Sibling Boundary & F7 Disposition Protocol

**Seat:** `TameshiR13.ScopeConnector` (connector, leaf).  
**Baseline:** `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`.  
**Scope:** Read-only connector scanning sibling overlap for F7 content disposition versus sibling gate ownership; reporting exact boundaries, preventing domain takeover, and providing grounded integration recommendations without claiming verdict authority.  
**Tooling Record:** Zero tools installed or updated (standard pre-installed host toolchain used exclusively).

---

## 1. Declared Axes & Posture (Godspeed)

- **Depth ($C_1$): 6 → 6.** Grounding the six recorded mutation legs in explicit git blob, commit, and worktree content disposition records (`tools/pin-disposition.py` + `.ufo/evidence/round-13/pin-manifest.json`) without claiming a seventh gate or inflating the depth scalar.
- **Calibration ($C_2$): 6 → 6.** Enforcing that identical target content does **not** establish safe result reuse (`result_reuse = "not_established"` across all six rows); preventing attribution errors that conflate file-hash matching with live gate validity; repairing routed metadata via companion evidence without altering historical frozen files.
- **Harm Check Across Other Axes:**
  - *Adjacency & Province:* Preserves strict boundary separation (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md`). Sibling gates remain under full owner-lane jurisdiction; tameshi provides reusable verification craft and recommendations only.
  - *Freshness:* Prevents papering over staleness debt (`corpus/README.md ## Known gaps`). Changed legs (`tsukuroi-census`, `mado-verify`, `kimi-census`) are observed as `changed`; no unilateral re-sweep or freshness claim is made without owner opt-in.
  - *Operability & Non-Interference:* Zero modification to sibling repositories; zero execution of sibling gate binaries or suites.

---

## 2. Evidence: Grounded Scan of Sibling Overlap & Current Substrate

The six recorded mutation legs belong to four distinct sibling repositories across the fleet. Read-only inspection of git object databases and worktree files reveals the following grounded facts:

| Leg Name | Owning Sibling Repo | Target Relative Path | Pinned Rev / Blob SHA-256 | Current Committed HEAD (Rev / Blob SHA-256) | Worktree SHA-256 & Status | Content Status | Result Reuse | Primary Context Blindness |
|---|---|---|---|---|---|---|---|---|
| `js-kimi-census` | `kumitate-shokunin` | `scripts/kimi-census.mjs` | `175de6ba…` / `83016d45…` | `1770305f…` / `5e8d5913…` | `5e8d5913…` (Clean) | **`changed`** | `not_established` | Probes live `~/.kimi-code` tree; K1–K5 member rules; mode pins |
| `bash-surface-census` | `kagi-shokunin` | `corpus/surface-census.sh` | `fecee874…` / `275d8294…` | `c2cab35b…` / `275d8294…` | `275d8294…` (Clean) | **`unchanged`** | `not_established` | Sibling TSVs (`surface-census.tsv`, `state-shape.tsv`); `sqlite3`; `the-janitor` |
| `bash-tsukuroi-census` | `tsukuroi-shokunin` | `tools/tsukuroi-census.sh` | `165307fe…` / `084951be…` | `9574a189…` / `d17d32a3…` | `d17d32a3…` (Clean) | **`changed`** | `not_established` | Expanded 976 → 2,679 lines (4 → 6 planes: update-safety, oom); host systemd/kernel |
| `bash-mado-verify` | `mado-shokunin` | `tools/mado-verify.sh` | `eead56b2…` / `d7edaab4…` | `95cbc41f…` / `037b05dc…` | `037b05dc…` (Clean) | **`changed`** | `not_established` | Expanded 1,098 → 3,458 lines; python `tomllib`; Hyprland compositor socket |
| `bash-checklist-run` | `kagi-shokunin` | `corpus/checklist-run.sh` | `fecee874…` / `7e5ec98b…` | `c2cab35b…` / `7e5ec98b…` | `7e5ec98b…` (Clean) | **`unchanged`** | `not_established` | Selftest synthetic fixtures vs production `checklist.tsv`; delegated corpus scripts |
| `js-claims-check` | `kumitate-shokunin` | `scripts/claims-check.mjs` | `175de6ba…` / `e9a21b44…` | `1770305f…` / `e9a21b44…` | `e9a21b44…` (Clean) | **`unchanged`** | `not_established` | Sandboxed mock trees in `--selftest` vs live `$UFO_SRC` origin tree resolution |

### Key Observations
1. **Three Unchanged Targets vs Three Changed Targets:**
   - Exact byte identity holds for `bash-surface-census`, `bash-checklist-run`, and `js-claims-check`. In all three cases, the sibling repo HEAD advanced (by 18–27 commits), but the target files were untouched.
   - Extensive drift occurred in `js-kimi-census`, `bash-tsukuroi-census` (+1,702 lines), and `bash-mado-verify` (+2,360 lines).
2. **Availability of Original Bytes:**
   - In all six cases, the original recorded bytes remain 100% available in the sibling git object stores and can be materialized via `git show <rev>:<path>`.
3. **Execution Permissions:**
   - Legs 2–6 carry mode `100755` (`-rwxr-xr-x`); leg 1 carries `100644`. Preserving the executable bit upon materialization is mandatory for legs whose selftests re-invoke `"$SELF"` (e.g. `checklist-run.sh`).

---

## 3. Boundary Definition: Tameshi Province vs Sibling Gate Ownership

To prevent domain takeover, the exact boundary between `tameshi-shokunin` and the sibling lanes must be maintained:

### What Tameshi Owns (`PROVINCE.md ## Domain / ## Owns`)
- **The Reusable Method:** The craft of honest verification fixtures, mutation sweeps, fail-closed assertions, and before/after proofs.
- **The Standing Ledger of Recorded Cases:** Maintaining immutable historical receipts of measured legs, their pinned revisions, defect specs, and observed tables.
- **Probe Instruments:** Tooling that performs read-only inspection of fleet baselines and content drift (`pin-disposition.py`).
- **The Service Opt-in Protocol:** The published contract under which a sibling lane may request an authorized mutation sweep (`corpus/knowledge/service-optin-protocol.md`).

### What Tameshi Refuses / Sibling Domain Authority (`PROVINCE.md ## Refuses / ## Adjacent`)
- **Product Clauses & Gate Implementation:** Every sibling owns its gate's source code, internal logic, exit semantics, and selftest suites. Tameshi **never** edits sibling gate code (`PROVINCE.md:16-18`).
- **Live Gate Verdicts:** Tameshi does **not** assert whether a sibling gate currently passes or fails in production, nor does it assert live kill rates for drifted gates.
- **Unilateral Re-Sweeping:** Tameshi cannot re-sweep a sibling gate without an explicit opt-in request defining pinned bytes and hermetic suites.
- **Domain Takeover via Disposition:** A content disposition probe is strictly a measurement of artifact drift against a recorded baseline; it is **never** an admission, certification, or invalidation of the sibling gate's live correctness.

---

## 4. Analysis of Boundary Hazards

1. **Hazard 1: Conflating Content Matching with Safe Result Reuse (Attribution Error).**  
   *Risk:* Inferring that because `bash-surface-census.sh`, `bash-checklist-run.sh`, or `scripts/claims-check.mjs` has an identical SHA-256, its historical mutation kill rate (80%, 47%, 70%) automatically holds today.  
   *Counter-Grounding:* As established by reopened sources S003 (StrykerJS) and S041 (PIT), incremental analysis blind spots (dependencies, environment, external tables) make verdict reuse an unproven inference. In `surface-census.sh`, sibling TSV tables govern the rules; in `checklist-run.sh`, selftest exercises synthetic fixtures rather than production checklists; in `claims-check.mjs`, live execution resolves `$UFO_SRC`. `result_reuse` must remain `not_established`.

2. **Hazard 2: Sibling Gate Execution During Disposition Probes (Contract Violation).**  
   *Risk:* A probe script attempting to run `bash <target> --selftest` or `node <target> --selftest` inside sibling checkouts.  
   *Counter-Grounding:* `tools/pin-disposition.py` must perform strictly static reads: read-only git queries (`cat-file`, `show`, `rev-parse`) and filesystem hashing (`open(..., 'rb')`). It must never execute sibling code.

3. **Hazard 3: Subprocess Git Traversal to Fleet Root (Security & Scope Leak).**  
   *Risk:* As identified by `PinGit`, running `git -C <path>` when `<path>` is not a git repository silently causes git to discover the enclosing fleet root `/home/vgpnk/Projects/shokunin` (HEAD `a53aad8`), resolving wrong commits and blobs.  
   *Counter-Grounding:* `pin-disposition.py` must assert that `git -C <repo> rev-parse --show-toplevel` resolves strictly to the target repository directory.

4. **Hazard 4: Masking Sibling Freshness Debt (Calibration Inflation).**  
   *Risk:* Treating a content disposition check as resolving the standing "stale ledger successors" debt for `tsukuroi-census` and `mado-verify` (`corpus/README.md ## Known gaps`).  
   *Counter-Grounding:* A pin disposition notes that content is `changed`. Resolving freshness debt requires a full calibrated re-sweep under an owner opt-in. The debt remains documented and open.

---

## 5. The Proposed Move: The 4-Layer Sibling Boundary Protocol for F7 Dispositions

Synthesizing findings across `PinSchema`, `PinGit`, `PinSelftest`, `ReuseCritic`, `FreshnessCritic`, `ScoreRestraint`, and the six scout reports, this report proposes the **F7 Read-Only Sibling Boundary Invariant**:

### Layer 1: Epistemic Decoupling (Observation vs Verdict)
`tools/pin-disposition.py` and `.ufo/evidence/round-13/pin-manifest.json` record only physical artifact disposition:
- `content_status ∈ {unchanged, changed, unavailable}`
- `target_dirty ∈ {true, false}`
- `result_reuse = "not_established"` (invariant on all 6 rows).  
No live kill rate or verdict projection is emitted.

### Layer 2: Hermetic Subprocess Containment
All interactions with sibling repositories in `tools/pin-disposition.py` must enforce:
1. **Top-Level Identity Check:** Validate `git -C <repo> rev-parse --show-toplevel == <repo>` before querying objects.
2. **Plumbing Commands Only:** Use `rev-parse --verify`, `cat-file -e`, `cat-file -t`, and `show <rev>:<path>` with `--end-of-options`.
3. **Environment Sanitization:** Strip `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and `GIT_OBJECT_DIRECTORY` from subprocess calls.
4. **Read-Only File Access:** Worktree comparison reads raw bytes via standard library file I/O; no temporary files written to sibling trees.

### Layer 3: Zero-Execution Policy
Under no circumstances may `tools/pin-disposition.py` invoke `node`, `bash`, or Python against sibling gate targets. Sibling execution remains restricted to:
- Sibling lane self-runs.
- Pinned historical regression runs in `tools/mutate-and-run.sh --regression` (which executes on temporary materialized copies in `/tmp`, never in sibling trees).

### Layer 4: Formal Province Hand-off
When content drift is observed (`js-kimi-census`, `bash-tsukuroi-census`, `bash-mado-verify`), tameshi’s role is complete upon recording the drift and noting it in round reports. Upgrading defect specs or re-measuring kill rates is deferred to owner opt-in under `corpus/knowledge/service-optin-protocol.md`.

---

## 6. Risks & Second-Order Effects

1. **Risk: Sibling Repo Movement During Sweep (Incident I1 Recurrence).**  
   *Second-order effect:* Sibling lanes operating in parallel waves may commit to HEAD or dirty their worktree while tameshi evaluates dispositions.  
   *Mitigation:* The manifest records both `pinned_commit` (immutable) and `current_head_commit` (live), plus `worktree_sha256`. A moved HEAD with clean worktree is classified accurately without failing the probe.
2. **Risk: Mode Loss on Target Materialization.**  
   *Second-order effect:* Tools materializing git blobs (e.g. `git show`) drop file permission modes (`100755` becomes `0644`). When gates invoke themselves via `$0`, permissions errors occur.  
   *Mitigation:* `PinProbe` and runner must preserve mode metadata (`100755`) alongside blob digests.
3. **Risk: False Sense of Coverage on Unchanged Targets.**  
   *Second-order effect:* Users might assume that `surface-census.sh` (unchanged) is completely verified.  
   *Mitigation:* The report and knowledge base explicitly document the context blindness dimensions (sibling TSVs, external binaries).

---

## 7. Exact Checks L1 Should Run (Advisory — Not Executed by This Seat)

L1 should run the following non-destructive checks during integration:

```sh
# 1. Verify that tools/pin-disposition.py executes selftest cleanly
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py --selftest

# 2. Verify that pin-disposition generates exactly six rows with result_reuse=not_established
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
  --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
  --root /home/vgpnk/Projects/shokunin > /tmp/pin-disp-out.json

jq '.legs | length' /tmp/pin-disp-out.json
# Expected: 6

jq '[.legs[].result_reuse] | unique' /tmp/pin-disp-out.json
# Expected: ["not_established"]

# 3. Verify content status split matches ground truth (3 unchanged, 3 changed)
jq '[.legs[] | {leg: .leg, status: .content_status}]' /tmp/pin-disp-out.json
# Expected:
#   js-kimi-census: changed
#   bash-surface-census: unchanged
#   bash-tsukuroi-census: changed
#   bash-mado-verify: changed
#   bash-checklist-run: unchanged
#   js-claims-check: unchanged

# 4. Sibling Non-Touch Verification: confirm no sibling worktree was dirtied
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain
# Expected: all return empty output

# 5. Verify no seventh gate or depth score inflation
grep -c "^#   \(js\|bash\)-" /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
# Expected: 6
```
