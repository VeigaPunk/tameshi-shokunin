seat: ScribeEntryUndetected

item: Drafted the re-grounded F3 entry `r5-undetected-flaky-failures.md` (deliverable `.ufo/waves/round-46/w1/ScribeEntryUndetected.entry.md`) against committed snapshot S259, with 10 located verbatim quotes (11 of the 6–25-token located spans absent from the package copy), 7 labelled `Inference:` blocks, and four explicit corrections of the package copy.

## Deliverable

- Path: `.ufo/waves/round-46/w1/ScribeEntryUndetected.entry.md` (68 lines, 12,466 B)
- sha256: `00ec1760c8fba06d59f4fd21bb03e3c13bcf65c2837e54d3c95cd308dcc741cf`
  (`sha256sum .ufo/waves/round-46/w1/ScribeEntryUndetected.entry.md` → the line above)
- Header line 1 is byte-identical to the frozen requirement (checked programmatically: `line1_exact_match= True` against the item's exact string); line 2 is `verified-at: 2026-10-25`; line 3 is `recheck: 365d — …` with the command run and its output pasted; line 4 is the `ground:` line (F3 + F5).
- Staged path this file must land at: `corpus/knowledge/r5-undetected-flaky-failures.md` (basename must stay `r5-undetected-flaky-failures.md`: the C3 counter reads the package copy as `PKG_PREFIX + os.path.basename(entry_path)`).

## Grounding

Snapshot: `.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html`
`sha256sum` → `5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f` (matches the frozen digest).

Extraction (the item's command, exit 0, 1 line / 1668 words):

```
python3 .ufo/evidence/round-45/freshness/measure.py --extract .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html
```

Structure found in the snapshot: the abstract is served **four** times — visible abstract (raw offset 17673), BibTeX `abstract` field (36180), RIS `N2` field (41426), RIS `AB` field (43167) — so most sentences occur 4×; sentences the BibTeX block escapes (`{\textquoteright}`, `{\textendash}`, `{\texttimes}`) occur 3×.

Located quotes in the deliverable (token counts over the counter's `fold()`; occurrence counts are `grep -oF | wc -l` over the extraction; "fresh" = absent from `.ufo/evidence/round-46/assimilation/package/r5-undetected-flaky-failures.md` after the counter's `fold()`):

| # | tokens | occ | package | opening words |
|---|---|---|---|---|
| 1 | 19 | 4 | fresh | Flaky tests produce non-deterministic outcomes, passing or failing inconsistently… |
| 2 | 15 | 4 | fresh | Modern CI systems commonly rerun failed tests within the same job… |
| 3 | 19 | 4 | fresh | Existing research predominantly analyzes data from this detection mechanism… |
| 4 | 18 | 3 | fresh | All apparently deterministic failures were systematically validated through reruns in fresh environments… |
| 5 | 18 | 3 | wording shared (package bolds clause 2) | We found that, across all projects, undetected flaky failures account for 9.8 %–16.3 %… |
| 6 | 14 | 4 | present | These flaky failure rates spike temporarily… |
| 7 | 9 | 4 | fresh | While failures concentrate heavily in small test case subsets |
| 8 | 19 | 4 | fresh | the most disruptive test cases with undetected flaky failures remain largely invisible… |
| 9 | 16 | 3 | fresh | Additionally, test environments significantly influence flakiness, with up to 3× variation… |
| 10 | 18 | 4 | fresh | Our publicly available dataset of 154,000 flaky test cases with 1.7 million flaky failures… |

Dash-form check (the item's warning): the visible abstract and both RIS fields render `9.8 %–16.3 %` (en dash); the BibTeX block renders `9.8 \%{\textendash}16.3 \%`; over the extraction `grep -oF '9.8 %–16.3 %' | wc -l` → `0`, `grep -oF '9.8 %-16.3 %' | wc -l` → `3`, `grep -oF '9.8 \%{\textendash}16.3 \%' | wc -l` → `1`. The counter's `fold()` maps the en dash to the hyphen, so the quoted span matches the snapshot text.

Predicate check against the frozen counter's own function (in-process, synthetic row dict — not a verdict run):

```
entry_ok('corpus/knowledge/r5-undetected-flaky-failures.md', <deliverable text>,
         {'S259': {'text': norm_text(snapshot), 'used': {'corpus/knowledge/r5-undetected-flaky-failures.md'}, 'doc': …}}, <package text>)
→ (True, 'ok', ['S259'])
```

with `located_quotes_6_25=13` (includes two short continuations of quotes 1 and 10) and `fresh_vs_package=11`.

## Recheck, run and pasted

```
curl -fsSL 'https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/' -o /tmp/tum-r46.html \
  && sha256sum /tmp/tum-r46.html \
  && python3 .ufo/evidence/round-45/freshness/measure.py --extract /tmp/tum-r46.html \
     | grep -oF 'Modern CI systems commonly rerun failed tests within the same job to identify flaky failures' | wc -l
```
→ `b3051e44beda9b924aa1e449685e7880c55025d1a629fd117f3ecfd3f02ebf34  /tmp/tum-r46.html`, `4`, exit 0.

A second fetch the same day (`/tmp/tameshi-r46-ScribeEntryUndetected/live.html`, 51,588 B) gave `b0619632ebf4f34c1f8587ae45b49bac9257132a3371f7f0380455d20b4d1524` with the same count `4`. Both fetches normalize to text identical to the snapshot (`norm_text` equality `True`, 1668 words each). So the page serves volatile bytes (nonces/attributes) and the honest drift signal is the located-string count, not a digest comparison; the entry states exactly that.

## Corrections made against the package copy

1. Package header: "online date 2026-09-19". `grep -c '2026-09-19' <snapshot>` → `0`; the page says `Accepted/In press - 2026`. The entry claims no publication day.
2. Package: "open access per the institutional record". The snapshot carries only a markup marker — `<li class="open-access">` around the DOI link — and no visible licence sentence. The entry records it as markup only.
3. Package: "the lane's own 'one green control' verdict … (round 1's `S107`)". `S107` is the TensorFlow Federated golden-tests row (`corpus/SOURCES.md:119`, F4 explicit update flag), not the F3 repeated-control ground. Corrected to `corpus/README.md:80` (F3 row, "one control per sweep … → N ≥ 3 byte-identical controls") and `corpus/knowledge/repeated-control-precondition.md`.
4. Package: "`aaron` has no copy of this DOI". This is a tool claim, not a snapshot claim; the entry carries it as unverified by this seat and uses it for nothing.

## Lane citations verified before use

- `corpus/README.md:80` F3 row; `corpus/README.md:82` F5 row; `corpus/README.md:127` the round-12 scope line for `knowledge/repeated-control-precondition.md`.
- `corpus/knowledge/repeated-control-precondition.md:6` title line.
- `corpus/knowledge/hermetic-env-differential.md:2` (nine pinned surfaces, seven profiles, clean controls) and `:4` ("F3 universal determinism and successor freshness remain unclaimed").
- `tools/repeat-control.py:18` ("the environment is inherited unchanged") and `:94` ("is not a determinism proof and it cures no flakiness"); `tools/env-diff.py` exists (11,191 B).
- `corpus/SOURCES.md:119` is the `S107` row.

## Numbers used, and only these

8.8 billion test executions; four industry-scale projects; two-month periods; 9.8 %–16.3 % of failed pipeline runs; up to 3× environment variation; 154,000 flaky test cases; 1.7 million flaky failures; DOI 10.1109/TSE.2026.3729363; state `Accepted/In press - 2026`. All are carried by the snapshot. No other figure is asserted.

## Unrun / out of scope

- The C3 counter was **not** run as a verdict (`--rev …`); the deciding run is the L1's. Only the in-process `entry_ok` predicate was exercised, as above.
- No staging to `corpus/knowledge/`, no `corpus/README.md` index edit, no `corpus/SOURCES.md` row, no `sources-census.sh validate`, no selftest of the counter, no commit — those belong to other seats.
- Required by the C3 predicate for the row seat / integrator: `S259`'s used-by cell must contain exactly `corpus/knowledge/r5-undetected-flaky-failures.md`, and `corpus/README.md` must index the entry as backticked `` `knowledge/r5-undetected-flaky-failures.md` ``.

## Findings / limits

- **Volatile live bytes** (receipt above): a digest-equality recheck on this portal is a false-drift detector; the content-level count is the stable signal.
- **QUALITY 51 tension**: criterion 51 wants the `verified-at` line to name the sha256 of the tool bytes and a committed receipt; the frozen item fixes line 2 to the bare date. I followed the frozen header and put the tool path and the snapshot digest in the body/header instead — routed to the reviewer rather than resolved unilaterally.
- **Package misattribution** `S107` → F3 (finding 3 above) is a package defect that the entry corrects; the package file itself was not edited (read-only).
- The snapshot carries no method section and no per-project numbers; the entry's F3/F5 statements are protocol claims plus the source's measured blind-spot size, and its F5 link is explicitly marked `Inference:`.

## Tooling

No tool installed or upgraded this seat (no `pacman`, per the host-wide pause). Scratch only: `/tmp/tameshi-r46-ScribeEntryUndetected/` (`extract.txt`, `tum.txt`, `quotes.json`, `live.html`, `tum-r46.html`); no writes to `/home/vgpnk/Projects/shokuknow`, to the fleet repo, to sibling lanes, or to the lane's git index/jj state.
