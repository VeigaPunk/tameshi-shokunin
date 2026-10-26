# T48A2CritC2Design — C2: what `refreshed=4` actually establishes

Attacked: contract C2 (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/contract.json`,
statement + amendments 1, 2, 8) and its frozen counter
`.ufo/evidence/round-48/freshness/measure.py` (sha256 `faefe9b4…` = `freeze-2.json`, byte-identical
at `7552984` and `c7586b9`; selftest 43/43 in my own run). I am not an author of the C2 records,
counter, controls or lesson.

Scratch: `/fast/scratch/hyaku/tameshi-r48/T48A2CritC2Design` (`TMPDIR` there), `git clone -q --shared`
of the lane for every commit; the lane checkout was read only (`git -C LANE show`), no git/jj
mutation in it. No tool installed or upgraded. Scratch deleted before yield (last section).

## 0. Milestone answer

**No — `refreshed=4` does not mean each held row is re-anchored against the live source this round.**
It means: for each target, an author-chosen quote of ≤25 words (0.30 %–3.54 % of the document's
extracted text) is still a substring of today's live extraction, *and* a lane-authored snapshot +
receipt agree with each other. Nothing binds the snapshot to live bytes, to this invocation, or to an
authorship event; nothing checks any live text outside the quoted span.

Reproduced in a clone at `c7586b9` (the content revision) with live on — i.e. the predicate the L1
will run:

```
TARGET S026 … entries=ok live=ok REFRESHED
TARGET S048 … entries=ok live=ok REFRESHED
TARGET S093 … entries=ok live=ok REFRESHED
TARGET S108 … entries=ok live=ok REFRESHED
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=on rev=c7586b9… C2_R48_PASS=true
```

So C2 will pass. The findings below are about what that pass is worth, and the two constructions in
F1/F2 show the same predicate printing `C2_R48_PASS=true` for material that is not re-anchored.

What actually moved in the source this round (round-45 snapshot vs round-48 snapshot, extraction =
amendment 2):

| T | r45 raw sha / B | r48 raw sha / B | bytes equal | extracted text equal |
|---|---|---|---|---|
| S026 | `5d74dd1c3c75` 236387 | `a4c5c46b4af9` 236387 | no | **yes** (26246 chars) |
| S048 | `e9cbc3e1ab7c` 8892 | `e9cbc3e1ab7c` 8892 | **yes** | yes (3253) |
| S093 | `f8a95822f727` 601469 (blob page) | `2cb77df2f4be` 33289 (raw tag) | no (different document form) | no |
| S108 | `9056c530ca6c` 111409 | `04e4c091715a` 111409 | no | **yes** (3496 chars) |

Three of four target documents are textually unchanged (S048 byte-identical to its round-45 snapshot
and to the 2026-10-20 fetch recorded in `corpus/knowledge/incremental-pin-disposition.md`,
`e9cbc3e1ab7c`, 8892 B); S093's round-48 bytes are the round-30 pin. The round's real delta is
*anchoring/receipt* evidence, not new source content — which is fine, but it is not what the word
"re-anchored" invites a reader to assume, and (F1) the counter cannot tell that case apart from the
stale-bytes case anyway.

## F1 (major) — the live check is a substring test of the author's quote; snapshots and receipts are unbound

`measure.py:336-350`: `check_live` fetches `receipt['url']`, and returns
`'ok' if quote in extract(raw) else 'absent'` (`:350`). It never compares the fetched bytes, their
length, their normalised text, or the document identity with the committed snapshot, and
`check_receipt` (`:263-290`) only proves the receipt agrees with the snapshot (`sha256` at `:280`,
`bytes` presence at `:282`) and with itself (`fetched_at` prefix at `:276`). The receipt is
lane-authored text; amendment 4 rejected exactly this kind of unbound text for C1 attestation, and
C2 still pays on it.

Strongest demonstration (scratch clone of `c7586b9`, one commit `5b6a542`, live on):
replace `sources/S026.html` with a 111-byte locally authored paragraph containing only the quote,
re-point `S265`'s anchor at its sha, rewrite the Gate line as `- C2-QUOTE S265 S026: \`84%\``
(a 1-token quote — legal: `REQUIRED['S026'] = ('84%',)` at `:87`, so the required phrase is a
3-character substring), and set the receipt `bytes` to `1`:

```
TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
… (S048, S093, S108 unchanged) …
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=on rev=5b6a542… C2_R48_PASS=true
```

Nothing in that snapshot was fetched from any URL; the receipt's byte count is false; the only
live-bound fact is that `84%` occurs somewhere in today's page. Independently, the lane's own
`CTL_H` fixture, which copies **round-45** bytes and stamps receipts `2026-10-26T00:00:00Z`, when
scored **live** (`6abc4c2`, built by `.ufo/evidence/round-48/control/c2-controls.py`) prints

```
TARGET S026 … live=ok REFRESHED      TARGET S108 … live=ok REFRESHED
C2_R48: self_pin=1 targets=4 refreshed=2 census_exit=0 live=on rev=6abc4c2… C2_R48_PASS=false
```

i.e. the cheapest control's two "credited" targets are credited by the *live* branch too. The
control set therefore contains no case that exhibits the live check discriminating at all (the
selftest's `live_absent`/`live_unreachable` use fake pages, and the controls run `--no-live`).

Location of the drift this tolerates is already visible in the delivered records: today's live S026
is `dfea6b9ba734` (236387 B, twice, curl and `live_fetch`) — not the committed `a4c5c46b4af9` — and
today's live S108 is a new digest on every fetch (F3). The extracted text happens to be identical
today (§0 table), which is why the pass is not *currently* hiding a text change; the design cannot
distinguish that case from one where it would.

Impacted axes: freshness (evidential strength of C2). Smallest safe correction, none available
pre-scoring (F7 is why): the *reading* must be the contract's — "the four quotes are still live" — and
any SCORECARD sentence that says the four rows were re-anchored to the live source should be
narrowed; for a later round, make the receipt's `bytes` equal the snapshot length, and add a live
fetch of the extracted text's normalised digest (or of `T`'s base URL) instead of the quote.

## F2 (major) — a target is credited while its entry claim is contradicted by the live page

`check_entries` (`:318-334`) tests only that each base used-by entry's `source:` line names `R` and
that a `verified-at:` line contains `2026-10-26`; the entry's content is never read against the
source. Combined with F1, the live check protects only the quoted span. S026's `teaches` claims
three things (1.5 % flaky runs, 84 % of transitions, the fail-3-in-a-row mark); the quote covers only
the 84 % sentence (78 of 26246 extracted characters, **0.30 %**).

Demonstration (same clone, `fetch` replaced by a function returning each committed snapshot with one
sentence appended — no fabricated page, the real document plus a retraction), live on:

```
TARGET S026 … live=ok REFRESHED   (page appended: "the 84% figure is retracted; do not cite it")
TARGET S048 … live=ok REFRESHED   (page appended: "prioritisation advice withdrawn")
TARGET S093 … live=ok REFRESHED   (page appended: "--unshare-all semantics changed")
TARGET S108 … live=ok REFRESHED   (page appended: "--update_goldens removed; .expected files are no longer checked")
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=on rev=c7586b9… C2_R48_PASS=true
```

The predicate prints PASS with every entry's claim contradicted on the live page. The lane is aware
that a text comparison is needed — `corpus/knowledge/r8-golden-update-flag.md`'s `verified-at` line
states it did "a line diff against today's live fetch (104928 B)" by hand — but that diff is lane
prose, not something the counter executes.

Impacted axes: freshness, and the provenance of the four entries' `verified-at: 2026-10-26` claims
(the date is asserted, not observed). Smallest safe correction: record in the round report that
`verified-at: 2026-10-26` on these entries is an author assertion whose only counter-checked part is
the quote; a future counter should diff the snapshot's extraction against the live extraction and
require the diff to be empty outside the head/script blocks (the method the entry's own prose uses).

## F3 (moderate) — S108: byte-variant serving makes the receipt sha unreproducible and the one-shot deciding run variant-dependent

The counter is right to ignore bytes for this page: in 15 live `?hl=zh-cn` fetches today (5 through
the counter's own `live_fetch`, 10 via curl with five User-Agent strings, two `hl` spellings and
Accept-Language variants) I saw **at least 13
distinct byte strings** at 111405/111409 B, every one of them extracting to the same 3496-character
text with the lesson quote present (one Googlebot-UA fetch: 112362 B, 3944 chars, quote present).
Consequences, all visible in the frozen design:

- The committed snapshot `04e4c091715a` can never be re-derived: no fetch I made reproduced it, so
  "sha256 equal to the snapshot's" (`:280`) reduces to self-consistency and `FROZEN_UNCHANGED` can
  pin an artifact nobody can reproduce.
- A parameter drop fails closed but for a routing reason: `/federated/golden_tests` without
  `hl=zh-cn` returns 112712 B, extracts 6087 chars, and does **not** contain the Chinese quote, so
  `check_live` would print `live=absent` → `refreshed=3` → miss.
- The lesson records a second zh-cn text variant (3148 chars, 1 of 6 extractions on 10-25). It says
  both carry `--update_goldens`; it does **not** say both carry the six-token quote, and I could not
  reproduce the 3148 variant today. If the deciding run is served it, `live=absent` follows, and
  amendment 8 forbids a second invocation — a one-shot verdict on a CDN variant.

Impacted axes: freshness (robustness of the deciding run, not of the claim). Smallest safe
correction: none pre-scoring; the round report should state that a `live=absent` on S108 is
indistinguishable from variant routing and that the predicate's one-shot rule makes that an
irrecoverable miss. A later counter should accept any live extraction that contains the quote *and*
show the served digest, so a miss is attributable.

## F4 (moderate) — one of the four "live re-anchors" is an identity and cannot detect the change its cadence names

`S267`'s receipt URL is `https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml`
(`.ufo/evidence/round-48/freshness/sources/S093.receipt.json`), a tag-pinned blob: today's fetch is
byte-identical to the snapshot (`2cb77df2f4be`, 33289 B). `check_live` therefore re-tests an
immutable object; the counter never fetches `T`'s base URL (the GitHub blob page, which is what the
registry row names and what the round-45 ledger fetched at 601469 B — the blob-page rendering of the
same XML, sha `f8a95822f727`) and contains no release check
(`grep -n 'release' .ufo/evidence/round-48/freshness/measure.py` → only `:490`,
`BASE_RECHECK = {… 'on-release' …}`, a selftest constant; no code path reads a tag or a release).
The row's recheck is
`on-release`, so the only freshness event that cadence names is "a newer bubblewrap release", which
this predicate cannot see. `https://api.github.com/repos/containers/bubblewrap/releases/latest` →
`v0.13.1 2026-10-14` today, so nothing is being missed *now*; the design would miss it tomorrow.

Impacted axes: freshness (S093's contribution to `refreshed=4` carries no this-round information).
Smallest safe correction: when the receipt URL is a tag-pinned raw blob, require a latest-release or
`HEAD`-of-branch probe (or record `live=identity` separately and exclude it from `refreshed`).

## F5 (minor, implementation vs its own docstring) — receipt `bytes` is presence-only

`:282` is `if 'bytes' not in data: return data, 'bytes'`. The docstring (`:34`) lists `bytes` as a
graded receipt field, and the value is never compared with `len(snapshot)`. Demonstration: F1's
clone passed with `"bytes": 1` next to a receipt `sha256` over a 111-byte snapshot. Consequence: a
lane cannot be caught mislabeling the fetched size, which is the one receipt field a reader would use
to notice a truncated/consent-page fetch. Smallest safe correction:
`str(len(raw)) == str(data.get('bytes'))` in `check_receipt` (needs the snapshot length passed in),
or delete the field from the docstring's graded list.

## F6 (minor) — "located in the snapshot's extracted text" can be a stitched passage

Amendment 2 replaces tags with a space, so a quote can cross element boundaries. S093's 25-word
quote does: raw bytes 5909-6400 show `--unshare-cgroup-try … else skip it</para></listitem>
</varlistentry> <varlistentry> <term><option>--unshare-all</option> …`. The live check then verifies a
concatenation that the page never renders as one passage. This is legal under the amendment and
harmless for credit, but `S267`'s cell reads as if both flags were documented together; the quote is
two `varlistentry` blocks plus their tags. Peer `T48W2CritC2Cheat` already notes the stitching; I add
the byte range and the extraction consequence. Smallest safe correction: report the offset range as
"lines 153-160, two varlistentries" (already in the anchor cell) and read the quote as two clauses.

## F7 (minor, contract vs script) — amendment 8 promises a frozen-set member the deciding script omits

Amendment 8 says `FROZEN_UNCHANGED` is recomputed over "both counters, statements.json, this
contract and the C2 snapshots"; `.ufo/evidence/round-48/deciding-run.sh:22` omits
`$E/freshness/sources`. The omission is load-bearing: the records commit (`5054532`) postdates the
freeze (`7552984`), so including the sources would make `FROZEN_UNCHANGED=0` and the deciding run
would exit non-zero. Peer `T48W2CritC2Rows.md:201` records the same omission. Either fix the
amendment text or freeze the snapshots in step 2; the current state is an unimplemented promise, not
a hole (everything is read at a fixed `REV`).

## What the design does establish (so the judge does not over-reject)

- `unreachable` is never credited: probe with a raising `fetch` at `c7586b9` →
  `live=unreachable` on all four, `refreshed=0`, `C2_R48_PASS=false`; selftest cases 41-42 pass.
- Row/gate/phrase/entry/census structure is genuinely enforced (43/43 selftest, and my runs returned
  `census_exit=0`); `self_pin=1`; the counter is byte-identical to `freeze-2.json`.
- The four quotes are live **today**: S026 2/2 probes, S048/S093 one each, S108 15/15 zh-cn probes.

## Verdict shape for the canonical judge

The frozen predicate is implemented faithfully and will print `C2_R48_PASS=true`; no control or
counter bug makes it print that on a tree that lacks the specified artifacts. But the claim's prose
("re-anchored against the live source this round") is stronger than the predicate: the pass is
(a) quote-substring, (b) unbound-snapshot, (c) blind outside 0.3 %–3.5 % of each document, and
(d) vacuous for the one tag-pinned target. The milestone question is answered *no* at the byte/
provenance level and *yes* only at the fragment level; C2 should be credited as "four frozen quotes
re-confirmed live against receipts the lane authored", and the deriver should not credit any
stronger reading.

## Scratch / tooling

`S=/fast/scratch/hyaku/tameshi-r48/T48A2CritC2Design` (`$S/lane` clone at `c7586b9`, `$S/syn` clone
with the synthetic commit `5b6a542`, `$S/ctl` control clone at `6abc4c2`, fetched pages) — `rm -rf`
run before yield. Disk guard: `/fast/scratch/hyaku` 26 % used, 598.8 G free. No pacman transaction,
no tool install. Every git call named `-C "$D"`; fixture toplevels verified with
`rev-parse --show-toplevel`.
