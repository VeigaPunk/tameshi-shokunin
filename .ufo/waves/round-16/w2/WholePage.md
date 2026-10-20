# WholePage — full-page contradiction / stale-summary / self-anchor audit

Seat: `TameshiR16.WholePage` (round 16, wave 2, falsify lane)
Target: `SKILL.md` at lane commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8`
Verified page sha256: `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (1795 lines)
Snapshot: `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` (1704 lines, `e69b488:SKILL.md` and `.ufo/evidence/round-16/coldread/SKILL.snapshot.md`)
Scratch: `/tmp/tameshi-r16w2-WholePage-FW476N`. No lane writes except this report; no installs or upgrades (read-only git/python/sha256sum work only).

**Verdict: partial** — the method sections and the dated receipts hold under re-check, but the page's present-tense state layer does not: its artifact map says six legs while the harness at the same commit has seven, several case/band summaries stop at earlier rounds, one self-anchor quotes wording the errata itself repaired away, three errata line references point at the wrong snapshot lines, `git show 97cf436b…` does not resolve, and the closing box-3 claim fails the page's own `measure.py` at `c699c8c` because the ledger it cites is absent.

---

## 1. What held (re-checked, not assumed)

1. Page bytes: `git cat-file -p c699c8c:SKILL.md | sha256sum` → `3d8a1edb…cb7a4`; `wc -l` → 1795. Match.
2. Snapshot bytes: `git cat-file -p e69b488:SKILL.md | sha256sum` → `97cf436b…3580`, 1704 lines. `.ufo/evidence/round-16/coldread/SKILL.snapshot.md` at the same commit has the same sha. The errata's snapshot claim is correct.
3. Line-count stability: `diff` of snapshot lines 1–1704 against current lines 1–1704 yields exactly 14 replaced ranges, every one a 1-for-1, 2-for-2 or 3-for-3 replacement (`15`, `63`, `134-135`, `271-272`, `278-280`, `361`, `505`, `514-515`, `925`, `950`, `1390`, `1393`, `1472`, `1614`). No pre-existing section changed length, so all numeric `:n` anchors still land on the same section. This part of the errata claim is true.
4. Bucket arithmetic: the snapshot has 50 `#`/`##`/`###` headings outside fences plus the preamble = 51 buckets; `assemble.py:16` says exactly "The snapshot produces 51 buckets (50 headings + preamble)." Match.
5. Seat count: `.ufo/waves/round-16/assignments1.json` has exactly 30 `CR\d` seats (`CR01`–`CR27`, plus `CR04a/b`, `CR11a/b`, `CR12a/b`). Match to "30 lane seats". The 38 `CR*.md` reports at the commit are not a contradiction — several seats wrote more than one report.
6. Seventh case pin: `git -C kumitate-shokunin cat-file -p 364f1d5…:scripts/round-gate.mjs | sha256sum` → `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`, matching L1743-1744 and L1755. `runner-regression.txt` at the commit shows the `js-round-gate` leg: `killed=5 survived=5 inconclusive=0 kill-rate=50%` and `REGRESSION: PASS (cases=7 passed=7; …)`. `runner-selftest.txt` shows `MUTATE_SELFTEST: 81/81 pass`.
7. Harness leg count: `tools/mutate-and-run.sh:85-91` at the commit lists seven ledger comment lines (`js-kimi-census`, `bash-surface-census`, `bash-tsukuroi-census`, `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`, `js-round-gate`). `measure.py --rev c699c8c…` reports `"recorded_cases": 7`, `"depth_score": 7`. The seventh leg is real.
8. Errata coverage of the diff: every actual in-place edit in lines 1–1704 is represented by an errata row (14 ranges; 13 rows, with two edits sharing a row). No unlisted edit was found in the common prefix.

---

## 2. Findings

### F1 — BLOCKING: the box-3 claim fails the page's own counting command; the ledger it cites is absent

The page says (L1781-1787):

> "**The full-page cold-read.** Every bucket of this page was read by a seat that saw only the page and what it names; instructions were executed in `/tmp`, records re-anchored. … The counting command: `python3 .ufo/evidence/round-16/measure.py --rev REV` (field `coldread.box3_full_page`). Lane seats are the lane: this earns the box-3 lane assertion (`[~]`), never an independent `[x]`."

and names the evidence (L1711-1712):

> "reports `.ufo/waves/round-16/w1/CR*.md`, ledger `.ufo/evidence/round-16/coldread/ledger.json`."

Observed:

```
$ git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json
fatal: path '.ufo/evidence/round-16/coldread/ledger.json' does not exist in 'c699c8c…'
exit=128

$ git ls-tree -r --name-only c699c8c | grep -i ledger.json
(no output; exit=1)
```

Running the committed counting command itself (`measure.py` was extracted from `c699c8c`, not the dirty worktree):

```
$ python3 /tmp/.../measure.py --rev c699c8c36d6e4eca4b796b81a8247904aa145ec8
"calibration_restraint_score": 6,
"coldread": {"box3_full_page": false, "ledger_present": false,
             "sections_covered": 0, "sections_total": 54, ...},
"depth_score": 7,
"recorded_cases": 7,
"shonen": {"box3_ledger_link": false, "box3_marked": true, "box3_points": false, ...}
EXIT=0
```

`measure.py`'s own docstring defines "no ledger → box3 false, score 6" (lines 37-39). `SHONEN.md:10` also cites the absent ledger. The wave-1 reports exist, and `assemble.py` can build the ledger, but at the named commit the file is absent and the page's box-3 claim is not reproducible from its own evidence. **This is the page's own closing claim failing its own command.** If wave 2 is expected to assemble the ledger, the page should date/mark the claim pending; it currently states it as done.

Secondary cause: `box3_ledger_link=false` even apart from the missing ledger — `measure.py`'s `BOX_RE` matches only the `- [~]` line (`SHONEN.md:9`), while the ledger path sits on the continuation line `SHONEN.md:10`.

### F2 — HIGH: "repaired and new sections were re-read in wave 2" is not evidenced at the commit

L1781-1784:

> "Every bucket of this page was read by a seat that saw only the page and what it names; instructions were executed in `/tmp`, records re-anchored. … repaired and new sections were re-read in wave 2."

Observed: `c699c8c` has author and committer time `2026-10-20 10:49:37 -0300`; the first wave-2 report in `.ufo/waves/round-16/w2/` is timestamped 10:53 and later (all untracked relative to the commit). The current page has 54 sections (`measure.py` `sections_total: 54`), the cold-read snapshot has 51 buckets; the three new sections (`Errata`, `Seventh recorded case…`, `Round-16 gate/probe registry`) are not in the snapshot and have no committed seat reports at `c699c8c`. The past-tense "were re-read" overstates the commit's evidence. Wave-2 reports now in the worktree may satisfy it later; at the commit they do not.

### F3 — HIGH: the artifact map says six legs; the harness at the same commit has seven

L1391 (current-state map row):

> "`tools/mutate-and-run.sh` | the instrument: `--selftest`, `--regression` (six-leg registry, git-materialized replay) | any sweep or replay"

Contradicted by the page itself and the artifact:

- L1390: "`corpus/knowledge/mutation-case-*.md` (six at round 11; seven since round 16)"
- L1747-1748: "The case is ledger leg `js-round-gate` (`tools/mutate-and-run.sh --regression` → `cases=7`)."
- `tools/mutate-and-run.sh:85-91` has seven leg lines; `measure.py` reports `recorded_cases: 7`.
- `.ufo/evidence/round-16/round-gate/runner-regression.txt` closes `REGRESSION: PASS (cases=7 passed=7; …)`.

Same stale "six" phrasing at:

| Line | Quote | Note |
|---|---|---|
| L1361 | "a ledger row recording the six-leg registry is the ledger owner's follow-on" | explicitly scoped "as measured at `r10-2`"; reads as a six-leg name, but the count is dated |
| L1456 | "the ledger row for the six-leg registry (`:1359-1363`)" | round-11 open item "at this write"; round 16 embeds the seventh leg, so the item is now resolved |
| L1483 | "not a change to the six-leg runner" | round-12 text, present tense |
| L1552 | "six-leg content disposition" | round-13 probe label; lower confidence (may be the manifest's fixed name) |
| L1555 | "No registry row changes rank, SHONEN authority, or the six recorded cases." | scope-ambiguous; the corpus now has seven |
| L1689 | "the six recorded cases, or the archived round-12–14 bytes" | same scope ambiguity |

The one unambiguous current-state failure is L1391: the standing map's instrument description says "six-leg registry" with no date, while the instrument at the same commit has seven. L1361/L1456/L1483/L1509 are dated or scoped but now read as open/stale items; L1555/L1689/L1552 are lower-confidence because they may denote the fixed set at that round.

### F4 — HIGH: self-anchor `:925-929` quotes repaired-away wording

Citing text (L1345-1346):

> "- **The supersessions stay append-only.** The round-7 section's "Four legs at this revision" (`:925-929`) and the round-9 receipt's `cases=4`"

Target (L925):

> "pinned original revision. Four legs at **that** revision (r7-1; seven since round 16) — `js-kimi-census`"

The quoted words "at this revision" no longer exist at the target; the errata repaired L925 (its own row L1727 records the old wording) but did not update the dependent quote at L1345. This is exactly a self-anchor whose target line no longer says what the citing text claims. The errata's summary "so every `SKILL.md:<line>` self-anchor still resolves" (L1713-1714) is true of line *numbers* but false of this *content*.

### F5 — HIGH: `git show 97cf436b…` is not a resolvable git object

L1713-1715:

> "the old wording stays in git (`git show 97cf436b…` is the snapshot blob at commit `e69b488`)."

Observed:

```
$ git cat-file -e 97cf436b
fatal: Not a valid object name 97cf436b
exit=128
```

`97cf436b…3580` is a sha256 of the snapshot bytes, not a git object id. The working retrieval is `git show e69b488:SKILL.md` (sha256 of that output matches), or `sha256sum .ufo/evidence/round-16/coldread/SKILL.snapshot.md`. As written, the errata's own "old wording stays in git" recovery instruction fails.

### F6 — MEDIUM: the preamble still says two mutation cases

L8-10:

> "Rounds 1–3 built the corpus from measured surfaces; every rule below earns a cited source. **Two mutation cases are now measured** — round 2 JS, round 3 bash, both 8/10 killed — and this page carries the method…"

Contradicted by L1390 ("six at round 11; seven since round 16"), L1742-1748 (the seventh case), and the page's own six-case statement at L1092-1154. The preamble is round-3-era text; only L14-15 was repaired. L234 ("the two mutation-case notes are the model") names two of seven notes the same way.

### F7 — MEDIUM: kill-rate band/crossover summaries are stale

L337-339:

> "(U: the 50 % crossover itself is unmeasured — both measurements landed at 80 %, so the band interiors are still unprobed; …)"

L717-719:

> "The bands table's 50-80 % row is now the measured one, superseding the 'band interiors unprobed' (U) — >80 % and <50 % stay unprobed, and the 50 % crossover is still unmeasured."

Contradicted by later measured sections in the same page:

- L899-920: mado `4/10 = 40 %`, "the first point below the 50-80 band".
- L1145: "the band now reads 40 / 47 / 60 / 70 / 80 / 80."
- L1744: round-gate "5/10 killed (50 %)" — the 50 % point itself is now measured.

L1150-1151 ("Unknown in all six … the 50 % crossover") is accurate only for the six-case set; as a page-level statement it is stale after round 16.

### F8 — MEDIUM: "Cases 5–6 are still not embedded" contradicts the six-leg receipt and its own resolution note

L1227-1228 (round 9):

> "Cases 5–6 are still not embedded: their rows carry no `REGRESSION` line — named debt, not smoothed"

L1339-1341 (round 10):

> "`--regression` → six legs, all exact: `match=10/10` (legs 1–4, 6), `match=15/15` (leg 5), … closing `REGRESSION: PASS (cases=6 passed=6; …)`"

L1347-1348:

> "the round-9 caveat that cases 5–6 were 'still not embedded — named debt' … is resolved at `r10-2` by embedding the recorded T8-1/T8-2 spec files"

The round-9 caveat is not dated in place; a reader reaching L1227 sees a present-tense claim that is false after L1348. This is the same pattern as F15: a later section resolves it, but the old sentence stays in the live present tense.

### F9 — MEDIUM: the receipt grammar is universalized to `defects=10` / `match=10/10`, but leg 5 has 15

L973-975:

> "Every case line `PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)` and every `REGRESSION_TABLE … match=10/10 … flips=0`; the closing line's `cases=4 passed=4`."

L1339-1340:

> "`--regression` → six legs, all exact: `match=10/10` (legs 1–4, 6), `match=15/15` (leg 5)"

Leg 5 (`bash-checklist-run`) has 15 defects, so "every case line … defects=10" and "every `REGRESSION_TABLE … match=10/10`" are false for it. The rule is round-7 grammar; the round-10 receipt already contradicts it. (The `cases=4` literal in the same rule is also a stale round-7 instance, though the following "Measured instance (T7-1…)" partly dates it.)

### F10 — MEDIUM: "three readings per case" vs "two readings"

L1014-1016:

> "**the cadence is a pin read executed at the tick** — three readings per case, three triggers, one re-pin rule"

L1027-1029:

> "- **Per case, two readings:** the target's relation to the fleet's live bytes (`current` / `stale` / `drift`) and the tool's relation to the last run (`held` / `moved`):"

Direct numeric contradiction inside the same section. The table has two reading rows; the intro says three.

### F11 — MEDIUM: "Round 11 … is the arc's final round" while rounds 12–16 follow

L1367:

> "Round 11 (training r10) is the arc's final round (`plans/round-11.plan.md:13`)"

L1374-1375:

> "the arc ends, the service remains, run by whoever the handoff names"

Later headings in the same page: `## Repeated controls and gate registry — round 12` (L1479), `## Pin disposition and provenance correction — round 13` (L1517), `## Effective expectation reconciliation — round 14` (L1563), `## Context gate classification and explicit exit classes — round 15` (L1609), `## Seventh recorded case and full-page cold-read — round 16` (L1740). If "arc" means the training arc specifically, the page never says the later rounds are a different arc; the "final/close" framing is contradicted by its own contents.

### F12 — MEDIUM: "Live instances today" is stale

L1073-1074:

> "Live instances today: tsukuroi `084951be…` (6/10) → live `bba6cdf6…`; mado `d7edaab4…` (4/10) → live `90d50cdd…`."

Later reads in the same page give different live bytes:

- L1184-1185 (round-9 tick): tsukuroi HEAD `72b038da`, live blob `bba6cdf6`; mado HEAD `12c8f08a`, live blob `7da4ec50`.
- L1404-1406 (round-11 pin read): tsukuroi live `10452443` (HEAD `af8adf15`); mado live `93e43f8f` (HEAD `f7bfc9fe`).

"Today" at round 8 is not today at round 11/16; the sentence is a timestamped observation presented as a standing one.

### F13 — MEDIUM: "no mutant experiment yet tests the suites' own code against regressions" vs the page's own method

L126-128:

> "**Unmeasured stays named.** Round-gate `INTERNAL_ERROR` has no hermetic case; integration groups were not executed; **no mutant experiment yet tests the suites' own code against regressions**"

L133-134 defines the method as:

> "Runs a suite's own code through one-exact-edit mutants and measures what it catches."

The page's round 2 does exactly that to `kimi-census.mjs`, a kumitate suite (L39-41, L527-593; the manifest at L571-582 mutates `kimi-census.mjs` ten times). On the page's own definition, the sentence is false. If the intended meaning is a different object ("regressions of the suite's own code" rather than "mutants in the suite's code"), the sentence is at least ambiguous and undated.

### F14 — MEDIUM: D5 is assigned to two different defect classes

L298:

> "| dropped arm | delete the arm's reporting/effect lines | … | D4 → 3 root-enum cases; **D5 → 1** (mutation-case-kimi-census.md:47-48) | …"

L299:

> "| weakened presence gate | force a presence bool to `true` | … | **D5 → 1** (mutation-case-kimi-census.md:48) | …"

D5's manifest edit (L576) is `const present = gens.length > 0;` → `const present = true;` — a bool force, not a deletion. One mutant cannot be both a dropped arm and a weakened presence gate. The "dropped arm" row should cite only D4.

### F15 — MEDIUM: round-5 "zero JS instances" vs round-8 "first JS instance"

L727:

> "| E unreached arms | none (D4/D5 reached) | B5 survives | B10 survives; §3.2 static inventory | **promoted toward pattern, still proposed** — 2 bash instances + inventory, **zero JS instances**; repair shape (add a case per arm) consistent |"

L1146-1148:

> "**Amended by the sixth case:** unreached-arm survivors — `D9` is the class's **first JS instance** … so the round-5 reading ('two bash instances, still zero JS') no longer stands"

The page acknowledges the amendment, but the round-5 table cell remains in the live present tense with no supersession mark. The same is true of F8.

### F16 — MINOR: the PROVINCE two-lane bar is cited at two different line ranges

L340: "… ≥2-lane bar, `PROVINCE.md:16-17`."
L462: "… the method's two-lane generality bar is met for the measured shapes (`PROVINCE.md:16-17`) …"
L763: "**Three-case confidence statement** (PROVINCE's two-independent-lanes bar, `PROVINCE.md:15-16`; …)"

Same claim, two ranges. At most one is right at the revision the page claims to have re-resolved ("All refs below were re-resolved by line number on 2026-10-14", L54-55). This is a source-anchor inconsistency, not a page self-anchor.

### F17 — MINOR: "886-line bash gate" vs "886 newlines (the 887th line …)"

L408:

> "kagi's `surface-census.sh` (886-line bash gate, 16-case selftest)"

L603:

> "44212 B, 886 newlines (the 887th line carries no trailing newline), mode 755"

A file with 886 newlines and an unterminated 887th line has 887 lines; the page calls it 886-line. The two statements are reconcilable only if "line" means "newline-terminated line", which Appendix B does not say.

### F18 — MINOR: three errata "Snapshot line" references point at the wrong snapshot lines

The errata table (L1717-1731) uses a "Snapshot line" column. Three rows cite lines that do not contain the quoted "Was" text:

| Row | Cites | Actual snapshot line(s) containing the quoted text |
|---|---|---|
| L1721 | `61` | snapshot 61 is the table separator `\|---\|---\|---\|`; the quoted live-gate row is snapshot **63** |
| L1722 | `269-270` | snapshot 269-270 are the D3 sentence and code line; the quoted "produces a *different mutant*" is on snapshot **271-272** |
| L1729 | `1388, 1392` | snapshot 1388 is the `fleet-suite-census.md` map row and 1392 is the `corpus/README.md` row; the quoted mutation-case row is **1390** and the quoted plans row is **1393** |

Two more are partial ranges: L1719 cites `15` but the quoted phrase begins on snapshot 14 ("Historical cold-read proof covers" on 14, "one JS mutant only…" on 15); L1723 cites `277-279` while the actual replacement spans 278-280 (it misses 280). The repairs themselves are in the diff; the index is wrong. This matters because the errata is the page's own map of what changed, and a reader re-checking `61`/`1388`/`1392` finds the neighboring rows.

### F19 — MINOR: self-anchor paraphrases that no longer match their targets

1. **`:811-812`** — citing text L1083-1084: "A moved pin is never re-interpreted against the new bytes (`:811-812`)." Target L811-812: "A moved substrate needs a re-pin, never a re-interpretation of the old table." The target has the opposite object ("old table", not "new bytes") and does not mention a pin. Semantics are close, wording is not.
2. **`:1250-1254`** — citing text L1294-1296: "where it and an anchored source diverge, the anchored source governs — the same rendering/divergence rule this page applies to `service-limits.md` (`:1250-1254`)." Target L1250-1254: "this page is the compact rendering, and a divergence between the two is the finding, never smoothed." The target does not say "the anchored source governs"; it says divergence is the finding. Different rule.
3. **`:1019`** — citing text L1160-1162 repeats the round-8 `[U]` and anchors `(:1019)`. Target line 1019 alone is "no lane acting stays [U]."; the full antecedent is L1018-1019. Minor off-range.
4. **`:1294-1297`** at L1384 includes line 1297 (the next bullet); the rule is 1294-1296. Minor over-range.

All other page-internal numeric anchors landed in the named section and supported the citing text: `:813-817`, `:840-844`, `:823-825`, `:879-881`, `:925-929` (range itself), `:965-1008`, `:1017-1019`, `:1021-1053`, `:1069-1090`, `:1218-1222`, `:1226-1228`, `:1230-1244`, `:1246-1270`, `:1324-1331`, `:1332-1344`, `:1359-1363`, `:131`.

### F20 — MINOR: mid-round-8 present-tense phrases stale at round 16

- L1112: "both still being appended by their own lanes" — the two notes are cited as landed (L1141-1142) and the count is seven by L1390.
- L1131: "would add a seventh *artifact* and a fifth *author*" — with seven recorded cases, the harness meta-sweep would now be an eighth artifact.
- L1145: "the band now reads 40 / 47 / 60 / 70 / 80 / 80" — the page now has a seventh rate, 50 (L1744); the live band is 40/47/50/60/70/80/80.
- L1150-1151: "Unknown in all six … the 50 % crossover" — accurate only of the six-case set; round 16 measures 50%.

### F21 — LOWER-CONFIDENCE / scope-ambiguous

- **L1555** "the six recorded cases" and **L1689** "the six recorded cases": these are round-13/15 registry-scope statements, not necessarily claims that the corpus still has six. They are stale as counts if read page-level; no contradiction if read as "the six cases existing at that round."
- **L1552** "six-leg content disposition" is a round-13 probe/registry label. The harness has seven legs now, but the probe's manifest may intentionally cover the six legs it was written for. Flagged as a label to check, not a defect.
- **L1509** "The bash study deepens one recorded case, never a seventh independently measured gate." Scoped to the bash study; true of that study, but the page now has a seventh independently measured gate (round-gate). The sentence reads as a corpus-level denial; it should be dated.

---

## 3. Command log (key commands, exits, key lines)

| Command | Exit | Key output |
|---|---|---|
| `git cat-file -p c699c8c:SKILL.md \| sha256sum` | 0 | `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` |
| `git cat-file -p c699c8c:SKILL.md \| wc -l` | 0 | `1795` |
| `git cat-file -p e69b488:SKILL.md \| sha256sum` | 0 | `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580`; 1704 lines |
| `git cat-file -p e69b488:SKILL.md \| wc -l` | 0 | `1704` |
| `git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json` | 128 | `fatal: path '…/ledger.json' does not exist` |
| `git ls-tree -r --name-only c699c8c \| grep -i ledger.json` | 1 | no output |
| `python3 <committed measure.py> --rev c699c8c` | 0 | `box3_full_page:false`, `ledger_present:false`, `sections_covered:0`, `sections_total:54`, `calibration_restraint_score:6`, `shonen.box3_points:false` |
| `git cat-file -e 97cf436b` | 128 | `fatal: Not a valid object name 97cf436b` |
| `git cat-file -p c699c8c:tools/mutate-and-run.sh \| grep -n '^#   (js\|bash)-'` | 0 | seven leg lines, lines 85–91, including `js-round-gate … 5/10 (50 %)` |
| `git cat-file -p c699c8c:.ufo/evidence/round-16/round-gate/runner-regression.txt \| tail -8` | 0 | `killed=5 survived=5 inconclusive=0 kill-rate=50%`; `REGRESSION: PASS (cases=7 passed=7; …)` |
| `git cat-file -p c699c8c:.ufo/evidence/round-16/round-gate/runner-selftest.txt \| tail -5` | 0 | `MUTATE_SELFTEST: 81/81 pass` / `VERDICT: PASS` |
| `git -C kumitate-shokunin cat-file -p 364f1d5…:scripts/round-gate.mjs \| sha256sum` | 0 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` |
| `git cat-file -p c699c8c:.ufo/waves/round-16/assignments1.json \| python3 …` | 0 | 30 `CR\d` seats |
| `git cat-file -p c699c8c:SHONEN.md \| sed -n '5,12p'` | 0 | box 3 `[~]`; ledger path on the continuation line 10 |
| `diff snapshot.md <(SKILL.md lines 1–1704)` | 1 | 14 changed ranges, all 1:1/2:2/3:3 replacements |
| `git -C tameshi-shokunin show -s --format='%ai %ci' c699c8c` | 0 | `author=2026-10-20 10:49:37 -0300 committer=2026-10-20 10:49:37 -0300` |
| `ls -l --time-style=+%H:%M:%S .ufo/waves/round-16/w2/` | 0 | first w2 report 10:53; rest 10:55–11:01 (untracked) |

---

## 4. Residual risk and verification gaps

1. **The ledger can be mechanically built but is not committed.** `assemble.py` exists at the commit (default output `.ufo/evidence/round-16/coldread/ledger.json`, `DEFAULT_OUT` at line 59) and its docstring says it assembles 51 buckets from the 30 seat reports. A wave-2 assembly could make F1/F2 true retroactively, but at `c699c8c` the page's claim is unsupported. The ledger would also need entries for the three post-snapshot sections, not just the 51 snapshot buckets.
2. **`box3_ledger_link`** would remain false even with a ledger unless `measure.py`'s line-only `BOX_RE` or `SHONEN.md`'s box-3 line changes: the path is on `SHONEN.md:10`, the `- [~]` marker is on line 9.
3. **Two anchor paraphrases** (F19.1/F19.2) are close enough that a lenient reader could call them acceptable restatements; a strict "target says what citing text claims" standard fails them. I report both sides verbatim so the L1 can decide.
4. **The six-leg label at L1552** and the "six recorded cases" at L1555/L1689 are scope-ambiguous; I did not treat them as hard defects.
5. No sibling gate was executed; no lane file was edited. The page's substrate claims (sha pins, line counts) were checked read-only through `git show`; the two live sibling pins (`kumitate` 364f1d5 and the seventh-case blob) were verified byte-for-byte.
6. The page's `SKILL.md:<line>` self-anchor claim was tested by content, not only by line number. Line numbers hold (F3 held section spans); content fails at L1345-1346.
7. Cross-artifact note (not a page defect): the map row L1384 accurately describes `corpus/knowledge/operator-runbook.md` §3 as "the six-case ledger", but the runbook at the same commit still says "six-case" (its L4, L49, L131, L178, L411, L447). The page's pointer is accurate about a stale runbook; the runbook's own `SKILL.md:1092-1104` anchor still resolves to the six-case roster. The L1 may want the runbook updated separately.

---

**Bottom line:** the page's method and its dated receipts survive re-execution of their pins; its "current state" layer does not. The highest-value repairs for wave 2 are: (a) generate/commit the cold-read ledger and make `measure.py` box3 true (or mark the claim pending), (b) replace every live "six-leg/six recorded" with the seven-leg state, (c) fix the `:925-929` quote, (d) fix or remove the `git show 97cf436b…` instruction, (e) correct the errata's snapshot-line index, and (f) reconcile the `:811-812`/`:1250-1254` paraphrases.
