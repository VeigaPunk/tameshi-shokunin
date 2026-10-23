# SrcBashCase — S098 source lookup

## Verdict

Blocked: the requested GNU Bash manual page could not be opened. No S098 row or Gate quote is emitted; inventing opened-date, byte-count, digest, or quoted text would break the SOURCES contract.

## Behavior

No product behavior was exercised or changed. This seat was limited to source lookup and report preparation.

## Gates and evidence

- URL lookup first: `functions.grep` for `https://www\.gnu\.org/software/bash/manual/html_node/Conditional-Constructs\.html` in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` returned `No matches found.`
- Read `/home/vgpnk/Projects/shokunin/CORPUS.md:64-115`: SOURCES requires an 11-column row; rule 1 requires the round Gate to record the URL, access date, and a quote of at most 25 words with its location.
- Read the frozen registry using `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c31814978969a41a8e9b0f7d99fa308c5993c1b7:corpus/SOURCES.md`. Its header and rows S094–S096 were inspected; the header is `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.
- Attempted the requested capture from the owned scratch directory:
  `timeout 45s curl --fail --location --silent --show-error --max-time 40 'https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html' -o bash-reference.html && printf 'URL=https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html\nACCESS_UTC=' && date -u '+%Y-%m-%dT%H:%M:%SZ' && printf 'BYTES=' && wc -c < bash-reference.html && printf 'SHA256=' && sha256sum bash-reference.html`
  Outcome: exit 28; `curl: (28) Connection timed out after 40000 milliseconds`.
- Retried with IPv4 and a shorter connection timeout:
  `timeout 30s curl --ipv4 --fail --location --silent --show-error --connect-timeout 8 --max-time 25 'https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html' -o bash-reference.html && printf 'URL=https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html\nACCESS_UTC=' && date -u '+%Y-%m-%dT%H:%M:%SZ' && printf 'BYTES=' && wc -c < bash-reference.html && printf 'SHA256=' && sha256sum bash-reference.html`
  Outcome: exit 28; `curl: (28) Connection timed out after 8001 milliseconds`.
- The static reader also failed on the same URL: `Method: failed`; `Cause: The operation timed out.` `getent ahosts www.gnu.org` resolved `2001:470:142:5::116` and `209.51.188.116`. A verbose curl diagnostic showed attempts to both addresses and `Connection timed out after 5001 milliseconds` (exit 28); `HTTPS_PROXY`, `HTTP_PROXY`, and `ALL_PROXY` were empty.
- The capture artifact is empty: `wc -c` reported `0`; SHA-256 was `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Touched surfaces

- This report: `.ufo/waves/round-32/w1/SrcBashCase.md`.
- Scratch capture path: `/fast/scratch/hyaku/tameshi-r32-seats/SrcBashCase/bash-reference.html` (0 bytes; failed fetch).
- No corpus, production, or other repository files were changed.

## Out of scope

No source row or Gate line was drafted without a successful open. No tool was installed; no runner, tests, or build were run.

## Findings

The URL was not already in the registry, but outbound HTTPS to `www.gnu.org` timed out for both resolved addresses, and the reader timed out too. Therefore no verified quote, page anchor, successful access date, byte size, or source digest is available. S098 remains unrecorded pending an accessible source fetch.

## Artifact paths

- Report: `.ufo/waves/round-32/w1/SrcBashCase.md`
- Failed source capture: `/fast/scratch/hyaku/tameshi-r32-seats/SrcBashCase/bash-reference.html`
