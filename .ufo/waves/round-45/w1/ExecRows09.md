seat: ExecRows09

# Round-45 w1 — C1 freshness re-verification: S061, S076, S062 (author)

Item: C1 row re-verification for rows S061, S076, S062. All three fetched live on 2026-10-25, quotes located afresh in the counter's `--extract` normalized text (never from registry cells), fragments graded with the round-45 freshness counter `--check` against freeze rev 3310e7be803516ca5934b4e949d91bcec824b179.

No tool installs were made (existing system `curl`, `python3` used; channel: none).

## S061
- URL: https://docs.jj-vcs.dev/latest/git-compatibility/ (row's first http(s) URL in source cell, byte-exact)
- curl: exit 0 (-fsSL -A 'Mozilla/5.0' --max-time 90)
- bytes: 61334, sha256: db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254
- CHECK: `CHECK S061 verified ok` (exit 0)
- note: The conversion-recipe shell comment in the row's anchor still says HEAD is pointed at the working-copy commit's parent, grounding the teaches claim that jj leaves Git detached there.
- Fragment JSON:
```json
{"id":"S061","url":"https://docs.jj-vcs.dev/latest/git-compatibility/","opened":"2026-10-25","verdict":"holds","raw_sha256":"db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254","quote":"Convince jj to update .git/HEAD to point to the working-copy commit's parent","snapshot":".ufo/evidence/round-45/freshness/sources/S061.raw.gz","author":"ExecRows09","note":"The conversion-recipe shell comment in the row's anchor still says HEAD is pointed at the working-copy commit's parent, grounding the teaches claim that jj leaves Git detached there."}
```

## S076
- URL: https://docs.jj-vcs.dev/latest/git-compatibility/ (row's first http(s) URL in source cell, byte-exact)
- curl: exit 0 (-fsSL -A 'Mozilla/5.0' --max-time 90)
- bytes: 61334, sha256: db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254
- CHECK: `CHECK S076 verified ok` (exit 0)
- note: Paragraph 3 of the Colocated workspaces section still contains the detached-HEAD statement the row supersedes S061 to point at, so the row holds.
- Fragment JSON:
```json
{"id":"S076","url":"https://docs.jj-vcs.dev/latest/git-compatibility/","opened":"2026-10-25","verdict":"holds","raw_sha256":"db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254","quote":"One reason for this (see below for more) is that jj commands will usually put the Git repo in a \"detached HEAD\" state","snapshot":".ufo/evidence/round-45/freshness/sources/S076.raw.gz","author":"ExecRows09","note":"Paragraph 3 of the Colocated workspaces section still contains the detached-HEAD statement the row supersedes S061 to point at, so the row holds."}
```

## S062
- URL: https://git-scm.com/docs/git-rev-parse (row's first http(s) URL in source cell, byte-exact)
- curl: exit 0 (-fsSL -A 'Mozilla/5.0' --max-time 90)
- bytes: 122331, sha256: 9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978
- CHECK: `CHECK S062 verified ok` (exit 0)
- note: The OPTIONS entry for --show-toplevel still defines it as reporting the working-tree top-level path, grounding the teaches claim that it reports the discovered top-level.
- Fragment JSON:
```json
{"id":"S062","url":"https://git-scm.com/docs/git-rev-parse","opened":"2026-10-25","verdict":"holds","raw_sha256":"9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978","quote":"--show-toplevel Show the (by default, absolute) path of the top-level directory of the working tree","snapshot":".ufo/evidence/round-45/freshness/sources/S062.raw.gz","author":"ExecRows09","note":"The OPTIONS entry for --show-toplevel still defines it as reporting the working-tree top-level path, grounding the teaches claim that it reports the discovered top-level."}
```

## Evidence / status
- All three rows: verdict `holds`, CHECK lines all `verified ok`, exit 0.
- Raw snapshots retained at /tmp/tameshi-r45-ExecRows09/S061.raw, S076.raw, S062.raw (same sha256 as fragment `raw_sha256`; S061/S076 share the same URL and byte-identical fetch).
- No blockers; no verdict `drifted`/`unreachable`.
