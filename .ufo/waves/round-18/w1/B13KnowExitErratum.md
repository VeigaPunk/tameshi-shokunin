# B13KnowExitErratum — R17-KNOW-EXIT (round 18, wave 1)

Base rev: 183f87b899e6cae46be98d251cbc87fb5118f6ca (branch master).

## Behaviour

Drafted an entry-local erratum appended after line 75 of
`corpus/knowledge/input-keyed-coldread-credit.md`. The staged full file is the
base bytes plus the appended block. No earlier line is edited. The erratum:

1. names the false §5 sentence (line 75, "2 rev/blob/ledger missing") and
   states the true split: a missing default ledger is a measured `no-ledger`
   state with exit 0; a missing explicit `--ledger-file` / `--ledger-rev` ledger
   exits 2;
2. narrows the `redbefore/measure-*.json` citation (§2, lines 45–48): three
   receipts are overlay runs, and `measure-98bea7d-strict.json` is not;
3. states the narrower R17-CMD-BIND claim: the rule binds credit to recorded
   inputs and does not bind trace argv to declared or required commands. It is
   not a command-coverage proof.

## Gates

No gate was run. This is a document draft. No lane selftest or checker was
executed.

## Touched surfaces

- WRITE (owned): `.ufo/waves/round-18/staged/corpus/knowledge/input-keyed-coldread-credit.md`
  (new staged copy; the live file is untouched).
- WRITE (report): `.ufo/waves/round-18/w1/B13KnowExitErratum.md` (this file).
- READ only: base blobs via `git show 183f87b…:<path>`; `.ufo/evidence/round-17/**`
  (receipts, measure.py, coldread/traces). Scratch copies in `/tmp/r18b13-*`.
- No git write, no GIT_* export, no jj, no install. No tool was installed or
  upgraded.

## Evidence

Prefix proof and diff shape (exit 0 for `cmp`):

```
$ cmp -n 5076 .ufo/waves/round-18/staged/.../input-keyed-coldread-credit.md /tmp/r18b13-base.md
PREFIX cmp: identical (5076 bytes)
$ diff /tmp/r18b13-base.md <staged>
75a76,147
base lines=75 staged lines=147
deleted-or-changed base lines: 0
```

Base blob sha256 (`git show 183f87b…:corpus/knowledge/input-keyed-coldread-credit.md`):
`1fad5a57c56ea059ebfecedf37edb8256739d94382f89cf302d49d319ab9e57c`.
Staged sha256: `0c45dccb4dfa78cdfd2dfddc59132d1e636ed0d548abcb9528d1b1aa21fd0636`.

Source lines verified at 183f87b (`git show 183f87b…:.ufo/evidence/round-17/measure.py`,
sha256 `d25d3d04…3ce7f3`, identical to the on-disk file):

| Claim | Lines | Observed text |
|---|---|---|
| no-ledger branch (default ledger absent) | 535–553 | `if ledger_raw is None:` … `'reason': 'no-ledger'` … `return out` at 553 |
| usage text, exit split | 93–95 | "a missing default ledger is a measured `no-ledger` state, not an error" · "2 rev/required-blob missing, explicit --ledger-file/--ledger-rev unreadable, or overlay unreadable/forbidden-field" · 64 |
| default-ledger path | 1545–1547 | `else:` / `ledger_raw = blob(repo, rev, DEFAULT_LEDGER_PATH)` / `ledger_source = 'rev'` |
| explicit `--ledger-file` / `--ledger-rev` exits | 1520–1543 | `return 2` at 1529, 1537, 1543 |
| overlay block exits | 1554–1592 | `try:` at 1554; `return 2` at 1562–1592 |
| return 0 | 1598 | `return 0` |
| trace binding | 368–380 | `trace_reason`; `traces-unrecorded` at 380 |
| receipt input binding | 403–412 | `rec_inputs = receipt.get('inputs')` at 403; `trace-input-drift:%s` at 412 |
| only receipt-argv reference | 773 | selftest fixture `'argv': ['cat', INPUT_FILE]` (the other `argv` hits are the CLI parameter at 1462, 1483) |
| bucket-commands.json reference | none | `grep -c bucket-commands` = 0 in measure.py at base |

Receipts in `.ufo/evidence/round-17/redbefore/` (Python JSON read):

| file | overrides_used | trace_gate | ledger_present | key result |
|---|---|---|---|---|
| measure-e69b488.json | true | legacy | — | bucket "Effective expectation reconciliation — round 14": `credited` |
| measure-09ee1d0.json | true | legacy | — | bucket: `input-drift:tools/mutate-and-run.sh` |
| measure-98bea7d.json | true | legacy | — | bucket: `input-drift:tools/mutate-and-run.sh` |
| measure-98bea7d-strict.json | **false** | strict | **false** | `coldread.reasons {"no-ledger": 54}`; no `error` key |

Default ledger presence (`git cat-file -e <rev>:.ufo/evidence/round-17/coldread/ledger.json`):
absent at 98bea7d, 09ee1d0 and e69b488; present at 183f87b.

Exit code of the strict receipt run is not recorded in the file. Exit 0 follows
from `measure.py:1598` [INFERENCE from source + absence of `error` key].

Trace receipt shape: `coldread/traces/CR01/1.json` carries `argv`
(`bash -c 'git -C … show eb7838b…:SKILL.md | sha256sum'`) and `inputs`; no code
path compares that argv with `coldread/bucket-commands.json`.

Lesson routing: `corpus/lessons/round-17-verifier-spotcheck.md` §7 item 1
(R17-KNOW-EXIT) and item 2 (R17-CMD-BIND), lines 419–425 at 183f87b.

## Out of scope

- R17-CMD-BIND itself (binding argv to declared commands with failure-backed
  coverage) is not implemented here. The erratum states only the narrower
  input-keyed claim, which the lesson's item 2 allows.
- G5 / G7 corrections in lesson §7 item 2 are not part of this entry.
- No edit to any round-17 evidence file, `measure.py`, the live
  `corpus/knowledge/input-keyed-coldread-credit.md`, the registry, or the ledger.
- No selftest was run (the erratum states no new measured number).

## Findings

- F1 (§5 line 75): the "ledger" half of "2 rev/blob/ledger missing" is false for
  the default ledger. Corrected in the erratum.
- F2 (§2 citation): `measure-*.json` includes a non-overlay strict receipt that
  shows no-ledger, not the input-drift bucket. Narrowed in the erratum.
- F3 (R17-CMD-BIND): the rule binds inputs, not argv. Stated in the erratum.
- Note: the erratum cites `measure.py:1554–1592` for overlay exits. Line 1554 is
  `try:` inside the `if args.inputs_overlay:` block, which begins at 1553.

## Verdict

built
