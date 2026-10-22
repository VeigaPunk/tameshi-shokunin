# C2Determinism — is the C2 interop counter byte-reproducible?

Lane: TameshiR25 / round 25, wave 1. Seat: `TameshiR25.C2Determinism` (leaf; no subagents spawned).
Frozen contract: `.ufo/evidence/round-25/contract.json` at lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`
(base `1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5`), plus the working-tree amendments 1 and 2 that were present
in the lane while this seat ran.
Scope: determinism of `tools/mte-interop.py --check` — the C2 counter — plus an independent re-derivation of the
C2 claim from the emitted artifacts. Read-only everywhere except this report file and `/tmp` scratch.

## Verdict

**PASS on the named check, with two bounded observations that the integrator must fold into the C2 wording.**

1. At the frozen lane revision `c9ff09f` the counter is byte-reproducible: **five independent runs produced
   byte-identical emitted trees and byte-identical stdout** (runs A–E below; 5/5 exit 0, `MTE_INTEROP: PASS
   legs_conforming=8/8`). The 9 emitted files per run carry the same sha256 in every run.
2. The emitted artifacts are independently re-derivable from the recorded ledger: a separate verifier I wrote
   (not the tool's own judge) re-validated every emitted report against the pinned official schema 3.9.0,
   matched every mutant id and every per-mutant verdict against the runner's committed `TABLE_*` constants,
   matched every emitted source against the runner's `PIN_*` blob hashes **and** against `git show <REV>:<path>`
   in the live fleet, and recomputed the kill rate against `official-metrics.json` — 8/8 on all four axes, for
   all six emit directories tested.
3. **Observation A (stdout, current tool version):** the tool version now in the lane working tree
   (`sha256 24de859f…`) prints `MTE_WORKDIR: /tmp/tameshi-mte-regression-<random>` as its first stdout line,
   so **stdout is not byte-reproducible** across runs even though the emitted artifacts are. Any recorded
   stdout transcript must be normalised (or the line dropped) before it can be compared byte-for-byte.
   The frozen-revision tool (`sha256 311448d9…`) does not print that line and its stdout is byte-identical
   across runs.
4. **Observation B (emit directory is not cleaned):** `--emit` creates the directory and writes the current legs
   but never removes anything else, so a stale artifact from an earlier run survives into the next emit
   (`tools/mte-interop.py:279-282`). A consumer that diffs two emit directories will see the stale file, not a
   tool change. Emit into a fresh directory, or clear it, when recording an emit as evidence.

Nothing here required a correction to the counter itself; the smallest safe correction is in the **recording
practice** (Observation A: quote the artifacts, not the raw stdout line; Observation B: use a fresh emit dir),
plus the wording notes in "Risks" below.

## Method

Private clone first, exactly as assigned — nothing ran inside the lane repo:

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/TameshiR25.C2Determinism-r25
git -C /tmp/TameshiR25.C2Determinism-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
# → CLONE_OK, HEAD c9ff09fb41fb8aac5fc335faf10858ff606bd5df
```

Tool under test (frozen revision):
`sha256sum tools/mte-interop.py` → `311448d92c10891e2fd9513586c203d4d245f94559ab7843de48bef4de1db422`
(vendor tarballs unchanged: `ce17812b…` / `adb78e13…`, matching the contract's `vendor_sha256`).

Host: node v24.21.0, uv 0.13.0, CPython 3.15.0, jsonschema 4.25.1 (all preinstalled; nothing installed —
see "Tooling record").

## Evidence

### 1. The counter command and its exits (frozen revision `c9ff09f`)

Command (identical to the contract's amended counting command):

```
cd /tmp/TameshiR25.C2Determinism-r25
uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check \
    --fleet-root /home/vgpnk/Projects/shokunin --emit /tmp/TameshiR25.C2Determinism-<X>
```

| run | emit dir | variation | exit | stdout verdict |
|---|---|---|---|---|
| A | `-a` | baseline | **0** | `MTE_INTEROP: PASS legs_conforming=8/8` |
| B | `-b` | baseline (repeat) | **0** | `MTE_INTEROP: PASS legs_conforming=8/8` |
| C | `-c` | baseline (repeat) | **0** | `MTE_INTEROP: PASS legs_conforming=8/8` |
| D | `-d` | `TMPDIR=/tmp/TameshiR25.C2Determinism-tmpD`, `PYTHONHASHSEED=12345` | **0** | `MTE_INTEROP: PASS legs_conforming=8/8` |
| E | `-e` | cwd `/tmp`, absolute tool path, emit dir pre-seeded with a stale file | **0** | `MTE_INTEROP: PASS legs_conforming=8/8` |

Full stdout of run A (identical for B, C, D, E):

```
MTE_LEG bash-checklist-run: CONFORMS (schema=ok official_score=46.666666666666664 tameshi_score=46.666666666666664 official_killed=7 recorded_killed=7 official_valid=15 recorded_defects=15)
MTE_LEG bash-mado-verify: CONFORMS (schema=ok official_score=40 tameshi_score=40.0 official_killed=4 recorded_killed=4 official_valid=10 recorded_defects=10)
MTE_LEG bash-surface-census: CONFORMS (schema=ok official_score=80 tameshi_score=80.0 official_killed=8 recorded_killed=8 official_valid=10 recorded_defects=10)
MTE_LEG bash-tsukuroi-census: CONFORMS (schema=ok official_score=60 tameshi_score=60.0 official_killed=6 recorded_killed=6 official_valid=10 recorded_defects=10)
MTE_LEG js-claims-check: CONFORMS (schema=ok official_score=70 tameshi_score=70.0 official_killed=7 recorded_killed=7 official_valid=10 recorded_defects=10)
MTE_LEG js-kimi-census: CONFORMS (schema=ok official_score=80 tameshi_score=80.0 official_killed=8 recorded_killed=8 official_valid=10 recorded_defects=10)
MTE_LEG js-round-gate: CONFORMS (schema=ok official_score=50 tameshi_score=50.0 official_killed=5 recorded_killed=5 official_valid=10 recorded_defects=10)
MTE_LEG js-sources-check: CONFORMS (schema=ok official_score=50 tameshi_score=50.0 official_killed=5 recorded_killed=5 official_valid=10 recorded_defects=10)
MTE_INTEROP: PASS legs_conforming=8/8
```

stderr was empty (0 bytes) for every run.

### 2. Byte-for-byte comparison of the emitted trees

`diff -r` between every pair (A/B, A/C, A/D, A/E) → no output, exit 0.
`cmp` per file → clean for all 9 files in every pair. The emitted sha256 set is identical in all five runs:

```
ddb9c3d4175a7fe205fb0c1399b9645bf86846cd478bd84423d4ceb682e71d2c  bash-checklist-run.mte.json
ff077c772f0f3429128ddc23c77eb8a5b3ddc0d408ee979c7207d4851cd73c4f  bash-mado-verify.mte.json
d42fa53fc015e1e82e9476d7d5203a14a16347fff74b18585e026f132b389267  bash-surface-census.mte.json
1cc871118896e9e547e997fdbe235dc3ffe42a371257b2bcdd735b5e85151b33  bash-tsukuroi-census.mte.json
c26a62195e5f0fc5bf4c73ac634b09789a6f57fe64fd3b50b8a5cc373248a781  js-claims-check.mte.json
43107b9b6402d7ef7662db0200b7f4aacc1abab879afcd101eafefa7e89056a4  js-kimi-census.mte.json
8c8e97a6c6114ce7c8ae3fa937a279d3b369e46720b9fbdfea57f38793d53f80  js-round-gate.mte.json
3f4aa76ab0f9d76a6cfe9297a9f3c90cbfbac81eee7902ea98b489a69a27544b  js-sources-check.mte.json
75fb992224d282c996d99b2a5f4c6340fbcf41d5b39b0e4ebabf20b8f4462ff5  official-metrics.json
```

stdout comparison: `cmp A.stdout B.stdout` clean; `cmp A.stdout C.stdout` clean; `cmp A.stdout D.stdout` clean;
`cmp A.stdout E.stdout` clean. (The frozen tool prints no workdir line, so its stdout is reproducible too.)

The emitted reports contain no absolute paths, no timestamps and no scratch-root names — grep for
`/tmp/`, `/home/`, `tameshi-mte`, ISO dates and clock times over the emitted JSON found no such field in any
file (the only hits were digit sequences inside the embedded `source` text of the pinned scripts).

### 3. Independent re-derivation of the C2 claim from the artifacts

My own verifier (`/tmp/TameshiR25.C2Determinism-verify.py`, outside the repo; it re-parses the runner's
`PIN_*`/`REV_*`/`TABLE_*` constants and never calls the tool's judge):

```
uv run --no-project --with jsonschema==4.25.1 python3 /tmp/TameshiR25.C2Determinism-verify.py <emit-dir>
```

Per leg it checks four independent axes:

- **schema**: the on-disk `<leg>.mte.json` re-validated with `jsonschema.Draft7Validator` against the vendored
  official `mutation-testing-report-schema` 3.9.0 member;
- **ledger**: the emitted mutant-id set equals the recorded table's id set, and every emitted per-mutant verdict
  equals the recorded `TABLE_*` verdict for that id (the recorded table is parsed out of
  `tools/mutate-and-run.sh`, not out of the tool's output);
- **pins**: `sha256(emitted source)` equals the runner's `PIN_*` for that leg **and** equals the bytes of
  `git show <REV>:<path>` read live from the fleet repo — so the emitted source is the pinned blob, not the
  working tree;
- **metrics**: `official-metrics.json`'s `killed` / `totalValid` / `mutationScore` equal the recomputed values
  and the recorded ledger's killed/total counts.

Result, identical for emit dirs `a`, `b`, `c`, `d`, `e` and `live1` (exit 0 each):

```
leg                    valid recKill   kill tameshiScore     offScore  verdict
bash-checklist-run        15      7      7 46.666666666666664 46.666666666666664  OK
bash-mado-verify          10      4      4         40.0           40  OK
bash-surface-census       10      8      8         80.0           80  OK
bash-tsukuroi-census      10      6      6         60.0           60  OK
js-claims-check           10      7      7         70.0           70  OK
js-kimi-census            10      8      8         80.0           80  OK
js-round-gate             10      5      5         50.0           50  OK
js-sources-check          10      5      5         50.0           50  OK

INDEPENDENT_VERIFY: PASS legs=8 schema_valid=8/8 ledger_agrees=8/8 pins_agree=8/8
```

This also confirms the runner's own hermeticity claim (`tools/mutate-and-run.sh:109-113`): each leg is
materialized from the repo's git object store at a pinned revision, so concurrent edits in the sibling lanes
cannot move a replay. My `git show` cross-check read the sibling repos **live** while other seats were editing
them, and the emitted bytes did not change.

### 4. The counter's own negative controls still fail when they should

```
uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest
→ MTE_SELFTEST: 10/10 pass   (exit 0)      # frozen-revision tool, sha256 311448d9…
→ MTE_SELFTEST: 16/16 pass   (exit 0)      # lane working-tree tool, sha256 24de859f…
```

The 16/16 run is the working-tree version that `contract-amendment-2.json` describes (judge gains `ledger` and
`per_mutant` checks; emitter-level INCONCLUSIVE→RuntimeError and exact-location cases). Both hold, so the
counter can still fail.

### 5. The tool version currently in the lane working tree (moving target)

The lane's `tools/mte-interop.py` is **not** the frozen revision's file. Observed hashes:

| where | sha256 |
|---|---|
| revision `2a97ec1` (pre-amendment) | `58a5ae924c155e9a05849ba23af195715030443480373d3a536310a2fe6240e6` (= contract `C2.tool_sha256`) |
| revision `c9ff09f` (amendment 1) | `311448d92c10891e2fd9513586c203d4d245f94559ab7843de48bef4de1db422` (= amendment 1 `tool_sha256_now`) |
| lane working tree, observed 2026-10-22 ≈05:45 | `24de859f18b9106c9e35d70cd35bcee92f7a3bef41eb22b732be23064f8f074f` |
| `contract-amendment-2.json` `tool_sha256["tools/mte-interop.py"]` | `8c24255c9e482751772e958e5ba9a615891ca7e5dfc9426d2fb5667ceae65552` |

The last two do not match each other: the working-tree file changed again after amendment 2 was written, so the
lane's tool is a moving target during this wave. I therefore measured the working-tree version as an immutable
snapshot: copied into `/tmp/TameshiR25.C2Determinism-r25b` (same revision, same vendored tarballs) and run twice.

Result: **both runs exit 0, `MTE_INTEROP: PASS legs_conforming=8/8`, and all 17 emitted files are
byte-identical** between the two runs (`diff -r` exit 0). The 8 `.mte.json` files and `official-metrics.json`
carry **exactly the same sha256 as the frozen revision's emit** (`ddb9c3d4…`, `75fb9922…`, …) — the newer
emitter only adds 8 `.spec` copies beside them. The two stdouts differ in exactly one line:

```
1c1
< MTE_WORKDIR: /tmp/tameshi-mte-regression-o973zaa_ (removed on PASS)
---
> MTE_WORKDIR: /tmp/tameshi-mte-regression-mh70oofk (removed on PASS)
```

That is Observation A: **the artifacts are deterministic; the stdout transcript of the current tool version is
not.** (The frozen-revision tool prints no such line — see §2.)

### 6. Clone outside the fleet root without `--fleet-root` (corroborates amendment 1)

```
cd /tmp/TameshiR25.C2Determinism-r25
uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check
→ MTE_INTEROP: SETUP (regression exit 2)
→ exit 2
```

Same message and same exit as the `observed_failure` recorded in `contract-amendment-1.json`
(`"exit": 2, "stdout": "MTE_INTEROP: SETUP (regression exit 2)"`): the runner resolves sibling lanes from its
own grandparent directory (`tools/mte-interop.py:222-245`), so a clone outside the fleet root must be given
`--fleet-root`. The frozen contract's `C2.counting_command` still omits `--fleet-root`; amendment 1 supplies it.

### 7. The "before" state holds

`git cat-file -e 1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5:tools/mte-interop.py` → not present ("exists on disk,
but not in …"), and `git ls-tree 1f73157 tools/vendor/` is empty: at the base revision the tool and its
vendored tarballs do not exist, which is the contract's `before` ("tool absent at 1f73157: legs_conforming=0/8
(exit 2, no file)").

### 8. No side effects on the fleet

Every write of these runs landed under `/tmp` (clone, emit dirs, scratch roots). The lane repo's
`git status --short` after the runs shows only sibling-authored wave files (`M corpus/SOURCES.md`,
`?? .ufo/waves/round-25/…`) and no artifact of the C2 counter; the counter stages a private copy of the runner
plus read-only symlinks to the sibling repos and materializes each leg from the git object store into a
temporary scratch root that is removed on PASS (`tools/mte-interop.py:222-245`).

## Findings to fold into the C2 wording

1. **Name the tool hash in the determinism statement.** The counter's bytes changed three times during this
   wave (`58a5ae…` → `311448d9…` → working tree). A determinism claim is only meaningful against a named
   `tools/mte-interop.py` sha256; both the frozen revision (`311448d9…`, 5/5 byte-identical) and the current
   working-tree snapshot (`24de859f…`, 2/2 byte-identical) satisfy it.
2. **Quote the emitted artifacts, not the raw stdout, as the reproducibility evidence** — the current tool's
   stdout embeds a random scratch path (`MTE_WORKDIR: /tmp/tameshi-mte-regression-<random>`).
3. **Emit into a fresh directory** when recording an emit; `--emit` does not clean its target
   (`tools/mte-interop.py:279-282`) and a stale file from an earlier run survives into the next emit
   (demonstrated in run E: `stale-leg.mte.json` was still present after the run).
4. **The counter needs `--fleet-root` outside the lane checkout** (exit 2 without it, §6).
5. **The emitted reports are a faithful, pinned projection of the ledger** — independently re-derived per leg
   against the runner's `TABLE_*`/`PIN_*` constants and against `git show <REV>:<path>` in the live fleet
   (§3). This is the strongest form of the C2 statement available and it holds for every emit directory tested.

## Risks and residual gaps

- **Moving target.** The lane's tool file changed twice after the contract was frozen (see §5 table); a
  determinism statement recorded against one hash does not automatically cover a later hash.
- **Sample size and environment.** Five samples at the frozen revision and two at the working-tree snapshot, on
  one host with node v24.21.0 / CPython 3.15.0. No evidence for other node versions, other platforms, or a
  long time gap; the official-metrics numbers come from the vendored `mutation-testing-metrics` 3.9.0 running
  under node, so a node major-version change is the most likely external source of drift.
- **Dependency on retained git objects.** The legs are materialized from the sibling repos' object stores at
  pinned revisions (`REV_*`); if a sibling repo is garbage-collected or rewritten, the counter SETUPs (exit 2)
  rather than reporting a false PASS. Not observed here (all 8 legs replayed in every run).
- **Concurrent fleet edits.** Live sibling repos were being edited by other seats throughout; the emitted bytes
  did not move, because the replay reads pinned blobs. A future change that makes a leg read the working tree
  would reintroduce drift — the `PIN_*` check in §3 is what would catch it.
- **My verifier is a scratch script**, not a repo artifact; the checks it performs are reproducible from the
  commands quoted above, but the script itself lives in `/tmp` and will not survive the wave.

## Tooling record

No tools installed or upgraded (operator directive 2026-10-19). Everything used was preinstalled:
`uv 0.13.0` with the ephemeral `uv run --with jsonschema==4.25.1` environment (CPython 3.15.0), `node v24.21.0`,
`git`, `diff`/`cmp`/`sha256sum`. No pacman transaction was attempted (all pacman transactions are paused
host-wide). No global install was made.

## Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-25/w1/C2Determinism.md` — this report
  (the only file written inside the lane).

Scratch only, outside the repo: `/tmp/TameshiR25.C2Determinism-r25` (clone at `c9ff09f`),
`/tmp/TameshiR25.C2Determinism-r25b` (clone at `c9ff09f` carrying a snapshot of the working-tree tool),
`/tmp/TameshiR25.C2Determinism-{a,b,c,d,e,live1,live2}` (emit dirs), `/tmp/TameshiR25.C2Determinism-*.stdout`
(transcripts), `/tmp/TameshiR25.C2Determinism-verify.py` (independent verifier).
