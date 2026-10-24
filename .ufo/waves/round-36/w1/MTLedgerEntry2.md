# MTLedgerEntry2 — mutation probe: cold-read ledger refresh entry 2 (section 375)

Seat: mutation tester (leaf, no subagent dispatch). Round 36 wave 1, calibration axis (C1).
Everything below ran in a scratch clone of the lane; the lane, the fleet repo and every
sibling lane were read-only for this seat.

## Target

- Ledger: `.ufo/evidence/round-21/coldread/ledger.json` at lane tip
  `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`; the entry attacked is **index 494**, the
  second of the four entries the refresh commit `b455001e` appended:
  - `skill_sha256` = `sha256` = `13d489ad9898567f2f6620120fa819eee3251302caf502a4b04b782c8bdaabf8`
  - `start` 375, `end` 404, heading `## Restore discipline — before/after identity, not continuous non-write proof`
  - `read_rev` `e423c41ba253357ab8c8513f0376dad9d38ab248`, `commands_executed_count` 1
  - inputs `SKILL.md`, `corpus/README.md` (7c0fe513…), `tools/mutate-and-run.sh` (a7d3f2dd…)
  - traces `['.ufo/evidence/round-36/coldread/traces/L1/source-2.json']`
- Detector: `python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <REV>`
  (round-21 selector over the frozen round-18 measurement core; strict gate, no overrides).

## Scratch setup

```bash
git clone --no-hardlinks -q /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry2/lane
git -C /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry2/lane checkout -q --detach b455001e2589b3f4f471d94a3de7e5e549b9f54c
# one throwaway clone per mutant, each parent = b455001e2589b3f4f471d94a3de7e5e549b9f54c
```

Each mutant was committed in its own scratch clone only (scratch git objects, no lane ref
touched). The monitor reads the ledger **from the measured rev**, so a mutant needs its own
commit; the round-21 selector forbids `--ledger-file` / `--ledger-rev` / `--inputs-overlay`
(exit 64), so overriding the ledger was not available.

## Baselines (must pass before a mutant counts)

| run | rev | score | sections | gate | verbatim reason for section 375 |
|---|---|---|---|---|---|
| pristine refresh commit | `b455001e2589b3f4f471d94a3de7e5e549b9f54c` | **8** | **64/64** | strict | `credited` |
| reference control (content commit) | `e423c41ba253357ab8c8513f0376dad9d38ab248` | **6** | **60/64** | strict | `input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh` |

Both baselines reproduce the contract's before/after numbers, so the detectors are live and a
mutant failure is attributable.

Isolation of credit at section 375 (measured with the frozen core's own `entry_reason` at rev
`b455001e…`, same bytes): 16 ledger entries carry section sha `13d489ad…`; 15 older entries fail
`input-drift` (stale) and contribute nothing, **entry 494 is the only crediting entry** (`None`).
That is the load-bearing point the probe attacks.

## Mutants

Base for every mutant: `b455001e2589b3f4f471d94a3de7e5e549b9f54c`. Diffs are one line each
(`git diff --stat` = 1 file, 1 insertion / 1–2 deletions).

### M1 — point the entry's trace path at a nonexistent file

Mutant rev `90b6e0a775305593e22da6945b9e17407f5213ce`; ledger sha256
`1e258efa05e4c2be210d213cbf6b967f198cfbef2e90628ea3c86d6504824989` (pristine
`29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`).

```diff
-    ".ufo/evidence/round-36/coldread/traces/L1/source-2.json"
+    ".ufo/evidence/round-36/coldread/traces/L1/source-2-missing.json"
```

Command: `python3 .ufo/evidence/round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry2/mut-m1 --rev 90b6e0a775305593e22da6945b9e17407f5213ce`

Output (verbatim section reason; score 6, sections 63/64, gate strict, overrides false):

```
input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh;trace-missing:.ufo/evidence/round-36/coldread/traces/L1/source-2-missing.json
```

Isolated per-entry reason for entry 494 at that rev:
`trace-missing:.ufo/evidence/round-36/coldread/traces/L1/source-2-missing.json`

**Verdict M1: KILLED — expected `trace-missing` fired for the exact mutated path.** Section
375 loses credit (64→63), the top-line score falls 8→6, and the 15 stale entries do not
launder the failure.

### M2 — blank one path in the trace receipt's `inputs`, entry still lists it

Receipt `.ufo/evidence/round-36/coldread/traces/L1/source-2.json`, pristine sha256
`1e23a1ad6892cf2c5369aca1079d76b752520271c318a56fd8a61cda82482797`. `tools/mutate-and-run.sh`
is one of the two non-ignored entry inputs. Three readings of "blank one path" were run
because they land on different branches of the frozen `trace_reason` and only one of them
matches the stated expectation.

| variant | mutation | mutant rev | trace sha256 | isolated reason (entry 494) | score / sections | verdict |
|---|---|---|---|---|---|---|
| M2a | digest value blanked | `21423a22df1b0d470e21dae404419d079f8266e2` | `cdf60f48ec709279bf9ed5f811564e3c5a70c1173259c8cb4ec1c0e446283a40` | `trace-input-drift:tools/mutate-and-run.sh` | 6 / 63-64 | killed, **wrong reason** vs the stated expectation |
| M2b | key deleted | `7c298850d20855e2501228bd2544aeee7f2e1da4` | `24a2ffd5e88c416b7ebb86803c89f596091589e078138d4ff12fbe610203e336` | `None` (credited) | **8 / 64-64** | **SURVIVED** |
| M2c | path key blanked to `""` | `dde1dad131a7aca5081a44abc589180a47c48b7a` | `62d059cb912a0ce145d9b87b03a43d7729e7f5a66532f606acf3689a981a3509` | `trace-input-unrecorded:` | 6 / 63-64 | killed, reason has **no path identity** |

Command shape for all three:
`python3 .ufo/evidence/round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry2/mut-m2{a,b,c} --rev <mutant rev>`

Verbatim section reasons (each compound includes the 15 stale entries' input-drift tokens; the
`trace-*` token is the fresh entry's):

```
M2a: input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh;trace-input-drift:tools/mutate-and-run.sh
M2b: credited
M2c: input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh;trace-input-unrecorded:
```

Diffs (single line each):

```diff
M2a  -    "tools/mutate-and-run.sh": "a7d3f2dd…d912eb9"
     +    "tools/mutate-and-run.sh": ""
M2b  -    "corpus/README.md": "7c0fe513…82619f",
     -    "tools/mutate-and-run.sh": "a7d3f2dd…d912eb9"
     +    "corpus/README.md": "7c0fe513…82619f"
M2c  -    "tools/mutate-and-run.sh": "a7d3f2dd…d912eb9"
     +    "": "a7d3f2dd…d912eb9"
```

**Verdict M2: expectation only holds for the path-blanked reading (M2c, `trace-input-unrecorded`),
and there the reason string terminates at the colon with an empty path.** Blanking the digest
gives `trace-input-drift` (M2a), not `trace-input-unrecorded`; deleting the entry-listed key is
undetected (M2b). This is consistent with the detector's documented direction, not a contract
breach: `measure.py` docstring line ~66 says trace `inputs` must be "a subset of the entry's
inputs … (`trace-input-unrecorded:<p>` for a key absent from the entry; `trace-input-drift:<p>`
for a shared key with a different digest)", and the selftest `trace-input-unrecorded` case uses
an *extra* trace key (`corpus/SOURCES.md`). So the token can only ever name a key the entry does
**not** list; a receipt that records fewer files than its entry still credits. Recorded as a
coverage boundary of the trace gate, not as a violation of C1.

## Calibration notes

1. Entry 494 is the **sole** crediting entry for section 375 at `b455001e…`; all 15 older entries
   with the same section sha are stale `input-drift`. Any single-point failure in that entry
   costs the section and moves the score 8→6 and 64/64→63/64, i.e. one failed refresh entry
   consumes the entire claimed gain. The claim is therefore fully load-bearing on this entry,
   and the mutant proves the monitor is not merely echoing its own receipt.
2. The uncovered-section reason is a `;`-joined union over all matching entries, so the
   decisive `trace-*` token arrives after three stale `input-drift` tokens. The expected string
   is still findable verbatim, but receipts quoting the section reason will not lead with the
   trace token.
3. M2b shows the receipt can be *narrowed* without any detector firing: the entry's own input
   gate still verifies `tools/mutate-and-run.sh` against the rev blob (so the digest is not
   fabricated), but the trace no longer covers it and the trace gate stays silent by design.

## Restoration evidence

- Mutant clones restored to the base commit: `git -C mut-m* checkout -f b455001e…` —
  `git status --porcelain` empty in all four.
- Restored bytes for every mutant clone: ledger
  `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf` (3,489,570 bytes) and
  trace `1e23a1ad6892cf2c5369aca1079d76b752520271c318a56fd8a61cda82482797` (1,576 bytes) —
  identical to the pristine control clone and to the lane blobs
  (`b0522d3c…` / `4d9a4763…` at `d9c496b`).
- Lane untouched by this seat: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status
  --porcelain` shows only the untracked `.ufo/waves/round-36/w1/` report directory; lane HEAD
  still `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`; lane working-file sha256s equal the
  committed blobs (`29bddc03…`, `1e23a1ad…`).
- No file was written outside `/fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry2/` and this
  report.

## Tooling

None installed, no upgrades (pacman untouched per host pause; no `uv`/`npx`/binary fetch needed).
Scratch runs used the system `python3` and `git` only.

## Verdict

**Probe 1 (nonexistent trace path): KILLED as expected — `trace-missing:<mutated path>`, entry
credit lost, 8→6 / 64→63. Probe 2 (blank a trace input path): partially as expected — the
literal path-blank kills with `trace-input-unrecorded:` (empty path), digest-blank kills with
`trace-input-drift:tools/mutate-and-run.sh` instead of the expected token, and deleting the
entry-listed key SURVIVES at 8 / 64-64 under the documented subset direction (coverage
boundary of the trace gate, not a C1 breach).** Refresh entry 2 is load-bearing and detectable;
its receipts cannot be narrowed silently only because nothing asks them to be complete.
