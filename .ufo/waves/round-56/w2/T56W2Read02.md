# T56W2Read02 — cold-read re-read 2/18 (round 56, wave 2)

- Heading: `## Effective expectation reconciliation — round 14`
- Candidate (content commit C0): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
- Section sha256 (frozen round-18 sectionize, computed at C0): `6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe`
- Section extent at C0: lines 1606–1639 of `SKILL.md` (same bytes as at base 981c5e8b, where the extent is 1593–1626)
- Verdict: **verified-record** (no false statement in the section; every command it names runs and produces the outcome it claims)
- Findings: **0** · Notes: 11 (see `T56W2Read02.json`)

Every command below was run in a scratch clone of the lane at C0
(`git clone --shared` then `git -C <clone> checkout --detach c0137451…`;
`git rev-parse --show-toplevel` printed the scratch clone path), plus an
extracted `git archive 28aeef4` tree for the frozen replay. The lane tree was
read only; no lane production file was edited, no mutating git command was run
anywhere, and the clone's `git status --porcelain` returned zero lines after
every run. Receipts: `.ufo/waves/round-56/w2/T56W2Read02-receipts/` (files 00–15).

## How the sha256 was computed (frozen sectionize, never reimplemented)

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
```

loaded into `.ufo/evidence/round-18/measure.py` via `importlib`
(`m.sectionize(raw)`). That module's blob sha256 is
`7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` — identical
at base, at the round-56 freeze `c3e2ca9f`, at the C0 blob, and in the
worktree copy, so the instrument is the frozen one. Result:
`1606 1639 6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe`
(receipt `13-sectionize-at-C0.txt`).

The same sha256 holds at 99c3bc8 (round-54 C1), 9cf0146 (round-55 C0), 51d1f0e
(round-55 fix), 981c5e8b (base) and c0137451 (C0): the section's bytes did not
move in rounds 54–56, only its line numbers did (1593–1626 → 1606–1639). That
is exactly why this heading is in the lost-headings list — a line-range drift,
not a content change.

## Commands run, and their outputs

### 1. Live tree, round-14 manifest before (step 2's live arm)

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json
```

exit **2**, `status: could_not_evaluate`, `id: expected_input_digest_mismatch`,
naming `tools/bash-witness-study.py` (observed `f2bb50c7…` vs expected
`49e9e5e2…`). The section says "both manifests now return 2
`expected_input_digest_mismatch`" — **holds** (receipt `01`).

### 2. Live tree, round-14 manifest after

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
```

exit **2**, same id, same first-mismatching input. **Holds** (receipt `02`).

### 3. The three stale pins, computed independently

Hashing all thirteen `inputs` of `.ufo/evidence/round-13/expected.json` against
the C0 bytes: exactly **3 stale** — `tools/pin-disposition.py`,
`tools/bash-witness-study.py`, `tools/mutate-and-run.sh`. The section's "three
of its thirteen inputs are stale at the live bytes" **holds** (receipt `05`).
`expected_checks` = **12**, `inputs` = **13**, matching "twelve expected rows
from thirteen pinned inputs" (receipt `05`).

### 4. Round attributions, first mover after the `git archive 28aeef4` baseline

```
git log --oneline --ancestry-path 28aeef4..c0137451 -- tools/mutate-and-run.sh
git log --oneline --ancestry-path 28aeef4..c0137451 -- tools/bash-witness-study.py
git log --oneline --ancestry-path 28aeef4..c0137451 -- tools/pin-disposition.py
```

- runner: `c699c8c` (round 16) — "the runner in round 16" **holds**
- witness-study tool: `58e5d53` (round 18), then `370f2df` (round 21) — "in rounds 18 and 21" **holds**
- `tools/pin-disposition.py`: `2a22ade` (round 17) — "in round 17" **holds**

The trailing clause "before either named round" reads, against the only two
rounds jointly named in the parenthesis (18 and 21), as *round 17 precedes both
rounds 18 and 21* — **true and checkable**:

```
git merge-base --is-ancestor 2a22ade 58e5d53   # exit 0
git merge-base --is-ancestor 2a22ade 370f2df   # exit 0
```

commit dates `2a22ade 2026-10-20 12:06 < 58e5d53 2026-10-20 17:20 < 370f2df 2026-10-21 09:24` (receipt `08`).

### 5. Frozen replay in an extracted `git archive 28aeef4` tree

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json
```

exit **1**, `status: failed`, `counts {effective 12, expected_checks 12, failed 1,
findings 1, passed 11, superseded 0}`, finding
`producer_before: stdout lacks 'summary preserves top-level exposed declaration
kind'` — the section's "→ 1, failing the unresolved producer_before assertion"
**holds** (receipt `03`).

The replay reproduces the committed receipt byte-for-byte except the `root`
field:

```
recorded  "root": "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
replay    "root": "/fast/scratch/…/arch28"
```

— one differing line, nothing else. The replay's tool digest
(`1609a9df…`, "evidence-disposition.py r14") equals the pinned
`input_sha256` of `tools/evidence-disposition.py` in
`.ufo/evidence/round-14/verification-final.json`, and the archive tree ships
that same r14 build (receipt `03`, `09`).

### 6. The same command with the repaired manifest → 0

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
```

exit **0**, `status: clean`, `counts {effective 11, expected_checks 12, failed 0,
findings 0, passed 11, superseded 1}` — the section's step 3 **holds** (receipt `04`).

That the row's explicit supersession is the **only** repair is checkable by
diffing the two manifests' row states: exactly one change —
`producer_before effective → superseded` — and the superseded row keeps
`raw_receipt .ufo/evidence/round-13/verification.json`, `raw_check
producer_before`, `superseded_by [producer_before_oracle,
producer_after_oracle]`, with both replacements effective and passing (receipt
`10`).

### 7. Step 3's live-tree pointer — the round-17 re-pin section

```
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json
```

round-18 `dispositions.json` → exit **0** clean (`effective 11, superseded 1`);
round-18 `dispositions-before.json` → exit **1** failed on `producer_before`;
round-17 `dispositions.json` → exit **2** `expected_input_digest_mismatch`. The
section's "Live-tree form: the round-17 re-pin section (round-18 manifests since
then)" **holds** (receipts `07`, `14`).

### 8. Step 4 — the two round-14 receipts

`.ufo/evidence/round-14/verification-final.json`: `disposition_selftest` exit 0,
`unresolved_before` 1/1, `resolved_after` 0/0 — "retains the corrected selftest
and frozen before/after outcomes" **holds**.
`.ufo/evidence/round-14/verification.json`: `disposition_selftest` stdout
carries `SELFTEST: FAIL (18/34 failed: …)` — "retains the initial 18-of-34
fixture failures rather than disguising them as green" **holds**. Each receipt
records its own `measured_commit` (`64314783…` and `0c6e36d0…`, both resolvable
commits) — "the revision measured is recorded separately" **holds** (receipt `09`).

### 9. Step 5 — the archived experiment and the maintained gate

```
python3 tools/context-capture.py --check
```

exit **0**, `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8… exit=0 findings=0)`.
The retained receipt's digest equals the digest the round-15 registry pins, and
`.ufo/evidence/round-14/capture-context.py` has
`OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"` — its historical
output path is the frozen receipt's own path, so re-running it would replace
the frozen receipt. Both halves of step 5 **hold** (receipts `11`, `12`).

### 10. The section's Sources line

`corpus/lessons/round-13-verifier-spotcheck.md` exists with a "Routed defects
and residuals" section whose items 1–3 cover exactly this subject matter;
S049 is the Python subprocess environment-mapping source (its teaches cell is
the explicit env/child-environment contract); S003 is the StrykerJS incremental
source whose Limitations the knowledge entry re-opens;
`corpus/knowledge/incremental-pin-disposition.md` §8 is "Empirical correction and
backlink — round 14", the entry `corpus/README.md` labels "empirical
correction8" — all **hold** (receipts `05`, `06`).

### 11. Census (lane-level)

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

exit **0**, output byte-identical to the committed
`.ufo/evidence/round-56/census-start.stdout`. The census reports
`tameshi rows 142` for the C0 tree and `rows 140` for the base registry
(`git show 981c5e8b:corpus/SOURCES.md | grep -c '^| S[0-9]'` → 140), so the
round-56 C0 commit `c0137451` added **two** SOURCES rows (S281, the in-toto
Statement layer specification, and S282, the SLSA provenance specification) and
the count is 142, not the 141 this wave's brief assumes. Flagged to the L1 as
an adjacent observation; it is not a statement of this heading.

## Verdict

**verified-record** — no statement in this section is false of the tree at C0,
and every command the section names a reader to run exists, runs, and produces
the outcome the section claims. Eleven notes carry the round-57 wording
suggestions (chief among them the "before either named round" and "which the
commands below name" phrasings, both carried over unrouted from round 54's
T54W2Read15 and both re-adjudicated here as loose rather than false), the
first-mover-only nature of the round attribution, and the corpus row count.
No lane file was edited; `SKILL.md` is untouched.
