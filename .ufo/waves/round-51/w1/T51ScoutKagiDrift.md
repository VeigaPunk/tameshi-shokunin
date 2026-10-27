# T51ScoutKagiDrift — what kagi says `drift-pins.sh` guarantees, and which defect breaks which guarantee

Seat: scout (read-only). Milestone: C2 owner intent. Round 51, tameshi lane.
Substrate read: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin` at HEAD `69b61db` via `git show` only (nothing written there).
Gate bytes: `git show HEAD:corpus/drift-pins.sh | sha256sum` → `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`; `git log --oneline -- corpus/drift-pins.sh` → only `e64e81b` (round 9) and `5f55ba8` (round 6). The gate at HEAD is byte-identical to the pin; no later kagi commit touched it or `corpus/knowledge/drift-gate.md` (`git log -- corpus/knowledge/drift-gate.md` → `e64e81b` is the newest content commit besides round-22 erratum `8ada17a`).
Labels: **[OBS]** observed with the named command · **[INF]** inference.
Line numbers: `D:` = kagi `corpus/drift-pins.sh` at HEAD; `K:` = kagi `corpus/knowledge/drift-gate.md` at HEAD; `R9:` = kagi `corpus/lessons/round-9.md`; `T:` = tameshi lane file.

## 1. The owner's record (what kagi says the gate guarantees)

Find command: `git -C kagi-shokunin grep -l drift-pins HEAD -- corpus/knowledge` → `drift-gate.md`, `checklist-execution.md`, `claim-ledger.md`, `substrate-deferral.md`, `surface-census.md`. Only `drift-gate.md` is the gate's own entry.

**[OBS] Header contract, `D:2-36`** (the guarantees the ten defects are mapped against):
- `D:9-10` two committed data files: baseline `path mode lines sha256`, symbols `path line ERE [shape]`.
- `D:12-13` file verdicts `OK|DRIFT|MISSING|LINK|UNPINNED|EXTRA|DUP|POLICY`.
- `D:14-18` symbol verdicts `OK|MOVED|GONE|AMBIG <n>|COUNT (#N line pins a count)|SHAPE (only for a shape row on a no-hash dotenv file)`.
- `D:19` exit 0 clean · 1 any drift · 2 usage/setup error (nothing written).
- `D:21-25` secret hygiene: no-hash paths pinned by mode+lines only, sha field `-`; nothing prints file content.
- `D:29-30` `--pin` records, never repairs; `D:31` `--selftest` "scratch-tree proof that the gate fires"; `D:32-33` `--baseline/--symbols` alternate pair — "membership check skipped".
- In-body guarantee comment `D:164-165`: "Membership is closed in both directions, and duplicate rows are defects" (`UNPINNED`, `EXTRA`, `DUP`); `D:166-168`: skipped for an alternate baseline.

**[OBS] Round-9 commit `e64e81b` message** (`git show -s --format=%B e64e81b…`): "drift gate with committed baselines"; `--selftest (13 cases on a scratch tree)`; "enforced NOHASH policy (POLICY verdict before any read)"; "LINK for symlinks AND hardlinks"; "EXTRADUP/EMPTY guards".

**[OBS] Knowledge entry `K:`**: verdict table `K:66-84` (every verdict above incl. `LINK … nlink>1 … Round-9 L2 critic found the hardlink variant` `K:73`, `POLICY … refused before the file is read` `K:77`); hash policy `K:90-112`; `--pin` semantics `K:114-133` ("a pin can absorb a line move but never a vanished or duplicated claim" `K:127-128`); bounds `K:135-165`; reproduction `K:167-193`; falsification `K:195-202`. The selftest list is `K:189-193`: "clean, content drift, restored, mode drift, missing file, symbol moved, symbol gone, symbol ambiguous, symlink, count drift, final clean, dotenv shape drift, shape restored — all on a `mktemp -d` scratch tree … host untouched."

**[OBS] Where the selftest is advertised elsewhere:**
- `corpus/README.md:36` — "`--selftest` (13 cases: content/mode drift, missing, **symlink+hardlink**, symbol moved/gone/ambiguous, count drift, dotenv shape drift, clean); vocabulary incl. `POLICY`/`EXTRA`/`DUP`/`EMPTY`/`SHAPE`".
- `SKILL.md:183` — "scratch-tree proof that the gate fires (13 cases)"; `SKILL.md:45` decision-table row lists the verdict words `DRIFT/MISSING/LINK/UNPINNED/EXTRA/DUP/POLICY/EMPTY` and `MOVED/GONE/AMBIG/COUNT/SHAPE`, exit 2 "usage/setup, nothing written".
- `R9:77-82` lesson 8: "The gate's own selftest is part of the deliverable. 13 cases … Without it, the new verdicts (`POLICY`, `SHAPE`, `EMPTY`, `EXTRA`, `DUP`) would be untested prose."

**[OBS] Later notes on the selftest:** none specific to `drift-pins.sh`. `git grep -n -i 'mutant\|mutation\|survivor' HEAD -- corpus ':!corpus/lessons' | grep -i drift` returns only unrelated lines (`scope-gate --falsify`, surface-census prose). The general lesson that applies is `corpus/lessons/round-21.md:115-122` ("a selftest that proves each finding fires does not prove nothing can pass unseen; mutations that should fail but did not are the missing half") and criterion `corpus/QUALITY.md:41` QM3. Kagi has never run a mutation sweep over this gate.

**[OBS] The lane's own earlier statements:**
- `T:corpus/knowledge/gates-survey-kagi.md:27` — drift-pins 451 L / 19088 B / `c138d34c7f0dfe95`, 13 cases, "lightest" suite (`:69`); `:52` `DRIFT_SELFTEST: PASS (13 cases)`; `:81` exit lattice anchored at `drift-pins.sh:19`; `:217` source-check table "`corpus/README.md:36` | drift-pins "13 cases" | 13 | yes" (the count was checked; the case list in the same cell was not).
- `T:corpus/knowledge/fleet-kill-rate-ledger.md:119` — "| drift-pins | 13 | `c138d34c7f0dfe95` | unmeasured by sweep; hermetic |"; `:280` keeps it among the eight standing queue rows. Command: `sed -n 119p corpus/knowledge/fleet-kill-rate-ledger.md`.
- Neither statement predicted a survivor count for this gate (the neighbouring rows at `:117-118` say "expect low survivor count"; `:119` says only "hermetic").

## 2. Defect → guarantee table

Spec: `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`. Sweep: `.ufo/evidence/round-51/c2/sweep/results.tsv`. "Neutral" = my scratch re-run (§3) with a sandbox directory name containing no verdict word.

| Defect | Code site (D:) | Guarantee it breaks (owner text) | Selftest case that should catch it | Sweep verdict | Neutral-name re-run |
|---|---|---|---|---|---|
| K_MODE_CMP | `:154` | `DRIFT … mode` verdict `D:12`; baseline mode column `D:9`; `K:71` | "mode drift" `D:413-414` (`DRIFT.*mode`) | KILLED | KILLED (exit mismatch: exit 0 want 1) |
| K_GONE_ARM | `:231-233` | `GONE` symbol verdict `D:14`; `K:80` "claim text absent"; `K:127` "a pin … never [absorbs] a vanished … claim" | "symbol gone" `D:422-423` (`GONE`) | SURVIVED | **KILLED** (`no /GONE/ in output`) |
| K_AMBIG_GT | `:234` | `AMBIG <n>` `D:14`; `K:81` "ERE now matches n>1 lines, so the pin cannot resolve" | "symbol ambiguous" `D:425-426` (`AMBIG`) | SURVIVED | **KILLED** (`no /AMBIG/ in output`) |
| K_COUNT_GE | `:210` | `COUNT` `D:15-16`; `K:44` "assert the ERE matches exactly N lines"; `K:82` | "count drift" `D:431-432` (`COUNT.*#1->#2`) | KILLED | KILLED (`no /COUNT.*#1->#2/`) |
| K_SHAPE_OPTIN | `:220` | `SHAPE` `D:17-18`; `K:44-47` "a malformed line cannot hide behind a correct count"; `K:83` | "shape drift" `D:435-436` (`SHAPE`) | SURVIVED | **KILLED** (`no /SHAPE/ in output`) |
| S_SHA_CMP | `:156` | baseline sha256 column `D:9`; `DRIFT … sha` `K:71`; hash tier `K:97` ("mode + lines + sha256"); the gate's reason to exist (`K:11-21`: v1 "could not detect drift"); the hand falsification at `K:172-176` (`DRIFT … sha deadbeef0b7e->2408b0c90b7e`) | none — "content drift" `D:409-410` appends a line, so `lines` already differs | SURVIVED | SURVIVED (13/13 PASS) |
| S_HARDLINK | `:135` | `LINK` "for symlinks AND hardlinks" (commit `e64e81b` message); `K:73` "(a hardlink — the path is not uniquely the file)"; `README.md:36` "symlink+hardlink" | none — "symlink" `D:428-429` uses `ln -s` only | SURVIVED | SURVIVED (13/13 PASS) |
| S_POLICY | `:145` | `POLICY` `D:13`; secret hygiene `D:21-25`; `K:77` "refused **before** the file is read"; hash policy `K:90-112` | none — scratch `env.txt` row carries sha `-` (`D:394`); no case passes a hash for a no-hash path | SURVIVED | SURVIVED (13/13 PASS) |
| S_DUP_UNIQ | `:188` | "duplicate rows are defects" `D:164-165`; `DUP` `D:12`; `K:76`, `K:75` ("membership is closed in both directions") | none, and none *possible as built*: the block runs only when `$BASELINE == $DEFAULT_BASELINE` (`D:168`) and `run()` always passes `--baseline` (`D:400`) | SURVIVED | SURVIVED (13/13 PASS) |
| S_USAGE_EXIT | `:88` | exit `2` "usage/setup error (nothing written)" `D:19`; `K:84`; `SKILL.md:45` "2 usage/setup, nothing written" | none — `run()` only passes known flags (`D:400`); `K:171` hand-checks the missing-argument arm (`D:85`), not the unknown-argument arm (`D:88`) | SURVIVED | SURVIVED (13/13 PASS) |

**[OBS] Neutral re-run counts:** 5/10 killed — all 5 kill-aimed, 0/5 hole-aimed — against the sweep's 2/10. The three sweep misses (K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN) flip; the five S_* hole-aimed mutants still survive; the pre-registered predictions (5 kill / 5 hole) hold exactly with neutral names.

## 3. Independent confirmation of the sandbox-name probe

Command (scratch, nothing in the lane): pristine blob from `git -C kagi-shokunin show e64e81b8…:corpus/drift-pins.sh` (sha256 `c138d34c…0feb` ✔), apply each spec `@old`→`@new` (asserting each `@old` matches exactly once in the pinned bytes), `chmod 755`, run `env -i PATH=… HOME=$h/home TMPDIR=$h/tmp LC_ALL=C bash MUTANT --selftest` from `$h` where `$h` is `sandbox-<DEFECT_ID>` or `neutral-q7`. Output, abridged:

```
K_MODE_CMP    sandbox 1 FAIL mode drift: exit 0 want 1
K_MODE_CMP    neutral 1 FAIL mode drift: exit 0 want 1
K_GONE_ARM    sandbox 0 DRIFT_SELFTEST: PASS (13 cases)
K_GONE_ARM    neutral 1 FAIL symbol gone: no /GONE/ in output
K_AMBIG_GT    sandbox 0 DRIFT_SELFTEST: PASS (13 cases)
K_AMBIG_GT    neutral 1 FAIL symbol ambiguous: no /AMBIG/ in output
K_COUNT_GE    sandbox 1 FAIL count drift: no /COUNT.*#1->#2/ in output
K_COUNT_GE    neutral 1 FAIL count drift: no /COUNT.*#1->#2/ in output
K_SHAPE_OPTIN sandbox 0 DRIFT_SELFTEST: PASS (13 cases)
K_SHAPE_OPTIN neutral 1 FAIL shape drift: no /SHAPE/ in output
S_SHA_CMP / S_HARDLINK / S_POLICY / S_DUP_UNIQ / S_USAGE_EXIT: PASS (13 cases) in both
```

**[OBS] Mechanism** (matches the L1's account): `D:403` is `grep -q "$3" <<< "$out"`, an unanchored substring match over the whole captured output, and that output prints scratch paths (`D:158` `DRIFT   %s …`, `D:140` `MISSING %s`, `D:203` `GONE %s:…`). In the "symbol gone"/"ambiguous"/"shape drift" cases `b.txt`/`env.txt` is rewritten, so a file-level `DRIFT <scratch>/b.txt …` line prints, and a path with `sandbox-K_GONE_ARM` satisfies `GONE`. `K_COUNT_GE`'s expected pattern `COUNT.*#1->#2` and `K_MODE_CMP`'s exit-code compare cannot be satisfied by a path, which is why those two were killed in both arms. The unanchored `DRIFT` expectation at `D:410` is a second, weaker instance: it also matches the `DRIFT_PINS:` summary prefix on every run, and the case rests on exit code alone ([INF]; not mutated).

**[INF] Exposure in kagi's own runs:** the gate's selftest scratch is `mktemp -d` (`D:376`), i.e. `$TMPDIR/tmp.XXXXXXXXXX`; a verdict word appears only if `TMPDIR` or the random suffix contains one (the suffix chance is ≈ 1e-6 per word). So kagi's *own* runs are not blind in practice; the blind spot is real but needs a caller-chosen name. It is a latent weakness of the check (`D:403`), and it is the harness's naming choice that exposes it.

## 4. Claims in the owner record that the selftest does not support

1. **README overclaim.** `corpus/README.md:36` lists "symlink+hardlink" among the 13 selftest cases. **[OBS]** the selftest has one link case, `ln -s` (`D:428-429`); `K:189-193`, `R9:77-82` and the commit message list the symlink only; no `ln` without `-s`, no `stat -c %h` expectation exists in `D:373-446` (`git show HEAD:corpus/drift-pins.sh | sed -n 373,446p | grep -n 'ln '` → one line, `ln -s`). The hardlink guard (`D:133-138`, `K:73`, commit message) has no selftest witness; S_HARDLINK survives for that reason. Command: `git -C kagi-shokunin show HEAD:corpus/README.md | sed -n 36p`. The lane's own `gates-survey-kagi.md:217` marked this README cell "yes" after checking only the number 13.
2. **Lesson 8 overclaim.** `R9:77-82` says the selftest exists so that `POLICY`, `SHAPE`, `EMPTY`, `EXTRA`, `DUP` are not "untested prose". **[OBS]** of those five only `SHAPE` has a case (`D:435-436`); `POLICY`, `EMPTY`, `EXTRA`, `DUP` (and `UNPINNED`) appear in no `run` call (`git show HEAD:corpus/drift-pins.sh | sed -n 373,446p | grep '^  run ' | grep -c 'POLICY\|EMPTY\|EXTRA\|DUP\|UNPINNED'` → 0; a bare grep for those words in the selftest body hits only comments and `DRIFT_EXTRA_NOHASH`). `R9:82-83` notes `UNPINNED` fired for real in a landing window, which is an incident, not a regression case.
3. **`--selftest` = "proof that the gate fires" (`D:31`, `SKILL.md:183`).** **[OBS]** no `run` case reaches the hardlink arm of `LINK` (`D:133-138`), `UNPINNED`, `EXTRA`, `DUP`, `POLICY`, `EMPTY`, any exit-2 path, or any of `--pin` (`D:262-371`, `K:114-133`). `K:171` and `K:178-182` demonstrate exit 2 (missing-argument arm only), sha drift and `POLICY` by hand — the owner's record treats these as manual reproduction, which is why the hole-aimed mutants S_SHA_CMP, S_POLICY and S_USAGE_EXIT survive an automated suite while having a documented manual witness.
4. **Structural, not an oversight, for DUP/EXTRA/UNPINNED.** `D:32-33`/`D:166-168` state that membership checks are skipped under `--baseline`; the harness depends on `--baseline` (`D:400`). The suite therefore cannot reach `S_DUP_UNIQ` without a harness change ([INF]: `BASELINE` defaults to `$SCRIPT_DIR/drift-baseline.tsv` `D:40`, so a copied script beside its own baseline plus `HOME=$d` would reach the default-baseline arm; not run by me — see the sibling witness seats).
5. Minor, unrelated to C2: `K:4` says `drift-symbols.tsv` has 20 rows while `K:3` and the commit message describe the round-9 build at 19 (a round-12 row was added, `PROVINCE.md:47`); `K:169` quotes `symbols=20`. Not a defect of the gate.

## 5. Recommendations as report lines (owner = kagi; recommendations only, per `PROVINCE.md:14-18`; adjacency: never absorbed — the tameshi lane edits nothing in kagi)

- R-1 `corpus/drift-pins.sh:403` — verdict check is an unanchored substring `grep -q "$3"` over output that embeds the scratch path (`:140,:158,:203`). Anchor to line start (`grep -q "^$3"`; every expected token at `:408-438` begins a line) or compare against output with the scratch prefix stripped. Witness: neutral vs `sandbox-<ID>` names in §3 (3 kill-aimed mutants flip).
- R-2 `corpus/README.md:36` — "symlink+hardlink" names a case that does not exist (`D:428-429` is `ln -s`); either add a hardlink case (`ln "$d/b.txt" "$d/b.h"` → expect `LINK.*hardlink`) or drop the word. Same row lists `POLICY`/`EXTRA`/`DUP`/`EMPTY` as vocabulary, not as selftest cases — keep that distinction explicit.
- R-3 `corpus/lessons/round-9.md:77-82` — lesson 8 says `POLICY`/`EMPTY`/`EXTRA`/`DUP` are not untested prose; they are. The lesson is append-only for kagi's lane records; record an erratum rather than an in-place edit.
- R-4 `corpus/drift-pins.sh:408-438` — no case holds a **sha-only** drift (same length, same mode): add content `alpha`→`alphX` style edit expecting `DRIFT.*sha` (kills S_SHA_CMP).
- R-5 `corpus/drift-pins.sh:394` — add one no-hash row whose baseline sha is not `-` and expect `POLICY` exit 1 (kills S_POLICY; `K:178-182` already gives the hand witness).
- R-6 `corpus/drift-pins.sh:400` — add one direct invocation with an unknown argument expecting exit 2 and an unknown-argument line (kills S_USAGE_EXIT; `K:171` covers only the missing-argument arm `D:85`).
- R-7 `corpus/drift-pins.sh:168` — make the membership block (`UNPINNED`/`EXTRA`/`DUP`, `D:164-189`) reachable from the selftest (parameterise the FILES list and baseline, or drive a copied script with `HOME=$d`); until then `DUP`/`EXTRA`/`UNPINNED` have no regression case and the header's "Membership is closed in both directions" is an assertion about code the suite cannot reach.
- R-8 `corpus/knowledge/drift-gate.md:189-193` — if R-4..R-7 land, update the 13-case list and every pinned count (`README.md:36`, `SKILL.md:183`, `claim-ledger.tsv` R11-05, `self-counts.tsv`); today's list is accurate to the code, README:36 is not.
- R-9 (outside the ten defects, noted for the owner) `--pin` (`D:262-371`, `K:114-133`) has no selftest case at all: the refusal list (`GONE`, `AMBIG`, changed count, missing/linked source) is exit-2-and-nothing-written code with prose-only evidence.

## 6. Notes for the C2 case entry (tameshi side, not an owner recommendation)

- The case entry's own record should carry both numbers: 2/10 killed with `sandbox-$DEFECT_ID` names (the lane's harness), 5/10 under neutral names (this seat's independent re-run; the kagi-native `mktemp -d` path is also neutral), with the miss cause stated as harness-induced and fixable at `D:403`, not as three missing cases. [INF] The honest owner-facing survivor set is the five S_* defects.
- Sources: kagi `drift-gate.md` (`K:`), commit `e64e81b`, and the header `D:2-36` are the owner statements; the lane's SOURCES row for the case must name them as the owner-intent anchor (ids S272/S273 are the next free ones per the item — not opened by this seat).

## Tooling
No installs or upgrades (none needed). Scratch `/fast/scratch/hyaku/tameshi-r51/T51ScoutKagiDrift/` (pristine blob, 10 mutant copies, run script) removed before yield; the §3 output above is the only retained receipt (not citable as a /tmp path).

## Summary
- Owner record: header `D:2-36`, entry `drift-gate.md`, commit `e64e81b`; gate unchanged since round 9; kagi never mutation-swept it (only a general lesson `round-21.md:115-122`).
- Ten defects map to guarantees in the §2 table; each has a header/entry line and a selftest case (or "none").
- Independent probe (scratch): neutral sandbox names kill all 3 kill-aimed misses (5/10 kill-aimed killed); 5 hole-aimed S_* still survive.
- Cause: `drift-pins.sh:403` unanchored `grep -q "$3"` over output that prints scratch paths; kagi's own `mktemp -d` runs are not blind in practice.
- Owner-record overclaims: `README.md:36` "symlink+hardlink" (no hardlink case), `round-9.md:77-82` (POLICY/EMPTY/EXTRA/DUP untested).
- DUP/EXTRA/UNPINNED are unreachable by construction (`:168` skip under `--baseline`); `--pin` has no case.
- Lane statements: `gates-survey-kagi.md:27,69,217`, `fleet-kill-rate-ledger.md:119` ("unmeasured by sweep; hermetic", no prediction).
- Nine owner-facing report lines R-1..R-9 (recommendations only; nothing absorbed).
