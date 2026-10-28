# T56W1ScribeSources — SOURCES.md row draft (milestone: SOURCES row draft)

Seat: T56W1ScribeSources · round 56 wave 1 · lane tameshi-shokunin · base 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 · instrument freeze c3e2ca9f020776b3d66c7af854fb82c834674fcf.

## Deliverable: the two table rows (verbatim)

The mined row for the source opened this round. The URL and pin follow the
scout's own record (`.ufo/evidence/round-56/assimilation/in-toto-statement-v1.json`,
accessed 2026-10-28T18:42:42Z by `T56W1ScoutSource`): it opened the tag-pinned
URL `blob/v1.2.0`, not `blob/main`. Same bytes either way (sha256 cbe684a1…ebea).

```
| S281 | Statement layer specification (in-toto Attestation Framework, Statement v1) — https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md | spec | A | what an in-toto Statement v1 applies to: a subject identified by digest, not git receipt encoding and not DSSE verification | §Fields, `subject` field, snapshot lines 36-37 and 54-55 @ spec/v1/statement.md tag v1.2.0 (commit df02077b; body sha256 cbe684a1…ebea, identical at main 50bf0171), fetched 2026-10-28 | an attestation applies to a subject identified by digest and subjects are matched purely by digest, so a statement naming another revision is about that revision and not evidence for the measured one | mined | 2026-10-28 | on-release | corpus/knowledge/receipt-revision-binding.md |
```

One REJECTED candidate row (the spec actually opened this round and honestly
evaluated; it is the in-toto *predicate* layer, not the statement layer):

```
| S282 | Build: Provenance (SLSA specification, predicate type slsa.dev/provenance/v1) — https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md | spec | A | SLSA's build-provenance predicate, not a statement-level subject binding | §Model, first paragraph @ spec/build-provenance.md on main, blob sha256 efece57a…76fc (path last changed ba7d291a, 2026-10-19), fetched 2026-10-28 | REJECTED: the predicate records that a build platform produced artifacts through execution of a buildDefinition, answering who built what and not which revision a measurement certifies; S281 carries the rule; flip: the lane publishes signed build provenance for its own artifacts and needs builder.id and buildType | rejected | 2026-10-28 | on-release | — |
```

## Grounding (measured, commands in receipts)

- Registry max at base: `S280` (`grep -oE '^ {0,3}\| S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | tail -1` → `S280`), so the next unused id is **S281**; S282 unused. Idle gaps S038-S255 exist; the seat rule is next-after-max, so S281.
- 140 rows at base; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, `tameshi<TAB>ok`, 16 warnings (15×W04 + 1×W01 S101), 0 errors. Receipt: `T56W1ScribeSources-receipts/census-base.txt`.
- No prior row names `in-toto/attestation` or `slsa-framework/slsa` (grep → exit 1); duplicate URL is not a risk. Receipt: `census-clone-final.txt`.
- Scout's opened artifact sha256 = `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`, identical to my independent fetch of the same URL (receipt `fetch-statement.txt`, artifact `in-toto-statement-v1.md`). Anchor lines 36-37 / 54-55 verified against the snapshot bytes at `.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md:54-55` — the quoted sentence spans lines 54-55 in the file.
- Located quote for the lesson `## Gate` (11 words, §Fields → `subject` → IMPORTANT paragraph, snapshot lines 54-55): "Subject artifacts are matched purely by digest, regardless of content type."
- Rejected candidate opened: `spec/build-provenance.md` on `slsa-framework/slsa@main`, sha256 `efece57a…76fc`, §Model sentence ("Provenance is an attestation that a particular build platform produced a set of software artifacts through execution of the `buildDefinition`."). Artifact `slsa-build-provenance.md`. The v1.1 rendered page is marked Retired (v1.2 is Approved but client-rendered); the normative markdown at main is the citable pin.

## Validation in a scratch clone (never the lane)

`git clone --shared` of the lane → `checkout --detach 981c5e8b`, rows inserted before `## Paths`, a stand-in `corpus/knowledge/receipt-revision-binding.md` created for E11, then `sources-census.sh validate <clone>`:

- exit 0, `clone<TAB>ok`, no new findings; both rows NF=11 cells. Receipt `census-clone-final.txt`.
- Negative controls (each reverts after firing): E11 fires on S281 when the used-by file is removed; E01 `fields=12` when one `\|` is injected into the teaches cell; E01 `fields=10` when one column is dropped. Receipt `census-controls.txt`.
- Ordering note for the L1: S281's `used-by` resolves only once `corpus/knowledge/receipt-revision-binding.md` exists on disk — land both in C0 and run the census after C0, not before.

## FINDING F1 (frozen-instrument defect, C2 counter — report only, never edit)

`.ufo/evidence/round-56/c2/measure.py:245` reads `cells[8] == 'mined'`; the
status cell of a registry row is `cells[7]` (cells[8] is `opened`, e.g.
`2026-10-28`). Consequence: the `mined` set is always empty, the
knowledge-entry docs arm can never increment, `docs` is capped at 3/4, so
`total ≥ 1` and `C2_R56_PASS` can never be true — the claim is unfalsifiable
as instrumented.

Demonstrated, not just read (receipt `c2-arm6-defect.txt`):

- Scratch clone at the freeze `c3e2ca9` + fixture commit `fee76603272487275fff6032a5bef43ae285d249` containing all four docs-arm conditions (QUALITY.md names the gate + a code; knowledge note header `source:/verified-at:/recheck:` + `S281`; SKILL.md contains `receipt-revision-gate`; `tools/registry.json` cell carries three refusal codes) and both registry rows committed.
- Frozen counter: `EXPLAIN arm6-docs 3/4` → `docs=3/4 total=2 C2_R56_PASS=false`.
- A scratch **copy** of measure.py patched `cells[8]`→`cells[7]` (frozen file untouched): `EXPLAIN arm6-docs 4/4` → `docs=4/4 total=1`.
- Standalone parse replication on the real registry (`c2-mined-parse.txt`): `cells[8]=='mined'` → mined set size 0; `cells[7]` → 113 rows, matching the reviewer's mined count.

Disposition is the L1's call (fix is a one-index change; the instrument is
frozen, so presumably wave-1 records the defect and the L1 decides whether C2
can hold at all). Related: the scout's proposed status for the new row was
`queued until the entry cites it`; the frozen counter requires `mined` —
S281 must land as `mined` in C0 or the arm loses its last remaining point.

## Items deliberately not in the row (quote discipline)

The ≤25-word located quote is for `corpus/lessons/round-56.md` `## Gate`,
not the row cell — handed to `T56W1ScribeLesson` via this report.

## Provenance / tooling

- No installs or upgrades needed; stdlib + curl + the fleet census script only.
- Lane production files untouched: `git -C tameshi-shokunin status` shows my seat's only writes are under `.ufo/waves/round-56/w1/T56W1ScribeSources*` and receipts; frozen `.ufo/evidence/round-56/` bytes untouched.
- Scratch: `$HYAKU_SCRATCH/tameshi-r56/T56W1ScribeSources` (clone + fixture + artifacts); fixture commits `9f18e441`, `fee76603` live only inside the clone.
