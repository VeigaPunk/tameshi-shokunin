# Read02A — cold read, SKILL.md:375 "## Restore discipline — before/after identity, not continuous non-write proof"

Class decision: **instruction**. The section is phrased as a policy a reader applies
("Apply this policy in order", items 1–7: record fingerprints, `cp -p` into scratch,
`git status --porcelain`, never `git checkout`/`git restore`, run
`bash tools/mutate-and-run.sh --regression` for replay). The cited line ranges are its
own evidence trail — so each was checked as a record claim too.

## What was executed (all under `tools/trace-inputs.py`, rev 9f3084bc)

1. Record-read of the three cited lane files — receipt `Read02A-1.json` (exit 0).
2. The fingerprint discipline itself on `corpus/knowledge/mutation-case-kimi-census.md`:
   before sha256 `034524eff8f1…` / 15679 B / mtime / `git status --porcelain` empty;
   `cp -p` into `/tmp` scratch, edit only the copy; after sha256 identical,
   `cmp` diff on the copy only, porcelain still empty — receipts `Read02A-2.json`
   (exit 0) and `Read02A-4.json` (exit 0). Endpoint identity held; only scratch wrote.
3. `timeout 390 bash tools/mutate-and-run.sh --regression` — the step-6 replay.
   All nine ledger legs materialized from pinned sibling blobs and matched the recorded
   tables exactly: `REGRESSION: PASS (cases=9 passed=9; ledger legs exact:
   killed-delta<=0 flips<=0)`, exit 0, ~260 s wall under strace — receipt
   `Read02A-3.json`.

## Claim checks

- Item 1 header fields: kimi note :13-16 records full sha256 `83016d45…4f426`, 896 L /
  43273 B, mtime, kumitate rev `175de6ba`, porcelain empty — matches. Kagi :13-17
  records `275d8294…53009f`, 44212 B, mtime `09:47:15 -0300`, mode 755, kagi HEAD
  `fecee87`, porcelain empty — matches.
- Item 2 "edits in scratch / `cp -p`": kimi :4-7 (all mutants are copies under
  `/tmp/tameshi-r2-1-work`, substrate read-only) and kagi :44-45 (`cp -p` byte copy,
  `cmp`-verified) — matches.
- Item 3 after-sweep records: kimi :34-35 (hash before = after `83016d45…4f426`,
  size 43273 B, mtime unchanged, tree clean; **no after-repo revision recorded** — the
  claim's "no after-repo revision" is accurate, the pin :15 is the before rev). Kagi
  :54-56 (hash `275d8294…53009f`, 44212 B, mtime `09:47:15`, porcelain empty,
  `cmp`-identical pristine) — matches, and likewise records no after-repo revision.
- Item 6: `SCORECARD.md:13` documents round-2 re-runs from the retained scratch
  (`sensitivity re-runs from the lane's retained scratch: node /tmp/tameshi-r2-1-work/…`).
  Both case notes' §4 reproduce commands call `/tmp/…/mutate_driver.py`, which is
  unversioned (not in `git ls-files`; kagi note :271-272 says so verbatim) — matches.
  The maintained replay it points to ran and passed (trace 3).
- Item 7's "G-R2-1 lesson, corpus/README.md round-2 addendum": README addendum row
  records the kagi claim-ledger pin corrected to 79301 B / `93c5827202b9cdec` because the
  surveyed pin "was an intermediate dirty-tree state never committed" — the dirty-pin
  lesson the section teaches. Match.

## Minor gaps (none blocking)

- Typo-run-ons inside the section: "hash83016d45…4f426,43273B", "unchanged09:47:15
  mtime" — missing separators; the cited records still check out.
- Section claims "before … repo revision" but neither case note records an *after*-repo
  revision; the section itself says so, so it is honest, just incomplete by design.

## Receipts

- `.ufo/evidence/round-29/coldread/traces/Read02A-1.json` — record read (3 inputs)
- `.ufo/evidence/round-29/coldread/traces/Read02A-2.json` — fingerprint + scratch-edit
  policy execution (exit 0 after stat-syntax fix; `.gitignore` picked up by `git status`)
- `.ufo/evidence/round-29/coldread/traces/Read02A-3.json` — `mutate-and-run.sh
  --regression`, 9/9 legs PASS (exit 0)
- `.ufo/evidence/round-29/coldread/traces/Read02A-4.json` — five-field fingerprint
  (sha256 + size + mtime + rev + porcelain)

All receipts: `rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5`, `live_lane_reads={}`.
SCORECARD.md and the lane-level reads were taken via `git show 9f3084bc…:<path>` outside
the collector and are recorded in `external_inputs`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read02A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 375, "heading": "## Restore discipline — before/after identity, not continuous non-write proof", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["run-together renderings inside the section: 'hash83016d45…4f426,43273B' and 'unchanged09:47:15 mtime' — missing separators", "before-fingerprint lists repo revision but neither case note records an after-repo revision — section itself names this gap, so it is honest but the proof remains before/after identity only"],
    "commands_executed": ["python3 -c \"import sys;[print(open(p, encoding='utf-8', errors='replace').read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/README.md", "bash -c 'p=corpus/knowledge/mutation-case-kimi-census.md; b=$(sha256sum $p|cut -d\" \" -f1); s=$(stat -c %s $p); m=$(stat -c %y $p); echo BEFORE $b $s $m; git status --porcelain -- $p; echo PORCELAIN-EMPTY; cp -p $p /tmp/Read02A-sweep-*/copy.md; echo SCRATCH-EDIT >> /tmp/Read02A-sweep-*/copy.md; a=$(sha256sum $p|cut -d\" \" -f1); echo AFTER $a; [ $a = $b ] && echo ENDPOINT-IDENTITY-OK; cmp -s $p /tmp/Read02A-sweep-*/copy.md && echo CMP-SAME || echo CMP-DIFF-EDIT-IN-SCRATCH-ONLY; git status --porcelain -- $p; echo PORCELAIN-STILL-EMPTY'", "timeout 390 bash tools/mutate-and-run.sh --regression", "bash -c 'p=corpus/knowledge/mutation-case-kimi-census.md; sha256sum $p; stat -c \"%s %y\" $p; git rev-parse HEAD; git status --porcelain -- $p; echo PORCELAIN-EMPTY'"],
    "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/README.md", "tools/mutate-and-run.sh", "tools/trace-inputs.py", ".gitignore"],
    "inputs": {"corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548", "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0", "corpus/README.md": "91c782f6803a30f26734793f73733e58bb6afc117965e06cbe4c625b88fd3c67", "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4", ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116", ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7"},
    "external_inputs": {"tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:SCORECARD.md": "004a411d7af71e1977d619f4ef72aba40c9b9db1059b4f2e7d34da023a98dbac"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read02A-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read02A-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read02A-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read02A-4.json"]}]}
```

COLDREAD Read02A: executed-ok
