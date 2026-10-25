seat: ExecRows08

# C1 rows S058, S059, S060, S075 — live re-verification (author ledger entries)

Round 45, hyaku run 7, attempt 1. Fragments staged in `/tmp/tameshi-r45-ExecRows08/`; `.raw` files kept there for L1 integration. All four `--check` runs against freeze rev `3310e7be803516ca5934b4e949d91bcec824b179` printed `verified ok` (exit 0). One check command per row:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 3310e7be803516ca5934b4e949d91bcec824b179 \
  --check /tmp/tameshi-r45-ExecRows08/S###.json --snapdir /tmp/tameshi-r45-ExecRows08
```

## S058 — Build Systems à la Carte (published PDF)

- Row: `corpus/SOURCES.md:67`.
- URL: `https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf`
- curl attempt 1 (UA `Mozilla/5.0`): exit 22 — `curl: (22) The requested URL returned error: 403`; retry with browser UA (Chrome 126): exit 0, http=200, bytes=728559.
- `sha256sum`: `d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede` — matches the anchor's published-PDF hash; `file`: PDF 1.5, 29 pages.
- Extract: `python3 .../measure.py --extract .../S058.raw` exit 0 (101696 bytes). §4.2.2 Verifying Traces (col ~47150): `...record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must be rebuilt ś in essence a trace which we can use to verify existing values.`
- Quote: `a trace which we can use to verify existing values` (10 tokens; shares trace/verify/existing/values with teaches/scope).
- CHECK output: `CHECK S058 verified ok`
- Note: live PDF sha256 equals the anchored published-PDF hash; §4.2.2 still describes verifying an existing value via a recorded-input trace.

```json
{"id":"S058","url":"https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf","opened":"2026-10-25","verdict":"holds","raw_sha256":"d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede","quote":"a trace which we can use to verify existing values","snapshot":".ufo/evidence/round-45/freshness/sources/S058.raw.gz","author":"ExecRows08","note":"Live PDF sha256 matches the anchored published-PDF hash; section 4.2.2 Verifying Traces still describes recording dependency hashes and verifying an existing value via a trace, grounding the teaches claim."}
```

## S059 — Bazel Remote Caching docs

- Row: `corpus/SOURCES.md:68`.
- URL: `https://bazel.build/remote/caching`
- curl exit 0 (UA `Mozilla/5.0`), bytes=250675.
- `sha256sum`: `c9653cfb149e45d3c2bfdc54b56dc21ae508040e1e29db9c06b138433ebd55c7`
- Extract: exit 0 (79102 bytes). Known issues section (col ~14704) retains heading `Bazel does not track tools outside a workspace` and body: `Bazel currently does not track tools outside a workspace. This can be a problem if, for example, an action uses a compiler from /usr/bin/ . Then, two users with different compilers installed will wrongly share cache hits because the outputs are different but they have the same action hash. See issue #4558 for updates.`
- Quote: `Bazel currently does not track tools outside a workspace` (9 tokens; shares track/tools/outside/workspace with anchor+scope).
- CHECK output: `CHECK S059 verified ok`
- Note: Known issues section still documents the false-hit class for inputs outside the key.

```json
{"id":"S059","url":"https://bazel.build/remote/caching","opened":"2026-10-25","verdict":"holds","raw_sha256":"c9653cfb149e45d3c2bfdc54b56dc21ae508040e1e29db9c06b138433ebd55c7","quote":"Bazel currently does not track tools outside a workspace","snapshot":".ufo/evidence/round-45/freshness/sources/S059.raw.gz","author":"ExecRows08","note":"Known issues section still documents that Bazel does not track tools outside a workspace, the row's documented false-hit class for inputs outside the key."}
```

## S060 — strace(1) man7 page

- Row: `corpus/SOURCES.md:69`.
- URL: `https://man7.org/linux/man-pages/man1/strace.1.html`
- curl exit 0, bytes=85238.
- `sha256sum`: `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6` (footer strace 7.1.0.62.c605d6 2026-06-25 unchanged).
- Extract: exit 0 (53082 bytes). §Filtering `%file` passage (col ~13082): `%file file Traces all system calls that take a file name as an argument. You can think of this as an abbreviation for --trace = open , stat , chmod , unlink ,...`
- Quote: `Traces all system calls that take a file name as an argument` (12 tokens; shares file/name with scope+teaches).
- CHECK output: `CHECK S060 verified ok`
- Note: man7 strace page still defines %file as tracing all system calls taking a file-name argument, grounding the teaches claim that file-name syscalls are observable per followed process.

```json
{"id":"S060","url":"https://man7.org/linux/man-pages/man1/strace.1.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6","quote":"Traces all system calls that take a file name as an argument","snapshot":".ufo/evidence/round-45/freshness/sources/S060.raw.gz","author":"ExecRows08","note":"The man7 strace page still defines %file as tracing all system calls that take a file name argument, grounding the teaches claim that file-name syscalls are observable per followed process."}
```

## S075 — strace(1) man7 page (supersedes S060's anchor)

- Row: `corpus/SOURCES.md:84`.
- URL: `https://man7.org/linux/man-pages/man1/strace.1.html` (same page as S060; fetched separately per row).
- curl exit 0, bytes=85238.
- `sha256sum`: `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6`
- Extract: exit 0 (53082 bytes). §Filtering `syscall_set` passage (col ~12284): `syscall Traces specific system call, specified by its name (see syscalls(2) for a reference, but also see NOTES ).`
- Quote: `syscall Traces specific system call, specified by its name` (9 tokens; shares syscall/specified/system with scope+anchor).
- CHECK output: `CHECK S075 verified ok`
- Note: §Filtering still defines syscall_set elements as specific system calls specified by name, grounding the superseding teaches that the collector passes an explicit syscall list rather than %file.

```json
{"id":"S075","url":"https://man7.org/linux/man-pages/man1/strace.1.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6","quote":"syscall Traces specific system call, specified by its name","snapshot":".ufo/evidence/round-45/freshness/sources/S075.raw.gz","author":"ExecRows08","note":"Section Filtering still defines syscall_set elements as specific system calls specified by name, grounding the superseding teaches that the collector passes an explicit syscall list rather than %file."}
```

## Tooling

No tool installed or updated. `pdftotext` 26.08.0 already present at `/usr/bin/pdftotext` (used by measure.py's PDF extraction); no pacman/uv/npx changes.

## Risks / notes

- S058 first fetch with default UA returned HTTP 403 (curl 22); retry with browser UA succeeded (http=200, exit 0), final artifact sha256 byte-identical to the anchored published-PDF hash.
- S060/S075 share one live URL; each row has its own raw artifact and fragment.
- No drifted/unreachable verdicts; all four rows `holds`, fresh against live bytes on 2026-10-25.
