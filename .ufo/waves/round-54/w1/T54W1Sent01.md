# T54W1Sent01 — sentinel attack: a forged reader report against the frozen C1 counter

Seat: `T54W1Sent01` · lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` ·
item: forge a reader JSON with a guessed `section_sha256`, no MD, run the frozen
C1 counter on a tree where the other arms pass, show the verdict stays false.
Everything ran on `git clone --shared` copies under
`$HYAKU_SCRATCH/tameshi-r54/T54W1Sent01/`; no lane file was edited, and the one
lane-side file I created (`T54W1ReadForged.json`) was deleted in the same
command that wrote it (bytes kept in
`T54W1Sent01-receipts/lane-forged-report-transcript.md`).

## 0. Verdict in one table

| # | tree (fixture commit) | counter bytes | arm 1 / arm 2 | arm 3 | arm 4 | verdict |
|---|---|---|---|---|---|---|
| a | lane at C0, no wave files | frozen `6a39b38` | 41 `RED` / 41,6 | dirs=[] | 0/7 | **false** total=4 |
| b | **A** binder-shaped re-key *directory* + synthetic 64-entry ledger + 7 fabricated reports with *true* shas, no MDs | frozen `6a39b38` | 64 `ok` / 64,8 | **dirs=[]** | 0/7 | **false** total=2 |
| c | A | amended `63f5f88` | 64 `ok` / 64,8 | dirs=[`rekey-r54-59c38109bf11`] | 7/7 | **true** total=0 |
| d | **B2** = A + zero-byte decoy file named `rekey-r54-<c0>` under `traces/`; the only report for `## Standing rules` carries a **guessed** sha | frozen `6a39b38` | 64 `ok` / 64,8 | dirs=[`rekey-r54-…`] (the *file*) | 6/7 | **false** total=1 |
| e | B2 (the item's tree) | amended `63f5f88` | 64 `ok` / 64,8 | dirs=[`rekey-r54-…`] | **6/7** | **false** total=1 |
| f | **C2** = B2 with the guess replaced by the sha `reader-section.py` prints | amended | 64 `ok` / 64,8 | 7/7 | 7/7 | **true** total=0 |
| g | **D** = C2 + a finding whose quote cannot occur in the section | amended | 64 `ok` / 64,8 | 7/7 | 7/7 | **true** total=0 |
| h | **E** = C2 + one post-C0 SKILL edit re-keyed at the *new* bytes, readers still pinned at C0 | amended | 64 `ok` / 64,8 | 7/7 | **6/7** | **false** total=1 |
| i | **F** = E with that one report's sha rewritten to the post-C0 bytes (`cand` still `59c3810`) | amended | 64 `ok` / 64,8 | 7/7 | 7/7 | **true** total=0 |

The answer to the assigned question is rows **d/e**: a guessed `section_sha256`
is the *only* thing arm 4 rejects, and the verdict stays **false** on a tree
whose other four arms are green. Rows **f–i** are what the same instrument does
with a report that was never read.

## 1. Method and byte anchors

Three commits of a scratch clone of lane C0 (`git clone --shared`, toplevel
asserted before every mutation):

* `783eab7` **A** — `.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11/traces/section-NN.json`
  (64 traces shaped exactly as `integrate/binder.py` writes them), a synthetic
  64-entry ledger whose `sha256` is each section's sha at C0 and whose inputs are
  `PROVINCE.md` at C0, and seven `T54W1ReadNN.json` reports carrying the true
  section shas, **no MDs, no reading**.
* `e6c643a` **B2** — A, minus `T54W1Read01.json`, plus `T54W1ReadForged.json`
  (heading `## Standing rules`, `cand` = C0, **guessed** sha), plus a zero-byte
  `traces/rekey-r54-59c38109bf11` file.
* `10ada0d` **C2**, `5222747` **D**, `2986c4c` **E**, `9ce447c` **F** — one-field
  edits, each receipted as its own patch.
* `bc6580b` **B** — a discarded intermediate, kept only as a receipt: its seven
  reports already covered every frozen heading, so the forged file was redundant
  and that run passed (`total=0`) without ever testing the guess. B2 replaced it;
  no verdict above depends on B.

Counter bytes used, hashed and stored as copies (never the live working tree,
which changed under me — §6):

```
6a39b38770e828aaa7624644169b07aed18f2f26477170c12d85a33799b1efec  code-frozen/c1/measure.py   (blob at C0 = freeze at 441c26be)
63f5f88147b898ee795dc925a04668d473c1fc845e370947307e3ea141a0b77b  code-amended/c1/measure.py  (amendment 1, HEAD 7883e0e)
a953d2e87116effc943f56a532b785cae8c8f44a104635083634c05fe0b8bb10  lost-headings-at-base.json (identical in both)
```

Every run: `python3 <copy>/c1/measure.py --lane <clone> --rev <rev> --work <empty> --explain`.

## 2. The assigned demonstration (rows b, d, e, f, g)

### 2.1 A guessed sha is rejected — and it is the only input that is checked

At B2 the forged file is the *only* report naming `## Standing rules`; the patch
is exactly two file changes. The operative lines are below; the complete patch
(header, `index` lines and the `-- ` signature included) is reproduced verbatim
at the end of this subsection and stored as `fixture-B2.patch`:

```diff
diff --git a/.ufo/waves/round-54/w1/T54W1Read01.json b/.ufo/waves/round-54/w1/T54W1Read01.json
deleted file mode 100644
--- a/.ufo/waves/round-54/w1/T54W1Read01.json
+++ /dev/null
@@ -1 +0,0 @@
-{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7", "findings": [{"quote": "T54W1Sent01 fabricated finding that never occurs in the section", "why": "fabricated"}]}
diff --git a/.ufo/waves/round-54/w1/T54W1ReadForged.json b/.ufo/waves/round-54/w1/T54W1ReadForged.json
--- a/.ufo/waves/round-54/w1/T54W1ReadForged.json
+++ b/.ufo/waves/round-54/w1/T54W1ReadForged.json
@@ -1 +1 @@
-{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7", "findings": []}
+{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "9942353c95371f27904c3a8ea2df7aedffd15ff8f03d9b05c07933fb9ee7b339", "findings": []}
```

Verbatim `fixture-B2.patch` (1252 bytes):

```
From e6c643adb8b64de05ed65407ce070506cc9912bf Mon Sep 17 00:00:00 2001
From: fixture <fixture@example.invalid>
Date: Wed, 28 Oct 2026 11:41:39 -0300
Subject: [PATCH] FIXTURE B2: forged report is the only report for its heading,
 sha still guessed

---
 .ufo/waves/round-54/w1/T54W1Read01.json     | 1 -
 .ufo/waves/round-54/w1/T54W1ReadForged.json | 2 +-
 2 files changed, 1 insertion(+), 2 deletions(-)
 delete mode 100644 .ufo/waves/round-54/w1/T54W1Read01.json

diff --git a/.ufo/waves/round-54/w1/T54W1Read01.json b/.ufo/waves/round-54/w1/T54W1Read01.json
deleted file mode 100644
index 65757f2..0000000
--- a/.ufo/waves/round-54/w1/T54W1Read01.json
+++ /dev/null
@@ -1 +0,0 @@
-{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7", "findings": [{"quote": "T54W1Sent01 fabricated finding that never occurs in the section", "why": "fabricated"}]}
diff --git a/.ufo/waves/round-54/w1/T54W1ReadForged.json b/.ufo/waves/round-54/w1/T54W1ReadForged.json
index a1ac9b3..c3a04aa 100644
--- a/.ufo/waves/round-54/w1/T54W1ReadForged.json
+++ b/.ufo/waves/round-54/w1/T54W1ReadForged.json
@@ -1 +1 @@
-{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7", "findings": []}
+{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "9942353c95371f27904c3a8ea2df7aedffd15ff8f03d9b05c07933fb9ee7b339", "findings": []}
-- 
2.56.0
```

`9942353c…` is `sha256("T54W1Sent01 forged guess, never read the section")`.

Verdict line (amended bytes, `mat-amended-B2.out`), the item's tree:

```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=e6c643adb8b6 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor exit=0 covered=64 score=8
EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
EXPLAIN arm4-readers 6/7
C1_R54: rev=e6c643adb8b6 c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=6/7 monitor=8/64 unstable=0 total=1 C1_R54_PASS=false
```

Same tree under the freeze bytes (`mat-frozen-B2.out`) is also false, and it
shows the second defect (§3) doing the work rather than arm 4:

```
EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
EXPLAIN arm4-readers 6/7
C1_R54: rev=e6c643adb8b6 c0=59c38109bf11 … rekeyed=7/7 readers=6/7 … total=1 C1_R54_PASS=false
```

### 2.2 One field, copied from the tool, flips the verdict

C2 changes only the 64 hex characters of `section_sha256` (`fixture-C2.patch`):

```diff
-{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "9942353c95371f27904c3a8ea2df7aedffd15ff8f03d9b05c07933fb9ee7b339", "findings": []}
+{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7", "findings": []}
```

```
C1_R54: rev=10ada0d5bc32 c0=59c38109bf11 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

That sha is printed by `python3 .ufo/waves/round-54/reader-section.py LANE 59c38109bf11 "## Standing rules"`
without reading one byte of the section. There is **no MD anywhere in the
fixture tree** and the counter never looks for one; `findings` is never
inspected, so D (a finding whose `quote` cannot occur in the section) still
prints `total=0 C1_R54_PASS=true` (`mat-amended-D.out`).

## 3. Finding S2 (high, **closed by amendment 1**): the freeze-bytes arm 3 could not see the binder's directory

`c1/measure.py` at C0 derived the re-key directory from *file basenames*:

```python
    tree = git(['-C', lane, 'ls-tree', '-r', '--name-only', rev,
                '.ufo/evidence/round-21/coldread/'], check=False).stdout.decode()
    rekey_dirs = sorted({Path(p).name for p in tree.splitlines()
                         if REKEY_RE.match(Path(p).name) and '/traces/' in p})
```

`ls-tree -r` lists blobs only, so no `Path(p).name` can ever be a directory.

* Fixture **A** is the layout `integrate/binder.py` actually writes
  (`trace_rel = '%s/traces/section-%02d.json'`): freeze bytes print
  `dirs=[] c0=None`, and because arm 4 keys on `c0`, one blind spot nulls two
  arms — `readers=0/7`, `total=2 C1_R54_PASS=false` (`mat-frozen-A.out`), with
  arms 1 and 2 already green.
* The **only** shape the freeze bytes accepted was a zero-byte file named
  `rekey-r54-59c38109bf11` inside `traces/` (row d): the counter reads the file's
  basename as the directory. That is a decoy no tool in the round emits.
* Round 53's counter had the mirror-image defect — the pathspec without a
  trailing slash prints the tree path itself, never its children
  (`arm3-detection.txt`): `git ls-tree --name-only C0 .ufo/evidence/round-21/coldread`
  → `.ufo/evidence/round-21/coldread`; with the trailing slash → the three
  `rekey-r53-*` directories. So neither round's arm 3 ever enumerated a
  `rekey-*` directory.
* Amendment 1 (`63f5f88`, HEAD `7883e0e`, recorded in both `freeze.json` and
  `contract.json`) matches the *directory component* of each traced path. I
  verified it independently rather than trusting the note: the same tree A
  moves from `dirs=[] / total=2 / false` to `dirs=['rekey-r54-59c38109bf11'] /
  readers=7/7 / total=0 / true` (`mat-frozen-A.out` vs `mat-amended-A.out`), and
  `git ls-tree -d --name-only <rev> .ufo/evidence/round-21/coldread/` lists the
  directory on the same tree (`arm3-detection.txt`).

Residual risk: an empty *directory* cannot exist in git, so `rekey-r54-<c0>/`
is only observable while it holds at least one blob — fine for the binder, but
the arm's "exactly one" count still silently ignores the 16 C0-only headings
(Crit02's fig-leaf finding, out of my scope).

## 4. Finding S1 (critical, open): arm 4 pins readers at C0 but compares them to REV bytes

`c1/measure.py` computes `sections` at REV and credits a report when
`d['section_sha256'] == sec['sha256']` **at REV** (line 240), while the contract
target, the wave spec and every seat's discipline pin the report at `<c0>`
(`"cand": "59c38109bf11…"`, bytes read at C0). The two agree only while
`SKILL.md` is unchanged after C0. It is not:

```
SKILL.md sha: C0=e0e0b4d0134f4555 99c3bc8=b5ff9727485da844 HEAD=b5ff9727485da844
sections changed C0->HEAD: 13/64
of the 23 re-read headings, changed after the readers read them: 13
frozen headings with NO satisfiable arm-4 report at HEAD: 5/7
```

(the 5: `## Standing rules`, `## Mutation-sweep recipe…`, `### The boundaries…`,
`### Using the ledger`, `### The operator's runbook…`; the two `Round-14`/
`Round-26` registry sections still match; full table in
`c0-pin-vs-deciding-rev.txt`.)

The fix pass `99c3bc8` landed at 11:38:37, six minutes after the first wave
deliverable (11:32:16) — it edited the sections the readers were told to read at
C0. At any deciding revision ≥ `99c3bc8` a report that truthfully pins C0 bytes
cannot equal the REV sha, and a report that pins the REV sha while naming C0 is
simply false. Two receipts:

* **E** — the best a competent wave can do: the edited section re-keyed at its
  *new* bytes (arms 1 and 2 still 64/64, arm 3 7/7), readers exactly as the spec
  demands → `readers 6/7 total=1 C1_R54_PASS=false` (`mat-amended-E.out`). No
  seat can fix that within its discipline.
* **F** — the same tree with that report's sha rewritten to the post-C0 value
  and `cand` left at C0 → `readers 7/7 total=0 C1_R54_PASS=true`
  (`mat-amended-F.out`). The passing report is provably false about its own
  `cand` (`cand-lie.txt`):

```
$ reader-section.py CLONE 59c38109bf11 "### Using the ledger"
{"heading": "### Using the ledger", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 946, "end": 977, "section_sha256": "808dad50760d693bc9e952a32a08cff129a74fd56163876aa3b656f9a9775d04"}
$ reader-section.py CLONE 9ce447c5 "### Using the ledger"
{"heading": "### Using the ledger", "cand": "9ce447c50971bf180c71a2a5fd10e0ef2d9e5e03", "start": 946, "end": 978, "section_sha256": "2b77db7324312f4ad88bf7952e0ec3e96c3acf3e93c0e7c609dd03ee9b5aedf7"}
$ git show 9ce447c5:.ufo/waves/round-54/w1/T54W1Read04.json
{"heading": "### Using the ledger", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "2b77db7324312f4ad88bf7952e0ec3e96c3acf3e93c0e7c609dd03ee9b5aedf7", "findings": []}
```

Exploit path, stated plainly: at the lane's HEAD the *honest* report shape is
uncreditable for 5 of the 7 frozen headings, and the *dishonest* shape is
credited. The instrument therefore selects for the forgery in §2 — a seat that
wants C1 green must copy the sha of bytes that did not exist at its own `cand`,
which is exactly what a forger does and exactly what a cold reader cannot do.
Combined with S3, `C1_R54_PASS=true` is reachable with zero reading.

Smallest remediations, in order of size:

1. **Arm 4 resolves the pin at the report's own `cand`** (which must equal `c0`
   and be an ancestor of REV), i.e. `sectionize(show(cand, 'SKILL.md'))`, and
   separately requires the heading to exist at REV. One predicate; matches the
   contract's own wording ("pins each section's bytes at `<c0>`") and mirrors
   arm 3, which already resolves at `read_rev`.
2. Or decide at a revision whose `SKILL.md` is the one the readers read: the 23
   headings must be re-read at the new content commit, which is a new wave, not
   an integration step.
3. Reverting the fix pass is *not* a remedy: it deletes the fixes the readers'
   findings demanded.

Until one of these is decided, the deciding invocation must not be run against
this target: it will be false for reasons no seat can repair, and the pressure it
creates is toward the §2 forgery.

## 5. Finding S3 (medium, open): arm 4 is a sha-copying check, not evidence of reading

* No MD is required, `findings` is never read, and there is no seat/nonce/author
  binding — a report is one line of JSON (rows f, g).
* `section_sha256` is obtainable with one command per heading
  (`reader-section.py`), which is the same command a legitimate reader runs.
* The only rejected input is a wrong sha (row d/e), so the arm distinguishes
  *copied* from *guessed*, never *read* from *fabricated*.

Smallest remediation: require the companion MD and at least one `findings`-free
attestation of *what was opened* (the reader's own `opened` list) to appear in
the MD, and bind the report to the seat's committed MD (`reports[]` already
exists in the ledger; the counter ignores it). This does not make forgery
impossible — nothing does — but it makes the cheapest forgery cost a document
that contradicts itself instead of one line of JSON.

## 6. Observation S4 (reproducibility, not a lane defect)

While this seat worked, the "frozen" bytes were live: amendment 1 was committed
at 11:44:51 (and legitimately recorded in both `freeze.json` and `contract.json`),
and `.ufo/evidence/round-54/c2/measure.py` and `.ufo/evidence/round-54/deciding-run.sh`
were modified in the working tree at 11:47 (`git status`, read-only). My first
baseline at 11:21 and my later runs therefore executed *different* counters.
Every number in §0 is re-derived from explicit byte copies whose sha256 are in
§1, and `mat-frozen-*` vs `mat-amended-*` are labelled accordingly. Any seat
receipt from this wave that invoked
`.ufo/evidence/round-54/c1/measure.py` by path is not byte-attributable without
its own copy; the deciding run should extract the counter from the freeze
manifest into scratch first (as `control/controls.sh` already does) and record
the sha in its verdict block.

## 7. What I did not find (sweeps that came back empty)

* A report for a heading **outside** the frozen seven does not credit: `arm 4`
  iterates `for h in frozen` only (code read, `c1/measure.py:235-242`).
* A single JSON cannot credit two headings: `readers` is keyed by the report's
  own `heading` string (same lines).
* A report whose `cand` is wrong but whose sha is right does not credit either
  (`d.get('cand') == c0` is conjunctive); row d proves the converse is also true
  — right `cand`, wrong sha, no credit.
* Garbage or unreadable JSON in the wave directory is skipped, not fatal
  (`except ValueError: continue`), so a forger cannot crash the arm into a false
  pass either.
* Arm 5's LOG.md/SCORECARD.md stability scan does fire on hand-bound entries —
  I did not need to use it: my fixture inputs are `PROVINCE.md` only, so
  `unstable=0` throughout and the row-a..i differences cannot be attributed to
  it.

## 8. Reproduction

```bash
export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r54/T54W1Sent01
mkdir -p "$S" && cd "$S" && git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin clone
cd clone && git rev-parse --show-toplevel          # must print the clone path
python3 <receipts>/fixture-build.py                # A, B, C
python3 <receipts>/build_followup.py               # B2, C2, D
python3 <receipts>/build_E.py                      # E
# F = E with T54W1Read04.json's sha set to 2b77db73…; see cand-lie.txt
# counter copies: code-frozen/c1 (6a39b38…) and code-amended/c1 (63f5f88…), §1
```

Scratch tree removed at the end of the seat; the two build scripts and every
patch are in the receipts directory, so the fixture is rebuildable from the
receipts alone.

## 9. Tooling and hygiene

* No installs (pacman transactions are paused host-wide; nothing needed):
  `python3` 3.13, `git` 2.56.0, coreutils.
* Lane writes: only `.ufo/waves/round-54/w1/T54W1Sent01.md` and
  `.ufo/waves/round-54/w1/T54W1Sent01-receipts/`. `T54W1ReadForged.json` in the
  wave dir existed for one command and was deleted (transcript + bytes
  receipted). No mutating git command outside the scratch clone; every clone
  mutation preceded by `git rev-parse --show-toplevel` == clone path.
* Scratch tree removed after the run; no `/tmp` artefacts.

## Receipts (`T54W1Sent01-receipts/`)

```
mat-frozen-C0.out mat-frozen-A.out mat-frozen-B2.out
mat-amended-A.out mat-amended-B2.out mat-amended-C2.out mat-amended-D.out
mat-amended-E.out mat-amended-F.out
arm3-detection.txt          # ls-tree forms, frozen vs -d, same tree
c0-pin-vs-deciding-rev.txt  # per-heading sha at C0 vs HEAD, 5/7 unsatisfiable
cand-lie.txt                # reader-section at cand vs at REV; the passing report
lane-forged-report-T54W1ReadForged.json  lane-forged-report.sha256  lane-forged-report-transcript.md
fixture-{A,B,C,B2,C2,D,E,F}.patch         # exact bytes of every fixture commit
fixture-build.py  build_followup.py  build_E.py
```

`fixture-A.patch` is 7.3 MB because it *replaces* the 568-entry historical
round-21 ledger with the fixture's 64 entries, so the diff carries the old file
in full; the other patches are 1–2 KB.
