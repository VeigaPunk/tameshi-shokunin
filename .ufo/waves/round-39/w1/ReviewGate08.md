# ReviewGate08 — census attack on `tools/mutate-and-run.sh` (r39 W1, gate attack)

Assignment: find one write the frozen census pattern misses in
`tools/mutate-and-run.sh`, or state that the pattern's named limits cover it.
No lane files were edited; all evidence is from REV bytes materialized to
scratch (`/tmp/tameshi-r39-ReviewGate08/`).

## Method

- Extracted `tools/write-path-census.py` and `tools/mutate-and-run.sh` from
  lane HEAD `233077f88d7a8d142eff329202a120457a5d5258` via `git show`. Census
  blob sha256 `bc8c660c…7edc62` — equals the contract pin
  (`contract.json claims.C2.tool_sha256`), so the frozen pattern audited here
  is the pinned one. Target blob sha256 `a7d3f2dd…12eb9`.
- Loaded the pinned census module (importlib, same mechanism as
  `census/measure.py:63-67`) and ran its own `WRITE_RE` / `classify_text` over
  the REV bytes — no reimplementation.
- Swept a superset detector (any `open(`, `.write(`, `.write_text`,
  `.write_bytes`, `fdopen`, `os.replace/rename`, `shutil.*`, `json.dump`,
  redirects, heredocs, `cp/mv/mkdir/mktemp/chmod/rm/ln/touch/tee/dd/install/
  truncate`, `sed -i`, `perl -i`, `git init/add/commit/checkout/restore/apply`)
  and hand-attributed every non-prose hit to a root.

## Ground truth (frozen pattern, REV bytes)

- `WRITE_RE` matches exactly **one** line:
  `tools/mutate-and-run.sh:429` — `with open(mutant, 'wb') as fh:` (the
  mutant-write inside the embedded Python spec helper heredoc).
- `classify_text` → `write_sites=1 unflagged=0`. `EXPECTED_RE` hits 0 lines in
  the file (no `.expected`/`expected.txt`/`golden`/`snapshot` string anywhere);
  `FLAG_RE` absent (irrelevant, since no write line names an expected file).
  `unflagged=0` is therefore structural, not incidental.
- End-to-end run of the pinned tool over a materialized 21-gate REV root:
  `WRITE_CENSUS: gates=21/21 live_write_sites=99 live_unflagged=0 missing=0`,
  row `GATE mutate-and-run.sh write_sites=1 unflagged=0 sha256=a7d3f2dd…`.

## Verdict: the pattern's named limits cover this gate — no falsifying miss found

Every write in `mutate-and-run.sh` other than the counted `:429` site falls
inside a limit the census names in its own docstring
(`tools/write-path-census.py:9-10`): *"This is not a full lexer and not a claim
that every write in every language is seen. Shell redirects and writes whose
path is not on the same line as the call are outside the frozen patterns."*

- **Shell redirects / heredocs (named limit 2):** 57 real write redirects, every
  target a scratch-rooted variable or fd-dup — `$WORKDIR/defects.tsv` (:509),
  `$WORKDIR/results.tsv` (:539/:554), nine embedded spec heredocs `cat
  >"$d/*.spec" <<'EOT'` (:661-:1084), blob materialization `git_clean -C
  "$repo" show "${rev}:${path}" >"$dst"` (:1204), `>"$cwd/sweep.log"` (:1250),
  selftest fixtures `cat >"$fx/target.sh" <<'EOT'` (:1495, :1510, :1530, :1537,
  :1547, :1554, :1561, :1673, :1788, :1803, :1820), run logs `>"$root/rg*.out"`
  (:1630-:1919), canary/canary-fixture markers (:1893, :1898), tally harness
  (:2003). `>"$2"` (:456) is run_one's evidence file, passed by callers as
  `$WORKDIR/evidence/<id>.out`. `>/dev/null`, `>&2`, `2>&1` are fd ops.
- **Cross-line path binding (named limit 2):** `fh.write(result)` at
  `:430` binds its path at the counted `:429` open two lines up — one logical
  write site, counted once. No distinct write path escapes uncounted.
- **Python heredoc reads:** `open(path, encoding='utf-8')` (:349),
  `open(pristine, 'rb')` (:418) — reads; `sys.stdout/stderr.write` (:324, :409,
  :425, :433, :437) — streams, not files.
- **Non-language fs ops (blanket clause, docstring line 9):** `mkdir -p` ×11
  (:484, :487, :1171, :1364, :1367, :1493, :1743, :1857, :1892, :1897, :1944),
  `chmod` ×7 (:1224, :1508, :1526, :1535, :1683, :1799, :1831), `cp` ×5 (:492,
  :510, :516, :1744, :1858-1859), `rm -rf` ×2 (:1466, :2049) — every argument
  scratch-rooted (`$WORKDIR`/`$EVID`/`$cwd`/`$dst`/`$root`/`$fx`/`$grepo`/
  `$super`/`$canary`/`$cdr`/`$lspecs`), all under `mktemp -d /tmp/…` (:482,
  :1360, :1477) or caller `--workdir`.
- **Git plumbing writes (blanket clause):** `fixture_commit`'s `init/add/commit`
  (:291-298) only ever receives scratch repos ($grepo/$super/$canary/$cdr), and
  the r17 `GIT_*` scrub (:271-281) plus its canary arm (:1899) is the dedicated
  guard proving those writes cannot land outside the fixture.

No `sed -i`, `perl -i`, `tee`, `dd`, `install`, `truncate`, `ln`, `mv`, or
`python3 -c`-embedded write exists anywhere in the file. No redirect target is
a literal path outside `/tmp` or the scratch variables.

## Findings by severity

**None (no falsifying miss in scope).** The classification
`write_sites=1 unflagged=0` for `tools/mutate-and-run.sh` is faithful to the
frozen pattern's declared semantics, and the assignment's second branch holds:
the named limits cover what the pattern does not count.

## Residual risk (boundary of the named limits — recorded, not a miss)

1. `cp`/`mkdir`/`mktemp`/`chmod`/`rm`/git-plumbing writes are covered only by
   the docstring's blanket clause (line 9), not by the two named exclusions.
   They are safe here purely because every argument is scratch-rooted. A future
   revision repointing e.g. `cp -p "$TARGET_ABS" "$PRISTINE"` (:492) at a
   lane expected-file would be a real expected-value write the census stays
   silent on, and neither named exclusion would cover it.
2. Latent pattern hole (general census, absent from this gate): `WRITE_RE`'s
   `open\s*\([^)]*['"]w…['"]` cannot cross a `)` in the first argument, so a
   same-line `open(os.path.join(d, 'case.expected'), 'w')` is a Python write
   missed by the pattern and covered by neither named exclusion (path is on the
   same line; not a redirect). This file's only opens are :349, :418, :429 —
   none of that shape.
3. The census counts pattern-matching *lines*, not logical sites; the
   :429/:430 pair is one write counted once. Harmless here; a handle `.write(`
   opened by a matched `open(` on a distant line would blur line-vs-site
   accounting.
4. Classification is REV-bound, not live-tree-bound:
   `census/measure.py:88-103` materializes each gate from REV via `git show`.
   My row is against HEAD `233077f`; if the executor lands further commits
   before the deciding run, the census re-reads those bytes and the per-gate
   `sha256=` row moves with them. The predicate (21/21 classified, planted
   controls, FLAG_GATE mutation) is drift-tolerant by construction, but the
   printed `live_write_sites` total is whatever the landing REV says.

## Verification gaps

- No `lsp` server answers for a `.sh` target in this seat's inventory; all
  caller/definition checks here are mechanical enumeration over REV bytes, not
  semantic analysis. That is inherent to attacking a lexical census.
- I did not run `census/measure.py` end-to-end (the deciding run is reserved by
  the contract kill_rule; base rev must stay `C2_R39_PASS=false`). I verified
  the census leg of the predicate — 21/21 gates classified from REV bytes,
  tool sha equals the pin — independently.
- Attributions of "all targets scratch-rooted" rest on reading every
  redirect/fs-op line of this file (listed above) and the definitions of the
  root variables, not on executing the tool.
