seat: T46MutFreshA
item: generalization attack on the hardened freshness counter `.ufo/evidence/round-46/hardening/freshness-counter.py` (content rev `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` bytes, sha256 `f2a8ec0f...c623c507`) — 19 NEW single-point mutants in 12 rule families that the declared manifest `mutants.json` (F01–F15, FN1–FN3) does not cover; 14 survive, 5 are killed, 1 survivor is equivalent, and every real-gap survivor ships with a validated kill case.

## Verdict

The wave-1 selftest additions pin exactly their declared mutants and nothing more. Every rule family listed in the seat assignment — overlap threshold, STOP-word/word-length filter, fold dash/quote tables, HTML tag/script strip + `html.unescape`, the `load_snapshot` `.gz` branch, the `member` extraction path, the `opened` comparison — tolerates at least one one-line weakening that leaves `--selftest` at `VERDICT: PASS` (exit 0). The overlap gate (counter docstring line 22: "shares >= 2 distinct content words (lowercase [a-z0-9]+, length >= 4, not a stopword)") is the worst case: all three of its clauses weaken independently and survive (G01, G03, G04 — HIGH). None of this falsifies C2, whose statement is scoped to the 25 declared survivors plus field equivalence; these are coverage findings for the next hardening pass, not a contract breach.

## Method

- Scratch copy: `cp .../hardening/freshness-counter.py /tmp/tameshi-r46-T46MutFreshA/h.py`; `sha256sum` both = `f2a8ec0fc3e08be1f439527cab8abfe6607353e91e22a1ca9277e010c623c507`.
- Detector (pristine baseline): `python3 h.py --selftest` → `C1_R45_SELFTEST: cases=34 failed=0`, `VERDICT: PASS`, rc=0. A mutant leaving this state is a survivor.
- Each mutant: exactly one replacement; driver `run.py` asserts the old fragment occurs exactly once in the source, runs `ast.parse` on the mutated copy (valid Python), runs the selftest as a subprocess, restores exact pristine bytes after every run.
- Killer harness `killers.py`: 14 cases, each asserting the PRISTINE documented behavior for one unpinned rule (grade()/load_snapshot() fixtures, no git). Run on pristine all 14 must PASS; run on a mutant, the target case failing is the validated kill.

## Fleet table (detector: `python3 /tmp/tameshi-r46-T46MutFreshA/h.py --selftest`)

`run.py` output, unabridged verdict column. Line numbers are in the pristine counter.

| id | file:line | old -> new | result |
|---|---|---|---|
| G01 | freshness-counter.py:163 | `if len(shared) < 2:` -> `if len(shared) < 1:` | SURVIVED (rc=0, cases=34 failed=0) |
| G02 | freshness-counter.py:163 | `if len(shared) < 2:` -> `if len(shared) < 0:` | killed — FAIL T8_boilerplate_no_overlap |
| G03 | freshness-counter.py:129 | `len(w) >= 4 and w not in STOP` -> `len(w) >= 4 and True` | SURVIVED |
| G04 | freshness-counter.py:129 | `len(w) >= 4 and w not in STOP` -> `len(w) >= 1 and w not in STOP` | SURVIVED |
| G05 | freshness-counter.py:102 | `('\u2019', "'")` -> `('\u2019', '\u2019')` | SURVIVED |
| G06 | freshness-counter.py:103 | `('\u2014', '-')` -> `('\u2014', '\u2014')` | SURVIVED |
| G07 | freshness-counter.py:103 | `('\u00ad', '')` -> `('\u00ad', '\u00ad')` | SURVIVED |
| G08 | freshness-counter.py:103 | `('\u00a0', ' ')` -> `('\u00a0', '\u00a0')` | SURVIVED — EQUIVALENT (see below) |
| G09 | freshness-counter.py:122 | `r'(?is)<(script\|style)\b.*?</\1\s*>'` -> `r'(?is)<(xscript\|xstyle)\b.*?</\1\s*>'` | SURVIVED |
| G10 | freshness-counter.py:124 | `text = html.unescape(text)` -> `text = text` | killed — FAIL T14_entity_unescaped |
| G11 | freshness-counter.py:121 | `if re.search(r'<(html\|body\|div\|p\|head)\b', text, re.I):` -> `if False:` | killed — FAIL T14_entity_unescaped only |
| G12 | freshness-counter.py:110 | `if member:` -> `if False:` | SURVIVED |
| G14 | freshness-counter.py:174 | `if path.endswith('.gz'):` -> `if path.endswith('.gzip'):` | SURVIVED |
| G15 | freshness-counter.py:178 | `return None` (in `except OSError:`) -> `data = b''` | SURVIVED |
| G16 | freshness-counter.py:139 | `< MIN_OPENED` -> `<= MIN_OPENED` | killed — 11 cases (T1, T10, T13, T14, T19, F01, F02, F03, F10, F11, F12) |
| G17 | freshness-counter.py:139 | `entry.get('opened', '')` -> `entry.get('opened', '2026-10-25')` | SURVIVED |
| G18 | freshness-counter.py:151 | `if n < 6 or n > 25:` -> `if n < 1 or n > 25:` | killed — FAIL T6_quote_too_short |
| G19 | freshness-counter.py:123 | `text = re.sub(r'(?s)<[^>]*>', ' ', text)` -> `text = text` | SURVIVED |
| G20 | freshness-counter.py:112 | `raw = tar.extractfile(member).read()` -> `raw = tar.extractfile(tar.getmembers()[0].name).read()` | SURVIVED |

## Survivors, classified

### Real selftest gaps (12 of 14; kill cases validated)

Each kill case below was run two ways: on pristine all 14 killer cases PASS (`python3 killers.py` → `KILLERS: cases=14 failed=0`), on the mutant the named case FAILS — that failure is the kill. Full harness: `/tmp/tameshi-r46-T46MutFreshA/killers.py`.

**G01 — overlap threshold, HIGH.** A quote sharing exactly one content word with the row is admitted. Kills the documented `>= 2` clause.
```python
page = b'<html><body><p>flaky perihelion quantum xor trombone carousel records</p></body></html>'
row = dict(ROW, teaches='rerun order hides defects')   # shares only 'flaky'
q = 'flaky perihelion quantum xor trombone carousel'
# pristine: ('invalid', 'overlap 1'); G01: ('verified', 'ok')
assert h.grade(entry(page, q), row, page) == ('invalid', 'overlap 1')
```
Validation: `TARGET G01 killers_rc=1 kills: FAIL K01_overlap_threshold got=('verified', 'ok') want=('invalid', 'overlap 1')`.

**G03 — STOP-word filter, HIGH.** With the filter dropped, a quote whose only row overlap is stopwords (`that`, `section`) reaches overlap 2 and is admitted.
```python
row = dict(ROW, teaches='rerun order hides defects that')
q = 'that section perihelion quantum trombone carousel'
# pristine: ('invalid', 'overlap 0'); G03: ('verified', 'ok')
```
`TARGET G03 ... FAIL K03_stopwords_stopped got=('verified', 'ok') want=('invalid', 'overlap 0')`.

**G04 — word length 4, HIGH.** Dropping the `len(w) >= 4` floor lets two 2-letter tokens carry the overlap.
```python
row = dict(ROW, teaches='rerun order hides defects ab cd')
q = 'ab cd perihelion quantum trombone carousel'
# pristine: ('invalid', 'overlap 0'); G04: ('verified', 'ok')
```
`TARGET G04 ... FAIL K04_word_length_floor got=('verified', 'ok') want=('invalid', 'overlap 0')`.

G01+G03+G04 together: the overlap gate — one sentence of the frozen predicate — has no selftest case below the boundary in any of its three clauses. T8 is the only boundary case and it sits at overlap 0, so any "refuse less" weakening of the threshold itself (G01) or of the word filter (G03/G04) passes.

**G05 — apostrophe fold, LOW.** `U+2019` left unfolded: a snapshot's typographic apostrophe no longer matches the entry's ASCII one.
```python
page = '<html><body><p>the author\u2019s summary claims reruns flake now</p></body></html>'.encode()
row = dict(ROW, teaches='author summary claims verified elsewhere')
q = "the author's summary claims reruns flake"
# pristine: ('verified', 'ok'); G05: ('invalid', 'quote absent')
```
`TARGET G05 ... FAIL K05_apostrophe_folded got=('invalid', 'quote absent')`.

**G06 — em dash fold, LOW.** Same shape with `U+2014` vs `-`. `TARGET G06 ... FAIL K06_emdash_folded got=('invalid', 'quote absent')`.

**G07 — soft hyphen, LOW.** `U+00AD` left in place splits a snapshot word: `order\u00ading` no longer matches `ordering`. `TARGET G07 ... FAIL K07_softhyphen_dropped got=('invalid', 'quote absent')`.

**G09 — script strip, LOW.** A quote that lives only inside `<script>` is admitted when the strip pattern is deafened. T13 does not cover this (see defects below).
```python
page = (b'<html><body><script>perihelion quantum trombone carousel records live here now</script>'
        b'<p>visible reruns text only today</p></body></html>')
# pristine: ('invalid', 'quote absent'); G09: ('verified', 'ok')
```
`TARGET G09 ... FAIL K09_script_stripped got=('verified', 'ok') want=('invalid', 'quote absent')`.

**G12 — member ignored, LOW.** With `if member:` -> `if False:`, a text-member fixture still verifies — a tar stream stores member bytes verbatim, so whole-stream decoding coincidentally finds the quote (K12 passes under G12). The separator is a member that pristine *transforms*: a PDF member (Flate-compressed text). Pristine runs pdftotext on the named member; the mutant decodes the raw tar stream, never reaches the `%PDF` branch, and the compressed quote is absent.
```python
pdf = _pdf_bytes('perihelion quantum trombone carousel records deeper')  # Flate content stream
tar = _tar_bytes([('doc.pdf', pdf)])
# pristine: ('verified', 'ok') via pdftotext; G12: ('invalid', 'quote absent')
```
`TARGET G12 ... FAIL K12p_pdf_member_transformed got=('invalid', 'quote absent')`.

**G14 — `.gz` branch dead, LOW.** `path.endswith('.gzip')` disables gunzip in `load_snapshot`; the compressed bytes then hash against the entry's raw `raw_sha256`. No selftest case reaches `load_snapshot` at all (grade-level cases pass raw bytes; the measure-level fixtures use plain `snap/page.txt`).
```python
gz = gzip.compress(page)                      # entry.raw_sha256 = sha256(page)
raw = h.load_snapshot(lambda p: gz, 'snap/page.txt.gz')
assert raw == page                             # G14: raw is the 93 compressed bytes -> sha mismatch
```
`TARGET G14 ... FAIL K14_gz_unpacked load_snapshot returned 93 bytes` (and K15 collaterally).

**G15 — corrupt-gz classification, LOW.** `except OSError: return None` -> `data = b''` reclassifies a corrupt `.gz` from `snapshot absent` into the hash/quote pipeline instead of the absent path.
```python
corrupt = b'\x1f\x8b\x09\x08junkjunk'          # gzip magic, invalid method byte -> BadGzipFile (OSError)
raw = h.load_snapshot(lambda p: corrupt, 'snap/page.txt.gz')
# pristine: raw is None and grade == ('invalid', 'snapshot absent'); G15: raw == b''
```
`TARGET G15 ... FAIL K15_corrupt_gz_absent load_snapshot returned b''`.

**G17 — missing `opened` accepted, LOW.** The `<` boundary itself is pinned (G16 killed by 11 cases), but the empty-string default is not: an entry with no `opened` key passes the gate under G17.
```python
e = entry(page, q); del e['opened']
# pristine: ('invalid', 'opened before round'); G17: ('verified', 'ok')
```
`TARGET G17 ... FAIL K17_opened_required got=('verified', 'ok')`.

**G19 — generic tag strip, LOW.** Deleting the `<[^>]*>` strip line survives: the only case named for tag-splitting (T13) is vacuous (defect 1 below). `TARGET G19 ... FAIL K19_tags_stripped got=('invalid', 'quote absent')`.

**G20 — wrong member, LOW.** Reading `members()[0]` instead of the named member survives; killed by a two-member tar whose quote lives in the second member. `TARGET G20 ... FAIL K20_named_member_not_first got=('invalid', 'quote absent')`.

### Equivalent (1)

**G08 — `('\u00a0', ' ')` table entry, INFO, dead code.** `unicodedata.normalize('NFKC', '\u00a0')` is already `' '` and `fold()` runs NFKC before the table on every call, so removing the entry cannot change any fold output. Differential sweep: `fold` vs fold-without-the-NBSP-entry over 6 probes (empty, plain ASCII, NBSP-heavy, and a string containing every other table character) → `IDENTICAL on 6 probes (incl. NBSP-heavy)`; the same probe shows NFKC leaves `\u00ad \u2019 \u2014 \u200b \ufeff` untouched, which is why G05–G07 are NOT equivalent. Not a gap; the entry is redundant with line 101.

## Kills (coverage the selftest already pins) — INFO

- G02 (`< 0`): T8 pins that overlap 0 refuses.
- G10 (unescape no-op) and G11 (strip gate off): T14 pins entity unescaping. Caveat: G11's kill arrives only through T14's unescape path, NOT through tag-splitting — T13 is vacuous (defect 1), and G19 proves the tag-strip line itself is unpinned.
- G16 (`<=`): the `opened >= 2026-10-25` boundary is the best-pinned rule in the file — 11 cases fail, every fixture sits exactly on the boundary.
- G18 (`n < 1`): T6 pins the 6-token quote floor (its quote is verbatim present in the fixture page, so a weakened floor flows through to `verified`).

## Defects found on the way

1. **T13_tag_split_quote is vacuous — LOW.** `tagged = page.replace(b'detected mutants', b'<b>detected</b> mutants')` no-ops because the fixture page holds a zero-width space between `detected` and `mutants`. Proof: `tagged == page` → `True`. T13 therefore cannot fail for its named rule (it passed under G11 and passes under G19); the generic tag-strip rule is pinned by no passing case. The same fixture with a real tag split (K19's page) is the one-line repair.
2. **Stale-bytecode harness pitfall — INFO.** Importing the counter as a module (importlib SourceFileLoader) validates `__pycache__` on (mtime seconds, size). A size-preserving mutant written in the same second as the previous compile is served stale bytecode: G01 was twice reported `rc=0` inside a validation loop while the identical mutant kills on a direct run, and G06 (same +5-byte size as G05) was graded with G05's bytecode. `killers.py` now `exec()`s the source bytes directly; the fleet table is unaffected because `python3 h.py --selftest` runs as `__main__`, which never reads `__pycache__`. Any future harness that imports the counter as a module should do the same.

## Commands and outputs

```
$ python3 h.py --selftest                      # pristine baseline
C1_R45_SELFTEST: cases=34 failed=0
VERDICT: PASS                                  # rc=0

$ python3 run.py                               # 19-mutant fleet, per-mutant restore
BASELINE rc=0 VERDICT: PASS | C1_R45_SELFTEST: cases=34 failed=0 fails=[]
... (table above; 14x SURVIVED rc=0, 5x killed rc=1) ...
RESTORED rc=0 VERDICT: PASS | C1_R45_SELFTEST: cases=34 failed=0 | sha=f2a8ec0f... match=True
DONE 19 mutants, 14 survived

$ python3 killers.py                           # pristine: all 14 hold
KILLERS: cases=14 failed=0
# per-mutant: python3 apply.py <Gxx> > h.py && python3 killers.py   (see TARGET lines above)

$ sha256sum h.py h.pristine.py <lane>/hardening/freshness-counter.py
f2a8ec0fc3e08be1f439527cab8abfe6607353e91e22a1ca9277e010c623c507  (all three identical)
```

Unrun (out of my seat's bounds): no counter run against `--rev` was made by this seat — `--selftest` only; the deciding runs belong to the L1.

## Tooling

No tool installed, upgraded or removed; pacman untouched. Only python3 + git (already present) were used.

## Bounds

All scratch under `/tmp/tameshi-r46-T46MutFreshA/` (`h.py`, `h.pristine.py`, `run.py`, `apply.py`, `killers.py`, `results.json`); fixture git repos were created only by the counter's own selftest inside its tempdirs. No `git`/`jj` command was run in the lane; the lane checkout is byte-identical to before (hash above); the only lane file written is this report.
