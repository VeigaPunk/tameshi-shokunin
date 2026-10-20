# AttrReview — wave-2 attack on the routed-defect-2 repair (round 16)

Seat: TameshiR16.AttrReview (leaf reviewer, no delegation).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at
`c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
Scratch: `/tmp/tameshi-r16w2-AttrReview-59j8ha` and
`/tmp/tameshi-r16w2-AttrReview-mut2-hzCwAA` (mutation probes).
Tool installs/updates: none. No pacman transaction. The only lane write is this file;
`.ufo/evidence/round-15` and `.ufo/evidence/round-16/attribution` stayed clean
(`git --no-optional-locks diff --stat c699c8c -- …` empty).

## Axes attacked

- **A1 evidence identity** — `.ufo/evidence/round-15/` is byte-identical to `28aeef4`.
- **A2 old-rule fidelity** — the copied verify.py rule reproduces every recorded `observed_id`.
- **A3 new-rule correctness** — only the two usage rows change; JSON rows and the text verdict row survive.
- **A4 selftest discrimination** — the fixtures must reject weaker rules, not merely pass.
- **A5 append-only contract** — receipt untouched; correction create-only, idempotent, refusing different bytes.
- **A6 consumer consistency** — the artifact's own description (`--help`), correction fields, and routing citations agree with the code.

## Evidence

### 1. Round-15 bytes are identical at `28aeef4` and `c699c8c`

Command (for each of the four files): compare `git rev-parse <rev>:<path>`,
`git hash-object <worktree path>`, and `sha256sum` of `git show 28aeef4:<path>` vs the worktree.

| file | blob @c699c8c = @28aeef4 = worktree | sha256 |
|---|---|---|
| `.ufo/evidence/round-15/verification-3.json` | `87987fb8bf2841aeedaf2fdfda492c019ad70793` | `3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce` |
| `.ufo/evidence/round-15/verify.py` | `b38cbf4c7f68ba4a6a725035ffca701da3211c61` | `7e4519d9a0ea68ebbd02890629f06a6fac8e6eab034d9fa3b19d386b088a2522` |
| `.ufo/evidence/round-15/verification.json` | `45eeef25ebc22e7a7ca20b1328fce56d44e97096` | `4d2fb03f81df6aa92574187614a2a9ece5b3e928a03170f1e34809109428352d` |
| `.ufo/evidence/round-15/verification-2.json` | `067db99e7730dcfb8a1861983e089c5d5e4dc44f` | `4073c8c6d1362001cef861c049f66eea139073c14460e38372af78d284ab6ade` |

`git diff --stat 28aeef4 c699c8c -- .ufo/evidence/round-15/` → empty.
All 14 command-row payloads in `verification-3.json` are identical between the two commits
(`row names equal: True`, `row payloads equal: True`).

### 2. `--selftest` from a /tmp mirror of committed bytes

Mirror built with `git show c699c8c:<path> > /tmp/.../lane/<path>`; committed
`reattribute.py` sha256 `b81086b0978976efd4f8199c59bb66df018ea35d24d642a6590bf25942b714e9`;
committed `verification-3.json` sha256 `3c419055…d8ce` as pinned in the correction.

`/usr/bin/python3 -I reattribute.py --selftest` → **exit 0**:

```
usage-proof-new: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
gate-usage: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
usage-proof-old: oracle=receipt_missing old='receipt_missing' PASS new='receipt_missing' PASS
forged-first-line: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)
```

### 3. Correction from the same mirror

`/usr/bin/python3 -I reattribute.py` (with `correction.json` removed first) → **exit 0**:

```
…/verification-3.json sha256=3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce
corrections: usage-proof-new context_consistent->usage_error, gate-usage context_consistent->usage_error
old rule reproduced every recorded observed_id (14 command rows)
wrote …/correction.json
```

`diff -u <(git show c699c8c:.ufo/evidence/round-16/attribution/correction.json) <regenerated>` → empty
(`IDENTICAL`); regenerated sha256 `1caf1237af5890beac86c8be04d9c25849c710128da9fd346738217f60bfcea1`
matches the worktree. `corrections` has exactly two entries and names exactly
`usage-proof-new` and `gate-usage`; `coverage_changes` is `[]`.

Independent per-row re-derivation (importing the committed module against the receipt):

```
selftest-historical-unsupported exit=64 recorded=None                         old=None                        new=None
selftest-new                 exit=0  recorded=None                         old=None                        new=None
usage-proof-old              exit=2  recorded=receipt_missing              old=receipt_missing             new=receipt_missing
usage-proof-new              exit=64 recorded=context_consistent           old=context_consistent          new=usage_error
gate-frozen-builtin          exit=0  recorded=context_consistent           old=context_consistent          new=context_consistent
gate-clean                   exit=0  recorded=context_consistent           old=context_consistent          new=context_consistent
gate-missing-env             exit=1  recorded=missing_injected_environment old=missing_injected_environment new=missing_injected_environment
gate-tampered-snapshot       exit=2  recorded=snapshot_tampered            old=snapshot_tampered           new=snapshot_tampered
gate-usage                   exit=64 recorded=context_consistent           old=context_consistent          new=usage_error
mapping-oracle-old           exit=1  recorded=expected_verdict_mismatch    old=expected_verdict_mismatch   new=expected_verdict_mismatch
mapping-oracle-new           exit=1  recorded=mapping_mismatch             old=mapping_mismatch            new=mapping_mismatch
measure-before               exit=0  recorded=None                         old=None                        new=None
measure-after                exit=0  recorded=None                         old=None                        new=None
sources-census               exit=0  recorded=None                         old=None                        new=None
```

`old == recorded` on all 14 rows, so `old_rule_fidelity_failures: []` is honest.
The real terminal verdict is the final stderr line for both misattributed rows:
`CONTEXT: USAGE_ERROR (id=usage_error exit=64)` (line index 28 of stderr; also the last line).
The old rule latches the help-text token `id=context_consistent` at byte offset 936.

### 4. Append-only behaviour

- Second correction run: **exit 0**, `…/correction.json already exists with identical bytes; left unchanged`.
- Appending one byte to the mirror's `correction.json` then rerunning: **exit 1**,
  `…/correction.json exists with different bytes; refusing to overwrite (append-only repair)`.
- The receipt sha256 is printed on every run and is unchanged.

### 5. Draft provenance

`correction-attrfix-draft.json` sha256 `344558958d8678215ed39f4fcafb556c06ea8574969f2c0b5501a5faff6aba41`
equals the correction sha AttrFix reported before AttrCritic (`w1/AttrFix.md:9`).
It has the old strict `rules.new` and 7 `coverage_changes`; the committed tool cannot produce it
(`--selftest` and correction both pass the JSON branch now). `corpus/lessons/round-16.md:54`
explicitly says it "is kept as `correction-attrfix-draft.json` and is superseded, not cited."
So the draft is disclosed provenance, not a live result.

## Findings

### Confirmed — no blocking defect

- A1: all four round-15 files are byte-identical at `28aeef4`, `c699c8c`, and the worktree.
- A2: the copied old rule reproduces all 14 recorded ids; `old_rule_fidelity_failures` is `[]`.
- A3: exactly two id corrections, both `context_consistent → usage_error`; every JSON row and
  `usage-proof-old` keep their ids; `coverage_changes` is empty.
- A5: create-only write is idempotent and refuses differing bytes; the receipt is never written.
- The `notes` citation is exact: `verify.py:552` is `usage-proof-new` and `:558` is `gate-usage`,
  both `{"exit": 64, "stderr_token": "id=usage_error"}`; `verify.py:222-223` applies the token
  to stderr but never compares `observed_id`, which is why the receipts stayed green.

### Minor gap 1 — tool's own description is the superseded rule

`reattribute.py:19-22` describes NEW as a strict line
`^[A-Z_]+: [A-Z_]+ \(id=([a-z_]+) exit=(\d+)\)$`, scanned "stderr first, else stdout",
with "no match -> null" — i.e. the pre-critic rule. `reattribute.py:29-32` says `--selftest`
replays **one** fixture. The implementation is different (`reattribute.py:106-133`): JSON branch
first, optional middle fields and `findings=`, exit field must equal the process exit, both
streams matching → null, and four fixtures are run. Because `argparse(description=__doc__)` uses
the docstring, `--help` prints the stale rule (verified). The accurate description exists only in
the code comment at `:99-105` and in `correction.json.rules.new`. A cold auditor reading `--help`
would expect the JSON rows to become null and be surprised by the committed correction.
Fix: update the docstring (or mark it as the historical first cut).

### Minor gap 2 — selftest passes four mutants of named rule features

All mutants were made in /tmp from the committed bytes; each ran `--selftest` and a fresh correction:

| mutant | selftest | correction |
|---|---|---|
| M1: first match instead of last (`found` only if `None`) | PASS 4/4 | IDENTICAL |
| M2: drop the JSON branch (text rule only) | PASS 4/4 | DIFFERS — 6 `coverage_changes`, all `→ None` |
| M3: drop the `exit=`-equals-`observed_exit` gate | PASS 4/4 | IDENTICAL |
| M4: drop the both-stream ambiguity null | PASS 4/4 | IDENTICAL |

Why M1 survives: the forged fixture prepends `CONTEXT: OK (id=context_consistent exit=0)` to the
usage stderr. The exit gate rejects it before order matters. A forged line with `exit=64` is not
tested; when I prepend one, the committed rule still returns `usage_error` but a first-match
mutant returns `context_consistent` (probe output below), so the fixture does **not** pin
last-vs-first. M3 and M4 survive because no fixture has a verdict with a non-matching exit or
verdicts on both streams.

```
usage-proof-new base=usage_error first-match-mutant=usage_error
  forged exit=64 first: base=usage_error first-match=context_consistent
gate-usage     base=usage_error first-match-mutant=usage_error
  forged exit=64 first: base=usage_error first-match=context_consistent
```

The selftest therefore pins "these four text fixtures yield `usage_error`/`receipt_missing` under
some structured-verdict rule", not the layered repaired rule. `--selftest` alone is not a guard
against dropping the JSON branch, the exit cross-check, ambiguity handling, or last-match. The
committed correction is still correct; this is a regression-detection gap. Suggested extra
fixtures: the exit=64 forged first line, one JSON row, one dual-stream row, one mismatched-exit row.

### Minor gap 3 — correction does not name the `detail` field (or `verification.json`)

Both misattributed rows carry the wrong id in **two** fields: `observed_id` and
`detail` (`"expected exit=64 id=None observed exit=64 id=context_consistent"` in
`verification-3.json`; `verification.json` has the identical value in the same two rows).
`correction.json` names `recorded_observed_id` and the two rows, but not `detail`, and its
`notes` mention only `observed_id`. `corpus/lessons/round-16.md:53` does disclose that the same
misattribution "sits in `verification.json` … and is named here, not corrected", so the round
record covers the second receipt; the `detail` field remains unnamed in both. This falls short of
AttrCritic F7's field-level recommendation, but does not make any statement in `correction.json`
false.

### Minor/latent — `verdict_line` uses a different predicate than the rule

`reattribute.py:197-202` picks `verdict_line` as the last line matching `VERDICT_LINE_RE`
without the `exit == observed_exit` filter that `_last_verdict` applies at `:111-117`.
On the two actual rows only one line matches, so the committed value is correct. A synthetic row
whose later matching line has `exit=0` yields `verdict_line = "CONTEXT: OK
(id=context_consistent exit=0)"` while the rule returns `usage_error` (probe reproduced).
Cheap fix: reuse `_last_verdict` for the field.

### Residual risks (not observed on the receipt)

- A forged matching-exit verdict line **after** the real terminal verdict wins:
  `forged-after-real exit=64 → context_consistent`. The gate's usage path prints the echoed
  message before the terminal verdict, so this is not reachable in the recorded tool; it is a
  property of any "last matching line" rule, not a defect of the correction.
- Cross-artifact citation: `.ufo/waves/round-16/w1/RoutedDisposition.md:19,37,70` cites
  `correction.json` sha256 `34455895…aba41` and 7 `coverage_changes` — the superseded draft, not
  the committed `1caf1237…cea1` / 0 changes. The lesson line 54 supersedes the draft, so this is a
  stale wave-1 disposition, outside the three named files; L1 should not cite RoutedDisposition's
  sha as the landed correction.

## Verification gaps

- I did not re-execute round-15's `candidate.py`; the fixtures are the retained stdout/stderr
  bytes in the receipt, which is exactly the "same fixture/argv" object under test. AttrFix and
  AttrCritic reported a byte-identical tool replay; I did not rerun it.
- I did not run the lane's `verify.py`, `measure.py`, or any gate; those would rewrite or depend
  on round-15 artifacts and are out of scope. The `--selftest` and correction were the checks
  named by the target.
- Mutation probes are /tmp-only; no lane byte was modified. Tool installs: none.

## Verdict

**Holds (with three minor gaps)** — all named claims reproduce exactly: the four round-15 files
are byte-identical to `28aeef4`, `--selftest` exits 0 with old rule failing 3/4, the regenerated
correction is byte-identical to the committed one, it names exactly `usage-proof-new` and
`gate-usage`, and the old rule reproduces all 14 recorded ids; the gaps are stale `--help`
documentation, a selftest that does not discriminate four named rule features, and the unnamed
`detail`/in-artifact `verification.json` disclosure.
