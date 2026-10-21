# F04 — Tools Helper Scan: SHA & Interval Logic

**Seat:** `TameshiR20-3.F04ToolsHelpers`  
**Role:** UFO-FSD Connector  
**Round:** 20 (Attempt 2, hyaku), Wave 1 Advisory  
**Target:** Scan `tools/` (`registry-check.py`, `evidence-disposition.py`, `trace-inputs.py`, `context-capture.py`) for existing sha/interval helpers. Report duplicate logic, exact function/line, recommend reuse or duplicate-logic defect.  
**Report Path:** `.ufo/waves/round-20/w1/F04ToolsHelpers.md`  

---

## 1. Declared Axes

1. **Calibration (Primary Claim C1, lane cap 8):** Close QUALITY20 recurrence via frozen contract (`6fd220b`), staged instruments (`receipt-window.py`, `measure.py`), and receipt-time gate without invalidating the 0/6 -> 6/6 population.
2. **Conformance & Contract Integrity:** Staged instrument bytes must remain strictly identical to their contract-frozen hashes (`f03ae7e9...` and `f34dc233...`); zero in-wave modifications or unauthorized refactoring.
3. **Hermeticity & Historical Replay:** Tools under `tools/` must execute independently across detached historical git revisions (`registry-check.py` `--rev` clone, `evidence-disposition.py` historical blob verification) without multi-file import coupling.
4. **Discernment & Soundness:** Distinguish intentional hermetic leaf duplication from defective code duplication; prevent reference drift across timezone representations (e.g. S049 BRT UTC-03:00 vs UTC).

---

## 2. Evidence: Inventory of Existing Helpers in `tools/` and `stage/`

### A. SHA Helpers in Target `tools/`

1. **`tools/registry-check.py`**
   - **Function:** `registry_sha256(path)` at lines 375–380.
     ```python
     def registry_sha256(path):
         try:
             with open(path, "rb") as fh:
                 return hashlib.sha256(fh.read()).hexdigest()
         except OSError:
             return None
     ```
   - **Characteristics:** Whole-file in-memory read (`fh.read()`); traps `OSError` and returns `None`.
   - **Inline/Selftest:** Line 1753 uses inline `hashlib.sha256(open(reg_diff, "rb").read()).hexdigest()`; Line 1651 asserts `len(rep["registry_sha256"]) == 64`.

2. **`tools/evidence-disposition.py`**
   - **Regex:** `HEX64 = re.compile(r"[0-9a-f]{64}")` at line 142.
   - **Function:** `sha256_bytes(payload)` at lines 207–208.
     ```python
     def sha256_bytes(payload):
         return hashlib.sha256(payload).hexdigest()
     ```
   - **Function:** `tool_sha256()` at lines 211–216 (hashes `SELF` using `sha256_bytes`, returns `None` on `OSError`).
   - **Selftest Alias:** `_sha(payload)` at lines 1715–1716 (`return sha256_bytes(payload)`).
   - **Validation:** Lines 668 & 844 assert `HEX64.fullmatch(digest) is not None`.

3. **`tools/trace-inputs.py`**
   - **Function:** `sha256_file(path)` at lines 501–506.
     ```python
     def sha256_file(path):
         h = hashlib.sha256()
         with open(path, "rb") as fh:
             for chunk in iter(lambda: fh.read(1 << 20), b""):
                 h.update(chunk)
         return h.hexdigest()
     ```
   - **Characteristics:** Chunked streaming (1 MiB / `1 << 20` bytes); does not trap `OSError`. Designed for large traced input files.

4. **`tools/context-capture.py`**
   - **Regex:** `HEX64 = re.compile(r"[0-9a-f]{64}")` at line 192 (verbatim duplicate of `evidence-disposition.py:142`).
   - **Function:** `sha256_bytes(payload)` at lines 316–317 (verbatim duplicate of `evidence-disposition.py:207–208`).
   - **Function:** `tool_sha256()` at lines 320–325 (verbatim duplicate of `evidence-disposition.py:211–216`).
   - **Validation:** Line 443 `require_hex(value, path, pattern)` with `pattern.fullmatch(value)`.

### B. Interval and Timestamp Helpers in Target `tools/`

1. **`tools/registry-check.py`**
   - **Interval/Timestamp Helpers:** **None.**
   - Uses `time.monotonic()` for elapsed wall-clock timing (lines 672, 703, 721).
   - Validates scalar `timeout_s` as a finite positive number `<= MAX_TIMEOUT_S (86400)` (lines 238–256).
   - Uses `/proc/{pid}/stat` `starttime` (tick integer) for Linux process leader ownership revalidation (lines 419–435).

2. **`tools/evidence-disposition.py`**
   - **Interval/Timestamp Helpers:** **None.**
   - Manages subprocess timeouts only (`timeout=30`, `timeout=120`). Does not parse git commit timestamps or interval ranges.

3. **`tools/trace-inputs.py`**
   - **Interval/Timestamp Helpers:** **None.**
   - Traces system calls via `strace -y`; ignores wall-clock and timestamp attributes entirely.

4. **`tools/context-capture.py`**
   - **Regex:** `OBSERVED_AT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")` at line 193.
   - **Function:** `require_observed_at(value, path)` at lines 451–456. Strict string regex matching for UTC format ending in literal `Z`.
   - **Characteristics:** Validates lexical format only. Does **not** parse into `datetime` objects, does not accept timezone offsets (`+00:00`), and contains **no interval range** (`[start, end]`) checking. When computing receipt hashes, `canonical_payload` (lines 828–830) strips `observed_at`.

---

## 3. Comparison with Staged Round-20 Instruments

1. **`.ufo/evidence/round-20/stage/receipt-window.py`**
   - **Regex:** `SHA_RE = re.compile(r"^[0-9a-f]{64}$")` at line 22 (anchored 64-hex regex used with `.match()`).
   - **Function:** `parse_ts(value)` at lines 34–46. Normalizes `Z` to `+00:00`, parses aware ISO-8601 via `datetime.fromisoformat()`, rejects naive timestamps (`dt.tzinfo is None`).
   - **Function:** `require_interval(obj, where)` at lines 49–58. Enforces `obj` is a dict with `start` and `end`, parses both through `parse_ts()`, validates `start <= end`.

2. **`.ufo/evidence/round-20/stage/measure.py`**
   - **Function:** `sha256(data)` at lines 50–51 (`return hashlib.sha256(data).hexdigest()`). Duplicates `sha256_bytes`.
   - **Function:** `parse_ts(value)` at lines 54–64. Duplicates `parse_ts` from `receipt-window.py:34–46` (with `return dt if dt.tzinfo is not None else None`).

---

## 4. Commands and Observed Outputs (Private `/tmp` Sandbox)

Executed inspection and validation scripts in `/tmp`:

### Command 1: Recomputing SHA-256 of all relevant tools and staged instruments
```sh
python3 -c "
import os, hashlib
repo = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
paths = {
    'registry-check.py': os.path.join(repo, 'tools/registry-check.py'),
    'evidence-disposition.py': os.path.join(repo, 'tools/evidence-disposition.py'),
    'trace-inputs.py': os.path.join(repo, 'tools/trace-inputs.py'),
    'context-capture.py': os.path.join(repo, 'tools/context-capture.py'),
    'staged receipt-window.py': os.path.join(repo, '.ufo/evidence/round-20/stage/receipt-window.py'),
    'staged measure.py': os.path.join(repo, '.ufo/evidence/round-20/stage/measure.py')
}
for name, p in paths.items():
    with open(p, 'rb') as fh:
        print(f'{name}: {hashlib.sha256(fh.read()).hexdigest()}')
"
```
**Observed Output:**
```text
registry-check.py: 33d0d17c140a6b9662c023a3a8cfa67065e17fb8c73af20d7c8055005565aeb6
evidence-disposition.py: 66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44
trace-inputs.py: fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636
context-capture.py: c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726
staged receipt-window.py: f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc
staged measure.py: f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d
```
*Verification:* Staged instrument digests match contract commit `6fd220b` and `contract.json` lines 23–24 & 31–32 exactly.

### Command 2: Evaluating Timestamp and Offset Behaviors Across Implementations
```sh
python3 -c "
import importlib.util
spec_rw = importlib.util.spec_from_file_location('rw', '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py')
rw = importlib.util.module_from_spec(spec_rw); spec_rw.loader.exec_module(rw)

spec_m = importlib.util.spec_from_file_location('m', '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/measure.py')
m = importlib.util.module_from_spec(spec_m); spec_m.loader.exec_module(m)

cases = ['2026-10-21T07:40:18Z', '2026-10-21T07:40:18+00:00', '2026-10-20T21:40:18-03:00', '2026-10-21T07:40:18', 'invalid']
for c in cases:
    print(f'rw.parse_ts({c!r}) -> {rw.parse_ts(c)}')
    print(f'm.parse_ts({c!r})  -> {m.parse_ts(c)}')
"
```
**Observed Output:**
```text
rw.parse_ts('2026-10-21T07:40:18Z') -> 2026-10-21 07:40:18+00:00
m.parse_ts('2026-10-21T07:40:18Z')  -> 2026-10-21 07:40:18+00:00
rw.parse_ts('2026-10-21T07:40:18+00:00') -> 2026-10-21 07:40:18+00:00
m.parse_ts('2026-10-21T07:40:18+00:00')  -> 2026-10-21 07:40:18+00:00
rw.parse_ts('2026-10-20T21:40:18-03:00') -> 2026-10-20 21:40:18-03:00
m.parse_ts('2026-10-20T21:40:18-03:00')  -> 2026-10-20 21:40:18-03:00
rw.parse_ts('2026-10-21T07:40:18') -> None
m.parse_ts('2026-10-21T07:40:18')  -> None
rw.parse_ts('invalid') -> None
m.parse_ts('invalid')  -> None
```
*Verification:* Both `receipt-window.py` and `measure.py` accept aware ISO-8601 datetimes, handle UTC `Z` and explicit offsets (such as `-03:00` BRT), and consistently reject naive timestamps and malformed strings.

---

## 5. Duplicate Logic: Defect vs. Reuse Evaluation

### A. Identified Duplications
1. **`sha256_bytes(payload)` & `tool_sha256()`:**
   - Duplicated verbatim across `tools/evidence-disposition.py` (lines 207–216) and `tools/context-capture.py` (lines 316–325).
   - Duplicated in `stage/measure.py` (lines 50–51) as `sha256(data)`.
2. **`parse_ts(value)`:**
   - Duplicated between `.ufo/evidence/round-20/stage/receipt-window.py` (lines 34–46) and `.ufo/evidence/round-20/stage/measure.py` (lines 54–64).
3. **`HEX64` / `SHA_RE` Pattern:**
   - `[0-9a-f]{64}` pattern duplicated across `evidence-disposition.py` (:142), `context-capture.py` (:192), and `receipt-window.py` (:22).

### B. Why Extracting a Shared Module is Contraindicated (The Anti-Pattern)
A naive software engineering impulse might propose extracting a `tools/common.py` or `tools/receipt_utils.py` to eliminate this duplicate code. In tameshi-shokunin, doing so would be a **catastrophic defect**:
1. **Frozen Contract Violation:** Staged files `stage/receipt-window.py` and `stage/measure.py` are cryptographically frozen in `contract.json` before dispatch. Altering them to import an external module would change their SHA-256 hashes, causing Population Item 2 (`staged_instruments_frozen`) and Item 3 (`installed_matches_contract`) to fail, collapsing C1 calibration.
2. **Historical Git Revision Portability:** `registry-check.py` invokes rows in cloned repositories at arbitrary historical commits (`clone_lane_at_rev`). If tools depend on a newly created shared module, running them against historical commits that lack that module crashes with `ModuleNotFoundError`.
3. **Self-Pinning Integrity:** `context-capture.py` computes and pins `tool_sha256()` of itself (`FROZEN_TOOL_SHA256`). Refactoring introduces dependency skew and breaks self-verification.
4. **Syscall Boundary Traceability:** `trace-inputs.py` monitors file access via `strace`. Shared modules introduce extra file open syscalls into execution traces, expanding the input surface and causing unexpected drift in input manifests.
5. **Purpose-Driven Chunking Divergence:** `trace-inputs.py:501` uses 1 MiB chunked reads (`sha256_file`), necessary to prevent OOM on large traced files. `registry-check.py`, `evidence-disposition.py`, and `context-capture.py` read whole files into memory (`fh.read()`), which is optimal for small JSON receipts (<100 KB). This difference is domain-specific tailoring, not an oversight.

---

## 6. Proposed Move: Formalize the Hermetic Leaf Helper Invariant

### Proposed Move
**Do not consolidate into a shared library. Classify the leaf utility duplication as an intentional Hermetic Leaf Helper Invariant.**
1. Maintain `tools/receipt-window.py` (upon post-wave installation) as a self-contained, single-file gate with embedded `parse_ts`, `require_interval`, and `SHA_RE`.
2. Maintain `stage/measure.py` as an evidence-only ruler that embeds its own `parse_ts` and `sha256`, guaranteeing it can execute against historical commits (`--rev REV`) where `tools/receipt-window.py` does not yet exist.
3. In the round lesson/appendix documentation, record the **Hermetic Leaf Helper Pattern**:
   *Leaf CLI gates and rulers in tameshi MUST remain standalone executables embedding minimal primitive helpers (SHA-256, aware ISO-8601 parsing) rather than importing multi-file libraries, ensuring full portability across historical commits, hermetic selftests, and unpolluted strace input graphs.*
4. Synthesize timezone handling: note that `parse_ts` in `receipt-window.py` and `measure.py` natively supports aware offsets, which harmonizes the S049 opened-date rider (local BRT `2026-10-20` vs UTC `2026-10-21`) without requiring changes to older schemas (e.g. `context-capture.py` retains strict `...Z` UTC format).

### Second-Order Effects & Risks
- **Runtime:** Zero runtime overhead or package resolution risks; tools remain zero-dependency Python 3 standard library scripts.
- **Contract:** Preserves exact contract SHAs for `receipt-window.py` (`f03ae7e9...`) and `measure.py` (`f34dc233...`), guaranteeing Population items 1–6 pass cleanly.
- **Substrate:** No production files mutated during wave 1; installation deferred to post-wave integration.
- **Risk:** Superficial duplicate-code warnings in automated linters. Mitigated by explicit architectural documentation of the hermeticity requirement in `QUALITY.md` and lesson records.

---

## 7. Verification

1. Verified all 4 target tools in `tools/` and both staged files in `stage/`.
2. Recomputed and confirmed SHA-256 hashes against `contract.json`.
3. Executed sandbox evaluation of `parse_ts` across UTC, offset (`-03:00`), naive, and invalid strings.
4. Confirmed no production files, sibling lanes, or git refs were mutated.
5. No tools installed or updated.
