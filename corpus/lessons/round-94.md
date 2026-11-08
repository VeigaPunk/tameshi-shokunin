# Round 94 — lesson (tameshi)

Base `a8f0e14bd400002324793d82030431696435d9a7` (round-93 verifier spot-check tip).
Freeze `fdbd18c672afb0474a72ad90f9ba6604ddc34001`; instrument revision
`7084358c732ebe1334c2eb9a352c3ed96b547f7c`. Two claims this round: R94-C1, coverage —
the fifth attempt at certifying the round-90 fleet-gate mutation case, under a reader
that anchors the gate identity in its own self-pinned bytes; R94-C2, calibration —
conjunct disposition with a reason test that must name a battery state or a pin digest,
and a frozen falsifiable floor.

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S321 GitHub Flavored Markdown Spec, §4.10 Tables (extension) | re-opened (A, `mined`, no status change) | https://github.github.com/gfm/, re-fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 08:53:23 GMT`, 508 310 B, sha256 `b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220` — byte-identical to the round-93 snapshot (`.ufo/evidence/round-94/sources/s321.html`, headers `s321.headers`, text `s321.txt`) | "The table is broken at the first empty line, or beginning of another block-level structure" (15 words) and "a single header row, a delimiter row separating the header from the data" (13 words). Re-opened because this round's QUALITY 165 adds the delimiter-width rule and the remainder-row policy, and both rest on this page: "The header row must match the delimiter row in the number of cells." is the delimiter rule, while "The remainder of the table's rows may vary in the number of cells. If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted. If there are greater, the excess is ignored" is the remainder policy. |
| S322 CommonMark Spec 0.31.2, §4.5 Fenced code blocks | re-opened (A, `mined`, no status change) | https://spec.commonmark.org/0.31.2/, re-fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 08:53:28 GMT`, 514 698 B, sha256 `c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d` — byte-identical to the round-93 snapshot (`.ufo/evidence/round-94/sources/s322.html`) | "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." (17 words). Re-opened because QUALITY 164 extends the fence rule from the note reader to the `coverage` scan: if a fence opens a literal block for one reader it must for every reader in the same instrument. |
| S320 sha256sum(1) re-opened (admitted round 92) | re-opened, no status change | https://man.archlinux.org/man/sha256sum.1.en, re-fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 08:53:29 GMT`, 12 127 B, sha256 `b968bc09839877f9b0bf892b8a37fce0f72f4fa0ff0f17208824161b8547277b` — byte-identical to the round-92/93 snapshots | "Print or check SHA256 (256-bit) checksums." (6 words). Re-opened because QUALITY 163 moves the gate identity into the counter's own self-pinned sha256, so the digest ground the seal rests on is re-checked rather than inherited. |
| Candidate: keep the gate identity in the lane's spec + `pins.json` (round-93 arrangement) | reject | `.ufo/waves/round-93/w1/R93SN1-probe18.log`; round-93 plan A3 | Round 93's seal compared the spec to itself: one lane commit repointing the spec and regenerating `pins.json` executed a foreign gate while printing `pin=true pins=true green=true canary=true`. Keeping that arrangement would re-open the same class. Flip: re-admit only if the pin file is anchored outside the lane's own commit graph (e.g. a fleet-root object the lane cannot rewrite), which is not available to this lane. |
| Candidate: name the `canary` and `unstable0` conjuncts falsifiable | reject | round-94 battery state `timeout`; `plans/round-94.plan.md` § Claim 1 | The `timeout` state exercises `green` and `inconclusive0`; it does not move `canary` or `unstable0`, and no committed lane state can (the gate bytes are now anchored by `GATE_SHA256` in the self-pinned counter). Declaring them falsifiable would be a wider claim than the battery shows. They stay `unfalsifiable` with a state/digest-naming reason under QUALITY 166. |

## Registry changes logged this round

| Row | Field | Old | New | Why |
|---|---|---|---|---|
| S320 | `used-by` | `corpus/lessons/round-92.md, corpus/lessons/round-93.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | the same plus `corpus/lessons/round-94.md` | This round re-opened S320 for the self-pin digest ground (QUALITY 163). No status, tier, scope, anchor or recheck change. |
| S321 | `used-by` | `corpus/lessons/round-93.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | the same plus `corpus/lessons/round-94.md` | Re-opened for the delimiter-width and remainder-row rules (QUALITY 165). No other field changed. |
| S322 | `used-by` | `corpus/lessons/round-93.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | the same plus `corpus/lessons/round-94.md` | Re-opened for the fence rule's extension to the `coverage` scan (QUALITY 164). No other field changed. |

No row was added this round: the three sources were already held, and the round's new
rules are narrower statements of ground these rows already carry. Registry rows
182 → 182 (command under § Sources census).

## Claim and kill

See `plans/round-94.plan.md` for the frozen predicate, the enumerated battery-state set
and the declared limits. This file records the gate above at the instrument revision; the
`## Measurements` and `## Wave` sections are appended in the records commit.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **the battery's own count was wrong in the plan before any seat scored.** The plan's Controls section named 31 hostile rows and the claim sentence said "thirty-five"; the battery actually registers 37 states plus 8 removal/setup extras = 45. Found by counting the driver's `states()` against the plan table, pre-scoring. | `plans/round-94.plan.md` (pre-freeze text at the freeze commit's parent, "thirty-five hostile states") vs `python3 -` enumeration of `.ufo/evidence/round-94/c1/controls-v94.py` `states()` → 6 positive + 30 hostile + 1 gate setup = 37 (+8 extras) = 45; corrected in `33279f40` | a one-line enumeration, not a rule — the same class as round-93 M3 | a freeze checklist item carried forward: every count in a claim sentence is re-derived from the driver's own `states()` (not from the plan's table, which the plan's author also wrote). |
| M2 | **a frozen artifact was edited after its freeze commit.** `claims.json` was patched to carry the freeze revision, which cannot exist inside the commit it names (fixpoint); the edit was reverted to the committed bytes and the revision recorded in `.ufo/waves/round-94/freeze-rev.txt` instead. | `git show master:.ufo/waves/round-94/claims.json | grep '"freeze"'` → `null`; the working-tree edit and its revert in `33279f40`'s tree; `freeze-rev.txt` | nothing — the helper would have committed a rewritten frozen file had it been listed; the check is a rule absent from this lane's pre-commit sweep | QUALITY 167 (appended below): a file inside a freeze commit cannot name that commit, so the freeze revision lives in a sibling receipt; a frozen artifact is never edited to carry it. |
| M3 | **the wave-spec generator's drift check compared a value no claim file carried.** The spec blob's sha256 is not in `claims.json` (it is derived into `pins.json`), so `SPEC_CONST_DRIFT spec` refused the first generator run. | first run of `.ufo/waves/round-94/make-spec.py` → `SPEC_CONST_DRIFT spec`; the generator now checks the two claim instruments against `claims.json` and names the spec pin's real home | the generator itself, correctly refusing | state the drift check's population where the population is: counter and driver against `claims.json`, spec against `pins.json` (the value the counter derives). A check that demands a value in the wrong file is a false refusal, not a finding. |
| M4 | **the C2 reason test was initially unfalsifiable in the wrong direction.** The new state/digest test rejected the *clean* selftest fixture because the fixture's own reason ("needs a nondeterministic gate, which the sealed pin forbids") names a mechanism but no state. | `python3 -I .ufo/evidence/round-94/conjunct-disposition-v94.py --selftest` first run → `SELFTEST clean FAIL findings=1 ... reason-names-no-state-or-digest`, `7/8 pass`, exit 1; fixed fixture → `8/8 pass` | the selftest's own clean case | a reason test's positive control must satisfy the test: keep one clean case whose reason names a real state, and one cheat case whose reason names only a mechanism word. Both are now fixed selftest cases. |

## Measurements

Frozen commands (the same the plan names):

    python3 -I .ufo/evidence/round-94/c1/measure-v94.py --repo . --rev 7084358c --work <empty dir>
    → C1_SUMMARY rev=7084358c… n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0
      trivial=0 witnessed=7/7 note=present mismatched=0 badrows=0 verdict_tables=1
      C1_SOURCE S320=row:1,quote:1 S321=row:1,quote:1 S322=row:1,quote:1
      C1_R94_PASS=true, exit 0        (.ufo/evidence/round-94/pre-freeze/controls/pos-real.out)

    python3 -I .ufo/evidence/round-94/c1/controls-v94.py --lane . --rev 7084358c \
      --base a8f0e14b --work <empty dir> --outdir <dir> --jobs 6
    → C1_CONTROLS states=45 matched=45 mismatches=0 missing=0, exit 0
      (.ufo/evidence/round-94/pre-freeze/controls/C1-summary.txt)

    python3 -I .ufo/evidence/round-94/conjunct-disposition-v94.py --lane . --rev 7084358c --min-falsifiable 17
    → DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0, exit 0
    python3 -I .ufo/evidence/round-94/conjunct-disposition-v94.py --selftest
    → DISPOSITION_SELFTEST: 8/8 pass, exit 0   (.ufo/evidence/round-94/pre-freeze/c2-selftest.out)

    python3 -I .ufo/evidence/round-94/c1/controls-v94.py --canary-selftest
    → CANARY_SELFTEST: PASS, exit 0

Do-nothing controls: `nowork-base` (`C1_SETUP spec-absent-at-rev`, exit 2),
`c2-nowork-base` (`DISPOSITION_SETUP counter-absent-at-rev`, exit 2), and the A4
mechanism-word cheat (a finding under the new reason test; the round-93 checker printed
`findings=0` on it).

## Sources census

    /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
    → `tameshi ok …/corpus/SOURCES.md`, exit 0 (before and after; W04 duplicate-URL warnings unchanged)

Rows: 182 content rows before → 182 after (`grep -cE '^ {0,3}\| S[0-9]{3,}' corpus/SOURCES.md`).
