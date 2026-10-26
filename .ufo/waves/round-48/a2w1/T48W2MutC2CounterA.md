# T48W2MutC2CounterA — mutation audit of the frozen C2 counter against its own `--selftest`

Seat: T48W2MutC2CounterA · round-48 attempt 2, wave a2w1 · 2026-10-26
Attacks: the selftest coverage of the FROZEN C2 counter `.ufo/evidence/round-48/freshness/measure.py` (lane-relative), within the assigned areas — new-row selection (id > S264, census pattern), the `supersedes T —` U+2014 prefix, opened/status cells, the amendment-1 URL-set rule, snapshot discovery/hash/anchor prefix, receipt keys (url in set, fetched_at date, http_status 200, sha256 equality). The counter is not mine; this report proposes no contract or counter change (a surviving mutant is a coverage finding).

## Baseline and method

- Frozen bytes verified: lane counter sha256 `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f` == `freeze-2.json` `counters["freshness/measure.py"].sha256` (byte-identical to the w1 source, per that record).
- Baseline `--selftest` on the pristine scratch copy: `C2_R48_SELFTEST: cases=43 failed=0`, exit 0 (43/43 pass). All mutant verdicts are relative to that passing baseline; no inconclusive results.
- Method: one single-site mutant at a time, applied to a copy under `/fast/scratch/hyaku/tameshi-r48/T48W2MutC2CounterA/` (never the lane file), each run in a fresh temp dir under the seat scratch with `TMPDIR` redirected; `--selftest` only. Verdict rule: SURVIVED iff exit 0 and `cases=43 failed=0`; otherwise KILLED (failing case names or crash recorded). 8-way parallel runs; per-run timeout 900 s.
- 40 mutants executed (39 in the batch + U04 rerun after a harness site-string quoting error — U04's batch entry never ran a mutated copy; the rerun did, result below). Site uniqueness asserted (`count == 1`) for every mutant.
- The only non-`--selftest` invocations were three `--no-live` probes (pristine control + survivors P02/U04) against a throwaway `git clone -q --shared` of the lane checked out at the content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17` inside the scratch dir. Probes are reported verbatim and are never verdicts.

## Results — 40 mutants: 24 KILLED, 16 SURVIVED, 0 inconclusive

`measure.py:LINE` = `.ufo/evidence/round-48/freshness/measure.py:LINE`. "40×" = all non-positive cases fail because the positive tree no longer refreshes (killed via `01_positive_all_four` and dependents).

| ID | Site | Single-site mutation | Selftest result | Verdict |
|----|------|----------------------|-----------------|---------|
| R01 | :97 | `MIN_NEW_ID = 264` → `263` | 43/43 pass | SURVIVED |
| R02 | :97 | → `270` | 40× | KILLED |
| R03 | :216 | `> MIN_NEW_ID` → `>=` | 43/43 pass | SURVIVED |
| R04 | :216 | drop the id filter entirely | 43/43 pass | SURVIVED |
| R05 | :216 | `and` → `or` (id filter alone selects) | 40× (S271 fixture row then matches every target → `row=ambiguous` everywhere) | KILLED |
| C01 | :103 | `^ {0,3}\|` → `^\|` (leading-space allowance dropped) | 43/43 pass | SURVIVED |
| C02 | :148 | `!= 13` → `!= 12` | 40× | KILLED |
| C03 | :147 | drop `c.strip()` in cell split | 40× | KILLED |
| P01 | :215 | prefix EMDASH → ASCII `'-'` | 40× | KILLED |
| P02 | :101 | `EMDASH = '\u2014'` → `'\u2013'` (en dash) | 43/43 pass | SURVIVED |
| P03 | :216 | `startswith(prefix)` → `prefix in teaches` | 43/43 pass | SURVIVED |
| A01 | :219 | `len(cands) > 1` → `> 2` | 1 case: `04_row_ambiguous` | KILLED |
| O01 | :222 | `!=` → `==` | 40× | KILLED |
| O02 | :222 | equality → containment (`OPENED not in opened`) | 43/43 pass | SURVIVED |
| O03 | :224 | status check dropped | 1 case: `08_row_status_queued` | KILLED |
| O04 | :99 | `STATUS = 'mined'` → `'queued'` | 1 case: `08_row_status_queued` | KILLED |
| O05 | :98 | `OPENED` → `'2026-10-27'` | 40× (killed by the fixture receipt's hardcoded literal timestamp, not by any row cell) | KILLED |
| U01 | :226 | base-URL subset check dropped | 1 case: `09_row_base_url_absent` | KILLED |
| U02 | :208 | base URLs read from `anchor` cell instead of `source` | 1 case: `09_row_base_url_absent` | KILLED |
| U03 | :153 | row URL set from `cells[2]` only (amendment-1 set narrowed to source) | 43/43 pass | SURVIVED |
| U04 | :104 | URL token stops widened `[^\s|,;)\]"\']+` → `[^\s|]+` | 43/43 pass (rerun; batch entry was a harness site-string error, never executed) | SURVIVED |
| U05 | :274 | receipt url membership vs source-only set | 43/43 pass | SURVIVED |
| S01 | :235 | drop `base.endswith(RECEIPT_SUFFIX)` exclusion | 40× (receipt file becomes a second snapshot candidate) | KILLED |
| S02 | :237 | `split('.', 1)[0]` → `rsplit('.', 1)[0]` | 40× | KILLED |
| S03 | :252 | anchor prefix `[:12]` → `[:8]` | 43/43 pass | SURVIVED |
| S04 | :252 | anchor lookup in `source` cell instead of `anchor` | 40× | KILLED |
| S05 | :255 | `.gz` branch disabled | 2 cases: `13_snapshot_bad_gzip`, `14_snapshot_gz` | KILLED |
| S06 | :258 | `except OSError:` → `except EOFError:` | crash — `gzip.BadGzipFile` escapes `13_snapshot_bad_gzip`, exit 1 | KILLED |
| K01 | :274 | receipt url check dropped | 1 case: `16_receipt_url_outside` | KILLED |
| K02 | :276 | `startswith(OPENED)` → `== OPENED` | 40× | KILLED |
| K03 | :276 | prefix → containment (`find >= 0`) | 43/43 pass | SURVIVED |
| K04 | :276 | `data.get('fetched_at', '')` → `get('fetched_at', OPENED)` | 43/43 pass | SURVIVED |
| K05 | :278 | `!= '200'` → `!= 200` | 40× (str/int always unequal) | KILLED |
| K06 | :278 | http_status check dropped | 1 case: `19_receipt_http_status` | KILLED |
| K07 | :278 | `data.get('http_status')` → `get('http_status', 200)` | 43/43 pass | SURVIVED |
| K08 | :280 | sha256 equality → first-12-hex equality | 43/43 pass | SURVIVED |
| K09 | :280 | `data.get('sha256', '')` → `get('sha256', digest)` | 43/43 pass | SURVIVED |
| K10 | :280 | equality → truthiness (`not sha`) | 1 case: `20_receipt_sha_mismatch` | KILLED |
| K11 | :282 | `bytes` presence check dropped | 1 case: `21_receipt_bytes_missing` | KILLED |

Every KILLED verdict was produced by the selftest alone; the killing-case names above are the actual failing case IDs from the runs (broad "40×" failures are the positive tree collapsing, the named single cases are the targeted detectors).

## The 16 survivors — killing cases and verdict-flip analysis

Committed-row facts used below, all read at the content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17` (`corpus/SOURCES.md`, `corpus/lessons/round-48.md`, `.ufo/evidence/round-48/freshness/sources/T.receipt.json`):

- Rows S265–S268: indent 0, teaches opens `supersedes Snnn ` + U+2014 (codepoint verified), opened `2026-10-26`, status `mined`.
- Every receipt URL sits in the row's **source** cell; no anchor cell carries any URL. S267's source cell additionally holds the raw URL immediately followed by `)`: `…blob/v0.13.1/bwrap.xml (the tag's raw XML bytes at https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml)`.
- Anchor cells carry the full 12-hex digest (S267's anchor also carries unrelated commit-hex tokens: `362936aea0d5 c6e70f7af75d 2d44b5a914cb` before `2cb77df2f4be`).
- Receipts: `fetched_at` 2026-10-26T08:40–08:41Z, `http_status` 200, full 64-hex `sha256`, `bytes` present.
- Gate lines S265→S026 (15 w), S266→S048 (21 w), S267→S093 (25 w), S268→S108 (6 w).

### Survivors that flip the deciding verdict on the committed rows (both false-negative direction — a correct tree scored false)

**P02 (en dash accepted, U+2014 rejected)** — `measure.py:101`. Killing case: a compliant row whose teaches cell opens `supersedes T ` + U+2014 (i.e. exactly the frozen predicate) is rejected with `row=none`; conversely a U+2013 row is accepted. Selftest blind spot: the fixture rows and the check both derive from `EMDASH`, so no case ever pins the three bytes of U+2014 (`STATUS='mined'` escapes the same trap only because case `08` hardcodes the literal `queued`; `OPENED` because the receipt fixture hardcodes its timestamp). Probe at `c7586b9a` (`--no-live`, scratch clone):

```
TARGET S026 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
TARGET S048 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
TARGET S093 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
TARGET S108 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
C2_R48: self_pin=0 targets=4 refreshed=0 census_exit=0 live=off rev=c7586b9a… C2_R48_PARTIAL=false
```

→ refreshed 4 → 0: **flips `C2_R48_PASS` to false on the committed rows.**

**U04 (URL token stops widened)** — `measure.py:104`. Killing case: any URL followed by `)`/`,`/`;`/quote in a source or anchor cell ingests the punctuation into the token, so a receipt URL written adjacently to punctuation no longer matches the row's URL set. The committed S267 source cell ends its parenthetical with `…v0.13.1/bwrap.xml)` — exactly that shape. Probe at `c7586b9a` (`--no-live`, scratch clone):

```
TARGET S093 row=S267 snapshot=ok receipt=url quote=ok phrases=ok entries=ok live=skipped NOT
C2_R48: self_pin=0 targets=4 refreshed=3 census_exit=0 live=off rev=c7586b9a… C2_R48_PARTIAL=false
```

(S026/S048/S108 still REFRESHED.) → refreshed 4 → 3: **flips `C2_R48_PASS` to false on the committed rows.** The selftest has no punctuation-adjacent URL anywhere, and no case where the receipt URL differs in form from the row cell URL.

### Survivors that cannot flip today's verdict (committed rows satisfy the stricter form) but are acceptance-weakening — what they would let past

| ID | Killing case (mutated counter accepts what the predicate forbids) | Why no flip on committed rows |
|----|-------------------------------------------------------------------|-------------------------------|
| R01/R03 (:97/:216) | a superseding row with id exactly **S264** (boundary, `>` → `>=`/`263`) is selected | committed ids S265–S268 are above S264 either way |
| R04 (:216) | a prefixed row with any id (e.g. `S030`) is selected — the "id above S264" clause is unenforced | all committed prefixed rows have ids > 264 |
| P03 (:216) | a teaches cell merely *containing* `supersedes T —` mid-cell (not opening) is selected | committed cells open with the prefix |
| C01 (:103) | a census-shape row indented 1–3 spaces (census-legal per the counter's own docstring) is invisible → `row=none` on a compliant tree | committed rows have indent 0 |
| O02 (:222) | opened cell `2026-10-26 (backdated from 2026-10-19)` passes | committed cells are exactly `2026-10-26` |
| U03/U05 (:153/:274) | the amendment-1 URL set narrowed to source-only: a receipt URL present only in the anchor cell → `receipt=url` on a compliant tree (false negative) | all four committed receipt URLs are also in the source cell |
| S03 (:252) | an anchor cell carrying only an 8-hex (32-bit) prefix binds the snapshot | committed anchors carry the full 12-hex |
| K03 (:276) | `fetched_at` merely *containing* `2026-10-26` anywhere passes | committed values start with the date |
| K04/K07/K09 (:276/:278/:280) | a receipt **missing** `fetched_at` / `http_status` / `sha256` passes (missing key defaults to the passing value) | committed receipts carry all keys |
| K08 (:280) | receipt `sha256` equal only in the first 12 hex (48-bit) passes | committed receipts carry the full digest |

No survivor loosens acceptance in a way that changes today's committed outcome: the pristine control probe at `c7586b9a` prints `self_pin=1 targets=4 refreshed=4 census_exit=0 … C2_R48_PARTIAL=true`, and every acceptance-weakening mutant would still score the committed rows 4/4.

### Structural selftest gaps (root causes, actionable as fixture additions only)

1. **Shared-constant blind spot** — fixture rows/receipts derive expected bytes from the same module constants the checks compare (`EMDASH` always; `OPENED` and `STATUS` partially). One positive case should pin the literal bytes (`—` U+2014, `mined`, `2026-10-26`) spelled out.
2. **Receipt-key drop gap** — only `bytes` has a missing-key case (`21_receipt_bytes_missing`); `url`, `fetched_at`, `http_status`, `sha256` have none, so default-to-pass mutants K04/K07/K09 survive (K08 rides the same line).
3. **Fixture/committed divergence on the URL rule** — fixture URLs never sit next to tokenizer punctuation, and fixture source/anchor cells always repeat the same URL, so amendment 1 is exercised only degenerately. The committed tree depends on `)` being a token stop (U04 flips) and currently on source-cell repetition (U03/U05 stay latent).
4. **Boundary/strength gaps** — no case sits at the S264 id boundary, mid-cell prefix, containment-vs-equality dates, 8-hex anchor or 12-hex receipt sha.

## Restoration evidence

- Lane counter never written: sha256 `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f` before the run (asserted in-harness), after the run (harness print `LANE_UNCHANGED=True`), and re-verified after scratch deletion. `git -C <lane> status --porcelain -- .ufo/evidence/round-48/freshness/` → 0 lines.
- All mutants were applied to copies under the seat scratch; pristine copy hash asserted equal to the frozen hash before every batch.
- The `--no-live` probes ran against a scratch-only shared clone (`toplevel` verified == clone root before use); the lane worktree, its jj state and its git index were never touched; no lane git/jj command beyond read-only `show`/`status`.
- Scratch tree `/fast/scratch/hyaku/tameshi-r48/T48W2MutC2CounterA/` deleted (`SCRATCH_REMOVED` verified); nothing left on disk.

## Tooling record

No tools installed or upgraded (python3 and git preexisting; pacman untouched, per the host-wide pause). Disk-guard checked before the heavy pass: `/fast/scratch/hyaku` 23% used, 621.0G free.
