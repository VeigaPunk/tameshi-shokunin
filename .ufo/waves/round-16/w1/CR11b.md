# CR11b — cold-read, SKILL.md lines 527–593 (Appendix A: JS case)

Snapshot `/tmp/tameshi-r16-CR11b/SKILL.snapshot.md`, sha256 verified:
`97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` (matches).

Range contains exactly one section heading:
`527:## Appendix A — worked example: JS case (reproduce from this page alone)`
(next heading at 594 = Appendix B, out of range).

## Classification

Section is **instruction** — a complete reproduction recipe: artifact pin,
command block, driver contract, exact-string manifest, expected results,
post-run integrity checks. Executed as a reader with no oral context.
No oral context was needed end-to-end.

## Environment / preconditions

- node v24.21.0, python3 3.14.8 (host already provisioned; no installs needed).
- Work dir `/tmp/tameshi-r16-CR11b/work` (page pattern `/tmp/<lane>-r<round>-<n>-work`).

## Deviations exercised by the page itself

1. **Worktree blob drifted.** Page pins `kumitate-shokunin/scripts/kimi-census.mjs`
   sha256 `83016d45…4f426`, 896 lines, 43273 B, rev `175de6ba`, clean status.
   Observed: worktree HEAD is `1770305fae2082…`; worktree file sha256 is
   `5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0`,
   922 lines, 44770 B; `git status --porcelain -- scripts/kimi-census.mjs`
   prints empty (file is committed, not dirty — the pin's "status empty"
   check passes but the blob no longer matches). The page names exactly this
   contingency ("A differing sha means the substrate moved… re-anchor to the
   note"). Re-anchored via `git -C kumitate-shokunin show 175de6ba:scripts/
   kimi-census.mjs` → sha256 `83016d45049b009a6c9868dc392ff6ebcecb357c
   9abfe423f476459f2724f426`, 896 lines, 43273 B — exact pin match.
   A reader who runs the literal `cp -p kumitate-shokunin/scripts/kimi-census.mjs`
   today would copy the wrong blob; the `sha256sum` guard on the next line
   catches it. Minor gap only because the remedy is one `git show` away and
   the page warns "verify before copying".

## Execution evidence

- `cp -p` pinned blob → `sha256sum pristine.mjs` → `83016d45…4f426` ✓
- `node pristine.mjs --selftest` → `KIMI_CENSUS_SELFTEST: 43/43 pass`,
  `VERDICT: PASS`, exit 0 ✓ (control)
- Driver written from the page's contract spec (check/run modes, unique
  replacement, `new != old`, 300 s timeout, `evidence/<id>.selftest.txt`,
  `evidence/<id>.meta.json` with sha256/exit/duration/summary/verdict/fails,
  `D00-control` first, `evidence/results.json` aggregate). File:
  `/tmp/tameshi-r16-CR11b/work/mutate_driver.py`.
- `python3 mutate_driver.py --check` → all 10 `occurrences=1`, final line
  `CHECK: all unique`, exit 0 ✓ (en-dash U+2013 in D4 and the
  `return 2;\n` in D8 both unique).
- `python3 mutate_driver.py --run` → exit 0, wall 7.79 s (page: "7.0 s",
  close enough; host difference, not a finding).

### Observed vs expected per-mutant results

| id | expected | observed | match |
|----|----------|----------|-------|
| control | 43/43 PASS | 43/43 PASS exit 0 | ✓ |
| D1 | 27/43 FAIL (16) | 27/43 FAIL exit 1 | ✓ |
| D2 | 43/43 PASS survivor | 43/43 PASS exit 0 | ✓ |
| D3 | 27/43 FAIL (16) | 27/43 FAIL exit 1 | ✓ |
| D4 | 40/43 FAIL (3) | 40/43 FAIL exit 1 | ✓ |
| D5 | 42/43 FAIL (1) | 42/43 FAIL exit 1 | ✓ |
| D6 | 41/43 FAIL (2) | 41/43 FAIL exit 1 | ✓ |
| D7 | 41/43 FAIL (2) | 41/43 FAIL exit 1 | ✓ |
| D8 | 40/43 FAIL (3) | 40/43 FAIL exit 1 | ✓ |
| D9 | 41/43 FAIL (2) | 41/43 FAIL exit 1 | ✓ |
| D10 | 43/43 PASS survivor | 43/43 PASS exit 0 | ✓ |
| total | 8/10 killed | 8/10 killed | ✓ |

### Survivor probes (off-suite observability)

- `node mutant-D2.mjs --root empty-root | tail -1` →
  `KIMI_CENSUS: DRIFT (MEMBER_MISSING config.toml; MEMBER_MISSING tui.toml;
  MEMBER_MISSING config.toml.*.bak; MEMBER_MISSING agents/secondary/;
  MEMBER_MISSING skills/; +23 more)` — exactly 5 ids + "+23 more",
  node exit 1 ✓
- `node mutant-D10.mjs --root empty-root | grep 'FAMILY K2'` →
  `FAMILY K2  members=0  checked=0  frozen=24` ✓ (mutated 25→24 observable)

### Post-run integrity

- `sha256sum pristine.mjs` → still `83016d45…4f426`; size 43273, mtime
  unchanged (cp -p preserved from pinned materialization) ✓
- `git -C kumitate-shokunin status --porcelain -- scripts/kimi-census.mjs`
  → empty ✓ (substrate untouched; all writes in /tmp)
- Evidence tree: 11 selftest.txt + 11 meta.json + results.json under
  `$W/evidence/` ✓

## Findings

- **wrong-expectation (host-level, predicted by the page):** the kumitate
  worktree blob no longer equals the pin; the page's own drift contingency
  covers it. Reported as a data point for ledger consumers: the `cp -p`
  command line as written now fails the very next `sha256sum` guard.
- All measured numbers (43/43 control, 8/10, D2/D10 survivors, every
  per-mutant pass count, probe output shapes) reproduce exactly.
- No blocking gaps: the driver contract was implementable from the page
  alone without opening `mutation-case-kimi-census.md` (deliberately not
  opened — reproduction "from this page alone" is the claim under test).

## Recommendations (bounded)

- In Appendix A, note that `git status --porcelain` being empty does not
  imply blob equality — the pin check must key on the sha256 line, which
  the page already does; optionally replace `cp -p` with
  `git show 175de6ba:scripts/kimi-census.mjs >` for drift immunity.

```json
{"seat":"CR11b","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[{"start":527,"heading":"## Appendix A — worked example: JS case (reproduce from this page alone)","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["kumitate worktree blob drifted from pin (worktree sha 5e8d5913…, 922 lines, 44770 B vs pinned 83016d45…, 896 lines, 43273 B; HEAD 1770305f not 175de6ba, status clean) — resolved via the page's own re-anchor contingency using git show 175de6ba:scripts/kimi-census.mjs; literal cp -p would now fail the next-line sha256 guard","sweep wall time 7.79 s vs stated 7.0 s (page frames timing deviations as host/suite findings, not reproduction failures)"],"commands_executed":["cp snapshot to /tmp + sha256sum (97cf436b… match)","git -C kumitate-shokunin rev-parse HEAD → 1770305fae2082…","git -C kumitate-shokunin status --porcelain -- scripts/kimi-census.mjs → empty","sha256sum worktree scripts/kimi-census.mjs → 5e8d5913… (drifted)","git -C kumitate-shokunin show 175de6ba:scripts/kimi-census.mjs > /tmp/…/pinned.mjs → sha 83016d45…4f426, 896 lines, 43273 B","node pristine.mjs --selftest → KIMI_CENSUS_SELFTEST: 43/43 pass, VERDICT: PASS, exit 0","python3 mutate_driver.py --check → CHECK: all unique, exit 0","python3 mutate_driver.py --run → 8/10 killed, survivors D2/D10, exit 0, 7.79 s","node mutant-D2.mjs --root empty-root | tail -1 → 5 ids + '+23 more', node exit 1","node mutant-D10.mjs --root empty-root | grep 'FAMILY K2' → frozen=24, exit 0","post-run sha256sum pristine.mjs → 83016d45…4f426 unchanged; kumitate status still empty"],"opened":["/tmp/tameshi-r16-CR11b/SKILL.snapshot.md (lines 527-593; header context 497-526 shown by reader)","/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs (read-only: sha256sum, wc, git status)","git show 175de6ba:scripts/kimi-census.mjs (blob materialized to /tmp)","/tmp/tameshi-r16-CR11b/work/mutate_driver.py (authored)","/tmp/tameshi-r16-CR11b/work/evidence/*.meta.json, results.json"],"scratch":"/tmp/tameshi-r16-CR11b"}]}
```
