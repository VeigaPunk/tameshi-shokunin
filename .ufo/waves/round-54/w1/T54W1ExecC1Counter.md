# T54W1ExecC1Counter — C1 instrument verification (frozen round-54 counter)

Seat: `T54W1ExecC1Counter` · item: *"Attack nothing; verify the instrument."* · lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only for this seat) ·
scratch `$HYAKU_SCRATCH/tameshi-r54/T54W1ExecC1Counter` (removed at exit, §H).

The counter under test: `.ufo/evidence/round-54/c1/measure.py`. Its bytes changed **during
this seat's session** (L1 landed amendment 1), so every run below records the sha256 of the
instrument bytes it actually executed:

| bytes | sha256 | in force |
|---|---|---|
| C0 freeze | `6a39b38770e828aaa7624644169b07aed18f2f26477170c12d85a33799b1efec` | `59c38109` … amendment 1 |
| amendment 1 | `63f5f88147b898ee795dc925a04668d473c1fc845e370947307e3ea141a0b77b` | `7883e0e` (11:44:51) … HEAD `097985c` |

Both were verified byte-identical to the tracked blob at the revision each run names
(`sha256sum` of working tree vs `git show <rev>:<path>`), except where noted.

---

## R1 — the commanded run at C0 (`--explain`)

Command (contract form, absolute paths, empty scratch work dir):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 59c38109bf119d0e9d4f878644a82babc937bc1e \
  --work $HYAKU_SCRATCH/tameshi-r54/T54W1ExecC1Counter/w0 --explain
```

**A. C0-frozen bytes (`6a39b387`)** — exit 1:

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=59c38109bf11 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

**B. Amendment-1 bytes (`63f5f881`)** — same arm outcomes, exit 1 (re-run at 14:49Z because
the bytes changed under the session):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=59c38109bf11 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

Verdict at C0 is therefore `C1_R54_PASS=false`, `total=4` (one per arm), exactly the
contract's "before" shape (`credited=57 lost=7` at base is *better* than C0's 41 — the
drift C0 introduced). The `before` file in the contract quotes `credited=57 lost=7`; this
run confirms C0's own regression to 41/23 as the wave context states.

## R2 — arm by arm: why each arm fails at C0

**arm1 (frozen round-48 precheck, bytes at REV, sha `3b07847afc86…`).** It compares the
credited set at floor `ef19d8e1` (64/64) against the credited set at `59c38109`. The 23 lost
sections, from the frozen selector at C0 (`--explain`, distilled in
`T54W1ExecC1Counter-receipts/c0-lost-sections.json`):

- 4 are `no-ledger-entry` — the section's bytes changed at C0, so no entry's `sha256`
  matches the section any more: `## Standing rules` (C0 added the three-arm scratch-root
  bullet), `### The boundaries — what a service run is not`, `### Using the ledger`,
  `### Round-26 gate/probe registry — report interop`.
- 19 are `input-drift:…` — entries still key to the section's bytes, but inputs C0 rewrote
  no longer hash to the pin: `corpus/SOURCES.md`, `tools/bash-witness-study.py`,
  `tools/env-diff.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`,
  `tools/registry.json`, `tools/registry-check.py`, `corpus/knowledge/service-limits.md`,
  `LOG.md`, `SCORECARD.md`, plus two round-15/round-21 receipts. Example, verbatim from the
  selector: `### The tick and the pin read | input-drift:tools/pin-disposition.py`.
- **No section is vetoed** (`vetoed` false on all 23; `unstable=0` because no arm-vs-`LOG.md`
  entry is under a `rekey-r54-*` trace path — there is no such dir yet).

**arm2 (unchanged round-21 selector at REV).** `covered=41` is the same 41 sections. The
score is 6, not 8, by `restraint = 2*Σ(boxes 1,2,4 marked ~) + 2*box3_points` with
`box3_points = box3_marked and box3_link and cr['box3_full_page']`, and
`box3_full_page = sections_covered == sections_total` (r18 `measure.py:678-687,695-699`).
Three boxes are asserted → 6; box three is worth the other 2 only when all 64 credit. So
`score=8` is a *consequence* of `covered=64`, not an independent gate — it cannot be
reached while the credit arm is short, and it follows automatically once it is not.

**arm3 (re-key directory).** Correctly empty at C0: `git ls-tree -r --name-only
59c38109 .ufo/evidence/round-21/coldread/` contains **0** paths under any `rekey-r54-*`
dir and 3 round-53 dirs (`rekey-r53-651773ab9e32`, `rekey-r53-a41195dfc13a`,
`rekey-r53-a9773948087e`). So `dirs=[]`, `c0=None`, `rekeyed=0/7`. *The reason it was empty
is right; the reason the code computed it was wrong — see R4.*

**arm4 (reader reports).** `0/7` for two independent reasons: (i) at C0 the wave directory
holds no reader report at all — `git ls-tree -r 59c38109 .ufo/waves/round-54/w1/` prints
nothing (the wave started after C0, and every reader report on disk now is uncommitted, so
invisible to the counter, which reads `ls-tree` at REV); (ii) arm4 is gated on `c0`
(`if d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']`), so while arm3
yields `c0=None` no reader JSON can ever match, whatever the wave writes.

## R3 — second run with a pre-populated work dir: it refuses

```
$ : > $S/wx/sentinel
$ python3 …/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 59c38109bf119d0e9d4f878644a82babc937bc1e --work $S/wx --explain
C1_R54: error=work-not-empty total=1 C1_R54_PASS=false
EXIT=2
$ ls -a $S/wx
.  ..  sentinel
```

Verdict: refuses before running any arm (no precheck invocation, no scratch written, the
sentinel untouched), exit 2, and the message names the class. The empty-dir run leaves only
`coldread-precheck.sh`, `mirror/`, `r18measure.py`, `__pycache__` under `--work`; `TMPDIR` is
pointed at `--work` for the children, and the frozen precheck's own scratch lands under
`$HYAKU_SCRATCH/tameshi-r48/` and is removed by its trap (checked: the dir was empty again
after the runs). No `/tmp` writes observed.

## R4 — FINDING F1 (critical, now fixed by amendment 1): arm3 could not see a re-key directory

C0 bytes, `measure.py:172-175`:

```python
tree = git(['-C', lane, 'ls-tree', '-r', '--name-only', rev,
            '.ufo/evidence/round-21/coldread/'], check=False).stdout.decode()
rekey_dirs = sorted({Path(p).name for p in tree.splitlines()
                     if REKEY_RE.match(Path(p).name) and '/traces/' in p})
```

`ls-tree -r` lists **blobs only**, so `Path(p).name` is always a file basename
(`1.json`), never the directory name; `REKEY_RE` (`^rekey-r54-([0-9a-f]{12})$`) therefore
can never match, and `rekey_dirs` is `[]` at *every* revision. Receipt, on a clone that
carries a correctly laid-out re-key dir:

```
$ git -C $D ls-tree -r --name-only 5b24aab1a72e .ufo/evidence/round-21/coldread/ \
    | grep -c 'rekey-r54-59c38109bf11/traces/'
23
$ git -C $D ls-tree -r --name-only 5b24aab1a72e .ufo/evidence/round-21/coldread/ \
    | python3 -c 'import re,sys;from pathlib import Path;RE=re.compile(r"^rekey-r54-([0-9a-f]{12})$");ps=[l for l in sys.stdin.read().splitlines() if l];print(sorted({Path(p).name for p in ps if RE.match(Path(p).name) and "/traces/" in p}))'
[]
# same paths, matched as a path COMPONENT:
['rekey-r54-59c38109bf11']
```

C0-frozen counter at that revision: `arm3-rekey dirs=[] c0=None … rekeyed=0/7 … total=2`
(R1/R6-A). Blast radius: `c0=None` also zeroes arm4, so the counter was pinned at
`total >= 2` at every revision and could never print `C1_R54_PASS=true`; `controls.sh`
phase B pre-registers `CTL_POS_c1 true`, so the control would have mismatched by
construction. Provenance: round 53's counter used a **non-recursive** `ls-tree --name-only`
(which lists the directory entries) and `re.fullmatch` on the name — correct there; the
round-54 "recursive listing" fix kept the basename match and lost the directories.

Status: L1's **amendment 1** (commit `7883e0e`, 11:44:51 −0300) replaces the two lines with a
path-component match — behaviourally identical to the control copy I had patched from the
C0 blob (`T54W1ExecC1Counter-receipts/ctrl.patch`, `ctrl-measure.py`), and `freeze.json`
now pins `63f5f881…`. Independently reproduced finding; no action requested.

## R5 — FINDING F2 (open, precision hazard): arm3 and arm2 disagree about the round-21 ledger as an input

The counter evaluates re-key entries with the **raw** round-18 module
(`measure.py:210`: `r18_mod.entry_reason(lane, rev, e, True)`), whose self-referential set is

```
$ python3 -c "…; print(sorted(m.IGNORED_INPUTS))"
['.ufo/evidence/round-17/coldread/ledger.json', '.ufo/evidence/round-18/coldread/ledger.json', 'SKILL.md']
```

while arm2 runs the round-21 selector, which adds the round-21 ledger itself:

```
module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))   # c1/measure.py mirrors this path
```

The round-18 module's own comment says *"either round's ledger is its own output"*, but the
default only carries the round-17 and round-18 paths. Consequence: an entry that records
`.ufo/evidence/round-21/coldread/ledger.json` as an input **always drifts in the very commit
that writes the re-key**, so it can never credit in arm3. Receipt, on the probe revision
(`6dbc834`, entries that pin the ledger):

```
$ python3 - <<'PY'   # entry_reason under arm3's gate, then under arm2's IGNORED set
entries that fail arm3 only because they pin the round-21 ledger: 2
   ## Mutation-sweep recipe — numbered steps; bounded cold-read   ledger sha 3a086406768e
   ### Round-21 gate/probe registry — finite environment differ   ledger sha 3a086406768e
  with r21 IGNORED set -> reason = None
  with r21 IGNORED set -> reason = None
```

End-to-end effect, counter at `6dbc834` (amendment-1 bytes): `rekeyed=6/7`; after dropping
only that pin (and the arm-5-unstable pins) at `d2ac3e8`: `rekeyed=7/7`. Blast radius on the
real ledger at C0: **6 of 568** entries pin the round-21 ledger, **0** of those pins equal
the C0 ledger sha — i.e. every such entry is uncreditable now and would be again after a
re-key that records it. So a binder following house style (recording the ledger among the
inputs) silently loses one of the seven, and the arm's `cannot_see` note will call it a
reader failure. Cheap fix if L1 wants it: add the round-21 ledger to the counter's ignored
set before `entry_reason` (or evaluate arm3 through the same wrapper the monitor uses).
Not fixed by amendment 1, which touched only discovery.

## R6 — can the instrument reach the target at a later revision with **entries only**?

Probe (all in a `git clone --shared` at `$S/reach/lane`, `rev-parse --show-toplevel`
asserted before every mutation; fixtures `probe.py`, `probe_readers.py`, `refine.py` in the
receipts dir):

1. `5b24aab1a72e` — **entries only.** 23 synthetic entries, one per section lost at C0,
   keyed by that section's sha at C0, `read_rev` = full C0, one trace receipt each under a
   single `.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/…` dir. Delta vs
   C0: `24 files changed` = `ledger.json` + 23 traces; `SKILL.md` diff is **0 lines**, and
   `sha256(SKILL.md)` is `e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9`
   at both revisions.
   - frozen selector at that rev: `selector covered=64 score=8`, `still-lost=0`.
   - counter, C0-frozen bytes: `arm3 dirs=[] … rekeyed=0/7 … total=2` (F1).
   - counter, amendment-1 bytes: `arm1 ok (64/0)`, `arm2 covered=64 score=8`,
     `arm3 dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf11`, `rekeyed=6/7` (F2 — those
     entries pin the ledger and `LOG.md`/`SCORECARD.md`), `readers=0/7`, `total=3`.
2. `6aad88551bf0` — **entries only, cleaned.** Same entries with the ledger/`LOG.md`/
   `SCORECARD.md` pins dropped, no wave reports (`git ls-tree … .ufo/waves/round-54/w1/`
   → 0 files):
   ```
   EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=6aad88551bf0 cand_credited=64 lost=0 ok
   EXPLAIN arm2-monitor exit=0 covered=64 score=8
   EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
   EXPLAIN arm4-readers 0/7
   C1_R54: rev=6aad88551bf0 c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=0/7 monitor=8/64 unstable=0 total=1 C1_R54_PASS=false
   ```
3. `d2ac3e8` — the same entries **plus** seven committed reader-shaped JSONs under
   `.ufo/waves/round-54/w1/T54W1SynthRead01-07.json` (heading, `cand` = C0, section sha
   recomputed at REV; verified MATCH on all seven):
   ```
   EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
   EXPLAIN arm4-readers 7/7
   C1_R54: rev=d2ac3e8 c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
   EXIT=0
   ```
   (Run at 14:47Z, after amendment 1 had landed; the same revision under my one-line-patched
   control copy gave the identical `PASS=true, EXIT=0` — that is what isolates F1 as the
   only thing that had been blocking it.)

**Answer.** *Entries only are not sufficient*: entries + their traces green arms 1, 2, 3 and
5 (the `unstable` arm) on their own — `rekeyed=7/7`, `unstable=0`, `credited=64`,
`score=8` — but arm 4 needs seven **committed file artifacts** (reader JSONs), which no
ledger entry can supply, so entries-only tops out at `total=1`, `PASS=false`. With the seven
reader reports committed, the target is reachable and was reached on the probe
(`total=0`, exit 0). Under the C0-frozen bytes it was reachable *by nothing*, because of F1.
Two sub-gates the binder must respect, both measured: (a) do not pin `LOG.md` or
`SCORECARD.md` (arm 5 counted 4 such pins on the ledger-pinning probe and refused —
`unstable=4`); (b) do not pin the round-21 ledger, or arm 3 will refuse (F2).

## R7 — properties of the instrument verified along the way

- **Frozen-ness is a property of the runner, not of the command.** The documented
  `python3 .ufo/evidence/round-54/c1/measure.py …` executes the *working-tree* bytes (it
  loads `lost-headings-at-base.json` from `Path(__file__).parent`), which is how this seat
  observed the instrument change under it mid-session. `deciding-run.sh` is the component
  that extracts the REV bytes into `$SCR/code/` and diffs the frozen paths — that invocation
  is insulated; the standalone one is not. Anyone quoting a verdict should record the
  instrument sha (as R1 does).
- **arm4 reads JSON only, never the MD and never `findings`.** The seven probe JSONs carry
  `"findings": []` and a `"probe": …` marker and still counted `7/7`, so the counter cannot
  distinguish a defended cold read from an empty placeholder; adjudicating findings is
  outside what it can see (consistent with the contract's `cannot_see`).
- **Freeze integrity at HEAD `097985c`**: 10/10 manifest entries hash to their working-tree
  bytes. Note the manifest mixes key roots after 097985c — round-54 evidence keys are
  round-relative (`c1/measure.py`), inherited counter bodies are repo-relative
  (`.ufo/evidence/round-18/measure.py`); a verifier that joins every key to the round dir
  will read three false mismatches (this seat did, then corrected).
- `lost-headings-at-base.json` is the frozen 7, and all seven are among the 23 lost at C0,
  so arm 3 and arm 4 are both asking about a subset of the credit deficit — no section can
  pass arm 4 while failing arm 1.

## H — hygiene

No lane file was edited: the only paths this seat wrote are
`.ufo/waves/round-54/w1/T54W1ExecC1Counter.md` and
`.ufo/waves/round-54/w1/T54W1ExecC1Counter-receipts/` (`probe.py`, `probe_readers.py`,
`refine.py`, `ctrl.patch`, `ctrl-measure.py`, `c0-lost-sections.json`). All revisions were
built in `git clone --shared` trees under `$HYAKU_SCRATCH` with `rev-parse --show-toplevel`
asserted first; no `git` command was run against the lane except read-only `show`/`ls-tree`/
`diff`/`log`/`status`. Scratch tree `$S` removed on exit. No tool installs were needed
(`python3` 3.14, `git`; no pacman transaction).
