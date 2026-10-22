# ColdreadPilot — one real cold read, end to end (round 26 wave 1)

Seat: `TameshiR26.ColdreadPilot` · lane: `tameshi-shokunin` · read point:
`a08e85c5d7f899e8a5992e20517edb1a380d79eb` · bucket: `SKILL.md:2086-2096`
(`## Ninth recorded case — round 26`) · scratch clone: `/tmp/tameshi-r26-coldread/fleet/tameshi-shokunin`.

## Verdict

1. **The recipe in `SKILL.md:1879-1893` works end to end.** One bucket was read cold
   in a fleet-mirror clone: 9 traced commands, 9 receipts, one `tameshi-coldread-report-v2`
   block, an assembly with `--carry` into a scratch ledger (305 entries = 304 carried + 1 new),
   and a round-21 measure against a scratch commit in the clone (exit 0,
   `recorded_cases=9`, `depth_score=9`, `trace_gate=strict`, `overrides_used=false`).
2. **Nine of the bucket's ten claims verify exactly** at the read point: the kumitate
   pin (sha256/2537 lines/mode 100755), the leg row, 5/10 killed, 10/10 predictions held,
   the pre-registration commit `622d31d` preceding the sweep, the `env -i` suite form of
   cases 7 and 8, the 62-case hermetic group, the sweep evidence file, and the replay
   (`REGRESSION_CASE js-cite-check: PASS`, `cases=9 passed=9`).
3. **One claim does not hold at the read point, and it is a pointer, not a number.**
   The bucket's last line names the knowledge entry
   `corpus/knowledge/mutation-case-kumitate-cite-check.md`; that file is absent from the
   tree at `a08e85c5` (and has no history). The bucket is therefore **not** a verified
   record at this rev: verdict `wrong-expectation`, which the round-18 credit rule
   treats as failing, so the bucket is **vetoed** (`credited=false, vetoed=true,
   reason=verdict:wrong-expectation`).
4. **Smallest safe correction:** land `corpus/knowledge/mutation-case-kumitate-cite-check.md`
   (the round-26 wave's entry seat owns that file) **before or together with** the page
   claim, then re-read this bucket. A what-if measurement on the same receipts and the
   same inputs, with G1 demoted to a minor gap, moves the bucket from vetoed to credited
   (32 → 33 of 64 buckets). No other edit is needed: claims 1-9 are exact.
   *Observed after the read point (2026-10-22, live lane):* that file now exists in the
   lane worktree as an untracked file (`git status --porcelain` →
   `?? corpus/knowledge/mutation-case-kumitate-cite-check.md`), so G1 is a **landing
   order** defect, not a missing artifact — it resolves the moment the L1 commits it.
   The lane's working-tree `SKILL.md` has also grown new wave-1 prose inside this very
   section (the survivor table), so the bucket's line range moves with it: **re-derive
   the section boundaries at the read rev, never reuse `2086-2096`**.

## The recipe a fresh seat can copy-paste for one section

Every command below was run this session; the observed output is quoted after each block.
The lane itself is never written to and never committed to: all writes happen in `$W`.

### 0. Pick the bucket and its identity

```bash
REV=a08e85c5d7f899e8a5992e20517edb1a380d79eb        # the 40-hex read point
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
```

Headings and their line numbers (a bucket is one `^#{1,3}` heading plus its body, up to
the next heading; the page is split on headings outside ``` fences):

```bash
git -C "$LANE" show "$REV:SKILL.md" | grep -n "^#\{1,3\} " | tail -8
```

Page sha256 (this is the report's `skill_sha256`; it identifies the whole page blob):

```bash
git -C "$LANE" show "$REV:SKILL.md" | sha256sum
# aa07235f5c505905c73969b57e34ccdd8c49602579b517aaedc4605f61f1ccd3  -
```

Bucket sha256 — the rule is: lines `start..end` of the page, trailing whitespace-only
lines stripped, joined with `\n`, no trailing newline:

```bash
git -C "$LANE" show "$REV:SKILL.md" | sed -n '2086,2096p' | sha256sum   # wrong: keeps the newline
s=$(git -C "$LANE" show "$REV:SKILL.md" | sed -n '2086,2096p'); printf '%s' "$s" | sha256sum
# 99d8173449786d748a436e3554e98385fb3576f80a005c50e930b6a286cb623a  -
```

(`$( )` strips the trailing newlines, which is exactly the rule's "strip trailing
whitespace-only lines"; `printf '%s'` must not add one back.)

### 1. Fleet-mirror clone, detached at the read point

```bash
W=$(mktemp -d /tmp/tameshi-coldread.XXXXXX)
mkdir -p "$W/fleet"
for d in "$LANE"/../*-shokunin "$LANE"/../*-shokukin; do
  b=$(basename "$d"); [ "$b" = tameshi-shokunin ] && continue; ln -s "$d" "$W/fleet/$b"
done
git clone -q "$LANE" "$W/fleet/tameshi-shokunin"
git -C "$W/fleet/tameshi-shokunin" checkout -q --detach "$REV"
R="$W/fleet/tameshi-shokunin"
T="$R/.ufo/evidence/round-26/coldread/traces/<SEAT>"; mkdir -p "$T"
cd "$R"
```

Observed: `git -C "$R" rev-parse HEAD` → `a08e85c5d7f899e8a5992e20517edb1a380d79eb`.
The lane clone must be **detached at `REV`**: the tracer stamps each receipt with the
root's HEAD commit, and the assembler rejects a receipt whose `rev` differs from the
report's `read_rev`.

### 2. Run every command the bucket names, under the tracer

```bash
python3 tools/trace-inputs.py --root "$R" --out "$T/01-<name>.json" -- <argv…>
```

Example (the replay the bucket names):

```bash
python3 tools/trace-inputs.py --root "$R" --out "$T/01-regression.json" -- \
  bash tools/mutate-and-run.sh --regression
```

Observed: tracer exit 0; receipt `rev=a08e85c5…`, `tracked_filter=true`,
`live_lane_reads={}`, `inputs={"tools/mutate-and-run.sh":"fb91ef76…9f9de"}`,
`external={}`, `dropped_home_count=5529`; stdout carried
`REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`
and `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`.
Wall time 4 m 54 s under `strace` (the nine legs run in parallel; 34 min of user time).

Every file the bucket cites should also be opened through the tracer, so that each
opened lane file has a receipt:

```bash
python3 tools/trace-inputs.py --root "$R" --out "$T/09-sweep.json" -- \
  bash -c 'sha256sum .ufo/evidence/round-26/cite-check/sweep/sweep.txt; grep -n "MUTATE: DONE\|62/62 cases passed" .ufo/evidence/round-26/cite-check/sweep/sweep.txt | head -3'
```

Observed: exit 0; `957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893`;
receipt `inputs={".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8…"}`.

Sibling artifacts (another lane's repo) are read with `git show` against the pinned rev
and recorded as **external inputs**; they are never credited as lane inputs.

### 3. Write the report (one ```json block, `tameshi-coldread-report-v2`)

Put it in the clone so that the assembler can glob it, e.g.
`$R/.ufo/evidence/round-26/coldread/reports/<SEAT>.md`. The exact shape is in the next
section. In one sentence: *one* closed ```json block, `seat`, the page sha, the read
rev, and one object per bucket with the bucket's line number, its heading, its class,
its verdict, the three finding lists, the commands, the opened files, the inputs with
sha256, the external inputs, and the receipt paths.

### 4. Assemble with `--carry` into a scratch ledger

```bash
python3 .ufo/evidence/round-18/coldread/assemble.py \
  --repo "$R" \
  --reports "$R/.ufo/evidence/round-26/coldread/reports" \
  --carry "$R/.ufo/evidence/round-21/coldread/ledger.json" \
  --out /tmp/scratch-ledger.json
```

Observed: `ledger written: /tmp/scratch-ledger.json (305 entries)`, `rejected reports: none`,
`coverage: 63/64 buckets covered (skill aa07235f5c50)`, and the uncovered bucket listed
as `start=2097 ### Round-26 gate/probe registry — report interop` (the sibling bucket I
did not read). **Exit code 1** — see pitfall P1.

### 5. Commit the receipts, the report and the ledger together, then measure

The round-21 selector reads its ledger from a fixed path inside the measured repo
(`--ledger-file` / `--ledger-rev` are refused, exit 64 `SELECTOR_OVERRIDE_FORBIDDEN`),
so the scratch ledger must be placed at that path in the clone and committed with the
receipts it names:

```bash
cp /tmp/scratch-ledger.json "$R/.ufo/evidence/round-21/coldread/ledger.json"
git -C "$R" add .ufo/evidence/round-26/coldread .ufo/evidence/round-21/coldread/ledger.json
git -C "$R" -c user.name=<seat> -c user.email=<seat>@example.invalid commit -q -m "cold read: <bucket>"
REV2=$(git -C "$R" rev-parse HEAD)
python3 "$R/.ufo/evidence/round-21/coldread/measure.py" --repo "$R" --rev "$REV2" --explain
```

Observed at scratch commit `f85e85a17b877edb64eab9d123b3d234e37d2bb9` (exit 0):
`recorded_cases=9`, `depth_score=9`, `calibration_restraint_score=6`,
`overrides_used=false`, `trace_gate=strict`, `ledger_source=rev`,
`ledger_committed=true`; `coldread.sections_total=64`, `coldread.sections_covered=32`,
`coldread.box3_full_page=false`; the pilot bucket reads
`start=2086 credited=false vetoed=true reason=verdict:wrong-expectation`, and
`start=2097 no-ledger-entry`.

The what-if run (same receipts, same inputs, G1 demoted to a minor gap — **not** the
pilot's verdict, only a check that the credit path is live) at
`ad6f67cf842b381bf5d50af462ada8edb8975bd4` reads
`sections_covered=33`, `start=2086 credited=true vetoed=false reason=credited`.

## The `tameshi-coldread-report-v2` shape, every required key

Top level (all four keys are required; `schema` is optional but must be exactly this
string if present):

| key | type | rule (from `assemble.py:load_report`) |
|---|---|---|
| `schema` | string | `"tameshi-coldread-report-v2"` |
| `seat` | string | non-empty; the seat id |
| `skill_sha256` | string | 64 hex, lower-cased; the sha256 of the whole page blob at `read_rev` |
| `read_rev` | string | 40 hex, lower-cased; must resolve in `--repo` and must equal every receipt's `rev` |
| `sections` | array | one object per bucket read; a non-object element is rejected |

Each element of `sections` (the assembler fills the five optional lists with `[]` when
they are absent, so they may be omitted, but a present one must be an array of strings):

| key | type | rule |
|---|---|---|
| `start` | integer | the bucket's first line on the page; must be a section start of the page at `skill_sha256` |
| `heading` | string | the heading line verbatim; must equal the page's heading at that start |
| `class` | string | `"instruction"` or `"record"` |
| `verdict` | string | one of `wrong-expectation`, `gap-blocking`, `not-executed`, `gap-minor`, `verified-record`, `executed-ok` |
| `blocking_gaps` | array of strings | findings that block the bucket |
| `wrong_expectations` | array of strings | claims the page makes that do not hold |
| `minor_gaps` | array of strings | non-blocking findings |
| `commands_executed` | array of strings | one entry per command actually run; if non-empty, `traces` must be non-empty |
| `opened` | array of strings | lane files opened by hand |
| `inputs` | object | lane-relative path → 64-hex sha256; the assembler merges the receipts' `inputs` into it, and a path present in both with a different sha is a `trace-conflict` rejection |
| `external_inputs` | object | sibling/other-repo path → 64-hex sha256; the key shape is `repo@<40-hex-rev>:path` or an absolute path; a key that resolves inside the lane is rejected (`external-input-lane`), and a malformed `x@y` shape is rejected (`external-input-shape`) |
| `traces` | array of strings | receipt paths, lane-relative against `--repo` (or absolute); each must exist, parse, carry `schema=tameshi-trace-inputs-v1`, and have `rev == read_rev` |

Class/verdict pairing that the credit rule enforces (`measure.py:entry_credit_reason`):

- `class=instruction` → verdict must be `executed-ok` or `gap-minor`, and
  `commands_executed_count` must be > 0.
- `class=record` → verdict must be `verified-record` or `gap-minor`.
- Any of `wrong-expectation`, `gap-blocking`, `not-executed`, or a non-empty
  `blocking_gaps` / `wrong_expectations`, is a **failing** entry: it vetoes the bucket
  unless its recorded inputs are stale (fail-closed).
- Every entry needs `commands_executed_count > 0` and, in strict mode (no
  `--ledger-file` / `--ledger-rev` / `--inputs-overlay`), at least one committed receipt.

A minimal, complete bucket object (this is what the pilot wrote, abridged):

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdreadPilot",
  "skill_sha256": "aa07235f5c505905c73969b57e34ccdd8c49602579b517aaedc4605f61f1ccd3",
  "read_rev": "a08e85c5d7f899e8a5992e20517edb1a380d79eb",
  "sections": [
    {
      "start": 2086,
      "heading": "## Ninth recorded case — round 26",
      "class": "record",
      "verdict": "wrong-expectation",
      "blocking_gaps": [],
      "wrong_expectations": ["G1: … the cited entry file does not exist at this rev …"],
      "minor_gaps": ["M1: …", "M2: …"],
      "commands_executed": ["bash -c '…' (exit 0; …)"],
      "opened": ["SKILL.md", "tools/mutate-and-run.sh"],
      "inputs": {"tools/mutate-and-run.sh": "fb91ef76…9f9de"},
      "external_inputs": {"kumitate-shokunin@1205c662…:scripts/cite-check.mjs": "40573448…c10c9f"},
      "traces": [".ufo/evidence/round-26/coldread/traces/CRPILOT/01-regression.json"]
    }
  ]
}
```

## Evidence (exact commands, observed output)

Bucket text at the read point — `git -C "$LANE" show a08e85c5…:SKILL.md | sed -n '2086,2096p'`:

```
## Ninth recorded case — round 26

kumitate `scripts/cite-check.mjs` at rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`
(blob sha256 `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines,
mode 100755) is ledger leg `js-cite-check`: 5/10 killed, 10/10 verdict predictions held. The
spec and predictions were committed (`622d31d`) before any mutant ran; the suite is the
hermetic `env -i` form of cases 7 and 8 and runs only the gate's hermetic group (62 cases).
Sweep: `.ufo/evidence/round-26/cite-check/sweep/sweep.txt`. Replay:
`bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-cite-check: PASS`,
`cases=9 passed=9`. Entry: `corpus/knowledge/mutation-case-kumitate-cite-check.md`.
```

| # | command | observed |
|---|---|---|
| 1 | `bash -c 's=$(sed -n "2086,2096p" SKILL.md); printf "%s" "$s" \| sha256sum; printf "%s" "$s" \| wc -c'` | `99d8173449786d748a436e3554e98385fb3576f80a005c50e930b6a286cb623a`, 725 bytes, exit 0 |
| 2 | `bash -c 'git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c662…:scripts/cite-check.mjs \| sha256sum; … \| wc -lc; git -C … ls-tree 1205c662… scripts/cite-check.mjs'` | `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, `2537 126735`, `100755 blob 9770de8c…`, exit 0 |
| 3 | `bash -c 'python3 -c "<compare predictions.json with sweep/results.tsv>"'` | `predictions 10 held 10 mismatch []`, `predicted_kill_rate 5/10`, exit 0 |
| 4 | `bash -c 'git cat-file -t 622d31d; git log -1 --format="%H %cI %s" 622d31d; git show --stat --format="%H %cI" 622d31d \| head -12; git log -1 --format="%H %cI %s" -- …/sweep/sweep.txt'` | `622d31d90b1fbc55c56e91a2b012bc18d6f1421a 2026-10-22T07:01:47-03:00 round-26: pre-register claims C1 … and C2 …`; spec + predictions in that commit; sweep evidence lands in `a08e85c5` at `2026-10-22T07:06:40-03:00`; `sweep.txt` `MUTATE_DATE: 2026-10-22T10:02:07Z` = 20 s after the pre-registration commit |
| 5 | `bash -c 'test -f corpus/knowledge/mutation-case-kumitate-cite-check.md && echo PRESENT \|\| echo ABSENT; git ls-tree -r --name-only HEAD -- corpus/knowledge \| grep -c "cite-check"; git log --oneline --all -- corpus/knowledge/mutation-case-kumitate-cite-check.md \| head -5'` | `ABSENT`, `0`, no history line, exit 0 — **the only claim that fails** |
| 6 | `bash tools/mutate-and-run.sh --regression` | exit 0; `REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`; `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`; 9 legs, 4 m 54 s wall under `strace` |
| 7 | `bash -c 'grep -n "^#   js-\|^#   bash-" tools/mutate-and-run.sh; … grep -o "env -i[^'\'']*node [^'\'']*" \| sort \| uniq -c'` | nine header legs incl. `#   js-cite-check  kumitate-shokunin/scripts/cite-check.mjs  5/10 (50 %)`; `3 env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest` — one identical suite string for cases 7, 8 and 9 |
| 8 | `bash -c 'sha256sum .ufo/evidence/round-26/cite-check/cite-check.defects.spec; grep -c "^@defect" …; grep -n "hermetic group only" …'` | `969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208`, `10` defects, header line 3: "hermetic group only, 62 cases at the pin" |
| 9 | `bash -c 'sha256sum .ufo/evidence/round-26/cite-check/sweep/sweep.txt; grep -n "MUTATE: DONE\|62/62 cases passed" … \| head -3'` | `957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893`, `62/62 cases passed (hermetic)`, `MUTATE: DONE (target=cite-check.mjs defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)` |

Receipts (all in the scratch clone, committed in `f85e85a1`):
`.ufo/evidence/round-26/coldread/traces/CRPILOT/01-regression.json` (exit 0, inputs
`tools/mutate-and-run.sh`), `02-bucket-sha.json`, `03-kumitate-pin.json` (external
sibling read; `dropped_home_count=9`), `04-predictions.json`, `05-prereg-commit.json`
(`dropped_home_count=18`), `06-entry-citation.json` (`dropped_home_count=6`),
`07-leg-and-suite.json`, `08-spec.json`, `09-sweep.json`. Every receipt reports
`rev=a08e85c5d7f899e8a5992e20517edb1a380d79eb`, `tracked_filter=true`,
`live_lane_reads={}`.

Two minor, evidence-chain notes found on the way (not defects of the bucket's claims):

- **M1** `sweep/sweep.txt` pins the tool that produced it as
  `sha256=d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`; that is
  `tools/mutate-and-run.sh` at commit `58e5d53d` (2026-10-20T17:20:09-03:00), i.e. the
  pre-ninth-leg runner. The runner committed at `a08e85c5` is
  `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`. Both shas are in
  the object store, so the sweep is reproducible — but the sweep was produced by
  different tool bytes than the replay the bucket names.
- **M2** the sweep file records machine-specific absolute paths
  (`/fast/scratch/hyaku/tameshi-r26/sweep`, the live-lane path of the tool) and was taken
  against the live lane tree rather than a clone; the re-runnable form is the
  lane-relative spec plus the runner's `--target` mode.

## Pitfalls hit (each one cost real time — read this before starting)

- **P1 — `assemble.py` exits 1 when the page is not fully covered.** A one-bucket pilot
  will always exit 1: the exit code means "uncovered buckets exist", not "assembly
  failed". Read the two lines it prints (`ledger written: … (N entries)`,
  `uncovered buckets:`) before treating 1 as an error. Exit 2 is the real failure
  (unreadable carry ledger, unresolvable read rev, unwritable output).
- **P2 — `--carry` changes the coverage basis.** With `--carry`, coverage is compared by
  **section sha256**, not by `(page sha, start)`; the tool prints
  `carry coverage basis: section_sha256`. A bucket that was edited since the carried
  entry loses its coverage silently.
- **P3 — the report's `skill_sha256` is the sha of the whole page, not of the bucket.**
  The bucket's own sha goes into the ledger entry, not into the report. Mixing them
  gives `page-sha-mismatch: no blob at rev … has sha256 …` and the report is rejected.
- **P4 — the receipt's `rev` must equal the report's `read_rev`.** The tracer stamps
  the receipt with the root's HEAD. If the clone is not detached at the read point, the
  receipt is rejected with `trace-rev-mismatch`. Detach the clone before tracing.
- **P5 — the bucket sha must be computed the assembler way.** `git show … | sed -n … |
  sha256sum` hashes the trailing newline too and does not match; use
  `printf '%s' "$(…)"`. The identity is: lines `start..end`, trailing whitespace-only
  lines stripped, joined with `\n`, no trailing newline. Heading lines inside ``` fences
  do not split buckets.
- **P6 — the tracer records only what was opened, not what was stat-ed.** `test -f`,
  `ls`, and `git ls-tree` leave no input in the receipt. Absence cannot be proven by a
  receipt; prove it with a `git ls-tree`/`git log --all` command whose *output* you
  quote in the report prose, and keep the receipt for the surrounding read.
- **P7 — sibling git-object reads vanish from the receipts.** `external` excludes any
  path with a `.git` component, so a sibling's `git show REV:path` is counted only in
  `dropped_home_count` (5529 for the regression run) and never appears as an input or
  an external entry. Record sibling artifacts as `external_inputs` with the
  `repo@<40-hex-rev>:path` shape instead.
- **P8 — the mirror's symlinks resolve to the real fleet.** `realpath` of
  `$W/fleet/kumitate-shokunin` is the live sibling, so with the default
  `--fleet-root /home/vgpnk/Projects/shokunin` a sibling read would be recorded under
  the live path. The regression is safe (it materialises the pinned blob from the
  object store into its own scratch), but a seat that reads a sibling's *worktree*
  would be reading the live tree. Keep `--live-lane` at its default so such a read is
  flagged `live-lane-read:`.
- **P9 — the run is slow.** `bash tools/mutate-and-run.sh --regression` took 4 m 54 s
  wall (34 min user) under `strace` for nine legs. Budget for it; do not run it twice.
- **P10 — the round-21 selector will not take a ledger from anywhere else.**
  `--ledger-file`, `--ledger-rev` and `--inputs-overlay` are refused with
  `SELECTOR_OVERRIDE_FORBIDDEN` (exit 64). The scratch ledger must be written to
  `.ufo/evidence/round-21/coldread/ledger.json` inside the clone and committed there.
- **P11 — the carried ledger does not credit the current page by itself.** The round-21
  ledger's 304 entries are keyed to 14 *older* page shas and to old read revs; at the
  pilot's scratch commit 31 of the 64 buckets failed with `input-drift:` because the
  lane files moved since those reads. A bucket needs a fresh read at the current rev,
  not just a carried entry. The pilot's own bucket was the only one that credited from
  a read taken at this rev.
- **P12 — the lane is jj-colocated.** Do not run any `jj` command anywhere: `jj log`,
  `jj st` included, they snapshot the colocated working copy. Use `git` with
  `GIT_OPTIONAL_LOCKS=0` for read-only lane inspection, and never `git add/commit` in
  the live lane — only in the scratch clone.
- **P13 — a bucket's line range belongs to one rev.** The lane's working tree is moving
  under the wave: while this pilot ran, `SKILL.md` itself was modified in the live lane
  and the ninth-case section grew new prose, so `2086-2096` is valid **only** for
  `a08e85c5`. Derive `start`/`end` from the read rev every time, and never reuse another
  seat's range.

## Wave-2 worklist (measured at the pilot's scratch commit `f85e85a1`)

`coldread.sections_total=64`, `coldread.sections_covered=32`, `box3_full_page=false`.
The 32 uncredited buckets and their reason:

- `131-245`, `827-857`, `858-882`, `883-898`, `921-932`, `933-964`, `965-1009`,
  `1021-1068`, `1069-1091`, `1092-1154`, `1164-1211`, `1212-1229`, `1246-1271`,
  `1272-1280`, `1281-1301`, `1302-1364`, `1380-1395`, `1499-1516`, `1517-1547`,
  `1548-1562`, `1563-1596`, `1609-1675`, `1754-1805`, `1806-1813`, `1814-1845`,
  `1846-1854`, `1905-1924`, `1925-1937`, `1938-1963`, `1964-2085` — every one of these
  fails with `input-drift:` (a carried entry whose recorded input no longer has its
  sha at the measured rev). A cold read at the current rev replaces the carried entry.
- `2086-2096` — the pilot's bucket, vetoed by its own `wrong-expectation` finding.
- `2097-2101` (`### Round-26 gate/probe registry — report interop`) — no entry; it
  names `tools/mte-interop.py --check --fleet-root …` and its `uv run --with
  jsonschema==4.25.1` dependency.

So wave 2 needs 31 re-reads plus the round-26 registry subsection, each with its own
receipts, before `box3_full_page` can become true at the current rev.

## Sources opened this session (path · access date · located quote)

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md:1879-1893` · 2026-10-22 ·
  recipe heading: "Recipe for one bucket, cold:"; step 3: "Record the verdict block
  (schema `tameshi-coldread-report-v2`)".
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md:2086-2096` · 2026-10-22 ·
  "Entry: `corpus/knowledge/mutation-case-kumitate-cite-check.md`."
- `…/.ufo/evidence/round-18/coldread/assemble.py` · 2026-10-22 · `load_report`:
  "missing/invalid 'skill_sha256' (64-hex required)"; `apply_trace_binding`:
  "trace-receipt-missing: start=%s ran %d command(s) without a trace receipt".
- `…/.ufo/evidence/round-18/measure.py` · 2026-10-22 · `entry_credit_reason`:
  "if cls == 'instruction':"; `coldread`: "covered = credited > 0 and not vetoes".
- `…/.ufo/evidence/round-21/coldread/measure.py` · 2026-10-22 · line 107:
  "SELECTOR_OVERRIDE_FORBIDDEN: " (the selector's refusal of a ledger override);
  `SKILL.md:1951` (the round-20 gate/probe registry row) reads "refuses ledger-file,
  ledger-rev and inputs-overlay flags".
- `…/tools/trace-inputs.py` · 2026-10-22 · "``external`` is restricted to the fleet
  root (default …) minus ``.git`` components".
- `…/.ufo/waves/round-17/w2/CR17.md` · 2026-10-22 · example report block:
  `"schema":"tameshi-coldread-report-v2","seat":"CR17"`.
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin` (read-only, pinned object store) ·
  2026-10-22 · `git show 1205c662…:scripts/cite-check.mjs` → 2537 lines,
  sha256 `40573448…c10c9f`.

## Scope, limits and tooling

- Tools installed or upgraded: **none** (no package manager transaction was needed;
  `node`, `uv`, `strace`, `git`, `python3` were already present — `node v24.21.0`,
  `uv 0.13.0`, `strace 7.2`).
- Writes: only the scratch clone `/tmp/tameshi-r26-coldread/**` and this report file.
  Nothing in the live lane was modified, staged or committed; no `jj` command was run;
  the sibling `kumitate-shokunin` was read only through `git show` on a pinned rev.
- The tracer cannot see environment variables, stat-only probes, inherited descriptors
  or network, and a seat can still omit a command: the rule makes a recorded read
  checkable, not complete. This pilot's bucket is one bucket of a 64-bucket page.
- No producer-authentication or promotion claim is made here: the numbers quoted are
  the ones the two tools printed, at the revs named.
