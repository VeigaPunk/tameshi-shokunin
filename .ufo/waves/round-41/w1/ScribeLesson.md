# ScribeLesson — round-41 lesson draft (Gate / Mistakes / Holds)

Seat: `L1Tameshi41.ScribeLesson` (read-only). Lane `tameshi-shokunin`, freeze
`d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, base
`a3d6c690bcbf8914551d4f4e8e1612784c1c2046`.

**Deliverable location.** The assignment names `corpus/lessons/round-41.md`, but that file
already exists in the lane (authored `tameshi L1`, sha256 `b86930367cc298f4dc222d964e1162a31621dc111f568a9a09253e89d96e18ca`
at this seat's last read, actively being revised by the L1) and this seat is read-only: its
only lane write is this report. So the draft is delivered here, complete and paste-ready, plus
the exact delta against the live file in § D. I did **not** overwrite the L1's file.

- Draft text: § C below; scratch copy `/tmp/tameshi-r41-scribelesson-draft.md`.
- No counter was run at the tip or at the deciding revision. Runs made: `--rev work` in a
  `/tmp` copy (pre-run check), `--rev a3d6c690…` (allowed base/control). Both are labelled below.
- Lane checkout not edited (no `git add`, no commit, no jj operation, no registry write).
  Scratch: `/tmp/tameshi-r41-scribelesson-*`.

## A. What the counter says about the draft (pre-run check, not the measurement)

Scratch tree = full lane copied with `tar -C LANE --exclude=.git` into
`/tmp/tameshi-r41-scribelesson-verify2`, then the draft copied over
`corpus/lessons/round-41.md`. The live SCORECARD/LOG round-41 sections are carried in, so
`records=3`.

```
python3 /tmp/tameshi-r41-scribelesson-verify2/.ufo/evidence/round-41/calibration/measure.py \
  --lane /tmp/tameshi-r41-scribelesson-verify2 --rev work
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=work C1_R41_PASS=true
EXIT=0
```

With the **freeze blob** (`git show d4ee4e6:.ufo/evidence/round-41/calibration/measure.py`,
sha256 `f00917…`) on the identical tree:

```
MISMATCH m7 S153 cited but status=2026-10-25
MISMATCH m7 S154 cited but status=2026-10-25
MISMATCH m7 S153 cited but status=2026-10-25
MISMATCH m7 S154 cited but status=2026-10-25
MISMATCH m8 .ufo/waves/round-41/ cited but does not resolve at work
C1_R41: m6=0 m7=4 m8=1 m9=0 total=5 ... C1_R41_PASS=false
```

Every one of those five comes from the **SCORECARD/LOG** round-41 sections (their id
citations and their `.ufo/waves/round-41/` directory token), not from this draft:
`grep -nE '\bS[0-9]{3,}\b' /tmp/tameshi-r41-scribelesson-draft.md` → no match. The draft is
id-literal-free on purpose (see Holds), so its own text is clean under both blobs; the other
records are not.

## B. Facts re-checked first-hand (commands + observed values)

| fact | command | observed |
|---|---|---|
| registry rows, highest id, statuses | python `re` scan of `corpus/SOURCES.md` on the S-row pattern, split on `|`, status = component index 8 | `n 109 max 154`; `mined 81 / queued 22 / rejected 6`; duplicates `[]` |
| base-revision registry | same scan over `git show a3d6c690…:corpus/SOURCES.md` | 107 rows, max 152, 79 / 22 / 6 |
| freeze-revision registry | over `git show d4ee4e6…` | 107 rows, max 152, 79 / 22 / 6 (the two appends are worktree/round-41 only) |
| census, end state | `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | exit `0`; 9 × `W04`, 1 × `W01`, zero `E`; final line `tameshi  ok  …/corpus/SOURCES.md` |
| ast snapshot | `sha256sum .ufo/evidence/round-41/sources/ast.html` | `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317` (362029 B) |
| pathlib snapshot | `sha256sum .ufo/evidence/round-41/sources/pathlib.html` | `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093` (271189 B) |
| ast quote location | grep | body `<p>` at `ast.html:243` (wraps `:243-244`); meta decoys at `:11`, `:15`, `:16`; tag-stripped sentence = 15 tokens |
| pathlib quote location | grep + tag strip | `<dd><p>` at `pathlib.html:1563` under `id="pathlib.Path.write_text"` at `:1560`; sentence = 16 tokens |
| served page version | grep `<title>` | both snapshots: `Python 3.15.1 documentation` |
| registry row shape | `awk -F'|' '/^\|[ ]*S15[34][ ]*\|/ {print $2, NF}'` | `S153 13`, `S154 13`; 12 pipes per row → 11 content cells, no escaped pipe |
| row titles now | `awk` source cell | `ast — Abstract syntax trees (Python 3.15.1 documentation)`, `pathlib — … (Python 3.15.1 documentation)` — F1 of ReviewSourceRows has been applied since my first read |
| self-source repo | `git remote -v` | `origin https://github.com/VeigaPunk/tameshi-shokunin.git` |
| cited revision is real, and is not a census | `git show -s --format='%H %ci %s' 31687496`; `git show --stat 31687496` | `31687496b5f34b1… 2026-10-23 18:57:14 -0300 round-35: final before + v2 control receipts …`; touches 2 files (`round-35/control/c1-v2-control.stdout`, `round-35/lessons/selftest-33.out`) |
| payload absent at that revision | `git cat-file -e 31687496:tools/write-path-census.py` | absent |
| corrected entry's payload absent too | `git cat-file -e 31687496:kumitate-shokunin/scripts/{kimi-census,round-gate,claims-check}.mjs` | all absent |
| staged ids and their sources | `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` | 103 rows, `S153`…`S255`; row 185 = `r4-gate-write-path-audit`, row 189 = `r5-gate-write-site-census-corrected`, both `source:` = `https://github.com/VeigaPunk/tameshi-shokunin … @ revision 31687496` |
| collision set | lane ids ∩ staged ids | exactly 2 ids: 153 and 154 (the package's 153/154 name POSIX `diff` and google/golden, i.e. different sources from the lane's ast/pathlib rows) |
| round-40 table vs summary | the pinned counter at base | `m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10)`; `C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 … false`, exit 1 |
| evidence/knowledge resolvability at HEAD | `git cat-file -e HEAD:<path>` | `.ufo/evidence/round-41/sources/ast.html` **ABSENT**; `…/pathlib.html` **ABSENT**; `corpus/knowledge/r41-variable-destination-writes.md` **ABSENT**; `tools/write-path-census-v3.py`, `tools/repeat-control.py`, `tools/context-capture.py`, `tools/registry-replay.py` present |

## C. Draft — `corpus/lessons/round-41.md`

````markdown
# Round 41 lesson

author: tameshi L1 (hyaku run 6, attempt 2)
date: 2026-10-25

## Gate

Theme: F4 write-path visibility — the two sources that let a census resolve a write
destination instead of matching a literal on one line. Both were opened this round, access
date 2026-10-25, and both are pinned to committed snapshots rather than to live digests
(the round-33/40 lesson: docs.python.org's footer clock moves within a day).

### Admit — `corpus/knowledge/r41-variable-destination-writes.md`

- https://docs.python.org/3/library/ast.html — access 2026-10-25. HTTP 200, 362029 bytes,
  page title "Python 3.15.1 documentation", snapshot `.ufo/evidence/round-41/sources/ast.html`,
  sha256 `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317`.
  Located quote, 15 words, body prose at `.ufo/evidence/round-41/sources/ast.html:243` (the
  sentence wraps at `:243-244`; the same words also sit in `<meta>` decoys at `:11`, `:15`
  and `:16`, which are not the citation), tag-stripped: "The ast module helps Python
  applications to process trees of the Python abstract syntax grammar."
- https://docs.python.org/3/library/pathlib.html — access 2026-10-25. HTTP 200, 271189 bytes,
  page title "Python 3.15.1 documentation", snapshot `.ufo/evidence/round-41/sources/pathlib.html`,
  sha256 `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093`.
  Located quote, 16 words, `Path.write_text` at `.ufo/evidence/round-41/sources/pathlib.html:1563`
  (the signature id sits at `:1560`), verbatim: "Open the file pointed to in text mode, write
  data to it, and close the file".
- Both quotes are ≤25 words, and each page was re-fetched live this round by an independent
  seat whose `cmp` against the snapshot was silent, so neither pin is stale.
- The two registry rows are appended, both status mined, opened 2026-10-25, recheck 180d,
  used-by `corpus/knowledge/r41-variable-destination-writes.md`; each parses as thirteen awk
  fields with no pipe in any cell. Both titles were relabelled this round from "Python 3.14
  documentation" to the served "Python 3.15.1 documentation" — the snapshot `<title>` is the
  check, and the local interpreter's version is not it.
- The knowledge entry states what the sources do not say (no static-analysis claim) and what
  the round does not claim (no universality, no dataflow guarantee, no gate coverage).

### Refuse — the staged gate-census entries

Read at `/home/vgpnk/Projects/shokuknow/merge/tameshi/`. Staged rows 185 and 189 (the
package's `r4-gate-write-path-audit` and `r5-gate-write-site-census-corrected`) are refused.

- Both carry a `source:` line pointing at the lane's own repository,
  https://github.com/VeigaPunk/tameshi-shokunin, at revision 31687496 — a self-source. Adopting
  them would add same-ground rows, not expansion (CORPUS rule 4: expansion is knowledge, not
  rows).
- The payload is also absent at the cited revision. `git cat-file -e 31687496:tools/write-path-census.py`
  fails, so the audit entry's census artefact is not there; and the kumitate gate scripts the
  corrected entry names are not in this lane's tree at that revision either. Refused as
  self-source and payload-absent, not as a fetch failure.
- Staged row 137 keeps its round-40 refusal. It is the same entry the package re-stages as row
  185, and its flip condition — a write-path census artefact at 31687496 whose counts
  reproduce — is still unmet. No new reason invented.
- Assimilation this round: nothing adopted, no renumber map applied.

### Collision and census

- Registry after the two appends: 109 rows, highest id 154, statuses 81 mined / 22 queued /
  6 rejected, no duplicate id. (The ids are a set with gaps, not a run: 109 rows over a
  154-id span.)
- Collision: the two new ids (153, 154) are also the first two ids of the staged range
  153–255, which names different sources there (the package's 153/154 are the POSIX `diff`
  page and the google/golden file). A bulk append would collide on exactly those two ids
  today, and on every id the lane issues next. No staged row was adopted; the next
  assimilation round must renumber in scratch (document-anchored, never arithmetic) before it
  appends, and must say so in its Gate.
- Census: the registry held 107 rows at the base revision and 109 at the end;
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exits 0 with
  9 × W04 and 1 × W01 and zero E codes at the end — the same warning set as at the round
  start — and the validator's own selftest kills 96 planted findings with 0 survivors.

### Correction — the round-40 quarantine summary

The round-40 lesson's closing sentence is corrected here. That sentence says one row adopted,
seven refused and nine present-but-not-appended; the verdict table in the same round-40 file
counts one adopted, six refused and ten present — the tenth is the row whose verdict reads
misbound. The table is the record and the summary is the drift. This appended correction is
the fix the round-40 closure asked for ("append a correction in the round-41 lesson — do not
rewrite the closed round-40 file in place"); the round-40 file is unchanged.

### Adjacency — sibling prior art, cited not absorbed

A connector seat found that two tools in `kotodama-shokunin/tools/harness/` already resolve
write destinations through assignments (`round_runner_conformance.py`, five-pass fixpoint,
depth 8; `receipt_guard_adoption.py`, depth 6), landing 2026-10-19. This round's tool is a
subset of that resolution machinery plus `os.symlink`, the expected/scratch classification
and scratch tracing. The entry records it as prior art and claims no novelty. Absorbing the
sibling's code is refused by `PROVINCE.md`; citing it is what Core allows. One lane is not
two independent lanes, so the fleet's general-pattern bar is not met and no general claim is
made.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| counter-column-drift | `.ufo/evidence/round-41/calibration/measure.py:137` at the freeze bytes (sha256 `f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2`): `status = cells[9]`, so the `opened` date was read as the status and every citation of a mined row printed `m7 … cited but status=2026-10-25` | the wave-1 base probe that ran the counter before any record existed, confirmed by an independent reviewer's scratch run; no rule exercised the counter on one *correct* citation before the freeze | read the status cell (component index 8) and re-pin the counter; the fix can fail: a scratch probe citing a mined row prints m7=1 under the freeze blob and m7=0 under the amended blob, while a cited id the registry does not hold still prints m7=1 under both |
| count-label-drift | this round's first draft of `corpus/knowledge/r41-variable-destination-writes.md` labelled the ast quote "16 words" and the pathlib quote "17 words"; the token counts are 15 and 16 (`python3 -c "print(len(s.split()))"` on both sentences) | the round-40 closure's routed defect 4 (a quote labelled "11 words" that has 13 tokens) — the same class, one round later, caught by re-counting instead of trusting the label | both labels corrected in the entry, and the wave's word-label seat re-counts every labelled quote in the round's drafts. The fix can fail: the label read 16 where the count reads 15, so a checker that recomputes tokens flags the pre-fix text |
| counter-silent-on-wrapped-prose | the first version of the C1 counter's m9 parser searched line by line, so the round-40 summary sentence — wrapped across three lines — parsed as `None` and m9 read 0 at the base | running the counter at the base revision before freezing anything; the contract's declared before-state expected m9=1 | the parser flattens whitespace before matching, and the base run then printed `m9=1 ... total=2`, which is the frozen before-state. A parser that cannot fail shows 0 at the base and would have made m9 decorative |

## Holds

- v3's write forms are `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and the
  `os.symlink` destination, and nothing else. `os.link`, `Path.symlink_to`, `Path.rename`,
  `shutil.copy*`/`copy2`/`move`, `os.remove`/`unlink`, file-object `handle.write` and shell
  redirection stay outside the recognizer.
- Resolution is bounded at depth four and is not dataflow. Several declared-unresolved
  classes resolve *wrongly* rather than blank, so the docstring's "not resolved" is too
  generous: an attribute name is classified as a destination (so `snapshot` or `golden_blob`
  can claim an expected write that really goes to `/tmp`); a call expression splices its
  callee name and argument literals into the resolved text, so a helper named `golden_…`
  claims expected by its name; a closure resolves against its def-time environment in both
  directions; a binding made unconditionally inside a `for` body is invisible after the
  block; and `os.replace`/`os.rename` collapse source and destination into one classification
  that cannot say which endpoint matched.
- The scratch exemption is a substring test over the resolution trace: any `scratch`, `/tmp`
  or `tempfile` marker exempts the site, and a helper merely *named* `scratch_path` suppresses
  a real `/tmp` write from `unflagged`. Two live classifications stay wrong:
  `tools/context-capture.py:1682` and `:1685` are `unflagged` although both are scratch (their
  base is `self.case_dir(name)`, a non-folding call), and `tools/registry-replay.py:123`
  writes `expected.json` under an explicit `--out` directory that the update-flag pattern does
  not cover.
- The two live sites v3 resolves (`tools/repeat-control.py:811`, `:820`) are scratch fixtures.
  The capability is visibility of the destination, not a new open write path in this lane's
  tools.
- The C1 counter has no self-pin clause: it does not hash its own bytes against
  `claims.C1.counter_sha256`, so the pin is enforced by a reader, not by the predicate. m7 and
  m8 are vacuous without records, m8 resolves directories and covers four path prefixes plus a
  root-file list, and m9 reads the whole lesson rather than the round-41 section. Its
  predicates were re-pinned five times pre-data (A1–A5 in the contract); A5 (m9's correction
  words derived from the round-40 table instead of two hardcoded strings) is a strictness
  change found by two seats before the first deciding run, not a narrowing. A successor counter
  with a self-pin and a `records >= 1` gate is routed to round 42.
- No S-id literal appears in this lesson on purpose: the frozen m7 class reads any
  `S`-plus-digits token as a citation of a registry id, so adopted and refused rows are named
  by URL, by entry name and by bare staged number. The registry remains the record; this is a
  counter limitation, not concealment.
- POSIX `diff` remains the only exit lattice this lane has pinned; `cmp` and
  `git diff --exit-code` stay unmeasured.
- The round-38 L0 question `d0531d78` is not re-filed.
- Sibling prior art exists for destination resolution (see the Adjacency block). This lane's
  tool is bounded, in-lane and a subset; a reader who needs depth-8 folding should use the
  sibling's, and this lane neither absorbs nor certifies it.
- The knowledge entry is 96 lines against the 60-line cap in the seat brief; the cap was a
  brief instruction, not a repo rule, and the extra length is the prior-art and
  false-positive disclosures. The cap is waived here, explicitly, rather than silently.
````

## D. Delta against the live `corpus/lessons/round-41.md` (sha `b8693036…`)

The live file already satisfies C1 (`--rev work` → `m6=0 m7=0 m8=0 m9=0 total=0`). Five
differences remain between it and this draft; each is a concrete edit, not a rewrite.

1. **Refused rows are never numbered.** The live Reject block names
   `r4-gate-write-path-audit` / `r5-gate-write-site-census-corrected` but not the staged ids
   the assignment requires (rows 185 and 189) and never ties the round-40 refusal to staged
   row 137. Insert the three bare-numbered references from § C § Refuse. Bare numbers, not
   `S`-literals: those three are not registry rows and m7 fails any `S`+digits token.
2. **The collision sentence is inverted.** Live: "the package's first two ids now name the
   lane's own rows". Measured: the package's 153/154 are the POSIX `diff` page and the
   google/golden file, while the lane's 153/154 are the ast and pathlib rows — the *lane* now
   names different sources than the staged package at the same two ids. Also "`S001` through
   `S154`" reads as a contiguous run; 109 rows over a 154-id span has gaps. Replace with the
   § C text.
3. **Two `## Holds` sections.** Live has `## Holds (instrument limits)` and then `## Holds`;
   the brief asks for one `## Holds`, and the v3 limits (the required "what v3 still misses")
   are stranded in the second one. Merge into the single § C section, v3 first.
4. **The live v3 hold is falsified by its own seat.** Live: "Aliases, closures over a
   reassigned name, attribute reassignment, conditional assignment … stay unresolved, and
   the docstring says so." ReviewV3Scope's six probes against the pinned tool show the
   opposite direction of error: attribute *names* are classified as destinations, a call
   expression splices callee name + argument literals, a closure resolves against its
   def-time env (both false-positive and false-negative), and an unconditional `for`-body
   binding is invisible. Use the § C wording; it keeps the docstring's scope claim and adds
   the measured wrong-resolution behaviour.
5. **Version label (already fixed in the live text, keep it).** Live now reads "Python 3.15.1
   documentation" and the registry rows say the same; my first read (sha `751e4b60…`) had
   `Python 3.14` in both. Keep the relabel sentence so the correction is on the record.

Everything else in the live file (theme paragraph, quote text with colon, ≤25-word statement,
census counts, correction paragraph, Adjacency block, the two live mistake rows, the C1
counter hold, the renumber hazard, the L0 line, the 60-line-cap waiver) is preserved in § C;
the § C `Mistakes` table adds only `counter-column-drift`.

## E. Findings for the L1 (routed, not applied)

- **F2 evidence pin is not committed (high).** `git cat-file -e HEAD:<path>` at
  `d4ee4e6` is ABSENT for `.ufo/evidence/round-41/sources/ast.html`,
  `…/pathlib.html` and `corpus/knowledge/r41-variable-destination-writes.md`. Both the live
  lesson and § C backtick those paths, and m8 fails any cited path that does not resolve at
  the measured revision (`measure.py` m8). The measurement commit must contain the two
  snapshots and the entry, or F2 turns C1 false at the deciding run.
- **Pin history is clean at the moment of writing, but fragile.** First read: `measure.py`
  sha `f00917…` = the contract's original pin; my allowed base run then printed
  `m6=1 m7=0 m8=0 m9=1 total=2` (matches the contract `before`). By the end of this seat the
  file is `9aaa99ac…` and the contract carries A1–A5 with `claims.C1.counter_sha256 =
  9aaa99ac…` — pin and bytes now agree. Note the judge risk plainly: if any reader re-runs the
  **freeze blob** against the final tree, C1 shows `m7=4 m8=1` from SCORECARD/LOG alone, so the
  amendment record (all five `before_data: true`) is what makes that a fix rather than a
  failed freeze. The C1 predicate itself never hashes the counter, so only a reader enforces
  the pin.
- **The m7 mechanism forces citation hygiene on every round-41 record, not just the lesson.**
  Any `S`+digits literal whose status cell is not `mined` fails; so does *any* id under the
  freeze blob. ScribeLog and ScribeScorecard reached the same conclusion independently. My
  draft is id-literal-free; the live SCORECARD/LOG sections are not, and are safe only under
  the amended blob.
- **The staged range collides 103-for-103 with the lane's future id space.** Only 153/154
  collide today; if the lane keeps appending at its maximum, the next appends collide with
  155, 156, … The renumber-in-scratch rule is a hold in the live file and in § C; it is the
  operative mitigation.
- **No v3 defect is claimed as a counter failure.** C2's predicate names two live sites and two
  planted classes and claims no universality; the wrong-resolution classes in § C Holds are
  scope disclosures, consistent with the contract's `declared_scope_limit` and with the
  `tools/context-capture.py` / `tools/registry-replay.py` disclosures already in SCORECARD.

## F. Tooling and integrity

- No install or upgrade was needed or performed (python3, git, awk, curl-free checks sufficed);
  no pacman transaction attempted (host-wide pause respected).
- Lane checkout: not edited. Files read: `corpus/SOURCES.md`, `corpus/lessons/round-40.md`,
  `corpus/lessons/round-41.md`, `corpus/knowledge/r41-variable-destination-writes.md`,
  `SCORECARD.md`, `LOG.md`, `tools/write-path-census-{v2,v3}.py`, the round-41 evidence and
  wave trees. Write: this report only.
- Scratch: `/tmp/tameshi-r41-scribelesson-draft.md`, `/tmp/tameshi-r41-scribelesson-draft.keep`,
  `/tmp/tameshi-r41-scribelesson-freeze.py`, `/tmp/tameshi-r41-scribelesson-verify/`,
  `/tmp/tameshi-r41-scribelesson-verify2/`, `/tmp/tameshi-r41-scribelesson-m7/`.
- Counter runs: `--rev work` (pre-run checks, labelled), `--rev a3d6c690…` (base control). No
  run at the tip or at the measurement revision; the deciding run stays the L1's.

Report: .ufo/waves/round-41/w1/ScribeLesson.md
