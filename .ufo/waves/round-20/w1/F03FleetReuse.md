# F03 — Fleet and Tools Reuse Analysis for Receipt-Window / Interval Validation

## 1. Declared Axes

- **Calibration (C1, Primary Target):** Close QUALITY20 recurrence by moving population from 0/6 to 6/6 via frozen-before-dispatch contract, staged instruments, and receipt-time instrument-sha / measurement-interval gating. Score remains at lane cap 8 (last 2 points require independent review).
- **Depth:** Preserved at 8 (no regression or reduction in depth).
- **Substrate & Integrity Safety:** Zero mutations to fleet scripts, sibling lanes, git/jj refs, or production files during advisory wave 1. Hermetic stdlib-only execution in private `/tmp` sandboxes.
- **Quality & Discernment:** Enforce strict, timezone-aware ISO-8601 measurement intervals (`start <= end`) and prevent in-wave instrument mutations vs loose or heuristic point-in-time checks.

---

## 2. Scan of Fleet Scripts (`/home/vgpnk/Projects/shokunin/scripts`)

Scanned all scripts and tools under `/home/vgpnk/Projects/shokunin/scripts` for receipt-window, interval, or instrument-sha validation logic.

### Exact Paths Scanned
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
- `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/wave-slot-selftest.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/wave-live.py`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/wave-slot.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane-selftest.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/closure-prompt.md`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/hyaku.env`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/await-capacity.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/probe-alias.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/status.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/await-event.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/pool.txt`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/append-closure.py`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`

### Observed Matches & Interfaces
- `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh` (lines 13, 61, 407): Contains `TICK_SECONDS` configuring the watchdog sleep sweep interval (`sleep "$INTERVAL"`). Not an evidence validator.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/await-capacity.sh` (lines 5, 7): Contains `window=90` denoting the time window (seconds) to average active subagents. Not a receipt or interval validator.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/wave-live.py` (lines 49-64, 66-80): Implements `timestamp(value)` using `datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))` and `success_artifact(dir_fd, name, record, message)` checking `artifact.st_mtime > when` for agent liveness heuristics. Does not validate measurement intervals, receipt documents, or instrument shas.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/append-closure.py` (lines 30-58): Implements `validate(e)` for MANIFEST closure entries (`round`, `closed_at`, `lanes`, `trends`). Does not validate measurement intervals or instrument provenance.

**Result for fleet scripts:** Zero receipt-window or measurement-interval validators exist in fleet scripts.

---

## 3. Scan of Lane Tools (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools`)

Scanned all tools in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools` for existing interval, receipt-window, or instrument-sha gating logic.

### Exact Paths Scanned
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/evidence-disposition.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/bash-witness-study.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/trace-inputs.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/context-capture.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/witness-metadata.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/repeat-control.py`

### Observed Matches & Interfaces
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/context-capture.py`:
  - **Interface:** `context-capture.py --check [--receipt FILE --expected FILE] [--json] | --selftest`
  - **Function:** Round-15 gate validating round-14 context receipt re-derivation.
  - **Time Logic:** Line 193 defines `OBSERVED_AT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")`; lines 452–456 enforce that `observed_at` matches this point-in-time regex.
  - **Limitation:** Does not parse timestamps to objects, has no interval concept (`start <= end`), and does not compare timestamps against an edit window or instrument sha.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/evidence-disposition.py`:
  - **Interface:** `evidence-disposition.py --check MANIFEST [--json] | --selftest`
  - **Function:** Round-14 gate validating evidence disposition manifests against expected checks and raw receipt check stdout.
  - **Time Logic:** None. Subprocess calls use fixed timeouts (`timeout=30`, `timeout=120`). Does not validate measurement intervals or timestamps.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py`:
  - **Interface:** `pin-disposition.py --run MANIFEST ROOT [--json] | --selftest`
  - **Function:** Computes git commit and worktree sha256 for specified legs.
  - **Time Logic:** Lines 680–682 stamp `observed_at` using `datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")` to mark probe completion. It outputs a point-in-time stamp; it does not validate intervals.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/trace-inputs.py`:
  - **Interface:** `trace-inputs.py --root DIR [--cwd DIR] [--out FILE] -- ARGV...`
  - **Function:** Runs strace on ARGV, filters opens, and emits a JSON receipt (`tameshi-trace-inputs-v1`) containing inputs sha256. Does not validate measurement intervals or windows.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh`, `registry-check.py`, `bash-witness-study.py`, `witness-metadata.py`, `repeat-control.py`:
  - None contain receipt-window or measurement-interval validation.

**Result for lane tools:** Zero receipt-window or measurement-interval validators exist in `tools/`.

---

## 4. Analysis: Reuse vs New Gate

### Is reuse of an existing tool better than the new gate?
**No. Reuse is strictly inferior and inadvisable for four structural reasons:**

1. **Zero Overlap in Invariant Coverage:** No existing tool implements ISO-8601 datetime parsing, interval ordering (`start <= end`), instrument sha classification (frozen vs installed vs historical), or edit-window boundary enforcement (`frozen.end <= edit.start`, `installed.start >= edit.end`). Attempting "reuse" would require authoring all of this logic from scratch anyway.
2. **Contract and Domain Violation:** The existing tools (`context-capture.py`, `evidence-disposition.py`) are purpose-built gates for specific historical claims (R14 context receipts and R13/R14 evidence dispositions). Overloading them with round-20 receipt-window logic would violate single-responsibility separation and pollute historical evidence schemas.
3. **Registry and Pin Invalidation:** `context-capture.py` and `evidence-disposition.py` are byte-pinned in `tools/registry.json` and historical evidence. Modifying their code would break their self-pinned identity hashes and historical regression baselines.
4. **Violation of Round-20 Frozen Contract:** Commit `6fd220b` establishes `.ufo/evidence/round-20/contract.json`, which explicitly defines population items 2, 3, 4, 5, 6 around `stage/receipt-window.py` and `tools/receipt-window.py` (sha256 `f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc`). Diverting from this dedicated gate would directly cause population items `staged_instruments_frozen`, `installed_matches_contract`, `selftest_receipt_clean`, and `final_receipts_clean` to fail.

### Why the new gate (`tools/receipt-window.py`) is superior:
- **Clean Interface:** `python3 tools/receipt-window.py --contract CONTRACT --receipts RECEIPTS [--json] | --selftest`
- **Purpose-Built for QUALITY20/21:** Specifically enforces that instruments are frozen before dispatch and that receipts reflect valid measurement windows.
- **Hermetic & Standalone:** Requires only standard library (`argparse`, `datetime`, `json`, `re`, `sys`), with no external dependencies or mutable state.
- **Exhaustive Selftest:** Self-contained 20-test suite covering clean, fail, invalid contract, and invalid receipt conditions.

---

## 5. UFO-FSD Connector Proposal (Non-Obvious Move)

- **Evidence:**
  1. Fleet scripts and existing lane tools lack any interval-window validator, while `stage/receipt-window.py` provides self-contained, aware ISO-8601 interval verification.
  2. Contract population item 3 requires `tools/receipt-window.py` to match `installed_sha256` (`f03ae7...`), but `tools/registry.json` currently has no entry for `receipt-window.py`.
  3. Sibling tools and fleet scripts each handle timestamps idiosyncratically (regexes in `context-capture.py`, `.replace("Z", "+00:00")` in `wave-live.py`, `strftime` in `pin-disposition.py`).
- **Affected Axes:**
  - **Calibration (+):** Directly enables population items 2–6 to achieve 6/6 cleanly.
  - **Quality & Discernment (+):** Retains strict ISO-8601 aware datetime semantics without creating shims or leaky couplings.
  - **Substrate Safety (Preserved):** Leaves fleet scripts and historical `tools/*` untouched.
  - **Depth (Preserved):** Unchanged at 8.
- **Proposed Move:**
  Install `stage/receipt-window.py` byte-identically into `tools/receipt-window.py` (matching contract frozen SHA `f03ae7...` exactly), and keep its schema `tameshi-receipt-window-v1` completely self-contained (requiring only `{id, instrument_sha256, measurement_interval: {start, end}}` per receipt). Do not attempt cross-lane imports or fleet-script mutations during round-20. When L1 registers the tool in `tools/registry.json`, register only the hermetic `--selftest` invocation (`["python3", "tools/receipt-window.py", "--selftest"]`), ensuring the tool is automatically verified by `registry-check.py` without requiring synthetic receipt fixtures in `tools/`.
- **Risks & Mitigation:**
  - *Risk:* Integrator might modify `tools/receipt-window.py` during install, violating item 3 (`installed_matches_contract`).
  - *Mitigation:* Install must be a pure byte copy (`cp .ufo/evidence/round-20/stage/receipt-window.py tools/receipt-window.py`) verified by `sha256sum`.
  - *Risk:* Receipt emitters might supply timezone-naive ISO strings.
  - *Mitigation:* The gate's aware ISO requirement (`require_interval`) strictly prevents timezone ambiguity by throwing `BAD_INTERVAL` (as confirmed by B05).
- **Verification:**
  - Recomputed staged gate sha256 matches `f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc`.
  - Selftest passes 20/20 in isolated sandbox with exit code 0.

---

## 6. Commands and Observed Outputs

### Command 1: Exhaustive Scan of Scripts and Tools
```sh
python3 -c '
import os, re
for d in ["/home/vgpnk/Projects/shokunin/scripts", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools"]:
    print(f"=== Scanning {d} ===")
    for root, _, files in os.walk(d):
        for f in sorted(files):
            p = os.path.join(root, f)
            try:
                content = open(p, "r", encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            hits = [(i, l.strip()) for i, l in enumerate(content.splitlines(), 1)
                    if re.search(r"\b(interval|receipt|window)\b", l, re.I)]
            if hits:
                print(f"File: {p} ({len(hits)} hits)")
                for lno, text in hits[:3]:
                    print(f"  L{lno}: {text[:100]}")
'
```

**Observed Output:**
```text
=== Scanning /home/vgpnk/Projects/shokunin/scripts ===
File: /home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh (3 hits)
  L13: #   TICK_SECONDS      sweep interval (default 450; positive integer).
  L61: INTERVAL=$TICK_SECONDS
  L407: sleep "$INTERVAL"
File: /home/vgpnk/Projects/shokunin/scripts/hyaku/await-capacity.sh (2 hits)
  L5: # under the session dir written within the last WINDOW seconds. A subagent inside one
  L7: #   await-capacity.sh <session-dir> [threshold=85] [max-seconds=3600] [window=90]
=== Scanning /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools ===
File: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/context-capture.py (149 hits)
  L2: """context-capture.py — round-15 retained context-receipt gate.
  L4: Question answered: does one retained round-14 context receipt, byte-pinned by
  L6: fact is RE-DERIVED from the receipt's raw fields — or does the retained record
File: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/evidence-disposition.py (38 hits)
  L6: raw receipt observation that satisfies the original expectation — or, for the
  L10: This is a gate over declarations and retained receipt JSON. It never executes
  L11: receipt argv. Pins in the dispositions document are configured authority for
File: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh (2 hits)
  L985: @defect C1060 | count floor: REPORT_MIN_BYTES 1024 -> 1060, one past the projected interval [26,1059
  L990: @defect C1059 | count floor: REPORT_MIN_BYTES 1024 -> 1059, the upper edge of the projected interval
File: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py (1 hits)
  L58: so it marks the end of the read window) and `not_compared`, a static list of
File: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry.json (4 hits)
  L378: "--receipt",
  L379: ".ufo/evidence/round-15/frozen/context-missing-env/receipt.json",
  L403: "--receipt",
File: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/trace-inputs.py (4 hits)
  L5: passes the command's stdout/stderr through, and writes a JSON receipt:
  L28: credential files can neither be read nor leaked into a receipt.
  L309: # there and this receipt is committed. Count only.
```

### Command 2: Staged Gate SHA-256 and Isolated Selftest
```sh
sandbox=$(mktemp -d /tmp/tameshi-r20-f03.XXXXXX)
cd "$sandbox"
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py
cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py ./receipt-window.py
python3 ./receipt-window.py --selftest
echo "SELFTEST_EXIT=$?"
rm -rf "$sandbox"
```

**Observed Output:**
```text
f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py
PASS [ 1/18] frozen receipt before the edit window is clean — CLEAN
PASS [ 2/18] installed receipt after the edit window is clean — CLEAN
PASS [ 3/18] missing instrument sha is refused — FAIL
PASS [ 4/18] unknown sha is refused — FAIL
PASS [ 5/18] missing interval is refused — FAIL
PASS [ 6/18] reversed interval is refused — FAIL
PASS [ 7/18] naive timestamp is refused — FAIL
PASS [ 8/18] frozen sha after the edit starts is refused — FAIL
PASS [ 9/18] installed sha before the edit ends is refused — FAIL
PASS [10/18] duplicate id is refused — FAIL
PASS [11/18] empty receipts is refused — FAIL
PASS [12/18] historical sha is classified, not gated — CLEAN
PASS [13/18] second historical sha is classified — CLEAN
PASS [14/18] identity instrument accepts a wave-time receipt — CLEAN
PASS [15/18] declared instrument mismatch is refused — FAIL
PASS [16/18] multi-receipt one-bad row fails the file — FAIL
PASS [17/18] frozen-sha receipt ending exactly at edit start is clean — CLEAN
PASS [18/18] installed-sha receipt starting exactly at edit end is clean — CLEAN
PASS [19/20] malformed contract is refused — CONTRACT_INVALID
PASS [20/20] malformed receipts is refused — RECEIPTS_INVALID
RECEIPT_WINDOW_SELFTEST: 20/20 pass
SELFTEST_EXIT=0
```

---

## 7. Agreement, Disagreement, and Defects

- **Agree:** Agree with contract design. No existing fleet script or lane tool validates receipt windows or measurement intervals. Authoring and installing the purpose-built `stage/receipt-window.py` as `tools/receipt-window.py` is the correct, contract-compliant architecture that satisfies QUALITY20/QUALITY21.
- **Disagree:** Disagree with any suggestion to reuse or modify `context-capture.py` or `evidence-disposition.py` for this role, as it would breach separation of concerns, break historical byte pins, and violate the frozen round-20 contract.
- **Defects Observed:** None in the assigned scope. The staged gate matches its contract digest, its selftest suite passes 20/20, and all fleet scripts remain safely read-only.
- **Tooling Record:** No packages installed or upgraded. Host `pacman` remained untouched.
