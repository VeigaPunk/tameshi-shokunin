# WitnessThreats — C2 witness-attribution critic (round 12, w1)

Seat: critic, leaf. This is an advisory, lane-internal report. It is not a non-author admission and it does not count as a pass.
Outcome hygiene: this file does not list any per-defect B1–B10 verdict, recorded or measured, and does not predict any witness. I never ran a spec defect. Every mutant below is a synthetic `X*` defect that is not in the spec.
Tool installs: none.

## Axes
- **depth** (C2): is the killed-on-witness / accidental / survived / inconclusive split honest?
- **calibration**: is the denominator the one actually executed, and is the control host-independent?

## Evidence (O = observed by this seat; scratch `/tmp/tameshi-r12-witnessthreats/`)

- **O1 Pin.** `git -C ../kagi-shokunin show fecee874…:corpus/surface-census.sh` gives sha256 `275d8294…53009f`. This equals `PIN_BASH` (`tools/mutate-and-run.sh:544`). `git log fecee874..HEAD -- corpus/surface-census.sh` is empty, so the target has not drifted. `.ufo/evidence/round-12/BashWitness/pristine.sh` has the same sha.
- **O2 Control, 3 runs.** `bash pristine.sh --selftest </dev/null` exited 0 three times. stdout was byte-identical each time (sha `09c21ee2…a2fca`) and stderr was empty. Final line: `SELFTEST: PASS (16 cases)`. The output has 14 `^ok-case` and 2 `^skip-case` lines: 15 verbs-sandboxed and 16 verbs-break-injection, both "handler not on PATH" (pinned `:817-823`). This holds on this host only.
- **O3 Host and env dependence.** With the same pinned bytes, `THE_JANITOR_BIN=/bin/true`, or a stub `the-janitor` on PATH, gives exit 1, `bad-case 15 verbs-sandboxed`, and `SELFTEST: FAIL (1/16 cases)`. The outputs were `hostdep.out` sha `fafb3f3a…` and `hostdep2.out` sha `423d83c3…`. The runner passes its environment to the suite (`run_one`, `tools/mutate-and-run.sh:394-395`). The suite also reads these env vars: `SQLITE3_BIN` (`:83`), `CENSUS_BREAK` (`:448`), and `DEEP` (`:584` `${DEEP:-}`, which execs `op` only when a handler resolves).
- **O4 Synthetic sweep.** Command: `tools/mutate-and-run.sh --target pristine.sh --defects synth.spec --suite 'bash "$MUTANT" --selftest' --workdir sweep`. synth.spec sha `815e1060…`; tool sha `75ed934d…`. The control was GREEN. The runner reported all four as KILLED.
  | id | edit | exit | ok/bad/skip | `^SELFTEST:` line |
  |---|---|---:|---|---|
  | X1 | `printf 'SELFTEST verbs\n'` → `exit 1` | 1 | 14/0/0 | **none** |
  | X2 | `--selftest)` → `die` | 2 | 0/0/0 | **none** |
  | X3 | CLEAN `exit 0` (:863) → `exit 3` | 1 | 12/2/2 | FAIL (2/16) |
  | X4 | `stat_mode` → constant `600` | 1 | 12/2/2 | FAIL (2/16) |
  X3 and X4 both fail exactly `{01 clean, 04 runtime-absent}`, even though they mutate unrelated code.
- **O5 Token masking.** In mutant X4, case `02 mode-drift` printed `ok-case … exit=1 SURFACE DIVERGED`. The fixture's perturbed path (`op.env` chmod 644) was **not** reported. The token came from four other rows (`the-janitor`, `xdg-data`, `opencode`, `log` at "mode 600"). `run_case` checks a substring anywhere in the output (pinned `:753`).
- **O6 Label grammar.** Pristine stdout has 0 lines starting with `PROBE`. PROBE lines appear only inside the `    | ` dumps under a bad-case, and only when a handler resolves (O3). The `run_case` failure line is `bad-case NN name want exit=W token=T got exit=G` (`:755`). The custom cases 10, 14, 15 and 16 print only `bad-case NN name exit=RC` (`:786,811,829,842`). That line carries no `want`, and case 16 has no dump.
- **O7 Contamination vectors before declaration.** Recorded per-defect outcomes for this leg are in:
  - `tools/mutate-and-run.sh:85` (aggregate), `:526-527` (per-defect), and `:555` (`TABLE_BASH`). The spec heredoc sits between them at `:630-670`.
  - The aggregate total, at `corpus/README.md:79`.
  - The note `corpus/knowledge/mutation-case-kagi-census.md`, plus other listed knowledge, plan and report files.
  - `.ufo/evidence/kaika-round-1/coldread/appendixB/*`.
  - Two round-12 seat files: `EvidenceScribe/inventory.md:85` and `MinimalityReview/probes.md:25,38`. On my request both owners redacted these, and a re-grep for per-defect patterns over `.ufo/evidence/round-12` and `w1` now finds 0 hits.

  The kagi repo has no tameshi outcome mention (grep: 0). BashWitness's directory held only `pristine.sh`, with mtime 23:14:43 local, when I checked. I cannot tell what it read before then.

## Counterexamples and threats

| # | Threat | Counterexample | Axis | Kind |
|---|---|---|---|---|
| T1 | **Denominator loss read as accidental.** Exit code alone cannot tell `SELFTEST: FAIL` from an abort. | X1 is exit 1 with no summary and 0 bad-case lines, so "red and no declared label failed" comes out as `accidental`. It must be `inconclusive`. X2 is exit 2 with 0 cases run and the runner still says KILLED. | depth, calibration | fixable |
| T2 | **Skip-inflated denominator.** A "full 16-case count" includes 2 cases that assert nothing on this host, and the count stays 16 when the set of cases changes (O3). | O2/O3. ClaimSkeleton M4 reached the same result independently. | calibration | fixable |
| T3 | **Generic witness collapses accidental kills into witness kills.** `clean` and `runtime-absent` turn red for any defect that disturbs the clean path. | X3 and X4 have identical failing sets. Declaring `clean` as a witness makes both "killed-on-witness". | depth | fixable (sensitivity), plus a tradeoff |
| T4 | **Duplicate-case inflation.** Identical failing-label sets from distinct edits are indistinguishable at case granularity. One defect red on k cases is still **one** kill. | X3 ≡ X4. Counting failing labels instead of defects inflates k. | depth | fixable |
| T5 | **Case-level witness ≠ assertion-level witness.** A case passes on a token from another row, and the exit-versus-token sub-assertion is only partly recoverable. | O5. O6: only `run_case` lines carry `want`; for those, if G==W the token was missing, otherwise it is ambiguous. | depth | tradeoff: the claim must state case-level scope |
| T6 | **Host-state accidental kills / red control.** | O3: an inherited env or PATH turns the pristine control red. With a real handler, verbs cases run real host state. | calibration | fixable (scrub and record env) |
| T7 | **Contamination.** Extracting the spec from the runner exposes the recorded per-defect table, and the aggregate total is public, so at best the declarations are blind per defect, never on the aggregate. | O7 | depth (provenance) | disclosure required |
| T8 | **Self-attested pre-registration time.** The round-1 hash and time were recorded by the same author (`kaika-round-1/witness/README.md:18-21`), and file mtimes can be edited. | — | depth (provenance) | fixable |
| T9 | **Reanalysis counted as a seventh gate.** | ScorecardReview probe (`w1/ScorecardReview.md:43-46`): one extra row makes command D print 7. | depth | the judge must reject |
| T10 | **Tail parsing.** The runner prints only 8 tail lines (`TAIL_N=8`, `:167`). X3's `.out` is 57 lines. | — | depth | fixable: parse `sweep/evidence/<id>.out` |

## Smallest safe corrections (for BashWitness / L1; none applied by me)

1. **Classifier preconditions.** `killed-on-witness` or `accidental` requires all of the following. Otherwise the defect is `inconclusive`, never `accidental` (T1, T2):
   - the last non-empty line matches `^SELFTEST: (PASS|FAIL) \((?:\d+/)?16 cases\)$`;
   - the ordered list of `^(ok|bad|skip)-case NN name` labels equals the control's 16-label list.

   Any case that is `skip` in the control is unexaminable. A witness declared only on such a case → `unresolved`.
2. **State two denominators**: executed = 14 and printed = 16. Declare witnesses only from cases 01–14 on this host.
3. **Labels**: parse only line-anchored `bad-case` names from the full `.out`. Ignore `    | ` lines (T5, T10). Record per defect whether G==W, so token failures and exit failures stay apart.
4. **Sensitivity row (T3)**: report each defect's |W|. Recount with `clean` and `runtime-absent` removed from W, unless the declared basis cites the mutated line in their path. Publish both counts. A defect that changes class between them goes in `unresolved`. WitnessSourceReview applied the same check to the js leg (`w1/WitnessSourceReview.md:34`).
5. **Count defects, not labels (T4).** Also report the groups of identical failing-label sets as "indistinguishable at case level".
6. **Environment (T6)**: run control and mutants with `env -u THE_JANITOR_BIN -u SQLITE3_BIN -u CENSUS_BREAK -u DEEP`. Record `command -v the-janitor sqlite3` and the bash and sqlite3 versions with the evidence.
7. **Provenance (T7, T8)**:
   - Read the spec only via `sed -n 631,669p tools/mutate-and-run.sh` (`:630` is the heredoc opener).
   - Disclose every outcome-bearing file already read, and call the result "per-defect blind at best; aggregate known".
   - Before the sweep, send the sha256 of the declared TSV to Main so the time is recorded externally. Make rerun mode refuse a TSV whose hash differs.
8. **Ledger identity (T9)**: label the result "leg 2 (bash-surface-census) reanalysis". The harness table must match `TABLE_BASH` exactly (0 flips), and that comparison happens only **after** the declaration hash. Any flip is an erratum, not a re-split.

## Reproduction (scratch, not in repo; QUALITY 9 — L1 copies these if a claim cites them)
```
W=/tmp/tameshi-r12-witnessthreats
git -C ../kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh >$W/pristine.sh
bash $W/pristine.sh --selftest </dev/null            # O2
THE_JANITOR_BIN=/bin/true bash $W/pristine.sh --selftest </dev/null   # O3
bash tools/mutate-and-run.sh --target $W/pristine.sh --defects $W/synth.spec --suite 'bash "$MUTANT" --selftest' --workdir $W/sweep   # O4
```
Hashes: `sweep/evidence/X1..X4.out` = `a1e3af4a…`, `cf16027a…`, `e4fb4b00…`, `4c3dc276…`; `results.tsv` = `0aa36593…`. Probe time 2026-10-20T02:16Z.

## Owned paths
- Written: `.ufo/waves/round-12/w1/WitnessThreats.md` (this file) only.
- Scratch: `/tmp/tameshi-r12-witnessthreats/`.
- Peer messages: one outcome-free warning to BashWitness, and redaction requests to EvidenceScribe and MinimalityReview, both applied by their owners.
