# T54W1Read22 — cold read at C0

- Heading: `### Round-21 gate/probe registry — finite environment differential`
- Candidate (content commit C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- Section bounds at C0 (`.ufo/waves/round-54/reader-section.py`): start 1990, end 2129
- `section_sha256`: `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06`
- Section bytes were read with `git -C <lane> show 59c38109bf11:SKILL.md` (lines 1990–2129), never from the working tree.
- Section text is byte-identical to base `d33053f7552d` (diffed both blobs; no differences), so C0 introduced no drift inside this section.

**Verdict: no finding against this section (`findings: []`).** One observation I made during the cold read is real but, on L1 ruling, is round-54 **C2 residue** and is kept below under `## Routed to L1` so the receipt survives.

## Routed to L1 — round-54 C2 residue (not a section finding)

L1 ruling (TameshiR54a2, this session): the `tools/env-diff.py` row's verdict map has an arm for the observed exit (`1 incomplete/failed measurement`), and the declared `could-not-evaluate = 2` class is scoped to each tool's **self-test** path (SKILL.md `## Standing rules`, the three-arm scratch-root bullet). The cell therefore understates an arm rather than stating a false clause, so it is routed as C2 residue — already on round 55's planned list as the `env-diff --contract` residue.

The disputed cell (byte-exact, SKILL.md:2001):

```
0 all surfaces classified; 1 incomplete/failed measurement; 2 could-not-evaluate; 64 usage
```

Observed at C0 and reproduced on a `git clone --shared` of the lane detached at C0 (`git -C "$D" rev-parse --show-toplevel` asserted the fixture dir first), running the row's documented Entry verbatim:

```
$ TMPDIR=<nonexistent> python3 fixture1/tools/env-diff.py \
    --contract fixture1/.ufo/evidence/round-21/c2-contract.json \
    --out out-f5.json --fleet-root /home/vgpnk/Projects/shokunin --jobs 1
EXIT=1
Traceback (most recent call last):
  ...
  File ".../fixture1/tools/env-diff.py", line 80, in execute
    with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir=strict_scratch_root()) as tmp:
  File ".../fixture1/tools/env-diff.py", line 45, in strict_scratch_root
    raise ScratchRootUnusable(
ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.../nonexistent-dir' (could-not-evaluate)
```

Mechanism at C0: `ScratchRootUnusable` was caught only in the `--selftest` branch (`tools/env-diff.py`:231–236); the run path's `except (OSError, ValueError, KeyError, TypeError)` at :263 excluded `RuntimeError`, so the run mode exited 1 with a traceback. The same tool's `--selftest` did hold the declared class: `EXIT=2`, one naming line, no traceback.

Forward state (read, not re-run): C1's fix commit `99c3bc8` ("… the env-diff run-path class") added `except ScratchRootUnusable` on the run path at `tools/env-diff.py:263`, so the residue the C0 receipts record has already been repaired forward.

Receipts (unchanged since the ruling; nothing was re-run):

- `T54W1Read22-receipts/env-diff-entry-unusable-tmpdir.stderr` (37 lines, traceback above)
- `T54W1Read22-receipts/env-diff-entry-unusable-tmpdir.stdout` (empty)
- `T54W1Read22-receipts/env-diff-selftest-unusable-tmpdir.stderr` (1 line, exit 2)
- `T54W1Read22-receipts/env-diff-selftest-unusable-tmpdir.stdout` (empty)

## Sweep — cells and anchors I opened that resolve at C0

Read with `git show 59c38109bf11:<path>` unless stated otherwise.

| Section claim | Artifact opened | Result |
|---|---|---|
| Source: `corpus/lessons/round-21.md` QUALITY43–44 | `corpus/lessons/round-21.md` | QUALITY43 at :79, QUALITY44 at :80 — resolves |
| `hermetic-env-differential.md` mined S079, reopened S028 | knowledge file :1; `corpus/SOURCES.md` rows S028, S079 | both rows present, `mined` — resolves |
| "frozen C1/C2 scripts and populations remain unchanged from 33d03b7" | blobs `c1-survivors.py`, `c2-count.py`, `c2-contract.json` at `33d03b7` vs C0 | identical blob ids — resolves |
| "c2 fixture is fleet-bound … reads sibling blobs at the fleet root" | `tools/round21-measure.py` docstring :8-12; `c2-count.py`:19 FLEET | matches — resolves |
| env-diff "frozen nine pins/seven profiles" | `c2-contract.json` | `surfaces` 9, `required_profiles` 7 keys — resolves |
| env-diff "raw tuples in `f5/receipt.json`"; "fixtures cover sensitivity, repeat variation and pin refusal" | `f5/receipt.json` (9 surfaces with per-profile tuples); `env-diff.py` selftest (tz/locale/home/columns, `repeat`, `pin-mismatch-public-cli`) | resolves |
| wave-route-mix Entry `--spec .ufo/waves/round-21/spec1.json --json`; "round20 refused spec/round21 accepted spec retained" | `spec1.json` (71 items, role counts match `routemix-spec1.json`), `routemix-r20-spec1.stderr` (`REFUSE seats=72`), `routemix-spec1.json` (`ok: true`) | resolves |
| round21-measure Entry flags; "delegates unchanged scripts"; "isolated fixture/private clones only; no lane Git writes" | `tools/round21-measure.py`:151-165, selftest fixture tempdirs | resolves |
| coldread probe Entry `--repo/--rev/--explain`, map "0 observed; 2 could-not-evaluate; 64 usage/forbidden override; selftest0 clean/1 failed" | `.ufo/evidence/round-21/coldread/measure.py`:103-113 + `round-18/measure.py`:1517-1539,1556-1655 | resolves |
| "frozen counter validates declared pins/tuple arithmetic and a source header" | `c2-count.py`:48-82, :117-118 | resolves |
| "Current source re-anchors retain the 199-entry prefix" | `coldread/ledger.json` `carried_from` + `provenance` ("original184 … plus15") and `lessons/round-21.md`:115,158 | resolves |
| Round22/23/24 `mined S082/S083/S084/S085` + QUALITY45/46/48 | the three knowledge files' `source:` lines; `round-22.md`:46, `round-23.md`:42, `round-24.md`:53 | resolves |
| wave-accounting "eight … fixtures"; "16 further"; wrong-count "1/TOTAL_MISMATCH" | `round-22/measure.py` (total 8), `accounting-extra-cases.json` (16), registry row `wave-accounting-wrong-count-entry`, `wrong-count-{bundle,expected}.json` | resolves |
| command-binding "ten-case counter"; source-read pair "expected1/ARGV_MISMATCH"; fixtures include round-23 and round-24 `extra-cases.json` | `round-23/measure.py` (total 10), registry rows, `command-binding.py`:166 | resolves |
| round-23 replay "opt-in `retain_streams=True`" | `.ufo/evidence/round-23/replay.py`:60 | resolves |
| "41 revision-pinned rows plus 2 live-dependent rows"; "covers all 43 stored receipts" | `.ufo/evidence/round-24/replay/bundle.json` (receipts 43), `live-dependent.json` (rows 43, `revision_pinned` 41, 2 live) | resolves |
| "`command-binding-selftest-r24` (44/44) … supersede the three round23 rows"; "two pinned rows … `bundle_sha256`"; "superseded 38/38 row … excluded" | `tools/registry.json` (44/44 row active; 3 round23 rows `superseded`; both pinned rows carry `bundle_sha256`) | resolves |
| "Frozen ruler `round-24/measure.py` (eleven predicates)" | `K1`…`K11` in `round-24/measure.py` | resolves |
| "47-row registry battery of round 24 (49 active rows from round 26 on; seat Read37)" | `tools/registry.json` at C0 (56 rows, 49 active, 7 superseded); `round-24` commits 47 active; `.ufo/waves/round-27/w1/Read37.md` | resolves |
| "`registry-replay-selftest` … expects 10/10; … projection and planning, not `--run`" | registry row text; `registry-replay.py`:190-245 (9 `--project` cases + 1 `--plan`) | resolves |
| "Errata E–P and residual corrections" | `round-24.md` errata E,F,G,H,I,J,K,L,M,N,O,P | resolves |
| Round-28 correction: `c2-count.py` FLEET "(line 19)" and `FLEET / frozen["repo"]` "(line 52)" | `c2-count.py` lines 19 and 52 | exact — resolves |
| "`round21-measure.py --claim c2` and its `--selftest` read the live lane's Git objects" | `c2-count.py`:19,52; `round21-measure.py` docstring :8-12 | resolves |
| "facade Entry above names the live lane path"; "write-scope cells cover writes only, not reads" | `round21-measure.py` entry text; section :2122-2124 | resolves |
| "`wave-route-mix.py` Entry reads `~/.omp/agent/config.yml`"; receipt `routemix-spec1.json` (`ok: true`) | `wave-route-mix.py`:19; receipt JSON | resolves |

Not reported (deliberately): the Round-23 "isolated clone" sentence and the Round-24 "writes only under `--out`"/"2 unavailable-input" cells are each contradicted by a labelled correction immediately below them in the same section ("fresh falsification, appended; text above unchanged"; "The table's write-scope and exit-map cells are not reliable safety promises"). They are disclosed errata, not unnoticed defects.

## Method / bounds

- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1Read22` (`HYAKU_SCRATCH=/fast/scratch/hyaku`); the clone was made with `git clone --shared` and detached at C0; `git -C "$D" rev-parse --show-toplevel` printed the fixture dir before any run. No mutating git command was run on the lane; no lane file was edited (the post-ruling `99c3bc8` check was a read of the lane log and file).
- No tool was installed or upgraded (pacman transactions paused host-wide; nothing was needed).
- Scratch tree removed after the receipts were copied here; no fixture left behind.
- Rewrite note: after the L1 ruling the JSON carries `findings: []`; the C0 receipts were not regenerated, and the same `cand`/`section_sha256` were kept.
