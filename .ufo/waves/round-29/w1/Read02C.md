# Read02C — cold read, SKILL.md "Restore discipline" (lines 375-404)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read02C", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 375, "heading": "## Restore discipline \u2014 before/after identity, not continuous non-write proof", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
    "Rule 2 cites mutation-case-kimi-census.md:4-7 for the `cp -p` wording; those lines support 'edit only copies under /tmp' but the literal `cp -p` command in that note is at :172 (commands appendix). The kagi cite (:44-45) does carry `cp -p` verbatim.",
    "Rule 6 cites SCORECARD.md:13 for 'the historical probes reran from scratch'; that line is the round-2 depth row documenting the ORIGINAL fresh-/tmp-copies run. The rerun claim is better supported by the round-7 ledger row (SCORECARD.md:20) and by tools/mutate-and-run.sh --regression itself, which I verified passing 9/9 with the exact pinned sha256s."],
  "commands_executed": [
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md tools/mutate-and-run.sh",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/README.md",
    "bash tools/mutate-and-run.sh --regression"],
  "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "tools/mutate-and-run.sh", "corpus/README.md"],
  "inputs": {"corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548", "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0", "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "corpus/README.md": "91c782f6803a30f26734793f73733e58bb6afc117965e06cbe4c625b88fd3c67"},
  "external_inputs": {"tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:SCORECARD.md": "004a411d7af71e1977d619f4ef72aba40c9b9db1059b4f2e7d34da023a98dbac"},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read02C-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read02C-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read02C-3.json"]}]}
```

Checked every numbered rule against its cited evidence at the pinned rev:

- **Rule 1** (before-sweep header fields): `mutation-case-kimi-census.md:13-16` records full sha256 `83016d45…4f426`, 43273 B, mtime 2026-10-13 18:53:12, kumitate rev `175de6ba…`, and `git status --porcelain` empty — all five fields. `mutation-case-kagi-census.md:13-17` does the same (`275d8294…53009f`, 44212 B, mtime 09:47:15, kagi HEAD `fecee87…`, porcelain empty). Verified verbatim.
- **Rule 3** (after-sweep fingerprints): kimi `:34-35` records sha256 before=after, size and mtime unchanged, tree clean — and indeed no after-repo revision; kagi `:54-56` records sha256 before=after, 44212 B, mtime 09:47:15 unchanged, porcelain empty, and `cmp`-identical pristine copy. Both exactly as the section states, including the honest "no after-repo revision" admission.
- **Rule 6** (durable evidence): `mutate_driver.py` is unversioned — `git ls-files | grep -c mutate_driver` → 0 — and the kimi note's commands (:172-175) run it from `/tmp`, so a scratch loss does take the driver down. The recommended replay, `bash tools/mutate-and-run.sh --regression`, ran green under the trace collector: `REGRESSION: PASS (cases=9 passed=9; ledger legs exact)`, pinning the identical sha256s the section cites (kimi `83016d45…4f426`, kagi `275d8294…53009f`). It replays via the in-tree runner, not the lost driver — the section's caveat is correct.
- **Rule 7** (dirty-at-pin → G-R2-1): `corpus/README.md:11` carries the kagi gates-survey round-2 addendum where G-R2-1 corrects a pin that caught an intermediate dirty-tree state (79294 B/`357fb245` never committed → re-pinned 79301 B/`93c5827202b9cdec`). Matches the rule's advice to re-pin a committed revision.
- Rules 4, 5 are policy/inference; the section marks rule 5 `(I)` itself.

Minor gaps (citation aim, not substance): the kimi cite for `cp -p` lands on the read-only-substrate sentence rather than the literal `cp -p` line at :172; the `SCORECARD.md:13` cite (read via `git show` at the pinned rev per the L1-append exception) is the round-2 original-run row — the "reran" aspect is better backed by the round-7 ledger row at SCORECARD.md:20 and by the replay I executed. Nothing in the section is false or unverifiable; it does not misstate what the cited records say.
COLDREAD Read02C: gap-minor
