# T54W1Sent02 — sentinel attack: pin LOG.md

Item: in a scratch clone at C0, hand-bind one ledger entry whose inputs include LOG.md and
whose trace records that sha, commit a LOG.md change, run the frozen C1 counter at the new
revision, show the entry stops crediting (input-drift), and name the arm that catches a
re-key with this failure mode.

Everything below happened in `$HYAKU_SCRATCH/tameshi-r54/T54W1Sent02/lane`, a
`git clone --shared` of the lane at `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0).
`git -C … rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/tameshi-r54/T54W1Sent02/lane` before every mutation. No lane file,
counter, contract, freeze, ledger (lane copy) or wave spec was written by this seat; all
receipts are under `T54W1Sent02-receipts/`.

## Result in one line

The LOG.md pin **does** cost the entry its credit (frozen r18 `input_reason` →
`input-drift:LOG.md`; arm 1's `cand_credited` drops 42 → 41), but the arm that is *supposed*
to catch the re-key with this failure mode — arm 5 `stable` / `UNSTABLE_INPUTS` — never runs:
arm 3's directory enumeration returns `dirs=[]` for the documented `rekey-r54-<c0>/traces/…`
layout, so `rekey_ok` is false and the whole `if rekey_ok:` block that contains arm 5 is
skipped. As frozen, `C1_R54_PASS` cannot become true at all, and a LOG.md-pinned re-key is
invisible to the counter's `unstable` field.

## Fixture (4 commits on top of C0)

| tag | commit | what it adds |
|---|---|---|
| C0 | `59c38109bf119d0e9d4f878644a82babc937bc1e` | untouched |
| REV1 | `a0abec06167c43228fbab4e32407fcf2e43e8e87` | hand-bound entry for `## Standing rules` (section sha `164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7`, start 17 end 40), `inputs={"LOG.md": c1dcfc52…}`, trace `…/rekey-r54-59c38109bf11/traces/SENT01/1.json` recording the same sha, `read_rev=C0` |
| REV2 | `8837b300b0c2a5bdedd5adc9ac03f17239469d3b` | one appended LOG.md line; LOG.md sha256 `c1dcfc52…` → `a7331afb…` |
| REV3 | `d4a7b843127f620d50e0832119e85383c8eaaefc` | child of REV1: one *file* named `rekey-r54-59c38109bf11` inside `…/traces/SENT01/` (arm-3 enumeration probe; LOG.md still at C0) |
| REV4 | `a38aab99bb928c3a4c44565076cec6bf1e317622` | child of REV3: the same LOG.md line |
| REV5 | `e7448b08e1950f8c123cb78bb3f06bd7b85ba054` | child of REV4: second entry `SENT02` for the same section, `inputs={"PROVINCE.md": b2875fe2…}`, `external_inputs={"LOG.md": c1dcfc52…}` (stale at REV5) |

Exact patch bytes:

`bind.patch` (REV1, 33 insertions, 2 files):

```
diff --git a/.ufo/evidence/round-21/coldread/ledger.json b/.ufo/evidence/round-21/coldread/ledger.json
index 2a1ff71..3461f68 100644
--- a/.ufo/evidence/round-21/coldread/ledger.json
+++ b/.ufo/evidence/round-21/coldread/ledger.json
@@ -66094,6 +66094,33 @@
     ".ufo/waves/round-53/w2/T53W2Read21.json",
     ".ufo/waves/round-53/w2/T53W2Read21.md"
    ]
+  },
+  {
+   "skill_sha256": "e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9",
+   "start": 17,
+   "end": 40,
+   "heading": "## Standing rules",
+   "sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7",
+   "class": "record",
+   "verdict": "verified-record",
+   "blocking_gaps": 0,
+   "wrong_expectations": 0,
+   "minor_gaps": 0,
+   "commands_executed_count": 1,
+   "read_rev": "59c38109bf119d0e9d4f878644a82babc937bc1e",
+   "inputs": {
+    "LOG.md": "c1dcfc5273767bac595cc2b1061fe4d74a0ee5b756deced3b6c4c12fd8f45e3c"
+   },
+   "external_inputs": {},
+   "traces": [
+    ".ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/SENT01/1.json"
+   ],
+   "seats": [
+    "SENT01"
+   ],
+   "reports": [
+    ".ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/SENT01/1.json"
+   ]
   }
  ],
  "carried_from": ".ufo/evidence/round-19/coldread/ledger.json",
diff --git a/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/SENT01/1.json b/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/SENT01/1.json
new file mode 100644
index 0000000..7880435
--- /dev/null
+++ b/.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/SENT01/1.json
@@ -0,0 +1,6 @@
+{
+ "inputs": {
+  "LOG.md": "c1dcfc5273767bac595cc2b1061fe4d74a0ee5b756deced3b6c4c12fd8f45e3c"
+ },
+ "schema": "tameshi-trace-inputs-v1"
+}
```

`log-change.patch` (REV2):

```
diff --git a/LOG.md b/LOG.md
index 61c1618..e724e9b 100644
--- a/LOG.md
+++ b/LOG.md
@@ -2492,3 +2492,4 @@ under this entry.
   three read revisions, inputs pinned at C7). Deciding run at 88afa941:
   C1 honest stop (58/64, six sections named in SCORECARD), C2 verified.
   Fleet census end: exit 0. Report committed on the fleet repo.
+- 2026-10-28 — round 54 (attack fixture): LOG.md touched after the bind; the pinned entry must stop crediting.
```

## Receipts — command, output, verdict

Counter invocation, identical every time except REV (fresh empty `--work` per run):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py \
  --lane /fast/scratch/hyaku/tameshi-r54/T54W1Sent02/lane --rev REV --work WORK --explain
```

| rev | code | counter verdict line | verdict |
|---|---|---|---|
| C0 | `59c38109bf11` | `EXPLAIN arm1-precheck exit=1 … cand=59c38109bf11 cand_credited=41 lost=23 RED` / `EXPLAIN arm3-rekey dirs=[] c0=None` / `C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false` | control: clone reproduces the frozen before-number (41/23) exactly |
| REV1 | `a0abec06167c` | `EXPLAIN arm1-precheck exit=1 … cand=a0abec06167c cand_credited=42 lost=22 RED` / `EXPLAIN arm3-rekey dirs=[] c0=None` / `C1_R54: rev=a0abec06167c c0=none credited=42 lost=22 rekeyed=0/7 readers=0/7 monitor=6/42 unstable=0 total=4 C1_R54_PASS=false` | the bound entry **credits**: `cand_credited` 41 → 42. `rekeyed=0/7` and `unstable=0` **despite** a real `rekey-r54-59c38109bf11/traces/` tree being present |
| REV2 | `8837b300b0c2` | `EXPLAIN arm1-precheck exit=1 … cand=8837b300b0c2 cand_credited=41 lost=23 RED` / `EXPLAIN arm3-rekey dirs=[] c0=None` / `C1_R54: rev=8837b300b0c2 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false` | after one LOG.md line the entry **stops crediting** (42 → 41) and the counter reports nothing else: `unstable=0` |
| REV3 | `d4a7b843127f` | `EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e` / `C1_R54: rev=d4a7b843127f c0=59c38109bf11 credited=42 lost=22 rekeyed=1/7 readers=0/7 monitor=6/42 unstable=1 total=5 C1_R54_PASS=false` | arm 3 only sees the re-key dir once a **file basename** matches the regex; then arm 5 fires: `unstable=1` |
| REV4 | `a38aab99bb92` | `C1_R54: rev=a38aab99bb92 c0=59c38109bf11 credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=1 total=5 C1_R54_PASS=false` | with arm 3 satisfied, drift is caught twice: credit 42 → 41 **and** `unstable=1` |
| REV5 | `e7448b08e195` | `C1_R54: rev=e7448b08e195 c0=59c38109bf11 credited=42 lost=22 rekeyed=1/7 readers=0/7 monitor=6/42 unstable=1 total=5 C1_R54_PASS=false` | a second entry re-credits the same section while its only LOG.md digest (`external_inputs`, stale `c1dcfc52…` vs `a7331afb…`) is never verified and never flagged |

Direct credit-algorithm receipts (`probe.py` = the FROZEN round-18 `measure.py` bytes at C0,
`entry_reason(lane, rev, entry, True)`):

```
rev=a0abec06167c  inputs={"LOG.md": c1dcfc52…}  entry_reason=null           input_reason=null
rev=8837b300b0c2  inputs={"LOG.md": c1dcfc52…}  entry_reason=input-drift:LOG.md  input_reason=input-drift:LOG.md
rev=d4a7b843127f  inputs={"LOG.md": c1dcfc52…}  entry_reason=null
rev=a38aab99bb92  inputs={"LOG.md": c1dcfc52…}  entry_reason=input-drift:LOG.md
rev=e7448b08e195  SENT01 inputs={"LOG.md": c1dcfc52…}            entry_reason=input-drift:LOG.md
rev=e7448b08e195  SENT02 inputs={"PROVINCE.md": b2875fe2…}
                  external_inputs={"LOG.md": c1dcfc52…}          entry_reason=null      (LOG.md is a7331afb… at REV5)
```

## Findings

### F1 — HIGH (blocking): arm 3 enumerates *file basenames*, so `rekey_dirs` is empty for every legitimate re-key tree

`c1/measure.py:172-175`

```python
    tree = git(['-C', lane, 'ls-tree', '-r', '--name-only', rev,
                '.ufo/evidence/round-21/coldread/'], check=False).stdout.decode()
    rekey_dirs = sorted({Path(p).name for p in tree.splitlines()
                         if REKEY_RE.match(Path(p).name) and '/traces/' in p})
```

`ls-tree -r --name-only` lists **blobs only**; `Path(p).name` is therefore the trace file's
basename (`1.json`, `section-07.json`), never the directory. `REKEY_RE` is
`^rekey-r54-([0-9a-f]{12})$`, so the set is empty for every tree whose trace files are
ordinary names.

Evidence (scratch clone):

```
$ git -C lane ls-tree -r --name-only a0abec06167c .ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/
.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/SENT01/1.json
('…/rekey-r54-59c38109bf11/traces/SENT01/1.json', '1.json', False, True)
rekey_dirs = []
parent-component match = ['traces']
```

…and the counter agrees: `EXPLAIN arm3-rekey dirs=[] c0=None` at REV1 and REV2 even though
the directory exists and the entry's trace lives under it. It only becomes non-empty when a
*file* is literally named `rekey-r54-59c38109bf11` (REV3, `contrived-name.patch`):
`EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf11…`.

Exploit path (no attacker needed — it is the happy path): a wave builds the documented
`rekey-r54-<c0>/traces/<seat>/<n>.json` tree, the ledger binds entries under it, every
reader report pins `cand=<c0>`; arm 3 still prints `dirs=[]`, so

* `rekeyed` stays `0/7` (`rekeyed != len(frozen)` → `total += 1`);
* `c0` stays `None`, so arm 4's `d.get('cand') == c0` never matches a real
  `59c38109bf11…` reader report → `readers=0/7` (`total += 1`);
* arm 5 never runs (see F2).

Impact: `C1_R54_PASS` is unreachable. A perfect re-key and seven perfect reader reports
produce `rekeyed=0/7 readers=0/7 … C1_R54_PASS=false`. The frozen claim C1 cannot be
satisfied by any honest wave, and the counter's failure does not name its own cause.

Context: the docstring at `c1/measure.py:16` says the round-53 counter's non-recursive
pathspec was "its R53.1 defect". The round-54 rewrite made the listing recursive but kept
the naming of the leaf; `.ufo/evidence/round-53/c1/measure.py:94-97` matched
`fullmatch(r'rekey-r53-…', n)` against the same blob names, so the R53.1 class survives this
fix in a new shape.

Smallest remediation (frozen file → L1 amendment, not a seat edit): test the *directory*
component, e.g. replace the comprehension with
`{p.split('/')[4] for p in tree.splitlines() if p.split('/')[4].startswith('rekey-r54-')}`
(paths are always `.ufo/evidence/round-21/coldread/<dir>/…`), or enumerate with
`git ls-tree -d --name-only rev .ufo/evidence/round-21/coldread/` and match `Path(p).name`.
Adding a selftest whose fixture tree has a trace named `1.json` under
`rekey-r54-<c0>/traces/` and asserting `dirs != []` would have caught this.

### F2 — HIGH: arm 5 (`stable`, the arm that catches a LOG.md pin) is dead code inside `if rekey_ok:`

`c1/measure.py:192-203`

```python
    rekeyed = 0
    unstable = []
    if rekey_ok:
        rekey_prefix = '.ufo/evidence/round-21/coldread/' + rekey_dirs[0] + '/'
        bound = [e for e in entries if …]
        for e in bound:
            inputs = e.get('inputs') or {}
            for p in UNSTABLE_INPUTS:
                if p in inputs:
                    unstable.append('%s:%s' % (e.get('heading', '?')[:40], p))
```

Because `rekey_ok` is false whenever arm 3's enumeration fails (F1), `unstable` stays `[]` and
the LOG.md/SCORECARD.md guard never evaluates a single entry. Receipt: REV2, where a bound
entry pins `LOG.md`, prints `unstable=0`; only the contrived REV3/REV4/REV5 trees print
`unstable=1`.

Impact: the one arm written for this failure mode — the round-53 "re-key lost its credit
because it pinned LOG.md, which changes every round" lesson — cannot fire on the actual
re-key layout. A wave that pins LOG.md and a wave that does not are indistinguishable to the
counter (`unstable=0`) until the *next* revision silently drops the sections.

Naming, as asked: the arm is **arm 5 `stable`** (`UNSTABLE_INPUTS` at `:55`, scan at `:199-203`,
`if unstable: total += 1`). It is the correct arm and it is currently unreachable. The drift
itself is caught only by the frozen r18 `input_reason` (`input-drift:LOG.md`) reached through
arm 1's precheck and arm 3's per-entry `r18_mod.entry_reason(lane, rev, e, True)` — a
*post-hoc* credit loss, never a named pin.

Smallest remediation: hoist the `UNSTABLE_INPUTS` scan out of `if rekey_ok:` and run it over
every entry whose `traces` contain `/rekey-r54-` (prefix derived from the path, no c0
resolution needed). One extra condition, no new data.

### F3 — MEDIUM (confirmed guard, wrong shape): a LOG.md pin costs credit at C0+1 but the verdict never says why

Receipts: arm 1 `cand_credited=42` (REV1) → `41` (REV2) from a one-line LOG.md append; frozen
`entry_reason` `null` → `input-drift:LOG.md`. So the credit loss is real and reproducible.
But at REV2 the verdict reads `credited=41 lost=23 rekeyed=0/7 … unstable=0` — byte-identical
in the `unstable` field to a wave that never pinned LOG.md. The wave cannot tell "the re-key
did not credit because its input drifted" from "the re-key is empty"; the `--explain` output
carries no per-entry reason. That is the same silent shape as round 53's loss.

Smallest remediation: none needed for safety (drift is caught), but arm 3 should surface the
first failing entry reason per frozen heading in `--explain` (`… frozen[i] reason=…`) so the
next round's loss is attributable without re-running r18 by hand.

### F4 — MEDIUM: a LOG.md pin can be laundered through entry-level `external_inputs`, where nothing checks it

* r18 `input_reason` reads only `entry['inputs']` (`measure.py:353-359` + `inputs_view`).
* `coldread()` only *aggregates* `external_inputs` for reporting (`measure.py:605-608`) — it
  never verifies a digest there.
* arm 5 reads only `e.get('inputs')` (`c1/measure.py:199-202`).

Receipt (REV5): the `SENT02` entry carries `inputs={"PROVINCE.md": b2875fe2…}` and
`external_inputs={"LOG.md": c1dcfc52…}` while LOG.md at REV5 is `a7331afb…`. Frozen
`entry_reason` → `null` (credits), counter `cand_credited=42`, `arm5_flags=[]`
(`arm5-attribution.txt`):

```
bound entries: 2
  seat=['SENT01'] inputs=['LOG.md'] external_inputs=[] arm5_flags=['LOG.md']
  seat=['SENT02'] inputs=['PROVINCE.md'] external_inputs=['LOG.md'] arm5_flags=[]
LOG.md sha256 at REV5: a7331afb715411de40c738e2f7da5e99fe85cf91fefe37007d46f982cccc9046
arm5 unstable set: ['## Standing rules:LOG.md']
```

Impact: even after F1/F2 are fixed, the arm-5 sentence "no entry bound under rekey-r54-*
pins LOG.md or SCORECARD.md as an input" is evadable by moving the dependency one key over;
the entry then credits indefinitely while its only record of the LOG.md bytes is stale.

Smallest remediation: treat `external_inputs` keys as first-class pinned inputs in both the
arm-5 scan and the r18 input gate (verify their digests at REV the same way `inputs` are).

## Sweep record (what was run, all read-only against the lane)

* `grep`/`sed` over `.ufo/evidence/round-54/c1/measure.py`, `.ufo/evidence/round-18/measure.py`,
  `.ufo/evidence/round-21/coldread/ledger.json` (shape + arm logic).
* `git ls-tree -r --name-only` / `-d --name-only` on the fixture (F1 evidence).
* 6 frozen-counter runs (C0, REV1…REV5), 5 direct `entry_reason` probes, 1 arm-5 attribution.
* Not attempted: reader-report forgery (Sent01 sibling item), trace forgery (Sent03),
  `live_lane_reads` manipulation. No lane file touched; no `agent://all` message.

## Tooling

No installs or upgrades were needed; the fixture uses `git`, `python3` (stdlib only) and the
frozen counters already in the lane.

## Receipts directory

`T54W1Sent02-receipts/`: `bind.patch`, `log-change.patch`, `contrived-name.patch`,
`log-change-contrived.patch`, `laundry-bind.patch`, `bind.py`, `probe.py`,
`counter-rev1.out` … `counter-rev5.out`, `probe-rev1.out` … `probe-rev5.out`,
`arm5-attribution.txt`, `fixture-history.txt`.

## Fixture lifecycle

The clone lived at `/fast/scratch/hyaku/tameshi-r54/T54W1Sent02/` (`lane/`, `bind.py`,
`probe.py`, per-run `--work` dirs) and was removed after the receipts above were copied, per
the seat's scratch bound. The five fixture commits are reproducible from the patches in
`T54W1Sent02-receipts/` applied to `59c38109bf119d0e9d4f878644a82babc937bc1e` in that order
(`bind.patch` → `log-change.patch`; the REV3-REV5 branch is `contrived-name.patch` →
`log-change-contrived.patch` → `laundry-bind.patch`, applied to `bind.patch`). No file under
`/tmp` was created; `TMPDIR` pointed into the same scratch tree.
