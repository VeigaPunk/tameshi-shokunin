# T51W2Read10 — cold-read re-key reader, `### The receipt at this boundary`

Seat T51W2Read10 (reader, round-51 wave 2). Candidate `6d8c11e378aa90b12650808e1b79270742935f15`, base
`9962033fd7a75aa2f2847e979dd687a5d28505a1`. Method: re-resolved the heading at CAND, read the whole section
through the next heading, then read every cited surface against candidate bytes (`git show CAND:<path>` for
lane files; a `--shared` scratch clone at CAND for the one executable claim). The fixture list and old
READERS_JSON were used only as a cross-check afterwards; every pointer below was taken from the section text
itself. Read-only everywhere except this report; scratch deleted before yield; no tools installed.

## Section resolution at CAND

- Heading `### The receipt at this boundary` re-resolved at **SKILL.md:1212** (grep over
  `git show 6d8c11e3…:SKILL.md`); span **1212–1229**; next heading `### The re-pin semantics, as executed`
  at **:1230**. Matches the old ledger entries' span (start 1212, end 1229) exactly.
- Section sha256 at CAND `88f5a68550693f4b280c858fe6f259d6b376584bb13c8ec1b8afb81553611fbc`; **identical at
  base** (same sha from `git show 9962033f…:SKILL.md | sed -n '1212,1229p' | sha256sum`). The SKILL.md diff
  base→CAND touches only the appended round-51 registry block (hunk `@@ -2134,3 +2134,38 @@`), so the
  monitor drop for this section is purely `input-drift:tools/mutate-and-run.sh` — the runner's bytes changed
  (126 insertions / 47 deletions), not the section's.

Section text at CAND (1212–1229), quoted in full:

> Run at the tick (this lane; `--selftest` 19:58:49Z, `--regression`
> `REGRESSION_DATE 2026-10-14T19:58:59Z`; logs `/tmp/w9-tameshi-t93/selftest.txt`,
> `/tmp/w9-tameshi-t93/regression.txt`):
>
> - `--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0.
> - `--regression` → 4 legs, each `match=10/10 … flips=0` (killed 8/8/6/4),
>   closing `REGRESSION: PASS (cases=4 passed=4; ledger legs exact:
>   killed-delta<=0 flips<=0)`, rc 0, tool `cf41efaa…`; workdir kept
>   `/tmp/w9-tameshi-t93/regression`.
>
> The legs replay their pinned blobs — git-materialized
> (`tools/mutate-and-run.sh:733-791`), so the two `stale` substrates cannot move
> them; re-verified at this boundary, since all four legs matched while cases 3–4
> read `stale`. Cases 5–6 are still not embedded: their rows carry no `REGRESSION`
> line — named debt, not smoothed (`fleet-kill-rate-ledger.md:282`).

## Pointers (every cited surface, checked against candidate bytes)

| ord | raw text (as cited) | resolves to | verdict | located excerpt / evidence |
|---|---|---|---|---|
| 0 | `tools/mutate-and-run.sh:733-791` (SKILL.md:1225) | tools/mutate-and-run.sh :733-791 | **absent at range — anchor rot** (range exists, cited content moved) | At CAND :731–753 is the bash-surface-census spec tail (`@defect B5…B10` heredoc, leg 2) and :755–791 the leg-3 comment + `cat >"$d/bash-tsukuroi-census.spec" <<'EOT'` with defects B1–B8 — leg-spec bytes, no materialization code. The cited content (the `regression_case()` git-materialization head) was exactly this range **at the pinned tool** `cf41efaa…` (verified: the runner blob at the section's writing revision b8eb96e hashes to `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`, and there :733 = `regression_case() {`, :770 = `git -C "$repo" show "${rev}:${path}"`, :786–791 = the pin-mismatch check). At CAND the function sits at **:1222–1402** (docstring :1223–1246 carries the same "pinned blob is materialized from that repo's git object store (`git show <rev>:<path>`)" sentence; repo-identity guard :1253–1263; `git_clean -C "$repo" show` :1276; exec-bit mirror :1294–1300; `REGRESSION_PIN … source=git` :1302; pin-mismatch SETUP :1314). Drift history: correct at b8eb96e (r9); stale since 606716f (r10, r10-2 leg 5); at r30 ColdB03 located it at :1154–1242; **the round-51 edit moved it again to :1222–1402** — the tenth-leg insertions land before the function. |
| 1 | `fleet-kill-rate-ledger.md:282` (SKILL.md:1228; no directory prefix; resolves to corpus/knowledge/) | corpus/knowledge/fleet-kill-rate-ledger.md :282 | **holds** | :282 = "- **Named follow-ups (not edits, not written here).** Cases 5/6 are not embedded in `--regression`: T8-2 E3 records the target pin / suite / spec for the tool's owner, and T8-1 U5 leaves the leg-cut decision to the same owner — rows 5/6 therefore carry no `REGRESSION` line over themselves. …" — exactly the "named debt, not smoothed" support the sentence cites. The ledger is **byte-identical base→CAND** (sha256 `13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e` at both revs), so the pointer holds unchanged. |
| 2 | `/tmp/w9-tameshi-t93/selftest.txt`, `/tmp/w9-tameshi-t93/regression.txt` (SKILL.md:1215–1216) | /tmp/w9-tameshi-t93/ | **absent** (ephemeral, expected) | `/tmp/w9-tameshi-t93/` does not exist on this host. Not lane files; the trace method never traces them. No other lane record of `t93` exists (grep over LOG.md and the ledger at CAND: nothing — the ledger's ER-4 tick used `/tmp/w9-tameshi-t91/`, :320). Known class: CR32 and Read18 both recorded the t93 evidence as ephemeral. |
| 3 | `/tmp/w9-tameshi-t93/regression` (SKILL.md:1222, "workdir kept") | /tmp/w9-tameshi-t93/regression | **absent** (ephemeral, expected) | Same t93 root; gone with it. Historical record of where the r9 run kept its workdir. |
| 4 | `cf41efaa…` (SKILL.md:1221, "tool …") | truncated sha256 of the runner blob at the tick | **holds as a record** | Full value recomputed: `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` = the runner blob at b8eb96e and 9f1d3c3 (r7-1 tool, 1 341 L / 61 632 B), matching the ledger's own pins (:281 "the harness at `cf41efaa8be5f52d…` (r7-1…)", :320 "Tool at the tick `cf41efaa8be5f52d…` …: **held**"). The live runner at CAND has a different sha (the round-51 edit); the receipt's sha is the tool **at the tick**, correctly scoped by "Run at the tick". |

## Claims checked against candidate bytes

1. **"`--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0"** — historical record of the
   r7-1 tool, corroborated by the ledger's own tick receipt (:341 "MUTATE_SELFTEST: 67/67 pass · VERDICT:
   PASS, rc 0"). **Not the current tally**: I ran `bash tools/mutate-and-run.sh --selftest` in the scratch
   clone at CAND (TMPDIR under scratch) → `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc 0; at base
   the same run prints `106/106`. Diffing the two case lists names the delta precisely: the leg-count arms
   went 9→10 (`calls=10 specs=10 nlegs=10 (want 10)`, `selftest leg tuples=10`) and one arm was added —
   `PASS embedded leg bash-drift-pins: spec and recorded table agree`. So the tenth leg added exactly one
   selftest case (106→107); the receipt's 67/67 stays a labeled historical record (the tool sha
   `cf41efaa…` sits in the same bullet).
2. **"`--regression` → 4 legs … (killed 8/8/6/4) … `REGRESSION: PASS (cases=4 passed=4; ledger legs exact:
   killed-delta<=0 flips<=0)`"** — historical record of the r9 tick, corroborated by ledger :281 (same
   REGRESSION string, "every leg `match=10/10 flips=0`"), :341 and :350 ("the tool embeds **4** legs —
   cases 5/6 … carry no `REGRESSION` line at `cf41efaa…`"). The killed counts match the recorded rates of
   legs 1–4 in the runner's leg table at CAND (:89–92: js-kimi-census 8/10, bash-surface-census 8/10,
   bash-tsukuroi-census 6/10, bash-mado-verify 4/10). **Not the current shape**: at CAND the runner wires
   **10** legs (leg table :88–98; `regression_case_git` calls :1459–1504; selftest leg-count arms want 10),
   and the C2 counter's own predicate requires `REGRESSION: PASS (cases=10 passed=10`.
3. **"The legs replay their pinned blobs — git-materialized …, so the two `stale` substrates cannot move
   them"** — the mechanism claim is **true of the candidate runner**: the materialization branch exists
   (pointer 0's "where content now lives") and the CAND selftest passes the drift-immunity arms verbatim:
   `PASS drifted working tree does not move a git-pinned leg`, `PASS drifted leg swept the pinned blob bytes
   (not the tree)`. The premise "all four legs matched while cases 3–4 read `stale`" is corroborated by
   ledger :333 ("Rows 3/4 are the two ER-3 already read `stale`") and :350 caveat (b).
4. **"Cases 5–6 are still not embedded: their rows carry no `REGRESSION` line — named debt, not smoothed"**
   — **split verdict.** Ledger-side half **holds at CAND**: ledger rows 5/6 (:276–277) contain no
   `REGRESSION` substring (the ledger's REGRESSION lines sit only at :88, :164, :196, :281, :282, :341,
   :350, :412, :435), and the ledger is byte-identical base→CAND. Runner-side clause **is superseded**:
   cases 5–6 (bash-checklist-run, js-claims-check) have been embedded since r10-2 (runner comments :850
   "r10-2 leg 5", :925 "r10-2 leg 6"; leg table :93–94; calls :1479/:1484; the ledger's own later leg table
   :387 records `bash-checklist-run` with its tool pin), so "still not embedded" is false of the runner at
   CAND — it narrates the r9 boundary (4 legs), where it was true. CR32 (r17) and Read18 (r27) flagged this
   exact sentence before me; the section still carries no supersession pointer, and the cited :282 is
   itself the r8 record that the later embedding superseded (the ledger recorded the growth in later ER
   entries without amending rows 5/6).
5. **Timestamps** — the section's `REGRESSION_DATE 2026-10-14T19:58:59Z` differs from ledger ER-4's
   `19:58:18Z` (:341), but the two receipts name different scratch roots (t93 vs t91, :320): two independent
   runs of the same command set on the same tool, consistent — ColdB03's finding, verified and carried
   forward.

## Strongest falsifier checked

Executed the receipt's own command against candidate bytes: `bash tools/mutate-and-run.sh --selftest` in a
`git clone --shared` scratch clone detached at CAND (toplevel asserted, TMPDIR under scratch) →
`MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc 0. This is the strongest falsifier because it tests
the section's only executable claim: the receipt's `67/67` is **not** the candidate tool's tally (and was
already not the base tally, 106/106) — the receipt survives only as a labeled historical record of the
`cf41efaa…` tool, which the ledger's :341 tick receipt independently corroborates at the same 67/67. The
same run doubles as a check that the round-51 runner edit kept the selftest green (C3's requirement) and
that the TMPDIR change is real (the run honored `TMPDIR`; a first attempt with a nonexistent TMPDIR failed
closed with `VERDICT: FAIL (mktemp)`, rc 1 — correct fail-closed behavior, not counted as a run).

Secondary falsifier: diffed the base vs CAND selftest case lists to name exactly what the tenth leg changed
(leg-count arms 9→10 + one new embedded-leg arm) — confirming no receipt-relevant behavior was silently
dropped.

## Findings by severity

- **Minor (known class, deepened by this round): anchor rot on `tools/mutate-and-run.sh:733-791`.** The
  range holds leg-spec heredoc bytes at CAND; the git-materialization code it cited moved to
  `regression_case()` :1222–1402. Correct at the pinned tool `cf41efaa…` (verified by recomputing that blob
  and reading :733/:770/:786–791 there); stale since r10; at :1154–1242 by r30 (ColdB03); the round-51 edit
  (+126/−47 before the function) moved it to :1222–1402. The mechanism claim itself remains true of the
  candidate runner and is still selftested. The lane's ER-jj2 cite-by-name precedent covers crediting the
  record with a stale anchor; the re-key row must carry the new location.
- **Minor (known class, still unamended): superseded present-tense narration.** "Cases 5–6 are still not
  embedded" is false of the runner at CAND (10 legs; those two are legs 5–6, embedded since r10-2) while its
  ledger-side half ("their rows carry no `REGRESSION` line") still holds byte-exactly. Previously flagged by
  CR32 and Read18; no supersession pointer has been added since. Not caused by the round-51 edit, but the
  tenth leg extends the same growth and the re-key would credit the sentence as-is.
- **Info (known class): ephemeral evidence.** `/tmp/w9-tameshi-t93/{selftest,regression}.txt` and the kept
  workdir are absent; no other lane record of t93 exists. Additionally, the runner now honors TMPDIR
  (runner :149–150 "r51 honours TMPDIR"; `${TMPDIR:-/tmp}` at :491/:1432/:1555), so a reader re-running the
  tick today gets TMPDIR-respecting scratch, not `/tmp/w9-*` — the section's paths are records of a
  pre-TMPDIR run.
- **Info: the four panel-tool updates (tally-audit.py, tally-audit-v2.py, tally-audit-v3.py,
  mte-interop.py) are not cited by this section** — its only runner pointer is :733-791, so the panel
  updates touch none of its anchors; their effect on this section is only the shared `input-drift` drop
  via the runner's bytes.
- **No wrong expectation found**: every checkable recorded value (67/67, 4 legs, killed 8/8/6/4,
  match=10/10 flips=0, the REGRESSION string, tool `cf41efaa…`, ledger :282's text) matches the ledger's
  records at CAND byte-for-byte or character-for-character; the two stale items above are anchor/narration
  currency, not record errors.

## reads.json row

```json
{
  "seat": "T51W2Read10",
  "heading": "### The receipt at this boundary",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "skill_md_span_at_cand": [1212, 1229],
  "next_heading_at_cand": "### The re-pin semantics, as executed (SKILL.md:1230)",
  "section_sha256_at_cand": "88f5a68550693f4b280c858fe6f259d6b376584bb13c8ec1b8afb81553611fbc",
  "section_bytes_unchanged_base_to_cand": true,
  "monitor_drop_reason": "input-drift:tools/mutate-and-run.sh (section bytes identical; runner changed 126/47)",
  "pointers": [
    {
      "ordinal": 0,
      "raw": "tools/mutate-and-run.sh:733-791",
      "file": "tools/mutate-and-run.sh",
      "ranges": [[733, 791]],
      "cited_for": "SKILL.md:1224-1225 'The legs replay their pinned blobs — git-materialized'",
      "verdict": "absent-at-range (anchor rot; content moved)",
      "located_excerpt": "CAND :731-753 = bash-surface-census spec @defect B5-B10 heredoc (leg 2 tail); :755-758 = 'r7-1 leg 3: tsukuroi …' comment; :759 = cat >\"$d/bash-tsukuroi-census.spec\" <<'EOT'; :760-791 = tsukuroi defects B1-B8. No materialization code in range.",
      "where_content_now_lives": "regression_case() tools/mutate-and-run.sh:1222-1402 (docstring :1223-1246; repo-identity guard :1253-1263; git show materialization :1276; exec-bit mirror :1294-1300; REGRESSION_PIN source=git :1302; pin-mismatch SETUP :1314)",
      "note": "Anchor correct at the pinned tool cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75 (runner blob at b8eb96e/9f1d3c3 recomputed; there :733 = 'regression_case() {', :770 = git show, :786-791 = pin check). Stale since r10 (606716f); at :1154-1242 by r30 (ColdB03); the round-51 edit moved it to :1222-1402. Mechanism claim itself true at CAND; selftest drift arms PASS."
    },
    {
      "ordinal": 1,
      "raw": "fleet-kill-rate-ledger.md:282",
      "file": "corpus/knowledge/fleet-kill-rate-ledger.md",
      "ranges": [[282, 282]],
      "cited_for": "SKILL.md:1227-1228 'Cases 5–6 are still not embedded: their rows carry no REGRESSION line — named debt, not smoothed'",
      "verdict": "holds",
      "located_excerpt": ":282 = '- **Named follow-ups (not edits, not written here).** Cases 5/6 are not embedded in `--regression`: T8-2 E3 records the target pin / suite / spec for the tool's owner, and T8-1 U5 leaves the leg-cut decision to the same owner — rows 5/6 therefore carry no `REGRESSION` line over themselves. …'",
      "note": "Ledger byte-identical base→CAND (sha256 13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e at both). Rows 5/6 (:276-277) contain no REGRESSION substring; the ledger's REGRESSION lines sit at :88/:164/:196/:281/:282/:341/:350/:412/:435 only."
    },
    {
      "ordinal": 2,
      "raw": "/tmp/w9-tameshi-t93/selftest.txt; /tmp/w9-tameshi-t93/regression.txt; workdir /tmp/w9-tameshi-t93/regression",
      "file": null,
      "ranges": null,
      "cited_for": "SKILL.md:1214-1216, 1222 'logs … ; workdir kept …'",
      "verdict": "absent (ephemeral /tmp scratch from the 2026-10-14 run; not lane files)",
      "located_excerpt": "/tmp/w9-tameshi-t93/ does not exist; no lane record of t93 outside this section (LOG.md and ledger at CAND grep clean; the ledger's ER-4 tick used /tmp/w9-tameshi-t91/, :320).",
      "note": "Known ephemeral-evidence class (CR32, Read18). The runner now honors TMPDIR (runner :149-150, :491, :1432, :1555), so a re-run today writes TMPDIR-respecting scratch, not /tmp/w9-*."
    },
    {
      "ordinal": 3,
      "raw": "cf41efaa…",
      "file": "tools/mutate-and-run.sh (blob sha256 at the tick)",
      "ranges": null,
      "cited_for": "SKILL.md:1221 'tool `cf41efaa…`'",
      "verdict": "holds as a record",
      "located_excerpt": "Full value cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75, recomputed as the runner blob sha256 at b8eb96e and 9f1d3c3 (r7-1, 1341 L / 61632 B); matches ledger :281 and :320 pins.",
      "note": "The live runner at CAND has a different sha (round-51 edit); the receipt's sha is the tool at the tick, scoped by 'Run at the tick'."
    }
  ],
  "claims_checked": [
    "selftest 67/67: historical r7-1 tally, corroborated by ledger :341 (t91 tick receipt, same 67/67); measured at CAND 107/107 PASS rc 0, at base 106/106 — the tenth leg added exactly one arm (leg-count arms 9→10 + 'PASS embedded leg bash-drift-pins: spec and recorded table agree')",
    "regression 4 legs / killed 8/8/6/4 / cases=4 passed=4: historical, corroborated by ledger :281/:341/:350; killed counts match legs 1-4 recorded rates in the CAND leg table (:89-92); at CAND the runner wires 10 legs (leg table :88-98, regression_case_git calls :1459-1504, selftest arms want 10; C2's predicate requires cases=10 passed=10)",
    "mechanism 'git-materialized … stale substrates cannot move them': true of the candidate runner (code at :1222-1402; selftest 'PASS drifted working tree does not move a git-pinned leg', 'PASS drifted leg swept the pinned blob bytes (not the tree)'); premise 'all four legs matched while cases 3-4 read stale' corroborated by ledger :333/:350",
    "'Cases 5–6 are still not embedded': split — ledger-side half holds (rows 5/6 carry no REGRESSION line, ledger unchanged); runner-side clause superseded (embedded since r10-2: runner :850/:925 comments, leg table :93-94, calls :1479/:1484, ledger :387 leg row); flagged before by CR32 and Read18; no supersession pointer added",
    "REGRESSION_DATE 19:58:59Z vs ledger ER-4 19:58:18Z: two independent runs (t93 vs t91 scratch roots), consistent — ColdB03's finding verified and carried forward"
  ],
  "strongest_falsifier": "Ran 'bash tools/mutate-and-run.sh --selftest' in a --shared scratch clone detached at CAND (toplevel asserted, TMPDIR under scratch): MUTATE_SELFTEST: 107/107 pass / VERDICT: PASS, rc 0 — the receipt's 67/67 is not the candidate tool's tally (base 106/106), so the receipt survives only as a labeled historical record of the cf41efaa… tool, independently corroborated by ledger :341. A first attempt with a nonexistent TMPDIR failed closed (VERDICT: FAIL (mktemp), rc 1) — correct behavior, not counted as a run. Also diffed base vs CAND selftest case lists to name the tenth leg's exact delta.",
  "verdict": "record stands; re-keyable — both lane-file pointers resolve to real bytes, the ledger line holds byte-exactly, and the mechanism claim is true of the candidate runner; two known-class residuals (runner anchor rot deepened by this round's edit to :1222-1402; the superseded 'still not embedded' narration) plus the ephemeral-/tmp and labeled-historical-count notes",
  "seat_name": "T51W2Read10"
}
```

## Bounds and cleanup

Read-only on the lane (all reads via `git show` or the `--shared` scratch clones at
`/fast/scratch/hyaku/tameshi-r51/T51W2Read10/`); the only writes are this report. Scratch (two clones,
selftest outputs, tmp dirs) deleted before yield. No tools installed; no `/tmp` use beyond the absent-path
check. No git/jj mutations anywhere.
