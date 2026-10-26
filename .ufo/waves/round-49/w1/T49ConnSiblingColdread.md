# T49ConnSiblingColdread — sibling-overlap scan for C1 (calibration)

Seat: T49ConnSiblingColdread (connector, leaf) · Date: 2026-10-26
Lane: tameshi-shokunin, base `8ca67421111fa354b47b803358391d0b07fc6db9`, round-49 contract frozen at `14d03ea`
Scope read: `*-shokunin/{SKILL.md,corpus/QUALITY.md,corpus/lessons/round-*.md}` plus fleet
`kotoba-shokunin/corpus/knowledge/fleet-skill-audit-round5.md`, `kengaku-shokunin/PROVINCE.md`,
`kaidoku-shokunin/.ufo/waves/round-26/w1/SiblingOverlap.md` (format precedent), and tameshi's own
frozen machinery (`.ufo/evidence/round-49/c1/measure.py`, `.ufo/evidence/round-18/measure.py`,
`.ufo/evidence/round-21/coldread/`). Read-only everywhere; nothing installed or upgraded
(system python 3.14.8, git, grep only).

## Axes

- **Calibration (C1)** — primary. Sibling patterns for keeping self-assessment pointers from
  going stale and for re-crediting drifted sections.
- Coverage (C2) — untouched frontier; no sibling overlap claimed against it (one adjacency
  note in §5).

## Commands (all read-only; the one counter invocation is the sanctioned `--list`)

1. `grep -rn -E '@[0-9a-f]{7,40}[:#]' */SKILL.md` — pinned-revision citation forms (fleet).
2. `grep -rln -i -E 'cold.?read' */SKILL.md */corpus/QUALITY.md` — cold-read protocol holders: kake, tabi, tameshi only.
3. `grep -rn -i -E '\bdrift(ed|ing)?\b' --include='SKILL.md' */` — drift handling (chousa gate family dominant).
4. `grep -rn -i -E 'stale (pointer|pin|line)|pointer.*stale|stale.*pointer' */corpus/lessons/` — stale-pointer lessons (chousa, kagi, kaidoku, game-dev-3d).
5. `grep -rn -i -E 're-?credit|laps(ed|ing)' */SKILL.md */corpus/QUALITY.md` — credit-lapse handling.
6. `TMPDIR=$S python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421… --list` (exit 0; receipt `T49ConnSiblingColdread-list-receipt.json` in this directory) — frozen extractor behavior probe on pinned-form text.
7. `grep -n 'handoff-status' kagi-shokunin/SKILL.md` + `sed -n '50,56p'` — drift check of kotoba's round-5 line citations into kagi.
8. `grep -rn -E 'tameshi.*SKILL\.md[:#][0-9L]' */` — fleet files citing tameshi SKILL.md line numbers.

## Patterns: what siblings do

### P1. Read volatile/record files through git blobs at a pinned revision, corroborate byte-identity independently — ADOPT (machinery level; the contract's work plan is sibling-confirmed)

- **kama-shokunin/corpus/QUALITY.md:61 (KQ16)** and **:49 (KQ15)**: a frozen historical copy
  is declared as `git show <pinned-commit>:<source-path>` and corroborated by a *separate*
  `git cat-file blob <pinned-commit>:<source-path>` read, checked against the code-pinned
  revision/path/OID/digest ("capture: git show; comparison: git cat-file blob"). KQ15: corrections
  land as a *new dated snapshot plus its own manifest*, the old frozen receipt stays byte-intact,
  and an erratum names it.
- **tameshi's own round-18 measure** (`.ufo/evidence/round-18/measure.py` docstring): "Reads
  blobs via `git cat-file`/`git show` at an explicit commit only (no worktree access)"; the input
  gate fails `input-drift:<p>` when a recorded sha256 differs from the blob at REV. The round-21
  cold-read refresh machinery (`refresh-specs.json` → `refresh-receipts.json` + `traces/`) is
  section-sha-keyed with per-spec `paths`, `previous_class`, `historical_failures`.
- Rationale quote, **chousa-shokunin/corpus/knowledge/revision-binding-r31.md:17**: "A path alone
  identifies where to look, not which contents were read."
- This is exactly the contract's "record files are read through git blobs, so a later record
  append does not lapse them" — kama KQ15/KQ16 are the fleet-native precedent for it, including
  the two-reader corroboration and the append-only correction shape.

### P2. A standing mechanical audit that counts stale/dangling pointers — ADOPT (verification level); its scan set must cover the files the pointers cite

- **kagi-shokunin/corpus/lessons/round-14.md:162**: `bash corpus/claim-ledger.sh cells` prints
  `CELL_AUDIT: CLEAN (cells=72 … stale_pointers=0 …)` — a per-row stale-pointer counter is a
  first-class audit column, run every round (also round-13.md:120).
- **chousa-shokunin/corpus/lessons/round-51.md:17 (mistake 4)**: "calibration: five
  self-assessment evidence pointers dangle at the base, and no criterion 1–80 requires a
  pointer to resolve" — the same defect class as tameshi's lapsed seven, one lane over. Their
  check's scan set (`stale-count-check.py:18` = QUALITY.md, README.md, LOG.md, round-49.md) had
  **0 hits for SCORECARD.md/SHONEN.md**, so nothing scanned the files the dangling pointers
  lived in. Fix was both: repair the five pointers **and** extend the scan set.
- **kumitate-shokunin/corpus/QUALITY.md:876,883**: pin gates (`source-dupes`, `readme-map`)
  compare live computed sets against `.ufo/pins/*.json`; a resolved group is DRIFT
  `stale-known` / `stale-covered` **until its pin is removed** — never silently refreshed.
- **mado-shokunin/corpus/QUALITY.md:158**: a hardened receipt checker prints `STALE` for
  `SHA_MISMATCH` (stale-ness is a verdict token, not an editing instruction).
- For C1: the round-21 cold-read monitor is tameshi's standing auditor (it scans every SKILL.md
  section, which is the scan-set completeness chousa lacked); `reads.json`'s `base_verdict`
  staleness fields are the per-pointer stale count. Keep both; report `stale_found_at_base` /
  `corrected` per the contract's `reported_not_pass`.

### P3. Re-credit by re-deriving at close — command, not heading presence; superseded text gets a dated erratum, never a silent rewrite — ADOPT (process level)

- **kengaku-shokunin/corpus/QUALITY.md:172 (R12)**: "current-state assertions re-derive at
  close … re-derived by command, not by heading presence; a stale assertion is closed by an
  appended correction that itself re-derives. Check: `python3 plans/state_check.py --summary`
  exits 0." Directly parallels C1's predicate: the *unchanged* round-21 monitor must still
  credit 64/64 after a record append — credit is a re-derivation result, not a heading match.
- **kengaku-shokunin/corpus/QUALITY.md:165 (R5)**: "a superseded premise gets a dated erratum
  naming the receipt and line; the old sentence is not left as current" (check: both greps hit).
- **tabi-shokunin/SKILL.md:1041-1044**: the "Carried-debt closure pointers" table stamps
  statuses "at this append — re-derive at record time"; **:1057** marks a dead pin block
  "(9/9 stale)" rather than repairing it silently; **:1441** names "declared-stale SKILL pins"
  as a first-class column value.
- **tsukuroi-shokunin/SKILL.md:1634**: when the record file LOG.md moved (a line was appended
  by the scribe), the errata answers with the *new* pin (md5, wc -l, bytes, mtime) and keeps
  the pre-existing text append-only. Record files move; pins answer, they do not rewrite.
- **chousa-shokunin/corpus/lessons/round-25.md:42 (R25-M6)**: fix for stale restatements was
  "SKILL uses owning-ledger pointer and re-derive command" — cite the ledger plus the command
  that re-derives, not the number.

### P4. Pinned-revision in-text citation forms (`path@rev:lines`, `lane@rev:path`) — AVOID VERBATIM in the seven sections; the frozen extractor cannot see them

- tameshi already uses the form once: **tameshi-shokunin/SKILL.md:929**
  (`tools/mutate-and-run.sh@9f1d3c3:72-109`). Probe with the frozen extractor
  (`--list` at base, receipt `T49ConnSiblingColdread-list-receipt.json`): that token is
  extracted only as a **path pointer** `tools/mutate-and-run.sh` (no ranges; raw drops
  `@9f1d3c3:72-109`). The pinned grammar has no provision in the round-49 extractor
  (`c1/measure.py` docstring lines 30-42: FILE = dir parts + name, then `:` RANGES; no `@`).
  A pointer "corrected" into pinned form would degrade from line-bound to whole-file, change
  kind/count semantics against the FLOORS table, and lose the located-excerpt binding the
  counter checks. Durability must come from the ledger/reads layer (P1), not from prose syntax.
- Sibling holders of the form, for the record: **kake-shokunin/.ufo/waves/round-21/w1/SourceScope.md:54-55**
  (cross-repo anchor fix: add `kimi-shokunin@e737d2e` to the anchor; keep the self-declared
  hash as provenance text only — a *fleet-canonical file* problem, not in-lane pointer repair);
  **tsukuroi-shokunin/SKILL.md:2313** (`mori-shokunin@4f05dd5a:corpus/knowledge/…` sibling-lane pin).
- **kagi-shokunin/corpus/lessons/round-8.md:50-52**: "Same wave caught a stale line ref:
  MODEL_ENDPOINT is script L19, not L17 — four corpus files carried L17 since round 4
  (**line-count-only pins can't catch per-symbol drift**)." Supports C1's stronger binding —
  every reads.json row must carry a located excerpt that really sits at the pointed lines
  (the frozen counter enforces EXCERPT_MIN..MAX occurrence in the pointed text) — but the
  maxim is a rationale, not a fix.

## Sibling ground C1 must not absorb (adjacency)

1. **chousa-shokunin/corpus/knowledge/line-binding-r31.md:42** — its Limits explicitly do
   *not* claim "verification of `## Claims` table pointers (`path:N`) in `verify` mode."
   Chousa's gate deliberately does not verify its own table pointers; C1 is exactly that
   verification. Do not import chousa's scope limits as a reason to narrow C1, and do not
   import its claims-JSONL `"line"`/`"sha256"` record grammar (`:20`, `revision-binding-r31.md:11`)
   into SKILL prose — different contract, different lane.
2. **chousa revision-binding-r31.md:34-36** — content pin, not a commit pin; TOCTOU race
   between hashing and reading. Named limits there; not solved, do not re-claim as solved here.
3. **kaidoku round-26 SiblingOverlap:11** — "Sibling line pointers into kaidoku SCORECARD.md
   sit below the edited section, so they drift if C2 changes that section's line count."
   Second-order warning for C1's own integration: the seven sections sit at SKILL.md
   131-1608, so any line-count change there shifts everything below — including
   **kengaku-shokunin/PROVINCE.md:318-319**, which cites tameshi `SKILL.md:1929` and
   `SKILL.md:1975` (registry rows). C1 cannot edit kengaku; the round report should name the
   impending drift as a reported-not-absorbed adjacency (kengaku re-derives at close per its
   own R12, which is the healthy pattern on their side).
4. **kotoba-shokunin/corpus/knowledge/fleet-skill-audit-round5.md:57** — "kagi L53–54" cited
   `handoff-status.json` bare; kagi-shokunin/SKILL.md:53-54 now holds the credential-triage
   row, and `handoff-status.json` lives at :195/:223/:328 (verified `grep -n`). A live
   demonstration that bare cross-lane line refs rot fastest. tameshi's one external pointer
   (`../PROTOCOL.md:63–68`, skill_line 1469) is the same class; the counter already resolves
   `../X` at the row's `fleet_commit`, which is the correct treatment — do not "fix" it into
   an unpinned in-lane path, and do not add more bare external line refs.
5. **The round-36 refresh shape is a frozen anti-pattern** (contract CTL_J: section-sha-keyed
   entries with latest inputs, records included, no read rows → must print PASS=false).
   tameshi's own `.ufo/evidence/round-21/coldread/refresh-specs.json` shows the native
   refresh discipline; sibling refresh patterns (tabi re-derive-at-record-time, kengaku R12)
   are governance analogues only — the deciding shape is the contract's work plan plus
   reads.json rows, not any sibling's.

## Risks

- If integration "corrects" stale pointers into pinned-revision syntax (P4), the frozen
  extractor will silently re-classify them (demonstrated: receipt in this directory); FLOORS
  count pointers, not bytes, so a kind change can pass floors while losing line binding.
- The kengaku PROVINCE citations at SKILL.md:1929/1975 will drift the moment the seven
  sections' line counts change; unreported, a sibling monitor may flag tameshi for it next round.
- chousa's round-51 lesson shows the failure mode *behind* a green check: a scan set that
  does not include the cited files. tameshi's monitor scans SKILL.md only; the reads seats
  are the coverage for the cited files — wave 2 should treat a cited file nobody read like a
  stale pointer, not a gap to skip.

## Verification

- Every file:line above was opened and read this session; fleet-wide greps are listed in
  Commands with their hit sets.
- The one counter run was `--list` (sanctioned probe), exit 0, against the lane at base
  `8ca67421…`; output copied to
  `.ufo/waves/round-49/w1/T49ConnSiblingColdread-list-receipt.json` (`.stderr` empty).
  It is a probe of extractor behavior, not a verdict on any claim.
- No fixture repos created; scratch `/fast/scratch/hyaku/tameshi-r49/T49ConnSiblingColdread`
  removed at exit. No tools installed or upgraded.

## Summary

1. Siblings confirm the contract's plan: kama KQ15/KQ16 (QUALITY.md:49,61) read record bytes
   via `git show <commit>:path` with independent `git cat-file` corroboration; tameshi's own
   round-18 input gate (`input-drift:<p>`) is the native form. Adopt at the ledger/reads layer.
2. kengaku R12 (QUALITY.md:172) is the re-credit principle: re-derive at close by command,
   not heading presence; R5 (:165) requires dated errata, never silent rewrites.
3. kagi (round-14.md:162) and chousa (round-51.md:17) run standing stale-pointer audits —
   but chousa's scan set missed the files its pointers cited; scan-set completeness is the
   lesson to keep, via reads.json `base_verdict` and wave-2 re-reads.
4. Do NOT adopt siblings' in-text pinned-revision forms (`path@rev:lines`): the frozen round-49
   extractor degrades them to whole-file path pointers (probe receipt in this directory),
   breaking line binding against the FLOORS semantics.
5. Adjacency not to absorb: chousa's line-binding Limits (:42 — no `path:N` verification;
   different claims-JSONL grammar), its content-pin/TOCTOU limits (:34-36), kake/tsukuroi
   cross-repo pins, and kotoba's bare cross-lane line refs (round5 audit :57, drifted — live
   counter-example).
6. Second-order drift: kengaku PROVINCE.md:318-319 cites tameshi SKILL.md:1929/1975, below the
   seven sections; C1's line-count changes will move them — report, don't absorb (kengaku's
   own R12 re-derivation is the healthy receiver).
7. No sibling lane performs C1's verification for tameshi; no C2 overlap claimed.
8. Probe only: `--list` at base (exit 0); deciding runs remain the L1's.
