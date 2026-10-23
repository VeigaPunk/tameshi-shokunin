# SrcBashExit — round 32, wave 1

Axis: operability.

## Verdict

Draft S097 is grounded by the official GNU Bash 5.3 manual source at pinned commit `b8c60bc9ca365f8261fa97900b6fa939f6ebc303`. The requested canonical HTML page timed out on direct retrieval; its byte size and digest are therefore unavailable. I opened and hashed the matching manual source file from Savannah instead. It states the full 0–255 status range and the special 126, 127, and 128+N cases. L1 should retain the access caveat when committing the row.

## Finding and Gate

The frozen registry at `c31814978969a41a8e9b0f7d99fa308c5993c1b7` has S094–S096 and names S097 as next unused. The requested URL was absent from both the working registry and the frozen registry snapshot.

Gate — URL: https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html; access attempt date: 2026-10-23 UTC. The canonical HTML fetch returned HTTP 000 / connection timeout, so no HTML bytes or digest are claimed. Verbatim quote (19 words): “Exit statuses fall between 0 and 255, though, as explained below, the shell may use values above 125 specially.” — §Exit Status, `@node Exit Status`, source lines 3896–3897. Verified in the official Bash 5.3 source file at pinned Savannah URL below.

The same section says fatal signal N maps to 128+N (line 3912), a missing command returns 127 (lines 3914–3915), and a found but non-executable command returns 126 (line 3916). This grounds the oracle's exhaustive status domain; it does not constitute execution evidence for the audit tool or counter.

## Evidence and provenance

- URL duplicate check: `functions.grep` with pattern `https://www\.gnu\.org/software/bash/manual/html_node/Exit-Status\.html` against `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` returned `No matches found.` The same search against the frozen `git show` artifact also returned `No matches found.`
- Frozen registry read: `timeout 20s git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c31814978969a41a8e9b0f7d99fa308c5993c1b7:corpus/SOURCES.md` completed. Its S094–S096 rows and allocation note show `Next unused id: S097` (full command output artifact: `artifact://31248`).
- Canonical HTML retrieval command: `timeout 30s curl --fail --location --silent --show-error --output Exit-Status.html --write-out 'http=%{http_code} effective=%{url_effective}\n' https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html` (run in this seat's scratch directory). The command timed out at 30 seconds, exit 124; it produced no source body. A retry with `--connect-timeout 20 --max-time 90` returned `curl: (28) Connection timed out after 20001 milliseconds`, `http=000`, exit 28. An IPv4 retry timed out after 8001 ms, and the `https://gnu.org/...` alias timed out after 10001 ms. The static reader also timed out on the canonical URL.
- Opened and pinned upstream manual source with: `timeout 15s curl --fail --location --silent --show-error --max-filesize 2000000 --connect-timeout 8 --max-time 13 --output bashref-5.3.texi --write-out 'http=%{http_code} effective=%{url_effective}\n' 'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303'` (run in this seat's scratch directory). Observed: `access_date_utc=2026-10-23`; `http=200`; `curl_exit=0`; `bytes=415804`; SHA-256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`.
- Savannah's `doc/bashref.texi` history identifies that commit as the Bash-5.3 distribution sources and documentation, dated 2025-07-03. `doc/version.texi` states version 5.3 and update date 18 May 2025 (fetched 2026-10-23 UTC; 210 bytes; SHA-256 `ad57e14bc98393c94822f8e75b2e103d683862ba5e2810c9fb3d0f93e02d6cb4`).
- The opened source section is `@node Exit Status` / `@subsection Exit Status`, lines 3890–3916. No code, build, test, lint, formatter, or runner check was performed.

## Draft SOURCES row for L1

```text
| S097 | GNU Bash Reference Manual: Exit Status — https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html | docs | A | Bash command exit-status range and the documented special statuses used to ground the tally oracle's 0–255 domain | §Exit Status (`@node Exit Status`, lines 3890–3916) @ Bash 5.3, commit b8c60bc9ca365f8261fa97900b6fa939f6ebc303; official `doc/bashref.texi` fetched 2026-10-23 UTC (415804 bytes; SHA-256 f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5); canonical HTML fetch timed out | Bash exit statuses cover 0–255; a fatal signal N maps to 128+N, a missing command to 127, and a found but non-executable command to 126 | mined | 2026-10-23 | on-release | tools/tally-audit.py; corpus/knowledge/runner-tally-audit.md |
```

## Touched surfaces, scope, and artifacts

- Repo write: this report only — `.ufo/waves/round-32/w1/SrcBashExit.md`. The L1 commits the SOURCES row; `corpus/SOURCES.md`, `tools/tally-audit.py`, and the mutation runner were not edited.
- Scratch source artifacts: `/fast/scratch/hyaku/tameshi-r32-seats/SrcBashExit/bashref-5.3.texi`, `bashref.texi`, and `version.texi`. No tool was installed.
- Out of scope: implementing or running `tally-audit.py`, auditing runner copies, and executing regression or selftest gates. Those results are not claimed here.
- Report artifact: `.ufo/waves/round-32/w1/SrcBashExit.md`.