# RerunRegistryCensus — round-27 wave 1

Seat: `TameshiR27.RerunRegistryCensus` (executor, leaf). Axes: operability, freshness.
Scope: the routed registry re-run and the SOURCES contract check for S012, S090, S091
at the round's content revision `2227d8338c02aa9a5fd7d95c1a41b76865ad7647`.
Base: `91edf9cd82ccc72e10f62f81d37181f549d593b8`.

Everything below was executed in `/tmp` clones. No gate, selftest or sweep was run
inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; no git write command and no
`jj` command was run anywhere. The only file this seat wrote is this report.

---

## 1. Verdict

1. **Registry at the landed head is fully held — 49/49, exit 0 — under the usage the
   lane documents** (a scratch clone whose parent holds the `*-shokunin` siblings,
   `SKILL.md:1839-1841`). Round 27 changed no registry row: `tools/registry.json` is
   byte-identical at base and head (sha256 `c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c`
   at head; the head commit touches no file under `tools/`). No harm.

2. **The literal command in the routed item reads `held=46/49` with 3 rows `differs`,
   and that reading is a measurement-setup artifact, not a content regression.**
   The `/tmp/<name>-reg` clone's parent directory contains no `*-shokunin` siblings, so
   the three rows that read a sibling repo refuse with SETUP
   `repo_identity_mismatch`. The same three rows read `held=46/49` at the **base**
   revision, and all three hold when the same clone is placed in a fleet mirror. The
   lane's own round-27 lesson already records this as mistake 3
   (`corpus/lessons/round-27.md:73-79`); this seat confirms it by measurement and
   reproduces the corrected reading.

3. **SOURCES contract: clean.** `sources-census.sh validate` exits 0 at the pinned
   revision with a warning set byte-identical to the base revision (7 pre-existing
   `W04` "same URL across scopes" warnings, none of them on S012/S090/S091). The
   S012 in-place edit changes **only** `status` and `used-by` (rule 2 compliant);
   S090 and S091 are **new appended rows** whose rule-1 grounding (URL, access date,
   ≤25-word quote, location) is recorded in the round lesson's `## Gate`
   (`corpus/lessons/round-27.md:23-52`). The whole-file diff base→head is three
   lines.

4. **One freshness defect, cheap to repair (recommended):**
   `corpus/SOURCES.md:338` still reads `- Next unused id: S090.` — but S090 and S091
   are now rows (`corpus/SOURCES.md:99-100`). The id-allocation marker is stale and
   invites an id reuse, which the contract forbids ("never reused").
   The lane's own precedent updates this marker whenever a row is written
   (`.ufo/waves/round-26/w1/DraftSourcesRows.md:281,387`).

5. **One freshness gap, worth one file (recommended, lower severity):** round 27
   commits **no registry receipt**, although the lesson states "the mirror receipt is
   the one committed" (`corpus/lessons/round-27.md:77`). Nothing under
   `.ufo/evidence/round-27/` is a registry receipt, so the claim is currently
   unbacked. Precedent exists (rounds 21, 22, 23, 25, 26 committed registry receipts;
   round 24 did not). The corrected reading to commit is in §3.

---

## 2. Evidence

### 2.1 Registry — the literal routed command (no siblings beside the clone)

```console
$ rm -rf /tmp/TameshiR27.RerunRegistryCensus-reg2 && git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/TameshiR27.RerunRegistryCensus-reg2 \
  && cd /tmp/TameshiR27.RerunRegistryCensus-reg2 \
  && git checkout -q --detach 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 \
  && python3 tools/registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
```

**REGISTRY_CHECK line**

```
REGISTRY_CHECK: held=46/49 superseded=7
```

exit code **1** (`held != total`).

**Every row that is not held** (3 active rows `differs` + 7 `superseded` rows, which
by design still run and are excluded from N/M — `tools/registry-check.py` help text:
"Superseded rows still execute so their observed outcome stays visible; they are
excluded from N/M and counted in `superseded=K`"):

```
ROW evidence-disposition-round17 superseded expect=0 got=2
ROW evidence-disposition-round17-before superseded expect=1 got=2
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
ROW mutate-and-run-regression expect=0 got=2 differs
ROW trace-inputs-round17-selftest superseded expect=0 got=0
ROW round21-measure-selftest expect=0 got=1 differs
ROW command-binding-selftest superseded expect=0 got=0
ROW command-binding-frozen-clean superseded expect=0 got=0
ROW command-binding-source-read-red superseded expect=1 got=1
ROW mte-interop-check expect=0 got=2 differs
```

**Diagnosis of the three `differs` rows** (`--only <row> --json`):

- `mutate-and-run-regression` — `stdout_tail`:
  `REGRESSION_CASE js-kimi-census: SETUP (repo_identity_mismatch: /tmp/tameshi-registry-check-…/fleet/kumitate-shokunin is not its own repository; toplevel=unresolved)`
- `round21-measure-selftest` — `stderr_tail`: `File ".../tools/round21-measure.py", line 74, in selftest` →
  `subprocess.run(["git", "-C", str(ROOT.parent / surface["repo"]), "show", …], check=True)`
  — the sibling repo it reads is absent, so `git show` raises.
- `mte-interop-check` — `stdout_tail`:
  `MTE_WORKDIR: /tmp/tameshi-mte-regression-… (removed on PASS)` /
  `MTE_INTEROP: SETUP (regression exit 2)` — it runs the same runner regression.

The cause is in the tool: `tools/registry-check.py:771-782` symlinks the siblings of
the **clone's parent directory** (`fleet_root = os.path.dirname(root_real)`) into the
scratch fleet mirror. A clone in `/tmp` has no `*-shokunin` siblings, so the three
rows that read a sibling repo cannot resolve one.

**Same command at the base revision — identical reading (no-harm evidence):**

```console
$ cd /tmp/TameshiR27.RerunRegistryCensus-reg && python3 tools/registry-check.py --rev 91edf9cd82ccc72e10f62f81d37181f549d593b8
ROW evidence-disposition-round17 superseded expect=0 got=2
ROW evidence-disposition-round17-before superseded expect=1 got=2
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
ROW mutate-and-run-regression expect=0 got=2 differs
ROW trace-inputs-round17-selftest superseded expect=0 got=0
ROW round21-measure-selftest expect=0 got=1 differs
ROW command-binding-selftest superseded expect=0 got=0
ROW command-binding-frozen-clean superseded expect=0 got=0
ROW command-binding-source-read-red superseded expect=1 got=1
ROW mte-interop-check expect=0 got=2 differs
REGISTRY_CHECK: held=46/49 superseded=7
```

Base and head are byte-identical in the non-held set: the 3 `differs` rows are a
property of the measurement setup, not of round 27's content.

### 2.2 Registry — the documented fleet-mirror usage (operability reading)

Mirror built in `/tmp` exactly as the tool expects: the lane clone as a real
directory, every sibling `*-shokunin` repo symlinked beside it (the fleet root
`/home/vgpnk/Projects/shokunin` holds those repos read-only; the tools only run
read-only `git show`/`rev-parse` against them — `tools/mutate-and-run.sh` says
"Fleet trees are never written").

```console
$ F=/tmp/TameshiR27.RerunRegistryCensus-fleet
$ mkdir -p $F
$ for d in /home/vgpnk/Projects/shokunin/*/; do n=$(basename "$d"); \
      case "$n" in *-shokunin) ln -s "${d%/}" "$F/$n";; esac; done
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $F/tameshi-shokunin
$ cd $F/tameshi-shokunin && git checkout -q --detach 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
$ python3 tools/registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
```

**REGISTRY_CHECK line at the head revision**

```
REGISTRY_CHECK: held=49/49 superseded=7
```

exit code **0**.

**Every row that is not held** (only the 7 by-design `superseded` rows; the 3
previously differing rows now read `held`):

```
ROW evidence-disposition-round17 superseded expect=0 got=2
ROW evidence-disposition-round17-before superseded expect=1 got=2
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
ROW trace-inputs-round17-selftest superseded expect=0 got=0
ROW command-binding-selftest superseded expect=0 got=0
ROW command-binding-frozen-clean superseded expect=0 got=0
ROW command-binding-source-read-red superseded expect=1 got=1
```

Same mirror, **base** revision, for symmetry:

```
REGISTRY_CHECK: held=49/49 superseded=7     (exit 0)
```

So: head = base = 49/49. Round 27 neither broke a row nor repaired one; the
registry's state at both revisions is fully held.

### 2.3 Sources census validator (read-only)

```console
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

Exit **0**. No `E`-coded finding (no malformed row, no duplicate id, no enum
violation, no community-at-tier-A, no missing `used-by` path). The seven `W04`
warnings are "same URL across scopes" and are **pre-existing**: validating the base
file with `--file` produces the identical seven lines and `EXIT=0`
(`W04` on S047/S048/S075/S076/S077/S078/S081 — none of them S012, S090 or S091):

```console
$ git show 91edf9cd82ccc72e10f62f81d37181f549d593b8:corpus/SOURCES.md > /tmp/base.md
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/base.md
file	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
… (identical seven lines) …
file	ok	/tmp/base.md
EXIT=0
```

Fleet census for the same lane (for the record):

```console
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi
tameshi	rows	89
tameshi	tier.A	80
tameshi	tier.B	7
tameshi	tier.C	2
tameshi	status.mined	61
tameshi	status.queued	22
tameshi	status.rejected	6
FLEET	rows	89 … FLEET	missing	0
EXIT=0
```

### 2.4 Contract census on the pinned file (CORPUS.md "SOURCES.md — where a shokunin learns")

Run on `corpus/SOURCES.md` at `2227d83` (the frozen manual census from CORPUS.md):

```
rows count: 89        malformed: 0        duplicate ids: (none)
tier histogram: A=80 B=7 C=2
status histogram: mined=61 queued=22 rejected=6
enum violations: (none)      missing used-by paths: (none)
```

(89 = S001–S091 minus the retired S038–S039; base has 87.)

### 2.5 S012 — append-only rule 2 (cell-by-cell, base vs head)

`git diff 91edf9cd 2227d83 -- corpus/SOURCES.md` is exactly three lines
(1 modified + 2 added). Cell comparison of S012:

| cell | base `91edf9cd` | head `2227d83` | verdict |
|---|---|---|---|
| id / source / kind / tier / scope / anchor / teaches | unchanged | unchanged | rule 2: only status, recheck, used-by may change — the other eight cells are untouched |
| status | `queued` | `mined` | allowed in place |
| opened | `2026-10-19` | `2026-10-19` | unchanged (correct: rule 2 forbids editing it) |
| recheck | `90d` | `90d` | unchanged |
| used-by | `—` | `corpus/knowledge/oracle-anchored-survivors.md` | allowed in place; the path exists at head |

- The in-place change is **logged old→new in the round lesson**
  (`corpus/lessons/round-27.md:27-35`: "Status `queued` → `mined`; used-by `—` →
  `corpus/knowledge/oracle-anchored-survivors.md`; opened and recheck cells unchanged
  (append-only rule)") — rule 2 satisfied.
- Rule 1 grounding for the re-open is recorded in the lesson's `## Gate`
  (`corpus/lessons/round-27.md:27-31`): URL `https://arxiv.org/abs/2608.17214`, access
  date 2026-10-22, quote of 25 words ("An expectation is specification-anchored when
  composed from values fixed outside the code under mutation, and state-anchored when
  it flows, directly or transitively, from that code."), location "abstract".
- The `opened`-cell tension is explicitly handled: the frozen counter wanted
  `opened = 2026-10-22`, which rule 2 forbids, so it was amended before any
  after-measurement (`.ufo/evidence/round-27/contract-amendment-1.json`), and the
  amendment names the contract rule as its reason. Consistent with the landed row.

### 2.6 S090 and S091 — new rows, rule 1 and shape

Both are **absent at base** and **present at head** as appended rows
(`corpus/SOURCES.md:99-100`), i.e. new rows, not in-place edits — append-only
compliant. Cell checks:

- shape: 11 columns (NF=13), no `|` inside any cell; id `S090`/`S091` are the next
  unused ids (base marker: "Next unused id: S090");
- `kind` ∈ enum (`docs`), `tier` ∈ enum (`A`, and `community` is not the kind, so no
  tier inflation), `status` ∈ enum (`mined`);
- `opened` = 2026-10-22 (a past/present ISO date), `recheck` = `365d` (a valid
  cadence);
- `anchor` is not a bare homepage: S090 "§ERRORS, EX_USAGE entry @ FreeBSD 15.1 page
  dated May 9, 2024, fetched 2026-10-22"; S091 "§SPECIFYING REVISIONS, `<sha1>` entry
  @ page last updated in 2.56.0 (2026-09-28), fetched 2026-10-22";
- rule 1 grounding for each new row is in the lesson's `## Gate`
  (`corpus/lessons/round-27.md:36-52`): URL, access date 2026-10-22, and a quote of
  17 words (S090) / 18 words (S091) with its location, plus the decision and the
  caveat that S090's page is "legacy and deprecated" and that S091 speaks of Git
  object names, not content pins;
- `status = mined` with a non-`—` `used-by` → the `W03`/`W01` warnings do not apply;
  the `used-by` path `corpus/knowledge/oracle-anchored-survivors.md` exists at head
  and cites all three rows in its `source:` line
  (`corpus/knowledge/oracle-anchored-survivors.md:1`);
- no `E04` duplicate URL+scope for either row (the validator reports no `E` finding).

### 2.7 Freshness findings

**(a) Stale id-allocation marker — `corpus/SOURCES.md:338`**

```
- Next unused id: S090.
```

while `corpus/SOURCES.md:99-100` are the S090 and S091 rows. The file's own
allocation list has no line for S090–S091 as round-27 rows either. Contract
("`id` — `S` + 3 or more digits, the next unused; never reused") plus the lane's
round-26 precedent (`.ufo/waves/round-26/w1/DraftSourcesRows.md:281` — "the
registry's next-unused marker now reads `S090`"; `:387` names the marker line) make
this a real, cheap fix.

**(b) No committed registry receipt for round 27**

`git ls-tree -r 2227d83 -- .ufo/evidence/round-27` lists
`before-rev.txt, c1-before.exit, c1-before.stdout, c1-measure.py,
c2-before-amended.exit, c2-before-amended.stdout, c2-before.exit, c2-before.stdout,
c2-measure.py, census-start.exit, census-start.stdout, contract-amendment-1.json,
contract.json, f8/` — no registry receipt, while
`corpus/lessons/round-27.md:77` says "the mirror receipt is the one committed".
Precedent receipts: `.ufo/evidence/round-21/final/registry.json`,
`round-22/final/registry-final.json`, `round-23/registry-C.json`,
`round-25/after/registry-final-3b20f07.json`, `round-26/after/registry-40a12bf.json`
(round 24 committed none). The round-26 receipt is itself a failing reading
(`"exit": 1, "held": 48, "total": 49`, the one active non-held row being
`mte-interop-check` with `got: "non-hermetic"`), so the lane's last *committed*
registry receipt is stale in both senses — round 27's corrected reading
(`held=49/49 superseded=7`, exit 0) would supersede it.

**(c) Observation, no correction required — no round-27 entry in the SOURCES
"## Search log".** Rule 5 binds "one prose note per bounded search". Round 27 opened
two known URLs (FreeBSD `sysexits(3)`, Git `gitrevisions`) and re-opened one existing
row (S012); it ran no query, so no search note is strictly due. If the L1 wants the
registry to carry the round's source work the way rounds 19–26 did, a one-line note
("bounded lookup: opened the two outside anchors; identified 3 / screened 3 /
included 3 / excluded 0; stop: one definition source and two convention anchors
answer the entry") is enough. **Not filed as a defect.**

---

## 3. Smallest safe correction

1. **`corpus/SOURCES.md:338` (one line, in the L1's lane):** change
   `- Next unused id: S090.` → `- Next unused id: S092.`, and add one allocation line
   above it, e.g.
   `- S090–S091: round-27 rows (outside anchors for the F8 entry: FreeBSD
   `sysexits(3)`, Git `gitrevisions`).`
   This is the only content edit the contract findings require; it touches no
   registry row, so it cannot affect the 89-row census counts, the tier/status
   histograms or the validator's exit code. (The id-allocation list is a maintained
   section outside the frozen v1 shape; the `## Registry` table itself stays
   append-only.)
2. **Optional, one file:** commit the corrected registry receipt for round 27 under
   `.ufo/evidence/round-27/` — the `--json` report of the fleet-mirror run at
   `2227d83` (`"exit": 0, "held": 49, "total": 49, "superseded": 7`,
   `registry_sha256 c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c`),
   matching the round-21/22/23/25/26 naming shape
   (e.g. `.ufo/evidence/round-27/after/registry-2227d83.json`). That makes the
   lesson's "the mirror receipt is the one committed" true.
3. **No change** to `tools/registry.json`, to `tools/registry-check.py`, to the S012
   row, to the S090/S091 rows, or to any gate. Nothing in this seat's reading shows
   a row needing re-pin or supersede.

---

## 4. Commands a reader can re-run (read-only, outside the lane)

```console
# 1. registry at the head revision, with the fleet mirror the tool expects
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/mirror/tameshi-shokunin
# siblings symlinked beside /tmp/mirror/tameshi-shokunin
cd /tmp/mirror/tameshi-shokunin && git checkout -q --detach 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
python3 tools/registry-check.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647   # → held=49/49 superseded=7, exit 0

# 2. the same at the base revision → held=49/49 superseded=7, exit 0
python3 tools/registry-check.py --rev 91edf9cd82ccc72e10f62f81d37181f549d593b8

# 3. sources validator (read-only, fleet root)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi   # → EXIT=0
```

---

## 5. Files changed by this seat

- `.ufo/waves/round-27/w1/RerunRegistryCensus.md` — this report (the only file
  written).

Nothing else. No production file was edited; no git write command and no `jj`
command was run in the lane, the fleet root or any clone; sibling repos were read
only (symlinked into a `/tmp` mirror, `git show`/`rev-parse` only).

## 6. Tooling

No tool was installed or upgraded by this seat (nothing in the routed item needed a
new tool; `git`, `python3`, `uv` 0.13.0, `node` v24.21.0 were already present and
were used as found). No update was performed, so no update-safety gate was entered.
