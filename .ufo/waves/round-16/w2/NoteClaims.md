# NoteClaims — line-by-line claim audit of `corpus/knowledge/mutation-case-kumitate-round-gate.md` @ `c699c8c`

Seat: TameshiR16.NoteClaims (leaf reviewer, depth + calibration falsification).
Target blob: `git show c699c8c36d6e4eca4b796b81a8247904aa145ec8:corpus/knowledge/mutation-case-kumitate-round-gate.md` (135 lines).
Scratch: `/tmp/tameshi-r16w2-NoteClaims/`. No lane or sibling file written except this report. No tool installed or upgraded.

**Verdict: partial — every pin, line number, count, exit code, sha prefix, duration and receipt holds under re-execution; three sentence-level wording gaps (nested SKIP claim, C1059 deferral presented under an absolute witness sentence, K/S table shorthand) and one historical porcelain assertion with no retained receipt fall short of their wording.**

---

## 1. Method

Read the target blob at the lane commit; materialized the pinned kumitate blob into /tmp with `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs`; checked every `:NNN` citation against those bytes; re-derived every count from the retained evidence under `.ufo/evidence/round-16/round-gate/`; re-ran the two `tools/mutate-and-run.sh` selftests from committed bytes; reconstructed four mutated gate files from the pre-registered `@old/@new` strings and ran the exact guarded suite / survivor probes. Seat-recorded experiments (RGRecon strace, RGSentinel hazards, RGControl repeat-control, the original 10-mutant sweep) were re-read and cross-checked, not duplicated; that distinction is stated per row.

Evidence roots:

- target note: `corpus/knowledge/mutation-case-kumitate-round-gate.md` (line numbers below are that file at `c699c8c`)
- pin: `kumitate-shokunin/scripts/round-gate.mjs` @ `364f1d5954158ef8844bca4a5fef57b05d2f2ca5`
- sweep: `.ufo/evidence/round-16/round-gate/sweep/{sweep.log,results.tsv,defects.tsv,spec.copy,evidence/*.out}`
- suite/control/probes: `.ufo/evidence/round-16/round-gate/{suite.txt,predictions.json,round-gate.defects.spec,survivor-probes/*}`
- receipts: `.ufo/evidence/round-16/round-gate/runner-{regression,selftest}.txt`
- supporting seat records: `.ufo/waves/round-16/w1/{RGRecon,RGSentinel,RGControl,SurvivorPrep,CRSentinel}.md`

## 2. Claim ledger

Mark key: **holds** = backing found and (unless stated) re-checked; **falls** = contradicted; **unbacked** = plausible but no backing artifact found.

### Header, lines 1–3

| line | claim | mark | backing |
|---|---|---|---|
| 1 | S053 = kumitate `scripts/round-gate.mjs` @ `364f1d59…`, blob sha256 `f890e277…d3e9`, read-only | holds | `git show 364f1d5:… \| sha256sum` → `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`; `ls-tree` mode 100755 |
| 1 | S052 / S056 / S057 source ids | holds | `corpus/SOURCES.md:61,65,66` (S052 Stryker families, S056 PIT boundary, S057 survey); S053 row at `:62` |
| 1 | projection = matrix §13, round 4 | holds | `corpus/knowledge/arm-class-matrix.md:298` §13 header; §13.10 pin `f890e277…a834d3e9` @ `175de6ba` |
| 2 | verified 2026-10-20, sweep 13:40:15Z, commits e69b488 + landing commit | holds | `sweep.log` `MUTATE_DATE: 2026-10-20T13:40:15Z`; `git log -1 e69b488` committer date `2026-10-20 10:39:59 -0300`; landing `c699c8c` `2026-10-20 10:49:37 -0300` |
| 3 | recheck `--regression` → `REGRESSION_CASE js-round-gate: PASS`; sha recheck → `f890e277…d3e9` | holds | `runner-regression.txt` line `REGRESSION_CASE js-round-gate: PASS`; `git show … \| sha256sum` re-run |

### Opening, lines 7–13

| line | claim | mark | backing |
|---|---|---|---|
| 7 | seventh recorded case; third kumitate gate | holds | `fleet-kill-rate-ledger.md` measured rows 1–6 (`:45-48`, `:276-277`) + round-16 seventh row (`:403`); kumitate at rows 1, 6, 7 |
| 7–8 | kumitate tree stayed read-only; target is a byte copy from the git object store | holds | `sweep.log` `MUTATE_TARGET: /tmp/…/round-gate.mjs sha256=f890e277… bytes=80415`; no suite/tool path writes kumitate; `git --no-optional-locks -C kumitate status --porcelain \| wc -l` → `0` now |
| 9 | `git --no-optional-locks status --porcelain` → 0 entries **before and after** | **unbacked (historical)** | no evidence file records that exact full-tree command around the sweep; wave-1 records exist (`SurvivorPrep.md:62`, `RGConnector.md:43,243`, `RGSource1.md:80,200`) but predate the 13:40:15Z sweep. Current status is 0. The /tmp-copy mechanism makes the claim mechanically sound. |
| 10 | no owner opt-in exists or was needed; PROVINCE.md:7-11 | holds | `PROVINCE.md:7-11` names `kumitate-shokunin/scripts/*` as tameshi's primary surfaces; no opt-in artifact for round-gate in the committed tree (`git grep -i opt-in c699c8c -- .ufo/waves/round-16` finds only protocol references in the cold-read snapshot) |
| 11 | like cases 1 and 6 | holds | `fleet-kill-rate-ledger.md:45` (kimi-census) and `:277` (claims-check) are both kumitate primary-surface cases |
| 11–13 | not a service run; does not drain the service queue (`service-optin-protocol.md` §0) | holds | `service-optin-protocol.md:20-30`: the queue is an offer, drains only under a fresh opt-in; this run carries none |

### §0 Pin and suite, lines 17–31

| line | claim | mark | backing |
|---|---|---|---|
| 17 | rev `364f1d5` is the file's last-touching commit | holds | `git -C kumitate log -1 --format=%H -- scripts/round-gate.mjs` → `364f1d5954158ef8844bca4a5fef57b05d2f2ca5` |
| 17–18 | HEAD `1770305` and `175de6ba` hold the same blob `1f7d623e…` | holds | `git ls-tree` / `rev-parse <rev>:scripts/round-gate.mjs` → `1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3` at `364f1d5`, `175de6ba`, and HEAD; HEAD = `1770305fae20826b39905a8251ddeca6b4957ac4` |
| 19 | 80,415 B / 1,511 lines / mode 100755 | holds | `wc -c` 80415; `wc -l` 1511; `ls-tree` `100755 blob 1f7d623e…` |
| 19–20 | same bytes as matrix §13 pin | holds | matrix §13/§13.10 pin sha `f890e277…a834d3e9` @ `175de6ba`; identical blob |
| 21 | suite `node round-gate.mjs --selftest`, 60 checks | holds | `sweep/evidence/control.out`: 60 PASS, `ROUND_GATE_SELFTEST: 60/60 pass`; 60 `check(` sites |
| 21–22 | hermetic: under strace zero reads under `~/Projects`, no network (RGRecon) | holds (seat-recorded) | `RGRecon.md` §4: 0 `openat` under `/home/vgpnk/Projects`, 0 `AF_INET/AF_INET6`/`connect`; not re-traced by this seat |
| 22–24 | GIT_DIR hazard: fixture commits land in that repository | holds (seat-recorded) | `RGSentinel.md` S1/E1b: canary HEAD moves, fixture commits land, index rewritten |
| 24 | TMPDIR inside a work tree makes 3 checks fail | holds (seat-recorded) | `RGSentinel.md` S3/E2: FAIL [37], [56], [51] |
| 25–26 | sweep runs under `env -i` with private HOME/TMPDIR per defect | holds | `suite.txt` exact string: `h="$WORKDIR/sandbox-$DEFECT_ID"; … exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" …`; `sweep.log` target sits under the workdir |
| 26–27 | ledger leg carries the same string | holds | byte-equal comparison of `suite.txt` with the suite literal at `tools/mutate-and-run.sh:1221` (`equal: True`) |
| 28 | 8 pristine runs exited 0 with empty stderr | holds | retained `/tmp/tameshi-r16-RGControl-3092/ctrl{3,5}`: 8 `run-N.exit` all `0`, 8 `run-N.stderr` all 0 B |
| 28–29 | stdout differed every run; one `mkdtemp` suffix; 9 lines per run | holds | 8 distinct stdout sha256; each run has exactly one unique `selftest-XXXXXX` token occurring 9× in 63 lines |
| 30 | `tools/repeat-control.py` → `controls_mismatch` exit 1 (RGControl) | holds | `ctrl3/finding.txt`: `REPEAT_CONTROL: controls_mismatch` / `REPEAT_EXIT: 1`; `RGControl.md` |
| 30–31 | verdicts graded on exit only; the runner does exactly that | holds | `tools/mutate-and-run.sh:471-495`: control red on any nonzero exit; KILLED = exit ∉ {0,124,126,127}; SURVIVED = 0 |

### §1 Pre-registration, lines 35–47

| line | claim | mark | backing |
|---|---|---|---|
| 35–36 | ten defects + predictions committed in `e69b488`; committer date 2026-10-20T10:39:59-03:00 | holds | `git show --stat e69b488` includes `predictions.json` (74 lines) and `round-gate.defects.spec` (57); `git log -1 --format=%ci` matches exactly |
| 36 | pushed to origin | holds | `git branch -r --contains e69b488` → `origin/master`; `origin/HEAD` = `c699c8c`; ancestor check rc 0 |
| 36–37 | before any mutant ran; sweep 13:40:15Z = 10:40:15-03:00 | holds | commit 10:39:59-03:00 = 13:39:59Z; `sweep.log` 13:40:15Z (16 s later) |
| 37–38 | spec sha256 `e99b87eb…11c4` equals sweep `spec.copy` | holds | both files hash `e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4` |
| 38–39 | composition 5 kill-aimed (A1,A3,B1,E3,C1060) / 5 hole-aimed (C1059,A2,B2,CKIND,E1) | holds | `predictions.json.composition` = 5/5; spec header "composition 5 kill-aimed / 5 hole-aimed" |
| 40–41 | drawn from matrix §13 and `RGSpec{A,B,C,E}.spec` | holds | fragments contain A1/A2/A3 (A), B1/B2/B3 (B), C floor/kind/pass (C), E1/E2/E3 (E); RGSpecD's D1–D3 are in `rejected_candidates` |
| 41–43 | operator families follow S052 (string literal, equality/boundary, array declaration, conditional) + S056 boundary | holds, wording note | actual edits: string literal (A1,A2,A3,B1,B2), equality/boundary (E3), integer boundary (C1059/C1060), array declaration (CKIND), conditional (E1). S052's own row names equality, conditional, string literal, boolean, array declaration; `boundary` is S056, cited in the same sentence — the parenthetical conflates the two lists |
| 43–44 | rejected candidates/reasons in `predictions.json → rejected_candidates` | holds | key present with RGD-B3, RGC-PASS-COUNT, RGD1, RGD2, RGD3, RGE-2, RGC-THIN-FLOOR(512) |
| 44–47 | `INTERNAL_ERROR` token edit dropped: no input reaches the catch-all (SurvivorPrep P12) | holds | `SurvivorPrep.md` P12 (`:245-257`): uninhabited, `TMPDIR=/nonexistent` exits 1 with a raw node stack, never `INTERNAL_ERROR`; predictions `RGD-B3` reason matches |

### §2 Result, lines 51–73

| line | claim | mark | backing |
|---|---|---|---|
| 51 | tool sha256 `75ed934d…adc5` (r10-2, unchanged at sweep) | holds | `sweep.log` `MUTATE_TOOL: … sha256=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; `git show e69b488:tools/mutate-and-run.sh \| sha256sum` identical; header line 2 says `r10-2` |
| 52 | Control GREEN (exit=0), 0 inconclusive, `MUTATE_RESTORE: OK`, 32 s | holds | `sweep.log`: `CONTROL: GREEN (exit=0 duration-ms=2913 …)`, `MUTATE: DONE … inconclusive=0`, `MUTATE_RESTORE: OK`; sum of control + 10 defect durations = 32,278 ms |
| 53–54 | evidence `results.tsv`, `evidence/*.out`, `sweep.log` | holds | all present |
| 58 | A1: KILLED, exit 1, 10 checks `[1][2][3][12][16][21][22][27][46][47]` | holds | `A1.out` has exactly those 10 FAIL lines plus [51]; `results.tsv` exit 1 |
| 59 | A3: KILLED, exit 1, 2 checks `[52][53]`; rt8 prefix stays green | holds | `A3.out` FAIL [51],[52],[53]; [59] (rt8) PASS under mutated output |
| 60 | B1: KILLED, exit 1, `[32]` fcA, `[45]` jFc | holds | `B1.out` FAIL [32] (`fail-closed: --reports-dir missing`) and [45] (`--json fail-closed`) plus [51] |
| 61 | E3: KILLED, exit 1, `[54]` rt3 | holds | `E3.out` FAIL [54] (`--tracked: only one filed report`) plus [51] |
| 62 | C1060: KILLED, exit 1, `[8]` r8; its 1059 B report now `REPORT_THIN` | holds (re-executed) | `C1060.out` FAIL [8] `kinds=[REPORT_THIN,REPORT_ROUND_MISMATCH]` plus [51]; `fxMentions(10,'round-1')` = 1059 B; reconstructed mutant sha `432b4d504a5e5f3c694dbde498ec467fe42f374c5cbddf5ada3352f0fad66434` (= `results.tsv`) ran under the exact guarded string → rc 1, FAIL [8], FAIL [51], nested 59/60, outer 58/60 |
| 63 | C1059: SURVIVED, exit 0, 0 | holds | `C1059.out` 60/60, no FAIL; `results.tsv` exit 0 |
| 64 | A2: SURVIVED, exit 0, 0 | holds | `A2.out` 60/60; `results.tsv` exit 0 |
| 65 | B2: SURVIVED, exit 0, 0 | holds | `B2.out` 60/60; `results.tsv` exit 0 |
| 66 | CKIND: SURVIVED, exit 0, 0 | holds | `CKIND.out` 60/60; `results.tsv` exit 0 |
| 67 | E1: SURVIVED, exit 0, 0 | holds | `E1.out` 60/60; `results.tsv` exit 0 |
| 69–70 | every kill also fails [51]; nested tallies A1 50/60, A3/B1 58/60, C1060/E3 59/60 | holds | each kill `.out` has `FAIL [51]` with `tail=ROUND_GATE_SELFTEST: {50,58,58,59,59}/60 pass`; outer tallies are 49/57/57/58/58 (the note explicitly cites the nested tally) |
| 71 | [51] is a duplicate witness, not an independent assert | holds | [51] simply re-runs the suite and fails iff the nested run fails |
| 72–73 | **No check was skipped in any run**; `env -i` leaves `KUMITATE_ROUND_GATE_NESTED` unset; control 60/60 with no skips | **falls as worded (minor)** | top-level control and all 10 mutant `.out` files have 0 SKIP lines, and the control is 60/60 — true. But the [51] check spawns a nested run with `KUMITATE_ROUND_GATE_NESTED='1'` (`round-gate.mjs:1386`), which pushes `{ok:true, skipped:true}` (`:1381-1382`) and prints `SKIP [51/60]`; RGRecon §3 recorded that SKIP line. So a check *is* skipped in the nested run the sweep itself creates. |

### §3 What the case measures, lines 77–92

| line | claim | mark | backing |
|---|---|---|---|
| 77–78 | matrix §13.4 projected any floor in [26,1059] changes no fixture verdict | holds | `arm-class-matrix.md` §13.4: "A single edit … to any integer in **[26, 1059]** changes no fixture verdict"; §13.10 #3 arithmetic |
| 78–79 | 1059 survived; 1060 killed by exactly the 1059-byte r8 fixture | holds (re-executed for 1060) | `C1059.out` 60/60; C1060 above; `fxMentions(10,'round-1')` = 1059 B; all other read reports 1119–2100 B (matrix §13.10 #3) |
| 81–83 | tracked verdict full-line by rt1/rt2, prefix-only by rt8; tail reorder kills two, passes third | holds | `round-gate.mjs:1411` anchored `^…$`; `:1426` anchored; `:1481` `^ROUND_GATE: CLEAN \(mode=tracked checked=2 ` without `$`; A3 evidence [52]/[53] FAIL, [59] PASS |
| 84–86 | B1 vs B2 species asymmetry; no fixture runs `--tracked` with a missing reports dir (matrix §13.6 #2) | holds | `fxTrackedMain` always `mkdirSync(reports)` (`round-gate.mjs:828-848`); rt5 uses that existing dir with a non-git main; B2.out 60/60; matrix §13.6 #2 |
| 87–90 | meta-check one-sided; `FINDING_KINDS` read only at :171 and :1488 | holds | `grep -n FINDING_KINDS` → exactly `171:` declaration and `1488:` filter; `missing = FINDING_KINDS.filter(k => !observed.has(k))`; shrinking the enum can only shrink `missing` |
| 90–92 | mutant gate behaviour identical to pristine; equivalent for gate behaviour | holds | no other reader of FINDING_KINDS; non-selftest path unaffected |

### §4 Survivors, lines 96–111

| line | claim | mark | backing |
|---|---|---|---|
| 96–97 | harness is SurvivorPrep's `probes.mjs`, retained in `survivor-probes/` | holds | retained file sha256 `131c2835b1b5ce5fab60960fbca864c444d2cd75c19f08da410616e49bd332fb` equals the sha in `SurvivorPrep.md:66`; override interface `GATE`/`FXROOT` documented at `:69-77` |
| 97–98 | each probe runs on pristine and mutant copies | holds (re-executed) | direct re-runs with reconstructed mutants: P1 pristine 0 / mutant 1; P1b 0/1; P6 0/1; P9 0/1 |
| 102 | A2 P1 pristine 0 / mutant 1 | holds (re-executed) | mutant sha `d6aa922c…074f0` (= `results.tsv`); pristine rc 0, mutant rc 1 |
| 103 | A2 P1b pristine 0 / mutant 1 | holds (re-executed) | same mutant; pristine rc 0, mutant rc 1 |
| 104 | B2 P6 pristine 0 / mutant 1 | holds (re-executed) | mutant sha `a8af2f4c…0f299a` (= `results.tsv`); pristine rc 0, mutant rc 1 |
| 105 | E1 P9 pristine 0 / mutant 1 | holds (re-executed) | mutant sha `7d56ab89…b3aafcfd` (= `results.tsv`); pristine rc 0, mutant rc 1 |
| 106 | C1059: report sized in [1024,1058]; wave-2 seat `C1059Probe`; mutant — | **unbacked at the landing commit / now backed post-commit** | `git grep C1059Probe c699c8c` returns only this note line; `spec2.json` is untracked (mtime 10:51) and the `c1059-{pristine,mutant}.log` files are untracked (mtime 10:54), all after the 10:49:37 commit. The post-commit probe now reports `report_bytes=1040` (inside the range), pristine `exit=0 CLEAN`, mutant `exit=1 REPORT_THIN (bytes=1040)` |
| 107 | CKIND: no probe; equivalent for gate behaviour | holds | §3 argument; no behavioural reader |
| 109–110 | S057: deciding whether a mutant is equivalent is undecidable | holds | fetched the cited UCL preprint; §5.3.1 is PDF p. 29 and reads verbatim: "Detecting equivalent mutants is a well-known undecidable problem [28]." |
| 110–111 | **each survivor carries either an off-suite witness or an explicit equivalence argument** | **falls as worded at the commit (minor)** | at 10:49:37 C1059 had neither: it carried a plan naming a seat absent from every committed file. The post-commit probe (10:54) now supplies the witness, making the sentence true only as of that later artifact |

### §5 Ledger leg, lines 115–122

| line | claim | mark | backing |
|---|---|---|---|
| 115 | `js-round-gate` is the seventh leg of `--regression` | holds | `runner-regression.txt` runs cases 1–7 with `js-round-gate` last; `REGRESSION_EXPECT` lists seven |
| 116–117 | holds pin, rev, spec verbatim, table `A1:K …`, guarded suite | holds, wording note | spec heredoc sha `e99b87eb…` = committed spec; `PIN_ROUNDGATE`/`REV_ROUNDGATE` at `tools/mutate-and-run.sh:562-563`; suite literal byte-equal; `TABLE_ROUNDGATE` at `:570` is `A1:KILLED,A3:KILLED,…,E1:SURVIVED` — the note's `K`/`S` is shorthand, not the stored spelling |
| 118–119 | receipt at runner sha256 `89722ddb…5594`, `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0 | holds | `runner-regression.txt` first line has that sha; final line exact; `rc=0`; working-tree and `git show c699c8c:tools/mutate-and-run.sh` both hash `89722ddb…` |
| 120 | `--selftest` → `MUTATE_SELFTEST: 81/81 pass` | holds (re-executed) | ran committed bytes from /tmp: `MUTATE_SELFTEST: 81/81 pass`, `VERDICT: PASS`, rc 0 |
| 120–121 | 80 before; the leg-cut check gained the seventh tuple | holds (re-executed) | ran `git show e69b488:tools/mutate-and-run.sh` from /tmp: `MUTATE_SELFTEST: 80/80 pass`, rc 0; diff adds the seventh `lent` tuple and one per-leg check |
| 121–122 | both receipts in `runner-{regression,selftest}.txt` | holds | both files present with those names |

### §6 Limits, lines 126–135

| line | claim | mark | backing |
|---|---|---|---|
| 126 | one revision, one host: node v24.21.0, Linux 7.2.11 | holds | `node --version` → `v24.21.0`; `uname -r` → `7.2.11-arch1-1`; control.out header prints `node v24.21.0` |
| 128–130 | 50 % mixes kill/hole-aimed by design; accuracy and kill rate separate readings | holds | predictions composition 5/5; 10/10 measured = predicted |
| 131–135 | recommendations reported, not absorbed | holds | kumitate HEAD `1770305`, status 0 entries; no gate edit in the case evidence |

## 3. Findings

No blocking defect. Concrete gaps, all minor:

1. **`No check was skipped in any run` overstates the scope (lines 72–73).** The graded top-level control and mutants have zero SKIP lines (`control.out` and the 10 `evidence/*.out` all SKIP=0), so the intended point — the control's 60/60 is not inflated by skips — holds. But check [51] spawns a nested `--selftest` with `KUMITATE_ROUND_GATE_NESTED='1'` (`round-gate.mjs:1386`), and that nested run records a `skipped: true` result (`:1381-1382`) printed as `SKIP [51/60]` (verified independently by RGRecon §3). The word "any" makes the sentence false for the nested invocation.
2. **C1059 is deferred under an absolute completeness sentence (lines 106, 109–111).** At `c699c8c` the note was the only committed mention of `C1059Probe`; the wave-2 seat and its logs postdate the commit (spec 10:51, logs 10:54). The table row itself is honest (`—` for the mutant cell), but the following sentence claims every survivor already carries a witness or equivalence argument. It became true only after the post-commit probe (1040 B; pristine exit 0 CLEAN; mutant exit 1 `REPORT_THIN`). Recommend marking the sentence as dependent on wave 2, or landing the probe evidence in the same commit.
3. **`§5` table shorthand is not the stored table (lines 116–117).** `TABLE_ROUNDGATE` is `A1:KILLED,A3:KILLED,…,E1:SURVIVED`; the note renders `A1:K … E1:S`. Semantics match exactly, but the backticked string is not literal.
4. **Historical porcelain claim has no retained receipt (lines 8–9).** The full-tree `git --no-optional-locks status --porcelain` output "before and after" the sweep is not in any evidence file. The mechanism (only a /tmp copy is executed; `sweep.log` target is `/tmp/…`) and the current status (0 entries) support it, and wave-1 seats recorded the same state before the sweep (`SurvivorPrep.md:62`, `RGConnector.md:43`, `RGSource1.md:80`), but the sweep-time receipt is missing.
5. **S052 family attribution is loose (lines 41–43).** S052's row (`SOURCES.md:61`) names equality, conditional, string literal, boolean, array declaration; "boundary" belongs to S056 (`:65`), which the same sentence cites. No defect in the mutant set depends on this wording.

## 4. Executed

| command (cwd, scratch where relevant) | exit | key output |
|---|---|---|
| `git show c699c8c:…/mutation-case-kumitate-round-gate.md \| nl -ba` | 0 | 135 lines audited |
| `git -C kumitate show 364f1d5:scripts/round-gate.mjs \| sha256sum / wc -c / wc -l` | 0 | `f890e277…d3e9`, 80415, 1511 |
| `git -C kumitate ls-tree 364f1d5 scripts/round-gate.mjs` | 0 | `100755 blob 1f7d623e…` |
| `git -C kumitate rev-parse HEAD:scripts/round-gate.mjs` | 0 | `1f7d623e…` |
| `git -C kumitate log -1 --format=%H -- scripts/round-gate.mjs` | 0 | `364f1d5…` |
| `git log -1 --format='%H %ci' e69b488` | 0 | `2026-10-20 10:39:59 -0300` |
| `git branch -r --contains e69b488` | 0 | `origin/master`; `origin/HEAD` |
| `sha256sum round-gate.defects.spec sweep/spec.copy` | 0 | both `e99b87eb…11c4` |
| `sha256sum tools/mutate-and-run.sh`; `git show c699c8c:… \| sha256sum`; `git show e69b488:… \| sha256sum` | 0 | `89722ddb…5594`; `75ed934d…adc5` |
| `bash /tmp/…/runner-e69/mutate-and-run.sh --selftest` (committed e69b488 bytes) | 0 | `MUTATE_SELFTEST: 80/80 pass` |
| `bash /tmp/…/runner-c699/mutate-and-run.sh --selftest` (committed c699c8c bytes) | 0 | `MUTATE_SELFTEST: 81/81 pass` |
| awk-extract of the `js-round-gate.spec` heredoc from `tools/mutate-and-run.sh` → `sha256sum` | 0 | `e99b87eb…11c4` (equal to spec) |
| Python equality of `suite.txt` and runner suite literal at `:1221` | 0 | `equal: True` |
| control artifact audit: 8 `run-N.exit`, `run-N.stderr`, stdout sha/token counts | 0 | 8× exit 0, 8× stderr 0 B, 8 distinct stdout shas, 9 token occurrences/run, 63 lines |
| `node -e` recompute of `fxMentions(10,'round-1')` byte length | 0 | 1059 |
| reconstructed C1060 mutant + exact guarded suite run | 1 | mutant sha `432b4d50…`; FAIL [8], FAIL [51]; nested 59/60, outer 58/60; stderr 0 B |
| reconstructed A2 mutant; `probes.mjs P1` pristine/mutant | 0 / 1 | mutant sha `d6aa922c…` (= results.tsv); P1 all-pass / FAIL(1) |
| reconstructed A2 mutant; `probes.mjs P1b` pristine/mutant | 0 / 1 | P1b all-pass / FAIL(2) |
| reconstructed B2 mutant; `probes.mjs P6` pristine/mutant | 0 / 1 | mutant sha `a8af2f4c…`; P6 all-pass / FAIL(2) |
| reconstructed E1 mutant; `probes.mjs P9` pristine/mutant | 0 / 1 | mutant sha `7d56ab89…`; P9 all-pass / FAIL(2) |
| `curl` + `pdftotext` S057 UCL preprint; section/page locate | 0 | §5.3.1 on PDF p. 29: "Detecting equivalent mutants is a well-known undecidable problem" |
| `git grep C1059Probe c699c8c` | 0 | only `corpus/knowledge/mutation-case-kumitate-round-gate.md:106` |
| `git --no-optional-locks -C kumitate status --porcelain \| wc -l` | 0 | `0` |
| `node --version`; `uname -r` | 0 | `v24.21.0`; `7.2.11-arch1-1` |

Not re-executed (seat-recorded backing only): the RGRecon strace, the RGSentinel hazard experiments, the RGControl repeat-control invocation, and the original 10-mutant sweep. Three mutants (A2, B2, E1) were reconstructed byte-identically to `results.tsv`, one kill (C1060) was re-swept end-to-end, and all 11 sweep `.out` files were read line-by-line.

## 5. Residual risk

- The sweep's own 5/10 headline was not re-run in full; it rests on retained `results.tsv` + `.out` files plus the byte-identical C1060 re-run. A full re-sweep is the only way to close that gap.
- The strace and environment-hazard claims are accepted from RGRecon/RGSentinel reports; their traces/logs were not reproduced here.
- The historical "before and after" porcelain state at sweep time is unrecoverable from the repository; only the mechanism and the current clean tree support it.
