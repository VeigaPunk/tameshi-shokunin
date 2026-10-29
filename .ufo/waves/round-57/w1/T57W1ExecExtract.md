# T57W1ExecExtract — round-57 defect-set extractor (wave 1)

Staged (nothing in the lane edited), under `.ufo/waves/round-57/w1/T57W1ExecExtract/stage/.ufo/evidence/round-57/c1/`:
`extract-defects.py`, `keys.json` (51 hand-curated entries, 2-5 keys each), `defects.json` (schema `tameshi-r57-defects-v1`).

## sha256 (receipts `T57W1ExecExtract-receipts/sha256.txt`)
- defects.json  `bef2293ba3db863b03247e9867b11aa2501aa54af0b098ce0f974817f485dee9`
- keys.json     `90a7b423a4237e94f5a9953a5a774b73ec199fb76041c55da99e76a0e9da8c07`
- extract-defects.py `424176c9c23301172f2fff8160dedd308ae79ceae81a4d8adb2bc97387f91dbe`
(defects.json regenerated twice from the same command: identical bytes.)

## Exact commands
```
python3 .../stage/.ufo/evidence/round-57/c1/extract-defects.py --selftest --work <EMPTY_DIR>        # SELFTEST PASS, 19 checks (receipts/selftest.stdout)
python3 .../stage/.ufo/evidence/round-57/c1/extract-defects.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 5e3569969b532310d2b8a3d130901757a3df356b --manual .../stage/.ufo/evidence/round-57/c1/keys.json > defects.json
```

## Count: 51 = r50 4, r51 8, r52 6, r53 9, r54 10, r55 7, r56 7 (matches expected; checked by eye against the seven files)

## DECISION the L1 must know: id rule deviation in round 51
The brief's rule ("else n is the item's 1-based position among the unlabelled items") collides in round 51: item 1 is labelled `**R51.1`, items 2-8 are unlabelled, so the literal reading gives the unlabelled item 2 the id `R51.1` again. The extractor uses the position among ALL items of the routed section(s) for an unlabelled item (R51.2..R51.8), which also agrees with the lane's own citations inside the items ("R51.2/R51.3" in item 2, "R51.4", "R51.5" in item 4) and is identical to the brief's rule for r50 (no labels) and r52-r56 (all labelled). A duplicate id that is not a fold exits 2. Scribes that applied the literal rule to R51 items 2-8 are off by one for those seven ids. (Messaged TameshiR57.)

## Other rule readings (documented in the script docstring)
- Scope: every `## ` section whose heading contains "rout" (case-insensitive): r54 has two (`:105`, `:231`), r56 `## 6. Verdict and routing`.
- Item = list line or non-indented bold-led paragraph; continues over following non-blank lines; blank line ends it. Preambles, `Operator note`, `For the operator`, `Ran in a temporary shell...`, r54 "R54.1–R54.9 as filed above..." are not items.
- `**R54.5 extended.**` (line 241-245) folds into R54.5: R54.5 keeps `line=116,end=116`, gains `extended: [[241,245]]`, `extended_text`; its keys are curated for both.
- Added fields vs round 50: `text_chars`, top-level `per_round`; `extended`/`extended_text` on R54.5 only. Round-50 fields kept: id, round, file, line, end, routed_at, file_sha256, text (600 chars), keys.
- `routed_at` = oldest `git log --diff-filter=A` commit of the file (receipts/routed_at.txt): r50 9962033f, r51 ef19d8e1, r52 c1d49d76, r53 2ef0a5ad, r54 650987a0 (the file's erratum section was written at the re-dispatch, so R54.10 shares the file's routed_at), r55 fa48c06c, r56 5e356996 (= lane base).
- R54.1 text (line 107-108) is cut at 600 chars in `text`; keys come from the full text only for the heuristic (here overridden by manual keys).

## Selftest
`--selftest [--work DIR]` (DIR must be empty or absent; no `/tmp` hardcode): parser cases (labelled with wrapped continuation, tail paragraph and later sections excluded, unlabelled positions incl. list `- `, mixed labelled/unlabelled positions, two routed headings with bold paragraphs, `extended` fold, closing remark excluded, foreign-round label rejected, collision rejected, keys_of) plus a fixture git repo (toplevel asserted, committed as `fixture`) checking count/per_round/routed_at-is-adding-commit/file_sha256 of the rev blob/manual-key override/unknown manual id rejected. Mutation not run by this seat.

## Keys
Hand-curated (not the `keys_of` heuristic, which gave `[]` for R52.2, R52.6, R55.3, R56.1, R56.7 and dumped whole quoted receipt lines for R54.1/R54.10). Keys are tokens a fixing excerpt in the tree would carry (ids, file names, hashes, numbers, code names), not quotes that exist only in the spot-check. Guesses about future fix text (e.g. `19/19`, `ten-leg`, `Landed changes`) are `[INFERENCE]`; a reviewer should widen those if a fixing excerpt misses them. The 15 scribes' per-id keys are for the L1 to merge.

## Risks
- Keys are checked case-insensitively as substrings of the excerpt or path suffix; entries like `rekey`-style short words (`re-key`, `coldread`, `bootstrap`) are the weakest discriminators.
- R54.5/R54.9 and R54.3/R54.10 share vocabulary (counts, paths); only the id-specific keys separate them.

## Tooling
No tool installed. Scratch `/fast/scratch/hyaku/tameshi-r57/T57W1ExecExtract` (selftest fixtures cleaned by the script).

## First five words of every item (id, line span; receipts/first5.txt)
- R50.1 L98-98 S022 status contradicts its used-by
- R50.2 L99-99 Gate/probe registry gap. `tools/shrink-case.py` (round
- R50.3 L100-100 Frontier table stale. `corpus/README.md:83` (F6)
- R50.4 L101-101 Carried (lane-acknowledged): the seven open
- R51.1 L126-126 R51.1, registry gate made unsatisfiable.
- R51.2 L127-127 Stale SKILL statements. Correct SKILL.md
- R51.3 L128-128 Cold-read re-key overstates. `coldread/refresh.py:224-227` writes
- R51.4 L129-129 C3 counter / round21-measure. Either
- R51.5 L130-130 Cross-domain routing owed to kagi.
- R51.6 L131-131 `## Gate` completeness. List rejected
- R51.7 L132-132 Ledger cell. `corpus/knowledge/fleet-kill-rate-ledger.md:119` still reads
- R51.8 L133-133 Freeze-stamped control receipts (lane mistake
- R52.1 L83-83 R52.1 coldread re-key debt. 19
- R52.2 L84-84 R52.2 LOG.md round-52 entry missing.
- R52.3 L85-85 R52.3 over-count review overstated (this
- R52.4 L86-86 R52.4 uncommitted round work. 4
- R52.5 L87-87 R52.5 hard-coded `/tmp` in `tools/registry-check.py:766`
- R52.6 L88-88 R52.6 report-contract repairs. Add per-box
- R53.1 L78-78 R53.1 — frozen C1 counter
- R53.2 L79-79 R53.2 — deciding receipts never
- R53.3 L80-80 R53.3 — phase-B break-one controls
- R53.4 L81-81 R53.4 — committed C2 receipt
- R53.5 L82-82 R53.5 — stale freeze receipts/pointers.
- R53.6 L83-83 R53.6 — CR47 exit-class mapping
- R53.7 L84-84 R53.7 — "inputs pinned at
- R53.8 L85-85 R53.8 — S275 locator. anchor
- R53.9 L86-86 R53.9 — uncommitted round work
- R54.1 L107-108 R54.1 — false positive-control claim
- R54.2 L110-110 R54.2 — three different freeze
- R54.3 L112-112 R54.3 — `SCORECARD.md:2584` quotes `total=14`
- R54.4 L114-114 R54.4 — stale c2 digest
- R54.5 L116-116 R54.5 — finding counts do
- R54.6 L118-118 R54.6 — uncommitted round work
- R54.7 L120-120 R54.7 — forged-file disposition is
- R54.8 L122-122 R54.8 — config-write incident record
- R54.9 L124-124 R54.9 — wave-table numbers. `w1-registry.json`
- R54.10 L233-239 R54.10 — the phase-A control
- R55.1 L118-122 R55.1 — no C2 verdict
- R55.2 L123-126 R55.2 — a quoted total
- R55.3 L127-130 R55.3 — the calibration instrument
- R55.4 L131-133 R55.4 — a stale control
- R55.5 L134-137 R55.5 — the deciding gate
- R55.6 L138-142 R55.6 — uncommitted round work
- R55.7 L143-147 R55.7 — closure-environment contamination (not
- R56.1 L130-130 R56.1 Replace SKILL page-local line
- R56.2 L131-131 R56.2 Fix the `## Standing
- R56.3 L132-132 R56.3 Replace the `14/14` `recheck:`
- R56.4 L133-133 R56.4 The 13 of 18
- R56.5 L134-134 R56.5 Pre-register the two controls
- R56.6 L135-135 R56.6 Registry: add a `gate`-kind
- R56.7 L136-136 R56.7 Correct the "no byte
