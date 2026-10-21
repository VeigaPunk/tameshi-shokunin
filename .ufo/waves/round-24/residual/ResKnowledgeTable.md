# ResKnowledgeTable — round24 residual critic

Target: `corpus/knowledge/replay-projection-hardening.md` at lane tip `4903959`. This covers the section "Errata — round24 fresh wave 1" (lines 42–61) and the "Routed-defect disposition" table (lines 63–76). They are checked against `git show 6a1821a:.ufo/waves/round-23/fresh-adjudication.json` lines 48–106, `tools/registry-replay.py` and `.ufo/evidence/round-24/measure.py`.

## Verdict

**Coverage is complete; the text overclaims.** The routed list has eight defects, and each has a row in the table. No routed defect is missing.

Four dispositions are accurate as written: the bundle pins, the stream row, the loose tokens and the runner digest's clone-copy half. The argv, negative-exit and realpath rows are accurate only as predicate pointers.

Two places overclaim:

- **The errata intro.** It says "The table above overstates four rows". At least one more row is overstated: the live-dependent row, line 19. The section also lists surviving weakenings only for the argv, stdout and sibling rows.
- **Disposition row 4 (line 70).** It overstates what K10 and the projection carry.

Three smaller inaccuracies also apply. The instrument_sha256 half of routed defect 5 is not mentioned. The table is not framed as successor-tool capability, as the lesson, QUALITY48 and SCORECARD frame it. The "seven mechanisms" count does not match the grouping the lesson states.

## Routed defects mapped (fresh-adjudication.json lines 48–106)

| # | Routed defect (line) | Knowledge row | Accurate? |
|---|---|---|---|
| 1 | ArgvExact name-insensitive mutant (53) | K1 predicate | yes (`measure.py:28-29`; round24 `extra-cases.json` `argv-swapped-between-names`; before K1 false, after true) |
| 2 | MutationDesign negative-exit (59) | K3 predicate | yes for the frozen `>= 0` mutant (`measure.py:32-33`); sibling survivors omitted, see F2 |
| 3 | bundle_sha256 pins on two rows (66) | K5/K6 | yes. `registry.json` diff 6a1821a..4903959 supersedes three r23 rows and adds `-pinned` rows with literals `3d6c99b7…` and `db620668…`; before K5/K6 false, after true |
| 4 | projection drops held, cleanup_ok, external, non_hermetic_argv; no live marker (74) | "carried … K7/K8/K10" | **partly; overclaims**, see F1 and F3 |
| 5 | runner_sha256 **and instrument_sha256** hash the live tree (81) | "implemented (clone copy hashed)" | runner half yes; instrument half not addressed in text, see F4 |
| 6 | sibling identity by string, fleet root not realpath'd (87) | K11 | yes, with the errata sibling caveat (lines 59–61) |
| 7 | streams unbounded, no redaction (93) | "size half only, publication-only (K9); redaction open" | yes: `registry-replay.py:181-184` writes `observations.json` before `project()` |
| 8 | loose stdout tokens (97–104) | "left frozen … open" | yes: the registry diff touches only the three command-binding rows |

My own check for row 5: `git show d2eaecd:tools/registry-check.py | sha256sum` gives `cba16646…944ad`. That equals `observations.json` `runner_sha256_clone_copy`, and `registry-replay.py:162-166` hashes and imports the same clone path.

## Findings

### F1 (medium, overclaim): the live-dependent row and disposition row 4 claim K10 coverage that K10 does not have

**Counterexample.** Delete either disjunct at `tools/registry-replay.py:99`: `if row.get('external') is True or result.get('non_hermetic_argv')`. Frozen K10 stays discriminated, because its only fixture sets **both** flags. That fixture is `measure.py:181`: `obs(external=True, non_hermetic_argv=['/live/root'])`.

Seat evidence:

- MutProject ran this mutation as M05 and M06 (`w1/MutProject.md:115-116,127`). The result was frozen K10 `T`; the public selftest failed at 9/10.
- On the real observations, dropping the `external` disjunct un-lists `verify-round15` (external, no `non_hermetic_argv`) while K10 still passes (`w1/CodeLiveList.md:170-187`; `w1/PredK10.md:9`).

**Where the knowledge text overclaims:**

- Main table line 19 says the rule "Fails when the list omits such a row". That is false for a row that has only one of the two flags. The errata intro (line 44) says only four rows are overstated, and line 19 is not among them.
- Disposition line 70 maps external carriage to "K10 predicate". QUALITY49 (`corpus/QUALITY.md:513-524`) says a one-fixture, all-triggers predicate "counts once, for the conjunction only". Its own falsifier is exactly this K10 mutant. The lesson also records it (`corpus/lessons/round-24.md:107-108`).
- Line 92 ("Each of K7–K11 uses one fixture shape") is generic. It does not withdraw line 19 or line 70.

**Additional fact from the code.** With the real runner, the `non_hermetic_argv` disjunct cannot change a published bundle's live list:

- `tools/registry-check.py:663-670`: a non-external row with a live-fleet argv token returns `held=False`, and `project()` refuses it (RUNNER_NOT_HELD).
- `tools/registry-check.py:671`: an external row keeps `non_hermetic_argv` and runs.

So in every published bundle, a row that carries `non_hermetic_argv` is already `external`. Only `--project` on hand-written observations can exercise that disjunct alone.

### F2 (low–medium, omission that reads as coverage): survivors are listed for some rows only

The errata lists surviving weakenings for argv (`argv[0]` case-fold, per-token prefix), stdout (last-token, case-insensitive, stripped) and sibling (unresolved symlinked sibling). It is silent on survivors that the lesson's Erratum F (`round-24.md:92-112`) records for the remaining predicates:

- **K3, exit comparison.** `abs()` and truthiness both survive the 44-case selftest. Example: required exit 1, receipt -1 is accepted (`w1/MutFixtures.md:44-46,546-552`; `w1/PredK3.md` W2/W3).
- **K9, byte counting.** Counting characters instead of bytes survives both the selftest and K9 (`w1/MutProject.md:114,123`, M04). The stream bullet (lines 55–58) states "It does count UTF-8 bytes" as a strength. That is true of the current code, but no detector would catch a regression.
  - It counts the bytes of re-encoded text that the runner already decoded with `errors="replace"` (`registry-check.py:717,726`), not raw process bytes. Each invalid input byte becomes U+FFFD and counts as 3 bytes.
- **K7 and K8.** `held is False` and first-row-only checks survive, and K8 survives reading `cleanup_error` only when the row is not held (lesson lines 101–104).
- **K5 and K6.** These record no failure reason (lesson lines 110–112).

A reader of the knowledge entry alone would infer that the exit, stream, refusal and pin rows have no known survivors.

### F3 (low, wording): "runner held/cleanup/external carried" contradicts the code

The routed defect says the projection *drops* the four fields. `registry-replay.py:102-104` still builds receipts without any of them. Their current handling:

- `held` and `cleanup_error` became publication gates (`:86-91`).
- `external` and `non_hermetic_argv` reach only the report and the `live-dependent.json` sidecar (`:99-100,125-127`). The parenthetical on line 70 correctly says the sidecar is not digest-covered.
- `non_hermetic_argv` is not named in the row label.

Round23's field name `cleanup_ok` does not exist in the runner output; the runner emits `cleanup_error` (`registry-check.py:707,730`). The round24 tool correctly reads `cleanup_error`.

### F4 (low, missing half): routed defect 5 also named `instrument_sha256`

The defect text (line 81) and the seats it cites cover both fields: `round-23/w2/RevisionDeclared.md:24-25` and `CorpusClaim.md:15`. Round23's `replay-command-A.json` recorded `tools/registry-check.py` under `instrument_sha256`, hashed from the live tree.

At round24, `.ufo/evidence/round-24/replay-command.json` records only `tools/registry-replay.py(live tree, equals rev blob)` = `9fcd2dbb…`. That *is* the copy that ran (its argv runs the live-tree path), and I confirmed that `git show d2eaecd:tools/registry-replay.py | sha256sum` gives `9fcd2dbb…`.

So the half is resolved in practice, but by a hand-written receipt label. `registry-replay.py` records no digest of itself, and the disposition row does not mention this half.

The row also says "implemented", but the QUALITY48 execution note (`QUALITY.md:510-511`) says this fix "does not count as a repair". Saying "no predicate" is consistent with the note; the note's conclusion is not carried over.

### F5 (low, framing): the table reads as repairs of round23's `replay.py`

The lesson (`round-24.md:70-72`), the QUALITY48 execution note and `SCORECARD.md:1163-1165` all say this about K7–K11:

- They failed at base only because the tool was absent.
- They are "a new capability, not the repair of a defective tool".
- Round23's `replay.py` is unchanged.

`.ufo/evidence/round-23/replay.py` still compares siblings by string (line 52), still hashes the live-tree runner (line 78), and still drops the runner fields (lines 66–71). Its retained `observations.json:1947` `runner_sha256` is still the live-tree digest.

The disposition table (lines 70–73) names predicates without this framing.

### F6 (nit): "seven mechanisms" (line 47) is undefined and conflicts with the lesson's grouping

The lesson (lines 68–69) groups K1/K2 as one argv comparison, K5/K6 as one pin mechanism, and K7/K8/K9 as one refusal branch. With that grouping, the ten moved predicates form six groups: {K1,K2}, {K3}, {K5,K6}, {K7,K8,K9}, {K10}, {K11}. Seven only results if K9 is split from K7/K8. ClosureCarry F4 counted nine. The knowledge entry states the number with no grouping.

### F7 (nit, provenance): the table header and front matter give different line ranges

The table header cites lines 48–106; the `source:` front matter cites S085 as 53–104. Both ranges contain all eight defects, so nothing is lost.

On loose tokens: round24 itself superseded three rows append-only without touching the frozen round23 `requirements.json`. Tightening the loose tokens by the same route would not be a retrofill. "Left frozen" is therefore a choice; "open" is honest.

## Checks that held (no defect)

- **Errata intro facts.** `after.json` shows exit 0, revision `c8c5b88`, and K1–K11 all true. `before.json` shows only K4 true, so "K4 is a control, ten moved" holds.
- **Stream bullet.** The strict `>` comparison and publication-only refusal match the code (`:96`, `:181-184`).
- **Sibling bullet.** "Lane and fleet root are resolved" matches `plan()` (`:63-69`). "Mirrored under its target's name, unlike `registry-check --rev`" matches `registry-replay.py:161` versus `registry-check.py:773-782`, which links by entry name.
- **Further bounds.** The lone-surrogate exit 1 follows from an uncaught `UnicodeEncodeError` at `:96`. The stale `--out` bundle follows from `publish()` returning early (`:117-118`). Live rows certified by the gate: `replay-gate.json` 0/[] over all 43 receipts, and `live-dependent.json` = `pin-disposition-read`, `verify-round15`.

Seat-reported survivors (PredK2, PredK4, MutFixtures, MutProject, MutPlan) were read from retained reports, not re-executed. This item is not a "Run" item.

## Smallest safe correction (text-only, append-only addendum to the entry)

1. Errata intro: change "four rows" to "five rows" and add this bullet: "Live-dependent row: K10's one fixture sets both `external` and `non_hermetic_argv`. Dropping either disjunct leaves K10 discriminated; only the tool selftest catches it. K10 counts once, for the conjunction (QUALITY49). With the real runner, a published row with `non_hermetic_argv` is always `external`." Cite PredK10, MutProject and CodeLiveList.
2. Add one bullet pointing at lesson Erratum F for the survivors of K3 (`abs`, truthiness), K7, K8, K9 (characters instead of bytes) and K5/K6 (no failure reason). Reword the stream bullet: "counts UTF-8 bytes of the runner-decoded text, an untested property (MutProject M04)".
3. Disposition row 4: "held/cleanup gate publication (K7/K8); external/non_hermetic_argv are listed in the report and sidecar (K10, conjunction only); receipts still drop all four fields; no live marker in the bundle."
4. Disposition row 5: append "instrument_sha256: `replay-command.json` records the live-tree `registry-replay.py`, which is the copy that ran (= d2eaecd blob `9fcd2dbb…`); not a repair under QUALITY48."
5. Below the table: "K7–K11 are capabilities of the successor `tools/registry-replay.py`; `.ufo/evidence/round-23/replay.py` and its receipts are unchanged."
6. Define the "seven mechanisms" grouping, or change the count to match the lesson's stated grouping (six).

No tool, fixture, ruler or registry change is needed.

Tooling: no tools installed or upgraded.
