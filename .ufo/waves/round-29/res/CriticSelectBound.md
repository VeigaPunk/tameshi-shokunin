# Verdict: C1 verifies with a disclosed bound

The committed 22-entry selection satisfies the unchanged frozen C1 predicate at both E (`7a45f7b9d6a2542a553276330c8b02ac2e28c7ef`) and the subsequently observed master (`9bb699ad2d9f795dff95df85eb967129c54927d6`). This is a review finding, not round admission or a canonical-judge decision.

The bound must remain explicit: **22 of 32 assembled entries were appended; ten positive entries were excluded for binding defects, and two additional reports were rejected by the assembler for evidence-format defects.** No failing verdict was dropped. Coverage did not rise through selection. Appending all 32 would **fail** the frozen predicate, despite identical 64/64 coverage.

Axes: **calibration** (C1's actual surface), evidence quality/provenance, and the underlying cold-read coverage metric. This selection provides no independent depth or new-surface coverage claim.

## Evidence

All execution was in `/fast/scratch/hyaku/tameshi-r29-critic-select-bound`, never the lane checkout. Runs were wrapped in `timeout 900`; Git environment overrides were unset. Only this requested report was written in the lane. No tools were installed or upgraded; no seats, models, judge, or other agent runtime were invoked.

### 1. Frozen predicate and rule-change attack

Verbatim `.ufo/evidence/round-29/contract-amendment-2.json:20`:

> PASS iff the pinned strict cold-read monitor at REV reports covered == total, restraint == 8 and box3_mismatch == 0 with no override, AND the cold-read ledger at REV keeps the 371 base entries and every non-entry key equal as data (canonical JSON), AND every ledger entry appended after base index 370 is bound to round-29 seat evidence: each of its reports exists at REV under .ufo/waves/round-29/, holds a json block whose seat is one of the entry's seats, whose read_rev equals the entry's read_rev, and whose sections name the entry's start and heading with the entry's verdict, and each of its seats is a member of a committed .ufo/waves/round-29/*/swarm-registry.json at REV.

The quantified population is **entries actually appended**, not every assigned read or every assembler output. There is no frozen requirement to append 32 entries. The kill rule remains a false predicate at landed head (`contract-amendment-2.json:22-24`). Counter implementation: `.ufo/evidence/round-29/c1-measure-v2.py:110-157`, particularly the nonempty reports/seats condition at 132 and final conjunction at 156-157.

The external round prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-29.md:351,357-360` forbids narrowing a landed target and changing a scored rule. Here the integrator changed the candidate ledger, not the counter, its predicate, the 371-entry preservation requirement, or its target. The selector explicitly discloses its post-wave introduction at `.ufo/evidence/round-29/coldread/select-bound.py:12-15`. Thus this is an integration choice the frozen predicate permits, not a replacement rule.

Executed:

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git log --format='%h %s' -- .ufo/evidence/round-29/contract-amendment-2.json .ufo/evidence/round-29/c1-measure-v2.py .ufo/evidence/round-29/coldread/select-bound.py .ufo/evidence/round-29/coldread/c1-dry-all32.txt
```

Observed commits: `09e4f27` freezes C1 v2 before data; `bc2058a` subsequently introduces the wave append/selection evidence. Counter SHA256 independently observed with `timeout 900 sha256sum .ufo/evidence/round-29/c1-measure-v2.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-21/coldread/measure.py`:

```text
2ec2f1a02f73ba10136288abc06197cd73cb388c013db80af3a926959ed70491  .ufo/evidence/round-29/c1-measure-v2.py
7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37  .ufo/evidence/round-18/measure.py
657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb  .ufo/evidence/round-21/coldread/measure.py
```

These match the frozen amendment's pins at lines 14-17.

### 2. No failing verdict was excluded; coverage was not increased

Executed in the clone:

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 .ufo/evidence/round-29/coldread/select-bound.py --assembled .ufo/evidence/round-29/coldread/assembled-w1.json --out /fast/scratch/hyaku/tameshi-r29-critic-select-bound-review-bound.json --receipt /fast/scratch/hyaku/tameshi-r29-critic-select-bound-review-receipt.json
```

Observed:

```text
{"assembled": 32, "kept": 22, "excluded": 10, "excluded_verdicts": ["gap-minor", "verified-record"]}
kept sections: [131, 375, 1380, 1479, 1517, 1548, 1563, 1609, 1814, 1925, 1938, 1964]
```

Executed comparison:

```sh
timeout 900 cmp /fast/scratch/hyaku/tameshi-r29-critic-select-bound-review-bound.json .ufo/evidence/round-29/coldread/assembled-w1-bound.json && timeout 900 cmp /fast/scratch/hyaku/tameshi-r29-critic-select-bound-review-receipt.json .ufo/evidence/round-29/coldread/select-receipt-w1.json && printf 'selector output and receipt byte-identical\n'
```

Observed: `selector output and receipt byte-identical` (exit 0).

Executed independent data count:

```sh
timeout 900 jq -n --slurpfile a .ufo/evidence/round-29/coldread/assembled-w1.json --slurpfile b .ufo/evidence/round-29/coldread/assembled-w1-bound.json --slurpfile r .ufo/evidence/round-29/coldread/select-receipt-w1.json '{assembled:($a[0].entries|length),kept:($b[0].entries|length),dropped:($r[0].excluded_entries|length),dropped_verdict_counts:($r[0].excluded_entries|group_by(.verdict)|map({verdict:.[0].verdict,count:length})),assembled_veto_failures:([$a[0].entries[]|select((.verdict=="gap-blocking") or (.verdict=="wrong-expectation") or (.verdict=="not-executed") or (.blocking_gaps!=0) or (.wrong_expectations!=0))]|length),all_reports_nonempty:all($a[0].entries[]; (.reports|length)>0),same_section_starts:(($a[0].entries|map(.start)|unique)==($b[0].entries|map(.start)|unique))}'
```

Observed: `assembled=32`, `kept=22`, `dropped=10`; excluded verdict counts `gap-minor=7`, `verified-record=3`; `assembled_veto_failures=0`, `all_reports_nonempty=true`, `same_section_starts=true`.

Receipt anchors: `.ufo/evidence/round-29/coldread/select-receipt-w1.json:6-233` enumerates every exclusion; lines 234-250 give the positive verdicts and retained 12 starts. Seven exclusions have normalized/merged verdicts differing from a source report; four have full agent IDs instead of registry-member seat names; one entry has both defects. These are not ten negative cold reads.

Why positive-only exclusion cannot raise coverage here: `.ufo/evidence/round-18/measure.py:459-474` makes failing verdicts or nonzero blocking/wrong-expectation counts veto-eligible. Lines 627-641 compute coverage as `credited > 0 and not vetoes`. None of these 32 entries is veto-eligible; removing positive entries cannot create credit or remove a veto. Both independent actual measurements below also show coverage unchanged at 64/64. This conclusion is about these bytes, not permission to discard future negative reads.

### 3. Strongest counterexample: all 32 entries fail binding

Existing evidence `.ufo/evidence/round-29/coldread/c1-dry-all32.txt:1-8` reports the all-32 sandbox at `15031e4f79be6730c593edfe7b3be9746914b317`:

```text
C1_R29_V2: covered=64/64 restraint=8 box3_mismatch=0 appended=32 bound=22 prefix_equal=1 rev=15031e4f79be6730c593edfe7b3be9746914b317
PREDICATE: C1_R29_V2_PASS=false
```

I independently rebuilt this counterexample from E, using E's committed reports/registry/traces. In my clone only, the ledger was replaced with the stdout of the executed `timeout 900 git -C /fast/scratch/hyaku/tameshi-r29-critic-select-bound show 367ec0f1d79cb9b67d724f2962e7554a0841b1fc:.ufo/evidence/round-21/coldread/ledger.json` (captured with Git environment overrides removed, written through the write tool). Then executed:

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'python3 .ufo/evidence/round-29/coldread/append-entries.py --assembled .ufo/evidence/round-29/coldread/assembled-w1.json --ledger .ufo/evidence/round-21/coldread/ledger.json --receipt /fast/scratch/hyaku/tameshi-r29-critic-select-bound-review-all32-append.json && git add -- .ufo/evidence/round-21/coldread/ledger.json && git -c core.hooksPath=/dev/null -c user.name=CriticSelectBound -c user.email=critic-select-bound@example.invalid -c commit.gpgsign=false commit --quiet -m "Review-only counterfactual: append all 32 assembled reads" && python3 .ufo/evidence/round-29/c1-measure-v2.py --repo /fast/scratch/hyaku/tameshi-r29-critic-select-bound --rev HEAD'
```

Observed (exit 1, expected falsifier result):

```text
{"prior_entries": 371, "appended": 32, "current_entries": 403, "prefix_entries_equal_as_data": true, "other_top_level_keys_unchanged": true}
C1_R29_V2: covered=64/64 restraint=8 box3_mismatch=0 appended=32 bound=22 prefix_equal=1 rev=2ec6c972a8a9b29b17ee84f5e00ee7f2d31a591f
PREDICATE: C1_R29_V2_PASS=false
```

Thus “all 32 would also pass” is false. Selection changes the overall conjunction by removing ten binding failures, not by increasing coverage or changing a failing reader verdict into success.

For the actual E ledger, executed:

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 .ufo/evidence/round-29/c1-measure-v2.py --repo /fast/scratch/hyaku/tameshi-r29-critic-select-bound --rev 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef
```

Observed (exit 0):

```text
C1_R29_V2: covered=64/64 restraint=8 box3_mismatch=0 appended=22 bound=22 prefix_equal=1 rev=7a45f7b9d6a2542a553276330c8b02ac2e28c7ef
PREDICATE: C1_R29_V2_PASS=true
```

Master advanced during review. After fetching only into my clone, executed:

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bash -c 'git fetch --quiet origin master && git log --format="%h %s" --name-only 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef..9bb699ad2d9f795dff95df85eb967129c54927d6 && python3 .ufo/evidence/round-29/c1-measure-v2.py --repo /fast/scratch/hyaku/tameshi-r29-critic-select-bound --rev 9bb699ad2d9f795dff95df85eb967129c54927d6'
```

Observed (exit 0):

```text
C1_R29_V2: covered=64/64 restraint=8 box3_mismatch=0 appended=22 bound=22 prefix_equal=1 rev=9bb699ad2d9f795dff95df85eb967129c54927d6
PREDICATE: C1_R29_V2_PASS=true
```

The observed intervening commit names SCORECARD.md, LOG.md, corpus/lessons/round-29.md and three measurement receipts; it does not change the selection/counter/ledger.

### 4. Read07A and Read10B are format rejects, not failing read verdicts

`.ufo/evidence/round-29/coldread/assemble-w1.out:34-36` and `assembled-w1.json:2409-2419` give the exact rejections:

- **Read07A:** `inputs[corpus/lessons/round-13-verifier-spotcheck.md]` is not a 64-hex SHA256. The report actually supplies `6b8d2cafdab33c72` at `.ufo/waves/round-29/w1/Read07A.md:22`. Its JSON says `executed-ok`, with empty blocking gaps, wrong expectations, and minor gaps at lines 10-12; its final read verdict is also `executed-ok` at line 117.
- **Read10B:** `external-input-shape:https://docs.python.org/3/library/os.html`. The URL keys occur at `.ufo/waves/round-29/w1/Read10B.md:79-82`. Its JSON says `verified-record`, with empty blocking gaps, wrong expectations, and minor gaps at lines 4-6; its final verdict agrees at line 101.

The unchanged assembler requires 64-hex digests (`.ufo/evidence/round-18/coldread/assemble.py:359-373`) and rejects malformed external-input shapes at lines 550-554. These reports did not enter the 32-entry candidate set. They must stay disclosed as rejected evidence, not be represented as accepted passing verification; neither is an observed negative cold-read verdict.

## Smallest safe correction

No production edit or frozen-rule change is needed to make the measured 22-entry ledger satisfy C1. Keep the all-32 failure and the complete exclusion/rejection receipts visible, and state **“22 bound appended entries; ten positive binding rejects; two assembler format rejects”**, rather than implying every assigned/assembled read bound successfully or that 64/64 means a fresh whole-page reread this round. Do not retrospectively rewrite seat identities or verdicts to manufacture binding.

One separate, fixable selector limitation should not become a second authority: `select-bound.py:41` iterates `e.get('reports') or []` without rejecting an empty list, whereas the frozen counter requires `bool(reports)` at `c1-measure-v2.py:132`. An otherwise registered entry without reports would therefore be retained by the helper but rejected by the authoritative counter. This is a static counterexample to the helper's general equivalence claim, **not a failure on this dataset** (`all_reports_nonempty=true`, actual bound=22/22). The smallest prospective helper correction is an explicit nonempty-reports guard; never weaken the frozen counter to match the helper. No such edit was made in this review.

No admission tradeoff is being recommended. The actual selected candidate passes as frozen; the all-32 candidate must remain a miss. All invoked finite commands completed; no background test process was left running.
