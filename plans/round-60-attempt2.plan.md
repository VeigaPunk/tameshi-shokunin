# tameshi round 60 — attempt 2 plan (win32 host re-run round; frozen before data)

Attempt 2 of round 60 (watchdog `zcode run14`, launch 2026-10-31, base
`9bc9b20b5d6723a19d1b69c8edd7246f82ea3d78` = origin/master). The dispatch
host is a NEW Windows host: the old Linux host (`/home/vgpnk`, `python3`,
`/fast/scratch`) does not exist here. Attempt 1's round-60 work is committed
lane state; its receipts and counting commands carry the old host's
invocation shape. This attempt sizes its claims from that fact.

Fresh-start duty (§7): the last three rejected closures (r57, r58, r59) were
re-read before declaring (§7 of the round prompt, plus
`corpus/lessons/round-59-verifier-spotcheck.md` §6), and attempt-1's r60 work
was spot-checked FIRST — its committed instruments were run on this host
before any claim was declared. Ruled out, with reasons:

- **Re-running attempt-1's C1 counting command as the claim** — ruled out: it
  is `python3 -I tools/executor-source-pin-measure.py --lane
  /home/vgpnk/...` and cannot run here (the `python3` on PATH is the
  Microsoft Store stub, exit 49; the `/home/vgpnk` lane path does not exist).
  A claim whose counting command cannot execute at adjudication is the exact
  r58/r59 rejection shape.
- **Extending the counter's failure modes (packed object, promisor partial
  clone — the round-61 planned move)** — ruled out this round: the win32 red
  receipt shows the frozen instrument cannot even run here; extending a
  predicate the host cannot execute would stack a new claim on a broken
  instrument. The portability repair must land and re-certify first.
- **Re-litigating attempt-1's C2 counts** — ruled out as a claim: they are
  tree-checkable here with `python` substituted for `python3`
  (`corpus/routed-defects.json` reads fine); re-measuring them adds no axis
  move. Their host scope becomes a C2 record instead.

Host probes (receipt `.ufo/evidence/round-60/win-host/host-probe.txt`):
`python3` = Store stub (exit 49); `python` = 3.13.15 with `PYTHONUTF8=1` in
the dispatch env; symlinks creatable (Developer Mode); git 2.55.0.windows.3
with `core.symlinks=false`. The frozen v1 counter red receipt
(`.ufo/evidence/round-60/win-host/red-v1-counter.{out,err}`) shows two
mechanisms: `UnicodeEncodeError` (cp1252 under `-I`, which ignores
`PYTHONUTF8`, cannot encode the 日本語 fixture content) and a
`PermissionError` cleanup crash (git-for-windows writes loose objects
read-only; `shutil.rmtree` cannot remove them).

## Stagnation nudge premise (unchanged from attempt 1, re-stated)

Scored axes sit at or above the saturation line 8 (depth 10, calibration 8,
freshness 9); coverage/adjacency/operability are verdict-only axes; no
capability has entered the SCORECARD table with a verified admission since
round 50. The lowest-axis obligation is waived (`AXES.md` §The stagnation
nudge); this attempt is a capability + calibration move, like attempt 1.

## Claim C1 — operability; capability cross-host re-certification (sourced S292, S293)

**Predicate (one sentence, same in contract-a2.json and the counter's PASS
label):** at the attempt-2 measured revision, the host-portable counter
revision `tools/executor-source-pin-measure-v2.py` — the frozen instrument's
cell design unchanged (8 shuffled class cells × 5 declared paths in ONE
invocation per cell, per-run nonce fixtures, shuffled order, empty-blob
declared path, corrupt cell expecting exit 2; only host-portability plumbing
differs: explicit UTF-8 fixture writes, `-X utf8` child invocation,
`git update-index --chmod=±x` exec-bit force, read-only-attribute-safe
reset/corrupt/cleanup arms) — run on `tools/executor-source-pin.py` v2
scores `passed=8/8 C1_R60V2_PASS=true` with exit 0 on this win32 host, twice
(two nonces, two class orders), while every control arm scores
`C1_R60V2_PASS=false` with the same per-arm scores the frozen instrument
produced on the Linux host: do-nothing tool-absent 0/8 (`reason=tool-absent`),
unfixed v1 tool 7/8 (only the `corrupt` cell failing), always-accept 3/8,
fingerprint 3/8, sequence 3/8, hash-only 3/8, first-path-only 6/8,
empty-blob-unsound 4/8.

**Before:** no non-Linux certification receipt exists anywhere in the tree at
base `9bc9b20b…`, and the frozen instrument itself cannot produce a verdict
on this host (red receipt, two named mechanisms above). A do-nothing control
cannot reach the after-state: the pass label `C1_R60V2` is absent from the
base tree (`git show 9bc9b20b…:tools/executor-source-pin-measure-v2.py`
fails).

**Counting command (runs on THIS host against committed bytes):**
`python -I tools/executor-source-pin-measure-v2.py --lane <lane> --rev <measured-rev> --work <empty scratch dir>`

**Kill rule:** any change to the v2 counter's cells, class set, expected
exits or PASS condition after the first scored run voids the claim
(re-freeze + re-declare required); any control arm scoring 8/8 kills the
counter and the claim honest-stops; a `C1_R60V2_PASS=true` line whose
receipt's `instrument` digest does not match
`.ufo/evidence/round-60/win-host/freeze-v2.json` defeats the claim.

**Sources:** S292 (git-update-index docs: `--chmod=(+|-)x` sets execute
permissions on updated index entries — opened this round) grounds the
exec-bit cell's index-mode force; S073 (Python command-line docs) is
**re-used, not duplicated** (the lane's S103 precedent: an existing row's
page re-opened this round with a fresh win32 fetch, used-by extended, no new
row for a held URL — CORPUS.md rule 2) for the encoding ground: `-X utf8`
enables UTF-8 mode, and `-I` isolated mode ignores all `PYTHON*` env vars,
so `PYTHONUTF8=1` cannot reach the frozen instrument. Extracts under
`.ufo/evidence/round-60/win-host/sources/`.

## Claim C2 — calibration; host-scope records (protocol + honesty rule)

**Predicate (one sentence):** the round's final tree records which
measurements are host-scoped and what the real host surfaces are:
`corpus/QUALITY.md` carries `### Criterion 118` (a cited counting command or
certification receipt names its host scope and instrument revision; a
command that cannot run on the current host is re-stated portably or
annotated host-scoped) citing `corpus/lessons/round-60.md` mistake 6;
`SCORECARD.md` annotates attempt-1's R60-C1/R60-C2 rows with the string
`counting command host-scoped (linux)`; `PROVINCE.md` carries a dated
correction recording the host-absent template path from line 66 and the
real win32 surfaces; `corpus/lessons/round-60.md` carries an
`## Attempt 2` section with the Gate (S292 opened this round; S073
re-opened with a fresh win32 fetch and used-by extended), mistake 6, and
the win32 verdict record.

**Counting commands (all run on THIS host against committed bytes):**
- `grep -c '### Criterion 118' corpus/QUALITY.md` → before 0, after ≥1
- `grep -c 'counting command host-scoped (linux)' SCORECARD.md` → before 0, after ≥2
- `grep -c 'recorded absent 2026-10-31' PROVINCE.md` → before 0, after ≥1
- `grep -c '^## Attempt 2' corpus/lessons/round-60.md` → before 0, after 1

**Kill rule:** any counting command ambiguous at adjudication kills the
claim honest-stop; receipts that do not resolve at the final revision defeat
the claim.

**Do-nothing control (§9):** every counting command run at base
`9bc9b20b…` scores zero (`git show 9bc9b20b…:<path> | grep -c ...`) — the
strings are introduced by this attempt's commits. Receipt recorded in the
round report.

## No-harm guards

- Cold-read precheck at the final revision (floor `9bc9b20b…` → candidate):
  `bash .ufo/evidence/round-48/quality/coldread-precheck.sh <lane> 9bc9b20b5d6723a19d1b69c8edd7246f82ea3d78 <final-rev>` → `lost=0` required
  (PROVINCE.md and corpus/QUALITY.md are monitor-pinned; this attempt edits
  both by appending, never removing headings).
- Sibling lanes, fleet repo, `.ufo/state/`, `templates/`, `scripts/`
  read-only. Frozen instruments (attempt-1's freeze.json set, incl. the v1
  counter bytes) unchanged — the v2 counter is a NEW file with its own
  freeze, so `.ufo/evidence/round-60/freeze.json` instrument verification at
  HEAD stays intact.
- Scratch under the workspace scratch dir only, deleted on exit.
