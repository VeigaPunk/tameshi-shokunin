# ReplayCensus — round 42 wave 2 (FALSIFY)

Seat `L1Tameshi42.ReplayCensus`. Attacked: the wave-1 census and id-collision records: `corpus/lessons/round-42.md:67-81`, `corpus/SOURCES.md:446-448`, `LOG.md:2198-2202`, `SCORECARD.md:2020`, and `.ufo/waves/round-42/assimilation/{collisions,guard/*}`. Run on 2026-10-25 against the lane worktree. The worktree's `corpus/SOURCES.md` is byte-identical to the integration tip `a21845f5` (`cmp` OK). This seat ran no C1/C2 counter. The scratch dir was `/tmp/tameshi-r42w2-ReplayCensus-coll` and has been deleted. No tools were installed.

## Findings

### F1 — Live census matches the round-start receipt. SURVIVES.
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
→ exit=0; 9 × W04 (S047 S048 S075 S076 S077 S078 S081 S092 S104), 1 × W01 (S101), 1 × ok
cmp <that stdout> .ufo/evidence/round-42/census-sources/start.stdout → CMP-IDENTICAL
grep -cP '\tE[0-9]' <that stdout> → 0
```
The four new rows (S155–S158) add no warning and no E code. The claims of the same warning set and zero E codes hold at the tip (`LOG.md:2202`, `SCORECARD.md:2020`).

### F2 — Row count is 113 under every extractor. SURVIVES.
```
grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md                  → 113   (column zero, SCORECARD's command)
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md    → 113   (0–3-space extractor)
grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md → 113 (any indent; no hidden indented row)
same two on `git show c77c2b7:corpus/SOURCES.md`               → 109 / 109
awk -F'|' '/^\| S15[5-8] \|/{print $2, NF}' corpus/SOURCES.md   → S155..S158 each 13 fields
```
These agree with "Rows 109 → 113" (`corpus/SOURCES.md:446`, `LOG.md:2198`) and with "113 rows at round 42" (`SCORECARD.md:2020`). The only commit touching SOURCES.md in `c77c2b7..a21845f` is `5f739ac`.

### F3 — Collision replay matches the receipts byte for byte. SURVIVES.
The replay uses the round-38 canonical extractor `'^ {0,3}\|[[:space:]]*S[0-9]{3,}'` (`.ufo/waves/round-38/spec-w1.json:149`). The registry is the base `c77c2b7:corpus/SOURCES.md`. The staged package is `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`, sha256 `020fbeaa…4807`.
```
grep -oE "$X03" reg | grep -oE 'S[0-9]{3,}' | sort -u > reg-ids        → 109
grep -oE "$X03" staged | grep -oE 'S[0-9]{3,}' | sort -u > staged-ids  → 103
comm -12 reg-ids staged-ids > collisions                               → S153 S154
cmp vs .ufo/waves/round-42/assimilation/{reg-ids,staged-ids,collisions} → IDENTICAL ×3
diff collisions .ufo/waves/round-42/assimilation/collisions            → empty
sha256 both = 412b6658f65611f1eaea9e751ca1e9f2720c9c61a25f6557aa52c676bc443882
```
Guard replay: base registry plus the line `  | S159 | guard fixture indented row | … |`. The rebuilt `guard/SOURCES.md` is IDENTICAL to the committed one. The 0–3-space extractor gives `S153 S154 S159`; the column-zero extractor gives `S153 S154`. All four of `guard/{reg-ids,reg-ids-col0,collisions,collisions-col0}` are IDENTICAL. This confirms `corpus/lessons/round-42.md:69-75` and `corpus/SOURCES.md:447`.

### F4 — The lesson does not state the 113-row end-of-round census, and no receipt for it is committed. LOW (records gap, not a false claim).
- `rg -n 'round end|after the append|113|→ 113' corpus/lessons/round-42.md` → no match. The lesson Gate (`:77-81`) states only the round-start validate (109 rows) and the scratch-mirror validate.
- The 113-row, same-warning-set, zero-E claim lives only in `LOG.md:2201-2202`, `SCORECARD.md:2020` and `corpus/SOURCES.md:446`.
- `git ls-files .ufo/evidence/round-42/census-sources` → only `start.exit` and `start.stdout`; no `end.*` receipt is committed.
- The mirror that `assimilation/validate.stdout` names (`.ufo/waves/round-42/assimilation/validate/corpus/SOURCES.md`) does not exist (`ls` → No such file). So that receipt's row count cannot be re-derived from committed bytes.

F1 and F2 above now provide the missing end-of-round evidence, and it agrees with the claim.

### F5 — After the append, the staged package collides on six ids, and the records do not say so. LOW (residual hazard for the next assimilation).
```
comm -12 <0–3-space ids of a21845f:corpus/SOURCES.md> staged-ids → S153 S154 S155 S156 S157 S158
grep -nE '^ {0,3}\|[[:space:]]*S(15[5-8]) ' SOURCES.append.md    → :9 arXiv 2302.09330, :10 arXiv 2406.09843, :11 JOSS Hypothesis, :12 Lam et al. UIUC
```
The lane's S155–S158 are now different documents from `staged:S155`–`staged:S158`. `corpus/SOURCES.md:448` sets `Next unused id: S159`, but `staged:S159`–`staged:S255` still occupy that range in the package. The lesson disclaims only `staged:S156` (`corpus/lessons/round-42.md:58`). The round-41 record logged its collision as a hazard for the next round (`corpus/SOURCES.md:442`); round 42 does not log the post-append set. This is not a defect in any stated claim. The next assimilation must re-run `comm -12` against the tip, which its contract rule requires anyway (`.ufo/evidence/round-42/contract.json:60`).

## Residual risk / verification gaps
- The lane's `.ufo/waves/round-42/w1/ScoutRegistryState.md:3` labels `'^\| {0,3}S[0-9]{3} \|'` as the 0–3-space count. That pattern allows 0–3 spaces after the pipe, not leading indent. It gives the same 109 at base, so no number changed, but the label is wrong.
- The census tool ignores rows indented 4 or more spaces (`measure.py:77`; already found in `ExecC1Falsify.md:38`). The any-indent count of 113 shows no such row exists at the tip.

SURVIVES
