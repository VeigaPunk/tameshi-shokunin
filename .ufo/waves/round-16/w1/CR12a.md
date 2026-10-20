# CR12a — cold-read: Appendix B, bash mutation case (lines 594–667)

Seat: TameshiR16.CR12a · Range: SKILL.snapshot.md lines 594–667 · One section: `## Appendix B — worked example: bash case (reproduce from this page alone)` (heading line 594).

## Scope and method

Snapshot copied to `/tmp/tameshi-r16-CR12a-1/SKILL.snapshot.md`; `sha256sum` printed `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` (matches the assigned pin). The range contains exactly one `##` section; the next heading is line 668 (`## Third case …`).

The section is **instruction** ("reproduce from this page alone"). I executed every command block and constructed the two artifacts the page directs the reader to write (`mutate_driver.py` + `SPECS`), plus the probe fixtures the page's commands require.

Named material opened per the contamination rule:
- `SKILL.snapshot.md` lines 527–593 — Appendix A, explicitly named by my range ("**Driver contract:** same as Appendix A except …"). Read for the contract only; I did not run Appendix A.
- `tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md` — explicitly named; used for §7 ("Reproduce"), which the page's probe comment cites ("note §7 commands"), and for spot-checking its cited anchors.
- `kagi-shokunin/corpus/surface-census.sh` — the pinned artifact itself (materialized via `git show`, never written); read to derive probe-fixture schemas for `$HOME`/`$STATE` prefixes, census/shapes/baseline TSV columns, and the verify/summary output contract.
- Nothing else: no LOG.md/SCORECARD.md/plans/other seats' files.

## Executed sequence and observed results

Host facts: `bash 5.3.20`, `python3 3.14.8`, `sqlite3 3.54.0`; `command -v the-janitor` → absent (matches the page's "both substrate-absent on this host" for cases 15/16).

**Artifact pin (page :601-606).** `git -C kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh > $W/pristine.sh; chmod 755`. Verified: sha256 `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` ✓; 44212 B ✓; mode 755 (applied, and worktree file is already 755) ✓; 886 newlines, last byte `0x63` — no trailing newline ✓; `git status --porcelain -- corpus/surface-census.sh` empty ✓. Deviation: kagi HEAD is now `c2cab35bc92e57e39e5489bac3386db078345b3f`, not `fecee87`; the page pins the *rev* only as the artifact's origin rev. `git show fecee87:corpus/surface-census.sh` and the worktree file both hash to the pinned sha256, so the pinned blob is unchanged — pin holds in substance.

**Control (page :615-617).** `bash $W/pristine.sh --selftest` → `SELFTEST: PASS (16 cases)`, rc=0; ok-case 01–14, `skip-case 15/16 … substrate-absent (handler not on PATH)`. Exact match to the page.

**`--check` (page :619).** `python3 mutate_driver.py --check` → `occurrences=1` for all ten specs, final line `CHECK: all unique`, rc=0.

**`--run` (page :620).** control + B1–B10, each a fresh copy (pristine untouched). Sweep wall ~12.6 s (page says 11.0 s — environment delta). Measured vs page (:652-660):

| Mutant | Measured | Page | Match |
|---|---|---|---|
| control | PASS, rc=0 | PASS | ✓ |
| B1 | exit=1, bad-case 05 undeclared-file | FAIL 1/16 | ✓ |
| B2 | exit=1, bad-case 01 clean + 04 runtime-absent | FAIL 2/16 | ✓ |
| B3 | exit=1, bad-case 01 + 04 + 06 crosscheck-disagree | FAIL 3/16 | ✓ |
| B4 | exit=1, bad-case 07 symlink-swap (`want exit=1 … got exit=1` — token-only kill) | FAIL 1/16 | ✓ |
| B5 | `SELFTEST: PASS (16 cases)`, rc=0 | survivor | ✓ |
| B6 | exit=1, bad-case 01 + 04 | FAIL 2/16 | ✓ |
| B7 | exit=1, bad-case 10 sqlite-unavailable | FAIL 1/16 | ✓ |
| B8 | exit=1, bad-case 13 malformed-row + 14 fused-shape-row | FAIL 2/16 | ✓ |
| B9 | exit=1, bad-case 03 asset-gone + 04 runtime-absent | FAIL 2/16 | ✓ |
| B10 | `SELFTEST: PASS (16 cases)`, rc=0 | survivor | ✓ |

**Kill rate: 8/10 = 80 %** — matches the headline (:596-597) and every per-mutant line including case labels.

**Survivor probes (page :621-623).** The page names the commands but no fixture contents; note §7 (:239-249) gives the same commands and likewise no fixture build. I derived fixtures from the script's header-documented TSV schema and its `resolve()`/`verify_surfaces()` contract:
- `probe/`: `host/bin/tool` (file, chmod 644); census.tsv = `$HOME/bin-tool row, class asset, kind exec, mode -`; empty shapes/baseline. `mutant-B5.sh verify …` → `SURFACE OK       $HOME/bin/tool (exec 644)` + `CLEAN (… ok=1 …)`, rc=0; pristine → `SURFACE DIVERGED $HOME/bin/tool (declared exec, no execute bit)` + DRIFT, rc=1. Matches :661-662 verbatim.
- `probe2/`: `host/f.txt` (644); census.tsv = `$HOME/f.txt, asset, file, 644`; empty shapes/baseline. `mutant-B10.sh verify …` → `CLEAN (assets=1 runtime=0 scanned=0 ok=0 …)`, rc=0; pristine → `ok=1`. Matches :662-663.

**Restore (page :664-665).** After the sweep: `sha256sum pristine.sh` still `275d8294…53009f` ✓; 44212 B / mode 755 unchanged ✓ (mtime differs from the note's `-0300` stamp only because I materialized via `git show`+`chmod`, not `cp -p` — irrelevant to the pin); `git status --porcelain` for the path still empty ✓; `cmp` scratch-vs-worktree → identical ✓.

## Gaps and observations

1. **Minor gap — probe fixtures unspecified.** The page's probe commands reference `$W/probe/{census,shapes,baseline}.tsv` and `probe/host` that nothing on the page builds; the note §7 the page points at also lists the commands without fixture construction ("Scratch (all under …): … probe fixtures probe/, probe2/" — §7:213). Reproducing required reading the artifact's schema docs and the §2 expected strings. A reader with no oral context *can* complete it (I did, output matched verbatim), but the page is not self-contained for this step — the claim "(reproduce from this page alone)" is ~95 % true.
2. **Minor — rev pin is historical.** Page says "kagi rev `fecee87`"; HEAD has moved (`c2cab35b`), though the pinned blob sha still matches both the rev and the worktree. A one-line "rev may be superseded; sha256 is the pin" note already exists in Appendix A (:537-538) but not restated for B.
3. No wrong-expectation findings: every stated outcome (control, 8/10, both survivor identities, all failing-case labels, probe strings, restore facts) was reproduced exactly; only the 11.0 s wall-time figure differed (12.6 s, environment-dependent).

## Recommendations (bounded)

- Add ~6 lines of fixture construction to Appendix B (or a `probe/` heredoc block) so the survivor probes are literal-copyable; alternatively soften "(reproduce from this page alone)" to name the census-TSV schema dependency.
- Consider restating the "sha256 is the pin, rev is historical" caveat once under Appendix B's artifact pin.

## Tooling

No installs or updates performed; existing `bash`/`python3`/`sqlite3`/`git` sufficed.

```json
{"seat":"CR12a","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[{"start":594,"heading":"## Appendix B — worked example: bash case (reproduce from this page alone)","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["survivor-probe fixture contents (census/shapes/baseline TSVs + probe host trees) are not given on the page nor in the note §7 it cites; I derived them from the artifact's header schema and matched the stated probe outputs verbatim","page pins 'kagi rev fecee87' but HEAD has moved to c2cab35b; pinned blob sha256 still matches rev and worktree so the pin holds, but the rev is historical","stated 11.0 s sweep measured 12.6 s on this host (environment delta)"],"commands_executed":["sha256sum /tmp/tameshi-r16-CR12a-1/SKILL.snapshot.md","git -C kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh > $W/pristine.sh; chmod 755","sha256sum $W/pristine.sh  # 275d8294...53009f","stat -c '%s %a' $W/pristine.sh  # 44212 755","wc -l corpus/surface-census.sh  # 886; tail -c1 -> 0x63 (no trailing NL)","git -C kagi-shokunin status --porcelain -- corpus/surface-census.sh  # empty","bash $W/pristine.sh --selftest  # SELFTEST: PASS (16 cases), rc=0","python3 $W/mutate_driver.py --check  # all unique, rc=0","python3 $W/mutate_driver.py --run  # 8/10 killed, survivors B5 B10","bash $W/mutant-B5.sh verify --root $W/probe/host --census $W/probe/census.tsv --shapes $W/probe/shapes.tsv --baseline $W/probe/baseline.tsv  # SURFACE OK ... (exec 644), rc=0","bash $W/pristine.sh verify --root $W/probe/host ...  # SURFACE DIVERGED ... no execute bit, rc=1","bash $W/mutant-B10.sh verify --root $W/probe2/host --census $W/probe2/census.tsv --shapes $W/probe2/shapes.tsv --baseline $W/probe2/baseline.tsv  # ok=0, rc=0","bash $W/pristine.sh verify --root $W/probe2/host ...  # ok=1, rc=0","cmp $W/pristine.sh kagi-shokunin/corpus/surface-census.sh  # identical"],"opened":["/tmp/tameshi-r16-CR12a-1/SKILL.snapshot.md","SKILL.snapshot.md:527-593 (Appendix A, named by range)","/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md","/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh (read-only; blob at pinned rev via git show)"],"scratch":"/tmp/tameshi-r16-CR12a-1-work"}]}
```
