# Verdict: done

## Findings

**Source/quote alignment — agree.** I reopened <https://reproducible-builds.org/docs/timezones/>. Under **“Avoid writing the current timezone”**, the paragraph immediately before the `TZ=UTC` example says: “When there is no dedicated option, it is most often possible to set the TZ environment variable:” The recorded S079 quote in `corpus/lessons/round-21.md:28-30` is an exact 17-word match (markdown code styling aside), within the 25-word limit. The lesson gives the URL and the matching section/location.

**A-tier calibration — agree, narrowly scoped.** At target revision `790abd2129f153c13b471e381d454186edbde65e`, `corpus/SOURCES.md:88` classifies S079 as `docs | A` and scopes it to “the project's explicit-TZ guidance, not universal hermeticity.” That is an appropriate primary/authoritative tier for the project’s own published guidance under `/home/vgpnk/Projects/shokunin/CORPUS.md:76-79` (tier A is scoped to a claim). The live page gives a concrete counterexample to unqualified reproducibility: `LC_ALL=C date -d'@2147483647' --rfc-2822` prints a `+0100` result and the page says the output would fail to reproduce in a different timezone; setting `TZ=UTC` yields `+0000`. It does **not** establish that all programs honor `TZ`: the page says setting it is “most often possible” when no dedicated option exists, and the knowledge entry preserves that limitation at `corpus/knowledge/hermetic-env-differential.md:16-18`.

**Mined/use-by linkage — agree.** S079’s row names `corpus/knowledge/hermetic-env-differential.md` as `used-by` (`corpus/SOURCES.md:88`). That file exists in the pinned target blob; its `source:` header explicitly cites S079 and the same URL/section (`corpus/knowledge/hermetic-env-differential.md:1`), and lines 16-18 explain its bounded use. The file’s presence and the SOURCES/lesson blobs at the target revision were confirmed with `git cat-file -e` (exit 0).

**Old-row immutability vs baseline — agree.** I compared every SOURCES table row in `git show 08175c6:corpus/SOURCES.md` (resolved commit `08175c62d661fddf052ed10abc91313dec8eb77d`) with the target blob. The read-only parser checked all 76 old IDs (S001–S037 and S040–S078), validated 11 cells per row, and found no malformed rows or duplicate IDs. For each shared old row, all immutable fields—`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, and `opened`—were identical. No old row was removed. The only old-row differences were `used-by` additions: S028 adds `corpus/knowledge/hermetic-env-differential.md`; S061 adds `corpus/knowledge/guard-kill-closure.md`. Target has 79 rows total, with only S079/S080/S081 new. No other old-row mutable fields changed.

## Commands and evidence

- `git rev-parse 08175c6` → `08175c62d661fddf052ed10abc91313dec8eb77d` (exit 0).
- `git rev-parse 790abd2129f153c13b471e381d454186edbde65e` → the same target revision (exit 0).
- `git cat-file -e <target>:corpus/SOURCES.md` and `git cat-file -e <target>:corpus/knowledge/hermetic-env-differential.md` → both present (combined command exit 0).
- A read-only Python comparison of the two `git show` blobs completed without error and reported 76/76 old rows checked, zero immutable-field differences, exactly the two `used-by` changes above, zero missing old IDs, and three new IDs.
- No production files were edited. Before writing this report, `git status --short` showed 15 untracked round-21 wave/evidence artifacts; the relevant tracked corpus files had no working-tree diffs.

## Remaining limit

The reopened URL is live documentation and the page reader exposed no version/publication identifier. This confirms the quote and scoped guidance on the reopened page, but does not independently establish the page’s exact historical bytes on its recorded opening date.
