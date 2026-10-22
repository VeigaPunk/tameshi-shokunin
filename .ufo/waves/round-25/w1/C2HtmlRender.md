# C2HtmlRender — emitted MTE reports load in the official mutation-testing-elements web component

Seat: TameshiR25.C2HtmlRender (executor, leaf). Judged on: coverage.
Frozen contract: `.ufo/evidence/round-25/contract.json` (lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df, base 1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5).
Mode: private clone at the pinned lane revision; nothing run inside the lane; no git/jj write commands; no production file edited.

## Verdict

1. **Every one of the 8 emitted reports loads and renders in the official `mutation-testing-elements` 3.9.0 web component, headlessly, with zero console or page errors, via both documented bindings (`src` attribute and `report` property) and via the documented unpkg CDN path.** The element's own computed metrics (its bundled `mutation-testing-metrics`) equal the vendored official metrics for all 8 legs — an independent cross-check of the tool's score semantics. The file view renders the full pinned source with one inline mutant marker per recorded defect (unique marker ids == per-leg mutant count: 15 for bash-checklist-run, 10 for each other leg), with Killed/Survived statuses colored in the source.
2. **The element is NOT a schema validator.** Doctored reports that fail the official schema (bogus status, missing `thresholds`, zero-line location, missing `framework`, missing `source`) load without error; a bogus status is silently dropped *from the tally* (totalMutants 10→9, score 50→44.44) with no error surface. The schema gate in `tools/mte-interop.py` is therefore load-bearing; the HTML consumer must not be relied on to catch invalid reports.
3. **No CLI exists in the package (npm `bin` empty); the documented consumer path is the web component**, which is what was exercised. The dist served by unpkg `/mutation-testing-elements` is byte-identical to the npm tarball dist (sha256 751fb010…) and resolves to the 3.9.0 build — the same version as the vendored schema/metrics pins.

## Evidence

### 1. Emit (the mandated counter, in the private clone)

```
$ cd /tmp/C2HtmlRender-r25   # clone at c9ff09f
$ uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check \
      --fleet-root /home/vgpnk/Projects/shokunin --emit /tmp/C2HtmlRender-r25/.ufo/evidence/round-25/mte-emit
MTE_LEG bash-checklist-run: CONFORMS (schema=ok official_score=46.666666666666664 … recorded-killed=7 recorded_defects=15)
MTE_LEG bash-mado-verify: CONFORMS (schema=ok official_score=40 … recorded-killed=4 recorded_defects=10)
MTE_LEG bash-surface-census: CONFORMS (schema=ok official_score=80 … recorded-killed=8 recorded_defects=10)
MTE_LEG bash-tsukuroi-census: CONFORMS (schema=ok official_score=60 … recorded-killed=6 recorded_defects=10)
MTE_LEG js-claims-check: CONFORMS (schema=ok official_score=70 … recorded-killed=7 recorded_defects=10)
MTE_LEG js-kimi-census: CONFORMS (schema=ok official_score=80 … recorded-killed=8 recorded_defects=10)
MTE_LEG js-round-gate: CONFORMS (schema=ok official_score=50 … recorded-killed=5 recorded_defects=10)
MTE_LEG js-sources-check: CONFORMS (schema=ok official_score=50 … recorded-killed=5 recorded_defects=10)
MTE_INTEROP: PASS legs_conforming=8/8
```

Exit 0; wall 140.1 s. Emitted: 8 `.mte.json` reports + `official-metrics.json`. The tool's own docstring explicitly disclaims HTML-element validation ("It does not … validate the HTML report elements"), which is the gap this seat covers.

### 2. Official elements package: version, integrity, documented path

```
$ npm view mutation-testing-elements@3.9.0 version dist.integrity
3.9.0 / sha512-3G4GhBO8Wc/ZrqOJ5uT8AbM1h/ew9kfX0MIlpy59gWu/amMZyKH3TreKAOMwwXNibhZMOL7A3n5nFvhYWLdtYQ==
$ npm view mutation-testing-elements@3.9.0 bin   # empty → no CLI
```

README (package README.md) documents exactly two consumption paths, both exercised:
- `<mutation-test-report-app src="mutation-report.json">` (script tag → `dist/mutation-test-elements.js`);
- property binding: `document.getElementsByTagName('mutation-test-report-app').item(0).report = {...}`.

Downloaded tarball sha512 == registry `dist.integrity` (verified). `dist/mutation-test-elements.js` is the IIFE browser build (default `browser` entry), size 238,114 bytes, contains the `mutation-testing-metrics` logic (`mutationScoreBasedOnCoveredCode`, `totalDetected`), i.e. it computes metrics itself — independent of the vendored tarball used by the tool.

### 3. Headless render check (Chromium 154.0.8037.97 via puppeteer-core; harness `/tmp/C2HtmlRender-r25/scratch/html/`)

Load page with `<mutation-test-report-app id="app">`, set `src` (documented attribute path), wait for `rootModel.systemUnderTestMetrics`, then:
- read `elementMetrics` from the element's own model;
- open the file view by clicking the file anchor in `mte-file-picker` (documented interaction);
- count inline mutant markers in the source (`.mutant` elements and unique marker ids);
- collect console/page errors.

**All 8 legs — element score == official metrics score (exact), zero errors:**

```
leg              element_score official_score killed valid mutants fileView markers_rendered
bash-checklist-run 46.666666666666664 46.666666666666664  7/15 15  yes  15 unique ids
bash-mado-verify   40                  40                  4/10 10  yes  10 unique ids
bash-surface-census 80                  80                  8/10 10  yes  10 unique ids
bash-tsukuroi-census 60                 60                  6/10 10  yes  10 unique ids
js-claims-check     70                  70                  7/10 10  yes  10 unique ids
js-kimi-census      80                  80                  8/10 10  yes  10 unique ids
js-round-gate       50                  50                  5/10 10  yes  10 unique ids
js-sources-check    50                  50                  5/10 10  yes  10 unique ids
```

Console/page errors: 0 across all runs (the only 404s ever logged were `/favicon.ico`, served 204 thereafter). For js-round-gate the file view renders 73,600 chars of source text; the status bar shows `detected=5, no-coverage=0, pending=0` matching the official counts. Property-binding path on the same report: identical metrics (`mutationScore=50, killed=5, survived=5, totalValid=10, totalMutants=10`), `errorMessage=null`.

Screenshots captured for evidence: `/tmp/C2HtmlRender-r25/scratch/html/shot-js-round-gate.png`, `shot-bash-checklist-run.png` (shell source renders too).

### 4. Documented CDN path

`npm`-documented `https://www.unpkg.com/mutation-testing-elements` resolves (302 → 200) to `mutation-testing-elements@3.9.0/dist/mutation-test-elements.js`, byte-identical to the tarball dist (sha256 `751fb010242b0b44e32d84fe7fe0b9ff1da182823b94f59f5c52b001fcfc163b` both). A page loading only the CDN script + `src="./js-round-gate.mte.json"` renders the same metrics (`mutationScore=50, killed=5, survived=5, totalValid=10, totalMutants=10`), `errorMessage=null`, no errors.

### 5. Negative controls — the element is schema-lenient (coverage finding)

Doctored variants of `js-round-gate.mte.json`, each fed through the same headless page:

| doctored report | official schema verdict (tool) | element behavior | element metrics |
|---|---|---|---|
| status `"Bogus"` | invalid (not in enum) | loads, **silently drops the mutant** | totalMutants 10→9, killed 4, survived 5, score 44.44 |
| `thresholds` removed | invalid (required) | loads, no error | unchanged (50) |
| location line 0 | invalid (min 1) | loads, no error | unchanged (50) |
| `framework` removed | invalid (required) | loads, no error | unchanged (50) |
| `source` removed | invalid (required) | loads, no error | unchanged (50) |
| status `"RuntimeError"` | valid | loads; counted invalid | totalInvalid 1, totalValid 9, totalMutants 10, score 44.44 |
| status `"NoCoverage"` | valid | loads; counted undetected | totalValid 10, survived 5, noCoverage 1, score 40 |

Since the element accepts schema-invalid reports (including a bogus status that silently changes the score), the schema conformance enforced by `tools/mte-interop.py` cannot be replaced by the HTML consumer; the two checks are complementary layers, and the tool's schema gate is the authoritative one.

## Risks and notes

1. The element's own mutationScore is computed by its bundled metrics library, which matched the vendored official metrics on all 8 legs; that adds an independent confirmation of score semantics but is not a substitute for the tool's schema + ledger checks (covered by C2LiveCheck/C2Integrity seats).
2. This seat is a verification witness for the already-shipped `tools/mte-interop.py` (frozen rev c9ff09f, sha256 311448d9…). The lane working tree carries an uncommitted newer tool (sha256 8c24255c… per the C2LiveCheck seat); this report covers the pinned tool's emitted artifacts. If the newer tool is integrated, re-running this HTML check on its emits is cheap (harness at `/tmp/C2HtmlRender-r25/scratch/html/`).
3. Blockers: none. All mandated actions ran to completion in the private clone.

## Tooling

- Installed: `puppeteer-core@23.11.1` via `npm install` into `/tmp/.../scratch` (official channel; package tarball fetched from registry.npmjs.org). No pacman transaction, no `uv tool install`, no service touched.
- Used as-is: system Chromium 154.0.8037.97 at `/usr/bin/chromium`; node v24.21.0; `mutation-testing-elements@3.9.0` (npm tarball + unpkg CDN).

## Files

- Written: `.ufo/waves/round-25/w1/C2HtmlRender.md` (this report) — the only file this seat created.
- Scratch (outside the repo, disposable): `/tmp/C2HtmlRender-r25` (clone at c9ff09f), `/tmp/C2HtmlRender-r25/.ufo/evidence/round-25/mte-emit/` (emitted reports), `/tmp/C2HtmlRender-r25/scratch/html/` (harnesses `check.mjs`, `alllegs.mjs`, `deep4.mjs`, `mutcount.mjs`, `neg.mjs`, `propbind.mjs`, `cdn.mjs`; screenshots; `all-legs.json`), `/tmp/C2HtmlRender-r25/scratch/mte/` (npm tarball + package).
