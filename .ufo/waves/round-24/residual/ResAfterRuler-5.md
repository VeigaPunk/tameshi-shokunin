# ResAfterRuler-5 — after.json fidelity and the "K4 control / seven mechanisms" reading

Item: run the frozen round24 ruler in a private clone at the delivered tip
`4903959687d16623adeeeae059bc010dcfc9d23f`, confirm 11/11 exit 0 and that the
ruler sha256 equals `before.json`/`after.json` `instrument_sha256`; then attack
`after.json` fidelity (does the recorded stdout match a fresh run row-by-row
ignoring temp paths?) and the lesson's After-measurement reading
("K4 control, ten moved, seven mechanisms").

## Verdict

**PASS on the measurement and on the receipt's fidelity; one MINOR
documentation defect (the "seven mechanisms" figure is not derivable from the
lesson text that asserts it), one MINOR receipt limitation (the recorded
`revision` is an operator claim the frozen ruler never verifies).**

- Fresh run at the tip: **11/11, exit 0**, stderr empty.
- `sha256(.ufo/evidence/round-24/measure.py)` at the tip =
  `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64`
  = `before.json.instrument_sha256` = `after.json.instrument_sha256`. Equal.
- `after.json`'s recorded stdout **reproduces exactly** at the recorded
  revision `c8c5b88…` and at the tip: 3 field diffs, all of them temp-path
  strings inside K11's `plan`; every other field of every row (including
  `stdout_tail`, `failing_cases`, K10's `bundle_sha256`) is byte-identical.
- `before.json` reproduces **raw byte-identical** at base `6a1821a…`.
- The lesson's "K4 is a carried control, so ten predicates were movable:
  0/10 → 10/10" is **accurate**. The "seven mechanisms" figure is
  **defensible but under-derived** (see Finding 3).
- No production file was edited. No git/jj write command was run in the lane.
  No tool was installed or upgraded (python3 3.x present; nothing needed).

## Environment / procedure (observed)

Host directive from L1: clone and heavy scratch placed under
`/fast/scratch/hyaku/tameshi-r24/ResAfterRuler-5/` (not `/tmp`).

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r24/ResAfterRuler-5/clone
git -C .../clone checkout --detach 4903959687d16623adeeeae059bc010dcfc9d23f
→ HEAD is now at 4903959 round-24: retain wave-1 spec, dispatch receipts, 64 seat reports, accounting and errata O-P
→ git rev-parse HEAD = 4903959687d16623adeeeae059bc010dcfc9d23f
```

`TMPDIR` was pointed at the scratch volume (the `/tmp` volume had filled
earlier); this changes only the temp-directory *prefix* of the ruler's
K11 paths, which is exactly the class of difference the item says to ignore.

### Run 1 — ruler at the tip (the item's Run step)

```
cd /fast/scratch/hyaku/tameshi-r24/ResAfterRuler-5/clone
TMPDIR=/fast/scratch/hyaku/tameshi-r24/ResAfterRuler-5/tmp \
  python3 .ufo/evidence/round-24/measure.py --repo "$PWD" > fresh-stdout.json 2> fresh-stderr.txt
EXIT=0
5298 fresh-stdout.json / 0 fresh-stderr.txt
```

`fresh-stdout.json` → `"discriminated": 11, "total": 11,
"schema": "tameshi-r24-hardening-v1"`; all eleven rows `discriminated: true`
(K1–K4 `restored_exit: 0`; K5/K6 `control` all `true` and `substituted` all
`false`; K7–K9 `exit 1` + `bundle_written false`; K10 `live_dependent ["one"]`;
K11 `fleet_root`/`repo`/`siblings` realpath-normalised).

### Digests

```
sha256sum .ufo/evidence/round-24/measure.py
0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64   (clone @ tip)
before.json  instrument_sha256 = 0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64
after.json   instrument_sha256 = 0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64
git log --oneline -- .ufo/evidence/round-24/measure.py
e338f1b round-24: freeze eleven-predicate hardening claim, ruler and before receipt
```

The ruler has exactly one commit in its history (`e338f1b`, before any seat),
so "frozen ruler bytes" is verifiable, not asserted.

### Run 2 — ruler at the *recorded* revision `c8c5b88…`

```
git clone --no-hardlinks … /fast/scratch/hyaku/tameshi-r24/ResAfterRuler-5/afterclone
git -C …/afterclone checkout --detach c8c5b88c8e961a929cdc351b95a7074c76958909
python3 .ufo/evidence/round-24/measure.py --repo "$PWD"   → EXIT=0
```

### Run 3 — ruler at the base `6a1821a…` (falsifies the "before" half)

```
git clone --no-hardlinks … /fast/scratch/hyaku/tameshi-r24/ResAfterRuler-5/baseclone
git -C …/baseclone checkout --detach 6a1821a8897eea6e7d9669292160ec9593669409
python3 <tip copy of>/.ufo/evidence/round-24/measure.py --repo "$PWD"   → EXIT=1
discriminated 1 / 11
K1 False | K2 False | K3 False | K4 True | K5 False | K6 False
K7 False tool-absent | K8 False tool-absent | K9 False tool-absent
K10 False tool-absent | K11 False tool-absent
```

## Finding 1 — after.json's recorded stdout reproduces exactly (PASS)

Field-level comparison of the recorded `after.json.stdout` against the two
fresh runs (JSON parsed, every key walked):

```
tip 4903959  field diffs: 3
   /rows[10]/plan/fleet_root   recorded: /tmp/tameshi-r24-measure-9r28nlgz/replay/fleet
                               fresh:    <TMPDIR>/tameshi-r24-measure-gv0e3s_n/replay/fleet
   /rows[10]/plan/repo         recorded: /tmp/tameshi-r24-measure-9r28nlgz/replay/fleet/lane-shokunin
                               fresh:    <TMPDIR>/tameshi-r24-measure-gv0e3s_n/replay/fleet/lane-shokunin
   /rows[10]/plan/siblings[0]  recorded: /tmp/tameshi-r24-measure-9r28nlgz/replay/fleet/other-shokunin
                               fresh:    <TMPDIR>/tameshi-r24-measure-gv0e3s_n/replay/fleet/other-shokunin
c8c5b88      field diffs: 3   (same three keys, same class of difference)
```

Everything else is byte-identical, including the parts a hand-assembled
receipt would most likely get wrong:

- K1–K4 `stdout_tail` strings (43/44 pass, the exact `CASE … FAIL` line and
  its neighbours) — identical;
- K10 `report.bundle_sha256 = 5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245`
  — identical (a digest over the fixture-derived bundle, so it is
  recomputable, not copyable);
- the JSON key order/indentation is exactly `json.dumps(indent=2,
  sort_keys=True)` as the ruler emits.

The recorded temp path shape is the ruler's own: the ruler uses
`tempfile.TemporaryDirectory(prefix='tameshi-r24-measure-')`
(`measure.py:209`), and the default TMPDIR yields
`/tmp/tameshi-r24-measure-q3ol0eag` (verified by an independent
`tempfile` call), i.e. the same `/tmp/tameshi-r24-measure-<8 chars>` shape as
the recorded `9r28nlgz`.

`after.json` metadata: `exit 0`, `stderr ""`, `revision c8c5b88…`, and the
working-tree copy is unmodified relative to its commit
`04657a6 round-24: retain replacement-L1 after receipt (11/11) and no-harm
receipt at c8c5b88` (`git diff --stat HEAD -- .ufo/evidence/round-24/after.json`
→ empty).

## Finding 2 — before.json reproduces raw byte-identically (PASS)

```
base fresh stdout == before.json['stdout']   → True (raw, no normalisation)
```

The base output contains no temp paths at all (K7–K11 are `tool-absent`), so
raw equality is the strongest possible form. This also corroborates seat
`RunRulerBase` (`.ufo/waves/round-24/w1/RunRulerBase.md`, "byte-identical") and
`RunRulerAfter` (11/11 at `c8c5b88`, `bundle_sha256 5c9aaf71…`, `plan
fleet_root=/tmp/tameshi-r24-measure-01u0aqib/replay/fleet`).

## Finding 3 — "seven mechanisms" is defensible but not derivable from the
lesson text (MINOR, documentation)

`corpus/lessons/round-24.md:66-69` (After-measurement, "Honest reading of
1/11 → 11/11"):

```
- K4 is a carried control, so ten predicates were movable: 0/10 → 10/10.
- They cover seven mechanisms. K1/K2 mutate one argv comparison, K5/K6 test
  one digest-pin mechanism on two rows, and K7/K8/K9 end in one refusal branch.
```

Parts that are **accurate**:

- "K4 is a carried control": `before.json` shows K4 `discriminated: true` at
  base with `CASE all-of-tokens FAIL` and `37/38 pass`; at the tip the same
  case still fails the mutant (`43/44 pass`). The compared logic is provably
  unchanged — the entire base→tip diff of `tools/command-binding.py` is the
  fixture loader (`tools/command-binding.py:161-172`), so the stdout-token
  check at `tools/command-binding.py:111` is byte-identical at both ends.
  K4 really is an unchanged-mechanism control, not a repair.
- "ten predicates were movable: 0/10 → 10/10": at base exactly one of eleven
  rows discriminated (K4) → 0 of the other ten; at the tip all ten do.
  Verified independently (Run 3 above).
- "K1/K2 mutate one argv comparison": both mutants patch the same single
  anchor `if receipt['argv'] != required['argv']:`
  (`tools/command-binding.py:103`; `anchor_count: 1` in both rows).
- "K5/K6 test one digest-pin mechanism on two rows": both rows pin the
  literal `"bundle_sha256": "…"` in `expect.stdout_contains`
  (`tools/registry.json` rows `command-binding-frozen-clean-pinned` and
  `command-binding-source-read-red-pinned`); one mechanism, two rows.
- "K7/K8/K9 end in one refusal branch": true of the code — the three
  detectors (`tools/registry-replay.py:87` `RUNNER_CLEANUP_FAILED`,
  `:90` `RUNNER_NOT_HELD`, `:97` `STREAM_LIMIT`) all feed the single refusal
  return `if findings: return 1, report, None` at
  `tools/registry-replay.py:109`.

Part that is **not derivable**: the sentence names only three mechanisms
(argv comparison, digest-pin, refusal branch) and leaves K3 (exit
comparison, `tools/command-binding.py:109`), K10 (live-dependent
classification, `tools/registry-replay.py:99-100`) and K11 (fleet/sibling
realpath, `tools/registry-replay.py:63-70`) unnamed. Counting *distinct
mechanisms covered by the ten moved predicates* with the lesson's own clause
applied ("K7/K8/K9 end in one refusal branch" ⇒ one mechanism) gives **six**:
argv comparison, exit comparison, digest-pin, refusal branch, live-dependent
classification, realpath identity.

The figure **seven** is reachable — and is correct — under the corpus's own
weak-link taxonomy in `corpus/knowledge/replay-projection-hardening.md:11-21`
("Weak link | Hardened rule"), which splits the refusal family into two rows
("replay publishes a bundle although the runner rejected a row" for K7/K8 and
"unbounded retained streams" for K9) and carries eight predicate-bearing rows,
of which seven are covered by the ten *moved* predicates (the eighth, the
stdout any-token row, is the K4 control):

| # | mechanism (weak-link row) | predicates | site |
|---|---|---|---|
| 1 | argv comparison | K1, K2 | `tools/command-binding.py:103` |
| 2 | exit comparison | K3 | `tools/command-binding.py:109` |
| 3 | registry row `bundle_sha256` literal | K5, K6 | `tools/registry.json` (pinned rows) |
| 4 | replay refusal: rejected / cleanup-failed rows | K7, K8 | `tools/registry-replay.py:87,90,109` |
| 5 | stream-bound refusal | K9 | `tools/registry-replay.py:97,109` |
| 6 | live-dependent classification | K10 | `tools/registry-replay.py:99-100` |
| 7 | fleet/sibling realpath identity | K11 | `tools/registry-replay.py:63-70` |

So the number is not false; it is imported from a taxonomy the lesson does not
name, and the same unexplained figure is repeated at
`SCORECARD.md:1163` ("The ten moved predicates cover seven mechanisms") and
`corpus/knowledge/replay-projection-hardening.md:47` ("ten predicates moved,
covering seven mechanisms"). A reader who applies the lesson's own grouping
gets six and has no way to reconcile it from the sentence.

Severity: **minor** — a claim-precision/traceability defect in prose, not a
numeric falsity in the measurement. It does not touch the 1/11 → 11/11 pair.

## Finding 4 — the receipt's `revision`/`cwd` are operator claims the frozen
ruler never verifies (MINOR, receipt limitation)

`measure.py` never inspects the `--repo` checkout (no `git rev-parse`
anywhere in the file); `after.json`'s `revision` and `cwd` fields are asserted
by the operator who ran it. I corroborated them externally — the run
reproduces 11/11 at `c8c5b88` *and* at the tip `4903959`, and the recorded
temp-path shape is the ruler's own — but the receipt alone carries no proof
that `--repo` was at `c8c5b88`. This is inherent to a frozen ruler and cannot
be fixed without touching frozen bytes; the honest fix is documentation, not
a re-run.

## Finding 5 — freeze verified in the tip range (INFO)

```
git log --oneline 6a1821a..4903959 -- tools/registry.json      → d2eaecd (one commit)
git log --oneline 6a1821a..4903959 -- tools/registry-replay.py  → d2eaecd (one commit)
git log --oneline 6a1821a..4903959 -- tools/command-binding.py  → d2eaecd (one commit)
git log --oneline -- .ufo/evidence/round-24/measure.py          → e338f1b (one commit)
git log --oneline -- .ufo/evidence/round-24/extra-cases.json    → d2eaecd (one commit)
git log --oneline 6a1821a..4903959 -- .ufo/evidence/round-23/extra-cases.json
    …/round-23/replay/bundle.json …/replay/expected.json
    …/round-23/source-read-bundle.json …/round-23/source-read-expected.json
    …/round-23/correct-command-bundle.json tools/registry-check.py   → (empty: untouched)
```

So "no tool, fixture, ruler or registry bytes changed after wave 1" holds
structurally in the tip range: every one of those paths last changed at
`d2eaecd` (before the wave) or `e338f1b` (the ruler freeze). The new
round-24 fixture set adds six cases (`argv-swapped-between-names`,
`argv-case-only`, `argv-padded-token`, `argv-repeated-flag`,
`negative-exit-mismatch`, `negative-exit-declared-match`), 38 → 44 selftest
cases, which is what actually moves K1–K3.

Observation, out of scope but noted: the lane working tree carries two
untracked files, `.ufo/evidence/round-24/final-verification.json` and
`.ufo/waves/round-24/residual-dispatch.json` (this wave's dispatch
scaffolding); neither is referenced by the claim, and `after.json` itself is
tracked and unmodified.

## Smallest safe correction

1. (Finding 3, prose only — no frozen byte changes) Append one clause to
   `corpus/lessons/round-24.md` in the After-measurement bullet naming the
   seven mechanisms explicitly and their source taxonomy, e.g.:

   > "They cover seven mechanisms — argv comparison, exit comparison, the
   > registry row's `bundle_sha256` literal, the replay refusal for
   > rejected/cleanup-failed rows, the stream-bound refusal, live-dependent
   > classification, and fleet/sibling realpath identity — counted over the
   > ten moved predicates, using the weak-link rows of
   > `knowledge/replay-projection-hardening.md` (K7/K8/K9 are three
   > detectors that end in one refusal return)."

   and mirror the same seven-name list in `SCORECARD.md:1163` and
   `corpus/knowledge/replay-projection-hardening.md:47`. This is
   append-only prose and leaves `before.json`, `after.json`, `measure.py`,
   the fixtures and the registry untouched — the frozen pair stays valid.
2. (Finding 4) Do **not** re-run or edit `after.json`. The revision claim is
   already corroborated by two independent reproductions (at `c8c5b88` and at
   the tip); state the corroboration in the wave accounting rather than
   modifying the receipt.
3. No change is required to `measure.py`, the fixtures, the registry rows, or
   the 1/11 → 11/11 pair: my runs reproduce both endpoints exactly.

## What I checked (and did not)

Checked: ruler reproduction at tip, at the recorded revision, and at base;
digest equality of instrument/before/after; field-level stdout equality;
temp-path shape provenance; freeze history of every tool/fixture/registry
path; K4-as-control by diffing `tools/command-binding.py` base→tip; the
lesson's and SCORECARD's/knowledge's mechanism counts against the code sites
and against the knowledge table's weak-link taxonomy; the two seat reports
`RunRulerAfter`/`RunRulerBase`.

Not checked (out of item scope): the 64 seat reports' individual claims, the
no-harm receipt, the monitor re-anchors, the errata E–P accuracy, the
replay/registry-run receipts, and any producer-authentication or score
question.

## Bounds kept

- Wrote exactly one file: this report
  (`.ufo/waves/round-24/residual/ResAfterRuler-5.md`; its parent directory
  `.ufo/waves/round-24/residual/` had to be created because it did not
  exist). No other path in the lane was written.
- No production file edited; no `git`/`jj` write command run in
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (only `GIT_OPTIONAL_LOCKS=0`
  read-only `log`/`diff`/`status`/`rev-parse`); the fleet repo, sibling lanes
  and the Git index were not touched.
- All clones and scratch under
  `/fast/scratch/hyaku/tameshi-r24/ResAfterRuler-5/` (host directive), never
  `/tmp`; the ruler's own temp copies were placed there via `TMPDIR`.
- No seat spawned. No tool installed or upgraded (none needed; python3
  present) — recorded per the operator tooling directive.
- Not claimed: producer authentication, promotion, or numeric score uplift.
