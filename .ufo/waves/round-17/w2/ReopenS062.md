# Reopen S062 — git-rev-parse(1) `--show-toplevel`

Seat: `TameshiR17.ReopenS062-2` (scout, wave 2, falsify). Read rev:
`eb7838b16490ca7ba17ea3242ade76a61f744af2`. Lane root untouched; all work in a
fleet-mirror `/tmp` clone.

Axes (godspeed): **A** quote fidelity (verbatim, word count, stated location) ·
**B** contract fit (row shape, tier/scope/teaches support) · **C** citation reach
(used-by exists at the read rev and actually cites S062).

## Setup

```
W=$(mktemp -d /tmp/tameshi-r17w2-ReopenS062-2-XXXXXX)   # W=/tmp/tameshi-r17w2-ReopenS062-2-0rTE5f
mkdir $W/fleet; for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" $W/fleet/; done
git clone -q …/tameshi-shokunin $W/fleet/tameshi-shokunin \
  && git -C $W/fleet/tameshi-shokunin checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
# CLONE_OK; rev-parse HEAD -> eb7838b16490ca7ba17ea3242ade76a61f744af2
C=$W/fleet/tameshi-shokunin
git --version   # git version 2.56.0 (same release the page serves)
```

## 1. The row, at the read rev

`git -C $C show eb7838b…:corpus/SOURCES.md` — S062 at **corpus/SOURCES.md:71**;
header row at `:10`, separator at `:11`, registry body after. Cell split
(`awk -F'|' NR==71`, 11 cells, `NF=13`):

```
1  S062
2  git-rev-parse(1): --show-toplevel (Git 2.56.0 docs) — https://git-scm.com/docs/git-rev-parse
3  docs
4  A
5  git's own definition of the working-tree top-level and its no-work-tree failure
6  OPTIONS, "Options for Files", --show-toplevel @ page last updated in 2.56.0, fetched 2026-10-20
7  --show-toplevel reports the discovered top-level, so comparing its realpath with the caller's repo path tests repository identity instead of assuming it
8  mined
9  2026-10-20
10 on-release
11 corpus/lessons/round-17.md
```

Blob sha256 of `corpus/SOURCES.md` at eb7838b:
`ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5`.

## 2. Live source — the quote is verbatim at the stated location

```
curl -sSL --max-time 60 -o /tmp/tameshi-r17w2-ReopenS062-2-gitdocs.html \
     https://git-scm.com/docs/git-rev-parse
# HTTP=200 SIZE=122459
curl -sSL -o /dev/null -w 'final_url=%{url_effective} http=%{http_code}\n' <same URL>
# final_url=https://git-scm.com/docs/git-rev-parse http=200      (no version-pinned redirect)
sha256sum /tmp/…gitdocs.html
# 1e84fc200220b2cd356b78f2344766ee7cbaafa8bcef64679dbf47ec585f19da
# second independent fetch: same sha256 1e84fc20…19da  (byte-stable at re-open time)
```

Version marker: extracted-text line 172 — `git-rev-parse last updated in 2.56.0`.
Effective anchor path in the page: `OPTIONS` (extracted line 296) → `Options for
Files` (586) → `--show-toplevel` (631), paragraph at **632-633**. Raw HTML at the
`<dt id="Documentation/git-rev-parse.txt---show-toplevel">`:

```html
<a class="anchor" href="#Documentation/git-rev-parse.txt---show-toplevel"></a>--show-toplevel </dt>
<dd>
<p>Show the (by default, absolute) path of the top-level directory
of the working tree. If there is no working tree, report an error.</p>
</dd>
```

- Verbatim match after joining the single intra-paragraph newline (only break:
  `directory` / `of`): **yes**. No HTML entities, no NBSP, no typographic
  substitution in the quoted span; comparison done on the tag-stripped text with
  only `[ \t]+` collapsed, and directly on the raw `<p>` bytes above.
- Word count: **23** (`Show the (by default, absolute) path of the top-level
  directory of the working tree. If there is no working tree, report an error.`) —
  ≤ 25.
- Location label `OPTIONS → Options for Files → --show-toplevel` is exact.
  `--show-toplevel` also sits between `The following options are modified by
  --path-format:` (600) and `The following options are unaffected by --path-format:`
  (642), which is what the quoted `(by default, absolute)` parenthetical refers to.
- Lesson quote agrees: `corpus/lessons/round-17.md:36` (inside `## Gate`, table
  headed "Sources opened this round (rule 1 — URL, access date, quote ≤25 words
  with location)") carries the identical sentence + `(OPTIONS → Options for
  Files → \`--show-toplevel\`)`, accessed `2026-10-20`.

Behaviour probes (each in its own `mktemp -d`):

```
git init --bare bare.git; cd bare.git; git rev-parse --show-toplevel
# fatal: this operation must be run in a work tree            exit=128
# -> the quoted "If there is no working tree, report an error." is observable.
super/ is a repo, super/sub has no .git:
  git -C super      rev-parse --show-toplevel -> /tmp/…/super   exit=0
  git -C super/sub  rev-parse --show-toplevel -> /tmp/…/super   exit=0
  realpath(/tmp/…/super/sub) != reported top
  git -C super/sub rev-parse --path-format=relative --show-toplevel -> ../   exit=0
# -> "by default, absolute" confirmed; the reported path is the discovered
#    top-level, not the caller's directory.
```

## 3. Tier / scope / teaches support

- **tier A** — `kind=docs`; this is the Git project's own manual page
  (`git-rev-parse last updated in 2.56.0`; page footer `Part of the git[1] suite`).
  Contract (`SOURCES-CONTRACT-v1.md` l.27-31 / `CORPUS.md` l.93-97): A = "primary or
  authoritative for that scope (… official docs …)"; `community` is never A and this
  row is not `community`. **Supported.**
- **scope** (`git's own definition of the working-tree top-level and its
  no-work-tree failure`) — both halves are literally in the quoted paragraph, and
  the no-work-tree half is observable (bare-repo probe, exit 128). **Supported.**
- **teaches** (`--show-toplevel reports the discovered top-level, so comparing its
  realpath with the caller's repo path tests repository identity instead of assuming
  it`) — the report half is the doc's own definition (probes above); the
  identity-comparison half is a one-hop design application of that definition: a
  non-repo child of a super-repo is answered from the super-repo, so
  `realpath(top) != realpath(caller)` is exactly the foreign-repo signal. [INFERENCE]
  at the boundary (the page never says "realpath" or "identity") but grounded, and
  the landing rev applies it: `tools/mutate-and-run.sh:1050-1053` does
  `repo_top=$(git_clean -C "$repo" rev-parse --show-toplevel)` then refuses with
  `repo_identity_mismatch` when `realpath(repo_top) != repo_real` (also
  `tools/pin-disposition.py:265`, `tools/evidence-disposition.py:411`). **Supported.**

## 4. Used-by — file exists at eb7838b and cites S062

```
git -C $C cat-file -e eb7838b…:corpus/lessons/round-17.md -> EXISTS
sha256 0047f2492b0e0d273ebb96ee85c7f88ff1fa5a606ad3c6a066df927a16ca0dc5
git -C $C show eb7838b…:corpus/lessons/round-17.md | grep -n S062
36:| S062 | https://git-scm.com/docs/git-rev-parse | 2026-10-20 | "Show the (by default, absolute) path of the top-level directory of the working tree. If there is no working tree, report an error." (OPTIONS → Options for Files → `--show-toplevel`) |
59:| repo identity | `tools/mutate-and-run.sh` read `git -C "$repo"` with no identity check; a lane dir without `.git` inside the fleet super-repo is answered from the super-repo (`JjAuditTameshi.md` §2.2, S062) | none | `repo_identity_mismatch` SETUP guard; … |
```

Line 36 satisfies contract rule 1 for the row (URL, access date, 23-word quote,
location). Lines 40-43 record the registry change ("this lesson for S061, S062,
S063") so `mined` has a logged basis; line 59 is a substantive use, not a
drive-by mention. **Supported.**

## 5. Row-contract census (contract census block, run from the clone)

```
awk … NF!=13 {n++} END{print n+0}       -> 0            exit 0
enum/tier-inflation sweep               -> (no output)  exit 0
mined used-by paths missing             -> (no output)  exit 0
duplicate ids                           -> (no output)
grep -cE '^\|…S[0-9]{3,}…\|'            -> 62
status histogram                        -> mined=35 queued=24 rejected=3
row S062                                -> NF=13 status=mined usedby=corpus/lessons/round-17.md
```

No `|` inside any S062 cell; `docs`/`A`/`mined`/`on-release` all in enum; `opened`
2026-10-20 = the day of this re-open.

## 6. Correction to the wave-1 receipt's line numbers (non-defect)

`.ufo/waves/round-17/w1/S18SrcGitToplevel.md` §2 cites "extracted-text line 2853
heading, paragraph at 2912-2915". My extraction (tag-strip → non-empty lines) puts
the same heading at 586 and the paragraph at 632-633. Both name `OPTIONS →
Options for Files → --show-toplevel`; the delta is the extraction method (S18 kept
a different line model). No anchor discrepancy. S18's recorded fetch size,
122,459 bytes, equals today's `size_download`; its Q1 word count (23) matches mine.

## 7. Residual unknowns

- The page is version-floating (`on-release` is the right control). Two fetches
  minutes apart were byte-identical (`1e84fc20…19da`); a later release that changes
  the paragraph is a new row per contract rule 2, not an edit. [INFERENCE for any
  future re-open]
- The row's `anchor` carries no line number, only section path + version; the
  contract allows "exact section / heading / page / line plus revision", so this is
  compliant, not complete-to-the-line.
- The lesson's mistake row names `JjAuditTameshi.md` as a bare filename. That file
  is not in the lane; it resolves at the fleet root
  `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditTameshi.md`,
  where §2.2 reproduces exactly the hazard the row cites (`git -C lane rev-parse
  --show-toplevel` → `exp2/super`, guard refuses). Pointer-precision nit in the
  lesson, **not** a defect in S062's cells.
- No claim made here about S058-S061/S063/S064; out of this seat's scope.

## 8. Command log (exits)

- clone + `checkout --detach eb7838b…` → `CLONE_OK`, HEAD = eb7838b… (exit 0).
- `curl` rev-parse page → `HTTP=200 SIZE=122459`; sha256 `1e84fc20…19da` twice.
- tag-strip locate: quote hit at extracted 632-633 under `--show-toplevel` 631 /
  `Options for Files` 586; raw `<p>` inspected → verbatim, 23 words.
- `git --version` → `git version 2.56.0`.
- bare-repo probe → exit 128, `fatal: this operation must be run in a work tree`.
- nested-dir probe → exit 0, reported enclosing top; `--path-format=relative` → `../`, exit 0.
- census block → 0 malformed, no enum violations, no missing used-by paths, no dup ids;
  62 rows; mined=35 queued=24 rejected=3.
- `cat-file -e …:corpus/lessons/round-17.md` → EXISTS; `grep -n S062` → lines 36, 59.
- Read-only: `git show`/`git grep`/`git ls-tree` only. No git write, no jj, no lane
  edits outside this report. Tooling directive: nothing installed or upgraded.

Verdict: **holds** — S062's quote is verbatim at OPTIONS → Options for Files →
`--show-toplevel` (23 words, line-wrap join only), the tier/scope/teaches cells are
supported by the live page and by executed git 2.56.0 probes, and
`corpus/lessons/round-17.md` exists at eb7838b and cites S062 in both the `## Gate`
source table and the repo-identity mistake row.
