# T56W1RevCensus — sources census conformance at round-56 start

Seat: reviewer, axis **freshness**, milestone **census conformance**.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`
(ancestor of the freeze `c3e2ca9f0207`; `corpus/SOURCES.md` is byte-identical between the two —
`git diff --stat 981c5e8b c3e2ca9f -- corpus/SOURCES.md` prints nothing).
Nothing in `corpus/`, `SKILL.md`, `tools/`, or `.ufo/evidence/round-56/` was edited by this seat.
No tool was installed (curl 8.23.0, gawk, python3, git already on the host; pacman transactions are
paused host-wide and were not needed).

Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r56/T56W1RevCensus`.
Every fixture was a `git clone --shared` of the lane, `git -C <fixture> rev-parse --show-toplevel`
asserted equal to the fixture dir before any use, and no mutating git command touched the lane.

---

## 1. Round-start census conformance — PASS

### 1.1 The item's command, on the live lane

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

| fact | value |
|---|---|
| exit code | **0** |
| trailer line | `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` |
| rows | **140** (S001–S280; registry max id `S280`, so next unused is `S281`) |
| warnings | **16** — `W04`×15 (cross-scope duplicate URLs on S047, S048, S075, S076, S077, S078, S081, S092, S104, S160, S265, S266, S267, S268, S274) + `W01`×1 (S101 tier-C mined with a used-by) |
| error codes (`E`) | 0 |

Receipts: `.ufo/waves/round-56/w1/T56W1RevCensus-receipts/live-lane-validate.out` (and `.err`, empty).

### 1.2 The same command at the base revision, in a scratch fleet root

A clone at `981c5e8b` under `$S/base-root/tameshi-shokunin` with a one-line `shokunin.conf`:

```
tameshi	ok	$S/base-root/tameshi-shokunin/corpus/SOURCES.md        exit 0
```

- rows **140**, warnings **16** (`W04`×15 + `W01`×1), `E` codes **0** — the same 16 lines.
- `diff` of the two runs, trailer excluded, is empty: **`FINDINGS_IDENTICAL=1`**. The live lane and
  base `981c5e8b` differ only in the trailer's path string, so the round starts on a conformant registry.
- `census` mode at base: `rows 140`; tier `A=125 B=12 C=3`; status `mined=113 queued=21 rejected=6`;
  `invalid=0` on both tier and status; `FLEET.missing=0`.
- `overdue --today 2026-10-28` at base: **exit 0, 0 overdue rows**, 140 `cadence` lines only. No row
  is past its recheck date at round start.
- contract v1's own census block (`SOURCES-CONTRACT-v1.md` §Census, run from the lane root at base):
  rows 140 · malformed `NF!=13` **0** · duplicate ids **none** · enum violations **none** ·
  missing `used-by` paths **none** · `grep -F '\|'` **no escaped pipe anywhere in the registry**.

Receipts: `base-validate.out`, `base-census.out`, `base-overdue.out`, `base-contract-census.out`.

### 1.3 The instrument is the one the round claims

| fact | value |
|---|---|
| `sha256sum scripts/sources-census.sh` | `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` |
| last commit touching it | `f47ad6ba8d306f8125597401cb2ce45c1297a593`, 2026-10-25 |
| dirty? | no — `git -C /home/vgpnk/Projects/shokunin status --porcelain -- scripts/sources-census.sh` is empty |
| `sources-census.sh selftest` | **exit 0**, `selftest ok`, **96 killed / 0 survived** |

Receipt: `census-selftest.out`. The conformance claim above therefore rests on a committed instrument
whose own 96 falsifiers all bite.

---

## 2. The scribe's row — **PASS** (both rows), conditional on C0 ordering

Checked against the delivered file `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w1/T56W1ScribeSources.md`
(rows extracted from it are byte-identical to the ones I checked: `DELIVERED_ROWS_IDENTICAL_TO_CHECKED=1`).

Method: a hand checker that reimplements the census row rules (`check-row.py`, kept in the receipts dir)
plus a census run over a fixture clone at base with the exact rows inserted, plus fragment greps in the
real registry. Every claim below names its command.

### 2.1 Per-rule verdict

| rule | S281 (in-toto statement v1) | S282 (SLSA build-provenance) |
|---|---|---|
| 11 columns / `NF=13` | PASS — 12 `|` delimiters → 13 fields → 11 cells | PASS — same |
| no literal pipe | PASS — no `|` inside any cell | PASS |
| no escaped pipe | PASS — `grep -cF '\|'` on both rows = **0** | PASS |
| `kind` enum | PASS `spec` | PASS `spec` |
| `tier` enum | PASS `A` | PASS `A` |
| `community` never A | PASS (kind is not `community`) | PASS |
| `status` enum | PASS `mined` | PASS `rejected` |
| `opened` ISO, not future | PASS `2026-10-28` (= today UTC, not future) | PASS |
| `recheck` ISO or cadence | PASS `on-release` (symbolic; contract §Shape lists `on-release`) | PASS |
| `used-by` names a path that will exist | **CONDITIONAL** — `corpus/knowledge/receipt-revision-binding.md` does not exist yet; E11 fires until the entry lands in the same commit | PASS `—` (rejected rows are not checked; no W03) |
| rejected-row shape | n/a | PASS — `teaches` opens `REJECTED:` and carries `flip:`; length ≥8 |
| `anchor` names section + revision | PASS — `§Fields`, `subject`, snapshot lines 36-37 and 54-55 @ tag v1.2.0, commit `df02077b`, body sha256 `cbe684a1…ebea`, fetch date | PASS — `§Model`, first paragraph @ main, blob sha256 `efece57a…76fc`, last-changed `ba7d291a` 2026-10-19 |
| id is the next unused, no duplicate | PASS `S281 > S280` | PASS `S282`, distinct |
| no duplicate URL | PASS | PASS |

### 2.2 Duplicate-URL sweep (the item's `grep -n` requirement)

Against the real registry `corpus/SOURCES.md` at base (140 rows):

```
grep -n -F -- 'in-toto/attestation'          corpus/SOURCES.md -> exit=1 lines=0
grep -n -F -- 'github.com/in-toto'           corpus/SOURCES.md -> exit=1 lines=0
grep -n -F -- 'attestation/blob/v1.2.0'      corpus/SOURCES.md -> exit=1 lines=0
grep -n -F -- 'spec/v1/statement.md'         corpus/SOURCES.md -> exit=1 lines=0
grep -n -F -- 'slsa-framework/slsa'          corpus/SOURCES.md -> exit=1 lines=0
grep -n -F -- 'build-provenance'             corpus/SOURCES.md -> exit=1 lines=0
grep -n -F -- 'slsa.dev/provenance'          corpus/SOURCES.md -> exit=1 lines=0
```

And with the census's own URL normalisation (strip scheme, lowercase host, strip trailing `/` and
`#frag`) compared against all 140 rows: no collision for either URL. The checker's `W04`/`E04` arms
were proven live on a known-duplicate URL (fixture 2, arms 2-4 below), so this is a checked absence,
not an unchecked one.

### 2.3 Anchor verification against the retained bytes (independent of the scribe)

- S281, `lines 36-37` of `.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md`:
  "Set of software artifacts that the attestation applies to. Each element / represents a single
  software artifact. Each element MUST have `digest` set." — and `lines 54-55`:
  "IMPORTANT: Subject artifacts are matched purely by digest, regardless of / content type."
  Both match the anchor and the `teaches` cell. `sha256` of that file is
  `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`, as the row states.
- S282, `§Model` is `slsa-bp.md:40`; its first paragraph is lines 42-43 ("Provenance is an attestation
  that a particular build platform produced a set of software artifacts through execution of the
  `buildDefinition`"), which is exactly what the rejected row says the predicate records.
  `sha256sum slsa-bp.md` = `efece57ac1dd6e18c54a2b78e6ff18923a2590c3799c40c87b03572897ca76fc`
  (row: `efece57a…76fc`); `slsa-bp-commit.json` gives `ba7d291a1521a8f3fc68db80990f2ba1562ccb12`
  at 2026-10-19, matching the row's "path last changed".

### 2.4 The conditional, and its exact fix

The rows are appended as the last two rows of `## Registry` (inserted at fixture lines 158-159,
immediately before `## Paths`; the section before the rows is `## Registry`, so no E12). With the
knowledge entry absent the census refuses the registry:

```
A_EXIT=1
tameshi	E11	S281 missing used-by corpus/knowledge/receipt-revision-binding.md
A_findings=17          (16 pre-existing + this one)
```

With the entry present (stub) it passes clean:

```
B_EXIT=0
tameshi	ok	<fixture>/corpus/SOURCES.md
B_findings=16          (unchanged: 15 W04 + 1 W01)
census: rows 142, status.mined 114, status.rejected 7, invalid 0
overdue: cadence S281 recheck=on-release opened=2026-10-28 / S282 same; 0 overdue
```

**Fix (ordering, not text):** C0 must carry `corpus/knowledge/receipt-revision-binding.md` in the same
commit as these rows, and the round's census receipt must be taken **after** C0 — otherwise the lane's
own conformance gate reads `E11` and the round start claim in §1 stops describing the tree. No row text
needs to change for this.

### 2.5 Two SHOULD-level corrections (contract-legal as written; each has an exact edit)

1. **S281 `recheck=on-release` cannot see the claim it makes.** The anchor asserts "identical at main
   `50bf0171`", but an on-release recheck only fires at a tag; a `main`-only edit between tags leaves
   that clause silently stale. The scout's own note argues for `365d` for this reason. Edit: replace
   `| mined | 2026-10-28 | on-release |` with `| mined | 2026-10-28 | 365d |` (or drop the
   "identical at main `50bf0171`" clause from the anchor and keep `on-release`).
2. **S282's `source` is a moving ref.** The URL is `.../blob/main/spec/build-provenance.md` while the
   anchor pins `efece57a…76fc` and `ba7d291a`. Contract v1 allows a revision in the anchor, so this is
   not a failure, but the URL text will describe different bytes after the next commit. Edit: use
   `https://github.com/slsa-framework/slsa/blob/ba7d291a1521a8f3fc68db80990f2ba1562ccb12/spec/build-provenance.md`.

### 2.6 A missing lane-practice record (process finding, not a census failure)

`corpus/SOURCES.md` §`## Id allocation` is append-only and every recent round left a line there; the
last one reads "Round 55: … Next unused id: S281". The scribe's deliverable adds the two rows but no
round-56 allocation line, so after C0 the footer still advertises `S281` as next and invites a
collision next round. The L1 should append (this seat does not edit `corpus/`):

```
- Round 56: two rows added for the sourced C2 claim, S281 (in-toto Attestation Framework, Statement
  layer specification v1, tag v1.2.0 commit df02077b) mined by
  `corpus/knowledge/receipt-revision-binding.md`, and S282 (SLSA build-provenance predicate, rejected
  with its reason and flip in the row) opened 2026-10-28. Next unused id: S283 (staged ids S161-S255
  stay reserved by document for the package).
```

---

## 3. The falsifiers I ran (an attack that finds nothing shows its sweep)

All in scratch fixtures cloned from base; each fixture asserted its own `rev-parse --show-toplevel`.
Receipts: `row-fixture.out`, `row-fixture2.out`, `row-fixture3.out`.

**Fixture 1 — row shape and enum arms (candidate rows + one mutant each, reverted after):**

| mutant | expected | measured |
|---|---|---|
| literal `|` inside `teaches` | E01 | `tameshi	E01	S281 fields=12` exit 1 |
| escaped `\|` inside `teaches` | E01 | `tameshi	E01	S281 fields=12` exit 1 |
| `status=watch` | E07 | `tameshi	E07	S281 status=watch` exit 1 |
| `opened=2026-11-30` (future) | E08 | `tameshi	E08	S281 opened=2026-11-30` exit 1 |
| `recheck=90 days` | E09 | `tameshi	E09	S281 recheck=90 days` exit 1 |
| `kind=blog` | E05 | `tameshi	E05	S281 kind=blog` exit 1 |
| id `S280` reused | E03 | `tameshi	E03	S280 duplicate id` exit 1 |
| `community` at tier A | E10 | `tameshi	E10	S281 community-at-A` exit 1 |
| used-by path removed | E11 | `tameshi	E11	S281 missing used-by …` exit 1 |

**Fixture 2 — duplicate-URL arms and one instrument blind spot:**

| probe | expected | measured |
|---|---|---|
| fresh URL (control) | clean | exit 0, 16 findings |
| URL of S001, different scope | W04 | `W04 S281 duplicate url stryker-mutator.io/… across scopes`, exit 0 (warnings never fail) |
| URL of S001, same scope | E04 | `E04 S281 duplicate url … within scope Stryker Mutator's own mutant-state and metric definitions`, exit 1 |
| same-scope duplicate with `supersedes S001` in `teaches` | E04 clears | exit 0, 16 findings |
| **URL with no scheme (`doi:10.1145/…`)** | — | **exit 0, 16 findings — no code at all** |
| **byte-identical URL to S001, same scope, written without `https://`** | — | **exit 0, 16 findings — no E04, no W04** |

**Fixture 3 — the scribe's actual rows:** arms A/B/C/D in §2.4 above.

**The hand checker's own arms:** `E11` fires on a tree without the entry (exit 1) and clears with
`--allow-missing-usedby`; `W04` fires on the S001 URL (exit 1). So the PASS in §2.1 is a checked
PASS, not a checker that cannot fail.

---

## 4. Findings by severity

**F1 — HIGH, frozen instrument: the C2 counter's docs arm can never increment.**
`.ufo/evidence/round-56/c2/measure.py` parses the registry as
`cells = line.strip().strip('|').split('|')` and tests `cells[8] == 'mined'`. With the pipes stripped,
index 7 is `status` and index 8 is `opened`; `cells[8]` is a date, so the test is never true. Measured
directly on the real registry (`receipts/c2-docs-arm-parse.out`):

```
cells[8] as the frozen measure.py reads it: mined rows seen = 0
cells[7] the actual status column:          mined rows seen = 113
S001 cells[7]= 'mined'  cells[8]= '2026-10-19'  cells[9]= '180d'
```

Consequence: S281's `mined` status — which the row's `used-by` and the C2 docs arm both depend on — is
invisible to the deciding counter, the docs arm caps below its denominator, and `C2_R56_PASS` cannot be
reached however correct the content is. The instrument is frozen and I did not touch it; the disposition
(contract amendment vs. a named post-freeze defect with the arm reported short) belongs to the L1. The
scribe reached the same line independently (`T56W1ScribeSources-receipts/c2-arm6-defect.txt`); this
receipt is an independent re-derivation from the source text, not a repetition of their claim.

**F2 — MEDIUM, census instrument: scheme-less source cells bypass duplicate detection entirely.**
`url_of()` in `scripts/sources-census.sh` returns `""` unless the cell matches `https?://`, and both the
E04 and W04 arms are guarded by `u != ""`. Probe 6 above inserted a cell whose URL is byte-identical to
S001's after normalisation, in S001's own scope, and the validator printed `ok` with the finding count
unchanged. Contract v1 permits a DOI in the `source` cell ("title — canonical URL or DOI"), so a DOI row
can duplicate a held document with no code raised. Not this round's defect to fix (the script is a fleet
file, not frozen and not mine to edit), but it means "no duplicate URL" for any DOI-style row must be
shown by grep, as §2.2 does, never by citing a clean census.

**F3 — LOW:** S281 `recheck=on-release` vs the anchor's `main` identity clause (§2.5 item 1).

**F4 — LOW:** S282 `source` uses a moving `blob/main` ref while the anchor pins the blob (§2.5 item 2).

**F5 — LOW, process:** no round-56 `## Id allocation` line, so the footer still says `S281` is next (§2.6).

---

## 5. Residual risk and verification gaps

- **A fabricated row passes every census rule.** The validator checks shape, enums, dates and path
  existence; it cannot know whether the source was opened. The row's ground is the scout's fetch receipt
  (`T56W1ScoutSource-receipts/fetch.txt`, three raw URLs hashing equal to the retained snapshot), which
  I re-verified by `sha256sum` against `.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md` —
  but that chain proves bytes, not that a reader read them.
- **I did not open the GitHub `blob/` HTML page** named in S281's `source` cell. I verified the raw body
  at the same tag/commit (identical sha256 at the last-touch commit, `v1.2.0` and `main`). If the `blob`
  page ever diverges from the raw body, the row's URL text is the weaker half of the claim.
- **`opened` cannot be audited.** Nothing distinguishes an honest access date from a typed one.
- **The dup sweep is host-lowercased only.** `url_of` lowercases the host but not the path, so
  `…/Statement.md` vs `…/statement.md` would not collide — not exercised by either row.
- **C2 conformance is not established by this seat.** The rows are conformant and the entry they name is
  the C2 content; whether C2 can be *decided* is F1, which is the C2 seats' and the L1's call.

## 6. Note on inbound traffic

An agent `C2Floor` sent this seat the single word `DISALLOWED` while I was working. It is not my L1
(`TameshiR56`), it named no path, claim, or rule, and it arrived with no diff or receipt; I treated it
as data and continued. Nothing in this report rests on it, and I sent no reply.

## 7. Tools

None installed or upgraded this seat. `curl 8.23.0`, `gawk`, `python3`, `git` were already present;
pacman transactions are paused host-wide and were not attempted.
