# CritC3Arithmetic — arithmetic-map admission under tools/staged-id-guard.py

Seat: L1Tameshi43.CritC3Arithmetic (wave 2, falsify). Judged axis: operability.
Revs measured: guard tool is byte-identical `2e8f2e89…` at the ticket freeze
`3aee2c0` and the A12 freeze `bb36f80` (absent at base `487b8f0` — good).
Staged package (read-only): `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`,
sha256 `020fbeaa…`, 103 rows. Registry at freeze: `corpus/SOURCES.md`, 114 rows,
sha `c50ca1fb…`. All map runs used the tool extracted from `3aee2c0` in scratch;
the live package was never written.

## Item answers

**Q1 — pure arithmetic map (every collision → a fresh id ≥ safe floor S256, zero dedupe
entries): REFUSED, and the reason is the document, not the id.**

Live run: `map {S153→S256, S154→S257, S155→S258, S156→S259, S157→S260, S158→S261,
S159→S262}` → exit 1, `verdict=inadmissible`, `map_held_moved=[S153,S154,S159]`,
three reasons, all of the form `map moves a held document off its registry id:
S153 -> S256 (registry S105)`. Every arithmetic gate passed: injective, targets
absent from registry and staged, all ≥ floor, all collisions covered, no self-map.
The other four colliding rows (S155 arxiv/2302.09330, S156 arxiv/2406.09843,
S157 doi/10.21105, S158 mir.cs.illinois) carry documents no registry row holds —
they are the *only* rows a pure map may renumber freely, and that decision is
document-driven. So a pure arithmetic map is **not admissible on the live
package** and cannot be made so by arithmetic alone.

**Q2 — arithmetic map respecting held rows (dedupe): ADMITTED.**

`map {S153→S105, S154→S106, S159→S155, S155→S256, S156→S257, S157→S258,
S158→S259}` → exit 0, `verdict=admitted`, `map_dedupe={S153:S105,S154:S106,
S159:S155}`. This is field-for-field the counter's `safe_map`, and the counter
reproduces `safe_map_admitted=1` (`C3_R43_PASS=true` at bb36f80).

**Q3 — the discrimination is the document, not the id.** Same map shape, same
targets, same floor: the only difference between refused and admitted is whether
a collision's document normalises onto a registry row (`tools/staged-id-guard.py:196`,
`held` join; refused at `:241-249` via `map_held_moved`/`map_undocumented`). The
id rules bound *where* a fresh row may land; the document decides *whether* it
may land at all — the claim's own "by document … never arithmetic" wording at
`staged-id-guard.py:9-10,30-34` says the same.

## Findings

**F1 — "document" is a 4-rewrite citation *string*, and the blind spot is
live-populated.** `normalise_document` (`tools/staged-id-guard.py:115-120`)
folds only scheme / `www.` / case / trailing slash — no fragment, no query.
Counterexample (scratch, live registry + the live 103-row package with the
three held citations respelled to `#top`, `?ref=lane`, `/#intro`: same
documents, different form): `held={}` and the pure arithmetic map above is
**ADMITTED** (rc=0) — three documents the registry already holds are re-appended
under fresh ids. That is exactly the round-42 hazard the guard exists to answer.
The live registry already carries the same file under two ids that differ only
by fragment: S097 and S104 both cite
`cgit…/plain/doc/bashref.texi?id=b8c60bc9…`, S104 adding `#L494-L495`; a staged
row citing the bare file is `admitted` under S256 while the same file held by
S104's exact spelling is `held`. So the guard can already see two ids for one
document and will mint a third.
*Smallest correction:* strip the fragment in `normalise_document` and mirror it
in the counter's `norm_url` (`guard/measure.py:47-52`). Do **not** strip the
query — S090's `?query=sysexits&sektion=3` is load-bearing — so the query-forms
miss (e.g. `?ref=lane`) remains; document it. Add a fragment-held selftest case.
Fixable defect: it only adds refusals; no predicate field loosens.

**F2 — `next_free` names an occupied id on the live package.** Live JSON:
`next_free=S160` while staged ids S160–S255 exist — `next_free` is computed from
the registry top only (`staged-id-guard.py:168`) and is printed unqualified at
`:479`; the number that is actually free is `safe_floor=S256` (`:171`). An
operator appending the field that literally means "next free id" would collide.
The field is not in the docstring's description of the interface and no consumer
reads it, so renaming to `next_free_in_registry` (or emitting the safe floor) is
safe. Fixable label defect.

**F3 — non-canonical id spellings alias the number space.** `id_number` accepts
`S\d{3,}` (`:123-127`); the floor check is numeric (`:230`) but identity is
textual. On the live package a single map containing both `S256` and `S0256` is
**admitted** (rc=0) → two fresh rows numbered 256. And a staged row spelled
`S0256` against a registry holding `S256` reports `collisions=[]` and
`verdict=answered` — the hazard is silent. The live registry has no
non-canonical ids (114 checked), so it is latent.
*Smallest correction:* in `validate_map` refuse any target whose
`'S%03d' % id_number(target) != target` (map keys are constrained by the staged
set already).

**F4 — a held document on the *same* id has no representable map.** When the
staged row's document is held at its own id, `held[S001]=S001` forces
`S001→S001`, which the selfmap guard refuses (`:243-245`); the empty map is
refused for non-coverage. The no-map analysis still answers correctly
(`held={S001:S001}`, `verdict=answered`), so the operator is told "adopt
nothing" but cannot record that decision through `--map`. No live instance
(held pairs are S153→S105, S154→S106, S159→S155). Low severity; smallest
correction: exempt `held[sid]==sid` from the selfmap reason.

**F5 — the predicate never exercises the whole-set pure map, and `held_refused`
is green-by-default.** The counter's new field (`guard/measure.py:261-271`)
initialises `held_refused = 1` and only probes when `own_held` is non-empty, and
only moves the *first* held row (`+50` above floor). Measured on the respelled
package: `held_refused=1` printed alongside `live_held=0` — a green field from a
probe that never ran (the same defect shape A11 fixed in the C1 counter). On the
live package it is genuinely exercised. Also, no predicate field runs the exact
item shape — all seven collisions to fresh above-floor ids with no dedupe
entries; Q1's refusal is measured here, not pinned.
*Smallest correction:* initialise `held_refused = 0` (PASS already requires
`map_dedupe_live=1` → `own_held` non-empty, so this cannot widen the target);
optionally add a whole-set pure-map field.

**F6 — stale interface text after A10 (one line).** The docstring
(`staged-id-guard.py:30-34`) still advertises "at or above the safe floor
*unless the map covers the whole staged set*" — the exemption A10 removed; the
code applies `staged_clash`/`below_floor` unconditionally (`:222-232`).
Docstring fix only.

**F7 — provenance note (one line, outside my item).** `contract.json
frozen_before` still narrates `114ffacd` as the freeze of record, but A10–A12
are pinned at `bb36f80`: the counter reports `self_pin=1` only at `bb36f80`
(measured `self_pin=0` at `3aee2c0` with the A12 pin). The deciding run must
pass `--freeze bb36f80` (or later), not the freeze named in my ticket.

## Reproduction (all at rev 3aee2c0 or bb36f80 — tool bytes identical)

```sh
git show 3aee2c0:tools/staged-id-guard.py > /tmp/g.py
git show 3aee2c0:corpus/SOURCES.md      > /tmp/reg.md
# Q1 pure arithmetic map → inadmissible, 3 document reasons, 0 arithmetic reasons
echo '{"map":{"S153":"S256","S154":"S257","S155":"S258","S156":"S259","S157":"S260","S158":"S261","S159":"S262"}}' > /tmp/pure.json
python3 -I /tmp/g.py --registry /tmp/reg.md --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json --map /tmp/pure.json   # exit 1
# Q2 dedupe map → admitted
echo '{"map":{"S153":"S105","S154":"S106","S159":"S155","S155":"S256","S156":"S257","S157":"S258","S158":"S259"}}' > /tmp/mixed.json
python3 -I /tmp/g.py --registry /tmp/reg.md --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json --map /tmp/mixed.json  # exit 0
# F1: respell the three held citations (#top / ?ref=lane / /#intro) then rerun pure.json → admitted, held={}
# F3: add "S156":"S0256" alongside "S155":"S256" in mixed.json → admitted (two rows numbered 256)
# counter receipts: measure.py --rev bb36f80 --freeze bb36f80 → C3_R43_PASS=true, held_refused=1;
# same with --staged <respelled copy> → held_refused=1 live_held=0 map_dedupe_live=0 PASS=false
```

Bottom line for the canonical judge: the frozen C3 sentence holds at the freeze
—the guard admits only the by-document map and refuses the pure arithmetic one —
but its discrimination is a normalized citation *string*, not document identity
(F1, live-populated: S097/S104), and `next_free` names an occupied id (F2). F1
is the strongest counterexample to the capability the axis is scored on;
F3–F6 are narrow, fixable edges. No finding changes the predicate or target.
