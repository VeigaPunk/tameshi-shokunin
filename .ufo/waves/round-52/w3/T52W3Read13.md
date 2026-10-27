# T52W3Read13 — CAND1 cold read

## Findings
- F1: “The cadence applies this table at intake” is unsupported at CAND1: `service-limits.md:4-5` records the note's stated role, but the cited cadence passages describe pin reads/re-sweep triggers and do not establish that this refusal table is applied at intake. Section evidence: `SKILL.md:1248`; command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '1246,1271p'`. Cross-check commands: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '1010,1154p'` and `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | nl -ba | sed -n '285p;318p'`.

## Holds
18 pointer groups checked at CAND1; all resolve and support the cited statements, except that the note's role statement is not operational evidence for F1.

1. `corpus/knowledge/service-limits.md:4-5` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-limits.md` (the note self-describes the role).
2. `SKILL.md:1010-1154` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '1010,1154p'` (cadence/pin-read description).
3. `corpus/knowledge/fleet-kill-rate-ledger.md:285` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | nl -ba | sed -n '285p'`.
4. `corpus/knowledge/fleet-kill-rate-ledger.md:318` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | nl -ba | sed -n '318p'`.
5. `corpus/knowledge/service-limits.md` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-limits.md` (table rows/detail and intake-precondition section).
6. `corpus/knowledge/service-optin-protocol.md:25-30` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-optin-protocol.md | sed -n '25,30p'`.
7. `corpus/knowledge/fleet-suite-census.md:277-286` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-suite-census.md | sed -n '277,286p'`.
8. `SKILL.md:813-817` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '813,817p'`.
9. `SKILL.md:840-844` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '840,844p'`.
10. `SKILL.md:823-825` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '823,825p'`.
11. `corpus/knowledge/service-optin-protocol.md:129-132` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-optin-protocol.md | sed -n '129,132p'`.
12. Repo-root `PROVINCE.md:14-18,20` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:PROVINCE.md | sed -n '14,20p'`.
13. `SKILL.md:879-881` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '879,881p'`.
14. `corpus/knowledge/fleet-kill-rate-ledger.md:156-158` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '156,158p'`.
15. `corpus/knowledge/fleet-kill-rate-ledger.md:220` (U2) — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '220p'`.
16. `corpus/knowledge/service-optin-protocol.md:267-269` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-optin-protocol.md | sed -n '267,269p'`.
17. `corpus/knowledge/fleet-kill-rate-ledger.md:35-36` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '35,36p'`.
18. `corpus/knowledge/service-optin-protocol.md:86-91` — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-optin-protocol.md | sed -n '86,91p'`.

The section is lines 1246–1271 inclusive (next level-1–3 heading at 1272). Its SHA-256 over those lines joined by `\n` with no trailing newline is `bbbaf35248fb042984a09e6cfc8e79efd7599f6246de91fc9187e28bbf8bd227`.

## Summary
- One unsupported-premise finding: cadence intake application is asserted by the note, not established by cited cadence/ledger text.
- 18 pointer groups checked at CAND1; all resolve.
- Findings are not a claim verdict.
