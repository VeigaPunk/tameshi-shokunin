# T54W1ConnPreBind — cross-claim pre-bind map

Axes: **calibration**, **adjacency**.
C0: `59c38109bf119d0e9d4f878644a82babc937bc1e`.
Method: for each of the 23 headings in `.ufo/evidence/round-54/c1/lost-headings-at-c0.json`, run `reader-section.py` at C0, then substring-search the `git show C0:SKILL.md` lines `start..end`. A path is a section pin only if it occurs byte-exact in that span. Companion: `T54W1ConnPreBind.json`. Receipts: `T54W1ConnPreBind-receipts/`.

C0-edited surfaces checked: `tools/env-diff.py`, `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry.json`.
L1-still-write checked: `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-54.md`.
C1 counter unstable inputs (measure.py): `LOG.md`, `SCORECARD.md` only.

## Binder rule (apply on every `rekey-r54-<c0>` entry)

1. **Pin at C0** — `read_rev` is C0; every `inputs` digest is `git show C0:<path>` (or omit the path).
2. **Drop unstable / L1-still-write paths** — never put `LOG.md` or `SCORECARD.md` in `inputs` (C1 arm fails otherwise). Also never put `corpus/lessons/round-54.md` in `inputs`: L1 still writes it after the rekey bind, and none of the 23 sections cite it.
3. **Never fabricate an input** — admissible pins are only paths the C0 section body byte-cites (or that the bound cold-read actually opened for that heading). Do **not** union historical `.ufo/evidence/round-21/coldread/ledger.json` `inputs` for the same heading; those unions drag in C0 tools and LOG/SCORECARD the live section does not name.
4. **C0-tool cites stay** — if the section body names one of the four edited tools or `tools/registry.json`, pin that path at C0. Omitting it to avoid C2 adjacency fabricates a thinner input set and harms calibration.

## Map (23 headings)

Legend: `base7` = also in `lost-headings-at-base.json` (arm-3 rekey set). `c0_pins` / `l1_pins` = section-body pins only.

| heading | base7 | c0_pins (section body) | l1_pins |
|---|---|---|---|
| `## Standing rules` | yes | *(none literal)* — soft: registry `scratch_root` cells | none |
| `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | yes | none | none |
| `### The boundaries — what a service run is not` | yes | none | none |
| `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | no | none | none |
| `### Using the ledger` | yes | none | none |
| `### The tick and the pin read` | no | none | none |
| `### Triggers T1–T3 and the re-pin rule` | no | none | none |
| `### The service's limits — what tameshi refuses to mutation-test` | no | none | none |
| `## The operator's runbook and the six-leg regression (round 10, measured)` | no | none | none |
| `### The operator's runbook — \`corpus/knowledge/operator-runbook.md\`` | yes | none | none |
| `## Repeated controls and gate registry — round 12` | no | none | none |
| `### Gate/probe registry` | no | `tools/bash-witness-study.py` | none |
| `## Pin disposition and provenance correction — round 13` | no | `tools/pin-disposition.py` | none |
| `### Round-13 gate/probe registry` | no | `tools/pin-disposition.py` | none |
| `## Effective expectation reconciliation — round 14` | no | `tools/evidence-disposition.py`, `tools/pin-disposition.py` | none |
| `### Round-14 historical registry — superseded by round 15` | yes | `tools/evidence-disposition.py` | none |
| `## Context gate classification and explicit exit classes — round 15` | no | none | none |
| `### Round-15 gate/probe registry` | no | `tools/evidence-disposition.py` | none |
| `## Live-tree re-pin and entry-command monitor — round 17` | no | `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry.json` | none |
| `### Round-17 gate/probe registry — re-pin and monitor` | no | `tools/evidence-disposition.py`, `tools/pin-disposition.py` | none |
| `### Round-18 gate/probe registry — routed-defect closure` | no | `tools/bash-witness-study.py`, `tools/evidence-disposition.py` | none |
| `### Round-21 gate/probe registry — finite environment differential` | no | `tools/env-diff.py` | none |
| `### Round-26 gate/probe registry — report interop` | yes | all four tools + `tools/registry.json` | none |

Counts: **11/23** section-body-pin at least one C0-edited tool or `tools/registry.json`. **0/23** section-body-pin `LOG.md`, `SCORECARD.md`, or `corpus/lessons/round-54.md`.

Per-tool (section-body only):

- `tools/bash-witness-study.py`: Gate/probe registry; Round-18 registry; Round-26 registry.
- `tools/pin-disposition.py`: Pin disposition (r13); Round-13 registry; Effective expectation (r14); Live-tree (r17); Round-17 registry; Round-26 registry.
- `tools/evidence-disposition.py`: Effective expectation (r14); Round-14 historical registry; Round-15 registry; Live-tree (r17); Round-17 registry; Round-18 registry; Round-26 registry.
- `tools/env-diff.py`: Round-21 registry; Round-26 registry.
- `tools/registry.json`: Live-tree (r17); Round-26 registry.

## Ambiguity (one defended reading)

**`## Standing rules`** — C0 added the three-arm scratch-root bullet. The span cites `corpus/knowledge/scratch-root-contract.md` and the soft phrase "seven tools and their registry `scratch_root` cells", but **not** the literal path `tools/registry.json` and **not** any of the four edited tool paths.

Defended reading: **do not** pin `tools/registry.json` or the four tools from that soft phrase (rule 3, never fabricate). **Do** pin `corpus/knowledge/scratch-root-contract.md`. **Drop** any inherited `LOG.md` / `SCORECARD.md` if a binder starts from an old ledger row (historical Standing-rules / Mutation-sweep entries still carry those keys; they are not in the C0 section body).

No other heading among the 23 is ambiguous on this map: either the path string is present in the C0 span, or it is not. Historical ledger unions that list C0 tools for headings whose C0 body does not name them are **not** pins for rekey — they are fabrication risk.

## Evidence / verification

```
$ python3 .ufo/waves/round-54/reader-section.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    59c38109bf119d0e9d4f878644a82babc937bc1e \
    "## Standing rules"
{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 17, "end": 40, "section_sha256": "164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7"}
```

Standing-rules C0 lines 21–22 (byte-exact):
`corpus/knowledge/scratch-root-contract.md; the seven tools and their registry \`scratch_root\` cells, measured by the round-54 C2 counter).`

Sweep TSV: `T54W1ConnPreBind-receipts/section-pin-sweep.tsv`.
C1 measure.py: `UNSTABLE_INPUTS = ('LOG.md', 'SCORECARD.md')` (stable arm rejects rekey entries that pin those).

## Affected axes / move / risks

- **Calibration:** binder pins only C0-stable, section-justified inputs → rekey entries can credit without LOGINPUT failure.
- **Adjacency:** C2’s C0 tool edits are named as pins where the prose already requires them (at C0), and are not invented for Standing rules; L1-writable lesson/LOG/SCORECARD stay out of inputs.
- **Risk:** a binder that copies historical ledger `inputs` for Standing rules or Mutation-sweep will reintroduce `LOG.md`/`SCORECARD.md` and fail the stable arm; a binder that upgrades Standing rules’ soft registry wording into `tools/registry.json` fabricates an input.
- **Verification the L1/binder should run:** after rekey bind, `python3 .ufo/evidence/round-54/c1/measure.py --lane … --rev REV --work EMPTY --explain` shows rekeyed=7 (base7) and no unstable notes; spot-check each of the 11 c0-pin headings has those paths in `inputs` hashed at C0; Standing rules `inputs` lacks `tools/registry.json` unless a real open of that file is disclosed in the bound wave read.

## Tools

No installs this seat (pacman paused; unused).

Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1ConnPreBind/` — removed on seat exit.
