# tameshi round 74 — plan (frozen before any claim data)

Lane: tameshi-shokunin. Base: `3d6ea1ee8e551e3baf94904384890e3a112088f0`
(branch `master` = `origin/master`, clean tree — the round-73 non-author
verifier spot-check commit; round 73 was **admitted**,
`corpus/lessons/round-73-verifier-spotcheck.md` §7). Round shape: **one v1
wave, 12 seats** (policy `scripts/hyaku/ufo-wave-policy.json`, band 8–16;
attack seats by the policy's named set = 2 reviewer + 1 critic + 1
mutation-tester = 4 = 33.3 %; `labrat` is a frozen-topology seat the validator
rejects, so no labrat item exists — the planner seat stays with the L1 per the
orchestrator ruling).

Saturation state at round start (SCORECARD.md): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. A
capability entered the table at round 73 (`wave-record reconciliation`), so the
stagnation window (N = 2) is **not** exceeded and the nudge does not fire. C2
works the lowest scored numeric axis (calibration 8).

Two claims, distinct axes, causally separable: C1 lands only inside
`tools/wave-reconcile.py`, its mutant spec and its battery receipt; C2 lands
only inside `tools/additivity-range.py` + `tools/additivity-range.json`. Neither
needs the other's files, counters or commits.

## R74-C1 — operability (verdict-only): the three arm gaps round 73 named become measured arms

**Before (measured at base, receipt `.ufo/evidence/round-74/base-measure-r74.txt`).**
`python3 -I -X utf8 tools/wave-reconcile.py --selftest` → `WAVE_RECONCILE_SELFTEST:
12/12 pass`. The round-73 wave measured three rules whose mutants survive that
suite (`corpus/lessons/round-73.md` §Named coverage gaps): `m2` (`delimited :=
True`) reads 12/12 pass (T73W1S02), the span-substring rule has no arm at all
(same seat), and `W2` (`seat_reports` counting at any depth) survives 12/12 plus
the standing six-row sweep with a non-equivalence probe reading `files=12` vs
`13` (T73W1S10). The tool's own docstring says the two rules are "carried by NO
arm of this suite".

**After.** Three frozen arms are added and each is proven load-bearing by the
lane's own runner:

| arm | the rule it guards | fixture input that moves it |
|---|---|---|
| `arm13-printed-undelimited-refused` | a `printed` value must be a delimited token inside the bound span | span `11 reports`, `printed: 1` → setup refusal (`printed-not-in-span`) |
| `arm14-span-not-in-record-refused` | the record span must be a byte substring of the record at its rev | span `13 seats` absent from the fixture record → setup refusal (`span-not-in-record`) |
| `arm15-seatreports-top-level-only` | `seat_reports` counts the `*.md` files at the TOP of the wave dir only | a nested `x/nested/deep.md` beside 12 top-level reports: top-level=12 (`meet`), any-depth=13 (`drift`) |

Counting commands (pasteable; the first re-derives the after-state alone, the
second re-derives the load-bearing property):

```sh
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r74/l1/battery" \
  --label wave-reconcile-arms
```

Expected after-state: `WAVE_RECONCILE_SELFTEST: 15/15 pass` exit 0; the battery
reads `MUTANTS: total=3 killed=3 survived=0 inconclusive=0` (the runner's own
verdict lines) with a green control at the same arm count. Each mutant must be
killed by its named arm, not by a neighbouring one:
`m2` → arm13, span rule → arm14, `W2` → arm15.

**Kill rule (frozen).** C1 fails if (i) any of the three named mutants still
passes every arm; (ii) any mutant is killed by an arm other than the one it is
named against; (iii) any pre-existing arm 1–12 changes its `ok`/`got` outcome;
(iv) the arm count is not exactly 15; or (v) a new arm passes without its
mutant being applied (an always-fail arm is not a kill).

## R74-C2 — calibration (lowest scored numeric axis, 8; sourced on re-opened S294): append-only claims are measured over a whole commit range

**Before (measured at base, same receipt).** `tools/additivity-receipt.py`
measures ONE `(base, tip, file)` pair per call and judges append-only on the
CR-normalized comparison by default; it has no range mode
(`grep -c 'rev-list' tools/additivity-receipt.py` → `0`). The consequence is the
round-73 closure's two routed defects (`round-73-verifier-spotcheck.md` §6
items 1–2): `corpus/QUALITY.md` rewrote CRLF→LF at `21a7332f` and `LOG.md` at
`862e8844`, and no receipt covers those commits. Measured this round with the
existing tool: on the `LOG.md` pair the default judgement prints
`raw_old_only=3484 … norm_cr_old_only=0 eol_rewrite_disclosed=true` and exits
**0** — a receipt that reads clean while the rewrite is real; on the
`corpus/QUALITY.md` pair it prints `raw_old_only=1593` and exits 1, but the
class (a rewrite absorbed into a content judgement) is never declared.

**After.** `tools/additivity-range.py` (schema `tameshi-additivity-range-v1`)
+ `tools/additivity-range.json` sweep a declared commit range per file, with
two row kinds and an explicit claim class:

- kind `commits`: every commit in `base..tip` that changes the file is measured
  at `parent → commit` (first parent); the row is `violated` when any commit
  violates its claim class, and the worst commit is named.
- kind `pair`: one `base → tip` measurement (the range-total view the round-73
  closure printed).
- claim classes: `append-only-raw` (judged on `raw_old_only`), `append-only-content`
  (judged on the CR-normalized `norm_cr_old_only`).
- `expect: hold|violated` per row, so a standing red row MEASURES the mismatch
  on every sweep instead of assuming it away.
- exit 0 every row measured its expected status, 1 at least one did not, 2
  setup; a zero-row manifest, an unresolvable revision or an absent blob is a
  setup refusal before any row effect.

Standing manifest over the round-73 range `a3dd3574..3d6ea1ee` (six rows):

| row | file | kind | claim | expect | why |
|---|---|---|---|---|---|
| `r73-log-declaration-append` | `LOG.md` | commits `17cd1939^..17cd1939` | append-only-raw | hold | the round-73 declaration entry is a clean append |
| `r73-log-post-wave-append` | `LOG.md` | commits `e309f59f^..e309f59f` | append-only-raw | hold | the post-wave entry is a clean append |
| `r73-log-eol-rewrite` | `LOG.md` | commits `862e8844^..862e8844` | append-only-raw | violated | r73 routed defect 2: 3,484 raw lines removed, 0 normalized |
| `r73-quality-append` | `corpus/QUALITY.md` | commits `be1199d3^..be1199d3` | append-only-raw | hold | the criterion append is clean |
| `r73-quality-criterion-pin` | `corpus/QUALITY.md` | commits `21a7332f^..21a7332f` | append-only-raw | violated | r73 routed defect 1: 1,593 raw lines removed (5 normalized = the declared re-pin) |
| `r73-log-range-total` | `LOG.md` | pair `a3dd3574..3d6ea1ee` | append-only-raw | violated | the closure's range-total view (`raw_old_only` > 0) |

Counting command (pasteable):

```sh
python3 -I tools/additivity-range.py --repo . --manifest tools/additivity-range.json
```

Expected after-state: six `ADDRANGE_ROW` lines and `ADDRANGE: rows=6 met=6
unexpected=0` exit 0; the two rewrite rows print their measured
`raw_old_only` at the named commit with `norm_cr_old_only=0`.

**Kill rule (frozen).** C2 fails if (i) a do-nothing control can print the
frozen `ADDRANGE: rows=6 met=6 unexpected=0` line without reading the range —
the control is the existing per-pair tool's default judgement (exit 0 on the
rewrite pair, no range line) plus a stub that echoes each row's `expect`;
(ii) either rewrite row does not measure `raw_old_only > 0` with
`norm_cr_old_only = 0` at the named commit; (iii) flipping either rewrite row
to `expect: hold` does not print `unexpected=1` exit 1 (the rows are
load-bearing); (iv) the same manifest with the rewrite row's `claim` set to
`append-only-content` does not read `hold` (the two classes are distinct); or
(v) any other row's measured status cannot be re-derived by a reader from
committed bytes with plain git.

## Controls frozen before data

1. **C1 do-nothing control.** The pristine tool at base: 12/12 pass, the three
   mutants survive. It cannot reach `15/15` or the battery's `killed=3`.
2. **C1 echo control.** A stub that prints the expected selftest line is not
   accepted as evidence: the battery re-derives the arm outcome from the
   suite's own `SELFTEST … FAIL` lines, and the frozen per-mutant `got=` values
   are named in the receipt.
3. **C2 do-nothing control.** `tools/additivity-receipt.py` default judgement
   over the same two rewrite pairs: exit 0 (LOG) / exit 1 (QUALITY), no
   `ADDRANGE` line; a stub echoing `expect` cannot print the measured
   `raw_old_only` values the rows carry.
4. **C2 class control.** The same eight-row manifest built with each rewrite
   row's `claim` changed to `append-only-content` reads `hold` for both — the
   two classes are distinct measurements, not labels.

## Frontier step (inside the claim cap, not a fourth claim)

- `corpus/SOURCES.md`: **re-open S294** (Git `gitattributes`, held since round
  63) for the line-ending conversion ground; the fetch, the ≤25-word located
  quotes, the access date and the `used-by` old→new go in the round lesson's
  `## Gate`. A second candidate row (the `git-diff` page's `--ignore-cr-at-eol`
  option) is checked this round and is appended only if the ground is not
  already held; if it duplicates a held page it is REFUSED with the reason and
  flip.
- Census before → after: `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` (start receipt
  `.ufo/waves/round-74/census-start-r74.txt`, exit 0, 163 rows).
- One mistake mined into `corpus/lessons/round-74.md` `## Mistakes`.
- `considerthese/2026-10-28.md` proposal 4 (assimilation backlog burn-down) is
  the one still-unimplemented proposal this round may mine; if mined it lands
  as a lesson line with a measured backlog count, never as a claim.

## Write scope and scratch

Write scope: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; the report at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-74/tameshi.md`; `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`
appends only. Scratch root: `$HYAKU_SCRATCH/tameshi-r74/<seat>/` (default
`/fast/scratch/hyaku`), removed on exit; `/tmp` for files under 50 MB only.
Commits only through `scripts/hyaku/jj-lane.sh` (lane) and
`scripts/hyaku/fleet-commit.sh` (report).
