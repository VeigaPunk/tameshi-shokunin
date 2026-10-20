# S05 — SCORECARD commands D/C baseline, seven-leg inventory, sources-check novelty

Seat: S05CommandDBaseline (leaf, no dispatch). REV measured:
`183f87b899e6cae46be98d251cbc87fb5118f6ca` (lane `master` tip at dispatch and at
read; `git -C . rev-parse HEAD` → same). All lane bytes read via `git show`; no lane
write besides this report. Scratch under `/tmp/tameshi-r18w1-S05CommandDBaseline-*`.

O = observed command output; I = inference; U = unknown.

## 0. Commands D and C (SCORECARD.md:73, :75) — both executed

Run from the lane root with `REV=183f87b899e6cae46be98d251cbc87fb5118f6ca`:

```
$ git show "$REV:tools/mutate-and-run.sh" | python3 -c '<D>'          # SCORECARD.md:73
recorded_cases=7 depth_score=7
exit=0

$ git show "$REV:SHONEN.md" | python3 -c '<C>'                       # SCORECARD.md:75
boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
exit=0
```

O. Depth counting rule (SCORECARD.md:66): one point per recorded case in the pinned
replay ledger, cap 10 — so the pre-move score at this REV is **7**, and an eighth
recorded leg moves it to **8**. The table cell still reads `6` because its
"Measured commit" is `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` (fleet round-1
baseline), not the current tip; the `7` comes from the reproducible command, matching
the L1 claim. Not a contradiction.

O. Calibration: C is a *mark census upper bound only* (SCORECARD.md:74 "awards no
evidence/authority credit"). SHONEN.md has exactly four boxes, all `[~]`
(`checked=0 asserted=4 untouched=0`) → upper bound 8, which equals the declared
restraint claim; C cannot itself promote that to a scored 8.

## 1. The seven ledger legs and their pins (verified, not just read)

Leg list: `tools/mutate-and-run.sh:85-91` (comment block), dispatcher call sites
`:1246-1280`, pins `:592-605`, tables `:606-612`. I recomputed every pin with
`git -C <repo> show <rev>:<path> | sha256sum` — **7/7 equal the recorded `PIN_*`**:

| # | leg | repo | rev | blob sha256 (recomputed = pin) | recorded |
|---|---|---|---|---|---|
| 1 | js-kimi-census | kumitate-shokunin | 175de6ba2e9e904010411b19cab27e0af9aad3d4 | 83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426 | 8/10 (80 %) |
| 2 | bash-surface-census | kagi-shokunin | fecee8743e52eb8fb5fbb40782934cb619a1a96e | 275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f | 8/10 (80 %) |
| 3 | bash-tsukuroi-census | tsukuroi-shokunin | 165307fe4746a8807b02ec4a7d7ecac0368454a6 | 084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5 | 6/10 (60 %) |
| 4 | bash-mado-verify | mado-shokunin | eead56b20ad2b28299ae4fa623d52a99b44c743c | d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13 | 4/10 (40 %) |
| 5 | bash-checklist-run | kagi-shokunin | fecee8743e52eb8fb5fbb40782934cb619a1a96e | 7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf | 7/15 (47 %) |
| 6 | js-claims-check | kumitate-shokunin | 175de6ba2e9e904010411b19cab27e0af9aad3d4 | e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b | 7/10 (70 %) |
| 7 | js-round-gate | kumitate-shokunin | 364f1d5954158ef8844bca4a5fef57b05d2f2ca5 | f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9 | 5/10 (50 %) |

O. Case registry is exactly these seven: `corpus/knowledge/mutation-case-*.md` = 7
files, one per leg (kimi-census, kagi-census, tsukuroi-census, mado-verify,
kagi-checklist, kumitate-claims, kumitate-round-gate). The highest case number is
`# Mutation case 7` (`mutation-case-kumitate-round-gate.md:1`), whose
`source:`/`recheck:` header pins the same round-gate bytes and names
`REGRESSION_CASE js-round-gate: PASS`. Case-7 procedure evidence tree is committed:
`.ufo/evidence/round-16/round-gate/` = 34 tracked files (predictions.json, spec,
sweep/, survivor-probes/, runner-*.txt).

## 2. `kumitate scripts/sources-check.mjs` is NOT a leg and NOT a recorded case

O. Commands and exits:

```
$ git show "$REV:tools/mutate-and-run.sh" | grep -n 'sources-check'   → no output, exit 1
$ git show "$REV:tools/mutate-and-run.sh" | grep -cE '^  regression_case_git (js|bash)-'  → 7
$ grep -rn 'sources-check' corpus/knowledge/                          → no output, exit 1
$ grep -rin 'sources.check|sources_check' corpus/knowledge/           → no output, exit 1
$ grep -rln 'sources-check' <lane root, --exclude-dir=.git>
  .ufo/waves/round-16/w1/Overlap1.md, .ufo/waves/round-16/w1/ProvinceBox4.md,
  .ufo/waves/round-16/w2/CKINDCheck.md, .ufo/waves/round-16/w2/C1Overlap.md,
  .ufo/waves/round-16/w2/ProvinceAppend.md, .ufo/waves/round-17/w2/CR13.md,
  .ufo/waves/round-18/spec1.json, .ufo/waves/round-18/dispatch1.json, PROVINCE.md
```

O. `corpus/knowledge/` holds 25 files; none is a sources-check case and no filename
contains "source". The only lane-file mentions outside wave scratch/dispatch data are
`PROVINCE.md:61` (the seven-gates correction) — i.e. a surface statement, not a
recorded mutation case. So the leg name `js-sources-check` and its knowledge note would
both be new. [I] No naming collision with an existing leg or case number; the new case
is case 8.

## 3. Province coverage — no service opt-in needed

O. `PROVINCE.md:7-11`: "**Owns:** the method, documented from the fleet's existing
gates as primary surfaces — `kumitate-shokunin/scripts/*` (six gates with selftest
suites + mutation controls), ...". `PROVINCE.md:14-17`: "Never edits a sibling's gate
code (read-only probes; recommendations travel in round reports)."

O. The `six gates` parenthetical is superseded by appended corrections:
`PROVINCE.md:52-57` — the ledger is "**seven**, not six. The seventh is kumitate
`scripts/round-gate.mjs` ... probed read-only as a kumitate `scripts/*` primary
surface. It is not a service run and needed no opt-in."; `PROVINCE.md:61-62` —
"kumitate carries seven gates, not six: `sources-check.mjs` landed in kumitate
`1a8eed5` (2026-10-19), after the line-8 survey".

O. Precedent for the exact form: `corpus/knowledge/mutation-case-kumitate-round-gate.md:10-11`
— "No owner opt-in exists or was needed: kumitate `scripts/*` are tameshi's read-only
primary surfaces (`PROVINCE.md:7-11`), like cases 1 and 6."

O. Protocol side: `corpus/knowledge/service-optin-protocol.md:26-30` — the service
queue "is an offer, not a schedule: ... it drains only under a fresh opt-in naming a
pinned target + a hermetic suite ... a round with no opt-in records the no-opt-in line
as its complete outcome"; `:75-77` (item 4) — "The service never edits, repairs or
re-pins the gate; a needed change is a recommendation to the owner, not a patch."

[I] Therefore a `kumitate scripts/*` probe is a **primary-surface self-service probe**,
not a service engagement: no opt-in, no request template, no drain of the service
queue; the sibling tree stays untouched and its bytes are materialized from git. This
is the same shape as cases 1, 6 and 7 (Kumitate only ever read).

## 4. Target pin sanity (for the L1's C1)

O. `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show
0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs | sha256sum` →
`6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`, 897 lines;
`git cat-file -t 0acb7752…` → `commit`; `git log -1 --format='%H %ci' 0acb7752…
-- scripts/sources-check.mjs` → `2026-10-19 20:44:37 -0300` (last-touching commit at
read). Suite measured from a /tmp copy of the pinned blob:
`node sources-check.mjs --selftest` → exit 0, 46 `PASS` lines,
`SOURCES_SELFTEST: 46/46 pass`, `VERDICT: PASS`. Kumitate registry row:
`SKILL.md:605` (`| sources-check | gate | … | --selftest | …`); kumitate HEAD at read
`1770305fae20826b39905a8251ddeca6b4957ac4`.

## 5. Coupling map for the eighth leg (actionable baseline)

O. If a leg is added at one place only, the runner's own selftest fails by design
(`tools/mutate-and-run.sh:1789-1797`): "the selftest's leg tuples, the regression call
sites, the written spec files and the declared nlegs must all be the same number". The
hardcoded `7`s at this REV:

- `:1282` `local nlegs=7 npass=0 nfail=0 nsetup=0 st` (headline `cases=`)
- `:1236` `REGRESSION_EXPECT: recorded kill-rates — …` printf, seven legs
- `:1246-1280` seven `regression_case_git` call sites
- `:1793-1797` `lcalls`/`lfiles`/`lnlegs` agreement, `-eq 7` and `(want 7)`
- `:1798-1806` `lent=( … )` seven tuples (name:spec:TABLE:total:killed)
- `:1807-1808` `[[ ${#lent[@]} -eq 7 ]]`, `(want 7)`
- `:606-612` `TABLE_*` declarations; `:640` `regression_specs()` writer
- `:85-91` the ledger comment block the SCORECARD D regex counts

[I] A `js-sources-check` leg therefore needs: `PIN_SOURCES`/`REV_SOURCES` (pin as
§4), a `TABLE_SOURCES` (10 defects per the C1 spec), a `js-sources-check.spec`
emitted by `regression_specs()`, one `regression_case_git` call with suite
`node "$MUTANT" --selftest`, one `lent` tuple, and the count updates 7→8 at `:1282`,
`:1796`, `:1797`, `:1807`, `:1808`, plus a one-line `:92` entry matching the D regex
`^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+`. [I] Command D then reads
`recorded_cases=8 depth_score=8`; note D counts the documented comment line, not the
run (SCORECARD.md:66 is explicit: "documented case depth, not newly executed cases"),
so D alone must not be presented as proof of a passing sweep — that needs
`bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=8 …)` in a
fleet-mirror /tmp clone.

## 6. Unrun / open

- U. The full `--regression` sweep at this REV was **not** run here (the target assigns
  baseline counting only; the sweep is the runner seat's measurement, and lanes gate on
  a PASS line, not on this report). No pass is claimed for `cases=7`.
- U. Whether `sources-check.mjs`'s 46-check suite has exactly the clause surface a
  10-defect spec needs is the spec author's question, not measured here.

**Verdict: built** — D=7 and C=8-at-upper-bound reproduce at 183f87b (exits 0); all
seven leg pins recompute byte-identical; `js-sources-check` is neither a leg (7 call
sites, grep exit 1) nor a `corpus/knowledge/` case (grep exit 1, max case = 7); and
`PROVINCE.md:7-11` + `:52-62` make kumitate `scripts/*` a read-only primary surface,
so no service opt-in is required (`service-optin-protocol.md:26-30,75-77`; precedent
`mutation-case-kumitate-round-gate.md:10-11`).
