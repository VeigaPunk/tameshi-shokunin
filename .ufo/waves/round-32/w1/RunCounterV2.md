# RunCounterV2 — repair check: round-31 C1 counter v2 (routed items 1–2)

seat: `TameshiR32.RunCounterV2` (leaf executor) · lane: `tameshi-shokunin` · axis: **calibration**
scope: verify that `.ufo/evidence/round-32/repair/c1-r31-measure-v2.py` differs from the frozen round-31
counter `.ufo/evidence/round-31/c1-measure.py` by exactly the two intended condition changes plus the
docstring, and that v2 produces the same verdict as v1 on real lane data at both measured revisions.

**Verdict: PASS.** The diff is exactly the two intended condition changes plus the docstring (3 hunks,
no other byte differs). All four counter runs completed; v1 and v2 stdout are byte-identical at both
revisions, so v2 changes no verdict on real data.

---

## 1. Diff verification — exactly two conditions plus the docstring

### Files compared

| Role | Path | sha256 |
|---|---|---|
| frozen v1 | `.ufo/evidence/round-31/c1-measure.py` | `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` |
| repair v2 | `.ufo/evidence/round-32/repair/c1-r31-measure-v2.py` | `e49b00de184ecb4c3a94b49b9d89a13650b13bc8ca6cd57c1a5f68c971f713b7` |

The v1 hash equals `contract.json` `claims[0].counter_sha256` (`.ufo/evidence/round-31/contract.json:14`);
the v2 hash equals the committed blob at the freeze commit `c318149`
(`git show c318149:.ufo/evidence/round-32/repair/c1-r31-measure-v2.py | sha256sum` → same digest), so the
repair file is committed content, not a working-tree edit.

### Command

```
diff -u .ufo/evidence/round-31/c1-measure.py .ufo/evidence/round-32/repair/c1-r31-measure-v2.py
```

Observed: `1 file changed, 11 insertions(+), 3 deletions(-)`. An independent line-level
`difflib.SequenceMatcher` over the same two files reports **3 opcodes, all non-`equal`** — the whole diff,
not a sampled view:

| # | v1 lines | v2 lines | Change | Kind |
|---|---|---|---|---|
| 1 | 2 | 2–9 | docstring: first line gains `, round-32 repair v2`, plus a 5-line paragraph describing the two changes and stating the output label stays `C1_R31` | docstring |
| 2 | 116 | 122 | `elif len(header) > 1 and header[1].startswith('Score'):` → `elif len(header) > 1 and header[1] == 'Score (0–10)':` | **condition 1** (routed item 1: axis-header selector) |
| 3 | 201 | 207–210 | `append_only = int(rev_sc.stdout.startswith(base_sc.stdout))` → two `subprocess.run(['git','-C',a.lane,'show', …:SCORECARD.md'], capture_output=True, env=env())` calls (bytes, not text) and `append_only = int(base_b.returncode == 0 and rev_b.returncode == 0 and rev_b.stdout.startswith(base_b.stdout))` | **condition 2** (routed item 2: append-only byte prefix) |

Everything else in the file — `STATEMENTS`, `CMD_D`, `env()`, `git()`, `strip_hidden()`, `tables()`,
`first_cells()`, `last_rows()`, `claim_of()`, `observe()`, `main()`'s clone/mirror setup, the statement
loop and the `C1_R31:` print format — is byte-identical. No third condition, no formatting-only drift,
no behavioural change outside the two selectors.

Notes on the two conditions, for calibration:

* Condition 1 literal is `Score (0–10)` with U+2013 EN DASH. The committed `SCORECARD.md` header at both
  revisions uses the same en dash (`git show <rev>:SCORECARD.md | sed -n '64p' | hexdump -C` → `30 e2 80 93 31 30 29`),
  so the strict equality matches the real file. The contract prose (`contract.json:12`) writes the
  hyphen form `Score (0-10)` (ASCII `2d`); the code now encodes the file's actual bytes, not the prose's.
  On this data the two readings coincide, so the choice is not load-bearing here.
* Condition 2 is a genuine tightening: v1 compared `str` objects produced by `git(... capture_output=True,
  text=True)` (default UTF-8 decode, lossy on invalid bytes); v2 compares raw `bytes` from
  `capture_output=True` without `text=True`, and additionally requires both `git show` calls to succeed
  (`returncode == 0`). v1's `base_sc`/`rev_sc` are still read for the row extraction; v2 adds two extra
  byte-level reads.

---

## 2. Fleet mirror setup

The counter's docstring and `--lane`/`--base` options were read first. It takes `--rev`, `--lane`
(default `/home/vgpnk/Projects/shokunin/tameshi-shokunin`), `--base` (default
`36c1d3933f680125aeefc447f07db0f03004901a`) and a required `--work` that must be empty or absent.
`main()` clones `--lane` twice — once into `<work>/clone` and once into `<work>/fleet/tameshi-shokunin`
(the *mirror*) — checks out `--rev` in both, and symlinks every sibling `*-shokunin` directory of the
fleet root into `<work>/fleet/` so the six-leg regression leg can materialise its ledger targets.

Setup performed in this seat's scratch only:

```
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/RunCounterV2
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r32-seats/RunCounterV2/lane
```

`git -C lane rev-parse --verify 08125328f87df92d3f25d0034ee792253ecbcbd9^{commit}` → exit 0;
same for `36c1d3933f680125aeefc447f07db0f03004901a`. Both counters were then run **from the clone's
copies** (`.ufo/evidence/round-31/c1-measure.py` and `.ufo/evidence/round-32/repair/c1-r31-measure-v2.py`
inside the clone), each with `--lane` pointing at that clone and `--base 36c1d3933f680125aeefc447f07db0f03004901a`.
The clone is clean (`git status --porcelain` empty) and untouched by the runs.

---

## 3. The four runs

Fresh `--work` per run (empty dir under the seat scratch), `timeout 2700` on each, all four launched
concurrently under `setsid` (script `run-all.sh` in the seat scratch). Receipts:
`<scratch>/runs/<tag>/{stdout,stderr,exit,seconds}`.

| tag | counter | rev | exit | wall |
|---|---|---|---|---|
| v1-base | frozen round-31 | `36c1d3933f680125aeefc447f07db0f03004901a` | 1 | 539 s |
| v1-head | frozen round-31 | `08125328f87df92d3f25d0034ee792253ecbcbd9` | 0 | 541 s |
| v2-base | round-32 repair v2 | `36c1d3933f680125aeefc447f07db0f03004901a` | 1 | 537 s |
| v2-head | round-32 repair v2 | `08125328f87df92d3f25d0034ee792253ecbcbd9` | 0 | 538 s |

All four stderr files are empty. No run hit the 2700 s timeout; the six-leg regression ledger leg (the
long pole, 2700 s inner timeout) completed in every run, so `unobservable=0` is a real observation, not a
timeout artefact.

### Result table (as requested)

| rev | v1 `C1_R31` line | v2 `C1_R31` line | equal? |
|---|---|---|---|
| `36c1d3933f680125aeefc447f07db0f03004901a` | `C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=36c1d3933f680125aeefc447f07db0f03004901a C1_R31_PASS=false` | `C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=36c1d3933f680125aeefc447f07db0f03004901a C1_R31_PASS=false` | **yes** |
| `08125328f87df92d3f25d0034ee792253ecbcbd9` | `C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=08125328f87df92d3f25d0034ee792253ecbcbd9 C1_R31_PASS=true` | `C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=08125328f87df92d3f25d0034ee792253ecbcbd9 C1_R31_PASS=true` | **yes** |

**Expected result confirmed: equal at both revisions.** Stronger than line-equality — the whole stdout is
byte-identical per revision pair:

```
diff v1-base/stdout v2-base/stdout   -> IDENTICAL   (sha256 6851938d7d37fe7cc6c24e52a22f59b854aec137bbef663ca660d25efb2653c2)
diff v1-head/stdout v2-head/stdout   -> IDENTICAL   (sha256 b3c3332e3a71c987c55cbcc87e8061f622acd62e85e9f04b0b7b3ab191864186)
```

All 12 `STATEMENT …` lines agree per pair, not just the summary. Independent cross-check of the head run
against the lane's own committed round-31 receipt: the 12 statement lines of `v1-head/stdout` are identical
to `.ufo/evidence/round-31/after/c1-at-final.stdout` (modulo the `rev=` field, which the committed
receipt omits) — so the v1 harness reproduces the lane's frozen measurement, and v2 reproduces v1.

### Why the two changes are inert on this data (mechanism, not just outcome)

Independently of the runs, the two selectors were exercised directly against the committed
`SCORECARD.md` at both revisions:

* **Header selector.** Every table in the file was classified under v1's `startswith('Score')` and v2's
  `== 'Score (0–10)'`. At `36c1d393` there is exactly one `Score`-headered table (line 64) and at
  `08125328` exactly two (lines 64 and 1534) — in both cases the header cell is literally
  `Score (0–10)` (en dash). The set of tables classified differently by the two conditions is **empty**
  at both revisions, and `last_rows()` returns the same 12 rows (base) / 15 rows (head) under both.
  `depth` claims `6`→`9` and `calibration` `0`→`8` identically under both.
* **Append-only.** Independently recomputed from raw `git show` bytes: base `SCORECARD.md` is a byte
  prefix of head's at both revisions (118 152 B → 118 152 B at base, → 127 356 B at head), so
  `append_only=1` under both the v1 text test and the v2 byte test.

So on the real lane data neither repair can move the verdict, and the measured equality is the expected
behaviour rather than a coincidence.

---

## 4. Risk notes for the integrator

* The v2 axis-header literal uses **U+2013 EN DASH** (`Score (0–10)`), matching the bytes of the committed
  `SCORECARD.md` header, while `contract.json:12` writes the **ASCII hyphen** form (`Score (0-10)`).
  The routed defect text ("the contract says `Score (0–10)`") and the contract prose disagree with each
  other on the dash. v2 encodes the file's actual bytes, which is the defensible choice, but the next
  contract should quote the selector's exact code condition (as routed item 1 requires) *including* the
  dash byte, so the contract text and the code cannot drift apart again.
* v2 keeps v1's `base_sc`/`rev_sc` (text-mode `git show`) for row extraction and adds two byte-mode
  `git show` calls for the append-only test. That is 4 `git show` reads of `SCORECARD.md` per run where
  v1 had 2. Cheap, but worth stating so nobody later reads it as an accident.
* v2's byte-mode reads use `env=env()`, which strips `GIT_*` from the environment, exactly as v1's `git()`
  helper does — no new environment surface.
* The v2 counter prints the label `C1_R31`, not `C1_R32`. Its docstring says so explicitly. If round 32
  wants a separate claim label for the repaired instrument, that is a decision for the L1, not a defect of
  the file; as written it is a repair instrument, not a round-32 claim counter.

## 5. Scope and hygiene

* Nothing outside `/fast/scratch/hyaku/tameshi-r32-seats/RunCounterV2/` and this report file was written.
  No production file was edited; no `git` write command and no `jj` command was run in
  `/home/vgpnk/Projects/shokunin` or in the lane repo. The only git write was the `git clone` into this
  seat's scratch.
* All four runs used `--lane` pointing at this seat's clone and `--work` under this seat's scratch; the
  counter's own clones live under `<work>/`. The real fleet siblings were only read (the counter symlinks
  them into `<work>/fleet/` for the regression leg; the runner materialises from their object stores).
* All processes started by this seat exited before return (`ps` shows no remaining `RunCounterV2`
  process tree). Scratch footprint 1.5 GB; `/fast` had 88 GB free at the end.
* No tool was installed or upgraded for this item; the stock `git`, `python3` (3.14.8), `bash`,
  `diff` were sufficient.

## 6. Evidence index

| Claim | Where |
|---|---|
| v1 hash = contract `counter_sha256` | `.ufo/evidence/round-31/contract.json:14`; `sha256sum .ufo/evidence/round-31/c1-measure.py` |
| v2 hash = committed blob at freeze | `git show c318149:.ufo/evidence/round-32/repair/c1-r31-measure-v2.py \| sha256sum` |
| exactly 3 diff hunks | `diff -u` output; `difflib.SequenceMatcher` opcode enumeration |
| four run receipts | `<seat scratch>/runs/{v1-base,v1-head,v2-base,v2-head}/{stdout,stderr,exit,seconds}` |
| stdout byte-identical per pair | `diff` + `sha256sum` of the four stdout files |
| v1 reproduces the lane's committed receipt | `diff` against `.ufo/evidence/round-31/after/c1-at-final.stdout` |
| header selection inert on real data | table-classification enumeration over `git show <rev>:SCORECARD.md` |
| byte-prefix holds at both revs | raw `git show` byte comparison (118 152 B / 127 356 B) |
