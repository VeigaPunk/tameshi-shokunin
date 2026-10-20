# R05 — Contract C review: input-keyed cold-read credit

Seat: TameshiR17.R05ReviewContractC (reviewer, leaf). Lane tip at dispatch:
`98bea7da5801f4bc58e4187690ee1687c8a5061f`. Reviewed against contract C as dispatched and the
round-16 implementations it ports: `.ufo/evidence/round-16/measure.py` (665 lines) and
`.ufo/evidence/round-16/coldread/assemble.py` (41 KB). All counts below read committed blobs at
explicit revs; nothing depends on the live lane's `HEAD` (see the live-lane notice, §7).

## 0. Executed checks (commands, exits, key lines)

| check | command (abridged) | result |
|---|---|---|
| v1 baseline at tip | `python3 .ufo/evidence/round-16/measure.py --rev 98bea7d…` | exit 0; `sections_covered 54/54`, `box3_full_page true`, `calibration_restraint_score 8` |
| ledger census | parse `.ufo/evidence/round-16/coldread/ledger.json` | 75 entries, 75 distinct sha256; 54 entries match the 54 tip sections; 21 entries are dead (pre/post-page sha versions); matched entries: 30 `record`, 24 `instruction`, **54/54 have `commands_executed_count>0`**, 0 have `inputs` |
| v2-rule red-before | applied the C rule to those 54 matched entries [COMPUTED at review start; the built v2 measure later reproduced it — §10] | `0/54`, all `inputs-unrecorded`; with round-17 `BOX3_LINK` absent at 98bea7d → `box3_full_page false`, score 6 |
| class-dodge credit | `measure.entry_credit_reason({"class":"record","verdict":"verified-record","commands_executed_count":0})` | `None` (credits); end-to-end `coldread()` 1/1 covered with `inputs:{}` |
| duplicate-sha aggregation | `coldread()` with two entries for one sha: `[instruction/executed-ok, instruction/gap-blocking]`, both orders | section **covered** despite the `gap-blocking` entry (measure.py:243-256 breaks on first credit) |
| missing-vs-drift resolution | `git show HEAD:d` (directory), `git cat-file blob HEAD:d`, `HEAD:nope`, `HEAD:untracked`, `HEAD:/f`, `HEAD:./f`, `ls-tree` on a symlink | `git show` dir → **exit 0**, prints `tree HEAD:d`; `cat-file blob` dir → exit 128; missing/untracked/leading-`/` → exit 128; `HEAD:./f` → exit 0; `ls-tree` symlink mode `120000` |
| r16 `blob()` on a tree | `measure.blob('.', 98bea7d, 'tools')` | returns `b'tree 98bea7d…'` (measure.py:83 uses `git show`) |
| empty preamble | `sectionize(b'\n\n# A\nbody\n')`; ledger entry for `sha256(b'')` | preamble bucket `start 1`, sha `e3b0c442…`; a `record/verified-record/0 cmds` entry covers it (2/2) |
| lenient counts | `commands_executed_count: True`; `"2"` | both credit (`int()` at measure.py:189-205) |
| revision echo | `measure.py --repo <clone> --rev HEAD` | `"revision": "HEAD"` — the resolved commit is never used for blob reads or output (measure.py:648-660) |
| filters | `.gitattributes` absent at 98bea7d; global git-lfs filters configured, no patterns | worktree bytes == blob bytes for tracked lane files today |

## 1. Findings

### F1 — BLOCKING (soundness): duplicate entries for one sha are aggregated permissively; a clean entry launders a failing one
`measure.py:243-256`: `by_sha` keeps ledger order and `coldread()` sets `covered=True` and `break`s on
the **first** entry that credits. Any later entry for the same sha — including
`verdict:"gap-blocking"`, `blocking_gaps>0`, `wrong_expectations>0` — is never examined. Executed:
one section, entries `[clean, gap-blocking]` → `sections_covered 1/2`, no missing record for that
section; reversed order identical. This is not hypothetical for v2: X09's assembler **keeps both
entries** when their `inputs` maps differ, and also keeps one entry per page pin, so two entries for
one sha with different inputs is the designed normal shape. Contract C fixes the input gate but says
nothing about aggregation, so the v2 measure as specced would inherit the v1 any-credit rule.
The r16 ledger escapes the demonstration only because its 21 duplicate-looking entries carry stale
page shas and do not match tip sections.

### F2 — BLOCKING (soundness): class dodging is a free credit under the contract's "no executed commands" exemption
Executed: `{"class":"record","verdict":"verified-record","blocking_gaps":0,"wrong_expectations":0,"commands_executed_count":0,"inputs":{}}` credits, end-to-end. Contract C's sentence "entries with no
executed commands keep v1 rules" makes that exact object a valid ledger entry for any section — no
command, no input, no page evidence. A seat that executed a bucket but wants to skip input-keying only
has to label it `record` and omit `commands_executed`; a seat that executed nothing gets the same
credit. The class label is seat-declared and cannot be inferred from the page (30 of the 54 matched
r16 entries are `record` *and* executed commands — e.g. record+`verified-record`+cmd 7 at start 794 —
so measure must not force `record` to have zero commands either). Cost of closing it: zero on the
actual page — all 54 matched entries have `commands_executed_count>0`, so the exemption changes
nothing in v1-shaped data.

### F3 — MAJOR (determinism/correctness): deleted / renamed / untracked / directory / symlink inputs are not distinguished, and the natural r16 helper mislabels them
Contract C names only `input-missing:<path>` and `input-drift:<path>` but does not pin the byte
source. r16's `blob()` uses `git show REV:path` (measure.py:83); executed: on a directory it **exits 0
and prints a tree listing**, so a v2 measure that reuses `blob()` reports `input-drift` for a directory
instead of `input-missing`; a tracked symlink also yields its target-path string as "content", so a
real content digest drifts. Also verified: `HEAD:./f` exits 0 (non-canonical keys resolve),
`HEAD:/f`, `HEAD:d/../f`, untracked paths and missing paths all exit 128. Pin `git cat-file blob` plus
`git ls-tree` mode, and canonical key grammar (§4 step 4).

### F4 — MAJOR (evidence integrity): "every lane input it ran against" is not enforced; the seat chooses what to list
Contract C defines `inputs` as "every lane-tracked regular file the section's executed commands opened
(captured by trace-inputs.py) plus every lane file the seat opened to check the section", but nothing
binds the trace receipts to the ledger map: X09's spec never reads `traces`, and the measure cannot.
A seat can run the trace (satisfying the prose in its report) and then hand-write a smaller `inputs`
map; the measure verifies only the smaller map, so the drift check silently misses exactly the inputs
it exists to key. The credit rule's soundness depends on an assembler-side superset invariant (§5 A4).

### F5 — MAJOR (undefined semantics): `read_rev` and merged v2 entries
The v2 entry adds per-entry `read_rev` and `inputs`, but X09's spec merges entries sharing
`(skill_sha256, start)` when their `inputs` agree and keeps both otherwise. A merged entry then has one
`seats`/`reports` list but no well-defined single `read_rev`, and two observations at different
`read_rev` with identical inputs would be merged (input maps agree) even though their read points
differ. (The built assembler goes further and keys the group on `read_rev` and `external_inputs` as
well — §10 — but the contract text does not say so.) Contract C never says which value the entry
carries, whether `read_rev` must resolve, or whether the page blob at `read_rev` must equal
`skill_sha256`. Today `read_rev` is decorative in C.

### F6 — MINOR (brittle false negatives, must be sequenced): the page is itself an input
A seat that reads the section opens `SKILL.md`; the contract requires that file in `inputs`, and the
input gate then verifies it at REV. Any page edit after a seat's trace (round-17 section appends, a
post-review repair, a front-matter tweak) yields `input-drift:SKILL.md` for **every** entry that
listed it — even entries whose section bytes are unchanged. That is the literal intent of
"at the measured rev", but it forces a full re-read after any page edit. The alternative (exempt the
page) is worse: Appendix A/B are "reproduce from this page alone" sections whose commands touch only
`/tmp` (trace-inputs records neither `/tmp` nor non-lane files), so with the page exempt their `inputs`
would be empty and `inputs-unrecorded` would uncredit honest execution. Recommendation: keep the page
in `inputs`, verify it, and state the wave order (§6). Reads of an immutable committed snapshot (e.g.
`.ufo/evidence/round-16/coldread/SKILL.snapshot.md`) are the stable pattern when the page must move.

### F7 — MINOR: preamble bucket
The preamble is a first-class bucket (heading `""`, start 1). Executed edge: a page whose pre-heading
lines are all blank produces a preamble with the empty-string sha `e3b0c442…`, which a
`record/verified-record/0 cmds` entry credits under v1 (and under F2's exemption); under the §4 rule it
needs a verified input like any other section. A page beginning with a heading has **no** preamble, so
`sections_total` shifts by one between pages — the assembler's `--expect-skill-sha` and the measure's
sectionizer must be the same function. Contract C says "the same sectionizer", but X07 and X09 are
separate files built by different seats; a divergence in fence toggling, front-matter `#` comment
lines (a YAML `# comment` line *is* a heading under `^#{1,3}(\s|$)` and splits the front matter), or
trailing-blank stripping silently uncredits the whole page.

### F8 — MINOR (counting honesty): the cited number must be reproducible from committed bytes
- `revision` echoes the raw `--rev` argument (`"revision": "HEAD"` executed above), and all blob reads
  use `args.rev` (measure.py:654, 660) while the resolved commit at line 648 is discarded. If the
  argument is a moving name, the census and the echoed identity can disagree.
- `--ledger-file` can credit a ledger that is not committed at REV, while `box3_link` proves only that
  the *path* is named. A count of 8 from an uncommitted ledger is not evidence about REV.
- `--inputs-overlay` appears in C's usage line with no schema or precedence; X07 defines it as a JSON
  list of `{start, heading, skill_sha256, read_rev, inputs}` merged by `skill_sha256+start` "for legacy
  red-before". The contract text must carry that definition and mark overlay-derived credit as
  not-committed.

### F9 — MINOR: input grammar and integer strictness
r16 accepts `True` for `commands_executed_count` and `"2"` (executed: both credit) because it calls
`int()`. For a committed v2 ledger the assembler writes real ints, so the measure should reject
booleans/numeric strings as `malformed-entry`. `inputs` keys need a canonical grammar (UTF-8, no NUL,
no leading `/` or `./`, no `..` or `.git` component) so reason strings are deterministic; `external_inputs`
keys that resolve under the lane root should be a report error (otherwise a lane file can be filed as
"external" and escape verification).

### F10 — MINOR: the in-flight ledger as an input
If a traced section command consumes `.ufo/evidence/round-17/coldread/ledger.json` (e.g. measure with
`--ledger-file`), the recorded digest is of the partial/being-assembled file, while REV's ledger bytes
are the assembled result — `input-drift` by construction. Not a rule bug: seats must not trace
commands that consume the ledger under construction, and the ledger must not be listed as a section
input.

## 2. The seven named edge cases — rule outcome

| edge case | outcome under §4 | reason |
|---|---|---|
| input deleted at REV | uncovered | `input-missing:<path>` |
| input renamed at REV (content now at another path) | uncovered; renames are **not** followed | `input-missing:<old path>` |
| input untracked at REV (worktree-only, scratch, or the in-flight ledger) | uncovered; measure reads committed blobs only | `input-missing:<path>` |
| inputs recorded from a dirty clone (modified tracked file) | uncovered; digest is of worktree bytes, blob differs | `input-drift:<path>` |
| two entries for one sha with different inputs | fail-closed: any failing entry denies; credit needs one entry passing class+input gates; instruction wins on class disagreement | failing entry's reason(s); else union of ineligible reasons |
| class dodging (executing bucket labelled `record`) | input gate is class-independent; omitting commands no longer avoids it. Residual: a seat can still label an executed bucket `record` and credit `verified-record` *with* verified inputs — execution cannot be proven from the ledger | `inputs-unrecorded` if no inputs; otherwise accepted residual |
| preamble bucket | first-class section; empty preamble has sha of `""`; same rule applies; page starting with a heading has no preamble; assembler/measure sectionizers must be identical | normal reasons |

## 3. Exact credit-rule wording (normative; replaces C's "input rule" sentence)

> **Cold-read credit (v2).** For each ledger entry `E`, evaluate in order and stop at the first
> failure; `reason(E)` is that failure (or `None`).
>
> 1. **Shape.** `sha256` is 64 lowercase hex; `start` is a JSON integer; `class` is `instruction` or
>    `record`; `verdict` is one of `executed-ok`, `verified-record`, `gap-minor`, `gap-blocking`,
>    `wrong-expectation`, `not-executed`; `blocking_gaps`, `wrong_expectations`, `minor_gaps`,
>    `commands_executed_count` are JSON integers ≥ 0 (booleans and numeric strings are
>    `malformed-entry`); `inputs` is a JSON object (absent or non-object → `inputs-unrecorded`);
>    `external_inputs`, when present, is a JSON object whose values are 64 lowercase hex.
> 2. **Findings (fail-closed).** `verdict` not one of the six strings → `verdict:<v>`;
>    `verdict` in {`gap-blocking`, `wrong-expectation`, `not-executed`} → `verdict:<v>`;
>    `blocking_gaps>0` → `blocking-gaps:<n>`; `wrong_expectations>0` → `wrong-expectations:<n>`.
>    An entry with any of these is **failing** and uncredits its section (step 5).
> 3. **Class gate.** `instruction`: `verdict` in {`executed-ok`, `gap-minor`} and
>    `commands_executed_count ≥ 1` (else `verdict-class:<v>/instruction` or
>    `commands-executed-count:<n>`). `record`: `verdict` in {`verified-record`, `gap-minor`}
>    (else `verdict-class:<v>/record`). Any other class → `class:<c>`.
> 4. **Input gate (class-independent, applies to every credited entry).**
>    `inputs` must contain at least one item (else `inputs-unrecorded`). Every key is a canonical
>    lane-relative path: non-empty, not starting with `/` or `./`, no `..` or `.git` path component,
>    valid UTF-8 without NUL; every value is 64 lowercase hex. A non-canonical key is
>    `input-missing:<key>`. For each key `p`:
>    `git -C ROOT ls-tree -z REV -- <p>` must name exactly one entry with mode `100644` or `100755`;
>    a directory, symlink (`120000`), gitlink (`160000`), deleted-at-REV, renamed-away or
>    untracked-at-REV path is `input-missing:<p>`. Then
>    `sha256(git -C ROOT cat-file blob <REV>:<p>)` must equal the recorded value, else
>    `input-drift:<p>`. Bytes are read with `cat-file blob` only — never the worktree, never
>    `git show` (a tree prints and exits 0). Renames are not followed.
> 5. **Section aggregation (fail-closed; supersedes "any entry credits").** Let `M(σ)` be every
>    ledger entry with `sha256 == σ` for section `S`. If `M(σ)` is empty → `no-ledger-entry`.
>    `S` is covered iff (i) no entry in `M(σ)` is failing, (ii) at least one entry in `M(σ)` has
>    `reason(E) is None`, and (iii) if any entry in `M(σ)` has `class == "instruction"`, the entry
>    satisfying (ii) is instruction-class. A clean entry never launders a failing one. When `S` is
>    uncovered, its `reason` is the deterministic, `;`-joined, lexicographically sorted union of the
>    reasons of every entry in `M(σ)` (failing entries contribute their step-2 reason; other
>    entries their first step-1/3/4 reason).
> 6. **Reported, not credited.** `external_inputs` never gate credit (output reports
>    `external_inputs_count` per entry); `read_rev` is echoed, not trusted by the measure (the
>    assembler binds it, §5 A3).
> 7. **No command exemption.** Entries with `commands_executed_count == 0` are **not** exempt from
>    step 4. This supersedes C's "entries with no executed commands keep v1 rules": the class label
>    is seat-declared, so any class-conditional exemption is a free-credit path (F2).
> 8. **The page is an ordinary input.** `SKILL.md` at the lane root is recorded when a seat opened
>    it and is verified at REV like any other path; a page edit after the trace yields
>    `input-drift:SKILL.md`. No path is exempt.

Rationale for step 5's instruction-wins clause: it is the v1 assembler rule (`assemble.py:390-392`,
`class = "instruction" when seats disagree`) applied at the measure; with per-observation entries it
stops a record-labelled observation from crediting a section another observation calls instruction.

## 4. Measure CLI / output (C text is under-specified; proposed additions)

- Resolve `--rev` once to a 40-hex commit and use the resolved sha for every blob read, `revision`
  output, and the ledger default; also echo `rev_input` (the raw argument). This closes the
  measure.py:648-660 TOCTOU and makes `revision` an identity.
- Default ledger path is `.ufo/evidence/round-17/coldread/ledger.json` at the **resolved** REV.
  Output adds `ledger_source` (`rev`|`file`), `ledger_committed` (true iff the bytes read are
  byte-identical to `cat-file blob REV:<ledger path>`), and `inputs_overlay` (path or null).
- `--ledger-file PATH`: unreadable file → exit 2; readable but not identical to REV's blob →
  `ledger_committed false` (measurement still returns 0). The round's cited count MUST be the one
  with `ledger_committed true` and `inputs_overlay null`.
- `--ledger-rev REV:PATH`: split at the first `:`; `ledger_committed` true iff the ledger rev equals
  the measured rev and the path is the default path with identical bytes.
- `--inputs-overlay FILE`: JSON list of `{start, heading?, skill_sha256, read_rev?, inputs}`;
  each item replaces `inputs` (and `read_rev` when present) of every entry matching
  `(skill_sha256, start)`; an item matching no entry is either exit 2 `overlay-unmatched` or ignored
  with `inputs_overlay_merged` accounting (the built measure ignores; the contract must state which —
  §10); overlay keys are restricted to `inputs`/`external_inputs`/`read_rev` (optionally `heading`)
  so an overlay cannot inject `verdict`/`class`/`sha256`; overlay items are measurement aids only and
  never appear in the cited count. (This folds X07's definition back into C.)
- Exit 2 also for: REV not a commit; any `REQUIRED_BLOBS` path missing at REV (v1 behavior);
  unreadable `--ledger-file`/`--ledger-rev`/overlay. An unparseable ledger stays a measurement result
  (`ledger_error`, `box3_full_page false`, exit 0) as in v1.
- Reasons are order-independent: shuffle the ledger's `entries` and the `missing` list must be
  byte-identical (sort once).

## 5. Assembler invariants (X09); contract C should state these as the trust boundary

- **A1 entry identity.** Emit one entry per observation; merge only observations whose
  `skill_sha256`, `start`, `read_rev` **and** `inputs` are all identical (strictest verdict, class
  instruction if any, summed counts, union `seats`/`reports`). The built assembler already groups on
  `(skill_sha256, start, inputs, external_inputs, read_rev)` (assemble.py:441); the contract should
  state that identity so it is not left to the implementation.
- **A2 count binding.** `commands_executed_count == len(commands_executed)`; a report that disagrees
  is rejected. With A2, "count>0 with an empty list" cannot be assembled.
- **A3 read-rev binding.** `read_rev` is a 40-hex commit in ROOT and
  `sha256(cat-file blob read_rev:SKILL.md) == skill_sha256`; otherwise reject the observation
  (`read_rev_page_mismatch`). This makes `read_rev` a real read point, not a label.
- **A4 trace binding.** For every observation with non-empty `commands_executed`: `traces` is
  non-empty; every receipt resolves at assembly time, has schema `tameshi-trace-inputs-v1` and
  `rev == read_rev`; the observation's `inputs` is a superset of the union of the receipts' `inputs`,
  and digests agree on overlap. A receipt input absent from `inputs` rejects the observation
  (`trace_input_undeclared`). Without A4 the input gate keys only what the seat chose to list (F4).
- **A5 external/lane separation.** An `external_inputs` key that resolves under the lane root is a
  report error (`external_input_lane`).
- **A6 ledger self-input.** Warn (do not reject) when an observation lists the round-17 ledger path;
  it cannot verify at REV by construction (F10).

## 6. Wave ordering required for the 8 claim (C1)

Input-keyed credit is only satisfiable if every path an entry lists is final before the trace and
unchanged at the measured rev. Required order:

1. Land in one commit: the final `SKILL.md` (round-17 text plus repairs), the SHONEN box-3 append
   (round-17 ledger path, unwrapped on one line), `tools/registry.json` and every lane instrument the
   page references (`tools/registry-check.py`, `tools/mutate-and-run.sh`, pin manifests, and the
   round-17 `measure.py`/`trace-inputs.py`/`assemble.py`).
2. Dispatch the full-page re-read at that commit; every seat traces its section commands there and
   records `read_rev` from the trace's `rev`.
3. Assemble the ledger; commit **only** the ledger (and other non-input evidence) as REV, or measure a
   later commit whose page/tool bytes are unchanged.
4. `python3 .ufo/evidence/round-17/measure.py --rev <REV>` (committed ledger, no overlay) — this is the
   cited number. Expected progression: pre-round-17 tip → 0/54 (`inputs-unrecorded`), score 6;
   after wave-2 traces at one final rev → 54/54, score 8.

## 7. Live-lane notice (reported to TameshiR17, not a contract-C finding)

While reviewing, the lane repo's git `HEAD` was found detached at `e16adb7` ("selftest-fixture-noexec";
reflog `e16adb7 <- 0559c60 <- f8832ef` (orphan diff deleting the tree) `<- 98bea7d export from jj`),
`refs/heads/master` intact at 98bea7d, index holding 3 fixture files, real files untracked at that
checkout. Verified: `measure.py --rev HEAD` → `{"error":"blob-missing", …}`; a default
`git clone <lane>` checks out the fixture (though `git checkout <full sha>` still works). This does not
affect the findings above (all use explicit 98bea7d); restore is L1-owned.

## 8. Acceptance deltas for X07/X09 selftests (all synthetic, mkdtemp)

Red-before and rule cases the current spec does not enumerate but the contract requires:
1. duplicate sha: `[clean, gap-blocking]` → **not** covered, in both entry orders;
2. `record/verified-record/0 cmds/inputs{}` → `inputs-unrecorded`, not covered (replaces v1
   `record-credited`, which must now carry one valid input);
3. `record/verified-record/1 cmds/{valid input}` → covered (record stays creditable with evidence);
4. deleted, renamed (content moved), untracked, directory, and symlink inputs → `input-missing`
   (not `input-drift`);
5. dirty-clone input → `input-drift`; clean clone at REV → covered;
6. two entries one sha with different inputs: one drifted + one valid → covered; both drifted →
   uncovered; one failing → uncovered;
7. empty preamble (`sha256(b'')`) requires inputs; page starting with a heading has no preamble;
8. page edited after the trace (`SKILL.md` in `inputs`) → `input-drift:SKILL.md`;
9. reason determinism: shuffled ledger order → identical `missing`;
10. `--rev HEAD` → `revision` is the 40-hex commit; `--ledger-file` on a non-committed ledger →
    `ledger_committed false`; overlay item matching no entry → exit 2;
11. red-before progression required by C: a credited bucket, then an input change at a later rev →
    `input-drift:<path>` and the bucket uncredits.

## 9. Residual risk / not verified

- Counterfactual design checks are [COMPUTED] on the r16 ledger and synthetic repos. measure v2 and
  assemble v2 landed during review; §10 re-checks every finding against the built artifacts, where
  F1/F2/F3/F8 reproduce and A4/A5 are missing. The §3 text is the acceptance target.
- Trace completeness is evidence, not proof: `strace -f` misses reads made via paths outside the
  traced process tree (hardlinks opened from `/tmp`, memfd, io_uring submissions are only partially
  visible), and `/tmp` is recorded nowhere. A4 narrows under-declaration but cannot prove it absent.
- The class label remains a seat claim. The unified input gate forces a verified input, not execution;
  a seat can still label an executed bucket `record` and credit `verified-record` with one verified
  lane file. This is the honest limit of a ledger-only rule and should be stated in the round's
  residual-unknown list.
- No `.gitattributes` exists today; a future `text`/smudge attribute would make clean worktree bytes
  differ from `cat-file blob` bytes and mass-produce `input-drift`. The rule text pins blob bytes;
  keep attributes out of the lane.

## 10. Addendum — the v2 artifacts landed during review; status of each finding

`.ufo/evidence/round-17/measure.py` (sha256 `f654d5b660c27632e121d8959c58d0d23b2d2f5ce29db0e5e0eda45dda829997`,
matches X07's report) and `.ufo/evidence/round-17/coldread/assemble.py` were written while this review
ran. Re-checked against them:

| finding | status in the built artifacts |
|---|---|
| F1 duplicate-sha laundering | **present**: `coldread()` still `covered = True; break`s on the first credited entry (measure.py:336-345); the F1 demonstration applies unchanged |
| F2 class-dodge exemption | **present**: `entry_input_reason()` returns `None` when `commands_executed_count<=0` (measure.py:243-260) and is only consulted after the v1 credit rule passes; the X07 selftest even encodes it as `record-zero-cmd-credited` |
| F3 missing-vs-drift | **present**: `blob()` is `git show <rev>:<path>` (measure.py:108-114); no `ls-tree` mode check, so a directory or symlink input reports `input-drift` instead of `input-missing` |
| F8 counting honesty | **present**: `main()` resolves the commit but reads blobs with `args.rev` and echoes it (measure.py:904-952); `--ledger-file` has no committed-bytes check |
| overlay footgun (new) | `new_entry.update(index[key])` (measure.py:314-327) lets an overlay replace **any** entry field — including `verdict`, `class`, `sha256` — and silently ignores unmatched items. A measurement-aid overlay must be key-whitelisted to `inputs`/`external_inputs`/`read_rev` (and optionally `heading`), with `inputs_overlay_merged` reported (it is); otherwise `--inputs-overlay` is a verdict-injection channel. My §4 "exit 2 on unmatched" is a preference, not a requirement — the builder's ignore-and-count is acceptable once the whitelist exists; the contract text must state which |
| red-before number | **reproduced by X07** independently: `--rev 98bea7d --ledger-rev 98bea7d:…round-16/coldread/ledger.json` → 0/54, `{"inputs-unrecorded": 54}`, `box3_full_page false`, score 6 — identical to §0's [COMPUTED] figure |
| A1 entry identity | **implemented, stricter than proposed**: assembler groups on `(skill_sha256, start, inputs, external_inputs, read_rev)` (assemble.py:441), so F5's merged-`read_rev` ambiguity is already closed |
| A2 count binding | **implemented**: ledger count is `sum(len(o["commands_executed"]))` (assemble.py:558) |
| A3 read-rev binding | **implemented**: `read_rev` must be 40-hex and resolvable, and the page is resolved at `read_rev` with a `page-sha-mismatch` rejection (assemble.py:351-353, 451-470) |
| A4 trace binding | **absent**: `traces` is validated only as a string list (assemble.py:383-386) and unioned into the entry (564-571); no receipt is opened, no `rev == read_rev` check, no superset check against `inputs`. F4's under-declaration hole stands |
| A5 external/lane separation | **absent**: `external_inputs` values are 64-hex-validated (assemble.py:389-391) but keys are not rejected for resolving under the lane root |

Consequence for the L1: F1, F2, F3 and F8 survive into the counting tool the round will run. F2 and F3
can be closed in measure.py without changing the v2 report/ledger schema (class-independent gate; read
inputs with `cat-file blob` + `ls-tree`); F1 needs the §3 step-5 aggregation; F4/A4 and A5 are
assembler-side and can still be added this wave (reports already carry `traces` and
`external_inputs`). The red-before evidence is already sound and reproducible.

Verdict: falls (as written; the §3/§5 text is the repair that makes C1's "input-keyed credit" true).
