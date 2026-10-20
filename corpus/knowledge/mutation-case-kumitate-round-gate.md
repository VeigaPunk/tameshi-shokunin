source: S053 kumitate `scripts/round-gate.mjs` @ 364f1d5954158ef8844bca4a5fef57b05d2f2ca5 (blob sha256 f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9), read-only; S052 Stryker supported mutators; S056 PIT mutators; S057 Papadakis et al. survey §5.3.1; projection `corpus/knowledge/arm-class-matrix.md` §13 (round 4)
verified-at: 2026-10-20, sweep 13:40:15Z, tameshi commit e69b488 (pre-registration) and the round-16 landing commit
recheck: `bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-round-gate: PASS`; `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs | sha256sum` → f890e277…d3e9

# Mutation case 7 — kumitate `scripts/round-gate.mjs` (round 16)

The seventh recorded case and the third kumitate gate. Kumitate's tree stayed
read-only: the target is a byte copy materialized from its git object store
(`git --no-optional-locks status --porcelain` → 0 entries before and after).
No owner opt-in exists or was needed: kumitate `scripts/*` are tameshi's
read-only primary surfaces (`PROVINCE.md:7-11`), like cases 1 and 6. This is
not a service run and does not drain the service queue
(`service-optin-protocol.md` §0).

## 0. Pin and suite

- Target: rev `364f1d5` (the file's last-touching commit; kumitate HEAD
  `1770305` and the round-4 read at `175de6ba` hold the same blob `1f7d623e…`),
  80,415 B, 1,511 lines, mode 100755. Same bytes as the arm-class matrix §13
  projection pin, so its predictions apply to the bytes measured here.
- Suite: `node round-gate.mjs --selftest`, 60 checks, hermetic: under strace,
  zero reads under `~/Projects`, no network (RGRecon). Two environment
  hazards (RGSentinel): an exported `GIT_DIR` makes fixture commits land in
  that repository, and a `TMPDIR` inside a work tree makes 3 checks fail. The
  sweep therefore runs the suite under `env -i` with a private `HOME` and
  `TMPDIR` per defect (`.ufo/evidence/round-16/round-gate/suite.txt`); the
  ledger leg carries the same string.
- Control determinism: 8 pristine runs exited 0 with empty stderr, but stdout
  differed every run (one `mkdtemp` suffix, 9 lines per run).
  `tools/repeat-control.py` → `controls_mismatch` exit 1 (RGControl). Verdicts
  are graded on exit status only, and the runner does exactly that.

## 1. Pre-registration

Ten defects and their predictions were committed in `e69b488` (committer date
2026-10-20T10:39:59-03:00, pushed to origin) before any mutant ran (sweep
13:40:15Z = 10:40:15-03:00). Spec `.ufo/evidence/round-16/round-gate/round-gate.defects.spec`
sha256 `e99b87eb…11c4` equals the sweep's `spec.copy`. Composition: 5
kill-aimed (A1, A3, B1, E3, C1060) and 5 hole-aimed (C1059, A2, B2, CKIND, E1),
drawn from matrix §13 and the wave-1 seat fragments
(`.ufo/waves/round-16/w1/RGSpec{A,B,C,E}.spec`). Operator families follow S052
(string literal, equality/boundary, array declaration, conditional) and S056's
boundary operator. Rejected candidates and reasons are in
`predictions.json` → `rejected_candidates`. One example: the `INTERNAL_ERROR`
token edit was dropped because no input reaches that catch-all (SurvivorPrep
P12), so a survivor there would be equivalent by unreachability and say
nothing about the suite.

## 2. Result — 5/10 killed (50 %), 10/10 predictions held

Tool `tools/mutate-and-run.sh` sha256 `75ed934d…adc5` (r10-2, unchanged at the
sweep). Control `GREEN (exit=0)`, 0 inconclusive, `MUTATE_RESTORE: OK`, 32 s.
Evidence: `.ufo/evidence/round-16/round-gate/sweep/` (`results.tsv`,
`evidence/*.out`, `sweep.log`).

| id | class | edit (round-gate.mjs line) | predicted | measured | exit | checks failed (excluding the nested [51]) |
|---|---|---|---|---|---|---|
| A1 | A verdict path | audit/close verdict `lane=`/`checks=` swapped (:677) | KILLED | KILLED | 1 | 10: [1] [2] [3] [12] [16] [21] [22] [27] [46] [47] |
| A3 | A verdict path | tracked verdict `errors=`/`warnings=` swapped (:575-576) | KILLED | KILLED | 1 | 2: [52] [53] — rt8's prefix regex stays green |
| B1 | B fail-closed | main-path `REPORTS_DIR_MISSING` → `MAIN_REPO_NOT_GIT` (:647) | KILLED | KILLED | 1 | 2: [32] fcA, [45] jFc |
| E3 | G boundary | `filed.length < 2` → `< 1` (:535) | KILLED | KILLED | 1 | 1: [54] rt3 |
| C1060 | C floor | `REPORT_MIN_BYTES` 1024 → 1060 (:167) | KILLED | KILLED | 1 | 1: [8] r8, its 1059 B report now `REPORT_THIN` |
| C1059 | C floor | `REPORT_MIN_BYTES` 1024 → 1059 (:167) | SURVIVED | SURVIVED | 0 | 0 |
| A2 | D reported-unread | FAIL-CLOSED tail gains `detail: ` (:617) | SURVIVED | SURVIVED | 0 | 0 |
| B2 | E unreached species | tracked `REPORTS_DIR_MISSING` → `MAIN_REPO_NOT_GIT` (:527) | SURVIVED | SURVIVED | 0 | 0 |
| CKIND | C meta-check | `TREE_DIRTY` dropped from `FINDING_KINDS` (:175) | SURVIVED | SURVIVED | 0 | 0 |
| E1 | E unreached arm | `UFO_SRC` set-value resolves the canonical candidate (:163) | SURVIVED | SURVIVED | 0 | 0 |

Every kill also fails check [51], the hermeticity check, which re-runs the whole
selftest nested and reports its tally (A1 50/60, A3 and B1 58/60, C1060 and E3
59/60). That makes [51] a duplicate witness, not an independent assert. No
check was skipped in any run: `env -i` leaves `KUMITATE_ROUND_GATE_NESTED`
unset, so the control is 60/60 with no skips.

## 3. What the case measures

- **The interval projection held at its edge.** Matrix §13.4 projected that any
  floor in [26, 1059] changes no fixture verdict. The edge pair is the test:
  1059 survived and 1060 was killed by exactly the 1059-byte r8 fixture. The
  floor is pinned by an interval, not a point.
- **Pin width is a gradient inside one verdict family** (A3). The tracked
  verdict is pinned full-line by rt1/rt2 and prefix-only by rt8, so a tail
  reorder kills two checks and passes the third.
- **Species asymmetry** (B1 vs B2). The same one-token edit is killed at the
  main-path call site and survives at the tracked-mode site, because no
  fixture runs `--tracked` with a missing reports dir (matrix §13.6 #2).
- **The meta-check is one-sided** (CKIND). It checks that every enum kind is
  observed, so shrinking the enum cannot fail it. `FINDING_KINDS` has no other
  reader (`grep -n FINDING_KINDS` → :171 and :1488 only), so the mutant's gate
  behaviour is identical to pristine. This survivor is equivalent for gate
  behaviour; it weakens only the suite's own net. It is recorded as that, not
  as a detection gap in the gate.

## 4. Survivors — non-equivalence off-suite

The probe harness is SurvivorPrep's `probes.mjs`, retained at
`.ufo/evidence/round-16/round-gate/survivor-probes/`. Each probe runs on the
pristine copy and on the mutant copy:

| survivor | probe | pristine | mutant |
|---|---|---|---|
| A2 | P1 (fail-closed tails) | exit 0 | exit 1 |
| A2 | P1b (remaining tails) | exit 0 | exit 1 |
| B2 | P6 (tracked `REPORTS_DIR_MISSING`) | exit 0 | exit 1 |
| E1 | P9 (`UFO_SRC` set-value) | exit 0 | exit 1 |
| C1059 | report sized in [1024, 1058] | wave-2 seat `C1059Probe` | — |
| CKIND | none; equivalent for gate behaviour (§3) | — | — |

S057 states the general limit: deciding whether a mutant is equivalent is
undecidable, so each survivor carries either an off-suite witness or an
explicit equivalence argument.

## 5. Ledger leg

`js-round-gate` is the seventh leg of `tools/mutate-and-run.sh --regression`.
It holds the pin, rev, the spec above verbatim, the table
`A1:K A3:K B1:K E3:K C1060:K C1059:S A2:S B2:S CKIND:S E1:S`, and the guarded
suite. Receipt at runner sha256 `89722ddb…5594`:
`REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`,
rc 0. `--selftest` → `MUTATE_SELFTEST: 81/81 pass` (80 before; the leg-cut check
gained the seventh tuple). Both receipts are in
`.ufo/evidence/round-16/round-gate/runner-{regression,selftest}.txt`.

## 6. Limits

- One revision, one host (node v24.21.0, Linux 7.2.11). The rate is a property
  of this suite at this pin, not of kumitate's gates in general.
- 50 % mixes kill-aimed and hole-aimed defects by design; prediction accuracy
  (10/10) and kill rate are separate readings. Do not compare this rate with
  cases 1–6 without that composition.
- Recommendations for the owner, reported and not absorbed: a `--tracked`
  missing-reports-dir fixture (B2), a full-line pin on rt8 (A3), a detail-tail
  assert on one fail-closed fixture (A2), a set-value `UFO_SRC` fixture (E1),
  a point pin of the floor constant (C1059), and an `observed ⊆ enum` check
  (CKIND).
