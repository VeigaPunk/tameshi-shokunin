# Reopen S063 — git(1) `GIT_CEILING_DIRECTORIES` / repository discovery

Seat: ReopenS063-2 (scout, w2). Target: row S063 of `corpus/SOURCES.md` at
`eb7838b16490ca7ba17ea3242ade76a61f744af2`, re-opened live at
https://git-scm.com/docs/git. Read/executed from a fleet-mirror clone
(`/tmp/tameshi-r17w2-ReopenS063-SmU4RZ/fleet/tameshi-shokunin`, detached at the
target rev).

Verdict: **holds** — the lesson quote is verbatim (17 words) at the stated
location, the tier/scope/teaches cells are supported, and the used-by file
exists at the rev and cites S063.

## 1. Row shape and rev

```
$ git -C $C show eb7838b…:corpus/SOURCES.md | grep -n '^| S063 '
72:| S063 | git(1): GIT_CEILING_DIRECTORIES and repository discovery (Git 2.56.0 docs) — https://git-scm.com/docs/git | docs | A | git's upward repository-discovery walk and the environment variables that redirect or bound it | ENVIRONMENT VARIABLES, "The Git Repository" @ page last updated in 2.56.0, fetched 2026-10-20 | discovery walks parent directories and environment variables override it, so a ceiling bounds the walk but is no identity check, and an inherited GIT_DIR redirects every `git -C` | mined | 2026-10-20 | on-release | corpus/lessons/round-17.md |
   exit 0
$ … | awk -F'|' '/^\| S063 /{print "NF="NF}'
NF=13          # 11 cells + 2 edge separators; matches the 11-column header (corpus/SOURCES.md:10)
   exit 0
$ grep -c '^| S063 |'  → 1 (unique row)
```

Rev confirmed: `git rev-parse eb7838b…` → `eb7838b16490ca7ba17ea3242ade76a61f744af2`
(`round-17: hermetic git env … C2 before/after receipts`, 2026-10-20 12:59:15 -0300).

## 2. Live page fetched

```
$ curl -sSL https://git-scm.com/docs/git -o <scratch>/git-docs.html
exit 0; 244355 bytes
sha256 8e04df786ac93f6339a15026e4ad8c6a49d611715cadbff56e0d15f76dc7a48c
$ curl -sSL -o /dev/null -w '%{url_effective} %{http_code}' https://git-scm.com/docs/git
https://git-scm.com/docs/git 200        # no redirect
```

Version marker matches the anchor's "page last updated in 2.56.0":
`git last updated in 2.56.0` (stripped-text line 1504; raw HTML line 1359).
`git --version` on the host is also 2.56.0.

## 3. Quote verbatim, ≤25 words

Target `<dd>` is the one anchored by
`id="Documentation/git.txt-GITCEILINGDIRECTORIES"` (HTML character offset 187691). Whitespace-normalized:

> This should be a colon-separated list of absolute paths. If set, it is a list of
> directories that Git should not chdir up into while looking for a repository directory
> (useful for excluding slow-loading network directories). …

```
$ python3 …  # extract dd, collapse whitespace, case-sensitive substring test
quote-exact: True words: 17
   exit 0
```

17 words ≤ 25; exact case-sensitive substring (starts mid-sentence at "a list …",
which is how the lesson quotes it). No curly punctuation or ellipsis inserted.

Independent primary confirmation on the installed man page:

```
$ man -P cat git | sed -n '1022,1026p'
     GIT_CEILING_DIRECTORIES
         This should be a colon-separated list of absolute paths. If set, it is
         a list of directories that Git should not chdir up into while  looking
         for  a repository directory (useful for excluding slow-loading network
         directories). …
```

Joining the wraps reproduces the quote exactly.

## 4. Stated location holds

`ENVIRONMENT VARIABLES → The Git Repository → GIT_CEILING_DIRECTORIES`:

- raw-HTML heading offsets: h2 `id="_environment_variables"` = 180706 <
  h3 `id="_the_git_repository"` = 183066 < dt `GIT_CEILING_DIRECTORIES` = 187691 <
  next h3 `Git Commits` = 192080.
- `man -P cat git`: `ENVIRONMENT VARIABLES` at line 950, `The Git Repository` at
  line 975, `GIT_CEILING_DIRECTORIES` at line 1022.

Minor cosmetic note only: the live web DOM h2 text is "Environment Variables"
(title case) and the page CSS does not uppercase h2; the uppercase form in the
row/lesson is exactly the git.1 man-page rendering (`man git` line 950). The
location is unambiguous either way.

## 5. Tier / scope / teaches

Contract read at fleet `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`
(frozen v1; `corpus/SOURCES.md` cites it by bare name).

- **tier A** — contract: A = "primary or authoritative for that scope (spec, official
  docs, source code, original paper, maintainer statement, the lane's own re-runnable
  gate output)". `git-scm.com/docs/git` is the official Git documentation; kind is
  `docs`, not `community`. Supported.
- **scope** — "git's upward repository-discovery walk and the environment variables
  that redirect or bound it": the same subsection documents `GIT_DIR`,
  `GIT_CEILING_DIRECTORIES`, `GIT_DISCOVERY_ACROSS_FILESYSTEM`; e.g.
  `GIT_DISCOVERY_ACROSS_FILESYSTEM`: "Git tries to find such a directory in the parent
  directories to find the top of the working tree, but by default it does not cross
  filesystem boundaries." Supported.
- **teaches** — clause by clause:
  - "discovery walks parent directories" — the `GIT_DISCOVERY_ACROSS_FILESYSTEM`
    sentence above.
  - "environment variables override it" — `GIT_DIR`: "If the GIT_DIR environment
    variable is set then it specifies a path to use instead of the default .git for the
    base of the repository"; ceiling text: "It will not exclude … a GIT_DIR set on the
    command line or in the environment."
  - "a ceiling bounds the walk" — the quoted sentence itself ("should not chdir up into
    while looking for a repository directory").
  - "is no identity check" — **[INFERENCE]** negative claim: the docs assign the
    variable only directory-exclusion semantics and no identity/validation semantics;
    nothing on the page contradicts it.
  - "an inherited GIT_DIR redirects every `git -C`" — `--git-dir`: specifying the .git
    location "using this option (or GIT_DIR environment variable) turns off the
    repository discovery"; `-C` only "Run as if git was started in <path> instead of
    the current working directory" (and makes relative path options relative to it).
    Nothing in the page lets `-C` clear or override `GIT_DIR`. Supported.

## 6. Used-by exists and cites S063

```
$ git -C $C cat-file -e eb7838b…:corpus/lessons/round-17.md ; echo $?
0
$ git show eb7838b…:corpus/lessons/round-17.md | sha256sum
0047f2492b0e0d273ebb96ee85c7f88ff1fa5a606ad3c6a066df927a16ca0dc5  -   (blob cec28bb261a158637e5852662864e43433701fd8)
$ git show eb7838b…:corpus/lessons/round-17.md | sed -n '37p'
| S063 | https://git-scm.com/docs/git | 2026-10-20 | "a list of directories that Git should not chdir up into while looking for a repository directory" (ENVIRONMENT VARIABLES → The Git Repository → `GIT_CEILING_DIRECTORIES`) |
```

`corpus/lessons/round-17.md:37` (the `## Gate` quote table) cites S063 with the same
quote, URL, access date and location; the prose at lines 41–42 ("… this / lesson for
S061, S062, S063 …") also names the lesson as S063's used-by (2 S063 mentions at the rev). The `used-by` path is repo-relative
and resolves at `eb7838b…`; `status: mined` is therefore satisfied. The lesson file is
a lesson, which the contract's `used-by` rule accepts ("knowledge entries or lessons").

## Gaps

- No blocking gaps. One cosmetic note: anchor/lesson uppercase the section label
  (`ENVIRONMENT VARIABLES`) while the web DOM heading is title case; it matches the
  man-page rendering exactly, so it identifies the same subsection.

## Verdict

Holds — S063 at `eb7838b16490ca7ba17ea3242ade76a61f744af2` survives a live re-open:
17-word verbatim quote at ENVIRONMENT VARIABLES → The Git Repository →
`GIT_CEILING_DIRECTORIES`, tier A / scope / teaches supported, and
`corpus/lessons/round-17.md` exists at the rev and cites S063.
