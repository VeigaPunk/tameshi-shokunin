# Round 40 lesson

author: tameshi L1 (Kimi fresh L1)
date: 2026-10-24

## Gate

Theme: F4 snapshot-practice corpus, and the write forms the round-39 pattern misses. Sources re-opened this round. Access date 2026-10-24. Two admits, one reject from the assimilation set. S108 was pinned before any new citation used it as support. The new write-form entry does not cite S108.

### Admit — `corpus/knowledge/r6-snapshot-practice-corpus.md` (S152)

- URL: https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download
- Access 2026-10-24. PDF sha256 `65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703`. Excerpt `.ufo/evidence/round-40/sources/s152-excerpt.txt`.
- Quote (11 words), English abstract: "drawbacks such as fragility and lack of context can lead to false positives".
- Staged recheck prose (`365d — curl …`) was stripped to `365d`. The curl condition is this block. No cell contains a pipe. used-by is the thesis entry and `corpus/knowledge/r40-write-form-misses.md`. Status mined. Opened date is this round's access date, not the campaign's.

### Admit — `corpus/knowledge/r3-snapshot-fixture-update-paths.md` (S132)

- URL: https://raw.githubusercontent.com/VictorGazzinelli/snapshot-testing/master/README.md
- Access 2026-10-24. Snapshot sha256 `8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea`.
- Quote (7 words), README row D29: "Snapshot Testing: Use With Care - Randy Coulman".
- The register marked S132 `payload-absent`. The raw README fetched this round contains that title, so the payload is present. Adopted with this anchor, not the campaign quote. used-by is only the admitted entry. Recheck normalized to `365d`.

### Reject — staged `r4-gate-write-path-audit` (S137)

Reason: the flip from round 39 is still unmet. `git show 31687496b5f34b153626e123d12ae2febdbd86a0` touches two round-35 receipt files, not a write-path census. `tools/write-path-census.py` is absent at that revision. `payload-absent`, not a fetch failure.
Flip: a hand-check that locates a write-path census artefact at that revision whose counts reproduce.

### S108 disposition

The round-39 closure could not re-open https://www.tensorflow.org/federated/golden_tests?hl=zh-cn (redirect loop) and there was no snapshot. This round fetched the page (111405 bytes, `lang=zh-CN`). The quote is in the tag-stripped text. The raw HTML wraps the flag and `.expected` in `<code>` tags, so a contiguous-byte search misses it. Snapshot `.ufo/evidence/round-40/s108/golden_tests.zh-cn.html`, sha256 `f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0`. The row stays mined. No status, recheck, or used-by cell on an existing row changed.

Quote (the round-39 sentence, located again): "可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。"

### Collision and census

Registry ids and staged S132/S152: collisions empty. Indented-guard proof: a scratch registry row `  | S132 |` produced a nonempty collisions file (`collisions` = `S132`); a column-zero-only pattern produced an empty list. Scratch `sources-census.sh validate --file` exited 0 before the registry append (warnings only, the pre-existing W01/W04 set). No E03 or E04 on the new rows.

### Transformation applied to the staged rows

No staged row was appended byte-exact. Two rows changed, both recorded here:

- S152 title: the campaign row reads `Undertstanding snapshot testing in practice`; the appended row reads `Understanding`. The quote and the URL are unchanged.
- S152 and S132 `recheck`: the staged prose `365d — curl … (expect a non-zero count; the string was present in the copy opened 2026-10-23)` is stripped to `365d`. The stripped curl condition is this Gate block.
- S132 `opened` and S152 `opened`: this round's access date `2026-10-24`, not the campaign's `2026-10-23`.
- `used-by`: exactly the admitted entries that cite the row — S132 → `corpus/knowledge/r3-snapshot-fixture-update-paths.md`; S152 → `corpus/knowledge/r6-snapshot-practice-corpus.md`, `corpus/knowledge/r40-write-form-misses.md`.
- No cell contains a literal or escaped pipe; all 107 registry rows parse as 13 awk fields.

### Quarantine — 17 data rows, one verdict each

Slice derived with the item-10 recipe (`awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/'`): 17 rows, every line carrying an S-id (`.ufo/waves/round-40/assimilation/quarantine-slice`). The register was not edited.

| id | class in register | verdict | seat |
|---|---|---|---|
| S105 | payload-absent | present — the register verdict is a whitespace-fold false positive; adopt-eligible, not appended (no admitted entry cites it) | `ScoutQ105` |
| S109 | payload-absent | absent — the landing page carries no abstract body; the linter's ABSENT is mechanically correct. Refuse | `ScoutQ109` |
| S110 | payload-absent | present, verbatim; adopt-eligible, not appended | `ScoutQ110` |
| S113 | could-not-be-fetched | present — the DOI resolves and the author camera-ready PDF opens (HTTP 200, 131622 bytes); the quote is located verbatim in §3.2. The prose class is stale; adopt-eligible, not appended | `ReviewQ113` |
| S118 | payload-absent | misbound — the lint record's quoted span is a parenthetical provenance note, not a claim about page content. Not a fabrication; not appended | `ScoutQ118` |
| S119 | payload-absent | present, verbatim (page locator off by one); adopt-eligible, not appended | `ScoutQ119` |
| S123 | could-not-be-fetched | present — the cited URL answers 202 to this host, and the staged figures are verbatim in the arXiv carrier the campaign already pins as S193; the prose class is stale. Adopt-eligible, not appended | `ReviewQ123` |
| S124 | payload-absent | present — the quoted line is in the cited source; adopt-eligible, not appended | `ReviewQ124` |
| S126 | payload-absent | present — the quoted span is in the cited source; adopt-eligible, not appended | `ReviewQ126` |
| S129 | payload-absent | present — the flagged token is a code token from a provenance note; the row's two real gate quotes verify. Adopt-eligible, not appended | `ReviewQ129` |
| S131 | payload-absent | refuse as pinned — the pinned locator times out from this host, so the row is unreachable, not fabricated; the content is already covered by S105. Not appended | `ReviewQ131` |
| S132 | payload-absent | present — the raw README row D29 carries the title. **Adopted** (see the Admit block above) | `ScoutS132` |
| S134 | could-not-be-fetched | present — the DOI opens through the campaign's own `aaron` channel and the quote is locatable in the fetched text. The prose class is stale; adopt-eligible, not appended | `ReviewQ134` |
| S137 | payload-absent | absent — the flip from round 39 is unmet at `31687496`. Refuse | `ScribeGate`, `ReviewQ141` |
| S140 | payload-absent | absent — the quoted span and the row's recheck output are in no cited source. Refuse | `ReviewQ140` |
| S141 | payload-absent | absent — commit `31687496` carries no 86-site census. Refuse | `ReviewQ141` |
| S143 | payload-absent | absent — the source is live but the quote is in none of it. Refuse | `ReviewQ143` |

One row adopted, seven refused (S109, S131, S137, S140, S141, S143 and the two prose-class rows whose premise a seat falsified), nine present-but-not-appended. No row is called a fabrication. The register and every campaign file were left byte-identical.

### Status changes

No existing row's status, recheck, or used-by changed. New rows only: S132, S152.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| quote-split | the S108 HTML wraps `--test_arg=--update_goldens` and `.expected` in `<code>` tags, so a raw-byte search for the contiguous quote fails | none until this round's counter; criterion 79 | the frozen check is tag-stripped text; removing the prefix `可以通过使用参数` makes `stripped_quote_fails=1` |
| vacuous-pattern | round-39 `EXPECTED_RE` misses `expected.json` and `WRITE_RE` misses `os.replace` | the round-39 lesson Holds, not a counter | successor tool; v1 pin unchanged; planted fixtures and two mutants fail if either recognizer is removed |
| draft-summary-drift | this lesson's first draft asserted "S113 and S123 … quotes were not located"; seats `ReviewQ113` (quote located verbatim in the author camera-ready PDF, HTTP 200) and `ReviewQ134` (the DOI opens through the campaign's `aaron` channel) falsified that sentence | none — no rule required the round's own summary to be re-read against the seat reports before it was written | the resumed L1 re-read each of the 17 slice seat reports and rewrote the quarantine table from them; the corrected table above carries one verdict and one seat pointer per row. The fix is only credited because the corrected verdicts contradict the draft — a rule that cannot fail is not a rule |

## Holds

- The v2 pattern still misses shell redirects, an `open()` whose path is not a string literal, and `os.replace` whose destination is a variable. The live `os.replace(tmp, path)` site is a write-site hit, not an expected-value hit.
- Seat `CriticUniversal` found that `os.symlink`, `os.link`, `Path.symlink_to`, `Path.rename`, `shutil.copy*`, `os.remove/unlink` and `handle.write` are outside v2's `WRITE_RE`. `tools/repeat-control.py:807-823` writes `expected.json` through a variable path and through `os.symlink`, and `tools/registry-replay.py:161,230` and `tools/bash-witness-study.py:1638,1705,1707` mutate the filesystem in forms v2 does not see. The frozen predicate names two live sites and two planted classes and claims no universality; these are open coverage gaps, not a counter failure. The v2 docstring dropped v1's non-universal disclaimer — disclosed here rather than repaired after the freeze.
- POSIX `diff` remains the only exit lattice this lane has pinned. `cmp` and `git diff --exit-code` stay unmeasured.
- The round-38 L0 question `d0531d78` is not re-filed.
