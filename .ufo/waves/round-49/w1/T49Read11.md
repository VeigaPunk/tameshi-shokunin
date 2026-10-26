# T49Read11 — C1 reader, `### The map`, ordinals 6–11

Base `8ca67421111fa354b47b803358391d0b07fc6db9`. Section `### The map — where a reader
enters, artifact by artifact` at `SKILL.md:1380-1395` (rows `:1384-1394`). Deliverable
`.ufo/waves/round-49/w1/T49Read11.rows.json` (`{"rows": [...]}`, 6 rows).

Read-only seat: the lane was never written; no counter was run for a verdict (only the
frozen `--list` mode, which prints pointers and no judgement). No tools installed or
upgraded, so no tooling record. Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read11`
(removed before yield).

## Verdicts

| ord | raw | kind | target | base_verdict |
|---|---|---|---|---|
| 6 | `corpus/knowledge/service-optin-protocol.md` | path | same | **holds** |
| 7 | `corpus/knowledge/fleet-suite-census.md` | path | same | **holds** |
| 8 | `corpus/knowledge/service-standing-state.md` | path | same | **holds** |
| 9 | `tools/mutate-and-run.sh` | path | same | **holds** |
| 10 | `corpus/README.md` | path | same | **holds** |
| 11 | `plans/round-N.plan.md` | path | none | **absent** |

All six are whole-file path pointers, so only support is at issue; there is no line-span
drift dimension for them (the frozen extractor agrees: `ranges: null` on all six).

## Per-pointer findings

### 6 — `corpus/knowledge/service-optin-protocol.md` → holds
Row: `` | `corpus/knowledge/service-optin-protocol.md` | request shape, the re-pin rule,
read-only guarantees, report shape, boundaries | `` (`SKILL.md:1387`). All five items are
present in the target:
- `:6-8` — "what a lane brings (request shape), what stays untouched (read-only
  guarantees), who absorbs (owner-hardens discipline), and what comes back (report shape)".
- `:59-62` — the re-pin rule: "A moved substrate needs a re-pin, never a re-interpretation
  of the old table".
- `:23-26` — boundaries: "Scope, stated so it is not over-claimed … single-edit mutants
  only; hermetic suites only; results are per-revision and per-host"; `:75-77` — "The
  service never edits, repairs or re-pins the gate; a needed change is a recommendation to
  the owner, not a patch".
- Section headings: `:54` request shape, `:109` read-only guarantees, `:182` report shape.
Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show
8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/service-optin-protocol.md |
awk 'NR>=6&&NR<=8 || NR>=23&&NR<=26 || NR>=54&&NR<=62 || NR>=75&&NR<=77 || NR==109 || NR==182'`.
Excerpt (156 chars, quoted from `:6-8`): "what a lane brings (request shape), what stays
untouched (read-only guarantees), who absorbs (owner-hardens discipline), and what comes
back (report shape)."

### 7 — `corpus/knowledge/fleet-suite-census.md` → holds
Row: `` | `corpus/knowledge/fleet-suite-census.md` | the suite census: the offer and the
queue (surveyed-but-unmeasured pins) | `` (`SKILL.md:1388`). Offer at `:269-275` ("The
offer (standing; no current commitment) …"); §5 heading `:249`; queue at `:277` ("Queue
(projection, ordered by expected yield — most static protection last):"); the updated
queue R.4 at `:594-615` is surveyed-but-unmeasured by construction — `:607` "Still
unmeasured, kumitate's five, order unchanged from §5" and rows `:612-615` each read
`unmeasured`. Both halves of the row (offer, queue) and the parenthetical are
demonstrably on the page.
Command: `… show <base>:corpus/knowledge/fleet-suite-census.md | awk 'NR>=260&&NR<=292 ||
NR>=594&&NR<=622'`.
Excerpt (212 chars, from `:269-271`): "**The offer (standing; no current commitment):**
any lane may ask tameshi to run a sweep on one of its gates. What a sweep needs from the
owner: a pinned revision (sha256) and a hermetic suite invocable on a copy".

### 8 — `corpus/knowledge/service-standing-state.md` → holds
Row: `` | `corpus/knowledge/service-standing-state.md` | the boundary note:
fleet-visible vs lane-owned, handoff conditions, SC1–SC3 | `` (`SKILL.md:1389`). Header
`:3-8` defines both directions and the handoff conditions (quoted below); §1 `:49`
fleet-visible artifacts, §2 `:68` lane-owned, §3 `:80-83` "A handoff is not a file move:
it is the set of conditions under which a claim becomes citable", §4 `:157-188` with the
literal labels SC1 `:159`, SC2 `:174`, SC3 `:181`. Nothing in the row is unbacked.
Command: `… show <base>:corpus/knowledge/service-standing-state.md | awk 'NR>=1&&NR<=20 ||
NR>=68&&NR<=84 || NR>=157&&NR<=190'`.
Excerpt (242 chars, from `:5-7`): "**fleet-visible** (committed, citable, re-derivable by
a lane that did not run the case) and what stays **lane-owned** (scratch, in-flight state,
the substrates themselves) — plus the **handoff conditions** that put something across the
line."

### 9 — `tools/mutate-and-run.sh` → holds
Row: `` | `tools/mutate-and-run.sh` | the instrument: `--selftest`, `--regression`
(six-leg registry at round 11, seven since round 16, eight since round 18, nine since round
26; git-materialized replay) | `` (`SKILL.md:1391`). Both modes are in the usage block
`:196-199`; `--selftest`'s contract is `:151-168`; the registry count matches the row
literally — `:83` "… r10-2 six legs; r16 seven; r18 eight; r26 nine", `:659`
`regression_specs() { # <dir> — write the nine embedded case specs`; the nine legs are
named at `:216-217` (js-kimi-census … js-cite-check) and the replay is git-materialized at
`:218-219` ("materialized from the repo's git object store (`git show <rev>:<path>` —
immune to working-tree drift").
Command: `… show <base>:tools/mutate-and-run.sh | awk 'NR>=83&&NR<=90 || NR>=145&&NR<=225'`.
Excerpt (349 chars, from `:215-219`): "--regression replays every recorded mutation case as
a leg: (js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify,
bash-checklist-run, js-claims-check, js-round-gate, js-sources-check, js-cite-check) at its
pinned revision, materialized from the repo's git object store (`git show <rev>:<path>` —
immune to working-tree drift;".

### 10 — `corpus/README.md` → holds
Row: `` | `corpus/README.md` | the coverage map — one row per note, holds + sources | ``
(`SKILL.md:1392`). The target has the map at `:3` ("## Coverage map"), the table header
`| Note | Holds | Sources |` at `:5`, one row per note at `:7-15`, and the fleet-round-1
addendum map with the same three columns at `:45-61`. Row count observed: `git -C LANE show
<base>:corpus/README.md | grep -c '^| `knowledge/'` → `62`.
Command: `… show <base>:corpus/README.md | sed -n '3,6p'; … | grep -c '^| `knowledge/'`.
Excerpt (42 chars, from `:3-5`): "## Coverage map | Note | Holds | Sources |".

### 11 — `plans/round-N.plan.md` → absent
The token is a naming convention, not a file; the section says as much in the same row
(`SKILL.md:1393`: "no separate round-11 record file exists (the wave deliverables are the
record, `LOG.md:316-317`)"). Resolution fails at base:
`git -C LANE cat-file -t 8ca67421111fa354b47b803358391d0b07fc6db9:plans/round-N.plan.md`
→ `fatal: path 'plans/round-N.plan.md' does not exist in
'8ca67421111fa354b47b803358391d0b07fc6db9'` (rc 128); the sibling
`plans/round-N-record-draft.md` (ordinal 12, not my range) fails the same way, while
`plans/round-11.plan.md` and `plans/round-10-record-draft.md` are blobs at base
(`cat-file -t` → `blob`). The frozen counter admits this shape only as a path pointer with
`file` null and a row whose verdict is `absent`; `excerpt` is therefore empty and no text
is claimed to support it.

Proposed fix (in `rows.json` under `proposed_fix`, optional — `absent` already passes the
counter, the fix gives the reader a resolvable instance without dropping the convention
pointer):

- `skill_old`: ``| `plans/round-N.plan.md`, ``
- `skill_new`: ``| `plans/round-N.plan.md` (latest `plans/round-11.plan.md`), ``
- `fixed_file`: `plans/round-11.plan.md`, `fixed_ranges`: null
- `fixed_excerpt` (116 chars, from `plans/round-11.plan.md:13-14`): "Case frame — **the
  final round**. tameshi round 11 is the tenth *training* round (r10) and the arc has no
  successor."

`skill_old` occurs exactly once in the section (`section.count(old) == 1`, and once in the
whole file). The inserted token extracts as a new path pointer, so C1 must also add a
`holds` row for it (the three `fixed_*` fields above); the map floor (17) rises rather than
falls. The edit touches only the first token of the cell so the sibling
`plans/round-N-record-draft.md` pointer (ordinal 12) and that reader's own fix stay
independent.

## Excerpt check (self-run, as the item requires)

Every non-empty excerpt was tested against the base blob before it was written, using the
counter's own collapse rule (`re.sub(r'\s+', ' ', text).strip()` over the whole pointed
file), and the length window 24–400:

```
6  corpus/knowledge/service-optin-protocol.md   len=156  in_target=True
7  corpus/knowledge/fleet-suite-census.md       len=212  in_target=True
8  corpus/knowledge/service-standing-state.md   len=242  in_target=True
9  tools/mutate-and-run.sh                      len=349  in_target=True
10 corpus/README.md                             len=42   in_target=True
11 (absent — no target, excerpt empty)          —
fix plans/round-11.plan.md                      len=116  in_target=True
```

Also checked: each `claim` is verbatim in the section (`section.count(claim) == 1` for all
six — the six claims are the row's `Holds` cell text, so they are quoted, not paraphrased).
Pointer list confirmed against the frozen extractor in its read-only listing mode:
`python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev
8ca67421111fa354b47b803358391d0b07fc6db9 --list` prints ordinals 6–11 exactly as in
`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json` (`:null` ranges, `file`
null only for ordinals 11–12).

## Findings

1. **No stale pointer in ordinals 6–11 at base.** Five of six path pointers are supported
   by the file they name, on the exact points their rows claim; the sixth is an absent
   pattern token the section itself declares a convention. Reads softening would have been
   possible (e.g. accepting `plans/round-N.plan.md` as "holds by convention"), and it was
   not used: the token resolves to no blob, so it is `absent`, not `holds`.
2. **One absent pointer, admissible but readable-worse.** `plans/round-N.plan.md`
   (`SKILL.md:1393`) sends a reader to a non-existent path; the row's own remedy is that
   the wave deliverables are the record. The proposed one-token insert gives the row a
   resolvable instance without deleting the pointer (map floor 17 is a minimum).
3. **The row at `SKILL.md:1393` is shared with ordinal 12** (`plans/round-N-record-draft.md`,
   another reader's pointer). My fix is scoped to the first token only; if the L1 merges
   both readers' edits in one pass, the two inserts are independent. Flagging so the L1
   does not apply a whole-cell rewrite that drops one of them.
4. **The `--regression` leg count is a live number that can lapse.** `tools/mutate-and-run.sh`
   matches the row today (`:83`, `:659`: nine legs, r26). Any future leg addition makes
   `SKILL.md:1391`'s parenthetical stale without touching the pointer's resolution — a
   drift the frozen counter cannot see (it checks resolution + excerpt, not the number).
   Recorded as a calibration risk, not a defect at base.
5. **Bounds compliance.** Lane checkout unmodified apart from this report and
   `T49Read11.rows.json`; the only counter invocation was `--list` (no `--rev` tree work,
   no judgment); no file under `/home/vgpnk/.local/state/`, no C2 witness stdout, no fleet
   repo, no sibling lane, no `git add/commit/stash/checkout/switch/reset/pull/push` and no
   `jj` mutation was touched.

## Known limits

- The verdicts are semantic support of a five-item `Holds` cell against a whole file; they
  are **not** durable-record, re-key, or monitor results, and they decide nothing. The
  deciding run is the L1's.
- Path pointers carry no line span, so "stale because the lines moved" cannot apply to this
  range; only ordinal 11 has a resolution failure, and it is by construction of the token.
- The excerpt is one contiguous span (24–400 chars); for rows whose `Holds` cell lists more
  items than one span can quote (§6: five items; §9: two modes plus a registry), the note
  field gives the additional line anchors rather than a longer quote.
- `absent` carries an empty excerpt because there is no pointed text to quote; the counter
  requires only `file: null` + verdict `absent` for that shape.

## Summary
- Six pointers read at base: ordinals 6–11 of `### The map` (`SKILL.md:1387-1393`).
- Five verdicts `holds`: service-optin-protocol, fleet-suite-census, service-standing-state, tools/mutate-and-run.sh, corpus/README.md — each backed by quoted base text and named lines.
- One verdict `absent`: `plans/round-N.plan.md` (no blob at base; a declared naming convention), with a one-token fix that adds a resolvable `plans/round-11.plan.md` instance.
- No stale line-drift finding is possible for path pointers; no pointer in this range is unsupported.
- All excerpts pass the counter's collapse + 24–400 window check against the base blobs (self-run, output above).
- Deliverable: `.ufo/waves/round-49/w1/T49Read11.rows.json` (6 rows, `proposed_fix` on ordinal 11).
- Read-only seat: only this report and the rows file written; no verdict claimed, no deciding counter run.
