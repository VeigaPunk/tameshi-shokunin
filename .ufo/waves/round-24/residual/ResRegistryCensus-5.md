# ResRegistryCensus-5 — registry census at the final tip, and the no-harm numbers

Item: (a) run `tools/registry-check.py` in a private clone against
`--rev 4903959687d16623adeeeae059bc010dcfc9d23f` and report
held/total/superseded/exit; (b) run `scripts/sources-census.sh validate` for the
`tameshi` lane and report exit and row count; (c) attack
`.ufo/evidence/round-24/noharm-c8c5b88.json` — does REV still hold the same
no-harm numbers?

## Verdict

**PASS at the assigned REV `4903959687d16623adeeeae059bc010dcfc9d23f` — no
defect found. The registry and census numbers are unchanged from wave 1 and
every no-harm number in `noharm-c8c5b88.json` is reproduced at that rev.**

**One lane-movement caveat (not a defect at the assigned REV):** while this seat
ran, the lane advanced to a newer commit `c6e827a97bba5998503b087ce8b91b77fef682ed`
("correct consumer warnings and residual review overclaims"). At that newer
commit the registry, census and C1-ruler numbers still hold, but the **cold-read
no-harm coverage regresses** (`calibration_restraint_score` 8→6,
`sections_covered` 62→59, 3 uncovered headings) until the lane's in-flight
"C-series" state (ledger append + C-series trace receipts) is committed — which
I verified restores 62/62 and 8/8 in a private probe. See F6.

- Registry check at the assigned REV: **held 47 / total 47, superseded 7,
  exit 0** — the same triple `noharm-c8c5b88.json` recorded, on the same
  registry bytes (`registry_sha256 a8f255f1…`).
- Sources census validate for `tameshi`: **exit 0**, registry **83 rows**
  (tier A74 / B7 / C2; status mined54 / queued23 / rejected6; 0 malformed),
  7 `W04` warnings, no `E`-code finding — identical to wave-1
  `RunSourcesCount.md`; `corpus/SOURCES.md` is byte-identical between
  `c8c5b88…` and the tip.
- No-harm witness at the assigned REV: exit 0, `calibration_restraint_score` 8,
  `depth_score` 8, `overrides_used` false, `trace_gate` strict, 62/62
  sections, `missing` [], `uncovered_headings` [], `ledger_committed` true,
  `recorded_cases` 8, `box3_full_page` true. The recorded monitor receipt
  reproduces **byte-identically**: re-running the recorded argv at `c8c5b88…`
  gives `stdout_sha256 146c4e01f70704612764ac8ee09d70121774f78de01da8b268b4fe80e6f1034d`,
  exactly the value stored in `noharm-c8c5b88.json`.
- Round-24 C1 ruler re-run at the tip: **11/11 discriminated, exit 0**, ruler
  sha256 `0a7f6daa…` unchanged (== `before.json`/`after.json`
  `instrument_sha256`).
- No production file edited; no git/jj write command run in the lane; no tool
  installed or upgraded (none needed).

## Environment / procedure (observed)

Host directive from L1 (superseding the `/tmp` clone instruction): clone and
heavy scratch placed under
`/fast/scratch/hyaku/tameshi-r24/TameshiR24-2.ResRegistryCensus-5/` (the
`/tmp` volume had filled earlier).

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r24/TameshiR24-2.ResRegistryCensus-5/repo
git -C .../repo checkout --detach 4903959687d16623adeeeae059bc010dcfc9d23f
→ HEAD is now at 4903959 round-24: retain wave-1 spec, dispatch receipts, 64 seat reports, accounting and errata O-P
```

All commands below ran with cwd = a private clone; `--root` / `--repo` pointed
at the live lane only as an argument (read-only). Nothing was executed with
cwd = the live lane, and the live lane was never written to (its only change
during my seat came from a concurrent writer — F4).

## Run 1 — registry check at the assigned REV (the item's Run step)

```
cd /fast/scratch/hyaku/tameshi-r24/TameshiR24-2.ResRegistryCensus-5/repo
TMPDIR=/fast/scratch/hyaku/tameshi-r24/TameshiR24-2.ResRegistryCensus-5/tmp \
  python3 tools/registry-check.py \
    --root /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 4903959687d16623adeeeae059bc010dcfc9d23f --json \
    > registry-4903959.json 2> registry-4903959.stderr
EXIT=0
```

stderr (human lines) ends with:

```
ROW command-binding-selftest-r24 expect=0 got=0 held
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
ROW command-binding-source-read-red-pinned expect=1 got=1 held
ROW registry-replay-selftest expect=0 got=0 held
REGISTRY_CHECK: held=47/47 superseded=7
```

stdout JSON (`tameshi-registry-check-report-v1`):

```
exit 0 · held 47 · total 47 · superseded 7 · live false · only null
rev 4903959687d16623adeeeae059bc010dcfc9d23f
rev_resolved 4903959687d16623adeeeae059bc010dcfc9d23f
registry_sha256 a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f
rows 54
root /tmp/tameshi-registry-check-g3s0j48g/fleet/tameshi-shokunin
```

**Answer to the item: held 47, total 47, superseded 7, exit 0.**

### Registry comparison against `noharm-c8c5b88.json` (row by row)

Both captures carry the same 54 rows (47 `active` + 7 `superseded`) and the
same `registry_sha256 a8f255f1…` (the registry file did not change between
`c8c5b88…` and the tip — see "no bytes changed" below). Machine diff over
every field except the stdout/stderr tails:

```
name sets equal: True            (no row added, removed or renamed)
only in new: []                   only in noharm: []
field diffs (expect/got/held/status/kind/tags/superseded_by): none
```

stdout tails differ on 9 of 54 rows, each for an accounted reason only:
temp-directory names, the mirror path inside the two `assemble-*-selftest`
reason strings (my `TMPDIR`), elapsed times, and the live-fleet head commits
inside `pin-disposition-read` (F2). No row's `expect`/`got`/`held` verdict
changed.

## Run 2 — sources census validate for the tameshi lane

```
cd /fast/scratch/hyaku/tameshi-r24/TameshiR24-2.ResRegistryCensus-5/repo
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tameshi
EXIT=0
```

Observed output (8 lines: 7 warnings + 1 ok; **no E-code finding**, so
`validate` is clean):

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

**Answer to the item: exit 0, row count 83.** Companion `census` mode for the
same lane (same script, same root):

```
tameshi rows 83 · tier.A 74 · tier.B 7 · tier.C 2
tameshi status.mined 54 · status.queued 23 · status.rejected 6
FLEET.rows 83 · FLEET.missing 0 · FLEET.tier.invalid 0 · FLEET.status.invalid 0
```

Independent recount (not sharing code with the census parser):
`git show <rev>:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3} '` → **81** at
base `6a1821a…`, **83** at `c8c5b88…`, **83** at the tip; the two new ids are
S084/S085 (wave-1 `RunSourcesCount.md` reports the same +2). The `W04` warnings
are pre-existing (same URL across scopes) and, per the script's own contract,
do not change lane status or the exit code.

## Run 3 — the no-harm witness (attack on `noharm-c8c5b88.json`)

The noharm file records two witnesses. I re-ran both, with the recorded argv
and only `--rev` advanced, cwd = private clone.

### 3a. Monitor — byte-identical reproduction at the recorded revision

```
python3 .ufo/evidence/round-21/coldread/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c8c5b88c8e961a929cdc351b95a7074c76958909 --explain
EXIT=0
sha256sum → 146c4e01f70704612764ac8ee09d70121774f78de01da8b268b4fe80e6f1034d
```

`noharm-c8c5b88.json` records
`"monitor": {…"stdout_sha256": "146c4e01f70704612764ac8ee09d70121774f78de01da8b268b4fe80e6f1034d"}`.
The recorded monitor receipt therefore **still reproduces exactly** today; its
numbers are not stale.

### 3b. Monitor at the assigned REV — same no-harm numbers

```
python3 .ufo/evidence/round-21/coldread/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 4903959687d16623adeeeae059bc010dcfc9d23f --explain
EXIT=0
sha256sum → 1a134eb0ab8187e4e601d5a5917ef5e5d501f80d70ebe4752bd22dbf244455fb
```

| no-harm field | noharm (c8c5b88) | assigned REV (4903959) | same? |
|---|---|---|---|
| exit | 0 | 0 | yes |
| calibration_restraint_score | 8 | 8 | yes |
| depth_score | 8 | 8 | yes |
| overrides_used | false | false | yes |
| trace_gate | strict | strict | yes |
| sections_covered / total | 62 / 62 | 62 / 62 | yes |
| missing | [] | [] | yes |
| uncovered_headings | [] | [] | yes |
| ledger_committed | true | true | yes |
| recorded_cases | 8 | 8 | yes |
| box3_full_page | true | true | yes |

Leaf-level diff of the two monitor JSONs: 1763 leaves, **8 differ** — the two
revision fields, plus two per-section reason sets:

```
/coldread/sections/1/reasons/1|2|3|4      (section "# tameshi-shokunin", 6–16)
/coldread/sections/60/reasons/1|2         (section "### Round-20 gate/probe registry — frozen receipt instruments", 1938–1963)
/revision, /rev_input
```

At the tip both sections gain one extra reason string
`input-drift:corpus/QUALITY.md`. Fully explained and benign:

- `corpus/QUALITY.md` digest: base `6a1821a…` `da964b81…` → `c8c5b88…`
  `9959bf4e…` → tip `b0800d1a…` (the QUALITY48 note + QUALITY49 appends).
- Ledger entries 267 and 280 pin `corpus/QUALITY.md = 9959bf4e…` (the
  `c8c5b88` value), so at the tip they drift on that one input and contribute
  the new string; the pre-existing strings are unchanged.
- The two entries appended at the tip (index 282 → section 1, index 283 →
  section 60; `read_rev 250069f1b4ea735cbe89a0637a96af9fae640dca`,
  `sha256` `79aa3f5e…` / `27fc0d2e…`) pin `corpus/QUALITY.md = b0800d1a…`
  and drift on **nothing** at the tip, so they are `credited`.
- Both sections remain `credited: true`, `vetoed: false` at both revisions;
  `sections_covered` stays 62/62 and the scores stay 8/8.

The ledger append is genuinely append-only:
`git diff --numstat c8c5b88… 4903959… -- .ufo/evidence/round-21/coldread/ledger.json`
→ `92  0`, and the first 282 entries are byte-identical (parsed-JSON compare).
`git cat-file -t 250069f1b4ea…` → `commit`; both new entries' `traces` /
`reports` (`.ufo/evidence/round-24/source-traces-B/source-6.json`,
`source-1938.json`, `source-refresh-receipts-B.json`) exist in the tip tree.

### 3c. Registry witness inside the noharm file

`noharm-c8c5b88.json → registry.stdout` records `exit 0, held 47, total 47,
superseded 7, registry_sha256 a8f255f1…`. My run at the assigned REV reproduces
exactly those five values (Run 1). The registry bytes are unchanged:
`git diff c8c5b88… 4903959… -- tools/registry.json corpus/SOURCES.md` →
**empty**.

### 3d. Round-24 C1 ruler at the assigned REV

```
python3 .ufo/evidence/round-24/measure.py --repo <private clone at 4903959>
EXIT=0 → "discriminated": 11, all K1..K11 discriminated: true
sha256(.ufo/evidence/round-24/measure.py) = 0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64
```

equal to `before.json.instrument_sha256` and `after.json.instrument_sha256`
(both `0a7f6daa…`) — the frozen instrument was not touched.

## Run 4 — the lane moved mid-seat: re-measurement at `c6e827a…`

Observed at ~14:47: the live lane HEAD advanced to
`c6e827a97bba5998503b087ce8b91b77fef682ed` ("round-24: correct consumer
warnings and residual review overclaims"), touching only
`SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/knowledge/replay-projection-hardening.md`, `corpus/lessons/round-24.md`
(`git show --stat`); `tools/registry.json`, `corpus/SOURCES.md` and all three
rulers are unchanged. Re-ran the same three witnesses against that rev from a
second private clone (`repo-c6e827a`):

| witness | at `c6e827a…` | result |
|---|---|---|
| `tools/registry-check.py --rev c6e827a…` | `REGISTRY_CHECK: held=47/47 superseded=7`, exit 0, `registry_sha256 a8f255f1…` | unchanged |
| `scripts/sources-census.sh validate … tameshi` | exit 0, last line `tameshi ok …/corpus/SOURCES.md` (7 `W04`) | unchanged (83 rows) |
| `.ufo/evidence/round-24/measure.py --repo <clone at c6e827a>` | exit 0, 11/11 discriminated, ruler sha `0a7f6daa…` | unchanged |
| `.ufo/evidence/round-21/coldread/measure.py --rev c6e827a… --explain` | exit 0, **calibration_restraint_score 6**, depth 8, **sections_covered 59/62**, missing 3, uncovered 3, `box3_full_page` false | **regressed** |

The three uncovered sections at `c6e827a…` and their reasons:

```
# tameshi-shokunin (6–16)                    input-drift:corpus/QUALITY.md;…  (all matching entries drift)
### Round-20 gate/probe registry (1938–1963) input-drift:corpus/QUALITY.md;…
### Round-21 gate/probe registry (1964–2084) no-ledger-entry
```

Cause: `c6e827a` changed `corpus/QUALITY.md` again (`b0800d1a…` →
`da102b09…`) and `SKILL.md` (section 61's content sha changed), while the
**committed** ledger still carries only the 284 entries of the previous tip,
whose pins and section shas describe the pre-`c6e827a` tree. So the no-harm
coverage of the *committed* newer tip is genuinely lower than at the assigned
REV.

The lane's in-flight state restores it. The live worktree at the time of
measurement carried a further ledger append (287 entries; +3 entries with
`read_rev c6e827a…`, `sha256 79aa3f5e…` / `27fc0d2e…` / `9f0b4ab4…`, traces
`.ufo/evidence/round-24/source-traces-C/source-{6,1938,1964}.json`, report
`source-refresh-receipts-C.json`) plus the untracked C-series evidence files.
I reproduced that state in a private clone only (copying the pending ledger and
the C-series files into `repo`, committing them there as `87c9448…`; the live
lane was never written to) and re-measured:

```
python3 .ufo/evidence/round-21/coldread/measure.py --repo <private clone> \
    --rev 87c94485349265a3bebbf1785be941e35648dd2b --explain
EXIT=0 → calibration_restraint_score 8 · depth_score 8 · sections_covered 62/62
          missing 0 · uncovered [] · box3_full_page true · reasons {"credited": 62}
```

(An intermediate probe that included the pending ledger but not the untracked
C-series trace files scored 59/62 with `trace-missing:…source-traces-C/…`
reasons — i.e. the trace receipts, not the ledger entries alone, are what the
strict gate needs. Both facts point at the same landing requirement, F6.)

## Findings

**F1 — (no defect) The no-harm numbers hold at the assigned REV.** Every
number recorded in `noharm-c8c5b88.json` is reproduced at `4903959…`: monitor
exit 0 / 8 / 8 / strict / 62-of-62 / no missing / no uncovered, and registry
47-of-47 with 7 superseded on identical registry bytes. The recorded monitor
`stdout_sha256` even reproduces byte-identically when the monitor is re-run at
its recorded revision, so the receipt is not merely self-consistent but
re-derivable.

**F2 — (observation, not a defect) `pin-disposition-read` is fleet-live and its
recorded output is time-dependent.** The row is tagged `fleet-live`, and under
`--rev` the tool flags it `non_hermetic_argv: ["/home/vgpnk/Projects/shokunin"]`.
Its stdout embeds the *current* HEAD of seven sibling lanes, and three of them
have moved since the noharm capture:

```
tsukuroi head 56c8ba3840cc506e55c1211d7eed0676e69e7ac6 → a61db549c6c425e6a865885009b278f62ae6ef0f
mado     head eead56b20ad2b28299ae4fa623d52a99b44c743c → e33ea30461f6e9bbeee40beef19770a953f7a105
third    head 4d308e5e79b0b9798183445f6431164f2e25e18a → 2dfb534b64c09086faf91f83d53ccc841c782151
```

The row still holds (`expect 0 / got 0 / held true`) because the *pinned* blobs
are unchanged (`"status": "verified"`, pinned blob `d17d32a3…` for
`tsukuroi-shokunin/tools/tsukuroi-census.sh`), and the per-leg
`content_status` distribution is identical in both captures
(`changed, changed, unchanged, changed`). Consequence for the record: the
noharm **registry** sub-capture is not byte-reproducible over time the way the
monitor's `stdout_sha256` is; the registry's identity claim rests on
held/total/superseded/exit and `registry_sha256`, all of which are stable.

**F3 — (observation) The tip adds two `input-drift:corpus/QUALITY.md` reason
strings** to the monitor's per-section detail (sections 1 and 60), explained in
3b. The aggregate no-harm numbers are untouched; a later cold reader comparing
the two monitor outputs should not mistake this for a regression. The two
re-anchoring ledger entries (282/283) are exactly the compensating records.

**F4 — (lane hygiene; not caused by this seat) The live lane was being edited
concurrently while this seat ran.** Timeline observed:

```
~14:36  live lane clean except three untracked paths
~14:44  six tracked files modified (SKILL.md, LOG.md, SCORECARD.md,
        corpus/QUALITY.md, corpus/knowledge/replay-projection-hardening.md,
        corpus/lessons/round-24.md), mtimes 14:44:46–14:45:39
~14:47  those edits land as commit c6e827a; worktree then shows
        .ufo/evidence/round-21/coldread/ledger.json modified (+150 lines,
        287 entries) and untracked C-series evidence
        (source-traces-C/, source-refresh-*-C.json, monitor-intermediate-C.json,
        final-verification.json, waves/round-24/residual/)
```

None of my commands writes to the live lane: every measurement was `--rev`-
pinned (a temp clone) or ran against a private copy, the census script is
read-only by contract, and the ruler copies `--repo` into a temp dir
("All work happens in private copies of --repo; nothing in --repo is written").
`corpus/SOURCES.md` was never among the modified files, so Run 2's row count
is unaffected by this movement. The practical consequence is that "the final
lane tip" is a moving target during the residual wave: a tip-pinned capture
(4903959) and the on-disk lane state (c6e827a + pending C-series) differ.

**F5 — (observation) The census `validate` mode emits 7 `W04` warnings** for
duplicate URLs across scopes (S047/S048, S075–S078, S081). Per the script's own
contract these do not change lane status or the exit code; `validate` returned
`ok` for `corpus/SOURCES.md` and exit 0.

**F6 — (finding, lane-owned, outside the assigned REV) The no-harm cold-read
coverage is *not* self-maintaining across lane edits: the committed tip
`c6e827a…` regresses to 59/62 (calibration_restraint_score 6) because
`corpus/QUALITY.md` and `SKILL.md` changed while the committed ledger still
pins the previous tree.** Concrete counterexample (reproducible):

```
python3 .ufo/evidence/round-21/coldread/measure.py \
    --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev c6e827a97bba5998503b087ce8b91b77fef682ed --explain
→ exit 0, calibration_restraint_score 6, depth_score 8,
  sections_covered 59/62, missing 3, uncovered_headings:
    "# tameshi-shokunin",
    "### Round-20 gate/probe registry — frozen receipt instruments",
    "### Round-21 gate/probe registry — finite environment differential"
  (reasons: input-drift:corpus/QUALITY.md;… ×2, no-ledger-entry ×1)
```

The in-flight C-series state (ledger 287 entries + the C-series trace
receipts `source-traces-C/source-{6,1938,1964}.json` and
`source-refresh-receipts-C.json`) restores 62/62 and 8/8 (measured in a
private clone at `87c9448…`). So the regression is a *landing-order* defect
waiting to happen, not a defect in the assigned REV: **a commit that changes
`corpus/QUALITY.md`/`SKILL.md` without landing the matching ledger entries and
trace receipts in the same commit leaves the committed tip with lower no-harm
coverage than the previous tip.** The strict trace gate is doing its job here
(it refuses credit without the receipt files), so the correction is on the
landing side, not in the ruler.

## Smallest safe correction

Nothing is required at the assigned REV — the registry numbers, the census
numbers and the C1 predicate count are unchanged there, and the recorded
monitor receipt still reproduces byte-identically.

Two optional, additive, append-only follow-ups (owner: L1 / the lane; not
performed by this seat, which may write only this report):

1. **Land the C-series ledger entries and the C-series trace/receipt files in
   the same commit as the `SKILL.md`/`corpus/QUALITY.md` edits** (or land them
   before those edits), and re-measure the monitor at the resulting tip. This
   closes F6: today the committed tip `c6e827a…` measures 59/62 / calib 6
   while the pending state measures 62/62 / calib 8. No ruler, fixture, tool
   or registry byte needs to change — only the landing set and one ledger
   append.
2. Record a tip-pinned no-harm capture next to the existing one —
   `.ufo/evidence/round-24/noharm-<final-tip>.json` in the same shape as
   `noharm-c8c5b88.json` — and cite it in the `SCORECARD.md` / `LOG.md`
   round-24 appends, so the final tip carries its own no-harm receipt instead
   of relying on the `c8c5b88` one. Also fold the F3 delta into the existing
   errata trail ("at the tip the monitor records `input-drift:corpus/QUALITY.md`
   for sections 1 and 60 because QUALITY.md moved at the errata commits; the
   two appended ledger entries re-anchor those sections with current pins").

F4 needs no lane edit from me: the concurrent writer's edits are their business;
I only note that the recorded tip and the on-disk lane state disagree while
the residual wave runs, so any downstream lane should re-pin to the tip it
actually measures.

## Commands (all read-only against the lane; GIT_OPTIONAL_LOCKS=0 where git was used)

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r24/TameshiR24-2.ResRegistryCensus-5/repo
git -C <repo> checkout --detach 4903959687d16623adeeeae059bc010dcfc9d23f

python3 tools/registry-check.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 4903959687d16623adeeeae059bc010dcfc9d23f --json        → exit 0, held 47/47, superseded 7

/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tameshi                     → exit 0, 83 rows, 7 W04
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
    --root /home/vgpnk/Projects/shokunin tameshi                     → rows 83, A74/B7/C2, mined54/queued23/rejected6

python3 .ufo/evidence/round-21/coldread/measure.py --repo <live lane> \
    --rev c8c5b88c8e961a929cdc351b95a7074c76958909 --explain         → exit 0, sha 146c4e01… (== recorded)
python3 .ufo/evidence/round-21/coldread/measure.py --repo <live lane> \
    --rev 4903959687d16623adeeeae059bc010dcfc9d23f --explain         → exit 0, sha 1a134eb0…, 8/8, 62/62

python3 .ufo/evidence/round-24/measure.py --repo <private clone at 4903959>
                                                                  → exit 0, 11/11 discriminated

# newer lane tip observed mid-seat
python3 tools/registry-check.py --root <live lane> --rev c6e827a97bba5998503b087ce8b91b77fef682ed --json
                                                                  → exit 0, held 47/47, superseded 7
python3 .ufo/evidence/round-24/measure.py --repo <private clone at c6e827a>
                                                                  → exit 0, 11/11 discriminated
python3 .ufo/evidence/round-21/coldread/measure.py --repo <live lane> \
    --rev c6e827a97bba5998503b087ce8b91b77fef682ed --explain         → exit 0, calib 6, 59/62, 3 uncovered
python3 .ufo/evidence/round-21/coldread/measure.py --repo <private clone at 87c9448> \
    --rev 87c94485349265a3bebbf1785be941e35648dd2b --explain         → exit 0, calib 8, 62/62, box3 true
    (probe commit: c6e827a + pending 287-entry ledger + C-series traces, private clone only)

git diff --numstat c8c5b88… 4903959… -- .ufo/evidence/round-21/coldread/ledger.json   → 92  0
git diff --name-status c8c5b88… 4903959… -- tools/registry.json corpus/SOURCES.md     → empty
git show <rev>:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3} '       → 81 (base) / 83 / 83
git cat-file -t 250069f1b4ea735cbe89a0637a96af9fae640dca          → commit
```

Tooling: nothing installed or upgraded; nothing to record. No producer
authentication, promotion or numeric score uplift is claimed — all numbers
above are observations from re-runs of the lane's own frozen instruments.
