# ReviewCounterB — C2 counter review (round 33, wave 1)

Seat: tameshi-r33-w1-ReviewCounterB-4
Scope: review the frozen counter `.ufo/evidence/round-33/c2/c2-measure.py` (blob f1c6c3a73a5da7fcda8da48b72679595241a85196a8afa28a3afe2a1cf4f452d at freeze rev f6d8a891f1d966c5c3cdda385090da3a6e804675, identical to the worktree file) against claim C2 in `.ufo/evidence/round-33/contract.json` and the SOURCES contract v1 (`/home/vgpnk/Projects/shokunin/CORPUS.md`).
Method: static read of the counter; canonical counter runs at the freeze rev and at base with exits captured (`cmd; echo $? > file`); fixture repos inside this seat's scratch to probe the digest and row-id checks. No `lsp` server was available in this session (not in tool inventory), so code understanding is by direct read, and check behavior is demonstrated by executed fixtures, not grep.

## Canonical runs (exit captured)

Freeze rev f6d8a891f1d966c5c3cdda385090da3a6e804675:

```
$ timeout 60 python3 .ufo/evidence/round-33/c2/c2-measure.py --lane <lane> --rev f6d8a891f1d966c5c3cdda385090da3a6e804675
C2_R33: row=none versioned_url=0 snapshot_sha_ok=1 gate_sha_ok=0 quote_ok=1 C2_R33_PASS=false
$ echo $?
1
```

Base 66e1fb444615b3afe380e7df0244ef7fae1dd985:

```
$ timeout 60 python3 .ufo/evidence/round-33/c2/c2-measure.py --lane <lane> --rev 66e1fb444615b3afe380e7df0244ef7fae1dd985
C2_R33: row=none versioned_url=0 snapshot_sha_ok=0 gate_sha_ok=0 quote_ok=0 C2_R33_PASS=false
$ echo $?
1
```

Both match the contract's before state (row=none, PASS=false, exit 1). At the freeze rev the snapshot already exists and matches the pinned digest (snapshot_sha_ok=1) and carries the quote (quote_ok=1); only the row and the round-33 lesson Gate are absent (no `corpus/lessons/round-33.md` at REV; last lesson is round-32), so C2 is false at the freeze rev, as expected for a claim measured later.

## Correct checks (confirmed sound)

- Row parsing positions are correct for the real table. SOURCES.md (CORPUS.md §Shape, 11 content columns: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by) splits with `|` into 13 fields including the leading and trailing empties; the counter's `cells[1]`=id, `cells[2]`=source URL, `cells[7]`=teaches match the actual header. The `|`-free cell rule (CORPUS.md) makes the split safe.
- Versioned-URL regex `docs\.python\.org/3\.[0-9]+/` rejects the moving `/3/` alias and accepts `3.15`. Fixture repo4 (URL `https://docs.python.org/3/library/doctest.html`, everything else valid) produced `versioned_url=0 C2_R33_PASS=false`, exit 1. Fixture repo1 (3.15) passed.
- Snapshot pin: `EXPECTED_SHA` equals the contract `snapshot_sha256` (217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899); the snapshot at REV hashes to it, and the frozen quote bytes are present (quote_ok=1 at freeze rev). The fetch receipt at REV corroborates: URL 3.15, 216574 bytes, same sha256, quote located in the module introduction's first bullet.
- REV purity: every input is read via `git -C lane show <rev>:<path>` (SOURCES, snapshot, lesson); no worktree path is opened; `SELF_DIR` is unused; `GIT_*` env vars are stripped and `GIT_OPTIONAL_LOCKS=0` set. Fixture runs against self-made repos confirm the counter depends only on the named rev's committed bytes.

## Findings, by severity

### Finding 1 (moderate): gate_sha_ok binds the digest to any lesson occurrence, not to the Gate record
`c2-measure.py` lines 78–81 collect every `sha256[ :=]+([0-9a-f]{64})` match in the whole lesson and pass if the snapshot digest is among them. The contract predicates on "the digest recorded in the round-33 lesson Gate at REV". Demonstrated hole (scratch fixture repo2-gatehole): the Gate records a different digest (`sha256: deadbeef...` with 64 hex chars) while the snapshot digest `217edd...` appears only in a later `## note` line; the counter prints `gate_sha_ok=1 C2_R33_PASS=true`, exit 0. So a lesson whose Gate never records the snapshot digest still passes if the hex string appears anywhere in the file, for example in a note, a template line, or a quoted receipt digest — the exact scenario the review asked about. This is an under-verification relative to the predicate (accepts a state the contract forbids), not a false rejection.

Smallest safe correction: scope the digest search to the Gate block — e.g., slice the lesson from the `## Gate` heading to the next heading before `findall`, and optionally require the versioned URL to appear in the same block.

### Finding 2 (moderate): row id > S099 is not enforced
The counter captures any `S[0-9]{3,}` row whose teaches opens `supersedes S055` and never compares to 99. Demonstrated (fixture repo3-oldrow): a row with id `S042` and otherwise valid content passes (`C2_R33_PASS=true`, exit 0), although the predicate requires id > S099 (the repair must be a new row, and SOURCES append-only rule 2 makes corrections new rows). Fix: parse the id integer and require > 99 before accepting the row.

### Finding 3 (low): prefix check is looser than the contract opener
`t.startswith('supersedes S055')` also accepts `supersedes S055x`; the contract literally requires the opener `supersedes S055 -`. Tighten to `startswith('supersedes S055 -')` (note the SOURCES v1 rule 2 style is `supersedes S0NN —`; the C2 contract pins the hyphen form, so match the C2 predicate).

### Finding 4 (low, residual risk): first-match break
The counter stops at the first row matching the id regex plus the supersedes prefix. If a future after-state ever carried more than one such row, the earlier one decides; a stale non-versioned supersedes row before the real repair would reject (conservative miss), and a wrong earlier row could pass. At the freeze rev zero rows contain `supersedes S055` (grep over REV SOURCES: no matches), so today only the intended new row can match; this is a residual risk, not an active failure.

### Finding 5 (evidence hygiene): the committed before receipt was produced by an older draft of the counter
`.ufo/evidence/round-33/before/c2-at-base.stdout` contains two `FutureWarning: Possible nested set` lines referencing a `ROW_RE = re.compile(r'^\|[[:space:]]*...|', re.M)` at line 26, but the frozen counter has no `ROW_RE` and no `[[:space:]]` (it uses `\s` inline and emits no warnings). The counter did not exist at base 66e1fb44 (git show of the path at base fails), so the before receipt was generated with a pre-freeze draft. The verdict line and exit are unchanged (row=none, PASS=false, exit 1), so semantics agree; recommend regenerating the before receipt with the frozen counter for byte-exact evidence.

## Overall verdict
The counter is sound on the positive path (a correctly authored repair row S101+ with a versioned URL, the committed snapshot, and the Gate recording the snapshot digest will pass) and conservative on most failure paths (missing snapshot, missing lesson, unversioned URL, absent row all yield false/exit 1). Two under-verification gaps relative to the C2 predicate are demonstrated: the Gate digest binding (Finding 1) and the id > S099 requirement (Finding 2). Neither blocks the honest after-state; both weaken rejection of nonconforming states. Recommend tightening Findings 1 and 2 in the counter before the data seat (or an explicit documented deviation), and regenerating the before receipt per Finding 5.

## Verification gaps
- The counter does not verify that the row's URL and the Gate's URL are the same version, nor that the snapshot's actual page version matches the row URL; the pinned digest plus quote binding make a wrong-version pass implausible today but not logically excluded.
- Uppercase-hex digests in a lesson would be missed (conservative direction; not exercised).

Evidence artifacts live under `/fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-ReviewCounterB-4/` (receipts, rev/base extracts, fixture repos repo1–repo4 with run outputs and exit files).
