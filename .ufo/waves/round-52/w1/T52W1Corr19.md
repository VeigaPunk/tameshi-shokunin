# T52W1Corr19 — correction record: `## Eighth recorded case — round 18`

- Seat `T52W1Corr19`, round 52 wave 1 (scribe, calibration / C2 m4), lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Re-key entry: heading `## Eighth recorded case — round 18`, `read_rev` `02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read19`.
- Reader file `.ufo/evidence/round-51/coldread/reads/T51W2Read19.md` (14068 bytes, sha256 `ef1ceb0e2405a83e9b2add8bfaac1ef752e25b6cebf1a4627d2e7fdce0e82c75` at `read_rev`; worktree copy byte-identical).
- Deliverable: `.ufo/waves/round-52/w1/T52W1Corr19.json`. This seat decides nothing; it produces the record the L1 appends to the round-21 ledger.

## What the ledger says at base (the defect this record repairs)

`git -C <lane> show ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:.ufo/evidence/round-21/coldread/ledger.json` → the `02ec217c…` entry for this heading reads:

```json
{"heading": "## Eighth recorded case — round 18", "read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9",
 "seats": ["T51W2Read19", "L1 TameshiR51a3 integration (attempt 3)"],
 "start": 1905, "end": 1924, "wrong_expectations": 0, "minor_gaps": 0,
 "verdict": "verified-record", "class": "record",
 "sha256": "c221eecdf8ff27487c2c974b3f1bd5e2cfa78111aaaebb2c8db561c74d9116fd"}
```

Top-level `"corrections"` list at base: **0 records**. The zero is written from code, not read from the reader: `.ufo/evidence/round-51/coldread/refresh.py:224-227` appends `'wrong_expectations': 0, 'minor_gaps': 0` and `'verdict': 'verified-record'` unconditionally (`sed -n '216,232p' .ufo/evidence/round-51/coldread/refresh.py`). That is routed defect 3 of `corpus/lessons/round-51-verifier-spotcheck.md:128`. The reader recorded one falsified statement.

## Findings (1)

### F1 — stale-count: the replay's case count parenthetical is superseded by the tenth leg

Reader anchors (all commands run from the lane root):

| Surface | Line | Command showing it |
|---|---|---|
| verdict cell of pointer row P7 | `T51W2Read19.md:21` | `awk 'NR==21' .ufo/evidence/round-51/coldread/reads/T51W2Read19.md` → `**PARTLY STALE — see F1**` in the Verdict column |
| finding heading | `:27` | `awk 'NR==27' …` → `### F1 (the one falsified statement — stale by the tenth leg)` |
| the section statement as the reader quoted it | `:29` | `awk 'NR==29' …` → `` `cases=8 passed=8` at the round-18 runner (`cases=9 passed=9` **from round 26 on**, ninth leg js-cite-check; seat Read34). `` |
| the reader's verdict and its evidence | `:31` | `awk 'NR==31' …` → "the round-51 C2 leg `bash-drift-pins` is wired in `tools/mutate-and-run.sh` … so the replay now runs and reports **`cases=10`**. The parenthetical's \"from round 26 on\" stopped being true the moment the tenth leg landed." |

Section text it concerns (`git -C <lane> show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md | awk 'NR>=1905 && NR<=1924 {printf "%d| %s\n", NR, $0}'`), lines 1913-1915:

```
1913| Entry: `corpus/knowledge/mutation-case-kumitate-sources-check.md`. Replay:
1914| `bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-sources-check: PASS`,
1915| `cases=8 passed=8` at the round-18 runner (`cases=9 passed=9` from round 26 on, ninth leg js-cite-check; seat Read34). Wave 2 probed all five survivors off-suite: four are non-equivalent, `S_KIND`
```

Why it does not hold at `read_rev` — the runner wires a tenth regression leg, so the replay's case count is 10, not 9:

```
$ git -C <lane> show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:tools/mutate-and-run.sh \
    | grep -n "tenth measured leg\|bash-drift-pins\|ninth measured leg"
18:# tenth measured leg, kagi corpus/drift-pins.sh, as bash-drift-pins.
97:#   bash-drift-pins       kagi-shokunin/corpus/drift-pins.sh          2/10 (20 %)
104:# .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec (leg 10).
1155:  cat >"$d/bash-drift-pins.spec" <<'EOT'
1219:     && -s "$d/bash-drift-pins.spec" ]]
1446:  printf 'REGRESSION_EXPECT: recorded kill-rates — … js-cite-check=%s/%s bash-drift-pins=%s/%s\n' \
1504:  regression_case_git bash-drift-pins \
2045:    'bash-drift-pins:bash-drift-pins.spec:TABLE_DRIFTPINS:10:2'
```

The historical half of the sentence (`cases=8 passed=8` at the round-18 runner) holds and is not counted: the reader records it as holding at `:21` ("historical part holds (ER8-1: replay at `01d586d` = `REGRESSION: PASS (cases=8 passed=8)`")), and `read_rev` is later than that runner state — `git -C <lane> merge-base --is-ancestor 6d8c11e378aa90b12650808e1b79270742935f15 02ec217c4d0afabe727fde2e261b7951d28fb4e9` → exit 0 (the reader's CAND is an ancestor of the ledger's `read_rev`).

Delivered record entry:

```json
{"quote": "so the replay now runs and reports **`cases=10`**. The parenthetical's \"from round 26 on\" stopped being true the moment the tenth leg landed.",
 "class": "stale-count",
 "skill_statement": "`bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-sources-check: PASS`, `cases=8 passed=8` at the round-18 runner (`cases=9 passed=9` from round 26 on, ninth leg js-cite-check; seat Read34)"}
```

Class `stale-count`: the statement's number of replayed cases (9, "from round 26 on") is out of date; the tenth leg (`bash-drift-pins`, round 51) makes the replay report `cases=10`. No measurement in the section is wrong; the reader's own severity is "stale-temporal". I did not re-run the regression to observe the printed total — that is the deciding run's job; the count is established from the legs wired at `read_rev` (command above).

## Checks run (commands and observed output)

1. Section location at `read_rev`: `git -C <lane> show 02ec217c…:SKILL.md | awk 'NR>=1905 && NR<=1924 {printf "%d| %s\n", NR, $0}'` → heading at 1905, body 1906-1923 (1923 = last table row), 1924 blank, next heading `### Round-18 gate/probe registry — routed-defect closure` at 1925. Matches the item's 1905-1924 and the ledger's `start`/`end` (1905/1924).
2. CAND vs `read_rev` section bytes: `diff <(git show 02ec217c…:SKILL.md | sed -n '1905,1924p') <(git show 6d8c11e3…:SKILL.md | sed -n '1905,1924p')` → `IDENTICAL`. The reader's CAND section text is byte-equal to the `read_rev` section, so its finding transfers unchanged.
3. Reader file at `read_rev` vs worktree: `git show 02ec217c…:.ufo/evidence/round-51/coldread/reads/T51W2Read19.md` → 14068 bytes, sha256 `ef1ceb0e…e82c75`, equal to the worktree file's sha256.
4. Reader verdict census (whole file, 70 lines): 8 `HOLDS` verdict cells (`:15`-`:20`, `:22`-`:23`) and 1 `PARTLY STALE` (`:21`) → exactly one statement recorded as not holding. `grep -o -E "PARTLY STALE|HOLDS" .ufo/evidence/round-51/coldread/reads/T51W2Read19.md | sort | uniq -c` → `8 HOLDS`, `1 PARTLY STALE`.
5. Ten legs at `read_rev`: command in F1 above → `:18`, `:97`, `:104`, `:1446`, `:1504`, `:2045` name `bash-drift-pins` as leg 10.
6. Ledger binding: sha256 of section lines 1905..1923 joined with `\n` = `c221eecdf8ff27487c2c974b3f1bd5e2cfa78111aaaebb2c8db561c74d9116fd` = the entry's `sha256` field, so the entry I correct is bound to exactly this section's bytes (`python3 -c` recomputation; `refresh.py:225-226` copies that hash from the round-51 spec rather than recomputing it).

## Self-check against the frozen rule (`check_findings`, `.ufo/evidence/round-52/c2/measure.py:82-95`)

The frozen module was copied to scratch and imported with `PYTHONDONTWRITEBYTECODE=1` so no bytecode lands in the lane:

```
$ S=/fast/scratch/hyaku/tameshi-r52/T52W1Corr19; mkdir -p "$S" \
  && cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/c2/measure.py "$S/measure.py" \
  && cd "$S" && PYTHONDONTWRITEBYTECODE=1 python3 -c '…import measure as m; check_findings(rec["findings"], git-show(reader_file))…'
heading = ## Eighth recorded case — round 18
reader  = T51W2Read19 | read_rev = 02ec217c4d0afabe727fde2e261b7951d28fb4e9
check_findings -> None
wrong_expectations == len(findings): True (1)
quote len=141 chars=141 class=stale-count verbatim=True
exit=0
```

`check_findings -> None` is the frozen counter's pass value: the quote is a verbatim substring of the reader file after whitespace collapse (`squash`), 141 characters (>= 20), and `wrong_expectations == len(findings) == 1`. No frozen floor applies to `T51W2Read19` (`measure.py:51`: floors exist only for `T51W2Read20` and `T51W2Read01`).

## Not counted (and why)

- The other 8 pointer rows are `HOLDS` (reader `:15`-`:20`, `:22`, `:23`) — verdicts holding, not failures. `:39` records "Unsupported premises: none found".
- `:9` "Fixture list §3 wrote \"1906-1925\" — one line over into the next heading; informational only" concerns the round-51 **fixture list**, not a statement of the section, and the reader itself marks it informational. Not a section statement; excluded.
- `:21`'s "PARTLY STALE" cell is the same statement as F1, not a second one.
- `:31`'s `passed=10` expectation and the "Verification gaps" block (`:62`-`:66`) are the reader's own unverified scope, not a section statement recorded as false.
- `:7`-`:9` location block and the `reads.json` row (`:43`-`:58`) are record surface; the `body: 1906-1924` note differs by one line from the hash-bound span (1905-1923) but names no section statement, so it is not a finding.

## Touched surfaces and bounds

- Wrote exactly two files, both in this seat's scope: `.ufo/waves/round-52/w1/T52W1Corr19.json` and `.ufo/waves/round-52/w1/T52W1Corr19.md`. No other lane file, no fleet-repo file, no sibling lane, no `shokuknow`, no jj/Git index; no `git add/commit/checkout/…` and no mutating jj call was run.
- Read-only throughout: all lane content came through `git show`/`git cat-file` or plain reads.
- No `__pycache__` was created in the lane by this seat: `.ufo/evidence/round-52/c2/__pycache__/measure.cpython-314.pyc` is stamped `2026-10-27 01:52:29 -0300`, before this seat's 05:11Z run; the module was imported from a scratch copy only.
- Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1Corr19` was created, held only a copy of `measure.py` (and its scratch `__pycache__`), and was removed in the same command that ran the check (`exit=0`, `rm -rf` after); nothing under `/tmp`, no fixture repo was needed, no clone was made.
- Tooling: no install or upgrade (no pacman, uv, npx, cargo or npm transaction); Python 3 (stdlib only) and git were used as installed.

## Known limits

- The reader worked at CAND `6d8c11e3…`; the ledger's `read_rev` `02ec217c…` is a later commit. I verified both section texts byte-identical (check 2) and confirmed the runner's ten legs directly at `read_rev`, so the finding is not inherited on trust.
- The replay's printed `passed=10` is not observed here (deciding-run regression owns it); F1 rests on the wired leg census, as the reader did.
- Appending this record to `.ufo/evidence/round-21/coldread/ledger.json` (top-level `corrections`) and the wave-2 re-key entries (C2 m6) are the L1's edits; this file is the record they consume.
- I did not audit the other 19 re-key entries (other seats) and did not run any counter beyond the `check_findings` self-check above.

## Summary

- Deliverable `.ufo/waves/round-52/w1/T52W1Corr19.json`: one finding, `wrong_expectations = 1` (ledger at base wrongly says 0, hardcoded by `refresh.py:224-227`).
- F1 `stale-count`: SKILL.md:1915 (at `02ec217c`) says the replay reports "`cases=9 passed=9` from round 26 on, ninth leg js-cite-check"; at `read_rev` the runner wires the tenth leg `bash-drift-pins` (`tools/mutate-and-run.sh:18,97,1446,1504`), so the replay reports `cases=10` (reader `T51W2Read19.md:21,27,29,31`).
- The section's historical half (`cases=8 passed=8`) holds per reader `:21` and is not counted; section bytes are identical at the reader's CAND and at `read_rev` (`diff` → `IDENTICAL`).
- Frozen `check_findings` on the delivered record: `None` (quote 141 chars, verbatim after whitespace collapse; count matches).
- All 8 other pointers hold; the fixture-list line nit and the reader's own inference are excluded, with reasons above.
- Lane untouched apart from the two scoped files; scratch removed; no tooling installed.
