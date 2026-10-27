# T53W1Read14 — cold read of `### Round-14 historical registry — superseded by round 15`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content revision (C\*): `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Section content was read **only** through git objects
  (`git -C <lane> show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md`); the lane working tree was
  never used as section content.
- Frozen boundary reproduced with the round-18 sectionizer the round-53 C1 counter imports
  (`.ufo/evidence/round-18/measure.py`, `R18` at
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-53/c1/measure.py:39`):
  `{'start': 1604, 'end': 1615, 'sha256': '06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af'}`
  — i.e. SKILL.md lines 1604–1614 inclusive, 11 lines, no trailing newline.
- `section_sha256 = 06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af`
- Verdict: **1 finding** (stale entry command). Every other statement in the section holds at C\*.

## Environment

- Scratch clone (deleted before yielding): `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read14/lane`,
  `git clone --no-hardlinks <lane>` then `git checkout -B probe C*`;
  `git rev-parse --show-toplevel` printed the clone dir, `git rev-parse HEAD` printed
  `a41195dfc13a73958e4c5228ec196b28d03ded03`.
- `python3` from the host; `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` present on PATH
  (relevant only to the section's self-test column).
- No tool was installed or updated for this seat.

## Checks run

| # | check | command | outcome |
|---|---|---|---|
| 1 | SKILL.md at C\* | `git -C $lane show C*:SKILL.md \| wc -l` | 2178 lines; `sha256sum` = `c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee` |
| 2 | frozen split | imported `C*:.ufo/evidence/round-18/measure.py`, called `sectionize(raw)` | 64 sections; target = `start 1604, end 1615, sha256 06a6864f…59af` |
| 3 | independent recompute | own splitter (`^#{1,3}(\s\|$)` outside ``` fences at C\*, trailing whitespace-only lines stripped, `'\n'.join`, sha256 over UTF-8 `surrogateescape`, no trailing newline) | same boundary 1604–1614 and same digest `06a6864f…59af`; the split is reproduced before hashing |
| 4 | heading provenance | `sed -n '1604p'` on the C\* dump | `### Round-14 historical registry — superseded by round 15` |
| 5 | the row's printed entry command, run at C\* | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | **exit 2**, `{"status":"could_not_evaluate","exit":2,"id":"expected_input_digest_mismatch"}`, message `tools/bash-witness-study.py: observed cca77724c47619d73902458067aaa9dae8b8f6ea9d4a3ae8507390a3dc8ae85d expects 49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80` |
| 6 | the named live entry | `… --dispositions .ufo/evidence/round-18/dispositions.json --json` | exit 0, `status: clean`, 12 rows |
| 7 | the round-17 claim | `… --dispositions .ufo/evidence/round-17/dispositions.json --json` | exit 2, `expected_input_digest_mismatch` (same drifted path) — the section's "round 17's now exits 2, bash-witness moved" holds |
| 8 | the self-test column | `TMPDIR=<scratch> python3 tools/evidence-disposition.py --selftest` | `SELFTEST: PASS (66/66)`, exit 0, includes `argv-never-executed PASS (marker absent=True)` and `usage-* PASS (exit=64 expects=64)` |
| 9 | normal-mode write scope | `git status --porcelain` in the clone after checks 5–7 | empty — normal mode wrote nothing into the lane tree (the only `mkdtemp` in the tool, `tools/evidence-disposition.py:2351`, is on the `--selftest` path) |
| 10 | pin counts | `C*:.ufo/evidence/round-13/expected.json` | `inputs 13`, `expected_checks 12` |
| 11 | before-counterpart pins | compared `round-14/dispositions.json` and `round-14/dispositions-before.json` | both v1, `expected_file` identical, `inputs` maps byte-identical (3 pins each), 12 rows each |
| 12 | archived capture script | `git ls-tree C* .ufo/evidence/round-14/capture-context.py` | `100755 blob 3601d26327cc633443d425bb3eaef5d93edc0b77`; `grep -c selftest` = 0, so the row's "helper-only controls do not satisfy the standalone gate selftest" is consistent |
| 13 | round-13 pin manifest + context receipt | `git show C*:.ufo/evidence/round-13/pin-manifest.json \| sha256sum` / same for `round-14/context-receipt.json` | `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` and `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` — the values other sections pin for those two retained files, so "unchanged" holds |
| 14 | exit-map legend | `tools/evidence-disposition.py` docstring at C\* (3223 lines) | `Exit map: 0 clean / 1 failed semantic expectation / 2 could-not-evaluate … / 64 usage error` — the printed map is faithful to the tool |

## Holds (verified against C\* bytes)

- **H1 — header claim "superseded by round 15".** The page carries
  `### Round-15 gate/probe registry` (C\* `SKILL.md:1683`) whose `effective expectation disposition`
  row (`:1688`) re-registers this gate and states the supersession explicitly, so the heading's
  claim lands on a real successor.
- **H2 — pinned targets exist and are pinned as stated.** `.ufo/evidence/round-14/dispositions.json`
  (v1, 12 rows) and its before counterpart `round-14/dispositions-before.json` both exist at C\* and
  pin the same three inputs; the historical expected file they point at
  (`.ufo/evidence/round-13/expected.json`) carries **13** input pins — the row's
  "historical expected pins13 original inputs" is substantively true (see the noted typo below).
- **H3 — "round 17's now exits 2, bash-witness moved".** Check 7: exit 2,
  `expected_input_digest_mismatch`, on `tools/bash-witness-study.py`. The round-14 v1 manifest has no
  `historical_inputs` waiver (v1 schema), which is exactly why the drift is fatal rather than waived.
- **H4 — "live entry since round 18: `.ufo/evidence/round-18/dispositions.json`".** Check 6: exit 0,
  `clean`, 12 rows; the manifest exists at C\* with sha256 `9caa2f76…2676`.
- **H5 — self-test command `python3 tools/evidence-disposition.py --selftest`.** Check 8: PASS 66/66,
  exit 0 at C\*. The column prints the command without its `jj` prerequisite; on this host `jj` is
  present, so the command as printed holds (recorded as a documentation thinness, not a finding).
- **H6 — write scope "normal mode read-only lane evidence, stdout only".** Checks 5–7 + 9: three
  normal-mode runs left `git status --porcelain` empty; `mkdtemp` exists only in the selftest path.
- **H7 — the closing paragraph's authority caveats.** The tool docstring says pins are configured
  authority, that stored argv is never re-executed, and that receipt-only checks stay informational
  and never become expectations — the paragraph is a faithful summary, not an overclaim.
- **H8 — second table row (`archived invocation context capture`).** "do not run" + "retained source
  … only" matches check 12: the retained script is a blob at C\*, has no self-test surface, and no
  other row in this section registers an invocation for it.

## Finding

### F1 — class `stale-entry-command`: the row's own printed entry command is dead for a verdict at C\*

Verbatim quote from the section's `Entry command` cell:

```
(historical; live entry since round 18: `.ufo/evidence/round-18/dispositions.json`; round 17's now exits 2, bash-witness moved)
```

Why it fails. The note explains the exit-2 drift for round 17's manifest and points at round 18 as
the live entry, but it leaves the row's own printed command presented as the historical entry with
"0 clean" first in its verdict map. Run at C\* (check 5), that exact command —

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
```

— exits 2 (`could_not_evaluate`, `expected_input_digest_mismatch`) because
`tools/bash-witness-study.py` no longer matches its round-13 pin (observed
`cca77724c47619d73902458067aaa9dae8b8f6ea9d4a3ae8507390a3dc8ae85d`, expects
`49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`), and the round-14 manifest is v1
with no `historical_inputs` waiver. Nothing the row prints can be run to a 0/1 disposition. The
page's own round-15 registry (C\* `SKILL.md:1688`) states the fact the section omits — "since round 16
this command returns 2 `expected_input_digest_mismatch` at `--root .` because the runner input moved"
— so the two registries disagree about whether this command evaluates: the round-15 row carries the
drift warning for the round-14 command, this round-14 row carries it only for round 17's.

Scope of the claim. This is a completeness/pointer defect, not a runnable falsehood: exit 2 does fall
inside the printed legend. The failure is that the row's historical entry is presented as the runnable
receipt for this gate while its only live pointer (round 18) sits in a parenthetical, and a cold reader
who runs the printed command gets `could_not_evaluate` with no statement in this section saying so.

## Noted text defects, deliberately not counted as findings

Both are visible in the C\* bytes but do not make a statement in the section false, so they are not
claimed as findings:

1. `historical expected pins13 original inputs` — missing space between `pins` and `13`. The intended
   count is true (check 10: `inputs 13`).
2. The self-test column prints `python3 tools/evidence-disposition.py --selftest` without the tool's
   documented `jj` prerequisite (`Selftest also requires jj for its isolated colocated-repository
   cases`); with `jj 0.45.1` on PATH the command passes 66/66 (check 8).

## Residual risk

- Checks 5–7 ran in a `git clone` of the lane checked out at C\* (detached branch `probe`), not in the
  lane working tree; the tool requires `<root>/.git`, so a clone was necessary. The tree bytes are the
  C\* tree (`git rev-parse HEAD` = C\*, `git status --porcelain` empty before and after the runs).
- Only the three named manifests were executed. No other row of the page was run, and
  `capture-context.py` was deliberately not executed.
- I did not evaluate whether re-pinning the round-14 manifest is the right repair; the finding records
  only the observable state at C\*.
