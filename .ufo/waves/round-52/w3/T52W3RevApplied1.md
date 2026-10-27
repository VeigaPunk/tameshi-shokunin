# Applied-fix falsifier — Fix01–Fix05

Scope: CAND1 `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`; comparison uses applied log plus each W2 draft. Findings classify replacement truth and scope; dates remain historical where explicitly dated.

## Fix01 — SKILL.md:1826 — TRUE, no overreach
- Replacement qualifies the formerly absolute branch-tip claim with current detached-root behavior. The CAND1 row names the branch/attached-tip case and detached-root raw-HEAD case, and gives implementation/selftest pointers.
- Evidence command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '1823,1828p'`; implementation: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/evidence-disposition.py | nl -ba | sed -n '460,525p'`.

## Fix02 — SKILL.md:224 — TRUE, no overreach
- The heading now says endpoint identity, matching its own immediately following limitation that endpoint checks do not prove absence of transient writes. It changes only the stale overclaim in the heading; preserves the historical round-27 correction pointer.
- Evidence command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '224,229p;375,378p'`.

## Fix03 — SKILL.md:925, 929 — TRUE, no overreach
- Line 925 preserves the four-leg count at the explicitly named r7-1 revision and dates later additions (7/8/9/10) instead of rewriting the historical count. Line 929 qualifies the round-18 table pointer by runner revision; the historical round-18 location remains intact.
- Evidence command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '921,931p'`; current runner anchors: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/mutate-and-run.sh | nl -ba | sed -n '84,108p;614,643p;1459,1517p'`.
- Pass-2 applied additions in this range: Fix03:8 distinguishes enumerated from executed counts and explicitly notes no skipped counts in current records; Fix03:10 updates current anchor :603-629 to :614-643. Both are accurate, scope-limited qualifiers/anchors.
- REFUSE/LEAVE2 residue in this range: Fix03:9 leaves “Current anchors (round 26)” standing at CAND1 line 960, although the same line also states “round 52 re-anchor”; the latter explicitly scopes the updated anchors, so not stale as a whole. Fix03:11 leaves `first-four specs :657-839`; at CAND1 the first-four specs are :671-849, so this is a stale pointer. Fix03:12 leaves “nine dispatches :1384-1428”; CAND1 has ten dispatches :1459-1508, stale count and pointer. Fix03:13 leaves N=8/N=9 count at SKILL.md:976; this is explicitly historical T7-1 under same tool sha, so dated and not stale. Fix03:14 and :15 refer to the historical same-sha replay and negative run, not current runner behavior. Fix03:16's “including a git-materialized replay” is historical measurement and not a present-tense current claim.
- Evidence command for residues: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '957,979p'`; runner: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/mutate-and-run.sh | nl -ba | sed -n '671,849p;1459,1508p'`.

## Fix04 — SKILL.md:1305 — OVERREACH / false as applied
- Pass-2 applied text is `replays six in r10-2 (ten since round 51)`; the earlier pass-1 form had the same qualifier and the later application retained it. This is malformed and contradictory: CAND1 line 1305 already includes “six … in r10-2 (ten since round 51)” and then another “(ten since round 51)”. The parenthetical repeats rather than clarifies. It should retain exactly one qualification. The underlying dated distinction (six at r10-2, ten at round 52) is accurate; the duplicate is overreach/editorial error.
- Evidence command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '1302,1309p'`; runner count: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/mutate-and-run.sh | nl -ba | sed -n '84,97p;1459,1510p'`.
- REFUSE/LEAVE2 residue: Fix04:2 leaves the literal `/tmp` scratch command in the historical round-4-2 receipt at CAND1 line 1321. It is explicitly qualified as default command in this usage section and conflicts with the CAND1 runner's `${TMPDIR:-/tmp}` behavior. Fix04 draft explicitly documented it as stale; this is a missed stale statement. Fix04:3 leaves “read at 75ed934d, the sha governs” at line 1308; it describes the historical tool revision, so not stale.
- Evidence command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '1304,1324p'`; runner: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/mutate-and-run.sh | nl -ba | sed -n '139,150p;1432p'`.

## Fix05 — SKILL.md:1064,1084 — TRUE, with a scope caveat
- Line 1064 preserves 67/67 as round-8 history and adds the CAND1 run's 107/107 value. This is correctly dated and does not rewrite the old observation.
- Line 1084 replaces impossible `:811-812` with existing ER-3/ER-4 lines in the same ledger, and retains the re-pin proposition.
- Evidence commands: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '1062,1067p;1082,1086p'`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | nl -ba | sed -n '310,320p'`.
- Pass-2 addition at line 1084 (“three labels are not exhaustive …”) correctly describes an unclassified state in the rule table, but broadens the original citation fix into a new current rule explanation. It is supported by line 1029 and ER-jj at ledger :420; no false claim found. Fix05:3's omitted `mutation-case-kumitate-claims.md:285-291` citation remains at line 1144, but it is a historically scoped source citation that still holds the D8 claim; the added citation :142-148 supplies the missing D7 evidence, so no stale statement remains.
- Evidence command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | nl -ba | sed -n '1027,1036p;1141,1145p'`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | nl -ba | sed -n '416,422p'`.

## Summary
- Fix01–Fix03 applied changes are true and preserve dated history; Fix03 leaves stale spec/dispatch anchors at line 961.
- Fix04's applied line 1305 duplicates its ten-since-round-51 qualifier (overreach); its refused literal `/tmp` pointer at 1321 remains stale.
- Fix05's dated count and citation repair are true; historical counts remain scoped to their original runs.
