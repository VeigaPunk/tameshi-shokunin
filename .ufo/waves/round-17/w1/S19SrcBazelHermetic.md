# S19 — Bazel "Hermeticity" page: row draft and the C1 input-set limit

Seat: `TameshiR17.S19SrcBazelHermetic` (scout, wave 1, round 17). Lane tip
read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`. Date: 2026-10-20.
Scope: open the Bazel hermeticity page live, record the access date, a
<=25-word located quote, draft one `corpus/SOURCES.md` row, and state what the
page teaches for this round's claims (acceptance: C1 limits, undeclared
inputs). No lane file was edited; scratch was `/tmp` only; no tool installs.

## Source access (observed, not inferred)

| Fact | Command | Observed |
|---|---|---|
| Canonical page | `curl -sSL -o /tmp/bazel-herm.html -w 'http=%{http_code} bytes=%{size_download}\n' https://bazel.build/basics/hermeticity` | `html_http=200 bytes=135609`; sha256 `16bacb8e7bc2392299bf9eea5cbd8429e9f1d57032b8aad67397ea034f25eb30` |
| Text route used for the quote | `curl -sS -D /tmp/bazel-herm-headers.txt -o /tmp/bazel-hermeticity.md https://bazel.build/basics/hermeticity.md` | `http=200 size=5947`; sha256 `76167a0dacc146cfbc13b54a0d6db03a283d413c75f50a32666611f90b0b73da`; `content-type: text/markdown`; `link: </llms.txt>; rel="llms-txt"` (Mintlify alternate-markdown route) |
| Access time and build pin | response headers, same request | `date: Tue, 20 Oct 2026 15:21:19 GMT`; `x-version: dpl_8LJVMfxYNq6LJkohTrn2iyWT8umj`; `cf-cache-status: EXPIRED`; `age: 32705` (body came from that deployment's CDN cache) |
| `last-modified` is not a revision | response headers | `last-modified: Tue, 20 Oct 2026 15:21:19 GMT` equals the fetch time, so it is generated per request and cannot pin the page |
| Git commit pin search | `curl -sSL https://raw.githubusercontent.com/bazelbuild/bazel/master/site/en/basics/hermeticity.md` | 404 (14 B body); `api.github.com/repos/bazelbuild/bazel/commits?path=site/en/basics/hermeticity.md&per_page=1` returned 403 "API rate limit exceeded" (unauthenticated). No commit pin was located; the deploy id plus body sha256 are the pins used in the row |
| Prior use of this URL in the lane | `grep -rn 'basics/hermeticity' --include='*.md' .` from the lane root | no output; this row would be the first citation of the page |

Quote location: `/tmp/bazel-hermeticity.md` line 41-42 (§Benefits, Speed
bullet). The canonical HTML carries the same sentence inside its serialized
payload (`grep -o 'The output of an action can be cached[^<]*'` matched), so the
alternate-markdown text is not a divergent copy.

## Quote (gate evidence for the row's `teaches`)

Primary, 19 words (<=25), verbatim after joining the page's two-line wrap
(§Benefits, lines 41-42):

> The output of an action can be cached, and the action need not be run again unless inputs change.

Supporting sentence, 20 words, same page (§Identifying non-hermeticity, lines
63-64), used for the host-input clause of `teaches` rather than as the gate
quote:

> System binaries that differ across hosts (such as `/usr/bin` binaries, absolute paths, system C++ compilers for native C++ rules autoconfiguration)

Verification: Python `re.sub(r'\s+', ' ', raw)` then substring test returned
`verbatim_after_linejoin: True`, `words: 19` for the primary and
`q2_verbatim: True words: 20` for the supporting sentence. The page does not
contain the word "undeclared" (`grep -c 'undeclared'` = 0); "undeclared inputs"
is the round's framing, not the page's vocabulary — the page says "inputs" and
"non-hermetic".

## Row draft (L1 inserts and assigns the id)

```md
| S0xx | Hermeticity (Bazel docs) — https://bazel.build/basics/hermeticity | docs | A | Bazel's own definition of hermetic builds and its catalogue of non-hermetic input sources | §Benefits and §Identifying non-hermeticity @ page fetched 2026-10-20; markdown alternate 5,947 B sha256 76167a0dacc146cfbc13b54a0d6db03a283d413c75f50a32666611f90b0b73da; deployment id x-version dpl_8LJVMfxYNq6LJkohTrn2iyWT8umj (no git commit exposed) | a cache claim holds only while its inputs are unchanged, and host binaries, absolute paths, non-deterministic files and source-tree writes are named non-hermetic inputs — a cached credit must pin or exclude its host-provided inputs | queued | 2026-10-20 | 180d | — |
```

Insertion notes:

- `S0xx` is the target's placeholder. At the tip the next unused id is `S058`
  (`corpus/SOURCES.md:187` at `98bea7d`: `Next unused id: S058.`); other source
  seats in this wave are drafting rows, so the L1 assigns.
- `status: queued` with `used-by: —` is correct at insertion (contract rule 2:
  `mined` requires a citing path). If the round-17 lesson or a knowledge entry
  cites it in the same round, the L1 changes `status` to `mined` and fills
  `used-by`, logging old-to-new in the round lesson.
- `teaches` makes one learner-benefit claim in one sentence; no cell contains a
  `|` (verified: `backtick_pipes=0`, `split_fields=13`).

Contract-shape check against the frozen census in `CORPUS.md` §Census, run on
the draft with `S058` substituted (the census regex matches `S` + three or
more digits, so the literal `S0xx` placeholder is deliberately not matched):

| Check | Command result |
|---|---|
| Row matches the row regex | `row_count=1` |
| Malformed rows | `malformed=0` (13 `split('|')` fields: 11 columns plus the two edge pipes) |
| Tier histogram | `tier A=1` |
| Status histogram | `status queued=1` |
| Enum and tier-inflation scan | no output (`enum_scan_done`) |
| Backtick-pipe guard | `backtick_pipes=0` |
| Red-before: the checker can fail | a copy with one column dropped → `red_before_malformed=1` |

Commands were the `awk -F'|'` census lines from `CORPUS.md` §Census on
`/tmp/draft-sources-S058.md` and `/tmp/draft-sources-broken.md`.

## What it teaches for C1 (input-keyed cold-read credit)

The v2 rule is a cache in the page's exact sense: an entry that executed
commands credits its bucket only while every recorded input keeps its sha256 at
the measured rev (interface C). The page supplies both the justification and
the boundary:

1. **Justification — source identity.** §Overview, "Source identity": hermetic
   systems "identify sets of code mutations with a unique hash code" and "use
   this hash to identify changes to the build's input". That is the design
   premise of lane-relative input paths resolved as blobs at `REV` (contract A's
   `git cat-file blob <rev>:<path>`; contract C's `--rev`). It also supports
   preferring a commit over a working-tree read: the working tree is the mutable
   thing the hash exists to replace.
2. **The limit — the cache key is only as complete as the declared input set.**
   The page's catalogue of non-hermetic sources names classes the v2 contract
   either records nowhere or records without crediting:
   - **Host binaries outside `/home`.** `trace-inputs.py`'s `external` map is
     specified as "regular files under /home outside root" (contract C), so
     `/usr/bin/python3`, `/usr/bin/git`, `/usr/bin/strace`, `/usr/bin/node`,
     `/usr/lib` shared libraries and the kernel are not in any recorded set. An
     entry whose executed commands shell out is credited while its toolchain is
     outside the key. This is precisely the page's
     "System binaries that differ across hosts" bullet. [INFERENCE: the trace
     helper is a new file this wave; I read the interface contract, not an
     implementation.]
   - **Absolute paths.** Ledger `inputs` are lane-relative; `external_inputs`
     are absolute but "reported, not credited" (contract C). A command that
     reaches lane bytes through an absolute path (a fleet-mirror clone symlink,
     a sibling repo) can sit outside `inputs`, so the credit cannot see those
     bytes move. Contract A's repo-identity guard (realpath of
     `git rev-parse --show-toplevel` equals realpath of root) closes the *root
     identity* half of the page's "absolute paths" bullet; it does not put
     host or sibling files into the key.
   - **Source-tree writes.** §Identifying non-hermeticity names writing to the
     source tree during the build because it fixes the tree for the first
     target. Analogue in contract B: registry rows run "with cwd = lane root",
     so a row that writes a fixture, cache or evidence file makes later rows'
     inputs depend on earlier rows' execution order. The registry declares no
     ordering and no write isolation, so a held N/M is order-sensitive until
     rows are proven read-only or run write-isolated. [INFERENCE from contract
     B; `tools/registry-check.py` and `tools/registry.json` are absent at
     `98bea7d`, verified with `git cat-file -e`.]
3. **What the page does not license.** It does not say a hash over the declared
   input set makes an outcome sound. It says the opposite: an input that is not
   declared is the definition of non-hermetic. So the round-17 text should claim
   "input-keyed credit is necessary, not sufficient — host-provided inputs stay
   outside the rule", not "credit is sound because inputs are pinned". If C1
   needs the stronger claim, the ledger must gain the `/usr`-class inputs (or
   state that credit is host-scoped). That is a design decision for the L1; this
   seat only records the limit.

The page's own diagnostics map one-to-one onto cheap countermeasures the round
could run if it wants to bound the limit:

- "Ensure null sequential builds" — run the same credit/registry evaluation
  twice in fresh clones at the same rev and compare exits; this proves
  within-host determinism only, not hermeticity.
- "Execute a build within a docker container that contains nothing but the
  checked-out source tree and explicit list of host tools" — the stronger form
  of `--rev`; the fleet-mirror layout deliberately adds host state, so a green
  `REGISTRY_CHECK` must not be described as a hermetic replay.

## What it teaches for C2 (registered entry commands at the branch tip)

`registry-check.py --rev` clones the lane into `mkdtemp` and symlinks the fleet
siblings next to it (contract B). The clone pins the lane's own bytes; the
siblings and the host toolchain are the page's "system binaries that differ
across hosts" / "absolute paths" class. Therefore a held row whose `argv`
shells into a sibling repo or a host tool is green only for that host state,
and two `--rev` runs at different times can disagree with no lane change. Cheap
bounds, in the page's own idiom: record the sibling revisions in the check
output, or restrict `--rev` rows to lane-local `argv` (python3 stdlib and lane
files). The source supports the second as hermetic and treats the first as
disclosed host dependence, not as reproducibility.

## Overlap and admission note

- **S028** (Bazel test encyclopedia) already carries the declared-dependency
  idea for tests: page lines 21-22, "Tests should be *hermetic*: that is, they
  ought to access only those resources on which they have a declared
  dependency. If tests are not properly hermetic then they do not give
  historically reproducible results." S028 owns the test-runner contract. This
  row is a different page and a different scope (builds and caches) and adds
  the cache conditional plus the concrete non-hermetic catalogue (host
  binaries, absolute paths, non-deterministic files, source-tree writes) and
  the null-sequential-build test. Recommendation: admit both; under contract
  rule 4 the L1 may decline this row and cite S028 instead, but then the
  "input set can be incomplete" teaching loses its cited ground.
- **S15** (same wave) is reading `https://bazel.build/remote/caching` — the
  action-cache key. Adjacent, not duplicate: S15 covers key composition
  (inputs/command/environment hash), this row covers input-set completeness and
  the classes that escape it. Keep the two `teaches` sentences distinct.
- Candidate `used-by` when mined: `corpus/README.md` F5 (hermetic environment
  normalization, currently open and citing S015, S016, S028) and the round-17
  knowledge/lesson entry that states the C1 limit. Neither was written here.

## Remaining unknowns

- No git commit pin exists for the page (404 on the guessed raw path, 403 on
  the commits API). A deploy id plus body sha256 is the available pin; that is
  at least as strong as S052's accepted "no commit pin exposed" anchor.
- When the page last changed before this fetch is unknown: `last-modified` is
  regenerated per request and the API was rate-limited. `recheck: 180d` is set
  because the text is unversioned docs.
- The v2 instruments do not exist at the tip —
  `.ufo/evidence/round-17/measure.py`,
  `.ufo/evidence/round-17/coldread/trace-inputs.py`,
  `.ufo/evidence/round-17/coldread/assemble.py`, `tools/registry-check.py`
  and `tools/registry.json` are all absent. Sweep:
  `for p in <the five paths>; do git cat-file -e 98bea7d:"$p"; test -e "$p"; done`
  reported `absent_at_tip` and `live: absent` for every path. Everything said
  about them above is read from the round's interface contract, not from
  executed code; the C1/C2 teaching is therefore design-level until the L1
  builds them.

Verdict: **built** — the page was opened live on 2026-10-20 (markdown alternate
5,947 B, sha256 `76167a0d…`), a 19-word verbatim quote at §Benefits:41-42 and
its supporting host-binaries sentence at §Identifying-non-hermeticity:63-64 are
recorded, the row is drafted and passes the frozen census with a demonstrated
red-before; the teaching for C1 is that pinned inputs are necessary but not
sufficient, because host binaries, absolute paths and source-tree writes remain
outside the recorded input key.
