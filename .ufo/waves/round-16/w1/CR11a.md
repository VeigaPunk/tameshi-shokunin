# CR11a — cold-read report: SKILL.snapshot.md lines 527–593 (Appendix A, JS case)

Seat: `TameshiR16.CR11a` · Lane: tameshi-shokunin · Wave: round-16/w1
Scratch: `/tmp/tameshi-r16-CR11a-work/` (all artifacts below live there)

## Snapshot verification

- `cp .ufo/evidence/round-16/coldread/SKILL.snapshot.md → /tmp/tameshi-r16-CR11a-work/SKILL.snapshot.md`
- `sha256sum` → `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` — **matches declared pin**.
- Heading scan of range: only heading is line 527 `## Appendix A — worked example: JS case (reproduce from this page alone)`; next heading is line 594 (Appendix B, out of range). Section classified **instruction** — the page is a reproduction recipe ("Commands (order matters)", "Driver contract (write from this spec)", manifest, expected results).

## Execution (cold reader, no oral context)

### Pin check — caught real substrate drift

- Live working tree: `sha256sum kumitate-shokunin/scripts/kimi-census.mjs` → `5e8d5913…6db3dc0` (922 lines, 44770 B), HEAD `1770305fae20826b39905a8251ddeca6b4957ac4`. **Differs from pinned `83016d45…4f426` / 896 lines / 43273 B / rev `175de6ba`.**
- `git -C kumitate-shokunin cat-file -t 175de6ba` → `commit`; `git show 175de6ba:scripts/kimi-census.mjs | sha256sum` → `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, 896 lines / 43273 B — **pinned blob verified**.
- The page's "verify before copying" clause is exactly what saves the reader: the command block's `cp -p kumitate-shokunin/scripts/kimi-census.mjs` would silently copy the drifted file. I materialized via `git show` → `pristine.mjs` (sha re-verified). `git status --porcelain -- scripts/kimi-census.mjs` → empty (clean, exit 0).

### Control

- `node pristine.mjs --selftest` → `KIMI_CENSUS_SELFTEST: 43/43 pass`, `VERDICT: PASS`, exit 0. Matches expected control.

### Driver

- Wrote `/tmp/tameshi-r16-CR11a-work/mutate_driver.py` solely from the page's "Driver contract" paragraph + manifest (D4 U+2013 en-dash and real newlines honored). Contract ambiguities resolved by inference: `fails` recorded as FAIL-prefixed case lines; `summary` as `n/43`.
- `python3 mutate_driver.py --check` → `occurrences=1` for all 10 defects, `CHECK: all unique`, exit 0 — **uniqueness gate holds on the pinned blob**.

### Sweep — verdict table reproduction

`python3 mutate_driver.py --run` (control first, 300 s timeouts, evidence/ written). Observed vs page's recorded table:

| id | recorded | observed | match |
|----|----------|----------|-------|
| D00-control | 43/43 PASS | 43/43 PASS exit 0 | ✓ |
| D1 | 27/43 FAIL (16) | 27/43 FAIL, 16 FAIL cases | ✓ |
| D2 | 43/43 PASS survivor | 43/43 PASS survivor | ✓ |
| D3 | 27/43 FAIL (16) | 27/43 FAIL, 16 cases | ✓ |
| D4 | 40/43 FAIL (3) | 40/43 FAIL, 3 cases | ✓ |
| D5 | 42/43 FAIL (1) | 42/43 FAIL, 1 case | ✓ |
| D6 | 41/43 FAIL (2) | 41/43 FAIL, 2 cases | ✓ |
| D7 | 41/43 FAIL (2) | 41/43 FAIL, 2 cases | ✓ |
| D8 | 40/43 FAIL (3) | 40/43 FAIL, 3 cases | ✓ |
| D9 | 41/43 FAIL (2) | 41/43 FAIL, 2 cases | ✓ |
| D10 | 43/43 PASS survivor | 43/43 PASS survivor | ✓ |

**8/10 killed — exact match to recorded outcome.** Sweep wall time 7.14 s ("runs in seconds" ✓). Per-mutant stdout in `evidence/<id>.selftest.txt`, metadata in `evidence/<id>.meta.json`, aggregate `evidence/results.json`.

### Survivor probes (off-suite observability)

- `node mutant-D2.mjs --root empty-root` → last line `KIMI_CENSUS: DRIFT (MEMBER_MISSING … skills/; +23 more)` — 5 ids + `+23 more`, node exit 1. Pristine contrast: 6 ids + `+22 more`. **D2 observably different off-suite.**
- `node mutant-D10.mjs --root empty-root | grep 'FAMILY K2'` → `frozen=24`; pristine → `frozen=25`. **D10 observably different.**

### Restore proof

- `sha256sum pristine.mjs` post-sweep → `83016d45…4f426`, size 43273 unchanged.
- `git -C kumitate-shokunin status --porcelain -- scripts/kimi-census.mjs` → empty (substrate untouched, read-only).

## Findings

1. **Minor gap (non-blocking):** working-tree `cp -p` in the commands block would copy the drifted 922-line file if the reader skipped the pin-verify clause. The page does say "verify before copying" and names the recovery path (re-derive manifest / re-anchor), so this is survivable — but on this host today the naive copy **fails**. Recommendation for L1: consider `git show <rev>:<path>` as the canonical materialization line.
2. **Driver-contract ambiguity (inference, named):** `fails` semantics unstated; FAIL-prefixed case lines reproduce the recorded parenthetical counts exactly (16/16/3/1/2/2/3/2).
3. **Named-but-unopened reference:** `mutation-case-kimi-census.md` is cited for provenance; the page itself contains the full expected table, so cross-checking the note was unnecessary for reproduction. Not opened (not needed to proceed).
4. No wrong expectations: every recorded number (43/43, 8/10, per-mutant counts, survivors, +23 more, frozen=24, restore pin) reproduced byte-for-byte or count-for-count.

## Recommendations (bounded)

- L1: ledger entry for section 527 → `instruction` / `executed-ok` with `minor_gaps=1` (the cp-vs-git-show drift footgun, item 1).
- Consider adding a live-sha note in Appendix A so future readers expect drift and go straight to `git show`.

## Files opened (complete)

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/SKILL.snapshot.md` (lines 527–593 read in full; heading scan only outside)
- `git show 175de6ba:scripts/kimi-census.mjs` in `/home/vgpnk/Projects/shokunin/kumitate-shokunin` (read-only, via git plumbing; content to `pristine.mjs`)
- `git status` / `sha256sum` / `wc` on `kumitate-shokunin/scripts/kimi-census.mjs` (metadata only)

No lane files outside scratch were written except this report. No tools installed (none needed).

```json
{"seat":"CR11a","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[{"start":527,"heading":"## Appendix A — worked example: JS case (reproduce from this page alone)","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["commands block uses `cp -p` of the working-tree file; live tree has drifted (922 lines, sha 5e8d5913…) vs pinned blob (896 lines, sha 83016d45…) — only the 'verify before copying' clause prevents a silent wrong-substrate run; materializing via `git show 175de6ba:scripts/kimi-census.mjs` works and reproduces every recorded number","driver contract leaves `fails` semantics unstated; inferred FAIL-prefixed case lines, which exactly reproduce recorded parenthetical counts"],"commands_executed":["cp snapshot to /tmp + sha256sum (97cf436b… match)","sha256sum/wc/git rev-parse/git status --porcelain on kumitate-shokunin/scripts/kimi-census.mjs (drift detected, status clean)","git -C kumitate-shokunin show 175de6ba:scripts/kimi-census.mjs > pristine.mjs (83016d45…, 896L/43273B)","node pristine.mjs --selftest → 43/43 PASS exit 0","python3 mutate_driver.py --check → all 10 occurrences=1, CHECK: all unique, exit 0","python3 mutate_driver.py --run → D00-control 43/43 PASS; D1 27/43; D2 43/43 survivor; D3 27/43; D4 40/43; D5 42/43; D6 41/43; D7 41/43; D8 40/43; D9 41/43; D10 43/43 survivor; 8/10 killed; 7.14s","node mutant-D2.mjs --root empty-root → last line 5 ids + '+23 more', exit 1 (pristine: 6 ids + '+22 more')","node mutant-D10.mjs --root empty-root | grep 'FAMILY K2' → frozen=24 (pristine: 25)","sha256sum pristine.mjs post-sweep → 83016d45…4f426, size 43273 unchanged; git status --porcelain clean"],"opened":["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/SKILL.snapshot.md","kumitate-shokunin/scripts/kimi-census.mjs via git show rev 175de6ba (read-only)"],"scratch":"/tmp/tameshi-r16-CR11a-work"}]}
```
