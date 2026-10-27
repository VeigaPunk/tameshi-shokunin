# T51ScribeEntry — C2 case entry for the tenth mutation case (round 51, w1)

Seat: T51ScribeEntry (UFO-FSD scribe, leaf — no subagent dispatch).
Item: draft the tenth case's knowledge entry for kagi `corpus/drift-pins.sh` @
`e64e81b8eb96f3682b00c1e7a291e84420b280fa`, plus the README coverage-map row.
Deliverable: `.ufo/waves/round-51/w1/T51ScribeEntry.mutation-case-kagi-drift-pins.md`
(the L1 copies it to `corpus/knowledge/mutation-case-kagi-drift-pins.md`).

Nothing here decides C2. The counters were not run against the lane; every
number below is either read from the frozen receipts or produced by a seat probe
in scratch and copied into `.ufo/waves/round-51/w1/T51ScribeEntry/`.

## 1. What the entry asserts, and where each fact comes from

| Entry assertion | Command that shows it | Observed |
|---|---|---|
| pin = the pinned bytes, blob unchanged at kagi HEAD | `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8…:corpus/drift-pins.sh \| sha256sum`; `git -C … show HEAD:corpus/drift-pins.sh \| sha256sum` | both `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`; 451 lines, 19,088 bytes; `git ls-tree` = `100755 blob 8a2903dc…`; kagi HEAD `69b61db` |
| spec pre-registered before the sweep, spec bytes unchanged by amendment 1 | `git log -1 --format='%H %cI' -- .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; `sha256sum` of the spec; `cmp` with `sweep/spec.copy` | added in `fe335384…` at `2026-10-26T20:52:43-03:00` (23:52:43Z); `sweep/sweep.txt:2` stamps `MUTATE_DATE: 2026-10-26T23:53:02Z` (19 s later); sha `a98271f6…` = the counter's `SPEC_SHA`; `spec.copy` byte-identical; amendment `84aa673…` at 23:54:18Z touched no spec byte |
| 2/10 killed, 8 survived, 0 inconclusive | `.ufo/evidence/round-51/c2/sweep/sweep.txt:31` | `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` |
| the recorded table reproduces under the guarded suite | seat sweep, same target bytes + frozen spec + `sandbox-$DEFECT_ID` suite | identical verdict map: `KILLED K_MODE_CMP, K_COUNT_GE`; 8 `SURVIVED`; `CONTROL: GREEN`; `MUTATE_RESTORE: OK` (`w1/T51ScribeEntry/sweep-id.txt`, `results.tsv`) |
| 7/10 predictions held | spec `# PREDICT` lines vs `results.tsv` | 5/5 hole-aimed held; 2/5 kill-aimed held (misses: K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN) |
| five survivors are holes, none equivalent | peer witness reports + this seat's S_DUP_UNIQ witness | see §3 |

## 2. The harness finding (probe-grade, marked so in the entry)

Mechanism, from the pinned bytes only:

- the gate prints fixture paths on every verdict line
  (`corpus/drift-pins.sh:158` `printf 'DRIFT   %s %s\n' "$p" …`), and the
  selftest's scratch dir honours `TMPDIR` (`:376` `d=$(mktemp -d)`);
- each selftest case asserts one **unanchored** word over combined
  stdout+stderr: `corpus/drift-pins.sh:403` `elif ! grep -q "$3" <<< "$out"`;
- the guarded suite that ran the sweep puts the defect id into the path it
  prints: `h="$WORKDIR/sandbox-$DEFECT_ID" … TMPDIR="$h/tmp"`
  (`tools/mutate-and-run.sh:1418` is the same form for the three js legs).

So for K_GONE_ARM, K_AMBIG_GT and K_SHAPE_OPTIN the path
`…/sandbox-<DEFECT_ID>/tmp/tmp.XXXX/…` satisfies the word assertion.

Seat probes (receipts `w1/T51ScribeEntry/`, script `case-probe.sh`; fixture
rebuilt from `corpus/drift-pins.sh:379-396`, run against the sweep's own mutant
bytes from `$S/w-id/mutant-<id>.target.sh`):

| defect | case | id-bearing sandbox | neutral sandbox |
|---|---|---|---|
| K_GONE_ARM | `symbol gone` (`:423`) | exit 1, out `DRIFT …/sandbox-K_GONE_ARM/tmp/tmp.XXXX/b.txt sha 2c8b08da5ce6->d9f86d34b0b0`, `grep -q GONE` = YES | same output, `grep -q GONE` = NO |
| K_AMBIG_GT | `symbol ambiguous` (`:426`) | exit 1, out `DRIFT …/sandbox-K_AMBIG_GT/…/b.txt lines 1->2 sha …`, `DRIFT_PINS: DRIFT (… symbols_ok=4 symbols_bad=0)`, `grep -q AMBIG` = YES | same, `grep -q AMBIG` = NO |
| K_SHAPE_OPTIN | `shape drift` (`:436`) | exit 1, out `DRIFT …/sandbox-K_SHAPE_OPTIN/…/env.txt lines 2->3`, `symbols_ok=4 symbols_bad=0`, `grep -q SHAPE` = YES | same, `grep -q SHAPE` = NO |

`case-probe.txt` (46 lines) holds all six blocks; the gate's own bytes are never
edited (probe copies only).

Whole-sweep counter-run with the sandbox renamed `sandbox-box` (same target,
same suite, same spec): **5/10 KILLED** — `K_MODE_CMP`, `K_GONE_ARM`,
`K_AMBIG_GT`, `K_COUNT_GE`, `K_SHAPE_OPTIN`; `CONTROL: GREEN`; `MUTATE_RESTORE:
OK` (`w1/T51ScribeEntry/sweep-neutral.txt`, `results-neutral.tsv`), and the
three cases fail on the missing word (`neutral-K_*.out`).

Standing: the mechanism is the L1's pre-wave probe; this seat reproduced it end
to end, but the named confirmation seat `T51LabSandboxLeak` had not published at
drafting time. The entry marks the finding probe-grade and states exactly which
text changes if confirmation fails (§3's three "harness artifact" rows; §0-§2
and the table are measurements).

## 3. Survivor composition (the entry's §3)

| survivor | status | evidence |
|---|---|---|
| K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN | harness artifact (suite does assert the arm) | §2 above |
| S_SHA_CMP | hole | `w1/T51LabWitSHACMP.md` (pristine exit 1 `DRIFT … sha e49c81e2d2f8->69726aa46966`, mutant exit 0 CLEAN) |
| S_HARDLINK | hole | `w1/T51LabWitHARDLINK.md` (pristine exit 1 `LINK … hardlink count 2`, mutant exit 0 CLEAN) |
| S_POLICY | hole | `w1/T51LabWitPOLICY.md` (pristine `POLICY …` vs mutant `DRIFT … sha deadbeefdead->-`, both exit 1) |
| S_DUP_UNIQ | hole (new witness, this seat) | `w1/T51ScribeEntry/dup-pristine.out`, `dup-mutant.out`, driver `dup-witness.sh` |
| S_USAGE_EXIT | hole | `w1/T51LabWitUSAGEEXIT.md` (unknown arg: exit 2 vs 0) |

S_DUP_UNIQ is the one survivor no peer witness covered. The DUP block runs only
for the default baseline (`corpus/drift-pins.sh:168`), and the selftest always
passes `--baseline` (`:400`), so the arm is unreachable on-suite. Witness built
from the gate's own `--pin` output under a scratch `HOME` (all 15 `FILES` paths
materialized), then one baseline row duplicated:

- pristine: one line, `DUP      $HOME/.local/bin/the-janitor (baseline has more than one row)`, exit 1;
- mutant: **14** lines, one `DUP` per *unique* row (e.g. `DUP      $HOME/.agents/AGENTS.md …`), exit 1.

So the spec's prose ("duplicate baseline rows are never reported") is true but
understates the mutant: `uniq -d`→`uniq -u` inverts the test. The `SURVIVED`
prediction still held. Both runs exit 1, so this witness separates on the
verdict lines, not the exit code — the entry says so.

## 4. Entry conformance to the C2 counter's entry checks

- `measure.py:205-206` reads the first 8 lines for a `source:` line; the entry's
  `source:` is line 1 and contains `tail = rel.split('/', 1)[1]` =
  `corpus/drift-pins.sh` (`measure.py:200`) inside the full target path
  `kagi-shokunin/corpus/drift-pins.sh`, plus S272 and S273.
- `measure.py:208-215` needs a row with status `mined`, opened `2026-10-26`,
  whose used-by names the entry; the entry names S272/S273 and says both are
  opened today (S272 by seat T51ScribeRowGate, S273 by T51ScribeRowBash). Those
  rows are not in `corpus/SOURCES.md` yet — the last line of that file still
  reads "Next unused id: S272" — so the L1 must land both rows with the entry.
- `measure.py:212-213` also needs the entry's name beyond the README base
  bytes; the row below carries `knowledge/mutation-case-kagi-drift-pins.md`.
- The leg name the entry refers to (`bash-drift-pins`) is the spec basename; the
  runner leg is not wired yet (`grep -c "drift-pins" tools/mutate-and-run.sh` →
  `0`), so the entry phrases the regression recheck as expected output, not as
  observed.

## 5. Recommendations that travel (adjacency — kagi's call, not an edit here)

Report lines for kagi, derived from the pinned bytes only:

1. `corpus/drift-pins.sh:403` — the selftest's verdict-word assertion is
   unanchored (`grep -q "$3"` over stdout+stderr that contains paths). Anchoring
   it to the verdict line (`grep -qE '^GONE '`, `'^AMBIG '`, `'^SHAPE '`) makes
   the case independent of the environment that runs it. Not edited here.
2. `corpus/drift-pins.sh:379-438` — no selftest case exercises: a content change
   at equal mode/lines (S_SHA_CMP), a hardlink with link count 2 (`:135`; the
   link case is a symlink, caught by `-L` at `:128`), a no-hash row whose sha
   field is not `-` (`:145`), the membership/DUP block under the default
   baseline (`:168`, `:186-188`), or an unknown argument (`:88`).
3. Nothing here measures whether drift-pins' verdicts about real host files are
   right; suite sensitivity is not gate truth.

## 6. Bounds, tooling, cleanup

- Lane checkout read-only: no runner, README, SOURCES, SKILL or PROVINCE edit;
  no git/jj mutation in the lane or fleet; no sibling lane written (kagi read by
  `git show` only); no `agent://all`.
- Counters not run; no lane clone made; fixtures/probes lived in
  `/fast/scratch/hyaku/tameshi-r51/T51ScribeEntry/`, deleted before yield.
- Tools: none installed or upgraded. One network attempt (`curl
  https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html`) to
  re-read S273's page failed (`curl: (28) connection timed out`,
  gnu.org:443 unreachable); the entry says so instead of claiming a re-read.
- pacman transactions: none (host guard).

## 7. Artifacts

- Entry: `.ufo/waves/round-51/w1/T51ScribeEntry.mutation-case-kagi-drift-pins.md`
- Receipts: `.ufo/waves/round-51/w1/T51ScribeEntry/` — `sweep-id.txt`,
  `results.tsv`, `sweep-neutral.txt`, `results-neutral.tsv`,
  `neutral-K_{GONE_ARM,AMBIG_GT,SHAPE_OPTIN}.out`, `case-probe.sh`,
  `case-probe.txt`, `dup-witness.sh`, `dup-witness.txt`, `dup-pristine.out`,
  `dup-mutant.out`, `dup-drift-baseline.tsv`
- Report: `.ufo/waves/round-51/w1/T51ScribeEntry.md`

## README coverage-map row (for `corpus/README.md`, round-51 section)

```text
| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/mutation-case-kagi-drift-pins.md` / Core (recorded legs) | source-headed entry citing mined S272 (the pinned gate) and S273 (bash `set` semantics), new this round; tenth ledger leg `bash-drift-pins`, 2/10 killed on the 13-case hermetic suite with the harness note (3 kill-aimed survivors are environment-masked; 5/10 under a neutral sandbox name), 7/10 verdict predictions, five survivors with off-suite witnesses and no equivalent mutant | `.ufo/evidence/round-51/c2/`; `.ufo/waves/round-51/w1/T51LabWit*.md`, `T51ScribeEntry/` |
```

## Summary

- Delivered the tenth-case entry (222 lines, `source:`-headed, S272 + S273, ground line verbatim) modelled on `mutation-case-kumitate-cite-check.md`.
- Facts re-derived, not assumed: pin/blob/mode, spec sha `a98271f6…`, pre-registration 23:52:43Z vs sweep 23:53:02Z, amendment 1 leaves spec bytes intact.
- Recorded 2/10 reproduced exactly with the guarded `sandbox-$DEFECT_ID` suite; the sweep receipt does not print the suite string, so this is stated as a reproduction.
- Harness finding isolated per case: `drift-pins.sh:403` unanchored word grep + `:158` path print + `TMPDIR` under `sandbox-<ID>`; id-sandbox matches, neutral sandbox does not.
- Neutral-name counter-run: 5/10 KILLED, exactly the three kill-aimed misses flip; flagged as a probe, not a ledger value, and marked awaiting `T51LabSandboxLeak`.
- Survivor composition corrected to 5 holes / 3 harness artifacts / 0 equivalents, with a new S_DUP_UNIQ witness (mutant prints 14 false DUPs, never the duplicate).
- Entry states the replay bound: neutralising the sandbox name without re-recording the table breaks `--regression`.
- Blocking dependency for the L1: S272/S273 rows must land mined with this entry in used-by, and the `bash-drift-pins` leg must be wired for the recheck line to be observable.
