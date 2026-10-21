# Route03 — R18-3 falsifier arithmetic

Review axes: evidence fidelity, correction precision, and failure-capable detection. This is a read-only proposal for routed defect R18-3; no production file was changed.

## Finding and evidence

`corpus/lessons/round-18.md:79` says the deleted-line falsifier is “the four allowed used-by cells only.” The non-author spot-check §5.3 says the pinned diff has “5 deleted lines (S001, S008, S052, S056, S057)” and explicitly identifies S008's status+used-by line as the omitted fifth deletion (`corpus/lessons/round-18-verifier-spotcheck.md:192-195`). The round-19 contract routes the same defect as R18-3 (`.ufo/waves/round-19/contract.json:9`).

Observed source command (read-only):

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && \
  git diff 183f87b899e6cae46be98d251cbc87fb5118f6ca \
           4b7c6823a462f5ea2eafcb262275300a545f3ed7 -- corpus/SOURCES.md \
  | grep -E '^-' | grep -vE '^---'
```

Outcome: five removed SOURCES rows, IDs S001, S008, S052, S056, S057. The grep was only a display filter on the Git diff; the row identities and count agree with the independently recorded spot-check. S001/S052/S056/S057 are the four used-by-only replacements; S008 additionally changes status (`queued` → `mined`) and used-by (`—` → `corpus/knowledge/mutation-case-kumitate-sources-check.md`).

No `lsp` device/server route is exposed in this seat's available tools, so no references/definition/diagnostics calls were possible or are claimed. This finding is limited to the cited text and revision-pinned diff. No old lane tools, tests, builds, linters, or formatters were run; no tool was installed.

## Exact append-only correction proposed

Append this dated erratum at the end of `corpus/lessons/round-18.md`; do not rewrite line 79:

> **R18-3 erratum — falsifier arithmetic (2026-10-21).** The falsifier in the first row of “Mistakes made this round” (original line 79) is incorrect. The pinned `corpus/SOURCES.md` diff from `183f87b899e6cae46be98d251cbc87fb5118f6ca` to `4b7c6823a462f5ea2eafcb262275300a545f3ed7` deletes five rows: S001, S008, S052, S056, and S057. Four are used-by-only replacements (S001, S052, S056, S057); S008 changes both status (`queued` → `mined`) and used-by (`—` → `corpus/knowledge/mutation-case-kumitate-sources-check.md`). The correct falsifier is five deleted rows with exactly those IDs. This correction is arithmetic/metadata only and changes no claim or score.

## Failure-capable predicate proposed (not executed)

Run in Bash against the pinned round-18 revisions. It exits nonzero for a missing, extra, or substituted deleted row (including the old four-ID expectation), and zero only for the observed five-ID list:

```bash
set -o pipefail
git diff --no-ext-diff --unified=0 \
  183f87b899e6cae46be98d251cbc87fb5118f6ca \
  4b7c6823a462f5ea2eafcb262275300a545f3ed7 -- corpus/SOURCES.md |
python3 -c 'import re,sys; actual=re.findall(r"^-\| (S\d{3}) \|", sys.stdin.read(), re.M); expected=["S001","S008","S052","S056","S057"]; print(f"deleted SOURCES IDs={actual}"); raise SystemExit(actual != expected)'
```

The predicate is proposed, not represented as run. No calibration value or promotion is inferred.