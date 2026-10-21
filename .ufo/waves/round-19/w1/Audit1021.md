# Audit1021: round-18 retained receipt `audit-1021` (tameshi r19 a1, w1, advisory)

Seat `TameshiR19-2.Audit1021` (reviewer, read-only), 2026-10-21. These findings are advisory and do not close anything. The verdict below is a recommendation.

## Scope opened

- `.ufo/evidence/round-18/final/audit-1021.stdout` (6574 B), `audit-1021.stderr` (0 B), `.ufo/evidence/round-18/coldread/traces/L1/audit-1021.json` (5837 B).
- Ledger entry `.ufo/evidence/round-18/coldread/ledger.json:12085-12128` (the only entry citing this trace), plus the report entry it cites, `.ufo/waves/round-18/w3/L1Residual.md:162-213` (and header `:3`).
- Goal context `corpus/lessons/round-18-verifier-spotcheck.md:180-208`.
- Read-only git plumbing (`cat-file`/`rev-parse`/`log`/`diff`/`merge-base`, `GIT_*` stripped, `GIT_OPTIONAL_LOCKS=0`), used only to test the trace's rev/input claims. I read no other receipt content and ran no `jj`. The receipt argv was not executed.

## Recommendation

The byte, revision and input binding **holds**. The receipt's `VERIFIED` line **overclaims**: its two clauses are printed unconditionally and its own program checks neither (M1). C1 as delivered at `21e79329` (refs/heads/master) **does not invalidate** this historical evidence (see §C1).

## Established (observed)

| # | Fact | How |
|---|---|---|
| B1 | stdout sha256 `721d9beb4baae817c62d433df46885aa30e7571a0292a3c1562f92452dba7ddd`, 6574 B, 72 lines, last line `VERIFIED …`; stderr empty (`e3b0c442…b855`); trace sha256 `5b619053e6e7…` | `sha256sum`, `stat` |
| B2 | The pair and the trace were introduced only in `a134a09` (2026-10-20 18:47:13 -0300, sole parent `a9c94c5c`). They are byte-identical at `a85f710`, `7243e7f1` (frozen baseline), `78b99dd`, `21e79329` (tip) and live. | `git log -- <path>`; blob sha256 per rev |
| B3 | No record in the lane holds the stdout or trace digest. Trace keys are `schema argv cwd root rev rev_reason exit tracked_filter env_overrides inputs untracked external live_lane_reads dropped_home_count`, with no stdout/stderr digest. The ledger and report entries carry none either. grep `721d9beb\|5b619053e6e7` over the lane gives 0 matches. | grep, JSON keys |
| B4 | **argv→stdout binding:** stdout is byte-for-byte equal (6574 B) to the argv's `print` statements rebuilt over `a9c94c5c` blobs, plus the literal VERIFIED line. Spec `{start:1021,end:1067}` has 15 paths. OPEN order equals spec order. 15/15 OPEN `sha256=`/`bytes=` equal the blobs at R. SECTION text equals `SKILL.md@R` lines 1021–1067. Knowledge-ledger first line and `TAIL` (last 700 chars) equal the blob. | python over `git cat-file blob` (code below) |
| B5 | Trace `inputs` (16) are exactly the spec paths plus `SKILL.md`. All 16/16 sha256 equal the git blobs at `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`, with `SKILL.md@R` = `1334c512…`. `untracked`/`external`/`live_lane_reads` are empty and `dropped_home_count` is 0 (tracer self-reports, see I2). | same |
| B6 | Ledger entry: `read_rev` equals trace `rev`. `inputs` equals trace inputs minus `SKILL.md` (`inputs_dropped:["SKILL.md"]`). `skill_sha256` equals the trace's `SKILL.md`, which equals `_meta.expect_skill_sha`. R is in `_meta.read_revs`. `commands_executed_count:1` matches the one trace. The entry is identical at `a134a09`, `a85f710`, `7243e7f1`, `21e79329`. Report entry: `opened` equals the spec paths in order, `inputs` equals the ledger inputs, and `read_rev`/`skill_sha256` match. | JSON compare at each rev |
| B7 | Ledger `end:1068` vs argv `end:1067` is **not** a coverage gap. Ledger section sha `60d65824…` equals sha256(`"\n".join(SKILL.md@R lines 1021..1067)`), and five other framings (including 1021..1068) differ. So the ledger `end` is exclusive [INFERENCE from the unique hash match]. Line 1068 is blank; 1069 is `### Triggers T1–T3 …`. | 6-variant hash test |
| B8 | `a9c94c5c` is a commit and an ancestor of `7243e7f1` and of `refs/heads/master` `21e79329`. It is also held by `refs/jj/keep/a9c94c5c…`, so it is reachable and not prunable. | `merge-base --is-ancestor`, `for-each-ref` |
| B9 | R was committed 18:46:21. Lane mtimes: trace 18:46:59.816, stdout/stderr 18:46:59.821. The receipts landed 14 s later in R's child. | `stat`, `git log` |

**The run establishes these, given exit 0 (trace), empty stderr and the VERIFIED line present:**

- `SKILL.md@R` 1021–1067 is exactly the printed 47 lines.
- The 15 opened files have the printed digests and sizes at R.
- These 9 predicates held over 9 R blobs:
  - registry `held==total==31`
  - probes `open=0 closed=11 total=11`
  - regression `cases=8 passed=8`
  - historical `cases=4 passed=4`
  - case7 and case8 `killed=5 survived=5 inconclusive=0 kill-rate=50%`
  - disposition `status=='clean'`
  - before `status=='failed'`
  - repeat contains `controls_match`

**The run does not establish:**

- Execution of any round-18 final receipt: no `*.stderr`, no exit code and no run trace is opened.
- "same instrument blobs" for ancestor runs.
- Any pin-read rule of the section.
- The section's dated 2026-10-14 executed instance.
- Interpreter identity.

## Findings by severity

### M1 (Medium, calibration): the VERIFIED line is an unconditional literal, and both clauses exceed the program's checks

- **Where:** trace `argv[29]` (the `python3 -c` program; `argv[30]` is the spec JSON), final statement `print('VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision')`; stdout:72.
- **Observed:** the 9 asserts above are the only checks.
  - The tool hashes at R are printed but never compared to any other revision or run.
  - The trace input map (16 paths) has nothing under `coldread/traces/` and no `*.stderr`. The run traces `traces/L1/{before,case7,case8,context,disposition,historical,regression,repeat,bash-witness}.json` were committed with the receipts in `5923d89` but never opened.
  - 6 of the 15 opened files have no predicate: `tools/pin-disposition.py`, `tools/mutate-and-run.sh`, `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-13/pin-manifest.json`, `final/context.stdout` and `final/checks.json`.
- **Concrete failing case:** the `final/checks.json` this audit opened has sha `fed3c8e6…`, identical at R, at `4b7c682` (the spot-check revision), and at `7243e7f1` and `21e79329`. That is the same bytes the spot-check found carrying a failed selftest row: "`final/checks.json` records `bash-witness-selftest` argv exit 64 with an empty stdout" (`round-18-verifier-spotcheck.md:196-197`, committed 2026-10-21 00:51 -0300). The audit printed "VERIFIED actual execution receipts" over that bundle and had no check that could fail on it. The exit-64 content comes from that source; I applied it here by hash identity and did not read `checks.json`.
- **Failing criterion:** a receipt verdict that names a property needs a check that can fail on that property.
  - "ancestor runs have the same instrument blobs": no check.
  - "actual execution receipts": only content substrings are checked.
- **Independent check (mine, not established by the receipt):** git blob ids are equal at `921ef807`, `5923d89` and `a9c94c5c`: `tools/pin-disposition.py` `89a6ca38…`, `tools/mutate-and-run.sh` `fd1a63a3…`. `git diff --name-status 921ef807 a9c94c5c -- tools` is empty. So the ancestor clause is true at the blob level but unestablished here. Whether those runs executed these blobs is recorded, if anywhere, in their unopened traces.
- **Disclosure exists only in report prose:** "This is input-keyed evidence, not complete required-command coverage." (`L1Residual.md:3`, `a134a09`, 2026-10-20). The receipt text carries no such bound.
- **C1 consequence:** C1's audit must not cite audit-1021's VERIFIED line as evidence about `checks.json`/defect 4, or about execution of the round-18 final receipts.

### L1 (Low, calibration): the instruction-class verdict rests on a command that runs no rule of the section

- Section 1021–1067 defines `current`/`stale`/`drift` through:
  - `git rev-parse … refs/heads/<branch>^{commit}`
  - `git show <tip>:<path>`
  - `git status --porcelain`
  - `jj-lane.sh state`
  - tool `held`/`moved` against the last `REGRESSION_TOOL`/`MUTATE_TOOL` line
- The program starts no subprocess, and the environment is `env -i` with `--unshare-net`. It prints the section and checks round-18 receipt substrings.
- Ledger fields: `class:instruction`, `verdict:gap-minor`, `blocking_gaps:0`, `wrong_expectations:0`, `commands_executed_count:1`. A consumer reading only these fields could take the instruction as exercised. Prose discloses the limit: "not a blind non-author cold read" (`L1Residual.md:170`).
- This is residual risk and not one of the five C1 defects. No action is assigned here.

### L2 (Low, informational): `env_overrides` does not describe the child's effective environment

- `env_overrides.set.PYTHONPYCACHEPREFIX=/tmp/trace-inputs-run-ku5lfdj0/pycache` is discarded by the argv's `env -i`.
- `git_vars_removed` lists `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_NOSYSTEM`, which the argv sets again to `/dev/null` and `1`.
- python3's effective environment is exactly the 8 `env -i` assignments in the argv.
- No effect on stdout: the program imports only `pathlib`/`hashlib`/`json`/`sys` and starts no process.

### I1 (Info): interpreter and sandbox identity are not recorded

- The argv `PATH` starts with user-writable shim dirs (`~/.grok/bin`, `~/.kimi-code/bin`, mise shims). The trace records no python3 or bwrap path, version or hash.
- Today (2026-10-21), `command -v python3` under that PATH resolves to `/usr/bin/python3` → `python3.14`. That is current state, not the historical one.
- Output depends only on stdlib semantics [INFERENCE]. This is a reproducibility gap only.

### I2 (Info): tracer self-reports are not verifiable within scope

- `external:{}` and `live_lane_reads:{}` are reported by the tracer. python3 has to read its stdlib outside `root`, so `external:{}` implies a filter that the trace does not record [INFERENCE]. I did not read the tracer (out of scope).
- The program text uses only paths relative to the scratch `cwd`, so live-lane reads cannot come from the program text.

### I3 (Info): the pair↔trace binding is by name, not by digest

- Per B3, the binding rests on the filename stem, the co-commit `a134a09`, the mtime adjacency (5 ms), and B4's byte reconstruction.
- Git history (B2) is the only integrity anchor for the stdout bytes, and it shows no modification since landing.

## C1: could the repairs invalidate this evidence?

**No, as delivered.** I checked `21e79329`, which equals refs/heads/master, and the live tree for these paths on 2026-10-21.

1. The evidence is bound to commit `a9c94c5c`. Descendant repairs cannot change it, and it stays reachable (B8).
2. The pair, trace, ledger entry and report entry are unchanged from `7243e7f1` through `78b99dd` and `21e79329` to live (B2, B6).
3. All 15 non-SKILL inputs are byte-identical at R, `7243e7f1`, `78b99dd`, `21e79329` and live.
   - C1 edits `corpus/knowledge/guard-kill-closure.md`, `corpus/knowledge/mutation-case-kumitate-sources-check.md` and `corpus/lessons/round-18.md` (defects 1–3). None of them is an input.
   - Defect 4 is repaired by **appending** `.ufo/evidence/round-19/bash-witness-selftest{,-complete}.{json,stdout,stderr}`. `final/checks.json` stays `fed3c8e6…`, so the input is preserved.
4. `SKILL.md` goes from `1334c512…` to `4d0190fd…` in a single hunk, `@@ -1934,0 +1935 @@`, which lies after the section. At `21e79329` and live the heading is still at line 1021, and lines 1021–1067 hash to `60d65824…`. The `section_sha256` carry (`_meta.carry_coverage_basis`) and the line anchors both hold.

**What would invalidate it (none of these happened):**

- (a) An in-place rewrite of `final/checks.json` or any other input. The R-bound claim would still be true, but replaying the input map against live would fail. The contract requires errata to be appended instead.
- (b) Any byte change inside `SKILL.md` 1021–1067. The section hash would change and the retained read would drop. The precedent is commit `a85f710`: "lesson citation edit invalidated one retained read" (2026-10-20 18:47:45 -0300).
- (c) An insertion before line 1021. The `start:1021` and `SECTION 1021 1067` anchors would shift, although the hash carry would survive.
- (d) Rewriting history so `a9c94c5c` becomes unreachable.

**The other direction:** this receipt cannot count as failure-capable evidence for any of the five C1 defects (M1).

## Verification gaps and residual risk

- **Not read (outside scope):** the nine round-18 run traces, the tracer tool, `checks.json` content and the other receipts.
- **Not re-performed:** execution. Exit 0 is a tracer self-report. The stdout bytes are consistent with the argv over R, but consistency is not proof that the command ran.
- **Scratch `/tmp/tameshi-r18-L1-final-a2vitd82` still exists.** HEAD is `a9c94c5c` and 16/16 input hashes equal the trace. `registry-branch-aligned.stdout` and `.git/index` have mtimes 18:46:59.425/.426, 0.39 s before the trace was written. This is mutable post-hoc state, so it is corroboration only.

## Commands (read-only, 2026-10-21) and outcomes

- `stat -c … ` and `sha256sum` on the three files gave the values in B1.
- `git for-each-ref`; `git cat-file -t a9c94c5c… / 7243e7f1…`: both commits. `a9c94c5c` is pinned by `refs/jj/keep`. master is `21e79329`.
- `git merge-base --is-ancestor a9c94c5c 7243e7f1` and `… 21e79329`: both true.
- `git log --format=… -- <pair/trace>`: `a134a09` only. `git log -- ledger.json L1Residual.md`: `a134a09`, `a85f710`.
- `git diff --name-status 7243e7f1 21e79329`: C1 file set. `git diff -U0 7243e7f1 21e79329 -- SKILL.md`: one hunk `@@ -1934,0 +1935 @@`.
- `git diff --name-status 921ef807 a9c94c5c [-- tools]`: 53 files, no `tools/` change. `git rev-parse <rev>:tools/{pin-disposition.py,mutate-and-run.sh}` at `921ef807`/`5923d89`/R: identical.
- `env -i PATH=<trace PATH> /usr/bin/sh -c 'command -v python3'`: `/usr/bin/python3` → `python3.14`. This resolves a name only; the receipt argv was not run.
- Investigation code (eval kernel, no files written). Core of the B4/B5 checks:

```python
blob=lambda rev,p: run(['git','-C',L,'cat-file','blob',f'{rev}:{p}']).stdout
spec=json.loads(trace['argv'][-1]); skl=blob(R,'SKILL.md').decode().splitlines()
parts=[f"SECTION {spec['start']} {spec['end']}\n", '\n'.join(skl[spec['start']-1:spec['end']])+'\n']
for p in spec['paths']:
    b=blob(R,p); parts.append(f"OPEN {p} sha256={sha256(b)} bytes={len(b)}\n")
    if p.startswith('corpus/knowledge/'): parts += [b.decode().splitlines()[0]+'\n', 'TAIL '+b.decode()[-700:]+'\n']
assert ''.join(parts).encode()+b'VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision\n' == stdout   # held
assert all(sha256(blob(R,p))==h for p,h in trace['inputs'].items())                                                                                 # held (16/16)
assert sha256('\n'.join(skl[1020:1067]).encode()) == ledger_entry['sha256']                                                                        # held; 1021..1068 variants differ
```

No tools were installed or updated, and no production, ref, index or jj state was touched. The only file written is this report.
