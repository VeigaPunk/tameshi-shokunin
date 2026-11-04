# QUALITY.md criterion draft — round 75 (criterion 125)

Append target: `corpus/QUALITY.md`, directly after criterion 124 (the current
last block; criteria 115–124 sit under the last `## Criteria appended` heading,
so the L1 decides whether a `## Criteria appended — round 75 (2026-11-03)`
heading is added — the block below is the row itself).

### Criterion 125 — a live capability figure is the instrument's current token or is labelled historical and pinned to the receipt that carries it

A capability table's printed figure is a measurement of the instrument, not a
quotation of the record. A live row therefore carries either the instrument's
**current** token — re-derived at the revision the table is read at, from the
instrument's own stdout — or it is explicitly labelled historical and pinned to
the receipt that carries it. A figure no instrument prints is a **stale
premise**, not a conservative estimate: it asserts a capability at a strength
nothing measures, and a reader who trusts it cannot tell a regression from a
forgotten edit. The two states are distinguishable only by re-running the
instrument, so a capability table is never "updated by hand"; it is re-derived
or demoted.

Lesson: `corpus/lessons/round-75.md` `## Claims — R75-C2` and `## Mistakes` row
1 (class `number-drift`/`stale-premise`), produced by round-74 closure defect 3
(`corpus/lessons/round-74-verifier-spotcheck.md` §6 item 3) and measured over the
whole population by `.ufo/evidence/round-75/base-measure-c2.txt` (seven of
sixteen live figures stale, `SELFSTATE_CONTROL: rows=16 match=9 stale=7`, exit
1). The instrument the criterion installs is `tools/selfstate-freshness.py` +
`tools/selfstate-freshness.json`: 16 live capability rows plus one frozen
historical statement, each figure regex searched in the pinned instrument's own
stdout extracted from git objects at its rev; an absent capability row or absent
figure is a setup refusal (exit 2), never a pass.

Falsifier that must fail: at `21ef81e9` the live `anchor-drift sweep` row quotes
`ANCHOR_DRIFT: rows=4 met=4 unexpected=0` while the lane instrument at its pinned
rev prints `ANCHOR_DRIFT: rows=16 met=16 unexpected=0` — the row reads
`SELFSTATE_ROW anchor-drift sweep … stale` in
`.ufo/evidence/round-75/base-measure-c2.txt`, and the same sweep closes on
`SELFSTATE_CONTROL: rows=16 match=9 stale=7` exit 1. The criterion holds when
`python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest
tools/selfstate-freshness.json --doc-rev <tip>` prints `SELFSTATE: rows=17
match=16 stale=1 unexpected=0` exit 0, with every live row reading `match` and
the one frozen row (`r74-frozen-addr-six`, `expect: stale`) measuring `stale` on
every sweep — `<L1 fills: tip rev and receipt path>`.
