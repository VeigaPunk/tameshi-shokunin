# RR3 — cold-read re-read, wave 3 (residual), round 17

- Read rev: `0ff273448ac4e62893c9b28a4cea7c580712df19` (fresh clone `/tmp/tameshi-r17w3-RR3-DeW0UG/fleet/tameshi-shokunin`, fleet-mirror symlinks for the four sibling repos; nothing executed against the live lane root).
- Page check: `sha256sum SKILL.md` → `de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc` (matches the pinned page identity, 1903 lines). Assigned section spans re-hashed from the page bytes: lines 1155–1163 → `dcfb2df9002dc26a506945a75b96eba941027872d4332e5f6148f6a8a696413f`, lines 1246–1271 → `bc252ddc1e16e1cafa1ec8fe7ba547e1215c0f8f60595d9182d3b526b3373d7b` — both match the assignment exactly (convention: lines joined with `\n`, trailing newline stripped).
- Every check below ran under `trace-inputs.py` (receipts `.ufo/evidence/round-17/coldread/traces/RR3/1..9.json`, all `exit 0`, `rev` field = `0ff273448…`).

## Section 1155–1163 — `## The cadence's first scheduled tick, and the service's limits (round 9, measured)` — record

Claims checked:

1. `[U]` anchor — receipt 2: `sed -n '1019p' SKILL.md` → `no lane acting stays [U].` The `:1019` anchor resolves to exactly the sentence the section cites ("whether a fleet driver would ever invoke it with no lane acting stays [U] (`:1019`)"). Holds.
2. "the tick is the round-8 section's command, executed and pasted below" — receipt 3: `sed -n '1164,1178p' SKILL.md` shows the pasted round-9 output ("Pin read at the round-9 boundary, **2026-10-14T20:00:34Z** …", six-row table, "4 × `current` · 2 × `stale` · 0 × `drift`; tool **held** at `cf41efaa…`"). The recorded pins/revisions in that paste match the harness constants (`tools/mutate-and-run.sh:592-605`: `PIN_JS=83016d45…/REV_JS=175de6ba…` through `PIN_CLAIMS=e9a21b44…/REV_CLAIMS=175de6ba…`). Holds.
3. "Round 8 landed the cadence as policy + a demonstrated pin read" — the round-8 section (named by this claim) carries the reading-rule table and an executed instance at `2026-10-14T19:15:14Z`. Holds on the page.
4. Re-execution of the round-8 command (the pin read per its stated rules) as a fresh tick — receipt 1, exit 0, at `2026-10-20T18:20:54Z`:
   - `js-kimi-census`: stale (`084951be`-style move: recorded pin `83016d45` ≠ tip blob `5e8d5913`, recorded rev ancestor of `refs/heads/master`, 0 porcelain lines)
   - `bash-tsukuroi-census`: stale (pin `084951be` ≠ tip blob `d17d32a3`)
   - `bash-mado-verify`: **stale + drift** (pin `d7edaab4` ≠ tip blob `1036d100`; live file `071d39d9` ≠ tip blob; 2 porcelain lines)
   - `bash-surface-census`, `kagi-checklist-run`, `kumitate-claims-check`: current (recorded pin == branch-tip blob)
   - Tool pin now `fb6d86d5…` (`sha256sum tools/mutate-and-run.sh`) — the harness has moved since the paste's `cf41efaa…`, i.e. the tool would read `moved` today.
   - This matches the page's own contract: "a timestamped observation, re-run at the next boundary — never carried as a standing claim". Today's cells differing from the 2026-10-14 paste is the mechanism working, not a wrong expectation. One correction to my own first pass (recorded for honesty): my shell one-liner's inline labeling printed `mixed` for rows where the recorded rev is an ancestor but the pin still equals the tip blob; the page's `current` rule is pin == branch-tip blob, under which the correct readings are the 3 current / 2 stale / 1 stale+drift above. My labeling bug, not a page defect.

No wrong expectations found. Verdict: **verified-record**.

## Section 1246–1271 — `### The service's limits — what tameshi refuses to mutation-test` — record (+ its re-resolve instruction)

The section instructs: "a reader on a differing revision re-resolves rather than trusts." I re-resolved every anchor on my rev's bytes (receipts 4–8, all exit 0):

- (b) `:813-817` → "must exercise the copy it is handed …, print its own executed count and verdict …, and read no live path"; `:840-844` → "`asserted` **before any suite run** … Any spec failure is `MUTATE: SETUP (<reason>)`, exit 2 — no headline" + "Control first … a red control exits 2". Supports row b.
- (c) `:823-825` → "Nothing else. The service never edits, repairs or re-pins the gate; a needed change is a recommendation to the owner". Supports row c.
- (f) `:879-881` → "**Sensitivity, not truth** — a sweep measures what the suite can detect, never whether the gate's verdicts are right". Supports row f.
- (a) `service-optin-protocol.md:26-30` → the queue "is an offer, not a schedule … a round with no opt-in records the no-opt-in line as its complete outcome"; `fleet-suite-census.md:277-286` → the ordered queue projection + "Scope of the offer, stated so it is not over-claimed". Support row a.
- (d) `service-optin-protocol.md:129-132` → "**No live substrate read.** … a PATH-level stub, never the session". Supports row d.
- (h) `service-optin-protocol.md:267-269` → "**U4** — a harness that adjudicates by exit code alone cannot kill the exit-flatten family; a stdout-reading harness is a named future, not a measurement". Supports row h.
- (j) `service-optin-protocol.md:86-91` → scratch namespace per lane; "≥37 foreign … directories, kept exactly its own 8". Supports row j.
- (e) `PROVINCE.md:14-18`,`:20` → "Never edits a sibling's gate code (read-only probes …). Credential material (→ kagi), endpoint health (→ kama)." / "**Out of province → report, never absorb.**" Supports row e.
- (g) `fleet-kill-rate-ledger.md:220` → "**U2** — coordinated multi-edit rewrites unmeasured everywhere (matrix §7)." Supports row g.
- (i) `fleet-kill-rate-ledger.md:35-36` → "A post-hardening re-run of the same spec is a **directed repair**, not an independent rate; it is recorded as such." Supports row i.

Detail-of-record comparison — receipt 9: `cat corpus/knowledge/service-limits.md` shows the same rows a–j as the page's compact table, with the verbatim anchor quotes (§2), the trigger column (§1 "Trigger at intake"), and the intake-precondition check (§3: the re-pin rule found present at `service-optin-protocol.md:59-63`, "No errata needed"). No substantive divergence between the page rendering and the note. Two cosmetic citation-range differences, neither a divergence in meaning: page row (e) cites `PROVINCE.md:14-18` where the note cites `:16-18` (the page's coarser range still contains the quoted lines); page row (a) cites `fleet-suite-census.md:277-286` where the note cites `:269-275` + `:277` (both name the same standing offer). Under the note's own rule ("row ids a–j, same refusals") these agree.

Verdict: **verified-record**.

## Commands, exits

| # | command (under trace-inputs.py, `--root $C`) | exit | receipt |
|---|---|---|---|
| 1 | `bash -c '<six-case pin-read tick per the round-8 rules; sha256sum tools/mutate-and-run.sh; date -u>'` | 0 | `.ufo/evidence/round-17/coldread/traces/RR3/1.json` |
| 2 | `sed -n '1019p' SKILL.md` | 0 | `…/RR3/2.json` |
| 3 | `sed -n '1164,1178p' SKILL.md` | 0 | `…/RR3/3.json` |
| 4 | `sed -n '813,817p;823,825p;840,844p;879,881p' SKILL.md` | 0 | `…/RR3/4.json` |
| 5 | `sed -n '26,30p;86,91p;129,132p;267,269p' corpus/knowledge/service-optin-protocol.md` | 0 | `…/RR3/5.json` |
| 6 | `sed -n '14,18p;20p' PROVINCE.md` | 0 | `…/RR3/6.json` |
| 7 | `sed -n '35,36p;220p' corpus/knowledge/fleet-kill-rate-ledger.md` | 0 | `…/RR3/7.json` |
| 8 | `sed -n '277,286p;288,291p' corpus/knowledge/fleet-suite-census.md` | 0 | `…/RR3/8.json` |
| 9 | `cat corpus/knowledge/service-limits.md` | 0 | `…/RR3/9.json` |

Residual risk: the tick re-run reads the four sibling repos' live branch tips (read-only git), so today's readings are host/time-dependent by design; the section's claims are about the 2026-10-14 tick, which I verified by presence, shape and harness-constant agreement, not by reproduction.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "RR3",
  "skill_sha256": "de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc",
  "read_rev": "0ff273448ac4e62893c9b28a4cea7c580712df19",
  "sections": [
    {
      "start": 1155,
      "heading": "## The cadence's first scheduled tick, and the service's limits (round 9, measured)",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "bash -c '<six-case pin-read tick per round-8 rules; sha256sum tools/mutate-and-run.sh; date -u>' (exit 0)",
        "sed -n '1019p' SKILL.md (exit 0)",
        "sed -n '1164,1178p' SKILL.md (exit 0)"
      ],
      "opened": [
        "SKILL.md:1155-1163 (assigned)",
        "SKILL.md:1019 (named anchor :1019)",
        "SKILL.md:1024-1050 (round-8 section's command/rules, named by the claim)",
        "SKILL.md:1164-1178 (pasted below, named by the claim)",
        "tools/mutate-and-run.sh:179-215,589-605 (named by the pasted record)"
      ],
      "inputs": {
        "tools/mutate-and-run.sh": "fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a"
      },
      "external_inputs": {
        "/tmp/tameshi-r17w3-RR3-DeW0UG/fleet/kumitate-shokunin/scripts/kimi-census.mjs": "5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0",
        "/tmp/tameshi-r17w3-RR3-DeW0UG/fleet/kagi-shokunin/corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
        "/tmp/tameshi-r17w3-RR3-DeW0UG/fleet/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e",
        "/tmp/tameshi-r17w3-RR3-DeW0UG/fleet/mado-shokunin/tools/mado-verify.sh": "071d39d99aa94d9e3d0c0a8c9d9e9e98b4bc79b51af0703e4dba774f85f7c75d",
        "/tmp/tameshi-r17w3-RR3-DeW0UG/fleet/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "/tmp/tameshi-r17w3-RR3-DeW0UG/fleet/kumitate-shokunin/scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b"
      },
      "traces": [
        ".ufo/evidence/round-17/coldread/traces/RR3/1.json",
        ".ufo/evidence/round-17/coldread/traces/RR3/2.json",
        ".ufo/evidence/round-17/coldread/traces/RR3/3.json"
      ]
    },
    {
      "start": 1246,
      "heading": "### The service's limits — what tameshi refuses to mutation-test",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "sed -n '813,817p;823,825p;840,844p;879,881p' SKILL.md (exit 0)",
        "sed -n '26,30p;86,91p;129,132p;267,269p' corpus/knowledge/service-optin-protocol.md (exit 0)",
        "sed -n '14,18p;20p' PROVINCE.md (exit 0)",
        "sed -n '35,36p;220p' corpus/knowledge/fleet-kill-rate-ledger.md (exit 0)",
        "sed -n '277,286p;288,291p' corpus/knowledge/fleet-suite-census.md (exit 0)",
        "cat corpus/knowledge/service-limits.md (exit 0)"
      ],
      "opened": [
        "SKILL.md:1246-1271 (assigned)",
        "SKILL.md:813-817,823-825,840-844,879-881 (named in-page anchors)",
        "corpus/knowledge/service-optin-protocol.md:26-30,86-91,129-132,267-269 (named anchors)",
        "PROVINCE.md:14-18,20 (named anchor)",
        "corpus/knowledge/fleet-kill-rate-ledger.md:35-36,220 (named anchors)",
        "corpus/knowledge/fleet-suite-census.md:277-286,288-291 (named anchors)",
        "corpus/knowledge/service-limits.md (named detail-of-record)"
      ],
      "inputs": {
        "corpus/knowledge/service-limits.md": "2b2fd1ab696bcba52e4a9b941ec39e03978b17152a80456dc9843c39f80e6002",
        "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
        "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "ac7f69d928e5ba0fb687821c2a2c0900e1375a8454901a285874735e35c21033",
        "PROVINCE.md": "49715af2b90eb0ea10c1a279a0a7edff9fa62caa4b729557ab43549cb6e04d0d"
      },
      "traces": [
        ".ufo/evidence/round-17/coldread/traces/RR3/4.json",
        ".ufo/evidence/round-17/coldread/traces/RR3/5.json",
        ".ufo/evidence/round-17/coldread/traces/RR3/6.json",
        ".ufo/evidence/round-17/coldread/traces/RR3/7.json",
        ".ufo/evidence/round-17/coldread/traces/RR3/8.json",
        ".ufo/evidence/round-17/coldread/traces/RR3/9.json"
      ]
    }
  ]
}
```
