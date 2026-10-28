# T56W3RevStale — round-56 pointer sweep at PIN

Seat `T56W3RevStale` (leaf, no dispatch), L1 `TameshiR56a3`, attempt 3.
Judged on freshness. Milestone: pointer sweep at PIN.

## Scope and method

- PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd` (content-final). All checks ran in a detached clone at PIN: `git clone --shared` into `$HYAKU_SCRATCH/tameshi-r56/T56W3RevStale/clone`, `git rev-parse --show-toplevel` = clone path, `git status` clean. The lane worktree is dirty (`.ufo/evidence/round-21/coldread/ledger.json`, the `rekey-r56-c0137451f5b7/traces/*` files, `corpus/lessons/round-56.md`); the lane was read only through `git` object queries and `git show`. No lane file was written.
- Round-introduced/touched pointers: `git diff 981c5e8b..PIN` for `corpus/SOURCES.md`, `corpus/QUALITY.md`, `SKILL.md`, `tools/registry.json`, `SCORECARD.md`, plus the new `corpus/knowledge/receipt-revision-binding.md` and `corpus/lessons/round-56.md`.
- Every `.ufo/`, `corpus/`, `tools/`, `considerthese/`, `scripts/` token on the round's added lines and in the two new files was checked for existence at PIN. Values were checked by running the command, not by reading prose.
- Upstream checks used `curl` and `git ls-remote` (read-only). Tools installed: none. Host tools used: `python3` stdlib, `git`, `curl`.

## 1. Pointer table

Legend: ok = observed matches the text; STALE = observed differs from the text (correct value in §2); PENDING = placeholder or future output by design.

| # | pointer (where) | command | observed | ok/stale |
|---|---|---|---|---|
| 1 | S281 URL (SOURCES row) | `curl -s -o /dev/null -w '%{http_code}' https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md` | 200 | ok |
| 2 | S281 body sha256 `cbe684a1…ebea` | `curl -fsSL https://raw.githubusercontent.com/in-toto/attestation/v1.2.0/spec/v1/statement.md \| sha256sum` | `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea` | ok |
| 3 | S281 tag commit `df02077b` | `git ls-remote https://github.com/in-toto/attestation refs/tags/v1.2.0` | `df02077bf97218a8860a5c534eff1f1381f56984` | ok |
| 4 | S281 "identical at main `50bf0171`" | `git ls-remote … refs/heads/main`; `curl …/main/spec/v1/statement.md \| sha256sum` | `50bf01716982…`; main sha256 `cbe684a1…ebea` | ok |
| 5 | S281 anchor lines 36-37, 54-55 | `sed -n '36,37p;54,55p' statement.md` | 36-37: "Set of software artifacts … Each element / represents a single software artifact. Each element MUST have `digest` set."; 54-55: "IMPORTANT: Subject artifacts are matched purely by digest, regardless of / content type." | ok |
| 6 | S281 local extraction files | `sha256sum .ufo/evidence/round-56/assimilation/in-toto-statement-v1.md`; `ls …/assimilation/` | `cbe684a1…ebea`, 2492 B; `.json` and `.extract.txt` present | ok |
| 7 | S282 URL | `curl -s -o /dev/null -w 'blob %{http_code}' https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md` | `blob 200` | ok |
| 8 | S282 blob sha256 `efece57a…76fc` | `curl -fsSL https://raw.githubusercontent.com/slsa-framework/slsa/main/spec/build-provenance.md \| sha256sum` | `efece57ac1dd6e18…ca76fc` | ok |
| 9 | S282 "§Model, first paragraph" | `grep -n '## Model'` on fetched file | line 40 `## Model`; lines 42-43 "Provenance is an attestation that a particular build platform produced a set of software artifacts through execution of the `buildDefinition`" | ok |
| 10 | S282 "path last changed ba7d291a, 2026-10-19" | GitHub API `commits?path=spec/build-provenance.md&per_page=1` | `ba7d291a 2026-10-19T17:35:05Z` | ok |
| 11 | S103 (cited by knowledge) | `grep -n '^\| S103 ' corpus/SOURCES.md` | row at line 112, URL `https://git-scm.com/docs/git-hash-object` | ok (row only; not refetched) |
| 12 | SOURCES row count (census note: 142 rows) | `grep -c '^\| S[0-9]\{3\} '` | 142 | ok |
| 13 | Knowledge `source:` gate sha `1d80f8a6…fbd2` at `c3e2ca9f` | `git show c3e2ca9f0207:tools/receipt-revision-gate.py \| sha256sum` | `1d80f8a665f83508…` | ok |
| 14 | Frozen gate at `21eb3c63` (registry `source:`) | `git show 21eb3c63:…/receipt-revision-gate.py \| sha256sum` | `c60772ceb0ce3f51…` (== PIN gate, == ER-R56-K2 C0 digest) | ok |
| 15 | Knowledge `recheck:`, §Falsifier 3, §Re-derive step 1: "`--selftest` prints `GATE_SELFTEST: 14/14 pass`" | `python3 tools/receipt-revision-gate.py --selftest; echo $?` at PIN | `GATE_SELFTEST: 19/19 pass`, exit 0 | **STALE** (ER-R56-K2 is the errata; body unchanged) |
| 16 | Knowledge §Re-derive step 2 (`--certified c21081008adb --paths round-54-surface.paths --receipt …round-54-ctl-pos-c1.stdout:positive`) | run at PIN | exit 3, `code=RECEIPT_REV_CONTENT_DRIFT`, `drift=.ufo/evidence/round-21/coldread/ledger.json,…`, `verdict=REFUSED` | ok |
| 17 | Knowledge step 3 (`controls-b.stdout:positive`, `--certified c21081008adb`) | run at PIN | exit 3, `RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98` | ok |
| 18 | Knowledge step 4 (`round-55/after/c2.stdout:verdict`, `--certified 4c04c1d33377`) | run at PIN | exit 3, `RECEIPT_REV_ABSENT`, `no rev= token` | ok |
| 19 | Knowledge step 5 `.ufo/evidence/round-54/after/deciding-run.exit` | `cat` | `DECIDING_RUN_EXIT=0` | ok |
| 20 | Knowledge step 6 fixture drivers `fixture-gate-demo.sh`, `fixture-gate-demo2.sh` (need `HYAKU_SCRATCH`, ER-R56-K3) | `HYAKU_SCRATCH=/fast/scratch/hyaku bash <each>` from the clone; both exit 0; no leftover fixture dirs | cases 1–11 print the claimed codes: 1 PASS, 2 `MISMATCH`, 3 PASS, 4 `CONTENT_DRIFT`, 5 PASS, 6 `CONTROL_NOT_ANCESTOR`, 7 PASS (blind spot), 8 `CONTENT_DRIFT` (empty `--paths`), 9 PASS (7-hex), 10 `RECEIPT_REV_ABSENT` (tag), 11 `RECEIPT_REV_AMBIGUOUS` | ok (ER-R56-K3 env note still needed) |
| 21 | Knowledge "round-56 C2 counter exercises … arm 2 red54, 3 red54b, 4 red55, 5 own, 6 docs"; `c2/measure.py` | `grep -n 'arm' .ufo/evidence/round-56/c2/measure.py` | arms 1–6 with those names; arm 6 checks `docs != 4` | ok |
| 22 | Knowledge "the lane's own surface … **nine paths**" (`control/frozen-surface.paths`) | `cat -n`; `wc -l` | 16 lines (SKILL.md, QUALITY, SOURCES, knowledge, registry, gate, ledger, c1+c2 measure, contract.json, freeze.json, controls.sh, deciding-run.sh, no-harm.sh, two red-before receipts). Same 16 at C0 | **STALE** |
| 23 | Knowledge "gate 0b … `deciding-run.sh:66-74`" | `grep -n 'gate 0b'` | comment `:114`, block `:114-127`; comment line identical at C0 | **STALE** |
| 24 | Knowledge "gate 0c … `:100-107`" | `grep -n 'gate 0c'` | comment `:156`, block `:156-163`; identical at C0 | **STALE** |
| 25 | Knowledge `tools/receipt-revision-gate.py` code list (11 codes, §Re-derive) | compare to gate `CODES` and selftest `codes-closed` | the 11 codes match | ok |
| 26 | SKILL.md bullet gate path `tools/receipt-revision-gate.py --lane LANE --certified REV` | `grep -n 'certified' SKILL.md`; file exists at PIN | bullet at lines 45–49, under `## Standing rules` (line 17) | ok |
| 27 | SKILL table row 1 "a verdict receipt names another revision → refused unless … `--paths` surface → `RECEIPT_REV_MISMATCH`" | fixture case 2 (no `--paths`) and case 4 (`--paths`, drifted) | no `--paths` → `RECEIPT_REV_MISMATCH`; `--paths` + drift → `RECEIPT_REV_CONTENT_DRIFT` (gate lines 145–151) | **STALE (imprecise)**: code column names only the no-`--paths` code |
| 28 | SKILL rows 2–4 codes | cases 8; round-54/55 receipts | CONTENT_DRIFT (positive, drifted); UNRESOLVABLE (`7df0e0426c98`); ABSENT (round-55) | ok |
| 29 | SKILL "ER-R54-1, R55.5" | `grep -rn 'ER-R54-1\|R55.5'` | ER-R54-1 in `corpus/lessons/round-54.md` (lines 77, 105, round-55 correction); R55.5 in `round-55-verifier-spotcheck.md:134` | ok |
| 30 | QUALITY 107 command: `--certified c21081008adbb6b6fe4e58a0aeec4831b30e318c --paths …round-54-surface.paths --receipt …round-54-ctl-pos-c1.stdout:positive` | run from the lane path and from the PIN clone | both: `GATE REFUSED … code=RECEIPT_REV_CONTENT_DRIFT`, summary `codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED`, exit 3 | ok |
| 31 | QUALITY 107 control: same receipt `--certified 077d431e69965fa4673cd006ab64f6fc387f9e15` | run | `GATE OK … revs=077d431e6996`, `verdict=PASS`, exit 0 | ok |
| 32 | QUALITY 107 both full shas resolve | `git rev-parse --verify -q <sha>^{commit}` | both resolve | ok |
| 33 | QUALITY 107 "Lesson: `corpus/lessons/round-56.md` `## Gate` (the R55.5 disposition …)" | `grep -n '^## ' corpus/lessons/round-56.md`; `grep -n R55.5` | `## Gate` (line 15) is the source-open table; R55.5 is row line 107 under `## Round-55 routed defects — dispositions (this round)` (line 99) | **STALE in body**; QUALITY "Corrections"/"Erratum" sections state the right anchor |
| 34 | QUALITY 107 scope-gap receipt `.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt` | `cat`; `grep -c 'credited=99'` | present at PIN; `GATE OK … revs=077d431e6996`, `verdict=PASS`, exit 0; 0 matches for `credited=99` | ok (erratum correct; the body sentence "resolves only after L1 lands" is historical) |
| 35 | QUALITY 107 `considerthese/2026-10-28.md` proposal 1 | `sed -n 73p considerthese/2026-10-28.md` | "1. **Receipt-existence linter for records.**" | ok |
| 36 | QUALITY 107 `.ufo/evidence/round-54/after/deciding-run.exit` = `DECIDING_RUN_EXIT=0` | `cat` | `DECIDING_RUN_EXIT=0` | ok |
| 37 | QUALITY 107 "round-56 C2 counter's `docs=0/4` arm" | `grep -n 'docs' c2/measure.py` | arm 6, denominator 4 | ok |
| 38 | Registry cell `receipt-revision-gate-selftest` (`rows` key; 57 rows) | parse JSON; run `argv` at PIN | `schema=tameshi-entry-registry-v1`; `python3 tools/receipt-revision-gate.py --selftest` → `GATE_SELFTEST: 19/19 pass`, exit 0 | ok |
| 39 | Registry `expect.stdout_contains` (12 strings) | `grep` each in selftest stdout | all 12 present | ok |
| 40 | Registry `source: tools/receipt-revision-gate.py@21eb3c63…:10-29` | `git show 21eb3c63:…` lines 10–29 | the usage block and the code list | ok |
| 41 | Registry `scratch_root`: `tempfile.TemporaryDirectory(prefix='tameshi-r56-gate-')` | `grep -n` | gate line 234 | ok |
| 42 | Registry `scratch_root`: unusable TMPDIR → platform `/tmp`, no could-not-evaluate line, exit 0 | `TMPDIR=/nonexistent/nope python3 tools/receipt-revision-gate.py --selftest; echo $?` | exit 0, `GATE_SELFTEST: 19/19 pass`, 0 lines containing `could` | ok |
| 43 | Registry `scratch_root` codes list (11) | compare to gate `CODES` | identical set | ok |
| 44 | SCORECARD round-56 block: every `.ufo/`, `corpus/`, `tools/` token on its added lines | token scan over the 35 added lines (diff stat `+35`) | all exist at PIN | ok |
| 45 | SCORECARD standing row "Measured commit `c1dd23b3…`" | `git merge-base --is-ancestor c1dd23b3… PIN` | ancestor | ok (value not re-measured here) |
| 46 | SCORECARD `C0 c0137451…`, freeze `21eb3c63…`, original freeze `c3e2ca9f0207…` | `git cat-file -t` / ancestor | all exist; C0 and freeze are ancestors of PIN | ok |
| 47 | Lesson receipt paths (33 distinct tokens) | token scan of `corpus/lessons/round-56.md` at PIN | all resolve except the three below | ok except below |
| 48 | Lesson `.ufo/evidence/round-56/after/` (deciding receipts) | `git cat-file -e PIN:…/after` | absent at PIN | **PENDING** (output dir the deciding run creates) |
| 49 | Lesson header: "`amendments` `<L1 fills>`" and "Content commit C0 `<L1 fills>`" (lines 12–13) | `grep -n '<L1 fills>'` at PIN | placeholders at PIN (4 occurrences); the lane worktree copy has 2 | **PENDING/STALE**: `amendments` = 1 (`freeze.json`, `21eb3c6`); C0 = `c0137451f5b7f22d65f748fc69f1b181f55e1378` |
| 50 | Lesson census line "`end: <L1 fills>` (`scripts/sources-census.sh validate …`)" (line 27) | not run here | placeholder at PIN; `scripts/sources-census.sh` exists at fleet root | **PENDING** |
| 51 | Lesson "`SOURCES.md` pointer … the target is line 508" (line 217) | `sed -n 508p corpus/SOURCES.md` | "Round 48: four rows added, S265-S268 (superseding held S026 …)" | ok (bare name; historic) |
| 52 | Knowledge and QUALITY `c3e2ca9f`, `21eb3c63` shas and round-54 shas | `git cat-file -t` | all exist | ok |
| 53 | Knowledge body quote of S281 lines 36–37 ("Set of software artifacts … Each element MUST have `digest` set") | compare to fetched lines 36–37 | body is a two-excerpt splice; the exact text is in ER-R56-K1 | **STALE in body**; errata correct |
| 54 | Knowledge lines 54–55 quote ("Subject artifacts are matched purely by digest, regardless of content type") | compare | exact | ok |

## 2. Stale pointers and correct values

1. **Knowledge `recheck:`, §Falsifier item 3, §Re-derive step 1 (lines 3, 155, 166): `GATE_SELFTEST: 14/14 pass`.** Correct value at PIN: `GATE_SELFTEST: 19/19 pass` (exit 0; gate sha256 `c60772ceb0ce3f51…`). The 14/14 value is the `c3e2ca9f` freeze. ER-R56-K2 records this; the body was not corrected.
2. **Knowledge line 100: `frozen-surface.paths` — "nine paths".** Correct value: **sixteen** lines (`SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge`, `tools/registry.json`, `tools/receipt-revision-gate.py`, `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-56/c1/measure.py`, `.ufo/evidence/round-56/c2/measure.py`, `.ufo/evidence/round-56/contract.json`, `.ufo/evidence/round-56/freeze.json`, `.ufo/evidence/round-56/controls.sh`, `.ufo/evidence/round-56/deciding-run.sh`, `.ufo/evidence/round-56/no-harm.sh`, `.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout`, `….stdout.sha256`). The count was 16 at C0 too. Wave-2 P10 records it.
3. **Knowledge line 75: gate 0b `deciding-run.sh:66-74`.** Correct: **`:114-127`** (comment `:114`; the `python3 "$SCR/gate/gate.py" … --receipt controls-a.stdout:control --receipt controls-b.stdout:positive` block through its exit check at `:127`). The `:114` comment line is identical at C0 and PIN; the block end `:127` was read at PIN only. Wave-2 P11 records the line numbers as `c3e2ca9f`-era; `deciding-run.sh` was rewritten in amendment `21eb3c6`.
4. **Knowledge line 76: gate 0c `:100-107`.** Correct: **`:156-163`** (comment `:156`; the `receipt-gate-verdicts` block through `:163`).
5. **QUALITY 107 "Lesson:" anchor `corpus/lessons/round-56.md` `## Gate`.** Correct: `## Round-55 routed defects — dispositions (this round)` (line 99), row `R55.5` (line 107). The QUALITY erratum states the same; the criterion body still carries the wrong anchor.
6. **SKILL standing-rule table row 1 (verdict receipt names another revision).** Code column is `RECEIPT_REV_MISMATCH` only without `--paths`. Correct: "`RECEIPT_REV_MISMATCH` (no `--paths`); `RECEIPT_REV_CONTENT_DRIFT` (`--paths` declared and the surface drifted)". Rows 2–4 are correct.
7. **Knowledge S281 quote (lines 7–10 splice).** Correct quote for `§Fields`, `subject`, lines 36–37: "Set of software artifacts that the attestation applies to. Each element represents a single software artifact. Each element MUST have `digest` set." (ER-R56-K1 gives the exact text.)
8. **Lesson lines 12–13: `amendments <L1 fills>`; `Content commit C0 <L1 fills>`.** Correct values: `amendments` = `1` (`freeze.json`, commit `21eb3c6`); C0 = `c0137451f5b7f22d65f748fc69f1b181f55e1378`. Still placeholders at PIN; the lane worktree copy has two fewer.
9. **Lesson line 27: `end: <L1 fills>` census.** Pending: L1 runs `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` and records the exit. Not run by this seat.
10. **Lesson line 12: `.ufo/evidence/round-56/after/`.** Pending by design (deciding receipts not yet produced at PIN).

## 3. `/tmp` literal and absolute-path sweep

Commands (run on the clone at PIN, over the 1154 added files from `git diff --name-only --diff-filter=A 981c5e8b… 2f5512a8…`):

```
git show "$P:$f" | grep -I -n '/tmp\b'                              # per added file
git show "$P:$f" | grep -I -o -n '/home/[^ ]*\|/fast/[^ ]*\|/tmp[^ ]*\|/var/…\|/etc/…\|/usr/…' \
  | grep -v '^N:/home/vgpnk/Projects/shokunin/tameshi-shokunin'
```

Results:

- `/tmp` in added files: 163 lines in 85 files. Most are receipts, logs, and wave reports quoting old `/tmp` namespaces, or the historical scratch rule itself.
- `/tmp` literals in round-56 **authored** files (not receipts):
  - `.ufo/waves/round-56/census-after.sh:77` — `TMP=$(mktemp -d "${TMPDIR:-/tmp}/census-after.XXXXXX")`. A fallback literal in a new script; allowed by the directive only for files under 50 MB. Flag.
  - `.ufo/waves/round-56/w2/T56W2RevCensusAfter.md:254-257` — `curl … -o /tmp/slsa.md` and `grep … /tmp/slsa.md` as re-derive commands (26 KB file, within the 50 MB limit). Flag as a command literal.
  - `.ufo/waves/round-56/w2/T56W2RevQuality.md:67` — "Run verbatim from `cwd=/tmp`". Flag (cwd only; no writes measured).
  - Description or prohibition mentions, not literals in use: `c1/measure.py:9`, `c2/measure.py:9` (scratch "never under /tmp"), `no-harm.sh:42` (a regex that scans `tools/` for `dir = "/tmp"`), the registry `scratch_root` (describes the fallback).
  - `tools/receipt-revision-gate.py` uses `tempfile.TemporaryDirectory` with no `/tmp` literal (line 234).
- Absolute paths outside the lane in added files: 1665 hits. Breakdown by prefix: `/fast/scratch/hyaku` (725; scratch paths, expected); `/home/vgpnk/Projects/shokunin/…` fleet paths (420: `scripts/sources-census.sh`, fleet `.ufo/`, fleet `*.md`); `/home/vgpnk/.omp/agent/RULES.md` and `config.yml` (11); `/home/vgpnk/Projects/kimi-shokunin` (8), `ufo-fsd-alpha` (3), `shokuknow` (2); `/usr/bin/…` and `/usr/lib/…` (120, tool paths in receipts); `/etc/passwd` (1, a critic probe in `T56W1CritC1.md:239`).
- Authored round-56 files with absolute out-of-lane paths: `.ufo/evidence/round-56/deciding-run.sh:16` `FLEET=/home/vgpnk/Projects/shokunin` (frozen; the deciding runner's fleet root, expected), `.ufo/waves/round-56/census-after.sh:37`, `build-spec-w{1,2,3}.py` (spec text naming the fleet census), and `T56W1CritC1.md` / `T56W1CritC2.md` (scratch lanes). None is a lane-pointer defect; each is fleet or scratch by design.

## 4. Summary

- Verified at PIN: S281 and S282 URLs, anchors, hashes and tag/main commits; the knowledge fixture cases; the four knowledge re-derive verdicts; the QUALITY 107 command and its control; the registry cell; the SKILL gate path and codes (rows 2–4); the `.ufo/` tokens on every round-added line of SCORECARD, SKILL, QUALITY, SOURCES and registry, and every token in the lesson and the knowledge entry.
- Stale (correct value in §2): knowledge `14/14` (three places) → `19/19`; knowledge "nine paths" → sixteen; knowledge gate 0b/0c line numbers → `:114-127`, `:156-163`; QUALITY 107 Lesson anchor (body; erratum correct); SKILL row 1 code (imprecise); knowledge S281 quote splice (body; ER-R56-K1 correct); lesson `amendments` and C0 placeholders.
- Pending: lesson census placeholder; `after/` directory.
- Overlap with `T56W2RevStalePointers.md`: P8–P11, P15 and P34 cover several of these. New from this seat: the registry/`TMPDIR` probe (exit 0, no could-not-evaluate line), the fixture-driver re-run with per-case codes, the `census-after.sh` `/tmp` fallback literal, and the lesson placeholder values.

## 5. Not checked

- The census command (`scripts/sources-census.sh validate`) was not run; it belongs to the census seat and L1.
- Lane worktree content was not compared with PIN (dirty `corpus/lessons/round-56.md`: two placeholders remaining vs four at PIN). Every result above is for PIN.
- Measured calibration and operability values (C1/C2 counters, `controls.sh`) were not run here.
- The registry `scratch_root` timing `(0.4 s)` was not re-measured.

## Verdict

Pointer freshness at PIN: eight stale or imprecise items across the knowledge entry, QUALITY, SKILL and lesson, and two pending placeholders. None of the stale items changes a gate verdict or a claim value; the gate commands, codes and receipts resolve. Corrections are for L1 to integrate in the content commit; this seat did not edit lane files.
