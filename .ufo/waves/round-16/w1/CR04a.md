# CR04a — cold-read: SKILL.snapshot.md lines 131–245

Seat: CR04a. Snapshot sha256 verified: `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580`
(1704 lines; copied to `/tmp/tameshi-r16-CR04a-1/SKILL.snapshot.md`, `sha256sum` match).
Lane root untouched; all writes under `/tmp/tameshi-r16-CR04a-1/` except this report.

## Range structure

Exactly one section: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`
(heading line 131, body through 244; next heading at 246). Classification: **instruction**
(the entire section is a numbered 10-step recipe telling the reader what to run, pin,
pre-register, adjudicate, probe and record).

## Execution — the recipe run end-to-end

The section designates **no specific artifact** for a cold reader to mutate — finding, see
below — so I executed on the artifact the section's own model case pins: kumitate
`scripts/kimi-census.mjs` @ `175de6ba2e9e904010411b19cab27e0af9aad3d4` (the section's
worked example, mutation-case-kimi-census.md). NOT round-gate.mjs (C1 target, wave-1
ban respected). Manifest replayed D1–D10 verbatim plus two blind additions (X1, X2)
since step 4 requires a reader-written defect list; total 12, inside the 8–12 band.

Per-step evidence (all under `/tmp/tameshi-r16-CR04a-1/work/`):

| step | instruction | executed | result |
|---|---|---|---|
| 1 | control must run hermetically, print `n/m pass` + `VERDICT:` | `node pristine.mjs --selftest` | exit 0, `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, 0.63 s |
| 2 | pin committed bytes: sha256, size, lines, mtime, rev, porcelain | `git show 175de6ba:scripts/kimi-census.mjs` | sha256 `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, 896 L, 43273 B; `git status --porcelain` for path **empty** |
| 3 | copy pristine to scratch, re-verify | `cp`→scratch, `sha256sum` | copy sha identical |
| 4 | defect list from next section's template, `expect:` pre-registered | `manifest.md` written BEFORE any mutant run | 12 entries; D1–D10 informed replay, X1/X2 blind |
| 5 | `--check` uniqueness gate, literal `all unique` | `python3 mutate_driver.py --check` | first run **UNIQUENESS FAILURE** on D9 (count=2, lines 292+305 share `kind === 'dir' : isLeaf(kind)`); re-derived `old` to `? (m.kind === 'dir' ? … : isLeaf(kind))` → count=1, `all unique`. Gate demonstrably fail-closed. |
| 6 | control + mutants, fresh copy, literal replace, sha≠, timeout, per-run evidence | `python3 mutate_driver.py --run` (300 s bound) | 13 runs in 8.58 s; `evidence/{control,D1..D10,X1,X2}.selftest.txt` + `.meta.json` + `results.json` |
| 7 | adjudicate exit AND verdict AND full count | per-run summary lines | below |
| 8 | probe every survivor on out-of-fixture input | `node mutant-D2/D10.mjs --root empty-root/` | D2: 5 ids + `+23 more` vs pristine 6 + `+22 more`; D10: `frozen=24` vs `frozen=25`. Non-equivalent, verbatim per note :82-99. |
| 9 | restore proof: sha/size/mtime/porcelain | `git show` re-sha + `git status` | pinned blob sha unchanged `83016d45…`; porcelain empty; `cmp` vs worktree file differs (substrate legitimately at `1770305f`, 44770 B — committed-drift, not writes; recipe pins *committed bytes*) |
| 10 | record sweep: table, tally, survivors, reproduce, calibration, unknowns | this report + manifest + evidence dir | below |

### Kill-rate table (measured, exit / suite line / verdict)

| id | expect (pre-registered) | measured | labels |
|---|---|---|---|
| control | green | 0 / `43/43 pass` / PASS | — |
| D1 | killed | 1 / `27/43` / FAIL | 16 (incl. exact baseline, verbatim list collected) |
| D2 | survived | 0 / `43/43` / PASS | survivor, probe ✓ |
| D3 | killed | 1 / `27/43` / FAIL | 16 |
| D4 | killed | 1 / `40/43` / FAIL | 3 (planted/hidden root child, orthogonal arm) |
| D5 | killed | 1 / `42/43` / FAIL | 1 (no-chain tripwire) |
| D6 | killed | 1 / `41/43` / FAIL | 2 (floor + FIFO collateral) |
| D7 | killed | 1 / `41/43` / FAIL | 2 |
| D8 | killed | 1 / `40/43` / FAIL | 3 (three fail-closed cases) |
| D9 | killed | 1 / `41/43` / FAIL | 2 (FIFO + dangling-symlink secrecy cases) |
| D10 | survived | 0 / `43/43` / PASS | survivor, probe ✓ |
| X1 `childCount: 18→19` (:137) | killed, predicted 3–6 cases | 1 / `21/43` / FAIL | **22** — PREDICTION MISS (calibration datum) |
| X2 isLeaf `&& kind !== 'fifo'` (:205) | killed, predicted 1–3 | 1 / `42/43` / FAIL | 1 (FIFO secrecy case exactly) |

**Kill rate 10/12 = 83 %**; manifest replay alone 8/10 = 80 %, reproducing the note's
headline exactly. Zero inconclusive; every run enumerated `n/43`. Duration 8.58 s for
13 runs (~0.66 s each) vs 300 s bound; node v24.21.0, python 3.14.8, host x86_64.

### Calibration data earned

- **X1 miss**: predicted 3–6 failing cases, measured 22. Cause (same shape as note E1):
  `childCount` is the enumeration table — the fixture generator loops `e.childCount`
  times (`:449`), so +1 fabricates a phantom live child that also breaks UNLISTED,
  secrecy, MEMBER_MISSING and SHAPE cases. Resolves kimi-census **U1** partially in the
  downward direction: desyncing `:137` alone IS caught, more broadly than `'19 children,
  18 declared'` explains — the desync corrupts the fixtures themselves, not just the
  count strings.
- X2 hit exactly its predicted 1-case kill (FIFO fixture).
- The step-5 gate caught my own transcription error (D9 `old` count=2) before any run —
  a lived demonstration of why `all unique` is fail-closed.

## Anchor re-checks (record claim clusters)

- kimi-census pin cluster :13-16 → sha/896/43273/rev all re-verified ✓; porcelain empty ✓.
- Control shape :20-21 → `43/43 pass` / `VERDICT: PASS` / exit 0 reproduced ✓.
- Driver gates :22-25 → `all unique` + count==1 reproduced; `new != old` assert in driver ✓.
- Kill-rate :29-33 → 8/10, 11 runs, no inconclusive, count held — reproduced (10/12 incl. extras) ✓.
- Kill labels :59-76 → D4=3, D5=1, D6=2, D7=2, D8=3, D9=2, D1/D3=16 each — all verbatim ✓.
- Survivor probes :82-99 → `+23 more`, `frozen=24` reproduced byte-exact ✓.
- Cost :204-205 → 7.0 s/11 runs on v24.21.0; my 8.58 s/13 same magnitude ✓.
- Recipe's kagi cites: surface-census.sh pin `275d8294…53009f`, 44212 B, 886+partial-887
  line, rev `fecee874` (kagi note :13-17) — internal consistency with the note's §7
  reproduce block verified by reading; live kagi repo HEAD is now `c2cab35b` (moved).
- `gates-survey-kumitate.md:19-31` → the `n/m` + `VERDICT:` shape table holds
  (round-gate `60/60`, kimi-census `43/43` rows verbatim) ✓.
- `corpus/README.md` G-R2-1 row → dirty-pin errata present at line 11 (`93c5827202b9cdec`
  corrected pin) ✓; gates-survey-kagi.md G-R2-1 errata block present :554-561 ✓.

## Findings for the ledger

1. **Executed-ok overall**: every instruction executable without oral context; every
   named file resolved and its cited anchors held. The step-4 cross-reference ("next
   section", 246–313) is required material and readable.
2. **gap-minor — no designated target**: step 1 says "pick the target" and names only
   shape requirements; a cold reader must independently locate a sibling suite
   (`kumitate-shokunin/scripts/*.mjs`, `kagi-shokunin/corpus/*.sh`) — the section assumes
   knowledge that those repos exist as siblings and where the model artifacts live.
   Resolved here by the in-range citations `kimi-census.mjs`/`surface-census.sh`, so
   non-blocking, but a reader who skips to the recipe cold has no path literal.
   Bounded fix suggestion (L1's call): one line in step 1 naming an example artifact
   path pattern, e.g. "the two worked sweeps targeted `<kumitate>/scripts/kimi-census.mjs`
   and `<kagi>/corpus/surface-census.sh`".
3. **gap-minor — driver not provided**: step 5/6 assume a `mutate_driver.py` with
   `--check`/`--run`; the notes show its *spec* but no source. I authored one in ~80
   lines from the description alone and it behaved correctly (caught my own D9
   non-uniqueness). Non-blocking; arguably intentional (the reader proves the contract).
4. **Restore-step wording**: step 9 says "size and mtime unchanged" — on a *moving*
   substrate these only hold per-force if the artifact hasn't legitimately drifted; my
   worktree copy had legitimately moved (44770 B vs pinned 43273 B) while committed-pin
   checks held. The correct reading ("committed bytes only", step 2) makes this
   self-consistent; flagging only that a literalist could misread step 9 as asserting the
   live file never moves.
5. `mutate_driver.py` `--run` re-runs `--check` first (as the notes imply); recommend
   that ordering be explicit in step 6's prose — it is implicit in "both lanes' drivers".

## Tooling directive record

No installs or upgrades performed. Used: node v24.21.0, python 3.14.8, git 2.56.0,
bash coreutils — all pre-installed. No pacman transactions (pause honored).

## Opened paths

`/tmp/tameshi-r16-CR04a-1/SKILL.snapshot.md` (lines 131-245 assigned; 246-313 as
range-named dependency of step 4); `tameshi-shokunin/corpus/knowledge/mutation-case-kimi-census.md`
(full); `…/mutation-case-kagi-census.md` (full); `…/gates-survey-kumitate.md` (lines 1-43);
`…/gates-survey-kagi.md` (grep-located errata lines 4-8, 429-433, 554-564);
`tameshi-shokunin/corpus/README.md` (grep-located rows 7-15, 47-61);
`kumitate-shokunin` git objects only (`show`, `status`, `log`, `hash-object` — no
checkout/write); kagi repo `rev-parse`/`status` only. Scratch: `/tmp/tameshi-r16-CR04a-1/`.

```json
{"seat":"CR04a","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[{"start":131,"heading":"## Mutation-sweep recipe — numbered steps; bounded cold-read evidence","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["step 1 names no concrete target artifact or sibling path — reader must infer kumitate-shokunin/scripts/*.mjs / kagi-shokunin/corpus/*.sh from the citations","steps 5-6 assume a mutate_driver.py --check/--run that exists only as behavioral spec in the cited notes; I authored one from the description (worked, and its gate caught my own non-unique @old)","step 9 'size and mtime unchanged' can be misread on a legitimately drifted worktree; correct reading is committed-bytes-only per step 2","step 6 does not state that --run should re-run the uniqueness check first (my driver did; the notes imply it)"],"commands_executed":["sha256sum /tmp/tameshi-r16-CR04a-1/SKILL.snapshot.md","git -C kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs > work/pristine.mjs","node work/pristine.mjs --selftest  (exit 0, 43/43 pass, VERDICT: PASS)","python3 work/mutate_driver.py --check  (first run UNIQUENESS FAILURE on D9 count=2; fixed; all unique)","python3 work/mutate_driver.py --run  (control+12 mutants, 8.58s, 300s bound)","node work/mutant-D2.mjs --root work/empty-root  (+23 more vs +22 more)","node work/mutant-D10.mjs --root work/empty-root  (frozen=24 vs 25)","git -C kumitate-shokunin status --porcelain -- scripts/kimi-census.mjs  (empty)","git -C kumitate-shokunin show 175de6ba…:scripts/kimi-census.mjs | sha256sum  (83016d45… unchanged after sweep)"],"opened":["/tmp/tameshi-r16-CR04a-1/SKILL.snapshot.md:131-245","/tmp/tameshi-r16-CR04a-1/SKILL.snapshot.md:246-313","corpus/knowledge/mutation-case-kimi-census.md","corpus/knowledge/mutation-case-kagi-census.md","corpus/knowledge/gates-survey-kumitate.md:1-43","corpus/knowledge/gates-survey-kagi.md (errata lines 4-8,429-433,554-564)","corpus/README.md (rows 7-15,47-61)","kumitate-shokunin git objects @175de6ba and @HEAD (read-only)","kagi-shokunin rev-parse/status (read-only)"],"scratch":"/tmp/tameshi-r16-CR04a-1"}]}
```
