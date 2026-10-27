# T53W1Read27 — cold read of `### The tick, executed`

Seat T53W1Read27, wave 1, round 53. Content commit C* = `a41195dfc13a73958e4c5228ec196b28d03ded03`.
Read entirely through git objects (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C*:<path>`); the working tree was never read for section text.

**Findings: none (`"findings": []`).** Nothing in this section fails at C*. The section is a dated record (round-9 tick, 2026-10-14) and every substantive claim either resolves at C* or is a timestamped observation whose limits are already stated in the text. What remains are dated-record artifacts (cleaned `/tmp` scratch, a moved harness sha), listed under limits below — none of them a statement that does not hold at C*.

## Section identity

Section bytes were taken from the frozen round-18 `sectionize` (`.ufo/evidence/round-18/measure.py`, extracted at C* and imported), never a reimplementation of the split rule:

```
$ git show C*:.ufo/evidence/round-18/measure.py > <scratch>/r18measure.py
$ python3 -c "import importlib.util,...; mod.sectionize(open('<scratch>/SKILL.md','rb').read())"
[{'start': 1166, 'end': 1213, 'heading': '### The tick, executed',
  'sha256': 'd58978b5611e65939b188704ce32de562ddce854885aee7a85cb24858707b2f0'}]
```

- Heading line at C*: 1166 (`### The tick, executed`); next heading line: 1214 (`### The receipt at this boundary`).
- Section = lines 1166–1212 after stripping the whitespace-only trailing line 1213; 47 lines, 3 551 bytes, no trailing newline.
- `section_sha256` = `d58978b5611e65939b188704ce32de562ddce854885aee7a85cb24858707b2f0` (also reproduced byte-for-byte by an independent split: heading match checked outside ``` fences, `SKILL.md` has 64 headings and `git show C*:SKILL.md | wc -l` = 2178).

## Holds — verified against C* bytes

1. **The PID-table vs the harness constants.** All six rows of the fenced pin-read table carry values that are still the harness's own `PIN_*`/`REV_*` at C* (`git show C*:tools/mutate-and-run.sh`):
   - `PIN_JS=83016d45…`, `REV_JS=175de6ba…` (js-kimi-census: `175de6ba / 83016d45`);
   - `PIN_BASH=275d8294…`, `REV_BASH=fecee874…` (bash-surface-census);
   - `PIN_TSUKUROI=084951be…`, `REV_TSUKUROI=165307fe…` (bash-tsukuroi-census);
   - `PIN_MADO=d7edaab4…`, `REV_MADO=eead56b2…` (bash-mado-verify);
   - `PIN_CHECKLIST=7e5ec98b…`, `REV_CHECKLIST=fecee874…` (kagi-checklist-run);
   - `PIN_CLAIMS=e9a21b44…`, `REV_CLAIMS=175de6ba…` (kumitate-claims-check).
2. **Line pointer `tools/mutate-and-run.sh:614-633` resolves at C*.** Line 614 is `PIN_JS=…`, line 632 `PIN_DRIFTPINS=…`, line 633 `REV_DRIFTPINS=…`; the range holds exactly ten `PIN_*`/`REV_*` pairs, so "ten legs since round 51" matches the file (the tool's own header, line 84, reads `(r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten)`) and `run_regression` declares `local nlegs=10 …` with ten `regression_case_git` calls, including `bash-checklist-run` and `js-claims-check`.
3. **"the r8 notes' pins for cases 5–6"** — the two pins still resolve in the two case notes at C*: `corpus/knowledge/mutation-case-kagi-checklist.md:22` carries `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf`; `corpus/knowledge/mutation-case-kumitate-claims.md:12` carries `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`.
4. **The pins resolve at their recorded revisions in the sibling object stores** (read-only `git -C <sibling> show <rev>:<path> | sha256sum`):
   `kumitate@175de6ba:scripts/kimi-census.mjs → 83016d45`;
   `kagi@fecee874:corpus/surface-census.sh → 275d8294`;
   `tsukuroi@165307fe:tools/tsukuroi-census.sh → 084951be`;
   `mado@eead56b2:tools/mado-verify.sh → d7edaab4`;
   `kagi@fecee874:corpus/checklist-run.sh → 7e5ec98b`;
   `kumitate@175de6ba:scripts/claims-check.mjs → e9a21b44`.
5. **The two `stale` cells and the two `live` blobs.** `tsukuroi@72b038da:tools/tsukuroi-census.sh → bba6cdf6`; `mado@12c8f08a:tools/mado-verify.sh → 7da4ec50`; the round-8 mado tip named in the "90d50cdd… (clean)" clause resolves too: `mado@0c20a76f:tools/mado-verify.sh → 90d50cdd`. The `anc yes` column is real: `git -C tsukuroi-shokunin merge-base --is-ancestor 165307fe 72b038da` exit 0; the same for `mado eead56b2 12c8f08a` exit 0.
6. **ER-4 pointer `corpus/knowledge/fleet-kill-rate-ledger.md:318-353`.** Line 318 is the ER-4 heading (`**ER-4 — the cadence fires its first scheduled tick: …`); line 353 is ER-4's closing paragraph ("What this tick closes…"); line 354 is the `New errata entries go below this one.` separator. Range correct at C*.
7. **`fleet-kill-rate-ledger.md:320`** carries the scratch the round-52 bracket attributes to ER-4: `Scratch `/tmp/w9-tameshi-t91/`` (with `pin-read.log` as "the raw six-case read, second pass 20:00:29Z"), so the bracket's statement that ER-4's record names `/tmp/w9-tameshi-t91/` holds.
8. **The quoted ER-4 phrase.** `second raw pass 20:00:29Z, same readings` is a byte-exact substring of ledger line 322 (`*Pin read (executed at the tick, 19:58Z; second raw pass 20:00:29Z, same readings):*`). The section's claim that ER-4 reproduces the same six-case read is consistent: the ledger's six-row table (lines 324-331) matches the section's table row for row, its headline is `LEDGER: 6 cases in; target current=4 stale=2 drift=0; tool held (cf41efaa…)`, and both drift chains (`084951be… → bba6cdf6…`, `d7edaab4… → 7da4ec50…`) appear at lines 337-338.
9. **`fleet-kill-rate-ledger.md:358-359`** carries exactly the shas the bracket names — line 358 `5d16378d…` (tsukuroi worktree, mtime 20:02:42Z), line 359 `5b6ace8e…` (mado worktree, mtime 20:02:38Z) — and the addendum heading is line 356, so the `:354-360` pointer encloses the addendum's heading and both shas (it starts one line early, at the errata separator on 354; the continuation it is cited for is inside the range, so the statement holds).
10. **"five minutes later".** The two round-8 stamps this clause leans on are `2026-10-14T19:15:14Z` (round-8 tick) and `19:20:29Z` (its re-read) — 5 min 15 s, so the repaired "five minutes later" is the accurate statement (the older text said "six minutes later").
11. **Host.** `hostname` prints `plazir27`, matching "host `plazir27`".
12. **Counts and scoping.** `4 × current · 2 × stale · 0 × drift` matches the six rows; "all four sibling trees porcelain-clean (0 lines each) *at the tick*" matches ER-4's "Sibling trees read-only, clean before and after (kumitate `175de6b` · kagi `fecee87` · tsukuroi `72b038d` · mado `12c8f08`)"; "the same regression outcome" matches both records' `REGRESSION: PASS (cases=4 passed=4; …)`; "provenance fields differ (scratch root, `REGRESSION_DATE`)" matches `/tmp/w9-tameshi-t91/` + `19:58:18Z` (ER-4) against `/tmp/w9-tameshi-t93/` + `19:58:59Z` (this lane's receipt).
13. **The falsifier's logic re-derives.** With js-kimi-census's pin replaced by `084951be` and its recorded revision left at `175de6ba` (an ancestor of the tip, tip blob `83016d45`), the recorded pin no longer equals the tip blob → `stale`, while the row as recorded reads `current`. The conclusion "the reading follows the row's pin, not the substrate's history" is consistent with the reading table above it.

## Limits (stated, not promoted to findings)

- **Scratch named by the record is gone.** `/tmp/w9-tameshi-t93` and `/tmp/w9-tameshi-t91` do not exist at C* (`ls -d` → "No such file or directory"), so `pin-read-final.txt`, the `falsifier/` copy, `selftest.txt`/`regression.txt` and ER-4's `pin-read.log` are not re-runnable. The section is explicitly dated ("Pin read at the round-9 boundary, **2026-10-14T20:00:34Z**"), and a dated record's `/tmp` file not surviving is not a false statement; it is a verification limit, and the round-27 cold read already logged it as a minor gap (0 wrong expectations).
- **The harness moved.** `sha256sum` of the C* blob of `tools/mutate-and-run.sh` is `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda` (2 159 L, 112 407 B), not the `cf41efaa…` of the tick. "tool **held** at `cf41efaa…`" is a `held`/`moved` reading against the last recorded run — true at the tick, and the preceding section at C* already records the runner's move to `977de470…`. Read as the dated reading it is, it holds; the parenthetical `(sha256sum tools/mutate-and-run.sh)` is an unscoped recipe and now returns the other sha.
- **Lineage wording.** "that in-flight edit resolved into the committed `7da4ec50…`" mirrors ER-4's own wording ("resolved into the committed `7da4ec50`") rather than claiming byte identity; the round-8 in-flight file was `dc864c6a` (99 716 B) and the committed blob is 131 612 B, so the sentence reads as lineage, which is what the ledger records.
- **Not re-observable:** the 19:58Z/20:00:34Z reads, the 20:03:34Z worktree shas (`b54f5732`, `31364115`), and the sibling trees' cleanliness at the tick; they rest on ER-4 and on git objects. The two `stale` tips have moved since the tick, so no current-state reading is claimed here.

## Process

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read27/` (blobs extracted with `git show C*:<path>`; `SKILL.md`, `ledger.md`, `mutate-and-run.sh`, `SKILL2227.md` for a 2227d-vs-C* diff of the section, `section.txt`, `r18measure.py`). Deleted after the final check (`rm -rf -- <dir>`); `ls -d` confirms it is absent.
- Writes: only `.ufo/waves/round-53/w1/T53W1Read27.json` and `.ufo/waves/round-53/w1/T53W1Read27.md`.
- Read-only sibling access: `git -C <sibling> show/merge-base/cat-file` only; no git or jj mutation anywhere, no commit/fetch/prune, no writes outside the two deliverables.
- Tools installed: none (git, python3, sha256sum already present). No pacman, no network.
