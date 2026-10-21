# Audit131 — round-18 `audit-131` receipt pair, trace and ledger entry (advisory)

Seat `TameshiR19-2.Audit131` (reviewer, read-only), 2026-10-21. Tameshi round 19 attempt 1, BUILD advisory wave, C1 boundary.
This is advisory evidence, not closure. Nothing was re-executed: I did not run the receipt argv, bwrap, the tracer, or any lane gate, selftest or measure tool.
No production, Git/JJ or ref writes were made. No tools were installed or updated.
No `lsp` device is mounted in this session. Tool semantics below come from the tools' own docstrings and from committed outputs. They are text reads, not semantic proof.

`L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Every git call below was read-only, with GIT_* removed and `GIT_OPTIONAL_LOCKS=0`.

## Axes
A1 stdout↔trace binding · A2 revision/input facts · A3 claim honesty of the receipt · A4 C1 invalidation risk.

## Verdict
**Historically valid; bound by input, not by output; its closing line overclaims.**
All 17 traced inputs equal the blobs at the read revision `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`. I reconstructed the retained stdout byte-for-byte from those blobs.
C1, as delivered at `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`, does not invalidate this evidence. It does make the evidence stale at the tip, and the C1 text already says so.

## Commands / sources and observed outcomes

| # | Source / command | Observed |
|---|---|---|
| 1 | `sha256sum` and `stat` on `.ufo/evidence/round-18/final/audit-131.{stdout,stderr}` and `coldread/traces/L1/audit-131.json` | stdout `b39aa459c7bd2de5f99921ea957ed0eae93df3e10687d980b7728ad1e2f8c541`, 11642 B. stderr 0 B (`e3b0c442…b855`). trace `ebc2c799…deae8`, 6023 B. Worktree mtimes: trace 18:46:59.520, pair 18:46:59.525 (-03:00). |
| 2 | Searched the whole lane for `b39aa459` (`grep`, gitignore off) | **No match.** The stdout digest is recorded nowhere: not in the trace, the ledger, or `L1Residual.md`. |
| 3 | `git log --diff-filter=A refs/heads/master -- <pair, trace>`; `git show REV:path` at a134a09, a85f710, 4b7c682, 7243e7f and master | Added in `a134a09` (2026-10-20T18:47:13-03:00), whose sole parent is `a9c94c5` (18:46:21). Byte-identical at every listed revision and in the worktree. Absent at `a9c94c5`. |
| 4 | Trace fields (`audit-131.json:2-74`) | `rev` = a9c94c5, `rev_reason` null, `exit` 0, `tracked_filter` true, `untracked`/`external`/`live_lane_reads` empty, `dropped_home_count` 0, 17 `inputs`. Per `tools/trace-inputs.py:527-541`, `rev` is the scratch root's HEAD after a toplevel==root identity check. There is no worktree-clean check. |
| 5 | Each of the 17 trace inputs: `sha256(git show a9c94c5:<p>)` | **17/17 equal.** This includes `SKILL.md` = `1334c512…c1e0` = the ledger's `skill_sha256`. |
| 6 | Independent reconstruction of the expected stdout from the a9c94c5 blobs, using my own code (below), not the receipt argv | **Byte-identical**: 11642 B, sha `b39aa459…c541`. 16 OPEN lines, in spec order, all equal to the trace inputs. All 9 assert conditions hold on the blobs. The stdout is fully determined by argv plus rev. |
| 7 | Section digest checks against `SKILL.md@a9c94c5` | stdout lines 2–115 equal SKILL lines 131–244. `sha256("\n".join(131..244))` = `c7247157…b6d6` = ledger `sha256`. Line 245 is blank and 246 is the next heading, so ledger `end: 245` and argv `end: 244` denote the same text. **Not a gap.** |
| 8 | Ledger entry (`coldread/ledger.json:11956-12000`; entry index 142 at 4b7c682) | `L1Residual`, `instruction`, `gap-minor`, `commands_executed_count: 1`, one trace, 16 inputs equal to the trace (SKILL.md in `inputs_dropped`). Identical from a134a09 to master. |
| 9 | Program text (`audit-131.json:33`, raw) | Content assertions cover 9 of the 16 opened files: registry-branch-aligned, probes, regression, historical, case7, case8, disposition, before, repeat. Seven files are only hashed or printed: kimi and kagi notes, `corpus/README.md`, `tools/mutate-and-run.sh`, `predictions.json`, `context.stdout`, `checks.json`. The program contains no `git`, `subprocess` or cross-revision operation. |
| 10 | `git show a9c94c5:.ufo/evidence/round-18/final/checks.json` | The `bash-witness-selftest` row has argv `tools/bash-witness-study.py --selftest`, `exit` **64**, and `stdout_sha256` equal to the empty-string digest. This is round-18 §5 defect 4, inside a file that audit-131 marked VERIFIED. |
| 11 | `git diff --name-status 921ef807 a9c94c5`; `git diff --name-status 5923d89 a9c94c5`; `merge-base --is-ancestor` on both | Both are ancestors. The diffs add only `.ufo/evidence/round-18/final/*` and `coldread/traces/L1/*`, plus M `SKILL.md` and M `corpus/lessons/round-18.md`. No tool or script path changed. |
| 12 | Section-131 entries at 4b7c682, recomputed against blob drift; `.ufo/evidence/round-19/round18-final-measure.stdout:1287-1299` | 3 entries. CR07 (carried) and CR06 (`wrong_expectations: 1`) show input drift on `corpus/README.md`. L1Residual (audit-131) has no drift. The committed measure shows `credited`, reasons `["credited","input-drift:corpus/README.md","wrong-expectations:1"]`, not vetoed. |
| 13 | `CR06.md:79-80` vs recomputation | CR06 reports a digest mismatch, quoted: "The assignment-supplied exact-range digest c7247157… does not match the captured lines 131-244 bytes". The same lines hash to `ab4dad0c599585…` when a trailing newline is added. CR06's wrong expectation is a hashing-convention artifact, not a section-text defect. |
| 14 | `git diff 7243e7f refs/heads/master` on audit-131 inputs | 15/17 unchanged. `SKILL.md` gains +1 table row at line 1935 (section 131 is still identical at lines 131–244, sha `c7247157`). `corpus/README.md` gains +17 lines appended after line 281. `checks.json` and the other 11 round-18 receipts are unchanged. |
| 15 | `test -e` on the scratch directories | `/tmp/tameshi-r18-L1-final-a2vitd82` is present (mutable; not read; not evidence). `/tmp/trace-inputs-run-conoc004` is absent, consistent with `trace-inputs.py:47-48`. |

## Findings by severity

### M1 — The receipt's closing verdict is a literal and overclaims (A3)
The final stdout line, `audit-131.stdout:157` (2026-10-20), reads:
"VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision"

This line is a constant `print` in argv. Nothing in the program compares blobs across revisions (row 9). Nothing in it can establish that a receipt came from an actual execution, either. The program only checks substrings and JSON fields in committed files.

Seven of the sixteen opened files get no content check. One of them, `checks.json`, carried defect 4 at this revision (row 10), and the audit still printed VERIFIED. The receipt is therefore failure-incapable for defect 4, and for anything else in those seven files.

- **Failing criterion:** a receipt's verdict line must be computed by its own argv.
- **Independent check, outside the receipt:** the ancestor clause holds for 921ef807 and 5923d89 over tracked files (row 11). It is unknown for any other producing revision and for any untracked instrument.
- **Measured-number impact:** none. The measure never reads stdout text.
- **Routing:** this is not one of C1's five items, so route it to a later round. The fix is an appended, dated, named erratum. Never rewrite the receipt.

### L1 — The stdout and stderr are not cryptographically bound to the trace (A1)
The `tameshi-trace-inputs-v1` schema has no output fields (`trace-inputs.py:7-16`). The ledger entry and `L1Residual.md` cite only the trace path, and the stdout digest appears nowhere (row 2). The pairing rests only on the filename stem `audit-131` and on both files being added in the same commit, `a134a09`.

**Mitigation, observed:** the stdout carries no independent information, because it is byte-reproducible from argv plus `a9c94c5` (row 6). The facts that this run actually happened are carried by the trace alone: strace-derived inputs and `exit: 0`. The empty stderr is consistent with that, since a failed assert would leave a traceback.

Round 19's `.ufo/evidence/round-19/round18-final-measure.json:13-14` does bind `stdout_sha256` and `stderr_sha256`. That is the better shape. audit-131 predates it.

### L2 — C1 item 5 inherits this entry, which is not blind (A4, residual and disclosed)
At 4b7c682, section 131 is credited only through this L1Residual entry. Both non-author entries are stale through README drift (row 12). C1 item 5's exact-revision receipt (`round18-final-measure.json`, `--rev 4b7c682`) therefore depends on audit-131 for one of its 60 sections.

[INFERENCE from `measure.py:56-76`] Without this trace, section 131 would be uncovered at 4b7c682. That gives 59/60, `box3_full_page` false, and restraint 6 by `measure.py:26-29`.

The single command executed none of the recipe's ten steps. The credit is input-keyed only, and this is disclosed. `L1Residual.md:3` (2026-10-20) says: "This is input-keyed evidence, not complete required-command coverage."

The suppressed CR06 veto is not hiding a defect in the section text (row 13).

### I1 — `env_overrides` does not describe the child's effective environment (info)
argv runs `env -i`, which re-sets `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_NOSYSTEM` (listed in `git_vars_removed`) and drops `PYTHONPYCACHEPREFIX` (listed in `set`). The effective environment is the literal argv list.

The interpreter path and version are not recorded. `dropped_home_count: 0` rules out a successful `/home` exec only.

This is immaterial to the output, which is deterministic.

## Could C1 repairs invalidate this historical evidence?

**Not as delivered, and not by any forward commit.**

- The measure reads blobs only at an explicit commit, with no worktree access (`measure.py:9-10`).
- a9c94c5, a134a09 and 4b7c682 are all ancestors of local and remote master `21e7932`.
- The receipt pair, the trace and ledger entry 142 are unchanged through master (rows 3 and 8).
- Of audit-131's 17 inputs, C1 touched only `SKILL.md` and `corpus/README.md`, and both edits are append-only (row 14).
- C1 handled defect 4 by adding round-19 receipts. It did not edit `checks.json` in place (`fed3c8e6…` is unchanged).

**Consequence at the tip.** Under the strict rule, this entry is `input-drift:corpus/README.md` at `21e7932`, and so are the other two section-131 entries. [INFERENCE from `measure.py:47-55,72-76`; measure not executed] Section 131 has no live credit at the tip, so a tip-level run would not reach 60/60 or calibration 8.

C1 already confines the claim to the historical revision. SCORECARD's round-19 block (2026-10-21) says: "Calibration remains **8**, a dated historical score; independent promotion and a current-page cold-read are not claimed."

**What would invalidate it:**
- rewriting or GC-dropping a9c94c5, a134a09 or 4b7c682;
- or editing the round-18 receipts or the ledger in place. That would break the preserved-evidence contract and the binding at the worktree level.

Verifiers must check against blobs at `a9c94c5`, not against tip files. At the tip, `SKILL.md` and `README` legitimately differ.

## Residual risk and verification gaps
- Provenance of the nine asserted round-18 receipts was not checked here: their own traces and producing revisions are out of scope. Only their committed bytes were checked.
- The worktree mtimes are uncommitted metadata and are weak timing evidence only.
- No measure or tracer run was performed, so the tip-staleness and 59/60 statements are rule-text inferences.
- No resume path or runtime rerouting is in scope for this receipt.

## Investigation code (kernel-local, read-only; receipt argv not executed)
```python
def blob(p): return git_show(f"a9c94c5:{p}")            # git show, GIT_* removed
sk = blob("SKILL.md").decode().splitlines()
exp = [f"SECTION 131 244", "\n".join(sk[130:244])]
for p in spec_paths:                                      # 16 paths from trace argv[-1]
    raw = blob(p); exp.append(f"OPEN {p} sha256={sha256(raw)} bytes={len(raw)}")
    if p.startswith("corpus/knowledge/"):
        exp += [raw.decode().splitlines()[0], "TAIL " + raw.decode()[-700:]]
exp.append("VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision")
assert ("\n".join(exp) + "\n").encode() == retained_stdout  # True, 11642 B
```
