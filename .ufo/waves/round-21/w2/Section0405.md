Verdict: done — `no-blocking-gaps`; two non-blocking mechanism inaccuracies and two citation-anchor corrections.

# Section 0405 — Cross-language divergence (round 3)

**read_rev:** `790abd2129f153c13b471e381d454186edbde65e`  
**SKILL range:** 405–465, `## Cross-language divergence — bash vs JS (round 3, measured)`

**Axes:** factual accuracy; source/citation precision; historical-versus-current scope; operator clarity.

## Findings

### Non-blocking wrong expectations (count 2)

1. **Bash test mechanics are stated too universally (SKILL 446–448).** The pinned `surface-census.sh` does rebuild its scratch host before the 14 filesystem/selftest cases, and `run_case` generally asserts an exit plus a token. It is not true for every one of the 16 cases: the `sqlite-unavailable` check requires both `SHAPE UNVERIFIED` and `unverified=3` (`../kagi-shokunin/corpus/surface-census.sh:778–788`); the two verbs cases are substrate-gated and skip with no execution when the handler is absent, or exercise the real handler rather than a freshly built census fixture when present (`:815–844`). This matches the 14 + 2 account at `corpus/knowledge/mutation-case-kagi-census.md:27–35`, but conflicts with the unqualified “per case” / “one token per run” wording in SKILL 446–448. Scope that explanation to the hermetic fixture cases and their assertion helpers.

2. **The JS mechanism description is factually wrong (SKILL 448–450).** The pinned JS selftest is filesystem-backed: `selfTest()` creates a `mkdtempSync` root, `mk()` builds fixture trees with `fixtureTree()`, and `runGate()` calls `spawnSync` (`../kumitate-shokunin/scripts/kimi-census.mjs:430–460,471–512`). It does not use in-memory fixtures. Nor does it assert exact verdict lines generally: the DRIFT helper uses `startsWith('KIMI_CENSUS: DRIFT')` plus kind checks (`kimi-census.mjs:495–501`); the case record explicitly identifies the one exact verdict-line assertion as CLEAN (`corpus/knowledge/mutation-case-kimi-census.md:82–89`; source `:506–514`). The broad kill widths remain correct; the supported explanation is that broadly affected baseline-derived fixture cases fail, not that the JS suite shares in-memory fixtures or uses exact verdict-line assertions throughout. The target's secondary citation to `mutation-case-kagi-census.md:171–175` repeats the inaccurate comparison rather than validating the JS implementation.

### Citation precision (non-blocking)

- SKILL 461–462 cites `PROVINCE.md:16–17` for the two-independent-lane admission bar. The complete rule starts at line 15 and ends at line 16 (“a pattern is admitted from evidence in TWO independent lanes…”); line 17 is the separate “Never edits a sibling's gate code” sentence. Correct range: `PROVINCE.md:15–16`.
- SKILL 464's `mutation-case-kagi-census.md:193–206` supports the verb-path U2 and host-stability U5 unknowns, but does not contain the band-boundary statement. For “band interiors” use the boundary statement at `:58–60` or the cross-language comparison at `:168–170`. This is an anchor omission, not a contradictory result.

No blocking gap: the cited source contains the two-lane rule, and the measured numerical claims remain supported by the case records and pinned artifacts. The citation issues are locally correctable.

## Agreements and historical scope

- `plans/round-3.plan.md:8–9` pre-registers the anti-claim exactly: a wild Bash/JS kill-rate divergence would itself be the finding.
- Kagi's record `corpus/knowledge/mutation-case-kagi-census.md:162–182` and Kimi's `:29–37` support both 8/10 kill rates, held suite denominators, no inconclusive runs, 16/43 versus 3/16 maximum widths, survivor identities, and the grammar distinction. The Bash skip accounting is supported at Kagi `:27–35`; token-only B4 kill at `:88–94`; calibration and unknowns at `:184–206`.
- The summary is historical, not a statement of current gate behavior: the Kagi case is dated 2026-10-14 and pins `fecee8743e52eb8fb5fbb40782934cb619a1a96e` / SHA-256 `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`; Kimi pins `175de6ba2e9e904010411b19cab27e0af9aad3d4` / SHA-256 `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`. Both exact source hashes matched the recorded pins. Kagi/Kumitate are separate gate/domain artifacts; both historical studies were performed by the Tameshi lane, so “independent” should be read as independent source lanes, not an independent executor replication.
- Historical forecast misses are correctly recorded: the Kimi pre-run verdict forecast missed D7 (`mutation-case-kimi-census.md:185–191`); Kagi verdict forecasts were 10/10, while case-count forecasts missed B2, B3, and B6 (`mutation-case-kagi-census.md:184–191`). Those four misses are study calibration outcomes, not false claims in this SKILL section.
- The SKILL range contains no runnable command or mutation recipe. No obsolete command appears in scope; none was executed.

## Commands, exits, and verification limits

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD` and `git rev-parse 790abd2129f153c13b471e381d454186edbde65e^{commit}` → exit 0; both returned the requested revision.
- Materialized the assigned SKILL and cited plan/case/PROVINCE/survey files with `git show 790abd2129f153c13b471e381d454186edbde65e:<path>` into `/tmp/tameshi-r21-Section0405/` → exit 0.
- An initial source lookup at `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kagi-shokunin` → exit 128 (path absent). Using the available sibling repositories instead, `git show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh` and `git show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs` → exit 0. `sha256sum` of the materialized artifacts → exit 0; results match the two hashes above.
- The original `/tmp/tameshi-r3-1-work/evidence/` and `/tmp/tameshi-r2-1-work/evidence/` directories named by the case notes were not present. I relied on the committed case records and source hashes; I did not reproduce their original raw stdout or rerun mutations.
- LSP status/references/definition/diagnostics were unavailable: `read xd://lsp` returned “No such tool” in this mount. Grep was used only for locating text; semantic claims above are grounded in direct reads of the pinned source and case files.
- No tests, builds, mutation recipes, or installs were run.
