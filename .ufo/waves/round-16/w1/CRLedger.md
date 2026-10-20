# CRLedger — C2 ledger assembly (round 16, wave 1)

## Files changed
- `.ufo/evidence/round-16/coldread/assemble.py` — new, stdlib-only ledger
  assembler (this seat's owned path). ~1050 lines including `--selftest`.

## What it does
- Sections one or two SKILL files (`--skill PATH`, repeatable; default = the
  pinned `SKILL.snapshot.md` next to the script). Sectioning: `#`/`##`/`###`
  heading lines outside fenced code blocks; preamble = lines before the first
  heading (start 1, heading `""`); section sha256 = sha256 of the section's
  lines joined by `\n` **after stripping trailing whitespace-only lines**
  (L1 decision 1). Verified: 51 buckets on the snapshot (50 headings +
  preamble), including the `#`-comment lines inside the Appendix A/B bash
  fences correctly ignored.
- Parses seat reports from glob args (default
  `.ufo/waves/round-16/{w1,w2}/*.md` relative to the script); takes the LAST
  fenced ` ```json ` block per file, which must carry `seat`,
  `skill_sha256`, `sections[]` (`start`, `heading`, `class`, `verdict`).
- Entries keyed by **section sha256** (L1 decision 2): a section identical in
  both SKILL files is one entry; `start`/`end`/`skill_sha256` come from the
  first containing skill and a `positions` array records every
  (skill_sha256, start, end) occurrence. Each report is validated against the
  SKILL file whose sha256 its `skill_sha256` names; a report naming no
  supplied sha is `REJECTED` loudly on stderr (L1 decision 4). Two `--skill`
  files add top-level `skill_pins: {pre, post}` (L1 decision 5).
- Merge rules per entry (L1 decision 2): per-observation downgrade —
  `executed-ok`/`verified-record` with non-empty `minor_gaps` becomes
  `gap-minor`; verdict = strictest in
  `wrong-expectation > gap-blocking > not-executed > gap-minor >
  verified-record > executed-ok`; `class` = `instruction` whenever seats
  disagree (a `class_votes` diagnostic field is added); `blocking_gaps`,
  `wrong_expectations`, `minor_gaps`, `commands_executed_count` are sums of
  the seat lists' lengths; `seats`/`reports` deduped, order-preserved.
- Overrides (`--override FILE`, L1 decision 3): records resolve by `sha256`
  or `start` (+ optional `skill_sha256`; ambiguous `start` across skills is
  an error). Stricter mode requires a verdict strictly stricter than the
  merged one — relaxing a same-sha entry is a hard error. Replace mode
  (`"report": PATH`) re-parses the cited report, requires its
  `skill_sha256` to cover the entry's sha and its `sections[]` to contain
  the entry's start, then replaces verdict/class/gap/command fields from
  that observation. Every applied override is recorded on the entry as
  `override: {mode, reason, merged_verdict, ...}`.
- Heading at `start` must equal the section's heading line (exact), except
  the preamble which tolerates `""` or the file's first line; a mismatch is
  a hard error. Unknown `start` (not a boundary in the report's skill file)
  is a hard error.
- Prints `coverage: N/M sections covered`, a per-entry line, and a missing
  list. Exit 0 = full coverage; 1 = missing sections (partial ledger is
  still written, with `_meta.missing` — deliberate, so a partial run is
  inspectable); 2 = hard errors (heading mismatch, bad override, unreadable
  skill).
- A glob hit with no/malformed ` ```json ` block is a loud `SKIPPED` warning
  on stderr, not fatal — the default glob will catch non-seat `.md` files
  (this report included).

## Evidence
- `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` →
  `SELFTEST: all checks passed`, exit 0. 34 checks covering: section math
  (pre/post skills, shared vs changed shas, fenced `#`, trailing-blank
  strip), two-skill merge (5 entries from 4+4 sections), strictest-merge,
  minor-gaps downgrade, `instruction`-wins class, gap/command sums,
  `skill_pins`, sha-mismatch rejection, non-report skip, coverage exit 1 +
  missing list, heading-mismatch exit 2, relaxing-override exit 2,
  stricter override, replace override, wrong-sha replace exit 2, preamble
  heading tolerance.
- Real snapshot run: `assemble.py --out /tmp/tameshi-r16-crledger/ledger.json`
  → `coverage: 0/51 sections covered`, exit 1, missing list of all 51
  sections (no seat reports exist yet — expected; w2 dir does not exist yet).
- Independent hash re-derivation (inline python, `sed`-equivalent slicing):
  Appendix A section (lines 527–593) sha256 matches `sectionize` output;
  preamble (lines 1–5, line 5 blank → hashed over 1–4) matches; lines
  548–549 (`# write driver` inside a ` ```bash ` fence) produce no spurious
  section.
- `python3 --version` → Python 3.14.8. No tools installed (stdlib only;
  pacman paused, nothing needed).

## Interface decisions I made beyond L1's list
- Override record schema: `[{"sha256"|"start"[+"skill_sha256"], "verdict"?,
  "report"?, "reason"}]`; `verdict` required in stricter mode, optional in
  replace mode (taken from the cited report). Bare list or `{"overrides":
  [...]}` accepted.
- Override on a section with NO entry is an error (replacing/strictening an
  uncovered section is meaningless — coverage should come from reports).
- Partial ledger is written even on exit 1; `_meta` carries
  `reports_loaded`/`reports_rejected`/`reports_skipped`/`missing`/`seats`.
- Section entry `skill_sha256` = sha of the skill supplying the canonical
  (first) position; `positions[]` added when >1 skill contains the sha.

## Risks / blockers
- None blocking. Note for L1: if seats hand a `start` for a *post*-SKILL
  section against a report whose `skill_sha256` is the pre sha (or vice
  versa), the `start`-boundary check will fail loudly — that's intended.
- `seats`/`reports` on entries hold seat names and report paths verbatim;
  no seat-identity verification (cold-read trust model is L1's).

## Recommendation
- L1: run after w1 reports land with
  `python3 .ufo/evidence/round-16/coldread/assemble.py` (defaults cover
  w1+w2 globs and write `coldread/ledger.json`); for wave 2, re-run with
  `--skill .ufo/evidence/round-16/coldread/SKILL.snapshot.md --skill
  SKILL.md` (or whichever post file) and an `--override` file if repairs
  relax or tighten verdicts.
