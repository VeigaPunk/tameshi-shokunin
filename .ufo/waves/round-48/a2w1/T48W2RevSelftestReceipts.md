# T48W2RevSelftestReceipts — re-verification of the committed round-47 selftest receipts

seat: T48W2RevSelftestReceipts (reviewer, leaf) · round 48 / a2w1 / hyaku run 8 attempt 2
item: re-run each command listed in `.ufo/waves/round-48/w1/T48ExecSelftestReceipts.md` in a scratch clone at
BASE `473336d9d789f6081195e7376d17836a24666bc3`, compare stdout/exit byte-for-byte against the committed
receipts; a tally that differs from the round-47 report's claim, or a receipt that does not match a rerun,
is a finding; check the criterion-93 falsifier output is present.
scratch: `/fast/scratch/hyaku/tameshi-r48/T48W2RevSelftestReceipts/` (deleted before this report was returned)
method: `git clone -q --shared` of the lane → `git checkout -q --detach 473336d9…`, `rev-parse --show-toplevel`
verified equal to the clone root; every rerun ran with `TMPDIR` inside the scratch dir; no lane file was
written; no mutating git command touched the lane.

**Bottom line: every committed receipt reproduces.** Four of the five counter selftests are byte-identical
to their receipts; the two non-byte-stable outputs (C1_R47 and C1_R48 selftests, falsifiers paths) differ
only in the fields w1 already documented as run-generated (fixture commit hashes, absolute temp/seat paths).
All tallies agree with every written round-47 claim. `CRITERION-93-FALSIFIER-OK` is present in both the
committed receipt (line 14) and my rerun (line 14). Two low-severity findings, both about prose, not bytes.

## 1. Bytes under test — pinned and re-hashed at BASE

All six sha256 values re-computed in my BASE clone match w1 §1 exactly:

| file | sha256 (BASE) |
|---|---|
| `.ufo/evidence/round-47/calibration/measure.py` | `c54debb241c0…daa0f30` |
| `.ufo/evidence/round-47/hardening/pool.py` | `7ea9ab1e2bcf…fa40e1904` |
| `.ufo/evidence/round-47/coverage/measure.py` | `c8fb89e69196…f894260` |
| `.ufo/evidence/round-47/quality/addition-lint.py` | `c33914274013…99dd56a` |
| `.ufo/evidence/round-47/quality/lesson-quote-check.py` | `858b020f6c40…8ffc83db6` |
| `.ufo/evidence/round-47/quality/falsifiers.sh` | `199c7d0953e3…511f460` |

All 23 committed receipts in `.ufo/waves/round-48/w1/selftest/` (`git ls-files` = 23) hash exactly as w1 §2
records: c1-measure `67399ce2…`, c2-pool `e51c59a9…`, c3-coverage `75ff3e3b…`, addition-lint `10b4b881…`,
lesson-quote-check `3d38cf33…`, falsifiers `1be5af68…`, falsifiers-verbatim `472c128d…`; every `.exit` is
`9a271f2a…` (`0\n`); every `.stderr` is `e3b0c442…` (empty) except falsifiers.stderr `f553068c…` (580 B).

## 2. Rerun-vs-receipt results

| run (command per w1 §2) | exit | stdout vs receipt | stderr vs receipt |
|---|---|---|---|
| `python3 .ufo/evidence/round-47/hardening/pool.py --selftest` | 0 | **byte-identical** (`cmp` clean) | both empty |
| `python3 .ufo/evidence/round-47/coverage/measure.py --selftest` | 0 | **byte-identical** | both empty |
| `python3 .ufo/evidence/round-47/quality/addition-lint.py --selftest` | 0 | **byte-identical** | both empty |
| `python3 .ufo/evidence/round-47/quality/lesson-quote-check.py --selftest` | 0 | **byte-identical** | both empty |
| `python3 .ufo/evidence/round-47/calibration/measure.py --selftest` | 0 | identical after `s/rev=[0-9a-f]{40}/rev=<sha>/` (35 differing lines, **all** contain `rev=`; 0 non-`rev=` differences; PASS case-name sets identical) | both empty |
| `bash falsifiers.sh` baselane shape (L→BASE clone, T→scratch; prepared by the same two-line substitution w1 recorded in `falsifiers.invocation.diff`; my script differs from w1's `falsifiers.baselane.sh` only on those two seat-path lines) | 0 | identical after masking the two path-bearing lines (2 and 10) to `<LANE>`/`<TMP>` | **byte-identical**, 580 B |

Tallies observed in my reruns, identical to the receipts and to every written claim:
`C1_R47_SELFTEST: cases=35 failed=0` + `VERDICT: PASS`; `C2_R47_SELFTEST: cases=14 failed=0` + `VERDICT: PASS`;
`C3_R47_SELFTEST: cases=24 failed=0`; `ADDITION_LINT_SELFTEST: cases=7 failed=0`;
`LESSON_QUOTE_SELFTEST: cases=11 failed=0`. `PASS`/`FAIL` counts 35/0, 14/0, 24/0, 7/0, 11/0; no duplicated
case name in any of the five (rerun and receipt).

Tally-by-tally against the round-47 claims (re-checked at the pinned sources):
- `SCORECARD.md` at lane HEAD-at-w1 `f1cfaad360130933983cac19f7036a8151f9054b`, lines 2308–2310: 35/35, 14/14,
  11/11, 7/7 — **agree**. Current HEAD `17cc5ce` still carries the same four values (grep, 1 occurrence each).
- Fleet `.ufo/reports/round-47/tameshi.md:12` (freeze bullet): "C1 35/35, C2 pool 14/14, C3 24/24" — **agree**;
  C3's tally exists only there and in `w1/T47MutC3Counter.md:6` / `w1/T47ScribeEntryPredict.md:28`, as w1 said.
- **No tally disagreement exists.** The routed defect remains what w1 called it: a receipt defect, closed by
  the committed receipts, not a false-tally defect.

## 3. Criterion-93 falsifier output — present

Committed `.ufo/waves/round-48/w1/selftest/falsifiers.stdout` line 14: `CRITERION-93-FALSIFIER-OK` (91 at
line 3, 92 at line 6). My rerun prints the same line at line 14, with the same block-93 shape:
`c93 oracle_lint_exit=1 real_additions_lint_exit=0` (planted compiled-oracle refused with 4 findings, six
real seat additions clean) and the three acid controls `CTL_E … neutral_killed=14`, `CTL_G … killed=122 …
C2_R47_PASS=false`, `CTL_H … killed=0 …` — the exact shapes block 93 requires (`falsifiers.sh:33`).
Criterion 93 passes at BASE and its output is present in the committed receipt. Same limits as w1 §5 apply:
the block's own `grep -E '^CTL_(E|G|H)' | cut -c1-260` discards CTL_A–D/F, and the script's last statement is
`rm -rf "$T"` (`falsifiers.sh:34`), so exit 0 carries no verdict — only the `CRITERION-*-FALSIFIER-OK` lines do.

## 4. Findings

**F1 (low — w1 report prose misdescribes the stderr receipts; the receipts themselves are correct).**
w1 §2 states: "Every `.stderr` is empty … except the falsifiers runs, whose only stderr is git's
detached-HEAD advice from block 92's own `git checkout --detach` (`f553068c…`, 580 bytes)." Two errors:
(a) `falsifiers-verbatim.stderr` is **empty** (`e3b0c442…`, 0 B; `cmp` reports EOF at byte 0) — only the
baselane `falsifiers.stderr` carries the advice; (b) the advice is emitted by block 92's
`git clone -q --no-hardlinks "$L" "$D"` (`falsifiers.sh:16`) when `$L` is a **detached-HEAD** source, not by
the checkout — the checkout is `-q` and silent. Attribution test (commands): from a detached-at-BASE clone,
`git clone -q --no-hardlinks <clone> <dst>` → stderr 580 B beginning `Note: switching to
'473336d9d789f6081195e7376d17836a24666bc3'.`; `git -C <dst> checkout -q --detach 9acfbe21…` → stderr 0 B.
The committed `falsifiers.stderr` first line names `473336d9…` — the w1 lane clone's detached BASE — which is
also why my rerun reproduced it **byte-identically** (my clone is detached at the same BASE), and why the
verbatim run (L = live lane, on a branch) legitimately produced none. No receipt mismatch; the defect is in
the w1 report sentence only.

**F2 (info — the item's named path holds the round-48 receipts, not the round-47 ones).**
`.ufo/evidence/round-48/selftest/` contains exactly four files: `c1-r48-selftest.{stdout,exit}` and
`c2-r48-selftest.{stdout,exit}` — the frozen round-48 counters' selftests referenced by
`freeze-2.json` (`selftest/c1-r48-selftest.stdout`, `selftest/c2-r48-selftest.stdout`). The round-47 receipts
this item targets are committed at `.ufo/waves/round-48/w1/selftest/` (23 files, all git-tracked). The
milestone "committed r47 selftest receipts" is satisfied there; nothing is missing, but a reader following the
item's path finds the wrong receipts. I verified the round-48 pair too (§5).

**F3 (info — w1's D1–D5 all re-confirmed by rerun).** C2 pool case ids skip `P13` (observed ids
`P01…P12, P14, P15`, `cases=14` correct); C1 label groups `T24_*`/`T25_*` appear only as dependence variants;
addition-lint prints `L07` first; `addition-lint.py:25` imports `tempfile` unused; the C1 selftest stdout is
not byte-reproducible (fixture `rev=` hashes). Extension of D5 to the round-48 counter: the C1_R48 selftest
embeds fresh fixture hashes in **both** `base=` and `rev=` fields (142 differing lines between receipt and
probe, 0 after masking both), so the round-48 c1 receipt is one-execution evidence for two fields, not one.

**F4 (low, pre-existing — `run-controls.py` temp leak re-confirmed).** One falsifiers execution (my rerun)
left **8** `tameshi-r47-ctl-*` directories in `TMPDIR`, **1.2 GB** total (w1 measured 2.7 GB across two
executions); `.ufo/evidence/round-47/control/run-controls.py:54` `mkdtemp` is never removed (no `rmtree` in
the file), and `falsifiers.sh:34` removes only `$T`. Honors `TMPDIR` (nothing leaked to `/tmp` or `/var/tmp`
from my runs; my leaked copies were inside my scratch and deleted with it). Real but pre-existing; not
introduced by round 48.

## 5. The round-48 receipts at the item's named path (probes, not verdicts)

Run as `--selftest` probes from a scratch clone at lane HEAD `17cc5ce` (counter bytes sha256-verified against
`freeze-2.json`: calibration `572a5670…26f3`, freshness `faefe9b4…df63f`, identical in HEAD and worktree):
- `c1-r48`: exit 0, `C1_R48_SELFTEST: cases=76 failed=0` + `VERDICT: PASS`, 76 `PASS` / 0 `FAIL`; identical to
  the committed receipt after masking `base=`/`rev=` fixture hashes (§4 F3).
- `c2-r48`: exit 0, `C2_R48_SELFTEST: cases=43 failed=0`, **byte-identical** to the committed receipt
  (1589 B; case lines are `SELFTEST <n>_<name>: PASS`, 43 of them — no `^PASS ` prefix, hence no VERDICT line).
Both receipts match `freeze-2.json`'s recorded selftest claims (76/0, 43/0). `freeze-2.json`'s
`contract_sha256` `4fff75db…` and `statements_sha256` `924102df…` both match the current files — no
post-freeze amendment of contract or statements.

## 6. Residual risks and verification gaps

- **`falsifiers-verbatim.*` was not re-run.** The committed script hardcodes
  `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin` (`falsifiers.sh:4`); a faithful rerun would read the live
  lane's working tree, which has legitimately moved past w1's `f1cfaad` (content revision `c7586b9` landed),
  so no byte-for-byte comparison to a receipt taken at `f1cfaad` is possible now — and repointing `L` would
  make the run non-verbatim. Verified instead: the verbatim receipt differs from the baselane receipt on
  exactly lines 2 and 10 (the `L=` and `T=` paths; diff shown), and its empty stderr is the expected signature
  of a branch-HEAD source clone (F1). Gap remains: no independent second execution of the verbatim variant.
- The falsifiers receipt is one-execution evidence: lines 2 and 10 embed absolute paths; CTL lines depend on
  `run-controls.py`'s deterministic scoring at BASE (reproduced identically here).
- `falsifiers.sh` exit code carries no verdict (`rm -rf "$T"` last, `falsifiers.sh:34`); a VACUOUS run would
  also exit 0. My rerun is non-vacuous by the three `OK` lines, not by the exit code.
- Block 93's own filter (`grep -E '^CTL_(E|G|H)' | cut -c1-260`) still hides CTL_A–D/F; unchanged from w1 §5.
- I did not re-derive w1's per-script temp-mechanism table line-by-line; I corroborated it behaviorally
  (all `tempfile` output landed under my `TMPDIR`; `/tmp` gained nothing from my runs).

## 7. Tooling record

No tool was installed, upgraded or fetched (nothing beyond `git`, `python3`, `bash`, `mktemp`, `cmp`, `du`,
`sed` was needed). No pacman transaction was attempted (host-wide pause respected). Scratch
`/fast/scratch/hyaku/tameshi-r48/T48W2RevSelftestReceipts/` — including the 1.2 GB of leaked `tameshi-r47-ctl-*`
clones measured in F4 — was deleted before this report was returned.
