seat: ExecRows12
# C1 freshness — rows S069, S070 (author re-verification)

Both rows fetched live 2026-10-25; both verdicts `holds`; both fragments passed the frozen counter's `--check` at `--rev 3310e7be803516ca5934b4e949d91bcec824b179` with `CHECK <id> verified ok`.

## S069 — Linux man-pages: setsid(2)
- URL: https://man7.org/linux/man-pages/man2/setsid.2.html
- curl: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S069.raw '<url>'` → exit 0
- bytes: 11555 ; sha256: `52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30`
- extract: `python3 .ufo/evidence/round-45/freshness/measure.py --extract S069.raw` → 633 words; anchor §DESCRIPTION ¶2 and §ERRORS EPERM still present
- CHECK: `CHECK S069 verified ok` (exit 0)
- note: DESCRIPTION still states the caller becomes the only process in the new group and session, grounding the teaches claim.
- fragment (verbatim):

```json
{"id":"S069","url":"https://man7.org/linux/man-pages/man2/setsid.2.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30","quote":"The calling process will be the only process in the new process group and in the new session.","snapshot":".ufo/evidence/round-45/freshness/sources/S069.raw.gz","author":"ExecRows12","note":"DESCRIPTION still states the caller becomes the only process in the new group and session, grounding the teaches claim."}
```

## S070 — Pro Git, 2nd ed., §10.8 Environment Variables
- URL: https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables
- curl: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S070.raw '<url>'` → exit 0
- bytes: 139144 ; sha256: `19fc78ffa39058c17ed038f2270855dcbb7055fe70c129f9a33b9c94a5566d95`
- extract: `python3 .ufo/evidence/round-45/freshness/measure.py --extract S070.raw` → 2355 words; anchor §10.8 subsection Repository Locations still present
- CHECK: `CHECK S070 verified ok` (exit 0)
- note: Repository Locations subsection still says GIT_DIR names the .git folder and Git walks up the tree when unset, grounding the teaches claim.
- fragment (verbatim):

```json
{"id":"S070","url":"https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables","opened":"2026-10-25","verdict":"holds","raw_sha256":"19fc78ffa39058c17ed038f2270855dcbb7055fe70c129f9a33b9c94a5566d95","quote":"GIT_DIR is the location of the .git folder. If this isn't specified, Git walks up the directory tree until it gets to ~","snapshot":".ufo/evidence/round-45/freshness/sources/S070.raw.gz","author":"ExecRows12","note":"Repository Locations subsection still says GIT_DIR names the .git folder and Git walks up the tree when unset, grounding the teaches claim."}
```

## Scratch/artifact locations
- Raw live bytes kept for L1 integration: `/tmp/tameshi-r45-ExecRows12/S069.raw`, `/tmp/tameshi-r45-ExecRows12/S070.raw`
- Folded extract text: `/tmp/tameshi-r45-ExecRows12/S069.fold.txt`, `/tmp/tameshi-r45-ExecRows12/S070.fold.txt`
- Fragments: `/tmp/tameshi-r45-ExecRows12/S069.json`, `/tmp/tameshi-r45-ExecRows12/S070.json`

No tools installed; no lane mutation beyond this report; contract read-only; URL byte-exact from the row source cells; quotes located afresh in live fetch (not copied from row cells).
