# SimplGuard — guard YAGNI probe (operability)

Seat: `L1Tameshi43.SimplGuard` (simplifier). Item: name code in
`tools/staged-id-guard.py` that no selftest case and no live input exercises —
fields the counter never reads, options never used, refusal branches never
reached; for each, whether deleting it changes any selftest or counter field.
Report a list, not an edit. Read-only on the lane; this file is the only lane
write.

## Subject bytes (pinned)

| blob | sha256 | source |
|---|---|---|
| `tools/staged-id-guard.py` | `2e8f2e89…d4d6ff2` | `git show 3aee2c0:tools/staged-id-guard.py` == `contract.frozen_tools["tools/staged-id-guard.py"]` == working tree |
| `.ufo/evidence/round-43/guard/measure.py` | `ae66342d…8f54161e` | `git show 3aee2c0:` == `claims.C3.counter_sha256`; disk bytes drifted mid-wave but the JSON read set is byte-identical to the freeze's (verified by AST) |
| `corpus/SOURCES.md` at 3aee2c0 | `c50ca1fb…f4c961fd` | live registry input (114 rows) |
| `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` | `020fbeaa…394807` | staged package (103 rows, collisions `S153–S159`, held `{S153:S105, S154:S106, S159:S155}`, floor `S256`) |

## Method (reproducible)

In-process branch coverage, coverage.py 7.17.0 (`uv run --with coverage`), four
sessions of `main()`: `--selftest`; `--registry … --staged … --json` (live);
same plus `--map naive.json`; same plus `--map safe.json` (maps built with the
counter's own `own_parse`/floor arithmetic — the exact bytes the counter
feeds). Missing statements/branch arcs intersected across all four sessions.
Reader audit via `ast` (Load subscripts + `.get()` args) on the tool, its
selftest, and the counter. Live probes for reachability of candidate refusals.

## A. Refusal / error branches reached by neither selftest nor live

| lines | branch | reached only by (probe) | deleting changes a selftest or counter field? | verdict |
|---|---|---|---|---|
| `:89–90` | `sid in rows` → `duplicate id` | crafted 2-row registry → `setup_refusal` rc2 | no (selftest has no duplicate fixture; live files have no dups) | **keep** — without it a duplicate silently last-row-wins and `collisions` is wrong; cheap for its hazard class |
| `:124–125` | `not SID_RE.fullmatch` → `not an S-id` | **unreachable, not just unexercised**: every call site pre-guarantees the pattern (`ROW_RE` capture `:81–84`, `validate_map`'s own `fullmatch` `:202–205`, derived `S%03d` strings) | no | **deletion candidate** (dead precondition; the one caller-visible effect is impossible today) |
| `:126–127` | `len(sid) > 12` → `S-id too long` | a >11-digit S-id | no | **keep** — Python 3.14 `int()` raises `ValueError: Exceeds the limit (4300 digits)`; verified. Deleting turns a 5000-digit map id into a bare traceback (exit 1, no JSON), falsifying the docstring's "never a bare traceback" promise the sentinel seat is enforcing |
| `:197–198` | non-dict `map_doc` / missing `"map"` | probe `{"map"}`-less file → `setup_refusal` rc2 | no | keep — exit-2 contract |
| `:416–417` | `os.stat` OSError | missing/EPERM path | no | keep — contract |
| `:418–419` | `not stat.S_ISREG` | FIFO probe | no | **keep** — without it a FIFO `--map` hangs `open()`; this is the sentinel's exact attack |
| `:420–421` | `st_size > limit` | >32 MiB file / >1 MiB map | no | keep — contract (also the only user of `MAX_TEXT`/`MAX_MAP` and `stat`) |
| `:425–426`, `:427–428` | read OSError / UnicodeDecodeError | adversarial bytes | no | keep — contract |
| `:435–436` | `json.JSONDecodeError` | malformed map file | no | keep — contract |
| `:449–451` | missing `--registry`/`--staged` | probe → stderr rc2 | no | keep — contract |
| `:465–470` | `except Refusal` handler + `setup_refusal` JSON | any of the above | **yes, weakly**: on a refusing input the counter would see `doc=None` (`measure.py:139–141`) and print the short `guard_error` line instead of the full field line. PASS/FAIL unchanged | keep — contract |
| `:244–245` | `selfmap` reason `map leaves a colliding id on itself` | probe map `{S153:S153}` → reason fires | no | **redundant code — deletion candidate**: `selfmap` ⊆ collisions ⊆ registry ids, so every self-map hits `target in registry` → `clash` first (`:217–224`, probed: both reasons emitted). Deleting removes a reason string only; verdict (`map_ok`, `verdict`) provably unchanged on every input, not just tested ones |
| `:398–399` | selftest `if not ok: print('FAIL …')` | fires only on a regression | deletes the failure diagnostic → a failing case would lose its note; `cases=`/`failed=` counts unchanged | keep — it's the test's error path, not dead weight |
| `:473→476, 480–481` | non-`--json` human output (`STAGED_ID_GUARD:` summary + per-collision lines) | probe without `--json` (works, prints `collisions=7 … verdict=refused`) | no | deletion candidate in form only — but it is the tool's human face (docstring advertises the flag, and `next_free`/`collision_count`/`cascade_count` have no other reader). Recommendation: keep; if deleted, drop those three fields too or they become unread |
| `:229–230, 237–239` | `below_floor` collect + `partial map targets are below the safe floor` | **reachable and probe-proven**: map `{S153:S105,S154:S106,S159:S155,S155:S000,S156:S257,S157:S258,S158:S259}` → `inadmissible`, `map_below_floor=["S000"]` | **yes — semantic change**: without it such maps are *admitted*. It is the only enforcement of "at or above the safe floor" for a fresh target, which `claims.C3.statement` asserts verbatim. T12 (`:364–368`) nominally covers it but is **satisfied by `not injective`** (self map `{S002:S003,S004:S003}`), so the floor has zero real test coverage. | **not a deletion candidate — a test gap**: deleting it silently falsifies the C3 claim and no counter field moves. Keep; the missing coverage is the finding |

## B. Emitted JSON fields with no reader anywhere

Counter reads off tool JSON (AST-verified): `collisions`, `held`, `unmapped`,
`cascade`, `naive_map`, `verdict`, `map_dedupe` (+ exit codes). Selftest
adds: `refused`, `extractor`, `column0_miss`, `map_held_moved`,
`map_undocumented` (+ `collisions`/`held`/`unmapped`/`naive_map`/`cascade`/
`map_dedupe`). Everything else emitted is **write-only**:

`registry_rows`, `staged_rows`, `registry_max`, `staged_max`, `safe_floor`,
`registry_docs`, `column0_collisions`, `registry_sha256`, `staged_sha256`,
`analysis_refused` (`:460`), `map_entries`, `map_targets`, `map_clash`,
`map_staged_clash`, `map_below_floor`, `map_uncovered`, `map_floor`,
`map_ok`, `map_reasons` (duplicate of the returned `reasons`), and `reason`
inside the `setup_refusal` JSON.

- Deleting any of them changes **no selftest case and no counter field**.
- Caveat: the docstring `:49–53` freezes every field above *except* the
  `map_*` keys as "the interface … for the round-43 counter", and wave-1 prose
  cites `column0_miss`/`extractor` as the indented-row proof. So these are
  interface-weight, not logic — removal is an interface decision, not an
  operability gain. Highest-signal single deletion: `column0_collisions`
  (computed `:135–138`, read by nobody, and its complement `column0_miss`
  carries the actual proof).
- `refused`: emitted value in `--map` mode is overwritten `:461`; read only by
  selftest (no-map path). Keep — internally loaded `:464`.

## C. Dead stores (executed, result never consumed)

| lines | store | reader | deletion changes? |
|---|---|---|---|
| `:93` | `'cells': len(cells)` | none (AST) | no selftest/counter field; dead key in every row dict |
| `:94` | `'lineno': lineno` | none (the refusal messages use local `lineno`, not `row['lineno']`) | same; delete both, keep only `'document'` |
| `:460` | `result['analysis_refused']` | none — docstring-mentioned, counter never reads it, selftest bypasses `main` | no |
| `:105` | `cells[1] if len(cells) > 1 else ''` | `len(cells) >= 5` guaranteed by `:86` — the `else ''` arm is **unreachable**, not just unexercised | no |
| `:441–443` | `argparse` defaults: `--registry`/`--staged`/`--map` lack `required=`/defaults — harmless | — | n/a |

## D. Options & entry points

- All five CLI options are exercised (`--selftest`, `--registry`, `--staged`,
  `--map`, `--json` — the counter invokes every one). **No unused option.**
- `main(argv=None)` — the `argv` parameter has no caller that passes one; only
  `sys.argv` runs it. Cosmetic, not a deletion.
- `--selftest` ignores the other flags silently — no finding, the counter
  relies on the short-circuit.

## E. Deletion candidates (ranked, no measured delta)

1. `selfmap` reason `:244–245` — verdict-redundant under `clash`; provably
   zero admitted/refused delta on any input. Cleanest removal.
2. `row['cells']` / `row['lineno']` `:93–94` — dead stores.
3. `id_number`'s `not SID_RE.fullmatch` guard `:124–125` — unreachable by
   construction at every call site.
4. `cells[1]` else-arm `:105` — unreachable by construction.
5. `analysis_refused` `:460` — write-only field.
6. `column0_collisions` `:174` — write-only field; `column0_miss` is the proof.
7. (Weakest) the non-`--json` else-branch `:475–481` — human-facing; deleting
   it is an interface call, not a correctness win.

## F. Stops — where deletion WOULD harm

- `below_floor` (`:229–230, :237–239`): deleting it flips `inadmissible →
  admitted` on an existing input class and voids "every fresh target is at or
  above the safe floor" in `claims.C3.statement`. It is claim-bearing code
  with **zero test coverage** — T12 is satisfied by injectivity before the
  floor reason is ever needed. The right fix is a selftest case
  (`{'S002':'S000'}`-style), not a deletion.
- The `read_text`/`load_map`/`main` refusal lattice: unexercised on live
  inputs but it is the documented exit-2/no-traceback contract and the only
  thing between a FIFO `--map` and a hang, between a 5000-digit id and a
  `ValueError` traceback.
- `duplicate id` refusal `:89–90`: untested but failure mode is silent wrong
  `collisions`.
- `extractor`, `column0_miss`, `map_held_moved`, `map_undocumented`: read only
  by the selftest — deleting them *breaks* cases T1_extractor_label /
  T1_column0_blind / T7 / T8.

## Evidence artifacts

`/tmp/tameshi-r43-w2-SimplGuard/` (deleted at return): `tool.py` (pinned
bytes), `counter.py`/`counter.freeze.py`, `registry.md`/`staged.md`,
`coverage.json` (per-session missing statements + branch arcs),
`live.json`/`naive.out`/`safe.out`, `floor.json`/`selfmap.json`/`notmap.json`/
`dupreg.md`/`dupkeys.json` probes.

## Tooling

`uvx --from coverage` / `uv run --with coverage` → coverage.py 7.17.0 (channel:
uv tool run; reason: branch-accurate reachability for this probe; pacman
untouched per pause). No other installs.

## Bounds kept

No edits anywhere; `--selftest`/live runs executed on the pinned copy under
/tmp only (the tool is read-only itself). No counter run at any rev. Only lane
write: this file.
