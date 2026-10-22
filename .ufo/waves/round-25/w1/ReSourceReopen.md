# ReSourceReopen — R23-REATTACK of round-23 w2 `SourceReopen` (S083 own-work source)

Seat: TameshiR25.ReSourceReopen (scout, leaf). Round-23 seat TameshiR23.SourceReopen
died (accounting bundle marks it `status: failed`, `replaced: false`) and never wrote
`.ufo/waves/round-23/w2/SourceReopen.md`; no transcript survives at the recorded path.
This is the fresh attack that item owed.

**Verdict: AGREE.** The attacked binding (S083's own-work source row: path, pinned
revision, located lesson quote, tier/used-by scope, no external authority) holds at the
pinned revision `28cae179…` and still holds at lane revision `c9ff09f…`. No counterexample
found. Evidence, then the drift notes, then the (empty) correction list.

## Attacked claim

`corpus/SOURCES.md:92` (at c9ff09f; same line at HEAD) — the row round 23 wrote:

> `| S083 | Required registry command declarations — tools/registry.json | own-work | A | this lane's persisted active command identities and expected outcomes, not authenticated executions | argv and expect fields at lines7–15, revision28cae179e4dc2c1fa7f032a79cdddf0b5d862d76; tools/registry-check.py:15–38 | bind a finite declared required-command set to exact argv and retained outcomes; a source read or positive count is not the same command | mined | 2026-10-21 | on-change | corpus/knowledge/required-command-binding.md, corpus/lessons/round-23.md |`

Item: reopen the source path at its pinned revision, the lesson quote, tier/used-by scope;
no external authority inferred. Original read-only checks plus one /tmp reproduction
(authorized by the re-attack text); nothing was run inside the lane checkout.

## Observed evidence

### 1. Row immutability (no supersession of the row itself)

- `git log -G "S083" --oneline -- corpus/SOURCES.md` → only `496d212` (round-23, row
  introduction) and `66a25ab` (round-22, the `- Next unused id: S083.` footer). No later
  commit touches the row text.
- Line-by-line diff of the S083 row at `496d212` vs `c9ff09f` vs HEAD (5b69fb2):
  byte-identical both ways.
- Round-24 block `corpus/SOURCES.md:302-306` states "New tierA/mined rows S084 and S085;
  no existing row changes." `git diff --stat c9ff09f HEAD` = only `.ufo/evidence/round-25/*`
  and `.ufo/waves/round-25/*` (1685 insertions), so HEAD equals c9ff09f for every
  production file.

### 2. Pinned revision is real and resolves

- `git cat-file -t 28cae179e4dc2c1fa7f032a79cdddf0b5d862d76` → `commit`.
- `git merge-base --is-ancestor 28cae179… HEAD` → yes; commit date `2026-10-21 11:09:45 -0300`,
  subject "round-22: land verified accounting capability and full wave evidence".

### 3. Anchor "argv and expect fields at lines7–15" @ 28cae179

`git show 28cae179…:tools/registry.json | nl -ba | sed -n '1,20p'` →
lines 7–12 are the first row's `"argv": [ "python3", "tools/repeat-control.py", "--snapshot",
".ufo/evidence/round-12/ControlGate" ]`; lines 13–15 are `"expect": { "exit": 0 }`.
A whitespace-normalized token comparison of the lesson quote against the pinned span:

```
ANCHOR_NORM : "argv": [ "python3", "tools/repeat-control.py", "--snapshot", ".ufo/evidence/round-12/ControlGate" ], "expect": { "exit": 0 },
QUOTE_NORM  : "argv": [ "python3", "tools/repeat-control.py", "--snapshot", ".ufo/evidence/round-12/ControlGate" ]
QUOTE_TOKENS_PRESENT_IN_ORDER: True      EXPECT_IN_ANCHOR: True
```

The quote is a normalized inline rendering of the exact pinned bytes (only line breaks
differ); every token, in order, is present at the stated lines, and the expect field the
lesson calls "neighboring" is inside the same span.

### 4. Anchor "tools/registry-check.py:15–38"

Lines 15–38 are the `tameshi-entry-registry-v1` schema + run-semantics doc block — at the
pin, at c9ff09f, and at HEAD (identical). The only post-pin change to that file (`496d212`)
touched `run_row` around lines 645–730 (`retain_streams`), not the anchored block.

### 5. Tier / used-by / no external authority

- Tier authority: `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26`
  — tier is scoped to `scope`, never global; **A** includes "source code … the lane's own
  re-runnable gate output"; `own-work` is in the kind enum (`:78`). The scope cell bounds
  A exactly to the lane's own persisted declarations and disclaims authenticated
  executions, so this is not tier inflation; kind is not `community`.
- used-by targets exist and cite S083: `corpus/knowledge/required-command-binding.md:1`
  (`source: S083 — tools/registry.json at 28cae179…; tools/registry-check.py:15-38;
  .ufo/evidence/round-23/contract.json`) and `corpus/lessons/round-23.md:27-36`.
- No external authority enters: the source cell is a repo path (no URL/DOI), and the
  lesson states "No external specification is inferred."
- Contract census run read-only from the lane root: malformed rows `0`; duplicate ids none;
  every mined used-by path exists; enum/tier-inflation check prints nothing; S083 `NF=13`.
- Append-only receipt: `.ufo/evidence/round-23/source-invariants.json` (revision `336565fc`)
  → `added: ["S083"]`, `changed_existing: []`, `removed: []`, rows 80→81, tiers A 71→72.
- Round-23 `## Gate` carries the rule-1 content: repo path, access date `2026-10-21`,
  the ≤25-word quote with location `lines7–15`, tier scope, `mined`/`on-change`/used-by,
  bounded lookup `identified2/screened2/included2/excluded0`, stop rationale.

## Does it still apply at lane revision c9ff09f?

Yes. Reproduced in a `/tmp` extraction of c9ff09f (`git archive c9ff09f | tar -x -C
/tmp/r25-s083`), never in the lane:

| check | observed |
|---|---|
| `python3 tools/command-binding.py --selftest` | exit 0, `COMMAND_BINDING_SELFTEST: 44/44 pass` |
| frozen replay gate (`--bundle .ufo/evidence/round-23/replay/bundle.json --expected …/replay/expected.json --json`) | exit 0, `finding_ids: []`, `bundle_sha256 3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9` |
| source-read substitution (`…/source-read-bundle.json` vs `…/source-read-expected.json`) | exit 1, `finding_ids: ["ARGV_MISMATCH"]`, `bundle_sha256 db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf` |
| `python3 .ufo/evidence/round-23/measure.py --repo /tmp/r25-s083` (lesson recheck) | `discriminated 10/10`, exit 0 |

These are exactly the two discriminators the row's `teaches` cell claims ("exact argv …
a source read … is not the same command"), and both digests equal the expectations of the
round-24 pinned registry rows.

Drift since round 23 (none of it contradicts S083):

- `tools/registry.json` is additive only since the pin (`git diff --stat 28cae179 HEAD` =
  `+74`), the anchored first row `repeat-control-snapshot-clean` is still `active`, and the
  current lines 7–15 are identical to the pinned ones.
- `tools/command-binding.py` changed once, in round 24: sha256 `d533dc1e…` (at `496d212`,
  selftest `38/38`) → `9230c68e…` (at c9ff09f and HEAD, `44/44`, six extra round-24 cases
  loaded from `.ufo/evidence/round-24/extra-cases.json`). The lesson's "public selftest38/38"
  sentence is revision-stamped to `496d212` and stays true there; its `recheck:` command
  still resolves and the round-23 counter still scores 10/10 at c9ff09f.
- The three round-23 command-binding registry rows are properly superseded in round 24
  (`command-binding-selftest` → `…-selftest-r24`, `…-frozen-clean` → `…-frozen-clean-pinned`,
  `…-source-read-red` → `…-source-read-red-pinned`), each with `superseded_by` naming an
  active successor. `[INFERENCE]` the superseded `command-binding-selftest` row's needle
  `38/38` no longer matches the current tool, so that superseded row would now diverge —
  which is precisely what its supersession records; superseded rows are excluded from N/M
  by `registry-check.py`'s documented run semantics.
- No row or correction supersedes S083 (`grep "supersedes S083"` → nothing).

Residual notes, deliberately not counted as counterexamples:

- The lesson header names a third provenance item, `.ufo/evidence/round-23/contract.json`
  (lane's own round-23 contract; its `base_revision` is the same pin), that the row's
  anchor cell does not enumerate. It is own-work, not external authority, and the
  knowledge-entry header convention includes evidence paths (cf. the S085 entry naming
  `.ufo/evidence/round-24/contract.json`).
- Round-23's bounded-lookup note sits under `## Id allocation` (`corpus/SOURCES.md:296-299`)
  rather than `## Search log`; the round-22 and round-24 notes sit there too, so it is a
  lane-wide placement convention, not an S083 defect.

## Smallest safe correction

None required — the binding holds. The only bookkeeping a planner might add is noting in
the round-25 lesson that the round-23 selftest count (38/38) was superseded by 44/44; that
is record-keeping, not a repair to S083.

## Tooling

Nothing installed or updated (no pacman/uv/npx action; no package needed).

Unresolved gaps: none material. The only read that was not semantically resolved is the
tier wording's origin (kaika's contract was read from the fleet-root `.ufo/waves/kaika/`
copy, matching the lane header's citation).

R23-REATTACK SourceReopen: AGREE
