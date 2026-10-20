# CriticC1Depth — wave-2 attack on C1 (depth 7→8) at `01d586dd`

Seat: TameshiR18.CriticC1Depth. Method: `/tmp` clone at the read rev
(`/tmp/tameshi-r18w2-CriticC1Depth-VkFc8l/fleet/tameshi-shokunin`), command-D
counts at three revs, full `--regression` rerun, byte-identity checks of
spec/suite/table, scratch counterexample probes against the pinned blob.
Acceptance rubric: `w1/R01CaseAcceptance.md` conditions + `w1/K02CaseDepthValue.md`
S1–S9 / D1–D5.

## Acceptance conditions, tested at `01d586dd`

| Condition | Test (command, exit) | Result |
|---|---|---|
| Command D counts 8 | `git show 01d586dd:tools/mutate-and-run.sh \| python3 -c '<SCORECARD:73 regex>'` | `recorded_cases=8 depth_score=8`; same command → 7 at `183f87b` and `93d22aa`. **Pass — the move exists at the committed tip.** |
| Count is not a placeholder | Runner `:93` reads `js-sources-check … 5/10 (50 %)`; `TABLE_SOURCESCHECK` `:620` is the real 10-row measured table; leg tuple `:1879` `…:10:5`. | Pass. |
| Pre-registration before sweep | `git show 93d22aa:.ufo/evidence/round-18/sources-check/sources-check.defects.spec \| sha256sum` = `c8d24cb4…408c91`, matching the committed spec; sweep receipt `sweep/sweep.txt:2-3` records `SWEEP_CONTEXT_COMMIT: 93d22aa` and `MUTATE_DATE: 19:41:29Z`; committer date of `93d22aa` is `2026-10-20T16:40:21-03:00` (=19:40:21Z, 68 s before; author date 19:22:36Z). | Pass. |
| Deterministic control | `control/repeat-hashes.json`: 8 runs, `all_exits_zero`, `distinct_stdout_sha256: 1` (`e0880a5a…`), 0-byte stderr. `control/hazard-summary.md`: GIT_DIR canary unchanged, TMPDIR-in-worktree clean. `control/strace-summary.md`: zero `~/Projects` reads, no external network. | Pass. |
| Hermetic suite string identical to sweep's | Installed runner `:1351` string is byte-identical to committed `suite.txt` (`sha256 6e550d5a…2423`, recorded as `SWEEP_SUITE_SHA256` in `sweep.txt:4`) — the guarded `env -i … node "$MUTANT" --selftest` form K02's S6 demanded. | Pass. |
| Embedded spec == pre-registered spec | `awk`-extracted heredoc from installed runner `:1015-1075` → sha256 `c8d24cb4…408c91`, identical to the `93d22aa` blob. | Pass. |
| Regression PASS at read rev | `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR bash tools/mutate-and-run.sh --regression` in the clone → `REGRESSION: PASS (cases=8 passed=8; …)`, leg-8 `match=10/10 flips=0`, `killed=5`, exit 0, 128 s. Real re-execution against `kumitate-shokunin @ 0acb7752` blob `6a293a72…258f`. | Pass — durable, not receipt-trust. |
| Entry with mined sources | `corpus/knowledge/mutation-case-kumitate-sources-check.md` committed in `58e5d53`; `corpus/SOURCES.md:19` S008 now `mined` with used-by → this entry; `corpus/README.md:265` case-8 row exists. | Pass with admission tail open (below). |
| Survivors probed (off-suite) | `mutation-case-kumitate-sources-check.md:150-163` still marks all five survivors `PENDING` ("PENDING wave-2 off-suite probes"). R01 demonstrated non-equivalence in scratch for all five; wave-2 probe seats are in flight. | **Open at read rev** — demonstrable, not yet durable. |

## Counterexamples attempted — and what survived

**CE-1: K_ROWS makes the recorded table host-flaky (K02 S3).**
Entry `§6` claims K_ROWS's kill channel is only the awk-gated parity check.
Built `krows.mjs` (`counts.rows += 1` → `+= 2`, count==1 asserted) and ran the
selftest under a `PATH` with no `awk` (symlinked sh/env/node/coreutils only):
`SOURCES_SELFTEST: 41/45 pass` — still killed via `clean fixture returns CLEAN`,
`1-3-space…` (not shown in tail but present in the FAIL list), `--json prints
one parseable contract object`, `S1000 is accepted and counted`; the parity
check reports `SKIP`. Pristine under the same PATH: `45/45 PASS`. **CE refuted
by measurement**: the recorded `K_ROWS:KILLED` holds on awk-absent hosts; the
entry's `§6` sentence ("its kill channel is the awk census parity check") is
wrong — parity is one of five channels, the rest host-independent. Smallest
correction: amend `§6`, no ledger change.

**CE-2: killed-by-the-wrong-check (K02 S8) for the three unattributed kills.**
The retained `sweep.txt` shows FAIL names only for K_EXIT/K_ROWS (tail-truncated,
`MUTATE_EVIDENCE` points at `/tmp`). Re-ran the three ambiguous mutants from the
spec (`count==1` asserted per edit): `kkind` → `43/46`, fails `TIER_ENUM: fixture
reports kind with expected exit` (+2 related) — the predicted case; `kstrict` →
`45/46`, fails `--strict promotes warnings to drift` — the predicted case;
`kclosed` → `44/46`, fails `SOURCES_MISSING: fail-closed exit 2` (+coverage
meta-check) — the predicted case. **CE refuted**: attribution gap is a
retention gap, not a correctness gap.

**CE-3: the `=8` is a syntax artifact.** Command D needs only the `\d+/\d+`
header; verified the header, table, embedded spec sha, suite string and a real
regression pass all agree — no placeholder path survives. **Refuted.**

**CE-4: stale-record falsification of the entry itself.** The committed entry
contains three statements false at `01d586dd`: §0 (:43-45) "sweep and control
directories are untracked" — `git ls-files` shows them committed in `58e5d53`;
§5 (:174-183) "the leg is not installed at base" / "installed-runner receipt is
pending" — the leg is installed and my regression run is that receipt; recheck
line (:3) still says "leg not yet installed at base, see §5". These are stale
draft sentences, not measurement errors — the case's own claims are
conservative, never inflated — but a reader trusting the entry's status lines
gets the pre-landing picture. Fixable: amend the entry (the file's own
procedure precedent is append-only errata blocks; the README's round-18 block
already practices this).

## Depth composition — is 5/5 kill/hole shallow?

K02's own rubric, applied literally:

- **S1 (shallow reject): not triggered.** Requires ≥7/10 in admitted classes
  AND zero defects touching §1 items 1–6. `K_STRICT` measures the severity-tier
  promotion arm (item 3 — first tiered-severity arm in the ledger) and `K_ROWS`
  exercises the cross-implementation parity channel (item 1 — first
  independent-implementation oracle in the ledger). Two new-species
  measurements.
- **Depth-bearing bar (≥2 of D1–D5): met.** D3 (K_STRICT, severity tier —
  killed on the predicted fixture) and D5 (S_VERDICT, verdict-tail survivor on
  the prefix/substring pin style) are both in the spec as delivered; D1 is
  touched via K_ROWS (with a now-proven non-host-gated kill channel, so S3's
  requirement is satisfied in fact even though the spec carried no explicit
  second-witness annotation).
- **Honest weighting:** the kill side is diversified (kind-emission, exit-map,
  severity promotion, fail-closed kind, count integrity — five distinct assert
  classes), but the hole side is conservative: all five survivors are
  replications of already-admitted families (one-sided meta-check S_KIND ≈
  case-7 CKIND; reported-unasserted S_VERDICT/S_DUP_LINE/S_ENTRY_COUNT ≈
  D2/D10/A2; unexecuted arm S_FILE_READ ≈ B5). K02's finer shapes it measured
  (M2b allowlist-content, M3 monthDays, M7 `..`-guard) were *not* taken. The
  case earns its point — two new-species measurements plus finer survivor
  granularity — but it does not exhaust the artifact's depth budget; leg 8 is
  real depth, modestly banked.

## Residual gaps (severity order)

1. **Medium — survivor witnesses not yet durable.** All five survivors are
   `PENDING` at the read rev (:150-163). R01's off-suite probes demonstrated
   non-equivalence for all five; the wave-2 survivor seats exist precisely to
   land them. The count does not depend on this, but the named acceptance
   condition "survivors probed" is unmet at `01d586dd`.
2. **Medium — admission tail open.** No LOG.md round-18 entry (grep
   `round 18|round-18|sources` → zero matches in `LOG.md`, 1083 lines, still
   ends on round 17); no case-8 row in `corpus/knowledge/fleet-kill-rate-ledger.md`
   (tail is the ER-jj2 erratum); no case-8 amendment in
   `corpus/knowledge/arm-class-matrix.md`; used-by backrefs for
   S001/S052/S056/S057 in `corpus/SOURCES.md` still point only at the older
   entries (:12,:61,:65,:66). The entry itself declares these routed under
   QUALITY 7 (:215-219).
3. **Low — stale status sentences** in the entry (§0 untracked claim, §5
   not-installed claim, recheck line; CE-4) and the §6 K_ROWS claim (CE-1).
4. **Low — per-mutant receipts not retained** (sweep tails only; QUALITY 9).
   Mitigated this wave by CE-2's independent re-derivation; the durable fix is
   retaining `MUTATE_EVIDENCE` under `.ufo/evidence/`.

## Smallest safe correction

Append an errata block to `mutation-case-kumitate-sources-check.md` recording:
leg installed at `58e5d53` (entry §5/§0 superseded), K_ROWS's kill verified on
an awk-absent PATH (non-parity channels fail), per-check failing names for
K_KIND/K_STRICT/K_CLOSED as measured above; land the wave-2 survivor probes into
§4's table; and close the LOG/ledger/matrix/used-by obligations. None of it
touches the ledger, spec, table, or count.

**Verdict: holds** — depth 8 is earned: the 7→8 move is committed and
regression-verified at `01d586dd`, every mechanical acceptance condition
passes, and the composition clears K02's depth bar (K_STRICT + S_VERDICT, with
K_ROWS empirically host-portable). The survivors-probed condition and the
admission tail remain open bookkeeping, not depth defects.
