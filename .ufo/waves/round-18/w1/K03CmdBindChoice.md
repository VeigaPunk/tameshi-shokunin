# K03CmdBindChoice — critic, R17-CMD-BIND decision

Seat: TameshiR18.K03CmdBindChoice (critic, read-only). Lane tip inspected:
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. All bytes read via
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <rev>:<path>`;
no lane writes, no git writes, no tools installed.

## 1. Is preserving the narrower claim honest and sufficient?

**Yes — it is one of the two options the closure itself offered, provided the
correction half is actually landed.** §7 item 2 of
`corpus/lessons/round-17-verifier-spotcheck.md:423-427` is a disjunction:

> correct the assertion that K02 holes1–4 are all closed; either bind trace
> argv to the declared/required commands with failure-backed coverage, **or
> explicitly preserve the narrower input-keyed evidence claim**. G7's
> hole5→hole7 pointer and G5's dated89 versus final94 tally also need a named
> correction, not historical evidence rewrites.

The verifier's own wording at `:329-332` fixes the residual precisely: "K02's
command-binding requirement is not fully closed … It forbids calling the
verifier a complete command-coverage proof." It does **not** require the
binding be built; it forbids the broader description. So the L1's choice is
sanctioned — it is not a dodge — **if and only if** the wave lands all three
named corrections (G5 breadth, G7 pointer, 89→94 tally) as appended text, not
just the "never describe as command coverage" criterion. The dispatch assigns
exactly those pieces (lesson correction block, wording-defect verification,
QUALITY.md criterion, staged knowledge-entry erratum); the assignment set
covers the item, but the item is closed only when the appended corrections
exist at the tip — a criterion alone does not satisfy "correct the assertion".

### Code state the narrower claim must survive (verified)

`git show 183f87b8:.ufo/evidence/round-17/measure.py`:

- `trace_reason` (`measure.py:368-424`) validates receipt schema
  `tameshi-trace-inputs-v1`, superset coverage of receipt `inputs`, and
  `live_lane_reads`/`external` binding. It **never reads `receipt['argv']`** —
  `argv` appears in the file only at `:773` (selftest fixture) and `:1462`
  (`main(argv)`). Receipts do record argv
  (`.ufo/evidence/round-17/coldread/traces/CR01/1.json` →
  `argv: ["bash","-c","git -C /tmp/…/tameshi-shokunin show eb7838b…:SKILL.md | sha256sum"]`).
- No required-command check exists: no `commands-unbound` reason, and
  `.ufo/evidence/round-17/coldread/bucket-commands.json` (schema
  `tameshi-bucket-commands-v1`, present at tip) is never opened by measure.py.
- `commands_executed_count` is self-reported; ledger entries carry `traces`
  and `reports` lists but **no argv/command list** (ledger.json entry keys:
  `commands_executed_count` only).
- Strict mode requires only ≥1 receipt when count>0
  (`measure.py:377-381`), not a receipt per command and never an argv match.

So the live dodge is narrower but real: an entry may claim `count=1`, attach
one receipt of an unrelated `bash -c true`, declare any verifying non-empty
`inputs`, and still credit the bucket. The knowledge entry already discloses
this (`input-keyed-coldread-credit.md:67`: "A seat can still skip a command;
the rule makes a recorded read checkable, not complete.") — the preserved
claim is honest *because* that sentence exists; keep it verbatim in the
staged file.

Hole accounting at tip (for the correction text): hole 2 closed
(`commands-unrecorded`, `measure.py:516-517` + `record-zero-cmd` selftest);
hole 3 closed (`OVERLAY_FIELDS` whitelist `:134-135`,
`overlay-field-forbidden` selftest `:1351-1359`); hole 4 closed
(`cat_file_blob`/`BLOB_MODES` in `input_reason` and `trace_reason`);
hole 1 **partly closed** — the inputs↔traces superset half yes, the
argv/commands half no. G7's reasoning is K02 **hole 7** (over-invalidation by
the page), not hole 5 (live-lane reads) — spot-check `round-17.md:24` vs
`K02InputCreditHoles.md` holes table.

## 2. Wording that would still overclaim

Any of these in the appended correction, the criterion, SCORECARD, LOG, the
report, or the staged knowledge entry falsifies the fix:

1. "K02 holes 1–4 (are) closed" or "all four input-credit holes closed" —
   must name hole 1's command-binding half as open.
2. "trace binding" unqualified (the G5 candidate text itself,
   `round-17.md:22`) — must read "trace-input binding" or "committed trace
   receipts whose recorded inputs are covered".
3. "commands are traced" / "executed commands have receipts" — false: ≥1
   receipt suffices for any count (`measure.py:377-381`), and no receipt
   needs argv-match.
4. "command coverage", "command-coverage proof", "proves the section's
   commands were run", "58/58 verifies the commands an agent ought to run" —
   the exact phrasing the spot-check forbids.
5. Presenting `commands_executed_count` as verified evidence — it is
   self-reported; only *some* traced command's inputs are bound.
6. In the correction block: claiming hole 1 closed "via
   `commands-unrecorded`" — that case closes hole 2's zero-command dodge,
   not the unrelated-trace dodge.
7. Tally restatement: `89/89` was the earlier W2 count; the final instrument
   records `94/94` (spot-check `:306`, `:312-313`). The correction must name
   both as versioned receipts, per the item's wording.
8. `round-17.md:24`'s "K02 hole 5" pointer — correct to hole 7 (the file is
   append-only, so the fix is a named appended correction, not an edit).

## 3. Cheap partial binding — should ride along

Two near-free additions exist inside work already contracted; neither moves
the claimed predicate:

**P1 (recommended, display-only, zero credit risk):** contract F's new
`measure.py --explain` already prints per-bucket credit reasons. Add a
non-crediting `argv_coverage` line per entry: join each listed trace
receipt's `argv` against the bucket's `bucket-commands.json` extraction at
REV and report covered/uncovered counts. It changes no reason and cannot
regress 58/58. Caveat verified against real bytes: receipt argv embeds
clone-absolute paths and `bash -c` wrappers (CR01/1.json above), while
bucket-commands holds recipe text — matching must be a substring/normalized
rule and labelled approximate, or P1 reports only "traced argv present vs
none" honestly.

**P2 (stronger, still cheap):** contract F already creates report schema
`tameshi-coldread-report-v2`. Have `assemble.py` record each entry's
`commands` argv list (it currently records only the count), then add one
credit reason `trace-argv-unrecorded` in measure.py: every declared trace
receipt's argv must appear in the entry's `commands`. That kills the
unrelated-trace dodge — half of hole 1 — with one selftest mutant (receipt
argv ∉ commands → uncredited). Carry-over entries (`carried_from`, no
`commands` list) must stay under the old rule via an explicit rule-version
or field-absence distinction, or the carried ledger silently uncredits.
If that dual-rule handling is judged fiddly this wave, land P1 alone and
name P2 as the residual.

What NOT to add: the full `commands-unbound` required-command gate is the
deferred disjunct — it needs per-bucket extraction coverage and its own
failure-backed mutants; shoehorning it into this wave without mutants
replicates the round-17 selftest-survivor defect (item 3) in a new file.

## 4. Findings

| # | Finding | Severity |
|---|---|---|
| F1 | The decision itself is sanctioned by §7 item 2's disjunction; not an overclaim. | holds |
| F2 | Closure is conditional: all three named corrections (G5 breadth, G7 hole5→hole7, 89→94) must land as appended text; criterion-only leaves item 2 open. | condition |
| F3 | Eight specific wordings (§2) would re-overclaim; the staged/erratum text must keep `input-keyed-coldread-credit.md:67`'s disclosure. | guard |
| F4 | P1 (`--explain` argv/bucket-commands coverage, non-crediting) and P2 (v2 report `commands` field + `trace-argv-unrecorded` for new entries) are cheap partial bindings available inside contracted work; P2 needs explicit carried-entry grandfathering. | recommendation |

Verdict: **holds with conditions** — the preserve-narrower-claim choice is honest and sufficient per §7 item 2 only if all three named corrections land appended (not criterion-only) and no §2 wording ships; ride along P1, and P2 if carried-entry grandfathering is made explicit.
