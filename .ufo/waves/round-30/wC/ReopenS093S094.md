# ReopenS093S094

seat: ReopenS093S094
revision read: bb681566b18211adf8ae9c28df91e17678e3f545
verdict: DISAGREE

The reopened S093 and S094 bytes match the registry rows and the round-30 snapshots. The knowledge entry quotes the mechanical part of each source faithfully, then overreaches in two sentences: "cleared environment" is stronger than `--clearenv`, and the S094 warning is identified with every control round and with a hash seal defeating allowlists.

No tools were installed.

## S093

Agree on the bytes, the six-flag sentence, and the limit. Disagree on "cleared environment".

Fetched `https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml` to `/tmp/reopen-s093s094/bwrap.xml`.

```
sha256sum bwrap.xml
2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da  bwrap.xml
wc -c → 33289
```

`cmp` against `.ufo/evidence/round-30/sources/S093-bwrap-0.13.1.xml` was equal (same sha256, 33289 bytes). That is the digest and size in `corpus/SOURCES.md` row S093 at the pinned revision. `corpus/SOURCES.md` and `corpus/knowledge/regression-tally-completeness.md` in the work tree are byte-identical to that revision.

Line 159, quoted:

```
Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try
```

Six options. The two `try` options say "if possible else skip it" (`bwrap.xml:131` and `:155`). The row's "try-else-skip" is that sentence, compressed. The other four are unconditional.

The other cited lines match the row's flag list:

- `:233-235` `--clearenv`: "Unset all environment variables, except for PWD and any that are subsequently set by --setenv"
- `:403` `--proc`: "Mount procfs on DEST"
- `:412-416` `--tmpfs`: mount a new tmpfs; mode 0755 and the default size unless `--perms` or `--size` came first
- `:575-577` `--new-session`: `setsid()`, disconnect from the controlling terminal
- `:589-592` `--die-with-parent`: SIGKILL the sandbox processes when bwrap or its parent dies

README at the same tag, lines 52-54: protection between sandbox and host "is entirely determined by the arguments passed to bubblewrap." Line 133: bubblewrap always creates a new mount namespace (mount is not one of the six). Tag `v0.13.1` is an annotated tag whose commit is `362936aea0d5c6e70f7af75d2d44b5a914cb4ba2`; the tag message says "Released: 2026-10-14", and the GitHub release `published_at` is `2026-10-14T12:21:00Z`. Local package is `bubblewrap 0.13.1-1`; `man bwrap` uses the same `--unshare-all` and `--clearenv` sentences (man line numbers differ; the row cites `bwrap.xml`).

`c1-measure-v4.py:321-326` is the argv the entry is talking about: `--unshare-all --die-with-parent --new-session --clearenv`, then `--proc /proc`, `--tmpfs /tmp`, then `--setenv` for `PATH`, `HOME`, `LANG`, and `TMPDIR`. Each job bind-mounts its own tree at `/w` (`:335`).

Faithful uses:

- `regression-tally-completeness.md:68` "six flags, two of them try-else-skip" matches line 159 plus `:131` and `:155`.
- The same bullet's "not a measured security boundary" matches the row scope and README 52-54. It does not say bubblewrap can never be a boundary.
- The hide claim in that bullet is pinned to wave-A seats, not to a sentence in the manual.

Overreach: line 42 says the sandbox runs "with a cleared environment". `--clearenv` keeps `PWD`, and this argv then sets four variables. "Cleared" drops both facts.

## S094

Agree on the bytes and on the warning paraphrase. Disagree on what that warning is used to explain.

Fetched `https://arxiv.org/pdf/1411.2664v3` with `-A Mozilla/5.0` to `/tmp/reopen-s093s094/1411.2664v3.pdf`.

```
sha256sum 1411.2664v3.pdf
6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697  1411.2664v3.pdf
wc -c → 322643
```

`cmp` against `.ufo/evidence/round-30/sources/S094-arxiv-1411.2664v3.pdf` was equal. The same sha256 came back from `https://arxiv.org/pdf/1411.2664` (the row's unversioned URL; 322643 bytes). `pdfinfo` CreationDate is `Wed Mar 2 23:49:08 2016 -03`. Page 1 stamp: `arXiv:1411.2664v3 [cs.LG] 2 Mar 2016`. Authors on that page: Cynthia Dwork, Vitaly Feldman, Moritz Hardt, Toniann Pitassi, Omer Reingold, Aaron Roth.

The sentence that begins "Each submitted model is" is on the PDF page whose footer is `2` (section 1, Introduction). The phrase "available only to the organizers" is inside it. `pdftotext -layout` gives:

> Each submitted model is evaluated on a (fixed) test set that is available only to the organizers. The score of each solution is provided back to each participant, who can then submit a new model. In addition the scores are published on a public leaderboard. At the conclusion of the competition the best entries of each participant are evaluated on an additional, hitherto unused, test set. The scores from these final evaluations are published. The comparison of the scores on the adaptively reused test set and one-time use test set frequently reveals significant overfitting to the reused test set.

Row S094's anchor (that sentence, printed page 2, v3, that sha256, 2 Mar 2016) matches. Its scope, "a holdout kept from the candidate, and why scores on a fixed holdout still overfit it", is a fair compression if "candidate" means the submitter. Its teaches cell adds a step the paper does not take: "a hash sealed before scoring fixes the bytes and does not by itself stop that reuse." The paper never mentions a hash. The "does not by itself stop that reuse" half does follow from the paragraph. The hash half is this lane's mechanism, not the paper's.

Faithful use: line 60's clause "a fixed holdout overfits once scores are returned and new candidates are submitted" restates the quoted paragraph (participants called candidates).

Overreach, same paragraph:

- "A sealed set committed by hash before scoring (the held-out idea of S094: a test kept from the candidate) defeats allowlists of the public shapes" makes S094's idea the subject of a result section 1 does not state. Section 1 says the opposite about a reused holdout: keeping the test from submitters does not stop overfitting once scores come back. The miss on the sealed items is a lane observation. It is not what the paper shows.
- "which is what each round of controls did" identifies every control round with that score-return loop. The entry's own earlier account is different: v1 through v3 were met by programs that knew the public ruler (lines 40-41 and the start of line 60), and the sealed set was added later (line 42). Those rounds are not the paper's "scores returned, then a new model on the same hidden test."

## Smallest safe correction

Do not edit the sources or the snapshots.

In `corpus/knowledge/regression-tally-completeness.md:42`, replace "with a cleared environment" by "with `--clearenv` (the manual keeps PWD) and `--setenv` for PATH, HOME, LANG, and TMPDIR".

In line 60, split the sealed-set result from S094. Keep S094 on one claim only: a fixed test withheld from submitters still overfits once scores are returned and later models are submitted. Delete "which is what each round of controls did", or replace it with the narrower fact the entry already states: programs that knew the public ruler met the earlier counters, which is not the phenomenon in section 1.

Leave line 68's six-flag sentence. Keep the hide claim on the wave-A seats named there; do not read it as a consequence of `--unshare-all`.
