# T54W2Read05 — cold read of `### Using the ledger` at C1 `99c3bc88d704566197783f66b211ee0a830e0330`

Seat: reader (wave 2, fresh read at the C1 fix commit). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Section bytes: SKILL.md `946-977` (0-based span start=946 end=977), `section_sha256 = 10c6288580f2b581a57818356480537e3ba6af51f8dfe6fa23e91110cb9766ec` (printed by the wave reader tool, `.ufo/waves/round-54/reader-section.py`).
Machine deliverable: `.ufo/waves/round-54/w2/T54W2Read05.json`.

## Findings (1)

### F1 — the receipt-N enumeration omits N=6, which the bullet's own cited inventory records

- Byte-exact quote (verified `count == 1` in the section bytes):
  `(N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since round 26, 10 since round 51)`
- Why: the rule is the citation form for kill-rate receipts — "Cite `REGRESSION: PASS (cases=N passed=N; …)` (N=4 at r7-1, 7 since round 16, ...)". The same bullet cites the tool's ten-leg inventory as `inventory :83-108`, and that inventory records a six-leg milestone; the page itself quotes two six-leg receipts and one registry row that names the six-leg era. A cold reader who meets any of those receipts has no `N` in this list to validate them against, and the sequence reads as if the count jumped 4 → 7.
- Artifact it is stale against (all at C1 unless stated):

  ```
  $ git -C <lane> show 99c3bc88…:tools/mutate-and-run.sh | sed -n '84p'
  # --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten) — the fleet's

  $ git -C <lane> show 606716f:tools/mutate-and-run.sh | grep -n 'nlegs=\|REGRESSION: PASS'
  1143:  local nlegs=6 npass=0 nfail=0 nsetup=0 st
  1164:  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
  # i.e. a round-10..15 receipt reads cases=6 passed=6 with the same PASS shape the rule quotes

  $ git -C <lane> show 99c3bc88…:SKILL.md | sed -n '1364p;1452p;1415p'
  (1364)  `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0
  (1452)  8/8/6/4/7/7; closing `REGRESSION: PASS (cases=6 passed=6; ledger legs
  (1415) | `tools/mutate-and-run.sh` | the instrument: `--selftest`, `--regression` (six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26, ten since round 51; git-materialized replay) | any sweep or replay |
  ```

- Locator: the quote is on SKILL.md line 963; the cited `inventory :83-108` is on line 974 of the same bullet, `tools/mutate-and-run.sh:84` is in that range.
- Falsifier for the counter-argument "the six-leg era is documented in its own section": the rule is the page's receipt-reading discipline, and the page's own six-leg receipts (1364, 1452) are kill-rate receipts the rule as written cannot sanction; the omission is inside the enumerated list, not a pointer elsewhere.

## Anchors checked at C1 (all resolve; no drift found)

Tool bytes are identical at C0 `59c38109` and C1 `99c3bc88` (`git diff 59c38109 99c3bc88 -- tools/mutate-and-run.sh` → empty), so the section's `re-verified at 59c38109` parenthetical still describes the shipped tool.

| Section claim | Cited anchor | What C1 bytes show | Verdict |
|---|---|---|---|
| `Exits 0/1/2: PASS/FAIL/SETUP` | `tools/mutate-and-run.sh:139-143,1519-1548` | `139-143` = exit-map comment (`0 all cases PASS · 1 … FAIL · 2 … could not be verified`, incl. r30 tally mismatch); `1519-1524` FAIL→exit 1, `1525-1530` SETUP→exit 2, `1540-1548` PASS→exit 0 | resolves |
| default scratch `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX`, allocated after prerequisite checks; removed on PASS unless `--keep`, kept on FAIL/SETUP; caller workdirs never removed; pre-allocation SETUP has no root | `1432` (`root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX")`), `1423-1427` (prereqs before it), `1542-1547` (`if [[ $auto -eq 1 && $KEEP -eq 0 ]]` → `rm -rf`), `1519-1529` (kept), `1431-1437` (`auto=0` when `--workdir`) | matches code path by path | resolves |
| `git show <rev>:<path>` materializes into the case workdir, mirrors the blob's mode, pins its SHA | `:1275-1317` | `1275` dst, `1276` `git show`, `1285-1300` ls-tree mode + chmod 755 mirror, `1312-1317` pin compare | resolves |
| `REGRESSION_PIN` names repo/rev/path/mode/sha256 | `(:1302-1306)` | `1302-1303` `source=git repo=%s rev=%s path=%s mode=%s sha256=%s`; `1305` file arm | resolves |
| refusal before that leg's suite; later legs still run; statuses aggregate | `(:1247-1317,1459-1517)` | `1247-1317` repo-identity/rev/path/pin refusals all `return 2` before the sweep at `1320`; ten dispatches `1459-1508`; tally `1510-1517`; no `set -e` (only `set -u -o pipefail`, `:183`) | resolves |
| the report prints defects/killed/survived/inconclusive | `(:78-79)` | `78` = `MUTATE: DONE|DEGRADED (target=… defects=… killed=… survived=… inconclusive=… kill-rate=…%)` | resolves |
| pins/revisions/tables | `tools/mutate-and-run.sh:614-643` | `614` `PIN_JS` … `643` `TABLE_DRIFTPINS` | resolves exactly |
| first-four specs | `:671-849` | `671` `regression_specs() {`; specs at `673/714/759/804`, 4th closes with `EOT` at `849` | resolves |
| inventory | `:83-108` | `84` milestone header, `88-97` ten legs with rates, `98-104` sources | resolves (see F1 for the enumeration inside it) |
| ten dispatches | `:1459-1508` | ten `regression_case_git` calls, last is `bash-drift-pins` | resolves exactly |
| round-26 tool recorded `:603-629` | `a08e85c:tools/mutate-and-run.sh` | `603` `PIN_JS` … `629` `TABLE_CITECHECK` (nine-leg era) | resolves exactly |

Leg counts behind the milestone parenthetical, re-measured from the tool's own `nlegs` line:

```
$ for r in 9f1d3c3 05a2247 58e5d53 a08e85c 6d8c11e 99c3bc88; do printf "%s nlegs=" "$r"; git show $r:tools/mutate-and-run.sh | sed -n 's/^  local nlegs=\([0-9]*\).*/\1/p' | head -1; done
9f1d3c3 nlegs=4
05a2247 nlegs=7     # round 16
58e5d53 nlegs=8     # round 18
a08e85c nlegs=9     # round 26
6d8c11e nlegs=10    # round 51
99c3bc88 nlegs=10   # C1
$ git show 606716f:tools/mutate-and-run.sh | sed -n 's/^  local nlegs=\([0-9]*\).*/\1/p' | head -1
6                   # r10-2 — the value the section's N list omits
```

## Sweeps that found nothing (recorded so the clean read is visible)

1. **QUALITY 104 duplicate-phrase scan over the section** (the round's own criterion 104 falsifier): zero repeated 4/5/6/7-grams.

   ```
   $ python3 -c "... grams(4..7) over the 946-977 bytes ..."
   4 0 []
   5 0 []
   6 0 []
   7 0 []
   ```

2. **Run-together token / missing-space scan.** The C1 fix already repaired `Exits0/1/2` → `Exits 0/1/2`; a scan for `[a-z].[A-Z]` and `[a-z]{2,}\d` over the section returns only `${TMPDIR:-/tmp}` and `sha256`, both inside code spans.

   ```
   $ git -C <lane> diff 59c38109 99c3bc88 -- SKILL.md | grep -n 'Exits\|C\*\*\|no leg skips\|report no skipped'
   60:-  are never removed. Pre-allocation SETUP has no root to retain. Exits0/1/2:
   61:+  are never removed. Pre-allocation SETUP has no root to retain. Exits 0/1/2:
   69:-  later legs still run and their statuses aggregate (:1247-1317,1459-1517; tool lines re-verified at C** — the ten-leg runner grew since round 26).
   70:+  later legs still run and their statuses aggregate (:1247-1317,1459-1517; tool lines re-verified at `59c38109` (round 54) — the ten-leg runner grew since round 26).
   78:-  executed and skipped counts distinguished [round 53 correction, seat T53W2R6: … ] (round 52: no leg skips — host-gated branches run sandboxed; the report prints defects/killed/survived/inconclusive, `tools/mutate-and-run.sh:78-79`); and the exact recorded verdict
   79:+  executed and skipped counts distinguished [round 53 correction, seat T53W2R6: … ] (round 52: the ten legs report no skipped case on this host; the kagi leg's own table is the one that records two, as the bracket above says — the report prints defects/killed/survived/inconclusive, `tools/mutate-and-run.sh:78-79`); and the exact recorded verdict
   # the round-53 bracket text elided inside 78/79 with "…" is byte-identical on both sides of that hunk.
   ```

3. **The C1 skip-count hunk (line 970), attacked, not reported.** Read both ways: (a) as a claim about the runner's report lines, "the ten legs report no skipped case on this host" is structurally true — the runner has no skip vocabulary (`grep -n 'skip' tools/mutate-and-run.sh` returns only a `@old` line of the round-gate spec at `:818-820`); (b) as a claim about the legs' suites it would be false, because the pinned kagi leg skips two cases here. The sentence then names that exception itself ("the kagi leg's own table is the one that records two"), so it is clumsy but not a self-contradiction I can defend. Measurement kept as the sweep receipt:

   ```
   $ bash surface-census.pinned.sh --selftest   # blob = 275d8294…, pinned rev fecee874, TMPDIR=<scratch>
   rc=0
   ok-case count: 14
   17:skip-case 15 verbs-sandboxed                    substrate-absent (handler not on PATH)
   18:skip-case 16 verbs-break-injection              substrate-absent (handler not on PATH)
   19:SELFTEST: PASS (16 cases)
   ```

   Same sweep shows the section's "14 executed + 2 skipped" figure is numerically right; the noun "recorded table" is loose (the kagi note's §1 table is the 10-defect verdict table; the 14+2 figure is its §0 prose and Erratum R21), but the fleet-kill-rate-ledger §2 row for that leg does carry `16 cases (14 hermetic + 2 substrate-gated skip-case)`, so a receipt exists and I do not report it.

## Artifacts opened (read-only)

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md` (lines 900-1000 read; section 946-977 read byte-exact, `cat -A` for whitespace)
- `.ufo/waves/round-54/reader-section.py` (read, to know what `section_sha256` covers)
- `tools/mutate-and-run.sh` at C1 (`99c3bc88`), C0 (`59c38109`), `9f1d3c3` (r7-1), `606716f` (r10-2), `05a2247` (r16), `58e5d53` (r18), `a08e85c` (r26), `6d8c11e` (r51) — git objects only
- `corpus/knowledge/mutation-case-kagi-census.md` (table at 64-76; §0 at 27-35; Erratum R21 at 268-269)
- `corpus/knowledge/fleet-kill-rate-ledger.md` (row 46, `16 cases (14 hermetic + 2 substrate-gated skip-case)`)
- `corpus/QUALITY.md:1564-1578` (criteria 103/104) and `corpus/lessons/round-53.md` (mistake row 1, fix-pass debris class)
- `corpus/knowledge/scratch-root-contract.md` (to check the `TMPDIR` language does not conflict with this section)
- `.ufo/evidence/round-54/contract.json` (C1/C2 claim text; not used as evidence about bytes)
- pinned kagi blob `corpus/surface-census.sh` @ `fecee874` (sha256 `275d8294…`, 886 lines) materialized into my scratch and run

## Commands run (all read-only against the lane; writes only into the seat scratch)

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read05 ; export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read05
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    99c3bc88d704566197783f66b211ee0a830e0330 "### Using the ledger"
  -> {"heading": "### Using the ledger", "cand": "99c3bc88…", "start": 946, "end": 977,
      "section_sha256": "10c6288580f2b581a57818356480537e3ba6af51f8dfe6fa23e91110cb9766ec"}
git -C <lane> show 99c3bc88:SKILL.md | sed -n '900,1000p'          # context + section
git -C <lane> show 99c3bc88:SKILL.md | sed -n '946,977p'           # exact section bytes
git -C <lane> show 99c3bc88:tools/mutate-and-run.sh > /tmp/mr.sh   # 2159 lines at C1
sed -n '70,160p;200,270p;600,700p;820,870p;1240,1330p;1417,1560p' /tmp/mr.sh
git -C <lane> diff 59c38109 99c3bc88 -- tools/mutate-and-run.sh    # empty: tool identical C0→C1
git -C <lane> rev-parse 59c38109 99c3bc88 ; git merge-base --is-ancestor 59c38109 99c3bc88
git -C <lane> show <rev>:tools/mutate-and-run.sh | sed -n 's/^  local nlegs=\([0-9]*\).*/\1/p'   # per milestone
git -C <lane> show a08e85c:tools/mutate-and-run.sh | sed -n '595,635p'                          # round-26 anchor
git -C <lane> show 99c3bc88:SKILL.md | sed -n '1360,1366p;1448,1453p;1415p'                      # six-leg receipts/row
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show fecee874:corpus/surface-census.sh > $TMPDIR/surface-census.pinned.sh
                                      # sha256 = 275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f, 886 lines
TMPDIR=<seat scratch> bash surface-census.pinned.sh --selftest   # rc 0, 14 ok-case, skip-case 15/16, PASS (16 cases)
python3 (dup 4..7-gram scan over section bytes)                  # 0 duplicates at every n
python3 (typo scan: double spaces, fused tokens, missing space after period)
```

No lane file, counter, contract, freeze, ledger, wave spec or registry was written; no git object was created or moved; the fixture run happened on a pinned blob copy under the seat scratch with `TMPDIR` inside that scratch. No tools installed this seat.

## Result

1 finding (F1). Every cited line anchor in the section resolves at C1; the two C1 hunks in this section (`Exits 0/1/2`, the `59c38109` replacement, the round-52 skip parenthetical) were re-read and only the milestone enumeration produced a defensible defect.
