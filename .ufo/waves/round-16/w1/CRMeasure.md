# CRMeasure — round 16 wave 1 — C1+C2 counting command

## Files changed

- `.ufo/evidence/round-16/measure.py` (new, ~545 lines, stdlib only, executable)

## What it does

`python3 .ufo/evidence/round-16/measure.py --rev REV [--repo REPO]` reads blobs
via `git show REV:path` only (never the worktree) and prints one JSON object:

- `recorded_cases` / `depth_score` / `ledger_legs` — count and names from
  `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` (multiline) over
  `tools/mutate-and-run.sh`; `depth_score = min(10, recorded_cases)`.
- `shonen` — box census via `^- \[([x~ ])\] (.*)$`; `marks` preserves file
  order (boxes 1–4 positional); `box3_marked`, `box3_ledger_link`,
  `box3_points` exposed separately.
- `coldread` — SKILL.md sectionized per L1 decision (1): preamble + every
  `^#{1,3}(\s|$)` heading outside ```` ``` ```` fences; section text = heading
  line through the line before the next heading **with trailing blank
  (whitespace-only) lines stripped**, `\n`-joined, no trailing newline; sha256
  over original blob bytes (surrogateescape). Matched by sha256 against
  `.ufo/evidence/round-16/coldread/ledger.json` at REV.
- **Credit rule per L1 decision (2)**, `entry_credit_reason()`
  (`measure.py:162`): hard fail on `blocking_gaps>0`,
  `wrong_expectations>0`, or verdict ∈ {gap-blocking, wrong-expectation,
  not-executed} (unknown/missing verdicts also fail); class `instruction`
  credits only on `executed-ok|gap-minor` with `commands_executed_count>0`;
  class `record` credits only on `verified-record|gap-minor`; anything else
  reports a named reason (`verdict:`, `blocking-gaps:`, `wrong-expectations:`,
  `verdict-class:`, `commands-executed-count:`, `class:`, `malformed-entry`,
  `no-ledger-entry`, `no-ledger`, `invalid-ledger`).
- `box3_full_page` = every section sha256 covered; report carries
  `sections_covered`/`sections_total`, `missing` (start/heading/reason) and
  `uncovered_headings` (L1 decision 4).
- `calibration_restraint_score` = `2·count(boxes 1,2,4 == '~') + 2·(box3 ==
  '~' and box3_full_page and the SHONEN box-3 line at REV contains
  `.ufo/evidence/round-16/coldread/ledger.json`)` — L1 decision (3).
- `sources` — `corpus/SOURCES.md` census: rows matching
  `^\|\s*S[0-9]{3,}\s*\|`, `malformed` = `len(line.split('|')) != 13` (exactly
  the census v2 awk `-F'|' NF!=13` rule,
  `.ufo/evidence/kaika-round-1/sources-census-v2.sh:11`), tier/status
  histograms from awk fields $5/$9 over NF==13 rows.

Exit map: 0 ok · 2 rev unresolvable (`rev-parse --verify --quiet
REV^{commit}`), repo missing, or a required blob (mutate-and-run.sh,
SHONEN.md, SKILL.md, SOURCES.md) absent — error JSON on stdout · 64 usage
(missing `--rev`, unknown arg). Missing/invalid ledger.json is a measured
state (`ledger_present:false` / `ledger_error`), not a tool failure.

`--selftest` builds a synthetic git repo in `mkdtemp`
(`/tmp/tameshi-r16-CRMeasure-*`; git identity via env, `HOME=tmp`) and asserts
33 literal checks: no-ledger→6 · complete→8 · section-missing→6 ·
gap-blocking→6 · byte-changed-sha→6 · uncredited verdict→6 · **instruction
with `commands_executed_count:0` → no credit** · **instruction class +
`verified-record` verdict → no credit** (misclassified instruction-as-record)
· record + `verified-record` → credited (score 8) · **box-3 line without the
ledger link → `box3_full_page` true but score 6** · exits 0/2/2/2/64/64.
Expected section sha256s hash literal line slices (`SYNTH_SECTIONS` with an
independent `_strip_tail`), not `sectionize` output.

## Evidence

- `python3 .ufo/evidence/round-16/measure.py --selftest` →
  `MEASURE_SELFTEST: 33/33 pass`, exit 0 (scratch
  `/tmp/tameshi-r16-CRMeasure-o3qz5oh1`).
- `python3 .ufo/evidence/round-16/measure.py --rev HEAD` (`28aeef4`) → exit 0:
  `recorded_cases:6 depth_score:6`; legs `js-kimi-census,
  bash-surface-census, bash-tsukuroi-census, bash-mado-verify,
  bash-checklist-run, js-claims-check`; `marks:[~,~,~,~]`;
  `box3_ledger_link:false` (current SHONEN box-3 line has no round-16 ledger
  path); `sections_total:51` (preamble + 50 headings — matches the pinned
  snapshot sha256 `97cf436b…23580`, independently parsed: 50 `#{1,3}`
  headings outside 18 fence lines, no `~~~`, no `####`);
  `calibration_restraint_score:6`; `sources:{rows:49, malformed:0,
  tiers:{A:42,B:5,C:2}, status:{mined:22,queued:24,rejected:3}}`.

## Interface notes for L1 (bounded)

1. **51 buckets on the snapshot**, preamble `heading:""` included — your
   decision (1) confirmed against the pinned snapshot.
2. Hash rule implemented: trailing whitespace-only lines stripped before
   join. If CRLedger's hasher diverges (fence rule, blank-strip, encoding),
   every entry reports `no-ledger-entry`; importing `sectionize` from this
   file is import-safe (`main()` under `__main__`).
3. `commands_executed_count` is required on instruction entries: missing →
   treated as 0 → `commands-executed-count:None` no credit. If the ledger
   schema instead carries `commands_executed:[...]`, say so and I'll derive
   the count — one-line change.
4. Missing-ledger is not exit 2 by design (it's the pre-ledger measured
   state; score collapses to 6 anyway).
5. Re-run after landing: `--rev <commit>`; expect `recorded_cases:7` once the
   `js-round-gate` leg lands and `calibration_restraint_score:8` once the
   ledger is complete and the box-3 line carries the ledger path.

## Risks / blockers

- None blocking. Interface question (3) above is advisory only.
- Tooling: nothing installed; stdlib + host git only.
