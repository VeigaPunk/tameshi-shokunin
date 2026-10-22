# Round 28 · wave 1 · RerunCensus — census re-run and S059 row-drift check

Seat: `TameshiR28.RerunCensus` (leaf executor; no subagents dispatched).
Lane: tameshi. Revs compared: base `06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c`
→ head `b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a`.
Tools installed: none. No `pacman`, `uv`, `cargo` or `npm` action was taken;
`bash`, `git` (read-only), `curl`, `python3`, `sha256sum`, `awk`, `grep` were
already present and were the only binaries used.

## Verdict first (per check)

| # | Check | Verdict |
|---|---|---|
| 1 | `sources-census.sh validate --root $W2 tameshi` at head `b05d2ee` | **PASS** — exit 0, `ok` line, 7 W04 warnings, byte-identical finding set to base |
| 2 | same command at base `06b59b93` | **PASS** — exit 0, same 7 W04 warnings |
| 3 | S059 row: only the `used-by` cell may change in place | **PASS** — `used-by` is the single differing cell; the other ten cells and NF=13 are unchanged |
| 4 | appended lookup note and `Next unused id: S092` must be appends | **PASS** — 14 lines appended at 339–352; base lines 1–337 untouched; stale `- Next unused id: S090.` kept at 338; no `S092` row created |
| 5 | fleet-wide sweep (extra coverage, beyond the named checks) | **PASS** — 204-line validate output identical modulo root path, 0 E-codes, both revs; census counters identical |

Two **non-blocking observations** (no defect in `corpus/SOURCES.md`; both are
in the round-28 lesson's `## Gate` prose and concern the re-open record, not
the row) — see *Observations* below. No correction to production files is
warranted; the smallest safe correction for each is stated there.

---

## Evidence

### Setup (mirrors, read-only against the real lane)

```sh
W2=$(mktemp -d /tmp/reruncensus-b05-XXXX)      # -> /tmp/reruncensus-b05-SbAn
cp /home/vgpnk/Projects/shokunin/shokunin.conf $W2/
ln -s /home/vgpnk/Projects/shokunin/scripts $W2/scripts
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W2/tameshi-shokunin
git -C $W2/tameshi-shokunin checkout -q --detach b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a

W3=$(mktemp -d /tmp/reruncensus-06b-XXXX)      # -> /tmp/reruncensus-06b-aYsS
... same three lines ...
git -C $W3/tameshi-shokunin checkout -q --detach 06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c
```

Observed: `HEAD=b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a` and
`HEAD=06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c`. A fleet mirror
(`/tmp/reruncensus-fleet-PcW8`, 20 sibling lane symlinks + the tameshi clone)
and a base-rev fleet mirror (`/tmp/reruncensus-fleetbase-kkKp`) were also built
for the fleet-wide sweep in check 5. Nothing was written inside
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` except this report; no `jj`
command was run anywhere; no git write command (`add/commit/checkout/reset/
stash/push/fetch/pull`) was run in the lane — the two `checkout --detach` calls
above are in the /tmp clones.

### Check 1 — census validate at head `b05d2ee`

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $W2 tameshi; echo "EXIT=$?"
```

Observed stdout (complete) and exit:

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	ok	/tmp/reruncensus-b05-SbAn/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

### Check 2 — census validate at base `06b59b93`

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $W3 tameshi; echo "EXIT=$?"
```

Observed stdout: the same seven `W04` lines with the same ids and the same
`ok` line for `/tmp/reruncensus-06b-aYsS/tameshi-shokunin/corpus/SOURCES.md`;
`EXIT=0`. The two outputs differ only in the temp-root path in the `ok` line.

**Zero `E`-codes at both revs** (`E01`–`E12`): no malformed row, no duplicate
id, no enum violation, no community-at-tier-A, no missing `used-by` path, and
no row-shaped source outside `## Registry`.

Census counters, both revs (from `sources-census.sh census --root $W tameshi`):

```
tameshi	rows	89      tameshi	status.mined	61
tameshi	tier.A	80      tameshi	status.queued	22
tameshi	tier.B	7       tameshi	status.rejected	6
tameshi	tier.C	2
FLEET	rows	89      FLEET	tier.invalid	0   FLEET	status.invalid	0   FLEET	missing	0
```

The lane's own committed receipt agrees with this rerun:
`.ufo/evidence/round-28/census-start.stdout` holds the same seven `W04` lines
and the same `ok` line; `.ufo/evidence/round-28/census-start.exit` holds `0`.

The frozen manual census from `CORPUS.md` §"SOURCES.md — where a shokunin
learns" was also run by hand at both revs and agrees with the script:
rows 89, malformed 0, tiers `A=80 B=7 C=2`, statuses `mined=61 queued=22
rejected=6`, no duplicate ids, no enum violations, no missing `used-by` paths.

### Check 3 — S059 row: in-place change limited to `used-by`

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 06b59b93... b05d2ee... -- corpus/SOURCES.md
```

`--numstat` for the file: `15  1  corpus/SOURCES.md` (15 added, 1 removed).
The single removed line is the old S059 row; the diff hunk
`@@ -65,7 +65,7 @@` shows exactly one `-`/`+` pair, and the tail hunk
`@@ -336,3 +336,17 @@` is pure addition.

Cell-by-cell comparison of the two S059 rows (split on `|`, NF=13 on both
sides, verified `awk -F'|' 'NR==68{print NF}'` → `13` for base and head):

```
SAME id       SAME source   SAME kind     SAME tier    SAME scope
SAME anchor   SAME teaches  SAME status   SAME opened  SAME recheck
DIFF used-by
   old: corpus/knowledge/input-keyed-coldread-credit.md
   new: corpus/knowledge/input-keyed-coldread-credit.md, corpus/lessons/round-28.md
```

`status` stays `mined`, `recheck` stays `90d`, `opened` stays `2026-10-20`.
This is the only mutable-in-place field the contract allows to change
(`CORPUS.md` §SOURCES rule 2: "Only `status`, `recheck` and `used-by` change in
place"), and the change is logged old→new in the round lesson's `## Gate`
(`corpus/lessons/round-28.md:18-20`):

```
- Change log: S059 `used-by` `corpus/knowledge/input-keyed-coldread-credit.md`
  → `corpus/knowledge/input-keyed-coldread-credit.md, corpus/lessons/round-28.md`.
  Status `mined` and recheck `90d` unchanged.
```

Both `used-by` paths exist on disk at the head (census `E11` and the manual
missing-path probe are silent), and `corpus/lessons/round-28.md` really cites
S059 (lines 12, 18, 40), so the second `used-by` entry is truthful.
`git ls-files` confirms both paths are tracked at the head.

### Check 4 — the lookup note and `Next unused id: S092` are appends

Base file: 338 lines. Head file: 352 lines. Line-level comparison of the two
files:

* Base lines 1–337 are **identical** to head lines 1–337 except index 67
  (1-based line 68 = the S059 row) — verified programmatically; the only
  differing base index list is `[67]`.
* Head lines 339–352 are new (blank separator at 339, then the note, then the
  new id line at 352):

```
339:
340: Round28 bounded lookup: re-opened S059, the Bazel Remote Caching page
341: (scripted `curl -sL`, fetched 2026-10-22; "Known issues" still reads "Bazel
342: currently does not track tools outside a workspace"), to name the
343: mechanism the round-28 mistake rests on: the cold-read monitor keys each
344: section's credit to the sha256 of every recorded input, so an append to a
345: widely read lane file (one blank line on SOURCES.md drops 10 sections)
346: misses the old credit the way a changed input misses an action cache.
347: identified1/screened1/included1/excluded0; no new row. S059 `used-by`
348: corpus/knowledge/input-keyed-coldread-credit.md → that path plus
349: corpus/lessons/round-28.md; status and recheck unchanged. The stale
350: `Next unused id: S090` line above stays append-only; S090 and S091 were
351: used in round 27.
352: - Next unused id: S092.
```

* The stale `- Next unused id: S090.` line is **preserved unchanged** at line
  338 in both revs — the append-only pattern the file already uses (the same
  shape is used for the `S065`/`S075` pair at lines 262–264). Nothing was
  edited in place to "fix" it.
* `- Next unused id: S092.` is the **last** line of the file, appended after
  the note, and the file ends with a newline (`tail -c 1` → `0a`).
* **No `S092` row exists**: `grep -c '^| S092 '` → 0; the highest row id in the
  registry is `S091`, and `S090`/`S091` are the round-27 rows
  (`corpus/lessons/round-27.md:36,42`). So `S092` is genuinely the next unused
  id — which is exactly what the round-27 spot-check routed item 3 asked for
  (`corpus/lessons/round-27-verifier-spotcheck.md:194`).
* `git diff --check` between the revs exits 0 (no whitespace damage).

Section placement of the new note: it lands inside `## Id allocation`
(line 246) — the same place the Round23–Round26 bounded-lookup notes occupy
(lines 302, 308, 315, 329). Consistent with the lane's existing pattern, and
the `## Search log` section (110–223) is untouched.

### Check 5 — fleet-wide sweep (extra coverage)

With `shokunin.conf` present in the fleet-mirror root:

* `validate --root $W/fleet` at head → exit 0, 204 output lines, **0 E-codes**.
* `validate --root $Wb/fleet` at base → exit 0, 204 output lines, **0 E-codes**.
* After normalising only the temp-root path, the two 204-line outputs are
  `diff`-identical.
* `census --root $W/fleet` at both revs → `diff`-identical; `FLEET rows 1723`,
  `tier.A 1473`, `tier.B 165`, `tier.C 85`, `tier.invalid 0`,
  `status.queued 267 / mined 1336 / rejected 120`, `status.invalid 0`,
  `missing 0`.
* `sources-census.sh selftest` → exit 0, 96 `killed` lines, 0 `SURVIVED`,
  final line `selftest ok`.

### Source re-open of S059 (the row's cited URL), independently fetched

```sh
curl -sL --max-time 25 https://bazel.build/remote/caching -o /tmp/bazel_caching.html
sha256sum /tmp/bazel_caching.html
```

Observed `9e3a2ebba08234a1b5896faaea54be7c4aea2adb3e1051037f477d8f24d42348`,
297255 B — **identical to the digest the round-28 lesson records**
(`corpus/lessons/round-28.md:13-14`), so the lesson's re-open evidence
reproduces. The two quoted strings are present verbatim in the fetched page:
`does not track tools outside a workspace` (3 occurrences) and
`The action cache, which is a map of action hashes to action result metadata`.
The row's recorded scope therefore still holds.

---

## Observations (non-blocking; no production edit made)

1. **Word-count label in the lesson's `## Gate` is off by one.**
   `corpus/lessons/round-28.md:16` labels the quote
   "The action cache, which is a map of action hashes to action result metadata."
   as "(13 words)"; the token count is **14** (`The action cache, which is a map
   of action hashes to action result metadata.` → 14 whitespace-delimited
   tokens). The contract bound is "≤25-word quote" (`CORPUS.md` §SOURCES rule
   1), so the requirement is met either way — the parenthetical is a
   cosmetic miscount.
   *Smallest safe correction:* change `(13 words)` to `(14 words)` in the
   lesson prose. This is prose, not a registry cell, so it does not touch the
   append-only contract; leave it to the lesson owner (this seat is read-only
   on production files). Severity: cosmetic.

2. **The quote's location label in the same `## Gate` bullet names no real
   heading.** The lesson writes
   `(§Remote Caching intro, "The remote cache stores two types of data")`.
   In the fetched markdown alternate the line
   `The remote cache stores two types of data:` sits at md:32 under the
   heading `## Overview` (md:15); the page headings are
   `# Remote Caching` (md:5), `## Overview`, `## Known issues` (md:321),
   … There is no "intro" heading. The quote itself is verbatim and correctly
   located; only the label is loose.
   *Smallest safe correction:* relabel the location as
   `§Overview` (or "§Overview — 'The remote cache stores two types of
   data'") in the lesson's `## Gate` bullet. No registry cell is affected.
   Severity: cosmetic; the row's own anchor cell points at `§Known issues`,
   which is a real heading and is unaffected.

3. **Source-side drift, not a defect in this revision:** the markdown
   alternate digest recorded in S059's (immutable) anchor cell,
   `0d362d113cdb9c434779bc7601f79844db12339da0207fa2a1b31d5b08badac5`,
   no longer reproduces. Today's live fetch of
   `https://bazel.build/remote/caching.md` returns 16210 B with sha256
   `266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b`
   (stable across four fetch variants and two repeat fetches; the earlier
   round-17 receipt recorded 16722 B for the same URL). The row's anchor cell
   was **not** touched by this revision and, by contract rule 2, cannot be
   edited in place — a correction would have to be a new `supersedes S059 —`
   row. The quoted anchor text still holds substantively: md:343 reads
   `**Bazel does not track tools outside a workspace**` and md:345 reads
   `Bazel currently does not track tools outside a workspace.`
   *Smallest safe correction:* none now; record the upstream change and let the
   next round decide whether the anchor warrants a supersedes row (the row's
   `recheck` is `90d`).

---

## Risks / blockers

* **None blocking.** No E-code, no missing path, no duplicate id, no malformed
  row at either rev; the census validate exits 0 at head and base and the
  fleet-wide sweep is clean.
* The lesson's `## Gate` re-open digest (HTML) reproduces exactly, so the
  round-28 evidence chain is sound; only the two prose nits (observations 1
  and 2) and an upstream page-size change to the markdown alternate
  (observation 3) are open.
* I did not re-run the round-28 C1 cold-read monitor; that is the
  `TameshiR28.RerunC1` seat's item, and running gates in the lane repo is
  outside this seat's bounds. The lane's committed
  `.ufo/evidence/round-28/append-probe.txt` (base 60/64 → SOURCES.md 50/64 →
  all six 47/64) is consistent with the "one blank line on SOURCES.md drops
  10 sections" statement in the appended note.

Report: .ufo/waves/round-28/w1/RerunCensus.md
