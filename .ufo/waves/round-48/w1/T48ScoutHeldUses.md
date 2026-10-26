# T48ScoutHeldUses — every citation of S026 / S048 / S093 / S108 at BASE 473336d9

Observed with `git grep` and `git show` at BASE `473336d9d789f6081195e7376d17836a24666bc3`. Line numbers are BASE lines. No LSP (markdown/tsv text), so grep is the literal method. The lane HEAD during this read was `f1cfaad3`, not BASE. I read only BASE objects.

## 1. Rows (corpus/SOURCES.md @ BASE)

| row | line | tier | opened | recheck | status | used-by cell (verbatim) |
|---|---|---|---|---|---|---|
| S026 | 37 | A | 2026-10-19 | 730d | mined | `corpus/knowledge/repeated-control-precondition.md` |
| S048 | 57 | A | 2026-10-20 | 90d | mined | `corpus/knowledge/incremental-pin-disposition.md` |
| S093 | 102 | A | 2026-10-23 | on-release | mined | `corpus/knowledge/regression-tally-completeness.md` |
| S108 | 120 | B | 2026-10-24 | 180d | mined | `corpus/knowledge/r8-golden-update-flag.md` |

Rows are 13 `|`-fields: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`. URLs:
- S026 https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- S048 https://pitest.org/quickstart/incremental_analysis/ (the same URL as S041 line 50 and S047 line 56)
- S093 https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml
- S108 https://www.tensorflow.org/federated/golden_tests?hl=zh-cn

## 2. Knowledge entries that cite them (the re-point set)

Each entry is `corpus/knowledge/<file>.md`. The header lines are 1 `source:`, 2 `verified-at:`, 3 `recheck:`, unless noted.

| row | entry | source: line | verified-at: line | recheck: line | in used-by? | cites row? |
|---|---|---|---|---|---|---|
| S026 | repeated-control-precondition.md | L1 `source: S004 — … ; S026 — …html — post body by John Micco, published 2016-05-27; fetched 2026-10-20T02:13:47Z, sha256 ca1145fb…7a6c8c (236,385 B). Located excerpts: .ufo/evidence/round-12/ControlKnowledge/quotes.tsv` | L2 `verified-at: 2026-10-20` | L3 `recheck: 730d — S026's registry cadence; … curl … grep -c 'hardly a perfect solution' → 2 (ran 2026-10-20T02:17:02Z …)` | yes | yes (source:) |
| S048 | incremental-pin-disposition.md | **L5** `source-correction: S048 — https://pitest.org/quickstart/incremental_analysis/ — same reopened bytes and numbered items 4–5 as S041/S047; supersedes S047's …` (L1 `source:` cites S003, S041, S047, S031 and not S048) | L2 `verified-at: 2026-10-20` | L3 `recheck: 90d — … curl … pitest.org … grep -c 'all these optimisations introduce a degree of potential error' → 1 …` | yes | yes (source-correction:) |
| S093 | regression-tally-completeness.md | L1 `source: S087 — …; S093 — bwrap(1), bubblewrap 0.13.1 bwrap.xml (the sandbox the v4 counter runs each selftest in); S094 — …` | L2 `verified-at: 2026-10-23 — sources re-opened by round-30 wave-A seats; …` | L3 `recheck: bash tools/mutate-and-run.sh --selftest …; …; re-open S087, S093, S094` | yes | yes (source:) |
| S108 | r8-golden-update-flag.md | L1 `source: S107 — …golden_tests.md — §How do I update .expected files?; S108 — https://www.tensorflow.org/federated/golden_tests?hl=zh-cn — 如何更新 .expected 文件？` | L2 `verified-at: 2026-10-24` | L3 `recheck: 365d` | yes | yes (source:) |

Body (non-header) mentions inside those four entries. These are context only and carry no source line:
- repeated-control-precondition.md: L16 (`S026.html:1130-1137`), L21, L27. These point at the old round-12 copy of the S026 body. Line numbers into the old snapshot go stale if the entry is re-pointed to a new snapshot.
- incremental-pin-disposition.md: L346 (`Source guidance correction: **S048 supersedes S047's …`). It also cites S041/S047 at L47, 67, 70, 71, 83, 97, 132, 136, 205, 206, 272, 286, 297, 300-302. Those are historical rows and stay.
- regression-tally-completeness.md: L42 (v4 row, "bubblewrap sandbox (S093)"), L68, L72 (E1 `S093 bwrap.xml:233-235`), L73.
- r8-golden-update-flag.md: header only (S108 is cited there at L1).

## 3. Used-by vs citers (the diff)

- Used-by entries that do not cite the row: **none.** All four rows' single used-by entry cites the row in its header.
- Entries that cite the row in a `source:`/`source-correction:` header but are not in used-by: **none.**
- Entries that mention the row in body text only. They are not in used-by and carry no source cite:
  - S026 → `corpus/knowledge/r9-false-red-rate.md` L10 and L16 (the "S026-ground entry repeated-control-precondition.md already quotes…" cross-reference). Its header is `source: S260` (L1), `verified-at: 2026-10-25` (L2), `recheck: 365d` (L3). **Do not re-point it.** S260 is the second carrier of the same post and is in its own used-by.
  - S048 → `corpus/knowledge/fleet-kill-rate-ledger.md` L374 (`source method: S003 and S048, incremental-pin-disposition.md`). It has no `source:`/`verified-at:`/`recheck:` header lines (grep found none). It is a prose back-reference to the S048 entry, not a source cite. S048 used-by does not list it. Judgement: leave it. Re-pointing would create a `source:` line where none exists, and the S048 used-by claim stays correct.
  - S108 → `corpus/knowledge/r40-write-form-misses.md` L14 ("S108 is not support for this entry"). Its header is `source: S152` (L1), `verified-at: 2026-10-24` (L2), `recheck: 365d` (L3). It is an explicit non-citation. **Do not re-point it** or add it to used-by.
  - S093 → none.
- So the exact re-point set is 4 entries:
  1. `repeated-control-precondition.md` L1 (S026), plus `verified-at:` L2 and the L3 recheck prose.
  2. `incremental-pin-disposition.md` L5 (S048 `source-correction:`), plus `verified-at:` L2 and the L3 recheck prose.
  3. `regression-tally-completeness.md` L1 (S093), plus `verified-at:` L2 and the L3 recheck text ("re-open S087, S093, S094").
  4. `r8-golden-update-flag.md` L1 (S108), plus `verified-at:` L2.
- Shape caveats for the L1:
  - Three entries carry several sources in one `source:` line (r8: S107 + S108; repeated-control: S004 + S026; regression-tally: S087 + S093 + S094). Re-pointing replaces only the S026/S093/S108 token with the new id and keeps the others.
  - incremental-pin-disposition cites the PIT page three times (S041, S047, S048). Only the S048 `source-correction:` token moves. S041 and S047 are not in the target set.
  - Where `verified-at:` is a whole-entry date (all four), the sibling sources (S004, S087/S094, S107, S003/S041/S047/S031) were not re-opened 2026-10-26. Setting `verified-at: 2026-10-26` over a multi-source line claims more than was re-verified, unless the L1 annotates which source was re-opened.
  - regression-tally-completeness L2 carries a prose qualifier ("sources re-opened by round-30 wave-A seats") that would need rewording.

## 4. Supersession relations and the round-45 ledger

Supersession chain (SOURCES.md): S041 (L50) → S047 (L56, "supersedes S041", used-by incremental-pin-disposition) → S048 (L57, "supersedes S047"). Round-13 notes (L297-298): "S047: round-13 precision correction to S041; original row retained", "S048: object-neutral clarification of S047; same PIT URL, no new source". All three share one URL, so the lane's census reports the S047/S048 `W04` duplicate-URL warnings. The new S048 superseding row will add another duplicate. No row supersedes or is superseded by S026, S093 or S108.

Related rows that are not supersessions:
- S260 (L135, mined, 365d, used-by r9-false-red-rate.md): a second, byte-stable carrier of the S026 post via the per-post feed. S026's own Teaches and S260's are the same 84% figure.
- S107 (tier A, used-by r8-golden-update-flag.md): the upstream English golden_tests.md that S108 localises.
- S094 (used-by regression-tally-completeness.md and runner-tally-audit.md): cited with S093 in the same `source:` line.

Round-45 ledger (`.ufo/evidence/round-45/freshness/ledger.json`, 73 entries, `round: 45`). Round-45 verifier spot-check says reviews.json has 71 agree and 2 dispute:
| id | ledger verdict (author) | review (reviewer) | quote | snapshot | raw_sha256 |
|---|---|---|---|---|---|
| S026 | holds (ExecRows04) | **agree** (CritJudge06) | "about 84% of the transitions we observe from pass to fail involve a flaky test" (15 tokens; raw lines 1132/1097) | round-45/freshness/sources/S026.raw.gz | 5d74dd1c…2296 |
| S047 | holds (ExecRows05) | not examined for this item | "Although this assumption seems reasonable, it is currently unproven ." | …/S047.raw.gz | e9cbc3e1…b590db |
| S048 | holds (ExecRows05) | **dispute** (CritJudge02, "agree with dispute" in spot-check L36/L72) | "If a mutation was previously killed, but the class or killing test has changed" (truncated antecedent; consequent "then it is likely … prioritised above others" is missing) | …/S048.raw.gz | e9cbc3e1…b590db (identical to S047) |
| S093 | holds (ExecRows17) | **dispute** (CritJudge03, spot-check L73 agrees) | 25-token markup-only fragment `< option >--unshare-user-try< /option > …` that never names `--unshare-all` and stops before `--unshare-cgroup-try` | …/S093.raw.gz | f8a95822…c240 |
| S108 | holds (ExecRows22) | **agree** (RevJudge02) | "可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。" (tag-stripped text) | …/S108.raw.gz | 9056c530…ff4c |

Per round-45 spot-check L35 and L88, the live bytes for S026, S093 and S108 differ from the committed snapshots (dynamic pages). Pin by quote, not whole-page hash. Where S026's and S108's quotes were still located live on that date, S093's live page shows a markup fragment.

Quotes the new Gate quotes must replace (from the dispute rulings):
- S048 needs the consequent, quote text `then it is likely that the last killing test will still kill it and it should therefore be prioritised above others` (the reviewer's cited text; only the 7-word "it should therefore be prioritised above others" was independently quoted in the round-13 spot-check L149). The sentence must be ≤25 words and located in the snapshot.
- S093 needs the `--unshare-all` listitem prose ("Unshare all possible namespaces. Currently equivalent with:" … through `--unshare-cgroup-try`). A single ≤25-word quote cannot cover all six flags, so it needs a different anchor for the "six-flag expansion" claim.
- S108 must be located in tag-stripped text. The raw HTML wraps `--test_arg=--update_goldens` and `.expected` in `<code>` (round-40 lesson: quote-split).

## 5. Other (non-entry) mentions, for completeness

Not re-pointed. These are historical lesson/spot-check/README records unless noted:
- SKILL.md: L1481 (`Source: S004/S026 and corpus/knowledge/repeated-control-precondition.md`), L1558 (`PIT source clarification: S048 supersedes S047's object-specific …`).
- corpus/README.md: L80 (F3 sources S004, S011, S025, S026, S027, S040), L127 (`S004, S026; tools/repeat-control.py`), L176 and L185 (S048), L501, L507, L511 (S108), L577 (S026). Tools: no hit (no `tools/` file cites these ids).
- corpus/QUALITY.md L954 (S108 redirect-loop).
- SCORECARD.md: L353, L379, L479, L532, L582 (S048 / S047 W04 warnings), L1870-1877 (S108 round-40 pin), L2154, L2159, L2200, L2292 (the round-45 freshness count; S048 and S093 disputed), L2312 (Planned round 48).
- SOURCES.md prose log: L192, L196 (S026 round-12 reopen), L298 (S048), L402 (S093 added, round 30), L481 (round 46).
- lessons/*: round-1 L385, round-12, round-13, round-14..round-31 (W04 S047/S048 warnings), round-30 (S093 reopen: snapshot `.ufo/evidence/round-30/sources/S093-bwrap-0.13.1.xml`, sha256 2cb77df2…be1da), round-39/40 (S108 and its snapshot), round-45, round-46, round-47.

## 6. Fact notes for the L1

- The census W04 duplicate-URL warnings (S047/S048 and later) are all older rows that are not in the S048 supersede target. A new S048-successor row on the same PIT URL adds a W04 for the new id.
- A new S026 row would duplicate the URL with S026 itself; the S260 row is a different URL.
- S093's row is `on-release` recheck, S108's 180d, S026's 730d, S048's 90d.
- S026 snapshot bytes in the entry (L1 sha256 `ca1145fb…`, 236,385 B, 2026-10-20) differ from the round-45 ledger snapshot sha `5d74dd1c…`, and the entry's `S026.html:1130-1137` line refs at L16/L21 point at the old copy.

No tools installed; no scratch beyond `/fast/scratch/hyaku/tameshi-r48/T48ScoutHeldUses` (removed).
