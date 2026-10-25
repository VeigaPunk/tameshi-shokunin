# Scout — Stryker "Equivalent mutants" page (S159, judged on freshness)

Seat: L1Tameshi43.ScoutStrykerEquiv · Round 43, wave 1 · Access date **2026-10-25**
Milestone: S159 (Stryker equivalent mutants) · Assimilation: none (shokuknow untouched)

## 1. Fetch result (observed)

Command (scratch dir named by the item, so it is retained):

```
mkdir -p /tmp/tameshi-r43-ScoutStrykerEquiv- && cd /tmp/tameshi-r43-ScoutStrykerEquiv- \
  && curl -fsSL -o equiv.html \
     https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/
```

| field | value |
|---|---|
| HTTP status | `200` (HTTP/2, `server: cloudflare`) |
| bytes (`size_download` / `wc -c`) | **38687** |
| sha256 | **`79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`** |
| lines | 24 (article body spans lines 4–24; prose lines 5–23) |
| `<title>` | **`Equivalent mutants \| Stryker Mutator`** — raw `<title data-rh=true>Equivalent mutants \| Stryker Mutator</title>`, line 1, byte 280 |
| generator | `<meta name=generator content="Docusaurus v3.10.2">` (line 1) |
| doc id | `docs-doc-id-mutation-testing-elements/equivalent-mutants` (line 1) |

Freshness evidence:

```
$ curl -sS -D headers.txt -o /dev/null https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/
HTTP/2 200
date: Sun, 25 Oct 2026 10:52:48 GMT
server: cloudflare
last-modified: Sat, 24 Oct 2026 15:08:38 GMT
cache-control: max-age=600
cf-cache-status: DYNAMIC
```

- `last-modified` is **2026-10-24T15:08:38Z**, i.e. under 20 h before the access at **2026-10-25T10:52:48Z**; `cf-cache-status: DYNAMIC` means Cloudflare served a regenerated object, not a stored copy.
- A second full download was byte-identical: both files hashed `79f6501a…4079ce`, `cmp -s` → `IDENTICAL_REDOWNLOAD` (equivalent content, so the digest is stable within the access window).
- No `<time>`/`datetime` element and no "Last updated" widget exists in the page body — the only machine-readable date is the HTTP `last-modified`.

## 2. Located anchors (HTML line numbers, `equiv.html`)

Line numbering is `\n`-split of the 24-line document; byte offsets are from the file start.

| line | byte | content |
|---|---|---|
| 13 | — | setup: `But what if we have both values the same? Let's say: 3, 3` |
| **14** | 27257 (first `pre`) | code block: `max = 3;` / `min = 3;` / `if (3 >= 3) {` / `a.number *= 10 ** 0;` / `} else {` / `b.number *= 10 ** 0;` / `}` |
| **15** | 30616 | `<p>Notice that 10 ** 0 = 1, so even if we change <code>>=</code> to <code>&lt;=</code> and even <code>&lt;</code> or <code>&gt;</code> we will get the same output each time!</p>` |
| **16** | 30796 / 30820 / 30908 | `<p>It is called <em>equivalent mutant</em>. There is no definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored.</p>` |
| 17 | 30963 | `<p>For now, the only solution is by finding these by hand, which is time consuming and try to rewrite the code so it won't occur, or accept that you won't make 100%.</p>` |
| 19–23 | — | second example: ``number1 += 0  // can be `-= 0` or `*= 1` `/= 1` `` (line 19); BigInt `a = a <= 0n ? -a : a;` (line 22) → `will produce another equivalent mutant.` (line 23) |

Uniqueness, stated per quoting form: **Q1** and the three prose fragments below are contiguous in the raw bytes — `src.count(...)` = 1 for "There is no definitive way for Stryker to find and ignore them." (byte 30820), `10 ** 0 = 1` (byte 30616), "no way yet to mark them to be ignored." (byte 30908) and "the only solution is by finding these by hand" (byte 30963). **Q2** is *not* contiguous in raw bytes (`<code>` tags wrap `>=`, `<=`, `<`, `>`; raw count = 0), but is contiguous and occurs exactly once after tag stripping (count = 1) — the tag-stripped text is what the quote reproduces. The string `equivalent mutant` occurs twice: line 16 (byte 30796) and line 23.

### The 10 ** 0 example

It is the third and deciding code block (`equiv.html:14`), reached from the 4/2 case (`equiv.html:10`, `10 ** 2`) via `equiv.html:13`. Rendered code text (tags stripped, `<br/>` → newline, no injected spaces):

```
max = 3;
min = 3;
if (3 >= 3) {
  a.number *= 10 ** 0;
} else {
  b.number *= 10 ** 0;
}
```

Its explanation is prose on `equiv.html:15`: with `max == min == 3`, `10 ** 0 = 1`, so `>=`, `<=`, `<` and `>` all leave the observable output unchanged. (`[INFERENCE]` The page's next line, `equiv.html:16`, names that outcome *equivalent mutant*; the page itself calls the output "the same", and does not use the phrase "behaviour change".)

## 3. Two located quotes (≤25 words, access date 2026-10-25)

**Q1 — `equiv.html:16` (byte 30820), 12 words:**
> "There is no definitive way for Stryker to find and ignore them."

Raw context on that line: `<p>It is called <em>equivalent mutant</em>. ` + Q1 + ` There is currently also no way yet to mark them to be ignored.</p>`

**Q2 — `equiv.html:15` (byte 30616), 20 words:**
> "even if we change >= to <= and even < or > we will get the same output each time!"

Verbatim continuation of the sentence whose opening clause is `Notice that 10 ** 0 = 1, so` (`<code>` markup around `>=`, `<=`, `<`, `>` only). Word counts verified programmatically: `len(q.split())` → 12 and 20.

Supplementary fragment, same page, 9 words — `equiv.html:17` (byte 30963):
> "the only solution is by finding these by hand"

## 4. Which sentence grounds the lane rule

**Q1 — `equiv.html:16`, "There is no definitive way for Stryker to find and ignore them."** — is the grounding sentence.

Reason: it states that the mutation tool cannot decide equivalence, so a non-killing tool result carries no classification. A survivor observed as *not killed* must therefore be classified by an explicit, tool-external rule (the round-43 `K/D/E/U` rule: `E` reserved for an explicit equivalence argument, `D` for the declared dead-code construct, `U` for a reachable-input survivor). The tool verdict "survived" is the *input* to classification, never the classification itself.

Two same-page sentences make that reading unavoidable rather than merely suggestive:
- `equiv.html:16`, "There is currently also no way yet to mark them to be ignored." — the tool cannot even take a human-supplied equivalence label, so no tool-side state can stand in for the lane's classification.
- `equiv.html:17`, Q3, "the only solution is by finding these by hand" — the page's own remedy is manual identification, i.e. classification is authored, not queried.

Scope note (`[INFERENCE]`): the page speaks about **Stryker** (JS/C#/Scala), not PIT. It grounds "no tool verdict can decide equivalence" as a general mutation-testing claim; it does not, by itself, assert anything about PIT's `equivalent` mutant status. That is sufficient for the lane rule (which forbids treating a tool verdict as a classification) and not sufficient to claim any PIT-specific equivalence detection.

## 5. Upstream source cross-check (freshness corroboration)

The rendered page's "Edit this page" link points at
`https://github.com/stryker-mutator/mutation-testing-elements/edit/master/docs/equivalent-mutants.md`.
Fetching the raw markdown (read-only) confirms verbatim parity and that the site build is current:

```
$ curl -fsSL -o source.md https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/docs/equivalent-mutants.md
code=200 bytes=2057
39aba4bc885bb228f03fc40a8294858a4fed6df61716e306060ced5a44422328  source.md
44:  a.number *= 10 ** 0;
46:  b.number *= 10 ** 0;
52:It is called _equivalent mutant_. There is no definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored.
54:For now, the only solution is by finding these by hand, which is time consuming and try to rewrite the code so it won't occur, or accept that you won't make 100%.
```

Source → render mapping: source `:52` → `equiv.html:16`; source `:54` → `equiv.html:17`; source `:44,:46` → code block `equiv.html:14`; source `:50` (`Notice that 10 \*\* 0 = 1, …`) → `equiv.html:15` — note the markdown escapes the asterisks (`\*\*`) while the rendered HTML carries the literal `10 ** 0`, so a grep for `10 ** 0` in the markdown misses it and matches only the code block.

## 6. Reproduction

```
cd /tmp/tameshi-r43-ScoutStrykerEquiv-
sha256sum equiv.html && wc -c equiv.html        # 79f6501a…4079ce / 38687
sed -n '15p;16p;17p' equiv.html                 # the three prose anchors
grep -n -o '<title[^<]*</title>' equiv.html     # Equivalent mutants | Stryker Mutator
```

Artifacts retained (dir named by the item, so not deleted): `/tmp/tameshi-r43-ScoutStrykerEquiv-/equiv.html`, `source.md`, `headers.txt`.

## 7. Unknowns / limits

- No in-page publication or revision date exists; only HTTP `last-modified` (2026-10-24T15:08:38Z). A Cloudflare-served regeneration date is not a proof of when the prose last changed.
- The page has a single hard sentence on tool capability; it names no issue tracker entry or version, so the claim cannot be dated beyond this snapshot.
- Tooling: no installs or upgrades were performed (none needed); `curl`, `sha256sum`, `python3`, `grep` were already present.
