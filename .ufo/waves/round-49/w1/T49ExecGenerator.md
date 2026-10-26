# T49ExecGenerator — F10 property-based generator for `tools/staged-id-guard.py`

Seat: `T49ExecGenerator` (leaf). Round 49 C2 / frontier F10. Lane `tameshi-shokunin`, base
`8ca67421111fa354b47b803358391d0b07fc6db9`, contract `.ufo/evidence/round-49/contract.json`
(frozen `14d03ea4`, read only). Nothing in the lane was edited except this seat's files under
`.ufo/waves/round-49/w1/`; no git/jj mutation, no counter invocation (only `--selftest` of the
generator and the guard, and the guard's own CLI against scratch fixtures).

## Deliverables (all in `.ufo/waves/round-49/w1/`)

| file | sha256 | note |
|---|---|---|
| `T49ExecGenerator.pbt-staged-id.py` | `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05` | 988 lines, stdlib only; the L1 copies it byte-exact to `tools/pbt-staged-id.py` |
| `T49ExecGenerator.pristine.stdout` | `d285e10213f043ee2a5bf9de9bd8ceb47e3441a977d81b8c77d422170366bead` | seed 4949, 400 cases, against the pinned guard |
| `T49ExecGenerator.pristine.dump.jsonl` | `ca62402bc6125cb8003b3854a30bef829d29d5c6656be1f8a516ca2828a7cd28` | the 400-case dump (318 999 bytes, indices 0…399) the receipt run produced |
| `T49ExecGenerator.selfmutants.md` | — | 14 self-authored guard mutants, 13 killed, exact strings + per-mutant sha256 |
| `T49ExecGenerator.md` | — | this report |

Named gate used unedited: `tools/staged-id-guard.py`
sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` — matches the contract's
`claims.C2.named_gate` bytes (`sha256sum tools/staged-id-guard.py`).

## What was built

Frozen interface, exactly as `claims.C2.generator_interface` requires:

```
python3 -I tools/pbt-staged-id.py --guard GUARD --seed INT --cases N --dump FILE   # exit 0/1/2
python3 -I tools/pbt-staged-id.py --selftest                                        # 31 checks
```

* **Guard contact is CLI-only.** Each case is written as `registry.md` (+ `staged.md`, optional
  `map.json`) into a `tempfile.mkdtemp()` under the caller's `TMPDIR`, then
  `python3 -I GUARD --registry R --staged G [--map M] --json` is run with a 60 s timeout. The
  guard's code is never imported, exec'd or read by the generator; the dump line is written
  *before* the run so a violation at index *k* still leaves `dump[0..k]`.
* **Own oracle from the documented contract** (module docstring + `validate_map` docstring +
  CORPUS census rule): census rows `^ {0,3}\|\s*(S\d{3,})\s*\|`; numerically sorted `collisions`;
  `held` / `unmapped` / `naive_map` / `cascade` / `refused` / `next_free` / `registry_max` /
  `staged_max` / `safe_floor` / `extractor` / `column0_collisions` / `column0_miss` /
  `registry_docs`; with `--map` also `map_entries`, `map_targets`, `map_clash`,
  `map_staged_clash`, `map_below_floor`, `map_dedupe`, `map_uncovered`, `map_undocumented`,
  `map_held_moved`, `map_floor`, `map_ok`, `map_reasons`, `analysis_refused`. Exit semantics are
  the **observed** ones in `claims.C2.guard_exit_semantics_observed` (0 answered/admitted, 1
  refused analysis *or* inadmissible map, 2 setup refusal), not the docstring's map-only exit 1.
* **Comparison is stronger than the counter's.** The counter checks, for non-map cases, exit-2-ness
  plus `collisions`/`registry_rows`/`staged_rows`; the generator checks exit, `verdict`, the exact
  key set, and every documented field value. `map_reasons` is compared as (class, ids) pairs rather
  than prose (a reason's wording is not a behaviour I will grade); an unrecognised reason class
  counts as a violation, so a new refusal cannot slip through.
* **Thirteen recipes**, each deterministic about the class it exists to cover, selected round-robin
  from a seed-shuffled order (`Cycle`), so a 400-case run gives every recipe 30–31 cases and even a
  `--cases 13` run touches all twelve classes. Row counts stay small (0–8 rows per table; measured
  histogram of total rows per case: 3→18, 4→71, 5→31, 6→89, 7→20, 8+→171 of 400).
* **Observed distribution (QuickCheck classify/collect).** Per-case classes are computed with the
  contract's own predicates and printed as `CLASS <name>=<n>` lines and as `classes=…` on the last
  line; `CLASS_MIN = 20` in the generator marks `SHORT` (the contract floor is 10, this seat's own
  floor is 20).

## Evidence

### Pristine run — 0 violations, all classes ≥ 30

```
$ cd .ufo/waves/round-49/w1-style tree/tools && TMPDIR=$S/w python3 -I pbt-staged-id.py \
      --guard /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py \
      --seed 4949 --cases 400 --dump $S/w/final.jsonl
CLASS indent_1_3=248
CLASS indent_4_plus=31
CLASS id_4_plus_digits=31
CLASS collision=204
CLASS no_collision=62
CLASS held=49
CLASS unmapped=31
CLASS cascade=45
CLASS refusal=61
CLASS url_form_variant=30
CLASS map=104
CLASS map_inadmissible=31
PBT_STAGED_ID_TIME: seconds=18.58
PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,…
exit 0
```

(verbatim in `T49ExecGenerator.pristine.stdout`, sha `d285e102…`; the run used a copy at
`<scratch>/mimic/tools/pbt-staged-id.py` byte-identical to the deliverable, with cwd = that tools
directory, i.e. the counter's own calling shape.)

* **Oracle agreement: 400/400** on exit, verdict and the full documented field set. The counter's
  own four checks are therefore a subset of what was verified.
* **Determinism**: two runs of the deliverable (seed 4949, 400 cases) produce byte-identical dumps
  (`ca62402b…` twice) and identical stdout apart from `PBT_STAGED_ID_TIME`. A different seed (7,
  40 cases) produces a different case sequence and still 0 violations.
* **Runtime**: 14.0–18.6 s for 400 cases (400 guard invocations dominate; the generator itself is
  milliseconds). `--selftest` ≈ 0.05 s. Counter budget is 1800 s.
* **Shapes actually exercised** (recomputed from the dump with the pinned guard):
  no-map 190 answered / 76 refused / 30 setup refusal; map 42 admitted / 31 inadmissible / 31
  setup refusal; `analysis_refused` carried into an admitted map 8 times; `map_dedupe` non-empty 20;
  `held` non-empty 75; `unmapped` 34; `cascade` 50; `column0_miss` non-empty 142; 61 setup refusals;
  all nine map-refusal classes exercised (`carry 3, cover 4, floor 4, held 6, injective 3,
  registry 7, self 3, staged 4, undocumented 3`).
* **Interface edge behaviour**: missing arguments → 2; non-existent guard → 2; `--cases 0` → 2;
  unwritable dump → 2; all printed to stderr, never a traceback.

### Self-mutants — 13 of 14 killed, 8 invisible to the guard's own selftest

Full table with exact strings in `T49ExecGenerator.selfmutants.md`. Summary: M1 extractor `{0,3}`→
`{0,2}`, M2 column-0 probe indent-blinded, M3 no `www.` strip, M4 naive `top+index+1`, M5 floor `<`→
`<=`, M6 `< 5` cells → `< 4`, M7 duplicate ids allowed, M8 `safe_floor` ignores `staged_top`, M9
`refused` drops `unmapped`, M11 no scheme strip, M12 `len(head) > 8` → `> 0`, M13 `/`-openability
dropped, M14 suffix `{2,6}` → `{2,}` — all confirmed by replaying the counterexample through the
pristine guard and the mutant (different `(exit, JSON−shas)`). M10 (strip/lower order swap) is the
deliberate equivalent control and survives, so `violations=0` is shown to be an answer, not a
vacuous generator.

## Findings

1. **The docstring's exit-1 sentence is imprecise — confirmed, not a bug to fix here.**
   `tools/staged-id-guard.py:38-39` says “exit 1 = the map is not admissible”. The guard also exits
   1 for a *refused analysis* (`refused = bool(unmapped) or bool(cascade)` at `:157`, returned at
   `:491-495`). Reproduction, a collision whose staged row has no document:
   ```
   $ python3 -I tools/staged-id-guard.py --registry D/registry.md --staged D/staged.md --json
   {'verdict': 'refused', 'refused': True, 'unmapped': ['S002'], 'collision_count': 1}
   $ echo $?   # 1
   ```
   This is exactly the `guard_exit_semantics_observed` note in the contract; the generator follows
   the observed semantics and never the docstring, and a `refusal`-class case exists for each
   route (76 refused no-map cases, 61 setup refusals).
2. **`document_key` reads the source head *before* the first spaced dash**, so a path-like document
   only counts when it begins the cell. `tools/staged-id-guard.py:106`
   (`head = re.split(r'\s+[—–]\s+', source)[0].strip()`) with the `len(head) > 8` gate at `:113`.
   My first path recipe wrote `Src S003 — notes/paper-3.md`; the guard correctly reported no
   document (`held {}`, `unmapped`) and only my oracle was wrong about which side of the dash is
   the head. Fixed by putting the document first (`notes/paper-3.md — note`); the shape is now a
   recipe (`rec_path_document`, 30 cases) and the branch is killable (M12, M14 above).
3. **The 0-3-space extractor is the whole point of the tool and needs both sides of the bound.**
   `RECIPES` emits indent 0–3 census rows *and* indent 4–6 non-rows, in both tables: 248 cases carry
   a 1–3-space row and 31 carry a 4+ space row (the `indent_4_plus` class exists only because 4+
   rows are excluded from `parse_rows`, `:82-83`). Without the 4+ shape the extractor's upper bound
   is untested — that is precisely M1's kill (`collision_count` 1 vs 0).
4. **`url_form_variant` requires raw forms that differ only in scheme/www/slash/case**, and the
   scheme axis is only testable if one side has *no* scheme: `normalise_document` (`:117-121`) strips
   `https?://`, `www.`, case and trailing slash. `doc_forms` pairs URL forms; the scheme rule needs a
   bare host/path head on one side (`rec_held` kinds `scheme_less_staged` / `scheme_less_registry`),
   which is what kills M11. A generator that only pairs URLs cannot test scheme stripping at all.
5. **Coverage that this generator deliberately does not reach** (each named with the reason, so the
   counter's `classes_short`/`oracle_disagree` are not the only thing a reader can check):
   * oversized inputs — `MAX_TEXT = 32 MiB` (`:69`), `MAX_MAP = 1 MiB` (`:70`), refusal at `:424`;
     the counter's fixtures are small and a 32 MiB write per case is not a case.
   * non-regular input files — `:422`; the interface writes regular files (verified by hand instead:
     `--map /dev/fd/N` → exit 2, `setup_refusal`).
   * non-UTF-8 bytes — `:437`; the dump is JSONL of `str`, so this route is structurally unreachable.
   * duplicate JSON map keys — `_no_duplicate_keys` at `:411`; `json.dumps` from a dict cannot emit
     them.
   * S-ids longer than 12 characters — refusal at `:128`, which the module docstring does not
     document; asserting it would be guessing from source, so no case is generated.
   * `registry_docs` first-wins when two registry rows carry one document — docstring says “dedupe
     to the registry id” without saying which; the generator never creates the ambiguity.
   * `map_reasons` prose — compared as (class, ids), so a mutant that only rewords a reason string
     survives by design.
6. **Why the class floors matter for the counter.** The counter counts a class only when the
   *pristine guard's* answer has the property (`claims.C2.classes`, `case_classes`), so a case that
   intends `held` but lands on an `unmapped` row counts for the wrong class. Each recipe is written
   so its class holds by construction (held: staged document normalises to a registry document;
   cascade: a staged-only id *is* the naive target `S%03d % (top+1)`; unmapped: a source that fails
   every `document_key` branch). Measured minimum over the 12 classes is 30 against a contract floor
   of 10 and this seat's floor of 20.

## Risks / limitations

* The hidden 12-mutant panel is unread. My self-panel is 13 distinct exact-string edits over the
  documented bullets and 13 are killed; a hidden mutant that changes only undocumented behaviour
  (finding 5) or only `map_reasons` prose would survive. That is a deliberate boundary, not an
  oversight, but it is the residual risk on the 11-of-12 target.
* Class coverage scales with `--cases / 13`: every class is *present* from 13 cases upward (one per
  recipe), but the contract floor of 10 per class needs ~130 cases and this seat's floor of 20 needs
  ~260. The frozen run is 400.
* Oracle agreement is evidence about the *guard*, not about my reading of prose: where the docstring
  is silent (finding 5) I asserted nothing.

## Tooling

Nothing installed or upgraded: Python 3.14.8 stdlib only (no third-party import in the deliverable);
pacman is paused host-wide and no install channel was needed. Scratch root
`/fast/scratch/hyaku/tameshi-r49/T49ExecGenerator/` was used with `TMPDIR` pointed inside it and is
deleted before yield; every cited receipt is copied into `.ufo/waves/round-49/w1/`.

## Summary

Built the F10 generator (`0cbee392…`, 988 lines, stdlib only, CLI-only guard contact, own oracle
from the documented contract and the observed exit semantics).
Pristine guard, seed 4949, 400 cases: `violations=0`, dump 400 lines (`ca62402b…`), 18.6 s;
deterministic across runs and stable across cwd.
All twelve frozen classes covered, minimum 30 (contract floor 10). Shape census of the 400 cases:
190/76/30 no-map answered/refused/setup-refusal and 42/31/31 map admitted/inadmissible/setup.
400/400 oracle agreement on exit, verdict, key set and every documented field — broader than the
counter's four checks.
14 self-mutants: 13 killed with differential confirmation, 8 of them invisible to the guard's own
`--selftest`; the surviving one is the deliberate equivalent control.
Findings: docstring exit-1 vs observed exit-1-for-refused-analysis; `document_key` head-before-dash
semantics; 4+ space rows and scheme-less forms are what make the extractor and normaliser killable.
Not covered, by design and named: oversized/non-regular/non-UTF-8 inputs, duplicate JSON keys,
S-ids > 12 chars, the first-wins ambiguity, and reason prose.
