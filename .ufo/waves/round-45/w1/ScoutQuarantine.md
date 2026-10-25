seat: ScoutQuarantine

# Round-45 w1 — quarantine slice re-derivation for lane `tameshi`

Scope (item): re-derive this lane's slice of the read-only absent-defect register, compare it with
the committed round-45 `quarantine-slice` and with the round-40 verdicts, and answer whether any
slice id is S202/S203 (this round's adopted documents).

Read-only package `/home/vgpnk/Projects/shokuknow` was only read — no campaign tool was executed
there, nothing was written, committed, fetched or pushed. No tools were installed or upgraded by
this seat (none needed: `awk`, `git`, `sha256sum`, `python3`, `grep` are all present; the pacman
guard was not touched). Scratch dir `/tmp/tameshi-r45-ScoutQuarantine/` holds only the derived
slice file. The lane checkout was not modified apart from this report file.

## 1. Recipe and count — 17 rows

```
awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Output — **17 rows**, every line carrying an S-id:

Exact output (17 lines):

```
 S105   `payload-absent`
 S109   `payload-absent`
 S110   `payload-absent`
 S118   `payload-absent`
 S119   `payload-absent`
 S124   `payload-absent`
 S126   `payload-absent`
 S129   `payload-absent`
 S131   `payload-absent`
 S132   `payload-absent`
 S137   `payload-absent`
 S140   `payload-absent`
 S141   `payload-absent`
 S143   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S123`   the cited source could not be fetched, so no quote was checked
 S134`   the cited source could not be fetched, so no quote was checked
```

Ids, sorted: **S105 S109 S110 S113 S118 S119 S123 S124 S126 S129 S131 S132 S134 S137 S140 S141
S143**. Register line numbers: **215–228** (the 14 `payload-absent` rows, section `## Rows`) and
**363–365** (the 3 never-checked rows, section `## Rows whose quotes were NEVER CHECKED`).

`grep -c '`tameshi`' absent-defect-register.md` → **18** = 17 data rows + 1 row of the By-lane
summary table (line 240). The awk recipe's `round[0-9]+` guard on field 3 is what excludes that
summary row.

Note the two distinct register shapes the recipe surfaces: the section-1 rows carry a **class**
in field 5 (`payload-absent`), while the section-2 rows carry the **prose reason** in field 5
("the cited source could not be fetched…") and a stray trailing backtick in the id field
(`S113\``), because the generator writes `| {id}\` |` for that table
(`absent-defect-register.py:169`). A reader must not read the trailing backtick as part of the id.

## 2. The committed round-45 slice is byte-identical to the re-derivation

```
sha256sum /tmp/tameshi-r45-ScoutQuarantine/derived-slice.txt
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/assimilation/quarantine-slice
cmp derived-slice.txt …/quarantine-slice
```

Both hash to **`cb8270615417d23454552f32edd0d3d57a0c4028b4a4180537d6c74fc7e796ad`**; `cmp` reports no
difference. The same hash is on `.ufo/waves/round-40/assimilation/quarantine-slice` and
`.ufo/waves/round-42/assimilation/quarantine-slice` — the slice has not moved in three rounds.

The register file itself has not moved either, and is clean in git:

```
sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
# 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833
git -C /home/vgpnk/Projects/shokuknow show d4ab45f281572ecb353dd3c9b71eee0e9213558b:.ufo/waves/corpus-expansion-1/absent-defect-register.md | sha256sum   # same hash
git -C /home/vgpnk/Projects/shokuknow status --porcelain -- .ufo/waves/corpus-expansion-1/absent-defect-register.md   # empty
git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %ad' -- .ufo/waves/corpus-expansion-1/absent-defect-register.md
# d4ab45f281572ecb353dd3c9b71eee0e9213558b  Sat Oct 24 08:37:10 2026 -0300
```

The slice is also present, and identical, at the freeze revision:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 3310e7be803516ca5934b4e949d91bcec824b179:.ufo/evidence/round-45/assimilation/quarantine-slice
# same 17 lines, sha256 cb8270615417d23454552f32edd0d3d57a0c4028b4a4180537d6c74fc7e796ad
```

**No drift, no missing row, no extra row.** The committed slice is correct.

## 3. Header / By-lane staleness, quantified

The item warned the header and By-lane summary are stale. Measured against the generator
(`absent-defect-register.py`) and the census (`quote-lint-full-v5.json`):

* Header `## Totals` (lines 16–24): "rows with at least one ABSENT quote: **194**", "ABSENT
  quotes: **324**", class table = `payload-absent` 194. The two numbers are **correct against the
  census** — v5 holds 324 `ABSENT` findings over exactly 194 distinct `(lane, round, id)` keys, and
  the register's section-1 row set equals that census key set in both directions (0 only-in-census,
  0 only-in-register). What is stale is the **shape**: the class legend (lines 11–15) defines two
  classes (`payload-absent`, `unreachable`) but the totals table carries only `payload-absent`, and
  section 2's rows are given no class label at all.
* The 324/194 headline also understates what the file shows: the generator emits at most **3** quote
  spans per row and truncates each at **120** characters
  (`absent-defect-register.py:142` — `qs = "<br>".join(f"`{q[:120]}`" for q in r["quotes"][:3])`).
  Measured: 21 of the 324 quotes are **not rendered at all** (17 rows hold >3) and 34 quotes are cut
  mid-span. A reader of the rendered table sees 290 whole `<br>`-separated spans, not 324.
* By-lane table (lines 234–256): sums to 194 and equals the **section-1** counts exactly for every
  lane (verified lane-by-lane). It therefore counts only the `payload-absent` rows. For `tameshi` it
  says **14** while the lane's real data-row count is **17** — the three never-checked rows are
  invisible in it. Two lanes (`lore` 9, `mori` 3) appear **only** in section 2 and are absent from
  the By-lane table altogether. A reader trusting By-lane under-counts this lane by 3 rows.

## 4. Family per id

**Family A — register class family** (the register's own class column / table):

| class family | ids | n |
|---|---|---|
| `payload-absent` — the register's "fabrication class": every relevant source fetched cleanly, the quote is in none of them | S105 S109 S110 S118 S119 S124 S126 S129 S131 S132 S137 S140 S141 S143 | 14 |
| prose fetch-failure class (never-checked section; no quote was ever checked, so no fabrication claim is possible) | S113 S123 S134 | 3 |

**Family B — cited-source family** (the register's cited-source cell):

| source family | ids | n |
|---|---|---|
| lane self-cite `https://github.com/VeigaPunk/tameshi-shokunin` | S124 S126 S131 S132 S137 S140 S141 S143 | 8 |
| DOI resolver `https://doi.org/…` | S109 S113 S123 S134 | 4 |
| other external URL | S105 S110 S118 S119 S129 | 5 |

**Family C — round-40 verdict family** (`corpus/lessons/round-40.md:55-71`, one verdict and one seat
per row, 17/17 of the slice ids covered):

| verdict family | ids | seat(s) |
|---|---|---|
| adopted (row appended) | S132 | `ScoutS132` |
| present / adopt-eligible, not appended | S105 S110 S113 S119 S123 S124 S126 S129 S134 | `ScoutQ105` `ScoutQ110` `ReviewQ113` `ScoutQ119` `ReviewQ123` `ReviewQ124` `ReviewQ126` `ReviewQ129` `ReviewQ134` |
| refused | S109 S131 S137 S140 S141 S143 | `ScoutQ109` `ReviewQ131` `ScribeGate`+`ReviewQ141` `ReviewQ140` `ReviewQ141` `ReviewQ143` |
| misbound (quoted span is a provenance note, not a claim) — not appended | S118 | `ScoutQ118` |

Counts: 1 adopted + 9 present-not-appended + 1 misbound + 6 refused = 17. The round-40 **class**
column is faithful to the register (14 `payload-absent` + 3 `could-not-be-fetched`). Every seat
report named in that table exists under `.ufo/waves/round-40/w1/` (17 files, all present).

Caveat carried forward from round 41: the round-40 lesson's *closing sentence* (`round-40.md:73`)
says "seven refused … nine present", while its own table counts one adopted / six refused / ten
present. The table is the record; the sentence is the drift, corrected by the appended correction in
`corpus/lessons/round-41.md:51-58`.

## 5. S202/S203 — answer: **no slice id is S202 or S203**

* The slice ids are S105 S109 S110 S113 S118 S119 S123 S124 S126 S129 S131 S132 S134 S137 S140 S141
  S143. Max is S143. **S202 and S203 do not appear.**
* The register's one `S202` row belongs to a **different lane**: `absent-defect-register.md:93` —
  `` `kama` | round1 | S202 | `payload-absent` | https://docs.docker.com/reference/compose-file/services/ ``.
  It is not a `tameshi` row and not in the slice. `S203` appears **nowhere** in the register
  (`grep -c 'S203'` → 0; the census has S203 findings for lanes `kake`, `kama`, `mado`, `tsukuroi`,
  all with non-ABSENT verdicts).
* The register ids are **per-lane corpus-expansion ids**, not the lane-registry or staged-package
  ids. This round's adopted documents are staged ids S202/S203 in
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:56-57` (googletest
  `docs/advanced.md` and `docs/primer.md` @ `cd8e73f0…`), which the guard-admitted map lands at
  **S256/S257** (`.ufo/evidence/round-45/assimilation/adoption-map.json`:
  `{"S202":"S256","S203":"S257"}`; guard receipt `guard-map.json`: `map_ok=true`, `map_floor=S256`,
  `safe_floor=S256`, `staged_max=S255`).
* **Quarantine status of the adopted documents: none exists.** GoogleTest never entered the
  corpus-expansion census: `grep -c googletest` on the register → **0** and on
  `quote-lint-full-v5.json` → **0**; `grep -c cd8e73f` on both → **0**. So there is no ABSENT
  verdict and no fabrication class against S256/S257 — they are un-quarantined **by construction**,
  not by exemption. Their snapshots are committed at
  `.ufo/evidence/round-45/coverage/sources/googletest-{advanced,primer,testing}.md`
  (sha256 `05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2`,
  `03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e`,
  `44c56c6198c6736bf2dc27c47391e4d481be70b36839e3c0073f273894d52d2b`).

## 6. Id-space divergence between the register and the round-40 verdicts (observation)

The register's `tameshi` ids and the round-40 verdict table's ids are **different id spaces that
share numbers**, and the register's own quoted span was re-tested in round 40 for only some ids.

Mapping, derived from source (register id → campaign pre-remap id = id+4 → `ID-REMAP.md` staged id),
with the campaign gate block that literally carries the register's quoted span:

| register id | round | pre-remap campaign id | staged id | campaign gate holding the register quote | register cited source = staged row source? |
|---|---|---|---|---|---|
| S105 | round1 | S109 | S153 | S153 | YES |
| S109 | round1 | S113 | S157 | S157 | YES |
| S110 | round1 | S114 | S158 | S158 | YES |
| S118 | round1 | S122 | S166 | S166 | YES |
| S119 | round2 | S123 | S167 | S167 | YES |
| S124 | round2 | S128 | S172 | S172 | lane self-cite |
| S126 | round2 | S130 | S174 | S174 | lane self-cite |
| S129 | round3 | S133 | S177 | S177 | YES |
| S131 | round3 | S135 | S179 | S179 | lane self-cite |
| S132 | round3 | S136 | S180 | S180 | lane self-cite |
| S137 | round4 | S141 | S185 | S185 | lane self-cite |
| S140 | round5 | S144 | S188 | S188 | lane self-cite |
| S141 | round5 | S145 | S189 | S189 | lane self-cite |
| S143 | round5 | S147 | S191 | S191 | lane self-cite |

(The +4 offset is the register-compile-time id; `lanes/tameshi/ID-REMAP.md` then renumbers to the
staged space, and states the hazard: "the same id in two rounds names two different rows, so a
round-blind substitution would move one round's citations onto another's rows while every
structural check stayed green".)

Consequence, measured by searching every round-40 seat report for the register's **own** quoted
span (full census quote, and the register's 120-char rendering):

| id | register span re-tested in a round-40 report? | which report |
|---|---|---|
| S105 | YES | `ScoutQ105.md` |
| S109 | YES | `ScoutQ109.md` |
| S110 | YES (rendered with a typographic apostrophe: `Google’s` vs the census `Google's`) | `ScoutQ110.md` |
| S118 | YES | `ScoutQ118.md` |
| S119 | YES (register cell truncated at 120 chars) | `ScoutQ119.md` |
| S124 | YES | `ReviewQ124.md` |
| S126 | YES | `ReviewQ126.md` |
| S129 | YES | `ReviewQ129.md` (+5 critic reports) |
| S140 | YES | `ReviewQ140.md` |
| S143 | YES | `ReviewQ143.md` |
| **S131** | **NO** | — |
| **S132** | **NO** | — |
| **S137** | **NO** | — |
| **S141** | **NO** | — |

The three never-checked rows have no quoted span to re-test (the register records a fetch failure,
not a span); their verdicts were rendered against the **URL cell** instead — `ReviewQ113.md:8,16-18`
(DOI 10.1145/3540250.3558911), `ReviewQ123.md:12,25` (DOI 10.1109/TSE.2026.3685588),
`ReviewQ134.md:9,25-30` (DOI 10.1145/351240.351266) — each of which also matches the staged row
reached by the +4→ID-REMAP mapping (S161, S171, S182), so those three are keyed correctly.

For **S131 / S132 / S137 / S141** the round-40 verdicts were rendered against *other documents*:

* register **S131** (lane self-cite, `bash-surface-census   kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)`) → campaign gate **S179** = "tameshi's fleet regression ledger and its recorded kill-rate expectation — tools/mutate-and-run.sh". The round-40 verdict for "S131" is GNU Diffutils "refuse as pinned" (`ReviewQ131.md:11`, row `merge/tameshi/SOURCES.append.md:29`).
* register **S132** (lane self-cite, `REGRESSION_DATE: 2026-10-23T22:25:58Z` / `REGRESSION_WORKDIR js-kimi-census: …`) → campaign gate **S180** = "tameshi's repeated-control instrument and its measured verdict on the fleet regression leg". The round-40 verdict for "S132" is the snapshot-README D29 title (`ScoutS132.md:5`, `corpus/lessons/round-40.md:66`).
* register **S137** (lane self-cite, `kimi-census.mjs writeFile=0 appendFile=0 createWriteStream=0 …`) → campaign gate **S185** = "tameshi's audited write-path census of the fleet gate selftests". The round-40 verdict for "S137" is the write-path census absence at `31687496` (`ScribeGate.md`).
* register **S141** (lane self-cite, `writeFileSync(abs, 'fixture\n');` / `else writeFileSync(join(root, …)`) → campaign gate **S189** = "tameshi's audited write-site census of the six fleet gate selftests". The round-40 verdict for "S141" is "commit `31687496` carries no 86-site census" (`ReviewQ141.md:3,17`).

Two of those verdicts nonetheless rest on the register's own row: `ReviewQ141.md:17` binds by the
row's *anchor* ("S141's corrected row …/round5/SOURCES-PROPOSED.md:21, staged id S141") and
`ScribeGate.md` binds its rejected entry to "round4/SOURCES-PROPOSED.md:22" — both are the +4
rows. So the verdicts are about the same **campaign rows** but were keyed by the *staged/registry*
number, while the register numbers those same rows 4 lower. `ReviewQ124.md:15-17` documents this
drift explicitly for S124 ("Row identified despite id drift: the only round2 `tameshi` row carrying
that quote/URL is the repeat-control instrument row — currently numbered **S128**") and notes the
`ID-REMAP.md` gap for round2.

The lane's own registry shows the same overlap from the other side: `corpus/SOURCES.md:117` **S105**
= the POSIX `diff` spec (the same document the register's S105 names), and `corpus/SOURCES.md:121`
**S132** = "Snapshot Testing document table" (`raw.githubusercontent.com/VictorGazzinelli/snapshot-testing/master/README.md`)
— a **different** document from the register's S132 row. The guard receipt records exactly this
coincidence where it holds: `guard-map.json` `map_dedupe` `{"S153":"S105","S154":"S106","S159":"S155","S160":"S156"}`
— staged rows whose document is already held are deduped onto the held id rather than given a new one.

**This is not a claim that any of the four rows is a fabrication.** It records that the register's
`payload-absent` verdict for those four was never re-tested against the exact spans it carries, and
that the round-40 verdict table's numbers for them name other documents. No row is called a
fabrication here, and the register was not edited.

## 7. Effect on the two declared claims: none

Neither counter reads the slice, so a slice defect could not move a number silently:

```
grep -niE "quarantine|absent-defect|shokuknow" .ufo/evidence/round-45/freshness/measure.py .ufo/evidence/round-45/coverage/measure.py
# only the word "absent" inside the freshness counter's own validation strings ("snapshot absent", "quote absent"); nothing in the coverage counter
```

For reference, the freshness counter at the freeze revision (read-only, permitted):

```
python3 .ufo/evidence/round-45/freshness/measure.py --lane …/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179
# C1_R45: self_pin=1 population=73 entries=0 verified=0 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=0 fresh=0 score=0 target=50 rev=3310e7b… C1_R45_PASS=false
```

(The 73-row population and `self_pin=1` are already in place at the freeze; only the ledger is
missing there.)

## 8. Commands run (all read-only)

```
# derivation
awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md   # → 17 lines
grep -c '`tameshi`' …/absent-defect-register.md    # → 18 (17 data rows + the By-lane summary row)
grep -n '| S202' …/absent-defect-register.md       # → line 93 only, lane kama
grep -c 'S203'  …/absent-defect-register.md        # → 0
grep -ci 'googletest' …/absent-defect-register.md  # → 0
grep -c 'cd8e73f' …/absent-defect-register.md /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint-full-v5.json   # → 0 / 0
# hashes / identity
sha256sum …/absent-defect-register.md ; git -C /home/vgpnk/Projects/shokuknow show d4ab45f2:… | sha256sum
git -C /home/vgpnk/Projects/shokuknow status --porcelain -- …/absent-defect-register.md
cmp /tmp/tameshi-r45-ScoutQuarantine/derived-slice.txt …/.ufo/evidence/round-45/assimilation/quarantine-slice
# lane side
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 3310e7b…:.ufo/evidence/round-45/assimilation/quarantine-slice
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 3310e7b…:corpus/SOURCES.md | grep -cE '^\s*\|\s*S[0-9]+\s*\|'   # → 115
# census cross-check
python3 -c "…" quote-lint-full-v5.json   # 324 ABSENT findings over 194 distinct keys; tameshi = 14 keys / 16 quotes
# package side
grep -nE '^\| S(202|203) \|' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md
cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/assimilation/{adoption-map.json,guard-map.json}
```

Nothing in `/home/vgpnk/Projects/shokuknow` was written, committed, fetched or pushed; no campaign
tool was executed there; the lane checkout was not modified apart from this report file; no lane
git/jj state was touched.

## 9. Findings summary

1. Slice = **17 rows**: S105 S109 S110 S113 S118 S119 S123 S124 S126 S129 S131 S132 S134 S137 S140
   S141 S143 (register lines 215–228 and 363–365).
2. The committed round-45 `quarantine-slice` is **byte-identical** to a fresh re-derivation
   (`cb8270615417d23454552f32edd0d3d57a0c4028b4a4180537d6c74fc7e796ad`), and identical to the
   round-40 and round-42 slices; the register file is unchanged since 2026-10-24 08:37 and is clean
   in git. **No drift.**
3. Family per id: register class family **14 `payload-absent` + 3 never-checked**; cited-source
   family **8 lane self-cite, 4 DOI, 5 other external**; round-40 verdict family **1 adopted
   (S132), 9 present-not-appended, 1 misbound (S118), 6 refused**.
4. Staleness confirmed and quantified: the By-lane table counts only the `payload-absent` rows, so
   it says **14** for this lane against **17** actual data rows, and it omits the two lanes that
   appear only in the never-checked section (`lore`, `mori`). The totals headline (194 rows / 324
   quotes) is right against the census, but the rendered table shows only 290 whole spans (the
   generator caps 3 quotes/row and 120 chars/quote, hiding 21 quotes and cutting 34 mid-span).
5. **No slice id is S202 or S203.** The register's sole S202 is a `kama` row; S203 does not occur in
   the register at all. The adopted documents (staged S202/S203 → lane S256/S257) carry **no
   quarantine status**: GoogleTest never entered the corpus-expansion census (0 hits for
   `googletest` and 0 for commit `cd8e73f0…` in both the register and the census), so there is no
   ABSENT verdict and no fabrication class against them.
6. Observation for the L1: the register's per-lane ids and the round-40 verdict table's ids are
   distinct id spaces sharing numbers (register id + 4 = the campaign id the round-40 seats used;
   `ID-REMAP.md` then maps that to the staged space). For **S131, S132, S137, S141** the register's
   own quoted span was not re-tested in round 40 (no seat report contains it), and the round-40
   verdict numbers for those ids name other documents. This does not touch C1/C2 (neither counter
   reads the slice) and no row is called a fabrication.
