seat: T46MutCoverB
item: Generalization attack on the hardened coverage counter (.ufo/evidence/round-46/hardening/coverage-counter.py): 20 new single-line mutants on rules the declared manifest C01-C10 does not cover, detected with the counter's own `--selftest`, survivors classified and each real gap killed by a demonstrated fixture.

# Bounds kept
- Read-only on the lane except this report file. All work in /tmp/tameshi-r46-T46MutCoverB/ (h.py is a byte copy of the lane counter; matrix.py drives the mutations; killers.py drives the killer fixtures; matrix.json holds raw results).
- Counter exercised only as `--selftest` and as `--lane <scratch> --rev m` inside throwaway fixture repos (`git init -q -b m` in mktemp dirs; `rev-parse --show-toplevel` asserted equal to the scratch dir before each first commit). No deciding run, no lane write, no git/jj mutation, no pacman, no tool installs.

# Baseline (detector sanity)
- `sha256sum h.py` = `200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9`, byte-identical to the lane counter at content revision's committed file (lane sha256 compared equal).
- `python3 h.py --selftest` -> rc=0, `C2_R45_SELFTEST: cases=20 failed=0`, `VERDICT: PASS`. Baseline passes, so verdicts below are meaningful (a baseline failure would have been inconclusive, not a kill).

# Method
For each mutant: exactly one `old -> new` substring replacement in the scratch copy (count==1 asserted), `ast.parse` validity gate, `python3 h.py --selftest`, verdict recorded, bytes restored and sha-checked after every mutant. Detector = the 20-case selftest (10 T-cases + HardCover1 C01-C05 + HardCover2 C06-C10). Survivors were then re-run against targeted killer fixtures: pristine vs mutated bytes on the smallest repo that separates the rule. All fixture runs self-pin the running file's own bytes at SELF_PATH, so `self_pin=1` throughout.

# Matrix (20 new mutants; none equals a declared (old,new) pair)
| id | file:line (h.py = lane counter bytes) | old -> new | --selftest result |
|----|----|----|----|
| N01 | 96 | `if not cited:` / return 'cites no googletest row' -> `if False and not cited:` (gate bypassed) | SURVIVES (PASS, 20/20) |
| N02 | 105 | `if path in rows[c]['used']]` -> `if True]` (used-by filter dropped) | killed (T5_not_used_by) |
| N03 | 110 | `any(quote in rows[c]['text'] for c in cited)` -> `all(...)` | SURVIVES (PASS, 20/20) |
| N04 | 110 | `if 6 <= len(quote.split()) <= 25` -> `if 1 <= ...` | SURVIVES (PASS, 20/20) |
| N05 | 101 | `m.group(1) < MIN_VERIFIED` -> `<=` | killed (T1, T3 + 8 more) |
| N06 | 129 | both README membership forms -> both without backticks | SURVIVES (PASS, 20/20) |
| N07 | 135 | `len(indexed) == len(entries)` -> `>=` | SURVIVES (PASS, 20/20) |
| N08 | 135 | `passed = self_pin == 1 and` -> `self_pin >= 1 and` | SURVIVES (PASS, 20/20) |
| N09 | 131 | `elif why != 'cites no googletest row':` -> `elif False:` | SURVIVES (PASS, 20/20) |
| N10 | 132 | `print('REFUSED %s %s' % (path, why))` -> `print('REFUSED %s' % path)` | SURVIVES (PASS, 20/20) |
| N11 | 171 | selftest build(): `put(SELF_PATH, open(...).read())` -> `put(SELF_PATH, b'# stub\n')` | killed (T1_two_entries_pass) |
| N12 | 64 | `return out.stdout.decode().split() if out.returncode == 0 else []` -> `return out.stdout.decode().split()` | SURVIVES (PASS, 20/20) |
| N13 | 33 | ROW_RE `^ {0,3}\|` -> `^\s*\|` | SURVIVES (PASS, 20/20) |
| N14 | 74 | `len(cells) != 13` -> `!= 14` | killed (T1 + 12 more) |
| N15 | 88 | `re.split(r'[,;]', cells[11])` -> `re.split(r',', cells[11])` | SURVIVES (PASS, 20/20) |
| N16 | 37 | HEX_RE `\b[0-9a-f]{8,64}\b` -> `\b[0-9a-f]{8,}\b` (trailing \b kept) | SURVIVES (PASS, 20/20) |
| N17 | 34 | URL_RE `[^\s;,)]+` -> `[^\s,)]+` | SURVIVES (PASS, 20/20) |
| N18 | 57 | Tree.read `if out.returncode != 0: return None` -> `if False:` | killed (HardCover1 C03_missing_snapshot_empty_sha) |
| N19 | 88 | `re.split(r'[,;]', cells[11])` -> `... cells[10])` | killed (T1 + 9 more) |
| N20 | 37 | HEX_RE `\b[0-9a-f]{8,64}\b` -> `\b[0-9a-f]{8,}` (trailing \b dropped) | SURVIVES (PASS, 20/20) |

Score against the undeclared-rule surface: 6 killed / 14 survived. Every survivor is named below; none is dead code (all sites execute on every `--selftest` and every measure run).

Site-overlap disclosure: N06, N07, N08, N14 touch text that substring-overlaps declared C06/C09/C10/CN2 olds, but each replacement is a different mutation (C06 keeps only the short backticked form — N06 keeps both forms unbackticked; C09 `>= 1` — N07 `>= len(entries)`; C10 `>= 0` — N08 `>= 1`; CN2 `0xD` is semantically neutral — N14 `14` is behavior-changing). No (old,new) pair collides with mutants.json (checked programmatically against both groups).

# Real selftest gaps (9 survivors, each killed by a demonstrated case)
All killer runs: pristine fixture shows the designed pristine outcome; the same fixture under the mutant diverges, so the asserted case kills. Fixtures are scratch repos built like the counter's own selftest builds.

## G1 — REFUSED classification/format unasserted (N01, N09, N10) — LOW
The selftest never reads any line except the last (the C2_R45 summary); REFUSED output is completely unguarded.
```python
reg = row('S256','advanced', EA+', '+EB) + row('S257','primer', EA+', '+EB)
extra = {'corpus/knowledge/plain.md':  'hello world\n',                       # non-entry
         'corpus/knowledge/broken.md': 'source: S256 — x\nverified-at: 2020-01-01\nrecheck: 5d\n'}
lines, summary = run(reg, {EA: ENTRY, EB: ENTRY}, IDX, extra)
refused = [l for l in lines if l.startswith('REFUSED')]
assert refused == ['REFUSED corpus/knowledge/broken.md verified-at'], refused
```
Observed: pristine `refused=1`, exactly `REFUSED corpus/knowledge/broken.md verified-at`, `C2_R45_PASS=true`. N01: `refused=2` (spurious `REFUSED corpus/knowledge/plain.md no provenance trio` — the cited-vs-provenance ordering flipped the silent skip into a refusal). N09: `refused=0` (unparsable entries silently swallowed). N10: `REFUSED corpus/knowledge/broken.md` (reason field lost).

## G2 — quote located in *any* vs *all* cited snapshots indistinguishable (N03) — LOW
Every fixture in the selftest gives all rows the same snapshot bytes, so `any` and `all` coincide.
```python
snapA = b'the quick brown fox jumps over the lazy dog again and again for ever and ever today\n'
snapB = b'pack my box with five dozen liquor jugs now please my friend okay done\n'
reg = row('S256','advanced', EA+', '+EB, h=sha8(snapA)) + row('S257','primer', EA+', '+EB, h=sha8(snapB))
ent = 'source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n' \
      'Body says "the quick brown fox jumps over the lazy dog" as quoted.\n'   # quote is in A only
lines, summary = run_two_snap(reg, ent)
assert 'C2_R45_PASS=true' in summary   # pristine: located via S256
```
Observed: pristine `rows=2 entries=2 indexed=2 ... PASS=true`; N03 `entries=0 ... PASS=false` (quote not in S257's text).

## G3 — 6-token quote floor unasserted (N04) — LOW
```python
ent = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
       'Upstream says "undefined, so your code" in brief.\n')   # 4 tokens, 23 chars: QUOTE_RE ok, window rejects
lines, summary = run(reg, {EA: ent, EB: ent}, IDX)
assert 'entries=0' in summary and 'C2_R45_PASS=false' in summary
```
Observed: pristine `entries=0 ... PASS=false`; N04 `entries=2 ... PASS=true`.

## G4 — README backtick requirement unasserted (N06) — LOW
```python
readme = 'see knowledge/a.md and knowledge/b.md for the entries'   # mentions, does not backtick
lines, summary = run(reg, {EA: ENTRY, EB: ENTRY}, readme)
assert 'indexed=0' in summary and 'C2_R45_PASS=false' in summary
```
Observed: pristine `indexed=0 ... PASS=false`; N06 `indexed=2 ... PASS=true`.

## G5 — table indent > 3 spaces must not count (N13) — LOW
```python
reg = '     ' + row('S256','advanced', EA+', '+EB) + '     ' + row('S257','primer', EA+', '+EB)  # 5-space: code block
lines, summary = run(reg, {EA: ENTRY, EB: ENTRY}, IDX)
assert 'rows=0' in summary and 'C2_R45_PASS=false' in summary
```
Observed: pristine `rows=0 ... PASS=false`; N13 `rows=2 entries=2 ... PASS=true`.

## G6 — ';'-separated used-by must parse (N15) — LOW
```python
reg = row('S256','advanced', EA+'; '+EB) + row('S257','primer', EA+'; '+EB)   # semicolon delimiter
lines, summary = run(reg, {EA: ENTRY, EB: ENTRY}, IDX)
assert 'C2_R45_PASS=true' in summary
```
Observed: pristine `entries=2 ... PASS=true`; N15 `entries=0 ... PASS=false` (`REFUSED ... not in used-by`).

## G7 — hex anchor token boundary unasserted (N20) — LOW
```python
anchor = SNAP_PREFIX + 'advanced.md ' + sha256(SNAP).hexdigest() + 'zz'   # 64-hex with trailing garbage
reg = row('S256','advanced', EA+', '+EB, anchor=anchor) + row('S257','primer', EA+', '+EB,
       anchor=SNAP_PREFIX + 'primer.md ' + sha256(SNAP).hexdigest() + 'zz')
lines, summary = run(reg, {EA: ENTRY, EB: ENTRY}, IDX)
assert 'rows=0' in summary and 'C2_R45_PASS=false' in summary   # pristine \b...{8,64}\b rejects the token
```
Observed: pristine `rows=0 ... PASS=false`; N20 `rows=2 entries=2 ... PASS=true`.

# Equivalent survivors (5) — INFO
- N07 (`len(indexed) == len(entries)` -> `>=`): a path enters `indexed` only inside the same branch that just appended it to `entries`, so `indexed` is always a subset of `entries`; `len(indexed) <= len(entries)` holds for every repo, hence `>=` is true exactly when `==` is. No input can distinguish; sweep over the selftest fixtures and killer fixtures shows identical output.
- N08 (`self_pin == 1` -> `self_pin >= 1`): `self_pin = int(blob is not None and <digests equal>)` is defined over {0, 1}; `>= 1` is `== 1`.
- N12 (Tree.ls ignores returncode): for `git ls-tree --name-only REV prefix`, every nonzero exit observed (bad rev, missing prefix, not-a-repo) prints diagnostics on stderr with empty stdout, so `.split()` equals the else-branch `[]`. No divergent input found in the sweep.
- N16 (HEX_RE `{8,64}` -> `{8,}`, trailing `\b` kept): for hex runs <= 64 both patterns extract identical tokens; for runs > 64 pristine extracts nothing and the mutant extracts only a token longer than any 64-char digest, so `any(digest.startswith(h))` decides identically. K7 under N16 reproduces the pristine output byte-for-byte (`rows=0 ... PASS=false`).
- N17 (URL_RE drops `;`/`)` exclusions): URL_RE feeds only `GT_RE.match`; both patterns start at the same leftmost `https?://`, and the fixed GT prefix (scheme + `github.com`/`raw.githubusercontent.com` + `/google/googletest/`) contains neither `;` nor `)`, so whenever the extractions differ in length, both fail (or both pass) GT_RE identically. Accept/reject invariant.

# Killed without being declared (6) — INFO
N02 (T5_not_used_by), N05 (10 cases), N11 (T1_two_entries_pass — the selftest's own snapshot write at SELF_PATH is load-bearing and pinned through T1's `C2_R45_PASS=true`), N14 (13 cases), N18 (HardCover1 C03 — the empty-bytes digest `e3b0c442` trap), N19 (10 cases). On these sites the 20-case selftest generalizes beyond the declared manifest.

# Restoration evidence
- After every mutant the scratch copy was rewritten from the pristine bytes and sha-checked (`sha256 restored == 200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9` after all 20 mutants and all killer runs).
- Post-restore `python3 h.py --selftest`: rc=0, `VERDICT: PASS`, `cases=20 failed=0`.
- Lane file untouched; scratch copy still byte-identical to the lane counter at close.

# Verdict summary
| class | ids | severity |
|----|----|----|
| real selftest gap, killer demonstrated | N01, N03, N04, N06, N09, N10, N13, N15, N20 | LOW (each) |
| equivalent mutant | N07, N08, N12, N16, N17 | INFO |
| killed by selftest (undeclared site) | N02, N05, N11, N14, N18, N19 | INFO |

No BLOCKING or HIGH finding: C2's letter (>= 23 of 25 declared survivors killed, 6 neutrals survive) is untouched by this probe — every mutant here is outside mutants.json. The finding is coverage, not defect: the hardened counter's 20-case selftest leaves the REFUSED channel, the any-vs-all quote-location discrimination, the 6-token quote floor, the README backtick form, the 3-space table indent, the `;` used-by delimiter and the hex-token boundary unguarded. The nine killer cases above (smallest-fixture form given) would close those gaps if folded into a future `extra_HardCover*` block; per wave-2 bounds I did not add them to the committed counter.
