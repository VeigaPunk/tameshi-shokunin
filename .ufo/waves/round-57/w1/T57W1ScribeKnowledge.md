# T57W1ScribeKnowledge — gate-row exit-map knowledge entry (round 57, wave 1)

Base `5e3569969b532310d2b8a3d130901757a3df356b`. Lane production files: none edited; no install; no tool installed. Everything below is staged under `.ufo/waves/round-57/w1/T57W1ScribeKnowledge/stage/` or written to this seat's receipts.

## Staged deliverables

| file | what | size |
|---|---|---|
| `stage/corpus/knowledge/gate-row-exit-map.md` | new knowledge entry: provenance trio, why executed rows beyond the selftest, exit map 0/1/2/3, code-by-condition truth table, what the staged rows cover, limits, re-derive, falsifier | 116 lines (`wc -l`) |
| `stage/corpus/knowledge/receipt-revision-binding.md.patch` | R56.3 errata, append-only `## Errata — round 57` block, `ER-R57-K1`; `recheck:` frontmatter line NOT rewritten | base 245 lines → 262 lines; +17, −0 (`git apply --check` OK on a scratch clone at base) |
| `stage/corpus/README.md.patch` | round-57 coverage-map addendum, one row indexing both entries (`receipt-revision-binding.md` and `gate-row-exit-map.md`) | base 645 lines → 653 lines; +8, −0 (`git apply --check` OK) |

Both patch hunks are pure additions appended at end of file, so no existing line moves. The `recheck:` line of `receipt-revision-binding.md` still reads 14/14; ER-R57-K1 says the current value is 19/19. The append-only instruction in the item and the R56.3 wording ("replace the recheck") differ. I followed the item. If the L1 wants the frontmatter line itself changed, that is one in-place line edit and a byte change; it is the L1's call.

## Verification (each with its command; outputs in receipts)

- Gate bytes: `git -C LANE show 5e3569969b…:tools/receipt-revision-gate.py | sha256sum` → `c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`, equal to the lane file (`lane-demo.stdout` lines 2–3). Matches ER-R56-K2.
- Selftest: `python3 tools/receipt-revision-gate.py --selftest` → `GATE_SELFTEST: 19/19 pass`, rc 0 (`gate-sweep.stdout` last lines; `lane-demo.stdout`). This is the value the errata states. The entry's `recheck:` names 19/19.
- Sweep: `receipts/gate-sweep.sh` prints 25 `CASE` lines (`grep -c '^CASE' gate-sweep.stdout` → 25): 19 fixture-repo invocations (scratch, not the lane), 3 lane-level and 3 staged-row invocations. Results are in `gate-sweep.stdout`; the table in the entry is copied from it.
- Staged rows executed: `receipts/registry-recheck.sh` commits the staged registry into a scratch clone and runs `registry-check.py --rev <scratch> --tag new-r57` → `ROW receipt-gate-accept expect=0 got=0 held`, `ROW receipt-gate-content-drift expect=3 got=3 held`, `ROW receipt-gate-unresolvable-certified expect=2 got=2 held`, `REGISTRY_CHECK: held=3/3 superseded=0`, rc 0 (`registry-recheck.stdout`). At base the same command gives `REGISTRY_CHECK: could-not-evaluate (--tag ['new-r57'] selects no registry row)`, rc 2.
- Code coverage count: `receipts/lane-demo.sh`, final block → `codes defined: 11 | emitted by the sweep: 11`, `emitted by a staged row: 2 ['RECEIPT_REV_CONTENT_DRIFT', 'RECEIPT_REV_UNRESOLVABLE']`, `emitted by no registry row: 9`.
- Patch check: `git -C <clone> apply --check <patch>` on both patches → OK; applied in the clone, line counts 245→262 and 645→653; `git diff --stat` in the clone shows 25 insertions, 0 deletions.

## Findings

1. **Exit 1 is outside the documented map and is reached by an uncaught traceback.** `paths-file-missing` (`gate-sweep.stdout`): `--paths /…/no-such-paths.txt` → `FileNotFoundError` traceback, rc 1. The header documents 0 and 3; code exit 2 at `tools/receipt-revision-gate.py:194` is undocumented in the header; exit 1 comes from the usage `SystemExit` (:92, :183, :187) and from the unguarded `Path(paths).read_text` (:197). A could-not-evaluate condition therefore exits 1, not 2. Routed to the lane's next round in the entry; not fixed (lane production file).
2. **Item count mismatch.** The item says "the six codes only the selftest covers." Measured (`lane-demo.stdout`): the three staged rows emit 2 of 11 codes, so 9 codes are emitted by no registry row. All 11 are emitted by the CLI sweep, which is not a registry row.
3. **`--only` takes one name.** `tools/registry-check.py` parses `--only` as a single value (`arg == "--only": only = value`). The recheck line therefore uses `--tag new-r57`, which selects the three staged rows. The item's `--only <row names>` form would fail. Per-row `--only` runs are in `registry-recheck.stdout` lines 11–19.
4. **Standing-rules cell confirmed wrong (R56.2, not edited here).** Sweep case `verdict-role-drift`: verdict role, `--paths` drift → `RECEIPT_REV_CONTENT_DRIFT`, rc 3. `SKILL.md` `## Standing rules` row 1 says `RECEIPT_REV_MISMATCH` for that situation. Owned by the SKILL/C2 seat.
5. **Truth table source.** `T57W1ExecStandingRules.md` is not present in the wave dir. The truth table is built from the sweep, not copied from that file.
6. **Source row not yet landed.** The provenance `source:` cites S283 (GNU grep §2.3 Exit Status), staged by T57W1ScoutSourceA in `T57W1ScoutSourceA.json` (`next_unused_id: S283`). `corpus/SOURCES.md` has no S283 at base (`grep -n '^| S283' corpus/SOURCES.md` → no line; S282 is the last row). The entry's citation is valid only after the L1 lands that row. The receipt sha256 `517177d02c39c446470c898273036a7616f705e4cbdcb6486b76a25700675f37` and quote at receipt line 1208 were checked: `sha256sum` matches, `grep -n "Normally the exit status"` → line 1208.
7. **Scouts' staged row candidate used only as provenance.** The grep row says "1 if no lines were selected"; the gate's own exit 1 is usage. The entry flags this as an [INFERENCE] about callers, not a measured fact.

## NO-HARM and wave-3 notes for the L1

- The errata patch and the README patch change pinned bytes (`receipt-revision-binding.md` and `corpus/README.md`). Per the item's no-harm note, sections that read these files lose credit until the L1's wave-3 re-key at C0. The new file `gate-row-exit-map.md` is a new knowledge entry; whether it affects any ledger pin I did not measure (I did not run the cold-read monitor; the item did not ask for it).
- Staged rows the entry depends on: `T57W1ExecRegistryRows/stage/tools/registry.json` (three rows, tag `new-r57`) and `stage/tools/fixtures/receipt-gate/` (`accept.receipt`, `drift.receipt`, `drift.paths`). The entry's `recheck:` holds only when they land together; the recheck was executed on exactly that staged content in a scratch commit.
- `drift.receipt` names `c34e2b14…`, which exists in the lane (`git cat-file -t c34e2b14…` → commit), and `round-56-verifier-spotcheck.md` differs between it and base (`git diff --name-only c34e2b14… 5e35699… -- corpus/lessons/round-56-verifier-spotcheck.md` → that path). The drift row therefore holds at base; it stops holding if that lesson is later re-aligned with `c34e2b14`.
- Lane status after this seat: `git status --short -- corpus tools SKILL.md` prints nothing (no lane file touched). The untracked `.ufo/waves/round-57/` and `.ufo/evidence/round-57/` are other seats' work.

## Receipts

`.ufo/waves/round-57/w1/T57W1ScribeKnowledge-receipts/`
- `gate-sweep.sh` / `.stdout` / `.stderr` — code-by-condition sweep (fixture repo under scratch; exits 0/1/2/3 as tabled)
- `registry-recheck.sh` / `.stdout` — staged rows at a scratch commit, `held=3/3`
- `lane-demo.sh` / `.stdout` — staged accept row from the lane (`RECEIPT_MISSING`, rc 3), selftest 19/19, gate sha, coverage count 11/2/9
- `additions/add-receipt-revision-binding.md`, `additions/add-readme.md` — the appended text the two patches were built from
- Stage patches: `.ufo/waves/round-57/w1/T57W1ScribeKnowledge/stage/corpus/knowledge/receipt-revision-binding.md.patch`, `…/stage/corpus/README.md.patch`

## Tools

None installed or upgraded. Used: `git`, `python3` (gate and registry-check at base), `sha256sum`, `diff`, `bash`.

## Checks the main agent should run (not run by this seat)

- `python3 tools/receipt-revision-gate.py --selftest` at the content-final commit: expect `GATE_SELFTEST: 19/19 pass`.
- `python3 tools/registry-check.py --rev REV --tag new-r57` after the staged registry lands: expect `REGISTRY_CHECK: held=3/3 superseded=0`.
- `git apply --check` for both patches at the wave-3 base.
- Re-run `gate-sweep.sh` if the gate bytes change (the table is keyed on `c60772ce…0569ac9`).
