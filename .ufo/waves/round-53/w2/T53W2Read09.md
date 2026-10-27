# T53W2Read09 — wave-2 re-read of `### Reading a receipt — the discipline`

- Section heading: `### Reading a receipt — the discipline`
- Content commit (C\*\*): `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`
- Section line range at C\*\*: `SKILL.md:970-1013` (next heading, `## The re-sweep cadence and the six-case confidence statement (round 8, measured)`, at `:1015`; blank `:1014` stripped as trailing whitespace)
- `section_sha256` = `53cbbf610d088a5f03053909b56a53134693a822950741ed4119d6c7d650458b` (UTF-8, surrogateescape; heading line through last non-blank line, joined with `\n`, no trailing newline)
- Findings: **1** (unsupported premise). The wave-1 finding for this section (stale selftest tally) is **repaired at C\*\***.

Every read below is of git objects at C\*\* (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5b703c6f…:SKILL.md` / `…:tools/mutate-and-run.sh`), never the working tree. The one execution used a copy of the C\*\* runner blob under the seat scratch (`/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read09`), with `TMPDIR` and `--workdir` under that scratch; the tree was deleted before yielding.

## 1. Fix verification first — the wave-1 tally finding

Wave-1 (`.ufo/waves/round-53/w1/T53W1Read12.*`) filed one finding: item 7's `MUTATE_SELFTEST: 67/67 pass` arrow named the command a reader runs and therefore promised a tally the current runner does not print. The L1's fix pass 2 rewrote item 7; the C\*\* bytes of the whole item now read (file lines 1007-1013):

```
7. **The ledger's own arms are selftested.** `bash tools/mutate-and-run.sh
   --selftest` at the pinned r7-1 tool printed `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0, tool
   sha256 `cf41efaa…` (a content sha, not a git revision; the tally is the pinned tool's, not the current command's — round 52: the same command prints `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc 0, at runner sha256 `977de470…` — seat T52W2Fix06's measurement and runner pin, `.ufo/waves/round-52/w2/T52W2Fix06.md` F3, receipt `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out`) — including a git-materialized replay passing at exact
   tolerance, a drifted working tree not moving a git-pinned leg, pin
   mismatch / unresolvable revision as SETUP, and a single flipped entry
   failing loudly. The r4-2 tolerance (`killed-delta<=1 flips<=1`) remains the
   fixture-mode default and is exercised by the selftest only.
```

Each element of the repaired sentence, checked at C\*\*:

1. **"at the pinned r7-1 tool"** — the r7-1 runner revision is `9f1d3c339a7094968041c7708a65dbf7eab9fae6` (`git cat-file -t` = commit); its `tools/mutate-and-run.sh` sha256 is `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`, the sha the sentence cites, and its driver counts `local nlegs=4` (the four-leg era).
2. **67/67 belongs to that blob** — committed receipt `.ufo/evidence/round-18/final/historical.stdout:69-71`: `MUTATE_SELFTEST: 67/67 pass`, `VERDICT: PASS`, `REGRESSION_TOOL: …/historical-r7.sh sha256=cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`. No rerun was needed; the receipt is committed at C\*\* and pins the tally to the sha.
3. **"(a content sha, not a git revision)"** — `cf41efaa…` is the file's sha256; the revision that carries those bytes is `9f1d3c3…` (command 1). Holds.
4. **"the tally is the pinned tool's, not the current command's"** — at C\*\* `tools/mutate-and-run.sh` has 2159 lines and sha256 `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`, not `cf41efaa…`.
5. **The round-52 parenthetical is a live receipt, not a stale one** — the cited runner sha `977de470…` *is* the C\*\* blob's sha (command 4), the cited files both exist at C\*\* (`.ufo/waves/round-52/w2/T52W2Fix06.md`, `…T52W2Fix06.selftest.out`), the `.out` receipt prints `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS` (`:108-109`), and `T52W2Fix06.md` F3 records `rc=0` and the same pin (`977de47034cbe52b…`, 2159 lines). The C\*\* blob is byte-identical to that CAND0 runner (same sha), and wave-1 measured 107/107 first-hand on the identical bytes; no rerun was performed here.

Verdict: the wave-1 finding is repaired in the C\*\* bytes. The section no longer asserts 67/67 as the current command's tally, and the current tally it does state carries its own revision and receipt.

## 2. Split reproduction

Fence-aware heading scan (`^#{1,3}(\s|$)` outside ``` fences) over the whole blob, then the section as heading line through the line before the next heading with trailing whitespace-only lines stripped:

```
matches: [(970, '### Reading a receipt — the discipline')]
next:    1015 '## The re-sweep cadence and the six-case confidence statement (round 8, measured)'
range:   970..1013 (44 lines)   sha256: 53cbbf610d088a5f03053909b56a53134693a822950741ed4119d6c7d650458b
lastline: '   fixture-mode default and is exercised by the selftest only.'
```

Cross-checked against `sed -n '966,1018p'` with `nl`: heading at 970, last non-blank section line 1013, blank 1014, next heading 1015. The split matches the frozen monitor's definition.

## 3. Holds (checked against C\*\* bytes / objects)

1. **Item 2 — exact PASS for ledger legs.** `regression_case_git` passes tolerance `0 0` for every leg (`:1412-1414`); the PASS line prints `defects=$(table_total)` (`:1396`, `exp_total` at `:1379`), so `D` is the recorded table's size: `TABLE_CHECKLIST` holds 15 entries (`:638`) and every other `TABLE_*` holds 10 (`:634-637`, `:639-643`). The closing PASS line prints `cases=$nlegs passed=$npass` (`:1540`) with `local nlegs=10` (`:1510`). The dated chain resolves: round-18 runner `4b7c682` has `local nlegs=8` and its selftest asserts `want 8`; round-26 commit `a08e85c` ("runner … wired to nine legs") has `local nlegs=9`; round 51 wired the tenth, and C\*\* carries ten legs.
2. **Item 2 — the T7-1 measured instance.** `.ufo/evidence/round-18/final/historical.stdout` records the replay at `REGRESSION_TOOL … sha256=cf41efaa…`: four legs, each `REGRESSION_TABLE … match=10/10 … flips=0`, `REGRESSION_CASE …: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)` ×4, `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, and the same `67/67` selftest. `reports/r7-aud-t7.md` §1 records the T7-1 primary run dated 2026-10-14 with the same headline lines and `exit 0`.
3. **Item 3 — FAIL names its rows, and both anchors resolve.** Emitters: `REGRESSION_DEFECT %s %s: measured=%s recorded=%s` including the two `ABSENT` arms (`:1357`, `:1371`), `REGRESSION_TABLE … flips=%s` (`:1392`), `REGRESSION_CASE %s: FAIL (out of band:%s; log: %s)` (`:1400`). `reports/r7-aud-t7.md` section 3 ("Flip-test the guard — on a scratch copy") carries F4 at report line 111 (table flip `TABLE_TSUKUROI B7`, `match=9/10 … flips=1`, leg FAIL out of band). `tools/mutate-and-run.sh:2010` is the line `grep -qF 'REGRESSION_CASE fixture: FAIL (out of band: killed-delta=1 flips=1;' …` — quoted content resolves at the cited line. `/tmp/w7-tameshi-1` does not exist (`ls` → No such file or directory), so the bracketed "that volatile path is gone" is true.
4. **Item 4 — SETUP is not a verdict.** SETUP arms at `:1244`, `:1249`, `:1263`, `:1268`, `:1272`, `:1277`, `:1286`, `:1291`, `:1297`, `:1309`, `:1314`, `:1327`; the SETUP closing lines are separate from FAIL (`:1526`, `:1535`).
5. **Item 5 — the ledger carries composition and revision.** `corpus/knowledge/fleet-kill-rate-ledger.md` exists at C\*\*; its §1 rows state each rate with its composition (`10 kill-aimed`, `6 kill-aimed (6/6) + 4 hole-aimed (0/4)`, `4 in-surface (4/4) + 6 out-of-surface (0/6)`, …) and its target pin/first-16; the file's header states "a rate is never implied to hold at a later revision" and "Composition is stated beside every rate". (The section names the file bare; the path is `corpus/knowledge/`, given in full two sections earlier — a resolvable pointer, not a finding.)
6. **Item 6 — the round-7 attestation leg.** `plans/round-7.plan.md:11-15` at C\*\* is verbatim "(2) Leg fleet-run case: mado's round-6 self-service sweep … is ATTESTED read-only: reproduced by tameshi from its pins, or its missing piece named. The lane operates; tameshi attests." — read-only replay plus the "missing piece named" alternative hold at the cited range.
7. **Item 7 — the selftest's coverage arms exist at C\*\*.** `ledger leg: git-materialized replay PASSes at exact tolerance` (`:1833`, with the `PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=2)` assertion), `drifted working tree does not move a git-pinned leg` (`:1840`), `ledger leg pin mismatch is SETUP (exit 2)` (`:1849`), `ledger leg unresolvable revision is SETUP (exit 2)` (`:1857`), `exact expectation: one flipped entry FAILs loudly` (`:2007`) with the defect-row and `killed-delta=1 flips=1` assertions (`:2008-:2010`). The tolerance sentence holds: `BAND_KILLED=1` / `BAND_FLIPS=1` (`:196-197`) are used only when the tolerance args are absent (`:1240-1241`), while ledger legs pass `0 0` (`:1413`).
8. **Item 3's quoted CASE FAIL line — held, not filed.** The emitted line continues `; log: <path>` before its closing paren (`:1400`; the same emitter shape at r7-1, `9f1d3c3:tools/mutate-and-run.sh:874`), so the section's `FAIL (out of band: killed-delta=1 flips=1)` is a truncation. Wave-1 examined this and recorded it as a hold (the negative-run receipt is gone; the mechanism is corroborated by F4 and the arithmetic is consistent), and this re-read finds no new evidence against that treatment.

## 4. Finding 1 — the receipt grammar is stated unconditionally (class: unsupported premise)

Verbatim quote from the section (item 1, byte-exact including leading spaces and line breaks):

```
1. **Read the block, not the last line.** `REGRESSION_TOOL` ·
   `REGRESSION_DATE` · `REGRESSION_BAND` · `REGRESSION_EXPECT` · one
   `REGRESSION_PIN` per leg · per leg one `REGRESSION_SWEEP` +
   `REGRESSION_TABLE` + `REGRESSION_CASE` · `REGRESSION_DEFECT` rows for
   differences · `REGRESSION_WORKDIR` · the closing `REGRESSION:
   PASS|FAIL|SETUP` line.
```

Asserted as an exact substring of the section bytes at C\*\* (single occurrence).

Why it does not hold at C\*\*: the bullet names SETUP as a possible closing verdict and asserts one `REGRESSION_PIN` per leg plus one `REGRESSION_SWEEP` + `REGRESSION_TABLE` per leg, but the C\*\* tool emits those three lines only for legs that get past materialization into a sweep. First-hand run of the C\*\* bytes:

```
$ mkdir -p <scratch>/lane/tools && git -C <lane> show 5b703c6f…:tools/mutate-and-run.sh > <scratch>/lane/tools/mutate-and-run.sh
$ cd <scratch>/lane/tools && TMPDIR=<scratch>/sf bash mutate-and-run.sh --regression --workdir <scratch>/sf/rg
REGRESSION_TOOL: …/lane/tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
REGRESSION_CASE js-kimi-census: SETUP (repo_identity_mismatch: … is not its own repository; toplevel=unresolved)
… (ten SETUP case lines) …
REGRESSION: SETUP (cases=10 passed=0 cannot-verify=10)
REGRESSION_WORKDIR: <scratch>/sf/rg (kept)
rc=2
```

The block carries the four `REGRESSION_*` header lines, ten `REGRESSION_CASE` SETUP lines and the closing SETUP line — and **zero** `REGRESSION_PIN`, `REGRESSION_SWEEP`, `REGRESSION_TABLE` lines. Code path: every SETUP return at `:1244`-`:1297` precedes the `REGRESSION_PIN` printf at `:1302`, and the `REGRESSION_SWEEP`/`REGRESSION_TABLE` prints at `:1324`/`:1392` follow the sweep. The lane's committed evidence shows the same grammar at an older sha: `.ufo/evidence/round-18/coldread/traces/CR18/7.out.txt` has `REGRESSION_CASE js-kimi-census: SETUP (path not in revision…)`, `…bash-surface-census: SETUP (repo_identity_mismatch…)` and `…bash-tsukuroi-census: SETUP (revision not found…)` with no PIN line for any of the three, while the pin-mismatch legs in the same block do print `REGRESSION_PIN` — PIN presence is stage-dependent inside one block. The FAIL stage shares the gap: the sweep-exit (`:1331`) and no-results-table (`:1337`) arms print `REGRESSION_CASE … FAIL` with no `REGRESSION_TABLE`.

Item 4 of the same section teaches readers that these SETUP blocks are legitimate receipts ("cannot verify"), so the unconditional grammar in item 1 is contradicted by the blocks the section itself asks readers to read.

## 5. Notes

- **No scratch-directive violation in the section.** The only `/tmp` mention is the historical negative-run path, bracketed as gone at round 52, and it is in fact gone.
- **Tooling:** no installs or upgrades; `git`, `bash`, `python3`, `sha256sum`, `sed`, `diff` were already present. No package manager was invoked (pacman guard respected).
- **Scope:** reads only inside the lane; the single execution ran entirely inside `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read09` (runner copy + workdir + `TMPDIR`), FLEET_ROOT resolved to that seat scratch (no fleet repo touched, no sweep run), and the whole scratch tree was deleted before yield. No writes outside `.ufo/waves/round-53/w2/T53W2Read09.{json,md}` and that scratch tree; no git/jj mutation anywhere.
