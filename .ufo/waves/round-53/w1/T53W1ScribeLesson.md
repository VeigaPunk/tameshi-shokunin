# T53W1ScribeLesson — round-53 lesson: do its Gate/Mistakes pointers resolve and say what it claims?

Seat `T53W1ScribeLesson` · round 53 wave 1 · lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Target: `corpus/lessons/round-53.md` (append-only; **not edited by this seat**).

- C\* (content commit) = `a41195dfc13a73958e4c5228ec196b28d03ded03`
- freeze commit = `e62d99711a0dd5d92b83acb96dd53ff22b31cb75`; base = `6db1d220b337c35ff1e25bf9cfd74abc9db1498d`
- post-fix candidate = `218bc6b` (`218bc6b5…`, "fix pass — 21 T52 reader findings resolved")
- lesson bytes: `sha256(corpus/lessons/round-53.md at C*) == sha256(working tree) == d0cd51ca987400ee2834c798c4c1e222f004852d800da53209ba2affe0b3447e` (lesson unchanged since C\*; my checks below read the C\* blob and the working-tree file interchangeably).

Commands used (all read-only; no git/jj mutation anywhere):

```
git -C <lane> show <rev>:<path>            # reads at e62d997, 218bc6b5, a41195df, 6db1d220, cf87276, a7ba4e3
git -C <lane> cat-file -e <rev>:<path>     # path resolution at C*
git -C <lane> git log --all -- <path>      # "was it ever committed"
sha256sum / pdftotext / grep -c / python3 (word counts, quote search, compile check)
curl -fsSL ... (two live fetches of the cited S275/S276 URLs, into scratch only)
```

## 1. Path resolution at C\*

| cited path | at C\* | working tree | notes |
|---|---|---|---|
| `.ufo/evidence/round-53/contract.json` | TRACKED | present | sha `5fb52e4d…` == freeze manifest entry |
| `.ufo/evidence/round-53/freeze.json` | TRACKED | present | 8 files, 5 amendments |
| `.ufo/evidence/round-53/before/coldread-precheck-at-tip.stdout` | TRACKED | present | shows the **45** run only |
| `.ufo/evidence/round-53/control/controls.stdout` | TRACKED | present | phase-A, 2/2 pass (post-fix) |
| `corpus/knowledge/change-aware-resweep-cadence.md` | TRACKED | present | adopted entry |
| `corpus/README.md`, `corpus/SOURCES.md` | TRACKED | present | F7 note :636+, rows :150–151, :508–509 |
| `corpus/lessons/round-52-verifier-spotcheck.md` | TRACKED | present | R52.1 :83, R52.5 :87 |
| `considerthese/2026-10-26.md` | TRACKED | present | proposal 1 at :74 |
| `.ufo/waves/round-52/w3/T52W3Read06.json`, `T52W3Read12.json`, `T52W3RevApplied1.md`, `T52W3RevApplied4.md` | TRACKED | present | |
| `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out` | TRACKED | present | 109 lines |
| `.ufo/evidence/round-53/assimilation/S161-camera-ready.pdf` | **ABSENT** | present (untracked) | 131622 B, sha256 `4d755c4e…` |
| `.ufo/evidence/round-53/assimilation/S162-arxiv.html` | **ABSENT** | present (untracked) | 41423 B, sha256 `d6dc4cf6…` |
| `assimilation/S161-camera-ready.txt` (used for line numbers) | **ABSENT** | present (untracked) | 544 lines |
| `assimilation/collisions` | **ABSENT** | present (untracked) | 8 ids |
| `assimilation/guard-fixture/reg.md` | **ABSENT** | present (untracked) | 34 B |
| `.ufo/evidence/round-53/verify-freeze.sh` | **ABSENT** | present (untracked) | also absent at e62d997 and ace79e3 |
| `.ufo/evidence/round-53/verify-freeze.stdout` | **ABSENT** | present (untracked) | prints `FREEZE_INTEGRITY: OK` |
| `CORPUS.md` (learner lane) | absent | absent | resolves at the **fleet root** `/home/vgpnk/Projects/shokunin/CORPUS.md` (:110 Rules, :112 rule 1) |

`git log --all --oneline -- .ufo/evidence/round-53/assimilation` is **empty**: the whole assimilation tree was never committed on any ref. `git status --porcelain .ufo/evidence/round-53/` prints `?? .ufo/evidence/round-53/assimilation/`, `?? …/verify-freeze.sh`, `?? …/verify-freeze.stdout`, `?? …/census-mid.stdout`, `?? …/integrate/`.

## 2. Per-citation table — `## Gate`

| # | Citation (lesson line) | Verdict | Observed at C\* / live |
|---|---|---|---|
| G1 | claims frozen at `e62d9971` (amendments 1–5; `contract.json`, `freeze.json`) (:5–6) | VERIFIED | e62d997 exists; `git show e62d997:…/freeze.json` → `files=8`, amendments 1–5 with prior freezes; contract.json sha matches manifest. (Note: contract.json's own `"amendments"` is `[]` — the amendments exist only in freeze.json.) |
| G2 | Base `6db1d220` (round-52 closure salvage) (:4) | VERIFIED | `git log -1 6db1d220` → "round-52 w3: commit wave markers and integrate script (closure salvage)" |
| G3 | both claims repair what round-52-verifier-spotcheck.md routed back (:8–9) | VERIFIED | `R52.1 coldread re-key debt` :83; `R52.5 hard-coded /tmp in tools/registry-check.py:766` :87 |
| G4 | round 52 "rejected-harmed … cold-read floor RED at the tip (45/64 credited)" (:9–10) | VERIFIED | spotcheck :9, :62, :78; `.ufo/evidence/round-52/integrate/precheck-cand1.stdout:20` → `cand_credited=45 lost=19 RED` |
| G5 | "Rows opened this round (CORPUS.md SOURCES contract v1 rule 1)" (:14) | VERIFIED | fleet-root CORPUS.md :112 rule 1 ("A row is a claim … a ≤25-word quote with its location") |
| G6 | S275 DOI `10.1145/3540250.3558911`; ACM copy HTTP 403 (:17–19) | VERIFIED | `curl -s -o /dev/null -w '%{http_code}' https://doi.org/…` → 302 → `dl.acm.org` final **403** |
| G7 | camera-ready HTTP 200, 131622 B, sha256 `4d755c4e…` (:20–21) | VERIFIED (live) | `curl -fsSL` → `http=200 size=131622`, sha256 `4d755c4e0b1925d1…` |
| G8 | snapshot `.ufo/evidence/round-53/assimilation/S161-camera-ready.pdf` (:21–22) | **MISMATCH** | `git cat-file -e a41195df:…S161-camera-ready.pdf` → fatal (absent); untracked, never committed (F1). Bytes do match the live fetch. |
| G9 | "Located quote (22 words, camera-ready p. 4, pdftotext lines 289–294)" (:23) | **MISMATCH** | 20 words; quote is on PDF page **3** (printed 1787); committed txt lines **292–294** (F2) |
| G10 | S276 arXiv HTTP 200, 41423 B, sha256 `d6dc4cf6…` (:29–30) | VERIFIED (live) | `curl -fsSL` → `http=200 size=41423`, sha256 `d6dc4cf6512861f5…` |
| G11 | snapshot `…/assimilation/S162-arxiv.html` (:30–31) | **MISMATCH** | absent at C\*, untracked, never committed (F1) |
| G12 | "Located quote (19 words, abstract)" (:31–32) | **MISMATCH** | quote is 20 words; text present in the snapshot (F3) |
| G13 | entry ADMITTED; PROVINCE verification-fixture craft — in scope (:39–40) | VERIFIED | `corpus/knowledge/change-aware-resweep-cadence.md` at C\*; `assimilation/validate/PROVINCE.md:3` "Domain: verification-fixture craft" |
| G14 | QUALITY bar: every claim cites its source with located quotes — holds (:40–41) | PARTIAL | both sources are quoted, but one entry quote is not byte-verbatim in the round's copy (F7) |
| G15 | F7 ground recorded in `corpus/README.md` frontier table (round-53 addendum) (:42–43) | VERIFIED | `git show a41195df:corpus/README.md` :636 "## Round 53 — F7 ground acquisition note (assimilation)" |
| G16 | both rows re-opened by the L1 this round (:43–44) | VERIFIED | SOURCES.md :150–151 "fetched 2026-10-27"; snapshots present |
| G17 | "the staged entry's quotes re-located verbatim in the round's copies" (:44–45) | **MISMATCH** | `grep -c '30% of mutants are commit-relevant'` on the snapshot = **0**; line 290 reads "are commitrelevant." (F7) |
| G18 | staged S161/S162 renumbered to S275/S276; S161–S255 stay reserved (:46–47) | VERIFIED | package `SOURCES.append.md:15–16` are S161/S162; lane SOURCES.md :508–509 "Next unused id: S275 / S277 … reserved" |
| G19 | collision check `assimilation/collisions` listed 8 collisions, none for adopted rows (:48–49) | PARTIAL | content VERIFIED (8 ids: S153–S160; no S275/S276), but the path is untracked (F1) |
| G20 | "0–3-space indented-row guard was proven on a scratch fixture before any append" (:49–50) | PARTIAL | fixture exists (`guard-fixture/reg.md`: `  \| S002 \| test \|` / `\| S010 \| test \|`), untracked; **no receipt of the guard's verdict** anywhere under round-53 evidence |
| G21 | "The other 85 staged `merge/tameshi` entries" (:54) | **MISMATCH** | package holds 85 entry files (81 `knowledge/*.md` + 4 `amendments/*.md`), one of them the adopted entry → 84 others; MERGE-REPORT's own count is 86 entries / 103 rows → 101 other rows (F5) |
| G22 | next-ranked candidates `r8-predictive-test-selection-cost.md`, `delta-debugging-minimization-contract.md` (:57–58) | VERIFIED | both exist at `merge/tameshi/knowledge/corpus/knowledge/…` |
| G23 | staged S161/S162 rows carry escaped pipes in the recheck cells (:60–62) | VERIFIED | `SOURCES.append.md` has 66 literal `\|`; lines 15 and 16 both contain them |
| G24 | appendable rows normalize to fleet schema (date + `365d`) (:62–63) | VERIFIED | lane rows S275/S276 end `… | mined | 2026-10-27 | 365d | corpus/knowledge/change-aware-resweep-cadence.md` |
| G25 | S275 re-check `curl … \| sha256sum` expect `4d755c4e…` (:64–66) | VERIFIED (live) | live sha256 `4d755c4e0b1925d1…` |
| G26 | S276 re-check `curl … \| grep -c '52% degrade'` expect 1 (:67–68) | **MISMATCH** | live: HTTP 200, 41423 B, same sha as snapshot, `grep -c` = **3**; the round's own snapshot also matches 3 lines (F4) |
| G27 | proposal 1 "implemented as `.ufo/evidence/round-53/verify-freeze.sh`" (:70–72) | **MISMATCH** | file untracked / absent at C\*, e62d997 and ace79e3 (F6); proposal identity itself VERIFIED (`considerthese/2026-10-26.md:74` "1. **Crash-resume integrity check.**") |
| G28 | "executed by the L1 at freeze time (receipt below)" (:72–73) | PARTIAL | re-ran `bash …/verify-freeze.sh <lane> e62d9971…` → `FREEZE e62d99711a0d files=8 amendments=5 … FREEZE_INTEGRITY: OK`, exit 0 — mechanism holds; receipt untracked, and it re-derives the e62 freeze (a post-freeze check: mtime 10:23 vs freeze 10:18:54) |
| G29 | Proposals 2–5 remain unmined (at most one per round) (:73) | VERIFIED | `considerthese/2026-10-26.md` lists exactly 5 proposals (lines 74–88); only 1 is implemented |

## 3. Per-citation table — `## Mistakes`

| # | Citation (lesson line) | Verdict | Observed |
|---|---|---|---|
| M1a | duplicate parenthetical `replays **six** in r10-2 (**ten** since round 51) (ten since round 51)` (:79–80) | VERIFIED (as base-state) | base `6db1d220:SKILL.md:1305` reads exactly "`--regression` replays **six** in r10-2 (**ten** since round 51) (ten since round 51)"; at `218bc6b5` and C\* :1311 it reads "… (**ten** since round 51)" — single parenthetical, so "fixed this round" holds (fixed in the 218b fix pass) |
| M1b | contradictory "Cases 5–6 were still not embedded at this boundary (both are legs 5–6 since round 10-2 …)" (:81–82) | VERIFIED (as base-state) | base `SKILL.md:1227` exact; at 218b/C\* :1229 rewritten to "Cases 5–6 were not yet embedded at this boundary (they became legs 5–6 at r10-2; …)" |
| M1c | round-52 parenthetical "rc 0, at tool sha `977de470…` — see `T52W2Fix06.selftest.out`" (:83–84) | VERIFIED (as base-state) | base `SKILL.md:1004` exact; at C\* :1006 re-anchored to "… runner sha256 `977de470…` — seat T52W2Fix06's measurement and runner pin, `.ufo/waves/round-52/w2/T52W2Fix06.md` F3, receipt `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out`" |
| M1d | "where the receipt names no command, exit, or sha" (:84–85) | VERIFIED | `grep -c 'sha256\|rc=0' T52W2Fix06.selftest.out` = 0; no command line, no overall exit statement — only PASS lines + `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS` |
| M2 | "The T52W3 readers caught all three as findings 12–14 (`.ufo/waves/round-52/w3/`)" (:86) | **MISMATCH** | actual catchers: `T52W3Read12.json` F1 (Cases 5–6), `T52W3Read06.json` F2 (receipt provenance of the 977de470 parenthetical), and **`T52W3RevApplied4.md` pass-2 `Fix04:1`** (duplicate parenthetical; also `T52W3RevApplied1.md` §Fix04 "OVERREACH / false as applied"). No numbering "12–14" exists in w3 (F8) |
| M3 | "the C2 tool fixes (7 files)" (:93) | VERIFIED | `git diff --name-only 6db1d220 218bc6b5 -- tools/` → 7 files (bash-witness-study, context-capture, env-diff, evidence-disposition, pin-disposition, registry-check, repeat-control) |
| M4 | "input-drifted 10 sections the round did not intend to touch" (:93–94) | **MISMATCH** | amendment 5 (freeze.json at e62): "19 inherited + 11 from the C2 tool/scratch edits"; the same bullet's "19 → 30" needs 11. 19+10=29 ≠ 30 (F9) |
| M5 | "grew 19 → 30 headings (amendment 5, disclosed before wave 1)" (:94–95) | VERIFIED | `c1/lost-headings.json` length **30**; amendment 5 commit e62d997 (10:18) precedes the wave-1 dispatch commit ace79e3 (10:26) |
| M6 | "the precheck LOST diff after the fix pass caught it (45 → 34 credited) before any seat ran" (:95–96) | **MISMATCH** | 45 receipted (`before/coldread-precheck-at-tip.stdout`: `cand=6db1d220… cand_credited=45 lost=19 RED`, exit 1); **no receipt anywhere records credited=34 / lost=30 at 218bc6b** — the 34 exists only as prose in `contract.json:15`, which cites that same receipt (F10) |
| M7 | "the first frozen c1 counter carried a NUL byte (syntax error)" (:100) | VERIFIED | `git show cf87276:…/c1/measure.py` → exactly 1 NUL (`'\x00'` inside a string literal); `py_compile` → `SyntaxError: source code string cannot contain null bytes` |
| M8 | "its do-nothing control crashed instead of printing a verdict" (:100–101) | VERIFIED (by reproduction) | ran the amendment-1 counter (`a7ba4e3:c1/measure.py`) at BASE: `subprocess.CalledProcessError: git … cat-file -e 6db1d220:.ufo/evidence/round-53/c1/lost-headings.json … exit 128`, exit 1 — traceback, no verdict |
| M9 | "both caught by the phase-A control run before wave 1 (amendments 1–2)" (:101–102) | PARTIAL | amendments 1 and 2 exist and describe exactly these two repairs; but the committed phase-A receipt (`control/controls.stdout`, commit a36d3e5, after amendments 1–2) shows a **clean** `CONTROLS: total=2 pass=2` with a fail-soft verdict line and no crash. The crash has no receipt (F11) |
| M10 | "the frozen do-nothing control — exactly what it exists for" + "must print a verdict line (never a traceback) — now part of the c1 contract" (:102–105) | VERIFIED (narrowly) | `c1/measure.py` at C\* :112 appends `lost-headings-missing-at-rev` and :191/:196 print the verdict + `PROBLEM` line. Note for L1: contract `CTL_0` expects "the counter at BASE prints lost=19", which the phase-A receipt does **not** show (`verdict=false PROBLEM lost-headings-missing-at-rev`) — contract↔receipt inconsistency, out of this seat's scope |

## 4. Out-of-mandate extras (header + `## The re-key method`) — reported, not adjudicated

| # | Citation | Verdict | Observed |
|---|---|---|---|
| X1 | "The T52W3 reader findings (16 findings across 10 sections, plus the missing Read18)" (:118–119) | **MISMATCH** | w3 holds 18 reader JSONs (Read01–17, 19; Read18 absent), 18 distinct headings, **19** findings; exactly **10** files carry ≥1 finding (Read02 4, Read03 3, Read06 2, Read07 2, Read10 2, Read12 2, Read13 1, Read14 1, Read16 1, Read17 1). "16" matches neither 19 nor the 218bc6b subject's "21 T52 reader findings resolved". "10 sections" holds |
| X2 | "fixed L1-inline at `218bc6b5`" (:119) | VERIFIED | commit exists; the three M1 artifacts are fixed in it (see M1a–M1c) |
| X3 | QUALITY criterion 104 "drafted; lands with the round commit" (:107–114) | VERIFIED | the criterion text is in the lesson at C\*; it does not exist in `SKILL.md` at C\* (`grep '^104\.'` → none) — the "landing" is lesson-only |
| X4 | contract.json's `C1.surface` still reads "the 19 sections …" while the frozen set is 30 | note | `git show e62d997:…/contract.json` — amendment 5 changed the heading file, not the contract prose |

## 5. Findings for the L1 (each evidenced above)

1. **F1 — cited snapshots are not at C\*.** `## Gate` (:21–22, :30–31) cites `.ufo/evidence/round-53/assimilation/S161-camera-ready.pdf` and `…/S162-arxiv.html` as the provenance of both rows; both are untracked and were never committed on any ref (`git cat-file -e a41195df:…` fails; `git log --all -- .ufo/evidence/round-53/assimilation` empty; `git status` → `??`). Same for `assimilation/collisions`, `assimilation/guard-fixture/reg.md`, `verify-freeze.sh`, `verify-freeze.stdout`. The bytes themselves are right (live fetches reproduce 131622 B / `4d755c4e…` and 41423 B / `d6dc4cf6…`), so this is a commit-scope defect, not a fabricated source.
2. **F2 — S275's located quote is misdescribed in all three dimensions.** `Located quote (22 words, camera-ready p. 4, pdftotext lines 289–294)`: 20 words; on PDF page **3** (printed 1787; `pdftotext -f 4 -l 4 … | grep -c '93% on average'` = 0); committed txt lines **292–294** (`-layout` run: 184–186). Fleet CORPUS rule 1 requires a quote "with its location", and the location is wrong here and in `corpus/SOURCES.md:150` and the knowledge entry.
3. **F3 — S276's quote is 20 words, not 19** (text itself present in the snapshot).
4. **F4 — S276's recorded re-check expectation is false.** `curl -fsSL 'https://arxiv.org/abs/2212.11762' | grep -c '52% degrade'` expect 1 → live returns **3** (HTTP 200, 41423 B, sha `d6dc4cf6…`, identical to the round's snapshot; the snapshot has 3 matching lines). The expectation was inherited from the 2026-10-23 package copy and not re-measured. (S275's sha re-check holds.)
5. **F5 — "The other 85 staged `merge/tameshi` entries" is off by one and by set.** 85 entry files exist (81 knowledge + 4 amendments); the adopted entry is one of them → 84 remain; MERGE-REPORT claims 86 entries / 103 rows (→ 101 other rows).
6. **F6 — `verify-freeze.sh` is untracked.** Cited as "implemented as `.ufo/evidence/round-53/verify-freeze.sh` and executed by the L1 at freeze time (receipt below)"; absent at C\*, at e62d997 and at ace79e3. Re-running it does print `FREEZE_INTEGRITY: OK` (exit 0) against e62d997, so the mechanism works but the citation does not resolve.
7. **F7 — one "verbatim" relocation is not verbatim.** The staged entry quotes "around 30% of mutants are commit-relevant"; the round's copy reads "around 30% of mutants are commitrelevant." (pdftotext dropped the line-break hyphen). `grep -c` for the hyphenated phrase = 0.
8. **F8 — "The T52W3 readers caught all three as findings 12–14" is wrong on both the catcher and the numbering.** Two are reader findings (`T52W3Read12` F1, `T52W3Read06` F2); the duplicate parenthetical was caught by reviewer `T52W3RevApplied4` pass-2 `Fix04:1` (and `T52W3RevApplied1` Fix04). No "findings 12–14" enumeration exists in `.ufo/waves/round-52/w3/`; Read13 is "The service's limits", Read14 "The six-leg regression".
9. **F9 — "input-drifted 10 sections" contradicts "19 → 30" and amendment 5.** Amendment 5 (freeze.json at e62) says "19 inherited + 11 from the C2 tool/scratch edits". The bullet is internally arithmetic-dead (19+10=29).
10. **F10 — "45 → 34 credited" is half-receipted.** `before/coldread-precheck-at-tip.stdout` is the base run (`cand=6db1d220… credited=45 lost=19 RED`, exit 1). No committed receipt shows credited=34/lost=30 at 218bc6b; `contract.json:15` asserts it while citing that base receipt. The 30-heading set is receipted only through `c1/lost-headings.json`.
11. **F11 — "caught by the phase-A control run" is not what the phase-A receipt shows.** `control/controls.stdout` (commit a36d3e5, after amendments 1–2) is a clean 2/2 with a fail-soft verdict; the NUL and the crash (both reproduced independently above) happened before it and have no receipt.

**Partial / unreceipted (not counted as findings, for the L1's judgement):** G14/G17 (quote byte-exactness), G19/G20 (collision + guard-fixture paths untracked; guard "proven" has no receipt), G28 ("at freeze time" — the receipt is a post-freeze re-derivation), X1 (reader-finding count), X3 (criterion 104 lands lesson-only), X4 (contract surface still says 19).

## 6. Holds worth recording

- The two external rows genuinely open: both URLs answer (200) and both bytes match the recorded size+sha; the ACM DOI does answer 403 as claimed.
- Every quoted SKILL.md artifact in `## Mistakes` exists byte-exactly at base `6db1d220` (`:1305`, `:1227`, `:1004`) and is repaired at C\* (`:1311`, `:1229`, `:1006`).
- The NUL-byte and do-nothing-crash defects are real and reproducible from the frozen commits (`cf87276`, `a7ba4e3`), i.e. the lesson's causal account of amendments 1–2 is sound even though its provenance attribution is not receipted.
- The re-key scope really is 30 headings (`c1/lost-headings.json`), and amendment 5 predates the wave-1 dispatch.
- `verify-freeze.sh` re-derives the frozen manifest and prints `FREEZE_INTEGRITY: OK` (exit 0) at e62d997.

## 7. Seat hygiene

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1ScribeLesson` (created with `mkdir -p`; held only the extracted counter blobs, `live161.pdf`, `live162.html`, `layout.txt`, `work/`). Removed before yield.
- No tools installed or upgraded (nothing needed). No git/jj mutation; no commit/push/fetch; the lane tree was read only through `git show`/`cat-file`/`grep`; `verify-freeze.sh` is read-only (it runs `git show` only).
- The lesson was **not** edited (sha at C\* == working tree before and after this seat).
