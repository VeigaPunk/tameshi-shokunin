source: S272 — kagi `kagi-shokunin/corpus/drift-pins.sh` @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (the file's last-modifying commit, 2026-09-28; blob sha256 c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb, 451 lines, 19,088 bytes, mode 100755, unchanged at kagi HEAD 69b61db), read-only, opened 2026-10-26; S273 — GNU Bash manual, The Set Builtin (`set -e`, `-o pipefail`: errexit on a failed assignment ends the run), opened 2026-10-26 (row drafted by seat T51ScribeRowBash; this seat's own fetch of the page failed — gnu.org unreachable — so the semantics named here are the ones the observed run in §0 shows, not a re-read of the page); procedure: `corpus/knowledge/mutation-case-kagi-census.md` (case 2) and cases 3–9
verified-at: 2026-10-26; pre-registration `fe33538405cd97c2f386c10ea91f9cf399d67866` (spec and predictions, 23:52:43Z), sweep 23:53:02Z; amendment 1 `84aa673a1a476e48ccf239335696f0518d08bae7` (23:54:18Z) changed no spec byte (`sha256sum` of the spec = the counter's frozen `a98271f6…`, and `sweep/spec.copy` is byte-identical); receipts under `.ufo/evidence/round-51/c2/`; survivor witnesses `.ufo/waves/round-51/w1/T51LabWit*.md` and `.ufo/waves/round-51/w1/T51ScribeEntry/`
recheck: `git -C kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh | sha256sum` → `c138d34c…e6c70feb`; `bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE bash-drift-pins: PASS` and `REGRESSION: PASS (cases=10 passed=10 …)` (expected once the C2 edit wires the leg; this entry is drafted before it); reopen S272 and S273
ground: Core — the tenth recorded mutation case, the first on a kagi drift gate (fleet-kill-rate-ledger.md queue row :119)

# Mutation case 10 — kagi `corpus/drift-pins.sh` (round 51)

The tenth recorded case and the first on a kagi *drift* gate: the ledger's queue
row named `drift-pins` "unmeasured by sweep; hermetic"
(`corpus/knowledge/fleet-kill-rate-ledger.md:119`). Kagi owns the gate; tameshi
owns the method and this measurement only. Kagi's tree stayed read-only: the
target is a byte copy materialized from its git object store.

One thing must be said before the number: the recorded **2/10 is a property of
the suite plus the harness that ran it, not of the suite alone.** Three
kill-aimed mutants survive because the harness names its sandbox with the defect
id and the selftest's verdict-word assertion is an unanchored `grep` over output
that prints paths (§3). Re-run under a neutral sandbox name the same ten defects
read 5/10 — a probe this seat reproduced, still awaiting the named confirmation
seat (§3, "Standing of that finding"). The recorded table keeps 2/10 because that is what the
pre-registered sweep measured; the composition of the eight survivors is
corrected here, not in the table.

## 0. Pin and suite

- Target: rev `e64e81b8eb96f3682b00c1e7a291e84420b280fa` (the file's
  last-modifying commit), blob sha256
  `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`, 19,088
  bytes, 451 lines, mode 100755 (S272). The blob is unchanged at kagi HEAD
  `69b61db`; the pin is the pinned bytes, not a moving tree.
- Suite: the guarded hermetic form the three js legs use
  (`tools/mutate-and-run.sh:1418`), with `bash` in place of `node`:
  `h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" &&
  exec env -i PATH=… HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C bash "$MUTANT"
  --selftest`. 13 cases at the pin, control `DRIFT_SELFTEST: PASS (13 cases)`
  (`drift-pins.sh:444`), exit 0 (`sweep/evidence/control.out`). One pristine
  control per sweep, GREEN, `MUTATE_RESTORE: OK`. No repeated controls, so
  byte-determinism is not established by this sweep. The sweep receipt does not
  print the suite string; this seat re-ran this form against the pinned bytes and
  the frozen spec and reproduced the recorded verdicts exactly
  (`w1/T51ScribeEntry/sweep-id.txt`, `results.tsv`).
- The suite is the gate's own selftest (`drift-pins.sh:374-446`): it builds a
  scratch tree (`:376` `d=$(mktemp -d)`, fixtures `:379-396`) and re-invokes the
  gate on an alternate baseline pair (`:400`, `--baseline`/`--symbols`). Each
  case is two assertions: the gate's exit code (`:401-402`) and **one
  unanchored verdict word** `grep -q "$3" <<< "$out"` over everything the gate
  printed, stdout and stderr (`:403`).
- The runner's verdict oracle is only the outer exit status of the selftest:
  `KILLED` = exit not in `{0,124,126,127}` (`tools/mutate-and-run.sh:545-551`).
  The 13 per-case assertions are the gate's, not the runner's.

## 1. Pre-registration

Ten defects and their verdict predictions were committed in `fe335384` at
23:52:43Z before any mutant ran; the sweep is stamped
`MUTATE_DATE: 2026-10-26T23:53:02Z`, 19 seconds later. Amendment 1 (`84aa673`,
23:54:18Z) fixed only the controls harness: the spec's sha256 is still the
frozen `a98271f6…` and `sweep/spec.copy` is byte-identical to the spec. The
runner's applier asserts `count == 1` per `@old` before running anything
(`tools/mutate-and-run.sh:420-433`), and all ten applications succeeded.
Composition: 5 kill-aimed (`K_*`) and 5 hole-aimed (`S_*`), chosen by hand from
the suite's predicates, matrix axes recorded in the spec header.

## 2. Result — 2/10 killed (20 %), 7/10 verdict predictions held

| id | edit (pinned line) | predicted | measured | cases passed | killing case (evidence/*.out) |
|---|---|---|---|---|---|
| K_MODE_CMP | mode compare `"$cm" != "$mode"` → `"$cm" != "$cm"` (:154) | KILLED | KILLED | 12/13 | `mode drift` (`:414`) — `drift-selftest: FAIL mode drift: exit 0 want 1`; the chmod is invisible, the case exits 0 |
| K_GONE_ARM | zero-match value pin `-eq 0` → `-eq -1` (:231) | KILLED | **SURVIVED** | 13/13 | none (§3) |
| K_AMBIG_GT | ambiguity threshold `-gt 1` → `-gt 2` (:234) | KILLED | **SURVIVED** | 13/13 | none (§3) |
| K_COUNT_GE | count pin `==` → `-ge` on the pinned count (:210) | KILLED | KILLED | 12/13 | `count drift` (`:432`) — `drift-selftest: FAIL count drift: no /COUNT.*#1->#2/ in output`; the exit half still held (file lines 2->3), the verdict word is missing |
| K_SHAPE_OPTIN | shape opt-in `"shape"` → `"shaped"` (:220) | KILLED | **SURVIVED** | 13/13 | none (§3) |
| S_SHA_CMP | content hash `"$cs" != "$sha"` → `"$cs" != "$cs"` (:156) | SURVIVED | SURVIVED | 13/13 | none |
| S_HARDLINK | hardlink guard `-gt 1` → `-gt 2` (:135) | SURVIVED | SURVIVED | 13/13 | none |
| S_POLICY | secret-refusal `"$sha" != "-"` → `"$sha" == "-x"` (:145) | SURVIVED | SURVIVED | 13/13 | none |
| S_DUP_UNIQ | duplicate detection `uniq -d` → `uniq -u` (:188) | SURVIVED | SURVIVED | 13/13 | none |
| S_USAGE_EXIT | usage catch-all `exit 2` → `exit 0` (:88) | SURVIVED | SURVIVED | 13/13 | none |

Recorded table: the new leg `bash-drift-pins` in `tools/mutate-and-run.sh`
(10 entries in spec order, 2 `KILLED` — `K_MODE_CMP`, `K_COUNT_GE`; the leg is
wired by the C2 edit, which this entry lands beside). Prediction accounting:
5/5 hole-aimed held; 2/5 kill-aimed held. The three misses are one mechanism,
not three independent gaps.

The two kills are decided by different assertions, which is worth keeping: K_MODE_CMP
fails both halves of its case (the mutant prints CLEAN and exits 0, so the
`DRIFT.*mode` word is absent too), K_COUNT_GE fails only the word half (its
exit is 1 for a file-level reason, and the `COUNT` verdict is absent). A suite
that asserted only exit codes would read 1/10 here: K_COUNT_GE's case would
pass. The word assertion is what kills it.

## 3. Survivors — five suite holes, three harness artifacts, no equivalent mutant

The three kill-aimed survivors pass both halves of their case without either half
testing the arm: the exit half of two is satisfied by a file-level `DRIFT` the
case also triggers, the exit half of the third by the abort the mutated arm
itself causes, and the word half of all three by the defect id in the path the
gate prints. The mutant's sandbox is
`$WORKDIR/sandbox-<DEFECT_ID>` and `TMPDIR` points inside it
(`sandbox-<ID>/tmp`), so the fixture directory the gate prints on every
`DRIFT`/`LINK`/`MISSING` line (`drift-pins.sh:158`) contains the defect id.
The case's word assertion (`:403`) is an unanchored substring test over that
output, so the id in the path satisfies it:

| survivor | case (`:408-438`) | what the gate actually prints | what satisfies `grep -q "$3"` |
|---|---|---|---|
| K_GONE_ARM | `symbol gone` (`:423`, wants `/GONE/`) | the case rewrites `b.txt` `one`→`uno`, so the file loop prints `DRIFT <d>/b.txt sha 2c8b08da5ce6->d9f86d34b0b0`; the value-pin arm then falls through to `:238`'s `grep`, matches nothing, and `pipefail` + `set -e` end the run — no `GONE` line is ever printed, and the exit is 1 (which the case wanted anyway) | the path `…/sandbox-K_GONE_ARM/tmp/tmp.XXXX/b.txt` |
| K_AMBIG_GT | `symbol ambiguous` (`:426`, wants `/AMBIG/`) | `b.txt` `one`→`one\none`: `DRIFT <d>/b.txt lines 1->2 sha …`, `symbols_ok=4 symbols_bad=0` — the ambiguous value pin is simply counted as a match at line 1 | the path `…/sandbox-K_AMBIG_GT/…` |
| K_SHAPE_OPTIN | `shape drift` (`:436`, wants `/SHAPE/`) | `env.txt` gains a line: `DRIFT <d>/env.txt lines 2->3`, `symbols_ok=4 symbols_bad=0` — the shape arm never runs | the path `…/sandbox-K_SHAPE_OPTIN/…` |

Reproduced per case against the sweep's own mutant bytes (both fixture shapes,
receipts `.ufo/waves/round-51/w1/T51ScribeEntry/case-probe.txt`): with the
id-bearing sandbox `grep -q` matches on all three; with the sandbox renamed
`sandbox-box` it matches on none, and the three cases fail exactly where they
should — `drift-selftest: FAIL symbol gone: no /GONE/ in output`,
`… symbol ambiguous: no /AMBIG/ in output`, `… shape drift: no /SHAPE/ in
output` (`w1/T51ScribeEntry/neutral-*.out`). The same ten defects, same target
bytes, same suite, run under a neutral sandbox name:
**5/10 KILLED, 5 SURVIVED, control GREEN**
(`w1/T51ScribeEntry/sweep-neutral.txt`, `results-neutral.tsv`). That counter-run
is a probe, not a recorded leg; the ledger value stays the pre-registered 2/10.

**Standing of that finding — probe-grade, not a verdict.** The mechanism is the
L1's pre-wave probe. This seat reproduced it end to end against the sweep's own
mutant bytes (the id-sandbox sweep, the neutral counter-run, and the per-case
`grep` check above), but the named confirmation seat (`T51LabSandboxLeak`) had
not published when this entry was drafted. So the entry records the finding as
probe-grade: the 2/10 stands as measured, the correction to the *composition* of
the eight survivors is asserted here and still owes its independent
confirmation. If that confirmation fails, §3's three "harness artifact" rows are
the only text that changes; §0–§2 and the table are measurements and do not.

Status of the eight survivors:

| survivor | on-suite | off-suite witness | status |
|---|---|---|---|
| K_GONE_ARM | SURVIVED (id-sandbox) | neutral counter-run: case `symbol gone` fails on the missing word | **harness artifact** — the suite does assert this arm, the harness defeated the assertion |
| K_AMBIG_GT | SURVIVED (id-sandbox) | neutral counter-run: case `symbol ambiguous` fails on the missing word | **harness artifact** |
| K_SHAPE_OPTIN | SURVIVED (id-sandbox) | neutral counter-run: case `shape drift` fails on the missing word | **harness artifact** |
| S_SHA_CMP | SURVIVED | one hashed file `alpha\nbeta\n`→`alpha\nBETA\n` (same mode, 2 lines, 11 bytes): pristine exit 1 `DRIFT … sha e49c81e2d2f8->69726aa46966`, mutant exit 0 `CLEAN` (`w1/T51LabWitSHACMP.md`) | **hole** |
| S_HARDLINK | SURVIVED | baseline row for a link-count-2 file: pristine exit 1 `LINK … hardlink count 2`, mutant exit 0 `CLEAN` (`w1/T51LabWitHARDLINK.md`) | **hole** |
| S_POLICY | SURVIVED | no-hash row whose sha field is `deadbeefdead…`, not `-`: pristine prints `POLICY …` and exits 1, mutant prints `DRIFT … sha deadbeefdead->-` and exits 1 (`w1/T51LabWitPOLICY.md`) | **hole** |
| S_DUP_UNIQ | SURVIVED | default-baseline witness (the DUP block runs only when `BASELINE == DEFAULT_BASELINE`, `:168`, and the suite always passes `--baseline`): pristine prints one `DUP` line for the duplicated path and exits 1; the mutant prints **14** `DUP` lines, one per *unique* row, and never names the duplicate, exit 1 (`w1/T51ScribeEntry/dup-pristine.out`, `dup-mutant.out`) | **hole** |
| S_USAGE_EXIT | SURVIVED | `bash <gate> --witness-unknown-arg`: pristine exit 2, mutant exit 0, identical streams (`w1/T51LabWitUSAGEEXIT.md`) | **hole** |

Composition: **5 holes, 3 harness artifacts, 0 equivalent mutants** — unlike
case 9, where one survivor was provably equivalent. Hole-aimed survivors were
therefore 5 of 5 holes; the equivalence question never had to be argued here.

Two details the witnesses settle that the spec's prose does not:

- **S_DUP_UNIQ is not silent.** `uniq -d`→`uniq -u` inverts the test: the
  mutant reports every row that occurs *once*. On the default baseline that is
  14 false `DUP` findings per run (the spec's "duplicate baseline rows are never
  reported" is true but understates it). The prediction `SURVIVED` still held,
  because the on-suite path never reaches the block.
- **S_POLICY's witness separates on the verdict line, not the exit code** (1 and
  1): the refusal is replaced by a content complaint. Exit status alone would
  call that witness a tie.

### Why the recorded table still replays exactly

The leg re-runs the same suite string, so `TMPDIR` again lands in
`sandbox-<DEFECT_ID>` on every replay and the three path-satisfied cases pass
again — deterministically, not by luck. The recorded table
therefore reproduces 2/10 forever, and this entry explains what the 2/10 means.
The constraint this creates is real: **fixing the sandbox name without
re-recording the table breaks `--regression`** (it would read 5/10 against a
table of 2/10). Whichever round neutralizes the harness must re-record §2 at
5/10 and supersede this entry in the same change.

### What a reader of the 2/10 must not conclude

1. Not that kagi's drift gate selftest is 20 % sensitive. Under a neutral
   sandbox the same suite kills 5/10, and the three extra kills are exactly the
   kill-aimed set's misses.
2. Not that the three survivors are equivalent mutants or uncovered arms. They
   are *unmeasured* by this harness: the suite asserts those arms, and the
   harness's own naming satisfied the assertion.
3. Not that 2/10 is comparable with the other nine legs' rates. Three of the
   other legs (`js-round-gate`, `js-sources-check`, `js-cite-check`,
   `tools/mutate-and-run.sh:1418-1428`) use the same `sandbox-$DEFECT_ID` +
   `TMPDIR` form; whether the mechanism ever bit one of them is **not measured
   here** and is raised as an adjacency in the round report.
4. Not that the gate is at fault. A human running `--selftest` gets
   `/tmp/tmp.XXXXXX` paths; the leak is a property of the naming *we* impose.

## 4. What this case teaches

- **A mutation score is a property of a triple — gate, suite, harness.** The
  runner hands the suite a mutable environment (`MUTANT`, `WORKDIR`,
  `DEFECT_ID`, `tools/mutate-and-run.sh:452-456`) and lets the suite string
  build the sandbox. Any harness that puts the defect id into a path the suite
  prints can satisfy an unanchored assertion inside the suite. The check costs
  one extra sweep: re-run the ten defects with the sandbox renamed and compare.
  Any kill-aimed mutant that flips is a harness artifact, not a hole and not a
  kill.
- **Assert on the verdict line, not on a word.** `grep -q "$3"` over combined
  stdout+stderr that contains paths is satisfiable by an environment. Anchored
  forms (`grep -qE '^GONE '`, `grep -qE '^DRIFT_PINS: DRIFT'`) are not. This
  travels to kagi as a report line (adjacency), never as an edit here: tameshi
  reads the pinned bytes and recommends, it does not touch the gate.
- **A prediction table needs the mechanism, not only the verdict.** Three
  `KILLED` predictions missed for one reason that no prediction row names. The
  spec's per-row comments carry the reasoning; the composition line should
  carry the harness assumption too ("suite assertions must be
  environment-independent").
- **Witness probes are what make a survivor readable.** All five hole-aimed
  survivors had a witness; all five are holes. The witness is also what catches
  prose drift (S_DUP_UNIQ's 14 false findings) and what distinguishes a
  line-level separation (S_POLICY) from an exit-code one.
- **The ledger cell and the entry are different artifacts.** The queue row
  (`fleet-kill-rate-ledger.md:119`) says "unmeasured by sweep; hermetic"; this
  case is that sweep, at 2/10 with the composition above. The ledger file is
  not edited this round.

**Limits.** One revision (blob unchanged at kagi HEAD), one host (GNU bash
5.3.20, Linux), one control per sweep. The 20 % is a property of this suite at
this pin under this harness, not of kagi's gates in general; the 50 % neutral
counter-run is a probe, not a recorded leg. Suite sensitivity is not gate truth:
nothing here measures whether drift-pins' verdicts about real host files are
right. Findings on the gate travel to kagi in the round report.
