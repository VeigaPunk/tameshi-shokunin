# S18 — git-rev-parse `--show-toplevel` and git(1) repository discovery (source opened for the C2 repo-identity guard)

Question: what do git's own docs say about `git rev-parse --show-toplevel`, `GIT_CEILING_DIRECTORIES`
and repository discovery, and what does that teach the round's repo-identity guard (C2 / R16-OP1)?
Scope: two documentation pages, opened live this round. No lane files edited. No tools installed.

Axes (godspeed): **A** source fidelity (live open, exact anchor, verbatim quote, version recorded) ·
**B** row-contract fit (`corpus/SOURCES.md` 11-column shape, tier scoped to scope) ·
**C** claim transfer (does the quote ground the actual guard, tested not asserted).

## 1. Access record (live, 2026-10-20)

| source | fetch | served version | bytes | result |
|---|---|---|---|---|
| https://git-scm.com/docs/git-rev-parse | `curl -sSL -o rev-parse.html` | "git-rev-parse last updated in **2.56.0**" (release row 2026-09-28) | 122,459 | HTTP 200 |
| https://git-scm.com/docs/git | `curl -sSL -o git.html` | "git last updated in **2.56.0**" | 244,355 | HTTP 200 |

Fetched into `/tmp/tameshi-r17w1-S18SrcGitToplevel-SZ5lZu/` (rev-parse.html, git.html, plus
HTML-stripped .txt used for the line locations below). The first read of the rev-parse page was
also done natively (`read` on the URL); it truncated at 300/1182 lines before the `--show-toplevel`
paragraph, so the anchor text is quoted from the same fetch's extracted text, not from memory.
Host binary: `git --version` → `git version 2.56.0` (same release as the served docs).

## 2. Quotes (verbatim, word counts checked)

**Q1 — git-rev-parse(1), `--show-toplevel`** (23 words), location: OPTIONS → subsection
"Options for Files" (extracted-text line 2853 heading, paragraph at 2912-2915), page last updated
in 2.56.0, accessed 2026-10-20:

> Show the (by default, absolute) path of the top-level directory of the working tree. If there is no working tree, report an error.

**Q2 — git(1), `GIT_CEILING_DIRECTORIES`** (17 words), location: ENVIRONMENT VARIABLES →
subsection "The Git Repository" (heading at extracted-text line 5237; variable at 5295-5309), page
last updated in 2.56.0, accessed 2026-10-20:

> a list of directories that Git should not chdir up into while looking for a repository directory

Supporting, same page, `GIT_DISCOVERY_ACROSS_FILESYSTEM` (18 words, not the row quote): "Git tries
to find such a directory in the parent directories to find the top of the working tree" — this is
the sentence that makes the upward walk explicit.

## 3. Row drafts (`corpus/SOURCES.md` Registry shape)

Ids: the registry's own allocation block says "Next unused id: S058", so the drafts below use
S058/S059 as placeholders; **the L1 assigns final ids**. Cells contain no `|`. Status is `queued`
and `used-by` is `—` because no knowledge entry cites them yet; the L1 flips to `mined` with a
logged change once `corpus/lessons/round-17.md` cites the row (rule 2, append-only).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S058 (L1 assigns) | git-rev-parse(1): --show-toplevel (Git 2.56.0 docs) — https://git-scm.com/docs/git-rev-parse | docs | A | git's own definition of the working-tree top-level and its no-work-tree failure | OPTIONS, "Options for Files", --show-toplevel paragraph @ page last updated in 2.56.0 (release 2026-09-28), fetched 2026-10-20 | --show-toplevel reports the discovered working-tree top-level (absolute by default) and errors outside a work tree, so comparing it with the caller's own realpath tests repository identity instead of assuming it | queued | 2026-10-20 | on-release | — |
| S059 (L1 assigns) | git(1): GIT_CEILING_DIRECTORIES (Git 2.56.0 docs) — https://git-scm.com/docs/git | docs | A | git's upward repository-discovery walk and the ceiling variable that bounds it | ENVIRONMENT VARIABLES, "The Git Repository", GIT_CEILING_DIRECTORIES paragraph @ page last updated in 2.56.0, fetched 2026-10-20 | discovery searches parent directories for a repository and GIT_CEILING_DIRECTORIES only bounds that walk while not excluding the current directory, so a ceiling is not an identity check | queued | 2026-10-20 | on-release | — |

Suggested Search-log note (contract rule 5; L1 appends it, and the round lesson `## Gate` carries the
two URLs, the 2026-10-20 access date and the Q1/Q2 quotes with their locations):

> 2026-10-20 — **git repository-identity semantics for C2's guard** (S18, W1).
> Question: does git's own documentation ground the repo-identity guard (`--show-toplevel`
> equality) and the discovery behavior it refuses? Where: https://git-scm.com/docs/git-rev-parse
> (HTTP 200, 122,459 B, page last updated in 2.56.0) and https://git-scm.com/docs/git (HTTP 200,
> 244,355 B, last updated in 2.56.0), one fetch each. Identified 2 · screened 2 · included 2 ·
> excluded 0. Both rows tier A: official documentation, scoped to git's own behavior. Stop
> rationale: the question is the two documented behaviors the guard names; no adjacent page was
> needed to answer it.

## 4. What this teaches for this round's claims

**C2 / R16-OP1 — the guard is an identity test, and the docs supply both halves.** At the
dispatch tip `98bea7d`, the guard is `tools/pin-disposition.py:235-263`: it takes
`git -C <repo_real> rev-parse --show-toplevel`, requires exit 0 and non-empty stdout, then refuses
when `os.path.realpath(top) != repo_real` (`repo_foreign`). Q1 grounds exactly this: the command
reports the *discovered* top-level, so equality means "this directory is its own working-tree
top-level"; the documented "by default, absolute" removes the relative-path caveat, and the
"report an error" clause grounds the tool's separate `repo_not_git` arm (its empty-stdout check is
the belt to that brace).

**The failure mode the guard refuses is the documented upward walk, observed live.** Sandbox
`/tmp/tameshi-r17w1-S18SrcGitToplevel-exp-RjKeKY`:

```
$ git -C outer/missing rev-parse --show-toplevel      # outer/ is a repo; outer/missing is a plain dir
/tmp/.../outer                                          exit 0
$ git -C outer/missing rev-parse --verify HEAD
8a21c73b0e8f44ec7e6ece20b4130b6e6536dc86                 exit 0     # borrowed from the enclosing repo
$ python3: realpath(top) == realpath(outer/missing)
False                                                  # -> the tip guard's repo_foreign
```

So "`git -C DIR rev-parse --verify` succeeded" is not evidence that DIR is a repository. This is
not hypothetical for this lane: the fleet root `/home/vgpnk/Projects/shokunin` **is** a git repo
(`git -C /home/vgpnk/Projects/shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin`,
exit 0), so a sibling directory that exists but lacks `.git` would have its git calls answered by
the fleet root's object store. That is the exact hazard `repo_identity`'s docstring names
(`tools/pin-disposition.py:236-240`).

**A ceiling is not the guard, and the lane cannot use one anyway.** Q2 says the ceiling bounds the
walk but "will not exclude the current working directory", i.e. it limits how far discovery goes,
not whether the answer is the repo you meant. `git_env()` in the same file scrubs every inherited
`GIT_*` (`tools/pin-disposition.py:197-200`), so `GIT_CEILING_DIRECTORIES` is not even present for
these calls; the realpath comparison is the only bound. Observed ceiling behavior, for the record:
with `GIT_CEILING_DIRECTORIES=<outer>`, `git -C outer/inner rev-parse --show-toplevel` fails
(`fatal: not a git repository ...`, exit 128), while `git -C outer ...` still answers correctly
(exit 0) — the current directory is not excluded, as documented.

**No-work-tree arm.** `--show-toplevel` "report an error" is observable: `git -C bare.git
rev-parse --show-toplevel` → `fatal: this operation must be run in a work tree`, exit 128 (host git
2.56.0). A guard that string-compared stdout without checking the exit code would conflate this
with a path mismatch; the tip guard checks `returncode` first, which is the correct order.

**Finding for the C2 verifier (not a source claim).** The interface contract describes a
"repo-identity guard in `tools/mutate-and-run.sh`", but at the dispatch tip that file has no
`--show-toplevel` call: `git -C . grep show-toplevel 98bea7d -- tools` returns only
`tools/pin-disposition.py:79` and `:255`. `regression_case_git` (`tools/mutate-and-run.sh:1140-1154`)
derives `repo="$FLEET_ROOT/${rel%%/*}"` and sends it to `rev-parse --verify`, `cat-file -e` and
`git show` (`:1001`, `:1005`, `:1010`) with no identity check, so a present-but-not-a-repo lane
directory would borrow the fleet root's objects there too. Grade the guard where it exists at the
rev being measured; if the round re-pins `mutate-and-run.sh`, the same `realpath(top) ==
realpath(repo)` check is what the docs above support.

## 5. Residual unknowns

- The docs pages are version-floating; the row anchors record 2.56.0 as served on 2026-10-20 and
  carry `recheck: on-release`. A later release that changes either paragraph is a new row, not an
  edit (contract rule 2).
- I did not test a `GIT_DIR` set on the command line or in the environment; git(1) says the ceiling
  does not exclude it, and Q2's sentence does not cover it. Not reachable in the lane's guard
  because `git_env()` scrubs `GIT_*` [INFERENCE for any other consumer].
- The doc does not spell out `--show-toplevel` behavior below a bare repository; the observed
  fatal line is host behavior at 2.56.0, recorded above as an observation, not as doc text.

## 6. Command log (exits and key lines)

- `curl -sSL` both URLs → `http=200` (`rev-parse bytes=122459`, `git bytes=244355`).
- `grep -n 'last updated'` → `git-rev-parse last updated in 2.56.0`; `git last updated in 2.56.0`.
- `grep -n -A4 -- '--show-toplevel'` → paragraph at extracted lines 2912-2915 under "Options for
  Files" (heading 2853).
- `grep -n -A12 'GIT_CEILING_DIRECTORIES'` → 5295-5309 under "Environment Variables" (5198) /
  "The Git Repository" (5237).
- Word counts: Q1 23, Q2 17 (both ≤25).
- Sandbox: enclosing-repo discovery exit 0; `--verify HEAD` exit 0; ceiling-at-outer exit 128;
  ceiling run inside outer exit 0; bare repo exit 128 ("this operation must be run in a work tree");
  symlinked `-C` returns the physical top-level and `realpath` equality is True.
- `git -C /home/vgpnk/Projects/shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin`,
  exit 0 (fleet root is a repo).
- Lane-tip greps are read-only `git show`/`git grep` at `98bea7da5801f4bc58e4187690ee1687c8a5061f`;
  no git writes, no jj, no lane edits except this report.
- Tooling directive: nothing installed or upgraded this task.

Verdict: **built** — two live-opened, version-anchored rows drafted (S058/S059 placeholders), quotes
verified at 23 and 17 words, and the teaching pins the guard to `realpath(--show-toplevel)` equality
with the fleet-root super-repo hazard observed; residual finding: at the dispatch tip the guard
exists only in `tools/pin-disposition.py`, not in `tools/mutate-and-run.sh`.
