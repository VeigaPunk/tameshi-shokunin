# ReviewFreezeOrder — freeze-before-data order audit (round 34, w1)

Seat: reviewer, leaf member, no subagents. Scope: verify the freeze-before-data order behind
C1's MEASURED TRUE at rev c17e593b, against lane tip 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7.
All work in /fast/scratch/hyaku/tameshi-r34-seats/ReviewFreezeOrder/ (clone `lane`, detached at
tip); the live lane was read-only except this report file. No tooling installed (none needed;
git + sha256sum only). No pacman transaction run (paused per 2026-10-20 ruling).

## Verdict

**FREEZE-BEFORE-DATA ORDER HOLDS — no ordering violation found.** The lineage is strictly
linear `6aaad5b3 → 9dd3174c → c17e593b → 0b99d48e`, with the counter amendment (witness gate)
landed before any sealed held-out byte existed in any ref, the controls receipt attesting the
amended counter minted between them, and the sealed set byte-identical from its introduction
(c17e593b) through the dispatch tip.

## Evidence — exact commands, exit codes, sha256s

Scratch: `S=/fast/scratch/hyaku/tameshi-r34-seats/ReviewFreezeOrder`; every verification command
ran as `cmd; echo $? > S/exit-*` (no `&&`). Exit-code files cited below all contain `0` unless
stated.

### 0. Setup and pin integrity

- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks
  /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/lane` → `exit-clone`=0;
  `git -C $S/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` →
  `exit-checkout`=0; `git -C $S/lane rev-parse HEAD` = 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7.
- Short SHAs resolve (rev-parse): 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a,
  9dd3174c6daaa55ff5bee32878b700ee3bc731b7, c17e593b51802dd4ed568da3265f21c6d00c4273 (matches
  the measurement revision in the deciding receipt), 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7.
- `git show $TIP:tools/tally-audit-v2.py > tool.py` (`exit-tool-extract`=0) → sha256
  **7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10** = pin ✓
- `git show $TIP:tools/mutate-and-run.sh > pristine.sh` (`exit-runner-extract`=0) → sha256
  **a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9** = pin ✓
- Live lane working-tree files hash identically (`sha256sum` on
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/{tally-audit-v2.py,mutate-and-run.sh}) ✓
- Both tools at c17e593b (`git show c17e593b…:tools/… | sha256sum`) hash identically to the
  pins — tool and runner unchanged from measurement revision to dispatch tip ✓

### 1. Amendment 6 (6aaad5b3) is the commit that changed ho_witness_ok

- `git show --stat --oneline 6aaad5b3` → commit "round-34: amendment 6 set-aware witness gate
  (pre-authoring, pre-data) …"; touches `.ufo/evidence/round-33/c1/c1-measure.py` (38 lines).
- Full diff saved (`git show 6aaad5b3 -- .ufo/evidence/round-33/c1/c1-measure.py >
  diff-6aaad5b3.txt`, `exit-diff-extract`=0). Second hunk `@@ -174,17 +182,39 @@ def
  block_run(block, vector, work):` opens on `def ho_witness_ok(ho, pristine, mutated, work)`
  (unchanged context) and rewrites its **body** to the set-aware gate: kill+head requires a
  leg-assignment-line diff with an identical block (`head-leg-assignment` /
  `head-edit-cannot-kill`); accept+head requires identical block (`head-with-block-edit` refusals);
  accept+vector flips to `a == b and mutated != pristine` (`vector-equivalence`); kill+vector
  keeps `a != b` with len-9. Docstring hunk adds: "Adopted BEFORE any sealed held-out authoring;
  no default-mode deciding run had occurred at amendment time."
- Verification trap recorded for future seats: `git log -G ho_witness_ok --oneline $TIP --
  .ufo/evidence/round-33/c1/c1-measure.py` matches **f6d8a89** (round-33 freeze, where the
  function name was introduced) and *not* 6aaad5b3 — because amendment 6 changed only body
  lines that do not contain the literal name. The claim is still true: the diff hunk is
  anchored at the ho_witness_ok definition. Pickaxe on the function name alone under-reports.
- `git merge-base --is-ancestor f6d8a891f1d966c5c3cdda385090da3a6e804675 6aaad5b3` →
  `exit-anc-f6d8a89`=0 (the round-33 freeze introducing ho_witness_ok precedes amendment 6).
- Counter bytes: `git show 6aaad5b3:c1-measure.py | sha256sum` =
  **f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c**, identical at tip —
  full match to the elided pin `f6b8868c…a07f28c`; counter unchanged from amendment to tip.

### 2. NO sealed held-out JSON exists at or before 6aaad5b3

- `git ls-tree 6aaad5b3 -- .ufo/evidence/round-33/heldout` → empty output (`exit-lstree-6aaad5b3`=0).
- `git log --oneline 6aaad5b3 -- .ufo/evidence/round-33/heldout` → empty (no ancestor of the
  amendment ever touched the path).
- Stronger: `git log --oneline --all -- .ufo/evidence/round-33/heldout` (all refs in the clone,
  incl. master a5b1936 and origin branches) → exactly one commit, **c17e593**.
- `git log --oneline --diff-filter=A $TIP -- …/heldout` → only c17e593 ("sealed held-out set
  authored after the amendment-6 counter freeze (8 must-kill + 6 must-accept …)").

### 3. Named commits are ancestors of the tip; linear chain

- `git merge-base --is-ancestor <c> $TIP; echo $?` → 6aaad5b3: 0; 9dd3174c: 0; c17e593b: 0;
  tip self-check: 0 (`exit-anc-*` files).
- `git rev-list --parents -n 12 $TIP` gives the strict chain 0b99d48e→c17e593b→9dd3174c→
  6aaad5b3→3fc1b2fe…; `git rev-list --count 6aaad5b3^..$TIP` = **4**; `git log --oneline
  6aaad5b3^..$TIP` = exactly amendment-6 → controls-receipt → sealed-set → deciding-receipt.

### 4. Controls receipt: 9dd3174c == working tree at c17e593b

- `git show 9dd3174c:.ufo/evidence/round-33/c1/controls-receipt.json | sha256sum` =
  **f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa**
- `git show c17e593b:…/controls-receipt.json | sha256sum` = same ✓
- Also identical at tip and in the live lane working tree (same sha) ✓
- At 6aaad5b3 the file does not exist: `git show 6aaad5b3:…/controls-receipt.json` →
  `fatal: path … exists on disk, but not in '6aaad5b3…'` (the e3b0c442… sha in that pipeline is
  sha256 of empty stdin, artifact of the failed feed). Receipt first committed at 9dd3174c,
  one commit after the amendment — consistent with "minted at the amended rev".
- Receipt content (live lane file, sha f1e62421…): `all_false: true`; four controls
  CtlDoNothing / CtlAlwaysPass / CtlAlwaysFail / CtlShaOnly all `predicate_pass: false`;
  `counter_sha256` = f6b8868c…a07f28c (the amended counter — attests the mint rev);
  `runner_sha256` = a7d3f2dd… (pinned runner).

### 5. Sealed set: sealed at c17e593b, byte-frozen through tip

- `git ls-tree -r c17e593b… -- .ufo/evidence/round-33/heldout` → exactly 14 files: 8
  `ho-kill-*` (head-extra-assign, head-nonbare, vector-arm-swap, vector-count-field-swap,
  vector-fail-exit-swap, vector-fail-threshold, vector-setup-arm-skip, vector-setup-threshold)
  + 6 `ho-accept-*` (head-comment, head-version-rename, vector-arith-space,
  vector-block-comment, vector-inert-line, vector-tail-comment). Matches 8 must-kill + 6
  must-accept.
- `git ls-tree -r $TIP -- …/heldout` → identical 14 blob SHAs (73850e11, c1beb64e, 58c87459,
  566e09df, 7e1a59aa, badf4830, e9ff0540, bd3dfbb0, dc57eae6, 2bea66f1, e9a272eb, 55cab922,
  e1aa4bd9, 248e463f) — sealed set byte-identical c17e593b → tip.
- `git diff --stat c17e593b 0b99d48e -- .ufo/evidence/round-33/heldout` → empty.

## Findings by severity

- **Blocking / Major / Minor: none.** No ordering violation. Every checkable component of the
  freeze-before-data claim verified against the tip clone; nothing landed wrong.
- **Advisory (dispatch wording, not a lane defect):** the assignment says "the four
  heldout-free commits 6aaad5b3, 9dd3174c, c17e593b" — it names three. Tree-level facts: the
  range 6aaad5b3^..tip contains exactly 4 commits (the named three + tip), of which only
  6aaad5b3 and 9dd3174c are heldout-*free*; c17e593b and tip each contain the 14-file sealed
  set, by design (data sealed AT c17e593b, consumed by the deciding run whose receipt reports
  `heldout_after_freeze=1`). The checkable intent (ancestry of the three named commits) holds.
- **Advisory (method):** `git log -G ho_witness_ok` does not surface 6aaad5b3 (changed body
  lines lack the literal); verification of "amendment 6 changed ho_witness_ok" must read the
  diff hunk, as done here. Anyone re-auditing with pickaxe alone would wrongly conclude the
  amendment didn't touch the gate.

## Residual risk and verification gaps

- Trust anchor is the local clone of the lane repo; no GPG/tag signature verification was
  possible or attempted (no signed refs observed). Byte pins verified against clone blobs and
  the live working tree, which agreed on all four artifacts (tool, runner, counter, receipt).
- Heldout JSON *filenames* and blob stability verified; the JSON contents (witness kind/set
  fields inside each copy) were not semantically audited — out of this seat's scope (other
  seats own content: ReceiptChain, CounterSemantics).
- The deciding run itself was not re-executed (kill rule consumed; counter only importable in
  scratch — not needed for ordering claims). The deciding receipt's PASS line is taken as the
  claim under attack; this seat verified only the freeze-order preconditions, all of which hold.
