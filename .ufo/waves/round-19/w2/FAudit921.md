# FAudit921: round-19 w2 falsification of w1 `Audit921.md`

Seat `TameshiR19-2.FAudit921` (reviewer, read-only, advisory only, no admission authority). Observed 2026-10-21.
- **Frozen build:** `55e1d312c4e8ac67aefad80099bd27581ff805c9`. `master` is now `e7039fd`.
- **Report attacked:** `.ufo/waves/round-19/w1/Audit921.md`. Its blob at 55e1d31 equals the worktree copy; it landed in `eedbc95`.
- **Method:** read-only git (`cat-file`, `diff`, `log`, `ls-tree`, `grep`, `for-each-ref`) with `GIT_*` removed, plus python3 hashing and JSON reads in the session kernel. No suites, selftests, builds, `measure.py` runs or probes.

Labels: **O** = observation, **I** = inference, **U** = unknown.

## Strongest material assertion
`Audit921.md:72`, `:111–134`: "none shows a C1 repair invalidating audit-921". The receipt triple, the ledger entry, its 13 inputs (including defect 4's `checks.json`) and SKILL lines 921–931 all stay bound. The report adds "One indirect pin drifts at the delivered tip" (`_meta.expect_skill_sha`), so a 60/60 at the tip "needs the ledger re-assembled against the new SKILL.md hash".

**Verdict:** **AGREE** that audit-921 stays bound; I re-proved it at 55e1d31, not only at 21e7932. **DISAGREE** with the no-harm corollary: that only one indirect pin drifts and that re-assembly is what a tip 60/60 needs.

## Evidence for the binding (all O)
- **Receipt triple:** `audit-921.{stdout,stderr,json}` are `60c300f1…` (3491 B), `e3b0c442…` (0 B) and `ce080d0c…` (5543 B) at a134a09, 4b7c682, 7243e7f, 21e7932, 55e1d31, e7039fd and in the worktree. `git log` lists only a134a09 for each file.
- **Stdout reproduces:** the trace `argv[29]` program plus its spec (921, 931, 13 paths) rebuilds the stdout byte-for-byte (3491 B) from the a9c94c5 blobs, and again from the 55e1d31 blobs.
- **Inputs:** all 13 entry inputs equal the ledger values at 55e1d31, e7039fd and in the worktree; `checks.json` is still `fed3c8e6…`. SKILL.md is the only drifting file: `4d0190fd…` at 21e7932, `0e3d7453…` (145410 B) at 55e1d31. The `"\n".join` of lines 921–931 still hashes to `21a2ebc8…`, and the text of lines 921, 932 and 933 is unchanged.
- **Ledger and monitors:** round 19's `coldread/ledger.json` at 55e1d31 carries the audit-921 entry identical to round 18 (`skill_sha256` still `1334c512…`). `current-ledger-monitor-55e1d31.json` (landed e7039fd; revision 55e1d31; `overrides_used` false) credits bucket 921–932 with reasons `["credited"]` (60/60, restraint 8). The 21e7932 monitor and `round18-final-measure.stdout` (rev 4b7c682, 60/60, restraint 8) credit it too. That confirms the carry inference at `:132` and closes the report's item-5 gap.
- **Ruler agrees on defect 4:** frozen `measure.py` at 55e1d31 (`bb651eef…`), `witness()` lines 194–199, requires the old `checks.json` row to keep exit 64 and an empty-stdout digest, and to be typed-superseded. So item 4's "binding holds" matches the ruler.
- **Cites verified:** `ledger.json` `:12001–12042` (entry), `:12706` (`_meta`), `:12874` (carry basis), `:12875` (`expect_skill_sha`); the `L1Residual.md:74` quote; committer dates 18:46:21 and 18:47:13 −03:00; `5774d8f` is a `refs/jj/keep` ref with parent 21e7932 that modifies LOG.md, SCORECARD.md and round-19.md. M1–M3 re-derived: the asserts read 9 of the 13 paths; the unasserted four are the ledger `.md`, `mutate-and-run.sh`, `context.stdout` and `checks.json`.

## Concrete falsifier (fires against the corollary)
**O:** `.ufo/evidence/round-19/current-ledger-monitor-21e7932.json` (landed 7af123b, 2026-10-21T02:58; same blob at 55e1d31) shows `sections_covered` 49/60, `calibration_restraint_score` 6, `overrides_used` false.
- Ten buckets lose credit on `input-drift` in files changed between 7243e7f and 21e7932: README.md, QUALITY.md, SOURCES.md and `mutation-case-kumitate-sources-check.md`.
- Bucket 1925–1935 fails with `no-ledger-entry`: the same SKILL append the report analysed at `:127`.
- No reason cites the whole-file hash. Only `assemble.py` reads `expect_skill_sha` (round 18, `:1317`, `:1345`, `:1976–2054`); `measure.py` never does.

**O:** the 60/60 at 55e1d31 came from a v2 ledger with no `_meta` plus 15 appended refresh entries (159 → 174), so re-assembly was not necessary. **I:** it would not be enough either, because it keeps the recorded input digests.

"Not harmed as long as nobody cites" also fails QUALITY 40. The lane already records the correct account, crediting w1 AxisBound: `round-19.md:90` at 55e1d31 reads "The actual monitor at landed21e7932 returned **49/60, restraint6**". No erratum names `Audit921.md:131–134`, so do not cite those lines as no-harm support. **I:** Audit921 observed master at 21e7932 (`:64`), before 7af123b landed this receipt; it made an inference, not a fabrication.

**Core falsifier (did not fire):** the binding claim would fail if any of the 13 inputs at 55e1d31 differed from its entry hash, if SKILL lines 921–931 hashed to something other than `21a2ebc8…`, or if the 55e1d31 monitor showed bucket 921 as `credited:false`.

## Stale or overlooked items (dated by revision)
1. **Stale at 55e1d31:** "pure append … one hunk `@@ -1934,0 +1935 @@`" and "`4d0190fd…`" (`:126–129`). `git diff -U0 7243e7f 55e1d31 -- SKILL.md` now shows `@@ -1890 +1890 @@` (an in-place edit from 88c8073) and `@@ -1934,0 +1935,2 @@` (7af123b appends a second row). Line 1890 is after 931, so audit-921's own invalidation condition is not met.
2. **Unit slip (QUALITY 38 class):** "2610 bytes after the section block" (`:41`) is 2610 characters, which is 2618 bytes because of the non-ASCII `—` and `…`. The substance is unchanged.
3. **M2 gap closed:** `repeat.stdout` (unchanged since a9c94c5) has the line `REPEAT_CONTROL: controls_match`. No false value exists, so the weakness stays hypothetical.
4. **Attribution:** `round-19.md:146–148` disposes of the printed VERIFIED "ancestor" line and credits Audit965, Audit1212 and Audit1925. Audit921 M1 found the same line at `audit-921.stdout:34` and is not named. The lesson's quote "ancestor runs share instrument blobs" paraphrases the printed "ancestor runs have the same instrument blobs as the read revision" (17 round-18 audit stdouts). The generic wording still covers audit-921.
5. **The ruler checks `checks.json` by fields only** (O, from a static read; not executed). Frozen `measure.py` reads only `probes` and the `bash-witness-selftest` exit and stdout digest. It does not pin the whole file (`fed3c8e6` is absent from the source) and only reports input digests (`:401`). An in-place rewrite that keeps those fields would leave all five rows unchanged. Item 4's "binding holds" is enforced by the input-keyed coldread monitor, not by C1's ruler.

## Residual unknowns
- **U: producer, interpreter and clone.** Whether the recorded producer actually wrote audit-921's stdout is unknown. The trace has no stream digest or timestamp, so the only links are the shared file-name stem and content I could reproduce. Interpreter identity and clean-clone state are also unknown, as Audit921 says.
- **U: monitor counts not recomputed.** I read them from retained receipts. No probe was run, because this seat is not authorized to run them.
- **U: worktree in flux.** Mid-review, worktree `measure.py` was briefly `3f19a16b…` (it showed an `OLD_CHECKS_PIN`) and is `bb651eef…` again. `guard-kill-closure.md` and `round-19.md` now differ from 55e1d31 in the worktree. Who made these changes is unknown. All findings are bound to the 55e1d31 and e7039fd blobs.
- **Writes and installs:** no tools installed or updated. The only write is this report.
