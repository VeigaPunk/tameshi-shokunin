# T48ExecC2Counter — round-48 C2 (freshness) counter and controls

Status: **delivered**. Both deliverables are in this directory; the L1 must copy
`T48ExecC2Counter.measure.py` **byte-exact** to
`.ufo/evidence/round-48/freshness/measure.py` at the counter freeze (the file self-pins on
`SELF_PATH='.ufo/evidence/round-48/freshness/measure.py'`). Nothing else in the lane was
written. No tool was installed or upgraded (no channel touched).

| deliverable | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-48/w1/T48ExecC2Counter.measure.py` | 38473 | `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f` |
| `.ufo/waves/round-48/w1/T48ExecC2Counter.controls.py` | 11633 | `46b8c039e0525b786ee3f97c65949c883b40b9fc4369303600acc824b74106b1` |

Inputs read before writing any code: `brief-c2-counter.md` (full), `contract.json`
`claims.C2` + `amendments` 1-2, the round-47 calibration counter (for git/self-pin and
selftest shape), the round-45 freshness counter (for extraction/gz precedent), round-45
`ledger.json`, `corpus/SOURCES.md` at BASE, `scripts/sources-census.sh`.

## 1. Contract conformance

The frozen statement, `required_phrases`, `predicate_label` and amendments 1-2 are
implemented as written; **no wording was changed and nothing was narrowed**. Field-by-field
mapping (all reads via `git -C LANE show REV:path`; BASE is the constant
`473336d9d789f6081195e7376d17836a24666bc3`):

* **row** — new registry rows = census line shape (`^ {0,3}\| S\d{3,} \|`, 13 `|` fields)
  with id > S264. Exactly one candidate whose teaches cell starts `supersedes T `<U+2014>;
  the ASCII-hyphen form is *not* accepted (own selftest case). Then `opened == 2026-10-26`,
  `status == mined`, and every https URL of T's source cell at BASE ∈ the URL set of R's
  source+anchor cells (amendment 1). The URL set is also what the receipt URL is tested
  against.
* **snapshot** — the single file matching
  `.ufo/evidence/round-48/freshness/sources/T.*` other than `T.receipt.json`; sha256 over
  the **committed bytes**, its first 12 hex must appear in R's anchor cell; `.gz` is
  decompressed for extraction only (hash stays the committed bytes).
* **receipt** — `T.receipt.json` at REV: `url` ∈ R's URL set, `fetched_at` starts
  `2026-10-26`, `http_status` stringifies to `200`, `sha256` equals the snapshot's sha256,
  and the `bytes` key is present (the brief lists it among the receipt's keys; the
  predicate does not require its value, so its value is not tested).
* **quote** — first line in file order of `corpus/lessons/round-48.md` matching amendment 2's
  `^- C2-QUOTE (S\d{3,}) (S\d{3,}): \`([^\`]+)\`` that names T second; its first id must be
  R (`line` otherwise). Quote whitespace-collapsed; `0` words → `empty`, `>25` → `<N>w`;
  otherwise it must be a substring of the snapshot's extracted text.
* **phrases** — every phrase of `required_phrases[T]` occurs in the quote (S093 needs both).
* **entries** — for every path in T's base used-by cell: the file exists at REV, a `source:`
  line among the first 10 lines names R, a `verified-at:` line carries `2026-10-26`; then
  R's used-by cell (comma-split, trimmed, `—` dropped) must equal exactly that path set.
* **live** (default on; `--no-live` replaces `C2_R48_PASS` with `C2_R48_PARTIAL`) — fetch
  the receipt URL (urllib, 60 s, gzip transport decoded), extract, the quote must be there.
  States: `ok` / `skipped` / `unreachable` (fetch raised) / `absent` (no receipt URL, no
  quote, or quote not in the fetched text).
* **census** — SOURCES.md at REV is written under TMPDIR as `corpus/SOURCES.md` and
  `scripts/sources-census.sh validate --file <it>` is run; `census_exit` is its exit code
  (127 if the tool is absent, 2 if the registry is missing at REV).
* **self_pin** — sha256 of the running file vs `git show REV:<SELF_PATH>`.
* Predicate: `C2_R48_PASS=true iff self_pin=1 targets=4 refreshed=4 census_exit=0`, where
  `refreshed` counts targets passing every field (with live `ok`, or `skipped` under
  `--no-live`).

Interpretation choices (all inside the contract's wording, none load-bearing for the four
frozen targets):

1. **Census materialisation.** `validate --file X` resolves `dir = dirname(dirname(X))` and
   its E11 check tests `-e "$dir/$path"` for every used-by path. Written literally with only
   SOURCES.md in the temp tree, E11 would fire for ~124 rows and `census_exit` could never be
   0. The counter therefore also materialises, at the same relative path, every blob that a
   used-by cell of the REV registry names (`git cat-file -t` must be `blob`), so E11 is
   graded **against REV**, not against an empty tree. A used-by path that does not exist at
   REV is still absent from the tree and still fires E11 (own selftest case
   `census_nonzero`). Verified on the real lane: `--rev BASE --no-live` prints
   `census_exit=0`.
2. `row=url` tests *every* https URL of T's base source cell; each of the four targets
   carries exactly one, so this is the contract's singular "T's URL" on the frozen
   population, and is strictly the amendment-1 reading.
3. Checks are graded in printed order and stop at the first failure (later fields print `-`),
   so the failing field names the first failing check, as the brief requires.
4. `snapshot=unreadable` is a defensive branch (a git blob is always readable) and is the one
   branch the selftest cannot construct; every other branch is covered.

Modes: `--lane L --rev R` (deciding), `--no-live` (probe), `--selftest`. No `--only` flag was
added (the brief names none for C2; per-target probes are `--no-live` runs).

## 2. Selftest — 43 cases, fixture git repos under TMPDIR, no network (fetch injected)

Run: `python3 -I .ufo/waves/round-48/w1/T48ExecC2Counter.measure.py --selftest`
(exit 0; 6.9 s; the fixture repo is its own toplevel, every git call names `-C ROOT`, commits
use a throwaway identity **only inside the fixture repo**, and the fixture tree is removed in
a `finally`).

```
SELFTEST 01_positive_all_four: PASS
SELFTEST 02_self_pin_mismatch: PASS
SELFTEST 03_base_only_no_row: PASS
SELFTEST 04_row_none: PASS
SELFTEST 05_row_ambiguous: PASS
SELFTEST 06_row_ascii_hyphen: PASS
SELFTEST 07_row_opened_wrong: PASS
SELFTEST 08_row_status_queued: PASS
SELFTEST 09_row_base_url_absent: PASS
SELFTEST 10_snapshot_absent: PASS
SELFTEST 11_snapshot_ambiguous: PASS
SELFTEST 12_snapshot_sha_mismatch: PASS
SELFTEST 13_snapshot_bad_gzip: PASS
SELFTEST 14_snapshot_gz: PASS
SELFTEST 15_receipt_absent: PASS
SELFTEST 16_receipt_url_outside: PASS
SELFTEST 17_receipt_fetched_at_wrong: PASS
SELFTEST 18_receipt_http_status: PASS
SELFTEST 19_receipt_sha_mismatch: PASS
SELFTEST 20_receipt_bytes_missing: PASS
SELFTEST 21_receipt_json_bad: PASS
SELFTEST 22_quote_noline: PASS
SELFTEST 23_quote_wrong_order: PASS
SELFTEST 24_quote_names_other_row: PASS
SELFTEST 25_quote_no_case_fold: PASS
SELFTEST 26_quote_26_words: PASS
SELFTEST 27_quote_25_words: PASS
SELFTEST 28_quote_script_only: PASS
SELFTEST 29_quote_style_only: PASS
SELFTEST 30_quote_entity_unescape: PASS
SELFTEST 31_quote_whitespace_only: PASS
SELFTEST 32_phrases_missing: PASS
SELFTEST 33_phrases_s093_needs_both: PASS
SELFTEST 34_entry_absent: PASS
SELFTEST 35_entry_source_wrong: PASS
SELFTEST 36_entry_verified_at_wrong: PASS
SELFTEST 37_entry_source_beyond_ten_lines: PASS
SELFTEST 38_entry_usedby_extra: PASS
SELFTEST 39_entry_usedby_empty: PASS
SELFTEST 40_census_nonzero: PASS
SELFTEST 41_live_absent: PASS
SELFTEST 42_live_unreachable: PASS
SELFTEST 43_no_live_partial: PASS
C2_R48_SELFTEST: cases=43 failed=0
```

Coverage argument: every check and every failure branch of §1 is exercised — row
(none/ambiguous/opened/status/url, plus the U+2014 rule), snapshot
(absent/ambiguous/sha/gzip, plus gz extraction), receipt
(absent/json/url-in-set/fetched_at/http_status/sha/bytes), quote (noline/line/empty/26w/absent,
plus the 25-word acceptance bound, script/style dropping, script-only and style-only bodies,
entity unescaping, no case folding, wrong order R/T), phrases (missing, and S093 needing both
`--unshare-all` and `--unshare-cgroup-try`), entries (absent/source/verified-at/usedby, plus a
`source:` line beyond the first 10 lines and both directions of used-by set equality), census
non-zero, live absent/unreachable, `--no-live` never printing `C2_R48_PASS`, self-pin
mismatch, and the positive control (`refreshed=4`, `C2_R48_PASS=true`).

## 3. Controls — CTL_F, CTL_G, CTL_H

Run: `python3 -I .ufo/waves/round-48/w1/T48ExecC2Counter.controls.py --work <scratch>/ctl`
(exit 0). The clone is `git clone -q --shared <lane> <work>/lane`; G and H are commits
detached from BASE in that clone; each control was scored with
`measure.py --lane <clone> --rev <commit> --no-live`. The lane checkout was only read.

```
  F | TARGET S026 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | TARGET S048 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | TARGET S093 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | TARGET S108 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
  F | C2_R48: self_pin=0 targets=4 refreshed=0 census_exit=0 live=off rev=473336d9d789f6081195e7376d17836a24666bc3 C2_R48_PARTIAL=false
CTL_F refreshed=0
  G | TARGET S026 row=S265 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | TARGET S048 row=S266 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | TARGET S093 row=S267 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | TARGET S108 row=S268 snapshot=absent receipt=- quote=- phrases=- entries=- live=skipped NOT
  G | C2_R48: self_pin=1 targets=4 refreshed=0 census_exit=0 live=off rev=f9e8f280ae490805f238e219fe4801fda1fceeab C2_R48_PARTIAL=false
CTL_G refreshed=0
  H | TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
  H | TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=missing entries=ok live=skipped NOT
  H | TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=missing entries=ok live=skipped NOT
  H | TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
  H | C2_R48: self_pin=1 targets=4 refreshed=2 census_exit=0 live=off rev=7e32d9f73578f7f383ffc302217575cd71462186 C2_R48_PARTIAL=false
CTL_H refreshed=2
CONTROLS: F=0 G=0 H=2 expected=F0,G0,H<=2 ok=true
```

Readings: **CTL_F=0** — the base tree has no superseding row at all, so every target is
`row=none` (self_pin=0 because the counter is not committed at BASE, which is what "base tree
unchanged" means). **CTL_G=0** — rows exist and are found (`row=S265..S268`) but point only at
`.ufo/evidence/round-45/freshness/sources/T.raw.gz`, so `snapshot=absent` is the first
failure. **CTL_H=2** — complete rows, receipts and re-labelled round-45 snapshot bytes satisfy
everything structural, and the round-45 ledger quotes fail exactly where the contract predicts:
`S048` lacks `should therefore be prioritised`, `S093` lacks both `--unshare-all` and
`--unshare-cgroup-try`; `S026` (`84%`) and `S108` (`--update_goldens`) pass. H is a control,
not a candidate: its receipts are dated `2026-10-26` by construction so the control isolates
the quote/phrase branch.

The control commits' revs are per-run (commit timestamps); only the refreshed counts are
stable, and those are what the contract fixes.

## 4. Probes (never verdicts)

* `measure.py --lane <lane> --rev 473336d9... --no-live` → all four `row=none`,
  `refreshed=0`, **`census_exit=0`**: the census materialisation passes on the real 124-row
  registry at BASE. This is the check that keeps `census_exit=0` reachable at the content
  revision.
* `measure.py --lane <lane> --rev f1cfaad --no-live` (wave-1 tip) → `refreshed=0`,
  `census_exit=0`, `C2_R48_PARTIAL=false`; with live on (no rows ⇒ no fetch) the same.
* Extraction check against the real round-45 bytes (amendment 2 verbatim): every round-45
  ledger quote is *located* after gz decompression and extraction (S026 15 words, S048 14,
  S093 25, S108 6) — which is why CTL_H fails on phrases and not on location.
* Live smoke test, real network, on the CTL_H commit (4 fetches, 60 s timeout):
  `live=ok` for all four targets — the four URLs answer 200 and still carry their round-45
  quotes. This validates the urllib path and current reachability; it says nothing about the
  round-48 quotes, which are w2's.

## 5. What the w2 executor must satisfy (from the counter's own branches)

1. Exactly one `T.*` file per target besides `T.receipt.json` in
   `.ufo/evidence/round-48/freshness/sources/` — a second `T.*` file makes `snapshot=ambiguous`.
2. The anchor cell must contain the snapshot's sha256 **first 12 hex**; the receipt must repeat
   the full sha256 and carry the `bytes` key.
3. For S093, the GitHub blob URL is T's base URL; the receipt/live URL must be an https URL in
   R's source **or** anchor cell (amendment 1 allows the `raw.githubusercontent.com` fetch URL,
   but it must be written into one of those cells).
4. Gate line at column 0, exactly `- C2-QUOTE <R> <T>: `<quote>`` (em dash in teaches, ASCII
   rules for the line). Quote ≤ 25 words, located verbatim in the extracted text, containing
   every required phrase — for S048 that means the literal `should therefore be prioritised`
   must appear *in the quote*, and S093 needs both `--unshare-all` and `--unshare-cgroup-try`
   in one quote.
5. Entry edits: `source:` among the entry's **first 10 lines** must name R, a `verified-at:`
   line must carry `2026-10-26`, and R's used-by cell must list exactly the base used-by path
   set (no additions).
6. `census_exit=0` at the content revision: the new rows must be census-clean (kind/tier/
   status/opened/recheck enums, unique ids, used-by paths present at REV; duplicate URL+scope
   is exempt when teaches carries `supersedes S...`).

## 6. Bounds, risks, blockers

* Lane checkout: read-only; only the two deliverables (and this report) were written, both
  under `.ufo/waves/round-48/w1/`. No git add/commit/checkout/reset in the lane; all commits
  were made inside scratch clones/fixture repos under
  `/fast/scratch/hyaku/tameshi-r48/T48ExecC2Counter/`, which was deleted before finishing.
  `/home/vgpnk/Projects/shokuknow` was never touched; the fleet repo was never edited.
* Risk (not a blocker): the live branch depends on the four pages still serving the w2 quotes
  at the deciding run; a fetch failure is reported as `unreachable` and never credited, as the
  kill rule requires.
* Risk (not a blocker): `census_exit` is the census tool's exit at run time, so an `opened`
  date after the host's UTC date would surface as E08. All four new rows are opened
  `2026-10-26`, the host date at this run.
* No deviation from the contract wording; the only additions are the census materialisation
  (§1.1) and the empty-quote guard (`quote=empty`, needed because amendment 2's regex accepts a
  whitespace-only quote — phrases would fail it anyway).
