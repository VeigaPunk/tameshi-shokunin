# T48A2RevC2Predicate — C2 predicate: contract vs frozen counter

Seat: tameshi round 48 attempt 2, wave a2w1. Scope: review the frozen C2 counter
`.ufo/evidence/round-48/freshness/measure.py` against `contract.json` C2 `statement`,
`required_phrases`, `predicate_label`, `kill_rule` and amendments 1–2; one finding per
conjunct that has no check or a check stricter/looser than the sentence.

Inputs verified before review:
- counter sha256 `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f` ==
  `freeze-2.json` counters.freshness/measure.py (`changes: none (byte-identical)`).
- contract sha256 `4fff75dbaac728992fa04ffd3ccfea6ace8ca80b944cc393b63c287fadc6d59e` ==
  `freeze-2.json` contract_sha256.
- BASE pinned in code at measure.py:84 = `473336d9d789f6081195e7376d17836a24666bc3`.

Method: sentence-by-sentence mapping of the amended C2 statement to code lines (read-only),
plus two permitted probes whose stdout is reported as observed — a probe is never a verdict:
- `TMPDIR=$S python3 .ufo/evidence/round-48/freshness/measure.py --lane . --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 --no-live`
- `TMPDIR=$S python3 .ufo/evidence/round-48/freshness/measure.py --selftest`
Both ran with TMPDIR under `/fast/scratch/hyaku/tameshi-r48/T48A2RevC2Predicate/` (since
deleted). No tools installed; no pacman transactions; lane untouched (reads only).

## Observed probe output (CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`, --no-live)

```
TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=off rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C2_R48_PARTIAL=true
probe_exit=0
```

Selftest rerun: `C2_R48_SELFTEST: cases=43 failed=0`, exit 0 — matches the frozen record in
`freeze-2.json`.

## Conjunct → code map (all line refs `.ufo/evidence/round-48/freshness/measure.py`)

| # | Conjunct (amended sentence) | Code | Verdict |
|---|---|---|---|
| 1 | target set {S026,S048,S093,S108} | :85 `TARGETS`, iterated :408 | conform |
| 2 | exactly one new row R, id above S264 | :213-221 (`cands` filter :214-216 `int(id[1:]) > 264` (:97), `len(cands) > 1 → ambiguous` :219) | conform (numeric compare, so S1000+ also handled) |
| 3 | teaches opens `supersedes T —` | :214 prefix `'supersedes %s %s' % (t, EMDASH)` with `EMDASH='\u2014'` (:101) | conform; ASCII hyphen rejected (selftest `row_ascii_hyphen`) |
| 4 | opened 2026-10-26 | :222-223 exact equality vs `OPENED` (:98) | conform |
| 5 | status mined | :224-225 exact equality vs `STATUS` (:99) | conform |
| 6 | source URL set (amendment 1) | :152 `urls_of(cells[2]+' '+cells[6])` (source+anchor, regex :104); T's base source URLs ⊆ R's set checked :226-227 | conform-with-note (F5) |
| 7 | receipt url in R's URL set (amendment 1 replaces "equal to R's URL") | :274-275 `data['url'] not in set(row['urls'])` | conform |
| 8 | committed snapshot `T.*`, sha256 12-hex prefix in anchor | :231-239 `snapshot_files` (ls-tree at REV, receipt excluded :235); :241-247 absent/ambiguous; :253-256 `digest[:12] not in row['anchor']` | conform ("committed" holds: everything read via `git show REV:` :119-121) |
| 9 | receipt fetched_at on 2026-10-26 | :276-277 `startswith(OPENED)` | conform (accepts ISO datetime; date-part reading) |
| 10 | receipt http_status 200 | :278-279 | conform |
| 11 | receipt sha256 == snapshot's | :280-281 full-digest equality vs committed bytes | conform |
| 12 | — (not in sentence) | :282-283 requires a `bytes` key | **stricter — finding F1** |
| 13 | Gate line grammar (amendment 2: R first, T second, quoted) | :105 `GATE_RE = ^- C2-QUOTE (S\d{3,}) (S\d{3,}): \`([^\`]+)\``; :287-289 over `corpus/lessons/round-48.md` at REV (:93); :292-298 requires T second and R's id first (`line` otherwise, `noline` if none) | conform |
| 14 | quote ≤ 25 words (whitespace tokens) | :299-304 `len(quote.split())`, `MAX_WORDS=25` (:100); 0-token quote → `empty` (verdict-equivalent: phrases would fail anyway) | conform |
| 15 | located in snapshot's extracted text (amendment 2 pipeline, no folding) | :170-176 `extract`: UTF-8 decode → drop `<script>/<style>` element contents → strip tags → `html.unescape` → collapse; located :305-306 case-sensitive substring | conform-with-note (F6) |
| 16 | quote contains T's required phrase(s) | :86-91 `REQUIRED` == contract `required_phrases` verbatim (all four, incl. both S093 flags); :310-316 collapse-substring in the quote | conform |
| 17 | every base used-by entry cites R in `source:` + `verified-at: 2026-10-26` | :318-333; base used-by from BASE row :209; entry read at REV :320-322 | conform-with-note (F2) |
| 18 | R's used-by cell lists exactly those entries | :331-333 set equality | conform |
| 19 | live fetch of the URL contains the quote (extracted text) | :336-350; fetches the receipt URL (already ∈ set via #7, so amendment 1's live-fetch clause holds); non-200/exception → `unreachable` → not refreshed | conform |
| 20 | refreshed counts targets meeting all | :424-433 all-fields conjunction | conform |
| 21 | census error (exit != 0) is a miss | :379-395 runs `sources-census.sh validate --file <materialized>`; exit folded into verdict :441-442; tool absent → 127 never credited :380-381; registry missing at REV → 2 :385-386 | conform |
| 22 | predicate label self_pin=1 targets=4 refreshed=4 census_exit=0 | :400-402 self_pin (running bytes == REV blob), :441-452 verdict + `C2_R48_PASS` only in live mode; `--no-live` prints `C2_R48_PARTIAL` (:443-446) — a probe can never emit PASS | conform |
| 23 | counter CLI `--lane --rev [--no-live] (--selftest)` | :845-858 | conform |

## Findings

### F1 (low, stricter than the sentence) — receipt must also carry a `bytes` key
`measure.py:282-283`: `if 'bytes' not in data: return data, 'bytes'`. The contract sentence
lists exactly url, fetched_at, http_status, sha256; no `bytes` requirement. A receipt that
satisfies the contract but omits `bytes` fails the counter (false negative only — it cannot
inflate `refreshed`). The restriction is deliberate and frozen: selftest case
`receipt_bytes_missing` (measure.py:718-719) asserts it. Vacuous at CONTENT: all four
committed receipts carry `bytes` (probe `receipt=ok` ×4 above). Show:
`awk 'NR>=280 && NR<=284' .ufo/evidence/round-48/freshness/measure.py`.

### F2 (low, stricter than the sentence) — `source:` line only recognized in the first 10 lines
`measure.py:325`: `lines[:10]` bounds the `source:` search, while `verified-at:` is searched
over all lines (:327-330) — an asymmetric restriction the contract does not state ("cites R
in its `source:` line"). An entry whose `source:` line sits at line 11+ fails `entries=source`
while satisfying the contract. Selftest `entry_source_beyond_ten_lines` (:771-772) asserts the
restriction. Vacuous at CONTENT: all four base used-by entries carry `source:` on line 1 and
`verified-at:` on line 2 (e.g. `git -C . show c7586b9a:corpus/knowledge/regression-tally-completeness.md | grep -n '^\(source\|verified-at\):'` → 1:, 2:).

### F3 (low, selftest-fidelity defect in the frozen counter) — duplicate dict keys silence four field assertions
Python dict literals keep the last duplicate key, so in four selftest cases the first
`expect_lines` needle is dead code: `quote_25_words` (:736-738, `'quote=ok'` dropped),
`live_absent` (:789-790, `'live=absent'` dropped), `live_unreachable` (:791-792,
`'live=unreachable'` dropped), `no_live_partial` (:793-795, `'live=skipped'` dropped). The
load-bearing summary assertions survive (`refreshed=0` for live failures, `refreshed=4` +
`C2_R48_PARTIAL=true` + forbidden `C2_R48_PASS=` for the probe case), so kill-power on the
frozen outcomes remains; but the printed PASS overstates per-field coverage. Show:
`grep -n "'S026': 'live=absent', 'S026'" .ufo/evidence/round-48/freshness/measure.py`.

### F4 (info, robustness) — census hang crashes instead of missing; empty live body mislabeled
`measure.py:390` `subprocess.run(..., timeout=900)` — a census hang raises uncaught
`TimeoutExpired`: the counter dies without any `C2_R48*` label, and the kill_rule only gives
semantics to `exit != 0`. The deciding run would then lack a C2 receipt entirely. Cosmetic
sibling: an empty 200-response body is labeled `unreachable` (:348-349) where `absent` would
be exact; no verdict effect either way.

### F5 (info, disclosed equivalence) — base-URL subset vs amendment-1 membership
`measure.py:226-227` requires *every* https URL of T's BASE source cell to be in R's URL set;
amendment 1 says "T's base URL must be in that set". Equivalent on the frozen domain: each of
the four base source cells carries exactly one URL (verified on
`git show 473336d9:corpus/SOURCES.md`); the docstring (:42-44) discloses exactly this. No
defect; would become over-strict only for a hypothetical multi-URL base row.

### F6 (info, interpretation) — strip-tags replaces each tag with a space
`measure.py:173` substitutes `' '` for every tag before collapse; amendment 2 says "strip
tags" without naming the replacement. Space-insertion cannot merge tokens across inline tags
(the `''` variant could fabricate locatedness), so it is the conservative reading; all four
CONTENT quotes locate (probe `quote=ok` ×4). No defect.

## Residual risk / verification gaps
- The live-fetch path (:128-138, :336-350) was reviewed as code only; my probe ran `--no-live`
  (by seat rule). The deciding run's live outcome (incl. network reachability of the four
  receipt URLs) is the L1's to observe; nothing in the counter credits a failed fetch.
- Census sandbox fidelity: verified by reading `scripts/sources-census.sh` — with `--file`,
  `resolve_targets` sets dir to `dirname(file)/..` (:497-503) and E11 resolves used-by paths
  against that dir (:546-570), which is exactly what `_materialise` (:353-376) fills from REV
  blobs; text checks (E01-E10, E12) run on the same REV bytes. Census `TODAY` defaults to the
  real date, so rows opened 2026-10-26 pass E08 at the deciding run. A census run on the real
  lane could only differ through files the census never reads in `--file` mode.
- Rows outside `## Registry` or with wrong field counts are skipped by `parse_rows` (:141-153)
  but census E01/E12 fires on the same text, so the `census_exit=0` conjunct closes that hole;
  no laundering path found.

Bottom line: every contract conjunct of C2 has a check; no conjunct is missing; no check is
looser than the amended sentence. Findings F1-F2 are strictly-narrower checks (false-negative
direction only, both vacuous on the CONTENT tree), F3 is a selftest assertion-fidelity defect
in the frozen counter, F4-F6 are robustness/interpretation notes.

Scratch dir `/fast/scratch/hyaku/tameshi-r48/T48A2RevC2Predicate/` deleted. No tooling
installed (none needed); pacman untouched; lane repo untouched except this report file.
