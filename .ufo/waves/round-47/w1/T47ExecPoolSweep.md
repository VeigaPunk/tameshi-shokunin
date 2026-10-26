# T47ExecPoolSweep — pool address stability and equivalence census

Item: two measurements on the frozen pool
`.ufo/evidence/round-47/hardening/pool.json` (sha256 `b4f0d075…3b038ea228c0879fdfaf4a4f669b8c63af4483`,
re-checked against `pool.POOL_SHA256` before probing; `base_sha256` matches the two round-46 hardened
counter files byte for byte: freshness `f2a8ec0fc3e08be1f439527cab8abfe6607353e91e22a1ca9277e010c623c507`,
coverage `200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9`).

Deliverables: this report and `.ufo/waves/round-47/w1/T47ExecPoolSweep.census.md` (61 rows, one per id).
No other lane file was touched; `pool.json` was read only. No counter was run as a verdict.

## 1. Address stability — PASS

Assembly with the specified inert addition (exact body `def extra_Dummy(): print('PASS D'); return 1, 0`)
and enumeration of the assembled file versus the round-46 hardened file, per group:

```
python3 .ufo/evidence/round-47/hardening/assemble.py --group freshness|coverage \
        --add /tmp/tameshi-r47-T47ExecPoolSweep/dummy-addition.py \
        --out /tmp/tameshi-r47-T47ExecPoolSweep/v2-dummy-<group>.py
python3 .ufo/evidence/round-47/hardening/pool.py --enumerate <v2-dummy-<group>.py>
python3 .ufo/evidence/round-47/hardening/pool.py --enumerate .ufo/evidence/round-46/hardening/<group>-counter.py
diff <base enum> <assembled enum>
```

| group | base sites | assembled sites | `diff` output | enum sha256 (both files) |
|---|---|---|---|---|
| freshness | 111 | 111 | **empty (0 bytes, exit 0)** | `28a0693f5cd295c4462c385c4e58f6632a5f10a964b7d4ea3c586c1e743c33d9` |
| coverage | 86 | 86 | **empty (0 bytes, exit 0)** | `33468f4bd58bda279319d217011de96412c43e4215a65853d24a4870686b663b` |

So the rule-code ids are identical, and so are the `line` fields of every enumerated site (the diff is over the
full JSONL lines, id + kind + neutral + line + desc). Two supporting facts, both observed:

* the assembled source differs from the round-46 file only in the `SELF_PATH` repoint (same string length,
  `46`→`47`), the inserted `extra_Dummy()` call block inside `selftest()` (after the last round-46 `extra_*` call),
  and the inserted `def extra_Dummy()` before `def main():` — nothing in or before any rule function:
  freshness `56c56`, `415a416,418`, `785a789,791`; coverage `31c31`, `211a212,214`, `396a400,402`;
* the dummy addition lands on the enumerator's existing exclusion (`EXCLUDE = ^(selftest|main|extra_\w+|_x\w+)$`),
  so it contributes no site, and the insert point follows the last rule function, so even the `line` numbers of the
  base sites are unchanged. Addresses are function-local (`<qualname>:<kind>:<ordinal>`), so they stay identical
  even if a future addition lands earlier in the file and shifts lines.
* the assembled dummy itself is inert: `python3 /tmp/tameshi-r47-T47ExecPoolSweep/v2-dummy-<group>.py --selftest`
  exits 0 with `PASS D`, `C1_R45_SELFTEST: cases=35 failed=0` / `C2_R45_SELFTEST: cases=21 failed=0`,
  `VERDICT: PASS` (seat probe on the /tmp copies, not a target run). Logs: `dummy-selftest-freshness.log`,
  `dummy-selftest-coverage.log`.
* `--enumerate` of each round-46 file also reproduces `pool.json`'s id list **and** line list exactly (checked
  programmatically, both groups) — the frozen pool is the enumeration of the bytes it pins.

## 2. Equivalence census — 39 behavioural, 22 mode-only, 0 equivalent

Every id whose baseline `--try` outcome is `survived` or `crashed` in `before/base-freshness.txt` (43) and
`before/base-coverage.txt` (18) — 61 in total; the 14 `NEUTRAL commute` mutants are outside the census — was
applied with `pool.apply_mutant(source, id)` (the same `ast.unparse` text `pool.judge` scores) and compared with the
pristine function on a chosen input. One row per id in `T47ExecPoolSweep.census.md`, with the pristine→mutant site
and the two observations.

| class | count | what the observation is |
|---|---|---|
| behavioural | **39** | a separating input is exhibited: 10 raise on that input, 1 changes the return type (`Tree.read` default `binary=True` returns `bytes`; its consumers then crash), 5 change the verdict token or the process exit code, 4 change only printed summary fields, 19 return a different value |
| unreachable-without-network/process | **22** | mutation sites inside `check()` (9) and `live()` (13) only; entered from `main()`'s `--check`/`--live` dispatch (`freshness-counter.py:807-810`), `selftest()` calls neither, `live()` additionally shells `curl` (line 310) and needs network |
| equivalent | **0** | no survivor is semantics-preserving; the only AST-different behaviour-equal edits in the pool stay the 14 neutral commute mutants (all surviving) |

By function: freshness — `parse_rows` 6, `extract` 2, `words` 3, `grade` 3, `review_sets` 2, `measure` 5,
`check` 9, `live` 13; coverage — `Tree.read` 1, `gt_rows` 3, `entry_ok` 8, `measure` 6.

Representative separations (full set in the census):

* `parse_rows:int:1` — one row `| S001 | https://e.org/a | docs | A | scopeX | anchorX | teachX | mined | … |`:
  key `'S001'` → key `'https://e.org/a'`; `int:3/4/5/6` shift `source`/`scope`/`anchor`/`teaches` to the next cell
  (`source` `'https://e.org/a'`→`'docs'`, …); `int:8` `url.group(0)`→`group(1)` raises `IndexError` (the
  pattern has no group), which is the `crashed` baseline.
* `extract:int:0` — `raw[:4] == b'%PDF'`→`raw[:5] == b'%PDF'` is *not* a dead constant: a 5-byte slice never equals
  the 4-byte marker, so the PDF branch is lost; on `.ufo/evidence/round-47/coverage/sources/lam-2020-reruns.pdf`
  pristine returns the pdftotext text, the mutant returns the folded raw PDF bytes. `extract:const:0`
  (`capture_output=False`) leaks pdftotext's output to the harness stdout and then raises
  `AttributeError: 'NoneType' object has no attribute 'decode'`.
* `words:bool:0` `words('and abcd')` → `{'abcd'}` vs `{'and','abcd'}`; `words:cmp:0/:int:0` `words('abcd xyz')`
  → `{'abcd'}` vs `set()`.
* `grade:cmp:9`/`grade:int:0` — a 7-token quote sharing exactly 2 content words: `('verified','ok')` vs
  `('invalid','overlap 2')`; `grade:cmp:11` — a 25-token located quote: `('verified','ok')` vs
  `('invalid','quote length 25')`.
* `review_sets:bool:1` — report names the id but not the reviewer: `(set(), set())` vs `({'S001'}, set())`;
  `review_sets:not:2` — report names both: `({'S001'}, set())` vs `(set(), set())`.
* `measure:cmp:4` / `measure:int:5` — 50 fresh rows, each variant's own bytes at `SELF_PATH` (so `self_pin=1` in
  both): pristine exit 0 / `C1_R45_PASS=true` vs mutant exit 1 / `false` (`fresh > TARGET`, and
  `self_pin == 2`); `measure:int:1` — same fixture, exit 0 vs exit 1 with the summary unchanged;
  `measure:int:0` — empty registry, `score=0` vs `score=1`; `measure:cmp:2` — one verified row, no `INVALID`
  lines vs `INVALID S001 ok`.
* coverage `entry_ok` — 3-line provenance trio: `(True,'ok')` vs `(False,'no provenance trio')` (`cmp:0`, `int:0`);
  6-token located quote: `True` vs `False` (`int:3`); 26-token located quote: `False` vs `True` (`int:4`);
  `group(2)`/`group(3)` indexes and `q.group(1) and q.group(2)` raise `IndexError`/`AttributeError`
  (`int:2`, `int:6`, `int:7`, `bool:3`).
* coverage `gt_rows` — one googletest row with a matching snapshot anchor: pristine returns `{'S256': …}`;
  `int:3`/`int:6` raise `IndexError`, `const:0` (`binary=False`) raises
  `TypeError: Strings must be encoded before hashing`.
* coverage `measure` — `int:0` passing fixture exit 0 vs 1; `int:1` failing fixture exit 1 vs 2; `const:0`
  `TypeError` traceback; `cmp:6` prints two `REFUSED … cites no googletest row` lines; `bool:5`
  `row_ids=S256,S257` vs `row_ids=-`; `cmp:9` `ENTRY …` vs `ENTRY … (not indexed)`.

Why these survived the round-46 selftest at all is a coverage fact, not an equivalence fact: the fixtures that
separate them are not in the round-46 case set (e.g. no case drives `parse_rows` cell mapping, `words()` bounds,
`grade()` overlap/length boundaries, `entry_ok` line-count/quote-length boundaries, the exit codes, or the
`check`/`live` modes).

## Retained evidence

| path | content |
|---|---|
| `.ufo/waves/round-47/w1/T47ExecPoolSweep.census.md` | the 61-row census (deliverable) |
| `/tmp/tameshi-r47-T47ExecPoolSweep/enum-{base,assembled}-{freshness,coverage}.txt` | the four enumerations (identical pairs) |
| `/tmp/tameshi-r47-T47ExecPoolSweep/enum-diff-{freshness,coverage}.txt` | both `diff` outputs, 0 bytes |
| `/tmp/tameshi-r47-T47ExecPoolSweep/v2-dummy-{freshness,coverage}.py` | assembled v2 + dummy addition |
| `/tmp/tameshi-r47-T47ExecPoolSweep/dummy-selftest-{freshness,coverage}.log` | `PASS D`, 35/21 cases, `VERDICT: PASS` |
| `/tmp/tameshi-r47-T47ExecPoolSweep/probe_pure.py`, `probe-pure.log` | 28 pure-rule probes (parse_rows, extract, words, grade, review_sets, entry_ok, gt_rows, Tree.read) |
| `/tmp/tameshi-r47-T47ExecPoolSweep/probe_measure.py`, `probe-measure.log` | 11 `measure()` probes over scratch git repos |
| `/tmp/tameshi-r47-T47ExecPoolSweep/diffs.txt` | `ast.unparse` unified diff per mutant (the site column source) |

Scratch repos: `tempfile.mkdtemp` under `/tmp/tameshi-r47-T47ExecPoolSweep/fix/`, each `git init -q -b m`,
`git -C <d> rev-parse --show-toplevel` asserted equal to the realpath'd scratch dir, one commit with
`-c user.name=t -c user.email=t@t`. No git or jj mutation was run in the lane.

## Risks and caveats

* The 22 mode-only rows follow the item's definition ("the code only runs in `--live`/`--check` modes"). `check()`
  is a plain function, so a `--check` invocation against a scratch lane would separate the nine `check:` rows; that
  mode is documented as a seat helper ("never a measurement") and `selftest()` does not call it. Whether such cases
  belong in a hardened selftest is the L1's call, not scored here.
* `gt_rows` was probed with a FakeTree exposing exactly the documented `read(path, binary=False)` contract that
  the real `Tree` implements; the real `Tree.read` was probed separately against a read-only `git show` at base.
* The census observes the pool's own mutant text (`ast.unparse` of the base source with the single site edited) —
  byte-identical to what `pool.judge` runs — so no observation depends on formatting drift.
* `parse_rows:int:3` (`source` cell) differs in `parse_rows`'s output while `source` is not consumed by the
  predicate; it is behavioural on the rule function, and its baseline was `survived` for the same reason as the
  other uncovered fields.
* No tool was installed or updated (host pacman is paused; nothing was needed). No deciding or `--targets` run was
  made, and no `--only`/`--rev` counter run was used; only the assembler, `--enumerate`, `--selftest` on /tmp
  assembled copies, and in-process `apply_mutant` probes.
