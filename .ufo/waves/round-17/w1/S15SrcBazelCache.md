# S15SrcBazelCache — round 17 wave 1 (C1 source: Bazel remote caching)

Seat: `TameshiR17.S15SrcBazelCache` (leaf, no delegation). Lane: tameshi-shokunin.
Lane tip read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`. Date: 2026-10-20.
Scope: open `https://bazel.build/remote/caching` live, record the access, locate one
≤25-word verbatim quote, draft a `SOURCES.md` row in the contract's 11-column shape
(id `S0xx`; the L1 assigns ids), and state what it teaches C1 and where the analogy
stops. No lane file was edited; no lane instrument or gate was executed (read-only
inspection only); no commit.

## 1. Access record (observed)

| Field | Value | Evidence |
|---|---|---|
| Canonical URL | https://bazel.build/remote/caching | page `<title>`: "Remote Caching - Bazel Documentation" |
| HTML fetch | `curl -sS -L` → `http_code=200 size=293138`, 2026-10-20T15:21:23Z | live shell, `date -u` in the same command |
| HTML sha256 | `037481fc4545547aeba5c8069c3123bdc77e3815df0408887e793d46421f3ab6` | `sha256sum bazel-caching.html` |
| Markdown alternate | https://bazel.build/remote/caching.md → `http_code=200 size=16722`, `content-type: text/markdown`, fetched 2026-10-20T15:23:12Z (file mtime 12:23:12-03:00) | `curl -fsSL`, `stat -c %y` |
| Markdown sha256 | `0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5` | `sha256sum bazel-caching.md` |
| Reader cross-check | `read` of the canonical URL served the markdown alternate (`Method: alternate-markdown`) and reproduced the quoted sentence verbatim | reader output |
| Page version | not stated in content. `Use Bazel version 0.10.0 or later` (md:29) is an implementation floor, not a doc revision. The HTML's docs config lists versions HEAD / 9.3 / 9.2; the canonical unversioned URL serves HEAD | grep of page bytes |
| `Last-Modified` | `Tue, 20 Oct 2026 15:21:23 GMT` — identical to the fetch second | `curl -sSI` vs fetch clock |

The `Last-Modified` equality is a **dynamic-generation artifact**, not a publication
date: the server reports "now" for each render. The anchor therefore pins the access
date plus the fetched-bytes digest, not `Last-Modified`.

## 2. Quote for the row

Q1 — §Known issues → subsection "Bazel does not track tools outside a workspace"
(`<h2 id="known-issues">` at md:353 / HTML:706). Source lines md:380-382, rendered
HTML:725-727. **24 words**:

> Then, two users with different compilers installed will wrongly share cache hits because the outputs are different but they have the same action hash.

Verbatim check (whitespace-normalized, because the docs hard-wrap at ~78 columns):
the sentence occurs exactly once in the extracted HTML text and exactly once in the
markdown alternate. The one-line form above is a reflow of the source's three lines
(`:380` ends "Then,", `:381` ends "hits", `:382` ends "See"); no word was changed.
A second raw occurrence exists in the serialized page payload on the manifest line
(an `_jsx` fragment, HTML:804), not in the rendered article.

Supporting passages opened for context (not the row quote):

- §Overview, md:19-21 — "Bazel breaks a build into discrete steps, which are called
  actions. Each action has inputs, output names, a command line, and environment
  variables. Required inputs and expected outputs are declared explicitly for each
  action."
- §Overview, md:36 — "The action cache, which is a map of action hashes to action
  result metadata."
- §Known issues, md:359-360 — "When an input file is modified during a build, Bazel
  might upload invalid results to the remote cache." The page offers
  `--experimental_guard_against_concurrent_changes` as change detection.
- §Known issues, md:369-371 — "Only environment variables explicitly whitelisted via
  `--action_env` are included in an action definition."

The page never states the hash's preimage. That the action hash covers the action's
declared inputs, output names, command line and whitelisted environment is
**[INFERENCE]** from the Overview's action definition plus the known-issue text
(a tool outside the workspace leaves the hash unchanged). The row below claims only
what the page says.

## 3. Draft SOURCES row (not written to `corpus/SOURCES.md`)

Lane id state at tip: "Next unused id: S058" (`corpus/SOURCES.md:187`). The draft keeps
the target's `S0xx` placeholder; the L1 assigns the number (S058 if unchanged).

```
| S0xx | Remote Caching (Bazel docs) — https://bazel.build/remote/caching | docs | A | Bazel's action-cache reuse keyed by action hash, and its documented false-hit class for inputs outside the key | §Known issues → "Bazel does not track tools outside a workspace", markdown alternate remote/caching.md:377-383 (quote :380-382) @ page fetched 2026-10-20, version unstated, sha256 0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5 | an action-cache hit is reuse keyed to the action hash, so an input outside the key (an untracked compiler) keeps the same hash while producing different outputs — credit is sound only for what the key records | queued | 2026-10-20 | 90d | — |
```

Cell notes:

- `status: queued` is the contract-honest value at wave 1 (`mined` requires ≥1 path in
  `used-by`, and no lane artifact cites the row yet). On landing, if
  `corpus/lessons/round-17.md` or a knowledge note cites it, change `queued` → `mined`
  and `used-by` → that path; append-only rule 2 makes that an in-place field change
  logged old→new in the lesson, as round 16 did for S052–S057.
- `recheck: 90d` because the quote lives in a "Known issues" block that points at
  issue #4558 for updates and can be removed when the issue closes. Recheck command:
  `curl -fsSL https://bazel.build/remote/caching.md | sha256sum` against
  `0d362d11…badac5`; any drift means re-open the block and re-pin the anchor.
- No `|` occurs inside any cell.

Shape check (run in `/tmp`, copies only; the lane registry was not modified):

| Check | Command | Observed |
|---|---|---|
| Column count of the draft row | `python3` split on the pipe character | `13` fields = 11 cells (open/close delimiters) |
| Census on a synthetic table with `S058` substituted | CORPUS.md census commands | rows `1`, malformed `0`, tier `A=1` |
| Census on a full copy with the row inserted after S057 | same commands | rows `56` (55 written rows + 1; S038–S039 retired per `SOURCES.md:176-179`), malformed `0`, status `mined=28 queued=25 rejected=3` |

The `S0xx` placeholder does not match the census id regex (`S` + 3 digits), so the
numeric-substitution run is the one that exercised the shape.

Optional search-log line for the L1 (rule 5): question — how does a content-addressed
build cache decide a recorded result may be reused; opened the target-named URL
directly; identified 1, screened 1, included 1, excluded 0; stop — the page's own
action-hash definition and false-hit class answered the question.

## 4. What it teaches this round's claims

### 4.1 C1 — the transfer is exact in shape

C1 as declared: an entry that executed commands credits its SKILL.md bucket only if
every lane input it ran against still has its recorded sha256 at the measured rev.

- Bazel decides reuse by the action hash. An input the hash does not cover — a
  compiler in `/usr/bin` that Bazel does not track — leaves the hash identical while
  the outputs differ, so the cache serves a **wrong hit**.
- R16-C2b is that same failure in the lane (`corpus/lessons/round-16-verifier-spotcheck.md:226`):
  the bucket's credit key was its section sha `97cf436b`; `tools/mutate-and-run.sh`
  moved `75ed934d` → `0673d2e5`; the section bytes did not change, so the bucket kept
  its credit although its recipe step 3 now exits 2 `expected_input_digest_mismatch`
  (step 2 takes the same path; the spot-check marks that one [INFERENCE]). Key
  matched, world did not.
- The three measure-v2 reasons map one-for-one onto ways a key fails to cover what ran:
  `inputs-unrecorded` ≈ a variable never whitelisted into the action definition;
  `input-missing` ≈ a declared input absent at the measured rev; `input-drift` ≈ the
  page's "input file modified during a build … invalid results".
- The remedy shape also transfers: the page makes coverage **explicit** (the
  `--action_env` whitelist) instead of inferring it. C1's `inputs` map from
  `trace-inputs.py` is that explicit declaration, and `inputs-unrecorded` is the
  refusal to accept an inferred key.

### 4.2 Where the analogy stops — do not overclaim

- **Declared vs observed.** Bazel's key is over *declared* inputs; C1's is over
  *observed* opens under `strace`. Observed is closer to what actually ran, but only
  as complete as the trace is. The page itself documents real outside-the-key classes
  (untracked tools; non-whitelisted environment), so the row supports "coverage must
  be explicit and bounded", never "the trace captures everything". The trace's limits
  are a tameshi fact, not this source's claim. **[INFERENCE]**
- **During-the-run change.** Bazel offers an opt-in, experimental concurrent-change
  guard (`--experimental_guard_against_concurrent_changes`) because a check can
  miss a modification made mid-run. C1's measure re-hashes at the measured rev, so
  a file changed during command execution and restored before REV would not be seen.
  This is a residual unknown of the check-at-REV design, not a defect this source
  proves exists in the lane. **[INFERENCE]**
- **Problem statement, not solution.** The untracked-tool case is an open known issue
  ("See issue #4558 for updates"). Tier A is scoped to Bazel's own cache semantics; it
  is not authority for any tameshi design.
- **Not C2 evidence.** Nothing here speaks to registered entry commands returning
  their registered outcome. C2 cites the disposition gate and the registry, not this
  row.

### 4.3 Falsifiers

- **Row drift:** the known-issues block is living text; if #4558 closes and the
  subsection is edited out, the quote disappears. The digest recheck catches it.
- **Overclaim:** a report that says "Bazel proves input-keyed credit is sufficient" is
  false on the page's own text — the page names a residual false-hit class, not a
  complete key.
- **Underclaim:** treating the row as mere analogy misses that the page states, at
  docs tier A, precisely the failure mode R16-C2b removes: a matching key with a
  changed input.

## 5. Evidence log

| Step | Command (from `/tmp/tameshi-r17w1-S15SrcBazelCache-oe0UrE`) | Exit | Key output |
|---|---|---|---|
| Fetch HTML | `curl -sS -L --max-time 60 -o bazel-caching.html -w '…' https://bazel.build/remote/caching` | 0 | `http_code=200 size=293138 url=https://bazel.build/remote/caching` |
| Fetch markdown alternate | `curl -fsSL --max-time 60 -o bazel-caching.md -w '…' https://bazel.build/remote/caching.md` | 0 | `http_code=200 size=16722 ctype=text/markdown; charset=utf-8` |
| Digests | `sha256sum bazel-caching.html bazel-caching.md` | 0 | `037481fc…f3ab6` / `0d362d11…adac5` |
| Quote location | `grep -n 'wrongly share cache hits' bazel-caching.md bazel-caching.html` | 0 | md:381, HTML:726 (rendered) |
| Quote verbatim/length | `python3`: whitespace-normalized substring count; word split | 0 | occurrences md=1, html-text=1; `words: 24` |
| Headings | `grep -n 'id="known-issues"\|id="overview"' bazel-caching.md bazel-caching.html` | 0 | md:15/353; HTML:458/706 |
| Row shape | `python3` split on the pipe character | 0 | `cols after split: 13` |
| Census (synthetic, S058) | the CORPUS.md census `grep`/`awk` trio | 0 | rows 1, malformed 0, `A=1` |
| Census (full copy) | same, row inserted after S057 | 0 | rows 56, malformed 0, `mined=28 queued=25 rejected=3` |
| Headers | `curl -sSI https://bazel.build/remote/caching` | 0 | `last-modified: Tue, 20 Oct 2026 15:21:23 GMT` = fetch second |
| Lane tip | `git rev-parse HEAD`; `git --no-optional-locks status --porcelain corpus/SOURCES.md` | 0 | `98bea7da…061f`; no output (clean) |

## 6. Opened paths (no contamination)

- https://bazel.build/remote/caching (HTML) and https://bazel.build/remote/caching.md
  (markdown alternate), plus the same URL via `read`.
- `tameshi-shokunin/corpus/SOURCES.md` (header, registry rows S052–S057, id allocation).
- `/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md (contract v1 shape and rules).
- `tameshi-shokunin/corpus/lessons/round-16.md` (Gate, Mistakes) and
  `tameshi-shokunin/corpus/lessons/round-16-verifier-spotcheck.md` §2, §3, §6.
- `tameshi-shokunin/.ufo/waves/round-16/w1/PITSource.md` and
  `tameshi-shokunin/.ufo/waves/round-12/w1/SourceBazel.md` (source-report precedents).
- `tameshi-shokunin/.ufo/waves/round-17/w1/W04QualityDraft.md` (report shape only).

No file outside this report was written in the lane. No `jj` command, no git write, no
lane tool executed, no registry edit.

## 7. Tools

None installed or upgraded; `curl`, `sha256sum`, `grep`, `awk`, `python3` sufficed.

## Verdict

**built** — page opened live (HTTP 200 at 2026-10-20T15:21:23Z, HTML `037481fc…`,
md `0d362d11…`), 24-word located quote verified once in both renderings, shape-validated
`S0xx` row drafted (next free S058), and the C1 teaching stated with its declared-vs-observed
limit: a matching cache key does not cover an untracked input, so credit is sound only
for what the key records.
