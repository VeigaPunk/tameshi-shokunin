# T53W1Read04 — cold read: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`

Seat T53W1Read04, round 53 wave 1 (C1 cold-read re-read). Content commit C* =
`a41195dfc13a73958e4c5228ec196b28d03ded03` (lane `tameshi-shokunin`). Every read below is of
git objects at C* (`git -C <lane> show C*:<path>`); the working tree was never read.
Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read04/` (removed on exit).

## Section boundary and hash (reproduced, not copied)

- Split SKILL.md at C* on lines matching `^#{1,3}(\s|$)` outside ``` fences: the heading is at
  line 131, the next heading (`## Defect-taxonomy templates and exact-string guidance`) at 246.
  Section = lines 131–245, trailing whitespace-only lines stripped → last content line 244,
  8,700 bytes, no trailing newline.
- `sed -n '131,244p' SKILL.md | head -c -1 | sha256sum` →
  `71ee856c8bc844468850aee317ad0dd09c6ad425653a415f6ede907dd12f712a`.
- The same bytes through the frozen round-18 `sectionize` extracted at C*
  (`.ufo/evidence/round-18/measure.py`, `spec.loader.exec_module` → `sectionize(raw)`) return
  `{'start': 131, 'end': 245, 'heading': '## Mutation-sweep recipe — numbered steps; bounded
  cold-read evidence', 'sha256': '71ee856c8bc844468850aee317ad0dd09c6ad425653a415f6ede907dd12f712a'}`.
  Both agree; `section_sha256` in the JSON is that value.

## What moved since the last credit for this heading

The round-51 ledger entry for this heading (`read_rev 02ec217c4d0afabe727fde2e261b7951d28fb4e9`,
`sha256 16878309483ed915…`) no longer matches C*. Section-line diff prev → C* shows five edits:

1. line 136 and step 3: `/tmp/<lane>-r<round>-<n>-work/` → `$HYAKU_SCRATCH` (default
   `/fast/scratch/hyaku`)/… — now agrees with Standing rules:25 and the host scratch directive;
2. two step-1 citations gained a `corpus/knowledge/` prefix (others in the section stay bare);
3. step 2's record list lost `size, line count` (was `Record: path, full sha256, size, line
   count, mtime, repo revision, …`);
4. the two `tools/mutate-and-run.sh` anchors were re-pointed 425 → 434 and 569-574 → 579-583;
5. step 9's title became `Restore + prove endpoint identity` (was `Restore + prove the substrate
   never moved`).

## Finding (1)

Quote (byte-exact, section line 224):

> Re-run step 2's checks (line count and repo revision included; neither model note records an after-revision):

Class: self-contradiction (stale cross-reference to step 2).

Why it fails at C*: step 9 tells the reader to **re-run step 2's checks** and asserts that the
line count is among them. Step 2 at C* reads:

```
2. **Pin the artifact — committed bytes only.** Record: path, full sha256,
   mtime, repo revision, and `git status --porcelain --
   <path>` empty (corpus/knowledge/mutation-case-kimi-census.md:13-16;
   corpus/knowledge/mutation-case-kagi-census.md:13-17 — note that gate's 887th line carries no
   trailing newline).
```

There is no line-count field (and no size field) in that list, so there is no line-count
before-value for step 9 to re-run; step 9's own next line (225) still requires `size` unchanged,
which has no step-2 baseline either. The two receipts step 2 cites do pin both fields —
`mutation-case-kimi-census.md:14` = "896 lines, 43273 B", `mutation-case-kagi-census.md:14` =
"44212 B, 886 newlines" — so the C* record list also under-installs what its citations show.
Edit 3 above (the deleted `size, line count`) is the root cause; it was not followed into step 9.

Evidence commands (run against C* objects):

```
git -C <lane> show C*:SKILL.md        # lines 150-152 (step 2), 224-225 (step 9)
git -C <lane> show C*:corpus/knowledge/mutation-case-kimi-census.md   # :13-16 pin fields
git -C <lane> show C*:corpus/knowledge/mutation-case-kagi-census.md   # :13-17 pin fields
git -C <lane> show 02ec217c:SKILL.md  # prev section, for the diff
```

## Holds (each pointer re-read at C*, content compared, not just the line number)

| Section statement | Verified at C* |
|---|---|
| line 135 "round 16's full-page cold-read executed it end to end (two seats; Errata — round 16)" | SKILL.md:1733 errata row `134-135 … round 16 executed the recipe end to end (CR04a, CR04b)` — two seats |
| line 136 + step 3 scratch path | Standing rules SKILL.md:25 names `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`), `/tmp` for <50 MB only, tree deleted on exit; no `/tmp` sweep path remains in the section |
| step 1 private `--root` / host-gated branches (kimi:4-7, kagi:24-38) | kimi:4-7 "every mutant is a copy under …; every run is `--selftest` … or `--root` pointed at an empty dir"; kagi:24-38 mktemp fixtures + the two `command -v "$JANITOR"` skip-cases |
| step 1 kumitate `n/m pass` + `VERDICT:` (gates-survey-kumitate.md:19-31) | :21 `62/62 cases passed (hermetic)` / `VERDICT: PASS`; :22 `42/42 cases passed` / `VERDICT: PASS` |
| step 1 `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS` exit 0 (kimi:20-21) | kimi:20-21, node v24.21.0 |
| step 1 bash 16 enumerated / 14 executed +2 skipped (kagi:27-35,42-43) | kagi:33-35 `ok-case 01..14` + `skip-case 15`/`16`, epilogue `SELFTEST: PASS (16 cases)`; :42-43 control run |
| step 2 pin fields incl. kagi's 887th line without trailing newline (kimi:13-16, kagi:13-17) | kimi:13-16 sha256/896 lines/43273 B/mtime/revision/clean; kagi:13-17 `44212 B, 886 newlines (the 887th line carries no trailing newline — `tail -c1` prints `c`)` |
| step 2 dirty-pin lesson (corpus/README.md G-R2-1; gates-survey-kagi errata block) | README:11 G-R2-1 row; gates-survey-kagi:503 `## 10. Errata`, :554 `G-R2-1 … intermediate dirty-tree state that was never committed` |
| step 3 bash `cmp`-verified copy (kagi:44-45) | kagi:44-45 "`cp -p` byte copy, `cmp`-verified" |
| step 4 manifest shape (kimi:41-53, :155-166) and E1s (kimi:183-191, kagi:184-191) | kimi:41-53 the 10-row kill-rate table, :155-166 the driver spec block, :183-191 E1 (D7 expectation wrong, kept); kagi:184-191 E1 (10/10 verdicts, 6/10 counts) |
| step 5 assert `count(old)==1`, `all unique`, first matching line (kimi:22-25; kagi:44-47) | kimi:22-25 "`mutate_driver.py --check` → `all unique`, first-line match on all 10"; kagi:44-46 same |
| step 5 maintained driver prints the failing count at `tools/mutate-and-run.sh:434` | :434 `sys.stderr.write('APPLY FAIL id=%s line=%d old-string-count=%d expected=1\n' …)` |
| step 5 "the cited notes do not establish that the round-2 driver carried the `new != old` guard" | kimi:22-25 records the uniqueness assert only; no `new != old` guard appears in either note |
| step 6 records (kimi:26-28, kagi:48-49); timeouts 300 s / 280 s | kimi:26-28 stdout/meta/aggregate; kagi:48-49 wall time + summary; kimi:31 "against the 300 s timeout"; kagi:53 "against the 280 s per-run bound" |
| step 7 denominators 43 and 16 (kimi:30-33; kagi:27-35,50-53) | kimi:32-33 "every mutant run still enumerated the full suite (`<n>/43`)"; kagi:50-53 "`(<n>/16 cases)` on every run" |
| step 7 failing-case labels (kimi:59-76; kagi:67,82-103) | kimi:59-78 labels per defect; kagi:67 `1/16` / FAIL row; kagi:84 `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0` |
| step 7 token-only kill, B4 (kagi:88-91) | kagi:88-91 "the **exit code still matched** … the token assert is what killed it" |
| step 7 kill rate band, driver DEGRADED at `tools/mutate-and-run.sh:579-583` | :579 `pct=$(( (200 * killed + total) / (2 * total) ))` divides by `total` (every defect); :580-583 `if [[ "$inconcl" -gt 0 ]]` → `MUTATE: DEGRADED …` + `exit 1` |
| step 7 round 2 / round 3 rates (kimi:29-31; kagi:50-53) | kimi:29-31 8/10 (80 %), no inconclusive, 11 runs, 7.0 s; kagi:50-53 8/10 (80 %), 11 runs, 11.0 s |
| step 8 survivor probes (kimi:82-99; kagi:111-114, :118-122, :252-254) | kimi:90-99 empty-root probes `+22 more`/`+23 more`, `frozen=25`/`frozen=24`; kagi:111-114 B5 `SURFACE OK … (exec 644)` vs `SURFACE DIVERGED … no execute bit`; kagi:118-122 B10 `ok=0` vs `ok=1`; kagi:252-254 the same expectations stated from the note alone |
| step 9 main clause "endpoint identity, not the absence of a transient write (SKILL.md:377-378; corrected in round 27, seat Read03)" | SKILL.md:377-378 "Before/after fingerprints establish endpoint identity, not that no transient write occurred"; `.ufo/waves/round-27/w1/Read03.md` exists and its verdict is exactly that correction |
| step 9 after-revision unknown (kimi:34-35, kagi:54-56) | neither note records an after-revision; kimi:34-35 hash-after/size/mtime/clean, kagi:54-56 hash-after/44212 B/09:47:15/clean/`cmp`-identical |
| step 10 record shape (kimi §1, §3-§6; kagi §1-§7) | headings confirmed present at kimi:39/109/148/183/193 and kagi:62/128/162/184/193/208 |
| cost profile + U5 (kimi:20-21,29-31,204-205; kagi:50-53,203-204) | kimi:204-205 node v24.21.0, this host, 2026-10-14; kagi:203-204 bash/sqlite3/python3/awk, this host, ~1.0 s per run |

## Considered but not reported as findings

- Step 4 "one per class" vs the cited manifests (kimi D4/D5 both `dropped arm`, kagi B4/B5 both
  `dropped branch`): the kimi class strings carry distinguishing qualifiers (`presence gate`,
  `findings cap`) and the next section's catalog splits them into separate rows, so the claim is
  readable as holding; not reported.
- Step 1's two newly prefixed citations sit beside bare ones (e.g. step 7 still cites
  `mutation-case-kimi-census.md:29-31`). Source notes itself uses both forms (SKILL.md:54), so no
  stated rule is broken; not reported.

## Limits

One section, one content commit, one pass. Reads were git-object only; no recipe step was
re-executed in this seat (the recipe's own runs belong to rounds 2/3/16/17 and are not
re-run merely to decorate this report). The held statements are verified as *statements whose
cited bytes say what the section says*, not as re-measured sweeps.
