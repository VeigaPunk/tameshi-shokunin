# Round-35 W2 — ScribeTrio metadata audit

Axes: source resolution, `verified-at` truth/reproducibility, and executable `recheck` instructions.

## Result

Audited the three entries changed at the round-35 freeze—`corpus/knowledge/witness-equivalence-rule.md`, `survivor-fixture-minimization.md`, and `closeout-r11.md`—plus the pre-existing related entry `runner-tally-audit-v2.md`. All source IDs resolve to rows in `corpus/SOURCES.md`, and every cited local source/evidence path exists at pin `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. No source-reference false positive found.

Every audited `recheck:` field is a cadence or a prose action, not an executable command. The prior tally note also has a stale/ambiguous `verified-at` pointer: its cited round-33 receipt is explicitly a not-run result, while the eventual C1_R33 deciding receipt is in round 34. The note's own body correctly records the round-33 honest stop. No runner, counter, selftest, build, or measurement command was executed in this audit.

## Findings (ranked)

### CRITICAL — prior tally-note verification pointer is false if read literally

Exact text, `corpus/knowledge/runner-tally-audit-v2.md:4`:

> verified-at: round-33 measurement revision (see SCORECARD.md round-33 row; counter receipts .ufo/evidence/round-33/after/)

At pin `7da...`, `SCORECARD.md:1622` says the C1 measurement was **NOT RUN** at the round-33 revision. Its cited `round-33/after/c1-at-head-notrun.stdout` says `controls_ok=0(receipt-missing)`, `v1_kill=0/0`, `ho_kill=0/0`, and `C1_R33_PASS=false`. The note itself says at lines 66–68: “Not measured this round (round 33 honest stop).” Thus the literal reading that the round-33 run measured/verified C1 is false. This does **not** falsify the later C1_R33 result: the deciding run was recorded at `c17e593b51802dd4ed568da3265f21c6d00c4273` in the round-34 receipt, `C1_R33_PASS=true`. The metadata needs to distinguish those events and point to the correct receipt.

**Report-only replacement:**

```text
verified-at: 2026-10-23 — round 33 C1 was not measured at that revision (SCORECARD.md:1622; .ufo/evidence/round-33/after/c1-at-head-notrun.stdout). The later C1_R33 deciding run is at c17e593b51802dd4ed568da3265f21c6d00c4273 (.ufo/evidence/round-34/measure/c1-deciding-run.stdout). The round-32 predecessor result remains .ufo/evidence/round-32/after/c1v2-at-measurement.stdout.
```

### HYGIENE — none of the four `recheck:` fields names a command

The exact source clauses are:

- `witness-equivalence-rule.md:5`: “recheck: on-counter-change — re-read `ho_witness_ok` in `.ufo/evidence/round-33/c1/c1-measure.py` and re-open S097/S101; drift if the branch set (kill/accept × head/vector) or its semantics change”
- `survivor-fixture-minimization.md:5`: “recheck: 90d — re-open S024 and re-hash the snapshot (`.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html`); drift if the snapshot is missing, the digest moves, or the F6 row in `corpus/README.md` `## Frontier` changes status”
- `closeout-r11.md:5`: “recheck: 90d — re-read `plans/round-11.plan.md:13-25` and the round-11 row of `SCORECARD.md`; drift if either path moves or the arc is re-opened by a later round”
- `runner-tally-audit-v2.md:5`: “recheck: on-runner-change (the audited surface is pinned at sha256 a7d3f2dd...2eb9; any runner edit re-opens every class)” 

**Report-only replacement drafts:**

Witness:
```text
recheck: on-counter-change — `python3 .ufo/evidence/round-33/c1/c1-measure.py --lane CLONE --rev REV --work EMPTY_DIR`; inspect `ho_witness_ok` at that revision and re-open S097/S101. Drift if the kill/accept × head/vector branches or semantics change. The cited counter CLI defines `--lane`, `--rev`, and `--work` (c1-measure.py:332-340).
```

Survivor:
```text
recheck: 90d — `sha256sum .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html`; `git -C "$LANE" show "$REV:corpus/README.md"`; `git -C "$LANE" show "$REV:.ufo/waves/round-29/w1/BuildF6B.md"`. Drift if the digest, F6 status, or retained receipt changes; this is a record check, not a new measurement.
```

Closeout:
```text
recheck: 90d — `git -C "$LANE" cat-file -e "$REV:plans/round-11.plan.md"`; `git -C "$LANE" cat-file -e "$REV:SCORECARD.md"`; `git -C "$LANE" cat-file -e "$REV:LOG.md"`; inspect later round plans with `git -C "$LANE" log --format=%H "$REV..$NEXT_REV" -- 'plans/round-*.plan.md'`. Drift if an anchor disappears or a later plan re-opens the arc.
```

Prior tally note:
```text
recheck: on-runner-change — `python3 tools/tally-audit-v2.py --runner tools/mutate-and-run.sh`; `python3 tools/tally-audit-v2.py --selftest`. Retain full stdout and exit codes and compare the runner digest with the stated pin.
```
Both invocations are listed by the tool's CLI documentation (`tools/tally-audit-v2.py:4-9`).

### BOUND — the new `verified-at` statements are documentary reviews, not retained executions

- `witness-equivalence-rule.md:4` says round 35 “re-read this entry against that landed gate and found no statement the code contradicts.” The counter pin is reproducible, and `ho_witness_ok` is at lines 184–218, but the conclusion is a manual review with no round-35 review receipt or executable test identified. No contrary code statement was found in the reviewed function; do not treat the wording as an automated verification result.
- `survivor-fixture-minimization.md:4` explicitly says “(no re-measurement).” Its objective archival claims check out: the snapshot digest matches, the retained BuildF6B report records the honest stop, and F6 remains open. It is not fresh behavioral evidence.
- `closeout-r11.md:4` is a repeatable record review, not a runtime measurement. The cited plan, scorecard, and log exist at the pin; a history diff confirms the 2026-10-14 body was not rewritten (only the metadata header was added).

**Report-only replacement drafts:**

Witness `verified-at`:
```text
verified-at: 2026-10-23 — static review only, against counter blob SHA-256 f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c (ho_witness_ok, lines 184–218); no round-35 behavioral remeasurement is claimed.
```

Survivor `verified-at`:
```text
verified-at: 2026-10-23 — archival check at REV=7da6e076c2e25936a3b60dde2a4080d8f05b7e5b: S024 snapshot SHA-256 3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99; F6 remains open in corpus/README.md; BuildF6B records the honest stop. No remeasurement.
```

Closeout `verified-at`:
```text
verified-at: 2026-10-23 — at REV=7da6e076c2e25936a3b60dde2a4080d8f05b7e5b, the cited plan, SCORECARD.md, and LOG.md are present; diff from the 2026-10-14 landing 284ab0f0b8b989ee73d9c00c0c0df0a59757af8d shows only this metadata header added and no closeout-body changes.
```

## Per-entry source resolution and supporting bytes

All four `source:` fields pass the stated existence test.

| Entry | Source resolution / verification |
|---|---|
| `witness-equivalence-rule.md:3` | S097 and S101 exist at `SOURCES.md:106,109`. S101's cited local snapshot exists and hashes to `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420`. |
| `survivor-fixture-minimization.md:3` | S024 exists at `SOURCES.md:35`; its local snapshot hashes to `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99`, matching the documented abbreviated digest. BuildF6B report SHA-256 is `3c9d44ad791f2effb5b365938878e8455b1e1f03b4cc3bc7ecdc4ad08aa35bf8`; README F6 row remains `open`. |
| `closeout-r11.md:3` | All three own-work anchors exist at pin: `plans/round-11.plan.md` SHA-256 `068578f198367b79b14fea95d9db550828908e345e5cbc161cabf0e4bea744f7`; `SCORECARD.md` `cbea24c85074baac8904cab3b2937c6e93634431c9ee408b711fc58e66e7961f`; `LOG.md` `34ec26b76ee2fa00cbb6ade6b5a6cbd64137dc77aa36196659abb90a1ccaaacb`. The cited plan lines 13–25, round-11 scorecard row, and LOG rows 303–310 resolve. |
| `runner-tally-audit-v2.md:3` | S097/S099 exist at `SOURCES.md:106-107`. Its own-work glob resolves to 22 committed JSON files under `.ufo/evidence/round-32/heldout/`. |

The `SOURCES.md` blob at the target pin is SHA-256 `f85c02e76b0994477df7ded8d95585d260885f2d93fbeb91e57deb358d7855fe`. The target blobs for the four entries are: witness `84a42f945e2016e5fd8e01869fbf2c7dc53b5c9961a20ed9636bce863154cbb1`; survivor `116b56236bc468c84da4a3d2d97aa4e8cd84de2ca396ab202dfa1fd835802a86`; closeout `f0894bf65aee32d81fde3f9233b8f35968e200bc7906d0035a786d3df94d1fd7`; prior tally v2 `83b410793279b6cb2843f1fcb9dd135da12ca6e5bd20ef26a05eab183539d5ac`.

## Commands and evidence provenance

The scratch lane was already present but at `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`, not the requested `7da...`; its object database could not resolve `7da` (`git cat-file -e` exit 128). I did not mutate Git or checkout state. The target commit exists in the read-only main repository object database (`git cat-file -e` exit 0); pin-specific blob hashes and the listed read-only comparisons below were therefore obtained there. The main repository's current HEAD was `1fc6cb7f764e150b038e132590b7f23250254fe7`; `git status --short` showed an unrelated `?? corpus/lessons/round-35.md`, left untouched.

Commands actually run (all reads only):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/ScribeTrio/lane rev-parse HEAD
# d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc; exit 0

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/ScribeTrio/lane cat-file -e 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b^{commit}
# fatal: Not a valid object name; exit 128

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b^{commit}
# exit 0

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format= --name-status d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc -- corpus/knowledge
# M closeout-r11.md; M survivor-fixture-minimization.md; M witness-equivalence-rule.md; exit 0

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --exit-code d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b -- corpus/knowledge/witness-equivalence-rule.md corpus/knowledge/survivor-fixture-minimization.md corpus/knowledge/closeout-r11.md corpus/SOURCES.md corpus/README.md plans/round-11.plan.md SCORECARD.md LOG.md
# no output; exit 0 (these blobs are unchanged between the scratch lane tip and target pin)

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b -- .ufo/evidence/round-32/heldout
# 22 committed JSON paths; exit 0

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-33/after/c1-at-head-notrun.stdout | sha256sum
# 51438fe51b44816c24ff47d6916eb2ef6150b42b36c95748ba232af1271e9467; pipeline exit 0

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-34/measure/c1-deciding-run.stdout | sha256sum
# 3e28149f94f2e5d832e680285306f0166029858982cfc5ae32bd4f19c9a9b05c; pipeline exit 0

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-32/after/c1v2-at-measurement.stdout | sha256sum
# 6f4f10820337ab3bf86e7e079f8e576ef90d9b61fedc3620064241c07e73b559; pipeline exit 0
```

Closeout provenance was checked with `git log 7da... --follow --format='%H %cs %s' -- corpus/knowledge/closeout-r11.md` (exit 0; history identifies landing `284ab0f...` and the metadata-add commit `d16f9b5...`) and `git diff --unified=0 284ab0f... 7da... -- corpus/knowledge/closeout-r11.md` (exit 0; output contains only the added metadata header and blank line, not body changes).

Target-pinned supporting hashes: round-33 counter `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`; round-32 C1 result `6f4f10820337ab3bf86e7e079f8e576ef90d9b61fedc3620064241c07e73b559`; round-34 C1_R33 result `3e28149f94f2e5d832e680285306f0166029858982cfc5ae32bd4f19c9a9b05c`.

## Touched surfaces, limits, and out of scope

- **Created:** only this report at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ScribeTrio.md`.
- **Read-only:** the four metadata entries, `SOURCES.md`, `README.md`, `SCORECARD.md`, `LOG.md`, `plans/round-11.plan.md`, and their cited receipts/snapshots at the stated pin.
- No product code, counter, runner, source registry, reports, or other files changed. No tools installed or updated; no checks or runtime commands executed. No report draft was written back into the audited entries.
- This is a metadata/provenance audit only. It does not remeasure C1/C2, re-run the note's historical commands, or claim a fresh behavioral result. The precise-pin scratch checkout was unavailable; pin-specific facts were read from the main repository's immutable Git object store without modifying either checkout.
