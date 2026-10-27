# T53W2Read01 — re-read of `## Effective expectation reconciliation — round 14` at C**

Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
Candidate read: C** = 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e, via git objects only:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md > .../SKILL.C2.md
```

The working tree was never used for section bytes (the live tree is at d008822 and differs from C** in SKILL.md by one errata line). Section and pin bytes were read from git objects; commands ran either in a `git archive` extraction of C** / `28aeef4`, or — where a command needs a git work tree (the waiver-bearing round-18 manifest) — from the lane root, whose `tools/` and evidence bytes equal C** (`git diff --stat 5b703c6..HEAD -- tools/` is empty). Scratch: /fast/scratch/hyaku/tameshi-r53/w2/T53W2Read01 (removed before yielding).

## Section split (verified before hashing)

Fence-aware split per the frozen monitor (`.ufo/evidence/round-18/measure.py:sectionize`, `^#{1,3}(\s|$)` outside ``` fences, heading line through the line before the next heading, trailing whitespace-only lines stripped, `\n`-joined, no trailing newline, sha256 over UTF-8 with surrogateescape):

```
heading:      ## Effective expectation reconciliation — round 14   (1-based line 1581)
next heading: ### Round-14 historical registry — superseded by round 15 (1-based line 1615)
body:         lines 1581-1614; line 1614 is whitespace-only and was stripped
body size:    33 lines, 3135 bytes, no trailing newline
section_sha256 = 9640e5dc426f1f9ed7050e2443ac96c478e008ed9c2948ad59790da8aa977e3d
```

The hash was produced twice — by importing the frozen `sectionize()` (start=1581, end=1614, sha256 as above) and by a hand split over the same line window — and both agree. `SKILL.md` at C** holds 64 sections.

## Fix verification (done first)

Wave-1 seat `T53W1Read02` filed one finding against this section at C*: the stale pinned inputs were under-attributed — the text named two movements and omitted `tools/pin-disposition.py` (round 17), although three of the thirteen pinned inputs were already stale at C*.

`diff` of the section at C* (a41195d) against C** shows exactly one changed line and nothing else in the section moved:

```diff
-   `expected_input_digest_mismatch` (their pinned inputs moved after round 14: the runner in round 16, the bash witness-study tool in rounds 18 and 21). Replay with cwd = an extracted
+   `expected_input_digest_mismatch` (their pinned inputs moved after round 14: three of the thirteen are stale at the live bytes — the runner in round 16, the bash witness-study tool in rounds 18 and 21, and `tools/pin-disposition.py` in round 17, before either named round). Replay with cwd = an extracted
```

The C** sentence, byte-exact:

> three of the thirteen are stale at the live bytes — the runner in round 16, the bash witness-study tool in rounds 18 and 21, and `tools/pin-disposition.py` in round 17, before either named round

Each element of that sentence was re-measured at C**:

**(a) Exactly three of the thirteen are stale, and they are the three named.** All thirteen pins of `.ufo/evidence/round-13/expected.json` compared against the C** blobs:

```
OK    .ufo/evidence/round-12/BashWitness/summary.json                 acc01268cb5f
OK    .ufo/evidence/round-12/BashWitness/declaration.json             e8d2024ad13e
OK    .ufo/evidence/round-12/BashWitness/declared.tsv                 0def0d3b3702
OK    .ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json 6726421fde88
STALE tools/pin-disposition.py           pin 297253971dab  live 07a3e0411dd6
OK    tools/witness-metadata.py          df3390682a04
STALE tools/bash-witness-study.py        pin 49e9e5e20b73  live 4e999ff45539
STALE tools/mutate-and-run.sh            pin 75ed934dc863  live 977de47034cb
OK    .ufo/evidence/round-13/pin-manifest.json 64eaa43e3f7a
OK    .ufo/evidence/round-13/witness-metadata.json 463282270a04
OK    .ufo/evidence/round-13/witness-metadata-old-null.json 28067a1cb76b
OK    .ufo/evidence/round-13/producer-before.py 592c5c3de86a
OK    .ufo/evidence/round-13/producer-oracle.py d5ae0bd4d4f7
stale count 3
```

The same three (same live digests) are stale at the live working tree, so the "live bytes" reading of the clause is also exact:

```
stale at working tree: 3
('tools/pin-disposition.py', '297253971dab', '07a3e0411dd6')
('tools/bash-witness-study.py', '49e9e5e20b73', '4e999ff45539')
('tools/mutate-and-run.sh', '75ed934dc863', '977de47034cb')
```

**(b) The pinned digests are the round-14-era bytes, so every named round is a post-round-14 move.** At the replay commit `28aeef4` (round-15 archive used by this recipe):

```
tools/mutate-and-run.sh          75ed934dc863   == pin
tools/bash-witness-study.py      49e9e5e20b73   == pin
tools/pin-disposition.py         297253971dab   == pin
```

**(c) The movement rounds named are the first post-round-14 moves.** `git log 28aeef4..5b703c6 -- <path>`:

```
tools/mutate-and-run.sh      c699c8c (round-16), 05a2247 (round-16), 2a22ade (r17), 58e5d53 (r18), a08e85c (r26), bb68156 (r30), 6d8c11e (r51)
tools/bash-witness-study.py  58e5d53 (round-18), 370f2df (round-21), 218bc6b (r53), 5b703c6 (r53)
tools/pin-disposition.py     2a22ade (round-17), 218bc6b (r53), 5b703c6 (r53)
```

The runner's earliest post-round-14 change is round 16, the witness-study tool's is round 18 with a second at round 21, and `tools/pin-disposition.py` moved at round 17 (`2a22ade`, bytes `331529eadafe`, differing from the pin). One post-round-14 change is sufficient for a pin to be stale, so the enumeration is a valid explanation of the staleness even though later rounds (r26/r30/r51 for the runner, r53 for the other two) moved the bytes again.

**(d) The ordering clause is true for the two rounds that follow it.** `git merge-base --is-ancestor`: `2a22ade` (r17) is an ancestor of `58e5d53` (r18), which is an ancestor of `370f2df` (r21) — so round 17 is before either of the rounds the witness-study tool is named with. Caveat 1 below records the wording weakness; no false reading is forced.

**Verdict: the wave-1 finding is resolved at C**. The three stale inputs are named, the count matches the bytes, and each named round is the input's first post-round-14 move.

## Holds (each backed by an executed command or a byte comparison at C**)

- "distinguish twelve expected rows from thirteen pinned inputs." — `.ufo/evidence/round-13/expected.json` at C** has `expected_checks` = 12 and `inputs` = 13.
- "at `--root .` both manifests now return 2" — executed from the lane root at C** (and again in a `git archive` extraction of C**, same result):

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json   → exit 2
{ "error": {"kind": "expected_input_digest_mismatch",
            "message": "tools/bash-witness-study.py: observed 4e999ff45539… expects 49e9e5e20b73…"},
  "exit": 2, "id": "expected_input_digest_mismatch", "status": "could_not_evaluate" }
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json          → exit 2
  status could_not_evaluate  id expected_input_digest_mismatch
```

  The reported input is the witness-study tool (the first mismatch in sorted order); the sentence names the runner first but claims no reporting order. Row 3 of the table ("Snapshot input or receipt bytes differ from their pinned digest | Could-not-evaluate") is exactly the observed status.
- "Replay with cwd = an extracted" `git archive 28aeef4` tree → 1: extracted `git archive 28aeef4` into `tree28` and ran the archive's own tool there (`evidence-disposition.py r14`, tool_sha256 `1609a9df970d`):

```
exit 1, status failed, counts {effective 12, expected_checks 12, failed 1, findings 1, passed 11, superseded 0}
finding: expected_contains_missing — "producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'"
```

  This is exactly the table's first row: the exit matches, the assertion is absent, so it is a failed expectation and not mechanism proof (the receipt describes the raw `FileNotFoundError` before the assertion).
- "→ 1, failing the unresolved producer_before assertion (a matching exit 1 alone is insufficient)." — same run; the failing id is `producer_before`.
- "3. The same command with `.ufo/evidence/round-14/dispositions.json` → 0: the only repair is that row's explicit supersession," + "keeping raw receipt/check and both passing replacements." — same cwd:

```
exit 0, status clean, counts {effective 11, expected_checks 12, failed 0, findings 0, passed 11, superseded 1}
```

  A field-by-field diff of the two manifests: 12 rows each, only row 4 (`producer_before`) differs — `state` effective→superseded, plus `reason`, `superseded_by: [producer_before_oracle, producer_after_oracle]`, and the same receipt/check values carried as `raw_receipt: .ufo/evidence/round-13/verification.json`, `raw_check: producer_before`. Both replacements are `effective` in the clean run and 11/11 effective rows pass, so "both passing replacements" holds; nothing was dropped.
- "keeping raw receipt/check and both passing replacements. Live-tree form: the round-17 re-pin section (round-18 manifests since then)." — the pointer's target heading exists at line 1832, and the live entry it names (the round-18 manifest, no replay) returns the claimed outcome from the lane root at C**: exit 0, counts 11/0/11/1, with `expected_inputs_historical` anchoring the three moved tools at `4acc607dfd79…`. Details in caveat 3.
- "4. `.ufo/evidence/round-14/verification-final.json` retains the corrected" selftest and the frozen before/after outcomes — the receipt's checks are the clean selftest (`SELFTEST: PASS (34/34)`, exit 0), the frozen before run (exit 1, counts 12/1/11) and the frozen after run (exit 0, counts 11/0/11), with `context_capture.measured_commit` recorded.
- "initial 18-of-34 fixture failures rather than disguising them as green." — `.ufo/evidence/round-14/verification.json` retains `SELFTEST: FAIL (18/34 failed: clean-superseded, unsuperseded-crash-mismatch, …)` exit 1, plus the same before/after outcomes; its `supersedes`-less note keeps the raw record and the final receipt's `supersedes` names only the selftest failure.
- "The revision measured is recorded separately." — the two receipts carry different `measured_commit` values (`verification-final` 64314783836b…, `verification` 0c6e36d0bd2f…).
- "5. **Archived experiment, not an entry point:** the round-14 copy" — `.ufo/evidence/round-14/capture-context.py` has `OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"` and sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, which is exactly the `tool_sha256` retained in that receipt; re-running the archive copy would overwrite the frozen receipt.
- "Use the maintained retained-only gate in the round15 registry below." — `### Round-15 gate/probe registry` is at line 1694, below this section, and its first row is `retained invocation-context gate` with entry `python3 tools/context-capture.py --check`. Executed in `treeC2`:

```
CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b86446… exit=0 findings=0)   exit 0
```

  `05cb55b8…` is the digest the registry row pins, and the registry's closing paragraph confirms the gate replays recorded predicates rather than re-executing stored argv, which matches "retained-only".
- "Sources: `corpus/lessons/round-13-verifier-spotcheck.md`, Routed defects 1–3;" — the lesson file has `## Routed defects and residuals`; `corpus/SOURCES.md` carries S049 ("Python subprocess environment mapping … `run()` env paragraph, not proof of a particular historical environment") and S003 ("StrykerJS incremental verdict reuse … §Limitations … env vars, dependencies and .snap files are not detected"); `corpus/knowledge/incremental-pin-disposition.md` has `## 8. Empirical correction and backlink — round 14 (2026-10-20)`.
- Table rows 2, 4 and 5 match the semantics exercised above (supersession keeps raw evidence with both replacements effective; a recorded child override credits only that experiment; one `GIT_DIR` injection is a bounded scrub observation, not hermeticity).

## Findings

None. No statement in this section fails at C**.

## Reader caveats (recorded, not findings)

1. **"before either named round" is loose.** Three rounds are named in the sentence (16, 18, 21) while "either" presupposes two; it is literally true only when read against the two rounds of the immediately preceding clause (18 and 21), read here as the witness-study tool's. A reader who reads "either named round" as covering round 16 would get a false ordering (17 is after 16). Verified fact: 2a22ade (r17) < 58e5d53 (r18) < 370f2df (r21).
2. **The enumeration names first post-round-14 moves, not the movements behind the live digests.** The runner also moved at r26/r30/r51 (latest bytes from 6d8c11e), and the other two at 218bc6b/5b703c6 this round. The sentence is still sound (any one post-round-14 move makes a pin stale), but a reader who tries to reproduce the live digest of the runner from "round 16" will not find it there.
3. **The "Live-tree form" pointer was followed to its outcome and holds.** `## Live-tree re-pin and entry-command monitor — round 17` exists at line 1832, and its recipe/registry name the round-18 manifests, so the pointer resolves. The live entry itself, executed from the lane root at C** (tool bytes unchanged to HEAD), returns the outcome the pointed-at sections claim:

```
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json   → exit 0
  counts {effective 11, expected_checks 12, failed 0, findings 0, passed 11, superseded 1}
  expected_inputs_historical: tools/bash-witness-study.py, tools/mutate-and-run.sh, tools/pin-disposition.py → 4acc607dfd79…
```

  So the three stale pins of this section are absorbed by the round-18 manifest's `historical_inputs` anchors (the round-13 anchor `4acc607` holds the pinned bytes), not by relabelling — consistent with the round-17 table row "Waive only paths that moved". **Measurement caveat:** the same command run inside a non-repo `git archive` extraction exits 2 `historical_input_unavailable` ("root is not inside a git work tree"), because the waivers resolve `<anchor>:<path>` through git. That exit is an artefact of the extraction, not of the live tree, and was discarded rather than scored.
4. **History, not live evidence.** The retained round-14 receipt text records selftest fixtures "kept at /tmp/tameshi-r14-evidence-disposition-selftest…". It is captured stdout inside a frozen receipt, not a scratch directive for a current run; no live /tmp path is presented as current, so it holds (scratch discipline applies to instructions in force, and this section issues none).

## Out of scope

- The round-17 live-tree section, the round-15 registry row and the erratum row named in caveat 3 were read only to check that step 3's pointer resolves; their outcome claims are those sections' business (and are covered by this wave's other seats).
- The ten non-stale inputs were checked only for digest equality at C**, not audited for provenance.
- No product file, tool, corpus file or evidence file was modified by this seat; no git/jj mutation was run; the only writes are the two deliverables.
- The lane changed outside this seat while it ran: uncommitted working-tree edits appeared in `SKILL.md` (two occurrences of the stale self-anchor `SKILL.md:377-378` rewritten to "the `## Restore discipline` section") and in `corpus/knowledge/service-limits.md` (`SKILL.md:1017-1019` rewritten to a section name), and commits `b468854` / `ceb372c` / `e43633c` landed (C***, re-key pass 1b). None of those edits are this seat's; every measurement in this report is against the C** objects named at the top.

## Tooling

No installs or upgrades were needed; `pacman` was not run. Commands used: `git` (read-only: show/log/cat-file/merge-base/archive), `python3` (stdlib only: import of the frozen `sectionize`, sha256, json), coreutils (`diff`, `sha256sum`).

## Artifacts

- .ufo/waves/round-53/w2/T53W2Read01.json
- .ufo/waves/round-53/w2/T53W2Read01.md
