# FAudit1436 — scoped review (2026-10-21)

Axes: revision/input binding; C1 correction attribution; receipt-stream integrity.

## Finding — Minor: C1 input-impact summary is stale

**Disagree** with Audit1436 §4.2's specific assertion that “The one C1 repair that touches an input of this audit is lessons §5.4” (Audit1436.md:65–71, 2026-10-21). The delivered C1 build changed another whole-file input, `SKILL.md`; the old `checks.json` was preserved. This is a current-tip reconciliation error, not evidence that the original audit's pinned historical result is invalid.

**Concrete falsifier.** The audit trace at `.ufo/evidence/round-18/coldread/traces/L1/audit-1436.json` pins `SKILL.md` SHA-256 `1334c512…` at `read_rev=a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`. At delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`, `SKILL.md` is `0e3d7453…`; the baseline→delivered diff replaces the round-18 measure command at line 1888 and adds round-19 measurement entries at lines 1935–36. The actual `checks.json` at that delivered revision remains SHA-256 `fed3c8e6…`, unchanged from the audit input. Thus the actual present tip drift is the `SKILL.md` input, not the predicted `checks.json` rewrite.

**Reproduced binding arithmetic (read-only).** All 17 trace input digests match Git blobs at the recorded `a9c94…` revision. The receipt has 16 `OPEN` rows; those equal all 16 argv-spec paths and each hash/byte count matches the opened file. The ledger `read_rev` equals the trace revision and its inputs equal the trace inputs minus `SKILL.md`. At delivered `55e…`, 16/17 whole-file input digests still match the worktree; only `SKILL.md` differs. The changed SKILL lines are outside the audited 1436–1447 excerpt.

**C1 attribution check.** `corpus/lessons/round-18.md:137–146` says the exit-64/empty-stdout `checks.json` row remains byte-identical and names a separate successful witness receipt. That receipt records argv `python3 tools/bash-witness-study.py selftest`, revision `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, exit 0, stdout/stderr digests, tool/runner pins, and supersession of the old row. `measure.py:183–199` checks those facts, including preservation of the failed historical row. The R19 ruler does not read Audit1436's trace/stdout, so this correction does not fix its separate stream-pin gap.

## Residual risk and verification gaps

- The historical conclusion remains supported: the source revision, input hashes, trace, ledger, and selected section are still reproducible at `a9c94…`; later `SKILL.md` drift does not rewrite that history. Re-verification against the new tip must use the recorded revision.
- Audit1436's output SHA-256 is stated in its own lines 14–15, but is absent from its trace/ledger; the wording “claimed nowhere” is therefore overbroad, while the narrower lack of an independent trace/ledger output pin remains. C1's digests bind other receipts, not this one.
- No ruler, public selftest, or historical audit command was run. L1's final same-ruler count remains the acceptance gate; this report grants no admission authority.
