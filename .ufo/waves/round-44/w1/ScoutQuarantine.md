# Quarantine slice re-derivation

- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`; relevant data rows are lines 214–230 (row IDs verified by the required awk command).
- Command: `awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
- Output: 17 rows total. Payload-absent (14): S105, S109, S110, S118, S119, S124, S126, S129, S131, S132, S137, S140, S141, S143. Could-not-be-fetched (3): S113, S123, S134. The three unavailable-class IDs print with a trailing backtick (`S113\``, `S123\``, `S134\``) because that malformed punctuation is present in the register's ID cells.
- Round-40 lesson slice: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-40/assimilation/quarantine-slice:1-17` has the same 17 ordered rows and same classes, including those trailing-backtick ID spellings. Byte-identity: yes (17 of 17). This comparison concerns the slice list, not verdicts; round-40 verdicts remain in that lesson, with no adoption here.
