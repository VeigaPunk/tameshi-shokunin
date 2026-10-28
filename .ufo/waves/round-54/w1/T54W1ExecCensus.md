# T54W1ExecCensus — sources census + S277-S279 rows

- Seat: `T54W1ExecCensus` (leaf), round 54 / hyaku run 11, L1 `TameshiR54a2`.
- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (all commands below absolute).
- Lane HEAD at observation: `59c38109bf119d0e9d4f878644a82babc937bc1e` = C0 (verified: `05-head.txt`).
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1ExecCensus/` (removed at end of run; no tree left behind).
- Tooling: no install or upgrade was needed; nothing added to any PATH directory.
- Receipts: `.ufo/waves/round-54/w1/T54W1ExecCensus-receipts/` (12 files, listed at the end).
- Write scope respected: only this file and the receipts directory. No lane production file, counter, contract, freeze, ledger or wave spec was touched.

## 1. Census run — exit code and warning lines (verbatim)

```
cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tameshi; echo "EXIT=$?"
```

Exit code: **0**. stderr: empty (`01-validate.stderr`, 0 bytes). Full stdout is `01-validate.stdout` (1,611 B); the 16 warning lines, pasted verbatim:

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
tameshi	W04	S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
tameshi	W04	S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes
tameshi	W04	S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes
tameshi	W04	S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes
tameshi	W04	S274 duplicate url bazel.build/basics/hermeticity across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Warning tally: 15 × W04 + 1 × W01 = 16; zero E codes; the final `ok` line is present. **No warning names S277, S278 or S279** (`grep -c "S27[789]"` on the stdout = 0).

## 2. Row count (0–3 leading spaces) and shape

Parsed independently of the census (`07-row-assertions.json`):

| measure | value |
|---|---|
| lines matching `^ {0,3}\|` | 141 |
| of which header (`\| id \| source \| … \|`) | 1 (line 10) |
| of which separator (`\|---\|…`) | 1 (line 11) |
| **S-rows** | **139** (lines 12–154, first `S001`, last `S279`) |
| lines matching `^ {4,}\|` (census-invisible indented rows) | **0** |
| rows outside `## Registry` (line 8) … `## Paths` (line 157) | 0 |
| duplicate ids | 0 |
| ids > S279 | 0 (S280 appears only in the `Next unused id:` prose) |

Cross-check with `sources-census.sh census` (`02-census.stdout`, EXIT=0): `rows 139`; tier `A 124 / B 12 / C 3` (Σ 139); status `mined 112 / queued 21 / rejected 6` (Σ 139); `missing 0`.

The registry count also reconciles with the changelog chain: round 51 records `Registry rows 131 → 133`; +1 (round 52, S274) +2 (round 53, S275-S276) +3 (round 54, S277-S279) = **139**.

## 3. S277, S278, S279 — the three assertions

| id | line | `\|`-parts | cells | kind | tier | status | opened | recheck | used-by | used-by exists |
|---|---|---|---|---|---|---|---|---|---|---|
| S277 | 152 | 13 (NF=13 in awk) | **11** | spec | A | **mined** | **2026-10-28** | 730d | `corpus/knowledge/scratch-root-contract.md` | yes |
| S278 | 153 | 13 (NF=13 in awk) | **11** | code | A | **mined** | **2026-10-28** | on-release | `corpus/knowledge/scratch-root-contract.md` | yes |
| S279 | 154 | 13 (NF=13 in awk) | **11** | docs | A | **mined** | **2026-10-28** | on-release | `corpus/knowledge/scratch-root-contract.md` | yes |

- **Exactly 11 cells each**: confirmed twice — Python cell split (`cells: 11`, `07-row-assertions.json`) and the contract's own awk rule `NF==13` / `NF-2 == 11` (`malformed rows count=0` over all 139 rows).
- **status/admit/date**: `status=mined`, `opened=2026-10-28` on all three; no E07/E08 raised by the census, and the date is today (not future).
- **used-by**: all three name `corpus/knowledge/scratch-root-contract.md`; the file exists (3,463 B) and **actually cites every row**: S278 at `:14` and `:19`, S279 at `:22`, S277 at `:28`. The census only checks path existence, so this citation check is mine, and it passes.
- No cell contains a `|` (a stray pipe would have produced NF≠13).

## 4. What the census cannot check — verified against the committed snapshots (PASS)

The census parses `anchor` but never compares it to anything (`sources-census.sh:627`: `anchor=trim($7)`, unused afterwards). So I opened the row anchors myself:

1. **sha256 prefixes are true.** The three anchor cells cite `sha256 89294048…`, `fb44155f…`, `6b0edccf…`. The committed snapshots under `.ufo/evidence/round-54/assimilation/` hash to:
   - `89294048dbc032eacc75804005e256eaa7eb6b5c9a2a9cf75b44d8c573d25ad7` (S277-posix-env.html) — prefix matches;
   - `fb44155f430fac1923d3d7b6af1a0210edcfb580291d664e66f338491d68b62b` (S278-tempfile.py) — matches;
   - `6b0edccf2e7f94fd574632a7ef445c7e0852ac0a362a7bfaed3aaf6b6b8ef7ba` (S279-tempfile-docs.html) — matches.
2. **S278 anchor `:163-165` is byte-exact** in the snapshot (`10-s278-anchor-lines.txt`): line 163 `    for envname in 'TMPDIR', 'TEMP', 'TMP':`, 164 `        dirname = _os.getenv(envname)`, 165 `        if dirname: dirlist.append(dirname)`. The `teaches` conclusion ("an empty value is skipped, so empty behaves as unset") follows from line 165.
3. **S277 quote present** in the text-extracted snapshot: `shall represent a pathname of a directory made available for programs that need a place to create temporary files` (context: `TMPDIR This variable shall represent …`). The naive text extraction yields 33,758 chars, exactly the "33758 B text-extracted" the round-54 lesson records — so the lesson's own extractor is reproduced here.
4. **S279 quote present, and the order is right**: `The list is: The directory named by the TMPDIR environment variable. The directory named by the TEMP environment variable. The directory named by the TMP environment variable. A platform-specific location: …` — the row's "then TEMP, TMP and platform locations" holds.
5. **Contract rule 1 (≤25-word Ground quote) holds** for all three lesson quotes: 22, 3 and 8 whitespace tokens respectively (`08-lesson-quote-wordcounts.txt`).

## 5. The row that would fail the census for a reason the census did not print — **S275**

This is the one real finding of the item. At lane HEAD = C0, the **working tree** carries an in-place edit to an existing row's **immutable `anchor` cell**:

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
D=/fast/scratch/hyaku/tameshi-r54/T54W1ExecCensus
git -C . show 59c38109bf11:corpus/SOURCES.md > "$D/c0.md"
diff -u "$D/c0.md" corpus/SOURCES.md
```

Output (full diff, one changed line — `04-C0-vs-worktree.diff`):

```diff
@@ -147,7 +147,7 @@
-| S275 | … | §3.2–3.3 (commit-relevant and subsuming mutants), p. 4 @ author camera-ready …
+| S275 | … | §3.2–3.3 (commit-relevant and subsuming mutants), p. 3 (physical; printed footer 1787) @ author camera-ready …
```

Char-level confirmation: `replace: C0='4' -> WORK='3 (physical; printed footer 1787)'` (741 → 773 chars on that line; exactly 1 changed line in the whole file).

Why this is a census failure the census cannot print:

- **Contract:** `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49-51` — *"**Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson. A correction is a new row whose `teaches` opens `supersedes S0NN —`."* `anchor` is not in the mutable set.
- **Census:** `sources-census.sh` has no append-only/immutability check at all. `anchor` is read at `:627` and never compared to a baseline; `supersedes` appears only as the E04 duplicate-URL exception (`:648`). The run above **validated the edited file** and exited 0 — the edit is invisible by construction.
- **No log:** `grep -n "S275\|S276\|old → new\|old→new" corpus/lessons/round-54.md` returns nothing. `round-54.md` mentions only S277/S278/S279 (7 mentions total), so the required old→new log does not exist.
- **State:** uncommitted (`git status --porcelain` → `M corpus/SOURCES.md`; `git hash-object` `2c3c86f3…` ≠ C0 blob `66b5dfc5…`). A paired edit in `corpus/knowledge/change-aware-resweep-cadence.md` changes its `source: S275 …` line from `p. 4` to `p. 3 (physical)`; that file is a knowledge entry, not a SOURCES row, so the row-level rule-2 breach is the SOURCES.md change.
- **Unassigned:** `grep -rn "S275\|S276" .ufo/evidence/round-54/contract.json .ufo/waves/round-54/*.json .ufo/waves/round-54/*.md` returns nothing — the frozen contract and the wave spec do not name this correction, so it is not a contracted C1/C2 move.

Verdict: **reported, not fixed** (lane files are read-only for this seat). The parent has two contract-clean routes: revert the in-place edit, or land the correction as a new row (`S280`, since the registry's `Next unused id` is S280) whose `teaches` opens `supersedes S275 —` with the corrected anchor, plus the old→new line in `corpus/lessons/round-54.md`. Note the supersedes form also passes the census's E04 guard by construction (`teaches` matching `supersedes S###` suppresses the same-URL/same-scope error).

Caveat, stated for fairness: the edit is uncommitted and other seats are live in this wave, so it may be mid-flight work. If a sibling owns it, the requirement above still applies before it is committed.

## 6. Sweep that found nothing (so the negative is auditable)

Run over all 139 rows in the working tree (which is what the census reads):

| check | result |
|---|---|
| rows with ≥4 leading spaces (invisible to the census's `^ {0,3}` rule) | 0 |
| S-rows outside `## Registry` (would be E12) | 0 |
| `NF != 13` / cells ≠ 11 | 0 |
| duplicate ids | 0 |
| enum violations (`kind`, `tier`, `status`) | 0 |
| `tier A` + `community` | 0 |
| `mined` rows with `used-by = —` (W03) | 0 |
| `mined` rows whose `used-by` path is missing on disk (E11) | 0 |
| ids above S279 | 0 |
| filename of every `used-by` path | all resolve |
| rows with no URL/DOI outside `own-work`/`tool`/`code` | 0 |
| anchors with no section/page/line locator (`§`, `@`, `p. N`, `:N`) | 15 hits, all false positives of my regex — each names a real locator (`Abstract`, `Post body`, `README opening paragraph`, `README row D29`, `opening definition paragraph`, …), which the contract's "*exact section / heading / page / line*" allows |
| contract's own census snippet (rows / malformed / dup ids / enums / used-by existence) | identical to the script: 139 rows, 0 malformed, 0 dup, 0 enum, 0 missing |

## 7. Observations that are not census failures (recorded, no fix implied)

1. **C0 dropped the final newline of `corpus/SOURCES.md`.** Base `d33053f7552d` ends with `\n`; C0 and the working tree end with `.` (`11-final-newline.txt`). `wc -l` = 513 for 514 logical lines. The census parses identically either way; this is a file-shape deviation only (POSIX text-file convention, and avoidable diff churn on the next append).
2. **Round-54 lesson word counts are wrong but harmless.** The Gate states 21, 5 and 11 words for the S277/S278/S279 quotes; actual tokens are 22, 3 and 8. The contract's binding limit is ≤25 words, which all three satisfy — so no rule is broken, but the stated counts are stale.
3. **S279's stated text-extracted size does not reproduce.** The lesson says "20462 B text-extracted"; the naive tag-strip that reproduces S277's 33,758 exactly yields 19,351 chars for S279. Either a different extractor was used or the number is stale. This is lesson metadata, not a row claim; the quote itself is present in the snapshot.
4. **S278's `teaches` cell flattens three source lines into one code span** (`for …: dirname = …; if …`). The anchor `:163-165` is correct and the claim is true; only the presentation implies single-line source. Cosmetic.

## Receipts index (`.ufo/waves/round-54/w1/T54W1ExecCensus-receipts/`)

| file | content |
|---|---|
| `01-validate.stdout` | full `validate` stdout + `EXIT=0` |
| `01-validate.stderr` | empty (0 B) |
| `02-census.stdout` | `census` mode histogram (rows/tier/status), EXIT=0 |
| `03-SOURCES-at-C0.md` | SOURCES.md at C0, for the diff |
| `04-C0-vs-worktree.diff` | full unified diff, one changed line (S275 anchor) |
| `05-head.txt` | `git rev-parse HEAD` = C0 |
| `06-S277-S279-rows.txt` | the three rows, verbatim |
| `07-row-assertions.json` | row count, cell counts, per-cell dump, `used_by_exists` |
| `08-lesson-quote-wordcounts.txt` | Gate quote token counts vs lesson claims |
| `09-snapshot-sha.txt` | full sha256 of the three committed snapshots |
| `10-s278-anchor-lines.txt` | S278 lines 163–165 byte-exact |
| `11-final-newline.txt` | final-byte comparison base / C0 / working tree |

## Answers to the item, in one place

- Census command exit code: **0**; 16 warning lines (15 W04, 1 W01) pasted above; zero E codes; final `ok` line present.
- Rows with 0–3 leading spaces: **139 S-rows** (141 pipe lines including header and separator); zero indented rows the census would skip.
- S277/S278/S279: **exactly 11 cells each**; `status=mined`, `opened=2026-10-28`, `used-by=corpus/knowledge/scratch-root-contract.md` (exists and cites all three) on all three.
- Rows that would fail the census for an unprinted reason: **S275** — uncommitted in-place `anchor` edit (`p. 4` → `p. 3 (physical; printed footer 1787)`) breaking SOURCES-CONTRACT-v1 rule 2, logged in no round lesson, and invisible to `sources-census.sh` (exit 0). No S277-S279 defect found.
