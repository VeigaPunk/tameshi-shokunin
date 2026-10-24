# SimplifierReceiptDupes — round-36 record dedup/contradiction sweep (w1, 2026-10-24)

**Verdict line: AGREE on all numbers — zero numeric contradictions across the round-36 record (every census row count, score, slot count, entry count and hash citation re-derives to the same value everywhere it appears); 6 citation-integrity defects found, the worst being a NEW dead pointer of the exact class round 36 repaired (`ResidualSentinelClosure.md`): "the round-36 report" does not exist.**

## What I attacked

The full round-36 record, for duplicated or contradictory statements:

- All 30 files under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/` (`contract.json`; `after/` 13 receipts; `control/` 9 receipts; `coldread/` specs, receipts, affected-sections, 4 traces; `c1/c1-measure-v2.py`; `src/s103-git-hash-object.html`; plus the untracked `c1/__pycache__/c1-measure-v2.cpython-314.pyc`).
- LOG.md round-36 block (`:1898-1942`) with its r35 correction context (`:1880-1897`); SCORECARD.md round-36 block (`:1731-1776`) with r35 context (`:1565-1725`).
- Cross-checks the two blocks cite: `corpus/lessons/round-36.md`, `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-35/` receipts, `.ufo/waves/round-35/residual/`, `.ufo/reports/`.

Revisions in play: before `796e08b888849308d0c4d5e932e56833600a139f` (r35 tip), content/control `e423c41ba253357ab8c8513f0376dad9d38ab248`, refresh/measured `b455001e2589b3f4f471d94a3de7e5e549b9f54c`, mutant (receipts-embedded only) `91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`.

## Contradictions and citation defects (the dedup list)

**C1 — NEW dead pointer: "the round-36 report" (same class as the r35 defect this round repaired).**
- `LOG.md:1919-1920` — refresh commit hash "named in the round-36 report and the `monitor-at-<rev>` receipt filename".
- `SCORECARD.md:1743` — "hash named in the `monitor-at-<rev>.stdout` receipt filename and the round-36 report"; `:1744` — "hash in the `c1v2-at-<rev>.stdout` receipt filename and the report".
- `LOG.md:1939-1941` — the 78 prepared seats are "itemized as prepared-but-undispatched receipts in the round report"; `corpus/lessons/round-36.md` (Wave note) repeats "the round report itemizes the 78 prepared-but-undispatched seats".
- Ground truth: `.ufo/reports/` contains only `round-1/tameshi.md` (glob + `git ls-files .ufo/reports/` → single file; last commit touching the dir is `9939b0e` round 1). No round-36 report exists. The reviewer seat `ReviewC2Claim.md` even quotes a `.ufo/reports/round-36/tameshi.md` that is not in the tree. Until that report lands, the refresh-commit hash `b455001e…` is stated **nowhere** in LOG.md, SCORECARD.md or the lesson (repo-wide grep: zero prose hits; only receipt filenames/`rev`/`rev_input` fields and this wave's own seat reports carry it). This is precisely the defect class QUALITY criterion 72 (added this round per the lesson `## Mistakes`) forbids: an evidence pointer that does not re-resolve.

**C2 — Phantom control receipt name `monitor-at-content-commit.*`.**
- `LOG.md:1918` and `SCORECARD.md:1743` cite `.ufo/evidence/round-36/control/monitor-at-content-commit.*`.
- The committed files are `control/monitor-at-e423c41b.{stdout,exit,stderr}` (their JSON `rev_input`/`revision` = `e423c41b…`, i.e. genuinely the content commit). The literal cited name resolves to nothing, and it breaks the same blocks' stated `monitor-at-<rev>` convention. Same artifact, wrong name — but criterion 72 makes name-level resolution load-bearing.

**C3 — SCORECARD quotes a receipt field that exists in no receipt.**
- `SCORECARD.md:1744` (C2 After cell): "`C1_R36V2: … pub_kill_slots=0 … C1_R36V2_PASS=false`".
- Actual line in `control/v2-at-emptypanel.stdout`: `C1_R36V2: mode=deciding … pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 … C1_R36V2_PASS=false`. The token `pub_kill_slots` is printed by no counter version (v2's print format, `c1-measure-v2.py:548-554`, has no such field). Exit code (`V2_EXIT=1`) and verdict (`false`) do match.

**C4 — Lesson's S103 quote mislabeled and miscounted.**
- `corpus/lessons/round-36.md:36-39`: "Located quote, §DESCRIPTION first sentence … (19 words)".
- Snapshot `.ufo/evidence/round-36/src/s103-git-hash-object.html:1607-1610`: the first sentence is "Computes the object ID value for an object with specified type with the contents of the named file (which can be outside of the work tree), and optionally writes the resulting object into the object database." — 36 words. The lesson quotes only its 18-word prefix and labels it "first sentence"; "19 words" matches neither 18 nor 36. The quoted text itself is verbatim-accurate as far as it goes.

**C5 — "Both receipts kept under `.ufo/evidence/round-36/`" (census) is not true as stated.**
- `corpus/lessons/round-36.md:48-50` and `LOG.md:1936-1937`: round start 99 rows, round end 100 rows, "both receipts kept under `.ufo/evidence/round-36/`".
- Under `round-36/` there is no round-start census receipt: only `after/census-at-b455001e.{stdout,exit}` (round end; itself contains NO row count — just `CENSUS_EXIT=0` and dupes lines) and `after/sources-rows-at-b455001e.txt` (`100`). The 99 figure's only in-round-36 carrier is the embedded monitor field `after/monitor-at-796e08b.stdout:1842` (`"rows": 99`; the r35-dir census receipts likewise print no row counts). Figures are correct; the "both receipts" sentence points at artifacts that don't exist under the named path. (Bonus imprecision in the same sentence: the census stdout files never state a row count, so "validate exit 0, 99/100 rows" pairs an exit receipt with a count carried elsewhere.)

**C6 — The emptied-panel mutant rev `91373d55…` is unresolvable from the lane.**
- Both demonstration receipts embed `rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` (`control/v1-at-emptypanel.stdout`, `control/v2-at-emptypanel.stdout`), and LOG:1926-1929 / SCORECARD:1744 present them as the before-demonstration pair ("the same mutant").
- `91373d55…` is not an object in the lane repo (`git log --all` → `fatal: bad object`); the mutant was committed only in a scratch clone. Neither block says where the mutant state lives or how to reconstruct it (delete the 9 panel JSONs at `b455001e`). The two receipts do agree with each other (same rev, v1 PASS=true / v2 PASS=false), so the pairing itself is sound — but the citation is to a commit the record does not contain.

## Duplicated statements that AGREE (checked, no action)

Every repetition I found is consistent — the record's redundancy is cross-attestation, not drift:

- **Calibration 6 → 8, 60/64 → 64/64**: contract (`before.expected`, `after_target`) = LOG:1911-1912,1920 = SCORECARD:1743,1756-1758 = receipts (score 6/6/8; `sections_covered` 60/60/64 + `sections_total` 64; `credited` 60→64). Single-valued everywhere.
- **6/3/9 frozen targets**: contract `frozen_targets` + `predicate` = `c1-measure-v2.py:68-70` and `:538-541` = LOG:1924-1925 = SCORECARD:1744 = deciding receipt `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9`.
- **Hashes, single-valued record-wide** (all re-hashed from bytes): `9eb8944c…` v2 counter (contract = LOG:1923 = SCORECARD:1736,1744 = actual file); `6188db16…` tally-audit-v3 (v2 `TOOL_SHA256` = lesson:70 = SCORECARD r35 = receipts `tool_sha` = actual file); `a7d3f2dd…` runner (v2 `PIN_RUNNER` = SCORECARD:1566,1701,1755 = depthD receipt = trace-1 input hash = actual file); `dd826dae…` S103 snapshot (contract = LOG:1934 = lesson:34 = actual file, 29,933 bytes as claimed); `f59c9312…` instrument (all 4 receipts' `instrument_sha256` = actual `tools/trace-inputs.py`); `796e08b…` and `e423c41b…` identical across contract/specs/receipts/traces/affected-sections/monitor `rev_input` fields.
- **Census 98→99→100**: LOG r35/r36 + lesson agree with monitor `rows` 99/100/100, `mined` 71→72, tiers `A` 89→90, and `sources-rows-at-b455001e.txt` = 100.
- **Depth 9 → 9**: `depthD-at-b455001e.stdout` (`recorded_cases=9 depth_score=9`) = monitor receipts = SCORECARD:1754-1755; 16 COPY rows = 9 pub (6+3) + 7 sealed (4+3) = SCORECARD's "16/16 verdicts".
- **Ledger 493+4=497**: `refresh-receipts.json` claims = actual `ledger.json` (497 entries; last 4 `read_rev` = `e423c41b…`).
- **Five residual reports** named in the LOG correction (`:1904-1908`) = actual `.ufo/waves/round-35/residual/` contents; `ResidualSentinelClosure*` absent repo-wide (correction claim verified).
- **Four sections**: identical start/end/heading across `refresh-specs.json` (with per-section sha256), `affected-sections.json`, trace argv (131/245, 375/404, 1380/1395, 1436/1448), receipt `section_start`s, and ledger headings.
- **39+39=78 prepared seats**: LOG:1938-1942 = lesson Wave note.
- **Exit codes**: v2 deciding `EXIT=0`, v2 emptypanel `V2_EXIT=1`, v1 emptypanel `V1_EXIT=0`, monitors `EXIT=0`, census `CENSUS_EXIT=0` — all match the blocks' claims.
- **Intentional duplication**: the protocol scope line "L1-author input-keyed source reads only; …" appears 7× in `refresh-receipts.json` plus specs/affected-sections — SCORECARD:1760-1762 explicitly requires it "carried verbatim"; not a defect.

## Deletion candidates (read-only seat; none taken)

- `.ufo/evidence/round-36/c1/__pycache__/c1-measure-v2.cpython-314.pyc` — untracked, git-ignored compiled duplicate of the frozen counter sitting inside the evidence tree (`git ls-files` absent; `git status --porcelain` clean). Not part of the record; safe to remove (round-35 has the same pattern). Candidate only.
- No in-record deletion is safe: the r35-measured `6` vs r36-measured `8` pairing is an append-only supersession chain both sides explicitly declare ("superseded by"); every other repetition is contract↔receipt↔lesson cross-attestation. The next deletion would harm the record's redundancy model — stopping there.

## Exact commands run (all read-only; no lane writes except this report)

```
sha256sum tools/tally-audit-v3.py tools/mutate-and-run.sh \
  .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-36/c1/c1-measure-v2.py \
  .ufo/evidence/round-21/coldread/measure.py tools/trace-inputs.py \
  .ufo/evidence/round-36/src/s103-git-hash-object.html
git ls-files .ufo/evidence/round-36/ ; git status --porcelain .ufo/evidence/round-36/
git ls-files .ufo/reports/ ; git log --oneline -3 -- .ufo/reports/
git log --all --oneline --name-only -1 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f   # bad object
python3 -c "<json probe>": ledger.json entry count (497) + last-4 read_rev (e423c41b…)
git diff --no-index -U0 .ufo/evidence/round-36/after/monitor-at-796e08b.stdout \
  .ufo/evidence/round-36/control/monitor-at-e423c41b.stdout      # 8 lines: reasons, rev fields, rows 99→100, mined 71→72, A 89→90
git diff --no-index -U0 .ufo/evidence/round-36/control/monitor-at-e423c41b.stdout \
  .ufo/evidence/round-36/after/monitor-at-b455001e.stdout        # score 6→8, box3 false→true, missing[]→credited 64
grep -n '"rows"\|"sections_total"\|sections_covered' <3 monitor stdouts>
read: all round-36 evidence files; LOG.md:1880-1942; SCORECARD.md:1565-1776; corpus/lessons/round-36.md;
      s103 html:1603-1614; round-35/after/census-at-round-end.stdout
grep sweeps: 'monitor-at-content-commit|pub_kill_slots'; hash prefixes (dd826dae 9eb8944c f59c9312 6188db16
  a7d3f2dd e423c41b b455001e 796e08b 91373d55 657f009b); 'b455001e' repo-wide; glob ResidualSentinelClosure*
```

Tooling: nothing installed or updated (system `git`, `python3`, `sha256sum`, `grep` only); `pacman` untouched per bounds; no subagents; no monitor/counter re-execution (committed receipts used).

## Tradeoffs

None taken — read-only seat. C1 is the actionable one: either the round-36 report lands at round close (curing LOG:1919/SCORECARD:1743,1744/1941 and the lesson's Wave note), or those pointers are dead-at-commit under the round's own new criterion 72 — the same defect class the round's correction entry was written to close.
