# T86S1 — round-86 lesson proposal (source Gate, Mistakes, curation delta)

Advisory draft for L1 TameshiR86. **Not** production, **not** a measurement receipt, **not**
independent admission, **not** canonical judgment. L1 is sole planner and integration owner.
Base `d10a9c66d6181cddcad52cdbffd672beb886ff6c`; freeze
`55d5a5c6002a048337cc511e1712df87b961d364`.

Axes touched by this draft: **source fidelity / non-duplication** (the Gate's sourced claim) and
**verification-fixture craft** (the pointer-resolution fixture below). The prose below is a
proposal for the lesson body, not a landed lesson.

## Gate

### Source re-open (proposed text)

Source **S305** (Git `git-ls-tree` documentation, git-scm.com, tier A docs) re-opened by L1 on
**2026-11-04** at `https://git-scm.com/docs/git-ls-tree`. HTTP/2 200, 39083 B, sha256
`ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267` — byte-identical to the
round-77 snapshot `.ufo/evidence/round-77/sources/s305-ls-tree.html`, so this is a **re-open of
an existing row, not a new source**. Round-86 snapshot:
`.ufo/evidence/round-86/sources/s305-ls-tree.html` (+ headers `s305.headers`).

**Located quotes — corrected.** The frozen plan and contract carry "page lines 1807 and 1811".
That is an **off-by-one**: the two quotes are at **snapshot lines 1808 and 1812**. Measured by
re-opening the URL live and by scanning the committed snapshot:

- snapshot line **1808** → `<p>The mode of the object.</p>` → rendered text
  **“The mode of the object.”** (5 whitespace tokens)
- snapshot line **1812** → `<p>The type of the object (<span class='synopsis'><code>commit</code></span>,
  <span class='synopsis'><code>blob</code></span> or
  <span class='synopsis'><code>tree</code></span>).</p>` → rendered text
  **“The type of the object (commit, blob or tree).”** (9 whitespace tokens)

Lines 1807 and 1811 are `<dd>` open tags, which render to the empty string — the quotes do not
appear there. **Both quotes appear verbatim in the source, at the corrected lines; the page-line
pointers in the plan and contract are what is wrong.** The quote text itself needs no correction.
(A raw-bytes literal test differs between the two: "The mode of the object." is a literal
substring of the HTML, while "The type of the object (commit, blob or tree)." is not, because the
HTML wraps `commit`/`blob`/`tree` in `<span class='synopsis'><code>` elements. The second quote is
verbatim only after tag-stripping and entity-unescaping — state it as *rendered* text.)

**What S305 supports.** The source supports **listing semantics only**: a tree listing carries a
per-entry **mode** and a per-entry **type**. The doc's own `FIELD NAMES` section defines the two
interpolation fields the counter's derivation reads (`objectmode`, `objecttype`), and the doc
states at snapshot line 1754 that the **default** output format is equivalent to
`%(objectmode) %(objecttype) %(objectname)%x09%(path)` — which is the exact shape
`.ufo/evidence/round-86/measure.py:190-196` parses (`meta, path = line.split('\t', 1)` then
`mode, otype, oid = meta.split()`).

**What S305 does not support.** The page does **not** enumerate the octal modes: `grep -o
"1006[0-9][0-9]\|1007[0-9][0-9]"` over the snapshot returns nothing. The counter's
`REGULAR = ('100644', '100755')` boundary is therefore **not** grounded by S305 — that boundary is
separately held by **S291** (index-format: “Only 0755 and 0644 are valid for regular files.
Symbolic links and gitlinks have value 0 in this field.”). S305 grounds *that a mode and a type
are present per entry*; S291 grounds *which modes count as regular*. The lesson's claim that S305
"classifies a declared tool path as a regular blob" over-reaches: S305 classifies it as an entry
with a mode and a type; the regular-ness test is S291's. The source supports listing semantics
only, **not** the audit verdict policy, and **not** any execution-provenance claim.

### Admit / reject pair (proposed text)

**Admit:** S305 as the **re-opened listing-semantics source** for R86-C1 — no new row. The
re-fetch is byte-identical to the round-77 snapshot (same sha256), so the URL is already held; the
re-open adds the `objectmode`/`objecttype` field-name ground for the counter's expected-row
derivation. This is the round-77/round-79/round-82 re-open precedent (S305 was re-opened in
rounds 77, 79 and 82 without a new row).

**Reject:** a **second `git-ls-tree` row** — a within-scope duplicate of S305. Held-registry
check: `grep -c "^| S[0-9]* .*docs/git-ls-tree" corpus/SOURCES.md` → **1** (S305 only), so a
second row would be a second URL-holder for one document. **Flip:** a *distinct* document at a
*distinct* URL that states a rule S305 does not — e.g. the mode/type field table in a normative
spec (a `gitformat`/`index-format` class spec), which is a different URL carrying a different
rule, not a second git-ls-tree row.

### Assimilation

None. `merge/tameshi/MERGE-REPORT.md` and the newest `considerthese/2026-10-28.md` serve neither
frozen claim; no package row or knowledge entry is appended.

## Mistakes

| id | class | located evidence | captured-by | proposed disposition |
|---|---|---|---|---|
| **M1** | **inherited — a certification freeze without the criterion-111 cheat family** | round-85's frozen counter admitted a no-git/no-parser basename oracle at 8/8 (`.ufo/waves/round-85/w1/T85C1.md:29-43`; witness sha256 `0acb90acf7a659e1e16cb79090781eb2181bf9735c08b5fc382bc94a307f0ef2`); the round-85 closure rejected the certification. Verified inherited: at the r85 freeze `118dbc805d595d9de23a23adf036cec22df6436a` the tree holds `.ufo/evidence/round-85/measure.py` and **no** `controls/` directory at all (`git ls-tree -r --name-only 118dbc80 .ufo/evidence/round-85/` → one path), and `plans/round-85.plan.md` names only "Constant-success control" and "skipped-work base" — zero occurrences of fingerprint/sequence/pinned-hash | QUALITY **criterion 111**, which existed before that freeze | Round-86 executes the four cheat classes **plus** the r85 witness itself and commits their receipts **before** the freeze: fingerprint 0/8, sequence 4/8, pinned-hash 0/8, always-accept 0/8, r85-forgery 6/8 against the real instrument's 8/8. Retain r85's rejected verdict and counter unchanged. |
| **M2** | **defect in this round's own artifacts — off-by-one source-page line pointers** | `plans/round-86.plan.md` and `.ufo/evidence/round-86/contract.json` (`frontier_step.quotes`) carried "page lines 1807"/"1811"; the quotes are at snapshot lines **1808**/**1812**. Red-before receipt: the pointer fixture run against the committed snapshot at the claimed lines prints `POINTER mode: claimed_line=1807 rendered='' resolves=NO actual_physical_line=1808` and the same for type at 1811 → `POINTER_SUMMARY claimed_mode=1807 claimed_type=1811 actual_mode=1808 actual_type=1812 resolved=0/2`, exit 1. Lines 1807/1811 are `<dd>` tags and render empty | QUALITY **criterion 116** (every line/page pointer the round adds is re-resolved against the bytes; drifted pointers are listed) | Corrected to 1808/1812 in the working tree (`git diff` on both files shows exactly this change). The lesson body and `corpus/SOURCES.md:713-714` must carry the corrected lines too — **as of this read, `corpus/SOURCES.md` still says "page lines 1807 and 1811"** and must be corrected before landing. |
| **M3** | **defect in this round's own artifacts — source over-reach on the regular-blob boundary** | `corpus/lessons/round-86.md` `## Gate`: the source "is cited by R86-C1's expected-row derivation, which **classifies a declared tool path as a regular blob**". The git-ls-tree page enumerates no octal modes (`grep -o "1006[0-9][0-9]\|1007[0-9][0-9]"` → 0 hits); the 100644/100755 boundary is S291's ground | QUALITY **criterion 116**; the lane's own S291 row already records "the git-ls-tree page does not enumerate the octal modes" | Narrow the lesson sentence: S305 grounds that a listing carries a mode and a type per entry; the regular-ness test is S291's. Name S291 beside S305 in the Gate's sourced claim. |
| **M4** | **defect in this round's own artifacts — word-count on a quote that does not tokenise as declared** | The lesson records the second quote as "(10 words)"; the rendered quote "The type of the object (commit, blob or tree)." is **9** whitespace tokens (and 9 alphabetic words). The lane's own convention for a quoted passage counts whitespace tokens — S305's held row says "Recurse into sub-trees." (4 words) where the text is 4 tokens only if the hyphen splits, and r59's S289 quote was recorded as 17 while the text is 18 tokens | QUALITY **criterion 116** (the r59 word-count drift is the precedent that named it) | State the second quote as **9 words** (whitespace tokens), or state the counting convention explicitly alongside the number. First quote "The mode of the object." is 5 under every convention — unchanged. |

## Source curation delta (proposed)

| item | before | after |
|---|---|---|
| registry rows | 171 | **171** (no new row) |
| new source rows | — | **0** |
| tier additions | — | **0** |
| source-id reuse | — | **0** (next unused id after the round is **S312**; S311 is the highest held) |
| S305 status | `mined` | `mined` (unchanged) |
| S305 tier | A | A (unchanged) |
| S305 scope / anchor / `opened` / `recheck` | as written | unchanged (`opened` 2026-11-04, `recheck` 365d) |
| S305 `used-by` | `corpus/lessons/round-77.md, corpus/lessons/round-79.md, corpus/lessons/round-82.md` | **same three plus `corpus/lessons/round-86.md`** |

Only the `used-by` cell of the S305 row changes; the `git diff` shows exactly one table row
touched and exactly one cell within it. The round-86 note is appended to the log section of
`corpus/SOURCES.md` (append-only, per criterion 129's registry-row-without-its-round-entry rule:
the note and the `used-by` cell land in the same commit).

**Duplicate-refusal check (measured):** `grep -c "^| S[0-9]* .*docs/git-ls-tree"
corpus/SOURCES.md` → **1**. A second git-ls-tree row is refused.

**Census:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
exits **0** with the 19 standing warnings retained and the final
`tameshi ok …/corpus/SOURCES.md` line present. The round-86 `census-before.txt` and
`census-after.txt` are byte-identical (same md5) — expected, since the round appends no row and
changes no URL; note that the "after" census is only meaningful once the lesson file exists,
because a `used-by` path that does not resolve on disk is an E11.

## Verification fixture (proposed, reproducible)

`pointer-check.py` — resolves the two S305 page pointers against the committed snapshot bytes and
prints the rendered text at each claimed line, the physically located line, and whether the quote
is a literal raw-byte substring or only a rendered-text match.

```
$ python3 pointer-check.py --snapshot .ufo/evidence/round-86/sources/s305-ls-tree.html \
    --expect-mode 1807 --expect-type 1811
POINTER mode: claimed_line=1807 rendered='' expected='The mode of the object.' resolves=NO actual_physical_line=1808
POINTER type: claimed_line=1811 rendered='' expected='The type of the object (commit, blob or tree).' resolves=NO actual_physical_line=1812
POINTER_SUMMARY claimed_mode=1807 claimed_type=1811 actual_mode=1808 actual_type=1812 resolved=0/2
LITERAL mode: raw_substring_present=True
LITERAL type: raw_substring_present=False
EXIT=1

$ python3 pointer-check.py --snapshot .ufo/evidence/round-86/sources/s305-ls-tree.html \
    --expect-mode 1808 --expect-type 1812
POINTER mode: claimed_line=1808 rendered='The mode of the object.' ... resolves=yes actual_physical_line=1808
POINTER type: claimed_line=1812 rendered='The type of the object (commit, blob or tree).' ... resolves=yes actual_physical_line=1812
POINTER_SUMMARY claimed_mode=1808 claimed_type=1812 actual_mode=1808 actual_type=1812 resolved=2/2
LITERAL mode: raw_substring_present=True
LITERAL type: raw_substring_present=False
EXIT=0
```

The fixture is the red-before receipt for M2 and the green receipt for the corrected pointers.
It is not proposed as a standing lane tool. It is written to
`.ufo/waves/round-86/w1/T86S1-pointer-check.py`, with the captured transcript in
`.ufo/waves/round-86/w1/T86S1-pointer-receipts.txt`.

## Checks actually run by this seat

Every command below was executed; outputs are quoted verbatim in the seat report
`.ufo/waves/round-86/w1/T86S1.md`. No claim in this proposal rests on an unrun check.

1. `curl -sSL -D s305-live.headers -o s305-live.html https://git-scm.com/docs/git-ls-tree` —
   HTTP/2 200, 39083 B, sha256 `ff06fbc8…18267` (byte-identical to the committed snapshot), live
   quotes at lines 1808/1812.
2. `grep -n "The mode of the object\.\|The type of the object"` against both the committed
   snapshot and the live fetch — 1808 and 1812 in both.
3. `pointer-check.py` at 1807/1811 (red, exit 1) and at 1808/1812 (green, exit 0).
4. `git ls-tree -r --name-only 118dbc80 .ufo/evidence/round-85/` — one path; no `controls/`
   directory at the r85 freeze (M1 evidence).
5. `grep -c "fingerprint\|sequence\|pinned-hash" plans/round-85.plan.md` → 0 (M1 evidence).
6. sha256 of the r85 witness extracted from `T85C1.md` vs
   `.ufo/evidence/round-86/controls/ctl-r85-forgery.py` — both
   `0acb90acf7a659e1e16cb79090781eb2181bf9735c08b5fc382bc94a307f0ef2`, byte-identical (the
   contract's "byte-exact" claim holds).
7. `grep -o "passed=[0-9]/8 C1_R86_PASS=[a-z]*"` over the five control receipts — 0/8, 4/8, 0/8,
   0/8, 6/8; all `C1_R86_PASS=false` (matches the contract's control table).
8. `grep -c "^| S[0-9]* .*docs/git-ls-tree" corpus/SOURCES.md` → 1 (duplicate refusal).
9. `grep -o "1006[0-9][0-9]\|1007[0-9][0-9]"` over the snapshot → no hits (M3 evidence).
10. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0,
    19 standing warnings, final `ok` line.
11. `python3 -I tools/rekey-cost.py --edit corpus/SOURCES.md` →
    `REKEY_COST sections=71 planned=1 at_risk=13 predicted_lost=13` (matches the contract's
    `coldread_forecast`).
12. `git diff` over `corpus/SOURCES.md` → one table row touched, one cell within it (`used-by`).

## Out of scope for this seat

The C1 counter's discrimination, the C2 census predicate, the C2 manifest, the standing sweeps,
the admission verdict, and the rekey/settlement are other seats' and L1's. This seat did not
edit the lane repo, the fleet repo, or any sibling lane; made no mutating git/jj call; and did
not dispatch a subagent. The proposal file and this seat's report are the only files written.
