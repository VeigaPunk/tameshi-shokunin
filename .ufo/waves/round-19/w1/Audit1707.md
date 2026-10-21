# Audit1707: round-18 receipt `audit-1707` (tameshi round 19 attempt 1, w1, advisory)

Seat: `TameshiR19-2.Audit1707` (reviewer, read-only). Written 2026-10-21, about 02:56-03:00.
This report is advisory. It does not close anything, and it is not an admission.

## Scope, sources, and what I did not do

- Receipt pair (`L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`):
  - `$L/.ufo/evidence/round-18/final/audit-1707.stdout`: 6063 B, 61 lines, sha256 `cebcea16f3decbd839177eeebc3b35e52d746859c589913892baf4222bd7e059`
  - `$L/.ufo/evidence/round-18/final/audit-1707.stderr`: 0 B, sha256 `e3b0c442…b855`, the empty-input digest
  - `$L/.ufo/evidence/round-18/coldread/traces/L1/audit-1707.json`: 5599 B, schema `tameshi-trace-inputs-v1`, sha256 `40ccc9b02b582959c23ef09baa76caacdfa93e31405a70cd55e97115e1fa5188`
- Ledger entry: `$L/.ufo/evidence/round-18/coldread/ledger.json:12346-12387`. This is page `1334c512…`, start 1707, end 1753, heading "## Errata — round 16 full-page cold-read". It is the only ledger entry that references this trace. I also read its source seat entry, `$L/.ufo/waves/round-18/w3/L1Residual.md:468-515`.
- Context: `$L/corpus/lessons/round-18-verifier-spotcheck.md` §5 (commit `7243e7f`, 2026-10-21T00:51:38-03:00).
- Git reads were read-only, run with `GIT_*` stripped and `git --no-optional-locks -C $L`:
  - `cat-file blob` for the 14 trace inputs at `a9c94c5`, `4b7c682`, `7243e7f` and `21e7932`
  - first-parent first-appearance scan over `183f87b..a134a09`
  - `diff --name-status 921ef80..a9c94c5` and `5923d89..a9c94c5`
  - `diff --stat`/`-U0 7243e7f..21e7932`
  - `status --porcelain` for `SKILL.md` and the round-16/round-18 evidence paths
- I did not:
  - re-execute the receipt argv;
  - read the contents of the other receipts (`checks.json`, `probes.stdout` and the rest were only hashed);
  - run any test, build, selftest or formatter;
  - write anything except this report;
  - install any tool.
- No `lsp` device is mounted in this session, and the material is JSON, Markdown and text with no code diff. Every check below is a byte, hash or Git-object check, not semantic proof.

Core investigation code (Python, ran in the session kernel, read-only):
```python
git = lambda *a: subprocess.run(["git","--no-optional-locks","-C",L,*a],capture_output=True,env=env_without_GIT).stdout
for p,h in trace["inputs"].items():                      # 14 inputs
    for rv in (a9c94c5, 4b7c682, 7243e7f, "HEAD"):
        assert_or_report(sha256(git("cat-file","blob",f"{rv}:{p}")) == h)
sec = "\n".join(stdout_lines[1:47]); sha256(sec) == ledger_entry["sha256"]
stdout_lines[1:47] == skill_a9c94c5.splitlines()[1706:1752]
```

## Verification results

| # | Check | Source / command | Observed |
|---|---|---|---|
| V1 | Stdout hash bound to a record | grep for `cebcea16` and `40ccc9b0` over all of `$L` (gitignore off) and `/home/vgpnk/Projects/shokunin/.ufo/reports` | **No match anywhere.** The trace schema has no stdout or stderr digest field, and neither does the ledger entry. Integrity rests on Git alone. See M1. |
| V2 | Pair stable in history | `cat-file` at `a134a09`, `a85f710`, `4b7c682`, `7243e7f`, `21e7932` | All three blobs are byte-identical at every revision. They were added in `a134a09` (2026-10-20T18:47:13-03:00), whose parent is `a9c94c5` (18:46:21-03:00). |
| V3 | argv → stdout structure | argv (31 elements): `bwrap … --unshare-net --chdir <root> env -i … python3 -c <script> <spec>` | Pass: `--chdir` = `cwd` = `root`. Spec is start 1707, end 1752, 13 paths, none under `corpus/knowledge/`. Stdout has 61 lines: `SECTION 1707 1752`, 46 section lines, 13 `OPEN` lines in spec order, 0 `TAIL` lines, and the script's literal final print. It ends with a newline. Stderr is empty and the trace records `exit: 0`, which is consistent with all asserts passing. |
| V4 | Section bytes | stdout lines 2–47 compared with `a9c94c5:SKILL.md` lines 1707–1752 | Byte-equal. `sha256("\n".join(lines 1707–1752))` = `290e75a4…47bb`, which equals the ledger entry `sha256`. I reproduced it from the stdout itself and from the blob. |
| V5 | OPEN digests and sizes | the 13 `OPEN` lines, the trace `inputs`, and the blobs at `a9c94c5` | All 13 digests and byte counts are equal. |
| V6 | Trace ↔ ledger | ledger entry fields | Ledger `inputs` equal trace `inputs` minus `SKILL.md`, exactly, and `inputs_dropped` is `["SKILL.md"]`. `skill_sha256` equals the trace's `SKILL.md` digest `1334c512…` and blob `a9c94c5:SKILL.md` (143694 B, 1934 lines). `read_rev` equals trace `rev` (`a9c94c5`). The entry is identical at `a134a09`, `a85f710`, `4b7c682`, `7243e7f` and `21e7932`; the ledger file digest changed at `a85f710`, but not this entry. |
| V7 | Revision fact | first-appearance scan over 11 first-parent lane commits | `a9c94c5` is the earliest lane revision that holds all 14 inputs at the recorded digests: `registry-branch-aligned.stdout` first appears there, the other 11 at those digests from `5923d89`, and the round-16 pair from `93d22aa`. The same 14 digests also hold at `a134a09`, `4b7c682` and `7243e7f`. |

## Findings by severity

### M1: No digest binds the stdout or stderr to the trace or the ledger (verification gap)

- **Observation:** V1. The only links between `audit-1707.stdout` and `traces/L1/audit-1707.json` are:
  - the shared filename stem;
  - the shared adding commit `a134a09`;
  - content consistency (V3–V5).
- **Inference:** Given the trace and the blobs, the script's output is fully deterministic. So someone could rebuild a byte-identical stdout without running anything, and the pair does not independently prove execution beyond the tracer-asserted `exit: 0`.
- **Consequence:** An in-place edit of the stdout or the trace would fail no receipt-level check; only Git history would show it.
- **Failing criterion:** The assigned "verify stdout hash" cannot be met against a recorded expected value, because none exists. I verified content-consistency in its place.

### M2: The terminal `VERIFIED` line claims more than the command checked

- The stdout ends with this line (stdout:61, `a134a09`, 2026-10-20): "VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision".
- **Observation:** That line is a hardcoded `print` literal in argv[-2]. The script has no git, blob, revision or ancestor logic. It runs 8 `assert` statements (9 evaluations, because case7 and case8 are checked in a loop) over 9 files:
  - `registry-branch-aligned`, `probes`, `regression`, `historical`
  - `case7`, `case8`
  - `disposition`, `before`, `repeat`
- Four inputs are only hashed, with no assertion:
  - the round-16 `SKILL.snapshot.md`
  - the round-16 `ledger.json`
  - `context.stdout`
  - `checks.json`
- `checks.json` is the receipt behind routed defect 4. The spot-check says (`round-18-verifier-spotcheck.md:196-198`, 2026-10-21): "`final/checks.json` records `bash-witness-selftest` argv exit 64 with an empty stdout". So "VERIFIED actual execution receipts" covered a failed invocation it never examined.
- **Independent check (mine, not established by the receipt):** `921ef80..a9c94c5` contains:
  - 51 added files under `.ufo/evidence/round-18/` (11 `.json`, 20 `.stdout`, 20 `.stderr`), all mode 100644;
  - modifications to `SKILL.md` and `corpus/lessons/round-18.md`;
  - nothing under `tools/` and no executable extensions.

  That corroborates the seat's statement at path level for that window (`L1Residual.md:476`, `a85f710`, 2026-10-20): "the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments."
- **Unknown:** Whether every receipt run before `921ef80` used the same instrument blobs. Settling that would mean reading other receipts' argv, which is outside my scope.
- This is outside C1's five items. If someone wants it corrected, it is a candidate for a future appended erratum, not a C1 expansion. `audit-1707.stdout` itself must not be edited.

### L1: The receipt establishes little about the section itself; the bucket's credit is keyed to inputs

- **Established about the section's content:**
  - its text at `a9c94c5` (V4);
  - that the round-16 snapshot and ledger it cites exist, with digests. The snapshot digest matches the section's `97cf436b…3580` citation.
- **Not established:**
  - the counts "51 buckets" and "30 cold-read seats";
  - any row of the repair table;
  - the minor-gaps list;
  - the `git show e69b488:SKILL.md` digest claim. I checked that one independently and it is true (`97cf436b…3580`), but the receipt did not check it.
- The 9 asserted round-18 final receipts have nothing to do with the round-16 errata. The same `final/*` set is also listed as inputs of the L1 buckets at 1676 (ledger :12318-12328) and 1754 (:12404-12414).
- The ledger warns about this itself (`SKILL.md:1934`, unchanged from `a9c94c5` to `21e7932`): "input-keyed credit only: it binds credit to recorded inputs, not to the commands a bucket requires". The seat also disclosed (`L1Residual.md:476`): "L1 residual verification is not a blind non-author cold read."
- This is not hidden, but reading this bucket's `gap-minor` credit as checked content would be extrapolation. It is residual risk for the calibration monitor, not a C1 failing criterion.

### L2: `env_overrides` does not describe the environment the measured command ran with

- **Observation:** The trace records `set.PYTHONPYCACHEPREFIX=/tmp/trace-inputs-run-pbzf8xkq/pycache` and `git_vars_removed=[GIT_CONFIG_GLOBAL, GIT_CONFIG_NOSYSTEM]`.
- The argv's `env -i` clears the environment and then sets: `PATH`, `HOME`, `TMPDIR`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `JJ_CONFIG=`, `LC_ALL=C`, `PYTHONDONTWRITEBYTECODE=1`.
- So `python3` ran without `PYTHONPYCACHEPREFIX` and with both GIT variables set. The field describes the tracer's outer process.
- It has no effect on this output: the script never calls git, and bytecode writing is disabled anyway.

### L3: The trace does not record interpreter or tracer identity, or timing

- `python3` was resolved through a `PATH` that starts with `~/.grok/bin`, `~/.kimi-code/bin`, mise shims and short-lived `/run/user/1000/fnm_multishells/*` directories.
- The trace records:
  - no interpreter path or version;
  - no blob or version of the tracer;
  - no start or end time.
- `external: {}` and `live_lane_reads: {}` are the tracer's own claims. The Python standard-library reads are not listed, which suggests the tracer filters system paths [INFERENCE]; whether it does is unknown.
- Impact is low: the script uses only deterministic standard-library calls.

### I1: `SECTION 1707 1752` against ledger `end: 1753` is reconciled (not a defect)

Line 1753 is the blank separator before the heading at 1754. The ledger's section hash covers exactly lines 1707–1752 (V4), which are the bytes the stdout printed.

## Could the C1 repairs invalidate this historical evidence?

**No, not as landed.** I checked `21e7932` and the live worktree as of 2026-10-21T02:55:18-03:00.

- **Repair commits:**
  - The repairs after the frozen baseline are `78b99dd` (02:28:10) and `21e7932` (02:48:27).
  - `7243e7f..21e7932` changes 30 files. None are under `.ufo/evidence/round-18/` or `.ufo/evidence/round-16/`.
  - All 13 evidence inputs, the receipt pair and the ledger entry are byte-identical at `21e7932` and in the worktree; `status` is clean for those paths.
- **`SKILL.md`:**
  - `21e7932` appends one row at line 1935, so the page digest goes from `1334c512…` to `4d0190fd…7691`.
  - The worktree carries one more uncommitted end-append, made by L1 while this audit was running: hunk `@@ -1935,0 +1936 @@`, file digest `b653979a…a864`.
  - Lines 1–1934 are identical to `a9c94c5`. The section hash (`290e75a4…`) and the 1707/1754 anchors are unchanged at `21e7932` and in the worktree.
  - The ledger key `1334c512…` is now a historical page key. The entry stays valid for `a9c94c5`/`1334c512`. Crediting it as current-page coverage would need a carry or refresh, and C1 claims no new cold-read coverage.
- **Defect 4 (`final/checks.json`, an input of this trace):**
  - The repair appended `.ufo/evidence/round-19/bash-witness-selftest{,-complete}.{json,stdout,stderr}`.
  - `checks.json` was not edited and stays at `fed3c8e6…`.
  - audit-1707 never asserted anything about `checks.json`, so the repair contradicts nothing this receipt established.
- **Defect 5:** The repair adds `round-19/round18-final-measure.*`, so it is additive only.
- **Defects 1–3:** These touch `corpus/knowledge/guard-kill-closure.md`, `corpus/knowledge/mutation-case-kumitate-sources-check.md` and `corpus/lessons/round-18.md`. None of them is an input of this trace.
- **C1's own audit:** It disclaims this kind of strengthening (`SKILL.md:1935`, `21e7932`, 2026-10-21): "Only metadata/effective-receipt reconciliation, never producer authentication, cold-read credit or required-command coverage". C1 neither strengthens nor weakens this receipt's credit.

Any of these would invalidate the evidence:

1. Rewriting `final/checks.json` in place. Its digest is recorded by this trace and by the ledger buckets at 1676, 1707 and 1754.
2. Editing `audit-1707.stdout`, `audit-1707.json` or ledger entry `1334c512`/1707. No digest would detect it (M1).
3. Inserting or changing `SKILL.md` lines at or before 1753, which would change the section hash and shift the anchors.
4. Re-assembling the ledger without carry, so the `1334c512` entries are dropped.

I observed none of these.

## Residual risk and verification gaps

- **Unknown:** Whether round-19's effective-receipt mapping marks `final/checks.json` superseded. I did not read the round-19 contract or monitor files. Either way, the hash-only reference in this receipt stays a true historical fact.
- **Unknown:** Whether the instrument blobs were equal for receipts run before `921ef80` (M2), and whether the tracer filters system paths (L3).
- I did not re-execute the argv, so `exit: 0` is the tracer's assertion. What I did establish: the stdout is consistent with that exit, and stderr is empty.
- Not applicable: resume continuity (this is not a resume path) and rerouting (there is a single bwrap → `env -i` → `python3` runtime and no reroute is recorded).
- No tool was installed or updated.
