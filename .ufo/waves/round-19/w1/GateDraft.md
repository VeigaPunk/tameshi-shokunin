# GateDraft — round-19 C1 Gate admit/reject for the five routed round-18 corrections

Seat: TameshiR19-2.GateDraft (leaf, read-only). Scope: C1 calibration only, five
routed defects from `corpus/lessons/round-18-verifier-spotcheck.md` §5. No production
file was edited. No lane selftest, build, lint, test, formatter, or `measure.py --check`
was run. No tool was installed or updated. Only read commands and one `/tmp` diff file
(created and removed) were used.

Repo HEAD observed: `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` (round-19 correction
commit `21e7932`). Frozen contract `78b99dd`, baseline `7243e7f`. Historical
verifier-cited tip `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, pre-round-19 base
`183f87b899e6cae46be98d251cbc87fb5118f6ca`.

Epistemic labels: **O** = observed by a command in this seat; **R** = read from a
committed receipt (not re-run); **I** = inference.

## Proposed Gate rows (admit / reject)

| Candidate | Decision | Grounded reason and evidence |
|---|---|---|
| **R18-1** `guard-kill-closure.md` line 2 `verified-at` / `Landed-tip results: PENDING` | **admit** | O: erratum `## Erratum R18-1` at `corpus/knowledge/guard-kill-closure.md:171`, +21/−0 vs `4b7c682`. It names line 2 explicitly and supersedes the PENDING statements. Effective revision `921ef80…` (commit exists, `git cat-file -e` ok). R: `final/checks.json` `probes` row, argv `defect-probes.py --rev 921ef80…`, exit 0, `stdout_sha256 d37c99e3…4eb8cf0`; `sha256sum final/probes.stdout` = `d37c99e3…` (match). Header line 2 is still literally PENDING; the routed defect permitted an appended correction naming that line, so the header is not edited. No fresh tip result is invented. |
| **R18-2** `mutation-case-kumitate-sources-check.md` line 1 `queued` S008 | **admit** | O: `## Erratum R18-2` at `…sources-check.md:266`, appended, names line 1. At `4b7c682`, `corpus/SOURCES.md` row S008: status field `mined` (tier A), used-by `corpus/knowledge/mutation-case-kumitate-sources-check.md`. Line 1 of the entry still reads `queued` (count = 1); the erratum supersedes it. Original bytes retained (+12/−0 in landing diff). |
| **R18-3** `round-18.md:79` "deletions = the four allowed used-by cells only" | **admit** | O: `git diff --numstat 183f87b 4b7c682 -- corpus/SOURCES.md` → `25 5`. `git diff -U0` deleted rows: S001, S008, S052, S056, S057 (5 IDs, 0 non-row deletions). Paired comparison (python, read-only): S001/S052/S056/S057 differ at used-by field only; S008 differs at status and used-by. This matches `## Erratum R18-3` (`corpus/lessons/round-18.md:121`) exactly. Line 79 is retained, not edited (base line 79 identical to current). **Nuance for prose:** the base→HEAD range (`7243e7f`…`21e7932`) also shows one SOURCES deletion (S049 row, round-19 `used-by` change, `9 insertions/1 deletion`). That is outside the R18-3 falsifier range, but any tip-stated falsifier must exempt it. |
| **R18-4** `final/checks.json` `bash-witness-selftest` (failed `--selftest`, exit 64) as effective selftest receipt | **admit** | O: current `checks.json` row = argv `tools/bash-witness-study.py --selftest`, exit 64, stdout sha of empty (`e3b0c442…`). Byte-retained: `sha256sum` = `fed3c8e6…` = `before.json` input digest; identical at `4b7c682`. Replacement `.ufo/evidence/round-19/bash-witness-selftest-complete.json`: argv `python3 tools/bash-witness-study.py selftest`, exit 0, `revision 4b7c682…`, `tool_sha256 8dfaa25a…` = `git show 4b7c682:tools/bash-witness-study.py \| sha256sum` (match), `runner_sha256 d22c4025…` = `git show 4b7c682:tools/mutate-and-run.sh \| sha256sum` (match), stdout sha `316b9713…` = `sha256sum` of `…complete.stdout` (match), stderr empty (`e3b0c442…`, match). Stdout contains `WITNESS_SELFTEST: 43/43 pass` and `VERDICT: PASS`. Failed round-19 scratch receipt `bash-witness-selftest.json` exit 1 (`FileNotFoundError …tools/mutate-and-run.sh`) is retained and explicitly superseded. |
| **R18-5** missing committed 60/60 receipt at `4b7c682` | **admit, with precise wording** | O: `.ufo/evidence/round-19/round18-final-measure.json` argv `…measure.py --repo … --rev 4b7c6823… --explain`, exit 0, `stdout_sha256 55c530bb…` = `sha256sum` of stdout (match). Stdout fields: `sections_covered 60`, `sections_total 60`, `calibration_restraint_score 8`, `overrides_used false`. `round-18/measure.py` blob at `4b7c682` sha `7ca87a7c…` = working-tree copy (match). **Correction to the verifier's ground:** `final/measure-final-60.json` was first committed in `4b7c682` (commit `4b7c682` +1978 lines); its `revision` and `rev_input` fields are `a85f7107…`. So the receipt existed in the `4b7c682` tree but **names `a85f710`**, not `4b7c682`. The routed defect (no receipt naming the cited revision) still holds; the Gate prose should say that, not "absent from `4b7c682`". The round-19 replay is a new measured receipt at `4b7c682`, not a backdated one (erratum says so). |

## Rejects (agree with round-19.md draft; one addition)

| Candidate | Decision | Reason |
|---|---|---|
| Reclassify historical failed invocations as passing, or overwrite `checks.json` | reject | O: `checks.json` sha unchanged (`fed3c8e6…`); history is what the supersession rests on. |
| Claim current round-19 full-page / required-command coverage | reject | No fresh cold-read was run; receipts are revision-bound to `4b7c682`/`a85f710`. |
| Close the 18 earlier guard survivors through metadata repair | reject | The five corrections exercise none of the survivors; the routed defects are metadata/receipt only. |
| First round-19 witness scratch run as successful evidence | reject | O: `bash-witness-selftest.json` exit 1; retained and superseded. |
| **Add:** rewrite the fleet round-18 report or round-18 lesson line 79 in place | reject | Append-only: errata cover it. Landing diff for `round-18.md`, `guard-kill-closure.md`, `mutation-case…md`, `checks.json` is additive only (0 deleted lines each, O). |

## Measured counts (O, commands in this seat)

- Corrections present at `HEAD` (`21e7932`): `Erratum R18-1`/`R18-2` headers 1 each in their files; `Erratum R18-3` and `Errata R18-4 / R18-5` headers 2 in `round-18.md`. All five present.
- Corrections-related deletions in landing diff `7243e7f..HEAD`: `guard-kill-closure.md` 21/0; `mutation-case…md` 12/0; `round-18.md` 36/0; `checks.json` unchanged (byte digest matches `before.json`). `SOURCES.md` 9/1 (one deletion = S049 used-by line, round-19 change).
- `PENDING` tokens in `guard-kill-closure.md` at `4b7c682`: 13 (lines 2,10,53,65,91,97,114,118,120,122,132,136,143). R18-1 erratum enumerates 2,10,53,65,91,97,114,118,120,122,132,134,136. Line 134 (`Not run: no after-landing probe run…`) is stale without the literal token; line 143 (`EG-1 measured, no longer PENDING`) is not stale and is correctly unlisted. The erratum's list is semantic, not literal; prose should say so rather than "every PENDING token".
- Current working-tree `PENDING` count: 15 (13 + two inside the R18-1 erratum text).

## Proposed prose for the Gate table (replacing the five admit rows in `corpus/lessons/round-19.md`)

Use the table above. Additional sentence for the `Gate` paragraph: "R18-5 receipt
`final/measure-final-60.json` was already in the `4b7c682` tree but names `a85f710`;
the round-19 replay supplies a receipt at `4b7c682`, and the round-18 verifier's
'committed at a85f710' location statement is corrected here (path first committed in
`4b7c682`)."

## Not done / limits

- Did not re-run `measure.py`, `checks.json` argv, or any witness/selftest. All receipt
  results are read from committed files and digest-checked; they are advisory, not an
  independent closure.
- Did not re-open external sources (S049 etc.); this seat's scope is the five defects.
- The round-19 lesson's `## Gate` claim "round18-final-measure.json records a real replay"
  is supported only by receipt metadata and digest match; not re-executed.
- Floating: round-19.md `## Gate` lists "S049 status mined→mined" recheck `on-release` —
  not verified in this seat (outside the five defects).
