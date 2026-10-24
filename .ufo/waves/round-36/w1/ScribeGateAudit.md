# ScribeGateAudit — round-36 lesson Gate audit for S103 (w1)

**Verdict: PASS on the substantive Gate claim — snapshot bytes, digest, path, row shape and
used-by resolution all verify. FAIL on two calibration details of the lesson prose
(word count `19` vs actual `18`; `§DESCRIPTION first sentence` is a prefix, not the whole
sentence), and one adjacent receipt overclaim (the round-start census receipt does not exist
on disk). No frozen artifact was edited; the lane was read-only except for this report.**

## Artifacts audited (identity pinned)

| Artifact | Revision / hash |
|---|---|
| Lane HEAD at audit time | `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` |
| `corpus/lessons/round-36.md` | sha256 `da4d41e103c93a33be11a5307b32331bb8a99c5077bde0016209044698144a92` |
| `corpus/SOURCES.md` | sha256 `16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7` |
| `.ufo/evidence/round-36/src/s103-git-hash-object.html` | 29,933 bytes, sha256 `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100`, committed in `e423c41` |
| `.ufo/evidence/round-36/contract.json` | `new_source_row` matches the row and lesson digest byte-for-byte |

Scope: the `## Gate` section of the round-36 lesson, the S103 row of `corpus/SOURCES.md`, the
committed snapshot, and the `used-by` targets. C1/C2 evidence was not re-run (other seats own
those axes); the census clause of `## Gate` was checked only for receipt existence and the
row count it names.

## Per-check verdicts

| # | Check | Command (exact) | Observed | Verdict |
|---|---|---|---|---|
| 1 | URL claimed and consistent | `grep -n "S103" corpus/SOURCES.md`; lesson lines 31-32 | Both carry `https://git-scm.com/docs/git-hash-object` | PASS (see caveat C5) |
| 2 | Access date 2026-10-24 UTC | `stat -c '%y' <snapshot>`; `git log -1 --date=iso-strict -- <snapshot>` | mtime `2026-10-24 03:03:35 -0300` = `06:03:35Z`; commit author `2026-10-24T02:50:40-03:00` = `05:50:40Z`; register `2026-10-24` | PASS (corroborated, not network-logged) |
| 3 | Snapshot path committed | `git ls-files --error-unmatch .ufo/evidence/round-36/src/s103-git-hash-object.html`; `git log --oneline -1 -- <snapshot>` | tracked; last touched by `e423c41`; working tree clean for that path | PASS |
| 4 | sha256 `dd826dae…` | `sha256sum <snapshot>` | `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100` | PASS (exact) |
| 5 | Byte count 29,933 | `wc -c < <snapshot>` | `29933` | PASS |
| 6 | Quote ≤ 25 words | `python3` tokenize of the lesson quote | 18 words | PASS (cap held) |
| 7 | Quote verbatim in snapshot (tags stripped) | tag-strip + whitespace-normalize (below) | present at offset 2259 of the stripped stream, immediately after the `DESCRIPTION` heading, inside the single `<p>` of `§DESCRIPTION` | PASS (whitespace-normalized only — C5) |
| 8 | SOURCES row well-formed | `python3` column parse against the table header | 11/11 cells; unique id; tier `A` ∈ {A,B,C}; status `mined` ∈ {mined,queued,rejected}; opened `2026-10-24`; recheck `365d` | PASS |
| 9 | `used-by` paths exist | `os.path.exists` on both cells | `.ufo/evidence/round-36/coldread/refresh-receipts.json` ✔; `corpus/lessons/round-36.md` ✔ | PASS |
| 10 | `used-by` paths actually cite S103 | `grep -n "S103" refresh-receipts.json`; `grep -n "S103" corpus/lessons/round-36.md` | 4 `cited_source` cites + `"cited_source_row": "S103"` in the receipts; Gate entry in the lesson | PASS |
| 11 | Row accounting `99 → 100` | `git show 796e08b:corpus/SOURCES.md \| grep -c '^| S[0-9]'`; `grep -c '^| S[0-9]' corpus/SOURCES.md` | 99 at `796e08b`; 100 at HEAD; `| S103` is the last id | PASS |
| 12 | Word-count claim `(19 words)` | same as #6 | 18 words | **FAIL** (F1) |
| 13 | Attribution `§DESCRIPTION first sentence` | stripped region readback | quoted fragment is the sentence's opening 18 words; the sentence continues `… (which can be outside of the work tree), and optionally writes the resulting object into the object database.` | **FAIL as wording** (F2) |
| 14 | `Gate` census `both receipts kept` | `grep -rl "CENSUS_EXIT" .ufo/evidence/` | exactly one file: `.ufo/evidence/round-36/after/census-at-b455001e.exit` | **FAIL** (F3) |

### Exact quote-verification code (checks 6-7)

```
F=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/src/s103-git-hash-object.html
python3 - "$F" > /fast/scratch/hyaku/tameshi-r36-seats/ScribeGateAudit/stripped.txt <<'EOF'
import sys, re, html
raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
s = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
s = re.sub(r"(?s)<[^>]+>", " ", s)
s = html.unescape(s)
s = re.sub(r"[ \t\r\f\v]+", " ", s)
s = re.sub(r"\n\s*\n+", "\n", s)
print(s)
EOF
# lesson quote extracted mechanically from round-36.md, whitespace-collapsed:
#   "Computes the object ID value for an object with specified type with the contents of the named file"
# result: snapshot-normalized contains quote = True; 18 tokens; offset 2259;
#         preceding text ends "... [--no-filters] DESCRIPTION"
# strict substring without whitespace normalization: False (both the HTML paragraph
# and the markdown line are hard-wrapped at different columns)
```

## Findings

- **F1 — word-count claim off by one.** Lesson `## Gate` says the quote is `(19 words)`; it is
  18. The `≤25` cap is unaffected. The SOURCES row carries no word count, so the row is clean.
- **F2 — attribution imprecision.** The quote is an 18-word prefix of the `§DESCRIPTION` first
  sentence, not the whole sentence (which runs to `… into the object database.`). Both the
  lesson (`§DESCRIPTION first sentence`) and the SOURCES `anchor` cell say "first sentence";
  the quoted span never misstates the manual (`Computes … named file` is contiguous and
  unedited), so this is citation precision, not misquotation.
- **F3 — receipt overclaim in `## Gate`.** "Census: round start (tip `796e08b`) … 99 rows;
  round end (refresh commit) … 100 rows — both receipts kept under `.ufo/evidence/round-36/`".
  Only the round-end receipt exists (`after/census-at-b455001e.{exit,stdout}`, exit 0, plus
  `after/sources-rows-at-b455001e.txt` = `100`). No `796e08b` census receipt exists anywhere
  under `.ufo/evidence/` (`find … -iname "*census-at-796e08b*"` empty; `grep -rl CENSUS_EXIT`
  returns one file). The 99 figure itself is independently reproducible (check 11), so the
  *number* holds while the *retention* claim does not. `LOG.md:1936` repeats the same claim.
- **F4 — register is self-referential about its contract (pre-existing).** `corpus/SOURCES.md:4`
  cites `SOURCES-CONTRACT-v1.md`; that file is absent from the lane and
  `git log --all -- '*SOURCES-CONTRACT*'` is empty — it was never committed. Row
  well-formedness was therefore judged against the table header itself (11 columns) and the
  vocabularies in use. This is the same `reference-drift` class the round repaired for `LOG.md`
  (criterion 72), surfacing one file over; not introduced by round 36.

## Caveats (not scored as failures)

- **C5 — URL↔snapshot binding is content-based, not cryptographic.** The snapshot carries no
  `<link rel="canonical">`, no `og:url`, and no self URL string. Identity rests on
  `<title>Git - git-hash-object Documentation</title>`, AsciiDoc anchors
  (`Documentation/git-hash-object.txt--tlttypegt`), and the manual body (`SYNOPSIS`,
  `--stdin`, `--literally`). The `curl exit 0` line is lesson-asserted; no fetch log or
  `curl -w '%{url_effective}'` capture was committed. A future fetch could record the
  effective URL alongside the digest.
- **C6 — the row's primary consumer does not repeat the digest.** `refresh-receipts.json` cites
  S103 four times in prose (`cited_source`) plus `"cited_source_row": "S103"`, but
  `grep dd826dae refresh-receipts.json` is empty: the digest `dd826dae…` appears in exactly
  three files (lesson, SOURCES row, contract). The claimed "byte-identity discipline" is
  therefore cited, not exercised, at that consumer. The binding lesson↔bytes still verifies
  (check 4), so provenance is intact; it is the receipts that stay digest-free.
- The row is 11 content cells — `awk -F'|'` reports `NF=13` because of the two edge fields; not
  a conflict with sibling `MTSourcesRow.md`'s `NF=13` pristine description.

## Notes

- Read-only throughout; the only lane write is this report. No git/jj mutation, no `pacman`,
  no tool installs or upgrades required, no subagents dispatched.
- Scratch: `/fast/scratch/hyaku/tameshi-r36-seats/ScribeGateAudit/stripped.txt` (tag-stripped
  snapshot text used for checks 6-7).
- Out of scope by assignment: C1 counter re-run, C2 v2 deciding run, monitor scores, and the
  wave-prep (78 seat) itemization. Cross-checks that did run here are limited to the S103 row,
  its snapshot, and the census row count named in the same Gate section.
