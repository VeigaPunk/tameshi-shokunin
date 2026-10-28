# T56W2Read09 — cold-read re-read of one SKILL.md section at C0

- **Seat:** `T56W2Read09` (wave 2, reader seat 9 of 18)
- **Heading:** `## The operator's runbook and the six-leg regression (round 10, measured)`
- **C0 (content commit):** `c0137451f5b7f22d65f748fc69f1b181f55e1378`
- **`section_sha256`:** `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7`
- **Section range at C0:** lines **1312–1320** (8 lines: the heading, a blank, and the round-10 orientation paragraph)
- **Verdict:** `verified-record` — `findings` is empty; every claim in the section is TRUE of the tree at C0 and every command it names runs.

## How the section was read

The section bytes were taken with the **frozen round-18 sectionizer**, never reimplemented for the hash:

```
python3 -c "import importlib.util,subprocess; s=importlib.util.spec_from_file_location('r18','/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); raw=subprocess.run(['git','-C','/home/vgpnk/Projects/shokunin/tameshi-shokunin','show','c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md'],capture_output=True,check=True).stdout; print([(x['start'],x['end'],x['sha256']) for x in m.sectionize(raw) if x['heading']==\"## The operator's runbook and the six-leg regression (round 10, measured)\"])"
```

Output:

```
[(1312, 1320, '636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7')]
```

The same sha was reproduced by a second, independent reimplementation of the sectionize rules (heading line → line before the next heading, trailing whitespace-only lines stripped, joined by `\n`, no trailing newline), which matched byte-for-byte. Receipt: `T56W2Read09-receipts/00-sectionize-at-C0.stdout`.

The section body read end to end:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md | sed -n '1312,1320p'
```

```
## The operator's runbook and the six-leg regression (round 10, measured)

Round 7 made `--regression` the ledger's replay gate; rounds 8–9 left two
named gaps: the registry ran four legs with cases 5–6 not yet embedded —
named debt (the round-9 receipt's wording; ER-4 caveat (a)), and the operator the arc was built for had no
single entry point. Round 10 closes both — the runbook lands (T10-1, this
round), and the leg cut resolves as an **embedding** of cases 5–6 (T10-2),
never a re-cut.
```

The two `###` subsections under it (1321 "The operator's runbook", 1342 "The six-leg regression") are **separate sections** under the frozen sectionizer, so they are outside this seat's byte range; they were read as context and are cited below only where they corroborate or constrain this section.

## The commands this section names, run at C0

The section names `--regression` as the ledger's replay gate and points the reader at the runbook and at the r10-2 leg cut. Those commands were run in a scratch clone of the lane at C0 (`git clone --shared`, then `git -C <clone> checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378`), with the four sibling repos (`kumitate`, `kagi`, `tsukuroi`, `mado`) cloned beside it as the tool requires.

```
bash tools/mutate-and-run.sh --regression --workdir $S/regwork2
```

`rc=0` — full receipt in `T56W2Read09-receipts/regression-at-C0.stdout`:

```
REGRESSION_TOOL: .../clone/tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10 js-round-gate=5/10 js-sources-check=5/10 js-cite-check=5/10 bash-drift-pins=2/10
REGRESSION_CASE js-kimi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-surface-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-tsukuroi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-mado-verify: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-checklist-run: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=15)
REGRESSION_CASE js-claims-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-drift-pins: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```

```
bash tools/mutate-and-run.sh --selftest
```

`rc=0` — `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS` (full output: `T56W2Read09-receipts/selftest-at-C0.stdout`).

## Claim-by-claim

### 1. "Round 7 made `--regression` the ledger's replay gate" — TRUE

`SKILL.md:949-955` (the round-7 section): *"Round 7 turns `--regression` from the tool's two-case self-check into the fleet's **leg ledger**: every recorded mutation case is a leg of this ledger, replayed at its pinned original revision."* The tool carries the mode (usage at `tools/mutate-and-run.sh:206`, dispatch from `:1459`); it ran green at C0 as shown above.

### 2. "rounds 8–9 left two named gaps: the registry ran four legs with cases 5–6 not yet embedded" — TRUE for the round-8/9 boundary

```
git show 9f1d3c3:tools/mutate-and-run.sh | grep -nE '^#   (js|bash)-'
```

```
75:#   js-kimi-census       kumitate-shokunin/scripts/kimi-census.mjs  8/10 (80 %)
76:#   bash-surface-census  kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)
77:#   bash-tsukuroi-census tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)
78:#   bash-mado-verify     mado-shokunin/tools/mado-verify.sh          4/10 (40 %)
```

Four legs at r7-1, and the ledger records the same at the tick:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '350p'
```

> Two measured caveats, stated not smoothed: (a) the tool embeds **4** legs — cases 5/6 (checklist-run, claims-check) carry no `REGRESSION` line at `cf41efaa…`; the leg-cut decision stands with the tool owner (ER-2's named hand-offs, `:282`), nothing re-cut to manufacture a line; …

### 3. "named debt (the round-9 receipt's wording; ER-4 caveat (a))" — TRUE, and the provenance is correct

The round-9 receipt block (`SKILL.md:1244-1260`) carries the phrase at `:1259-1260`:

> …read `stale`. Cases 5–6 were not yet embedded at this boundary (they became legs 5–6 at r10-2; the current tool carries them at `tools/mutate-and-run.sh:88-97`): their rows carried no `REGRESSION` line at this boundary — named debt, not smoothed (`fleet-kill-rate-ledger.md:282`; the debt was retired when the legs embedded).

and the ledger's ER-2 named-follow-up cell says the same:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '282p'
```

> **Named follow-ups (not edits, not written here).** Cases 5/6 are not embedded in `--regression`: T8-2 E3 records the target pin / suite / spec for the tool's owner, and T8-1 U5 leaves the leg-cut decision to the same owner — rows 5/6 therefore carry no `REGRESSION` line over themselves. …

Both cited anchors resolve; the phrase really is the round-9 receipt's wording.

### 4. "the operator the arc was built for had no single entry point" — corroborated at C0

`plans/round-10-record-draft.md:205` (round-10 record, at C0): *"round-9 state: the cadence's first tick recorded (4/4 legs PASS) but the operator had no single entry point; the registry ran **four** legs (cases 5/6 "not embedded — named debt")"*. Round-8's own record names the second half of the gap (`plans/round-8-record-draft.md:58`): *"are **not embedded** in `--regression` (named hand-offs T8-2 E3 / T8-1 U5)"*.

### 5. "the runbook lands (T10-1, this round)" — TRUE

`corpus/knowledge/operator-runbook.md` exists at C0 with the title `# Operator runbook — the tameshi mutation service, end to end (round 10, T10-1)`, 516 lines / 33 515 bytes, and its blob is identical at `59c38109` and at C0 (`54c72164fa76f0a00f3b0bf1a2af6a87518a326b`), so the "the sha governs" rule at `SKILL.md:1323-1324` holds. The runbook's own quick-start block (`§0`) runs: `sha256sum tools/mutate-and-run.sh`, `--selftest` (107/107 PASS at C0), `--regression` (10/10 PASS at C0), and the per-case pin read (`sha256sum`, `git show <tip>:<path> | sha256sum`, `git status --porcelain`, `git merge-base --is-ancestor`) — all exercised successfully.

### 6. "the leg cut resolves as an **embedding** of cases 5–6 (T10-2), never a re-cut" — TRUE (the load-bearing claim)

Two independent checks, both in `T56W2Read09-receipts/02-embedding.stdout`:

**(a) Nothing existing was re-cut.** All twelve anchors of legs 1–4 — `PIN_JS`/`REV_JS`/`TABLE_JS`, `PIN_BASH`/`REV_BASH`/`TABLE_BASH`, `PIN_TSUKUROI`/`REV_TSUKUROI`/`TABLE_TSUKUROI`, `PIN_MADO`/`REV_MADO`/`TABLE_MADO` — are **byte-identical** between r7-1 (`git show 9f1d3c3:tools/mutate-and-run.sh`) and C0.

**(b) Cases 5/6 were added, not substituted.** They are new legs with their own pins (`PIN_CHECKLIST=7e5ec98b…` @ `REV_CHECKLIST=fecee874`, `PIN_CLAIMS=e9a21b44…` @ `REV_CLAIMS=175de6ba`), specs at `tools/mutate-and-run.sh:854` and `:925` (`# r10-2 leg 5:` / `# r10-2 leg 6:`), dispatch at `:1479-1487`.

The sibling section states the same (`SKILL.md:1389-1390`): *"resolved at `r10-2` by embedding the recorded T8-1/T8-2 spec files (their 25 `@old` strings re-verified `count==1` against the pinned blobs)"*. I reproduced that count independently: **15** `@old` in the leg-5 spec + **10** in the leg-6 spec = **25** total, and with the tool's own `ESCAPES` unescape every one of the 25 occurs **exactly once** in its pinned blob (0 violations).

## Cross-section consistency

- The sibling `### The six-leg regression — usage and this round's receipt` (`SKILL.md:1342-1404`) states the same resolution and keeps the supersessions append-only.
- The round-7 section (`SKILL.md:949-961`) keeps its "four legs at r7-1" reading **dated** rather than re-cut.
- A full-tree grep for `not embedded` / `still not embedded` in `SKILL.md` at C0 returns **no** hit that contradicts the round-10 resolution — no section still asserts cases 5/6 are unembedded in the current tree.

## Notes (improvements — not findings)

1. **"the registry ran four legs"** reads, for a moment, like `tools/registry.json` (57 rows at C0, one of them the `mutate-and-run-regression` gate). The parallel section at `SKILL.md:949` calls the same thing "the leg ledger"; using that name here would remove the ambiguity with the gate/probe registry.
2. The artifact this section points at carries one **stale line anchor** of its own: `corpus/knowledge/operator-runbook.md:175` and `:376` cite `SKILL.md:1226-1228` for the round-9 cases-5/6 caveat, but at C0 that range holds the falsifier paragraph ("substrate, same moment; the reading follows the row's pin, not the substrate's history"); the caveat now lives at `SKILL.md:1259-1260`. This is inside the runbook, not this section, and `SKILL.md:1425` makes the anchored source govern on divergence — but a reader who follows this section into the runbook will meet it. Receipt: `T56W2Read09-receipts/04-runbook-anchor.stdout`.
3. The round-9 receipt's amended line at `SKILL.md:1259` points at `tools/mutate-and-run.sh:88-97` for the current leg list; that range resolves correctly at C0 (legs 5 and 6 at `:92-93`).

## Census

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

exits **0** (only W-codes and one `ok` line for the tameshi registry).

Row count at C0 is **142** (base `981c5e8b` = 140; round 56 added S281 and S282), i.e. one more than the wave brief's "141 after this round's one new row". `corpus/SOURCES.md:521` records why: S281 is the mined row and **S282 is the deliberately added REFUSED row** (SLSA Build Provenance). The brief's arithmetic counts only the mined row; the census itself is clean and the validator's exit code is 0.

## Tooling

No tool was installed, upgraded, or modified for this seat — the work needed only `git`, `python3` (stdlib), `bash`, and `grep`, all already present. No `pacman` transaction was run (host-wide pacman transactions are paused).

## Files

- `T56W2Read09.json` — the machine-readable report the round-55 binder binds
- `T56W2Read09.md` — this file
- `T56W2Read09-receipts/00-sectionize-at-C0.stdout` — frozen sectionize at C0 + independent recomputation
- `T56W2Read09-receipts/regression-at-C0.stdout` — `--regression` at C0 (10/10 PASS, rc 0)
- `T56W2Read09-receipts/selftest-at-C0.stdout` — `--selftest` at C0 (107/107 PASS, rc 0)
- `T56W2Read09-receipts/01-pointers.stdout` — pointer resolution for every claim
- `T56W2Read09-receipts/02-embedding.stdout` — the "embedding, never a re-cut" evidence
- `T56W2Read09-receipts/03-consistency.stdout` — cross-section checks and the census
- `T56W2Read09-receipts/04-runbook-anchor.stdout` — the stale anchor inside the runbook (note 2)
