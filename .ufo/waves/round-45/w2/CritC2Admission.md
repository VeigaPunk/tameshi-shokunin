seat: CritC2Admission
(round 45, w2, lane tameshi-shokunin, 2026-10-25; item: outside-critic spot-check of the three C2 assimilation decisions + attack on the coverage claim's novelty)

## 0. Bounds and method

- Read first: `.ufo/evidence/round-45/contract.json` (never edited). Lane checkout read-only; the only write is this report. Scratch: `/tmp/tameshi-r45-CritC2Admission/` (created; `chk.py`, `live-{advanced,primer}.md`). Read-only package `/home/vgpnk/Projects/shokuknow` opened read-only only.
- **No counter executed.** The deciding run is the L1's. I re-implemented the counter's `fold`/`QUOTE_RE`/`gt_rows`/`entry_ok` clauses (`coverage/measure.py:40,45-53,60-112`) in `/tmp/tameshi-r45-CritC2Admission/chk.py` and read the worktree files with `git show HEAD:<path>`; that is analysis, not a `measure.py` invocation.
- No tool installed or upgraded (pacman paused host-wide; curl/git/python3 sufficed).

## 1. Verdicts

| decision | verdict | deciding evidence |
|---|---|---|
| admit S256 (advanced.md) + `r8-gtest-order-and-seed.md` | **AGREE** (one LOW nit, §3-L1) | row + entry pass every counter clause by local reimplementation; all 10 cited line anchors verify; live bytes today = committed snapshot |
| admit S257 (primer.md) + `r8-gtest-primer-independence.md` | **AGREE, one correction** (§3-M3: the F2-mapping sentence overreaches) | same; 17 cited anchors verify; 18/18-404 receipt is real |
| refuse `r8-gtest-generator-contract.md` (staged S204) | **AGREE** — over-determined, four independent grounds | §2.3 |
| is the GoogleTest order/fixture ground new for this lane? | **YES at entry level, NO at registry-lead level** — the claim survives, the README prose overclaims | §2.4 |

## 2. Evidence

### 2.1 S256 + `r8-gtest-order-and-seed.md` — admit

```
$ python3 /tmp/tameshi-r45-CritC2Admission/chk.py
ROW S256 status= mined snap= .ufo/evidence/round-45/coverage/sources/googletest-advanced.md sha_ok= True sha= 05546ed6db922144 used= ['corpus/knowledge/r8-gtest-order-and-seed.md']
ROWS ['S256', 'S257']
line0 cites: ['S256'] | starts source: True
line1: verified-at: 2026-10-25
line2 prefix recheck: True
in used-by: ['S256']
QUOTE (15, "Remember that the test order is undefined, so your code can't depend o")
QUOTE (13, 'the random seed value, such that you can reproduce an order-related te')
ENTRY_OK(local reimpl) = True
```

- Row is 13 cells, `status=mined`, `cell[6]` names `…/sources/googletest-advanced.md` + `sha256 05546ed6` and the committed blob hashes to exactly that (`corpus/SOURCES.md:131`).
- Indexed: `corpus/README.md:562` carries `` `knowledge/r8-gtest-order-and-seed.md` `` (counter accepts the `corpus/`-stripped form, `measure.py:129-130`).
- Live re-grounding is real, not a relabel: `curl -fsSL …/cd8e73f…/docs/advanced.md | sha256sum` → `05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2`, identical to the snapshot; `grep -cF 'the random seed value, such that you can reproduce an order-related test failure'` on the live bytes → `1`.
- All anchors named in the entry resolve: `:872/:873` ("GoogleTest creates a new test fixture object for each test in order to make" / "tests independent and easier to debug."), `:896/:897/:899`, `:1975/:1977/:1979/:1981/:1982` — verified line by line against `.ufo/evidence/round-45/coverage/sources/googletest-advanced.md`.
- The wave-1 HIGH-1 defect is fixed in the landed text (`ad5942c`): the false "the lane's instrument excluded clock stamps" sentence is gone; the replacement claim ("`hermetic-env-differential.md` hashes raw streams with `normalization: none`") matches `tools/env-diff.py:113` (`"normalization": "none"`) and `tools/env-diff.py:8-9` ("Raw streams are hashed, never normalized").

### 2.2 S257 + `r8-gtest-primer-independence.md` — admit

- Row `corpus/SOURCES.md:132` is 13 cells, `mined`, snapshot `…/googletest-primer.md`, `sha256 03d756ab`; blob hash `03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e` matches, and today's live fetch of the pinned URL hashes to the same value.
- Entry passes the trio/verified-at/used-by/quote clauses by local reimplementation; 15 double-quoted spans locate, e.g. 23-token "Tests should be *independent* and *repeatable*…", 12-token "GoogleTest always deletes a test fixture before it creates the next one.", 24-token "GoogleTest does **not** reuse the same test fixture for multiple tests…".
- Anchors verify exactly: `:14-15`, `:15-16`, `:83-84`, `:107-111`, `:251`, `:252-253`, `:329-330`, `:356-364`.
- The dead-path finding is receipted, not asserted: `.ufo/waves/round-45/w1/ScribeGtestPrimer.md:36-58` lists the 18 `curl -w '%{http_code}'` outputs, all `404` — matching the entry's "18/18" and the 9 refs × 2 prefixes count.
- Indexed at `corpus/README.md:563`.

### 2.3 Refusal of `r8-gtest-generator-contract.md` (staged S204) — agree, four independent grounds

1. **No admitted id.** `adoption-map.json` targets are exactly `S105,S106,S155,S156,S256,S257,S258,S259,S260,S261`; `guard-map.json` `verdict=admitted, map_floor=S256, map_entries=10`. S204 is in no declared map, and the next free id (S262) is outside the guard-admitted cascade — a third row would need a post-freeze contract amendment after seats have scored.
2. **No located quote at all.** `QUOTE_RE` (`measure.py:38`) finds **zero** double-quoted spans ≥10 chars in the package entry — its only quoted sentence (`"a generator whose contract the lane's gate fixtures can be checked against"`) is line-wrapped, and the rest are single-quoted. `entry_ok` → `no located quote`.
3. **`verified-at: 2026-10-24`** < `MIN_VERIFIED = '2026-10-25'` (`measure.py:40,100-102`).
4. **Content defect verified independently of the counter:** the upstream table has **six** generators, not five — `googletest-testing.md:104-113` includes `ConvertGenerator<T>(g)` (`grep -cF ConvertGenerator` → 8); and every yield string in the entry's table is absent from the snapshot: `bounded arithmetic sequence`=0, `fixed set`=0, `elements of a container`=0, `two-element sequence`=0, `cartesian product`=0. The entry presents a paraphrase as "the upstream reference document's generator table" — QUALITY bar 2/3.
- Refusal costs C2 nothing (needs entries ≥ 2 from S256/S257; only those two entries cite a googletest row: `grep -rln 'S256\|S257' corpus/knowledge/` → the two files, no third).

### 2.4 The coverage claim's novelty — the attack

Sweep as assigned, at base `5891bdb77aba8489683533ae4cdd3b49b5e2626b`:

```
$ git -C . grep -rniE 'googletest|gtest|test order|shuffle' 5891bdb… -- corpus/knowledge SKILL.md
(zero matches)
```

Widened to `corpus/README.md` and the registry:

- `test order` / `test-order` / `shuffle`: **0 files** across `corpus/knowledge`, `SKILL.md`, `corpus/README.md`.
- `seed` matches 5 entries (`mte-report-interop`, `regression-tally-completeness`, `runner-tally-audit`, `runner-tally-audit-v2`, `verification-patterns-fleet`); every hit is mutation-seeding / commit-seeding / `tameshi-hand-seeded` — **none is a test-order seed**.
- `googletest`: 0 rows and 0 entries at base (reproduces the contract's `surface` sentence).

**Counterexample to the prose, not to the claim.** Two *held registry rows* already state the order-dependence proposition, and neither is cited or acknowledged by the new entries:

- `corpus/SOURCES.md:24` **S013** Jest CLI Options, `docs`, status `queued`, used-by `—`: teaches "… `--randomize with --seed` reproduces order-dependent failures …". That is a test framework's own upstream documentation asserting exactly entry 1's second half (order randomisation + seed reproduces the failure).
- `corpus/SOURCES.md:36` **S025** Luo et al. FSE 2014, status `queued`, used-by `—`, and a listed F3 source (`corpus/README.md:80`): teaches "top causes are Async Wait, Concurrency and Test Order Dependency; 74% of order-dependency fixes clean shared state" — the hazard class plus the shared-state fix.

So the accurate novelty statement is: **first *mined* GoogleTest rows and the first knowledge entries citing a test framework's own normative document on order/fixture lifecycle.** The claim as frozen is citation-scoped ("0 rows and 0 entries citing github.com/google/googletest at base") and is **not falsified**; the entry bodies make no novelty claim. What is new and genuinely uncarried is the *normative* form: order is *undefined* (not merely randomisable), a fresh fixture object per test, and the published-seed mechanism — none of which appears in S013/S025.

### 2.5 Registry integrity after the append (no-harm spot-check)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md      → 117   (115 + S256 + S257)
$ awk -F'|' '… NF!=13 {n++} END{print n+0}' corpus/SOURCES.md               → 0
$ awk -F'|' '… {i=$2; …} ' corpus/SOURCES.md | sort | uniq -d               → (empty)
$ status tally                                                              → mined=89 queued=22 rejected=6
$ grep -c 'raw.githubusercontent.com/google/googletest' corpus/SOURCES.md  → 2
```
Footer reconciled append-only: `corpus/SOURCES.md:467` "Next unused id: S258 (the staged-id guard's safe floor after this append; staged ids S161–S255 stay reserved by document for the package)."

## 3. Findings by severity

### MEDIUM-1 — `corpus/README.md:565` overclaims the novelty
"Frontier F3 (determinism precondition) gains its **first upstream test-framework sources**". False as written: S013 (Jest 30.5 CLI docs, `corpus/SOURCES.md:24`) and S018 (Hypothesis API reference, `:29`) are test-framework upstream docs already in the registry (both `queued`), and S004 (cargo-mutants book, `:15`) is a *mined* test-tool upstream doc already listed in F3's own source cell (`corpus/README.md:80`).
**Smallest safe correction:** replace with "gains its first *mined GoogleTest* rows and the first knowledge entries citing a test framework's own normative document on test order and fixture lifecycle; S013's `--randomize/--seed` and S025's order-dependency finding remain queued leads."

### MEDIUM-2 — Neither new entry records the lane's nearest existing statements (S013, S025)
A future reader of the two entries plus README:565 would conclude the lane held no order-dependence ground. The refused package entry at least recorded its unreconciled relation to S120 (`r8-gtest-generator-contract.md`, "What is still unknown"). The adopted entries do not.
**Smallest safe correction:** one `## Limits` bullet in each: "the relation to held lead S013 (`--randomize with --seed`) and S025 (order dependency as a top flaky cause; shared-state fixes) is not reconciled here — this entry adds the framework's normative statement, not the hazard's first appearance in the lane." (No counter impact: `entry_ok` ignores the body.)

### MEDIUM-3 — `r8-gtest-primer-independence.md` maps ASSERT/EXPECT onto F2 too loosely
The entry's F2 inference ends: "A gate that reports a bare case label … **without saying whether execution continued past the witness** is strictly less informative than this." F2's witness distinction is *red-on-witness vs red-elsewhere* (`corpus/knowledge/witness-scoped-kill-verdict.md:9-14`: `killed` = "went red on its witness", `accidental` = "went red, but not on its witness"). Whether execution *continued* is a fail-fast/aggregation property, not witness identity: a gate can report "case 05 failed; execution continued" and still be `accidental`. The quoted observation itself is accurate (verified at `googletest-primer.md:107-111`), and the first half of the inference — a fatal failure names the deciding assertion and stops the function, so the verdict is attributable to it — is sound.
**Smallest safe correction:** drop the continuation clause; keep "a fatal failure makes the verdict attributable to the named assertion, EXPECT aggregates several assertions into one verdict".

### LOW-1 — Entry 1 anchor `:1981` for a span that ends on `:1982`
"The console output includes "the random seed value, such that you can reproduce an order-related test failure" (`:1981`)" — `googletest-advanced.md:1981` ends at "test failure"; the sentence continues "later." on `:1982`. The quoted span is a verbatim substring, so the counter and QUALITY are satisfied; the anchor names only the start line and the elided "later." carries no ellipsis. Nit only; no change required.

### LOW-2 — Entry 2's ground line cites `QUALITY.md` criterion 62 for the wrong clause
`corpus/QUALITY.md:701-707` (criterion 62) governs *revision-named measured values requiring a committed receipt*, not "the determinism precondition". The entry's `recheck:` line does assert a measured value ("ran 2026-10-25 → 1"), so the citation is defensible there but misleading in the `ground:` line.
**Smallest safe correction:** move the criterion-62 reference to the recheck clause, or drop it from `ground:`.

### LOW-3 — `corpus/README.md:567` forward-references a file that does not exist yet
"… is refused this round (`corpus/lessons/round-45.md` `## Gate`)" — `ls corpus/lessons/round-45.md` → `No such file or directory`. Expected: `.ufo/waves/round-45/spec-w2.json` and `w2-dispatch.json` reference the lesson, so this is a landing obligation, not a wave-1 miss. **Landing condition:** the file and its `## Gate` must exist at the deciding revision, with the refusal recorded per QUALITY bar 5 ("A rejection is kept, not silently dropped").

### Notes, not defects
- The counter's line-wrap fragility that CritC2Control demonstrated (`w1/CritC2Control.md`) is now neutralised for the two adopted entries: both carry multiple single-line 6-25-token spans, so acceptance no longer hinges on one wrapped quote. The refused entry has *zero* double-quoted spans for the same reason.
- Entry 2's `sha256 03d756ab…` is 8-hex-truncated while entry 1 gives the full digest; the row anchor also uses the 8-hex prefix that `HEX_RE` matches. Cosmetic only.

## 4. Residual risk / verification gaps

- I did not run `coverage/measure.py` at any revision (bounds). The `ENTRY_OK`/`rows` results above come from my re-implementation of `measure.py:40-112` against `HEAD`; the one deciding run remains the L1's.
- Live-byte identity was checked today (2026-10-25) for both pinned documents; upstream `main` can move after today, bounded by the commit pin.
- My novelty sweep covered `corpus/knowledge`, `SKILL.md`, `corpus/README.md` and the registry. I did not sweep `corpus/lessons/` or `.ufo/` history for order-dependence prose; the claim's surface is registry/entry-scoped, so that gap does not bear on the count.
- Untested by me: whether any sibling lane holds GoogleTest ground (out of this lane's census); the lane's own census is what the contract scores.
