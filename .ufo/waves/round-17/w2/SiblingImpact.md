# SiblingImpact — do the landed tameshi tools move any sibling gate or pin?

Seat: TameshiR17.SiblingImpact-2 (R17 W2, FALSIFY). Read-only; no sibling writes, no lane writes
except this report. Lane rev under test: `eb7838b16490ca7ba17ea3242ade76a61f744af2`.
Fleet root: `/home/vgpnk/Projects/shokunin` (21 lane repos; tameshi excluded from the sibling scan).

## 1. What actually moved, and the two old digests

| tool | at `98bea7d` (pre-landing) | at `eb7838b` | diff |
|---|---|---|---|
| `tools/mutate-and-run.sh` | `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa`, 85,003 B | `fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a`, 92,210 B | +146/−19: `git_clean` GIT_* scrub, `fixture_commit` helper, repo-identity guard in `regression_case` (`git -C` toplevel must equal the leg repo), 5 new selftest arms |
| `tools/pin-disposition.py` | `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`, 53,116 B | `331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c`, 59,295 B | +158/−16: `detect_branch` branch ladder, `head` is now the branch tip (`refs/heads/<branch>`), `head_differs_from_branch`, detached-HEAD selftest case |

So `0673d2e5…` = the runner bytes at `98bea7d`; `29725397…` = the pin-disposition bytes that every rev
from round 13 through `98bea7d` held. Both moved in `2a22ade`, not in the tip-only `eb7838b` commit
(`eb7838b` touches only `tools/evidence-disposition.py` plus receipts).

Staged round-17 copies at `eb7838b` are byte-equal to the landed files for both target tools
(`.ufo/waves/round-17/staged/tools/mutate-and-run.sh` = `fb6d86d5…`; `…/pin-disposition.py` =
`331529ea…`). Evidence-disposition staged ≠ landed (`a0c3a308…` vs `f8f05c7a…`) — outside this
target, noted only so the equality above is not read as a general staged=landed rule.

## 2. Consumers found, and whether their verdict changes

Scan method: full-text across the 20 sibling lane repos for `tameshi-shokunin/tools/mutate-and-run`,
`tameshi-shokunin/tools/pin-disposition`, `pin-disposition`, `mutate-and-run`, and the exact prefixes
`0673d2e5` / `29725397`; name and size probes for vendored copies (old sizes 85,003 B / 53,116 B);
executable-file scan (`.sh .py .mjs .js`) for any sibling that actually invokes the tools.
Only executable consumer across all 20 repos: **mado-shokunin**. Everything else is prose/history.

### 2.1 mado-shokunin — live gate, digest is provenance only → verdict unchanged (already re-run)

- `mado-shokunin/tools/mado-verify.sh:1919` resolves the harness:
  `harness="${MADO_VERIFY_HARNESS:-$MADO_R7_FLEET/tameshi-shokunin/tools/mutate-and-run.sh}"`.
  Registered gate row: `mado-shokunin/SKILL.md:552` (`mado-regression`, verdict map "0 clean (PASS)").
- The gate invokes the harness only in **target mode**:
  `mado-verify.sh:1824` `bash "$REGRESSION_RUNNER" --target "$target" --defects "$spec" --suite …`.
  It never calls the runner's `--regression`/`--selftest` modes, so the two changed code paths — the
  repo-identity guard and the GIT_* scrub, both only inside `regression_case`/fixture helpers — are
  **unreachable** from mado's gate. Its target file is a `/tmp` derivative of `mado-verify.sh`, not a
  git rev:path read.
- The digest is printed and labelled ungated: `mado-verify.sh:1931`
  `REGRESSION_HARNESS: … sha256=%s (recorded revision … — provenance, not gated)`.
  `HARNESS_SHA_RECORDED='b56c6e57…'` (`:1706`) is round-7 provenance, not the moved digests.
- Direct post-landing behavioral receipt (mado worktree, untracked `??`, being rewritten live by
  mado's own round-18 w2 seat while this read ran):
  `mado-shokunin/.ufo/waves/round-18/evidence/w2-gate-regression.txt`. Two reads seconds apart:
  first `sha256=08920a1d9f50…72b2b5` with `REGRESSION_DATE 2026-10-20T16:00:17Z`; second
  `sha256=4336ee196529…9ab7d` with `REGRESSION_DATE 2026-10-20T16:05:01Z`. Both runs are **after**
  the lane landing commit time `2026-10-20T15:59:15Z`.
  - line 1 `RECEIPT … measured_commit=abfbf35b1ed4d4a1eb294d525ef286be30f3886f utc=2026-10-20T16:05:01Z`
  - line 4 `REGRESSION_HARNESS: … sha256=fb6d86d5…` ← exactly the landed bytes (invariant across both reads)
  - line 13 `MADO_REGRESSION: PASS (case=mado-verify-hardened; target=20714096…)`
  - line 15 `exit=0`; table 10/10 KILLED, flips 0, control GREEN, restore OK (lines 7–11).
  This is the strongest single fact: the sibling gate was executed on the moved runner and its verdict
  did not change. (Caveat: the receipt is not committed in mado and is a moving worktree file; the
  digest on line 4 and the PASS/exit are the stable facts across both reads.)
- mado's pre-landing re-cut at 15:46Z used the old bytes (`…/round-18/evidence/regression-recut.txt:19`,
  `0673d2e5…`); that is a superceded receipt, not a pin. Mado's own w1 reports
  (`RevengePinRecut.md:30,251`, `RevGateRcFixPlan.md:180`, `SimplifyGateStub.md:114`,
  `SiblingOverlap18.md:128,282`) also record `0673d2e5…` as "live harness". Those are prose
  observations labelled "provenance, not gated" (`SiblingOverlap18.md:128-130`), now stale; the
  landing changes their truth value but no gate consumes them, and mado's own w2 receipt already
  records the replacement digest. No verdict flip.

### 2.2 mado-shokunin — frozen historical gates → unchanged (independent local copies)

- `mado-shokunin/.ufo/waves/round-13/frozen/{gate.sh,harness.sh,expected.json}` and the round-14
  frozen copy pin a **local copy** of the runner, not the sibling path:
  `expected.json` input `harness.sh` = `75ed934dc86360f5…`; `sha256sum` of the frozen file confirms it;
  retained evidence `.ufo/waves/round-13/evidence/frozen-regression.txt:4-5`
  `FROZEN_INPUT: gate.sh … verified` / `harness.sh … verified`.
  The landing does not touch mado's frozen files, so these historical gate replays are byte-identical.
  If replayed **without** `MADO_VERIFY_HARNESS`, the frozen gate would print the new live digest as
  provenance and still run target mode; no pinned input covers the live path.
- mado `.ufo/waves/round-13/frozen/gate.sh:1645` and round-14 `:1854` share the live-path default, but
  their retained runs used the frozen copy (`REGRESSION_HARNESS: …/frozen/harness.sh sha256=75ed934d…`).
  Not affected.

### 2.3 tsukuroi-shokunin — historical prose pins only → unchanged

- `tsukuroi-shokunin/SKILL.md:565-570` records "Tool pin: r4-2, md5 `26a27d35…`, sha256
  `597e141989065e03…331b`" and cites the runner method; `corpus/knowledge/memory-arm-mutants-s8.md:23`
  pins `cf41efaa…`; `corpus/knowledge/closeout-r11.md:337` similar.
- No tsukuroi executable invokes the sibling path; the only code hit is a comment
  (`tools/tsukuroi-census.sh:2174`). Neither `0673d2e5` nor `29725397` appears in tsukuroi.
  These pins are historical revisions of the harness, not the moved bytes; no verdict changes.

### 2.4 kaidoku-shokunin — one audit expectation goes stale at landing → no gate

- `kaidoku-shokunin/.ufo/waves/round-18/w1/ConnFleetJjPractice.md:86-89` says the round-17 rewrite
  "`documents` the branch ladder … but still calls `HEAD^{commit}` at `:328`; the whole `round-17/`
  directory is untracked (`?? .ufo/waves/round-17/`)" and infers "tameshi wrote the contract text one
  round before the code."
- At `eb7838b`: staged `pin-disposition.py` is byte-equal to landed (`331529ea…`); the file now
  implements `detect_branch` at `:324` (ladder: `refs/remotes/origin/HEAD`, `master`, `main`, first
  local branch), calls it at `:401`, resolves `refs/heads/<branch>` at `:415`, and records
  `head_differs_from_branch` at `:426`. The raw `HEAD^{commit}` read still exists at `:392`, but it is
  the raw-HEAD input to the branch resolution, not the returned `commit`. The `.ufo/waves/round-17/`
  tree is tracked at `eb7838b` (76 files). So the transcript's "contract before code" inference and
  its `:328` anchor are stale post-landing; the literal "still calls `HEAD^{commit}`" survives at a
  shifted line. This is a sibling **record/expectation**, not a gate input (no executable in kaidoku
  references the tool; the file is a wave report), so no verdict flips.

### 2.5 No other consumers

- `kama-shokunin/.ufo/waves/round-17/build/advice/ConnectTameshi.md:106` explicitly says the runner
  was "outside the bounded read" — not a consumer.
- The lanes whose gates are targets of tameshi's ledger legs (e.g. kumitate, kagi) are not consumers
  of the tool bytes; their own gates were not touched by this landing.
- Fleet-level: `MANIFEST.json:8256` mentions `0673d2e5` only in round-16 recheck prose;
  `.ufo/reports/round-16/tameshi.md:17` same. `scripts/`, `.tower/`, `shokunin.conf` contain no
  reference to either path or digest. These are records, not gates.
- Vendored copies: no sibling file is 85,003 B or 53,116 B; no sibling file is named
  `mutate-and-run.sh` or `pin-disposition.py`. The only sibling copy of runner bytes is mado's frozen
  `harness.sh` (77,904 B, `75ed934d…`), which predates both moved digests and is mado-owned.

## 3. Digest scan results (the requested check)

- `0673d2e5…` in 20 sibling repos: **7 lines / 6 files, all in mado-shokunin's round-18
  evidence/reports** (`regression-recut.txt:6,19,29`; `RevengePinRecut.md:30,251`;
  `RevGateRcFixPlan.md:180`; `SimplifyGateStub.md:114`; `SiblingOverlap18.md:128,282`).
  **Zero** occurrences in any `expected.json`, frozen manifest, gate script, or executable.
- `29725397…` in 20 sibling repos: **zero occurrences** (`grep` exit 1).
- Therefore neither old digest is a sibling pin. The move cannot flip a check that compares it.

## 4. Second-order effects and residual risks

- Runner: the guard and scrub fire only in `--regression`/fixture paths; no sibling invokes those
  modes. mado's target-mode call is byte-path independent of git state. No sibling exports `GIT_*`
  into the harness (mado's `GIT_*` hits at `mado-verify.sh:662-694` are `STUB_GIT_*` knobs for its own
  hermetic selftest PATH, not the harness environment), so the scrub is neutral for the fleet.
- The new guard would refuse a consumer that pointed the runner at a directory without its own
  repository; no sibling does that, and mado's repo/worktree has its own `.git`.
- Pin-disposition: no sibling calls it at all; the branch-tip change affects only tameshi's own probe
  output shape (`head.branch`, `head.head_differs_from_branch` are additive).
- Limits: I did not re-execute mado's gate myself (assignment is read-only and the post-landing PASS
  receipt already exists at the exact landed digest). The receipt is untracked in mado's worktree
  (`?? .ufo/waves/round-18/evidence/w2-gate-regression.txt`); mado owes the commit, but the run fact
  stands. Digest equality is necessary, not sufficient, for behavioral equivalence — the post-landing
  PASS is the behavioral half.

## 5. Commands executed (all read-only; no writes outside this report and /tmp)

| # | command | exit | key line |
|---|---|---|---|
| 1 | `git -C tameshi-shokunin show eb7838b:tools/mutate-and-run.sh \| sha256sum` | 0 | `fb6d86d59b5c…3001a  -` |
| 2 | `git -C tameshi-shokunin show eb7838b:tools/pin-disposition.py \| sha256sum` | 0 | `331529eadaf…2a4c  -` |
| 3 | same two against `98bea7d` | 0 | `0673d2e5374b…18aa`, `297253971dab…4f11` |
| 4 | `git diff --stat 98bea7d eb7838b -- tools/mutate-and-run.sh tools/pin-disposition.py` | 0 | `146 insertions(+), 19 deletions(-)`; `158 insertions(+), 16 deletions(-)` |
| 5 | full sibling grep for `0673d2e5` | 0 | 7 lines, all `mado-shokunin/.ufo/waves/round-18/…` (paths above) |
| 6 | full sibling grep for `29725397` | 1 (no match) | no output |
| 7 | `find <20 siblings> -type f -size 85003c -o -size 53116c` | 0 | no output (no vendored old-byte copies) |
| 8 | `find <20 siblings> -name mutate-and-run.sh -o -name pin-disposition.py` | 0 | no output |
| 9 | `grep -n 'REGRESSION_RUNNER" --target' mado-shokunin/tools/mado-verify.sh` | 0 | `1824:  bash "$REGRESSION_RUNNER" --target …` |
| 10 | `grep -n` provenance line in same file | 0 | `1931: printf 'REGRESSION_HARNESS: … — provenance, not gated'` |
| 11 | `sha256sum mado …/w2-gate-regression.txt` (twice; file rewritten between reads) | 0 | `08920a1d9f50…72b2b5` then `4336ee196529…9ab7d`; both: line 4 harness `fb6d86d5…`, line 13 `PASS`, line 15 `exit=0` |
| 12 | `sha256sum mado .ufo/waves/round-13/frozen/harness.sh` | 0 | `75ed934dc863…19adc5` (frozen copy, unchanged) |
| 13 | `grep -n` kaidoku report lines 85-89; `git show eb7838b:tools/pin-disposition.py \| grep -n` | 0 | detect_branch `:324`, raw HEAD `:392`, branch tip `:415`; 76 round-17 files tracked |
| 14 | `git -C tameshi-shokunin show -s --format=%cI eb7838b` | 0 | `2026-10-20T12:59:15-03:00` (=15:59:15Z) vs mado runs `16:00:17Z` and `16:05:01Z` (both later) |

No tools installed or updated (no package action taken).

**Verdict:** Holds — no sibling lane gate consumes or pins either moved digest (`0673d2e5…`: zero
gate/expected-manifest hits; `29725397…`: zero sibling hits at all), the only executable consumer
(mado's regression gate) reads the runner in target mode and its post-landing receipt already shows
`fb6d86d5…` + `MADO_REGRESSION: PASS` + `exit=0`, and the sole sibling expectation that changes is
prose (mado's 0673d2e5 observations, kaidoku's staged-file claim), not a verdict.
