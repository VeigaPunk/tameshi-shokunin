# CodeSupersession — registry.json supersession semantics, round-24 W1

**Verdict: the supersession mechanics are correct and the failing superseded row is honestly observable; the disclosure of that failure is incomplete in the committed corpus, and the new `new-r24` rows leave two new gaps that the round-24 lesson does not name. Three findings, no blocking defect in the registry schema or in `registry-check.py` semantics.**

**Method / bounds.** Read-only inspection only. No command was executed inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin`: the registry battery, the frozen ruler and both selftests were **not** run (my item carries no "Run" token). Facts are taken from committed artefacts (`.ufo/evidence/round-24/noharm-c8c5b88.json`, `before.json`, `after.json`), from `git show`/`diff`/`cat-file` (read-only, `GIT_OPTIONAL_LOCKS=0`), and from two **static simulations** that import the production `tools/registry-check.py` module and call only `load_registry` / `registry_errors` — no row was executed. No tool was installed or upgraded (nothing beyond stock `python3` was needed). No producer authentication, promotion, historical R17-CMD-BIND closure or numeric score uplift is claimed.

---

## 1. What changed (verified)

`git diff 6a1821a8897eea6e7d9669292160ec9593669409 c8c5b88c8e961a929cdc351b95a7074c76958909 -- tools/registry.json` → **+46 −3, 50 rows → 54 rows**. Programmatic row-level diff (base vs head, keyed by `name`):

- **No row removed.** 4 rows added, 3 rows changed.
- **Changed (3):** only `status` (`active` → `superseded`) and a new `superseded_by`. `argv`, `expect`, `timeout_s`, `tags`, `source`, `kind` are byte-identical.
  - `command-binding-selftest` → `command-binding-selftest-r24` (`tools/registry.json:928-937`)
  - `command-binding-frozen-clean` → `command-binding-frozen-clean-pinned` (`:939-948`)
  - `command-binding-source-read-red` → `command-binding-source-read-red-pinned` (`:950-959`)
- **Added (4):** `command-binding-selftest-r24` (`:961-969`), `command-binding-frozen-clean-pinned` (`:971-979`), `command-binding-source-read-red-pinned` (`:981-989`), `registry-replay-selftest` (`:991-999`). All four are `status: "active"`, tagged `new-r24`.

`tools/registry-check.py` is **unchanged** in this wave (`git diff --stat base..head -- tools/registry-check.py` is empty; last touched at `496d212`). The three round-23 fixtures under `.ufo/evidence/round-23/` are also unchanged, and the pinned bundle bytes are identical at base and head:

```
git show 6a1821a…:.ufo/evidence/round-23/replay/bundle.json | sha256sum
  3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9
sha256sum .ufo/evidence/round-23/replay/bundle.json
  3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9
git show 6a1821a…:.ufo/evidence/round-23/source-read-bundle.json | sha256sum
  db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf
```

The two `bundle_sha256` literals in the new pinned rows (`:974`, `:984`) are exactly those two digests, so the pins are honest.

**Schema validity.** `registry_errors()` (the production validator, `tools/registry-check.py:190-299`) on the head registry returns **`[]`** — no schema violation. In particular the second pass (`:277-298`) confirms each `superseded_by` names an existing **active** row; all three targets are among the four new active rows.

---

## 2. registry-check.py semantics — verified correct for the question asked

**Q: do superseded rows still run, and do they count toward `held`?**

Both halves verified against the production code and against the retained receipt.

*Still run.* `evaluate()` builds fragments for **every** selected row with no status filter: `fragments = [run_row(row, root, fleet_root) for row in selected]` (`tools/registry-check.py:872`). The documented contract says the same (`tools/registry-check.py:30-35`: "every active row and every superseded row RUNS … Superseded rows still execute so their observed outcome stays visible"). The successor rows carry `superseded_by` into the fragment (`:660-661`).

*Do not count to held.* Counting is done over the **active** fragments only:

```
tools/registry-check.py:874-884
874  active = [f for f in fragments if f["status"] == "active"]
877  superseded = [f for f in fragments if f["status"] == "superseded"]
880  held = sum(1 for f in active if f["held"])
882  report["total"] = len(active)
883  report["superseded"] = len(superseded)
884  return (0 if held == len(active) else 1), report
```

So a superseded row's `held` is computed but excluded from the numerator, from the denominator, and from the exit code. `print_human` (`:894-900`) prints superseded rows on a separate line form (`ROW <name> superseded expect=… got=…`) with no `held|differs` token, and the trailer (`:905-908`) is `REGISTRY_CHECK: held=<N>/<M> superseded=<K>` where `M` counts active rows only.

**Observed at the delivered revision** (`.ufo/evidence/round-24/noharm-c8c5b88.json`, `registry` entry: `exit 0`):

```
held 47  total 47  superseded 7   registry_sha256 a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f
```

Per-row fragments for the seven affected rows (same file, `registry.stdout.rows`):

| row | status | expect | got | held | note |
|---|---|---|---|---|---|
| `command-binding-selftest` | superseded | 0 | 0 | **false** | `stdout_missing: ["COMMAND_BINDING_SELFTEST: 38/38 pass"]`; tail shows `44/44 pass` |
| `command-binding-frozen-clean` | superseded | 0 | 0 | true | — |
| `command-binding-source-read-red` | superseded | 1 | 1 | true | — |
| `command-binding-selftest-r24` | active | 0 | 0 | true | tail `44/44 pass` |
| `command-binding-frozen-clean-pinned` | active | 0 | 0 | true | `bundle_sha256 3d6c99b7…` |
| `command-binding-source-read-red-pinned` | active | 1 | 1 | true | `bundle_sha256 db620668…` |
| `registry-replay-selftest` | active | 0 | 0 | true | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` |

**Conclusion: the semantics are exactly as the knowledge entry claims** ("The runner still executes superseded rows; they do not count toward `held`", `corpus/knowledge/replay-projection-hardening.md:23-26`). The pre-existing precedent rows behave identically (`evidence-disposition-round14-superseded` has been visibly `got=2` since round 17 — `.ufo/waves/round-17/w2/ReviewRegistryCheckCode.md:60-68`), so this wave introduces no new semantics.

---

## 3. The superseded 38/38 row now failing — honest in mechanism, under-disclosed in prose

**The failure is real and the mechanism is honest.** The `command-binding-selftest` row's `expect.stdout_contains` is still the literal `COMMAND_BINDING_SELFTEST: 38/38 pass` (`tools/registry.json:931`), but the tool now prints `44/44` because the loader was widened to read both fixture files (`tools/command-binding.py:166-169`). The case arithmetic closes exactly: 1 base case + 16 inline `changed(...)` cases + 19 round-23 fixture cases + 6 round-24 fixture cases + 2 harness cases (`tampered`, `duplicate-json-key`) = **44**; the base tree has no round-24 fixture file, so it was 17 + 19 + 2 = **38** — matching the recorded `before.json` tails (`COMMAND_BINDING_SELFTEST: 38/38 pass`) and the round-23 critic's note that the token "moves with the fixture count" (`.ufo/waves/round-23/w2/ArgvExact.md:27`).

The row's failure is **observable, not hidden**: the JSON fragment carries `held: false` plus `stdout_missing: ["COMMAND_BINDING_SELFTEST: 38/38 pass"]`, and the run still exits 0 because the row is superseded. The design is therefore honest *in the machine-readable channel* and *in the exit code*.

**F1 (medium, calibration/disclosure) — no committed artifact states that the superseded round-23 selftest row now differs.** The committed corpus at `c8c5b88` never says so:

- `corpus/lessons/round-24.md` (committed) — no occurrence of `38/38` outside the base-measurement sentence; the "no-harm" line only reports `registry 47/47 held, 7 superseded, exit 0` (working-tree `corpus/lessons/round-24.md:76`).
- `corpus/knowledge/replay-projection-hardening.md:23-26` — describes the supersession *mechanism* but asserts nothing about the stale expectation.
- `SKILL.md:2054-2057` — "Registry rows `command-binding-selftest-r24` (44/44) … supersede the three round23 rows append-only." No mention that the predecessor's own `38/38` needle is now permanently false.
- `corpus/knowledge/required-command-binding.md:71` still reads "public selftest38/38" without a round-24 qualifier.

The only place the fact appears is a **wave-1 seat report**, `.ufo/waves/round-24/w1/ClosureCarry.md:50-53` ("The superseded `command-binding-selftest` row now holds false (it expects 38/38; the tool prints 44/44) … the designed append-only supersession") and `.ufo/waves/round-24/w1/CodeAnchors.md:188-194`. The round-24 lesson's own errata list (E–O, `corpus/lessons/round-24.md:86-201`) does **not** carry it, and the lesson's Errata I ("routed accounting") does not mention it either.

Why this matters for calibration, concretely: the round-23 `38/38` claim is the *frozen* number in `before.json` and in the `required-command-binding.md` knowledge entry, and the delivered tool's number is 44. A reader of the committed corpus who has not read the wave-1 seat files can believe the registry still exercises a "38-case selftest" and that the round-23 row still holds. The same trap the round-17 reviewer recorded for `evidence-disposition-round14-superseded` ("the registry records an expectation that is unenforced and currently false", `.ufo/waves/round-17/w2/ReviewRegistryCheckCode.md:66-68`) is now reproduced for a **round-24** row and is not named as an erratum.

**Smallest safe correction (additive, no tool/fixture/ruler bytes change):** add one sentence to the round-24 lesson's errata and one clause to the knowledge entry, e.g.:

> Erratum P — the superseded `command-binding-selftest` row expects `38/38` and the delivered tool prints `44/44` (the round-24 fixture file adds six cases). The row is `status: superseded`, so it is excluded from `held`/`total` and from the exit code, and its `stdout_missing` is retained in the JSON report. The superseded expectation is unenforced and currently false by design.

and in the knowledge entry, after "they do not count toward `held`": "A superseded row whose expectation the current tool no longer satisfies still runs and is reported with `held: false` and `stdout_missing`; it cannot affect the verdict. Round-24's `command-binding-selftest` is one such row (`38/38` expected, `44/44` printed)."

**F2 (low, calibration) — the `new-r23` tag is now a superseded-only selection, and a superseded-only selection exits 0 with an empty denominator.** Tag inventory, base → head:

```
BASE: ('new-r23','active')=3
HEAD: ('new-r23','superseded')=3 , ('new-r24','active')=4
```

`new-r23` is the **only** tag in the registry that selects zero active rows. Static simulation through the production `load_registry` + the production selection code (`:850-871`) gives:

```
--tag new-r23 : selected=3 active=0 superseded=3 → total=0 → exit 0, trailer "REGISTRY_CHECK: held=N/0 superseded=3"
--tag new-r24 : selected=4 active=4 superseded=0 → total=4
--only command-binding-selftest : exit 0, trailer "held=0/0 superseded=1"
```

This is the round-17 **F5** defect (`.ufo/waves/round-17/w2/ReviewRegistryCheckCode.md:69-70`: "any future selection with no active rows is indistinguishable from a fully passing one by exit code. … Suggest exit 2 when `total == 0`") still unimplemented — there is no `total == 0` guard in `tools/registry-check.py` today. It is pre-existing, not introduced here, and no script in the repo invokes `--tag new-r23` (grep across the tree finds the tag only in `tools/registry.json` and the retained receipt), so nothing currently depends on it. It becomes reachable-by-construction for the first time: the tag now names a set with no active member, so a future `--tag new-r23` gate would report `held=0/0 superseded=3` and exit 0 — a green that verifies nothing.

**Smallest safe correction:** either (a) note in the lesson that `new-r23` is now a superseded-only tag and that `--tag` selections with zero active rows exit 0 (a live instance of round-17 F5), or (b) route F5 to round 25 (it is already a known-but-unimplemented item — confirm it is in the routed table). **Not** a round-24 code change: the frozen tool is the correct object of a future round's change, and altering `registry-check.py` after the only falsification wave would invalidate the before/after pair (the lesson's own rule, `corpus/lessons/round-24.md:80-84`).

---

## 4. Two gaps in the new rows that the wave-1 seats did not name

**F3 (medium, calibration) — `command-binding-selftest-r24`'s `source` anchor points at a passage that supports a different number and marks it unexecuted.** The row (`tools/registry.json:961-969`) cites `.ufo/waves/round-23/fresh-adjudication.json@6a1821a…:53-59`. At that rev those lines are the *routed defect* statements:

> `:53` "A name-insensitive argv mutant (receipt argv in any requirement argv) is outside the ten-anchor sweep and would survive **all 38 selftest cases** **[seat inference, not executed]**. Needs a swapped-name supplemental case plus that mutant."
> `:59` "An unexecuted negative-exit guard-weakening candidate. Its expected survival is a seat inference, not a measured survivor."

The row's own expectation is `COMMAND_BINDING_SELFTEST: 44/44 pass`. The cited authority states 38 and explicitly marks the number as an unexecuted seat inference. The two pinned rows are fine — `:66` is exactly the `bundle_sha256` defect their added expectation answers. This is the anchor-vs-expectation mismatch the wave-1 seat `CodeFixtureLoader.md:111-127` (M4) raised; it is a real finding but it is recorded only in a seat file, not in the lesson's Errata J (documentation), which lists four documentation items and not this one.

Related and also unrecorded in the lesson: the `44/44` literal is a **moving count**, exactly the fragility the round-23 critic named (`.ufo/waves/round-23/w2/ArgvExact.md:27` — "Update the selftest pass count … since it moves with the fixture count"). The round-24 fix is correct for now (44 = the delivered count), but the successor row will need the same treatment in round 25 whenever a new fixture file is added — that is the intended append-only pattern, and it should be stated as such rather than left implicit.

**F4 (low) — the `registry-replay-selftest` row is not named in `SKILL.md` or in the corpus registry prose.** `SKILL.md:2054-2057` lists three of the four new rows; `registry-replay-selftest` (`tools/registry.json:991-999`) is absent from `SKILL.md` and from `corpus/knowledge/*.md` and `corpus/README.md` (grep: "NOT MENTIONED"). It is the only row that keeps the *new* tool under continuous registry supervision, so the omission means the new capability is registered but not documented in the operator-facing registry section. The wave-1 seat `CorpusErrataCarry.md` and `CorpusSkill.md` touch the surrounding prose, and `corpus/lessons/round-24.md:137-146` (Erratum J) already lists "SKILL.md names only the round23 fixture file and omits the `registry-replay-selftest` row" — so this one **is** disclosed in the working-tree lesson, though the same Erratum J list does not mention the round-24 fixture file being unnamed in `SKILL.md:2019` either. Confirmed: `grep -n "round-24/extra-cases" SKILL.md` → no match, while `SKILL.md:2019` still says "public fixtures include `.ufo/evidence/round-23/extra-cases.json`" as the tool's complete fixture set. That is Erratum J's first bullet, so it is disclosed; I list it here only to confirm the finding and that the fix is a one-line `SKILL.md:2019` edit, not a tool change.

---

## 5. Checks performed that found nothing (stated for calibration)

- **Registry schema:** `registry_errors()` returns `[]` for the head registry. No duplicate names, no invalid `superseded_by` target, no invalid `source`/timeout/kind/expect.
- **No row was removed**, so the round-23 rows remain individually re-runnable and the append-only rule in the knowledge entry (`:23`) and in `SKILL.md:1829` ("A row leaves `active` only as `superseded` with `superseded_by`, and still runs") is respected.
- **The three superseded rows' `argv`/`expect` are byte-identical to base** — the supersession added the pin strength only in the successors, as the knowledge entry's "a new active row carries the stronger expectation" claims.
- **The pinned digests are honest**: both literals equal the actual SHA-256 of the committed bundles, at base and at head.
- **The two new gate rows really are red/green for the right reason** (from the retained receipt): `command-binding-frozen-clean-pinned` → `exit 0, finding_ids []`; `command-binding-source-read-red-pinned` → `exit 1, finding_ids ["ARGV_MISMATCH"]`; `registry-replay-selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`.
- **Cost of the append-only duplication is negligible**: the three superseded round-23 command-binding rows cost 2.31 s of the 193.46 s total battery time (1.2 %), per `noharm-c8c5b88.json`.
- **The `new-r24` tag is healthy**: 4 selected, 4 active, 0 superseded — the denominator is never empty for it.

---

## 6. Residual risk and verification gaps

1. **No row was executed by me.** The `held`/`got`/`stdout_missing` values above are read from `.ufo/evidence/round-24/noharm-c8c5b88.json` (retained receipt at `c8c5b88`, `registry` entry `exit 0`), not re-measured. The `held=47/47` claim rests on that receipt; I re-derived the *selection and counting* semantics from the production code, not the execution.
2. **`registry-check.py` semantics are read, not fuzzed.** I did not construct an adversarial registry (e.g. a superseded row whose `superseded_by` chains two deep, or a `--only` on a superseded row with a non-zero exit) against the production binary. The chain-depth case is statically blocked: `registry_errors` requires the target to be `active` (`:295-298`), so a superseded→superseded edge is a schema error — the round-17 selftest already covers it (`registry-check.py:1362-1373`).
3. **The `--tag new-r23` vacuity (F2) is derived statically**, from `evaluate()`'s selection and counting code plus the row inventory; I did not execute `registry-check.py --tag new-r23`. The arithmetic (`held=N/0 superseded=3`, exit 0) follows directly from `:857-884`, and the same shape is empirically recorded in the wave-1 seat receipt `.ufo/waves/round-24/w1/MutPins.md:151-156` (`--only command-binding-frozen-clean` → exit 0, `REGISTRY_CHECK: held=0/0 superseded=1`).
4. **No registry row pins the round-24 replay bundle.** `.ufo/evidence/round-24/replay/bundle.json` (sha256 `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`) is referenced by **no** registry row (`grep` over `tools/registry.json` → no row names `round-24/replay`); only `.ufo/evidence/round-23/replay/bundle.json` is pinned. This is already recorded in the working-tree lesson as Erratum L (`:156-159`, "No registry row pins the round24 replay bundle"), routed to round 25 — I confirm it, and it is out of this item's lane to repair.
5. **The `after.json` receipt landed after this revision.** `.ufo/evidence/round-24/after.json` is **not** in `c8c5b88` (`git cat-file -e c8c5b88:.ufo/evidence/round-24/after.json` → exit 128) and landed in `04657a6`. The delivered revision `c8c5b88` therefore does not itself contain the 11/11 after-receipt; the round-24 lesson's "After measurement" section (working tree) discloses this. Not a defect of the supersession; recorded so the 11/11 claim is not read as a property of `c8c5b88`'s tree.
6. **Not claimed:** producer authentication, promotion, historical R17-CMD-BIND closure, numeric score uplift, or that the two `bundle_sha256` pins authenticate the bundle's producer. The pins prove byte identity of the committed bundle only — the knowledge entry's own bound ("A bundle digest pin … is not producer authentication") holds.
