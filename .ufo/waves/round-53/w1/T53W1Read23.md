# T53W1Read23 — cold read of `### The receipt at this boundary`

- **Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read via git objects only)
- **Content commit C\* (cand):** `a41195dfc13a73958e4c5228ec196b28d03ded03`
- **Heading:** `### The receipt at this boundary`
- **Section span at C\*:** lines 1214–1230 (heading 1214, next heading 1232; the single blank line 1231 is stripped by the splitter)
- **Section sha256:** `a44eec946e9adcfcb8f864f89b2f4de3925614ace891edea212dca7d951ca90e`
- **Findings:** none (`findings: []`) — every statement I could check resolves at C\*.

## Section text at C\* (verbatim)

```
### The receipt at this boundary

Run at the tick (this lane; `--selftest` 19:58:49Z, `--regression`
`REGRESSION_DATE 2026-10-14T19:58:59Z`; logs `/tmp/w9-tameshi-t93/selftest.txt`,
`/tmp/w9-tameshi-t93/regression.txt`):

- `--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0.
- `--regression` → 4 legs, each `match=10/10 … flips=0` (killed 8/8/6/4),
  closing `REGRESSION: PASS (cases=4 passed=4; ledger legs exact:
  killed-delta<=0 flips<=0)`, rc 0, tool `cf41efaa…`; workdir kept
  `/tmp/w9-tameshi-t93/regression`.

The legs replay their pinned blobs — git-materialized
(`tools/mutate-and-run.sh:1222-1303`), so the two `stale` substrates cannot move
them; re-verified at this boundary, since all four legs matched while cases 3–4
read `stale`. Cases 5–6 were not yet embedded at this boundary (they became legs 5–6 at r10-2; the current tool carries them at `tools/mutate-and-run.sh:88-97`): their rows carried no `REGRESSION`
line at this boundary — named debt, not smoothed (`fleet-kill-rate-ledger.md:282`; the debt was retired when the legs embedded).
```

## Checks run

1. **Section split reproduced with the frozen splitter, not hand-rolled.** I read
   `.ufo/evidence/round-18/measure.py` from the C\* blob, imported its `sectionize()`, and
   fed it the C\* `SKILL.md` blob bytes:

   ```
   $ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
       a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md   # 2178 lines
   sectionize -> 64 sections
   {'start': 1214, 'end': 1231, 'heading': '### The receipt at this boundary',
    'sha256': 'a44eec946e9adcfcb8f864f89b2f4de3925614ace891edea212dca7d951ca90e'}
   ```

   The splitter's own contract (round-18 `measure.py:209-253`) matches the wave spec: heading
   line through the line before the next heading, trailing whitespace-only lines stripped,
   `\n`-joined, no trailing newline, sha over surrogateescape UTF-8 bytes. The heading occurs
   exactly once in the file at C\*, so the range is unambiguous.

2. **Pointer `tools/mutate-and-run.sh:1222-1303` (git-materialized replay) — holds.**
   At C\* `tools/mutate-and-run.sh` is 2159 lines. Line 1222 is `regression_case() {`; the
   comment block (1223–1241) states the `git show <rev>:<path>` materialization and the
   `100755 -> +x` mode mirror; the code does exactly that:

   ```
   1276:  if ! git_clean -C "$repo" show "${rev}:${path}" >"$dst" 2>"$cwd/git-show.err"; then
   1285:  if ! blob_mode=$(git_clean -C "$repo" ls-tree "$rev" -- "$path" | awk '{print $1}'); then
   1295:  if [[ "$blob_mode" == 100755 ]]; then
   1302:  printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s\n' \
   ```

   The range ends at 1303, i.e. it covers the materialization and the pin provenance line and
   stops before the tolerance/pin-check body (1307+). The legs reach this code through
   `regression_case_git()` (1404–1415), which passes `repo`/`rev`/`path` and tolerance `0 0`.

3. **Pointer `tools/mutate-and-run.sh:88-97` (the current tool carries cases 5–6) — holds.**
   Lines 84–97 are the recorded-kill-rate comment table for `--regression`; the rows at 88–97
   name all ten legs, including `bash-checklist-run` (line 92) and `js-claims-check` (line 93)
   in positions 5 and 6. The leg invocations themselves sit at 1479 and 1484 in that same
   order, so `:88-97` genuinely indexes the two cases the sentence is about.

4. **Pointer `fleet-kill-rate-ledger.md:282` (named debt, not smoothed) — holds.**
   The file resolves at C\* as `corpus/knowledge/fleet-kill-rate-ledger.md` (441 lines; no
   root-level copy exists — bare-name citation is this document's standing convention, cf.
   SKILL.md:998, 1084, 1242). Line 282 reads, in the ER-2 errata block: cases 5/6 are not
   embedded in `--regression`, rows 5/6 "therefore carry no `REGRESSION` line over themselves".
   The two rows it names (276–277) contain no `REGRESSION` token
   (`awk 'NR==276||NR==277' | grep -c REGRESSION` → `0`).

5. **"4 legs, each `match=10/10 … flips=0` (killed 8/8/6/4)" — holds against the ledger's own
   tick record.** ER-4 (`corpus/knowledge/fleet-kill-rate-ledger.md:341-348`) records the
   four-leg run at `cf41efaa…` with sweeps 8/10, 8/10, 6/10, 4/10 and `match=10/10 … flips=0`
   per leg, closing
   `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0.
   The quoted closing form is the tool's own printf template at C\* (`:1540`, and the ten-leg
   self-check expectation at `:2087`), so it is not a paraphrase dressed as a receipt.

6. **"the two `stale` substrates cannot move them … cases 3–4 read `stale`" — holds.**
   ER-4's pin read (`:328-329`, headline `:333`) reads row 3 (tsukuroi, `084951be…` →
   `bba6cdf6…`) and row 4 (mado, `d7edaab4…` → `7da4ec50…`) as **stale**, while the leg table
   (`:345-348`) shows all four legs PASS. That is exactly the claim: a materialized leg replays
   the pinned blob, not the live file (tool comment `:1228` — "A drifted tree cannot move it").

7. **"became legs 5–6 at r10-2" — holds.** The tool's own header at C\* records the leg-count
   history `r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten`
   (`:84`) and the cut record naming cases 5/6 as that round's work (`:12, :27`).

8. **`MUTATE_SELFTEST: 67/67 pass` — corroborated, not contradicted.** The count is also the
   figure ER-4 records for the tick (`:341`) and it appears in the committed round-18 cold-read
   traces at C\* (`.ufo/evidence/round-18/coldread/traces/CR18/4.out.txt:68`).

## Observations that are not findings (dated receipts)

- **The `/tmp/w9-tameshi-t93/` receipts are gone.** `ls -la /tmp/w9-tameshi-t93` →
  `No such file or directory`. The section is an explicitly dated record ("at the tick",
  `19:58:49Z`, `REGRESSION_DATE 2026-10-14T19:58:59Z`, workdir "kept"), so absence today is
  the expected fate of a `/tmp` receipt, not a false statement; per the findings discipline a
  dated milestone is a hold. Nothing in the section *instructs* a reader to place scratch under
  `/tmp`, so there is no scratch-directive violation to report either (the host directive is
  stamped 2026-10-25, after this 2026-10-14 run).
- **Two runs at one boundary.** The section's scratch root (`/tmp/w9-tameshi-t93/`) differs
  from ER-4's tick root (`/tmp/w9-tameshi-t91/regression`, `:320`) and its `REGRESSION_DATE`
  (`19:58:59Z`) differs from ER-4's (`19:58:18Z`). Both records agree on `67/67`, four legs,
  and the exact-band close, so I read this as a second run by this lane at the same boundary,
  which is the disposition round 52 already recorded (`T52W2Fix12.md:66`). The adjacent section
  at C\* carries that annotation at SKILL.md:1169; this section does not, but the statement it
  makes is about its own run, so I do not treat it as failing.
- **`cf41efaa…` is a text pin, not a resolvable object here.**
  `git rev-list --objects --all | grep -c '^cf41efaa'` → `0` in this lane. The prefix names the
  harness copy as ER-2 (`:281`) and ER-4 (`:320`) also record it (`cf41efaa8be5f52d…`, 1 341 L
  / 61 632 B, r7-1); the pointer is corroborated in prose, which is all the section claims.

## Limits

- The clock stamps (`19:58:49Z`, `19:58:59Z`) have no surviving machine record; I did not run
  the tool (read-only seat), so the numbers themselves were only cross-checked against the
  ledger's independent record of the same tick.
- `tools/mutate-and-run.sh:1222-1303` is correct at C\*; it was **not** correct at the tick tool
  `cf41efaa…`, where round-18 CR25 recorded the same mechanism at `:733-791` and the anchor
  `:1079ff` at that round's read rev. The sentence is present-tense about the repo's current
  tool, so the mixed revision is a scope note, not a failure.
- Scratch (`/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read23/`, holding the extracted
  `SKILL.md`, `tools/mutate-and-run.sh`, `corpus/knowledge/fleet-kill-rate-ledger.md`, and the
  imported `measure.py`) was removed before this report was finalized.
