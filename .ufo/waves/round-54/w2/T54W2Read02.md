# T54W2Read02 — cold read of `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` at C1

Axis: calibration. Milestone: C1 fresh read at C1 (wave 2 of round 54).

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Candidate: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Heading: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`
- Section: `start=142`, `end=256` (line 256 is the blank separator), body = lines 142–255, **8820 bytes** after the trailing-newline strip, `section_sha256=77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da`
- Split verification: `reader-section.py` hashes through the round-18 `sectionize()` (`git show C1:.ufo/evidence/round-18/measure.py:209-249`), which splits at headings outside fences, keeps the heading line through the line before the next heading, strips trailing whitespace-only lines and joins with `\n` with no trailing newline. An independent re-derivation (`git show C1:SKILL.md | sed -n '142,256p'`, strip trailing blank lines, `sha256`) gives the same 8820 bytes and the same sha. The same bytes **with** a trailing newline hash `af07b356dd4a2cf40007a8701f4ccd6ad9b727ca981059d3926765d42f4c7231`, and a raw 142–256 slice (which includes the separator) hashes `185b2b6720358a98039627536020ac5c76ba7484efc4490b5ba2eb9c92fa443a`; only the stripped form matches the monitor, so the quotes below are substrings of that exact 8820-byte body.
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Read02/` (`TMPDIR` set there for every command). Nothing outside `.ufo/waves/round-54/w2/` was written in the lane; no lane file was edited.
- Tooling: nothing installed or upgraded for this seat; no `pacman`/`uv`/`npx` transaction was run.

## Commands run

```bash
export HYAKU_SCRATCH=/fast/scratch/hyaku
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read02
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read02
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin

python3 .ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 \
  "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence"
# {"heading": "## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence",
#  "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 142, "end": 256,
#  "section_sha256": "77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da"}

git show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '142,256p'          # read whole, then line by line
git show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | nl -ba | sed -n '17,40p;105,141p;257,324p;386,415p;1733,1779p'
git show 99c3bc88d704566197783f66b211ee0a830e0330:.ufo/evidence/round-18/measure.py | grep -n -A40 'def sectionize'

# every citation in the section, resolved at C1
git show C1:corpus/knowledge/mutation-case-kimi-census.md | nl -ba | sed -n '1,60p;59,100p;109,148p;148,157p;150,205p'
git show C1:corpus/knowledge/mutation-case-kagi-census.md | nl -ba | sed -n '1,60p;60,130p;180,195p;195,215p;245,260p'
git show C1:corpus/knowledge/gates-survey-kumitate.md | nl -ba | sed -n '1,40p'
git show C1:corpus/knowledge/gates-survey-kagi.md | grep -n -i 'errata\|G-R2-1\|re-pin'
git show C1:corpus/knowledge/gates-survey-kagi.md | nl -ba | sed -n '548,566p'
git show C1:corpus/README.md | grep -n 'G-R2-1'
git show C1:corpus/QUALITY.md | nl -ba | sed -n '90,125p'
git show C1:corpus/QUALITY.md | grep -n -i 'duplicate parenthetical\|Criterion 104'
git show C1:tools/mutate-and-run.sh | nl -ba | sed -n '425,445p;500,570p;570,595p'

# fix-pass scope (which hunks touched this section at C1)
git diff 59c38109bf11 99c3bc88d704566197783f66b211ee0a830e0330 -- SKILL.md

# finding receipts
git show C1:corpus/knowledge/mutation-case-kimi-census.md | nl -ba | sed -n '43,45p;47,48p;53,57p'
git show C1:corpus/knowledge/mutation-case-kimi-census.md | grep -n 'non-equivalence'
git show C1:corpus/knowledge/mutation-case-kimi-census.md | sed -n '80,107p' | sed -n '1p;$p'
git show C1:SKILL.md | nl -ba | sed -n '259,261p'
git show C1:SKILL.md | sed -n '304,318p' | grep -n 'D5'
```

C1 is `round-54: C1 fix pass — 26 wave-1 reader findings adjudicated and fixed …`; the C0→C1 diff touches this section in exactly two hunks: step 2 (`full sha256,` → `full sha256, size,`) and step 4 (`one per class` → `at least one per class (two of the JS ten share a class — the :47-48 pair — and the bash exemplar's :70-71 pair does the same)`). Every other line of the section is C0 text carried forward.

## Artifacts opened

| Artifact (at C1 unless noted) | Range read | Why |
|---|---|---|
| `SKILL.md` | 17–40 (`## Standing rules`) | line 6's `(Standing rules; deleted on exit)` pointer |
| `SKILL.md` | 105–141 (`## The mutation bar`) | step 10's `(mutation bar above)` pointer |
| `SKILL.md` | 142–255 (this section) | the whole section, twice (once as text, once with `nl -ba` and invisible-character scans) |
| `SKILL.md` | 257–324 (`## Defect-taxonomy templates…`) | step 4's `(catalog + entry template in the next section)` pointer and the class vocabulary |
| `SKILL.md` | 386–415 (`## Restore discipline`) | step 9's `Full checklist below (Restore discipline)` |
| `SKILL.md` | 1733–1779 (`## Errata — round 16 full-page cold-read`) | the intro's `(two seats; Errata — round 16)` |
| `corpus/knowledge/mutation-case-kimi-census.md` | 1–60, 59–100, 109–148, 148–157, 150–205 | the note's header, table, §2 probes, §3–§6 |
| `corpus/knowledge/mutation-case-kagi-census.md` | 1–60, 60–130, 180–195, 195–215, 245–260 | the note's header, table, §5, §6 U5, §7 sensitivity checks |
| `corpus/knowledge/gates-survey-kumitate.md` | 1–40 | six-suite verdict table |
| `corpus/knowledge/gates-survey-kagi.md` | errata grep, 548–566 | G-R2-1 errata block |
| `corpus/README.md` | `G-R2-1` grep (line 11) | the round-2 addendum row |
| `corpus/QUALITY.md` | 90–125, criterion 104 | the fix-pass re-read rule this wave is judged by |
| `tools/mutate-and-run.sh` | 425–445, 500–570, 570–595 | `:434` failing-count line, `:579-583` DEGRADED/kill-rate block, and the `total` the rate divides by |
| `.ufo/evidence/round-18/measure.py` (via `reader-section.py`) | 209–249 | the hashing convention |
| `.ufo/waves/round-27/w1/Read03.md` | head (first 40 lines) | provenance only — the earlier cold read of this same section, consulted **after** my own pass to check whether a defect I found had already been repaired; nothing from it is cited as evidence about C1 bytes |

## Anchor sweep — every citation in the section resolves at C1

40 distinct anchors; all resolve to the clause they are attached to. No stale line number, no dangling path, no shifted `tools/mutate-and-run.sh` line (the four tool edits this round moved no line this section cites).

| # | Anchor as written | Establishes | Resolves? |
|---|---|---|---|
| 1 | `mutation-case-kimi-census.md:4-7` | /tmp work dir, no fleet write, no live path | yes |
| 2 | `mutation-case-kagi-census.md:24-38` | `mktemp -d` fixtures; two substrate-gated `skip-case`s | yes |
| 3 | `gates-survey-kumitate.md:19-31` | six verdict lines; cite-check `62/62 cases passed`, surface-probe `42/42 cases passed` | yes |
| 4 | `mutation-case-kimi-census.md:20-21` | `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 | yes |
| 5 | `mutation-case-kagi-census.md:27-35,42-43` | 16 cases, 14 hermetic + `skip-case 15`/`16`, control PASS | yes |
| 6 | `mutation-case-kimi-census.md:13-16` | sha256 / size / mtime / repo rev / clean path | yes |
| 7 | `mutation-case-kagi-census.md:13-17` | 886 newlines, "887th line carries no trailing newline" | yes |
| 8 | `corpus/README.md` G-R2-1 row | dirty intermediate state never committed | yes (line 11) |
| 9 | `gates-survey-kagi.md` errata block | G-R2-1 re-pin, §10/`### Errata (round 2)` at :554-561 | yes |
| 10 | `mutation-case-kagi-census.md:44-45` | `cp -p` copy, `cmp`-verified | yes |
| 11 | `mutation-case-kimi-census.md:41-53` | the 10-defect table | yes |
| 12 | `mutation-case-kimi-census.md:155-166` | the 10-edit manifest block | yes |
| 13 | the `:47-48` pair | D4 `dropped arm`, D5 `dropped arm (presence gate)` | yes |
| 14 | kagi `:70-71` pair | B4/B5 both `dropped branch` | yes |
| 15 | `mutation-case-kimi-census.md:183-191` | E1: D7 expectation wrong and kept | yes |
| 16 | `mutation-case-kagi-census.md:184-191` | E1: failing-case counts miscalled 4/10 | yes |
| 17 | `mutation-case-kimi-census.md:22-25` | uniqueness assert, `all unique` | yes |
| 18 | `mutation-case-kagi-census.md:44-47` | same assert, `all 10` | yes |
| 19 | `tools/mutate-and-run.sh:434` | `APPLY FAIL … old-string-count=%d expected=1` | yes |
| 20 | `mutation-case-kimi-census.md:26-28` | per-defect evidence files + aggregate | yes |
| 21 | `mutation-case-kagi-census.md:48-49` | per-defect evidence + `meta.json` with wall time | yes |
| 22 | `mutation-case-kimi-census.md:30-33` | 8/10, 7.0 s, `<n>/43` held | yes |
| 23 | `mutation-case-kagi-census.md:27-35,50-53` | 16 cases held, 11.0 s, 280 s bound | yes |
| 24 | `mutation-case-kimi-census.md:59-76` | failing-case labels verbatim | yes |
| 25 | `mutation-case-kagi-census.md:67,82-103` | `1/16` / FAIL row + `bad-case 05 …` line | yes |
| 26 | `mutation-case-kagi-census.md:88-91` | B4 `got exit=1`, dead on the token | yes |
| 27 | `mutation-case-kimi-census.md:44-53` | D1–D10 rows, D2/D10 survived | yes |
| 28 | `tools/mutate-and-run.sh:579-583` | `pct=$(( (200*killed+total)/(2*total) ))`, `DEGRADED`, `exit 1` | yes (denominator is `total` = every defect line, :515-516) |
| 29 | `mutation-case-kimi-census.md:29-31` | 8/10 = 80 %, 11 runs, 7.0 s, "No inconclusive run" | yes |
| 30 | `mutation-case-kagi-census.md:50-53` | 8/10 = 80 %, 11 runs, 11.0 s | yes |
| 31 | `mutation-case-kimi-census.md:82-99` | D2 `+23 more` vs `+22 more`; D10 `frozen=24` | yes |
| 32 | `mutation-case-kagi-census.md:111-114, :118-122, :252-254` | B5/B10 non-equivalence probes | yes |
| 33 | `mutation-case-kimi-census.md:34-35` | restore proof (no after-revision) | yes |
| 34 | `mutation-case-kagi-census.md:54-56` | restore proof (no after-revision) | yes |
| 35 | `## Restore discipline` section | "Full checklist below" | yes — at `SKILL.md:386`, ordered list 1–7 |
| 36 | `mutation-case-kimi-census.md §1, §3-§6` | the model | sections exist, but the range omits §2 — see F2 |
| 37 | `mutation-case-kagi-census.md §1-§7` | the model | yes (all seven exist) |
| 38 | `mutation-case-kimi-census.md:20-21,29-31` | node v24.21.0, 7.0 s | yes |
| 39 | `Kimi U5 at 204-205`; `Kagi U5 at 203-204` | cross-host stability unknown | yes |
| 40 | `Errata — round 16` | "round 16 executed the recipe end to end (CR04a, CR04b)" | yes (`SKILL.md:1752`; two seats) |

Other consistency checks that came out clean:

- Arithmetic: `8/(8+2) = 80 %` for both rounds; `14` executed `+2` skipped `= 16` enumerated; `43` and `16` are the two denominators the notes print.
- Step 5's disclosure ("The cited historical notes do not establish that the round-2 driver carried the `new != old` no-op guard") matches the notes: neither `mutation-case-kimi-census.md:22-25` nor `mutation-case-kagi-census.md:44-47` records such a guard.
- Step 7's "neither model exercised this" matches both notes' "No inconclusive run" lines (`:29`, `:50`).
- Step 1's `n/m pass` with the `n/m cases passed` parenthetical matches the kumitate table exactly (only cite-check and surface-probe use the "cases passed" wording).
- Invisible-character scan: no double space outside list indentation, no trailing whitespace, no run-together token, no missing space after a sentence period; parenthesis depth over the whole section returns to 0 with no negative excursion. One adjacent-parenthetical pair exists at step 5 (`…failing count: tools/mutate-and-run.sh:434`) (mutation-case-kimi-census.md:22-25; …)`) — balanced and each carries distinct content, so recorded as style, not a defect.

## Findings

### F1 — the shared-class count in step 4 is wrong for the JS exemplar

- Quote (byte-exact substring of the section):

  `8–12 defects, at least one per class (two of the JS ten share a class — the :47-48 pair — and the bash exemplar's :70-71 pair does the same)`

- Why: the kimi note's own class accounting shows a **second** shared-class pair in the JS ten — D1 (`off-by-one count`) and D2 (`off-by-one count (findings cap)`) are tallied together as `off-by-one 1/2` — so four of the ten share a class, not two, and the parenthetical names only the `:47-48` pair; the bash side is right (B4/B5 are the only pair, `dropped branch 1/2`).
- Receipt:

```bash
$ git show C1:corpus/knowledge/mutation-case-kimi-census.md | nl -ba | sed -n '43,45p;47,48p;53,57p'
    43	| — | control | unmutated copy | 0 | `43/43 pass` / `VERDICT: PASS` | green | 0 |
    44	| D1 | off-by-one count | K2 counted dir `counted: 18` → `17` (kimi-census.mjs:105) | 1 | `27/43 pass` / `FAIL` | **killed** | 16 (incl. the exact baseline) |
    45	| D2 | off-by-one count (findings cap) | `findings.slice(0, 6)` → `slice(0, 5)` (kimi-census.mjs:378) | 0 | `43/43 pass` / `PASS` | **survived** | 0 |
    47	| D4 | dropped arm | root-stray reporting loop deleted (kimi-census.mjs:351-353) | 1 | `40/43 pass` / `FAIL` | **killed** | 3 |
    48	| D5 | dropped arm (presence gate) | chain presence `gens.length > 0` → `true` (kimi-census.mjs:255) | 1 | `42/43 pass` / `FAIL` | **killed** | 1 |
    53	| D10 | wrong reported constant | `FROZEN.K2 25` → `24` (kimi-census.mjs:145) | 0 | `43/43 pass` / `PASS` | **survived** | 0 |
    54	
    55	By class: off-by-one 1/2 · inverted condition 1/1 · dropped arm 2/2 · wrong mode pin 1/1 ·
    56	weakened predicate 1/1 · wrong exit mapping 1/1 · weakened secrecy pin 1/1 · wrong
    57	reported constant 0/1.
```

  The tally sums to 8 killed / 10 total, and the only two-member classes are `off-by-one` (D1, D2) and `dropped arm` (D4, D5). The section's parenthetical therefore picked one of the two pairs and described it as the only one. The sentence is inside the C1 fix hunk (`git diff 59c38109bf11 99c3bc88d704566197783f66b211ee0a830e0330 -- SKILL.md`, step-4 hunk), so it is a fix-pass artefact rather than carried C0 text.

### F2 — step 10's kimi model range excludes the only section holding the survivor-probe receipts

- Quote (byte-exact substring of the section):

  `mutation-case-kimi-census.md §1, §3-§6`

- Why: the record list step 10 requires includes `survivor probes`, and the kimi note's survivor-probe results (`O (non-equivalence): …`, the `+23 more` / `frozen=24` observations) exist only in §2, which this range skips — while the same sentence's kagi range (`§1-§7`) does include that note's §2, so the two model pointers disagree about whether the survivor section is part of the model.
- Receipt:

```bash
$ git show C1:corpus/knowledge/mutation-case-kimi-census.md | grep -n 'non-equivalence'
90:O (non-equivalence): on an empty root (28 findings) — pristine prints six ids then
98:O (non-equivalence): same empty root — pristine `FAMILY K2  members=0  checked=0

$ git show C1:corpus/knowledge/mutation-case-kimi-census.md | grep -n '^## '
18:## 0. Method and headline
39:## 1. Kill-rate table
80:## 2. Surviving-defect class analysis
109:## 3. What the 43-case suite protects — and does not
148:## 4. Reproduce
183:## 5. Calibration and errata (append-only)
193:## 6. Unknowns
```

  Both `non-equivalence` receipts (lines 90 and 98) fall inside §2 (80–107) and nowhere else in the note, and step 8 of the same section cites exactly those lines (`(mutation-case-kimi-census.md:82-99)`). The kagi note's §2 is `Surviving-defect class analysis` too (`mutation-case-kagi-census.md:105`), and `§1-§7` covers it — hence the asymmetry.

## Cross-section observation (reported, not counted as a finding)

While resolving step 4's `(catalog + entry template in the next section)` pointer I found a live contradiction whose erring bytes are **not** in this section, so it is recorded here for the owner of `## Defect-taxonomy templates and exact-string guidance` rather than claimed as this section's defect:

- `SKILL.md:260` (next section): `One defect per class per sweep, and widen beyond the measured set when the artifact offers a new mechanism.`
- Step 4 of this section now says `at least one per class` and cites an exemplar whose two pairs share classes, so an executor cannot satisfy both. The catalog's own table also splits D5 across two rows (`dropped arm` and `weakened presence gate`, `SKILL.md:309-310`), which contradicts `One defect per class per sweep` in the other direction.

Receipt:

```bash
$ git show C1:SKILL.md | nl -ba | sed -n '259,261p'
   259	The classes are the injection vocabulary; read which class the suite can see.
   260	One defect per class per sweep, and widen beyond the measured set when the
   261	artifact offers a new mechanism.

$ git show C1:SKILL.md | sed -n '304,318p' | grep -n 'D5'
6:| dropped arm | … | D4 → 3 root-enum cases; D5 → 1 (mutation-case-kimi-census.md:47-48) | … |
7:| weakened presence gate | force a presence bool to `true` | the single no-chain tripwire | D5 → 1 (mutation-case-kimi-census.md:48) | … |
```

## Limits

- I read the section as an executor, with no use of the wave-1 verdicts. The `.ufo/waves/round-27/w1/Read03.md` head was opened **after** F1 and F2 were written down, only to check whether the C1 hunks had already answered them; it is not evidence for anything above. That round-27 report's third minor gap named the same shared-class fact (`Kimi D1 and D2 are both off-by-one count … D4 and D5 are both dropped arm … Kagi B4 and B5 are both dropped branch`) and the C1 hunk repaired step 4 by citing only the `:47-48` and `:70-71` pairs, which is how the undercount reached C1.
- "Two of the JS ten share a class" was tested against the note's own by-class tally, not against my own re-classification; if a reader rejects the tally as authoritative, F1 collapses to an incompleteness rather than a miscount. F2 does not depend on any classification.
- Everything else in the section checked clean: 40/40 anchors resolve, the numeric claims match the notes and the driver, and no run-together token, duplicate parenthetical or self-contradiction was found inside the section's own 8820 bytes.
- No lane file was edited; `SKILL.md`, the counters, contract, freeze, ledger and wave specs are untouched. No mutating git command was run. The only two files I wrote are the `.json` and `.md` named above, both under `.ufo/waves/round-54/w2/`.
- Observed lane state (not mine, no action taken): at 12:00:31 the index reported ` M .ufo/evidence/round-54/c1/measure.py`. `git diff --numstat` for that path is empty and the worktree sha256 `d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812` equals `git show HEAD:…/c1/measure.py`'s sha, so it was a stat-only index entry, not a content change; the entry cleared on the next `git status`. Flagged only because a frozen counter moving during the round would matter, and it did not.
