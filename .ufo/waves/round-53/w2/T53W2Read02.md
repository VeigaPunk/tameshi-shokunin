# T53W2Read02 — wave-2 re-read: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`

Seat T53W2Read02, round 53 wave 2. Candidate C** = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`
(lane `tameshi-shokunin`). Every read below is of git objects at C**
(`git -C <lane> show C**:<path>`); the working tree was never read. Wave-1 reader of this
heading: `T53W1Read04` (1 finding, "line count" in step 9's cross-reference).

Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read02/` (removed on exit).

## 1. Section boundary and hash (reproduced, not copied)

- Split SKILL.md at C** on lines matching `^#{1,3}(\s|$)` outside ``` fences: the heading is at
  line 134, the next heading (`## Defect-taxonomy templates and exact-string guidance`) at 249.
  Section = lines 134–248, trailing whitespace-only lines stripped → last content line 247,
  8,684 bytes, no trailing newline. 64 sections in total at C**.
- Independent split `sha256` (surrogateescape over the joined section bytes) →
  `2495d8c00061318a622abb1e97c498c3e3a4e3d2aa5537a010d5a0630f554ed1`.
- The same bytes through the frozen round-18 `sectionize`
  (`.ufo/evidence/round-18/measure.py` via `spec.loader.exec_module` → `sectionize(raw)`) return
  `{'start': 134, 'end': 248, 'heading': '## Mutation-sweep recipe — numbered steps; bounded
  cold-read evidence', 'sha256': '2495d8c0…54ed1'}`. Both agree; `section_sha256` in the JSON is
  that value.
- The section moved 131 → 134 since C*: the C** fix pass rewrote the Standing-rules errata bullet
  (SKILL.md:24-27, +3 lines), shifting every later line by 3.

## 2. Wave-1 fix verification (first)

**Named fix: step 9's stale cross-reference to step 2.**

- C* line 224 read `Re-run step 2's checks (line count and repo revision included; …):`.
- C** line 227 reads:
  `9. **Restore + prove endpoint identity.** Re-run step 2's checks (repo revision included; neither model note records an after-revision)`
- Verified in bytes: `grep -n "line count"` over section lines 134–247 returns **no hit** — the
  bogus field is gone from the whole section, not just the parenthetical (`git diff C* C** -- SKILL.md`
  shows exactly that one line changed inside this section).
- The surviving limbs of the wave-1 finding now resolve:
  - *repo revision* — a step-2 field (`SKILL.md:153-155`) and the parenthetical says neither note
    records an after-revision. Checked against the notes at C**: `mutation-case-kimi-census.md:34-35`
    records sha256/size/mtime/clean and **no** after-revision; `mutation-case-kagi-census.md:54-56`
    records sha256/44212 B/mtime/clean/`cmp` and no after-revision. Holds.
  - *size* — step 2's own record list does not name it, but step 9's last line points at "Full
    checklist below (Restore discipline)", and `SKILL.md:383-385` lists "sha256 (full), size, mtime,
    repo revision, and `git status --porcelain -- <path>` empty" among the before-fingerprints; the
    cited pins carry the values (`mutation-case-kimi-census.md:14` "896 lines, 43273 B",
    `mutation-case-kagi-census.md:14` "44212 B, 886 newlines"). Supported, not reported as a finding.

**Verdict on the named fix: applied and complete.**

## 3. Findings

### F1 — stale scratch shape: the section prescribes a path its own cited rule declares dead

Quote (SKILL.md:139, byte-exact):

> Scratch for a sweep: `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>-<n>-work/` (Standing rules; deleted on exit).

Second occurrence, step 3 (SKILL.md:161, byte-exact):

> 3. **Copy pristine to scratch.** `mkdir -p "$HYAKU_SCRATCH/<lane>-r<round>-<n>-work/evidence"`

The cited authority, Standing rules at C** (SKILL.md:28, byte-exact excerpt):

> **Scratch namespace is `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>/<sub>/`** (host scratch directive of 2026-10-25: `/tmp` is for files under 50 MB only; a seat deletes its tree on exit; the shape every landed round since 37 uses — the older `<lane>-r<round>-<n>-*` dash form died at round 36)

Class: stale scratch directive / self-contradiction with the cited rule.

Why it fails at C**: the section's `(Standing rules; deleted on exit)` parenthetical asserts
Standing rules as the source of that path. At C** that rule says the opposite — the dash form
`<lane>-r<round>-<n>-*` "died at round 36", the live shape is `<lane>-r<round>/<sub>/`, which is
also the shape round 53's own seats use (`/fast/scratch/hyaku/tameshi-r53/w2/<seat>/`). The
delete-on-exit half of the parenthetical is accurate; the path shape is not. A sweep run from this
page would create `…/tameshi-r<N>-<n>-work/`, a namespace the rule forbids.

Provenance: the contradiction is introduced by the fix pass, not inherited — absent at `C*`, present at `C**`. At `C*` Standing rules:25 still carried the same
dash form (`<lane>-r<round>-<n>-*/`) and the section was consistent; the C** fix pass rewrote that
rule (SKILL.md:28, live shape `<lane>-r<round>/<sub>/`, "dash form died at round 36") and did not
update the two occurrences in this section.

### F2 — stale self-anchor `SKILL.md:377-378`

Quote (SKILL.md:231, byte-exact):

> so this shows endpoint identity, not the absence of a transient write (SKILL.md:377-378; corrected in round 27, seat Read03)

Class: stale anchor (the quoted content is absent at the cited lines).

Why it fails at C**:

```
$ git show C**:SKILL.md | sed -n '377,381p'
377: (blank)
378: ## Restore discipline — before/after identity, not continuous non-write proof
379: (blank)
380: All substrate edits must stay in scratch. Before/after fingerprints establish endpoint
381: identity, not that no transient write occurred. Apply this policy in order:
```

The phrase the section attributes to 377-378 ("endpoint identity, not the absence of a transient
write" / Restore discipline's "not that no transient write occurred") is at 380-381. Line 377 is
blank and 378 is the section heading, which does not carry the quoted sentence. The anchor was
correct at C* (wave-1 verified 377-378); the C** fix pass inserted three lines into Standing rules
(+3 shift, heading 131 → 134) and did not re-point this citation. The sibling reference in the same
sentence — "Full checklist below (Restore discipline)" — is name-based and still resolves.

## 4. Holds (each pointer re-read at C**, content compared, not just the line number)

| Section statement | Verified at C** |
|---|---|
| "round 16's full-page cold-read executed it end to end (two seats; Errata — round 16)" (SKILL.md:137-138) | errata row at SKILL.md:1744: `134-135 … round 16 executed the recipe end to end (CR04a, CR04b)` — two seats (historical receipt, append-only) |
| line 139 scratch root uses `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`), deleted on exit; no `/tmp` in the section | Standing rules SKILL.md:28; `grep -n /tmp` over section lines 134–247 → no hit (the `/tmp`→`$HYAKU_SCRATCH` wave-1 repair holds) |
| step 1 private `--root` / host-gated branches (kimi:4-7; kagi:24-38) | kimi:4-7 copies under scratch, `--selftest` or `--root` empty dir; kagi:24-38 mktemp fixtures + `command -v "$JANITOR"` skip-cases |
| step 1 kumitate `n/m pass` + `VERDICT:` (gates-survey-kumitate.md:19-31) | :21 `62/62 cases passed (hermetic)` / `VERDICT: PASS`; :22 `42/42 cases passed` / `VERDICT: PASS` |
| step 1 `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (kimi:20-21) | kimi:20-21, node v24.21.0 |
| step 1 bash 16 enumerated / 14 executed +2 skipped (kagi:27-35,42-43) | kagi:33-35 `ok-case 01..14` + `skip-case 15`/`16`, epilogue `SELFTEST: PASS (16 cases)`; :42-43 control run |
| step 2 pin fields; kagi's 887th line without trailing newline (kimi:13-16; kagi:13-17) | kimi:13-16 sha256/896 lines/43273 B/mtime/revision/clean; kagi:13-17 `44212 B, 886 newlines (the 887th line carries no trailing newline …)` |
| step 2 dirty-pin lesson (corpus/README.md G-R2-1; gates-survey-kagi errata) | README:11 G-R2-1 row ("intermediate dirty-tree state never committed") |
| step 3 kagi `cmp`-verified copy (kagi:44-45) | kagi:44-45 "`cp -p` byte copy, `cmp`-verified" |
| step 4 manifest shape (kimi:41-53, :155-166) | the 10-row kill-rate table and the 10-line edit manifest |
| step 4 E1s (kimi:183-191; kagi:184-191) | kimi E1 D7 expectation wrong, kept; kagi E1 10/10 verdicts, 6/10 counts |
| step 4 "catalog + entry template in the next section" (SKILL.md:166) | next section (249–316) carries `**Entry template (one per defect, written before any run):**` (:257) and `**Class catalog (worked rows are the calibration):**` (:294) |
| step 5 `count(old)==1`, first matching line, `all unique` (kimi:22-25; kagi:44-47) | kimi:22-25 "asserts the old string occurs exactly once … `all unique`, first-line match on all 10"; kagi:44-47 same |
| step 5 maintained driver prints the failing count at `tools/mutate-and-run.sh:434` | :434 `sys.stderr.write('APPLY FAIL id=%s line=%d old-string-count=%d expected=1\n' …)` |
| step 5 "the cited notes do not establish that the round-2 driver carried the `new != old` guard" | kimi:22-25 and kagi:44-47 record only the uniqueness assert; no `new != old` guard appears |
| step 6 records (kimi:26-28; kagi:48-49); timeouts 300 s / 280 s | kimi:26-28 stdout/meta/aggregate; kimi:31 "against the 300 s timeout"; kagi:48-49 wall time + summary; kagi:53 "against the 280 s per-run bound" |
| step 7 denominators 43 and 16 (kimi:30-33; kagi:27-35,50-53) | kimi:32-33 "`<n>/43`"; kagi:51-52 "`(<n>/16 cases)` on every run" |
| step 7 failing-case labels (kimi:59-76; kagi:67,82-103) | kimi:59-78 labels per defect; kagi:67 `1/16` / FAIL row; kagi:84 `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0` |
| step 7 token-only kill, B4 (kagi:88-91) | kagi:88-91 "the **exit code still matched** … the token assert is what killed it" |
| step 7 kill-rate rule + driver DEGRADED at `tools/mutate-and-run.sh:579-583` | :579 `pct=$(( (200 * killed + total) / (2 * total) ))`; `total` = spec line count (`:516`, every defect); :580-583 `MUTATE: DEGRADED …` + `exit 1` |
| step 7 "neither model exercised this" (inconclusive) | kimi:29-30 and kagi:50-51 both "No inconclusive run" |
| step 7 rates (kimi:29-31; kagi:50-53) | kimi 8/10 (80 %), 11 runs, 7.0 s; kagi 8/10 (80 %), 11 runs, 11.0 s |
| step 8 survivor probes (kimi:82-99; kagi:111-114, :118-122, :252-254) | kimi:90-92 pristine `+22 more` vs D2 `+23 more`; :98-99 `frozen=25` vs 24; kagi:111-114 B5 `SURFACE OK … (exec 644)` vs `SURFACE DIVERGED`; :118-122 B10 `ok=0` vs `ok=1`; :252-254 the same expectations from the note alone |
| step 9 main clause "(SKILL.md:377-378; corrected in round 27, seat Read03)" — the round-27 correction exists | `.ufo/waves/round-27/w1/Read03.md` present at C**; its verdict quotes "The page's own Restore discipline says the check proves endpoint identity only" (see F2 for the anchor itself) |
| step 9 after-values (kimi:34-35; kagi:54-56) | kimi hash/size 43273 B/mtime/clean; kagi 44212 B/09:47:15/clean/`cmp`-identical |
| step 10 record shape (kimi §1, §3-§6; kagi §1-§7) | headings present: kimi 39/109/148/183/193, kagi 62/128/162/184/193/208 |
| cost profile + U5 (kimi:20-21,29-31,204-205; kagi:50-53,203-204) | kimi:204-205 "measured only on node v24.21.0, this host, 2026-10-14"; kagi:203-204 same for bash/sqlite3/python3/awk, ~1.0 s per run |

## 5. Considered but not reported

- Step 9's remaining `size` requirement against step 2's record list: supported via the
  "Full checklist below (Restore discipline)" pointer to SKILL.md:383-385 and via the cited pins
  (kimi:14, kagi:14); no false statement remains.
- Step 4 "one per class" vs the cited manifests (kimi D4/D5, kagi B4/B5 carry the same class word):
  the next section's catalog splits them into separate rows (`dropped arm` vs `weakened presence
  gate`), so the claim is readable as holding. Same call as wave 1, no new evidence.
- `Require `new != old` in future drivers` while the maintained driver already refuses no-ops
  (`tools/mutate-and-run.sh:412`): a forward requirement, not a claim about the current tool.

## 6. Adjacent observation (not this section's finding, routed to the L1)

The same dead dash-form scratch shape that F1 reports also appears outside this section at
`git show C**:SKILL.md`: lines 345, 546, 602, 614 (`/tmp/<lane>-r<round>-<n>-work`). Those lines
belong to other sections/seats; listed here only so the sweep can be complete. The section under
this seat contains no `/tmp` path.

## 7. Limits

One section, one candidate, one pass. Reads were git-object only; no recipe step was re-executed
(the sweeps of rounds 2/3/16/17 are historical and are not re-run to decorate this report). The
held statements are verified as *statements whose cited bytes say what the section says*, not as
re-measured sweeps. The two findings are byte-level: each has the exact lines at C** printed above.
