# T53W1Read02 — cold read of SKILL.md section `## Effective expectation reconciliation — round 14`

Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
Read at content commit C* = a41195dfc13a73958e4c5228ec196b28d03ded03, via git objects only:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md
```

Working tree was never read for section content. Scratch: /fast/scratch/hyaku/tameshi-r53/w1/T53W1Read02 (removed before yielding).

## Section split

Fence-aware split of the C* blob (a line matching `^#{1,3}(\s|$)` outside ``` fences starts a section):

```
heading: ## Effective expectation reconciliation — round 14   (line 1570, 1-based)
next heading: ### Round-14 historical registry — superseded by round 15 (line 1604)
section lines 1570–1602 (33 lines, 3010 bytes), no trailing newline
section_sha256 = 664a9dfb18fc4318feb4321cc23ad69ffd742e5e37c1477b7b63abd8d05827e1
```

Line 1603 is whitespace-only and was stripped; the hash was recomputed after stripping.

## Finding 1 — incomplete attribution of the stale pinned inputs

Quote (byte-exact substring of the section):

> their pinned inputs moved after round 14: the runner in round 16, the bash witness-study tool in rounds 18 and 21

The sentence at lines 1588–1589 reads: "at `--root .` both manifests now return 2 `expected_input_digest_mismatch` (their pinned inputs moved after round 14: the runner in round 16, the bash witness-study tool in rounds 18 and 21)". The exit-2 behaviour holds (checked below), but the parenthetical enumerates two movements and reads as the account of which pinned inputs moved. At C* **three** of the thirteen inputs pinned by `.ufo/evidence/round-13/expected.json` are stale, and the third one moved before either named round.

Evidence:

1. Pinned digests vs live bytes at C* (all thirteen inputs checked):

```
tools/mutate-and-run.sh       pin 75ed934dc863…  live 977de47034cb…   MISMATCH
tools/bash-witness-study.py   pin 49e9e5e20b73…  live cca77724c476…   MISMATCH
tools/pin-disposition.py      pin 297253971dab…  live ae4a6763cd5d…   MISMATCH
(the other ten inputs match)
```

2. `tools/pin-disposition.py` was still at the pinned bytes at the replay commit, so its movement is after round 14:

```
$ for rev in 28aeef4 05a2247 2a22ade; do git show $rev:tools/pin-disposition.py | sha256sum | cut -c1-12; done
297253971dab      # 28aeef4 (round-15 archive, used by this recipe)
297253971dab      # 05a2247 (round 16)
331529eadafe      # 2a22ade (round 17) — moved here
```

3. `git log` for that path between the archive and C*: round 17 (`2a22ade`) and round 53 (`218bc6b`, this round's TMPDIR fix). The runner and `bash-witness-study.py` also moved at `218bc6b`. So the enumeration is stale twice over at C*: it omits a third pinned input entirely, and the two named ones moved again this round.

4. The command a reader actually runs reports only the first mismatch in sorted order, which is `tools/bash-witness-study.py` — not the runner the parenthetical names first:

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
{ "error": { "kind": "expected_input_digest_mismatch",
             "message": "tools/bash-witness-study.py: observed cca77724c476… expects 49e9e5e20b73…" }, "exit": 2, … }
```

Why it fails: a cold reader is told which pinned inputs moved and gets an incomplete list; `tools/pin-disposition.py` is a third stale input whose movement (round 17, commit 2a22ade) is neither named nor derivable from the text.

## Holds (checked, no finding)

- **Line 1587 — "distinguish twelve expected rows from thirteen pinned inputs".** `.ufo/evidence/round-13/expected.json` has `expected_checks` = 12 and `inputs` = 13. The round-14 manifests each carry 12 rows and 3 pinned inputs.
- **Line 1588 — "at `--root .` both manifests now return 2 `expected_input_digest_mismatch`".** Executed at C*:

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json   → exit 2, id expected_input_digest_mismatch
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json          → exit 2, id expected_input_digest_mismatch
```

  (Both status `could_not_evaluate`. Only the parenthetical attribution fails — see Finding 1.)
- **Line 1588 — runner pinned at `75ed934d…`.** `.ufo/evidence/round-13/expected.json` pins `tools/mutate-and-run.sh` at `75ed934dc863…`; the round-14 context receipt records the same runner digest (`sources.runner.sha256`).
- **Lines 1589–1591 — replay → 1, `producer_before`.** Extracted `git archive 28aeef4` into scratch, ran from that cwd:

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json
exit 1; status failed; counts effective 12, passed 11, failed 1
finding: expected_contains_missing — producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'
tool header: evidence-disposition.py r14
```

- **Lines 1592–1593 — same replay with `dispositions.json` → 0.** Exit 0, status clean, counts effective 11, superseded 1, passed 11, findings 0. A `diff` of the two manifests shows the only difference is the `producer_before` row: `state` effective→superseded plus `reason`, `raw_receipt`, `raw_check`, `superseded_by: [producer_before_oracle, producer_after_oracle]`. So "the only repair is that row's explicit supersession, keeping raw receipt/check and both passing replacements" holds; the two replacements are `state: effective` and pass in the clean run.
  - Reader caveat (not a finding): item 3 reads "The same command with … → 0" after item 2 has just stated the live-tree result is 2 for both manifests. The antecedent is the replay command of item 2, and the trailing clause "Live-tree form: the round-17 re-pin section" marks the live path as separate, so the text is consistent under the natural reading; executed literally from the lane root, that command returns 2.
- **Line 1593 — "Live-tree form: the round-17 re-pin section (round-18 manifests since then)".** The heading `## Live-tree re-pin and entry-command monitor — round 17` exists at C*; the round-18 manifests are the live entry the round-15 registry row names, and at C* they are still clean:

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json → exit 0, status clean
```

- **Lines 1594–1598 — the two round-14 receipts.** `verification-final.json`: `disposition_selftest` exit 0 expected 0 with stdout `34/34`, plus the frozen before/after checks (exit 1 expected 1; exit 0 expected 0) and `context_capture.measured_commit`. `verification.json`: `disposition_selftest` exit 1 expected 0 with stdout containing `18/34`, and the same before/after outcomes. The initial failures are retained, not relabelled green. The final receipt's `supersedes` field names only the selftest failure. `measured_commit` is recorded per receipt (`0c6e36d0…` vs `6431478…`).
- **Lines 1599–1602 — archived capture-context.** `.ufo/evidence/round-14/capture-context.py` exists at C*, its `OUTPUT_REL = .ufo/evidence/round-14/context-receipt.json`, and the retained receipt records `tool_sha256 = 7313e9a208ac…`, which equals the sha256 of those very bytes; re-running the archive copy would overwrite the frozen receipt at that path. So the "archived experiment, not an entry point" directive holds.
- **Line 1602 — "the maintained retained-only gate in the round15 registry below".** `### Round-15 gate/probe registry` sits below the section and its first row is `retained invocation-context gate` with entry `python3 tools/context-capture.py --check`; the row's pinned receipt digest `05cb55b8…` matches the receipt at C* and the gate is still green:

```
$ python3 tools/context-capture.py --check
CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b86446… exit=0 findings=0)   EXIT=0
```

- **Sources line (1572–1575).** `corpus/lessons/round-13-verifier-spotcheck.md`, `corpus/knowledge/incremental-pin-disposition.md` and `tools/context-capture.py` are present at C*; the knowledge file's `## 8. Empirical correction and backlink — round 14 (2026-10-20)` is the cited §8 and does record the twelve-row/eleven-effective-plus-one-superseded ledger and the 18-of-34 → 34/34 selftest history; `corpus/SOURCES.md` carries S049 as "Python subprocess environment mapping … `run()` env argument semantics, not proof of a particular historical environment" and S003 as the StrykerJS incremental page with §Limitations.
- **Table rows (1579–1583).** Each condition matches the tool semantics exercised above: exit equality alone is not mechanism proof (the `producer_before` FileNotFoundError case), supersession keeps raw receipt+check with both replacements effective, digest mismatch is `could_not_evaluate` (exit 2), a new experiment establishes only its own documented override, and one GIT_DIR injection yields a bounded scrub observation. No row contradicts the executed behaviour.

## Out of scope

- Round-15 registry row values beyond the pointer (row 1's own verdict map, pinning of expected-pin schema) were read only to confirm the pointer resolves; their accuracy is that section's claim, not this one's.
- The other nine inputs of `expected.json` were checked for mismatch but not audited for provenance.
- No product file, tool, corpus file or evidence file was modified; no git/jj mutation was run; the only writes are the two deliverables.

## Tooling

No installs or upgrades were needed. Commands used: coreutils (`sha256sum`, `diff`), `python3` (3.x in-path), `git` (read-only: show/log/cat-file/ls-tree/grep/archive).

## Artifacts

- .ufo/waves/round-53/w1/T53W1Read02.json
- .ufo/waves/round-53/w1/T53W1Read02.md
