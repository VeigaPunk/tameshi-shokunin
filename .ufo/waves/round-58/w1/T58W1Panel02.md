# T58W1Panel02 — blind calibration panel

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.
Axes: calibration accuracy, evidence completeness, blindness preservation. No lane content changes proposed or staged. Recommendations only.

## Method and commands

Created `/fast/scratch/hyaku/tameshi-r58/T58W1Panel02/clone` with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r58/T58W1Panel02/clone`; checked its `rev-parse --show-toplevel` against that absolute clone path before `git -C <clone> checkout --detach 2a32aa8228d5f86a85c81a923a3148bf792a9538`. Output: `HEAD is now at 2a32aa82 round-57 verifier spot-check (integrator, hyaku): non-author admit/reject`.

All evidence below is from this detached tree unless explicitly identified as the externally stored canonical report. Read only assigned records from the working-tree round-58 defects document. No forbidden panel, candidate, round-57 wave artifact, or other round-58 seat artifact was opened. An incidental corpus search encountered only permitted baseline ledger content.

`read xd://lsp` returned `No such tool: xd://lsp`; semantic references/definition/diagnostics were unavailable. Literal grep is evidence discovery, not semantic proof. Receipts contain exact tool arguments and outputs; paths inside those arguments are absolute. Receipt directory: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel02-receipts/`.

## Findings, by severity

### Open — R51.4: required mutation attack remains unsupported

The declaration portion is repaired: `read <clone>/.ufo/evidence/round-52/contract.json:18-28` returns a pre-registered fleet-bound fix, including `the fix declares the round21-measure self-test fleet-bound`. `read <clone>/SKILL.md:2200` returns `fleet-bound, not hermetic (since round 52...)`.

However the frozen item explicitly also requires the missing round-51 C3 mutation attack. Literal sweep command (specialized grep): pattern `T51W2MutC3Counter|round-51/c3/measure.py|C3 counter.*mutation|mutation attack.*C3`, paths `<clone>/corpus/lessons/round-5[1-6]*.md;<clone>/SCORECARD.md:2448-2630;<clone>/.ufo/waves/round-5[2-6]/**/T*MutC3*.md`.

Output includes `corpus/lessons/round-51.md:65`: `the C3 counter's mutation attack is the one item left unrun`, `:98`: `never ran`, and `SCORECARD.md:2487`: `Re-run the C3 counter's mutation attack (R51.5).` No completion receipt appeared in that sweep. This is not a claim that every possible differently named artifact was searched; absent affirmative execution evidence, the compound item cannot be fixed. No reasoned decline located. Receipts: `c3-sweep.txt`, `preregistration.txt`, `skill.txt`.

### Open — R51.5: draft is not the promised next report item

`read <clone>/.ufo/waves/round-52/w1/T52W1ScribeKagiRoute.md:1-9` returns an excellent explicit draft: `Domain: kagi-shokunin`, the unanchored `grep -q "$3"`, pinned lines 400/403/158, and routing ownership. It was committed as seat evidence, not integrated report content.

`read <clone>/LOG.md:2444-2463` identifies the canonical next report as `.ufo/reports/round-52/tameshi.md` in the fleet (`53fdd555`). Opened the discovered absolute path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/tameshi.md:1-36`: output contains status, claims, work performed, sources/frontier, trend verdicts and SHONEN, but no kagi/cross-domain finding. This external report is corroboration, not a lane-tree edit or resolving lane commit.

Literal grep of the next scorecard and lesson report surfaces returned only lesson line 15 rejecting the draft's suggested `grep -qxF` fix. That rejection does not route the gate defect to kagi in the report. No reasoned decline of routing located. Receipts: `routing-draft.txt`, `routing-sweep.txt`, `scorecard52.txt`, `report-reference.txt`, `canonical-report52.txt`.

### Open — R51.6: historical Gate omission persists

`read <clone>/corpus/lessons/round-51.md:5-14` returns opened S272/S273 followed by `Rows touched`, then `## C1`; no rejected candidates or reasons appear under Gate.

Command `git -C <clone> log --format='%H %s' ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4..2a32aa8228d5f86a85c81a923a3148bf792a9538 -- corpus/lessons/round-51.md` returned no output: no subsequent edit repaired that lesson.

Counterevidence considered: `read <clone>/corpus/lessons/round-52.md:5-17` returns `Candidates rejected:` with three reasoned rejects. This improves the successor lesson, but does not correct the particular round lesson whose omitted rejects the assigned item describes. No recorded reasoned decline of the historical repair located. Receipts: `gate51.txt`, `gate52.txt`, `history.txt`.

## Resolved items

### Fixed — R51.2

Content repair introduced by `bcba8924894216268afc4171f06eb8c28e912b46`; completing fresh-reader re-key identified at `7fa9a5e0104bc181872401547987d6744f3b570d`, the verdict's resolving commit for the compound requirement.

Command `git -C <clone> show --format= --no-ext-diff bcba8924894216268afc4171f06eb8c28e912b46 -- SKILL.md` shows original replacements:
- `nine ledger legs` → `ten ledger legs`, and 9/9 → 10/10;
- runner pointer 425 → 434 and 569-574 → 579-583;
- default regression scratch `/tmp/...` → `${TMPDIR:-/tmp}/...`;
- runner registry write scope gains TMPDIR.

At base, `read <clone>/SKILL.md:202,239,966-970,2179,2192` still locates those corrections. `read <clone>/.ufo/evidence/round-21/coldread/ledger.json` with the receipt's jq selection returns three fresh T54 records for recipe, Using the ledger and Round-26, each `wrong_expectations: 0`, `read_rev: 99c3bc88d704566197783f66b211ee0a830e0330`, with T54W2Read02/05/23 and trace paths. `git -C <clone> log --format='%H %s' -- .ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/traces/section-17.json` returned `7fa9a5e0104bc181872401547987d6744f3b570d round-54: re-key of all 23 headings...`.

`git -C <clone> merge-base --is-ancestor <commit> 2a32aa8228d5f86a85c81a923a3148bf792a9538` succeeded for both full hashes in the recorded command chain. Receipts: `history.txt`, `skill.txt`, `fresh-rekey.txt`.

### Fixed — R51.3

Resolving commit: `bcba8924894216268afc4171f06eb8c28e912b46` (ancestor check above).

Command: specialized `read <clone>/.ufo/evidence/round-21/coldread/ledger.json?q=.corrections[] | select(.reader == "T51W2Read20")`. Output:
- `reader: T51W2Read20`, heading `### Round-26 gate/probe registry — report interop`;
- `wrong_expectations: 7`, seven quoted findings including HIGH-1, HIGH-2, MED-1;
- `corrects: ledger entry ... wrong_expectations 0 was written from code (round-51 refresh.py:227)`;
- `routed_by: corpus/lessons/round-51-verifier-spotcheck.md routed defect 3`.

The item permits an appended named correction, so preserving the historical zero does not leave this defect open. No assertion that every other correction's semantics are correct is needed or made. Commit stat locates 606 ledger-line additions/changes introducing the correction records. Receipts: `correction.txt`, `history.txt`.

## Residual risk and verification gaps

No runtime selftest, deciding counter, admission, integration or shipping action was performed. This is document/tree status adjudication. Open judgments R51.4/R51.5 rely on explicitly bounded evidence sweeps plus affirmative omission/unrun evidence, not exhaustive proof of absence. R51.6 is interpreted as repair of the identified historical round-51 Gate section rather than only improved future process. No statuses copied from prior panels or another seat.

Self-review: accuracy 4/5 (bounded absence evidence explicitly qualified); completeness 4/5 (all five items and compound clauses examined, no exhaustive differently named artifact sweep); clarity 4/5 (receipt paths provide detailed reproducibility, at cost of length); actionability 5/5 (one exact machine verdict per assigned ID, resolving hashes and outstanding clauses identified); conciseness 4/5 (command detail retained for audit). Overall 4.2/5. Highest-impact improvement would be an affirmative completion receipt for the missing mutation attack; without one it cannot be marked fixed.

Tools installed/updated: none. Scratch `/fast/scratch/hyaku/tameshi-r58/T58W1Panel02` was deleted before delivery; cleanup command returned `scratch removed` (`cleanup.txt`). No prior-round evidence or lane tracked content was modified.
