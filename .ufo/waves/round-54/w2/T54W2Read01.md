# T54W2Read01 — cold read of `## Standing rules` at C1

Axis: calibration. Milestone: C1 fresh read at C1.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Candidate: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Heading: `## Standing rules`
- Section: `start=17`, `end=40`, 1990 bytes after trailing-newline strip, `section_sha256=61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc`
- Split verification: an independent re-derivation (`git show C1:SKILL.md`, `splitlines()[16:40]`, `'\n'.join(...).rstrip('\n')`) gives the same 1990 bytes and the same sha; the same bytes with a trailing newline hash `d23b2462…` and without the rstrip `2808acaf…`, so the monitor's convention (split at the 1-based lines 17-40, strip trailing newlines) is reproduced exactly.
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Read01/` (`TMPDIR` set there for every command); nothing outside `.ufo/waves/round-54/w2/` was written in the lane.
- Tooling: none installed or upgraded for this seat.

## Commands run

```bash
export HYAKU_SCRATCH=/fast/scratch/hyaku; mkdir -p $HYAKU_SCRATCH/tameshi-r54/T54W2Read01
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read01
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 .ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "## Standing rules"
# {"heading": "## Standing rules", "cand": "99c3bc88d704566197783f66b211ee0a830e0330",
#  "start": 17, "end": 40,
#  "section_sha256": "61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc"}

git show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '17,40p'
```

Section bytes (C1, lines 17-39; line 40 is the blank separator) were read whole and then
re-read line by line with `cat -A` for invisible characters. Byte-level scans over the
1990-byte section: no repeated word, no missing space after a period outside code spans,
no double space outside list indentation, no trailing whitespace, no run-together token.

## Finding

**F1 — duplicated closing parenthesis (QUALITY 104 typographic class).**

- Quote (byte-exact substring of the section):
  `not as a live convention [round 53 correction of the round-53 'rounds 25-36' overstatement, seat T53W2R4]))`
- Why: the scratch-namespace bullet opens exactly one parenthetical after the bolded path
  (`(host scratch directive of 2026-10-25: …`; its other pair, `` (default `/fast/scratch/hyaku`) ``,
  closes on the same line) and closes it twice at `seat T53W2R4]))`. The section's
  parenthesis depth therefore ends at **-1** and the stray `)` renders literally with
  nothing to close.
- Receipt:

```bash
python3 - <<'PY'
import subprocess
b=subprocess.run(['git','show','99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md'],
                 capture_output=True).stdout.decode()
sec='\n'.join(b.splitlines()[16:40]).rstrip('\n')
print('chars', len(sec), 'paren balance', sec.count('(')-sec.count(')'))
d=0
for i,ch in enumerate(sec):
    if ch=='(': d+=1
    elif ch==')':
        d-=1
        if d<0: print('first negative depth at char', i); break
PY
```

```
chars 1976 paren balance -1
first negative depth at char 1146
```

`char 1146` is the last character of `seat T53W2R4]))` (context printed:
`"nvention [round 53 correction of the round-53 'rounds 25-36' overstatement, seat T53W2R4]))\n  (in the original …"`).

Provenance (context for the L1, not part of the verdict): the tail was introduced by the
round-53 C6 commit `7c10fa7` and is unchanged by the C1 fix pass
(`git log --oneline -S "seat T53W2R4]))" -- SKILL.md` → one hit, `7c10fa7`; the C0→C1 diff for
this section begins at line 31). The C1 fix pass edited the same section
(`@@ -31,12 +31,12 @@`) but did not touch this hunk, so the defect is present in the C1 bytes
a wave-2 reader is given. Smallest correction: delete one `)` so the sequence reads
`…seat T53W2R4])`.

## What resolved at C1 (no finding)

Every anchor and every measurement claim in the section was checked against a command;
none failed:

| Claim in the section | Check | Result |
|---|---|---|
| `PROVINCE.md` declares the write surface the rule's exception needs | `read` of `/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md` — `**Owns:** … Also: this lane's own corpus and gates.` | resolves |
| `## Errata — round 16 full-page cold-read` is a real heading and "discloses its own in-place repairs" | byte compare of the backticked token against the heading line at C1 | equal (`b'\xe2\x80\x94'` em dash, 1 occurrence) |
| the block "says so" | `sed -n '1733,1780p' SKILL.md` — "The page edits are in-place repairs, and so are this table's own cells" | holds |
| `mutation-case-kimi-census.md:4-7` / `mutation-case-kagi-census.md:4-6` keep mutants+evidence under `/tmp` | `sed -n '4,7p'` / `'4,6p'` of `corpus/knowledge/*-census.md` | lines 4-5 name `/tmp/tameshi-r2-1-work/` (r2) and `/tmp/tameshi-r3-1-work/` (r3) and "no fleet file was written"; bare filename is the page's dominant convention (47 of 53 kimi, 46 of 52 kagi citations) |
| "0 dash-form seat trees across rounds 48-52" | `grep -rho "tameshi-r4[89]-…\|tameshi-r5[0-2]-…"` over `.ufo/waves/round-48…52` | only 6 unique dash-form tokens, all schema ids/mkdtemp prefixes (`tameshi-r49-reads-v1`, `tameshi-r50-recurrence-walk-v1`, `tameshi-r50-sandboxed-confirm-v1`, `tameshi-r50-synthetic-hidden-probe-v1`, `tameshi-r51-c3-selftest-`, `tameshi-r49-w2-precheck-sections-v1`); zero seat trees |
| "thousands of the slash form" | same grep, slash pattern | 8010 occurrences |
| "the dash form survives only in run artifacts and quoted text" | `grep -rn "tameshi-r53-" .ufo/waves/round-53 .ufo/waves/round-54` | one hit, quoted analysis text in `w1/T53W1Read07.md:107` |
| "every landed round since 48" uses the slash shape | spec grep: r48 `…/tameshi-r48/<YourSeatName>`, r49 `…/tameshi-r49/<your…`, r50 `…/tameshi-r50/<your seat>`, r51 `…/tameshi-r51/refresh`, r52 `…/tameshi-r52/refresh`, r53 `tameshi-r53/w1/<seat-name>` / `w2/<seat-name>` | holds |
| "round 53 correction … seat T53W2R4" | `git cat-file -e C1:.ufo/waves/round-53/w2r/T53W2R4.md` and its F1 row ("the dash form's last committed occurrences are rounds 25-36") | resolves, committed |
| "`strict_scratch_root()` honours `TMPDIR`: unset → the platform default" | body of `tools/repeat-control.py:148-159` — `t = os.environ.get("TMPDIR"); … return tempfile.gettempdir()` | holds |
| "empty (`TMPDIR=""`) → unset (the resolver skips an empty candidate, S278:163-165)" | `.ufo/evidence/round-54/assimilation/S278-tempfile.py` lines 163-165 = `for envname in 'TMPDIR', 'TEMP', 'TMP':` / `dirname = _os.getenv(envname)` / `if dirname: dirlist.append(dirname)`; helper's `if t:` treats `""` as unset | holds |
| "the documented list follows, S279" | `corpus/SOURCES.md:154` (S279, Python docs, "The list is: The directory named by the TMPDIR environment variable …") | holds |
| "set but unusable → exit 2, could-not-evaluate, naming the value — never a silent `/tmp` fallback, never a traceback, never exit 1" | all seven selftests run with `TMPDIR=<scratch>/does-not-exist` | 7/7 exit 2; each line names the value `'/fast/scratch/hyaku/tameshi-r54/T54W2Read01/does-not-exist'` and prints `could-not-evaluate`; no traceback; no exit 1 (output below) |
| empty arm end-to-end | `TMPDIR="" python3 tools/registry-check.py --selftest` | rc 0 |
| unset arm end-to-end | `env -u TMPDIR python3 tools/repeat-control.py --selftest` | rc 0 |
| "Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter)" | `.ufo/evidence/round-54/c2/measure.py:44-50` lists the seven tools with `--selftest`, and `bash-witness-study.py` with `selftest` | exact match |
| "the seven registry `scratch_root` cells" | `git show C1:tools/registry.json` → 56 rows, 7 carrying `scratch_root` | 7/7 |
| "corpus/knowledge/scratch-root-contract.md" | `git cat-file -e C1:corpus/knowledge/scratch-root-contract.md` | present |
| no traceback / exit-1 drift in the *checked-out* tools vs C1 | `git diff --stat C1 HEAD -- tools/` | empty, so the runs above are the C1 bytes |

Unusable-`TMPDIR` receipt (working tree = C1 for `tools/`):

```bash
for t in "bash-witness-study.py selftest" "context-capture.py --selftest" \
         "env-diff.py --selftest" "evidence-disposition.py --selftest" \
         "pin-disposition.py --selftest" "registry-check.py --selftest" \
         "repeat-control.py --selftest"; do
  set -- $t
  out=$(TMPDIR=$S/does-not-exist python3 .../tools/$1 $2 2>&1); rc=$?
  echo "== $1 rc=$rc"; echo "$out" | tail -3
done
```

```
== bash-witness-study.py rc=2
WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W2Read01/does-not-exist' (could-not-evaluate)
== context-capture.py rc=2
SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '…' (could-not-evaluate))
== env-diff.py rc=2
ENVDIFF_SETUP: could-not-evaluate: … '…' (could-not-evaluate)
== evidence-disposition.py rc=2
evidence-disposition.py: could-not-evaluate: … '…' (could-not-evaluate)
== pin-disposition.py rc=2
pin-disposition.py: could-not-evaluate: … '…' (could-not-evaluate)
== registry-check.py rc=2
registry-check: could-not-evaluate: … '…' (could-not-evaluate)
== repeat-control.py rc=2
repeat-control: setup: RuntimeError: … '…' (could-not-evaluate)
REPEAT_CONTROL: setup_error
```

Two tools prefix a label that is not the phrase `could-not-evaluate` (`SELFTEST: FAIL`,
`REPEAT_CONTROL: setup_error`) but both put the class string in the same output, name the
value, exit 2 and print no traceback; the section's sentence is about the class, the exit
code and the named value, all of which hold, so this is recorded as observed wording, not
as a finding.

## Considered and not reported

- `(the resolver skips an empty candidate, S278:163-165; the documented list follows, S279)`
  is tight but not wrong: the skip is in `_candidate_tempdir_list`, the ordered list is the
  docs page. No claim exceeds its source.
- "unset → the platform default" does put tool scratch under `/tmp` when `TMPDIR` is unset,
  while the same bullet says "`/tmp` is for files under 50 MB only"; the 50 MB clause is the
  seat's file-placement directive (this seat's own bounds repeat it) and the tool arm states
  the platform default, not a permission. Not a self-contradiction I can defend.
- The bare filenames `mutation-case-kimi-census.md` / `mutation-case-kagi-census.md` are the
  page's own convention (47/6 and 46/6); an executor resolves them under `corpus/knowledge/`.

## Artifacts opened (all at C1 unless stated)

- `.ufo/waves/round-54/reader-section.py` (invoked), `.ufo/waves/round-54/contract.json` (read via grep for the C2 target text only)
- `SKILL.md` at `99c3bc88…:17-40` (section), `:1733-1780` (errata block), `:28` (`cat -A`)
- `corpus/knowledge/scratch-root-contract.md` (committed at C1), `.ufo/evidence/round-54/assimilation/S278-tempfile.py:158-170`
- `corpus/SOURCES.md:153-154` (S278, S279), `corpus/QUALITY.md` (Criterion 104/105 blocks)
- `corpus/knowledge/mutation-case-kimi-census.md:1-10`, `mutation-case-kagi-census.md:1-9`
- `tools/registry.json` at C1 (56 rows, 7 `scratch_root`), `tools/repeat-control.py:148-159`, `tools/*.py` (7 selftest paths)
- `.ufo/evidence/round-54/c2/measure.py:44-50`, `.ufo/waves/round-53/w2r/T53W2R4.md` (F1), `PROVINCE.md`
- Wave/spec greps over `.ufo/waves/round-48` … `round-54`

## Verdict

One finding (F1, duplicated closing parenthesis). Everything else in the section resolves
at C1: the four in-section anchors (`PROVINCE.md`, the round-16 errata heading, both census
files), the two source ids (S278 at lines 163-165, S279), the contract note, the seven
registry cells, the three TMPDIR arms measured end to end on all seven tools, and the
round-53 correction bracket. No stale table cell (the section has no table) and no
self-contradiction found.
