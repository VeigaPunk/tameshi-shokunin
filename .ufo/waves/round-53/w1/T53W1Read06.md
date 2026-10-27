# T53W1Read06 — cold read of `## Repeated controls and gate registry — round 12`

Candidate `C*` = `a41195dfc13a73958e4c5228ec196b28d03ded03`. Section read from git objects only
(`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C*:SKILL.md`), never the working tree.
Scratch root: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read06/` (deleted before yield).

- Section bytes: **1371**, sha256 **`532bebc8fad6dadff4ef3581677a15230b994cbbac56dbdaa571e59204cf0d74`**.
- Heading line range at C*: **1486–1504** (1-based, inclusive). Next heading `### Gate/probe registry`
  at 1506; line 1505 is the whitespace-only line the frozen monitor strips.
- Split method reproduced twice (independent implementations agree, see Checks C1/C2):
  line-split on `\n`, heading = `^#{1,3}(\s|$)` outside ``` fences, section = heading line through the
  line before the next heading, trailing whitespace-only lines stripped, joined with `\n`, no trailing
  newline, sha256 over UTF-8 `surrogateescape` bytes.

## Checks run (commands and observed output)

All tool runs used the C* blob of `tools/repeat-control.py` (extracted with `git show C*:…`), never the
working-tree copy; `TMPDIR` pointed at my scratch.

- **C1 — split, primary.** Python walker over the extracted SKILL.md: `matches: [42] total heads: 63`,
  `heading line range (1-based): 1486 - 1504`, `next heading line: 1506`, `section bytes: 1371`,
  `sha256: 532bebc8fad6dadff4ef3581677a15230b994cbbac56dbdaa571e59204cf0d74`.
- **C2 — split, independent.** `awk 'NR>=1486 && NR<=1504' skill.md` then strip the trailing newline and
  sha256 → `532bebc8fad6dadff4ef3581677a15230b994cbbac56dbdaa571e59204cf0d74`, 1371 bytes,
  `trailing ws-only lines removed: True`. No ``` fence line exists between 1440 and 1520, so the
  fence state cannot move the boundary here.
- **C3 — cited paths exist at C*.** `git ls-tree -r --name-only C*` contains
  `corpus/knowledge/repeated-control-precondition.md`, `.ufo/evidence/round-12/verification-final.json`,
  `.ufo/evidence/round-12/ControlGate/expected.json` and
  `.ufo/evidence/round-12/ControlGate/mismatch/expected.json`, and `tools/repeat-control.py`.
- **C4 — the receipt is the gate's runtime evidence.** `verification-final.json` at C* holds 10 checks;
  the gate's rows are `repeat-control-selftest` (expected/observed 0), `frozen-match` (0),
  `frozen-mismatch` (1) and `real-pristine-three-controls` (0), each with `REPEAT_CONTROL: …` stdout.
- **C5 — decision table, executed against the C* tool** (three-run controls, out dirs under my scratch):
  - row 1, identical zero-exit: `REPEAT_COMPARE identical=yes runs=3` → `REPEAT_CONTROL: controls_match`, exit 0.
  - row 2, stdout differs (`echo $RANDOM`): `REPEAT_COMPARE identical=no runs=3` →
    `REPEAT_CONTROL: controls_mismatch`, exit 1.
  - row 3a, equal nonzero (`exit 7`, three times): `identical=yes` → `REPEAT_CONTROL: baseline_nonzero`, exit 2.
  - row 3b, missing argv[0]: `REPEAT_RUN 1 exit=unavailable` ×3 → `REPEAT_CONTROL: command_unavailable`, exit 2.
- **C6 — "The output directory must not exist."** Re-running with an existing `--out`:
  `repeat-control: --out already exists (refused, never overwritten)` → `REPEAT_CONTROL: invalid_usage`, exit 64.
- **C7 — "Caller owns timeout policy; hanging commands yield no verdict."** The C* tool has no timeout
  and no process supervisor (`grep -n 'timeout' tools/repeat-control.py` → only the docstring lines
  "there is no timeout and no process supervisor … or hangs it indefinitely"), so a hanging command
  produces no verdict line without the caller's own wrapper. Holds.
- **C8 — the cited snapshot receipts still verify with the C* tool.**
  `python3 repo/tools/repeat-control.py --snapshot …/ControlGate` → `SNAPSHOT_INPUTS 9 verified`,
  `REPEAT_CONTROL: controls_match`, exit 0; `…/ControlGate/mismatch` → `controls_mismatch`, exit 1.
  `--selftest` → `SELFTEST: PASS (29 cases)`, exit 0. All with
  `REPEAT_CONTROL_TOOL … tool-sha256=6dd44263c2b3f9ebe847cd0263a9bed0b096036ebea88288a196b4410416477e`.
- **C9 — scratch policy lines inside the same file.** `grep -n HYAKU_SCRATCH skill.md` → lines 25, 136,
  158, 1982. Line 25 at C* reads: "**Scratch namespace is `$HYAKU_SCRATCH` (default
  `/fast/scratch/hyaku`)/`<lane>-r<round>-<n>-*/`** (host scratch directive of 2026-10-25: `/tmp` is
  for files under 50 MB only; a seat deletes its tree on exit)". Line 1982's recipe uses
  `--out "$HYAKU_SCRATCH/tameshi-f5.json"`.
- **C10 — retained evidence size and mode.** `os.makedirs(out_dir)` in the C* tool creates the out dir
  with default mode; my run's `out/c1` is `drwxr-xr-x` (0755), and every run's full streams are copied
  in. The fleet's own byte-boundary matrix records a 400,000 B stdout + 400,000 B stderr case
  (`git cat-file -s C*:.ufo/evidence/round-12/BytesReview/cli/C19-large-dual-stream/run-1.stdout` →
  400000; same for `run-1.stderr`), i.e. `--out` volume is bounded only by the command.
- **C11 — the receipt shows the recipe was followed as written.** In `verification-final.json` the
  three `--runs 3` checks record `--out /tmp/tameshi-r12-integrated-kkp7con7/real-controls`,
  `--out /tmp/tameshi-r12-oracle-repair-yywimjvg/red-before-single-control-mutant` and
  `--out /tmp/tameshi-r12-oracle-repair-yywimjvg/green-after-restored-repetition` — the `/tmp`
  instruction is live practice, not a hypothetical.
- **C12 — source rows.** `corpus/SOURCES.md:140` = S265 row, teaches "supersedes S026 — …
  re-anchored to the 2026-10-26 bytes"; `corpus/SOURCES.md:500` = "Round 48: four rows added, S265-S268
  (superseding held S026, S048, S093, S108 …)". `corpus/knowledge/repeated-control-precondition.md`
  opens "source: S004 … ; S265 (supersedes S026) — …". `grep -n 'S026\|S265' SKILL.md` → only line 1488,
  the line under test; S265 appears nowhere in SKILL.md.

## Holds (pointers verified against C* bytes)

- **`corpus/knowledge/repeated-control-precondition.md`** — exists at C* and is the note this section
  leans on; its §3.1 table reproduces exactly the section's three decision rows and its exit-2 class
  (`baseline_nonzero`, `command_unavailable`, `setup_error`, `invalid_usage` 64, `snapshot_tampered`).
- **`runtime evidence: .ufo/evidence/round-12/verification-final.json`** — exists, is the gate's
  receipt, and its four gate checks still reproduce with the C* tool bytes (C8). *Caveat, not filed as
  a finding:* the receipt's `REPEAT_CONTROL_TOOL … tool-sha256=296fe566…` names the round-12 tool
  revision, while the C* blob hashes `6dd44263…`; `git diff 9df9212 C* -- tools/repeat-control.py` is
  exactly one line (`dir="/tmp"` → `dir=tempfile.gettempdir()` in `selftest()`), and C8 shows that
  revision still produces the same verdicts. The section's statement ("runtime evidence: <file>") holds;
  the pin inside the file is older than the tree.
- **Rows 1–3 of the decision table** — each row reproduced by execution (C5), including the precedence
  the note states (a disagreement is `controls_mismatch` before `baseline_nonzero`; unavailable argv is
  `command_unavailable` even when the three "unavailable" samples are identical).
- **"The output directory must not exist."** — C6.
- **"Caller owns timeout policy; hanging commands yield no verdict."** — C7.
- **"put evidence outside any tree it inspects"** — matches the C* tool's own warning
  (`--out` placed inside a tree the command itself inspects makes the command disagree with itself).
- **"not a change to the six-leg runner of round 12"** — historically scoped and true: the C* runner
  header records the leg history `r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten`, so six legs
  is round 12's shape. *Caveat, not filed:* at C* the live runner has ten legs, so a reader who takes
  the phrase as the fleet's current shape is misled; the explicit "of round 12" scoping is why this is a
  hold rather than a finding.
- **"Do not retry until green, normalize output, or interpret a finite match as proof of reliability"**
  and the sensitive-data warning — normative and consistent with the tool (unnormalized byte compare,
  no retry loop); no source contradiction found.
- The section is dated/historical in no other respect that changes a checkable claim: it carries no
  counts other than the decision rows and the six-leg scope, both examined above.

## Findings

### F1 — scratch-directive violation (the recipe sends retained evidence to `/tmp`)

Quote (byte-exact, single line, line 1499):

> --out /tmp/tameshi-r12-controls-UNIQUE

Why it fails at C*: the same file's standing rule (line 25) puts a round's scratch under
`$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`)/`<lane>-r<round>-<n>-*/` and bounds `/tmp` to files
under 50 MB. This recipe names `/tmp` with no namespace and no size bound, for the evidence of an
arbitrary `COMMAND` whose full stdout and stderr the tool copies per run into a directory it creates
mode 0755 (C10; a recorded case is 400,000 B × 2 per run). The section's own closing line warns the
same streams "may contain sensitive data", which is the opposite of the shared, world-readable `/tmp`
it instructs the caller to retain them in. The other recipes in this file were moved to
`$HYAKU_SCRATCH` (lines 136, 158, 1982); this one was not, and the round-12 receipt shows the `/tmp`
form being executed (C11). A caller following the section cannot satisfy the directive it lives under.

### F2 — stale source pointer (`S026` is held-superseded by `S265`)

Quote (byte-exact, line 1488):

> Source: S004/S026 and `corpus/knowledge/repeated-control-precondition.md`

Why it fails at C*: `corpus/SOURCES.md:140` records S265 as "supersedes S026 — … re-anchored to the
2026-10-26 bytes", `corpus/SOURCES.md:500` records round 48 adding S265–S268 "superseding held S026,
S048, S093, S108", and the note cited on this same line already reads "S265 (supersedes S026)". The
section therefore cites a held row as its current source while the companion pointer on the same line
says that row is superseded; S265 is named nowhere in SKILL.md. The lane's convention is explicit
qualification (SKILL.md:1565 "S048 supersedes S047's object-specific", SKILL.md:1688 "superseded in
round 17"), so the unqualified `S026` is the defect, not a stylistic choice.

Everything else in the section held under execution; no third finding is filed, and nothing in this
report upgrades an unrun check to evidence.

## Limits

- The `--runs 3` probes (C5) ran my own trivial commands (`bash -c`, `exit 7`, a missing argv[0]), not
  the fleet gates; they falsify the decision table, not any gate's stability.
- C8 ran the C* tool from a scratch tree with the committed `ControlGate` snapshot files copied in
  (`git show C*:…`), because `--selftest` resolves its fixture root relative to the tool's own path; the
  repo itself was not written to.
- "Sensitive data" is the section's own premise; I measured the out-dir mode and the per-run copy
  behaviour, not any particular leak.
- No tool was installed or upgraded for this seat (nothing needed): no uv/cargo/npm/pacman transaction,
  per the host-wide pacman pause.
- Scratch tree `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read06/` (SKILL.md copy, C* tool blob, copied
  snapshot fixtures, `out/`, `tmp/`) was removed before yield.
