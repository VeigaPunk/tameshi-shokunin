# T48W2RefetchS093 — independent re-open of target S093 (claim C2)

Seat: T48W2RefetchS093 (leaf, freshness). Attacks: C2 target S093 only. Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, CONTENT revision
`c7586b9a10effc63b4bd327f976edc094c1bdc17` (HEAD `17cc5ce` adds only the a2w1 wave spec:
`git diff --stat c7586b9a..17cc5ce -- corpus/ tools/ SCORECARD.md` is empty). I am not an author of
what I attack; the only counter execution below is a `--no-live` probe, explicitly not a verdict.

## Bottom line

S093 re-opens **clean at every check the contract makes measurable outside the deciding run**:
the superseding row S267, the committed snapshot and receipt, the Gate quote (25 tokens, located
once in both snapshot and live text, both required phrases) and the citing entry all hold against
a live fetch whose bytes are **identical** to the committed snapshot. One citing-entry sentence
("with a cleared environment") is imprecise against the live `--clearenv` text; it is already
disclosed and corrected by the entry's own errata E1, so it is not a silent stale claim. One
quote-support gap (the teaches cell's user-flag clause sits outside the quote) is noted, not a
contract failure. No action requested of the L1.

## 1. Live fetch (independent)

```
S=/fast/scratch/hyaku/tameshi-r48/T48W2RefetchS093; export TMPDIR="$S"
curl -sS -L -o S093.live.xml -w 'http_code=%{http_code}\nbytes=%{size_download}\nurl=%{url_effective}\n' \
  https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml
sha256sum S093.live.xml; wc -c S093.live.xml
```

| field | observed |
|---|---|
| HTTP | 200 |
| bytes | 33289 |
| sha256 | `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da` |
| url | `https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml` |
| fetch time | 2026-10-26T13:29:33Z (file mtime 10:29:33 -0300) |
| tool | curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 |

- `cmp S093.live.xml .ufo/evidence/round-48/freshness/sources/S093.xml` → identical; the
  content-revision blob (`git show c7586b9a:.ufo/evidence/round-48/freshness/sources/S093.xml`)
  is also byte-identical. So "located live" and "located in the snapshot" are the same bytes here,
  not merely the same digest.
- Receipt `.ufo/evidence/round-48/freshness/sources/S093.receipt.json` (blob sha256
  `ab26b08449e3754ae8199474c9a24387e9a95d1555e7ccfe1c864b7bb09ec1cc`, equal at worktree and
  CONTENT) states url = the fetched raw URL, `fetched_at 2026-10-26T08:41:10Z`, `http_status 200`,
  `bytes 33289`, `sha256` = the digest above. All four match. Amendment 1 holds: S093's base URL
  (github.com/…/blob/v0.13.1/bwrap.xml) and the receipt URL (raw.githubusercontent.com) both occur
  in S267's source/anchor cells.
- Annotated tag check: `git ls-remote https://github.com/containers/bubblewrap 'refs/tags/v0.13.1*'`
  → `362936aea0d5c6e70f7af75d2d44b5a914cb4ba2  refs/tags/v0.13.1^{}`, equal to S093's and S267's
  pinned commit.

## 2. Superseding row S267 (`corpus/SOURCES.md:142`)

`grep -n 'supersedes S093 —' corpus/SOURCES.md` → exactly one line, 142. Parsed as 11 cells
(`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`, header line 10):

- id `S267` (> S264); kind `docs`; tier `A`; status `mined`; opened `2026-10-26`; recheck `on-release`.
- source cell carries S093's base URL and, parenthetically, the raw URL.
- anchor cell carries `sha256 2cb77df2f4be` (12 hex, matches the snapshot prefix) and
  `§Options … raw lines 153–160 (the quote spans lines 154–159, bytes 5909–6400)`.
- teaches cell opens exactly `supersedes S093 —`.
- used-by cell is exactly `corpus/knowledge/regression-tally-completeness.md`, which is exactly
  S093's base used-by cell (`git show 473336d:corpus/SOURCES.md`, row at line 102).

Anchor coordinate check against the live bytes (`nl -ba`, byte offsets computed from the raw file):

- lines 153–160 are the two `varlistentry` blocks `--unshare-cgroup-try` (153–156) and
  `--unshare-all` (157–160);
- first `--unshare-cgroup-try` token starts at raw byte **5909** (line 154,
  `      <term><option>--unshare-cgroup-try…`); the last `--unshare-cgroup-try` token ends at raw
  byte **6400** (line 159, `…<option>--unshare-cgroup-try</option></para></listitem>`).
  The row's `5909–6400` span is exact.

S093's other anchor refs were re-read live and still land on the claimed text: `:159` = the
`--unshare-all` sentence; `:233-235` = `--clearenv`; `:403` = `--proc`; `:412-416` = `--tmpfs`;
`:575-577` = `--new-session`; `:589-592` = `--die-with-parent`. README at the same tag still has the
"security boundary … entirely determined by the arguments" passage at 52–54 and the mount-namespace
passage at 133 (fetched live, 10687 B, sha256 `0c1dc12c6d94017c…`).

## 3. Gate quote (`corpus/lessons/round-48.md:23`)

Line 23: `- C2-QUOTE S267 S093: \`…\`` — exactly one S093 gate line; R = S267, T = S093.

Quote (whitespace-collapsed): `--unshare-cgroup-try Create a new cgroup namespace if possible else
skip it --unshare-all Unshare all possible namespaces. Currently equivalent with:
--unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try`

Extraction replicated per amendment 2 (exactly `measure.py:166-177`: UTF-8 decode, drop
`script`/`style` contents, strip tags, `html.unescape`, collapse whitespace):

| check | observed | verdict |
|---|---|---|
| token count (whitespace split) | **25** | PASS (at the cap: any added token fails) |
| located in snapshot extraction | once, normalized offset **2641** of **16699** chars (matches lesson:52-54) | PASS |
| located in live extraction | once, offset 2641 of 16699 | PASS |
| byte-exact after whitespace collapse | extracted slice == quote exactly (`repr` compared) | PASS |
| required phrases S093 (`--unshare-all`, `--unshare-cgroup-try`) | both present | PASS |
| states the teaches claim, not boilerplate/navigation | yes for the six-flag equivalence, the six flag names, and `--unshare-cgroup-try`'s "if possible else skip it"; the teaches cell's **user-flag** try-else-skip clause is **not inside the quote** (it is live at raw lines 130–131, which the lesson Scope at :57-64 also cites as outside the quote) | PASS-WITH-GAP (O1) |

The quote is substantive: it is the two consecutive varlistentry bodies, in document order, and it
reaches the sixth flag and its try-else-skip wording whole. It does not resolve `--unshare-all` to
a sealed-isolation claim; the live text's own "all possible namespaces" supports the row's
"not a sealed isolation claim" reading.

## 4. Citing knowledge entry (`corpus/knowledge/regression-tally-completeness.md`)

The entry is byte-identical at worktree and CONTENT (sha256 `c5a8b799734f8c49…`); S093's base
used-by names only this entry, and S267's used-by names only this entry.

Pointer checks: `source:` line 1 cites `S267` (and still describes S093 as the sandbox doc);
`verified-at: 2026-10-26` line 2. PASS.

Every S093-resting claim, checked against the live text:

| entry claim | live evidence | verdict |
|---|---|---|
| L1 `S093 — bwrap(1), bubblewrap 0.13.1 bwrap.xml (the sandbox the v4 counter runs each selftest in)` | v4 counter `BWRAP = ['bwrap', …]` (`.ufo/evidence/round-30/c1-measure-v4.py:321`) | holds |
| L2 "with the six `--unshare-all` flags and both try-else-skip sentences re-read", digest/bytes unchanged | six flags at line 159; user-try "if possible else skip it" lines 130–131; cgroup-try lines 154–155; sha/bytes as above | holds |
| L42 v4 row "runs each `--selftest` in a bubblewrap sandbox (S093) **with a cleared environment**" | live `--clearenv` (233–235): "Unset all environment variables, **except for PWD and any that are subsequently set by --setenv**"; counter then sets PATH, HOME, LANG, TMPDIR (`c1-measure-v4.py:325-326`) | **imprecise, disclosed** (F1) |
| L68 "S093's `--unshare-all` is six flags, two of them try-else-skip" | six `--unshare-*-try`/plain flags at 159; only `--unshare-user-try` and `--unshare-cgroup-try` carry "if possible else skip it" | holds |
| L68 "not a measured security boundary" | S093's teaches and the README security-boundary passage; nothing measured | holds |
| L72 E1: "S093 bwrap.xml:233-235: `--clearenv` unsets all variables 'except for PWD and any that are subsequently set by --setenv'" | lines 233–235 exactly; fragment present after tag strip/unescape | holds (exact line numbers) |
| L72 E1: "the counter then sets PATH, HOME, LANG and TMPDIR" | `c1-measure-v4.py:325-326` sets exactly those four | holds |

No other knowledge entry cites S093 (`grep -rn 'S093' corpus/` → only this entry, the registry
rows, README index and historical lessons).

## Findings

**F1 (disclosed, non-blocking) — `corpus/knowledge/regression-tally-completeness.md:42`.** The v4
row still says the sandbox runs "with a cleared environment". Against the live document that is too
strong: `--clearenv` (bwrap.xml:233-235) keeps `PWD` and permits later `--setenv`, and
`c1-measure-v4.py:325-326` then sets PATH, HOME, LANG and TMPDIR. The same entry's append-only
errata **E1 at line 72 already states this correction** (it is where the round-30 seats landed it),
so the re-point did not silently re-assert a dead claim and the entry is self-correcting. Shown by:
`sed -n '42p;72p' corpus/knowledge/regression-tally-completeness.md` and
`sed -n '231,236p' <live S093.xml>`.

## Observations (not C2 misses)

**O1 — quote-support gap.** S267's teaches cell (SOURCES.md:142, cell 7) asserts both the user and
cgroup flags are worded "if possible else skip it", but the 25-word quote only reaches the cgroup
sentence (raw 154–155); the user sentence is raw 130–131, outside the quote. The anchor cell is
scoped honestly ("the try-else-skip wording of `--unshare-cgroup-try`"), and the claim is true in
the live document, so this is narrower quote support than the teaches wording, not a false claim.

**O2 — pointer hygiene, outside the C2 predicate.** `corpus/README.md:453` still lists `S093` (not
`S267`) in the source column of the entry's index row, and the entry's `recheck:` line 3 still says
"re-open S087, S093, S094". README is not a knowledge entry in S093's base used-by cell and the
recheck target still resolves (same URL), so neither affects `refreshed`; I am read-only on
`corpus/` and did not touch them.

## Probe (never a verdict)

```
TMPDIR="$S" python3 .ufo/evidence/round-48/freshness/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 --no-live
```

Observed: `TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped
REFRESHED`; overall `C2_R48_PARTIAL=true` (live=off). This only shows the frozen counter parses the
same facts I measured by hand; the live/deciding verdict is the L1's deciding invocation.

## Scratch, tooling, bounds

- Scratch `S=/fast/scratch/hyaku/tameshi-r48/T48W2RefetchS093` held the live fetch and extracted
  README; deleted before finishing (`rm -rf -- "$S"`). No file was written outside this report.
- No tool installed or upgraded. No git/jj mutation in the lane; `git status --porcelain` shows only
  the pre-existing untracked `.ufo/waves/round-48/a2w1/`. No write under `corpus/`, `tools/` or
  `SCORECARD.md`. Disk at the time of the pass: 602G free on `/fast`.
