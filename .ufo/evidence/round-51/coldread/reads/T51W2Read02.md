# T51W2Read02 — cold-read re-key reader, `## Restore discipline — before/after identity, not continuous non-write proof`

Seat T51W2Read02, round 51 wave 2 (falsify). Candidate (CAND) `6d8c11e378aa90b12650808e1b79270742935f15`,
base `9962033fd7a75aa2f2847e979dd687a5d28505a1`. Read-only on the lane/fleet/sibling repos; every experiment
ran inside scratch under `/fast/scratch/hyaku/tameshi-r51/T51W2Read02/` (deleted before yield). No tools
installed. The contract (`.ufo/evidence/round-51/contract.json`) and the C1/C2/C3 counter docstrings were
read before the item; the C2 counter's `regression()` body (`.ufo/evidence/round-51/c2/measure.py:162-187`)
is the recipe my live run replicates. The re-key that consumes this row is
`.ufo/evidence/round-51/coldread/refresh.py` (round-49 method, round-21 monitor).

## 1. The section at CAND

Heading re-resolved at CAND (not taken from the fixture list or the old READERS_JSON): the heading starts at
SKILL.md:375; the next heading is `## Cross-language divergence — bash vs JS (round 3, measured)` at
SKILL.md:405; no other heading line sits between. The section is SKILL.md:375-404 (29 non-blank lines after
trailing-blank trim), section sha256
`83c2ceddd3455d5973318e77547580cad7ef863aeeac110c70e42cf0c2e5deaa` — **byte-identical to base** (the
SKILL.md diff base→CAND is a single hunk `@@ -2134,3 +2134,38 @@`, the round-51 registry append; no line
before 2134 moved). Verbatim:

```
## Restore discipline — before/after identity, not continuous non-write proof

All substrate edits must stay in scratch. Before/after fingerprints establish endpoint
identity, not that no transient write occurred. Apply this policy in order:

1. **Before the sweep:** sha256 (full), size, mtime, repo revision, and
   `git status --porcelain -- <path>` empty — recorded in the note's header
   (mutation-case-kimi-census.md:13-16; mutation-case-kagi-census.md:13-17).
2. **All edits in scratch:** `cp -p` the artifact into scratch outside
   the lane and edit only copies (mutation-case-kimi-census.md:4-7, :172;
   mutation-case-kagi-census.md:44-45).
3. **After the sweep:** require endpoint fingerprints to agree; historical
   Kimi recorded hash 83016d45…4f426, 43273 B, unchanged mtime and path cleanliness
   (mutation-case-kimi-census.md:34-35); no after-repo revision was recorded.
   Kagi recorded hash 275d8294…53009f, 44212 B, unchanged 09:47:15 mtime,
   clean path and `cmp`-identical scratch copy (mutation-case-kagi-census.md:54-56).
   Its after-repo revision is likewise not established by those records.
4. **A drift is an incident:** stop, report it as one, do not "repair" by
   rewriting — a repair would itself be an unauthorized write.
5. **Never restore via `git checkout`/`git restore`.** Those write to the
   substrate; the only correct end state is *never-modified*. (I)
6. **Retain durable evidence.** The historical probes' sensitivity re-runs read the lane's retained scratch
   (`SCORECARD.md:13`), but the case-note commands rely on an unversioned
   `mutate_driver.py` (one-off and not in-tree; `SCORECARD.md:16`) and do not directly rebuild after scratch loss.
   Use the maintained `bash tools/mutate-and-run.sh --regression` ledger
   replay for those pinned cases; it does not recover the old driver.
7. **If the artifact was already dirty at pin time:** that pin is not a clean
   baseline — record the dirty state exactly, or better, stop and re-pin a
   committed revision (the G-R2-1 lesson, corpus/README.md round-2 addendum).
```

Why it is a re-key target: the round-21 ledger (`.ufo/evidence/round-21/coldread/ledger.json`, 511 entries)
holds 18 entries for this heading; the last two (round-49 re-keys, read_rev `9b9b2a01` / `54a52365`, verdict
`verified-record`) pin inputs `SKILL.md`, both case notes, and `tools/mutate-and-run.sh` =
`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (the base runner sha). At CAND the
runner sha256 is `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda` (C2's tenth leg +
the r51 TMPDIR change; diff +126/−47) → `input-drift:tools/mutate-and-run.sh` (the reason class the
precheck parses, `.ufo/evidence/round-48/quality/coldread-precheck.sh:25`). The section's own bytes did not
change; the runner it cites did. That is exactly what this row re-binds.

## 2. Pointer inventory (extractor cross-check, not the fixture list)

Ran the round-49 extractor that refresh.py reuses (`.ufo/evidence/round-49/c1/measure.py`, `extract` +
`resolve` + the VOLATILE split) on the section text at CAND: **11 pointer tokens** → direct non-record
`{corpus/knowledge/mutation-case-kimi-census.md, corpus/knowledge/mutation-case-kagi-census.md,
tools/mutate-and-run.sh}`, records (blob-read) `{SCORECARD.md, corpus/README.md}`, no internal pointer.
This matches the fixture list's entry for the section (T51ExecRekey.md:105-107) token for token — verified,
not trusted.

Input stability at CAND: both case notes are **byte-identical base→CAND** (kimi
`034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548`, kagi
`d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0` — the same shas the round-49 ledger
entries pin), so every line-range pointer into them is stable. SCORECARD.md grew +12 but its only hunk is
`@@ -2444,3 +2444,15 @@` and README.md grew +26 with its only hunk at `@@ -606,3 +606,29 @@` — the cited
lines (:13, :16; the round-2 addendum rows at :10-11) are byte-identical to base. No pointer moved.

## 3. Pointers verified against candidate bytes

Method: `git show CAND:<path>` / `git cat-file` reads of committed bytes; the one runnable instruction was
executed end-to-end in a `--shared` clone checked out `--detach` at CAND
(`/fast/scratch/hyaku/tameshi-r51/T51W2Read02/reg/fleet/tameshi-shokunin`, `git rev-parse --show-toplevel`
asserted equal to the clone, owner repos `kumitate-shokunin`/`kagi-shokunin`/`tsukuroi-shokunin`/
`mado-shokunin` symlinked beside it as the C2 counter's `regression()` does, `TMPDIR` pointed into my
scratch). No lane/fleet/sibling repo was written; no fixture commit was made.

### P1 `mutation-case-kimi-census.md:13-16` (item 1) — **holds**

- Raw: "sha256 (full), size, mtime, repo revision, and `git status --porcelain -- <path>` empty — recorded
  in the note's header (mutation-case-kimi-census.md:13-16; …)"
- File `corpus/knowledge/mutation-case-kimi-census.md`, lines 13-16 (unchanged base→CAND).
- Located excerpt: `:13` "Artifact under test (O: `sha256sum`, `stat`, `git rev-parse`): sha256" · `:14`
  "`83016d45049b009a…4f426`, 896 lines, 43273 B," · `:15` "mtime 2026-10-13 18:53:12; kumitate repo
  `175de6ba2e9e904010411b19cab27e0af9aad3d4`," · `:16` "`git status --porcelain -- scripts/kimi-census.mjs` empty."
- All five claimed elements (full sha256, size, mtime, repo revision, empty porcelain) are present in the
  cited span, in the note's header (before §0). Holds.

### P2 `mutation-case-kagi-census.md:13-17` (item 1) — **holds**

- Raw: same sentence, Kagi half.
- File `corpus/knowledge/mutation-case-kagi-census.md`, lines 13-17 (unchanged base→CAND).
- Located excerpt: `:13` "Artifact under test (O: `sha256sum`, `stat`, `git`): sha256" · `:14`
  "`275d8294a94e9eb7…53009f`, 44212 B, 886 newlines …" · `:15` "… mtime 2026-10-14 09:47:15 -0300," ·
  `:16` "mode 755; kagi `HEAD fecee8743e52eb8fb5fbb40782934cb619a1a96e`," · `:17`
  "`git status --porcelain -- corpus/surface-census.sh` empty."
- Same five elements present in the header span. Holds.

### P3 `mutation-case-kimi-census.md:4-7` (item 2) — **holds**

- Raw: "`cp -p` the artifact into scratch outside the lane and edit only copies (mutation-case-kimi-census.md:4-7, :172; …)"
- Located excerpt: `:4` "Substrate: kumitate-shokunin **read-only** — every mutant is a copy under" · `:5`
  "`/tmp/tameshi-r2-1-work/`, and no fleet file was written." · `:6-7` "No live `~/.kimi-code` path was
  read: every run is `--selftest` … or `--root` pointed at an empty dir under `/tmp`."
- Supports "edits only copies, scratch outside the lane" (the work root is `/tmp`, outside the lane). Holds.

### P4 `mutation-case-kimi-census.md:172` (item 2) — **holds**

- Located excerpt: `:172` "cp -p kumitate-shokunin/scripts/kimi-census.mjs /tmp/tameshi-r2-1-work/pristine.mjs"
- The `cp -p` command is at exactly :172 (grep-pinned; my first sed-range read mis-numbered it, the grep is
  authoritative). Holds.

### P5 `mutation-case-kagi-census.md:44-45` (item 2) — **holds**

- Located excerpt: `:44` "- O: each defect = ONE exact-string replacement applied to a fresh copy of
  `pristine.sh` (a" · `:45` "`cp -p` byte copy, `cmp`-verified); the driver asserts the old string occurs
  exactly once before"
- `cp -p` byte copy, `cmp`-verified — exactly the claim. Holds.

### P6 `mutation-case-kimi-census.md:34-35` (item 3) — **holds**

- Raw: "historical Kimi recorded hash 83016d45…4f426, 43273 B, unchanged mtime and path cleanliness
  (mutation-case-kimi-census.md:34-35); no after-repo revision was recorded."
- Located excerpt: `:34` "- O: restore proof — original sha256 before `83016d45…4f426` and after
  `83016d45…4f426`;" · `:35` "size 43273 B and mtime unchanged; kumitate working tree clean for that path."
- Every element verified; the negative claim "no after-repo revision was recorded" is true of :34-35 (no
  repo rev appears there; the header's `175de6ba…` at :15 is the before-pin). Hash ellipsis matches the
  full recorded sha. Holds.

### P7 `mutation-case-kagi-census.md:54-56` (item 3) — **holds**

- Raw: "Kagi recorded hash 275d8294…53009f, 44212 B, unchanged 09:47:15 mtime, clean path and
  `cmp`-identical scratch copy (mutation-case-kagi-census.md:54-56). Its after-repo revision is likewise
  not established by those records."
- Located excerpt: `:54` "- O: restore proof — kagi sha256 before `275d8294…53009f` and after
  `275d8294…53009f`; 44212 B and" · `:55` "mtime 09:47:15 unchanged; `git status --porcelain` for the path
  empty; `/tmp/…/pristine.sh` still" · `:56` "`cmp`-identical to the kagi original after the sweep."
- All elements verified; :54-56 indeed record no after HEAD (the before HEAD `fecee87…` sits in the header
  :16-17). Holds.

### P8 `SCORECARD.md:13` (item 6) — **holds**, one scope note

- Raw: "The historical probes' sensitivity re-runs read the lane's retained scratch (`SCORECARD.md:13`)"
- File `SCORECARD.md` (VOLATILE record; read as the CAND blob), line 13 — byte-identical to base (the
  SCORECARD diff's only hunk is at :2444).
- Located excerpt (line 13, round-2 depth move-log row): "… sensitivity re-runs from the lane's retained
  scratch: `node /tmp/tameshi-r2-1-work/mutant-D2.mjs --root /tmp/tameshi-r2-1-work/empty-root | tail -1`
  → 5 ids + `+23 more`, `node /tmp/tameshi-r2-1-work/mutant-D10.mjs … | grep 'FAMILY K2'` → `frozen=24`
  (both survivors observably different off-suite, as claimed) …"
- The pointer is exact for the round-2 (Kimi) probe. Scope note: the sentence's plural "the historical
  probes'" is broader than the single pointer — SCORECARD:15 (round-3 row) records the Kagi probe's
  re-verification as a full independent re-sweep through the shipped tool from a spec cut from the pinned
  artifact, not a retained-scratch re-run, and no `r3-1-work` scratch appears anywhere in SCORECARD. The
  fragility the item asserts (re-runs depend on retained scratch that the repo cannot rebuild) still holds
  for both probes — the Kagi note itself records its scratch contents (`:210`) and the same driver
  dependence (`:271-272` "The old §7 commands depend on an unversioned scratch `mutate_driver.py`; they do
  not by themselves recreate that driver after scratch loss."). Recorded as a scope note, not a defect:
  the cited line says what the section claims it says.

### P9 `SCORECARD.md:16` (item 6) — **holds**

- Raw: "the case-note commands rely on an unversioned `mutate_driver.py` (one-off and not in-tree; `SCORECARD.md:16`)"
- Located excerpt (line 16, round-3 operability move-log row): "… a per-lane ad-hoc driver left in /tmp
  (round 2's `mutate_driver.py` was one-off, unversioned, not in-tree) …"
- Corroborated at CAND: `git ls-tree -r CAND | grep mutate_driver` → 0 matches (not in-tree); the case-note
  command blocks call `/tmp/…/mutate_driver.py` (kimi :174-175, kagi :245-246). Holds.

### P10 `tools/mutate-and-run.sh` (item 6, bare path — the drifted input) — **holds, run live at CAND**

- Raw: "Use the maintained `bash tools/mutate-and-run.sh --regression` ledger replay for those pinned
  cases; it does not recover the old driver."
- File `tools/mutate-and-run.sh` at CAND (2159 lines; sha `977de47034cbe52b…`), no line range cited.
- Verified in the CAND bytes: `--regression` exists (usage `:206` "mutate-and-run.sh --regression
  [--workdir DIR] [--keep]"; engine from `:590`); it replays the leg ledger — ten legs at CAND, the two
  historical census cases first (`:1459-1464` `regression_case_git js-kimi-census …
  'kumitate-shokunin/scripts/kimi-census.mjs' "$PIN_JS" "$REV_JS"`, `regression_case_git bash-surface-census
  … 'kagi-shokunin/corpus/surface-census.sh' "$PIN_BASH" "$REV_BASH"`), so "those pinned cases" are covered;
  the r51 TMPDIR change is real (`:148-150` "Scratch root: mktemp -d `${TMPDIR:-/tmp}/…` by default (r51
  honours TMPDIR)"); and the runner's only `mutate_driver` mention is a comment about the round-5 manifest
  used to *generate* a spec (`:755-758`) — the replay embeds the specs and does not ship or recover the old
  driver, exactly as the item says.
- **Strongest falsifier, run end-to-end at CAND:** the cited command itself. `TMPDIR=$S/tmp bash
  tools/mutate-and-run.sh --regression --workdir $S/work` in the fleet-mirror clone → **exit 0**, terminal
  line `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)`, wall 242.2 s.
  All ten `REGRESSION_CASE` lines PASS; the two census legs reproduced their committed tables
  (js-kimi-census 8/10, bash-surface-census 8/10 — match=10/10, flips=0 each), and the tenth leg
  `bash-drift-pins` (kagi `corpus/drift-pins.sh` @ `e64e81b8`, pin `c138d34c…`) reproduced its committed
  2/10 table (`MUTATE: DONE (… killed=2 survived=8 …)`, match=10/10, flips=0) — consistent with the
  disclosed harness-masking finding (K_GONE_ARM/K_AMBIG_GT/K_SHAPE_OPTIN survive in the registered suite;
  the regression band checks killed-delta/flips, not off-suite witnesses, so nothing here contradicts the
  disclosed 5/10 neutral-path result). Had any leg drifted from its committed table, the run would exit 1
  and item 6's "maintained replay" would be false. It passed. This is an independent replication of
  sibling seat T51W2Read16's end-to-end run (239.7 s, same terminal line).
- The runner's selftest is not this section's claim (C3's row covers it); not re-run here.

### P11 `corpus/README.md` round-2 addendum (item 7) — **holds**

- Raw: "… stop and re-pin a committed revision (the G-R2-1 lesson, corpus/README.md round-2 addendum)."
- File `corpus/README.md` (VOLATILE record; CAND blob), the round-2 addendum rows at :10-11 — byte-identical
  to base (README's only hunk is at :606+).
- Located excerpt (:11, the `knowledge/gates-survey-kagi.md — round-2 addendum (G-R2-1…6, append-only)` row):
  "§1 claim-ledger pin corrected: **79301 B / sha256 first16 `93c5827202b9cdec`** — the surveyed
  79294/`357fb245` was an intermediate dirty-tree state never committed; … (G-R2-1)"
- The lesson the item glosses (a pin taken from a dirty, never-committed state is not a clean baseline;
  re-pin the committed revision) is what the addendum records. Holds.

## 4. Adversarial sweep against the round's changes

- **Tenth leg (C2):** adds leg 10 to the replay. Item 6 says "for those pinned cases" — the replay is now a
  superset (the two census cases are still legs 1-2 and still replayed at their pinned blobs); the
  instruction stays true. No falsity introduced.
- **Runner TMPDIR change (r51):** the section names no temp path anywhere; item 2's "scratch outside the
  lane" is the manual policy (the case notes' `/tmp` work roots), not a claim about the runner's scratch
  root. The new TMPDIR-honouring behavior was observed directly in my run (the regression's auto workdir
  machinery used my `TMPDIR`). No conflict.
- **Four panel-tool updates (amendment 2: `tools/tally-audit.py`, `tools/tally-audit-v2.py`,
  `tools/tally-audit-v3.py`, `tools/mte-interop.py`):** none is cited by this section (extractor
  inventory §2 is exhaustive). No impact.
- **Statement-level falsifiers attempted and closed:** (a) the two negative claims "no after-repo revision
  was recorded" / "likewise not established" — checked the cited spans contain no repo rev (P6/P7); (b)
  hash ellipses match the full recorded shas (`83016d45…4f426`, `275d8294…53009f`); (c) "unchanged mtime"
  for Kimi — `:35` records it, header `:15` gives the value; (d) item 5's premise that `git
  checkout`/`git restore` write the substrate — true of the commands by definition, and correctly tagged
  (I); (e) "does not recover the old driver" — driver absent from the CAND tree (0 ls-tree matches), the
  replay embeds specs (P10); (f) the one runnable instruction executed end-to-end at CAND (P10, PASS).
- **Unsupported-premise hunt:** the only wording broader than its pointer is item 6's plural "the
  historical probes'" (P8 scope note). Everything else is pointer-backed at CAND bytes.

## 5. Row for reads.json

```json
{
  "seat": "T51W2Read02",
  "heading": "## Restore discipline — before/after identity, not continuous non-write proof",
  "read_rev": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "skill_lines": {"start": 375, "end": 404},
  "section_sha256": "83c2ceddd3455d5973318e77547580cad7ef863aeeac110c70e42cf0c2e5deaa",
  "section_vs_base": "byte-identical (SKILL.md diff base→CAND is one hunk at :2134+)",
  "rekey_reason": "input-drift:tools/mutate-and-run.sh (ledger pins a7d3f2dd…, CAND runner is 977de470…)",
  "extractor_crosscheck": {"tokens": 11, "direct": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "tools/mutate-and-run.sh"], "records": ["SCORECARD.md", "corpus/README.md"], "internal": []},
  "pointers": [
    {"raw": "mutation-case-kimi-census.md:13-16", "file": "corpus/knowledge/mutation-case-kimi-census.md", "ranges": ["13-16"], "verdict": "holds", "excerpt": ":14 '83016d45049b009a…4f426, 896 lines, 43273 B' · :15 'mtime 2026-10-13 18:53:12; kumitate repo 175de6ba…' · :16 'git status --porcelain -- scripts/kimi-census.mjs' empty"},
    {"raw": "mutation-case-kagi-census.md:13-17", "file": "corpus/knowledge/mutation-case-kagi-census.md", "ranges": ["13-17"], "verdict": "holds", "excerpt": ":14 '275d8294…53009f, 44212 B' · :15 'mtime 2026-10-14 09:47:15 -0300' · :16 'kagi HEAD fecee87…' · :17 'git status --porcelain -- corpus/surface-census.sh' empty"},
    {"raw": "mutation-case-kimi-census.md:4-7", "file": "corpus/knowledge/mutation-case-kimi-census.md", "ranges": ["4-7"], "verdict": "holds", "excerpt": ":4-5 'Substrate: kumitate-shokunin read-only — every mutant is a copy under /tmp/tameshi-r2-1-work/, and no fleet file was written'"},
    {"raw": "mutation-case-kimi-census.md:172", "file": "corpus/knowledge/mutation-case-kimi-census.md", "ranges": ["172"], "verdict": "holds", "excerpt": ":172 'cp -p kumitate-shokunin/scripts/kimi-census.mjs /tmp/tameshi-r2-1-work/pristine.mjs'"},
    {"raw": "mutation-case-kagi-census.md:44-45", "file": "corpus/knowledge/mutation-case-kagi-census.md", "ranges": ["44-45"], "verdict": "holds", "excerpt": ":44-45 'fresh copy of pristine.sh (a cp -p byte copy, cmp-verified)'"},
    {"raw": "mutation-case-kimi-census.md:34-35", "file": "corpus/knowledge/mutation-case-kimi-census.md", "ranges": ["34-35"], "verdict": "holds", "excerpt": ":34 'restore proof — original sha256 before 83016d45…4f426 and after 83016d45…4f426' · :35 'size 43273 B and mtime unchanged; kumitate working tree clean for that path'"},
    {"raw": "mutation-case-kagi-census.md:54-56", "file": "corpus/knowledge/mutation-case-kagi-census.md", "ranges": ["54-56"], "verdict": "holds", "excerpt": ":54 'sha256 before 275d8294…53009f and after 275d8294…53009f; 44212 B' · :55 'mtime 09:47:15 unchanged; git status --porcelain for the path empty' · :56 'cmp-identical to the kagi original after the sweep'"},
    {"raw": "SCORECARD.md:13", "file": "SCORECARD.md", "ranges": ["13"], "verdict": "holds", "excerpt": ":13 'sensitivity re-runs from the lane's retained scratch: node /tmp/tameshi-r2-1-work/mutant-D2.mjs … → 5 ids + +23 more … (both survivors observably different off-suite, as claimed)'", "note": "scope: the plural 'the historical probes'' exceeds the single pointer — SCORECARD:15 records round 3's re-verification via the shipped tool, not retained scratch; the scratch-dependence claim itself holds for both probes (kagi note :210, :271-272)"},
    {"raw": "SCORECARD.md:16", "file": "SCORECARD.md", "ranges": ["16"], "verdict": "holds", "excerpt": ":16 'round 2's mutate_driver.py was one-off, unversioned, not in-tree' (corroborated: 0 ls-tree matches at CAND)"},
    {"raw": "bash tools/mutate-and-run.sh --regression", "file": "tools/mutate-and-run.sh", "ranges": [], "verdict": "holds", "excerpt": "run live at CAND in a --shared fleet-mirror clone: exit 0, 'REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)', 242.2 s; census legs 1-2 replayed at pinned blobs (8/10, 8/10, flips=0); tenth leg bash-drift-pins reproduced its committed 2/10 table; runner's only mutate_driver mention is the round-5 manifest comment :755-758 — the replay embeds specs and does not recover the old driver"},
    {"raw": "corpus/README.md round-2 addendum", "file": "corpus/README.md", "ranges": ["10-11"], "verdict": "holds", "excerpt": ":11 'G-R2-1 … the surveyed 79294/357fb245 was an intermediate dirty-tree state never committed' — corrected to the committed 79301 B / 93c5827202b9cdec pin"}
  ],
  "strongest_falsifier": "the section's one runnable instruction executed end-to-end at CAND bytes: bash tools/mutate-and-run.sh --regression in a --shared clone at 6d8c11e with owner repos symlinked (the C2 counter's own regression() recipe) — any leg drifting from its committed table would exit 1 and falsify item 6's 'maintained replay'; observed exit 0, REGRESSION: PASS (cases=10 passed=10), all ten legs matching, 242.2 s",
  "verdict": "holds",
  "deliverable": ".ufo/waves/round-51/w2/@P@Read02.md"
}
```

## 6. Bounds, cleanup, disclosure

- Writes: only this deliverable and its copy `T51W2Read02.md` under `.ufo/waves/round-51/w2/`. Everything
  else read-only (`git show`/`cat-file`/`ls-tree` on committed bytes; ledger and reports read in place).
- Scratch: `/fast/scratch/hyaku/tameshi-r51/T51W2Read02/` (reg fleet-mirror clone + workdirs + outputs),
  deleted before yield; nothing in `/tmp` beyond the runner's own TMPDIR-honouring scratch, which was
  redirected into my scratch and removed with it.
- Git operations: `git clone --shared --no-checkout` + `checkout --detach` inside my scratch clone only
  (toplevel asserted before use); no fixture commit was needed; no mutation in the lane/fleet/sibling repos.
- No tools installed (nothing to record under RULES.md).
- Cross-checked, not trusted: the fixture list's entry for this section (T51ExecRekey.md:105-107) and
  sibling reader T51W2Read16's end-to-end regression — both matched my independent reads.
