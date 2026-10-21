# S001 — bounded source re-open for round-19 calibration (scout `TameshiR19-2.SourceS001`, advisory)

Accessed 2026-10-21 (page fetch 2026-10-21T05:50:03Z). Frozen baseline
`7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`. This report covers the C1 source and
no-harm boundary only. It is advisory and does not close anything.

## Verdict

- **Use, narrowly and unchanged:** S001 is still a valid tier-A anchor for the S001
  citations that round-19 metadata sweeps touch: `mutation-case-kumitate-sources-check.md:1`
  (descriptor) and `:90` (formula). It is also one of the five row IDs in the R18-3 line count.
  The page bytes match the round-1 retained body exactly, so there is no drift.
- **Reject as evidence for C1 itself:** do not use S001 for the 0/5 → 5/5 durable-correction
  count, or for any receipt or metadata rule (R18-1, R18-4, R18-5; working-copy QUALITY 37 and 39).
  S001 defines Stryker's mutant states and mutation score. It says nothing about receipts, argv,
  exit codes, revision binding, `verified-at:` currency or calibration. If its `detected / valid`
  were turned into a "correction score", that would be an invented score.
- **Registry:** no change recommended. Each cell was re-checked below.

## Registry row (observed)

`corpus/SOURCES.md:12`: S001 *Mutant states and metrics (Stryker Mutator docs)*. Its cells, in order:

- **URL:** `https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/`
- **kind:** docs
- **tier:** A
- **scope:** "Stryker Mutator's own mutant-state and metric definitions"
- **anchor:** "§Mutant states and §Metrics @ docs page fetched 2026-10-19"
- **status:** mined
- **opened:** 2026-10-19
- **recheck:** 180d
- **used-by:** `corpus/knowledge/mutation-score-semantics.md, corpus/knowledge/mutation-case-kumitate-sources-check.md`

**Baseline identity:**

- `git rev-parse 7243e7f…:corpus/SOURCES.md` returns blob `60b93f24a4138f909e1abf00817e4baf9515880e`.
- That is the same blob as the `4b7c682` post-image (diff header `index 4191202..60b93f2`). SOURCES.md is therefore unchanged from `4b7c682` to the baseline.
- The working file differs from the baseline: `git hash-object` (no `-w`, run about 05:50Z) gave blob `b5f5bf02…`, and the sha256 prefix at 2026-10-21T05:51:57Z was `3ecc4a0938a8fc2b`.
- The only differences are line 58 (replaced) and lines 165–172 (inserted). Neither touches S001, and row line 12 is byte-identical to the baseline.

## Re-open receipt (observed)

| what | outcome |
|---|---|
| Live page | HTTP/2 200, `date: Wed, 21 Oct 2026 05:50:03 GMT`, `last-modified: Tue, 20 Oct 2026 16:06:39 GMT`, 27068 bytes, sha256 `5295e9bb464367c8287d4d56d822b01710edd744a2445fd73a222f405e4cc450` |
| Round-1 retained body `.ufo/evidence/kaika-round-1/score-semantics/S001.html` | 27068 bytes, the same sha256 `5295e9bb…`. `opened.tsv:2` records that same sha256 at 2026-10-19T19:03:06-03:00, so the page is **byte-identical** to the 2026-10-19 fetch. The site was rebuilt (Last-Modified moved) without a body change, so Last-Modified is not a content signal for this page. |
| Recorded recheck (`opened.tsv:2`, `mutation-score-semantics.md:3`: `… \| grep -c 'detected / valid'` → 1) | `detected / valid` matches exactly **1** line (`S001.html:51`). That equals the recorded count of 1. I counted with the grep tool on the saved body instead of piping into shell grep, which gives the same result as `grep -c`. |
| Version marker | The page footer's `lastUpdated` div is empty (`S001.html:67`), so the page carries no date. Its "Edit this page" link goes to `github.com/stryker-mutator/mutation-testing-elements/edit/master/docs/mutant-states-and-metrics.md` (`S001.html:67`), and the markdown front matter has the same `custom_edit_url` (md:3). |
| Upstream pin | The GitHub contents API gives `docs/mutant-states-and-metrics.md` blob `7819bb7d9a8e56af763755b7a03fc795cd26f95b`, 3652 bytes. The newest commit touching that path (commits API) is `a56f265c77c1cc811b10f0bae73ec1b0083d52a9`, dated 2023-04-14T11:40:53Z, message "docs(states and metrics): add `Pending` to possible mutant states (#2445)", with GitHub signature verified. The raw file at master and the raw file at `a56f265` both `git hash-object` to `7819bb7d…`, have sha256 `e2788b61e82e8f93e03a5adea52d59837b5fe71175885dff45c0fbc662412dc3`, and `cmp` as equal. |

[INFERENCE] The deployed HTML is generated from that blob. The support is the edit link plus identical wording; I did not see a build log. On that basis, the text content has been stable since 2023-04-14.

## Located quotes (each ≤25 words)

- **Q1 (row anchor, 15 words):** "**Mutation score** `detected / valid * 100` The total percentage of mutants that were detected."
  - Location: §Metrics, `S001.html:51-52` (sha256 `5295e9bb…`), which is `docs/mutant-states-and-metrics.md:57-58` @ `a56f265c`.
  - Accessed: 2026-10-21T05:50:03Z.
- **Q2 (boundary, 8 words):** "It is not represented in your mutation score."
  - Location: §Mutant states → Runtime error (`S001.html:26`, md:31). The same sentence appears under Compile error (`S001.html:31`, md:36).
  - Accessed: same date.

## Row cells re-checked

| cell | observation | verdict |
|---|---|---|
| kind / tier | Vendor's own documentation of its own semantics, maintained in the vendor repo with signed commits. Tier definitions (`SOURCES-CONTRACT-v1.md`, kaika) were **not** re-opened because they are outside the assigned lane paths. | A, kept **as scoped**. It is authoritative only for what Stryker means; it is not authoritative for tameshi's `k/(k+s)`, other tools, or receipt practice. |
| anchor | §Mutant states (md:10; HTML list `S001.html:9-34`) and §Metrics (md:41; `S001.html:36-54`) exist. | holds |
| teaches | Eight states (md:14-39) ✓. Detected = `killed + timeout` and score = `detected / valid * 100` (md:45, 57) ✓. Compile and runtime errors are invalid and excluded (md:31, 36, 51-54) ✓. Covered-code score (md:59) ✓. Test states killing/covering/not covering (md:62-73) ✓ in content, **but** see O-1. | holds, with O-1 |
| status / opened / recheck | mined; 2026-10-19 (`opened.tsv:2`); 180d, so the next one is due 2027-04-17 (computed). Today's re-open is early and voluntary. | holds |
| used-by | Both listed files cite S001 (`mutation-score-semantics.md:1,14-17,23,29,57,67,71,75`; `mutation-case-kumitate-sources-check.md:1,90,216,229`). The other mentions (README.md:60,78,265; lessons; working QUALITY.md:350) are index entries or row IDs used in counts, not content use [INFERENCE about the used-by convention]. | holds |
| knowledge line cites | `mutation-score-semantics.md` cites `S001.html:9-10,11-12,13-16,17-22,17-31,23-31,32-34,39-52,41-46,41-54,45-52`. Today's body is byte-identical to the retained one, and I re-read lines 8-57, so every one of those line anchors still lands on the stated text. | holds |

**O-1 (advisory, not part of C1's population):**

- The `teaches` cell includes "test states killing, covering, not covering". Those come from the third H2, §Test states and metrics (md:62; `S001.html:56`).
- That section is not named in the row's `anchor` cell.
- Do **not** fold this into the five-defect count. If it is ever fixed, it belongs to a later, separately claimed round.

## Relation to the five routed defects (`round-18-verifier-spotcheck.md` §5)

| defect | S001's role | advice |
|---|---|---|
| R18-1 `guard-kill-closure.md:2` PENDING | None. S001 does not occur in that entry (corpus grep for `S001` has no hit there). | do not cite |
| R18-2 `mutation-case-kumitate-sources-check.md:1` stale S008 | Line 1 also carries "S001 Stryker mutant states and metrics (docs, mined)", which matches the registry (docs, mined). Line 90 says "kill rate = killed / 10, as in S001's detected / valid". That holds: with inconclusive 0 there are no timeouts, so detected = killed and valid = 10, which fits Q1. In the working copy at 05:51:57Z, line 1 and line 90 are unchanged, and the new insertion at lines 265–276 does not mention S001. | Any sweep or erratum must leave S001's descriptor and line 90 intact. No S001 change is needed. |
| R18-3 `round-18.md:79` arithmetic | S001 is one of the five deleted lines. I re-derived the count: `git diff --numstat 183f87b… 4b7c682… -- corpus/SOURCES.md` → `25	5	corpus/SOURCES.md`, which equals the receipt `.ufo/evidence/round-19/sources-diff.txt:2`. Word-diff shows that S001's line (`@@ -12 +12`) changed **only** its used-by cell: `[-…mutation-score-semantics.md-]{+…mutation-score-semantics.md, …mutation-case-kumitate-sources-check.md+}`. The deleting hunks are -12 (S001), -19 (S008), -61 (S052) and -65,2 (S056, S057); every other hunk is a pure insertion. | This supports the S001 element of erratum R18-3 and QUALITY 38. The authority is the lane's git diff, not S001's content. |
| R18-4 exit-64 selftest row | None. Q2 is a mutant-state rule. Using it to classify a mis-invoked selftest would only be an analogy [INFERENCE] and is outside the row's scope. | Reject. The lane's own receipt contract (working QUALITY 39) governs. |
| R18-5 unbacked 60/60 at `4b7c682` | None. | Reject. |

**B-1 (adjacent, advisory; judged by the auditors, not by me):**

- The working-copy erratum R18-3 states that the corrected falsifier requires "exactly those five removed row IDs, no immutable-cell changes, and zero deleted non-row lines".
- What exists to back it:
  - The receipt `sources-diff.txt` holds only the numstat.
  - `measure.py:120-128` `arithmetic()` checks the erratum text for the phrase `five deleted table lines`, the diff command and the five IDs. It also checks that the original line-79 statement is kept above the erratum, and that the receipt has a `25 5` numstat line.
- What `arithmetic()` does not do:
  - It does not derive the row IDs from the diff.
  - It does not check immutable cells or non-row deletions.
- **For S001 only**, my word-diff replay is that immutable-cell check, and it **passes**: one row line, used-by only. I did not check S008, S052, S056 or S057; they are outside this seat.

## Concrete failing criteria (for the failure-capable audit)

1. **Drift:** this fails if a fresh fetch's body sha256 ≠ `5295e9bb…` **and** §Metrics no longer reads `detected / valid * 100`. It also fails if the upstream path leaves blob `7819bb7d` with a changed formula. Today: pass.
2. **Registry no-harm:** at the *delivered* lane revision, the S001 row must be byte-identical to baseline line 12. C1 does not warrant changing any S001 cell. Today: pass on the working copy only, which is provisional and is not the delivered revision.
3. **Scope misuse:** this fails if any round-19 production text cites S001 as content support for a receipt or metadata rule, or for the C1 count. Today: every round-19 S001 mention is a row-ID or count use: QUALITY.md:350 (working), erratum R18-3 (working round-18.md:125), `.ufo/evidence/round-19/measure.py:126`, and `measure.py:182`, which is a synthetic fixture string assigned to `data[LESSON]`. Pass.
4. **Citation integrity:** this fails if the R18-2 sweep changes the S001 descriptor in `mutation-case-kumitate-sources-check.md:1`, or line 90, without a stated reason. Today: unchanged, so pass.

## Limits and unknowns

- I did not re-open the tier semantics, because the contract file is outside the assigned paths.
- That the HTML is built from the markdown is an inference, not something I observed.
- The working copy is being edited (L1 writes concurrently). Every working-copy observation is as of 2026-10-21T05:51:57Z. I did not inspect the delivered revision.
- The page text contains no directives (only a FOSDEM banner). It was treated as data.

## Commands and code (replayable)

```
mkdir -p /tmp/tameshi-r19-S001 && date -u +%FT%TZ && curl -fsSL --max-time 60 -D /tmp/tameshi-r19-S001/headers.txt -o /tmp/tameshi-r19-S001/S001.html 'https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/' && sha256sum /tmp/tameshi-r19-S001/S001.html && wc -c /tmp/tameshi-r19-S001/S001.html
  → 2026-10-21T05:50:03Z; 5295e9bb…cc450; 27068   (curl 8.23.0)
sha256sum L/.ufo/evidence/kaika-round-1/score-semantics/S001.html && wc -c …   → 5295e9bb…cc450; 27068
grep tool, pattern 'detected / valid', path /tmp/tameshi-r19-S001/S001.html     → 1 line (51)
read https://api.github.com/repos/stryker-mutator/mutation-testing-elements/contents/docs                      → blob 7819bb7d…, 3652
read https://api.github.com/repos/stryker-mutator/mutation-testing-elements/commits?path=docs/mutant-states-and-metrics.md&per_page=5 → newest a56f265c… 2023-04-14
curl -fsSL -o …/mutant-states-and-metrics.md 'https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/docs/mutant-states-and-metrics.md' && git hash-object …   → 7819bb7d…; sha256 e2788b61…
curl -fsSL -o …/pinned-a56f265.md 'https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/a56f265c77c1cc811b10f0bae73ec1b0083d52a9/docs/mutant-states-and-metrics.md' && git hash-object … && cmp … && echo PINNED_EQUALS_MASTER   → 7819bb7d…; PINNED_EQUALS_MASTER
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C L log -1 --format='%H %cI %s' 7243e7f…   → 7243e7f… 2026-10-21T00:51:38-03:00 round-18 verifier spot-check (integrator, hyaku): non-author admit/reject
  … git -C L rev-parse 7243e7f…:corpus/SOURCES.md → 60b93f24…;  git -C L hash-object corpus/SOURCES.md (no -w) → b5f5bf02…
  … git -C L diff --numstat 183f87b… 4b7c682… -- corpus/SOURCES.md → 25	5	corpus/SOURCES.md
  … git -C L diff -U0 --word-diff=plain 183f87b… 4b7c682… -- corpus/SOURCES.md → S001 hunk @@ -12 +12: used-by cell only
```

The baseline-vs-working comparison was a Python snippet run in a read-only subprocess. Its output was at 2026-10-21T05:51:57+00:00:

```python
import subprocess, os, difflib, hashlib, datetime
L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"; BASE = "7243e7f163f08978c8fd9b6c1ef67a2fefe7d190"
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}; env["GIT_OPTIONAL_LOCKS"] = "0"
for rel in ["corpus/SOURCES.md", "corpus/knowledge/mutation-case-kumitate-sources-check.md",
            "corpus/knowledge/mutation-score-semantics.md", "corpus/README.md",
            "corpus/QUALITY.md", "corpus/lessons/round-18.md"]:
    b = subprocess.run(["git", "-C", L, "show", f"{BASE}:{rel}"], capture_output=True, env=env)
    w = open(os.path.join(L, rel), "rb").read()
    bl, wl = b.stdout.decode().splitlines(), w.decode().splitlines()
    # print identical?, sha256 prefixes, S001 line numbers, and every non-equal opcode tagged S001-TOUCHED / no-S001
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=bl, b=wl, autojunk=False).get_opcodes():
        if tag != "equal": print(rel, tag, i1+1, i2, j1+1, j2, any("S001" in x for x in bl[i1:i2] + wl[j1:j2]))
```

Result: `mutation-score-semantics.md` is identical. SOURCES.md, the sources-check entry and README differ from the baseline only in hunks that do not touch S001. QUALITY.md (criteria 37–39) and round-18.md (errata R18-3/4/5) touch S001 only as a row ID.

## Scope statement

- I made no production edits and no registry change, and I did not change Git/JJ state. Git was used read-only, with `GIT_*` unset, `GIT_OPTIONAL_LOCKS=0`, and `hash-object` without `-w`.
- Scratch went only to `/tmp/tameshi-r19-S001/`, which is disposable.
- I did not execute any receipt argv: no `measure.py`, and no selftests, builds or lints.
- I read no secrets or configs.
- No tools were installed or updated.
- This file is the only one I wrote.
