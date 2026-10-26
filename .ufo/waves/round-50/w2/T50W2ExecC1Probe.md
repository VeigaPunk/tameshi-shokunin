# T50W2ExecC1Probe — non-deciding probe of the frozen C1 counter (wave 2, round 50)

Seat: `T50W2ExecC1Probe`. Item: run the frozen C1 counter at the candidate
`80ea77e99e239982ab0b93e416645ef2359725d3`, paste its output, then try to break the PASS line
honestly by replacing five fixed rows' cited excerpts with unrelated keyed lines in the same file,
in a scratch clone. **This is a probe, not a verdict; the L1 owns the deciding run.**

## 0. Preconditions and disclosure

- Acceptance rule under test: `.ufo/evidence/round-50/c1/measure.py:114` (`has_key`) makes a witness
  "keyed" when a key substring is in the excerpt or the path *ends with* the key;
  `.ufo/evidence/round-50/c1/measure.py:120` (`check_evidence`) tests path, line range, excerpt
  presence and the ACK words; `.ufo/evidence/round-50/c1/measure.py:252` is the freshness refusal
  (`fixed-not-new`); floors at `:50-52`.
- Counter bytes were checked equal in three places before use:
  `sha256sum .ufo/evidence/round-50/c1/measure.py` and
  `git show <rev>:.ufo/evidence/round-50/c1/measure.py | sha256sum` for `cdbf24c0…` (freeze) and
  `80ea77e9…` (candidate) all print
  `ceee320c9ad84c89a7846fd746a072a60758a465d25ff80343fb95e0bd88ae29`. The run reports
  `self=ceee320c9ad8`, so the bytes scored here are the frozen bytes.
- System under test: `git diff` is never written; every read is `git -C LANE show REV:path`.
- Disclosure: the brief-ordered invocation is the only counter invocation at REV I made. It is
  read-only — no `--work`, no `OUTDIR`, and `measure.py` writes nothing (`main()` only reads
  `git show` blobs; `selftest()` is the only writer and was not run). It produced no deciding
  line; the L1's `deciding-run.sh` line is the deciding one.
- Fixture: one clone, `git clone -q --shared LANE /fast/scratch/hyaku/tameshi-r50/T50W2ExecC1Probe/lane`;
  `git rev-parse --show-toplevel` printed that clone before the first commit; every later git call
  names `-C <clone>`. The lane checkout was never written (final `git status --porcelain` shows only
  the untracked `.ufo/waves/round-50/w2/` paths). Mutated commits exist only in that clone; the
  receipts below carry the substituted rows verbatim so the runs are reproducible without it.
- Tooling: nothing installed or upgraded this seat (no pacman — the host guard pauses it — and no
  `uv`/`npx` need arose).

## 1. The counter at the candidate (verbatim)

```
$ python3 .ufo/evidence/round-50/c1/measure.py --lane . --rev 80ea77e99e239982ab0b93e416645ef2359725d3 --explain
C1_R50: self=ceee320c9ad8 rev=80ea77e99e239982ab0b93e416645ef2359725d3 defects=49 rows=49 fixed=31 open=7 declined=11 fixed_this_round=8 missing=0 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 total=0 C1_R50_PASS=true
EXIT=0
```

`--explain` printed no `EXPLAIN` line: no term fired. Floors are met with margin
(fixed 31 ≥ 20; declined 11 ≤ 12; `fixed_this_round` 8 ≥ 5). Receipt:
`.ufo/waves/round-50/w2/T50W2ExecC1Probe.candidate.stdout` (re-run inside the clone, identical
line). The spot-check digests (`spotcheck_changed=0`) and the frozen defect set pin
(`defects_pin=0`, sha256 `6a953e6e…`) both hold at the candidate.

## 2. Five fixed rows whose evidence I replaced with an unrelated keyed line

Method: in the clone at the candidate, each chosen row's `evidence` array was reduced to **one**
item — a line of the *same* file that (a) carries one of the item's `keys` (in its text or as a path
suffix), (b) is absent from that file at the item's `routed_at`, (c) carries no ACK word and (d) is
15–400 chars. That is exactly the counter's own acceptance test, so the substitution is not an
out-of-rule trick: it satisfies every clause the counter checks and none of the semantics the item
asked for. One commit carries all five
(`17eb76421f35718f1db034756e32c0ee0b63080b`, parent = candidate):

```
$ python3 .ufo/evidence/round-50/c1/measure.py --lane <clone> --rev 17eb76421f35718f1db034756e32c0ee0b63080b
C1_R50: self=ceee320c9ad8 rev=17eb76421f35718f1db034756e32c0ee0b63080b defects=49 rows=49 fixed=31 open=7 declined=11 fixed_this_round=8 missing=0 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 total=0 C1_R50_PASS=true
EXIT=0
```

**The line is byte-identical to §1 except for `rev=`: every counter term, the total and the PASS
value are unchanged by five fabricated witnesses.** Receipts:
`T50W2ExecC1Probe.mut5.stdout`, `T50W2ExecC1Probe.mut5-substitutions.txt`,
`T50W2ExecC1Probe.mut5-rows.json`.

| id | what the routed item asked (spot-check text) | witness I cited instead | why it is unrelated | accepted witnesses in that file |
|---|---|---|---|---|
| R41.3 | round-41 spot-check routed 3: successor pair must carry "self-pin, `records >= 1`, out-of-process tool execution, `resolved` inspection, exit-plus-FAIL kill oracle" | `.ufo/evidence/round-42/census/measure.py:377` — `print('C2_R42: SETUP self_pin=0 pin=%s rev=%s freeze=%s' % (pin, rev, freeze))` | a format string printed on self-pin *failure*. It supports at most the existence of a self-pin branch; it is silent on `records >= 1`, out-of-process execution, `resolved` inspection and the exit-plus-FAIL oracle — four of the five asks, in a compound item | 6 |
| R44.1 | round-44 spot-check routed 1: the `round-44.md` Gate quote is labelled "20 words" but tokenizes to ~28; "correct the label in a future round (append-only)" | `corpus/QUALITY.md:1256` — `line = open(lane + '/corpus/lessons/round-44.md', encoding='utf-8').read().split('\n')[25]` | a line of Python inside the criterion's falsifier heredoc. It reads the lesson; it says nothing about a corrected label, an errata line, or the measured count. It carries the file path only; the corrected label and the errata the item asks for are not in it | 6 |
| R47.1 | round-47 spot-check routed 1: "append a superseding row for `six-leg regression ledger` … `hermetic env-differential probe` … needs the same treatment" | `SCORECARD.md:2332` — the **`sources-registry`** row, keyed only because its evidence cell happens to contain the literal `runs 3 stable` | it is a *sibling* capability row. Neither of the two rows the item names is evidenced; the row would pass even if both target rows were deleted, because the key `runs 3` lives in 12 unrelated lines of the same table | 12 |
| R48.2 | round-48 spot-check routed 2: "write start and exit receipts before any output is read, and drop receipt directories from the frozen path list" | `.ufo/evidence/round-49/deciding-run.sh:30` — `mkdir -p "$SCR"; export TMPDIR="$SCR"` | scratch-directory setup. It is keyed only by the path suffix `deciding-run.sh`, so *every* line of the file (47/47) is "keyed"; this one touches neither receipt ordering nor the frozen list | 47 |
| R49.1 | round-49 spot-check routed 1: "an unreadable guard exits 1, where the docstring says 2 … Each fix needs a selftest case that fails before it" | `tools/pbt-staged-id.py:811` — `case_dir = os.path.join(work, case_dir_name)` | plumbing inside the new `workspace()` helper (added by the same commit `43bfa7ae`, verified with `git show 43bfa7ae -- tools/pbt-staged-id.py \| grep -c 'case_dir = os.path.join(work, case_dir_name)'` → `1`). It is neither the `os.access(guard, os.R_OK)` branch nor a selftest case; keyed only by the path suffix `pbt-staged-id.py` | 87 |

"accepted witnesses" = lines of the row's counter-acceptable path that satisfy the counter's own
evidence rules (keyed + new since routing + no ACK word + 15–400 chars); `T50W2ExecC1Probe.surface.tsv`
lists all 31 fixed rows. The widest surfaces: R40.1 108/109 (path-suffix key), R49.1 87, R43.2 56,
R48.2 47/47. The narrowest: R41.2, R41.4, R41.5, R46.4 with 1 alternative each.

## 3. Negative controls — what the PASS *does* check

Same method, two deliberate mistakes, each its own clone commit:

- **N1 (key dropped).** R41.3 evidence → `.ufo/evidence/round-42/census/measure.py:371`,
  `at_freeze = show(lane, freeze, SELF_REL)` (new, unrelated, but no key):
  `… key_miss=1 … total=1 C1_R50_PASS=false`, `EXIT=1`. So the substitution in §2 passes *because*
  it carries the key substring, not because evidence is ignored.
- **N2 (old text reused).** R47.1 evidence → `SCORECARD.md:242`, the pre-existing six-leg row
  sentence that is present at `routed_at`:
  `… fixed_bad=1 … total=1 C1_R50_PASS=false`, `EXIT=1`;
  `--explain` prints `EXPLAIN fixed-not-new R47.1`. The freshness test is a substring test over the
  whitespace-normalised *file*, which is stricter than line identity — it caught my first R41.4
  pick, whose text existed at `routed_at` under a different line wrap.

Receipts: `T50W2ExecC1Probe.n1.stdout`, `.n1-substitutions.txt`, `.n2.stdout`, `.n2-substitutions.txt`.

## 4. How wide the hole is: the same swap applied to every fixed row

`T50W2ExecC1Probe.sweep3-picks.txt` + `.sweep3-substitutions.json`: for each fixed row I took the
last alternative witness under the rule above from a path its cited commit actually touches.
**29 of 31 fixed rows admit one** (skipped: R40.4 and R48.5, whose keys occur only on the cited
lines). Swapping all 29 at once:

```
$ python3 .ufo/evidence/round-50/c1/measure.py --lane <clone> --rev 6141ca035e8d7639ae0deec90ad0e67dc39a9f45
C1_R50: self=ceee320c9ad8 rev=6141ca035e8d7639ae0deec90ad0e67dc39a9f45 defects=49 rows=49 fixed=31 open=7 declined=11 fixed_this_round=8 missing=0 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 total=0 C1_R50_PASS=true
EXIT=0
```

So the PASS survives 5 hand-judged semantic substitutions and 29/31 simultaneous mechanical ones.
(Unrelatedness was hand-judged only for the five in §2; the sweep's picks are arbitrary keyed new
lines, some of which are topically near their row.)

## 5. Incidental findings

1. **R41.4's cited commit does not touch its first evidence path.**
   `git diff-tree --no-commit-id --name-only -r --root -m 5f739acf21e8 | grep -E 'round-42/(census|calibration)/measure.py|lessons/round-42.md'`
   prints only `corpus/lessons/round-42.md`; the row's first item
   (`.ufo/evidence/round-42/census/measure.py`, `ledger` row evidence[0]) is dead weight — the row
   passes on its second item alone. No rule is broken (the counter needs one fresh item), but the
   extra item is not a witness for its own commit.
2. **Path-suffix keys make a whole file "keyed".** R49.1 (`pbt-staged-id.py`), R48.2/R48.3
   (`deciding-run.sh`), R40.1 (`corpus/lessons/round-41.md`) accept *any* new line of the file:
   108/109, 47/47 and 87/903 accepted lines respectively.
3. **The counter's `self=` field is read from the running file, not from REV**
   (`os.path.abspath(__file__)` in `self_sha()`, `.ufo/evidence/round-50/c1/measure.py:275`); the round-50 deciding script runs the REV bytes
   (`.ufo/evidence/round-50/deciding-run.sh:9`), so the deciding line is unaffected — and the three
   copies are byte-equal here anyway (§0).
4. **Compound items are not decomposed.** R41.3 (five mechanisms) and R49.1 (behaviour + a
   red-before selftest) each passed on a single keyed line, so a row may satisfy one clause of its
   ask and nothing else.

## 6. Reading of the result (probe, not verdict)

The PASS line is a bookkeeping verdict, not a semantic one. It constrains: the id set, one row per
id, status vocabulary, the fixed/declined/this-round floors, a key substring per row, freshness of
the cited text since `routed_at`, ancestry of the cited commit, that the commit touched the file,
absence of ACK words on the cited lines, and byte-stability of the ten spot-checks. It does not
constrain: that the cited line concerns the item, that the ask's behaviour exists, or that a
compound ask is wholly met. That is exactly the contract's declared blind spot
(`contract.json` C1 `cannot_see`, `measure.py` docstring "What it cannot see"), now quantified:
**5/5 hand-picked rows and 29/31 fixed rows can carry an unrelated keyed witness with a
byte-identical PASS line.** Consequence for the round-50 closure: a green C1 line certifies the
ledger's shape and floors, not that 31 routed defects are fixed; the wave-2 per-row semantic checks
(other seats) are the load-bearing evidence for the disposition, and any row on which they disagree
with the ledger voids the claim at the row, not at the counter.

## 7. Risks and blockers

- None blocking; no lane writes, no deciding invocation, no counter mutation, no model calls.
- Scope note: I did not test status misclassification (overclaim of `open`/`declined` on a fixed
  item) or the `Planned` paragraph rule — out of this seat's item; the frozen controls
  (`control/c1-CTL_OPEN.stdout`, `c1-CTL_PLANOPEN.stdout`, `c1-CTL_DECLINE.stdout`,
  `c1-CTL_FAB.stdout`) score the status and floor axes at freeze.
- Scratch `/fast/scratch/hyaku/tameshi-r50/T50W2ExecC1Probe` is deleted before yield; nothing citable
  lives there (the mutated rows and every counter line are copied into this directory).

## Receipts (this directory)

- `T50W2ExecC1Probe.candidate.stdout` — counter at the candidate, `EXIT=0`.
- `T50W2ExecC1Probe.mut5.stdout`, `.mut5-substitutions.txt`, `.mut5-rows.json` — the five-row swap.
- `T50W2ExecC1Probe.n1.stdout` / `.n1-substitutions.txt`, `.n2.stdout` / `.n2-substitutions.txt` — controls.
- `T50W2ExecC1Probe.sweep3.stdout`, `.sweep3-picks.txt`, `.sweep3-substitutions.json` — 29/31 sweep.
- `T50W2ExecC1Probe.surface.tsv` — accepted-witness count per fixed row.

## Summary

- Frozen C1 counter at the candidate: `total=0 C1_R50_PASS=true`, `fixed=31 open=7 declined=11
  fixed_this_round=8`, exit 0; no `EXPLAIN` term fired; counter bytes = freeze bytes
  (`ceee320c9ad8…`).
- Five fixed rows (R41.3, R44.1, R47.1, R48.2, R49.1) re-pointed at keyed but unrelated lines of
  the same file still print a byte-identical PASS line: the verdict is blind to semantic support.
- A mechanical sweep replaces the evidence of 29 of 31 fixed rows at once with the same PASS.
- Controls show the PASS depends on the key substring (N1 `key_miss=1`) and on freshness since
  routing (N2 `fixed_bad=1`, `fixed-not-new`), not on what the line says.
- Path-suffix keys make whole files "keyed" (R48.2 47/47, R49.1 87/903, R40.1 108/109); compound
  asks are not decomposed (R41.3, R49.1 passed on one line each).
- Incidental: R41.4's first evidence item is in a path its cited commit does not touch.
- Not a verdict: no deciding invocation was made; the L1's run decides.
