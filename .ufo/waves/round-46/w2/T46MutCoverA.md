seat: T46MutCoverA
item: Generalization attack on the hardened coverage counter `.ufo/evidence/round-46/hardening/coverage-counter.py` (CONTENT rev `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`, sha256 `200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9`): 16 new single-rule mutants (none in mutants.json C01–C10) probed with its `--selftest`; 12 survive — 11 real selftest gaps, each with a demonstrated kill case, plus 1 equivalent — and 4 die, one of them for an incidental reason.

# Bounds kept
- Lane checkout untouched except this report file. No git/jj state touched; no `git add/commit/stash/checkout/switch/reset/pull/push` in the lane; no mutating jj command. No writes to `/home/vgpnk/Projects/shokunin` (fleet) or the read-only package `/home/vgpnk/Projects/shokuknow`.
- All scratch under `/tmp/tameshi-r46-T46MutCoverA/` (`h.py` working copy, `hN01.py`…`hN16.py` mutants, `baseline.log`, `n03b-selftest.log`, `probes.py`, `probes2.py`). Every fixture repo was `mktemp -d` + `git init -q -b m`, every later git call `-C "$D"`, toplevel asserted equal to the temp dir, commit identity `t <t@t>` confined to that dir — the same pattern the counter's own `--selftest` uses for its internal `--lane <scratch> --rev m` sub-invocations. All counter runs were `--selftest` or measure-mode over those throwaway scratch repos; no verdict was taken on the lane and no deciding run claimed (the deciding run is the L1's).
- No pacman; no tools installed (nothing beyond python3/git already present).

# Baseline (pristine)
- Command: `cp .ufo/evidence/round-46/hardening/coverage-counter.py /tmp/tameshi-r46-T46MutCoverA/h.py && python3 h.py --selftest`
- Output (baseline.log): `C2_R45_SELFTEST: cases=20 failed=0` / `VERDICT: PASS`, rc=0, wall 1.87s. Detector rule: a mutant whose selftest still prints `VERDICT: PASS` survives; `ast.parse` checked valid Python for all 16 mutants (16/16 parse-ok).

# Verdict table (16 mutants; pristine line numbers in h.py)
| id | file:line | old -> new (one site each) | --selftest | verdict |
|----|-----------|----------------------------|------------|---------|
| N01 | h.py:46 | `text = text.replace(a, b)` -> `pass  # N01: fold table disabled` (fold quote table off) | `VERDICT: PASS` | SURVIVES — real gap |
| N02 | h.py:37 | HEX_RE `\b[0-9a-f]{8,64}\b` -> `\b[0-9a-f]{4,64}\b` (8-hex lower bound -> 4) | `VERDICT: PASS` | SURVIVES — real gap |
| N03 | h.py:36 | SNAP_RE charset `[A-Za-z0-9._/-]+` -> `[A-Za-z0-9._/ -]+` (adds space) | `VERDICT: FAIL` (13 cases) | KILLED — but incidentally (see below) |
| N04 | h.py:38 | QUOTE_RE `{10,400}` -> `{1,400}` (both alternatives) | `VERDICT: PASS` | SURVIVES — equivalent (sweep below) |
| N05 | h.py:38 | QUOTE_RE `{10,400}` -> `{10,4000}` (both alternatives) | `VERDICT: PASS` | SURVIVES — real gap |
| N06 | h.py:110 | token window `<= 25` -> `<= 250` | `VERDICT: PASS` | SURVIVES — real gap |
| N07 | h.py:101 | `if not m or m.group(1) < MIN_VERIFIED:` -> `if not m:` (date floor dropped) | `VERDICT: FAIL` (T3_old_verified_at) | KILLED |
| N08 | h.py:88 | `re.split(r'[,;]', cells[11])` -> `re.split(r',', cells[11])` (semicolon separator dropped) | `VERDICT: PASS` | SURVIVES — real gap |
| N09 | h.py:74 | `len(cells) != 13` -> `len(cells) < 13` (13-cell equality -> lower bound) | `VERDICT: PASS` | SURVIVES — real gap |
| N10 | h.py:33 | ROW_RE `^ {0,3}\|` -> `^\s*\|` (indent bound removed) | `VERDICT: PASS` | SURVIVES — real gap |
| N11 | h.py:124 | `if not path.endswith('.md'):` -> `if False:` (.md scan filter off) | `VERDICT: PASS` | SURVIVES — real gap |
| N12 | h.py:37 | HEX_RE `\b[0-9a-f]{8,64}\b` -> `[0-9a-f]{8,64}` (word boundaries dropped) | `VERDICT: PASS` | SURVIVES — real gap |
| N13 | h.py:39 | CITE_RE `\bS\d{3,}\b` -> `S\d{3,}` (word boundaries dropped) | `VERDICT: PASS` | SURVIVES — real gap |
| N14 | h.py:123 | `tree.ls('corpus/knowledge/')` -> `tree.ls('corpus/')` | `VERDICT: FAIL` (10 cases) | KILLED |
| N15 | h.py:74 | `cells[8] != 'mined'` -> `cells[8] not in ('mined', 'queued')` | `VERDICT: FAIL` (T8_queued_rows) | KILLED |
| N03b | h.py:36 | SNAP_RE charset `[A-Za-z0-9._/-]+` -> `[A-Za-z0-9._/-~]+` (surgical widening, adds `~`) | `VERDICT: PASS` | SURVIVES — real gap |

# Killed mutants (4) — observed mechanisms
- N07: dies exactly on `T3_old_verified_at` (entry `verified-at: 2026-10-24` now accepted). Clean kill; the MIN_VERIFIED comparison is covered.
- N15: dies exactly on `T8_queued_rows` (queued rows counted). Clean kill; the `cells[8]` status rule is covered.
- N14: `git ls-tree --name-only m corpus/` lists direct children (`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge`), so the nested `a.md`/`b.md` are never scanned (`corpus/knowledge` has no `.md` suffix) and entries=0 on every counting case. Killed, but by a cascade that breaks everything — this only shows the ls prefix matters, not that any fixture pins its exact value.
- N03 (INCIDENTAL KILL, severity LOW as a kill-quality finding): with a space in the charset, SNAP_RE greedily swallows the whole anchor cell `advanced.md deadbeef` (space + sha included) as the path, `tree.read` fails, and rows=0 on ALL fixtures — 13 unrelated cases die. Probe (probes.py `N03`): pristine on the good fixture `... rows=2 entries=2 indexed=2 ... C2_R45_PASS=true`; hN03 `... rows=0 entries=0 ... false`. So the kill says nothing about the charset rule itself. The surgical widening N03b (`~` added) passes `--selftest` (`C2_R45_SELFTEST: cases=20 failed=0` / `VERDICT: PASS`, rc=0) and flips a `we~ird.md` fixture: pristine `rows=0`, hN16 `rows=2 ... C2_R45_PASS=true`. The charset rule is genuinely unpinned.

# Equivalent survivor (1): N04 — QUOTE_RE lower char bound
Sweep argument (no distinguishing input exists): `entry_ok` (h.py:110) accepts a quote only when `6 <= len(quote.split()) <= 25`. Any 6-token quote has >= 11 chars (6 tokens + 5 separators), so every quote the token window could admit already matches `{10,400}`. Lowering to `{1,400}` only adds matches of 1–9 chars, and every <= 9-char quote has <= 5 tokens (a 6-token quote needs >= 11 chars) — all rejected by the token window. The two regexes therefore induce identical `entry_ok` verdicts for every input. Empirical spot-checks (probes.py): `N04a` 7-char quote `"defined"` — pristine and hN04 both `entries=0`; `N04b` 6-token 31-char quote — both `entries=2 ... C2_R45_PASS=true`. Verdict: equivalent, not a gap. (The 400-char upper bound is a different story — N05 below.)

# Real selftest gaps (11) — each with its demonstrated kill case
All runs below: `python3 probes.py` / `python3 probes2.py` (scratch repos; last stdout line of measure mode shown). Kill-case code = the fixture + an added selftest case asserting the pristine line; e.g. `('N01_curly_fold', <reg>, <files>, <ents>, idx, 'C2_R45_PASS=true')` appended to the HardCover2-style case list.

1. N01 — fold quote table (h.py:44-46). Gap: quotes containing typographic characters (’ “ ” nbsp) no longer match snapshots folded the other way.
   Fixture: snapshot `Alone-passing tests “don’t fail in isolation, a known mirage” here.`; entry quotes `"don't fail in isolation, a known mirage"`.
   Observed: pristine `... rows=2 entries=2 indexed=2 ... C2_R45_PASS=true`; hN01 `... entries=0 indexed=0 ... C2_R45_PASS=false`. FLIP.
   Kill-case code:
   ```python
   snap = 'Alone-passing tests “don’t fail in isolation, a known mirage” here.\n'.encode()
   h = hashlib.sha256(snap).hexdigest()[:8]
   reg = row('S256', 'advanced', both, h=h) + row('S257', 'primer', both, h=h)
   quote = "don't fail in isolation, a known mirage"   # straight apostrophe
   # assert pristine prints C2_R45_PASS=true; N01 prints C2_R45_PASS=false
   ```
2. N02 — HEX_RE 8-hex lower bound (h.py:37). Gap: a 4-hex anchor prefix counts as a digest pin.
   Fixture: anchors `...advanced.md <first-4-hex-of-digest>`. Observed: pristine `rows=0 ... false`; hN02 `rows=2 ... true`. FLIP.
   ```python
   reg = row('S256', 'advanced', both, h=digest[:4]) + row('S257', 'primer', both, h=digest[:4])
   # assert pristine prints rows=0; N02 prints rows=2
   ```
3. N03b — SNAP_RE charset (h.py:36). Gap: charset exclusions are unpinned; any widening that keeps alnum/`.`/`_`//`-` filenames parseable passes the selftest.
   Fixture: snapshot files named `we~ird.md` / `we~ird2.md`, anchors naming them. Observed: pristine `rows=0 ... false`; hN16 `rows=2 ... C2_R45_PASS=true`; hN16 `--selftest` = `VERDICT: PASS`. FLIP.
   ```python
   files = {SP + 'we~ird.md': snap, SP + 'we~ird2.md': snap}
   reg = row('S256', 'advanced', both, anchor=SP + 'we~ird.md ' + digest) + \
         row('S257', 'primer', both, anchor=SP + 'we~ird2.md ' + digest)
   # assert pristine prints rows=0; N03b prints rows=2
   ```
4. N05 — QUOTE_RE 400-char upper bound (h.py:38). Gap: a >400-char located quote (<= 25 tokens, e.g. a long verbatim sentence in a large snapshot) is invisible to the pristine counter; a mutant accepting it flips the verdict.
   Fixture: snapshot of 20 x 25-char tokens (520 chars); entry quotes the whole run. Observed: pristine `entries=0 ... false`; hN05 `entries=2 ... true`. FLIP.
   ```python
   tok = 'a' * 25
   snap = ((tok + ' ') * 19 + tok + '\n').encode()
   quote = (tok + ' ') * 19 + tok          # 520 chars, 20 tokens
   # assert pristine prints entries=0; N05 prints entries=2
   ```
5. N06 — 6..25 token window upper bound (h.py:110). Gap: quotes of >= 26 tokens (long verbatim excerpts) are accepted by a weakened window.
   Fixture: snapshot `w0 w1 ... w29`; entry quotes all 30 tokens. Observed: pristine `entries=0 ... false`; hN06 `entries=2 ... true`. FLIP.
   ```python
   line = ' '.join('w%d' % i for i in range(30))
   snap = (line + '\n').encode(); quote = line
   # assert pristine prints entries=0; N06 prints entries=2
   ```
6. N08 — used split on `,`/`;` (h.py:88). Gap: semicolon-separated used-by lists stop splitting; every entry of such a row becomes "not in used-by".
   Fixture: used-by cells `a.md; b.md`. Observed: pristine `entries=2 ... C2_R45_PASS=true`; hN08 `entries=0 ... false`. FLIP (this one kills the mutant from the PASS side).
   ```python
   reg = row('S256', 'advanced', ea + '; ' + eb) + row('S257', 'primer', ea + '; ' + eb)
   # assert pristine prints C2_R45_PASS=true; N08 prints C2_R45_PASS=false
   ```
7. N09 — 13-cell equality check (h.py:74). Gap: rows with 14+ cells (malformed/extra column) are counted.
   Fixture: both rows carry a trailing 14th cell ` extra |`. Observed: pristine `rows=0 ... false`; hN09 `rows=2 ... true`. FLIP.
   ```python
   reg = row('S256', 'advanced', both)[:-1] + ' extra |\n' + \
         row('S257', 'primer', both)[:-1] + ' extra |\n'
   # assert pristine prints rows=0; N09 prints rows=2
   ```
8. N10 — ROW_RE 0-3 space indent (h.py:33). Gap: rows indented >= 4 spaces (markdown code blocks) or tabs are counted.
   Fixture: both rows prefixed with 6 spaces. Observed: pristine `rows=0 ... false`; hN10 `rows=2 ... true`. FLIP. (T10 only exercises 2- and 3-space indents, which both sides accept.)
   ```python
   reg = ''.join('      ' + r for r in [row('S256', 'advanced', both), row('S257', 'primer', both)])
   # assert pristine prints rows=0; N10 prints rows=2
   ```
9. N11 — `.md` scan filter (h.py:124). Gap: non-`.md` files under corpus/knowledge/ are scanned and counted as entries. Note the used-by gate must list the file or the filter is never reached (my first fixture listed it nowhere and both sides refused it — corrected here).
   Fixture: `corpus/knowledge/c.txt` valid entry, listed in both rows' used-by, absent from the README index. Observed: pristine `entries=2 indexed=2 ... true`; hN11 `entries=3 indexed=2 ... false`. FLIP.
   ```python
   three = ea + ', ' + eb + ', corpus/knowledge/c.txt'
   reg = row('S256', 'advanced', three) + row('S257', 'primer', three)
   ents = {ea: entry, eb: entry, 'corpus/knowledge/c.txt': entry}
   # assert pristine prints C2_R45_PASS=true; N11 prints C2_R45_PASS=false
   ```
10. N12 — HEX_RE word boundaries (h.py:37). Gap: a digest embedded in a larger token (`x<digest>`) counts as a pin.
    Fixture: anchors `...advanced.md x<digest>`. Observed: pristine `rows=0 ... false`; hN12 `rows=2 ... true`. FLIP.
    ```python
    reg = row('S256', 'advanced', both, anchor=SP + 'advanced.md x' + digest) + \
          row('S257', 'primer', both, anchor=SP + 'primer.md x' + digest)
    # assert pristine prints rows=0; N12 prints rows=2
    ```
11. N13 — CITE_RE word boundaries (h.py:39). Gap: a row id embedded in a token (`XS256`) counts as a citation.
    Fixture: entries with line 1 `source: XS256 — upstream`. Observed: pristine `entries=0 ... false` (REFUSED, cites no googletest row); hN13 `entries=2 ... true`. FLIP.
    ```python
    ents = {ea: entry_with_cite('XS256'), eb: entry_with_cite('XS256')}
    # assert pristine prints entries=0; N13 prints entries=2
    ```

# Severity summary (findings name what they attack)
- HIGH (selftest coverage gaps that would let a future counter regression pass silently): N01 fold table, N05 QUOTE_RE upper bound, N06 token window, N08 used-split. These guard the quote-locating/used-by rules — the core of the C3 evidence chain.
- LOW (edge-of-surface gaps; counts change only on malformed or exotic inputs): N02, N03b (and the incidental N03 kill), N09, N10, N11, N12, N13.
- INFO: N04 is an equivalent mutant (argued + spot-checked); N14/N07/N15 are genuine kills, of which N14 dies by cascade rather than by a pinned rule value.
- Nothing BLOCKING: the C2 claim as stated (killed >= 23/25 declared, 6 neutrals survive, pristine passes) is unaffected by this attack; these are coverage findings against the undeclared rule surface, not contract violations. The pristine counter at CONTENT rev passes its selftest (`cases=20 failed=0`, `VERDICT: PASS`).

# Restoration evidence
- Working copy never mutated in place; each mutant lived in its own copy (`hN01.py`…`hN16.py`).
- `sha256sum h.py` -> `200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9` (after all runs) = the copy taken from the lane = `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/hardening/coverage-counter.py` -> `200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9`. Lane bytes identical before/after the seat.
