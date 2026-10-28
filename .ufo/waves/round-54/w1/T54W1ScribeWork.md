## Work performed — round 54 (hyaku run 11, attempt 2)

Draft for merge by L1 `TameshiR54a2`. Written by seat `T54W1ScribeWork` at 2026-10-28T14:33:47Z from
`.ufo/evidence/round-54/contract.json` (freeze `441c26be`), the content commit
`59c38109bf119d0e9d4f878644a82babc937bc1e`, the wave spec `.ufo/waves/round-54/spec-w1.json`,
`.ufo/waves/round-54/w1/section-manifest.json`, and the receipts that existed in
`.ufo/evidence/round-54/` and `.ufo/waves/round-54/w1/` at that time. Nothing below is a
verdict: the only C1/C2 PASS/FAIL lines this round may print are the deciding run's
(`.ufo/evidence/round-54/deciding-run.sh`, receipts in its OUTDIR). Receipts that did not
exist when this section was written are simply absent from the dated listing below; nothing
is inferred from their absence.

Two axes are frozen with the contract: **calibration** (C1, the lowest non-retired axis,
carrying round 53's honest stop) and **operability** (C2).

### Declared claims — frozen at `441c26be`, before any seat ran

- **C1 — calibration (axis 8).** Surface, as frozen: "the cold-read floor: 57 of 64 SKILL.md sections credit at base; the seven uncredited sections are the round-53 honest stop and its collateral".
  `before`: `credited=57 lost=7 monitor=6/57 (measured at d33053f7, .ufo/evidence/round-54/before/c1.stdout)`. Target, verbatim:
  "C1_R54_PASS=true: the frozen round-48 precheck prints cand_credited=64 lost=0 ok at the deciding revision, the unchanged round-21 selector reads covered=64 score=8, every one of the seven base-lost sections carries a fresh entry bound under rekey-r54-<c0> that credits at the deciding revision, a committed wave reader report pins each section's bytes at <c0>, and no re-key entry pins LOG.md or SCORECARD.md". Counter:
  `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` — five arms, precheck / monitor / rekey / readers / stable
  (`.ufo/evidence/round-54/c1/measure.py:7-42`). Kill rule: "any arm failing makes C1_R54_PASS=false; a section that cannot be re-read cleanly is an honest stop, never a narrowed target".
  Controls `CTL_0 CTL_FAB CTL_LOGINPUT CTL_POS`. `cannot_see`: "whether a reader's judgment of a section is fair, and whether a re-keyed entry's inputs are the ones the reader actually needed; the wave's adversarial re-reads and the L1's disclosed adjudications stand in for that".
- **C2 — operability.** Surface, as frozen: "the scratch-root exit class across the seven tools that call strict_scratch_root()".
  `before`: `unusable_exit2=3 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false (measured at d33053f7, .ufo/evidence/round-54/before/c2.stdout)`. Target, verbatim:
  "C2_R54_PASS=true: 7/7 self-tests exit 2 with a naming could-not-evaluate line and no traceback on a set-but-unusable TMPDIR, 7/7 exit 0 on an empty TMPDIR (declared unset) and on a usable one with no mkdir under /tmp, the seven registry rows carry the scratch_root cell, and the note corpus/knowledge/scratch-root-contract.md cites an S row mined this round with the lesson Gate naming its URL and 2026-10-28". Counter:
  `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` — five arms, unusable / empty / usable / docs / note
  (`.ufo/evidence/round-54/c2/measure.py:9-31`). Kill rule: "any arm short of 7/7 makes C2_R54_PASS=false".
  Controls `CTL_0 CTL_EXIT0 CTL_POS`. `cannot_see`: "whether a tool's self-test exercises the branch that allocates scratch on its real path, and whether a registry cell describes the tool as it now behaves beyond the three named arms".

### Work items — pre-wave (L1, before the wave opened)

- **W0 freeze.** `441c26be` commits the claim contract and `freeze.json`, whose seven
  sha256 entries are `contract.json`, both counters (`c1/measure.py`, `c2/measure.py`), the
  frozen heading set `c1/lost-headings-at-base.json`, `no-harm.sh` (14 monitors),
  `deciding-run.sh` and `control/controls.sh` — evidence: `git show --stat 441c26be`,
  `.ufo/evidence/round-54/freeze.json`.
- **W0 base receipts.** `control/controls-a.stdout` runs five pre-registered controls and
  ends `CONTROLS_A: 5/5 as pre-registered`, exit `0` (`control/controls-a.exit`); its
  `CTL_0_c1` / `CTL_0_c2` lines are the two base verdicts. `before/c1.stdout` (363 B) is a
  base run of the C1 counter: `C1_R54: rev=d33053f7552d c0=none credited=57 lost=7
  rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false`.
- **W0 round-53 negative control.** `control/r53-counter-at-88afa941.stdout` re-runs the
  round-53 C1 counter at its own content revision: `C1_R53: rev=88afa9415454 credited=58
  lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false`, with `PROBLEM
  rekey-dir-count=0` and 30 `PROBLEM rekey-entry-missing` lines (37 `PROBLEM` lines in all)
  — the dead pathspec arm QUALITY criterion 105 is written against.
- **W1 content commit `59c38109`.** 12 files, 2866 insertions, 11 deletions
  (`git show --stat`). The four tools that still raised an uncaught `RuntimeError` now
  declare `ScratchRootUnusable(RuntimeError)` and map it at the entry point to exit 2 with
  one naming line, the raised message text unchanged:
  - `tools/env-diff.py:32` class, `:45` raise, `:235` `ENVDIFF_SETUP: could-not-evaluate: %s`;
  - `tools/bash-witness-study.py:205` / `:218` / `:1789` `WITNESS_STUDY: could-not-evaluate: …`;
  - `tools/evidence-disposition.py:191` / `:204` / `:3232` `evidence-disposition.py: could-not-evaluate: …`;
  - `tools/pin-disposition.py:161` / `:174` / `:1400` `pin-disposition.py: could-not-evaluate: …`.
  The other three of the seven (`registry-check.py`, `context-capture.py`,
  `repeat-control.py`) are untouched, which is the note's own account of the split: "the
  class existed in three tools and not in four (routed defect R53.6)"
  (`corpus/knowledge/scratch-root-contract.md`).
- **W2 registry cells.** `59c38109` adds a `scratch_root` cell to exactly seven selftest
  rows (`grep -c '"scratch_root"'` on the C0 `tools/registry.json` = `7`): `repeat-control-selftest`,
  `bash-witness-selftest`, `pin-disposition-selftest`, `evidence-disposition-selftest`,
  `context-capture-selftest`, `registry-check-selftest`, `env-diff-selftest`. Each cell
  names TMPDIR, the empty arm and the could-not-evaluate exit class, and points at the note.
- **W3 documentation.** `corpus/knowledge/scratch-root-contract.md` (new: three-arm table,
  "why the class is uniform", "what measures it", "falsifier"); `corpus/SOURCES.md` rows
  S277-S279 plus the footer line "Next unused id: S280" (S rows at C0: `grep -cE '^ {0,3}\| S[0-9]{3,} \|'`
  = 139, max id S279); `corpus/lessons/round-54.md` (`## Gate` naming S277-S279 with URLs
  and 2026-10-28, `## Mistakes`, QUALITY criterion 105, the method note the ordering
  depends on); `SKILL.md:32-39`, the bullet "**The scratch root has three arms.**" under
  `## Standing rules`.
- **W4 the C0 reader set.** `.ufo/evidence/round-54/c1/lost-headings-at-c0.json` — 23
  headings, the re-read set this wave works from (the frozen seven of
  `c1/lost-headings-at-base.json` plus 16 sections this round's own C0 edits moved). The
  instrument is `.ufo/waves/round-54/reader-section.py`; `w1/section-manifest.json` pins
  `cand=59c38109…`, `skill_sha256=e0e0b4d0…` (198186 bytes) and start/end/sha256 per
  section.
- **W5 re-key binder.** `.ufo/evidence/round-54/integrate/binder.py` binds committed reader
  reports to ledger entries under `.ufo/evidence/round-21/coldread/rekey-r54-<c0>`: union of
  the 23 headings at C0 and the frozen seven at base, section identity from the frozen
  round-18 sectionize at C0, `LOG.md`/`SCORECARD.md`/`SKILL.md` dropped from the input union
  (`binder.py:49`), one trace + one entry per heading, its own prior output replaced on a
  second pass.

### Work items — wave `round-54-w1` (76 seats: one v2 wave, build and attack together)

One bullet per dispatched item, naming where that seat's receipt lands. No outcome is
asserted per bullet: the wave was still running when this draft was assembled. A dated
directory listing of what was already present in `w1/` follows the bullets.

#### Readers (23) — cold-read of the 23 lost sections at C0; each writes `<seat>.json` (`heading`, `cand`, `section_sha256`, `findings`) and `<seat>.md`

- **T54W1Read01** — `## Standing rules` (SKILL.md 17-40 at C0, `section_sha256` `164390276b453ddb…`); evidence: `.ufo/waves/round-54/w1/T54W1Read01.json` + `T54W1Read01.md`.
- **T54W1Read02** — `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (SKILL.md 142-256 at C0, `section_sha256` `c413b4268eb84263…`); evidence: `.ufo/waves/round-54/w1/T54W1Read02.json` + `T54W1Read02.md`.
- **T54W1Read03** — `### The boundaries — what a service run is not` (SKILL.md 869-893 at C0, `section_sha256` `9aa3c41cfd365e32…`); evidence: `.ufo/waves/round-54/w1/T54W1Read03.json` + `T54W1Read03.md`.
- **T54W1Read04** — `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` (SKILL.md 932-945 at C0, `section_sha256` `430dd86f25b6ce3d…`); evidence: `.ufo/waves/round-54/w1/T54W1Read04.json` + `T54W1Read04.md`.
- **T54W1Read05** — `### Using the ledger` (SKILL.md 946-977 at C0, `section_sha256` `808dad50760d693b…`); evidence: `.ufo/waves/round-54/w1/T54W1Read05.json` + `T54W1Read05.md`.
- **T54W1Read06** — `### The tick and the pin read` (SKILL.md 1034-1082 at C0, `section_sha256` `ca86e98de294306f…`); evidence: `.ufo/waves/round-54/w1/T54W1Read06.json` + `T54W1Read06.md`.
- **T54W1Read07** — `### Triggers T1–T3 and the re-pin rule` (SKILL.md 1083-1105 at C0, `section_sha256` `2350210704efcc3b…`); evidence: `.ufo/waves/round-54/w1/T54W1Read07.json` + `T54W1Read07.md`.
- **T54W1Read08** — `### The service's limits — what tameshi refuses to mutation-test` (SKILL.md 1265-1294 at C0, `section_sha256` `37d63abf882e89d8…`); evidence: `.ufo/waves/round-54/w1/T54W1Read08.json` + `T54W1Read08.md`.
- **T54W1Read09** — `## The operator's runbook and the six-leg regression (round 10, measured)` (SKILL.md 1295-1303 at C0, `section_sha256` `636e850f885cb399…`); evidence: `.ufo/waves/round-54/w1/T54W1Read09.json` + `T54W1Read09.md`.
- **T54W1Read10** — "### The operator's runbook — `corpus/knowledge/operator-runbook.md`" (SKILL.md 1304-1324 at C0, `section_sha256` `c246d3743e0a4412…`); evidence: `.ufo/waves/round-54/w1/T54W1Read10.json` + `T54W1Read10.md`.
- **T54W1Read11** — `## Repeated controls and gate registry — round 12` (SKILL.md 1504-1523 at C0, `section_sha256` `2613c4fe5c89d297…`); evidence: `.ufo/waves/round-54/w1/T54W1Read11.json` + `T54W1Read11.md`.
- **T54W1Read12** — `### Gate/probe registry` (SKILL.md 1524-1541 at C0, `section_sha256` `99285e24a71a8d2a…`); evidence: `.ufo/waves/round-54/w1/T54W1Read12.json` + `T54W1Read12.md`.
- **T54W1Read13** — `## Pin disposition and provenance correction — round 13` (SKILL.md 1542-1572 at C0, `section_sha256` `ad8d6c4010f2c584…`); evidence: `.ufo/waves/round-54/w1/T54W1Read13.json` + `T54W1Read13.md`.
- **T54W1Read14** — `### Round-13 gate/probe registry` (SKILL.md 1573-1588 at C0, `section_sha256` `896722c4941841f2…`); evidence: `.ufo/waves/round-54/w1/T54W1Read14.json` + `T54W1Read14.md`.
- **T54W1Read15** — `## Effective expectation reconciliation — round 14` (SKILL.md 1589-1622 at C0, `section_sha256` `9640e5dc426f1f9e…`); evidence: `.ufo/waves/round-54/w1/T54W1Read15.json` + `T54W1Read15.md`.
- **T54W1Read16** — `### Round-14 historical registry — superseded by round 15` (SKILL.md 1623-1634 at C0, `section_sha256` `06a6864fb05fd63d…`); evidence: `.ufo/waves/round-54/w1/T54W1Read16.json` + `T54W1Read16.md`.
- **T54W1Read17** — `## Context gate classification and explicit exit classes — round 15` (SKILL.md 1635-1701 at C0, `section_sha256` `132cfb9ef1aa0711…`); evidence: `.ufo/waves/round-54/w1/T54W1Read17.json` + `T54W1Read17.md`.
- **T54W1Read18** — `### Round-15 gate/probe registry` (SKILL.md 1702-1732 at C0, `section_sha256` `da6ef23c23f06af0…`); evidence: `.ufo/waves/round-54/w1/T54W1Read18.json` + `T54W1Read18.md`.
- **T54W1Read19** — `## Live-tree re-pin and entry-command monitor — round 17` (SKILL.md 1840-1871 at C0, `section_sha256` `037c9df3076fc7ad…`); evidence: `.ufo/waves/round-54/w1/T54W1Read19.json` + `T54W1Read19.md`.
- **T54W1Read20** — `### Round-17 gate/probe registry — re-pin and monitor` (SKILL.md 1872-1880 at C0, `section_sha256` `8a92f71e046aae24…`); evidence: `.ufo/waves/round-54/w1/T54W1Read20.json` + `T54W1Read20.md`.
- **T54W1Read21** — `### Round-18 gate/probe registry — routed-defect closure` (SKILL.md 1951-1963 at C0, `section_sha256` `1f0a60ec99834f64…`); evidence: `.ufo/waves/round-54/w1/T54W1Read21.json` + `T54W1Read21.md`.
- **T54W1Read22** — `### Round-21 gate/probe registry — finite environment differential` (SKILL.md 1990-2129 at C0, `section_sha256` `eccd3ec82207fa69…`); evidence: `.ufo/waves/round-54/w1/T54W1Read22.json` + `T54W1Read22.md`.
- **T54W1Read23** — `### Round-26 gate/probe registry — report interop` (SKILL.md 2158-2197 at C0, `section_sha256` `cc23587b353fb780…`); evidence: `.ufo/waves/round-54/w1/T54W1Read23.json` + `T54W1Read23.md`.

#### Executors (13) — instrument checks and measurements against the frozen counters and the C0 tree

- **T54W1ExecC1Counter** — Attack nothing; verify the instrument. Run the FROZEN C1 counter at C0: python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py --lane /home/vgpnk/Projects/shokunin…; evidence: `.ufo/waves/round-54/w1/T54W1ExecC1Counter.md`.
- **T54W1ExecC2Counter** — Run the FROZEN C2 counter at C0: python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 59c38109bf119d0…; evidence: `.ufo/waves/round-54/w1/T54W1ExecC2Counter.md`.
- **T54W1ExecNoHarm** — Run bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/no-harm.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e and paste all 14 NOHAR…; evidence: `.ufo/waves/round-54/w1/T54W1ExecNoHarm.md`.
- **T54W1ExecCensus** — Run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi; paste the exit code and the warning lines; evidence: `.ufo/waves/round-54/w1/T54W1ExecCensus.md`.
- **T54W1ExecRegistryGate** — Run python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py --selftest (expect exit 0) and then python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py --…; evidence: `.ufo/waves/round-54/w1/T54W1ExecRegistryGate.md`.
- **T54W1ExecRegistryFull** — Run python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 59c38109bf119d0e9d4f878644a82babc937bc1e (the full 56-row…; evidence: `.ufo/waves/round-54/w1/T54W1ExecRegistryFull.md`.
- **T54W1ExecDryBinder** — For each of the 23 headings in .ufo/evidence/round-54/c1/lost-headings-at-c0.json, read the ledger at C0 and list the union of the section's prior entries' input paths, flagging every path that is (a)…; evidence: `.ufo/waves/round-54/w1/T54W1ExecDryBinder.md`.
- **T54W1ExecManifest** — Using /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/reader-section.py, compute for each of the 23 lost headings its start, end and section_sha256 at C0 and write /home/vgpnk/Proje…; evidence: `.ufo/waves/round-54/w1/T54W1ExecManifest.md`.
- **T54W1ExecExitClass** — Diff each of the four edited tools (env-diff, bash-witness-study, evidence-disposition, pin-disposition) between d33053f7552db4bd290c99a36979760f544c41ad and 59c38109bf119d0e9d4f878644a82babc937bc1e (…; evidence: `.ufo/waves/round-54/w1/T54W1ExecExitClass.md`.
- **T54W1ExecEmptyStrace** — Under TMPDIR="", run each of the seven self-tests under strace -f -e trace=mkdir,mkdirat -o LOG and report the mkdir paths each tool used; evidence: `.ufo/waves/round-54/w1/T54W1ExecEmptyStrace.md`.
- **T54W1ExecStraceNoise** — The C2 counter's tmp_mkdirs arm counts mkdir("/tmp... lines in its own strace log; evidence: `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`.
- **T54W1ExecFreeze** — Re-implement the round-53 crash-resume check for this round (scratch script, do not add a file): for every path in .ufo/evidence/round-54/freeze.json, compute sha256 of the blob at 441c26bec5e4c1cc31b…; evidence: `.ufo/waves/round-54/w1/T54W1ExecFreeze.md`.
- **T54W1ExecCitations** — For each of the 23 lost sections, extract every lane-relative path the section names and check it exists as a blob at C0 (git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e 59c38109bf11…; evidence: `.ufo/waves/round-54/w1/T54W1ExecCitations.md`.

#### Scouts and connectors (6) — source re-opening and cross-claim checks

- **T54W1ScoutS277** — Re-open S277 yourself: curl -fsSL --max-time 60 https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html, sha256 it, and locate the TMPDIR sentence in the text; evidence: `.ufo/waves/round-54/w1/T54W1ScoutS277.md`.
- **T54W1ScoutS278** — Re-open S278 yourself: curl -fsSL --max-time 60 https://raw.githubusercontent.com/python/cpython/v3.12.7/Lib/tempfile.py, sha256 it, and locate _candidate_tempdir_list; evidence: `.ufo/waves/round-54/w1/T54W1ScoutS278.md`.
- **T54W1ScoutS279** — Re-open S279 yourself: curl -fsSL --max-time 60 https://docs.python.org/3/library/tempfile.html, sha256 it, and locate the search-list sentence the row quotes; evidence: `.ufo/waves/round-54/w1/T54W1ScoutS279.md`.
- **T54W1ScoutNextEntry** — Read /home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.md and /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/delta-debugging-minimization-contract.md (read-only; never run campaign too…; evidence: `.ufo/waves/round-54/w1/T54W1ScoutNextEntry.md`.
- **T54W1ConnPreBind** — Cross the two claims: for each of the 23 lost headings, which of them pin any of the four tools C0 edited or tools/registry.json, and which of them pin files the L1 will still write (LOG.md, SCORECARD…; evidence: `.ufo/waves/round-54/w1/T54W1ConnPreBind.md`.
- **T54W1ConnDuplicateNote** — Search /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/ for notes that already state any part of the scratch-root contract (env-diff contract drift, service limits, the tools registry…; evidence: `.ufo/waves/round-54/w1/T54W1ConnDuplicateNote.md`.

#### Counter mutation, C1 (6) — each mutant must make the counter fail, mutant tree and output kept

- **T54W1MutC101** — Attack the frozen C1 counter by mutation: delete the if reader_ok != len(frozen) failure (make the readers arm advisory) and show the counter still passes at a tree with no reader JSONs; evidence: `.ufo/waves/round-54/w1/T54W1MutC101.md`.
- **T54W1MutC102** — Attack the frozen C1 counter by mutation: replace str(e.get("read_rev")) == c0 with a startswith(c0[:12]) test and find a tree where that admits an entry the exact test refuses; evidence: `.ufo/waves/round-54/w1/T54W1MutC102.md`.
- **T54W1MutC103** — Attack the frozen C1 counter by mutation: delete the unstable accounting and show a tree whose entries pin LOG.md still passes; evidence: `.ufo/waves/round-54/w1/T54W1MutC103.md`.
- **T54W1MutC104** — Attack the frozen C1 counter by mutation: make entry_reason(..., strict=True) into strict=False semantics in the credit call and show what it admits; evidence: `.ufo/waves/round-54/w1/T54W1MutC104.md`.
- **T54W1MutC105** — Attack the frozen C1 counter by mutation: replace the section-sha match with a heading match in the frozen round-18 module (copy it) and show a tree where a stale section credits; evidence: `.ufo/waves/round-54/w1/T54W1MutC105.md`.
- **T54W1MutC106** — Attack the frozen C1 counter by mutation: relax the precheck arm's lost=0 ok to lost<=7 and show the base tree then satisfies arm 1 while the verdict should be false; evidence: `.ufo/waves/round-54/w1/T54W1MutC106.md`.

#### Counter mutation, C2 (3) — the same discipline on the operability counter

- **T54W1MutC204** — Attack the frozen C2 counter by mutation: change ok = (rc == 2 and ...) to ok = (rc in (0, 2) and ...) and show the mutant still passes at C0; evidence: `.ufo/waves/round-54/w1/T54W1MutC204.md`.
- **T54W1MutC205** — Attack the frozen C2 counter by mutation: make the tmp_mkdirs arm vacuously true (usable_ok += 1) and show the mutant passes at C0; evidence: `.ufo/waves/round-54/w1/T54W1MutC205.md`.
- **T54W1MutC206** — Attack the frozen C2 counter by mutation: require only "TMPDIR" in the cell and show the mutant passes at C0; evidence: `.ufo/waves/round-54/w1/T54W1MutC206.md`.

#### Boundary probes (3) — TMPDIR edge shapes beyond the counter's three arms

- **T54W1MutB01** — Boundary probe (a mutation-tester seat; the policy refuses a standalone labrat lane): empty TMPDIR in the stdlib; evidence: `.ufo/waves/round-54/w1/T54W1MutB01.md`.
- **T54W1MutB02** — Boundary probe (a mutation-tester seat; the policy refuses a standalone labrat lane): non-writable TMPDIR. Create a directory, chmod 500 it, and run two of the seven tools' self-tests with TMPDIR poin…; evidence: `.ufo/waves/round-54/w1/T54W1MutB02.md`.
- **T54W1MutB03** — Boundary probe (a mutation-tester seat; the policy refuses a standalone labrat lane): TMPDIR is a file; evidence: `.ufo/waves/round-54/w1/T54W1MutB03.md`.

#### Critics (4) — falsification of each claim from the sufficiency side

- **T54W1Crit01** — Falsify the claims: C1's input sufficiency. The C1 predicate binds a fresh entry per heading to a reader report and a trace. Attack the *sufficiency* direction: construct the strongest tree that satis…; evidence: `.ufo/waves/round-54/w1/T54W1Crit01.md`.
- **T54W1Crit02** — Falsify the claims: the seven-heading frozen set vs 23 actual; evidence: `.ufo/waves/round-54/w1/T54W1Crit02.md`.
- **T54W1Crit03** — Falsify the claims: C2's registry cell vs behaviour. Attack the scratch_root cell on the seven rows: does each cell describe what its tool now does? Run the three arms by hand for one tool and compare…; evidence: `.ufo/waves/round-54/w1/T54W1Crit03.md`.
- **T54W1Crit04** — Falsify the claims: the sourced claim. The C2 claim is the round's sourced claim (S277-S279). Attack its logic: does corpus/knowledge/scratch-root-contract.md claim anything the three rows do not supp…; evidence: `.ufo/waves/round-54/w1/T54W1Crit04.md`.

#### Reviewers (4) — review of the C0 diffs

- **T54W1Rev01** — Review the C0 change to tools/env-diff.py: git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff d33053f7552db4bd290c99a36979760f544c41ad 59c38109bf119d0e9d4f878644a82babc937bc1e -- tools/env-dif…; evidence: `.ufo/waves/round-54/w1/T54W1Rev01.md`.
- **T54W1Rev02** — Review the C0 change to tools/bash-witness-study.py: git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff d33053f7552db4bd290c99a36979760f544c41ad 59c38109bf119d0e9d4f878644a82babc937bc1e -- too…; evidence: `.ufo/waves/round-54/w1/T54W1Rev02.md`.
- **T54W1Rev03** — Review the C0 change to tools/evidence-disposition.py plus tools/pin-disposition.py: git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff d33053f7552db4bd290c99a36979760f544c41ad 59c38109bf119d0…; evidence: `.ufo/waves/round-54/w1/T54W1Rev03.md`.
- **T54W1Rev04** — Review the C0 change to tools/registry.json plus SKILL.md: git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff d33053f7552db4bd290c99a36979760f544c41ad 59c38109bf119d0e9d4f878644a82babc937bc1e…; evidence: `.ufo/waves/round-54/w1/T54W1Rev04.md`.

#### Sentinels (4) — forged-report, LOG.md-pin, fabricated-trace and print-then-exit-0 attacks

- **T54W1Sent01** — Sentinel attack: forge a reader report. Fabricate a reader JSON at /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ReadForged.json with a guessed section_sha256 and no MD, t…; evidence: `.ufo/waves/round-54/w1/T54W1Sent01.md`.
- **T54W1Sent02** — Sentinel attack: pin LOG.md. In a scratch clone at C0, hand-bind one entry whose inputs include LOG.md and whose trace records that sha, then commit a LOG.md change and run the frozen C1 counter at th…; evidence: `.ufo/waves/round-54/w1/T54W1Sent02.md`.
- **T54W1Sent03** — Sentinel attack: fabricate a trace. In a scratch clone at C0, hand-bind an entry with a trace JSON whose recorded input sha differs from the blob at C0 and show the frozen C1 counter refuses to credit…; evidence: `.ufo/waves/round-54/w1/T54W1Sent03.md`.
- **T54W1Sent04** — Sentinel attack: print the class but exit 0. In a scratch clone at C0, patch one of the four tools so it prints the could-not-evaluate line and returns 0 on the unusable arm, and run the frozen C2 cou…; evidence: `.ufo/waves/round-54/w1/T54W1Sent04.md`.

#### Revenge (3) — dependencies on the old behaviour of the four edited tools

- **T54W1Revenge01** — Find every dependency on the OLD behaviour of the four edited tools: grep -n the lane for their exits (could-not-evaluate, RuntimeError, --selftest, selftest) across SKILL.md, corpus/, tools/*.json, t…; evidence: `.ufo/waves/round-54/w1/T54W1Revenge01.md`.
- **T54W1Revenge02** — For each of the four edited tools, find the paths that reach strict_scratch_root() and DO NOT go through the mapped entry point (a helper called before the try, a module-level import-time call); evidence: `.ufo/waves/round-54/w1/T54W1Revenge02.md`.
- **T54W1Revenge03** — The mapping is at each tool's entry point. Enumerate every documented invocation of the seven tools (their --help, USAGE strings, registry argv, SKILL text) and show that each one, under an unusable T…; evidence: `.ufo/waves/round-54/w1/T54W1Revenge03.md`.

#### Simplifiers (2) — duplication in the class/mapping and in the registry cell

- **T54W1Simplify01** — The four tools now each declare a five-line ScratchRootUnusable class and a three-line mapping; evidence: `.ufo/waves/round-54/w1/T54W1Simplify01.md`.
- **T54W1Simplify02** — The scratch_root cell is one ~45-word sentence repeated on seven rows; evidence: `.ufo/waves/round-54/w1/T54W1Simplify02.md`.

#### Dedupe (1) — the round's routed defects against the new criteria

- **T54W1RevDedup01** — Dedupe seat (a reviewer; the policy refuses a standalone distiller lane); evidence: `.ufo/waves/round-54/w1/T54W1RevDedup01.md`.

#### Scribes (4) — report sections (this one is `T54W1ScribeWork`)

- **T54W1ScribeWork** — Draft the round report's **Work performed** section (the round's declared claims first, then one bullet per work item with an evidence pointer) from .ufo/evidence/round-54/contract.json, the C0 commit…; evidence: `.ufo/waves/round-54/w1/T54W1ScribeWork.md`.
- **T54W1ScribeMeasure** — Draft the **Before → after measurements** and **Landed changes** sections: for each claim, the counting command, the base value from .ufo/evidence/round-54/before/ (or the CTL_0 line in .ufo/evidence/…; evidence: `.ufo/waves/round-54/w1/T54W1ScribeMeasure.md`.
- **T54W1ScribeQuality** — Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md's last ten criteria and the round-53 lesson's QUALITY 104; evidence: `.ufo/waves/round-54/w1/T54W1ScribeQuality.md`.
- **T54W1ScribeScorecard** — Draft the SCORECARD.md additions for round 54: the standing axis table restated at C0 (depth 10, calibration 8, freshness 9 with their counting commands), the two claim rows with before/target/after p…; evidence: `.ufo/waves/round-54/w1/T54W1ScribeScorecard.md`.

### Receipts present in `w1/` at 2026-10-28T14:35:02Z

Directory listing at that instant, `swarm-registry.json`, `section-manifest.json` and this
file excluded; it is a snapshot, not a claim about the wave's final state.

- `T54W1ConnDuplicateNote-receipts/`
- `T54W1ConnDuplicateNote.md`
- `T54W1ConnPreBind-receipts/`
- `T54W1ConnPreBind.json`
- `T54W1ConnPreBind.md`
- `T54W1Crit02-receipts/`
- `T54W1Crit03-receipts/`
- `T54W1Crit04-receipts/`
- `T54W1ExecCensus-receipts/`
- `T54W1ExecCensus.md`
- `T54W1ExecCitations-receipts/`
- `T54W1ExecDryBinder-input-map.json`
- `T54W1ExecDryBinder-receipts/`
- `T54W1ExecDryBinder.md`
- `T54W1ExecEmptyStrace-receipts/`
- `T54W1ExecManifest-receipts/`
- `T54W1ExecManifest.md`
- `T54W1ExecNoHarm-receipts/`
- `T54W1ExecNoHarm.md`
- `T54W1MutB03-receipts/`
- `T54W1MutC101-receipts/`
- `T54W1MutC102-receipts/`
- `T54W1MutC104-receipts/`
- `T54W1MutC106-receipts/`
- `T54W1MutC206-receipts/`
- `T54W1Read02.json`
- `T54W1Read02.md`
- `T54W1Read03.json`
- `T54W1Read03.md`
- `T54W1Read04.json`
- `T54W1Read04.md`
- `T54W1Read05.json`
- `T54W1Read05.md`
- `T54W1Read06.json`
- `T54W1Read06.md`
- `T54W1Read07.json`
- `T54W1Read07.md`
- `T54W1Read08.json`
- `T54W1Read08.md`
- `T54W1Read09.json`
- `T54W1Read09.md`
- `T54W1Read10.json`
- `T54W1Read10.md`
- `T54W1Read11-receipts/`
- `T54W1Read11.json`
- `T54W1Read11.md`
- `T54W1Read13-receipts/`
- `T54W1Read13.json`
- `T54W1Read13.md`
- `T54W1Read14.json`
- `T54W1Read14.md`
- `T54W1Read15-receipts/`
- `T54W1Read15.json`
- `T54W1Read15.md`
- `T54W1Read18.json`
- `T54W1Read18.md`
- `T54W1Read19.json`
- `T54W1Read19.md`
- `T54W1Read20.json`
- `T54W1Read20.md`
- `T54W1Read21.json`
- `T54W1Read21.md`
- `T54W1Rev01-receipts/`
- `T54W1Rev02-receipts/`
- `T54W1Rev03-receipts/`
- `T54W1Rev04-receipts/`
- `T54W1ScoutNextEntry.md`
- `T54W1ScoutS277.md`
- `T54W1ScoutS278-receipts/`
- `T54W1ScoutS278.md`
- `T54W1ScoutS279-receipts/`
- `T54W1ScoutS279.md`
- `T54W1ScribeQuality-receipts/`

### Observed preconditions at draft time (2026-10-28T14:33:47Z) — not claims

Recorded so the merge does not have to re-derive them, and so nothing above is read as
already satisfied.

- **No `controls-b` receipt.** `ls .ufo/evidence/round-54/control/controls-b*` → no match.
  `deciding-run.sh:23-27` requires all four control receipts (`controls-a|b.stdout|.exit`)
  to be committed at REV and chained after the freeze, and refuses otherwise with
  `DECIDING_REFUSED control-receipt-missing $f`. `corpus/QUALITY.md` criterion 105's
  falsifier also cites `control/controls-b.stdout`. Until that file exists and is committed,
  the deciding run cannot start.
- **No deciding-run receipt.** No directory under `.ufo/evidence/round-54/` carries
  `c1.start`/`c2.start`. This section therefore quotes no C1 or C2 verdict; the claims'
  PASS/FAIL is the deciding run's output, not this draft's.
- **The `before` receipts exist but are not committed, and the C2 one disagrees with the
  contract's line.** `before/c1.stdout` (363 B) reproduces the contract's C1 `before`
  exactly (`credited=57 lost=7 … monitor=6/57`). `before/c2.stdout` (1355 B) re-runs the C2
  counter at base and prints `C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7
  empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=0 note=0 sources=0 total=14 C2_R54_PASS=false`,
  where the contract's `before` line says `total=13`; the same frozen counter at the same
  revision therefore reports 14 now and 13 at freeze, and the difference sits in
  `usable_ok=6` (one tool fails the usable arm at base). `git log --all --
  .ufo/evidence/round-54/before/*` prints nothing and `git ls-tree -r 441c26be` lists no
  such path, so both files are untracked working-tree artifacts: the deciding run's
  clean-tree gate (`deciding-run.sh:29-30`) requires them to be committed or removed, and
  ScribeMeasure should quote the line it actually reads rather than the contract's summary.
- **Uncommitted and untracked inputs at this moment.** `git status --porcelain`:
  modified = ['SKILL.md', 'corpus/QUALITY.md', 'corpus/SOURCES.md', 'corpus/knowledge/change-aware-resweep-cadence.md', 'corpus/lessons/round-54.md']; untracked = ['.ufo/evidence/round-54/before/', '.ufo/evidence/round-54/c1/lost-headings-at-c0.json', '.ufo/evidence/round-54/control/controls-a.exit', '.ufo/evidence/round-54/control/controls-a.stdout', '.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout', '.ufo/evidence/round-54/integrate/', '.ufo/waves/round-54/']. This list moves while the wave runs (`SKILL.md` was clean when the draft opened and is modified now), so take `git status --porcelain` at merge as authoritative: the C0 line numbers cited above describe `59c38109`, not the working tree. The round commit must carry these (control
  receipts, `before/`, `c1/lost-headings-at-c0.json`, `integrate/`, the `corpus/` edits,
  `.ufo/waves/round-54/`) before any deciding invocation. `integrate/binder.py:50` reads
  `c1/lost-headings-at-c0.json` from the lane working tree, so that file is not optional for
  the re-key pass either.
- **What this seat did not run.** The counters, `no-harm.sh`, `registry-check.py` and
  `sources-census.sh` were left to the executor seats and the deciding run; this draft quotes
  only receipts that already existed (`controls-a`, `r53-counter-at-88afa941`, `before/*`)
  and C0 object bytes. The 139-row census count is a `grep` over `59c38109:corpus/SOURCES.md`;
  the census validate's exit code belongs to `T54W1ExecCensus` and to `census.exit` in the
  deciding OUTDIR.
- **Tooling.** This seat installed and upgraded nothing; no pacman transaction was attempted
  (host-wide pause) and no install channel was used.

### How to refresh the presence list at merge

The list above was taken at 2026-10-28T14:34:29Z. From the lane root, `ls
.ufo/waves/round-54/w1/` re-derives it; the per-bullet evidence paths need no editing, and
each seat's filename is its own seat name, so a landed receipt resolves against its bullet
by name.
