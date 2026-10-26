# T49RevGuardExit — analysis-mode exit semantics of `tools/staged-id-guard.py`

Hypothesis to falsify: in analysis mode (no `--map`) the guard exits 1 whenever its JSON
`refused` is true (unmapped or cascade non-empty), although the module docstring names
exit 1 only for an inadmissible map.

**Result: hypothesis confirmed, not falsified.** All three named cases behave exactly so,
plus a held (dedupe) case that confirms the converse. The docstring exit paragraph is
map-centric and under-specifies analysis mode; the code is self-consistent with the
docstring's own `--json` verdict vocabulary.

## Docstring lines (the mismatch)

`tools/staged-id-guard.py:38-41`:

> Exit 0 = the question was answered and, with `--map`, the map is admissible;
> exit 1 = the map is not admissible; exit 2 = setup refusal (missing or
> non-regular file, oversized file, malformed row, malformed map) — never a bare
> traceback.

Exit 1 is named only for an inadmissible map. But the same docstring's `--json` vocabulary,
`tools/staged-id-guard.py:53-55`, already lists mode-aware verdicts
`("refused"|"answered"|"admitted"|"inadmissible"|"setup_refusal")` and says that without
`--map` the object carries the no-map analysis. So the docstring contradicts itself only
between its exit paragraph and its verdict list; the implementation follows the latter.

## Code path (pinned bytes)

- `tools/staged-id-guard.py:157` — `refused = bool(unmapped) or bool(cascade)`
- `tools/staged-id-guard.py:473` — no-map branch: `result['verdict'] = 'refused' if result['refused'] else 'answered'`
- `tools/staged-id-guard.py:491-493` — `if result['verdict'] in ('admitted', 'answered'): return 0` then `return 1`
  ⇒ every analysis `refused` verdict is exit 1.

Show with: `sed -n '157p;473p;491,493p' tools/staged-id-guard.py` (from the lane root).

Probes ran on the pinned capability bytes: `sha256sum tools/staged-id-guard.py` →
`03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`, equal to the contract's
`claims.C2.named_gate` hash, and `git log --oneline 8ca6742111..HEAD -- tools/staged-id-guard.py`
is empty (0 commits since base). Tool health: `python3 -I tools/staged-id-guard.py --selftest`
→ exit 0.

## Probes (scratch `/fast/scratch/hyaku/tameshi-r49/T49RevGuardExit/w`, cleaned up)

Registry in all cases: `S001 https://a.test/alpha`, `S002 https://b.test/beta`.
Command per case (absolute guard path, `-I`):

```
python3 -I tools/staged-id-guard.py --registry R.md --staged G_<case>.md --json; echo exit=$?
```

| case | staged rows | collisions | unmapped | cascade | held | refused | verdict | exit |
|---|---|---|---|---|---|---|---|---|
| cascade-only | S002 gamma URL + S003 delta URL | `[S002]` | `[]` | `["S003"]` | `{}` | `true` | `"refused"` | **1** |
| unmapped-only | S002 "prose without doc" (no URL/DOI, no path-like head) | `[S002]` | `["S002"]` | `[]` | `{}` | `true` | `"refused"` | **1** |
| neither | S002 gamma URL only | `[S002]` | `[]` | `[]` | `{}` | `false` | `"answered"` | **0** |
| held (extra) | S002 `HTTPS://B.test/beta/` (form-insensitive dedupe) | `[S002]` | `[]` | `[]` | `{"S002":"S002"}` | `false` | `"answered"` | **0** |

Observed JSON (verdict field quoted; full lines were emitted by the commands above):

- cascade-only: `"cascade": ["S003"], "unmapped": [], "refused": true, "verdict": "refused"`, `exit=1`
- unmapped-only: `"cascade": [], "unmapped": ["S002"], "refused": true, "verdict": "refused"`, `exit=1`
- neither: `"cascade": [], "unmapped": [], "refused": false, "verdict": "answered"`, `exit=0`
- held: `"held": {"S002": "S002"}, "refused": false, "verdict": "answered"`, `exit=0`

The naive-map mechanism is what produces the cascade case: `analyse()` maps every collision
to `max(registry)+1, +2, …` (`tools/staged-id-guard.py:149-156`), so with S003 also staged the
naive target is not free and `refused` fires even though every colliding row has a document.

## Contract cross-check

`.ufo/evidence/round-49/contract.json` `claims.C2.guard_exit_semantics_observed` already
records exactly these semantics — "0 answered/admitted; 1 analysis refused (unmapped or
cascade non-empty) or map inadmissible; 2 setup refusal" — and names the docstring gap "a
documentation mismatch recorded for the lesson, not edited (the guard is a pinned
capability)". This seat's probes independently reproduce that record at the pinned bytes;
nothing in the contract needed correcting.

## Should the generator oracle treat exit 1 in analysis mode as correct?

**Yes — conditionally: exit 1 in analysis mode is correct iff the guard's own JSON says
`verdict == "refused"` (`refused == true`, i.e. `unmapped` or `cascade` non-empty), and exit 0
iff `verdict == "answered"`.** Grounds:

1. The guard is the pinned named gate (hash match above, never edited); its real exit
   contract is verdict-driven (`:491-493`), and the docstring's own verdict list (`:53-55`)
   includes `"refused"`/`"answered"` for the no-map object. The only oracle consistent with
   both code and docstring-vocabulary is verdict-mirroring.
2. The 12 frozen classes (`claims.C2.classes`) include `unmapped`, `cascade` and `held` with
   `class_min: 10`. An oracle built on the narrow docstring reading ("exit 1 = map not
   admissible") would flag the pristine guard on nearly every `unmapped`/`cascade` case, stop
   at the first violation, and falsely fail C2 against an unmutated gate. The frozen
   `guard_exit_semantics_observed` field is the authoritative statement; the oracle must
   match it, not the exit paragraph.
3. Corollaries the oracle should keep (all now observed, not just read):
   - `held` (dedupe) does **not** refuse: refused stays `false` because `:157` only counts
     unmapped/cascade — exit 0, verdict `"answered"`. An oracle demanding exit 1 for any
     collision would also misjudge the `held` class.
   - exit 2 ⇔ `verdict == "setup_refusal"`; exit 1 with verdict `"answered"` or exit 0 with
     verdict `"refused"` on the pristine guard is a genuine violation (a real mutant signal).

Residual risk / verification gaps:

- `--map` mode exits (`admitted`/`inadmissible`) were read from `:466-473`/`:491-493` but not
  exercised here — the map branch is outside this item's three named cases and is covered by
  the contract's WITNESS control and the `map`/`map_inadmissible` classes.
- Line numbers cite tip bytes `6db4b93`; the guard is pinned at the contract hash, so they
  are stable unless the capability is ever edited.

No tools were installed or upgraded for this seat (none needed).

## Summary

- Hypothesis confirmed: analysis mode exits 1 iff JSON `refused` is true (cascade-only → exit 1 `"refused"`; unmapped-only → exit 1 `"refused"`; neither → exit 0 `"answered"`).
- Docstring `:38-41` names exit 1 only for an inadmissible map, but its `:53-55` verdict list includes `"refused"`/`"answered"` — the code follows the latter (`:157`, `:473`, `:491-493`).
- Probes ran on the pinned capability (sha256 `03a796c5…` = contract `named_gate`; 0 commits since base); selftest exit 0.
- Held/dedupe case observed: `refused=false`, exit 0 — collisions alone never refuse.
- Oracle recommendation: treat exit 1 in analysis mode as correct iff `verdict=="refused"` (unmapped or cascade non-empty); exit 0 iff `"answered"`; exit 2 iff `"setup_refusal"`.
- An oracle following the narrow docstring reading would false-fail the pristine gate on the frozen `unmapped`/`cascade`/`held` classes.
- Matches `contract.json claims.C2.guard_exit_semantics_observed` verbatim; no contract correction needed.
- Gaps: `--map` exits read from source only (map classes covered elsewhere); report file is the only lane write.
