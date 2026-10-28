# T54W1Crit04 — falsify C2 sourced claim (S277–S279)

Seat: `T54W1Crit04` (critic). Axes under test: **discernment**, **calibration**.
Target: `corpus/knowledge/scratch-root-contract.md` at C0 `59c38109bf119d0e9d4f878644a82babc937bc1e` vs rows S277–S279.
Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1Crit04/` (cleaned on exit).
Receipts: `.ufo/waves/round-54/w1/T54W1Crit04-receipts/`.
No lane production files edited. No pacman install.

## Verdict

The note **overreaches S278/S279 on three empty-arm sentences**. The S277 “standard fixes only the meaning” sentence **holds against the S277 row** (it restates the claim cell; opened POSIX supplies only the positive quote). S279 is cited for empty-string fall-through that its opened artifact never states — false provenance; empty skip is S278 alone.

## Opened artifacts

| Artifact | Path | Check |
|---|---|---|
| Note at C0 | `git show 59c38109bf11:corpus/knowledge/scratch-root-contract.md` | empty-arm block lines 9–30 |
| S277 row | `corpus/SOURCES.md` S277 | claim cell vs note |
| S278 row | `corpus/SOURCES.md` S278 | claim cell vs note |
| S279 row | `corpus/SOURCES.md` S279 | claim cell vs note |
| S277 snapshot | `.ufo/evidence/round-54/assimilation/S277-posix-env.html` | sha256 `89294048…` matches row |
| S278 snapshot | `.ufo/evidence/round-54/assimilation/S278-tempfile.py` | sha256 `fb44155f…`; lines 163–165 |
| S279 snapshot | `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html` | sha256 `6b0edccf…`; gettempdir list |
| Registry | `tools/registry.json` `scratch_root` cells | echo “platform default applies” |

---

## Finding 1 — empty-arm table attributes “platform default” to the empty arm (overreaches S278)

**Sentence (note L14):**
> **unset**: Python's resolver skips an empty candidate, so the next candidate wins (S278) and the platform default applies

**Why it overreaches.** S278 supports skip + “next candidate wins”. It does **not** support “the platform default applies”. The candidate list after a skipped `TMPDIR` is `TEMP`, `TMP`, then OS locations, then cwd (S278:163–179; S279 list order). If `TEMP`/`TMP` is set, that wins — not the platform default.

**Counterexample (receipt r9):**

```text
=== R9 counterexample: TMPDIR='' + TEMP=custom → next candidate, not platform default ===
TMPDIR= ''
TEMP= /fast/scratch/hyaku/tameshi-r54/T54W1Crit04/temp-candidate
gettempdir()= /fast/scratch/hyaku/tameshi-r54/T54W1Crit04/temp-candidate
equals_custom= True
equals_/tmp= False
VERDICT: platform default does NOT apply when next candidate (TEMP) wins
```

Command:
`python3 -c '… TMPDIR=""; TEMP=<custom>; tempfile.tempdir=None; print(tempfile.gettempdir())'`
Full transcript: `T54W1Crit04-receipts/r9-platform-default-counterexample.txt`.

**Minimal rewrite that would not overreach:**
> **unset**: Python's resolver skips an empty candidate, so the next candidate wins (S278)

(Drop “and the platform default applies”. Unset-arm may keep “platform default” for *absent* TMPDIR; empty-arm must not.)

Same overreach is echoed in all seven `tools/registry.json` `scratch_root` cells (“TMPDIR empty => unset, the platform default applies”) — receipt r8 — so “the registry rows say so” (note L30) is circular confirmation of the same defect, not S-row support.

---

## Finding 2 — citing S279 for empty-arm “falls through” (false provenance)

**Sentence (note L17–22):**
> … so an empty `TMPDIR` never becomes a candidate directory; the documented list also starts at "the directory named by the TMPDIR environment variable" and then falls through (S279).

**Sentence-by-sentence vs S278 / S279:**

| Clause | S278? | S279 opened artifact? |
|---|---|---|
| Code quote + `:163-165` | yes (exact) | n/a |
| empty never becomes a candidate | yes (`if dirname:`) | no |
| list starts at “directory named by TMPDIR” | (code order) | yes (quoted) |
| “and then falls through” **for empty** | yes (skip → next) | **no** — artifact never says empty/missing/fall-through |

**Evidence (receipts r4, r5, r10):** S279 HTML has zero hits for `empty` / `unset` / `missing` / `fall through`. gettempdir docs only list search order. S279’s SOURCES claim cell itself inserts “missing or empty TMPDIR falls through”; the opened snapshot does not. The note inherits that padding by hanging `(S279)` on the fall-through clause.

```text
# r10
artifact contains "empty": False
claim cell contains "empty": True
SUPPORTED_BY_ARTIFACT_FOR_EMPTY: False
SUPPORTED_BY_ARTIFACT_FOR_LIST_ORDER: True
```

**Minimal rewrite:**
> … so an empty `TMPDIR` never becomes a candidate directory (S278). The documented search list begins “The directory named by the TMPDIR environment variable”, then TEMP, TMP, and platform locations (S279).

(Attribute empty→skip→continue only to S278; S279 only for ordered-list wording.)

---

## Finding 3 — “allocate under the working directory” is not supported by S277–S279

**Sentence (note L22–24):**
> A tool that treated `""` as a path would try to allocate under the working directory — a silent, wrong scratch root — which is why the arm is declared rather than left to whatever `os.path.isdir("")` happens to return.

**Why it overreaches.** None of S277–S279 assert that treating `""` as a path allocates under cwd. S278’s cwd entry is a **last resort after failed candidates** (L175–179), a different control path. `os.path.isdir("")` is not mentioned in any of the three rows.

**Evidence (receipts r6, r13):** on this host `os.path.isdir("")` is `False`; `os.path.join("","tmpTest")` abspath-lands under cwd — speculative local behaviour, not source-backed.

**Minimal rewrite:**
> Empty is skipped by the resolver the lane calls (S278); the lane therefore declares empty⇒unset instead of treating `""` as a directory path.

---

## S277 check — “standard fixes only the meaning” (does **not** overreach the row)

**Sentence (note L26–28):**
> The standard fixes only the variable's meaning, not its empty-string handling: `TMPDIR` "shall represent a pathname of a directory made available for programs that need a place to create temporary files" (S277).

| Half | vs S277 claim cell | vs opened POSIX TMPDIR paragraph |
|---|---|---|
| positive quote | matches | present verbatim (`This variable shall represent…`) — r2/r11 |
| “not its empty-string handling” | **exact claim-cell language** | absent from TMPDIR paragraph (r7/r11b: `empty_in_tmpdir_paragraph: False`; unrelated “empty string” hits are LANGUAGE / printf elsewhere on the same HTML page) |

**Verdict:** against S277 the row, the sentence holds (note restates the mined claim). Against opened POSIX alone, the negative half is silence-inference already packaged by the row — not a new note overreach beyond S277. No rewrite required for note-vs-S277-row; optional clarity mark `(I)` on the negative half if the lane wants source-vs-inference hygiene.

“The empty arm is therefore a lane declaration that follows the resolver…” is sound given S277 silence + S278 behaviour. Trailing “and the registry rows say so” does not add S-row support (Finding 1).

---

## Sentences that do **not** overreach (empty-arm sweep)

- “The empty arm is not a convenience.” — framing; no S claim.
- S278 code quote and “empty `TMPDIR` never becomes a candidate directory” — S278.
- Unusable-arm / exit-class / round-53 history / measure.py paragraphs — not attributed to S277–S279; out of this attack’s sourced-claim scope.
- Snapshot digests match SOURCES truncated shas (receipt r1).

---

## Runnable receipt index

| ID | File | Assertion |
|---|---|---|
| r1 | `r1-sha-vs-sources.txt` | assimilation sha256 prefixes match S277–S279 |
| r2 | `r2-s277-tmpdir-text.txt` | POSIX TMPDIR shall-represent sentence |
| r3 | `r3-s278-empty-skip.txt` | `_candidate_tempdir_list` 163–165; `if dirname` skips `""` |
| r4 | `r4-s279-docs-text.txt` | gettempdir list order quote |
| r5 | `r5-s279-no-empty.txt` | S279 artifact has no empty/unset/missing/fall-through |
| r6 | `r6-empty-as-path.txt` | join/`gettempdir` under empty TMPDIR |
| r7 | `r7-s277-silence.txt` | TMPDIR paragraph has no empty handling |
| r8 | `r8-citations-and-registry.txt` | note citation sites; registry echoes platform-default |
| r9 | `r9-platform-default-counterexample.txt` | TEMP wins when TMPDIR=""; falsifies “platform default applies” |
| r10 | `r10-s279-claim-vs-artifact.txt` | S279 claim cell “empty” absent from artifact |
| r11 | `r11-s277-quote-check.txt` | note quote + row/artifact split on negative half |
| r11b | `r11b-empty-string-locus.txt` | “empty string” on S277 page is non-TMPDIR |
| r12 | `r12-note-empty-arm-block.txt` | C0 note lines 9–30 |
| r13 | `r13-isdir-empty.txt` | `isdir("")` is False here |

## Impacted axes / smallest safe correction

- **Discernment:** S279 cited for empty semantics it does not contain (Finding 2); cwd-allocation sentence unsourced (Finding 3).
- **Calibration:** “platform default applies” on the empty arm is false under a set `TEMP` (Finding 1) — overclaims what S278 measures.

Smallest safe correction (note only; this seat does not edit): apply the three minimal rewrites above; optionally align registry `scratch_root` cells to drop “platform default applies” on the empty arm so they stop echoing the overreach. No change required to the S277 sentence vs its row.

## Tooling

No installs. Host pacman paused; nothing needed via uv/npx/binary.
