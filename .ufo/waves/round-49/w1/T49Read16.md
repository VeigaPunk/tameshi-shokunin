# T49Read16 — C1 reader, `## Pin disposition and provenance correction — round 13`, pointer ordinals 5-8

Seat: T49Read16 (scribe, C1 reads). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base: `8ca67421111fa354b47b803358391d0b07fc6db9`. Deliverable: `.ufo/waves/round-49/w1/T49Read16.rows.json`.
I decide no claim and ran no verdict-producing invocation: only `--list` at base, plus read-only `git show`.

## Method

1. `python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list` → exit 0.
   Output kept verbatim as `T49Read16.c1-list-at-base-8ca67421.json`; its sha256
   `92a2e532fb323bee556e44b0877107339f7faa9e1c8f9636a8a6b1a8de6d4d3c` is **equal to the frozen control file**
   `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`, so the frozen table is exactly this extractor's
   `--list` output at base (extractor determinism, not a copy of convenience).
2. Section identity: `git -C . show 8ca67421:SKILL.md | sed -n '1517,1547p'`; the monitor's own splitter
   (`.ufo/evidence/round-18/measure.py:209` `sectionize`, loaded through `.ufo/evidence/round-21/coldread/measure.py`)
   gives start 1517, end 1547, sha256 `eb9c487be851b8886298fa2340a61af0c970d6ce75cbabd0e7eea741875e3e83` — equal to the
   frozen `section_sha256`; the heading occurs once in SKILL.md at base. The `###` sub-heading at SKILL.md:1548 starts a
   different section, so this read window is SKILL.md:1517-1547.
3. Targets at base: `git -C . show 8ca67421:.ufo/evidence/round-13/witness-metadata.json` (3500 B);
   `git -C . show 8ca67421:corpus/SOURCES.md | sed -n '14p;50p;56p'` for S003 / S041 / S047.
4. Excerpt gate reproduced locally with the counter's own `norm()` / `pointed_text()` semantics, `EXCERPT_MIN=24`,
   `EXCERPT_MAX=400` (`.ufo/evidence/round-49/c1/measure.py:202-208`, `:307-313`): every row's collapsed excerpt occurs in
   the collapsed pointed text (path pointer → whole file; S-id pointer → its SOURCES.md row line), and every `claim` is a
   verbatim substring of base SKILL.md. Receipt: `T49Read16.excerpt-check.txt`.

## Rows (verdicts)

| ord | pointer | file | ranges | verdict | one-line reasoning |
|---|---|---|---|---|---|
| 5 | `.ufo/evidence/round-13/witness-metadata.json` | same | null | holds | The receipt SKILL.md:1538-1539 calls the companion really is the round-13 companion, and its declared digests equal the sha256 of the frozen round-12 files they name, so "digest-anchored frozen sources" is re-checkable on this exact file. |
| 6 | `S003` | `corpus/SOURCES.md` | [[14,14]] | holds | SOURCES.md:14 is the single S003 row (StrykerJS incremental verdict reuse, tier A, mined, used-by `corpus/knowledge/incremental-pin-disposition.md`), and its teaches cell is precisely the blind-spot limit the section's table restates at SKILL.md:1526/1529. |
| 7 | `S047` | `corpus/SOURCES.md` | [[56,56]] | holds | SOURCES.md:56 is titled "precision correction" (the phrase SKILL.md:1519 uses) for the same PIT page with scope "not a general reuse guarantee", and `corpus/knowledge/incremental-pin-disposition.md:1` names S047 as this section's precision-correction row. |
| 8 | `S041` | `corpus/SOURCES.md` | [[50,50]] | holds | SOURCES.md:50 is the PIT result-reuse row ("F7 — PIT's result-reuse assumptions", reuse is an inference not an observation) that S047's row says it supersedes, which is exactly what "(historical S041 retained)" asserts. |

No row is `stale`, `unresolved` or `absent`; therefore no row carries `proposed_fix`. Nothing needed correcting among these
four pointers — reported as observed, not softened and not inflated.

## Findings

1. **ordinal 5 — the companion is digest-anchored, checkably.** `.ufo/evidence/round-13/witness-metadata.json:3` says
   `"generated_for": "round-13"`; `:4` says "Digest-anchored normalized metadata for the frozen round-12 BashWitness
   declaration"; `:12` anchors `summary.json` at `acc01268…` , and the sibling entries pin `declaration.json` and
   `declared.tsv`. All four pins re-hash equal at base (`T49Read16.excerpt-check.txt`, "companion digest anchors
   re-checked"): `acc01268…`, `e8d2024a…`, `0def0d3b…`, plus the out-of-scope rerun summary `6726421f…`.
   `tools/witness-metadata.py:63` ("These are the authority, not the companion file") and `:72-89` (`PINNED_INPUTS`) pin the
   same literals, and `:68` sets `DEFAULT_COMPANION_REL` to this exact path — so the recipe step's verb "checks …
   against digest-anchored frozen sources" is satisfied by this file plus that tool, not by a different receipt.
   Command: `python3 - <<'PY' … hashlib.sha256(git cat-file blob base:<path>) …` (receipt file, section "companion digest
   anchors").
2. **ordinal 6 — S003 supports the sentence it sits in, and more than the sentence.** SKILL.md:1519 lists S003; the row at
   SOURCES.md:14 carries the source, tier, scope and teaches cell, and the section's own first pointer
   `corpus/knowledge/incremental-pin-disposition.md:1` re-states the same id and page. The section's Limit column
   ("Mode, dependencies, environment, runner/spec and invocation identity remain unmeasured", SKILL.md:1526) is the row's
   declared blind spots (env vars, dependencies, `.snap`), so the citation is load-bearing rather than decorative.
   Command: `git -C . show 8ca67421:corpus/SOURCES.md | sed -n '14p'`.
3. **ordinal 7 — the pointer crosses a section boundary that matters for the L1.** SKILL.md:1558-1561 says
   "S048 supersedes S047's object-specific paraphrase; retain only the supported distinction 'item 4 is prioritisation, not a
   reuse skip'". That sentence is **not** in this section: `sectionize` closes this heading at line 1547 and opens
   `### Round-13 gate/probe registry` at 1548 (monitor splitter, verified by recomputed sha256 equality). It does not make
   the Sources line stale — S047's row is literally the precision-correction row and S047 is still a named source — but the
   integration should not read it as "S047 supplies the pronoun distinction"; the section itself already retires that part.
   Commands: `git show 8ca67421:SKILL.md | sed -n '1548,1562p'`; section split as in Method step 2.
4. **ordinal 8 — the register's status word is not the section's wording.** SOURCES.md:50 still says `mined` in the status
   column while SKILL.md:1519 calls S041 "historical". These are different vocabularies (register status vs. the section's
   use-disposition) and the row itself records the approach: "reuse of a prior verdict is an inference, not an observation".
   No defect; recorded because a reader diffing the two columns will notice it.
5. **Durability for the REV read.** SKILL.md (166524 B), `corpus/SOURCES.md` (116284 B) and the round-13 companion (3500 B)
   are byte-identical at base and at HEAD `455b2cd66fd9f237146a5355ca8bbc84f3071c50`; the three registry rows still sit at
   lines 14/50/56 at HEAD (`git show HEAD:corpus/SOURCES.md | grep -n '^| S00[34]\|^| S041'`). S-id pointers are re-resolved
   at REV by the counter, so these row numbers are a base fact, not a pinned range the integration must freeze.
   Command: `python3` digest/size comparison of `cat-file blob base:<p>` vs `cat-file blob HEAD:<p>` (receipt).

## Touched surfaces

Written (my only writes, both inside `.ufo/waves/round-49/w1`):

- `.ufo/waves/round-49/w1/T49Read16.rows.json` — sha256 `73b365529eb006bc67191082c7ad9f5cab20214cc3058cb67d239d1278a1d914`, 4 rows (ordinals 5-8), all `holds`.
- `.ufo/waves/round-49/w1/T49Read16.excerpt-check.txt` — sha256 `bd147a86b23cdcf6c26d1eee701e81b0cd052e41d2c9921d30731b7646a15a16`.
- `.ufo/waves/round-49/w1/T49Read16.c1-list-at-base-8ca67421.json` — sha256 `92a2e532fb323bee556e44b0877107339f7faa9e1c8f9636a8a6b1a8de6d4d3c` (receipt copy of the `--list` output).
- `.ufo/waves/round-49/w1/T49Read16.md` — this report.

No scratch dir was needed: every command was a read against the lane's own git store; nothing was cloned, nothing written
under `/tmp` except the `--list` capture, which was copied into `w1` and is cited only from there.

## Out of scope / not claimed

- Ordinals 0-4 of this same section (`corpus/knowledge/incremental-pin-disposition.md`,
  `corpus/lessons/round-12-verifier-spotcheck.md`, `tools/pin-disposition.py`, `.ufo/evidence/round-13/pin-manifest.json`,
  `tools/witness-metadata.py`) belong to other seats and are not read here.
- No counter verdict: `C1_R49_PASS` is the L1's; `--list` prints pointers only. The excerpt check reproduces the counter's
  normalisation, it does not stand in for the deciding invocation.
- Semantic support (does the quoted text really mean what the section says) is my judgement; the contract's `cannot_see`
  names exactly this limit, and CTL_K2 is the positive control for mechanically valid but unsupporting rows.
- I did not read anything under `/home/vgpnk/.local/state/`, no C2 control stdout, no hidden panel; no model was passed; no
  tool was installed or upgraded this seat (nothing needed).

## Summary

Read the four assigned pointers of `## Pin disposition and provenance correction — round 13` against base `8ca67421`.
Verdicts: ordinal 5 `.ufo/evidence/round-13/witness-metadata.json` holds; ordinal 6 `S003` holds; ordinal 7 `S047` holds; ordinal 8 `S041` holds.
Zero stale, zero unresolved, zero absent — no `proposed_fix` rows, reported as observed rather than manufactured.
The companion's four digest pins re-hash equal to the frozen round-12 blobs, so "digest-anchored frozen sources" is checkable on that exact file.
Section identity is pinned: start 1517, end 1547, sha256 `eb9c487b…` equals the frozen value; the heading occurs once.
Boundary note for integration: the S048 narrowing (SKILL.md:1558-1561) sits in the `###` registry block, not in this section.
All three targets and SKILL.md are byte-identical base..HEAD `455b2cd6`, so a REV read resolves the same bytes.
Deliverables: `T49Read16.rows.json`, `T49Read16.excerpt-check.txt`, `T49Read16.c1-list-at-base-8ca67421.json`, `T49Read16.md`.
