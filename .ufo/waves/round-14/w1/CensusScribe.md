# CensusScribe — tameshi round 14, w1 source census (read-only)

Seat: `TameshiR14.CensusScribe` (leaf, no delegation). Scope: `corpus/SOURCES.md` row census, the census contract, and a suggested mutable ledger and own-work row policy. No census gate execution (`scripts/sources-census.sh` was read, not run). No edits to any repo file. No tools installed or updated.

## Inputs read

- `corpus/SOURCES.md` (baseline bytes at `d6809df7775338f000e44c8a916067b8866867fb`; working tree identical at first read)
- `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` at fleet root (frozen contract; the census section is what the contract calls "run from the lane root")
- `scripts/sources-census.sh` at fleet root (fleet gate; read for E/W-code semantics only)
- `AGENTS.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/lessons/round-13-verifier-spotcheck.md`, `.ufo/waves/round-14/spec.json`, `.ufo/waves/round-14/w1/swarm-registry.json`

Method: static parsing of bytes in an in-process Python session (rows = Registry-section table lines with 0–3 leading spaces and an `S[0-9]{3,}` id, mirroring the script's `row_pass` rules), plus read-only `git show` / `cat-file` on named commits and `test -e` on used-by paths.

## 1. Baseline census (initial rows, from bytes at d6809df)

| Observable | Value |
|---|---|
| SOURCES.md bytes / sha256 | 32539 / `382524762dcfe0dab91fe77df776433ede058b994537e649a3474d134cde36de` |
| Registry rows | 46 (all NF=13; malformed 0) |
| Duplicate ids | 0 |
| Id gaps | S038, S039 (retired, per Id allocation prose) |
| Next unused id (prose) | S049 |
| Tier A / B / C | 39 / 5 / 2 |
| Status mined / queued / rejected | 19 / 24 / 3 |
| Kind | paper 17, docs 12, code 10, spec 2, community 2, book 1, tool 1, own-work 1 |
| Mined rows whose used-by paths are missing on disk | 0 |
| Anchors without a revision marker (`@`, fetched/accessed, arXiv, Abstract, version, date, hash) | 0 |
| Rejected rows matching `REJECTED: … ; flip: …` | 3 / 3 |
| `supersedes` targets | S047→S041, S048→S047; both exist |
| Same-URL groups | pitest.org/…/incremental_analysis = S041, S047, S048 (different scopes; W04 only) |
| Community at tier A | 0 |

These agree with the round-13 closure's recorded 46 / 39-5-2 / 19-24-3 observations.

Baseline row table (`id | kind | tier | status | opened | recheck | used-by count`):

| id | kind | tier | status | opened | recheck | used-by # |
|---|---|---|---|---|---|---|
| S001 | docs | A | mined | 2026-10-19 | 180d | 1 |
| S002 | spec | A | mined | 2026-10-19 | on-release | 1 |
| S003 | docs | A | mined | 2026-10-19 | 180d | 1 |
| S004 | docs | A | mined | 2026-10-19 | on-release | 2 |
| S005 | code | A | mined | 2026-10-19 | on-release | 1 |
| S006 | code | A | mined | 2026-10-19 | 90d | 3 |
| S007 | paper | A | queued | 2026-10-19 | 365d | 0 |
| S008 | paper | A | queued | 2026-10-19 | 365d | 0 |
| S009 | paper | A | queued | 2026-10-19 | 730d | 0 |
| S010 | paper | A | queued | 2026-10-19 | 730d | 0 |
| S011 | paper | A | mined | 2026-10-19 | 730d | 1 |
| S012 | paper | B | queued | 2026-10-19 | 90d | 0 |
| S013 | docs | A | queued | 2026-10-19 | on-release | 0 |
| S014 | docs | A | queued | 2026-10-19 | on-release | 0 |
| S015 | docs | A | queued | 2026-10-19 | 365d | 0 |
| S016 | code | A | queued | 2026-10-19 | 365d | 0 |
| S017 | docs | A | queued | 2026-10-19 | on-release | 0 |
| S018 | docs | A | queued | 2026-10-19 | on-release | 0 |
| S019 | paper | A | queued | 2026-10-19 | 730d | 0 |
| S020 | paper | A | queued | 2026-10-19 | 365d | 0 |
| S021 | paper | A | queued | 2026-10-19 | 180d | 0 |
| S022 | paper | A | queued | 2026-10-19 | 730d | 0 |
| S023 | code | A | queued | 2026-10-19 | 90d | 0 |
| S024 | book | B | queued | 2026-10-19 | 365d | 0 |
| S025 | paper | A | queued | 2026-10-19 | 730d | 0 |
| S026 | docs | A | mined | 2026-10-19 | 730d | 1 |
| S027 | paper | A | queued | 2026-10-19 | 180d | 0 |
| S028 | spec | A | mined | 2026-10-19 | 365d | 1 |
| S029 | tool | C | rejected | 2026-10-19 | 180d | 0 |
| S030 | paper | B | rejected | 2026-10-19 | 365d | 0 |
| S031 | own-work | A | mined | 2026-10-19 | 90d | 12 |
| S032 | code | A | mined | 2026-10-19 | 180d | 3 |
| S033 | code | A | mined | 2026-10-19 | 180d | 2 |
| S034 | code | A | mined | 2026-10-19 | 180d | 4 |
| S035 | code | A | mined | 2026-10-19 | 180d | 2 |
| S036 | code | A | mined | 2026-10-19 | 180d | 1 |
| S037 | code | A | mined | 2026-10-19 | 180d | 1 |
| S040 | paper | B | queued | 2026-10-19 | 730d | 0 |
| S041 | docs | A | mined | 2026-10-19 | 90d | 1 |
| S042 | paper | A | queued | 2026-10-19 | 730d | 0 |
| S043 | paper | A | queued | 2026-10-19 | 730d | 0 |
| S044 | paper | A | queued | 2026-10-19 | 365d | 0 |
| S045 | community | B | queued | 2026-10-19 | 365d | 0 |
| S046 | community | C | rejected | 2026-10-19 | 90d | 0 |
| S047 | docs | A | mined | 2026-10-20 | 90d | 1 |
| S048 | docs | A | mined | 2026-10-20 | 90d | 1 |

## 2. In-flight change observed (not authored by this seat)

Between my first read and a later re-read, another round-14 seat appended **S049** (Python subprocess environment mapping; docs; tier A; mined; opened 2026-10-20; recheck on-release; used-by `corpus/lessons/round-14.md`), and the Id allocation now reads "Next unused id: S050". Current bytes: 33590 bytes, sha256 `39b44271199d2aacf88965508d67b3f1d0728c06f1895f18b7e9dd5eb22be204`, `git status` = modified. Current counts: 47 rows, NF=13 for all, tier A/B/C 40/5/2, status mined/queued/rejected 20/24/3.

Observed risk: at re-read, `corpus/lessons/round-14.md` did not exist on disk, so S049's used-by is dangling. Any validate run before that lesson lands fails E11 for S049. I did not change it.

## 3. Mutable-field drift (used-by), static evidence

Contract Rule 2 says used-by lists the knowledge entries or lessons citing a row. Text mentions in `corpus/knowledge/*.md` and `corpus/lessons/*.md` that are absent from used-by include:

- **S048** (mined): `corpus/knowledge/fleet-kill-rate-ledger.md:374` cites "source method: S003 and S048" — a real citation, not listed.
- **S003** (mined): the same ledger line, plus round-13 lessons; not listed.
- **S041, S047, S048** (mined): cited in round-13 lessons; not listed.
- **S004, S011, S026, S028** (mined): cited in round-12 lessons; not listed.
- **S031**: the used-by list has 12 entries, but three knowledge files cite S031 without listing it.
- **S032–S037** (fleet gates, mined): their used-by knowledge entries do not contain the S-id. The contract does not require that, so this is a note, not a drift.

Queued rows are cited in `corpus/README.md` and round-1 lessons as Paths or lead lists. Those are not used-by citations, and queued rows correctly have used-by `—`.

## 4. Census-script coverage versus the contract (static read)

Not run. Gaps relative to the contract as written:

1. Next-unused-id and id-gap accounting are not checked (prose only).
2. E04's exemption is `teaches !~ /supersedes S[0-9]{3}/`. It matches anywhere in teaches, not only when teaches opens with `supersedes`. It does not check that the target exists. Current targets exist.
3. W02 checks only that teaches has at least 8 characters. It does not check the `REJECTED: …; flip: …` shape. Current rows comply.
4. Anchor revision markers are not checked. Current anchors all carry one.
5. Append-only discipline (only status, recheck, used-by change; each change logged old→new) needs a baseline diff. A single-snapshot validate cannot detect it.
6. used-by reciprocity (a citing file absent from used-by) is not checked.
7. `opened` is checked against `--today`. S047, S048 and S049 are opened 2026-10-20. Any run with `--today 2026-10-19` fails E08. L1 must pass the actual UTC date.

## 5. Suggested source mutable ledger (proposal; no new file)

Keep one source of truth. Do not add a parallel ledger file.

- Record each in-place change to status, recheck or used-by in the round lesson's `## Gate` as a table: `| id | field | old | new | round | reason |`. This is contract Rule 2 as written.
- For round 14, the required transitions are the used-by reconciliation in §3, plus S049's dangling used-by once the lesson lands. Append them only if the owning seat judges them citations.
- If a mechanical check is wanted, a read-only checker could diff `git show d6809df:corpus/SOURCES.md` against the working tree and require: no row removed; all non-mutable cells unchanged; every changed status, recheck or used-by matched by a transition row. That is a new checker. Route it to the fleet-gate owner. This seat does not build it.

## 6. Suggested own-work row policy (proposal; no schema change)

No new kind value. `own-work` stays in the contract enum; E05 already accepts it.

- `kind: own-work` is only for artifacts in this repo: `tools/…` and committed `.ufo/evidence/…`. Never a sibling repo's gate. Sibling gate code stays `kind: code` (S032–S037 pattern).
- Anchor must give path:line range, a commit that exists (`git cat-file -t`), and the blob sha256 at that commit. A changed blob needs a new row, not an in-place anchor edit.
- Tier A only when a committed command reproduces the output. Otherwise the artifact is not a source row; put it in knowledge with its own provenance.
- `teaches` names the scope of what the output proves. Not a fleet-wide verdict.
- `opened` is the date the row author re-read the output. Recheck `on-release` if tied to a commit, else 90d.
- Evidence must be copied under `.ufo/evidence/…` before the row cites it (QUALITY criterion 9). `/tmp` is not an anchor.
- Mined requires used-by paths that exist and that name the row.

Current compliance, S031 (only own-work row): anchor `tools/mutate-and-run.sh:80-89 @ 4eb4cf3` — commit exists; `git show 4eb4cf3:tools/mutate-and-run.sh` sha256 = `75ed934d…adc5`, matching the anchor and the HEAD blob. Its six legs are described in lines 80–89 with the expected kill rates. I did not re-verify the embedded defect specs.

Sibling anchors S032–S037: commits `175de6b`, `fecee87`, `165307f`, `eead56b` exist in the sibling repos. I checked commit existence only, not the recorded blob sha256 values.

## 7. Risks

- S049 dangling used-by until `corpus/lessons/round-14.md` exists (E11).
- A validate run with a stale `--today` fails E08 for S047–S049.
- used-by under-reporting (§3) is judgement-dependent: text mention is not citation.
- W04 duplicates for S041/S047/S048 are intentional and will repeat on every validate run; they do not fail it.
- The E04 supersedes exemption is substring-based (§4.2). No current row exploits it.
- Freshness: S032–S037 anchors pin 2026-10-19 sibling commits; any later sibling change cannot be read from this lane. Recheck cadence is 180d; nothing is overdue on 2026-10-20.

## Changes recommended (for owners; none applied by this seat)

1. Reconcile used-by for S003, S048 (and S041, S047 if the round-13 lesson counts as a citation) with a transition row in the round-14 lesson.
2. Land `corpus/lessons/round-14.md` before any validate that includes S049, or revert the S049 used-by until then.
3. Adopt the mutable-ledger rule in §5 and the own-work policy in §6 as text in the round-14 lesson, not as new files.

## Checks L1 should run after all seats finish

- Contract census commands (SOURCES-CONTRACT-v1, lane root): row count, NF≠13 count (expect 0), duplicate ids (expect none), tier/status histograms, enum violations (expect none), mined used-by missing (expect none). Expected post-S049: 47 rows, 40/5/2, 20/24/3, given the current bytes.
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi --today <actual UTC date>` — expect exit 0 with W04 only for S041/S047/S048. This is the one gate execution; run it once, after the lesson exists.
- Confirm `git diff d6809df -- corpus/SOURCES.md` shows only appended S049 and the Id allocation line, with no changes to existing rows except any logged transitions.

## Verdict

Baseline registry is structurally clean against the contract's shape rules and the census's E-code rules. Round-14 work adds S049, which is clean except for its used-by path not yet existing. The gaps are in used-by reconciliation and in checks the script does not perform, not in the rows' tiers or statuses.
