# RX9 — cold-read re-read: `## Errata — round 16 full-page cold-read` (SKILL.md:1707-1753)

Seat `TameshiR16.RX9-3`. Page at lane commit `34907080f6adda2b18ea13eff23822671cc6930e`,
sha256 `906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397` (verified against
the cold-read interface pin). Snapshot `e69b488` sha256
`97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` (verified, and identical
to `.ufo/evidence/round-16/coldread/SKILL.snapshot.md`). Scratch
`/tmp/tameshi-r16w2-RX9-tYuMqa` (mktemp). Lane tools ran from `/tmp` copies of committed
bytes; sibling repos read-only via `git show`; no tool installs or upgrades.

Scope: page lines 1707-1753 only, plus what that range names — the errata's own diff
(`git -C … diff e69b488 34907080 -- SKILL.md`), the ledger/assemble/snapshot it names, the
report globs it names, and the files/commands each table row cites. Section class:
**record** (it reports what the round did; the only directive-ish sentence, `git log -p --
SKILL.md`, was executed: exit 0, 21 commits, 2697 patch lines).

## Pin, path, and count checks (errata intro)

| Claim | Command | Observed |
|---|---|---|
| snapshot sha `97cf436b…3580` | `git show e69b488:SKILL.md \| sha256sum` | `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` |
| snapshot == `SKILL.snapshot.md` | `sha256sum .ufo/evidence/round-16/coldread/SKILL.snapshot.md` | same sha |
| current page sha | `git show 34907080:SKILL.md \| sha256sum` | `906fb649…1397` |
| 51 buckets = preamble + 50 headings outside fences | python count of `^#{1,6} ` outside fences | snapshot: 50 headings → 51 buckets; post: 53 → 54 |
| 30 cold-read seats (CR01–CR27, three a/b replicas) | ledger pre-version entries | 30 distinct `CR*` labels: CR01…CR27 + CR04a/b, CR11a/b, CR12a/b; 51/51 snapshot sections have ≥1 seat |
| reports `w1/CR*.md` | `git ls-tree 34907080:.ufo/waves/round-16/w1` | 75 files, 38 `CR*` (30 seats + CRCritic1/2 + role reports) |
| re-reads `w2/RR*.md`, `w3/RX*.md` | `git ls-tree 34907080:…/w2`, `…/w3` | w2: 68 files, 16 `RR*` (RR01–RR15, RR12b); w3: 8 files, RX1–RX8 |
| ledger path | `git cat-file -e 34907080:.ufo/evidence/round-16/coldread/ledger.json` | present |
| `coldread/assemble.py` | `git cat-file -e 34907080:.ufo/evidence/round-16/coldread/assemble.py` | present |
| ledger holds merged verdicts/gap counts per bucket | ledger JSON | schema `tameshi-coldread-ledger-v1`, 74 entries with `verdict`/`blocking_gaps`/`wrong_expectations`/`minor_gaps` per section; per version 51 (97cf) + 14 (3d8a1edb) + 9 (e289acec); sections_total 75, covered 74 |
| edits are in-place, cells edited in place, line counts unchanged | hunk parity + `assemble.py:sectionize` on both files | all 14 pre-append hunks are deletion/insertion-equal (4/4, 1/1 ×8, 2/2 ×2, 3/3); final hunk 1 del / 109 add is the EOF-no-newline fix plus the append. Sectionizer: 51 pre sections all present post; **one** changed length (see minor 1) |
| every `SKILL.md:<line>` anchor resolves | `.ufo/evidence/round-16/coldread/anchor-check.txt` (committed at 34907080) + `git diff c699c8c 34907080` | 22/22 anchors RESOLVE, "changed lines (same-index): 19", "heading lines moved/altered inside snapshot span: 0"; later commit's hunks before the tail are same-size (1,13 / 276,8 / 1343,7 / 1388,9 / 1678,7), so no line moved |

## Row-by-row (18 rows)

All "Snapshot line" anchors were checked by printing those lines from `e69b488:SKILL.md`
(all exact), and each "Was"/"Now" against the diff. "Result" is the independent check of the
**Now** claim.

| Row (subject) | Independent check (command → result) | Result |
|---|---|---|
| 15 sufficiency caveat | post line 15 == "…one JS mutant only; round 16 adds a full-page cold-read (Errata — round 16)." | verified |
| 134-135 recipe evidence | post 134-135 name the round-16 full-page cold-read, two seats; ledger bucket 131-245 seats CR04a+CR04b, `commands_executed_count` 18 | verified (report prose not opened — cold-read rule) |
| 63 live-gate exit lattice | `bash claim-ledger.sh --bogus-flag` → `claim-ledger: unknown argument` **exit 2**; `node claims-check.mjs --bogus-flag` → usage block incl. `exit map: … 64 usage`, **exit 64**; surface-probe.mjs selftest itself asserts `unknown flag → exit 64 (usage)` | verified |
| 271-272 two-space substring | against pinned `kimi-census.mjs` (rev 175de6ba, sha 83016d45…): full line count 1, two-space substring count 1; replace both → **byte-identical** mutant, sha `1ea6d77f…f971` each | verified |
| 278-280 `${n}` location | `grep '\${n}'` in both mutation-case notes → rc 1 (absent); present in Appendix A D4 at line 575; the other three tokens present at the cited spots (kimi:157 `slice(0, 6)`, kimi:161 `(mode & m.modeFloor)`, kagi:221 `[[ "$got" -ge "$floor" ]]`) | verified |
| 360-361 D1/D3 16 each, 14 shared | rebuilt D1 and D3 on the pinned suite: control 43/43 pass; D1 16 fails / 27/43 FAIL; D3 16 fails / 27/43 FAIL; intersection **14** (D1-only 2, D3-only 2) | verified |
| 505 23 denied verbs | `claim-ledger.sh:164` is `DENY_WORD_RE=…`; alternation = op, the-janitor, git, rm, mv, cp, chmod, chown, curl, wget, sudo, ssh, scp, systemctl, tmux, kill, pkill, dd, truncate, shred, ln, rsync, tar = **23** | verified |
| 513-515 arm accounting | surface-probe.mjs selftest asserts `--src /nonexistent → exit 2 fail-closed` (1294-1299); cite-check.mjs selftest asserts the bare-run `--src` fail-closed arm exit 2 (2334-2345); both have no token enum beyond their exits (`0/1/2/64`) | verified |
| 925 four legs dated | snapshot 925 exact; post dates it "(r7-1; seven since round 16)"; `REGRESSION_EXPECT` prints 7 legs and the 7 `regression_case_git` calls at 1190-1220 are live | verified (count from registry; full 7-leg replay not run) |
| 949-950 receipt `cases=N` | tool prints `REGRESSION: PASS (cases=%s passed=%s; …)` (line 1247) and `REGRESSION_EXPECT` lists 7 legs | verified |
| 1390, 1393 "(six)" / round-11 record | `corpus/knowledge/mutation-case-*.md` = 7 now, 6 at `e69b488`; `plans/` holds `round-11.plan.md` only, no record file; `LOG.md:316-317` = "the lane deliverables in this repo ARE the wave record (no `.ufo/waves/tameshi-r11-*` directory)"; `corpus/knowledge/closeout-r11.md` exists | verified |
| 1472 Box 3 dated | post 1472 reads "Box 3 was `[ ]` at this write (`[~]` since; Errata — round 16)"; the appended section says the cold-read earns the lane assertion `[~]`, never `[x]` | verified within the page; no external status registry opened |
| 1614 `../PROTOCOL.md` | lane root has no `PROTOCOL.md`; fleet-root `PROTOCOL.md` has `## Gate standard` at line 375 | verified |
| 3, 9-10 frontmatter + two cases | strict YAML: old frontmatter → `ScannerError: mapping values are not allowed here`; current quoted frontmatter parses; post 9-10 say "The first two mutation cases … are worked here (seven recorded since round 16)"; 7 case notes exist | verified |
| 1346 quote now dated | snapshot 1346 exact; post says "(`:925-929`; dated there since round 16)" | verified |
| 1391 six-leg registry | snapshot 1391 exact; post says "six-leg registry at round 11, seven since round 16"; tool registry = 7 live legs | verified |
| round-15 registry disposition row | snapshot row: `--root .` with verdict map "0 clean…"; **today**: `python3 tools/evidence-disposition.py --root <lane> --dispositions .ufo/evidence/round-14/dispositions.json --json` → **exit 2**, `id=expected_input_digest_mismatch` (`tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`); extracted `git archive 28aeef4` (commit = "round-15 verifier spot-check", exists) with `--root <extracted>`, run from the lane root → **exit 0**, `status=clean` | verified |
| round-16 registry assemble row | `c699c8c` row read `64 usage`; `05a2247` row already reads `2 usage (argparse) or an invalid override`; `python3 assemble.py --bogus-flag` → argparse usage, **exit 2**; `--selftest` → `SELFTEST: all checks passed`, exit 0 | verified (repair landed at 05a2247, not the final commit) |

Header/threat-model checks not tied to a row: all four named paths exist at 34907080; the
ledger is honest about itself (`_meta.missing` lists exactly one bucket — this errata section,
post sha `906fb649…`, 1707-1753); `assemble.py` docstring and my count agree on "51 buckets".

## Minor gaps (non-blocking, named)

1. **"line count of every edited section unchanged" is one section short.** Under the page's
   own `assemble.py:sectionize` rule, `### Round-15 gate/probe registry` (start 1676) is 30
   lines in the snapshot (1676-1705) and **31** in the current page (1676-1706): the append
   begins with the blank line 1706, which the sectionizer assigns to the last old section
   (`anchor-check.txt` itself counts the append tail as starting at 1706). The purpose clause
   still holds — 22/22 anchors resolve and all changed lines keep their index — so this is
   wording, not damage.
2. **"Snapshot line" cell without a snapshot line.** The last row's cell says "round-16
   registry, assemble row", but that registry was created by round 16 (`c699c8c`); no such
   line exists in the snapshot `e69b488` the column header and intro name. It is a
   page-location reference in a column defined as snapshot line.
3. **Ledger merge does not cover 5 rows' "Found by" labels.** `_meta.reports_loaded` (61
   reports) contains CR01–CR27, CRRevenger, CRSource, RR01–RR15(+RR12b), RX1–RX8 and the
   Replicas, but **not** CRCritic1, CRCritic2, or WholePage (rows 1, 2, 12, 15); and RR11
   (row 16) is a seat only of the errata bucket at `3d8a1edb` (1707-1739), not of the
   line-1391 bucket (1380-1395: seats CR23+RR08). The reports exist in `w1/` and `w2/`, so
   attribution is plausible, but those findings are not represented in any per-bucket gap
   count — a reader reading "the merged verdict and gap counts per bucket" as complete
   provenance cannot reconcile them. Seat reports themselves were not opened (cold-read rule).

Observations, not gaps: the ledger's own `_meta` declares 74/75 coverage with this errata
bucket the single miss (the residual re-read, this seat, closes it); every other header claim
matched exactly; every one of the 18 rows' command/exit expectations that was executed held
(`exit 2/64/0` as stated), and no row states a behavior I could falsify.

## Verdict

18/18 errata rows are accurate against the diff and their cited artifacts (commands and exits
re-executed), all named paths exist at 34907080, and the only defects are three non-blocking
wording/provenance minors (one section's line count moved by a trailing blank; a
"snapshot line" cell that is not in the snapshot; ledger-merge seats missing five rows'
"Found by" labels) — no blocking gap and no wrong expectation.

```json
{"seat":"RX9","skill_sha256":"906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397","sections":[{"start":1707,"heading":"## Errata — round 16 full-page cold-read","class":"record","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["`line count of every edited section unchanged` is one section short: under assemble.py sectionize, `### Round-15 gate/probe registry` (start 1676) is 30 lines in the snapshot (1676-1705) vs 31 in the current page (1676-1706) because appended blank line 1706 is assigned to the last old section; anchors still resolve 22/22 and changed lines keep their index.","`Snapshot line` cell for the last row (`round-16 registry, assemble row`) names a table that does not exist in snapshot e69b488 — it was created by round 16 at c699c8c; the cell is a page-location reference, not a snapshot line.","The ledger's merged seats omit five rows' `Found by` labels: CRCritic1 (rows 1, 2, 12), CRCritic2 (row 12), WholePage (row 15) are absent from `_meta.reports_loaded` (61 reports), and RR11 (row 16) is a seat only of the errata bucket at 3d8a1edb:1707-1739, not of the line-1391 bucket (1380-1395: CR23+RR08); reports exist in w1/w2, so those findings are absent from per-bucket gap counts."],"commands_executed":["git show 34907080:SKILL.md | sha256sum → 906fb649…1397","git show e69b488:SKILL.md | sha256sum → 97cf436b…3580 (== SKILL.snapshot.md)","git diff --numstat e69b488 34907080 -- SKILL.md → 134 26","git log -p -- SKILL.md (-c core.pager=cat) -> exit 0, 21 commits, 2697 lines","python3 hunk parity → all 14 pre-append hunks deletion==insertion","python3 heading count outside fences → snapshot 50 headings/51 buckets; post 53/54","python3 assemble.py sectionize pre/post → 1 changed section (1676: 30→31)","python3 assemble.py --selftest → exit 0, SELFTEST: all checks passed","python3 assemble.py --bogus-flag → exit 2 (argparse usage)","python3 evidence-disposition.py --root <lane> --dispositions .ufo/evidence/round-14/dispositions.json --json → exit 2, id=expected_input_digest_mismatch","git archive 28aeef4 | tar -x; python3 evidence-disposition.py --root <extract28> … → exit 0, status=clean","bash claim-ledger.sh --bogus-flag → exit 2","node claims-check.mjs --bogus-flag → exit 64","node pristine.mjs --selftest → 43/43 pass, exit 0","node mutant-D1.mjs --selftest → 27/43 FAIL, exit 1, 16 fail labels","node mutant-D3.mjs --selftest → 27/43 FAIL, exit 1, 16 fail labels; D1∩D3 = 14","python3 replace D3 full-line vs two-space substring → byte-identical mutant sha 1ea6d77f…f971, each count 1","grep '\\${n}' mutation-case-kimi/kagi-census.md → rc 1; Appendix A line 575 contains it","python3 yaml.safe_load(old frontmatter) → ScannerError mapping values are not allowed here; quoted parses","grep DENY_WORD_RE claim-ledger.sh → line 164, 23 verbs","grep --src selftest arms surface-probe.mjs:1294-1299, cite-check.mjs:2334-2345 → both assert exit 2","grep REGRESSION_EXPECT + 7 regression_case_git calls mutate-and-run.sh:1190-1220","git ls-tree 34907080:.ufo/waves/round-16/{w1,w2,w3} → 75/68/8 files","python3 ledger analysis → 74 entries, 51/14/9 per version, 30 CR seats, reports_loaded 61, missing=[errata 1707-1753]","grep -n 'Gate standard' PROTOCOL.md → 375; lane PROTOCOL.md absent","ls plans/; git show 34907080:corpus/knowledge/closeout-r11.md; awk LOG.md:314-318","python3 anchor evidence anchor-check.txt → 22/22 RESOLVES, 19 same-index changed lines"],"opened":["SKILL.md:1707-1753 at 34907080","git diff e69b488 34907080 -- SKILL.md","SKILL.md at e69b488, c699c8c, 05a2247 (anchors/errata evolution)",".ufo/evidence/round-16/coldread/ledger.json",".ufo/evidence/round-16/coldread/assemble.py",".ufo/evidence/round-16/coldread/anchor-check.txt",".ufo/evidence/round-16/coldread/SKILL.snapshot.md",".ufo/waves/round-16/w1 (listing), w2 (listing), w3 (listing)","corpus/knowledge/mutation-case-kimi-census.md","corpus/knowledge/mutation-case-kagi-census.md","corpus/knowledge/gates-survey-kumitate.md:285-295","kagi-shokunin/corpus/claim-ledger.sh","kumitate-shokunin/scripts/claims-check.mjs","kumitate-shokunin/scripts/kimi-census.mjs (rev 175de6ba)","kumitate-shokunin/scripts/surface-probe.mjs:1288-1302","kumitate-shokunin/scripts/cite-check.mjs:2330-2348,2514-2526","tools/mutate-and-run.sh (registry/receipt/legs)","tools/evidence-disposition.py (committed copy)","PROTOCOL.md (fleet root):375","LOG.md:314-318","plans/ (listing)","corpus/knowledge/closeout-r11.md"],"scratch":"/tmp/tameshi-r16w2-RX9-tYuMqa"}]}
```
