# SpecTamper — snapshot digest mismatch: fixture recipe, token, expected exit

Seat: `TameshiR15.SpecTamper` (executor, leaf). Assignment: read historical
`capture-context.py`, draft only a concrete isolated fixture recipe for a
snapshot digest mismatch with exit2 / `snapshot_tampered`, state the exact
existing stable token and expected exit if supported, invent no required broad
validation feature, no source edits.

Evidence basis: source reads only, 2026-10-20, working tree at the round-15
lane root. **Nothing was executed**; no gate, selftest, fixture or historical
command was run. No tool was installed or updated.

## 1. Verdict

**The pair is supported, but not by the historical script.** `snapshot_tampered`
→ exit **2** is an existing, literal, committed stable pair in this lane at
`tools/repeat-control.py` (round-12 `--snapshot` mode), where it is declared
could-not-evaluate. The historical `.ufo/evidence/round-14/capture-context.py`
has **zero** occurrences of `snapshot` or `tamper`; its digest disagreements
are exit **1** `mismatch`, and its exit2 is a different token shape
(`kind=<InvalidContext.kind>`).

Therefore: the fixture must target the **new** `tools/context-capture.py`
snapshot mode (already an admit criterion in `corpus/lessons/round-15.md:31-33`),
reuse the existing token/exit, and never be added to the frozen historical
bytes. This is a promotion of an existing lane contract, not a new broad
validation feature.

## 2. Exact anchors read

| Claim | Anchor |
|---|---|
| Historical exit map: `1 mismatch`, `2 could-not-evaluate`, `64 usage` | `.ufo/evidence/round-14/capture-context.py:26-29` |
| Historical digest disagreement is a **verdict mismatch**, exit1 | `capture-context.py:553-580` (`decide`); reasons at 564-566 and 572-573; return `"mismatch", 1` at 578-579 |
| Historical exit2 token is `kind=<InvalidContext.kind>`, status `invalid_input` | `capture-context.py:617-629`; kinds are defined at 145-155, 163-199, 235-237, 250-265, 296-304, 337-338, 449-452 |
| Historical script/receipt contain no snapshot/tamper concept | `grep -n "snapshot\|tamper"` over both files returned status 1 (no match) |
| Existing stable token and exit | `tools/repeat-control.py:43-44` (`snapshot_tampered 2`), `:127` (`EXIT_BY_ID`), `:44-47` (declared could-not-evaluate) |
| Snapshot manifest validation (schema, int-not-bool, expected pair, exact inputs, 64-hex, regular file, unlisted files) | `repeat-control.py:361-409` |
| Per-input digest check rejects symlink and mismatch | `repeat-control.py:411-423` (`lstat`, `S_ISREG`, sha256 equality) |
| Mode precedence: missing dir → 64; tamper → 2; intact+recomputed equal → recorded pair; intact+recomputed different → 1 | `repeat-control.py:449-478` |
| Six hermetic tamper arms, each pinning literal `snapshot_tampered`/2 | `repeat-control.py:787-843` |
| Stated limit: intrinsic digests catch accidental drift, not a coordinated edit; external anchor is git history | `repeat-control.py:90-93` |
| Second lane precedent: exit2 is the could-not-evaluate class for **tampered** pinned input, token `input_digest_mismatch` | `tools/evidence-disposition.py:66-69,130,1174-1177`; hermetic case `tamper-receipt` → exit2 + `input_digest_mismatch` at `:1745-1750` |
| Round-15 admit criterion: persisted snapshot bytes digest-checked before interpreting their retained verdict | `corpus/lessons/round-15.md:31-33` |
| Round-14 retained receipt fields a retained check reads | `.ufo/evidence/round-14/context-receipt.json`: `tool_sha256`, `environment.env_delta_matches_declared`, `environment.baseline_has_GIT_DIR`, `sources.probe.matches_declared`, `sources.runner.matches_manifest_declaration`, `comparison.equal`, `comparison.payload_tool_sha256_matches_disk`, `comparison.error`, `positive_control.effective`, `mapping.all_match`, `mapping.reasons` |

Boundary note: the round-14 receipt is pinned by raw file bytes if it is ever
used as a snapshot input; unlike `comparison` normalization
(`capture-context.py:383-392`), the snapshot digest does **not** exclude
`observed_at`.

## 3. Concrete isolated fixture recipe

The recipe is parameterized on one CLI flag. If ContextGate names the mode
`--check-snapshot DIR` (recommended, mirrors `repeat-control.py`), the argv is
`[sys.executable, SELF, "--check-snapshot", dirpath]`; a
`--check-receipt RECEIPT --pins PINS` pair-mode keeps the same fixture bytes,
token and exit, only the argv changes. Do not add a second token for the
pair-mode.

Scratch root (hermetic, temp-only):

```python
scratch = tempfile.mkdtemp(prefix="tameshi-r15-context-selftest.", dir="/tmp")
# removed on pass, kept on failure, exactly like repeat-control.py:597,859
```

Valid snapshot directory:

```text
snap-valid/
  expected.json      # frozen record
  receipt.json       # synthetic retained receipt, literal bytes authored in selftest
```

`expected.json` (schema name is ContextGate's to fix; shape is the existing
`repeat-control-snapshot-v1` analogue):

```json
{
  "schema": "context-receipt-snapshot-v1",
  "expected_id": "ok",
  "expected_exit": 0,
  "inputs": {
    "receipt.json": "<sha256 of the exact receipt.json bytes>"
  }
}
```

`receipt.json` floor: the minimal document that the maintained `decide()`
actually reads. From historical `decide()` (`capture-context.py:553-580`) that
floor is:

```json
{
  "schema": "tameshi-round14-context-receipt-v1",
  "tool": "context-capture.py fixture",
  "tool_sha256": "<64 lowercase hex>",
  "environment": {"env_delta_matches_declared": true, "baseline_has_GIT_DIR": false},
  "sources": {
    "probe": {"matches_declared": true},
    "runner": {"matches_manifest_declaration": true}
  },
  "comparison": {
    "equal": true,
    "payload_tool_sha256_matches_disk": true,
    "error": null
  },
  "positive_control": {"effective": true},
  "mapping": {"all_match": true, "reasons": []},
  "status": "ok",
  "exit": 0,
  "reasons": []
}
```

If the maintained gate's required structure is stricter, extend the literal
with its own required keys — do **not** copy the live round-14 receipt file
into the fixture, because the selftest must not read lane roots. Author these
bytes from string literals in the selftest, as
`tools/evidence-disposition.py:1230` does for its oracle fixture.

### 3.1 The mismatch arm (this seat's case)

`snapshot-tamper-byte` — changed byte, digest no longer matches the pin:

```python
tamper = os.path.join(scratch, "snap-tamper-byte")
shutil.copytree(valid, tamper)
target = os.path.join(tamper, "receipt.json")
data = bytearray(open(target, "rb").read())
data[0] ^= 0x01
open(target, "wb").write(bytes(data))
proc = subprocess.run([sys.executable, SELF, "--check-snapshot", tamper],
                      cwd=scratch, stdin=subprocess.DEVNULL,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert (last_finding_id(proc.stdout), proc.returncode) == ("snapshot_tampered", 2)
```

`snapshot-tamper-pin` — the purest "snapshot digest mismatch": receipt bytes
are untouched, only the frozen digest disagrees. This is the arm that proves
the gate hashes before it interprets:

```python
tamper = os.path.join(scratch, "snap-tamper-pin")
shutil.copytree(valid, tamper)
record_path = os.path.join(tamper, "expected.json")
record = json.load(open(record_path, "rb"))
record["inputs"]["receipt.json"] = "0" * 64   # valid 64-hex shape, wrong value
open(record_path, "w").write(json.dumps(record, indent=2, sort_keys=True) + "\n")
# expect ("snapshot_tampered", 2)
```

### 3.2 Sibling tamper arms (same token/exit, already proven shape)

Each is a copy of `snap-valid` plus one mutation, invoked as a child process,
pinned to `snapshot_tampered`/2, mirroring `repeat-control.py:787-843`:

| Case name | Mutation | Expected pair |
|---|---|---|
| `snapshot-tamper-missing` | remove `receipt.json` | `snapshot_tampered`, 2 |
| `snapshot-tamper-unlisted` | add `extra.json` to the directory | `snapshot_tampered`, 2 |
| `snapshot-tamper-duplicate-key` | inject a second `"inputs"` key into `expected.json` | `snapshot_tampered`, 2 |
| `snapshot-tamper-manifest-symlink` | replace `expected.json` with a symlink to the valid copy | `snapshot_tampered`, 2 |
| `snapshot-tamper-input-symlink` | replace `receipt.json` with a symlink to the valid copy | `snapshot_tampered`, 2 |
| `snapshot-usage-missing-dir` | pass an absent directory path | `invalid_usage`, **64** (usage, not tamper) |
| `snapshot-pass` | unmodified `snap-valid` | `ok`, 0 |
| `snapshot-intact-verdict-mismatch` | intact bytes + matching pin, but `comparison.equal=false` so `decide()` fails | `mismatch`, **1** |

The last two rows are the anti-conflation boundary: **digest integrity is not
the verdict**. An intact snapshot whose stored bytes recompute to a failing
`decide()` must exit 1; only changed/missing/symlinked/unlisted/unparsable
snapshot bytes exit 2 `snapshot_tampered` (`repeat-control.py:449-478` is the
exact precedent).

### 3.3 Selftest harness and literal assertion

Invoke the real public CLI as a child, never the helper:

```python
def last_finding_id(stdout_bytes):
    last = ""
    for line in stdout_bytes.decode("utf-8", "replace").splitlines():
        if line.strip():
            last = line.strip()
    prefix = "CONTEXT: "
    return last[len(prefix):] if last.startswith(prefix) else "<" + last + ">"

def snapshot_case(name, dirpath, expect_id, expect_exit):
    proc = subprocess.run([sys.executable, SELF, "--check-snapshot", dirpath],
                          cwd=scratch, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    observed = last_finding_id(proc.stdout)
    ok = proc.returncode == expect_exit and observed == expect_id
    print("SELFTEST_CASE {} {} (expected={}/{} observed={}/{})".format(
        name, "PASS" if ok else "FAIL", expect_id, expect_exit, observed, proc.returncode))
    return ok
```

Final line convention: `SELFTEST: PASS (n/n)` / `SELFTEST: FAIL (...)` /
`SELFTEST: COULD_NOT_EVALUATE (...)`, as in
`tools/evidence-disposition.py:1848-1856` and `repeat-control.py:855-863`.
The finding line must be the **last non-empty stdout line** and stable across
runs; the selftest asserts the literal pair, not a substring.

## 4. Bounded implementation requirements this fixture pins

These are the minimum predicates the fixture will expose; none is a broad new
environment claim.

1. **Token and exit**: add `"snapshot_tampered": 2` to the gate's stable map;
   registry maps it as could-not-evaluate. Do not mint
   `receipt_digest_mismatch` or reuse `input_digest_mismatch` for this mode —
   both exist elsewhere with different shapes
   (`evidence-disposition.py:1174`), and the assignment's literal token is
   already the lane's.
2. **Digest first**: hash every listed snapshot input before any `decide()`
   predicate; the cached bytes are what `decide()` reads.
3. **Read-only, subprocess-free**: snapshot mode executes nothing and reaches
   no live lane path. A `subprocess` call reachable from this mode breaks the
   hermetic clause and the "no live roots" selftest claim.
4. **Regular files only**: `os.lstat` + `stat.S_ISREG` for `expected.json` and
   every listed input; reject symlinks (`repeat-control.py:363-368,411-419`).
5. **No duplicate keys**: parse `expected.json` with an
   `object_pairs_hook` that rejects duplicates, else a second `"inputs"` key
   shadows the pin.
6. **Exact input set**: listed inputs must equal the required set; unlisted
   regular files are tampering.
7. **Stable expected pair**: `expected_id` must be in the stable map and
   `expected_exit` must be an `int` that is **not** `bool` and equals the map
   value (`repeat-control.py:381-389`).
8. **Exit precedence**: absent directory → 64 `invalid_usage`; any tamper
   class → 2 `snapshot_tampered`; intact and recomputed pair equal → recorded
   pair; intact and recomputed pair different → 1 `mismatch`.
9. **Own-failure class**: an unexpected exception must map to a 2
   `setup_error`-style class, never 1, so no crash reads as a verdict
   (`repeat-control.py:200-203` rationale).
10. **Historical freeze**: `.ufo/evidence/round-14/capture-context.py` and
    `.ufo/evidence/round-14/context-receipt.json` stay byte-identical; the new
    token lives only in `tools/context-capture.py`.

## 5. Risks, false positives, unearned claims

- **False positive to reject**: an "intact snapshot whose `decide()` fails"
  reported as `snapshot_tampered`. That is a verdict mismatch (exit1), not
  tampering; the fixture table above separates them deliberately.
- **False positive to reject**: passing the fixture when the child exits 2 for
  an unrelated reason (missing `python3`, unreadable temp dir). The case must
  assert the token as well as the exit, which the literal pair does.
- **Unearned claim to reject**: "tamper-proof snapshot". Digests live inside
  the directory they validate, so they catch accidental drift, not a
  coordinated edit of receipt plus pin; the external anchor is committed git
  history (`repeat-control.py:90-93`). State this limit in the tool docstring.
- **Unearned claim to reject**: "the retained receipt's verdict is
  re-executed". Snapshot mode interprets the retained document's bytes; it
  runs no probe and establishes no live environment, suite or sibling state.
- **Isolation trap**: copying `.ufo/evidence/round-14/context-receipt.json`
  into the fixture makes the selftest read a live lane root and couples it to
  historical bytes. Use literals.
- **Boundary trap**: a missing snapshot directory is usage (64), not tampering
  (2); reviewers will test that edge (`repeat-control.py:451-452`).
- This report is source-read evidence only. Whether the fixture passes is L1's
  single post-integration check; no executed result is claimed here.

## 6. Recommendation to ContextGate (via TameshiR15)

Implement `--check-snapshot DIR` (or the pair-mode equivalent) with the
`snapshot_tampered`/2 class and the eight-case table in §3.2, assert literal
pairs as a child process, keep snapshot mode read-only and subprocess-free,
and leave all historical bytes untouched. That satisfies the round-15 admit
criterion (`corpus/lessons/round-15.md:31-33`) with the lane's existing token
and exit, without adding any broad validation surface.
