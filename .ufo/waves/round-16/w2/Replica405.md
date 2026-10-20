# Replica405 — cold-read replica, SKILL.md:405–465

**Verdict: holds.** The single section in range, `## Cross-language divergence — bash vs JS
(round 3, measured)` (SKILL.md:405–465), is a **record** of round 3's measured mutation-sweep
comparison; every claim cluster re-checked at the named anchors. No gap.

## Page verification

```
git -C …/tameshi-shokunin show c699c8c3…:SKILL.md | sha256sum
→ 3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4  (matches expected)
```

Range 405–465 contains exactly one heading — `405:## Cross-language divergence — bash vs JS
(round 3, measured)`. The next heading, `## No-permissiveness audit recipe`, begins at 466.
Classification: **record** — it reports measured results and rules derived from two measured
cases ("each backed by the two cases"); the embedded rule bullets are lessons, and each was
exercised rather than contradicted during the re-check below.

## Anchor re-checks (commit c699c8c36d6e4eca4b796b81a8247904aa145ec8)

Cited files pulled to scratch `/tmp/tameshi-r16w2-Replica405-Ku0xus/` via `git show`.

### Claim cluster 1 — headline parity + anti-claim (lines 409–416)

- `plans/round-3.plan.md:8-9` — verbatim: "Anti-claim: if the bash suite's kill-rate diverges
  wildly, that divergence IS the finding (language-class differences in what suites protect)."
  **Matches** the SKILL claim.
- `mutation-case-kagi-census.md:162-170` — confirms "it does not diverge wildly on the headline
  rate", both 8/10 (80 %), suite count held every run, no inconclusive run. **Matches.**
- `mutation-case-kimi-census.md:29-37` — "kill rate 8/10 (80 %); survivors D2, D10. No
  inconclusive run … 11 runs … 7.0 s"; restore proof `83016d45…4f426` before=after. **Matches.**

### Claim cluster 2 — table rows (lines 418–430)

| Row | Re-check |
|---|---|
| artifacts/lines | `surface-census.sh` live sha256 `275d8294a94e…53009f` = record's pin, 44212 B, **886 lines** ✓. `kimi-census.mjs` at kumitate commit `f86b8ed` has sha256 `83016d45049b…4f426` = record's pin, **896 lines** ✓. |
| JS suite grammar | `kimi-census.mjs` (pinned blob) :852 prints `KIMI_CENSUS_SELFTEST: ${passed}/${results.length} pass`; :850 prints `FAIL <label>` lines ✓ |
| bash suite grammar | `surface-census.sh`: `ok-case`/`bad-case`/`skip-case` prints at :755/:758/:821/:823; `SELFTEST: PASS (%s cases)` / `FAIL (%s/%s cases)` at :846–847 ✓ |
| abstention | :817 `command -v "$JANITOR"` gate → two `skip-case … substrate-absent (handler not on PATH)` prints inside the 16-case count ✓ |
| kill width | kimi report :44/:46 — D1 and D3 each 16/43 (`27/43 pass`), incl. exact green baseline (:74); kagi report :171–175 — widest 3/16 (B3), "labels are near-singletons" ✓ |
| survivors | kimi :29 D2+D10 (reported-but-unasserted family, :94–103 for D10); kagi :71/:76/:107–122 B5 unreached exec-x-bit arm + B10 unasserted `ok=` count ✓ |
| calibration | kimi :185–191 E1 9/10, miss = D7; kagi :186–187 E1 10/10 verdicts, 6/10 counts, B2/B3/B6 each +1 ✓ |
| cost | kimi :30 "11 runs … 7.0 s"; kagi :52–53 "11.0 s wall for 11 runs", control 1.0 s (:43) ✓ |
| restore pins | `83016d45…` (kimi) and `275d8294…` (kagi) — both file sha256s, both verified identical at restore in the reports; `surface-census.sh` still hashes to that pin **today** ✓ |

### Claim cluster 3 — rules (lines 432–465)

- Grammar-before-summary, token-only kill (B4 exit matched, token caught it — kagi :88–91 ✓),
  abstention structural (kagi :27–35, incl. `:741-744` kagi LOG cite ✓), kill-width structural
  (kagi :171–175 ✓), survivor sub-classification (kagi :176–180 vs gates-survey-kagi :326–361 —
  F-2 is literally "three of six refusal paths … have no selftest case", the refusal-paths-
  without-cases pattern ✓), exact strings (kagi :181–182; `unverified=3` demand confirmed at
  `surface-census.sh:782` per kagi report's own cite), anti-claim verdict naming U2/U5 still
  unknown — kagi :193–206 Unknowns section contains exactly U2 ("verbs-logic mutants …
  host-gated") and U5 ("kill-rate stability across hosts/toolchains") ✓. PROVINCE.md:16-17
  records the "independent lanes" generality bar ✓.

## Minor observations (not gaps)

- `kimi-census.mjs` has evolved since round 3: kumitate HEAD blob is 922 lines, sha256
  `5e8d5913…`. The record's 896-line / `83016d45` pin is accurate for the round-3 blob (commit
  f86b8ed); post-round drift is expected and does not falsify the record.
- Rule bullets are instruction-shaped, but the section is presented as a measured record; all
  rule substance was exercised in the re-checks above, so no separate execution verdict needed.

## Commands executed (exits 0 unless noted)

- `git show c699c8c3…:SKILL.md | sha256sum` → expected sha ✓
- `git ls-tree -r --name-only c699c8c3… | grep …` → located cited files
- `git show c699c8c3…:<file>` ×5 → /tmp scratch copies
- `sed -n` anchor reads: kagi 27-35/82-103/162-206, kimi 29-37/44-53/185-191,
  plan 8-9, PROVINCE 16-17, gates-survey 326-361
- `sha256sum` both gate artifacts; `git -C kumitate-shokunin log/show` pin resolution;
  `grep` grammar checks on both pinned files
- `git cat-file -t 275d8294 / 83016d45` in sibling repos → not git objects (they are file
  sha256s — report clarifies "restore pin" = artifact digest)

## Files opened

- `corpus/knowledge/mutation-case-kagi-census.md` (at c699c8c3…)
- `corpus/knowledge/mutation-case-kimi-census.md` (at c699c8c3…)
- `corpus/knowledge/gates-survey-kagi.md` (at c699c8c3…, :326-361 only)
- `plans/round-3.plan.md` (at c699c8c3…, :8-9 only)
- `PROVINCE.md` (at c699c8c3…, :16-17 only)
- `kagi-shokunin/corpus/surface-census.sh` (live, = record pin; :755-847 region)
- `kumitate-shokunin/scripts/kimi-census.mjs` (pinned blob at f86b8ed; grammar lines)

```json
{"seat":"Replica405","skill_sha256":"3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4","sections":[{"start":405,"heading":"## Cross-language divergence — bash vs JS (round 3, measured)","class":"record","verdict":"verified-record","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["git show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SKILL.md | sha256sum","git ls-tree -r --name-only c699c8c3 | grep mutation-case|gates-survey|round-3.plan|PROVINCE","git show c699c8c3:<cited files> into /tmp/tameshi-r16w2-Replica405-Ku0xus","sed -n anchor reads on all cited line ranges","sha256sum surface-census.sh kimi-census.mjs (+ pinned blob at kumitate f86b8ed)","grep ok-case/bad-case/skip-case/SELFTEST surface-census.sh; grep selftest prints kimi-census-pinned.mjs"],"opened":["corpus/knowledge/mutation-case-kagi-census.md@c699c8c3","corpus/knowledge/mutation-case-kimi-census.md@c699c8c3","corpus/knowledge/gates-survey-kagi.md@c699c8c3:326-361","plans/round-3.plan.md@c699c8c3:8-9","PROVINCE.md@c699c8c3:16-17","kagi-shokunin/corpus/surface-census.sh:755-847","kumitate-shokunin/scripts/kimi-census.mjs@f86b8ed"],"scratch":"/tmp/tameshi-r16w2-Replica405-Ku0xus"}]}
```
