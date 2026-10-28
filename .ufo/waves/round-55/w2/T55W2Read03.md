# T55W2Read03 — executor-sufficiency cold read of `## Standing rules` at C0

- **Candidate:** `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0)
- **Section:** `## Standing rules`, `SKILL.md` lines 17–44 (heading 17; bullets 19–20, 21, 22–23, 24–27, 28–31, 32–43)
- **section_sha256:** `acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767`
  (cut with `.ufo/evidence/round-18/measure.py` `sectionize()`; 64 sections at C0, exactly one match for the heading; receipt `00`, `09`)
- **Angle:** executor sufficiency — can an executor with **no lane context** carry out each rule from this text alone? Not a style review.
- **Verdict:** 7 findings (2 high, 3 medium, 2 low). The rule whose wording is **ambiguous and unverifiable** is *"The scratch root has three arms"* (lines 32–43); the rule a next round's editor can **break without noticing** is that same bullet's closing citation clause (lines 41–43), because the only automated read of this section is a substring test.
- Reader JSON: `.ufo/waves/round-55/w2/T55W2Read03.json`; receipts: `.ufo/waves/round-55/w2/T55W2Read03-receipts/`.

## Method (git objects only, never the working tree)

```
$ python3 sec.py    # imports the frozen .ufo/evidence/round-18/measure.py sectionize()
sections=64 heading='## Standing rules' start=17 end=44 sha256=acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767
```

The section was cut from `git cat-file blob C0:SKILL.md`; every other lane read used `git show C0:path` or `git grep C0`. Receipt `09` independently recomputes the body sha and proves each JSON quote is verbatim (whitespace-normalised) in the section. Attack fixtures are `git clone --shared` copies at C0 under `$HYAKU_SCRATCH/tameshi-r55/T55W2Read03/clone`, with `git rev-parse --show-toplevel` asserted equal to the clone before every commit-free mutation (the single mutation was to the clone's `SKILL.md`, restored with `git checkout --`).

## The two named answers

**Rule whose wording is ambiguous / unverifiable: lines 32–43, "The scratch root has three arms."**
It carries three independent sufficiency gaps in one bullet: the unset arm names no root ("the platform default") while the preceding bullet (28–31) names a different root (`$HYAKU_SCRATCH`); the measured set is a count whose members are never listed; and the artifact it cites for measurement contradicts the sentence. Measured: `tempfile.gettempdir()` = `/tmp` with `TMPDIR` unset, no tool reads `HYAKU` at all, a `repeat-control --selftest` writes 44 dirs under `/tmp` and 0 under the namespace, and `registry-check --rev` (one of the named modes) copies a 383 MB tree into whatever root the unset arm yields — a root the same section caps at 50 MB. Nothing in the section tells the executor to export `TMPDIR` inside the namespace.

**Rule an editor can break without noticing: lines 41–43, the closing citation and its numerals.**
`skill = 1 if MARKER in norm(SKILL.md)` (counter line 260, unchanged at tip `133b2ce`) is the only automated read. Rewriting "the seven self-tests" → "the seventeen self-tests" and "the five non-allocating modes" → "the ninety non-allocating modes" in a C0 clone leaves `skill = 1`. Adding a scratch-allocating tool does trip the registry-cell arm, but its failure text points at `tools/registry.json`, so the editor fixes the rows and the sentence's numerals stay false, unwatched.

## Findings

### F1 — two scratch roots, one unnamed default (ambiguous; high)
> `` `strict_scratch_root()` honours `TMPDIR`: unset → the platform default; empty (`TMPDIR=""`) → unset `` (33–34)

```
$ env -u TMPDIR python3 -c "import tempfile;print(tempfile.gettempdir())"
/tmp
$ git -C "$L" grep -c "HYAKU" 9cf0146b -- tools
rc=1 (no match)
$ HYAKU_SCRATCH=… strace -f -e trace=mkdir,mkdirat -o log env -u TMPDIR python3 tools/repeat-control.py --selftest
rc=0
mkdir calls under /tmp : 44
mkdir calls under $HYAKU_SCRATCH: 0
```

With `TMPDIR` unset the tool root is `/tmp`; with the seat namespace exported it is still `/tmp`, because no tool consults `$HYAKU_SCRATCH`. The same section bounds `/tmp` to files under 50 MB, yet the mode it names in this bullet needs a 383 MB tree (`git clone --no-hardlinks`, flags at `tools/registry-check.py:800-810`):

```
$ du -sh $L/.git → 123M
$ git clone --no-hardlinks $L $S/clonesize → 383M
```

An executor with no lane context cannot decide whether to export `TMPDIR=$HYAKU_SCRATCH/...`, leave it unset, or treat the two bullets as disjoint. Receipts `01`, `02`.

### F2 — the measured set cannot be enumerated, and the cited counter contradicts the sentence (unverifiable; high)
> "Measured on every documented allocating mode — the seven self-tests plus `env-diff --contract` and `registry-check --rev` — as one stderr line" (37–38)

```
$ python3 mode-counts.py     # imports the C0 counter, calls its own modes()
modes=14 allocating=9 lazy=5
allocating: ['repeat-control --selftest', 'registry-check --selftest', 'bash-witness-study selftest',
 'pin-disposition --selftest', 'evidence-disposition --selftest', 'context-capture --selftest',
 'env-diff --selftest', 'env-diff --contract', 'registry-check --rev']
contract.json (C0) amendments: 7
contract.json target: C2_R55_PASS=true: 9/9 allocating modes (the seven self-tests, `env-diff --contract`, …
$ sed -n '17p' .ufo/evidence/round-55/c2/measure.py
  grammar  8 allocating modes (the seven self-tests + `env-diff --contract`):
$ grep -n "(8 - note)\|note=%d/9" .ufo/evidence/round-55/c2/measure.py
273:        + tmp_total + (7 - docs) + (8 - note) + (1 - skill)
280:          "tmp_mkdirs=%d docs=%d/7 note=%d/9 …
perfect-tree total, code's (8 - note) term with note=9: -1
```

The section's arithmetic (7 + 2 = 9) agrees with the frozen C2 target and with the counter's code, but disagrees with the counter's own header ("8") and with its total (still `(8 - note)`), so at C0 an all-green tree scores `total=-1`, `PASS=false`: the section's claim cannot be verified by the artifact it cites. The seven are also unnamed in the section; only the registry's seven `scratch_root` cells identify them. Receipt `03`.
*Ancillary, out of item scope:* the lane tip advanced during this seat from C0 to `133b2ce` ("freeze amendment 8"), whose diff changes exactly these two terms (`(len(cheap) - …)`, `(len(allocating) - note)`); the header line 17 still says 8 at that tip. Not adjudicated here.

### F3 — the numerals are unguarded prose (breakable without noticing; medium)
> "2; the five non-allocating modes stay lazy (round-55 C2 counter; corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root` cells)." (41–43)

```
$ python3 -    # counter line 260's own skill-arm expression, C0 clone
skill before mutation: 1
skill after seven->seventeen and five->ninety: 1
mutated line: 1. Measured on every documented allocating mode — the seventeen self-tests plus
$ git -C "$S/clone" checkout -- SKILL.md    # restored
```

The counts, the mode names and the registry-cell number are all prose that no arm reads; only the grammar marker is matched. A wave that adds, renames or drops a mode changes truth here with the counter green. Receipt `04`.

### F4 — the permission clause has no referent (unresolvable; medium)
> "Read-only substrates unless PROVINCE.md declares a write surface; detection-and-report for operator-owned remediation." (19–20)

```
$ git -C "$L" grep -n -i "write surface" 9cf0146b -- PROVINCE.md AGENTS.md
matches=0 rc=1
```

`PROVINCE.md` at C0 contains no such declaration and never uses the term, so the escape clause cannot be evaluated; "substrates" is undefined (which of corpus/, SCORECARD.md, sibling lanes?) and the file is unrooted. PROVINCE.md does say the lane owns "this lane's runner, corpus and source registry", but whether that is a declared write surface is left to the reader. Receipt `06`.

### F5 — "shape-only" has no definition anywhere (undefined terminal; medium)
> "Secrets shape-only, never content-read." (21)

```
$ git -C "$L" grep -n "shape-only" 9cf0146b -- corpus tools AGENTS.md PROVINCE.md
AGENTS.md:5 / arm-class-matrix.md:424 / closeout-r11.md:20,243 /
gates-survey-kagi.md:617 / operator-runbook.md:258 / service-limits.md:50,118 …
definitional hits (means|defined as|shape-only is): 0
```

The phrase is restated, never defined; the nearest operational instance is an `ls -l` path-presence check (`gates-survey-kagi.md:617`) that the section does not cite. An executor cannot decide whether a sha256, a size or a mode is shape or content. Receipt `06`.

### F6 — an unanchored claim inside the rule that demands anchors (self-violated; low–medium)
> "w1/w2 occurrence counts: 0 dash-form seat trees across rounds 48-52, thousands of the slash form" (28)

```
$ grep -rn "dash-form" .ufo/evidence/round-53/integrate/resolutions.json
4: "… w1 occurrence evidence: 0 dash trees rounds 48-52 in T53W1Read07.md …
$ grep -rn "host scratch directive" "$L" --include=*.md -l
…/round-53/assimilation/validate/SKILL.md
…/round-53/w1/T53W1Read06.md, T53W1Read04.md, T53W1Read11.md, T53W1Read07.md
```

No path:line, command or evidence id is given for the counts ("thousands" is unquantified), and the underlying evidence sits in a round-53 adjudication the section does not cite. "The host scratch directive of 2026-10-25" resolves only to copies of SKILL.md and round-53 wave notes — a directive with no artifact. This directly contradicts bullet 22–23. Receipt `06`.

### F7 — "one stderr line" leaves the other stream undefined (ambiguous; low)
> "as one stderr line, `<tool>: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`, exit 2" (38–40)

```
$ python3 class-sweep.py    # TMPDIR=/nonexistent-r55-sweep, cwd = C0 clone
mode                   rc  grammar  stdout_b  stdout first line
repeat-control         2   yes      28        'REPEAT_CONTROL: setup_error'
registry-check         2   yes      0         ''
bash-witness-study     2   yes      0         ''
pin-disposition        2   yes      0         ''
evidence-disposition   2   yes      0         ''
context-capture        2   yes      0         ''
env-diff               2   yes      0         ''
```

All seven satisfy the letter; `repeat-control` additionally prints a *second* verdict token naming a different class on stdout. The section does not say whether stdout must be empty, and the cited counter only forbids `RuntimeError`/`Traceback` on either stream, so nothing measures it. A caller that parses the tool's verdict grammar (stdout) cannot distinguish could-not-evaluate from a test failure. Receipt `08`.

## What an executor *can* carry out from this text alone (calibration)

| Bullet | Lines | Carriable? | Evidence |
|---|---|---|---|
| Read-only unless PROVINCE declares | 19–20 | **No** (F4) | `write surface`: 0 matches |
| Secrets shape-only | 21 | **No** (F5) | 0 definitional hits |
| Every claim: measured anchor | 22–23 | **Yes** — the three anchor forms are given and both S-refs resolve | `S278`/`S279` rows exist in `corpus/SOURCES.md:153-154`; and the section is checked by this very rule (F6) |
| Errata append-only | 24–27 | **Yes** — checkable as a pure-addition diff; verified over base→C0: one hunk inside Standing rules, errata blocks byte-identical | receipt `07` |
| Scratch namespace `$HYAKU_SCRATCH/<lane>-r<round>/<sub>/` | 28–31 | Partly — the shape is exact, `<sub>` is never expanded, and the counts are unanchored (F6) | receipts `06` |
| Scratch root, three arms | 32–43 | **Partly** — empty arm fully carriable (S278/S279 resolve; `TMPDIR=""` skips the candidate), unusable arm reproducible byte-exactly, unset arm ambiguous (F1) and the measurement unverifiable (F2, F3, F7) | receipts `01`–`05`, `08` |

Positive check of the unusable arm, executed verbatim from the section's own text:

```
$ TMPDIR=/nonexistent-r55 python3 tools/repeat-control.py --selftest
rc=2
stderr: repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root:
        TMPDIR is not a usable directory: '/nonexistent-r55' (could-not-evaluate)
```

The empty arm's anchors also resolve exactly as claimed: `S278` is CPython's `_candidate_tempdir_list:163-165` with the empty-value skip, `S279` the documented fall-through order (`corpus/SOURCES.md:153-154`). That half of the bullet is the strongest text in the section — it names the mechanism, cites the resolver, and reproduces byte-exactly.

## Sweep (what was attacked, not only what was found)

- All six bullets read line by line at C0; every quantified claim, every named artifact and every external reference in 28–43 traced to a file at C0.
- Seven self-tests + the two extra modes: `modes()` enumeration, grammar reproduction, stream census.
- Registry: 7 `scratch_root` cells present at lines 44, 87, 135, 333, 424, 620, 895 of `tools/registry.json`.
- Tools: `strict_scratch_root()` body in `repeat-control.py:156-167` and `registry-check.py:761-774`; clone flags in `registry-check.py:800-810`.
- Diff scope: base→C0 `SKILL.md` is 7 insertions/3 deletions, one hunk, inside Standing rules — so no other section drifted and the append-only rule held over this edit.
- No attack found a *false* factual statement in the section: the numerals 7/5/7 match the registry and the C0 contract; the grammar line matches the tools. The failures are sufficiency failures (unresolvable references, undefined terminals, unguarded prose), which is what this angle measures.

## Artifacts opened (provenance)

| Artifact | Revision / method | What was used |
|---|---|---|
| `SKILL.md` | C0, `git cat-file blob` | full file for heading index; lines 17–44 verbatim |
| `.ufo/evidence/round-18/measure.py` | C0, read `sectionize()` + docstring, imported | section cut and sha |
| `.ufo/evidence/round-55/c2/measure.py` | C0, docstring 1–57, `modes()` 78–130, arms 180–292, imported | enumeration, arms, total arithmetic |
| `.ufo/evidence/round-55/c2/measure.py` | tip `133b2ce`, `git show` | amendment-8 denominator fix, skill arm |
| `.ufo/evidence/round-55/contract.json` | C0 (`git show`; 7 amendments) and tip (8) | C2 target 9/9; amendment 6/8 text |
| `.ufo/evidence/round-55/freeze.json` | working tree | amendment count |
| `.ufo/evidence/round-55/before/c1.stdout`, `c2.stdout` | working tree | base receipts |
| `.ufo/evidence/round-53/integrate/resolutions.json` | C0, grep | dash-form evidence path |
| `corpus/knowledge/scratch-root-contract.md` | C0, full | three arms, nine modes, five lazy modes, blind spot |
| `corpus/SOURCES.md` | C0, rows 153–154 | S278/S279 resolution |
| `corpus/knowledge/gates-survey-kagi.md` | C0, lines 610–625 | the only operational `shape-only` example |
| `corpus/knowledge/arm-class-matrix.md`, `closeout-r11.md`, `operator-runbook.md`, `service-limits.md` | C0, grep hits | `shape-only` occurrences (no definition) |
| `tools/registry.json` | C0, 7 `scratch_root` cells | cell text and allocating-mode lists |
| `tools/repeat-control.py` | C0, lines 156–167 | `strict_scratch_root()`, exception class |
| `tools/registry-check.py` | working tree (clean vs C0 per `git status`), lines 736–840 | `clone_lane_at_rev`, `--no-hardlinks` |
| `PROVINCE.md` | C0, head 40 lines + grep | ownership sentences; absence of "write surface" |
| `AGENTS.md` | C0, grep hit line 5 | `shape-only` restatement |
| `.ufo/waves/round-55/spec-w2.json` | working tree | this seat's item |
| `.ufo/waves/round-53/w2/T53W2Read02.json` | C0, head 30 | reader-JSON house style |
| `.ufo/waves/round-55/w1/`, `.ufo/waves/round-55/w2/` | directory listings | naming/seat inventory |

## Bounds, scratch, tooling

- Writes: only `.ufo/waves/round-55/w2/T55W2Read03.json`, `.md`, and `T55W2Read03-receipts/` (9 receipts + `driver.sh`, `mode-counts.py`, `class-sweep.py`). No lane production file, frozen file or wave spec was modified; `git status --porcelain` is clean for `SKILL.md`, `tools/registry-check.py`, `tools/repeat-control.py`, `.ufo/evidence/round-55/contract.json`.
- Scratch: `HYAKU_SCRATCH=/fast/scratch/hyaku`, seat tree `tameshi-r55/T55W2Read03` (shared clone at C0, a `--no-hardlinks` clone for the size measurement), deleted on exit; the shared parent was never removed.
- Tooling: nothing installed or upgraded (no `pacman`, no `uv`). `strace` and `python3` were already present.
- The lane's working tree carried other seats' writes (dirty `.ufo/waves/round-55/w1/*`, modified `before/c2.stdout`, untracked `c1/lost-headings-at-c0.json`, `control/`); none were touched, and every claim here was read from git objects at the named revision.
