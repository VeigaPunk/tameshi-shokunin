# Admission bar (probation draft)

1. Every claim falsifiable or marked opinion.
2. Every claim carries a source: a measured anchor (path:line, command,
   evidence id) — never oral knowledge.
3. Observation, inference, and unknown stay separate.
4. Errata are append-only blocks.
5. A rejection is kept, not silently dropped.

## Criteria appended — fleet round 1 (kaika continuation, 2026-10-19)

Each criterion cites the mistake it learns from
(`lessons/round-1.md` `## Mistakes`). Criteria 1–5 are unchanged.

6. A pre-registered prediction carries its executed outcome in the same
   entry; a miss is an errata row naming the discriminator, never a
   silent drop. (MK-2, MK-3)
7. A knowledge file lands with its coverage-map row in the same round,
   or the missing row is named as debt in `LOG.md` with an owner.
   (MK-4)
8. A verification that ran lands its report in-repo in the round it
   ran; an executed-but-unreported verification is named debt, never
   cited as a pass. (MK-5)
9. Scratch stays in `/tmp`; evidence a claim rests on is copied into
   the repo (`.ufo/evidence/…`) before the commit that cites it.
   (MK-6)
10. A new `knowledge/` entry opens with `source:`, `verified-at:` and
    `recheck:`; an external source enters through a `SOURCES.md` row
    opened in the round that writes it (tiers: `SOURCES.md`, contract
    v1); a tier-C row is never sole support. (MK-7)
