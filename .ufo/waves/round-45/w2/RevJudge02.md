seat: RevJudge02

# C1 falsify wave — independent re-judgment of S089, S094, S108

Inputs at commit `ad5942c6e9858af19d00000b58439b321ddfa62b`: ledger `.ufo/evidence/round-45/freshness/ledger.json` (S089/S094/S108 entries), committed snapshots `.ufo/evidence/round-45/freshness/sources/S0{89,94,108}.raw.gz`, author reports `.ufo/waves/round-45/w1/ExecRows16.md`, `w1/ExecRows17.md`, `w1/ExecRows22.md`. Registry rows `corpus/SOURCES.md:98` (S089), `:103` (S094), `:120` (S108); byte-identical between `ad5942c` and the worktree (`diff -q` of `git show ad5942c:corpus/SOURCES.md` vs worktree → identical). Scratch: `/tmp/tameshi-r45-RevJudge02/`. No tools installed or upgraded; no pacman/uv/npx transactions; the only lane write is this report.

## Verdicts

S089 agree — reviewer RevJudge02 — sha equal (live=snapshot=ledger `79f6501a…079ce`); quote sits in body directly after the `10 ** 0` example at the row's anchor and its no-definitive-way-for-Stryker-to-find-or-ignore statement supports the teaches that an equivalent mutant stays a survivor.
S094 agree — reviewer RevJudge02 — sha equal (live=snapshot=ledger=anchor digest `6e9532a9…0d697`); quote is §1 body at the anchored "Each submitted model" sentence and states the organizer-only fixed test set that grounds the teaches' holdout-overfit claim.
S108 agree — reviewer RevJudge02 — snapshot sha matches ledger (`9056c530…0ff4c`); today's live sha differs (`dc8d49c4…cb45d`, dynamic chrome) but the quote is present verbatim in today's live extracted text, sits directly under the anchored `如何更新 .expected 文件?` heading, and states the `--update_goldens`/`--test_strategy=local` update plus the resulting-diff check that the teaches cell claims.

## Provenance (my own fetches, 2026-10-25)

`curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-RevJudge02/S###.live <url>`, then `sha256sum` live vs `gunzip -c <snapshot> | sha256sum` vs ledger `raw_sha256`:

| row | live sha256 (mine) | snapshot sha256 | ledger raw_sha256 |
|---|---|---|---|
| S089 | `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce` (38687 B) | same | same — EQUAL |
| S094 | `6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697` (322643 B) | same | same — EQUAL (also the digest pinned in `corpus/SOURCES.md:103`) |
| S108 | `dc8d49c48469e5b43a4cf85b3f7df397bff9e2fcd2215c896f4ebadeffccb45d` (111409 B) | `9056c530ca6cc9dfe036f2acd523aec7e9d7aa312fd4a5fcb2a94ad74740ff4c` | `9056c530…` — snapshot==ledger; live DIFFERS (dynamic page; `w1/ExecRows22.md` records a third digest `a9b2752f…` from a prior dispatch at the same 111409-byte size) |

S108 hash-mismatch branch: per the falsify procedure I extracted today's live text (`measure.py --extract S108.live`) — the quote is present at the same offset as in the snapshot extract; the normalized texts are byte-identical (`snap_txt == live_txt: True`), so the drift is page chrome, not content. No dispute.

## Quote context (measure.py --extract of the committed snapshot)

- S089, idx 1681, body after the `10 ** 0` example (anchor cell: "page body after the `10 ** 0` example"): "…even if we change >= to <= and even < or > we will get the same output each time! **It is called equivalent mutant . There is no definitive way for Stryker to find and ignore them.** There is currently also no way yet to mark them to be ignored…" — 18 tokens; shares equivalent/mutant/stryker with the cells; not copied from any cell. Supports teaches (`corpus/SOURCES.md:98`: an equivalent mutant stays a survivor in the score…).
- S094, idx 5008, §1 Introduction body (anchor: "sentence beginning Each submitted model is"): "…can submit (multiple) predictive models in the course of competition. **Each submitted model is evaluated on a (fixed) test set that is available only to the organizers.** The score of each solution is provided back to each participant, who can then submit a new model…" — 17 tokens; shares fixed/model/submitted/test; supports the teaches' holdout-kept-from-the-candidate claim.
- S108, idx 2515, directly under the heading `如何更新 .expected 文件?` (the row's anchor section), followed only by footer license boilerplate: "…test_case_last.expected 如何更新 .expected 文件? **可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。** 如未另行说明,那么本页面中的内容已根据 知识共享署名 4.0 许可…" — 6 whitespace tokens (exactly at the contract minimum, still ≥6); shares expected/goldens/update; supports teaches (`corpus/SOURCES.md:120`: the zh-cn page restates that .expected files update only via --update_goldens and that the resulting diff is checked).

## Counter cross-check (authorized mode, non-deciding)

`python3 .ufo/evidence/round-45/freshness/measure.py --lane <lane> --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-RevJudge02/S###.json --snapdir /tmp/tameshi-r45-RevJudge02` → `CHECK S089 verified ok` / `CHECK S094 verified ok` / `CHECK S108 verified ok` (exit 0 each; fragment = the committed ledger entry verbatim). Independent re-derivation with the counter's own `grade()` also gives verified/ok for all three, with `copied-from-cells: False` and shared-content-word counts 3/4/3.

## Result

No dispute: all three wave-1 entries are honest re-verifications — provenance confirmed (S089, S094 byte-equal today; S108 snapshot-faithful with live quote re-located today), quotes are body content at the row anchors, and each supports its row's teaches. Reviews filed at `/tmp/tameshi-r45-RevJudge02/reviews.json` pointing at this report.
