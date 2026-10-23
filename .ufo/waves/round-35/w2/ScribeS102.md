# ScribeS102 — S102 registry-row audit

## Scope and result

Attacked only the S102 row in `corpus/SOURCES.md` against the read-only dispatch snapshot `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. I checked its source identity, anchor and teaching summary against the committed POSIX HTML, then checked the `used-by` paths against that revision. I did not attack C1 runtime behavior or mutate any lane artifact.

**CRITICAL — false `used-by` path.** `corpus/SOURCES.md:110` lists `corpus/lessons/round-35.md`, but that file is absent at the dispatch pin: `git cat-file -e 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:corpus/lessons/round-35.md` returned exit 128, `fatal: path 'corpus/lessons/round-35.md' does not exist in '7da6e076c2e25936a3b60dde2a4080d8f05b7e5b'`. The row-change prose at `corpus/SOURCES.md:412-418` repeats the same nonexistent backlink. The real code consumer is `tools/tally-audit-v3.py:29-32`, whose docstring explicitly attributes the comment rule to S102. The contract also has a `sourced_by` attribution at `.ufo/evidence/round-35/contract.json:42`; this is not added as a `used-by` consumer, consistent with the neighboring S097 row at `corpus/SOURCES.md:106` (which likewise lists its tool and knowledge consumer, not the contract attribution).

**No other row cell was falsified.** The source snapshot is POSIX.1-2024 Shell Command Language §2.3, `tag_19_03`; its sentence at HTML lines 303-304 says `#` and subsequent characters through (excluding) the next newline are discarded as a comment. This supports the row's anchor and paraphrase. `corpus/SOURCES.md:110` records URL `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html`, kind `spec`, tier `A`, status `mined`, opened `2026-10-23`, and recheck `365d`. The row's recorded fetch date, byte count and digest match the source record: snapshot size 357,953 bytes and SHA-256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`. The URL reader also returned the Shell Command Language page with §2.3 Token Recognition. Opened/recheck are registry metadata; I did not independently reconstruct the original fetch timestamp or recheck policy.

## Corrected row text

```text
| S102 | POSIX.1-2024 Shell Command Language, §2.3 Token Recognition — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | spec | A | the normative rule that makes a `#` start a comment and where the comment ends | §2.3 Token Recognition, the `#` sentence @ page fetched 2026-10-23 UTC (357,953 bytes; SHA-256 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd; committed snapshot .ufo/evidence/round-35/src/s102-posix-chap02.html) | a `#` at the point a token begins discards that character and all up to (excluding) the next newline as a comment, so comment text is never code — the ground for blanking comments before structural scans | mined | 2026-10-23 | 365d | tools/tally-audit-v3.py |
```

## Commands, outcomes, provenance

The specified setup command was attempted verbatim:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane checkout -q --detach 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```

It exited 128: `fatal: destination path '/fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane' already exists and is not an empty directory.` I left that existing path untouched; its read-only `HEAD` was `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`, not the requested dispatch pin. I instead created a separate scratch clone at `lane-dispatch-pin` with the same clone/checkout operations and the requested commit; the command exited 0 with no output. The read-only pin check

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin rev-parse HEAD
```

exited 0 and printed `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.

Byte evidence from the dispatch snapshot:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/corpus/SOURCES.md /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/.ufo/evidence/round-35/contract.json /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/tools/tally-audit-v3.py /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/.ufo/evidence/round-35/src/s102-posix-chap02.html
```

Exit 0; SHA-256s, in command order:

- `corpus/SOURCES.md`: `f85c02e76b0994477df7ded8d95585d260885f2d93fbeb91e57deb358d7855fe`
- `.ufo/evidence/round-35/contract.json`: `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0`
- `tools/tally-audit-v3.py`: `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`
- `.ufo/evidence/round-35/src/s102-posix-chap02.html`: `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`

```sh
wc -c /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/.ufo/evidence/round-35/src/s102-posix-chap02.html && sha256sum /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/.ufo/evidence/round-35/src/s102-posix-chap02.html
```

Exit 0: `357953` bytes; SHA-256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`.

`test -f /fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/corpus/lessons/round-35.md` exited 1 (absent); the committed-tree `git cat-file -e` check above independently exited 128 for the same path.

An earlier compound pin-and-hash command also printed the snapshot `HEAD`, the expected HTML/tool/SOURCES digests, then exited 1 because its final `sha256sum` operand was the absent lesson path. The successful standalone pin and successful hash command above are the retained positive evidence. No installs, C1/C2 measurements, code tests, or runtime probes were performed.

## Surfaces, limits, artifacts

- Product/lane files changed: **none**. No commits or code edits. Only this report was written under the assigned report path.
- Read-only audit surfaces: `corpus/SOURCES.md:110, 412-418`; `.ufo/evidence/round-35/src/s102-posix-chap02.html:237, 303-304`; `tools/tally-audit-v3.py:29-32`; `.ufo/evidence/round-35/contract.json:42`.
- Out of scope: C1/C2 runtime verdicts, runner behavior, sealed specimens, and any later revision's row/lesson state.
- Scratch provenance: `/fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane-dispatch-pin/` is the dispatch-pin clone; preexisting `/fast/scratch/hyaku/tameshi-r35-seats/ScribeS102/lane/` was not altered.
- Report artifact: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ScribeS102.md`.
