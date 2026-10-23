# Cold-read re-crediting: `corpus/SOURCES.md` rows S097–S101

Seat: `tameshi-r34-w1-ColdReadSourcesRows` (round 34, wave 1). Verified against the
lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. All scratch work in
`/fast/scratch/hyaku/tameshi-r34-seats/ColdReadSourcesRows/`; the lane was not
written to. No tools were installed or updated (nothing needed beyond stock
`git`/`curl`/`sha256sum`/`awk`); the pinned tool and runner were hash-verified
byte-exactly and never executed.

**Verdict: rows S097, S099, S100, S101 re-credited.** Id order clean, every
mentioned digest verified (against the row's own anchor live, or a committed
snapshot, or both), S101's used-by path exists and cites the row, and no row
changed this wave. One LOW finding (S100 used-by names a path that does not
cite the row) and three informational notes. The deciding C1 run is untouched
by anything here; these are observations.

## 1. Setup and pin verification

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ColdReadSourcesRows
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r34-seats/ColdReadSourcesRows/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
git -C lane rev-parse HEAD          # -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
```

Pinned bytes extracted from the tip commit and hashed before any run:

```
git -C lane show 0b99d48e...:tools/tally-audit-v2.py > tool.py    # rc 0
git -C lane show 0b99d48e...:tools/mutate-and-run.sh > pristine.sh # rc 0
sha256sum tool.py pristine.sh
# 7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py      == pin, MATCH
# a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh  == pin, MATCH
```

## 2. No row edited this wave

- `cmp /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md lane/corpus/SOURCES.md` → rc **0**; both 80,747 bytes. The fleet working copy is byte-identical to the tip blob, so `git diff 0b99d48e..working -- corpus/SOURCES.md` is empty as expected (the scratch tree *is* the tip checkout).
- `git log --format='%h %ad %s' -1 -- corpus/SOURCES.md` → `0b99d48 2026-10-23 round-34: C1 measured true at c17e593b (deciding run receipt) + ... + S101 row + census end exit 0 (98 rows)` — the last change to the file is the dispatch tip itself.

## 3. Id order and gaps

- `awk -F'|' '/^\| S/ {...}' corpus/SOURCES.md` (order check) → `total_rows=98`, `last=S101`, **no order violations** (ids strictly increase down the Registry).
- Missing ids S001–S101: **38, 39, 98**. All three are pre-documented, not lost rows:
  - S038–S039: `corpus/SOURCES.md:257-261` — "allocated, never written, retired — never reused or renumbered (lesson `round-1.md` ER-K8). A census gap at S038–S039 is this note, not a lost row."
  - S098: `corpus/SOURCES.md:384-388` — "S098 is not used: seat SrcBashCase could not open ... so no row was written for it." `grep -c '^| S098 '` → 0 (rc 1): no S098 row exists.
- Tip commit message "census end exit 0 (98 rows)" matches the observed 98 rows.

## 4. Row-by-row digest verification

### S097 (line 106) — Bash 5.3 `bashref.texi`, sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`, 415,804 bytes

Verifiable against the row's own anchor (the URL pins git commit `b8c60bc9ca365f8261fa97900b6fa939f6ebc303`, so bytes are deterministic):

```
curl --fail --location --silent --show-error --max-filesize 4194304 \
  --connect-timeout 10 --max-time 45 --output s097-bashref.texi \
  'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303'
# attempt 1: curl exit 28 (45 s timeout, 0 bytes) — see Finding F4
# attempt 2 (--connect-timeout 8 --max-time 50): exit 0
wc -c s097-bashref.texi   # -> 415804  == row claim
sha256sum s097-bashref.texi  # -> f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5  == row digest
```

Anchor line claims checked inside those digest-verified bytes:
- `grep -n '@node Exit Status'` → line **3890** exactly (row: lines 3890–3916); special statuses confirmed in-section: 128+N at :3910-3911, 127 not-found at :3912-3913, 126 not-executable at :3914-3915 — the exact content the row's `teaches` names.
- `case` section: `@item case` at line **1044** exactly (row: lines 1044–1084); "The first pattern that matches determines the command-list that is executed." at :1081-1082 and the `@samp{*}` default idiom at :1083-1084 — first-match rule confirmed.
- Independently corroborated by committed round-32 records: `.ufo/waves/round-32/w1/SrcBashExit.md:22` (bytes=415804, same digest) and `.ufo/waves/round-32/w2/ReviewSources.md:50-52` (independent live re-fetch, same digest), plus `corpus/lessons/round-32.md:20-21`.

### S099 (line 107) — pitest.org, sha256 `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc`, 12,023 bytes

Verifiable against the row's own anchor:

```
curl --fail --location --silent --show-error --max-filesize 4194304 \
  --connect-timeout 10 --max-time 45 --output s099-pitest.html 'https://pitest.org/'
# exit 0
wc -c s099-pitest.html      # -> 12023  == row claim
sha256sum s099-pitest.html  # -> b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc  == row digest
```

- `<h1>What is mutation testing?</h1>` at line **101** (section named by the anchor exists); the taught sentence "The quality of your tests can be gauged from the percentage of mutations killed." at line **114** exactly (row anchor: lines 110–114). Matches `corpus/lessons/round-32.md:28-29` and the round-33 byte-identical re-open (`corpus/lessons/round-33.md:26-29`, `.ufo/waves/round-33/w1/SrcPitestReopen.md:9-35`).

### S100 (line 108) — doctest 3.15, pinned by committed snapshot (row mentions **no digest**, by design)

The row's `teaches` explains why: "the /3/ alias drifts (footer rebuilds move the digest); this pins the 3.15 build by committed bytes." With no digest mentioned, the criterion falls to the pin claim itself — verified:

- Committed snapshot exists at the tip: `lane/.ufo/evidence/round-33/c2/doctest-snapshot.html`, 216,574 bytes, sha256 `217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899` — equal to the digest frozen in the C2 counter (`.ufo/evidence/round-33/c2/c2-measure.py:29` `EXPECTED_SHA`) and the lesson Gate (`corpus/lessons/round-33.md:18-23`).
- Live cross-check today (2026-10-23): `curl ... https://docs.python.org/3.15/library/doctest.html` → exit 0, 216,574 bytes, sha256 `7fbaae97f49dc850e9b28301b0a09bf9df2775fdc6b9ad2681329d32a7e37097`; `cmp` vs snapshot → rc 1, first difference char 216322, line 2205. `cmp -l | wc -l` → **exactly 3 differing bytes** (positions 216322, 216324, 216325 — footer "Last updated" timestamp digits). This is precisely the footer-drift class the row cites as its reason to pin committed bytes; the snapshot remains the stable pin and the anchor location is intact in both bodies.
- Anchor location verified in the snapshot: module-introduction paragraph at :245-247, first common-use bullet at :249-250 — matching "module introduction, first bullet".

### S101 (line 109) — mutation-testing.org, sha256 `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420`, 4,341 bytes, committed snapshot named in the row

Verifiable against **both** a committed snapshot and the anchor:

```
sha256sum lane/.ufo/evidence/round-34/src/s101-mutation-testing.html
# 0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420  == row digest; wc -c -> 4341 == row claim
curl ... --output s101-live.html 'https://mutation-testing.org/'   # exit 0
cmp s101-live.html lane/.ufo/evidence/round-34/src/s101-mutation-testing.html  # rc 0 — live is byte-identical today
cat lane/.ufo/evidence/round-34/src/s101-fetch.exit  # -> MUT_EXIT=0
```

Corroborated by `corpus/lessons/round-34.md:18-22` (same digest, snapshot path, quote). The unrelated `s101b-abs-exit-status.html` (9,728 bytes, `60cebcc8…d291`) is the rejected TLDP ABS duplicate kept as evidence only (`corpus/lessons/round-34.md:30-33`); no row references it.

## 5. used-by existence and citation direction

All used-by paths of rows S097–S101 exist (`test -e`, rc 0 each), and each row is cited by ≥1 of them (contract: `mined` = cited by ≥1 used-by path):

| Row | used-by paths (row line) | Cited? |
|---|---|---|
| S097 | `tools/tally-audit.py`, `corpus/knowledge/runner-tally-audit.md` | tool cites S097 at `tools/tally-audit.py:21`; knowledge entry at `:1`,`:12` — matches the round-32 census decision "S097 keeps both paths (the tool cites it)" (`corpus/SOURCES.md:394-397`) |
| S099 | `corpus/knowledge/runner-tally-audit.md` | `:1`,`:3`,`:13` (narrowed cell matches the same round-32 decision) |
| S100 | `corpus/lessons/round-33.md`, `corpus/knowledge/executable-self-assessment.md` | lesson `:18`,`:41` yes; **knowledge entry: no S100 anywhere** — Finding F1 |
| S101 | `corpus/knowledge/witness-equivalence-rule.md` | **exists** (the seat's named criterion) and cites S101 at `:62`,`:65`, quoting the snapshot path |

## 6. Census reproduction

Fleet gate rerun on the scratch lane (script copied to scratch; validate is read-only):

```
cp /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census.sh
bash census.sh validate --today 2026-10-23 /fast/scratch/hyaku/tameshi-r34-seats/ColdReadSourcesRows/lane
# exit 0; output: 8x W04 (pre-existing duplicate-url warnings, S047/S048/S075-S078/S081/S092)
#              + 1x W01 "S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md"
#              + "lane ok .../lane/corpus/SOURCES.md"
```

Matches the tip commit message "census end exit 0 (98 rows)". Note the gate **cannot** catch Finding F1: E11 only checks used-by path existence on disk (`scripts/sources-census.sh:29`, `:566-568`); there is no used-by-cites-id check in the fleet census.

## Findings

### F1 (LOW) — S100's used-by names a path that does not cite S100

`corpus/SOURCES.md:108` lists `corpus/knowledge/executable-self-assessment.md` in used-by, but that file never mentions S100:

```
grep -c 'S100' lane/corpus/knowledge/executable-self-assessment.md   # -> 0, rc 1
grep -n 'doctest|docs\.python\.org|S100|SOURCES' ... (case-insensitive)  # hits only S055/S095/S096 contexts
```

Its `source:` header (`:1`) cites **S055** — the row S100's `teaches` explicitly supersedes — plus S095/S096 (last touched round-31, commit `2da841b`, before S100 existed), and its doctest URL (`:23`) is the drifting `https://docs.python.org/3/library/doctest.html` `/3/` alias that S100 was created to replace. Contract: used-by holds "paths of the knowledge entries or lessons **citing the row**" (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` Shape; `CORPUS.md` §SOURCES.md). This is the same no-id-or-path-cite defect class the lane treated as worth fixing for S099 in round 32 (used-by narrowed with an old→new log, `corpus/SOURCES.md:394-397`). S100's `mined` status is unaffected (`corpus/lessons/round-33.md` cites it at `:18`,`:41`, and the row-change log `:41-42` shows the used-by was set this way at creation). Disposition is the lane's call (a logged rule-2 used-by narrowing, or an entry amendment citing S100); as a row-cell accuracy matter it does not touch the C1/C2 measurements or any digest pin.

### F2 (INFO) — census W01 on S101 (tier C + mined + used-by)

The fleet census emits `W01 S101 tierC mined used-by=...` (warning, exit unaffected). The contract's tier-C rule is "lead only — never sole support for an admitted entry." Assessed not material here: `corpus/knowledge/witness-equivalence-rule.md` cites S101 as corroboration alongside S097 (`:59-66`), and its primary ground is the lane's own probe battery and deciding run (`:40-57`, own-gate output is tier-A class). Recorded so the W01 is not mistaken for a new regression.

### F3 (INFO) — C2 QUOTE exact bytes live only in the snapshot's meta tags

The exact byte string frozen in the C2 counter (`c2-measure.py:26`) occurs in `doctest-snapshot.html` only at the meta lines 11, 15, 16 (`grep -n` full sentence → 3 lines); in the body the same sentence spans lines 245–247 wrapped across lines with inline `<code>` markup. The counter's byte-containment check therefore passes via the meta occurrence. No impact on C2 (measured true) or on the S100 row (which names no quote or digest); noted for bookkeeping precision — the round-33 spotcheck's "present in the snapshot BODY ... not only in meta tags" (`corpus/lessons/round-33-verifier-spotcheck.md:50-53`) is true of the sentence text, not of the exact counter bytes.

### F4 (INFO) — Savannah flakiness observed, digest verified on retry

First S097 fetch: `curl exit 28` (45 s timeout, 0 bytes received); identical retry with `--connect-timeout 8 --max-time 50`: exit 0 with the exact pinned digest and size. Same network-flakiness class the row itself records for gnu.org (`corpus/SOURCES.md:106`). The digest is additionally anchored by two committed independent round-32 records (§S097 above), so the pin never rested on a single fetch.

## Residual risks and verification gaps

- S097: the range *end* 3916 was not separately bounded (Exit Status content confirmed at 3890–3922; the next `@node` was not located). Range start 3890 and all taught content verified in digest-checked bytes.
- S099: lines 110–113 were not re-derived line-by-line; the taught quote is verified at exactly line 114 and the section `<h1>` at line 101 of the digest-checked fetch.
- S100: the live-vs-snapshot difference is quantified as exactly 3 bytes (footer timestamp); the snapshot remains the sole stable pin per the row's design, and no digest is claimed in the row, so no drift criterion applies to it.
- The pinned tool/runner were hash-verified only; neither was executed (out of this seat's scope; the C1 kill rule was not consumed — `c1-measure.py` was never invoked).
