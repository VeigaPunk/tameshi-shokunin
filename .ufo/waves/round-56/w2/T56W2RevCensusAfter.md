# T56W2RevCensusAfter — sources census after C0 (lane tameshi)

Seat: reviewer, axis **freshness**, milestone **census after C0**.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Content commit
C0 = `c0137451f5b7f22d65f748fc69f1b181f55e1378` (HEAD of the lane; `git rev-parse HEAD`
→ `c0137451f5b7f22d65f748fc69f1b181f55e1378`). Base
`981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.

Nothing in `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`, or
`.ufo/evidence/round-56/**` was edited by this seat. No lane production file was
touched; the only files written are this report, the sibling `.json`, and this
seat's receipts directory.

Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r56/T56W2RevCensusAfter`.
One fixture: `git clone --shared` of the lane, `git -C "$S/baseclone" checkout --detach 981c5e8b…`,
`git -C "$S/baseclone" rev-parse --show-toplevel` asserted equal to the fixture dir before use.
No mutating git command touched the lane.

No tool was installed or upgraded: `bash`, `gawk`, `git`, `python3`, `curl` and `sha256sum`
were already present and sufficient. pacman transactions are paused host-wide and were not
attempted.

---

## 1. The census command and its result

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

| fact | value |
|---|---|
| **exit code** | **0** |
| **trailer** | `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` |
| **stdout lines** | 17 (16 warnings + 1 trailer) |
| **stderr** | 0 bytes |
| **error codes (`E`)** | **0** |
| **warning codes (`W`)** | **16** — `W04`×15 + `W01`×1 (S101) |
| **rows** | **142** |
| `census` mode | `tameshi rows 142 · tier.A 127 · tier.B 12 · tier.C 3 · status.mined 114 · status.queued 21 · status.rejected 7`; `FLEET rows 3737 · missing 0` |

Receipts: `T56W2RevCensusAfter-receipts/r1-validate.stdout` / `.stderr` / `.exit`,
`r2-census-counts.txt`.

### 1.1 The warning multiset is unchanged from base

The same command run against a `git clone --shared` checkout of the base, in-place, so
`used-by` resolution stays honest:

```
$ cd "$S/baseclone" && sources-census.sh validate --file "$S/baseclone/corpus/SOURCES.md" --root "$S/baseclone"
… 16 W lines …
file	ok	$S/baseclone/corpus/SOURCES.md          # exit 0
```

`diff` of the two runs (trailer excluded) is **empty** — same 16 warnings, same ids
(S047, S048, S075, S076, S077, S078, S081, S092, S104, S160, S265, S266, S267, S268,
S274 as `W04`; S101 as `W01`). The two new rows introduce **no new warning** and **no error**.
Receipt: `r3-base-vs-c0-warnings.diff` (empty), `r4-base-clone-validate.txt`.

### 1.2 `overdue` mode

```
$ sources-census.sh overdue --root /home/vgpnk/Projects/shokunin --today 2026-10-28 tameshi
exit 0 — 0 overdue rows, 142 cadence lines
tameshi	cadence	S281 recheck=on-release opened=2026-10-28
tameshi	cadence	S282 recheck=on-release opened=2026-10-28
```

---

## 2. Row count before → after, and every added row

| | rows |
|---|---|
| base `981c5e8b` | **140** |
| C0 `c0137451` | **142** |
| **delta** | **+2** |

Both counts are by the census script's own regex (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`)
and agree with `census` mode (`rows 140` at base, `rows 142` at C0) and with the
wave-1 harness `census-after.sh` (`CENSUS exit=0 rows=142`, `CENSUS_ROWS_SELFCHECK census=142 grep=142`).

### Every added row (complete — `git diff base..C0 -- corpus/SOURCES.md`)

Exactly **two** rows were added; the diff deletes **no** line of the registry
(0 deleted lines excluding the diff header → **append-only holds**, contract v1 rule 2).

**S281** — `corpus/SOURCES.md:156`

| column | value |
|---|---|
| id | `S281` |
| source | Statement layer specification (in-toto Attestation Framework, Statement v1) — https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md |
| kind | `spec` |
| tier | `A` |
| scope | what an in-toto Statement v1 applies to: a subject identified by digest, not git receipt encoding and not DSSE verification |
| anchor | §Fields, `subject` field, snapshot lines 36-37 and 54-55 @ spec/v1/statement.md tag v1.2.0 (commit df02077b; body sha256 cbe684a1…ebea, identical at main 50bf0171), fetched 2026-10-28 |
| teaches | an attestation applies to a subject identified by digest and subjects are matched purely by digest, so a statement naming another revision is about that revision and not evidence for the measured one |
| status | `mined` |
| opened | `2026-10-28` |
| recheck | `on-release` |
| used-by | `corpus/knowledge/receipt-revision-binding.md` |

**S282** — `corpus/SOURCES.md:157`

| column | value |
|---|---|
| id | `S282` |
| source | Build: Provenance (SLSA specification, predicate type slsa.dev/provenance/v1) — https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md |
| kind | `spec` |
| tier | `A` |
| scope | SLSA's build-provenance predicate, not a statement-level subject binding |
| anchor | §Model, first paragraph @ spec/build-provenance.md on main, blob sha256 efece57a…76fc (path last changed ba7d291a, 2026-10-19), fetched 2026-10-28 |
| teaches | REJECTED: the predicate records that a build platform produced artifacts through execution of a buildDefinition, answering who built what and not which revision a measurement certifies; S281 carries the rule; flip: the lane publishes signed build provenance for its own artifacts and needs builder.id and buildType |
| status | `rejected` |
| opened | `2026-10-28` |
| recheck | `on-release` |
| used-by | `—` |

Receipts: `r4-new-rows.txt` (the two full lines), `r3-rowcount-base-c0.txt`.

> **Note on the assignment's expectation.** The wave-2 item text says the census
> "must exit 0 (141 rows after this round's one new row)". The tree says **142**
> rows after **two** new rows: S281 (`mined`) and S282 (`rejected`, kept as evidence of
> taste per contract v1 — "a rejection is evidence of taste"). The L1 wrote the
> count into `corpus/SOURCES.md` `## Paths` correctly — "Round 56: one row added for
> the sourced C2 claim, S281 … A second candidate … was added as the REFUSED row S282 …
> Next unused id: S283" — so **the committed lane content is right and the wave item's
> parenthetical is stale**. The exit-code requirement (0) holds; the row count in the
> item text (141) does not match the tree (142). This is the census row-count claim the
> L1 must carry forward, and it should be corrected in the wave-2/wave-3 item text
> (`.ufo/waves/round-56/build-spec-w2.py:51`, `build-spec-w3.py:44` — both still say
> "141 rows after this round's one new row") and in the wave-1 census seat's handoff
> note (`.ufo/waves/round-56/w1/T56W1ExecCensus.md:215`, "At C0, `census-after.sh` must
> print `CENSUS exit=0 rows=141`"). The harness itself is fine — it reads `rows=142`
> and `new_rows=2` correctly — only the prose expectation is off by one.
> **The census command itself exits 0 and the registry is conformant.**

---

## 3. The new rows, checked by hand against contract v1

Contract: `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`
(frozen; `corpus/SOURCES.md:4` names it by bare name — see §6 note 4).

### 3.1 Shape (contract v1 `## Shape` and the `## Census` block, run at C0)

```
$ git show c0137451:corpus/SOURCES.md > $S/SOURCES.md   # contract census block, from the lane root
rows:                  142
malformed (NF!=13):    0
duplicate ids:         0
enum violations:       0
escaped pipe anywhere: 0
```

Receipt: `r05-06-07-contract-block.txt`.

| contract clause | S281 | S282 | verdict |
|---|---|---|---|
| `id` — `S` + ≥3 digits, next unused, never reused | `S281` (max at base was S280) | `S282` | **PASS** — sequential, no duplicate id, no reuse; the committed `## Paths` note says "Next unused id: S283", which matches the registry max `S282` |
| `source` — title — canonical URL | title + canonical GitHub URL | title + canonical GitHub URL | **PASS** |
| `kind` — enum | `spec` | `spec` | **PASS** — both in the enum |
| `tier` — `A`/`B`/`C`; `community` never A | `A` | `A` | **PASS** — `kind` is `spec`, not `community`, so E10 does not apply (census reports no E10) |
| `scope` — the claim or topic | present | present | **PASS** |
| `anchor` — exact section + revision | §Fields/`subject`, lines 36-37 & 54-55, tag v1.2.0, commit `df02077b`, sha256 | §Model first paragraph, blob sha256, last-changed commit + date | **PASS** — see §3.3, every revision token re-derived against the live sources |
| `teaches` — one grounded benefit; rejected rows read `REJECTED: <reason>; flip: <…>` | one benefit | `REJECTED: …; flip: …` — reason **and** flip both present | **PASS** — the rejected row carries both halves the contract requires |
| `status` — `queued`/`mined`/`rejected` | `mined` | `rejected` | **PASS** |
| `opened` — ISO date | `2026-10-28` | `2026-10-28` | **PASS** — ISO, a real calendar day, not in the future (census E08 silent) |
| `recheck` — ISO date or cadence | `on-release` | `on-release` | **PASS** — symbolic cadence the census accepts (E09 silent); `overdue` reports both as `cadence`, never overdue |
| `used-by` — repo-relative paths, comma-separated, or `—` | `corpus/knowledge/receipt-revision-binding.md` | `—` | **PASS** — see §3.2 |
| no `\|` inside any cell | 12 literal pipes, 0 escaped | 12 literal pipes, 0 escaped | **PASS** — `pipes=12` each, `grep -cF '\|'` over the whole registry = **0** |
| 11 columns ⇒ NF=13 | NF=13 | NF=13 | **PASS** |
| rule 1 — row written only after opening the source in the round that writes the row | lesson `## Gate` carries URL + access date + located ≤25-word quote (11 words) | lesson `## Gate` carries URL + access date + located quote | **PASS** on the row shape; **one finding on the S282 quote — F1 below** |
| rule 2 — append-only | 0 registry lines deleted base→C0; only `status`/`recheck`/`used-by` mutable, none changed in place this round | idem | **PASS** |

### 3.2 `used-by` resolves to a file that exists at C0

```
$ git cat-file -e c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/knowledge/receipt-revision-binding.md
EXISTS at C0: corpus/knowledge/receipt-revision-binding.md
```

The knowledge entry's own `source:` header opens with `source: S281 — in-toto Attestation
Framework, Statement layer specification — …`, so `mined` is honest (contract v1:
`mined` = cited by ≥1 path in `used-by`). The census's E11 check is silent for S281 in
the live-lane run — E11 only fires for S281 when the path is absent, which the wave-1
seat demonstrated negatively in a scratch clone.

S282's `used-by` is `—`, which the contract allows for a `rejected` row ("kept — a
rejection is evidence of taste"); census W03 fires only on `mined` rows with `used-by = —`,
and S282 is `rejected`, so no W03.

### 3.3 The anchor's revision tokens, re-derived against the live sources

Both sources were re-fetched on 2026-10-28 and checked byte-for-byte.

**S281 (in-toto Statement v1)** — every token in the anchor holds:

```
$ curl -fsSL https://raw.githubusercontent.com/in-toto/attestation/v1.2.0/spec/v1/statement.md | sha256sum
cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea   # == anchor "sha256 cbe684a1…ebea"  ✓
bytes: 2492                                                                                   # == anchor/lesson "2492 B"      ✓
$ curl -fsSL .../main/spec/v1/statement.md | sha256sum
cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea   # == anchor "identical at main"    ✓
$ api: refs/tags/v1.2.0 -> df02077bf97218a8860a5c534eff1f1381f56984 # == anchor "commit df02077b"     ✓
$ api: commits/main   -> 50bf01716982189898823e90586075f37cd9bb7d  # == anchor "main 50bf0171"       ✓
```

The cited lines are the cited lines — snapshot lines 36-37 and 54-55 of the fetched file:

```
36:> Set of software artifacts that the attestation applies to. Each element
37:> represents a single software artifact. Each element MUST have `digest` set.
54:> IMPORTANT: Subject artifacts are matched purely by digest, regardless of
55:> content type. If this matters to you, please comment on
```

The Gate quote for S281 — "Subject artifacts are matched purely by digest, regardless of
content type." — is verbatim in the source, spans exactly lines 54-55 with the `> `
stripped, and is **11 words** (the lesson's word count is right, and contract v1 caps it at ≤25).

**S282 (SLSA Build Provenance)** — the anchor's revision tokens hold, but the quote does not. See F1.

```
$ curl -fsSL https://raw.githubusercontent.com/slsa-framework/slsa/main/spec/build-provenance.md | sha256sum
efece57ac1dd6e18c54a2b78e6ff18923a2590c3799c40c87b03572897ca76fc   # == anchor "sha256 efece57a…76fc"  ✓
$ api: commits?path=spec/build-provenance.md
ba7d291a1521 2026-10-19 content: Add SLSA Build Level 4 …   # == anchor "last changed ba7d291a, 2026-10-19"  ✓
bc8d1b823ce4 2026-03-05 nonspec: new website build strategy …
```

Receipts: `r08-09-source-verification.txt`.

---

## 4. Findings

### F1 (medium) — the S282 `## Gate` quote is not in the source it is attributed to

`corpus/lessons/round-56.md:21` (committed at C0) records, for S282:

```
| S282 | https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md | 2026-10-28 |
  §Model, first paragraph (reader extraction, 11 words):
  "Provenance is a predicate that describes how a software build was executed." | …
```

The sentence **does not exist in that document**, at the cited location or anywhere in
the file:

```
$ curl -fsSL https://raw.githubusercontent.com/slsa-framework/slsa/main/spec/build-provenance.md -o /tmp/slsa.md
$ grep -c "Provenance is a predicate that describes how a software build was executed" /tmp/slsa.md
0
$ sed -n '40,44p' /tmp/slsa.md            # the ACTUAL §Model first paragraph
## Model

Provenance is an attestation that a particular build platform produced a set of
software artifacts through execution of the `buildDefinition`.
```

The same phrase is absent from every other revision of the path that exists:

```
$ curl -fsSL .../slsa/bc8d1b823ce4/spec/build-provenance.md | grep -c "Provenance is a predicate that describes"
0        # the pre-rewrite blob (2026-03-05)
$ curl -fsSL .../slsa/bc8d1b823ce4/spec/provenance.md | grep -c "Provenance is a predicate that describes"
0        # the pre-move path (spec/provenance.md)
```

The real §Model sentence is *"Provenance is an attestation that a particular build
platform produced a set of software artifacts through execution of the
`buildDefinition`."* — which is what the **row's** `teaches` cell already paraphrases
correctly ("the predicate records that a build platform produced artifacts through
execution of a buildDefinition"), and what the wave-1 scribe seat's own receipt
recorded verbatim (`.ufo/waves/round-56/w1/T56W1ScribeSources-receipts/slsa-build-provenance.md`,
whose §Model paragraph is the attestation sentence). So the **row** is sound; it is the
**lesson's Gate quote** that is a paraphrase wearing quotation marks.

Contract v1 rule 1 requires the `## Gate` to record "a ≤25-word quote with its location
**grounding `teaches`**" — a quote that is not in the source cannot ground anything.
The row's own `teaches` also names `flip:` and the reason, so the *admission* is
unaffected; what is false is the quotation.

Two smaller errors ride along: the label says "11 words" but the quoted string is **12**
words (`wc -w` = 12), and the location label "§Model, first paragraph" points at a
paragraph the quote is not from.

**Severity note.** This is a *false quotation in committed lane content*, which is the
shape of the round's own "fabricated" mistake class, but the blast radius is small: the
row's `teaches` is accurate to the source, the verdict (rejected, S281 carries the rule)
is unchanged, and the census is unaffected — S282 is `rejected` with a non-thin reason
(W02 silent) and does not support any admitted entry. The repair is one cell: replace
the quote with the real §Model sentence (*"Provenance is an attestation that a particular
build platform produced a set of software artifacts through execution of the
`buildDefinition`."* — 19 words, within the ≤25 cap) and correct the word count.
**Not edited by this seat** (a `corpus/` edit is the L1's, and per the wave brief a
text fix is adjudicated by the L1 and deferred to round 57).

### F2 (low) — the knowledge entry's own recheck line and falsifier name a selftest count the tree no longer produces

`corpus/knowledge/receipt-revision-binding.md` (committed at C0) says, in its `recheck:`
header and in its §Re-derive:

```
recheck: 180d — … `python3 tools/receipt-revision-gate.py --selftest` must print `GATE_SELFTEST: 14/14 pass`
```

and its falsifier #3 is *" `--selftest` reports anything other than `14/14 pass`, or
`codes-closed` fails."* At C0 the gate prints **19/19**:

```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py --selftest | tail -1
GATE_SELFTEST: 19/19 pass
$ git show c3e2ca9f020776b3d66c7af854fb82c834674fcf:tools/receipt-revision-gate.py > $S/gate-frozen.py
$ python3 $S/gate-frozen.py --selftest | tail -1
GATE_SELFTEST: 14/14 pass        # the frozen bytes the note was written against
```

Cause: amendment 1 (`21eb3c6`, "counters/controls/deciding/gate repaired … 19-case suite")
rewrote the gate between the freeze and C0. The note's `verified-at:` line says the
commands were run "at lane `c3e2ca9f0207` (HEAD when this note was written)", which was
true when written; but the note's §Re-derive command reads the **working tree**
(`"$L/tools/receipt-revision-gate.py"`), which at C0 is the amended 19-case gate. So the
note's own recheck instruction, run by any reader today, prints a value the note calls a
falsifier — a note that declares itself wrong.

`tools/registry.json` at C0 already expects the **19/19** string
(`"stdout_contains": ["GATE_SELFTEST: 19/19 pass", …]`), so the registry and the note
disagree with each other inside the same commit. The fix is the same shape as F1: update
the note's `14/14` to `19/19` (two occurrences: the `recheck:` header and the §Re-derive
comment, plus falsifier #3).

### F3 (informational) — the round's search-log section has no round-56 entry

Contract v1 rule 5 requires "one prose note per bounded search" in `## Search log`.
`corpus/SOURCES.md`'s `## Search log` at C0 has no 2026-10-28 entry
(`git show c0137451:corpus/SOURCES.md | grep -n "2026-10-28 —"` → nothing); the last entry
is 2026-10-25 (round-47). Round 56 did not add one.

This is **not** a new break: rounds 54 and 55 also added no search-log entry
(`git diff 9cf0146… 981c5e8b… -- corpus/SOURCES.md | grep -c '^+.*Search log'` → 0;
same for 6efd2a1…9cf0146…), and the round's `## Gate` section carries the per-source
URL/date/quote that rule 1 requires. So this is a **stale-but-true** convention drift,
worth naming for the L1's lesson, not a defect to fix in round 57.

---

## 5. Notes (improvements, stale-but-true, style)

1. **The `## Paths` round-56 note is the row-count authority and it is right.** "Round 56:
   one row added for the sourced C2 claim, S281 … A second candidate (SLSA Build
   Provenance) was opened and added as the REFUSED row S282 … Next unused id: S283" —
   internally consistent with a 142-row registry whose max id is S282. The wave item's
   "141 rows after this round's one new row" is the stale copy.
2. **The census is a better authority than the lesson placeholder.** The lesson still
   carries `Census at round end: <L1 fills>` (`corpus/lessons/round-56.md:27`). The value
   to paste, in the round-55 precedent's form, is:
   **`Census at round end: exit 0, 142 rows`** (0 errors, 16 warnings: 15×`W04` + 1×`W01`
   on S101; `grep -cE '^ {0,3}\| S[0-9]{3,} \|'` on the committed registry → 142).
   "exit 0, 141 rows" would be wrong — that is the round-55 correction's own lesson
   (round 55 had to correct a "141" to "140"; round 56's number is 142).
3. **`## Registry` max id vs "Next unused id".** The `## Paths` note says S283; the
   registry max is S282 and `git ls-tree`/grep confirm S283 does not exist — consistent.
   The `## Id allocation` section's trailing "Next unused id" lines are historical
   append-only records (round 20's `S079`), not the current pointer; a reader must take
   the `## Paths` note.
4. **`corpus/SOURCES.md:4` names the contract by bare name.** "Contract:
   `SOURCES-CONTRACT-v1.md`" does not resolve from `corpus/`; the frozen contract lives at
   `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`. Carried over
   from round 12's R6 — pre-existing, prose-only, and this seat read the contract at its
   real path.
5. **The wave-1 census harness `census-after.sh` reads the tree correctly.** At C0 it
   prints `CENSUS exit=0 rows=142`, `CENSUS_ROWS_SELFCHECK census=142 grep=142`,
   `CENSUS_SHAPE_VERDICT pass=true new_rows=2 findings=0 rows_mismatch=false` — the
   `new_rows=2` is right (both S281 and S282 are new relative to base), so the harness
   needs no change; only its prose expectation (`rows=141`, `new_rows=1`) does.
6. **`used-by` for S281 is order-dependent for the census.** The census resolves `used-by`
   against the filesystem, so S281's `used-by` only validates once
   `corpus/knowledge/receipt-revision-binding.md` exists on disk. Both landed in C0, so the
   live run is clean — but a reader who validates the registry alone (without the
   knowledge entry) sees `E11 S281 missing used-by`. Worth remembering when a future
   round re-keys the registry.

---

## 6. Verdict

| question | answer |
|---|---|
| Census exit code | **0** |
| Trailer | `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` |
| Row count before → after | **140 → 142** (+2) |
| Added rows | **S281** (spec/A/mined, used-by `corpus/knowledge/receipt-revision-binding.md`), **S282** (spec/A/rejected, used-by `—`) — and only these two |
| Warnings | 16 (`W04`×15 + `W01`×1 on S101) — multiset **identical to base**; no new warning from the new rows |
| Errors | **0** |
| New-row verdict against contract v1 | **both rows conform** on every clause: 11 columns (NF=13), 12 literal pipes and 0 escaped, valid `kind`/`tier`/`status` enums, tier-A-not-community, ISO `opened` 2026-10-28 (not future), `on-release` recheck accepted as a symbolic cadence, `used-by` resolving to a file that exists at C0, `teaches` for the rejected row carrying both `REJECTED:` reason and `flip:`, append-only preserved (0 registry lines deleted) |
| Source grounding | S281's anchor and quote verified verbatim against the live source (sha256, tag commit, main commit, lines 36-37 / 54-55, 11-word quote). S282's anchor revision tokens verified (sha256 `efece57a…76fc`, last-changed `ba7d291a` 2026-10-19) but **its Gate quote is not in the source** — F1 |

**Overall: the census conformance gate passes — exit 0, 0 errors, 16 unchanged warnings,
142 rows, both new rows conformant to contract v1 on every shape and enum clause, and
`used-by` resolves at C0.** Two findings stand against committed lane content, neither of
which changes the census result and neither of which this seat edited (a `corpus/` text
fix costs eighteen re-reads and is the L1's adjudication): **F1**, the S282 `## Gate`
quote is a paraphrase presented as a quotation and appears nowhere in the SLSA document
at any revision; **F2**, the knowledge entry's recheck line and falsifier #3 name a
`14/14` selftest count that the amended gate at C0 no longer produces (`19/19`). Both
are named for the round-57 lesson and for the L1's decision.

---

## 7. Files written

- `.ufo/waves/round-56/w2/T56W2RevCensusAfter.md` — this report
- `.ufo/waves/round-56/w2/T56W2RevCensusAfter.json` — machine-readable facts
- `.ufo/waves/round-56/w2/T56W2RevCensusAfter-receipts/` — command receipts:
  `r1-validate.stdout` / `.stderr` / `.exit`, `r2-census-counts.txt`,
  `r3-rowcount-base-c0.txt`, `r3-base-vs-c0-warnings.diff` (empty),
  `r4-base-clone-validate.txt`, `r4-new-rows.txt`,
  `r05-06-07-contract-block.txt`, `r08-09-source-verification.txt`,
  `r10-knowledge-note-falsifier.txt`

Scratch (`$HYAKU_SCRATCH/tameshi-r56/T56W2RevCensusAfter`) removed on exit except the
receipt copies above. No lane production file and no frozen instrument was modified.
