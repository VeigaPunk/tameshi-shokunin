# W2LabratTraceSubset — round-36 trace-inputs ⊆ ledger-entry-inputs probe

Attacked: C1 support surface — the trace gate's subset rule for the four
round-36 cold-read ledger entries (starts 131, 375, 1380, 1436) and their
committed trace receipts. Read-only probe; no production edits; no subagents.

## Rule verified (from source)

`.ufo/evidence/round-21/coldread/measure.py` selects the unchanged round-18
credit algorithm (`IMPLEMENTATION = .ufo/evidence/round-18/measure.py`, lines
15-18). The trace gate (`trace_reason`, measure.py:373-417) requires each
committed trace blob to be schema `tameshi-trace-inputs-v1` and every
non-`IGNORED_INPUTS` trace input key to exist in the entry's `inputs` with
equal sha256 (`trace-input-unrecorded:<p>` / `trace-input-drift:<p>`).
`IGNORED_INPUTS` = {`SKILL.md`, round-17 ledger path, round-18 ledger path}
(measure.py:133-136). I checked both the gate view (ignored keys skipped) and
the literal view (all recorded keys compared) — identical verdicts here.

## Commands

- `git rev-parse HEAD` → fbb01cf46f8437fd1264c1a3acc053c882fa2164 (lane tip);
  refresh commit b455001e2589b3f4f471d94a3de7e5e549b9f54c.
- `git -C <lane> show <rev>:.ufo/evidence/round-21/coldread/ledger.json` →
  497 entries; ledger blob sha256
  29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf — identical
  at b455001e and HEAD (bytes stable since the refresh commit; the later
  receipts/verifier commits touched no ledger or trace bytes).
- `git show <rev>:<trace>` for the four `traces[]` paths each entry names.
- Python (stdlib json/hashlib/subprocess) computed each trace's input set and
  each entry's input set from those committed bytes and compared membership +
  sha256 equality. Output: /fast/scratch/hyaku/tameshi-r36-seats/W2LabratTraceSubset/subset-check.txt

## Per-entry verdicts (committed bytes @ HEAD = fbb01cf; identical @ b455001e)

| entry (start, heading) | trace | schema | gate-view inputs trace/entry | unrecorded | drift | verdict |
|---|---|---|---|---|---|---|
| 131 Mutation-sweep recipe | traces/L1/source-1.json (908dfa76…) | ok | 8/8 (+SKILL.md shared, equal) | none | none | PASS subset+equality |
| 375 Restore discipline | traces/L1/source-2.json (1e23a1ad…) | ok | 2/2 (+SKILL.md shared, equal) | none | none | PASS subset+equality |
| 1380 The map | traces/L1/source-3.json (c039d691…) | ok | 3/3 (+SKILL.md shared, equal) | none | none | PASS subset+equality |
| 1436 Where to enter | traces/L1/source-4.json (065c4a14…) | ok | 1/1 (+SKILL.md shared, equal) | none | none | PASS subset+equality |

Notes: pairing is authoritative via each entry's `traces[]` field — exactly
one trace per entry, and exactly four entries list round-36 traces. Each
trace's `rev` field records e423c41b (the read rev; matches `read_rev` in the
entries) — consistent with the gate, which resolves the trace *blob* at the
measured REV, not at `trace.rev`. `external`, `untracked`, `live_lane_reads`
are all `{}` in every trace (no external/live-lane reads to bind).

Caveat (observed, not a failure): the gate skips `IGNORED_INPUTS` keys, so a
trace's recorded `SKILL.md` digest is not gate-checked. Here all four traces
record SKILL.md = 23818731…575d5ac66557f617d35a, equal to each entry's
recorded SKILL.md anyway, so the literal superset also holds.

Verdict: all 4/4 round-36 entries PASS — every trace input is present in its
ledger entry's inputs with equal sha256; subset hypothesis holds, no
trace-input-unrecorded or trace-input-drift exposure.
