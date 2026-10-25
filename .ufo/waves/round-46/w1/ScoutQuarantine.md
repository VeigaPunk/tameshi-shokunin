seat: ScoutQuarantine
item: Re-derived the tameshi quarantine slice from the read-only absent-defect register (corpus-expansion-1) and compared it with the committed round-46 slice and the round-40/45 lesson verdicts; checked adopted-document overlap and fresh-fetch resolution.

## Re-derivation (the item's awk recipe)

Command: `awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`

- Count: **17 data rows** (9 external-doc rows, 8 own-work-repo rows).
- sha256 of derived output = `cb8270615417d23454552f32edd0d3d57a0c4028b4a4180537d6c74fc7e796ad`; `cmp` clean against **all three** committed slices: round-46 `.ufo/evidence/round-46/assimilation/quarantine-slice`, round-45 `.ufo/evidence/round-45/assimilation/quarantine-slice`, round-40 `.ufo/waves/round-40/assimilation/quarantine-slice`. Byte-identical across rounds 40/45/46.
- Register header/By-lane summary is stale as stated: the "## By lane" table says tameshi 14 (it counts only the ABSENT-table rows; the 3 never-checked rows live in the separate "## Rows whose quotes were NEVER CHECKED" section, which the By-lane counter excludes). The data rows give 17.

## Ids and family per id

| id | register round | class family | document family | merge/id-space counterpart (+48) | round-40 verdict | round-45/46 status |
|---|---|---|---|---|---|---|
| S105 | round1 | payload-absent | external-doc (POSIX diff spec) | S153 (POSIX diff spec; guard map_dedupe S153→held S105) | present — whitespace-fold false positive; adopt-eligible, not appended | unchanged, no new verdict |
| S109 | round1 | payload-absent | external-doc (JOSS Hypothesis DOI) | S157 | absent — refused | unchanged |
| S110 | round1 | payload-absent | external-doc (Lam et al. flaky-rerun PDF) | S158 | present verbatim; adopt-eligible, not appended | unchanged |
| S113 | round1 | could-not-be-fetched | external-doc (DOI 10.1145/3540250.3558911) | S161 | present (DOI resolves, camera-ready PDF HTTP 200); adopt-eligible, not appended | unchanged |
| S118 | round1 | payload-absent | external-doc (Zenn mutation article) | S166 | misbound — quoted span is a provenance note; not appended | unchanged |
| S119 | round2 | payload-absent | external-doc (purdue delta-debugging PDF) | S167 | present verbatim (locator off by one); adopt-eligible, not appended | unchanged |
| S123 | round2 | could-not-be-fetched | external-doc (DOI 10.1109/TSE.2026.3685588, OpenStack Cross-Project Flakiness) | S171 | present (202 at DOI; figures verbatim in arXiv carrier arXiv:2602.09311 = merge S237); adopt-eligible, not appended | unchanged |
| S124 | round2 | payload-absent | own-work-repo | S172 | present; adopt-eligible, not appended | unchanged |
| S126 | round2 | payload-absent | own-work-repo | S174 | present; adopt-eligible, not appended | unchanged |
| S129 | round3 | payload-absent | external-doc (Kyoto IEICE index page) | S177 (and S192 duplicate page) | present — flagged token is a code token; two real gate quotes verify; adopt-eligible, not appended | unchanged |
| S131 | round3 | payload-absent | own-work-repo | S179 | refuse as pinned (unreachable, not fabricated; content covered by S105); not appended | unchanged |
| S132 | round3 | payload-absent | own-work-repo | S180 | present — **adopted round 40** into lane registry as S132 (Snapshot Testing table) | unchanged; lane-registry row S132 exists (used-by r3-snapshot-fixture-update-paths.md) |
| S134 | round4 | could-not-be-fetched | external-doc (DOI 10.1145/351240.351266) | S182 | present (DOI via aaron channel); adopt-eligible, not appended | unchanged |
| S137 | round4 | payload-absent | own-work-repo | S185 | absent — flip unmet; refused | unchanged |
| S140 | round5 | payload-absent | own-work-repo | S188 | absent — refused | unchanged |
| S141 | round5 | payload-absent | own-work-repo | S189 | absent — refused | unchanged |
| S143 | round5 | payload-absent | own-work-repo | S191 | absent — source live but quote absent; refused | unchanged |

Class families: 14 `payload-absent` + 3 `could-not-be-fetched`. Document families: 9 external documents (spec/DOI/papers/index) + 8 own-work repo rows (`github.com/VeigaPunk/tameshi-shokunin`), i.e. quotes from the lane's own outputs.

Id-format quirk (fidelity note): the three never-checked rows render in the register's second table as `S113``/`S123``/`S134`` (stray trailing backtick in the id cell), so the derived/committed slice lines carry `S113`` etc.; an exact-match `grep -x 'S113'` against the slice file fails. The mapping above strips the backtick.

## Comparison with lesson verdicts

- Round-40 lesson table covers exactly these 17 ids with one verdict each (as tabulated above); one adopted (S132), six refused (S109, S131, S137, S140, S141, S143), ten present-but-not-appended (S105, S110, S113, S118, S119, S123, S124, S126, S129, S134).
- Round-45 lesson ("Quarantine slice" section) states: "17 rows, unchanged, no new verdicts: 14 payload-absent … and 3 could-not-be-fetched (S113 S123 S134). The re-derivation is byte-identical to the committed slice (sha256 cb827061…, cmp clean) and to the round-40 list. … Verdicts stay those recorded in the round-40 lesson." All reproduced exactly (sha256 and cmp above).
- Round-46: no new verdicts are introduced by this seat (derive-only; no slice row is appended this round — none of the 17 ids exists in the lane registry corpus/SOURCES.md; registry has 117 rows with max S257; S258/S259/S260 absent at base).

## Adopted staged documents check (S190/S195/S216 and duplicates S225/S229/S235)

Question: is any slice id among the three adopted staged documents or their duplicates?

- Literal id comparison (register space): the slice ids are S105…S143; none equals S190/S195/S216/S225/S229/S235.
- Mapped comparison (merge-id space, register id + 48, verified per-row by URL/fragment and via campaign ID-REMAP register→campaign(+4)→merge): slice counterparts are S153, S157, S158, S161, S166, S167, S171, S172, S174, S177, S179, S180, S182, S185, S188, S189, S191 — none equals S190/S195/S216/S225/S229/S235.
- Document identity: the adopted documents' register-space rows are (a) round5 S142 ↔ merge S190 = TUM portal record of the TSE 2026 Leinen et al. paper — the census verdict for S142 was **sweep-found** (the quote was located), so it is NOT in the register (not ABSENT) and hence not in the slice; (b) merge S195 (arXiv 2504.16777) → register id S147 has no census finding at all; (c) merge S216/S225/S229/S235 (Google Testing Blog per-post feed) → register id S168 has no census finding at all. So **no slice id is among the adopted staged documents or their duplicates**, and none of the three adopted documents appears in the quarantine slice.
- Nearest call: slice S123's document (OpenStack Cross-Project Flakiness, DOI 10.1109/TSE.2026.3685588) shares journal/year with adopted S190 (Leinen et al., DOI 10.1109/TSE.2026.3729363) but is a different paper (different DOI); round-40 already established S123 present via arXiv:2602.09311.

## Does the lane's fresh fetch resolve any slice row?

- Fresh fetch snapshots (`.ufo/evidence/round-46/coverage/sources/`): `arxiv-2504.16777-abs.html` (sha256 28d2954d…), `tum-portal-flaky-failures.html` (sha256 5eb59adf…; contains DOI 3729363 14× and "Leinen" 9×), `google-flaky-feed-6277555988217606236.json` (sha256 434d8658…; contains feed id 4×). These are exactly the carriers of the three adopted documents (S258/S259/S260).
- None of the 17 slice rows cites any of these three documents (checked by cited-source URL against the snapshots).
- Quote-scan of all slice quoted spans against the three snapshots: only one hit — S129's single-token quote `canonical` appears in the arxiv abs snapshot, but only inside HTML chrome `<link rel="canonical" …/>`; that is a false positive, not the Kyoto IEICE content, so it does NOT resolve S129 (round-40 verdict already established S129's real gate quotes verify).
- **Fresh fetch resolves none of the 17 slice rows.** The adopted S190's register-space row (round5 S142) was resolved by the census itself (sweep-found) before this round; the fresh TUM portal snapshot independently re-confirms that document's presence, but S142 is not in the slice.

## Tools / installs

No tools installed or updated (read-only derivation; grep/awk/python3 only). No pacman.

## Handoff to main agent

No build/test/lint needed (report-only seat). Suggested spot-checks if desired: `cmp` of derived vs committed slice (sha256 cb8270615417d23454552f32edd0d3d57a0c4028b4a4180537d6c74fc7e796ad); the census verdict for round5 S142 = sweep-found (quote located) as the reason the S190 document is absent from the slice.
