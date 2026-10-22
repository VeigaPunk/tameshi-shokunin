# MtWeakerGate — round 25, wave 1

**Verdict:** the ruler's seven multi-token stdout fixtures kill the six recorded
mutants (M1–M6, 6/6 KILLED) but they do **not** pin the stdout-token contract.
Four strictly-weaker implementations of the check at
`tools/command-binding.py:111` — case-folded, case-folded+whitespace-collapsed,
whitespace-stripped, punctuation-insensitive — **survive** the ruler *and* the
gate's own 44-case selftest. The C1 ruler is therefore calibrated only for the
mutation classes it was written against; a whole family of normalising
rewrites of the stdout check passes it silently. This is a coverage finding
about the ruler, not a defect in the production check, and not permission to
change the contract.

---

## 1. Setup and restoration evidence

| item | value |
|---|---|
| private clone | `/tmp/MtWeakerGate-r25` |
| clone revision | `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` (detached) |
| lane repo | read-only; never entered for writes |
| target under test | `tools/command-binding.py` (220 lines) |
| target sha256 (pristine, before) | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| target sha256 (after, clone) | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| target sha256 (lane, after) | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` (byte-identical to the clone) |
| fixture bytes | `.ufo/evidence/round-25/multitoken-cases.json` sha256 `ea64fca92306177d1a454a81c8d476cd56800022327c0c0e74e97412f8a7739f` (clone copy == lane copy) |
| suite bytes | `.ufo/evidence/round-25/c1-suite.py` sha256 `ae33a04bd0a3646ec6a879b786024861de2af1a83b1a914369f4b720e75b15f9` (clone copy == lane copy) |

**The target file was never written.** Every mutant is a separate byte copy
under `/tmp/MtWeakerGate-r25/probe/mutants/`; the clone's `tools/command-binding.py`
and the lane's copy still hash to the pinned pristine value above. The lane
working tree shows no change from this item (`git status --porcelain` in the
lane lists only other peers' files: `M tools/mte-interop.py` and the untracked
`.ufo/evidence/round-25/*`, `.ufo/waves/round-25/*`).

## 2. Detector

The bounded behavioural detector is the ruler's own multi-token suite, run
exactly as the assignment names it, inside the private clone:

```
cd /tmp/MtWeakerGate-r25
python3 .ufo/evidence/round-25/c1-suite.py multitoken <mutant copy>
```

Suite semantics (`c1-suite.py:44-70`): exit `0` = every case passed, exit `1` =
at least one explicit `FAIL` witness line, exit `3` = setup error. So:

* suite exit 0 → the mutant **SURVIVED** the ruler;
* suite exit 1 with a `FIXTURE <name> FAIL` line → the mutant was **KILLED**;
* suite exit 3 → INCONCLUSIVE (never observed).

**Baseline (pristine bytes):** `MULTITOKEN_SUITE: 7/7 pass`, exit 0 — the
detector is green before any mutation, so every kill below is attributable.

## 3. Mutants tried (twelve; the six named in the assignment are W1–W6)

Each mutant replaces exactly one line — `tools/command-binding.py:111`:

```python
        if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):
```

`@old` string asserted unique in the pristine bytes before each run.

| id | weakening | replacement condition | suite exit | ruler verdict | killed-by witness |
|---|---|---|---|---|---|
| W1 | token-set equality | `set(receipt['stdout'].split()) != set(tokens)` | 0 | **SURVIVED** | – |
| W2 | prefix match | token is a prefix of some stdout word | 0 | **SURVIVED** | – |
| W3 | case-folded match | `token.lower() not in receipt['stdout'].lower()` | 0 | **SURVIVED** | – |
| W4 | whitespace-split membership | `not set(tokens) <= set(receipt['stdout'].split())` | 0 | **SURVIVED** | – |
| W5 | first-and-last only | only `tokens[:1] + tokens[-1:]` are checked | 1 | KILLED | `FIXTURE mt-missing-middle FAIL (exit=0 findings=[])` |
| W6 | per-line match | token must appear inside a single stdout line | 0 | **SURVIVED** | – |
| W7 | case-folded + whitespace-collapsed | `' '.join(stdout.split()).lower()` contains `token.lower()` | 0 | **SURVIVED** | – |
| W8 | prefix-of-whole-stdout | `not receipt['stdout'].startswith(token)` | 1 | KILLED | `mt-clean-reordered FAIL`, `mt-clean-two-requirements FAIL` |
| W9 | stdout words == token set (both directions) | `not set(tokens) <= set(words) or not set(words) <= set(tokens)` | 0 | **SURVIVED** | – |
| W10 | whitespace-stripped match | `token.replace(' ','') not in stdout.replace(' ','')` | 0 | **SURVIVED** | – |
| W11 | punctuation-insensitive match | token/stdout stripped of ` ,.:;-_` before the search | 0 | **SURVIVED** | – |
| W12 | token lowercased before search | `token.lower() not in receipt['stdout']` | 1 | KILLED | `mt-clean-reordered FAIL`, `mt-clean-two-requirements FAIL` |

Ruler kill rate on these twelve probes: **3/12 killed, 9/12 survived**
(baseline 7/7 green, no INCONCLUSIVE run).

## 4. Which survivors are genuinely *weaker* (differential probe)

Surviving is not the same as weakening, so each survivor was diffed against the
pristine bytes over 17 hand-built `(tokens, stdout)` pairs (script
`probe/diff-probe.py`, results `probe/mutants/differential.json`). A mutant is
*strictly weaker* when it accepts a pair the pristine gate rejects; *strictly
stricter* when it rejects a pair the pristine gate accepts.

| id | strictly weaker on (pristine REJECT → mutant ACCEPT) | strictly stricter on (pristine ACCEPT → mutant REJECT) | class |
|---|---|---|---|
| W3 | `lowercase-token`, `lowercase-stdout` | – | **strictly weaker** |
| W7 | `lowercase-token`, `lowercase-stdout`, `newline-between-tokens` | – | **strictly weaker** |
| W10 | `token-no-space-vs-stdout-space` | – | **strictly weaker** |
| W11 | `trailing-comma-token` | – | **strictly weaker** |
| W5 | `middle-token-missing` | – | strictly weaker — but **killed** by the ruler |
| W1 | – | `token-inside-word`, `prefix-token`, `extra-word`, `two-tokens-one-word` | stricter divergence |
| W2 | – | `token-inside-word`, `two-tokens-one-word` | stricter divergence |
| W4 | – | `token-inside-word`, `prefix-token`, `two-tokens-one-word` | stricter divergence |
| W9 | – | `token-inside-word`, `prefix-token`, `extra-word`, `two-tokens-one-word` | stricter divergence |
| W6 | – | – (equivalent on all probes) | equivalent on probes |

Reading:

* **W3, W7, W10, W11 are strictly weaker and survive the ruler.** They accept a
  receipt whose stdout does not literally carry the declared token
  (`alpha` satisfied by `ALPHA`; `ALPHABETA` satisfied by `ALPHA BETA`;
  `ALPHA,` satisfied by `ALPHA`; `ALPHA BETA` satisfied by `ALPHA\nBETA`).
  The seven fixtures never exercise case, whitespace or punctuation, so the
  normalising rewrites are invisible to them.
* **W1, W2, W4, W9 survive but are stricter**, i.e. a rewrite of the check that
  the ruler would also call "clean" while it *rejects* stdout the real gate
  accepts (`xALPHA` for token `ALPHA`, a token that is itself a two-word
  phrase, extra stdout words under a set-equality rewrite). The fixtures pin
  neither substring semantics nor token multiplicity, so the ruler is blind in
  the false-mismatch direction as well.
* **W6** is equivalent to pristine on every probe pair and passes the ruler —
  the fixtures do not pin whether a declared token may span a newline.

## 5. Secondary detector: the gate's own selftest

`python3 .ufo/evidence/round-25/c1-suite.py selftest <mutant>` (44 cases):

```
mutant-W1  selftest_exit=1  43/44 pass
mutant-W2  selftest_exit=0  44/44 pass
mutant-W3  selftest_exit=0  44/44 pass
mutant-W4  selftest_exit=0  44/44 pass
mutant-W5  selftest_exit=0  44/44 pass
mutant-W6  selftest_exit=0  44/44 pass
mutant-W7  selftest_exit=0  44/44 pass
mutant-W8  selftest_exit=1  43/44 pass
mutant-W9  selftest_exit=1  43/44 pass
mutant-W10 selftest_exit=0  44/44 pass
mutant-W11 selftest_exit=0  44/44 pass
mutant-W12 selftest_exit=1  18/44 pass
pristine   selftest_exit=0  44/44 pass
```

The four strictly-weaker survivors (W3, W7, W10, W11) pass **both** detectors
in the lane. No detector in the lane can currently see them.

## 6. Cross-check: the recorded C1 mutant spec is honest

`tools/mutate-and-run.sh` re-run over the already-recorded spec
`.ufo/evidence/round-25/multitoken-mutants.spec` with the ruler as the suite,
in the clone:

```
bash tools/mutate-and-run.sh --target tools/command-binding.py \
  --defects .ufo/evidence/round-25/multitoken-mutants.spec \
  --suite 'python3 .ufo/evidence/round-25/c1-suite.py multitoken "$MUTANT"'
…
MUTATE_RESTORE: OK (target-sha256 before=9230c68… after=9230c68…)
MUTATE: DONE (defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)
```

M1–M6 are all genuinely killed; the C1 counter's credit for that spec is
earned, not inflated. The gap is in the *classes the ruler covers*, not in the
recorded run.

## 7. Smallest safe correction (recommendation only — this item wrote no repo file)

Four extra rows in the ruler's fixture file kill exactly the four strictly-weaker
survivors and leave pristine green. Verified with
`probe/candidate-fixture-check.py`, which writes the candidate fixture into a
**temp copy** and never touches the repo file:

```json
{"name": "mt-case-folded-token",            "requirements": [["a-gate", ["alpha"], "ALPHA"]],            "expected_exit": 1, "finding_ids": ["STDOUT_MISMATCH"]},
{"name": "mt-space-insensitive-token",       "requirements": [["a-gate", ["ALPHABETA"], "ALPHA BETA"]],   "expected_exit": 1, "finding_ids": ["STDOUT_MISMATCH"]},
{"name": "mt-punctuation-insensitive-token", "requirements": [["a-gate", ["ALPHA,"], "ALPHA"]],          "expected_exit": 1, "finding_ids": ["STDOUT_MISMATCH"]},
{"name": "mt-newline-insensitive-token",     "requirements": [["a-gate", ["ALPHA BETA"], "ALPHA\nBETA"]], "expected_exit": 1, "finding_ids": ["STDOUT_MISMATCH"]}
```

Measured: extended ruler vs pristine → `MULTITOKEN_SUITE: 11/11 pass` (exit 0,
still green); and with the extended ruler

```
mutant-W3  exit=1  killed_by=mt-case-folded-token
mutant-W7  exit=1  killed_by=mt-case-folded-token,mt-newline-insensitive-token
mutant-W10 exit=1  killed_by=mt-space-insensitive-token
mutant-W11 exit=1  killed_by=mt-punctuation-insensitive-token
mutant-W5  exit=1  killed_by=mt-missing-middle      (already killed by the current fixture)
```

All other rows stay green for the mutants that are only *stricter* (W1, W2, W4,
W6, W9) — those would need a different fixture family (a token that is a
substring of a longer word, a multi-word token, extra stdout words) to
discriminate. Ownership of the fixture file belongs to the C1 ruler item; this
item proposes the rows, it does not write them.

## 8. Axes walked (godspeed framing)

1. *Ruler kill power on stdout-token weakenings* — 3/12 killed; four strictly
   weaker classes survive (W3, W7, W10, W11).
2. *Calibration of the C1 counter* — the recorded M1–M6 credit holds (6/6, no
   INCONCLUSIVE, restore OK); the counter's blind spot is class coverage, not
   bookkeeping.
3. *No-harm* — the lane repo, the fixture file, the suite file and the
   production check were not modified; the target's before/after hashes are
   identical.

## 9. Tooling

No tool was installed, upgraded or removed by this item; the work used the
stock `python3`, `git`, `bash` and `sha256sum` already present on the host.
(Operator tooling directive: nothing to record beyond "no installs".)

Report: .ufo/waves/round-25/w1/MtWeakerGate.md
