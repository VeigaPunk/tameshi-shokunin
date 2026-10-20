# Re-open S065 — Python `json` default NaN/Infinity acceptance

Seat: TameshiR18.ReopenS065 (wave 2, FALSIFY). Date: 2026-10-20.
Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Clone: `/tmp/tameshi-r18w2-ReopenS065-1PITAC/fleet/tameshi-shokunin`; `git rev-parse HEAD` printed the read rev (exit 0).
No tools installed or updated.

## Object

- Row: `corpus/SOURCES.md:74` (read rev; file sha256 `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37`).
  Fields: kind `docs`, tier `A`, status `mined`, opened `2026-10-20`, recheck `on-release`,
  used-by `corpus/knowledge/guard-kill-closure.md`.
- Quote under test: `.ufo/waves/round-18/staged/lesson-round-18-gate.md:17` (read rev):
  `"by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values"` at `§Standard Compliance and Interoperability › Infinite and NaN Number Values` (inline code markup removed).
- Page: `https://docs.python.org/3/library/json.html`, fetched 2026-10-20 to `/tmp/tameshi-r18w2-ReopenS065-1PITAC/json.html`, HTTP 200, 115104 bytes, sha256 `c766c45677f370e8c1681a158e26980ea9cc1b41711ae280a095338aa4d7871e`; a second fetch was byte-identical (`cmp` exit 0). Title line 20: `json — JSON encoder and decoder — Python 3.15.0 documentation`.
- Used-by: `corpus/knowledge/guard-kill-closure.md`, sha256 `9312bdebd4e93d427ea32d3db8652f95530237477b49ffecffdf4e4ac49991fb`.

## Checks

### 1. Row presence and shape — pass

- `git show 01d586…:corpus/SOURCES.md | awk 'NR==74'` prints the S065 row above; `awk -F'|' 'NR==74{print NF}'` = 13 (11 columns).
- Contract census (frozen contract `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, "Census" block): malformed rows `0`; duplicate ids none; mined rows with missing `used-by` paths none; all commands exit 0.
- Row is already at `e08271a` (`git show e08271a:corpus/SOURCES.md | grep -c '^| S065'` = 1) and was added by `58e5d53` (2026-10-20 17:20:09 -0300).

### 2. Quote verbatim, word count, anchor — pass

Tag-stripping the `<p>` under `<section id="infinite-and-nan-number-values">` (`json.html:878-880`) yields:

`The RFC does not permit the representation of infinite or NaN number values. Despite that, by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values:`

- `quote in plain` = `True` (Python substring check, exit 0). The quote begins mid-sentence after "Despite that," but is verbatim; no word is altered.
- Word count = **20** (`wc -w` and `awk '{print NF}'` both 20), so ≤25 holds even if `-Infinity` were split.
- Anchor: `json.html:838` `<h2>Standard Compliance and Interoperability` (id `standard-compliance-and-interoperability`); `json.html:877` `<h3>Infinite and NaN Number Values` (id `infinite-and-nan-number-values`). The stated `h2 › h3` path is exact.
- "inline code markup removed" is accurate: `json.html:879-880` wraps `Infinity`, `-Infinity`, `NaN` in `<code class="docutils literal notranslate">`; the quote shows the bare words.
- `json.load() parameter parse_constant`: `json.load` signature `json.html:459`; parameter bullet `json.html:501-504` says the callable receives `'-Infinity'`, `'Infinity'`, or `'NaN'` and "can be used to raise an exception if invalid JSON numbers are encountered"; `json.loads` (`json.html:544-545`) is "Identical to load()". The section itself (`json.html:893-895`) says the deserializer's `parse_constant` can alter the behaviour.

### 3. `teaches` vs the page — pass, one unmarked inference

Clause by clause against the fetched page:

- "json.loads accepts Infinity, -Infinity and NaN by default" — page sentence (`:878-880`) says the module "accepts and outputs" them "by default"; examples `json.loads('-Infinity')` → `-inf` and `json.loads('NaN')` → `nan` (`json.html:886-890`). The row narrows "module accepts and outputs" to the decoder, which is a subset, not an overstatement.
- "as if they were valid JSON number literals" — page says "as if they were valid JSON number literal values".
- "parse_constant is called with each such literal" — page bullet `:501-503` documents the three strings; runtime cross-check on the installed Python 3.14.8 confirmed the hook receives all three: `json.loads('[NaN, Infinity, -Infinity]', parse_constant=…)` saw `['NaN', 'Infinity', '-Infinity']`. The docs are 3.15.0; the runtime check is corroboration only, not proof of the 3.15.0 build.
- "so a registry loader can reject it by name instead of trusting the default" — the mechanism is on-page ("can be used to raise an exception"); "registry loader" is the lane's application and is not marked `[INFERENCE]` (cf. S066 and S069, which mark design inferences). See F3; non-blocking.

The row does **not** repeat the draft's "although RFC 7159 does not permit them", so it does not overstate the page's RFC attribution.

### 4. Tier / kind — pass

Frozen contract `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`:

- line 24: `docs` is an allowed kind;
- lines 26-30: tier **A** = "primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement, the lane's own re-runnable gate output)"; tier is scoped, never global.

`docs.python.org` is the official Python 3.15.0 documentation and is authoritative for the scoped claim (CPython `json` decoder behaviour). `docs` rather than `spec` is correct: the normative JSON grammar row is S066 (RFC 8259). Scope is the decoder behaviour plus `parse_constant`, which matches the cited sentences.

### 5. Used-by path — pass

- `git cat-file -e 01d586…:corpus/knowledge/guard-kill-closure.md` exit 0.
- `git show 01d586…:corpus/knowledge/guard-kill-closure.md | grep -n 'S065'` → lines **1** (`source:` header cites S065 with the same anchor), **3** (recheck instruction to re-open S065–S074), and **57** (the Fact, with the quote and the `parse_constant` anchor).
- Status `mined` is contract-consistent (`mined` = cited by ≥1 path in `used-by`).

### 6. Staged vs landed row — pass

`git show 01d586…:.ufo/waves/round-18/staged/corpus/SOURCES.md | grep '^| S065' | sha256sum` and the same command over `corpus/SOURCES.md` both print `c48d0ed8c2e95aa02cbd2f925b118ce7fc4c20985cdd64894033e8aa67526260`; the installed row is byte-identical to the staged row.

## Receipts (exact commands, exits, key lines)

- `git -C <clone> rev-parse HEAD` → `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (exit 0).
- `git show 01d586…:corpus/SOURCES.md | awk 'NR==74{print NR": "$0}'` → line 74 is the S065 row; `awk -F'|' 'NR==74{print NF}'` → `13`.
- Census: malformed `0`, duplicate ids `(none)`, missing mined used-by `(none)` (exit 0).
- `curl -sSL -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective}' -o json.html https://docs.python.org/3/library/json.html` → `http=200 bytes=115104 url=https://docs.python.org/3/library/json.html` (exit 0).
- `sha256sum json.html` → `c766c45677f370e8c1681a158e26980ea9cc1b41711ae280a095338aa4d7871e`; refetch `cmp` → identical (exit 0).
- `python3` tag-strip + `quote in plain` → `True`; `wc -w quote.txt` → `20`.
- `grep -n` anchors → h2 `838`, h3 `877`, quote `878-880`, parse_constant bullet `501-504`, `json.loads` signature `543-545`, deserializer sentence `894`.
- `git cat-file -e 01d586…:corpus/knowledge/guard-kill-closure.md` → exit 0; `git show … | grep -n 'S065'` → `1`, `3`, `57`.
- Staged vs landed row: both `grep '^| S065' | sha256sum` → `c48d0ed8c2e95aa02cbd2f925b118ce7fc4c20985cdd64894033e8aa67526260`.
- `python3 -c "json.loads(...)"` (3.14.8) → `inf -inf nan`; `[NaN, Infinity, -Infinity]` hook saw `['NaN', 'Infinity', '-Infinity']` (exit 0).

## Findings

- **F1 — minor, false record sentence.** `.ufo/waves/round-18/staged/lesson-round-18-gate.md:62-64` says: "The page cites RFC 7159 for the format but does not state that prohibition." The page **does** state it at `json.html:878`: "The RFC does not permit the representation of infinite or NaN number values." (RFC 7159 is named at `json.html:839`.) The row and Gate quote are unaffected, but the explanatory note is false as written; the honest wording is that the *quoted sentence* does not carry the prohibition, not the page.
- **F2 — minor, Gate quote covers half of `teaches`.** Rule 1 of the frozen contract (lines 36-41) requires the Gate to record a ≤25-word quote "grounding `teaches`". The S065 Gate quote grounds the default-acceptance clause; the `parse_constant` clause has no Gate quote (the row's `anchor` names it and the page supports it at `json.html:501-504`). Non-blocking, but the Gate table alone does not let a reader verify that clause.
- **F3 — minor, unmarked inference.** The trailing "so a registry loader can reject it by name instead of trusting the default" is a lane design consequence. The page supports the capability ("can be used to raise an exception") but says nothing about a registry loader; the lane marks comparable design inferences with `[INFERENCE]` (S066, S069). It does not overstate the page's factual content.
- **F4 — observation, not a defect.** The knowledge entry's inline quote at `guard-kill-closure.md:57` adds code backticks and a trailing ellipsis, so it is not verbatim as printed; it marks truncation and cites S065. The Gate quote under test is separately verbatim.
- **F5 — observation.** The row records no body hash and says "version-coupled; no commit pin". That is honest and the `on-release` cadence fits a `/3/` dev-docs URL; the Gate quote is the drift detector. Historical fetch time cannot be proven from the artifact, but today's live page matches the quote and the row's 3.15.0 title.

## Unresolved

- Whether the page text at the wave-1 fetch instant (2026-10-20, before commit `58e5d53` 17:20 -0300) was identical: not provable from the lane. Two fetches now are byte-identical (`c766c456…`), and the quote matches.
- The 3.15.0 docs' decoder behaviour was cross-checked on Python 3.14.8 only; the documentation statement itself is what the row teaches, and it is on-page.

## Verdict

holds — S065's row, Gate quote (verbatim, 20 words, exact h2›h3 anchor), tier/kind fit, and the cited used-by path (exists, cites S065 at lines 1/3/57) all check out at `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; the only defects are a false explanatory sentence at staged-lesson lines 62-64 (F1) and two non-blocking gate/inference nits (F2, F3), none of which changes the row.
