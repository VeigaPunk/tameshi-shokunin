seat: CritJudge03

# Round-45 w2 — C1 falsify: independent re-judgment of S003, S076, S093

Inputs read at commit `ad5942c6e9858af19d00000b58439b321ddfa62b` (ledger + snapshots via `git show <rev>:<path>`; worktree bytes at `1f9266a` are the same blobs). Scratch: `/tmp/tameshi-r45-CritJudge03/`. Reviewer is not the author of any of the three entries (authors: ExecRows01, ExecRows09, ExecRows17). No tool installs (preinstalled `curl`, `python3`, `sha256sum`).

## Verdicts

S003 agree — reviewer CritJudge03 — live sha256 equals the entry `raw_sha256` and the gunzipped snapshot, and the quote sits in the §Limitations list of the Incremental page asserting that environment changes and updated (dev) dependencies are not detected, which is exactly the teaches blind-spot claim.
S076 agree — reviewer CritJudge03 — live sha256 equals the entry `raw_sha256` and the gunzipped snapshot, and the quote is the complete detached-HEAD clause in the 3rd `<p>` after `<h2 id="colocated-jujutsugit-workspaces">`, so the row's "¶3, not ¶2" anchor holds.
S093 dispute — reviewer CritJudge03 — the 25-token quote is a markup-only fragment of the `--unshare-all` listitem that never names `--unshare-all`, drops the "Unshare all possible namespaces. Currently equivalent with:" assertion and truncates before the sixth flag `--unshare-cgroup-try`, so it does not state the teaches claim "score --unshare-all as its six-flag expansion, with user and cgroup try-else-skip"; its only shared content words are `unshare` and `user`.

`reviews.json` written to `/tmp/tameshi-r45-CritJudge03/reviews.json` (3 entries, reviewer CritJudge03, report `.ufo/waves/round-45/w2/CritJudge03.md`).

## Provenance — sha256 comparisons

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-CritJudge03/S###.live '<url>'
$ gunzip -c <(git show ad5942c:...sources/S###.raw.gz) | sha256sum
$ sha256sum /tmp/tameshi-r45-CritJudge03/S###.live
```

```
S003  entry raw_sha256  4ae955dd4806682d268cd840ff268510255ec126405766598ae130fd96bae1cd
S003  snapshot         4ae955dd4806682d268cd840ff268510255ec126405766598ae130fd96bae1cd  (33898 bytes)
S003  live 2026-10-25  4ae955dd4806682d268cd840ff268510255ec126405766598ae130fd96bae1cd  (33898 bytes)  EQUAL

S076  entry raw_sha256  db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254
S076  snapshot         db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254  (61334 bytes)
S076  live 2026-10-25  db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254  (61334 bytes)  EQUAL

S093  entry raw_sha256  f8a95822f7277eae4809c664bef2e6b1ca0749f4cb6fb373c123f4c9c303e240
S093  snapshot         f8a95822f7277eae4809c664bef2e6b1ca0749f4cb6fb373c123f4c9c303e240  (601469 bytes)
S093  live 2026-10-25  1cacfaf80f4aa6a7b67a8d51db8330f1ffd9f37d9c330e6b09dc576476fac585  (601469 bytes)  DIFFERENT
```

S093 live-vs-snapshot is dynamic GitHub chrome only: 434 differing bytes, all in `fetch-nonce`, `request-id`, `html-safe-nonce`, `visitor-payload`/`visitor-hmac`, tooltip UUIDs, `uploadToken` and `fileTreeProcessingTime` (`cmp -l` + `diff`). The normalized text is byte-identical:

```
$ measure.py --extract S093.snap | sha256sum   -> 76d29fbe588b36ae50f16f98dc74d14ffc3146bfda4fc4be19241c66e0d1228a
$ measure.py --extract S093.live | sha256sum   -> 76d29fbe588b36ae50f16f98dc74d14ffc3146bfda4fc4be19241c66e0d1228a
```

and the quote is present in today's live text (`found=True`, both snapshot and live; same for S003 and S076). So provenance is **not** the ground for the S093 dispute — the quote is located, at the anchor, and live. The ground is what the quote says.

## Located context

S003 (row `corpus/SOURCES.md:14`; quote 18 tokens):
```
... Detecting test changes is only supported if the test runner plugin supports reporting test locations. (see support table below)
[Any other changes to your environment are not detected, such as updates to other files, updated (dev) dependencies]
, changes to environment variables, changes to .snap files, readme files, etc. Static mutants don't have test coverage ...
```
Section check: `t.rfind('Limitations', 0, quote_idx)` = 3062, quote at 3577 — inside the §Limitations list that the anchor names ("§Incremental mode and §Limitations"). Body content, not nav/title/footer. Supports teaches ("env vars, dependencies and .snap files are not detected"): the quoted clause states environment changes are not detected and gives updated (dev) dependencies as the example. Shared content words: `dependencies`, `detected`, `files`. Not copied from the row cells (row wording differs).

S076 (row `corpus/SOURCES.md:85`; quote 23 tokens):
```
... it may be easier to keep track of what is going on if you mostly use read-only git commands and use jj to make changes to the repo.
[One reason for this (see below for more) is that jj commands will usually put the Git repo in a "detached HEAD" state]
, since in jj there is not concept of a "currently tracked branch". Before doing mutating Git commands ...
```
Paragraph check (raw HTML, `<p>` count between `<h2 id="colocated-jujutsugit-workspaces">` at 49563 and the quote at 50510): 3 paragraphs, quote inside the 3rd (`It is allowed to mix jj and git commands ... One reason for this ...`). So the row's "¶3, not ¶2" supersession claim is true of today's bytes. Complete clause, states the detached-HEAD fact. Shared content words: `commands`, `detached`, `head`, `repo`, `state`, `usually`.

S093 (row `corpus/SOURCES.md:102`; quote 25 tokens — the cap):
```
< term >< option >--unshare-all</ option ></ term > < listitem >< para >Unshare all possible namespaces. Currently equivalent with:
[< option >--unshare-user-try</ option > < option >--unshare-ipc</ option > < option >--unshare-pid</ option > < option >--unshare-net</ option > < option >--unshare-uts</ option >]
 < option >--unshare-cgroup-try</ option ></ para ></ listitem > </ varlistentry > ...
```
It sits at the anchor (`bwrap.xml:403`, `:412-416` region, the `--unshare-all` varlistentry) but the span starts one clause too late and stops one flag too early. Teaches cell (`corpus/SOURCES.md:102`, cell 7): "score --unshare-all as its six-flag expansion, with user and cgroup try-else-skip, and score every other flag on its own sentence; the word all is not a sealed isolation claim". The quote contains none of the three load-bearing elements: not `--unshare-all` (the subject), not "Currently equivalent with" (the assertion that makes the list an expansion), not `--unshare-cgroup-try` (the sixth flag and the cgroup try-else-skip half of the claim). A 25-token quote that does carry the assertion exists: `Unshare all possible namespaces. Currently equivalent with: < option >--unshare-user-try</ option > < option >--unshare-ipc</ option > < option >--unshare-pid</ option >` (22 tokens), so the omission is a choice, not a length limit.

The author's own report states the gap: `.ufo/waves/round-45/w1/ExecRows17.md` — "quote covers `--unshare-user-try` through `--unshare-uts`, and `--unshare-cgroup-try` follows in the same sentence at extract index ~11490 with 'Create a new cgroup namespace if possible else skip it'". The ledger entry carries no `note` (`.ufo/evidence/round-45/freshness/ledger.json:534`), so nothing in the ledger asserts the support either.

Mechanical grade (why this is a semantic dispute, not a counter failure):
```
$ measure.py --lane <lane> --rev 3310e7be... --check /tmp/tameshi-r45-CritJudge03/S093.frag.json
CHECK S093 verified ok
```
The counter's overlap rule is satisfied only by vocabulary: `words(quote) & words(scope+anchor+teaches)` = `['unshare', 'user']` (`unshare` from the `--unshare-*` stems, `user` from teaches' "with user and cgroup try-else-skip"). Two generic words, no statement. This is the "only shares vocabulary" / "truncated so that it no longer says the claim" case the falsify item defines as a dispute.

## Collateral observation (not a dispute ground)

S093's registry anchor pins `xml sha256 2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da (33289 bytes)` — the raw `bwrap.xml`. The entry's `raw_sha256` (`f8a95822…`, 601469 bytes) is the GitHub blob **HTML** page that embeds it. Both are legitimate fetches of the row's own URL, but they are different objects, so the entry's digest can never be compared with the anchor's pin. Same finding as `.ufo/waves/round-45/w2/ConnDriftAnchors.md:72`. No counter rule is broken by this; flagging it so the L1 does not treat the entry hash as a confirmation of the anchor's XML pin.

## Commands

- `git show ad5942c6e9858af19d00000b58439b321ddfa62b:.ufo/evidence/round-45/freshness/ledger.json` -> `/tmp/tameshi-r45-CritJudge03/ledger.json`
- `curl -fsSL -A 'Mozilla/5.0' --max-time 90` for the three row URLs (all exit 0)
- `gunzip -c <(git show ad5942c:…/sources/S###.raw.gz) | sha256sum`
- `measure.py --extract` on snapshot and live bytes for each id; `measure.py --lane … --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check S###.frag.json` (all three `verified ok`)
- `cmp -l`, `diff` on S093 snapshot vs live; paragraph/heading counting on S076 raw HTML; `measure.py` module import to list the shared content-word set per row

Lane was not written except this file; no git/jj mutating command was run.
