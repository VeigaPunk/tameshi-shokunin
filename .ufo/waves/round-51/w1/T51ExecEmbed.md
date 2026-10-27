# Seat T51ExecEmbed — C2 tenth leg `bash-drift-pins` embedded in the runner (+ the four panel tools)

Bound: scratch clone of the lane only; the lane checkout was read-only throughout (`git -C
/home/vgpnk/Projects/shokunin/tameshi-shokunin status` never showed a write from this seat).
Deliverable file: `.ufo/waves/round-51/w1/T51ExecEmbed/mutate-and-run.sh`, sha256
`977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`.
Patch base: `84aa673a1a476e48ccf239335696f0518d08bae7` (`embed.patch`, 126 insertions / 47
deletions, one file).

## 1. The tenth recorded leg (runner)

Ledger row (the shape the C2 counter's `LEDGER_RE`/`LEG_RE` match), deliverable
`mutate-and-run.sh:97`:

```
#   bash-drift-pins       kagi-shokunin/corpus/drift-pins.sh          2/10 (20 %)
```
Shown by `grep -n 'bash-drift-pins       kagi' mutate-and-run.sh`. Total recorded legs 10
(`grep -c '^#   \(js\|bash\)-' mutate-and-run.sh` → 10; the counter prints
`recorded_cases=10 wired_legs=10`).

| site | deliverable line | what |
|---|---|---|
| channel line | :17-18 | "r51 adds the tenth measured leg, kagi corpus/drift-pins.sh, as bash-drift-pins" |
| regression parenthetical | :84 | `r26 nine; r51 ten` |
| source list + provenance | :103-104, :111-114, :120-121 | leg-10 spec path; "spec is the round-51 pre-registration committed in fe335384 before any mutant ran; its table is the measured 2026-10-26 sweep (23:53:02Z, .ufo/evidence/round-51/c2/sweep/sweep.txt; 7/10 verdict predictions held)"; "All ten defect specs" |
| usage leg list | :224-225 | `… js-cite-check,` / `bash-drift-pins) at its pinned` |
| pin | :632 | `PIN_DRIFTPINS=c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb` |
| rev | :633 | `REV_DRIFTPINS=e64e81b8eb96f3682b00c1e7a291e84420b280fa` |
| table | :643 | `TABLE_DRIFTPINS='K_MODE_CMP:KILLED,K_GONE_ARM:SURVIVED,K_AMBIG_GT:SURVIVED,K_COUNT_GE:KILLED,K_SHAPE_OPTIN:SURVIVED,S_SHA_CMP:SURVIVED,S_HARDLINK:SURVIVED,S_POLICY:SURVIVED,S_DUP_UNIQ:SURVIVED,S_USAGE_EXIT:SURVIVED'` |
| embedded spec | :1155-1212 | `cat >"$d/bash-drift-pins.spec" <<'EOT'` … `EOT` |
| specs-written guard | :1213-1219 | ten-file `[[ -s … ]]` |
| leg call | :1504-1507 | `regression_case_git bash-drift-pins 'kagi-shokunin/corpus/drift-pins.sh' "$PIN_DRIFTPINS" "$REV_DRIFTPINS"` … `"$root/bash-drift-pins"` |
| suite string | :1505 | exactly the sweep's: `h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C bash "$MUTANT" --selftest` (sandbox name deliberately **not** changed — the recorded table depends on it) |
| counts | :1510-1511 | `local nlegs=10 …` and the ten-operand `for st in …"$st_driftpins"; do` |
| REGRESSION_EXPECT | :1445-1455 | `… js-cite-check=%s/%s bash-drift-pins=%s/%s` + `TABLE_DRIFTPINS` args |

Pin/rev provenance, shown without touching the owner repo:

```
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8…:corpus/drift-pins.sh | sha256sum
  → c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb   (= PIN_DRIFTPINS)
git -C …/kagi-shokunin ls-tree e64e81b8… -- corpus/drift-pins.sh
  → 100755 blob 8a2903dc…                                           (exec bit mirrored by the runner)
```

`TABLE_DRIFTPINS` is the sweep's ten `DEFECT` lines in spec order
(`grep '^DEFECT ' .ufo/evidence/round-51/c2/sweep/sweep.txt`): 2 KILLED (`K_MODE_CMP`,
`K_COUNT_GE`), 8 SURVIVED. It equals `,`.join of those verdicts — confirmed by the counter,
`table_match=1` (§3).

Embedded spec is byte-identical to the frozen file. Re-extracted with the counter's own
`heredoc()` regex: embedded sha256 `a98271f639bc520f7052e63efaaa0b560cda959d3122d9c6921dcd1b9b61a602`
= `sha256sum .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`
(`match True` in the check cell; the counter independently reports `spec_prereg=1`).

All other counts that had to move 9 → 10:

- `:1445` `REGRESSION_EXPECT` line, `:1457` `st_*` declaration adds `st_driftpins`, `:1507`
  `st_driftpins=$?`, `:1510-1511` `nlegs=10` + tally operands.
- selftest: `:2024` "ten files written"; `:2032-2034` `lcalls/lfiles/lnlegs -eq 10` and
  `(want 10)`; `:2045` leg tuple `'bash-drift-pins:bash-drift-pins.spec:TABLE_DRIFTPINS:10:2'`;
  `:2046-2048` tuple count `-eq 10`, `(want 10)`.
- tally harness: `:2073-2076` block/name extraction on `local nlegs=10` with `(want 10)`;
  `:2086-2088` PASS line `cases=10 passed=10` + ten zero statuses; `:2091-2092` ten positions
  `for ti in 0 … 9`, `tst=(0×10)`; `:2102-2105` status vectors with ten operands; `:2116`
  `REGRESSION: SETUP (case-tally mismatch: cases=10 counted=9)`.

## 2. TMPDIR-honouring scratch defaults (defect fix, same file)

`mktemp -d /tmp/…` → `mktemp -d "${TMPDIR:-/tmp}/…"` at `:491` (run), `:1432` (regression),
`:1555` (selftest); doc text `:149-160`, `:217`. Receipt `tmpdir-probe.stdout`: with
`TMPDIR=<scratch>/tc` and no `--workdir`, the run printed
`MUTATE_EVIDENCE: <scratch>/tc/tameshi-r4-2-run.SwEH0l`, i.e. nothing under `/tmp`.

## 3. Measured runner behaviour (receipts copied into this directory)

- `selftest.stdout` — `bash tools/mutate-and-run.sh --selftest` (from the scratch clone,
  `TMPDIR=<scratch>/tmp`): `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc=0.
- `regression.stdout` — `bash tools/mutate-and-run.sh --regression --workdir <scratch>/reg`:
  ten `REGRESSION_CASE <leg>: PASS`, one of them
  `REGRESSION_TABLE bash-drift-pins: match=10/10 recorded-killed=2 measured-killed=2 survived=8 inconclusive=0 flips=0`,
  then `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)`, rc=0.
- `c2-probe.stdout` — frozen counter,
  `python3 .ufo/evidence/round-51/c2/measure.py --lane <clone> --rev HEAD --work <empty> --explain`:
  ```
  C2_R51: rev=a7622ff4d6c018d479367045cda91654b6468bf9 recorded_cases=10 wired_legs=10 depth_score=10
  new_legs=1 target_new=1 pin_ok=1 spec_prereg=1 sweep_ok=1 sweep_after_freeze=1 table_match=1
  regression=1 entry=0 sourced=0 readme=0 predictions_held=7/10 C2_R51_PASS=false
  ```
  Every structural field is 1; `entry/sourced/readme` are the other seats' deliverables. rc=1,
  i.e. not a verdict — the probe is reported as observed.
- `c2-probe-freeze-base.stdout` — same counter against the clone based exactly on the freeze
  commit `84aa673` (`rev=5a020bea…`): `recorded_cases=10 wired_legs=10 depth_score=10
  target_new=1 pin_ok=1 spec_prereg=1 sweep_ok=0 sweep_after_freeze=0 table_match=0 regression=1
  predictions_held=0/0`. Cause, shown by `git -C <lane> log --oneline -- …/c2/sweep/sweep.txt`:
  the sweep receipts landed in `f0129a5`, i.e. **after** the freeze commit, so `git show
  84aa673:…/sweep/sweep.txt` is empty and the counter cannot see the sweep or the table at that
  rev. The lane-tip base (`4e095c9`) carries them; the runner bytes are identical in both bases
  (sweep's `MUTATE_TOOL … sha256=a7d3f2dd…`), and the edit is the same patch, so the lane-tip run
  is the wiring parse.

## 4. The four dependent panel tools (scope extension from L1)

Delivered as full copies under `tools/` beside patches against `4e095c9caf8097c724ec347812ba2252ca2a74e4`
(the lane tip; these files are byte-identical at `84aa673`). Each was run with its default
`--runner` = the edited runner beside it.

| tool | edits | audit / check | selftest |
|---|---|---|---|
| `tools/tally-audit.py` (sha256 `4fe7c1c0…`) | `REF_BLOCK` :49-50 (ten operands, `nlegs=10`, comment re-pinned to sha `977de470…0bda`, lines 1510-1548); `REF_NAMES` :89-90; last-operand fault :267; seeds :407-408 (10→9 nlegs, `"$st_driftpins"`); harness-skip seeds :414-416 (ten positions) | `CHECK static PASS legs=10 operands=10 nlegs=10` / `runtime PASS vectors=358 mismatched=0` / `harness PASS reference cases=9; faults rejected=29/29` → `TALLY_AUDIT: PASS` (`audit-v1.stdout`) | `TALLY_AUDIT_SELFTEST: 11/11 pass` (`selftest-v1.stdout`) |
| `tools/tally-audit-v2.py` (`b3141e9d…`) | `REF_BLOCK` :67-68; `REF_NAMES` :107-108; fault :451; seeds `start` :614, second-extraction :628, operand/nlegs :632-633, harness-skip :648-650; docstring pair-bound 0..9 → 0..n :17, :43, :363 | `head PASS legs=10` / `static PASS legs=10 operands=10 nlegs=10` / `runtime PASS vectors=18288 mismatched=0` / `harness PASS … faults rejected=36/36` → `TALLY_AUDIT: PASS` (`audit-v2.stdout`) | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` (`selftest-v2.stdout`) |
| `tools/tally-audit-v3.py` (`a43de798…`) | `REF_BLOCK` :102-103; `REF_NAMES` :142-143; fault :655; seeds `start` :818, second-extraction :839, operand/nlegs :843-844, harness-skip :879-881; docstring pair-bound :49, :75, :566 | `head PASS legs=10` / `static PASS` / `runtime PASS vectors=36576 mismatched=0` / `harness PASS … faults rejected=36/36` → `TALLY_AUDIT: PASS` (`audit-v3.stdout`) | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` (`selftest-v3.stdout`) |
| `tools/mte-interop.py` (`4dbfd5ce…`) | `LEG_TABLE` :78 adds `'bash-drift-pins': 'TABLE_DRIFTPINS'`; setup message :318 "the ten ledger legs" | `MTE_INTEROP: PASS legs_conforming=10/10`, with `MTE_LEG bash-drift-pins: CONFORMS (… official_killed=2 official_survived=8 recorded=2/10 per_mutant=ok failed=none runner_pct=20 official_rounded_half_up=20)` (`mte-check.stdout`; run `--check --workdir <the ten-leg regression workdir> --regression-stdout regression.stdout`) | `MTE_SELFTEST: 17/17 pass` (`mte-selftest.stdout`) |

No other behaviour was touched: the panel/reference strings are the only nine-leg pins, and each
tool's non-leg checks were left as written.

Tooling: nothing installed or upgraded (no brew/pacman/uv/npx call). `jsonschema 4.25.1` and
`node v24.21.0` were already present (checked with `python3 -c 'import jsonschema'` and
`node --version`); the vendored `tools/vendor/*.tgz` were used as shipped.

## 5. Risks and notes for integration

1. **Cold-read re-key** (contract `coldread_note`): the runner's sha changed
   (`a7d3f2dd…` → `977de470…`), so the 20 credited sections whose ledger entries pin the runner
   drop until re-keyed against the new bytes (round-49 method); the four tool shas changed too, so
   any section whose entry read one of those files needs the same treatment. I edited no SKILL.md
   section and no PROVINCE.md.
2. **No-harm tools-scope is already satisfied**: `.ufo/evidence/round-51/no-harm.sh:8,35` allows
   exactly `M:tools/mutate-and-run.sh` plus the four tools edited here (amendment 2).
3. **The three kill-aimed survivors are data, not bugs**: `K_GONE_ARM`, `K_AMBIG_GT`,
   `K_SHAPE_OPTIN` stay SURVIVED in `TABLE_DRIFTPINS` because the recorded sweep is what the leg
   replays. I did not neutralise the `sandbox-$DEFECT_ID` name (the item forbids it); the
   independent witness probes belong to the labrat seats.
4. **C2 remains false until other seats land**: `entry=0 sourced=0 readme=0`. The knowledge entry,
   its SOURCES row (S272/S273) and the README line are not in my scope.
5. `prediction` accounting is 7/10, matching the sweep's own claim; the counter prints it outside
   the predicate.
6. Scratch was deleted after the receipts were copied; nothing under `/tmp` is cited, and no
   scratch path appears in this report except as a placeholder inside the probe transcripts
   (`c2-probe*.stdout` records `--work` paths by design; they are not evidence of the lane).

## Summary

- Tenth leg embedded: ledger row at `mutate-and-run.sh:97`, pin/rev :632-633, `TABLE_DRIFTPINS`
  :643 (2 KILLED / 8 SURVIVED, sweep order), byte-identical spec heredoc :1155-1212, call
  :1504-1507 with the sweep's exact `sandbox-$DEFECT_ID` suite, every count 9→10 (:1510,
  :1445-1455, :2024-2048, :2073-2116).
- Runner verified: `--selftest` **107/107 PASS**, `--regression` **PASS (cases=10 passed=10)**,
  `bash-drift-pins` table match 10/10 flips 0.
- Frozen C2 counter on a lane-tip clone: recorded 10 / wired 10 / depth 10, new_legs 1, target_new,
  pin_ok, spec_prereg, sweep_ok, sweep_after_freeze, table_match, regression all 1, predictions
  7/10; entry/sourced/readme 0 (other seats).
- Freeze-base (`84aa673`) clone cannot see the sweep (it landed in `f0129a5`); recorded in
  `c2-probe-freeze-base.stdout`, same structural fields otherwise.
- TMPDIR honoured in run/regression/selftest scratch defaults (:491, :1432, :1555), receipt
  `tmpdir-probe.stdout`.
- Four panel tools wired to the ten-leg panel: tally-audit 11/11, v2 22/22, v3 35/35, mte-interop
  17/17 with `--check` `legs_conforming=10/10`; full copies and patches under `tools/`.
- Deliverables: `mutate-and-run.sh`, `embed.patch`, `tools/*.py` + `tools/*.patch`, 13 stdout
  receipts (+ 2 empty stderr files).
- No lane write, no mutation in any repo, scratch removed.
