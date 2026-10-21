# Assemble selftest receipt audit (round 19 w1, BundleAssembleSelftest)

Audit date: 2026-10-21. Scope: only row `assemble-selftest` of
`.ufo/evidence/round-18/final/checks.json` (lines 75-84), its retained
`assemble-selftest.stdout`/`.stderr`, the CLI source
`.ufo/evidence/round-18/coldread/assemble.py`, and retained receipts that run the
same argv. The command was **not executed**. I made no production edits and
installed or updated no tools. All paths are relative to
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless absolute.

## Verdict (advisory, not closure)

The row is **effective evidence**: a successful, correctly spelled run whose
digest matches its retained output, attributable to `921ef80`. It is **not** a
failed raw attempt and does **not** repeat the R18-4 (`bash-witness-selftest`)
defect.

| Axis | Count / result |
|---|---|
| Digest match | **1/1**. Recorded `stdout_sha256` equals the retained stdout bytes. The row has no stderr digest field. |
| Argv spelling vs CLI source | **3/3 tokens agree**. The `--selftest` flag is defined and dispatched, and the CLI takes no positional arguments. |
| Revision attribution | **Correct by tool-byte identity**, with corroboration at the same revision. The row itself does not record tool sha256, cwd or time. |
| Failed raw attempt vs current evidence | **This row is current evidence.** Of 8 located observations of this tool's selftest (7 bind the tool's exit), 0 failed. |
| No-harm across round 19 | Row and streams are **byte-identical** at `5923d89`, `7243e7f` (frozen baseline) and `21e7932` (delivered). |
| QUALITY 39 completeness | **Gap: no `stderr_sha256`.** This is a receipt-format limit shared by all 8 rows, not a C1 population item. |

## Findings

1. **Digest: 1/1 match (observed).**
   - The row records `stdout_sha256` `bce10627d6cdf4f264088c69d58507f16d3a586a37309a0dc8c681b31a8d682b` (`checks.json:83`).
   - `sha256sum final/assemble-selftest.stdout` returns the same digest. The file is 8340 bytes and 89 lines. It contains 80 `  [ok]` lines and 0 `FAIL`, and ends `SELFTEST: 80/80 pass` (line 89).
   - Lines 19-26 continue check 18's detail, which is the captured summary of the carry-only ledger run. They are not checks.
   - `final/assemble-selftest.stderr` is 0 bytes (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). The row has no stderr digest field, so stderr is retained corroboration only. It is not a second digest match.
   - Only commit `5923d89` (2026-10-20 18:40:48 -0300) added the three files. Their git blobs at `5923d89` and at `21e7932` are identical:
     - stdout `f2b4863c04ff…`
     - stderr `e69de29bb2d1…` (the empty blob)
     - `checks.json` `d8c98a92fd71…`
   - `checks.json` sha256 is `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d` at `5923d89`, at `7243e7f`, at HEAD `21e7932` and in the working tree.
2. **Argv spelling agrees with the CLI source (observed).**
   - The row's argv is `["python3", ".ufo/evidence/round-18/coldread/assemble.py", "--selftest"]` (`checks.json:76-80`).
   - In `assemble.py`:
     - Usage (`:91-92`) lists `[--selftest]`.
     - `--selftest` is `action="store_true"` (`:1965-1969`).
     - `if a.selftest: return _selftest()` (`:1972-1973`) runs before the `--reports`/`--carry` requirement (`:1974-1975`).
     - No positional arguments are defined.
     - `_selftest` returns 0 only when there are no failures (`:1920-1925`). Argparse misuse exits 2 (`:97`).
   - So exit 0 together with `SELFTEST: 80/80 pass` can only come from the selftest branch.
   - The registry row `assemble-round18-selftest` in `tools/registry.json@921ef80` spells the identical argv. It expects exit 0 and `stdout_contains: ["SELFTEST: "]`, with source `SKILL.md@58e5d53:1923-1932`.
   - Contrast with R18-4: `bash-witness-study.py` needs the positional `mode`, so `--selftest` exited 64. The assemble row does not share that defect.
3. **Revision attribution: correct, reconstructed rather than self-bound.**
   - The row names `921ef8077440f90d092aab4b9fdc750a45de1224` (`checks.json:81`), committed 2026-10-20 18:28:40 -0300.
   - `git show <rev>:.ufo/evidence/round-18/coldread/assemble.py | sha256sum` gives `bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a` at `921ef80`, `a85f710`, `4b7c682`, `7243e7f`, `78b99dd` and `21e7932`, and in the working tree.
   - The tool was last modified in `58e5d53` (17:20:09 -0300).
   - The selftest is synthetic. Every `main()` call passes `--repo repo --out out` inside `TemporaryDirectory(prefix="assemble-v2-selftest-")` (`:1130-1133`; e.g. `:1250`, `:1304`). So the result depends on the tool bytes plus the interpreter and git, not on other lane content. Attribution therefore reduces to tool-byte identity, which holds.
   - Independent retained corroboration at the same revision: `final/registry.stdout` is a registry-check run in its own clone with `rev_resolved` `921ef80…`.
     - Its row `assemble-round18-selftest` is held (`registry.stderr:34`), with `elapsed_s` 0.208 and stdout tail ending `SELFTEST: 80/80 pass`.
     - The same row is also held in `registry-success` and `registry-branch-aligned` at `5923d89`, which has the same tool bytes (`:34` in each; elapsed 0.185 and 0.198).
   - Ephemeral corroboration (not retained in the lane): the L1 scratch clone `/tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin` has this reflog (`git log -g`, read with `GIT_OPTIONAL_LOCKS=0`):

     | Time (-0300) | Move |
     |---|---|
     | 18:29:34 | clone + checkout to `921ef80` |
     | 18:41:04 | to `5923d89` |
     | 18:46:59 | to `a9c94c5` |

   - The stream files' mtime is 18:33:15.3776 and `checks.json`'s is 18:33:15.3778, inside the `921ef80` window.
   - The stdout embeds the TMPDIR `/tmp/tameshi-r18-L1-final-a2vitd82/tmp/…` (`stdout:18,60`). That matches `TMPDIR="$W/tmp"` in `/tmp/tameshi-r18-L1-sbx.sh`.
   - [INFERENCE] The cwd was that clone; the row does not record cwd. Even if the cwd was the live lane, that file was byte-identical then (mtime 16:50:55, sha `bf7c12f7…`).
   - Downstream citations are consistent and none restates the tally at `4b7c682`:
     - Fleet report `a85e4d8:.ufo/reports/round-18/tameshi.md:19` cites "assembler selftests **98/98**, **80/80**. Evidence: … `final/`".
     - Spot-check `corpus/lessons/round-18-verifier-spotcheck.md:110-113` lists "assemble 80/80" as evidence-verified.
4. **Failed raw attempt vs current evidence.**
   - This row has integer exit 0, 80/80 and empty stderr, so it is current, effective evidence.
   - Observations found for tool `bf7c12f7…`: 8. Passing: 8. Failing: 0. I found them by scanning every `.ufo/evidence/round-18/**/*.json` for an `argv` containing `coldread/assemble.py` and `--selftest`.
     - (a) This row, at `921ef80`.
     - (b) `final/registry.stdout`, at `921ef80`.
     - (c) `final/registry-success.stdout`, at `5923d89`.
     - (d) `final/registry-branch-aligned.stdout`, at `5923d89`.
     - (e) `coldread/traces/CR48-r3/6.json`, at `4acdeac`. Its argv ends `exit $rc`, so the trace `exit: 0` is the tool's exit.
     - (f) `coldread/traces/CR50-r3/9.json`, at `4acdeac`, and (g) `coldread/traces/CR50/11.json`, at `01d586d`. Both are `bwrap … env -i … python3 .ufo/evidence/round-18/coldread/assemble.py --selftest`, so `exit: 0` is the tool's exit passed through. Both record input `assemble.py` = `bf7c12f7…`. These receipts do not retain stdout.
     - (h) `coldread/traces/CR48/7.json`, at `01d586d`.
   - **Caution on (h):** its `exit: 0` is the exit of `bash -c '…; echo "assemble18 --selftest exit=$?"'`. That masks the tool's exit, so it is not tool-exit evidence by itself. Its 80/80 output survives only in `/tmp/tameshi-r18w2-CR48-5kGfrT/tmp/selftest-assemble18.txt`, which is ephemeral.
   - Excluded from the count:
     - `CR50/25.json` greps CLI flags (a round-17 vs round-18 `add_argument` comparison). It does not run the selftest.
     - `CR45/07.json` runs the round-16 assembler, a different tool.
   - Round 19 has no assemble re-run. `.ufo/evidence/round-19/` has no assemble artifacts, and its `measure.py` reads `OLD_CHECKS` only for the bash-witness `supersedes` link.
   - The failed raw rows in this bundle are other rows:
     - `registry`: exit 1, `sources-census` differs. Commit `a9c94c5` says it is retained as a stale scratch-branch failure.
     - `bash-witness-selftest`: exit 64 (R18-4).
5. **The raw digest cannot be reproduced by a replay (observed).**
   - Each run varies the random TMPDIR name (`assemble-v2-selftest-iz35nra5`) and the synthetic temp-repo commit ids (`078592249bbf…`, `4da5539351c5…`, `4fa09aea4a38…`).
   - After normalizing those values (code below), three outputs are identical: normalized sha256 `5e376027195547e37b4e90829f817869ec26aaf9ae572de01389f36c77331263`, 7307 bytes, 80 ok, 0 FAIL. The three are:
     - this row's stdout;
     - CR48-r3 (`4acdeac`, written 18:16:37);
     - CR48 (`01d586d`, written 17:44:20).
   - So `bce10627…` binds only this retained observation. A future replay with a different raw digest is expected, and is not evidence of failure.
6. **QUALITY 39 gap: binding format, not content.**
   - `corpus/QUALITY.md:352-354` (added in round 19) requires "both digests".
   - The row has argv, revision, integer exit, retained stdout/stderr and the stdout digest. It has no `stderr_sha256`; the `checks.json` schema has that field in none of its 8 rows. It also records no tool sha256, cwd or timestamp.
   - The stderr content is empty and is bound by git blob `e69de29…` in `5923d89`, so nothing is hidden.
   - This row is outside the C1 population (`.ufo/evidence/round-19/contract.json:6-12`; R18-4 is the bash-witness row only). C1's 0/5 → 5/5 count must neither count it as a correction nor add it as a sixth defect.
7. **No harm from the round-19 correction (observed).**
   - `before.json` and `after-21e7932.json` both pin the `checks.json` input to `fed3c8e6…`.
   - `git log` on the three paths shows only `5923d89`.
   - Round 19 neither reclassified nor superseded this row.

## Recommended preserved-history treatment

1. Keep `checks.json` (including lines 75-84) and both `assemble-selftest.*` stream files byte-identical. Do not edit them in place, and do not overwrite them with a re-run.
2. Classify the row as the **effective historical receipt** for "assemble selftest 80/80 at `921ef80`, tool sha256 `bf7c12f7…`". Do **not** give it a `supersedes` relation, since nothing failed. Do not fold it into R18-4 or count it toward C1.
3. Add a binding note only if a later claim re-cites this tally under QUALITY 39. If one is needed, append a separate dated sidecar or erratum that *annotates* `checks.json#assemble-selftest`; it must not supersede the row. It should record these derived fields, each labeled "derived from retained bytes, not recorded at run time":
   - stderr: 0 bytes, sha256 `e3b0c442…`, git blob `e69de29…`;
   - `tool_sha256`: `bf7c12f7…` at `921ef80`;
   - `committed_in`: `5923d89`;
   - `cwd_kind`: scratch clone (inference).
4. Do not restate 80/80 as a run at `4b7c682`, `7243e7f` or `21e7932`. Tool-byte identity there is a fact; a run there is not, and saying so would repeat the R18-5 pattern.
5. Any replay is a new, separately named receipt. Judge it by exit, the `SELFTEST: 80/80 pass` tally and normalized content, never by raw digest equality with `bce10627…`.
6. Cite `CR48/7.json`'s exit as a wrapper exit, never as the tool's exit.

## Falsifiers (what would reopen this audit)

- `sha256sum .ufo/evidence/round-18/final/assemble-selftest.stdout` gives anything other than `bce10627…`.
- `checks.json` sha256 differs from `fed3c8e6…` at any revision from `5923d89` on.
- `git show 921ef80:.ufo/evidence/round-18/coldread/assemble.py | sha256sum` gives anything other than `bf7c12f7…`.
- A retained selftest observation of tool `bf7c12f7…` shows a tool exit other than 0 or a `FAIL` line.

## Unknowns

- The runner that wrote `checks.json` (its argv, start times, interpreter version) is not retained. `repeat/command.txt` in the same scratch shows `python=3.14.8`; it is adjacent evidence, not this row's.
- The cwd is inferred, not recorded.
- The mtimes run sequentially: measure-selftest at 18:33:15.2598, assemble at .3776, `checks.json` at .3778. That puts 0.118 s between the end of measure-selftest and the assemble write. Registry-check recorded `elapsed_s` of 0.185–0.208 for the same selftest. [INFERENCE] Its timing may include process-cleanup polling (`time.sleep(0.01)` loops at `tools/registry-check.py@921ef80:593,609`). Treat the 0.118 s gap as weak, order-of-magnitude consistency only.

## Commands run (all read-only) and outcomes

- `sha256sum` and `wc -c` on `final/assemble-selftest.{stdout,stderr}` → `bce10627…`/8340 and `e3b0c442…`/0.
- `grep -c '^  \[ok\]'` → 80; FAIL count → 0.
- `git ls-tree -l 921ef80 -- …/assemble.py` → blob `186bad5c0404…`, 78662 bytes. `git show <rev>:…/assemble.py | sha256sum` at 6 revisions (HEAD = `21e7932`), plus the working tree → `bf7c12f7…`.
- `git log` on `assemble.py` → `58e5d53`. `git log` on the three final paths → `5923d89` only. `git ls-tree 5923d89|21e7932` → identical blobs. `git show <rev>:checks.json | sha256sum` → `fed3c8e6…`.
- `git merge-base --is-ancestor`: `921ef80` → `4b7c682` → `7243e7f`, both true.
- `GIT_OPTIONAL_LOCKS=0 git -C /tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin log -g` → the reflog above.
- `git show 921ef80:tools/registry.json` → row extracted. Read the `final/registry*.stdout` JSON rows and the `.stderr` line 34 of each.
- In-memory Python scan of `.ufo/evidence/round-18/**/*.json` for any `argv` that contains both `coldread/assemble.py` and `--selftest` → 7 files (the `checks.json` row; CR48/7, CR48-r3/6, CR50/11, CR50-r3/9 and CR50/25, all exit 0; and CR45/07, which is the round-16 tool). Classified in Finding 4.
- `git -C /home/vgpnk/Projects/shokunin show a85e4d8:.ufo/reports/round-18/tameshi.md` → line 19.
- Disclosure: I ran one `git status --porcelain` on the lane without `GIT_OPTIONAL_LOCKS=0`. The lane `.git/index` mtime (2026-10-21 02:50:01.93 -0300) is earlier than that call, so no index write by this seat is observed.

Normalization code, run in memory with no files written:

```python
import re, hashlib
F = ".../final/assemble-selftest.stdout"
A = "/tmp/tameshi-r18w2-CR48-MJmC2B/assemble-selftest.txt"
B = "/tmp/tameshi-r18w2-CR48-5kGfrT/tmp/selftest-assemble18.txt"
p1 = re.compile(rb"/tmp/[^\s'\]]*?assemble-v2-selftest-[A-Za-z0-9_]{8}")
p2 = re.compile(rb"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
p3 = re.compile(rb"@[0-9a-f]{12}:")
keep = {b"1" * 40, b"0" * 40}
def norm(p):
    b = p1.sub(b"<TD>", open(p, "rb").read())
    b = p2.sub(lambda m: m.group(0) if m.group(0) in keep else b"<REV>", b)
    return p3.sub(b"@<REV12>:", b)
# all three -> sha256 5e376027…, 7307 bytes, equal: True
```

## Quotes (opened 2026-10-21)

- "SELFTEST: 80/80 pass" (`final/assemble-selftest.stdout:89`).
- "run built-in synthetic self-test and exit" (`assemble.py:1968`).
- "ROW assemble-round18-selftest expect=0 got=0 held" (`final/registry.stderr:34`).
- "Do not leave a failed invocation as the selftest row of the final receipt bundle." (`round-18-verifier-spotcheck.md:199-200`).
- "A final-success claim names one effective receipt with matching argv, measured revision, integer exit, retained stdout/stderr and both digests." (`corpus/QUALITY.md:352-354`).
