# ReviewFreeze — round-33 freeze conformance audit (f6d8a89)

## Verdict

**CONFORMANT.** The freeze commit f6d8a891f1d966c5c3cdda385090da3a6e804675 matches the contract's claimed frozen_artifacts: every pinned sha256 verifies over the committed blob, the runner is byte-untouched, SCORECARD.md/LOG.md/corpus are byte-identical to base 66e1fb4, the before receipts carry real captured exits (proven `;`-form) and predate the freeze, and the dev selftest receipt shows 21/21 with exit 0. No conformance defect found in the freeze. Named observations and residual risks follow the evidence; none blocks data.

Reviewed as the assigned diff only; I did not write any audited content. No tool installs or upgrades were made (host pacman transactions are paused; nothing beyond present git/sha256sum was needed).

## 1. Mandated diff (66e1fb4 → f6d8a89)

Command (run in /home/vgpnk/Projects/shokunin/tameshi-shokunin, read-only flags; scratch capture /fast/scratch/hyaku/tameshi-r33-seats/ReviewFreeze/difftree.z, exit `0` in difftree.exit):

```
git --no-optional-locks diff-tree --name-status -z --no-renames 66e1fb444615b3afe380e7df0244ef7fae1dd985 f6d8a891f1d966c5c3cdda385090da3a6e804675
```

Observed: `M .ufo` `M considerthese` `M tools` — three modified top-level trees. Methodology note (not a defect): without `-r` the command cannot enumerate files; it names top-level entries only. Its output still evidences the byte-identity claim: SCORECARD.md and LOG.md (root files) and `corpus` (root tree) are absent from it, so none changed. Authoritative enumeration required the recursive rerun below.

## 2. Recursive enumeration and attribution

`git --no-optional-locks diff-tree -r --name-status -z --no-renames 66e1fb4 f6d8a89` (difftree-r.z, exit 0) lists exactly 13 additions:

```
A .ufo/evidence/round-33/before/c1-at-base.exit      A .ufo/evidence/round-33/before/c1-at-base.stdout
A .ufo/evidence/round-33/before/c2-at-base.exit      A .ufo/evidence/round-33/before/c2-at-base.stdout
A .ufo/evidence/round-33/c1/c1-measure.py            A .ufo/evidence/round-33/c2/c2-measure.py
A .ufo/evidence/round-33/c2/doctest-snapshot.html    A .ufo/evidence/round-33/c2/fetch-receipt.txt
A .ufo/evidence/round-33/contract.json               A .ufo/evidence/round-33/dev/selftest-final.exit
A .ufo/evidence/round-33/dev/selftest-final.stdout   A considerthese/2026-10-23.md
A tools/tally-audit-v2.py
```

Freeze-commit-only diff (`f4e88ec → f6d8a89`, difftree-freezeonly.txt, exit 0) contains exactly the 12 round-33 paths + the tool; `considerthese/2026-10-23.md` is **not** in it. Attribution: the mandated range spans intermediate commit f4e88ec ("considerthese: 2026-10-23 daily reflection", committed 09:38:07 — the freeze's parent), so that journal file appears in the range but is not a freeze artifact. Not a defect.

Classification of the 12 freeze paths: contract frozen_artifacts (`tools/tally-audit-v2.py`, `.ufo/evidence/round-33/c1/c1-measure.py`, `.ufo/evidence/round-33/c2/c2-measure.py`, `.ufo/evidence/round-33/c2/doctest-snapshot.html`) + freeze infrastructure named by the audit target (contract.json, 4 before-receipt files, dev/selftest-final.stdout+exit) + `.ufo/evidence/round-33/c2/fetch-receipt.txt`. Observation: fetch-receipt.txt is not itemized in contract.json's `frozen_artifacts`; its content is the C2 sourcing receipt (two ordinary curl fetches of the versioned URL, both HTTP 200, 216574 bytes, sha256 217edd57…4899, byte-identical by cmp) and it substantiates the pinned snapshot — expected, named here per the "name it" rule, judged non-defective.

## 3. Pin verification (content sha256 of blobs at f6d8a89)

Captures sha-tool-freeze.out/.exit, sha-snapshot-freeze.out/.exit, sha-runner-freeze.out/.exit (all exit 0):

| Artifact | Claimed pin | Observed at freeze | Result |
|---|---|---|---|
| tools/tally-audit-v2.py | 9dbbce62…33a4 | 9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4 | MATCH |
| c2/doctest-snapshot.html | 217edd57…4899 | 217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899 | MATCH |
| tools/mutate-and-run.sh | a7d3f2dd…2eb9 | a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 | MATCH |

Runner untouched, directly proven: git blob id of tools/mutate-and-run.sh is `2d81b929c765d52d6ff38837bb76901cd3358c8e` at base and identical at freeze (byte-identity.out), and the path is absent from both diffs. Counter digests at freeze recorded for the record (contract pins none): c1-measure.py `7ff776df0cfc9f32ea3003db6e0d0018258188b1a803a4ad57a7c896b99f8cc6`, c2-measure.py `f1c6c3a73a5da7fcda8da48b72679595241a85196a8afa28a3afe2a1cf4f452d`. The working-tree tool bytes at audit time still equal the frozen pin (on-disk sha256 = 9dbbce62…33a4), so wave-2 measurement will see the pinned bytes.

## 4. SCORECARD.md / LOG.md / corpus byte-identity

Git content ids equal at base and freeze (byte-identity.out, exit 0): SCORECARD.md blob `f7d6c594…b389`, LOG.md blob `9d2e1a99…62ad`, corpus tree `f17abe06…10a7`. Combined with absence from both diff-trees (§1–2): byte-identical to 66e1fb4. Confirmed.

## 5. Before receipts — content, exit discipline, predate-the-freeze

Content (committed bytes; on-disk files sha256-SAME as freeze blobs, see §5 third bullet):

- `.ufo/evidence/round-33/before/c1-at-base.stdout:1`: `C1_R33: tool_present=0 tool_sha_ok=0 runner_sha_ok=1 controls_ok=0(not-checked) v1_kill=0/0 v1_accept=0/0 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 heldout_after_freeze=0 seed=2ce55dbe3f51538e rev=66e1fb444615b3afe380e7df0244ef7fae1dd985 C1_R33_PASS=false` — matches contract C1.before (tool_present=0, controls_ok=0, PASS=false) and the goal's marker `runner_sha_ok=1`.
- `.ufo/evidence/round-33/before/c2-at-base.stdout`: `C2_R33: row=none versioned_url=0 snapshot_sha_ok=0 gate_sha_ok=0 quote_ok=0 C2_R33_PASS=false` — matches contract C2.before (row=none, PASS=false). Observation: two Python FutureWarning lines (stderr, about `ROW_RE`'s `[[:space:]]` nested-set) are interleaved in the captured stdout, i.e. the capture combined streams; markers intact, cosmetic only.

Exit discipline: `.exit` files contain `1` (c1) and `1` (c2). Both runs necessarily fail (PASS=false → exit 1 per the contract's before-claims), so a `cmd && echo $? > f` chain would have skipped the capture entirely; a recorded `1` is reachable only via `cmd; echo $? > f`. Real exits, `;`-form — proven observably, not from a process transcript.

Predate the freeze: mtimes — c1-at-base.stdout/exit 15:34:00.51/.52, c2-at-base.stdout/exit 15:34:00.57, selftest-final 15:32:34, fetch-receipt 15:33:15, snapshot 15:33:15, contract.json 15:33:47, tool 15:31:12 — all before the freeze commit time 2026-10-23T15:34:19-03:00 (history-mtime.out). All receipt files were added in the freeze commit itself and their on-disk bytes still equal the freeze blobs (sha256 SAME for c1/c2 stdout+exit, selftest stdout+exit, contract.json, tool), so nothing was mutated after the freeze.

## 6. Dev selftest receipt 21/21

`.ufo/evidence/round-33/dev/selftest-final.stdout` (grep -c '^CASE ' = 21): 16 must-kill mutants each `PASS (exit 1)` (dup-drop, nlegs, head-masked, status-4, guard-undercount, in-block-7bit, arm-00, head-overwrite, printf-swap, majority-gated, conditional-double, harness exit-only / swallowed / positions 0, 1, 8) and 5 must-accept variants each `PASS (exit 0)` (pristine, aux wrapper loop, aux pre-count loop, second extraction line, reversed operands); final line `TALLY_AUDIT_V2_SELFTEST: 21/21 pass`; `selftest-final.exit` contains `0`. The receipt is committed in the freeze and on-disk matches the freeze blob. Confirmed: 21/21 cases judged PASS with the correct per-class exits, overall receipt exit 0.

## 7. Post-freeze amendments (named; within the contract's amendment rule — not freeze defects)

Lane history advanced past the freeze while this audit ran (HEAD moved 27902a1 → e6a5f4b; freeze IS ancestor of HEAD, base IS ancestor of freeze — no rewrite, single-parent chain):

- 27902a1 15:42:40 "round-33 amendment 1: fix c1 counter --write-controls --receipt arg handling (procedural; predicate, kill rule and label unchanged; no seat has scored the claim's rule)"
- e6a5f4b 15:50:07 "round-33 amendment 2: harden c2 counter per ReviewCounterB (Gate-scoped digest search; row id > S099; tighter supersedes opener) before any data run; before-verdict unchanged"

Both land pre-data with disclosed scope, which the contract's kill_rule permits ("amendments land only as new frozen artifacts before any data run … disclosed in the round lesson"). Pin retention verified (pins.out, exit 0): the frozen c1 counter at f6d8a89 contains the tool pin and runner pin, the frozen c2 counter contains the snapshot pin, and the amended HEAD counters retain all three (each count 1). Residual risk for L1 (§ Residual): the committed before-receipts were produced by the frozen counter bytes (7ff776df… / f1c6c3a7…) that no longer exist at HEAD; amendment 2 asserts "before-verdict unchanged" without a regenerated before receipt. Smallest safe correction (L1's call, not mine to edit): regenerate the before receipts with the amended counters before wave-2 measurement, or record explicit acceptance of the assertion in the round lesson.

## 8. Untracked, outside the freeze (observations)

Scoped `git status --porcelain -- .ufo/evidence/round-33 tools/tally-audit-v2.py`: `?? dev/monitor-at-freeze.stdout`, `?? dev/monitor-at-freeze.exit`, `?? repair/` (mte-selftest.*, mte-install.*) — uncommitted wave-1 receipts awaiting L1 integration; not freeze content. `.ufo/evidence/round-33/c1/__pycache__/c1-measure.cpython-314.pyc` exists but is gitignored (absent from status) — import litter implying the counter module was imported once; no evidence of a forbidden default-mode counter run and no contract clause violated by an import.

## Residual risk and verification gaps

1. Before-receipt/counter version skew after amendment 2 (see §7) — the one item L1 should close before measurement.
2. Counters were never executed by this seat (forbidden outside their item); receipt content was verified against the contract's before-claims textually and by hash, not re-derived.
3. "Predates the freeze" rests on same-host wall-clock mtimes, corroborated by membership in the freeze tree and byte-identity to freeze blobs.
4. Exit-discipline is proven observably (a recorded `1` is impossible under `&&`), not from a captured process transcript.
5. The mandated non-recursive diff-tree cannot enumerate files; recursive and freeze-only diffs were supplied as the authoritative enumeration.

Scratch receipts (all commands cited above captured as `cmd; echo $? > file` in /fast/scratch/hyaku/tameshi-r33-seats/ReviewFreeze/): difftree.z/.exit, difftree-r.z/.exit, difftree-freezeonly.txt/.exit, sha-{tool,snapshot,runner,c1counter,c2counter}-freeze.out/.exit, byte-identity.out/.exit, history-mtime.out/.exit, pins.out/.exit.
