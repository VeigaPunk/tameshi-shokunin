# T54W1Sent03 — sentinel attack: fabricate a trace

Round 54 (hyaku run 11, L1 TameshiR54a2), w1, lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

**Item.** In a scratch clone at C0 (`59c38109bf119d0e9d4f878644a82babc937bc1e`), hand-bind a re-key
entry with (a) a trace JSON whose recorded input sha differs from the blob at C0, and (b) a real sha
but a `live_lane_reads` entry naming a live path at a wrong digest. Show the frozen C1 counter
refuses both (`trace-input-drift`, `live-lane-read`).

**Verdict.** Both fabrications are refused, by the same frozen predicate the counter calls
(`r18.entry_reason(lane, rev, entry, strict=True)`), with the two exact reason strings, and the
counter's own verdict line drops the section from credit (`rekeyed` 1/7 -> 0/7, precheck credit
42 -> 41). The trace-only controls — same commit, one field of the trace changed back to the true
value — credit. Nothing in the lane was edited.

| variant | commit | fabricated field | entry_reason (strict) | arm 3 at the counter |
|---|---|---|---|---|
| baseline C0 | `59c3810` | — | — | `rekeyed=0/7 credited=41 lost=23` |
| documented-layout drift | `a1a17228` | `inputs.tools/registry.json` = pre-C0 blob | `trace-input-drift:tools/registry.json` | `rekeyed=0/7 credited=41 lost=23` |
| documented-layout control | `302a504b` | none | `None` | `rekeyed=1/7 credited=42 lost=22` |
| gate drift | `1cf6c010` | `inputs.tools/registry.json` = pre-C0 blob | `trace-input-drift:tools/registry.json` | `rekeyed=0/7 credited=41 lost=23` |
| gate live-read wrong digest | `770d9b62` | `live_lane_reads["<lane>/SKILL.md"]` = `'c'*64` | `live-lane-read:/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` | `rekeyed=0/7 credited=41 lost=23` |
| gate live-read bound (control) | `1ac50207` | none (true C0 digest) | `None` | `rekeyed=1/7 credited=42 lost=22` |

Every variant is the *same* entry, under the *same* section sha
(`164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7`, `## Standing rules`, lines
17-40 at C0), differing in one trace field only. The predicate breakdown proves the isolation:
for all five variants `entry_failure == None`, `entry_credit_reason == None`,
`input_reason == None`; only `trace_reason` changes (receipt `variants.json`, key
`reason_fields`).

## 1. The gate as frozen, and where it is called

* `.ufo/evidence/round-54/c1/measure.py:186-209` (arm 3): an entry credits only when
  `heading` is one of the frozen seven, `read_rev == c0`, `wrong_expectations`/`blocking_gaps`
  are 0 **and** `r18_mod.entry_reason(lane, rev, e, True) is None`.
* `.ufo/evidence/round-18/measure.py:513-526` `entry_reason`: findings -> class -> commands ->
  `input_reason` -> `trace_reason`, first failure wins.
* `.ufo/evidence/round-18/measure.py:330-352` `input_failures` / `:353-360` `input_reason`:
  `sha256(git cat-file blob REV:<p>)` must equal the entry's recorded value.
* `.ufo/evidence/round-18/measure.py:373-430` `trace_reason`: each declared trace must resolve to a
  blob at REV whose JSON `schema` is `tameshi-trace-inputs-v1`; each recorded input key must be in
  the entry's inputs with the **same** digest (`trace-input-drift:<p>` otherwise); each
  `live_lane_reads` key must satisfy `live_read_bound` (`live-lane-read:<p>` otherwise).
* `.ufo/evidence/round-18/measure.py:432-457` `live_read_bound`: a live path counts as a read of REV
  only when it is a blob at REV whose sha256 equals the recorded digest (with the documented `.git/`
  carve-out in the second half of this section, see observation O3).

The entry I bind passes arms 1-4 of that chain on true values, so the only thing an attacker can
turn without tripping an earlier gate is what the trace *records* — which is the surface this item
attacks.

## 2. Environment and exact bytes

* Clone: `git clone --shared --no-checkout <lane> $HYAKU_SCRATCH/tameshi-r54/T54W1Sent03/clone`;
  `git -C <clone> rev-parse --show-toplevel` printed the clone path before any write;
  checked out at C0 on a local branch of the clone only.
* Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku`;
  tree `$HYAKU_SCRATCH/tameshi-r54/T54W1Sent03/`; `TMPDIR` inside it; removed before yield.
* Commits are made with **plumbing only**: `git hash-object -w --stdin`, a private
  `GIT_INDEX_FILE` fed through `git update-index -z --index-info`, `git write-tree`,
  `git commit-tree <tree> -p C0`. No ref is created, no `git add`, no `git commit`, no fetch, no
  reset; the resulting commit sha is handed to the counter as `--rev`. Driver:
  `T54W1Sent03-receipts/attack.py`.
* Counter bytes used. The lane's `c1/measure.py` was amended (freeze amendment 1) while this seat
  ran, so every number below names the bytes it came from:
  * `6a39b38770e828aaa7624644169b07aed18f2f26477170c12d85a33799b1efec` — the C0 blob
    (`git show C0:.ufo/evidence/round-54/c1/measure.py`), reproduced hash-verified at
    `T54W1Sent03-receipts/frozen-c1-at-c0.py`. Runs that report `arm3-rekey dirs=[]` for a trace
    under `.../rekey-r54-<c0>/traces/` used these bytes.
  * `63f5f88147b898ee795dc925a04668d473c1fc845e370947307e3ea141a0b77b` — the lane file at yield and
    the value in `.ufo/evidence/round-54/freeze.json:files["c1/measure.py"]`; this is the byte set
    the deciding run is eligible to use, and the one every verdict quoted in the table came from
    (the gate-* variants were re-run under it and reproduce their pre-amendment verdicts exactly).

## 3. Baseline at C0 (unmodified clone)

`T54W1Sent03-receipts/baseline-frozen-bytes.out` (the same five lines came back from the C0-blob
bytes, `baseline.out`):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=59c38109bf11 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

This matches the frozen claim (credited=41 lost=23 at C0). arm 3 reads `dirs=[]` because no
`rekey-r54-*` path exists yet; arm 4 reads 0/7 readers.

## 4. Attack 1 — a trace whose recorded input sha differs from the blob at C0

The entry (`T54W1Sent03-receipts/entry.json`) records the four true C0 digests, so arm 4's input
gate passes. The trace records the **pre-C0** `tools/registry.json` blob
`d65a5c42b4c1e234edb5b21829954af2603925d9eb93ac9d3472f28ad360427b` (the round-53 content, resolved
from base `d33053f7552d`) where C0 has
`ef79ab8e91986565d728f998c0468a5eb32e9ec30ae7527d6bda39e9cd4287c4`. That is exactly the fabrication
a re-key seat would produce if it copied a trace from before the content commit.

Exact patch bytes (`T54W1Sent03-receipts/patch-gate-trace-input-drift.diff`; the ledger insert is a
byte splice that adds the element and its separator only — the diff has no `-` line at all, so no
existing byte of the 7 MB ledger changes, and the blob still parses with 568 -> 569 entries):

```diff
diff --git a/.ufo/evidence/round-21/coldread/ledger.json b/.ufo/evidence/round-21/coldread/ledger.json
index 2a1ff71..bffd32b 100644
--- a/.ufo/evidence/round-21/coldread/ledger.json
+++ b/.ufo/evidence/round-21/coldread/ledger.json
@@ -66094,6 +66094,39 @@
     ".ufo/waves/round-53/w2/T53W2Read21.json",
     ".ufo/waves/round-53/w2/T53W2Read21.md"
    ]
+  },
+  {
+   "blocking_gaps": 0,
+   "carried_from": {
+    "synthetic": "trace-fabrication attack"
+   },
+   "class": "instruction",
+   "commands_executed_count": 3,
+   "end": 40,
+   "external_inputs": {},
+   "heading": "## Standing rules",
+   "inputs": {
+    "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
+    "corpus/SOURCES.md": "81252de0e185720eaa54ea0ab6ea67b8a97470ef0c11082e049d15641a058ce8",
+    "tools/mutate-and-run.sh": "977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda",
+    "tools/registry.json": "ef79ab8e91986565d728f998c0468a5eb32e9ec30ae7527d6bda39e9cd4287c4"
+   },
+   "minor_gaps": 0,
+   "read_rev": "59c38109bf119d0e9d4f878644a82babc937bc1e",
+   "reports": [
+    ".ufo/waves/round-54/w1/T54W1Sent03.md"
+   ],
+   "seats": [
+    "T54W1Sent03"
+   ],
+   "sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7",
+   "skill_sha256": "e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9",
+   "start": 17,
+   "traces": [
+    ".ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11"
+   ],
+   "verdict": "executed-ok",
+   "wrong_expectations": 0
   }
  ],
  "carried_from": ".ufo/evidence/round-19/coldread/ledger.json",
diff --git a/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11 b/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11
new file mode 100644
index 0000000..c515256
--- /dev/null
+++ b/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11
@@ -0,0 +1,28 @@
+{
+ "argv": [
+  "/usr/bin/python3",
+  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/trace-inputs.py",
+  "59c38109bf119d0e9d4f878644a82babc937bc1e"
+ ],
+ "cwd": "/home/vgpnk/Projects/shokunin/tameshi-shokunin",
+ "dropped_home_count": 0,
+ "env_overrides": {
+  "GIT_CONFIG_GLOBAL": "/dev/null",
+  "GIT_CONFIG_NOSYSTEM": "1"
+ },
+ "exit": 0,
+ "external": {},
+ "inputs": {
+  "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
+  "corpus/SOURCES.md": "81252de0e185720eaa54ea0ab6ea67b8a97470ef0c11082e049d15641a058ce8",
+  "tools/mutate-and-run.sh": "977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda",
+  "tools/registry.json": "d65a5c42b4c1e234edb5b21829954af2603925d9eb93ac9d3472f28ad360427b"
+ },
+ "live_lane_reads": {},
+ "rev": "59c38109bf119d0e9d4f878644a82babc937bc1e",
+ "rev_reason": "hand-bound trace, seat T54W1Sent03 trace-fabrication attack",
+ "root": "/home/vgpnk/Projects/shokunin/tameshi-shokunin",
+ "schema": "tameshi-trace-inputs-v1",
+ "tracked_filter": "git-object reads only",
+ "untracked": []
+}
\ No newline at end of file
```

Counter, at `1cf6c010aaee228d7e273506a6aa194b5f3525c7` (amended bytes; the C0-bytes counter gives the
same verdict line):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=1cf6c010aaee cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
EXPLAIN arm4-readers 0/7
C1_R54: rev=1cf6c010aaee c0=59c38109bf11 credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

The predicate the counter called, printed directly at strict mode (`attack.py`):

```
gate-trace-input-drift  rev=1cf6c010aaee  reason=trace-input-drift:tools/registry.json
```

and the frozen credit algorithm's own per-section record
(`T54W1Sent03-receipts/r18-gate-trace-input-drift-summary.json`):

```
section[17..40] credited=False reason=trace-input-drift:tools/registry.json
```

**Control.** The same commit with that one digest set back to the true C0 value credits: section
`credited=True reason=credited`, counter `credited=42 lost=22 rekeyed=1/7`.
The two patches differ in one line of the trace body (the only other delta `diff` reports is the
`index` blob id git prints for the new trace file):

```
< +  "tools/registry.json": "d65a5c42...427b"     (fabricated: pre-C0 blob)
> +  "tools/registry.json": "ef79ab8e...4287c4"   (true C0 blob, credits)
```

## 5. Attack 2 — a real input sha, but `live_lane_reads` at a wrong digest

Same entry, true input digests everywhere; the trace adds

```json
 "live_lane_reads": {
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
 },
```

Exact patch bytes (`T54W1Sent03-receipts/patch-gate-live-lane-read-wrong-digest.diff`):

```diff
diff --git a/.ufo/evidence/round-21/coldread/ledger.json b/.ufo/evidence/round-21/coldread/ledger.json
index 2a1ff71..bffd32b 100644
--- a/.ufo/evidence/round-21/coldread/ledger.json
+++ b/.ufo/evidence/round-21/coldread/ledger.json
@@ -66094,6 +66094,39 @@
     ".ufo/waves/round-53/w2/T53W2Read21.json",
     ".ufo/waves/round-53/w2/T53W2Read21.md"
    ]
+  },
+  {
+   "blocking_gaps": 0,
+   "carried_from": {
+    "synthetic": "trace-fabrication attack"
+   },
+   "class": "instruction",
+   "commands_executed_count": 3,
+   "end": 40,
+   "external_inputs": {},
+   "heading": "## Standing rules",
+   "inputs": {
+    "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
+    "corpus/SOURCES.md": "81252de0e185720eaa54ea0ab6ea67b8a97470ef0c11082e049d15641a058ce8",
+    "tools/mutate-and-run.sh": "977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda",
+    "tools/registry.json": "ef79ab8e91986565d728f998c0468a5eb32e9ec30ae7527d6bda39e9cd4287c4"
+   },
+   "minor_gaps": 0,
+   "read_rev": "59c38109bf119d0e9d4f878644a82babc937bc1e",
+   "reports": [
+    ".ufo/waves/round-54/w1/T54W1Sent03.md"
+   ],
+   "seats": [
+    "T54W1Sent03"
+   ],
+   "sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7",
+   "skill_sha256": "e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9",
+   "start": 17,
+   "traces": [
+    ".ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11"
+   ],
+   "verdict": "executed-ok",
+   "wrong_expectations": 0
   }
  ],
  "carried_from": ".ufo/evidence/round-19/coldread/ledger.json",
diff --git a/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11 b/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11
new file mode 100644
index 0000000..4253b48
--- /dev/null
+++ b/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/rekey-r54-59c38109bf11
@@ -0,0 +1,30 @@
+{
+ "argv": [
+  "/usr/bin/python3",
+  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/trace-inputs.py",
+  "59c38109bf119d0e9d4f878644a82babc937bc1e"
+ ],
+ "cwd": "/home/vgpnk/Projects/shokunin/tameshi-shokunin",
+ "dropped_home_count": 0,
+ "env_overrides": {
+  "GIT_CONFIG_GLOBAL": "/dev/null",
+  "GIT_CONFIG_NOSYSTEM": "1"
+ },
+ "exit": 0,
+ "external": {},
+ "inputs": {
+  "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
+  "corpus/SOURCES.md": "81252de0e185720eaa54ea0ab6ea67b8a97470ef0c11082e049d15641a058ce8",
+  "tools/mutate-and-run.sh": "977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda",
+  "tools/registry.json": "ef79ab8e91986565d728f998c0468a5eb32e9ec30ae7527d6bda39e9cd4287c4"
+ },
+ "live_lane_reads": {
+  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
+ },
+ "rev": "59c38109bf119d0e9d4f878644a82babc937bc1e",
+ "rev_reason": "hand-bound trace, seat T54W1Sent03 trace-fabrication attack",
+ "root": "/home/vgpnk/Projects/shokunin/tameshi-shokunin",
+ "schema": "tameshi-trace-inputs-v1",
+ "tracked_filter": "git-object reads only",
+ "untracked": []
+}
\ No newline at end of file
```

Counter at `770d9b62aea31d13283a3a69b4e97b20ab9d417c`:

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=770d9b62aea3 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
EXPLAIN arm4-readers 0/7
C1_R54: rev=770d9b62aea3 c0=59c38109bf11 credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

Predicate and section record:

```
gate-live-lane-read-wrong-digest  rev=770d9b62aea3  reason=live-lane-read:/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md
section[17..40] credited=False reason=live-lane-read:/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md
```

**Control.** The same live path at the true C0 `SKILL.md` digest
(`e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9`) credits: `rekeyed=1/7
credited=42 lost=22`.

**Extra probe, refused too (fail-closed).** The same digest on a path under the *clone*
(`/fast/scratch/hyaku/tameshi-r54/T54W1Sent03/clone/SKILL.md`) is refused as well, because
`live_read_bound` returns False for anything outside the live lane root:
`live-lane-read:/fast/scratch/hyaku/tameshi-r54/T54W1Sent03/clone/SKILL.md`.

## 6. The documented re-key layout, under both counter bytes

The round-53 re-key driver writes `.ufo/evidence/round-53/.../traces/section-%02d.json`
(`.ufo/evidence/round-53/integrate/rekey.py:130,147-148`). A round-54 re-key that follows it writes
`rekey-r54-<c0>/traces/section-NN.json`. Two runs of the *same* commit `a1a17228` (a hand-bound
drift entry bound to `.../rekey-r54-59c38109bf11/traces/section-17.json`):

```
# C0 frozen bytes (6a39b38...) — receipts/counter-c0bytes-documented-drift.out
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=a1a172287a18 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=a1a172287a18 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false

# amended frozen bytes (63f5f88...) — receipts/counter-amended-documented-drift.out
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=a1a172287a18 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
EXPLAIN arm4-readers 0/7
C1_R54: rev=a1a172287a18 c0=59c38109bf11 credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

The C0 bytes match `REKEY_RE` against the traced file's **basename**, so the documented layout is
invisible to arm 3 (`dirs=[]`, `c0=none`) and `rekeyed` can never leave 0/7 no matter how good the
re-key is. Amendment 1 (`contract.json.amendments[0]`, quoted verbatim):

> "c1/measure.py arm 3 matched the re-key directory against each traced file's basename; it now
> matches the DIRECTORY component of every traced path. Mechanical discovery bug, found by the
> binder dry run before any control was scored and before any deciding invocation; predicate,
> target and both counters' arms are unchanged."

The amendment is effective and the arm now engages: with the amended bytes the same commit gives
`dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf11`, and the documented-layout control `302a504b`
gives `rekeyed=1/7 credited=42 lost=22`:

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=302a504b150b cand_credited=42 lost=22 RED
EXPLAIN arm2-monitor exit=0 covered=42 score=6
EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
EXPLAIN arm4-readers 0/7
C1_R54: rev=302a504b150b c0=59c38109bf11 credited=42 lost=22 rekeyed=1/7 readers=0/7 monitor=6/42 unstable=0 total=4 C1_R54_PASS=false
```

Reproduced independently of my own driver by the first build of this seat (counter bytes at that
time were the C0 bytes), receipts `counter-documented-layout-drift.out` (`dirs=[]`) against
`counter-gate-control-good.out` (trace file named after the directory:
`dirs=['rekey-r54-59c38109bf11']`, `rekeyed=1/7`).

## 7. Observations for the L1 / integrator

**O1 (fixed mid-round, verified).** Arm 3's re-key discovery was basename-keyed at the C0 bytes;
the documented `section-NN.json` layout was undetectable, so C1's arm 3 could not have passed for a
correct re-key, and a wave could only reach the arm by inventing an undocumented trace filename
(`.../traces/rekey-r54-<c0>`, which is how I first reached it). Freeze amendment 1 changes the match
to the directory component; I verified the before/after pair on one commit (§6). Severity if
unfixed: the target is reachable only through a filename no seat was told to produce, and the
undocumented one is the only shape the arm can see.

**O2 — `CTL_FAB` does not exercise the gate it names (calibration).** `controls.sh:59-95` binds the
fabricated trace at `.ufo/evidence/round-54/fab/traces/fabricated.json` — not under
`rekey-r54-<c0>` — so arm 3 never evaluates that entry; the control passes because `rekeyed=0/7`
for the trivial reason `dirs=[]`. The pre-registered receipt shows the fabricated entry was
**credited**: `controls-a.stdout` has
`CTL CTL_FAB C1_R54: rev=f6fe57bfcad0 c0=none credited=58 lost=6 ...`, one more than the base's 57.
My control runs reproduce that at the entry contract: a hand-written trace whose `argv` names a
command I never ran, with true C0 digests, takes arm 1's precheck from `credited=41 lost=23` to
`credited=42 lost=22` (`counter-amended-documented-control.out`). The credit gate binds *content*
(inputs hash to the measured bytes), not *execution*; seven consistent hand-written traces would
read `rekeyed=7/7`. That is a meaning limit of "credited at the deciding revision", not a code
defect — but CTL_FAB should bind under the re-key directory and assert the per-entry refusal
reason, not only the aggregate `PASS=false`, or it cannot tell a gate that works from an arm that
never ran.

**O3 — `live_lane_reads` under the lane's `.git/` is digest-blind (by design).**
`.ufo/evidence/round-18/measure.py:432-457` accepts any digest for a path under `<lane>/.git/`
(rev-addressed object reads), and the frozen selftest relies on that
(`.ufo/evidence/round-18/measure.py:949-951` binds `.git/HEAD` at `'d'*64` and credits). Probe
(`T54W1Sent03-receipts/dotgit-probe.out`), a trace with both `.git/config` and `.git/objects/pack`
at invented digests:

```
commit 73ebb03f8d8e6fea720c5917b3aa79dcc1beca6f
entry_reason None
live_read_bound(.git/config, c*64) True
```

So `live_lane_reads` cannot be the guard for working-tree reads; the entry's `inputs` remain the
only content gate (as the docstring says). No action requested — recording it so no one reads
`live_lane_reads` as stronger than it is.

**O4 — the freeze manifest is self-consistent at yield (checked, no action).** During the seat the
manifest was transiently stale: `freeze.json` listed `contract.json` at
`e15bffb3e888dd39bfc2a0932f054a416a506351c1be850427989792b08c380e` (the C0 blob) while the amended
contract on disk hashed `fca27997...`. Recomputing at yield shows the L1 has re-pinned everything:
all ten hashed paths match the tree (`contract.json` `7283e67...`, `c1/measure.py` `63f5f88...`,
`c2/measure.py` `49280f...`, `deciding-run.sh` `42fb06...`, `freeze.json` itself excluded by design),
and the three newly pinned dependencies are byte-identical to their C0 blobs
(`round-18/measure.py` `7ca87a7c...`, `round-21/coldread/measure.py` `657f009b...`,
`round-48/quality/coldread-precheck.sh` `3b07847a...`). Amendments 1 and 2 are recorded in both
`freeze.json` and `contract.json`.

## 8. What I opened

* `.ufo/evidence/round-54/c1/measure.py` — arms 1-4; the arm-3 tree scan (`:170-215` working bytes,
  `:173-185` at the C0 blob), the frozen-heading loop (`:186-209`), the wave reader arm.
* `.ufo/evidence/round-18/measure.py` (C0 blob) — `CANONICAL_LANE_PATH`/`inputs_view`/`input_failures`
  (`:297-360`), `trace_reason` (`:373-430`), `live_read_bound` (`:432-457`), `entry_failure`/
  `entry_credit_reason`/`entry_reason` (`:459-526`), `coldread` credit selection (`:549-650`),
  selftest trace fixtures (`:941-951`, `:1286-1312`), CLI (`:1516-1620`).
* `.ufo/evidence/round-21/coldread/measure.py` (selector), `.ufo/evidence/round-21/coldread/ledger.json`
  (568 entries, format and tail), `rekey-r53-651773ab9e32/traces/section-01.json` (trace schema).
* `.ufo/evidence/round-53/integrate/rekey.py:130,147-148` (documented trace filenames).
* `.ufo/evidence/round-54/contract.json` (C1 target/controls/kill rule), `freeze.json` (hashes and
  amendment 1), `control/controls.sh:40-100` + `controls-a.stdout`/`controls-a.exit`,
  `deciding-run.sh:26,35-36`, `c1/lost-headings-at-base.json`.
* `.ufo/waves/round-54/spec-w1.json` — names the re-key step for the counter but prescribes no trace
  filename to the seats (the only `re-key` hits are the three items that discuss the arm).
* Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` -> `ok`, exit 0.

## 9. Reproduction

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r54/T54W1Sent03; mkdir -p "$S/tmp"; export TMPDIR="$S/tmp"
git clone --shared --no-checkout <lane> "$S/clone"
git -C "$S/clone" checkout --quiet -B attack 59c38109bf119d0e9d4f878644a82babc937bc1e
mkdir -p "$S/receipts"
python3 <receipts>/attack.py                 # builds all five commits, prints the strict reason
python3 <receipts>/section17_control.py       # documented-layout control commit 302a504b
python3 <receipts>/documented_layout.py       # documented-layout drift commit a1a17228
python3 <receipts>/dotgit.py                  # .git carve-out probe
python3 <lane>/.ufo/evidence/round-54/c1/measure.py --lane "$S/clone"         --rev <commit> --work "$S/work" --explain
```

`<receipts>` = `.ufo/waves/round-54/w1/T54W1Sent03-receipts/`. The clone is throwaway; the commits
exist only inside it and only their shas are quoted here.

## 10. Bounds honoured / tooling

* No lane file edited; no mutation outside the scratch clone; no ref, `git add`, `git commit`,
  `git push`, `git fetch` or `git reset` anywhere. Every `git -C` named the scratch clone.
* Read-only surfaces used as read-only: fleet root, `.ufo/state/`, `tools/registry.json`, sibling
  material.
* Scratch tree `$HYAKU_SCRATCH/tameshi-r54/T54W1Sent03` removed before yield (`trap ... EXIT` in the
  driving shell); nothing left under `/tmp`.
* No tool installed or upgraded this seat.
