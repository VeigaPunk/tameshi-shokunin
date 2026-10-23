[seat AllFourLesson34] Round-34 lesson all-four cold read — re-credit report

Scope: cold read of `corpus/lessons/round-34.md` (Gate / Mistakes / Holds / Wave), tip
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (detached clone at
`/fast/scratch/hyaku/tameshi-r34-seats/AllFourLesson34/lane`; lesson bytes identical to the
fleet checkout, sha256 `737d4ff98e49dfa3531452ef10be12e231b519fa35374c3040e15bf8174477de`,
73 lines / 4,676 bytes). Lane read-only; all commands below were run in the scratch clone.

## Findings

### F1 (low) — Quote-precision drift in the S101 gate row (line 22)

Lesson L21-22: `Quote (Overview feature list, 15 words): "exporting source-code mutants;
suppressing equivalent mutants; computing the mutant-detection rate and the set of live
mutants"`.

- The string is 16 whitespace-separated tokens, not 15 (`python3 -c` count → `tokens: 16`).
- The quoted span is verbatim against the tag-stripped snapshot
  (`.ufo/evidence/round-34/src/s101-mutation-testing.html`, 4,341 B, sha256
  `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420` — size/hash match the
  lesson), BUT it truncates source list-item 3 mid-sentence: the item reads "computing the
  mutant-detection rate and the set of live mutants for a given set of tests;" (source lines
  44–47). The lesson drops "for a given set of tests" with no ellipsis. Supported claim is
  unaffected; the parenthetical word count and the silent truncation are the drift.
- Reproduce: `python3 -c "s='exporting source-code mutants; suppressing equivalent mutants;
  computing the mutant-detection rate and the set of live mutants'; print(len(s.split()))"`
  → `16`; `grep -n 'equivalent mutants' .ufo/evidence/round-34/src/s101-mutation-testing.html`
  → line 45, plus lines 44/46 for the full item.

### F2 (low) — Cited receipt does not carry the claimed evidence (lines 26–28)

Gate rejection: "unreachable from this host (two timeouts, receipt
`.ufo/evidence/round-34/src/s101-fetch.exit`)". The cited file's entire content is the 11-byte
line `MUT_EXIT=0` (`od -c .ufo/evidence/round-34/src/s101-fetch.exit` → `M U T _ E X I T = 0 \n`;
`wc -l` → 1). It records the successful mutation-testing.org fetch exit, not the gnu.org
timeouts; no other file under `.ufo/evidence/round-34/src/` carries a timeout record (the
directory contains only the two snapshots plus this file — `find .ufo/evidence/round-34/src
-type f`). The timeout fact is independently corroborated by `corpus/SOURCES.md:106` (S097 row:
"rendered page … timed out on 2026-10-23"), so the claim stands but its receipt pointer is
stale/misdirected.

### F3 (info) — Wave section has no pointer to the validated taskCall JSON (lines 70–73)

The Wave section says "the validated taskCall JSON is returned to the orchestrator" and
"seat relays … are folded here on arrival" but names no path. Nothing round-34 exists under
`.ufo/waves/`: `find .ufo/waves/round-34 -type f` → `No such file or directory`, `find . -iname
'*task*call*'` shows only round-23/24 artifacts. Contrast round-33, which committed
`spec-w1.json` / `dispatch-w1.json` / `swarm-registry.json`. Consistent with "zero dispatches
from this session" (the JSON lives orchestrator-side), but the wave's build+validation
artifacts (spec, validation result) have no committed evidence and no named location — the
only pointer to them is this prose.

### F4 (info) — Mistakes pointer names the wrong generation/file (lines 50–52)

"fix … shown able to fail by the caught receipt itself
(`.ufo/evidence/round-34/dev/authoring-receipts.json` first generation, preserved in the
scratch transcript)". Committed `authoring-receipts.json` (3,641 B) is the post-fix
generation: all 14 entries `as_expected: true`. The caught receipt is actually line 7 of the
committed `.ufo/evidence/round-34/dev/authoring.stdout`:
`{"id": "ho-kill-vector-setup-threshold", …, "witness": [false, "vector"], …,
"as_expected": false}` — so the evidence IS committed (the claim is honest) but lives in
`authoring.stdout`, not the JSON named by the pointer, and "scratch transcript" undersells a
committed artifact. The same transcript ends `SEALED: kill=8 accept=6
all_as_expected=False` — cosmetic: "SEALED" prints even on a generation that could not
commit; the sealed set that did land (`c17e593b`) has the corrected witness `[2,0,0,…]`
(`cat .ufo/evidence/round-33/heldout/ho-kill-vector-setup-threshold.json`).

## Verified — no drift (all checks executed at `0b99d48`, exit 0 unless noted)

- Sections present and ordered: title L1, `## Gate` L14, `## Mistakes` L42, `## Holds` L54,
  `## Wave` L66; 73 lines total.
- Pin bytes: `git show 0b99d48:tools/tally-audit-v2.py` sha256
  `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`;
  `tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
  — both match the frozen pins (also Holds L56 `7b11ba25…8d10`).
- Commit chain (L3–8): `66e1fb44` exists, subject "round-32 verifier spot-check (integrator,
  hyaku): non-author admit/reject"; order verified by `git merge-base --is-ancestor`:
  `6aaad5b3` → `9dd3174c` → `c17e593b` → `0b99d48` (each check exit 0; parent links are exact:
  `git rev-parse 9dd3174c^` = `6aaad5b3`, `c17e593b^` = `9dd3174c`). Amendment-6 gate is
  strictly pre-authoring (RevengerWitness report committed at `6aaad5b3`; sealed set first
  commit `c17e593b` — `git log --diff-filter=A -- .ufo/evidence/round-33/heldout/` → exactly
  `c17e593b`; `git diff c17e593b..0b99d48 -- heldout/` → 0 lines, bytes unchanged since authoring).
- Counter: `git show 6aaad5b3:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum` →
  `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`, identical at tip; matches
  `counter_sha256` inside `controls-receipt.json` and `runner_sha256` matches the runner pin.
- Controls receipt: 4 controls, `all_false: true`, per-control kill/accept counts identical to
  `controls/mint.stdout` transcript (`CtlDoNothing 0/18+8/8`, `CtlAlwaysPass 0/18+8/8`,
  `CtlAlwaysFail 18/18+0/8`, `CtlShaOnly 18/18+1/8`).
- Deciding run: `.ufo/evidence/round-34/measure/c1-deciding-run.exit` = `0`; `.stdout` is
  byte-identical to the receipt quoted in the assignment (all counts, seed
  `685f63bd25263908`, rev `c17e593b`, `C1_R33_PASS=true`). No score drift vs the lesson's
  L9–10 quote.
- Sealed set: 14 files = 8 `ho-kill-*` + 6 `ho-accept-*`, all added at `c17e593b`.
- SOURCES: scoped to this round (`git diff 5bfa3b5..0b99d48 -- corpus/SOURCES.md`) → exactly
  one row added (`| S101` at line 109; parent had 97 `^| S` rows, tip 98). "No other cell
  changed" TRUE for the round's own edit. Row content matches lesson: tier C, hash, snapshot
  pointer, `used-by=corpus/knowledge/witness-equivalence-rule.md`; the knowledge file cites
  S097 (L57) and S101 (L62–65) as stated. S097 row (L106) does record the gnu.org timeout,
  supporting the rejection's duplicate-scope reasoning. NOTE: the base→tip span also contains
  the round-33 S100 row (`732b686`, `5bfa3b5`), so "rows 97 → 98" is correct only read
  round-scoped — it is, and the commit subject itself says "98 rows".
- Census: `census-end.exit` = `0`; stdout shows `tameshi W01 S101 tierC mined
  used-by=corpus/knowledge/witness-equivalence-rule.md` and `ok …/corpus/SOURCES.md` (8
  pre-existing W04 duplicate-url warnings unrelated to this round).
- Holds: LedgerAudit sizing "~19 SOURCES-citing + 3 all-four" verified —
  `.ufo/waves/round-33/w1/LedgerAudit.md` L58–68 lists exactly 19 SOURCES-citing section
  starts and exactly 3 sections citing all four families. DevPrintf whole-stdout class is
  recorded at `corpus/lessons/round-33.md:61` and `:132` and the seat report exists
  (`.ufo/waves/round-33/w1/DevPrintf.md`). r33 baseline "64/64 restraint 8" verified:
  `.ufo/evidence/round-33/dev/monitor-at-freeze.stdout` has `"calibration_restraint_score": 8`
  (and LedgerAudit L8 records 64/64 at `f6d8a89`, exit 0); no monitor/baseline file exists
  under `.ufo/evidence/round-34/` (full listing taken), consistent with "not re-run this round".
- SCORECARD: capabilities table row admitted this round with the same receipt text; numeric
  axes note "depth 9 → 9 … no owned axis score lowered" (SCORECARD.md tail).
- LOG: entries for receipt minting, deciding run (verbatim receipt, exit 0), frontier/census,
  and wave dispatch consistent with the lesson (LOG.md tail).
- Selftest/panel receipts: `dev/tool-selftest.stdout` `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`;
  `dev/panel.stdout` `PANEL: kill=18/18 accept=8/8`.

## Commands relied on (all inside the scratch clone, lane at 0b99d48)

`git clone --no-hardlinks` + `checkout --detach 0b99d48` (exit 0); `git show 0b99d48:<path>`
for pinned bytes; `sha256sum` on tool/runner/counter/snapshot copies; `git log --oneline
66e1fb44..0b99d48`; `git merge-base --is-ancestor` (exit 0 for each claimed ordering);
`git log --diff-filter=A -- .ufo/evidence/round-33/heldout/` (→ `c17e593b` only); `git diff
5bfa3b5..0b99d48 -- corpus/SOURCES.md` (1 insertion); `find .ufo/waves/round-34` (exit 1, dir
absent); `od -c .ufo/evidence/round-34/src/s101-fetch.exit`; `cat`/`grep`/`wc`/`python3 json`
reads of all files cited above. The counter was not executed (kill rule consumed); no lane
writes, no installs (pacman pause honored — nothing needed).

## Verdict

Lesson is materially accurate: ordering, pins, receipt text, counts, and Holds provenance all
check out at the tip. Findings are two LOW drifts (F1 word-count/truncation; F2 stale receipt
pointer) and two INFO pointer imprecisions (F3 no committed wave-artifact location; F4 wrong
generation/filename for the caught receipt). The deciding-run receipt stands unchallenged.
