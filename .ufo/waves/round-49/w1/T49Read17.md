# T49Read17 — C1 reader: `## Effective expectation reconciliation — round 14`, pointer ordinals 0-4

Seat: C1 reader (leaf, no dispatch). Base `8ca67421111fa354b47b803358391d0b07fc6db9`; frozen pointers
`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`. I produce findings and rows, no claim decision.

## Behavior

Five pointers read at base, each opened at its `skill_line` in base SKILL.md and compared with the target at base:

| ord | raw | base_verdict | one-line reasoning |
|---|---|---|---|
| 0 | `corpus/lessons/round-13-verifier-spotcheck.md` | holds | the file's `## Routed defects and residuals` really carries defects 1-3 and their prescriptions (:175, :179-:181) |
| 1 | `corpus/knowledge/incremental-pin-disposition.md` | holds | §8 is the empirical correction the sentence numbers 8 (:314) and records the twelve-row/one-superseded ledger (:380) |
| 2 | `tools/evidence-disposition.py` | holds | the tool exists at base and its USAGE is exactly `--root LANE --dispositions FILE [--json]` (:167) with the supersession gate (:170-173) |
| 3 | `.ufo/evidence/round-14/dispositions-before.json` | holds | a v1 disposition manifest on the round-13 expected file with 12 all-`effective` rows (:2-:9, :35-:38) — the run that fails `producer_before` |
| 4 | `dispositions.json` | unresolved | bare filename: the frozen extractor resolves none of its four candidates at base, `--list` prints `file=null`; the file the sentence means is held at `.ufo/evidence/round-14/dispositions.json` |

Deliverable rows: `.ufo/waves/round-49/w1/T49Read17.rows.json` (heading/ordinal/raw/file/ranges copied from the frozen
pointer file; `verdict` mirrors `base_verdict`; ordinal 4 carries `proposed_fix`).

### Row detail

**ordinal 0 — holds.** SKILL.md:1565 `Sources: corpus/lessons/round-13-verifier-spotcheck.md, Routed defects1–3;`.
`git -C LANE show 8ca67421:corpus/lessons/round-13-verifier-spotcheck.md | sed -n 175,181p` prints
`## Routed defects and residuals` (175) and items 1-3: defect 1 (179) = the stale `expected.json expected_checks.producer_before`
row plus "Add a clearly effective/superseded expectation disposition or replacement receipt … Do not erase the initial failure",
defect 2 (180) = the GIT_DIR setup not durably recorded, defect 3 (181) = "Add a later empirical backlink/correction in future
knowledge maintenance". Those are exactly the section's table rows 2 and 4 (SKILL.md:1573, :1575) and the reason pointer 1 is
cited; the file is a record that has not moved. No line drift (path pointer, whole file).

**ordinal 1 — holds.** SKILL.md:1567 `` corpus/knowledge/incremental-pin-disposition.md , empirical correction8.``
`git -C LANE show 8ca67421:corpus/knowledge/incremental-pin-disposition.md | sed -n 314,320p` prints
`## 8. Empirical correction and backlink — round 14 (2026-10-20)` and "This addendum supersedes only section6's
**deferred-at-write** status …". :380 states "All twelve expected rows are accounted for, eleven effective plus one explicitly
superseded", i.e. the reconciliation the section teaches; :363 names the stale `producer_before` assertion. Support is exact.

**ordinal 2 — holds.** SKILL.md:1583 `python3 tools/evidence-disposition.py --root . --dispositions
.ufo/evidence/round-14/dispositions-before.json --json`. The base tool (sha256 39ee5c5e…) is r18, `VERSION` at
tools/evidence-disposition.py:135; its USAGE line :167 is the same flag set, :170-173 states "the one configured
producer_before supersession must retain a genuinely mismatched raw observation and pass both oracle replacements", and the
exit map (:107-111) gives 1 = failed semantic expectation, 2 = could-not-evaluate. The sentence's replay runs the extracted
`git archive 28aeef4` tree's own r14 copy (sha256 1609a9df…); both copies accept the identical CLI, which is the clause the
pointer supports — the `→ 1` outcome belongs to the archive copy and is corroborated in Probes.

**ordinal 3 — holds.** SKILL.md:1583 argument `.ufo/evidence/round-14/dispositions-before.json`.
`git -C LANE show 8ca67421:.ufo/evidence/round-14/dispositions-before.json` is a `evidence-dispositions-v1` manifest (:2) on
`.ufo/evidence/round-13/expected.json` (:3), pins that file plus its two receipts (:4-:7), and holds 12 rows (:9 onward) all
`state: effective`, `producer_before` included at :35-:38. That pre-supersession state is what makes the replay fail
`producer_before`; the target supports the argument and its documented effect.

**ordinal 4 — unresolved.** SKILL.md:1585 "The same command with `dispositions.json` → 0: the only repair is that row's
explicit supersession,". `python3 -I .ufo/evidence/round-49/c1/measure.py --lane LANE --rev <base> --list` prints
`{"ordinal": 4, "raw": "dispositions.json", "kind": "path", "file": null}`; `measure.py:171-193` tries `dispositions.json`,
`corpus/knowledge/dispositions.json`, `corpus/dispositions.json`, `corpus/lessons/dispositions.json` and finds no blob, and
`measure.py:271-279` counts every file-null pointer unresolved unless a row claims `absent`. The target is **not** absent: the
sentence means the round-14 after-manifest, held at `.ufo/evidence/round-14/dispositions.json` (base blob sha256
77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005), whose `producer_before` row is `"state": "superseded"`
(:36) with `raw_receipt`/`raw_check` retained (:38-:39) and `superseded_by` naming `producer_before_oracle` +
`producer_after_oracle` (:40-:43), both replacement rows `state: effective` (:46-:49, :51-:55). So the defect is the missing
directory qualifier, and staying `absent` would drop a pointer the section still needs. Fix (in the row):
`The same command with `dispositions.json` → 0` → `The same command with `.ufo/evidence/round-14/dispositions.json` → 0`
(fixed_file `.ufo/evidence/round-14/dispositions.json`, no ranges). Dry run of the frozen extractor on the edited section text:
10 pointers before and after, ordinals unchanged, ordinal 4 now resolves (file was `None`); the section floor of 10
(`measure.py` FLOORS) is untouched.

## Excerpt verification

Every excerpt was tested with the counter's own `norm()`/pointed-text rule (`measure.py:202-209`) against the whole-file
target at base, before and after writing the rows. Transcript: `.ufo/waves/round-49/w1/T49Read17.excerpt-check.txt`.

- ordinal 0: 389 chars, occurs once in collapsed text of `corpus/lessons/round-13-verifier-spotcheck.md`
- ordinal 1: 234 chars, occurs once in `corpus/knowledge/incremental-pin-disposition.md`
- ordinal 2: 277 chars, occurs once in `tools/evidence-disposition.py`
- ordinal 3: 213 chars, occurs once in `.ufo/evidence/round-14/dispositions-before.json`
- ordinal 4: 161 chars quoted from the intended target `.ufo/evidence/round-14/dispositions.json` (there is no blob at the
  written path), occurs once there; the same text is `fixed_excerpt`

## Probes (observed output; a probe is never a verdict)

All probes ran on extracted `git archive` trees under the seat scratch root; no lane byte was written. Receipt:
`.ufo/waves/round-49/w1/T49Read17.probe-receipt.json`.

- Archive `28aeef4` (its own tool r14, sha256 1609a9df…): `python3 -I tools/evidence-disposition.py --root .
  --dispositions .ufo/evidence/round-14/dispositions-before.json --json` → **exit 1**, `status=failed`, counts
  `{effective 12, expected_checks 12, failed 1, passed 11, superseded 0}`, finding
  `expected_contains_missing / producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'`, all 13
  expected inputs verified. Same command with `dispositions.json` → **exit 0**, `status=clean`, `{effective 11, passed 11,
  superseded 1}`. This reproduces SKILL.md:1583-1586 exactly.
- Base tree (its tool r18, sha256 39ee5c5e…): both manifests → **exit 2**, `status=could_not_evaluate`,
  `id=expected_input_digest_mismatch`, first finding `tools/bash-witness-study.py: observed 60575e62… expects 49e9e5e2…`.
  Matches SKILL.md:1581 "at `--root .` both manifests now return 2 `expected_input_digest_mismatch`".
- 13 pinned inputs at base: 10 match, 3 differ (`tools/pin-disposition.py`, `tools/bash-witness-study.py`,
  `tools/mutate-and-run.sh`).
- Runner parenthetical SKILL.md:1581-1582 "(the runner moved in round 16)": round-13/14 runner content sha256 is
  `75ed934dc863…` (identical at 606716f70 and 28aeef4) and the first later content is `0673d2e5…` at commit 05a224754
  ("round-16: wave-2 repairs"). The parenthetical is accurate; the reader at base simply meets
  `tools/bash-witness-study.py` first because the tool stops at the first mismatched input.

## Touched surfaces

- Written: `.ufo/waves/round-49/w1/T49Read17.rows.json`, `T49Read17.md`, `T49Read17.excerpt-check.txt`,
  `T49Read17.probe-receipt.json`.
- Read only: base blobs via `git -C LANE show <base>:<path>`; frozen counter `--list`; two extracted archives in scratch.
- Nothing else written; no lane/jj/Git-index change, no fleet-repo or `shokuknow` write, no `~/.local/state` read, no
  control stdout read (c2-WITNESS/CTL_FIX/CTL_ABSENT untouched), no model call, no `agent://all` message.
- Tool installs/updates: none (python3/git present, nothing installed).
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read17` deleted before yield.

## Out of scope

- Ordinals 5-9 of the same section (other seats). Observed in `--list` only: ordinals 6 (`verification.json`) and 7
  (`capture-context.py`) are also file-null bare tokens; I did not adjudicate them or propose their fixes.
- No SKILL.md edit, no `reads.json`, no C1 verdict, no counter deciding run, no panel access.

## Findings

1. **SKILL.md:1585 — bare `dispositions.json` cannot resolve.** `--list` gives `file=null`, `kind=null`; the four
   resolution candidates are absent at base (`measure.py:171-193`). The intended file exists at
   `.ufo/evidence/round-14/dispositions.json` (sha256 77faac58…) and its `producer_before` row is exactly the supersession the
   sentence describes (:35-:43). Qualifying the path keeps one pointer and the 10-pointer floor.
2. **Ordinals 0-3 hold with exact support** — the three sources the section names exist and say what the section attributes
   to them; no line drift (all four are whole-file path pointers).
3. **SKILL.md:1581-1583 replay is reproducible as written** — archive `28aeef4` gives 1/1-failed for the before manifest and
   0/clean for the after manifest; the base-tree `2 expected_input_digest_mismatch` also reproduces (Probes). No correction
   needed there for calibration beyond the ordinal-4 qualifier.
4. **Pointer 2's target is the lane's current tool (r18), the sentence's replay uses the archive tree's r14 tool** — both
   expose the same flags and exit map, so the pointer still supports its clause; recorded so wave-2 does not read the version
   difference as a defect.

## Summary

1. Five pointers read at base: 4 `holds`, 1 `unresolved` (ordinal 4, bare filename), nothing `stale`/`absent`.
2. Each excerpt is 161-389 chars, verified verbatim (whitespace-collapsed) against the base blob, occurring once.
3. Fix for ordinal 4: qualify the path to `.ufo/evidence/round-14/dispositions.json`; extractor dry run keeps 10 pointers and resolves ordinal 4.
4. Section's own factual claims reproduce: archive `28aeef4` replay → 1 then 0; base tree → 2 `expected_input_digest_mismatch`.
5. Parenthetical "the runner moved in round 16" verified (75ed934d… → 0673d2e5… at commit 05a224754).
6. Ordinals 5-9 (others' rows) and the section edit/reads.json remain with the L1; I proposed no fix outside 0-4.
7. Artifacts: `w1/T49Read17.rows.json`, `.md`, `.excerpt-check.txt`, `.probe-receipt.json`; scratch removed.
