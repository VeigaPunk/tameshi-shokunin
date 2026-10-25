# ReviewQ124 — quarantined `tameshi` round2 S124 (axis: depth)

## Verdict: PRESENT — the quoted line is in the cited source; the register's `payload-absent` verdict is falsified

The register row claims "cited source, companion URLs and local artifacts were all
checked; the quote is in none of them". That claim is false: the quote occurs
verbatim in the cited repository at the revision the row's own Gate pins, in ten
committed evidence records, and the cited instrument reproduces it live.

## The row under check

- Register: `.ufo/waves/corpus-expansion-1/absent-defect-register.md` (shokuknow) line 220:
  `tameshi | round2 | S124 | payload-absent | https://github.com/VeigaPunk/tameshi-shokunin`
  quote `SNAPSHOT_OBSERVED id=controls_match exit=0`, reason "the quote is in none of them".
- Row identified despite id drift: the only round2 `tameshi` row carrying that quote/URL is the
  repeat-control instrument row — currently numbered **S128** in
  `shokuknow/lanes/tameshi/round2/SOURCES-PROPOSED.md` (`## Gate — S128`, lines 70–74), whose
  Gate pins "read at revision `d16f9b5a` in a scratch copy". Dispatch-time scout summary
  (`.ufo/scopes/corpus-expansion-1/ScoutTameshi.md`) corroborates that round2's last own-work
  row was S124 at register-compile time (later shifted +4). `ID-REMAP.md` records **no** round2
  mapping — the remap file is incomplete relative to that shift (observation only; register not edited).
- Companion corpus copy agrees: `lanes/tameshi/round2/KNOWLEDGE-PROPOSED.md:242` records the
  same verbatim gate output block.

## Fetch and reproduction (2026-10-24, scratch `/tmp/tameshi-r40-ReviewQ124/`)

Cited source = the lane's own public repository; the local checkout's `origin` is exactly
`https://github.com/VeigaPunk/tameshi-shokunin.git` (`git remote -v`), and `curl` answers
HTTP 200 for the cited URL — same-identity reroute to the local clone is sound.

1. Pinned revision resolves: `git rev-parse d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` →
   subject "round-35: tally-audit-v3 … C1/C2 counters frozen …", 2026-10-23T17:31:25-03:00;
   `git merge-base --is-ancestor <rev> HEAD` → ancestor of HEAD.
2. Quote present in the cited tree (committed):
   `git grep -cF 'SNAPSHOT_OBSERVED id=controls_match exit=0' d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc -- .ufo/evidence`
   → **10 files**, each 1 occurrence: `.ufo/evidence/round-12/verification.json`,
   `verification-progress.json`, `verification-final.json`, and seven `.ufo/evidence/round-17/`
   records (`c2-after-*.json`, `c2-before-*.json`, `registry-before-manual.json`,
   `registry-full-*.json`). Also present at HEAD (`git grep -lF … HEAD -- .ufo/evidence`).
   The string has been in the tree since round-12 (introducing commits `5a0859e`, `9df9212`,
   2026-10-20) — a HEAD-time search could not have missed it.
3. Quote reproduced live from the cited source (read-only gate, no mutation):
   ```
   git archive d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc | tar -x -C /tmp/tameshi-r40-ReviewQ124/rev
   cd /tmp/tameshi-r40-ReviewQ124/rev
   python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
   ```
   → exit 0, stdout ends:
   `SNAPSHOT_INPUTS 9 verified` / `SNAPSHOT_EXPECTED id=controls_match exit=0` /
   **`SNAPSHOT_OBSERVED id=controls_match exit=0`** / `REPEAT_CONTROL: controls_match`
   (captured at `/tmp/tameshi-r40-ReviewQ124/rerun.stdout`).
4. Instrument self-consistency at that revision: the tool's self-reported `tool-sha256=` equals
   `sha256sum tools/repeat-control.py` (compared in-process → EQUAL), so the recorded receipt and
   the live receipt are the same tool's output.

## Why the register missed it (candidates, unproven)

The register stores no fetch log, so the miss cannot be attributed definitively. The quote was
reachable by every route the row names: cited source at the pinned revision (committed since
2026-10-20), local artifacts (the lane checkout itself), and the live URL (HTTP 200). Plausible
mechanisms: the checker's search scope covered proposal/source text but not `.ufo/evidence/**`
JSON records, or a fetch failure was scored as absence. Not resolved here.

## Residual risk and verification gaps

- Exact byte transcription above passed through lossy display channels; load-bearing facts were
  each confirmed channel-independently (fixed-string grep counts, in-process sha equality,
  ancestor test, HTTP status), not by eyeballing.
- The sibling quote in the same Gate (`REPEAT_COMPARE identical=yes runs=3`) and the register's
  round2 S126 row (`MTE_INTEROP: SETUP …`) are sibling tickets — not checked here.
- The quote is a run receipt, not documentation prose: if the register's matching rule required
  the line in a non-evidence source file, "present" would still hold for the row's own Gate
  wording ("Quote (frozen-snapshot gate, `SNAPSHOT_OBSERVED` line)"), which cites the live run.

## Bounds

Read-only throughout: no lane checkout/index/jj mutation (`--no-optional-locks` git only),
shokuknow read-only, register untouched, scratch confined to `/tmp/tameshi-r40-ReviewQ124/`.
No tool installs (none needed).
