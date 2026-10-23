# CriticV2 — counter v2 adversarial review

**Verdict: v2 improves isolation, but the held-out minimum does not establish shortcut resistance. Amendment 2 changes an operative predicate constant after real-tool data; my advisory reading of addendum §9 is that it cannot count as the unchanged frozen claim. A separate validity defect permits the same runner bytes to qualify for opposite labels.** These are findings for the canonical Rust judge, not an admission or shipment decision.

Seat: `CriticV2`. Axes: **operability** is the assigned changed surface; **calibration** is the guardrail against attributing a stronger capability or cleaner measurement provenance than the evidence supports. No other axis improvement is claimed. Capability acquisition is the claim type, not another axis (`AXES.md:13-16,40-41,57-64`).

Paths below are relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless explicitly absolute. Citation shorthand: `v2/` means `.ufo/evidence/round-32/v2/`; bare amendment filenames are in that directory; bare `c1-measure.py`, `contract.json` and `w2-items.json` are in `.ufo/evidence/round-32/`; `w1/` means `.ufo/waves/round-32/w1/`; `AXES.md` means `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md`. Review was read-only except this requested report. Static counterexamples below are labeled **[INFERENCE]** and were not executed. I did not run either counter, the tool, a selftest, or a regression.

## 1. Which cheap shortcut could still meet v2?

**Verdict: no replacement shortcut can literally satisfy the current full predicate without satisfying its exact tool digest. That identity gate is not evidence that the behavioral test rejects shortcuts. An embedded public-accept recognizer plus a shallow held-out rule remains a counterexample to the design's claimed discrimination. No passing v2 shortcut run is asserted here.**

### Identity versus work

- `v2/c1-measure-v2.py:66,357-358,394-396` pins one particular tool digest and requires `tool_sha_ok`. Any different control fails that conjunct even if every COPY outcome is right. Amendment 1 explicitly includes this identity in the predicate (`contract-amendment-1.json:10,14,21`). Consequently, “all controls print false” is insufficient: a meaningful control receipt must also show its **behavioral** misses separately from the expected identity mismatch.
- The current tool is not being accused of being an allowlist. Its `audit()` actually calls `check_static`, `check_runtime` and `check_harness` (`tools/tally-audit.py:357-377`). That source evidence is distinct from what the counter's finite classifications establish.
- The public accept grammar remains small: six frozen constructors and generated operand-permutation/nonce constructors (`c1-measure.py:140-168`). Wave 1 already contains an observed allowlist success on that public component: `w1/CriticC1.md:46-73,86-104`. Moving the constructors into the tool would remove the runtime counter-read dependency without introducing an oracle or harness.

**[INFERENCE: concrete behavioral shortcut.]** Precompute that public accept grammar; for other inputs, normalize only comments and a small set of equivalent arithmetic/quoting changes, compare against an embedded pristine reference, and reject everything else. This performs no tally execution or fault injection. It handles a permitted easy population containing six benign variants in that normalization grammar and six copies of one obvious fault outside it. The counter counts files, not distinct mechanisms (`v2/c1-measure-v2.py:343-356,394-396`). Even identical bodies under different JSON paths count separately; there is no body-digest uniqueness or author-independence check.

A particularly simple mechanically valid population is six distinct inert-comment accept copies and six comment-distinguished copies that classify status 4 as PASS. For the latter, vector `[4,0,0,0,0,0,0,0,0]` distinguishes the pinned SETUP from the mutant PASS (`tools/mutate-and-run.sh:1434-1451`). Repetition of v1 shapes would violate the authors' separate instruction to create genuinely new shapes (`w2-items.json:8,16,24,32,40,48,56,64`), so this is a counterexample to **the enforced minimum**, not an allegation that the actual seats submitted such a set. Novel but shallow equivalent spellings can likewise satisfy that instruction without supplying a lower bound on adversarial difficulty.

### Side channels

| Candidate shortcut | Evidence and assessment |
|---|---|
| Read counter, Git history, sibling copies, filename labels | Substantially closed by the per-copy mount boundary and fixed `/in/runner.sh` path (`v2/c1-measure-v2.py:257-264`). The old counter-reading control is not directly portable. |
| Creation order or mtime | Amendment 2 shuffles writes, sets mtime to zero and shuffles execution (`:359-379,382-385`). Sorting the reporting list at `:375` does not undo the separate execution shuffle. I found no demonstrated deterministic timing/inode label rule remaining. ctime/inodes are not normalized, but their mere visibility is not proof of a label correlation after shuffled creation. |
| File size or content markers | Still visible: the original bodies are bound into the sandbox, with no label-neutral pairing or padding. A public-v1 allowlist plus a size cutoff, or a comment marker used only in benign held-outs, can classify a correspondingly correlated held-out population without auditing. **[INFERENCE]** This is possible, not an observed correlation in the actual returned set. JSON `set`, `author` and `rationale` are not directly mounted; leakage would have to be in body bytes or metadata. |
| Pure timing guess | Execution is randomized; no successful attack is established. Avoid promoting an untested possibility into a demonstrated bypass. |

**Smallest safe correction:** retain the digest as treatment provenance, but assess negative controls by their per-copy behavioral results rather than the inevitable digest failure. For a future freeze, require label-neutral, structurally matched accept/kill pairs and an embedded-allowlist control with its cheap fallback rules. Do not describe sandboxing alone as defeating embedded answers.

## 2. Is amendment 2 a post-data rule change or a pre-data object fix?

**Verdict: both descriptions have a defensible engineering meaning, but under the binding freeze language my advisory ruling is a post-data predicate change. It may be a useful development repair; it is not the same frozen claim.**

### Strongest argument for a pre-data development fix

Amendment 1 had already replaced the v1 measurement design. Amendment 2 discloses that no full v2 run on the real tool preceded it, that the decisive held-outs would be written only afterward, and that the first full v2 run still decides without reseeding (`contract-amendment-2.json:7-13`; amendment 1 `:33-35`). Public v1 fixtures are development inputs, not concealed test data. The newly added position-only faults repair a genuine harness-panel weakness, and shuffled copy creation is a useful hardening rather than a relaxed threshold. On this prospective, fresh-held-out interpretation, development stopped before that new population existed.

### Strongest argument against

1. The rule says **“after any seat has scored”**, not “after the L1 runs the latest full counter” (fleet `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-32.md:352-360`). The original contract is stricter still about amendments after controls (`contract.json:6,31`). Even granting amendment 1 as the addendum's permitted pre-data control redesign, amendment 2 follows actual treatment-tool results, not merely a failing cheap control.
2. DeterminismProbe records v1 failures for the very digest pinned by amendment 1, `158202f8…a356a`, at seeds `00ff` and `0900` (`w1/DeterminismProbe.md:203-219`). These are prior-seat observations, not runs I repeated. Amendment 2 expressly acknowledges both those observations and subsequent development sweeps (`contract-amendment-2.json:6-11`). Its retained development receipt says `DEVSWEEP bodies=688 kill=282 accept=406 misses=0` (`v2/dev/devsweep-200.stdout:1`); the script reads the working tool directly (`devsweep.py:2-3,18-24`), rather than certifying a revision-bound final measurement.
3. `TOOL_SHA256` is an operative predicate constant. Replacing `158202f8…a356a` with `9639c458…99ef` changes which revisions can pass. Keeping the symbolic sentence and label unchanged does not keep its denotation unchanged. Amendment 1 also explicitly said the tool could not change afterward (`:14`). Amendment 2 candidly calls this a changed pinned identity after data on the shared v1 subset (`:11`).
4. The v1 subset is still mandatory in v2 (`v2/c1-measure-v2.py:315-316,394-396`). Its outcomes cannot be treated as unrelated evidence solely because the wrapper's version number changed. An out-of-assignment run still produces observed data; its assignment error does not erase its information.

**Ruling and correction:** preserve the original rule and all observed failures; identify the repaired tool and v2 experiment as a separately frozen prospective/supplemental result, subject to the canonical judge's procedural ruling. Do not silently treat amendment 2 as having left C1's predicate unchanged. There is no documentation edit or later passing attack panel that retroactively makes that chronology pre-data.

**Related enforcement gap:** `adding_commit()` returns the counter's initial adding commit (`v2/c1-measure-v2.py:278-281,326-335`), not the amendment-2 tool freeze. **[INFERENCE]** A held-out file added between amendment 1 and amendment 2 would satisfy `after`, even though it predates the current tool freeze. The actual dispatch directs authors to work after amendment 2; I do not allege that this happened. A newly frozen protocol should bind ancestry to the exact effective tool-freeze commit and preserve held-out content identity, not merely a path's first appearance.

## 3. Does the 6+6 minimum exclude do-nothing and shortcuts?

**Verdict: do-nothing is excluded, but not by the held-out minimum; nontrivial shortcut resistance is not established by that minimum. Worse, the acceptance validator admits a concrete contradictory-label population.**

No tool fails presence/digest and produces OTHER; always-PASS fails the required kill copies; always-FAIL fails the public accept copies. This follows before adding any held-out requirement (`v2/c1-measure-v2.py:268-273,357-358,380-396`). The old do-nothing observation is recorded at `w1/CtlDoNothing.md:5,48-77`; it was not rerun here.

The actual white-box adversarial assignments are stronger than an arbitrary dozen files: eight seats cover different surfaces, are told to seek tool failures, must avoid v1 families, and report validity plus tool outcomes (`w2-items.json:8,16,24,32,40,48,56,64`). Seeing and probing the tool can help falsification; it is not itself misconduct or automatically invalid evidence. L1's duty to retain every returned file is also valuable (`contract-amendment-1.json:27-29`). Nevertheless:

- The executable checks do not enforce semantic diversity, unique bodies, independent authors, or exhaustion of attempted shapes.
- Authors choose what to return after probing; retaining everything returned does not retain every attempted candidate.
- Fixed anchors restrict accepted refactors before the tool is assessed (`v2/c1-measure-v2.py:70-74,87-106,141-148`). Parser-invalid hard examples are excluded, not evidence of successful general auditing. Passing this population cannot establish broader refactor support.

### Strongest static counterexample: the same body is both valid accept and valid kill

**[INFERENCE: source-derived, not an executed receipt.]** Starting from the pinned runner, replace the unique tally start:

```text
  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n
```

with that exact line followed by:

```bash
  if [[ $st_js == 1 && $st_citecheck == 1 ]]; then exit 0; fi
```

Leave everything else unchanged. Submit one JSON as `set: accept`, and another with identical edits as `set: kill`, witness vector `[1,0,0,0,0,0,0,0,1]`. A permitted vector-only held-out population needs no block witnesses.

The static checks are decisive:

1. Both fixed anchors, every leg assignment and the loop operands remain intact. The inserted Bash conditional is syntactically ordinary and the body differs from pristine.
2. Every acceptance sweep has at most one nonzero leg (`v2/c1-measure-v2.py:185-192`); every stress vector is all zero (`:245-248`). The new condition is false on all of them.
3. The harness section is unchanged, and validation replaces its extracted tally with the injected reference/fault block (`:141-153,249-251`). It therefore does not test this new condition as the candidate's tally during harness equivalence checking.
4. On the kill witness both selected legs equal 1, so the candidate returns 0 with no tally line. The pinned tally instead returns 1 and `REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)` (`tools/mutate-and-run.sh:1441-1445`). Thus the kill validator's required difference holds (`v2/c1-measure-v2.py:217-230`).
5. There is no cross-label body-conflict check. These identical bytes can be demanded to produce both ACCEPT and KILL. A deterministic semantic auditor cannot satisfy both. More directly, the real tool's existing runtime vector for the first/last legs with statuses `(1,1)` detects the real defect and rejects the nominal accept (`tools/tally-audit.py:229-241`). That rejection would be correct auditing, not evidence that it lacks the claimed capability.

This is not a Python/prose mismatch: the published acceptance validity rule itself omits mixed-status vectors (`v2/c1-measure-v2.py:34-37`). It is an unsound labeling rule relative to the claimed operation. It also shows why “a valid held-out defeats the tool” needs semantic interpretation, not automatic credit.

**Smallest future correction for this counterexample:** test accepts against the tool's existing mixed-status vectors and every submitted kill vector/stress witness, and detect cross-label body-digest conflicts. Do not retroactively relabel or drop a returned file to rescue the current frozen result.

## 4. Smallest response to the strongest objection

**Verdict: preserve the present experiment honestly; do not issue a third rule repair to make the current claim pass.** The procedural defect cannot be repaired retrospectively. The labeling and control-design defects are fixable prospectively.

For the current report, distinguish (a) original frozen rule and observed data, (b) amended prospective experiment, (c) exact fixed tool identity, and (d) finite behavioral outcomes. Report a first-run miss unchanged. No full v2 result was produced by this review.

For the next properly frozen measurement, the smallest defensible package is: correct the demonstrated accept/kill conflict; commit a label-neutral paired held-out manifest before outcome-based selection; count distinct semantic challenges rather than paths; and require the embedded public-allowlist plus cheap-fallback control to miss behaviorally, separately from its identity gate. Record the real effective freeze commit. This answers the exhibited objections without claiming finite tests prove a universal auditor.

## Evidence commands and observed output

The following read-only commands ran from `/fast/scratch/hyaku/tameshi-r32-seats/CriticV2/`. No code under review was executed.

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/v2/c1-measure-v2.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/v2/contract-amendment-1.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/v2/contract-amendment-2.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
```

Observed exit 0, in the same order:

```text
1ab9e9cf8e408f6230110ac42495da2b9c3f51236fe3a32754bd23524f7f7c94  c1-measure-v2.py
dd8aff54b9e29e3056fe68ad485d47c88bb5c52c5630f56fc142147c84037a91  contract-amendment-1.json
1c22df5447a376089c90bf0398164674afe205de782b458e7e8f4774f86dd763  contract-amendment-2.json
9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef  tools/tally-audit.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh
```

Basenames above abbreviate the absolute paths printed by `sha256sum`; digests are verbatim.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%H %P %s' --max-count=6 528f8deec8d6473006727aff629caf1800ff67fd -- .ufo/evidence/round-32/v2/c1-measure-v2.py .ufo/evidence/round-32/v2/contract-amendment-1.json .ufo/evidence/round-32/v2/contract-amendment-2.json tools/tally-audit.py
```

Observed exit 0:

```text
528f8deec8d6473006727aff629caf1800ff67fd b50a18f009df3a7a3899839621992784563395b2 round-32: amendment 2 before any v2 run — tool re-frozen (sha 9639c458: position-only harness faults after DeterminismProbe), counter copy-order side channel closed, dev sweep receipts
b50a18f009df3a7a3899839621992784563395b2 e9f3b9571985543196b51082ba6dc257b32ffb8b round-32: C1 re-designed before data (v1 met by CriticC1 allowlist) — counter v2 (sandbox, tool freeze, sealed held-out set) + amendment 1; tools/tally-audit.py frozen (sha 158202f8)
```

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --no-ext-diff --unified=2 b50a18f009df3a7a3899839621992784563395b2 528f8deec8d6473006727aff629caf1800ff67fd -- .ufo/evidence/round-32/v2/c1-measure-v2.py tools/tally-audit.py
```

Observed exit 0. The diff changes the operative tool hash from `158202f8…a356a` to `9639c458…99ef`, adds seed validation and shuffled/mtime-normalized copy creation, and adds the position-only fault loop plus two tool selftest cases. Complete raw tool output: `artifact://36113`. No unshown outcome is inferred from commit-message wording.

Prior-seat execution evidence was read only from the lane's wave-1 reports; no other seat's scratch directory was opened. No exhaustive independent audit of the assertion “no earlier real-tool v2 run anywhere” was performed; the ruling above holds even taking that disclosure as true. Only this report was written in the lane. No production tool, Git index, or fleet state was written. No tools were installed or upgraded. All commands started by this seat completed; no process kill, subagent, judge or other orchestration runtime was invoked.

Report: .ufo/waves/round-32/w2/CriticV2.md
