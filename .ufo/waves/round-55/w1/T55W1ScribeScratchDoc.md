# T55W1ScribeScratchDoc — the five-line operator snippet for the scratch-root class

Seat: leaf scribe (no subagent dispatch), milestone "operator snippet", judged on **operability**.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base `0a2010ac`; the frozen counters are at
`631cd645` (round-55 freeze). Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1ScribeScratchDoc`
(`git clone --shared`, then `git -C <clone> checkout -B <name> 631cd645` — a local branch, never the
lane; tool fixes applied inside the clone only). **No lane production file was edited**; the
deliverable is the patch in `08-operator-snippet.patch` plus the scratch-clone demonstration below.
Receipts: `.ufo/waves/round-55/w1/T55W1ScribeScratchDoc-receipts/`.

Census: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0
(§7). The assignment states 139 rows through S279 at round start; the lane's `SOURCES.md` reads **140
rows through S281** in the live worktree at my read (`M corpus/SOURCES.md`, another seat's in-flight
rows S280/S281) — observed, not mine, and not a defect of the validator.

---

## 1. The deliverable — five lines, exactly

Proposed insertion: at the end of `corpus/knowledge/scratch-root-contract.md`, after the closing
blind-spot paragraph of `## One line, every mode (round 55)`, as a new subsection. The block is ten
added lines (heading + blank + fence + five lines + fence); no existing byte is touched.

````markdown
### Operator snippet — parse the class, not a verdict (five lines)

```
# 1  set-but-unusable TMPDIR => exit 2 and ONE line on STDERR; the class is never on stdout (stdout may carry a status token) and never a traceback
# 2  frozen grammar (verbatim, .ufo/evidence/round-55/c2/measure.py:GRAMMAR): ^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.+' \(could-not-evaluate\)$
# 3  parse: rc==2 && grep -Eq 'could-not-evaluate: cannot create clone scratch under the scratch root: ' err; never anchor on the tool name -- that token varies (ENVDIFF_SETUP, WITNESS_STUDY, repeat-control)
# 4  TMPDIR="" is unset, not a path: empty candidates are skipped and the platform default (/tmp) applies -- empty means /tmp, never the CWD and never "no scratch"
# 5  not a pass: a lazy mode (--snapshot/--check/--json/count/--read) exits 0 without allocating and can still print a pass-shaped line ("status": "ok", REPEAT_CONTROL: controls_match), so an unusable TMPDIR is invisible to it
```
````

Line 2 is **byte-identical** to the pattern `measure.py` compiles from its three literals
(`measure.py:46-50`); verified programmatically, not by eye (`11-doc-arms.txt`:
`line-2 pattern == compiled GRAMMAR pattern: True`).

If the L1 prefers `corpus/knowledge/operator-runbook.md`, the identical five lines paste under §0 with
no change; placement in the note is proposed because the note already owns the class and is the file
the C2 `note` arm reads.

## 2. Each line's measured basis (command → receipt)

Allocating modes were run with `TMPDIR` set to a **nonexistent** path; cwd = the clone; both streams
captured separately. The emitted shape (the real bytes, `context-capture --selftest`):

```
context-capture.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r55/T55W1ScribeScratchDoc/no-such-tmpdir' (could-not-evaluate)
```

| line | claim | measurement | receipt |
|---|---|---|---|
| 1 | exit 2, exactly one stderr line; class never on stdout | 8/8 allocating modes `rc=2`, `stderrlines=1`, `grammar=1`, 7/8 with empty stdout, `repeat-control` stdout carries only `REPEAT_CONTROL: setup_error` (a status token, not the class); no `RuntimeError`/`Traceback` on either stream | `01-modes-unusable.txt`, `03-grammar-and-tokens.txt` |
| 2 | the grammar is the frozen regex | line 2 extracted from the note == `GRAMMAR.pattern`; the same regex matches all 8 emitted lines (`matches=1` each) | `03-grammar-and-tokens.txt`, `11-doc-arms.txt` |
| 3 | the prefix parses; the tool name does not | the token before `: could-not-evaluate` is `WITNESS_STUDY`, `ENVDIFF_SETUP` (2/8 are not the filename stem), `repeat-control`, `registry-check`, and `*.py` for three; a filename-anchored parse fails 2/8. Prefix-only parse classifies 8 class + 5 no-class correctly | `03-grammar-and-tokens.txt`, `04-parse-recipe.txt` |
| 4 | `TMPDIR=""` is unset → `/tmp` | `TMPDIR=''` → `tempfile.gettempdir()=/tmp`, `strict_scratch_root() -> /tmp`; all 13 modes keep their expected exit on the empty arm (13/13) | `05-empty-tmpdir.txt`, `02-modes-empty.txt` |
| 5 | a lazy mode's exit 0 is not a pass | 5/5 lazy modes `rc=0` with `0` mkdir calls under `strace`; they print pass-shaped output under the unusable TMPDIR: `REPEAT_CONTROL: controls_match`, `"status": "ok"` + `"verdict_matches_expected": true`, `"exit": 0`. Control: the same allocating tool with a **usable** TMPDIR makes 625 mkdir calls, so the census can see mkdir | `01-modes-unusable.txt`, `04-parse-recipe.txt`, `06-strace-no-scratch.txt` |

The 8 allocating modes are the seven self-tests plus `env-diff --contract`; the 5 lazy modes are
`repeat-control --snapshot`, `bash-witness-study count`, `pin-disposition --read`,
`evidence-disposition --json`, `context-capture --check` — the same 13 the C2 counter measures
(`measure.py:78-115`).

## 3. Why the snippet has to name the stream and refuse the filename anchor

At base the same environment produced lines that a plausible parser reads two different ways
(`10-base-residue.txt`, base clone at `631cd645`):

- `repeat-control.py --selftest` → **stderr** `repeat-control: setup: RuntimeError: cannot create
  clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`
  — the class words are all there, one token (`setup: RuntimeError: `) inside the line; the frozen
  grammar does not match (`grammar_matches=0`) and `RuntimeError` is present.
- `context-capture.py --selftest` → **stdout** `SELFTEST: FAIL (setup error: RuntimeError: cannot
  create clone scratch under the scratch root: …`, **stderr empty** — a stderr-only reader saw
  nothing at all (`10-base-context-capture.stderr` is 0 bytes).

So "which stream" is not pedantry: before the round, one tool's class was on the wrong stream and the
other's was unparseable in place. After the round both are one stderr line, but the tool-name token
still varies.

## 4. Patch and scratch-clone demonstration

1. Fixture clone `$S/fixture` = lane at `631cd645`, then the L1's **uncommitted integration state**
   copied in (`note` sha256 `d3c7eff3…`, `SKILL.md` `a157f37d…`, `registry.json` `429e4718…`, the two
   edited tools; mtimes 13:41; `07-integration-snapshot.txt`), committed as `7600f16`.
2. Snippet applied (the patch above), committed as `25b1333`; `08-operator-snippet.patch`
   (sha256 `3691d197…`, 10 added lines, one file). The patch also passes a read-only
   `git -C <lane> apply --check` against the live note (`rc=0`, no mutation performed), so it lands
   cleanly as long as the note keeps digest `d3c7eff3…`.
3. The **frozen** C2 counter run against that fixture (`--rev 25b1333`, empty `--work`):

```
C2_R55: rev=25b1333d41b3 grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=0 C2_R55_PASS=true
```

(`09-c2-with-snippet.stdout`, counter exit 0). The doc arms are also checked in isolation against the
same commit: note `MARKER` true, 8/8 allocating mode names present, SKILL marker true, 7/7 registry
cells carry the marker (`11-doc-arms.txt`). The snippet is therefore neutral to the counter: it adds
prose that repeats the marker and the mode ids, and touches nothing the other arms read.

## 5. Findings reported, not fixed (frozen artefacts untouched)

- **F1 — `repeat-control` still prints a setup token on stdout.** Under the refusal it emits
  `REPEAT_CONTROL: setup_error` on stdout (`01-modes-unusable.txt`). The round text says "stdout
  carries no setup error"; the frozen counter does not check stdout beyond `RuntimeError`/`Traceback`,
  so C2 passes either way. Either the prose means "no setup *error string*" (then the token is fine
  and my line 1's "stdout may carry a status token" is the accurate wording) or the token is a
  residue the L1 may want to drop in the same tool edit. Reported, not changed.
- **F2 — the class prefix's tool token is not the filename for 2/8** (`ENVDIFF_SETUP`,
  `WITNESS_STUDY`). The frozen grammar permits any `[A-Za-z][A-Za-z0-9_.-]*(\.py)?` prefix, so this
  is conformant; it only breaks callers that anchor on the filename, which line 3 of the snippet
  forbids. No action required for C2.
- **F3 — `evidence-disposition --json` prints `"exit": 0` inside its JSON under an unusable
  TMPDIR.** That field is not the process exit code; a parser that greps stdout JSON for `exit` can
  misread a lazy run. This is the concrete instance behind line 5. Reported for the note's blind-spot
  sentence; not fixed (tool behaviour is out of this seat's scope).
- **F4 — frozen counters/contract:** nothing found that I believe is wrong. The contract's C2
  `cannot_see` bullet ("whether a caller parses the grammar by prefix or by the whole line") is the
  gap this snippet answers, so the snippet is a documentation complement, not a counter change.
- **F5 — census row drift:** assignment says 139 rows (S001-S279); live `SOURCES.md` has 140 rows
  through S281 in the worktree (S280/S281 added by another seat while this ran). Census exits 0
  (receipt `12-census.txt`).

## 6. Limits

- The snippet is a **proposal**; the lane note still lacks it until the L1 applies
  `08-operator-snippet.patch`. Everything above was measured on the fixture, not on the lane.
- The fixture reproduces the L1's uncommitted doc state as of 13:41 (digests in
  `07-integration-snapshot.txt`). If the note/SKILL/registry change after that, re-run the counter; the
  snippet itself is text and cannot change the tool arms.
- 13 documented modes only. A mode outside the registry and usage text is outside both the counter and
  this check — the note already names that blind spot.
- "platform default (/tmp)" is measured on this host; other platforms may resolve differently (the
  contract's three arms are about the lane's resolver, not about every OS).
- A first counter run lost its scratch to an external `rm -rf` at 13:54 (job survived, files gone);
  everything here is from the rebuild whose receipts are in the durable directory, and the counter was
  re-run end to end afterwards.

## 7. Tools, versions, conformance

No installs or upgrades were made. Used: `git 2.56.0`, `Python 3.14.8`, `strace 7.2`,
`bash 5.3.20`. Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tameshi` → exit 0 (`12-census.txt`).

## 8. Artifacts

Report: `.ufo/waves/round-55/w1/T55W1ScribeScratchDoc.md`.
Receipts (`.ufo/waves/round-55/w1/T55W1ScribeScratchDoc-receipts/`):

| file | content |
|---|---|
| `00-setup.txt` | clone toplevel, tool-fix patch application, patch sha256 |
| `01-modes-unusable.txt` | 13 modes under a nonexistent TMPDIR: rc + stream sizes |
| `02-modes-empty.txt` | 13 modes under `TMPDIR=""` |
| `03-grammar-and-tokens.txt` | each rc=2 line vs the frozen regex; tool-token census |
| `04-parse-recipe.txt` | the snippet's prefix parse over 13 modes; pass-shaped lazy stdout |
| `05-empty-tmpdir.txt` | `gettempdir()` and `strict_scratch_root()` under `""` vs unset |
| `06-strace-no-scratch.txt` | lazy/allocating mkdir census + usable-root control |
| `07-integration-snapshot.txt` | digests/mtimes of the L1 state copied into the fixture |
| `08-operator-snippet.patch` | the proposed 10-line addition (sha256 `3691d197…`) |
| `09-c2-with-snippet.stdout` | frozen C2 counter at the snippet commit: `total=0 PASS=true` |
| `10-base-*` | base residue: stderr/stdout bytes and grammar match at `631cd645` |
| `11-doc-arms.txt` | verbatim-pattern identity, note/SKILL/registry arms at the snippet commit |
| `12-census.txt` | census validate output (exit 0) |
| `strace-*.log` | raw traces behind the mkdir census |
