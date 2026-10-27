# T51W2Read08 — cold-read re-key

## Reader

Read `SKILL.md` at candidate `6d8c11e378aa90b12650808e1b79270742935f15`, resolving the exact heading `### The tick and the pin read` (lines 1021–1068; next heading at 1069). The section digest, with trailing blank lines removed as `refresh.py` does, is `60d658245f87d166809e43a14a1bc8b873d2604032b37fa9ab6c3d2965ed5853`. The section is byte-unchanged from base: the base-to-CAND `SKILL.md` diff hunk is only at line 2134 and later.

The fleet and lane pointers were checked against their stated revisions/current files; the runner statements were checked against the CAND runner and its CAND-run receipts. The section's dated round-8 observations mostly hold as historical observations, not as claims about present worktree state.

### Findings and scope

- **Current-engine self-test count is stale, but its historical framing matters.** The section says the engine's doctored-pin refusal was “selftested `MUTATE_SELFTEST: 67/67`”. That count remains a valid round-8 historical record, but is not the count for the runner at CAND: the CAND runner receipt prints `MUTATE_SELFTEST: 107/107 pass`; base-era receipts already print `106/106`. Thus the number was already stale as a current-engine count before this round; the tenth-leg change raises it by one more. The mechanism claim (doctored pin is a separate SETUP refusal arm) still holds: the CAND runner's self-test covers pin mismatch and unresolvable revision as SETUP/exit 2. The sibling Round-9/receipt text at SKILL.md:1003 and :1218 repeats 67/67; those are other reader sections, but this should be visible to integration.
- **Historical scratch paths are absent now.** `/tmp/w8-tameshi-t84/pin-read.txt` and `/tmp/w8-tameshi-t84/drift-demo.txt` do not exist. They are presented as round-8 scratch observations; they cannot be replayed from those paths now. The runner's current TMPDIR/scratch policy does not change the truth of those dated observations. No current TMPDIR claim in this section depends on them.
- **Potential taxonomy gap (strongest falsifier checked).** The stated `current`/`stale`/`drift` readings leave a possible history-rewrite case unclassified if the three labels are meant to be exhaustive. In an isolated scratch Git repo, recorded pin `48bd6282…` on commit `030c14e5…` and unrelated rewritten branch tip `c8670620…` had a different tip blob `83fd965b…`; the recorded commit was not an ancestor (`merge-base --is-ancestor` rc 1), while live bytes equaled the tip blob and path porcelain was clean. Applying the section's rules yielded `current=no, stale=no, drift=no`. This demonstrates an uncovered state, not a contradiction in the six recorded examples; the prose does not explicitly say how to label non-ancestor branch rewrites.
- **No CAND panel-tool interaction found.** The four updated panel tools are not cited in this section. The runner's `MUTATE_TOOL`/`REGRESSION_TOOL` markers remain present at CAND. The historical mado case is correctly timestamped: `mado-shokunin@0c20a76f:tools/mado-verify.sh` hashes to `90d50cdd…` as stated, but its present worktree hash is `050efc72…` (current `main` `02165600…`); the old live-drift hash `dc864c6a…` is no longer the present file. The historical `current`/`stale` table pins for all six examples match the CAND regression receipt; the two stale recorded tip-blob prefixes also match `tsukuroi-shokunin@aa136d69` (`bba6cdf6…`) and `mado-shokunin@0c20a76f` (`90d50cdd…`).
- The historical host/time and transient live mado worktree state are observations in the section, not independently recoverable from CAND. Their status is therefore “not re-observable now”, not disproved.

## Structured row for `reads.json`

```json
{
  "seat": "T51W2Read08",
  "heading": "### The tick and the pin read",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "section_lines": [1021, 1068],
  "section_sha256": "60d658245f87d166809e43a14a1bc8b873d2604032b37fa9ab6c3d2965ed5853",
  "pointers": [
    {
      "raw": "scripts/shokunin-watchdog.sh:3-5",
      "file": "fleet:scripts/shokunin-watchdog.sh@17c1fadfddc5ecbfa5ef362ef44d111792fa3e94",
      "ranges": [[3, 5]],
      "verdict": "holds",
      "located_excerpt": "# A lane's round ends when .ufo/reports/round-<N>/<lane>.md lands; watchdog completes the mission and launches a fresh process for round N+1. Cap 1024/lane. Tick 450s."
    },
    {
      "raw": ":14 (of scripts/shokunin-watchdog.sh at fleet 17c1fad)",
      "file": "fleet:scripts/shokunin-watchdog.sh@17c1fadfddc5ecbfa5ef362ef44d111792fa3e94",
      "ranges": [[14, 14]],
      "verdict": "holds",
      "located_excerpt": "LANES=\"protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama\" (no tameshi)."
    },
    {
      "raw": "5efb4114 (2026-10-19); shokunin.conf names tameshi",
      "file": "fleet:shokunin.conf@5efb4114e8a4f6ff17d0b1594cb0767b144e4f9c",
      "ranges": [[55, 55]],
      "verdict": "holds",
      "located_excerpt": "tameshi|tameshi-shokunin|depth + calibration (verification-fixture craft)"
    },
    {
      "raw": "../scripts/hyaku/jj-lane.sh state <repo> (git config lane.branch first, else function detect_branch())",
      "file": "fleet:scripts/hyaku/jj-lane.sh (current working-tree helper; external to CAND)",
      "ranges": [[101, 105], [116, 128], [156, 182]],
      "verdict": "holds",
      "located_excerpt": "lane_branch_git reads `git config --get lane.branch`; detect_branch checks attached refs/heads then origin/HEAD; cmd_state resolves lane_branch_git then detect_branch and prints `state branch=$branch ...`. This helper is external and is not revision-pinned by the section."
    },
    {
      "raw": "`refs/heads/<branch>^{commit}` via git rev-parse --verify --quiet --end-of-options; git show <tip>:<path> sha256 equality",
      "file": "Git behavior, as written in SKILL.md; corresponding runner refusal paths at tools/mutate-and-run.sh@CAND",
      "ranges": [[1268, 1277], [1314, 1318], [1730, 1738], [1856, 1858]],
      "verdict": "holds",
      "located_excerpt": "CAND runner has SETUP paths for missing revision/path and pin mismatch; its self-test asserts pin mismatch and unresolvable revision exit 2. Direct rev-parse check accepted --end-of-options for a valid branch and returned nonzero for a missing branch (runner maps unverifiable cases to SETUP/2)."
    },
    {
      "raw": "`current` / `stale` / `drift` rules (including recorded revision ancestor test)",
      "file": "SKILL.md@CAND, lines 1033-1036; isolated scratch Git fixture (removed)",
      "ranges": [[1033, 1036]],
      "verdict": "holds",
      "located_excerpt": "Rules match the six recorded cases, but the rewritten-history scratch case had `current=no`, `stale=no`, `drift=no` (recorded pin 48bd6282…, tip blob/live 83fd965b…, ancestor rc 1, clean porcelain). If the three labels are exhaustive, this is an unclassified edge case."
    },
    {
      "raw": "tools/mutate-and-run.sh (tool sha `cf41efaa…`; REGRESSION_TOOL / MUTATE_TOOL markers)",
      "file": "tools/mutate-and-run.sh@CAND",
      "ranges": [[506, 506], [1442, 1442]],
      "verdict": "holds",
      "located_excerpt": "CAND runner still emits `MUTATE_TOOL:` and `REGRESSION_TOOL:`. Its CAND-run regression receipt identifies the runner SHA as 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda, different from the explicitly dated round-8 `cf41efaa…` tool pin."
    },
    {
      "raw": "MUTATE_SELFTEST: 67/67",
      "file": "tools/mutate-and-run.sh self-test; CAND-run receipt `.ufo/waves/round-51/w1/T51ExecEmbed/selftest.stdout`",
      "ranges": [[1064, 1064]],
      "verdict": "absent",
      "located_excerpt": "CAND-run receipt: `MUTATE_SELFTEST: 107/107 pass`; base-era evidence includes `MUTATE_SELFTEST: 106/106`. 67/67 remains plausible only as the dated round-8 count, not a current CAND count."
    },
    {
      "raw": "tools/mado-verify.sh; live file `dc864c6a…` vs HEAD blob `90d50cdd…`",
      "file": "mado-shokunin/tools/mado-verify.sh (external sibling repo; HEAD reference 0c20a76f)",
      "ranges": null,
      "verdict": "holds",
      "located_excerpt": "`git show 0c20a76f:tools/mado-verify.sh | sha256sum` begins `90d50cdd`; the present worktree file begins `050efc72` at main `02165600`. Thus the section's HEAD-at-round-8 pin is confirmed, while the transient live file `dc864c6a…` is no longer recoverable as the current file."
    },
    {
      "raw": "`/tmp/w8-tameshi-t84/pin-read.txt`",
      "file": "/tmp/w8-tameshi-t84/pin-read.txt",
      "ranges": null,
      "verdict": "absent",
      "located_excerpt": "The path does not exist now; section frames it as scratch for the 2026-10-14 executed instance."
    },
    {
      "raw": "`/tmp/w8-tameshi-t84/drift-demo.txt`",
      "file": "/tmp/w8-tameshi-t84/drift-demo.txt",
      "ranges": null,
      "verdict": "absent",
      "located_excerpt": "The path does not exist now; section frames it as a round-8 scratch falsifier."
    },
    {
      "raw": "six-row executed-instance pin table (js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, kagi checklist-run, kumitate claims-check)",
      "file": "sibling source files referenced by CAND regression receipt; table is SKILL.md@CAND lines 1043-1049",
      "ranges": [[1043, 1049]],
      "verdict": "holds",
      "located_excerpt": "CAND regression receipt materializes the same recorded rev/pin pairs: kumitate 175de6ba / 83016d45 and claims-check e9a21b44; kagi fecee874 / 275d8294 and checklist 7e5ec98b; tsukuroi 165307fe / 084951be; mado eead56b2 / d7edaab4. The historical moved-tip blobs also verify: tsukuroi aa136d69 / bba6cdf6 and mado 0c20a76f / 90d50cdd."
    },
    {
      "raw": "round 17 / `@-` working-copy HEAD cross-reference",
      "file": "SKILL.md@CAND, round-17 section lines 1815-1854",
      "ranges": [[1815, 1854]],
      "verdict": "holds",
      "located_excerpt": "The section cites S061 (`jj` leaves Git HEAD detached at `@-`) and instructs readers to use committed branch-tip refs rather than HEAD."
    }
  ],
  "strongest_possible_falsifier_checked": {
    "test": "A clean worktree on a rewritten, non-descendant branch whose tip blob differs from the recorded pin",
    "result": "No stated label applies: not current (tip blob differs), not stale (recorded revision is not ancestor), not drift (live file equals tip blob and path porcelain is clean).",
    "interpretation": "Potential unclassified case if current/stale/drift is intended as exhaustive; no contradiction to the six dated examples."
  }
}
```

No scratch files remain.