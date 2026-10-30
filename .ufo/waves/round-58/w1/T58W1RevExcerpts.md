# T58W1RevExcerpts — excerpt compliance sample

Axes: excerpt fidelity; whole-token relevance; historical novelty; counter compatibility.

## Findings, by severity

### High — seven sampled rows contain noncompliant excerpts

The individual-excerpt contract passes every supplied excerpt in only **5/12 rows**. This does not reverse any semantic fixed/open judgment; it identifies evidence that cannot be copied into the ledger unchanged.

| Item / source seat | Excerpt contract | Observed failure / output |
|---|---|---|
| R50.1 / Verify01 | FAIL | First SOURCES.md:33 excerpt already occurs at routed_at: `routed_excerpt_present=true`. Second excerpt is novel and otherwise usable. |
| R51.1 / Verify02 | FAIL | registry.json:1251-1270 excerpt inserts literal `...` and collapses nonadjacent JSON: `present_in_named_base_lines=false`. |
| R51.7 / Verify03 | PASS | fleet-kill-rate-ledger.md:441: length 231, keys match, novel, no ACK words. |
| R52.1 / Verify04 | FAIL | Both excerpts have `key_hits=[]`, including LOG.md:2617-2622. The lesson excerpt's `re-key` is not the assigned `rekey` token. |
| R52.5 / Verify05 | FAIL | registry-check.py:761-772 replaces actual docstring text with `...`: literal normalized excerpt is absent. Raw length 461 additionally exceeds the seat's literal 400-character bound; counter-normalized length is 397. |
| R53.3 / Verify06 | PASS | controls-b.stdout:5: length 33, key CONTROLS_B, path absent at routed_at, no ACK words. |
| R53.7 / Verify07 | PASS | round-54.md:124-126: length 233, keys read_rev / inputs pinned, path absent at routed_at, no ACK words. |
| R54.6 / Verify09 | FAIL | First excerpt, T54W2Sent03.md:221, was already present at routed_at; both excerpts have no whole key token. Second path is also a frozen spotcheck path, excluded by counter check_evidence. |
| R54.10 / Verify10 | PASS | SCORECARD.md:2698-2701: length 276, keys match, novel at routed_at, no ACK words. |
| R56.2 / Verify12 | PASS | SKILL.md:53-54: length 257, keys match, novel at routed_at, no ACK words. |
| R56.6 / Verify13 | FAIL | registry.json:1366-1385 excerpt inserts `...` between JSON fields: `present_in_named_base_lines=false`. |
| R50.2 / Verify01 | FAIL | First SKILL.md:2193 excerpt closes the backtick after staged-id-guard.py, but actual command continues `--seed 1 --cases 400 --dump OUT.jsonl`; `present_in_named_base_lines=false`. Second excerpt matches. |

### Medium — five sampled rows use unsupported singleton line syntax

R50.1, R50.2, R51.7, R53.3 and R54.6 encode lines as `33`, `2193`, etc. The canonical `LINES` predicate in measure.py requires `a-b` (lines 120, 219-221), so use `33-33`, etc. This is independent of semantic validity and excerpt novelty. Three rows pass both the sampled excerpt checks and the additional line-format checks unchanged: R53.7, R54.10, R56.2.

Canonical counter details matter: all evidence entries must pass check_evidence (277-304); key relevance and fresh fixed evidence use existential selection (305-350), not a requirement that every entry be fresh. Thus an old or unkeyed supplemental excerpt alone is not necessarily a counter failure. ACK_WORDS is checked over the entire named span, not only the excerpt (345-348). The captured spans were additionally checked: no sampled span contains an ACK_WORDS substring. The counter also permits a whole path suffix as key relevance; this report's key column follows the assignment's stricter excerpt-token requirement.

## Executed commands and output

Sweep command:

```text
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevExcerpts-receipts/audit.py
```

Observed output: `sample_size=12`, `all_evidence_pass_rows=3`, `any_usable_evidence_rows=3`. The latter two include strict line syntax. Derived requested excerpt-only count: `excerpt_contract_pass_rows=5`.

Full executed JSON output is retained at the absolute path:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevExcerpts-receipts/audit.stdout.json`.

Per-row command arrays, selected line output, boolean check output, source input SHA256s, routed-path output SHA256s, and Git stderr are in the machine-readable report beside this file. For every evidence entry, the executed commands were:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:<evidence.path>
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <defects.json routed_at>:<evidence.path>
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <row.commit>:<evidence.path>
```

All sampled rows claim fixed-at-base, so the named state for line matching is the frozen base, not the shifting working tree. Excerpt and full-span whitespace normalization matches measure.py:146-147. ACK_WORDS was parsed as data from the counter AST; no counter code was imported or executed.

Selection: first proposed-fixed row per available source seat, then earliest remaining proposed-fixed row to reach 12. Verify08 had no proposed-fixed row. Verify11 was missing during execution; one final availability poll found all 13 outputs. Verify11 was then read: R55.4/R55.5/R55.7 are proposed open, R55.6 proposed fixed; R55.6 was not added to the already-complete sample.

## Residual risk and verification gaps

- This is evidence-format/novelty review, not independent semantic disposition adjudication or a full counter pass. Full counter eligibility includes excluded paths, commit ancestry, first-parent novelty, touched paths, item ties, and panel provenance not exhaustively tested here.
- Commit-state probes expose additional provenance gaps: e.g. R52.5's supplied commit cannot resolve registry-check.py, while some excerpts appear at base but not at their claimed resolving commit. These require canonical provenance review before admission; no replacement commit is invented here.
- LSP unavailable: `read xd://lsp` returned `No such tool`. No references/definition/diagnostics or semantic proof is claimed. This task audits JSON/text evidence through Git snapshots.
- No canonical runtime, rerouting, saturation or resume logic was changed or exercised; those broader reviewer axes are outside this assigned sample.
- Findings are a recommendation only. No lane content was edited, no commits were made, and no counter/build/test suite was run.

Scratch: no scratch directory or clone was created; none remains to delete. Tool installations/updates: none. The audit script is a retained reproduction receipt, not product scaffolding.

Self-evaluation: accuracy 4 (formal evidence checks, not full provenance); completeness 4 (12-row requested sample, late R55.6 unsampled); clarity 4 (two distinct pass counts explicitly separated); actionability 4 (exact offending fields and repair direction, no replacement rows); conciseness 4 (full receipts separated from summary). Overall 4.0/5. Main should repair evidence strings/ranges and run the canonical counter at the integrated deciding commit.
