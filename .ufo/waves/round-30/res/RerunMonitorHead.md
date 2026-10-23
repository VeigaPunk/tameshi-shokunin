# RerunMonitorHead — residual review, round 30, attempt 3

Seat: RerunMonitorHead
Date: 2026-10-23
Scope: independent re-run of the calibration no-harm monitor (round-27 C1 counter) at the integrated commit 957c5ddb2af61063c8993e8aed1321cb0d54b66a, at base 9ed6db840dc97a0a5f4758b6b5f60cee83a61645, and at content revision bb681566b18211adf8ae9c28df91e17678e3f545; plus the ledger append-only check and the frozen-binding byte-identity check.

## Verdict

PASS — consistent. The monitor reproduced exactly as expected at all three revisions, the cold-read ledger append from bb681566b18211adf8ae9c28df91e17678e3f545 to 957c5ddb2af61063c8993e8aed1321cb0d54b66a is strictly append-only with the 393-entry prefix preserved as data, and `.ufo/evidence/round-30/coldread/bind-select-v3.py` is byte-identical at 9207f226e177c8a1a9a82de677df3cd9f8d1cda3 and 957c5ddb2af61063c8993e8aed1321cb0d54b66a. No defect found in scope.

## How the runs were made

Clone (own scratch seat, nothing in the lane repo touched):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin c
```

Clone dir: /fast/scratch/hyaku/tameshi-r30a3-seats/TameshiR30A3.RerunMonitorHead/c — all three revisions resolved by `git rev-parse --verify <rev>^{commit}` to the full hashes named above.

Because the counter runs the lane monitor from the working tree (`cwd=repo` in `.ufo/evidence/round-27/c1-measure.py`), each revision was checked out in its own detached `git worktree` inside the scratch clone, so the counter/monitor script version is co-resolved with the analyzed revision:

- wt-integrated at 957c5ddb2af61063c8993e8aed1321cb0d54b66a
- wt-base at 9ed6db840dc97a0a5f4758b6b5f60cee83a61645
- wt-content at bb681566b18211adf8ae9c28df91e17678e3f545

Run command (per revision, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset, wrapped in `timeout 600`, the three runs executed concurrently):

```
timeout 600 python3 .ufo/evidence/round-27/c1-measure.py --repo <worktree> --rev <full-rev-hash>
```

## Observed values

Expected receipt `.ufo/evidence/round-30/head/c1monitor-at-65b6e84f.stdout`: `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=65b6e84fd2f58ba052475d96a2bf7d14ce8ee64f`, `exit=0`.

| revision | exit | observed stdout |
|---|---|---|
| 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 (base) | 0 | `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=9ed6db840dc97a0a5f4758b6b5f60cee83a61645` |
| bb681566b18211adf8ae9c28df91e17678e3f545 (content) | 1 | `C1_MONITOR: covered=33/64 restraint=6 box3_mismatch=1 depth_score=9 rev=bb681566b18211adf8ae9c28df91e17678e3f545` + 31 `uncovered:` heading lines |
| 957c5ddb2af61063c8993e8aed1321cb0d54b66a (integrated) | 0 | `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=957c5ddb2af61063c8993e8aed1321cb0d54b66a` |

Reading of the three results:

- Integrated 957c5ddb: 64/64, restraint 8, box3_mismatch 0, depth_score 9, exit 0 — the same value shape as the receipt taken at 65b6e84f (differences only in the rev field, as expected; 65b6e84fd2f58ba052475d96a2bf7d14ce8ee64f is an ancestor of 957c5ddb, `git merge-base --is-ancestor` exit 0).
- Base 9ed6db84: identical value shape, exit 0 — the pre-edit lane state was fully credited.
- Content bb681566: 33/64 covered, restraint 6, box3_mismatch 1, exit 1 — this reproduces the stated drift ("strict monitor at bb681566: 33/64") exactly. Exit 1 is the counter's honest failure (covered != total); recorded as observed, not "fixed". The 31 uncovered headings include the widely read sections edited in that revision (for example `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`, `## Restore discipline — before/after identity, not continuous non-write proof`, `### The protocol — ordered, fail-closed`, `## The operator's runbook and the six-leg regression (round 10, measured)`).

## Ledger append-only check

Command and observed output:

```
git diff --numstat bb681566b18211adf8ae9c28df91e17678e3f545 957c5ddb2af61063c8993e8aed1321cb0d54b66a \
  -- .ufo/evidence/round-21/coldread/ledger.json
-> 3924	0	.ufo/evidence/round-21/coldread/ledger.json
```

3924 lines added, 0 deleted — append-only at the line level. Data-level check (the file is a JSON object with keys `schema`, `entries`, `carried_from`, `provenance`, `round21_provenance`; scalar fields equal at both revisions):

- `entries` count at bb681566: 393; at 957c5ddb: 456.
- First 393 entries of 957c5ddb equal the 393 entries of bb681566 as parsed data: True (prefix preserved).
- 63 entries appended; the appended records are cold-read traces whose headings correspond to the sections uncovered at bb681566 (first entries cite `skill_sha256 c46ec02e…`, headings `## Mutation-sweep recipe — numbe…`, `## Restore discipline — before/a…`, `### The protocol — ordered, fail…`), i.e. the appends are the no-harm cold reads, not rewrites.

## Frozen-binding byte identity

`.ufo/evidence/round-30/coldread/bind-select-v3.py`:

- blob id at 9207f226e177c8a1a9a82de677df3cd9f8d1cda3: `875c1834cfdac9a8b77d6c12192cc2c8d26ae299`
- blob id at 957c5ddb2af61063c8993e8aed1321cb0d54b66a: `875c1834cfdac9a8b77d6c12192cc2c8d26ae299`
- raw byte comparison of `git show <rev>:<path>` outputs: identical, 8773 bytes
- `git diff --shortstat 9207f226..957c5ddb -- <path>`: empty

The selector script was frozen before data and is unchanged through the integrated commit.

## Caveats and residual risk

- The named receipt was taken at 65b6e84fd2f58ba052475d96a2bf7d14ce8ee64f, which is not one of my three run revisions; my comparison to it is on value shape (covered/total, restraint, box3_mismatch, depth_score, exit code), plus the verified ancestor relation. Byte-equality of my stdout with that receipt file is not claimed and cannot hold (different rev string).
- The bb681566 failing read (33/64, exit 1) is the expected pre-integration state, not a defect; the no-harm repair is visible as the 63 appended ledger entries and the restored 64/64 at 957c5ddb.
- One orchestration note: the ledger file is a JSON object, not a top-level array; the first data-level check attempt sliced the object and raised. Corrected by descending into the `entries` key; all reported numbers come from the corrected check.
- No tools were installed or upgraded for this seat (nothing beyond stock git/python3 was needed).
- Scratch left in place for re-checking: /fast/scratch/hyaku/tameshi-r30a3-seats/TameshiR30A3.RerunMonitorHead/ (clone `c`, worktrees `wt-integrated`, `wt-base`, `wt-content`). All started processes exited before this report; no processes were killed.
