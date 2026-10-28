# T55W2Read01 — `## Standing rules` cold read at C0 (anchors and counts)

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (all reads via `git show` / `git grep` at an explicit rev; no lane working-tree read for section bytes, no git/jj mutation, no lane production edit)
- Candidate: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0)
- Section: `## Standing rules`, `SKILL.md:17-43` at C0 (`end` 44 exclusive; line 44 is blank and stripped; next heading `## Source notes` at `:45`; no fence inside the range)
- `section_sha256` = `acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767` (2246 bytes), from the frozen sectionizer `.ufo/evidence/round-18/measure.py` `sectionize` over the C0 blob, and reproduced independently by `git show C0:SKILL.md | sed -n '17,43p'` with trailing newline stripped (receipt `r01-section-sha.txt`)
- Verdict: **2 findings**, 12 holds, 5 checked-and-not-filed, 0 unverifiable-inside-the-section
- Angle: anchors and counts — every `file:line` anchor, every count, and every cited corpus note checked against the tree at C0

## 1. Method

1. Materialized the section bytes from git objects only (`git show`, never the working tree).
2. Ran the frozen round-18 sectionizer to get `start`/`end`/`sha256`, then re-derived the same sha by `sed` + trailing-newline strip.
3. Took each sentence of the section and turned it into a checkable predicate:
   - every `file:line` / `S###:lines` anchor resolved and read at those exact lines;
   - every count (`three arms`, `seven self-tests`, `two extra modes`, `five non-allocating`, `seven registry cells`, `0 dash-form trees across rounds 48-52`, `thousands of the slash form`, `rounds 37-52`) recounted at C0;
   - every cited note opened and checked to say what the section says it says;
   - the quoted stderr line compared byte-for-byte against what the nine modes actually print at C0.
4. Ran the round-55 C2 counter at C0 (allocation under `/fast/scratch/hyaku/tameshi-r55/T55W2Read01`, removed) and independently ran all nine allocating modes with `TMPDIR` set to a nonexistent path.

Axis note (Godspeed): axes were *anchor resolvability*, *count agreement*, and *quoted-output fidelity*; every check was cheap and ran in one batch where independent, and only the C2 counter (≈6.5 min) was expensive.

## 2. Findings

### F1 — the quoted "one line" byte-shape names a tool token that 3 of the 9 measured modes do not print

**Quote (section, `SKILL.md:37-41` at C0):**

```
  … Measured on every documented allocating mode — the seven self-tests plus
  `env-diff --contract` and `registry-check --rev` — as one stderr line,
  `<tool>: could-not-evaluate: cannot create clone scratch under the scratch
  root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`, exit
  2; …
```

**Verdict:** the class half holds for all nine modes (rc=2, exactly one stderr line each); the `<tool>` half does not. Three of the nine print a fixed program tag that is not the tool name.

**Command (all nine modes, clone of the lane at C0, `TMPDIR` = nonexistent path):**

```
export TMPDIR=$S/c2work/no-such-tmpdir
python3 tools/repeat-control.py --selftest
python3 tools/registry-check.py --selftest
python3 tools/bash-witness-study.py selftest
python3 tools/pin-disposition.py --selftest
python3 tools/evidence-disposition.py --selftest
python3 tools/context-capture.py --selftest
python3 tools/env-diff.py --selftest
python3 tools/env-diff.py --contract .ufo/evidence/round-55/c2/fixture-contract.json --out OUT --fleet-root .
python3 tools/registry-check.py --rev HEAD
```

**Output (first token of the single stderr line, per mode; every run rc=2, `stderr_lines=1`):**

| mode | leading token printed |
|---|---|
| `repeat-control --selftest` | `repeat-control` |
| `registry-check --selftest` | `registry-check` |
| `registry-check --rev` | `registry-check` |
| `bash-witness-study selftest` | **`WITNESS_STUDY`** |
| `pin-disposition --selftest` | `pin-disposition.py` |
| `evidence-disposition --selftest` | `evidence-disposition.py` |
| `context-capture --selftest` | `context-capture.py` |
| `env-diff --selftest` | **`ENVDIFF_SETUP`** |
| `env-diff --contract` | **`ENVDIFF_SETUP`** |

Verbatim lines (receipt `r05-nine-mode-lines.txt`):

```
bash-witness-selftest                  WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)
env-diff-selftest                      ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)
env-diff-contract                      ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)
```

Source anchors at C0: `tools/bash-witness-study.py:1789` `print(f"WITNESS_STUDY: could-not-evaluate: {exc}", file=sys.stderr)`; `tools/env-diff.py:235` and `:264` `print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)`.

**Why the counter cannot see it:** the frozen C2 counter's `GRAMMAR` accepts any identifier as the leading token (`^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: …`) and its `MARKER` compares only the tail from `could-not-evaluate:` on. Parsing the counter's own regex against both lines (receipt `r06-grammar-accepts-tokens.txt`):

```
WITNESS_STUDY matches GRAMMAR: True
ENVDIFF_SETUP matches GRAMMAR: True
```

**Same shape, more specific, in the frozen rows.** The seven `scratch_root` cells repeat the tool-name assumption for the two deviating tools and pass the counter's `docs` arm (7/7) regardless, because the arm checks only `MARKER`:

```
tools/registry.json:87   "… \"bash-witness-study.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)\" …"
tools/registry.json:895  "… \"env-diff.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)\" …"
```

Neither string is ever printed by those tools at C0. The note `corpus/knowledge/scratch-root-contract.md` carries the same generic `<tool>` shape in its `## One line, every mode (round 55)` section (`:73-75`).

**Consequence:** a caller that parses the class by prefix — the reading the sentence invites — breaks on 3 of 9 modes; a caller that the round's contract itself flags as the blind spot ("whether a caller parses the grammar by prefix or by the whole line", `contract.json` C2 `cannot_see`). Smallest correction available to the page: say the leading token is a fixed program tag (not always the tool), or make the two tools print their own name and fix the two registry cells.

### F2 — the dash-form end boundary "rounds 37-52" is stale at C0

**Quote (section, `SKILL.md:28` at C0):**

```
  … the shape every landed round since 48 uses — w1/w2 occurrence counts: 0 dash-form seat trees across rounds 48-52, thousands of the slash form; the dash form survives only in run artifacts and quoted text of rounds 37-52, not as a live convention [round 53 correction of the round-53 'rounds 25-36' overstatement, seat T53W2R4])
```

**Verdict:** the "0 dash-form seat trees across rounds 48-52" and "thousands of the slash form" halves hold exactly; the end boundary "of rounds 37-52" does not. At C0 the dash form survives past 52 in two independent objects, one of them a live tree created by this very round.

**Command + output (receipt `r07-dash-census.txt`):**

```
git -C LANE grep -o -E '(hyaku/|(var/)?tmp/)tameshi-r[0-9]+-[A-Za-z0-9_]+' C0 -- .
   default base (hyaku/…): 25:9  27:2  29:101  31:1027  32:1508  33:382  34:1034  35:1717  36:155  55:1
   /tmp + /var/tmp:       1:135 … 37:18 38:7 39:152 40:162 41:211 42:150 43:243 44:113 45:1700 46:586 47:380 53:11
git -C LANE grep -o -E 'hyaku/tameshi-r(4[89]|5[012])/' C0 -- . | wc -l          -> 8183
git -C LANE grep -o -E '(var/)?tmp/tameshi-r(4[89]|5[012])-[A-Za-z0-9_]+' C0 -- . | wc -l -> 0
```

(The `53:11` bucket in the second line is the round-17 CR53 trace strings explained in §4a — cold-read case 53, not round-53 trees; no round-53 tree is counted there.)

**Counterexample 1 — a live dash-form seat tree in round 55** (`.ufo/waves/round-55/w1/T55W1ExecNoHarm.md:189-190` at C0, verbatim):

```
  I re-rooted later scratch at
  `/fast/scratch/hyaku/tameshi-r55-noHarmC2/` and removed it on completion.
```

That is a live tree under the default base, created in round 55 — three rounds after the stated boundary, and the same parenthetical says the default base is where the slash shape rules. It is recorded in a run artifact *of round 55*, not "of rounds 37-52".

**Counterexample 2 — quoted text past 52** (`.ufo/evidence/round-53/assimilation/validate/SKILL.md:25` at C0):

```
- **Scratch namespace is `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>-<n>-*/`** (host scratch directive of 2026-10-25: …)
```

A round-53 artifact still carrying the dash-form sentence — the "quoted text" family, outside 37-52.

**Which half of the clause survives:** "run artifacts" is exact only for 37-47 (0 dash-form trees in 48-52, matching the sentence's own "0 … across rounds 48-52"), and "quoted text" runs at least through round 53. "Not as a live convention" is weakened rather than refuted: one seat's incident re-root is not a round-wide convention. The end boundary should read "through round 55" (trees) / "through round 53" (quoted text), or the clause should be scoped to the round-53 rewrite.

## 3. Checks that held (with the number/line each was checked at)

1. **`$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)** — the variable-or-default idiom is what the lane's scripts actually use: `.ufo/evidence/round-48/deciding-run.sh:10,17` `# … $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r48/deciding` and `SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r48/deciding`; same idiom in rounds 49-52 scripts (`git grep HYAKU_SCRATCH C0`).
2. **`<lane>-r<round>/<sub>/` — "the shape every landed round since 48 uses"** — slash form present in every round 48-55: 48:305, 49:638, 50:4822, 51:2258, 52:160, 53:581, 54:6134, 55:1951 (`hyaku/tameshi-r<NN>/` census, receipt `r07`).
3. **"0 dash-form seat trees across rounds 48-52"** — 0 under every base tested (`hyaku/`, `/tmp/`, `/var/tmp/`); the 53 other dash-form *strings* in 48-52 are schema ids and mkdtemp prefixes (`tameshi-r49-reads-v1` ×17, `tameshi-r51-c2-selftest-` ×3, …), not trees — so the "seat trees" qualifier is load-bearing and present.
4. **"thousands of the slash form"** — 8183 occurrences across rounds 48-52.
5. **`mutation-case-kimi-census.md:4-7` / `mutation-case-kagi-census.md:4-6`** — both cited ranges carry "every mutant is a copy under `/tmp/tameshi-r2-1-work/`" (kimi `:5`) and "`/tmp/tameshi-r3-1-work/`" (kagi `:4`), i.e. both mutation lanes kept mutants + evidence under `/tmp`. Exact.
6. **`S278:163-165`** — `corpus/SOURCES.md:153` (row S278) pins `_candidate_tempdir_list :163-165 @ v3.12.7`; the snapshot `.ufo/evidence/round-54/assimilation/S278-tempfile.py:163-165` is exactly `for envname in 'TMPDIR', 'TEMP', 'TMP': / dirname = _os.getenv(envname) / if dirname: dirlist.append(dirname)` — i.e. the resolver skips an empty candidate, as the section says.
7. **`S279` "the documented list"** — `corpus/SOURCES.md:154` (row S279); snapshot `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html:510` is `<li><p>The directory named by the … TMPDIR … environment variable.</p></li>`, then TEMP/TMP/platform locations.
8. **"three arms" / "seven self-tests plus `env-diff --contract` and `registry-check --rev`" / "five non-allocating"** — the registry's `Allocating modes` union is exactly those nine (5 rows `selftest`, `registry-check` `selftest, --rev`, `env-diff` `selftest, --contract`); the C2 counter's `allocating` list is the same nine and its `lazy` list is the same five (`repeat-control --snapshot`, `bash-witness-study count`, `pin-disposition --read`, `evidence-disposition --json`, `context-capture --check`). Measured at C0: grammar 9/9, lazy 5/5, empty 13/13, usable 13/13, tmp_mkdirs 0, docs 7/7, note 9/9, skill 1/1 (`r03`, `r04`).
9. **"the seven registry `scratch_root` cells"** — `git show C0:tools/registry.json | grep -c scratch_root` = 7, one per tool that defines `strict_scratch_root()` (7 files: repeat-control, registry-check, bash-witness-study, pin-disposition, evidence-disposition, context-capture, env-diff).
10. **`strict_scratch_root()` honours `TMPDIR` (unset → default; empty → unset; unusable → exit 2 naming the value)** — the seven helpers agree (spot-read at `tools/env-diff.py:36-50`), and the empty arm exits 0 for all 13 modes while the unusable arm exits 2 for all nine allocating modes.
11. **`## Errata — round 16 full-page cold-read` "discloses its own in-place repairs"** — the heading exists verbatim at C0 `SKILL.md:1737` and the block says "The page edits are in-place repairs, and so are this table's own cells" (`:1749-1751`).
12. **`PROVINCE.md` declares what the lane may write** — `PROVINCE.md` exists at C0 and its "Owns" paragraph claims "the method … Also: this lane's own corpus and gates", with "Out of province → report, never absorb". The literal phrase "write surface" is not in the file; the declaration is functional, and the rule is normative. Held (see §4c).

## 4. Checked and not filed (with the reason)

a. **`(var/)?tmp/tameshi-r53-…` inside `.ufo/evidence/round-17/coldread/traces/CR53/*.json`** — my first census put 11 dash-form occurrences at "round 53". They are round-17 artifacts (committed in `fad9e95`, round 17) whose paths are named after cold-read case **53**, not the round: `/tmp/tameshi-r53-probe-b2`. A name collision, not a survival instance; excluded from F2. (Same family: `.../CR53/10.json` records `rev eb7838b`, a round-17 revision.)
b. **"run artifacts … of rounds 37-52" as a range** — measured run-artifact dash trees are rounds 37-47 only (3722 occurrences). Under a strict "every round in the range has both kinds" reading this over-claims 48-52, but under the ordinary "the surviving instances lie inside 37-52" reading it does not; the sentence does not assert per-round presence. Not filed separately; F2 is the concrete failure of the *end* boundary.
c. **`PROVINCE.md` never uses the phrase "write surface"** — the rule is "unless PROVINCE.md declares a write surface", and the file declares ownership/writes in different words. Not filed: no lane object contradicts the rule, and the rule is about a declaration existing, not about a phrase.
d. **"host scratch directive of 2026-10-25" has no in-lane anchor for the date.** The substance is live and matches every seat bound of rounds 48+ (`/tmp` only for files under 50 MB; the tree is removed on exit): `git grep -c '50 MB' C0` hits round-48/51/53 artifacts (`.ufo/waves/round-48/a2-items.py:22` "under 50 MB, removed on exit") and `.ufo/waves/round-53/w1/T53W1ExecRegCheck.md:201` repeats the date ("host scratch directive (2026-10-25: `/tmp` is for files under 50 MB only)"). The phrase itself appears in 31 C0 objects, all repetitions of the directive rather than its record: `SKILL.md:28`, `.ufo/evidence/round-53/assimilation/validate/SKILL.md:25`, and 29 round-53 wave artifacts (`git grep -l 'host scratch directive' C0 -- . | wc -l` = 31), e.g. `.ufo/waves/round-53/w1/T53W1ExecRegCheck.md:201`, which repeats both the date and the substance. The date is inherited, not verifiable from lane objects. Not filed: no lane object contradicts it (same conclusion as round-53 seat T53W2R4's provenance note), but the anchor is outside the lane and the section gives no path.
e. **The round-55 C2 counter's own bookkeeping at C0** (adjacent, not a section claim — but it is the section's cited receipt). The section cites "(round-55 C2 counter)". At C0 the counter's bytes (`sha256 36ca47d3…`) compute `total = … + (len(table) - empty_ok) + (len(table) - usable_ok) + … + (8 - note) + …` with `len(table)=14`, `empty_ok=usable_ok=13`, `note=9`, so with every arm green it prints `total=1 C2_R55_PASS=false` and exits 1 — a false negative with an empty `bad` map. My run (started 14:19, before the file's 14:20:47 mtime and before commit `133b2ce` at 14:21:00; Python loads the file at start) reproduced exactly that arithmetic. The freeze pointer has since moved to `133b2ce` ("freeze amendment 8 — c2/measure.py totals use the denominators they measure"), where the formula is `(len(cheap) - empty_ok) + (len(cheap) - usable_ok) + … + (len(allocating) - note) + …`; re-running those bytes (`sha256 0458f632…`) against the same rev gives `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true`, exit 0 (receipt `r09`). Two residual stale-doc facts remain at `133b2ce`: the module docstring still says "8 allocating modes" / "the eight / allocating modes issue no mkdir" / "names all eight allocating modes" (`:17,24-25,28`) while the code measures nine and the verdict prints `note=%d/9`. The *section's* substantive claim (nine modes measured, one line, exit 2) is what my run shows; the counter's PASS flag is the round's C2 business. Flagged here for the L1/critic, not filed as a section finding.

## 5. Gates run

| gate | command | result |
|---|---|---|
| section sha (frozen sectionizer) | `import .ufo/evidence/round-18/measure.py; sectionize(git show C0:SKILL.md)` | `{"start":17,"end":44,"heading":"## Standing rules","sha256":"acfb671a…a9ad767"}` |
| independent sha | `git show C0:SKILL.md \| sed -n '17,43p'` + strip trailing newline | `acfb671a…a9ad767` (2246 B) |
| C2 counter at C0, C0-bytes | `python3 .ufo/evidence/round-55/c2/measure.py --lane LANE --rev C0 --work <empty> --explain` | every arm `ok`: grammar 9/9, lazy 5/5, empty 13/13, usable 13/13, tmp_mkdirs 0, docs 7/7, note 9/9, skill 1/1; printed `total=1 C2_R55_PASS=false`, exit 1 (the C0 bookkeeping bug, §4e) |
| C2 counter at C0, amended freeze bytes (`133b2ce`) | same command, counter `sha256 0458f632…` | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true`, exit 0 |
| nine allocating modes, direct | `TMPDIR=<nonexistent> python3 tools/<tool> …` in a C0 clone | all rc=2, all exactly 1 stderr line; 3 of 9 with a non-tool leading token (F1) |
| dash/slash census | `git grep -o -E …` at C0 (three patterns) | slash 48-52 = 8183; dash trees 48-52 = 0; dash artifacts 37-47 = 3722; default-base dash 25-36 + 55:1 (F2) |

## 6. Artifacts opened (all at C0 unless stated)

Section and sectionizer: `SKILL.md` (C0 blob; `:17-43` and the errata block `:1737-1786`), `.ufo/evidence/round-18/measure.py` (`sectionize`).

Round-55 frozen material: `.ufo/evidence/round-55/c2/measure.py` (C0 blob `36ca47d3…` **and** lane-head blob `0458f632…` at `133b2ce`), `.ufo/evidence/round-55/contract.json` (claims.C2, amendments 6-8), plus the receipts my run produced (`c2-receipts.json`).

Corpus: `corpus/knowledge/scratch-root-contract.md` (incl. `## One line, every mode (round 55)` and the falsifier), `corpus/knowledge/mutation-case-kimi-census.md:1-10`, `corpus/knowledge/mutation-case-kagi-census.md:1-10`, `corpus/SOURCES.md:150-154` (S275-S279).

Source snapshots: `.ufo/evidence/round-54/assimilation/S278-tempfile.py:158-168`, `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html:449,510`.

Tools: `tools/registry.json` (7 `scratch_root` cells), `tools/repeat-control.py` (selftest, `emit`/`emit_err`, `could_not_evaluate`, entry handler `:925`), `tools/env-diff.py` (`strict_scratch_root` `:36-50`, handlers `:234,263`), `tools/registry-check.py` (`strict_scratch_root` `:761`, handlers `:1851,1935`), `tools/context-capture.py` (`:300,313,2217`), `tools/pin-disposition.py` (`:161,175,1399`), `tools/evidence-disposition.py` (`:191,205,3231`), `tools/bash-witness-study.py` (`:205,219,1788`).

Records: `PROVINCE.md`, `.ufo/waves/round-53/w2r/T53W2R4.md` + `.json`, `.ufo/waves/round-53/w1/T53W1Read07.md`, `.ufo/waves/round-55/w1/T55W1ExecNoHarm.md:178-200`, `.ufo/evidence/round-53/assimilation/validate/SKILL.md:25`, `.ufo/evidence/round-17/coldread/traces/CR53/10.json`, `.ufo/evidence/round-48/deciding-run.sh`, `.ufo/waves/round-48/a2-items.py`; `git log --oneline` for `.ufo/evidence/round-55/c2/measure.py` and `.ufo/evidence/round-17/coldread/traces/CR53/10.json`.

## 7. Bounds, scratch, tools

- Reads only through `git show`/`git grep`/`git log` at explicit revs; no mutating git/jj command in the lane; `git -C <lane>` used for every call.
- Writes: this report, its JSON, and `T55W2Read01-receipts/` — all under `.ufo/waves/round-55/w2/`. Nothing else in the lane was written; no fleet-root, sibling-lane, `.ufo/state/`, `.scratch/`, `~/.omp/` file was touched.
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/T55W2Read01` (created and removed on exit); no shared parent removed; `/tmp` unused.
- Tools installed or upgraded: none (no `pacman` touched; nothing was needed).
- Census gate: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → **rc=0**, final line `tameshi\tok\t…/tameshi-shokunin/corpus/SOURCES.md` (16 W04 duplicate-URL advisories and 1 W01 advisory, no failure). Read-only run; nothing was changed by it.

## 8. Receipt index (`T55W2Read01-receipts/`)

| file | what it is |
|---|---|
| `r01-section-sha.txt` | sectionizer output (start/end/heading/sha) + independent `sed` sha + boundary lines |
| `r02-section.txt` | verbatim section at C0 (`SKILL.md:17-43`) |
| `r03-c2-run-at-c0.stdout` | full `--explain` output of the C2 counter at C0 + rc |
| `r04-c2-receipts-at-c0.json` | the counter's `c2-receipts.json` for that run (`bad` empty, all arms green) |
| `r05-nine-mode-lines.txt` | the nine allocating modes' actual stderr lines at C0 |
| `r06-grammar-accepts-tokens.txt` | the counter's own GRAMMAR accepting `WITNESS_STUDY` and `ENVDIFF_SETUP` |
| `r07-dash-census.txt` | dash/slash censuses, the round-55 live tree, the round-53 quoting artifact |
| `r08-counter-total-drift.txt` | C0 vs `133b2ce` total formula + stale docstring lines |
| `r09-c2-run-amended-freeze.stdout` | the amended-freeze counter (`0458f632…`) at C0: `total=0 C2_R55_PASS=true`, exit 0 |
| `r10-c2-receipts-amended-freeze.json` | that run's `c2-receipts.json` |
