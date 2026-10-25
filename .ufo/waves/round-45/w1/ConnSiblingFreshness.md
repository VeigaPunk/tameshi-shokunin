seat: ConnSiblingFreshness

# ConnSiblingFreshness — sibling freshness-ledger patterns (round-45 w1)

Axes named (godspeed): **freshness** (judged axis — do sibling lanes re-open SOURCES rows against live bytes, and how does C1 compare), **coverage of sibling evidence** (how many lanes/tools/rounds are examined), **precision/actionability** (every claim file:line-anchored; only patterns that improve an axis without harming another are proposed).

Scope: read-only scan of /home/vgpnk/Projects/shokunin/*-shokunin (sibling lanes) for row-level source re-verification practices. Lane bound: leaf member, no subagent dispatch. No lane or fleet repo was modified; scratch only under /tmp/tameshi-r45-ConnSiblingFreshness/.

## Method (commands run)

- `ls` of `/home/vgpnk/Projects/shokunin` → 20 sibling `*-shokunin` lanes (audio, chousa, game-dev-2d/3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tsukuroi).
- `glob` of `*/tools/*` across lanes; `grep` over `tools/`, `corpus/`, `.ufo/evidence/` for `freshness|reopen|re-open|re-verif|source-drift|snapshot.*sha|digest|quote.*reopen|quote.*verif|ledger|drift`.
- Evidence dirs found (`.ufo/evidence` only in chousa, mado, tsukuroi; counters/snapshots also live under `corpus/evidence/` in chousa/mori/tabi and `.ufo/waves/` in mori/tabi/tsukuroi).
- Full read of the closest sibling freshness tools: mori `count-c1.py` (round-32), mori `mori-source-drift.py`, tabi `measure-c1.mjs` + `recheck-fetch.mjs` (round-18), chousa `quote-reopen.py`, kotodama `reopen-row.py` + `check-row-fragments.py` + `check-gate-quotes.py`, tsukuroi `check-btrfs-space-r30.py` + `check-freshness-r17.py` + `check-review-snapshots.py`, souji `souji-gate-check.py`, kama `citation-provenance.py`, and evidence files (mori `recheck-r32/README.md`, `sources-r30/S156.txt`, `recheck-r33/SHA256SUMS`; tabi receipts; tsukuroi `round-1-kaika/reviewer-quotes.md`; mado `round-12/l2-driftrecord.md`).

## Findings — sibling patterns

### 1. mori-shokunin — closest prior art (round-32 C1: live recheck ledger)
- `mori-shokunin/.ufo/waves/round-32/count-c1.py`: frozen counter over 34 population rows (mutable-URL mined rows at base `641a6e86`). R1: Recheck-table row url==p.url, `accessed` ISO-8601 UTC ≥ 2026-10-23T01:00:00Z, verdict `current|drifted|unreachable` (lines 12-13). R2: sha256==committed copy `corpus/evidence/recheck-r32/<r>.src`; quotes 3-25 words present in normalised copy; quotes together share ≥2 content tokens with `teaches+anchor+scope` (lines 14-17). R3: *counter itself re-fetches live* (`curl -sSL --fail -m 60`, 3 tries) and every quote must appear in normalised live text; unreachable only if all fetch tries fail (lines 18-20). R4: judge receipt `JudgeRecheck.md` must carry `judge-role: reviewer`, `judge-seat: <Name>` appearing as an agent-reviewer task in a committed `*dispatch*.json`, `judged-sha256` == sha256 of the judged `## Recheck` section bytes, and the line `- <r>: agree` (lines 21-23). R5: for drifted rows every `corpus/knowledge/` path in `used_by` must gain a new line naming `<r>` and `Round32` (lines 24-25).
- `mori-shokunin/corpus/evidence/recheck-r32/README.md`: fetch method (curl flags grounded in S175), normalisation (drop script/style, unescape, NFKC, fold quotes/dashes), non-author reviewer against teaches cell, first-URL-only population, tag-pinned URLs excluded, and the rule *“dynamic full-page hashes are fetch identities, not semantic drift”* (byte-dynamic S067 → quote-presence check, not byte equality; S047/S064 false-drift example). Lines 1-29.
- Digest pins: `corpus/evidence/recheck-r33/SHA256SUMS` (11 `.src` files); `corpus/evidence/sources-r30/S156.txt` header `id/url/sha256/accessed/lines` (lines 1-5) with line-window quoting.

### 2. tabi-shokunin — receipt-per-row with body+excerpt digest pins (round-18)
- `tabi-shokunin/.ufo/waves/round-18/measure-c1.mjs`: counts receipts in `corpus/evidence/round-18/source-recheck/<S###>.json`. Validates: schema `tabi-source-recheck-v1`, `rowUrl` ∈ row source cell, `sha256` 64-hex == retained body sha, `quoteWords ≤ 25` and consistent, `quoteFound=true`, `fetchedAt` exactly 2026-10-20, pinned curl command (`-sSL --compressed --max-time 90`), HTTP 200, `producerSha256` pinned, gz body digest/length, quote offset/excerpt blob equality; `teachesVerdict` ∈ held|drift, and **drift requires a superseding row** `teaches.startsWith("supersedes <r> —")` (lines 389-416, 439-486). `liveCheck()` re-fetches during counting only with `--live` (lines 489-548).
- URL canonicalisation / fetch-target identity: `normalizeHttpUrl` (strip hash, trailing slash) plus per-row canonical alternates — GitHub blob → raw.githubusercontent, gitiles → `?format=TEXT`, StackOverflow answer via API identity, IEEE abstract (lines 209-275); `isPinnedUrl` classes immutable_pinned vs living_live (lines 312-317).
- `recheck-fetch.mjs`: one shared fetch/normalise (NFC, typographic folds, whitespace-run collapse) + decoders `none|base64|html-text|pdf-text` (lines 22-54).

### 3. chousa-shokunin — live quote re-open (no digest pin, no review)
- `chousa-shokunin/tools/quote-reopen.py`: items TSV `id/source_id/quote`; fetches registry URL once per run; verdicts `NO_SOURCE|TOO_LONG|UNREACHABLE|VERBATIM|ABSENT` (lines 495-532). `found()` requires token-boundary match of the normalised quote in normalised page text (lines 161-174). Fetch hardening: global-address-only, watchdog deadline, 8 MiB caps, redirect chain policy, gzip inflation cap (lines 212-368). No sha pin, no reviewer, no teaches-overlap check; quote comes from the item file, not the row.
- `corpus/evidence/round45/build-spans.py`: pins `capture_sha256`, `offset`, `span_file`, `quote`, `entry` in `spans.tsv`; each quote must occur exactly once in its capture, else nothing written (lines 41-55).

### 4. kotodama-shokunin — row-anchor quote re-open (reuses the row's own quote)
- `kotodama-shokunin/tools/reopen-row.py`: refetches each row's source URL(s) and locates the row's **own anchor quote**; verdicts `LOCATED|CAPTION_ONLY|ABSENT|TRUNCATED|UNREACHABLE|REFUSED|MALFORMED|NO_QUOTE|NO_ROW` (lines 11-34), body caps/retries/redirect/private-address policies (lines 73-94). No digest pin, no reviewer, and quote reuse is by design — the opposite of C1's fresh-quote-not-copied rule.
- `tools/check-row-fragments.py`: `norm_url` query/fragment-aware identity (host casefold, www. strip, default port, trailing slash) for duplicate URL detection; capture-original must normalize-equal live URL (lines 48-69). `tools/check-gate-quotes.py`: ≤25-word quote runs, ellipsis-join, doubled-locator, truncated-grounds checks (lines 41-63).

### 5. tsukuroi-shokunin — snapshot sha inside the SOURCES row; structured review manifest
- `tools/check-btrfs-space-r30.py` (sourced-row counter): R4 requires the snapshot's sha256 to appear **inside the SOURCES row text itself** (line 316); R5 snapshot is a regular file under `.ufo/waves/round-30/`; R6 quote ≥20 chars, must occur in the cited-line ±2 window and pair `(snapshot sha256, line)` is unique (lines 318-336); R9 SKILL.md marker single-mention + source id (lines 358-367).
- `tools/check-freshness-r17.py`: freshness-recheck JSON records — `baseline_quote` must remain a substring of the baseline file while `notice_heading` appended after baseline; `STALE-UNFLAGGED` reported for every record whose quote is present without the notice (lines 2-26). This is a *doc-level* staleness flag, not row-level.
- `tools/check-review-snapshots.py` + `.ufo/waves/round-21/reviews.json`: review manifest binds `name → report → source file sha256 → predicate` (lines 69-120; JSON lines 1-43) — a structured, digest-pinned review ledger.
- `.ufo/evidence/round-1-kaika/reviewer-quotes.md` line 7 caveat: the reviewer fetched current revisions but did NOT re-verify pinned oldid anchors (S010/S011/S014/S023/S026); verdicts CONFIRMED/WRONG/UNREACHABLE (lines 5-31). `.ufo/evidence/round-1-kaika/sources-quotes.md` lines 1-3, 7-38: quote-per-row ≤25 words, access date 2026-10-19, location (section/commit/line).

### 6. souji-shokunin — verbatim quote in committed snapshot + locator (no live recheck)
- `souji-shokunin/tools/souji-gate-check.py`: Gate entry must name https URL + `opened: <round date>`; quote ≤25 words with locator token; every quoted span appears verbatim (whitespace-collapsed) in the committed snapshot named on the same line and living under `--snapshot-dir`; cited `source: S<digits>` resolve in corpus/SOURCES.md (lines 37-115). Snapshot path discipline, but no sha pin and no live re-fetch.

### 7. Other lanes
- `kama-shokunin/tools/citation-provenance.py`: `cite(<rev>, <path>, sha256=…)` tokens verified by `git cat-file` at rev:path (lines 31-68) — anchors **committed documents**, not live bytes. `tools/kama-probe.sh` snapshot mode keeps UTC ids + predecessor link (per `tools/test-snapshot.sh`).
- `mado-shokunin/.ufo/evidence/round-12/l2-driftrecord.md` lines 3-17: host-side drift flags with SHA pins (old pin vs backup match), line counts, live spot-checks (hyprctl) — config/live-host freshness, not SOURCES rows.

## Comparison with C1 (round-45 freshness measure)

C1 reference: `tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py` — population() (95-97), grade() (132-165), review_sets() (192-215), measure() (218-268), live() (300-322).

**C1 duplicates extant sibling patterns:**
1. ≥2 content-token overlap with scope/anchor/teaches = mori R32 R2 (count-c1.py 16-17) exactly.
2. Snapshot digest pin (raw_sha256) = mori R30 R4 (check-btrfs-space-r30.py 316), tabi receipt sha256 (measure-c1.mjs 406/461), mori SHA256SUMS files.
3. Quote length ≤25 (C1: 6-25) = souji (37-41), mori (15), chousa (509), tabi (409).
4. Verdict trichotomy holds/drifted/unreachable = mori R32 R1 (13).
5. One-entry-per-id uniqueness = mori R32 (R2 exact-one-row), tabi duplicate-receipt reject (394).

**Patterns C1 lacks (gaps vs sibling defenses):**
1. **Live re-fetch in the deciding run.** mori R32 R3 (18-20), chousa quote-reopen (513-524), kotodama reopen-row, tabi `--live` (489-548) all fetch during measurement. C1's `measure()` never opens the network; `--live` is separate and informational (measure.py 300-322, docstring 38-39). C1 trusts the committed snapshot blob + `opened` date, so a snapshot fetched once on 2026-10-25 and committed unchanged satisfies the predicate even if the live page drifted afterward. Not a defect for reproducibility (network in deciding run would harm determinism), but a genuine freshness gap versus mori R32.
2. **Structured non-author reviewer attestation.** mori R32 R4 (21-23) binds judge-role + judge-seat to a committed dispatch JSON and pins `judged-sha256` of the judged section. C1's review_sets (192-215) only requires report text to name id+reviewer and the reviewer to be a seat with non-empty w2 output — weaker: an agreeing seat can mention the row in prose without an explicit verdict line; no digest pins the judged artifacts.
3. **Drift side-effects on knowledge.** mori R32 R5 (24-25) requires every `used_by` knowledge path to gain a dated `Round32` notice on drift; tabi requires a superseding row (413-416). C1 flags `drifted` (stats/exit) but does not force any stale-claim update in referenced entries — stale cites remain live.
4. **URL canonicalisation / fetch-target identity.** tabi (209-275), kotodama norm_url (48-69) normalize scheme/www/trailing-slash/query/fragment and allow canonical alternates. C1 uses exact string equality of the first http(s) URL (grade 137-138; population 95-97). Strict (no aliasing), but blind to legitimate mirrors/redirects → false invalid possible. (ConnPackageCross's staged-vs-lane matching uses modulo scheme/www/trailing-slash — a hint C1's exactness is intentionally stricter.)
5. **Caption/head filtering.** kotodama distinguishes `CAPTION_ONLY` (13-16); chousa drops head/title and restricts content types (66-73). C1 strips only script/style then tags (121-124); title/nav/caption text is kept, so a quote matching boilerplate could pass.
6. **Decoder/caps coverage.** tabi adds base64 (gitiles) (22-24); kotodama gzip-inflation cap (92-94); chousa 8 MiB cap (54). C1 handles gz/tar/pdf/html (109-125) but no base64 and no explicit byte cap.
7. **Date strictness.** mori R32 requires ISO-8601 UTC format (13); C1 compares `opened` lexicographically ≥ '2026-10-25' (139-140) — non-ISO strings ≥ that literal would pass.

**Population difference:** mori R32 excludes tag-pinned URLs (README 17-18; `isPinnedUrl` tabi 312-317). C1 includes every mined row ≤S160 with an http(s) URL, pinned or not (95-97) — broader, but "freshness" is less meaningful for pinned/immutable URLs (echoes tsukuroi reviewer caveat: pinned oldid anchors not re-verified, reviewer-quotes.md:7).

## Proposed non-obvious move (future round, not touching frozen C1)

Adopt mori R32 R5 + tabi drift-supersede as a **companion drift-propagation ledger** for C1: when an entry grades `drifted`, every `corpus/knowledge/` path in the row's `used_by` must gain a dated notice naming the row and `Round45` (mirroring tsukuroi check-freshness-r17's STALE-UNFLAGGED mechanism + mori R5). This improves freshness accountability (drift now forces stale-claim updates) and harms none (no change to C1's counts; only invariant additions after drift). Secondary, non-breaking hardening proposals for C1-style counters: (a) require the reviewer report to carry an explicit `- <r>: agree/dispute` line (mori R4 shape) instead of prose mention; (b) add ISO-8601 validation for `opened`; (c) treat caption-only matches as non-verified (kotodama CAPTION_ONLY).

## Verification

- All reads were committed blobs/worktree files; no mutation of any lane. No git/jj writes. Scratch lives in `/tmp/tameshi-r45-ConnSiblingFreshness/` (scripts: search_lanes.py, fast_scan.py, find_counters.py, list_rounds.py, list_ufo.py, scan_focus.py — all read-only).
- Claims above are anchored to the file:line references given; line numbers are from the exact files read this session.
- Not run: any C1 counter measurement (seats may not decide); sibling counters were only read.
