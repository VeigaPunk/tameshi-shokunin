# T54W1ConnDuplicateNote — duplicate-note scan of `corpus/knowledge/scratch-root-contract.md`

Seat item: search `corpus/knowledge/` for notes that already state any part of the
scratch-root contract (env-diff contract drift, service limits, the tools registry
notes, the round-53 lesson) and report where the new note duplicates or contradicts
them; name each overlap with file:line and propose the sentence the new note should
carry to point at the older home instead of restating it. **No edits made.**

Sweep: a regex pass over every `corpus/knowledge/*.md` plus `corpus/lessons/`,
`tools/registry.json`, `SKILL.md` for `scratch.?root|strict_scratch|ScratchRoot|
TMPDIR|dir="/tmp"|could-not-evaluate|foreign scratch|env-diff`. Receipt:
`.ufo/waves/round-54/w1/T54W1ConnDuplicateNote-receipts/citation-sweep.txt`
(command + per-citation PASS lines; verdict ALL_PASS; 20/20 cited needles resolve
at the named lines; 7/7 registry `scratch_root` cells confirmed to both cite the
note and restate all three arms).

## Verdict up front

No outright contradiction found — the new note's scope phrase
"Every lane tool that allocates scratch through a `strict_scratch_root()` helper"
correctly fences it to the seven Python tools. But it **restates three things
older homes already own**, and it sits one sentence away from two older `/tmp`
conventions it neither cites nor delimits. Five overlaps, each with the proposed
pointer sentence.

## Overlap 1 — the exit-class principle is already homed (DUPLICATES)

`corpus/knowledge/repeated-control-precondition.md` already owns the rule the new
note re-derives:

- `:28` — "An unusable baseline yields no verdict. … Exit-2 is that shape — a
  refusal to evaluate, never a kill and never a clean pass."
- `:41-45` — the exit map: `baseline_nonzero` / `command_unavailable` /
  `setup_error` / `snapshot_tampered` → 2 could-not-evaluate; invalid usage → 64.

New note `:34-36` ("A set-but-unusable `TMPDIR` is an environment fact, not a
failed measurement: the gate did not run, so no verdict may be printed and the
exit class is could-not-evaluate (2)") restates that convention without citing it.
`guard-kill-closure.md:18` ("A nonzero pristine exit is could-not-evaluate (exit
2), never \"closed\"") is a second precedent for the same class.

**Proposed sentence for the new note** (in "Why the class is uniform"):
> "The class is the lane's standing convention — an unusable baseline yields no
> verdict (`repeated-control-precondition.md:28`, `:41-45`;
> `guard-kill-closure.md:18`); this note binds that convention to the
> scratch-root arm, it does not invent it."

## Overlap 2 — the R53.6 history is already homed in the round-53 record (DUPLICATES)

`corpus/lessons/round-53-verifier-spotcheck.md` already records every fact in the
new note's history paragraph (`:37-41`):

- `:83` — "**R53.6 — CR47 exit-class mapping incomplete in 4 of 7 tools.**
  bash-witness-study, env-diff, evidence-disposition, pin-disposition raise an
  uncaught RuntimeError (rc=1) on set-but-unusable TMPDIR instead of the declared
  could-not-evaluate exit 2 (registry-check, context-capture, repeat-control map
  correctly; no silent /tmp fallback anywhere)."
- `:47-48` — the measured prior state: `dir="/tmp"` = 9 in 7 files at base → 0;
  "`strict_scratch_root()` present in exactly the 7 claimed tools".
- `corpus/lessons/round-53.md:7` names the axis ("C2 operability — `tools/`
  scratch hygiene") and `:120` records the scratch-directive staleness fix that
  touched "Standing rules, recipe, registry rows".

The new note paraphrases all of it ("Round 53 removed the silent `/tmp` fallback
in seven tools and its own closure spot-check routed the residue … routed defect
R53.6") — it does name R53.6 but re-narrates the residue instead of pointing.

**Proposed sentence:**
> "The residue this arm closes is routed defect R53.6
> (`corpus/lessons/round-53-verifier-spotcheck.md:83`; the 9→0 `dir="/tmp"`
> sweep and the 7-tool `strict_scratch_root()` population are measured at
> `:47-48`; the axis is named at `corpus/lessons/round-53.md:7`)."

## Overlap 3 — the `dir="/tmp"` census findings are the falsifier's home (DUPLICATES)

New note `:59` — "A tool that regains a `dir=\"/tmp\"` literal fails the round-53
monitor and the C2 `tmp_mkdirs` arm together." The literals it guards against are
already catalogued:

- `corpus/knowledge/r41-variable-destination-writes.md:37`, `:53` — census rows
  recording `scratch = tempfile.mkdtemp(…, dir="/tmp")` at `:597` and
  `self.root = tempfile.mkdtemp(…, dir="/tmp")`.
- `corpus/knowledge/r42-attribute-and-outflag-destinations.md:32` — the same
  literal in `tools/context-capture.py`; `:101-102` even anticipates the
  identifier collision ("`/tmp` inside `tmpl` or an identifier such as
  `scratch_root` flips `scratch`") — which is now the new contract's own name.

**Proposed sentence** (appended to the Falsifier):
> "The `dir=\"/tmp\"` shape is the write-path census's recorded class
> (`r41-variable-destination-writes.md:37`,`:53`;
> `r42-attribute-and-outflag-destinations.md:32`); v4's resolved-text check
> (`r42:101-102`) already treats a `scratch_root` identifier as scratch, so the
> literal test and the identifier test do not collide."

## Overlap 4 — the service-scratch convention is adjacent, undelimited (BOUNDARY, not duplication)

The older service corpus owns a *different* scratch rule the new note never
mentions — and its own "nothing falls back to `/tmp`" sits next to it:

- `corpus/knowledge/service-optin-protocol.md:86-91` — "**Scratch namespace per
  lane.** Every write is lane-scoped (round-7 convention `/tmp/w7-<lane>-*`)…";
  `:105` — the template row "scratch: `/tmp/w7-<lane>-*` (lane-scoped; foreign
  scratch never removed)".
- `corpus/knowledge/service-limits.md:55` (refusal row j) and `:165-170` — the
  same convention as detail of record; `service-standing-state.md:72` the same
  again as the lane-owned boundary row; `operator-runbook.md:213`, `:263` the
  compact restatement.
- `corpus/knowledge/operator-runbook.md:120` — the runner's evidence default
  `mktemp -d /tmp/tameshi-r4-2-run.XXXXXX` (SKILL.md:1408 already discloses this
  is stale vs TMPDIR honouring; `mutate-and-run.sh` is a bash tool outside the
  seven anyway).

A cold reader can misread "nothing falls back to `/tmp`" + "no `mkdir` under
`/tmp`" as condemning the documented `/tmp/w<N>-*` service convention or the
`/tmp` scratch receipts the older notes are built on. One boundary sentence
fixes it.

**Proposed sentence** (end of the Three-arms table block):
> "Scope: this contract binds only the seven tools' TMPDIR-resolved
> allocations. The mutation service's lane-scoped scratch convention
> (`/tmp/w<N>-<lane>-*`, foreign scratch never removed —
> `service-optin-protocol.md:86-91`,`:105`; `service-limits.md:55`,`:165-170`)
> and the seat-level `$HYAKU_SCRATCH` rule are separate homes this note does
> not restate."

## Overlap 5 — the env-diff note's `/tmp` paths are the named "contract drift" adjacency (BOUNDARY)

`corpus/knowledge/hermetic-env-differential.md` — the note behind the tool the
new contract covers — still documents `/tmp` surfaces the new note ignores:

- `:3` — recheck writes `--out /tmp/tameshi-f5-recheck.json` (caller-chosen
  output path, not a resolver allocation — not a violation, but a visible `/tmp`
  in the covered tool's own home note).
- `:27`, `:82` — the bwrap scratch "private writable `/tmp/w`" and the
  `kumitate-round-gate-selftest-*` dirs beneath `/tmp/w/tmp` (the sandbox mount,
  again outside `strict_scratch_root()`).
- `:34` — the `clean` profile's "private HOME/TMPDIR" (the mechanism the new
  contract now pins arms for).
- Adjacent history: `corpus/lessons/round-48.md:354` — env-diff mounts a tmpfs
  on `/tmp`, which is *why* the round-47 counter's `/tmp`-placed `--work`
  masked the interpreter (the concrete "env-diff contract drift" instance).

**Proposed sentence:**
> "`env-diff.py`'s own experiment scratch is the bwrap `/tmp/w` mount and its
> recheck `--out` is caller-chosen (`hermetic-env-differential.md:3`,`:27`);
> the round-48 attribution (`corpus/lessons/round-48.md:354`) is the same
> mechanism. This contract governs only what the helper resolves from TMPDIR."

## Overlap 6 — the registry cells and SKILL bullet restate all three arms (two-direction duplication)

The item's "tools registry notes": all seven `scratch_root` cells
(`tools/registry.json:44`,`:87`,`:135`,`:333`,`:424`,`:620`,`:862`) carry the
full three-arm sentence verbatim *and* cite the note; `SKILL.md:32-39` (Standing
rules bullet) likewise restates all three arms and cites the note. The new note
`:30` answers with "the registry rows say so" — i.e., each side states the whole
contract and each side cites the other. The lane's own precedent for this shape
is explicit: `operator-runbook.md:247-250` and `service-limits.md:10-12` declare
"restates with pointers — it is not a second home; on drift the anchored source
governs." The new note never says which side governs.

**Proposed sentence** (replacing ":30 …the registry rows say so."):
> "The seven registry `scratch_root` cells and the SKILL standing-rules bullet
> are compact restatements that point here; on divergence this note is the
> anchored source (the rendering/divergence rule of
> `service-limits.md:10-12`, `operator-runbook.md:247-250`)."

## What was opened and checked

- `corpus/knowledge/scratch-root-contract.md` (full, 60 lines at C0).
- Every `corpus/knowledge/*.md` swept for scratch/TMPDIR/exit-class terms;
  hits read in context: `service-limits.md`, `service-optin-protocol.md`,
  `service-standing-state.md`, `operator-runbook.md`, `hermetic-env-differential.md`,
  `repeated-control-precondition.md`, `r41-variable-destination-writes.md`,
  `r42-attribute-and-outflag-destinations.md`, `guard-kill-closure.md`,
  `gates-survey-kumitate.md`, `closeout-r11.md`, `executor-test-sufficiency.md`,
  `mutation-case-*` notes (TMPDIR-as-suite-env rows — adjacent, not overlapping:
  they use TMPDIR as a per-defect sandbox env var, not as the tools' resolver
  input), `incremental-pin-disposition.md`, `required-command-binding.md`.
- `corpus/lessons/round-53.md` (`:1-128`), `round-53-verifier-spotcheck.md`
  (`:43-90`), `round-54.md` (Gate/QUALITY), `round-48.md` (`:309`,`:354`),
  `round-52-verifier-spotcheck.md:87` (R52.5 root cause).
- `tools/registry.json` — 7/7 `scratch_root` cells located and content-checked.
- `SKILL.md:17-39` (the three-arm bullet), `:1408` (stale-runbook disclosure),
  `:2168-2197` (registry table TMPDIR cells).
- `corpus/SOURCES.md:152-154` (S277–S279 rows) — correctly point at the new
  note; no second home.
- `corpus/README.md` frontier — no scratch-root row conflict.

## Bottom line for the L1

The note is not a duplicate home for the *contract itself* — it is the right new
home. The defects are (a) three restatements of already-homed facts (exit-class
convention, R53.6 history, `dir="/tmp"` census) that should be pointer clauses,
and (b) two missing boundary sentences against adjacent `/tmp` conventions
(service-scratch and env-diff's own `/tmp` paths) where a cold reader could
manufacture a contradiction that does not exist. Proposed sentences above are
drop-in; none requires touching the older notes.
