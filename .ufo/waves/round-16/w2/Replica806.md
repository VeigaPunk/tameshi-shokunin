# Replica806 — cold-read replica, SKILL.md lines 806–857 (round 16, wave 2)

**Attacked:** the post-freeze replica claim for the mado-verify mutation gate —
SKILL.md `### The opt-in contract` (record) and `### The protocol — ordered,
fail-closed` (instruction), re-executing `mutate-and-run.sh` against the pinned
mado gate with the reconstructed 10-defect spec.

**One-line verdict: HOLDS.** On the pinned bytes the sweep reproduced the
recorded table exactly: `MUTATE: DONE … killed=4 survived=6 inconclusive=0
kill-rate=40%`, all ten mutant sha256 matching the recorded prefixes, exit 0.

## Page pin

- `git show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SKILL.md | sha256sum`
  → `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` — matches
  the assigned page sha.
- Read only lines 806–857 plus explicitly named files. `mutation-case-*.md`
  resolved to `corpus/knowledge/mutation-case-mado-verify.md` (in
  `corpus/knowledge/`, not the forbidden `corpus/lessons/`). `plans/round-6.
  plan.md:23-25` is inside the forbidden `plans/` prefix — named but not read.

## Named artifact state

| artifact | pin claimed | recovered at | measured |
|---|---|---|---|
| `mado-shokunin/tools/mado-verify.sh` | sha256 `d7edaab4…d0e13`, 45334 B, 1098 newlines | mado-shokunin commit `eead56b20ad2` | sha256 `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` · 45334 B · 1098 lines · no trailing newline (tail = `…exit 1` no `\n`) — **pin exact** |
| `tameshi-shokunin/tools/mutate-and-run.sh` | `597e1419…ff6331b`, 1001 lines | tameshi-shokunin commit `b58b26fbeba8` | sha256 `597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b` · 1001 lines — **pin exact** |
| live `mado-shokunin` tree | "porcelain-clean sibling tree" | — | `git status --porcelain` empty at HEAD `27cd06f5`; **live gate is now `fba82a66…`, 177849 B / 3711 lines — substrate moved since the pin** (pin still re-executable from history; a re-pin would be needed for a fresh run, exactly as the contract's own sentence 1 states) |
| live `mutate-and-run.sh` @ c699c8c3 | — | — | `89722ddb…`, 1726 lines — harness also moved; run used the pinned `597e1419…` bytes from `b58b26fbeba8` |

## Contract anchors (section 806–826, record)

- `bash "$MUTANT" --selftest` exercises `$0` (the copy): `mado-verify.sh:340`
  `mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX`; `:406` runs `… "$0" --root "$A"`
  under a starved `PATH` sandbox (`:400-406`, no `hyprctl`); `:380` fixture
  byte-identity assert; `:422` `rm -rf "$T"` on green — matches case file
  `:44-49` description.
- Green count line `MADO_SELFTEST: 28/28 assertions passed` — printed verbatim
  by the control run (below).
- Gate header clauses all present on pinned bytes: verdict tokens `:9-10`,
  exit map `:12-13`, anti-claim `:25-26`, include census `EXPECT` array
  `:463-480`, 12-conf inventory `:522`, sha pin `:574`, boundary `:735-742`.
- Clause-mapped defect spec: 10 defects over clauses A–F — reconstructed and
  every `@old` re-verified `count==1` on the pinned bytes (grep -F counts:
  all 1; `"$reason"` and `exit 1` non-unique individually, matched as the
  single two-line span `"$reason"\nexit 1` per case-file E3).

## Protocol execution (section 827–857, instruction)

All in `/tmp/tameshi-r16w2-Replica806-BwllZj/` (gate, harness, spec, workdir —
no lane/substrate path written):

```
bash $S/mutate-and-run.sh --target $S/mado-verify.sh \
  --defects $S/spec/mado-verify.defects.spec \
  --suite 'bash "$MUTANT" --selftest' --workdir $S/work --label mado-verify.sh --tail 14
```

Log head pins: `MUTATE_TOOL sha256=597e1419…` · `MUTATE_TARGET sha256=d7edaab4…
bytes=45334` · `MUTATE_SPEC defects=10`.

| step | claim | observed |
|---|---|---|
| 1 pin + pristine | fresh byte copies | pristine sha `d7edaab4…`, all 10 mutants `diff` = exactly one line |
| 2 spec uniqueness | asserted before any run | no SETUP refusal; control ran (=> parse+count passed) |
| 3 control first | must run green | `CONTROL: GREEN (exit=0 duration-ms=585)` + `MADO_SELFTEST: 28/28 assertions passed` |
| 4 one mutant/defect | KILLED/SURVIVED by exit | exit=2 → KILLED (D1,D2,D4,D6); exit=0 → SURVIVED (D3,D5,D7,D8,D9,R1); 0 inconclusive |
| 5 restore re-check | `MUTATE_RESTORE: OK\|DRIFT` | `MUTATE_RESTORE: OK (target-sha256 before=d7edaab4… after=d7edaab4… pristine-sha256=d7edaab4…)` |
| 6 headline + evidence | DONE, exit 0; evidence dir | `MUTATE: DONE (target=mado-verify.sh defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%)` exit 0; `MUTATE_EVIDENCE` dir holds `pristine.mado-verify.sh`, `mutant-{D1..D9,R1}.*`, `evidence/{CONTROL→control,D1..R1}.out`, `results.tsv`, `defects.tsv`, `spec.copy` |

**Reproduced table vs recorded (`mutation-case-mado-verify.md` §1):** identical
verdicts 10/10 (pre-registration written into the spec header before the run
held 10/10), and all ten mutant sha256 in my `results.tsv` match the recorded
§9 prefixes byte-for-byte: D1 `ec60ae5c8f82…`, D2 `41ae4e6e26e6…`, D3
`1c0e1d3ee758…`, D4 `7902653acf98…`, D5 `5f0937367e74…`, D6 `4b94c1802ba0…`,
D7 `ce37404f12eb…`, D8 `81351c897a8b…`, D9 `81817f67c950…`, R1 `6f3affd3849e…`.
Failing-assertion lines also match §1 verbatim (D1 `A: CLEAN verdict`, D2
3-failure C block, D4 `B/C: exit 1`, D6 `hypr.local.inventory FAIL`).

## Gaps / notes

- `plans/round-6.plan.md:23-25` (contract point 4's anchor) is inside the
  forbidden `plans/` prefix → not re-checked; coverage note, not a
  contradiction.
- Wave-1 artifact `.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh` exists in
  the tree but `.ufo/waves/` is outside the cold-read scope → not read.
- No installs needed; tools used: git, bash, coreutils (host).

```json
{"seat":"Replica806","skill_sha256":"3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4","sections":[{"start":806,"heading":"### The opt-in contract — what the lane brings","class":"record","verdict":"verified-record","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["plans/round-6.plan.md:23-25 anchor named by the record sits inside the forbidden plans/ prefix; not re-checked"],"commands_executed":["sha256sum mado-verify.sh -> d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13 (45334B, 1098 newlines, no trailing NL)","git -C mado-shokunin status --porcelain -> clean at HEAD 27cd06f5; live gate now fba82a66/177849B (substrate moved since pin)","git -C mado-shokunin log scan -> pinned gate bytes found at commit eead56b20ad2","CONTROL: GREEN exit=0; MADO_SELFTEST: 28/28 assertions passed (via sweep below)"],"opened":["c699c8c3:SKILL.md:806-857","c699c8c3:corpus/knowledge/mutation-case-mado-verify.md","mado-shokunin@eead56b2:tools/mado-verify.sh (into /tmp)","tameshi-shokunin@b58b26fb:tools/mutate-and-run.sh (into /tmp)"],"scratch":"/tmp/tameshi-r16w2-Replica806-BwllZj"},{"start":827,"heading":"### The protocol — ordered, fail-closed","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["bash /tmp/…/mutate-and-run.sh --target /tmp/…/mado-verify.sh --defects /tmp/…/spec/mado-verify.defects.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/…/work --label mado-verify.sh --tail 14","MUTATE_TOOL sha256=597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b","MUTATE_TARGET sha256=d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13 bytes=45334","CONTROL: GREEN (exit=0) · D1 KILLED · D2 KILLED · D3 SURVIVED · D4 KILLED · D5 SURVIVED · D6 KILLED · D7 SURVIVED · D8 SURVIVED · D9 SURVIVED · R1 SURVIVED","MUTATE_RESTORE: OK (before=after=d7edaab4…) · MUTATE_EVIDENCE: /tmp/…/work","MUTATE: DONE (defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%) exit=0","all 10 mutant sha256 == recorded mutation-case-mado-verify.md §9 prefixes; every mutant diff = exactly 1 line"],"opened":["/tmp/tameshi-r16w2-Replica806-BwllZj/work/results.tsv","/tmp/tameshi-r16w2-Replica806-BwllZj/work/mutant-*.mado-verify.sh (diff vs pristine)","/tmp/tameshi-r16w2-Replica806-BwllZj/mutate-and-run.sh:140-200 (spec format docs)"],"scratch":"/tmp/tameshi-r16w2-Replica806-BwllZj"}]}
```
