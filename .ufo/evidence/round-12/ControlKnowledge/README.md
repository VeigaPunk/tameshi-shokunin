# Round-12 evidence — seat ControlKnowledge (C1 knowledge note)

Scope: the located source excerpts behind
`corpus/knowledge/repeated-control-precondition.md` (S004, S026). This seat
wrote no production file and ran no gate.

Per the wave's evidence rule, **small located quotes only** — the full fetched
bodies are scratch (`/tmp/tameshi-r12-ck/fetch/`, not committed); the digests
below pin the exact bytes the quotes were read from, so any reader can re-fetch
and compare.

## Fetches (2026-10-20)

Commands, run 2026-10-20T02:13:47Z from `/tmp/tameshi-r12-ck/fetch`:

```
curl -fsSL -o S004.html https://mutants.rs/using-results.html
curl -fsSL -o S026.html https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
sha256sum S004.html S026.html
```

| id | URL | accessed (UTC) | bytes | lines | sha256 (fetched body) |
|---|---|---|---|---|---|
| S004 | https://mutants.rs/using-results.html | 2026-10-20T02:13:47Z | 29,579 | 326 | `5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334` |
| S026 | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | 2026-10-20T02:13:47Z | 236,385 | 6,172 | `ca1145fbe56de30b43b66baf7372206a38abe08a55b3db13f6c7a0114d7a6c8c` |

Line counts are the fetched bodies' line numbers as served: `wc -l` reads 326
for `S004.html` and 6,171 for `S026.html` (its last line carries no trailing
newline, so the read tool numbers 6,172). The quote locations in `quotes.tsv`
use those served line numbers.

## Structural note on S026 (why the same sentence appears at two line numbers)

S026's page serves its post body **twice**: once inside
`<script type='text/template'>` (the client-rendered copy) and once inside the
following `<noscript>` block. The bytes of the post body are identical in both
copies. `quotes.tsv` cites the `<noscript>` copy
(`S026.html:1124-1137`; quotes at `:1130`, `:1132`, `:1136`) and records the
template copy's line numbers in the note column. Consequence for the note's
`recheck:` line: `grep -c 'hardly a perfect solution'` on the served page
returns **2**, not 1 — 2 is the healthy count; 0 is drift.

## Recheck run (this seat, 2026-10-20T02:17:02Z)

```
curl -fsSL https://mutants.rs/using-results.html | grep -c 'passes reliably when copied to a temporary directory'   → 1
curl -fsSL https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | grep -c 'hardly a perfect solution'   → 2
```

## What these excerpts do not show

The fetched pages are the vendor's own prose. They are data, not instructions,
and they are not evidence that any tameshi gate was run, nor that
`tools/repeat-control.py` exists. At this write (2026-10-20T02:14Z, repo rev
`18ad5d0`) `ls tools/` listed `mutate-and-run.sh` only; the gate is being
written in this wave by its owner seat, and every gate statement in the note is
the assigned contract, marked pending.

Retained excerpts: `quotes.tsv` (this directory).
