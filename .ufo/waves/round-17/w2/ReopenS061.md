# ReopenS061 — S061 source-row re-open (falsify)

Rev under test: `eb7838b16490ca7ba17ea3242ade76a61f744af2` (branch `master`).
Lane clone: `/tmp/tameshi-r17w2-ReopenS061-SqNBuT/fleet/tameshi-shokunin`, detached at
that rev, fleet-mirror symlinks in place. All lane-file reads came from the clone.
No lane tools executed against the live lane root. This report is the only lane write.
No installs or upgrades: jj 0.46.0 was extracted to `/tmp` from the official release
tarball for one empirical check (not installed).

## Target

Row `corpus/SOURCES.md:70`, the lesson quote at `corpus/lessons/round-17.md:35`, and
the row's `used-by` claim (`corpus/lessons/round-17.md` exists at the rev and cites S061).

## Verdict summary

| Check | Result |
|---|---|
| Quote verbatim (line-wrap joins allowed) | PASS — byte-identical, 12 words (limit 25) |
| Quote at stated location | PASS — `§Converting a workspace into a colocated workspace`, manual-process code block, `#` comment immediately above `jj new && jj undo` |
| Revision anchor `@ v0.46.0 (alias latest)` | PASS — `versions.json` publishes `v0.46.0` with alias `latest` |
| `tier` cell (A) | PASS — official jj docs, authoritative for their own Git-compatibility behavior; contract allows A for official docs |
| `scope` cell | PASS with wording caveat — HEAD-at-working-copy-parent and "detached HEAD" are both on the page |
| `teaches` cell | PASS for the mechanism; one overbroad consequence (see Gaps) |
| `anchor` cell | MINOR GAP — `§Colocated Jujutsu/Git workspaces ¶2` is a paragraph off (the detached-HEAD claim is ¶3) |
| `used-by` file exists + cites S061 | PASS — exists (8969 bytes); cites S061 at lines 35, 42, 58 |
| Contract census on the row | PASS — NF=13, kind/tier/status enums valid, used-by path exists, no dup id |

Verdict: **holds** at `eb7838b1`; two non-blocking imprecisions, no blocking gap and no
false quote.

## Commands, exits, key output

1. Row extraction (exit 0):
   `git -C $C show eb7838b1...:corpus/SOURCES.md | sed -n '70p'`
   Output (full row, 11 cells, NF=13):
   `| S061 | Git compatibility (Jujutsu docs) — https://docs.jj-vcs.dev/latest/git-compatibility/ | docs | A | colocated jj/git workspaces: what Git HEAD points at and why a Git-side HEAD read is not the branch tip | §Colocated Jujutsu/Git workspaces ¶2 and §Converting a workspace into a colocated workspace, recipe comment @ v0.46.0 (alias latest), fetched 2026-10-20 | in a colocated workspace jj leaves Git detached at the working-copy commit's parent, so `git rev-parse HEAD` is not the bookmark tip; read the branch ref or an explicit revision | mined | 2026-10-20 | 180d | corpus/lessons/round-17.md |`

2. Byte comparison of lesson quote vs live page (exit 0), Python `html.unescape` on the
   `<span class="c1">` comment, lesson quote extracted from `round-17.md:35`:
   ```
   lesson quote : "Convince jj to update .git/HEAD to point to the working-copy commit's parent"
   page quote   : "Convince jj to update .git/HEAD to point to the working-copy commit's parent"
   equal        : True
   lesson words : 12
   page context line: 2319
   non-ascii in quote: []
   ```

3. Live page fetch (exit 0): `curl -sS -o git-compat.html -w 'HTTP %{http_code} bytes=%{size_download}' https://docs.jj-vcs.dev/latest/git-compatibility/`
   → `HTTP 200 bytes=61334`; `sha256 db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254`.
   `grep -n "Convince jj"` → `2319:<span class="c1"># Convince jj to update .git/HEAD to point to the working-copy commit&#39;s parent</span>`.
   Section anchors: `2223:<h2 id="colocated-jujutsugit-workspaces">`, `2297:<h3 id="converting-a-workspace-into-a-colocated-workspace">`.

4. Version manifest (exit 0): `curl https://docs.jj-vcs.dev/versions.json`
   → entry `{"version": "v0.46.0", ..., "aliases": ["latest"]}`; `prerelease` has no alias.
   So the anchor's revision claim is true today.

5. Version-pinned source (exit 0): `curl https://raw.githubusercontent.com/jj-vcs/jj/v0.46.0/docs/git-compatibility.md`
   → `HTTP 200 bytes=13185`; `sha256 135a99ea40d2e626d0bc282283459650ba864df728449ac9225965578bc4e4bc`.
   `grep -n "Convince jj"` → `239:# Convince jj to update .git/HEAD to point to the working-copy commit's parent`;
   `grep -n "^### Converting"` → `204:### Converting a workspace into a colocated workspace`.
   Lines 228-241 show the comment inside the fenced manual-process block, immediately
   before `jj new && jj undo` — the "recipe comment" location claimed by the lesson.

6. Contract text (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`,
   read-only, exit 0):
   - line 26-27: `A: primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement, ...)`.
   - line 32-33: `anchor — exact section / heading / page / line plus revision (version, commit, or publication date)`. Never a bare homepage.
   - line 34-35: `teaches — one grounded learner benefit`.
   - line 36: `status — ... mined (cited by ≥1 path in used-by)`.
   - line 38-39: `recheck — ISO date or cadence (90d, 180d, on-release)`.
   - line 45-48: the round lesson's `## Gate` records URL, access date, and a ≤25-word quote with its location grounding `teaches`.

7. Used-by file at the rev (exit 0):
   `git cat-file -s eb7838b1...:corpus/lessons/round-17.md` → `8969`;
   `git show eb7838b1...:corpus/lessons/round-17.md | grep -c "S061"` → `3`.
   `grep -n '^##'` → `14:## Gate`, `48:## Mistakes`; the source table at lines 30-38 is
   inside `## Gate`, as the contract requires.
   Line 35 is the S061 quote row; line 42 says "this lesson for S061, S062, S063"; line 58
   uses S061 for the jj HEAD-semantics fix. The file's working-tree sha256 in the clone is
   `0047f2492b0e0d273ebb96ee85c7f88ff1fa5a606ad3c6a066df927a16ca0dc5`.

8. Contract census commands against the clone's `corpus/SOURCES.md` (all exit 0):
   - `NF for S061` → `NF=13`.
   - enums → `kind=docs tier=A status=mined`.
   - mined used-by existence → `exists: corpus/lessons/round-17.md`.
   - malformed-row scan (`NF!=13`) → no output; duplicate-id scan → no output.

9. Empirical HEAD-semantics check, official jj 0.46.0 binary (exit 0; tarball
   `jj-v0.46.0-x86_64-unknown-linux-musl.tar.gz`, 11110358 bytes, extracted under `/tmp`;
   `jj 0.46.0-7d382314f9420b4b8d932245b49c99492c812b9f`):
   ```
   state A: bookmark at @ (only commit)
     .git/HEAD: ref: refs/heads/master          (unborn)
     git rev-parse HEAD: fatal: ambiguous argument 'HEAD'
     main: 96710d1e...
   state B: after `jj new`  (bookmark sits on the working-copy parent)
     .git/HEAD: 96710d1e...                     (detached)
     HEAD: 96710d1e...
     main: 96710d1e...
     equal: YES
   state C: after `jj bookmark set main -r @` (bookmark on the working copy)
     HEAD: 96710d1e...                          (the working-copy parent)
     main: 87a6a80d...
     equal: NO
   ```
   Mechanism in the row is exactly reproduced: `HEAD` is the working-copy commit's parent.
   But the categorical consequence "`git rev-parse HEAD` is not the bookmark tip" is false
   in state B.

## Gaps (non-blocking)

1. **Anchor paragraph off by one.** `§Colocated Jujutsu/Git workspaces ¶2` is
   "This mode is very convenient when tools (e.g. build tools) expect a Git repo to be
   present." (v0.46.0 `docs/git-compatibility.md:139-140`). The used claim — jj commands
   "usually put the Git repo in a 'detached HEAD' state" — is ¶3 at lines 142-148
   (`¶1` is 133-137). The same section is the right place; only the paragraph number is wrong.
   The quote's own stated location ("recipe comment") is correct.

2. **"so `git rev-parse HEAD` is not the bookmark tip" overgeneralizes.** It holds when the
   bookmark points at the working-copy commit (test state C), but not when the bookmark
   sits on the working-copy parent (state B: HEAD == `refs/heads/main`). The docs say
   "usually" detached, not "always", and on the first commit HEAD is an unborn symref
   (state A). The operational advice — "read the branch ref or an explicit revision" — is
   correct and is the lesson the lane actually needs: HEAD is not *reliably* the bookmark
   tip. Suggest `teaches` phrase "not reliably the bookmark tip" if the row is ever revised;
   the row's status and tier do not change.

## Remaining unknowns

- `latest` is a moving alias; v0.46.0 was confirmed as its target on 2026-10-20 via
  `versions.json`. A later docs release could move `latest` without changing this row's
  URL, which is why the row's `recheck 180d` is appropriate.
- The empirical check used the official v0.46.0 binary, but jj behavior in a fleet-shaped
  repo could differ from the clean `/tmp` fixture; this does not affect the doc-quote check.

## One-line verdict

S061 holds at `eb7838b16490ca7ba17ea3242ade76a61f744af2`: the lesson quote is verbatim
(12 words) at the stated recipe comment, tier A and the scope are grounded in the page,
and `corpus/lessons/round-17.md` exists and cites S061; two non-blocking imprecisions —
the anchor's `¶2` should be `¶3`, and "HEAD is not the bookmark tip" is state-dependent.
