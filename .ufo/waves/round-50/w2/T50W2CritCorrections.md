# Corrections review — T50W2CritCorrections

Seat: T50W2CritCorrections. Content revision read: `80ea77e99e239982ab0b93e416645ef2359725d3`
(`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:<path>`).
Source of truth per item: `corpus/lessons/round-50.md` `## Corrections to earlier records` and the appended block at the
end of `corpus/lessons/round-46.md`. Every claim below was checked against the tree at the revision, never the working tree.

## R40.2 — settlement receipt, sha256, counts — **true**

Command:
```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:.ufo/waves/round-40/settlement-receipt.json | sha256sum
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:.ufo/waves/round-40/settlement-receipt.json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d["seats"]), d["registry_members"], d["seat_exits"], d["reports_present"])'
```
Observed: sha256 `659e39bb7fba6d381ee3af27daec8b74a6542d861b8b4666b4d46d4ad44f89a3` (matches the lesson), `seats` array
length 64, `registry_members=64`, `seat_exits=64`, `reports_present=64`. The lesson's receipt citation is exact.

## R40.3 — pasted id lists vs `.ufo/waves/round-40/assimilation/{reg-ids,staged-ids}` — **true**

Commands:
```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:.ufo/waves/round-40/assimilation/reg-ids | sha256sum    # b11c94133a35ce8c2c13bb30c04dc545290e53c40710cfd09c4b0a3d94126e91
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:.ufo/waves/round-40/assimilation/staged-ids | sha256sum   # d77a652a2dbc36459dc74a10e8daa7f2e47cc713db0d02fc10d7f48dbb129fce
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:corpus/lessons/round-50.md | python3 -c '...extract pasted id runs...'
```
Observed: `reg-ids` = 105 ids (5 unique), sha256 matches the lesson's `b11c9413…`; `staged-ids` = 2 ids (S132 S152),
sha256 matches `d77a652a…`. The id runs pasted in the lesson (105 ids, then S132 S152) are identical to the file contents
as sequences — verified by diffing the extracted run against the file's ids joined with single spaces (exact match; the only
difference is the line separator, newline in the file vs space in the prose paste, which is inherent to embedding the list in
a paragraph). Counts and hashes are as stated.

## R40.4 — S152 quote token count — **true**

Commands:
```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:corpus/lessons/round-40.md | awk 'NR==14'
python3 -c 'q="drawbacks such as fragility and lack of context can lead to false positives"; print(len(q.split()))'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:corpus/knowledge/r6-snapshot-practice-corpus.md | sed -n '10p'
```
Observed: `corpus/lessons/round-40.md:14` reads `- Quote (11 words), English abstract: "drawbacks such as fragility and
lack of context can lead to false positives".` The quote is 13 whitespace tokens and 13 letter/digit words, not 11. The
same slip stands at `corpus/knowledge/r6-snapshot-practice-corpus.md:10` (`The quote is 11 words: "drawbacks such as
fragility and lack of context can lead to false positives".`). Both citations in the correction are accurate.

## R46.4 — appended block at end of `corpus/lessons/round-46.md` — **true**

Commands:
```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:corpus/lessons/round-46.md | sed -n '42p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | python3 -c 'import sys; s=sys.stdin.read(); print(s.count("9.8 %\u201316.3 %"), s.count("9.8 %-16.3 %"))'
```
Observed: line 42 of `round-46.md` prints the tail of the S259 quote as `for 9.8 %-16.3 % of failed pipeline runs."` —
ASCII hyphen, no U+2013 on the line. The pinned snapshot `tum-portal-flaky-failures.html` holds the en-dash phrase
`9.8 %–16.3 %` (U+2013) exactly 3 times and the ASCII-hyphen phrase 0 times. The block's fold description (U+2013 → `-`,
lane's quote fold, not a misquote) and the en-dash counts are exact; the quote text at line 42 matches the block's reading.
The round-47 checker it cites exists (`.ufo/evidence/round-47/quality/lesson-quote-check.py`) and reads lesson lines
generically (it parses `### `/bullet blocks), consistent with "still reads line 42 as written".

## R41.7 (declined) — decline reason vs the registry note block — **true**

The decline reason is the round-41 note block in `corpus/SOURCES.md`. Located at round 41 (commit `b37ce97`, the round-41
lesson commit that introduced the note) and now (at `80ea77e9`):

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show b37ce97:corpus/SOURCES.md | awk 'NR>=435 && NR<=440'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 80ea77e9:corpus/SOURCES.md | awk 'NR>=463 && NR<=468'
```
Observed (round-41 numbering): line 435 `- Next unused id: S105.`, line 436 blank, line 437 `Round 41: two rows added, …`,
lines 438-440 bullets (`- Id collision check …`, `- Census: …`, `- Next unused id: S155.`). Now: the same block at lines
463-468 (bullet, blank, paragraph, three bullets). The blank line at 436 (now 464) plus the paragraph does split the bullet
chain: cmark renders the span as **two separate `<ul>` lists** (the S105 bullet alone; the collision/census/next-unused-id
bullets together) with the paragraph between — `cmark` on `sed -n '435,440p'` of the round-41 file yields 2 `<ul>` elements.
No parse impact: the registry table's last row is at line 146, so the note span (prose below the table) contains zero `| S… |`
rows the lane's parsers read. The reason is accurate, and the decline (reflowing would edit a closed registry note for no
gain) is consistent with the found state.

## Conclusion

All five corrections checked — R40.2, R40.3, R40.4, R46.4, R41.7 — are **true** at `80ea77e9`; nothing is false or
incomplete. Commands that show each finding are named per item above.

## Summary

- R40.2: receipt sha256 `659e39bb…` matches; seats array 64; registry_members/seat_exits/reports_present all 64. true.
- R40.3: reg-ids 105 ids (sha256 `b11c9413…`) and staged-ids S132 S152 (sha256 `d77a652a…`) match the source files; pasted sequences identical (only separator/linebreak inherent to prose). true.
- R40.4: quote is 13 whitespace tokens / 13 letter-digit words; round-40.md:14 and r6-snapshot-practice-corpus.md:10 both say "11 words". true.
- R46.4: line 42 has ASCII hyphen; snapshot holds en-dash phrase 3×, hyphen phrase 0×; fold description exact. true.
- R41.7: round-41 note block at b37ce97:436-440 (now 464-468); blank line splits bullet chain into two lists (cmark: 2 `<ul>`); notes lie below the table (last row 146), no parse impact. true.
- No correction found false or incomplete at the content revision.
