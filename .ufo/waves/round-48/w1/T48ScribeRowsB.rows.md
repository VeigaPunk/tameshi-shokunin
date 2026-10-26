# T48ScribeRowsB — C2 row and entry drafts for S093 (→ S267) and S108 (→ S268)

Seat T48ScribeRowsB (leaf, scribe). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at base
`473336d9d789f6081195e7376d17836a24666bc3`. Contract `.ufo/evidence/round-48/contract.json` was read
first, including amendments 1–3. **Nothing in this file is applied to the lane checkout**: it is paste-ready
text for the L1. Every block below was exercised in a throwaway clone at `/fast/scratch/hyaku/tameshi-r48/T48ScribeRowsB/lane`
(sparse checkout of `corpus/`, commits with a scoped throwaway identity, clone deleted before this seat finished);
the scratch clone's HEAD reproduced the C2 draft counter's `REFRESHED` verdict on both targets — §6.

Registry ids used: **S267** for S093, **S268** for S108 (contract: next free id S265; S026 → S265, S048 → S266,
so the C2 set consumes S265–S268). The rows go after `| S264 |` (current line 139), i.e. new lines 140 and 141.

## 1. Registry rows (append to `## Registry` after S264)

The item asks for the anchor digest as `sha256 @SHA:<T>@`. The blocks below carry the substitution already
performed, because the value is known and the row is otherwise broken (`check_snapshot` wants the committed
snapshot's 12-hex prefix *inside* the anchor cell):

- `@SHA:S093@` → `2cb77df2f4be` (`.ufo/evidence/round-48/freshness/sources/S093.xml`, 33 289 B,
  sha256 `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da`, written by T48ExecFetchS093;
  today's own fetch of the raw URL is **byte-identical**, so the value survives a re-fetch)
- `@SHA:S108@` → `04e4c091715a` (`.ufo/evidence/round-48/freshness/sources/S108.html`, 111 409 B,
  sha256 `04e4c091715a9ee2258cb12f52af6c64aa3134c6afc3669501b14f20966d1af1`, written by T48ExecFetchS108;
  see §7 risk 2 — a *fresh* fetch today is 104 928 B, so this value must match whichever bytes the L1 commits,
  not the bytes of a later re-fetch)

```markdown
| S267 | bwrap(1), bubblewrap 0.13.1 — https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml (the tag's raw XML bytes at https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml) | docs | A | supersedes S093's anchor and quote only: the same six flags documented in the raw bwrap.xml at tag v0.13.1, quoted so that --unshare-all's six-flag expansion and the try-else-skip wording of --unshare-cgroup-try sit inside one 25-word quote; not a measured security boundary for any argv | §Options, the --unshare-cgroup-try and --unshare-all varlistentries at bwrap.xml raw lines 153–160 (the quote spans lines 154–159, bytes 5909–6400) @ tag v0.13.1, commit 362936aea0d5c6e70f7af75d2d44b5a914cb4ba2, released 2026-10-14; fetched 2026-10-26; snapshot .ufo/evidence/round-48/freshness/sources/S093.xml 33289 B sha256 2cb77df2f4be | supersedes S093 — the raw XML at v0.13.1 still defines --unshare-all as the six flags --unshare-user-try, --unshare-ipc, --unshare-pid, --unshare-net, --unshare-uts and --unshare-cgroup-try, with the user and cgroup flags worded "if possible else skip it"; score each other flag on its own sentence and read all as that expansion, not as a sealed isolation claim | mined | 2026-10-26 | on-release | corpus/knowledge/regression-tally-completeness.md |
```

```markdown
| S268 | 黄金测试 zh-cn localization (TensorFlow Federated) — https://www.tensorflow.org/federated/golden_tests?hl=zh-cn | docs | B | supersedes S108's anchor and quote only: the same --update_goldens sentence as worded on the official zh-cn page, re-located in a committed 2026-10-26 snapshot; the English upstream row S107 remains the tier-A statement | §如何更新 .expected 文件？, the section's single paragraph at page raw line 3611 (heading at raw line 3609) @ zh-cn page fetched 2026-10-26, last-modified header Tue, 07 Jun 2022 16:32:12 GMT; snapshot .ufo/evidence/round-48/freshness/sources/S108.html 111409 B sha256 04e4c091715a | supersedes S108 — the zh-cn page still states that .expected files are updated by running the affected test with --test_arg=--update_goldens --test_strategy=local and that the resulting diff is checked; the sentence is re-located verbatim in the 2026-10-26 snapshot | mined | 2026-10-26 | 180d | corpus/knowledge/r8-golden-update-flag.md |
```

Field notes: 11 cells, no `|` inside any cell; `teaches` opens `supersedes <T> — ` with U+2014; `used-by` is
exactly the base row's used-by set; `opened` 2026-10-26; `status` mined. S267's `source` cell holds the base
row's GitHub blob URL **and** the raw URL, which is what amendment 1 needs: the receipt url is the raw one, and
`check_row` requires the base URL to be in the row's URL set (source ∪ anchor). S268's `source` url is the
receipt url already.

## 2. Gate lines (for `corpus/lessons/round-48.md`)

Format fixed by amendment 2 (`^- C2-QUOTE (S[0-9]{3,}) (S[0-9]{3,}): `([^`]+)`` — R first, then T, then the
quote in backticks; one line each, no wrapping, nothing between the backticks.)

```markdown
- C2-QUOTE S267 S093: `--unshare-cgroup-try Create a new cgroup namespace if possible else skip it --unshare-all Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try`
- C2-QUOTE S268 S108: `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。`
```

Token counts under the amendment-2 rule (whitespace-split): S267 quote **25** tokens — exactly at the cap;
S268 quote **6** tokens. Both quotes are whitespace-collapsed already and occur **once** in the amendment-2
extracted text of the committed snapshot (S093: offset 2 641 of 16 699 chars; S108: offset 2 533 of 3 496 chars).
Provenance: I re-derived both quotes myself from the committed snapshots and from my own live fetches, and they
agree verbatim with the quotes proposed by T48ExecFetchS093 and T48ExecFetchS108 — the fetch seats' quotes are
used as proposed, not replaced. The S267 quote can be shortened to 14 tokens by dropping the `--unshare-cgroup-try`
definition, but then the cgroup try-else-skip wording that the row's `teaches` claims would no longer be quoted;
the 25-token form is the one that answers round-45's dispute (`CritJudge03`: the old fragment "never names
--unshare-all … truncates before the sixth flag").

## 3. Entry edits (two lines each: `source:` and `verified-at:`)

### 3a. `corpus/knowledge/regression-tally-completeness.md` (S093's only base used-by path)

Line 1 currently reads:

```markdown
source: S087 — mutation-testing-metrics 3.9.0, `package/src/calculateMetrics.ts` and `package/src/model/metrics.ts` (external metric arithmetic, not tameshi's own kill-rate formula; re-opened round 30, `.ufo/waves/round-30/wA/ReopenS087.md`); S093 — bwrap(1), bubblewrap 0.13.1 `bwrap.xml` (the sandbox the v4 counter runs each selftest in); S094 — Dwork et al., arXiv:1411.2664v3 §1 (a held-out test kept from the candidate)
```

Replace line 1 with:

```markdown
source: S087 — mutation-testing-metrics 3.9.0, `package/src/calculateMetrics.ts` and `package/src/model/metrics.ts` (external metric arithmetic, not tameshi's own kill-rate formula; re-opened round 30, `.ufo/waves/round-30/wA/ReopenS087.md`); S093 — bwrap(1), bubblewrap 0.13.1 `bwrap.xml` (the sandbox the v4 counter runs each selftest in); S267 — the same bwrap.xml at tag v0.13.1, re-anchored 2026-10-26 from the raw XML (supersedes S093's anchor and quote); S094 — Dwork et al., arXiv:1411.2664v3 §1 (a held-out test kept from the candidate)
```

Line 2 currently reads:

```markdown
verified-at: 2026-10-23 — sources re-opened by round-30 wave-A seats; fix, counters, amendments 1-4 and pre-data control receipts inspected; this entry records no lane-head measurement
```

Replace line 2 with:

```markdown
verified-at: 2026-10-26 — S267 re-opened live: raw bwrap.xml at tag v0.13.1, sha256 2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da (33289 B), unchanged from the row's pin, with the six --unshare-all flags and both try-else-skip sentences re-read; S087 and S094, the fix, the counters, amendments 1-4 and the pre-data control receipts were inspected by round-30 wave-A seats and are not re-inspected in this re-anchor; this entry records no lane-head measurement
```

Line 3 (`recheck: …`) is **not** touched: it is a recipe plus the list of sources to re-open, still true.
The body's citations of S093 stay as they are (§5 below says why every one of them still holds); no body line
is edited, so nothing reads as a claim that was silently re-scoped.

### 3b. `corpus/knowledge/r8-golden-update-flag.md` (S108's only base used-by path)

Line 1 currently reads:

```markdown
source: S107 — https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md — §How do I update `.expected` files?; S108 — https://www.tensorflow.org/federated/golden_tests?hl=zh-cn — 如何更新 .expected 文件？
```

Replace line 1 with (S107 and its URL kept byte-for-byte, S108 and its URL kept, S268 added):

```markdown
source: S107 — https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md — §How do I update `.expected` files?; S108 — https://www.tensorflow.org/federated/golden_tests?hl=zh-cn — 如何更新 .expected 文件？; S268 — the same zh-cn URL, re-anchored 2026-10-26 (supersedes S108's anchor and quote)
```

Line 2 currently reads:

```markdown
verified-at: 2026-10-24
```

Replace line 2 with:

```markdown
verified-at: 2026-10-26 — the zh-cn page re-opened live: its §如何更新 .expected 文件？ heading and paragraph are unchanged and the paragraph is re-located in the 2026-10-26 snapshot; a line diff against today's live fetch (104928 B) finds only the head hreflang link block, the language-selector menu and the per-request script blocks (analytics JSON, CSP nonce, devsite flag list), so the extracted article text is identical; S107 is fetched from a commit-pinned URL and was not re-fetched
```

Line 3 (`recheck: 365d`) and line 4 (`ground: F4 …`) are untouched.

Style note: this follows the item's "keeping the old URL, adding the new id" literally — both ids stay on the
line, as in `corpus/knowledge/incremental-pin-disposition.md` where S041 and its superseding row S047 are cited
together. The other house precedent (`corpus/knowledge/r44-anchor-refresh-rule.md`) cites only the superseding
row; if the L1 prefers that, delete `S093 — … ; ` respectively `S108 — … ; ` from each line — the counter only
requires the new id to be **present** in `source:` (and 2026-10-26 in `verified-at:`) and requires the entry's
path to be the row's `used-by`.

## 4. Gate block prose (CORPUS.md rule 1: URL, access date, located quote with its location)

Two subsections, in the round-45 house style (`corpus/lessons/round-45.md:16-62`).

````markdown
### Supersede — S267 (new row): bwrap(1), bubblewrap 0.13.1, raw `bwrap.xml`

- URL https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml (row's source cell); the fetched bytes
  are the tag's raw file https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml; access date
  2026-10-26; 33 289 bytes. Snapshot `.ufo/evidence/round-48/freshness/sources/S093.xml`, SHA-256
  `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da`; fetch receipt
  `S093.receipt.json` (http_status 200, fetched_at 2026-10-26T08:41:10Z, same digest and byte count).
  This digest is the row's own pin, so the re-anchor changes no bytes' identity — only the quote.
- Located quote (amendment-2 extraction of the snapshot: UTF-8, no script/style content, tags stripped,
  entities unescaped, whitespace collapsed; found once, at normalized offset 2 641 of 16 699 characters;
  **25 tokens**):
  - `<quote>` — spans two consecutive `<varlistentry>` blocks of §Options: `--unshare-cgroup-try` at raw lines
    153–156 and `--unshare-all` at raw lines 157–160; quote lines 154–159, bytes 5 909–6 400.
- Scope: the raw bwrap.xml at tag v0.13.1 documents `--unshare-all` as "Unshare all possible namespaces.
  Currently equivalent with:" the six flags `--unshare-user-try`, `--unshare-ipc`, `--unshare-pid`,
  `--unshare-net`, `--unshare-uts`, `--unshare-cgroup-try`, with `--unshare-user-try` (raw lines 130–131) and
  `--unshare-cgroup-try` (line 155) worded "if possible else skip it". It is not a measured security boundary
  for any argv, and nothing here claims one.
- Row change: `corpus/SOURCES.md:140` appends S267 as `docs`/`A`/`mined`, opened 2026-10-26, recheck
  `on-release`, anchor `§Options, the --unshare-cgroup-try and --unshare-all varlistentries at bwrap.xml raw
  lines 153–160 … snapshot .ufo/evidence/round-48/freshness/sources/S093.xml 33289 B sha256 2cb77df2f4be`,
  `used-by` `corpus/knowledge/regression-tally-completeness.md`.
- Cited by `corpus/knowledge/regression-tally-completeness.md` (`source:` S267 on line 1, `verified-at:
  2026-10-26` on line 2). Answers round-45's dispute of S093 (`CritJudge03`): the quote now names
  `--unshare-all`, carries its six-flag expansion whole and reaches the sixth flag with its try-else-skip
  wording.

### Supersede — S268 (new row): 黄金测试 zh-cn localization (TensorFlow Federated)

- URL https://www.tensorflow.org/federated/golden_tests?hl=zh-cn; access date 2026-10-26; 111 409 bytes;
  response `last-modified: Tue, 07 Jun 2022 16:32:12 GMT`. Snapshot
  `.ufo/evidence/round-48/freshness/sources/S108.html`, SHA-256
  `04e4c091715a9ee2258cb12f52af6c64aa3134c6afc3669501b14f20966d1af1`; fetch receipt `S108.receipt.json`
  (http_status 200, fetched_at 2026-10-26T08:41:18Z, same digest and byte count).
- Located quote (amendment-2 extraction; found once, at offset 2 533 of 3 496 characters; **6 tokens**):
  - `<quote>` — the single `<p>` of the section `如何更新 .expected 文件？`, raw line 3611 (the `<h2>` is raw
    line 3609), inside the article body after the `path/ to/ some_test_goldens/` listing.
- Scope: the zh-cn page's wording only — `.expected` files are updated by running the affected test with
  `--test_arg=--update_goldens --test_strategy=local`, and the resulting diff is checked. The English upstream
  row S107 (commit-pinned) stays the tier-A statement; this row is tier B for the wording on this page.
- Row change: `corpus/SOURCES.md:141` appends S268 as `docs`/`B`/`mined`, opened 2026-10-26, recheck `180d`,
  anchor `§如何更新 .expected 文件？, the section's single paragraph at page raw line 3611 … snapshot
  .ufo/evidence/round-48/freshness/sources/S108.html 111409 B sha256 04e4c091715a`, `used-by`
  `corpus/knowledge/r8-golden-update-flag.md`.
- Cited by `corpus/knowledge/r8-golden-update-flag.md` (`source:` S268 on line 1, `verified-at: 2026-10-26`
  on line 2). Round 45 raised no dispute for S108 (`reviews.json`: `RevJudge02` → `agree`).
````

In both subsections `<quote>` is the §2 line's backticked text, verbatim, so the prose and the machine-read
line cannot drift apart.

## 5. The citing entries' claims, re-checked against the live sources

Every line below was read in the live bytes I fetched on 2026-10-26, not in a cached copy. No claim failed;
there is nothing to report as a finding, so no body line is edited.

### 5a. `regression-tally-completeness.md` (S093)

| entry line | claim | live text (S093 raw, tag v0.13.1) | verdict |
|---|---|---|---|
| 1 | S093 is "bwrap(1), bubblewrap 0.13.1 `bwrap.xml` (the sandbox the v4 counter runs each selftest in)" | the fetched document is that file: DocBook `<refentry>` for `bwrap`, tag v0.13.1, 33 289 B, sha256 `2cb77df2…` — the row's own pin | holds |
| 42 | the v4 counter "runs each `--selftest` in a bubblewrap sandbox (S093)" | historical statement about round-30's counter, not a claim about the document; the document is the `bwrap` man page it names | holds (unchanged by this round) |
| 68 | "S093's `--unshare-all` is six flags, two of them try-else-skip" | line 159: `Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try`; line 131: `Create a new user namespace if possible else skip it`; line 155: `Create a new cgroup namespace if possible else skip it` — six flags, exactly two worded try-else-skip | holds |
| 72 (errata E1) | "S093 bwrap.xml:233-235: `--clearenv` unsets all variables \"except for PWD and any that are subsequently set by --setenv\"" | lines 233–235 are exactly `Unset all environment variables, except for <envar>PWD</envar> and any that are subsequently set by <option>--setenv</option>` — the quoted words are contiguous after tag stripping, and the line numbers are unchanged | holds |

The base row S093's other anchor line numbers are also still exact in the live bytes (independently re-read
here, not taken from the fetch seat): `:159` `--unshare-all` listitem; `:233-235` `--clearenv`; `:403`
`Mount procfs on <arg>DEST</arg>`; `:412-416` tmpfs with mode 0755 / `--perms` / `--size`; `:575-577`
`Create a new terminal session for the sandbox (calls setsid())`; `:589-592` `Ensures child process (COMMAND)
dies when bwrap's parent dies … PR_SET_PDEATHSIG`.

### 5b. `r8-golden-update-flag.md` (S108)

| entry line | claim | live text (zh-cn page, 2026-10-26) | verdict |
|---|---|---|---|
| 1 | the zh-cn source is the section `如何更新 .expected 文件？` | the live page carries `<h2 id="如何更新_expected_文件？" …>如何更新  <code>.expected</code> 文件？</h2>` (raw line 3493 of today's fetch) | holds |
| 5 | "The same page's official zh-cn localization restates that flag and the diff check." | `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。` — the flag **and** the diff check, in one sentence | holds |
| 5 | "The upstream markdown is the tier-A statement; the localization is tier B for the wording on that page" | S107 is a commit-pinned raw URL (`4d3a89c9…`); this row stays tier B | holds |

## 6. Probe evidence (scratch clone, no verdict scored)

Bounds observed: lane checkout untouched (no write, no index change, no jj command); one live clone at
`/fast/scratch/hyaku/tameshi-r48/T48ScribeRowsB/lane` (`git clone -q --shared --no-checkout`, sparse checkout of
`corpus/`), commits made only inside that clone with `-c user.name/'user.email'` scoped to the command;
`TMPDIR` inside the scratch dir; scratch dir deleted at the end of the seat.

- The draft counter `.ufo/waves/round-48/w1/T48ExecC2Counter.measure.py --lane <clone> --rev HEAD --no-live`
  printed, with the §1–§3 text applied in the clone:
  `TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED` and
  `TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED`, with
  `census_exit=0`; S026/S048 read `row=none` only because they are other seats' rows.
- The same run **with live on** printed `live=ok` for both targets (`refreshed=2`, `census_exit=0`): the receipt
  URLs returned 200 and the quotes are located in today's live extracted text.
- With the digest placeholder left unsubstituted the counter prints `snapshot=sha` — the placeholder must be
  replaced, which is why §1 carries the values.
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file …` on the base registry vs the
  registry with S267/S268 added: the new output adds exactly two lines and removes none —
  `W04 S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes` and
  `W04 S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes`; no E-code for
  either row (E04 is avoided twice over: the scope text differs from the base row's, and `teaches` opens with
  `supersedes S…`). The counter's own census run — which materialises every used-by path — exits 0 both at
  BASE and at the content revision.
- Amendment-1 check: the S267 `source` cell's URL set is {blob URL, raw URL} ⊇ {S093's base URL} and holds the
  receipt url (the raw one); S268's URL set is the base URL, which is also the receipt url.

## 7. What the L1 must still do, and the risks

1. **Relocate the snapshots.** The committed bytes live at
   `.ufo/waves/round-48/w1/sources/{S093.xml,S093.receipt.json,S108.html,S108.receipt.json}` but the counter
   reads `.ufo/evidence/round-48/freshness/sources/` (`SNAP_DIR`) and takes the file name's stem as the target.
   Copy them to the evidence path unchanged and commit them there; my rows' anchors already name that path.
   A name change during the move breaks `check_snapshot` (`absent`).
2. **S108 is byte-unstable live.** Today's own fetch is 104 928 B (sha256
   `d590e8dd2d376e6aaa07da8b277a6dd7d86065b4548f33a2a53af2f3b087a6f0`) against the committed 111 409 B
   (`04e4c091715a…`). The whole difference is the head `hreflang` link block, the language-selector menu and
   three per-request script blocks (analytics JSON, CSP nonce, devsite flag list); the amendment-2 extracted
   text differs only by the language-name list the snapshot carries twice, and the quote is located in **both**
   texts, so the live check passes. Consequence: the anchor digest must be the digest of the bytes actually
   committed (04e4c091715a today), and any seat that re-fetches before committing must re-derive it. The
   counter never compares live bytes to the snapshot (only receipt↔snapshot), so this is a row-text risk, not
   a predicate risk.
3. **The S267 quote is exactly at the 25-token cap.** It is 25 under amendment-2 whitespace splitting; a
   counter that tokenises differently (e.g. splitting `with:`) would push it to 26. If the L1 freezes a
   stricter counter, substitute the 14-token form
   `--unshare-all Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try`
   (still contains both required phrases, but drops the cgroup try-else-skip wording — then also soften
   `teaches`' "if possible else skip it" clause). Do not do this silently: it weakens the answer to round-45's
   dispute.
4. **Two new W04 warnings are expected** (`S267`, `S268`), one per supersede row, because the URL is reused
   in a second scope. They are warnings: `census_exit=0` both at base and with the rows. Reusing the base
   row's scope text verbatim would have produced E04 instead, which is why the scope cells differ.
5. **Id collision.** S267/S268 must be free at the moment of landing; if another wave-1 seat takes them, the
   row id, the Gate line's first field and nothing else change (the entries do not name the id twice).
6. **Out of scope, flagged only:** S093 is cited outside its `used-by` cell in
   `corpus/lessons/round-30.md:16,36-38,51-52,57`, `corpus/lessons/round-30-verifier-spotcheck.md:159,193`,
   `corpus/lessons/round-45.md:162`, `corpus/lessons/round-45-verifier-spotcheck.md:34-36,73` (found by
   T48ExecFetchS093 and not re-enumerated by me). The frozen C2 statement only covers the knowledge entries
   in the base `used-by` cells, so these are not re-pointed here; a lesson that cites S093 as a live source
   would need its own note if the L1 wants one.

## 8. Tooling

No tool was installed or upgraded; `pacman` was not invoked (transaction pause respected). `curl 8.23.0`,
`git`, `python3` and `bash` were already present.

