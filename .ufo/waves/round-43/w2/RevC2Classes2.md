# RevC2Classes2 — m11/m12/m13 class sentences vs implementation (post-A6 re-check)

Seat: L1Tameshi43.RevC2Classes2 (wave-2 falsify, calibration). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only; this report is my only lane write). Scratch: `/tmp/tameshi-r43-w2-RevC2Classes2/` (`git clone --shared`, deleted on return).

## What was checked

Contract sentences (`.ufo/evidence/round-43/contract.json`, `claims.C2.classes`):

- m11: "every 40-hex object cited by those records resolves in the lane (object existence, not commit-only)"
- m12: "the newest '## Round N' SCORECARD block carries the field '**Planned (round N+1):**' (a prose mention is not the field)"
- m13: "the newest standing sources-registry row's backticked counting command names the census-valid 0-3-space pattern, and an indented-row mirror proves the difference (column0 = N-1, census-valid = N)"

## Counter-version note

Three counter versions exist; m11/m12/m13 logic is identical in all. I verified the pinned-A6 bytes (`97609511…`, the sha `claims.C2.counter_sha256` names) and the in-flight worktree version (`ab76cbd3…`, m10-rewrite by L1); the records-commit version (`52961c37…`) shares m11/m13 byte-identically and differs in m12 only by lacking the A10 tail check (its `find`/`in` semantics — the divergence driver — are identical). All end-to-end evidence below uses the pinned-A6 counter run against scratch commits; the in-flight counter was also rerun over the same matrix and produced identical m-fields.

**Method:** `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r43-w2-RevC2Classes2/lane`, checkout `3aee2c07…` (freeze of record), apply one constructed edit per scratch commit, run the counter with `--rev <scratch commit> --freeze 3aee2c07…`. Baseline at freeze: `m11=0 m12=0 m13=0` (`m7=5 m8=3` are pre-existing records debt at the freeze — the deciding records commit is `c5335c70`).

## Findings by severity

### F-m11-1 (medium): `HEX40` silently drops cited 40-hex in colon-prefixed and uppercase forms

**Implementing lines:** `measure.py:83` `HEX40 = re.compile(r'(?<![0-9a-f:])[0-9a-f]{40}(?![0-9a-f])')`; `m11_revisions` at `measure.py:317-330` (`git cat-file -e` only for extracted tokens).

**Divergence (accepts what the sentence rejects).** The sentence covers "every 40-hex object cited"; the extractor's `(?<![0-9a-f:])` lookbehind excludes a token immediately preceded by `:`, and `[0-9a-f]` is lowercase-only. `git` resolves uppercase object names (verified: `git cat-file -e 487B8F0DA89FA0E2B8BEA6930068ACCBF36E70A9` → exit 0), so both are live citation spellings a record can carry.

**Constructed input (end-to-end, scratch commit):** append to `corpus/lessons/round-43.md`:

```
Cited at commit:0000000000000000000000000000000000000001 (colon form).
Cited at 0123456789ABCDEF0123456789ABCDEF01234567 (uppercase form).
```

Counter output: `m11=0` (both unresolvable ids invisible). Sentence: `m11=2`. Reproduced on both counter versions (`m11=0` on branch `A_m11_colon_and_upper`).

### F-m11-2 (medium): `HEX40` flags a 40-hex URL path segment that is not an object citation

**Same lines.** Direction reversed: implementation rejects what the sentence accepts.


**Constructed input:** append to `corpus/lessons/round-43.md`:

```
Source page https://example.test/commit/0123456789abcdef0123456789abcdef01234567 was read.
```

Counter output: `m11=1` (`cat-file -e` fails on the URL fragment). The sentence requires resolution of cited *objects*; a URL path segment is not one. This is the more likely live shape — records routinely cite `github.com/…/commit/<40hex>` URLs (no such cite exists in the current records, verified below). Branch `B_m11_url_not_a_cite`.

### F-m12-1 (medium): the field check is a substring `find`, so a prose mention *of the field form itself* passes

**Implementing lines:** `measure.py:124-129` `newest_round_block` (block = `## Round N` header to EOF); `m12_planned` `measure.py:139-147` (`index = block_text.find(wanted)`; non-empty tail after the match). The sentence's parenthetical — "(a prose mention is not the field)" — rejects a prose mention that happens to embed the bolded token; `find` cannot distinguish the field-as-label from the token-as-text.

**Constructed input A (negation):** replace the `**Planned (round 44):**` line's first segment with:

```
This block carries no **Planned (round 44):** field; the plan is in LOG.md.
```

Counter: `m12=0` (non-empty tail after the match). Sentence: `m12=1` — the block carries no `planned` field. Branch `C_m12_negation_field`. Same result for the token inside `<!-- … -->` or a fenced code block (verified at unit level: `m12_planned` returns `[]` on both).

**Constructed input B (block boundary):** delete the planned paragraph and append at file end:

```
## Standing

**Planned (round 44):** stale text
```

`newest_round_block` returns `scorcard_text[last.start():]` — to EOF — so the field in the `## Standing` section is read as part of the round-43 block. Counter: `m12=0`. Sentence: `m12=1` (the field is not *in* the block). Branch `D_m12_field_below_section`. Latent today: no `##` section follows the newest round block at `c5335c70`.

### F-m12-3 (low, deciding-counter version only): the records-commit counter lacks the "names nothing" and contract-round checks

At the records commit `c5335c70` the pinned counter is `52961c37…`, whose `m12_planned` is `hits = [] if wanted in block_text else [wanted]` — no `names nothing` tail check and no `newest block is round N` contract-round check (both are A10 additions, verified absent via `git show c5335c70:…`). Constructed input: `## Round 43\n\n**Planned (round 44):**\n\nmore\n` → `m12=0` on that counter, while the sentence requires the field to *declare* the next round's planned claims. Latent: the real field's tail is non-empty.

### F-m13-1 (medium): `'0,3' in span` accepts non-census patterns; the `grep` need not be the counting command

**Implementing lines:** `measure.py:194-198` — `commands = [span for span in re.findall(r'`([^`]*)`', newest) if 'grep' in span]`; `elif not any('0,3' in span for span in commands): hits.append('standing command is column-zero only')`. Two escapes from "names the census-valid 0-3-space pattern":

- `0,3` substring, not the pattern. Constructed input (end-to-end): change the standing cell to `grep -cE '^ {0,30}\| S[0-9]{3} \|' corpus/SOURCES.md` (counts rows with 4–30 leading spaces the census ignores → not the census-valid pattern) → `m13=0` (branch `E2_m13_range_0_30`). Or `grep -cE '^ {0,3}' corpus/SOURCES.md` (counts every indented line, 456 not 114 — the "re-derivable count" is wrong while the class is clean) → `m13=0` (branch `E_m13_bare_0_3`).
- `grep` in *any* backticked span of the row, not the command cell. Constructed input: counting command = `awk -F'|' '/^\| S[0-9]{3} \|/{n++}END{print n}'` (column-zero) while another cell carries `` `grep -cE '^ {0,3}' other/doc` `` → `m13=0` (branch `E3_m13_grep_other_cell`).

### F-m13-2 (medium): `line.startswith('| sources-registry |')` rejects legal rows and silently re-points "newest" — both directions

**Implementing lines:** `measure.py:151-156` `standing_registry_rows`; `measure.py:189` `newest = standing[-1]`.

- `|  sources-registry  |` (two spaces — a valid table row carrying the census-valid command) → the row is skipped, `standing` drops to the *previous* row (round-42, column-zero command): `m13=1`, plus a collateral `m6=1` because m6's `row_count_claim` now reads that older row's `113 rows at round 42` (branch `F_m13_row_spacing`). False hit produced by formatting, not by the command.
- Masking variant: newest row indented one space *with a column-zero command*, while an older row is upgraded to census-valid → the skipped row is no longer "newest" and the counter grades the upgraded older row: `m13=0`. Sentence reads the true newest row → `m13=1` (branch `F2_mask`). The strict prefix *hides* a defect rather than flagging the row.

The census (fleet `scripts/sources-census.sh`, `CORPUS.md:152`) accepts 0–3 leading spaces on table rows; the counter's own registry parser (`rows()`, `measure.py:~100`) tolerates them. The standing-row detector is the only strict-format reader.

### F-m13-3 (low): the mirror probe is built from the shipped registry, so a legal indented row produces a false hit

**Implementing lines:** `measure.py:174-181` `indent_mirror` (indents the first column-zero row of the live `corpus/SOURCES.md`); `measure.py:199-202` requires `valid == column0 + 1`.

With `k` pre-indented rows, the built mirror yields `column0 = N-k-1, valid = N`; the `+1` invariant holds only for `k = 0`. Constructed input: indent any one registry row by two spaces (explicitly census-valid — the census accepts 0–3 spaces) → `m13=1` reporting `indent probe not load-bearing (column0=112 valid=114)` even though the standing command names the census pattern and the sentence's mirror could be built on a column-zero copy (branch `G_m13_legal_indent`). The class couples pass/fail to the registry's current indentation convention. Latent: the registry at `c5335c70` has zero indented rows.

## Live status at the records commit `c5335c70` (checked by reading blobs; no counter run)

All divergences are **latent** at the deciding rev: `corpus/SOURCES.md` has zero indented rows; the record set carries no colon-prefixed or uppercase 40-hex citations and no 40-hex URL segments; the newest standing row is a literal column-zero `| sources-registry |` row whose command is `grep -cE '^ {0,3}\| S[0-9]{3} \|'`; the `**Planned (round 44):**` field stands alone on its line inside the round-43 block. So the deciding `m11=m12=m13=0` is not masked by these findings today — each is a reproducible escape hatch, not a current false verdict.

## Residual risk / verification gaps

- The `m6` collateral in F-m13-2 means `standing_registry_rows`' strictness is shared: any formatting change to the standing row silently degrades *both* m6's stated-count comparison and m13's newest-row selection to the previous row.
- The selftest (A6's three new cases) covers prose-only `Planned`, column-zero-plus-prose `0,3`, and multi-entry map — none of the constructed inputs above; none of these divergences would be caught by the counter's own fixtures.
- Counter-version drift: three versions of `measure.py` are live across pins (`97609511` pinned A6, `52961c37` at `c5335c70`, `ab76cbd3` in the worktree). Findings are version-invariant, but the deciding run's counter sha should be re-confirmed before reliance.
- No tool installs or updates were made for this item; the operator directive required none (python3 + git sufficed).
