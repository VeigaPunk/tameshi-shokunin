# T51ScribeMistakes — draft `## Mistakes` for `corpus/lessons/round-51.md`

- Seat: `T51ScribeMistakes` (leaf; no subagents)
- Round: 51 (hyaku run 9, L1 `TameshiR51`) · wave w1 · lane `tameshi-shokunin`
- Item: draft the round's `## Mistakes` section — two rows, contract form `class · evidence pointer · captured-by · fix`, a fix counting only once shown able to fail
- Lane state read: base `9962033fd7a75aa2f2847e979dd687a5d28505a1` (read through `git show`), REV-side current tree for receipts under `.ufo/evidence/round-51/`
- Files written by this seat: this report and `w1/T51ScribeMistakes/` receipts only. No lane file, no counter, no gate was edited or executed (see §5).

## 1. Deliverable — the section, ready to append

Append the block below to `corpus/lessons/round-51.md` (new file; the lane has no round-51 lesson yet —
`test -e corpus/lessons/round-51.md` → absent). Class vocabulary follows the form rounds 48–50 used
(one bare class token, then the gloss; no `mistakes.md` exists in the lane or the fleet —
`find /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokuknow -maxdepth 3 -name mistakes.md` → none,
so round-48's "the `mistakes.md` §5 vocabulary" cites a file that is not in the tree and is not repeated here).

```markdown
## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `oracle-leak` — the suite proved its own label: the gate's self-test asserted bare verdict words with an unanchored substring `grep` over output that prints absolute scratch paths, and the harness named each sandbox after the defect id, so three detectable defects were recorded as survivors and 3 of 5 kill-aimed predictions missed | kagi `corpus/drift-pins.sh` @ `e64e81b8eb96f3682b00c1e7a291e84420b280fa` (blob sha256 `c138d34c…`, 451 lines; copy + sha in `w1/T51ScribeMistakes/drift-pins.e64e81b8.sh`): the oracle is `:403` `elif ! grep -q "$3" <<< "$out"; then`, over the stdout+stderr captured at `:400`, and the fixture lives under `:376` `d=$(mktemp -d)` whose files are printed by `:158` `printf 'DRIFT   %s %s\n' "$p" …` (also `:203`, `:213`, `:224`, `:232`, `:235`, `:242`); the id enters that path from the harness: `grep -n 'sandbox-\$DEFECT_ID' tools/mutate-and-run.sh` → `:1418` (leg `js-round-gate`, r16), `:1423` (`js-sources-check`, r18), `:1428` (`js-cite-check`, r26); sweep receipt `.ufo/evidence/round-51/c2/sweep/sweep.txt:10,12,17` (`K_GONE_ARM`, `K_AMBIG_GT`, `K_SHAPE_OPTIN` `SURVIVED (exit=0)`) and `:31` (`killed=2 survived=8 … kill-rate=20%`); the single-variable pair `.ufo/waves/round-51/w1/T51LabSandboxLeak.md` §3–§4 and `T51LabSandboxLeak/README.md` (A id-named → `PASS (13 cases)` exit 0; B neutral `sandbox-n2` → `FAIL symbol gone: no /GONE/ in output` exit 1; C verdict-word name resurrects `K_GONE_ARM`; 3 repeats identical, no other verdict flips); text-level demonstration of the oracle alone: `w1/T51ScribeMistakes/row1-oracle-leak.txt` | **no rule reached the oracle's input.** The nearest is QUALITY 96 (`corpus/QUALITY.md:1420-1426`, "a differing observation is attributed to a cause only by a run that varies that cause alone"): it binds the *explanation* of a difference and was satisfied only afterwards by the sandbox-name pair — it cannot see a survivor that the suite manufactured. `PROTOCOL.md:385-389` (`§Gate standard`, Self-test) requires isolated fixtures and "a stable expected finding-id" but nothing about the oracle's input: an assertion satisfied by the fixture's own path is a stable finding-id. QUALITY 101 (`corpus/QUALITY.md:1526-1536`) binds selftest *reach* (`measure()`), not what the oracle reads. The pre-registration's own oracle model is wrong in one clause: `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec:3` ("Suite: hermetic `env -i` … ; verdict oracle = exit status only") is true of the harness verdict and false of the gate's self-test oracle, which is a word grep — and no criterion compares a spec's declared oracle with the suite it declares | drafted QUALITY criterion 102 (text at `.ufo/waves/round-51/w1/T51ScribeMistakes.md` §2, to land with the round's criteria block): a self-test's verdict is invariant under renaming its fixture — recorded verdicts are the neutral-naming run (`sandbox-n<ordinal>`), a hostile root splicing the asserted words must not change any verdict, no harness names a sandbox/work dir/mutant after the defect id. It counts only once its falsifier fails: `T51LabSandboxLeak/red-gone-id.sh` (exit 0, `PASS (13 cases)`) must be rejected and `green-gone-neutral.sh` (exit 1, `no /GONE/ in output`) accepted on the pinned blob, the A-vs-B flip must be exactly the three misses, and the three exit-status-only legs (`js-round-gate`, `js-sources-check`, `js-cite-check`) must stay identical under both namings — a check that flagged them too would be vacuous |
| `self-description-drift` — the lane's inventory and its coverage map disagreed with what the lane had already shipped, for up to ten rounds: the registry home named 2 instruments while 30 lane tools expose a self-test, and 7 of the coverage map's 10 status cells still read `open` while the lane's own appended sections declared them held/partly held; the frozen round-45 monitor also kept S022 at `queued` with a used-by path | at base `9962033`: `git show 9962033:SKILL.md \| sed -n '1499,1507p'` → `### Gate/probe registry` at `:1499` with **2** data rows (`:1503`, `:1504`) and the self-limiting sentence `:1506` "Registry scope is these round-12 instruments"; `git show 9962033:corpus/README.md \| sed -n '76,87p' \| awk -F'\|' 'NR>2{print $2 $5}'` → F1 held (round 1), F2 held (round 1), F3–F9 `open`, F10 `open`; the same tree's `:599` reads "F10 … **held (round 49)**" and `:608` "F6 … **held (round 50)**", so `:87` and `:83` contradict their own map's prose; the L1's frozen reading names 7 superseded cells with their basis lines (`.ufo/evidence/round-51/c1/frontier-expected.json` → F1, F2, F4, F5, F6, F8, F10); routing: `corpus/lessons/round-50-verifier-spotcheck.md:99` (registry gap: `tools/shrink-case.py`, `tools/pbt-staged-id.py`) and `:100` (table stale), `:98` (S022); receipts `w1/T51ScribeMistakes/row2-base-red.txt` | **QUALITY 76** (`corpus/QUALITY.md:903-913`, "a standing self-assessment row must state what the committed tree holds … at every deciding run") is the rule that should have caught the stale table, and it did not fire: its text and its falsifier are scoped to *a count of committed bytes in a SCORECARD row* (the counter's `m6`), while the stale surface is a *status cell in `corpus/README.md`* — not SCORECARD, not a count. `PROTOCOL.md:363-365` ("Corrections sweep every mention") did not fire because its trigger is a grep for the superseded claim and the superseded token is `open`, which the same table legitimately uses for F3/F7/F9. The registry side has a rule with no reading: `PROTOCOL.md:418-421` (`Delivery`/closure: "closure grades no gate conformant until its registry row exists at the lane's *registry home*") plus `Registry` `:398-405` — but the lane's own section narrowed its scope at `SKILL.md:1506`, so a round-49/50 tool's absent row read as out of scope, and nothing enumerated tools → rows (the round-50 spot-check found both by hand) | the two frozen round-51 counters supply the missing mechanical readings, each red on this surface at base: C1 (`.ufo/evidence/round-51/c1/measure.py`) requires the appended table to cite, per Fk, a ≤ 6-line range holding the id and the frozen status phrase, and every `mined` row to carry a used-by path that exists — at base `contract.json` `claims.C1.before` = `frontier_bad=10 … status_conflicts=1 (S022) total=11 C1_R51_PASS=false`; C3 (`.ufo/evidence/round-51/c3/measure.py`) requires one conforming row per tool of the frozen 30, each row's self-test exit 0 with its last-line finding id recorded — at base `claims.C3.before` = `covered 2 at most of 30 … C3_R51_PASS=false`. They count once the L1's deciding run prints them false at base and true at REV; that run is the L1's, not this seat's |
```

Row notes for the L1 (not part of the appended block):

- Row 1's fix is a *drafted* criterion. Nothing in this round has yet shown criterion 102 able to fail
  except the pair named in its falsifier, which is a seat's run, not mine (§2, §4).
- Row 2's fix is C1+C3, whose red-at-base state is recorded in the contract, not observed by this seat.
  The base *surface* I re-read directly is in `w1/T51ScribeMistakes/row2-base-red.txt`: 2 registry rows,
  0 rows naming either round-49/50 tool, F6/F10 `open` against `:599`/`:608` in the same commit.

## 2. Drafted criterion — next free number is 102

The tail of `corpus/QUALITY.md` ends at criterion 101 (`grep -n '^### Criterion' corpus/QUALITY.md | tail -1`
→ `1526:### Criterion 101 …`; file length 1546 lines), and `grep -c 'Criterion 102' corpus/QUALITY.md` → 0.
The block belongs under a new `## Criteria appended — round 51 (2026-10-26)` heading.

```markdown
### Criterion 102 — a self-test's verdict is invariant under renaming its fixture

A gate's self-test and the mutation suite that drives it are one instrument, so the verdict must not
depend on what the fixture is called. Every recorded verdict is measured under two roots that differ in
one variable: a neutral root (`sandbox-n<ordinal>`, no verdict vocabulary in any path) and a hostile root
whose path splices the words the self-test asserts (`sandbox-GONE-AMBIG-SHAPE`). The two must agree, and
the neutral run is the recorded one. A self-test case that passes only because its expected word occurs
inside a path the gate itself prints — a scratch absolute path, a fixture name, the mutant file name — is
measuring its harness, not the gate: a bare `grep -q 'WORD'` over output that carries an absolute path
fails the rule at inspection, and a gate with a bare-word pattern and any printed path is read as suspect
until the pair runs. No mutation harness names its sandbox, work dir or mutant file after the defect id.
A gate green under the hostile root and red under the neutral one is repaired, never re-recorded: the
neutral-naming verdicts are the ones a kill rate may rest on. The rule binds oracle input, not
environment isolation (that is PROTOCOL §Gate standard, Self-test) and not selftest reach (criterion 101).

Check that can fail: `tools/mutate-and-run.sh`'s `--selftest` gains the two naming arms over one fixture
spec — the same target, spec and timeout, the sandbox template of `:1418`/`:1423`/`:1428` with
`$DEFECT_ID` replaced by an ordinal in one arm and by a verdict-word string in the other — and prints one
`ORACLE_NAMES <defect> <verdict-A> <verdict-B> <same|DIFF>` line per case, exit 1 on any `DIFF`; the
static arm lists, per gate, its bare-word self-test patterns beside the lines that print a path, exit 1
when a gate has both and its dynamic pair is not committed beside it.

Lesson: `corpus/lessons/round-51.md` `## Mistakes` row 1 (the C2 sweep: 2/10 KILLED where the
pre-registered spec predicted 5/10, and the three misses are the suite's own sandbox names satisfying the
gate's oracle; `.ufo/waves/round-51/w1/T51LabSandboxLeak.md`).

Falsifier that must fail: on kagi `corpus/drift-pins.sh` @ `e64e81b8` (sha256 `c138d34c…`) the pair
`.ufo/waves/round-51/w1/T51LabSandboxLeak/red-gone-id.sh` prints `DRIFT_SELFTEST: PASS (13 cases)` and
exits 0 while `green-gone-neutral.sh` prints `drift-selftest: FAIL symbol gone: no /GONE/ in output` and
exits 1 — the check must reject the first and accept the second, and the A/B flip must be exactly
`K_GONE_ARM`, `K_AMBIG_GT`, `K_SHAPE_OPTIN` with no other verdict moving over three repeats
(`T51LabSandboxLeak/README.md` `table.tsv`, `raw/`). Negative controls that must not move: the three
exit-status-only recorded legs `js-round-gate`, `js-sources-check`, `js-cite-check` keep identical
verdicts under both namings (`.ufo/waves/round-51/w1/T51LabLeakRoundgate.md` §4,
`T51LabLeakSourcesCheck.md` results table, `T51LabLeakCiteCheck.md` findings 1–2); a check that flagged
them is vacuous. Out of scope, named: a word the gate echoes from fixture *content* rather than a path;
`mkdtemp` suffix nondeterminism inside stdout; a gate whose self-test prints no path at all.
```

Landing note for the L1: the check edits `tools/mutate-and-run.sh` (the suite template and, once C2 lands,
the tenth leg), and the round-21 cold-read monitor pins that file — the contract's own
`no_harm.coldread_note` measures 20 credited sections lost on any byte change there, so the edit carries
the reading-bound re-key and the QUALITY 98 precheck (`corpus/QUALITY.md:1436-1444`) before the deciding
run. The registry row this criterion implies for the runner does not exist at base either
(`SKILL.md:1499-1503`, 2 rows) — it is C3's surface, not a second fix.

## 3. What this seat read and ran (each finding above rests on one of these)

| # | command | observed |
|---|---|---|
| 1 | `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8…:corpus/drift-pins.sh \| sha256sum` | `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb` (= the C2 spec header's pin) |
| 2 | `grep -n 'elif ! grep -q' drift-pins.e64e81b8.sh`; `grep -n 'd=$(mktemp -d)' …`; `grep -n "printf 'DRIFT   %s" …`; `grep -n 'out=\$(' …` | `:403` the oracle, `:376` the fixture root, `:158` the path-printing line, `:400` the capture the oracle reads |
| 3 | `grep -n 'sandbox-\$DEFECT_ID' tools/mutate-and-run.sh` | `:1418`, `:1423`, `:1428` — one suite template on the r16/r18/r26 legs |
| 4 | `grep -n 'DEFECT K_GONE_ARM\|DEFECT K_AMBIG_GT\|DEFECT K_SHAPE_OPTIN\|MUTATE: DONE' .ufo/evidence/round-51/c2/sweep/sweep.txt` | `:10`, `:12`, `:17` three `SURVIVED (exit=0)` lines; `:31` `killed=2 survived=8 … kill-rate=20%` |
| 5 | text demo, `w1/T51ScribeMistakes/row1-oracle-leak.txt` | `DRIFT … /w/sandbox-K_GONE_ARM/… \| grep -q GONE` → exit 0; `/w/sandbox-n2/… \| grep -q GONE` → exit 1 (same for `AMBIG`, `SHAPE`) — the oracle alone is satisfied by the id, with no mutant involved |
| 6 | `git show 9962033:SKILL.md \| sed -n '1499,1507p'` | header + 2 data rows + the `:1506` scope sentence |
| 7 | `git show 9962033:corpus/README.md \| sed -n '76,87p' \| awk -F'\|' 'NR>2{print $2 $5}'` | F3–F9 and F10 `open` at base |
| 8 | `git show 9962033:corpus/README.md \| sed -n '599p;608p'` | "F10 … **held (round 49)**", "F6 … **held (round 50)**" in the same commit |
| 9 | `jq -r '.rows\|to_entries[]\|"\\(.key) \\(.value.status)"' .ufo/evidence/round-51/c1/frontier-expected.json` | F1 held, F2 partly held, F4 partly held, F5 Core, F6 held, F8 partly held, F10 held — 7 cells the table does not state |
| 10 | `git grep -l selftest 9962033 -- tools \| wc -l` → 31; `jq '.tools\|length' .ufo/evidence/round-51/c3/tools-base.json` → 30 | the registry's 2 rows against the frozen 30 (the crude grep counts one file the list excludes; the list governs) |
| 11 | `.ufo/waves/round-51/w1/T51LabSandboxLeak.md` §3–§5 and `T51LabSandboxLeak/README.md` (read, not re-run) | A/B/C table; A-vs-B flip exactly the three misses; red/green pair files and exits |
| 12 | `.ufo/waves/round-51/w1/T51LabLeak{Roundgate,SourcesCheck,CiteCheck}.md` (read, not re-run) | all three recorded legs keep identical verdicts under both namings; their oracles are exit-status-only |

## 4. Limits, and what this seat did not do

- I ran no counter, no gate, no sweep and no mutant. All sweep, lab and leg numbers above are read from
  committed receipts or peer reports, and are labelled as such in the table; the only executions are the
  read-only `git show`/`grep`/`awk`/`jq` reads and the two-line `printf | grep -q` text demo.
- Row 1's fix (criterion 102) is a draft. Its "able to fail" status rests entirely on
  `T51LabSandboxLeak`'s pair, which I read but did not reproduce; whether it *fails the draft check* is
  the L1's call when the check is built.
- Row 2's fix is C1+C3. Their red-at-base values are the contract's `claims.*.before` strings; I observed
  the base *surface* (items 6–8, 10) but not the counters' verdict lines.
- The 7-cell count in row 2 is the L1's frozen reading (`frontier-expected.json`); the two cells I
  re-read in the tree at base are F6 (`:83`) and F10 (`:87`). A reader who disputes the other five is
  disputing that file, not this report.
- Row 1's `:400`/`:403` line numbers are the pinned blob's, not the worktree's; the kagi worktree may have
  moved past `e64e81b8`. The copy in `w1/T51ScribeMistakes/` carries the sha.
- Out of scope for this seat, named: the C2 ledger entry and the tenth leg (`tools/mutate-and-run.sh`, the
  C2 executor's); the registry rows for the 28 uncovered tools (`SKILL.md`, C3's); the cold-read re-key of
  the sections those edits drop; `PROVINCE.md`; the deciding run and every claim verdict (the L1's).
- No scratch path is cited as evidence: every receipt named above is under
  `.ufo/waves/round-51/w1/` or `.ufo/evidence/round-51/`.

## 5. Touched surfaces, tooling, scratch

- Lane checkout: read-only. Written: this report, `w1/T51ScribeMistakes/{row1-oracle-leak.txt,
  row2-base-red.txt, drift-pins.e64e81b8.sh}`.
- Fleet repo, sibling lanes, `shokuknow`, jj state, Git index: untouched (`git show` reads only).
- Scratch `/fast/scratch/hyaku/tameshi-r51/T51ScribeMistakes/` — created for the pinned blob, then deleted;
  the blob and both receipts were copied into `w1/` first.
- Tools installed or upgraded: none. Used `git 2.x`, `grep`, `awk`, `jq`, `sha256sum` as present.

## 6. Artifact paths

- `.ufo/waves/round-51/w1/T51ScribeMistakes.md` (this report)
- `.ufo/waves/round-51/w1/T51ScribeMistakes/row1-oracle-leak.txt`
- `.ufo/waves/round-51/w1/T51ScribeMistakes/row2-base-red.txt`
- `.ufo/waves/round-51/w1/T51ScribeMistakes/drift-pins.e64e81b8.sh` (sha256 `c138d34c…`)

## Summary

1. Drafted both `## Mistakes` rows in the contract's four-column form; row 1 is the C2 sandbox-id leak, row 2 a rounds-48..50 self-description drift (registry gap + stale frontier table, with S022 appended).
2. Row 1 evidence: gate oracle `drift-pins.sh:403` over `:399`'s captured output, fixture under `:376`, paths printed at `:158`; harness id-naming at `mutate-and-run.sh:1418/:1423/:1428`; sweep `:10,:12,:17,:31` (2 KILLED / 8 SURVIVED).
3. Row 1 captured-by: no rule reaches the oracle's input — QUALITY 96 binds only the explanation, `PROTOCOL.md:385-389` binds isolation and a stable finding-id but not the oracle's input, 101 binds reach.
4. Row 1 fix: drafted QUALITY criterion 102 (verdict invariant under renaming the fixture; neutral naming is the record), falsified by `T51LabSandboxLeak`'s committed red/green pair with the three exit-status-only legs as negative controls.
5. Row 2 evidence at base `9962033`: 2 registry rows under `SKILL.md:1499` with the `:1506` scope sentence, F6/F10 `open` at `README.md:83/:87` against `:608/:599` held, 7 superseded cells per `frontier-expected.json`.
6. Row 2 captured-by: QUALITY 76 should have caught the table but is scoped to a SCORECARD byte count; `PROTOCOL.md:363-365`'s grep cannot target the token `open`; `PROTOCOL.md:418-421` grades conformance, not inventory completeness.
7. Next free criterion number is 102; the drafted QA check lands on `tools/mutate-and-run.sh`, so it carries the contract's 20-section cold-read re-key and the QUALITY 98 precheck.
8. No counter, gate or sweep was run by this seat; every number is read from a committed receipt or peer report, and the fix rows say which ability-to-fail evidence is still the L1's to produce.
