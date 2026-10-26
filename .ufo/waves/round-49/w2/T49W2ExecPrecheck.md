# T49W2ExecPrecheck — QUALITY 98 precheck + round-49 no-harm at `f181a961`

Seat item: run the round-48 cold-read precheck and the round-49 no-harm monitors on the candidate
`f181a961ae44061af486f600e5ea257d2baf78f8` (floor `8ca67421111fa354b47b803358391d0b07fc6db9`), copy both
outputs into `.ufo/waves/round-49/w2/T49W2ExecPrecheck.*.stdout`, and report every RED line. I am a seat:
nothing here is a verdict on C1 or C2, and no counter was invoked (bounds: counters only as `--selftest`,
`--list`, or against scratch trees). Lane writes: this report plus the receipts named below, only.

Scratch: `S=/fast/scratch/hyaku/tameshi-r49/T49W2ExecPrecheck` (one `git clone --shared` of the lane for the
direct-monitor re-run), `TMPDIR=$S`, `HYAKU_SCRATCH=$S` so the precheck's own temporary dirs stayed inside the
seat root; scratch deleted before yielding.

## 1. Item result — both monitors, zero RED

**Command 1 (exact):**

```
S=/fast/scratch/hyaku/tameshi-r49/T49W2ExecPrecheck; export HYAKU_SCRATCH=$S TMPDIR=$S; cd "$S"
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/quality/coldread-precheck.sh \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  8ca67421111fa354b47b803358391d0b07fc6db9 f181a961ae44061af486f600e5ea257d2baf78f8
```

Observed, exit `0`, stderr empty (receipt `.ufo/waves/round-49/w2/T49W2ExecPrecheck.coldread-precheck.stdout`):

```
COLDREAD_PRECHECK floor=8ca67421111f floor_credited=57 cand=f181a961ae44 cand_credited=64 lost=0 ok
```

No `LOST ...` line was printed, so no credited section lapsed and no drift path is named.

**Command 2 (exact):**

```
S=/fast/scratch/hyaku/tameshi-r49/T49W2ExecPrecheck; export TMPDIR=$S; cd "$S"
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-49/no-harm.sh \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin f181a961ae44061af486f600e5ea257d2baf78f8
```

Observed, exit `0`, stderr empty (receipt `.ufo/waves/round-49/w2/T49W2ExecPrecheck.no-harm.stdout`):

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-128 130 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [A:tools/pbt-staged-id.py ] ok
```

**RED lines: none.** All nine monitors printed `ok`; the precheck printed `ok` with `lost=0`.

## 2. The monitors I ran are the frozen bytes, and they bind to the candidate

- `.ufo/evidence/round-49/freeze.json` `sha256[".ufo/evidence/round-49/no-harm.sh"]` =
  `edcf04c7495e22ace7b4bed8d9bd5d0fc69387f8b7e7aa358fa0c06abea9dac1`; freeze's
  `sha256[".ufo/evidence/round-48/quality/coldread-precheck.sh"]` =
  `3b07847afc86d0d6c14d2e6c20a6b3778da1798d9304204ec3a360a6301b2924`.
- Command: `sha256sum .ufo/evidence/round-49/no-harm.sh .ufo/evidence/round-48/quality/coldread-precheck.sh`
  in the lane → those two digests exactly. Same command over `git show <rev>:<path> | sha256sum` at
  `f181a96…` → the same two digests, so the working-tree scripts the two commands executed are the candidate
  blobs, not drifted copies (`git status --porcelain -- <both paths>` printed nothing, rc 0).
- `git cat-file -e 8ca67421:.ufo/evidence/round-49/no-harm.sh` → `fatal: path … exists on disk, but not in
  '8ca67421111fa354b47b803358391d0b07fc6db9'` (rc 128): the no-harm script is new this round, as its header
  (`.ufo/evidence/round-49/no-harm.sh:2-7`) states; the precheck is byte-identical at base
  (`3b07847a…` at `8ca67421` too), so the QUALITY 98 script is the round-48 one unmodified.

## 3. Criterion 98 passed for the right reason: base→candidate credit of the seven C1 headings

The precheck compares only the set of `credited` sections of the round-21 monitor. I re-derived the per-section
detail in a scratch clone (`git clone --shared` of the lane, `git -C "$S/clone" rev-parse --show-toplevel`
printed `/fast/scratch/hyaku/tameshi-r49/T49W2ExecPrecheck/clone`), running
`.ufo/evidence/round-21/coldread/measure.py --repo "$S/clone" --rev <rev>` for both revs (rc 0 both, empty
stderr, 255 565 B and 243 256 B of JSON). Receipt:
`.ufo/waves/round-49/w2/T49W2ExecPrecheck.coldread-sections.json`.

| heading (contract `targets_frozen`) | at base | at candidate |
|---|---|---|
| `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | `credited=False`, reason `input-drift:LOG.md;…SCORECARD.md;…corpus/QUALITY.md;…corpus/README.md;…corpus/SOURCES.md` | `credited=True` |
| `## Restore discipline — before/after identity, not continuous non-write proof` | `credited=False`, `input-drift:corpus/README.md;…tools/mutate-and-run.sh` | `credited=True` |
| `### The map — where a reader enters, artifact by artifact` | `credited=False`, `input-drift:corpus/README.md;…corpus/knowledge/closeout-r11.md;…` | `credited=True` |
| `## Promotion-evidence calibration — fleet round-1` | `credited=False`, `input-drift:reports/round-1-calibration.md` | `credited=True` |
| `## Repeated controls and gate registry — round 12` | `credited=False`, `input-drift:corpus/SOURCES.md;…corpus/knowledge/repeated-control-precondition.md;…` | `credited=True` |
| `## Pin disposition and provenance correction — round 13` | `credited=False`, `input-drift:.ufo/evidence/round-17/coldread/assemble.py;…corpus/knowledge/incremental-pin-disposition.md` | `credited=True` |
| `## Effective expectation reconciliation — round 14` | `credited=False`, `input-drift:.ufo/evidence/round-14/context-missing-env.json;…corpus/SOURCES.md;…` | `credited=True` |

Aggregates: base `score=6 covered=57/64`; candidate `score=8 covered=64/64`. This matches the contract's
`axes_at_base.calibration` (6, 57/64) and C1 `target` (score 8, all credited). The seven heading strings in
`.ufo/evidence/round-49/contract.json` `targets_frozen` match the monitor's headings verbatim (no row was
`MISSING-HEADING`), so no heading text was silently rewritten to earn credit.

## 4. No-harm monitors: what each line actually shows (and where it cannot see)

- `.ufo/evidence/round-49/no-harm.sh:10-11` commandD: `recorded_cases=9 depth_score=9 ok` — depth not raised.
- `.ufo/evidence/round-49/no-harm.sh:12-13` cold-read **floor**: the predicate is
  `int(s["score"])>=6 and int(s["credited"])>=57`. Observed `score=8 credited=64`, so the C1 target value is
  actually present, but this line alone would also print `ok` at exactly 6/57 — it is a floor by design
  (header `.ufo/evidence/round-49/no-harm.sh:3-5`) and is not the place where the C1 target is checked.
- `.ufo/evidence/round-49/no-harm.sh:14-15` freshness `population=73 fresh=71 C1_R45_PASS=true ok`;
  `:16-17` r45 coverage `rows=2 entries=2`; `:18-19` `S160-count 1`; `:20-21` `registry-rows-not-below-128 130`
  (130 ≥ 128); `:22-23` r46 `rows=3 entries=3`; `:24-25` r47 `rows=3 entries=3`. All at their expected values.
- `.ufo/evidence/round-49/no-harm.sh:26-27` tools scope: `git diff --name-status --no-renames $BASE $REV -- tools`
  → the single line `A:tools/pbt-staged-id.py`, which is the only value the `case` at `:27` accepts. Verified
  independently: `git diff --name-status --no-renames 8ca67421 f181a961 -- tools` printed exactly
  `A	tools/pbt-staged-id.py`; `git ls-tree -r --name-only f181a961 -- tools | wc -l` = 32; the pinned
  `tools/staged-id-guard.py` at the candidate hashes `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`,
  equal to the contract's `named_gate` digest. Any `M`/`R`/`D` under `tools/` would have matched none of the two
  accepted strings and gone RED, so the monitor does cover the pinned-tool case.

## 5. Calibration findings — monitor weaknesses, none triggered here

**F1 (real, latent): the precheck's `ok`/`RED` state is cardinality, not loss.** `.ufo/evidence/round-48/quality/coldread-precheck.sh:22` computes `lost = fc - cc`, `:23-26` prints one `LOST` line per lost
heading, but `:27` decides `state = 'RED' if len(cc) < len(fc) else 'ok'`. A candidate that loses a credited
heading while gaining at least as many prints `LOST …` and still exits 0 with `ok`, so a gate consuming only the
exit code (or only the last word) would accept a lapse. Demonstrated with the script's exact lines 22-27 logic on
synthetic section lists in scratch (receipt `.ufo/waves/round-49/w2/T49W2ExecPrecheck.classifier-probe.txt`):

```
-- case: 1 lost, 2 gained
LOST C | drifted=corpus/SOURCES.md
COLDREAD_PRECHECK floor=x floor_credited=3 cand=y cand_credited=4 lost=1 ok
-- case: 1 lost, 1 gained (swap)
LOST C | drifted=corpus/QUALITY.md
COLDREAD_PRECHECK floor=x floor_credited=3 cand=y cand_credited=3 lost=1 ok
-- case: 2 lost, 0 gained
LOST B | drifted=corpus/README.md
LOST C | drifted=corpus/SOURCES.md
COLDREAD_PRECHECK floor=x floor_credited=3 cand=y cand_credited=1 lost=2 RED
PROBE lost_one_gained_two=ok
PROBE swap_equal_count=ok
PROBE pure_loss=RED
```

Not triggered at this candidate: the observed run printed `lost=0` with no `LOST` line and `cand_credited=64`
≥ `floor_credited=57`. Criterion 98 therefore holds at `f181a961`; the weakness is that the exit code alone is a
weaker certificate than "no section lost credit". I did not edit the script (round-48 frozen bytes, lane
read-only for this seat); the minimal fix is to decide on `len(lost)==0` instead of the count comparison at `:27`.

**F2 (latent): the precheck ignores the calibration score.** It compares only `credited` flags (`:19-27`), so a
candidate keeping 57 credited headings with score dropped below the base 6 would still print `ok`. `no-harm.sh:13`
adds a floor (`score>=6`) but no monitor in my item can see the C1 target of **8**; that value is only visible in
the C1 deciding run. Observed value here is 8/64, so no gap at this candidate.

**F3 (hygiene): the precheck discards the monitor's stderr** (`2>/dev/null` at `:14-15`), so a monitor that
warned and still exited 0 would be invisible. I re-ran the same monitor directly in the scratch clone: both
invocations rc 0, stderr files 0 bytes, JSON 255 565 B / 243 256 B — nothing was suppressed in this run.

## 6. Cross-checks recorded

- `git merge-base --is-ancestor 8ca67421… f181a961…` → `ancestor=yes` (the candidate is a descendant of the
  floor the precheck compares against, so `floor_credited=57` is the base value from the contract).
- Base has no `.ufo/evidence/round-49/no-harm.sh` (rc 128 above); the round-49 monitor is new, consistent with
  the contract's `no_harm.monitors`.
- Peer IRC from `SentTool-3` arrived mid-run about round-46 clause-r sandboxing; out of scope for this item
  (no device sandbox or hyprctl harness is involved in either monitor I ran) and not acted on.

## 7. Risks / blockers

- **R1**: precheck F1 is a real false-`ok` path; at this candidate it is not exercised (`lost=0`), so milestone
  "QUALITY 98 precheck" is met on observed output.
- **R2**: the durability half of C1's predicate (one appended line per record file must not lapse the seven
  sections) is outside criterion 98 and deliberately outside no-harm (criterion 88); I did not measure it —
  bounds allow counters only via `--selftest`/`--list`/scratch trees, and the deciding run is the L1's.
- **Blockers: none.**
- Tooling: nothing installed or upgraded (host pacman paused; no uv/npx/`~/.local/bin` writes); both commands
  ran under the host's stock `bash`/`python3`, and the seat scratch tree was deleted before yielding.

## Files written

- `.ufo/waves/round-49/w2/T49W2ExecPrecheck.md` (this report)
- `.ufo/waves/round-49/w2/T49W2ExecPrecheck.coldread-precheck.stdout` / `.coldread-precheck.stderr`
- `.ufo/waves/round-49/w2/T49W2ExecPrecheck.no-harm.stdout` / `.no-harm.stderr`
- `.ufo/waves/round-49/w2/T49W2ExecPrecheck.coldread-sections.json` (base→candidate credit of the seven headings)
- `.ufo/waves/round-49/w2/T49W2ExecPrecheck.classifier-probe.txt` (F1 demonstration)

## Summary
1. QUALITY 98 precheck at `f181a961`: exit 0, `floor_credited=57 cand_credited=64 lost=0 ok` — no lapse, no RED.
2. Round-49 no-harm at `f181a961`: exit 0, nine monitors all `ok` (commandD 9, coldread 8/64, freshness 73/71, r45/r46/r47 coverages, S160, registry 130, tools-scope `A:tools/pbt-staged-id.py`) — no RED.
3. Both scripts hashed equal to `freeze.json` digests and to the candidate blobs; precheck byte-identical at base, so the round-48 script was used unmodified.
4. All seven contract target headings are uncredited at base (input-drift on the five record files and cited tools) and credited at candidate; score 6→8, 57/64→64/64.
5. Latent F1: `coldread-precheck.sh:27` decides `ok`/`RED` on credited-set cardinality, so one lost heading plus two gained prints `ok` (probe receipt included); not exercised here (`lost=0`).
6. Latent F2: the precheck never compares the calibration score, and no-harm's cold-read line is a floor at 6, so only the C1 deciding run can see the target 8 — observed 8 here.
7. Hygiene F3: `2>/dev/null` at `coldread-precheck.sh:14-15` hides monitor stderr; direct scratch-clone re-run gave rc 0 and empty stderr both revs.
8. No blockers; durability (record-append) half of C1 is outside this item and left to the L1's deciding run.
