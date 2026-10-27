# T52W3Read05 — cold-read re-key reader

Section: `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` at CAND1 `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`, SKILL.md lines 1010–1020 (the next heading of level 1–3 is `### The tick and the pin read` at line 1021, so the section is exactly 1010–1020, last line blank).

Section sha256 (lines joined by `\n`, i.e. the exact byte range): `4a01d2336c2679c31d82432dffc146c1312476bbdcf5f3dff3bd8f969d1fb75e`. Receipt copied to `.ufo/waves/round-52/w3/T52W3Read05-section.txt`.

Method: fresh cold read of the CAND1 bytes only; every pointer opened with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:<path>`; the one dating claim checked with read-only `git log -S`. No earlier reader files or fix drafts consulted. No tools installed.

## Findings

None. No statement of this section fails at CAND1.

## Holds

Checked and holding, 10 items:

- H1 — quote + pointer + label: `"this ledger's update cadence is a convention, not a mechanism"` is present verbatim at `corpus/knowledge/fleet-kill-rate-ledger.md:235-237`, which is exactly the three-line `**U9**` bullet. Show: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '235,237p'`.
- H2 — "Round 7 left its own gap open in writing": accurately dated; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%h %ad %s' --date=short -S "update cadence is a convention" -- corpus/knowledge/fleet-kill-rate-ledger.md` returns a single commit `9f1d3c3 2026-10-14 probation round 7 (training r6)`.
- H3 — "Round 8 closes it by measurement: **the cadence is a pin read executed at the tick**": the round-8 subsections below define and execute it — tick is the round boundary (SKILL.md:1023) and the executed pin read is pasted at SKILL.md:1038–1053.
- H4 — "three readings per case": holds under the document's own frame — per case the pin read answers the three labels `current`/`stale`/`drift`, and the round-52 bracket at SKILL.md:1029 counts them as per-case read outcomes ("all three read no"). Noted tension, not a finding: the definitional bullet says "Per case, two readings" (SKILL.md:1027), grouping the three labels into one reading; since the section's "three" maps onto the doc's own three-label count, I do not record a mismatch.
- H5 — "three triggers": T1, T2, T3 at SKILL.md:1069–1082 (heading `### Triggers T1–T3 and the re-pin rule`).
- H6 — "one re-pin rule": exactly one, the paragraph "The re-pin rule." at SKILL.md:1083–1086.
- H7 — "the same tick read is the ground the six-case confidence statement below stands on": `### Six-case confidence statement (round 8, measured)` exists below at SKILL.md:1092 with six cases tabled at 1097–1104, and the executed tick read (1042–1050) covers those cases' pins.
- H8 — "No daemon, no timer": consistent at CAND1 — SKILL.md:1160–1162 repeats it for the round-9 execution; the mechanism is an executed command at the boundary, no daemon/timer.
- H9 — `"standing" is the ledger + the policy + an executed command at the round boundary`: matches the mechanism as defined in the subsections (ledger pins, trigger policy, executed pin read).
- H10 — "whether any fleet driver would ever invoke the command with no lane acting stays [U]": still marked [U] at SKILL.md:1162, whose self-pointer `:1019` resolves to exactly this section's line 1019.

holds_checked: 10.

## Summary

- Section read: SKILL.md 1010–1020 at CAND1 (terminates at `###` line 1021); sha256 `4a01d2336c2679c31d82432dffc146c1312476bbdcf5f3dff3bd8f969d1fb75e`.
- Findings: 0 — every statement holds at CAND1; no stale pointer, count, or premise.
- U9 quote/pointer verified byte-exact at `fleet-kill-rate-ledger.md:235-237`; round-7 dating confirmed by pickaxe (`9f1d3c3`, 2026-10-14).
- Three triggers, one re-pin rule, six-case statement below, no-daemon/no-timer, and the standing-[U] claim (self-pointer `:1019`) all verified.
- "Three readings per case" holds via the doc's three-label frame (SKILL.md:1029); the "two readings" wording at :1027 is a definitional grouping, recorded as tension, not a finding.
