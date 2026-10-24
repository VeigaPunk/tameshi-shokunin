# ReviewSourcesFrontier — Sources & frontier conformance (round 36, w1)

**Seat.** Reviewer, leaf (read-only), axis: calibration. No production edits. Only this
report was written; scratch is under
`/fast/scratch/hyaku/tameshi-r36-seats/ReviewSourcesFrontier/`. Tool installs: none.

**Target.** The round-36 frontier claims on `corpus/SOURCES.md`: rows 99→100, S103 the
only addition, S103 opened this round (snapshot dated 2026-10-24), at least one claim
citing S103 (refresh receipts or lesson), and S103's `tier`/`kind`/`status` against the
contract enums. Contract basis: `SOURCES-CONTRACT-v1.md` (kaika, 2026-10-19) — the lane's
cited copy is not committed, so the fleet copy
`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` and the fleet
validator `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`) were used as
the authoritative enums.

**Revisions reviewed.** `796e08b` (r35 tip = round-start tip), `e423c41b` (content
commit: S103 row + round-36 lesson), `b455001e` (refresh/measurement commit: refresh
receipts), `d9c496b` (receipts commit, current HEAD).

**Verdict: PASS on the frontier claim.** Rows 99→100, S103 the only addition, opened
2026-10-24, cited by both `refresh-receipts.json` and `corpus/lessons/round-36.md`,
`kind=docs` / `tier=A` / `status=mined` all inside the contract enums, census exit 0 at
the reviewed bytes. One minor calibration finding (F1) and two low/trivial notes (F2, F3).

## Findings (by severity)

### F1 — MINOR (calibration): the round-start census receipt named by the round record does not exist

`corpus/lessons/round-36.md:48-50` says:

> `- Census: round start (tip `796e08b`) `sources-census.sh validate` exit 0, 99 rows;
> round end (refresh commit) exit 0, 100 rows — both receipts kept under
> `.ufo/evidence/round-36/`.`

`LOG.md:1936-1937` repeats the same claim. Only the round-end artifacts exist:

- `.ufo/evidence/round-36/after/census-at-b455001e.stdout` (10 lines: 8×W04, 1×W01 S101,
  one `tameshi ok …` line) and `.exit` = `CENSUS_EXIT=0`;
- `.ufo/evidence/round-36/after/sources-rows-at-b455001e.txt` = `100\n` (a bare number, no
  generating command recorded);
- `find /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence -iname '*census*796*'`
  → empty; `grep -rl CENSUS_EXIT .ufo/evidence/round-36/` → only
  `after/census-at-b455001e.exit`.

Mitigation, and why the *numbers* still hold: the 99-row registry at `796e08b` is the same
blob (`f85c02e76b0994477df7ded8d95585d260885f2d93fbeb91e57deb358d7855fe`) as the r35 end
commit `5df962b`, whose end census receipt
`.ufo/evidence/round-35/after/census-at-round-end.stdout` exits 0; and both counts are
directly re-derivable (see commands 1–3 below: 99 at `796e08b`, 100 at `e423c41b`,
`b455001e` and `HEAD`). Also note `validate` mode prints no row count at all — the "100"
in the lesson is not in the cited census stdout either; it is the separate bare file plus
my own `census`-mode run (`rows 100`).

Recommendation: append-only correction in the round record (lesson erratum or LOG
correction) naming the receipts that actually exist and attributing 99/100 to the
re-derivable count command; do not edit the S103 row (rule 2, append-only). This is the
same defect independently reported by `ScribeGateAudit` F3 (`w1/ScribeGateAudit.md:74-79`).

### F2 — LOW (evidence ordering): S103's `used-by` forward-references the refresh receipts by one commit

S103 became `mined` at `e423c41b`, but one of its two `used-by` paths,
`.ufo/evidence/round-36/coldread/refresh-receipts.json`, first exists at `b455001e`
(`git cat-file -e e423c41b:.ufo/evidence/round-36/coldread/refresh-receipts.json` →
missing; exists at `b455001e`). Validated on an extracted scratch tree, the contract's
E11 rule fires at the content commit and not at the refresh commit:

- `e423c41b` tree: `file	E11	S103 missing used-by .ufo/evidence/round-36/coldread/refresh-receipts.json`
- `b455001e` tree: no `S103` line (E11 clean for the row; the other 115 E11s in the scratch
  run are unrelated used-by paths not materialized in the scratch copy).

`status=mined` is still supported at the writing commit because the second path,
`corpus/lessons/round-36.md`, exists at `e423c41b` and names S103. At the round-end /
measurement commit `b455001e` both paths resolve, so the frontier claim is clean where it
is evaluated. Secondary note: the contract defines `used-by` as "knowledge entries or
lessons"; a JSON evidence file is a wider reading (precedent: S102 lists
`tools/tally-audit-v3.py`), not a round-36 regression.

### F3 — TRIVIAL (citation precision): the Gate quote is 18 words, not 19, and is a prefix of the first sentence

`corpus/lessons/round-36.md:43-44` calls the quote "(19 words)"; it is 18 tokens. The
quoted span is contiguous and unedited but stops at "named file" while §DESCRIPTION's
first sentence continues "(which can be outside of the work tree), and optionally writes
the resulting object into the object database." Both the lesson and the row's `anchor`
say "first sentence"; the quote is its first 18 words. The contract's ≤25-word cap and
location requirement are satisfied; strict HTML substring is false only because the
snapshot hard-wraps at "type\nwith", and the whitespace-normalized substring is present
(offset 16241, immediately after the DESCRIPTION heading). Same observation as
`ScribeGateAudit` F1/F2; no row change needed.

## Confirmations (what holds, with evidence)

- **Rows 99→100, S103 only.** Contract row regex at `796e08b` → 99; at `e423c41b`,
  `b455001e`, `HEAD` → 100. Sorted id-set difference `796e08b`→`b455001e` is exactly
  `> | S103` (no removals, no other id). `git diff --numstat 796e08b e423c41b --
  corpus/SOURCES.md` = `3 1` (S103 row + blank line; `Next unused id` S103→S104). The
  refresh commit does not touch SOURCES.md (`git diff --stat e423c41b b455001e` and
  `b455001e HEAD` → empty), and the file is byte-identical at `e423c41b`/`b455001e`/`HEAD`
  (blob `e67cbf03…`, sha256 `16fae0a1…`).
- **S103 opened this round.** Row `opened=2026-10-24`; snapshot committed at `e423c41b`
  (`git log --all -- .ufo/evidence/round-36/src/s103-git-hash-object.html` → `e423c41b`
  plus three non-ancestor duplicate commit objects with identical content); file mtime
  `2026-10-24 03:03:35 -0300`; 29,933 bytes; sha256
  `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100`, matching the row and
  `contract.json`. `git grep -n 'S103' 796e08b -- .` finds only `- Next unused id: S103.`
  — no prior row.
- **Citation.** `git show b455001e:.ufo/evidence/round-36/coldread/refresh-receipts.json`
  contains `S103` 5× (4 `cited_source` + `round36_provenance.cited_source_row`); `git show
  e423c41b:corpus/lessons/round-36.md` contains it 2× (Gate bullet; "Rows: 99 → 100 (S103
  only)"). H4 id-in-used-by check on the live tree: no `no-id-cite` output for S103 (the
  `no-id-cite` lines printed for S031–S037 are pre-existing, unrelated rows). E11 clean at
  `b455001e`; both used-by paths exist there.
- **Enums.** Contract §Census on the exact `b455001e` blob (extracted, sha256
  `16fae0a1…`): `rows=100`, malformed `0`, enum/tier-inflation output empty, duplicate ids
  empty, `NF=13`. S103 fields: `id=S103 kind=docs tier=A status=mined opened=2026-10-24
  recheck=365d`; `docs` ∈ kind enum, `A` ∈ tier enum (official Git docs — primary for its
  own semantics; not `community`, no E10), `mined` ∈ status enum, `365d` a valid cadence.
  Row sits inside `## Registry` (lines 8–116), not E12; URL `git-scm.com/docs/git-hash-object`
  occurs once (no E04 duplicate); `Next unused id: S104`.
- **Quote grounding.** Snapshot `s103-git-hash-object.html:1604-1610` is the DESCRIPTION
  section; the quoted sentence at 1607-1608 reads "Computes the object ID value for an
  object with specified type / with the contents of the named file (which can be outside
  of the work tree)…". Live fetch today: `HTTP=200 final=https://git-scm.com/docs/git-hash-object`.
- **Census.** `TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
  --root /home/vgpnk/Projects/shokunin --today 2026-10-24 tameshi` → exit 0, only
  pre-existing W04×8 + W01 S101; `census` mode → `tameshi rows 100`, `tier.A 90 tier.B 7
  tier.C 3`, `status.mined 72 status.queued 22 status.rejected 6`, `missing 0`. This
  independently reproduces the end-state validation (the committed receipt's warning set
  matches line-for-line).
- **No row flips.** The only SOURCES.md change in round 36 is the S103 row plus the
  append-only `Next unused id` footer; no existing row's `status`/`recheck`/`used-by` was
  edited.

## Exact commands run (read-only; lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless noted)

```sh
# 1. cardinality and delta
git show 796e08b:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'   # 99
git show e423c41b:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  # 100
git show b455001e:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  # 100
git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'      # 100
diff <(git show 796e08b:corpus/SOURCES.md | grep -oE '^\| S[0-9]{3,}' | sort) \
     <(git show b455001e:corpus/SOURCES.md | grep -oE '^\| S[0-9]{3,}' | sort)            # 99a100 > | S103
git diff --numstat 796e08b e423c41b -- corpus/SOURCES.md                                 # 3  1
git diff --stat e423c41b b455001e -- corpus/SOURCES.md ; git diff --stat b455001e HEAD -- corpus/SOURCES.md  # empty

# 2. exact-bytes enum / shape census on the b455001e blob (scratch extraction, sha256 16fae0a1…)
git show b455001e:corpus/SOURCES.md > /fast/scratch/hyaku/tameshi-r36-seats/ReviewSourcesFrontier/SOURCES-b455001e.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' SOURCES-b455001e.md   # 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 { ... tier/status/kind enums ... }' SOURCES-b455001e.md  # empty
awk -F'|' '/^\|[[:space:]]*S103[[:space:]]*\|/ { ... }' SOURCES-b455001e.md               # docs / A / mined / 2026-10-24 / 365d

# 3. snapshot identity and quote grounding
sha256sum .ufo/evidence/round-36/src/s103-git-hash-object.html                             # dd826dae…
stat -c '%s %y' .ufo/evidence/round-36/src/s103-git-hash-object.html                      # 29933 2026-10-24 03:03:35 -0300
grep -n -i -A6 -B2 'DESCRIPTION' .ufo/evidence/round-36/src/s103-git-hash-object.html      # headings 1604; quote 1607-1608
curl -sS -o /dev/null -w 'HTTP=%{http_code} final=%{url_effective}\n' -L https://git-scm.com/docs/git-hash-object  # HTTP=200

# 4. citation at the two relevant commits
git show b455001e:.ufo/evidence/round-36/coldread/refresh-receipts.json | grep -c 'S103'  # 5
git show e423c41b:corpus/lessons/round-36.md | grep -c 'S103'                             # 2
git cat-file -e e423c41b:.ufo/evidence/round-36/coldread/refresh-receipts.json            # missing
git cat-file -e b455001e:.ufo/evidence/round-36/coldread/refresh-receipts.json            # exists
git cat-file -e e423c41b:corpus/lessons/round-36.md                                       # exists

# 5. census re-run (read-only) and receipt search
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin --today 2026-10-24 tameshi                          # exit 0
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
  --root /home/vgpnk/Projects/shokunin --today 2026-10-24 tameshi                          # rows 100, missing 0
grep -rl CENSUS_EXIT .ufo/evidence/round-36/                                               # only after/census-at-b455001e.exit
find .ufo/evidence -iname '*census*796*'                                                   # empty
xxd .ufo/evidence/round-36/after/sources-rows-at-b455001e.txt                              # "100\n"

# 6. transient E11 at the content commit (scratch trees under the seat scratch dir)
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file /fast/scratch/.../e423c41b-tree/corpus/SOURCES.md --today 2026-10-24              # E11 S103 missing …refresh-receipts.json
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file /fast/scratch/.../b455001e-tree/corpus/SOURCES.md --today 2026-10-24              # no S103 error

# 7. r35-end coverage of the same 99-row bytes
git show 5df962b:corpus/SOURCES.md | sha256sum                                             # f85c02e7… = 796e08b blob
cat .ufo/evidence/round-35/after/census-at-round-end.stdout                                 # warnings + ok, exit 0
```

## Residual risk and verification gaps

- **No LSP path.** This seat's toolset exposes no `lsp` device/server, and the artifact is
  Markdown; caller/definition/diagnostics checks do not apply. Semantic conformance was
  judged with the contract's own validator (`scripts/sources-census.sh`, sha256
  `3fb72615…`) plus git object reads; literal `grep` was used only for id naming
  (`S103`), never as a substitute for the validator.
- **Fetch moment not independently witnessed.** The lesson's "curl exit 0" has no
  committed fetch log; the committed snapshot's digest binds the bytes that exist, and the
  live URL resolves 200 now, but the fetch itself is lesson-asserted (sibling
  `ScribeGateAudit` C5).
- **Citation is nominal in the receipt.** `refresh-receipts.json` names S103 in prose but
  does not repeat the snapshot digest `dd826dae…` (it appears only in the row, lesson and
  contract — sibling `ScribeGateAudit` C6). The lane requirement "names S103" is met, and
  the lesson carries the located quote.
- **SCORECARD count restatement.** The live standing cell still reads "99 rows at round
  35" (`SCORECARD.md:1609`, historically scoped, not false); the round-36 block records
  "Frontier: S103 opened and mined" without restating 100. The 100 figure lives in
  LOG/lesson and is re-derivable; no contradiction, but no round-36 standing-count cell
  either.
- **Duplicate commit objects.** `git log --all` shows non-ancestor duplicate commit objects
  (`3cbd764`, `6632275`, `ef37d72`) carrying the same S103 row/snapshot; they are not in
  the canonical history, so this is not id reuse. `e423c41b` is the only canonical commit
  that writes S103.

**Verdict line:** `PASS — Sources & frontier conformance holds (99→100, S103 only, opened
2026-10-24, cited by refresh-receipts.json + lesson, docs/A/mined valid, census exit 0);
one MINOR calibration repair recommended (F1: missing round-start census receipt /
count-attribution in the lesson and LOG), plus LOW/TRIVIAL notes F2 (one-commit forward
used-by reference) and F3 (18-vs-19-word quote precision).`
