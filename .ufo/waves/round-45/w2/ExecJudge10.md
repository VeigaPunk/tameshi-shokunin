seat: ExecJudge10

# Round-45 w2 — C1 falsify review of S059, S066, S096

Inputs read: `.ufo/evidence/round-45/contract.json` (frozen, not edited), the wave-1 ledger
`.ufo/evidence/round-45/freshness/ledger.json` at commit `ad5942c6e9858af19d00000b58439b321ddfa62b`
(73 entries; the three entries below are byte-identical to the worktree copy), the three committed
snapshots `.ufo/evidence/round-45/freshness/sources/{S059,S066,S096}.raw.gz` read out of that same
commit, the registry rows in `corpus/SOURCES.md:68,75,105`, and the author reports
`.ufo/waves/round-45/w1/ExecRows08.md` (S059), `ExecRows11.md` (S066), `ExecRows18.md` (S096).
I am the author of none of the three entries; reviewer id ExecJudge10 differs from every author.

## Verdicts

S059 agree — reviewer ExecJudge10 — sha equal (my 2026-10-25 live fetch = entry raw_sha256 `c9653cfb…` = gunzipped snapshot, 250675 bytes both); the 9-token quote is the body paragraph of the "Bazel does not track tools outside a workspace" item inside the page's Known issues section (section heading at normalized offset 13655, quote at 14724, raw HTML `<span data-as="p">`), and the sentence after it states that two users with different compilers wrongly share cache hits because the outputs differ but the action hash is the same — the row's documented false-hit class for inputs outside the key, so it supports `teaches`.
S066 agree — reviewer ExecJudge10 — sha equal (`6fd09811…`, 243776 bytes both); the 18-token quote is body prose of §6 Numbers (heading `6 . Numbers` at normalized offset 12021, quote at 12594) immediately before the `number = [ minus ] int [ frac ] [ exp ]` grammar and states verbatim that numeric values the grammar cannot represent, such as Infinity and NaN, are not permitted, which is the row's `teaches`.
S096 agree — reviewer ExecJudge10 — sha equal (`95572c73…`, 51137 bytes both, matching the row's anchored 51,137-byte 2026-10-23 fetch, i.e. the page is unchanged); the 22-token quote is the first body paragraph of the "Documentation tests" chapter inside `<main><h1 id="documentation-tests">` (raw offset 14259), not nav/help chrome, and states that rustdoc executes documentation examples as tests so examples stay up to date and working — the row's `teaches`.

No dispute. Quote lengths are 9 / 18 / 22 whitespace tokens (inside 6–25); distinct content-word
overlap with scope+anchor+teaches is 5 / 6 / 6 (inside `bazel track tools outside workspace`,
`numeric values cannot grammar infinity permitted`, `rustdoc documentation examples tests date
working`), all ≥ 2; and each quote is not a substring of the folded source/scope/anchor/teaches
cells (checked explicitly: False for all three — S059's anchor carries the near-miss "Bazel does not
track tools outside a workspace" while the quoted body sentence reads "Bazel currently does not
track tools outside a workspace", and the raw HTML confirms the body sentence, so this is located
text, not a copy).

## sha256 comparison (live today vs entry vs committed snapshot)

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
1f9266ac6d4a107a16ca80a2b81c985df5ecad14
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecJudge10/S0XX.live '<url>'   # rc=0 for all three
$ sha256sum S059.live S066.live S096.live
c9653cfb149e45d3c2bfdc54b56dc21ae508040e1e29db9c06b138433ebd55c7  S059.live   (250675 bytes)
6fd09811202d477f54aa65ef3f3e9d4caba2cf6ab4ab8b235b2ca774da419f4c  S066.live   (243776 bytes)
95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7  S096.live   (51137 bytes)
$ git -C … show ad5942c6…:.ufo/evidence/round-45/freshness/sources/S0XX.raw.gz > S0XX.committed.gz
$ gunzip -c S0XX.committed.gz | sha256sum
c9653cfb149e45d3c2bfdc54b56dc21ae508040e1e29db9c06b138433ebd55c7  -
6fd09811202d477f54aa65ef3f3e9d4caba2cf6ab4ab8b235b2ca774da419f4c  -
95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7  -
```

Live == entry `raw_sha256` == committed snapshot for all three: provenance confirmed, no dynamic
chrome drift, so the extract-fallback path was not needed. The same three quotes are also present
in today's live text (`measure.py --extract S0XX.live`, exit 0 each).

## Located context (a few words either side, normalized snapshot text)

- S059 (`S059.snap`, offset 14724): `… have an old /etc/bazel.bazelrc file. `**`Bazel currently does not track tools outside a workspace.`**` This can be a problem if, for example, an action uses a compiler from /usr/bin/ . Then, two users with different compilers installed will wrongly share cache hits because the outputs are different but they have the same action hash.` Preceded by the `<strong>` item heading "Bazel does not track tools outside a workspace", inside Known issues (offset 13655) after the "Environment variables leaking into an action" item.
- S066 (`S066.snap`, offset 12594): `… The E and optional sign are followed by one or more digits. `**`Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted.`**` number = [ minus ] int [ frac ] [ exp ] …` (raw HTML confirms the `6 . Numbers` selflink heading precedes this prose; the offset-25440 "6. Numbers" hit is the table of contents, not the section).
- S096 (`S096.snap`, offset 256): `… The rustdoc book Documentation tests `**`rustdoc supports executing your documentation examples as tests. This makes sure that examples within your documentation are up to date and working.`**` The basic idea is this: …` Raw markup: `<main><h1 id="documentation-tests">…</h1><p><code>rustdoc</code> supports executing your documentation examples as tests. This makes sure that …</p>`.

## Counter helper (never a measurement)

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --check /tmp/tameshi-r45-ExecJudge10/S059.entry.json \
    --snapdir /tmp/tameshi-r45-ExecJudge10 --lane …/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179
CHECK S059 verified ok   (rc=0)
CHECK S066 verified ok   (rc=0)
CHECK S096 verified ok   (rc=0)
```

(`--check` with `--snapdir` reads my locally gunzipped copies, whose hashes equal the entries'
`raw_sha256`; the `--rev` used is the allowed freeze rev. No deciding run was executed by me.)

## Handoff notes for L1

- My review set is at `/tmp/tameshi-r45-ExecJudge10/reviews.json` (3 entries, verdicts `agree`); I am
  read-only on the lane, so the L1 must merge it into
  `.ufo/evidence/round-45/freshness/reviews.json` at the deciding revision. The counter also requires
  reviewer seat `ExecJudge10` to appear with non-empty output in the orchestrator-written
  `.ufo/waves/round-45/w2-results.json`, and this report names each id and the reviewer string.
- Lane checkout untouched: only this report file was written; all scratch under
  `/tmp/tameshi-r45-ExecJudge10/`; git was used read-only (`rev-parse`, `show`, `cat-file -e`).
- No tools installed or upgraded this seat (existing `curl`, `python3`, `gzip` sufficed).
