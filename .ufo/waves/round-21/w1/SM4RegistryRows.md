# SM4RegistryRows — `tools/registry.json` YAGNI review (read-only)

**Verdict:** done (proposal-only; no lane edits)

**Revision reviewed:** `33d03b716d3edcf1d8656d46d6df61801d232c52` (frozen base)  
**Registry:** `tools/registry.json` — schema `tameshi-entry-registry-v1`, **40 rows**, sha256 `05ec47e016bfdbf090553dc8495dfa8aed4e835ea99391115cc1f1865bb407fb`

## Axes (godspeed)

| Axis | Question this review asks |
|---|---|
| **Operability** (primary) | Does every row earn its slot in `registry-check` runs (baseline tag, full battery, wall time)? |
| **Monitor clarity** | Do superseded rows still *run* without misleading `expect`/`got` lines? |
| **Provenance** | Are receipt-cited row names preserved? |
| **Schema weight** | Are there duplicate `argv` vectors that double-run the same command? |

## Inventory

| Metric | Value | Citation |
|---|---|---|
| Active rows | 36 | ```252:277:tools/registry.json``` … ```844:853:tools/registry.json``` |
| Superseded rows | 4 | ```218:222:tools/registry.json```, ```245:249:tools/registry.json```, ```322:326:tools/registry.json```, ```671:675:tools/registry.json``` |
| `baseline`-tagged | 25 (includes 2 superseded disposition rows) | tags on rows ```19:21:tools/registry.json```, ```219:221:tools/registry.json```, ```324:326:tools/registry.json``` |

## Finding 1 — Exact duplicate `argv` rows

**None.** Programmatic scan: 40 unique `argv` lists (byte-identical JSON serialization). `registry-check.py` validates unique `name` only, not `argv` deduplication (```206:206:tools/registry-check.py```; no argv-duplicate lint).

## Finding 2 — Superseded rows still carried (intentional contract)

Superseded rows **must remain** and **still execute**; they are excluded from `held=N/M` but counted in `superseded=K` (```30:35:tools/registry-check.py```, ```874:880:tools/registry-check.py```). SKILL matches: a row leaves `active` only as `superseded` with `superseded_by`, and still runs (```1829:1829:SKILL.md```).

| Row | `superseded_by` | Tags | Stale `expect` vs current tool (at `33d03b7`) |
|---|---|---|---|
| `evidence-disposition-round17` | `evidence-disposition-round18` | `baseline` | expect `0`, observed `2` (round-17 manifest now refused) ```197:222:tools/registry.json``` |
| `evidence-disposition-round17-before` | `evidence-disposition-round18-before` | `new-r17` | expect `1`, observed `2` ```225:249:tools/registry.json``` |
| `evidence-disposition-round14-superseded` | `evidence-disposition-round18` | `baseline` | expect `0`, observed `2` ```306:326:tools/registry.json``` |
| `trace-inputs-round17-selftest` | `trace-inputs-selftest` | `new-r17` | expect `0`, observed `0` (held) ```656:675:tools/registry.json``` |

Round-18 SKILL already documents that round-17 disposition recipes **exit 2** on current tooling (```1835:1836:SKILL.md```). Round-20 full-battery stderr records the three disposition superseded mismatches (```10:14:.ufo/evidence/round-20/final/registry-complete.stderr```); `registered-effective.json` marks those three `held: false` while excluding them from active totals (```93:136:.ufo/evidence/round-20/final/registered-effective.json```).

**Fan-in:** two superseded disposition rows point at the same active successor (`evidence-disposition-round18`) — ```222:222:tools/registry.json``` and ```323:323:tools/registry.json```. That is two historical manifests, not duplicate argv.

## Finding 3 — Structural argv families (not duplicates, operability cost)

Same *shape* (`python3 …/measure.py --selftest`, `…/assemble.py --selftest`, `…/evidence-disposition.py … dispositions.json --json`), different paths — each pins a **round-frozen** instrument, so YAGNI does **not** recommend merging or deleting.

Examples:

- Measure selftests: ```508:526:tools/registry.json```, ```635:653:tools/registry.json```, ```720:738:tools/registry.json```, ```783:801:tools/registry.json```, plus ```835:842:tools/registry.json``` (`receipt-measure-selftest`).
- Assemble selftests: ```529:547:tools/registry.json```, ```678:696:tools/registry.json```, ```741:759:tools/registry.json```.
- Cold-read selector selftests: ```804:822:tools/registry.json```, ```845:852:tools/registry.json```.
- Trace successor pair (different argv): round-17 evidence copy ```658:661:tools/registry.json``` vs promoted tool ```701:704:tools/registry.json```; SKILL keeps the round-17 path as historical evidence (```1933:1933:SKILL.md```).

## Finding 4 — Receipt-cited rows (do not remove)

Explicit `registry_row` in committed receipts:

- `receipt-window-selftest` — ```60:60:.ufo/evidence/round-20/final/receipts.json```

No other `registry_row` fields under `.ufo/evidence/**/receipt*.json` in this repo snapshot. **Proposal constraint:** never delete or rename rows receipts cite; superseded rows may only be re-pinned, not dropped.

Cold-read / registry-complete artifacts **name** all four superseded rows as observed rows (e.g. ```273:279:.ufo/evidence/round-20/final/registered-effective.json```) — treat as historical observation keys, not deletion candidates.

## Finding 5 — Baseline operability at frozen rev

Command (scratch clone, no lane mutation):

```bash
W=$(mktemp -d /tmp/tameshi-r21-sm4c-XXXXXX)
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin "$W/fleet/tameshi-shokunin"
git -C "$W/fleet/tameshi-shokunin" checkout -q --detach 33d03b716d3edcf1d8656d46d6df61801d232c52
python3 "$W/fleet/tameshi-shokunin/tools/registry-check.py" \
  --rev 33d03b716d3edcf1d8656d46d6df61801d232c52 --tag baseline
```

- **Exit code:** `1` (one active baseline row differs).
- **Trailer:** `REGISTRY_CHECK: held=22/23 superseded=2`
- **Differing active row:** `mutate-and-run-regression` — expect `0`, got `2` (```462:480:tools/registry.json```). Separate from superseded-row YAGNI; blocks a green `--tag baseline` at this rev.

Superseded baseline rows still run (`superseded=2` in baseline filter: `evidence-disposition-round17`, `evidence-disposition-round14-superseded`).

## Proposals (operability-first, no deletions)

| # | Proposal | Improves | Harms | Receipt-safe |
|---|---|---|---|---|
| P1 | **Re-pin** the three superseded **disposition** rows: set `expect.exit` to `2`, drop or replace `stdout_contains` with a stable “manifest superseded” needle if one exists in stderr/stdout at exit 2. Keeps rows and `superseded_by` edges; aligns monitor lines with ```1835:1836:SKILL.md``` and round-20 observations. | Monitor clarity, operability log signal | None if pins match live tool | Yes — rows retained |
| P2 | **Do not remove** any of the four superseded rows; contract requires execution (```30:35:tools/registry-check.py```). | Provenance | Would break supersession chain validation (```277:297:tools/registry-check.py```) | Yes |
| P3 | **Do not merge** round-N `measure.py` / `assemble.py` / `coldread/measure.py` selftest rows — argv differs by frozen evidence path; not duplicate authority. | — | Would collapse round-specific guards | Yes |
| P4 | **Optional schema lint** (future): warn on identical `argv` across two `name`s or two **active** rows sharing `argv` — today absent; would catch true duplicates early. | Operability | Small implementation cost | N/A |
| P5 | **Investigate** `mutate-and-run-regression` at `33d03b7` (baseline `22/23`) — out of scope for registry row deletion, but it is the active baseline failure at frozen base. | Operability | — | N/A |

**Explicit non-proposals:** Removing `baseline` from superseded disposition rows would change the C2 grading denominator documented in SCORECARD (```609:609:SCORECARD.md```) — defer unless L1 replays all historical `--tag baseline` evidence.

## Tooling / installs

No packages installed this seat.

## Disagreements / defects

- None with registry schema vs `registry-check.py` docstring.
- **Note:** Piping `registry-check` to `grep` reports `grep`’s exit code, not the checker’s; use a file redirect when capturing exit codes.

## Evidence paths

- Review target: `tools/registry.json`
- Operability run: `/tmp/tameshi-r21-sm4c-*/` (ephemeral clone; command above)
- Receipt citation: `.ufo/evidence/round-20/final/receipts.json`
- Round-20 full battery: `.ufo/evidence/round-20/final/registry-complete.stderr`, `registered-effective.json`
