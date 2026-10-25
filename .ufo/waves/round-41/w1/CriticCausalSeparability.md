# CriticCausalSeparability — are C1 (calibration) and C2 (depth) causally separable?

**Verdict.** Separable **as instruments**; coupled **as records**, one-directionally
(C1 reads what C2 lands; C2 reads nothing C1 lands). The coupling can only *fail* C1 —
it cannot manufacture a pass in either direction, so it is **not fatal to scoring
integrity**. It **is** fatal to the claim "independent axes" if a seat reads a green C1
as independent corroboration of C2's depth.

**Separate defect found en route (not separability):** all five amendments carry
`rule_changed: false`, and two of them (A2, A5) change the pass predicate / m9 acceptance
set (§5).

---

## 0. What I ran (permitted only; no default-mode run at the tip)

| run | command | result |
|---|---|---|
| base fidelity | `calibration/measure.py --rev a3d6c690…` | `m6=1 m9=1 total=2` — matches contract `before` exactly |
| control | `census/measure.py --control` | `C2_R41_CONTROL_PASS=false` — matches contract |
| base | `census/measure.py --rev a3d6c690…` | `tool_absent=1 … C2_R41_PASS=false` — matches contract |
| pre-run | `calibration/measure.py --rev work` (03:42) | `total=0 PASS records=2 sources_rows=109` |
| scratch | `/tmp/tameshi-r41-critic-causal/{lane,now,vA…vL,e3,e4,g2,k,l}` | disposable git repos built from `rsync` copies; the lane, its index and jj state untouched |

No tool installed or upgraded. Scratch is under `/tmp`, outside `.ufo/waves/`.

The C1 counter changed under this review (pin drift while I read it, §5). The final bytes
and the pin now agree at
`9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd`; all scratch
conclusions below were re-run against those bytes except where another sha is named.

---

## 1. Read sets, exact

**C1 counter** `.ufo/evidence/round-41/calibration/measure.py`:

| input | anchor |
|---|---|
| `corpus/SOURCES.md` — S-row count + `status` | `S_ROW_RE` :43, `registry()` :135-140, `status = cells[8]` :137 |
| `SCORECARD.md` — **last** `\| sources-registry \|` row, `(\d+) rows` | :218 (`standing[-1]`) |
| `corpus/lessons/round-41.md`, `SCORECARD ## Round 41`, `LOG ## 2026-10-25 — round 41` | :142-148 |
| `git cat-file -e REV:<path>` for every backticked token under `corpus/`, `tools/`, `.ufo/evidence/round-41/`, `.ufo/waves/round-41/` | `resolves()` :111-118, `PATH_PREFIXES` :46-51, `path_tokens()` :181-190 |
| `corpus/lessons/round-40.md` — quarantine table vs summary | m9 block, derived words :253-258 |

**C2 counter** `.ufo/evidence/round-41/census/measure.py`: `TOOL`, `V2`, `FIXTURES`,
`CONTRACT`, `LIVE` (:25-29); of the contract it consumes **only**
`claims.C2.tool_sha256` (:146); v2 is a hardcoded `V2_SHA` (:30); live sites are the
hard-coded windows `805..815` / `815..825` (:224, :226).

**Intersection:** `corpus/SOURCES.md` (C1 reads the rows; the round's entries S153/S154
land there) and `contract.json` (C2 reads it; C1 does not). No shared code, no import, no
hash chain links the two counters.

---

## 2. Direction A — can C1 verify if C2's tool, fixtures and entry never landed?

**With the records as they stand: no.** Scratch `e3` = current tree, minus
`tools/write-path-census-v3.py`, minus `.ufo/evidence/round-41/census/`, minus rows
S153/S154, minus `corpus/knowledge/r41-variable-destination-writes.md`; record text
untouched:

```
C1_R41: m6=1 m7=6 m8=7 m9=0 total=14 records=3 sources_rows=107 C1_R41_PASS=false
```

- **m6** — standing row declares 109; withholding the two entries leaves 107 (:218).
  Isolated: 109/109 → `m6=0`; 109 declared / 108 present → `m6=1`.
- **m7** — S153/S154 are cited in all three records, so 2 ids × 3 records = 6. The class
  counts per record, not per distinct id.
- **m8** — `tools/write-path-census-v3.py`, `.ufo/evidence/round-41/census/fixtures.json`,
  `.ufo/evidence/round-41/census/measure.py`, `corpus/knowledge/r41-variable-destination-writes.md`.

**Instrument-wise: yes.** Scratch `e4` = identical removals, records rewritten to cite no
S-id and no C2 path, **same counter bytes (9aaa99…)**:

```
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=1 sources_rows=107 C1_R41_PASS=true
```

So the counter never opens a C2 artifact. The dependency is entirely in the **record
text** and in m6's denominator, not in the measurement.

---

## 3. Direction B — can C2 verify if C1's edits never landed?

**Yes, unconditionally.** Scratch `g2` = current tree with `SCORECARD.md`, `LOG.md`,
`corpus/SOURCES.md` and `corpus/lessons/` deleted, committed:

```
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1
var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1
scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811
live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0
live_symlink_lineno=820 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1
live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1
mutant_symlink_arg_killed=1 rev=HEAD C2_R41_PASS=true
```

exit 0, full 25-field line. C2 opens no `corpus/`, no `SCORECARD`, no `LOG`, no lesson.
Its only non-C2 input is the wave-0 contract's tool pin, which is not a C1 edit.

---

## 4. Is the coupling fatal?

**Not to scoring.** The coupling is one-directional and can only *subtract*: if C2's entry
is missing, C1 gains mismatches; it never gains a pass it did not earn. Symmetrically C2
cannot ride on C1 (G2). The C1-owned classes stay C1-owned: m9's correction lives only in
the round-41 lesson (`e4` keeps `m9=0` only because the lesson restates the table), and m6's
declaration lives only in SCORECARD — C2 contributes to neither.

**Yes to the wording "independent axes"**, if that means evidence independence: a green C1
is *not* independent corroboration of C2's depth. It should be reported as a joint-revision
property.

**Note on A1.** With the original frozen bytes (`f00917…`, `cells[9]`) m7 fired on *every*
cited id — citing S001, status `mined`, produced `m7 S001 cited but status=2026-10-19`
(scratch `vA`). That bug masked the entry-absent signal (absent and mined were
indistinguishable). A1 restores the signal and therefore *exposes* this coupling; that is
correct behaviour, not a regression.

---

## 5. Freeze integrity — the drift is fixed; two amendments still misdeclare `rule_changed`

**Resolved during the review.** At 03:43:54–03:45:39 the pin was `8bc9b422…` while the
bytes were `9aaa99ac…` (counter mtime 03:43:31, contract 03:43:22; A4 recorded
`new_sha256: 8bc9b422`, not the bytes). A5 landed at ~03:46 and the pin now equals the
bytes: `9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd`. Scratch runs
above use those bytes, so they match the pin.

**What is still wrong — every amendment declares `rule_changed: false`; two of them
change the rule:**

- **A5** replaces m9's literal gate (`'six refused' in correction and 'ten present' in
  correction`) with words derived from the round-40 table (`.ufo/evidence/round-41/calibration/measure.py:253-258`,
  `want_refused`/`want_present`). That changes which records can silence m9 — the
  acceptance set. A5's own `what` states the defect that made the change necessary. For
  this round's table (6 refused, 10 present) the outcome is identical, so the change is
  **latent**, but the declaration is still wrong.
- **A2** adds a required conjunct to `claims.C2.predicate` — "all three recognizer mutants
  (name resolution, symlink branch, symlink destination argument) make the v3 selftest
  fail" — and a required field to `claims.C2.target`
  (`mutant_symlink_arg_killed=1`). Narrowing the pass predicate is a rule change by any
  reading.
- Consequence for a reader: the ledger cannot be used as evidence that "only bugs were
  fixed". The predicate/target/gate text has to be diffed, not the flag.

**Enforcement gap (unchanged by A1–A5).** No counter verifies its own sha (the C1 counter
has no `hashlib` at all). The C2 counter consumes only `claims.C2.tool_sha256`
(`census/measure.py:146`), so `fixtures_sha256` (A2's new `20b6254d…`), `counter_sha256`
and `v2_sha256` are prose. The v2 pin exists **twice** — contract
`claims.C2.v2_sha256` and hardcoded `V2_SHA` (`census/measure.py:30`) — with nothing tying
them. A2's fixture re-pin is therefore decorative: fixtures.json can change and C2 still
passes while the four derived fields match.

**Smallest safe correction.**

1. Set `rule_changed: true` on A2 and A5 (or append A6 saying so). Do not leave a ledger
   that claims no rule moved when the predicate did.
2. Make the C2 counter read `claims.C2.v2_sha256` and `claims.C2.fixtures_sha256` and
   assert them (emit `v2_pin_ok`, `fixtures_sha_ok`); delete the duplicate `V2_SHA`
   constant so there is one authority.
3. Have each counter print its own sha in the output line; the L1 files it with the
   receipt so "the pinned counter produced this" is checkable without out-of-band state.

---

## 6. The landing-order risk that will actually decide C1 (independent of C2)

Every backticked path in the three records is load-bearing, and m8 counts per record.
Today the records cite seven paths that are **on disk but absent at HEAD**:

`.ufo/evidence/round-41/sources/ast.html` (lesson, LOG), `…/pathlib.html` (lesson),
`corpus/knowledge/r41-variable-destination-writes.md` (lesson, SCORECARD, LOG),
`corpus/lessons/round-41.md` (SCORECARD, LOG), `.ufo/waves/round-41/dispatch-w1.json`,
`…/spec-w1.json`, `…/w1/swarm-registry.json` (LOG).

Measured exactly:

| scratch revision | result |
|---|---|
| all committed (`now`) | `total=0 PASS` |
| records + SOURCES committed, the 6 evidence files omitted (`l`) | **`m8=9 total=9`** |
| the above **plus** the lesson omitted (`k`) | `m6=1 m7=4 m8=8 m9=1 total=14` |

So: commit `.ufo/evidence/round-41/sources/{ast,pathlib}.html`,
`corpus/knowledge/r41-variable-destination-writes.md`,
`.ufo/waves/round-41/{dispatch-w1.json,spec-w1.json,w1/swarm-registry.json}`,
`corpus/lessons/round-41.md`, the SCORECARD/LOG sections and SOURCES S153/S154 **before**
the deciding run — or drop the backticks on any wave-plan file that is meant to stay
ephemeral.

Also: a `--rev work` pass is not a `--rev <sha>` pass. `resolves()` tests
`os.path.exists` in work mode and `git cat-file` in rev mode (:111-118); scratch H4/H5 are
the same working tree scoring `m8=1` at a sha and `m8=0` at `work`.

---

## 7. Counterexample tested (strongest available)

**Hypothesis under attack:** "C1 is an independent witness that C2's depth claim is real."
**Counterexample:** `e3` — leave C1 untouched, remove only C2's deliverables, and C1 falls
from `total=0` to `total=14` with every mismatch on a C2-owned artifact. C1 therefore has
no independent standing to corroborate C2. It still cannot *pass* C2 (G2), and C2 cannot
*pass* C1 (m9 is lesson-only), so the pair remains impossible to mask — but any scorecard
that presents C1 and C2 as independent evidence must be corrected to "one joint revision,
two disjoint instruments."

**Command for the deciding run (record the shas beside it):**

```
sha256sum .ufo/evidence/round-41/calibration/measure.py .ufo/evidence/round-41/census/measure.py
python3 .ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <sha-with-every-cited-path-committed>
python3 .ufo/evidence/round-41/census/measure.py  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <same sha>
```

Report: `.ufo/waves/round-41/w1/CriticCausalSeparability.md`
