# R07 — R16-EV1 runner-sha receipt: stale value, correct value, pin surface, correction draft

Seat: `TameshiR17.R07RunnerShaReceipt` (wave 1, round 17). Lane tip read:
`98bea7da5801f4bc58e4187690ee1687c8a5061f`. Read-only: this report is the only lane write. No
tool was installed or upgraded; no `jj`/git write was run; no runner command was re-executed.

## 1. The two values (confirmed)

| Fact | Command | Observed |
|---|---|---|
| Receipt at tip | `git show 98bea7d:.ufo/evidence/round-16/round-gate/runner-sha256.txt` | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594  tools/mutate-and-run.sh`; 1 line, 90 B, file sha256 `c0a6203beb70627f2e77c6434ab41d2798d6727137bbfb05f143a4d3c76f5754` (same blob at `c699c8c`) |
| Stale value is the c699c8c runner | loop over `git log --all --format=%h -- tools/mutate-and-run.sh`, `git show <c>:tools/mutate-and-run.sh \| sha256sum` | only `c699c8c` hashes `89722ddb…` (1726 lines); every later revision differs |
| Correct value — 05a2247 | `git show 05a2247:tools/mutate-and-run.sh \| sha256sum` | `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa` (1739 lines) |
| Correct value — 09ee1d0 | `git show 09ee1d0:tools/mutate-and-run.sh \| sha256sum` | `0673d2e5…8118aa` |
| Correct value — 017a2b0, tip 98bea7d, live tree | `git show <rev>:… \| sha256sum`; `sha256sum tools/mutate-and-run.sh` | `0673d2e5…8118aa` for both revs and the worktree (`git status --porcelain tools/` clean) |
| Commit that moved the runner | `git diff --stat c699c8c 05a2247 -- tools/mutate-and-run.sh` | `+19/−6`; body adds the leg-count agreement check (`# r16: leg-count agreement …`); selftest 81/81 → 83/83 |
| Receipts that already carry the right sha | `nl -ba` both files | `runner-regression.txt:1` checksum line and `:2` `REGRESSION_TOOL … sha256=0673d2e5…`, `:3` `REGRESSION_DATE: 2026-10-20T14:13:30Z`; `runner-selftest.txt:84` `MUTATE_SELFTEST: 83/83 pass`, `:87` `0673d2e5…  tools/mutate-and-run.sh` |
| Scope of the stale literal | `git grep -l "89722ddb" -- . ':!.ufo/waves'` | four files: this receipt, `corpus/knowledge/fleet-kill-rate-ledger.md`, `corpus/knowledge/repeated-control-precondition.md`, `corpus/lessons/round-16-verifier-spotcheck.md`. The receipt is the only instrument-side record; the other three are prose. |

`05a2247` rewrote both companion receipts to `0673d2e5…` (and added the selftest's trailing checksum
line, absent at `c699c8c`) but left `runner-sha256.txt` untouched — its git history is only `c699c8c`.
That is the whole defect: one stale line, no second carrier.

## 2. Pin surface — nothing pins this receipt

- **Its own digest:** `git grep -n c0a6203b…` and the 16-hex prefix both return `NONE`;
  `git log --all -S c0a6203b… -- .` is empty. The digest of the live-appended file
  (`9758a1d8…`, §3) is also unpinned.
- **Path references:** `git grep -n "round-gate/runner-sha256"` hits only `.ufo/waves/**` (round-16/17
  reports, which are records) and `corpus/lessons/round-16-verifier-spotcheck.md:65,234` (the routed
  defect). No executable reference.
- **Tools:** `git grep -n "round-gate\|runner-sha256" -- tools/` returns only the runner's embedded
  `js-round-gate` leg and spec (`tools/mutate-and-run.sh:15,91,204,547,901-907,968,1180,1220-1223,1678`).
  `:904` names the sibling `round-gate.defects.spec` (pinned `e99b87eb…`), not this receipt. No tool
  opens `runner-sha256.txt`.
- **Checksum manifests:** the only `sha256sum -c` invocations in the tree are a replay note
  (`.ufo/evidence/round-16/Overlap1/manifest-replay.txt:2`) and wave-report quotations; the manifest
  it names (`.ufo/evidence/round-16/Overlap1/manifest.sha256`, 30 lines) has no runner/round-gate
  line (`grep -n "runner\|round-gate"` → none). The other checksum sidecars (`.ufo/evidence/round-13/
  pin-manifest.json`, round-12 witness `manifest.json`s, `.ufo/evidence/kaika-round-1/coldread/
  SHA256SUMS.txt`) name no path under `.ufo/evidence/round-16` (`git grep -n
  "round-gate/runner-sha256"` → only waves/lesson, per the path bullet above).
- **Disposition/expected manifests:** `grep -rn "round-16" --include=expected*.json
  --include=dispositions*.json .` → none; `.ufo/evidence/round-14/dispositions.json` pins three
  round-13 evidence files; no `expected.json` exists in round-14 or round-16.
- **Registered commands:** `tools/registry.json` and `tools/registry-check.py` do not exist at
  `98bea7d`, and neither `SKILL.md` nor `SCORECARD.md` names the receipt (`SKILL.md` grep → none), so
  no registry row sourced from the interface-B sources can pin it. `.ufo/state/` has no reference.

## 3. Live tree already carries an append (not mine, verified accurate)

`git status --porcelain` reports ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`;
mtime `2026-10-20 12:21:34.984 -0300`, 5 lines, 553 B, sha256
`9758a1d89fd301dd93095a611eb1738a9a9afeebba2c6dbe28cfdbb04a764d99`. The `git diff` append is:

```
# correction 2026-10-20 (round 17, routed R16-EV1; corpus/lessons/round-16-verifier-spotcheck.md §2, §6 item 5): the line above is the
# c699c8c runner. 05a2247 moved the runner; runner-regression.txt and runner-selftest.txt were re-run on it and carry this sha.
# The runner at 05a2247, 09ee1d0, 017a2b0 and 98bea7d (git show <rev>:tools/mutate-and-run.sh | sha256sum):
0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa  tools/mutate-and-run.sh
```

Every factual claim in it checks out against §1 (all four cited revs and both receipts). Its one
format consequence: the final line is a second machine-readable checksum record, so
`sha256sum -c .ufo/evidence/round-16/round-gate/runner-sha256.txt` now prints
`FAILED` then `OK`, rc 1 (committed blob: a single `FAILED`, rc 1). No consumer exists, so this is
not a defect today, but the file is no longer a one-record manifest. **Do not append a second
correction block.** Either commit this append as-is, or replace it (pre-commit; still an append to
the committed base) with the comment-only draft below.

## 4. Exact correction text (draft)

Comment-only form — the file keeps exactly one machine-readable record, so `sha256sum -c` remains a
single unambiguous `FAILED` on the stale line. Byte-exact result: 9 lines, 885 B, sha256
`1ae4df1d0ab63f23902750679f03d099a0217cebabc682877488845800e857d3`; `sha256sum -c` from the lane
root prints one `FAILED`, rc 1 (verified from a `/tmp` copy).

```text
89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594  tools/mutate-and-run.sh
# correction 2026-10-20 (round 17, R16-EV1; this file: .ufo/evidence/round-16/round-gate/runner-sha256.txt,
# per corpus/lessons/round-16-verifier-spotcheck.md sections 2 and 6 item 5). The checksum above is
# tools/mutate-and-run.sh at c699c8c (round-16 landing, leg 7). 05a2247 moved the runner (leg-count agreement
# check; +19/-6 lines; selftest 81 -> 83 cases). The landed runner, verified with
# git show <rev>:tools/mutate-and-run.sh | sha256sum at 05a2247, 09ee1d0, 017a2b0 and 98bea7d, is
# 0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa  tools/mutate-and-run.sh
# and runner-regression.txt:1 plus runner-selftest.txt:87 carry that same sha. Comment-only on purpose:
# sha256sum -c then reports exactly one record (the stale line above, FAILED), not an OK/FAILED mix.
```

If the L1 keeps the live append of §3 instead, the end-state digest is `9758a1d8…`; the facts are the
same and neither form is pinned anywhere.

## 5. Is appending safe? — Yes

- No committed file or registered command pins the receipt's digest (§2), and nothing reads the
  path except prose reports and the lesson.
- The append changes the receipt's own digest (`c0a6203b…` → `9758a1d8…` live, or `1ae4df1d…` draft);
  no pin depends on it.
- History is not rewritten: the round-16 bytes stay reachable at `98bea7d` (`c0a6203b…`) and at
  `c699c8c`; the correction is a new blob in the round-17 commit, which is the routed repair.
- `sha256sum -c` exits 1 in every version (the recorded sha is stale against today's runner). The
  append changes the printed lines, not the exit class.
- Conditions: append only (line 1 is the record and must not be edited); one correction block, not
  two (§3); if the §4 draft is adopted, replace the uncommitted live append rather than stack it.

## 6. Residual risk and gaps

- I did not re-run `--regression` or `--selftest`; the receipts are read as records and their sha
  lines verified directly. An unrun check is not claimed as run.
- Attribution of the live append rests on mtime and its absence from every peer report
  (`grep -rn "# correction" .ufo/waves/round-17/` → none outside dispatch/spec). [INFERENCE] it is
  an integrator-side edit in flight.
- `sha256sum 0.8.0` on this host skips `#` comment lines (valid line + comment → `OK`, rc 0) and
  evaluates every checksum line (valid + stale → `OK`/`FAILED`, rc 1). A GNU coreutils host may warn
  on comment lines; nothing consumes the file, so the exit class is unchanged.
- A future registry row could be written to read this receipt; none exists at the tip.

## 7. Verdict

built — stale value confirmed (`89722ddb…` is the `c699c8c` runner), correct value confirmed
(`0673d2e5…` at `05a2247`, `09ee1d0`, `017a2b0`, `98bea7d`) and corroborated by both companion
receipts; nothing pins the receipt's digest, so appending is safe; the live tree already carries a
verified append, so commit one correction, not two.
