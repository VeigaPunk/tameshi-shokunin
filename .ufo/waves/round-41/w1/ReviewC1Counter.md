# ReviewC1Counter — round-41 C1 counter

Seat: reviewer (read-only). Only write: this file. Lane checkout untouched; scratch under
`/tmp/tameshi-r41-c1counter/`.

## 0. What was reviewed (the instrument moved during the review)

`.ufo/evidence/round-41/calibration/measure.py` was rewritten by another seat while this review
ran. Four artifacts exist for the same claim:

| artifact | sha256 | status |
|---|---|---|
| HEAD blob at freeze `d4ee4e6` | `f00917dd…` | the original `contract.json` pin; reads status from `cells[9]` |
| worktree 03:39–03:40 | `f00917dd…` | identical to HEAD |
| worktree since 03:40 | `5ccb42d8…` | `cells[9]→cells[8]` (amendment A1) |
| worktree 03:4x | `8bc9b422…` | + A4 (`os.path.exists`, `rstrip('/')`); **this is the current `contract.json` pin** |
| worktree 03:44:59 | **`9aaa99ac…`** | + an **undeclared** m9 rule change (derived words) |

Current state as of 2026-10-25T03:46:32-03:00: `contract.json` pins `8bc9b422…`; the file on disk is
`9aaa99ac…`. The contract now
carries amendments `A1, A2, A3, A4`, none of which describes the m9 derivation change that is in the
file on disk:

```
python3 -c "import json;c=json.load(open('.ufo/evidence/round-41/contract.json'));print(c['claims']['C1']['counter_sha256']);print([a['id'] for a in c['amendments']])"
  → 8bc9b4221c59c7b380892b7f97885e9b8ada1f5d82b0703effa166f0519ce11c   ['A1','A2','A3','A4']
sha256sum .ufo/evidence/round-41/calibration/measure.py
  → 9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd
```

Every finding below was executed twice: against the frozen `f00917dd…` copy (extracted with
`git show d4ee4e6:.ufo/evidence/round-41/calibration/measure.py`) and against the current
`9aaa99ac…` snapshot. Each finding carries its status under the current snapshot.

Verified repo facts, re-checked rather than inherited: at base `a3d6c69` the registry holds 107 rows,
107 unique ids, max `S152`, statuses **79 mined / 22 queued / 6 rejected** (column 8). In the
worktree it holds 109 rows / 109 distinct ids, statuses **81 mined / 22 queued / 6 rejected**;
`S153` and `S154` are `mined`, both dated 2026-10-25. Both snapshot sha256 values in
`corpus/lessons/round-41.md` are as the lesson states.

---

## P0 — the claim is scored by an instrument the predicate does not authenticate

**P0-1. `C1_R41_PASS` has no counter-pin clause and the counter never checks its own bytes.**
`contract.json` `claims.C1.predicate` is only "m6, m7, m8 and m9 all count 0", while `claims.C2`
requires "the committed v3 tool matches its contract pin". The C1 counter contains no hash check:

```
grep -n "sha256\|hashlib\|counter_sha\|__file__" .ufo/evidence/round-41/calibration/measure.py
  (no output)
```

Consequence, right now: the contract pins `8bc9b422…`, the file is `9aaa99ac…`, and the counter
still prints `C1_R41_PASS=true` on the worktree. Any edit to the instrument is inherited by the next
run with no clause failing; the pin is enforced by nothing but a reviewer typing `sha256sum`. This
is the same class the lane already carries as round-35's `m4 frozen-contract pin`, and round 41 does
not re-check it. **Fix shape:** C1's predicate must state that the counter's own sha equals
`claims.C1.counter_sha256`, and the counter must print its own sha in its verdict line.

**P0-2. The tool on disk contains an undeclared rule change.** The m9 correction test now derives
the expected words from the table (`measure.py` m9 block: `counts = {v: k for k, v in WORDS.items()}`
/ `want_refused` / `want_present`). That is a real tightening — it closes the hardcoded-literal hole
this review found at `f00917dd…` — but no amendment records it, and it is not the pinned artifact.
An instrument change introduced and left undeclared during a freeze is exactly what the round-35
pin class exists to catch; here nothing in the tool can catch it. Either declare it as `A5` with a
new pin, or revert it; do not run a deciding measurement on `9aaa99ac…` while the pin says
`8bc9b422…`.

**P0-3. The round-41 SCORECARD already contradicts the contract on the amendment count.** Line 1903
of `SCORECARD.md` states "three pre-data amendments are recorded there (A1 …, A2 …, A3 …)" while the
contract holds four (`A1`–`A4`). This is precisely the record-vs-state drift C1 claims to reconcile,
inside the section C1's own scorecard evidence sits in, and none of m6–m9 can see it. Severity is
`A4`/the SCORECARD prose, not the predicate — but the deciding run should not leave a stale count in
the record that the claim certifies.

## P0 — PASS is reachable with an empty audit surface

**P0-4. Every input is optional; absence prints PASS.** `round41_records` drops `None` and empty
parts (`measure.py:142-146`); missing files become `''` (`:209,:215`); `m6` is skipped when no
standing row exists (`:217`); `m9` is skipped when the round-40 lesson is absent (`:245`); the
verdict is "no mismatch strings" (`:266-276`). `records=` is printed but never gated.

```
python3 /tmp/tameshi-r41-c1counter/pinned_9aaa.py --lane /tmp/tameshi-r41-c1counter/f1_empty --rev HEAD
  C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=0 … C1_R41_PASS=true     [STANDS]
python3 … --lane /tmp/tameshi-r41-c1counter/allabsent --rev HEAD
  C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=0 sources_rows=0 … C1_R41_PASS=true   [STANDS]
```

A lane consisting of one README scores PASS on all four classes. This is not academic: the base
revision itself prints `records=0` (no round-41 file, neither round-41 head present), so before this
wave m7 and m8 were 0 by construction, and a renamed head reproduces that state
(`m7_nohead`: `## Round Forty-One` + em-dash-less LOG head → `records=0`, PASS). **Fix shape:** gate
the verdict on `len(records) == 3` (lesson + SCORECARD section + LOG section) and on
`sources_rows > 0`, and print a distinct `SETUP` verdict, as the counter already does for an
unresolvable `--rev`.

## P1 — class surfaces that do not cover the claim

**P1-1. `m8` audits four prefixes plus seven bare filenames** (`measure.py:46-51,52-60,183-190`).
One fixture citing fifteen nonexistent repo-relative paths flagged three:

```
flagged:   corpus/nope.md   tools/nope.py   .ufo/evidence/round-41/nope.json
invisible: docs/nope.md  scripts/nope.py  assets/missing.png  src/gone.ts  measure.py
           calibration/measure.py  .ufo/evidence/round-40/nope.json  corpus/lessons/round-*.md
```

A path from the *wrong round* (`.ufo/evidence/round-40/…`) escapes. The contract says "a
repo-relative path that does not resolve at the measured revision"; the code audits an allowlist.
`tools/`, `corpus/` and `.ufo/evidence/round-41/` are the only directories ever checked.

**P1-2. `m8` tokenisation excludes far more than it admits** (`:183-190`). Only single-backtick
tokens are read; tokens containing `,`, `(`, `)`, `*`, `{`, `}`, `|`, `…` or a space are dropped.
Unbackticked prose paths, markdown link targets and unbackticked table cells are invisible;
`tools/x.py:12-14,20` is dropped by the comma; globs by `*`; and an `#L` anchor is not stripped:

```
MISMATCH m8 corpus/anchor-gone.md#L12 cited but does not resolve      [STANDS, false positive]
```

Directory citations now pass by design (`corpus/lessons/` and `corpus/lessons` both resolve), so
`m8` certifies a *name exists*, not that a file exists: `git cat-file -e rev:path` succeeds for a
tree and `os.path.exists` for a directory. A cited directory is not the claim "this path resolves".
[STANDS]

**P1-3. `m6` binds to the last matching row and to one spelling** (`:216-218`). `SCORECARD.md`
carries four `| sources-registry |` rows (240, 1514, 1609, 1851) and only 1851 is compared. A
bolded name (`| **sources-registry** |`) or a count phrased `… entries` skips the class entirely
while the row is stale. Both fixtures printed `m6=0 … PASS` under the frozen counter; the m6 block
is unchanged in `9aaa99ac…`, so the class still reads only `standing[-1]`. [STANDS]

**P1-4. `m6` compares a stated count against distinct parsed ids, not rows** (`:130-139,211`:
`len(rows)` over a dict). Four physical rows with a duplicate id → `sources_rows=3`; a row saying
`3 rows` passes. Rows written as list items, indented more than three spaces, or with four-digit ids
are not counted at all: three physical rows scored `sources_rows=2` and a `2 rows` claim passed.
Today the registry happens to be 109 rows / 109 distinct ids, so the discrepancy is latent, not
live. [STANDS]

**P1-5. `m9` is silenced by removing evidence from the round-40 record** (`:245-248` requires both
`table` and `summary` non-`None`):

```
no ### Quarantine section     → m9=0 … PASS   (table absent)
no summary sentence           → m9=0 … PASS   (table present, summary gone)
```

`quarantine_summary` is one first match over whitespace-flattened text (`:168-181`), so a correct
sentence placed before a wrong closing sentence masks it (`m9_mask`: round-40 ends with "Seven
refused and nine present was the shape of it." and the counter reports `m9=0`). And `### Quarantine`
is a prefix match, so `### Quarantined sources` is accepted as the section. Requirement for the
deciding run: the round-40 `### Quarantine` section must still be present with its 17 verdict rows
intact — `m9=0` alone does not prove the contradiction was corrected. [STANDS]

**P1-6. `m9` accepts a restatement as a correction, and reads the whole lesson file** (`:249`).
`correction = read(lane, rev, LESSON)` is not scoped to the round-41 section, so the words may sit
in any appendix (`m9_appendix` → `m9=0`). With the derived-word form now on disk, an echo such as
"the round-40 lesson said six refused and ten present" clears the class without asserting that the
table is the record (`m9_echo` → `m9=0`; the table is indeed 6/10, so the class behaves as written
but certifies less than "the contradiction is corrected"). [STANDS]

**P1-7. `m7` still misses real citation spellings and over-matches others** (`:44,229-236`),
independent of the column fix:

```
invisible: S42 (2 digits)   s002 (lowercase)   S 003 (space)   S–001 (en dash)
flagged:   S0001, S0020 (4 digits → treated as ids the registry lacks)
```

`S_CITE_RE = \bS(\d{3,})\b` is case-sensitive and requires ≥3 digits. Bold, table-cell, comma-list
and en-dash-range spellings are otherwise covered (verified: `**S999**`, `| S998 |`, `S997,S996`,
`S995–S990` all flag). Since a 2-digit or lowercase citation is a real way to write a real id, the
class can under-count; since a 4-digit token is not an id, it can over-count. [STANDS]

## P2 — measurement identity

**P2-1. No pin on the revision or the tree.** `:195-208` accepts any `--rev`, resolves it with
`git rev-parse`, and reads the working tree for `--rev work`. Nothing asserts the resolved sha is
the measurement revision, nothing asserts a clean tree. The same lane therefore scores PASS/FAIL by
flag alone (`revwork`: committed HEAD clean → PASS `records=0`; dirty worktree → the citation is
found). The contract's kill rule is prose; the verdict line prints `rev=work` with no sha, so a
reviewer cannot tell a deciding run from a pre-check. [STANDS]

**P2-2. Any `--lane` is accepted.** `:200` only calls `os.path.abspath`; no remote, path or commit
identity is checked. All fixture evidence in this report is a working demonstration that a
directory with matching text scores the verdict.

**P2-3. No `--control` / `--selftest`; `--fleet` is dead.** `:194-198` defines only
`--lane/--rev/--fleet`, and `--control` exits 2 with "unrecognized arguments" (verified on the
current snapshot). `--fleet` is parsed and never read. The counter therefore has no ingested
control and no self-test — the contract's do-nothing control is reproducible only by hand, which is
why the two mutations a sibling seat planted (`quarantine_counts` self-comparison, m8 filter
disable) are caught by nothing but the hash pin. [STANDS]

**P2-4. `read()` treats any git failure as absence** (`:96-113`), so a mistyped constant, a moved
file or a non-repo lane silently shrinks the audit surface instead of erroring — and by P0-4 a
smaller surface is a PASS. [STANDS]

**P2-5. Docstring/flag drift.** `:6` documents `--mode work`; the flag is `--rev`. [STANDS]

## P3 — count semantics and scoping

**P3-1. Counts are mismatch lines, not defects** (`:228-240`). One bad id cited in lesson +
SCORECARD section + LOG section yields `m7=3`; one bad path in two records yields `m8=2`. `total` is
not a defect count and the class numbers are not comparable to each other. [STANDS]

**P3-2. `section()` returns head-to-EOF** (`:120-125`, `text[idx:]`), so everything after
`## Round 41` in SCORECARD belongs to the round-41 record. A later `## Round 39 (archive)` section
citing `tools/gone-in-39.py` is reported as an `m8` failure against round 41 (`m8_tail`), and a
later round's `S999` as `m7`. Head matching is substring, so `## Round 410` also matches. Today the
round-41 section is the last thing in the file, so the exposure is latent. [STANDS]

**P3-3. A head rename silently removes a record and its PASS** (`m7_nohead` → `records=0`, PASS).
Same hole as P0-4, reached by editing one heading. [STANDS]

## Status of the two P0s this review opened earlier

| earlier finding | status under `9aaa99ac…` |
|---|---|
| `m7` read status from `cells[9]` (the `opened` date), so every mined citation failed | **FIXED** by declared amendment `A1` (`cells[8]`); verified: mined passes, `queued`/`rejected` flag correctly, and the base-state line is byte-identical (`m6=1 m9=1 total=2`), so `before` stays valid |
| `m9`'s correction gate was three hardcoded strings (`round-40`, `six refused`, `ten present`), so a table of 7/9 with a summary of 8/6 cleared on words matching neither | **FIXED in the worktree, but undeclared and unpinned** (P0-2). Verified: the same fixture now scores `m9=1` |

## Residual risk / verification gaps

- I did not run the counter in default mode at the measurement revision; the deciding run is the
  L1's. Base-revision and `--rev work` runs only, per the kill rule.
- The instrument changed four times during this review. Every finding above was re-executed on the
  `9aaa99ac…` snapshot; if the file changes again before the deciding run, only the findings marked
  [STANDS] survive unchanged, and the pin question (P0-1/P0-2) must be re-asked.
- Fixtures are synthetic lanes; their purpose is to show classifier behaviour, not to score the real
  lane. The real-lane pre-run at `9aaa99ac…` printed `m6=0 m7=0 m8=0 m9=0 total=0 records=3
  sources_rows=109 C1_R41_PASS=true rev=work` — a pre-check, not the measurement.
- No tool was installed or upgraded (pacman transactions are paused host-wide).

## Verdict

Against the contract as written and the artifact currently on disk, `C1_R41_PASS=true` still does
not imply the claim. Even after A1 and A4, it is reachable by: an instrument that matches no pin
(P0-1/P0-2), an empty audit surface (`records=0`, P0-4/P3-3), a stale standing row in a
bolded/renamed/duplicated form or a duplicated registry id (P1-3/P1-4), an `m8` allowlist that
cannot see most repo-relative paths (P1-1/P1-2), and an `m9` that is silenced by deleting the
round-40 summary or by an echo of numbers the counter now derives (P1-5/P1-6). The m7 column defect
that made C1 unpassable for any citing record is fixed and declared; that was the round's one
blocking instrument bug, and the remaining work is to pin what runs, gate absence, and widen the
two allowlists. Recommendation: no `C1_R41_PASS=true` should be admitted until the counter's sha is
asserted inside the predicate, `records=0` is a failure, and the round-40 `### Quarantine` table is
verified present.

## Appendix — self-contained reproduction (scratch is not evidence)

Scratch was swept in another lane during this wave, so the fixtures are reproduced here. Build once,
then run the snapshot under test against each lane:

```python
import os, subprocess, shutil
ROOT = "/tmp/tameshi-r41-c1counter"; shutil.rmtree(ROOT, ignore_errors=True); os.makedirs(ROOT)
COUNTER = "/tmp/tameshi-r41-c1counter/pinned.py"   # snapshot under test, hashed first
def row(i, st): return "| S%03d | source | docs | A | scope | anchor | teaches | %s | 2026-10-19 | 180d | corpus/knowledge/x.md |" % (i, st)
def make(name, files):
    lane = os.path.join(ROOT, name); os.makedirs(lane)
    for p, c in files.items():
        f = os.path.join(lane, p); d = os.path.dirname(f)
        if d: os.makedirs(d, exist_ok=True)
        open(f, "w").write(c)
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    for cmd in (["git","init","-q",lane], ["git","-C",lane,"add","-A"], ["git","-C",lane,"commit","-qm","fx"]):
        subprocess.run(cmd, check=True, env=env, capture_output=True)
    return lane
REG = "## Registry\n\n" + "\n".join(row(i, "mined") for i in (1,2,3)) + "\n"
# P0-4: no round-41 record -> PASS
make("f1_empty", {"corpus/SOURCES.md": REG, "SCORECARD.md": "# S\n", "LOG.md": "# L\n"})
# P1-3: row spelling skip and last-row authority
make("f2_bold-name", {"corpus/SOURCES.md": REG, "SCORECARD.md": "# S\n\n| **sources-registry** | 103 rows |\n"})
make("f2_entries-not-rows", {"corpus/SOURCES.md": REG, "SCORECARD.md": "# S\n\n| sources-registry | 3 entries |\n"})
make("f2_dupe-last-right", {"corpus/SOURCES.md": REG, "SCORECARD.md": "# S\n\n| sources-registry | 103 rows |\n| sources-registry | 3 rows |\n"})
# P1-4: duplicate id collapses to 3 distinct while the row says 3
make("m6_dup", {"corpus/SOURCES.md": "## Registry\n\n" + row(1,"mined")+"\n"+row(2,"mined")+"\n"+row(3,"mined")+"\n"+row(1,"mined")+"\n",
                "SCORECARD.md": "# S\n\n| sources-registry | 3 rows |\n"})
# P1-1/P1-2: m8 allowlist and tokeniser
make("m8_cover", {"corpus/SOURCES.md": REG, "SCORECARD.md": "# S\n",
  "corpus/lessons/round-41.md": "`docs/nope.md` `scripts/nope.py` `measure.py` `.ufo/evidence/round-40/nope.json` `corpus/nope.md` `tools/nope.py` `.ufo/evidence/round-41/nope.json`\n"})
# P1-5/P1-6: m9 None shortcut, masking, echo, appendix
R40 = ("## Round 40\n\n### Quarantine\n\n| S001 | x | **Adopted** |\n"
       + "\n".join("| S%03d | x | refused |" % i for i in range(2,8))
       + "\n" + "\n".join("| S%03d | x | present |" % i for i in range(11,21)) + "\n")
make("m9_nosum", {"corpus/SOURCES.md": REG, "SCORECARD.md": "# S\n", "corpus/lessons/round-41.md": "# R41\n",
                  "corpus/lessons/round-40.md": R40})
make("m9_mask", {"corpus/SOURCES.md": REG, "SCORECARD.md": "# S\n", "corpus/lessons/round-41.md": "# R41\n",
                 "corpus/lessons/round-40.md": R40 + "\nAs the table shows, one row adopted, six refused, ten present.\n\n## Closing\n\nSeven refused and nine present.\n"})
```

Then, for each lane: `python3 /tmp/tameshi-r41-c1counter/pinned.py --lane /tmp/tameshi-r41-c1counter/<name> --rev HEAD`.
Expected under `9aaa99ac…`: `f1_empty` PASS `records=0`; `f2_bold-name` PASS; `f2_entries-not-rows`
PASS; `f2_dupe-last-right` PASS; `m6_dup` `sources_rows=3` PASS; `m8_cover` `m8=3` (only the three
prefixed paths); `m9_nosum` PASS; `m9_mask` PASS. Under the frozen `f00917dd…`, add the
`m7_11col` case (a mined `S001` citation → `m7 S001 cited but status=2026-10-19`) and the
`m9_hardcode` case (table 7/9, summary 8/6, lesson "six refused and ten present" → `m9=0`; under
`9aaa99ac…` it is `m9=1`).

## Cross-seat corroboration

`MutC1Parse` independently reproduced the `cells[9]`/`cells[8]` finding and the m9 `None` shortcut,
and their mutant-A probe shows `quarantine_counts` has exactly one consumer, so its behaviour is
unobservable except by the hash — which is the argument for P2-3, not against the pin. Their §6
snapshot ("lane counter is byte-unchanged") was true at 03:39 and is now stale by two edits; do not
carry it into the deciding run as a fact.
