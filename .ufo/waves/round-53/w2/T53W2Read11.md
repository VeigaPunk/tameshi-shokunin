# T53W2Read11 — wave-2 re-read of `### Round-14 historical registry — superseded by round 15`

Seat: re-reader (T53W2Read11), wave 2, round 53, lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Candidate read: **C\*\* = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`**, through git objects only (the lane
working tree was never read for section content):

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md
  -> 2189 lines, sha256 4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d
```

Frozen section boundary, computed with **the sectionizer the round-53 C1 counter imports**
(`.ufo/evidence/round-18/measure.py`, `sectionize()`, reached via
`.ufo/evidence/round-53/c1/measure.py:39` `R18`), extracted from C\*\* itself:

```
{'start': 1615, 'end': 1626, 'heading': '### Round-14 historical registry — superseded by round 15',
 'sha256': '06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af'}
```

i.e. SKILL.md lines 1615–1625 inclusive (11 lines, `end` is exclusive), no trailing newline.
`section_sha256 = 06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af`

**Verdict: 0 findings.** The section is byte-identical to C\*, which is exactly the stated wave-1 fix
("no content change needed beyond cross-section line drift"), and every statement it makes holds at C\*\*.

## 1. Fix verification (FIRST)

The item's parenthetical names the wave-1 fix as **"no content change needed beyond cross-section line
drift"**. Verified, in this order:

1. Split both revisions with the frozen sectionizer and compared the section bodies byte for byte:

```
diff -u <C*:a41195dfc13a73958e4c5228ec196b28d03ded03 section> <C**:5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e section>
  -> empty; IDENTICAL_SECTION (1641 bytes each)
```

```
C*   {'start': 1604, 'end': 1615, 'sha256': '06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af'}
C**  {'start': 1615, 'end': 1626, 'sha256': '06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af'}
```

2. The only change is the line span: start **1604 → 1615** and end **1615 → 1626**, a uniform **+11**
   shift with an unchanged 11-line body and an unchanged digest — the "cross-section line drift" the fix
   describes. No in-section edit was expected, so there is no in-section edit to miss.
3. The heading arrives at C\*\* outside any ``` fence (checked: the body contains no fence marker), so the
   frozen splitter and an independent reimplementation agree on the boundary.

## 2. Environment

- Fixture clone (deleted before yielding): `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read11/lane`,
  `git clone --shared <lane>` then `git checkout 5b703c6ff3ff…`;
  `git rev-parse --show-toplevel` printed the clone dir, `git rev-parse HEAD` printed
  `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`, `git status --porcelain` empty before and after all runs.
- `TMPDIR=/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read11/tmp` for every tool invocation; no `/tmp` use.
- `python3` from the host; `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` on PATH (needed only by the
  section's self-test column). No tool was installed or updated for this seat; pacman was never invoked.

## 3. Checks run

| # | check | command | outcome |
|---|---|---|---|
| 1 | fix: section unchanged C\* → C\*\* | frozen `sectionize()` on both revisions, then `diff` of the bodies | identical, `06a6864f…59af` both revisions; only start/end moved +11 |
| 2 | fix: line drift only | `sed -n '1615p;1626p;1627p' SKILL_C**.md` | 1615 = heading; 1626 = blank; 1627 = `## Context gate classification and explicit exit classes — round 15` |
| 3 | split reproduced before hashing | independent splitter (`^#{1,3}(\s|$)` outside fences, trailing blank lines stripped, `'\n'.join`, sha256 over UTF-8 `surrogateescape`) | line 1615, next heading 1627, 11 lines, sha `06a6864f…59af`, no fence in body — agrees with the frozen boundary |
| 4 | row 1 printed entry, at C\*\* | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | **exit 2**, `{"status":"could_not_evaluate","exit":2,"id":"expected_input_digest_mismatch"}` on `tools/bash-witness-study.py`: observed `4e999ff4553948e4fffdbc55f7a18c3d41604af4acb3292a8499fb6cb4557142`, expects `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80` |
| 5 | "round 17's now exits 2, bash-witness moved" | `… --dispositions .ufo/evidence/round-17/dispositions.json --json` | exit 2, `expected_input_digest_mismatch`, same `tools/bash-witness-study.py` drift |
| 6 | "live entry since round 18" | `… --dispositions .ufo/evidence/round-18/dispositions.json --json` | **exit 0**, `status: clean`, `rows=12`, no finding ids |
| 7 | verdict map exit 1 | `… --dispositions .ufo/evidence/round-18/dispositions-before.json --json` | exit 1, `status: failed` (the "1 failed semantic expectations" class is live) |
| 8 | verdict map exit 64 / 0 / 2 classes | `TMPDIR=… python3 tools/evidence-disposition.py --selftest` | `SELFTEST: PASS (66/66)`, exit 0; cases `usage-* PASS (exit=64 expects=64)` |
| 9 | write scope "stdout only" | `git status --porcelain` in the clone after checks 4–8 | empty — normal mode wrote nothing into the tree |
| 10 | pinned values: manifests | `json.load` of `.ufo/evidence/round-14/dispositions.json` and `…-before.json` | both schema `evidence-dispositions-v1`, `expected_file: .ufo/evidence/round-13/expected.json`, `inputs` 3 pins, `rows` 12 each |
| 11 | "historical expected pins13 original inputs" | `json.load('.ufo/evidence/round-13/expected.json')` at C\*\* | `len(inputs) == 13` |
| 12 | "literal isolated selftest expectations in tool" | `grep -n "SELFTEST" tools/evidence-disposition.py` | literals `SELFTEST_ORACLE_PY`, `SELFTEST_FIXTURE_INPUT`, `SELFTEST_TOOL_V1/V2/OTHER/CRLF`, `SELFTEST_V1_DOC` (lines 1709–1717); fixtures written under `tempfile.mkdtemp(..., dir=strict_scratch_root())` (line 2365) |
| 13 | closing paragraph, sentence 1 | `sed -n '1,15p' tools/evidence-disposition.py` | "Pins in the dispositions document are configured authority for the bytes read here; they are not an authentication or preregistration claim" |
| 14 | closing paragraph, sentence 2 | same docstring | "It never executes receipt argv." / "passing this gate does not prove that any recorded command was rerun" |
| 15 | closing paragraph, sentence 3 | `grep -n` accounting + `sed -n '1130,1160p'` | rows are validated against `expected_checks` only: `row_unknown` "row name is not an expected_checks key", `row_missing` "expected check has no disposition row"; expected rows come from `expected_file` only (no receipt-derived rows) |
| 16 | exit map legend | `grep -n "Exit map" -A6 tools/evidence-disposition.py` | `0 clean`, `1 failed semantic expectation`, `2 could-not-evaluate: missing/unreadable/malformed/tampered/path-invalid input…`, `64 usage error` |
| 17 | row 2 "retained source … only" | `git ls-tree -r --name-only HEAD .ufo/evidence/round-14`; `sha256sum` | `.ufo/evidence/round-14/capture-context.py` present, sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` (the digest the round-15 section states for it) |
| 18 | row 2 "helper-only controls do not satisfy the standalone gate selftest" | `grep -c selftest .ufo/evidence/round-14/capture-context.py` | `0` — no selftest surface exists in the archive |
| 19 | row 2 "unchanged round13 pin manifest and context receipt" | `git log --oneline -- <path>` for both, plus `sha256sum` | pin-manifest added once (`4acc607`), context receipt added once (`6431478`), neither modified since: `64eaa43e…0af6` and `05cb55b8…9c1a` (the receipt digest the round-15 section pins as the frozen clean receipt) |
| 20 | row 2 "no supported invocation" | `grep -n capture-context tools/registry.json` | no registry row invokes `.ufo/evidence/round-14/capture-context.py`; the registered context rows invoke the maintained `tools/context-capture.py` |
| 21 | heading "superseded by round 15" | read C\*\* successor sections | `## Context gate classification and explicit exit classes — round 15` (line 1627) and `### Round-15 gate/probe registry` (line 1694) both exist and re-register this gate |
| 22 | "live entry since round 18" is still the newest | `ls .ufo/evidence/*/dispositions*.json`; `json.load('tools/registry.json')` | newest manifest is round-18; rows `evidence-disposition-round17*` and `evidence-disposition-round14-superseded` carry `superseded_by` naming round-18; `evidence-disposition-round18` is `active` |

## 4. Holds (verified against the C\*\* bytes)

- **H1 — heading claim.** "Round-14 historical registry — superseded by round 15" lands on a real successor:
  the round-15 classification section says "The round-14 registry history is retained above with an inline
  archive marker, not a callable entry", and the round-15 registry row re-registers `effective expectation
  disposition` as **superseded in round 17** with the drift statement for this exact argv. And
  `tools/registry.json` carries `evidence-disposition-round14-superseded` with
  `superseded_by: evidence-disposition-round18`. Three independent surfaces agree with the heading.
- **H2 — "historical; live entry since round 18: `.ufo/evidence/round-18/dispositions.json`".** Check 6: exit 0,
  `clean`, 12 rows at C\*\*, *after* the wave-1 fix pass also edited `tools/evidence-disposition.py`
  (C2 `$TMPDIR` helper, +16 lines). Check 22: no newer manifest supersedes round-18.
- **H3 — "round 17's now exits 2, bash-witness moved".** Check 5: exit 2,
  `expected_input_digest_mismatch`, on `tools/bash-witness-study.py`; the round-14 v1 manifest has no
  `historical_inputs` waiver, which is why the same drift kills its own command too.
- **H4 — verdict map.** Every code the row prints is live at C\*\*: 0 (check 6), 1 (check 7), 2 (checks 4–5),
  64 (check 8 usage cases). The row is a faithful abbreviation of the tool's own `Exit map:` block (check 16).
- **H5 — self-test command.** `python3 tools/evidence-disposition.py --selftest` → `PASS (66/66)`, exit 0.
- **H6 — pinned values.** Both v1 manifests exist, pin the same three historical inputs and the same
  `expected_file`; the expected file carries exactly **13** original input pins; the self-test expectations are
  literals inside the tool with isolated fixture trees (checks 10–12).
- **H7 — write scope.** Normal mode is read-only over lane evidence and writes only to stdout: three normal-mode
  runs (checks 4–7) left the tree clean; the only `mkdtemp` is on the `--selftest` path.
- **H8 — archived row.** Retained source present and unreferenced by any registry row; it has no selftest
  surface; the two retained inputs it names are added-once files whose digests match the page's own pins.
- **H9 — closing paragraph.** All three sentences are the tool's own documented contract (checks 13–15), not an
  overclaim: pins are configured authority, argv is never executed, and an unmapped receipt-only check cannot
  become an expected row because rows are validated only against `expected_file`'s `expected_checks`.

## 5. Wave-1 finding, adjudicated at C\*\* (not re-filed)

Wave-1 (`T53W1Read14.json`, F1, class `stale-entry-command`) argued that the row's own printed command is dead
for a 0/1 disposition while the note blames the drift on round 17's manifest only:

```
(historical; live entry since round 18: `.ufo/evidence/round-18/dispositions.json`; round 17's now exits 2, bash-witness moved)
```

F1's factual premise **reproduces at C\*\*** — and with a different live digest than wave 1 saw, because C\*\*
itself edited `tools/bash-witness-study.py`: observed `4e999ff4…7142` now (wave 1 saw `cca77724…e85d`),
expects `49e9e5e2…ad80`; exit 2, `expected_input_digest_mismatch` (check 4). It is nevertheless **not a finding
at C\*\*** under the wave-2 bar (a statement that does not hold):

1. The row labels the command **historical** and the heading declares the registry **superseded by round 15**;
   the command is not presented as live.
2. The pointer it does present as live — round-18 — resolves **clean, exit 0** at C\*\* (check 6), so no
   stale-as-current pointer exists in the section.
3. The observed exit code, 2, is inside the printed verdict map, and the successor row at C\*\*
   `SKILL.md:1699` states the fact for this exact argv: "**superseded in round 17**: since round 16 this
   command returns 2 `expected_input_digest_mismatch` at `--root .` because the runner input moved". The page
   therefore does not present the 0-clean outcome as current; F1's own text concedes it is
   "not a runnable falsehood".
4. The lane's registry agrees with the supersession and stays coherent with it: the row
   `evidence-disposition-round14-superseded` keeps `expect: {exit: 0}` but is `status: superseded` with
   `superseded_by: evidence-disposition-round18`; `tools/registry-check.py` runs superseded rows for
   visibility, prints `ROW <name> superseded expect=<exit> got=<exit>` and **excludes them from `held=N/M`**
   (docstring lines 30–36, `print_human`), so a superseded row's changed outcome is surfaced, never graded as
   the active contract.

So the wave-1 fix decision ("no content change needed") is consistent with the C\*\* bytes and with the rest of
the page; the underlying fact (the round-14 argv now exits 2) is recorded on the page by the successor row and in
the registry row's `superseded` status.

## 6. Noted text defects, deliberately not counted as findings

1. `historical expected pins13 original inputs` — missing space between `pins` and `13`. The count is true
   (check 11: `inputs` 13), so no statement fails.
2. The self-test column prints `python3 tools/evidence-disposition.py --selftest` without the tool's own
   prerequisite note "Selftest also requires `jj` for its isolated colocated-repository cases"
   (`tools/evidence-disposition.py:121`). On this host `jj 0.45.1` is on PATH and the command passes 66/66;
   a documentation thinness, not a false statement.

## 7. Findings

**None.** No statement in `### Round-14 historical registry — superseded by round 15` fails at
`5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`; the wave-1 fix (no content change beyond cross-section line drift)
is present exactly as described, and the section's digest is unchanged from C\*.

## 8. Residual risk

- The disposition runs were made in a `git clone` of the lane at C\*\* (the tool requires `<root>/.git`), not in
  the lane working tree; the clone's bytes are the C\*\* commit bytes and `rev-parse --show-toplevel` was asserted.
- The exit-2 verification is host- and revision-bound: `tools/bash-witness-study.py`'s live digest is a property
  of C\*\*, and a later re-pin would change it (that would change neither the row's "historical" marking nor the
  live round-18 pointer, both of which were checked directly).
- Whether round-18's manifest stays clean on a later revision is outside this read; at C\*\* it is clean.
