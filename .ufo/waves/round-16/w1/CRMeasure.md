# CRMeasure — round 16 wave 1 — C1+C2 counting command

## Files changed

- `.ufo/evidence/round-16/measure.py` (new, 480 lines, stdlib only, executable)

## What it does

`python3 .ufo/evidence/round-16/measure.py --rev REV [--repo REPO]` reads blobs
via `git show REV:path` only (never the worktree) and prints one JSON object:

- `recorded_cases` / `depth_score` / `ledger_legs` — count and names from
  `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` (multiline) over
  `tools/mutate-and-run.sh`; `depth_score = min(10, recorded_cases)`.
- `shonen` — box count and per-mark census via `^- \[([x~ ])\] `; `marks`
  preserves file order so boxes 1–4 are positional.
- `coldread` — SKILL.md sectionized (preamble + every `^#{1,3}(\s|$)` heading
  outside ```` ``` ```` fences; section text = heading line through the line
  before the next heading, `\n`-joined, no trailing newline; bytes hashed via
  surrogateescape so sha256 is over original blob bytes). Matched **by sha256
  only** against `.ufo/evidence/round-16/coldread/ledger.json` at REV.
  `box3_full_page` = every section's sha256 has a ledger entry with that
  sha256, verdict ∈ {executed-ok, verified-record, gap-minor},
  `blocking_gaps == 0`, `wrong_expectations == 0`. Reports
  `sections_covered`/`sections_total`/`missing` (each missing item: start,
  heading, reason: `no-ledger` | `invalid-ledger` | `no-ledger-entry` |
  `verdict:<v>` | `blocking-gaps:<n>` | `wrong-expectations:<n>` |
  `malformed-entry`).
- `calibration_restraint_score` = `2·count(boxes 1,2,4 == '~') +
  2·(box3 == '~' and box3_full_page)`.
- `sources` — `corpus/SOURCES.md` census: rows matching
  `^\|\s*S[0-9]{3,}\s*\|`, `malformed` = `len(line.split('|')) != 13` (exactly
  the census v2 awk `-F'|' NF!=13` rule,
  `.ufo/evidence/kaika-round-1/sources-census-v2.sh:11`), tier histogram from
  field 5 (awk $5) and status histogram from field 9 (awk $9) over NF==13 rows.

Exit map: 0 ok · 2 rev unresolvable (`rev-parse --verify --quiet REV^{commit}`),
repo missing, or any required blob (mutate-and-run.sh, SHONEN.md, SKILL.md,
SOURCES.md) absent — error JSON on stdout. 64 usage (missing `--rev`, unknown
arg — `UsageParser.error` override). Missing/invalid `ledger.json` is **not**
exit 2: it is reported inline (`ledger_present:false` / `ledger_error`) with
`box3_full_page:false` — that is a measured state, not a tool failure.

`--selftest` builds a synthetic git repo in `mkdtemp` under
`/tmp/tameshi-r16-CRMeasure-*` (git user set via env, `HOME=tmp`,
`GIT_CONFIG_NOSYSTEM=1`), commits variants, and asserts literal values:
no-ledger→6, complete→8, missing-section→6, gap-blocking→6, byte-changed
section sha→6, uncredited verdict→6, plus exits 0/2/2/2/64/64 across six
error cases. Expected section sha256s are computed by hashing literal line
slices (`SYNTH_SECTIONS`), not by reusing `sectionize`, so the sectionizer is
checked against an independent expectation.

## Evidence

- `python3 .ufo/evidence/round-16/measure.py --selftest` →
  `MEASURE_SELFTEST: 26/26 pass`, exit 0 (run twice: before and after the
  scratch-prefix fix; both 26/26, exit 0).
- `python3 .ufo/evidence/round-16/measure.py --rev HEAD` → exit 0. Key output
  (HEAD `28aeef4`): `recorded_cases:6 depth_score:6`,
  `ledger_legs:[js-kimi-census, bash-surface-census, bash-tsukuroi-census,
  bash-mado-verify, bash-checklist-run, js-claims-check]`,
  `shonen.marks:[~,~,~,~]`, `calibration_restraint_score:6` (ledger absent →
  `box3_full_page:false`, `sections_total:51`),
  `sources:{rows:49, malformed:0, tiers:{A:42,B:5,C:2},
  status:{mined:22,queued:24,rejected:3}}`.
- Sectionizer cross-checked against the pinned snapshot: `sha256
  .ufo/evidence/round-16/coldread/SKILL.snapshot.md` =
  `97cf436b…23580` (matches claim); independent python parse of the snapshot
  found the same 50 headings outside fences (18 ` ``` ` fence lines, 0 `~~~`,
  no `####` headings), so `sections_total` for that blob = 51 including the
  5-line preamble.

## Interface notes for L1 (bounded)

1. **Preamble is a section** per the ledger schema (`heading:""`), so the
   snapshot has **51 sections, not 50**. `box3_full_page` needs a ledger entry
   for it; if CRLedger omits the preamble, the score can never exceed 6.
2. Matching is sha256-only per spec — `start`/`heading` in entries are not
   cross-checked. If any entry with the section's sha256 is credited, the
   section counts as covered.
3. Fence rule implemented: a line whose **stripped** text starts with ` ``` `
   toggles fence state; `~~~` fences are not tracked (none present). If
   CRLedger's hasher uses a different fence rule, every sha will disagree and
   all sections report `no-ledger-entry` — the cheapest coordination is to
   import `sectionize` from this file (it is import-safe; `main()` is under
   `__main__`).
4. Re-run after L1 lands the ledger and (if pinned) the `js-round-gate` leg:
   `python3 .ufo/evidence/round-16/measure.py --rev <commit>`; expect
   `recorded_cases:7 depth_score:7` and, with a complete credited ledger,
   `calibration_restraint_score:8`.

## Risks / blockers

- None blocking. Residual: if a sibling edits SKILL.md *and* the ledger in
  one commit, coverage is measured at whatever REV is passed — the tool
  reports facts, not freshness.
- Tooling: nothing installed; stdlib + host git only.
