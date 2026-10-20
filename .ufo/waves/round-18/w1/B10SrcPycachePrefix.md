# B10SrcPycachePrefix — round-18 wave 1 source row (C2 P06)

Verdict: built — S074 admitted as `mined` (tier A, docs), provisional id; row and Gate in `.ufo/waves/round-18/sources/S074-B10SrcPycachePrefix.md`.

## Commands and results
- `grep -rn 'using/cmdline\|PYTHONPYCACHEPREFIX\|PYTHONDONTWRITEBYTECODE' corpus/SOURCES.md` → no lines (duplicate check negative; the registry holds S001–S064 and no cmdline URL).
- `read https://docs.python.org/3/using/cmdline.html` → opened (Python 3.15.0 docs, 1309 reader lines).
- `curl -fsSL https://docs.python.org/3/using/cmdline.html -o …/cmdline.html && sha256sum` → exit 0, sha256 a4863a38223e1dab199e8eb0974915561c859b23dbacc8ecff76bb06e589b734.
- `grep -n 'envvar-PYTHON…'` → PYTHONDONTWRITEBYTECODE at line 1131, PYTHONPYCACHEPREFIX at line 1139.
- Stripped-tag text of lines 1131–1146 checked with `grep -F`: both quotes hit verbatim. Word counts (`wc -w`): 22 and 14, both ≤25.

## Findings
- PYTHONPYCACHEPREFIX: "Added in version 3.8." Writes .pyc in a mirror tree at the given path, equivalent to `-X pycache_prefix=PATH`.
- PYTHONDONTWRITEBYTECODE: non-empty value equals `-B`; the entry states write behaviour only.
- Scope limit: the served docs are the 3.15.0 dev build; the page states nothing about reads or child processes. Any claim beyond write location is [INFERENCE] and not in the row.

## Id and path notes
- Target's provisional id S074 used as instructed. The lane tip's SOURCES.md says "Next unused id: S065"; S065–S073 are unallocated in the file and the L1 must reconcile at integration.
- Used-by is provisional `.ufo/evidence/round-18/` (exists); the L1 should replace it with the citing path once the probe citation is written.
- Write scope: the Target owns only the S074 file; this report was written to the `Report:` trailer path as instructed. No other lane file touched. No installs. No git commands run in the lane.

## Not done
- No knowledge entry written (not in scope). No rejection (source supports the purpose).
