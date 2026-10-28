# T56W1ExecReaderSchema — reader-report validator (round 56, wave 1)

**Deliverable:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/validate-readers.py`
(743 lines, stdlib only, `--selftest`; sha256 `a5c5711f927db8cd8bfab328fb0362616962815d04ce473d1265d992321ea784`, 31413 bytes).
Nothing committed; no lane production file and no frozen instrument touched.

## What it is

The gate the L1 runs before the C1 bind. For every heading frozen in
`.ufo/evidence/round-56/c1/lost-headings-at-base.json` (18 at base), it requires a **committed** report
under `.ufo/waves/round-56/w2` or `.../w3` whose path matches the **frozen round-56 C1 counter's own
glob** (`/T56W\d+.*Read.*\.json$`, copied verbatim from `c1/measure.py` arm 4 so this gate can never be
laxer than the counter it gates) with:

| key | requirement |
|---|---|
| `heading` | exactly one frozen heading string (no trailing space, no reflow) |
| `cand` | 40-hex, equal to the content commit C0 (full hex, not a prefix) |
| `section_sha256` | the sha256 of that heading's section bytes **at C0**, computed by the **frozen round-18 `sectionize`** loaded from the git blob at C0 — never a reimplementation; the blob is pinned to `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` (identical at base `981c5e8b` and at the freeze `c3e2ca9f`) |
| `findings` | a list |
| `commands` | a non-empty list of strings |

plus a committed `.md` **beside** it (same stem, same directory) that names the heading and runs at
least one of those commands verbatim.

Usage for wave 2 (the re-key directory only exists after the wave-3 bind, so wave 2 must name C0):

```
python3 .ufo/waves/round-56/validate-readers.py --lane LANE --rev <report commit> --c0 <C0> --explain
python3 .ufo/waves/round-56/validate-readers.py --selftest
```

Wave 3 may omit `--c0`: it is then derived exactly as the counter derives it (the single
`.ufo/evidence/round-21/coldread/rekey-r56-<12hex>` directory at REV, resolved, REV-or-ancestor).
Exit 0 iff PASS, 1 on refusal, 2 on usage/IO error. Verdict line:
`READERS_R56: rev=.. c0=.. r18=.. headings=.. passed=../.. failed=.. refusals=.. warn=.. xrev=.. READERS_R56_PASS=..`

## Refusals (the five the seat spec names, plus what operability needs)

`READER_MISSING` (no report for a frozen heading — includes a report filed only under `w1`), `READER_CAND_MISMATCH`,
`READER_HASH_MISMATCH`, `READER_MD_MISSING` (absent sibling `.md`, `.md` not naming the heading, or `.md` quoting
none of the listed commands), `READER_FINDINGS_NOT_LIST`, `READER_COMMANDS_EMPTY` (absent / not a list / empty /
non-string entry), `READER_HEADING_MISSING` (report has no usable `heading`), `READER_JSON_INVALID`,
`HEADING_ABSENT_AT_C0`, `HEADING_AMBIGUOUS`, `C0_UNRESOLVABLE`, `C0_NOT_ANCESTOR`, `REV_UNRESOLVABLE`,
`R18_MISSING`, `R18_SECTIONIZE_DRIFT`, `SKILL_MISSING_AT_C0`, `HEADINGS_UNREADABLE`.
Non-refusing warnings: `READER_HEADING_UNFROZEN` (dead weight, not harm), `READER_FINDINGS_EMPTY`.

Two design choices worth the L1's attention:

1. **`READER_HASH_XREV_DRIFT`** — the counter reads sections at **REV**, the seat spec pins reports at **C0**.
   Where the two disagree the counter refuses a report that is right at C0, so this gate refuses it first and
   names both hashes. In the normal flow (`SKILL.md` untouched after C0) `xrev=0`. This is the arm that catches
   a post-C0 `SKILL.md` edit before the bind, instead of after it.
2. **Unknown frozen-set headings are warnings, not refusals** — an extra report for a heading outside the 18
   cannot harm the bind, and refusing on it would block the L1 on dead weight. A report with *no* `heading` is
   a refusal (`READER_HEADING_MISSING`): it cannot be scoped and cannot be credited.

## Evidence (command → output, all receipts under `w1/T56W1ExecReaderSchema-receipts/`)

### 1. Selftest — 30 cases, 0 failed (`selftest.txt`)

`python3 .ufo/waves/round-56/validate-readers.py --selftest` →
`SELFTEST: cases=30 failed=0`. Synthetic git tree (`git init` in scratch, `rev-parse --show-toplevel`
asserted equal to the fixture before any commit), the **real** round-18 `measure.py` copied in at its lane
path, a fixture `SKILL.md` whose `## Beta` body contains a fenced `## Fenced not a heading` line — so the
`frozen-sectionize-shape` case (4 sections, not the 5 a naive splitter would report) fails if anyone ever
swaps in a reimplementation. Cases: accept arm; missing heading; report filed outside w2/w3; wrong cand;
non-hex cand; wrong hash; missing `.md`; `.md` without the command; `.md` without the heading; findings not a
list; empty findings (warns, still passes); empty commands; non-string command; heading key absent; unfrozen
extra (warns, still passes); invalid JSON; C0-after-REV drift; r18 blob drift; C0 derived from the re-key
directory; two re-key directories (refused); ancestor C0 accepted; descendant C0 refused; the c0==rev
fixed-point check; and four CLI wiring cases (exit 0 accept, exit 1 refusal, exit 1 unresolvable rev, exit 2
non-empty `--work`).

### 2. Before arms on the lane (`before-arms.txt`)

| command | output |
|---|---|
| `--lane LANE --rev 981c5e8b --c0 981c5e8b` | 18 × `REFUSE READER_MISSING`, `passed=0/18 … READERS_R56_PASS=false`, exit 1 |
| `--lane LANE --rev 981c5e8b` (derivation) | `REFUSE C0_UNRESOLVABLE no single rekey-r56-* directory at rev=981c5e8b20a2 (dirs=none)`, exit 1 |
| `--lane LANE --rev c3e2ca9f --c0 981c5e8b` | 18 × `REFUSE READER_MISSING`, exit 1 |

The arm is live at both the base and the freeze revision: zero reports exist in either tree.

### 3. Accept arm on the real 18 headings (`clone-arm2.txt`)

Scratch clone (`git clone --shared` of the lane, `checkout --detach 981c5e8b`, toplevel asserted), then:
C0 = one commit editing only `## Standing rules` (the sole heading whose text changes this round); 18 reports
with `cand=C0` and C0-computed hashes; commit.

`READERS_R56: rev=561c1a274174 c0=6602e67df665 r18=7ca87a7c9819 headings=18 passed=18/18 failed=0 refusals=0 warn=0 xrev=0 READERS_R56_PASS=true` (exit 0).

The same run asserts, in the clone, that the C0 edit moves `## Standing rules` (`acfb671afd76` → `9f67b4842e7f`)
and **no other frozen heading** — i.e. the other 17 report hashes are the base hashes.

### 4. Refusal arms on the real headings (`clone-arm2.txt`)

* report for `## Standing rules` carrying the **base** hash while C0 changed it →
  `REFUSE READER_HASH_MISMATCH … c0-sha256=9f67b4842e7f`, `passed=17/18`, exit 1;
* a post-C0 edit to `## Standing rules` with the reports left at C0 →
  `REFUSE READER_HASH_XREV_DRIFT … c0-sha256=9f67b4842e7f rev-sha256=95bb9ba31000`, `xrev=1`, exit 1.

### 5. Agreement with the frozen C1 counter (`clone-arm.txt`)

Same clone, same report set, the **frozen** `.ufo/evidence/round-56/c1/measure.py --explain`:

| report set | this gate | frozen counter arm 4 |
|---|---|---|
| 18 valid reports at C0 + `rekey-r56-<c0>` | `passed=18/18 PASS=true` | `EXPLAIN arm4-readers 18/18` |
| same with one rotated hash | `passed=17/18`, `READER_HASH_MISMATCH` | `EXPLAIN arm4-readers 17/18` |

The counter's other arms fail there for reasons this seat does not own and that are the known round-56
before-state: `arm1-precheck … cand_credited=46 lost=18 RED`, `arm2-monitor covered=46 score=6 box3=False`,
`arm3-rekey rekeyed=0/18` (no ledger entries bound yet), and `arm6-restate row_score=8 row_commit=d33053f7552d
score_at_row=6` — the R55.3 defect, restated from the instrument itself, not from the task text.

### 6. Attack sweep — six arms, all refused (`sweep.txt`)

| attack | result |
|---|---|
| S1: all 18 valid reports filed under `w1` (the seat's own directory) | `passed=0/18`, 18 × `READER_MISSING` |
| S2: valid structure, each report carrying **another** section's sha256 | `passed=0/18`, 18 × `READER_HASH_MISMATCH` |
| S3: heading string with a trailing space | `passed=0/18`, 18 × `READER_MISSING`, 18 × `READER_HEADING_UNFROZEN` |
| S4: one report named `T56WRead-…` (no digit after `T56W`, misses the counter's glob) | `passed=17/18`, `READER_MISSING` for that heading |
| S5: one report with a `.json.bak` suffix | `passed=17/18`, `READER_MISSING` for that heading |
| S6: all reports valid, every sibling `.md` deleted | `passed=0/18`, 18 × `READER_MD_MISSING` |

### 7. Freeze discipline and census

* All 10 files in `.ufo/evidence/round-56/freeze.json` hash to their pinned values (checked twice: before
  writing, and after all runs). No frozen instrument was modified.
* `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → `census_exit=0`
  (140 rows; the W04 duplicate-URL warnings are pre-existing and unrelated to this seat). This seat adds no
  `SOURCES.md` row, so the end-of-round census is unaffected by it.
* No mutating git command ran in the lane. Mutations happened only inside scratch clones, each preceded by
  `git -C <clone> rev-parse --show-toplevel` equal to the clone path (asserted in every driver script).

## Defects found, and what they cost

1. **My own, caught by the selftest's first run and fixed before any claim:** the helper was written
   `def git(repo, *args)` while every call site passes `-C repo …`, so the first argument was swallowed and
   `git <path> show …` ran instead. Every `git show` would have returned `None`, i.e. the gate would have
   reported 18/18 `READER_MISSING` *and* 0/18 hashes on a correct tree — a silent false refusal. The
   selftest failed on `git-init` on the first execution and this was fixed; nothing in the report rests on
   the broken build. Recorded because it is the exact class of defect this round exists to stop.
2. **Selftest fixture, caught by the selftest itself:** the post-C0-drift case edited a string that does not
   occur in the fixture `SKILL.md`, so the arm silently proved nothing (`xrev=0`, PASS). Fixed by editing a
   string that exists; the arm now reads `REFUSE READER_HASH_XREV_DRIFT … xrev=1`.
3. **State-space fact the L1 should know:** a report set can never name as `c0` the commit that contains it —
   that is a hash fixed point. So **C0 is always a strict ancestor of the commit carrying the reports**, and
   the reports must be written in a commit *after* C0. The selftest asserts the fixed point stays refused
   (`c0-strict-ancestor-of-reports`) rather than pretending to test an unreachable accept.
4. **Instrument observation (no edit proposed):** `freeze.json` mixes path bases — nine keys are relative to
   `.ufo/evidence/round-56/`, but `tools/receipt-revision-gate.py` is relative to the **lane root**. A naive
   resolver (evidence-dir-relative for all keys) reads that one entry as `MISSING`, i.e. as freeze drift that
   is not there. Resolving each key against the evidence dir then the lane root gives 10/10 pinned. The C2
   instrument must be using lane-root resolution; if it is not, its own freeze arm is reading a phantom drift.
5. **Default-path note:** `--headings` defaults to `<lane>/.ufo/evidence/round-56/c1/lost-headings-at-base.json`,
   which exists only at revisions at or after the freeze commit. A clone checked out at base has no such file;
   the gate then prints `REFUSE HEADINGS_UNREADABLE` and exits 1 — it fails loudly and can never pass with
   `headings=0` (`passed()` requires `headings>0`). Pass `--headings` when validating a tree older than the freeze.

## What wave 2 must produce (operational, from the measurements above)

* file name `T56W<digits>…Read….json` (digits required — `T56WRead.json` is not credited) under
  `w2/` or `w3/`, with the `.md` beside it quoting the heading line and the command verbatim;
* `cand` = the full 40-hex C0; `section_sha256` = the section's hash **at C0**, computed with the frozen
  round-18 `sectionize` on the C0 bytes. For 17 of the 18 headings that equals the base hash below; for
  `## Standing rules` it does **not** (C0 rewrites it), so that one must be recomputed at C0, never copied
  from base — copying it is the `READER_HASH_MISMATCH` / `READER_HASH_XREV_DRIFT` refusal demonstrated above;
* `findings` a list, `commands` a non-empty list of strings, at least one of which appears in the `.md`.

Base section table measured with the frozen `sectionize` at `981c5e8b` (64 sections, no duplicate headings,
all 18 present; start/end are 1-based inclusive line numbers of the blob):

| heading | start | end | sha256 (base) |
|---|---|---|---|
| `## Context gate classification and explicit exit classes — round 15` | 1639 | 1705 | `132cfb9ef1aa…` |
| `## Effective expectation reconciliation — round 14` | 1593 | 1626 | `6110606ea4a9…` |
| `## Live-tree re-pin and entry-command monitor — round 17` | 1844 | 1875 | `6395900104ed…` |
| `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 146 | 260 | `77d88c022646…` |
| `## Pin disposition and provenance correction — round 13` | 1546 | 1576 | `1fa3130bc6d4…` |
| `## Repeated controls and gate registry — round 12` | 1508 | 1527 | `3a78cbfcef65…` |
| `## Standing rules` | 17 | 44 | `acfb671afd76…` (**changes at C0**) |
| `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 936 | 949 | `430dd86f25b6…` |
| `## The operator's runbook and the six-leg regression (round 10, measured)` | 1299 | 1307 | `636e850f885c…` |
| `### Gate/probe registry` | 1528 | 1545 | `99285e24a71a…` |
| `### Round-13 gate/probe registry` | 1577 | 1592 | `896722c49418…` |
| `### Round-15 gate/probe registry` | 1706 | 1736 | `78edbb693cdd…` |
| `### Round-17 gate/probe registry — re-pin and monitor` | 1876 | 1884 | `309f83283e75…` |
| `### Round-18 gate/probe registry — routed-defect closure` | 1955 | 1967 | `661f63518af6…` |
| `### Round-21 gate/probe registry — finite environment differential` | 1994 | 2133 | `eccd3ec82207…` |
| `### Round-26 gate/probe registry — report interop` | 2162 | 2201 | `cc23587b353f…` |
| `### The service's limits — what tameshi refuses to mutation-test` | 1269 | 1298 | `7e240e714c6e…` |
| `### Triggers T1–T3 and the re-pin rule` | 1087 | 1109 | `2350210704ef…` |

(The full drift map is another seat's item; this table is the byproduct of computing the hashes, and it is the
exact set of numbers the 17 unchanged readers must reproduce at C0.)

## Residual gap — what this gate cannot see

The `section_sha256` is computable from the tree without reading the section, so a **fabricated** reader
report satisfies every check here. This is the same hole the round-56 contract states for C1 arm 4
(`cannot_see`: "a fabricated reader report satisfies arm 4"), and it is not narrowed by this tool: the `.md`
check only proves that a command is *quoted* next to the heading, not that it ran or that anyone read the
output. The adversarial wave seats remain the only guard; this gate removes the mechanical ways a report can
be wrong (stale revision, stale hash, wrong directory, wrong name, missing prose) and nothing more.

## Risks for the L1

* **C0 must be a strict ancestor of the report commit** (defect 3 above): bind the reports in a commit after C0.
* **`## Standing rules` must be re-read after C0, not before**: its hash changes at C0. Any reader that
  computed its hash at base will be refused with a named code, not silently credited.
* **Any `SKILL.md` edit after C0** turns 17/18 into `READER_HASH_XREV_DRIFT` and the counter's arm 4 into
  `17/18`; the gate names the heading and both hashes.
* `--work`, when given, must be empty (mirrors the counter's discipline); omit it to get a temp dir.

## Tooling

No install or upgrade was needed or performed; the tool is stdlib-only on the host's Python 3.14.8.
