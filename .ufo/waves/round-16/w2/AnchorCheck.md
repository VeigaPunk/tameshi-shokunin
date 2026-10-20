# AnchorCheck — wave-2 falsification of the round-16 in-place SKILL.md repairs

**Seat:** TameshiR16.AnchorCheck
**Attacked:** the errata preamble claim at SKILL.md:1714 — *"Wrong expectations
were repaired in place with the line count of every edited section unchanged,
so every `SKILL.md:<line>` self-anchor still resolves."*
**Verdict: holds** — all 22 this-page anchors still resolve at identical line
numbers; every repair is a same-line-index byte replacement plus a pure
91-line append tail. One quoting line (SKILL.md:1346) now quotes wording that
line 925's repair changed; that is intentional historical citation, not an
anchor break.

## Evidence files

- Script (I own): `.ufo/evidence/round-16/coldread/anchor-check.py`
- Full output: `.ufo/evidence/round-16/coldread/anchor-check.txt`

## Commands and key results

```
$ python3 .ufo/evidence/round-16/coldread/anchor-check.py   # exit 0
page   c699c8c…:SKILL.md  sha256=3d8a1edb…cbb7a4  lines=1796
  expected sha256=3d8a1edb…cbb7a4  match=True            # matches the announced page hash
snapshot e69b488:.ufo/evidence/round-16/coldread/SKILL.snapshot.md
  sha256=97cf436b…3580  lines=1705                       # matches sha printed at SKILL.md:1709
changed lines (same-index): 19                           # {15,63,134,135,271,272,278,279,280,
                                                         #  361,505,514,515,925,950,1390,1393,
                                                         #  1472,1614}
pure append tail: new[1706..1796] = 91 lines             # errata + round-16 sections
heading lines moved/altered inside snapshot span: 0      # => every edited section kept its
                                                         #    line count AND its line range
result: 22/22 this-page anchors resolve; 1 points into repaired text
```

### What was checked, concretely

1. **No real `SKILL.md:<n>` literal anchors exist.** The only `SKILL.md:`-style
   token is `:1714`'s generic `` `SKILL.md:<line>` `` pattern mention.
   Self-references are bare `:n[-m]`; the page itself declares the convention
   at SKILL.md:1250 — "(Anchors `:…` are this page; the others are
   repo-relative.)" Bare `:n` that *continues* a `file.md:n` citation (e.g.
   `mutation-case-kimi-census.md:45, :82-92`) refers to that file, not this
   page — judged by context; ~180 such continuations were classified to their
   named files (kimi/kagi/tsukuroi/mado census notes, gates-survey-*, the two
   manifest blobs `kimi-census.mjs`/`surface-census.sh`, ledger, plans,
   PROVINCE, `tools/mutate-and-run.sh`).

2. **22 bare anchors judged to mean this page all resolve** (script output,
   `== self-anchors judged to mean this page ==`): `:131` (recipe heading),
   `:811-812`, `:813-817`, `:823-825`, `:840-844`, `:879-881`,
   `:925-929`, `:965-1008`, `:1017-1019`, `:1021-1053`, `:1069-1090` (×2),
   `:1218-1222`, `:1226-1228` (×2), `:1246-1270`, `:1250-1254`, `:1294-1297`,
   `:1324-1331`, `:1332-1344`, `:1359-1363`. All target lines exist and are
   byte-identical to the snapshot **except** `:925-929`, whose line 925 was
   repaired ("Four legs at this revision" → "Four legs at that revision
   (r7-1; seven since round 16)") — status RESOLVES-CHANGED.

3. **Stale quote, not stale anchor:** SKILL.md:1346 cites `:925-929` by
   quoting the old wording `'Four legs at this revision'`; the cited line
   keeps the same number and meaning. Deliberate ("stand at `cf41efaa…`" —
   the sentence is about what the historical text *said*), flagged for
   completeness, not a break.

4. **Line-count claim verified two ways.** (a) All 19 changed lines are
   same-index replacements — the diff contains zero insertion/deletion hunks
   inside the snapshot span; (b) every `##`-level heading occupies the same
   line in both files (`heading lines moved/altered: 0`), so each edited
   section's line range — and hence its line count — is unchanged. The only
   structural change is the append tail starting at line 1706 (the snapshot's
   last line 1705 lacked a trailing newline; it is byte-identical in the new
   file).

5. **Ambiguous bare `:n` refs** (context strongly suggests another file;
   none resolve *meaningfully* as this page; listed per contract):
   - `:14` (SKILL.md:1025) — watchdog lane-map line, after
     `scripts/shokunin-watchdog.sh:3-5`.
   - `:20` (SKILL.md:1262) — likely `PROVINCE.md` continuation of `:14-18`.
   - `:305-320` (SKILL.md:756) — a range in the tsukuroi S5-1 evidence the
     sentence discusses (note or ledger), not this page.
   - `:354-360` (SKILL.md:1207) — "ER-4's addendum", likely
     `fleet-kill-rate-ledger.md` lines.
   - `:281` (SKILL.md:1361) — "superseded in the ledger by ER-2", likely
     `fleet-kill-rate-ledger.md:281`.
   - `:932-960` (SKILL.md:1328) and `:1488-1527` (SKILL.md:1331) — most
     likely `tools/mutate-and-run.sh` regions alongside `:104-106`; on this
     page `:932-960` lands on "Using the ledger" (plausible prose) but
     `:1488-1527` lands in the round-12 registry which does not "cover the
     mirror", favouring the tool reading.
   - `:1230-1244` (SKILL.md:1419) — "rows land appended in the ledger":
     either ledger lines or this page's re-pin-semantics section, which does
     state the append-only rule — resolves on this page but ambiguous.

   Timestamp/mtime false positives (`09:47:15`, `19:15:14Z`, `14:06:23`, …)
   and the `gate.rs:15`→`:11` rename were classified as non-anchors.

## Minor observation (not a fall)

Pre-repair wording inside the page refers to "this page" anchors loosely in
three places (`:1025 :14`, `:1207 :354-360`, `:1361 :281`) that only hold as
*other* files' lines — the `:…` = this-page convention at :1250 is thus
contextual, not global. A strict reader of the convention could misresolve
them. Recorded, not repaired (wave-2 seats advise only).

## Tooling

None installed. Python 3.14 (system) + git only. Scratch:
`/tmp/tameshi-r16w2-AnchorCheck-1792504298/` (exports of both blobs).
