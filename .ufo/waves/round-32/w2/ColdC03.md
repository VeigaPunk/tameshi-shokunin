# ColdC03 — independent cold read, SKILL.md section 2 (line 375), rev a4f718138bdad20de741faeca57891645e5a64d9

Verdict: **verified-record** (section 2, lines 375–404, "## Restore discipline — before/after identity, not continuous non-write proof"). Every factual claim in the section checks out against the cited sources; two minor, non-blocking gaps listed below.

## Claim-by-claim evidence

Section extent: lines 375–404 (next heading at 405), read from the fleet-mirror clone detached at a4f7181 (HEAD verified = a4f718138bdad20de741faeca57891645e5a64d9; SKILL.md sha256 = 2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a, matching the assignment).

1. "Before the sweep" header records (rule 1, cites kimi :13-16 and kagi :13-17) — verified. `corpus/knowledge/mutation-case-kimi-census.md:13-16` records full sha256 `83016d45…4f426`, 896 lines / 43273 B, mtime 2026-10-13 18:53:12, kumitate repo `175de6ba…`, and `git status --porcelain -- scripts/kimi-census.mjs` empty. `corpus/knowledge/mutation-case-kagi-census.md:13-17` records full sha256 `275d8294…53009f`, 44212 B, mtime 2026-10-14 09:47:15 -0300, mode 755, kagi `HEAD fecee874…`, porcelain empty. All five claimed fields present in both.
2. Copy-only editing (rule 2, cites kimi :4-7 and kagi :44-45) — verified in substance. Kagi :44-45 is exact ("a fresh copy of `pristine.sh` (a `cp -p` byte copy, `cmp`-verified)"). Kimi :4-7 records "every mutant is a copy under `/tmp/tameshi-r2-1-work/`, and no fleet file was written"; the literal `cp -p` for kimi sits in that note's §4 command list (`cp -p kumitate-shokunin/scripts/kimi-census.mjs /tmp/tameshi-r2-1-work/pristine.mjs`), not on :4-7 — pointer slightly loose, substance holds (minor gap 1).
3. After-sweep fingerprints (rule 3, cites kimi :34-35 and kagi :54-56) — verified. Kimi :34-35: sha256 before = after `83016d45…4f426`, size 43273 B, mtime unchanged, working tree clean; the note records a repo revision only pre-sweep (:15) — "no after-repo revision was recorded" is accurate (grep over the note finds no post-sweep revision). Kagi :54-56: sha256 before = after `275d8294…53009f`, 44212 B, mtime 09:47:15 unchanged, porcelain empty, `/tmp/…/pristine.sh` still `cmp`-identical; likewise no after-revision anywhere (kagi `HEAD` appears only at :16, pre-sweep). All quoted strings (`hash83016d45…4f426,43273B`, `hash275d8294…53009f,44212B`, `09:47:15`) match the notes byte-for-byte.
4. Rule 6's record claims — verified. `SCORECARD.md:13` (read via `git show a4f7181:SCORECARD.md` because SCORECARD.md is one of the four L1-appended files; recorded in external_inputs) is the round-2 depth row: "first measured kill-rate: `kimi-census.mjs`'s 43-case hermetic suite vs 10 single-edit mutants (fresh /tmp copies, one exact edit each, driver asserts old-string unique; original byte-identical, sha256 before=after `83016d45…`)" — supports "the historical probes reran from scratch". Both case notes' reproduce sections do rely on an unversioned `/tmp/.../mutate_driver.py`, which is not tracked in the lane (`git ls-files | grep mutate_driver` → empty), and the kagi note's own R21 erratum states exactly the section's remedy: "The old §7 commands depend on an unversioned scratch `mutate_driver.py` … Use `bash tools/mutate-and-run.sh --regression` for the maintained pinned case replay."
5. Rule 7's attribution (G-R2-1 lesson, corpus/README.md round-2 addendum) — verified. The corpus/README.md coverage-map row "`knowledge/gates-survey-kagi.md` — round-2 addendum (G-R2-1…6)" records: "§1 claim-ledger pin corrected: 79301 B / sha256 first16 `93c5827202b9cdec` — the surveyed 79294/`357fb245` was an intermediate dirty-tree state never committed; substrate moved 09:58:55, kagi's own round-18 `fecee87` re-pinned `stamps.tsv` (G-R2-1)" — i.e. precisely the already-dirty-at-pin-time lesson the section draws.
6. Rule 6's named command, `bash tools/mutate-and-run.sh --regression` — partially executed. A bounded 360 s attempt (assignment's 6-minute skip budget) ran the replay from the pinned clone with `--workdir /fast/scratch/hyaku/tameshi-r32-seats/ColdC03/rg-1`: it printed the tool identity `sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (the pinned runner bytes) and completed the first two legs `js-kimi-census` and `bash-surface-census` as `PASS … match=10/10 … flips=0` at the recorded 8/10 rates before the cap cut it off mid-`bash-tsukuroi-census`. The run exceeded the budget, so it was not retried; it left no receipt and is therefore not listed in `commands_executed`/`traces` (minor gap 2). No processes of mine survived the cap (verified via /proc cwd scan of my scratch paths); the kept `rg-1` workdir stays inside my scratch dir.

Classification: record (the section states the restore-discipline policy and what the historical case notes recorded, with evidence pointers; its only named command is conditional guidance for a restore scenario).

No tool installs or upgrades were performed. Nothing outside my scratch dir, the trace directory, and this report was written; no git/jj write commands anywhere; the live lane was never opened during traces.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdC03", "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a", "read_rev": "a4f718138bdad20de741faeca57891645e5a64d9",
  "sections": [{"start": 375, "heading": "## Restore discipline — before/after identity, not continuous non-write proof", "class": "record", "verdict": "verified-record",
    "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [
      "mutation-case-kimi-census.md:4-7 records the copy-only discipline (every mutant a copy under /tmp, no fleet file written) but the literal `cp -p` sits in that note's section 4 command list, not on :4-7; the kagi :44-45 pointer is exact",
      "the section's named `bash tools/mutate-and-run.sh --regression` replay was not executed to completion: a bounded 360 s attempt (assignment 6-minute skip budget) confirmed tool sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 and observed js-kimi-census and bash-surface-census legs PASS (match=10/10, flips=0) before the cap; the capped run left no trace receipt and is disclosed here instead"
    ],
    "commands_executed": [
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kagi-census.md",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/README.md"
    ],
    "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/README.md"],
    "inputs": {"corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
               "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
               "corpus/README.md": "c244f8ca2f877411e2d90195503f446a186bd10600664d75edfd0d6d59f14437"},
    "external_inputs": {"tameshi-shokunin@a4f718138bdad20de741faeca57891645e5a64d9:SCORECARD.md": "ffb67ddb172f55af771681432264b2124b74715eb5678091c7004708f0900008"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC03-2-1.json",
               "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC03-2-2.json",
               "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/coldread/traces/ColdC03-2-3.json"]}]
}
```

Note: read the section (lines 375–404) from a detached fleet-mirror clone at a4f7181; traced full reads of the two cited census case notes and corpus/README.md under tools/trace-inputs.py (receipts rev-matched, exit 0); verified every cited line range (kimi :13-16, :4-7, :34-35; kagi :13-17, :44-45, :54-56), the quoted fingerprints, the no-after-revision claims, the unversioned-driver claim (driver untracked in lane git; kagi R21 erratum concurs), the G-R2-1 attribution in corpus/README.md's round-2 addendum row, and SCORECARD.md:13 via `git show` (SCORECARD is an L1-appended file, so it is recorded under external_inputs). The `--regression` replay was corroborated only partially (two legs PASS exact, correct tool sha) before the 6-minute bound; that capped run is disclosed above and deliberately absent from the receipted command list.

COLDREAD ColdC03: verified-record
