seat: T46CritEntryUndetected

item: Overreach attack on `corpus/knowledge/r5-undetected-flaky-failures.md` (attacked at content rev `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`) — one BLOCKING bar-2/bar-3 defect in the "Observation" section, a status-word contradiction against the frontier table, an inherited "exactly" identity claim, and a criterion-51 header defect shared by all three round-46 entries.

Scratch: `/tmp/tameshi-r46-T46CritEntryUndetected/` (`extract.txt` = the snapshot extraction). Read-only on the lane; no counter was run as a verdict; no `--selftest` was run by this seat.

## Target pin

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6f2168e028ce7ff6e82ac92093ac05dd1f147c32:corpus/knowledge/r5-undetected-flaky-failures.md | sha256sum
sha256sum corpus/knowledge/r5-undetected-flaky-failures.md
```
→ `00ec1760c8fba06d59f4fd21bb03e3c13bcf65c2837e54d3c95cd308dcc741cf` for both lines: the committed entry and the checkout file are the same bytes, so every line number below is the committed line number.

Snapshot pin: `sha256sum .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html` → `5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f` (matches line 1's prefix `5eb59adf…`).

Extraction used for every quote check: `python3 .ufo/evidence/round-45/freshness/measure.py --extract .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html` → exit 0, `1668` words / `12011` bytes.

## F1 — BLOCKING: line 36 states an inference as "Observation", and the snapshot does not carry it (bar 2 and bar 3)

Attacked: line 36, `## The mechanism, in the source's own terms`:

> Observation, from quotes 2–4: the projects' own detector is a rerun of the failed test **within the same job** (2); …

Evidence that quote 2 does not support the attribution:

```
grep -oF 'Modern CI systems commonly rerun failed tests within the same job to identify flaky failures' /tmp/tameshi-r46-T46CritEntryUndetected/extract.txt | wc -l
→ 4
grep -oE '[^.]*projects[^.]*\.' /tmp/tameshi-r46-T46CritEntryUndetected/extract.txt | sort | uniq -c
→ 4 8 billion test executions from four industry-scale projects over two-month periods.
→ 3  All apparently deterministic failures were systematically validated through reruns in fresh environments within the projects' original CI infrastructure to identify undetected flaky failures.
→ 1  All apparently deterministic failures were systematically validated through reruns in fresh environments within the projects{\textquoteright} original CI infrastructure to identify undetected flaky failures.
→ 4  We found that, across all projects, undetected flaky failures account for 9.
```

The only sentences in the snapshot that mention the studied projects are the 8.8-billion sentence and quote 4 (and quote 5's "across all projects"). Quote 2 is a statement about "Modern CI systems commonly", and quote 3 is about "Existing research". Nothing in the snapshot states that the four studied projects' own detector is a same-job rerun; that is an inference from "commonly" plus "apparently deterministic". Presenting it under the word `Observation` violates the admission bar items 2 and 3 (`corpus/QUALITY.md:4-6`: "Every claim carries a source: a measured anchor (path:line, command, evidence id) — never oral knowledge" / "Observation, inference, and unknown stay separate").

It is **new in this entry**, not inherited: the package copy it replaces states the same fact at the level the source supports — `sed -n '28,29p' .ufo/evidence/round-46/assimilation/package/r5-undetected-flaky-failures.md` → "**A rerun-based verdict has a known blind spot.** Modern CI reruns a failed test *in the same job* to decide whether it is flaky". The scribe escalated "Modern CI" to "the projects' own detector".

Scope of the block: the entry's admission, not the C3 count. The C3 predicate does not read content separation — `entry_ok` checks only provenance trio, cited row, `used-by`, and one located+fresh quote (`.ufo/evidence/round-46/coverage/measure.py:124-151`), so the entry still grades `ok` with this sentence in it:

```
python3 - (in-process import of the frozen counter, rows read at rev 6f2168e, no --rev verdict run)
→ rows: ['S258', 'S259', 'S260']
→ entry_ok: (True, 'ok', ['S259'])
```

Smallest safe correction: relabel line 36's first clause as inference ("Inference: if the projects' detector is the same-job rerun that quote 2 names as common, …") or drop the attribution and keep the quote's own subject ("modern CI systems commonly …").

Two smaller members of the same sentence, same section, same defect class (LOW):
- "the authors classified failures by rerunning **in fresh environments**" — the abstract's verb is "validated": `grep -oF 'All apparently deterministic failures were systematically validated through reruns in fresh environments' <extract> | wc -l` → `4`. "classified" is a stronger operation than "validated".
- "they state the class that the first mechanism misses is not small (5)" — "not small" is the entry's evaluation of `9.8 %–16.3 %`; the snapshot states the range, not the evaluation.

## F2 — HIGH: line 44 calls F3's ground `held`; the frontier table prints `open` and the lane defines `held` otherwise

Attacked: line 44 first clause — "F3's **held** ground is a repeated-control precondition with a finite sample".

```
sed -n '80p' corpus/README.md | grep -o 'open'
→ open
sed -n '120,121p' corpus/README.md
→ A ground reads `held` only when its next move in the table is
→ measured.
sed -n '577p' corpus/README.md | cut -c1-200
→ Frontier F3 (determinism precondition, flaky-aware verdicts) gains three published measurements about how flakiness hides from a rerun; F3 stays `open` — these entries state what the literature meas
```

The lane's status word is defined at `corpus/README.md:120-121`, the F3 row at `:80` carries `open`, and the round's own README block at `:577` says F3 stays `open`. The entry is the only record in the round that calls the ground `held`. Either reading of "held ground" (the theme's held portion, or the frontier status) collides with one of those three lines.

Sub-finding F2b — HIGH, adjacency: line 47 announces that "F3's next move stops being only \"N ≥ 3 byte-identical controls\" and becomes \"N ≥ 3 controls that agree while the environment tuple varies\"", but the plan anchor `corpus/README.md:80` still prints the old move verbatim (`one control per sweep (…) → N ≥ 3 byte-identical controls, or a named mismatch`) and the round-46 block does not record the change. `PROVINCE.md:40-42` designates "F1–F10 in `corpus/README.md` `## Frontier`" as the frontier surface, so a changed next move with no carrier there is a plan claim the lane's own table contradicts.

Smallest safe correction: change line 44's `held` to `open`, and either update `corpus/README.md:80`'s next-move cell in the same landing or mark line 47's proposal as a proposal that the table has not adopted.

## F3 — HIGH: line 54's "exactly the protocol quote 4 describes" is an identity claim the snapshot does not make (inherited from the package and not corrected)

Attacked: line 54 — "`tools/env-diff.py` … is the instrument that can vary the environment tuple across a repeated control, **which is exactly the protocol quote 4 describes**".

Quote 4 (line 24, 3 occurrences, verified) describes: "All apparently deterministic failures were systematically validated through reruns in fresh environments within the projects' original CI infrastructure". That is (a) a rerun in a *replacement* environment, (b) applied to failures already judged apparently deterministic, i.e. conditional on a failure. The lane instrument varies one declared input across profiles:

```
sed -n '2p;3p' corpus/knowledge/hermetic-env-differential.md
→ verified-at: 2026-10-21; nine pinned surfaces executed under seven profiles, clean controls exit0; raw tuple classifications below. This is a finite experiment, not a universal hermeticity certificate.
→ recheck: python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/tameshi-f5-recheck.json; python3 tools/env-diff.py --selftest. Reopen S079, S028 and S081; compare the located quotes in lessons/round-21.md.
```

One-input variation across profiles is not a fresh-environment replacement, and an unconditional repeated control is not a rerun conditioned on failure. The word `exactly` converts a family resemblance into an identity.

This is an inherited overreach that the entry's own correction section does not list: package `:40-41` says "The lane's F5 profile machinery is **exactly** the tool for that". Lines 56-62 claim to correct four package overstatements; this fifth one is carried unchanged into the admitted entry. That is a coverage gap in the correction section, not only a wording defect.

Smallest safe correction: replace "which is exactly the protocol quote 4 describes" with the two named differences ("a replacement environment rather than one varied input; applied to an apparently deterministic failure rather than to a green control"), and add the package line to the corrections list.

## F4 — HIGH: line 2 fails QUALITY criterion 51, and all three round-46 entries share the defect

Attacked: line 2, `verified-at: 2026-10-25`.

`sed -n '560,570p' corpus/QUALITY.md` (criterion 51) requires the `verified-at` line to name "the sha256 of the tool bytes it vouches for, the lane revision of the run, and a committed receipt of that run". Line 2 names a date and nothing else; line 3 names the tool *path* (`.ufo/evidence/round-45/freshness/measure.py`) and two live-fetch digests, but no tool sha256, no lane revision, and no receipt. No committed receipt carries either fetch digest:

```
grep -rl 'b3051e44\|b0619632' .ufo/evidence/round-46/
→ (no output)
```

A compliant sibling shows the shape criterion 51 wants: `sed -n '2p' corpus/knowledge/mte-report-interop.md` → "verified-at: 2026-10-22 (refreshed round 26); tool sha256 193ea6e3… at lane a08e85c5… (nine ledger legs): `--check` PASS 9/9, exit 0 (`.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`) …".

Systemic, not this seat's alone:

```
for f in r5-undetected-flaky-failures r6-flaky-failures-cluster r9-false-red-rate; do sed -n '2p' corpus/knowledge/$f.md; done
→ verified-at: 2026-10-25
→ verified-at: 2026-10-25
→ verified-at: 2026-10-25
```

`grep -c 'criterion 51\|Criterion 51' corpus/QUALITY.md` → `0`: no amendment or errata qualifies criterion 51. Wave-1's own report (`.ufo/waves/round-46/w1/ScribeEntryUndetected.md`, "QUALITY 51 tension") recorded that the frozen item fixed line 2 to the bare date; the conflict is therefore contract-level and this finding routes to the reviewer/integrator: either extend line 2 (tool sha256 + lane revision + committed receipt) or record an errata naming the frozen header as the cause.

## F5 — LOW: line 62's justification "the page carries no other [figure]" is false

Attacked: line 62 — "No figure beyond 8.8 billion executions, 9.8 %–16.3 % of failed pipeline runs, up to 3× environment variation, 154,000 flaky test cases, 1.7 million flaky failures, four projects and two-month periods is claimed here, **because the page carries no other**."

```
grep -oE '(Earth and Planetary Sciences|Computer Science|Keyphrases) [0-9]+%' /tmp/tameshi-r46-T46CritEntryUndetected/extract.txt | sort | uniq -c
→ 1 Computer Science 100%
→ 1 Computer Science 20%
→ 1 Computer Science 40%
→ 2 Earth and Planetary Sciences 100%
→ 3 Keyphrases 25%
```

The page carries a Pure "Fingerprint" block with eight weighted concepts (100 % ×3, 40 %, 25 % ×3, 20 %). They are derived topic weights, not paper measurements, so the entry is right not to claim them — but "the page carries no other" is false as written. Smallest correction: "the page carries no other measurement; its remaining numbers are the portal's derived Fingerprint weights (100 %, 40 %, 25 %, 20 %), which this entry does not use".

## F6 — LOW: line 10's "nothing else about the paper's content" excludes a section the page carries

Attacked: line 10 — "It carries the abstract, the DOI, the citation block and the bibliographic details, and nothing else about the paper's content."

The page also carries the Fingerprint block (`grep -oE 'Fingerprint Dive into the research topics of' <extract> | wc -l` → `1`), the research-output type marker ("Contribution to journal › Article › peer-review"), and two abstract sentences the entry never quotes, one of which is substantive: "These findings reveal fundamental limitations in current detection strategies and highlight the need for comprehensive approaches to flaky test management" (`grep -oF 'These findings reveal fundamental limitations in current detection strategies' <extract> | wc -l` → `4`). The last is abstract content the entry does not use; the sentence at line 10 says the page carries nothing else. Smallest correction: "and the portal's derived Fingerprint block; no method section, no per-project numbers."

## F7 — LOW: line 47's "the source's own flaky verdicts were produced by reruns in fresh environments" overbroadens to the detected class

Attacked: line 47. The abstract's detected-flaky verdicts come from the *other* mechanism — quote 2, "Modern CI systems commonly rerun failed tests within the same job to identify flaky failures" (4 occurrences). Only the *undetected* class was produced by the fresh-environment reruns (quote 4). The sentence's own continuation ("the failures those reruns identified as undetected flaky failures") carries the restriction, so the defect is the opening noun phrase. Smallest correction: "the source's undetected-flaky verdicts were produced by reruns in fresh environments (4)".

## F8 — LOW: line 54's anchor `corpus/knowledge/hermetic-env-differential.md:6` names the heading, not the forms it is cited for (QUALITY 2)

```
sed -n '3p;6p' corpus/knowledge/hermetic-env-differential.md | cut -c1-90
→ recheck: python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/tamesh
→ # Hermetic environment differential — vary one input, keep the repeat control
```

Line 54 cites `:6` for "the contract and `--selftest` forms"; those forms are on line 3. Smallest correction: cite `:3`.

## F9 — LOW: line 53's range `corpus/knowledge/hermetic-env-differential.md:1-6` includes a blank line and the following heading (QUALITY 70)

Attacked: line 53. The range's content ("nine pinned surfaces … seven profiles … clean controls exit0") is line 2, and the command is line 3; lines 5 and 6 are blank and the `#` heading.

```
sed -n '5,6p' corpus/knowledge/hermetic-env-differential.md | awk '{print (NR==1?"line5:":"line6:") ($0==""?"<blank>":"heading:" substr($0,1,40))}'
→ line5:<blank>
→ line6:heading:# Hermetic environment differential — va
```

Criterion 70 (`corpus/QUALITY.md:793-799`): "A line-range citation to a paragraph names all and only the lines containing that paragraph; it excludes adjacent blank lines and a following heading." Smallest correction: cite `:2-3`.

## F10 — LOW: line 12 silently normalizes the snapshot's German "und" to "and" while labelling the source "visible text"

```
grep -o 'Chair of Software [a-z]* Systems Engineering' .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | sort | uniq -c
→ 2 Chair of Software und Systems Engineering
```

Line 12 prints "Chair of Software and Systems Engineering" and annotates "(snapshot §header, visible text)". The affiliation is a located markup fact; the transcription changes one word. Smallest correction: keep `und` or mark the bracket as a translation.

## F11 — LOW: line 67's universal self-claim is false on the entry's own lines

Attacked: line 67 — "Every statement above is either a located quote, a located markup fact, a lane file line, or explicitly labelled `Inference:`."

Counterexamples inside the entry: line 19 (occurrence counts over the extractor — a measurement of the snapshot's structure, none of the four categories), line 32 (the dash-form analysis and its `grep` counts — same), line 53's headline "Environment is a first-class flake input" (an evaluation; quote 9 states variation, not primacy), and line 36's first clause (F1 above). Smallest correction: add a fifth category, "a measured count over the snapshot's own extraction", and label the line 53 headline as the entry's reading.

## F12 — INFO: line 53 relabels the source's unit

"the source's *real suites* vary up to 3× between environments" — quote 9's unit is "flake rates between them", i.e. between test environments, over four industry-scale projects. "real suites" is the lane's own vocabulary (F5's surfaces are gates), imported as the source's. The following Inference sentence is correctly labelled, so this is a wording note, not a defect.

## F13 — INFO: line 48's "blind to its own worst class" drops the source's hedge

Quote 8: "the most disruptive test cases with undetected flaky failures remain largely invisible to tools relying on current detection mechanisms". The entry writes "blind", the source writes "largely invisible". The sentence carries `Inference:`, so the bar is met; the paraphrase is stronger than the quote.

## Checks that passed (attacked and found clean)

- **Prescriptive sentences are labelled.** `grep -nE '\b(must|should|needs to|becomes|stops being|is the concrete|requires|ought)\b' corpus/knowledge/r5-undetected-flaky-failures.md` → lines 47, 53, 54 only; each of the three carries an explicit `Inference:`. The item's label test passes for every "the lane must/should" sentence.
- **Located quotes and their counts are honest (QUALITY 87, 79).** All ten labels match the counter's own `fold()`+split, measured in-process against the frozen counter:
  `q1 19→19, q2 15→15, q3 19→19, q4 18→18, q5 18→18, q6 14→14, q7 9→9, q8 19→19, q9 16→16, q10 18→18` — ten of ten OK; the inline Boundary quote measures 13 tokens (unlabelled, inside the 6–25 bar). Occurrence counts also hold: `grep -oF <quote> <extract> | wc -l` → `4,4,4,3,3,4,4,4,3,4` for quotes 1-10, matching the entry's stated 4×/3× split. The four abstract copies are real: `We analyzed 8.8 billion` occurs 4× in the raw snapshot at offsets 17922 (visible), 36429 (`@article` BibTeX), 41675 (RIS `N2  -`), 43416 (RIS `AB  -`) — line 19's structure claim verified.
- **Lane file lines cited are correct.** `sed -n '80p'` / `'82p'` / `'127p'` of `corpus/README.md` carry the F3 row, the F5 row, and the `repeated-control-precondition.md` scope the entry quotes verbatim; `tools/repeat-control.py:18` carries "the environment is inherited unchanged" and `:94` carries "it is not a determinism proof and it cures no flakiness"; `corpus/knowledge/hermetic-env-differential.md:4` carries "F3 universal determinism and successor freshness remain unclaimed"; `corpus/SOURCES.md:119` is the S107 row. (The two exceptions are F8 and F9.)
- **No sibling lane is named, and nothing in the entry is falsifiable by reading sibling gates.** `grep -nE 'kumitate|kagi|tsukuroi|mado|kaidoku|kaika|sibling|fleet'` → line 68 only ("the lane's own F3 verdict on its fleet legs remains unmade"). That claim is true as written: `grep -c 'F3' corpus/knowledge/fleet-kill-rate-ledger.md` → `0`. The entry asserts nothing about any sibling gate's code, so no claim here can be contradicted by reading one; reported, per the item, without reading sibling gates.
- **No PROVINCE.md violation found.** `sed -n '1,20p' PROVINCE.md` puts the reusable verification craft and "this lane's own corpus and gates" in province, and requires adjacent evidence to be reported, not absorbed. The entry's F3/F5 statements are protocol claims about the lane's own tools, the source's numbers are bounded at line 66 ("They are not the lane's measurements and do not transfer to the lane's gates"), and no flaky-test-engineering method is adopted as the lane's own. The closest adjacency is line 53's headline claim about suites (F12); it is bounded by the Inference sentence and by line 66, so it is reported as adjacency, not absorption.
- **The frontier claim "F3 stays open" (corpus/README.md:577) is honest about status.** The round added no lane measurement of its own controls (the entry says so at line 68; the ledger carries no F3 verdict — `grep -c 'F3' … → 0`), so `open` is the right status word. What is not honest is the surrounding sentence's characterization: it says these entries "state what the literature measures", while this entry also asserts a status (`held`, F2) and a changed next move (F2b) that the table does not carry. The defect sits on the entry and the table, not on the status word.

## Unrun

- No counter was run as a verdict: no `coverage/measure.py --rev …` run, no `--selftest` run by this seat, no `mutate.py`, no calibration run. The C3 predicate was exercised in-process only (`entry_ok`), as quoted in F1.
- No live fetch: the recheck's live-byte claim was not re-fetched by this seat; only the committed snapshot was read.
- Sibling gates were not read for correctness (item instruction).

## Tooling

No tool installed or upgraded; no `pacman` (host-wide pause). Scratch only under `/tmp/tameshi-r46-T46CritEntryUndetected/`. No writes to `/home/vgpnk/Projects/shokuknow`, the fleet repo, sibling lanes, the lane's git index or jj state; all git calls were read-only `git show`.
