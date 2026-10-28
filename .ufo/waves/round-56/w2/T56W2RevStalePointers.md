# T56W2RevStalePointers — round-56 pointer resolution at C0

Seat: `T56W2RevStalePointers` (wave 2, round 56 / hyaku run 11).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit under review: **C0 = `c0137451f5b7f22d65f748fc69f1b181f55e1378`**.
Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; frozen instruments `c3e2ca9f020776b3d66c7af854fb82c834674fcf`.

Scope: resolve every pointer the round's **new** content introduces at C0 — the SOURCES row's
URL/anchor, the knowledge entry's `S###` citation and its URL, the QUALITY criterion's command
and code, the SKILL bullet's gate path, the registry cell's selftest command, and every
`corpus/lessons/round-56.md` reference. Each row states the pointer, the resolution command,
the observed value, and ok/stale. A pointer that resolves to a different line than claimed is
**stale** and is named with the correct value.

No lane production file was edited. Receipts: `.ufo/waves/round-56/w2/T56W2RevStalePointers-receipts/`.

---

## 1. Pointer table

| # | pointer | resolution command | observed value | verdict |
|---|---|---|---|---|
| P1 | SOURCES S281 URL `https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md` | `curl -fsSL https://raw.githubusercontent.com/in-toto/attestation/v1.2.0/spec/v1/statement.md \| sha256sum` (R08) | HTTP 200, 2492 B, sha256 `cbe684a18b81…585ebea` — equals the committed snapshot `.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md` and the SOURCES row's `cbe684a1…ebea` | **ok** |
| P2 | SOURCES S281 anchor "§Fields, `subject` field, snapshot lines 36-37 and 54-55" | `awk 'NR==36\|\|NR==37\|\|NR==54\|\|NR==55' .ufo/evidence/round-56/assimilation/in-toto-statement-v1.md` (R08) | line 36-37 = `Set of software artifacts that the attestation applies to…MUST have digest set`; 54-55 = `IMPORTANT: Subject artifacts are matched purely by digest, regardless of / content type.` — the row's lines are right | **ok** |
| P3 | SOURCES S281 pin "tag v1.2.0 (commit df02077b; identical at main 50bf0171)" | `git ls-remote --tags … v1.2.0`; `git ls-remote … refs/heads/main`; `curl … /main/spec/v1/statement.md` (R08) | `df02077bf97218a8860a5c534eff1f1381f56984` = `refs/tags/v1.2.0`; main HEAD `50bf01716982189898823e90586075f37cd9bb7d`; main body sha256 identical to the tag body | **ok** |
| P4 | SOURCES S282 URL `https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md` + "blob sha256 efece57a…76fc" + "path last changed ba7d291a, 2026-10-19" | `curl -fsSL …/slsa/main/spec/build-provenance.md \| sha256sum`; GitHub commits API on that path (R10) | HTTP 200, sha256 `efece57ac1dd…ca76fc` = the row's `efece57a…76fc`; newest commit touching the path is `ba7d291a1521` dated `2026-10-19T17:35:05Z` | **ok** |
| P5 | SOURCES S282 row's `mined` cell (last column) | `awk -F'\|' '/^\| S28[12] /{print $13}' corpus/SOURCES.md` | S281 `mined` → `corpus/knowledge/receipt-revision-binding.md` (exists at C0); S282 → `—` with status `rejected` | **ok** |
| P6 | knowledge entry front-matter `source:` cites **S281** with URL + "IMPORTANT paragraph at lines 54-55" | `head -1 corpus/knowledge/receipt-revision-binding.md`; the fetch of P1/P2 | matches the S281 row's URL, anchor, sha256, 2492 B and "byte-identical at `main`" | **ok** |
| P7 | knowledge entry front-matter cites **S103** — `https://git-scm.com/docs/git-hash-object` — "§DESCRIPTION, first sentence @ page fetched 2026-10-24 (a blob's object id is computed from the contents of the named file…)" | `curl -fsSL https://git-scm.com/docs/git-hash-object`; strip tags at `DESCRIPTION`; `grep 'contents of the named file'` | live page HTTP 200, 29 933 B; the DESCRIPTION body reads *"Computes the object ID value for an object with specified type with the contents of the named file (which can be outside of the work tree)…"*. The **phrase** `contents of the named file` is present (1 hit live, 1 hit in the committed `.ufo/evidence/round-36/src/s103-git-hash-object.html`); S103's own row already pins that snapshot's sha256 `dd826dae…f6100` and 29 933 B, so the citation is consistent with the corpus | **ok** |
| P8 | knowledge `recheck:` — "`python3 tools/receipt-revision-gate.py --selftest` must print `GATE_SELFTEST: 14/14 pass`" | `python3 tools/receipt-revision-gate.py --selftest` at C0 (R01) | **`GATE_SELFTEST: 19/19 pass`** — the tree at C0 carries the amended gate (19 cases). 14/14 is the count of the **frozen** gate at `c3e2ca9f` (R02), which is no longer the tree's gate | **STALE** → correct value `19/19 pass` |
| P9 | knowledge `source:` — "own work — `tools/receipt-revision-gate.py` (sha256 `1d80f8a6…fbd2` at `c3e2ca9f`)" and §Re-derive step 1 `git show c3e2ca9f:… \| sha256sum  # 1d80f8a6…fbd2` | `git show <rev>:tools/receipt-revision-gate.py \| sha256sum` for c3e2ca9f / 21eb3c6 / C0 (R03) | c3e2ca9f = `1d80f8a6…78fbd2` (matches the note); **C0 = `c60772ce…569ac9`** (the amendment commit `21eb3c6` rewrote the gate). The note's own-work sha is right *for the freeze* but is not the tree's sha at C0 | **STALE** → correct value `c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9` |
| P10 | knowledge — "The lane's own surface is `.ufo/evidence/round-56/control/frozen-surface.paths` — **nine paths**: SKILL.md, corpus/QUALITY.md, corpus/SOURCES.md, corpus/knowledge, tools/registry.json, the gate itself, the cold-read ledger and both counters." | `wc -l .ufo/evidence/round-56/control/frozen-surface.paths`; same at c3e2ca9f (R04) | **16 lines at C0** (9 at c3e2ca9f). The nine named paths are the *first nine* lines; the amendment added 7 more: `contract.json`, `freeze.json`, `controls.sh`, `deciding-run.sh`, `no-harm.sh`, `c2/red-before/round-54-ctl-pos-c1.stdout`, `…stdout.sha256` | **STALE** → correct value "sixteen paths" |
| P11 | knowledge — "gate 0b gates the lane's own control receipts at `$REV` (`.ufo/evidence/round-56/deciding-run.sh:66-74`) and gate 0c … (`:100-107`)" | `grep -n 'gate 0b\|gate 0c' .ufo/evidence/round-56/deciding-run.sh` (R05) | 66/100 are the **c3e2ca9f** line numbers; at C0 gate 0b is at **line 114** and gate 0c at **line 156** (`deciding-run.sh` was rewritten by amendment `21eb3c6`) | **STALE** → correct values `:114` (0b) and `:156` (0c) |
| P12 | knowledge — "the closed list of eleven" codes; "case `codes-closed`" | `python3 -c` parse of `CODES = (...)`; `--selftest` output | 11 codes, exactly as listed (`RECEIPT_MISSING` … `RECEIPT_REQUIRED_LINE_MISSING`); `CASE codes-closed PASS` present | **ok** |
| P13 | knowledge §Re-derive step 2 (ER-R54-1 positive control refused at `c21081008adb` with `--paths`) | the command verbatim (R11/R13) | `GATE REFUSED … code=RECEIPT_REV_CONTENT_DRIFT … drift=.ufo/evidence/round-21/coldread/ledger.json,…` exit 3; at its own rev `077d431e…` → `verdict=PASS` exit 0. The drift list matches the note's "`drift=.ufo/evidence/round-21/coldread/ledger.json,…`" | **ok** |
| P14 | knowledge §Re-derive steps 3 & 4 (`controls-b.stdout:positive` → `RECEIPT_REV_UNRESOLVABLE`; `round-55/after/c2.stdout:verdict` → `RECEIPT_REV_ABSENT`) | the commands verbatim (R13/R14) | step 3: `code=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98` exit 3; step 4: `code=RECEIPT_REV_ABSENT no rev= token` exit 3. `7df0e0426c98` does not resolve (`git rev-parse --verify` prints nothing) — the note says so | **ok** |
| P15 | knowledge §Re-derive step 6 — `bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo.sh` (and `-demo2.sh`) | the command verbatim, from the lane root, with `HYAKU_SCRATCH` unset (R06); and from `/tmp` (R07) | **exits 1**: `line 8: HYAKU_SCRATCH: parameter null or not set`. The scripts hard-require `HYAKU_SCRATCH` (`BASE=${HYAKU_SCRATCH:?}`) and the relative path only resolves from the lane root. The note's §Re-derive block sets `L=` but never exports `HYAKU_SCRATCH` and never `cd`s | **STALE** → correct invocation `export HYAKU_SCRATCH=/fast/scratch/hyaku; cd "$L"; bash …` |
| P16 | knowledge §Re-derive step 5 — `cat .ufo/evidence/round-54/after/deciding-run.exit` → `DECIDING_RUN_EXIT=0` | `cat` | `DECIDING_RUN_EXIT=0` | **ok** |
| P17 | knowledge — "the same file, line `CTL_EXIT0` \| `rev=7df0e0426c98` \| certified `c2108100`"; "`CTL_POS_c1` \| `rev=077d431e6996`"; "`round-55/after/c2.stdout` … 0 matches for `rev=` and for a JSON `rev` key, 28 lines" | `grep -n 'CTL_POS_c1\|CTL_EXIT0' .ufo/evidence/round-54/control/controls-b.stdout`; `grep -c 'rev='`/`grep -c '"rev"'`/`wc -l` on round-55 c2.stdout | `CTL_POS_c1 … rev=077d431e6996` (line 1), `CTL_EXIT0 … rev=7df0e0426c98` (line 4); round-55 c2.stdout: 0 / 0 / 28 lines | **ok** |
| P18 | knowledge — "`corpus/lessons/round-54-verifier-spotcheck.md` (R54.1)", "`corpus/lessons/round-55-verifier-spotcheck.md` (R55.5)", "`ER-R54-1`" | `grep -n 'R54.1' corpus/lessons/round-54-verifier-spotcheck.md`; `grep -n 'R55.5' …`; `grep -rn 'ER-R54-1' corpus/ SKILL.md` | R54.1 at line 11/75/100; R55.5 at line 134 of the round-55 spotcheck; `ER-R54-1` defined at `SCORECARD.md:2631`. All three files exist at C0 | **ok** |
| P19 | QUALITY 107 "Check that can fail" command, "run from any cwd" | the block verbatim from `/tmp` (R11) | prints `code=RECEIPT_REV_CONTENT_DRIFT` on the `GATE REFUSED` line and `codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED` on the summary line, exit **3** — exactly as the criterion states; the same receipt at `077d431e…` prints `verdict=PASS`, exit 0 | **ok** |
| P20 | QUALITY 107 falsifier — "at the round-56 freeze `c3e2ca9f` … `corpus/QUALITY.md` names neither `tools/receipt-revision-gate.py` nor any `RECEIPT_*` code" | `git show c3e2ca9f:corpus/QUALITY.md \| grep -c 'receipt-revision-gate\|RECEIPT_'` | `0` — the claim holds | **ok** |
| P21 | QUALITY 107 falsifier — "round 54's deciding run accepted the set this command refuses (`.ufo/evidence/round-54/after/deciding-run.exit` reads `DECIDING_RUN_EXIT=0`)" | `cat` | `DECIDING_RUN_EXIT=0` | **ok** |
| P22 | QUALITY 107 — "Lesson: `corpus/lessons/round-56.md` `## Gate` (the R55.5 disposition — … names `077d431e6996` on `CTL_POS_c1` and `7df0e0426c98` on `CTL_EXIT0` while the round measured `c2108100`)" | `sed -n '15,37p' corpus/lessons/round-56.md \| grep -c 'R55.5\|077d431e6996\|7df0e0426c98\|c2108100'`; `grep -n '^| R55.5 |'` (R19) | The lesson's `## Gate` section (the sources table) contains **0** of those tokens. The R55.5 disposition is in a **different** section, `## Round-55 routed defects — dispositions (this round)`, at line 99 | **STALE** → correct section `## Round-55 routed defects — dispositions (this round)` (line 99) |
| P23 | QUALITY 107 scope-gap pointer — "`.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`, exit 0 on `rev=077d431e6996 credited=99 lost=0`" | `git cat-file -e C0:<path>`; `grep -c 'credited=99' <path>` (R20) | The file is **not committed at C0** (wave-1 output; `git ls-tree C0 -- .ufo/waves/round-56` = 0 files). Its text is `revs=077d431e6996` / `verdict=PASS` / `exit=0`; the string `credited=99` appears **0** times in it — the quoted payload is the *fabricated* receipt the fixture fed, not the receipt's own bytes | **STALE** → correct quote is the receipt's own line `revs=077d431e6996 … verdict=PASS … exit=0`; the cited path resolves only in the wave-1 worktree, not at C0 |
| P24 | lesson round-56 — "Census at round end: `<L1 fills>`"; "Content commit C0 `<L1 fills>`"; "amendments `<L1 fills>`"; after-paths `<L1 fills>` | `grep -n '<L1 fills>' corpus/lessons/round-56.md` | 4 unfilled placeholders (lines 12, 27, 95, 97) — the L1 fills these; the lesson's own `## Mistakes` says so | **ok (L1-owned placeholder, not a stale pointer)** |
| P25 | lesson round-56 — every backticked `.ufo/**` path vs. the tree at C0 | `git cat-file -e C0:<path>` for each (R18) | 13 of 16 resolve at C0. The 3 that do not are the `<L1 fills>` after-paths (P24) and the wave-1 file `.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt` (P23). Everything else — `.ufo/evidence/round-54/…`, `round-55/…`, `round-56/{before,c2,contract,controls,deciding,freeze}.*`, `round-56/assimilation/in-toto-statement-v1.md`, `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` — is committed at C0 | **ok except P23** |
| P26 | lesson round-56 — "Base `981c5e8b`"; "frozen at `c3e2ca9f`"; "the contract, both counters, `tools/receipt-revision-gate.py`, `controls.sh`, `no-harm.sh` and `deciding-run.sh` are frozen at `c3e2ca9f`" | `git show <rev>:<file> \| sha256sum` for each frozen file at c3e2ca9f and C0 (R02/R03 and the R-file comparison) | The freeze manifest at C0 records **12** files and **1** amendment; `c3e2ca9f` recorded 10 files and 0 amendments. `contract.json`, `c2/measure.py`, `control/frozen-surface.paths`, `controls.sh`, `deciding-run.sh` and `tools/receipt-revision-gate.py` all **changed** between c3e2ca9f and C0 | **STALE** → the freeze is `c3e2ca9f` **+ amendment 1 at `21eb3c6`**; the lesson's "frozen at `c3e2ca9f`" plus its `<L1 fills>` for `amendments` must name the amendment |
| P27 | lesson round-56 — "`R55.5` — the deciding gate cannot compare the revision it certifies — is C2"; "`corpus/lessons/round-55-verifier-spotcheck.md`, verdict `rejected-harmed`" | `grep -n 'rejected-harmed' corpus/lessons/round-55-verifier-spotcheck.md`; `grep -n 'R55.5' …` | line 11 `verdict: **not admitted — \`rejected-harmed\`.**`; R55.5 at line 134 of the same file. Both exist at C0 | **ok** |
| P28 | lesson round-56 — R55.4 evidence "`.ufo/evidence/round-55/control/controls-a.stdout` (`CTL_SKIP_c2 … total=4`, `CONTROLS_A: 5/5`)" | `grep -n 'CTL_SKIP_c2\|CONTROLS_A:' .ufo/evidence/round-55/control/controls-a.stdout` | line 5 `CTL_SKIP_c2 … total=4`; line 6 `CONTROLS_A: 5/5 as pre-registered` | **ok** |
| P29 | lesson round-56 — R55.2 evidence "`.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` (`total=1 C2_R55_PASS=false` where the report quoted `total=0`)" | `cat` | the receipt's last line reads `… total=1 C2_R55_PASS=false`; committed at C0 | **ok** |
| P30 | lesson round-56 — R55.5 "red-before: `.ufo/evidence/round-56/before/c2.stdout` (`red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE`, `docs=0/4`)" and R55.3 "`.ufo/evidence/round-56/before/c1.stdout` (`credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 restate=8`)" | `cat` both receipts | `before/c2.stdout`: `red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE … docs=0/4`; `before/c1.stdout`: `credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 restate=8` — both verbatim | **ok** |
| P31 | lesson round-56 — "the `before/` receipts … not in any commit (`git cat-file -e c3e2ca9f:.ufo/evidence/round-56/before/c1.stdout` → absent)" and "fix: C0 commits `before/{c1,c2,c2-at-base}.stdout`" | `git cat-file -e c3e2ca9f:.ufo/evidence/round-56/before/c1.stdout`; `git ls-tree C0 -- .ufo/evidence/round-56/before` | absent at c3e2ca9f; the three `before/` files **are** committed at C0 | **ok** |
| P32 | lesson round-56 — "**fix**: C0 commits `before/{c1,c2,c2-at-base}.stdout` (and the wave-1 reports and receipts)" | `git ls-tree -r C0 -- .ufo/waves/round-56 \| wc -l` | **0** — C0 commits the `before/` receipts but **not** the wave-1 reports and receipts it says it commits | **STALE** → at C0 only the `before/` receipts are committed; the wave-1 deliverables are still untracked |
| P33 | SKILL.md standing rule — gate path `tools/receipt-revision-gate.py --lane LANE --certified REV` | `git cat-file -e C0:tools/receipt-revision-gate.py`; `python3 tools/receipt-revision-gate.py --help`-style invocation (R15) | the file exists at C0 (sha `c60772ce…`); the literal form **without** `--receipt` exits 1 with the usage line (`--receipt PATH:ROLE[:REGEX] …` is required). The path and the two flags are real; only the minimum-arity is not shown | **ok** (path and flags resolve; the bullet quotes the flag pair, not a full command — note, not a finding) |
| P34 | SKILL.md standing rule — "round-56 C2; ER-R54-1, R55.5"; the four code names `RECEIPT_REV_MISMATCH` / `RECEIPT_REV_CONTENT_DRIFT` / `RECEIPT_REV_UNRESOLVABLE` / `RECEIPT_REV_ABSENT` | `grep -n 'ER-R54-1' SCORECARD.md`; the `CODES` tuple parse | `ER-R54-1` defined at `SCORECARD.md:2631`; all four codes are members of the gate's 11-code list | **ok** |
| P35 | SKILL.md standing rule sits inside `## Standing rules` (the C2 counter's SKILL cell scopes to that section) | `grep -n '^## ' SKILL.md`; `grep -n 'A receipt is evidence only' SKILL.md` | `## Standing rules` at line 17, `## Source notes` at line 58; the new bullet is at line 45 → inside. `c2/measure.py` at C0 scores `docs=4/4` | **ok** |
| P36 | registry cell `receipt-revision-gate-selftest` — argv `python3 tools/receipt-revision-gate.py --selftest`, expect exit 0 and `GATE_SELFTEST: 19/19 pass` + 11 named `CASE … PASS` lines | `python3 tools/receipt-revision-gate.py --selftest` from the lane root (R16) | exit 0, prints `GATE_SELFTEST: 19/19 pass` and every one of the 11 expected CASE lines | **ok** |
| P37 | registry cell `source` — `tools/receipt-revision-gate.py@21eb3c63cd0f3190c0deeb8953c6c91c7742cd68:10-29` | `git show 21eb3c6:tools/receipt-revision-gate.py \| sed -n '10,29p'` (R17) | resolves: line 10 = `Usage:`, line 29 = `  RECEIPT_DIGEST_MISMATCH · RECEIPT_REQUIRED_LINE_MISSING` — the usage/roles/codes block the cell documents | **ok** |
| P38 | registry cell `scratch_root` — "with TMPDIR unusable it falls back to the platform default `/tmp` with no could-not-evaluate line and exit 0" | `TMPDIR=/nonexistent/nope python3 tools/receipt-revision-gate.py --selftest`; `TMPDIR=/nonexistent/nope python3 -c "import tempfile;print(tempfile.mkdtemp(prefix='tameshi-r56-gate-'))"` | exit 0, `19/19 pass`, no could-not-evaluate line; the fixture lands in `/tmp/tameshi-r56-gate-ou1_0v2q` | **ok** |
| P39 | census — `scripts/sources-census.sh validate --root … tameshi` must exit 0 with **141** rows after this round's one new row | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`; `… census … \| grep '^tameshi rows'` (R21) | validate exits **0** ✓, but the census counts **142** rows: base `981c5e8b` = 140, C0 = **142**. The round adds **two** rows (S281 `mined` **and** S282 `rejected`), not one | **STALE** → correct count **142** (140 + 2) |
| P40 | SOURCES "Round 56:" roll-up — "one row added for the sourced C2 claim, S281 … Next unused id: S283" and "A second candidate (SLSA Build Provenance) was opened and added as the REFUSED row S282" | `grep -c '^| S283' corpus/SOURCES.md` | S283 is free ✓. The roll-up text itself already says two rows are added (S281 + S282) — it is the *assignment's* "one new row" / "141 rows" expectation that is stale, and the census agrees with the corpus (142) | **ok** (SOURCES roll-up is right) |
| P41 | lesson `## Gate` table — S281 row quote "Subject artifacts are matched purely by digest, regardless of content type." at "snapshot lines 54–55, `> ` stripped", 11 words | `awk` over the committed snapshot; `python3` word count | exactly the two snapshot lines, 11 words ✓ | **ok** |
| P42 | lesson `## Gate` table — S282 row quote "Provenance is a predicate that describes how a software build was executed." at "§Model, first paragraph (reader extraction, 11 words)" | `grep -c` over the fetched body **and** over the wave-1 extraction receipt (which is byte-identical, sha `efece57a…76fc`) (R10) | **0 hits in both.** The actual first paragraph of `## Model` is "Provenance is an attestation that a particular build platform produced a set of software artifacts through execution of the `buildDefinition`." The claimed sentence appears at no SLSA tag (`v0.1`, `v1.0.0`, `v1.1`, `v1.2`, `v0.2` paths all 0 hits) nor at slsa.dev/provenance/v0.2 (0 hits). The string is also **12** words, not 11 | **STALE** → correct value: the `## Model` first paragraph quoted above; the quoted sentence is not in the document at the cited anchor |
| P43 | lesson `## Gate` table — DSSE row (§Signature Definition, line 27) and the "no row" rejection | `curl …/dsse/master/protocol.md`; `awk 'NR==27'` | line 27 = `*   SERIALIZED_BODY: Arbitrary byte sequence to be signed.`; `## Signature Definition` heading at line 11 ✓. No DSSE snapshot is committed in the tree — but the row is explicitly "(no row)", so nothing in the corpus depends on it | **ok** |

---

## 2. Findings — FALSE claims and FAILING commands

Every finding carries the command that produced it and its output.

### F1 (stale) — knowledge entry's `recheck:` and §Falsifier 3 name a selftest count the tree no longer produces

The note's `recheck:` line says *"`python3 tools/receipt-revision-gate.py --selftest` must print
`GATE_SELFTEST: 14/14 pass`"*, and its Falsifier item 3 says *"`--selftest` reports anything other
than `14/14 pass` … this note is wrong"*. At C0 the tree's gate is the **amended** gate and prints
**19/19**. A reader following the recheck instruction at C0 is told the note is wrong, and the
falsifier fires on the note itself.

```
$ python3 tools/receipt-revision-gate.py --selftest          # at C0 worktree
...
CASE unresolvable-certified-refused PASS
GATE_SELFTEST: 19/19 pass
exit=0

$ git show c3e2ca9f:tools/receipt-revision-gate.py > gate-freeze.py && python3 gate-freeze.py --selftest
CASE codes-closed PASS
GATE_SELFTEST: 14/14 pass          # the freeze-era gate — no longer the tree's gate
exit=0
```

Correct value at C0: **`GATE_SELFTEST: 19/19 pass`** (the 19-case suite the amendment added).
Receipt: `pointers-01-selftest-surface-gates.txt` §R01–R02.

### F2 (stale) — knowledge entry pins the wrong gate sha256 as the tree's own work

`source:` says *"own work — `tools/receipt-revision-gate.py` (sha256 `1d80f8a6…fbd2` at `c3e2ca9f`)"*
and §Re-derive step 1 comments `# 1d80f8a6…fbd2`. The sha is right for the **freeze**, but the
gate **in the tree at C0** is the amended one:

```
c3e2ca9f: 1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2
21eb3c6  : c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9
C0       : c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9
worktree : c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9
```

Correct value: **`c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`** (amendment
`21eb3c6`). The `recheck:` sha and the §Re-derive step-1 sha both need updating, or the note must
say explicitly that it describes the frozen bytes and not the tree's.
Receipt: `pointers-01-selftest-surface-gates.txt` §R03.

### F3 (stale) — knowledge entry calls the frozen surface "nine paths"; it is sixteen at C0

The note states *"The lane's own surface is `.ufo/evidence/round-56/control/frozen-surface.paths` —
nine paths"*, and enumerates nine. The file at C0 has **16** lines; the nine named are lines 1–9 and
the amendment added seven more:

```
c3e2ca9f: 9
C0      : 16
--- C0 list ---
SKILL.md
corpus/QUALITY.md
corpus/SOURCES.md
corpus/knowledge
tools/registry.json
tools/receipt-revision-gate.py
.ufo/evidence/round-21/coldread/ledger.json
.ufo/evidence/round-56/c1/measure.py
.ufo/evidence/round-56/c2/measure.py
.ufo/evidence/round-56/contract.json          <- added by the amendment
.ufo/evidence/round-56/freeze.json            <- added by the amendment
.ufo/evidence/round-56/controls.sh            <- added by the amendment
.ufo/evidence/round-56/deciding-run.sh        <- added by the amendment
.ufo/evidence/round-56/no-harm.sh             <- added by the amendment
.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout        <- added by the amendment
.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout.sha256 <- added by the amendment
```

Correct value: **sixteen paths**. The note's nine-path list also names "the cold-read ledger and both
counters" without `contract.json`/`freeze.json`/`controls.sh`/`deciding-run.sh`/`no-harm.sh`, i.e. the
pre-amendment surface. This matters because the surface is what the exception is bounded by: the note
says *"A round that widens the surface widens what a stale control may certify, so the list is frozen
with the instrument."* The round-56 surface is wider than the note says.
Receipt: `pointers-01-selftest-surface-gates.txt` §R04.

### F4 (stale) — knowledge entry's `deciding-run.sh` line pointers point at the wrong lines at C0

The note says *"gate 0b gates the lane's own control receipts at `$REV`
(`.ufo/evidence/round-56/deciding-run.sh:66-74`) and gate 0c gates the verdict receipts the run has
just produced (`:100-107`)"*. Those are the `c3e2ca9f` line numbers. `deciding-run.sh` was rewritten
by amendment `21eb3c6`, so at C0:

```
C0:        114:# gate 0b (this round's C2): the lane's own receipts must pass the binding gate.
           156:# gate 0c: the verdicts this run just produced must name the certified revision.
c3e2ca9f:  66:# gate 0b (this round's C2): the lane's own receipts must pass the binding gate.
           100:# gate 0c: the verdicts this run just produced must name the certified revision.
```

Correct values: **`:114`** for gate 0b and **`:156`** for gate 0c (the note's own two blocks run
114–127 and 156–163).
Receipt: `pointers-01-selftest-surface-gates.txt` §R05.

### F5 (FAILING command) — knowledge §Re-derive step 6 fails as written

The note's §Re-derive step 6 is:

```sh
bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo.sh
bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo2.sh
```

Run verbatim from the lane root, as the surrounding block implies (`L=…` is set but never `cd`-ed
to, and `HYAKU_SCRATCH` is never exported):

```
$ env -u HYAKU_SCRATCH bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo.sh
.ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo.sh: line 8: HYAKU_SCRATCH: parameter null or not set
exit=1
```

The scripts hard-require `HYAKU_SCRATCH` (`BASE=${HYAKU_SCRATCH:?}`) and use a **relative** path, so
they also fail from any other cwd:

```
$ cd /tmp && bash …/fixture-gate-demo.sh
…/fixture-gate-demo.sh: line 8: HYAKU_SCRATCH: parameter null or not set
exit=1
```

With `HYAKU_SCRATCH` exported and cwd = lane root, both scripts run and reproduce the note's
measured table (case 2 → `RECEIPT_REV_MISMATCH`, case 3 → PASS, case 4 → `RECEIPT_REV_CONTENT_DRIFT`
`drift=b.txt`, case 6 → `RECEIPT_CONTROL_NOT_ANCESTOR`, case 7 → PASS blind spot, case 8 →
`RECEIPT_REV_CONTENT_DRIFT` with `drift=<no --paths given: content identity is not checkable>`,
case 9 → PASS 7-hex prefix, case 10 → `RECEIPT_REV_ABSENT`, case 11 → `RECEIPT_REV_AMBIGUOUS`).
**The measurements are right; the command as printed does not run.** Correct invocation:
`export HYAKU_SCRATCH=/fast/scratch/hyaku; cd "$L"; bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo.sh`.
Receipt: `pointers-01-selftest-surface-gates.txt` §R06–R07.

### F6 (stale) — QUALITY 107's Lesson pointer names the wrong lesson section

Criterion 107 says *"Lesson: `corpus/lessons/round-56.md` `## Gate` (the R55.5 disposition — …)"*.
The lesson's `## Gate` section is the sources-opened table (lines 15–37) and contains **none** of the
R55.5 disposition, of `077d431e6996`, of `7df0e0426c98`, or of `c2108100`:

```
$ sed -n '15,37p' corpus/lessons/round-56.md | grep -c 'R55.5\|077d431e6996\|7df0e0426c98\|c2108100'
0
$ grep -n '^| R55.5 |' corpus/lessons/round-56.md
99:| R55.5 | FIXED by C2: `tools/receipt-revision-gate.py` binds each receipt's `rev=` …
```

Correct value: **`## Round-55 routed defects — dispositions (this round)`**, row `R55.5`, line 99.
Receipt: `pointers-04-lesson-census.txt` §R19.

### F7 (stale) — QUALITY 107's scope-gap pointer: wrong quote and the path is not at C0

Criterion 107 says the fabricated receipt *"still passes the gate
(`.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`, exit 0 on
`rev=077d431e6996 credited=99 lost=0`)"*. The receipt's own bytes are:

```
## E. scope gap: a receipt naming the certified rev whose printed numbers are fabricated still PASSES
GATE OK /fast/scratch/hyaku/tameshi-r56/T56W1ScribeQuality/fabricated.stdout role=positive revs=077d431e6996
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

`grep -c 'credited=99'` on that file = **0**. The string `rev=077d431e6996 credited=99 lost=0` is the
*fabricated payload* that was fed in, not a line the receipt carries; the receipt carries
`revs=077d431e6996 … verdict=PASS … exit=0`. The lesson repeats the same wrong quote
(`corpus/lessons/round-56.md:117`). And the path itself is **not committed at C0** —
`git ls-tree -r C0 -- .ufo/waves/round-56` returns **0** files, so the pointer resolves only in the
wave-1 worktree.

Correct value: the receipt's own line `GATE OK … role=positive revs=077d431e6996` / `verdict=PASS` /
`exit=0`, and the file's status must be "not yet committed at C0" until the L1 lands it.
Receipt: `pointers-04-lesson-census.txt` §R20.

### F8 (stale) — the lesson's `## Gate` table quotes a sentence that is not in the SLSA document

The S282 row of `corpus/lessons/round-56.md` `## Gate` gives the located quote as *"§Model, first
paragraph (reader extraction, 11 words): 'Provenance is a predicate that describes how a software
build was executed.'"* The quoted string is **not in the document the row cites**:

```
$ curl -fsSL https://raw.githubusercontent.com/slsa-framework/slsa/main/spec/build-provenance.md | sha256sum
efece57ac1dd6e18c54a2b78e6ff18923a2590c3799c40c87b03572897ca76fc   # == SOURCES row's efece57a…76fc
$ grep -c 'Provenance is a predicate that describes how a software build was executed' <that body>
0
$ grep -c 'Provenance is a predicate that describes' .ufo/waves/round-56/w1/T56W1ScribeSources-receipts/slsa-build-provenance.md
0        # the wave-1 extraction receipt is byte-identical to the fetched body
$ grep -A4 '^## Model' <that body>
## Model

Provenance is an attestation that a particular build platform produced a set of
software artifacts through execution of the `buildDefinition`.
```

The claimed sentence appears at no SLSA tag (`v0.1`, `v1.0.0`, `v1.1`, `v1.2`, plus the `v0.2`
`docs/` and `spec/` paths — all 0 hits) nor at `slsa.dev/provenance/v0.2` (0 hits). It is also **12**
words, not the 11 the row claims.

Correct value: the `## Model` first paragraph, *"Provenance is an attestation that a particular
build platform produced a set of software artifacts through execution of the `buildDefinition`."*
The row's **verdict** (reject — the predicate binds a build to its artifacts, not a receipt to a
revision) is unaffected and stays correct.
Receipt: `pointers-02-urls-anchors.txt` §R10.

### F9 (stale) — the lesson says C0 commits the wave-1 reports and receipts; it does not

`corpus/lessons/round-56.md` `## Mistakes` says *"fix: C0 commits `before/{c1,c2,c2-at-base}.stdout`
(**and the wave-1 reports and receipts**) so every before-pointer resolves at the commit that cites
it (QUALITY 97)."* At C0:

```
$ git ls-tree -r c0137451f5b7f22d65f748fc69f1b181f55e1378 -- .ufo/waves/round-56 | wc -l
0
```

C0 commits the `before/` receipts and the evidence tree, but **no** wave-1 report or receipt. The
lesson's own sentence is therefore a false claim about C0, and the QUALITY 107 / lesson pointers into
`.ufo/waves/round-56/w1/…` (F7) cannot resolve at C0 because of it. Correct value: at C0 the wave-1
deliverables are still untracked; the fix lands only when the L1 commits them.
Receipt: `pointers-04-lesson-census.txt` §R18, §R20.

### F10 (stale) — the lesson describes the freeze as "frozen at `c3e2ca9f`" with no amendment

The lesson says *"the contract, both counters, `tools/receipt-revision-gate.py`, `controls.sh`,
`no-harm.sh` and `deciding-run.sh` are frozen at `c3e2ca9f` (`.ufo/evidence/round-56/freeze.json`,
`amendments` `<L1 fills>`)"*. The manifest at C0 records **12** files and **1** amendment; at
`c3e2ca9f` it recorded **10** files and **0** amendments. Comparing the frozen bytes:

```
CHANGED contract.json  (2530a547 -> 254dd098)
SAME    c1/measure.py
CHANGED c2/measure.py  (d17d36bd -> 91558019)
CHANGED control/frozen-surface.paths  (a0ebd3d4 -> 46c93f10)
CHANGED controls.sh  (df1ee355 -> 65b4b510)
SAME    no-harm.sh
CHANGED deciding-run.sh  (6a63f505 -> a644123e)
SAME    c1/lost-headings-at-base.json
SAME    c2/red-before/round-54-surface.paths
SAME    c2/red-before/round-54-ctl-pos-c1.stdout
```

Correct value: the freeze is **`c3e2ca9f` plus amendment 1 at `21eb3c6`**, and the lesson's
`amendments` field must name that amendment rather than `<L1 fills>`. As written the lesson points
at a freeze that no longer describes the tree — which is the mechanism behind F3 and F4.
Receipt: `pointers-04-lesson-census.txt` §R18 (freeze manifest compared in `pointers-01` §R04/R05).

### F11 (stale count) — the census has 142 tameshi rows at C0, not 141

The assignment expects "141 rows after this round's one new row". The census exits 0, but the count
is **142**:

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi ; echo $?
0
$ bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin | grep -E '^tameshi\s+rows'
tameshi	rows	142
$ git show 981c5e8b…:corpus/SOURCES.md | grep -c '^| S[0-9]'   # base
140
$ grep -c '^| S[0-9]' corpus/SOURCES.md                          # C0
142
```

The round adds **two** S-rows — `S281` (`mined`) and `S282` (`rejected`) — and the corpus says so
itself (`corpus/SOURCES.md` "Round 56:" roll-up: *"one row added for the sourced C2 claim, S281 … A
second candidate (SLSA Build Provenance) was opened and added as the REFUSED row S282"*). Correct
value: **142 rows** (140 + 2). The census requirement (exit 0) is met; only the expected count is
stale.
Receipt: `pointers-04-lesson-census.txt` §R21.

---

## 3. Notes (stale-but-true, style, improvements — not findings)

- **N1** — S281's live URL and every pin on it resolve cleanly (§R08): tag `v1.2.0` →
  `df02077bf97218a8860a5c534eff1f1381f56984`, main `50bf01716982189898823e90586075f37cd9bb7d`,
  2492 B, sha256 `cbe684a1…585ebea` identical at both, and the committed snapshot's sha256 equals
  the fetched body's. The S281 row is the round's best-evidenced pointer.
- **N2** — S103's citation in the knowledge front-matter is carried over from the round-36 row and
  resolves: the live `git-scm.com/docs/git-hash-object` page returns HTTP 200 / 29 933 B, and the
  phrase `contents of the named file` is present (1 hit) both live and in the committed snapshot
  `.ufo/evidence/round-36/src/s103-git-hash-object.html` whose sha256 (`dd826dae…f6100`) is the one
  the S103 row pins. The knowledge note paraphrases it as "a blob's object id is computed from the
  contents of the named file" — the spec says "an object with specified type", so the paraphrase is
  loose, but it is the corpus's own pre-existing wording and not a round-56 pointer defect.
- **N3** — SKILL.md's standing-rule bullet quotes the flag pair
  `tools/receipt-revision-gate.py --lane LANE --certified REV`. The path and both flags are real;
  the tool additionally requires at least one `--receipt` (run verbatim without one it exits 1 with
  the usage line). The bullet is quoting the invocation shape, not a runnable command, so this is
  not a finding — but a reader who copies it gets a usage error rather than a refusal.
- **N4** — The lesson's four `<L1 fills>` placeholders (lines 12, 27, 95, 97) are L1-owned and are
  consistent with the lesson's own convention; they are not stale pointers. The three `<L1 fills>`
  paths inside `## Round-55 routed defects` point into `.ufo/evidence/round-56/after/`, which does
  not exist at C0 — correctly, since those are the deciding receipts the round has not yet produced.
- **N5** — The lesson's DSSE row is marked "(no row)" and cites `## Signature Definition`, line 27 of
  `dsse/blob/master/protocol.md`; that line reads exactly as claimed. No DSSE snapshot is committed
  in the tree, but nothing in the corpus depends on it (rejected before append).
- **N6** — The QUALITY 107 "Check that can fail" block is fully sound: run from a foreign cwd it
  prints `code=RECEIPT_REV_CONTENT_DRIFT` on the `GATE REFUSED` line, `codes=RECEIPT_REV_CONTENT_DRIFT
  verdict=REFUSED` on the summary line and exits 3; the same receipt at its own revision
  `077d431e69965fa4673cd006ab64f6fc387f9e15` prints `verdict=PASS` and exits 0. The falsifier's two
  supporting claims both hold at `c3e2ca9f` (QUALITY names neither the gate nor any `RECEIPT_*`
  code — 0 hits; and `.ufo/evidence/round-54/after/deciding-run.exit` reads `DECIDING_RUN_EXIT=0`).
- **N7** — The registry cell `receipt-revision-gate-selftest` is the one pointer in the round that
  was **updated for the amendment**: it expects `GATE_SELFTEST: 19/19 pass` and all 11 named CASE
  lines, and the C0 gate produces exactly that. Its `source` pointer
  `tools/receipt-revision-gate.py@21eb3c6…:10-29` resolves to the usage/roles/codes block, and its
  `scratch_root` note about the `/tmp` fallback under an unusable `TMPDIR` is exactly what the tool
  does (exit 0, `19/19 pass`, fixture under `/tmp/tameshi-r56-gate-…`).
- **N8** — The knowledge note's substantive measurements all reproduce at C0: the round-54 positive
  control is refused `RECEIPT_REV_CONTENT_DRIFT` with the ledger named; the same file's `CTL_EXIT0`
  line is refused `RECEIPT_REV_UNRESOLVABLE` at `rev=7df0e0426c98` (which genuinely does not
  resolve); round 55's `after/c2.stdout` is refused `RECEIPT_REV_ABSENT`; the eleven-code closed
  list and the `codes-closed` selftest case hold; and `7df0e0426c98`, `077d431e6996`, `c2108100`
  and `4c04c1d33377` resolve exactly as the note says.
- **N9** — `corpus/lessons/round-56.md` cites only three `.ufo/**` paths that are not at C0, and two
  of the three are the `<L1 fills>` after-paths. Every other lane path the lesson cites — the
  round-54/55 evidence, the round-56 `before/`, `c2/`, `contract.json`, `controls.sh`,
  `deciding-run.sh`, `freeze.json`, `no-harm.sh`, `assimilation/`, and the round-55 wave receipt
  `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` — is committed at C0, which
  is the R55.6 landing class the lesson itself claims to have fixed.

---

## 4. Verification performed

Every pointer above was resolved by a command whose output is in
`.ufo/waves/round-56/w2/T56W2RevStalePointers-receipts/`:

- `pointers-01-selftest-surface-gates.txt` — selftest counts at C0 and at the freeze; gate sha256 at
  three revisions; frozen-surface line count at two revisions; gate 0b/0c line numbers at two
  revisions; fixture scripts run verbatim and from a foreign cwd.
- `pointers-02-urls-anchors.txt` — S281 URL fetch, sha256, byte count, anchor lines 36/37/54/55, tag
  and main refs; S282 URL fetch, sha256, the claimed quote's absence, the actual `## Model` paragraph,
  and the path's last-change commit.
- `pointers-03-commands.txt` — QUALITY 107's command verbatim from `/tmp` and the same receipt at its
  own revision; knowledge §Re-derive steps 3 and 4; SKILL's invocation form; the registry cell's
  selftest command and expectation; the registry `source` line range.
- `pointers-04-lesson-census.txt` — every backticked lane path in the lesson checked against C0; the
  QUALITY 107 Lesson line and the lesson's actual R55.5 location; the scope-gap receipt's bytes and
  its commit status; census validate exit code and row counts at base and C0.

Census requirement: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tameshi` exits **0** (see §R21); the row count is 142, not 141 (F11).

No `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**` or `tools/**` file was edited, and nothing under
`.ufo/evidence/round-56/` was touched. Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W2RevStalePointers`.
No tooling was installed or upgraded for this seat; the only tools used were `git`, `curl`, `python3`,
`grep`/`awk`/`sed` and the lane's own `scripts/sources-census.sh`, all already present.

---

## 5. Summary

**43 pointers resolved: 32 ok, 11 stale.** Of the stale ones, 2 are failing commands (F5, and the
census-count expectation in F11), and the rest are pointers that resolve to a *different line, file or
value* than claimed (F1–F4, F6–F10) — none is a broken link to a missing file except F7's
wave-1 path and F9's wave-1-commit claim, which are the same landing gap seen twice.

The dominant pattern: **the amendment commit `21eb3c6` rewrote the gate, the counters, the surface
list, the control script and the deciding run after the round's prose was written, and the prose was
not re-pointed.** The knowledge entry, the lesson and QUALITY 107 each carry a small set of
pre-amendment pins — a selftest count, a gate sha, a surface size, two line ranges, a freeze
revision — that a reader at C0 will find contradicted by the tree. The registry cell was updated;
the other four places were not. F5, F7, F8 and F9 are independent of the amendment (a command that
needs an env var it never sets, a quote attributed to a receipt that does not contain it, a quote
that is not in the document it cites, and a commit claim the commit does not fulfil).

None of these is a false verdict about the round's *rule* — the rule (a receipt is evidence only for
the revision it names) is stated correctly, the gate enforces it as claimed, and QUALITY 107's
can-fail command behaves exactly as the criterion says. These are pointer-freshness defects in the
records that carry the rule, which is what this seat was asked to find. Per the wave-2 discipline no
`SKILL.md` edit is made here; the findings are for the L1 to adjudicate and to carry into round 57.
