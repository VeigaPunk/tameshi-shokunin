# T50Disp42 — C1 disposer, round-42 verifier spot-check (R42.1–R42.4)

Seat: T50Disp42. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, read-only; tree read at
base `e3729de862f73ae080d98fcf522a7081ce16e40a`. All four routed items of
`corpus/lessons/round-42-verifier-spotcheck.md` (routed at `487b8f0da89fa0e2b8bea6930068accbf36e70a9`,
frozen in `.ufo/evidence/round-50/c1/defects.json`) were read in full in the spot-check under
`## 6. Routed defects / notes for the lane` (lines 102–116) and judged against the tree. Rows:
`.ufo/waves/round-50/w1/T50Disp42.rows.json` (`{"round": 42, "rows": [...]}`). No open items, so no
`fix_plan` rows.

## R42.1 — C2 survivors — status: fixed

**Ask.** `outflag_no_parse_args_check` and `method_fold_several_returns` survived the round-42 mutant
set; the lane must either add fixtures/judgment (the method-fold mutant "differs only on dead code")
or adjust the declared mutant set with reasons, and keep the miss visible until the gate is met
(`corpus/lessons/round-42-verifier-spotcheck.md:104-108`). The miss was real at routing:
`.ufo/evidence/round-42/after/c2-at-242c1b4a.stdout:4` (`MUTANT method_fold_several_returns class=method outcome=survived`),
`:6` (`MUTANT outflag_no_parse_args_check class=outflag outcome=survived`), last line
`mutants_killed=4 … C2_R42_PASS=false`.

**What exists now.** Both asks are met in `.ufo/evidence/round-43/mutants/measure.py`, added whole by
`697d2f17568d900fb0bfbe063c6292090781cbfe` (`git -C <lane> diff-tree --no-commit-id --name-status -r
--root 697d2f17568d900fb0bfbe063c6292090781cbfe -- .ufo/evidence/round-43/mutants/measure.py` → `A`):

- the frozen K/D/E/U rule at `:11-20` — `K` kill on reachable code, `D` `dead_code_only` when every
  differing case has a statement after an unconditional `return`/`raise`;
- the F11 kill fixture at `:209-228` (`SimpleNamespace(out='golden')` is not a `parse_args`
  namespace, so the destination is not operator-named) and the F12 dead-code discriminator at
  `:231-248` (second top-level `return` unreachable); declarations at `:250-253`;
- kill binding at `:614-615` — the mutant is killed only if its failing fixture is exactly
  `F11_outflag_namespace`, "not asserted from F11's source text".

The predicate is written and met: `.ufo/evidence/round-43/after/c1-at-3c4003f6.stdout:1` →
`fixtures_pass=12/12 … mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 not_killed=0
runtime_error=0 apply_error=0 unresolved=0 … kill_binding=1 mutants_sha_ok=1 … C1_R43_PASS=true`
(the round-42 declaration blob is unchanged: `mutants_sha_ok=1`). The miss stayed visible rather than
being re-adjudicated: `.ufo/evidence/round-43/mutants/measure.py:4-7` states the round-42 predicate
`C2_R42_PASS` "stays false and is not re-adjudicated", and the round-42 receipt above still records
the survivors. The round-43 record names the same fix (`corpus/lessons/round-43.md:126`,
`frozen-rule-without-code` → contract amendment A5) and the SCORECARD round-43 block quotes the
receipt (`SCORECARD.md:2089-2093`).

**Status: fixed**, commit `697d2f17568d900fb0bfbe063c6292090781cbfe` (post-routing, ancestor of
base). Evidence: `.ufo/evidence/round-43/mutants/measure.py:37-41` and `:209-211` (keyed excerpts
absent at `routed_at`, where the path does not exist:
`git -C <lane> cat-file -e 487b8f0d:.ufo/evidence/round-43/mutants/measure.py` → "exists on disk, but
not in '487b8f0d…'").

## R42.2 — m10/m8 blind spots — status: declined

**Ask.** The item is a disclosure: "m10 is content-blind and reads only boolean `present` … m8 relies
on line-scoped backtick extraction … (verified). The deletion/rewrite counterexamples V1–V6 remain
unfixed by design (append-only repair route). **No action required this round.**" Its own heading
reads "(disclosed, optional to repair)" (`corpus/lessons/round-42-verifier-spotcheck.md:109-113`).

**What exists now.** The disclosure is in the tree twice: `corpus/lessons/round-42.md:176-178`
("m10 is content-blind. A superseding receipt clears a stale claim for any path that resolves,
including an empty file, an unrelated stub or a directory"), `:200-203` (the two surviving m10 and two
m8 mutants, each with the fixture that would kill it), `:190` (the V1–V6 scratch-clone variants), and
`SCORECARD.md:2014-2016` ("Instrument limits, disclosed rather than repaired after data"). The
successor counter carried m10 forward with one refinement only — superseded receipts treated as
history, `.ufo/evidence/round-43/calibration/measure.py:22-25` — and stayed presence-based, so the
blind spot is an unrepaired instrument limit by design, not a missing tree artefact.

**Status: declined** — an observation whose repair the spot-check explicitly marks optional; the
V1–V6 variants are harms to closed-round evidence handled by the lane's append-only repair route
(`corpus/lessons/round-42.md:191-192`), not defects the tree lacks. No text in the tree is missing.

## R42.3 — staged-collision hazard — status: declined

**Ask.** "The staged set collides with six lane rows (S153–S158); recorded in `corpus/SOURCES.md` as
the next round's hazard. **No action required this round.**"
(`corpus/lessons/round-42-verifier-spotcheck.md:114-115`).

**What exists now.** The hazard record is in `corpus/SOURCES.md:473` verbatim ("Round 42 post-append
hazard (for the next assimilation round): after this round's append the staged id set collides with
six lane rows — `S153` … `S158` … Renumber by document in scratch before appending"), and it was
already present at routing (`git -C <lane> log -S'Round 42 post-append hazard'
487b8f0d..e3729de8 -- corpus/SOURCES.md` → no commit, i.e. added at or before `routed_at`). The next
rounds handled it read-only and by document: `corpus/SOURCES.md:476` (guard reports the same six
collisions, safe floor S256, no staged row adopted in round 43) and `:481` (round-44 recheck, eight
overlaps), with the by-document adoption realising it in round 45 (`:484`).

**Status: declined** — the routed content is a recorded hazard with an explicit no-action ruling; the
note is not a defect and no lane edit is owed to it.

## R42.4 — SHONEN box promotion — status: declined

**Ask.** "No SHONEN box moved; all `[~]` — promotion remains operator-owned (noted for the
operator)" (`corpus/lessons/round-42-verifier-spotcheck.md:116`).

**What exists now.** `SHONEN.md:5-12` still carries four `[~]` boxes, each annotated "lane
assertion, no independent promotion verifier"; `corpus/lessons/round-42.md:146-153` tabulates which
boxes a non-author can check and states "One box out of four is mechanically checkable today. No box
moves this round." The remaining calibration points are explicitly reserved to independent promotion
review (`SCORECARD.md:67`: "the remaining 2 require independent promotion review of all boxes").

**Status: declined** — an operator/closure-owned item; the lane cannot promote its own boxes, so it is
not lane-repairable.

## Self-check (probe, never a verdict)

Scratch clone `git clone -q --shared <lane> /fast/scratch/hyaku/tameshi-r50/T50Disp42/lane`
(`git -C … rev-parse --show-toplevel` → the clone; `HEAD` was `4afb060c…`), only my four rows
written to `corpus/routed-defects.json` (`{"defects": [...]}`), committed as
`58cefde11f6a6aaed5b8ba0901330e1e4d22abef` with scratch identity
(`user.name=seat-T50Disp42`):

```
TMPDIR=$S python3 <lane>/.ufo/evidence/round-50/c1/measure.py --lane "$S/lane" --rev HEAD --explain
C1_R50: self=ceee320c9ad8 rev=58cefde11f6a6aaed5b8ba0901330e1e4d22abef defects=49 rows=4 fixed=1
open=0 declined=3 fixed_this_round=0 missing=45 extra=0 duplicate=0 spotcheck_changed=0
defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0
fixed_short=19 declined_over=0 this_round_short=5 total=69 C1_R50_PASS=false
```

exit 1. Full output: `.ufo/waves/round-50/w1/T50Disp42.explain.stdout` (46 lines).

- **No EXPLAIN line names R42.1–R42.4** — all four rows passed evidence resolution, key matching,
  the fixed commit/freshness/acknowledgement gates and the declined-reason length gate
  (`evidence_bad=0 key_miss=0 fixed_bad=0 declined_bad=0 bad_status=0 duplicate=0 extra=0
  spotcheck_changed=0 defects_pin=0`).
- `missing=45` (45 × `EXPLAIN missing R4x.y`) is every item of the other nine spot-checks, expected
  for a scratch tree carrying only one round's rows.
- `fixed_short=19` (floor 20) and `this_round_short=5` (floor 5) are the lane-level floors; they are
  unmet here by construction — my rows cite a round-43 fix, so `fixed_this_round=0` — and are other
  seats'/the L1's to supply. `total=69 C1_R50_PASS=false` at this scratch revision is the expected
  probe result, not a claim verdict.

## Limits and out-of-scope

- I did not re-run the round-43 C1 counter (`.ufo/evidence/round-43/mutants/measure.py`); R42.1's
  fixed status rests on its committed receipt bytes
  (`.ufo/evidence/round-43/after/c1-at-3c4003f6.stdout:1`) and on the fixture/rule text read at base.
- Evidence avoids `SCORECARD.md` so that the L1's round-50 edits cannot shift cited line numbers; the
  four cited paths are append-only or frozen (round-42 lesson, `corpus/SOURCES.md` tail, `SHONEN.md`,
  round-43 counter).
- Not done, per seat bounds: no lane edit, no `git add/commit` in the lane, no model call, no reading
  of `/home/vgpnk/.local/state/`, no mutant names from `control/c2-*.stdout`.
- Tooling: nothing installed (no pacman, uv, npm; pacman transactions are paused host-wide).
- Scratch `/fast/scratch/hyaku/tameshi-r50/T50Disp42` deleted after copying the receipts above.

## Summary

- R42.1 **fixed** by `697d2f17`: F11 fixture kills `outflag_no_parse_args_check` (kill binding in the
  counter), F12 + the frozen K/D/E/U rule classifies `method_fold_several_returns` dead-code-only;
  `C1_R43_PASS=true` at `3c4003f6`, round-42 declaration unchanged and its `C2_R42_PASS=false` kept
  visible.
- R42.2 **declined**: disclosure-only item, repair explicitly optional; disclosure lives at
  `corpus/lessons/round-42.md:176-178,200-203` and `SCORECARD.md:2014-2016`; successor counter
  carried m10 without making it content-aware.
- R42.3 **declined**: recorded hazard (`corpus/SOURCES.md:473`), no action required; later rounds
  answered it by document under the staged-id guard (`:476`, `:481`, `:484`).
- R42.4 **declined**: SHONEN promotion is independent-review/operator-owned (`SHONEN.md:5-12`,
  `SCORECARD.md:67`); the lane cannot move its own boxes.
- Scratch counter probe: four rows clean, 45 expected `missing` for other rounds, floors unmet at a
  4-row tree; receipt at `.ufo/waves/round-50/w1/T50Disp42.explain.stdout`.
