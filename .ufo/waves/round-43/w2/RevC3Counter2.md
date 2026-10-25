# RevC3Counter2 — C3 counter independence after A9 (A14-head)

Seat: reviewer (C3 operability). Lane: tameshi-shokunin.
Item: re-review `.ufo/evidence/round-43/guard/measure.py` after A9 — five questions.

Operative bytes:
- Counter: `.ufo/evidence/round-43/guard/measure.py` at HEAD `6b83a11`, sha256
  `47a6afce1547037487c0dcc54c0e4653269fa628fa9c0df6ed5bc1d3cb67d2c2` = `contract.json`
  `claims.C3.counter_sha256` (frozen at `6b83a11`, A14). The file also matches
  `3aee2c0` (A10): C3 counter bytes were untouched by A11–A14.
- Tool: `tools/staged-id-guard.py` at HEAD, sha256
  `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` = frozen_tools pin (A14).
- Staged input: `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` (read-only; 103 rows, 7 collisions S153–S159).
- Registry: `git show 6b83a11:corpus/SOURCES.md` (114 rows).

Method: running counter at `--rev/--freeze 6b83a11` inside a scratch `git clone --shared`
(`/tmp/tameshi-r43-w2-RevC3Counter2/clone`) — out-of-lane, read-only, no lane writes. Permitted
rev pair (base 487b8f0 / freeze 3aee2c0) also run: base C3 `PASS=false` (`tool_absent=1`),
freeze-A10 `PASS=true` at `3aee2c0` (line record below). A substitute tool is scored via the
counter's own `--tool-file`; the substitute = the frozen tool blob plus one site mutation and a
neutered selftest (the mutated tool's *own* tests removed, so only the counter's live fields can
fire). No installs; no campaign tool. Sibling seats: `RevC3Tool2.md` (tool-side findings) and
`MutC3Held.md` (held-move mutant) — this report is the counter side, cross-referenced.

Baseline (deciding configuration, A14):
`C3_R43_PASS=true`: self_pin=1 tool_sha_ok=1 selftest_cases=24 failed=0 staged_rows=103
live_collisions_agree=1 live_held_agree=1 live_unmapped=0 live_verdict=refused live_cascade=1
naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 held_refused=1 naive_agree=1
substitute=0, exit 0.

---

## 1. Naive-map check after A9 — independent, and now the *only* two live checks that are actually independent (LOW residual)

`measure.py:236-242`: `own_naive = {sid: 'S%03d' % (top_reg + index) for index, sid in
enumerate(own_collisions, 1)}`; `naive_agree = 1 if doc.get('naive_map') == own_naive else 0`.
Counter recomputes the map from its own `own_parse` (same census row regex, same registry bytes —
registry is snapshot-copied into `<work>/SOURCES.md` once, `measure.py:184-187`). Mutant
`naive[sid] = S(top+index+1)` (a14_naive) → `naive_agree=0`, `naive_map_refused=0`, all other
live fields green. This is the one check where the counter would catch a fabricated value even
with the selftest gutted. Genuine fix, holds at A14.

## 2. Fabricated cascade — `live_cascade` is membership-only; it cannot tell the cascade from the naive map (MEDIUM)

`measure.py:231-233`:

```python
cascade = doc.get('cascade') or []
live_cascade = 1 if cascade and all(sid in staged_ids for sid in cascade) else 0
```

This asserts non-empty and "every entry is a staged id". It never recomputes the expected
`{naive_map values} ∩ staged` set, so any staged id not in the map *also* passes, and the whole
fabrication is untied from the naive map. Scenario: substitute tool sets `cascade = ['S255']`
(S255 is a staged id, but not a naive target — naive targets are S160–S166). Counter prints
`live_cascade=1 naive_agree=1 live_verdict=refused`, i.e. every live field green; the sole
blockers of PASS are the A9 substitute gate (see 3) and the tool pin. A tool whose selftest
still covers the cascade (T3) is killed by that *self-report*; a falsifier that drops the case
with the behaviour (as in the MutC3Held double-mutant pattern) passes all live fields. The
docstring claim "`live_cascade=1` — that naive map's targets are all ids another staged row
still holds" is not what the code checks; the code checks membership only. Cheap fix: `own_cascade
= sorted({t for t in own_naive.values() if t in staged_ids})` and compare `doc['cascade'] ==
own_cascade`, exactly the pattern A9 used for the naive map.

## 3. `substitute=1` — yes, it really stops a PASS; but it also makes the counter's live fields unobservable via the PASS bit (MEDIUM)

`measure.py:202-208,270-272,279,313`: `--tool-file` sets `substitute=1` and the substitute
bytes are written to `<work>/tools/staged-id-guard.py`; `passed` includes `substitute == 0`.
All three mutated tools (cascade/naive/unmapped with selftest neutered) print `C3_R43_PASS=false`
with every measurement field green — the *only* conjunct blocked is `substitute==0`. So the
substitute gate is not behavioural coverage: it proves which bytes ran, not that the capability
is present (same point as MutC3Held's closing paragraph). Consequence for falsifier seats: with
`--tool-file`, the PASS bit carries no information; only individual fields do. The counter as a
*predicate* therefore cannot falsify any single live clause (cascade, unmapped, held, verdict)
using its own instrument; it can only never-PASS substitutes. Note also `tool_sha_ok` is
computed from the REV blob, not from the substituted bytes (`measure.py:192-194`), so a receipt
for a substitute run can print `tool_sha_ok=1` side-by-side with `substitute=1` — disclosed in
the same line, but as a pair they say "the pinned tool is the right bytes, and the bytes that ran
are not it".

## 4. `own_document` vs the tool's rule — identical at A10, divergent at A14 (MEDIUM)

At A10 both were copy-identical (verified: 0 divergences across 20 synthetic cell batteries +
114 registry rows + 103 staged rows). A14 changed the tool's `openable` rule to reject spaced
filename extensions (`tools/staged-id-guard.py:111-112`): `' ' not in head and` was added. The
counter's `own_document` (`measure.py:104-112`) was not updated — it still accepts any
`\.[A-Za-z0-9]{2,6}$` head, spaced or not. Differential on A14 bytes:
`'A paper on the topic.PDF — t'` → counter `'a paper on the topic.pdf'`, tool `''`
(documented vs undocumented); `'see the appendix.md — t'` → same divergence. On the frozen live
inputs this cannot fire (all 103 staged rows carry URLs; divergence class is prose/path-head
only), so the failure is latent: the counter's `live_held_agree`/`live_unmapped` are compared
against a *different rule* than the one the tool implements. Because the counter is broader, the
tool is stricter, the failure is fail-closed (a row the tool treats as undocumented is seen as
held by the counter → mismatch → PASS false), i.e. it costs operability, not falsification
soundness; but the two are no longer "the same rule", and a future round with a spaced-filename
row would false-fail a correct tool.

## 5. `staged_sha256` — the bytes actually read, three times, never compared (MEDIUM, open)

The tool now hashes raw bytes (`tools/staged-id-guard.py:480-481` `hashlib.sha256(read_bytes(...))`)
and the CRLF divergence of the A10 text-mode digest is fixed (verified: CRLF copy's tool digest
now equals `sha256sum`). But there are still three independent reads of the staged file, in
order: tool `read_text` (guard run 1, plus map runs 2-3), counter `own_parse(read(args.staged))`
(`measure.py:214`), counter digest `sha(read_bytes(args.staged))` (`measure.py:315`). The printed
digest is a *fourth* read (run 1's tool read, runs 2-3's map reads, `own_parse`, digest all
separate `open`s), and nothing compares it to the tool's JSON `staged_sha256` — the counter never
reads `doc['staged_sha256']` (grep: the only `staged_sha256` in measure.py is line 315). Proof
of the disconnect: the probe copy of the counter (env-flag appends a comment line to the staged
file *after* the guard runs, before the digest) prints `staged_sha256=07f6a707…` = sha of the
post-append bytes — while the guard's own `staged_sha256` (computed before the append) is
`020fbeaa…`. If the file changed between the tool's read and the digest, the receipt's digest
would not be the bytes judged, and nothing would notice. Also, interesting: with the probe
flag, `live_collisions_agree` stayed 1 (the appended line is not a row) — so an attacker
holding append access could even swap the staged *rows* between the tool read and `own_parse`
and the counter would compare two different snapshots; that direction fails closed (mismatch)
only if the swap changes the extraction. Fix: read the staged file once into a work copy (like
the registry), run the guard on the copy, hash the copy, and compare with the tool's reported
`staged_sha256`.

---

## Summary table

| Question | Verdict | Evidence |
|---|---|---|
| naive-map check independent | Yes (A9 fix holds at A14) | `measure.py:236-242`; mutant naive_agree=0 |
| fabricated cascade can pass | Yes, at field level; PASS bit blocked only by `substitute` | `measure.py:231-233`; a14_cascade all-green |
| substitute=1 stops PASS | Yes — but it masks every live clause | `measure.py:279`; 3 mutants all PASS=false |
| own_document == tool rule | Yes at A10, no at A14 (spaced ext heads) | `measure.py:104-112` vs `staged-id-guard.py:111-112` |
| staged_sha256 = bytes read twice | No — three+ reads, never compared | `measure.py:315`; probe digest 07f6a707 ≠ tool 020fbeaa |

## Residual risk

- L1 (falsification): the counter could be pointed at a self-consistent frozen commit whose
  contract pins a broken tool (self_pin only proves counter == contract). The deciding run fixes
  the freeze, so this is a governance guard, not a code defect.
- L2: `live_unmapped` is read verbatim from `doc['unmapped']` with no counter-side expectation
  (`measure.py:229`); the frozen staged data has 0 undocumented rows, so the "refuses a colliding
  row with no document" clause is exercised live nowhere — only by the tool's own selftest
  (T2/T8). Same vacuity class as the cascade finding. (Sibling RevC3Tool2 residual 2 makes the
  equivalent tool-side point.)
- Verification gaps: no `lsp` device is mounted in this seat; all findings are the counter's own
  executed behaviour and cited source lines. The TOCTOU on the staged path (5) is demonstrated
  by construction (an inserted hook), not by a race.

## Checks that hold (attacked, not broken)

- A10 freeze `3aee2c0` counter run: `PASS=true`, same fields as A14 baseline.
- Base `487b8f0`: `tool_absent=1`, exit 1 (control direction confirmed).
- `--control` stub: `stub_collisions_agree=0`, CONTROL_PASS=false (exit 1).
- `held_refused` (A12) fires on a moved held row (S153→S306, floor S256 → verdict inadmissible,
  exit 1).
- Safe-map admission and `map_dedupe_live` agree with the counter's `own_held` on live data.
