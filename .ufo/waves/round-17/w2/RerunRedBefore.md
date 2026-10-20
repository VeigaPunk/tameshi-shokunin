# RerunRedBefore — C1 red-before re-execution (round-17, wave 2)

Seat: RerunRedBefore. Attacked: the C1 red-before claim (`measure.py` with the round-16
ledger plus the e69b488 input overlay) at `e69b488`, `09ee1d0`, `eb7838b`, and the
overlay's 19-input provenance against an independent strace of the round-14 recipe
steps 2–3 at `e69b488`.

Execution clone: `/tmp/tameshi-r17w2-RerunRedBefore-gCFwxt/fleet/tameshi-shokunin`
(fleet-mirror layout, detached at `eb7838b16490ca7ba17ea3242ade76a61f744af2`;
`git status --porcelain` empty). Live-lane HEAD read-only = `eb7838b...`.
`measure.py` at the rev: sha256 `f348adc3d88a7adf98451b366bf7fdef1bafefc94df992961f2595c85a328c89`.
No tool installs or updates were needed (host `strace 7.2`, `python3 3.14`).

## 1. Red-before at the three revs

Command (cwd = clone root; the assignment form with `--repo $C`):

```
python3 .ufo/evidence/round-17/measure.py --repo "$C" --rev <R> \
  --ledger-rev 98bea7da5801f4bc58e4187690ee1687c8a5061f:.ufo/evidence/round-16/coldread/ledger.json \
  --inputs-overlay .ufo/evidence/round-17/redbefore/legacy-r14-inputs.json
```

All three exits 0; each run reports `overrides_used: true`, `trace_gate: "legacy"`,
`inputs_overlay_merged: 1` (by design a measurement aid, not a claim run).

| R | resolved revision | round-14 `sections[]` entry | whole-page `coldread.reasons` | covered/total |
|---|---|---|---|---|
| `e69b488` | `e69b488f65b17bcfd41949abf7d538a77678dc26` | `credited: true, reason: "credited", start: 1563` | `{credited: 1, inputs-unrecorded: 43, verdict:gap-blocking: 1, verdict:wrong-expectation: 5, wrong-expectations:1: 1}` | 1/51 |
| `09ee1d0` | `09ee1d099190918ec388019bb79afbb6b93f1ff2` | `credited: false, reason: "input-drift:tools/mutate-and-run.sh", start: 1563` | `{input-drift:tools/mutate-and-run.sh: 1, inputs-unrecorded: 53}` | 0/54 |
| `eb7838b` | `eb7838b16490ca7ba17ea3242ade76a61f744af2` | `credited: false, reason: "no-ledger-entry", start: 1563` | `{inputs-unrecorded: 48, no-ledger-entry: 10}` | 0/58 |

Observed sequence: **credited, input-drift, no-ledger-entry**. The ticket's expected
third reason (`input-drift`) does not hold at the landing rev; the bucket is still
denied credit, for a different reason.

Reproducibility: the committed `redbefore/measure-e69b488.json` and
`measure-09ee1d0.json` are equal to my reruns in every JSON value except `rev_input`
(the committed files recorded the 40-hex revision; I passed abbreviations, which
`measure.py` resolves into `revision`).

Causal control: the same command at `2a22ade` (the build commit immediately below
`eb7838b`; same `SKILL.md` blob `8ca9eee19e595333f02b433cb9ed1504eb1ed8a3`) also
returns `no-ledger-entry`. `eb7838b` only changed tooling (hermetic git env for the
selftest), so the landing edit, not the tip commit, is the cause.

### Why `eb7838b` is `no-ledger-entry`

- `measure.py` hashes the section body (heading line through the line before the next
  heading, trailing blanks stripped; `measure.py:229-240`) and matches the ledger by
  that sha (`measure.py:554-559`); a miss is `no-ledger-entry` (`measure.py:559`).
- The round-14 section body sha is
  `e8720037c0b1bd43db7b21fe2dd9a2669fe64db11f72649c754c85d1832e7cbd` at `e69b488`,
  `09ee1d0` and `98bea7d`, but
  `c121412bd8cf27b0f93b731ae0b43033870c429a5ebe14de77b234a2ada236a7` at
  `2a22ade`/`eb7838b`.
- Commit `2a22ade` rewrote recipe steps 2–3 to the historical form
  (`SKILL.md:1581-1586` at `eb7838b`: "**Historical (round 14, runner
  `75ed934d…`):** … Replay with cwd = an extracted `git archive 28aeef4` tree … Live-tree
  form: the round-17 re-pin section.") versus the live-tree commands at `e69b488`
  (`SKILL.md:1581-1586`). That is the C2a edit; it intentionally changes the bucket text.
- The round-16 ledger entry for this bucket
  (`98bea7da...:.ufo/evidence/round-16/coldread/ledger.json`, one entry with
  `start=1563`, `end=1596`, `sha256=e872...`, `skill_sha256=97cf...`) cannot match the
  landing section: no entry has `sha256=c121...`, and the ledger's
  `_meta.skill_files` page pins are `97cf.../3d8a.../e289.../906f...`, not the landing
  page `b1bd20...`.
- `--inputs-overlay` merges only into ledger entries keyed by
  `(entry.skill_sha256, entry.start)` (`measure.py:529-543`) and may set only
  `start/skill_sha256/heading/inputs/read_rev/traces` (`measure.py:127`) — it cannot
  set the section `sha256` or re-key the section. Merge count is 1 at every rev, so the
  overlay did apply; the section-sha gate stops the entry before any input check.
- The inputs do drift at landing but are never consulted: at `eb7838b` 3 of the
  overlay's 19 pins differ (`tools/evidence-disposition.py`,
  `tools/mutate-and-run.sh`, `tools/pin-disposition.py`); at `09ee1d0` only
  `tools/mutate-and-run.sh`; at `e69b488` none.
- Coverage gap: the selftest's red-before drift case (`measure.py:1215-1223`) changes
  only an input file at the second rev and leaves the section text byte-identical; it
  pins `input-drift:<file>` and never exercises the landing's case (section body also
  changed), which yields `no-ledger-entry`.

Effect: the anti-laundering outcome at `eb7838b` still holds — with the round-16
ledger plus the e69b488 overlay the round-14 bucket (and the other 57 sections) earns
no credit — but the landing red is "the old ledger entry cannot match a rewritten
bucket", not "the inputs drifted".

## 2. Overlay inputs vs independent strace of recipe steps 2–3 at e69b488

Overlay: `.ufo/evidence/round-17/redbefore/legacy-r14-inputs.json`, sha256
`3280b8cc16efc088aede64344dfab44bfcfc2a1e2115ced0fe609e55cbdac045`, one item
(`start=1563`, `read_rev=e69b488...`, 19 `inputs`). All 19 pins match
`git cat-file blob e69b488:<path>` (0 mismatches).

Tree: `git -C "$C" archive e69b488 | tar -x -C "$T"` (exit 0), then from `$T` (no
`.git`, so no hidden history reads):

```
strace -f -qq -e trace=%file -o step2.strace python3 tools/evidence-disposition.py \
  --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json
# EXIT=1 (expected 1); counts: effective 12, expected_checks 12, failed 1, findings 1,
# passed 11, superseded 0; exit 1
strace -f -qq -e trace=%file -o step3.strace python3 tools/evidence-disposition.py \
  --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
# EXIT=0 (expected 0); counts: effective 11, expected_checks 12, failed 0, findings 0,
# passed 11, superseded 1; exit 0
```

Parsing successful `O_RDONLY` opens of regular files under `$T`: step 2 opens 18,
step 3 opens 18, union 19; **overlay − observed = ∅ and observed − overlay = ∅**.
The only per-step asymmetry is each step's own manifest (step 2 opens
`dispositions-before.json`, not `dispositions.json`; step 3 the reverse). The non-file
paths touched are only parent directories (`.ufo`, `.ufo/evidence`,
`.ufo/evidence/round-12`, `.ufo/evidence/round-12/BashWitness`,
`.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z`,
`.ufo/evidence/round-13`, `tools`) from component `lstat` checks. No live-lane path is
read: the straces contain 0 mentions of `/home/vgpnk/Projects/shokunin`; the only
`/home/vgpnk` accesses are the Python launcher's `PATH` probes (all `ENOENT`) and its
own `site-packages` directory.

The 19 inputs (membership shown where the steps differ):

```
.ufo/evidence/round-12/BashWitness/declaration.json
.ufo/evidence/round-12/BashWitness/declared.tsv
.ufo/evidence/round-12/BashWitness/summary.json
.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json
.ufo/evidence/round-13/expected.json
.ufo/evidence/round-13/pin-manifest.json
.ufo/evidence/round-13/producer-before.py
.ufo/evidence/round-13/producer-oracle-repair.json
.ufo/evidence/round-13/producer-oracle.py
.ufo/evidence/round-13/verification.json
.ufo/evidence/round-13/witness-metadata-old-null.json
.ufo/evidence/round-13/witness-metadata.json
.ufo/evidence/round-14/dispositions-before.json      (step 2 only)
.ufo/evidence/round-14/dispositions.json             (step 3 only)
tools/bash-witness-study.py
tools/evidence-disposition.py
tools/mutate-and-run.sh
tools/pin-disposition.py
tools/witness-metadata.py
```

Committed strace cross-check: `redbefore/logs/e69b488-before.strace` and
`e69b488-after.strace` independently show the same 18/19 split (each lacks the other
step's manifest), consistent with the rerun.

## 3. Context (not this seat's claim)

At `eb7838b` the no-override invocation (`measure.py --rev eb7838b`) reports
`overrides_used: false`, `trace_gate: "strict"`, `coldread.reasons {"no-ledger": 58}`
because `.ufo/evidence/round-17/coldread/ledger.json` is not committed at the rev
(only `assemble.py`, `bucket-commands.json`, `trace-inputs.py` are). The C1 green
number therefore depends on this wave's assembled ledger, not on the landing tree as
committed.

## Findings

1. **Wrong expectation (claim text); artifact behavior is correct.** The red-before's
   third reason at `eb7838b` is `no-ledger-entry`, not `input-drift`; the round's
   red-before statement should read `credited → input-drift → no-ledger-entry` (or
   cite the landing run explicitly). Root cause is the C2a rewrite of the same bucket
   in `2a22ade`; `measure.py`'s section-sha key is working as designed — an edited
   section is a new bucket and cannot be laundered by the old entry.
2. **Overlay provenance verified.** The 19 inputs are exactly the union of regular
   files read by recipe steps 2–3 at `e69b488` (18+18 → 19, no extras, no omissions),
   all hashes match the e69b488 blobs, and the two exits are the recipe's stated 1 and 0.
3. **Optional hardening (not a defect):** add a selftest case for "overlay at a rev
   where the section body changed → `no-ledger-entry`, not `input-drift`"; the current
   red-before selftest (`measure.py:1215-1223`) only covers an input change with a
   byte-identical section, which is exactly why the landing expectation could be
   authored wrongly.

Verdict: **Partial** — the red-before denies credit at all three revs and the 19-input
overlay is exactly the strace-observed step 2–3 read set, but the expected landing
reason falls: `eb7838b` returns `no-ledger-entry` (rewritten bucket), not `input-drift`.
